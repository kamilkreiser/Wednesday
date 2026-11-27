#!/usr/bin/env python3
# scan_dry_lists.py — an INDEPENDENT, read-only scan of one dry run's file lists (logs/<seat>/<stamp>_dry_*.files0:
# the exact NUL-separated paths the engine would be handed). Names only; no file on the drive is opened.
# It does NOT call nb_core.secret_shape: the patterns below are written separately (after the QA checker's
# B2_scan_real_dry_lists.py), so a hole in the tool's own rule is not hidden by asking the tool.
# ANSWER-2 ruling 2: "the real DRY list must show 0 secret-shaped names by a scan with a positive control".
#   scan_dry_lists.py <logs dir> <stamp>
import glob, os, re, sys
logs, stamp = sys.argv[1], sys.argv[2]
SECRET = [
 ("a component containing 4_credentials or 3_access_keys (any case, any decoration)", re.compile(r"(?i)(4_credentials|3_access_keys)")),
 ("a name starting .env, containing .env. or ending .env (any case)", re.compile(r"(?i)(^|/)(\.env[^/]*|[^/]*\.env\.[^/]*|[^/]*\.env)(/|$)")),
 ("key or certificate by extension (.pem .key .p12 .pfx .ppk .jks .keystore .kdbx .skey), any case, also before .bak", re.compile(r"(?i)\.(pem|key|p12|pfx|ppk|jks|keystore|kdbx|skey)(\.[^/]*)?(/|$)")),
 ("ssh key names (id_rsa id_ed25519 id_ecdsa id_dsa), any case", re.compile(r"(?i)(^|/)id_(rsa|ed25519|ecdsa|dsa)[^/]*(/|$)")),
 ("deploy keys and credential files (github_deploy*, *deploy_key*, .git-credentials, .netrc, .npmrc, .pypirc, .pgpass, client_secret*, credentials.json, secrets.json)", re.compile(r"(?i)(^|/)(github_deploy[^/]*|[^/]*deploy[_-]key[^/]*|\.git-credentials|\.netrc|\.npmrc|\.pypirc|\.pgpass|client_secret[^/]*|credentials\.json|secrets\.json)(/|$)")),
 ("credential stores as a component (.ssh .aws .azure .gh-config .gnupg .kube), any case", re.compile(r"(?i)(^|/)\.(ssh|aws|azure|gh-config|gnupg|kube)(/|$)")),
 ("terraform state", re.compile(r"(?i)\.tfstate")),
]
OTHER = [
 ("a component containing datasec (any case)", re.compile(r"(?i)datasec")),
]
CONTROLS = [
 ("POSITIVE CONTROL 1: ordinary .md paths (must be far above 0)", re.compile(r"(?i)\.md$")),
 ("POSITIVE CONTROL 2: names containing 'env' that are NOT secret-shaped, e.g. environment.ts (shows the scan sees env-like names)", re.compile(r"(?i)(^|/)[^/.][^/]*env[^/]*$")),
 ("POSITIVE CONTROL 3: names containing 'key' that are NOT key files, e.g. keyboard.js", re.compile(r"(?i)(^|/)[^/]*key[^/]*\.(js|ts|md|json|py)$")),
]
files = sorted(glob.glob(os.path.join(logs, "%s_dry_*.files0" % stamp)))
print("lists read: %d (stamp %s)" % (len(files), stamp))
tot = 0
count = dict((c[0], 0) for c in SECRET + OTHER + CONTROLS)
for f in files:
    for d in open(f, "rb").read().split(b"\0"):
        if not d:
            continue
        n = d.decode("utf-8", "replace")
        tot += 1
        for label, rx in SECRET + OTHER + CONTROLS:
            if rx.search(n):
                count[label] += 1
print("paths read in total (files and new folders): %d" % tot)
bad = 0
for label, _ in SECRET:
    print("SECRET-SHAPED  %7d  %s" % (count[label], label)); bad += count[label]
for label, _ in OTHER:
    print("OTHER CLIENT   %7d  %s" % (count[label], label)); bad += count[label]
ok = True
for label, _ in CONTROLS:
    print("CONTROL        %7d  %s" % (count[label], label)); ok = ok and count[label] > 0
print("RESULT: %d secret-shaped or other-client names in the list; controls %s" % (bad, "all above 0" if ok else "FAILED (a control found nothing: the scan proves nothing)"))
sys.exit(0 if (bad == 0 and ok and tot > 0) else 1)
