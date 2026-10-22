# Core v5 run — every transaction (auto-generated from `proofs/tx_reconciled.tsv`)

Core `0x9629E19c11Ab40d9848575A8E699E1d48DBDA209`; produced by `scripts/live/lifecycle.sh` and `scripts/live/post_deadlines.sh`. Outcome is the leader receipt result decoded from chain: `return` = success, `user_error:X` = deliberate contract rejection.

| # | label | tx | consensus | outcome |
|---|---|---|---|---|
| 1 | deploy | `0x16c2c2aceb879e367ef3b77629c694e2ad794ac048b51ae6129b98e03425de00` | MAJORITY_AGREE | return:1 bytes |
| 2 | create | `0xf779efeab8b39ade1441634daee8d26a5158f3796d1eea097230828040de269c` | MAJORITY_AGREE | return:1 bytes |
| 3 | st1 | `0x3823732fc73962588cf4580327eb8f11be035942a5921e8a9df8d95e7220660c` | MAJORITY_AGREE | return:1 bytes |
| 4 | st2 | `0xf51ce6724d7f8c6ba9c96d995ca29d3392edbedb14f711cab1de769c61689e19` | MAJORITY_AGREE | return:1 bytes |
| 5 | st3 | `0xa4175057a8337e98d792ae62037df30aa4c629a197bbb9bf7040bb0580025ec4` | MAJORITY_AGREE | return:1 bytes |
| 6 | st4 | `0xfccd675378e76bee5dfaf5068bac10e647ba10ad7e5e0f786e8e89b92ba0a658` | MAJORITY_AGREE | return:1 bytes |
| 7 | st5 | `0x4a4c20720d74d73a4dd33e72066788350ca8faa830efae47487b80eb29168c9f` | MAJORITY_AGREE | return:1 bytes |
| 8 | st6 | `0x955e922f3f5387540091f6a1c996e9c73542c39b4754b48726e0ea730cdc0e94` | MAJORITY_AGREE | return:1 bytes |
| 9 | req1-a | `0xf89d9ca6c22bba1ef80ab1feb2b261791a20d9a11eca4629784de06fd20f1148` | MAJORITY_AGREE | return:1 bytes |
| 10 | req1-b | `0x29a1de4ce245ec72f4a474b3e360952c8f8ea0820e031088a061964b44d160c6` | MAJORITY_AGREE | return:1 bytes |
| 11 | req3-a | `0x15b0194c10913c73a71785d4aa855e09f2ea01cbd3af0e6656c9135813aefc1a` | MAJORITY_AGREE | return:1 bytes |
| 12 | req3-b | `0xac68e41e0bb9cce6fd633bcf41955f004b10b3afc70e224772c4c17a4a9e5aea` | MAJORITY_AGREE | return:1 bytes |
| 13 | timeout4 | `0x77c9c7bdc51247b9540e8ff782073e46c064ab8deacb8637378a86fa78f74651` | MAJORITY_AGREE | return:1 bytes |
| 14 | seal | `0xb1a6dcacdbc174e5790df6dda83b7a2bdf6045f4751cd4075cfd808c1482268f` | MAJORITY_AGREE | return:66 bytes |
| 15 | freeze | `0x83ff620f3e8ee0f3cd6a41562daf1ea2cfa84d089028ad338121b952c6125d73` | MAJORITY_AGREE | return:1 bytes |
| 16 | submit-while-frozen | `0x0cd862f03d32736e8a1b2d343d2c8c0d2f2f87dfd0cec3367f48f7e0f59e21a5` | MAJORITY_AGREE | user_error:WORKFLOW_FROZEN |
| 17 | thaw | `0x4b03c74016e4a6041bb72d67741d3824b8f4fa5d2bae70daa357b513d2b742d6` | MAJORITY_AGREE | return:1 bytes |
| 18 | freeze-by-nonowner | `0x00ec73c9851d3bcd59260e87b5581f0f299ddc82858e52a273f365a3041574cd` | MAJORITY_AGREE | user_error:ONLY_OWNER |
| 19 | s1-submit | `0x12e7eec1e9a331403d36f81d66c3d69cf92f13c095dca1f80bd7471e2ed4603f` | MAJORITY_AGREE | return:66 bytes |
| 20 | s1-support-nonworker | `0x4a47b9a2bab26e86e3ccc5583290679b112fafb95871913d3cd23b0f8c2740a9` | MAJORITY_AGREE | user_error:ONLY_WORKER |
| 21 | s1-support | `0x0e9375768a02f68326311ee67b90201c9f20253fe6e5adfa5fe106a6df71f568` | MAJORITY_AGREE | return:1 bytes |
| 22 | s1-support-again | `0xe09f02c05d101f357ec563d233e65d2966ae090cc05992b43ad69de3b66473fe` | MAJORITY_AGREE | user_error:SUPPORT_NOT_OPEN |
| 23 | s1-challenge | `0x0688dc6977fe0ec32488ff8142d994fbd8af1382638c43fbad3249105c083c7b` | MAJORITY_AGREE | return:1 bytes |
| 24 | s1-assess | `0x28ab69ae96d93423ea362b8ff24e43a99adb3b7fcf07913b78f3c1fffd156db6` | MAJORITY_AGREE | return:1 bytes |
| 25 | s1-appeal-worker | `0x718888f448c71d582625c5361776d22955d018587f6ef03a2d33e5fd1f739f7e` | MAJORITY_AGREE | return:1 bytes |
| 26 | s1-resolve | `0xff40af1a1a921907b66b7917a2cbcf85342c408f172b66c1c20913d64773e5c7` | MAJORITY_AGREE | return:66 bytes |
| 27 | freeze2 | `0xd6fda2d3f7d5fe1a4360f1c5d13a0caf76cce689ce8bc6b73bb73b5e4c98e941` | MAJORITY_AGREE | return:1 bytes |
| 28 | release-while-frozen | `0xe25d6f07c667c72b4c3bc27577d2d901a4afa47f73e47f6d17f6e4687b7407ca` | MAJORITY_AGREE | user_error:WORKFLOW_FROZEN |
| 29 | thaw2 | `0x74bcec0b332f14a50ac6e77e6e6ce28ee58ef3099542ac9fff3d7270d6356dba` | MAJORITY_AGREE | return:1 bytes |
| 30 | s1-release | `0x749764c0fa80ed18b07fbed9639f6d9bd990b00b33fa25d8ea3f5290c989e0b5` | MAJORITY_AGREE | return:66 bytes |
| 31 | s1-release-replay | `0xc3cea0058d9604ef541335df2b3b84fdf8c4ccc97af927e5b062b0959ec64e71` | MAJORITY_AGREE | user_error:ALREADY_RELEASED |
| 32 | s3-submit | `0x663698812ba45fdd9c24b472366cd966cdab1194cec1baf3c7dd71c6b9866461` | MAJORITY_AGREE | return:66 bytes |
| 33 | s3-challenge | `0x262928990d4954ccb768534123b9198170445c56f5b28180510752e99286bc01` | MAJORITY_AGREE | return:1 bytes |
| 34 | s3-assess | `0x8031d84089745075707c17594260d94b0dc201941256027c98d3b66f95ffe1b6` | MAJORITY_AGREE | return:1 bytes |
| 35 | s3-appeal | `0x2b89d41707abef3b9739879d2702be458d3eb7d9124a448a86ecd0e52481f4df` | MAJORITY_AGREE | return:1 bytes |
| 36 | s3-resolve | `0xcca40e86d7ed89723dc7ee39d643b4f4662a556004dd130be5e640d907d90bd5` | MAJORITY_AGREE | return:66 bytes |
| 37 | s3-release-failed | `0xa2133474536c66b836b5c51a207758924c1ea0720513fba227be6aa871f01fc7` | MAJORITY_AGREE | user_error:NOT_FINAL_PASS |
| 38 | s3-retry | `0xfd7563fe4007b7d3c4a9795d8e249d6f8e3a0d6b2109c0af07669bec7e66659d` | MAJORITY_AGREE | return:1 bytes |
| 39 | s3-submit2 | `0x83befb7e3e39c12fd2ad3c2a6ed6f8fd011ec2ac69c09a5f8f6c5543da6a76c3` | MAJORITY_AGREE | return:66 bytes |
| 40 | s3-challenge2 | `0x203ddd8f5b832ca00d2dfc28e1bb18d8127e29eec814303c23f6e1557caf0fe2` | MAJORITY_AGREE | return:1 bytes |
| 41 | s3-assess2 | `0xfacc7b612229200ddeff5897295a055065857d33ddf1fa912d4088152ac56ade` | MAJORITY_AGREE | return:1 bytes |
| 42 | s3-appeal2 | `0x1054b873f5374e3c9eddafe2ceac8a3e944854e0a3d9ea8139839083aa061a84` | MAJORITY_AGREE | return:1 bytes |
| 43 | s3-resolve2 | `0xe0a04d4ae814dcb9d779fb5ffca4e5d7109fe1a2bc4e7a89d811a0c1714420d3` | MAJORITY_AGREE | return:66 bytes |
| 44 | s3-release | `0xac95435592d80209784c817f4ac1ce7e693552f682f7da85ead4f23e99b503f1` | MAJORITY_AGREE | return:66 bytes |
| 45 | s2-submit | `0x621d107d8bac748c270f13583deb782a715511e110a1bd11a4e934319debfd90` | MAJORITY_AGREE | return:66 bytes |
| 46 | s2-challenge | `0xe2755f59d3c8d696bc6295a1ebcbe12ebbe218548b6fb805aa43d3357813708d` | MAJORITY_AGREE | return:1 bytes |
| 47 | s2-assess | `0xd1c4041ff808f279af4248e34f487b00b258dde8141b5d31e5144148a0dfae12` | MAJORITY_AGREE | return:1 bytes |
| 48 | s2-appeal | `0x65b2db231f95e4ec9ffea724cf38fd7a89fa1f4d3d0bebbd1c4261e751e57e80` | MAJORITY_AGREE | return:1 bytes |
| 49 | s2-resolve | `0x49e13170ce98e7698da5a9f5875c9ff7bd9a0bf6022b126e0aa711dcfd23de2b` | MAJORITY_AGREE | return:66 bytes |
| 50 | s2-release | `0x6af64ca3180d08e13b5b2d4b4271d842ce880c5357809917102b91a0dd5507db` | MAJORITY_AGREE | return:66 bytes |
| 51 | deploy | `0x4f064d17dfeb1d1e275d167ade69bfdd662d2a3f598be522c83973b0a1394347` | MAJORITY_AGREE | return:1 bytes |
| 52 | deploy | `0x859a0c14c7da428ffd33206824ef4495965821d987afd4bcef02adb8da3732b5` | MAJORITY_AGREE | return:1 bytes |
| 53 | deploy | `0xe17939fa438e7263fd7d0bdc0142d120df1f1bfc35c0034f0edfe466efa78ddc` | MAJORITY_AGREE | return:1 bytes |
| 54 | deploy | `0x13aa1a4c5d00690d4cab29fd935f35ce5a265aab283fe311689a71d88451eb51` | MAJORITY_AGREE | return:1 bytes |
| 55 | CA-unauth | `0x4f430608de542dbd32a43eb7ed8e36461b6bc0c7a34ec8ae36a057425c8358a7` | MAJORITY_AGREE | user_error:ONLY_OPERATOR |
| 56 | CA-wrong-receipt | `0x8ea86fbf379d1afa60f35f366cd2c02f3d253a2fe6dffe86fc54ba49905358e5` | MAJORITY_AGREE | user_error:HANDOFF_NOT_RELEASED |
| 57 | CA-exec | `0x9e2f7ed8bfad809f6828fba1ad3292f5e2ebbc160ae841f6c1456c7cf8cbcceb` | MAJORITY_AGREE | return:1 bytes |
| 58 | CA-replay | `0xdcc3ff425e3d9f782da678309ed62647da02a927cf66000956e3af39e7810056` | MAJORITY_AGREE | user_error:ALREADY_EXECUTED |
| 59 | CKS-consume-1 | `0x13ff5f0b3a1986ba8ba7ffbe20574342820889527fc72dae170d62eac099f436` | MAJORITY_AGREE | return:1 bytes |
| 60 | CKS-replay-1 | `0x5e218133325f95401abcce24f42dfe965a75e2d8cb35d00850bc799cda0093b9` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 61 | CKS-wrong-action | `0x60ca8e69b1eb1dd7fe449f420dc1c78d78fde42dfb4441a316cb70e26e4ded10` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 62 | CKL-unauth | `0xbb252190a23574dcac6d8c04fe120f62b592fe5afee65500b2bd8196767cba4c` | MAJORITY_AGREE | user_error:ONLY_OPERATOR |
| 63 | CKL-consume-1 | `0xe9b25cf2cf17800d23873729857d559d2a89c08a57aada7fd51321c8c8c286ca` | MAJORITY_AGREE | return:1 bytes |
| 64 | cx-open | `0x2d09a708d69fc14fdab35e6f36d2113f7bdeec878e90680e444ed699ba34e2b5` | MAJORITY_AGREE | return:1 bytes |
| 65 | CKL-consume-during-cx | `0x561c5b95a32bac1544886fe9b562013a1642f2506f9ddf4dfe1b2d1dadcf138b` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 66 | cx-resolve | `0x9d575215b64fec5f77e5bf63d898710034a8a19a40d3ecd0a25f84ba9d4474d4` | MAJORITY_AGREE | return:66 bytes |
| 67 | CKL-consume-after-cx | `0xb60a68328a6414b5af3503b8510de5948b9f36d9d99e66ff0a95fe255127c40a` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 68 | cx-appeal-outsider | `0x291d2693231434403bcd6daf4c6f491afce6d2cd48bdc122a5a4d57a6a1bd917` | MAJORITY_AGREE | user_error:ONLY_WORKER |
| 69 | cx-appeal | `0x350f373b67559f297b3bdeb160426f093058460f9aa21b632b5534d1417bc40d` | MAJORITY_AGREE | return:1 bytes |
| 70 | repair-while-appeal-pending | `0x47b19a2d32011391cda164605b296a4ba0d6ee0ddb1fdca0a621f9da597ffc88` | MAJORITY_AGREE | user_error:COUNTER_APPEAL_PENDING |
| 71 | cx-appeal-resolve | `0x49618d460b73ef6d3faabffb488f4e259968505545b2f840c9dbf56f78b5a08c` | MAJORITY_AGREE | return:66 bytes |
| 72 | repair | `0x611356f34dbd036383f01c0a25c1a38369c65a6a2b579d898665f97e59267508` | MAJORITY_AGREE | return:1 bytes |
| 73 | s1-resubmit | `0xeab93294ed487de48cba385225df06fac6dd5e4af00dfe866f4a8befc3d9e570` | MAJORITY_AGREE | return:66 bytes |
| 74 | s1-challenge-2 | `0xacc4cdd9e59da5df2e1da95c5e2caeb07372502ea449c3cfb66f56ed8f6a6fa5` | MAJORITY_AGREE | return:1 bytes |
| 75 | s1-assess-2 | `0xf1ad10ce08811a0f4b0615335eecb2ad32b2c7e8f7345788cde9a6aa080029e8` | MAJORITY_AGREE | return:1 bytes |
| 76 | s1-appeal-2 | `0xe9fb88519504d61f2d24d901c153f2f5d52274a2bd8877dc90b4d3035588b6e0` | MAJORITY_AGREE | return:1 bytes |
| 77 | s1-resolve-2 | `0x40914d432b9668a9416a125c785beede8fb1d6e1a5addabc914b9a1c9d50dec2` | MAJORITY_AGREE | return:66 bytes |
| 78 | s1-release-2 | `0x99a02b81a2d2cf0e7b675b5bf3c87c168e96cadb638f87d4932a721834f9f3d9` | MAJORITY_AGREE | return:66 bytes |
| 79 | s2-release-stale | `0xe68a592b629ad75616fec55af0ff9b3c9b84298cd69a6bd1ce1a29f92b2680d0` | MAJORITY_AGREE | user_error:STALE_PREREQUISITE |
| 80 | s2-invalidate | `0xdd768fe9ca4b54ad11a54ec5060a69fd4ee3b21a4291d91ffea7c524fd6fa0d9` | MAJORITY_AGREE | return:66 bytes |
| 81 | s2-invalidate-again | `0x0e76d6c3f31b28a82f337e31085982e054c0ae2fbb0767e8e69db0389d407bd0` | MAJORITY_AGREE | user_error:NOT_INVALIDATABLE |
| 82 | s2-repair | `0xfc4f84da66a5360b9bef8aa0f8b8585bb222d185c4adb01866a770b9d77b6451` | MAJORITY_AGREE | return:1 bytes |
| 83 | s2-resubmit | `0x14b8d3e951a5e30d8cbd4ce53119ffd9f564b02e30c0e5174077b49fb8f6f00a` | MAJORITY_AGREE | return:66 bytes |
| 84 | s2-challenge-2 | `0xcbe14596b84ab40816e4e62232f70985fd2ab73448476c5687a3ff1bc7e891d0` | MAJORITY_AGREE | return:1 bytes |
| 85 | s2-assess-2 | `0x42a82e4ec3b1410e42fbb18fcf04a3d9a6c42384ccc7634e31dcbaa19974d31d` | MAJORITY_AGREE | return:1 bytes |
| 86 | s2-appeal-2 | `0x2349fad0b377b93dd2290162b0390cb13852d02492c35f1565e5ad00b3b00048` | MAJORITY_AGREE | return:1 bytes |
| 87 | s2-resolve-2 | `0xb2660ac230ce50bd2990c29ebc7767ed6ed092fc9ddf989527af1d291d5eb5c9` | MAJORITY_AGREE | return:66 bytes |
| 88 | s2-release-2 | `0x26ace4a1bcf1974d8db3b11b56132feefe52cbf2a76a5227323e99b104ee6eab` | MAJORITY_AGREE | return:66 bytes |
| 89 | CKL-consume-after-recovery | `0xedbec3285e7cc2df676a1b9e0bd06d58daf9f05418a5c0b060242aaf71e287e7` | MAJORITY_AGREE | return:1 bytes |
| 90 | CKL-over-cap | `0xbb20cafcc716f926faf8284dd8901544180068fd824ca15c6af0cff4c48ea7f7` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
| 91 | CA3-exec | `0x9740754bf6714f7d80cb7c6122ec9c2b6d68e18906733c06d71aac6c1c96263d` | MAJORITY_AGREE | return:1 bytes |
| 92 | CA3-replay | `0xde94a863d54fd08089bf0830d91d84bc4ece110f9807d83729101f27c8ed0451` | MAJORITY_AGREE | user_error:ALREADY_EXECUTED |
| 93 | s5-submit | `0xf9b2d69145a144ef4cdbd15707471916cd4786eab4b131fb4adc91031d702ef8` | MAJORITY_AGREE | return:66 bytes |
| 94 | s6-submit | `0x9db98b03d86a1b5f9659e41bb2bf9776b6d1d5f3a850d97c7afe9f7642fe3de2` | MAJORITY_AGREE | return:66 bytes |
| 95 | s6-challenge | `0x51886115f1016643b4c937012f96cd12453d5e3fffaf029c2505f49e8b617e44` | MAJORITY_AGREE | return:1 bytes |
| 96 | s6-assess | `0xe3cb62a42bb3dfc1a753e3ccac7d68236ef656708c44d0f1340146533f27ba02` | MAJORITY_AGREE | return:1 bytes |
| 97 | expire-delivery-4 | `0xfa53fc958f56c5022914fbb8735cd29527e02812072df3b2aa6b3715197a243e` | MAJORITY_AGREE | return:66 bytes |
| 98 | expire-delivery-4-again | `0x365fb6bdce397b3935695f8ae04e40987621e02609224da92ba7a4c373834e1d` | MAJORITY_AGREE | user_error:DELIVERY_NOT_EXPIRABLE |
| 99 | CKS-after-expiry | `0x51f758fda714ff37aca548311e1c295d6583aee17153c078cadd95f570760c36` | MAJORITY_AGREE | user_error:CAPABILITY_INVALID |
