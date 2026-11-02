# Operator 71: KS-1868 kyc/src/index.ts remaining catches (inline `let reason` guard merged at :191-:198 etc.). Vitest. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='b887480394cc67764922b0aa123027c344241ed7'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator71/gen/'
SV='Blockchain/Dev/services/kyc/'
PROD=SV+'src/index.ts'
TD=SV+'src/__tests__/'
REF=TD+'db.retry.test.ts'
def G(ind,expr):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
E1="err instanceof Error ? err.message : String(err)"
E2="err?.message"
def pair(ind,fn,ctx,expr):
    o=" "*ind+"logger.%s('%s', { error: %s });\n"%(fn,ctx,expr)
    n=G(ind,expr)+" "*ind+"logger.%s('%s', { error: reason });\n"%(fn,ctx)
    return (o,n)
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 22 open PRs read 2026-11-02 through the GitHub API; 124 file entries; services/kyc appears only as package.json in PRs 575/649 and package-lock.json in PR 1360; positive control services/originate present in 7 entries)."
COMMON=dict(prod=PROD,
   red1="At the tip the catch itself throws, so the expected log line is missing and the assertions fail")
T={
 'p1':dict(COMMON, dir='ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw',
   edits=[pair(4,'error','DB save image failed',E1)], hunks='1', nh=1, lines='353',
   fn='the `dbSaveImage` catch block of kyc `index.ts` (the attestation write)', short='one catch block',
   test=TD+'ks1868-kyc-save-image-attestation-unreadable-throw.test.ts', tsrc='t71_p1.ts.txt', ncells='3 cells: C1 (ordinary Error), R1, R2',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once each (2 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message, the upload is refused with the attestation failure and nothing is recorded) (1 cell)",
   dbnote="`../db` (an in-memory verification table; the `svc_kyc_images` INSERT rejects with the value the cell sets), `../subjectDeks`, `../utils/logger` and `@secuura/shared` (the real module, with the field-encryption and auth names replaced) are replaced; `express` listen is stubbed and the app is mounted on a real loopback listener. The image sniffing is real (a real 1x1 PNG is posted).",
   whatwrong="In `index.ts` the catch block of `dbSaveImage` (the KS-386 attestation write: it records that a verified image type was submitted, never the image bytes) logs `logger.error('DB save image failed', { error: err instanceof Error ? err.message : String(err) })` (line 353) and then THROWS the authored `new AppError('The verification attestation could not be recorded. No document was accepted.', 500, 'KYC_ATTESTATION_WRITE_FAILED')`. If the INSERT rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before the authored AppError is thrown, so the caller sees the raw TypeError instead. The fix keeps the log line's text and replaces only the value: it first reads the SAME expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `{ error: reason }`. The `throw new AppError(...)` that follows is untouched. This is the inline guard already merged in the same file at the five helpers above it (`dbSaveVerification`, `dbGetVerification`, `dbGetVerificationsByUser`, `dbGetVerificationStats`, `dbSaveConsent`, e.g. lines 191-198); no helper is added.",
   callers="CALLERS (git grep at the tip, kyc/src/index.ts): `dbSaveImage` is called at :868 (front image) and :873 (back image) in POST /api/kyc/:id/document and at :978 (selfie) in POST /api/kyc/:id/selfie. All three sit inside a route `try` whose `catch` first tests `instanceof z.ZodError` (a TypeError is not one) and then calls `next(error)` to the shared `errorHandler`. STRICT IDENTITY NOTE: this catch decides no verification outcome, no erasure, no retention action and returns no personal data; it logs a field-name-only line (the error text, no identity value) and rethrows a constant AppError. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, today the route receives a raw TypeError and the shared errorHandler answers whatever it answers a non-AppError (500, not the authored code; the exact body was not measured), and no log line is written; after, the constant reason is logged and the route answers the authored 500 `KYC_ATTESTATION_WRITE_FAILED`, exactly what an ordinary Error already gets (control C1). Persisted state is the same before and after and for an ordinary Error: the image attestation row is not written, and the document route aborts BEFORE `dbSaveVerification`, so no document is attached and the verification status stays as it was. No outbound call is made in or after the catch. Recommended tier 1 (KYC identity-document upload route).",
   fixnote="the five `let reason` guards already merged in this file (operator 47's KS-1868 batch), e.g. lines 191-198"),
 'p2':dict(COMMON, dir='ks_1868_o71_p2_kyc_verify_db_ready_boot_probe_catch_unreadable_throw',
   edits=[pair(4,'warn','KYC DB verification query failed',E2)], hunks='1', nh=1, lines='505',
   fn='the `verifyDbReady` catch block of kyc `index.ts` (the boot-time table probe)', short='one catch block',
   test=TD+'ks1868-kyc-verify-db-ready-boot-probe-unreadable-throw.test.ts', tsrc='t71_p2.ts.txt', ncells='3 cells: C1 (ordinary Error), R1, R2',
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once each (2 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` is logged with its own message and the boot probe ends without a rejection) (1 cell)",
   dbnote="`../db` (`initDb` resolves true and the `COUNT(*)` probe rejects with the value the cell sets), `../subjectDeks`, `../utils/logger` (its `warn` is captured) and `@secuura/shared` (the real module with `authenticate` replaced) are replaced; `express` listen is stubbed; the app module is imported fresh (`vi.resetModules()`) per cell and the cell waits up to two seconds for the probe to finish. No request is made.",
   whatwrong="In `index.ts` `verifyDbReady` (called once at boot from `initDb().then(async (connected) => { if (connected) await verifyDbReady(); })`, line 1281) runs `SELECT COUNT(*) AS cnt FROM svc_kyc_verifications` and, in its catch, logs `logger.warn('KYC DB verification query failed', { error: err?.message })` (line 505) and returns nothing. If the query rejects with a revoked Proxy, `err?.message` itself throws a TypeError inside the catch block (property reads on a revoked Proxy throw); if it rejects with an Error whose `message` getter throws, `err?.message` throws. Either way the catch throws before the line is logged, `verifyDbReady` rejects, and the boot callback's promise has no handler (an unhandled rejection, process-fatal on Node >= 15). The fix keeps the log line's text and replaces only the value: it first reads the SAME expression `err?.message` into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log line then uses `{ error: reason }`. This is the inline guard already merged in the same file (lines 191-198 etc.); no helper is added.",
   callers="CALLERS (git grep at the tip, kyc/src/index.ts): `verifyDbReady` has exactly one caller, :1281, in the boot callback `initDb().then(...)` with no `.catch`. STRICT IDENTITY NOTE: this is a boot-time table-count probe. The catch is log-only (it does not return or respond), it runs before the service takes traffic from the probe's point of view, it decides no verification outcome, no erasure, no retention action and returns no personal data, and the logged value is the error text, never an identity value. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, today the catch throws, nothing is logged and the boot callback rejects with no handler (unhandled rejection; process-fatal on Node >= 15); after, the constant reason is logged at warn level and boot continues, exactly what an ordinary Error already gets (control C1). Persisted state: none, before or after (a COUNT query). No response or outbound call is involved. Recommended tier 1 (KYC service boot path; hold for Kam's call because the catch has no HTTP response).",
   fixnote="the five `let reason` guards already merged in this file (operator 47's KS-1868 batch), e.g. lines 191-198"),
}
def build(k):
    X=T[k]
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
    pins=("# code_patch2: kyc index.ts (%s hunk) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/kyc_index.ts_and_src/__tests__/_are_in_no_open_PR_(22_PRs_124_files_read_2026-11-02_by_op71,_kyc_only_as_package.json_in_575/649_and_package-lock.json_in_1360,_positive_control_services/originate_in_7_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['hunks'],REF,first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 kyc: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 71 for Wednesday, 2026-11-02. Secuura (kyc) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (line {X['lines']}), reusing {X['fixnote']}. {OPEN_PR} Other KS-1868 files and the other kyc sites are separate briefs or deliberately skipped.

File: `{PROD}`  (product, modified in place: EXACTLY {X['hunks']} hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/kyc`)
Tier: `code_patch2`
Rung: **3 ({X['hunks']} product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the {X['hunks']} hunk under "The exact change", byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{X['whatwrong']}

## Where

`{PROD}`: line {X['lines']}. {X['callers']}

## The exact change

EXACTLY {X['hunks']} hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text. The log message text is unchanged.

**Do NOT touch** any other catch block of the file, any message text, or any other line.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from the merged sibling suites of this directory (`ks1868-kyc-save-consent-unreadable-throw.test.ts`, `ks1845-kyc-review-requires-a-platform-reviewer.test.ts`; pinned ref `{REF}`). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells
{X['redlines']}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {X['red1']}; after the edit the constant reason is logged.
- GREEN at the tip and after: {X['greens']}.
- The stand-ins rejecting with the thrown value are plain functions, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` line {X['lines']} is the unguarded read at the tip (read whole with `git show` at `{TIP[:12]}`, which is where the kyc file is identical to origin develop `93e5c6699d1c` by `git diff --stat` over services/kyc, empty).
- Open PRs: 22 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (124 file entries; services/kyc only as package.json in PRs 575/649 and package-lock.json in 1360); the positive control services/originate appears in 7 file entries.
- No test or script reads this log line's text as source (`git grep` for the message text over Blockchain/Dev at origin develop: one hit, the line itself).

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other kyc sites (the decrypt catches, the PII init and subscriber-start catches, the Zod-preceded route catches) were not touched. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot with a real Postgres and a real Express 4 were not run.

## Scope

**This site only.** Refs KS-1868; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
