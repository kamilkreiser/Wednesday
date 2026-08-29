#!/bin/bash
# board_watch_peter.sh — emit one line per event on the Secuura board (KS+PS), CLASSIFIED.
# Built 2026-08-28 22:2x on Kam's "Peter is active, keep monitoring them as they come through".
# REWRITTEN 2026-08-30 (consolidation; ledger w=44 2026-08-29): the first version printed every
# actor-less updatedAt bump as "KS WALK (no comment — review/automation?)", and I carried that
# LABEL into a mail as the event — the bump was a Linear BACKLINK (relationChanges `ar → KS-nnn`)
# created by a comment, not a state walk. Now every bump is read from the issue's HISTORY API and
# printed as what it is, with its actor:
#   PETER COMMENT <id> ...            his comments (name starts with "peter")
#   COMMENT <id> by <actor>           anyone else's comment
#   STATE <id> <from> -> <to> by <actor|automation>
#   RELATION <id> <type>-><target> by <actor>   (ar = backlink from a comment/description mention)
#   OTHER <id> by <actor>             history entry with none of the above (labels/attachments/etc.)
#   UNEXPLAINED BUMP <id>             updatedAt moved but no history entry in the window — READ IT
# Run via the Monitor tool (persistent): board_watch_peter.sh "$(date -u +%Y-%m-%dT%H:%M:%SZ)" 120
# Third arg non-empty = run once and exit (exercise / positive control).
# Key sourced transiently each poll (read-only grant); never written anywhere. stderr never discarded.
ENV="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
SINCE="${1:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"; INTERVAL="${2:-120}"; ONCE="${3:-}"
while :; do
  NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( set -a; . "$ENV"; set +a; python3 - "$SINCE" <<'PY' 2>>"$HOME/.peter_watch.err" || echo "peter_watch: poll error $(date +%H:%M) (see ~/.peter_watch.err)"
import os,sys,json,urllib.request
since=sys.argv[1]
def gql(q,v):
    r=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":v}).encode(),
        headers={"Authorization":os.environ["LINEAR_API_KEY"],"Content-Type":"application/json"})
    d=json.load(urllib.request.urlopen(r,timeout=40))
    if "errors" in d: raise SystemExit("peter_watch: GraphQL errors "+json.dumps(d["errors"])[:300])
    return d["data"]
q='''query($a:DateTimeOrDuration!){ issues(first:50, filter:{ team:{key:{in:["KS","PS"]}}, updatedAt:{gt:$a} }){
  pageInfo{hasNextPage} nodes{ identifier title state{name} updatedAt
    comments(first:50){nodes{createdAt user{name} body}}
    history(first:25){nodes{createdAt actor{name} fromState{name} toState{name} relationChanges{identifier type} addedLabelIds removedLabelIds attachment{title}}} } } }'''
d=gql(q,{"a":since})["issues"]
if d["pageInfo"]["hasNextPage"]: print("peter_watch: MORE PAGES since",since,"— read the board directly")
def nm(x): return (x or {}).get("name") or "automation"
for n in sorted(d["nodes"],key=lambda x:x["updatedAt"]):
    i=n["identifier"]; st=n["state"]["name"]; t=n["title"][:60]
    explained=False
    for c in n["comments"]["nodes"]:
        if c["createdAt"]<=since: continue
        explained=True; who=nm(c["user"]); body=c["body"][:140].replace("\n"," ")
        if who.lower().startswith("peter"): print(f"PETER COMMENT {i} [{st}] {c['createdAt'][11:16]}Z: {body}")
        else: print(f"COMMENT {i} [{st}] by {who} {c['createdAt'][11:16]}Z: {body}")
    for h in n["history"]["nodes"]:
        if h["createdAt"]<=since: continue
        explained=True; who=nm(h["actor"]); ts=h["createdAt"][11:16]+"Z"
        if h["fromState"] or h["toState"]:
            print(f"STATE {i} {nm(h['fromState'])} -> {nm(h['toState'])} by {who} {ts} {t}")
        elif h["relationChanges"]:
            rc=", ".join(f"{r['type']}->{r['identifier']}" for r in h["relationChanges"])
            print(f"RELATION {i} {rc} by {who} {ts}")
        else:
            print(f"OTHER {i} by {who} {ts} (labels/attachment/other field)")
    if not explained: print(f"UNEXPLAINED BUMP {i} [{st}] {n['updatedAt'][11:16]}Z {t} — read it")
PY
  )
  SINCE="$NOW"; [ -n "$ONCE" ] && exit 0; sleep "$INTERVAL"
done
