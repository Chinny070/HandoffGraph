# Threat model and residual risk

Status legend: **Live** = observed on StudioNet (see `LIVE_PROOFS.md`); **Direct** = real GenVM Direct Mode with mocked web/LLM and warped time (`direct_tests/`); **Offline** = labelled mock runtime only; **Design** = argued, not exercised.

| Threat | Mitigation | Evidence | Residual risk |
|---|---|---|---|
| Worker invents completion | Independent AI evaluation of exact commit-pinned bytes; mandatory requirement matrix | Live (PASS and FAIL on real evidence), Direct | A truthful-looking document can lie; hashing authenticates bytes, not claims |
| Leader reports false PASS | Validators re-fetch, re-derive verdict/coverage/risk, and run a falsification audit on any PASS | Direct (`run_validator` with forged leader output, forged matrix, audit gaps); Live (7 real MAJORITY_DISAGREE results left state unchanged) | Correlated model error; LLM non-determinism |
| Liveness loss from strict consensus | Every nondeterministic call fails closed and can be retried by anyone; expiry paths end stalled states as UNKNOWN/FAILED, never PASS | Live: stage 3 repaired-evidence assessment needed 4 attempts (3 MAJORITY_DISAGREE) before one applied | Borderline evidence can take several retries; each retry costs a consensus round |
| Missing mandatory criterion | Frozen per-requirement checks, all-PASS gate | Direct, Offline | Badly drafted requirements cannot be fixed after seal |
| Counterevidence ignored after release | Counterexample immediately quarantines the stage and every descendant; independent verdict follows | Live (sustained, quarantine, downstream and capability denied) | Already-executed off-chain actions cannot be undone; 7-day window |
| Malicious leader mislabels a result as "source unavailable" | `source_ok` is recomputed by every validator from its own fetch and must match; state transitions never read the leader's free-text `gap` | Direct (4 forged-claim tests, reserved-gap test) | Honest fetch failures on some validators cause a disagreement and a retry, not a state change |
| Descendant stays active after its prerequisite is repaired | Submission commits to prerequisite receipts; stale descendants are inactive and permissionlessly invalidated | Live (v5), Direct | A descendant must be re-evaluated, costing consensus rounds |
| Frivolous counterexample (griefing) | Standing limited to reviewer/owner; commit-pinned source; independent verdict; at most 3 attempts per stage; an unverifiable source frees the slot, a substantive UNKNOWN fails closed | Direct, Offline | Reviewer/owner can suspend a valid release until someone calls the permissionless resolve; no bond |
| Wrongly sustained counterexample | One worker appeal within 24 h, then independent re-evaluation | Live (appeal resolved UPHELD), Direct (OVERTURNED restores the original receipt) | Appeal can also err; capability stays revoked while pending |
| False source provenance | GitHub raw URL pinned to a 40-hex commit, exact SHA-256, size and UTF-8 bounds, fail closed on any fetch problem | Direct (status 404/500/empty, wrong SHA, oversize, non-UTF-8, 10 URL shapes, 5 SHA shapes), Live | Does not prove authorship, execution, or factual truth |
| Prompt injection via evidence, objection or appeal | All untrusted text is embedded as JSON strings in delimited tags; strict categorical parser; extra model keys ignored | Direct (quoted-data assertions), Offline | Probabilistic defence |
| Malformed model output | Strict shape check; `PASS` requires COMPLETE coverage, no risk, gap NONE | Direct (10 malformed verdicts, 6 malformed matrices) | None known |
| Stale or replayed release receipt | `release` and consumers require the exact current receipt; repair issues a new receipt and the old one is inactive | Live (replay and stale receipt rejected; old receipt inactive after repair), Direct | None known |
| Consumer acts on non-final state | `execute_once` and `consume` require BOTH an accepted-state gate and a FINALIZED-state gate fetched by every validator from the StudioNet RPC | Live (probe and consumers); Offline (RPC failure, wrong value, non-200) | Trusts the RPC endpoint to report finality; a lying endpoint can only downgrade to accepted-state protection because the accepted-state gate is still required. `LATEST_FINAL` cross-contract reads hang on StudioNet, so they are not used |
| Consumer replay / unauthorized caller | Operator check, one-shot flag, nonce map, usage cap, expiry, action hash | Live | None known |
| Capability expiry and revocation | Expiry compared at execution time; revocation is the core's quarantine/failed-state, checked on every use | Live (expired capability refused while the stage release stayed active; capability refused after sustained counterexample) | No operator-initiated revoke call; revocation only follows core state |
| Deadline denial of service | Permissionless expiry produces UNKNOWN/FAILED, never success; retries bounded to 3 attempts | Live (delivery expiry), Direct (every boundary: ±1 s) | Delayed execution can cause false negatives |
| Storage / cost bombs | 16 stages, 3 deps, 6 requirements, 3 attempts, 3 counter attempts, 16 KB per fetch | Direct (limits asserted) | A 16-stage graph with several consensus rounds can be costly; fees are zero on StudioNet only |
| Governance override | No admin verdict setter; owner controls only configuration and two 24 h freezes | Direct (freeze/thaw/limit, non-owner rejected), Live | Owner can freeze twice and holds counterexample standing; if owner = worker = reviewer the role separation collapses (consensus review still applies) |
| Tests mistaken for production evidence | Evidence labelled by tier; reconciled transaction table | `proofs/tx_reconciled.tsv` | — |

## Finality design (consumers)

1. The core only reports a stage PASSED after protocol-level finalization (appeal resolution or an unchallenged window).
2. A StudioNet transaction can still be appealed at consensus level until it is FINALIZED. Measured lag from ACCEPTED to FINALIZED was roughly 30 s on this network.
3. A consumer therefore refuses to act unless the finalized-state RPC read also reports the release as bound. If either gate fails, nothing executes.

## Safety and privacy

All on-chain data and public GitHub references are public. No private keys, PII or secrets belong in evidence. No custody or payment logic and no GEN transfers. External services may be unavailable; every path fails closed. Already-executed consumer actions are never reversed.
