#!/bin/bash
# Gate 163: merge-tree of PR 1980 and PR 1979 onto develop (re-read by ls-remote), each alone and both in both orders.
# All write verbs run in MY clone (repo/); objects land in repo/.git/objects (a --shared clone writes only its own store).
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate163-ks1957-pr1980
R=$W/repo
S="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
date -u
git -C "$S" ls-remote origin refs/heads/develop refs/pull/1980/head refs/pull/1979/head
DEV=$(git -C "$S" ls-remote origin refs/heads/develop | awk '{print $1}')
git -C $R cat-file -e $DEV 2>/dev/null || { echo "develop $DEV not in clone: fetch needed"; exit 3; }
echo "develop=$DEV"
B=66cbe4e52d5afadc9d13ca141200026cc68d5095
echo "base is ancestor of develop: rc=$(git -C $R merge-base --is-ancestor $B $DEV; echo $?)"
echo "files develop moved since base: $(git -C $R diff --name-only $B $DEV | wc -l)"
echo "  shared with 1980: $(comm -12 <(git -C $R diff --name-only $B $DEV | sort) <(git -C $R diff --name-only $B pr/1980 | sort) | wc -l)"
echo "  shared with 1979: $(comm -12 <(git -C $R diff --name-only $B $DEV | sort) <(git -C $R diff --name-only $B pr/1979 | sort) | wc -l)"
echo "  under services/referral: $(git -C $R diff --name-only $B $DEV -- Blockchain/Dev/services/referral | wc -l)"
echo "1979 merge-base with develop: $(git -C $R merge-base pr/1979 $DEV)"
echo "1979 x 1980 shared files (positive control: 1980's own list has $(git -C $R diff --name-only $B pr/1980 | wc -l)):"
comm -12 <(git -C $R diff --name-only $B pr/1980 | sort) <(git -C $R diff --name-only $B pr/1979 | sort)
echo "(end shared list)"
T=$(git -C $R merge-tree --write-tree $DEV pr/1980); echo "1980 onto develop rc=$? $T"
T=$(git -C $R merge-tree --write-tree $DEV pr/1979); echo "1979 onto develop rc=$? $T"
T1=$(git -C $R merge-tree --write-tree $DEV pr/1980); C1=$(git -C $R commit-tree $T1 -p $DEV -p pr/1980 -m g163-dev+1980)
TA=$(git -C $R merge-tree --write-tree $C1 pr/1979); echo "order A (develop+1980)+1979 rc=$? $TA"
T2=$(git -C $R merge-tree --write-tree $DEV pr/1979); C2=$(git -C $R commit-tree $T2 -p $DEV -p pr/1979 -m g163-dev+1979)
TB=$(git -C $R merge-tree --write-tree $C2 pr/1980); echo "order B (develop+1979)+1980 rc=$? $TB"
[ "$TA" = "$TB" ] && echo "orders A and B give the SAME tree" || echo "orders A and B DIFFER"
git -C $R commit-tree $TA -p $DEV -m g163-combined > $W/logs/combined_commit.txt; echo "combined commit $(cat $W/logs/combined_commit.txt)"
