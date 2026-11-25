#!/bin/bash
# QA-MEASURE-2-R2 task 6 scope: a copy of QA-MEASURE-2's qm2_scope.sh for head cdb8955, with the control commit built by
# git plumbing (a temporary index in my work dir; no worktree, so nothing to remove). usage: bash qm2r_scope.sh <clone> <workdir>
C="$1"; WD="$2"; B=184b35ef17cf9865c4f9b20c721f9647233f8b98; H=cdb8955e5b0115d6e304de30523849ac3f066439
scope() { # $1 = commit
  n=$(git -C "$C" diff --name-only $B $1 | wc -l | tr -d ' ')
  inside=$(git -C "$C" diff --name-only $B $1 | grep -c '^spikes/U-B2-host-facts/')
  docs=$(git -C "$C" diff --name-only $B $1 | grep -c -x -e BACKLOG.md -e docs/M0-OUTCOMES.md)
  echo "changed paths: $n ; under spikes/U-B2-host-facts/: $inside ; the two documents: $docs ; anything else: $((n-inside-docs))"
  git -C "$C" diff --name-only $B $1 | grep -v '^spikes/U-B2-host-facts/' | grep -v -x -e BACKLOG.md -e docs/M0-OUTCOMES.md | sed 's/^/  OTHER: /'
  echo "status letters: $(git -C "$C" diff --name-status $B $1 | cut -f1 | sort | uniq -c | tr '\n' ' ')"
  echo "bytes of diff under crates Cargo.toml Cargo.lock scripts preview .github: $(git -C "$C" diff $B $1 -- crates Cargo.toml Cargo.lock scripts preview .github | wc -c | tr -d ' ')"
  echo "any Cargo file anywhere in the diff: $(git -C "$C" diff --name-only $B $1 | grep -c -i cargo)"
  git -C "$C" diff --numstat $B $1 -- BACKLOG.md docs/M0-OUTCOMES.md | sed 's/^/numstat: /'
  for f in BACKLOG.md docs/M0-OUTCOMES.md; do
    python3 -I -B -c 'import sys,subprocess as s
a=s.run(["git","-C",sys.argv[1],"show",sys.argv[2]+":"+sys.argv[4]],capture_output=True).stdout
b=s.run(["git","-C",sys.argv[1],"show",sys.argv[3]+":"+sys.argv[4]],capture_output=True).stdout
print("prefix test %s: base %d bytes, head %d bytes, base is a byte prefix of head: %s" % (sys.argv[4], len(a), len(b), b.startswith(a)))' "$C" $B $1 $f
  done
}
echo "### head $H"; scope $H
export GIT_INDEX_FILE="$WD/ctl.index"; git -C "$C" read-tree $H
m=$( (git -C "$C" show $H:crates/coagent-hook/src/main.rs; printf 'x\n') | git -C "$C" hash-object -w --stdin)
b=$(git -C "$C" show $H:BACKLOG.md | sed '1d' | git -C "$C" hash-object -w --stdin)
git -C "$C" update-index --cacheinfo 100644,$m,crates/coagent-hook/src/main.rs --cacheinfo 100644,$b,BACKLOG.md
P=$(git -C "$C" -c user.name=qa -c user.email=qa@invalid commit-tree $(git -C "$C" write-tree) -p $H -m "planted control"); unset GIT_INDEX_FILE
echo "### CONTROL commit (one line added under crates/, BACKLOG's first line removed; plumbing, in my clone only)"; scope $P
