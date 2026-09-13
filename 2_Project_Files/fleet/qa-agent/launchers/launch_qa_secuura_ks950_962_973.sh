#!/bin/bash
# launch_qa_secuura_ks950_962_973.sh — cross-project QA agent, TIER 1 (through code; a boot-path
# statement that WRITES the users table on api-gateway — PII/data integrity; no rendered surface, so the
# real-browser half of tier 1 does not apply) gate ROUND 1 on Secuura KS-950 / KS-962, PR #973
# @ dfed981d0, ONE commit whose parent IS origin develop 0f69129b3 (= #932's squash, M6).
#
# The seed half: the api-gateway's main-DB user statement was `INSERT … ON CONFLICT (email)` (42P10 on
# every boot on the deployed schema; logged at debug). #928 (HELD by Wednesday 2026-09-12) re-pointed it
# to `ON CONFLICT (id)` — the shape KS-962 records as REVERTED by Kam's `split` ruling of 2026-09-07
# 12:13, because it writes PLAINTEXT into an encrypted users.email. #973 follows KS-962's RATIFIED shape:
# `UPDATE users … FROM (VALUES twelve (id, tenant_id, tenant_slug)) … WHERE u.id = v.id::uuid AND
# (IS DISTINCT FROM guard)` — creates no row, names no PII/role/status column, catch at warn. The loader
# half: #928's `{applied, failed}` file loader + INCOMPLETE wording on top of #932's MigrateResult.
# Plus the returned 26-cell suite scripts/__tests__/ks949_main_seed_idempotence.test.sh on a real
# socket-only PostgreSQL. TWO files +443 −31. The gate MEASURES against the TICKET's shape, not the
# builder's paraphrase, and honours the #928 HOLD (Peter's consolidated comment 5601372608).
#
# Adapted from launch_qa_secuura_ks1062_932.sh (the tier-1 gate on the SAME file) by gen_launcher_973.py
# (asserted substitutions, three asserted insertions, residual guard): same guards and exit codes,
# re-pointed at #973, plus a develop pin (exit 18) as in the #969 set.
#
# The develop pin is DELIBERATELY strict: #973's parent is develop's tip, so the brief's merged-tree ask
# is a fast-forward at 0f69129b3. If develop moves (another seat's squash lands first), this launcher
# REFUSES with exit 18 — the installer confirms the new develop delta is disjoint from the two files by
# name (startup-migrations.ts is touched by nothing else live) and re-pins DEVELOP_SHA in the launcher AND
# the brief's TARGET section AND the prompt; that is a different brief, so it must be a deliberate edit.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks950_962_973.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA973_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-973-ks950-ks962-tier1.md}"
PROMPT_FILE="${QA973_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-973-ks950-ks962-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-950-the-boot-seed-dies-permanently-at-boot-2-migration-030-drops'
HEAD_SHA="${QA973_HEAD:-dfed981d00603b68da24298086b43188fba15380}"
MERGE_BASE='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
DEVELOP_SHA='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-973-ks950-ks962-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read the merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }

if ! git -C "$REPO" ls-remote origin refs/heads/develop | grep -q "^${DEVELOP_SHA}[[:space:]]"; then
  echo "REFUSING: origin develop is not at $DEVELOP_SHA (#973's parent, M6) — the brief's base and merged-tree asks are pinned to it; confirm the new delta is disjoint from the two files by name, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
  git -C "$REPO" ls-remote origin refs/heads/develop >&2
  exit 18
fi

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  origin develop still $DEVELOP_SHA (#973's parent, M6; git ls-remote)"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA973_BRIEF:-}${QA973_PROMPT:-}${QA973_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
