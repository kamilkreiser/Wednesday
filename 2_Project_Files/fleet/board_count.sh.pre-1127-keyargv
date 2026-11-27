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
# THE TWO RULES IT ENFORCES:
#   1. if returned == requested limit, the result is TRUNCATED until proven otherwise,
#      and this script refuses to print a total. A count equal to its own limit is a
#      suspect, never a measurement.
#   2. (added 2026-09-21, RD-586) if returned == 0, the result is an UNVALIDATED ZERO
#      until a positive control proves the query's FIELD VALUES RESOLVE, and this script
#      refuses to print it. A zero from a query nobody validated is a suspect too.
#
# WHY RULE 2 (measured, not theorised). RD-586, found by the Datasec/NexusAI-C seat with
# curl BYPASSING the script: Jira's /rest/api/3/search/jql answers HTTP 200 with an EMPTY
# RESULT for a status name that does not resolve. `jira-query.sh --count` therefore returned
# a bare 0, exit 0, for two statuses whose true values were 95 and 6. Nothing errored. The
# same shape exists on the Linear path for a filter naming a state that does not exist.
#   Rule 1 and rule 2 are COMPLEMENTS: a cap is a CEILING (too low because capped); an
#   unresolvable field value is a FLOOR AT ZERO (too low because nothing matched anything
#   real). This script had the mirror of its own sentence and never wrote it down.
#   It is also clause 4 of the 2026-09-21 NexusAI floor rule in another costume:
#   A ZERO IS ONLY REPORTABLE IF A CONTROL FIRED. A test that finds nothing and a test that
#   never ran produce the same output, and so do these.
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
PAGE="${BOARD_COUNT_PAGE:-5000}"  # 2026-10-23: linear = rows per request; jira = cap on TOTAL rows fetched across pages (was 250 per request)

die() { echo "board_count: $*" >&2; exit 2; }

# BOARD_COUNT_ZERO_OK — the attestation that discharges rule 2. It is NOT a bypass: the
# caller must NAME the positive control it ran and the non-zero it returned, and that string
# is printed beside the zero so the claim is attributable. Same standing as a brief's
# SELF-CHECK line — not tamper-proof, but it makes the omission visible and the assertion owned.
ZERO_OK="${BOARD_COUNT_ZERO_OK:-}"

guard() { # $1 returned  $2 requested
  if [ "$1" -eq 0 ] && [ -z "$ZERO_OK" ]; then
    cat >&2 <<MSG
=============================================================
UNVALIDATED ZERO — refusing to report this as a total.
  returned 0, and no positive control was attested.
A zero can mean "nothing matches" or "the query named a field
value that does not resolve" — Jira answers HTTP 200 with an
empty result for the second, and Linear returns an empty node
list. Those are indistinguishable from this side. (RD-586: a
bare 0 was reported for two statuses whose true values were
95 and 6.)

Run a POSITIVE CONTROL on the SAME FIELD — a value you know
exists, which must return non-zero — then re-run with:
  BOARD_COUNT_ZERO_OK='<control query> -> <its non-zero result>'
The attestation is printed beside the zero, so it is owned.
=============================================================
MSG
    exit 1
  fi
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
  if [ "$1" -eq 0 ]; then
    echo "TOTAL=0  (UNVALIDATED-ZERO discharged by control: $ZERO_OK)"
    return
  fi
  echo "TOTAL=$1  (limit was $2, so this is a real count and not a cap)"
}

case "${1:-}" in
  linear)
    PAGE="${BOARD_COUNT_PAGE:-250}"   # linear keeps its original per-request cap (Linear max page is 250)
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
    # PAGING (2026-10-23): /rest/api/3/search/jql serves <=100 rows per page whatever maxResults says, so a board
    # over 100 was refused as "MORE PAGES EXIST". Now follows nextPageToken until isLast. Rule 1 applies to the
    # TOTAL: PAGE is the overall hard cap on rows fetched (BOARD_COUNT_PAGE), per-request size is min(PAGE,100).
    # A fetch that stops at the cap with pages still outstanding is TRUNCATED and refuses; a page that fails
    # mid-way refuses (never a partial total).
    PER=$(( PAGE < 100 ? PAGE : 100 ))
    : > /tmp/.bcj_$$
    TOKEN=""; ROWS=0
    while :; do
      if [ -n "$TOKEN" ]; then
        RESP=$(curl -sS -u "$3:$4" -H "Accept: application/json" --get "https://$2/rest/api/3/search/jql" \
                 --data-urlencode "jql=$5" --data-urlencode "maxResults=$PER" --data-urlencode "fields=status" \
                 --data-urlencode "nextPageToken=$TOKEN") || { rm -f /tmp/.bcj_$$; die "jira request failed (see stderr above)"; }
      else
        RESP=$(curl -sS -u "$3:$4" -H "Accept: application/json" --get "https://$2/rest/api/3/search/jql" \
                 --data-urlencode "jql=$5" --data-urlencode "maxResults=$PER" --data-urlencode "fields=status") \
          || { rm -f /tmp/.bcj_$$; die "jira request failed (see stderr above)"; }
      fi
      # one line per page: "<n> <isLast 0/1> <nextPageToken or ->" ; status names appended to the tally file
      META=$(echo "$RESP" | TALLY=/tmp/.bcj_$$ python3 -c '
import json,sys,os
d=json.load(sys.stdin)
if "issues" not in d: print("JIRA ERROR:", str(d)[:400], file=sys.stderr); sys.exit(3)
with open(os.environ["TALLY"],"a") as f:
    for i in d["issues"]: f.write(i["fields"]["status"]["name"]+"\n")
last = 1 if (d.get("isLast") or not d.get("nextPageToken")) else 0
print(len(d["issues"]), last, d.get("nextPageToken") or "-")
') || { rm -f /tmp/.bcj_$$; exit 3; }
      N=${META%% *}; REST=${META#* }; LAST=${REST%% *}; TOKEN=${REST#* }
      ROWS=$((ROWS+N))
      [ "$LAST" = 1 ] && break
      if [ "$ROWS" -ge "$PAGE" ]; then
        rm -f /tmp/.bcj_$$
        cat >&2 <<MSG
=============================================================
TRUNCATION SUSPECTED - refusing to report this as a total.
  fetched $ROWS rows (cap $PAGE) and Jira still reports more pages.
Raise BOARD_COUNT_PAGE (cap on TOTAL rows) or narrow the JQL.
=============================================================
MSG
        exit 1
      fi
      [ "$N" -gt 0 ] || { rm -f /tmp/.bcj_$$; die "jira returned an empty page with more pages pending - refusing"; }
    done
    sort /tmp/.bcj_$$ | uniq -c | sort -rn | sed 's/^ *\([0-9]*\) /  \1  /' >&2
    rm -f /tmp/.bcj_$$
    # a complete fetch at exactly the cap is still valid (isLast was true), so the guard's ">= limit" test uses cap+1
    guard "$ROWS" "$((PAGE+1))"
    ;;
  *) die "usage: board_count.sh linear|jira ..." ;;
esac
