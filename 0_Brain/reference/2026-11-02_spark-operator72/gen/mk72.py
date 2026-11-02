# Operator 72: KS-1868 nft ipfs upload catches / verifier / admin. Vitest. Reuses spark/gen/mk.py (udiff); rd() reads the read-only clone at TIP.
import sys, os, subprocess, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='8aded39571d0d26dc5cd3632948803cd95c4680c'
CLONE='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate89-e25-1904-1906-1907/repo'
def rd(p): return subprocess.run(['git','-C',CLONE,'show',TIP+':'+p],check=True,capture_output=True).stdout.decode('utf-8')
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator72/gen/'
def G(ind,expr):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
OPEN_PR_TAIL="(the open PRs read 2026-11-02 through the GitHub API; 126 file entries; the file appears in none; the positive control services/originate is present in 7 entries)."
exec(open(GEN+'sites72.py',encoding='utf-8').read())
def build(k):
    X=T[k]; SV=X['sv']; PROD=SV+X['file']; TD=SV+'src/__tests__/'; REF=TD+X['ref']; TEST=TD+X['testname']
    old=rd(PROD); new=old
    for o,n in X['edits']:
        assert new.count(o)==1,(k,o[:70],new.count(o))
        new=new.replace(o,n)
    import difflib as _dl, types as _ty
    _n=X.get('ctxn',3); mk.difflib=_ty.SimpleNamespace(unified_diff=lambda a,b,n=3: _dl.unified_diff(a,b,n=_n))
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    hl=[l for l in pd.splitlines() if l.startswith('@@ ')]
    assert len(hl)==X['nh'],(k,len(hl),hl)
    tbody=open(GEN+X['tsrc'],encoding='utf-8').read()
    td=mk.udiff(TEST,'',tbody,True); nlines=len(tbody.splitlines())
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
    pins=("# code_patch2: %s (%s hunk) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_%s_and_its_src/__tests__/_are_in_no_open_PR_(22_PRs_126_files_read_2026-11-02_by_op72,_positive_control_services/originate_in_7_entries);_live_lanes_beyond_PRs_not_checked\n")%(X['file'],X['nh'],REF,first,X['file'].replace(' ','_'))
    open(d+'/spark.pins','w').write(pins)
    tp=X['testname']; nh=X['nh']
    txt=f"""# KS-1868 {X['svname']}: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {nh} product hunk(s) given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 72 for Wednesday, 2026-11-02. Secuura ({X['svname']}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)` or `(X as Error).message`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (lines {X['lines']}), reusing {X['fixnote']}. No open PR touches this file or its `src/__tests__/` directory {OPEN_PR_TAIL} Other KS-1868 files and the other sites of this file are separate briefs or deliberately skipped.

File: `{PROD}`  (product, modified in place: EXACTLY {nh} hunk(s))
Test file: `{TEST}`  (NEW file, vitest, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `{SV.rstrip('/')}`)
Tier: `code_patch2`
Rung: **3 ({nh} product hunk(s), skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the {nh} hunk(s) under "The exact change", byte for byte.
2. `{TEST}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{X['whatwrong']}

## Where

`{PROD}`: lines {X['lines']}. {X['callers']}

## The exact change

EXACTLY {nh} hunk(s) in the product file. The file header lines and the `@@` header(s) are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/{PROD} b/{PROD}`).**

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text. The returned/logged message text is unchanged except for the value.

**Do NOT touch** any other catch block of the file, any message text, or any other line.

## The test

File: `{TEST}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from the merged sibling suite of this directory (`{X['sibling']}`; pinned ref `{REF}`). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells
{X['redlines']}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {X['red1']}; after the edit the constant reason is used.
- GREEN at the tip and after: {X['greens']}.
- The stand-ins rejecting with the thrown value are plain functions, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}` lines {X['lines']} are the unguarded reads at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 22 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `{SV}src/__tests__/` ; the positive control services/originate appears in 7 file entries.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. {X['unm']} Whether a real path throws such a value here is not known (KS-1868 says the same).

## Scope

**This site only.** Refs KS-1868; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
