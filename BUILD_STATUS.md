# HandoffGraph v0.3 — evidence-based build status

**Verdict:** DEPLOYED ON STUDIONET, CORE LIFECYCLE VERIFIED LIVE; PARTIAL (see gaps).

## Verified

- **Real GenVM lint:** `genvm-lint check` passes for all three contracts.
- **Real Direct Mode:** 13 `gltest` Direct Mode tests pass (sealing, access control, graph gates, requirement registration, source pin validation, deadlines).
- **Offline mock suite:** 133 tests pass. These use a labelled mock runtime, not GenVM or consensus.
- **Live StudioNet (chain 61999):** core v3 `0x5E716D24DB36Cb8F2C4E793a9295Ba2F341cd447` plus three consumer deployments; see `LIVE_PROOFS.md` and `proofs/tx_log.tsv` for hashes, results and the exact limits of what was verified.

## Fixed during this pass

- Storage records now built with `get_or_insert_default` (previous direct construction of storage structs failed in GenVM).
- Pinned-source fetch used a non-existent response field; it now uses `status`.
- Linter reachability: source assembly moved to a module-level helper.
- Address arguments normalized in `add_stage`.
- New single-call view `is_release_bound`; consumers use it instead of five cross-contract reads.
- Consumers no longer use `StorageType.LATEST_FINAL` (hangs on StudioNet).

## Not done

- Review/appeal 12 h and 24 h windows, `finalize_unappealed`, freeze/thaw, support attachment, counter-appeal, capability time expiry were not exercised live.
- Direct Mode suite has not been extended with the leader/validator disagreement and adversarial matrix requested; the only live disagreement evidence is one observed MAJORITY_DISAGREE.
- On-chain source parity for the three consumer deployments (core v3 parity is verified).
- No independent security review; no claim is made about relative scoring against Ratchet.

## Commands

`python -m pytest tests direct_tests -q` (needs `gltest.config.yaml`, set `PYTHONUTF8=1` on Windows), `genvm-lint check contracts/<file>.py`, `node scripts/assert_studionet.mjs`.
