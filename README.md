# HandoffGraph — Proof-Carrying, Quarantine-Aware Agent Handoffs

**Standalone GenLayer Intelligent Contract** with optional integration consumers. Target: **stable StudioNet 61999 only**. No frontend, backend, DAO, GEN escrow, token, oracle operator, or automatic payout.

HandoffGraph links autonomous-agent tasks as an immutable directed acyclic graph, verifies real Git-commit-pinned artifacts against natural-language acceptance requirements with GenLayer's independent validator consensus, and releases the next stage **only after a final PASS**. A substantiated post-release counterexample can **quarantine all dependent work** and revoke future consumer authorization. Successful appeals can restore access, without erasing evidence of past decisions.

## State of proof — 20 October 2026

- Code implemented; **133 passing offline Python mock-runtime tests** across core/consumer/security suites.
- Structural preflight and Python compilation are available; see exact commands below.
- **NOT verified:** GenVM semantic/AST lint through official runtime, GenLayer Direct Mode, StudioNet deployment, live multi-validator equivalence, cross-IC FINALIZED state reads, transaction fees or source parity.
- These are meaningful gaps and MUST be closed before submission. Offline mocks do not prove onchain safety.

## The project in one picture

```text
Owner defines graph + criteria + up to 6 objective checks per stage → seal immutable root
       ↓
Worker supplies Git-commit-pinned source SHA-256, optionally a supplemental proof
       ↓
Review window → independent per-requirement AI consensus + adversarial review
       ↓
Provisional verdict → bounded appeal → final decision certificate
       ↓
Permissionless one-time release → dependent agent may start
       ↓
Reviewer or owner submits pinned counterevidence within seven days
       ↓
Immediately quarantine this stage AND all transitive descendants
       ↓
Independent counterexample verdict → dismiss, sustain or inconclusive
       ↓
If sustained: future consumer actions revoked; worker may appeal or repair
```

**Safety caveat:** No smart contract can undo an external action already executed. Causal quarantine restricts **future** actions by integrating consumers which query the latest-final release state at execution time; consumers do not magically intercept arbitrary external agents.

## Why GenLayer, rather than traditional Solidity?

A deterministic hash authenticates bytes but cannot judge if a document, codebase, research deliverable or policy analysis meets nuanced human-readable acceptance requirements. GenLayer's `gl.vm.run_nondet_unsafe` allows the leader and validators to independently fetch pinned public bytes, evaluate qualitative evidence and dispute facts, compare material categorical results, and independently falsify an affirmative PASS. **Deterministic code** still decides all roles, frozen rules, deadlines, hash commitments, revocations, replay protection, storage limits and transitions. Model prose explanations are leader-reported, not validator-certified text.

## What is included

| Capability | Implementation |
| --- | --- |
| Immutable DAG and acceptance criterion | `create_workflow`, `add_stage`, `seal_workflow` |
| Requirement-by-requirement verification | `add_requirement` (max 6 per stage), independent `_requirements_jury`, strict ALL-PASS gate |
| Pinned proof bundle | `submit`, `attach_support` (primary plus one supplementary immutable-commit artifact) |
| Independent evaluation and challenge | `challenge`, `assess`, `_jury`, adversarial negative test |
| Bounded provisional appeals | `appeal`, `resolve_appeal`, `finalize_unappealed` |
| Release and dependency unlocking | `release`, `can_submit`, `can_release` |
| Causal quarantine after new facts | `open_counterexample`, `resolve_counterexample`, `expire_counterexample` |
| Adversarial counterexample appeal | `appeal_counterexample`, `resolve_counter_appeal`, `expire_counter_appeal` |
| Repair without history erasure | `retry_failed`, `submit_repair`, new attempts with repair-note commitment |
| Bounded expiry and safe recovery | `set_delivery_timeout`, `expire_delivery`, `expire_assessment`, `expire_appeal` |
| Cryptographic decision certificate | `get_certificate`, `get_decision` |
| Consumer release queries | `is_release_active` — honors transitive quarantine and freeze |
| Optional contract #1 | `contracts/handoff_consumer_example.py`: single protected action |
| Optional contract #2 | `contracts/handoff_capability_consumer.py`: scoped action, nonce replay guard, max uses, expiry |

### API and invariants

All requirements, deadlines and DAG dependencies are added **before sealing**; the workflow root commits to their hashes. Dependencies reference earlier stages in the same graph, preventing cycles. Up to **16 stages** per workflow, **3 parents** per stage, **6 mandatory checks**, **3 attempts** per stage, **one supplemental artifact** per attempt and **one post-release counterexample per attempt**. Workers and reviewers cannot be the same address. Rejected or nonfinal evidence never enables release. A post-release counterexample temporarily quarantines affected work immediately and can only permanently revoke effective capabilities upon a non-PASS court decision or conservative timeout. Restoration after an appeal uses the same original receipt; the dispute history remains inspectable.

Submission and challenge text is public onchain. Never put secrets, credentials, private medical information, or confidential company documents in these fields or referenced public artifacts.

### Timeline

- Optional delivery deadline: 1 hour to 30 days, starting at **seal for root stages** or **last dependency release for dependent stages**.
- Review window: 12 hours; challenged cases may be assessed sooner.
- Standard appeal window: 24 hours after the provisional verdict.
- Post-release counterexample window: 7 days (one case per attempt); if unresolved, may be expired after 48 hours and stays quarantined.
- Sustained counterexample may be appealed by the original worker for 24 hours; appealed countercases time out conservatively after an additional 72 hours.
- Global owner freeze: at most two 24-hour freezes; `thaw` ends early.
- Timeouts **never automatically produce a semantic PASS**. Any validated final PASS still requires explicit permissionless `release`.

### Exact source pin

Accepted source address pattern:

`https://raw.githubusercontent.com/<owner>/<repo>/<40-character-lowercase-Git-commit>/<path>`

with separately provided, lowercase 64-digit SHA-256 digest. The source is fetched and hash-checked independently by the leader and validators inside the non-deterministic boundary. No branch names, tracking links, arbitrary domains, or mutable web search results. **A correct SHA authenticates bytes only, not whether their claims are accurate.**

## Verify locally

```bash
python -m pip install 'pytest>=8.2,<9'
python -m pytest tests/ -q
python scripts/preflight.py
python -m compileall -q contracts tests scripts
python scripts/create_source_manifest.py
```

The included `tests/conftest.py` is an **explicit Python double**, not GenVM: it substitutes SHA3-256 for Keccak, mocks consensus, and never makes a network request. Counting these tests as live AI verdicts would be misleading.

GenVM / StudioNet checks required before production:

```bash
python -m pip install -r requirements-dev.txt
genvm-lint check contracts/handoff_graph.py
genvm-lint check contracts/handoff_consumer_example.py
genvm-lint check contracts/handoff_capability_consumer.py
gltest direct_tests/test_handoff_direct.py -v -s
npm install
node scripts/assert_studionet.mjs
```

Do not claim the checks above have passed without actually running them in a compatible environment. No live deployment has been performed here, and no GEN has been spent by this build. Only the main contract is necessary for standalone eligibility.

## Further reading

- [Architecture and API](docs/ARCHITECTURE.md)
- [Consensus and threat model](docs/THREAT_MODEL.md)
- [Consumer integration](docs/CONSUMER_INTEGRATION.md)
- [Deployment and live evidence gates](docs/DEPLOYMENT_GATES.md)
- [Ratchet comparison](docs/RATCHET_COMPARISON.md)
- [Agent implementation handoff](CODEX_HANDOFF.md)
- [Official GenLayer non-determinism reference](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)
- [Official Direct Mode reference](https://docs.genlayer.com/api-references/genlayer-test/direct)
