#!/bin/bash
# Proofs that need only wall-clock time to pass after scripts/live/lifecycle.sh:
#   - stage 4 delivery deadline (1 h) -> permissionless expire_delivery
#   - 25-minute capability -> refused after expiry even though the stage release is still active
# usage: same GL_* variables as lifecycle.sh, plus GL_CORE=<core address from the lifecycle run>
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
: "${GL_CORE:?set GL_CORE}"
CORE=$GL_CORE
read -r CA CA3 CKS CKL < "$GL_STATE_DIR/consumers"
AH=$(echo -n "release-payment-batch-7" | sha256sum | cut -d' ' -f1)
echo "now=$(date +%s)"; rd "$CORE" get_stage --args 4 | grep -E "^\s+(state|delivery_deadline)"
gw expire-delivery-4 "$O" "$CORE" expire_delivery 4
rd "$CORE" get_stage --args 4 | grep -E "^\s+(state|ruling|revocation_hash)"
gw expire-delivery-4-again "$O" "$CORE" expire_delivery 4
RC1=$(fld "$CORE" 1 receipt)
echo "stage 1 release still active:"; rd "$CORE" is_release_active --args 1 "$RC1"
echo "short capability view (expired):"; rd "$CKS" can_consume --args 2 "$AH" "$RC1"
gw CKS-after-expiry "$O" "$CKS" consume 2 "$AH" "$RC1"
rd "$CKS" get_status | grep -E "use_count|expires_at"
echo POST_DEADLINES_DONE
