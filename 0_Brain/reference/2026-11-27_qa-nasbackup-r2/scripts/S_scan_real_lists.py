#!/usr/bin/env python3
# S_scan_real_lists.py — fresh checker's OWN scan of the seat's round-2 real dry-run lists (names only; no file opened).
# Written separately from nb_core.secret_shape and from the seat's tests/scan_dry_lists.py.
#   S_scan_real_lists.py <logs dir> <stamp> [--access]
# --access additionally asks the OS (os.access R_OK, lstat) whether each listed FILE is readable by this user:
# metadata only, nothing is opened. It never touches a path whose component looks like 4_credentials / 3_access_keys.
import glob, os, re, sys, collections
logs, stamp = sys.argv[1], sys.argv[2]
do_access = "--access" in sys.argv
SRC = {  # list-file suffix -> source folder (from seats/wednesday.conf set= lines)
 "WEDNESDAY": "/Volumes/DevMASTER/WEDNESDAY", "Secuura": "/Volumes/DevMASTER/!CODING/Secuura",
}
def src_for(safe):
    if safe in SRC: return SRC[safe]
    assert safe.startswith("CODING__"), safe
    return "/Volumes/DevMASTER/!CODING/" + safe[len("CODING__"):].replace("__", "/")
I = re.IGNORECASE
# (tier, label, regex on the whole relative path). tier A = the tool's own declared shapes (must be 0);
# tier B = CONVENTIONAL credential names the coordinator listed or that are in wide use; tier C = broad heuristics
# (many false positives expected: read the distinct names).
P = [
 ("A", "component contains 4_credentials / 3_access_keys", r"(4_credentials|3_access_keys)"),
 ("A", ".env* / *.env / *.env.*", r"(^|/)(\.env[^/]*|[^/]*\.env(\.[^/]*)?)(/|$)"),
 ("A", "key/cert extensions the tool lists (.pem .key .p12 .pfx .ppk .jks .keystore .kdbx .skey)", r"\.(pem|key|p12|pfx|ppk|jks|keystore|kdbx|skey)(\.[^/]*| [^/]*)?(/|$)"),
 ("A", "ssh key names id_rsa/id_dsa/id_ecdsa/id_ed25519", r"(^|/)id_(rsa|dsa|ecdsa|ed25519)[^/]*(/|$)"),
 ("A", "stores .ssh .aws .azure .gh-config .gnupg .kube", r"(^|/)\.(ssh|aws|azure|gh-config|gnupg|kube)(/|$)"),
 ("A", ".netrc .npmrc .pypirc .pgpass .git-credentials credentials.json secrets.json|yaml|yml", r"(^|/)(\.netrc|\.npmrc|\.pypirc|\.pgpass|\.git-credentials|credentials\.json|secrets\.(json|ya?ml)|service_principal_entries\.json)(/|$)"),
 ("A", "client_secret* msal_token_cache* github_deploy* *deploy[_-]key* *_deploy_rw|ro", r"(^|/)(client_secret[^/]*|msal_token_cache[^/]*|github_deploy[^/]*|[^/]*deploy[_-]key[^/]*|[^/]*_deploy_r[wo])(/|$)"),
 ("A", "terraform state (.tfstate)", r"\.tfstate"),
 ("B", "service-account*.json / service_account*.json / serviceAccount*.json / *-sa.json", r"(^|/)(service[-_ ]?account[^/]*\.json|[^/]*-sa\.json|[^/]*sa[-_]key[^/]*\.json)(/|$)"),
 ("B", ".htpasswd / htpasswd", r"(^|/)\.?htpasswd[^/]*(/|$)"),
 ("B", "terraform.tfvars / *.tfvars / *.auto.tfvars(.json)", r"\.tfvars(\.json)?(/|$)"),
 ("B", ".docker/ (config.json holds registry auth) / .dockercfg", r"(^|/)(\.docker/|\.dockercfg(/|$))"),
 ("B", "application_default_credentials.json / gcloud dirs", r"(^|/)(application_default_credentials\.json|\.config/gcloud/|gcloud/credentials)"),
 ("B", "credentials (bare) / credentials.* other than .json / *credentials*.json|yml|csv|ini", r"(^|/)(credentials|credentials\.(ya?ml|csv|ini|txt|xml|toml|db)|[^/]*credentials?[^/]*\.(json|ya?ml|csv|ini|xml))(/|$)"),
 ("B", "secrets.* other than json/yaml (toml env txt ini) / secret.json|yml / .secrets / .secret", r"(^|/)(secrets\.(toml|txt|ini|env|xml|py|js|ts)|secret\.(json|ya?ml|txt|key)|\.secrets?)(/|$)"),
 ("B", "kubeconfig / *.kubeconfig", r"(^|/)([^/]*\.)?kubeconfig[^/]*(/|$)"),
 ("B", "local.settings.json (Azure Functions) / appsettings.*.json with Secret", r"(^|/)local\.settings\.json(/|$)"),
 ("B", "token stores: .vault-token accessTokens.json azureProfile.json token.json tokens.json auth.json .boto .s3cfg", r"(^|/)(\.vault-token|accessTokens\.json|azureProfile\.json|tokens?\.json|auth\.json|\.boto|\.s3cfg|\.terraformrc|\.yarnrc\.yml)(/|$)"),
 ("B", "more key/cert containers (.der .p8 .pkcs12 .ovpn .mobileprovision .kdb .agekey .gpg .asc .cer .crt)", r"\.(der|p8|pkcs12|ovpn|mobileprovision|kdb|agekey|gpg|asc|cer|crt)(/|$)"),
 ("B", "wallet/mnemonic/seed names (mnemonic* seed-phrase* recovery-phrase* *.wallet wallet.dat keystore* UTC--*)", r"(^|/)([^/]*mnemonic[^/]*|[^/]*seed[-_ ]?phrase[^/]*|[^/]*recovery[-_ ]?phrase[^/]*|[^/]*\.wallet|wallet\.dat|keystore[^/]*|UTC--[^/]*)(/|$)"),
 ("B", "cardano key files (.vkey .skey .addr .cert .counter, *signing*key*)", r"(\.(vkey|addr)(/|$)|(^|/)[^/]*signing[-_.]?key[^/]*(/|$))"),
 ("B", "private key by name (*private*key* *privkey* *.priv)", r"(^|/)([^/]*priv(ate)?[-_. ]?key[^/]*|[^/]*\.priv)(/|$)"),
 ("C", "basename contains 'secret'", r"(^|/)[^/]*secret[^/]*$"),
 ("C", "basename contains 'password' or 'passwd'", r"(^|/)[^/]*pass(word|wd)[^/]*$"),
 ("C", "basename contains 'credential'", r"(^|/)[^/]*credential[^/]*$"),
 ("C", "basename contains 'apikey' / 'api_key' / 'api-key'", r"(^|/)[^/]*api[-_]?key[^/]*$"),
 ("C", "basename contains 'token' and is json/txt/yaml or has no extension", r"(^|/)([^/]*token[^/]*\.(json|txt|ya?ml)|[^/.]*token[^/.]*)$"),
 ("D", "OTHER CLIENT: component contains datasec", r"datasec"),
 ("D", "OTHER SEAT inside the seat tree list only: component contains tuesday or friday", None),
 ("Z", "POSITIVE CONTROL: *.md", r"\.md$"),
 ("Z", "POSITIVE CONTROL: basename contains 'env' (ordinary)", r"(^|/)[^/.][^/]*env[^/]*$"),
 ("Z", "POSITIVE CONTROL: basename contains 'key' with a code extension", r"(^|/)[^/]*key[^/]*\.(js|ts|md|json|py)$"),
]
RX = [(t, l, re.compile(r, I) if r else None) for t, l, r in P]
# unit controls: each tier-A/B pattern must fire on a synthetic name, and must not fire on an ordinary one
UNIT = {0: "a/4_Credentials (conflict)/x", 1: "a/.env.local", 2: "a/server.PEM", 3: "a/ID_RSA.pub", 4: "a/.AWS/config", 5: "a/.netrc",
        6: "a/github_deploy_rw", 7: "a/terraform.tfstate.backup", 8: "a/service-account-prod.json", 9: "a/.htpasswd", 10: "a/terraform.tfvars",
        11: "a/.docker/config.json", 12: "a/application_default_credentials.json", 13: "a/.aws2/credentials", 14: "a/secrets.toml",
        15: "a/kubeconfig", 16: "a/local.settings.json", 17: "a/token.json", 18: "a/cert.p8", 19: "a/mnemonic.txt", 20: "a/payment.vkey",
        21: "a/private_key.txt"}
unit_bad = [i for i, n in UNIT.items() if not RX[i][2].search(n)]
unit_fp = [l for t, l, rx in RX if rx is not None and t in "AB" and rx.search("src/components/Button.tsx")]
print("UNIT CONTROLS: %d synthetic secret names, %d not matched by their own pattern %s; patterns firing on 'src/components/Button.tsx': %d"
      % (len(UNIT), len(unit_bad), unit_bad, len(unit_fp)))
files = sorted(glob.glob(os.path.join(logs, "%s_dry_*.files0" % stamp)))
print("lists read: %d (stamp %s)" % (len(files), stamp))
count = collections.Counter(); ex = collections.defaultdict(list); names = collections.defaultdict(collections.Counter)
tot = 0; unread = []; missing = 0; checked = 0; nonreg = 0
for f in files:
    safe = os.path.basename(f)[len(stamp) + len("_dry_"):-len(".files0")]
    src = src_for(safe)
    seat_tree = (safe == "WEDNESDAY")
    for d in open(f, "rb").read().split(b"\0"):
        if not d: continue
        n = d.decode("utf-8", "surrogateescape"); tot += 1
        for i, (t, l, rx) in enumerate(RX):
            hit = rx.search(n) if rx is not None else (seat_tree and re.search(r"(tuesday|friday)", n, I))
            if hit:
                count[i] += 1
                names[i][os.path.basename(n).lower()] += 1
                if len(ex[i]) < 6: ex[i].append("%s :: %s" % (safe, n))
        if do_access:
            p = os.path.join(src, n)
            if re.search(r"(4_credentials|3_access_keys)", p, I): continue
            try:
                st = os.lstat(os.fsencode(p))
            except OSError:
                missing += 1; continue
            import stat as _s
            if _s.S_ISDIR(st.st_mode):
                if not os.access(os.fsencode(p), os.R_OK | os.X_OK): unread.append(("DIR", safe, n))
                continue
            if not _s.S_ISREG(st.st_mode): nonreg += 1; continue
            checked += 1
            if not os.access(os.fsencode(p), os.R_OK): unread.append(("FILE", safe, n, oct(st.st_mode & 0o7777), st.st_uid))
print("paths read in total (files and new folders): %d" % tot)
for i, (t, l, rx) in enumerate(RX):
    print("TIER %s %8d  %s" % (t, count[i], l))
    if t in "ABCD" and count[i]:
        top = names[i].most_common(12)
        print("          distinct basenames: %d; most common: %s" % (len(names[i]), "; ".join("%s x%d" % kv for kv in top)))
        for e in ex[i][:4]: print("          e.g. %s" % e)
if do_access:
    print("ACCESS CHECK (metadata only): %d listed regular files asked; %d no longer exist (changed since the dry run); %d not regular now; NOT READABLE by this user: %d"
          % (checked, missing, nonreg, len(unread)))
    for u in unread[:40]: print("   UNREADABLE %s" % (u,))
    print("ACCESS POSITIVE CONTROL: os.access on a mode-000 scratch file returns %s (must be False)" % os.access(sys.argv[sys.argv.index("--access") + 1], os.R_OK))
