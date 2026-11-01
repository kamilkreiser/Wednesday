# Operator 57: KS-1868 tenant-provisioning/src/index.ts catch reads (code_patch2, O53/O55 shape). P1: three clean route catches; P2: DELETE archive route (3 reads).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator57/gen/'
SV='Blockchain/Dev/services/tenant-provisioning/'
PROD=SV+'src/index.ts'
TD=SV+'src/__tests__/'
REF=TD+'ks1861-tenant-delete-archives-and-keeps-every-row.test.ts'
def guard(ind, expr, var):
    s=' '*ind
    return (s+"let %s: string;\n"%var+s+"try {\n"+s+"  %s = %s;\n"%(var,expr)+s+"} catch {\n"+s+"  %s = 'unreadable thrown value';\n"%var+s+"}\n")
E="err instanceof Error ? err.message : String(err)"
def site(route):
    old="    const message = %s;\n    console.error('[provisioning] %s failed:', message);\n"%(E,route)
    new=guard(4,E,'message')+"    console.error('[provisioning] %s failed:', message);\n"%route
    return old,new
OLD_RB="""      await client.query('ROLLBACK').catch((rollbackErr: unknown) => {
        console.error('[provisioning] DELETE /api/tenants/:id rollback failed:', rollbackErr instanceof Error ? rollbackErr.message : String(rollbackErr));
      });
"""
NEW_RB="""      await client.query('ROLLBACK').catch((rollbackErr: unknown) => {
"""+guard(8,"rollbackErr instanceof Error ? rollbackErr.message : String(rollbackErr)",'reason')+"""        console.error('[provisioning] DELETE /api/tenants/:id rollback failed:', reason);
      });
"""
OLD_OUT="""  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    // Ruling 1 (KS-1861): the audit log records a failed attempt too."""
NEW_OUT="""  } catch (err: unknown) {
"""+guard(4,E,'message')+"""    // Ruling 1 (KS-1861): the audit log records a failed attempt too."""
OLD_AU="""    ).catch((auditErr: unknown) => {
      console.error('[provisioning] DELETE /api/tenants/:id could not audit the failure:', auditErr instanceof Error ? auditErr.message : String(auditErr));
    });
"""
NEW_AU="""    ).catch((auditErr: unknown) => {
"""+guard(6,"auditErr instanceof Error ? auditErr.message : String(auditErr)",'reason')+"""      console.error('[provisioning] DELETE /api/tenants/:id could not audit the failure:', reason);
    });
"""
T={
 'p1':dict(dir='ks_1868_o57_p1_tenant_provisioning_get_tenant_patch_status_get_audit_log_unreadable_throw',
   edits=[site('GET /api/tenants/:id'),site('PATCH /api/tenants/:id/status'),site('GET /api/audit-log')],
   fn='three route catches of tenant-provisioning `index.ts` (GET /api/tenants/:id, PATCH /api/tenants/:id/status, GET /api/audit-log)',
   short='three log-only route catches', lines='424, 482 and 651',
   test=TD+'ks1868-tenant-provisioning-route-catches-p1-unreadable-throw.test.ts', tsrc='t57_p1.ts.txt', ncells='12 cells: 3 routes x (R1, R2, C1, C2)',
   hunks='3', nh=3,
   redlines="- RED ks1868 R1\n- RED ks1868 R2\n",
   redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route (6 cells)",
   greens="'control ks1868 C1' (an ordinary `Error` logs its own message and the answer is the constant 500 without it) and 'control ks1868 C2' (a thrown string is logged as itself, as before), once per route (6 cells)",
   whatwrong="In `index.ts` the catch blocks of GET /api/tenants/:id (line 424), PATCH /api/tenants/:id/status (line 482) and GET /api/audit-log (line 651) each begin `const message = err instanceof Error ? err.message : String(err);`, then `console.error('[provisioning] <route> failed:', message);`, then answer the CONSTANT 500 body `{ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } }`; the message is only logged (KS-1410 made it never reach the response). If the route's database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before anything is logged and before the 500 is sent; the async handler rejects, Express 4 does not catch that, and the request gets no response (the gateway's upstream timeout answers 504). The fix replaces the ONE `const message` line of each catch with `let message: string;` plus a `try` that runs the SAME expression and a `catch` that sets the constant `'unreadable thrown value'`; every later line (the `console.error` line, the 500) is untouched, and an ordinary Error still logs its own message. This is the inline guard already merged in other services (analytics ExportService.dbSaveExport, nft-certificate minting.service.ts, billing PR 1906); this service has no helper and none is added.",
   callers="CALLERS (git grep at the tip): all three are called only over HTTP by `services/api-gateway/src/routes/platform.ts` (`/api/tenants/${id}` GET at :365/:1039, `/status` PATCH at :401, `/api/audit-log` GET at :488), each through `fetchWithTimeout`. GET /api/tenants/:id and GET /api/audit-log are READ-ONLY routes. PATCH /api/tenants/:id/status runs an UPDATE, then (if a row changed) a SEPARATE audit INSERT, with no transaction: unchanged by this fix. **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable thrown value from the database call: today the catch itself throws, the request gets NO response and Node sees an unhandled rejection (process-fatal on Node >= 15); after, the constant reason is logged and the route answers its existing constant 500, exactly what an ordinary Error already gets. (2) Persisted state: none changes. For PATCH /status, if the UPDATE succeeded and the audit INSERT then rejects with an unreadable value, the status change stays and no audit row exists, before and after (an ordinary Error leaves the same state). No response body, status code or log text for an ordinary Error or a string changes.",
   dbnote="`express` (the route handlers are captured; `param`, `patch` and `delete` included), `pg` (a `Pool` whose `query` and `connect().query` return what the cell plans) and `@secuura/shared` (the five names the module imports) are replaced; the captured handler is called with a fake request and response, no port is bound, no database is touched. Each cell makes EVERY database statement reject with the thrown value.",
   red1="At the tip the handler rejects instead of answering, so the response stays at the default 200 and the status assertion fails"),
 'p2':dict(dir='ks_1868_o57_p2_tenant_provisioning_delete_archive_rollback_outer_audit_unreadable_throw',
   edits=[(OLD_RB,NEW_RB),(OLD_OUT,NEW_OUT),(OLD_AU,NEW_AU)],
   fn='the three catch reads of the tenant-provisioning DELETE /api/tenants/:id archive route',
   short='three catch reads of one route', lines='603, 622 and 629',
   test=TD+'ks1868-tenant-provisioning-delete-catches-p2-unreadable-throw.test.ts', tsrc='t57_p2.ts.txt', ncells='12 cells: 2 thrown kinds x (outer, rollback, audit) = 6 red, plus 3 controls = 9',
   hunks='2', nh=2,
   redlines="- RED ks1868 outer\n- RED ks1868 rollback\n- RED ks1868 audit\n",
   redcells="`outer`, `rollback` and `audit`, each with `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws) as the thrown value (6 cells)",
   greens="'control ks1868 C1 outer', 'C2 rollback' and 'C3 audit' (ordinary Errors: each is logged with its own message, the failed attempt is audited, and the answer is the constant 500), the controls showing the normal path is unchanged (3 cells)",
   whatwrong="In `index.ts` the DELETE /api/tenants/:id handler archives a tenant inside a transaction. Three catch reads of a caught value are written `x instanceof Error ? x.message : String(x)`: (1) line 603, inside the transaction block's `catch (err)`: `await client.query('ROLLBACK').catch((rollbackErr: unknown) => { console.error('... rollback failed:', rollbackErr instanceof ...) })`, after which the block rethrows the ORIGINAL `err`; (2) line 622, the first line of the outer `catch (err: unknown)`: `const message = err instanceof Error ? err.message : String(err);`, which comes BEFORE the Ruling-1 (KS-1861) `tenant_archive_failed` audit INSERT and the constant 500; (3) line 629, inside that INSERT's `.catch((auditErr: unknown) => { console.error('... could not audit the failure:', auditErr instanceof ...) })`. If the value is a revoked Proxy (`instanceof` throws) or an Error whose `message` getter throws: (1) the `.catch` callback throws, so the ROLLBACK await rejects with a TypeError that REPLACES the original error (the outer catch then reports the TypeError, not the cause); (2) the outer catch throws on its first line: no failed-attempt audit row, no 500, the request gets no response (unhandled rejection); (3) the callback throws, the INSERT's await rejects out of the catch block, and the 500 is never sent. The fix wraps each read in its own try with the constant fallback `'unreadable thrown value'`: (1) and (3) read into a local `reason` used by the existing console.error line, (2) turns the one `const message` line into `let message: string;` + try/catch; every other line is untouched, and ordinary Errors log exactly what they log today. No helper is added (this service has none; this is the inline guard merged in analytics, nft-certificate and billing PR 1906).",
   callers="CALLERS (git grep at the tip): the route is called only over HTTP by `services/api-gateway/src/routes/platform.ts` (`/api/tenants/${id}` DELETE at :420) through `fetchWithTimeout`. It is the tenant ARCHIVE route (KS-1861: status set to `archived`, no row deleted, no database dropped), a platform-admin write. **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable value from the transaction (outer): today the catch throws on its first line, so NO `tenant_archive_failed` audit row is written and the caller gets NO response (gateway 504); after, the audit row is written, the cause is logged as `unreadable thrown value` and the route answers the constant 500, exactly what an ordinary Error already gets (cell `outer`, control C1). The transaction itself is unaffected: its ROLLBACK already ran in the inner catch, so no archive is committed before or after. (2) unreadable value from the ROLLBACK itself: today the original error is lost and replaced by a TypeError; after, the rollback failure is logged as `unreadable thrown value` and the original error is the one the outer catch reports (same as an ordinary rollback Error, control C2). (3) unreadable value from the audit INSERT: today no 500 is sent; after, it is logged and the constant 500 is sent (control C3). Persisted state differs only in (1): the failed-attempt audit row now exists, as it does for an ordinary Error.",
   dbnote="`express` (the route handlers are captured), `pg` (a `Pool` whose `query` and `connect().query` answer the tenant read and the statements of the archive transaction, and reject the UPDATE, the ROLLBACK or the failed-attempt audit INSERT with the value the cell sets) and `@secuura/shared` (the five names the module imports) are replaced; the captured DELETE handler is called with a fake request and response, no port is bound, no database is touched.",
   red1="At the tip the handler rejects or reports the wrong error, so the response stays at the default 200 (outer, audit) or the log does not name the original error (rollback) and the assertions fail"),
}
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 19 open PRs read 2026-11-02 through the GitHub API; 108 file entries; services/tenant-provisioning appears only as package.json / package-lock.json in PRs 649 and 1360; planted positive control: the same scan finds services/originate in 6 entries)."
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
    pins=("# code_patch2: tenant-provisioning index.ts (%s hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/tenant-provisioning_src/index.ts_and_src/__tests__/_are_in_no_open_PR_(19_PRs_108_files_read_2026-11-02_by_op57,_tenant-provisioning_only_as_package.json/package-lock.json_in_649/1360,_positive_control_services/originate_in_6_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['hunks'],REF,first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 tenant-provisioning: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {X['hunks']} product hunks given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 57 for Wednesday, 2026-11-02. Secuura (tenant-provisioning) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (lines {X['lines']}). {OPEN_PR} Sibling sites of this file are separate briefs (O57-P1, O57-P2); this pass is generated against the same tip and is disjoint from the other. The catch blocks that start with an `instanceof z.ZodError` check (POST /api/tenants, GET /api/tenants, PATCH /api/tenants/:id) are deliberately NOT in this series: on a revoked Proxy that check throws before the message line, so a message-line-only fix would be half a fix.

File: `{PROD}`  (product, modified in place: EXACTLY {X['hunks']} hunks)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/tenant-provisioning`)
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

**Do NOT touch** any message text, any other line of the file, or any other catch block in it (in particular the three catch blocks that start with `instanceof z.ZodError`, and the POST /api/tenants create route).

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (a vitest file that replaces `pg` and `@secuura/shared` and imports the entry module). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character, including every backslash, exactly as given.

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
- Open PRs: 19 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (108 file entries; services/tenant-provisioning only as package.json / package-lock.json in PRs 649 and 1360); the positive control services/originate appears in 6 file entries.
- The existing `ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts` reads this file as text and requires `console.error(...message...)` within four lines before each 500 and exactly three `details: err.errors`: this change keeps both (the variable stays named `message` where it was, no ZodError block is touched).
- The pinned ref `ks1861-tenant-delete-archives-and-keeps-every-row.test.ts` runs in the baseline.

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
