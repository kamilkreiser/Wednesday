#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_988_ks704.sh on SCRATCH COPIES only. Never touches the
# real dirs. Green asserted FIRST (cell 0, rc 0, 11 guard lines), one red per guard at a DISTINCT exit
# code, every tamper asserted LANDED (anchor must exist; the new marker grep'd, cmp non-identical to
# pristine), green again LAST on the sha-identical pristine set. Every cell runs under env -i with a PATH
# that has git/python3/grep but NO claude, GH_TOKEN unset, 180 s alarm.
set -u
G="${G:?set G to the gate988 scratch dir}"
L="$G/launch_qa_secuura_988_ks704.sh"
B="$G/2026-09-14_secuura-988-ks704-tier2.md"
P="$G/2026-09-14_secuura-988-ks704-tier2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
HEAD='8cb99a002c5177bb1418ee1fab7cd2974076989a'
DEV='0e78c7270188ac45c1c29f927bdf90728f10215d'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut perl cmp script; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "bash: $(/bin/bash --version | head -1)"

run() { # name expected launcher brief prompt headenv mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" headenv="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA988_BRIEF="$brief" QA988_PROMPT="$prompt" ${headenv:+"$headenv"} \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA988_BRIEF="$brief" QA988_PROMPT="$prompt" \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-notty" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-tty" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" TERM=dumb \
      perl -e 'alarm 180; exec @ARGV' script -q "$W/$name.typescript" bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  fi
  local ok="ok"; [ "$rc" = "$exp" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  [ "$landed" = "LANDED" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  printf '%-70s | %3s | %3s | %s | %s\n' "$name" "$exp" "$rc" "$landed" "$ok"
}
tamper() { # src dst old new n
  local src="$1" dst="$2" old="$3" new="$4" n="$5"
  python3 - "$src" "$dst" "$old" "$new" <<'PY'
import sys
src,dst,old,new=sys.argv[1:5]
s=open(src,encoding="utf-8").read()
assert old in s, f"anchor absent: {old!r}"
open(dst,"w",encoding="utf-8").write(s.replace(old,new))
PY
  local c
  if [ -n "$new" ]; then c="$(/usr/bin/grep -cF -- "$new" "$dst")"; [ "$c" -ge "$n" ] && ! cmp -s "$src" "$dst" && echo LANDED || echo NOT-LANDED
  else c="$(/usr/bin/grep -cF -- "$old" "$dst")"; [ "$c" -eq 0 ] && ! cmp -s "$src" "$dst" && echo LANDED || echo NOT-LANDED; fi
}

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "11" ] || { echo "  green output does not list 11 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $DEV" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop note"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "compare: mb=$DEV ahead=1 files=4" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the compare line"; FAILS=$((FAILS+1)); }

# ---- the head guard (exit 6) ------------------------------------------------------------------------------
run "1 wrong head (env override)" 6 "$L" "$B" "$P" "QA988_HEAD=0000000000000000000000000000000000000000" check LANDED

# ---- the compare guard (exit 10) -------------------------------------------------------------------------
cp "$L" "$W/l_ahead.sh"; ld="$(tamper "$L" "$W/l_ahead.sh" "AHEAD_WANT=1" "AHEAD_WANT=9" 1)"
run "2 wrong AHEAD_WANT pin (launcher tamper) -> 10" 10 "$W/l_ahead.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_files.sh"; ld="$(tamper "$L" "$W/l_files.sh" "FILES_WANT=4" "FILES_WANT=9" 1)"
run "3 wrong FILES_WANT pin (launcher tamper) -> 10" 10 "$W/l_files.sh" "$B" "$P" "" check "$ld"

# ---- the env-file guard (exit 13: the compare API call fails entirely, not merely mismatches) --------------
cp "$L" "$W/l_env.sh"; ld="$(tamper "$L" "$W/l_env.sh" "4_Credentials/.env'" "4_Credentials/.env.does-not-exist'" 1)"
run "4 env file missing -> compare API unreadable -> 13" 13 "$W/l_env.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "could not read the compare from the GitHub compare API" "$W/4 env file missing -> compare API unreadable -> 13.out" || { echo "  cell 4 wrong reason"; FAILS=$((FAILS+1)); }

# ---- the develop content-judgement guard (exit 18): force CUR_DEV to a value that is neither the pin nor
# a readable commit, WITHOUT touching BASE_SHA (so the compare guard above still passes on its own pin) --
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" 'CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"' 'CUR_DEV="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"' 1)"
run "5 develop pin diverges from a live read, compare-of-two-shas unreadable -> 18" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "the move touches systemTest/performance/ without a content clearance" "$W/5 develop pin diverges from a live read, compare-of-two-shas unreadable -> 18.out" || { echo "  cell 5 wrong reason"; FAILS=$((FAILS+1)); }

# ---- files present -----------------------------------------------------------------------------------------
: > "$W/empty.md"; [ ! -s "$W/empty.md" ] && le=LANDED || le=NOT-LANDED
run "6 empty brief" 3 "$L" "$W/empty.md" "$P" "" check "$le"
run "7 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check "$le"
cp "$L" "$W/l_qadir.sh"; ld="$(tamper "$L" "$W/l_qadir.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/does-not-exist'" 1)"
run "8 QA project dir missing (launcher tamper)" 2 "$W/l_qadir.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/does-not-exist'" 1)"
run "9 repo dir missing (launcher tamper)" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- brief/prompt agreement -----------------------------------------------------------------------------
ld="$(tamper "$B" "$W/b_tier.md" "TIER 2" "TIER 3" 1)"
run "10 brief says TIER 3 (brief tamper)" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_tier.txt" "TIER 2" "TIER 3" 1)"
run "11 prompt says TIER 3 (prompt tamper)" 7 "$L" "$B" "$W/p_tier.txt" "" check "$ld"
ld="$(tamper "$B" "$W/b_round.md" "ROUND 1" "ROUND 3" 1)"
run "12 brief says ROUND 3 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 1" "ROUND 3" 1)"
run "13 prompt says ROUND 3 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses -------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "14 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "gate988/2026-09-14_secuura-988-ks704-tier2.md" "gate988/2026-09-14_secuura-OTHER-tier2.md" 1)"
run "15 prompt lacks the real brief path" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT" 1)"
run "16 prompt lacks MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_push.txt" "or preflight.sh inside the Secuura checkout" "or preflight.sh within the Secuura checkout" 1)"
run "17 prompt lacks the NEVER-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mem.txt" "Do no memory maintenance" "Do no memory upkeep" 1)"
run "18 prompt lacks no-memory-maintenance" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value" 1)"
run "19 prompt lacks NEVER-print-a-credential" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the head-SHA-in-both guard (exit 20) ---------------------------------------------------------------
ld="$(tamper "$P" "$W/p_sha.txt" "$HEAD" "8cb99a002" 1)"
run "20 prompt lacks the full head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA $HEAD" "$W/20 prompt lacks the full head SHA (exit 20).out" || { echo "  cell 20 wrong reason"; FAILS=$((FAILS+1)); }

# ---- launch modes with NO claude on PATH ----------------------------------------------------------------
run "21 override launch, no claude on PATH -> 16" 16 "$L" "$B" "$P" "" launch-override LANDED
run "22 real launch, pristine defaults (brief+prompt exist locally), no TTY -> 22" 22 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/22 real launch, pristine defaults (brief+prompt exist locally), no TTY -> 22.out" \
  || { echo "  cell 22 did not reach the TTY refusal on the REAL default paths"; FAILS=$((FAILS+1)); }
run "23 the same under a pty (script), claude absent -> 127 at the exec line" 127 "$L" "$B" "$P" "" launch-tty LANDED
/usr/bin/grep -q "claude: command not found\|exec: claude: not found\|claude: No such file" "$W/23 the same under a pty (script), claude absent -> 127 at the exec line.out" "$W/23 the same under a pty (script), claude absent -> 127 at the exec line.typescript" 2>/dev/null \
  || { echo "  cell 23 did not reach the exec line"; FAILS=$((FAILS+1)); }

# ---- HEAD_SHA one-line substitution point: prove it actually re-pins (a wrong-but-valid-looking SHA fires the head-moved guard) ----
cp "$L" "$W/l_repin.sh"; ld="$(tamper "$L" "$W/l_repin.sh" "HEAD_SHA=\"\${QA988_HEAD:-$HEAD}\"" "HEAD_SHA=\"\${QA988_HEAD:-ffffffffffffffffffffffffffffffffffffffff}\"" 1)"
run "25 HEAD_SHA line alone re-pinned to a wrong-but-valid-looking SHA -> 6 (proves the one-line substitution point works)" 6 "$W/l_repin.sh" "$B" "$P" "" check "$ld"

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
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

# ---- green again on the pristine set: sha-identical ----------------------------------------------------------
SHA_L1="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B1="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P1="$(shasum -a 256 "$P" | cut -d' ' -f1)"
if [ "$SHA_L0" = "$SHA_L1" ] && [ "$SHA_B0" = "$SHA_B1" ] && [ "$SHA_P0" = "$SHA_P1" ]; then id=LANDED; else id=NOT-LANDED; fi
run "26 green again (pristine sha-identical)" 0 "$L" "$B" "$P" "" check "$id"

echo "pristine sha256: launcher ${SHA_L1:0:16} brief ${SHA_B1:0:16} prompt ${SHA_P1:0:16}"
echo "work dir (kept, never rm'd): $W"
echo "FAILS=$FAILS"
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
exit "$FAILS"
