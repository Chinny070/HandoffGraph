# HandoffGraph — evidence-based build status

**Verdict:** DEPLOYED AND VERIFIED ON STUDIONET FOR THE CORE LIFECYCLE AND BOTH CONSUMERS; PARTIAL on long-window expiries (see "Not live-proven").
Evidence tiers are kept separate below. Offline mock results are never counted as consensus verification.

## Test and verification evidence

| Tier | Result | Command / location |
|---|---|---|
| GenVM semantic lint | pass, all 3 contracts | `genvm-lint check contracts/<file>.py` |
| Offline mock suite (labelled mock runtime, not GenVM) | 175 passed | `python -m pytest tests -q` |
| Real GenVM Direct Mode (mocked web/LLM, warped time, validator replay) | 105 passed | `python -m pytest direct_tests -q` |
| One-command portable run of all tiers | pass | `python scripts/verify.py` (CI: `.github/workflows/direct-mode.yml`) |
| Structural preflight | 33/33 | `python scripts/preflight.py` |
| Live StudioNet (chain 61999) | 496 logged transactions, all FINALIZED; current run 99 transactions, all MAJORITY_AGREE | `LIVE_PROOFS.md`, `proofs/tx_reconciled.tsv`, `proofs/V5_RUN.md` |
| Independent RPC-only recheck | 5 contracts bytecode-matched to a commit, 40 transactions re-read | `proofs/RECHECK.md` (`scripts/recheck_deployment.py`) |

Direct Mode and offline tests run on Windows with `PYTHONUTF8=1` and `gltest.config.yaml`.

## Current deployment

Core v5 `0x9629E19c11Ab40d9848575A8E699E1d48DBDA209` plus four consumer instances (addresses in `LIVE_PROOFS.md`). Source parity verified for all five (CRLF working-copy form; use `scripts/verify_source_parity.py`), and independently rechecked over the RPC (`proofs/RECHECK.md`). Earlier deployments are superseded.

## Verified live

On core v5: freeze/thaw, support evidence, requirement-by-requirement evaluation, PASS and FAIL, appeal and adjudication, release and replay rejection, repair and retry, counterexample open/sustain/appeal (upheld), causal quarantine, independent-branch recovery, downstream authorization after recovery, delivery-deadline expiry, one-shot consumer on the finalized-state gate, capability consumption, replay, wrong action, unauthorized caller, expiry, and denial after quarantine, and (new) a released descendant going stale after an upstream repair, being invalidated and re-validated.

## Not live-proven

- `expire_assessment`, `expire_appeal`, `expire_counterexample`, `expire_counter_appeal`, `finalize_unappealed` and review-window expiry need 12 h to 7 days of real time. Two of them (review window, `finalize_unappealed`) were started live on core v5 stages 5 and 6 and are run by `scripts/live/timed_proofs.sh`; check `proofs/timed_proofs_v5.log.txt` for completion (earliest unix times 1792701652 and 1792745043). All of them are covered in Direct Mode with warped time, which is not live evidence.
- Counterexample dismissal (PASS verdict) and counter-appeal OVERTURNED were not produced by the live models; covered in Direct Mode and offline only.
- Malicious-leader and dishonest-RPC behaviour are tested in Direct Mode and offline only, not live.
- Fees beyond StudioNet (gas price and gas used are 0 there).

## Changes in this pass

Fixes F1–F11 in `SECURITY_AUDIT.md`, notably: validated `source_ok` instead of a leader-controlled label in the counterexample court (F8); descendants bound to prerequisite receipts with `invalidate_stale` (F9); consumers' finalized-state gate hardened and its RPC trust disclosed in the contracts (F10); portable verification and live scripts without machine paths.

## Known limitations

LLM judgement is probabilistic and strict consensus can need several retries; the consumer finalized-state gate trusts the StudioNet RPC (it can only deny, never authorize beyond the accepted-state gate), so the examples are not trustless authorizers; owner holds configuration and counterexample standing; no independent reviewer has examined this code and no comparative score is claimed.
