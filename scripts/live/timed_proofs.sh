#!/bin/bash
# Real-time deadline proofs for a workflow created by scripts/live/lifecycle.sh.
#   stage 5: review-window (12 h) expiry -> permissionless assess with no challenge
#   stage 6: appeal-window (24 h) expiry -> finalize_unappealed, then release
# usage: GL_CORE=0x... [GL_*...] bash scripts/live/timed_proofs.sh
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
: "${GL_CORE:?set GL_CORE to the core address}"
CORE=$GL_CORE
waituntil() { while [ "$(date +%s)" -lt "$1" ]; do sleep 60; done; }
D5=$(rd "$CORE" get_stage --args 5 | grep -oE "review_deadline: [0-9]+" | grep -oE "[0-9]+")
D6=$(rd "$CORE" get_stage --args 6 | grep -oE "appeal_deadline: [0-9]+" | grep -oE "[0-9]+")
echo "stage5 review_deadline=$D5 stage6 appeal_deadline=$D6 (started $(date -u +%FT%TZ))"
echo "--- stage 5 assess before the review window closes (must be rejected REVIEW_WINDOW_OPEN)"
gw t5-assess-early "$O" "$CORE" assess 5
waituntil $((D5 + 30))
echo "--- stage 5 after the review window: $(date -u +%FT%TZ)"
gw t5-assess-after-window "$O" "$CORE" assess 5
rd "$CORE" get_stage --args 5 | grep -E "^\s+(state|ruling)"
echo "--- stage 6 finalize_unappealed inside the appeal window (must be rejected APPEAL_WINDOW_OPEN)"
gw t6-finalize-early "$O" "$CORE" finalize_unappealed 6
waituntil $((D6 + 30))
echo "--- stage 6 after the appeal window: $(date -u +%FT%TZ)"
gw t6-finalize "$O" "$CORE" finalize_unappealed 6
wait_state "$CORE" 6 6
RC=$(fld "$CORE" 6 receipt); echo "RC6=$RC"
gw t6-release "$RV" "$CORE" release 6 "$RC"
rd "$CORE" is_release_active --args 6 "$RC"
echo TIMERS_DONE
