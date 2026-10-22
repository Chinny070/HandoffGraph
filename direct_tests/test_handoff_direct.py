"""Real GenVM Direct Mode contract smoke tests. NEVER count as passed until `gltest` runs.

This suite runs in GenLayer's runtime adapter, not in the offline mock.
The source-backed semantic success/falsification matrix is a mandatory extension
before a deployment is called ready. See docs/DEPLOYMENT_GATES.md.
"""
import os

import pytest

# Pinned: Direct Mode otherwise resolves the newest GenVM release, which may lack the needed asset.
GENVM_SDK_VERSION = os.environ.get('HANDOFF_GENVM_VERSION', 'v0.2.16')

RULE = 'The published delivery report documents exactly three validated output records.'
ZERO = 0


def setup_one(direct_deploy, direct_vm, direct_alice):
    c = direct_deploy('contracts/handoff_graph.py', sdk_version=GENVM_SDK_VERSION)
    owner = direct_vm.sender
    w = c.create_workflow('Direct', 'Source-bound review and final release')
    s = c.add_stage(w, 'Output', direct_alice, owner, RULE, ZERO, ZERO, ZERO)
    return c, w, s, owner


def test_workflow_can_seal_in_genvm(direct_deploy, direct_vm, direct_alice):
    c, w, s, owner = setup_one(direct_deploy, direct_vm, direct_alice)
    assert len(c.seal_workflow(w)) == 64
    assert c.get_workflow(w)['sealed'] is True
    assert c.get_stage(s)['state'] == 1


def test_nonowner_cannot_seal(direct_deploy, direct_vm, direct_alice):
    c,w,s,_ = setup_one(direct_deploy, direct_vm, direct_alice)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert('ONLY_OWNER'):
            c.seal_workflow(w)


def test_no_new_stages_after_seal(direct_deploy, direct_vm, direct_alice):
    c,w,s,owner = setup_one(direct_deploy, direct_vm, direct_alice)
    c.seal_workflow(w)
    with direct_vm.expect_revert('GRAPH_SEALED'):
        c.add_stage(w,'Extra',direct_alice,owner,RULE,0,0,0)


def test_worker_cannot_self_review(direct_deploy, direct_vm, direct_alice):
    c,w,s,owner = setup_one(direct_deploy, direct_vm, direct_alice)
    with direct_vm.expect_revert('REVIEWER_MUST_BE_INDEPENDENT'):
        c.add_stage(w,'Second',direct_alice,direct_alice,RULE,0,0,0)


def test_graph_dependency_gate(direct_deploy, direct_vm, direct_alice):
    c,w,s,owner = setup_one(direct_deploy, direct_vm, direct_alice)
    d = c.add_stage(w,'Follow-up',direct_alice,owner,RULE,s,0,0)
    c.seal_workflow(w)
    assert c.can_submit(d) is False
    assert c.get_stage(d)['dependencies'] == [s]


def test_owner_freeze_expires_at_transaction_clock(direct_deploy, direct_vm, direct_alice):
    c,w,s,owner = setup_one(direct_deploy, direct_vm, direct_alice)
    c.seal_workflow(w)
    c.freeze(w)
    assert c.can_submit(s) is False
    # GenLayer Direct Mode's warp is explicitly documented in the current SDK.
    direct_vm.warp('2030-01-01T00:00:00+00:00')
    assert c.can_submit(s) is True


def test_unknown_graph_fails_closed(direct_deploy, direct_vm, direct_alice):
    c,w,s,owner = setup_one(direct_deploy, direct_vm, direct_alice)
    assert c.can_release(500000,'0'*64) is False
    assert c.can_submit(500000) is False


def test_duplicate_dependency_rejected(direct_deploy, direct_vm, direct_alice):
    c,w,s,owner = setup_one(direct_deploy, direct_vm, direct_alice)
    with direct_vm.expect_revert('DUPLICATE_DEPENDENCY'):
        c.add_stage(w,'Other',direct_alice,owner,RULE,s,s,0)


def test_requirement_registration_and_seal_in_genvm(direct_deploy, direct_vm, direct_alice):
    c,w,s,_=setup_one(direct_deploy,direct_vm,direct_alice)
    c.add_requirement(s,'The CSV contains exactly three unique records')
    c.add_requirement(s,'A parsing report documents schema compliance')
    c.seal_workflow(w)
    assert len(c.get_stage(s)['requirements'])==2
    with direct_vm.expect_revert('GRAPH_SEALED'):
        c.add_requirement(s,'Post-seal rule injection')


def test_source_pin_requires_commit_sha_in_genvm(direct_deploy, direct_vm, direct_alice):
    c,w,s,_=setup_one(direct_deploy,direct_vm,direct_alice)
    c.seal_workflow(w)
    with direct_vm.prank(direct_alice):
        with direct_vm.expect_revert('INVALID_PINNED_SOURCE'):
            c.submit(s,'alleged work','https://raw.githubusercontent.com/x/y/main/file.txt','0'*64)


def test_countercase_not_open_before_release_in_genvm(direct_deploy, direct_vm, direct_alice):
    c,w,s,_=setup_one(direct_deploy,direct_vm,direct_alice)
    c.seal_workflow(w)
    with direct_vm.expect_revert('COUNTER_NOT_ELIGIBLE'):
        c.open_counterexample(s,'allegation','https://raw.githubusercontent.com/x/y/'+'a'*40+'/file.txt','0'*64)


def test_initial_final_active_requires_release_in_genvm(direct_deploy, direct_vm, direct_alice):
    c,w,s,_=setup_one(direct_deploy,direct_vm,direct_alice)
    c.seal_workflow(w)
    assert c.is_release_active(s,'0'*64) is False
    assert c.can_submit(s)
    assert c.can_release(s,'0'*64) is False


def test_preseal_bad_delivery_deadline_in_genvm(direct_deploy, direct_vm, direct_alice):
    c,w,s,_=setup_one(direct_deploy,direct_vm,direct_alice)
    with direct_vm.expect_revert('INVALID_DEADLINE'):
        c.set_delivery_timeout(s,1)
    c.set_delivery_timeout(s,3600)
    c.seal_workflow(w)
    assert c.get_stage(s)['delivery_deadline'] > 0
