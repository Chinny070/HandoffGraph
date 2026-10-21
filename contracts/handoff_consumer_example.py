# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Optional HandoffGraph consumer: one protected action after a finalized, released PASS.

Separate deployable IC. It is NOT required by HandoffGraph. No GEN transfers.
can_execute is an accepted-state advisory view. execute_once requires BOTH the accepted-state
gate (catches fresh quarantine) and a FINALIZED-state gate fetched by every validator from the
StudioNet RPC (LATEST_FINAL cross-contract reads hang on StudioNet; see LIVE_PROOFS.md).
"""
from genlayer import *
from genlayer.py import calldata
import json

STUDIONET_RPC = 'https://studio.genlayer.com/api'


@gl.contract_interface
class IHandoffGraph:
    class View:
        def get_workflow(self, workflow_id: u256) -> dict: ...
        def get_stage(self, stage_id: u256) -> dict: ...
        def get_decision(self, decision_id: u256) -> dict: ...
        def is_release_active(self, stage_id: u256, expected_receipt: str) -> bool: ...
        def is_release_bound(self, workflow_id: u256, stage_id: u256, expected_root: str,
                             expected_receipt: str) -> bool: ...
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
        # Reads accepted state; finality is enforced by the core (PASSED only after protocol finalization).
        view = IHandoffGraph(self.graph_address).view()
        return bool(view.is_release_bound(self.workflow_id, self.stage_id,
                                          self.expected_root, receipt))


    def _finalized_bound(self, receipt: str) -> bool:
        """True only if the StudioNet RPC reports the release as bound in FINALIZED state.

        gl LATEST_FINAL cross-contract reads hang on StudioNet, so each validator instead
        fetches a finalized gen_call from the RPC; strict equality means every validator
        must observe the identical boolean. Any error or mismatch fails closed.
        """
        graph = str(self.graph_address)
        payload = calldata.encode({'method': 'is_release_bound',
                                   'args': [int(self.workflow_id), int(self.stage_id), self.expected_root, receipt]})
        body = json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'gen_call', 'params': [{
            'type': 'read', 'to': graph, 'from': '0x' + '00' * 20,
            'data': '0x' + payload.hex(), 'status': 'finalized'}]})

        def fetch() -> bool:
            try:
                r = gl.nondet.web.post(STUDIONET_RPC, body=body,
                                       headers={'content-type': 'application/json', 'user-agent': 'curl/8.0'})
                if r.status != 200 or r.body is None or len(r.body) > 4096:
                    return False
                result = json.loads(r.body.decode('utf-8')).get('result')
                if not isinstance(result, str):
                    return False
                return calldata.decode(bytes.fromhex(result)) is True
            except Exception:
                return False

        return bool(gl.eq_principle.strict_eq(fetch))

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
        if not self._eligible(receipt) or not self._finalized_bound(receipt):
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
