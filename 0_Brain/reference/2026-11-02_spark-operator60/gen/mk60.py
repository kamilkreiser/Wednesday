# Operator 60: KS-1868 analytics/src/routes/analytics.ts three clean route catches (code_patch2, O57 shape).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator60/gen/'
SV='Blockchain/Dev/services/analytics/'
PROD=SV+'src/routes/analytics.ts'
TD=SV+'src/__tests__/'
REF=TD+'ks1868-export-service-db-save-unreadable-throw.test.ts'
def guard(ind, expr, var):
    s=' '*ind
    return (s+"let %s: string;\n"%var+s+"try {\n"+s+"  %s = %s;\n"%(var,expr)+s+"} catch {\n"+s+"  %s = 'unreadable thrown value';\n"%var+s+"}\n")
E="error instanceof Error ? error.message : String(error)"
def site(msg):
    old="    logger.error('%s', { error: %s });\n"%(msg,E)
    new=guard(4,E,'reason')+"    logger.error('%s', { error: reason });\n"%msg
    return old,new
T={
 'p1':dict(dir='ks_1868_o60_p1_analytics_routes_realtime_export_by_id_export_list_unreadable_throw',
   edits=[site('Error fetching real-time metrics'),site('Error fetching export'),site('Error listing exports')],
   fn='three route catches of analytics `routes/analytics.ts` (GET /realtime, GET /exports/:id, GET /exports)',
   short='three log-only route catches', lines='245, 350 and 372',
   test=TD+'ks1868-analytics-routes-catches-p1-unreadable-throw.test.ts', tsrc='t60_p1.ts.txt', ncells='12 cells: 3 routes x (R1, R2, C1, C2)',
   hunks='3', nh=3,
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route (6 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` logs its own message under the existing `logger.error` text and the answer is the constant 500 without it) and 'control ks1868 C2' (a thrown string is logged as itself, as before), once per route (6 cells)",
   whatwrong="In `routes/analytics.ts` the catch blocks of GET /realtime (line 245), GET /exports/:id (line 350) and GET /exports (line 372) each have NO ZodError branch and one line that reads the caught value: `logger.error('<text>', { error: error instanceof Error ? error.message : String(error) });`, followed by the CONSTANT 500 body `{ success: false, error: { code: 'INTERNAL_ERROR', message: '<fixed text>' } }`; the message is only logged. If the service call rejects with a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `error.message` throws. Either way the catch throws before anything is logged and before the 500 is sent; the async handler rejects, Express 4 does not catch that, and the request gets no response (the gateway proxy times out). The fix puts a `let reason: string;` plus a `try` that runs the SAME expression and a `catch` that sets the constant `'unreadable thrown value'` just above the `logger.error` line, and changes that line to log `{ error: reason }`; the log text and the 500 are untouched, and an ordinary Error still logs its own message. This is the inline guard (variable `reason`) already merged in this service (exportService.ts dbSaveExport and loadFromDb, analyticsService.ts, metricsCollector.ts, scheduledJobs.ts); no helper is added. The OTHER nine catches of this file open with `instanceof z.ZodError`, which throws first on a revoked Proxy, so a message-line fix would be half a fix there: they are deliberately NOT in this series.",
   callers="CALLERS (git grep at the tip): the router is mounted at `/api/analytics` in analytics `src/index.ts` (:78) and reached over HTTP through the api-gateway proxy (`routes/proxy.ts` :1219, `proxy('analytics', ...)`); no in-process caller. All three routes are READ-ONLY (GET): realtime metrics, one export's status, the export list. **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable thrown value from the service call: today the catch itself throws, the request gets NO response and Node sees an unhandled rejection; after, the constant reason is logged and the route answers its existing constant 500, exactly what an ordinary Error already gets (cells R1/R2 against control C1). (2) Persisted state: none (no write on these routes). No response body, status code or log text for an ordinary Error or a string changes.",
   dbnote="`express` (a `Router` whose `get` and `post` capture the handlers), `../services/analyticsService`, `../services/exportService` (each method rejects with the value the cell sets) and `../utils/logger` (`error` is a spy recording the call) are replaced; the captured handler is called with a fake request and response, no port is bound, no database is touched.",
   red1="At the tip the handler rejects instead of answering, so the response stays at the default 200 and the status assertion fails"),
}
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 20 open PRs read 2026-11-02 through the GitHub API; 113 file entries; services/analytics appears only as package.json / package-lock.json in PRs 575, 649, 948 and 1360; planted positive control: the same scan finds services/originate in 6 entries)."
def build(k):
    X=T[k]
    old=mk.rd(PROD); new=old
    for o,n in X['edits']:
        assert new.count(o)==1,(k,o[:70],new.count(o))
        new=new.replace(o,n)
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    hl=[l for l in pd.splitlines() if l.startswith('@@ ')]
    assert len(hl)==X['nh'],(k,len(hl))
    tbody=open(GEN+X['tsrc'],encoding='utf-8').read()
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    golden=pd+td
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    # first changed line (new-file numbering is irrelevant; the pin is the OLD line of the first '-')
    first=0
    cur=None
    for l in pd.splitlines():
        if l.startswith('@@ '):
            cur=int(l.split()[1].split(',')[0][1:]); continue
        if cur is None: continue
        if l.startswith('-') and not l.startswith('---'): first=cur; break
        if l.startswith(' ') : cur+=1
    assert first
    pins=("# code_patch2: analytics routes/analytics.ts (%s hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/analytics_src/routes/analytics.ts_and_src/__tests__/_are_in_no_open_PR_(20_PRs_113_files_read_2026-11-02_by_op60,_analytics_only_as_package.json/package-lock.json_in_575/649/948/1360,_positive_control_services/originate_in_6_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['hunks'],REF,first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 analytics: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunks given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 60 for Wednesday, 2026-11-02. Secuura (analytics) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (lines {X['lines']}). {OPEN_PR} This is the only pass (O60-P1) on this file. The nine catch blocks that start with an `instanceof z.ZodError` check (overview, certifications, verifications, governance, revenue, users, activity, POST exports, POST reports) are deliberately NOT in this series: on a revoked Proxy that check throws before the message line, so a message-line-only fix would be half a fix.

File: `{PROD}`  (product, modified in place: EXACTLY {X['hunks']} hunks)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/analytics`)
Tier: `code_patch2`
Rung: **3 ({X['hunks']} product hunks, skeletons dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the {X['hunks']} hunks under "The exact change", in that order, byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{X['whatwrong']}

## Where

`{PROD}`: lines {X['lines']}. {X['callers']}

## The exact change

EXACTLY {X['hunks']} hunks in the product file, in this order. The file header lines and every `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The log message text (the string literal before `, `) is unchanged. **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it (in particular the nine catch blocks that start with `instanceof z.ZodError`).

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (a vitest file that replaces the module's collaborators with plain functions and a spy logger). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character, including every backslash, exactly as given.

```diff
{td}```

## Red cells
{X['redlines']}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {X['red1']}; after the edit the constant `unreadable thrown value` is logged.
- GREEN at the tip and after: {X['greens']}.
- The stand-ins rejecting with the thrown value are plain functions, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` lines {X['lines']} are the `instanceof Error` reads at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 20 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (113 file entries; services/analytics only as package.json / package-lock.json in PRs 575, 649, 948 and 1360); the positive control services/originate appears in 6 file entries.
- No existing analytics test reads `routes/analytics.ts` as text or imports it (git grep at the tip); the ks1364 tests only cite it in comments. No ZodError block is touched.
- The pinned ref `ks1868-export-service-db-save-unreadable-throw.test.ts` (merged KS-1868 analytics test) runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path, a real Postgres and a real Express 4 were not run.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
