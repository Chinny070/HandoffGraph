# Core v4 run — every transaction (auto-generated from `proofs/tx_reconciled.tsv`)

Core `0x82B4D2f2b2DcD9590CE605095515891BAE2aFB25`. Outcome = leader receipt result decoded from chain: `return` is success, `user_error:X` is a deliberate contract rejection, `vm_error` is a VM-level failure. Consensus `MAJORITY_DISAGREE` / `NO_MAJORITY` means validators did not apply the transaction.

| # | label | tx | consensus | outcome |
|---|---|---|---|---|
| 1 | deploy-core-v4 | `0x278c1d5aa329c92b79cc746342d199e254b06ccce68ac227366571dd330befd8` | MAJORITY_AGREE | return:1 bytes |
| 2 | create | `0x7f59777ef95b3b959fa12abb68459b3869ab4c51920a6863ab94229b1512b900` | MAJORITY_AGREE | return:1 bytes |
| 3 | st1 | `0xfafc2c29fcd006f0e337cdae9271c80375df44ef7e61c211c17add0b92d21331` | MAJORITY_AGREE | return:1 bytes |
| 4 | st2 | `0x5dd5a1e330920e7faa84f3db219e757b758c9e1c17f92bee692ef7d4f9e03b60` | MAJORITY_AGREE | return:1 bytes |
| 5 | st3 | `0xefd538b60ccf5f320560647143543f9d8e7f7211c7c9ffd15e9c85eaa7422e5f` | MAJORITY_AGREE | return:1 bytes |
| 6 | st4 | `0x7144cb53d544b2283e2d5c0819ac524ba44c049f1440a97983b8a8812f200c3c` | MAJORITY_AGREE | return:1 bytes |
| 7 | st5 | `0x657ffda14fc8ce1446df725cbcadd08041229a4726bce6dad6ce2d7d2d7d8608` | MAJORITY_AGREE | return:1 bytes |
| 8 | st6 | `0x5f2229a8fc6ad6fffd63c8c893367f7131f7ea13b937632590c9bafc9fcd27d8` | MAJORITY_AGREE | return:1 bytes |
| 9 | req1-a | `0x696218cff92f440565cfbfdcfe5b7d61b578bce11baf78e1f52ad0040091cc1f` | MAJORITY_AGREE | return:1 bytes |
| 10 | req1-b | `0xe32e0f1926bc2a631b3ac0758cd0c2a32c98c8fa78fa55f59e02079f1fb81370` | MAJORITY_AGREE | return:1 bytes |
| 11 | req3-a | `0x2412d549e797f9eed8bdce9a1e169b4229c3bc281cee33f99f8ede78e9e7ea50` | MAJORITY_AGREE | return:1 bytes |
| 12 | req3-b | `0x599284dcdeaabdf29972bb4ca903d3908da2a98dce22837f6a7cb96ca6a239f4` | MAJORITY_AGREE | return:1 bytes |
| 13 | timeout4 | `0x15ba2914ed80e63ecb5f2a93030881c5fea2926712c641a25b5aad63a14392f3` | MAJORITY_AGREE | return:1 bytes |
| 14 | seal | `0xe3d8094ac53073454f45f9d58b0485990a5ba3e3c203dfe31473a8c618c6ba7c` | MAJORITY_AGREE | return:66 bytes |
| 15 | freeze | `0x1994b5fc6d441e1c9d7c6357a93e1b06f5384ee191f9e4e76e34eedb5c1d8765` | MAJORITY_AGREE | return:1 bytes |
| 16 | submit-while-frozen | `0x4a927763db8d78bcd43648c29970e3bfefb60e629c1418fe88b75e64f18d363b` | MAJORITY_AGREE | user_error:WORKFLOW_FROZEN |
| 17 | thaw | `0x7030be8c677ea69d8939d2f466fcdaabcd0f7c1a06af780d14c8fe12e307bf38` | MAJORITY_AGREE | return:1 bytes |
| 18 | freeze-by-nonowner | `0x5660df844a1ba330959d77f17c39920b96853bf06e102feadae49a255ebbe864` | MAJORITY_AGREE | user_error:ONLY_OWNER |
| 19 | s1-submit | `0x402fb804cd357ce6782a782f61d6499e0cf8ecba2cbda63a3c05592d0c9c6824` | MAJORITY_AGREE | return:66 bytes |
| 20 | s1-support-nonworker | `0xc0abc7eb4541b989196fd0d8eca464f67e4df6bb9d1a2aeb4dd837fe50f1a549` | MAJORITY_AGREE | user_error:ONLY_WORKER |
| 21 | s1-support | `0x2a32c3d836828e4c2e3d52db78efb237ca63911c19d20f52673342c207731a1b` | MAJORITY_AGREE | return:1 bytes |
| 22 | s1-support-again | `0x7ee650282c07618068f51af772d72e2a5018dd774a3eefcb72511c4a2fd91720` | MAJORITY_AGREE | user_error:SUPPORT_NOT_OPEN |
| 23 | s1-challenge | `0xb232d208d415a425d1b6cb36b9d581faa4b227407109278f709ba966f8d08d45` | MAJORITY_AGREE | return:1 bytes |
| 24 | s1-assess | `0x741e80de6884e6643da7f0ff506c4a4eb9c6629df3296d2337553c8c17d6740e` | MAJORITY_AGREE | return:1 bytes |
| 25 | s1-appeal-outsider | `0x7379c4387c0ab1880a95bae774b73bb7935d79f51857c02c21f92ea31fcc394e` | MAJORITY_AGREE | return:1 bytes |
| 26 | s1-resolve | `0x864206dd024d3f41e86ccc5a76f5a7403bb55ea536cfda54e3333f41aab15154` | MAJORITY_AGREE | return:66 bytes |
| 27 | freeze2 | `0x86ec516aa59acc4dde8f4158187bf2908e9539a07dd301d8a927b7ce9648ac85` | MAJORITY_AGREE | return:1 bytes |
| 28 | release-while-frozen | `0x011471e51f76f782ddd5c55af036c883d866834c6f47c7059de8e28f81f3c5f8` | MAJORITY_AGREE | user_error:WORKFLOW_FROZEN |
| 29 | thaw2 | `0x10f00d62941db1be5df47f0ed90663e10f417c35353f53bbca572e715cc09efb` | MAJORITY_AGREE | return:1 bytes |
| 30 | s1-release | `0xb6386a2d723a7b14955518b33bddf4bf9b06de01e0a838480890cf6ed1ef4005` | MAJORITY_AGREE | return:66 bytes |
| 31 | s1-release-replay | `0xb96df3a3f55088da4fe8040fdb1f96f351340ceabdec254ae2cf4b4e8e91abe0` | MAJORITY_AGREE | user_error:ALREADY_RELEASED |
| 32 | s1-release-stale | `0x3f54f5aec05e861d47c069516b977f7759c62ca4175e758a4d5d34eb623fb111` | MAJORITY_AGREE | user_error:ALREADY_RELEASED |
| 33 | s3-submit | `0x12c110b958bce807c3e13655212157e9e1148791a85ac04f778bfe6dfae6f461` | MAJORITY_AGREE | return:66 bytes |
| 34 | s3-challenge | `0x7a10a8803c96adb3fd490517046eb78ba3fc7e25d5669b4f539a85dd14d98494` | MAJORITY_AGREE | return:1 bytes |
| 35 | s3-assess | `0xe6158bc9a9c343a423d9e96d64fe2eb25d6dc4e095519a72a4e65071a8c0438d` | MAJORITY_AGREE | return:1 bytes |
| 36 | s3-appeal | `0x07213ebc35785143c5830ed5fbb8ad4d10e4f9f991a7bd107f2c6aa74ba4239d` | MAJORITY_AGREE | return:1 bytes |
| 37 | s3-resolve | `0x25f4ac556a2543d271825590613a38a38c2a9e2ddb9cb0c97fb6cda19be79e16` | MAJORITY_AGREE | return:66 bytes |
| 38 | s3-release-failed | `0xb7182897800ca66dcf654833ae59afad9d625b117b03eb1151afce4ce5eac3a1` | MAJORITY_AGREE | user_error:NOT_FINAL_PASS |
| 39 | s3-retry | `0xa31017e8ef36178fc6fa68aa1236258c4f358b87e77f65fc604ea7e3a2818f83` | MAJORITY_AGREE | return:1 bytes |
| 40 | s3-submit2 | `0xbfec8170e0abef06a19342b3a666a22ea25c82b750027d0256ea94b9673ee9c1` | MAJORITY_AGREE | return:66 bytes |
| 41 | s3-challenge2 | `0x65a3d5b23327a892682f41314e84df0fd2cea41d430bf38d5446b107daa95a25` | MAJORITY_AGREE | return:1 bytes |
| 42 | s3-assess2 | `0xb3cfdf796c19791b2bf229c4055f89bc5dcf51c7c425c0d25900f384222a6a30` | MAJORITY_DISAGREE | return:1 bytes |
| 43 | s3-assess2 | `0x3e3afc1dfff5ba699ed1421a98d295ec748a02fd5c1669ecf190ae7ca7113267` | MAJORITY_DISAGREE | return:1 bytes |
| 44 | s3-assess2 | `0x8d73ca22c32a38ab893c457fcd702ad2a3b7d01930d70d454e8fb8c4db66db00` | MAJORITY_DISAGREE | return:1 bytes |
| 45 | s3-appeal2 | `0x08a00bebb67e8748089dbb7a2eea183c10ff183013c939065c032822aebb788d` | MAJORITY_AGREE | user_error:NOT_APPEALABLE |
| 46 | s3-resolve2 | `0x8ec1ca71986b4815a24e2fb1353b9b4fd1115ab06c3548aaae5a6f56acfcb803` | MAJORITY_AGREE | user_error:NO_PENDING_APPEAL |
| 47 | s3-release | `0x35c2b801d2adec9f6ef011d36beaea9509e2140c0765091d632d165102af0108` | MAJORITY_AGREE | vm_error:exit_code 1 |
| 48 | deploy | `0x29dd61845dac5897c2dd6d6d732650e5eba98c8296ca954b990b6d600b71fb8e` | MAJORITY_AGREE | return:1 bytes |
| 49 | deploy | `0x6d834283aca423d4d7672834abbbc96db5413ccc5ba6abdd0212a05172575ca1` | MAJORITY_AGREE | return:1 bytes |
| 50 | deploy | `0xdf956a35c623e18ceec31bf8384a9e28c1e0151a5eb9021ec4128463738a2090` | MAJORITY_AGREE | return:1 bytes |
| 51 | deploy | `0x8f12844f9ebcf028a63e9e7b20fc7bb9f11acc0027e191d3276cf897afe3edd4` | MAJORITY_AGREE | return:1 bytes |
| 52 | CA-unauth | `0x2c014ed230f3701087dcce5ac4c28699eacf614d0b321ad9e923b744e8da69b4` | MAJORITY_AGREE | user_error:ONLY_OPERATOR |
| 53 | CA-wrong-receipt | `0x029009029318b5f5980af50c256ceb60337906dddb1daa87b0bd998d53b71ddc` | MAJORITY_AGREE | user_error:HANDOFF_NOT_RELEASED |
| 54 | CA-exec | `0xdae6d816f05cf73cb296c90cc37c26fcd4794efd50a728175813f52525bb0280` | MAJORITY_AGREE | return:1 bytes |
| 55 | CA-replay | `0xd015f34209f6769bbf6308b14203a1c5f1f1b6dc50f10b420687649bafb78ccd` | MAJORITY_AGREE | user_error:ALREADY_EXECUTED |
| 56 | CKS-consume-1 | `0x469cdd5640e93ba91f81ad52e7c3a851e9da95b3d2ae1b2fac44a0266bd73b1c` | MAJORITY_AGREE | return:1 bytes |
| 57 | CKS-replay-1 | `0xddbfe65510d7d2ea0a09c002341e65cff3ba9e99c9be4e12b8fcecef609c0440` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 58 | CKS-wrong-action | `0x650664fd44e92b8859253d0b75636eb7c28cd9c1ab310671edacd2a08fd95cc6` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 59 | CKL-unauth | `0x876e40ff80701c72ce6230dadc48771189fee954ce688cf1a10a986f56b6d5de` | MAJORITY_AGREE | user_error:ONLY_OPERATOR |
| 60 | CKL-consume-1 | `0x15b2873ce8427f62c51fbe820c76fcb88a251c69cf59f2a9068ff98d45e6618b` | MAJORITY_AGREE | return:1 bytes |
| 61 | cx-open | `0x11b04191d9da97d22671cab0de526cee55d6553e97c06ce30853cf88c7642c2b` | MAJORITY_AGREE | return:1 bytes |
| 62 | CKL-consume-during-cx | `0x740ee153c5bb29b0e31b2c08bb78360d382cda95bc460c733f56327ec7f14961` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 63 | cx-resolve | `0x1e35aa4888a0e8f7b70242ab2684c71376a6ecd777fcb938d16ffee294b8218e` | MAJORITY_AGREE | return:66 bytes |
| 64 | CKL-consume-after-cx | `0x65dd08a2db758ddb0e0780b26899efcf63c465d1aa5fdb38239b651cf9ea7d2b` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 65 | CA3-before-final | `0xeec47e1b9c624b5a405b7790d4c437edb9afcb7fc73cca191788dfc67e657d2d` | MAJORITY_AGREE | vm_error:exit_code 1 |
| 66 | cx-appeal-outsider | `0x92a975f47b5c81f7b81f2da53f722aadbc93d9f5ddbcfd32099d914d0c6235db` | MAJORITY_AGREE | user_error:ONLY_WORKER |
| 67 | cx-appeal | `0x68c06764d91b965d9193c04f2505015b1f5b59e7581d16cd7d92fc1ba7c86eba` | MAJORITY_AGREE | return:1 bytes |
| 68 | repair-while-appeal-pending | `0x7aa574af1c4c59bd8a94189c0f579a9fe1af4e0f5f4fb2523c9cd146fa03ccce` | MAJORITY_AGREE | user_error:COUNTER_APPEAL_PENDING |
| 69 | cx-appeal-resolve | `0xf28a5e6e8982539cd18c43dbcd57ad0933987b4b8fb49ab0f392c0ad3c701aec` | MAJORITY_AGREE | return:66 bytes |
| 70 | repair | `0x20ef158f71d03dee661f31fad20e13cecb7547befcb0250fce05e9626d58f654` | MAJORITY_AGREE | return:1 bytes |
| 71 | s1-resubmit | `0xe9236c166fa96baff6ed14b2e31714e52e9b47b9ee595343aed7c6abec65a5ae` | MAJORITY_AGREE | return:66 bytes |
| 72 | s1-challenge-2 | `0xe7d427fff3547bb755f9f32b079ebd181fce38ac67ff33857bce6bfb1bb24f37` | MAJORITY_AGREE | return:1 bytes |
| 73 | s1-assess-2 | `0xc19cfbda762a8c8bad29b03c718ac8c536e5e4312d358400a085ccf63b04499f` | MAJORITY_AGREE | return:1 bytes |
| 74 | s1-appeal-2 | `0xd1f223f5e9065bb4c2fa2bbc553ed03e3926daba13707ca12e34573677d0b8c6` | MAJORITY_AGREE | return:1 bytes |
| 75 | s1-resolve-2 | `0xa0e9a346cecf35d7698e895857b071810cffd863b5075c0c667dda357e80652b` | MAJORITY_AGREE | return:66 bytes |
| 76 | s1-release-2 | `0x09916baa3008eaac76a639962c520b692f0edbcebed7cd680457ce5cd5e9b130` | MAJORITY_AGREE | return:66 bytes |
| 77 | s1-old-receipt | `0x270c92e3e31aede6cf64adaf207cbd7fed64b28b308108615391f94b03af1763` | MAJORITY_AGREE | user_error:ALREADY_RELEASED |
| 78 | s2-submit-after-recovery | `0xbf147a3bae707820d309a42609352b6cbf33b6070a1fbfd219c06e416ea56890` | MAJORITY_AGREE | return:66 bytes |
| 79 | s5-submit | `0xe7644bb1f883a38d859c970b29aca6e76b0854be7bc91d8d0f2dff4768b72569` | MAJORITY_AGREE | return:66 bytes |
| 80 | s6-submit | `0x643090c62b9b4c410c704a2d5b214835a4fc4725c9c0d610d40474bd41e9d0fe` | MAJORITY_AGREE | return:66 bytes |
| 81 | s6-challenge | `0x364c6c1036955d7cd7d0e36bdea385aa3f1b2506eb5616430a4d71bbc573db8c` | MAJORITY_AGREE | return:1 bytes |
| 82 | s6-assess | `0xc210f5a444a56a8fac2c44c53791fc93d91437b3d000e6ab8bebe31b49bcc89d` | MAJORITY_AGREE | return:1 bytes |
| 83 | s3-assess2-retry1 | `0x4c158d90f74bc73d14102a0dbc4868ebdde6b64854b961013cbf94f145309343` | MAJORITY_AGREE | return:1 bytes |
| 84 | expire-delivery-4 | `0x93c6c7d62e61566bbea6d465553de423ab1ab8c20cafced5a271b22eb4f3b155` | MAJORITY_AGREE | return:66 bytes |
| 85 | expire-delivery-4-again | `0xfa8dcb39438f5d39ca2f47a6da0563f2ba9da8e02161ce23f8b248ef43416194` | MAJORITY_AGREE | user_error:DELIVERY_NOT_EXPIRABLE |
| 86 | s3-appeal2b | `0xf7a621b8d40f9e38235be59589404b7921d2d55073ca7bd7a6469472949a24f0` | MAJORITY_AGREE | return:1 bytes |
| 87 | CKS-after-expiry | `0x6d105f2ad72e35ae050b0c2532a7789b21332ddf898d135d91a2f1080818c465` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 88 | t5-assess-early | `0x99f0b19d0d267aa76a2debfc83f53af43e4d62a55ce9f4d368da97f1a871f8d4` | MAJORITY_AGREE | user_error:REVIEW_WINDOW_OPEN |
| 89 | s3-resolve2b | `0xbbc696aba8618df973bec225fd3e504bdd3220b2fa53083735e12b07200138c9` | MAJORITY_AGREE | return:66 bytes |
| 90 | s3-release | `0xf473089e36c2be1ffade0b502004963dcfd50efade0e44f4628592961ded5ebb` | MAJORITY_AGREE | return:66 bytes |
| 91 | CA3-exec | `0x2e6305bcb4be1c7911f57b6752109148501bf44f87ccbaa3cb1991fbb76edcc6` | MAJORITY_AGREE | return:1 bytes |
| 92 | CA3-replay | `0xc528acec47fbfb37d0d723fb9c00840ecfb5883fd429cda1d137e2f7d6bad23f` | MAJORITY_AGREE | user_error:ALREADY_EXECUTED |
| 93 | CKL-consume-after-recovery | `0x75fb2a2939a98429f4075b680241ce8be421b6d6ef36ba5d688d09834e567f44` | MAJORITY_AGREE | return:1 bytes |
| 94 | CKL-over-cap | `0xd2d3960fa11e99264fdb0e21c8594d6ad0341aa881c250d076a7ff81c8385a3e` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
