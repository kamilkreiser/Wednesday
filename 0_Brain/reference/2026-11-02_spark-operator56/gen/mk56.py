# Operator 54: KS-1868 services/security/src/index.ts (key-register route save catch, ~:1411-1417)
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator56/gen/'
SV='Blockchain/Dev/services/security/'
PROD=SV+'src/index.ts'
TD=SV+'src/__tests__/'
def edit1(t,old,new):
    assert t.count(old)==1, old
    return t.replace(old,new)
P1_OLD=("    const infra = isInfrastructureDbError(saveErr);\n"
        "    log('error', 'KS-888: API key revoke not stored, the key is revoked in this process only', { keyId: apiKey.id, code: saveErr?.code, infra });\n")
P1_NEW=("    let infra = false;\n    let code: unknown;\n    try {\n      infra = isInfrastructureDbError(saveErr);\n      code = saveErr?.code;\n    } catch {\n"
        "      // A thrown value that cannot be read cannot be classified: no code, not infrastructure (500), as for any non-infrastructure error.\n    }\n"
        "    log('error', 'KS-888: API key revoke not stored, the key is revoked in this process only', { keyId: apiKey.id, code, infra });\n")
def p1(t): return edit1(t,P1_OLD,P1_NEW)
P2A_OLD=("    if (error instanceof z.ZodError) return badRequestFromZod(res, error);\n    // The pull request 1539 gate's m1. An infrastructure fault reached errorHandler and answered a\n")
P2A_NEW=("    let isZod = false;\n    let infra = false;\n    try {\n      isZod = error instanceof z.ZodError;\n      infra = isInfrastructureDbError(error);\n    } catch {\n"
         "      // A thrown value that cannot be read cannot be classified: hand the error handler an ordinary Error, as for any non-infrastructure error.\n      return next(new Error('unreadable thrown value'));\n    }\n"
         "    if (isZod) return badRequestFromZod(res, error as z.ZodError);\n    // The pull request 1539 gate's m1. An infrastructure fault reached errorHandler and answered a\n")
P2B_OLD="    if (isInfrastructureDbError(error)) {\n      // Read off the request"
P2B_NEW="    if (infra) {\n      // Read off the request"
def p2(t): return edit1(edit1(t,P2A_OLD,P2A_NEW),P2B_OLD,P2B_NEW)
SCAN=("19 PRs / 108 file entries read 2026-11-02 07:12 AEDT through the GitHub API by operator 56 (prscan_start.out); services/security/src/index.ts is in none; planted positive control: the same scan finds services/security in 2 file entries (and services/auth in 7)")
COMMON_PR="No open PR touches this file: the "+SCAN+"."
REF=TD+'ks1868-security-save-key-and-retire-priors-unreadable-throw.test.ts'
PINS_OK=("KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_security/src/index.ts_is_in_no_open_PR_(19_PRs_108_files_read_2026-11-02_by_op56,_positive_control_services/security_in_2_entries);_live_lanes_beyond_PRs_not_checked")
T={}
T['p1']=dict(dir='ks_1868_o56_p1_security_key_revoke_save_catch_unreadable_throw', fix=p1, line=1583, tag='O56-P1', test=TD+'ks1868-security-key-revoke-save-catch-unreadable-throw.test.ts', tsrc='t56_p1.ts.txt', ref=REF,
  title="the key revoke route's save catch must still log its KS-888 line and answer 500 when the thrown value cannot be read",
  site="the save catch of the `DELETE /api/keys/:id` handler (the key revoke route), the one that reads `isInfrastructureDbError(saveErr)` and `saveErr?.code`",
  whatwrong="In `index.ts` the `DELETE /api/keys/:id` handler marks the key inactive in memory (`apiKey.isActive = false`), then persists it inside a `try` with `await dbSaveApiKey(apiKey, { rethrow: true })`. Its `catch (saveErr: any)` classifies the failure with `const infra = isInfrastructureDbError(saveErr);` (line 1583; that helper reads `err.code` and `err.message`, :1150-1152) and logs the KS-888 line with `code: saveErr?.code` (line 1584), then answers 503 (infrastructure) or 500 with `The API key revoke could not be saved, so it may not survive a restart`. `dbSaveApiKey`'s own catch reads only `err?.message` before it rethrows the raw value, so a rejection whose `message` is readable but whose `code` getter throws reaches the route catch unchanged, and the read of `.code` throws inside the catch block. The handler is `async` on Express 4, so the throw becomes an unhandled rejection, no answer is sent and the KS-888 line is lost. The fix computes `infra` (starting `false`) and `code` inside an inner `try` and, when the value cannot be read, leaves them at `false` and `undefined`; the log call uses the local `code`. An ordinary Error is unchanged (its `code` is still logged and still classified).",
  callers="CALLERS (git grep at the tip): the handler is the route itself (`app.delete('/api/keys/:id', requireKeyAdmin, ...)`, ~:1525); no other code calls it in process (callers are operators and the gateway/admin UI over HTTP). **BEHAVIOUR CHANGE the raise PR must state:** when the revoke's save rejects with a value whose `code` cannot be read, the route today throws inside its catch (unhandled rejection in an async Express 4 handler: no answer, no KS-888 line); after the fix it logs the KS-888 line (`infra: false`, no code) and answers 500 INTERNAL_ERROR `The API key revoke could not be saved, so it may not survive a restart`, which is exactly what an ordinary non-infrastructure Error already gets. The key is revoked in this process in both cases (`apiKey.isActive = false` runs before the try and the catch never un-revokes it), and nothing is persisted in either, so whether the key ends up revoked does not change; 503 is never produced for an unreadable value. A revoked Proxy does not reach this catch raw: `dbSaveApiKey`'s `err?.message` read turns it into a TypeError first (control cell C3), so it is not a red cell. The sibling catches at :1411 (key-register save, operator 54) and :1773 (admin-scopes) are NOT touched by this pass.",
  harness="`../db` is replaced (`isDbAvailable` true, a `query` that rejects an `INSERT INTO svc_api_keys` with the test's value once the test sets it, every other statement resolving empty); the key is minted first through the real `POST /api/keys` (the stand-in accepts that INSERT) and then revoked through the real `DELETE /api/keys/:id` on a loopback listener behind a real RS256 `super_admin` token (the ks888 harness); console.log is spied for the JSON log lines; no database and no network beyond loopback.",
  red1="At the tip the catch throws on the `.code` read, so no `KS-888: API key revoke not stored` line is logged and no answer is sent (the request times out), not the 500 `The API key revoke could not be saved, so it may not survive a restart`",
  donot="the key-register save catch (:1411), the admin-scopes catch (:1773), `isInfrastructureDbError` itself (:1149), `dbSaveApiKey`, `apiKey.isActive = false` and the in-memory revoke above the try")
T['p2']=dict(dir='ks_1868_o56_p2_security_admin_scopes_put_catch_unreadable_throw', fix=p2, line=1768, tag='O56-P2', test=TD+'ks1868-security-admin-scopes-put-catch-unreadable-throw.test.ts', tsrc='t56_p2.ts.txt', ref=REF,
  title="the admin-scopes write route's catch must still answer 500 when the thrown value cannot be read",
  site="the catch of the `PUT /api/keys/admin-scopes/:userId` handler (the admin organisation scope write), the one that tests `error instanceof z.ZodError` and then `isInfrastructureDbError(error)`",
  whatwrong="In `index.ts` the `PUT /api/keys/admin-scopes/:userId` handler runs its DELETE, INSERT and audit statements in one `transaction()` (a failure rolls everything back and rethrows the raw value). Its `catch (error)` first tests `error instanceof z.ZodError` (line 1768) and then `isInfrastructureDbError(error)` (line 1773; that helper reads `err.code` and `err.message`, :1150-1152), and otherwise calls `next(error)`. If the transaction rejects with a revoked Proxy, the `instanceof` test itself throws a TypeError (it reads the prototype of the revoked object); if it rejects with an Error whose `message` getter throws, `isInfrastructureDbError` throws on `e?.message`. Either way the catch throws, in an `async` handler on Express 4, so the throw becomes an unhandled rejection and no answer is sent. The fix reads both classifications inside one inner `try` (`isZod`, starting `false`, and `infra`, starting `false`); when the value cannot be read the catch calls `next(new Error('unreadable thrown value'))`, handing the error handler an ordinary Error. The `badRequestFromZod` branch and the 503 infrastructure branch are unchanged and keep their order, and a readable value takes exactly the paths it takes today.",
  callers="CALLERS (git grep at the tip): the handler is the route itself (`app.put('/api/keys/admin-scopes/:userId', requireAdminScopeWriter, ...)`, :1631), behind `platformRoleGate`; it is called over HTTP by platform operators. **BEHAVIOUR CHANGE the raise PR must state:** when the scope transaction rejects with a value that cannot be read, the route today throws inside its catch (unhandled rejection in an async Express 4 handler: no answer is sent); after the fix it answers 500 INTERNAL_ERROR through the error handler, exactly as an ordinary non-infrastructure Error already does (cell C1). Nothing is written in either case: the transaction has already rolled back, so no admin organisation scope changes and no key is created or revoked (the route is a pure scope write). 503 is never produced for an unreadable value, and the infrastructure branch (cell C3) is unchanged. The catch of the GET route below it (:1803) has the same `instanceof` read and is NOT touched by this pass; nor are the key-register save catch (:1411, operator 54) and the revoke save catch (:1582, operator 56 P1).",
  harness="`../db` is replaced (`isDbAvailable` true; `query` answers the target-ADMIN lookup `SELECT 1 FROM users` with one row and everything else empty; a `transaction` whose client rejects the `DELETE FROM admin_organisation_scopes` with the test's value, every other statement resolving empty); the real app runs on a loopback listener behind a real RS256 `super_admin` token (the ks888 harness); console.log is spied for the JSON log lines; no database and no network beyond loopback.",
  red1="At the tip the catch throws, so no answer is sent (the request times out), not the 500 `INTERNAL_ERROR` an ordinary Error gets",
  donot="the GET admin-scopes catch (:1803), the key-register save catch (:1411), the revoke save catch (:1582), `isInfrastructureDbError` itself (:1149), `badRequestFromZod`, and the message texts")
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
    pins=("# code_patch2: security index.ts (1 hunk) + a NEW test file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok="+PINS_OK+"\n")%(X['ref'],X['line'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 security: {X['title']} (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 56 for Wednesday, 2026-11-02. Secuura (security) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {X['site']} in `services/security/src/index.ts`. {COMMON_PR} PR 1908 (merged as 8eae0dda) already guarded the :293 and :400 catches in this file with the same inner-try pattern; operator 54 found this site beside the key-register save catch it fixed at :1411 (a separate, disjoint hunk).

File: `{PROD}`  (product, modified in place: ONE hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; 5 cells (2 red, 3 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/security`)
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

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. In particular do NOT touch {X['donot']}, or the two catch blocks that already carry the inner `try` (:293 and :400).

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{X['ref']}`. {X['harness']} The test file contains backslashes in regular expressions, quotes and template strings: keep every character, including every backslash, exactly as given.

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws). {X['red1']}.
- GREEN at the tip and after: the 'control ks1868' cells (C1 an ordinary `Error`, C2 the normal path, C3 as named in the test), the controls showing the rig works, that the answer for an ordinary Error is the one R1 and R2 must now match, and that the normal path is unchanged.
- The stand-in rejecting with the thrown value is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}:{X['line']}` is the unguarded read at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: {SCAN}; none touches `{PROD}`.
- The pinned ref runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the 253 were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path, a real Redis and a real Postgres were not run. The route was not run against a real Postgres.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
