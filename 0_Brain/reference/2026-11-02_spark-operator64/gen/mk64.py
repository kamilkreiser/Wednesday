# Operator 64: KS-1868 analytics/src/routes/analytics.ts three clean route catches (code_patch2, O57 shape).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator64/gen/'
SV='Blockchain/Dev/services/analytics/'
PROD=SV+'src/services/scheduledJobs.ts'
TD=SV+'src/__tests__/'
REF=TD+'ks1868-scheduled-jobs-save-alert-rule-unreadable-throw.test.ts'
def guard(ind, expr, var):
    s=' '*ind
    return (s+"let %s: string;\n"%var+s+"try {\n"+s+"  %s = %s;\n"%(var,expr)+s+"} catch {\n"+s+"  %s = 'unreadable thrown value';\n"%var+s+"}\n")
E="err instanceof Error ? err.message : String(err)"
def site(msg):
    old="    logger.info('%s', { error: %s });\n"%(msg,E)
    new=guard(4,E,'reason')+"    logger.info('%s', { error: reason });\n"%msg
    return old,new
T={
 'p1':dict(dir='ks_1868_o64_p1_analytics_scheduledjobs_dbsavealert_unreadable_throw',
   edits=[site('DB save alert failed')],
   fn='the dbSaveAlert catch of analytics `services/scheduledJobs.ts`',
   short='one log-only catch', lines='90-92 (the catch at line 90, the read at line 91)',
   test=TD+'ks1868-scheduled-jobs-save-alert-unreadable-throw.test.ts', tsrc='t64_p1.ts.txt', ncells='4 cells: R1, R2, C1, C2',
   hunks='1', nh=1,
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws)",
   greens="'control ks1868 C1' (an ordinary `Error` logs its own message under the existing `logger.info` text) and 'control ks1868 C2' (a thrown string is logged as itself, as before)",
   whatwrong="In `services/scheduledJobs.ts` the module-level function `dbSaveAlert` (line 69) pushes the alert into memory, then runs an INSERT ... ON CONFLICT inside a `try`; its catch (line 90) has one line that reads the caught value: `logger.info('DB save alert failed', { error: err instanceof Error ? err.message : String(err) });`. The message is only logged. If the query rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before anything is logged and `dbSaveAlert` rejects instead of resolving. The sole caller, `ScheduledJobs.acknowledgeAlert` (line 486), calls `dbSaveAlert(alert).catch(() => {})`, so the rejection is swallowed: today the scheduler loop, the cron jobs and acknowledgeAlert's `return true` are unaffected, and only the INFO line is lost. The fix puts a `let reason: string;` plus a `try` that runs the SAME expression and a `catch` that sets the constant `'unreadable thrown value'` just above the `logger.info` line, and changes that line to log `{ error: reason }`; the log text is untouched and an ordinary Error still logs its own message. This is the inline guard (variable `reason`) already merged at the tip in this same file (dbSaveAlertRule line 58-64, loadScheduledJobsFromDb line 155-161), exportService.ts, analyticsService.ts and metricsCollector.ts; no helper is added.",
   callers="CALLERS (git grep at the tip): `dbSaveAlert` is module-private and has ONE caller, `ScheduledJobs.acknowledgeAlert` (line 486, `dbSaveAlert(alert).catch(() => {})`); no route in analytics src calls `acknowledgeAlert` (git grep: only the definition). The cron callbacks (`addJob`) never reach it. **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable thrown value from the INSERT: today the catch throws, `dbSaveAlert` rejects and the empty `.catch` swallows it, so nothing is logged; after, the constant reason is logged at INFO exactly as an ordinary Error already is (cells R1/R2 against control C1). The alert stays acknowledged in memory either way (the in-memory update precedes the save). (2) Persisted state: the INSERT failed in both cases, so nothing is written either way. The scheduler loop is not affected in either state (the rejection never reaches it). No log text for an ordinary Error or a string changes.",
   dbnote="`../db` (`isDbAvailable` returns true, `query` rejects with the value the cell sets) and `../utils/logger` (`info` is a spy recording the call) are replaced; the real `ScheduledJobs` class is built with a stub metrics collector, one rule is added and evaluated to raise a real alert, and `acknowledgeAlert` is called; no database is touched.",
   red1="At the tip the catch throws inside `dbSaveAlert` (swallowed by the empty `.catch`), so no `DB save alert failed` line is recorded and the length assertion fails"),
}
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 22 open PRs read 2026-11-02 through the GitHub API; 125 file entries; services/analytics appears only as package.json / package-lock.json in PRs 575, 649, 948 and 1360; planted positive control: the same scan finds services/originate in 6 entries)."
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
    pins=("# code_patch2: analytics services/scheduledJobs.ts (%s hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/analytics_src/services/scheduledJobs.ts_and_src/__tests__/_are_in_no_open_PR_(22_PRs_125_files_read_2026-11-02_by_op64,_analytics_only_as_package.json/package-lock.json_in_575/649/948/1360,_positive_control_services/originate_in_6_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['hunks'],REF,first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 analytics: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunks given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 64 for Wednesday, 2026-11-02. Secuura (analytics) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (lines {X['lines']}). {OPEN_PR} This is the only pass (O64-P1) on this file. The other catches of this file already carry the guard at the tip, or pass the raw value to the logger without reading it, and are not touched.

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

**Do NOT touch** any message text, any other line of the file, or any other catch block in it.

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
- Open PRs: 20 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (125 file entries; services/analytics only as package.json / package-lock.json in PRs 575, 649, 948 and 1360); the positive control services/originate appears in 6 file entries.
- The existing sibling tests `ks1868-scheduled-jobs-save-alert-rule-unreadable-throw.test.ts` and `ks1868-scheduled-jobs-load-unreadable-throw.test.ts` (merged) cover the other two guarded catches and run in the baseline; no existing test reads `dbSaveAlert` or `acknowledgeAlert`.
- The pinned ref `ks1868-scheduled-jobs-save-alert-rule-unreadable-throw.test.ts` (merged KS-1868 analytics test, same module and same db/logger mocks) runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were already guarded and were not touched. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path, a real Postgres and a real Express 4 were not run.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
