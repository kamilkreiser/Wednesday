#!/bin/bash
# QA-MEASURE-2 4.5 scope: paths changed, forbidden trees, numstat, byte-prefix test, with a planted control commit.
# usage: bash qm2_scope.sh <clone> ; run from anywhere (git -C only; no cd)
C="$1"; B=184b35ef17cf9865c4f9b20c721f9647233f8b98; H=f96589ece19ebfd88eeeb4463a4d997e29b998b5
n=$(git -C "$C" diff --name-only $B $H | wc -l | tr -d ' ')
inside=$(git -C "$C" diff --name-only $B $H | grep -c '^spikes/U-B2-host-facts/')
docs=$(git -C "$C" diff --name-only $B $H | grep -c -x -e BACKLOG.md -e docs/M0-OUTCOMES.md)
echo "changed paths: $n ; under spikes/U-B2-host-facts/: $inside ; the two documents: $docs ; anything else: $((n-inside-docs))"
git -C "$C" diff --name-only $B $H | grep -v '^spikes/U-B2-host-facts/' | grep -v -x -e BACKLOG.md -e docs/M0-OUTCOMES.md | sed 's/^/  OTHER: /'
echo "status letters: $(git -C "$C" diff --name-status $B $H | cut -f1 | sort | uniq -c | tr '\n' ' ')"
echo "bytes of diff under crates Cargo.toml Cargo.lock scripts preview .github: $(git -C "$C" diff $B $H -- crates Cargo.toml Cargo.lock scripts preview .github | wc -c | tr -d ' ')"
echo "any Cargo file anywhere in the diff: $(git -C "$C" diff --name-only $B $H | grep -c -i cargo)"
git -C "$C" diff --numstat $B $H -- BACKLOG.md docs/M0-OUTCOMES.md | sed 's/^/numstat: /'
for f in BACKLOG.md docs/M0-OUTCOMES.md; do
  python3 -I -B -c 'import sys,subprocess as s
a=s.run(["git","-C",sys.argv[1],"show",sys.argv[2]+":"+sys.argv[4]],capture_output=True).stdout
b=s.run(["git","-C",sys.argv[1],"show",sys.argv[3]+":"+sys.argv[4]],capture_output=True).stdout
print("prefix test %s: base %d bytes, head %d bytes, base is a byte prefix of head: %s" % (sys.argv[4], len(a), len(b), b.startswith(a)))' "$C" $B $H $f
done
# control: a throwaway commit in the clone touching crates/ and removing a BACKLOG line, on a detached HEAD, then back
W=$(mktemp -d /private/tmp/claude-501/qm2/ctlwt.XXXX); git -C "$C" worktree add -q --detach "$W" $H
printf 'x\n' >> "$W/crates/coagent-hook/src/main.rs"; sed -i '' '1d' "$W/BACKLOG.md"
git -C "$W" -c user.name=qa -c user.email=qa@invalid commit -q -am "planted control" ; P=$(git -C "$W" rev-parse HEAD)
echo "CONTROL commit (crates line added, BACKLOG first line removed):"
echo "  bytes under crates..: $(git -C "$C" diff $B $P -- crates Cargo.toml Cargo.lock scripts preview .github | wc -c | tr -d ' ') ; other paths: $(git -C "$C" diff --name-only $B $P | grep -v '^spikes/U-B2-host-facts/' | grep -v -x -e BACKLOG.md -e docs/M0-OUTCOMES.md | wc -l | tr -d ' ')"
git -C "$C" diff --numstat $B $P -- BACKLOG.md | sed 's/^/  numstat: /'
python3 -I -B -c 'import sys,subprocess as s
a=s.run(["git","-C",sys.argv[1],"show",sys.argv[2]+":BACKLOG.md"],capture_output=True).stdout
b=s.run(["git","-C",sys.argv[1],"show",sys.argv[3]+":BACKLOG.md"],capture_output=True).stdout
print("  prefix test BACKLOG.md on the control: %s" % b.startswith(a))' "$C" $B $P
git -C "$C" worktree remove --force "$W"; echo "control worktree removed (it lived in my work dir only)"
