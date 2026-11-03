import json,sys
s=json.load(sys.stdin)["services"]; n=0
for k,v in sorted(s.items()):
    e=v.get("environment") or {}
    if "GATE166_CTRL" in e:
        n+=1
        print("%-22s loads .env.local (ctrl)=y  DATABASE_URL_remote=%s  NODE_ENV=%s" % (k, "gate166rmt" in (e.get("DATABASE_URL") or ""), e.get("NODE_ENV")))
print("services:", len(s), "loading .env.local:", n)
