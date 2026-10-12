# Gate verdict: Secuura Platform K PR #1515 (KS-1517), round 2 closing amendment. SONNET tier 3, narrow delta gate

- **Head under test: `a7d0583dd171992d661a725a70659529d3209d5c`.** Fetched as `refs/pull/1515/head` into a `git clone --shared` in my scratchpad (`.../scratchpad/g3/repo`) with the project's `core.sshCommand`; `rev-parse` equals the brief's sha. Previous gated head `6c73effc` (control, "prev"). Nothing was written, checked out or fetched under `!CODING`; no pushes, no GitHub or Linear writes.
- develop: the merged side is `425ad3e0` (ancestor of the head, ancestor of develop now). Develop has since moved to `b08ee629`; I compared against `425ad3e0` (the merge parent) and re-checked topology against `b08ee629`.
- Trees: `git archive` of head, prev (`6c73effc`) and dev (`425ad3e0`), each with a shell node_modules of symlinks to the main checkout's deps, `packages/shared` built with tsc (29 dist entries each). TypeScript 5.9.3, node 24.7.0, vitest per the repo.
- Checker sha256/16: head `458b26cdb851efe0`, prev `c862a80d1b3ace00` (equals the previous gate's recorded head checker, so "prev" is the thing that gate measured), dev `f59c81b6c85c96b3`.
- I read the previous gate's verdict first. I reused its harness (`evidence/tools/`, re-pathed), and added `table5.py` (E, Z, B, Q cells), `table6.py` (null package.json, note-throws plus real verdict), `table7.py` (mutant shapes), `mutants3.py` / `mutants4.py`. Prior-gate numbers are NOT used as evidence; everything below was measured in this run.

## VERDICT: GO WITH NOTE

**Majors: 0. Minors: 5** (none blocks). All four ruled items hold. MJ1's two shapes (G5 huge file, G7a FIFO) no longer crash or hang, a genuine TS2307 and TS7016 still exit 2 for the right reason through the new try/catch, the E1 family no longer exits 2, and C5, the try/catch-removal mutant and the K3 (code-check-and-anchor) mutant are all killed on a green baseline. The note below is: the try/catch fix is real but a catch-body regression (m3) and the C1 mutant (m2) are not pinned by the suite, and the scan still has a bounded superlinear-time shape under the new cap (m1).

## 1. The four ruled items against the previous gate's shapes

Instrument: `harness.measure` runs tsc (`--noEmit --pretty false -p tsconfig.test.json`) and then prev / dev / head checkers on one fixture. Raw rows: `evidence/out/shapes.jsonl` (138 unique shapes; per-shape outputs for the key ones are beside it).

| Shape | tsc | prev (6c73effc) | dev | **head** | Reading |
|---|---|---|---|---|---|
| G5: 16.8 MB file of `''` pairs (8,400,000 pairs), tsconfig-excluded, complete build | 0 | **1 RangeError** | 0 | **0** | MJ1 fixed. The control (prev) fails as the old verdict said |
| G5 original 18 MB (9M starts) | 0 | **1** | 0 | **0** | same |
| G7a: FIFO `src/garbage/fifo.ts`, complete build | 0 | **TIMEOUT 60 s and 150 s** | 0 | **0** | MJ1 fixed; control hangs |
| G7c: FIFO nested `src/garbage/sub/deep/fifo.tsx` | 0 | TIMEOUT | 0 | 0 | fixed |
| G7b: symlink loop, dangling symlink, dir named `dir.ts`, unreadable file, `..` dirlink | 0 | 0 | 0 | 0 | no regression from the new `isFile` guard (symlinks are now skipped rather than followed; harmless for a note) |
| N1: package.json literally `null`, ROOT import, tsc happy (the author's new cell) | 0 | **1 TypeError crash** | 0 | **0** | the try/catch works; control crashes |
| N2 to N5: object / number / array / string package.json, same shape | 0 | 0 | 0 | 0 | |
| E1 (m2): TS2322 quoting `Cannot find module '@secuura/shared/thing'`, thing unbuilt and not imported | 2 (TS2322) | **2 (STALE)** | 1 NEW | **1 NEW** | fixed |
| E1b: same, TS2322 baselined | 2 | **2** | 0 | **0** | fixed (prev refused a push dev accepts) |
| E2: template-literal type quoting the TS7016 phrase | 2 | **2** | 1 | **1** | fixed |
| E4, E5 (echo in an object type; echo in a trailing comment) | 2 | 2 / 1 | 1 | 1 / 1 | fixed |
| E1c: echo on a complete build | 2 | 1 | 1 | 1 | unchanged, correct |

Result: head exit codes are rc 0 / no hang / never CANNOT RUN on every MJ1 and E1 shape, as the author states.

**Cap boundary (item 1, "regular files under a 4 MiB cap").** Two cells with an arm-A (runtime-only) gap so a note should print when the file is scanned: B1 a 4,194,141-byte file holding the only importing specifier -> head prints the note (rc 0). B2 a 4,194,363-byte file -> no note (rc 0). So the cap really skips, and the note is lost for a source file over 4 MiB; B1 is the control showing B2's silence is the cap and not a broken fixture. Accepted by design, listed for completeness.

**Corpus claim.** "Largest real source file is 280,069 bytes": `git ls-tree -r -l` over all `.ts/.tsx/.mts/.cts` at the head (2,042 files; positive control: the count is non-zero and the max file is named) gives 280,069 bytes, `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`. Confirmed.

## 2. The try/catch must not swallow a real tsc-driven verdict

Instrument: same harness. Genuine stale shapes on an imported, unbuilt subpath:

| Shape | tsc | prev | dev | head |
|---|---|---|---|---|
| Z1 genuine TS7016 (declaration alone missing) | 7016 | 2 STALE | 1 NEW | **2, "missing declaration target: dist/thing/theThing.d.ts ... tsc said TS7016 at src/u.ts(1,19)"** |
| Z2 genuine TS2307 (directory unbuilt) | 2307 | 2 | 1 | **2** (same format, tsc said TS2307) |
| Z4 / Z5: Z1 / Z2 plus a 16.8 MB excluded file plus a FIFO in the same tree | 7016 / 2307 | 1 CRASH | 1 | **2 STALE for the right reason** |
| N6: note block THROWS (null package.json, root import) AND a real NEW type error in a test file | 2322 | 1 CRASH | 1 NEW | **1 NEW** (the real verdict survives the catch) |
| N7: note block throws AND a genuine stale `@secuura/crypto` TS7016 | 7016 | 1 CRASH | 1 NEW | **2 STALE naming `@secuura/crypto`** |
| Real api-gateway arm B (`defaultDocumentType.d.ts` moved aside in my scratch tree) | TS7016 | n/a | 1 NEW | **2, CANNOT RUN naming dist/documents/defaultDocumentType.d.ts, tsc said TS7016 at src/routes/verification.ts(20,39)**; restored: 0 |
| Real api-gateway complete | | | 0 | 0 |

Structural reason it holds: `staleFatal` is filled in the `for (const e of errors)` loop BEFORE the `try {` at `check.cjs:346`, and `die(2)` for it runs AFTER the `} catch {` at `:362`. The catch only wraps the note loop. Across the 61 shapes where tsc exits 0 (instrument: `shapes.jsonl`, key `tsc==0`), head never exited non-zero. The instrument can fail: prev produced rc 1 on G5 and N1 and TIMEOUT on the FIFO, on tsc-happy builds.

## 3. Mutants, on a green baseline

Instrument: copy of the head tree (`mut/`), 29 cells scoped by `-t KS-1517` (vitest JSON reporter), anchor asserted to occur exactly once (a count other than 1 prints `ANCHOR COUNT` and skips), restored by bytes with sha256 asserted equal each time. **Baseline: 29/29 green before and after both runs** (`458b26cd`). Logs: `evidence/out/mut.log`, `evidence/out/mutants4.txt`.

| Mutant | Result | Reading |
|---|---|---|
| **C5** corroboration removed, source scan decides before tsc | **KILLED (2 cells)**: the `CORROBORATION one way` cell (R2 fixture) and the null-package.json cell | item (2) proven. Previously C5 survived all 25 cells |
| **T1** try/catch removed (BOTH anchors, so the file stays valid JS) | **KILLED (1 cell)**: `MJ1: a throw anywhere in the NOTE block ...` | right reason: TypeError reaches exit 1 |
| my first T1 (only the `try {` removed, `catch` left) read **26/29 red**: that was a SyntaxError, not a detection. I retract it as evidence and use the valid T1 above (the "read why a red is red" rule) | | |
| **K3** code check AND message anchor both removed | KILLED (1 cell, E1) | E1 pins the pair |
| K1 code check removed, anchor kept | SURVIVED | see m5 |
| K2 anchor removed, code check kept | SURVIVED | see m5 |
| **C1** any module, any code (regex and SPLIT_SPEC widened) | **SURVIVED (0/29)** | m2. Non-equivalent: `thirdparty` with a missing `types` file, tsc TS7016: head **1**, C1 **2** (`table7`, `M_C1_thirdparty_types_missing`) |
| A11 first array target only | SURVIVED | carried from the previous gate; not a ruled item |
| F1 `isFile` guard removed | KILLED (1, the FIFO cell) | |
| C3 on-disk check ignored | KILLED (1) | |
| A9 `*` head off by one | KILLED (2) | |
| S1 size cap removed; S2 cap raised to 64 MiB | SURVIVED | expected and equivalent in behaviour: the try/catch catches the G5 RangeError, and the code comment says the cap exists for out-of-memory, which no cell can test |
| **T2** catch body changed to `process.exit(0)` | **SURVIVED (0/29)** | m3. Non-equivalent: N6 gives head 1, T2 **0** (a real NEW type error lost) |

## 4. Suites at the head, compared with develop

| Instrument | head `a7d0583d` | dev `425ad3e0` |
|---|---|---|
| ks1000 suite (vitest, JSON reporter) | **64 / 64 passed** | 35 / 35 |
| services/auth full vitest (once, quiet machine) | **93 files, 1053 / 1053** | 93 files, 1024 / 1024 |
| `npm run check:test-types` | rc 0: auth 144 examined / 93 under `__tests__` / 42 in baseline / 0 new / 0 stale; api-gateway 152 / 117 / 35 / 0 / 0 | identical numbers |
| eslint on check.cjs and the ks1000 suite | rc 0 | n/a |

Controls: the head-minus-dev delta is exactly +29 tests = the 29 KS-1517 cells (+4 vs the previous gate's 25: the four new ruled-item cells); the `check:test-types` lines show non-zero baselines (42, 35), so they are not vacuous; eslint control `var x = ;` in the same directory gives rc 1 (a parse error), though a plain unused variable would not (lint is parse-level there, as the previous gate also found).

## 5. The develop merge

Instrument: `git diff`, `rev-parse`, `merge-tree` (script `topo.sh`, output `evidence/out/topo.txt`).
- Numstat `6c73effc..0723117b` is exactly the author's: **check.cjs +36/-12, ks1000 +75/-2, CLAUDE.md +15/-6**.
- Blobs: the PR's three files are identical at the head and at `0723117b` (`6babf105b1`, `f76917e4e5`, `77e9cd04df`): the merge did not touch them.
- Develop's three files (`ks1185...test.ts`, `ks1359...test.ts`, `routes/verification.ts`) have the same blob at `425ad3e0` and at the head (`bed106e2eb`, `f6f4269d99`, `ed8003eb50`).
- `git diff --name-only 425ad3e0 head` = exactly the PR's 3 files; `git diff --name-only 0723117b head` = exactly develop's 3 files.
- `git merge-tree --write-tree 425ad3e0 0723117b` = tree `aa04520f2a23...` = the head's tree. The merge is a clean, reproducible recreation. Merge commits, never rebased (all three of `425ad3e0`, `0723117b`, `6c73effc` are ancestors).
- Develop since moved to `b08ee629` (two new files, `platform.ts` and `ks1512...test.ts`, no overlap with the PR); `merge-tree develop-now head` is clean (`2103af45`).

## 6. KS-1546 residue

Not re-gated. Only the question "should anything block?": nothing. X17b, X16, X18, the version-range and TS2792-class shapes are reproduced unchanged in this run (X17b: dev 0, head 2; X16 and X18 head 2) and need a baselined TS2307 or TS7016 that does not exist in either committed baseline, per the code comment's own measurement. The CLAUDE.md and comment text now state this honestly (see minors for the one inaccuracy found).

## Findings

No Majors.

**m1 (Minor). The note scan still has a bounded superlinear-time shape under the cap: a 4 MiB source file of comment + specifier pairs takes about 26 to 39 s, against 0.25 s on develop.** Code: `inAny` at `check.cjs:178`, called per specifier match at `:130`; `lexSpans` collects `comments` as an array and `ranges.some` is a linear scan per match, so the cost is quadratic in the pair count. Shapes: Q1 `//\nfrom'@secuura/shared/thing'\n` repeated to 4,194,269 bytes, tsconfig-excluded: head **25.8 s**, dev 0.25 s (two timings, 26.06 s and 25.82 s). Q2 `//\nrequire('@secuura/a')\n` x 4 MiB: head **39.4 s** (39.46 s and 39.43 s), dev 0.25 s; rc 0 on both. Controls: Q3 to Q5 (4 MiB of `''`, backticks, `/**/`) take 1 s (no specifiers, so `inAny` never runs); the previous gate measured 6 s at 60k pairs, consistent. Not a hang (finishes, rc 0) and not a crash; unreachable on the real tree (largest file 280,069 B scales to about 0.2 s by the same law). It is the residue of MJ1's class, "the note-only scan must not be able to disturb the check", that the cap does not close. Fix-shape: an index/binary search or a moving cursor instead of `ranges.some`, or a smaller cap, or a time budget on the note. Regression test to add: Q1 in the ks1000 suite with an assertion on elapsed time below a generous bound.

**m2 (Minor, test gap). The mutant C1 (judge any package, not just `@secuura/*`) survives all 29 cells.** `check.cjs:294-296` (`SECUURA_IN_DIAGNOSTIC`) and `:297`. Shape: a non-@secuura `thirdparty` whose `types` file is missing, tsc TS7016: head **1** (NEW), C1 **2** (STALE, naming `index.d.ts`). The ruled item (2) asked only for C5, so this is carried, not a regression. A11 (first array target only) also survives, as it did in the previous gate. Test to add: the `thirdparty` shape expecting rc 1 and no CANNOT RUN.

**m3 (Minor, test gap). The try/catch is pinned for "does not throw" but not for "execution continues after it".** Mutant T2 (`catch { process.exit(0); }`) survives 29/29; N6 shows the observable difference (a real NEW test-file type error: head rc 1, T2 rc 0, so a silent pass of a real verdict). Why it matters: the brief's item 2 is exactly "the catch must not swallow a real verdict", and no cell asserts it. Test to add: the null-package.json cell plus a second test file with a real type error, expecting rc 1 and "NEW type errors"; and one with a genuinely stale second package expecting rc 2 (N6, N7).

**m4 (Minor, carried, disclosed by the author). A `null` package.json on the FATAL side still crashes with a TypeError (rc 1, stack trace).** `check.cjs:307` (`pkg.typesVersions` on `null`), reached from the fatal loop at `:327`, outside the try/catch. Shape (G8 null, subpath import `@secuura/shared/thing`, complete build): tsc TS2307, dev rc 1 with a NEW list, head rc 1 with `TypeError: Cannot read properties of null (reading 'typesVersions')`. Same exit code as develop; different, worse message. The suite comment at the new null cell says "a separate, ticketed residual". Fix: `JSON.parse(...) || {}` in `packageJsonOf` (`:303`).

**m5 (Minor, documentation). CLAUDE.md:403 says "Both the code and the anchor are needed".** Mutants K1 (code check removed, anchor kept) and K2 (anchor removed, code check kept) each SURVIVE all 29 cells, so each alone already rejects E1; only K3 (both removed) is caught. The check.cjs comment at `:314-317` ("The anchor and the code each reject it") is the accurate wording. The two guards are redundant for the pinned fixture; a TS2792 shape (message begins `Cannot find module '...'` with a different code) is the only kind of input I can see where the code check alone decides, and no cell uses it. I did not test that shape, so I make no claim about its behaviour.

Nothing else in the diff's wording contradicted what I measured: "Where tsc is happy, it cannot exit 2" holds (61 rows, 0 non-zero); "the note cannot crash it" holds for every shape tried except the fatal-side `null` crash in m4, which the sentence does not claim (it says "the note").

## What I did NOT test

- The full 16-leg pre-push preflight and `scripts/preflight/test-types-ratchet.sh` itself, and its shell suite (`preflight_test_types_ratchet_leg.test.sh`); the previous gate ran them, I did not. Legs 3, 4, 8 need the local stack.
- The api-gateway full vitest suite and every other service and platform suite. I ran services/auth and ks1000 only, plus api-gateway's checker arms.
- `--init`, `--update`, `--rekey` with the new code (the paths are unchanged code; X17b was reproduced only as an information row).
- The other 8 mutants of the author's own set (G2 to G12 style) and the author's runner: I did not run it. I ran my own set of 15 (12 plus T1-valid, K3, T2) on the new anchors.
- A TS2792 or other near-phrase diagnostic (m5), moduleResolution node16 or bundler, Windows or a CRLF checkout of check.cjs, other TypeScript versions than 5.9.3, a real `npm ci` tree or CI container (symlinked deps plus a tsc-built shared package were used, as the previous gate did).
- Worst-case timing beyond Q1 and Q2 (a 21-byte pair would be about 1.1x worse by the same arithmetic, not measured). Timings were taken once under no other load for the repeat and once during other work; both agree to 1.5%.
- Memory behaviour of the scan on a file just under the cap (the code comment claims out-of-memory is not catchable; I did not try to provoke it).
- The residue in KS-1546 (not mine to re-gate), the ts-expect-error/skip semantics, and anything on a running server or box. No GitHub or Linear writes; the project checkout was not written to.

## Self-corrections in this run

- First T1 mutant was invalid (left a dangling `catch`): its 26/29 red was a SyntaxError. Replaced by a two-anchor T1; the valid one kills 1/29 for the right reason.
- My mutant checkers initially lived outside the head tree and exited 2 for "cannot resolve typescript"; those two rows were discarded and re-run from `head/.../typecheck-tests/` (then moved out, head checker sha re-asserted `458b26cdb851efe0`).

Evidence: `evidence/out/` (shapes.jsonl, mut.log, mutants4.txt, topo.txt, suite and arm outputs, key per-shape outputs) and `evidence/tools/` (harness, tables 1 to 7, mutants3/4).
