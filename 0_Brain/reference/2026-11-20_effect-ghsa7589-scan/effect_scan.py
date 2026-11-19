import json, sys, glob, os
n = 0; errs = 0
for f in sorted(glob.glob(sys.argv[1] + "/lk_*package-lock.json")):
    try:
        d = json.load(open(f))
    except Exception as e:
        errs += 1; print("ERR", os.path.basename(f), type(e).__name__); continue
    n += 1; out = []
    for k, v in d.get("packages", {}).items():
        if k.split("node_modules/")[-1] == "effect":
            out.append("%s @ %s" % (k, v.get("version")))
        deps = {}
        for key in ("dependencies", "peerDependencies", "optionalDependencies", "devDependencies"):
            deps.update(v.get(key, {}) or {})
        if "effect" in deps:
            out.append("pulled-by %s wants %s" % (k or "(root)", deps["effect"]))
    if out:
        print(os.path.basename(f)); [print("   ", o) for o in out]
print("parsed", n, "errors", errs)
