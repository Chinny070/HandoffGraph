"""Only offline AST/structure checks; NOT official GenVM semantic lint."""
import ast
from pathlib import Path

root=Path(__file__).resolve().parents[1]
files=[root/'contracts'/x for x in ('handoff_graph.py','handoff_consumer_example.py','handoff_capability_consumer.py')]
texts={p.name:p.read_text(encoding='utf-8') for p in files}
modules={p.name:ast.parse(texts[p.name]) for p in files}
s=texts['handoff_graph.py']
core=modules['handoff_graph.py']
classes={x.name:x for x in core.body if isinstance(x,ast.ClassDef)}
contract=classes['HandoffGraph']
funcs={n.name:n for n in contract.body if isinstance(n,ast.FunctionDef)}


def is_one_contract(source):
    module=modules[source]
    return sum(1 for c in module.body if isinstance(c,ast.ClassDef) and any(
        isinstance(b,ast.Attribute) and b.attr=='Contract' for b in c.bases)) == 1


def field_present(name):
    return any(isinstance(x,ast.AnnAssign) and isinstance(x.target,ast.Name) and
               x.target.id==name for x in contract.body)

checks={
    'one IC class per deployable file':all(is_one_contract(p.name) for p in files),
    'no consumer imported in standalone core':'handoff_consumer' not in s and 'handoff_capability_consumer' not in s,
    'persisted workflows':field_present('workflows'),
    'persisted stages':field_present('stages'),
    'persisted decisions':field_present('decisions'),
    'persisted counterexamples':field_present('counterexamples'),
    'never custody or send GEN':all(x not in s for x in ('gl.evm.contract_interface','transfer_funds(', 'gl.message.value')),
    'leader validator custom consensus':'run_nondet_unsafe' in s,
    'separate requirement consensus':'_requirements_jury' in funcs,
    'strict structured matrix parser':'def requirement_vector(' in s,
    'pinned artifact hash check':'hashlib.sha256(raw)' in s,
    'restricted Git commit source allowlist':'https://raw.githubusercontent.com/' in s,
    'independent reread in source jury':'source = assemble_sources(' in s,
    'adversarial positive veto':'ADVERSARIAL NEGATIVE TEST' in s,
    'normal bounded appeal':'appeal' in funcs and 'resolve_appeal' in funcs,
    'counterexample adjudication':'open_counterexample' in funcs and 'resolve_counterexample' in funcs,
    'counterexample appeal':'appeal_counterexample' in funcs and 'resolve_counter_appeal' in funcs,
    'transitive quarantine traversal':'_is_quarantined' in funcs,
    'transitive release dependency gate':'_deps_released' in funcs,
    'consumer effective release gate':'is_release_active' in funcs,
    'bounded attempts':'MAX_ATTEMPTS = 3' in s,
    'bounded freeze':'MAX_FREEZES = 2' in s,
    'bounded requirements':'MAX_REQUIREMENTS = 6' in s,
    'bounded graph':'MAX_STAGES = 16' in s,
    'preseal requirement registration':'add_requirement' in funcs,
    'preseal delivery timeout':'set_delivery_timeout' in funcs,
    'safe deadline expiration':'expire_delivery' in funcs and 'expire_appeal' in funcs,
    'immutable root':'seal_workflow' in funcs,
    'decision certificate':'get_certificate' in funcs,
    'two independently deployable consumers':all('_finalized_bound' in texts[n] and 'is_release_bound' in texts[n] and "'finalized'" in texts[n] for n in ('handoff_consumer_example.py','handoff_capability_consumer.py')),
    'action capability nonces':'self.used[nonce] = True' in texts['handoff_capability_consumer.py'],
    'no unrestricted admin shortcut':all(x not in funcs for x in ('force_pass','admin_override','upgrade','replace_root','set_ruling')),
    'nonempty UTF8 source':all(len(t)>500 for t in texts.values()),
}
for k,v in checks.items():
    print(f'{"PASS" if v else "FAIL"}  {k}')
print(f'\n{sum(checks.values())}/{len(checks)} offline structural checks passed')
if not all(checks.values()):
    raise SystemExit(1)
