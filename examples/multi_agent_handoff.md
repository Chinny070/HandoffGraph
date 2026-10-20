# Illustrative end-to-end workflow (not a live deployment)

**Agent A — produce a tested schema.** Criteria: schema validates exactly three data records and contains a reproducible test. Two mandatory checks: (1) 3 records conform; (2) test log shows successful parsing. Owner configures the stage and immutable requirement list. Worker submits commit-pinned `schema.json` with SHA-256 and adds a pinned `test_report.txt`. Independent validators assess both checks; no valid PASS is possible if either returns UNKNOWN/FAIL. Reviewer can challenge and worker may appeal the provisional verdict. A final PASS receives one release receipt.

**Agent B — import the dataset.** Stage B depends on Stage A. It cannot submit until A's receipt is finalized and released. B's delivery timer begins at actual A release, not at workflow creation.

**Counterexample:** After A's release, the reviewer discovers a reproducible parser failure and files a commit-pinned counterexample within seven days. HandoffGraph immediately quarantines Stage A and Stage B for *future actions*. An independent jury determines whether the new claim disproves acceptance. If sustained, the A worker can appeal within 24 hours or submit a repaired artifact as a fresh attempt; the old release remains in immutable history but is no longer executable. Dismissing or overturning the counterexample restores effective permission. No contract can undo a previous external import.

**Consumer demonstration:** An optional one-shot `HandoffConsumerExample` bound to A's root/ID/receipt performs a protected action only after final release. A more expressive `HandoffCapabilityConsumer` binds an action hash, operator, expiry and nonce replay restrictions. Neither consumer uses escrow or GEN transfers.
