# QA gate, round 2 (delta): Secuura Platform K PR #1506 (KS-1489, ratchet hardening, tier 2 tooling + baselines)

- Head gated: `b32e4912c6c7e2976d6cbb4e6fe93a9715e717f2` (bundle `ks1489-b32e4912c6c7.bundle`, sha256/16 `f498b64ea5083122` = builder's figure; `git bundle list-heads` = `b32e4912... HEAD`).
- Round-1 gated head: `767a75dceafa6f4d419fa2c1e03f0a03c79a62b2` (my round-1 verdict sha256/16 `337ad769de67f732`).
- Base named by the builder: develop `c63cec1f6070e06009969526615011dc8734ac13` (= merge-base of the head with the real tip).
- Real develop tip: `bfd42c980891975f7427038754dea8c3097ac267` (`git ls-remote origin refs/heads/develop` in the project dir, read-only; also fetched into my scratch clone as `origin/develop`). Develop is ONE commit past the builder's base (#1509, one gateway test file, ks1204).
- How I got the tree: scratch clone `g1506r2/repo` (local clone of an earlier gate's scratch repo, `--no-checkout`), `git fetch <bundle> HEAD:pr1506`, `git fetch origin develop` using the project's own read deploy key via `core.sshCommand` (read only, into the scratch clone). Merged `pr1506` onto the real tip: commit `ca4b19810ec8`, tree `a9b19869334a65d66873d7598fc3f7651a2692f2` (= builder's predicted `a9b19869334a`). Worktrees of that ONE commit at four spellings: `g1506r2/a` (plain), `g1506r2/Deep.Dir-X/Sub.v2-Aa/long-Name.with.dots/b` ('.', '-', capitals, 4 levels), `g1506r2/via-link` (a symlink to `real-c`), and `real-c` reached through `/tmp/claude-501/...` (macOS `/tmp` -> `/private/tmp`). `node_modules` is a shell of symlinks to the project's installed deps (`tools/nm.sh`, workspace `@secuura/*` re-pointed at each worktree), `packages/shared` built in each (tsc rc 0). Nothing was written under `!CODING` (only `git rev-parse`/`config`/`ls-remote`/`status`/`log`/`show` verbs there; one short-lived bundle read). Node v24.7.0, TypeScript from the project install. Tier: Sonnet-tier independent gate.
- All scratch work: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/eaa04c5f-0a63-4ff7-879d-d52477f7a663/scratchpad/g1506r2/` (tools/, out/). Throwaway fixture roots I made under `/tmp` (`/tmp/a`, `/tmp/ab`, ...) were moved to `g1506r2/_quarantine_tmp/`.

## VERDICT: GO WITH NOTE

The Major is fixed and holds: on one merged commit at four differently spelled paths the auth and gateway checks read 0 new 0 stale rc 0, the regenerated auth baseline is byte-identical at every path, and the new fingerprint 13111132 came out the same across 10 further constructed roots (spaces, `<root>`/`<service>` in the name, `+ ( ) $ [ ] { } ^ .`, `/tmp/a` vs `/tmp/ab`, a root appearing twice in one message), each equal to an independent oracle. Every round-1 Minor and Note that needed action is folded in with a cell that passes (29/29, leg-16 26/0, ks1090 + ks1204 12/12, tsc and eslint clean) and round 1's checker goes red on 8 of the 29 cells.
The note: 3 guards inside `withoutRoots` (the word-boundary lookahead, the `g` flag, the regex escaping) are correct but have NO killing cell (my mutants survive the PR's 29 cells and die against my 10-root harness), so the Major's fix is better pinned for the service dir than for the edge shapes; plus a few documentation/wording inaccuracies. None blocks the merge.

## Round-1 findings: status

| Round-1 finding | Status | Evidence |
|---|---|---|
| 1 Major: auth baseline line 10 TS1192 fingerprint hashed the absolute checkout path | **FIXED** | Raw tsc line still names the checkout (`Module '"<tree>/Blockchain/Dev/services/auth/src/repositories/userRepo"' has no default export.`); normalised `<service>/src/repositories/userRepo` hashes to `13111132` in tree `a` AND tree `b` (my own sha1, `tools/realfp.cjs`) = committed line 10. check.cjs auth/gateway rc 0 at 4 paths (By my runs 2). Regenerated auth baseline byte-identical at all 4 (sha256/16 `b2e97bf543993cb7`). `git diff 767a75dce HEAD -- baseline-auth.txt`: one line changed (`67406236` -> `13111132`). Round-1 checker run on the round-2 tree reads rc 1 on auth (2.5 s runs, `tools/timing.sh`). |
| 2 Minor: fingerprint stability untested, position-free identity pinned only by REAL cell | **FIXED** | Cells "four checkout roots" and "unrelated edit ABOVE an error" in `ks1000...test.ts:289` and `:333`; mutants R1/R3/W5 killed. (The "edit above" cell is green on the old checker too, as the cell's own title says: it pins, not reproduces.) |
| 3 Minor: `@ts-ignore`/`@ts-expect-error` limit not written | **FIXED** | `git grep -n "ts-ignore" -- CLAUDE.md` -> `CLAUDE.md:395`; `check.cjs:46`. Cell at test `:453` pins both names in both files. Probe on the real auth tree: planted `// @ts-ignore` + TS2322 in a non-baselined file rc 0 (stated limit), same plant without the comment rc 1 "1 new" (positive control). |
| 4 Minor: no floor line = silently no floor; second floor line and duplicate key last-wins | **FIXED** | Real auth baseline with the floor line deleted: rc 2 `no "examined-test-files <N>" line`; second floor line rc 2 `p_floor2.txt:33: a second examined-test-files line`; duplicate TS1192 key rc 2 `:33: duplicate entry`. Missing baseline FILE unchanged (treated as empty: rc 1 "42 new" on auth). Mutants R11, R12, R13 killed. |
| 5 Minor: CRLF comment line made the baseline unreadable | **FIXED** | Real auth baseline converted to CRLF (`sed 's/$/\r/'`) -> rc 0, 42/42. Mutant R10 killed. |
| 6 Minor: writers wrote a baseline the reader rejects (space, `#`) | **FIXED** | Cell `:379`, mutant R14 killed; code `check.cjs:165-166`. (I did not run a manual `--init` with a spaced path outside the cell: unmeasured separately.) |
| 7 Minor: four guards without a killing cell (`/m`, `--init`/`--rekey`/`--update` refusing unbaselinable) | **FIXED** | Cells `:389`, `:396`; mutants R15, R16, R17, R18 killed (builder's G4/G6/G7/G9 equivalents also in his table). |
| 8 Note: leg-16 hint text for exits 1 and 2 | **FIXED** | `git diff origin/develop HEAD -- scripts/preflight/test-types-ratchet.sh`: exit-1 and exit-2 strings now name swap/no-file/@ts-nocheck/floor and count-only/no floor line/duplicate; closing hint says "The lines above name the cause". |
| 9 Note: `@ts-nocheck` matcher broader than tsc | **FIXED** (documented) | `check.cjs:52-53`. |
| 10 Note: floor protects only down to its last value | **FIXED** (documented, no action needed) | `check.cjs:48-49`, `CLAUDE.md:395-396`. |
| 11 Note: files outside `__tests__` invisible | **FIXED** (documented) | `check.cjs:51`. |
| 12 Note: develop moved; re-key must be path-independent | **FIXED** | Re-key done on the normalised text; re-gated on the real tip (tree `a9b19869334a`, merge-tree rc 0). |

## By my runs

**1. Bundle, head, base, merged tree, net change.**
- `shasum -a 256 <bundle>` = `f498b64ea508312238fca8a7c2ab3cf304f732b636e455964fcbe4c5ee0cd0bf` (builder: `f498b64ea5083122`). `git bundle list-heads` = `b32e4912c6c7e2976d6cbb4e6fe93a9715e717f2 HEAD`. `git rev-parse pr1506` = same. `git bundle verify` in my clone lists its prerequisites (`88c348375`, `cc2939bb`, ...) as present objects, hash algorithm sha1.
- `git ls-remote origin refs/heads/develop` (project dir) = `bfd42c980891975f7427038754dea8c3097ac267`. `git merge-base pr1506 origin/develop` = `c63cec1f6070e06009969526615011dc8734ac13`. `git merge-tree --write-tree origin/develop pr1506` -> `a9b19869334a65d66873d7598fc3f7651a2692f2`, rc 0 (builder's prediction `a9b19869334a`).
- `git diff --numstat origin/develop HEAD` (merged commit `ca4b19810`): `preflight/test-types-ratchet.sh 5/5`, `baseline-api-gateway.txt 21/16`, `baseline-auth.txt 31/29`, `check.cjs 155/29`, `ks1000...test.ts 365/21`, `CLAUDE.md 10/2` = 6 files, +587/-102 (the builder's figure). `git diff --numstat pr1506 HEAD` = only develop's ks1204 file (10/1): the merge adds nothing of the PR's.
- The two develop merges (`eb8923e`, `b32e491`) did not reintroduce anything: the net diff against the real tip is exactly the PR's 6 files; no conflict markers (`git grep "<<<<<<< "` on scripts and CLAUDE.md: none). The 21 deleted lines in the ks1000 test are fixture adaptations (empty `baseline.txt` -> `ZERO_FLOOR`, direct `path.join`) and the old "Not covered" comment; none weaken a cell.

**2. THE MAJOR (path independence), one merged commit, four spellings (`tools/run2.sh`).**
```
TREE 1 .../g1506r2/a                                   auth: 144 files, 93 under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale  rc=0
TREE 2 .../Deep.Dir-X/Sub.v2-Aa/long-Name.with.dots/b  auth: same line rc=0
TREE 3 .../g1506r2/via-link (symlink)                  auth: same line rc=0
TREE 4 /tmp/claude-501/...(/tmp -> /private/tmp)/real-c auth: same line rc=0
gateway at all four: 149 files, 114 under __tests__; 35 errors: 35 in the baseline, 0 new; 0 stale  rc=0
regen auth (--init --baseline <scratch>) at all four: BYTE-IDENTICAL to committed (b2e97bf543993cb7)
regen gateway at all four: differs from the committed file on ONE line only:  examined-test-files 114 (now) vs 113 (committed)
```
(The gateway line is not a path effect: develop's new test files since the baseline's recording raise the examined count to 114; see Note below.)

*Brute-check, ten further roots + extern packages (`tools/fixture.sh`, `tools/harness.cjs`, `tools/extern.cjs`).* A fixture root (copy of the merged `check.cjs` two levels down, a hoisted `node_modules`, a service-local `node_modules`, 7 test files producing TS1192, TS2305 x2, TS2322 with two `import("/abs/...")` paths in ONE message, TS7016 hoisted, TS7016 service-local, TS2306) built at each root, `--init` run through a path with a trailing slash:
```
roots: /tmp/a | /tmp/ab | "/tmp/sp ace/De v" | /tmp/x<root>y | /tmp/x<service>y | /tmp/<root> | /tmp/<service>/Dev
       | /tmp/p+l(u)s.d$ollar[b]{c}^ | /tmp/Deep.Dir-X/Sub-v2.Aa/b | <scratch>/Deep.Dir-X/Sub.v2-Aa/zz
a.test.ts TS1192  fps=b47db36b acrossRootsIdentical=true equalsOracle=true
b.test.ts TS2305  505d5360 true true      c.test.ts TS2305 9e7f6534 true true
d.test.ts TS2322 (two roots in one message) 977d8ffe true true
e.test.ts TS7016 (hoisted, <root>/node_modules/...) 09f5e4f1 true true
f.test.ts TS7016 (service-local) ed092e17 true true     g.test.ts TS2306 5dafead3 true true
ALL IDENTICAL AND EQUAL TO ORACLE: true         (every init rc 0)
```
The oracle is my own literal-prefix replacer with an explicit boundary test (not the checker's regex). `/tmp/a` and `/tmp/ab` coexist in the list. Same run from a RELATIVE service argument and another cwd (extern.cjs): rc 0.
- *External dirs whose name starts with the root's text* (same package dir, roots `/tmp/a` and `/tmp/q`): `/tmp/ab_ext`, `/tmp/a-ext`, `/tmp/a.ext`, `/tmp/a@ext`, `/tmp/aa`, `/tmp/zz_far`: fingerprint SAME at both roots (the lookahead holds). `/tmp/a+ext`, `/tmp/a~ext`, `/tmp/a ext`: DIFFERENT (a=`f5571983` q=`c686b300`, etc.): see Finding 2.
- *What tsc actually prints.* TS2305 and TS2307 for relative or bare specifiers print the SPECIFIER (`Module '"../repo"' has no exported member 'zz'`, `Cannot find module '../nothere'`), not an absolute path; absolute paths appeared in TS1192 (relative import AND a package-resolved `node_modules/pkg/index`), TS2306, TS7016 (package-resolved, realpath spelling `/private/tmp/...`), and TS2322 `import("/abs/...")`. All were normalised (rows above). So "TS2305/TS2307 print absolute paths" (check.cjs header, CLAUDE.md) is imprecise: Note.
- *Windows / `/private/var`-style symlink spelling.* macOS `/tmp` vs `/private/tmp`: tree 4 above and the TS7016 rows (tsc printed `/private/tmp/...` while I typed `/tmp/...`; handled because `check.cjs` realpaths the service dir, spawns tsc with that cwd, and node realpaths the main module). Windows: SIMULATION only (`tools/win.cjs`, no Windows run): `path.win32.resolve` gives `C:\work\repo\...`, tsc prints `C:/work/repo/...`; the regex does not match (`matched: false`), so on Windows the fingerprint stays path-bound. Not stated in the header; Note.
- *Human-facing output still raw*: NEW-error listing in the swap probe printed `Module '"/private/tmp/col/services/svc/src/y/repo"' ...` (raw); mutant R22 (normalise the displayed text too) is killed by the four-root cell's `toContain(realpath)`.

**3. Conservation (own script `scratchpad/tools/cons.cjs`, per-(file,code) sums; negative controls).**
```
auth     pre (develop) 27 lines, 27 groups, 42 errors | post 27 entries, 27 groups, 42 errors, floor 93, dup 0  -> IDENTICAL, rc 0
         control bump one count:  DIFF auth.integration.test.ts TS6133: 1 -> 2   rc 1
         control drop one group:  DIFF ... 1 -> undefined                        rc 1
gateway  pre 14 lines, 14 groups, 35 errors | post 17 entries, 14 groups, 35 errors, floor 113, dup 0 -> IDENTICAL, rc 0
         control bump: csrf.test.ts TS2345: 10 -> 11 rc 1   control drop: 10 -> undefined rc 1
```
Gateway baseline vs `develop`: NOT byte-identical (`cmp` rc 1): the PR converts it to the fingerprinted format. It IS byte-identical to the file at the round-1 gated head (`git diff --quiet 767a75dce HEAD -- baseline-api-gateway.txt` rc 0), i.e. untouched by this round, which is what the builder claimed.

**4. Cells, round-1 checker, mutants.**
- Merged tree, `ks1000...test.ts` (via `tools/vt.sh`): `Tests 29 passed (29)`. 
- Round 1's `check.cjs` (`git show 767a75dce:...` copied over, run `tools/old.sh`): `29 tests | 8 failed`; the four-root cell fails with `one fingerprint under four roots, got ... TS1192 da3dbd4a | ... 0969a425 | ... e876cb65 | ... f6ac7b49: expected 4 to be 1`; the repo-root ("fake two roots") cell fails (`expected [ 1, ... ] to deeply equal [ 0, ...]`, i.e. the baseline from root A is NOT read at root B); REAL fails; the five round-1 Minor cells and the limits cell fail. `check.cjs` restored (sha256/16 `f59c81b6c85c96b3` before and after).
- Mutants (`tools/mut2.cjs`, each applied alone, whole ks1000 file run, restore compared by sha256): 35 run. 27 KILLED: R1 path not removed, R2 repo root not removed, R3 resolved service dir not removed, R10 CR strip, R11 duplicate key, R12 second floor, R13 no-floor accepted, R14 writer accepts unreadable path, R15 `/m` lost, R16/R17/R18 `--init/--rekey/--update` ignore unbaselinable, R19 fileless diagnostic, R20 floor off-by-one, R21 legacy baseline accepted, R22 displayed text normalised, W2 only the first root applied, W3 service dir not realpathed, W5 position in the hash, W6 message ignored, W7 normalise-after-hash, W8 stale ignored, W9 `@ts-nocheck` off, W10 `--rekey` admits growth, W11 no-test-file exit 2 removed, W12 silent tsc no longer exit 2, N10 unparseable line skipped. `check.cjs` restored byte-identical (sha256/16 `f59c81b6c85c96b3`) after EVERY mutant.
  8 SURVIVED the PR's 29 cells: R4 (typed service spelling dropped), R5 (resolved root spelling dropped), R7 (longest-first sort dropped), W4 (root token same as service token): these I judge EQUIVALENT today (tsc runs with a realpath cwd so a typed spelling is never printed; `DEV_ROOT` comes from node's realpath'd main-module path; the Map insertion order already puts the service dir first; the two tokens never meet), by argument not by a distinguishing run. And R6 (word-boundary lookahead removed), R8 (`g` flag removed: a root twice in one message), R9 (regex escaping removed), W1 (boundary reduced to `\w`): these are NOT equivalent. Proof: my harness against mutated copies (`tools/mutharness.sh`): R8 -> `d.test.ts` (two paths in one message) `fps=fb568859,1a1d47e6 acrossRootsIdentical=false equalsOracle=false`; R9 -> a,d,e,f,g all `false` (roots with `+ ( ) $ [ ] { } ^`); R6 -> extern prefix siblings `/tmp/ab_ext /tmp/a-ext /tmp/a.ext /tmp/a@ext /tmp/aa` all DIFFERENT. The builder's own table (`logs22/mutants1489r2_table.txt`) shows N10 "PATTERN COUNT 0 - NOT RUN" with "ALL MUTANTS KILLED ... False"; the builder's mail says he re-ran it killed; I ran N10 myself: killed. His 28 do not include R6/R8/R9/W1.

**5. Round-1 minors / behaviour change.**
- Cells for each exist (table above). Hint text diff read (Findings table row 8).
- Every existing baseline in the repo: `git ls-files | grep typecheck-tests` -> `baseline-auth.txt` and `baseline-api-gateway.txt` only, BOTH carry `examined-test-files` (93 and 113). Consumers: `git grep` for `check.cjs|typecheck-tests|baseline-auth|check:test-types` -> `package.json:44` (`check:test-types`), `preflight/test-types-ratchet.sh`, `preflight.sh:683-690`, `__tests__/preflight_test_types_ratchet_leg.test.sh`, `__tests__/preflight_deps.test.sh:335-338` (stubs the leg), the ks1000 and ks1090 tests, `CLAUDE.md`. `systemTest/api-explorer/tsconfig.test.json` has no baseline and is not passed to the checker. The only "baseline file without a floor line" fixtures were six of the PR's own ks1000 fixtures (fixed to `ZERO_FLOOR`). I ran every consumer: ks1000 29/29, ks1090 + ks1204 `Test Files 2 passed, Tests 12 passed (12)`, leg-16 suite 26/0, `preflight_deps.test.sh` `56 passed, 0 failed`, `npm run check:test-types` rc 0.

**6. Couplings on the merged tree** (`tools/couple.sh`, `tools/timing.sh`).
- `bash scripts/__tests__/preflight_test_types_ratchet_leg.test.sh`: `preflight_test_types_ratchet_leg: 26 passed, 0 failed`; includes "the default list is BOTH gated services" and "the checker ran exactly twice".
- `npm run check:test-types`: rc 0, 4 runs: 6.69 s, 5.37 s, 5.39 s, 5.43 s. Leg-16 script alone (both services) 3 runs: 5.41, 5.42, 5.26 s.
- tsc: `tsc --noEmit -p tsconfig.json` auth rc 0, api-gateway rc 0.
- eslint on `check.cjs` and the ks1000 test: rc 0; planted `debugger;` control: `1:1 error Unexpected 'debugger' statement no-debugger`, rc 1.
- Cost: bare `tsc --noEmit --listFiles -p tsconfig.test.json` is 2.50-2.55 s (auth) and 2.69-2.71 s (gateway); the round-2 checker is 2.49-2.56 s (auth) and 2.67-2.70 s (gateway); round-1's checker 2.53-2.54 s / 2.66-2.76 s. So the checker itself adds nothing measurable over tsc; the whole leg is now ~5.3 s for BOTH services (round 1: +2.7 s for auth alone, now the second service's ~2.7 s comes with #1507's both-services default, not with this PR's code). Machine was otherwise idle for these runs.

**7. CLAUDE.md.** `CLAUDE.md:385-397` (merged): "Leg 16 gates `services/auth` and `services/api-gateway` (the script's default list), and `npm run check:test-types` runs the same two (KS-1090)". True on the merged tree: `test-types-ratchet.sh` `set -- services/auth services/api-gateway` when no args; `package.json:44` runs both; leg-16 suite cell 26/0 asserts two checker lines. The `@ts-ignore` / `@ts-expect-error` limit is named ONCE (`CLAUDE.md:395`, `git grep -c "@ts-ignore" -- CLAUDE.md` = 1), not contradicted elsewhere in the file; no conflict markers left.

**8. Does normalisation make two DIFFERENT errors collide?** Constructed (`tools/collide.sh`): `src/x/repo.ts` (no default) and `src/y/repo.ts` (default), one test file importing both; baselined (`TS1192 7486622f 1`); then SWAP (fix x, break y):
```
--- unchanged  1 in the baseline, 0 new; 0 stale  rc=0
--- swapped    1 errors: 0 in the baseline, 1 new; 1 stale baseline entry.
  NEW ...a.test.ts(2,8): TS1192: Module '"/private/tmp/col/services/svc/src/y/repo"' has no default export.
  STALE ... TS1192 7486622f: baseline 1, now 0       rc=1
```
Detected. Normalisation only strips the checkout prefix, so two paths collide only if they differ ONLY in that prefix, which is exactly the independence being bought; the `<service>` and `<root>` tokens differ so a service-local and a hoisted package of the same name stay apart (rows e and f: different fingerprints `09f5e4f1` / `ed092e17`). Not a regression against round 1 (round 1 distinguished them by accident of the absolute path). The only new blind spot: two errors in one file with identical normalised text still count as one entry (round-1 Note, unchanged, documented at `check.cjs:50`).

## Findings

**Major: none.**

**Minor**

1. **Three guards in `withoutRoots` have no killing cell, and the PR's mutant set does not aim at them.** `check.cjs:103` word-boundary lookahead `(?![\w.@-])`, the `'g'` flag, and the escape `p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')`. Mutants R6/W1 (lookahead removed or cut to `\w`), R8 (no `g`), R9 (no escape) all PASS 29/29. The code is right (my 10-root harness and extern runs show it) but the Major's fix is pinned only for the service dir and one hoisted-package root; a later "simplification" of the regex would regress path independence for a root with `+ ( [ $`, a sibling dir named like a prefix of the root (`/x/Dev` vs `/x/Dev-old`), or a message naming the root twice, and nothing would go red. Fix: add a cell (or extend the repo-root cell) with a root containing `+(`, a sibling external package at `<root>-ext`, and the two-`import("...")` TS2322 message from `tools/fixture.sh`.
2. **The boundary set misses `~`, `+`, space, and any other non-`[\w.@-]` char**, so an external package dir whose name merely starts with the root's text and then one of those characters (`/tmp/a+ext`, `/tmp/a~ext`, `/tmp/a ext` for root `/tmp/a`) is rewritten to `<root>+ext/...` and its fingerprint then depends on the root (`a=f5571983 q=c686b300` for the same dir). Contrived (needs a package resolved OUTSIDE the checkout at a sibling of it); does not affect the committed baselines (the only absolute-path entry is service-local).

**Note**

3. **Doc inaccuracy.** `check.cjs:26-27` and `CLAUDE.md:396-397` say tsc names the checkout in "TS1192/TS2307/TS2305". Measured: TS2305 and TS2307 print the specifier; the codes that print an absolute path are TS1192, TS2306, TS7016 and the `import("/abs")` form inside TS2322 and similar. The normalisation covers all of them; the sentence just lists the wrong codes.
4. **Windows is not handled and not said**: tsc prints `C:/...`, `path.resolve` builds `C:\...`, the regex never matches (simulation, `tools/win.cjs`). The repo's gate is macOS/Linux; add one line to the header's "does not catch" list.
5. **Stale comment in the ks1000 test** (`ks1000...test.ts:30-33`, added by this PR; absent on develop): "KS-1487 tracks running the checker itself from the pre-push preflight" and "Not covered: the other services" are untrue now that leg 16 runs both services (#1507 and KS-1090). Comment-only.
6. **The api-gateway floor already under-protects by one on the tip**: committed `examined-test-files 113`, merged tree examines 114 (regenerated baseline differs on that one line at all four paths), so deleting one gateway test file passes until someone runs `--update`. Not caused by this PR (round-1 Note 12 said the same); a one-line `--update` in this PR or a follow-up closes it.
7. **A missing baseline FILE is still treated as an empty baseline with no floor** (builder: "unchanged"; I ran it on auth with errors: rc 1 `42 new`). A clean service with no baseline file would pass; I did not run that case (unmeasured), it follows from `check.cjs:138` and `:221` (`base.exists` guards the new exit 2).
8. The builder's mutant-table artefact in the project says `ALL MUTANTS KILLED AND check.cjs RESTORED: False` with N10 not run; his mail says N10 was re-run killed and I confirm it independently (above). The artefact is stale, not the code.

## Not measured

- The real pre-push hook and legs 1-15 on the merged tree; the full vitest suites for auth (93 files) and api-gateway (114 files); `npm ci` (symlinked deps used, as in round 1). Builder reports them green from a fresh worktree; I ran only the ks1000, ks1090 and ks1204 files, the leg-16 and preflight_deps shell suites, tsc, eslint, `check:test-types`.
- Windows, Linux, GitHub-runner paths, Node versions other than 24.7.0; other TypeScript versions or other services' messages (`services/*` other than auth and api-gateway). The Windows behaviour above is a simulation of the regex builder, not a run.
- R4/R5/R7/W4 equivalence is argued, not proven by a distinguishing run. A manual `--init` with a spaced path outside the cell; a clean service with a missing baseline file; the PR body and the CI/board state (read nothing from GitHub).
- A real tsc file-less diagnostic (cannot be produced; pinned by a stub in the PR's cell, mutant R19 killed).
- The merged commit `ca4b19810` is my construction (merge of the bundle head onto the real tip); the tree equals the builder's predicted tree, but the squash commit GitHub will make is not measured.
