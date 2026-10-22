# Independent deployment recheck

Pinned to commit `112d073a952b6a0e833c2814d70a01d350450f2f`. Chain id (RPC): `0xf22f` (61999 = 0xf22f). Checked 2026-10-22 09:14:31 UTC via https://studio.genlayer.com/api only.

## Deployed bytecode

| contract | address | on-chain SHA-256 | matches |
|---|---|---|---|
| HandoffGraph core v5 | `0x9629E19c11Ab40d9848575A8E699E1d48DBDA209` | `3dbff19303b347f0a1481a21b365e36f17b27df13d1e5097b0647a8681b88dcd` | CRLF of contracts/handoff_graph.py |
| Consumer example (stage 1) | `0xf7555975184b18F56223bb77b0E255761A4bFee0` | `5eb4b0d6b33ab30ac299e9bf4edc40d19ea254219827e61c03a63c1fa12b40ac` | CRLF of contracts/handoff_consumer_example.py |
| Consumer example (stage 3) | `0x05a4A3c90F8F1CFADEdEFc942D517bc9F5a76A74` | `5eb4b0d6b33ab30ac299e9bf4edc40d19ea254219827e61c03a63c1fa12b40ac` | CRLF of contracts/handoff_consumer_example.py |
| Capability consumer (25 min) | `0x1A263E205D65D3E452680D648c5051Fb2635fd16` | `3d497eabe22d22310e1dfb1897ca1eb40a72a8ee6e54435c7410603cf5ed86ab` | CRLF of contracts/handoff_capability_consumer.py |
| Capability consumer (24 h) | `0xF1b86f0B5FcE6E33435E424a09fbe076A745aeAC` | `3d497eabe22d22310e1dfb1897ca1eb40a72a8ee6e54435c7410603cf5ed86ab` | CRLF of contracts/handoff_capability_consumer.py |

## Representative transactions

| label | tx | status | consensus | outcome | expected | ok |
|---|---|---|---|---|---|---|
| seal | `0xb1a6dcacdbc174e5790df6dda83b7a2bdf6045f4751cd4075cfd808c1482268f` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| submit-while-frozen | `0x0cd862f03d32736e8a1b2d343d2c8c0d2f2f87dfd0cec3367f48f7e0f59e21a5` | FINALIZED | MAJORITY_AGREE | user_error:WORKFLOW_FROZEN | MAJORITY_AGREE / user_error:WORKFLOW_FROZEN | yes |
| freeze-by-nonowner | `0x00ec73c9851d3bcd59260e87b5581f0f299ddc82858e52a273f365a3041574cd` | FINALIZED | MAJORITY_AGREE | user_error:ONLY_OWNER | MAJORITY_AGREE / user_error:ONLY_OWNER | yes |
| s1-support | `0x0e9375768a02f68326311ee67b90201c9f20253fe6e5adfa5fe106a6df71f568` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| s1-support-again | `0xe09f02c05d101f357ec563d233e65d2966ae090cc05992b43ad69de3b66473fe` | FINALIZED | MAJORITY_AGREE | user_error:SUPPORT_NOT_OPEN | MAJORITY_AGREE / user_error:SUPPORT_NOT_OPEN | yes |
| s1-assess | `0x28ab69ae96d93423ea362b8ff24e43a99adb3b7fcf07913b78f3c1fffd156db6` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| s1-resolve | `0xff40af1a1a921907b66b7917a2cbcf85342c408f172b66c1c20913d64773e5c7` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| release-while-frozen | `0xe25d6f07c667c72b4c3bc27577d2d901a4afa47f73e47f6d17f6e4687b7407ca` | FINALIZED | MAJORITY_AGREE | user_error:WORKFLOW_FROZEN | MAJORITY_AGREE / user_error:WORKFLOW_FROZEN | yes |
| s1-release | `0x749764c0fa80ed18b07fbed9639f6d9bd990b00b33fa25d8ea3f5290c989e0b5` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| s1-release-replay | `0xc3cea0058d9604ef541335df2b3b84fdf8c4ccc97af927e5b062b0959ec64e71` | FINALIZED | MAJORITY_AGREE | user_error:ALREADY_RELEASED | MAJORITY_AGREE / user_error:ALREADY_RELEASED | yes |
| s3-release-failed | `0xa2133474536c66b836b5c51a207758924c1ea0720513fba227be6aa871f01fc7` | FINALIZED | MAJORITY_AGREE | user_error:NOT_FINAL_PASS | MAJORITY_AGREE / user_error:NOT_FINAL_PASS | yes |
| s3-release | `0xac95435592d80209784c817f4ac1ce7e693552f682f7da85ead4f23e99b503f1` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| CA-unauth | `0x4f430608de542dbd32a43eb7ed8e36461b6bc0c7a34ec8ae36a057425c8358a7` | FINALIZED | MAJORITY_AGREE | user_error:ONLY_OPERATOR | MAJORITY_AGREE / user_error:ONLY_OPERATOR | yes |
| CA-wrong-receipt | `0x8ea86fbf379d1afa60f35f366cd2c02f3d253a2fe6dffe86fc54ba49905358e5` | FINALIZED | MAJORITY_AGREE | user_error:HANDOFF_NOT_RELEASED | MAJORITY_AGREE / user_error:HANDOFF_NOT_RELEASED | yes |
| CA-exec | `0x9e2f7ed8bfad809f6828fba1ad3292f5e2ebbc160ae841f6c1456c7cf8cbcceb` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| CA-replay | `0xdcc3ff425e3d9f782da678309ed62647da02a927cf66000956e3af39e7810056` | FINALIZED | MAJORITY_AGREE | user_error:ALREADY_EXECUTED | MAJORITY_AGREE / user_error:ALREADY_EXECUTED | yes |
| CKS-consume-1 | `0x13ff5f0b3a1986ba8ba7ffbe20574342820889527fc72dae170d62eac099f436` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| CKS-replay-1 | `0x5e218133325f95401abcce24f42dfe965a75e2d8cb35d00850bc799cda0093b9` | FINALIZED | MAJORITY_AGREE | user_error:CAPABILITY_INVALID | MAJORITY_AGREE / user_error:CAPABILITY_INVALID | yes |
| CKS-wrong-action | `0x60ca8e69b1eb1dd7fe449f420dc1c78d78fde42dfb4441a316cb70e26e4ded10` | FINALIZED | MAJORITY_AGREE | user_error:CAPABILITY_INVALID | MAJORITY_AGREE / user_error:CAPABILITY_INVALID | yes |
| CKL-unauth | `0xbb252190a23574dcac6d8c04fe120f62b592fe5afee65500b2bd8196767cba4c` | FINALIZED | MAJORITY_AGREE | user_error:ONLY_OPERATOR | MAJORITY_AGREE / user_error:ONLY_OPERATOR | yes |
| cx-open | `0x2d09a708d69fc14fdab35e6f36d2113f7bdeec878e90680e444ed699ba34e2b5` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| cx-resolve | `0x9d575215b64fec5f77e5bf63d898710034a8a19a40d3ecd0a25f84ba9d4474d4` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| CKL-consume-after-cx | `0xb60a68328a6414b5af3503b8510de5948b9f36d9d99e66ff0a95fe255127c40a` | FINALIZED | MAJORITY_AGREE | user_error:CAPABILITY_INVALID | MAJORITY_AGREE / user_error:CAPABILITY_INVALID | yes |
| cx-appeal-outsider | `0x291d2693231434403bcd6daf4c6f491afce6d2cd48bdc122a5a4d57a6a1bd917` | FINALIZED | MAJORITY_AGREE | user_error:ONLY_WORKER | MAJORITY_AGREE / user_error:ONLY_WORKER | yes |
| cx-appeal | `0x350f373b67559f297b3bdeb160426f093058460f9aa21b632b5534d1417bc40d` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| repair-while-appeal-pending | `0x47b19a2d32011391cda164605b296a4ba0d6ee0ddb1fdca0a621f9da597ffc88` | FINALIZED | MAJORITY_AGREE | user_error:COUNTER_APPEAL_PENDING | MAJORITY_AGREE / user_error:COUNTER_APPEAL_PENDING | yes |
| cx-appeal-resolve | `0x49618d460b73ef6d3faabffb488f4e259968505545b2f840c9dbf56f78b5a08c` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| repair | `0x611356f34dbd036383f01c0a25c1a38369c65a6a2b579d898665f97e59267508` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| s1-release-2 | `0x99a02b81a2d2cf0e7b675b5bf3c87c168e96cadb638f87d4932a721834f9f3d9` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| s2-release-stale | `0xe68a592b629ad75616fec55af0ff9b3c9b84298cd69a6bd1ce1a29f92b2680d0` | FINALIZED | MAJORITY_AGREE | user_error:STALE_PREREQUISITE | MAJORITY_AGREE / user_error:STALE_PREREQUISITE | yes |
| s2-invalidate | `0xdd768fe9ca4b54ad11a54ec5060a69fd4ee3b21a4291d91ffea7c524fd6fa0d9` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| s2-invalidate-again | `0x0e76d6c3f31b28a82f337e31085982e054c0ae2fbb0767e8e69db0389d407bd0` | FINALIZED | MAJORITY_AGREE | user_error:NOT_INVALIDATABLE | MAJORITY_AGREE / user_error:NOT_INVALIDATABLE | yes |
| s2-release-2 | `0x26ace4a1bcf1974d8db3b11b56132feefe52cbf2a76a5227323e99b104ee6eab` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| CKL-consume-after-recovery | `0xedbec3285e7cc2df676a1b9e0bd06d58daf9f05418a5c0b060242aaf71e287e7` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| CKL-over-cap | `0xbb20cafcc716f926faf8284dd8901544180068fd824ca15c6af0cff4c48ea7f7` | FINALIZED | MAJORITY_AGREE | user_error:CAPABILITY_INVALID | MAJORITY_AGREE / user_error:CAPABILITY_INVALID | yes |
| CA3-exec | `0x9740754bf6714f7d80cb7c6122ec9c2b6d68e18906733c06d71aac6c1c96263d` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| CA3-replay | `0xde94a863d54fd08089bf0830d91d84bc4ece110f9807d83729101f27c8ed0451` | FINALIZED | MAJORITY_AGREE | user_error:ALREADY_EXECUTED | MAJORITY_AGREE / user_error:ALREADY_EXECUTED | yes |
| expire-delivery-4 | `0xfa53fc958f56c5022914fbb8735cd29527e02812072df3b2aa6b3715197a243e` | FINALIZED | MAJORITY_AGREE | return | MAJORITY_AGREE / return | yes |
| expire-delivery-4-again | `0x365fb6bdce397b3935695f8ae04e40987621e02609224da92ba7a4c373834e1d` | FINALIZED | MAJORITY_AGREE | user_error:DELIVERY_NOT_EXPIRABLE | MAJORITY_AGREE / user_error:DELIVERY_NOT_EXPIRABLE | yes |
| CKS-after-expiry | `0x51f758fda714ff37aca548311e1c295d6583aee17153c078cadd95f570760c36` | FINALIZED | MAJORITY_AGREE | user_error:CAPABILITY_INVALID | MAJORITY_AGREE / user_error:CAPABILITY_INVALID | yes |

Result: **ALL CHECKS PASSED**
