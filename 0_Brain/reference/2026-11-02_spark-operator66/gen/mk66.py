# Operator 66: KS-1868 originate systemErrors.ts (P1, reuse in-file fail500) and errorTrackingService.ts trackError (P2, inline guard). Jest. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator66/gen/'
SV='Blockchain/Dev/services/originate/'
TD=SV+'src/__tests__/'
REF=TD+'ks1133-v2-verify-hash-read-first.test.ts'
def G(ind,msg,var):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%var+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
E="error instanceof Error ? error.message : String(error)"
O1="      logger.error('v2 verification error', { error: %s });\n"%E
N1=G(6,'','error instanceof Error ? error.message : String(error)')+"      logger.error('v2 verification error', { error: reason });\n"
O2="    logger.error('v2 file verification error', { error: %s });\n"%E
N2=G(4,'','error instanceof Error ? error.message : String(error)')+"    logger.error('v2 file verification error', { error: reason });\n"
OPEN_PR="No open PR touches this file or its `src/__tests__/` neighbours (the 22 open PRs read 2026-11-02 through the GitHub API; 125 file entries; services/originate appears only as package.json and integration tests in PRs 575/949/1726/1790/1792/1794; positive control services/originate present)."
T={
 'p1':dict(dir='ks_1868_o66_p1_originate_verification_v2_verify_verify_file_catches_unreadable_throw', prod=SV+'src/routes/verificationV2.ts',
   edits=[(O1,N1),(O2,N2)], hunks='2', nh=2, lines='441 and 477',
   fn='the two route catch blocks of originate `routes/verificationV2.ts` (POST /verify and POST /verify-file)', short='two route catch blocks',
   test=TD+'ks1868-verification-v2-route-catches-p1-unreadable-throw.test.ts', tsrc='t66_p1.ts.txt', ncells='8 cells: 2 routes x (R1, R2, C1, C2)',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route (4 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message and the answer is the constant 500) and 'control ks1868 C2' (a thrown string is logged as itself), once per route (4 cells)",
   whatwrong="In `routes/verificationV2.ts` the catch blocks of POST /verify (line 440) and POST /verify-file (line 476) each log `logger.error('<context>', { error: error instanceof Error ? error.message : String(error) })` (lines 441 and 477) and then answer the constant 500 `Verification failed` / `File verification failed`. If the database call rejects with a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch; if it rejects with an Error whose `message` getter throws, `error.message` throws. Either way the catch throws, nothing is logged and the request gets no answer. The fix keeps each log line's text and replaces only the value: it first reads the same expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `{ error: reason }`. The constant 500 answers are untouched. This is the inline guard already merged in originate `routes/certifications.ts` (`let reason: string; try { ... } catch { reason = 'unreadable thrown value'; }`); this file has no helper and none is added.",
   callers="CALLERS (git grep at the tip): both routes are public verification endpoints mounted by `src/index.ts` as `verificationV2Router` under `/api/v2/verification` and reached by the api-gateway and external verifiers over HTTP. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value from the database only, today the request gets no answer (the handler rejects; the gateway times out); after, the constant reason is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status or log for an ordinary Error or a string changes. Persisted state: none (read-only routes).",
   dbnote="`../db` (a `prisma` whose `$queryRaw` is a jest stand-in that rejects with the thrown value; `getTenantManager` returns null so the cross-tenant lookup is skipped), `../middleware/auth` (pass-through), `@secuura/shared` (the existing helper `./helpers/sharedModuleMock`), `../repositories/documentRepo` and `../utils/logger` are replaced; the router is mounted on a real loopback listener under `/api/v2/verification`.",
   red1="At the tip the handler rejects instead of answering, so the request reports `NO ANSWER` after 1.5 seconds and the assertion fails",
   fix_nature="adds the inline `let reason` guard (originate certifications.ts shape)", pin_files="verificationV2.ts"),
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
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/originate_%s_and_src/__tests__/_are_in_no_open_PR_(22_PRs_125_files_read_2026-11-02_by_op66,_originate_only_as_package.json_and_3_integration_tests_in_575/949/1726/1790/1792/1794,_positive_control_services/originate_in_11_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['pin_files'],X['hunks'],REF,first,X['pin_files'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 originate: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunk(s) given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 66 for Wednesday, 2026-11-02. Secuura (originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file ({X['fix_nature']}; lines {X['lines']}). {OPEN_PR} Other KS-1868 files are separate briefs.

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
- The existing suites that mount this router (`ks1133-v2-verify-hash-read-first`, `ks1129-heal-persists-a-number`, `ks1634-v2-chain-only-match-carries-simulated`) use the same mocks (`../db`, `../middleware/auth`, `@secuura/shared` via `./helpers/sharedModuleMock`, `../repositories/documentRepo`); their pass state was not measured separately by this brief.

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
