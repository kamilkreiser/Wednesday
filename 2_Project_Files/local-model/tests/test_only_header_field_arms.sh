#!/bin/bash
# test_only_header_field_arms.sh — arms for the 2026-09-19 test_only header-field fix (IMPROVEMENTS 08:06, KS-739 F1 r1
# FAIL T2 "no file header in the diff"). The builder now writes `diff_file_headers` (the two exact header lines, from
# test_file + test_mode); task.md rule 3 names it; the checker's T2 is UNCHANGED. Negative control = the OLD builder.
#   OLD_BUILDER (default: build_test_only_input.sh.pre-0919-headerfield)  NEW_BUILDER (default: build_test_only_input.sh)
#   NEW_TASK    (default: tasks/test_only/task.md)
# Writes only under $ARMS_SCRATCH (default: a mktemp dir). Read verbs only on the source checkout; the A4 re-check runs
# the checker against a throwaway local clone (git clone --no-checkout, then checkout of the pinned tip) in scratch.
# No model is called. bash 3.2. stderr never discarded.
set -uo pipefail
LM="$(cd "$(dirname "$0")/.." && pwd)"; T="$LM/tasks/test_only"; B="$LM/night/briefs"
OLD="${OLD_BUILDER:-$T/build_test_only_input.sh.pre-0919-headerfield}"
NEW="${NEW_BUILDER:-$T/build_test_only_input.sh}"
TASKMD="${NEW_TASK:-$T/task.md}"
S="${ARMS_SCRATCH:-$(mktemp -d "${TMPDIR:-/tmp}/hdrfield_arms.XXXXXX")}"; mkdir -p "$S"
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
echo "old builder: $OLD ($(shasum -a 256 "$OLD" | cut -c1-12))"
echo "new builder: $NEW ($(shasum -a 256 "$NEW" | cut -c1-12))"
echo "task.md:     $TASKMD ($(shasum -a 256 "$TASKMD" | cut -c1-12))"
echo "scratch:     $S"
P=0; F=0
ok()  { echo "PASS $1"; P=$((P+1)); }
bad() { echo "FAIL $1"; F=$((F+1)); }
build() { # <builder> <id> <brief> <out>
  bash "$1" "$2" "$4" "$3" > "$4.build.out" 2>&1; local rc=$?
  [ "$rc" -eq 0 ] || { echo "  build rc=$rc: $(cat "$4.build.out")"; }
  return $rc
}
field() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1])).get("diff_file_headers"); print("ABSENT" if v is None else "\n".join(v))' "$1"; }

# ---- A1: KS-739-F1 r1 brief (no prose header sentence)
BR1="$B/KS-739-F1.md.pre-0919-r2headers"
TF1="Blockchain/Dev/services/originate/src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts"
build "$NEW" KS-739 "$BR1" "$S/a1_new.json"; rn=$?
build "$OLD" KS-739 "$BR1" "$S/a1_old.json"; ro=$?
GOT="$(field "$S/a1_new.json")"; WANT="$(printf -- '--- a/%s\n+++ b/%s' "$TF1" "$TF1")"
echo "  A1 new field:"; echo "$GOT" | sed 's/^/    /'
echo "  A1 old field: $(field "$S/a1_old.json")"
[ "$rn" -eq 0 ] && [ "$GOT" = "$WANT" ] && ok "A1 new builder: KS-739-F1 r1 field == --- a/<tf> / +++ b/<tf> (mode modify)" || bad "A1 new builder field wrong (rc=$rn)"
[ "$ro" -eq 0 ] && [ "$(field "$S/a1_old.json")" = ABSENT ] && ok "A1 negative control: OLD builder's JSON has no diff_file_headers" || bad "A1 negative control: old builder rc=$ro or field present"

# ---- A2: a `new`-mode brief
for c in KS-1062-F1 KS-991-R1; do
  build "$NEW" "${c%-*}" "$B/$c.md" "$S/a2_$c.json" || continue
  m="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["test_mode"])' "$S/a2_$c.json")"
  [ "$m" = new ] && { A2C="$c"; break; }
  echo "  $c is mode $m — trying the next"
done
if [ -n "${A2C:-}" ]; then
  TF2="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["test_file"])' "$S/a2_$A2C.json")"
  GOT="$(field "$S/a2_$A2C.json")"; echo "  A2 ($A2C) field:"; echo "$GOT" | sed 's/^/    /'
  [ "$GOT" = "$(printf -- '--- /dev/null\n+++ b/%s' "$TF2")" ] && ok "A2 new-mode brief $A2C: field == --- /dev/null / +++ b/<tf>" || bad "A2 new-mode field wrong for $A2C"
else bad "A2 no new-mode brief built (KS-1062-F1, KS-991-R1)"; fi

# ---- A3: no regression — every other field identical; description == brief bytes
for c in KS-1101-N3 KS-864-R1 KS-1062-F1; do
  build "$NEW" "${c%-*}" "$B/$c.md" "$S/a3_${c}_new.json"; r1=$?
  build "$OLD" "${c%-*}" "$B/$c.md" "$S/a3_${c}_old.json"; r2=$?
  python3 - "$S/a3_${c}_old.json" "$S/a3_${c}_new.json" "$B/$c.md" <<'PY' > "$S/a3_$c.cmp" 2>&1
import json, sys
o = json.load(open(sys.argv[1], encoding="utf-8")); n = json.load(open(sys.argv[2], encoding="utf-8"))
brief = open(sys.argv[3], "rb").read()
extra = set(n) - set(o); missing = set(o) - set(n)
n2 = {k: v for k, v in n.items() if k != "diff_file_headers"}
same = (n2 == o); desc = n["ticket"]["description"].encode("utf-8") == brief
print(f"extra={sorted(extra)} missing={sorted(missing)} others_equal={same} description==brief_bytes={desc} mode={n['test_mode']} field={n.get('diff_file_headers')}")
sys.exit(0 if (extra == {"diff_file_headers"} and not missing and same and desc) else 1)
PY
  rc=$?; echo "  A3 $c: $(cat "$S/a3_$c.cmp")"
  [ "$r1" -eq 0 ] && [ "$r2" -eq 0 ] && [ "$rc" -eq 0 ] && ok "A3 $c: new JSON == old JSON except diff_file_headers; ticket.description == brief bytes" || bad "A3 $c regression (build rc new=$r1 old=$r2 cmp rc=$rc)"
done

# ---- A4: checker unchanged, and the r1 bare-hunk out.md still FAILS T2
DS="$(git -C "$LM/../.." diff --stat -- 2_Project_Files/local-model/tasks/test_only/checker.sh 2>&1)"
[ -z "$DS" ] && ok "A4 checker.sh: git diff --stat empty (T2 untouched)" || bad "A4 checker.sh has a diff: $DS"
RUN="$LM/runs/2026-09-19_ks739-ornith35b-night"
mkdir -p "$S/a4"; cp "$RUN/input.json" "$S/a4/input.json"; cp "$RUN/out.md" "$S/a4/out.md"
[ -f "$RUN/out.md.meta.json" ] && cp "$RUN/out.md.meta.json" "$S/a4/out.md.meta.json"
TIP="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["tip"])' "$S/a4/input.json")"
if [ ! -d "$S/a4/clone/.git" ]; then
  git clone -q --no-checkout "$SRC" "$S/a4/clone" > "$S/a4/clone.out" 2>&1 && git -C "$S/a4/clone" checkout -q "$TIP" >> "$S/a4/clone.out" 2>&1
fi
bash "$T/checker.sh" "$S/a4/input.json" "$S/a4/out.md" "$S/a4/clone" > "$S/a4/checker.out" 2>&1; crc=$?
sed 's/^/    /' "$S/a4/checker.out"
if [ "$crc" -ne 0 ] && /usr/bin/grep -q '^FAIL T2 ' "$S/a4/checker.out" && /usr/bin/grep -q 'stopped at T2' "$S/a4/checker.out"; then
  ok "A4 r1 bare-hunk out.md re-checked: still FAIL at T2 (rc=$crc)"
else bad "A4 r1 re-check did not FAIL at T2 (rc=$crc)"; fi

# ---- A5: the assembled prompt (lm_call.py's user_content, built the same way) carries both lines + task.md names the field
python3 - "$LM/lib/lm_call.py" "$TASKMD" "$S/a1_new.json" "$TF1" <<'PY' > "$S/a5.out" 2>&1
import re, sys
src, task, inp, tf = sys.argv[1:5]
code = open(src, encoding="utf-8").read()
# the harness's own assembly expression, lifted verbatim from lm_call.py (so a change there breaks this arm)
m = re.search(r"user_content = \((.*?)\n    \)", code, re.S)
assert m, "user_content assembly not found in lm_call.py"
task_text = open(task, encoding="utf-8").read(); input_text = open(inp, encoding="utf-8").read()
user_content = eval("(" + m.group(1) + ")", {"task_text": task_text, "input_text": input_text})
want = [f'"--- a/{tf}"', f'"+++ b/{tf}"']
hits = [l for l in user_content.split("\n") if any(w in l for w in want)]
for h in hits: print("PROMPT LINE: " + h.strip())
rule = [l for l in user_content.split("\n") if "diff_file_headers" in l]
for r in rule: print("TASK LINE:   " + r.strip())
sys.exit(0 if len(hits) == 2 and any("first two lines" in r or "first two lines" in user_content for r in rule) and len(rule) >= 2 else 1)
PY
rc=$?; cat "$S/a5.out"
[ "$rc" -eq 0 ] && ok "A5 assembled prompt carries both header lines (INPUT JSON) and task.md names diff_file_headers" || bad "A5 prompt lacks the header lines or the rule (rc=$rc)"

echo "RESULT: $P PASS, $F FAIL"
[ "$F" -eq 0 ]
