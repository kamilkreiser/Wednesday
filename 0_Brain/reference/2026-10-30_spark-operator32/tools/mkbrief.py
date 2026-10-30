import sys,os,importlib.util,difflib,json,datetime
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator32'
sys.argv=[sys.argv[0]]+sys.argv[1:]
grp,keys=sys.argv[1],sys.argv[2].split(',')
spec=importlib.util.spec_from_file_location('golden',O+'/tools/golden.py'); 
args=sys.argv; sys.argv=[args[0]]; g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g); sys.argv=args
T=g.T; REL='Blockchain/Dev/services/api-gateway/src/__tests__/'
files={}  # fname -> (orig lines, new text)
for k in keys:
    for f,o,n in g.E[k]:
        if f not in files: files[f]=open(T+f).read()
        orig=open(T+f).read()
        assert files[f].count(o)==1
        files[f]=files[f].replace(o,n)
BR=O+'/../../../2_Project_Files/local-model/night/briefs/ks_1864_'+grp
BR=os.path.normpath('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1864_'+grp)
os.makedirs(BR,exist_ok=True)
golden=''; edits=[]; inputs={}
for f,new in files.items():
    orig=open(T+f).read(); a=orig.split('\n'); b=new.split('\n')
    inputs[REL+f]=orig
    golden+=''.join(l if l.endswith('\n') else l+'\n' for l in difflib.unified_diff([x+'\n' for x in a[:-1]]+[a[-1]] if a[-1] else [x+'\n' for x in a[:-1]],[x+'\n' for x in b[:-1]]+[b[-1]] if b[-1] else [x+'\n' for x in b[:-1]],'a/'+REL+f,'b/'+REL+f,n=3))
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='equal': continue
        if os.environ.get('REBRIEF') and tag=='insert':
            tag,i1,i2,old_,new_='replace',i1-1,i1,[a[i1-1]],[a[i1-1]]+b[j1:j2]
            edits.append((REL+f,tag,i1,i2,old_,new_,a))
        else: edits.append((REL+f,tag,i1,i2,a[i1:i2],b[j1:j2],a))
open(BR+'/golden.diff','w').write(golden)
nE=len(edits); assert nE<=3,nE
nerr=int(sys.argv[3]) if len(sys.argv)>3 else 0
out=[]
w=out.append
now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
fl=', '.join('`'+p+'`' for p in inputs)
w(f"# KS-1864 {grp.upper()} - type-only fixes so the listed api-gateway test file(s) compile under tsc (no behaviour change)\n")
w(f"Files: {fl}\nTip: `a8c554659cb3` (develop)\nRunner: `vitest` (run per file) and `tsc --noEmit -p tsconfig.o32-node.json` (service tsconfig with src/__tests__ included)\n")
w(f"Written {now} from a8c554659cb3, each file read whole.\n")
w("## The mode - read this twice\n")
w(f"TEST-ONLY, TYPE-LEVEL ONLY. Your diff touches EXACTLY {len(inputs)} file(s): {fl}, each modified in place (same path on `---` and `+++`). You never touch any product file (nothing outside `src/__tests__/`), never rename or delete a test, never change what a test asserts.\n")
w("## What is wrong (one paragraph)\n")
w(f"The service tsconfig excludes `src/__tests__`, so the type errors in these test files were never seen. With the tests in the tsc program, `tsc` reports {nerr} error(s) in the file(s) above (measured by tsc 2026-10-30 at a8c554659cb3, identical with `types` set to [\"node\"] and with `types` unset). Each is a typing problem in the TEST code only (a mock or an untyped JSON body or an untyped callback parameter), not a defect in the product. The fix is a cast or an annotation: it changes types only and compiles away, so the test runs exactly as before.\n")
w("## The exact change\n")
for i,(p,tag,i1,i2,old,new,a) in enumerate(edits,1):
    kind='pure insertion' if tag=='insert' else 'replacement'
    ln=i1+1 if tag!='insert' else i1
    w(f"Edit {i} - `{p}`, line {i1+1 if tag!='insert' else i1+1}, {kind}.")
    pre=a[i1-1] if i1>=1 else ''; post=a[i2] if i2<len(a) else ''
    w(f"Context: line {i1} is `{pre}`, line {i2+1} is `{post}` - copy both as context lines (hunk context may be larger; every context line is copied from the file you were given).\n")
    w('```'); 
    for l in old: w('-'+l)
    for l in new: w('+'+l)
    w('```\n')
w("**Do NOT touch** any other line of these files: every `it(...)` title, every `expect(...)` line, every `import` line other than the one edited above, every mock, every fixture. Do not add helper functions, `// @ts-ignore`, `// @ts-expect-error`, `as any` or a `.d.ts`. Do not change `vi.fn()` / `vi.spyOn` calls. The edits above are the whole change; the `+` lines are byte-exact (leading whitespace included).\n")
w("## The test\n")
w("No new test. The checker runs `tsc` (the file's error count must drop to 0, every other file's count unchanged) AND the file's own vitest suite before and after (identical pass count: a type fix must not change behaviour). There is no database / app boot / network beyond what the suite already does.\n")
w("## Cells and controls\n")
CNT={'ks1374-global-limiter-at-demo-limit.test.ts':7,'ks695-ask3-erase-connector-door.test.ts':6,'ks1464-limiter-key-hygiene.test.ts':12,'ks1457-audit-finish-reads-use-the-entry-path.test.ts':9,'ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts':7,'csrf.test.ts':10,'rateLimitEnforce.test.ts':13}
w("- control = every existing test in each file stays GREEN with the same count as at the tip (measured by vitest at the tip): "+'; '.join(f"`{os.path.basename(p)}` {CNT[os.path.basename(p)]} passed" for p in inputs)+".\n")
w("## The failing case (the \"tamper\")\n")
w("Not applicable: a type fix has no red test. The tsc error count is the red/green signal (red at the tip, 0 after).\n")
w("## Premises (each one measured, with where)\n")
w("- The error count and positions come from `tsc --noEmit -p tsconfig.o32-node.json` run in a clone at a8c554659cb3 (read 2026-10-30).\n- Every `-` line above is the line's current text at the tip, counted once in its file.\n- The golden version of these edits was run: tsc errors 0 for these files, vitest pass counts identical to the tip.\n")
w("## UNMEASURED - stated rather than glossed\n")
w("- Whether `eslint` accepts the casts (not run). Whether the same edits compile under the tsconfig of other packages (not run). The service's production build (`tsc -p tsconfig.json`) excludes these files and was not re-run.\n")
w("## Collision\n")
w("- No open PR touches these files (GitHub API list of open PRs, 2026-10-30, planted positive control fired). Attempt count for KS-1864: {'REBRIEF: this is the ONE rebrief of the group (round 1 failed: the model put the inserted line one line too low and the hunk had no trailing context). Edit 1 is now written as a REPLACEMENT of the line above the insertion point (that line is repeated unchanged as a `-` and a `+` line, followed by the new `+` line), so there is no insertion point to misplace.' if os.environ.get('REBRIEF') else (os.environ.get('RB_NOTE') or 'this is the original brief.')}\n")
w("## Scope\n")
w(f"Closes the {nerr} tsc error(s) in the file(s) above; refs KS-1864, does NOT close it (the other test files of the 27 are separate briefs).\n")
w("## Output\n")
w("Exactly ONE fenced diff block, nothing outside it. Paths exactly as the Files: line gives them (`a/<path>` and `b/<path>`). Every `+` line on its own physical line. Every context line keeps its leading space. Count the hunk header from the lines you actually emit."+(os.environ.get('FENCE_LINE') or '')+"\n")
open(BR+'/KS-1864.md','w').write('\n'.join(out))
json.dump({'files':inputs,'keys':keys},open(BR+'/inputs.json','w'))
print(BR,nE,'edits',len(golden.splitlines()),'golden lines')
