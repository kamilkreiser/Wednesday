# Operator 41 brief generator. Reuses spark/gen/mk.py (rd, udiff) for the diffs; the prose follows the o36 brief.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='85c56a3d1eb92c8399dcfd3d6ee2a717cf356428'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
SVC='Blockchain/Dev/services/'
FALL="'unreadable thrown value'"

exec(open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_spark-operator41/gen/tasks41.py').read())

def build(k):
    T=TASKS[k]
    old=mk.rd(T['prod']); assert old.count(T['old'])==1
    new=old.replace(T['old'],T['new'])
    pd=mk.udiff(T['prod'],old,new)
    pd_body=pd.split('\n',1)[1]          # drop the `diff --git` line like the o35 briefs
    td=mk.udiff(T['test'],'',T['tbody'],True)
    nlines=len(T['tbody'].splitlines())
    golden=pd+td
    d=BR+T['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    pins=("# code_patch2: %s (1 hunk) + a NEW vitest file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_Backlog;_%s_source_is_in_no_open_PR_(19_PRs_108_files_read_2026-11-01_by_op41,_positive_control_services/auth_in_7_entries);_file_is_not_tenant-context/tenant-pool-manager;_live_lanes_beyond_PRs_not_checked\n")%(T['file'],T['ref'],T['where_line'],T['svc'].replace('-','_'))
    open(d+'/spark.pins','w').write(pins)
    tp=T['test'].split('/')[-1]; pp=T['prod']
    txt=f"""# KS-1868 {T['svc']}: {T['fn']} must still report when the thrown value cannot be read (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW vitest file given whole)

DRAFT by Spark operator 41 for Wednesday, 2026-11-01. Secuura ({T['svc']}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {T['intro_site']}. {T['consequence']} No open PR touches this file (the 19 open PRs read 2026-11-01 through the GitHub API; 128 file entries; planted positive control: the same scan finds services/auth in 7 of them).

File: `{pp}`  (product, modified in place: ONE hunk)
Test file: `{T['test']}`  (NEW file, vitest, given in full below; 3 cells (2 red, 1 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `{T['runner_dir']}`)
Tier: `code_patch2`
Rung: **3 (one product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{pp}` - modified in place: EXACTLY the one hunk under "The exact change", byte for byte.
2. `{T['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{T['whatwrong']}

## Where

`{pp}:{T['where_line']}`. {T['where_note']}

## The exact change

ONE hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The log message text may contain an em dash; copy it unchanged.

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. {T['sibling']}.

## The test

File: `{T['test']}`

The test section is a NEW vitest file given whole. The `+` lines are byte-exact. The shape is copied from `{T['ref']}` (a `vi.hoisted` holder, `vi.mock(...)` of the collaborators, then the import). There is no database, no app boot and no network here.

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws). {T['red1']}; after the edit the result carries the constant `unreadable thrown value`.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `Error` logs/returns its own message), the control showing the normal path is unchanged.
- The stand-in rejecting with the thrown value is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.
- {T['dbnote']}

## Premises (each one measured, with where)

- `{pp}:{T['where_line']}` is the `instanceof Error` read at the tip (read whole with `git show` at `{TIP[:12]}`). {T['where_note']}
- Open PRs: 19 read 2026-11-01 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{pp}` (19 PRs, 108 file entries); the positive control services/auth appears in 7 file entries.
- {T['s9note']}

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the 253 were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path was not run.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
