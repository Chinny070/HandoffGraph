# HandoffGraph — Proof-Carrying, Quarantine-Aware Agent Handoffs

**Standalone GenLayer Intelligent Contract** with optional integration consumers. Target: **stable StudioNet 61999 only**. No frontend, backend, DAO, GEN escrow, token, oracle operator, or automatic payout.

HandoffGraph links autonomous-agent tasks as an immutable directed acyclic graph, verifies real Git-commit-pinned artifacts against natural-language acceptance requirements with GenLayer's independent validator consensus, and releases the next stage **only after a final PASS**. A substantiated post-release counterexample can **quarantine all dependent work** and revoke future consumer authorization. Successful appeals can restore access, without erasing evidence of past decisions.

## State of proof

The authoritative, under-review state of this project is the **`dev/live-verification`** branch. `main` holds an older v0.3 baseline and has not been updated pending review. Evidence is kept in separate tiers and never mixed:

- **GenVM lint:** passes for all three contracts (`genvm-lint`).
- **Offline mock tests** (`tests/`): a labelled Python double, not GenVM and not consensus.
- **Real GenVM Direct Mode** (`direct_tests/`): real runtime with mocked web/LLM and warped time.
- **Live StudioNet (chain 61999):** deployments, lifecycles and rejections, reconciled from the chain.

Current numbers and addresses: [BUILD_STATUS.md](BUILD_STATUS.md), [LIVE_PROOFS.md](LIVE_PROOFS.md), [SECURITY_AUDIT.md](SECURITY_AUDIT.md). Known limits: consumer finality trusts the StudioNet RPC (native `LATEST_FINAL` reads hang on StudioNet), several long-window expiries are Direct-Mode-only, and no independent reviewer has examined the code.

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

**Safety caveat:** No smart contract can undo an external action already executed. Causal quarantine restricts **future** actions by integrating consumers which re-check the release at execution time (accepted state plus a StudioNet-RPC finalized-state gate); consumers do not magically intercept arbitrary external agents.

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
| Consumer release queries | `is_release_active`, `is_release_bound` — honor transitive quarantine, freeze and prerequisite receipts |
| Stale descendants after upstream repair | `invalidate_stale` (permissionless), `parent_digest` commitment |
| Optional contract #1 | `contracts/handoff_consumer_example.py`: single protected action |
| Optional contract #2 | `contracts/handoff_capability_consumer.py`: scoped action, nonce replay guard, max uses, expiry |

### API and invariants

All requirements, deadlines and DAG dependencies are added **before sealing**; the workflow root commits to their hashes. Dependencies reference earlier stages in the same graph, preventing cycles. Up to **16 stages** per workflow, **3 parents** per stage, **6 mandatory checks**, **3 attempts** per stage, **one supplemental artifact** per attempt and **up to 3 counterexample attempts per stage** (an unverifiable counter-source frees the slot; a substantive UNKNOWN fails closed). Workers and reviewers cannot be the same address. Rejected or nonfinal evidence never enables release. A post-release counterexample temporarily quarantines affected work immediately and can only permanently revoke effective capabilities upon a non-PASS court decision or conservative timeout. Restoration after an appeal uses the same original receipt; the dispute history remains inspectable.

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

One portable command runs every tier and reports them separately (Python 3.12):

```bash
python -m pip install --pre -r requirements-dev.txt
python scripts/verify.py
```

Direct Mode pins GenVM `v0.2.16` (override with `HANDOFF_GENVM_VERSION`) because it would otherwise resolve the newest release, which may lack the needed asset. It runs compile checks, the structural preflight, `genvm-lint` on all three contracts, the offline mock tests and the real Direct Mode tests. CI runs the same script (`.github/workflows/direct-mode.yml`). Individual steps:

```bash
python scripts/preflight.py
python -m pytest tests -q
python -m pytest direct_tests -q
python scripts/create_source_manifest.py
```

The included `tests/conftest.py` is an **explicit Python double**, not GenVM: it substitutes SHA3-256 for Keccak, mocks consensus, and never makes a network request. Counting these tests as live AI verdicts would be misleading.

Live verification (needs the `genlayer` CLI, funded keystores and a pushed evidence commit; the header of each script lists the environment variables):

```bash
node scripts/assert_studionet.mjs          # confirms chain 61999
bash scripts/live/lifecycle.sh             # deploys a fresh core and runs the full lifecycle
bash scripts/live/timed_proofs.sh          # real 12 h / 24 h deadline proofs
python scripts/reconcile_tx_log.py         # re-reads every logged tx from the chain
python scripts/verify_source_parity.py <address> contracts/<file>.py HEAD
```

Only the main contract is necessary for standalone eligibility. The consumers are optional demonstrations and are **not** trustless authorizers on StudioNet: their finalized-state gate trusts the StudioNet RPC endpoint.

## Further reading

- [Architecture and API](docs/ARCHITECTURE.md)
- [Consensus and threat model](docs/THREAT_MODEL.md)
- [Security audit](SECURITY_AUDIT.md), [build status](BUILD_STATUS.md), [live proofs](LIVE_PROOFS.md)
- [Consumer integration](docs/CONSUMER_INTEGRATION.md)
- [Deployment and live evidence gates](docs/DEPLOYMENT_GATES.md)
- [Ratchet comparison](docs/RATCHET_COMPARISON.md)
- [Historical agent handoff prompt (superseded)](CODEX_HANDOFF.md)
- [Official GenLayer non-determinism reference](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)
- [Official Direct Mode reference](https://docs.genlayer.com/api-references/genlayer-test/direct)
