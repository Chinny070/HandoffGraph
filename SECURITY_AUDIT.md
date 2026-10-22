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

## Findings from the second review pass (all fixed, with tests)

| # | Severity | Finding | Fix | Regression tests |
|---|---|---|---|---|
| F8 | High (integrity) | The counterexample court freed the stage's slot and lifted quarantine when the jury result's free-text `gap` equalled `SOURCE_UNAVAILABLE`. Validators did not compare `gap`, so a malicious leader could pair a genuinely undecided model verdict (or a model that wrote that string) with this label and neutralize valid counterevidence. | Source availability is a separate boolean `source_ok` produced by the leader and **recomputed by every validator from its own fetch**; mismatch rejects the result. `SOURCE_UNAVAILABLE` is reserved (a model-written gap with that text is renamed; a validator rejects it when sources verify). State transitions use `source_ok`, never `gap`. | Direct: forged unavailability when sources verify, forged `source_ok` when they do not, legacy result without the field, reserved-gap smuggling, court slot not freed by model-claimed unavailability |
| F9 | High (integrity) | A descendant's PASS and release were checked only against its prerequisites' current state. After an upstream repair and re-release (new receipt), an already-released descendant silently became active again though it was judged against the old output. | Each submission commits to the exact receipts of its prerequisites (`parent_digest`, part of the submission hash and therefore the receipt). `is_release_active`, `is_release_bound` and `release` require the digest to be current (`STALE_PREREQUISITE`); permissionless `invalidate_stale` withdraws stale decisions so the stage is re-evaluated. A dismissed counterexample leaves the parent receipt unchanged, so descendants stay valid. | Direct: released descendant after upstream repair, stale-but-unreleased, mid-review, unchanged parents, dismissed counterexample; **Live: v5 run** |
| F10 | Medium (finality disclosure) | The consumer examples did not state that their finalized-state gate trusts the RPC, and accepted any JSON shape. | Docstrings and `get_status` disclose `trustless_finality: false`; strict JSON-RPC envelope validation (version, id, no error, no extra keys, bounded size, exact `True`). | Offline: 15 dishonest or malformed responses per consumer, a dishonest "yes" cannot override an accepted-state denial |
| F11 | Info (tooling) | The genlayer CLI keeps a single global active account; another process switched it mid-run and corrupted a live run. | Live scripts use a private CLI home, abort on the first submission failure, and the run was repeated on a fresh core. | `scripts/live/lib.sh` |

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
| Offline (mock runtime) | 175 | State machine, consumers, adversarial inputs; NOT consensus |
| Direct Mode (real GenVM) | 105 | Lifecycle, freeze, support, counterexample court, expiries, malicious-leader substitution, descendant binding, validator replay |
| Live StudioNet | 496 reconciled transactions, 99 in the current run | Deployments, lifecycles, consumers, negative paths; independent RPC recheck in `proofs/RECHECK.md` |
