#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_919_ks739.sh on SCRATCH COPIES only. Never touches the real dirs.
# Green asserted FIRST (cell 0, rc 0), one red per guard at a DISTINCT exit code, every tamper asserted LANDED
# (anchor must exist; the new marker grep'd; cmp non-identical to pristine), green again LAST on the
# sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL and FAILS=N. Every cell runs
# under env -i with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset except where a cell needs it,
# 180s alarm.
set -u
G="${G:?set G to the gate919 scratch dir}"
L="$G/launch_qa_secuura_919_ks739.sh"
B="$G/2026-09-14_secuura-919-ks739-tier2.md"
P="$G/2026-09-14_secuura-919-ks739-tier2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
HEAD='4736e22771c12e56d004f58a67f960ddbc0b0508'; DEV='0e78c7270188ac45c1c29f927bdf90728f10215d'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut cmp; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"

run() { # name expected launcher brief prompt headenv mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" headenv="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA919_BRIEF="$brief" QA919_PROMPT="$prompt" ${headenv:+"$headenv"} \
      bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-notty" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA919_BRIEF="$brief" QA919_PROMPT="$prompt" bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  fi
  local ok="ok"; [ "$rc" = "$exp" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  [ "$landed" = "LANDED" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  printf '%-70s | %3s | %3s | %s | %s\n' "$name" "$exp" "$rc" "$landed" "$ok"
}
tamper() { # src dst old new
  local src="$1" dst="$2" old="$3" new="$4"
  python3 - "$src" "$dst" "$old" "$new" <<'PY'
import sys
src,dst,old,new=sys.argv[1:5]
s=open(src,encoding="utf-8").read()
assert old in s, f"anchor absent: {old!r}"
open(dst,"w",encoding="utf-8").write(s.replace(old,new))
PY
  if [ -n "$4" ]; then /usr/bin/grep -qF -- "$4" "$dst" && ! cmp -s "$1" "$2" && echo LANDED || echo NOT-LANDED
  else ! /usr/bin/grep -qF -- "$3" "$dst" && ! cmp -s "$1" "$2" && echo LANDED || echo NOT-LANDED; fi
}

# ---- cell 0: green --check ----
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $DEV" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop-still note"; FAILS=$((FAILS+1)); }

# ---- 1: wrong head (env override) -> 6 ----
run "1 wrong head (env override)" 6 "$L" "$B" "$P" "QA919_HEAD=0000000000000000000000000000000000000000" check LANDED

# ---- 2: files present ----
: > "$W/empty.md"
run "2 empty brief" 3 "$L" "$W/empty.md" "$P" "" check LANDED
run "3 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check LANDED
cp "$L" "$W/l_qadir.sh"; ld="$(tamper "$L" "$W/l_qadir.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/does-not-exist'")"
run "4 QA project dir missing (launcher tamper)" 2 "$W/l_qadir.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/does-not-exist'")"
run "5 repo dir missing (launcher tamper)" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- 6: compare-API mismatch (launcher tamper on CMP_WANT) -> 10 ----
cp "$L" "$W/l_cmp.sh"; ld="$(tamper "$L" "$W/l_cmp.sh" 'CMP_WANT="mb=$DEVELOP_SHA ahead=2 files=4"' 'CMP_WANT="mb=$DEVELOP_SHA ahead=99 files=4"')"
run "6 compare mismatch (launcher tamper) -> 10" 10 "$W/l_cmp.sh" "$B" "$P" "" check "$ld"

# ---- 7: develop guard — a nonsense pin makes the compare API itself unreadable -> 13 ----
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'" "DEVELOP_SHA='1111111111111111111111111111111111111111'")"
run "7 nonsense develop sha -> the compare API cannot resolve it -> 13" 13 "$W/l_dev.sh" "$B" "$P" "" check "$ld"

# ---- 8: develop guard — pin one commit back (M37); the live M37..M38 delta (BACKLOG.md + a ks444 test, neither
# guarded) is judged DISJOINT -> rc 0. Requires CMP_WANT re-aimed too (mb=M37 ahead=3 files=6, measured live).
cp "$L" "$W/l_dev37.sh"
ld1="$(tamper "$L" "$W/l_dev37.sh" "DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'" "DEVELOP_SHA='54e9b835d486c771d0e6f5461dd9cbbfc77cc75c'")"
ld2="$(tamper "$W/l_dev37.sh" "$W/l_dev37b.sh" 'CMP_WANT="mb=$DEVELOP_SHA ahead=2 files=4"' 'CMP_WANT="mb=$DEVELOP_SHA ahead=3 files=6"')"
[ "$ld1" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "8 develop re-pinned to M37 (compare re-aimed): the live M37..M38 delta is DISJOINT -> 0" 0 "$W/l_dev37b.sh" "$B" "$P" "" check "$ld"

# ---- 8b: same M37 pin, GUARDED list widened to catch BACKLOG.md (one of the two M37..M38 files) -> 18 ----
cp "$W/l_dev37b.sh" "$W/l_dev37g.sh"
ld="$(tamper "$W/l_dev37b.sh" "$W/l_dev37g.sh" 'GUARDED = [os.environ["YAML_FILE"], os.environ["OAI_FILE"], os.environ["DOC_FILE"], os.environ["TEST_FILE"], os.environ["BASELINE_FILE"], os.environ["LOCK_FILE"]]' 'GUARDED = [os.environ["YAML_FILE"], os.environ["OAI_FILE"], os.environ["DOC_FILE"], os.environ["TEST_FILE"], os.environ["BASELINE_FILE"], os.environ["LOCK_FILE"], "BACKLOG.md"]')"
run "8b M37 pin, GUARDED widened to BACKLOG.md (in the M37..M38 delta, un-cleared) -> 18" 18 "$W/l_dev37g.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED BACKLOG.md" "$W/8b M37 pin, GUARDED widened to BACKLOG.md (in the M37..M38 delta, un-cleared) -> 18.out" || { echo "  cell 8b did not name BACKLOG.md as the guarded hit"; FAILS=$((FAILS+1)); }

# ---- 8c: same M37 pin + GUARDED widened to BACKLOG.md, ALSO registered in LANDED_OK at its real, MEASURED M38
# blob (dca47caa155e3f743ad401fc62a56618ec6f47fa) -> BACKLOG.md is the ONLY guarded hit in the M37..M38 delta
# (the ks444 test file is not a guarded path at all, so it is not counted), and it clears entirely -> exit 19,
# the LANDED arm (this exercises the exact mechanism exit 19 uses for #919's own four files, on a real blob).
cp "$W/l_dev37g.sh" "$W/l_dev37c.sh"
ld="$(tamper "$W/l_dev37g.sh" "$W/l_dev37c.sh" 'LANDED_OK = {os.environ["YAML_FILE"]: os.environ["YAML_HEAD_BLOB"], os.environ["OAI_FILE"]: os.environ["OAI_HEAD_BLOB"],' 'LANDED_OK = {"BACKLOG.md": "dca47caa155e3f743ad401fc62a56618ec6f47fa", os.environ["YAML_FILE"]: os.environ["YAML_HEAD_BLOB"], os.environ["OAI_FILE"]: os.environ["OAI_HEAD_BLOB"],')"
run "8c M37 pin, BACKLOG.md guarded AND content-cleared at its real, measured M38 blob -> the only hit clears -> 19" 19 "$W/l_dev37c.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "BACKLOG.md now at the head's own blob" "$W/8c M37 pin, BACKLOG.md guarded AND content-cleared at its real, measured M38 blob -> the only hit clears -> 19.out" || { echo "  cell 8c did not name BACKLOG.md as the cleared/landed hit"; FAILS=$((FAILS+1)); }

# ---- 9: brief/prompt tier disagreement -> 7 ----
ld="$(tamper "$B" "$W/b_tier.md" "TIER 2" "TIER 3")"
run "9 brief says TIER 3 (brief tamper) -> 7" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"

# ---- 10: round disagreement -> 15 ----
ld="$(tamper "$B" "$W/b_round.md" "ROUND 1" "ROUND 3")"
run "10 brief says ROUND 3 (brief tamper) -> 15" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"

# ---- 11: no ultrathink -> 8 ----
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard")"
run "11 prompt lacks ultrathink first line -> 8" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"

# ---- 12: prompt lacks brief path -> 9 ----
ld="$(tamper "$P" "$W/p_path.txt" "gate919/2026-09-14_secuura-919-ks739-tier2.md" "gate919/2026-09-14_secuura-OTHER-tier2.md")"
run "12 prompt lacks the real brief path -> 9" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"

# ---- 13: head SHA missing from prompt -> 20 ----
ld="$(tamper "$P" "$W/p_sha.txt" "$HEAD" "4736e2277xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")"
run "13 prompt lacks the full head SHA -> 20" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"

# ---- 14: MAIL YOUR VERDICT missing -> 12 ----
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT")"
run "14 prompt lacks MAIL YOUR VERDICT -> 12" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"

# ---- 15: never-push line missing -> 11 ----
ld="$(tamper "$P" "$W/p_push.txt" "or preflight.sh inside the Secuura checkout" "or preflight.sh within the Secuura checkout")"
run "15 prompt lacks the NEVER-push line -> 11" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"

# ---- 16: no-memory-maintenance missing -> 14 ----
ld="$(tamper "$P" "$W/p_mem.txt" "no memory maintenance" "no memory upkeep")"
run "16 prompt lacks no-memory-maintenance -> 14" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"

# ---- 17: never-print-credential missing -> 17 ----
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value")"
run "17 prompt lacks NEVER-print-a-credential -> 17" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- 18: head SHA missing from brief -> 20 ----
ld="$(tamper "$B" "$W/b_sha.md" "$HEAD" "4736e2277yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")"
run "18 brief lacks the full head SHA -> 20" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- 19: env override present at real launch -> 16 ----
run "19 override launch env set -> 16" 16 "$L" "$B" "$P" "" launch-override LANDED

# ---- 20: no TTY at real launch (defaults point at the scratch set) -> 21 ----
cp "$L" "$W/l_tty.sh"
ld1="$(tamper "$L" "$W/l_tty.sh" 'BRIEF="${QA919_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate919/2026-09-14_secuura-919-ks739-tier2.md}"' "BRIEF=\"\${QA919_BRIEF:-$B}\"")"
ld2="$(tamper "$W/l_tty.sh" "$W/l_tty2.sh" 'PROMPT_FILE="${QA919_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate919/2026-09-14_secuura-919-ks739-tier2.prompt.txt}"' "PROMPT_FILE=\"\${QA919_PROMPT:-$P}\"")"
[ "$ld1" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "20 real launch shape (defaults -> scratch set), stdin not a TTY -> 21" 21 "$W/l_tty2.sh" "" "" "" launch-notty "$ld"
/usr/bin/grep -q "stdin is not a TTY" "$W/20 real launch shape (defaults -> scratch set), stdin not a TTY -> 21.out" || { echo "  cell 20 wrong reason"; FAILS=$((FAILS+1)); }

# ---- raw-control-byte census on the whole set + a synthetic positive control ----
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" <<'PY' || FAILS=$((FAILS+1))
import sys
bad=0
for p in sys.argv[1:]:
    b=open(p,'rb').read()
    off=[i for i,x in enumerate(b) if (x<0x20 and x not in (9,10,13)) or x==0x7f]
    print(f"  raw-control-byte census {p.split('/')[-1]}: {len(off)}")
    bad+=len(off)
ctrl=b"const bad = 'doc\x00bad';\n"
c=[i for i,x in enumerate(ctrl) if (x<0x20 and x not in (9,10,13)) or x==0x7f]
print(f"  positive control (synthetic NUL): offsets {c}")
sys.exit(0 if bad==0 and c==[16] else 1)
PY

echo "  exit codes declared in the launcher (distinct): $(/usr/bin/grep -h -o 'exit [0-9][0-9]*' "$L" | sort -u | tr '\n' ' ')"
/bin/bash -n "$L" && echo "  /bin/bash -n launcher: ok" || { echo "  /bin/bash -n launcher: FAIL"; FAILS=$((FAILS+1)); }

# ---- green again on the pristine set: sha-identical ----
SHA_L1="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B1="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P1="$(shasum -a 256 "$P" | cut -d' ' -f1)"
if [ "$SHA_L0" = "$SHA_L1" ] && [ "$SHA_B0" = "$SHA_B1" ] && [ "$SHA_P0" = "$SHA_P1" ]; then id=LANDED; else id=NOT-LANDED; fi
run "21 green again (pristine sha-identical)" 0 "$L" "$B" "$P" "" check "$id"

echo "pristine sha256: launcher ${SHA_L1:0:16} brief ${SHA_B1:0:16} prompt ${SHA_P1:0:16}"
echo "work dir (kept, never rm'd): $W"
echo "FAILS=$FAILS"
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
exit "$FAILS"
