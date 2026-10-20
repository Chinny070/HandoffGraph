# Optional consumer contracts

The main HandoffGraph core stands alone. Consumers are separately deployed demonstrations; neither is required for contract eligibility.

1. `handoff_consumer_example.py`: binds to immutable graph address, workflow ID/root, stage ID and operator. `execute_once(receipt)` executes a protected action once only when the target stage is a final PASS, released, currently unquarantined, and historical Decision identity matches the submission/attempt. It uses `StorageType.LATEST_FINAL` and queries `is_release_active`.
2. `handoff_capability_consumer.py`: binds the same fields plus a 64-hex `action_hash`, expiry timestamp, immutable max uses (1–32), and nonce 1–32. `consume(nonce, requested_action, receipt)` requires correct operator, exact action, unused nonce, remaining usage and final-active graph proof. The action is demonstrated as an onchain capability consumption **event**, not a privileged call into an external EVM contract. Integration with an actual application requires that application's own authorization logic.

**Adversarial cases:** revoked upstream stage, paused workflow, mismatched root, mismatched stage, mismatched historical Decision, wrong receipt, early/non-final PASS, expired capability, wrong action, repeated nonce, wrong operator, usage cap, source unavailable. All must deny. Offline tests exist; actual cross-contract `LATEST_FINAL` read behavior and return types must be independently validated in GenVM and StudioNet before deployment claims.

**Integration sequence:** deploy core; create workflow and stage; seal, submit artifact, assess and finalize; release and verify `is_release_active` on latest-final state; deploy consumer pinned to actual workflow root; demonstrate pre-PASS or unreleased denial and final-PASS success; open counterexample and demonstrate **future** consumed actions deny; verify old already-consumed actions are not reversed. Never use unfinalized or optimistic state to authorize a protected action.
