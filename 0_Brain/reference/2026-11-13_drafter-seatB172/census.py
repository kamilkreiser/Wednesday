import subprocess,json
C="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172/clone"
def g(*a,raw=False):
    r=subprocess.run(["git","-C",C]+list(a),capture_output=True,check=True)
    return r.stdout if raw else r.stdout.decode("utf-8","replace")
def census(ref):
    locks=[p for p in g("ls-tree","-r","--name-only","-z",ref).split("\0") if p.endswith("package-lock.json")]
    out={}
    for p in locks:
        j=json.loads(g("show",ref+":"+p))
        pk=j.get("packages",{})
        vs=sorted({v.get("version") for k,v in pk.items() if k.endswith("node_modules/@hono/node-server")})
        if vs: out[p]=vs
    return len(locks),out
for name,ref in [("develop 9105cfdee484","origin/develop"),("2226 head","refs/remotes/pr/2226")]:
    n,o=census(ref); print(name,"tracked package-lock.json:",n,"carriers:",o)
# planted control: census function sees a synthetic lock
import io
j={"packages":{"node_modules/@hono/node-server":{"version":"9.9.9"}}}
vs=sorted({v.get("version") for k,v in j["packages"].items() if k.endswith("node_modules/@hono/node-server")})
print("planted synthetic control finds:",vs)
# numstat per file
dev=g("rev-parse","origin/develop").strip()
print(g("diff","--numstat","dc57df60a959","refs/remotes/pr/2226"))
