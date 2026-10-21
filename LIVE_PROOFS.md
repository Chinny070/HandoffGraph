# HandoffGraph — Live StudioNet proofs

Network: GenLayer StudioNet, chain id 61999, RPC https://studio.genlayer.com/api.
Evidence files: `proofs/tx_log.tsv` (raw log written while running), `proofs/tx_reconciled.tsv` (every logged transaction re-read from the chain: final status, consensus result, leader execution result decoded, gas used), `proofs/V4_RUN.md` (all 94 core-v4 transactions with hashes and outcomes).
Reconciliation result: **325 transactions, 325 FINALIZED**, gas used 0 on all 325. Final status alone does not mean the contract accepted the call: each row's decoded outcome says whether the leader returned a value (`return`), rejected deliberately (`user_error:X`), or failed in the VM. Consensus `MAJORITY_DISAGREE` (10 transactions) and `NO_MAJORITY` (12) mean validators did not apply the transaction.

## Current deployment

| Contract | Address | Deploy tx |
|---|---|---|
| HandoffGraph core v4 | 0x82B4D2f2b2DcD9590CE605095515891BAE2aFB25 | 0x278c1d5aa329c92b79cc746342d199e254b06ccce68ac227366571dd330befd8 |
| Consumer example, bound to stage 1 | 0x98EF87D7C33D6d12E8B5d814FF8B896f96b05ad5 | see `V4_RUN.md` |
| Consumer example, bound to stage 3 | 0x05f11AE0835A1166Ee69A8213b7D5dF51D3c5a8D | see `V4_RUN.md` |
| Capability consumer, 25-minute expiry | 0x80564f838c275140236d27aD3d38EA85B1F6E13C | see `V4_RUN.md` |
| Capability consumer, 24-hour expiry | 0x9cF06d52283F6F05626745065198935F649D7FFf | see `V4_RUN.md` |

Workflow 1 root: `733128a79675de9b2a2bbea2c84ae822d972cccafacbe5de6a2cda19423b824e`. Evidence is pinned to commit `694f81ba502c1a5249e194b600795a92f8faa46c` (see `evidence/`).

**Source parity (all VERIFIED with `scripts/verify_source_parity.py`):** core v4 on-chain SHA-256 `7271b461e936eda678999d7aac1df246f46a1f1fb800e17296992b000400c535` equals the committed file in CRLF form (the form a Windows working copy uploads). The two consumer-example instances match `864f53e7…` and both capability consumers match `f5f8b0cf…`, again as CRLF. Earlier deployments are also verified: consumers `0x97cb…30fE`, `0x6C07…94F4`, `0x90E8…8C1E` match commit `c049f64`; core v3 matches its file.

Superseded deployments (kept for the record): core v1 `0x8252…bBed` (every source fetch failed closed, bug F1), v2 `0x6C01…c08C`, v3 `0x5E71…d447` (workflow 3 proofs), and several probe contracts.

## Actors

Owner `my-studionet-wallet` `0xaffe15ee…e70b`; worker `hg-worker` `0xb410641d…0c6d`; reviewer `hg-reviewer` `0x8d3a9a8a…6160` (created for this run). No transfers were made from the owner wallet.

## Lifecycle proofs on core v4 (all FINALIZED; hashes in `proofs/V4_RUN.md`)

| Item | Result | Transaction |
|---|---|---|
| Create, 6 stages, requirements, delivery timeout, seal | sealed | seal `0xe3d8094ac53073454f45f9d58b0485990a5ba3e3c203dfe31473a8c618c6ba7c` |
| Freeze blocks submission; non-owner cannot freeze | `WORKFLOW_FROZEN`, `ONLY_OWNER` | `0x4a927763…363b`, `0x5660df84…e864` |
| Support evidence: non-worker rejected, worker attach binds hash, second attach rejected | `ONLY_WORKER`, success (decision stores `support_sha256 1398f6e0…`), `SUPPORT_NOT_OPEN` | `0xc0abc7eb…a549`, `0x2a32c3d8…1a1b`, `0x7ee65028…1720` |
| Requirement-by-requirement AI evaluation | PASS, both requirements PASS | assess `0x741e80de6884e6643da7f0ff506c4a4eb9c6629df3296d2337553c8c17d6740e` |
| Appeal then final adjudication | final PASS, receipt `5c762a1e…5a00` | resolve `0x864206dd024d3f41e86ccc5a76f5a7403bb55ea536cfda54e3333f41aab15154` |
| Release while frozen | `WORKFLOW_FROZEN`; succeeds after thaw | `0x011471e5…c5f8`, release `0xb6386a2d723a7b14955518b33bddf4bf9b06de01e0a838480890cf6ed1ef4005` |
| Replayed release | `ALREADY_RELEASED` | `0xb96df3a3…abe0` |
| Legitimate FAIL, blocked release | final FAIL; release rejected `NOT_FINAL_PASS` | resolve `0x25f4ac55…9e16`, `0xb7182897…c3a1` |
| Retry and repaired evidence (stage 3) | assessment needed 4 attempts: 3 MAJORITY_DISAGREE (`0xb3cfdf79…a30`, `0x3e3afc1d…3267`, `0x8d73ca22…db00`) then success `0x4c158d90…9343`; final PASS, released | release `0xf473089e36c2be1ffade0b502004963dcfd50efade0e44f4628592961ded5ebb` |
| Consumer, stage 1: wrong receipt, non-operator, authorized execution, replay | `HANDOFF_NOT_RELEASED`, `ONLY_OPERATOR`, executed once, `ALREADY_EXECUTED` | `0x029009…1ddc`, `0x2c014ed2…69b4`, `0xdae6d816…0280`, `0xd015f342…8ccd` |
| Capability (25 min): consume, replay nonce, wrong action | consumed once, `CAPABILITY_INVALID` twice | `0x469cdd56…3b1c`, `0xddbfe655…0440`, `0x650664fd…5cc6` |
| Capability (24 h): non-operator, consume | `ONLY_OPERATOR`, consumed | `0x876e40ff…d5de`, `0x15b2873c…618b` |
| Counterexample opened (quarantine immediate), capability denied during court | `CAPABILITY_INVALID` | open `0x11b04191…2c2b`, deny `0x740ee153…4961` |
| Counterexample sustained, stage FAILED, descendants and capability denied | status 3; `is_release_active` false; stage 2 `can_submit` false; capability denied | resolve `0x1e35aa48…218e`, deny `0x65dd08a2…7d2b` |
| Counterexample appeal: outsider rejected, worker appeals, repair blocked while pending, appeal resolved | `ONLY_WORKER`; success; `COUNTER_APPEAL_PENDING`; UPHELD (status 7) | `0x92a975f4…35db`, `0x68c06764…6eba`, `0x7aa574af…ccce`, `0xf28a5e6e…1aec` |
| Repair after upheld counterexample, re-evaluation, new receipt | final PASS, new receipt `fb085e27…bdc4`; old receipt inactive | repair `0x20ef158f…f654`, resolve `0xa0e9a346…652b`, release `0x09916baa…b130` |
| Downstream authorization after recovery | stage 2 `can_submit` true, submission accepted | `0xbf147a3b…6890` |
| Capability and consumer after recovery | 24 h capability consumed with the new receipt (use_count 2), over-cap use denied; stage-3 consumer executed once on the finalized gate, replay `ALREADY_EXECUTED` | `0x75fb2a29…7f44`, `0xd2d3960f…5a3e`, `0x2e6305bc…edcc6`, `0xc528acec…d23f` |
| Unaffected branch | stage 3 independently failed, repaired and released while stage 1 was being quarantined and repaired | see above |
| Delivery deadline expiry | stage 4 expired to FAILED after its 1-hour deadline; second call `DELIVERY_NOT_EXPIRABLE` | `0x93c6c7d6…b155`, `0xfa8dcb39…6194` |
| Capability expiry | with the stage release still active, the expired capability was refused (`CAPABILITY_INVALID`), use_count unchanged | `0x6d105f2a…c465` |

Notes on rows: the transaction labelled `s1-appeal-outsider` in the raw log was actually sent by the worker (a valid appeal), not an outsider; outsider-appeal rejection is proven in Direct Mode. `s1-release-stale` and `s1-old-receipt` were rejected with `ALREADY_RELEASED` (the state check fires before the receipt check), so the `STALE_RECEIPT` branch is proven in Direct Mode, not live.

## Finality investigation (consumers)

- `StorageType.LATEST_FINAL` cross-contract reads hang on StudioNet. Reproduced against a trivial one-method contract (`0x7885…F820` read by probe `0x6CBB…6474`): the transaction never reached ACCEPTED within 300 s, and earlier consumer transactions ended `NO_MAJORITY` with `vm_error: timeout` after 600 s. Default and `LATEST_NON_FINAL` reads complete normally.
- Measured accepted-to-finalized lag on StudioNet was about 30 s.
- Working alternative, verified live: a probe (`0x01D4…4baA`) made every validator POST a `gen_call` with `status: finalized` to the RPC under strict-equality consensus; it returned `True` for released stage 11 and `False` for quarantined stage 9. Both consumers now use this as a second gate alongside the accepted-state gate and fail closed on any error. The residual trust in the RPC endpoint is documented in `docs/THREAT_MODEL.md` and `SECURITY_AUDIT.md`.

## Real-time deadline proofs still pending

Started on core v4 stages 5 and 6 and run by the detached script `scripts/run_timed_proofs.sh` (log: `proofs/timed_proofs.log`):

| Proof | Earliest time (unix) | Status at time of writing |
|---|---|---|
| Stage 5 `assess` rejected before the 12 h review window closes | now | done: rejected `REVIEW_WINDOW_OPEN` (`0x99f0b19d…f8d4`) |
| Stage 5 permissionless `assess` after the review window | 1792630168 | pending |
| Stage 6 `finalize_unappealed` rejected inside the 24 h appeal window | now | script attempts it |
| Stage 6 `finalize_unappealed` and release after the window | 1792673512 | pending |

## Not proven live (Direct Mode only, with warped time)

`expire_assessment`, `expire_appeal`, `expire_counterexample`, `expire_counter_appeal`, counterexample dismissal (PASS verdict) and counter-appeal OVERTURNED, and every window boundary at ±1 s. These need 24 h to 7 days of real time per case. They are covered by `direct_tests/test_handoff_lifecycle.py` (real GenVM runtime, mocked web/LLM, `direct_vm.warp`) and must not be read as live proofs.

## Findings made during live testing

1. F1: `response.status_code` does not exist in the GenVM web API (the field is `status`); the swallowed exception made every source fetch fail closed.
2. F6: `LATEST_FINAL` hang, above.
3. Strict consensus can stall a stage: the repaired-evidence assessment needed four attempts. Failure is closed (state unchanged) and retryable by anyone.
4. The CLI reports `FINALIZED` for transactions whose consensus result was `MAJORITY_DISAGREE`; callers must check the consensus result and re-read state, not just the status.
5. A shell bug in my first scripts passed an empty receipt argument to 11 calls, which the VM rejected as malformed calldata (`vm_error: exit_code 1`); these are tooling errors, not contract defects.

## Fees

`eth_gasPrice` returns 0, every one of the 325 reconciled transactions reports `gas_used` 0, and the worker and reviewer accounts (balance 0) submitted dozens of transactions. StudioNet charged no fees for this work. This says nothing about costs on any other network.
