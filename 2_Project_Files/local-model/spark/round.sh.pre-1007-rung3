#!/bin/bash
# round.sh <brief_dir> [--dry-run] [pin=value ...] — ONE Spark round for ONE Secuura brief (2026-10-05, Kam "aim for 50 a day").
#
# The durable, in-tree replacement for the scratchpad round scripts (mksrc.sh / linknm.sh / mkclone.sh / precheck.sh /
# ap.sh) that died with their session at every rotation (IMPROVEMENTS 2026-09-27 19:22, 2026-10-04 19:0x, 2026-10-05
# 02:3x). It re-implements NO builder and NO checker; it only sequences the harness's own:
#
#   1. brief gate        spark/brief_lint.py (shape, client, tier, pins)                        -> rc 2 REFUSED
#   2. endpoint          GET $SPARK_URL/v1/models must answer 200                               -> rc 4 ENDPOINT DOWN
#   3. lock              spark/state/round.lock (one round at a time; the box runs ONE request) -> rc 3 BUSY
#   4. base              develop as `git -C <Secuura checkout> ls-remote origin refs/heads/develop` reads it (or
#                        SPARK_TIP), fetched into the durable cache clone spark/cache/src (origin = the checkout's own
#                        GitHub origin + its core.sshCommand, so the builders' own `ls-remote origin` agrees — the
#                        09-29/10-01 stale-origin fault cannot recur); node_modules symlinked FROM the Secuura checkout
#                        INTO the cache (never the reverse); refuses if Blockchain/Dev/node_modules is absent there.
#   5. stale brief       the brief's files must be unchanged between its `Tip:` and the pinned base -> rc 2 (pin
#                        allow_drift=1 to override)
#   6. input             night/build_input.sh (code_patch) | tasks/code_patch2/build_input2.sh (code_patch2: the same
#                        builder for the first product, plus the declared multi-file set) |
#                        tasks/bash_patch/build_bash_input.sh (bash_patch), with
#                        NIGHT_SOURCE_CHECKOUT=cache/src, NIGHT_BRIEFS_DIR=<brief_dir>; builder rc 2 -> rc 2 REFUSED
#   7. clone             `git clone --shared --no-checkout cache/src` + `checkout --detach <tip>` under
#                        spark/cache/work/<run-id>/clone; code_patch: tasks/code_patch/prepare_clone.sh
#   8. model             local_model_task.sh with LM_BACKEND=spark, SPARK_THINK=0 (thinking OFF, always), the
#                        harness's own timeouts (10 s health, SPARK_HTTP_TIMEOUT 1800 s in lib/spark_call.py)
#   9. checker           code_patch: tasks/code_patch/spark_checker.sh (checker.sh + A2a)
#                        code_patch2: tasks/code_patch2/checker.sh, then A2a as for bash_patch (task.md DERIVED from
#                        code_patch's by tasks/code_patch2/make_task.py into the run dir)
#                        bash_patch: tasks/bash_patch/checker.sh, then A2a (code_patch/a2a_anchor.py over
#                        sections_with_n.json) appended to checker.out with the same PASS/FAIL A2a + SPARK RESULT lines
#  10. golden            `cmp` of out.md.checker/patch.diff against <brief_dir>/golden.diff when one exists
#
# Run dir: local-model/runs/spark_secuura_<YYYY-MM-DD>_<brief-dir-name>[-rN], the shape the 10-05 rounds left:
# input.json, out.md(+.meta.json, .raw.json), run.log, checker.out, out.md.checker/, prepare_clone.out (code_patch),
# plus build_input.out and round.json (this script's own record).
# Prints ONE verdict line last:  SPARK ROUND <tag>: <PASS|FAIL|REFUSED|...> ...
#
# --dry-run: steps 1, 2 (reported, not enforced), 3-6 into spark/state/dry/<id>/; no clone, no model, no run dir.
# --control: the GOLDEN control (what the scratch precheck.sh's CONTROL half did): steps 1, 3-7, 9, 10 with out.md = the
#            brief dir's golden.diff in a ```diff fence instead of a model answer; no endpoint check, no model call.
#            Run dir ..._<tag>-control[-rN]. A brief whose golden does not PASS here is a brief defect, not a model one.
#
# Exit: 0 PASS · 1 FAIL (a model verdict) · 2 REFUSED (brief/client/stale/builder) · 3 BUSY · 4 ENDPOINT DOWN ·
#       5 HARNESS (cache/fetch/clone/prepare/model-call/VOID — not a model verdict) · 64 usage.
# It NEVER raises a PR, pushes, merges, posts, or holds a READY. Never writes under !CODING: git READ verbs only there
# (ls-remote, config --get, clone-from). bash 3.2; stderr never discarded; no cd.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(dirname "$HERE")"
SECUURA="${SPARK_SECUURA_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
SPARK_URL="${SPARK_URL:-http://127.0.0.1:47788}"
CACHE="${SPARK_CACHE:-$HERE/cache}"
STATE="${SPARK_STATE:-$HERE/state}"
WORK_ROOT="${SPARK_WORK_ROOT:-$CACHE/work}"
RUNS="${SPARK_RUNS:-$LM/runs}"
SRC="$CACHE/src"
SUBDIR="Blockchain/Dev"
# node_modules dirs NOT linked into the cache (IMPROVEMENTS 2026-10-01: billing's own lock modules make tsc FAIL rc 2;
# the root farm alone is green). Space-separated, relative to Blockchain/Dev.
NM_EXCLUDE="${SPARK_NM_EXCLUDE:-services/billing}"

BDIR=""; DRY=0; CONTROL=0; PINS=()
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    --control) CONTROL=1 ;;
    -h|--help) sed -n 2,40p "$0"; exit 0 ;;
    *=*) PINS+=("$a") ;;
    *) if [ -z "$BDIR" ]; then BDIR="$a"; else echo "round.sh: unexpected argument '$a'" >&2; exit 64; fi ;;
  esac
done
[ -n "$BDIR" ] || { echo "usage: round.sh <brief_dir> [--dry-run|--control] [pin=value ...]" >&2; exit 64; }
[ "$DRY" -eq 1 ] && [ "$CONTROL" -eq 1 ] && { echo "round.sh: --dry-run and --control are exclusive" >&2; exit 64; }
[ -d "$BDIR" ] || { echo "SPARK ROUND ?: REFUSED — brief dir does not exist: $BDIR"; exit 2; }
BDIR="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$BDIR")"
TAG="$(basename "$BDIR")"
T0=$(date +%s)
SUMMARY="${SPARK_ROUND_SUMMARY:-}"

say() { echo "round: $*"; }
summary() { # summary <verdict line> <rc> [run_dir]
  [ -n "$SUMMARY" ] || return 0
  python3 - "$SUMMARY" "$TAG" "$1" "$2" "${3:-}" "$(( $(date +%s) - T0 ))" <<'PY'
import json, os, sys
p, tag, line, rc, run, wall = sys.argv[1:7]
d = {"tag": tag, "verdict": line.split()[0], "line": line, "rc": int(rc), "run_dir": run, "round_wall_s": int(wall)}
if run and os.path.isfile(os.path.join(run, "round.json")):
    d.update(json.load(open(os.path.join(run, "round.json"))))
json.dump(d, open(p, "w"), indent=1)
PY
}
finish() { # finish <rc> <verdict line> [run_dir]
  local rc="$1" line="$2" run="${3:-}"
  echo "SPARK ROUND $TAG: $line"
  summary "$line" "$rc" "$run"
  exit "$rc"
}

# ------------------------------------------------------------------ 1. brief gate
LINT_OUT="$(python3 "$HERE/brief_lint.py" "$BDIR" ${PINS[@]+"${PINS[@]}"} 2>&1)"; LRC=$?
if [ "$LRC" -ne 0 ]; then
  echo "$LINT_OUT" | sed 's/^/round: /'
  finish 2 "REFUSED — brief gate: $(echo "$LINT_OUT" | grep -c '^REFUSED') reason(s), first: $(echo "$LINT_OUT" | grep -m1 '^REFUSED' | cut -c9-220)"
fi
eval "$LINT_OUT"
say "brief $B_BRIEF · tier $B_TIER · runner $B_RUNNER · pins: ${B_PINS:-none}"

# ------------------------------------------------------------------ 2. endpoint
if [ "$CONTROL" -eq 1 ]; then
  [ -n "$B_GOLDEN" ] || finish 2 "REFUSED — --control needs $BDIR/golden.diff"
  say "control: golden $B_GOLDEN (no model call; endpoint not checked)"
else
EP_CODE="$(curl -s -m 10 -o /dev/null -w '%{http_code}' "$SPARK_URL/v1/models" 2>&1)"; EP_RC=$?
if [ "$EP_RC" -ne 0 ] || [ "$EP_CODE" != "200" ]; then
  if [ "$DRY" -eq 1 ]; then
    say "endpoint: DOWN ($SPARK_URL/v1/models curl rc=$EP_RC http=$EP_CODE) — a real round would refuse rc 4"
  else
    finish 4 "ENDPOINT DOWN — $SPARK_URL/v1/models curl rc=$EP_RC http=$EP_CODE. Check the tunnel (pgrep -fl 'L 47788:127.0.0.1:8888') then the box; this script never restarts either"
  fi
else
  say "endpoint: $SPARK_URL/v1/models 200"
fi
fi

# ------------------------------------------------------------------ 3. lock
mkdir -p "$STATE"
LOCK="$STATE/round.lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  OLDPID="$(cat "$LOCK/pid" 2>/dev/null)"
  if [ -n "$OLDPID" ] && kill -0 "$OLDPID" 2>/dev/null; then
    finish 3 "BUSY — another round holds $LOCK (pid $OLDPID: $(cat "$LOCK/what" 2>/dev/null)); the Spark runs ONE request at a time"
  fi
  STALE="$STATE/stale_locks/$(date +%Y%m%d-%H%M%S)"; mkdir -p "$STALE"
  mv "$LOCK" "$STALE/round.lock" && say "reclaimed a stale lock (pid ${OLDPID:-none} not alive) -> $STALE" >&2
  mkdir "$LOCK" 2>/dev/null || finish 3 "BUSY — could not take $LOCK after reclaiming a stale one"
fi
echo $$ > "$LOCK/pid"; echo "$TAG $( [ $DRY -eq 1 ] && echo dry-run )$( [ $CONTROL -eq 1 ] && echo control ) since $(date '+%F %T')" > "$LOCK/what"
trap 'rm -f "$LOCK/pid" "$LOCK/what" "$LOCK/work"; rmdir "$LOCK" 2>/dev/null' EXIT

# ------------------------------------------------------------------ 4. base: cache clone at develop
[ -d "$SECUURA/.git" ] || finish 5 "HARNESS — Secuura checkout missing at $SECUURA"
[ -d "$SECUURA/$SUBDIR/node_modules" ] || finish 5 "HARNESS — $SECUURA/$SUBDIR/node_modules is absent: prepare_clone links node_modules FROM the source, so A4-A7 would fail 'Preset ts-jest not found' (IMPROVEMENTS 2026-09-27 19:22). A Secuura seat must install first"
ORIGIN_URL="$(git -C "$SECUURA" remote get-url origin 2>&1)"
case "$ORIGIN_URL" in
  git@*|ssh://*|https://*) ;;
  *) finish 5 "HARNESS — the Secuura checkout's origin is not a remote URL ($ORIGIN_URL): its ls-remote would answer from a local path (the 09-29 stale-origin fault)" ;;
esac
SSHCMD="$(git -C "$SECUURA" config --get core.sshCommand 2>/dev/null)"
if [ ! -d "$SRC/.git" ]; then
  mkdir -p "$CACHE"
  say "cache: first use — cloning $SECUURA into $SRC (--no-hardlinks: an independent object store, nothing written to the source)"
  git clone -q --no-hardlinks --no-checkout "$SECUURA" "$SRC" 2>&1 | sed 's/^/round: clone: /'
  [ -d "$SRC/.git" ] || finish 5 "HARNESS — cache clone failed"
  git -C "$SRC" config gc.auto 0   # per-round clones borrow these objects (--shared); never let gc prune under them
fi
git -C "$SRC" remote set-url origin "$ORIGIN_URL"
if [ -n "$SSHCMD" ]; then git -C "$SRC" config core.sshCommand "$SSHCMD"; fi

if [ -n "${SPARK_TIP:-}" ]; then
  TIP="$SPARK_TIP"; TIP_HOW="SPARK_TIP (pinned by the caller)"
else
  TIP="$(git -C "$SECUURA" ls-remote origin refs/heads/develop 2>&1 | awk '/refs\/heads\/develop$/{print $1}')"
  TIP_HOW="git -C <Secuura checkout> ls-remote origin refs/heads/develop at $(date '+%F %T')"
fi
echo "$TIP" | grep -qE '^[0-9a-f]{40}$' || finish 5 "HARNESS — could not read develop's tip (got '${TIP:-nothing}'; offline?)"
if [ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" != "commit" ]; then
  say "cache: fetching develop from origin (tip $TIP not yet local)"
  git -C "$SRC" fetch -q origin "+refs/heads/develop:refs/remotes/origin/develop" 2>&1 | sed 's/^/round: fetch: /'
fi
[ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" = "commit" ] || finish 5 "HARNESS — tip $TIP is still not in the cache after a fetch"
CACHE_LS="$(git -C "$SRC" ls-remote origin refs/heads/develop 2>/dev/null | awk '{print $1}')"
if [ -z "${SPARK_TIP:-}" ] && [ "$CACHE_LS" != "$TIP" ]; then
  finish 5 "HARNESS — VOID: develop moved while preparing (Secuura read $TIP, cache's origin now reads ${CACHE_LS:-nothing}); re-run"
fi
git -C "$SRC" checkout -q --detach -f "$TIP" 2>&1 | sed 's/^/round: checkout: /'
[ "$(git -C "$SRC" rev-parse HEAD)" = "$TIP" ] || finish 5 "HARNESS — cache checkout is not at $TIP"
say "base: develop $TIP ($TIP_HOW)"

# node_modules: symlink FROM the Secuura checkout INTO the cache (first-level dirs under Blockchain/Dev, minus NM_EXCLUDE)
NM_N=0
while IFS= read -r nm; do
  [ -z "$nm" ] && continue
  rel="${nm#"$SECUURA/$SUBDIR/"}"; rel="${rel%/node_modules}"; [ "$rel" = "node_modules" ] && rel="."
  skip=0; for x in $NM_EXCLUDE; do [ "$rel" = "$x" ] && skip=1; done
  [ "$skip" -eq 1 ] && continue
  if [ "$rel" = "." ]; then t="$SRC/$SUBDIR/node_modules"; else t="$SRC/$SUBDIR/$rel/node_modules"; fi
  [ -d "$(dirname "$t")" ] || continue          # the dir is not at this tip
  if [ ! -e "$t" ] && [ ! -L "$t" ]; then ln -s "$nm" "$t"; fi
  ex="/${t#"$SRC/"}"; grep -qxF "$ex" "$SRC/.git/info/exclude" 2>/dev/null || echo "$ex" >> "$SRC/.git/info/exclude"
  NM_N=$((NM_N+1))
done < <(find "$SECUURA/$SUBDIR" -mindepth 1 -maxdepth 3 -name node_modules -not -path '*/node_modules/*' 2> "$STATE/nm_find.err")
[ -e "$SRC/$SUBDIR/node_modules" ] || finish 5 "HARNESS — cache has no $SUBDIR/node_modules after linking"
DIRTY="$(git -C "$SRC" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
[ "$DIRTY" = "0" ] || finish 5 "HARNESS — cache checkout has $DIRTY tracked modification(s); it must be pristine at $TIP"
say "cache: $SRC at $TIP, $NM_N node_modules link(s) (excluded: ${NM_EXCLUDE:-none})"

# ------------------------------------------------------------------ 5. stale brief
BT="$B_BRIEF_TIP"
if git -C "$SRC" cat-file -e "$BT^{commit}" 2>/dev/null; then
  BT_FULL="$(git -C "$SRC" rev-parse "$BT^{commit}")"
  if [ "$BT_FULL" != "$TIP" ]; then
    DPATHS=()
    for p in $B_DRIFT_PATHS; do
      if git -C "$SRC" cat-file -e "$TIP:$p" 2>/dev/null || git -C "$SRC" cat-file -e "$BT_FULL:$p" 2>/dev/null; then DPATHS+=("$p")
      else DPATHS+=("$SUBDIR/$p"); fi
    done
    CHANGED="$(git -C "$SRC" diff --name-only "$BT_FULL" "$TIP" -- "${DPATHS[@]}" 2>&1)"
    if [ -n "$CHANGED" ]; then
      if [ "$B_ALLOW_DRIFT" = "1" ]; then
        say "WARNING brief written at ${BT_FULL:0:12}; these changed by $TIP: $(echo $CHANGED) — allow_drift=1, proceeding"
      else
        finish 2 "REFUSED — STALE BRIEF: written at ${BT_FULL:0:12}, and by develop ${TIP:0:12} these changed: $(echo $CHANGED). Re-measure the brief (or pin allow_drift=1 if the edit points are untouched)"
      fi
    else
      say "brief written at ${BT_FULL:0:12}; develop is now ${TIP:0:12}; none of [${DPATHS[*]}] changed between them"
    fi
  fi
else
  say "WARNING the brief's Tip: $BT is not in the cache — drift not measured"
fi

# ------------------------------------------------------------------ 6. input
DAY="$(date +%Y-%m-%d)"
if [ "$DRY" -eq 1 ]; then
  RUN="$STATE/dry/${TAG}_$(date +%Y%m%d-%H%M%S)"
else
  SFX=""; [ "$CONTROL" -eq 1 ] && SFX="-control"
  RUN="$RUNS/spark_secuura_${DAY}_${TAG}${SFX}"; n=2
  while [ -e "$RUN" ]; do RUN="$RUNS/spark_secuura_${DAY}_${TAG}${SFX}-r$n"; n=$((n+1)); done
fi
mkdir -p "$RUN"
say "run dir: $RUN"
if [ "$B_TIER" = code_patch2 ]; then
  NIGHT_SOURCE_CHECKOUT="$SRC" NIGHT_BRIEFS_DIR="$BDIR" bash "$LM/tasks/code_patch2/build_input2.sh" "$B_TICKET" "$RUN/input.json" "$B_BRIEF" ${B_PINS_ARR[@]+"${B_PINS_ARR[@]}"} > "$RUN/build_input.out" 2>&1; BRC=$?
elif [ "$B_TIER" = code_patch ]; then
  NIGHT_SOURCE_CHECKOUT="$SRC" NIGHT_BRIEFS_DIR="$BDIR" bash "$LM/night/build_input.sh" "$B_TICKET" "$RUN/input.json" ${B_PINS_ARR[@]+"${B_PINS_ARR[@]}"} > "$RUN/build_input.out" 2>&1; BRC=$?
else
  NIGHT_SOURCE_CHECKOUT="$SRC" bash "$LM/tasks/bash_patch/build_bash_input.sh" "$B_TICKET" "$RUN/input.json" "$B_BRIEF" ${B_PINS_ARR[@]+"${B_PINS_ARR[@]}"} > "$RUN/build_input.out" 2>&1; BRC=$?
fi
if [ "$BRC" -ne 0 ]; then
  sed 's/^/round: build: /' "$RUN/build_input.out" | tail -8
  if [ "$BRC" -eq 2 ]; then finish 2 "REFUSED — builder rc 2: $(grep -m1 -i 'REFUSED' "$RUN/build_input.out" | cut -c1-240)" "$RUN"; fi
  finish 5 "HARNESS — builder rc $BRC: $(tail -1 "$RUN/build_input.out" | cut -c1-240)" "$RUN"
fi
if [ "$B_TIER" != bash_patch ] && ! grep -q 'WEDNESDAY BRIEF' "$RUN/build_input.out"; then
  finish 2 "REFUSED — the builder did not read the brief as the prompt (no 'WEDNESDAY BRIEF' in build_input.out): a ticket-description fallback is a refusal (kit 02 §1)" "$RUN"
fi
IN_TIP="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("tip") or d.get("repo",{}).get("tip",""))' "$RUN/input.json")"
[ "$IN_TIP" = "$TIP" ] || finish 5 "HARNESS — VOID: the builder pinned ${IN_TIP:-nothing}, the round prepared $TIP (develop moved mid-round?)" "$RUN"
SELFTEST="$(python3 -c 'import json,sys; print(1 if json.load(open(sys.argv[1])).get("self_testing") else 0)' "$RUN/input.json")"
TASK_MD="$LM/tasks/$B_TIER/task.md"
[ "$B_TIER" = bash_patch ] && [ "$SELFTEST" = 1 ] && TASK_MD="$LM/tasks/bash_patch/task_selftest.md"
if [ "$B_TIER" = code_patch2 ]; then
  TASK_MD="$RUN/task.md"
  python3 "$LM/tasks/code_patch2/make_task.py" "$TASK_MD" > "$RUN/make_task.out" 2>&1 || finish 5 "HARNESS — make_task.py could not derive the code_patch2 task: $(tail -1 "$RUN/make_task.out" | cut -c1-200)" "$RUN"
fi
[ -n "$B_OVERRIDE_NOT_RUNNABLE" ] && say "WARNING the brief's header says NOT RUNNABLE; overridden by pin override_not_runnable=$B_OVERRIDE_NOT_RUNNABLE"
say "input: $(tail -1 "$RUN/build_input.out" | cut -c1-200)"

if [ "$DRY" -eq 1 ]; then
  finish 0 "DRY-RUN OK — brief accepted, input built at ${TIP:0:12} ($(wc -c < "$RUN/input.json" | tr -d ' ') B) in $RUN; a real round would call $SPARK_URL with $(basename "$(dirname "$TASK_MD")")/$(basename "$TASK_MD"), thinking OFF" "$RUN"
fi

# ------------------------------------------------------------------ 7. clone (+ prepare)
RUN_ID="$(basename "$RUN")_$(date +%H%M%S)"
WORK="$WORK_ROOT/$RUN_ID"; CLONE="$WORK/clone"
mkdir -p "$WORK"
# the marker prune_work.py requires before it removes anything: this dir was created by round.sh, for this run
printf 'run_dir=%s\npid=%s\ncreated=%s\n' "$RUN" "$$" "$(date '+%F %T')" > "$WORK/.spark_round_work"
echo "$WORK" > "$LOCK/work"
git clone -q --shared --no-checkout "$SRC" "$CLONE" > "$WORK/clone.out" 2>&1 \
  && git -C "$CLONE" checkout -q --detach "$TIP" >> "$WORK/clone.out" 2>&1 \
  || finish 5 "HARNESS — clone failed: $(tail -2 "$WORK/clone.out" | tr '\n' ' ')" "$RUN"
[ "$(git -C "$CLONE" rev-parse HEAD)" = "$TIP" ] || finish 5 "HARNESS — clone HEAD is not $TIP" "$RUN"
say "clone: $CLONE at ${TIP:0:12}"
if [ "$B_TIER" = code_patch ] || [ "$B_TIER" = code_patch2 ]; then
  bash "$LM/tasks/code_patch/prepare_clone.sh" "$RUN/input.json" "$CLONE" > "$RUN/prepare_clone.out" 2>&1 \
    || finish 5 "HARNESS — prepare_clone.sh failed: $(tail -2 "$RUN/prepare_clone.out" | tr '\n' ' ' | cut -c1-240)" "$RUN"
  say "prepare: $(grep -m1 'shared built' "$RUN/prepare_clone.out" || tail -1 "$RUN/prepare_clone.out")"
fi

# ------------------------------------------------------------------ 8. model (thinking OFF) — or the golden (--control)
if [ "$CONTROL" -eq 1 ]; then
  { printf '```diff\n'; cat "$B_GOLDEN"; printf '```\n'; } > "$RUN/out.md"
  echo "control: out.md = $B_GOLDEN fenced (no model call)" > "$RUN/run.log"
  say "control: out.md is the golden, fenced"
else
LM_BACKEND=spark SPARK_URL="$SPARK_URL" SPARK_THINK=0 bash "$LM/local_model_task.sh" "$TASK_MD" "$RUN/input.json" "$RUN/out.md" 2> "$RUN/run.log"; MRC=$?
if [ "$MRC" -ne 0 ]; then
  EP2="$(curl -s -m 10 -o /dev/null -w '%{http_code}' "$SPARK_URL/v1/models" 2>&1)"
  if [ "$EP2" != "200" ]; then finish 4 "ENDPOINT DOWN — the model call failed rc $MRC and $SPARK_URL/v1/models now answers '$EP2': $(tail -1 "$RUN/run.log" | cut -c1-200)" "$RUN"; fi
  finish 5 "HARNESS — model call failed rc $MRC (endpoint still up): $(tail -1 "$RUN/run.log" | cut -c1-240)" "$RUN"
fi
THINK_BAD="$(python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); print("" if (not m.get("think_field_requested") and not m.get("thinking_chars") and not m.get("think_leak_in_content")) else "thinking was ON or leaked")' "$RUN/out.md.meta.json" 2>&1)"
[ -z "$THINK_BAD" ] || finish 5 "HARNESS — $THINK_BAD (meta: $RUN/out.md.meta.json); coding runs with thinking OFF" "$RUN"
say "model: $(tail -1 "$RUN/run.log" | cut -c1-200)"
fi

# ------------------------------------------------------------------ 9. checker
if [ "$B_TIER" = code_patch ]; then
  bash "$LM/tasks/code_patch/spark_checker.sh" "$RUN/input.json" "$RUN/out.md" "$CLONE" > "$RUN/checker.out" 2>&1; CRC=$?
else
  bash "$LM/tasks/$B_TIER/checker.sh" "$RUN/input.json" "$RUN/out.md" "$CLONE" > "$RUN/checker.out" 2>&1; BCRC=$?
  REP="$RUN/out.md.checker"
  # A2a for bash_patch — the leg the bash checker lacks (IMPROVEMENTS 2026-09-30 02:40, 2026-10-05 02:3x), run exactly
  # as it was run by hand on 09-30 and 10-05: sections.json + a 1-based `n`, then code_patch/a2a_anchor.py.
  if [ -f "$REP/sections.json" ]; then
    python3 -c 'import json,sys; s=json.load(open(sys.argv[1])); [d.__setitem__("n", i+1) for i, d in enumerate(s)]; json.dump(s, open(sys.argv[2], "w"))' "$REP/sections.json" "$REP/sections_with_n.json"
    python3 "$LM/tasks/code_patch/a2a_anchor.py" "$RUN/input.json" "$CLONE" "$REP/sections_with_n.json" > "$REP/a2a_anchor.out" 2>&1; ARC=$?
  else
    echo "no sections.json — the checker stopped before splitting the diff" > "$REP/a2a_anchor.out"; ARC=5
  fi
  SUMLINE="$(grep -m1 '^SUMMARY' "$REP/a2a_anchor.out" 2>/dev/null)"
  {
    if [ "$ARC" -eq 0 ]; then echo "PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip ($SUMLINE)"
    elif [ "$ARC" -eq 1 ]; then echo "FAIL A2a ANCHOR: a hunk's header does NOT name the line its old side sits at: $(grep -m2 '^BAD' "$REP/a2a_anchor.out" | tr '\n' ' ' | cut -c1-400) ($SUMLINE)"
    elif [ "$ARC" -eq 5 ]; then echo "INFO A2a skipped — $(head -1 "$REP/a2a_anchor.out")"
    else echo "FAIL A2a ANCHOR MEASURE ERROR (rc=$ARC): $(head -2 "$REP/a2a_anchor.out" | tr '\n' ' ')"; fi
    if [ "$BCRC" -eq 0 ] && [ "$ARC" -eq 0 ]; then echo "SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)"
    else echo "SPARK RESULT: FAIL (checker rc=$BCRC; A2a rc=$ARC)"; fi
  } >> "$RUN/checker.out"
  if [ "$BCRC" -eq 0 ] && [ "$ARC" -eq 0 ]; then CRC=0; else CRC=1; fi
fi
RESULT="$(grep -m1 '^RESULT:' "$RUN/checker.out" | cut -c9-)"
SRESULT="$(grep -m1 '^SPARK RESULT:' "$RUN/checker.out" | cut -c15-)"

# ------------------------------------------------------------------ 10. golden + record
GOLD="none"
if [ -n "$B_GOLDEN" ] && [ -f "$RUN/out.md.checker/patch.diff" ]; then
  if cmp -s "$RUN/out.md.checker/patch.diff" "$B_GOLDEN"; then GOLD="BYTE-IDENTICAL"; else GOLD="DIFFERS"; fi
elif [ -n "$B_GOLDEN" ]; then GOLD="no-patch"; fi
if [ "$CRC" -eq 0 ]; then VERDICT=PASS; else VERDICT=FAIL; fi
[ "$CONTROL" -eq 1 ] && VERDICT="CONTROL-$VERDICT"
WALL=$(( $(date +%s) - T0 ))
python3 - "$RUN" "$VERDICT" "$WALL" "$TIP" "$B_TIER" "$BDIR" "$GOLD" "$WORK" "${RESULT:-}" "${SRESULT:-}" "${B_PINS:-}" "${B_OVERRIDE_NOT_RUNNABLE:-}" <<'PY'
import json, os, sys
run, verdict, wall, tip, tier, bdir, gold, work, result, sresult, pins, override = sys.argv[1:13]
m = {}
try: m = json.load(open(os.path.join(run, "out.md.meta.json")))
except Exception: pass
u = m.get("usage") or {}
json.dump({"verdict": verdict, "tier": tier, "brief_dir": bdir, "pins": pins, "tip": tip, "golden": gold,
           "checker_result": result, "spark_result": sresult, "round_wall_s": int(wall),
           "model_wall_s": m.get("wall_clock_seconds"), "prompt_tokens": u.get("prompt_tokens"),
           "completion_tokens": u.get("completion_tokens"), "finish_reason": m.get("finish_reason"),
           "model": m.get("model"), "work_dir": work,
           "override_not_runnable": override or None}, open(os.path.join(run, "round.json"), "w"), indent=1)
PY
MW="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print("no model (control)" if d.get("model_wall_s") is None else "%ss model, %s+%s tok" % (d.get("model_wall_s"), d.get("prompt_tokens"), d.get("completion_tokens")))' "$RUN/round.json")"
finish "$([ "$CRC" -eq 0 ] && echo 0 || echo 1)" "$VERDICT — ${SRESULT:-$RESULT} · golden $GOLD · tip ${TIP:0:12} · ${WALL}s round, $MW · $RUN" "$RUN"
