#!/bin/bash
# redproof.sh — every declared exit code of launch_qa_secuura_AUTH4_983_984_986_987.sh fires at least once, the pass
# path returns 0, the develop-moved arm (live develop != M20 — DISJOINT -> 0), the head-in-develop LANDED arm (19), the
# GUARDED arm (18), the headless-TTY arm (21) and the override-on-launch arm (16, under a pty). Cells that need a
# different pin edit a COPY of the launcher in the work dir (never the deliverable); the deliverable's sha256 is
# asserted unchanged at the end. Work dir: mktemp -d under the gate set (never deleted; quarantine by name).
set -u
O='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateAUTH4'
L="$O/launch_qa_secuura_AUTH4_983_984_986_987.sh"
B="$O/2026-09-14_secuura-AUTH4-983r2-984r2-986-987-ks823-835-1151-1150-tier1.md"
P="$O/2026-09-14_secuura-AUTH4-983r2-984r2-986-987-ks823-835-1151-1150-tier1.prompt.txt"
W="$(mktemp -d "$O/redproof.XXXXXX")"
SHA0="$(shasum -a 256 "$L" | cut -c1-16)"
echo "redproof $(date '+%H:%M:%S %Z') work dir $W launcher sha $SHA0"
FAILS=0; FIRED=""
cell() {  # name expected-rc launcher-path [env assignments...]  -- runs --check unless $MODE=launch
  local name="$1" want="$2" lp="$3"; shift 3
  local out="$W/$name.out"
  if [ "${MODE:-check}" = launch ]; then env "$@" bash "$lp" < /dev/null > "$out" 2>&1; rc=$?
  elif [ "${MODE:-check}" = pty ]; then script -q /dev/null env "$@" bash "$lp" < /dev/null > "$out" 2>&1; rc=$?
    # `script` returns the child's status on macOS; if the pty is unavailable the cell is INCONCLUSIVE, not a pass
  else env "$@" bash "$lp" --check > "$out" 2>&1; rc=$?; fi
  FIRED="$FIRED $rc"
  if [ "$rc" = "$want" ]; then echo "ok   $name rc=$rc (want $want): $(tail -1 "$out" | cut -c1-150)"
  else echo "FAIL $name rc=$rc (want $want): $(tail -1 "$out" | cut -c1-200)"; FAILS=$((FAILS+1)); fi
}
OV="QAAUTH4_BRIEF=$B QAAUTH4_PROMPT=$P"
# 0 — the pass path on the scratch set (the live develop may be M21/M22: the MOVED-disjoint arm IS the pass path today)
cell 0_pass 0 "$L" $OV
grep -q 'origin develop MOVED' "$W/0_pass.out" && echo "     (0_pass exercised the develop-MOVED disjoint arm: $(grep -o 'MOVED [0-9a-f]* -> [0-9a-f]*: commits=[0-9]* files=[0-9]*' "$W/0_pass.out"))"
grep -q 'origin develop still' "$W/0_pass.out" && echo "     (0_pass: develop still M20 — the MOVED arm is exercised by cell 3m below)"
# 2/3/4/5 — presence guards
sed "s#^QA_DIR=.*#QA_DIR='/nonexistent/qa'#" "$L" > "$W/l2.sh"; cell 2_qa_dir_missing 2 "$W/l2.sh" $OV
cell 3_brief_missing 3 "$L" QAAUTH4_BRIEF=/nonexistent/brief.md QAAUTH4_PROMPT="$P"
cell 3b_brief_not_installed 3 "$L"
cell 4_prompt_missing 4 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT=/nonexistent/p.txt
sed "s#^REPO=.*#REPO='/nonexistent/repo'#" "$L" > "$W/l5.sh"; cell 5_repo_missing 5 "$W/l5.sh" $OV
# 6 — each head moved / wrong branch (a real SHA at the wrong branch)
cell 6a_983_wrong 6 "$L" $OV QAAUTH4_HEAD=9b020ff827be9c83fbf5e9d62d47bc020a44519d
cell 6b_984_wrong 6 "$L" $OV QAAUTH4_HEAD_984=5b0f4dd583c745e5606c9dbd580fa31f90191c6c
cell 6c_986_as_987 6 "$L" $OV QAAUTH4_HEAD_986=b6ed60f3b1bfe2f72ada658242b0995d0bef7424
cell 6d_987_as_986 6 "$L" $OV QAAUTH4_HEAD_987=ac1c119b56888bc064a820f9b191c409c520df64
# 10 — each compare on its own assertion (the expected string moved in a copy)
sed 's#"$MERGE_BASE ahead=3 files=4" \] ||#"$MERGE_BASE ahead=4 files=4" ] ||#' "$L" > "$W/l10a.sh"; cell 10a_983_compare 10 "$W/l10a.sh" $OV
sed 's#"$MERGE_BASE ahead=5 files=7" \] ||#"$MERGE_BASE ahead=5 files=8" ] ||#' "$L" > "$W/l10b.sh"; cell 10b_984_compare 10 "$W/l10b.sh" $OV
sed 's#"$HEAD_984 ahead=1 files=2" \]   ||#"$HEAD_984 ahead=1 files=3" ]   ||#' "$L" > "$W/l10c.sh"; cell 10c_986_compare 10 "$W/l10c.sh" $OV
sed "s#^MERGE_BASE='6e78961e1d04277ecbdb0537e630afa0bf63b13c'#MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'#" "$L" > "$W/l10d.sh"; cell 10d_merge_base_M18 10 "$W/l10d.sh" $OV
# 13 — the compares unreadable (an empty env file: no GH_TOKEN)
: > "$W/empty.env"; sed "s#^SECUURA_ENV=.*#SECUURA_ENV='$W/empty.env'#" "$L" > "$W/l13.sh"; cell 13_compares_unreadable 13 "$W/l13.sh" $OV
# 18 — GUARDED: develop's oauth.ts blob "a version nobody pinned" (the OK blob mis-pinned in a copy)
sed 's#"80e05458e9759fbc6c7f33bc8cd90060d30e6149": "develop.s (M19 = M20, \#982 landed)"#"0000000000000000000000000000000000000000": "nobody"#' "$L" > "$W/l18a.sh"
grep -q '"0000000000000000000000000000000000000000": "nobody"' "$W/l18a.sh" || echo "FAIL 18a sed did not land"
cell 18a_guarded_blob 18 "$W/l18a.sh" $OV
# 18b — GUARDED path: the pinned develop moved to a SHA whose delta touches services/auth (M18 -> live develop includes M19's three auth files)
sed "s#^DEVELOP_SHA='a5334350221c819f54d4a20a3308daeb9ca09617'#DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'#" "$L" > "$W/l18b.sh"; cell 18b_guarded_path_M18pin 18 "$W/l18b.sh" $OV
# 18c — UNJUDGEABLE: develop pinned at a SHA that is NOT an ancestor of the live develop (status diverged) -> 18
sed "s#^DEVELOP_SHA='a5334350221c819f54d4a20a3308daeb9ca09617'#DEVELOP_SHA='f62c975c11ec97cdef04500fd98a43618e702763'#" "$L" > "$W/l18c.sh"; cell 18c_unjudgeable_diverged 18 "$W/l18c.sh" $OV
# 19 — LANDED: develop's auth.ts blob declared as #986's own (the two blob strings swapped in a copy)
sed 's#"132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6": "develop.s (M18 = M19 = M20)"},#"18946cd7c5c394d89ecbecf860ab66a96b1e22c7": "x"},#; s#{"18946cd7c5c394d89ecbecf860ab66a96b1e22c7": "\#986.s own"}#{"132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6": "\#986 landed (sim)"}#' "$L" > "$W/l19.sh"
grep -q '"132d3b8d39b4fc6bb7cd4140a6f9e814826e7cd6": "#986 landed (sim)"' "$W/l19.sh" || echo "FAIL 19 sed did not land"
cell 19_landed 19 "$W/l19.sh" $OV
# 3m — the develop-MOVED disjoint arm explicitly: pin M19 (live develop delta = M20's three script files + whatever landed since; disjoint) -> 0
sed "s#^DEVELOP_SHA='a5334350221c819f54d4a20a3308daeb9ca09617'#DEVELOP_SHA='6e78961e1d04277ecbdb0537e630afa0bf63b13c'#" "$L" > "$W/l3m.sh"; cell 3m_develop_moved_disjoint 0 "$W/l3m.sh" $OV
grep -q 'origin develop MOVED 6e78961e1' "$W/3m_develop_moved_disjoint.out" || { echo "FAIL 3m did not print the MOVED note"; FAILS=$((FAILS+1)); }
# 7/15/8/9/20/12/11/14/17 — brief / prompt content guards (edited copies of the brief / prompt)
sed 's/TIER 1/TIER 2/g' "$B" > "$W/b7.md"; cell 7_tier 7 "$L" QAAUTH4_BRIEF="$W/b7.md" QAAUTH4_PROMPT="$P"
sed 's/ROUND 2/ROUND TWO/g' "$P" > "$W/p15.txt"; cell 15_round2_missing 15 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p15.txt"
sed 's/ROUND 1/ROUND ONE/g' "$B" > "$W/b15.md"; cell 15b_round1_missing 15 "$L" QAAUTH4_BRIEF="$W/b15.md" QAAUTH4_PROMPT="$P"
sed '1s/ultrathink/think/' "$P" > "$W/p8.txt"; cell 8_ultrathink 8 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p8.txt"
sed 's#/briefs/2026-09-14_secuura-AUTH4#/briefs/2026-09-14_secuura-AUTHX#' "$P" > "$W/p9.txt"; cell 9_brief_path 9 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p9.txt"
for h in 5b0f4dd583c745e5606c9dbd580fa31f90191c6c 9b020ff827be9c83fbf5e9d62d47bc020a44519d ac1c119b56888bc064a820f9b191c409c520df64 b6ed60f3b1bfe2f72ada658242b0995d0bef7424; do
  sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$P" > "$W/p20_$h.txt"; cell "20_sha_${h:0:9}_prompt" 20 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p20_$h.txt"
  sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$B" > "$W/b20_$h.md"; cell "20_sha_${h:0:9}_brief" 20 "$L" QAAUTH4_BRIEF="$W/b20_$h.md" QAAUTH4_PROMPT="$P"
done
sed 's/MAIL YOUR VERDICT/SEND YOUR VERDICT/' "$P" > "$W/p12.txt"; cell 12_mail 12 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p12.txt"
sed 's/NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout/never push/' "$P" > "$W/p11.txt"; cell 11_push 11 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p11.txt"
sed 's/no memory maintenance/no memory upkeep/' "$P" > "$W/p14.txt"; cell 14_memory 14 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p14.txt"
sed 's/NEVER print a credential value/never show a secret/' "$P" > "$W/p17.txt"; cell 17_credential 17 "$L" QAAUTH4_BRIEF="$B" QAAUTH4_PROMPT="$W/p17.txt"
# 21 — headless launch refuses (the TTY guard); 16 — overrides set on a real launch under a pty; 3 — real launch, not installed
MODE=launch cell 21_headless_launch 21 "$L" $OV
if command -v script > /dev/null 2>&1; then MODE=pty cell 16_override_under_pty 16 "$L" $OV; else echo "SKIP 16 (no script(1) for a pty) — INCONCLUSIVE"; fi
MODE=launch cell 3c_real_launch_not_installed 3 "$L"
# raw control-byte census over the deliverables + a synthetic NUL control
for f in "$L" "$B" "$P" "$O/gen_launcher_AUTH4.py" "$O/controls_check.sh" "$O/redproof.sh" "$O/guards_sim.py"; do
  [ -f "$f" ] || continue
  n=$(python3 -c "import sys;b=open(sys.argv[1],'rb').read();print(sum(1 for x in b if (x<0x20 and x not in (9,10,13)) or x==0x7f))" "$f")
  [ "$n" = 0 ] && echo "ok   control-bytes 0 in $(basename "$f")" || { echo "FAIL control-bytes $n in $f"; FAILS=$((FAILS+1)); }
done
printf 'abc\0def' > "$W/nul.ctl"; n=$(python3 -c "import sys;b=open(sys.argv[1],'rb').read();print(sum(1 for x in b if (x<0x20 and x not in (9,10,13)) or x==0x7f))" "$W/nul.ctl"); [ "$n" = 1 ] && echo "ok   control-byte census positive control = 1" || { echo "FAIL census control"; FAILS=$((FAILS+1)); }
bash -n "$L" && echo "ok   bash -n" || { echo "FAIL bash -n"; FAILS=$((FAILS+1)); }
# every declared exit code fired?
for want in 0 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21; do
  case " $FIRED " in *" $want "*) ;; *) echo "FAIL exit $want never fired"; FAILS=$((FAILS+1));; esac
done
SHA1="$(shasum -a 256 "$L" | cut -c1-16)"; [ "$SHA0" = "$SHA1" ] && echo "ok   launcher sha unchanged $SHA1" || { echo "FAIL launcher sha changed $SHA0 -> $SHA1"; FAILS=$((FAILS+1)); }
echo "fired:$FIRED"
echo "FAILS=$FAILS $(date '+%H:%M:%S')"
exit $((FAILS > 0))
