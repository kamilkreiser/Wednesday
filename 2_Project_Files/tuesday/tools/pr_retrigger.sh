#!/bin/bash
# pr_retrigger.sh <owner/repo> <pr number> [max-reopens]
# pr_retrigger.sh --check <owner/repo> <run id> <head sha> [expected main sha]
#
# Re-runs a PR's pull_request CI against CURRENT main and PROVES which merge ref the run built, by the
# job log's checkout line `HEAD is now at <sha> Merge <head> into <base>`. Uses the caller's GH_CONFIG_DIR.
#
# WHY (ledger _ledger_laptop_datasec.md 2026-10-27 stale-merge-ref REGRESSION w=3, rows 10-24 #207, 10-26 #224,
# 10-27 #230): three times a close+reopen was used as the recompute trigger and the run built the OLD merge ref,
# because the run reads whatever refs/pull/<n>/merge GitHub holds at the event, and the API's answer a second
# later is not that ref. pr_checks_wait.sh then reported ALL GREEN on a merge nobody meant to test.
#
# Default mode: reads main and the PR head; if the PR's merge_commit_sha already has current main as its first
# parent it still re-triggers (the existing checks predate the move or the caller would not be here); closes and
# reopens the PR; waits for the NEW pull_request run on the head (created after the reopen); waits until its first
# job completes; reads that job's log for the Merge line. Names current main -> prints OK and the run id, rc 0.
# Names another base -> reopens again, up to max-reopens (default 2) -> rc 3 STALE. Head moved -> rc 2.
# Then run pr_checks_wait.sh as usual: this tool proves WHICH merge was built, not that it passed.
#
# --check mode: reads one existing run's job log and compares its Merge line with <expected main> (default: the
# repo's main now). rc 0 MATCH, rc 3 STALE, rc 4 no Merge line found (a false absence: say so, never "match").
# Read verbs only in --check mode. Default mode WRITES (close/reopen of the PR): run it only on a PR you own.
set -u
WAIT_RUN=${PR_RETRIGGER_WAIT_RUN:-300}     # seconds to wait for the new run to appear
WAIT_JOB=${PR_RETRIGGER_WAIT_JOB:-1500}    # seconds to wait for its first job to complete

merge_line() { # <repo> <run id> -> prints the first "HEAD is now at ... Merge" line of any completed job
  local repo=$1 rid=$2 j
  for j in $(gh api "repos/$repo/actions/runs/$rid/jobs?per_page=50" --jq '.jobs[]|select(.status=="completed")|.id'); do
    local l
    # `gh api .../jobs/<id>/logs` REFUSES bodies holding terminal escapes (exercised 2026-10-27 05:3x: 0 lines,
    # "pass --allow-escape-sequences"), which read as a false absence; `gh run view --job` prints them.
    l=$(gh run view -R "$repo" --job "$j" --log 2>&1 | /usr/bin/grep -i -m1 -o -E 'HEAD is now at [0-9a-f]+ Merge [0-9a-f]{40} into [0-9a-f]{40}')
    if [ -n "$l" ]; then printf '%s\n' "$l"; return 0; fi
  done
  return 1
}

judge() { # <line> <head> <main> -> rc 0 match, 3 stale (prints verdict)
  local line=$1 head=$2 main=$3 base
  base=$(printf '%s' "$line" | sed -E 's/.* into ([0-9a-f]{40}).*/\1/')
  case "$line" in *"Merge $head into "*) ;; *) echo "WRONG HEAD in the Merge line (expected $head): $line"; return 3;; esac
  if [ "$base" = "$main" ]; then echo "MATCH: built Merge ${head:0:8} into ${main:0:8} (current main)"; return 0; fi
  echo "STALE: built Merge ${head:0:8} into ${base:0:8}; current main is ${main:0:8}"; return 3
}

if [ "${1:-}" = "--check" ]; then
  repo=$2; rid=$3; head=$4; main=${5:-$(gh api "repos/$repo/commits/main" --jq .sha)}
  line=$(merge_line "$repo" "$rid") || { echo "NO MERGE LINE in any completed job of run $rid (not a match; jobs may still be running)"; exit 4; }
  echo "run $rid: $line"
  judge "$line" "$head" "$main"; exit $?
fi

repo=$1; n=$2; max=${3:-2}
head=$(gh api "repos/$repo/pulls/$n" --jq .head.sha) || { echo "cannot read PR $n"; exit 1; }
for attempt in $(seq 1 "$max"); do
  main=$(gh api "repos/$repo/commits/main" --jq .sha)
  echo "$(date +%T) attempt $attempt/$max: head ${head:0:8} main ${main:0:8}"
  t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  gh pr close "$n" -R "$repo" >/dev/null && sleep 3 && gh pr reopen "$n" -R "$repo" >/dev/null || { echo "close/reopen failed"; exit 1; }
  rid=""; waited=0
  while [ -z "$rid" ] && [ $waited -lt "$WAIT_RUN" ]; do
    sleep 15; waited=$((waited+15))
    rid=$(gh api "repos/$repo/actions/runs?event=pull_request&head_sha=$head&per_page=10" \
      --jq "[.workflow_runs[]|select(.created_at >= \"$t0\")]|sort_by(.created_at)|.[0].id // empty")
  done
  [ -n "$rid" ] || { echo "no new pull_request run on ${head:0:8} within ${WAIT_RUN}s"; exit 1; }
  echo "$(date +%T) new run $rid; waiting for its first completed job"
  line=""; waited=0
  while [ -z "$line" ] && [ $waited -lt "$WAIT_JOB" ]; do
    sleep 30; waited=$((waited+30))
    now_head=$(gh api "repos/$repo/pulls/$n" --jq .head.sha)
    [ "$now_head" = "$head" ] || { echo "HEAD MOVED to ${now_head:0:8}"; exit 2; }
    line=$(merge_line "$repo" "$rid") || line=""
  done
  [ -n "$line" ] || { echo "run $rid: no completed job with a Merge line within ${WAIT_JOB}s"; exit 1; }
  echo "run $rid: $line"
  main=$(gh api "repos/$repo/commits/main" --jq .sha)
  if judge "$line" "$head" "$main"; then echo "OK run=$rid"; exit 0; fi
done
echo "STALE after $max reopen(s): do not trust run $rid"; exit 3
