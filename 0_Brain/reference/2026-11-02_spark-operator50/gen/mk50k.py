# Operator 50, task 2 (KS-1796 auth.openapi.ts + GENERATED docs/openapi/secuura-api.yaml): code_patch2 brief generator.
import sys, os, re, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='ca36945e974081be6abbc15e548f4f8d02767e14'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator50/gen/'
G='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/66680214-b2c7-480c-9bb4-0097b61ede13/scratchpad/g/'
D='Blockchain/Dev/'
TS=D+'services/auth/src/auth.openapi.ts'
YAML=D+'docs/openapi/secuura-api.yaml'
TEST=D+'services/auth/src/__tests__/ks1796-change-password-publishes-its-422.test.ts'
REF=D+'services/auth/src/__tests__/ks1467-the-weak-password-422-through-the-real-routes.test.ts'
# the product edit = what the generator produced in the scratch clone (ts edited by the operator, yaml WRITTEN BY scripts/generate-openapi.ts)
ts_new=open(G+'clone/'+TS,encoding='utf-8').read()
ts_old=mk.rd(TS)
yaml_diff=open(G+'yaml_only.diff',encoding='utf-8').read()   # `git diff -U3` of the generated yaml, index line removed
pd_ts=mk.udiff(TS,ts_old,ts_new); ts_body=pd_ts.split('\n',1)[1]
pd_y=yaml_diff
y_body=pd_y.split('\n',1)[1]
tbody=open(GEN+'t50_k.ts.txt',encoding='utf-8').read(); nl=len(tbody.splitlines())
td=mk.udiff(TEST,'',tbody,True)
golden=pd_ts+pd_y+td
d=BR+'ks_1796_o50_p1_auth_change_password_422_openapi'
if os.path.exists(d+'/golden.diff') and not os.environ.get('GEN_OVERWRITE'): sys.exit('exists')
os.makedirs(d,exist_ok=True)
open(d+'/golden.diff','w',encoding='utf-8').write(golden)
open(d+'/spark.pins','w').write("# code_patch2: auth.openapi.ts (1 hunk) + GENERATED secuura-api.yaml (2 hunks) + a NEW vitest file; ref = shape only; line = the first changed line in auth.openapi.ts.\ntier=code_patch2\nref=%s\nline=1012\nctx=65536\nstarted_ok=KS-1796_state_read_from_the_board_screen_2026-11-01;_auth.openapi.ts_and_docs/openapi/secuura-api.yaml_are_in_no_open_PR_(22_PRs_128_files_read_2026-11-02_by_op50)\n"%REF)
txt=f"""# KS-1796 auth: the published change-password operation must declare its 422 (RUNG 3, code_patch2: one source hunk and two GENERATED-file hunks dictated, one NEW test file given whole)

DRAFT by Spark operator 50 for Wednesday, 2026-11-02. Secuura (auth) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Ticket KS-1796 (board screen 2026-11-01, section 3 item 4): in `services/auth/src/auth.openapi.ts` the `POST /api/users/me/change-password` operation (line 1012) declares one 400 "Wrong current password or new password too weak" and no 422, but the handler (`routes/users.ts`, change-password) throws `BadRequestError` (400) for a wrong current password and `ValidationError` (422) for a weak new password, checked AFTER the current password verified. The sibling `POST /api/auth/reset-password` block (line 813) already declares `422: {{ ...commonErrorResponses[422], description: 'New password too weak' }}` and is the citable source. `docs/openapi/secuura-api.yaml` is GENERATED from the source by `scripts/generate-openapi.ts`: the yaml hunks below were produced by RUNNING THAT GENERATOR on the edited source in a scratch clone at the tip (the baseline `--check` passed first, rc 0), not written by hand; the generator discovered 19 service files and wrote 314 paths. No open PR touches either file (22 open PRs, 128 file entries read 2026-11-02; services/auth appears only as users.ts, a ks1006 test and package.json).

File: `{TS}`  (product source, modified in place: ONE hunk)
File: `{YAML}`  (GENERATED product, modified in place: TWO hunks; the file is very large, you get excerpts)
Test file: `{TEST}`  (NEW file, vitest, given in full below; 5 cells (3 red, 2 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/ks1796-change-password-publishes-its-422.test.ts` from `Blockchain/Dev/services/auth`)
Tier: `code_patch2`
Rung: **3 (dictated hunks; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 3 file(s), in this order:
1. `{TS}` - modified in place: EXACTLY the one hunk under "The exact change".
2. `{YAML}` - modified in place: EXACTLY the two hunks under "The exact change", byte for byte.
3. `{TEST}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nl} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

The published contract for change-password tells a client that one 400 covers both a wrong current password and a weak new password, and declares no 422, while the service answers the weak password with 422. The fix splits them exactly as the reset-password sibling does: the 400 text becomes `Wrong current password` and a `422` entry `New password too weak` (same body schema as the sibling) is added, in the source and in the generated spec.

## Where

`{TS}:1012`, and the generated entry of `/api/users/me/change-password` in `{YAML}` (about lines 17143 and 17169).

## The exact change

THREE section headers and every `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). A context line contains an em dash; copy it unchanged.

Source file, one hunk:

```diff
{ts_body}```

Generated spec, two hunks (the 422 entry is inserted between the 415 and 429 entries because the generator orders responses by status):

```diff
{y_body}```

**Do NOT touch** any other line of either file, nor any other operation.

## The test

File: `{TEST}`

A NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}`; it reads the real spec and the real source from disk (no mocks, no network, no server). Keep every character, including quotes, exactly as given.

```diff
{td}```

## Red cells
- RED ks1796 R1
- RED ks1796 R2
- RED ks1796 R3

## Cells and controls

- RED at the tip, GREEN after: R1 (422 declared, same schema as reset-password), R2 (400 text) and R3 (the TypeScript source says the same as the YAML). All fail by assertion at the tip.
- GREEN at the tip and after: C1 (the spec and the sibling are found; the sibling's 422 is the entry copied) and C2 (the other statuses of the operation are unchanged).

## UNMEASURED - stated rather than glossed

- The golden is written by the operator; the YAML part is the generator's own output. tsc and eslint on the new file were not run outside the checker. Whether other consumers of the spec (gateway spec method map, Schemathesis, the docs fragments) react to a new 422 on this operation is not measured here beyond the checker's suites.

## Scope

**This operation only.** Refs KS-1796. No handler change.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 3 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
open(d+'/KS-1796.md','w',encoding='utf-8').write(txt)
print('wrote',d)
