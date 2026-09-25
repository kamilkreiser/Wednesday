#!/usr/bin/env bash
# =============================================================================
# TESTS for run-shell-suites.sh (KS-731, QA FR-800-04)
# =============================================================================
# 148 lines of enforcement shipped with zero assertions. Its only appearance in
# any test file was a `cp` inside preflight_deps.test.sh's leg-1 fixture — and in
# that fixture tree it self-SKIPs (not a git checkout, rc 0), so THE REAL SCRIPT
# AND THE `exit 0` STUB THE COMMENT EXPLICITLY REJECTED ARE BEHAVIOURALLY
# IDENTICAL THERE. The stated reason for choosing the real script is the one
# thing that fixture cannot deliver.
#
# So this file gives it a REAL `git init` fixture, which is what makes the
# reachability verdict reachable at all. It also makes the runner self-hosting:
# this suite sits under one of the ROOTS it globs, so the runner runs it.
#
# Every case asserts the EXIT CODE, because that is what preflight branches on —
# same contract as check_slot_credentials.test.sh, same reason.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh
# =============================================================================

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="${RUNNER_SH:-$HERE/../run-shell-suites.sh}"
if [[ ! -f "$RUNNER" ]]; then
  echo "FATAL: run-shell-suites.sh not found at $RUNNER" >&2
  exit 2
fi

# The globbed roots, read FROM THE SCRIPT rather than retyped. A fixture that
# hardcodes its own copy passes when the script's contract changes, which is the
# shape of bug this file exists to catch.
# NOT `mapfile`: it is bash 4 and macOS ships bash 3.2, which is the KS-676 class
# this repo already has a ticket for. A while-read loop is the portable form and
# the portability suite agrees with it.
ROOTS=()
while IFS= read -r _root; do
  [ -n "$_root" ] && ROOTS+=("$_root")
done < <(sed -n '/^ROOTS=(/,/^)/p' "$RUNNER" | grep -oE '"[^"]+"' | tr -d '"')
if [[ "${#ROOTS[@]}" -eq 0 ]]; then
  echo "FATAL: could not read ROOTS out of $RUNNER" >&2
  exit 2
fi
PRIMARY_ROOT="${ROOTS[0]}"
SECOND_ROOT="${ROOTS[1]:-$PRIMARY_ROOT}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
PASS=0
FAIL=0

check() {   # $1 = label, $2 = expected, $3 = actual
  if [[ "$2" == "$3" ]]; then
    echo "  ok   $1 (=$3)"; PASS=$((PASS + 1))
  else
    echo "  FAIL $1 — expected $2, got $3"; FAIL=$((FAIL + 1))
  fi
}

# Build a REAL git repo with the runner in place. Committing is the point: the
# reachability check enumerates from `git ls-files`, so an uncommitted tree
# exercises nothing.
new_repo() {   # -> path
  local r; r="$(mktemp -d "$TMP/repo.XXXXXX")"
  mkdir -p "$r/$(dirname "$PRIMARY_ROOT")" "$r/$PRIMARY_ROOT" "$r/$SECOND_ROOT"
  mkdir -p "$r/Blockchain/Dev/scripts"
  cp "$RUNNER" "$r/Blockchain/Dev/scripts/run-shell-suites.sh"
  git -C "$r" init -q
  git -C "$r" config user.email "test@secuura.local"
  git -C "$r" config user.name  "KS-731 fixture"
  printf '#!/usr/bin/env bash\nexit 0\n' > "$r/.keep-marker"
  git -C "$r" add -A >/dev/null 2>&1
  git -C "$r" commit -qm init >/dev/null 2>&1
  printf '%s' "$r"
}

suite_at() {   # $1 = repo, $2 = path relative to repo, $3 = exit code the suite returns
  mkdir -p "$1/$(dirname "$2")"
  printf '#!/usr/bin/env bash\necho "fixture suite %s"\nexit %s\n' "$2" "$3" > "$1/$2"
}

commit_all() { git -C "$1" add -A >/dev/null 2>&1; git -C "$1" commit -qm t >/dev/null 2>&1; }

run_runner() {   # $1 = repo, $2... = args -> "<rc>"
  local r="$1"; shift
  ( cd "$r/Blockchain/Dev" && bash scripts/run-shell-suites.sh "$@" >/dev/null 2>&1 )
  printf '%s' "$?"
}

runner_out() {   # $1 = repo, $2... = args -> stdout+stderr
  local r="$1"; shift
  ( cd "$r/Blockchain/Dev" && bash scripts/run-shell-suites.sh "$@" 2>&1 )
}

echo "run-shell-suites.sh — the enforcement that had no test of its own"

# --- --check-unreached: the reachability contract -----------------------------

# The all-clear. Without this the FAIL cases below could all be satisfied by a
# script that simply refuses everything.
R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/inside.test.sh" 0; commit_all "$R"
check 'CONTROL: every tracked suite inside ROOTS -> rc 0' 0 "$(run_runner "$R" --check-unreached)"
check 'CONTROL: and it says so, naming the count' 1 \
  "$(runner_out "$R" --check-unreached | grep -c 'OK — all 1 tracked shell suite')"

# The enforcement itself: a TRACKED suite the glob cannot reach.
R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/inside.test.sh" 0
suite_at "$R" "somewhere/else/orphan.test.sh" 0; commit_all "$R"
check 'a tracked suite outside ROOTS -> rc 1' 1 "$(run_runner "$R" --check-unreached)"
check 'and the unreachable file is NAMED, not merely counted' 1 \
  "$(runner_out "$R" --check-unreached | grep -c 'somewhere/else/orphan.test.sh')"

# An UNTRACKED stray is not a suite the repo owns. This is the discriminator that
# proves the check enumerates from git rather than walking the worktree — without
# it, `git ls-files` and `find` would be indistinguishable here.
R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/inside.test.sh" 0; commit_all "$R"
suite_at "$R" "somewhere/else/untracked.test.sh" 0     # deliberately NOT committed
check 'an UNTRACKED stray outside ROOTS is ignored -> rc 0' 0 "$(run_runner "$R" --check-unreached)"

# THE POSITIVE CONTROL INSIDE THE SCRIPT, exercised. If the glob reaches nothing
# while git tracks suites, `comm` would report every suite as unreached — a
# dramatic-looking finding that is really the script being broken. It must say
# which of the two it is.
R="$(new_repo)"; suite_at "$R" "somewhere/else/only.test.sh" 0; commit_all "$R"
rmdir "$R/$PRIMARY_ROOT" "$R/$SECOND_ROOT" 2>/dev/null
check 'glob reaches 0 while git tracks N -> rc 1' 1 "$(run_runner "$R" --check-unreached)"
check 'and it blames ITSELF, not the wiring' 1 \
  "$(runner_out "$R" --check-unreached | grep -c 'the glob reached 0 suites while git tracks')"

# The SKIP arm, asserted so it cannot quietly become a plain pass. It is rc 0 by
# design in a non-git tree — the label is the only thing distinguishing it from a
# measured all-clear, so the label is what this case pins.
R="$(mktemp -d "$TMP/nogit.XXXXXX")"; mkdir -p "$R/Blockchain/Dev/scripts"
cp "$RUNNER" "$R/Blockchain/Dev/scripts/run-shell-suites.sh"
check 'a non-git tree SKIPs advisorily -> rc 0' 0 "$(run_runner "$R" --check-unreached)"
check 'and it SAYS it skipped, so rc 0 is not read as a measurement' 1 \
  "$(runner_out "$R" --check-unreached | grep -c 'SKIP (advisory)')"

# --- run mode -----------------------------------------------------------------

R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/green.test.sh" 0; commit_all "$R"
check 'run mode, every suite green -> rc 0' 0 "$(run_runner "$R")"

R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/green.test.sh" 0
suite_at "$R" "$PRIMARY_ROOT/red.test.sh" 1; commit_all "$R"
check 'run mode propagates a RED suite -> rc 1' 1 "$(run_runner "$R")"
check 'and names the suite that failed' 1 \
  "$(runner_out "$R" | grep -c 'FAILED: .*red.test.sh')"

# Refusing to report success on an empty run. A runner that finds nothing and
# exits 0 is the exact failure this whole mechanism exists to prevent.
#
# THE RC ALONE IS NOT LOAD-BEARING HERE, and this is measured rather than
# assumed. Removing the refusal makes the script reach `"${reached[@]}"` with an
# empty array, which under bash 3.2 + `set -u` is an UNBOUND VARIABLE error and
# exits 1 anyway. So `rc 1` is satisfied by a CRASH as readily as by a refusal:
# a tamper that deleted the guard left an rc-only assertion green. The verdict
# and the status are asserted together so the two states are distinguishable.
empty_run_verdict() {   # $1 = repo -> "REFUSED/<rc>" | "RAN/<rc>" | "CRASHED/<rc>"
  local out rc
  out=$(runner_out "$1")
  rc=$?
  if printf '%s' "$out" | grep -q 'no shell suites found'; then
    printf 'REFUSED/%s' "$rc"
  elif printf '%s' "$out" | grep -q 'unbound variable'; then
    printf 'CRASHED/%s' "$rc"
  else
    printf 'RAN/%s' "$rc"
  fi
}
R="$(new_repo)"
check 'run mode with NO suites REFUSES (not crashes, not passes)' REFUSED/1 "$(empty_run_verdict "$R")"

# --- QA R2-2: check mode had NO empty-run refusal at all ----------------------
#
# Run mode has refused an empty run since it was written. Check mode did not,
# and the gap produced a green that meant nothing on the leg the pre-push hook
# actually calls (preflight leg 12).
#
# With ZERO tracked suites the script did all three of these in one run:
#   1. hit `"${reached[@]}"` on an empty array under `set -u` — bash 3.2, which
#      is what macOS ships — raising "unbound variable" INSIDE a command
#      substitution, where the error goes to stderr and nothing reads it;
#   2. skipped the broken-glob guard, which requires tracked_count > 0;
#   3. printed "OK — all 0 tracked shell suite(s) are reached" and exited 0.
#
# THE ORACLE IS DELIBERATELY NOT `rc 1`, and that is the whole lesson from the
# run-mode case above: deleting the new refusal puts the script back on the
# unbound-variable path, which ALSO exits non-zero. An rc-only assertion is
# satisfied by a crash as readily as by a refusal, and would have gone green
# against the very defect it names. Verdict and status are asserted together.
empty_check_verdict() {   # $1 = repo -> "REFUSED/<rc>" | "OK-ZERO/<rc>" | "CRASHED/<rc>"
  local out rc
  out=$(runner_out "$1" --check-unreached)
  rc=$?
  if printf '%s' "$out" | grep -q 'unbound variable'; then
    printf 'CRASHED/%s' "$rc"
  elif printf '%s' "$out" | grep -q 'reaches no shell suites at all'; then
    printf 'REFUSED/%s' "$rc"
  elif printf '%s' "$out" | grep -q 'OK — all 0'; then
    printf 'OK-ZERO/%s' "$rc"
  else
    printf 'OTHER/%s' "$rc"
  fi
}
R="$(new_repo)"
check 'check mode with NO suites REFUSES (not crashes, not "OK — all 0")' REFUSED/1 \
  "$(empty_check_verdict "$R")"

# The emitted-and-discarded half, asserted separately because it is a different
# defect from the verdict: even when the verdict is right, a runtime error the
# script prints and ignores is a fault. Zero occurrences, on the fixture that
# used to produce one.
R="$(new_repo)"
check 'check mode emits NO discarded runtime error on an empty tree' 0 \
  "$(runner_out "$R" --check-unreached | grep -c 'unbound variable')"

# CONTROL: the same probe on a POPULATED tree must still pass, so the refusal
# above cannot be satisfied by a script that refuses everything.
R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/inside.test.sh" 0; commit_all "$R"
check 'CONTROL: with a tracked suite in ROOTS, check mode still passes' 0 \
  "$(run_runner "$R" --check-unreached)"

# --- argument handling --------------------------------------------------------

R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/inside.test.sh" 0; commit_all "$R"
check '--list prints the reached suites' 1 \
  "$(runner_out "$R" --list | grep -c "$PRIMARY_ROOT/inside.test.sh")"
check '--list does not RUN them' 0 \
  "$(runner_out "$R" --list | grep -c 'fixture suite')"
check 'an unknown argument is rejected -> rc 2' 2 "$(run_runner "$R" --nonsense)"

# --- KS-1086: run mode must not hand a suite the CALLER's git environment ------
#
# Preflight leg 14 runs this runner inside the pre-push hook. Pushed from a
# linked worktree, git exports GIT_DIR=<repo>/.git/worktrees/<name> to that
# hook; every suite inherited it, and the suites' fixture git calls rewrote the
# SHARED repository's config and refs (s176, 2026-09-11). These cells rebuild
# that exact shape in scratch — a real repo, a real linked worktree, its gitdir
# exported — and assert the shared repo comes out byte-identical.
#
# Ordered so that a green cannot mean "nothing happened": the first CONTROL
# proves the fixture really does the damage without the runner, REACH proves it
# really ran under the runner, and the run-mode CONTROL proves the check-mode
# fixture can run at all.

shared_repo() {   # -> "<repo>|<its linked worktree's gitdir>"
  local s gd
  s="$(mktemp -d "$TMP/shared.XXXXXX")"
  git -C "$s" init -q
  git -C "$s" -c user.name=shared -c user.email=shared@secuura.local commit -q --allow-empty -m base
  git -C "$s" worktree add -q --detach "$s-wt" HEAD >/dev/null 2>&1
  gd="$(git -C "$s-wt" rev-parse --absolute-git-dir)"
  printf '%s|%s' "$s" "$gd"
}

writer_suite_at() {   # $1 = dir, $2 = path relative to it, $3 = marker the suite touches when it runs
  mkdir -p "$1/$(dirname "$2")"
  cat > "$1/$2" <<EOF
#!/usr/bin/env bash
# The incident's fixture shape: git state written in the suite's OWN temp dir.
d="\$(mktemp -d "$TMP/writer.XXXXXX")"
cd "\$d" || exit 1
: > "$3"
git init -q .
git config user.email t@e.com
git -c user.name=t -c user.email=t@e.com commit -q --allow-empty -m fixture
git branch fixture-branch
git config core.bare true
exit 0
EOF
}

# Without the runner, the fixture does the damage. If this ever reads identical,
# every identity cell below is green for the wrong reason.
IFS='|' read -r K_CTL_REPO K_CTL_GITDIR <<< "$(shared_repo)"
cp "$K_CTL_REPO/.git/config" "$TMP/k1086-ctl.config"
writer_suite_at "$TMP" "k1086-direct/writer.test.sh" "$TMP/k1086-direct.ran"
( GIT_DIR="$K_CTL_GITDIR" bash "$TMP/k1086-direct/writer.test.sh" ) >/dev/null 2>&1
check 'CONTROL: the writer suite run DIRECTLY under a worktree GIT_DIR rewrites the shared config' CHANGED \
  "$(cmp -s "$K_CTL_REPO/.git/config" "$TMP/k1086-ctl.config" && echo identical || echo CHANGED)"

# The same fixture, run BY THE RUNNER under the same inherited GIT_DIR.
IFS='|' read -r K_REPO K_GITDIR <<< "$(shared_repo)"
cp "$K_REPO/.git/config" "$TMP/k1086.config"
git -C "$K_REPO" for-each-ref > "$TMP/k1086.refs"
R="$(new_repo)"; writer_suite_at "$R" "$PRIMARY_ROOT/writer.test.sh" "$TMP/k1086-runner.ran"; commit_all "$R"
K_OUT="$( cd "$R/Blockchain/Dev" && GIT_DIR="$K_GITDIR" bash scripts/run-shell-suites.sh 2>&1 )"
check 'run mode under an inherited worktree GIT_DIR leaves the shared config byte-identical' identical \
  "$(cmp -s "$K_REPO/.git/config" "$TMP/k1086.config" && echo identical || echo CHANGED)"
check 'and leaves the shared refs identical' identical \
  "$(git -C "$K_REPO" -c core.bare=false for-each-ref | cmp -s - "$TMP/k1086.refs" && echo identical || echo CHANGED)"
check 'REACH: the writer suite really ran under the runner' 1 \
  "$([ -e "$TMP/k1086-runner.ran" ] && echo 1 || echo 0)"
check 'and the runner names GIT_DIR among the variables it cleared' 1 \
  "$(printf '%s\n' "$K_OUT" | grep -c '^git environment: cleared for the suites: .*GIT_DIR')"

# Leg 12 calls --check-unreached; only leg 14's run mode may execute a suite.
R="$(new_repo)"; writer_suite_at "$R" "$PRIMARY_ROOT/writer.test.sh" "$TMP/k1086-check.ran"; commit_all "$R"
run_runner "$R" --check-unreached >/dev/null
check 'leg 12 path: --check-unreached RUNS no suite' 0 \
  "$([ -e "$TMP/k1086-check.ran" ] && echo 1 || echo 0)"
run_runner "$R" >/dev/null
check 'CONTROL: run mode on the same tree does run it' 1 \
  "$([ -e "$TMP/k1086-check.ran" ] && echo 1 || echo 0)"

# When git cannot be asked for its list, refuse BEFORE any suite runs. Verdict,
# status and reach together: a crash or a silent run would each satisfy one alone.
R="$(new_repo)"; writer_suite_at "$R" "$PRIMARY_ROOT/writer.test.sh" "$TMP/k1086-empty.ran"; commit_all "$R"
K_FAKEBIN="$(mktemp -d "$TMP/fakebin.XXXXXX")"
printf '#!/usr/bin/env bash\nexit 0\n' > "$K_FAKEBIN/git"; chmod +x "$K_FAKEBIN/git"
K_EMPTY="$( cd "$R/Blockchain/Dev" && PATH="$K_FAKEBIN:$PATH" bash scripts/run-shell-suites.sh 2>&1 )"; K_RC=$?
K_VERDICT=RAN
printf '%s\n' "$K_EMPTY" | grep -q 'could not ask git which variables' && K_VERDICT=REFUSED
check 'an empty --local-env-vars list REFUSES before any suite runs (verdict/rc/ran)' REFUSED/1/0 \
  "$K_VERDICT/$K_RC/$([ -e "$TMP/k1086-empty.ran" ] && echo 1 || echo 0)"

# --- KS-1086 round 2: the tier-1 gate's QA-1 and QA-2 --------------------------
#
# QA-1. The cells above pin GIT_DIR only, so cutting the runtime list down to
# GIT_DIR (the gate's tamper T8) left every cell green. Drive three names a push
# really hands the hook — GIT_DIR (a linked worktree), GIT_WORK_TREE (a
# `--git-dir/--work-tree` push) and GIT_CONFIG_PARAMETERS (a `git -c` push) — and
# assert the suite sees all three unset AND the verdict line names all three.
env_probe_suite_at() {   # $1 = repo, $2 = path relative to it, $3 = file the suite records what it saw in
  mkdir -p "$1/$(dirname "$2")"
  cat > "$1/$2" <<EOF
#!/usr/bin/env bash
for v in GIT_DIR GIT_WORK_TREE GIT_CONFIG_PARAMETERS; do
  if printenv "\$v" >/dev/null 2>&1; then echo "\$v=set"; else echo "\$v=unset"; fi
done > "$3"
exit 0
EOF
}
IFS='|' read -r K3_REPO K3_GITDIR <<< "$(shared_repo)"
R="$(new_repo)"; env_probe_suite_at "$R" "$PRIMARY_ROOT/probe.test.sh" "$TMP/k1086-three.seen"; commit_all "$R"
K3_OUT="$( cd "$R/Blockchain/Dev" && GIT_DIR="$K3_GITDIR" GIT_WORK_TREE="$K3_REPO-wt" \
  GIT_CONFIG_PARAMETERS="'qa.probe'='1'" bash scripts/run-shell-suites.sh 2>&1 )"
check 'QA-1: GIT_DIR, GIT_WORK_TREE and GIT_CONFIG_PARAMETERS all reach the suite UNSET' \
  'GIT_DIR=unset GIT_WORK_TREE=unset GIT_CONFIG_PARAMETERS=unset' \
  "$([ -f "$TMP/k1086-three.seen" ] && tr '\n' ' ' < "$TMP/k1086-three.seen" | sed 's/ $//')"
check 'QA-1: and the verdict line names all three as cleared' 3 \
  "$(printf '%s\n' "$K3_OUT" | grep '^git environment: cleared for the suites: ' | tr ' ' '\n' \
     | grep -cxE 'GIT_DIR|GIT_WORK_TREE|GIT_CONFIG_PARAMETERS')"

# QA-2. The refusal keyed on EMPTY TEXT, so a list from which no usable name parses
# passed it: the gate printed the real names with CRLF line endings, and the runner
# cleared nothing, exited 0 and ran the suites under the inherited GIT_DIR. Each
# fake git below answers `rev-parse --local-env-vars` and hands every other call to
# the real one. Each refusal is matched on the REASON it prints, so a refusal for
# some other cause cannot turn these cells green.
K_REALGIT="$(command -v git)"
K_CRLFBIN="$(mktemp -d "$TMP/crlfbin.XXXXXX")"
cat > "$K_CRLFBIN/git" <<EOF
#!/usr/bin/env bash
if [ "\${1:-}" = rev-parse ] && [ "\${2:-}" = --local-env-vars ]; then
  "$K_REALGIT" rev-parse --local-env-vars | awk '{ printf "%s\r\n", \$0 }'
  exit 0
fi
exec "$K_REALGIT" "\$@"
EOF
chmod +x "$K_CRLFBIN/git"
K_N_REAL=$("$K_REALGIT" rev-parse --local-env-vars | grep -c .)
K_N_CR=$("$K_CRLFBIN/git" rev-parse --local-env-vars | LC_ALL=C grep -c $'\r$')
check 'CONTROL: the CRLF fake git prints every name git lists, each ending in CR' "$K_N_REAL/$K_N_REAL" \
  "$([ "${K_N_REAL:-0}" -gt 0 ] && echo "$K_N_REAL/$K_N_CR" || echo no-names)"

IFS='|' read -r KC_REPO KC_GITDIR <<< "$(shared_repo)"
R="$(new_repo)"; writer_suite_at "$R" "$PRIMARY_ROOT/writer.test.sh" "$TMP/k1086-crlf.ran"; commit_all "$R"
K_CRLF="$( cd "$R/Blockchain/Dev" && GIT_DIR="$KC_GITDIR" PATH="$K_CRLFBIN:$PATH" bash scripts/run-shell-suites.sh 2>&1 )"; K_RC=$?
K_VERDICT=RAN
printf '%s\n' "$K_CRLF" | grep -qF 'with 0 usable name(s)' && K_VERDICT=REFUSED
check 'QA-2: a CRLF list that parses to no usable name REFUSES before any suite runs (verdict/rc/ran)' REFUSED/1/0 \
  "$K_VERDICT/$K_RC/$([ -e "$TMP/k1086-crlf.ran" ] && echo 1 || echo 0)"

K_NODIRBIN="$(mktemp -d "$TMP/nodirbin.XXXXXX")"
cat > "$K_NODIRBIN/git" <<EOF
#!/usr/bin/env bash
if [ "\${1:-}" = rev-parse ] && [ "\${2:-}" = --local-env-vars ]; then
  "$K_REALGIT" rev-parse --local-env-vars | grep -vx GIT_DIR
  exit 0
fi
exec "$K_REALGIT" "\$@"
EOF
chmod +x "$K_NODIRBIN/git"
R="$(new_repo)"; writer_suite_at "$R" "$PRIMARY_ROOT/writer.test.sh" "$TMP/k1086-nodir.ran"; commit_all "$R"
K_NODIR="$( cd "$R/Blockchain/Dev" && PATH="$K_NODIRBIN:$PATH" bash scripts/run-shell-suites.sh 2>&1 )"; K_RC=$?
K_VERDICT=RAN
printf '%s\n' "$K_NODIR" | grep -qE 'with [1-9][0-9]* usable name\(s\), GIT_DIR absent' && K_VERDICT=REFUSED
check 'QA-2: a list that parses but does not name GIT_DIR REFUSES before any suite runs (verdict/rc/ran)' REFUSED/1/0 \
  "$K_VERDICT/$K_RC/$([ -e "$TMP/k1086-nodir.ran" ] && echo 1 || echo 0)"

# --- KS-1089 QA-8 + QA-7, KS-1127 and KS-1135 ---------------------------------
#
# Four defects in this one runner, and one run of this file proves all four, which is
# what KS-1089 asked for. Ordered so a green cannot mean "nothing happened": every
# defect cell is paired with a CONTROL that goes red if the fix were written as an
# unconditional — a --list that prints nothing always, a headline that never varies, a
# tally that always says "skipped", a TMPDIR note that is always emitted.

suite_with() { # $1 = repo, $2 = path relative to repo, $3 = body line, $4 = exit code
  mkdir -p "$1/$(dirname "$2")"
  printf '#!/usr/bin/env bash\n%s\nexit %s\n' "$3" "$4" > "$1/$2"
}

# --- KS-1089 QA-8: `--list` on a tree with ZERO reached suites -----------------
# Under `set -u` on bash 3.2 — what macOS ships and the pre-push hook runs —
# `"${reached[@]}"` on an empty array raised "unbound variable" and rc 1, and the `exit 0`
# after it never ran. The assertion is in BYTES, deliberately: a `$(…)` capture reads
# empty for the guarded form AND for the `+alternate` form (which writes one newline), so
# a capture cannot tell them apart. Only a byte count can.
R="$(new_repo)"
check 'QA-8: --list on a tree with no reached suites exits 0' 0 "$(run_runner "$R" --list)"
check 'QA-8: ...and writes ZERO bytes, not a bare newline (measured in bytes, not by a capture)' 0 \
  "$( ( cd "$R/Blockchain/Dev" && bash scripts/run-shell-suites.sh --list 2>/dev/null ) | wc -c | tr -d ' ' )"
suite_at "$R" "$PRIMARY_ROOT/qa8-one.test.sh" 0; commit_all "$R"
check 'QA-8 CONTROL: --list with ONE suite still prints exactly one line, so the guard is not a no-op' 1 \
  "$( ( cd "$R/Blockchain/Dev" && bash scripts/run-shell-suites.sh --list 2>/dev/null ) | wc -l | tr -d ' ' )"

# --- KS-1089 QA-7: a headline per cause ---------------------------------------
# One headline served every cause and only the parenthetical named which; with git absent
# from PATH the output was identical to the empty-list case, and nothing said git was
# missing. Each cause now gets its own first line.
qa7_bin() { # $1 = the stub body for `rev-parse --local-env-vars`; -> a bin dir holding a git stub
  local b; b="$(mktemp -d "$TMP/qa7.XXXXXX")"
  cat > "$b/git" <<EOF
#!/usr/bin/env bash
if [ "\$1" = "rev-parse" ] && [ "\$2" = "--local-env-vars" ]; then $1; exit 0; fi
exec /usr/bin/git "\$@"
EOF
  chmod +x "$b/git"; printf '%s' "$b"
}
qa7_head() { # $1 = repo, $2 = bin dir to prepend, $3 = 1 to drop the rest of PATH
  local r="$1" b="$2" only="${3:-0}" p
  if [ "$only" = 1 ]; then p="$b"; else p="$b:$PATH"; fi
  ( cd "$r/Blockchain/Dev" && PATH="$p" bash scripts/run-shell-suites.sh 2>&1 | grep -m1 '^FAIL — ' )
}
R="$(new_repo)"; suite_at "$R" "$PRIMARY_ROOT/qa7.test.sh" 0; commit_all "$R"
check 'QA-7: git printed NOTHING -> the headline says git could not be asked' \
  'FAIL — could not ask git which variables are repository-local' \
  "$(qa7_head "$R" "$(qa7_bin 'true')")"
check 'QA-7: git printed a list with no GIT_DIR -> the headline says the list is UNUSABLE' \
  "FAIL — git's list of repository-local variables is unusable" \
  "$(qa7_head "$R" "$(qa7_bin 'echo GIT_INDEX_FILE; echo GIT_OBJECT_DIRECTORY')")"
# git absent: a PATH holding only the tools the runner needs, git NOT among them. The
# CONTROL below is what makes this cell mean anything — the same PATH WITH git symlinked in
# must let the runner get past this check, proving the PATH is otherwise sufficient.
qa7_nogit_bin() { # $1 = 1 to include git
  local b t; b="$(mktemp -d "$TMP/qa7ng.XXXXXX")"
  for t in bash sh comm env grep mktemp printenv rm sed sort tee cat wc tr chmod mkdir dirname basename ls; do
    if command -v "$t" >/dev/null 2>&1; then ln -sf "$(command -v "$t")" "$b/$t"; fi
  done
  [ "$1" = 1 ] && ln -sf "$(command -v git)" "$b/git"
  printf '%s' "$b"
}
check 'QA-7: git ABSENT from PATH -> the headline names git, not the list' \
  'FAIL — git is not on PATH, so its list of repository-local variables cannot be read' \
  "$(qa7_head "$R" "$(qa7_nogit_bin 0)" 1)"
check 'QA-7 CONTROL: the SAME minimal PATH with git in it gets past the check, so the cell above is about git and not about a broken PATH' \
  '' "$(qa7_head "$R" "$(qa7_nogit_bin 1)" 1)"

# --- KS-1127: an exit-0 SKIP is tallied as SKIPPED, not passed -----------------
# A suite that cannot run its cells prints `SKIP — …` and exits 0. Scored by exit code
# alone it read identically to one that ran every cell, and so did the verdict leg 14
# prints. Four suites: a real pass, a SKIP, a real failure, and a SILENT exit 0 — the last
# is the control that stops "skipped" being applied to every zero exit.
R="$(new_repo)"
suite_at   "$R" "$PRIMARY_ROOT/t1127-pass.test.sh" 0
suite_with "$R" "$PRIMARY_ROOT/t1127-skip.test.sh" \
  'echo "SKIP — no PostgreSQL binaries (initdb pg_ctl postgres psql) found; searched: /nowhere; 0/26 cells run"' 0
suite_at   "$R" "$PRIMARY_ROOT/t1127-fail.test.sh" 1
suite_with "$R" "$PRIMARY_ROOT/t1127-quiet.test.sh" ':' 0
commit_all "$R"
T1127_OUT="$(runner_out "$R")"
check 'KS-1127: the verdict carries a skipped count, and the SILENT exit 0 is still a pass' 1 \
  "$(printf '%s\n' "$T1127_OUT" | grep -c '^shell suites: 2 passed, 1 failed, 1 skipped (of 4)')"
check 'KS-1127: the skipped suite is NAMED' 1 \
  "$(printf '%s\n' "$T1127_OUT" | grep -c '^SKIPPED: .*t1127-skip\.test\.sh')"
check 'KS-1127: the failing suite is still named, and separately' 1 \
  "$(printf '%s\n' "$T1127_OUT" | grep -c '^FAILED: .*t1127-fail\.test\.sh')"
check 'KS-1127 CONTROL: a skip does not fail the runner on its own — the rc here is the real FAILURE' 1 \
  "$(run_runner "$R")"
# CONTROL: with no skipping suite the tally reads 0 skipped and prints no SKIPPED: block,
# so "skipped" is measured rather than always printed.
R2="$(new_repo)"; suite_at "$R2" "$PRIMARY_ROOT/t1127-only.test.sh" 0; commit_all "$R2"
T1127_CLEAN="$(runner_out "$R2")"
check 'KS-1127 CONTROL: a tree with nothing to skip reads 0 skipped' 1 \
  "$(printf '%s\n' "$T1127_CLEAN" | grep -c '^shell suites: 1 passed, 0 failed, 0 skipped (of 1)')"
check 'KS-1127 CONTROL: ...and prints no SKIPPED: block' 0 \
  "$(printf '%s\n' "$T1127_CLEAN" | grep -c '^SKIPPED:')"

# --- KS-1135: a long TMPDIR is named, not left as six anonymous reds -----------
# tsx binds its IPC socket at $TMPDIR/tsx-<uid>/<pid>.pipe and macOS refuses a sun_path
# over ~104 bytes (listen EINVAL). The #971 gate read 19 passed / 6 failed under a
# 123-character TMPDIR on a tree that reads 25/0 under a 28-character one.
T1135_LONG="$TMP/$(printf 'x%.0s' $(seq 1 120))"
mkdir -p "$T1135_LONG"
T1135_OUT="$( cd "$R2/Blockchain/Dev" && TMPDIR="$T1135_LONG" bash scripts/run-shell-suites.sh 2>&1 )"
# TWICE, and that is the assertion: once before the run and once beside the verdict. A note
# only at the top is buried under 58 suites of output, which is where a reader is not looking.
check 'KS-1135: a TMPDIR over 80 chars is NAMED as the cause TWICE — before the run and beside the verdict' 2 \
  "$(printf '%s\n' "$T1135_OUT" | grep -c 'TMPDIR was [0-9]* chars (> 80) — the suites ran under /tmp/rss\.')"
check 'KS-1135: ...and the run still reports its real verdict' 1 \
  "$(printf '%s\n' "$T1135_OUT" | grep -c '^shell suites: 1 passed, 0 failed, 0 skipped (of 1)')"
check 'KS-1135 CONTROL: a SHORT TMPDIR emits no such line, so the note is conditional' 0 \
  "$(printf '%s\n' "$( cd "$R2/Blockchain/Dev" && TMPDIR=/tmp bash scripts/run-shell-suites.sh 2>&1 )" | grep -c 'TMPDIR was')"
check 'KS-1135 CONTROL: the caller TMPDIR is restored, so the runner does not leak its substitute' "${#T1135_LONG}" \
  "$( cd "$R2/Blockchain/Dev" && TMPDIR="$T1135_LONG" bash -c 'bash scripts/run-shell-suites.sh >/dev/null 2>&1; printf "%s" "${#TMPDIR}"' )"

echo
echo "run_shell_suites: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
