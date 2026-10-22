#!/bin/bash
# Full live lifecycle on a FRESH core (deploys one itself). Portable: no machine-specific paths.
# usage: GL_OWNER_ACCOUNT=.. GL_WORKER_ACCOUNT=.. GL_REVIEWER_ACCOUNT=.. \
#        GL_OWNER_ADDR=.. GL_WORKER_ADDR=.. GL_REVIEWER_ADDR=.. [GL_EVIDENCE_COMMIT=<pushed sha>] \
#        bash scripts/live/lifecycle.sh
# Stage ids assume a fresh core (ids start at 1). Follow with scripts/live/timed_proofs.sh and
# scripts/reconcile_tx_log.py. Everything is logged to proofs/tx_log.tsv.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
PASSH=$(ev_hash delivery_pass.md); FAILH=$(ev_hash delivery_fail.md)
CXH=$(ev_hash counter_defect.md); REPH=$(ev_hash delivery_repaired.md); SUPH=$(ev_hash support_audit.md)
B=$EVIDENCE_BASE
ZERO64=$(printf '0%.0s' $(seq 1 64))

echo "=== deploy core ($(date -u +%FT%TZ))"
if [ -z "$GL_CORE" ]; then dep contracts/handoff_graph.py; GL_CORE=$(cat "$GL_STATE_DIR/last_addr"); fi
CORE=$GL_CORE; echo "CORE=$CORE"; echo "$CORE" > "$GL_STATE_DIR/core"
python scripts/verify_source_parity.py "$CORE" contracts/handoff_graph.py HEAD | tail -1

echo "=== A. build and seal"
gw create "$O" "$CORE" create_workflow "HandoffGraph live" "Lifecycle verification"
gw st1 "$O" "$CORE" add_stage 1 Ingest "$W" "$R" "$RULE" 0 0 0
gw st2 "$O" "$CORE" add_stage 1 Transform "$W" "$R" "$RULE" 1 0 0
gw st3 "$O" "$CORE" add_stage 1 Audit "$W" "$R" "$RULE" 0 0 0
gw st4 "$O" "$CORE" add_stage 1 DeliveryTimer "$W" "$R" "$RULE" 0 0 0
gw st5 "$O" "$CORE" add_stage 1 ReviewTimer "$W" "$R" "$RULE" 0 0 0
gw st6 "$O" "$CORE" add_stage 1 AppealTimer "$W" "$R" "$RULE" 0 0 0
for s in 1 3; do
  gw req$s-a "$O" "$CORE" add_requirement $s "The report lists exactly three output records."
  gw req$s-b "$O" "$CORE" add_requirement $s "Every listed record has the validation result VALID."
done
gw timeout4 "$O" "$CORE" set_delivery_timeout 4 3600
gw seal "$O" "$CORE" seal_workflow 1
ROOT=$(rd "$CORE" get_workflow --args 1 | grep -oE "root: '[0-9a-f]{64}'" | cut -d"'" -f2); echo "ROOT=$ROOT"

echo "=== B. freeze / thaw"
gw freeze "$O" "$CORE" freeze 1
gw submit-while-frozen "$WK" "$CORE" submit 1 "Delivery report DR-100." "$B/delivery_pass.md" "$PASSH"
gw thaw "$O" "$CORE" thaw 1
gw freeze-by-nonowner "$WK" "$CORE" freeze 1

echo "=== C. stage 1: support evidence, PASS, freeze blocks release, release"
gw s1-submit "$WK" "$CORE" submit 1 "Delivery report DR-100 lists three records, all VALID." "$B/delivery_pass.md" "$PASSH"
gw s1-support-nonworker "$RV" "$CORE" attach_support 1 "$B/support_audit.md" "$SUPH" "audit"
gw s1-support "$WK" "$CORE" attach_support 1 "$B/support_audit.md" "$SUPH" "Independent audit AUD-100 confirms the three records."
gw s1-support-again "$WK" "$CORE" attach_support 1 "$B/support_audit.md" "$SUPH" "second"
gw s1-challenge "$RV" "$CORE" challenge 1 "Verify the report really contains three distinct VALID records."
gw s1-assess "$O" "$CORE" assess 1
gw s1-appeal-worker "$WK" "$CORE" appeal 1 "Requesting final adjudication."
gw s1-resolve "$O" "$CORE" resolve_appeal 1
wait_state "$CORE" 1 6 || exit 1
RC1=$(fld "$CORE" 1 receipt); echo "RC1=$RC1"
gw freeze2 "$O" "$CORE" freeze 1
gw release-while-frozen "$RV" "$CORE" release 1 "$RC1"
gw thaw2 "$O" "$CORE" thaw 1
gw s1-release "$RV" "$CORE" release 1 "$RC1"
gw s1-release-replay "$RV" "$CORE" release 1 "$RC1"

echo "=== D. stage 3 FAIL -> final FAIL -> retry -> repaired PASS -> release"
gw s3-submit "$WK" "$CORE" submit 3 "Delivery report DR-200 lists the produced records." "$B/delivery_fail.md" "$FAILH"
gw s3-challenge "$RV" "$CORE" challenge 3 "Verify the record count and validation results."
gw s3-assess "$O" "$CORE" assess 3
gw s3-appeal "$WK" "$CORE" appeal 3 "The report should be accepted as delivered."
gw s3-resolve "$O" "$CORE" resolve_appeal 3
wait_state "$CORE" 3 7 || exit 1
gw s3-release-failed "$RV" "$CORE" release 3 "$ZERO64"
gw s3-retry "$WK" "$CORE" retry_failed 3
gw s3-submit2 "$WK" "$CORE" submit 3 "Repair delivery DR-201 lists three records, all VALID." "$B/delivery_repaired.md" "$REPH"
gw s3-challenge2 "$RV" "$CORE" challenge 3 "Verify the repaired report independently."
for n in 1 2 3 4; do
  gw s3-assess2 "$O" "$CORE" assess 3
  [ "$(fld "$CORE" 3 state)" = "4" ] && break
done
gw s3-appeal2 "$WK" "$CORE" appeal 3 "Requesting final adjudication of the repaired delivery."
gw s3-resolve2 "$O" "$CORE" resolve_appeal 3
wait_state "$CORE" 3 6 || exit 1
RC3=$(fld "$CORE" 3 receipt); echo "RC3=$RC3"
gw s3-release "$RV" "$CORE" release 3 "$RC3"

echo "=== E. downstream stage 2 released against stage 1's first receipt"
gw s2-submit "$WK" "$CORE" submit 2 "Transform output built on the ingest delivery." "$B/delivery_pass.md" "$PASSH"
gw s2-challenge "$RV" "$CORE" challenge 2 "Verify independently."
gw s2-assess "$O" "$CORE" assess 2
gw s2-appeal "$WK" "$CORE" appeal 2 "Requesting final adjudication."
gw s2-resolve "$O" "$CORE" resolve_appeal 2
wait_state "$CORE" 2 6 || exit 1
RC2=$(fld "$CORE" 2 receipt); echo "RC2=$RC2"
gw s2-release "$RV" "$CORE" release 2 "$RC2"
echo "stage2 release active:"; rd "$CORE" is_release_active --args 2 "$RC2"

echo "=== F. consumers (accepted-state + finalized-state gates) and capabilities"
AH=$(echo -n "release-payment-batch-7" | sha256sum | cut -d' ' -f1)
EXP_SHORT=$(( $(date +%s) + 1500 )); EXP_LONG=$(( $(date +%s) + 86400 ))
dep contracts/handoff_consumer_example.py "$CORE" 1 1 "$ROOT" "$OP"; CA=$(cat "$GL_STATE_DIR/last_addr")
dep contracts/handoff_consumer_example.py "$CORE" 1 3 "$ROOT" "$OP"; CA3=$(cat "$GL_STATE_DIR/last_addr")
dep contracts/handoff_capability_consumer.py "$CORE" 1 1 "$ROOT" "$AH" "$OP" "$EXP_SHORT" 2; CKS=$(cat "$GL_STATE_DIR/last_addr")
dep contracts/handoff_capability_consumer.py "$CORE" 1 1 "$ROOT" "$AH" "$OP" "$EXP_LONG" 2; CKL=$(cat "$GL_STATE_DIR/last_addr")
echo "CA=$CA CA3=$CA3 CKS=$CKS (expires $EXP_SHORT) CKL=$CKL"; echo "$CA $CA3 $CKS $CKL" > "$GL_STATE_DIR/consumers"
echo "can_execute CA:"; rd "$CA" can_execute --args "$RC1"
gw CA-unauth "$WK" "$CA" execute_once "$RC1"
gw CA-wrong-receipt "$O" "$CA" execute_once "$ZERO64"
gw CA-exec "$O" "$CA" execute_once "$RC1"
gw CA-replay "$O" "$CA" execute_once "$RC1"
rd "$CA" get_status | grep -E "executed|action_count|finality|trustless"
gw CKS-consume-1 "$O" "$CKS" consume 1 "$AH" "$RC1"
gw CKS-replay-1 "$O" "$CKS" consume 1 "$AH" "$RC1"
gw CKS-wrong-action "$O" "$CKS" consume 2 "deadbeef$(echo "$AH" | cut -c9-)" "$RC1"
gw CKL-unauth "$WK" "$CKL" consume 1 "$AH" "$RC1"
gw CKL-consume-1 "$O" "$CKL" consume 1 "$AH" "$RC1"

echo "=== G. counterexample against stage 1 -> quarantine of stage 1 AND released descendant stage 2"
gw cx-open "$RV" "$CORE" open_counterexample 1 "Audit found REC-003 duplicates REC-001, contradicting three validated records." "$B/counter_defect.md" "$CXH"
rd "$CORE" is_release_active --args 1 "$RC1"
gw CKL-consume-during-cx "$O" "$CKL" consume 2 "$AH" "$RC1"
gw cx-resolve "$O" "$CORE" resolve_counterexample 1
rd "$CORE" get_counterexample --args 1 | grep -E "status|verdict"
echo "stage1 active / stage2 active (both must be false):"; rd "$CORE" is_release_active --args 1 "$RC1"; rd "$CORE" is_release_active --args 2 "$RC2"
gw CKL-consume-after-cx "$O" "$CKL" consume 2 "$AH" "$RC1"
CXSTATUS=$(rd "$CORE" get_counterexample --args 1 | grep -oE "status: [0-9]+" | grep -oE "[0-9]+")
if [ "$CXSTATUS" = "3" ]; then
  gw cx-appeal-outsider "$RV" "$CORE" appeal_counterexample 1 "not the worker"
  gw cx-appeal "$WK" "$CORE" appeal_counterexample 1 "The audit misread the table; REC-003 has a distinct payload."
  gw repair-while-appeal-pending "$WK" "$CORE" submit_repair 1 "cannot repair yet"
  gw cx-appeal-resolve "$O" "$CORE" resolve_counter_appeal 1
fi
CXSTATUS=$(rd "$CORE" get_counterexample --args 1 | grep -oE "status: [0-9]+" | grep -oE "[0-9]+")
echo "counterexample status after appeal: $CXSTATUS (6 overturned, 7 upheld)"

if [ "$CXSTATUS" = "7" ]; then
  echo "=== H. repair stage 1; descendant stage 2 must go stale and be re-validated"
  gw repair "$WK" "$CORE" submit_repair 1 "Replaced the duplicate REC-003 with a newly produced record."
  gw s1-resubmit "$WK" "$CORE" submit 1 "Repaired delivery DR-201 lists three distinct records, all VALID." "$B/delivery_repaired.md" "$REPH"
  gw s1-challenge-2 "$RV" "$CORE" challenge 1 "Verify the repaired report."
  for n in 1 2 3 4; do gw s1-assess-2 "$O" "$CORE" assess 1; [ "$(fld "$CORE" 1 state)" = "4" ] && break; done
  gw s1-appeal-2 "$WK" "$CORE" appeal 1 "Requesting final adjudication."
  gw s1-resolve-2 "$O" "$CORE" resolve_appeal 1
  wait_state "$CORE" 1 6
  RC1B=$(fld "$CORE" 1 receipt); echo "RC1B=$RC1B"
  gw s1-release-2 "$RV" "$CORE" release 1 "$RC1B"
  echo "stage1 old/new receipt active:"; rd "$CORE" is_release_active --args 1 "$RC1"; rd "$CORE" is_release_active --args 1 "$RC1B"
  echo "stage2 prerequisites_current / release active (both must be false: bound to the OLD parent receipt):"
  rd "$CORE" get_stage --args 2 | grep -E "prerequisites_current|parent_digest"; rd "$CORE" is_release_active --args 2 "$RC2"
  gw s2-release-stale "$RV" "$CORE" release 2 "$RC2"
  gw s2-invalidate "$O" "$CORE" invalidate_stale 2
  gw s2-invalidate-again "$O" "$CORE" invalidate_stale 2
  gw s2-repair "$WK" "$CORE" submit_repair 2 "Re-validated against the repaired upstream receipt."
  gw s2-resubmit "$WK" "$CORE" submit 2 "Transform output rebuilt on the repaired ingest." "$B/delivery_pass.md" "$PASSH"
  gw s2-challenge-2 "$RV" "$CORE" challenge 2 "Verify independently."
  for n in 1 2 3 4; do gw s2-assess-2 "$O" "$CORE" assess 2; [ "$(fld "$CORE" 2 state)" = "4" ] && break; done
  gw s2-appeal-2 "$WK" "$CORE" appeal 2 "Requesting final adjudication."
  gw s2-resolve-2 "$O" "$CORE" resolve_appeal 2
  wait_state "$CORE" 2 6
  RC2B=$(fld "$CORE" 2 receipt); echo "RC2B=$RC2B"
  gw s2-release-2 "$RV" "$CORE" release 2 "$RC2B"
  echo "stage2 old/new receipt active:"; rd "$CORE" is_release_active --args 2 "$RC2"; rd "$CORE" is_release_active --args 2 "$RC2B"
  gw CKL-consume-after-recovery "$O" "$CKL" consume 2 "$AH" "$RC1B"
  gw CKL-over-cap "$O" "$CKL" consume 3 "$AH" "$RC1B"
fi
echo "stage3 consumer after repaired release:"; rd "$CA3" can_execute --args "$RC3"
gw CA3-exec "$O" "$CA3" execute_once "$RC3"
gw CA3-replay "$O" "$CA3" execute_once "$RC3"

echo "=== I. start real-time timers (finish with scripts/live/timed_proofs.sh)"
gw s5-submit "$WK" "$CORE" submit 5 "Delivery report DR-100 lists three records, all VALID." "$B/delivery_pass.md" "$PASSH"
gw s6-submit "$WK" "$CORE" submit 6 "Delivery report DR-100 lists three records, all VALID." "$B/delivery_pass.md" "$PASSH"
gw s6-challenge "$RV" "$CORE" challenge 6 "Verify independently."
gw s6-assess "$O" "$CORE" assess 6
echo "stage4 delivery deadline / stage5 review deadline / stage6 appeal deadline:"
rd "$CORE" get_stage --args 4 | grep -E "delivery_deadline"; rd "$CORE" get_stage --args 5 | grep -E "review_deadline"; rd "$CORE" get_stage --args 6 | grep -E "appeal_deadline"
echo "After the 1 h delivery deadline: gw expire-delivery-4 \$O \$GL_CORE expire_delivery 4 (see LIVE_PROOFS.md)"
echo "After the 25 min capability expiry: consume with CKS and the current stage-1 receipt must be rejected."
echo LIFECYCLE_DONE
