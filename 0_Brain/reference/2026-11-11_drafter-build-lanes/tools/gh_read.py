# Drafter 2026-11-11: READ-ONLY. gh_read.py <ref> tree <prefix>  |  gh_read.py <ref> file <path> <outfile>. GH_TOKEN from env (envrun); never printed.
import base64, json, os, sys, urllib.parse, urllib.request
H = {"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json", "User-Agent": "wed-drafter-readonly"}
B = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60))
ref, mode = sys.argv[1], sys.argv[2]
if mode == "tree":
    t = get(f"{B}/git/trees/{ref}?recursive=1")
    print("truncated:", t.get("truncated"), "entries:", len(t["tree"]))
    for e in t["tree"]:
        if e["path"].startswith(sys.argv[3]): print(e["type"][0], e["size"] if "size" in e else "", e["path"])
elif mode == "file":
    d = get(f"{B}/contents/{urllib.parse.quote(sys.argv[3])}?ref={ref}")
    t = base64.b64decode(d["content"]).decode(errors="replace")
    open(sys.argv[4], "w").write(t); print(sys.argv[3], "sha", d["sha"][:10], "bytes", len(t), "lines", t.count("\n"))
