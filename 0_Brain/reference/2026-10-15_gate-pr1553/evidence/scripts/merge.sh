#!/bin/bash
# merge.sh <scratch clone>: merge prediction + planted conflict control (all writes in the scratch clone)
C=$1; T=Blockchain/Dev/scripts/__tests__/ks884_pre_push_tag_named_develop.test.sh
echo "## live refs $(date -u +%FT%TZ)"; git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1553/head
git -C "$C" fetch -q origin +refs/heads/develop:refs/remotes/origin/develop
echo "## fetched develop in scratch: $(git -C "$C" rev-parse origin/develop)"
MB=$(git -C "$C" merge-base origin/develop origin/pr1553); echo "## merge-base $MB"
echo "## develop commits since merge-base: $(git -C "$C" rev-list --count $MB..origin/develop)"
echo "## overlap (files on develop since base, intersect PR files):"; comm -12 <(git -C "$C" diff --name-only $MB origin/develop | sort) <(git -C "$C" diff --name-only $MB origin/pr1553 | sort); echo "## (end overlap)"
echo "## merge-tree real:"; git -C "$C" merge-tree --write-tree origin/develop origin/pr1553; echo "rc=$?"
echo "## PR head tree: $(git -C "$C" rev-parse 'origin/pr1553^{tree}')"
# planted control: a fake develop commit editing the SAME line 113 differently
W=$(mktemp -d /tmp/g1553/plant.XXXXXX)
git -C "$C" worktree add -q --detach "$W" origin/develop
sed -i '' '113s|echo more >> docs/readme.md|echo planted >> docs/readme.md|' "$W/$T"
git -C "$W" -c user.name=gate -c user.email=gate@local commit -qam "planted conflicting edit"
P=$(git -C "$W" rev-parse HEAD); echo "## planted commit $P"
echo "## merge-tree planted (expect conflict, rc=1):"; git -C "$C" merge-tree --write-tree --name-only $P origin/pr1553; echo "rc=$?"
# planted non-overlap control: a different file edited -> expect clean
W2=$(mktemp -d /tmp/g1553/plant2.XXXXXX)
git -C "$C" worktree add -q --detach "$W2" origin/develop
echo "# planted" >> "$W2/README.md" 2>/dev/null || echo "# planted" >> "$W2/planted.txt"
git -C "$W2" add -A; git -C "$W2" -c user.name=gate -c user.email=gate@local commit -qm "planted non-overlapping edit"
P2=$(git -C "$W2" rev-parse HEAD)
echo "## merge-tree planted non-overlap (expect clean, rc=0):"; git -C "$C" merge-tree --write-tree $P2 origin/pr1553; echo "rc=$?"
