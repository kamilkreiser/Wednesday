# Operator 62: KS-1868 tenant-provisioning index.ts, the three Zod-preceded catches (code_patch2). One pass O62-P1, 3 hunks.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator62/gen/'
SV='Blockchain/Dev/services/tenant-provisioning/'
PROD=SV+'src/index.ts'
TD=SV+'src/__tests__/'
REF=TD+'ks1861-tenant-delete-archives-and-keeps-every-row.test.ts'
TEST=TD+'ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts'
CATCH="  } catch (err: unknown) {\n"
NEWHEAD=("  } catch (thrown: unknown) {\n"
"    let err: unknown = thrown;\n"
"    try {\n"
"      if (!(thrown instanceof z.ZodError)) {\n"
"        String(thrown instanceof Error ? thrown.message : thrown);\n"
"      }\n"
"    } catch {\n"
"      err = new Error('unreadable thrown value');\n"
"    }\n")
ANCH=[CATCH+"    if (err instanceof z.ZodError) {\n",
      CATCH+"    // Return 400 for validation errors, 500 for everything else\n",
      CATCH+"    // KS-497: a body failing updateTenantSchema"]
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 22 open PRs read 2026-11-02 through the GitHub API; 125 file entries; services/tenant-provisioning appears only as package.json / package-lock.json in PRs 649 and 1360; planted positive control: the same scan finds services/originate in 6 entries)."
old=mk.rd(PROD); new=old
for a in ANCH:
    assert new.count(a)==1,(a,new.count(a))
    new=new.replace(a,NEWHEAD+a[len(CATCH):])
pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
hl=[l for l in pd.splitlines() if l.startswith('@@ ')]
assert len(hl)==3,hl
print(pd)
tbody=open(GEN+'t62_p1.ts.txt',encoding='utf-8').read()
td=mk.udiff(TEST,'',tbody,True); nlines=len(tbody.splitlines())
golden=pd+td
d=BR+'ks_1868_o62_p1_tenant_provisioning_zod_precheck_post_get_patch_tenants_unreadable_throw'
os.makedirs(d,exist_ok=True)
open(d+'/golden.diff','w',encoding='utf-8').write(golden)
first=0;cur=None
for l in pd.splitlines():
    if l.startswith('@@ '):
        cur=int(l.split()[1].split(',')[0][1:]); continue
    if cur is None: continue
    if l.startswith('-') and not l.startswith('---'): first=cur; break
    if l.startswith(' '): cur+=1
assert first
pins=("# code_patch2: tenant-provisioning index.ts (3 hunks) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
 "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/tenant-provisioning_src/index.ts_and_src/__tests__/_are_in_no_open_PR_(22_PRs_125_files_read_2026-11-02_by_op62,_tenant-provisioning_only_as_package.json/package-lock.json_in_649/1360,_positive_control_services/originate_in_6_entries);_O57_holds_two_disjoint_passes_here_not_in_any_PR;_live_lanes_beyond_PRs_not_checked\n")%(REF,first)
open(d+'/spark.pins','w').write(pins)
tp=TEST.split('/')[-1]
txt=f"""# KS-1868 tenant-provisioning: the three Zod-preceded catches (POST /api/tenants, GET /api/tenants, PATCH /api/tenants/:id) must still answer when the thrown value cannot be read (RUNG 3, code_patch2: 3 product hunks given as skeletons, one NEW test file given whole)

DRAFT by Spark operator 62 for Wednesday, 2026-11-02. Secuura (tenant-provisioning) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes three catch blocks in ONE file, inline, with no shared helper (lines 337, 378 and 536). {OPEN_PR} Other sites of this file (O57-P1, O57-P2, held, not in any PR) are separate passes generated against the same tip and are disjoint from this one by more than three lines.

File: `{PROD}`  (product, modified in place: EXACTLY 3 hunks)
Test file: `{TEST}`  (NEW file, vitest, given in full below; 12 cells: 3 routes x (R1, R2, C1, C2))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/tenant-provisioning`)
Tier: `code_patch2`
Rung: **3 (3 product hunks, skeletons dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the 3 hunks under "The exact change", in that order, byte for byte.
2. `{TEST}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

In `index.ts` the catch blocks of POST /api/tenants (line 337), GET /api/tenants (line 378) and PATCH /api/tenants/:id (line 536) each begin `catch (err: unknown) {{` and test `if (err instanceof z.ZodError)` first (it answers 400 with `details: err.errors` and returns), then read `const message = err instanceof Error ? err.message : String(err);` for a `console.error` line and a 500. If a database call rejects with a revoked Proxy, `err instanceof z.ZodError` itself throws a TypeError as the first statement of the catch; if it rejects with an Error whose `message` getter throws, `err.message` throws on the message line. Either way the catch throws before anything is logged and before any response is sent; the async handler rejects, Express 4 does not catch that, and the request gets no response. A fix on the message line alone is half a fix, because the ZodError test runs first. The fix renames the catch variable to `thrown`, declares `let err: unknown = thrown;` and runs one try that probes BOTH reads on `thrown` (the `instanceof z.ZodError` test, and for anything that is not a ZodError the same message expression); if the probe throws, `err` becomes `new Error('unreadable thrown value')`. Every later line of the catch keeps using `err` and is untouched: an ordinary ZodError still answers 400 with `details: err.errors`, an ordinary Error or string still takes its own path, and an unreadable value takes exactly the path an ordinary Error takes. This is the shape already used for the analytics Zod-preceded catches (O61, 3/3 PASS); this service has no helper and none is added.

## Where

`{PROD}`: lines 337, 378 and 536. CALLERS (git grep at the tip): all three are called only over HTTP by `services/api-gateway/src/routes/platform.ts`, each through `fetchWithTimeout`. **BEHAVIOUR CHANGES the raise PR must state:** (1) unreadable thrown value: today the catch itself throws on its first statement, the request gets NO response and Node sees an unhandled rejection; after, it takes the path an ordinary Error takes: logged as `unreadable thrown value`, then GET /api/tenants and PATCH /api/tenants/:id answer the existing constant 500, and POST /api/tenants answers its existing 500 whose `message` is the caught message (the answer line is untouched; Kam's open card on that answer is not touched). (2) Persisted state, POST /api/tenants (it CREATES a tenant): a ZodError path never rolls back and still does not (unchanged, also when raised after the tenant row is inserted); an ordinary Error after the tenant row was inserted rolls the partial tenant back with three DELETEs and still does (unchanged); the only difference is the unreadable value after the insert: today the catch throws first, so NO rollback runs and the partial `provisioning` tenant row stays; after, the rollback runs exactly as for an ordinary Error. Before the insert nothing is persisted on any path. GET /api/tenants persists nothing; PATCH /api/tenants/:id persists nothing on a failing UPDATE (its audit INSERT follows the UPDATE separately, no transaction, unchanged). No response body, status code or log text for an ordinary ZodError, Error or string changes.

## The exact change

EXACTLY 3 hunks in the product file, in this order. The file header lines and every `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it (in particular the catch blocks of the other routes, the cleanup `catch (cleanupErr)` and the inner key-service catches of POST /api/tenants).

## The test

File: `{TEST}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (a vitest file that replaces `pg` and `@secuura/shared` and imports the entry module). `express` (the route handlers are captured), `pg` (a `Pool` whose `query` and `connect().query` answer what the cell plans) and `@secuura/shared` (the five names the module imports) are replaced, and the key-service `fetch` is replaced by a rejection; the captured handler is called with a fake request and response, no port is bound, no database is touched. The test file contains backslashes, quotes and template strings: keep every character, including every backslash, exactly as given.

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws), once per route (6 cells). At the tip the handler rejects instead of answering, so the response stays at the default 200 and the status assertion fails; after the edit the constant `unreadable thrown value` is logged and the route answers its ordinary-Error 500 (POST also rolls the partial tenant back with three DELETEs).
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary ZodError answers 400 with `details` equal to its `errors`, logs nothing, and rolls nothing back) and 'control ks1868 C2' (an ordinary Error logs its own message and answers the same 500 as before, POST rolling back with three DELETEs), once per route (6 cells).
- The stand-ins rejecting with the thrown value are plain functions, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` lines 337, 378 and 536 are the `catch (err: unknown) {{` heads of the three Zod-preceded catches at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 22 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (125 file entries; services/tenant-provisioning only as package.json / package-lock.json in PRs 649 and 1360); the positive control services/originate appears in 6 file entries.
- The existing `ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts` reads this file as text and requires `console.error(...message...)` within four lines before each 500 (unchanged: the message lines and the 500 lines are not touched) and exactly three `details: err.errors` (unchanged: those lines are not touched, and `err` is still the name used there). It stays green and is not edited.
- The pinned ref `ks1861-tenant-delete-archives-and-keeps-every-row.test.ts` runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were not touched or measured (POST's `(cleanupErr as Error).message` and `(err as Error).message` in the inner key-service catches are separate, unfixed reads). Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path, a real Postgres and a real Express 4 were not run.

## Scope

**These sites only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
print('wrote',d)
