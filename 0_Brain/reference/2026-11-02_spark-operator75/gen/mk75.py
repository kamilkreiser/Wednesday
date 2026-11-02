# Operator 75: KS-1868 governance remaining catches (jest) + auth routes. Reuses spark/gen/mk.py (rd, udiff). Template text from operators 44 and 71.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='92a26320e30ad680459cdb96c5b68b91a5f175a5'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator75/gen/'
SV='Blockchain/Dev/services/'
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 23 open PRs read 2026-11-02 through the GitHub API; 141 file entries; planted control services/auth/ present in 7 entries)."
def G(ind,expr):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
E1="err instanceof Error ? err.message : String(err)"
def pair(ind,fn,ctx,extra='',expr=E1):
    o=" "*ind+"logger.%s('%s', { %serror: %s });\n"%(fn,ctx,extra,expr)
    n=G(ind,expr)+" "*ind+"logger.%s('%s', { %serror: reason });\n"%(fn,ctx,extra)
    return (o,n)
E1="err instanceof Error ? err.message : String(err)"
OS=SV+'originate/'
OPROD=OS+'src/routes/anchors.ts'
OREF=OS+'src/__tests__/ks1657-an-anchor-read-fault-is-not-a-404.test.ts'
def pairx(ind, head, tail, expr, var):
    # head/tail: text before/after the object value; expression read once into reason
    pass
T={}
o50=("    logger.error('anchors: database connection FAILED — anchor operations will not be available', {\n      error: err instanceof Error ? err.message : String(err),\n    });\n")
n50=G(4,E1)+("    logger.error('anchors: database connection FAILED — anchor operations will not be available', {\n      error: reason,\n    });\n")
o90=("    logger.warn('Failed to fetch anchor from DB', { documentId, error: err instanceof Error ? err.message : String(err) });\n")
n90=G(4,E1)+("    logger.warn('Failed to fetch anchor from DB', { documentId, error: reason });\n")
E2="error instanceof Error ? error.message : String(error)"
o202=("      logger.error('Failed to get anchor', { error: error instanceof Error ? error.message : String(error) });\n")
n202=G(6,E2)+("      logger.error('Failed to get anchor', { error: reason });\n")
T['p1']=dict(dir='ks_1868_o75_p1_originate_anchors_db_ready_and_get_catches_unreadable_throw', prod=OPROD, ref=OREF, runner='jest', runcmd='', rdir=OS[:-1],
  edits=[(o50,n50),(o90,n90),(o202,n202)],
  nh=3, lines='50, 90 and 202', test=OS+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts', tsrc='t75_p1.ts.txt',
  fn='the `verifyAnchorsDbReady` catch and the `GET /api/anchors/:documentId` lookup and route catches', short='three catch blocks',
  whatwrong="In `routes/anchors.ts` three catch blocks read the rejection value with `X instanceof Error ? X.message : String(X)` before logging: `verifyAnchorsDbReady` (line 50: it logs `anchors: database connection FAILED ...` and then throws the constant `Error('Database is required for anchor operations')`), the DB helper `getAnchorByDocumentId` (line 90: it logs the warn `Failed to fetch anchor from DB` and then RETHROWS the caught value `throw err`, KS-1657) and the route catch of `GET /api/anchors/:documentId` (line 202: it logs `Failed to get anchor` and answers the constant 500 INTERNAL_ERROR). If the value is a revoked Proxy, `X instanceof Error` itself throws a TypeError inside the catch block; if it is an Error whose `message` getter throws, `X.message` throws. At the tip that means: at line 50 `verifyAnchorsDbReady` rejects with a TypeError instead of its constant error and no ERROR line is logged; at line 90 the warn is not logged and a TypeError (readable) replaces the thrown value, so the route still answers its constant 500 but only the route's error line is logged. **The three blocks MUST be fixed together:** if line 90 alone were fixed it would rethrow the unreadable value to the route catch at line 202, which would then throw inside the async handler (no response). The fix reads the SAME expression into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; each log call then uses `reason`. This is the inline guard already merged in the same service at `routes/certifications.ts` (KS-1844, line 1086-1094) and in `services/auth` `routes/auth.ts` (PR 1911, lines 308-313); no helper is added. The `throw err` at line 90 and the constant error at line 52 are untouched.",
  callers="CALLERS (git grep at the tip): `verifyAnchorsDbReady` is one of the four readiness checks in `Promise.all([...])` at `index.ts` line 414 (boot); `getAnchorByDocumentId` is called by the GET route (line 160 region) and nowhere in a write path (the file writes nothing to anchor_store, KS-1384 F-a; the cells assert `$executeRaw` is never called). WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the log lines with the error's message and, on the GET route, the constant 500 INTERNAL_ERROR (KS-1657: a failed read is not a 404); `verifyAnchorsDbReady` rejects with the constant Error. After the fix an unreadable thrown value gets exactly that, with the constant reason in the log lines; the cells assert the status, the body code and the thrown message. Today the GET route answers the same 500 (the TypeError that replaces the value is readable) but the warn line is missing, and `verifyAnchorsDbReady` rejects with a TypeError. Nothing here submits, signs or writes an anchor: no anchor-service call, no status write, no retry. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the two helper catches and the GET route catch log a constant reason, the GET route still answers its constant 500 and `verifyAnchorsDbReady` rejects with its constant Error (instead of a TypeError). Persisted state: none. Recommended tier 1 (anchor read route and boot check; anchoring is evidence-adjacent, Kam's tier-1-with-Opus-gate ruling).",
  ncells='6 cells: C1 and C2 (ordinary Error on the GET route and on verifyAnchorsDbReady), R1 to R4',
  red1="At the tip the warn line `Failed to fetch anchor from DB` is not logged (R1, R2) and `verifyAnchorsDbReady` rejects with a TypeError whose message is not the constant (R3, R4), so those assertions fail",
  dbnote="`../db` (the Prisma `$queryRaw` rejects with the value the cell sets; `$executeRaw` counts any write), `../middleware/auth`, `../middleware/rbac` and `../utils/logger` are mocked as in the ks1657 suite; the real `anchorsRouter` is mounted on a real loopback Express server. No database, no anchoring service and no network.",
  greens="'control ks1868 C1' (GET route) and 'control ks1868 C2' (`verifyAnchorsDbReady`): an ordinary `Error` is logged with its own message and the route answers 500 / the helper rejects with the constant error (2 cells)",
  redcells="`R1` (revoked Proxy) and `R2` (message getter throws) on the GET route, `R3` and `R4` the same on `verifyAnchorsDbReady` (4 cells)",
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n- RED ks1868 R3\n- RED ks1868 R4\n",
  fix_anchor="`routes/certifications.ts` (KS-1844) and `services/auth` `routes/auth.ts` (PR 1911)", sib="`ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts`")

ANS=SV+'anchoring/'
AIDX=ANS+'src/index.ts'
AREF=ANS+'src/__tests__/ks1822-a-foreign-tenants-anchor-reads-as-absent.test.ts'
def lg(ind, msg, extra=''):
    return " "*ind+"log('warn', '%s', { %serror: %%s });\n" % (msg, extra)
def e2(ind, msg, extra=''):
    o=lg(ind,msg,extra) % 'err?.message'
    n=G(ind,'err?.message')+(lg(ind,msg,extra) % 'reason')
    return (o,n)
T['p2']=dict(dir='ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw', prod=AIDX, ref=AREF, runner='vitest', runcmd='run ', rdir=ANS[:-1],
  edits=[e2(6,'verify-by-hash: local DB lookup failed'), e2(6,'DB lookup anchor by content hash failed'), e2(4,'DB lookup anchor by tx failed','txHash, ')],
  nh=3, lines='694, 1304 and 1807', test=ANS+'src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts', tsrc='t75_p2.ts.txt',
  fn='the three read-side lookup catches (`GET /api/anchors/verify/:hash` local step, `POST /api/anchors/verify`, `dbGetAnchorByTx` for `GET /api/anchors/tx/:txHash`)', short='three catch blocks',
  whatwrong="In the anchoring service `index.ts` three catch blocks that only LOG a failed anchor_store SELECT and carry on read the rejection value with `err?.message` inside the log call: the local-DB step of `handleAnchorVerifyByHash` (line 694, `log('warn', 'verify-by-hash: local DB lookup failed', { error: err?.message })`), the content-hash lookup of `POST /api/anchors/verify` (line 1304, `DB lookup anchor by content hash failed`) and `dbGetAnchorByTx` (line 1807, `DB lookup anchor by tx failed`, which then returns undefined). If the query rejects with a revoked Proxy, the property read `err?.message` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err?.message` throws. Either way the catch throws before the log line and before its documented fall-through. At the tip: line 694 and line 1304 hand the TypeError to the route's own outer catch (500 for verify-by-hash with `details`, `next(error)` for POST verify) instead of continuing to the chain step / the verified:false answer; line 1807 leaves the async handler of `GET /api/anchors/tx/:txHash` (no try) with a rejection, so Express 4 sends NO response and Node sees an unhandled rejection. The fix reads the SAME expression `err?.message` into a local `reason` inside its own `try`, and a `catch` sets the constant `'unreadable thrown value'`; the log call then uses `reason`. This is the inline guard already merged in `services/auth` `routes/auth.ts` (PR 1911, lines 308-313) and `services/originate` `routes/certifications.ts` (KS-1844); no helper is added.",
  callers="CALLERS (git grep at the tip): `dbGetAnchorByTx` has ONE caller, `GET /api/anchors/tx/:txHash` (line 1271), which answers 404 when it returns undefined. The verify-by-hash catch (694) sits in `handleAnchorVerifyByHash` (registered pre-auth at line 473) and the content-hash catch (1304) in `POST /api/anchors/verify`; all three are READ routes: every statement involved is a SELECT and the cells assert that no INSERT/UPDATE/DELETE/CREATE/ALTER is issued. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the warn line with the error's message and then the same fall-through: 404 (tx route), the chain step (verify-by-hash: with no Cardano credentials a 404 `Not found in local DB and Blockfrost not configured.`), `verified: false` (POST verify). After the fix an unreadable thrown value gets exactly that with the constant reason logged; the cells assert status and body for the ordinary Error and for both unreadable shapes. **Raise-seat attention:** an ordinary DB error on these verify routes already answers 'not found / not verified' (pre-existing, unchanged); today an unreadable one answers 500 (verify routes) or hangs (tx route). Nothing here submits, signs or retries an anchor, writes an anchor status, or selects a wallet/UTxO. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the three lookups log a constant reason and the routes answer as for an ordinary Error (404 / chain step / verified:false) instead of a 500 or no response. Persisted state: none. Recommended tier 1 (anchor verification and lookup routes; Kam's tier-1-with-Opus-gate ruling).",
  ncells='9 cells: C1 to C3 (ordinary Error on each route), R1 to R6',
  red1="At the tip the tx route sends no response (R1, R2: the cell's client times out after 1.5 s and an unhandled rejection is counted) and the two verify routes answer 500 or fall to the error handler (R3 to R6), so the status/body assertions fail",
  dbnote="`../db` keeps its real exports except `isDbAvailable` (true) and `query` (the table-presence probe answers; the SELECT the cell targets rejects with the value the cell sets; any write statement is counted), as in the ks1822 suite; the real `index.ts` app is served on an ephemeral port with a real RS256 bearer (`express.application.listen` is spied before the import). No database, no chain provider and no network.",
  greens="'control ks1868 C1' (tx route), 'control ks1868 C2' (verify-by-hash) and 'control ks1868 C3' (POST verify): an ordinary `Error` is logged with its own message and the route answers as above (3 cells)",
  redcells="`R1`/`R2` (tx route), `R3`/`R4` (verify-by-hash), `R5`/`R6` (POST verify): a revoked Proxy and an Error whose `message` getter throws, once each (6 cells)",
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n- RED ks1868 R3\n- RED ks1868 R4\n- RED ks1868 R5\n- RED ks1868 R6\n",
  fix_anchor="`services/auth` `routes/auth.ts` (PR 1911) and `services/originate` `routes/certifications.ts` (KS-1844)", sib="`ks1822-a-foreign-tenants-anchor-reads-as-absent.test.ts`")

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
    nh=X['nh']
    pins=("# code_patch2: %s (%d hunk) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_this_file_and_its_src/__tests__/_are_in_no_open_PR_(23_PRs_141_files_read_2026-11-02_by_op75,_planted_control_services/auth_in_7_entries);_live_lanes_beyond_PRs_not_checked\n")%(PROD.split('/')[-1],nh,X['ref'],first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]; svc=PROD.split('/')[3]
    runner=X['runner']
    hw='hunk' if nh==1 else 'hunks'
    txt=f"""# KS-1868 {svc}: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {nh} product {hw} given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 75 for Wednesday, 2026-11-02. Secuura ({svc}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (line {X['lines']}), reusing the guard already merged in this file at {X['fix_anchor']}. {OPEN_PR} Other KS-1868 files and the other sites of this file are separate briefs or deliberately skipped.

File: `{PROD}`  (product, modified in place: EXACTLY {nh} {hw})
Test file: `{X['test']}`  (NEW file, {runner}, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `{runner}` (`npx {runner} {X['runcmd']}src/__tests__/{tp}` from `{X['rdir']}`)
Tier: `code_patch2`
Rung: **3 ({nh} product {hw}, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the {nh} {hw} under "The exact change", byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{X['whatwrong']}

## Where

`{PROD}`: line {X['lines']}. {X['callers']}

## The exact change

EXACTLY {nh} {hw} in the product file. The file header lines and the `@@` headers are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text. The log message text is unchanged.

**Do NOT touch** any other catch block of the file, any message text, or any other line.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from the merged sibling suites of this directory ({X.get('sib','`ks1868-get-total-vote-power-unreadable-throw.test.ts`')}; pinned ref `{X['ref']}`). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells
{X.get('redlines','- RED ks1868 R1'+chr(10)+'- RED ks1868 R2'+chr(10))}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {X['red1']} (and no ERROR line is logged); after the edit the constant reason is logged.
- GREEN at the tip and after: {X['greens']}.
- The stand-in rejecting with the thrown value is a plain function, not `{'jest.fn()' if runner=='jest' else 'vi.fn()'}`, on purpose: a spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` line {X['lines']} is the unguarded read at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 23 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or the service's `src/__tests__/` (141 file entries; planted control services/auth/ appears in 7 file entries).
- No test or script reads this log line's text as source other than the new test.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were not touched. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot with a real Postgres and a real Express 4 were not run.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
if __name__=='__main__':
    for k in sys.argv[1:]: build(k)
