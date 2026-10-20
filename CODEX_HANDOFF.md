# CODEX / CLAUDE — HandoffGraph completion prompt (v0.3)

You are the final implementation, audit, integration and deployment engineer for this **existing** source package. Do not rebuild, rename, clone Ratchet or replace this system with a frontend. Repository: `https://github.com/Chinny070/HandoffGraph`. Target **stable GenLayer StudioNet ONLY**: chain `61999`, RPC `https://studio.genlayer.com/api`. Do not use Bradbury or preview networks. Preserve the working protocol and the standalone main IC.

## Current truth

This package contains `contracts/handoff_graph.py` (single independently deployable IC), optional `contracts/handoff_consumer_example.py` and `contracts/handoff_capability_consumer.py`, mock offline tests (133 passed here), Direct Mode draft, deployment network gate, docs and threat model. **No real GenVM lint/Direct Mode/live StudioNet proof has yet passed in this environment**, and the GitHub repository was observed EMPTY at handoff. Do not pretend otherwise. The source manifest is local hash evidence only.

## Mandatory order of work

1. **GitHub:** Confirm the repo is still empty before initializing `main`; if new commits appeared, inspect/diff and do not overwrite. Commit the complete source package without caches or secrets. Push to `Chinny070/HandoffGraph` using the connected account. Prefer feature branch + pull request if main has meaningful work; otherwise initial commit is fine. Provide commit SHA and verify remote file parity.
2. **Safety baseline:** Run `pytest tests/ -q`, `python scripts/preflight.py`, `python -m compileall -q contracts tests scripts`, source SHA manifest. Keep all existing tests passing. No speculative fees or deployment writes during this gate.
3. **GenVM:** Install the actual compatible SDK and semantic linter; run `genvm-lint check` for all three files. Fix GenVM storage API incompatibilities, out-of-bounds loops, nested transaction/time semantics, Runner feature support and source size. The monolithic contract may be too large for hosted execution: measure first, optimize without sacrificing invariants, and document any required scoping. DO NOT convert mock test successes into live claims.
4. **Real Direct Mode:** Execute and extend `direct_tests/test_handoff_direct.py` with exhaustive positive, negative, malformed, leader/validator disagreement, per-requirement independent rederivation, adversarial falsification, source SHA mismatch, appeal, counter appeal, timeout, repair, revocation, transitive quarantine, and frozen graph cases. Use real `direct_vm` fixtures and validators. Test that `storage_type=StorageType.LATEST_FINAL` on cross-contract reads resolves correctly. If an API differs, implement the verified SDK alternative and update tests. Document actual pass/fail counts.
5. **Formalize audit:** Threat-model the exact semantic and state machine, especially `open_counterexample` DoS, `resolve_counterexample` UNKNOWN behavior, restoring receipt after successful counter appeal, proof matrix provenance, downstream delivery activation times, countercase reentry/order, arbitrary action replay, historical evidence immutability, and mocked `hashlib.sha3_256` parity gap. Attack the contract actively. Fix vulnerabilities and rerun ALL tests.
6. **Deployment preflight:** `node scripts/assert_studionet.mjs` MUST confirm chain `61999`. Confirm signer authorization and balance. Track fees in an auditable ledger. Respect hard cumulative spending ceiling **10 GEN**, and first proof <= **0.01 GEN** when technically possible; if correct fee estimation/charge cannot be established, STOP paid writes rather than guess or silently bypass safeguards. No secret/private-key printing.
7. **Live StudioNet proofs:** Deploy core, verify finalized successful receipt and exact `gen_getContractCode` source SHA-256 match. Execute a real frozen graph + requirement-PASS + mandatory-fail + appeal + final release + downstream release flow. Validate independent validator participation, source fetch and SHA. Deploy optional consumers, demonstrate fail-before-final, success-after-release, and deny-after-countercase quarantine. Capture independent finalized readbacks, tx hashes, chain IDs, fees and sources for each. If there is a reproducible SDK/network limitation, report exact blocker instead of inventing proof.
8. **Documentation and submission:** Update README, deployment records, actual counts, onchain addresses, SHA manifest, CI and submission description. Keep explicit distinctions among offline mocks, actual GenVM Direct Mode, and live StudioNet; do not claim greater score than Ratchet absent independent reviewer results.

## Hard security invariants

- One standalone core only; both consumers optional.
- DAG sealed once; requirements bound before seal; no policy-ratchet logic or admin override.
- Release only final PASS, complete mandatory check matrix, no stale receipt, no unreleased prerequisite, no active quarantine, no freeze.
- Counterexample cannot undo completed external actions; it MUST block **future** downstream authorizations and preserve old Decision history.
- `StorageType.LATEST_FINAL` or verified equivalent only; no optimistic/nonfinal state for consumer authorization.
- No unrestricted HTTP URLs, no mutable branch references or hashes accepted as evidence of truth; never embed secrets.
- Malformed source, model disagreement, unknown facts or expired review cannot become a silent PASS.
- No GEN custody/transfer, frontend/backend/DAO, or unrelated features unless explicitly asked.

## Exact deliverables expected from you

A pushed, parity-checked remote commit; actual GenVM and Direct Mode logs; test totals; CI status; independent security review notes; contract addresses/source parity if safely deployable; live FINALIZED tx/readback evidence; GEN spend ledger; updated `/docs/DEPLOYMENT_GATES.md`; and a concise DONE / PARTIAL / BLOCKED verdict. Do not give generic progress only. If StudioNet access or compatible runtime is blocked, finish all local work and document just that blocker.
