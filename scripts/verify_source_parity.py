"""Compare deployed StudioNet contract code with a local file or a git revision.

usage: verify_source_parity.py ADDRESS PATH [GIT_REV]
Reads gen_getContractCode, base64-decodes it, and reports SHA-256 against the file as-is, and
(with GIT_REV) against that revision's blob in LF and CRLF form. Deploying from a Windows
working copy uploads CRLF bytes, so an LF-blob mismatch with a CRLF match is parity.
"""
import base64, hashlib, json, subprocess, sys, urllib.request

RPC = 'https://studio.genlayer.com/api'


def onchain(address):
    req = urllib.request.Request(RPC, data=json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'gen_getContractCode',
                                                       'params': [address]}).encode(),
                                 headers={'content-type': 'application/json', 'user-agent': 'curl/8.0'})
    return base64.b64decode(json.load(urllib.request.urlopen(req, timeout=60))['result'])


def main(address, path, rev=None):
    deployed = hashlib.sha256(onchain(address)).hexdigest()
    print('onchain  ', deployed)
    candidates = {'file-as-is': open(path, 'rb').read()}
    if rev:
        blob = subprocess.run(['git', 'show', '%s:%s' % (rev, path)], capture_output=True, check=True).stdout
        candidates['blob-LF@' + rev] = blob.replace(b'\r\n', b'\n')
        candidates['blob-CRLF@' + rev] = blob.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
    match = None
    for name, data in candidates.items():
        h = hashlib.sha256(data).hexdigest()
        flag = 'MATCH' if h == deployed else '     '
        print('%s %-22s %s' % (flag, name, h))
        if h == deployed:
            match = name
    print('PARITY' if match else 'NO PARITY', match or '')
    return 0 if match else 1


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
