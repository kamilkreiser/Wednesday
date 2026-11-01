# Operator 63: KS-1868 originate systemErrors.ts (P1, reuse in-file fail500) and errorTrackingService.ts trackError (P2, inline guard). Jest. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator63/gen/'
SV='Blockchain/Dev/services/originate/'
TD=SV+'src/__tests__/'
REF=TD+'ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts'
O1=("    logger.error('System error ingest failed', { error: err instanceof Error ? err.message : String(err) });\n"
    "    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });\n")
N1="    fail500(res, 'System error ingest failed', err);\n"
O2=O1.replace('System error ingest failed','Client error ingest failed'); N2=N1.replace('System error ingest failed','Client error ingest failed')
O3="    logger.error('Failed to persist error', { error: err instanceof Error ? err.message : String(err) });\n"
N3=("    let reason: string;\n    try {\n      reason = err instanceof Error ? err.message : String(err);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n"
    "    logger.error('Failed to persist error', { error: reason });\n")
OPEN_PR="No open PR touches this file or its `src/__tests__/` neighbours of the same name (the 22 open PRs read 2026-11-02 through the GitHub API; 125 file entries; services/originate appears only as package.json in PRs 575/949/1726 and three integration-test files in PRs 1790/1792/1794; planted positive control: the same scan finds services/originate in 11 entries)."
T={
 'p1':dict(dir='ks_1868_o63_p1_originate_system_errors_ingest_client_errors_catches_unreadable_throw', prod=SV+'src/routes/systemErrors.ts',
   edits=[(O1,N1),(O2,N2)], hunks='2', nh=2, lines='134 and 165',
   fn='the two ingest catch blocks of originate `routes/systemErrors.ts` (POST /ingest and POST /client-errors)', short='two catch blocks',
   test=TD+'ks1868-system-errors-ingest-catches-p1-unreadable-throw.test.ts', tsrc='t63_p1.ts.txt', ncells='8 cells: 2 routes x (R1, R2, C1, C2)',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route (4 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message and the answer is the constant 500) and 'control ks1868 C2' (a thrown string is logged as itself), once per route (4 cells)",
   whatwrong="In `routes/systemErrors.ts` the catch blocks of POST /ingest (line 134) and POST /client-errors (line 165) each log `logger.error('<context>', { error: err instanceof Error ? err.message : String(err) });` and then answer the CONSTANT 500 `{ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } }`. If the awaited `errorTracking.trackError` call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before anything is logged and before the 500 is sent; the async handler rejects, Express 4 does not catch that, and the request gets no response. The same file already has the guard for exactly this: the module function `fail500(res, context, err)` (KS-730, hardened by KS-1772) describes the value in its own try, logs `{ error: described }` in another, and always sends the same constant 500 body. The four admin routes of the file already use it. The fix replaces the two lines of each catch (the `logger.error` line and the `res.status(500)` line) with ONE call `fail500(res, '<the same context text>', err);`. No helper is added: the existing one is reused.",
   callers="CALLERS (git grep at the tip): both routes are mounted by `src/index.ts` as `systemErrorsRouter`; POST /ingest is called by other services and POST /client-errors by the React error boundary over HTTP (both unauthenticated ingest paths). The 500 body is identical before and after. **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable thrown value from `trackError`: today the catch throws, nothing is logged and the caller gets NO response (unhandled rejection); after, the log line `{ error: 'thrown value that could not be described' }` is written under the same context text and the caller gets the constant 500 an ordinary Error already gets. (2) Log text for a thrown value that is NOT an Error and NOT a string (e.g. a plain object): today `String(err)` (`[object Object]`); after, `fail500`'s description `thrown <Constructor> with fields [<keys>]` (the form KS-1346 chose for the other six routes of this file). Ordinary Errors and strings log exactly what they log today (pinned by the existing `ks730a` cells A3 and A4, which stay green). (3) Persisted state: none changes (`trackError` swallows its own database failures, so it can only reject with a hostile value in tests).",
   dbnote="`../services/errorTrackingService` (its five exports), `../middleware/auth` (pass-through) and `../utils/logger` are replaced; the router is mounted on a real loopback listener under `/api/system-errors` and driven with `fetch`; no database is touched.",
   red1="At the tip the handler rejects instead of answering, so the request reports `NO ANSWER` after 1.5 seconds and the assertion fails",
   fix_nature="reuses the in-file `fail500` helper (KS-730 / KS-1772)", pin_files="systemErrors.ts"),
 'p2':dict(dir='ks_1868_o63_p2_originate_error_tracking_track_error_catch_unreadable_throw', prod=SV+'src/services/errorTrackingService.ts',
   edits=[(O3,N3)], hunks='1', nh=1, lines='65',
   fn='the catch block of `trackError` in originate `services/errorTrackingService.ts`', short='one log-only catch',
   test=TD+'ks1868-error-tracking-track-error-p2-unreadable-throw.test.ts', tsrc='t63_p2.ts.txt', ncells='5 cells: 2 red (R1, R2) + 3 controls (C1 ordinary Error, C2 string, C3 success)',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws) as the value the database insert rejects with (2 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message and `trackError` resolves), 'control ks1868 C2' (a thrown string is logged as itself) and 'control ks1868 C3' (a successful insert logs nothing and reaches the database once) (3 cells)",
   whatwrong="In `services/errorTrackingService.ts` the function `trackError` is documented as \"never throws (fire-and-forget for error handlers)\", and its catch block (line 63) logs `logger.error('Failed to persist error', { error: err instanceof Error ? err.message : String(err) });` (line 65), after the comment \"Never throw from error tracking\". If the database insert rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws, nothing is logged, and `trackError` REJECTS, breaking its own contract. The fix keeps the `logger.error` line's text and replaces only the value: it first reads the same expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `{ error: reason }`. This is the inline guard already merged in originate `routes/certifications.ts` (a `let reason: string; try { ... } catch { reason = 'unreadable thrown value'; }`); this service has no helper and none is added.",
   callers="CALLERS (git grep at the tip): `middleware/errorHandler.ts` (fire-and-forget, after a 5xx), `src/index.ts` :79 and :84 (`.catch(() => {})` on unhandledRejection / uncaughtException) and the two awaited calls in `routes/systemErrors.ts` (POST /ingest, POST /client-errors). **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable thrown value from the insert: today `trackError` rejects (its contract says it never does); after, the constant reason is logged and it resolves, exactly what an ordinary Error already gets. (2) Consequence for the two ingest routes, only for such a value: today they reach their catch and answer 500; after, `trackError` resolves and they answer `201 { success: true }`, which is what they already answer when an ORDINARY database error happens (trackError swallows it). No response for an ordinary Error or a string changes. (3) Persisted state: none (the insert failed in both cases; no audit or retry). Left out on purpose: the sibling catch in `getRecentErrors` (line 135): it returns the list the GET /api/system-errors body is built from, so for an unreadable value the route's 500 would become a 200 with an empty list, a client-visible body change that needs Kam's call.",
   dbnote="`../db` (a `prisma` whose `$executeRaw` and `$queryRaw` are plain jest stand-ins; the tagged-template call is a normal function call) and `../utils/logger` are replaced; `trackError` is called directly; no database is touched.",
   red1="At the tip the catch throws inside itself, so `trackError` is REJECTED (read through `.then(() => 'resolved', () => 'REJECTED')`) and the assertion fails",
   fix_nature="adds the inline `let reason` guard (originate certifications.ts shape)", pin_files="errorTrackingService.ts"),
}
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
    pins=("# code_patch2: originate %s (%s hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/originate_%s_and_src/__tests__/_are_in_no_open_PR_(22_PRs_125_files_read_2026-11-02_by_op63,_originate_only_as_package.json_and_3_integration_tests_in_575/949/1726/1790/1792/1794,_positive_control_services/originate_in_11_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['pin_files'],X['hunks'],REF,first,X['pin_files'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 originate: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunk(s) given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 63 for Wednesday, 2026-11-02. Secuura (originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file ({X['fix_nature']}; lines {X['lines']}). {OPEN_PR} Sibling files are separate briefs (O63-P1 systemErrors.ts, O63-P2 errorTrackingService.ts); each pass is generated against the same tip and is disjoint from the other.

File: `{PROD}`  (product, modified in place: EXACTLY {X['hunks']} hunk(s))
Test file: `{X['test']}`  (NEW file, jest, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `jest` (`npx jest src/__tests__/{tp}` from `Blockchain/Dev/services/originate`)
Tier: `code_patch2`
Rung: **3 ({X['hunks']} product hunk(s), skeletons dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the {X['hunks']} hunk(s) under "The exact change", in that order, byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{X['whatwrong']}

## Where

`{PROD}`: lines {X['lines']}. {X['callers']}

## The exact change

EXACTLY {X['hunks']} hunk(s) in the product file. The file header lines and every `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any other catch block of the file, any message text, or any other line.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (a jest file that replaces the service, auth and logger modules and drives the router on a loopback listener). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells
{X['redlines']}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {X['red1']}; after the edit the constant reason is logged.
- GREEN at the tip and after: {X['greens']}.

## Premises (each one measured, with where)

- `{PROD}` lines {X['lines']} are the `instanceof Error` reads at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 22 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` (125 file entries; services/originate only as package.json in PRs 575/949/1726 and integration tests in 1790/1792/1794); the positive control services/originate appears in 11 file entries.
- The existing originate suites that cover this file (`ks730a`, `ks1346a`, `ks444`, `ks1780-system-errors`) pass at the tip in the same clone (measured: whole-suite baseline 163 suites, 36 s; the 37 red suites there are unrelated to these files and load-fail on a stale `@secuura/shared` build).

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). A real Express listener is used for P1; a real Postgres is not.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
