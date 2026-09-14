#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_ks1061_931.sh on SCRATCH COPIES only. Never touches the real
# briefs/ dir or the launchers/ dir. Green asserted FIRST (cell 0, rc 0), one red per guard at its OWN
# distinct exit code, every tamper asserted LANDED (anchor must exist, replaced text grep'd, or for a
# removal the removed token grep'd 0; NOT byte-identical to the pristine copy), green again LAST on the
# sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL and FAILS=N.
# Every cell runs under env -i with a PATH that has git/python3/perl/grep/curl but NO claude, GH_TOKEN
# read fresh from the Secuura .env by the launcher itself (never injected by this script), 120s alarm
# (macOS has no `timeout` — perl -e 'alarm N; exec @ARGV').
# The develop-move guard's GUARDED arm (exit 18) is exercised LIVE: removing ks695-erasure-by-external-
# ref.test.ts from KNOWN_PR_FILES makes the launcher treat it as an ordinary changed file under the
# guarded directory; at the LIVE develop tip that file still carries its OLD hand-written root
# @secuura/shared factory (>=1 occurrence) because develop has never merged this PR — so the guard MUST
# name it as a GUARDED hit. This is a real network read (GitHub contents API), not a simulation.
set -u
G="${G:?set G to the gate931 scratch dir}"
L="$G/launch_qa_secuura_ks1061_931.sh"
B="$G/2026-09-14_secuura-931-ks1061-tier2.md"
P="$G/2026-09-14_secuura-931-ks1061-tier2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
# RE-PINNED 2026-09-14 ~13:5x AEST — see BUILD_REPORT.md "THE RE-PIN". 53b8a1f7a/dfc63fe48 (M23) are SUPERSEDED.
HEAD='7953070230d285fdebc0c65b834ac8340c02c0b6'
DEVBASE='b9f541e6b158f831576ecc870244f361f219a114'

SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 perl grep head cat shasum wc cut cmp script sed curl; do
  p="$(command -v "$t" 2>/dev/null)"; [ -n "$p" ] && ln -s "$p" "$BIN/$t"
done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "bash: $(/bin/bash --version | head -1)"

run() { # name expected launcher brief prompt headvar mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" head="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i PATH="$NOCLAUDE_PATH" HOME="$HOME" QA931_BRIEF="$brief" QA931_PROMPT="$prompt" ${head:+QA931_HEAD="$head"} \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-headless" ]; then
    env -i PATH="$NOCLAUDE_PATH" HOME="$HOME" QA931_BRIEF="$brief" QA931_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-pty" ]; then
    env -i PATH="$NOCLAUDE_PATH" HOME="$HOME" QA931_BRIEF="$brief" QA931_PROMPT="$prompt" \
      script -q "$W/$name.typescript" perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  fi
  local ok="ok"; [ "$rc" = "$exp" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  [ "$landed" = "LANDED" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  printf '%-72s | %3s | %3s | %s | %s\n' "$name" "$exp" "$rc" "$landed" "$ok"
}
tamper() { # src dst old new expect_new_count(>=1) -> LANDED/NOT-LANDED (new="" means a removal, expect old->0)
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

# ---- cell 0: green --check (scratch brief+prompt) --------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" -ge "10" ] || { echo "  green output does not list at least 10 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name the head SHA $HEAD" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "the isolated model/repo clone (for merge-tree) is present" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the model-clone line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "will refuse unless stdin is a TTY (exit 21)" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the TTY line"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-160)"

# ---- head / merge-base / env file -------------------------------------------------------------------------
run "1 wrong head sha (env override)" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
cp "$L" "$W/l_mb.sh"; ld="$(tamper "$L" "$W/l_mb.sh" "MERGE_BASE='$DEVBASE'" "MERGE_BASE='2222222222222222222222222222222222222222'" 1)"
run "2 wrong merge-base (launcher tamper)" 10 "$W/l_mb.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_env.sh"; ld="$(tamper "$L" "$W/l_env.sh" "4_Credentials/.env'" "4_Credentials/.env.does-not-exist'" 1)"
run "3 env file missing -> compare API unreadable" 13 "$W/l_env.sh" "$B" "$P" "" check "$ld"

# ---- files present ------------------------------------------------------------------------------------
: > "$W/empty.md"; [ ! -s "$W/empty.md" ] && le=LANDED || le=NOT-LANDED
run "4 empty brief" 3 "$L" "$W/empty.md" "$P" "" check "$le"
run "5 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check "$le"
cp "$L" "$W/l_qadir.sh"; ld="$(tamper "$L" "$W/l_qadir.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/does-not-exist'" 1)"
run "6 QA project dir missing (launcher tamper)" 2 "$W/l_qadir.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/does-not-exist'" 1)"
run "7 repo dir missing (launcher tamper)" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- brief/prompt agreement ---------------------------------------------------------------------------
ld="$(tamper "$B" "$W/b_tier.md" "TIER 2" "TIER 3" 1)"
run "8 brief says TIER 3 (brief tamper)" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_tier.txt" "TIER 2" "TIER 3" 1)"
run "9 prompt says TIER 3 (prompt tamper)" 7 "$L" "$B" "$W/p_tier.txt" "" check "$ld"
ld="$(tamper "$B" "$W/b_round.md" "ROUND 1" "ROUND 9" 1)"
run "10 brief says ROUND 9 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 1" "ROUND 9" 1)"
run "11 prompt says ROUND 9 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses -------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "12 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-931-ks1061-tier2.md" "/briefs/2026-09-14_secuura-OTHER-tier2.md" 1)"
run "13 prompt lacks the real brief path" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT" 1)"
run "14 prompt lacks MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_push.txt" "NEVER push, from this gate, to origin" "NEVER push, from this session, to origin" 1)"
run "15 prompt lacks the NEVER-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mem.txt" "Do no memory maintenance" "Do no memory upkeep" 1)"
run "16 prompt lacks no-memory-maintenance" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value" 1)"
run "17 prompt lacks NEVER-print-a-credential" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the model-clone-present guard (exit 19) ------------------------------------------------------------
cp "$L" "$W/l_clone.sh"; ld="$(tamper "$L" "$W/l_clone.sh" "gatesets/2026-09-14_gate931/model/repo" "gatesets/2026-09-14_gate931/model/repo-does-not-exist" 1)"
run "18 model-repo clone path tampered to a missing dir (exit 19)" 19 "$W/l_clone.sh" "$B" "$P" "" check "$ld"

# ---- the head-SHA-in-both guard (exit 20), both arms -----------------------------------------------------
ld="$(tamper "$P" "$W/p_sha.txt" "$HEAD" "53b8a1f7a" 1)"
run "19a prompt lacks the full head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA" "$W/19a prompt lacks the full head SHA (exit 20).out" || { echo "  cell 19a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha.md" "$HEAD" "53b8a1f7a" 1)"
run "19b brief lacks the full head SHA (exit 20)" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- the live develop-move guard (exit 18) — a REAL GitHub read, not a simulation --------------------------
# Post-re-pin, ks695 is no longer part of the delta between DEVBASE (M31, already contains the ks695 union)
# and the live develop tip — a bare KNOWN_PR_FILES removal has nothing to bite on any more (confirmed: this
# exact test read exit 0 against the live pin, because compare(DEVBASE...CUR_DEV) currently carries 0 files
# under the guarded directory). To still exercise the GUARDED-arm logic for real, this cell ALSO rewinds
# DEVELOP_SHA to the ORIGINAL M23 pin (where ks695 legitimately WAS part of the live-moving delta), reproducing
# the exact scenario PART 1 was originally built against — a compound, deliberate two-part tamper.
cp "$L" "$W/l_ks695.sh"
ld1="$(tamper "$L" "$W/l_ks695.sh" \
  '    "Blockchain/Dev/services/originate/src/__tests__/ks695-erasure-by-external-ref.test.ts",' \
  '' 1)"
cp "$W/l_ks695.sh" "$W/l_ks695b.sh"
ld2="$(tamper "$W/l_ks695.sh" "$W/l_ks695b.sh" "DEVELOP_SHA='$DEVBASE'" "DEVELOP_SHA='dfc63fe48ebaa97271f3ff66315a742ba4d79bc2'" 1)"
[ "$ld1" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "20 KNOWN_PR_FILES missing ks695 + DEVELOP_SHA rewound to M23 -> live content check names it GUARDED (exit 18)" 18 "$W/l_ks695b.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED.*ks695-erasure-by-external-ref.test.ts" "$W/20 KNOWN_PR_FILES missing ks695 + DEVELOP_SHA rewound to M23 -> live content check names it GUARDED (exit 18).out" \
  || { echo "  cell 20 did not name ks695 as the GUARDED hit — see its .out"; FAILS=$((FAILS+1)); }
echo "  cell 20 GUARDED line: $(/usr/bin/grep -o 'GUARDED[^—]*' "$W/20 KNOWN_PR_FILES missing ks695 + DEVELOP_SHA rewound to M23 -> live content check names it GUARDED (exit 18).out" | head -1 | cut -c1-160)"

# ---- the TTY guard (exit 21) and the launch modes with NO claude on PATH -----------------------------------
run "21a override launch, HEADLESS (stdin closed) -> TTY guard" 21 "$L" "$B" "$P" "" launch-override-headless LANDED
run "21b override launch, PTY (script) -> past TTY guard, hits the override guard (exit 16)" 16 "$L" "$B" "$P" "" launch-override-pty LANDED

# ---- final green, PRISTINE files, sha-identical to the start ----------------------------------------------
run "22 green --check on the PRISTINE installed-shape files, no overrides needed" 0 "$L" "$B" "$P" "" check LANDED
SHA_L1="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B1="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P1="$(shasum -a 256 "$P" | cut -d' ' -f1)"
[ "$SHA_L0" = "$SHA_L1" ] && echo "ok   launcher bytes unchanged across the whole run ($SHA_L1)" || { echo "FAIL launcher bytes CHANGED during the run"; FAILS=$((FAILS+1)); }
[ "$SHA_B0" = "$SHA_B1" ] && echo "ok   brief bytes unchanged across the whole run ($SHA_B1)" || { echo "FAIL brief bytes CHANGED during the run"; FAILS=$((FAILS+1)); }
[ "$SHA_P0" = "$SHA_P1" ] && echo "ok   prompt bytes unchanged across the whole run ($SHA_P1)" || { echo "FAIL prompt bytes CHANGED during the run"; FAILS=$((FAILS+1)); }

echo "FAILS=$FAILS"
[ "$FAILS" = "0" ] && exit 0 || exit 1
