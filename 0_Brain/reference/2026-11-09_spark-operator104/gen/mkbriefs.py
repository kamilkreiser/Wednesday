import difflib, os
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator104/gen/'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
TIP='7eda23b34d3b7a413ca8f9c0945c7843708ce9f4'
SV='Blockchain/Dev/services/auth/src/'
def rd(n): return open(G+n,encoding='utf-8').read()
def dd(p,old,new):
    return 'diff --git a/%s b/%s\n'%(p,p)+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),'a/'+p,'b/'+p,n=3))
def edit(src,lo,hi,newlines):
    L=src.splitlines(True)
    return ''.join(L[:lo-1])+''.join(x+'\n' for x in newlines)+''.join(L[hi:])
# P1
oa=rd('auth.openapi.ts.tip')
na=edit(oa,5,21,[
"// The module is loaded by `src/__tests__/s130-f6-openapi-module-in-the-import-graph.test.ts`,",
"// so a module-scope throw in this file turns the auth suite red (KS-810).",
"//",
"// It was once un-importable from a test:",
"//",
"//   TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function",
"//",
"// because `services/passwordLoginGate.ts` imported `z` from 'zod' directly. The",
"// shared registry requires a consumer to import `z` from '@secuura/shared' so",
"// `extendZodWithOpenApi` lands on the same prototype; the gate file now does.",
"//",
"// The QA2-F4 guard still asserts the GENERATED yaml, which is the artefact a",
"// client generates from, so it is the thing that would ship wrong."])
ot=rd('ks796-f6-mfa-schema-identity.test.ts.tip')
nt=edit(ot,109,124,[
"// ⚠ WHY THIS READS THE GENERATED YAML AND NOT THE SCHEMA OBJECTS. The yaml is the",
"// artefact a client generates from. This guard was written when `auth.openapi.ts`",
"// could not be loaded from a test:",
"//",
"//   TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function",
"//",
"// because `services/passwordLoginGate.ts` imported `z` from 'zod'; the shared",
"// registry requires `z` from '@secuura/shared' so `extendZodWithOpenApi` lands on",
"// the same prototype. KS-810 fixed that: the gate file now imports `z` from",
"// '@secuura/shared', and `s130-f6-openapi-module-in-the-import-graph.test.ts`",
"// imports `auth.openapi.ts`, so a module-scope throw there now turns the suite red."])
p1=dd(SV+'auth.openapi.ts',oa,na)+dd(SV+'__tests__/ks796-f6-mfa-schema-identity.test.ts',ot,nt)
# P2
om=rd('mfa.ts.tip')
nm=om.replace("// MFA_CODE_PATTERN (passwordLoginGate.ts:87), not a second opinion about what","// MFA_CODE_PATTERN (passwordLoginGate.ts), not a second opinion about what"); assert nm!=om
ol=rd('accountLockout.ts.tip')
nl=ol.replace(" * `services/passwordLoginGate.ts:119` (via the gate's own normalisation)."," * `services/passwordLoginGate.ts` (by the gate's own normalisation)."); assert nl!=ol
p2=dd(SV+'routes/mfa.ts',om,nm)+dd(SV+'services/accountLockout.ts',ol,nl)
def brief(tag,title,files,what,change,patch,expect,unm,extra=''):
    d=BR+tag+'/'; os.makedirs(d,exist_ok=True)
    open(d+'golden.diff','w',encoding='utf-8').write(patch)
    fl=''.join('File: `%s`\n'%f for f in files)
    md='''# %s

DRAFT by Spark operator 104 for Wednesday, 2026-11-09 AEDT. Secuura (Platform K) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-2022 (gate 206 N2, Info) ROUND 2 OF 2: this brief SUPERSEDES held READY KS-2022-O102-P1 (round 1 covered 2 of the 4 citations). Counter: original + this one rebrief.

Tier: `doc_only`
Runner: vitest
Tip: `%s`
%s
## The mode
doc_only: a COMMENT-ONLY change. Every changed line is a whole-line comment; no code line changes.
%s
## What is wrong
%s

## The exact change
%s

The whole diff, to copy EXACTLY (the hunk header counts are correct: 3 lines of unchanged context before and after each change, so `git apply` takes it with no fuzz; do not shorten the context, do not recompute the headers):

```diff
%s```

## Expect
%s
## UNMEASURED
%s

## Scope
Exactly the File lines above. Nothing else changes in any file: no other comment, no re-wrapping, no code. The new text is given above verbatim: copy it.

## Output
ONE unified diff in a ```diff fence.
'''%(title,TIP,fl,extra,what,change,patch,expect,unm)
    open(d+'KS-2022.md','w',encoding='utf-8').write(md)
brief('ks_2022_o104_p1_stale_paragraphs_supersedes_o102_p1',
 'KS-2022 round 2, pass 1 (supersedes O102-P1): the two comments that cite passwordLoginGate.ts:55 and describe a zod import the file no longer has (DOC-ONLY: two TypeScript files)',
 [SV+'auth.openapi.ts',SV+'__tests__/ks796-f6-mfa-schema-identity.test.ts'],
 'KS-2022 citations (1) and (2), and the two stale paragraphs KS-810\'s closing comment names (auth.openapi.ts lines 1-21 and ks796-f6-mfa-schema-identity.test.ts lines 110-122). Both say `services/passwordLoginGate.ts:55` imports `z` from \'zod\' and that auth.openapi.ts cannot be imported from a test. At the tip line 55 of that file is a comment, the file imports `z` from \'@secuura/shared\' (line 61), and `src/__tests__/s130-f6-openapi-module-in-the-import-graph.test.ts` imports `../auth.openapi`, so a module-scope throw there turns the auth suite red.',
 'Two edit points, one per file. In auth.openapi.ts replace the 17 comment lines 5 to 21 (the whole "NOTHING IMPORTS THEM YET" paragraph) with 13 comment lines; in the test file replace the 16 comment lines 109 to 124 with 11 comment lines. The new text is in the diff below, verbatim. No line number of another file is cited in the new text.',
 p1,
 "expect_absent: `passwordLoginGate.ts:55` in `%sauth.openapi.ts`\nexpect_absent: `NOTHING IMPORTS THEM YET` in `%sauth.openapi.ts`\nexpect_absent: `passwordLoginGate.ts:55` in `%s__tests__/ks796-f6-mfa-schema-identity.test.ts`\nexpect_present: `turns the auth suite red (KS-810)` in `%sauth.openapi.ts`\nexpect_present: `KS-810 fixed that` in `%s__tests__/ks796-f6-mfa-schema-identity.test.ts`\n"%((SV,)*5),
 'No test run: comments only. Whether the surviving comment text elsewhere in each file is still true (not re-checked beyond the named paragraphs). The claim that s130-f6 turns the suite red on a module-scope throw is KS-810\'s own measured canary, quoted, not re-run.')
brief('ks_2022_o104_p2_mfa_lockout_citations',
 'KS-2022 round 2, pass 2 (supersedes O102-P1): two comments cite passwordLoginGate.ts by a line number that no longer holds (DOC-ONLY: routes/mfa.ts and services/accountLockout.ts)',
 [SV+'routes/mfa.ts',SV+'services/accountLockout.ts'],
 'KS-2022 citations (3) and (4). routes/mfa.ts line 130 cites `passwordLoginGate.ts:87` for MFA_CODE_PATTERN; at the tip it is on line 95. services/accountLockout.ts line 71 cites `services/passwordLoginGate.ts:119` "(via the gate\'s own normalisation)"; at the tip line 119 is `export const MFA_CODE_ACCEPTED = ...`, not the normalisation. A line number drifts every time the file is edited; the file name is enough.',
 'Two edit points, ONE LINE EACH, comment text only. (1) routes/mfa.ts line 130: remove `:87` from the citation. (2) services/accountLockout.ts line 71 (inside the `/** ... */` block above `normaliseEmailForKey`): remove `:119` and change the word "via" to "by" so the expectation below can discriminate. The new text is in the diff below, verbatim.\n\nHARD LIMIT on accountLockout.ts: change ONLY the text of line 71. That file\'s catch blocks, control flow and error handling are NOT to change in any way: not one `try`, `catch`, `if`, `return`, `logger` line or any other code line may appear in the diff, and the diff may touch no line of accountLockout.ts other than line 71 (a fix in those catches can turn the lockout fail-closed into fail-open, gate 131 G131-F5, which is why this pass is a comment and nothing else).',
 p2,
 "expect_absent: `passwordLoginGate.ts:87` in `%sroutes/mfa.ts`\nexpect_absent: `passwordLoginGate.ts:119` in `%sservices/accountLockout.ts`\nexpect_present: `MFA_CODE_PATTERN (passwordLoginGate.ts), not a second opinion` in `%sroutes/mfa.ts`\nexpect_present: `(by the gate's own normalisation)` in `%sservices/accountLockout.ts`\n"%((SV,)*4),
 'No test run: comments only. Whether the "(by the gate\'s own normalisation)" claim itself is accurate is not re-checked (only the line number is corrected). The rest of the mfa.ts comment is unchanged.',
 extra='\n')
print('ok')
