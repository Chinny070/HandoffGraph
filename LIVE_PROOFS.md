# HandoffGraph — Live StudioNet Proofs

Network: GenLayer StudioNet, chain id 61999, RPC https://studio.genlayer.com/api.
Every transaction is also logged in `proofs/tx_log.tsv` (label, account, method, hash, final status, consensus result, execution tally).
Only items marked VERIFIED were observed on-chain; nothing here is inferred from mock tests.

## Contracts

| Contract | Address | Deploy tx | Source SHA-256 | Source parity |
|----------|---------|-----------|----------------|---------------|
| HandoffGraph (core) | 0x8252ab2Aa97373cb7C2a344427Ab12Ad06b7bBed | 0x00b365cb494fb20269aaf25685e438fb35dfc188532a6c1ae2b57006ef3c8b1a | 09d16a99fc51d6371197677a90b576bcee31434fe9e64c5896717e640583fd83 | VERIFIED: base64-decoded `gen_getContractCode` bytes hash to the same SHA-256 as `contracts/handoff_graph.py` |

Deploy receipt: status FINALIZED, consensus MAJORITY_AGREE, execution SUCCESS.

## Actors

| Role | Account | Address |
|------|---------|---------|
| Owner | my-studionet-wallet (pre-existing signer) | 0xaffe15eec45b68835cc9e5b4ab85dd5deae8e70b |
| Worker | hg-worker (new, StudioNet faucet-funded) | 0xb410641df4727fc8fc950f2eb0805128cf490c6d |
| Reviewer | hg-reviewer (new, StudioNet faucet-funded) | 0x8d3a9a8a5a41fe6142e5922c60e5f8a8d0276160 |

## Evidence artifacts (pinned to commit 0139bc794606bfb203792b48d7ecc93ba4caf6bd)

| File | SHA-256 |
|------|---------|
| evidence/delivery_pass.md | 4cb07a3fea6afa772dee8335f9e2d7272be90b0fb72ef93bdf8ea23a4b8dccd3 |
| evidence/delivery_fail.md | 0502c36b448dc5c15f81b5c044ab17e60fe9420aaa0004704cb4e4ac12776162 |
| evidence/counter_defect.md | 748b6335cbabf9f3f55cb7d536d34e38837c547ffcb3c7f458c3570bbc398c68 |
| evidence/delivery_repaired.md | ccd46d561cddbf9b50af8736a74800037f89dfb3202542f73802fdf3c59c2fe9 |

## Lifecycle progress

Workflow 1 created and sealed (root 74b8996310b490546cfaa18b82cb29acd836a27a40e714b3b3a42a100eab8c87):
stages 1 (Ingest) -> 2 (Transform), stage 3 (Audit, independent), stage 4 (Spare, 3600 s delivery timeout);
two mandatory requirements on each of stages 1-3. All setup transactions reached FINALIZED / MAJORITY_AGREE.

Remaining lifecycle steps are appended below as they are executed and verified.
