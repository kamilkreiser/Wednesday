# pr_checks_newest.py: reads a GitHub check-runs JSON on stdin, prints the NEWEST run per check name as
# "status<TAB>conclusion<TAB>name" (used by pr_checks_wait.sh; a re-trigger leaves older runs beside the new ones).
#
# --mixed (2026-11-18, ledger _ledger_laptop_datasec.md 2026-11-18 s287 row): instead prints one line
# "MIXED<TAB>name<TAB>newest=<conclusion><TAB>older-not-green=<conclusions>" for every name whose NEWEST run is
# green (success/neutral/skipped) while an OLDER completed run of the same name is not. On NexusAI #220 one head
# carried two audit-production-deps runs, a success and a failure; newest-per-name alone can read that green.
import json, sys
GREEN = ("success", "neutral", "skipped")
runs = json.load(sys.stdin)["check_runs"]
by_name = {}
for c in runs:
    by_name.setdefault(c["name"], []).append(c)
key = lambda c: (c.get("started_at") or "")
if "--mixed" in sys.argv[1:]:
    for k in sorted(by_name):
        rs = sorted(by_name[k], key=key)
        newest = rs[-1]
        if (newest.get("conclusion") or "-") not in GREEN:
            continue
        older_bad = [r.get("conclusion") or "-" for r in rs[:-1]
                     if r.get("status") == "completed" and (r.get("conclusion") or "-") not in GREEN]
        if older_bad:
            print("MIXED\t%s\tnewest=%s\tolder-not-green=%s" % (k, newest.get("conclusion"), ",".join(older_bad)))
    sys.exit(0)
for k in sorted(by_name):
    c = max(by_name[k], key=key)
    print("%s\t%s\t%s" % (c["status"], c.get("conclusion") or "-", k))
