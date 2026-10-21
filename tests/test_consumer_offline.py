"""Optional consumer tests with an explicit Python double; NOT real GenVM or chain execution."""
import importlib.util
import pathlib
import sys
import types
import pytest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / 'contracts' / 'handoff_consumer_example.py'
ROOT = 'a' * 64
RECEIPT = 'b' * 64
OPERATOR = '0x' + '11' * 20
GRAPH = '0x' + '22' * 20


@pytest.fixture
def consumer_env(monkeypatch):
    state = {'sender': OPERATOR, 'final_reads': [], 'graph': {
        'workflow': {'sealed': True, 'root': ROOT},
        'stage': {'workflow_id': 1, 'state': 6, 'released': True, 'ruling': 1,
                  'receipt': RECEIPT, 'decision_id': 4, 'attempt': 1, 'submission_hash': 'abc', 'quarantined': False},
        'decision': {'final': True, 'receipt': RECEIPT, 'stage_id': 3,
                     'attempt': 1, 'submission_hash': 'abc'},
    }}

    class Proxy:
        def view(self, *, state=None):
            tests['final_reads'].append(state)
            return self
        def get_workflow(self, _id): return tests['graph']['workflow']
        def get_stage(self, _id): return tests['graph']['stage']
        def get_decision(self, _id): return tests['graph']['decision']
        def is_release_active(self, _id, _receipt): return tests['graph'].get('active', True)

        def is_release_bound(self, workflow_id, stage_id, root, receipt):
            g = tests['graph']; w, s, d = g['workflow'], g['stage'], g['decision']
            return bool(w['sealed'] and w['root'] == root and int(s['workflow_id']) == int(workflow_id)
                and int(s['state']) == 6 and s['released'] and not s['quarantined'] and int(s['ruling']) == 1
                and s['receipt'] == receipt and d['final'] and d['receipt'] == receipt
                and int(d['stage_id']) == int(stage_id) and int(d['attempt']) == int(s['attempt'])
                and d['submission_hash'] == s['submission_hash'] and tests.get('active', True))

    tests = state
    genlayer = types.ModuleType('genlayer')
    gl = types.SimpleNamespace(Contract=object, Event=type('Event', (), {'emit':lambda self:None}),
        public=types.SimpleNamespace(write=lambda f:f, view=lambda f:f),
        vm=types.SimpleNamespace(UserError=ValueError),
        contract_interface=lambda _: lambda address: Proxy(),
        message=types.SimpleNamespace(sender_address=OPERATOR))
    genlayer.gl, genlayer.Address, genlayer.u256, genlayer.u32 = gl, str, int, int

    import json as _json
    def _post(url, body=None, headers=None):
        assert url == 'https://studio.genlayer.com/api'
        req = _json.loads(body)['params'][0]
        assert req['status'] == 'finalized'
        if state.get('web_exc'):
            raise RuntimeError('network down')
        if 'rpc_raw' in state:
            return types.SimpleNamespace(status=state.get('web_status', 200), body=state['rpc_raw'])
        payload = _json.dumps(state.get('final_bound', True)).encode().hex()
        return types.SimpleNamespace(status=state.get('web_status', 200),
                                     body=_json.dumps({'jsonrpc': '2.0', 'id': 1, 'result': payload}).encode())
    gl.nondet = types.SimpleNamespace(web=types.SimpleNamespace(post=_post))
    gl.eq_principle = types.SimpleNamespace(strict_eq=lambda fn: fn())
    calldata_mod = types.SimpleNamespace(
        encode=lambda d: _json.dumps(d).encode(), decode=lambda b: _json.loads(b))
    py_mod = types.ModuleType('genlayer.py')
    py_mod.calldata = calldata_mod
    public_abi = types.ModuleType('genlayer.py.public_abi')
    public_abi.StorageType = types.SimpleNamespace(LATEST_FINAL='LATEST_FINAL')
    monkeypatch.setitem(sys.modules, 'genlayer', genlayer)
    monkeypatch.setitem(sys.modules, 'genlayer.py', py_mod)
    monkeypatch.setitem(sys.modules, 'genlayer.py.public_abi', public_abi)
    spec = importlib.util.spec_from_file_location('handoff_consumer_example', SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    obj = module.HandoffConsumerExample(GRAPH, 1, 3, ROOT, OPERATOR)
    return obj, state, gl


def test_success_and_consume_once(consumer_env):
    c, s, gl = consumer_env
    assert c.can_execute(RECEIPT)
    c.execute_once(RECEIPT)
    assert c.get_status()['action_count'] == 1
    assert c.get_status()['receipt'] == RECEIPT
    assert c.can_execute(RECEIPT) is False
    with pytest.raises(ValueError, match='ALREADY_EXECUTED'):
        c.execute_once(RECEIPT)


def test_reads_final_state_only(consumer_env):
    c, s, _ = consumer_env
    assert c.can_execute(RECEIPT)
    assert s['final_reads'] and set(s['final_reads']) == {None}


def test_reject_before_release(consumer_env):
    c, s, _ = consumer_env
    s['graph']['stage']['released'] = False
    assert not c.can_execute(RECEIPT)
    with pytest.raises(ValueError, match='HANDOFF_NOT_RELEASED'):
        c.execute_once(RECEIPT)


def test_reject_failed_verdict(consumer_env):
    c, s, _ = consumer_env
    s['graph']['stage']['state'] = 7
    assert not c.can_execute(RECEIPT)


def test_reject_unfinalized_decision(consumer_env):
    c, s, _ = consumer_env
    s['graph']['decision']['final'] = False
    assert not c.can_execute(RECEIPT)


def test_reject_mismatched_root(consumer_env):
    c, s, _ = consumer_env
    s['graph']['workflow']['root'] = 'c' * 64
    assert not c.can_execute(RECEIPT)


def test_reject_mismatched_stage_identity(consumer_env):
    c, s, _ = consumer_env
    s['graph']['decision']['stage_id'] = 100
    assert not c.can_execute(RECEIPT)


def test_reject_old_submission(consumer_env):
    c, s, _ = consumer_env
    s['graph']['decision']['submission_hash'] = 'previous'
    assert not c.can_execute(RECEIPT)


def test_reject_wrong_receipt(consumer_env):
    c, _, _ = consumer_env
    assert not c.can_execute('d' * 64)


def test_only_operator_can_execute(consumer_env):
    c, s, gl = consumer_env
    gl.message.sender_address = '0x' + 'ff' * 20
    with pytest.raises(ValueError, match='ONLY_OPERATOR'):
        c.execute_once(RECEIPT)


def test_invalid_constructor_root(consumer_env):
    c, _, _ = consumer_env
    with pytest.raises(ValueError, match='BAD_WORKFLOW_ROOT'):
        type(c)(GRAPH, 1, 3, 'invalid', OPERATOR)


def test_view_returns_false_on_unavailable_source(consumer_env):
    c, s, _ = consumer_env
    del s['graph']['decision']['final']
    assert c.can_execute(RECEIPT) is False


def test_finalized_gate_blocks_even_if_accepted_state_looks_good(consumer_env):
    c, s, _ = consumer_env
    s['final_bound'] = False
    assert c.can_execute(RECEIPT)                      # advisory accepted-state view only
    with pytest.raises(ValueError, match='HANDOFF_NOT_RELEASED'):
        c.execute_once(RECEIPT)
    assert c.get_status()['action_count'] == 0


@pytest.mark.parametrize('field', ['web_exc', 'web_status'])
def test_finalized_gate_fails_closed_on_rpc_errors(consumer_env, field):
    c, s, _ = consumer_env
    s[field] = True if field == 'web_exc' else 503
    with pytest.raises(ValueError, match='HANDOFF_NOT_RELEASED'):
        c.execute_once(RECEIPT)
    s.pop(field)
    c.execute_once(RECEIPT)
    assert c.get_status()['action_count'] == 1


import json as _j


def _hex(value):
    return _j.dumps(value).encode().hex()


def _env(**kw):
    base = {'jsonrpc': '2.0', 'id': 1, 'result': _hex(True)}
    base.update(kw)
    return _j.dumps(base).encode()


DISHONEST = [
    b'not json',
    b'[]',
    _env(error={'code': -1, 'message': 'x'}),
    _env(id=2),
    _env(jsonrpc='1.0'),
    _env(extra='field'),
    _env(result=_hex(1)),
    _env(result=_hex('true')),
    _env(result=_hex(None)),
    _env(result='zz'),
    _env(result=12345),
    _env(result='00' * 40),
    _env(result=_hex(False)),
    b'x' * 5000,
    b'',
]


@pytest.mark.parametrize('raw', DISHONEST)
def test_dishonest_or_malformed_rpc_never_authorizes(consumer_env, raw):
    c, s, _ = consumer_env
    s['rpc_raw'] = raw
    with pytest.raises(ValueError, match='HANDOFF_NOT_RELEASED'):
        c.execute_once(RECEIPT)
    assert c.get_status()['action_count'] == 0


def test_dishonest_yes_cannot_override_accepted_state_denial(consumer_env):
    c, s, _ = consumer_env
    s['graph']['stage']['quarantined'] = True       # accepted state says quarantined
    s['final_bound'] = True                         # lying RPC says finalized and bound
    with pytest.raises(ValueError, match='HANDOFF_NOT_RELEASED'):
        c.execute_once(RECEIPT)
    assert c.get_status()['action_count'] == 0


def test_status_discloses_rpc_trust(consumer_env):
    c, s, _ = consumer_env
    st = c.get_status()
    assert st['trustless_finality'] is False and 'RPC' in st['finality_model']
