#!/usr/bin/env python3
"""guards_sim.py — a port of the #986 guard and the refresh route's side-effect ORDER (routes/auth.ts:658-724 at
ac1c119b5, read via the checkout) plus the jwt.ts payload composition (:187-234), so every prediction in the brief's
section C tamper table is a computed prediction, not a hunch. Also the #987 pin (oauth.ts:837) over USER_STATUSES.
Read-only; no network; no vitest. Prints the prediction table the brief carries (predicted-by: drafter)."""
import subprocess, re
R = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H986 = 'ac1c119b56888bc064a820f9b191c409c520df64'
src = subprocess.run(['git', '-C', R, 'show', H986 + ':Blockchain/Dev/services/auth/src/routes/auth.ts'], capture_output=True, text=True).stdout
route = src.split("authRoutes.post('/refresh'")[1].split('\n});')[0]
# the ORDER of the route's calls, read from the source itself
order = [n.replace('if (payload.client_id !== undefined', 'GUARD') for n in re.findall(r"(verifyRefreshToken\(|if \(payload\.client_id !== undefined|getSession\(|isRefreshJtiDenylisted\(|revokeSession\(|getUserByIdPreAuth\(|generateTokenPair\(|rotateSessionRefreshToken\(|denylistRefreshJti\(|res\.cookie\()", route)]
order = [n.rstrip('(') for n in order]
print('route call order at head:', ' -> '.join(order))
assert order.index('verifyRefreshToken') < order.index('GUARD') < order.index('getSession') < order.index('rotateSessionRefreshToken'), 'the guard is not between verify and getSession'

# --- the jwt.ts payload composition (mirror of :187-234): the claim authMethod comes ONLY from the oauth option ---
def mint(user, sid, oauth=None):
    p = {'userId': user['id'], 'role': user['role'], 'sessionId': sid, 'type': 'refresh', 'jti': 'j-' + sid}
    if oauth: p.update({'scopes': list(oauth['scopes']), 'authMethod': 'oauth', 'client_id': oauth['clientId']})
    return p   # NOTE: user['authMethod'] ('email'|'wallet'|'social'|'federated') is NEVER copied — jwt.ts lists its fields explicitly

# --- the route, with the guard as a pluggable predicate and the ORDER as a pluggable position ---
def refresh(payload, guard, guard_pos='before_getSession', session_ok=True, denylisted=False, user_status='ACTIVE'):
    calls = []
    def g():
        if guard(payload): raise PermissionError(401)
    try:
        if guard_pos == 'before_getSession': g()
        calls.append('getSession')
        if guard_pos == 'after_getSession': g()          # T5
        if not session_ok: raise PermissionError(401)
        calls.append('isRefreshJtiDenylisted')
        if denylisted: calls.append('revokeSession'); raise PermissionError(401)
        calls.append('getUserByIdPreAuth')
        if user_status != 'ACTIVE': raise PermissionError(401)
        calls.append('generateTokenPair'); calls.append('rotateSessionRefreshToken'); calls.append('denylistRefreshJti')
        if guard_pos == 'after_rotate': g()               # T3
        calls.append('res.cookie')
        return 200, calls
    except PermissionError as e:
        return int(str(e)), calls

HEAD = lambda p: p.get('client_id', None) is not None or p.get('authMethod') == 'oauth'   # `!== undefined`: JSON null counts as present -> refused (fail-closed)
HEAD_STRICT = lambda p: ('client_id' in p) or p.get('authMethod') == 'oauth'
T1 = lambda p: False                                   # guard deleted
T2 = lambda p: p.get('authMethod') == 'oauth'          # client_id arm dropped
T6 = lambda p: 'client_id' in p                        # authMethod arm dropped
T7 = lambda p: 'client_id' in p or p.get('authMethod') == 'OAUTH'

U = {'id': 'u', 'role': 'OWNER', 'authMethod': 'email'}
FIX = {
 'C1 OAuth-minted (both claims)':      mint(U, 'sess-x', {'clientId': 'client-1', 'scopes': ['openid']}),
 'C6 client_id-only (#983-era)':       {k: v for k, v in mint(U, 'sess-x', {'clientId': 'client-1', 'scopes': ['openid']}).items() if k != 'authMethod'},
 'C7 label-only (no client_id)':       {k: v for k, v in mint(U, 'sess-x', {'clientId': 'client-1', 'scopes': ['openid']}).items() if k != 'client_id'},
 'C4 password login':                  mint(U, 'sess-x'),
 'C5 social login':                    mint({**U, 'authMethod': 'social'}, 'sess-x'),
 'C5 wallet login':                    mint({**U, 'authMethod': 'wallet'}, 'sess-x'),
}
print('\n=== status per fixture per guard (pos = head position) ===')
print('%-34s %-6s %-6s %-6s %-6s %-6s' % ('fixture', 'HEAD', 'T1', 'T2', 'T6', 'T7'))
for name, p in FIX.items():
    print('%-34s %-6s %-6s %-6s %-6s %-6s' % (name, *[refresh(p, g)[0] for g in (HEAD_STRICT, T1, T2, T6, T7)]))
print('\n=== side-effect ORDER for the OAuth fixture C1 ===')
for pos, tag in (('before_getSession', 'HEAD (:677 before :686)'), ('after_getSession', 'T5 (guard below getSession)'), ('after_rotate', 'T3 (guard below rotate)')):
    st, calls = refresh(FIX['C1 OAuth-minted (both claims)'], HEAD_STRICT, pos)
    print('%-32s status=%s calls=%s' % (tag, st, calls))
print("\n=== the builder's 5 cells vs the gate's harness under each tamper (predicted-by: drafter) ===")
# builder cells: 1/2 assert 401 + rotated==[] + denylisted==[]; 3 the client_id-only 401 + rotated==[]; 4 login 200 + rotated==['sess-x']; 5 garbage 401 (never reaches the route body)
def builder(guard, pos):
    red = []
    for cell, p in (('1', FIX['C1 OAuth-minted (both claims)']), ('2', FIX['C1 OAuth-minted (both claims)']), ('3', FIX['C6 client_id-only (#983-era)'])):
        st, calls = refresh(p, guard, pos)
        if st != 401 or 'rotateSessionRefreshToken' in calls or 'denylistRefreshJti' in calls: red.append(cell)
    st, calls = refresh(FIX['C4 password login'], guard, pos)
    if st != 200 or calls.count('rotateSessionRefreshToken') != 1: red.append('4')
    return red
def gate(guard, pos):
    red = []
    for cell in ('C1 OAuth-minted (both claims)', 'C6 client_id-only (#983-era)', 'C7 label-only (no client_id)'):
        st, calls = refresh(FIX[cell], guard, pos)
        if st != 401 or calls: red.append(cell.split()[0] + ('(order)' if st == 401 and calls else ''))
    for cell in ('C4 password login', 'C5 social login', 'C5 wallet login'):
        st, calls = refresh(FIX[cell], guard, pos)
        if st != 200: red.append(cell.split()[0])
    return red
for tag, guard, pos in (('T1 guard deleted', T1, 'before_getSession'), ('T2 client_id arm dropped', T2, 'before_getSession'), ('T3 guard after rotate', HEAD_STRICT, 'after_rotate'),
                        ('T5 guard after getSession', HEAD_STRICT, 'after_getSession'), ('T6 authMethod arm dropped', T6, 'before_getSession'), ('T7 oauth->OAUTH', T7, 'before_getSession'), ('HEAD', HEAD_STRICT, 'before_getSession')):
    b = builder(guard, pos); g = gate(guard, pos)
    print('%-28s builder red cells=%-12s (%d failed | %d passed)   gate red=%s' % (tag, b, len(b), 5 - len(b), g))

# --- #987: the pin over USER_STATUSES ---
print('\n=== #987 code-grant pin over USER_STATUSES (oauth.ts:837) ===')
for s in ['PENDING', 'ACTIVE', 'SUSPENDED', 'DEACTIVATED', 'INVITED', None]:
    parent = 400 if s is None else 200
    head = 200 if s == 'ACTIVE' else 400
    print('%-12s parent(:833 !user)=%s  head(:837 !user || status!==ACTIVE)=%s  %s' % (s, parent, head, 'NEW REFUSAL' if parent != head else ''))
print('T1 (pin reverted, description kept): cell1 red only; T2 (!== -> ===): SUSPENDED admitted (cell1 red) AND ACTIVE refused (cell2 red); T4 (description reverted, pin kept): cells 1+4 + ks790:229 red (3 across 2 files)')
