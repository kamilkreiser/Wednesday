#!/bin/bash
# board_sweep.sh — sweep a Linear board for AGENT-ACTIONABLE tickets, and never
# size one from its description alone.
#
# WHY THIS EXISTS (ledger 2026-09-09, work-done-and-the-board-not-saying-so at
# w=12 — the family's twelfth instance and the first to reach a BRIEF):
# Wednesday swept the KS board with an ad-hoc GraphQL query that requested
#   identifier / title / priority / state / assignee / description
# and briefed four tickets across two parallel seats. THREE OF THE FOUR WERE
# ALREADY BUILT:
#   KS-961  built as PR #887, Peter holding on one named line
#   KS-992  built as PR #904, APPROVED by Peter 2026-09-08 13:57
#   KS-993  tsconfig merged by #902, its check green
# Every ticket honestly read as unbuilt and the board honestly said In Progress
# / In Review. THE BUILT STATE LIVED IN COMMENTS AND LINKED PRs, AND NEITHER
# FIELD WAS IN THE QUERY. Two fresh seats spent their first turn correcting a
# commission instead of working it, on the morning Kam asked for throughput.
#
# The fix is not "be more careful" — it is that the fields carrying the answer
# are requested BY THE PATH. That is what this file is.
#
# Usage:
#   board_sweep.sh <TEAM_KEY> <KEY_ENV_VAR> [--json]
#     e.g.  board_sweep.sh KS LINEAR_API_KEY
# Source the project's .env first; the key is read from the named env var so it
# is never typed on a command line (2026-08-03 read-only tracker grant: keys are
# sourced transiently for the query and never copied into Wednesday's files).
#
# Exit: 0 swept · 2 usage/env · 3 API error
set -u

TEAM="${1:-}"; KEYVAR="${2:-}"; FMT="${3:-}"
[ -n "$TEAM" ] && [ -n "$KEYVAR" ] || {
  echo "usage: board_sweep.sh <TEAM_KEY> <KEY_ENV_VAR> [--json]" >&2
  echo "  e.g. board_sweep.sh KS LINEAR_API_KEY   (source the project .env first)" >&2
  exit 2; }
KEY="$(eval printf '%s' "\"\${$KEYVAR:-}\"")"
[ -n "$KEY" ] || { echo "board_sweep: env var $KEYVAR is empty — source the project's .env first" >&2; exit 2; }

# NOTE ON `first:` — this script does NOT print a total and must never be used
# to produce one. board_count.sh is the only thing that may state a board total,
# because it refuses when the result equals its own limit. This is a SAMPLE for
# triage, and it says so in its own output.
export BS_TEAM="$TEAM" BS_KEY="$KEY" BS_FMT="$FMT"
python3 - <<'PY'
import json, os, sys, urllib.request

TEAM = os.environ["BS_TEAM"]; KEY = os.environ["BS_KEY"]; FMT = os.environ.get("BS_FMT","")
LIMIT = 60

Q = """
{ issues(filter:{ team:{key:{eq:"%s"}},
                  state:{type:{in:["started","unstarted"]}} },
         first:%d, orderBy: updatedAt) {
    nodes { identifier title priority url
            state { name }
            assignee { name }
            comments(first:20) { nodes { createdAt body user { name } } }
            attachments(first:10) { nodes { title url } } } } }
""" % (TEAM, LIMIT)

req = urllib.request.Request("https://api.linear.app/graphql",
        data=json.dumps({"query": Q}).encode(),
        headers={"Authorization": KEY, "Content-Type": "application/json"})
try:
    d = json.load(urllib.request.urlopen(req, timeout=45))
except Exception as e:
    sys.stderr.write("board_sweep: API call failed: %r\n" % (e,)); sys.exit(3)
if "errors" in d:
    sys.stderr.write("board_sweep: GraphQL errors: %s\n" % json.dumps(d["errors"])[:400]); sys.exit(3)

nodes = d.get("data",{}).get("issues",{}).get("nodes",[])

# NO KEYWORD FLAG — and the reason is a defect this script had on its FIRST RUN.
# A first version scored each ticket against a word list ("approved", "merged",
# "pr #", "already"...). Exercised against a KNOWN control set — KS-961, KS-992,
# KS-993, all three verifiably already built — it flagged all three. It also
# flagged 58 of 60 tickets, INCLUDING KS-926, the one ticket that was genuinely
# open. A discriminator that fires on 97% of its input discriminates nothing;
# it is the same "check that cannot fail" shape this fleet keeps filing, wearing
# a triage costume. Secuura tickets are written in prose that quotes PR numbers
# and prior work, so the vocabulary IS the corpus.
#
# So the tool does not classify. It SHOWS the two fields the 2026-09-09 sweep
# omitted — linked PRs and the newest comment — and leaves the judgement where
# it belongs. The failure was never a missing verdict; it was never having seen
# the evidence at all.
def evidence(iss):
    prs, newest = [], None
    for a in (iss.get("attachments") or {}).get("nodes") or []:
        u = a.get("url") or ""
        if "/pull/" in u: prs.append("#" + u.rsplit("/", 1)[-1])
    cs = (iss.get("comments") or {}).get("nodes") or []
    if cs:
        c = sorted(cs, key=lambda x: x.get("createdAt") or "")[-1]
        who = ((c.get("user") or {}).get("name") or "?").split("@")[0]
        first = " ".join((c.get("body") or "").split())[:150]
        newest = "%s @ %s: %s" % (who, (c.get("createdAt") or "")[:10], first)
    return prs, newest, len(cs)

def line(n):
    a = (n.get("assignee") or {}).get("name") or "UNASSIGNED"
    return " %-9s P%s %-12s %-16s %s" % (n["identifier"], n["priority"],
            n["state"]["name"][:12], a.split("@")[0][:16], (n["title"] or "")[:58])

if FMT == "--json":
    out = {}
    for n in nodes:
        prs, newest, ncom = evidence(n)
        out[n["identifier"]] = {"prs": prs, "comments": ncom, "newest": newest}
    print(json.dumps(out, indent=1)); sys.exit(0)

print("board_sweep %s — %d returned (SAMPLE, limit %d; NOT a total — use"
      " board_count.sh for that)" % (TEAM, len(nodes), LIMIT))
print()
print("Each ticket shows its LINKED PRs and its NEWEST COMMENT, because those are")
print("the two fields the 2026-09-09 sweep omitted and they are where the built")
print("state lives. THIS TOOL DOES NOT DECIDE WHETHER A TICKET IS DONE. Open the")
print("comments before commissioning anything from a description.")
print("=" * 78)
withpr = 0
for n in nodes:
    prs, newest, ncom = evidence(n)
    print(line(n))
    if prs:
        withpr += 1
        print("             PRs: %s" % " ".join(prs))
    if newest:
        print("             last(%d): %s" % (ncom, newest))
    if not prs and not newest:
        print("             (no comments, no linked PRs)")
print("=" * 78)
print("%d of %d carry a linked PR. A ticket with a linked PR may be built, may be"
      % (withpr, len(nodes)))
print("superseded, or may be parked on a PR that was CLOSED WITHOUT MERGING — this")
print("repo has had all three. The PR number is where to look, not the answer.")
