# Operator 50, task 1 (KS-1868 services/auth/src/routes/auth.ts :306/:612/:880): code_patch2 brief generator (O49 shape).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='ca36945e974081be6abbc15e548f4f8d02767e14'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator50/gen/'
SV='Blockchain/Dev/services/auth/'
PROD=SV+'src/routes/auth.ts'
TD=SV+'src/__tests__/'

CATCH_OLD="    }).catch(err => logger.error('Failed to publish event', { error: err instanceof Error ? err.message : String(err) }));\n"
def new_catch():
    return ("    }).catch(err => {\n      let reason: string;\n      try {\n        reason = err instanceof Error ? err.message : String(err);\n"
            "      } catch {\n        reason = 'unreadable thrown value';\n      }\n      logger.error('Failed to publish event', { error: reason });\n    });\n")
def edit_nth(text, old, new, n):
    idx=-1
    for _ in range(n): idx=text.index(old, idx+1)
    return text[:idx]+new+text[idx+len(old):]
def p1(t):
    assert t.count(CATCH_OLD)==2
    return edit_nth(t,CATCH_OLD,new_catch(),1)
def p2(t):
    assert t.count(CATCH_OLD)==2
    return edit_nth(t,CATCH_OLD,new_catch(),2)
P3_OLD=("      logger.error('Password reset: the session revocation THREW after the password write', {\n"
        "        userId: user.id, error: err instanceof Error ? err.message : String(err),\n      });\n")
def p3(t):
    assert t.count(P3_OLD)==1
    new=("      let reason: string;\n      try {\n        reason = err instanceof Error ? err.message : String(err);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n"
         "      logger.error('Password reset: the session revocation THREW after the password write', {\n        userId: user.id, error: reason,\n      });\n")
    return t.replace(P3_OLD,new)

COMMON_PR=("No open PR touches this file or the new test file's directory contents that matter: the 22 open PRs read 2026-11-02 through the GitHub API (128 file entries) touch services/auth only as users.ts and "
 "__tests__/ks1006-... (PR 1796, PR 1798) and package.json (PRs 575, 649, 948, 1726); none touches `src/routes/auth.ts`; planted positive control: the same scan finds services/auth in 7 entries.")
T={}
T['p1']=dict(dir='ks_1868_o50_p1_auth_register_publish_event_unreadable_throw', fix=p1, line=306, tag='O50-P1',
  test=TD+'ks1868-auth-register-publish-event-unreadable-throw.test.ts', tsrc='t50_p1.ts.txt',
  ref=TD+'ks1460-register-over-an-invited-stub-confirms-its-activating-write.test.ts',
  title="the register route's event-publish catch handler must still log when the rejection value cannot be read",
  site="the `.catch` handler of the fire-and-forget `publishEvent(EventTypes.USER_REGISTERED, ...)` call in `POST /register`",
  quote="`}).catch(err => logger.error('Failed to publish event', { error: err instanceof Error ? err.message : String(err) }));`",
  whatwrong="`POST /register` publishes `user.registered` without awaiting it: `publishEvent(...).catch(err => logger.error('Failed to publish event', { error: err instanceof Error ? err.message : String(err) }))` (the read is on line 306; the response is built after it). If the publish rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the handler; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the handler throws before the line is logged, the promise `.catch` returns rejects, nothing is attached to it, and Node reports an unhandled rejection. The fix turns the arrow into a block body that reads the value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and logs `{ error: reason }`. An ordinary Error still logs `error: <its message>`. The response (201) is the same in every case.",
  callers="CALLERS: this IS the route handler (`authRoutes.post('/register', ...)`, mounted at `/api/auth` by `src/index.ts:112`); the publish is fire-and-forget and the `.catch` handler has no other caller. `publishEvent` (`src/events.ts`) wraps its Redis work in its own `try`/`catch {}` and returns early without Redis, so at this tip it does not reject: the handler is defence in depth and is reachable only if `publishEvent` changes or something throws before its `try`. **BEHAVIOUR CHANGE the raise PR must state:** for a rejection value that cannot be read, the handler today throws inside the `.catch`, producing an UNHANDLED REJECTION in the auth process after the 201 was sent; the auth service installs no `unhandledRejection` handler (its Dockerfile runs `node:24-alpine`, and only the api-gateway sets `UNHANDLED_REJECTION_MODE=survive` in `docker-compose.yml`), so under Node's default the process would terminate. After the fix the handler logs `error: unreadable thrown value` and nothing is unhandled. The response sent to the client is unchanged either way. That Node 24 terminates on an unhandled rejection with no listener is read from the Dockerfile and Node's documented default, not run here.",
  harness="`../repositories/userRepo`, `../services/password` (hashPassword), `../services/jwt` (generateTokenPair), `../services/session`, `../services/email`, `../events`, `../db` and the logger are replaced; the real router runs behind the real error handler on a loopback listener (the harness of the pinned ref); no database, no Redis and no network beyond 127.0.0.1. The publish is fire-and-forget, so the cells wait for the outcome (a log line or an unhandled rejection) and count unhandled rejections with their own `process` listener.",
  red1="At the tip the handler throws, so no `Failed to publish event` line is logged and the cell's own listener counts one unhandled rejection (`h.unhandled` is 1, not 0)")
T['p2']=dict(dir='ks_1868_o50_p2_auth_login_publish_event_unreadable_throw', fix=p2, line=612, tag='O50-P2',
  test=TD+'ks1868-auth-login-publish-event-unreadable-throw.test.ts', tsrc='t50_p2.ts.txt',
  ref=TD+'ks1157-the-marker-at-the-route-and-across-a-rotation.test.ts',
  title="the login route's event-publish catch handler must still log when the rejection value cannot be read",
  site="the `.catch` handler of the fire-and-forget `publishEvent(EventTypes.USER_LOGIN, ...)` call in `POST /login`",
  quote="`}).catch(err => logger.error('Failed to publish event', { error: err instanceof Error ? err.message : String(err) }));`",
  whatwrong="`POST /login` publishes `user.login` without awaiting it: `publishEvent(...).catch(err => logger.error('Failed to publish event', { error: err instanceof Error ? err.message : String(err) }))` (the read is on line 612; the refresh-token cookie and the 200 response follow it). If the publish rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the handler; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the handler throws before the line is logged, the promise `.catch` returns rejects, nothing is attached to it, and Node reports an unhandled rejection. The fix turns the arrow into a block body that reads the value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and logs `{ error: reason }`. An ordinary Error still logs `error: <its message>`. The response (200 with tokens) is the same in every case.",
  callers="CALLERS: this IS the route handler (`authRoutes.post('/login', ...)`, mounted at `/api/auth` by `src/index.ts:112`); the publish is fire-and-forget and the `.catch` handler has no other caller. `publishEvent` (`src/events.ts`) wraps its Redis work in its own `try`/`catch {}` and returns early without Redis, so at this tip it does not reject: the handler is defence in depth and is reachable only if `publishEvent` changes or something throws before its `try`. **BEHAVIOUR CHANGE the raise PR must state:** this is the LOGIN path, so it runs on every successful password login: for a rejection value that cannot be read, the handler today throws inside the `.catch`, producing an UNHANDLED REJECTION in the auth process after the 200 was sent; the auth service installs no `unhandledRejection` handler (its Dockerfile runs `node:24-alpine`, and only the api-gateway sets `UNHANDLED_REJECTION_MODE=survive`), so under Node's default the process would terminate. After the fix the handler logs `error: unreadable thrown value` and nothing is unhandled. The response sent to the client is unchanged either way. That Node 24 terminates on an unhandled rejection with no listener is read from the Dockerfile and Node's documented default, not run here. This pass does not touch the other `catch` blocks of the login handler.",
  harness="`../db`, `../repositories/userRepo`, `../services/password`, `../services/session`, `../services/jwt`, `../services/refreshDenylist`, `../services/accountLockout`, `../services/email`, `../middleware/authenticate`, `../middleware/tenantGuc`, `../events` and the logger are replaced (the mock set of the pinned ref, minus its OAuth parts); the real router runs behind the real error handler on a loopback listener; no database, no Redis and no network beyond 127.0.0.1. The publish is fire-and-forget, so the cells wait for the outcome (a log line or an unhandled rejection) and count unhandled rejections with their own `process` listener.",
  red1="At the tip the handler throws, so no `Failed to publish event` line is logged and the cell's own listener counts one unhandled rejection (`h.unhandled` is 1, not 0)")
T['p3']=dict(dir='ks_1868_o50_p3_auth_reset_password_revoke_unreadable_throw', fix=p3, line=880, tag='O50-P3',
  test=TD+'ks1868-auth-reset-password-revoke-unreadable-throw.test.ts', tsrc='t50_p3.ts.txt',
  ref=TD+'ks1407-reset-password-refuses-when-the-store-cannot-revoke.test.ts',
  title="the reset-password revocation catch block must still map to its 503 when the thrown value cannot be read",
  site="the `catch (err: unknown)` block around `revokeAllUserSessions` in `POST /reset-password`",
  quote="`userId: user.id, error: err instanceof Error ? err.message : String(err),`",
  whatwrong="`POST /reset-password` writes the new password, then calls `revokeAllUserSessions(user.id)` inside a `try` (KS-1692). Its catch block logs `logger.error('Password reset: the session revocation THREW after the password write', { userId: user.id, error: err instanceof Error ? err.message : String(err), })` (the read is on line 880) and then throws a `ServiceUnavailableError` (503 SERVICE_UNAVAILABLE, `Your password WAS reset, but your other sessions could not be ended ...`, reset link NOT used). If the revocation rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch block throws before the log line and before the 503 is built, so the route's outer catch hands `next(error)` a TypeError and the caller gets a generic 500 INTERNAL_ERROR instead. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `error: reason`. The 503 is then thrown as before. An ordinary Error still logs `error: <its message>`.",
  callers="CALLERS: this IS the route handler (`authRoutes.post('/reset-password', ...)`, mounted at `/api/auth` by `src/index.ts:112`; a public, pre-auth route authenticated by the emailed token); the catch block has no other caller. It is reachable whenever `revokeAllUserSessions` rejects (KS-1692: a rejected Redis command). **BEHAVIOUR CHANGE the raise PR must state, and it is a security surface:** for a thrown value that cannot be read, a password reset whose session revocation failed today answers 500 INTERNAL_ERROR (the password HAS been written, the other sessions are NOT revoked, the single-use token is not burned, and the caller is told only that something unexpected happened); after the fix it answers the 503 SERVICE_UNAVAILABLE that every ordinary revocation failure already gets, telling the caller the password WAS reset, the other sessions were not ended and the link is still usable. What is written and what is burned is the same in both. The identical read exists at `src/routes/users.ts` change-password (outside this file, not touched here).",
  harness="`../repositories/userRepo` (getResetToken, getUserByIdPreAuth, updateUserOrThrow, consumeResetToken), `../services/password` (hashPassword only), `../services/session` (isRedisAvailable, revokeAllUserSessions), `../services/email`, `../events`, `../db` and the logger are replaced; the real router runs behind the real error handler on a loopback listener (the harness of the pinned ref); no database, no Redis and no network beyond 127.0.0.1.",
  red1="At the tip the catch block throws before the 503 is built, so the route answers 500 INTERNAL_ERROR and no `Password reset: the session revocation THREW ...` line is logged (the status assertion fails first)")

def build(k):
    X=T[k]
    old=mk.rd(PROD); new=X['fix'](old)
    assert new!=old
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    tbody=open(GEN+X['tsrc'],encoding='utf-8').read()
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    golden=pd+td
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    pins=("# code_patch2: auth routes/auth.ts (1 hunk) + a NEW test file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/auth_src/routes/auth.ts_is_in_no_open_PR_(22_PRs_128_files_read_2026-11-02_by_op50,_auth_only_as_users.ts/ks1006_test/package.json,_positive_control_services/auth_in_7_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['ref'],X['line'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 auth: {X['title']} (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 50 for Wednesday, 2026-11-02. Secuura (auth) only. **auth is a security surface: the raise of this pass is gated tier 1.** A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {X['site']} in `services/auth/src/routes/auth.ts`. {COMMON_PR} This pass is one of three sequenced in old-line order in this one file (register :306, login :612, reset-password :880); each is generated against the same tip and is disjoint from the others. Seat S 10th's list of the log-only unguarded reads in this file after its KS-1885 sweep is the source of the three sites.

File: `{PROD}`  (product, modified in place: ONE hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; 4 cells (2 red, 2 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/auth`)
Tier: `code_patch2`
Rung: **3 (one product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the one hunk under "The exact change", byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{X['whatwrong']}

## Where

`{PROD}:{X['line']}`. {X['callers']}

## The exact change

ONE hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The log message text is unchanged. A context line may contain an em dash; copy it unchanged.

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. In particular do NOT touch the other two KS-1868 sites of this file (the other `Failed to publish event` handler, the reset-password revocation block), the KS-1885 code (`authoredExchangeText` at :989-990 and the exchange-error handling near :1113 and :1403; Seat S 10th named :1080-1081 and :1362 at its own tree, which sit about 30-40 lines away at this tip), or any `err?.message` read (:372, :547, :587, :768 here; S 10th listed :371, :546, :586, :767 at its tree): those are a different form and out of this pass.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{X['ref']}`. {X['harness']} The test file contains backslashes in regular expressions, quotes and template strings: keep every character, including every backslash, exactly as given.

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws). {X['red1']}; after the edit the result carries the constant `unreadable thrown value`.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `Error` logs its own message) and 'control ks1868 C2' (the normal path), the controls showing the rig works and the normal path is unchanged.
- The stand-in rejecting with the thrown value is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}:{X['line']}` is the `instanceof Error` read at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 22 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}`; the positive control services/auth appears in 7 file entries.
- services/auth uses its own node_modules; the pinned ref runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the 253 were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path, a real Redis and a real Postgres were not run. The three sequenced passes were not run together by the pipeline.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
