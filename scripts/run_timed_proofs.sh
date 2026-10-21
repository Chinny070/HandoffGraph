#!/bin/bash
# Real-time deadline proofs on core 0x82B4D2f2b2DcD9590CE605095515891BAE2aFB25 (stages 5 and 6 of workflow 1).
# Stage 5: review window (12h) expiry -> permissionless assess without any challenge.
# Stage 6: appeal window (24h) expiry -> finalize_unappealed, then release.
export PYTHONUTF8=1
S='C:/Users/USERpc/AppData/Local/Temp/claude/C--Users-USERpc-Documents-HandoffGraph/f516de16-0c0f-4018-890c-d52b804b818f/scratchpad'
cd /c/Users/USERpc/Documents/HandoffGraph
CORE=0x82B4D2f2b2DcD9590CE605095515891BAE2aFB25; O=my-studionet-wallet
g() { "$S/gw.sh" "$@" | cut -f1,4,5,6; }
rd() { for i in 1 2 3 4 5; do o=$(genlayer call "$@" 2>&1); if ! echo "$o" | grep -qE "Error|error:"; then echo "$o" | grep -vE "genlayer-js|Calling|^$|Result|✔"; return; fi; sleep 10; done; echo READ_FAILED; }
waituntil() { while [ $(date +%s) -lt $1 ]; do sleep 60; done; }
D5=$(rd $CORE get_stage --args 5 | grep -oE "review_deadline: [0-9]+" | grep -oE "[0-9]+")
D6=$(rd $CORE get_stage --args 6 | grep -oE "appeal_deadline: [0-9]+" | grep -oE "[0-9]+")
echo "stage5 review_deadline=$D5 stage6 appeal_deadline=$D6 (started $(date -u +%FT%TZ))"
echo "--- before stage-5 deadline (must be rejected REVIEW_WINDOW_OPEN)"
g t5-assess-early $O $CORE assess 5
waituntil $((D5+30))
echo "--- stage 5 after review window: $(date -u +%FT%TZ)"
g t5-assess-after-window $O $CORE assess 5
rd $CORE get_stage --args 5 | grep -E "^\s+(state|ruling)"
echo "--- before stage-6 deadline (must be rejected APPEAL_WINDOW_OPEN)"
g t6-finalize-early $O $CORE finalize_unappealed 6
waituntil $((D6+30))
echo "--- stage 6 after appeal window: $(date -u +%FT%TZ)"
g t6-finalize $O $CORE finalize_unappealed 6
for i in $(seq 1 12); do rd $CORE get_stage --args 6 | grep -q "state: 6" && break; sleep 10; done
RC=$(rd $CORE get_stage --args 6 | grep -oE "receipt: '[0-9a-f]{64}'" | cut -d"'" -f2); echo RC6=$RC
g t6-release hg-reviewer $CORE release 6 $RC
rd $CORE is_release_active --args 6 $RC
echo TIMERS_DONE
