# pr_checks_newest.py: reads a GitHub check-runs JSON on stdin, prints the NEWEST run per check name as
# "status<TAB>conclusion<TAB>name" (used by pr_checks_wait.sh; a re-trigger leaves older runs beside the new ones).
import json, sys
runs = json.load(sys.stdin)["check_runs"]
newest = {}
for c in runs:
    k = c["name"]
    if k not in newest or (c.get("started_at") or "") > (newest[k].get("started_at") or ""):
        newest[k] = c
for k in sorted(newest):
    c = newest[k]
    print("%s\t%s\t%s" % (c["status"], c.get("conclusion") or "-", k))
