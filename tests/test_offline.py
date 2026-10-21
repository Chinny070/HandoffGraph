"""Offline state-machine security tests; does NOT claim validator/network execution."""
import pytest
import hashlib

OWNER = '0x'+'11'*20
WORKER = '0x'+'22'*20
REVIEWER = '0x'+'33'*20
OTHER = '0x'+'44'*20
WORKER2 = '0x'+'55'*20
REVIEWER2 = '0x'+'66'*20
CRITERION = 'A documented JSON export shall contain exactly 3 valid records and a reproducible schema.'
EVIDENCE = 'A reproducible source artifact contains schema examples.'
ARTIFACT_URL = 'https://raw.githubusercontent.com/example/project/' + 'a'*40 + '/README.md'
ARTIFACT_SHA = hashlib.sha256(b'Verified public source text for deterministic offline tests.').hexdigest()


def decision(d='PASS', c='COMPLETE', risk=False, gap='NONE'):
    return {'decision':d,'coverage':c,'risk':risk,'gap':gap,'explanation':'The supplied material covers the stated criteria.'}


def make(env, cast, two=True):
    m, c, state, _ = env
    cast(OWNER)
    wid = c.create_workflow('Pipeline', 'Agent coordination with accountable handoff checks')
    first = c.add_stage(wid,'Extract',WORKER,REVIEWER,CRITERION,0,0,0)
    second = c.add_stage(wid,'Integrate',WORKER2,REVIEWER2,
        'Consume the verified export without losing records.', first,0,0) if two else None
    c.seal_workflow(wid)
    return wid, first, second


def submit(env, cast, sid, who=WORKER):
    m, c, state, gl = env
    cast(who)
    return c.submit(sid, EVIDENCE, ARTIFACT_URL, ARTIFACT_SHA)


def judged(env, cast, sid, result=None):
    m, c, state, gl = env
    state['now'] += m.REVIEW_SECONDS
    state['script'] = [result or decision()]
    did = c.assess(sid)
    return did


def finalize(env, sid):
    m,c,state,_ = env
    state['now'] += m.APPEAL_SECONDS
    return c.finalize_unappealed(sid)


def complete(env, cast, sid):
    submit(env,cast,sid)
    judged(env,cast,sid)
    receipt = finalize(env,sid)
    cast(OWNER)
    c=env[1]
    c.release(sid,receipt)
    return receipt


def assert_error(message, fn):
    with pytest.raises(Exception, match=message):
        fn()


def test_workflow_root_is_64_hex(env,cast):
    wid, sid, dep = make(env,cast)
    assert len(env[1].get_workflow(wid)['root']) == 64
    assert env[1].get_workflow(wid)['sealed']


def test_owner_is_bound_at_creation(env,cast):
    wid,sid,_ = make(env,cast)
    assert env[1].get_workflow(wid)['owner'] == OWNER


def test_must_seal_nonempty(env,cast):
    cast(OWNER); c=env[1]
    w=c.create_workflow('X','P')
    assert_error('EMPTY_WORKFLOW',lambda:c.seal_workflow(w))


def test_nonowner_cannot_add_stage(env,cast):
    cast(OWNER); c=env[1]
    w=c.create_workflow('X','P')
    cast(OTHER)
    assert_error('ONLY_OWNER',lambda:c.add_stage(w,'a',WORKER,REVIEWER,CRITERION,0,0,0))


def test_seal_is_permanent(env,cast):
    w,s,_=make(env,cast)
    assert_error('ALREADY_SEALED',lambda:env[1].seal_workflow(w))


def test_no_postseal_nodes(env,cast):
    w,s,_=make(env,cast)
    assert_error('GRAPH_SEALED',lambda:env[1].add_stage(w,'x',WORKER,REVIEWER,CRITERION,0,0,0))


def test_no_self_review(env,cast):
    cast(OWNER); c=env[1]; w=c.create_workflow('X','P')
    assert_error('REVIEWER_MUST_BE_INDEPENDENT',lambda:c.add_stage(w,'x',WORKER,WORKER,CRITERION,0,0,0))


def test_cross_workflow_dependency_rejected(env,cast):
    cast(OWNER); c=env[1]; wa=c.create_workflow('A','P'); wb=c.create_workflow('B','P')
    a=c.add_stage(wa,'a',WORKER,REVIEWER,CRITERION,0,0,0)
    assert_error('CROSS_WORKFLOW_DEPENDENCY',lambda:c.add_stage(wb,'b',WORKER2,REVIEWER2,CRITERION,a,0,0))


def test_unknown_dependency_rejected(env,cast):
    cast(OWNER); c=env[1]; w=c.create_workflow('A','P')
    assert_error('UNKNOWN_STAGE',lambda:c.add_stage(w,'b',WORKER,REVIEWER,CRITERION,9000,0,0))


def test_duplicate_dependency_rejected(env,cast):
    cast(OWNER); c=env[1]; w=c.create_workflow('A','P')
    s=c.add_stage(w,'a',WORKER,REVIEWER,CRITERION,0,0,0)
    assert_error('DUPLICATE_DEPENDENCY',lambda:c.add_stage(w,'b',WORKER2,REVIEWER2,CRITERION,s,s,0))


def test_dag_dependencies_precede_child(env,cast):
    w,s,child=make(env,cast)
    assert s < child
    assert env[1].get_stage(child)['dependencies']==[s]


def test_worker_only_submission(env,cast):
    _,s,_=make(env,cast)
    cast(OTHER)
    assert_error('ONLY_WORKER',lambda:env[1].submit(s,EVIDENCE,ARTIFACT_URL,ARTIFACT_SHA))


def test_downstream_cannot_submit_before_final_release(env,cast):
    _,s,child=make(env,cast)
    cast(WORKER2)
    assert not env[1].can_submit(child)
    assert_error('PREREQUISITES_NOT_RELEASED',lambda:env[1].submit(child,EVIDENCE,ARTIFACT_URL,ARTIFACT_SHA))


def test_submit_binds_digest(env,cast):
    _,s,_=make(env,cast)
    sha=submit(env,cast,s)
    assert len(sha)==64
    assert sha==env[1].get_stage(s)['submission_hash']


def test_double_submit_prevented(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s)
    assert_error('NOT_READY',lambda:env[1].submit(s,EVIDENCE,ARTIFACT_URL,ARTIFACT_SHA))


def test_nonreviewer_cannot_challenge(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s)
    cast(OTHER)
    assert_error('ONLY_REVIEWER',lambda:env[1].challenge(s,'bad'))


def test_reviewer_can_challenge(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s)
    cast(REVIEWER); env[1].challenge(s,'Missing export row')
    assert env[1].get_stage(s)['state']==env[0].DISPUTED


def test_challenge_window_closes(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    env[2]['now'] += env[0].REVIEW_SECONDS
    cast(REVIEWER)
    assert_error('CHALLENGE_WINDOW_CLOSED',lambda:env[1].challenge(s,'late'))


def test_assessment_waits_for_window(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    assert_error('REVIEW_WINDOW_OPEN',lambda:env[1].assess(s))


def test_dispute_can_be_assessed_early(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    cast(REVIEWER); env[1].challenge(s,'missing evidence')
    env[2]['script']=[decision('FAIL','MISSING',True,'MISSING_EXPORT')]
    assert env[1].assess(s)==1


def test_verdict_provisional_not_release(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    cast(OWNER)
    assert_error('NOT_FINAL_PASS',lambda:env[1].release(s,'x'*64))


def test_appeal_deadline_enforced(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    assert_error('APPEAL_WINDOW_OPEN',lambda:env[1].finalize_unappealed(s))


def test_permissionless_finalization_after_deadline(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    cast(OTHER)
    sha=finalize(env,s)
    assert len(sha)==64 and env[1].get_stage(s)['state']==env[0].PASSED


def test_failed_judgment_never_releases(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    judged(env,cast,s,decision('FAIL','MISSING',True,'MISSING_EXPORT'))
    sha=finalize(env,s); cast(OWNER)
    assert not env[1].can_release(s,sha)
    assert_error('NOT_FINAL_PASS',lambda:env[1].release(s,sha))


def test_partial_fails_closed(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    judged(env,cast,s,decision('PARTIAL','MISSING',False,'PARTIAL_DELIVERY'))
    finalize(env,s)
    assert env[1].get_stage(s)['state']==env[0].FAILED


def test_unknown_fails_closed(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    judged(env,cast,s,decision('UNKNOWN','UNVERIFIABLE',True,'NO_SOURCE'))
    finalize(env,s)
    assert env[1].get_stage(s)['state']==env[0].FAILED


def test_release_and_dependency_unblock(env,cast):
    _,s,child=make(env,cast)
    complete(env,cast,s)
    assert env[1].can_submit(child)
    cast(WORKER2)
    assert len(env[1].submit(child,EVIDENCE,ARTIFACT_URL,ARTIFACT_SHA))==64


def test_double_release_blocked(env,cast):
    _,s,_=make(env,cast); sha=complete(env,cast,s)
    assert_error('ALREADY_RELEASED',lambda:env[1].release(s,sha))


def test_wrong_receipt_rejected(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s); judged(env,cast,s); finalize(env,s); cast(OWNER)
    assert_error('STALE_RECEIPT',lambda:env[1].release(s,'0'*64))


def test_appeal_changes_fail_to_pass(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    judged(env,cast,s,decision('FAIL','MISSING',True,'INCOMPLETE'))
    cast(WORKER); env[1].appeal(s,'Independent reproduction notes attached')
    env[2]['script']=[decision()]
    r=env[1].resolve_appeal(s)
    assert env[1].get_stage(s)['state']==env[0].PASSED
    assert env[1].get_decision(1)['appeal_verdict']==env[0].PASS
    assert len(r)==64


def test_appeal_changes_pass_to_fail(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    cast(REVIEWER); env[1].appeal(s,'Found conflicting row evidence')
    env[2]['script']=[decision('FAIL','CONFLICTING',True,'CONFLICT')]
    env[1].resolve_appeal(s)
    assert env[1].get_stage(s)['state']==env[0].FAILED


def test_nonparty_cannot_appeal(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    cast(OTHER)
    assert_error('NO_APPEAL_STANDING',lambda:env[1].appeal(s,'grounds'))


def test_no_double_appeal(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    cast(WORKER); env[1].appeal(s,'grounds')
    assert_error('NOT_APPEALABLE',lambda:env[1].appeal(s,'more grounds'))


def test_can_retry_failed_preserving_decision(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    judged(env,cast,s,decision('FAIL','MISSING',True,'NO_EXPORT')); finalize(env,s)
    original=env[1].get_decision(1)
    cast(WORKER); env[1].retry_failed(s)
    assert env[1].can_submit(s)
    assert env[1].get_decision(1)==original


def test_retry_is_bounded(env,cast):
    _,s,_=make(env,cast)
    for i in range(3):
        submit(env,cast,s); judged(env,cast,s,decision('FAIL','MISSING',True,'MISSING'))
        finalize(env,s)
        if i<2:
            cast(WORKER); env[1].retry_failed(s)
    cast(WORKER)
    assert_error('ATTEMPT_LIMIT',lambda:env[1].retry_failed(s))


def test_freeze_blocks_new_submissions_not_finality(env,cast):
    w,s,_=make(env,cast)
    submit(env,cast,s)
    cast(OWNER); env[1].freeze(w)
    judged(env,cast,s)
    # Finalization can proceed while/after a freeze; no owner approval needed.
    assert len(finalize(env,s))==64
    assert env[1].get_stage(s)['state']==env[0].PASSED


def test_freeze_blocks_release(env,cast):
    w,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s); r=finalize(env,s)
    cast(OWNER); env[1].freeze(w)
    assert_error('WORKFLOW_FROZEN',lambda:env[1].release(s,r))


def test_freeze_expires_without_owner(env,cast):
    w,s,_=make(env,cast)
    cast(OWNER); env[1].freeze(w)
    assert not env[1].can_submit(s)
    env[2]['now']+=env[0].FREEZE_SECONDS
    assert env[1].can_submit(s)


def test_freeze_limited(env,cast):
    w,s,_=make(env,cast)
    cast(OWNER); env[1].freeze(w)
    env[2]['now']+=env[0].FREEZE_SECONDS
    env[1].freeze(w)
    env[2]['now']+=env[0].FREEZE_SECONDS
    assert_error('FREEZE_LIMIT',lambda:env[1].freeze(w))


def test_owner_can_thaw(env,cast):
    w,s,_=make(env,cast)
    cast(OWNER); env[1].freeze(w); env[1].thaw(w)
    assert env[1].can_submit(s)


def test_validator_rejects_malicious_leader(env,cast):
    m,c,state,gl=env
    _,s,_=make(env,cast)
    submit(env,cast,s); judged(env,cast,s)
    state['script']=[decision('FAIL','MISSING',True,'MATERIAL_GAP')]
    assert state['validator'](gl.vm.Return(decision_as_norm(m))) is False


def decision_as_norm(m):
    return {'decision':m.PASS,'coverage':m.COMPLETE,'risk':False,'gap':'NONE','explanation':'valid','source_ok':True}


def test_validator_agree_then_falsification_accepts(env,cast):
    m,c,state,gl=env
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    state['script']=[decision(), {'material_gap':False,'contradiction':False,'unverifiable':False}]
    assert state['validator'](gl.vm.Return(decision_as_norm(m))) is True


def test_validator_adversarial_veto(env,cast):
    m,c,state,gl=env
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    state['script']=[decision(), {'material_gap':True,'contradiction':False,'unverifiable':False}]
    assert state['validator'](gl.vm.Return(decision_as_norm(m))) is False


def test_validator_rejects_malformed_falsification(env,cast):
    m,c,state,gl=env
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    state['script']=[decision(), {'material_gap':'false','contradiction':False,'unverifiable':False}]
    assert state['validator'](gl.vm.Return(decision_as_norm(m))) is False


def test_validator_requires_vm_return(env,cast):
    m,c,state,gl=env
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    assert state['validator'](decision_as_norm(m)) is False


@pytest.mark.parametrize('malformed', [None, 'PASS', [], {},
 {'decision':'PASS','coverage':'COMPLETE','risk':'false','gap':'NONE','explanation':'x'},
 {'decision':'PASS','coverage':'MISSING','risk':False,'gap':'NONE','explanation':'x'},
 {'decision':'PASS','coverage':'COMPLETE','risk':True,'gap':'NONE','explanation':'x'},
 {'decision':'PARTIAL','coverage':'MISSING','risk':False,'gap':'NONE','explanation':'x'},
 {'decision':'PASS','coverage':'COMPLETE','risk':False,'gap':'../../','explanation':'x'}])
def test_malformed_verdict_does_not_pass(env,malformed):
    m,*_=env
    assert m.verdict(malformed)['decision'] != m.PASS


def test_no_funds_and_no_upgrade_entrypoint(env):
    m,c,_,_=env
    api=[x for x in dir(c) if not x.startswith('_')]
    assert all(x not in api for x in ('withdraw','upgrade','transfer','mint','pay','override_verdict'))


def test_anyone_can_release_final_jury_pass(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s); judged(env,cast,s); receipt=finalize(env,s)
    cast(OTHER)
    assert env[1].release(s,receipt)==receipt


def test_nonowner_cannot_freeze(env,cast):
    w,s,_=make(env,cast)
    cast(OTHER)
    assert_error('ONLY_OWNER',lambda:env[1].freeze(w))


def test_false_positive_is_not_proof_of_live_consensus(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s)
    # This offline double deliberately returns leader output WITHOUT running
    # validators. The validator callback has to be tested independently.
    judged(env,cast,s)
    assert env[2]['validator'] is not None
    assert env[1].get_stage(s)['state']==env[0].PROVISIONAL


@pytest.mark.parametrize('url', [
    'http://raw.githubusercontent.com/owner/repo/'+ 'a'*40+'/README.md',
    'https://evil.example.com/asset',
    'https://raw.githubusercontent.com/owner/repo/main/README.md',
    'https://raw.githubusercontent.com/owner/repo/'+'a'*40+'/../secrets',
    'https://raw.githubusercontent.com/owner/repo/'+'a'*40+'/file?token=secret',
    'https://raw.githubusercontent.com/owner/repo/'+'a'*40+'/x%2f..',
])
def test_ssrf_and_unpinned_sources_rejected(env,cast,url):
    _,s,_=make(env,cast)
    cast(WORKER)
    assert_error('INVALID_PINNED_SOURCE',lambda:env[1].submit(s,EVIDENCE,url,ARTIFACT_SHA))


def test_source_hash_mismatch_is_not_a_pass(env,cast):
    _,s,_=make(env,cast)
    cast(WORKER)
    env[1].submit(s,EVIDENCE,ARTIFACT_URL,'f'*64)
    env[2]['now']+=env[0].REVIEW_SECONDS
    assert env[1].assess(s)==1
    assert env[1].get_decision(1)['provisional']==env[0].UNKNOWN
    assert env[2]['web_calls']==1


def test_valid_source_is_fetched_on_evaluation(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s); judged(env,cast,s)
    assert env[2]['web_calls']==1
    assert env[1].get_decision(1)['artifact_sha256']==ARTIFACT_SHA


def test_validator_refetches_source(env,cast):
    m,c,state,gl=env
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    original=state['web_calls']
    state['script']=[decision(), {'material_gap':False,'contradiction':False,'unverifiable':False}]
    assert state['validator'](gl.vm.Return(decision_as_norm(m))) is True
    assert state['web_calls']==original+1


def test_validator_vetoes_if_artifact_changes(env,cast):
    m,c,state,gl=env
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    state['source_bytes']=b'Maliciously changed artifact'
    assert state['validator'](gl.vm.Return(decision_as_norm(m))) is False


def test_public_audit_payload_preserves_material_evidence(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s)
    cast(REVIEWER); env[1].challenge(s,'There is an unresolved duplicate row')
    audit=env[1].get_case_payload(s)
    assert audit['evidence']==EVIDENCE
    assert audit['objection']=='There is an unresolved duplicate row'
    assert audit['artifact_sha256']==ARTIFACT_SHA


def test_public_audit_payload_missing_stage_rejected(env,cast):
    assert_error('UNKNOWN_STAGE',lambda:env[1].get_case_payload(999999))


def test_history_keeps_full_prior_evidence_after_retry(env,cast):
    _,s,_=make(env,cast)
    submit(env,cast,s)
    cast(REVIEWER); env[1].challenge(s,'Unverified source claims')
    env[2]['script']=[decision('FAIL','MISSING',True,'UNVERIFIED_CLAIMS')]
    env[1].assess(s)
    env[2]['now']+=env[0].APPEAL_SECONDS
    env[1].finalize_unappealed(s)
    cast(WORKER); env[1].retry_failed(s)
    history=env[1].get_decision(1)
    assert history['evidence_text']==EVIDENCE
    assert history['objection_text']=='Unverified source claims'
    assert history['final'] is True
    assert env[1].get_case_payload(s)['evidence']==''


def test_appeal_text_remains_in_final_decision(env,cast):
    _,s,_=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    cast(REVIEWER); env[1].appeal(s,'The checked hash omits an important entry')
    env[2]['script']=[decision('FAIL','CONFLICTING',True,'OMITTED_ITEM')]
    env[1].resolve_appeal(s)
    assert env[1].get_decision(1)['appeal_text']=='The checked hash omits an important entry'
