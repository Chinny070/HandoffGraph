# Historical handoff prompt (superseded)

This file originally held the v0.3 instructions for an implementation agent, written when the package had no
GenVM, Direct Mode or StudioNet evidence and the GitHub repository was empty. Those instructions are obsolete.

Authoritative status lives in:

- `BUILD_STATUS.md` - current verdict and test tiers
- `LIVE_PROOFS.md` and `proofs/` - StudioNet deployments and reconciled transactions
- `SECURITY_AUDIT.md` - findings, fixes and residual risks
- `docs/DEPLOYMENT_GATES.md` - the verification gates and their status

Constraints that still hold: stable StudioNet (chain 61999) only; one standalone core with optional consumers;
sealed DAG with no admin override; release only after a final PASS with a complete requirement matrix and current
prerequisite receipts; no GEN custody; evidence limited to commit-pinned GitHub raw files with a SHA-256; never
claim an unexecuted test, consensus result or transaction.
