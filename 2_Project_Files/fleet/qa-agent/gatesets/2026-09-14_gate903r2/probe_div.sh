#!/bin/bash
# probe_div.sh — Peter's note-2 shape, which NO cell builds: local develop is STALE AND carries a local commit (DIVERGED from
# origin/develop), no upstream, docs-only branch cut from origin/develop. The guard's is-ancestor clause is false, local develop
# is consulted, its diff carries the trunk's Blockchain/Dev change -> the gate RUNS (the KS-991 false positive remains — the
# safe direction, stated in the PR body's NOT covered) and NO KS-991 line prints. Under develop's hook: the same RUN. Same fixture recipe as the suite's build_fixture (bare origin, seed, fresh clone,
# preflight stubbed). Drafter's probe; the gate re-runs it as a scratch probe, never a committed cell.
# Written by the Write tool because it contains legitimate `cd`s inside subshells (fixture recipe).
set -u
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
G="${1:?output dir}"; W="$(mktemp -d "$G/sim/tmp/probe.XXXXXX")"
build() { # root hook
  local root="$1" hook="$2"
  mkdir -p "$root"
  ( git init -q --bare -b main "$root/origin.git"; git init -q -b main "$root/seed"; cd "$root/seed"
    git config user.email t@t.t; git config user.name t
    mkdir -p Blockchain/Dev/scripts/preflight systemTest/scripts docs
    echo base > Blockchain/Dev/file.txt; echo docs > docs/readme.md
    printf '#!/usr/bin/env bash\necho "[preflight] ran"\nexit 0\n' > Blockchain/Dev/scripts/preflight/preflight.sh
    : > systemTest/slot-target.sh; printf '#!/usr/bin/env bash\nexit 0\n' > systemTest/scripts/check-package-format.sh; chmod +x systemTest/scripts/check-package-format.sh
    git add -A; git commit -qm init; git branch develop; git remote add origin "$root/origin.git"; git push -q origin main develop
    cd "$root"; git clone -q "$root/origin.git" fresh; cd fresh; git config user.email t@t.t; git config user.name t
    mkdir -p .githooks; cp "$hook" .githooks/pre-push; chmod +x .githooks/pre-push; git config core.hooksPath .githooks
    git branch develop origin/develop          # local develop at the OLD tip ...
    git checkout -q develop; echo local >> docs/local.md; git add docs/local.md; git commit -qm "a local commit on develop"   # ... plus a local commit: DIVERGED (add ONLY that file: `add -A` would sweep the untracked .githooks/pre-push into develop and the later checkout of origin/develop would delete it from the working tree — the first run of this probe did exactly that and measured a hookless push)
    ( cd "$root/seed"; git checkout -q develop; echo trunk-moved > Blockchain/Dev/trunk.txt; git add -A; git commit -qm "trunk moved"; git push -q origin develop )
    git fetch -q origin
    git checkout -q -b docs/div --no-track origin/develop; echo more >> docs/readme.md; git add -A; git commit -qm "docs only"
  ) >/dev/null 2>&1
}
for pair in "head:$G/model/pre-push.a4f71cde6" "develop:$G/model/pre-push.8861e6216"; do
  name="${pair%%:*}"; hook="${pair#*:}"; build "$W/$name" "$hook"
  pre="$( git -C "$W/$name/fresh" merge-base --is-ancestor develop origin/develop || echo "PRECONDITION: develop is NOT an ancestor of origin/develop (diverged)"; git -C "$W/$name/fresh" merge-base --is-ancestor origin/develop develop || echo "PRECONDITION: origin/develop is NOT an ancestor of develop (diverged)"; git -C "$W/$name/fresh" diff --name-only origin/develop HEAD | /usr/bin/grep -q '^Blockchain/Dev/' || echo "PRECONDITION: the branch carries no Blockchain/Dev path" )"
  out="$(git -C "$W/$name/fresh" push origin docs/div 2>&1)"
  printf '%s\n%s\n' "$pre" "$out" > "$W/$name.out"
  echo "== $name: hook present in the working tree = $( [ -x "$W/$name/fresh/.githooks/pre-push" ] && echo yes || echo NO ) ; preconditions (expect 3) = $(printf '%s' "$pre" | /usr/bin/grep -c 'PRECONDITION:') ; KS-991 lines = $(printf '%s' "$out" | /usr/bin/grep -c 'KS-991') ; [pre-push] lines = $(printf '%s' "$out" | /usr/bin/grep -c '\[pre-push\]') ; preflight ran = $(printf '%s' "$out" | /usr/bin/grep -c '\[preflight\] ran') ; push rc-ish = $(printf '%s' "$out" | /usr/bin/grep -c 'new branch')"
done
echo "positive control: the CASE 10 shape (stale, NOT diverged) under the head hook SKIPS with the notice — sim/run.head-1b22d4e14.out"
echo "work dir (kept): $W"
