# Operator 49, task 2 (KS-1868 security index.ts :293 and :400): code_patch2 brief generator (O47 shape).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='d7691f35312ea158f043e87a3227e477cccb183d'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
SV='Blockchain/Dev/services/billing/'
PROD=SV+'src/routes/webhooks.ts'
REF=SV+'src/__tests__/webhooks-replay-auth.test.ts'

def mknew(old,ind):
    marker='error: error instanceof Error ? error.message : String(error)'
    assert old.count(marker)==1
    s=' '*ind
    head=(s+"let reason: string;\n"+s+"try {\n"+s+"  reason = error instanceof Error ? error.message : String(error);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
    return head+old.replace(marker,'error: reason')

TESTSRC=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator49/gen/t3_test.ts.txt').read()
T={}
T['p1']=dict(dir='ks_1868_o49_p3_billing_webhook_replay_unreadable_throw', fn='the webhook replay handler', line=316, ind=6,
  test=SV+'src/__tests__/ks1868-billing-webhook-replay-unreadable-throw.test.ts',
  oldblock="      logger.error('Replay failed', { eventId, error: error instanceof Error ? error.message : String(error) });\n",
  indent=6, tbody=TESTSRC,
  descr=dict(
   site_intro="the catch block of the `POST /webhooks/replay` handler in `services/billing/src/routes/webhooks.ts`",
   consequence="Today a hostile rejection from the database layer makes the catch block itself throw, so nothing is logged and the handler's promise rejects instead of answering the constant 500 `Replay failed`.",
   red1="At the tip the route never answers (Express 4 does not see an async handler's rejection), so the request hits the cell's deadline and the status assertion fails",
   whatwrong="In `webhooks.ts` the replay handler (admin-only, KS-157) reads the stored event with `query(...)` inside a try; its catch logs `logger.error('Replay failed', { eventId, error: error instanceof Error ? error.message : String(error) })` (the read is on line 316) and then answers the constant `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Replay failed' } })`. If the database call rejects with a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch; if it rejects with an Error whose `message` getter throws, `error.message` throws. Either way the catch throws before the line is logged and before the 500 is sent, so the handler rejects and the request is left unanswered. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. The response stays the constant 500 `Replay failed` in every case: the thrown text is only ever logged, never sent. An ordinary Error still logs `error: <its message>`.",
   callers="CALLERS: this IS the route handler (`router.post('/replay', authenticate(), requireRole('SYSTEM_ADMIN','SUPER_ADMIN'), ...)`), mounted by billing's index; the comment above it says the gateway does not route `/webhooks/replay`, only `/webhooks/stripe`. There is no other caller. **BEHAVIOUR CHANGE the raise PR must state:** for a hostile throw from the database (inside the try: the event SELECT, `handleWebhookEvent`, the status UPDATE) an admin's replay request today is left UNANSWERED (the async rejection is unhandled, Express 4), and after the fix it is answered with the same constant 500 `Replay failed` an ordinary DB error already gets, with the log line `error: unreadable thrown value`. Nothing from the thrown value reaches the response either way. Note that `handleWebhookEvent` side effects (credit grants) run BEFORE the status UPDATE: a hostile throw from the UPDATE leaves the credits granted and the status unchanged in both the old and new code; this brief does not change that.",
   dbnote="`../db` (`isDbAvailable` true, `query` rejecting with the thrown value), `../services/stripeService` and `../utils/logger` are replaced; the real router runs behind the real shared `authenticate()` / `requireRole` with an RS256 token signed in the test, on a loopback listener (the harness of the pinned ref); no database and no network beyond 127.0.0.1. Because the tip leaves the request unanswered, the cell gives the request a short deadline and counts the unhandled rejection itself instead of letting the runner report it."))
def build(k):
    X=T[k]
    old=mk.rd(PROD); assert old.count(X['oldblock'])==1
    new=old.replace(X['oldblock'],mknew(X['oldblock'],X['indent']))
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    tbody=X['tbody']
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    golden=pd+td
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    pins=("# code_patch2: billing webhooks.ts (1 hunk) + a NEW test file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/billing_src/routes/webhooks.ts_and_src/__tests__/_are_in_no_open_PR_(23_PRs_134_files_read_2026-11-02_by_op49,_billing_only_as_package.json/package-lock.json_in_575/649/1360,_positive_control_services/auth_in_10_entries);_live_lanes_beyond_PRs_not_checked\n")%(REF,X['line'])
    open(d+'/spark.pins','w').write(pins)
    D=X['descr']; tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 billing: {X['fn']} must still report when the thrown value cannot be read (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 49 for Wednesday, 2026-11-02. Secuura (billing) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {D['site_intro']}. {D['consequence']} No open PR touches this file or its `src/__tests__/` directory (the 23 open PRs read 2026-11-02 through the GitHub API; 134 file entries; services/billing appears only as package.json / package-lock.json in PRs 575, 649 and 1360; planted positive control: the same scan finds services/auth in 10 entries). This is the only site of this file in the brief set.

File: `{PROD}`  (product, modified in place: ONE hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; 3 cells (2 red, 1 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/billing`)
Tier: `code_patch2`
Rung: **3 (one product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the one hunk under "The exact change", byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{D['whatwrong']}

## Where

`{PROD}:{X['line']}`. {D['callers']}

## The exact change

ONE hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The log message text contains an em dash; copy it unchanged.

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. 

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (env set first, `vi.mock` of `../db`, the services and the logger, then a top-level-await import of the router mounted on an express app). {D['dbnote']} ****

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws). {D['red1']}; after the edit the result carries the constant `unreadable thrown value`.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `Error` logs its own message), the control showing the normal path is unchanged.
- The stand-in rejecting with the thrown value is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}:{X['line']}` is the `instanceof Error` read at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 23 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (23 PRs, 134 file entries; services/billing only as package.json / package-lock.json); the positive control services/auth appears in 10 file entries.
- This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator.\n- services/billing uses its own node_modules (SPARK_NM_EXCLUDE); the pinned ref `webhooks-replay-auth.test.ts` runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the 253 were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path and a real Postgres were not run.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
