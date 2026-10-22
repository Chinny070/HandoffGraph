# HandoffGraph — Live StudioNet proofs

Network: GenLayer StudioNet, chain id 61999, RPC https://studio.genlayer.com/api.

## Evidence files

| File | What it is |
|---|---|
| `proofs/tx_log.tsv` | Raw log written while the scripts ran |
| `proofs/tx_reconciled.tsv` | **496 logged transactions re-read from the chain**: final status, consensus result, decoded leader outcome, gas used |
| `proofs/V5_RUN.md` | All 99 transactions of the current (v5) run with hashes and outcomes |
| `proofs/V4_RUN.md` | The earlier v4 run (superseded contracts, see below) |
| `proofs/RECHECK.md` | RPC-only recheck pinned to a commit: deployed bytecode of 5 contracts and 40 representative transactions |
| `proofs/lifecycle_v5.log.txt`, `proofs/post_deadlines_v5.log.txt` | Console output of the v5 scripts |
| `proofs/aborted_run_v5a_lifecycle.log.txt` | An aborted attempt kept for honesty (see "Abandoned runs") |

Reconciliation: all 496 logged transactions are FINALIZED, gas used 0 on every one. Final status alone does not mean the call was accepted by the contract; the decoded outcome says so. Consensus `MAJORITY_DISAGREE` (10) and `NO_MAJORITY` (12) transactions were not applied by validators; none of those are in the v5 run (all 99 v5 transactions are MAJORITY_AGREE: 76 returns, 23 deliberate rejections).

## Current deployment (v5; sources are those of commit `112d073a952b6a0e833c2814d70a01d350450f2f`)

| Contract | Address | On-chain SHA-256 | Parity |
|---|---|---|---|
| HandoffGraph core v5 | `0x9629E19c11Ab40d9848575A8E699E1d48DBDA209` | `3dbff19303b347f0a1481a21b365e36f17b27df13d1e5097b0647a8681b88dcd` | CRLF of `contracts/handoff_graph.py` |
| Consumer example, stage 1 | `0xf7555975184b18F56223bb77b0E255761A4bFee0` | `5eb4b0d6…40ac` | CRLF of `contracts/handoff_consumer_example.py` |
| Consumer example, stage 3 | `0x05a4A3c90F8F1CFADEdEFc942D517bc9F5a76A74` | `5eb4b0d6…40ac` | same |
| Capability consumer, 25-minute expiry | `0x1A263E205D65D3E452680D648c5051Fb2635fd16` | `3d497eab…86ab` | CRLF of `contracts/handoff_capability_consumer.py` |
| Capability consumer, 24-hour expiry | `0xF1b86f0B5FcE6E33435E424a09fbe076A745aeAC` | `3d497eab…86ab` | same |

Parity means the base64-decoded `gen_getContractCode` bytes hash to the same SHA-256 as the committed file after converting to CRLF (a Windows working copy uploads CRLF; the git blob is LF). Verified by `scripts/verify_source_parity.py` and independently re-verified over the RPC only by `scripts/recheck_deployment.py` (`proofs/RECHECK.md`, result: ALL CHECKS PASSED).

Workflow 1 root: `648abf43d19429ef5ad4051d2de649025c67cdb4f2b6d2bf23f9d375d6b900f7`; actors: owner `my-studionet-wallet` `0xaffe15ee…e70b`, worker `hg-worker` `0xb410641d…0c6d`, reviewer `hg-reviewer` `0x8d3a9a8a…6160`. Evidence is pinned to commit `694f81ba502c1a5249e194b600795a92f8faa46c` (`evidence/`).

## Lifecycle proofs on core v5 (all FINALIZED, MAJORITY_AGREE)

| Item | Outcome | Transaction |
|---|---|---|
| Create, 6 stages, requirements, delivery timeout, seal | sealed | seal `0xb1a6dcacdbc174e5790df6dda83b7a2bdf6045f4751cd4075cfd808c1482268f` |
| Freeze blocks submission | `WORKFLOW_FROZEN` | `0x0cd862f03d32736e8a1b2d343d2c8c0d2f2f87dfd0cec3367f48f7e0f59e21a5` |
| Support evidence attached (hash bound into the decision); second attach | success; `SUPPORT_NOT_OPEN` | `0x0e937576…f568`, `0xe09f02c0…` |
| Requirement-by-requirement evaluation, appeal, final adjudication | PASS | assess `0x28ab69ae96d93423ea362b8ff24e43a99adb3b7fcf07913b78f3c1fffd156db6`, resolve `0xff40af1a1a921907b66b7917a2cbcf85342c408f172b66c1c20913d64773e5c7` |
| Release while frozen; release after thaw; replay | `WORKFLOW_FROZEN`; released; `ALREADY_RELEASED` | `0xe25d6f07…07ca`, `0x749764c0fa80ed18b07fbed9639f6d9bd990b00b33fa25d8ea3f5290c989e0b5`, `0xc3cea005…4e71` |
| Legitimate FAIL, blocked release, retry, repaired evidence PASS, release | final FAIL; `NOT_FINAL_PASS`; later PASS and released | `0xcca40e86…0bd5`, `0xa2133474…1fc7`, `0xac95435592d80209784c817f4ac1ce7e693552f682f7da85ead4f23e99b503f1` |
| Downstream stage 2 released against stage 1's first receipt | active | release `0x6af64ca3180d08e13b5b2d4b4271d842ce880c5357809917102b91a0dd5507db` |
| One-shot consumer: non-operator, wrong receipt, authorized execution on the finalized gate, replay | `ONLY_OPERATOR`; `HANDOFF_NOT_RELEASED`; executed once; `ALREADY_EXECUTED` | `0x4f430608…58a7`, `0x8ea86fbf…58e5`, `0x9e2f7ed8bfad809f6828fba1ad3292f5e2ebbc160ae841f6c1456c7cf8cbcceb`, `0xdcc3ff42…0056` |
| Capability: consume, replay nonce, wrong action, non-operator | consumed once; `CAPABILITY_INVALID` x2; `ONLY_OPERATOR` | `0x13ff5f0b…f436`, `0x5e218133…93b9`, `0x60ca8e69…`, `0xbb252190…` |
| Counterexample opened (immediate quarantine), resolved SUSTAINED | stage 1 and released descendant stage 2 both inactive; capability denied | open `0x2d09a708d69fc14fdab35e6f36d2113f7bdeec878e90680e444ed699ba34e2b5`, resolve `0x9d575215b64fec5f77e5bf63d898710034a8a19a40d3ecd0a25f84ba9d4474d4`, deny `0xb60a68328a6414b5af3503b8510de5948b9f36d9d99e66ff0a95fe255127c40a` |
| Counterexample appeal: outsider; worker; repair blocked while pending; resolved | `ONLY_WORKER`; success; `COUNTER_APPEAL_PENDING`; UPHELD (status 7) | `0x291d2693…`, `0x350f373b…c40d`, `0x47b19a2d…`, `0x49618d460b73ef6d3faabffb488f4e259968505545b2f840c9dbf56f78b5a08c` |
| Repair and re-release of stage 1 | new receipt; old receipt inactive | repair `0x611356f3…7508`, release `0x99a02b81a2d2cf0e7b675b5bf3c87c168e96cadb638f87d4932a721834f9f3d9` |
| **Descendant bound to prerequisite receipts (new)**: stage 2 after stage 1's repair | `prerequisites_current: false`, release inactive; `release` rejected `STALE_PREREQUISITE` | `0xe68a592b629ad75616fec55af0ff9b3c9b84298cd69a6bd1ce1a29f92b2680d0` |
| Stale descendant invalidated, repeat rejected, repaired, re-evaluated, re-released | success; `NOT_INVALIDATABLE`; new receipt active, old inactive | invalidate `0xdd768fe9ca4b54ad11a54ec5060a69fd4ee3b21a4291d91ffea7c524fd6fa0d9`, again `0x0e76d6c3f31b28a82f337e31085982e054c0ae2fbb0767e8e69db0389d407bd0`, release `0x26ace4a1bcf1974d8db3b11b56132feefe52cbf2a76a5227323e99b104ee6eab` |
| Capability and consumer after recovery | consumed with the new receipt; over-cap `CAPABILITY_INVALID`; stage-3 consumer executed once, replay `ALREADY_EXECUTED` | `0xedbec328…87e7`, `0xbb20cafc…a7f7`, `0x9740754bf6714f7d80cb7c6122ec9c2b6d68e18906733c06d71aac6c1c96263d`, `0xde94a863…0451` |
| Delivery deadline (1 h) expiry | stage 4 FAILED; second call `DELIVERY_NOT_EXPIRABLE` | `0xfa53fc958f56c5022914fbb8735cd29527e02812072df3b2aa6b3715197a243e`, `0x365fb6bd…4e1d` |
| Capability expiry (25 min) | refused with the stage release still active | `0x51f758fda714ff37aca548311e1c295d6583aee17153c078cadd95f570760c36` |

## Finality investigation

- `StorageType.LATEST_FINAL` cross-contract reads hang on StudioNet. Reproduced against a trivial one-method contract; earlier consumer calls ended `NO_MAJORITY` with a 600 s `vm_error: timeout` (visible in `tx_reconciled.tsv`). Default and `LATEST_NON_FINAL` reads complete.
- Measured accepted-to-finalized lag on StudioNet: roughly 30 s.
- Implemented alternative: each consumer requires the accepted-state gate AND a finalized-state gate in which every validator POSTs a `gen_call` with `status: finalized` to the RPC under strict equality; the JSON-RPC envelope is validated (version, id, no error, no extra keys, bounded size, hex result decoding to exactly `True`).
- **This is not trustless finality.** The finalized gate trusts the StudioNet RPC endpoint. A dishonest endpoint can only deny or fall back to accepted-state protection; it cannot authorize anything the accepted-state gate denies. The consumers' `get_status` reports `trustless_finality: false`. Do not use the examples for irreversible authorization where RPC trust is unacceptable.

## Real-time deadline proofs not yet complete

`scripts/live/timed_proofs.sh` was started on core v5 stages 5 and 6 (log: `proofs/timed_proofs_v5.log.txt`):

| Proof | Earliest time (unix) | Status when this was written |
|---|---|---|
| Stage 5 `assess` rejected before the review window closes | now | done: `REVIEW_WINDOW_OPEN` (`0x750f9a16…1175`) |
| Stage 5 permissionless `assess` after the 12 h review window | 1792701652 | pending |
| Stage 6 `finalize_unappealed` rejected inside the appeal window | now | script attempts it |
| Stage 6 `finalize_unappealed` and release after the 24 h window | 1792745043 | pending |

If that process is no longer running, rerun the script with the same `GL_*` variables; it is safe to repeat.

## Not proven live (Direct Mode only, with warped time)

`expire_assessment`, `expire_appeal`, `expire_counterexample`, `expire_counter_appeal`, counterexample dismissal (PASS) and counter-appeal OVERTURNED, and every window boundary at ±1 s: covered by `direct_tests/test_handoff_lifecycle.py` on the real GenVM runtime with mocked web/LLM; these are not live evidence. Malicious-leader and dishonest-RPC behaviour are likewise tested only in Direct Mode and offline, not live.

## Superseded, abandoned and probe deployments

Kept on chain for the record; none should be used. Core v1 `0x8252…bBed` (every source fetch failed closed), v2 `0x6C01…c08C`, v3 `0x5E71…d447`, v4 `0x82B4D2f2b2DcD9590CE605095515891BAE2aFB25` (verified earlier run, `V4_RUN.md`; predates the `source_ok` binding and descendant binding), v5a core `0x3a87283a433692667CffF98be01F2Bb5654c5091` with four consumers from an aborted run (another process changed the CLI's shared active account mid-run, so many submissions failed; the live scripts now isolate their own CLI home and abort on the first submission failure), and several probe contracts.

## Findings made during live testing

1. `response.status_code` does not exist in the GenVM web API (the field is `status`); the swallowed exception made every source fetch fail closed.
2. `LATEST_FINAL` hang (above).
3. Strict consensus can stall a stage; assessments sometimes needed several attempts. The CLI reports `FINALIZED` even for transactions whose consensus did not apply them, so scripts must check the consensus result.
4. The genlayer CLI keeps one global "active account"; another process on the same profile switched it during a run. Isolating the CLI home fixed that.
5. Early shell scripts passed empty receipt arguments to 11 calls, which the VM rejected as malformed calldata; tooling errors, not contract defects.

## Fees

`eth_gasPrice` returns 0 and every one of the 496 reconciled transactions reports `gas_used` 0; accounts with a 0 balance submitted dozens of transactions. StudioNet charged nothing here. This says nothing about other networks.
