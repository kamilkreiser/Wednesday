#!/usr/bin/env python3
# B2 — READ-ONLY scan of the seat's own real dry-run file lists (logs/wednesday/*_dry_*.files0: the exact NUL-separated
# list of paths the engine WOULD have been handed on 2026-11-27 12:59). Names only; no file on the drive is opened.
# Question: does that list contain secret-shaped or other-client/other-seat names the fixed exclusions missed?
import glob, os, re, sys
logs = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/nas-backup/logs/wednesday"
cats = [
 ("CONTROL: ordinary .md files (must be > 0)", re.compile(r"\.md$")),
 ("component matches 4_credentials / 3_access_keys, any case or decoration", re.compile(r"(?i)(4_credentials|3_access_keys)")),
 ("basename .env-like, any case (.env, .ENV, .env.x, x.env, .envrc, env.bak ...)", re.compile(r"(?i)(^|/)([^/]*\.env(\.[^/]*)?|\.env[^/]*|\.envrc)$")),
 ("key / cert material by extension, any case (.pem .key .p12 .pfx .ppk .jks .keystore .kdbx .crt .cer .skey .vkey)", re.compile(r"(?i)\.(pem|key|p12|pfx|ppk|jks|keystore|kdbx|skey)$")),
 ("ssh key names, any case (id_rsa id_ed25519 deploy_key github_deploy)", re.compile(r"(?i)(^|/)(id_(rsa|ed25519|ecdsa|dsa)|[^/]*deploy_?key|github_deploy)[^/]*$")),
 ("basename has secret / credential / token / passw (any case)", re.compile(r"(?i)(^|/)[^/]*(secret|credential|token|passw)[^/]*$")),
 ("cloud / tool credential stores (.azure .aws .ssh .gnupg .kube .docker .gh-config), any case, as a component", re.compile(r"(?i)(^|/)\.(azure|aws|ssh|gnupg|kube|docker|gh-config)(/|$)")),
 ("component contains datasec (any case)", re.compile(r"(?i)datasec")),
 ("component contains tuesday or friday (any case)", re.compile(r"(?i)(tuesday|friday)")),
 ("path contains conflict_on_", re.compile(r"(?i)conflict_on_")),
 ("cardano signing keys (.skey)", re.compile(r"(?i)\.skey$")),
]
files = sorted(glob.glob(os.path.join(logs, "*_dry_*.files0")))
print("lists read: %d" % len(files))
tot = 0
hits = dict((c[0], []) for c in cats)
per = {}
for f in files:
    setname = os.path.basename(f).split("_dry_", 1)[1][:-7]
    data = open(f, "rb").read().split(b"\0")
    names = [d.decode("utf-8", "replace") for d in data if d]
    tot += len(names)
    for n in names:
        for label, rx in cats:
            if rx.search(n):
                hits[label].append(setname + " :: " + n)
print("paths read in total (files and new folders): %d" % tot)
for label, _ in cats:
    h = hits[label]
    print("\n== %s: %d" % (label, len(h)))
    seen = {}
    for x in h:
        base = x.rsplit("/", 1)[-1] if "CONTROL" not in label else ""
        seen.setdefault(x.split(" :: ")[0], 0)
        seen[x.split(" :: ")[0]] += 1
    print("   per set: %s" % ", ".join("%s=%d" % kv for kv in sorted(seen.items())))
    if "CONTROL" in label:
        continue
    for x in h[:14]:
        print("   " + x[:230])
