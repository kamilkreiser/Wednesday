#!/bin/bash
# (D) each merge commit's tree = git merge-tree of its parents; ancestry; the comment-only commit. Objects only, worktree untouched.
R=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate140-ks1725-pr1953-delta/repo
for m in 25523f25e69c 928ee20c84dc; do p="$(git -C $R rev-parse $m^1) $(git -C $R rev-parse $m^2)"; echo "merge $m parents $p"
  t=$(git -C $R merge-tree --write-tree $p 2>&1); rc=$?; echo "merge-tree rc=$rc tree=$(echo "$t"|head -1) committed=$(git -C $R rev-parse $m^{tree})"; [ "$(echo "$t"|head -1)" = "$(git -C $R rev-parse $m^{tree})" ] && echo "  EQUAL" || echo "  DIFFERENT"; done
echo; git -C $R merge-base --is-ancestor ea6d924eb5de 928ee20c84dc; echo "ea6d924 ancestor of head rc=$?"; git -C $R rev-list --first-parent --oneline ea6d924eb5de..928ee20c84dc
echo; echo "second parents: 25523f25^2=$(git -C $R rev-parse 25523f25e69c^2) 928ee20c^2=$(git -C $R rev-parse 928ee20c84dc^2)"
echo; echo "473ef1e0:"; git -C $R show --stat --format='%H %s' 473ef1e01bb2; git -C $R show --format= 473ef1e01bb2 | grep '^[-+]'
echo; echo "paths the merges add vs first parent, not from develop (should be none):"
for m in 25523f25e69c 928ee20c84dc; do comm -23 <(git -C $R diff --name-only $m^1 $m | sort) <(git -C $R diff --name-only $(git -C $R merge-base $m^1 $m^2) $m^2 | sort); done
