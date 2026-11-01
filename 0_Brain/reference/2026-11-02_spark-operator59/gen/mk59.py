# Operator 59: KS-1868 nft-certificate ipfs.service.ts fetch() two catches (code_patch2, O51/O57 shape)
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator59/gen/'
SV='Blockchain/Dev/services/nft-certificate/'
PROD=SV+'src/services/ipfs.service.ts'
TD=SV+'src/__tests__/'
REF=TD+'ks1836-nft-read-gate.test.ts'
def guard(ind):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = error instanceof Error ? error.message : String(error);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
OLD_A="      logger.warn('IPFS gateway unreachable', {\n        cid,\n        error: error instanceof Error ? error.message : String(error),\n      });\n"
NEW_A=guard(6)+"      logger.warn('IPFS gateway unreachable', {\n        cid,\n        error: reason,\n      });\n"
OLD_B="      logger.warn('IPFS gateway body read failed', {\n        cid,\n        error: error instanceof Error ? error.message : String(error),\n      });\n"
NEW_B=guard(6)+"      logger.warn('IPFS gateway body read failed', {\n        cid,\n        error: reason,\n      });\n"
X=dict(dir='ks_1868_o59_p1_nftcertificate_ipfs_fetch_unreadable_throw', edits=[(OLD_A,NEW_A),(OLD_B,NEW_B)],
  test=TD+'ks1868-ipfs-fetch-unreadable-throw.test.ts', tsrc='t59_p1.ts.txt')
OPEN_PR="No open PR touches this file: the 20 open PRs read 2026-11-02 through the GitHub API (113 file entries) were scanned for `ipfs.service.ts`, `blockchain-verifier.service.ts` and `minting.service.ts`; only PR 1909 lists minting.service.ts (Seat E 26th; a different file, left alone) and none lists ipfs.service.ts; planted positive control: the same scan finds services/nft-certificate in 5 file entries."
WHATWRONG=("In `ipfs.service.ts` the method `IPFSService.fetch` (used when the provider has no native `read`, i.e. every HTTP-gateway provider) has two catch blocks that each map a failure to `throw new ServiceUnavailableError('IPFS gateway')` after a `logger.warn`: (1) line 487, the gateway request `response = await fetch(url, ...)`, logs `'IPFS gateway unreachable'`; (2) line 512, the body read `await response.arrayBuffer()`, logs `'IPFS gateway body read failed'`. Both log `error: error instanceof Error ? error.message : String(error)`. If the awaited call rejects with a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `error.message` throws. Either way the catch throws before the warning is logged and before the `ServiceUnavailableError`, so `fetch` rejects with the TypeError instead of the 503 error. The fix adds, before each `logger.warn`, a `let reason: string;` plus a `try` that runs the SAME expression and a `catch` that sets the constant `'unreadable thrown value'`, and the log call uses `error: reason`; the `throw new ServiceUnavailableError('IPFS gateway')` is then reached as for any ordinary failure. An ordinary Error still logs `error: <its message>`.")
CALLERS=("CALLERS (git grep at the tip): `IPFSService.fetch` is called by `fetchEncrypted` (same file) and directly by routes/nft.routes.ts `GET /api/nft/ipfs/:cid` (:584) and, through `fetchEncrypted`, `GET /api/nft/ipfs/:cid/encrypted` (:609); both routes `catch (error) { next(error); }` into the shared `errorHandler`, which answers `err.statusCode || 500` with the code `err.code || SERVER_INTERNAL` and a redacted message for any 5xx. Nothing in nft-certificate src outside those two routes calls `fetch`; minting.service.ts uses only `uploadEncrypted`. These are READ routes: no mint, no chain write, no verification verdict and no persisted state is involved. **BEHAVIOUR CHANGE the raise PR must state:** when the gateway request or body read rejects with an unreadable value, those two GET routes today answer 500 (INTERNAL) because the TypeError has no statusCode; after, they log the constant reason and answer 503 SERVICE_UNAVAILABLE, exactly what every ordinary gateway failure already answers (an ordinary Error already gets the after-state).")
def build():
    old=mk.rd(PROD); new=old
    for o,n in X['edits']:
        assert new.count(o)==1,(o[:70],new.count(o))
        new=new.replace(o,n)
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    hl=[l for l in pd.splitlines() if l.startswith('@@ ')]
    assert len(hl)==2,hl
    tbody=open(GEN+X['tsrc'],encoding='utf-8').read()
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(pd+td)
    first=0;cur=None
    for l in pd.splitlines():
        if l.startswith('@@ '):
            cur=int(l.split()[1].split(',')[0][1:]); continue
        if cur is None: continue
        if l.startswith('-') and not l.startswith('---'): first=cur; break
        if l.startswith(' '): cur+=1
    assert first
    pins=("# code_patch2: nft-certificate ipfs.service.ts (2 hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_ipfs.service.ts_is_in_no_open_PR_(20_PRs_113_files_read_2026-11-02_by_op59,_positive_control_services/nft-certificate_in_5_entries);_live_lanes_beyond_PRs_not_checked\n")%(REF,first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 nft-certificate: `IPFSService.fetch` must still answer 503 and log when the thrown value cannot be read (RUNG 3, code_patch2: 2 product hunks given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 59 for Wednesday, 2026-11-02. Secuura (nft-certificate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes the two log-only catch reads of `IPFSService.fetch` in ONE file, inline, with no shared helper (lines 487 and 512). {OPEN_PR} Other sites of the service are not in this brief.

File: `{PROD}`  (product, modified in place: EXACTLY 2 hunks)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; 6 cells: 2 sites x (R, R) = 4 red, plus 2 controls)
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/nft-certificate`)
Tier: `code_patch2`
Rung: **3 (2 product hunks, skeletons dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the 2 hunks under "The exact change", in that order, byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{WHATWRONG}

## Where

`{PROD}`: lines 487 and 512. {CALLERS}

## The exact change

EXACTLY 2 hunks in the product file, in this order. The file header lines and every `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The log message text (the string literal before `, `) is unchanged. **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (a vitest file that replaces the logger and imports the real service). `../utils/logger` is replaced; the real `IPFSService` runs with the `pinata` provider and a gateway URL; the global `fetch` is stubbed with a plain function per cell, and the answer is read as `statusCode` and `code` (the shared error class may resolve to another module copy, so `instanceof` is not used); no network. The test file contains backslashes, quotes and template strings: keep every character, including every backslash, exactly as given.

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2
- RED ks1868 R3
- RED ks1868 R4

## Cells and controls

- RED at the tip, GREEN after: `R1` and `R2` (request site: revoked Proxy, Error whose `message` getter throws) and `R3` and `R4` (body-read site: the same two values). At the tip the catch throws a TypeError, so the call rejects without a statusCode and the answer assertion fails; after the edit it rejects with the 503 SERVICE_UNAVAILABLE error and the warning carries the constant `unreadable thrown value`.
- GREEN at the tip and after: 'control ks1868 C1 request' and 'control ks1868 C2 body' (ordinary Errors: each is logged with its own message and the call answers 503), the controls showing the rig works and the normal path is unchanged.
- The stand-ins rejecting with the thrown value are plain functions, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` lines 487 and 512 are the `instanceof Error` reads at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 20 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` (113 file entries); the positive control services/nft-certificate appears in 5 file entries (PR 1909 minting.service.ts included).
- The pinned ref `ks1836-nft-read-gate.test.ts` runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the service were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). A real gateway, the Express routes and the shared errorHandler were not run.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
build()
