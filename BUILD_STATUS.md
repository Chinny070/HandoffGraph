# HandoffGraph v0.3 — evidence-based build status

**Date:** 2026-10-20. **Verdict:** LOCAL BUILD READY; GENVM/NETWORK RELEASE BLOCKED.

## Completed here

- Standalone main IC: DAG, sealed requirement matrix, independent verdict and requirement consensus, pinned evidence bundle, reviewer challenge, provisional appeal, permissionless finalization, one-time release, transitive causal quarantine, bounded post-release counterexample court and appeal, repair/re-evaluation, safe deadline expiry, hash certificates and effective release capability views.
- Two separately deployable optional examples: one-shot protected action and bounded action hash/nonce/expiry capability consumer. Neither is required by the core.
- Unit and adversarial negative regression suite: **133 passed** using clearly labelled mock GenLayer runtime.
- Structural AST preflight: **33/33 passed**; Python bytecode syntax compilation passes.
- Sources and ZIP handoff package prepared with local SHA-256 manifest.

## Explicitly not completed

- No real GenVM semantic lint tool or `genlayer-test` is installed here. No actual Direct Mode validator execution was run. Existing Direct Mode scenarios are **drafts**, not passes.
- No live StudioNet deployment, explorer address, transaction hash, fee receipt or contract source parity is available. No GEN spent.
- GitHub `Chinny070/HandoffGraph` was **empty when checked**. The container cannot resolve `github.com` and therefore cannot push git commits via its terminal; the complete source bundle has not been claimed as pushed. Codex handoff explicitly requires pushing source, after checking for concurrent changes.
- GenVM serialization and nested consensus performance for a ~50KB core, cross-contract final-state reads, `TreeMap` storage, source-fetch byte compatibility and fee estimation still need real proof before production claims.

## Packaging rules

Unzip into a working directory; install only trusted package versions; run `python -m pytest tests/ -q`, `python scripts/preflight.py`, compile and SDK checks; upload **all** project files, not just the ZIP. The Codex/Claude prompt is `CODEX_HANDOFF.md`. Never treat offline test count as onchain evidence or claim it scored higher than Ratchet without reviewer results.
