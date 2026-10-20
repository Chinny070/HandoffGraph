"""Non-circular source SHA manifest: local audit ONLY, NOT onchain code parity."""
from pathlib import Path
import hashlib
import json

root=Path(__file__).resolve().parents[1]
excluded={'SOURCE_SHA256_MANIFEST.json'}
files=[]
for p in root.rglob('*'):
    if not p.is_file() or any(x in ('.pytest_cache','__pycache__','.git','node_modules') for x in p.parts):
        continue
    if p.name in excluded or p.suffix in ('.pyc','.zip'):
        continue
    files.append(p)
files.sort()
manifest={
    'schema_version':'0.3',
    'purpose':'LOCAL source integrity, NOT parity with a deployment',
    'target_network':'StudioNet',
    'target_chain_id':61999,
    'offline_tests_observed':'133 passed (2026-10-20, mock Python; see CI for fresh counts)',
    'direct_mode':'NOT EXECUTED',
    'genvm_semantic_lint':'NOT EXECUTED',
    'studio_network_deployment':'NOT DEPLOYED',
    'files_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
}
(root/'SOURCE_SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n',encoding='utf-8')
print(f'Wrote local source manifest for {len(files)} files (not a StudioNet proof)')
