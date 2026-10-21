# HandoffGraph — Live StudioNet Proofs

Network: GenLayer StudioNet, chain id 61999, RPC https://studio.genlayer.com/api.
Every submitted transaction is logged in `proofs/tx_log.tsv` (label, account, method, hash, final status, consensus result, execution tally, note). Note: a few early rows have blank status because the CLI lost its RPC connection while polling; those transactions were re-verified by receipt where they matter, and the helper now retries.
Nothing below is inferred from mock tests.

## Final deployed contracts (current)

| Contract | Address | Deploy tx | Local source SHA-256 |
|----------|---------|-----------|----------------------|
| HandoffGraph core v3 | 0x5E716D24DB36Cb8F2C4E793a9295Ba2F341cd447 | 0xbc3e5100d870977aa2dbc4811a6af318cb0eee8738845d2402e748fb5e664003 | 99fa8f0db31aaa5ab200eb95b61083ab82f9f9cd16426f4b42f4ea003cdea3b0 |
| HandoffConsumerExample, stage 9 (released) | 0x97cb9feBC8c4F953F2F0CD787a19086f3fb430fE | 0xa997c2548c17e474123ef012e7aff9cf7a124f4a633ecc72717033665e85fdf7 | see note |
| HandoffConsumerExample, stage 11 | 0x6C07F7e2B17C3Ac5dAeeC9E0DAdf96E3C5f394F4 | 0x3f496e36d67493c5afc3bc6a95996a50db564e279a219bbb9b2a0c665f55f0f8 | see note |
| HandoffCapabilityConsumer, stage 9 | 0x90E857EbBC55717714e653361d0ca0e304028C1E | 0x336f995c8103684a583540bccecd367887485f85ccacd6e6297f522513f3ec42 | see note |

Note: the consumer sources on disk at deploy time were the committed `contracts/handoff_consumer_example.py` and `contracts/handoff_capability_consumer.py` of commit "Consumers use accepted-state single-call gate". Core source parity (on-chain `gen_getContractCode`, base64-decoded, SHA-256) was verified for core v1, v2 and v3 (v3 on-chain hash equals the local hash above). It was NOT checked for the three consumers.

Superseded deployments (kept for the record): core v1 `0x8252ab2Aa97373cb7C2a344427Ab12Ad06b7bBed` (failed closed on every source fetch because the code read `status_code`), core v2 `0x6C0188da134d7518b6198A9fd2e0e94066a5c08C` (consumers read 5 views and hung), probe `0xa7d69B09824aB66E23C238121754750046E35f66`.

## Actors

Owner `my-studionet-wallet` 0xaffe15eec45b68835cc9e5b4ab85dd5deae8e70b (pre-existing signer). Worker `hg-worker` 0xb410641df4727fc8fc950f2eb0805128cf490c6d and reviewer `hg-reviewer` 0x8d3a9a8a5a41fe6142e5922c60e5f8a8d0276160 were created for this run and funded from the StudioNet faucet. Nothing was transferred from the owner wallet.

## Evidence (pinned to commit 0139bc794606bfb203792b48d7ecc93ba4caf6bd)

delivery_pass.md 4cb07a3f…ccd3 · delivery_fail.md 0502c36b…6162 · counter_defect.md 748b6335…8c68 · delivery_repaired.md ccd46d56…2fe9 (full hashes in `proofs/tx_log.tsv` commands and `evidence/`).

## Verified lifecycle (workflow 3 on core v3, root 1819c907610f19067a83ef14a7cff60ef12f8ecd67c224a873ad9f739e895258)

All rows are FINALIZED transactions; AI evaluation used the StudioNet validator set with real pinned-source fetches.

| Item | Result | Evidence tx |
|------|--------|-------------|
| Create + seal, 4 stages, DAG 9→10, 2 mandatory requirements on stages 9–11 | sealed | seal `0xa94a2530…733a` |
| Stage 9 requirement-by-requirement evaluation | PASS, both requirements PASS | assess `0xdb43259e…6cdb` |
| Appeal then final adjudication, permissionless release | final PASS, released | resolve `0x519629fe…8cd3`, release `0xf95fdc8f…e71b` |
| Replayed release | rejected `ALREADY_RELEASED` | `0x138614de…2505` |
| Stage 11 FAIL on genuinely deficient evidence | final FAIL (stage 11 attempt 1), release blocked | appeal/resolve rows in log |
| Counterevidence challenge after release | counterexample sustained (status 3) | open `0x4d6ea13a…063b`, resolve `0x3887fa67…ae8f` |
| Causal quarantine | stage 9 quarantined, `is_release_active` false, downstream stage 10 `can_submit` false | reads in `life3` run |
| Unaffected branch | stage 11 recovered from FAIL with repaired evidence, final PASS and released | retry/resubmit/assess/resolve/release rows |
| Delivery deadline expiry | stage 12 expired to FAILED via `expire_delivery` | `0xd892f360…6908` |
| Validator disagreement | resolve_appeal on stage 11 returned MAJORITY_DISAGREE (votes AGREE, DISAGREE, DISAGREE, DISAGREE), no state change; retry succeeded | `0xfe1749d4…c191`, `0xafa1ad37…bea91` |
| Consumer: refused before final | `HANDOFF_NOT_RELEASED` | `0xf9186939…1264` |
| Consumer: unauthorized caller | rejected | `0x1e266eb8…bac` |
| Consumer: authorized action | executed once (`action_count: 1`) | `0x06e54050…98b0` |
| Consumer: replay | rejected `ALREADY_EXECUTED` | `0xda676b34…e137` |
| Capability: wrong action hash, unauthorized caller | rejected `CAPABILITY_INVALID` / not operator | `0xcae63931…f940`, `0x36cb25a7…983f` |
| Capability: consume nonce 1, replay nonce 1 | consumed once (`use_count: 1`), replay rejected | `0x4eea5ce0…4362`, `0xa868aa96…5410` |
| Capability after quarantine | rejected `CAPABILITY_INVALID` | `0x680002c3…e164` |
| Stage 11 consumer after repair and release | executed once, replay refused (`action_count: 1`) | `0xcdd563f3…d4c8d463`, `0xff7be98e…e046` |

## Not verified live

- Review-window (12 h) and appeal-window (24 h) expiry paths, `finalize_unappealed`, `expire_assessment`, `expire_appeal`, counterexample expiry: not waited out.
- Freeze/thaw, `attach_support`, `submit_repair`, counter-appeal (`appeal_counterexample`): no live run.
- Capability time expiry and revocation after a later countercase beyond the quarantine case above.
- Source parity for the three consumer deployments.

## Findings from live testing

1. `response.status_code` does not exist in the GenVM web API (field is `status`); the swallowed exception made every source fetch fail closed. Mock tests had the same wrong field. Fixed in core v2.
2. Cross-contract reads using `StorageType.LATEST_FINAL` hang on StudioNet: a probe transaction (`0x20e15ed0…c9c`) stayed in PROPOSING indefinitely, while default and `LATEST_NON_FINAL` reads complete. Consumers therefore read accepted state. Finality is enforced at the protocol level (the core only reports PASSED after appeal resolution), not at consensus-snapshot level. The original design invariant is therefore weakened on StudioNet.
3. A consumer making 5 cross-contract view calls timed out the leader (600 s). The core now exposes `is_release_bound`, a single-call gate used by both consumers.
4. Reads can briefly lag the last write on StudioNet (state read immediately after a write sometimes showed the previous state); sequence-dependent scripts must wait for the expected state.

## Fees

The owner wallet balance read 309.93 GEN before and after the run and the new accounts showed no balance requirement; no GEN fee was observed on StudioNet. Fees are therefore unmeasured rather than proven zero. No transfers were made.
