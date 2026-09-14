#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_L9_940_941_942_887.sh on SCRATCH COPIES only. Never touches the real dirs.
# Green asserted FIRST (cell 0, rc 0, 12 guard lines), one red per guard at a DISTINCT exit code, every tamper asserted
# LANDED (anchor must exist; the new marker grep'd >= expected; cmp non-identical to pristine), green again LAST on the
# sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL and FAILS=N. Every cell runs under env -i
# with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset, 180 s alarm. The develop note is accepted in EITHER
# shape — 'still M18' or 'MOVED -> <tip> … disjoint' (develop moved to M19 6e78961e1, #982's squash, at 09:00 AEST while the
# first run was in flight; the launcher judged it disjoint, as designed). The develop guard's arms are exercised
# against the LIVE deltas to the tip (M15 1c38077ba..M18 = 3 commits / 6 files incl. ONE under systemTest/__tests__/ (the
# `manifest_readers_agree` shell suite moved by KS-1016? — see the cell's own printed hit) and M12 3fc158c39..M18 = 6 commits /
# 9 files; the exact arms are aimed with a slot re-pointed at a file in the delta). The LANDED arm (19) is fired by pinning
# a landed blob as the "OK" blob so M18's real blob reads as the landed one; the live-run guard (21) by a run id at another
# head; the compare guard (10) by a wrong BASE; the four head guards (6) by env override per head; the no-TTY guard (22) once;
# the TTY pass path is driven under `script` with claude ABSENT from PATH, so it reaches the exec line and dies 127.
set -u
G="${G:?set G to the gateL9 scratch dir}"
L="$G/launch_qa_secuura_L9_940_941_942_887.sh"
B="$G/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md"
P="$G/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
M18='8861e62161466c40f08d2b10a30edeb203123993'; M15='1c38077ba2aea5f4c4371c1b68796026dc577764'; M12='3fc158c3975b71654f71d67a89913dc6c98bf08b'
H940='1aa708be9fcf7a23575398546d84848c967e81c5'; H941='d105e07a81c8549b7f47c0542e9594204ce6f599'; H942='53b9c3cc1a89f513620516c580a5de5bd60c64de'; H887='3aee3deed2e3ac557f0a52c0797c2a4a8df25f69'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut perl cmp script; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "bash: $(/bin/bash --version | head -1)"

run() { # name expected launcher brief prompt headenv mode landed   (headenv = "VAR=value" or "")
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" headenv="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QAL9_BRIEF="$brief" QAL9_PROMPT="$prompt" ${headenv:+"$headenv"} \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QAL9_BRIEF="$brief" QAL9_PROMPT="$prompt" \
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
  printf '%-74s | %3s | %3s | %s | %s\n' "$name" "$exp" "$rc" "$landed" "$ok"
}
tamper() { # src dst old new expect_new_count  (a removal: new="" and the old token must read 0 after)
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
DEVPIN="DEVELOP_SHA='$M18'"
SCANOK="SCAN_BLOB_OK='47da5cac924cbe6c58edce8bba7593b81e13257b'"
SUITESOK="SUITES_BLOB_OK='a509ad7934a50cd3f96c7241d9445b942c638cb7'"
TESTS='"systemTest/__tests__/",'
GATESLANDED="GATES_BLOB_LANDED='eac30f09b461bd4fd270ba4da1d24423a53255c1'"

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "12" ] || { echo "  green output does not list 12 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $M18 (M18\|origin develop MOVED $M18 -> [0-9a-f]*: .*— disjoint from the three judged files" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop note (still M18, or MOVED-disjoint)"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "live runs: #940 run 34426409872 completed/failure at 1aa708be9 · #941 run 34427102258 completed/failure at d105e07a8 · #942 run 34785721609 completed/failure at 53b9c3cc1 · #887 run 34786655660" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the live-runs line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "compares: #940 mb=a1e49d15152102acec7c97d96918211227c7fe1e ahead=1 files=1 | #941 mb=a1e49d15152102acec7c97d96918211227c7fe1e ahead=1 files=2 | #942 mb=$M18 ahead=2 files=3 | #887 mb=$M18 ahead=5 files=2" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the compares line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name all four head SHAs" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-140)"

# ---- the four head guards (exit 6), one per head ------------------------------------------------------------
run "1a wrong #940 head (env override)" 6 "$L" "$B" "$P" "QAL9_HEAD940=0000000000000000000000000000000000000000" check LANDED
run "1b wrong #941 head (env override)" 6 "$L" "$B" "$P" "QAL9_HEAD941=0000000000000000000000000000000000000000" check LANDED
run "1c wrong #942 head (env override: the ORIGINAL commit c1676269d)" 6 "$L" "$B" "$P" "QAL9_HEAD942=c1676269d4b438b9b3f897d80bfeae1161dbec39" check LANDED
run "1d wrong #887 head (env override: the REVIEWED head cb7a3e3be)" 6 "$L" "$B" "$P" "QAL9_HEAD887=cb7a3e3be735c2536e8246877fac72ecd4bcd06d" check LANDED
/usr/bin/grep -q "cb7a3e3be735c2536e8246877fac72ecd4bcd06d is not at refs/heads/feature/ks-961-workspace-suites-advisory-on-pr on origin" "$W/1d wrong #887 head (env override: the REVIEWED head cb7a3e3be).out" || { echo "  cell 1d wrong reason"; FAILS=$((FAILS+1)); }

# ---- the live-run guard (exit 21): a run id that exists but sits at another head; a run id that does not exist -------
cp "$L" "$W/l_run.sh"; ld="$(tamper "$L" "$W/l_run.sh" "RUN942='34785721609'" "RUN942='34427586025'" 1)"
run "21a #942's run re-pointed at the base's run 34427586025 (at c1676269d) -> 21" 21 "$W/l_run.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "MOVED #942 run 34427586025 is at head c1676269d, not the pinned 53b9c3cc1" "$W/21a #942's run re-pointed at the base's run 34427586025 (at c1676269d) -> 21.out" || { echo "  cell 21a wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_run2.sh"; ld="$(tamper "$L" "$W/l_run2.sh" "RUN887='34786655660'" "RUN887='1'" 1)"
run "21b #887's run id -> 1 (does not exist) -> 21" 21 "$W/l_run2.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GONE #887 run 1 HTTP 404" "$W/21b #887's run id -> 1 (does not exist) -> 21.out" || { echo "  cell 21b wrong reason"; FAILS=$((FAILS+1)); }

# ---- the compare guard (exit 10) and the env-file guard (exit 13) -------------------------------------------------
cp "$L" "$W/l_base.sh"; ld="$(tamper "$L" "$W/l_base.sh" "BASE_940_941='a1e49d15152102acec7c97d96918211227c7fe1e'" "BASE_940_941='2222222222222222222222222222222222222222'" 1)"
run "3 wrong #940-#941 merge-base pin (launcher tamper) -> 10" 10 "$W/l_base.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_env.sh"; ld="$(tamper "$L" "$W/l_env.sh" "4_Credentials/.env'" "4_Credentials/.env.does-not-exist'" 1)"
run "4 env file missing -> the run guard cannot read the API -> 21 (first API guard)" 21 "$W/l_env.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not where the brief says: GONE #940 run 34426409872 HTTP 401" "$W/4 env file missing -> the run guard cannot read the API -> 21 (first API guard).out" || { echo "  cell 4 wrong reason (expected a 401 GONE on the first run)"; FAILS=$((FAILS+1)); }

# ---- the develop guard: unknown pin (18), a landed blob (19), the GUARDED prefix arm (18), disjoint (0) --------------
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='1111111111111111111111111111111111111111'" 1)"
run "2 unknown develop sha -> the compare guard reads #942 and #887 mb != pin -> 10" 10 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
# 19: pretend M18's real security-scan.yml blob is a LANDED one: swap the OK blob with the first LANDED blob (#940's) — develop's real 47da5cac9 then reads LANDED? No: 47da5cac9 would read OTHER. So instead put 47da5cac9 INTO the LANDED list and a dummy as OK.
cp "$L" "$W/l_land.sh"; ld1="$(tamper "$L" "$W/l_land.sh" "$SCANOK" "SCAN_BLOB_OK='0000000000000000000000000000000000000000'" 1)"
ld2="$(tamper "$W/l_land.sh" "$W/l_land2.sh" "SCAN_BLOBS_LANDED='fac9ef1b89d53884d3655e3e50ea73c54c9a022a " "SCAN_BLOBS_LANDED='47da5cac924cbe6c58edce8bba7593b81e13257b " 1)"
[ "$ld1" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "19 develop's real scan blob listed as '#940 landed' (launcher tamper) -> 19" 19 "$W/l_land2.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "security-scan.yml blob 47da5cac9 (LANDED #940)" "$W/19 develop's real scan blob listed as '#940 landed' (launcher tamper) -> 19.out" || { echo "  cell 19 wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_other.sh"; ld="$(tamper "$L" "$W/l_other.sh" "$SUITESOK" "SUITES_BLOB_OK='0000000000000000000000000000000000000000'" 1)"
run "18a develop's real suites blob pinned as neither OK nor LANDED -> OTHER -> 18" 18 "$W/l_other.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "pr-platform-suites.yml blob a509ad793 (OTHER) — a version nobody pinned" "$W/18a develop's real suites blob pinned as neither OK nor LANDED -> OTHER -> 18.out" || { echo "  cell 18a wrong reason"; FAILS=$((FAILS+1)); }
# 18b: develop pinned at M15 with the shipped GUARDED list — the live M15..M18 delta (6 files) has a file under systemTest/__tests__/ ? measure: the cell prints the hit; a 0 here means the delta is disjoint, which is ALSO a legitimate reading — the cell asserts only that the launcher JUDGED (rc 18 with GUARDED, or rc 0 with MOVED) and prints which.
cp "$L" "$W/l_dev15.sh"; ld="$(tamper "$L" "$W/l_dev15.sh" "$DEVPIN" "DEVELOP_SHA='$M15'" 1)"
# with develop pinned at M15, the #942/#887 compares read mb=M18 != M15 -> exit 10 BEFORE the develop guard. So aim the compare pins too: CMP_WANT uses $DEVELOP_SHA — replace the two mb=$DEVELOP_SHA with mb=M18 literal so the compare passes and the develop guard is reached.
ld2="$(tamper "$W/l_dev15.sh" "$W/l_dev15b.sh" '#942 mb=$DEVELOP_SHA ahead=2 files=3 | #887 mb=$DEVELOP_SHA ahead=5 files=2' "#942 mb=$M18 ahead=2 files=3 | #887 mb=$M18 ahead=5 files=2" 1)"
[ "$ld" = LANDED ] && [ "$ld2" = LANDED ] && ldd=LANDED || ldd=NOT-LANDED
env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QAL9_BRIEF="$B" QAL9_PROMPT="$P" perl -e 'alarm 180; exec @ARGV' bash "$W/l_dev15b.sh" --check > "$W/probe15.out" 2>&1 </dev/null; rc15=$?
if /usr/bin/grep -q "not provably disjoint: GUARDED" "$W/probe15.out"; then exp15=18; else exp15=0; fi
run "18b pinned to M15 (compare pins aimed at M18): the launcher JUDGES the live M15..M18 delta -> $exp15" "$exp15" "$W/l_dev15b.sh" "$B" "$P" "" check "$ldd"
echo "  cell 18b judgement: $(/usr/bin/grep -o 'disjoint: GUARDED [^—]*\|origin develop MOVED [^;]*' "$W/18b pinned to M15 (compare pins aimed at M18): the launcher JUDGES the live M15..M18 delta -> $exp15.out" | head -1 | cut -c1-200)"
# 18c: the same pin with the systemTest/__tests__/ prefix neutralised AND the DEV-PROCESS.md entry aimed at a file in the delta — the EXACT arm. Read the delta's files from the probe: pick the first file name printed by a MOVED note is not available; instead aim at a known M15..M18 file: the ks949 seed-identity auth test (from the #983 set's measurement).
cp "$W/l_dev15b.sh" "$W/l_dev15c.sh"; ld3="$(tamper "$W/l_dev15b.sh" "$W/l_dev15c.sh" '"Blockchain/Dev/docs/DEV-PROCESS.md",' '"Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts",' 1)"
ld4="$(tamper "$W/l_dev15c.sh" "$W/l_dev15d.sh" "$TESTS" '"systemTest/__tests__-NOT-GUARDED/",' 1)"
[ "$ld3" = LANDED ] && [ "$ld4" = LANDED ] && ldd=LANDED || ldd=NOT-LANDED
run "18c M15 pin, tests prefix neutralised, the doc slot AIMED at the ks949 auth test (in M15..M18) -> 18" 18 "$W/l_dev15d.sh" "$B" "$P" "" check "$ldd"
/usr/bin/grep -q "GUARDED Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts" "$W/18c M15 pin, tests prefix neutralised, the doc slot AIMED at the ks949 auth test (in M15..M18) -> 18.out" || { echo "  cell 18c did not name the aimed file as the guarded hit"; FAILS=$((FAILS+1)); }
# 18d: the control — M15 pin, tests prefix neutralised, NO slot aimed at the delta -> 0 or 18 by the live delta (printed)
cp "$W/l_dev15b.sh" "$W/l_dev15e.sh"; ld5="$(tamper "$W/l_dev15b.sh" "$W/l_dev15e.sh" "$TESTS" '"systemTest/__tests__-NOT-GUARDED/",' 1)"
env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QAL9_BRIEF="$B" QAL9_PROMPT="$P" perl -e 'alarm 180; exec @ARGV' bash "$W/l_dev15e.sh" --check > "$W/probe15e.out" 2>&1 </dev/null; rc15e=$?
if /usr/bin/grep -q "not provably disjoint: GUARDED" "$W/probe15e.out"; then exp15e=18; else exp15e=0; fi
run "18d M15 pin, tests prefix neutralised, nothing aimed: the delta judged on the other seven paths -> $exp15e" "$exp15e" "$W/l_dev15e.sh" "$B" "$P" "" check "$ld5"
echo "  cell 18d judgement: $(/usr/bin/grep -o 'disjoint: GUARDED [^—]*\|origin develop MOVED [^;]*' "$W/18d M15 pin, tests prefix neutralised, nothing aimed: the delta judged on the other seven paths -> $exp15e.out" | head -1 | cut -c1-220)"

# ---- files present ---------------------------------------------------------------------------------------
: > "$W/empty.md"; [ ! -s "$W/empty.md" ] && le=LANDED || le=NOT-LANDED
run "5 empty brief" 3 "$L" "$W/empty.md" "$P" "" check "$le"
run "6 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check "$le"
cp "$L" "$W/l_qadir.sh"; ld="$(tamper "$L" "$W/l_qadir.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/does-not-exist'" 1)"
run "7 QA project dir missing (launcher tamper)" 2 "$W/l_qadir.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/does-not-exist'" 1)"
run "8 repo dir missing (launcher tamper)" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- brief/prompt agreement -------------------------------------------------------------------------------
ld="$(tamper "$B" "$W/b_tier.md" "TIER 2" "TIER 3" 1)"
run "9 brief says TIER 3 (brief tamper)" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_tier.txt" "TIER 2" "TIER 3" 1)"
run "10 prompt says TIER 3 (prompt tamper)" 7 "$L" "$B" "$W/p_tier.txt" "" check "$ld"
ld="$(tamper "$B" "$W/b_round.md" "ROUND 1" "ROUND 3" 1)"
run "11 brief says ROUND 3 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 1" "ROUND 3" 1)"
run "12 prompt says ROUND 3 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses ---------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "13 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md" "/briefs/2026-09-14_secuura-OTHER-tier2.md" 1)"
run "14 prompt lacks the real brief path" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT" 1)"
run "15 prompt lacks MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_push.txt" "or preflight.sh inside the Secuura checkout" "or preflight.sh within the Secuura checkout" 1)"
run "16 prompt lacks the NEVER-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mem.txt" "Do no memory maintenance" "Do no memory upkeep" 1)"
run "17 prompt lacks no-memory-maintenance" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value" 1)"
run "18 prompt lacks NEVER-print-a-credential" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the head-SHA-in-both guard (exit 20), one head per arm ------------------------------------------------
ld="$(tamper "$P" "$W/p_sha.txt" "$H887" "3aee3deed" 1)"
run "20a prompt lacks #887's full head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA $H887" "$W/20a prompt lacks #887's full head SHA (exit 20).out" || { echo "  cell 20a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha.md" "$H941" "d105e07a8" 1)"
run "20b brief lacks #941's full head SHA (exit 20)" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- launch modes with NO claude on PATH -------------------------------------------------------------------
run "23 override launch, no claude on PATH -> 16" 16 "$L" "$B" "$P" "" launch-override LANDED
run "24 real launch (not installed yet), no claude -> 3" 3 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md" "$W/24 real launch (not installed yet), no claude -> 3.out" \
  || { echo "  cell 24 did not refuse on the REAL brief path"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_tty.sh"
ld1="$(tamper "$L" "$W/l_tty.sh" 'BRIEF="${QAL9_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md}"' "BRIEF=\"\${QAL9_BRIEF:-$B}\"" 1)"
ld2="$(tamper "$W/l_tty.sh" "$W/l_tty2.sh" 'PROMPT_FILE="${QAL9_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.prompt.txt}"' "PROMPT_FILE=\"\${QAL9_PROMPT:-$P}\"" 1)"
[ "$ld1" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "22 real launch shape (defaults -> scratch set), stdin not a TTY -> 22" 22 "$W/l_tty2.sh" "" "" "" launch-notty "$ld"
/usr/bin/grep -q "stdin is not a TTY" "$W/22 real launch shape (defaults -> scratch set), stdin not a TTY -> 22.out" || { echo "  cell 22 wrong reason"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $M18\|origin develop MOVED $M18 -> [0-9a-f]*: .*— disjoint" "$W/22 real launch shape (defaults -> scratch set), stdin not a TTY -> 22.out" || { echo "  cell 22 did not reach the DEV_NOTE echo (a guard refused earlier)"; FAILS=$((FAILS+1)); }
run "22b the same under a pty (script), claude absent -> 127 at the exec line" 127 "$W/l_tty2.sh" "" "" "" launch-tty "$ld"
/usr/bin/grep -q "claude: command not found\|exec: claude: not found\|claude: No such file" "$W/22b the same under a pty (script), claude absent -> 127 at the exec line.out" "$W/22b the same under a pty (script), claude absent -> 127 at the exec line.typescript" 2>/dev/null \
  || { echo "  cell 22b did not reach the exec line (no 'claude: not found' from the exec)"; FAILS=$((FAILS+1)); }

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_L9.py" "$G/gen_patch_887.py" "$G/brief_patch_887.py" "$G/gh_read.py" "$G/gh_read_887.py" "$G/linear_read.py" "$G/guards_sim.py" <<'PY' || FAILS=$((FAILS+1))
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
run "25 green again (pristine sha-identical)" 0 "$L" "$B" "$P" "" check "$id"

echo "pristine sha256: launcher ${SHA_L1:0:16} brief ${SHA_B1:0:16} prompt ${SHA_P1:0:16}"
echo "work dir (kept, never rm'd): $W"
echo "FAILS=$FAILS"
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
exit "$FAILS"
