#!/bin/bash
# fetch PR head + develop from GitHub into the gate clone (write verbs only in the clone)
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate173-ks915-pr1989
C="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
R=$W/repo
SSHC=$(git -C "$C" config --get core.sshCommand)
git -C $R remote set-url origin "$(git -C "$C" config --get remote.origin.url)"
git -C $R -c core.sshCommand="$SSHC" fetch -q origin refs/pull/1989/head:refs/gate/pr refs/heads/develop:refs/gate/develop refs/pull/1982/head:refs/gate/pr1982 || exit 1
git -C $R rev-parse refs/gate/pr refs/gate/develop refs/gate/pr1982
git -C $R merge-tree --write-tree refs/gate/develop refs/gate/pr; echo "merge-tree rc=$?"
echo "merge-base $(git -C $R merge-base refs/gate/develop refs/gate/pr)"
git -C $R diff --stat refs/gate/develop...refs/gate/pr
