# Architecture, lifecycles, and contract interfaces

## Component boundary

**Core `contracts/handoff_graph.py`**: one independently deployable GenLayer IC, no imports from optional contracts, no payment/tokens. The graph is immutable after sealing. Actor roles: owner configures/short-freezes; worker submits/repairs; reviewer challenges; owner or reviewer can file a bounded post-release counterexample; worker can appeal; every other lifecycle function is permissionless after deterministic eligibility checks. Distinct worker/reviewer address is enforced; owner/reviewer non-collusion is not cryptographically guaranteed.

**Optional `handoff_consumer_example.py`**: a fixed `(graph address, workflow ID, stage ID, workflow root, operator)` one-shot action. Reads the latest-final graph state and calls `is_release_active` to prevent stale receipts after quarantine. **Optional `handoff_capability_consumer.py`**: same binding plus immutable `action_hash`, deadline, max 1–32 uses and nonce replay map. Consumer cannot force the graph to decide PASS; it only reads an existing final, released certificate.

## Trust division

Deterministic: sender attribution, DAG construction, immutable sealing root, requirement bounds, role checks, timestamps from GenVM tx context, SHA-256 matching inside each non-deterministic closure, response-shape parsing, deadline limits, finalization, replay lock, receipt/certificate creation, quarantine traversal and consumer gating.

AI/equivalence: assess whether artifact satisfies natural-language criteria; per-requirement PASS/FAIL/UNKNOWN; adjudicate appeal and contradictory evidence; independently seek counterexamples. A model cannot directly write into graph state. Multiple nondeterministic consensus boundaries may be used in one `assess` when requirement-level checks are configured. SDK/GenVM support and operational cost must be measured in Direct Mode/StudioNet.

## Invariants to verify

1. Every dependency points to a lower-ID stage in the **same** workflow.
2. Sealed root includes stage IDs, roles, criterion hashes, dependency IDs, requirement hashes, delivery timeout, owner and purpose.
3. Only finalized PASS gives release eligibility; the release itself is one-time.
4. Every staged submission is bound to the sealed workflow root, exact artifact digest, attempt and evidence; support attached later creates a new submission commitment and restarts review.
5. Mandatory requirement checks are committed as a matrix; ANY non-PASS prevents effective overall PASS; the appeal rechecks previously non-PASS mandatory requirements.
6. Revoked/quarantined ancestor disables all descendant submissions and release-dependent consumers, even if previously released; existing external actions are irreversible.
7. Historical decisions and proof artifacts are not overwritten by repair attempts.
8. `is_release_active` is false for frozen workflows, quarantine, failed stage, unreleased stage, mismatched receipt, nonfinal decision and unreleased prerequisites.
9. Unknown source or malformed/unavailable model output cannot generate release, but can produce a fail-closed UNKNOWN result.
10. Timeouts do not auto-PASS. External links are limited to commit-addressed raw GitHub artifacts.

## Decision records and witness provenance

`Decision` retains the original frozen criterion hash, submission hash, source URL/SHA, evidence and objection text, appeal fields, bounded leader explanation, requirement matrix and its hash, support SHA, repair hash, final receipt, and deterministic certificate hash. The matrix decisions are consensus-bound categories; explanation strings are leader-reported. The original Decision stays final even if a later countercase revokes the stage's *effective* capability; query `get_stage`, `get_counterexample`, `get_certificate`, or `is_release_active` for latest effective status.

## State machine

`READY(1)` → `REVIEW(2)` → [reviewer objection] `DISPUTED(3)` → `PROVISIONAL(4)` → [appeal] `APPEALED(5)` → `PASSED(6)` / `FAILED(7)`.

- Retry: `FAILED` → `READY` for unused attempts; historical decisions remain.
- Release: `PASSED` → `PASSED + released=true`, once per attempt.
- Counterexample: `PASSED + released` → `quarantined`, independently adjudicated. Dismissal clears quarantine; sustained verdict changes effective state to `FAILED`, retaining original decision/release history. Bounded worker appeal can overturn and reactivate original receipt; otherwise repair starts a new attempt. Timed-out unresolved countercases fail closed and do not restore capability.

See `examples/multi_agent_handoff.md` for a complete illustrative flow. It is a scenario, NOT claimed onchain evidence.
