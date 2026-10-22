"""Independent recheck of a deployment through the StudioNet RPC only (no CLI, no private state).

usage: python scripts/recheck_deployment.py MANIFEST.json COMMIT [OUT.md]

MANIFEST.json:
  {"contracts": [{"name": "...", "address": "0x...", "file": "contracts/x.py"}],
   "transactions": [{"label": "...", "tx": "0x...", "expect_consensus": "MAJORITY_AGREE",
                     "expect_outcome": "return" | "user_error:CODE" | "vm_error"}]}

For every contract it compares the base64-decoded `gen_getContractCode` bytes with `git show COMMIT:file`
(LF and CRLF forms). For every transaction it re-reads status, consensus result and the decoded leader
outcome and checks them against the expectation. Writes a Markdown report pinned to COMMIT and exits
non-zero if anything differs.
"""
import base64, hashlib, json, subprocess, sys, time, urllib.request

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
    if not isinstance(res, str):
        return 'unknown'
    raw = base64.b64decode(res) if res else b''
    if not raw:
        return 'empty'
    kind = {0: 'return', 1: 'user_error', 2: 'vm_error'}.get(raw[0], 'kind%d' % raw[0])
    return kind if raw[0] == 0 else '%s:%s' % (kind, raw[1:].decode('utf-8', 'replace'))


def blob(commit, path):
    data = subprocess.run(['git', 'show', '%s:%s' % (commit, path)], capture_output=True, check=True).stdout
    lf = data.replace(b'\r\n', b'\n')
    return {'LF': lf, 'CRLF': lf.replace(b'\n', b'\r\n')}


def main(manifest_path, commit, out='proofs/RECHECK.md'):
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    commit = subprocess.run(['git', 'rev-parse', commit], capture_output=True, text=True, check=True).stdout.strip()
    chain = rpc('eth_chainId', []).get('result')
    lines = ['# Independent deployment recheck', '',
             'Pinned to commit `%s`. Chain id (RPC): `%s` (61999 = 0xf22f). Checked %s UTC via %s only.' %
             (commit, chain, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()), RPC), '',
             '## Deployed bytecode', '', '| contract | address | on-chain SHA-256 | matches |', '|---|---|---|---|']
    failures = 0
    for c in manifest['contracts']:
        result = rpc('gen_getContractCode', [c['address']]).get('result')
        deployed = hashlib.sha256(base64.b64decode(result)).hexdigest() if result else 'UNREADABLE'
        hit = [k for k, v in blob(commit, c['file']).items() if hashlib.sha256(v).hexdigest() == deployed]
        if not hit:
            failures += 1
        lines.append('| %s | `%s` | `%s` | %s |' % (c['name'], c['address'], deployed, ('%s of %s' % (hit[0], c['file'])) if hit else '**NO MATCH**'))
    lines += ['', '## Representative transactions', '',
              '| label | tx | status | consensus | outcome | expected | ok |', '|---|---|---|---|---|---|---|']
    for t in manifest['transactions']:
        r = rpc('eth_getTransactionByHash', [t['tx']]).get('result') or {}
        leader = ((r.get('consensus_data') or {}).get('leader_receipt') or [{}])[0]
        got_outcome = outcome(leader.get('result'))
        ok = (r.get('status') == 'FINALIZED' and r.get('result_name') == t['expect_consensus'] and
              got_outcome.startswith(t['expect_outcome']))
        if not ok:
            failures += 1
        lines.append('| %s | `%s` | %s | %s | %s | %s / %s | %s |' % (
            t['label'], t['tx'], r.get('status'), r.get('result_name'), got_outcome,
            t['expect_consensus'], t['expect_outcome'], 'yes' if ok else '**NO**'))
        time.sleep(0.3)
    lines += ['', 'Result: **%s**' % ('ALL CHECKS PASSED' if not failures else '%d CHECK(S) FAILED' % failures), '']
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('\n'.join(lines[-3:]))
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
