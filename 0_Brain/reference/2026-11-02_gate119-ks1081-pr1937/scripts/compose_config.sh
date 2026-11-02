for side in base head; do
  docker compose --project-directory /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/head2_tree/Blockchain/Dev -f /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/head2_tree/Blockchain/Dev/docker-compose.yml --env-file /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/scratch_bootstrap/$side/Blockchain/Dev/.env config --format json > /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/compose_$side.json 2> /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937/logs/compose_$side.err; echo "$side rc=$?"
done
python3 -I - <<'PY'
import json
W="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate119-ks1081-pr1937"
keys=["ADMIN_USER_PASSWORD","ENABLE_DEMO_SEED","ALLOW_DEFAULT_SEED_PASSWORDS","TSA_URL","TSA_AUTH_KEY"]
res={}
for side in ("base","head"):
    try: c=json.load(open(f"{W}/logs/compose_{side}.json"))
    except Exception as e: print(side,"unparseable",e); continue
    r={}
    for sn,sv in c.get("services",{}).items():
        env=sv.get("environment",{}) or {}
        for k in keys:
            if k in env: r[(sn,k)]=("EMPTY" if env[k]=="" else "NONEMPTY")
    res[side]=r
for key in sorted(set().union(*[set(v) for v in res.values()])):
    print(key, "base=",res.get("base",{}).get(key,"ABSENT"), "head=",res.get("head",{}).get(key,"ABSENT"))
print("identical service env for the five keys:", res.get("base")==res.get("head"))
PY
