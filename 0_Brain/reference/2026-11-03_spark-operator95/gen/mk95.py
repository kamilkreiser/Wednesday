# operator 95: KS-1868 brief builder. Derived from operator 89 mk89b.py. Reuses spark/gen/mk.py.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
mk.SRC='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator95/repo/'
TIP=mk.TIP=os.environ.get('MK_TIP','27fe5476526c4200b752449e04be689724289e6d')
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator95/gen/'
SV='Blockchain/Dev/services/'
OS=SV+'originate/'
OPEN_PR="No open PR lists this file or the new test file name (the 23 open PRs read 2026-11-03 through the GitHub API; 124 file entries; planted control services/originate present in 5 entries)."
def G(ind,expr):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
T={}
KEEPBLANK=set(os.environ.get('KEEPBLANK','').split(','))
exec(open(GEN+'sites95.py').read())
def build(k):
    X=T[k]; PROD=X['prod']; K=X['key']; kl=K.lower().replace('-','')
    old=mk.rd(PROD); new=old
    for o,n in X['edits']:
        assert new.count(o)==1,(k,o[:70],new.count(o))
        new=new.replace(o,n)
    if k in KEEPBLANK:
        import difflib
        pd=''.join([f'diff --git a/{PROD} b/{PROD}\n',f'--- a/{PROD}\n',f'+++ b/{PROD}\n']+list(difflib.unified_diff(old.splitlines(True),new.splitlines(True),n=3))[2:])
    else:
        pd=mk.udiff(PROD,old,new)
    pd_body=pd.split('\n',1)[1]
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
        if (l.startswith('-') and not l.startswith('---')) or (l.startswith('+') and not l.startswith('+++')): first=cur; break
        if l.startswith(' '): cur+=1
    assert first
    nh=X['nh']
    pins=("# code_patch2: %s (%d hunk) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_umbrella_Refs_only;_operator_95_screen;_status_not_read_by_operator;_open_PRs_(23_PRs_124_files_read_2026-11-03_by_op95,_planted_control_services/originate_in_5_entries)_and_held_READY_files_checked_per_the_brief;_live_lanes_beyond_PRs_not_checked\n")%(PROD.split('/')[-1],nh,X['ref'],first)
    open(d+'/spark.pins','w').write(pins)
    tp=X['test'].split('/')[-1]; svc=PROD.split('/')[3]
    runner=X['runner']
    hw='hunk' if nh==1 else 'hunks'
    txt=f"""# {K} {svc}: {X['fn']} must still report when the thrown value cannot be read (RUNG 3, code_patch2: {nh} product {hw} given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 95 for Wednesday, 2026-11-03. Secuura ({svc}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: {K} (catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes {X['short']} in ONE file, inline, with no shared helper (line {X['lines']}), {X['reuse']} {X.get('openpr',OPEN_PR)} Other KS-1868 files and the other sites of this file are separate briefs or deliberately skipped.

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

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text. The message text around the reason is unchanged.

**Do NOT touch** any other catch block of the file, any message text, or any other line.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from the merged sibling suites of this directory ({X.get('sib','`ks1868-signatories-write-routes-p2-unreadable-throw.test.ts`')}; pinned ref `{X['ref']}`). {X['dbnote']} The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{td}```

## Red cells
{X.get('redlines','- RED '+kl+' R1'+chr(10))}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {X['red1']} ; after the edit the reply carries the constant or the coerced text.
- GREEN at the tip and after: {X['greens']}.
- The stand-in rejecting with the thrown value is a plain function, not `{'jest.fn()' if runner=='jest' else 'vi.fn()'}`, on purpose: a spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- {X['premise']} (read whole with `git show` at `{TIP[:12]}`).
- {X.get('premise_pr', 'Open PRs:  23 read 2026-11-03 via the GitHub REST API (pulls?state=open, then pulls/N/files); none lists `'+PROD+'` or the new test file (124 file entries; planted control services/originate appears in 5 file entries).')}
- No test or script reads this log line's text as source other than the new test.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the file were not touched. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot with a real Postgres and a real Express 4 were not run.

## Scope

**These sites only.** Refs {K}; does NOT close it, and introduces no new helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    open(d+'/'+K+'.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
if __name__=='__main__':
    for k in sys.argv[1:]: build(k)
