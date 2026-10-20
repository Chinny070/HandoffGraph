"""Adversarial v0.3 tests using the explicit *offline* GenLayer double."""
import json
import pytest
from test_offline import (OWNER, WORKER, WORKER2, REVIEWER, OTHER, REVIEWER2,
    CRITERION, EVIDENCE, ARTIFACT_URL, ARTIFACT_SHA, decision, make,
    submit, judged, finalize, complete, assert_error)


def configured(env, cast, requirements=('Manifest has exactly three rows',), timeout=0):
    m,c,t,_=env
    cast(OWNER)
    wid=c.create_workflow('Assured','Verifiable scoped handoffs')
    a=c.add_stage(wid,'Deliver',WORKER,REVIEWER,CRITERION,0,0,0)
    b=c.add_stage(wid,'Consume',WORKER2,REVIEWER2,CRITERION,a,0,0)
    for r in requirements: c.add_requirement(a,r)
    if timeout: c.set_delivery_timeout(a,timeout)
    c.seal_workflow(wid)
    return wid,a,b


def matrix(*statuses):
    return {'checks':[{'id':i,'status':status,'reason':'Verified in public artifact'} for i,status in enumerate(statuses)]}


def assess_with_matrix(env, sid, checks, overall=None):
    m,c,t,_=env
    t['now']+=m.REVIEW_SECONDS
    t['script']=[matrix(*checks), overall or decision()]
    return c.assess(sid)


def release_with_matrix(env, cast, sid, checks=('PASS',)):
    submit(env,cast,sid)
    assess_with_matrix(env,sid,checks)
    receipt=finalize(env,sid)
    cast(OWNER)
    env[1].release(sid,receipt)
    return receipt


def test_matrix_hash_in_sealed_graph(env,cast):
    w,s,d=configured(env,cast,('One','Two'))
    old=env[1].get_workflow(w)['root']
    assert len(old)==64
    assert env[1].get_stage(s)['requirements']==['One','Two']
    assert_error('GRAPH_SEALED', lambda:env[1].add_requirement(s,'Three'))


def test_requirement_matrix_all_pass(env,cast):
    w,s,d=configured(env,cast,('A','B'))
    r=release_with_matrix(env,cast,s,('PASS','PASS'))
    cert=env[1].get_certificate(1)
    assert cert['final'] and cert['currently_active']
    assert len(cert['certificate_hash'])==64
    assert json.loads(cert['matrix'])[1]['status']=='PASS'
    assert env[1].get_stage(d)['state']==env[0].READY


def test_one_requirement_failure_prevents_pass(env,cast):
    w,s,d=configured(env,cast,('A','B'))
    submit(env,cast,s)
    assess_with_matrix(env,s,('PASS','FAIL'))
    assert env[1].get_decision(1)['provisional']==env[0].PARTIAL
    r=finalize(env,s)
    assert env[1].get_stage(s)['state']==env[0].FAILED
    assert not env[1].can_release(s,r)


def test_requirement_unknown_prevents_pass(env,cast):
    w,s,d=configured(env,cast)
    submit(env,cast,s); assess_with_matrix(env,s,('UNKNOWN',))
    assert env[1].get_decision(1)['provisional']!=env[0].PASS


def test_matrix_untrusted_wrong_shape_rejected(env,cast):
    m,c,t,_=env
    assert m.requirement_vector({'checks':[{'id':1,'status':'PASS','reason':'X'}]},1) is None
    assert m.requirement_vector({'checks':[{'id':0,'status':'SURE','reason':'X'}]},1) is None
    assert m.requirement_vector({'checks':[]},1) is None
    assert m.requirement_vector({'checks':[{'id':True,'status':'PASS','reason':'X'}]},1) is None


def test_requirements_independent_validator_rejects_malicious_leader(env,cast):
    m,c,t,gl=env
    configured(env,cast)
    t['script']=[matrix('PASS')]
    c._requirements_jury(['Check'],CRITERION,EVIDENCE,ARTIFACT_URL,ARTIFACT_SHA,'','')
    t['script']=[matrix('FAIL')]
    assert t['validator'](gl.vm.Return(matrix('PASS')['checks'])) is False


def test_requirements_counterexample_vetoes_pass(env,cast):
    m,c,t,gl=env
    t['script']=[matrix('PASS')]
    c._requirements_jury(['Check'],CRITERION,EVIDENCE,ARTIFACT_URL,ARTIFACT_SHA,'','')
    t['script']=[matrix('PASS'),{'material_gap':True,'contradiction':False,'unverifiable':False}]
    assert t['validator'](gl.vm.Return(matrix('PASS')['checks'])) is False


def test_requirement_unauthenticated_caller_rejected(env,cast):
    w,s,d=configured(env,cast)
    cast(OTHER)
    assert_error('ONLY_OWNER',lambda:env[1].add_requirement(s,'Unauthorized'))


def test_duplicate_requirement_rejected(env,cast):
    cast(OWNER); c=env[1]
    w=c.create_workflow('x','y'); s=c.add_stage(w,'X',WORKER,REVIEWER,CRITERION,0,0,0)
    c.add_requirement(s,'A')
    assert_error('DUPLICATE_REQUIREMENT',lambda:c.add_requirement(s,'A'))


def test_requirement_bound(env,cast):
    cast(OWNER); c=env[1]
    w=c.create_workflow('x','y'); s=c.add_stage(w,'X',WORKER,REVIEWER,CRITERION,0,0,0)
    for n in range(env[0].MAX_REQUIREMENTS): c.add_requirement(s,str(n))
    assert_error('REQUIREMENT_LIMIT',lambda:c.add_requirement(s,'overflow'))


def test_support_digest_renews_review_window(env,cast):
    w,s,_=make(env,cast)
    first=submit(env,cast,s)
    t=env[2]
    t['now']+=40
    cast(WORKER)
    env[1].attach_support(s,ARTIFACT_URL,ARTIFACT_SHA,'Additional test transcript')
    stage=env[1].get_stage(s)
    assert first!=stage['submission_hash']
    assert stage['support_sha256']==ARTIFACT_SHA
    assert stage['review_deadline']==t['now']+env[0].REVIEW_SECONDS
    assert_error('SUPPORT_NOT_OPEN',lambda:env[1].attach_support(s,ARTIFACT_URL,ARTIFACT_SHA,'again'))


def test_support_worker_only(env,cast):
    w,s,_=make(env,cast); submit(env,cast,s)
    cast(REVIEWER)
    assert_error('ONLY_WORKER',lambda:env[1].attach_support(s,ARTIFACT_URL,ARTIFACT_SHA,'a'))


def test_support_hash_failure_does_not_pass(env,cast):
    w,s,_=make(env,cast); submit(env,cast,s)
    cast(WORKER)
    env[1].attach_support(s,ARTIFACT_URL,'f'*64,'Provided evidence')
    env[2]['now']+=env[0].REVIEW_SECONDS
    did=env[1].assess(s)
    assert env[1].get_decision(did)['provisional']==env[0].UNKNOWN


def test_counter_open_transitive_quarantine(env,cast):
    w,s,child=make(env,cast)
    r=complete(env,cast,s)
    assert env[1].is_release_active(s,r)
    cast(REVIEWER)
    cid=env[1].open_counterexample(s,'Reproduction reports fail',ARTIFACT_URL,ARTIFACT_SHA)
    assert env[1].get_counterexample(cid)['status']==env[0].COUNTER_PENDING
    assert env[1].get_stage(child)['quarantined']
    assert not env[1].can_submit(child)
    assert not env[1].is_release_active(s,r)
    assert not env[1].get_certificate(1)['currently_active']


def test_counter_ineligible_for_nonparty(env,cast):
    w,s,child=make(env,cast); complete(env,cast,s)
    cast(OTHER)
    assert_error('NO_COUNTER_STANDING',lambda:env[1].open_counterexample(s,'x',ARTIFACT_URL,ARTIFACT_SHA))


def test_counter_duplicate_block(env,cast):
    w,s,child=make(env,cast); complete(env,cast,s)
    cast(REVIEWER); env[1].open_counterexample(s,'fault',ARTIFACT_URL,ARTIFACT_SHA)
    assert_error('COUNTER_ALREADY_USED',lambda:env[1].open_counterexample(s,'fault',ARTIFACT_URL,ARTIFACT_SHA))


def test_counter_late_block(env,cast):
    w,s,_=make(env,cast);complete(env,cast,s)
    env[2]['now']+=env[0].COUNTER_WINDOW_SECONDS
    cast(REVIEWER)
    assert_error('COUNTER_WINDOW_CLOSED',lambda:env[1].open_counterexample(s,'fault',ARTIFACT_URL,ARTIFACT_SHA))


def test_counter_dismiss_unlock(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Concern investigated',ARTIFACT_URL,ARTIFACT_SHA)
    env[2]['script']=[decision()]
    env[1].resolve_counterexample(cid)
    assert env[1].get_counterexample(cid)['status']==env[0].COUNTER_DISMISSED
    assert env[1].can_submit(d) and env[1].is_release_active(s,r)


def test_counter_sustained_revokes_future_execution(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Proven flaw',ARTIFACT_URL,ARTIFACT_SHA)
    env[2]['script']=[decision('FAIL','CONFLICTING',True,'CONFIRMED_DEFECT')]
    env[1].resolve_counterexample(cid)
    assert env[1].get_stage(s)['state']==env[0].FAILED
    assert len(env[1].get_stage(s)['revocation_hash'])==64
    assert not env[1].can_submit(d)
    assert not env[1].is_release_active(s,r)
    assert env[1].get_decision(1)['final'] # historic proof preserved


def test_counter_invalid_source_fails_closed(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Invalid source',ARTIFACT_URL,'e'*64)
    env[1].resolve_counterexample(cid)
    assert env[1].get_counterexample(cid)['status']==env[0].COUNTER_INCONCLUSIVE
    assert env[1].is_release_active(s,r) # bounded independent evidence found no corroborated defect


def test_counter_timeout_never_auto_unlocks(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Unresolved alarm',ARTIFACT_URL,ARTIFACT_SHA)
    assert_error('COUNTER_DEADLINE_OPEN',lambda:env[1].expire_counterexample(cid))
    env[2]['now']+=env[0].COUNTER_RESOLVE_SECONDS
    env[1].expire_counterexample(cid)
    assert not env[1].is_release_active(s,r)
    assert not env[1].can_submit(d)


def test_counter_repair_preserves_original_decision(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Flaw',ARTIFACT_URL,ARTIFACT_SHA)
    env[2]['script']=[decision('FAIL','MISSING',True,'FAILED_SPEC')]
    env[1].resolve_counterexample(cid)
    cast(WORKER)
    env[1].submit_repair(s,'Replaced original artifact and tests')
    assert env[1].get_stage(s)['state']==env[0].READY
    assert env[1].get_decision(1)['receipt']==r
    assert not env[1].is_release_active(s,r)
    new=env[1].submit(s,EVIDENCE,ARTIFACT_URL,ARTIFACT_SHA)
    assert new!=env[1].get_decision(1)['submission_hash']


def test_no_repair_with_success(env,cast):
    w,s,d=make(env,cast);complete(env,cast,s)
    cast(WORKER)
    assert_error('REPAIR_NOT_ALLOWED',lambda:env[1].submit_repair(s,'x'))


def test_expire_delivery(env,cast):
    w,s,d=configured(env,cast,(),timeout=3600)
    assert_error('DELIVERY_DEADLINE_OPEN',lambda:env[1].expire_delivery(s))
    env[2]['now']+=3600
    receipt=env[1].expire_delivery(s)
    assert len(receipt)==64
    assert env[1].get_stage(s)['state']==env[0].FAILED
    assert not env[1].can_submit(s)


def test_deadline_bounds(env,cast):
    cast(OWNER);c=env[1]
    w=c.create_workflow('x','y');s=c.add_stage(w,'x',WORKER,REVIEWER,CRITERION,0,0,0)
    assert_error('INVALID_DEADLINE',lambda:c.set_delivery_timeout(s,1))
    assert_error('INVALID_DEADLINE',lambda:c.set_delivery_timeout(s,999999999))


def test_review_expiry_no_ai_pass(env,cast):
    w,s,d=make(env,cast); submit(env,cast,s)
    env[2]['now']+=env[0].REVIEW_SECONDS+env[0].REVIEW_RESOLVE_SECONDS
    env[1].expire_assessment(s)
    assert env[1].get_stage(s)['state']==env[0].FAILED
    assert env[1].get_stage(s)['ruling']==env[0].UNKNOWN


def test_appeal_expiry_fails_closed(env,cast):
    w,s,d=make(env,cast); submit(env,cast,s); judged(env,cast,s)
    cast(WORKER);env[1].appeal(s,'Missing evidence')
    env[2]['now']+=env[0].APPEAL_SECONDS+env[0].APPEAL_RESOLVE_SECONDS
    env[1].expire_appeal(s)
    assert env[1].get_stage(s)['state']==env[0].FAILED
    assert env[1].get_decision(1)['explanation_provenance']==env[0].TIMEOUT_PROVENANCE


def test_no_premature_appeal_expiry(env,cast):
    w,s,d=make(env,cast);submit(env,cast,s);judged(env,cast,s)
    cast(WORKER);env[1].appeal(s,'x')
    assert_error('APPEAL_RESOLUTION_OPEN',lambda:env[1].expire_appeal(s))


def test_certificate_available_only_after_finalization(env,cast):
    w,s,d=make(env,cast);submit(env,cast,s);judged(env,cast,s)
    assert env[1].get_certificate(1)['certificate_hash']==''
    r=finalize(env,s)
    certificate=env[1].get_certificate(1)
    assert certificate['receipt']==r
    assert len(certificate['certificate_hash'])==64
    assert not certificate['currently_active']


def test_freeze_disables_active_release(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(OWNER);env[1].freeze(w)
    assert not env[1].is_release_active(s,r)
    env[1].thaw(w)
    assert env[1].is_release_active(s,r)


def test_counter_appeal_overturn_reactivates_pinned_receipt(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Defect',ARTIFACT_URL,ARTIFACT_SHA)
    env[2]['script']=[decision('FAIL','CONFLICTING',True,'BUG')]
    env[1].resolve_counterexample(cid)
    cast(WORKER);env[1].appeal_counterexample(cid,'Reproduction demonstrates fix was already included')
    env[2]['script']=[decision()]
    env[1].resolve_counter_appeal(cid)
    assert env[1].get_counterexample(cid)['status']==env[0].COUNTER_OVERTURNED
    assert env[1].get_stage(s)['state']==env[0].PASSED
    assert env[1].is_release_active(s,r)
    assert env[1].get_decision(1)['receipt']==r


def test_counter_appeal_upheld_keeps_quarantine(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Defect',ARTIFACT_URL,ARTIFACT_SHA)
    env[2]['script']=[decision('FAIL','MISSING',True,'BUG')]
    env[1].resolve_counterexample(cid)
    cast(WORKER);env[1].appeal_counterexample(cid,'My defense')
    env[2]['script']=[decision('FAIL','MISSING',True,'BUG')]
    env[1].resolve_counter_appeal(cid)
    assert env[1].get_counterexample(cid)['status']==env[0].COUNTER_UPHELD
    assert not env[1].is_release_active(s,r)


def test_counter_appeal_one_time_and_standing(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Defect',ARTIFACT_URL,ARTIFACT_SHA)
    env[2]['script']=[decision('FAIL','MISSING',True,'BUG')]
    env[1].resolve_counterexample(cid)
    assert_error('ONLY_WORKER',lambda:env[1].appeal_counterexample(cid,'Reviewer cannot self-appeal'))
    cast(WORKER);env[1].appeal_counterexample(cid,'Worker defense')
    assert_error('COUNTER_NOT_APPEALABLE',lambda:env[1].appeal_counterexample(cid,'second'))
    assert_error('COUNTER_APPEAL_PENDING',lambda:env[1].submit_repair(s,'cannot reset while appealing'))


def test_counter_appeal_timeout_safe(env,cast):
    w,s,d=make(env,cast);r=complete(env,cast,s)
    cast(REVIEWER);cid=env[1].open_counterexample(s,'Defect',ARTIFACT_URL,ARTIFACT_SHA)
    env[2]['script']=[decision('FAIL','MISSING',True,'BUG')]
    env[1].resolve_counterexample(cid)
    cast(WORKER);env[1].appeal_counterexample(cid,'My evidence')
    assert_error('COUNTER_APPEAL_STILL_OPEN',lambda:env[1].expire_counter_appeal(cid))
    env[2]['now'] += env[0].COUNTER_APPEAL_SECONDS + env[0].APPEAL_RESOLVE_SECONDS
    env[1].expire_counter_appeal(cid)
    assert not env[1].is_release_active(s,r)


def test_dependent_deadline_begins_after_release(env,cast):
    m,c,t,_=env
    cast(OWNER)
    w=c.create_workflow('Pipeline','long lead task')
    parent=c.add_stage(w,'first',WORKER,REVIEWER,CRITERION,0,0,0)
    child=c.add_stage(w,'second',WORKER2,REVIEWER2,CRITERION,parent,0,0)
    c.set_delivery_timeout(child,3600)
    c.seal_workflow(w)
    t['now'] += 20*24*3600
    assert c.get_stage(child)['delivery_deadline']==0
    r=complete(env,cast,parent)
    assert c.can_submit(child)
    assert c.get_stage(child)['delivery_deadline']==t['now']+3600
    t['now']+=3600
    assert not c.can_submit(child)
    c.expire_delivery(child)
    assert c.get_stage(child)['state']==m.FAILED


def test_delivery_timeout_recovery_for_unsubmitted(env,cast):
    w,s,d=configured(env,cast,(),timeout=3600)
    env[2]['now']+=3600
    env[1].expire_delivery(s)
    cast(WORKER)
    env[1].retry_failed(s)
    assert env[1].can_submit(s)
