#!/bin/bash
# Arms for filler/drain.sh. No Spark, no network (run_filler.py --stub-reply seam). All writes in a temp dir under $1 (default: mktemp -d under $TMPDIR).
# run: bash /abs/path/tests/test_drain.sh [scratch_dir]
T="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; F="$(cd "$T/.." && pwd)"
W="${1:-$(mktemp -d)}/drain_arms.$$"; mkdir -p "$W" || exit 2
pass=0; fail=0
ok()   { pass=$((pass+1)); echo "PASS: $1"; }
bad()  { fail=$((fail+1)); echo "FAIL: $1"; }
chk()  { if [ "$2" = "$3" ]; then ok "$1"; else bad "$1 (got '$2', want '$3')"; fi; }
HDR="# arms
id	kind	input	status	result"
ROW_Q="F08-numstat-pr2211	numstat	tasks/F08-numstat-pr2211.json	queued	"
ROW_Q2="F03-numstat-pr2209	numstat	tasks/F03-numstat-pr2209.json	queued	"
ROW_D="F04-numstat-pr2208	numstat	tasks/F04-numstat-pr2208.json	done_accepted	runs/x.json"
# a stub Spark reply: a claim JSON (checker verdict is data; any terminal status proves the row was run and marked)
cat > "$W/stub.md" <<'S'
{"pr": 2211, "files_changed": 2, "additions": 155, "deletions": 2, "files": [{"path": "Blockchain/Dev/services/kyc/src/index.ts", "additions": 4, "deletions": 2}]}
S
mk() { # dir rows... -> sets env for an isolated drain
  d="$W/$1"; mkdir -p "$d/state" "$d/runs"; shift
  printf '%s\n' "$HDR" > "$d/queue.tsv"; for r in "$@"; do printf '%s\n' "$r" >> "$d/queue.tsv"; done
}
env_for() { export FILLER_QUEUE="$W/$1/queue.tsv" FILLER_RUNS="$W/$1/runs" FILLER_LOG="$W/$1/runs.tsv" DRAIN_STATE="$W/$1/state"; }

# ARM 1: empty queue (only a done row) -> rc 0, fast, log says empty
mk a1 "$ROW_D"; env_for a1
s=$(date +%s); bash "$F/drain.sh" --stub-reply "$W/stub.md" 2>"$W/a1.err"; rc=$?; e=$(date +%s)
chk "arm1 empty queue rc 0" "$rc" 0
[ $((e-s)) -le 3 ] && ok "arm1 empty queue fast ($((e-s))s)" || bad "arm1 slow"
grep -q "	empty	" "$W/a1/state/drain.log" && ok "arm1 log has empty line" || bad "arm1 log"
[ -d "$W/a1/state/drain.lock" ] && bad "arm1 lock left behind" || ok "arm1 lock released"

# ARM 2: two stubbed queued rows -> both run + marked, rc 0, one 'ran' log line each, nothing queued after
mk a2 "$ROW_Q" "$ROW_Q2" "$ROW_D"; env_for a2
bash "$F/drain.sh" --stub-reply "$W/stub.md" 2>"$W/a2.err"; rc=$?
chk "arm2 drain rc 0" "$rc" 0
chk "arm2 no queued rows left" "$(awk -F'\t' '$4=="queued"' "$W/a2/queue.tsv" | wc -l | tr -d ' ')" 0
chk "arm2 two ran lines" "$(grep -c '	ran	' "$W/a2/state/drain.log")" 2
case "$(awk -F'\t' '$1=="F08-numstat-pr2211"{print $4}' "$W/a2/queue.tsv")" in done_*) ok "arm2 F08 marked done_*";; *) bad "arm2 F08 status";; esac
[ -f "$W/a2/runs.tsv" ] && ok "arm2 runs log written in temp (not the real one)" || bad "arm2 runs.tsv"

# ARM 3: live held lock -> refuse rc 5, row untouched, lock untouched
mk a3 "$ROW_Q"; env_for a3
sleep 30 & hp=$!
mkdir "$W/a3/state/drain.lock"; echo $hp > "$W/a3/state/drain.lock/pid"
bash "$F/drain.sh" --stub-reply "$W/stub.md" 2>"$W/a3.err"; rc=$?
chk "arm3 held lock rc 5" "$rc" 5
chk "arm3 row still queued" "$(awk -F'\t' '$1=="F08-numstat-pr2211"{print $4}' "$W/a3/queue.tsv")" queued
[ "$(cat "$W/a3/state/drain.lock/pid")" = "$hp" ] && ok "arm3 holder's lock untouched" || bad "arm3 lock clobbered"
grep -q "held by live pid" "$W/a3/state/drain.log" && ok "arm3 log names live holder" || bad "arm3 log"
kill $hp 2>/dev/null; wait $hp 2>/dev/null

# ARM 4: stale lock (dead pid) -> refuse rc 5, lock NOT removed, says STALE
mk a4 "$ROW_Q"; env_for a4
mkdir "$W/a4/state/drain.lock"; echo 99999999 > "$W/a4/state/drain.lock/pid"
bash "$F/drain.sh" --stub-reply "$W/stub.md" 2>"$W/a4.err"; rc=$?
chk "arm4 stale lock rc 5" "$rc" 5
[ -d "$W/a4/state/drain.lock" ] && ok "arm4 stale lock left for a human" || bad "arm4 lock removed"
grep -q "STALE lock" "$W/a4/state/drain.log" && ok "arm4 log says STALE" || bad "arm4 log"

# ARM 5: runner gated (rc 3) -> drain stops rc 3, row untouched; runner usage (rc 2) -> rc 2; runner rc 0 but no progress -> rc 4
printf '#!/bin/bash\nexit 3\n' > "$W/r3.sh"; printf '#!/bin/bash\nexit 2\n' > "$W/r2.sh"; printf '#!/bin/bash\nexit 0\n' > "$W/r0.sh"
mk a5 "$ROW_Q"; env_for a5
DRAIN_RUNNER="bash $W/r3.sh" bash "$F/drain.sh" 2>"$W/a5.err"; chk "arm5 gated rc 3" "$?" 3
chk "arm5 gated row untouched" "$(awk -F'\t' '$1=="F08-numstat-pr2211"{print $4}' "$W/a5/queue.tsv")" queued
DRAIN_RUNNER="bash $W/r2.sh" bash "$F/drain.sh" 2>>"$W/a5.err"; chk "arm5 usage rc 2" "$?" 2
DRAIN_RUNNER="bash $W/r0.sh" bash "$F/drain.sh" 2>>"$W/a5.err"; chk "arm5 no-progress rc 4 (no spin)" "$?" 4
[ -d "$W/a5/state/drain.lock" ] && bad "arm5 lock left behind" || ok "arm5 lock released after stops"

# ARM 6: two concurrent drains -> exactly one runs (second refuses rc 5)
mk a6 "$ROW_Q" "$ROW_Q2"; env_for a6
printf '#!/bin/bash\nsleep 2\npython3 %s/run_filler.py "$@"\n' "$F" > "$W/slow.sh"
DRAIN_RUNNER="bash $W/slow.sh" bash "$F/drain.sh" --stub-reply "$W/stub.md" 2>"$W/a6a.err" & p1=$!
sleep 1
bash "$F/drain.sh" --stub-reply "$W/stub.md" 2>"$W/a6b.err"; rc2=$?
wait $p1; rc1=$?
chk "arm6 first drain rc 0" "$rc1" 0
chk "arm6 second drain refused rc 5" "$rc2" 5

echo "RESULT: $pass passed, $fail failed (work dir $W)"
[ "$fail" -eq 0 ]
