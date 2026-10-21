#!/bin/bash
# Shared helpers for live StudioNet runs. Source this file; do not execute it.
# Requires: genlayer CLI (0.39.x) logged in with the keystores named below, git, python, curl.
#
# Configuration (environment variables, no machine-specific defaults):
#   GL_OWNER_ACCOUNT / GL_WORKER_ACCOUNT / GL_REVIEWER_ACCOUNT   genlayer CLI keystore names
#   GL_WORKER_ADDR / GL_REVIEWER_ADDR / GL_OWNER_ADDR            their 0x addresses
#   GL_EVIDENCE_COMMIT   pushed commit that contains evidence/*.md (default: current HEAD)
#   GL_STATE_DIR         scratch state (default: <repo>/.live-state, git-ignored)
export PYTHONUTF8=1
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT" || exit 1
: "${GL_OWNER_ACCOUNT:?set GL_OWNER_ACCOUNT}" "${GL_WORKER_ACCOUNT:?set GL_WORKER_ACCOUNT}" "${GL_REVIEWER_ACCOUNT:?set GL_REVIEWER_ACCOUNT}"
: "${GL_OWNER_ADDR:?set GL_OWNER_ADDR}" "${GL_WORKER_ADDR:?set GL_WORKER_ADDR}" "${GL_REVIEWER_ADDR:?set GL_REVIEWER_ADDR}"
GL_STATE_DIR="${GL_STATE_DIR:-$ROOT/.live-state}"
GL_EVIDENCE_COMMIT="${GL_EVIDENCE_COMMIT:-$(git rev-parse HEAD)}"
mkdir -p "$GL_STATE_DIR" "$ROOT/proofs"
TXLOG="$ROOT/proofs/tx_log.tsv"
[ -f "$TXLOG" ] || printf "label\taccount\tmethod\ttx\tstatus\tconsensus\texecution\tnote\n" > "$TXLOG"

O="$GL_OWNER_ACCOUNT"; WK="$GL_WORKER_ACCOUNT"; RV="$GL_REVIEWER_ACCOUNT"
OP="$GL_OWNER_ADDR"; W="$GL_WORKER_ADDR"; R="$GL_REVIEWER_ADDR"
RULE='The published delivery report documents exactly three validated output records.'
EVIDENCE_BASE="https://raw.githubusercontent.com/Chinny070/HandoffGraph/$GL_EVIDENCE_COMMIT/evidence"
ev_hash() { git show "$GL_EVIDENCE_COMMIT:evidence/$1" | sha256sum | cut -d' ' -f1; }

# gw LABEL ACCOUNT CONTRACT METHOD [args...]
# Sends a write, waits for FINALIZED, logs it. Retries only transactions that never reached the
# chain or whose consensus did not apply them (MAJORITY_DISAGREE, NO_MAJORITY, timeouts).
# NOTE: the CLI reports FINALIZED even when consensus did not apply the call; the consensus column
# and `scripts/reconcile_tx_log.py` show the true outcome.
gw() {
  local label=$1 acct=$2 contract=$3 method=$4; shift 4
  local round attempt tx out rec st res ex
  for round in 1 2 3; do
    tx=""
    for attempt in 1 2 3 4 5; do
      genlayer account use "$acct" >/dev/null 2>&1
      if [ $# -gt 0 ]; then out=$(genlayer write "$contract" "$method" --args "$@" 2>&1); else out=$(genlayer write "$contract" "$method" 2>&1); fi
      tx=$(echo "$out" | grep -oE "tx_id: '0x[0-9a-fA-F]{64}'" | head -1 | grep -oE "0x[0-9a-fA-F]{64}")
      [ -z "$tx" ] && tx=$(echo "$out" | grep -oE "0x[0-9a-fA-F]{64}" | head -1)
      [ -n "$tx" ] && break
      sleep 10
    done
    st=""; rec=""
    for attempt in 1 2 3 4 5 6; do
      rec=$(genlayer receipt "$tx" --status FINALIZED 2>&1)
      st=$(echo "$rec" | grep -oE "status_name: '[A-Z_]+'" | tail -1 | cut -d"'" -f2)
      [ "$st" = "FINALIZED" ] && break
      sleep 15
    done
    res=$(echo "$rec" | grep -oE "result_name: '[A-Z_]+'" | tail -1 | cut -d"'" -f2)
    ex=$(echo "$rec" | grep -oE "execution_result: '[A-Z_]+'" | sort | uniq -c | tr -s ' ' | tr '\n' ',')
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t\n" "$label" "$acct" "$method" "$tx" "$st" "$res" "$ex" | tee -a "$TXLOG" | cut -f1,4,5,6
    case "$res" in
      MAJORITY_DISAGREE|NO_MAJORITY|UNDETERMINED|LEADER_TIMEOUT|VALIDATORS_TIMEOUT) echo "  (consensus did not apply the tx; retrying)"; sleep 5;;
      *) break;;
    esac
  done
}

# rd ARGS...   read-only call with retries; prints decoded result lines
rd() {
  local i o
  for i in 1 2 3 4 5 6; do
    o=$(genlayer call "$@" 2>&1)
    if ! echo "$o" | grep -qE "Error|error:"; then echo "$o" | grep -vE "genlayer-js|Calling|^$|Result|✔"; return; fi
    sleep 10
  done
  echo READ_FAILED
}

# fld CORE STAGE FIELD
fld() { rd "$1" get_stage --args "$2" | grep -E "^\s+$3:" | head -1 | sed -E "s/.*: '?([^',]*)'?,?/\1/"; }

# wait_state CORE STAGE STATE   (waits up to ~5 minutes for a stage state number)
wait_state() {
  local i
  for i in $(seq 1 30); do [ "$(fld "$1" "$2" state)" = "$3" ] && return 0; sleep 10; done
  echo "TIMEOUT waiting for stage $2 state $3 (is $(fld "$1" "$2" state))"; return 1
}

# dep CONTRACT_FILE ARGS...   deploys with the owner account; prints and stores the address in $GL_STATE_DIR/last_addr
dep() {
  local out h a
  genlayer account use "$O" >/dev/null 2>&1
  out=$(genlayer deploy --contract "$1" --args "${@:2}" 2>&1)
  h=$(echo "$out" | grep -oE "'Transaction Hash': '0x[0-9a-f]+'" | grep -oE "0x[0-9a-f]+")
  a=$(echo "$out" | grep -oE "'Contract Address': '0x[0-9a-fA-F]+'" | grep -oE "0x[0-9a-fA-F]+")
  printf "deploy\t%s\t%s\t%s\n" "$1" "$h" "$a" | tee -a "$TXLOG"
  echo "$a" > "$GL_STATE_DIR/last_addr"
}
