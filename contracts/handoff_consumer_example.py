# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Optional HandoffGraph consumer: one protected action after a finalized, released PASS.

Separate deployable IC. It is NOT required by HandoffGraph. No GEN transfers.
Uses GenVM's finalized snapshot for cross-contract state reads; this integration
must be verified with the StudioNet-compatible SDK and real Direct Mode tests.
"""
from genlayer import *
from genlayer.py.public_abi import StorageType


@gl.contract_interface
class IHandoffGraph:
    class View:
        def get_workflow(self, workflow_id: u256) -> dict: ...
        def get_stage(self, stage_id: u256) -> dict: ...
        def get_decision(self, decision_id: u256) -> dict: ...
        def is_release_active(self, stage_id: u256, expected_receipt: str) -> bool: ...
    class Write:
        pass


class ProtectedActionExecuted(gl.Event):
    def __init__(self, stage_id: u256, receipt: str, /, **kwargs): ...


class HandoffConsumerExample(gl.Contract):
    graph_address: Address
    workflow_id: u256
    stage_id: u256
    expected_root: str
    operator: Address
    executed: bool
    accepted_receipt: str
    action_count: u32

    def __init__(self, graph_address: Address, workflow_id: u256,
                 stage_id: u256, expected_root: str, operator: Address):
        if int(workflow_id) <= 0 or int(stage_id) <= 0:
            raise gl.vm.UserError('BAD_BINDING_IDS')
        if len(expected_root) != 64 or any(ch not in '0123456789abcdef' for ch in expected_root):
            raise gl.vm.UserError('BAD_WORKFLOW_ROOT')
        if str(graph_address) == str(Address('0x' + '00' * 20)) or str(operator) == str(Address('0x' + '00' * 20)):
            raise gl.vm.UserError('BAD_BINDING_ADDRESS')
        self.graph_address = graph_address
        self.workflow_id = workflow_id
        self.stage_id = stage_id
        self.expected_root = expected_root
        self.operator = operator
        self.executed = False
        self.accepted_receipt = ''
        self.action_count = u32(0)

    def _eligible(self, receipt: str) -> bool:
        if self.executed or not isinstance(receipt, str) or len(receipt) != 64:
            return False
        # Critical: read ONLY the finalized HandoffGraph state. Nonfinal views
        # may change under protocol appeals and must not authorize work.
        target = IHandoffGraph(self.graph_address)
        view = target.view(state=StorageType.LATEST_FINAL)
        workflow = view.get_workflow(self.workflow_id)
        stage = view.get_stage(self.stage_id)
        if (not workflow['sealed'] or workflow['root'] != self.expected_root or
            int(stage['workflow_id']) != int(self.workflow_id) or
            int(stage['state']) != 6 or not stage['released'] or stage['quarantined'] or
            int(stage['ruling']) != 1 or
            stage['receipt'] != receipt or int(stage['decision_id']) <= 0):
            return False
        decision = view.get_decision(u256(int(stage['decision_id'])))
        return bool(decision['final'] and decision['receipt'] == receipt and
                    int(decision['stage_id']) == int(self.stage_id) and
                    int(decision['attempt']) == int(stage['attempt']) and
                    decision['submission_hash'] == stage['submission_hash'] and
                    view.is_release_active(self.stage_id, receipt))

    @gl.public.view
    def can_execute(self, receipt: str) -> bool:
        try:
            return self._eligible(receipt)
        except Exception:
            return False

    @gl.public.write
    def execute_once(self, receipt: str):
        if gl.message.sender_address != self.operator:
            raise gl.vm.UserError('ONLY_OPERATOR')
        if self.executed:
            raise gl.vm.UserError('ALREADY_EXECUTED')
        if not self._eligible(receipt):
            raise gl.vm.UserError('HANDOFF_NOT_RELEASED')
        self.executed = True
        self.accepted_receipt = receipt
        self.action_count = u32(1)
        ProtectedActionExecuted(self.stage_id, receipt).emit()

    @gl.public.view
    def get_status(self) -> dict:
        return {'graph_address': str(self.graph_address),
                'workflow_id': int(self.workflow_id), 'stage_id': int(self.stage_id),
                'expected_root': self.expected_root,
                'operator': str(self.operator), 'executed': bool(self.executed),
                'receipt': self.accepted_receipt, 'action_count': int(self.action_count)}
