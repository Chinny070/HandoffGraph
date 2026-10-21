# HandoffGraph security and engineering audit

Scope: `contracts/handoff_graph.py` (core), `contracts/handoff_consumer_example.py`, `contracts/handoff_capability_consumer.py`, as of the commit that contains this file.
Method: manual review of every public method and state transition, real GenVM Direct Mode tests, labelled offline mock tests, and live StudioNet runs. This is a self-review by the implementer. No independent reviewer has scored it, and no scores are claimed.

Evidence tiers used below: **Live** (StudioNet transactions, `LIVE_PROOFS.md`, `proofs/tx_reconciled.tsv`), **Direct** (`direct_tests/`, real GenVM runtime, mocked web/LLM, warped time), **Offline** (`tests/`, mock runtime).

## Findings fixed

| # | Severity | Finding | How found | Fix | Regression test |
|---|---|---|---|---|---|
| F1 | High (availability) | Pinned-source fetch read `response.status_code`; the SDK field is `status`. The bare `except` swallowed the error, so every live source fetch failed closed with `SOURCE_UNAVAILABLE` and no evidence could ever PASS. | Live (first assessment returned UNKNOWN) | Use `response.status`; mock aligned | All Direct Mode assessment tests run through the real SDK shape |
| F2 | High (deployability) | Storage dataclasses were built by calling the constructor with `DynArray` values, which GenVM forbids. Contract could not create a workflow. | Direct Mode (first run) | `get_or_insert_default` + `init_record` | All 93 Direct Mode tests |
| F3 | Medium (liveness) | `Address` arguments arrive as bytes in some runtimes; `add_stage` stored them unconverted. | Direct Mode | Normalize with `Address(...)` | `setup_one` tests |
| F4 | Medium (integrity) | An inconclusive counterexample verdict lifted the quarantine and consumed the stage's single counterexample slot. A transient fetch failure (or a reviewer-supplied bad source) could therefore neutralize valid counterevidence. | Review | Unverifiable source: lift this quarantine but free the slot; substantive UNKNOWN: fail closed (quarantined, stage FAILED, revocation hash) | `test_counter_source_unavailable_frees_slot_*`, `test_counter_substantive_unknown_fails_closed` (Offline + Direct) |
| F5 | Medium (griefing) | F4's freed slot would allow unlimited reopen cycles, each creating a record and a temporary quarantine. | Review of F4 | `MAX_COUNTER_ATTEMPTS = 3` per stage, reset only by a repair | `test_counter_attempts_are_bounded`, `test_counter_attempts_exhausted_real_runtime` |
| F6 | High (finality) | Consumers authorized irreversible actions from accepted-state reads. `StorageType.LATEST_FINAL` cross-contract reads hang on StudioNet (reproduced against a trivial contract), so they could not be used. | Live | Both consumers now require an accepted-state gate AND a finalized-state gate fetched from the RPC by every validator under strict equality; any failure denies | Offline (RPC error, non-200, wrong value, finalized false), Live |
| F7 | Info | Early diagnosis blamed five cross-contract view calls for a 600 s leader timeout. The real cause was the `LATEST_FINAL` hang (F6); call count was never shown to matter. | Live | Kept a single `is_release_bound` core view as a simplification (smaller consumer surface) | `test_is_release_bound_gate` |

## Properties reviewed

- **Access control.** Owner-only: add stage/requirement, set timeout, seal, freeze, thaw. Worker-only: submit, support, retry, repair, counterexample appeal. Reviewer-only: challenge. Reviewer or owner: open counterexample. Worker or reviewer: appeal. Permissionless by design: assess, resolve_*, finalize_unappealed, expire_*, release. Direct tests assert every rejection (`test_unauthorized_actions_rejected`, `test_only_owner_can_freeze_or_thaw`, invalid-appeal tests). Live: outsider appeal, non-owner freeze, non-worker support attach, non-operator consumer calls all rejected.
- **State machine.** READY → REVIEW → (DISPUTED) → PROVISIONAL → (APPEALED) → PASSED/FAILED; counterexample court and repair are separate transitions guarded by state checks. Each expiry boundary is tested at ±1 s in Direct Mode.
- **Replay and stale receipts.** Release requires `expected_receipt == stage.receipt`; a repair issues a new receipt and `is_release_active(old)` is false. Live and Direct.
- **Quarantine invariants.** `_is_quarantined` walks ancestors; a quarantined ancestor makes every descendant non-releasable and not submittable, including already-released ones. Independent branches are unaffected. Live and Direct.
- **Evidence authenticity.** Commit-pinned GitHub raw URL + SHA-256; non-200, hash mismatch, oversize, non-UTF-8 and empty bodies all fail closed. Authorship and truth of content are out of scope.
- **Consensus.** Leader output is re-derived by each validator; PASS also needs a clean falsification audit. Direct Mode replays validators against forged leader outputs. Live: 7+ real MAJORITY_DISAGREE results left state unchanged.
- **Resource bounds.** 16 stages, 3 dependencies, 6 requirements, 3 attempts, 3 counterexample attempts, ≤16 KB per fetched source, ≤3 sources per jury.
- **Storage consistency.** All records are created through `get_or_insert_default`; decisions are never rewritten except the documented finalization fields.

## Residual risks and known limitations

1. **Finality gate trusts the StudioNet RPC.** A lying endpoint can only downgrade the consumer to accepted-state protection (the accepted-state gate is still required); it cannot authorize an action the accepted-state gate denies. It is not a substitute for native `LATEST_FINAL`, which is unusable here.
2. **LLM judgement is probabilistic.** Correlated model errors, prompt-injection resistance and evidence truthfulness cannot be proven. Strict consensus also costs liveness: one live repaired-evidence assessment needed four attempts.
3. **Owner trust.** The owner picks workers and reviewers, can freeze twice, and has counterexample standing. If one party holds all roles the separation collapses, though consensus review still applies.
4. **Counterexample court is bounded, not bonded.** A reviewer can suspend a valid release until someone resolves it; there is no deposit or slashing.
5. **Long windows were not waited out live** except the delivery timeout and capability expiry. Review-window and appeal-window expiry proofs are listed in `LIVE_PROOFS.md` with their exact status; counterexample/assessment/appeal expiries beyond that are Direct-Mode-only (warped time), not live.
6. **Source parity depends on line endings.** Deploying from a Windows working copy uploads CRLF bytes; use `scripts/verify_source_parity.py` which checks LF and CRLF forms.
7. **No fee evidence beyond StudioNet.** Gas price and gas used are 0 here; costs on another network are unmeasured.
8. **Self-review only.** No independent reviewer has examined this code.

## Test evidence

| Tier | Count | Scope |
|---|---|---|
| Offline (mock runtime) | see `BUILD_STATUS.md` | State machine, consumers, adversarial inputs; NOT consensus |
| Direct Mode (real GenVM) | 93 | Lifecycle, freeze, support, counterexample court, expiries, adversarial matrix, validator replay |
| Live StudioNet | see `LIVE_PROOFS.md` | Deployments, lifecycles, consumers, negative paths |
