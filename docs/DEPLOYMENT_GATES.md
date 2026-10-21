# Proof gates and honest deployment protocol

Target only **stable StudioNet (chain 61999)**, RPC `https://studio.genlayer.com/api`. Never use Bradbury, studio-dev, studio-next, or preview chain 61997. Status: the gates below were executed; results are in `BUILD_STATUS.md`, `LIVE_PROOFS.md` and `SECURITY_AUDIT.md`. The spending-ceiling language is historical: StudioNet reported gas price 0 and gas used 0 for all 325 transactions.

## Gate 0 — local determinism / static

- `python -m pytest tests/ -q` must pass all tests (record real total and commit).
- `python scripts/preflight.py` must pass (structural checks only).
- `python -m compileall -q contracts tests scripts` must pass.
- Run actual `genvm-lint check` on all three contracts; inspect SDK/semantic lint, not only AST. Fix genuine errors; record unresolved issues.
- Measure source size and runtime/fee constraints. Core is intentionally a standalone contract; do not alter its semantics just to shave lines.

## Gate 1 — real GenVM Direct Mode

- Install matching SDK/toolchain and run `gltest direct_tests/test_handoff_direct.py -v -s`.
- Expand Direct Mode tests for every v0.3 transition, including leader/validator disagreement, malformed requirement matrix, failed SHA verification, adversarial positive veto, post-release source corroboration, disputed appeal and freeze, transitive quarantine of already-released descendants, timeout, stale consumer receipts, and recovery.
- Run every optional consumer against real cross-contract final-state APIs, not only Python doubles. Direct Mode cannot alone prove actual multi-validator network finality.
- Build fresh fixture-backed public Git commits with matching SHA and separately proven test content. No fake proof labels.

## Gate 2 — budget / network preflight

- `npm install`, `node scripts/assert_studionet.mjs` must confirm RPC chain 61999.
- Confirm wallet signer permissions, balance, expected fee and GenVM cost. NEVER expose keys/seed in logs; no arbitrary fee assumptions.
- **Hard cumulative safety ceiling: 10 GEN** unless user changes it explicitly; first funded demonstration <=0.01 GEN if technically possible. If fees cannot be estimated, pause deployment and report, not guess.
- Contracts are unpaid, do not transfer or custody funds. Record independent fee receipt for writes.

## Gate 3 — live transaction and source parity

- Deploy core and optional consumer(s) on stable StudioNet. Record exact addresses, tx hashes and `FINALIZED` status. Verify `gen_getContractCode` SHA-256 parity against the source commit. Do NOT treat a deployment that finalized with runtime error as deployed successfully.
- Write/read real graph; exercise valid PASS, negative/equivocal FAIL/UNKNOWN, adversarial challenge, appeal, deadline, counterexample, quarantine of descendent, sustained revocation, successful counter appeal, repair and second attempt.
- Prove optional consumer denial before final release, success after release, and **subsequent denial on post-release quarantine**; once-executed events remain historical.
- Record exact transaction hashes, fresh latest-final readbacks and gas/GEN spent. Only then update a live-proof file and submission score claims.

## Gate status (executed)

- Gate 0: lint pass (3/3), 141 offline, 33/33 structural.
- Gate 1: 93 real Direct Mode tests; consumers' cross-contract path verified live, not in Direct Mode.
- Gate 2: StudioNet chain 61999 asserted; fee behavior measured (zero).
- Gate 3: deployments with source parity, live lifecycle, consumer denial/success/quarantine denial recorded. Review/appeal/counter long-window expiries are not all live-proven.

## Known build limitations (historical, resolved or re-scoped)

The notes below were written before any GenVM run. Resolved: storage dataclasses, cross-contract views, nested prompt cost, runner compatibility. Re-scoped: `StorageType.LATEST_FINAL` hangs on StudioNet and is replaced by an RPC-based finalized gate.

The source is not certified deployable because GenVM semantic compilation, Direct Mode and StudioNet are unavailable here. In particular, complex `@allow_storage` dataclasses, storage of requirement vectors and countercases, cross-contract `StorageType.LATEST_FINAL`, callable `is_release_active` views, nested prompt cost, and pinned runner compatibility require real verification. This is **not** a minor checkbox; these are mandatory gates.
