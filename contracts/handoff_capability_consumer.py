# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Optional bounded action-capability consumer for HandoffGraph v0.3.

Single deployable IC. Never transfers GEN. The immutable workflow root, action
identifier, operator and cap count prevent arbitrary contract-side reuse.
can_consume is an accepted-state advisory view. consume requires BOTH the accepted-state gate
and a FINALIZED-state gate fetched by every validator from the StudioNet RPC (LATEST_FINAL
cross-contract reads hang on StudioNet; see LIVE_PROOFS.md).
"""
from genlayer import *
from genlayer.py import calldata
import json
from datetime import datetime, timezone

STUDIONET_RPC = 'https://studio.genlayer.com/api'


@gl.contract_interface
class IHandoffGraphCapability:
    class View:
        def get_workflow(self, workflow_id: u256) -> dict: ...
        def get_stage(self, stage_id: u256) -> dict: ...
        def get_decision(self, decision_id: u256) -> dict: ...
        def is_release_active(self, stage_id: u256, expected_receipt: str) -> bool: ...
        def is_release_bound(self, workflow_id: u256, stage_id: u256, expected_root: str,
                             expected_receipt: str) -> bool: ...


class CapabilityConsumed(gl.Event):
    def __init__(self, nonce: u256, stage_id: u256, /, **kwargs): ...


class HandoffCapabilityConsumer(gl.Contract):
    graph_address: Address
    workflow_id: u256
    stage_id: u256
    workflow_root: str
    action_hash: str
    operator: Address
    expires_at: u256
    max_uses: u32
    use_count: u32
    used: TreeMap[u256, bool]
    last_receipt: str

    def __init__(self, graph_address: Address, workflow_id: u256, stage_id: u256,
                 workflow_root: str, action_hash: str, operator: Address,
                 expires_at: u256, max_uses: u32):
        if int(workflow_id) <= 0 or int(stage_id) <= 0:
            raise gl.vm.UserError('BAD_IDS')
        for value in (workflow_root, action_hash):
            if len(value) != 64 or any(ch not in '0123456789abcdef' for ch in value):
                raise gl.vm.UserError('BAD_COMMITMENT')
        zero = str(Address('0x' + '00' * 20))
        if str(graph_address) == zero or str(operator) == zero:
            raise gl.vm.UserError('BAD_ADDRESS')
        if not (1 <= int(max_uses) <= 32):
            raise gl.vm.UserError('BAD_USAGE_BOUND')
        if int(expires_at) <= int(datetime.now(timezone.utc).timestamp()):
            raise gl.vm.UserError('BAD_EXPIRY')
        self.graph_address, self.workflow_id, self.stage_id = graph_address, workflow_id, stage_id
        self.workflow_root, self.action_hash = workflow_root, action_hash
        self.operator, self.expires_at = operator, expires_at
        self.max_uses, self.use_count = max_uses, u32(0)
        self.last_receipt = ''

    def _eligible(self, nonce: u256, requested_action: str, receipt: str) -> bool:
        if (int(nonce) <= 0 or int(nonce) > 32 or self.used.get(nonce, False) or
            int(self.use_count) >= int(self.max_uses) or
            int(datetime.now(timezone.utc).timestamp()) >= int(self.expires_at) or
            requested_action != self.action_hash or len(receipt) != 64):
            return False
        latest_final = IHandoffGraphCapability(self.graph_address).view()
        return bool(latest_final.is_release_bound(self.workflow_id, self.stage_id,
                                                  self.workflow_root, receipt))


    def _finalized_bound(self, receipt: str) -> bool:
        """True only if the StudioNet RPC reports the release as bound in FINALIZED state.

        gl LATEST_FINAL cross-contract reads hang on StudioNet, so each validator instead
        fetches a finalized gen_call from the RPC; strict equality means every validator
        must observe the identical boolean. Any error or mismatch fails closed.
        """
        graph = str(self.graph_address)
        payload = calldata.encode({'method': 'is_release_bound',
                                   'args': [int(self.workflow_id), int(self.stage_id), self.workflow_root, receipt]})
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
    def can_consume(self, nonce: u256, requested_action: str, receipt: str) -> bool:
        try:
            return self._eligible(nonce, requested_action, receipt)
        except Exception:
            return False

    @gl.public.write
    def consume(self, nonce: u256, requested_action: str, receipt: str):
        if gl.message.sender_address != self.operator:
            raise gl.vm.UserError('ONLY_OPERATOR')
        if not self._eligible(nonce, requested_action, receipt) or not self._finalized_bound(receipt):
            raise gl.vm.UserError('CAPABILITY_INVALID')
        self.used[nonce] = True
        self.use_count = u32(int(self.use_count) + 1)
        self.last_receipt = receipt
        CapabilityConsumed(nonce, self.stage_id).emit()

    @gl.public.view
    def get_status(self) -> dict:
        return {'graph_address': str(self.graph_address), 'workflow_id': int(self.workflow_id),
            'stage_id': int(self.stage_id), 'workflow_root': self.workflow_root,
            'action_hash': self.action_hash, 'operator': str(self.operator),
            'expires_at': int(self.expires_at), 'max_uses': int(self.max_uses),
            'use_count': int(self.use_count), 'last_receipt': str(self.last_receipt)}
