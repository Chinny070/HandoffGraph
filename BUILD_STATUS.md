# HandoffGraph — evidence-based build status

**Verdict:** DEPLOYED AND VERIFIED ON STUDIONET FOR THE CORE LIFECYCLE AND BOTH CONSUMERS; PARTIAL on long-window expiries (see "Not live-proven").
Evidence tiers are kept separate below. Offline mock results are never counted as consensus verification.

## Test and verification evidence

| Tier | Result | Command / location |
|---|---|---|
| GenVM semantic lint | pass, all 3 contracts | `genvm-lint check contracts/<file>.py` |
| Offline mock suite (labelled mock runtime, not GenVM) | 141 passed | `python -m pytest tests -q` |
| Real GenVM Direct Mode (mocked web/LLM, warped time, validator replay) | 93 passed | `python -m pytest direct_tests -q` |
| Structural preflight | 33/33 | `python scripts/preflight.py` |
| Live StudioNet (chain 61999) | 325 transactions, all FINALIZED; contracts deployed with source parity | `LIVE_PROOFS.md`, `proofs/tx_reconciled.tsv`, `proofs/V4_RUN.md` |

Direct Mode and offline tests run on Windows with `PYTHONUTF8=1` and `gltest.config.yaml`.

## Current deployment

Core v4 `0x82B4D2f2b2DcD9590CE605095515891BAE2aFB25` plus four consumer instances (addresses in `LIVE_PROOFS.md`). Source parity verified for all five (CRLF working-copy form; use `scripts/verify_source_parity.py`).

## Verified live

Freeze/thaw, support evidence, requirement-by-requirement evaluation, PASS and FAIL, appeal and adjudication, release and replay rejection, repair and retry, counterexample open/sustain/appeal (upheld), causal quarantine, independent-branch recovery, downstream authorization after recovery, delivery-deadline expiry, one-shot consumer on the finalized-state gate, capability consumption, replay, wrong action, unauthorized caller, expiry, and denial after quarantine.

## Not live-proven

- `expire_assessment`, `expire_appeal`, `expire_counterexample`, `expire_counter_appeal`, `finalize_unappealed` and review-window expiry need 12 h to 7 days of real time. Two of them (review window, `finalize_unappealed`) were started live on stages 5 and 6 and are being run by `scripts/run_timed_proofs.sh`; check `proofs/timed_proofs.log` for completion. All of them are covered in Direct Mode with warped time, which is not live evidence.
- Counterexample dismissal (PASS verdict) and counter-appeal OVERTURNED were not produced by the live models; covered in Direct Mode and offline only.
- Fees beyond StudioNet (gas price and gas used are 0 there).

## Changes in this pass

Real-runtime fixes (F1–F7 in `SECURITY_AUDIT.md`): working source fetch (`status` field), GenVM-compatible storage construction, Address normalization, fail-closed counterexample court with bounded attempts, finalized-state gate for consumers (native `LATEST_FINAL` reads hang on StudioNet), single-call `is_release_bound` view.

## Known limitations

LLM judgement is probabilistic and strict consensus can need several retries; the finalized gate trusts the StudioNet RPC (it can only deny, never authorize beyond the accepted-state gate); owner holds configuration and counterexample standing; no independent reviewer has examined this code and no comparative score is claimed.
