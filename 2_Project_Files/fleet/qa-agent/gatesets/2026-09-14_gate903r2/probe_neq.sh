#!/bin/bash
# probe_neq.sh — the shape NO cell of pre_push_hook_base.test.sh builds: local develop == origin/develop (CURRENT), no upstream,
# docs-only branch. Under the head hook the KS-991 guard's `!=` clause keeps the notice silent; under Tg-B (the clause dropped)
# the notice prints although nothing is stale. Same fixture recipe as the suite's build_fixture (bare origin, seed, fresh clone,
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
    git branch develop origin/develop          # CURRENT local develop: == origin/develop
    git checkout -q -b docs/cur --no-track origin/develop; echo more >> docs/readme.md; git add docs/readme.md; git commit -qm "docs only"
  ) >/dev/null 2>&1
}
for pair in "head:$G/model/pre-push.a4f71cde6" "TgB:$G/sim/pre-push.TgB-neq-dropped"; do
  name="${pair%%:*}"; hook="${pair#*:}"; build "$W/$name" "$hook"
  pre="$( [ "$(git -C "$W/$name/fresh" rev-parse develop)" = "$(git -C "$W/$name/fresh" rev-parse origin/develop)" ] && echo "PRECONDITION: develop == origin/develop" )"
  out="$(git -C "$W/$name/fresh" push origin docs/cur 2>&1)"
  printf '%s\n%s\n' "$pre" "$out" > "$W/$name.out"
  echo "== $name: hook present in the working tree = $( [ -x "$W/$name/fresh/.githooks/pre-push" ] && echo yes || echo NO ) ; precondition = $(printf '%s' "$pre" | /usr/bin/grep -c 'PRECONDITION: develop == origin/develop') ; KS-991 lines = $(printf '%s' "$out" | /usr/bin/grep -c 'KS-991') ; [pre-push] lines = $(printf '%s' "$out" | /usr/bin/grep -c '\[pre-push\]') ; preflight ran = $(printf '%s' "$out" | /usr/bin/grep -c '\[preflight\] ran') ; push rc-ish = $(printf '%s' "$out" | /usr/bin/grep -c 'new branch')"
done
echo "positive control: the head hook under the CASE 10 shape prints the notice — sim/run.head-1b22d4e14.out has CASE 10 'says so (KS-991)' ok"
echo "work dir (kept): $W"
