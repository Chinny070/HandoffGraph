"""Re-read every transaction in proofs/tx_log.tsv from StudioNet and write proofs/tx_reconciled.tsv.

Columns: label, tx, finalized_status, consensus_result, leader_execution, leader_outcome, gas_used.
leader_outcome is the contract-level result of the leader receipt (return value or UserError text).
Read-only; throttled to stay under the RPC read rate limit.
"""
import base64, csv, json, sys, time, urllib.request

RPC = 'https://studio.genlayer.com/api'


def rpc(method, params):
    req = urllib.request.Request(RPC, data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}).encode(),
                                 headers={'content-type': 'application/json', 'user-agent': 'curl/8.0'})
    for attempt in range(6):
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception:
            time.sleep(5 * (attempt + 1))
    return {}


def outcome(res):
    """Leader result bytes: 0x00=return, 0x01=UserError(message), 0x02=VM error (e.g. timeout)."""
    if isinstance(res, str):
        try:
            raw = base64.b64decode(res)
        except Exception:
            return res[:80]
        kinds = {0: 'return', 1: 'user_error', 2: 'vm_error'}
        if not raw:
            return 'empty'
        text = raw[1:].decode('utf-8', 'replace') if raw[0] in (1, 2) else ('%d bytes' % (len(raw) - 1))
        return '%s:%s' % (kinds.get(raw[0], 'kind%d' % raw[0]), text[:90])
    if isinstance(res, dict):
        return str(res.get('status'))
    return str(res)[:80]


def main(src='proofs/tx_log.tsv', dst='proofs/tx_reconciled.tsv'):
    rows, seen = [], set()
    with open(src, encoding='utf-8') as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            tx = next((p for p in parts if p.startswith('0x') and len(p) == 66), None)
            if tx and tx not in seen:
                seen.add(tx)
                rows.append((parts[0], tx))
    out = []
    for label, tx in rows:
        r = rpc('eth_getTransactionByHash', [tx]).get('result') or {}
        cd = r.get('consensus_data') or {}
        lr = (cd.get('leader_receipt') or [{}])[0]
        out.append([label, tx, r.get('status', 'NOT_FOUND'), r.get('result_name', ''),
                    lr.get('execution_result', ''), outcome(lr.get('result')), lr.get('gas_used', '')])
        time.sleep(0.4)
    with open(dst, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['label', 'tx', 'finalized_status', 'consensus_result', 'leader_execution', 'leader_outcome', 'gas_used'])
        w.writerows(out)
    unfinal = [o for o in out if o[2] != 'FINALIZED']
    print('%d transactions, %d not FINALIZED' % (len(out), len(unfinal)))
    for o in unfinal:
        print('  NOT FINAL:', o[0], o[1], o[2])


if __name__ == '__main__':
    main(*sys.argv[1:])
