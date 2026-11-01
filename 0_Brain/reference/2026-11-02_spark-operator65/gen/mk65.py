# Operator 65: KS-1868 originate systemErrors.ts (P1, reuse in-file fail500) and errorTrackingService.ts trackError (P2, inline guard). Jest. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator65/gen/'
SV='Blockchain/Dev/services/originate/'
TD=SV+'src/__tests__/'
REF=TD+'ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts'
def edit(kind,ctx):
    o=("    logger.error('%s: database connection FAILED \u2014 %s will not be available', {\n"
       "      error: err instanceof Error ? err.message : String(err),\n    });\n")
    n=("    let reason: string;\n    try {\n      reason = err instanceof Error ? err.message : String(err);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n"
       "    logger.error('%s: database connection FAILED \u2014 %s will not be available', {\n      error: reason,\n    });\n")
    return (o%(kind,ctx), n%(kind,ctx))
OPEN_PR="No open PR touches this file or its `src/__tests__/` neighbours of the same name (the 22 open PRs read 2026-11-02 through the GitHub API; 125 file entries; services/originate appears only as package.json in PRs 575/949/1726 and three integration-test files in PRs 1790/1792/1794; no entry under src/repositories/; planted positive control: the same scan finds services/auth in 11 file entries)."
def mkT(k,kind,ctx,lineno,word):
    return dict(dir='ks_1868_o65_%s_originate_%s_verify_db_ready_catch_unreadable_throw'%(k,kind.lower()), prod=SV+'src/repositories/%s.ts'%kind,
   edits=[edit(kind,ctx)], hunks='1', nh=1, lines=lineno,
   fn='the catch block of `verifyDbReady` in originate `repositories/%s.ts`'%kind, short='one log-then-throw-a-constant catch',
   test=TD+'ks1868-%s-verify-db-ready-%s-unreadable-throw.test.ts'%(kind.lower().replace('repo','-repo'),k), tsrc='t65_%s.ts.txt'%k,
   ncells='5 cells: 2 red (R1, R2) + 3 controls (C1 ordinary Error, C2 string, C3 healthy database)',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws) as the value the readiness query rejects with (2 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message and the constant Error is thrown), 'control ks1868 C2' (a thrown string is logged as itself and the constant Error is thrown) and 'control ks1868 C3' (a healthy database resolves and logs no error) (3 cells)",
   whatwrong=("In `repositories/%s.ts` the function `verifyDbReady` runs `SELECT 1` and, when it fails, its catch (line %s) logs `logger.error('%s: database connection FAILED ...', { error: err instanceof Error ? err.message : String(err) });` and THEN throws the constant `new Error('Database is required for %s operations')`. If the query rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the log line is written and before the constant Error, so the caller receives a TypeError (a different Error, with a different message) and nothing is logged. The fix keeps the log call's text and replaces only the value: it first reads the same expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `error: reason`. This is the inline guard already merged in originate `routes/certifications.ts` (a `let reason: string; try { ... } catch { reason = 'unreadable thrown value'; }`); no helper is added.")%(kind,lineno,kind,word),
   callers=("CALLERS (git grep at the tip, positive control: the same grep finds the definition and the tests): `src/index.ts` :411/:412 calls it with no argument inside `Promise.all([...]).then(...).catch((err) => logger.warn('Some database connections failed ...', { error: err?.message }))`; the catch only LOGS `err?.message` and the service keeps running in degraded mode. %s No other non-test caller. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the rejection that reaches that startup `.catch` goes from a TypeError (message e.g. `Cannot perform 'get' on a proxy that has been revoked`) to the constant Error `Database is required for %s operations`, which is exactly what an ordinary Error already produces; and the repository now writes its own `database connection FAILED` log line with `error: 'unreadable thrown value'` where today it writes none. Nothing else changes: no response, no persisted state, no verdict, the startup log is the only observer. Ordinary Errors and strings log and throw exactly as today (pinned by C1 and C2 and by the existing repository suite)."%(("`routes/certifications.ts` :70 calls `initRepo()` (which awaits this function) with a `.catch` that logs the message; the same reasoning applies." if kind=='certificationRepo' else "Its tests are `__tests__/documentRepo.test.ts` and ks597."),word)),
   dbnote="`../db` (a `prisma` stand-in and `withTenant`)%s and `../utils/logger` are replaced (`@secuura/shared` is NOT mocked: a hand-written factory for it is refused by the ks1061 completeness suite, and the real module loads); the readiness query's stand-in is passed as the `db` argument and is a plain jest function that rejects with the thrown value; no database is touched."%(""),
   red1="At the tip the catch throws a TypeError inside itself, so the constant Error never arrives (the outcome is read through a promise `.then(...)` and compared with the constant message) and nothing is logged",
   fix_nature="adds the inline `let reason` guard (originate certifications.ts shape)", pin_files="%s.ts"%kind)
T={'p1':mkT('p1','certificationRepo','certifications','58-61','certification'),'p2':mkT('p2','documentRepo','documents','138-141','document')}
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
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/originate_%s_and_src/__tests__/_are_in_no_open_PR_(22_PRs_125_files_read_2026-11-02_by_op65,_originate_only_as_package.json_and_3_integration_tests_in_575/949/1726/1790/1792/1794,_positive_control_services/originate_in_11_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['pin_files'],X['hunks'],REF,first,X['pin_files'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 originate: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunk(s) given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 65 for Wednesday, 2026-11-02. Secuura (originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file ({X['fix_nature']}; lines {X['lines']}). {OPEN_PR} Sibling files are separate briefs (O65-P1 certificationRepo.ts, O65-P2 documentRepo.ts); each pass is generated against the same tip and is disjoint from the other.

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
- The existing repository suites (`__tests__/certificationRepo.test.ts`, `__tests__/documentRepo.test.ts`) pin `verifyDbReady` throwing `Database is required` for an ordinary Error; they are read, not run by the operator; the harness control measures the whole-suite baseline in its own clone.

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
