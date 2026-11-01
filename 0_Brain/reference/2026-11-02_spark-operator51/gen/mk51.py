# Operator 51: KS-1868 services/nft-certificate/src/services/minting.service.ts (:177 getCertificationData, :688 getWalletNFTCertificates)
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='8afcf256ed5fb38d05f7273e08e1b912446bac5c'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator51/gen/'
SV='Blockchain/Dev/services/nft-certificate/'
PROD=SV+'src/services/minting.service.ts'
TD=SV+'src/__tests__/'
def edit1(t,old,new):
    assert t.count(old)==1, old
    return t.replace(old,new)
def safe(ind, fn_old_lines):
    pass
P1_OLD=("      logger.error('Error fetching certification data from originate service', {\n        certificationId,\n"
        "        error: err instanceof Error ? err.message : String(err),\n      });\n")
P1_NEW=("      let reason: string;\n      try {\n        reason = err instanceof Error ? err.message : String(err);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n"
        "      logger.error('Error fetching certification data from originate service', {\n        certificationId,\n        error: reason,\n      });\n")
P2_OLD="        logger.error('DB get wallet certificates failed', { error: err instanceof Error ? err.message : String(err) });\n"
P2_NEW=("        let reason: string;\n        try {\n          reason = err instanceof Error ? err.message : String(err);\n        } catch {\n          reason = 'unreadable thrown value';\n        }\n"
        "        logger.error('DB get wallet certificates failed', { error: reason });\n")
def p1(t): return edit1(t,P1_OLD,P1_NEW)
def p2(t): return edit1(t,P2_OLD,P2_NEW)
COMMON_PR=("No open PR touches this file: the 22 open PRs read 2026-11-02 through the GitHub API (124 file entries) were scanned for `nft-certificate/src/services/minting.service.ts` and none lists it (PR 1900 is the kyc DB helpers); planted positive control: the same scan finds services/nft-certificate in 2 file entries.")
REF=TD+'ks1836-nft-read-gate.test.ts'
T={}
T['p1']=dict(dir='ks_1868_o51_p1_nftcertificate_get_certification_data_unreadable_throw', fix=p1, line=177, tag='O51-P1',
  test=TD+'ks1868-nft-get-certification-data-unreadable-throw.test.ts', tsrc='t51_p1.ts.txt', ref=REF,
  title="`getCertificationData` must still log and return null when the originate-service fetch throws a value that cannot be read",
  site="the production-branch catch block of the module function `getCertificationData`",
  quote="`error: err instanceof Error ? err.message : String(err),`",
  whatwrong="In production `getCertificationData` fetches the certification from the originate service inside a `try`; its catch block logs `logger.error('Error fetching certification data from originate service', { certificationId, error: err instanceof Error ? err.message : String(err) })` (the read is on line 177) and then `return null`. If the fetch rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before `return null`, so the function rejects with the TypeError. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `error: reason`; the `return null` is then reached as for any ordinary fetch failure. An ordinary Error still logs `error: <its message>`.",
  callers="CALLERS (git grep at the tip): only `NFTMintingService.mintNFT` (:249), `const certification = await getCertificationData(request.certificationId); if (!certification) { throw new Error('Certification not found'); }`, all inside the big `try` of `mintNFT` whose catch calls `classifyMintError(error)` and returns `{ success:false, error: message, errorCode }`; POST /api/nft/mint (routes/nft.routes.ts:85-110) answers that message in the body with `mintFailureHttpStatus(errorCode)`. The read itself only feeds the log line (never a response). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable fetch rejection in production, `mintNFT` today resolves `{ success:false, errorCode:'MINT_FAILED' }` carrying the TypeError's text (a revoked Proxy gives a TypeError that says it cannot perform getPrototypeOf on a revoked proxy; a throwing getter gives the getter's text) and the route answers 400 with that text; after the fix it resolves `{ success:false, error:'Certification not found', errorCode:'CERTIFICATION_NOT_FOUND' }` and the route answers 404, exactly as it already does for every ordinary fetch failure (the fetch-failure-reported-as-not-found conflation is existing behaviour and out of scope). The FAILED record's errorMessage changes the same way. The other branch (non-production, :186) swallows with a bare `catch {}` and is not touched.",
  harness="`../db` (isDbAvailable false, so nothing is saved), `../cardano` and `../utils/logger` are replaced; `fetch` is stubbed with a plain function and `process.env.NODE_ENV` is set to `production` for the test and restored; the real minting service runs through `mintNFT`; no database, no network.",
  red1="At the tip the catch throws, so `mintNFT` resolves `errorCode` `MINT_FAILED` (not `CERTIFICATION_NOT_FOUND`) and no `Error fetching certification data ...` line is logged")
T['p2']=dict(dir='ks_1868_o51_p2_nftcertificate_get_wallet_nft_certificates_unreadable_throw', fix=p2, line=688, tag='O51-P2',
  test=TD+'ks1868-nft-get-wallet-nft-certificates-unreadable-throw.test.ts', tsrc='t51_p2.ts.txt', ref=REF,
  title="`getWalletNFTCertificates` must still report when the thrown value cannot be read",
  site="the catch block of `getWalletNFTCertificates`",
  quote="`logger.error('DB get wallet certificates failed', { error: err instanceof Error ? err.message : String(err) });`",
  whatwrong="In `minting.service.ts` the catch block of `getWalletNFTCertificates` logs `logger.error('DB get wallet certificates failed', { error: err instanceof Error ? err.message : String(err) })` (the read is on line 688) and then falls through to the sorted `certificates` return. If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before the normal return, so the function rejects. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }`.",
  callers="CALLERS (git grep at the tip): routes/nft.routes.ts:241 (GET /certificates, the `walletAddress` branch), inside a try whose catch answers 500 with the constant message 'Failed to fetch NFT certificates' (its own log read at :~262 is on the TypeError, an ordinary Error). The message is only logged. **BEHAVIOUR CHANGE the raise PR must state:** when the DB query rejects with an unreadable value, GET /api/nft/certificates?walletAddress=... today answers 500 (the call rejects); after the fix it logs the constant reason and returns the in-memory matches (often an empty list) with 200, then `selectReadableCertificates` filters as usual; this is exactly what an ordinary DB error already does, so an unreadable DB failure now reads to the client as an empty/partial list rather than an error (the read-gate and owner binding of KS-1836 are unchanged).",
  harness="`../db`, `../cardano` and `../utils/logger` are replaced; the real minting service runs; no database, no app boot and no network.",
  red1="At the tip the call rejects, so no `DB get wallet certificates failed` line is logged and the `resolves` assertion fails")
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
    pins=("# code_patch2: nft-certificate minting.service.ts (1 hunk) + a NEW test file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_minting.service.ts_is_in_no_open_PR_(22_PRs_124_files_read_2026-11-02_by_op51,_positive_control_services/nft-certificate_in_2_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['ref'],X['line'])
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 nft-certificate: {X['title']} (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 50 for Wednesday, 2026-11-02. Secuura (nft-certificate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {X['site']} in `services/nft-certificate/src/services/minting.service.ts`. {COMMON_PR} This pass is one of two sequenced in old-line order in this one file (getCertificationData :177, getWalletNFTCertificates :688); each is generated against the same tip and is disjoint from the other. The sites are the log-only unguarded reads Seat R 72nd left after PR 1899 (and gate 84's list). The third candidate, `mintOnCardano` :798, is deliberately not in this series (it rethrows into the unguarded `classifyMintError`).

File: `{PROD}`  (product, modified in place: ONE hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; 4 cells (2 red, 2 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/nft-certificate`)
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

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. In particular do NOT touch the other unguarded read of this series, the `Real minting failed` catch in `mintOnCardano` (:798), or `classifyMintError` (a different file), and leave the four catch blocks that already carry the inner `try` (:92, :137, :518, :604) alone.

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
- Open PRs: 22 (124 file entries) read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}`; the positive control services/nft-certificate appears in 2 file entries.
- The pinned ref runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the 253 were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path, a real Redis and a real Postgres were not run. The three sequenced passes were not run together by the pipeline.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
