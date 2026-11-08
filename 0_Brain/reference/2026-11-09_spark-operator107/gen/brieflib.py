# Operator 107 brief generator (code_patch2: product hunks from exact old->new blocks + one NEW vitest/jest test file given whole).
# Shape copied from night/briefs/ks_1868_o96_p8_* and ks_1868_o105_p1_*. Diff is computed by difflib from the tip file (git show), 3 lines context.
import difflib, subprocess, os, sys
SRC='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs'
def tipfile(tip, path):
    return subprocess.run(['git','-C',SRC,'show',f'{tip}:Blockchain/Dev/{path}'],capture_output=True,text=True,check=True).stdout
def make(spec):
    tip=spec['tip']; P=spec['product']; T=spec['test']
    old=tipfile(tip,P); new=old
    for (a,b) in spec['edits']:
        assert new.count(a)==1, ('edit anchor count',new.count(a),a[:80])
        new=new.replace(a,b)
    ol=old.splitlines(keepends=True); nl=new.splitlines(keepends=True)
    d=list(difflib.unified_diff(ol,nl,fromfile='a/'+P,tofile='b/'+P,n=spec.get('ctxn',3),lineterm='\n'))
    d=[x if x.endswith('\n') else x+'\n' for x in d]
    prod_diff=''.join(d)
    first_changed=next(i for i,(x,y) in enumerate(zip(ol,nl),1) if x!=y)
    nhunks=sum(1 for x in d if x.startswith('@@'))
    body=spec['test_body'].rstrip('\n')+'\n'
    tl=body.splitlines()
    test_diff=(f"diff --git a/{T} b/{T}\nnew file mode 100644\n--- /dev/null\n+++ b/{T}\n@@ -0,0 +1,{len(tl)} @@\n"+''.join('+'+x+'\n' for x in tl))
    prod_section=f"diff --git a/{P} b/{P}\n"+prod_diff
    golden=prod_section+test_diff
    key=spec['key']; D=f"{BR}/{key}"; os.makedirs(D,exist_ok=False)
    open(D+'/golden.diff','w').write(golden)
    reds=spec['reds']; ctrls=spec['controls']
    brief=f"""# {spec['ticket']} {spec['title']} (RUNG 3, code_patch2: {nhunks} product hunk(s) given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 107 for Wednesday, 2026-11-09 AEDT. {spec.get('roundtxt','Round 1 of 2 (counter: original + ONE rebrief).')} Secuura ({spec['area']}) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. {spec['origin']} No open PR lists the product file or the new test file name (44 open PRs / 295 file entries read 2026-11-09 through the GitHub API at the start of operator 107; planted control services/originate present in 16 entries). Other sites and files are separate briefs or deliberately skipped.

File: `Blockchain/Dev/{P}`  (product, modified in place: EXACTLY {nhunks} hunk(s))
Test file: `Blockchain/Dev/{T}`  (NEW file, {spec['runner']}, given in full below; {len(reds)+len(ctrls)} cells: {', '.join(c[0] for c in ctrls)} controls, {', '.join(c[0] for c in reds)} red)
Tip: `{tip}` (origin develop; every line number and quote below was read from it)
Runner: `{spec['runner']}` (`{spec['runcmd']}` from `Blockchain/Dev/{spec['rundir']}`)
Tier: `code_patch2`
Rung: **3 ({nhunks} product hunk(s), skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `Blockchain/Dev/{P}` - modified in place: EXACTLY the {nhunks} hunk(s) under "The exact change", byte for byte.
2. `Blockchain/Dev/{T}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{len(tl)} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{spec['wrong']}

## Where

`Blockchain/Dev/{P}`: {spec['where']}

## The exact change

EXACTLY {nhunks} hunk(s) in the product file. The file header lines and the `@@` headers are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). **The product section has FOUR header lines before its first `@@`: `diff --git a/<path> b/<path>`, `--- a/<path>`, `+++ b/<path>`, and only then the `@@` line. A previous attempt left out the `--- a/` and `+++ b/` lines of the product section, which makes the patch unappliable: write all of them (the three lines after the first are shown in the block below; the `diff --git` line is `diff --git a/Blockchain/Dev/{P} b/Blockchain/Dev/{P}`).**

```diff
{prod_diff.replace('a/'+P,'a/Blockchain/Dev/'+P).replace('b/'+P,'b/Blockchain/Dev/'+P)}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any other line of the file, any message text, or any other code.

## The test

File: `Blockchain/Dev/{T}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. {spec['test_note']} The test file contains backslashes, quotes and template strings: keep every character exactly as given.

```diff
{test_diff.replace('a/'+T,'a/Blockchain/Dev/'+T).replace('b/'+T,'b/Blockchain/Dev/'+T)}```

## Red cells
""" + ''.join(f"- RED {spec['tag']} {c[0]}\n" for c in reds) + f"""
## Cells and controls

""" + spec['cells_text'] + f"""
## Premises (each one measured, with where)

{spec['premises']}
- Open PRs: 44 read 2026-11-09 via the GitHub REST API (pulls?state=open, then pulls/N/files); none lists `Blockchain/Dev/{P}` or the new test file (295 file entries; planted control services/originate appears in 16 file entries).

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. {spec['unmeasured']}

## Scope

**These sites only.** {spec['scope']}

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` headers unchanged.
"""
    # the product diff paths in golden must carry Blockchain/Dev/ prefix: rebuild
    gold=golden.replace(f"a/{P}",f"a/Blockchain/Dev/{P}").replace(f"b/{P}",f"b/Blockchain/Dev/{P}").replace(f"a/{T}",f"a/Blockchain/Dev/{T}").replace(f"b/{T}",f"b/Blockchain/Dev/{T}")
    open(D+'/golden.diff','w').write(gold)
    open(D+f"/{spec['ticket']}.md",'w').write(brief)
    open(D+'/spark.pins','w').write(f"# code_patch2: {os.path.basename(P)} ({nhunks} hunk) + a NEW test file; ref = shape only; line = the first changed line.\ntier=code_patch2\nref=Blockchain/Dev/{spec['ref']}\nline={first_changed}\nctx=65536\nstarted_ok={spec['started_ok']}\n")
    print(D, 'hunks',nhunks,'line',first_changed,'testlines',len(tl))
