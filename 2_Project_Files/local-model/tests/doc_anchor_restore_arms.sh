#!/bin/bash
# doc_anchor_restore_arms.sh — red-proof for the doc checker's D2 ANCHOR RESTORE (tasks/doc_patch/anchor_restore.py),
# 2026-09-16 22:2x, the doc twin of bash_patch's B3c. Real run artefacts where they exist, synthetic hunks where the case
# has no run. Every checker call writes its report under the work dir (out.md is COPIED there; run dirs are never written).
#   a  KS-890 r2 real out.md (`- Ops notes:`)            NEW → PASS D2 ANCHOR RESTORED, whole verdict PASS (8/8)
#   b  KS-1036 r2 real out.md (a PASS, no '-' lines)     NEW == OLD == recorded checker.out, no accommodation named
#   c  KS-789 r3 real out.md (must_remove input)         NEW == OLD (FAIL D7), not restored
#   c2 KS-789 r3 + insert_after at its '-' line (386, a must-remove line)  → REFUSED by the must-remove clause, not restored
#   c3 control for c2: the same with must_remove emptied → the helper DOES restore (so c2's refusal is that clause)
#   d  ambiguous anchor: `|---|---|` (tip :29 and :45) marked '-'   → REFUSED (matches 2 tip lines), not restored
#   e  the OLD checker (.pre-0916-anchorrestore) on (a)  → FAIL D2 (the arm reaches the new code)
#   f  byte-exact `-Ops notes:` (no extra space)         NEW → ANCHOR RESTORED PASS (8/8); OLD → applies and deletes the anchor, FAIL D9
#   g  `-Ops notes:` AND `+Ops notes:` in the hunk       → REFUSED (re-added), not restored
#   h  a second '-' line in the anchor's hunk            → REFUSED (2 '-' lines), not restored
# Env: ARMS_WORK (work dir, default mktemp -d) · ARMS_CLONE (an existing clone at the tip; else one is made in the work dir)
#      ARMS_NEW / ARMS_OLD (checker paths; default tasks/doc_patch/checker.sh and its .pre-0916-anchorrestore copy)
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
T=$LM/tasks/doc_patch
NEW="${ARMS_NEW:-$T/checker.sh}"; OLD="${ARMS_OLD:-$T/checker.sh.pre-0916-anchorrestore}"
W="${ARMS_WORK:-$(mktemp -d)}"; mkdir -p "$W"
SRC=/Volumes/DevMASTER/\!CODING/Secuura/Blockchain/2_Project_Files
R890=$LM/runs/2026-09-16_ks890-ornith35b-night2; R1036=$LM/runs/2026-09-16_ks1036-ornith35b-night2; R789=$LM/runs/2026-09-16_ks789-ornith35b-night2
TIP=0b25f823f6660ac52b665f14055799ff0c3b616d
for f in "$NEW" "$OLD" "$R890/out.md" "$R890/input.json" "$R1036/out.md" "$R1036/input.json" "$R1036/checker.out" "$R789/out.md" "$R789/input.json"; do
  [ -f "$f" ] || { echo "ARM SETUP FAIL: missing $f"; exit 1; }
done
for i in "$R890/input.json" "$R1036/input.json" "$R789/input.json"; do
  [ "$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tip"])' "$i")" = "$TIP" ] || { echo "ARM SETUP FAIL: $i is not at $TIP"; exit 1; }
done
CLONE="${ARMS_CLONE:-$W/clone}"
if [ ! -d "$CLONE/.git" ]; then
  git clone --shared --no-checkout "$SRC" "$CLONE" > "$W/clone.log" 2>&1 && git -C "$CLONE" checkout --detach "$TIP" >> "$W/clone.log" 2>&1 || { echo "ARM SETUP FAIL: clone (see $W/clone.log)"; exit 1; }
fi
[ "$(git -C "$CLONE" rev-parse HEAD)" = "$TIP" ] || { echo "ARM SETUP FAIL: clone not at $TIP"; exit 1; }
[ -z "$(git -C "$CLONE" status --porcelain --untracked-files=no)" ] || { echo "ARM SETUP FAIL: clone has tracked modifications"; exit 1; }

# synthetic inputs / outputs, derived from the real ones
python3 - "$W" "$R890" "$R789" "$CLONE" <<'PY' || { echo "ARM SETUP FAIL: synthetic build"; exit 1; }
import json, os, sys
w, r890, r789, clone = sys.argv[1:5]
def put(name, inp, out):
    d = os.path.join(w, name); os.makedirs(d, exist_ok=True)
    json.dump(inp, open(os.path.join(d, "input.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(d, "out.md"), "w", encoding="utf-8").write(out)
i890 = json.load(open(os.path.join(r890, "input.json"), encoding="utf-8")); o890 = open(os.path.join(r890, "out.md"), encoding="utf-8").read()
i789 = json.load(open(os.path.join(r789, "input.json"), encoding="utf-8")); o789 = open(os.path.join(r789, "out.md"), encoding="utf-8").read()
assert o890.count("\n- Ops notes:\n") == 1 and o890.count("\n - **A successful WRITE") == 1
put("a", i890, o890); put("e", i890, o890)
# c2 / c3: insert_after at the 789 hunk's single '-' line
tip789 = open(os.path.join(clone, "Blockchain/Dev/CONTRIBUTING.md"), encoding="utf-8").read().split("\n")
ln = tip789.index("the hard gate. Bypass a single push with `git push --no-verify`.") + 1
assert ln == 386 and "the hard gate. Bypass a single push with `git push --no-verify`." in i789["defect_line"]["must_remove"]
c2 = json.loads(json.dumps(i789)); c2["defect_line"]["insert_after"] = ln; put("c2", c2, o789)
c3 = json.loads(json.dumps(c2)); c3["defect_line"]["must_remove"] = []; put("c3", c3, o789)
# d: an anchor whose text occurs twice at the tip
tip890 = open(os.path.join(clone, "Blockchain/Dev/deployment/DEPLOYMENT-ARCHITECTURE.md"), encoding="utf-8").read().split("\n")
assert tip890[28] == "|---|---|" and [k+1 for k,l in enumerate(tip890) if l == "|---|---|"] == [29, 45]
d = json.loads(json.dumps(i890)); d["defect_line"]["insert_after"] = 29
p = "/Blockchain/Dev/deployment/DEPLOYMENT-ARCHITECTURE.md"
put("d", d, "```diff\n--- a" + p + "\n+++ b" + p + "\n@@ -28,3 +28,4 @@\n " + tip890[27] + "\n-" + tip890[28] + "\n+| Row | added by arm d |\n " + tip890[29] + "\n```\n")
put("f", i890, o890.replace("\n- Ops notes:\n", "\n-Ops notes:\n"))
put("g", i890, o890.replace("\n- Ops notes:\n", "\n-Ops notes:\n+Ops notes:\n"))
put("h", i890, o890.replace("\n - **A successful WRITE", "\n-- **A successful WRITE"))
PY
mkdir -p "$W/b" "$W/c"; cp "$R1036/input.json" "$W/b/input.json"; cp "$R1036/out.md" "$W/b/out.md"; cp "$R789/input.json" "$W/c/input.json"; cp "$R789/out.md" "$W/c/out.md"
for n in b c e f; do mkdir -p "$W/${n}_old"; cp "$W/$n/input.json" "$W/$n/out.md" "$W/${n}_old/"; done

fail=0; npass=0
chk() { # chk <checker> <arm dir> → <arm dir>/checker.out
  bash "$1" "$W/$2/input.json" "$W/$2/out.md" "$CLONE" > "$W/$2/checker.out" 2>&1
  [ -z "$(git -C "$CLONE" status --porcelain --untracked-files=no)" ] || { echo "ARM SETUP FAIL: the checker left the clone modified after $2"; exit 1; }
}
ok()  { echo "ARM $1 PASS — $2"; npass=$((npass+1)); }
bad() { echo "ARM $1 FAIL — $2"; /usr/bin/grep -E '^(PASS D2|INFO D2|FAIL|RESULT)' "$W/$3/checker.out" 2>/dev/null | cut -c1-240 | sed 's/^/    /'; fail=1; }
v()   { /usr/bin/grep -m1 '^RESULT:' "$W/$1/checker.out"; }
named() { /usr/bin/grep -q 'ANCHOR RESTORED' "$W/$1/checker.out"; }

chk "$NEW" a
if /usr/bin/grep -q '^PASS D2 .*ANCHOR RESTORED.*tip line 75' "$W/a/checker.out" && [ "$(v a)" = "RESULT: PASS (8/8)" ]; then ok a "KS-890 r2 → D2 ANCHOR RESTORED; verdict: $(v a)"; else bad a "KS-890 r2 not restored to PASS; verdict: $(v a)" a; fi

chk "$NEW" b; chk "$OLD" b_old
if cmp -s "$W/b/checker.out" "$W/b_old/checker.out" && cmp -s "$W/b/checker.out" "$R1036/checker.out" && ! named b; then ok b "KS-1036 r2 → identical to OLD and to the recorded checker.out, no accommodation named; verdict: $(v b)"; else bad b "KS-1036 r2 output changed ($(diff "$W/b_old/checker.out" "$W/b/checker.out" | head -3 | tr '\n' ' '))" b; fi

chk "$NEW" c; chk "$OLD" c_old
if cmp -s "$W/c/checker.out" "$W/c_old/checker.out" && ! named c; then ok c "KS-789 r3 (must_remove) → identical to OLD, not restored; verdict: $(v c)"; else bad c "KS-789 r3 output changed" c; fi

chk "$NEW" c2
if ! named c2 && /usr/bin/grep -q "^INFO D2 anchor restore REFUSED: .*must-remove" "$W/c2/checker.out"; then ok c2 "789 + insert_after at its must-remove '-' line → REFUSED by the must-remove clause; verdict: $(v c2)"; else bad c2 "must-remove anchor not refused by name" c2; fi

chk "$NEW" c3
if /usr/bin/grep -q '^RESTORED: .*tip line 386' "$W/c3/out.md.checker/anchor_restore.out"; then ok c3 "control for c2: must_remove emptied → the helper restores (D2: $(/usr/bin/grep -m1 -E '^(PASS|INFO|FAIL) D2' "$W/c3/checker.out" | cut -c1-90))"; else bad c3 "control did not restore: $(head -1 "$W/c3/out.md.checker/anchor_restore.out")" c3; fi

chk "$NEW" d
if ! named d && /usr/bin/grep -q "^INFO D2 anchor restore REFUSED: .*matches 2 tip lines" "$W/d/checker.out"; then ok d "ambiguous anchor (|---|---| at :29 and :45) → REFUSED, not restored; verdict: $(v d)"; else bad d "ambiguous anchor not refused" d; fi

chk "$OLD" e
if /usr/bin/grep -q '^FAIL D2 diff does NOT apply' "$W/e/checker.out" && ! named e && cmp -s "$W/e/checker.out" "$R890/checker.out"; then ok e "OLD checker on KS-890 r2 → $(v e) (identical to the recorded run)"; else bad e "OLD checker did not FAIL D2 as recorded" e; fi

chk "$NEW" f; chk "$OLD" f_old
if /usr/bin/grep -q '^PASS D2 .*ANCHOR RESTORED.*byte-exact' "$W/f/checker.out" && [ "$(v f)" = "RESULT: PASS (8/8)" ] && /usr/bin/grep -q '^FAIL D9' "$W/f_old/checker.out"; then ok f "byte-exact '-Ops notes:' → NEW $(v f) restored; OLD $(v f_old) with FAIL D9 (anchor deleted)"; else bad f "byte-exact variant: NEW $(v f) / OLD $(v f_old)" f; fi

chk "$NEW" g
if ! named g && /usr/bin/grep -q "^INFO D2 anchor restore REFUSED: .*re-added" "$W/g/checker.out"; then ok g "'-' and '+' of the anchor → REFUSED; verdict: $(v g)"; else bad g "re-added anchor not refused" g; fi

chk "$NEW" h
if ! named h && /usr/bin/grep -q "^INFO D2 anchor restore REFUSED: .*carries 2 '-' lines" "$W/h/checker.out"; then ok h "two '-' lines in the anchor's hunk → REFUSED; verdict: $(v h)"; else bad h "two-minus hunk not refused" h; fi

echo "doc_anchor_restore_arms: $npass/10 arms passed (work dir $W)"
exit $fail
