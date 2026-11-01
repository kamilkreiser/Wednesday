# Operator 54: KS-1868 services/security/src/index.ts (key-register route save catch, ~:1411-1417)
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator54/gen/'
SV='Blockchain/Dev/services/security/'
PROD=SV+'src/index.ts'
TD=SV+'src/__tests__/'
def edit1(t,old,new):
    assert t.count(old)==1, old
    return t.replace(old,new)
P1_OLD=("      memApiKeys.delete(apiKey.id);\n      const infra = isInfrastructureDbError(saveErr);\n"
        "      log('error', 'KS-888: API key mint refused, the key could not be saved', { keyId: apiKey.id, code: saveErr?.code, infra });\n")
P1_NEW=("      memApiKeys.delete(apiKey.id);\n      let infra = false;\n      let code: unknown;\n      try {\n        infra = isInfrastructureDbError(saveErr);\n        code = saveErr?.code;\n      } catch {\n"
        "        // A thrown value that cannot be read cannot be classified: no code, not infrastructure (500), as for any non-infrastructure error.\n      }\n"
        "      log('error', 'KS-888: API key mint refused, the key could not be saved', { keyId: apiKey.id, code, infra });\n")
def p1(t): return edit1(t,P1_OLD,P1_NEW)
COMMON_PR=("No open PR touches this file: the 19 open PRs read 2026-11-02 07:04 AEDT through the GitHub API (108 file entries) were scanned for `services/security/src/index.ts` and none lists it; planted positive control: the same scan finds services/security in 2 file entries (and services/auth in 7).")
REF=TD+'ks1868-security-save-key-and-retire-priors-unreadable-throw.test.ts'
T={}
T['p1']=dict(dir='ks_1868_o54_p1_security_key_register_save_catch_unreadable_throw', fix=p1, line=1413, tag='O54-P1', test=TD+'ks1868-security-key-register-save-catch-unreadable-throw.test.ts', tsrc='t54_p1.ts.txt', ref=REF,
  title="the key-register route's save catch must still log its KS-888 line and answer 500 when the thrown value cannot be read",
  site="the save catch of the `POST /api/keys` handler (the key-register route), the one that reads `isInfrastructureDbError(saveErr)` and `saveErr?.code`",
  quote="`const infra = isInfrastructureDbError(saveErr);` / `code: saveErr?.code`",
  whatwrong="In `index.ts` the `POST /api/keys` handler saves the new key inside a `try` (a rotate through `saveKeyAndRetirePriors`, otherwise `dbSaveApiKey`). Its `catch (saveErr: any)` first drops the in-memory key, then classifies the failure with `const infra = isInfrastructureDbError(saveErr);` (line 1413; that helper reads `err.code` and `err.message`, :1150-1152) and logs the KS-888 line with `code: saveErr?.code` (line 1414), then answers 503 (infrastructure) or 500 with `The API key could not be saved, so no key was issued`. If the INSERT rejects with a revoked Proxy, any property read throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `isInfrastructureDbError` throws on `e?.message`. Either way the catch throws before the log line and before its JSON answer, so the KS-888 line is lost and the request falls through to the generic error path. The fix computes `infra` (starting `false`) and `code` inside an inner `try` and, when the value cannot be read, leaves them at `false` and `undefined`; the log call uses the local `code`. An ordinary Error is unchanged (its `code` is still logged and still classified).",
  callers="CALLERS (git grep at the tip): the handler is the route itself (`app.post('/api/keys', ...)`, :1176, behind `requireKeyAdminOrProvisioner`); it is called by the gateway `register-connector` route (api-gateway routes/platform.ts) and by operators. The catch only runs on the rotate path in practice (`saveKeyAndRetirePriors` rethrows the raw value out of `transaction()`); `dbSaveApiKey`'s own catch reads `err?.message` first (a different read, not touched). **BEHAVIOUR CHANGE the raise PR must state:** when the rotate INSERT rejects with an unreadable value, the route today logs NO `KS-888: API key mint refused` line and answers 500 with the generic `An unexpected error occurred` (gate 90, G90-F4: no key issued, nothing committed, ROLLBACK, no unhandled rejection); after the fix it logs the KS-888 line (`infra: false`, no code) and answers 500 INTERNAL_ERROR `The API key could not be saved, so no key was issued`, which is exactly what an ordinary non-infrastructure Error already gets. Status stays 500, fail-closed is unchanged, and no 503 is produced for an unreadable value (it cannot be classified as infrastructure). The sibling catches at :1582 (revoke) and :1773 (admin-scopes) read `isInfrastructureDbError` the same way and are NOT touched by this pass.",
  harness="`../db` is replaced (`isDbAvailable` true, a `transaction` whose client rejects the INSERT into `svc_api_keys` with the test's value, every other statement resolving empty); the real app runs on a loopback listener behind a real RS256 `super_admin` token (the ks888 harness); console.log is spied for the JSON log lines; no database and no network beyond loopback.",
  red1="At the tip the catch throws, so no `KS-888: API key mint refused` line is logged and the answer is the generic `An unexpected error occurred`, not `The API key could not be saved, so no key was issued`")
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
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_security/src/index.ts_is_in_no_open_PR_(19_PRs_108_files_read_2026-11-02_by_op54,_positive_control_services/security_in_2_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['ref'],X['line'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 security: {X['title']} (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 54 for Wednesday, 2026-11-02. Secuura (security) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {X['site']} in `services/security/src/index.ts`. {COMMON_PR} PR 1908 (merged as 8eae0dda) already guarded the :293 and :400 catches in this file with the same inner-try pattern; gate 90 found this one (finding G90-F4).

File: `{PROD}`  (product, modified in place: ONE hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; 4 cells (2 red, 2 control))
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

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. In particular do NOT touch the revoke route's save catch (:1582), the admin-scopes catch (:1773), `isInfrastructureDbError` itself (:1149), `dbSaveApiKey`, or the two catch blocks that already carry the inner `try` (:293 and :400).

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
- Open PRs: 19 (108 file entries) read 2026-11-02 07:04 AEDT via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}`; the positive control services/security appears in 2 file entries.
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
