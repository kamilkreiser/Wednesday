#!/usr/bin/env bash
# TESTS for .githooks/pre-push - a TAG named develop must not beat the branch (KS-884)
# The base loop tried the bare name `develop` first. git resolves a bare name to a TAG before a branch, and
# --quiet hides the ambiguity warning, so a tag named develop became the base and the changed set was wrong.
# Fixture: origin/develop is one commit AHEAD of the merge-base with a tag named develop (the tag sits on a side commit and
# is never pushed, and is NOT an ancestor of origin/develop); there is NO local branch develop. A docs-only branch off origin/develop must be judged
# against origin/develop (nothing under Blockchain/Dev changed) and must NOT run the preflight. Every
# fixture pushes to a LOCAL BARE REMOTE; the preflight and the systemTest formatting gate are stubs.
# ADDED by the raise seat (Spark payload + additive hardening): two more fixtures that pin the edits the original cells do not.
#   S4  a LOCAL develop that is BEHIND origin/develop, plus a tag develop: the KS-991 stale-local skip must still fire (the
#       --is-ancestor test must name refs/heads/develop, not the bare name a tag captures) and the base is origin/develop.
#   S10 the same with a tag named origin/develop: the stale-local skip must leave ONLY the fully-qualified remote-tracking ref.
#   S13 a tag literally named refs/heads/develop (git resolves refs/heads/develop to refs/tags/refs/heads/develop when no such
#       branch exists), with no local develop and no origin/develop: the loop must verify the EXACT ref (git show-ref --verify),
#       or that tag becomes the base and a real Blockchain/Dev change is skipped where the old hook ran the preflight.
# Two edits in the patch (the --verify and the != comparison in the KS-991 condition) are consistency-only: no scenario
# distinguishes them from the unedited text, so no cell pins them.
# Usage: bash Blockchain/Dev/scripts/__tests__/ks884_pre_push_tag_named_develop.test.sh
#        HOOK_SH=/path/to/other/pre-push bash ...   (to test a different copy)
set -uo pipefail
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
HOOK="${HOOK_SH:-$REPO_ROOT/.githooks/pre-push}"
[ -f "$HOOK" ] || { echo "FATAL: pre-push hook not found at $HOOK" >&2; exit 2; }
WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks884.XXXXXX")"
trap 'echo WORK=$WORK' EXIT
pass=0
fail=0
ok()   { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad()  { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
(
  git init -q --bare -b main "$WORK/origin.git"
  git init -q -b main "$WORK/seed"
  cd "$WORK/seed"
  git config user.email t@t.t; git config user.name t
  mkdir -p Blockchain/Dev/scripts/preflight systemTest/scripts docs
  echo base > Blockchain/Dev/file.txt
  echo docs > docs/readme.md
  printf '#!/usr/bin/env bash\necho "[preflight] ran"\nexit 0\n' > Blockchain/Dev/scripts/preflight/preflight.sh
  : > systemTest/slot-target.sh
  printf '#!/usr/bin/env bash\n[ "${1:-}" = "--all" ] || cat >/dev/null\nexit 0\n' > systemTest/scripts/check-package-format.sh
  chmod +x systemTest/scripts/check-package-format.sh
  git add -A; git commit -qm init
  git branch develop
  echo more >> Blockchain/Dev/file.txt
  git add -A; git commit -qm "dev change"
  git branch -f develop
  git remote add origin "$WORK/origin.git"
  git push -q origin main develop
  cd "$WORK"
  git clone -q "$WORK/origin.git" fresh
  cd fresh
  git config user.email t@t.t; git config user.name t
  mkdir -p "$WORK/hooks"
  cp "$HOOK" "$WORK/hooks/pre-push"
  chmod +x "$WORK/hooks/pre-push"
  git config core.hooksPath "$WORK/hooks"
  git tag develop "$(git commit-tree -p "$(git rev-parse origin/develop~1)" -m side "$(git rev-parse 'origin/develop~1^{tree}')")"
) >/dev/null 2>&1
docs_out="$(
  cd "$WORK/fresh" || exit 1
  git checkout -q -b docs/tagged --no-track origin/develop
  echo more >> docs/readme.md
  git add -A; git commit -qm "docs only"
  git rev-parse --verify --quiet refs/tags/develop >/dev/null || echo "PRECONDITION-LOST: the tag develop is missing"
  git rev-parse --verify --quiet refs/heads/develop >/dev/null && echo "PRECONDITION-LOST: a local branch develop exists"
  [ "$(git rev-parse refs/tags/develop)" != "$(git rev-parse origin/develop)" ] || echo "PRECONDITION-LOST: the tag equals origin/develop"
  git push origin docs/tagged 2>&1
  git ls-remote origin refs/heads/docs/tagged | grep -q . && echo "PUSH-LANDED"
)"
dev_out="$(
  cd "$WORK/fresh" || exit 1
  git checkout -q -b feat/tagged --no-track origin/develop
  echo more >> Blockchain/Dev/file.txt
  git add -A; git commit -qm "dev change on the branch"
  git push origin feat/tagged 2>&1
  git ls-remote origin refs/heads/feat/tagged | grep -q . && echo "PUSH-LANDED"
)"
if printf '%s' "$docs_out" | grep -q 'PRECONDITION-LOST'; then
  bad "preconditions hold" "$(printf '%s' "$docs_out" | grep 'PRECONDITION-LOST' | tr '\n' ';')"
else
  ok "preconditions hold - a tag named develop sits off origin/develop's history and no local branch develop exists"
fi
if printf '%s' "$docs_out" | grep -q 'PUSH-LANDED'; then
  ok "the docs-only push reached the bare remote"
else
  bad "the docs-only push reached the bare remote" "the push was refused or did not run"
fi
if printf '%s' "$docs_out" | grep -q '\[preflight\] ran'; then
  bad "a tag named develop does not become the base" "the preflight ran on a docs-only branch: the base was the tag, not origin/develop"
else
  ok "a tag named develop does not become the base - the docs-only push skips the preflight"
fi
if printf '%s' "$dev_out" | grep -q 'PUSH-LANDED' && printf '%s' "$dev_out" | grep -q '\[preflight\] ran'; then
  ok "a push that changes Blockchain/Dev still runs the preflight"
else
  bad "a push that changes Blockchain/Dev still runs the preflight" "the preflight did not run, or the push did not land"
fi

# ---- added cells: a stale LOCAL develop together with a tag (S4) and with a tag named origin/develop (S10) ----------------
mkfresh() { # mkfresh <name>: another clone of the same bare origin, with the hook under test installed
  ( cd "$WORK" && git clone -q "$WORK/origin.git" "$1" && cd "$1" \
    && git config user.email t@t.t && git config user.name t && git config core.hooksPath "$WORK/hooks" ) >/dev/null 2>&1
}
SIDE='git commit-tree -p "$(git rev-parse refs/remotes/origin/develop~1)" -m side "$(git rev-parse "refs/remotes/origin/develop~1^{tree}")"'
mkfresh stale_tag
s4_out="$(
  cd "$WORK/stale_tag" || exit 1
  git branch develop refs/remotes/origin/develop~1
  git tag develop "$(eval "$SIDE")"
  git checkout -q -b docs/stale --no-track refs/remotes/origin/develop
  echo s4-distinct >> docs/readme.md   # R45: must differ from the cell 1 commit on docs/tagged, or the two share a SHA
  git add -A; git commit -qm "docs only"
  git merge-base --is-ancestor refs/heads/develop refs/remotes/origin/develop || echo "PRECONDITION-LOST: local develop is not behind origin/develop"
  [ "$(git rev-parse refs/heads/develop)" != "$(git rev-parse refs/remotes/origin/develop)" ] || echo "PRECONDITION-LOST: local develop equals origin/develop"
  [ "$(git rev-parse refs/tags/develop)" != "$(git rev-parse refs/remotes/origin/develop)" ] || echo "PRECONDITION-LOST: the tag equals origin/develop"
  git merge-base --is-ancestor refs/tags/develop refs/remotes/origin/develop 2>/dev/null && echo "PRECONDITION-LOST: the tag is an ancestor of origin/develop"
  git push origin docs/stale 2>&1
  git ls-remote origin refs/heads/docs/stale | grep -q . && echo "PUSH-LANDED"
)"
mkfresh stale_origin_tag
s10_out="$(
  cd "$WORK/stale_origin_tag" || exit 1
  git branch develop refs/remotes/origin/develop~1
  git tag origin/develop "$(eval "$SIDE")"
  git checkout -q -b docs/stale10 --no-track refs/remotes/origin/develop
  echo s10-distinct >> docs/readme.md   # K10: must differ from the S4 commit, or the two share a SHA
  git add -A; git commit -qm "docs only"
  git merge-base --is-ancestor refs/heads/develop refs/remotes/origin/develop || echo "PRECONDITION-LOST: local develop is not behind origin/develop"
  [ "$(git rev-parse refs/tags/origin/develop)" != "$(git rev-parse refs/remotes/origin/develop)" ] || echo "PRECONDITION-LOST: the tag equals the remote-tracking ref"
  [ "$(git rev-parse origin/develop 2>/dev/null)" = "$(git rev-parse refs/tags/origin/develop)" ] || echo "PRECONDITION-LOST: the bare name origin/develop is not captured by the tag"
  git push origin docs/stale10 2>&1
  git ls-remote origin refs/heads/docs/stale10 | grep -q . && echo "PUSH-LANDED"
)"
if printf '%s' "$s4_out" | grep -q 'PRECONDITION-LOST'; then
  bad "S4 preconditions hold" "$(printf '%s' "$s4_out" | grep 'PRECONDITION-LOST' | tr '\n' ';')"
else
  ok "S4 preconditions hold - a local develop BEHIND origin/develop and a tag develop off its history"
fi
if printf '%s' "$s4_out" | grep -q 'PUSH-LANDED' && printf '%s' "$s4_out" | grep -q 'KS-991' && ! printf '%s' "$s4_out" | grep -q '\[preflight\] ran'; then
  ok "S4 a stale local develop beside a tag develop: the KS-991 skip fires and the docs-only push skips the preflight"
else
  bad "S4 a stale local develop beside a tag develop: the KS-991 skip fires and the docs-only push skips the preflight" "landed=$(printf '%s' "$s4_out" | grep -c PUSH-LANDED) ks991=$(printf '%s' "$s4_out" | grep -c KS-991) preflight-ran=$(printf '%s' "$s4_out" | grep -c '\[preflight\] ran')"
fi
if printf '%s' "$s10_out" | grep -q 'PRECONDITION-LOST'; then
  bad "S10 preconditions hold" "$(printf '%s' "$s10_out" | grep 'PRECONDITION-LOST' | tr '\n' ';')"
else
  ok "S10 preconditions hold - a local develop BEHIND origin/develop and a tag named origin/develop that captures the bare name"
fi
if printf '%s' "$s10_out" | grep -q 'PUSH-LANDED' && printf '%s' "$s10_out" | grep -q 'KS-991' && ! printf '%s' "$s10_out" | grep -q '\[preflight\] ran'; then
  ok "S10 a tag named origin/develop does not become the base - the stale-local skip leaves only the remote-tracking ref"
else
  bad "S10 a tag named origin/develop does not become the base - the stale-local skip leaves only the remote-tracking ref" "landed=$(printf '%s' "$s10_out" | grep -c PUSH-LANDED) ks991=$(printf '%s' "$s10_out" | grep -c KS-991) preflight-ran=$(printf '%s' "$s10_out" | grep -c '\[preflight\] ran')"
fi

# ---- added cell (the Opus gate on PR 1474): a tag named refs/heads/develop must not be taken for the branch (S13) ---------
mkfresh hijack
s13_out="$(
  cd "$WORK/hijack" || exit 1
  git update-ref -d refs/remotes/origin/develop
  git checkout -q -b dev/hijack --no-track main
  echo more >> Blockchain/Dev/file.txt
  git add -A; git commit -qm "dev change"
  git tag refs/heads/develop
  echo more >> docs/readme.md
  git add -A; git commit -qm "docs on top"
  git show-ref --verify --quiet refs/heads/develop && echo "PRECONDITION-LOST: a real branch develop exists"
  git rev-parse --verify --quiet refs/remotes/origin/develop >/dev/null 2>&1 && echo "PRECONDITION-LOST: origin/develop still resolves"
  git rev-parse --verify --quiet refs/heads/develop >/dev/null 2>&1 || echo "PRECONDITION-LOST: the tag does not capture refs/heads/develop"
  git push origin dev/hijack 2>&1
  git ls-remote origin refs/heads/dev/hijack | grep -q . && echo "PUSH-LANDED"
)"
if printf '%s' "$s13_out" | grep -q 'PRECONDITION-LOST'; then
  bad "S13 preconditions hold" "$(printf '%s' "$s13_out" | grep 'PRECONDITION-LOST' | tr '\n' ';')"
else
  ok "S13 preconditions hold - a tag named refs/heads/develop captures that name, with no local develop and no origin/develop"
fi
if printf '%s' "$s13_out" | grep -q 'PUSH-LANDED' && printf '%s' "$s13_out" | grep -q '\[preflight\] ran'; then
  ok "S13 a tag named refs/heads/develop is not the base - a Blockchain/Dev change behind it still runs the preflight"
else
  bad "S13 a tag named refs/heads/develop is not the base - a Blockchain/Dev change behind it still runs the preflight" "landed=$(printf '%s' "$s13_out" | grep -c PUSH-LANDED) preflight-ran=$(printf '%s' "$s13_out" | grep -c '\[preflight\] ran')"
fi
printf '\n  %d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
exit 0
