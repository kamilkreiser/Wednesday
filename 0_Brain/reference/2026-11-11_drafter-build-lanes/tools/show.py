import json, sys
for k in sys.argv[1:]:
    i = json.load(open(f"/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_drafter-build-lanes/evidence/tickets/{k}.json"))
    c = sorted(i["comments"]["nodes"], key=lambda x: x["createdAt"], reverse=True)
    print("=====", k, i["title"], "|", i["state"]["name"], "| assignee", (i["assignee"] or {}).get("name"), "| attach", [a["url"].rsplit("/",1)[-1] for a in i["attachments"]["nodes"]])
    print((i["description"] or "")[:2600])
    for x in c[:2]:
        print("--- comment", x["id"][:8], x["createdAt"][:16]); print(x["body"][:1800])
