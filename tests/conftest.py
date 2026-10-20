"""An OFFLINE compatibility double. It is NOT GenVM, consensus, or Keccak parity."""
import sys
import types
import hashlib
import importlib.util
import pathlib
import pytest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / 'contracts' / 'handoff_graph.py'

class Generic(list):
    @classmethod
    def __class_getitem__(cls, _):
        return cls

class Map(dict):
    factory = None

    @classmethod
    def __class_getitem__(cls, _):
        return cls

    def get_or_insert_default(self, key):
        if key not in self:
            record = self.factory.__new__(self.factory)
            for name, ann in self.factory.__annotations__.items():
                if ann is Generic:
                    setattr(record, name, [])
            self[key] = record
        return self[key]

class Emitter:
    def __init__(self, *args, **kwargs):
        pass
    def emit(self):
        pass

class Return:
    def __init__(self, calldata):
        self.calldata = calldata

class Error(Exception):
    pass

class Contract:
    pass

class Hash:
    def __init__(self, data):
        self._data = data
    def hexdigest(self):
        # SHA3-256 is NOT Ethereum Keccak-256. Mock used only for transition tests.
        return hashlib.sha3_256(self._data).hexdigest()

@pytest.fixture
def env(monkeypatch):
    state = {'now': 1_800_000_000, 'sender': '0x'+'11'*20,
             'script': [], 'validator': None, 'last_prompt': ''}
    def exec_prompt(p, response_format=None):
        state['last_prompt'] = p
        assert response_format == 'json'
        if not state['script']:
            raise RuntimeError('Model response not mocked')
        return state['script'].pop(0)
    def jury(leader, validator):
        state['validator'] = validator
        return leader()
    def get_web(url):
        state['web_calls'] = state.get('web_calls', 0) + 1
        body = state.get('source_bytes', b'Verified public source text for deterministic offline tests.')
        return types.SimpleNamespace(status=state.get('web_status', 200), body=body)
    gl = types.SimpleNamespace(
        Contract=Contract, Event=Emitter,
        public=types.SimpleNamespace(write=lambda fn: fn, view=lambda fn: fn),
        vm=types.SimpleNamespace(UserError=Error, Return=Return, run_nondet_unsafe=jury),
        nondet=types.SimpleNamespace(exec_prompt=exec_prompt, web=types.SimpleNamespace(get=get_web)),
        message=types.SimpleNamespace(sender_address=state['sender']))
    fake = types.ModuleType('genlayer')
    fake.gl = gl
    fake.Address = str
    fake.u8 = int
    fake.u32 = int
    fake.u256 = int
    fake.DynArray = Generic
    fake.TreeMap = Map
    fake.Keccak256 = Hash
    fake.allow_storage = lambda cls: cls
    monkeypatch.setitem(sys.modules, 'genlayer', fake)
    spec = importlib.util.spec_from_file_location('handoff_graph', SOURCE)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, 'handoff_graph', module)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, 'clock', lambda: state['now'])
    obj = module.HandoffGraph()
    def typed(cls):
        m = Map()
        m.factory = cls
        return m
    obj.workflows, obj.stages = typed(module.Workflow), typed(module.Stage)
    obj.decisions, obj.counterexamples = typed(module.Decision), typed(module.Counterexample)
    return module, obj, state, gl

@pytest.fixture
def cast(env):
    m, c, state, gl = env
    def as_user(who):
        state['sender'] = who
        gl.message.sender_address = who
    return as_user
