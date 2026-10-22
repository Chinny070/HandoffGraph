"""Source integrity manifest: SHA-256 of every tracked source file, line endings normalized to LF.

This is local integrity only. It is NOT parity with a deployment (use scripts/verify_source_parity.py) and it
makes no claim about tests or deployments: current evidence is in BUILD_STATUS.md, LIVE_PROOFS.md and proofs/.
"""
from pathlib import Path
import hashlib
import json
import subprocess

root = Path(__file__).resolve().parents[1]
excluded = {'SOURCE_SHA256_MANIFEST.json'}
tracked = subprocess.run(['git', 'ls-files'], cwd=root, capture_output=True, text=True, check=True).stdout.split('\n')
files = sorted(p for p in (root / t for t in tracked if t)
               if p.is_file() and p.name not in excluded and p.suffix not in ('.pyc', '.zip'))


def lf_sha256(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
manifest = {
    'schema_version': '0.4',
    'purpose': 'Local source integrity (LF-normalized SHA-256 of tracked files). Not a deployment or test claim.',
    'generated_at_commit': commit,
    'line_endings': 'CRLF and LF checkouts hash identically; a Windows-deployed contract uploads CRLF bytes',
    'evidence_documents': ['BUILD_STATUS.md', 'LIVE_PROOFS.md', 'SECURITY_AUDIT.md', 'proofs/tx_reconciled.tsv'],
    'target_network': 'StudioNet',
    'target_chain_id': 61999,
    'files_sha256': {str(p.relative_to(root)).replace('\\', '/'): lf_sha256(p) for p in files},
}
(root / 'SOURCE_SHA256_MANIFEST.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n',
                                                  encoding='utf-8', newline='\n')
print('Wrote source manifest for %d files at commit %s' % (len(files), commit[:12]))
