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

    tests = state
    genlayer = types.ModuleType('genlayer')
    gl = types.SimpleNamespace(Contract=object, Event=type('Event', (), {'emit':lambda self:None}),
        public=types.SimpleNamespace(write=lambda f:f, view=lambda f:f),
        vm=types.SimpleNamespace(UserError=ValueError),
        contract_interface=lambda _: lambda address: Proxy(),
        message=types.SimpleNamespace(sender_address=OPERATOR))
    genlayer.gl, genlayer.Address, genlayer.u256, genlayer.u32 = gl, str, int, int
    public_abi = types.ModuleType('genlayer.py.public_abi')
    public_abi.StorageType = types.SimpleNamespace(LATEST_FINAL='LATEST_FINAL')
    monkeypatch.setitem(sys.modules, 'genlayer', genlayer)
    monkeypatch.setitem(sys.modules, 'genlayer.py', types.ModuleType('genlayer.py'))
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
    assert s['final_reads'] and set(s['final_reads']) == {'LATEST_FINAL'}


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
