# Comparison with Ratchet

This compares two different GenLayer contracts on facts that can be checked. It does not contain reviewer scores and does not claim HandoffGraph "beats" Ratchet. Ratchet facts below are what its public repository page states (<https://github.com/ometere123/ratchet>); I did not independently run its tests, re-read its contract source for this pass, or verify its transactions.

## What each contract decides

| | Ratchet (as described by its repository) | HandoffGraph |
|---|---|---|
| Question adjudicated | Is a proposed policy revision strictly stronger than the current head and the genesis rule? | Does commit-pinned agent work satisfy frozen acceptance requirements, and is its downstream release still valid? |
| On-chain effect | Admit or log-reject a stronger revision; tighten-only history | Permit or block future dependent actions; release capability that can later be revoked |
| Core state machine | Up to 8 tracks, sealed genesis, monotonic versions | DAG of up to 16 stages, sealed root, review/dispute/appeal/final/release, counterexample court, repair |
| Evidence handling | Policy text | Commit-pinned GitHub bytes with SHA-256, optional support artifact |
| Consumers | One example consumer | One-shot consumer and an action-scoped capability consumer |
| Source size | not stated on its page | ~56 KB core |

## Evidence that exists today

| | Ratchet (self-reported, unverified by me) | HandoffGraph (verified in this repository) |
|---|---|---|
| Offline mock tests | 14 | 141 |
| Real GenVM Direct Mode tests | 24 (author's workstation) | 93 (run here, `direct_tests/`) |
| GenVM lint | not stated | pass on all 3 contracts |
| Live StudioNet deployment | contract and consumer addresses and source hashes listed; consumer deny-then-allow reported | core v4 + 4 consumers deployed; 325 transactions reconciled FINALIZED; source parity verified |
| Live negative paths | not stated on its page | rejections recorded with decoded reasons (`proofs/tx_reconciled.tsv`) |
| Live validator disagreement observed | not stated | 10 transactions ended MAJORITY_DISAGREE with no state change |
| Documented limitations | semantic guardrail, not a formal proof; LLM errors possible | see `SECURITY_AUDIT.md`: probabilistic judgement, finality gate trusts the RPC, long-window expiries not all live-proven, self-review only |

## Honest reading

- The two contracts solve different problems, so counts of tests or features do not rank them. A larger state machine also means a larger attack surface; HandoffGraph's live testing found and fixed several real-runtime defects (see `SECURITY_AUDIT.md`), which is evidence the extra surface needed that testing, not evidence of superiority.
- HandoffGraph has more verified test volume and a wider range of live negative-path evidence. Ratchet is a smaller, simpler primitive and, by its own description, has no escrow, upgrade key or admin bypass, as is true here too.
- Gaps that remain on the HandoffGraph side: several expiry paths are Direct-Mode-only, consumers depend on the StudioNet RPC for the finality gate, and no independent reviewer has assessed it. Any reviewer scoring would have to come from reviewers; none is invented here.
