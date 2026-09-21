#!/bin/bash
# board_count.sh — count a tracker query WITHOUT letting a row cap become a total.
#
# WHY THIS EXISTS (enforcement, not advice): ledger w=5, 2026-08-14.
# Twice in one day I put a number into a brief that my own data did not support.
#   - Secuura: wrote "twelve merged-unshipped" when my own Linear query had
#     returned FOURTEEN thirty minutes earlier.
#   - NexusAI: ran `maxResults=30` with an ORDER BY, then wrote "30 open issues"
#     into the brief. The board holds 46 — and because of the ordering, the 16
#     dropped were exactly the Testing + Release Ready states, which is the half
#     of the board I then assigned the agent as work while never having seen it.
# Both were caught by the receiving agent, not by me. The provenance gate cannot
# catch this class: the PROVENANCE line cited a real query, honestly, and the
# query ran. The defect was that the number in the prose was the cap, not the
# count. So the rule "state the bound" becomes a script that states it for me.
#
# THE ONE RULE IT ENFORCES:
#   if returned == requested limit, the result is TRUNCATED until proven otherwise,
#   and this script refuses to print a total. A count equal to its own limit is a
#   suspect, never a measurement.
#
# Usage:
#   board_count.sh linear <api-key-env-var> '<GraphQL filter OBJECT — unquoted keys, e.g. { team: { key: { eq: "WED" } } }>'  (NOT JSON: it is spliced raw into the query)
#   board_count.sh jira   <site> <email> <token> '<jql>'
#
# Never prints or stores a key. stderr is never discarded (ledger 2026-08-06).
set -uo pipefail

# Deliberately far above any board we run; the guard below is the real check.
# Overridable ONLY so the refuse path can be exercised against a live board —
# a gate whose failure branch has never run is a gate I have shipped broken twice
# (2026-08-14: a `-i` flag made the path gate pass everything; `cycle` reported
# "no child" on a search that never ran). Both were found by forcing the branch.
PAGE="${BOARD_COUNT_PAGE:-250}"

die() { echo "board_count: $*" >&2; exit 2; }

guard() { # $1 returned  $2 requested
  if [ "$1" -ge "$2" ]; then
    cat >&2 <<MSG
=============================================================
TRUNCATION SUSPECTED — refusing to report this as a total.
  returned ($1) >= requested limit ($2)
A count equal to its own limit is a cap, not a measurement.
Re-run with a higher limit or page through before quoting it.
=============================================================
MSG
    exit 1
  fi
  echo "TOTAL=$1  (limit was $2, so this is a real count and not a cap)"
}

case "${1:-}" in
  linear)
    [ $# -eq 3 ] || die "usage: board_count.sh linear <KEY_ENV_VAR> '<GraphQL filter object, unquoted keys — NOT JSON>'"
    KEY="${!2:-}"; [ -n "$KEY" ] || die "env var $2 is empty — source the project's .env first"
    Q="{ issues(first:$PAGE, filter:$3) { nodes { identifier } pageInfo { hasNextPage } } }"
    BODY=$(python3 -c 'import json,sys; print(json.dumps({"query":sys.argv[1]}))' "$Q")
    RESP=$(curl -sS -X POST https://api.linear.app/graphql \
             -H "Authorization: $KEY" -H "Content-Type: application/json" -d "$BODY") \
      || die "linear request failed (see stderr above)"
    echo "$RESP" | python3 -c '
import json,sys
d=json.load(sys.stdin)
if "errors" in d: print("LINEAR ERRORS:", json.dumps(d["errors"])[:400], file=sys.stderr); sys.exit(3)
i=d["data"]["issues"]
if i["pageInfo"]["hasNextPage"]:
    print("MORE PAGES EXIST — this is not a total.", file=sys.stderr); sys.exit(1)
print(len(i["nodes"]))
' > /tmp/.bc_$$ || { rm -f /tmp/.bc_$$; exit 1; }
    guard "$(cat /tmp/.bc_$$)" "$PAGE"; rm -f /tmp/.bc_$$
    ;;
  jira)
    [ $# -eq 5 ] || die "usage: board_count.sh jira <site> <email> <token> '<jql>'"
    RESP=$(curl -sS -u "$3:$4" -H "Accept: application/json" \
             --get "https://$2/rest/api/3/search/jql" \
             --data-urlencode "jql=$5" --data-urlencode "maxResults=$PAGE" \
             --data-urlencode "fields=status") \
      || die "jira request failed (see stderr above)"
    echo "$RESP" | python3 -c '
import json,sys,collections
d=json.load(sys.stdin)
if "issues" not in d: print("JIRA ERROR:", str(d)[:400], file=sys.stderr); sys.exit(3)
if d.get("nextPageToken"): print("MORE PAGES EXIST — this is not a total.", file=sys.stderr); sys.exit(1)
iss=d["issues"]
for k,v in sorted(collections.Counter(i["fields"]["status"]["name"] for i in iss).items(), key=lambda x:-x[1]):
    print(f"  {v:>4}  {k}", file=sys.stderr)
print(len(iss))
' > /tmp/.bc_$$ || { rm -f /tmp/.bc_$$; exit 1; }
    guard "$(cat /tmp/.bc_$$)" "$PAGE"; rm -f /tmp/.bc_$$
    ;;
  *) die "usage: board_count.sh linear|jira ..." ;;
esac
