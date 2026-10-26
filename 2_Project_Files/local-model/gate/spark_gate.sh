#!/usr/bin/env bash
# spark_gate.sh — DETERMINISTIC half of the Spark QA gate (no LLM anywhere in this file).
#
# usage: spark_gate.sh <repo-clone> <pr-number> <head-sha> <base-ref> <test-file>... [--runner "cmd"] [--work DIR] [--out DIR]
#   <repo-clone>  an existing clone (scratch dir; this script fetches into it and adds worktrees under --work)
#   <head-sha>    the 40-char sha the gate is FOR. Must equal the tip of refs/pull/<n>/head, or be a commit in that PR's
#                 history (a superseded round) — anything else REFUSES (exit 3).
#   <base-ref>    branch name or sha the PR targets (e.g. develop). The diff is against merge-base(head, base).
#   <test-file>   repo-relative test files to run on BASE product code and on HEAD. A missing file REFUSES (exit 4).
#   --runner      command prefix that runs pytest, default "python3 -m pytest" (e.g. "/path/venv/bin/python -m pytest").
#   --node-modules DIR   (non-pytest mode) symlinked as node_modules into the vitest package dir of the head worktree.
# SUITE KINDS (2026-10-26): all <test-file>s *.py -> the pytest path below. All non-.py (*.sh -> `/bin/bash <file>`;
#   *.test.ts/tsx -> `npx vitest run <file>`, jest if the package has jest.config.js) -> this script does the same fetch / head
#   assertion / missing-file refusal / diff, then HANDS OFF to shadow_facts.py (the one non-pytest harness; it was NOT forked)
#   which runs the files on HEAD and on BASE product code and writes facts.json with per-file rc/passed/failed and totals.
#   Mixing .py and non-.py files in one call REFUSES (exit 2).
# Exit: 0 facts.json written · 2 usage · 3 head-sha mismatch · 4 test not found / 0 tests collected · 5 git failure.
# Writes <out>/facts.json, diff.patch, targeted_{base,head}.log, unit_{base,head}.log, lint.log.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
die() { echo "spark_gate: $2" >&2; exit "$1"; }

[ $# -ge 5 ] || die 2 "usage: spark_gate.sh <repo-clone> <pr> <head-sha> <base-ref> <test-file>... [--runner cmd] [--work DIR] [--out DIR]"
REPO="$1"; PR="$2"; HEAD_SHA="$3"; BASE_REF="$4"; shift 4
TESTS=(); RUNNER="python3 -m pytest"; WORK=""; OUT=""; NODE_MODULES=""
while [ $# -gt 0 ]; do
  case "$1" in
    --runner) RUNNER="$2"; shift 2;;
    --work) WORK="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    --node-modules) NODE_MODULES="$2"; shift 2;;
    *) TESTS+=("$1"); shift;;
  esac
done
[ ${#TESTS[@]} -ge 1 ] || die 2 "at least one test file is required"
NPY=0; for t in "${TESTS[@]}"; do case "$t" in *.py) ;; *) NPY=$((NPY+1));; esac; done
[ $NPY -eq 0 ] || [ $NPY -eq ${#TESTS[@]} ] || die 2 "mixed .py and non-.py test files in one call; run the gate once per kind"
case "$PR" in ''|*[!0-9]*) die 2 "PR number must be digits";; esac
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || die 2 "head-sha must be a full 40-char sha"
[ -d "$REPO/.git" ] || die 2 "$REPO is not a git clone"
STAMP="$(date +%Y%m%d-%H%M%S)"
[ -n "$WORK" ] || WORK="$(dirname "$REPO")/work_pr${PR}_${HEAD_SHA:0:8}_$STAMP"
[ -n "$OUT" ] || OUT="$WORK/out"
case "$(cd "$(dirname "$WORK")" 2>/dev/null && pwd)/" in /Volumes/DevMASTER/WEDNESDAY/*) die 2 "refusing to work with a cwd under /Volumes/DevMASTER/WEDNESDAY";; esac
[ ! -e "$WORK" ] || die 2 "work dir $WORK exists (this script never deletes); pass a fresh --work"
mkdir -p "$WORK" "$OUT" || die 5 "cannot create $WORK"
T0=$(date +%s)

# ---- 1. fetch the PR ref and ASSERT the head sha ------------------------------------------------------------------
git -C "$REPO" fetch -q origin "refs/pull/$PR/head" || die 5 "fetch refs/pull/$PR/head failed"
TIP="$(git -C "$REPO" rev-parse FETCH_HEAD)"
MODE="tip"
if [ "$TIP" != "$HEAD_SHA" ]; then
  if git -C "$REPO" cat-file -e "$HEAD_SHA^{commit}" 2>/dev/null && git -C "$REPO" merge-base --is-ancestor "$HEAD_SHA" "$TIP"; then
    MODE="historic-round (head-sha is an ancestor of the current PR tip $TIP)"
  else
    die 3 "REFUSE: head sha mismatch — asked for $HEAD_SHA but refs/pull/$PR/head is $TIP and the asked sha is not in its history"
  fi
fi
git -C "$REPO" fetch -q origin "$BASE_REF" 2>/dev/null || true
if git -C "$REPO" rev-parse -q --verify "origin/$BASE_REF^{commit}" >/dev/null; then BASE_TIP="$(git -C "$REPO" rev-parse "origin/$BASE_REF")"
elif git -C "$REPO" rev-parse -q --verify "$BASE_REF^{commit}" >/dev/null; then BASE_TIP="$(git -C "$REPO" rev-parse "$BASE_REF^{commit}")"
else die 5 "cannot resolve base ref $BASE_REF"; fi
MB="$(git -C "$REPO" merge-base "$HEAD_SHA" "$BASE_TIP")" || die 5 "no merge-base"
echo "spark_gate: head $HEAD_SHA ($MODE) · merge-base $MB · base tip $BASE_TIP"

# ---- 2. test files must exist at head (a test that cannot be found REFUSES) -----------------------------------------
for t in "${TESTS[@]}"; do
  git -C "$REPO" cat-file -e "$HEAD_SHA:$t" 2>/dev/null || die 4 "REFUSE: test file $t does not exist at $HEAD_SHA — not reporting 0, not running"
done

# ---- 3. diff, touched files, classification --------------------------------------------------------------------------
git -C "$REPO" diff "$MB" "$HEAD_SHA" > "$OUT/diff.patch"
git -C "$REPO" diff --numstat "$MB" "$HEAD_SHA" > "$OUT/numstat.txt"
git -C "$REPO" diff --name-status "$MB" "$HEAD_SHA" > "$OUT/namestatus.txt"
[ -s "$OUT/namestatus.txt" ] || die 5 "empty diff between merge-base and head"
for t in "${TESTS[@]}"; do
  grep -q "[[:space:]]$t\$" "$OUT/namestatus.txt" || echo "spark_gate: WARNING named test file $t is not in the diff (unchanged by the PR)" >&2
done
# ---- 3b. kind: pytest vs everything else ------------------------------------------------------------------------------
if [ $NPY -gt 0 ]; then
  git -C "$REPO" worktree add -q --detach "$WORK/head" "$HEAD_SHA" || die 5 "worktree head"
  NMARG=(); [ -z "$NODE_MODULES" ] || NMARG=(--node-modules "$NODE_MODULES")
  python3 "$HERE/shadow_facts.py" "$WORK/head" "$REPO" "$PR" "$HEAD_SHA" "$BASE_REF" "$OUT" --tests "${TESTS[@]}" ${NMARG[@]+"${NMARG[@]}"} > "$OUT/shadow_facts.stdout" 2>&1; RC=$?
  [ -f "$OUT/facts.json" ] || { tail -20 "$OUT/shadow_facts.stdout" >&2; die 5 "shadow_facts.py produced no facts.json (rc=$RC)"; }
  python3 - "$OUT/facts.json" <<'PY2'
import json, sys
f = json.load(open(sys.argv[1]))
print("spark_gate: head", f["head_sha"], f["head_mode"], "· merge-base", f["merge_base"], "· diff", f["diff_stat"])
print("spark_gate: targeted on HEAD:", f["targeted_head_totals"]); print("spark_gate: targeted on BASE product code:", f["targeted_base_totals"])
PY2
  echo "spark_gate: non-pytest facts -> $OUT/facts.json ($(( $(date +%s) - T0 ))s)"; exit 0
fi
# package dir = nearest dir with pyproject.toml above the first test file
PKG=""; d="$(dirname "${TESTS[0]}")"
while [ "$d" != "." ] && [ "$d" != "/" ]; do
  if git -C "$REPO" cat-file -e "$HEAD_SHA:$d/pyproject.toml" 2>/dev/null; then PKG="$d"; break; fi
  d="$(dirname "$d")"
done
[ -n "$PKG" ] || die 4 "no pyproject.toml above ${TESTS[0]}"

# ---- 4. worktrees: head, and base = merge-base (pure develop product + develop tests) ------------------------------
git -C "$REPO" worktree add -q --detach "$WORK/head" "$HEAD_SHA" || die 5 "worktree head"
git -C "$REPO" worktree add -q --detach "$WORK/base" "$MB" || die 5 "worktree base"

PYBIN="${RUNNER%% *}"
REQ=(); for t in "${TESTS[@]}"; do REQ+=(--require-file "${t#$PKG/}"); done
run_pytest() {  # $1 worktree  $2 label  $3.. pytest targets (relative to package dir)
  local wt="$1" label="$2"; shift 2
  ( cd "$wt/$PKG" && PYTHONPATH="$wt/$PKG" $RUNNER --rootdir="$wt/$PKG" -c pyproject.toml -p no:cacheprovider --no-cov -q \
      --tb=short -o junit_family=xunit1 --junitxml="$OUT/$label.xml" "$@" > "$OUT/$label.log" 2>&1 )
  local rc=$?
  echo "spark_gate: $label pytest rc=$rc"
  [ -f "$OUT/$label.xml" ] || { tail -20 "$OUT/$label.log" >&2; die 4 "REFUSE: $label produced no junit report"; }
}
REL=(); for t in "${TESTS[@]}"; do REL+=("${t#$PKG/}"); done

# ---- 5. unit suite BEFORE (pure merge-base tree) and targeted tests on BASE product code ------------------------------
run_pytest "$WORK/base" unit_base tests/unit
python3 "$HERE/gate_facts.py" junit "$OUT/unit_base.xml" "$OUT/unit_base.json" || die 4 "unit_base unreadable/empty"
# swap ONLY the product files back: base tree + the PR's test files copied over from head
for t in "${TESTS[@]}"; do mkdir -p "$(dirname "$WORK/base/$t")"; cp "$WORK/head/$t" "$WORK/base/$t"; done
run_pytest "$WORK/base" targeted_base "${REL[@]}"
python3 "$HERE/gate_facts.py" junit "$OUT/targeted_base.xml" "$OUT/targeted_base.json" "${REQ[@]}" || die 4 "targeted_base: test not found / 0 tests"

# ---- 6. HEAD ----------------------------------------------------------------------------------------------------------
run_pytest "$WORK/head" targeted_head "${REL[@]}"
python3 "$HERE/gate_facts.py" junit "$OUT/targeted_head.xml" "$OUT/targeted_head.json" "${REQ[@]}" || die 4 "targeted_head: test not found / 0 tests"
run_pytest "$WORK/head" unit_head tests/unit
python3 "$HERE/gate_facts.py" junit "$OUT/unit_head.xml" "$OUT/unit_head.json" || die 4 "unit_head unreadable/empty"

# ---- 7. lint on touched .py files at head ---------------------------------------------------------------------------
PYFILES=(); while IFS=$'\t' read -r st f _; do case "$st" in D*) ;; *) case "$f" in *.py) PYFILES+=("${f#$PKG/}");; esac;; esac; done < "$OUT/namestatus.txt"
: > "$OUT/lint.log"; RUFF_RC="n/a"; FMT_RC="n/a"; MYPY_RC="n/a"
if [ ${#PYFILES[@]} -gt 0 ]; then
  ( cd "$WORK/head/$PKG" && "$PYBIN" -m ruff check "${PYFILES[@]}" ) >> "$OUT/lint.log" 2>&1; RUFF_RC=$?
  ( cd "$WORK/head/$PKG" && "$PYBIN" -m ruff format --check "${PYFILES[@]}" ) >> "$OUT/lint.log" 2>&1; FMT_RC=$?
  ( cd "$WORK/head/$PKG" && "$PYBIN" -m mypy tests/ ) >> "$OUT/lint.log" 2>&1; MYPY_RC=$?
fi

# ---- 8. facts.json ---------------------------------------------------------------------------------------------------
python3 - "$OUT" "$PR" "$HEAD_SHA" "$TIP" "$MODE" "$MB" "$BASE_REF" "$BASE_TIP" "$PKG" "$RUFF_RC" "$FMT_RC" "$MYPY_RC" "$(( $(date +%s) - T0 ))" "${TESTS[@]}" <<'PY'
import json, sys, os
out, pr, head, tip, mode, mb, bref, btip, pkg, ruff, fmt, mypy, secs, *tests = sys.argv[1:]
J = lambda n: json.load(open(f"{out}/{n}.json"))
tb, th, ub, uh = J("targeted_base"), J("targeted_head"), J("unit_base"), J("unit_head")
touched, nums = [], {}
for l in open(f"{out}/namestatus.txt"):
    p = l.rstrip("\n").split("\t"); touched.append({"status": p[0], "path": p[-1]})
for l in open(f"{out}/numstat.txt"):
    a, d, f = l.rstrip("\n").split("\t"); nums[f] = {"added": a, "deleted": d}
for t in touched: t.update(nums.get(t["path"], {}))
is_test = lambda p: p in tests or os.path.basename(p).startswith("test_")
bn = {f["name"] for f in ub["failing"]}; hn = {f["name"] for f in uh["failing"]}
lint = open(f"{out}/lint.log").read()
facts = {
 "pr": int(pr), "head_sha": head, "pr_tip_now": tip, "head_mode": mode, "merge_base": mb, "base_ref": bref, "base_ref_tip_now": btip,
 "package_dir": pkg, "test_files": list(tests),
 "touched_files": touched,
 "product_files": [t["path"] for t in touched if not is_test(t["path"])],
 "diff_stat": {"files": len(touched), "added": sum(int(v["added"]) for v in nums.values()), "deleted": sum(int(v["deleted"]) for v in nums.values())},
 "targeted_on_base_product_code": tb, "targeted_on_head": th,
 "unit_suite_before": {k: ub[k] for k in ("tests","passed","failed","errors","skipped")},
 "unit_suite_after": {k: uh[k] for k in ("tests","passed","failed","errors","skipped")},
 "unit_failing_before": sorted(bn), "unit_failing_after": sorted(hn),
 "unit_new_failures_vs_base": sorted(hn - bn), "unit_fixed_vs_base": sorted(bn - hn),
 "lint": {"ruff_check_rc": ruff, "ruff_format_check_rc": fmt, "mypy_rc": mypy, "output_tail": lint[-1500:]},
 "gate_seconds": int(secs),
 "not_run": ["live/integration runs", "security scan", "anything needing network or a deployed service"],
}
json.dump(facts, open(f"{out}/facts.json", "w"), indent=1)
print(json.dumps({k: facts[k] for k in ("head_sha","merge_base","diff_stat","unit_suite_before","unit_suite_after","unit_new_failures_vs_base")}))
print("targeted base:", {k: tb[k] for k in ("tests","passed","failed","errors")}, "head:", {k: th[k] for k in ("tests","passed","failed","errors")})
PY
RC=$?; echo "spark_gate: facts -> $OUT/facts.json (rc=$RC, $(( $(date +%s) - T0 ))s)"; exit $RC
