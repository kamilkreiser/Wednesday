#!/bin/bash
# board_watch_peter.sh — built 2026-08-28 22:2x on Kam's "Peter is active, keep monitoring them as they come through".
# Run via the Monitor tool (persistent): board_watch_peter.sh "$(date -u +%Y-%m-%dT%H:%M:%SZ)" 120
# Exercised before arming: positive control from 09:00Z showed real Peter comments; quiet control silent.
# Emits: PETER COMMENT <ticket> … (his comments) and KS WALK … (state moves without a comment = review submissions / automation / our own agents — READ, do not assume Peter).
# peter_watch.sh — emit one line per Peter event on the Secuura board (KS+PS).
# Key sourced transiently each poll (read-only grant); never written anywhere.
ENV="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
SINCE="${1:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"; INTERVAL="${2:-120}"; ONCE="${3:-}"
while :; do
  NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  ( set -a; . "$ENV"; set +a; python3 - "$SINCE" <<'PY' 2>>"$HOME/.peter_watch.err" || echo "peter_watch: poll error $(date +%H:%M) (see ~/.peter_watch.err)"
import os,sys,json,urllib.request
since=sys.argv[1]
q='''query($a:DateTimeOrDuration!){ issues(first:50, filter:{ team:{key:{in:["KS","PS"]}}, updatedAt:{gt:$a} }){ pageInfo{hasNextPage} nodes{ identifier title state{name} updatedAt comments(first:50){nodes{createdAt user{name} body}} } } }'''
r=urllib.request.Request("https://api.linear.app/graphql",data=json.dumps({"query":q,"variables":{"a":since}}).encode(),headers={"Authorization":os.environ["LINEAR_API_KEY"],"Content-Type":"application/json"})
d=json.load(urllib.request.urlopen(r,timeout=40))["data"]["issues"]
if d["pageInfo"]["hasNextPage"]: print("peter_watch: MORE PAGES since",since,"— read the board directly")
for n in sorted(d["nodes"],key=lambda x:x["updatedAt"]):
    new=[c for c in n["comments"]["nodes"] if c["createdAt"]>since]
    pc=[c for c in new if (c["user"] or {}).get("name","").startswith("peter")]
    for c in pc: print(f"PETER COMMENT {n['identifier']} [{n['state']['name']}] {c['createdAt'][11:16]}Z: {c['body'][:140].replace(chr(10),' ')}")
    if not new and n["updatedAt"]>since and n["identifier"].startswith("KS"):
        print(f"KS WALK (no comment — review/automation?) {n['identifier']} -> [{n['state']['name']}] {n['updatedAt'][11:16]}Z {n['title'][:60]}")
PY
  )
  SINCE="$NOW"; [ -n "$ONCE" ] && exit 0; sleep "$INTERVAL"
done
