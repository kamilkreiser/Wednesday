#!/bin/bash
# storage_dryrun_arms.sh -- proves tools/storage_dryrun_secuura.sh (WED-154).
#   (a) an old, merged, clean working copy reads CANDIDATE
#   (b) a dirty one reads KEEP
#   (c) a folder modified now reads KEEP (live)
#   (d) the self-check refuses a copy of the script with a removal verb planted
#   (e) a real run over the real tree produces the dated report
# Plus extras: unmerged old copy reads KEEP; the tool left the fixture byte-identical (no write other than its report).
# Scratch fixture only under the session scratchpad. bash 3.2.

TOOL=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/storage_dryrun_secuura.sh
SCR=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/storage
FX="$SCR/fx_$(date +%H%M%S)"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "ARM PASS: $1"; }
bad() { FAIL=$((FAIL+1)); echo "ARM FAIL: $1"; }

mkdir -p "$FX/proj/worktrees" "$FX/proj/deploy-clones" "$FX/proj/5_Project_History" "$FX/lm/runs" "$FX/report" "$FX/up" || exit 1
git init -q -b develop "$FX/up" || exit 1
git -C "$FX/up" config user.email t@example.invalid
git -C "$FX/up" config user.name t
echo base > "$FX/up/a.txt"
echo node_modules/ > "$FX/up/.gitignore"
git -C "$FX/up" add a.txt .gitignore
git -C "$FX/up" commit -q -m base || exit 1

mkclone() { # name
  git clone -q "$FX/up" "$FX/proj/worktrees/$1" || return 1
  git -C "$FX/proj/worktrees/$1" config user.email t@example.invalid
  git -C "$FX/proj/worktrees/$1" config user.name t
}
age() { # name  (make every file and dir old: 2026-09-01)
  find "$FX/proj/worktrees/$1" -exec touch -t 202609010000 {} +
}

mkclone old-merged; age old-merged
mkclone old-dirty;  echo wip > "$FX/proj/worktrees/old-dirty/wip.txt"; age old-dirty
mkclone old-unmerged
git -C "$FX/proj/worktrees/old-unmerged" checkout -q -b feat/x
echo x > "$FX/proj/worktrees/old-unmerged/x.txt"
git -C "$FX/proj/worktrees/old-unmerged" add x.txt
git -C "$FX/proj/worktrees/old-unmerged" commit -q -m x
age old-unmerged
mkclone live-now   # fresh mtimes, merged and clean: only recency should keep it
mkdir -p "$FX/proj/worktrees/old-merged/Dev/node_modules/pkg"; echo n > "$FX/proj/worktrees/old-merged/Dev/node_modules/pkg/i.js"
age old-merged

mkdir -p "$FX/proj/scratchpad/j1"
git clone -q "$FX/up" "$FX/proj/scratchpad/j1/repo"
mkdir -p "$FX/proj/scratchpad/j1/repo/node_modules/p"; echo n > "$FX/proj/scratchpad/j1/repo/node_modules/p/i.js"
find "$FX/proj/scratchpad" -exec touch -t 202609010000 {} +

before=$(find "$FX/proj" "$FX/lm" "$FX/up" -type f -not -path '*/.git/*' | sort | xargs shasum 2>/dev/null | shasum | cut -d' ' -f1)
OUT="$FX/out.txt"
/bin/bash "$TOOL" --root "$FX/proj" --lm "$FX/lm" --report-dir "$FX/report" --date 2099-01-01 --jobs 2 > "$OUT" 2> "$FX/err.txt"
rc=$?
echo "fixture run rc=$rc"
after=$(find "$FX/proj" "$FX/lm" "$FX/up" -type f -not -path '*/.git/*' | sort | xargs shasum 2>/dev/null | shasum | cut -d' ' -f1)

line() { grep -F "worktrees/$1\`" "$OUT" | head -1; }
l=$(line old-merged);   echo "$l"; case "$l" in *"| CANDIDATE |"*) ok "(a) old merged clean working copy -> CANDIDATE";; *) bad "(a) expected CANDIDATE";; esac
l=$(line old-dirty);    echo "$l"; case "$l" in *"| KEEP |"*DIRTY*) ok "(b) dirty working copy -> KEEP (DIRTY)";; *) bad "(b) expected KEEP DIRTY";; esac
l=$(line live-now);     echo "$l"; case "$l" in *"| KEEP |"*LIVE*) ok "(c) folder modified now -> KEEP (LIVE)";; *) bad "(c) expected KEEP LIVE";; esac
l=$(line old-unmerged); echo "$l"; case "$l" in *"| KEEP |"*UNMERGED*) ok "(x) old unmerged working copy -> KEEP (UNMERGED)";; *) bad "(x) expected KEEP UNMERGED";; esac
nm=$(grep -F "| N | CANDIDATE |" "$OUT" | head -1)
[ -z "$nm" ] && ok "(x) node_modules inside a W candidate is not double-counted in class N" || bad "(x) N double-count: $nm"
l=$(grep -F 'scratchpad/j1/repo`' "$OUT" | grep -F '| P |' | head -1); echo "$l"
case "$l" in *"| CANDIDATE |"*) ok "(y) old merged clean scratch clone in scratchpad -> CANDIDATE";; *) bad "(y) expected P CANDIDATE";; esac
[ "$(grep -F '| P |' "$OUT" | grep -c 'node_modules')" = 0 ] && ok "(y) node_modules inside a candidate clone not listed twice" || bad "(y) nm listed twice"
[ "$before" = "$after" ] && ok "(x) fixture files byte-identical before/after (tool wrote nothing but its report)" || bad "(x) fixture changed"
[ -f "$FX/report/dryrun_2099-01-01.md" ] && ok "(x) fixture report written" || bad "(x) fixture report missing"

# (d) plant a removal verb in a copy of the script; the self-check must refuse
PL="$FX/planted.sh"
cp "$TOOL" "$PL"
printf '%s\n' 'rm -rf /nonexistent-planted-path' >> "$PL"
/bin/bash "$PL" --root "$FX/proj" --lm "$FX/lm" --report-dir "$FX/report2" --date 2099-01-02 > "$FX/d.out" 2> "$FX/d.err"
drc=$?
cat "$FX/d.err"
if [ "$drc" -ne 0 ] && grep -q 'SELF-CHECK FAILED' "$FX/d.err" && [ ! -e "$FX/report2" ]; then ok "(d) self-check refused the planted copy (rc=$drc, no report dir created)"; else bad "(d) planted copy was not refused (rc=$drc)"; fi
# and the genuine script passes its own check
/bin/bash "$TOOL" --self-check-only && ok "(d2) genuine script passes its own self-check" || bad "(d2) genuine script fails its own self-check"
# other planted verbs
for v in 'mv /a /b' 'git worktree prune' 'find /x -delete' 'rsync -a --delete /a /b' 'git clean -fd'; do
  cp "$TOOL" "$PL"; printf '%s\n' "$v" >> "$PL"
  /bin/bash "$PL" --self-check-only > /dev/null 2>&1 && bad "(d3) planted '$v' not refused" || ok "(d3) planted '$v' refused"
done

# (e) real run over the real tree
if [ -n "$ARMS_FIXTURE_ONLY" ]; then echo "ARMS: pass=$PASS fail=$FAIL (fixture only; (e) skipped)"; [ "$FAIL" -eq 0 ]; exit; fi
REAL_OUT="$FX/real_out.txt"
/bin/bash "$TOOL" > "$REAL_OUT" 2> "$FX/real_err.txt"
erc=$?
RP=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_storage-policy/dryrun_$(date +%F).md
if [ "$erc" -eq 0 ] && [ -s "$RP" ] && grep -q '^## Totals' "$RP"; then ok "(e) real run rc=0, report written: $RP ($(wc -c < "$RP") bytes)"; else bad "(e) real run rc=$erc or report missing"; fi
tail -14 "$REAL_OUT"
echo "ARMS: pass=$PASS fail=$FAIL"
[ "$FAIL" -eq 0 ]
