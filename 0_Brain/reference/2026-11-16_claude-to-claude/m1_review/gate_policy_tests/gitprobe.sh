#!/bin/bash
# Benign git probes, all inside the scratch probe dir. Every "program" run is marker.sh (appends to MARKER).
X=/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m2_policy/probe
M=$X/marker.sh
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
W=$X/ws
mkdir -p $W
git -C $W init -q
printf 'x\n' > $W/a.txt
git -C $W add a.txt
git -C $W -c user.name=t -c user.email=t@t commit -qm init

echo "=== 1. git log --outp=FILE (abbreviation of --output)"
git -C $W --no-pager log --outp=$X/git_out.txt --oneline; echo "rc=$?"
ls -la $X/git_out.txt 2>&1

echo "=== 2. .git/commondir redirect: fsmonitor from a non-.git/config file, run by 'git status'"
mkdir -p $W/evil/objects $W/evil/refs
printf '[core]\n\trepositoryformatversion = 0\n\tfsmonitor = %s\n' "$M" > $W/evil/config
cp -R $W/.git/objects/. $W/evil/objects/ ; cp -R $W/.git/refs/. $W/evil/refs/
printf '../evil\n' > $W/.git/commondir
: > $X/MARKER
git -C $W status --porcelain >/dev/null 2>&1; echo "status rc=$?"
echo "marker lines after git status: $(wc -l < $X/MARKER)"
mv $W/.git/commondir $X/commondir.used

echo "=== 3. bare-repo discovery in a plain workspace subdir + 'git diff --no-index' + diff.external"
B=$W/bare
mkdir -p $B/objects $B/refs
printf 'ref: refs/heads/main\n' > $B/HEAD
printf '[core]\n\trepositoryformatversion = 0\n\tbare = true\n[diff]\n\texternal = %s\n' "$M" > $B/config
printf 'one\n' > $X/f1; printf 'two\n' > $X/f2
: > $X/MARKER
git -C $B --no-pager diff --no-index $X/f1 $X/f2 >/dev/null 2>&1; echo "diff rc=$?"
echo "marker lines after git diff --no-index in bare dir: $(wc -l < $X/MARKER)"
