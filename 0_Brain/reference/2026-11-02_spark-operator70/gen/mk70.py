# Operator 70: KS-1868 originate routes/verification.ts route catches (inline `let reason` guard merged in certifications.ts:1086). Jest. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='b887480394cc67764922b0aa123027c344241ed7'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator70/gen/'
SV='Blockchain/Dev/services/originate/'
TD=SV+'src/__tests__/'
REF=TD+'ks1133-v2-verify-hash-read-first.test.ts'
def G(ind,var):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%var+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
E="error instanceof Error ? error.message : String(error)"
def pair(ind,ctx):
    o=" "*ind+"logger.error('%s', { error: %s });\n"%(ctx,E)
    n=G(ind,E)+" "*ind+"logger.error('%s', { error: reason });\n"%ctx
    return (o,n)
OPEN_PR="No open PR touches this file or its `src/__tests__/` neighbours (the 22 open PRs read 2026-11-02 through the GitHub API; 127 file entries; services/originate appears only as package.json in PRs 575/949/1726 and integration tests in PRs 1790/1792/1794; positive control services/auth present in 7 entries)."
COMMON=dict(
   prod=SV+'src/routes/verification.ts',
   dbnote="`../db`, `../middleware/auth`, `@secuura/shared` (the existing helper `./helpers/sharedModuleMock`), `../repositories/documentRepo` and `../utils/logger` are replaced exactly as in the sibling verification suites; the router is mounted on a real loopback listener under `/api/verification`, behind a one-shot hook that makes the handler throw the chosen value from inside its own try.",
   red1="At the tip the handler rejects instead of answering, so the request reports `NO ANSWER` after 1.5 seconds and the assertion fails",
   fix_nature="adds the inline `let reason` guard already merged in `routes/certifications.ts` (GET /:id catch, lines 1086-1094) and used by the verificationV2 patch; no helper", pin_files="verification.ts")
T={
 'p1':dict(COMMON, dir='ks_1868_o70_p1_originate_verification_verify_hash_status_route_catches_unreadable_throw',
   edits=[pair(6,'Verification error'),pair(6,'Hash generation error'),pair(6,'Status check error')], hunks='3', nh=3, lines='1438, 1467 and 1489',
   fn='the verify, hash and status route catch blocks of originate `routes/verification.ts` (POST /verify, POST /hash, GET /status/:documentId)', short='three route catch blocks',
   test=TD+'ks1868-verification-verify-hash-status-route-catches-p1-unreadable-throw.test.ts', tsrc='t70_p1.ts.txt', ncells='12 cells: 3 routes x (R1, R2, C1, C2)',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route (6 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message and the answer is the constant 500) and 'control ks1868 C2' (a thrown string is logged as itself), once per route (6 cells)",
   whatwrong="In `routes/verification.ts` the outer catch blocks of POST /verify (line 1437), POST /hash (line 1466) and GET /status/:documentId (line 1488) each log `logger.error('<context>', { error: error instanceof Error ? error.message : String(error) })` (lines 1438, 1467, 1489) and then answer the constant 500 (`Verification failed`, `Hash generation failed`, `Status check failed`). If a call in the try throws a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch; if it throws an Error whose `message` getter throws, `error.message` throws. Either way the catch throws, nothing is logged and the request gets no answer. The fix keeps each log line's text and replaces only the value: it first reads the same expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `{ error: reason }`. The constant 500 answers are untouched. This is the inline guard already merged in `routes/certifications.ts` (GET /:id catch, lines 1086-1094: `let reason: string; try { ... } catch { reason = 'unreadable thrown value'; }`); no helper is added.",
   callers='CALLERS: `verificationRouter` is mounted by `src/index.ts` (line 279) under `/api/verification` and reached through the api-gateway; these are public verification endpoints. STRICT NOTE: each catch only logs and answers the constant 500 `{ success: false, error: { code: \'INTERNAL_ERROR\', message } }`, which carries no `verified` or verdict field; nothing before the logger in any of the three catches decides an outcome, and the catches write nothing (the three routes persist nothing). The lineage-attach catches, the empty-lineage fallbacks and the inner dbErr catch of POST /verify are NOT touched. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, today the request gets no answer (the handler rejects; the gateway times out); after, the constant reason is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status, body, verdict or log for an ordinary Error or a string changes. Persisted state: none, before or after. Recommended tier 1 (public verification route file).'),
 'p2':dict(COMMON, dir='ks_1868_o70_p2_originate_verification_verify_file_route_catch_unreadable_throw',
   edits=[pair(4,'File verification error')], hunks='1', nh=1, lines='759',
   fn='the verify-file route catch block of originate `routes/verification.ts` (POST /verify-file)', short='one route catch block',
   test=TD+'ks1868-verification-verify-file-route-catch-p2-unreadable-throw.test.ts', tsrc='t70_p2.ts.txt', ncells='4 cells: 1 route x (R1, R2, C1, C2)',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once (2 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message and the answer is the constant 500) and 'control ks1868 C2' (a thrown string is logged as itself), once (2 cells)",
   whatwrong="In `routes/verification.ts` the outer catch block of POST /verify-file (line 758) logs `logger.error('File verification error', { error: error instanceof Error ? error.message : String(error) })` (line 759) and then answers the constant 500 `File verification failed`. If a call in the try throws a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch; if it throws an Error whose `message` getter throws, `error.message` throws. Either way the catch throws, nothing is logged and the request gets no answer. The fix keeps the log line's text and replaces only the value: it first reads the same expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `{ error: reason }`. The constant 500 answer is untouched. This is the inline guard already merged in `routes/certifications.ts` (GET /:id catch, lines 1086-1094); no helper is added.",
   callers='CALLERS: `verificationRouter` is mounted by `src/index.ts` (line 279) under `/api/verification` and reached through the api-gateway (`/api/verification/verify-file` is a public raw-bytes endpoint). STRICT NOTE: this is the file-verification route, but its catch only logs and answers the constant 500 `{ success: false, error: { code: \'INTERNAL_ERROR\', message: \'File verification failed\' } }`, which carries no `verified` field; nothing before the logger in the catch decides an outcome and the catch writes nothing. Any registry write or verdict happens (or not) in the try, before the catch, exactly as today for any thrown value. The inner chain-first catch (line 699, `chainErr?.message`) and the lineage code are NOT touched. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, today the request gets no answer (the handler rejects; the gateway times out); after, the constant reason is logged and the constant 500 is answered, exactly what an ordinary Error already gets. No response, status, body, verdict or log for an ordinary Error or a string changes. Persisted state: unchanged by this patch. Recommended tier 1 (public file-verification route).'),
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
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/originate_%s_and_src/__tests__/_are_in_no_open_PR_(22_PRs_125_files_read_2026-11-02_by_op70,_originate_only_as_package.json_and_3_integration_tests_in_575/949/1726/1790/1792/1794,_positive_control_services/auth_in_7_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['pin_files'],X['hunks'],REF,first,X['pin_files'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 originate: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunk(s) given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 69 for Wednesday, 2026-11-02. Secuura (originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file ({X['fix_nature']}; lines {X['lines']}). {OPEN_PR} Other KS-1868 files are separate briefs.

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

- `{PROD}` lines {X['lines']} are the `instanceof Error` reads at the tip (read whole with `git show` at `{TIP[:12]}`, which is origin develop by ls-remote at the start of operator 70's session; the round's drift check covers the files).
- Open PRs: 22 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` (127 file entries; services/originate only as package.json in PRs 575/949/1726 and integration tests in 1790/1792/1794); the positive control services/auth appears in 7 file entries.
- The existing suites that mount this router (`ks1103-verify-hash-field`, `ks1118-verify-documenthash-over-hash`) use the same module mocks as the new test (shape from ks1133); their pass state was not measured separately by this brief.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file (lineage catches, empty-lineage fallbacks, `?.message` warn sites) were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). A real Express listener is used; a real Postgres is not, and the throw is injected by a request-side hook (an accessor on `req.db`, or a one-shot throwing `res.json`), not by a real failing call.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
