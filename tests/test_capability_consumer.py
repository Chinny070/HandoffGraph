"""Bounded capability consumer. Offline model only: NO cross-contract GenVM proof."""
import importlib.util
import pathlib
import sys
import types
import pytest

SOURCE=pathlib.Path(__file__).resolve().parents[1]/'contracts'/'handoff_capability_consumer.py'
ROOT='a'*64
RECEIPT='b'*64
ACTION='c'*64
USER='0x'+'11'*20
GRAPH='0x'+'22'*20

@pytest.fixture
def cap_env(monkeypatch):
    state={'time':1900000000,'sender':USER,'final_reads':[], 'active':True,
           'graph':{'workflow':{'sealed':True,'root':ROOT},
                    'stage':{'workflow_id':1,'state':6,'ruling':1,'released':True,
                             'quarantined':False,'receipt':RECEIPT,'decision_id':9,
                             'attempt':1,'submission_hash':'proof'},
                    'decision':{'final':True,'receipt':RECEIPT,'stage_id':3,
                                'attempt':1,'submission_hash':'proof'}}}
    class Proxy:
        def view(self, *, state=None):
            data['final_reads'].append(state)
            return self
        def get_workflow(self,_):return data['graph']['workflow']
        def get_stage(self,_):return data['graph']['stage']
        def get_decision(self,_):return data['graph']['decision']
        def is_release_active(self,_,__):return data['active']
    data=state
    class Event:
        def __init__(self,*args,**kwargs):pass
        def emit(self):pass
    fake=types.ModuleType('genlayer')
    gl=types.SimpleNamespace(Contract=object, Event=Event,
        public=types.SimpleNamespace(view=lambda f:f, write=lambda f:f),
        vm=types.SimpleNamespace(UserError=ValueError),
        message=types.SimpleNamespace(sender_address=USER),
        contract_interface=lambda _:lambda address:Proxy())
    fake.gl=gl
    fake.Address=str
    fake.u256=int
    fake.u32=int
    fake.TreeMap=dict
    abi=types.ModuleType('genlayer.py.public_abi')
    abi.StorageType=types.SimpleNamespace(LATEST_FINAL='LATEST_FINAL')
    monkeypatch.setitem(sys.modules,'genlayer',fake)
    monkeypatch.setitem(sys.modules,'genlayer.py',types.ModuleType('genlayer.py'))
    monkeypatch.setitem(sys.modules,'genlayer.py.public_abi',abi)
    spec=importlib.util.spec_from_file_location('handoff_capability_consumer',SOURCE)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    class Clock:
        @classmethod
        def now(cls,tz=None):
            return types.SimpleNamespace(timestamp=lambda:state['time'])
    monkeypatch.setattr(module,'datetime',Clock)
    obj=module.HandoffCapabilityConsumer(GRAPH,1,3,ROOT,ACTION,USER,1900000100,2)
    obj.used={}
    return obj,state,gl,module


def test_accept_valid_and_reject_replay(cap_env):
    c,s,_,_=cap_env
    assert c.can_consume(1,ACTION,RECEIPT)
    c.consume(1,ACTION,RECEIPT)
    assert not c.can_consume(1,ACTION,RECEIPT)
    assert c.get_status()['use_count']==1


def test_two_uses_max(cap_env):
    c,s,_,_=cap_env
    c.consume(1,ACTION,RECEIPT)
    c.consume(2,ACTION,RECEIPT)
    assert not c.can_consume(3,ACTION,RECEIPT)
    with pytest.raises(ValueError,match='CAPABILITY_INVALID'):
        c.consume(3,ACTION,RECEIPT)


def test_wrong_action_rejected(cap_env):
    c,s,_,_=cap_env
    assert not c.can_consume(1,'d'*64,RECEIPT)


def test_bad_nonce_rejected(cap_env):
    c,s,_,_=cap_env
    assert not c.can_consume(0,ACTION,RECEIPT)
    assert not c.can_consume(33,ACTION,RECEIPT)


def test_wrong_operator_rejected(cap_env):
    c,s,gl,_=cap_env
    gl.message.sender_address='0x'+'ff'*20
    with pytest.raises(ValueError,match='ONLY_OPERATOR'):
        c.consume(1,ACTION,RECEIPT)


def test_expired_rejected(cap_env):
    c,s,_,_=cap_env
    s['time']=1900000100
    assert not c.can_consume(1,ACTION,RECEIPT)


def test_upstream_quarantine_rejected(cap_env):
    c,s,_,_=cap_env
    s['graph']['stage']['quarantined']=True
    assert not c.can_consume(1,ACTION,RECEIPT)


def test_revoked_graph_release_rejected(cap_env):
    c,s,_,_=cap_env
    s['active']=False
    assert not c.can_consume(1,ACTION,RECEIPT)


def test_final_snapshot_used(cap_env):
    c,s,_,_=cap_env
    assert c.can_consume(1,ACTION,RECEIPT)
    assert set(s['final_reads'])=={'LATEST_FINAL'}


def test_wrong_root_rejected(cap_env):
    c,s,_,_=cap_env
    s['graph']['workflow']['root']='d'*64
    assert not c.can_consume(1,ACTION,RECEIPT)


def test_unfinalized_rejected(cap_env):
    c,s,_,_=cap_env
    s['graph']['decision']['final']=False
    assert not c.can_consume(1,ACTION,RECEIPT)


def test_bad_commitment_constructor(cap_env):
    c,s,_,module=cap_env
    with pytest.raises(ValueError,match='BAD_COMMITMENT'):
        module.HandoffCapabilityConsumer(GRAPH,1,3,ROOT,'not-hash',USER,1900000100,2)


def test_max_uses_constructor(cap_env):
    c,s,_,module=cap_env
    with pytest.raises(ValueError,match='BAD_USAGE_BOUND'):
        module.HandoffCapabilityConsumer(GRAPH,1,3,ROOT,ACTION,USER,1900000100,33)
