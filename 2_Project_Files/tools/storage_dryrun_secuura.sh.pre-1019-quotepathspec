#!/bin/bash
# storage_dryrun_secuura.sh -- WED-154 dry-run: which old Secuura/Blockchain (Platform K) storage is "not needed".
#
# READ-ONLY. Prints every candidate path per class with size, age and a verdict (CANDIDATE / KEEP and why), plus
# totals, and writes a dated markdown report. It performs NO removal, move or rename: it only measures.
# Whoever acts on the report is the project's own seat, under Kam's word (hard rule 1; learnings 2026-08-26,
# 2026-09-29, 2026-10-07, 2026-10-15).
#
# Classes (names follow 1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md where they exist):
#   W  working copy (policy class 1): worktrees/*, deploy-clones/*  merged + tidy + idle >= OLD_DAYS
#   N  regenerable node_modules (policy class 2) inside working copies that W kept, idle >= REGEN_DAYS
#   T  test artefacts (coverage, test-results, playwright-report, allure-*, .nyc_output) idle >= REGEN_DAYS
#   P  scratchpad/ (seat scratch): scratch clones + node_modules only; unclassified folders listed as KEEP
#   E  5_Project_History evidence folders: regenerable subtrees only (node_modules, scratch clones); the rest is a RECORD
#   R  local-model runs/: scratch clones + caches inside a run (record files stay)
#   S  local-model spark/cache/work/*: prune_work.py's four guards, checked read-only
#   H  local-model hosted/work/*
# NEVER candidates: 2_Project_Files (main checkout), 1_Project_Definition, 3_Access_Keys, 4_Credentials, history.md,
# HANDOVER files, anything dirty / unmerged, anything a live process holds, anything modified in the last LIVE_HOURS.
#
# usage: storage_dryrun_secuura.sh [--root DIR] [--lm DIR] [--report-dir DIR] [--date YYYY-MM-DD] [--now EPOCH]
#                                  [--live-hours 48] [--old-days 7] [--regen-days 14] [--jobs 6] [--self-check-only]
# bash 3.2 compatible; no directory changes (absolute paths only); stderr is never discarded.

SELF="${BASH_SOURCE[0]:-$0}"

# ---- self-check: refuse to run if this very file contains a removal/move/rename verb -------------------------
# The patterns are assembled from fragments so this block does not trip itself.
self_check() {
  local f="$1" bad="" p
  local V1='r''m' V2='r''mdir' V3='m''v' V4='un''link' V5='sh''red'
  local W1='rem''ove' W2='pru''ne' D1='dele''te' C1='cle''an'
  # token verbs at a command position
  p="(^|[;&|(\`[:space:]])($V1|$V2|$V3|$V4|$V5)([[:space:]]|\$)"
  if grep -E -n "$p" "$f" | grep -v '^[0-9]*:[[:space:]]*#' > /dev/null; then bad="$bad token-verb"; fi
  # git verbs that write
  if grep -E -n "worktree[[:space:]]+($W1|$W2)" "$f" | grep -v '^[0-9]*:[[:space:]]*#' > /dev/null; then bad="$bad worktree-$W1/$W2"; fi
  if grep -E -n "git[^#]*[[:space:]]$C1([[:space:]]|\$)" "$f" | grep -v '^[0-9]*:[[:space:]]*#' > /dev/null; then bad="$bad git-$C1"; fi
  if grep -E -n -e "-$D1([[:space:]]|\$)" -e "--$D1" "$f" | grep -v '^[0-9]*:[[:space:]]*#' > /dev/null; then bad="$bad $D1-flag"; fi
  if [ -n "$bad" ]; then
    echo "SELF-CHECK FAILED: $f contains a forbidden removal/move/rename verb ($bad). Refusing to run." >&2
    return 1
  fi
  echo "self-check: no removal/move/rename verb found in $f" >&2
  return 0
}

# ---- defaults ---------------------------------------------------------------------------------------------
ROOT=/Volumes/DevMASTER/\!CODING/Secuura/Blockchain
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
REPORT_DIR=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_storage-policy
DATE=""
NOW=""
LIVE_HOURS=48
OLD_DAYS=7
REGEN_DAYS=14
JOBS=6
PROBE_ONLY=""
CHECK_ONLY=""

while [ $# -gt 0 ]; do
  case "$1" in
    --root) ROOT="$2"; shift 2;;
    --lm) LM="$2"; shift 2;;
    --report-dir) REPORT_DIR="$2"; shift 2;;
    --date) DATE="$2"; shift 2;;
    --now) NOW="$2"; shift 2;;
    --live-hours) LIVE_HOURS="$2"; shift 2;;
    --old-days) OLD_DAYS="$2"; shift 2;;
    --regen-days) REGEN_DAYS="$2"; shift 2;;
    --jobs) JOBS="$2"; shift 2;;
    --self-check-only) CHECK_ONLY=1; shift;;
    --probe) PROBE_ONLY="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 64;;
  esac
done

# ---- probe mode (called via xargs, read-only): one TSV line per working copy ------------------------------
if [ -n "$PROBE_ONLY" ]; then
  export GIT_OPTIONAL_LOCKS=0
  P="$PROBE_ONLY"
  if [ ! -e "$P/.git" ]; then printf '%s\tNOTGIT\t\t0\t0\tnodev\t0\t0\t0\t0\n' "$P"; exit 0; fi
  br=$(git -C "$P" symbolic-ref -q --short HEAD 2>/dev/null); [ -z "$br" ] && br="(detached)"
  hd=$(git -C "$P" rev-parse HEAD 2>/dev/null)
  ct=$(git -C "$P" log -1 --format=%ct 2>/dev/null)
  dirty=$(git -C "$P" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  m=nodev
  if git -C "$P" rev-parse --verify -q origin/develop > /dev/null 2>&1; then
    m=no
    if git -C "$P" merge-base --is-ancestor "$hd" origin/develop 2>/dev/null; then m=ancestor
    else
      mb=$(git -C "$P" merge-base "$hd" origin/develop 2>/dev/null)
      if [ -n "$mb" ]; then
        files=$(git -C "$P" diff --name-only "$mb" "$hd" 2>/dev/null)
        if [ -z "$files" ]; then m=ancestor
        elif git -C "$P" diff --quiet "$hd" origin/develop -- $(echo "$files" | tr '\n' ' ') 2>/dev/null; then m=squash
        fi
      fi
    fi
  fi
  sz=$(du -sk "$P" | cut -f1)
  nm=$(find "$P" -maxdepth 5 -name node_modules -type d -prune -print0 | xargs -0 du -sk 2>/dev/null | awk '{s+=$1} END{print s+0}')
  newest=$(find "$P" \( -name node_modules -o -name .git \) -prune -o -type f -exec stat -f %m {} + | sort -n | tail -1)
  topm=$(stat -f %m "$P")
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$P" "$br" "$hd" "${ct:-0}" "$dirty" "$m" "$sz" "$nm" "${newest:-0}" "$topm"
  exit 0
fi

if ! self_check "$SELF"; then exit 3; fi
[ -n "$CHECK_ONLY" ] && exit 0

# ---- mount guard -------------------------------------------------------------------------------------------
if ! mount | grep -q ' on /Volumes/DevMASTER '; then
  echo "REFUSED: /Volumes/DevMASTER is not mounted." >&2
  exit 2
fi
if [ ! -d "$ROOT" ]; then echo "REFUSED: root $ROOT not found." >&2; exit 2; fi

[ -z "$NOW" ] && NOW=$(date +%s)
[ -z "$DATE" ] && DATE=$(date -r "$NOW" +%F)
LIVE_S=$((LIVE_HOURS * 3600)); OLD_S=$((OLD_DAYS * 86400)); REGEN_S=$((REGEN_DAYS * 86400))
export GIT_OPTIONAL_LOCKS=0
mkdir -p "$REPORT_DIR" || exit 2
REPORT="$REPORT_DIR/dryrun_$DATE.md"

# ---- tallies ----------------------------------------------------------------------------------------------
CLASSES="W N T E P R S H"
for c in $CLASSES; do eval "N_$c=0; K_$c=0; CN_$c=0; CK_$c=0"; done
tally() { # class verdict kb
  local c="$1" v="$2" kb="$3"
  eval "N_$c=\$((N_$c+1)); K_$c=\$((K_$c+kb))"
  if [ "$v" = CANDIDATE ]; then eval "CN_$c=\$((CN_$c+1)); CK_$c=\$((CK_$c+kb))"; fi
}
mb() { awk -v k="$1" 'BEGIN{printf "%.1f", k/1024}'; }
age_d() { awk -v n="$NOW" -v t="$1" 'BEGIN{ if (t<=0) print "?"; else printf "%.1f", (n-t)/86400 }'; }
row() { # class verdict kb age path reason
  printf '| %s | %s | %s | %s | `%s` | %s |\n' "$1" "$2" "$(mb "$3")" "$4" "$5" "$6"
}

# ---- live set: cwd of every process + any path mentioned in a running command line ------------------------
LIVE_PATHS=$(
  { lsof -d cwd -Fn | sed -n 's/^n//p'; ps -axo command= | tr ' ' '\n'; } |
    awk -v a="$ROOT" -v b="$LM" 'index($0,a)==1 || index($0,b)==1'
)
is_live() { # path -> 0 if a live process cwd/cmdline sits at or under path, or path is under it
  local p="$1" l
  [ -z "$LIVE_PATHS" ] && return 1
  while IFS= read -r l; do
    [ -z "$l" ] && continue
    case "$l" in "$p"|"$p"/*) return 0;; esac
  done <<EOF
$LIVE_PATHS
EOF
  return 1
}
# the live seat itself: its cwd is the project root, which is also an ancestor of everything; only exact
# worktree-or-below hits count (root itself is not a candidate class), so no special case is needed.

main() {
echo "# Storage dry-run: Secuura/Blockchain + Wednesday local-model -- $DATE"
echo
echo "READ-ONLY report. Nothing was removed, moved or renamed. root=\`$ROOT\` lm=\`$LM\` now=$(date -r "$NOW" '+%F %T')"
echo "Predicates: live = modified < ${LIVE_HOURS}h or a process cwd/cmdline holds it; W = merged(ancestor|squash vs local origin/develop, no fetch) + clean + idle >= ${OLD_DAYS}d; N,T,E,R = regenerable + idle >= ${REGEN_DAYS}d."
echo
echo "| class | verdict | MB | age d | path | why |"
echo "|---|---|---|---|---|---|"

# ---- W + N: working copies ---------------------------------------------------------------------------------
WC_LIST=$(find "$ROOT/worktrees" "$ROOT/deploy-clones" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort)
export SELF
PROBES=""
if [ -n "$WC_LIST" ]; then
  PROBES=$(printf '%s\n' "$WC_LIST" | tr '\n' '\0' | xargs -0 -n1 -P "$JOBS" /bin/bash "$SELF" --probe)
fi
NM_LINES=""
while IFS=$'\t' read -r P BR HD CT DIRTY MRG SZ NM NEWEST TOPM; do
  [ -z "$P" ] && continue
  eff=$NEWEST; [ "${TOPM:-0}" -gt "${eff:-0}" ] && eff=$TOPM
  idle=$((NOW - eff)); [ "$eff" -le 0 ] && idle=0
  ad=$(age_d "$eff")
  verdict=KEEP; why=""
  if [ "$BR" = NOTGIT ]; then why="not a git checkout"
  elif is_live "$P"; then why="LIVE: a running process holds this path"
  elif [ "$idle" -lt "$LIVE_S" ]; then why="LIVE: modified within ${LIVE_HOURS}h"
  elif [ "$DIRTY" != 0 ]; then why="DIRTY: $DIRTY uncommitted path(s)"
  elif [ "$MRG" = nodev ]; then why="no origin/develop ref known locally: merged state unprovable"
  elif [ "$MRG" = no ]; then why="UNMERGED: branch $BR not contained in origin/develop"
  elif [ "$idle" -lt "$OLD_S" ]; then why="young: idle ${ad}d < ${OLD_DAYS}d (merged:$MRG)"
  else verdict=CANDIDATE; why="merged:$MRG, clean, idle ${ad}d (branch $BR)"
  fi
  row W "$verdict" "$SZ" "$ad" "$P" "$why"
  tally W "$verdict" "$SZ"
  # N: node_modules in a working copy W kept, if not live and idle long enough (regenerable; not in git)
  if [ "$verdict" = KEEP ] && [ "${NM:-0}" -gt 0 ] && [ "$BR" != NOTGIT ] && ! is_live "$P" && [ "$idle" -ge "$REGEN_S" ]; then
    NM_LINES="$NM_LINES$P	$NM	$ad
"
  fi
done <<EOF
$PROBES
EOF

echo
echo "| class | verdict | MB | age d | path | why |"
echo "|---|---|---|---|---|---|"
while IFS=$'\t' read -r P NM AD; do
  [ -z "$P" ] && continue
  row N CANDIDATE "$NM" "$AD" "$P/**/node_modules" "regenerable (npm ci); working copy kept by W but idle ${AD}d >= ${REGEN_DAYS}d, no live holder"
  tally N CANDIDATE "$NM"
done <<EOF
$NM_LINES
EOF

# ---- T: test artefacts in non-live working copies idle >= REGEN_DAYS ------------------------------------------
echo
echo "| class | verdict | MB | age d | path | why |"
echo "|---|---|---|---|---|---|"
TA=$(find "$ROOT/worktrees" "$ROOT/deploy-clones" -maxdepth 6 \( -name node_modules -o -name .git \) -prune -o -type d \
      \( -name coverage -o -name test-results -o -name playwright-report -o -name allure-results -o -name allure-report -o -name .nyc_output \) -print 2>/dev/null)
while IFS= read -r D; do
  [ -z "$D" ] && continue
  kb=$(du -sk "$D" | cut -f1)
  newest=$(find "$D" -type f -exec stat -f %m {} + 2>/dev/null | sort -n | tail -1); newest=${newest:-$(stat -f %m "$D")}
  ad=$(age_d "$newest"); idle=$((NOW - newest))
  top=$(printf '%s' "$D" | sed -E "s|^($ROOT/(worktrees\|deploy-clones)/[^/]+)/.*|\1|")
  if is_live "$top"; then v=KEEP; w="LIVE: process holds the working copy"
  elif [ "$idle" -lt "$LIVE_S" ]; then v=KEEP; w="LIVE: modified within ${LIVE_HOURS}h"
  elif [ "$idle" -lt "$REGEN_S" ]; then v=KEEP; w="young: idle ${ad}d < ${REGEN_DAYS}d"
  elif [ -n "$(git -C "$top" ls-files -- "${D#$top/}" 2>/dev/null | head -1)" ]; then v=KEEP; w="TRACKED: git tracks files in it (not regenerable output)"
  else v=CANDIDATE; w="untracked test output, idle ${ad}d"; fi
  row T "$v" "$kb" "$ad" "$D" "$w"; tally T "$v" "$kb"
done <<EOF
$TA
EOF

# ---- E / P: regenerable subtrees inside evidence folders (5_Project_History) and seat scratch (scratchpad) ----------
# Records stay. Only scratch clones (clean, HEAD in origin/develop) and node_modules are ever candidates.
scan_scratch() { # class rootdir
  local C="$1" R="$2" D kb newest ad idle v w dirty hd kind CANDCL="" cl cov EV
  [ -d "$R" ] || return 0
  EV=$( { find "$R" -maxdepth 6 -name .git -print 2>/dev/null | sed 's|/\.git$||' | sed 's|^|clone\t|'
          find "$R" -maxdepth 6 -name .git -prune -o -type d -name node_modules -print -prune 2>/dev/null | sed 's|^|nm\t|'
        } | sort -u)
  while IFS=$'\t' read -r kind D; do
    [ -z "$D" ] && continue
    if [ "$kind" = nm ]; then
      cov=0
      for cl in $CANDCL; do case "$D" in "$cl"/*) cov=1;; esac; done
      [ "$cov" = 1 ] && continue   # already inside a candidate clone: not counted twice
    fi
    kb=$(du -sk "$D" | cut -f1)
    newest=$(find "$D" \( -name node_modules -o -name .git \) -prune -o -type f -exec stat -f %m {} + 2>/dev/null | sort -n | tail -1); newest=${newest:-$(stat -f %m "$D")}
    ad=$(age_d "$newest"); idle=$((NOW - newest))
    v=KEEP; w=""
    if is_live "$D"; then w="LIVE: process holds it"
    elif [ "$idle" -lt "$LIVE_S" ]; then w="LIVE: modified within ${LIVE_HOURS}h"
    elif [ "$idle" -lt "$REGEN_S" ]; then w="young: idle ${ad}d < ${REGEN_DAYS}d"
    elif [ "$kind" = nm ]; then v=CANDIDATE; w="regenerable node_modules; the files beside it stay"
    else
      dirty=$(git -C "$D" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
      hd=$(git -C "$D" rev-parse HEAD 2>/dev/null)
      if [ "$dirty" != 0 ]; then w="DIRTY: $dirty uncommitted path(s)"
      elif ! git -C "$D" rev-parse --verify -q origin/develop > /dev/null 2>&1; then w="no origin/develop ref locally: merged state unprovable"
      elif git -C "$D" merge-base --is-ancestor "$hd" origin/develop 2>/dev/null; then v=CANDIDATE; w="scratch clone/worktree, clean, HEAD in origin/develop, idle ${ad}d"
      else w="UNMERGED (ancestor test only here): not proven merged"; fi
    fi
    [ "$kind" = clone ] && [ "$v" = CANDIDATE ] && CANDCL="$CANDCL $D"
    row "$C" "$v" "$kb" "$ad" "$D" "$w"; tally "$C" "$v" "$kb"
  done <<EOF2
$EV
EOF2
}
echo
echo "| class | verdict | MB | age d | path | why |"
echo "|---|---|---|---|---|---|"
scan_scratch E "$ROOT/5_Project_History"
scan_scratch P "$ROOT/scratchpad"
# P: seat scratch folders that hold neither a clone nor node_modules are unclassified: listed, never candidates
if [ -d "$ROOT/scratchpad" ]; then
  for D in "$ROOT"/scratchpad/*/*; do
    [ -d "$D" ] || continue
    if [ -n "$(find "$D" -maxdepth 4 \( -name .git -o -name node_modules \) -print 2>/dev/null | head -1)" ]; then continue; fi
    kb=$(du -sk "$D" | cut -f1); mt=$(stat -f %m "$D")
    row P KEEP "$kb" "$(age_d "$mt")" "$D" "unclassified seat scratch (no clone, no node_modules): owner decides"
    tally P KEEP "$kb"
  done
fi

# ---- R: local-model runs: scratch clones / caches inside a run (the record files stay) ---------------------------
echo
echo "| class | verdict | MB | age d | path | why |"
echo "|---|---|---|---|---|---|"
if [ -d "$LM/runs" ]; then
  RC=$(find "$LM/runs" -maxdepth 3 -type d \( -name clone -o -name clones -o -name cache -o -name work \) -prune -print 2>/dev/null)
  while IFS= read -r D; do
    [ -z "$D" ] && continue
    kb=$(du -sk "$D" | cut -f1)
    newest=$(find "$D" \( -name node_modules -o -name .git \) -prune -o -type f -exec stat -f %m {} + 2>/dev/null | sort -n | tail -1); newest=${newest:-$(stat -f %m "$D")}
    ad=$(age_d "$newest"); idle=$((NOW - newest))
    if is_live "$D"; then v=KEEP; w="LIVE: process holds it"
    elif [ "$idle" -lt "$LIVE_S" ]; then v=KEEP; w="LIVE: modified within ${LIVE_HOURS}h"
    elif [ "$idle" -lt "$REGEN_S" ]; then v=KEEP; w="young: idle ${ad}d < ${REGEN_DAYS}d"
    else v=CANDIDATE; w="regenerable run scratch (clone/cache), idle ${ad}d; run record files beside it stay"; fi
    row R "$v" "$kb" "$ad" "$D" "$w"; tally R "$v" "$kb"
  done <<EOF
$RC
EOF
fi

# ---- S: spark/cache/work -- prune_work.py's four guards, read-only ------------------------------------------------
echo
echo "| class | verdict | MB | age d | path | why |"
echo "|---|---|---|---|---|---|"
DONE_MD="$LM/spark/done.md"
if [ -d "$LM/spark/cache/work" ]; then
  for D in "$LM"/spark/cache/work/*; do
    [ -d "$D" ] || continue
    kb=$(du -sk "$D" | cut -f1)
    mt=$(stat -f %m "$D"); ad=$(age_d "$mt"); idle=$((NOW - mt))
    mk="$D/.spark_round_work"
    v=KEEP; w=""
    if [ ! -f "$mk" ]; then w="no .spark_round_work marker (prune_work guard 2): not the runner's own"
    else
      rd=$(sed -n 's/^run_dir=//p' "$mk"); pid=$(sed -n 's/^pid=//p' "$mk")
      if [ -z "$rd" ] || ! grep -F -q "$rd" "$DONE_MD" 2>/dev/null; then w="no verdict row in done.md for its run (guard 3): round not recorded"
      elif [ -z "$pid" ] || [ "$pid" -le 1 ] 2>/dev/null; then w="marker pid malformed (guard 4)"
      elif ps -p "$pid" > /dev/null 2>&1; then w="LIVE: marker pid $pid alive"
      elif is_live "$D"; then w="LIVE: a process holds it"
      elif [ "$idle" -lt "$LIVE_S" ]; then w="LIVE: modified within ${LIVE_HOURS}h (recorded, pid dead; prune_work.py may take it)"
      else v=CANDIDATE; w="recorded in done.md, pid $pid dead, idle ${ad}d; regenerable from cache/src (prune_work.py guards 1-4 hold)"; fi
    fi
    row S "$v" "$kb" "$ad" "$D" "$w"; tally S "$v" "$kb"
  done
fi

# ---- H: hosted/work -------------------------------------------------------------------------------------------------
echo
echo "| class | verdict | MB | age d | path | why |"
echo "|---|---|---|---|---|---|"
if [ -d "$LM/hosted/work" ]; then
  for D in "$LM"/hosted/work/*; do
    [ -d "$D" ] || continue
    kb=$(du -sk "$D" | cut -f1)
    newest=$(find "$D" \( -name node_modules -o -name .git \) -prune -o -type f -exec stat -f %m {} + 2>/dev/null | sort -n | tail -1); newest=${newest:-$(stat -f %m "$D")}
    ad=$(age_d "$newest"); idle=$((NOW - newest))
    if is_live "$D"; then v=KEEP; w="LIVE: process holds it"
    elif [ "$idle" -lt "$LIVE_S" ]; then v=KEEP; w="LIVE: modified within ${LIVE_HOURS}h"
    elif [ "$idle" -lt "$REGEN_S" ]; then v=KEEP; w="young: idle ${ad}d < ${REGEN_DAYS}d"
    else v=CANDIDATE; w="hosted-model work dir, idle ${ad}d (regenerable by the next hosted run)"; fi
    row H "$v" "$kb" "$ad" "$D" "$w"; tally H "$v" "$kb"
  done
fi

# ---- totals ------------------------------------------------------------------------------------------------------------
echo
echo "## Totals (MB; W includes the node_modules inside its candidates, N is only for working copies W kept)"
echo
echo "| class | items | total MB | candidates | candidate MB |"
echo "|---|---|---|---|---|"
GT=0
for c in $CLASSES; do
  eval "n=\$N_$c; k=\$K_$c; cn=\$CN_$c; ck=\$CK_$c"
  echo "| $c | $n | $(mb "$k") | $cn | $(mb "$ck") |"
  GT=$((GT + ck))
done
echo
echo "Candidate total: $(awk -v k="$GT" 'BEGIN{printf "%.2f", k/1048576}') GiB. Proposal only; removal is the project seat's act under Kam's word."
echo "Not measured here: remote boxes (kintsugi, demo), PR state via gh, docker images, /Volumes/Development."
echo "done: no file was changed other than this report."
}
main | tee "$REPORT"
