#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_874_ks926.sh on SCRATCH COPIES only. Never touches the real
# dirs. Green asserted FIRST (cell 0, rc 0), one red per guard at a DISTINCT exit code, every tamper
# asserted LANDED (anchor must exist; the new marker grep'd; cmp non-identical to pristine), green again
# LAST on the sha-identical pristine set. Every cell runs under env -i with a PATH that has git/python3/
# grep but NO claude, GH_TOKEN unset except where a cell needs it, 180s alarm.
set -u
G="${G:?set G to the gate874 scratch dir}"
L="$G/launch_qa_secuura_874_ks926.sh"
B="$G/2026-09-14_secuura-874-ks926-tier2.md"
P="$G/2026-09-14_secuura-874-ks926-tier2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
HEAD='b244f4913c948b6d763a6abcf018dac301232345'; DEV='0e78c7270188ac45c1c29f927bdf90728f10215d'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut cmp perl; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"

run() { # name expected launcher brief prompt headenv mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" headenv="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA874_BRIEF="$brief" QA874_PROMPT="$prompt" ${headenv:+"$headenv"} \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA874_BRIEF="$brief" QA874_PROMPT="$prompt" \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-notty" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
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
/usr/bin/grep -q "compare: mb=$DEV ahead=5 files=1" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the compare line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief states the KS-926 archived-ticket exception" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the archived-ticket-exception line"; FAILS=$((FAILS+1)); }

# ---- 1: wrong head (env override) -> 6 ----
run "1 wrong head (env override)" 6 "$L" "$B" "$P" "QA874_HEAD=0000000000000000000000000000000000000000" check LANDED

# ---- 2/3: files present ----
: > "$W/empty.md"
run "2 empty brief" 3 "$L" "$W/empty.md" "$P" "" check LANDED
run "3 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check LANDED
cp "$L" "$W/l_qadir.sh"; ld="$(tamper "$L" "$W/l_qadir.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/does-not-exist'")"
run "4 QA project dir missing (launcher tamper)" 2 "$W/l_qadir.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/does-not-exist'")"
run "5 repo dir missing (launcher tamper)" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- 6: compare-API mismatch (launcher tamper on CMP_WANT) -> 10 ----
cp "$L" "$W/l_cmp.sh"; ld="$(tamper "$L" "$W/l_cmp.sh" 'CMP_WANT="mb=$BASE_SHA ahead=$AHEAD_WANT files=$FILES_WANT"' 'CMP_WANT="mb=$BASE_SHA ahead=99 files=$FILES_WANT"')"
run "6 compare mismatch (launcher tamper) -> 10" 10 "$W/l_cmp.sh" "$B" "$P" "" check "$ld"

# ---- 7: env file missing -> compare API unreadable -> 13 ----
cp "$L" "$W/l_env.sh"; ld="$(tamper "$L" "$W/l_env.sh" "4_Credentials/.env'" "4_Credentials/.env.does-not-exist'")"
run "7 env file missing -> compare API unreadable -> 13" 13 "$W/l_env.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "could not read the compare from the GitHub compare API" "$W/7 env file missing -> compare API unreadable -> 13.out" || { echo "  cell 7 wrong reason"; FAILS=$((FAILS+1)); }

# ---- 8: develop guard — force CUR_DEV to a nonsense value, WITHOUT touching BASE_SHA -> 18 ----
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" 'CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"' 'CUR_DEV="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"')"
run "8 develop pin diverges from a live read, compare-of-two-shas unjudgeable -> 18" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "the move touches the PR's file without a content clearance" "$W/8 develop pin diverges from a live read, compare-of-two-shas unjudgeable -> 18.out" || { echo "  cell 8 wrong reason"; FAILS=$((FAILS+1)); }

# ---- 8b: re-pin DEVELOP_SHA one commit back (M37, 54e9b835d — ONE commit / 2 files to M38, neither the
# doc) so the content-judgement branch runs on live, small, real data -> DISJOINT -> 0.
cp "$L" "$W/l_devparent.sh"; ld="$(tamper "$L" "$W/l_devparent.sh" "DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'" "DEVELOP_SHA='54e9b835d486c771d0e6f5461dd9cbbfc77cc75c'")"
run "8b DEVELOP_SHA re-pinned to M37 (one commit back): the live M37..M38 delta is DISJOINT from the doc -> 0" 0 "$W/l_devparent.sh" "$B" "$P" "" check "$ld"

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
ld="$(tamper "$P" "$W/p_path.txt" "gate874/2026-09-14_secuura-874-ks926-tier2.md" "gate874/2026-09-14_secuura-OTHER-tier2.md")"
run "12 prompt lacks the real brief path -> 9" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"

# ---- 13: head SHA missing from prompt -> 20 ----
ld="$(tamper "$P" "$W/p_sha.txt" "$HEAD" "b244f4913xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")"
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
ld="$(tamper "$B" "$W/b_sha.md" "$HEAD" "b244f4913yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")"
run "18 brief lacks the full head SHA -> 20" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- 19: brief lacks the archived-ticket exception statement -> 21 (this gateset's own extra guard) ----
ld="$(tamper "$B" "$W/b_arch.md" "KS-926 is Done and ARCHIVED" "KS-926 is Done and closed")"
run "19 brief lacks the archived-ticket-exception statement -> 21" 21 "$L" "$W/b_arch.md" "$P" "" check "$ld"

# ---- 20: env override present at real launch -> 16 ----
run "20 override launch env set -> 16" 16 "$L" "$B" "$P" "" launch-override LANDED

# ---- 21: no TTY at real launch (defaults point at the scratch set) -> 22 ----
run "21 real launch, pristine defaults (brief+prompt exist locally), no TTY -> 22" 22 "$L" "$B" "$P" "" launch-notty LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/21 real launch, pristine defaults (brief+prompt exist locally), no TTY -> 22.out" || { echo "  cell 21 wrong reason"; FAILS=$((FAILS+1)); }

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
run "22 green again (pristine sha-identical)" 0 "$L" "$B" "$P" "" check "$id"

echo "pristine sha256: launcher ${SHA_L1:0:16} brief ${SHA_B1:0:16} prompt ${SHA_P1:0:16}"
echo "work dir (kept, never rm'd): $W"
echo "FAILS=$FAILS"
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
exit "$FAILS"
