#!/usr/bin/env python3
# B2b — detail of B2: distinct BASENAMES (names only, read from the seat's dry-run lists) for the .env-like and
# secret/credential/token groups, and everything under a component named secrets / .paperclip-home.
import glob, os, re, collections
logs = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup/logs/wednesday"
names = []
for f in sorted(glob.glob(os.path.join(logs, "*_dry_*.files0"))):
    s = os.path.basename(f).split("_dry_", 1)[1][:-7]
    names += [(s, d.decode("utf-8", "replace")) for d in open(f, "rb").read().split(b"\0") if d]
print("paths:", len(names))
def show(title, rx, top=45, full=False):
    c = collections.Counter(); ex = {}
    for s, n in names:
        if rx.search(n):
            b = n if full else n.rsplit("/", 1)[-1]
            c[b] += 1; ex.setdefault(b, s + " :: " + n)
    print("\n== %s: %d paths, %d distinct" % (title, sum(c.values()), len(c)))
    for b, k in c.most_common(top):
        print("  %6d  %-48s e.g. %s" % (k, b[:48], ex[b][:150]))
show(".env-like basenames", re.compile(r"(?i)(^|/)([^/]*\.env(\.[^/]*)?|\.env[^/]*|\.envrc)$"))
show("basenames with secret|credential|token|passw EXCLUDING source-code/doc/image extensions",
     re.compile(r"(?i)(^|/)[^/]*(secret|credential|token|passw)[^/]*(?<!\.ts)(?<!\.tsx)(?<!\.js)(?<!\.jsx)(?<!\.mjs)(?<!\.py)(?<!\.md)(?<!\.sh)(?<!\.webp)(?<!\.png)(?<!\.snap)(?<!\.rs)(?<!\.ak)(?<!\.go)(?<!\.html)(?<!\.css)(?<!\.map)(?<!\.d\.ts)(?<!\.svg)(?<!\.sql)(?<!\.yml)(?<!\.yaml)(?<!\.txt)(?<!\.log)(?<!\.out)(?<!\.err)$"), top=60)
show("paths under a component named secrets/ or .paperclip-home/ (full paths)", re.compile(r"(?i)(^|/)(secrets|\.paperclip-home)/"), top=30, full=True)
show("json/yaml/txt whose basename has secret|credential|token|passw", re.compile(r"(?i)(^|/)[^/]*(secret|credential|token|passw)[^/]*\.(json|ya?ml|txt|toml|ini|cfg|conf)$"), top=40)
