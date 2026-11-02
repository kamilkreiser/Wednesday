import json, subprocess, sys
R = sys.argv[1]; BASE = sys.argv[2]; HEAD = sys.argv[3]
locks = ["Blockchain/Dev/package-lock.json", "Blockchain/Dev/packages/shared/package-lock.json", "Blockchain/Dev/services/m365-integration/package-lock.json"]
def load(sha, p):
    return json.loads(subprocess.check_output(["git", "-C", R, "show", f"{sha}:{p}"]))
for p in locks:
    b = load(BASE, p)["packages"]; h = load(HEAD, p)["packages"]
    print("==", p, "entries base", len(b), "head", len(h))
    for k in sorted(set(b) | set(h)):
        eb, eh = b.get(k), h.get(k)
        if eb == eh: continue
        if eb is None: print("  ADDED  ", k, eh.get("version"), "hasInstallScript" if eh.get("hasInstallScript") else "", eh.get("resolved","(no resolved)")); continue
        if eh is None: print("  REMOVED", k, eb.get("version")); continue
        keys = sorted(x for x in set(eb)|set(eh) if eb.get(x) != eh.get(x))
        print("  CHANGED", k, eb.get("version"), "->", eh.get("version"), "fields:", keys, "INSTALLSCRIPT" if eh.get("hasInstallScript") else "")
    # resolved hosts at head
    bad = [ (k, e.get("resolved")) for k, e in h.items() if e.get("resolved") and not e["resolved"].startswith("https://registry.npmjs.org/") and not e.get("link")]
    print("  non-registry resolved at head:", len(bad), bad[:5])
    badb = [ (k, e.get("resolved")) for k, e in b.items() if e.get("resolved") and not e["resolved"].startswith("https://registry.npmjs.org/") and not e.get("link")]
    print("  non-registry resolved at base:", len(badb))
    print("  hasInstallScript count base", sum(1 for e in b.values() if e.get("hasInstallScript")), "head", sum(1 for e in h.values() if e.get("hasInstallScript")))
    # who depends on version-changed packages (other than closure)
    for name in ["bundle-name","default-browser","is-wsl","is-docker","is-inside-container","wsl-utils","open","define-lazy-prop","default-browser-id","run-applescript","powershell-utils","is-in-ssh","@azure/core-process","@azure/msal-common","@azure/msal-node"]:
        deps = [k for k, e in h.items() if name in (e.get("dependencies") or {}) or name in (e.get("optionalDependencies") or {}) or name in (e.get("peerDependencies") or {})]
        print("   dependents@head of", name, ":", deps)
