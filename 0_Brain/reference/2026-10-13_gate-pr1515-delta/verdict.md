# Gate verdict: Secuura Platform K PR #1515 (KS-1517), fix round 1 delta. OPUS tier, round 1 of 2 under the cap

- Head under test: `79107f316a5b83e053db427dbb81cd0ebd846035` (fetched `refs/pull/1515/head`, matches exactly)
- develop: `4ec53e1874d06636cacc08dd224d980139e5906b` (`git ls-remote origin` at gate time, did not move). develop is an ancestor of the head, so the merge is a fast-forward and cannot conflict.
- Tree: `git clone --shared` of the Blockchain 2_Project_Files into my scratchpad (git verbs run through a python wrapper with its cwd set to the scratch clone), PR head and develop fetched there with the project's core.sshCommand (read only), `git archive` of develop (base), eff6d021 (r0, round-0 head) and the PR head (head), including the repo-root CLAUDE.md. node_modules is a set of symlinks to the main checkout's installed deps, with the `@secuura/*` links relative so they resolve inside MY tree. `packages/shared` is BUILT with tsc in base and head (rc 0, 29 dist entries each). Nothing was written inside !CODING. TypeScript 5.9.3, node 24.7.0.
- Author bundles: delta sha256/16 `2afe15f4155a8104`, full `9b90d4b2626482df`. Both match the stated values and both name HEAD 79107f31. Checker sha256/16: head `c5dc305331f8c8b9`, r0 `597c81dacdaf752b` (matches round 0), develop `f59c81b6c85c96b3`.

## VERDICT: NO GO

Majors: **2** (two classes, five shapes). Both are latent: neither can fire on the shipped repo, as explained below. Both are the same class as the L1 issue that held this PR for a round: a reproducible false exit 2 on a healthy COMPLETE build of a legitimate package, where tsc reads rc 0 and the pre-change checker reads rc 0. Round 0 did not test these shapes. They were already in the round-0 code (r0 also returns rc 2), and the fix round did not reach them. If the coordinator rates latent shapes the way round 0 did (Minor-latent), this reads as GO WITH NOTE. The fixes and a recommended one-move fix are at the end.

## Majors

**M1. The checker picks a typesVersions entry differently from TypeScript. It takes the first match in object order and reads only the `"*"` version range. TypeScript takes the longest-prefix pattern and the first version range that matches.** Code: `check.cjs:199-210` (`mapTargets` returns at the first `k.endsWith('*')` key whose head matches) and `check.cjs:233` (`pkg.typesVersions['*']` only).
- R2: `typesVersions: {"*": {"*": ["dist/*.d.ts"], "sub/*": ["dist/other/*.d.ts"]}}`, `import '@secuura/shared/sub/a'`, `dist/other/a.d.ts` built. tsc rc 0 (traceResolution: "matched pattern 'sub/*'" -> dist/other/a.d.ts). develop checker rc 0. Head checker **rc 2**: "missing declaration target: dist/sub/a.d.ts". With the keys in the other order (R2b), head reads rc 0.
- R3: `typesVersions: {">=4.0": {"thing": ["dist/new/thing.d.ts"]}, "*": {"thing": ["dist/old/thing.d.ts"]}}`, only `dist/new` built. tsc rc 0 (trace: "entry '>=4.0' that matches compiler version '5.9.3'"). develop rc 0. Head **rc 2** on dist/old/thing.d.ts.

**M2. A root import is judged on the raw `types` field. TypeScript maps that field through typesVersions first.** Code: `check.cjs:236` (`sub === '' ? candidates(pkg.types)`).
- R1: `"types": "index.d.ts"`, `typesVersions: {"*": {"*": ["dist/*"]}}`, `dist/index.d.ts` built, `import { R } from '@secuura/shared'`. tsc rc 0 (trace: "Module name 'index.d.ts', matched pattern '*'" -> dist/index.d.ts). develop rc 0. Head **rc 2**: "missing declaration target: index.d.ts (imported as '@secuura/shared')".
- R1b: the same with a literal key, `{"index.d.ts": ["dist/index.d.ts"]}`, `"types": "./index.d.ts"`. Head **rc 2**, tsc 0.

Why these cannot fire today (measured): `packages/shared` is the only package in Dev with typesVersions. It has one version key (`*`) and 23 literal keys, each with a literal `.d.ts` target; all 23 exist after a build. Its `types` is `dist/index.d.ts`, which exists. The trigger is adding a second wildcard key, a version range, or a redirected `types` field to an `@secuura/*` package. That is the same "someone edits shared's typesVersions" trigger as L1. The result would block every seat's leg 16 with a message telling them to rebuild, and rebuilding would not fix it.

## Minors

- **m1. The author's "EQUIVALENT" claim for survivor L1a (extension variants removed) is FALSE.** Shape EQ1 (outside the author's 14 rows): `"f": ["dist/f", "src/f.d.ts"]`, with `dist/f.d.ts` built. tsc 0, head 0, **L1a mutant rc 2** on a complete build. EQ1b gives the same result for `"sub/*": ["dist/sub/*", "types/sub/*.d.ts"]`. The "two guards per fault" argument fails for mixed arrays. The judgeable-skip guard fires only when NO candidate names a `.d.ts`, so in a mixed array the variants are the ONLY guard against a false exit 2, and no cell pins them. Add the EQ1 cell. The redundancy itself is fine; leaving it unpinned is not.
- **m2. The author's "EQUIVALENT" claim for survivor L2b (line-comment ranges not recorded) is also false, but only in the L2 class.** EQ2: `// this subpath is imported from\n'@secuura/shared/thing';` with the target genuinely unbuilt. Head 0, **L2b rc 2**, tsc 0. SPEC's `\s*` spans the newline, so `from` sits in the comment and the quote opens a real string; only `inAny(comments, m.index)` rejects it. On a complete build it is equivalent. My own lexer mutants X2 (an escape consumes 1 character) and X3 (a newline no longer ends a `'`/`"` string) also SURVIVE the suite. Neither is equivalent. X2 is distinguished by EQ3 (`'it\'s'` before an import on the same line, unbuilt: head 2, X2 1). X3 is distinguished by 5 rows (for example a regex `/'/` on the line before an import). Both are false-negative direction. X6 (block-comment ranges not recorded) was equivalent on all 135 of my rows.
- **m3. The position-recording lexer ignores regex literals and JSX text, so some REAL imports escape the precondition.** r0 caught these (it read rc 2); head reads rc 1 NEW. tsc fails with TS7016 on all of them. Shapes (`check.cjs:140-168`):
  - a regex containing `'` on the same line as the import
  - a regex containing a backtick (it opens a template and swallows the following lines)
  - a regex containing `\/\/` on the same line
  - a regex `/\/*$/` (it opens a "block comment" that runs to the next `*/`)
  - JSX text containing a backtick or `/*`
  - `import { X } from /* c */ '@secuura/...'`. This one also escaped at r0: SPEC needs `from\s*['"]`.

  Leg 16 still FAILS on all of them, with the pre-PR misattribution ("NEW type error"), so none produces a silent green. Real-repo survey: across 1284 .ts/.tsx files in services/, packages/ and frontend/, SPEC matches 267 specifiers. The filter drops 49, and I read all 49 by hand: every one is a comment, JSDoc or test-fixture string. **0 real imports dropped.** By the literal FN wording in the brief ("a stale build the precondition cannot see although tsc fails with TS7016") these shapes qualify. I rate them Minor-latent because they occur nowhere in the repo and the leg decision does not move. Coordinator's call.
- **m4. Extensionless and other non-`.d.ts` targets escape by design.** Affected: `dist/sub/*`, `"*": ["dist/*"]`, `dist/e`, `dist/d`, `.d.mts`. When the declaration is genuinely missing, head reads rc 1 NEW and tsc reads TS7016/TS2307. This is the "skip, never guess" contract the coordinator asked for, and it is stated in CLAUDE.md, so it is not a defect. Listed for completeness, because the brief's FN criterion read literally would capture it.
- **m5. Two L2-class cases are still judged when the target is unbuilt (tsc 0, head 2).** A file excluded by tsconfig: the stated limit, as claimed. A plain `require('@secuura/shared/thing')` inside a function in a .ts file: tsc does not resolve it in TS, and this case is not documented.
- **m6. Windows separators in a typesVersions target** (`"dist\\thing\\theThing.d.ts"`, R9). tsc normalizes them and reads rc 0; head reads **rc 2** on POSIX. This is an exotic package.json, so I rate it Minor. By the literal rule it is the same false-exit-2 class as M1/M2. The fix is a one-line `replace(/\\/g,'/')`.
- **m7. Documentation.**
  - CLAUDE.md:409-410 says "Anything the check cannot pin to a literal declaration file (a **wildcard** or extensionless target) is skipped". A wildcard target whose substitution ends in `.d.ts` (`"sub/*": ["dist/sub/*.d.ts"]`) IS judged, and the author's own sibling cell asserts rc 2 on it.
  - check.cjs:102-103 does not say that the first `*` key in object order wins, or that only typesVersions `"*"` is read. Those are exactly M1.
  - "Leg 16's decision is unchanged for every real-service state measured" is accurate as measured (below), and the sentence now correctly says it is not a general claim. It does not mention that M1/M2/m6 shapes would still move pass to fail.
  - The Node10/moduleResolution qualifier is accurate: no `moduleResolution` appears in either service's tsconfig*.json (grep -i rc 1, with a positive control on `"module"` that hit).
- Carried from round 0, unchanged and not in the diff: leg 16's exit-2 `why` text still does not mention a stale build. The checker's own lines above it do.

## What I ran (all measured here)

1. **Topology.**
   - `diff --numstat eff6d021 79107f31`: check.cjs 93/21, ks1000 suite 220/15, CLAUDE.md 9/3. Exactly the claimed 3 files.
   - `diff --numstat develop 79107f31`: 184/0, 245/0, 16/0. Pure additions, so **0 lines of develop's ks1000 suite are dropped**. It is 530 lines by `wc -l` / awk NR, ends in a newline, and `diff dev head | grep -c '^<'` = 0. The author's "531" is off by one; their claim holds.
   - Graph: 980befcf -> merge 551dc98 (eff6d021) -> dad324c0 (fix) -> merge 4ec53e18 (79107f31). Never rebased. develop is an ancestor of the head (`merge-base --is-ancestor` rc 0), so the merge onto develop is a clean fast-forward.
   - The KS-1519 guard cell ("no cell compares a run as one array") passes inside the 57/57.
2. **Real services, complete build.** develop checker vs head checker on services/auth and services/api-gateway: all four rc 0, stdout identical after path normalisation, ZERO note lines (grep -ic note = 0 on all 8 output files). auth 144 files / 93 tests / 42 errors, all baselined, 0 new, 0 stale. api-gateway 150 / 115 / 35 / 35 / 0 / 0. These equal `npm run check:test-types`, both rc 0.
3. **Real arms, api-gateway with the head checker.** Each file was moved aside into my scratch and restored, then re-run.
   - C: rc 0.
   - B: `dist/documents/defaultDocumentType.d.ts` hidden. rc 2: "CANNOT RUN", "missing declaration target: dist/documents/defaultDocumentType.d.ts (imported as '@secuura/shared/documents/default-type')", "rebuild it: npm run build -w @secuura/shared".
   - D: `dist/documents/` hidden. rc 2: the same target, plus an "also missing (runtime only…)" line, plus the build command.
   - A: the `.js` only hidden. rc 0, plus the one-line note.
   - C2: rc 0.
4. **Leg 16** (`scripts/preflight/test-types-ratchet.sh`; not in the diff):
   - head checker, complete build: exit 0, "OK - 2 service(s)".
   - head checker, arm B stale build: exit 1, "FAIL - services/api-gateway … exited 2", with the stale-build message and build command above it.
   - develop checker on an identically built tree with the same file hidden: exit 1, "exited 1: a NEW test-file type error", 2 x TS7016.
   - Same decision, different stated cause, as claimed.
5. **ks1000 suite at head: 57 passed / 57.**
   - Red-first: the head suite against the develop checker gives 7 failed / 50. Against the round-0 checker it gives 8 failed / 49: the 4 L1 complete-build cells, the 3 comment/nested-string cells, and the unpinnable-target-skip cell. So the new cells are live against the code they fix.
   - **Leg-16 shell suite: 36 passed, 0 failed.**
   - **services/auth full suite: 93 files / 1046 tests passed, rc 0.**
   - **eslint** on check.cjs: rc 0. Positive control (`var x = ;` in the same directory): rc 1.
6. **Mutants.** Each was applied to MY scratch check.cjs and scored on `-t KS-1517` (22 cells). The file was restored byte-identical every time; final sha256/16 `c5dc305331f8c8b9`.
   - **All 12 of the author's mutants** (anchors read as data from their mutants1517r2.py): F1-F5, L1b, L2a and S1-S3 KILLED. **L1a and L2b SURVIVE**, which matches their 10/12.
   - My 6:
     - X1 quoteAt off by one: KILLED (7 failed)
     - X4 every array entry must resolve: KILLED
     - X5 candidates() keeps only the first array entry: KILLED
     - X2 escape consumes 1 character: **SURVIVES** (not equivalent, EQ3)
     - X3 newline does not end a string: **SURVIVES** (not equivalent, 5 rows)
     - X6 block-comment ranges not recorded: SURVIVES, equivalent on all my rows
   - **Equivalence check:** every mutant copy was run over my full 135-row table. Results in m1/m2.

## Shape table (complete build unless "unbuilt"; head = 79107f31, r0 = eff6d021, dev = develop's pre-change checker)

| Shape | tsc | dev | r0 | head | Judgement |
|---|---|---|---|---|---|
| comment `//` and `/* */`, mapped target exists | 0 | 0 | 0 | 0 | ok |
| string unmapped; require inside a template; typeof import; import type; export *; dynamic import(); deep subpath not in tv; middle-`*` key; no typesVersions; other @secuura pkg | 0 | 0 | 0 | 0 | ok |
| L1 x4 (trailing-* extless, bare `*`, literal extless, array first absent) | 0 | 0 | **2** | 0 | fixed |
| directory target + index.d.ts; `dist/d/index` extless; array mixing wildcard forms; `.d.mts` target; `typings` field; root `types` array; symlinked declaration | 0 | 0 | 0/2 | 0 | ok |
| L2 line comment / block comment / nested string, unbuilt | 0 | 0 | 2 | 0 | fixed |
| L2 tsconfig-excluded file, unbuilt | 0 | 0 | 2 | 2 | stated limit |
| plain `require()` in a function (.ts), unbuilt | 0 | 0 | 2 | 2 | m5 |
| line comment ending `from` + string next line, unbuilt | 0 | 0 | 2 | 0 | ok (kills L2b) |
| CRLF comment specifier, unbuilt; template-literal specifier, unbuilt; side-effect `import 'x'` | 0 | 0 | 0/2 | 0 | ok |
| **R1 / R1b root `types` redirected by typesVersions** | **0** | **0** | 2 | **2** | **M2 false exit 2** |
| **R2 `*` key listed before a longer `sub/*` key** | **0** | **0** | 2 | **2** | **M1 false exit 2** |
| R2b same keys, longer key first | 0 | 0 | 0 | 0 | ok |
| **R3 version range `>=4.0` before `*`** | **0** | **0** | 2 | **2** | **M1 false exit 2** |
| **R9 backslashes in the target** | **0** | **0** | 2 | **2** | m6 false exit 2 |
| EQ1 mixed array `["dist/f","src/f.d.ts"]` | 0 | 0 | 2 | 0 | ok, but the guard is unpinned (m1) |
| arm C / B / D / A (fixture) | 0 / 7016 / 2307 / 0 | 0/1/1/0 | 0/2/2/0+note | 0/2/2/0+note | as claimed |
| tpl `${}` with quotes; nested template; odd backtick inside `${}`; escaped quote; backslash-newline; `'http://x'` and `'/*'` strings before an import (same line); block comment with quotes; CRLF; BOM; `import … // 'b'`; import = require; export *; multiple per line; dq; `from` newline quote; JSX apostrophe — all unbuilt | 7016 | 1 | 2 | 2 | caught |
| regex `/'/` same line; regex with backtick; regex `\/\/` same line; regex `/\/*$/` (also closed later); JSX text with backtick or `/*` — unbuilt | 7016 | 1 | 2 | **1 NEW** | m3 escape (regression vs r0) |
| `from /* c */ '…'`, unbuilt | 7016 | 1 | 1 | 1 | m3 escape (also at r0) |
| L1-form extless / bare-`*` / dir / `.d.mts` declaration genuinely missing | 7016/2307 | 1 | 1-2 | 1 | m4, by design |
| array with both entries absent; `"*": ["dist/*.d.ts"]` unbuilt; root `types` unbuilt; literal `.d.ts` unbuilt; dangling symlink | 7016/2307 | 1 | 2 | 2 | caught |
| `typesVersions` target missing but the plain subpath `.d.ts` exists (R4) | 2307 | 1 | 2 | 2 | consistent (TS does not fall back) |
| all lexer shapes and the 3 JSX shapes, COMPLETE build | 0 | 0 | 0 | 0 | no false 2 from the lexer |

The complete rows are in my scratchpad (`g1515d/out/edge.jsonl`, `edge2.jsonl`; 135 rows, with each checker's output saved per row). Run 1 and run 2 head/tsc results are identical on the 123 shared rows.

## Recommended fix (one move closes M1, M2, m5 and m6, and is robust against the next unknown shape)

Corroborate with tsc before refusing. The checker already runs tsc. Run it first, and keep the exit 2 only for a specifier whose judged target is missing AND for which tsc reported TS2307/TS7016 naming that module. If tsc resolved it, demote the finding to a note. That keeps "a stale build is exit 2, not NEW" for every true positive measured here. It makes a false exit 2 on a build tsc is happy with impossible by construction, instead of re-implementing TypeScript's resolver one shape at a time.

The minimum point-fixes, if preferred:
- M1: longest-prefix key selection, and select the version range the way TypeScript does (or skip judging when typesVersions has more than the `"*"` key).
- M2: map the root `types` path through typesVersions before judging.
- m6: normalise `\` to `/`.
- Cells: EQ1, EQ2 and EQ3 (they pin L1a, L2b and X2).

## NOT TESTED / NOT RUN
- The full pre-push preflight (16 legs); legs 3, 4 and 8 (need the local stack). Platform suites; the other 26 services' suites; api-gateway's full vitest suite.
- Windows itself (only backslashes in package.json and in a specifier, on POSIX). A CRLF checkout of check.cjs. Services on moduleResolution node16 or bundler.
- A real `npm ci` tree (I used symlinked deps plus a tsc-built shared). A CI container.
- `--update`, `--init` and `--rekey` paths (code unchanged, not in the diff).
- TypeScript versions other than 5.9.3. `--noUncheckedSideEffectImports` (off by default, so tsc ignores side-effect imports, consistent with SPEC not matching them).
- No GitHub or Linear writes; nothing written under !CODING.
