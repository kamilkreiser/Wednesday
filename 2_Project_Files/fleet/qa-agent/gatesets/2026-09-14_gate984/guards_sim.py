#!/usr/bin/env python3
"""guards_sim.py — Wednesday's drafter re-derivations for the #984 gate set, over the bytes read from the head tree
(model/*.head, extracted by `git show <sha>:<path>` from a --shared clone; the contents-API copies model/gh_* are
byte-compared to them first).

  1. the ks860 loopback guard's site/host regexes (:433 / :440 of the guard at develop M18 = head, blob e0dfadb9c)
     over the THREE test files #984 touches — the widened-guard rule: every new listener binds 127.0.0.1;
  2. a Python port of the gateway's requireScope / attachScopes (scopes.ts :23-92 at head) driven with the claim
     shapes jwt.ts mints at head, to derive the predictions for the gateway cells and the gate-designed tampers;
  3. the enforcement.ts :159-170 allowedAuthProviders arm, before (unlabelled -> 'email') and after ('oauth') —
     the label's third consumer, which the builder's blast radius does not name;
  4. the rateLimitEnforce.ts :61/:83 MACHINE_AUTH_METHODS membership for 'oauth'.
Exit 0 = every expectation holds · 1 = at least one failed.
"""
import re, sys, hashlib, os
G = sys.argv[1]
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1

# --- 0. the contents-API copies == the clone's copies (two instruments agree on the bytes)
for a, b in [("jwt.ts.head", "gh_jwt.ts.head"), ("oauth.ts.head", "gh_oauth.ts.head"), ("scopes.ts.head", "gh_scopes.ts.head"),
             ("ks835-auth.test.ts.head", "gh_ks835-oauth-mint-carries-granted-scope.test.ts.head"),
             ("ks835-gw.test.ts.head", "gh_ks835-oauth-token-scope-gate.test.ts.head"),
             ("ks823.test.ts.head", "gh_ks823-refresh-grant-client-auth-and-binding.test.ts.head")]:
    x = open(f"{G}/model/{a}", "rb").read(); y = open(f"{G}/model/{b}", "rb").read()
    ck(len(x) > 0 and x == y, f"{a} ({len(x)} B, sha256 {hashlib.sha256(x).hexdigest()[:16]}) == contents-API copy {b}")

# --- 1. the ks860 guard's regexes over the three test files
SITE = re.compile(r"\.listen\(\s*0\s*(,|\))"); HOST = re.compile(r"^\s*(['\"])127\.0\.0\.1\1")
def offenders(src):
    out = []
    for m in SITE.finditer(src):
        rest = src[m.end():]
        if not (m.group(1) == ',' and HOST.match(rest)):
            out.append(src[:m.start()].count('\n') + 1)
    return out
for f in ["ks835-auth.test.ts.head", "ks835-gw.test.ts.head", "ks823.test.ts.head"]:
    s = open(f"{G}/model/{f}", encoding="utf-8").read()
    sites = [s[:m.start()].count('\n') + 1 for m in SITE.finditer(s)]
    ck(len(sites) == 1 and offenders(s) == [], f"ks860 :433/:440 over {f}: listen(0 sites at {sites}, offenders {offenders(s)} (expected one site, [])")
for src, exp in [("const s = app.listen(0, () => {});", 1), ("const s = app.listen(0);", 1), ("const s = app.listen(0, '127.0.0.1');", 0), ("server = app.listen(0, '127.0.0.1', resolve);", 0)]:
    ck(len(offenders(src)) == exp, f"guard control {src!r} -> {len(offenders(src))} offender(s) (expected {exp})")
gw = open(f"{G}/model/ks835-gw.test.ts.head", encoding="utf-8").read().split('\n')
ck("app.listen(0, '127.0.0.1', resolve)" in gw[63], f"gateway test :64 = {gw[63].strip()[:90]}")
au = open(f"{G}/model/ks835-auth.test.ts.head", encoding="utf-8").read().split('\n')
ck("app.listen(0, '127.0.0.1');" in au[126], f"auth test :127 = {au[126].strip()}")

# --- 2. a port of requireScope / attachScopes (scopes.ts at head, :23-92)
def attach(user):
    if user is not None and not user.get('scopes'):
        # JS: `!user.scopes` — [] is TRUTHY in JS, so an empty array is NOT re-parsed; port that exactly
        if 'scopes' in user and isinstance(user['scopes'], list):
            return user
        s = user.get('scope') or ''
        if s:
            user['scopes'] = [x for x in re.split(r'[\s,]+', s) if x]
    return user
def require(user, *required):
    if user is None: return 401
    am = user.get('authMethod') or 'jwt'
    if am in ('jwt', 'email'): return 200
    scopes = user.get('scopes') or []
    if '*' in scopes: return 200
    return 200 if any(r in scopes for r in required) else 403
def mint(oauth=None, role_default=('documents:write',)):
    """jwt.ts generateAccessToken at head :192-207: an OAuth mint carries the granted list + 'oauth'; a login mint the role default and no label."""
    p = {'userId': 'u', 'role': 'OWNER', 'type': 'access'}
    if oauth is not None:
        p['scopes'] = list(oauth['scopes']); p['authMethod'] = 'oauth'; p['client_id'] = oauth['clientId']
    elif role_default:
        p['scopes'] = list(role_default)
    return p
def mint_parent(oauth=None, role_default=('documents:write',)):
    """jwt.ts at the PARENT f62c975c1 (:191-204 there): scopes = role default whatever the grant; no label; client_id only."""
    p = {'userId': 'u', 'role': 'OWNER', 'type': 'access'}
    if role_default: p['scopes'] = list(role_default)
    if oauth is not None: p['client_id'] = oauth['clientId']
    return p
print("--- the gateway cells, from the head mint shape")
ck(require(attach(mint({'clientId': 'c', 'scopes': ['openid']})), 'webhooks:manage') == 403, "cell 1: OAuth mint granted [openid] at requireScope('webhooks:manage') -> 403")
ck(require(attach(mint({'clientId': 'c', 'scopes': ['webhooks:manage']})), 'webhooks:manage') == 200, "cell 2: the same with webhooks:manage granted -> 200")
ck(require(attach({'authMethod': 'api_key', 'scopes': ['openid']}), 'webhooks:manage') == 403, "cell 3: sk_* key (authMethod api_key, scopes [openid]) -> 403")
ck(require(attach(mint(None)), 'webhooks:manage') == 200, "cell 4: a LOGIN mint (no label, role default) -> 200 (RBAC governs)")
ck(require(attach(mint({'clientId': 'c', 'scopes': []})), 'webhooks:manage') == 403, "cell 5: OAuth mint with an EMPTY grant (scopes: []) -> 403 (the [] is truthy in JS; attachScopes leaves it)")
u = attach({'authMethod': 'oauth', 'scopes': ['openid'], 'scope': 'webhooks:manage'}); ck(u['scopes'] == ['openid'], "cell 6a: the array wins over a singular scope string")
u = attach({'authMethod': 'oauth', 'scope': 'a:read b:write'}); ck(u['scopes'] == ['a:read', 'b:write'], "cell 6b: the legacy string is parsed when no array is present")
u = attach({'authMethod': 'oauth'}); ck('scopes' not in u, "cell 6c: nothing to read -> scopes stays undefined")
print("--- the UNFIXED product (parent mint shape) through the same gate — why H1/H2 were the defect")
ck(require(attach(mint_parent({'clientId': 'c', 'scopes': ['openid']})), 'webhooks:manage') == 200, "PARENT: an OAuth mint granted [openid] carried the role default and no label -> 200 (the ticket's defect, by sim)")
print("--- gate-designed tampers on scopes.ts (predictions, drafter)")
def require_tg1(user, *required):  # :36 widened to short-circuit 'oauth' too
    am = (user or {}).get('authMethod') or 'jwt'
    if am in ('jwt', 'email', 'oauth'): return 200
    return require(user, *required)
cells = [("c1", lambda R: R(attach(mint({'clientId': 'c', 'scopes': ['openid']})), 'webhooks:manage') == 403),
         ("c2", lambda R: R(attach(mint({'clientId': 'c', 'scopes': ['webhooks:manage']})), 'webhooks:manage') == 200),
         ("c3", lambda R: R(attach({'authMethod': 'api_key', 'scopes': ['openid']}), 'webhooks:manage') == 403),
         ("c4", lambda R: R(attach(mint(None)), 'webhooks:manage') == 200),
         ("c5", lambda R: R(attach(mint({'clientId': 'c', 'scopes': []})), 'webhooks:manage') == 403)]
red = [n for n, f in cells if not f(require_tg1)]
ck(red == ['c1', 'c5'], f"Tg1 (:36 short-circuits 'oauth' too) -> red {red} (predicted exactly c1 + c5; c6 is attachScopes-only, unaffected)")
def require_tg3(user, *required):  # :42 absent scopes -> ['*'] (fail-open on a missing claim)
    if user is None: return 401
    am = user.get('authMethod') or 'jwt'
    if am in ('jwt', 'email'): return 200
    scopes = user.get('scopes') or ['*']
    if '*' in scopes: return 200
    return 200 if any(r in scopes for r in required) else 403
red = [n for n, f in cells if not f(require_tg3)]
ck(red == ['c5'], f"Tg3 (:42 `user.scopes || ['*']`) -> red {red} (predicted exactly c5 — an EMPTY array is truthy, so only the ABSENT-claim cell reaches the fallback)")
def attach_tg2(user):  # :84 `if (user)` — the string overrides the array
    if user is not None:
        s = user.get('scope') or ''
        if s: user['scopes'] = [x for x in re.split(r'[\s,]+', s) if x]
    return user
u = attach_tg2({'authMethod': 'oauth', 'scopes': ['openid'], 'scope': 'webhooks:manage'})
ck(u['scopes'] == ['webhooks:manage'], f"Tg2 (:84 `if (user)`) -> cell 6a reds (the string overrides the array: {u['scopes']}); c1-c5 carry no `scope` string, so they stay green -> exactly 1 red")
print("--- enforcement.ts :159-170 allowedAuthProviders, unlabelled (parent) vs 'oauth' (head)")
def provider_refused(user_auth_method, allowed):
    a = [p.lower() for p in allowed]; m = (user_auth_method or 'email').lower()
    return (m not in a) and ('email' not in a) and ('any' not in a)
for allowed in [['google'], ['email'], ['any'], ['google', 'email'], ['oauth'], ['wallet', 'github'], []]:
    before = provider_refused(None, allowed) if allowed else False
    after = provider_refused('oauth', allowed) if allowed else False
    ck(not (after and not before), f"allowedAuthProviders={allowed}: refused before={before} after={after} (after must never refuse where before admitted)")
print("--- rateLimitEnforce.ts :61 MACHINE_AUTH_METHODS")
MACHINE = {'api_key', 'oauth_app'}
ck('oauth' not in MACHINE, "'oauth' is NOT in MACHINE_AUTH_METHODS {'api_key','oauth_app'} — an OAuth-labelled token is NOT per-client rate-limited (it was not before either: unlabelled -> not in the set); the limiter's own comment :58-60 says a new machine auth method must be added there AND populate req.user.rateLimit — a RECORD for the class, symbol MACHINE_AUTH_METHODS, not a #984 regression")
print("--- the launder path (READ ONLY, drafter): routes/auth.ts :658-689 POST /api/auth/refresh re-mints with generateTokenPair(user, session.id) — no OAuth options")
authr = open(f"{G}/model/auth-routes.ts.head", encoding="utf-8").read().split('\n')
ck("authRoutes.post('/refresh'" in authr[657], f"auth.ts :658 = {authr[657].strip()[:80]}")
ck("const payload = verifyRefreshToken(refreshTokenValue);" in authr[664], f"auth.ts :665 = {authr[664].strip()}")
ck("const tokens = generateTokenPair(user, session.id);" in authr[688], f"auth.ts :689 = {authr[688].strip()} (NO third argument: the re-mint is LOGIN-shaped)")
ck(not any('client_id' in l or "authMethod" in l for l in authr[657:700]), "auth.ts :658-700 reads neither client_id nor authMethod off the refresh token — an OAuth refresh token is accepted as a login's")
launder = mint(None)  # what :689 mints for the OAuth token's user
ck(require(attach(launder), 'webhooks:manage') == 200 and 'authMethod' not in launder and 'client_id' not in launder, "the re-minted pair (sim of :689): no label, no client_id, role-default scopes -> passes requireScope('webhooks:manage') 200 — the grant is shed in one unauthenticated call (PREDICTION for the gate's H-launder cell)")
sys.exit(1 if fails else 0)
