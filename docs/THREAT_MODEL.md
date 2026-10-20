# Threat model and residual risk

| Threat | Mitigation | Residual risk |
|---|---|---|
| Worker invents completion | independent AI evaluation of exact Git-commit-pinned bytes; mandatory check matrix | truthful-looking documents can lie; independent external verification is limited |
| Leader lies PASS | validators fetch independently; compare categorical verdict/coverage/risk; falsification on affirmative PASS | correlated model mistakes, non-determinism and prompting limits |
| Missing mandatory criterion | frozen per-requirement checks and all-PASS gate | badly drafted initial requirements cannot be fixed after seal |
| Counterevidence ignored after release | post-release review suspends effective capability and transitively blocks descendants | already performed offchain actions cannot be undone; seven-day window |
| Frivolous counterexample causes denial of service | standing restricted to owner/reviewer, pinned source, one case per attempt, independent verdict | reviewer/owner can suspend valid workflow pending decision; no bond or slashing |
| Malicious counterexample wrongly sustained | worker can appeal once within 24h, independent re-evaluation | appeal may still err; while pending, capability stays revoked |
| False source provenance | commit-pinned GitHub raw URL with SHA-256 exact bytes and bounded fetches | does not establish author identity, actual tests, factual accuracy, code execution, or authenticity of signatures |
| Forged supplemental evidence | single immutable-commit URL plus SHA-256; review window restarts after attachment | authenticated bytes may still make unsupported assertions |
| Stale accepted receipt | `is_release_active` queries live effective final-stage state, checks dependencies + quarantine + freeze | consumer MUST query latest-final state immediately before use; later revocations cannot undo past actions |
| Client replay of consumer authorization | pinned address + workflow + root + stage + action; nonce map; max uses; expiry and operator | cross-contract final-state implementation not yet tested in GenVM |
| Deadline denial of service | permissionless expiry creates UNKNOWN/FAILED, not automatic success; retries bounded | delayed execution can cause false negatives; transaction timestamps not wall time |
| Storage or cost bombs | 16 stages, 3 dependencies, 6 checks, 3 attempts, one supplemental file, one countercase per attempt, 16KB/fetch | 16-node graph and two consensus boundaries can be costly; GenVM limits must be measured |
| Source instructions prompt-inject validator | delimited untrusted payloads; immutable prompts; categorical parser and independent falsification | LLM defense is probabilistic |
| Governance override/capture | no super-admin, downgrade or arbitrary verdict setter | workflow owner controls configuration and two 24-hour freezes |
| Tests mistaken for production evidence | explicit offline mock labels; Direct Mode + live proof gates | compilation and semantic GenVM compatibility remain unverified |

## Safety and privacy

All onchain data and public GitHub references are public. No private keys, PII, private files or executable secrets. No custody/payment logic. No transfers. Do not claim that a hashed GitHub file is an independently executed test. External services may be unavailable; fail closed. No protocol promise of reversibility for already-executed consumer actions. Contracts may require refactoring if GenVM package size or fee constraints are exceeded: never hide such limits or silently split core into multiple mandatory contracts.
