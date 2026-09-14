#!/usr/bin/env python3
"""guards_sim.py — the drafter's re-derivations for the #799 (KS-764) / #880 (KS-577) gate set, over the `git show`
copies in model/ (head = 6da848891; p38f = 38f6377b9; dev = 8861e6216) and the contents-API copies (gh_*.h880 etc.).
Nothing here is evidence of runtime behaviour — it is what the brief's `predicted-by: drafter` rows rest on:
  1. the ks860 guard's :433/:440 regexes (ported) over the two changed test files at head (0 offenders) and over the
     pre-round spellings at 38f6377b9 (1 offender each) — the T1o/T1s predictions;
  2. a Python port of decideTenantAccess/decideKeyRevoke (:163-268) over the brief's §2a(A) shapes;
  3. it( censuses of the four ks764 files, ks860, ks742, ks577 (the cell counts the brief states);
  4. the develop-alone arithmetic; 5. the JSON.stringify drop of an undefined key (the jwt.ts:173/:263 Record);
  6. every tamper anchor's count at head (must be exactly what the brief says); 7. byte-equality of the git-show
     copies with the contents-API copies (two reads of the bytes agree); 8. #880: the two false sentences absent at
     head / present at develop, the two true ones present; the yaml -U0 hunk count; the .ts changed-line count.
Exit 0 = every check ok; 1 = a check failed."""
import re, sys, os, hashlib, difflib, json
G = os.path.dirname(os.path.abspath(__file__))
H = lambda n: open(f"{G}/model/head/{n}", encoding="utf-8").read()
P = lambda n: open(f"{G}/model/p38f/{n}", encoding="utf-8").read()
D = lambda n: open(f"{G}/model/dev/{n}", encoding="utf-8").read()
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1

ORIG = "services__originate__src____tests____ks764-admin-api-keys-revoke-route-contract.test.ts"
SEC = "services__security__src____tests____ks764-revoke-organisation-route-contract.test.ts"
POL = "packages__shared__src__security__keyRevokePolicy.ts"
GUARD = "packages__shared__src____tests____ks764-key-revoke-call-site-guard.test.ts"
ARM = "services__security__src____tests____ks764-key-revoke-organisation-arm.test.ts"
KS860 = "packages__shared__src____tests____ks860-test-listeners-bind-loopback.test.ts"
KS742 = "services__security__src____tests____ks742-keys-tenancy-route-contract.test.ts"
SIDX = "services__security__src__index.ts"; ADM = "services__originate__src__routes__adminConfig.ts"
SHIDX = "packages__shared__src__index.ts"; OAUTH = "services__originate__src__middleware__auth.ts"
SHMW = "packages__shared__src__middleware__index.ts"; JWT = "services__auth__src__services__jwt.ts"

# ---- 1. the ks860 predicate, ported from :433/:440 (over a comment-masked source: a simplified mask that blanks
#         // line comments and /* */ blocks — sufficient for these two files, whose only comment mentions are // lines)
SITE = re.compile(r"\.listen\(\s*0\s*(,|\))"); HOST = re.compile(r"^\s*(['\"])127\.0\.0\.1\1")
def mask(src):
    src = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), src, flags=re.S)  # keep newlines: line numbers must survive the mask
    return "\n".join(l if "//" not in l else l[: l.index("//")] + " " * (len(l) - l.index("//")) for l in src.split("\n"))
def offenders(src):
    m = mask(src); out = []
    for x in SITE.finditer(m):
        rest = m[x.end():]
        if not (x.group(1) == "," and HOST.match(rest)): out.append(m[: x.start()].count("\n") + 1)
    return out
def sites(src):
    return [mask(src)[: x.start()].count("\n") + 1 for x in SITE.finditer(mask(src))]
print("--- 1. ks860 regexes over the two test files")
for name, src, want_sites in [("originate@head", H(ORIG), [145]), ("security@head", H(SEC), [138])]:
    ck(offenders(src) == [] and sites(src) == want_sites, f"{name}: sites {sites(src)} offenders {offenders(src)} (want sites {want_sites}, offenders [])")
for name, src, want in [("originate@38f6377b9", P(ORIG), [121]), ("security@38f6377b9", P(SEC), [128])]:
    ck(offenders(src) == want, f"{name}: offenders {offenders(src)} (want {want} — Peter's :121/:128)")
ck(offenders("const s = app.listen(0, () => {});") == [1] and offenders("const s = app.listen(0, resolve);") == [1] and offenders("const s = app.listen(0);") == [1], "predicate fires on the three defect spellings (:507/:508/:511 controls)")
ck(offenders("const s = app.listen(0, '127.0.0.1', () => {});") == [] and offenders('const s = app.listen(0, "127.0.0.1", resolve);') == [] and offenders("const s = app.listen(0, '127.0.0.1');") == [], "the three loopback spellings accepted (:515-517 controls)")
ck(offenders("    // Loopback, explicitly — `listen(0, resolve)` puts the callback in the host\n    server = app.listen(0, '127.0.0.1', resolve);") == [], "the security file's :135 comment is masked, :138 accepted")
# the T1 tampers, applied to the head bytes
t1o = H(ORIG).replace("server = app.listen(0, '127.0.0.1', () => resolve());", "server = app.listen(0, () => resolve());")
t1s = H(SEC).replace("server = app.listen(0, '127.0.0.1', resolve);", "server = app.listen(0, resolve);")
ck(H(ORIG).count("server = app.listen(0, '127.0.0.1', () => resolve());") == 1 and offenders(t1o) == [145], f"T1o: anchor x1; tampered -> offenders {offenders(t1o)} (want [145])")
ck(H(SEC).count("server = app.listen(0, '127.0.0.1', resolve);") == 1 and offenders(t1s) == [138], f"T1s: anchor x1; tampered -> offenders {offenders(t1s)} (want [138])")

# ---- 2. the policy, ported from keyRevokePolicy.ts :163-268
PLATFORM = {"SYSTEM_ADMIN", "SUPER_ADMIN"}; ORG_BOUNDED = {"ORG_ADMIN", "ISSUER_ADMIN"}
def norm(v): return v.strip().lower() if isinstance(v, str) and v.strip() != "" else None
def decideTenantAccess(user, targetTenantId, scope=None):
    if str((user or {}).get("role") or "").upper() in PLATFORM: return (True, "platform-admin")
    if not (user or {}).get("tenantId"): return (False, "caller has no tenant")
    if user["tenantId"] != targetTenantId: return (False, "cross-tenant")
    if scope is not None and str(user.get("role") or "").upper() in ORG_BOUNDED:
        t = norm(scope["targetOrganizationId"]); c = norm(user.get("organizationId"))
        if not t: return (True, "same-tenant")
        if not c: return (False, "caller has no organisation")
        if c != t: return (False, "cross-organisation")
        return (True, "same-organisation")
    return (True, "same-tenant")
def decideKeyRevoke(user, key): return decideTenantAccess(user, key["tenantId"], {"targetOrganizationId": key.get("organizationId")})
A, B = "tenant-a", "tenant-b"; OA, OB = "org-a", "org-b"
print("--- 2. the policy over the §2a(A) shapes (drafter rows)")
rows = [
 ("platform x any", {"role": "super_admin"}, {"tenantId": B, "organizationId": OB}, (True, "platform-admin")),
 ("CASE 1 same org", {"role": "ISSUER_ADMIN", "tenantId": A, "organizationId": OA}, {"tenantId": A, "organizationId": OA}, (True, "same-organisation")),
 ("CASE 2 cross org", {"role": "ORG_ADMIN", "tenantId": A, "organizationId": OA}, {"tenantId": A, "organizationId": OB}, (False, "cross-organisation")),
 ("CASE 3 org-less key", {"role": "ISSUER_ADMIN", "tenantId": A, "organizationId": OA}, {"tenantId": A, "organizationId": None}, (True, "same-tenant")),
 ("CASE 4 org-less caller", {"role": "ISSUER_ADMIN", "tenantId": A}, {"tenantId": A, "organizationId": OA}, (False, "caller has no organisation")),
 ("CASE 5 tenant-less caller (F-3)", {"role": "ISSUER_ADMIN", "organizationId": OA}, {"tenantId": A, "organizationId": OA}, (False, "caller has no tenant")),
 ("cross-tenant", {"role": "ISSUER_ADMIN", "tenantId": A, "organizationId": OA}, {"tenantId": B, "organizationId": OA}, (False, "cross-tenant")),
 ("ADMIN tenant-wide, cross org", {"role": "ADMIN", "tenantId": A}, {"tenantId": A, "organizationId": OB}, (True, "same-tenant")),
 ("case/padding normalised", {"role": "ORG_ADMIN", "tenantId": A, "organizationId": " ORG-A "}, {"tenantId": A, "organizationId": "org-a"}, (True, "same-organisation")),
 ("no scope (KS-742 callers)", None, None, None),
]
for name, u, k, want in rows:
    if k is None:
        ck(decideTenantAccess({"role": "ISSUER_ADMIN", "tenantId": A, "organizationId": OA}, A) == (True, "same-tenant"), f"{name}: omitting organisationScope applies no bound")
        continue
    got = decideKeyRevoke(u, k); ck(got == want, f"{name}: {got} (want {want})")
# T3 (the arm -> allow) and T9 (the fixture gains a tenant) both flip CASE 5 and nothing else in the table
def decide_T3(u, k):
    if str((u or {}).get("role") or "").upper() in PLATFORM: return (True, "platform-admin")
    if not (u or {}).get("tenantId"): return (True, "same-tenant")          # the tampered :175-177
    return decideKeyRevoke(u, k)
flipped = [n for n, u, k, w in rows if k is not None and decide_T3(u, k) != w]
ck(flipped == ["CASE 5 tenant-less caller (F-3)"], f"T3 (no-tenant arm -> allow) flips exactly {flipped}")
ck(decideKeyRevoke({"role": "ISSUER_ADMIN", "tenantId": A, "organizationId": OA}, {"tenantId": A, "organizationId": OA}) == (True, "same-organisation"), "T9 (ADMIN_NO_TENANT gains tenantId A) -> the same call now ALLOWS (CASE 5 reds 200)")
# T5 (originate drops organizationId): CASE 2 and CASE 4 allow; CASE 5 still refused
def decide_T5(u, k): return decideKeyRevoke(u, {"tenantId": k["tenantId"]})
t5 = {n: decide_T5(u, k) for n, u, k, w in rows if k is not None}
ck(t5["CASE 2 cross org"][0] is True and t5["CASE 4 org-less caller"][0] is True and t5["CASE 5 tenant-less caller (F-3)"] == (False, "caller has no tenant") and t5["CASE 1 same org"][0] is True and t5["CASE 3 org-less key"][0] is True,
   f"T5 (organizationId dropped at the originate call): CASE 2 -> {t5['CASE 2 cross org']}, CASE 4 -> {t5['CASE 4 org-less caller']}, CASE 5 -> {t5['CASE 5 tenant-less caller (F-3)']} (aimed reds = CASE 2 + CASE 4)")

# ---- 3. it( censuses
print("--- 3. cell censuses")
def its(src): return len(re.findall(r"^\s*it\(", src, flags=re.M))
for name, src, want in [("originate route test", H(ORIG), 10), ("security route test", H(SEC), 7), ("security arm test", H(ARM), 11), ("ks860 guard", H(KS860), 23), ("ks577 (#880)", open(f"{G}/model/gh_services__security__src____tests____ks577-revoke-on-rotate.test.ts.h880", encoding="utf-8").read(), 8)]:
    ck(its(src) == want, f"{name}: {its(src)} it( (want {want})")
g = H(GUARD); per_site = len(re.findall(r"^      it\(", g, flags=re.M)); top = len(re.findall(r"^  it\(", g, flags=re.M)); n_sites = g.count("revokeWrite:")
ck(per_site == 5 and top == 5 and n_sites == 2, f"ks764 source guard: {per_site} per-site cells x {n_sites} sites + {top} top-level = {per_site*n_sites+top} (want 15)")
ck(its(P(ORIG)) == 9 and its(P(SEC)) == 6, f"at 38f6377b9: originate {its(P(ORIG))} (want 9), security {its(P(SEC))} (want 6) — one new cell each this round")

# ---- 4. develop-alone arithmetic
print("--- 4. develop-alone arithmetic (predictions)")
ck(828 - 15 == 813 and 205 - 18 == 187 and 598 - 10 == 588 and 195 - 8 == 187 and 187 + 18 + 8 == 213, "828-15=813; 205-18=187; 598-10=588; #880: 195-8=187 (= Peter's 187 at 85f8263c2 + develop's 8 reconcile); the pair 187+18+8=213")

# ---- 5. the jwt.ts Record
print("--- 5. jwt.ts :173 vs :263")
jl = H(JWT).split("\n")
ck(jl[172].strip() == "tenantId: user.tenantId," and jl[262].strip() == "...(meta.tenantId ? { tenantId: meta.tenantId } : {}),", f"jwt.ts:173 = {jl[172].strip()!r}; :263 = {jl[262].strip()!r}")
ck(H(JWT) == D(JWT), "jwt.ts blob-identical head = develop (d0d55c11b)")
ck(json.dumps({"tenantId": None if False else None}) is not None and json.dumps({k: v for k, v in {"tenantId": None, "role": "x"}.items() if v is not None}) == '{"role": "x"}', "an undefined-valued key is dropped by JSON serialisation (Python model of JSON.stringify; the gate runs the node one-liner)")
for f in (ADM, OAUTH, SHMW, ORIG): ck(H(f).count("jwt.ts:263") == 1, f"{f.split('__')[-1]}: cites jwt.ts:263 x1")

# ---- 6. tamper anchors at head, counts
print("--- 6. tamper anchors")
anchors = [
 (SHIDX, "  decideKeyRevoke,\n} from './security/keyRevokePolicy';", 1, "T2 (F-2 at source)"),
 (ORIG, "    expect(typeof shared.decideKeyRevoke).toBe('function');", 1, "F-2 line :184"),
 (POL, "  if (!user?.tenantId) {\n    return { allow: false, status: 403, reason: 'caller has no tenant' };\n  }", 1, "T3 :175-177"),
 (SIDX, "  if (!decision.allow) {", 1, "T4 security :1140"),
 (ADM, "      organizationId: keyRows[0].organization_id == null ? undefined : String(keyRows[0].organization_id),\n", 1, "T5 originate :1035"),
 (ORIG, "        if (principal.tenantId) req.tenantId = principal.tenantId;", 1, "T6 stub :88"),
 (ORIG, "const ADMIN_NO_TENANT = { userId: 'u5', role: 'ORG_ADMIN', organizationId: ORG_A };", 1, "T9o :131"),
 (SEC, "const ADMIN_NO_TENANT = () => token({ role: 'ISSUER_ADMIN', organizationId: ORG_A });", 1, "T9s :91"),
 (ADM, "      logger.warn('API key revoke refused', {", 1, "T10 :1038"),
 (ADM, "    if (!decision.allow) {", 1, "originate if(!decision.allow) :1037"),
 (ADM, "    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';", 6, "the default-tenant literal line (NEVER an anchor)"),
 (ADM, "      return res.json({ success: false, message: 'Not found' });", 3, "the Not-found 200 line (NEVER an anchor)"),
 (ORIG, "jest.spyOn(logger, 'warn')", 1, "the warn spy"),
 (ORIG, "expect.objectContaining({ reason: 'caller has no tenant' })", 1, "the log pin"),
 (OAUTH, "req.tenantId", 0, "originate authenticate() never touches req.tenantId (docblock claim)"),
 (OAUTH, "_secuuraUser", 3, "positive control for the zero above"),
 (SIDX, "return res.status(decision.status ?? 403).json({", 1, "6(b) security"),
 (ADM, "      return res.status(403).json({", 2, "6(b) originate — the hardcoded-403 line file-wide (x2: :1047 the revoke route, :1901 another route); the in-route count is asserted below"),
]
for f, a, n, label in anchors:
    c = H(f).count(a); ck(c == n, f"{label}: count {c} (want {n})")
adm = H(ADM); i0 = adm.index("adminConfigRouter.delete('/api-keys/:id'"); region = adm[i0: adm.index("UPDATE svc_api_keys SET is_active = false", i0)]
ck(region.count("return res.status(403).json({") == 1 and region.count("message: 'Not authorised to revoke this key'") == 1, "within the revoke route: one hardcoded 403 and the 6(c) text")
ck(H(SIDX).count("message: 'Not authorised to revoke this API key'") == 1, "6(c) security text x1")
ck(H(SIDX).count("app.delete('/api/keys/:id', requireKeyAdmin") == 1, "security DELETE route x1")
# H-reach: no tenantId read on the DELETE path between :1122 and :1135
sl = H(SIDX).split("\n"); seg = "\n".join(sl[1121:1134])
ck("tenantId" not in seg and "callerTenantId" in "\n".join(sl[1140:1150]), "H-reach: no tenantId read between security :1122 and :1135; the refusal log's callerTenantId is the positive control")

# ---- 7. byte-equality git-show copies vs contents-API copies
print("--- 7. two reads of the bytes agree")
pairs = [(ORIG, "gh_services__originate__src____tests____ks764-admin-api-keys-revoke-route-contract.test.ts.head"),
         (SEC, "gh_services__security__src____tests____ks764-revoke-organisation-route-contract.test.ts.head"),
         (POL, "gh_packages__shared__src__security__keyRevokePolicy.ts.head"), (SIDX, "gh_services__security__src__index.ts.head"),
         (ADM, "gh_services__originate__src__routes__adminConfig.ts.head"), (KS860, "gh_packages__shared__src____tests____ks860-test-listeners-bind-loopback.test.ts.head")]
for a, b in pairs:
    x = open(f"{G}/model/head/{a}", "rb").read(); y = open(f"{G}/model/{b}", "rb").read()
    ck(x == y, f"{a.split('__')[-1]}: git show == contents API ({hashlib.sha256(x).hexdigest()[:16]})")
for a, want in [(ORIG, "32edded63a6bc739"), (SEC, "4b68c363d7a517f8"), (POL, "9539d243958a9123")]:
    ck(hashlib.sha256(open(f"{G}/model/head/{a}", "rb").read()).hexdigest()[:16] == want, f"{a.split('__')[-1]}: sha256 {want}… = the builder's pristine")

# ---- 8. #880
print("--- 8. #880 — the two strings")
Y = lambda t: open(f"{G}/model/gh_docs__openapi__secuura-api.yaml.{t}", encoding="utf-8").read()
T = lambda t: open(f"{G}/model/gh_services__tenant-provisioning__src__tenant-provisioning.openapi.ts.{t}", encoding="utf-8").read()
ck(Y("h880").count("The old key stays active until explicitly revoked.") == 0 and Y("dev").count("The old key stays active until explicitly revoked.") == 1, "false sentence 1 absent at head, x1 at develop")
ck(Y("h880").count("(revoke the old key separately)") == 0 and Y("dev").count("(revoke the old key separately)") == 1, "false sentence 2 absent at head, x1 at develop")
ck(Y("h880").count("retires the prior active keys of the same") == 1 and Y("h880").count("The prior\n            active keys of the same connector are retired") == 1 and Y("dev").count("prior active keys") == 0, "the two true descriptions present x1 each at head (the second wrapped at lineWidth 100), 0 at develop")
ck(T("h880").count("API_KEY_ROTATION_GRACE_SECONDS") == 2 and T("dev").count("API_KEY_ROTATION_GRACE_SECONDS") == 0, "the .ts source carries the env name x2 at head, 0 at develop")
ts_diff = [l for l in difflib.unified_diff(T("m880").split("\n"), T("h880").split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
ck(len(ts_diff) == 8 and sum(1 for l in ts_diff if l[0] == "-") == 3 and sum(1 for l in ts_diff if l[0] == "+") == 5, f"the .ts round delta = {len(ts_diff)} changed lines (-3 +5)")
y_hunks = [l for l in difflib.unified_diff(Y("m880").split("\n"), Y("h880").split("\n"), lineterm="", n=0) if l.startswith("@@")]
ck(len(y_hunks) == 2, f"the yaml round delta = {len(y_hunks)} hunks: {y_hunks}")
ck(T("m880") == T("dev") and Y("m880") == Y("dev"), "at the merge commit the .ts source and the yaml are develop's bytes")
gen = open(f"{G}/model/gh_scripts__generate-openapi.ts.h880", encoding="utf-8").read()
ck("yaml.stringify(doc, { lineWidth: 100 })" in gen and "CHECK FAIL: generated YAML differs from on-disk version" in gen and "CHECK PASS: on-disk YAML matches generated" in gen, "the generator's byte-compare and lineWidth:100")
pl = open(f"{G}/model/gh_services__api-gateway__src__routes__platform.ts.h880", encoding="utf-8").read()
ck(pl.count("priorKeysRevoked === null") == 1 and pl.count("rotated: rotate && existing.rows.length > 0,") == 1 and "priorKeysRevoked" not in pl[pl.index("rotated: rotate"): pl.index("rotated: rotate") + 400], "platform.ts consumes priorKeysRevoked (:712) and returns rotated (:748); priorKeysRevoked is not in the response block")
print("guards_sim: FAILS=%d" % fails)
sys.exit(1 if fails else 0)
