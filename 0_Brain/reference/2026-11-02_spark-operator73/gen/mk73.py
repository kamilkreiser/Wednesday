# Operator 73: KS-1868 governance remaining catches (jest) + auth routes. Reuses spark/gen/mk.py (rd, udiff). Template text from operators 44 and 71.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='d9acf71a3fcc9b70a216a904d7339a8fc1ccf4a0'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator73/gen/'
SV='Blockchain/Dev/services/'
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 21 open PRs read 2026-11-02 through the GitHub API; 120 file entries; the service appears only as package.json / package-lock.json entries; positive control services/originate present in 7 entries)."
def G(ind,expr):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
E1="err instanceof Error ? err.message : String(err)"
def pair(ind,fn,ctx,extra='',expr=E1):
    o=" "*ind+"logger.%s('%s', { %serror: %s });\n"%(fn,ctx,extra,expr)
    n=G(ind,expr)+" "*ind+"logger.%s('%s', { %serror: reason });\n"%(fn,ctx,extra)
    return (o,n)
GS=SV+'governance/'
GPROD=GS+'src/services/governanceService.ts'
GREF=GS+'src/__tests__/ks1845-process-expired-requires-a-platform-admin.test.ts'
T={}
def gtest(call, descr, imp):
    return open(GEN+'t73_'+call+'.ts.txt',encoding='utf-8').read()
T['p1']=dict(dir='ks_1868_o73_p1_governance_get_participant_catches_unreadable_throw', prod=GPROD, ref=GREF, runner='jest', runcmd='', rdir=GS[:-1],
  edits=[pair(4,'error','DB get participant failed','id, '), pair(4,'error','DB get participant by address failed','walletAddress, ')],
  nh=2, lines='276 and 286', test=GS+'src/__tests__/ks1868-get-participant-unreadable-throw.test.ts', tsrc='t73_p1.ts.txt',
  fn='`dbGetParticipant` and `dbGetParticipantByAddress`', short='two catch blocks',
  whatwrong="In `governanceService.ts` the catch blocks of `dbGetParticipant` (line 276) and `dbGetParticipantByAddress` (line 286) each log `logger.error('...', { <id|walletAddress>, error: err instanceof Error ? err.message : String(err) })` and then fall out of the catch to `return undefined`. If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the ERROR line is logged and before the documented `return undefined`: the exported `getParticipant` rejects with the TypeError instead of resolving undefined. The fix reads the SAME expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log call then uses `reason`. This is the inline guard already merged in the same file at `dbGetProposal` (line 218) and the other readers (lines 255, 313, 342, 448); no helper is added.",
  callers="CALLERS (git grep at the tip, governanceService.ts): `dbGetParticipant` is called at :446 (`getParticipant`), :501 (`createProposal`, the proposer), :666 (`castVote`, the voter), :867 (`cancelProposal`) and :903/:904 (`delegateVotePower`); `dbGetParticipantByAddress` at :413 (`registerParticipant`) and :448 (`getParticipant`). WHAT AN ORDINARY ERROR GETS (this is the rule for taking the site): an ordinary Error from the database is logged and the helper returns `undefined`, so the callers behave as for an unknown participant (`castVote` throws Forbidden 'Voter not registered as governance participant', `delegateVotePower` and `cancelProposal` refuse, `registerParticipant` proceeds as a first registration). After the fix an unreadable thrown value gets exactly that same outcome and the constant reason is logged; today it rejects with a TypeError out of the helper and the route answers whatever the shared error handler answers a non-AppError. The catches return no vote-power or quorum number: they return a participant record or `undefined`, and the vote power used by a vote is read from that record only when the read succeeded. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the participant helpers log a constant reason and return `undefined` (as for an ordinary Error) instead of rejecting with a TypeError. Persisted state is unchanged; the outcomes at the callers are those an ordinary Error already produces (a pre-existing property of an ordinary DB failure, e.g. `registerParticipant` re-registering on a failed lookup, is not changed by this patch). Recommended tier 1 (DAO voting participant lookups; Kam's tier-1-with-Opus-gate ruling).",
  ncells='3 cells: C1 (ordinary Error), R1, R2',
  red1="At the tip `getParticipant` rejects, so the `resolves` assertion fails",
  dbnote="`../db` and `../utils/logger` are mocked; no database, no app boot and no network. Neither helper is exported, so the test reaches both through the exported `getParticipant` (which calls `dbGetParticipant` and then, finding nothing, `dbGetParticipantByAddress`).",
  greens="'control ks1868 C1' (an ordinary `Error` logs its own message on both lines and `getParticipant` resolves undefined) (1 cell)",
  redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once each (2 cells)",
  fix_anchor="`dbGetProposal` (line 218) and the readers at lines 255, 313, 342, 448")
T['p2']=dict(dir='ks_1868_o73_p2_governance_verify_db_ready_catch_unreadable_throw', prod=GPROD, ref=GREF, runner='jest', runcmd='', rdir=GS[:-1],
  edits=[pair(4,'error','Failed to seed proposal counter from DB')],
  nh=1, lines='389', test=GS+'src/__tests__/ks1868-verify-db-ready-unreadable-throw.test.ts', tsrc='t73_p2.ts.txt',
  fn='`verifyDbReady`', short='one catch block',
  whatwrong="In `governanceService.ts` the catch block of `verifyDbReady` (the boot-time proposal-counter seed) logs `logger.error('Failed to seed proposal counter from DB', { error: err instanceof Error ? err.message : String(err) })` (line 389) and ends; it neither returns a value nor rethrows. If the query rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the ERROR line is logged and `verifyDbReady` rejects instead of resolving. The fix reads the SAME expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log call then uses `reason`. This is the inline guard already merged in the same file at lines 218, 255, 313, 342 and 448; no helper is added.",
  callers="CALLERS (git grep at the tip): `verifyDbReady` (aliased as `loadFromDb`) is the `onReady` hook passed to `initDb(() => governanceService.verifyDbReady())` in `services/governance/src/index.ts` (line 175); `initDb` awaits it from `runDbReadyHook` on the success path at boot and again on a later background recovery. WHAT AN ORDINARY ERROR GETS: the ERROR line is logged, the proposal counter stays at its initial value, and `verifyDbReady` resolves; boot continues. After the fix an unreadable thrown value gets exactly that outcome; today the catch throws and the hook's promise rejects (the boot path's handling of a rejecting hook was not measured). The catch decides no vote, no quorum and no returned data; it touches `proposalCounter` only on the success path, which is untouched. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, a constant reason is logged and the boot hook resolves, as for an ordinary Error. Persisted state: none (a MAX() query). No response or outbound call. Recommended tier 1 (DAO governance boot path).",
  ncells='3 cells: C1 (ordinary Error), R1, R2',
  red1="At the tip `verifyDbReady` rejects, so the `resolves` assertion fails",
  dbnote="`../db` (`isDbAvailable` returns true and `query` rejects) and `../utils/logger` are mocked; no database, no app boot and no network.",
  greens="'control ks1868 C1' (an ordinary `Error` logs its own message and `verifyDbReady` resolves) (1 cell)",
  redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once each (2 cells)",
  fix_anchor="`dbGetProposal` (line 218) and the readers at lines 255, 313, 342, 448")
AS=SV+'auth/'
T['p3']=dict(dir='ks_1868_o73_p3_auth_internal_connector_token_catch_unreadable_throw', prod=AS+'src/routes/internal.ts', ref=AS+'src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts', runner='vitest', runcmd='run ', rdir=AS[:-1],
  edits=[pair(4,'error','connector-token exchange failed','',"(err as Error).message")],
  nh=1, lines='80', test=AS+'src/__tests__/ks1868-internal-connector-token-unreadable-throw.test.ts', tsrc='t73_p3.ts.txt',
  fn='the `POST /internal/connector-token` catch', short='one catch block',
  whatwrong="In `internal.ts` the catch block of the connector-token exchange route logs `logger.error('connector-token exchange failed', { error: (err as Error).message })` (line 80) and then answers the constant `502 BAD_GATEWAY` 'Key validation unavailable'. If the upstream call (the security service key validation, or the token mint) rejects with a revoked Proxy, the property read `.message` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `.message` throws. Either way the catch throws before the line is logged and before the 502 is sent. Express 4 does not catch a rejection of an async handler, so the request gets NO response and Node sees an unhandled rejection. The fix reads the SAME expression `(err as Error).message` into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log call then uses `reason`. The 502 response is untouched. This is the inline guard already merged in `routes/auth.ts` (PR 1911, e.g. lines 308-313); no helper is added.",
  callers="CALLERS: the route is mounted at `/internal` in `services/auth/src/index.ts` (line 111) and called service-to-service by the api-gateway when it has an `x-api-key: sk_...` request. The catch decides nothing about authorisation: a key is accepted only on the success path (`data.valid` true from the security service), which is untouched; every failure here, including this catch, answers 502 and mints NO token. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the ERROR line with the message and the constant 502 BAD_GATEWAY. After the fix an unreadable thrown value gets exactly that; today it gets no response (the gateway call times out) and an unhandled rejection. No token is minted before or after. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the route logs a constant reason and answers the constant 502 (as for an ordinary Error) instead of leaving the request unanswered. Persisted state: none. Outbound call: the same one as before the catch (nothing new). Recommended tier 1 (auth service, API-key to connector-token exchange).",
  ncells='3 cells: C1 (ordinary Error), R1, R2',
  red1="At the tip the route sends no response (the cell's client times out after 1.5 s and the status assertion fails) and an unhandled rejection is counted",
  dbnote="`../utils/logger` and `../services/jwt` are mocked; the global `fetch` the route calls is replaced by a plain function that rejects with the value the cell sets (the test client keeps the real one); the route is mounted on a real loopback Express server. No security service, no database and no key material.",
  greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message, the route answers 502 BAD_GATEWAY and no token is returned) (1 cell)",
  redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once each (2 cells)",
  fix_anchor="`routes/auth.ts` (PR 1911, lines 308-313 and the two others)", sib="`ks1868-auth-login-publish-event-unreadable-throw.test.ts`")
T['p4']=dict(dir='ks_1868_o73_p4_auth_oauth_authorize_post_and_token_catches_unreadable_throw', prod=AS+'src/routes/oauth.ts', ref=AS+'src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts', runner='vitest', runcmd='run ', rdir=AS[:-1],
  edits=[pair(4,'error','OAuth authorize POST error','',"error.message"), pair(4,'error','OAuth token error','',"error.message")],
  nh=2, lines='805 and 1109', test=AS+'src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts', tsrc='t73_p4.ts.txt',
  fn='the `POST /api/oauth/authorize` and `POST /api/oauth/token` outer catches', short='two catch blocks',
  whatwrong="In `oauth.ts` the outer catch of `POST /authorize` (line 805) logs `logger.error('OAuth authorize POST error', { error: error.message })` and the outer catch of `POST /token` (line 1109) logs `logger.error('OAuth token error', { error: error.message })`; each then answers the constant `500` with code `INTERNAL_ERROR` and message `server_error`. If an awaited call in the try (for example the client app lookup `getAppByClientId`) rejects with a revoked Proxy, the property read `error.message` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `error.message` throws. Either way the catch throws before the line is logged and before the 500 is sent. Express 4 does not catch a rejection of an async handler, so the request gets NO response and Node sees an unhandled rejection. The fix reads the SAME expression `error.message` into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log call then uses `reason`. The 500 responses are untouched. This is the inline guard already merged in `routes/auth.ts` (PR 1911, e.g. lines 308-313); no helper is added.",
  callers="CALLERS: both are Express route handlers on `oauthRouter` (mounted under /api/oauth), reached over HTTP by OAuth clients. The catches decide nothing about authorisation: an authorization code is minted, and tokens are issued, only on the success paths inside the try, which are untouched; the app lookup is the first await on both paths in the cells (a rejection there means nothing was minted). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the ERROR line with the message and the constant 500 `server_error`. After the fix an unreadable thrown value gets exactly that; today it gets no response and an unhandled rejection. Nothing is minted before or after in the cells. The sibling catches of this file that read `error?.code` / `/regex/.test(error?.message)` first, or that put `error.message` into the response body (lines 531, 1259, 1283, 1296, 1353, 1382, 1407), are NOT in this brief. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the two routes log a constant reason and answer the constant 500 (as for an ordinary Error) instead of leaving the request unanswered. Persisted state: none changes in the cells; a rejection later in the try (after a code or session write) would leave the same persisted state as for an ordinary Error. Recommended tier 1 (OAuth authorize and token endpoints).",
  ncells='6 cells: C1 and C2 (ordinary Error on each route), R1 to R4',
  red1="At the tip the route sends no response (the cell's client times out after 1.5 s and the status assertion fails) and an unhandled rejection is counted",
  dbnote="`../utils/logger`, `../services/oauth` (the app lookup rejects with the value the cell sets), `../services/jwt`, `../services/session`, `../services/password`, `../services/accountLockout`, `../services/refreshDenylist`, `../repositories/userRepo`, `../middleware/authenticate`, `../db` and `../events` are mocked; the router is mounted on a real loopback Express server. No database, no key material.",
  greens="'control ks1868 C1' (authorize) and 'control ks1868 C2' (token): an ordinary `Error` is logged with its own message and the route answers 500 server_error (2 cells)",
  redcells="`R1` (revoked Proxy) and `R2` (message getter throws) on authorize, `R3` and `R4` the same on token (4 cells)",
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n- RED ks1868 R3\n- RED ks1868 R4\n",
  fix_anchor="`routes/auth.ts` (PR 1911, lines 308-313 and the two others)", sib="`ks1868-auth-login-publish-event-unreadable-throw.test.ts`")
def pair2(ctx):
    o="    logger.error('%s', {\n      error: err instanceof Error ? err.message : String(err),\n    });\n"%ctx
    n=G(4,E1)+"    logger.error('%s', {\n      error: reason,\n    });\n"%ctx
    return (o,n)
T['p5']=dict(dir='ks_1868_o73_p5_auth_issuer_certs_list_and_revoke_catches_unreadable_throw', prod=AS+'src/routes/issuerCerts.ts', ref=AS+'src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts', runner='vitest', runcmd='run ', rdir=AS[:-1],
  edits=[pair2('Issuer cert list failed'), pair2('Issuer cert revoke failed')],
  nh=2, lines='364 and 509', test=AS+'src/__tests__/ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts', tsrc='t73_p5.ts.txt',
  fn='the `GET /api/issuer-certs` and `POST /api/issuer-certs/:id/revoke` outer catches', short='two catch blocks',
  whatwrong="In `issuerCerts.ts` the outer catch of the list route (line 364) logs `logger.error('Issuer cert list failed', { error: err instanceof Error ? err.message : String(err) })` and the outer catch of the revoke route (line 509) logs `logger.error('Issuer cert revoke failed', { ... same expression })`; each then answers the constant `500` with code `INTERNAL_ERROR` ('Failed to list issuer certs' / 'Failed to revoke issuer cert'). If the awaited repository call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before the 500 is sent. Express 4 does not catch a rejection of an async handler, so the request gets NO response and Node sees an unhandled rejection. The fix reads the SAME expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log call then uses `reason` (the call keeps its two-line object layout). The 500 responses are untouched. This is the inline guard already merged in `routes/auth.ts` (PR 1911, e.g. lines 308-313); no helper is added.",
  callers="CALLERS: both are Express route handlers on `issuerCertsRoutes` (mounted at /api/issuer-certs), reached over HTTP behind the role/scope gates, which run BEFORE the try body reaches the repository and are untouched. The catches decide nothing about authorisation. On the revoke route the catch is reached when `getIssuerCertById` or `revokeIssuerCert` rejects, i.e. the revocation is NOT confirmed: the ordinary-Error outcome is the constant 500 and no `ISSUER_CERT_REVOKED` event (that publish is after the UPDATE succeeds), and the cells assert exactly that for the unreadable value too. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the ERROR line with the message and the constant 500. After the fix an unreadable thrown value gets exactly that; today it gets no response and an unhandled rejection. No private-key material, signing or certificate parsing is on these two paths (upload, rotate and sign are NOT in this brief). The sibling catches that read `err.code` first (the get route, line 407) or are preceded by `instanceof IssuerCertError` (the inner parse/verify/sign catches) are NOT in this brief. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the two routes log a constant reason and answer the constant 500 (as for an ordinary Error) instead of leaving the request unanswered. Persisted state: unchanged; a revoke is not recorded when the UPDATE rejects, before or after, and for an ordinary Error. Recommended tier 1 (issuer-certificate admin routes; revoke is a security action).",
  ncells='6 cells: C1 and C2 (ordinary Error on each route), R1 to R4',
  red1="At the tip the route sends no response (the cell's client times out after 1.5 s and the status assertion fails) and an unhandled rejection is counted",
  dbnote="`../utils/logger`, `@secuura/shared/utils/logger`, `../middleware/authenticate` (the caller is an ORG_ADMIN with a tenant), `../repositories/issuerCertRepo` (list and revoke reject with the value the cell sets; the cert read returns an active cert), `../events` and `../db` are mocked; the router is mounted on a real loopback Express server. No database and no key material.",
  greens="'control ks1868 C1' (list) and 'control ks1868 C2' (revoke): an ordinary `Error` is logged with its own message and the route answers the constant 500 (2 cells)",
  redcells="`R1` (revoked Proxy) and `R2` (message getter throws) on list, `R3` and `R4` the same on revoke (4 cells)",
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n- RED ks1868 R3\n- RED ks1868 R4\n",
  fix_anchor="`routes/auth.ts` (PR 1911, lines 308-313 and the two others)", sib="`ks1868-auth-login-publish-event-unreadable-throw.test.ts`")
EXP='err?.message'
T['p6']=dict(dir='ks_1868_o73_p6_auth_login_rehash_and_logout_denylist_catches_unreadable_throw', prod=AS+'src/routes/auth.ts', ref=AS+'src/__tests__/ks1868-auth-login-publish-event-unreadable-throw.test.ts', runner='vitest', runcmd='run ', rdir=AS[:-1],
  edits=[pair(8,'warn','UPGRADE-ON-VERIFY rehash failed (non-fatal)','userId: user.id, ',EXP), pair(10,'warn','Logout denylist failed (non-fatal)','',EXP)],
  nh=2, lines='555 and 784', test=AS+'src/__tests__/ks1868-auth-rehash-and-logout-denylist-unreadable-throw.test.ts', tsrc='t73_p6.ts.txt',
  fn='the login UPGRADE-ON-VERIFY rehash catch and the logout refresh-JTI denylist `.catch`', short='two non-fatal handlers',
  whatwrong="In `auth.ts` two handlers that are meant to be non-fatal read the rejection value with `err?.message`: the catch around the password-hash upgrade in POST /login (line 555: `logger.warn('UPGRADE-ON-VERIFY rehash failed (non-fatal)', { userId: user.id, error: err?.message })`) and the `.catch` on `denylistRefreshJti` in POST /logout (line 784: `logger.warn('Logout denylist failed (non-fatal)', { error: err?.message })`). If the awaited call rejects with a revoked Proxy, the property read `err?.message` itself throws a TypeError inside the handler; if it rejects with an Error whose `message` getter throws, `err?.message` throws. Either way the handler throws before the line is logged: in /login the exception leaves the route's try and ends in the error handler as a 500 with NO tokens (the password was verified and the session was not yet created), in /logout the `await` rejects, the route's catch calls `next(error)` and the client gets a 500, with the refresh cookie NOT cleared (the session revocation above it already ran). The fix reads the SAME expression `err?.message` into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log call then uses `reason`. This is the inline guard already merged in the same file (PR 1911, lines 308-313, 622-627, 896-900); no helper is added.",
  callers="CALLERS: both are Express route handlers on `authRoutes` (mounted at /api/auth), reached over HTTP. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): both handlers log the warn line and carry on: /login finishes normally (the user keeps the old hash, the session is created and tokens are issued), /logout clears the refresh cookie and answers 200 (the session was already revoked). After the fix an unreadable thrown value gets exactly that; the cells assert it (200 with tokens; 200 with the cookie cleared). Today it gets a 500 with no tokens (login) and a 500 with the cookie left in place (logout). The fix issues no credential that an ordinary Error does not already receive, grants nothing new (the login reaches the token step only after the password, lockout and MFA gates above it, all untouched) and the logout path ends the session in both cases. Sibling `err?.message` reads in the same file (line 380, the platform-admin rehash catch, and line 595, the tenant-resolution debug catch) are NOT in this brief. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, a failing password-hash upgrade no longer fails the login and a failing denylist write no longer fails the logout; each logs a constant reason and proceeds as for an ordinary Error. Persisted state: the old password hash is kept (as for an ordinary Error); the denylist entry is not written (as for an ordinary Error). Recommended tier 1 (login and logout routes of the auth service).",
  ncells='6 cells: C1 and C2 (ordinary Error on login and logout), R1 to R4',
  red1="At the tip the login answers 500 with no tokens (R1, R2) and the logout answers 500 with no cookie cleared (R3, R4), so the status assertions fail",
  dbnote="Repository, password, session, jwt, refresh denylist, lockout, mail, event bus, logger and the authenticate middleware are mocked as in the sibling suite; a small middleware sets `req.cookies` (no cookie parser is mounted) and the real router and error handler are mounted on a real loopback Express server. No database and no network.",
  greens="'control ks1868 C1' (login) and 'control ks1868 C2' (logout): an ordinary `Error` is logged with its own message and the route still succeeds (2 cells)",
  redcells="`R1` (revoked Proxy) and `R2` (message getter throws) on login, `R3` and `R4` the same on logout (4 cells)",
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n- RED ks1868 R3\n- RED ks1868 R4\n",
  fix_anchor="the same file (PR 1911, lines 308-313, 622-627 and 896-900)", sib="`ks1868-auth-login-publish-event-unreadable-throw.test.ts`")
def build(k):
    X=T[k]; PROD=X['prod']
    old=mk.rd(PROD); new=old
    for o,n in X['edits']:
        assert new.count(o)==1,(k,o[:70],new.count(o))
        new=new.replace(o,n)
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    hl=[l for l in pd.splitlines() if l.startswith('@@ ')]
    assert len(hl)==X['nh'],(k,len(hl),hl)
    tbody=open(GEN+X['tsrc'],encoding='utf-8').read()
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    golden=pd+td
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    first=0; cur=None
    for l in pd.splitlines():
        if l.startswith('@@ '):
            cur=int(l.split()[1].split(',')[0][1:]); continue
        if cur is None: continue
        if l.startswith('-') and not l.startswith('---'): first=cur; break
        if l.startswith(' '): cur+=1
    assert first
    nh=X['nh']
    pins=("# code_patch2: %s (%d hunk) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_this_file_and_its_src/__tests__/_are_in_no_open_PR_(21_PRs_120_files_read_2026-11-02_by_op73,_positive_control_services/originate_in_7_entries);_live_lanes_beyond_PRs_not_checked\n")%(PROD.split('/')[-1],nh,X['ref'],first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]; svc=PROD.split('/')[3]
    runner=X['runner']
    hw='hunk' if nh==1 else 'hunks'
    txt=f"""# KS-1868 {svc}: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {nh} product {hw} given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 73 for Wednesday, 2026-11-02. Secuura ({svc}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (line {X['lines']}), reusing the guard already merged in this file at {X['fix_anchor']}. {OPEN_PR} Other KS-1868 files and the other sites of this file are separate briefs or deliberately skipped.

File: `{PROD}`  (product, modified in place: EXACTLY {nh} {hw})
Test file: `{X['test']}`  (NEW file, {runner}, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `{runner}` (`npx {runner} {X['runcmd']}src/__tests__/{tp}` from `{X['rdir']}`)
Tier: `code_patch2`
Rung: **3 ({nh} product {hw}, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the {nh} {hw} under "The exact change", byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{X['whatwrong']}

## Where

`{PROD}`: line {X['lines']}. {X['callers']}

## The exact change

EXACTLY {nh} {hw} in the product file. The file header lines and the `@@` headers are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text. The log message text is unchanged.

**Do NOT touch** any other catch block of the file, any message text, or any other line.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from the merged sibling suites of this directory ({X.get('sib','`ks1868-get-total-vote-power-unreadable-throw.test.ts`')}; pinned ref `{X['ref']}`). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells
{X.get('redlines','- RED ks1868 R1'+chr(10)+'- RED ks1868 R2'+chr(10))}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {X['red1']} (and no ERROR line is logged); after the edit the constant reason is logged.
- GREEN at the tip and after: {X['greens']}.
- The stand-in rejecting with the thrown value is a plain function, not `{'jest.fn()' if runner=='jest' else 'vi.fn()'}`, on purpose: a spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` line {X['lines']} is the unguarded read at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 21 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or the service's `src/__tests__/` (120 file entries; positive control services/originate appears in 7 file entries).
- No test or script reads this log line's text as source other than the new test.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were not touched. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot with a real Postgres and a real Express 4 were not run.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
if __name__=='__main__':
    for k in sys.argv[1:]: build(k)
