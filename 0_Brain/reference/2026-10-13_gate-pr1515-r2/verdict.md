# Gate verdict: Secuura Platform K PR #1515 (KS-1517), fix round 2. OPUS tier, DELTA gate, round 2 of 2 under the cap

- Head under test: `6c73effcf9a60279363ac024c77b66ae060372d5`. Read with `git ls-remote` and fetched as `refs/pull/1515/head`; it matches exactly.
- develop: `250596098fa9c2b5e1d5930afeef882143b5f5f1` (ls-remote at gate time; this is the expected value). Merge base `898a1ae11f3c` (KS-1532). develop is NOT an ancestor of the head; see Topology.
- Tree: a `git clone --shared` of Blockchain/2_Project_Files in my scratchpad (`.../scratchpad/g2/repo`). The head and develop were fetched there with the project's `core.sshCommand`, read only. I made five `git archive` trees: `dev`, `head`, `rf` (head plus a swapped checker), `mut` (mutants) and `leg` (leg 16 and the real arms). Each includes the repo-root CLAUDE.md. Each node_modules is a shell of symlinks to the main checkout's installed deps, with the `@secuura/*` links kept relative so they resolve inside MY tree. `packages/shared` was BUILT with tsc in every tree (rc 0, 29 dist entries each). Nothing was written, checked out or fetched inside !CODING. Toolchain: TypeScript 5.9.3, node 24.7.0, vitest 4.1.10.
- Checker sha256/16: head `c862a80d1b3ace00`, develop `f59c81b6c85c96b3`, round 1 (79107f31) `c5dc305331f8c8b9`, which equals round 1's stated value.
- Tier: OPUS, delta gate on fix round 2. The first two gates' results are not used as evidence. Every number below was measured in this run.

## VERDICT: NO GO

Majors: **1**. It is latent and cannot fire on the shipped repo. It is Major only because the brief's rubric names it: "a crash/non-zero from the note-only scanner". The fix is about five lines (below). Without it, this round reads **GO WITH NOTE**. The corroboration design does what it claims on the side that matters most. Across **50** rows where tsc reads rc 0 (122 unique rows measured; 31 of the 50 are package/specifier shapes, including all of my attacks on that property, and 19 are scanner-garbage or package.json rows), the new checker **never exited 2**. Its only non-zero there is the MJ1 crash. The 8 round-0/round-1 complete-build shapes that exited 2 in earlier rounds (R1, R1b, R2, R3, R9, the L1 forms, EQ1) all read rc 0 now. No stale build that tsc fails on exits 0.

## Major

**MJ1. The note-only source scan can crash the checker (exit 1) on a build tsc is happy with. develop reads rc 0.** Code: `check.cjs:155` (`stringStarts.add(i)`), reached from the note loop at `check.cjs:326`, which has no try/catch.
- V8 caps a Set at 2^23 = 8,388,608 entries (measured: `Set maximum size exceeded 8388608`). Shape G5: an 18 MB `.ts` file of `''` pairs under `src/garbage/`, excluded from tsconfig.test.json, with a complete build. tsc 0, develop **0**, head **1**: `RangeError: Set maximum size exceeded at lexSpans (check.cjs:155) ... at sourceSpecifiers (check.cjs:127) ... (check.cjs:326)`. Leg 16 would report this as "a NEW test-file type error".
- Same root cause, a hang instead of a crash. Shape G7a: a FIFO named `fifo.ts` under `src/`. develop rc 0 in under 1 s. Head **hangs** until killed (60 s and 90 s timeouts). The scan walks ALL of `src/` regardless of tsconfig, and calls `readFileSync` on non-regular files (`check.cjs:109-116`).
- Both contradict the code comment at `check.cjs:325` ("It cannot fail the check, so the source scan that feeds it cannot either") and the CLAUDE.md promise that the note cannot fail anything.
- Why it is latent: across all 1,288 .ts/.tsx files under services/, packages/ and frontend/, the most string starts in any one file is **1,464** (`packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`), against the 8,388,608 limit. The largest file is 279 KB. There is no FIFO in any source tree.
- Fix: wrap lines 326-340 in `try { ... } catch { /* the note is advisory: skip it */ }`. In `walk`, skip anything that is not `e.isFile()` and skip files over a few MB. Pin it with one cell: a tsconfig-excluded file under src that makes `lexSpans` throw must still give rc 0.

## Minors (residuals, to be ticketed; each was measured)

- **m1. The suite does NOT pin corroboration, the property this whole round exists for.** Removing corroboration entirely, so the source scan decides before tsc the way round 1 did (my mutant C5), **survives all 25 KS-1517 cells**. C5 exits 2 on R1, R2, R3 and R9, all complete builds with tsc rc 0. The cell "CORROBORATION one way" (ks1000 suite, line 682) cannot catch it. Its fixture (`sub/*` -> `dist/sub/*`, extensionless) is one the resolver ALREADY reads as present through the extension variants. It is green against C5 and green against the round-1 checker c5dc3053. Against round 1, the head suite fails only **1/60**: the `tsc said TS7016` text assertion. So the author's "corroboration pinned both ways" holds for the fail side only. Fix: give that cell the R2 fixture (`{"*":["dist/*.d.ts"],"sub/*":["dist/other/*.d.ts"]}`, with `dist/other/a.d.ts` built). Other survivors, none of them equivalent, each with a constructed shape that tells it apart:
  - C1: any module judged, any code. `thirdparty` with a missing `types` file: head 1, C1 2.
  - C2: TS2307 for any module. `thirdparty/sub` mapped by typesVersions and unbuilt: head 1, C2 2.
  - C4: any mention of an @secuura specifier counts. A TS2322 echo without the phrase: head 1, C4 2.
  - A11: only the first array target consulted. The array-divergence shape: head 1, A11 2.
- **m2. The diagnostic match is text-only, so a diagnostic other than TS2307/TS7016 can exit 2.** Code: `check.cjs:280-281` (unanchored regex) and `:297-304` (the `e.code` check that was removed).
  - E1: a test file contains `export const e: "a" = "Cannot find module '@secuura/shared/thing'";`, and the `thing` declaration is unbuilt but NOT imported anywhere. tsc emits only TS2322: `Type '"Cannot find module '@secuura/shared/thing'"' is not assignable to type '"a"'`. Head **rc 2**: "tsc itself could not resolve the module ... tsc said **TS2322** at src/__tests__/echo.test.ts(1,14)". develop rc 1.
  - E1b: the same, with the TS2322 baselined. develop **0**, head **2**.
  - E2: a template-literal type carrying the TS7016 phrase also gives head 2.
  - This refutes the comment at `check.cjs:298-302` ("no fixture can make it the deciding guard (no other diagnostic carries either phrase)"). It also breaks the invariant "only imported subpaths are judged". Fix: restore `e.code === 'TS2307' || e.code === 'TS7016'`, anchor the regex at `^`, and add E1 as the pinning cell. The trigger is contrived, so this is Minor.
- **m3. A declaration target that is permanently absent is reported as a stale build ("rebuild it"), and rebuilding cannot fix it.** All complete builds:
  - X17: typesVersions names `dist/ghost.d.ts`, which the build never emits. tsc TS7016; develop 1; head **2**.
  - X16: a typo subpath under a catch-all `"*": ["dist/*.d.ts"]`. tsc TS2307; develop 1; head **2** "missing dist/thnig.d.ts". Under a catch-all key every subpath counts as "declared", so the "no declared target -> left to tsc" exemption never applies.
  - X18: the reverse resolver divergence (first-match `*` vs TypeScript's longest `sub/*`). Head **2** names the wrong file.
  - **X17b: X17 with the TS7016 baselined. develop 0 -> head 2 (pass becomes fail).**
  - Why it is unreachable today: both committed baselines hold **0** TS2307/TS7016 entries (positive control: `TS` hits 17 and 27 lines). The real shared package has no catch-all key and every target is built. Head's `--init`/`--update` exit 2 before writing, so a new such entry cannot be admitted. Possible fix: exit 2 only when a rebuild would plausibly help (the target lies under the package's outDir), or demote to a NEW error carrying a "may be stale" hint.
- **m4. Stale builds that still read rc 1 "NEW" (the pre-PR misattribution).** Leg 16 still fails on each of these, so none is a silent pass:
  - X19: version-range key (TS reads `>=4.0`; the resolver reads `*`).
  - Y2: main-only package; sibling `index.d.ts` missing.
  - Y3: deep path, no typesVersions.
  - Y11: directory target unbuilt.
  - Y5b: re-export chain with `skipLibCheck:false`.
  - X2b: a nearer stale copy under `src/node_modules`.

  I judge this acceptable. The design deliberately names only what its resolver can name. Y5, Y5c and Y8 (a nested `.d.ts` missing behind a built entry) read **tsc 0, develop 0, head 0**: tsc itself is happy under `skipLibCheck:true`. That is not a checker regression.
- **m5. Fatal-side crash on an installed @secuura package whose package.json is literally `null`** (`check.cjs:293`, `TypeError: Cannot read properties of null`). rc 1; develop also rc 1 (TS2307). npm would not install such a package. Fix: `JSON.parse(...) || {}` at `:289`.
- **m6. Cosmetic.**
  - One "missing declaration target" line is printed per importing site (real arm B prints the same target twice).
  - "tsc itself could not resolve the module" is printed for TS7016, where tsc did resolve the `.js`.
- **m7. Documentation against what I measured.**
  - CLAUDE.md:399-402 says it "exits 2 only for a module tsc ITSELF could not resolve (TS2307) or could not find a declaration for (TS7016)". m2 shows exit 2 on a TS2322.
  - CLAUDE.md:407 says "A false exit 2 is impossible where tsc is happy, by construction". **Confirmed**: across 50 tsc-rc-0 rows plus the real arms C, A and C2, head never exited 2. It should add that a crash (MJ1) is a non-zero of its own.
  - CLAUDE.md:412-413 says "where it is wrong it can misname a path in a message or stay silent, never refuse a push". X18 shows the resolver being wrong turning a NEW into a confident "rebuild". X17b and E1b refuse a push that develop accepts.
  - CLAUDE.md:414-416 says "a subpath the package declares no declaration target for ... left to tsc". True, but it never applies under a catch-all key (X16).
  - check.cjs:325 is false, per MJ1.
  - check.cjs:102-103 is the stale round-1 "Limit" comment. It still describes judging specifiers and does not say that first-match and `*`-only version reading remain.
  - The author's claim that "the earlier tsconfig-excluded-file limit is gone": **confirmed** (L2 excluded, unbuilt: head 0).
- Carried, not in the diff: leg 16's exit-2 `why` text (`test-types-ratchet.sh:65`) still does not mention a stale build. The checker's own stderr lines above it do.

## What I ran, with results

1. **Topology.**
   - PR files from the merge base: `check.cjs` +241/-0, the ks1000 suite +316/-0, `CLAUDE.md` +18/-0. Exactly the 3 claimed files, all pure additions.
   - develop since the merge base touched only `api-gateway/src/__tests__/ks1185-...test.ts` and `api-gateway/src/routes/verification.ts`. **Zero overlap.**
   - `git merge-tree --write-tree develop head`: rc 0, tree `169e5587`. Its diff against develop is exactly the 3 files, +575/-0. Clean.
   - `health.ts` blob `561de476` is identical at develop and head, as claimed.
   - KS-1519 is intact. develop's ks1000 suite is 530 lines, and `diff dev head | grep -c '^<'` = **0**, so no line of it was dropped. head is 846 lines. The guard cell passes inside the 60/60.
   - check.cjs dev->head is insertions only (hunks `85a86,225`, `118a259,359`), so every line after the new block is byte-identical to develop.
2. **ks1000 suite at head: 60/60 passed.**
   - Red-first against develop's checker: **8 failed / 52**. The failures are the 4 TS7016/TS2307/exports/order cells, the CONTROL-for-three cell, `import type`, the sibling subpath, and the divergence cell (on its `note:` assertion).
   - Against the round-1 checker: **1 failed / 59** (only `tsc said TS7016`). See m1.
3. **services/auth full suite: 93 files / 1049 tests passed, rc 0**, measured on a quiet machine. A first run under concurrent load had 2 timeouts (ks949, s130-f6, both at 5000 ms). Both files re-run alone gave 33/33; the full quiet re-run is clean. This matches the author's ks949-under-load incident.
4. **Leg-16 shell suite** (`scripts/__tests__/preflight_test_types_ratchet_leg.test.sh`): **36 passed, 0 failed.**
5. **Leg 16** (`scripts/preflight/test-types-ratchet.sh`, byte-identical in develop and head):
   - Head, complete build: **exit 0**, "OK — 2 service(s)". auth 144/93/42/42/0 new/0 stale; api-gateway 152/117/35/35/0/0.
   - Head with arm B planted (`dist/documents/defaultDocumentType.d.ts` moved aside): **exit 1**. "FAIL — services/api-gateway ... exited 2: the check could not run", with "CANNOT RUN ... missing declaration target: dist/documents/defaultDocumentType.d.ts ... tsc said TS7016 at src/routes/verification.ts(20,39)" and the build command above it.
   - Same plant with develop's checker: **exit 1**, "exited 1: a NEW test-file type error", with 2 x TS7016 listed as NEW.
   - Restored and re-run: exit 0. Checker sha256/16 `c862a80d1b3ace00` after the swap.
6. **Real api-gateway arms** (files moved aside into my scratch and restored), head vs develop:

   | Arm | Head | develop |
   |---|---|---|
   | C | 0 | 0 |
   | B (declaration only) | **2**, 1 CANNOT RUN | 1 NEW |
   | D (whole dist/documents) | **2**, plus "also missing (runtime only)" | 1 NEW |
   | A (.js only) | **0** plus 1 note | 0 |
   | C2 | 0 | 0 |

   `npm run check:test-types`: rc 0, 0 new, 0 stale on both services.
7. **eslint**: check.cjs rc 0 and the ks1000 suite rc 0. Positive controls: `var x = ;` in the same directory gives rc 1 (parse error); `const x: number = ;` in `services/auth/src/__tests__` gives rc 1. A plain unused variable in a `.cjs` reads rc 0, so lint is parse-level there. I note that rather than claim more.
8. **Mutants** (copy in `mut/`, scored on `-t KS-1517`, 25 cells, JSON reporter). **The unmutated baseline was green (25/25) both before and after the run.** Every mutant was restored by bytes, and sha256 was asserted equal each time (final `c862a80d1b3ace00`).
   - **8 of the author's 11**, with anchors copied verbatim from their `mutants1517r3.py`: G2, G3, G4, G5, G6, G9, G10, G12. **All 8 KILLED** (1, 1, 1, 1, 1, 6, 2, 1 cells).
   - Mine:
     - A9 (`*` head off by one): KILLED (2).
     - A11 (first target only): **SURVIVED**.
     - C1 (any module, TS7016/TS2307): **SURVIVED**.
     - C2 (TS2307 for any module): **SURVIVED**.
     - C3 (on-disk check ignored): KILLED (1).
     - C4 (any mention of an @secuura specifier): **SURVIVED**.
     - C5 (corroboration removed, scan decides): **SURVIVED**.
   - All 5 survivors are shown non-equivalent by constructed shapes (m1).
9. **Shape tables.** Fixtures were built by my own harness (`evidence/tools/harness.py`): a throwaway service with a `tsconfig.test.json` like the suite's, a ZERO-floor baseline, and the package under `node_modules/@secuura/*`. For each shape I ran tsc, develop's checker and head's checker. All rows are in `evidence/out/shapes.jsonl`. The G rows appear twice because one script re-imported another; the results are identical.

### Table 1: the earlier gates' shapes reproduced, with develop's checker as control (25 rows)

| Shape | tsc | dev | head |
|---|---|---|---|
| L1 x4 (trailing-* extless, bare `*`, literal extless, array first absent), dir target, R1, R1b, R2, R3, R9, EQ1 (complete) | 0 | 0 | 0 |
| L2 line comment / block comment / nested string / tsconfig-excluded file, target unbuilt | 0 | 0 | 0 |
| arm C complete | 0 | 0 | 0 |
| arm A (.js missing) | 0 | 0 | 0 + note |
| arm B (.d.ts missing) | TS7016 | 1 NEW | **2** |
| arm D (dir missing) | TS2307 | 1 NEW | **2** |
| R4 (tv target missing, plain `thing.d.ts` exists) | TS7016 | 1 | 2 (true positive) |
| m3 lexer escapes (regex `/'/` same line; `from /* c */ '...'`), unbuilt | TS7016 | 1 | 2 (round 1's escapes are gone) |
| author's divergence cell (named file exists) | TS2307 | 1 | 1 + note |
| non-@secuura TS2307 | TS2307 | 1 | 1 |
| `require()` inside a function (types: []) | TS2591 | 1 | 1 |

Head matches develop on every row except the true positives (B, D, R4, the two m3 rows: rc 1 -> 2) and the arm-A note. This confirms the author's 19/2 claim. On my wider set, the extra differences are also all true positives.

### Table 2: attacks (expected vs actual)

| Shape | tsc | dev | head | Verdict |
|---|---|---|---|---|
| X1 `paths` maps the subpath to a local stub, tv target absent | 0 | 0 | 0 | ok |
| X2 complete copy nearer the importer, service copy stale | 0 | 0 | 0 | ok |
| X2b nearer STALE copy, service copy complete | 0 | 0 | 0 | ok |
| X3 symlinked package complete / stale | 0 / 7016 | 0 / 1 | 0 / 2 | ok |
| X4 ambient `declare module` shim, tv target absent | 0 | 0 | 0 | ok |
| X5 project reference via paths (TS6305) | 2 | 1 | 1 | ok, unchanged |
| X6 sibling-prefix pkg `@secuura/shared-extra` stale | 7016 | 1 | 2 | ok (names the right pkg) |
| X6b `shared-extra` uninstalled | 2307 | 1 | 1 | ok |
| X7 / X7b `@secuura-legacy/thing`, `@secuurax/shared/thing` (non-@secuura lookalikes) | 7016 / 2307 | 1 | 1 | ok |
| X7c `@secuura/jsonly` (no types at all) | 7016 | 1 | 1 | ok (no declared target) |
| X8 / X8b / X8c `import type`, `typeof import()`, `export *`, stale | 7016 | 1 | 2 | ok |
| X9 / X9b `skipLibCheck:false` complete / stale | 0 / 7016 | 0 / 1 | 0 / 2 | ok |
| X10 `noResolve` complete | 2307 | 1 | 1 | ok (target exists: author's error kept) |
| X10b `noResolve` stale | 7016 | 1 | 2 | ok |
| X11 4,000 errors, 8-level x 60-char path, all baselined, complete | 2 | 0 | 0 | ok, no truncation |
| X11b the same, stale | 2322 + 7016 | 1 | 2 | ok |
| X12 `locale` in tsconfig | TS6266 (CLI-only option) | 1 | 1 | ok: locale cannot be set from tsconfig |
| E3 `LANG=de_DE` env | 7016 (English) | 1 | 2 | ok |
| X13 `pretty:true` in tsconfig (CLI `--pretty false` wins) | 7016 / 0 | 1 / 0 | 2 / 0 | ok |
| X14 backslash in the specifier (`@secuura/shared\thing`) | 2307 | 1 | 1 | ok |
| R9 backslash in the tv target, complete | 0 | 0 | 0 | ok (round-1 m6 closed) |
| **E1 TS2322 echoing the phrase, unimported target absent** | 2322 | 1 | **2** | **m2** |
| **E1b the same, baselined** | 2322 | **0** | **2** | **m2** |
| E1c the echo on a complete build | 2322 | 1 | 1 | ok |
| E2 template-literal type echoing the TS7016 phrase | 2322 | 1 | **2** | m2 |
| **X16 typo under a catch-all `*` key, complete** | 2307 | 1 | **2** | m3 |
| **X17 / X17b map names a never-built file (/ baselined)** | 7016 | 1 / **0** | **2 / 2** | m3 |
| X18 reverse divergence, TS's target absent | 2307 | 1 | 2 (names the wrong file) | m3 |
| X19 version range `>=4.0` absent, `*` present | 7016 | 1 | 1 NEW | m4 |

### Table 3: the other side (stale builds)

| Shape | tsc | dev | head |
|---|---|---|---|
| Y1 no exports/tv, root `types` absent | 7016 | 1 | 2 |
| Y2 main only, sibling `index.d.ts` absent | 7016 | 1 | 1 NEW (m4) |
| Y3 deep path `dist/thing/theThing`, no tv | 7016 | 1 | 1 NEW (m4, by design) |
| Y4 nested literal subpath `a/b/c` stale | 7016 | 1 | 2 |
| Y5 / Y5c re-export chain, inner `.d.ts` missing (skipLibCheck true) | 0 | 0 | 0 (tsc happy) |
| Y5b the same, skipLibCheck false | 2307 | 1 | 1 NEW (m4) |
| Y6 `@secuura/crypto` (not shared) stale | 7016 | 1 | 2, "npm run build -w @secuura/crypto" |
| Y7 root `types` mapped through tv, stale | 2307 | 1 | 2 (names `index.d.ts`, the unmapped path) |
| Y8 built, but a nested `.d.ts` the entry imports is missing | 0 | 0 | 0 (tsc happy) |
| Y9 / Y10 extensionless / bare-`*` target unbuilt | 7016 | 1 | 2 (names `dist/sub/a`, `dist/thing`) |
| Y11 directory target unbuilt | 7016 | 1 | 1 NEW (m4) |
| Y12 dangling symlink declaration | 7016 | 1 | 2 |

**No stale build that tsc fails on exits 0.** Across all 122 rows, the only rows where tsc fails and head reads 0 are X11 and X15b. In both, the errors are baselined, and develop also reads 0. Structurally, the round-2 code adds only `die(2)` and stdout notes. It removes nothing from the baseline path (insertions only), so the only way it can produce a silent pass is to not run, and it always runs.

### Table 4: note-only scanner garbage (complete build; garbage under `src/garbage`, excluded from tsconfig)

| Shape | dev | head |
|---|---|---|
| G1 unterminated `'`, template, block comment, trailing backslash, unterminated specifier | 0 | 0 |
| G2 regex/JSX bait (.tsx) | 0 | 0 |
| G3 BOM + CRLF | 0 | 0 |
| G4 binary / invalid UTF-8 / NUL, complete and with the arm-A gap | 0 | 0 (+ note on A) |
| G5b 11 MB, 400k strings + 400k comments | 0 | 0 |
| G6 / G6b 20k / 60k comment+specifier pairs (quadratic `inAny`) | 0 | 0 (1 s / 6 s) |
| G7b symlink loop, dangling symlink, directory named `dir.ts` (mode 000), unreadable file, `..` dirlink | 0 | 0 |
| **G5 18 MB, 9M string starts** | 0 | **1, RangeError crash (MJ1)** |
| **G7a FIFO named `fifo.ts`** | 0 | **hang (MJ1)** |
| G8 package.json oddities (number, exports as string / array / null entries, tv string, main number, types object), C/A/B | as dev, or 2 on B | ok |
| G8 package.json `null` | 1 | 1 via TypeError crash (m5) |
| G8 `typesVersions: {"*": null}` | 2 | 2 (tsc itself crashes; both checkers say "cannot tell") |

## NOT TESTED / NOT RUN

- The full 16-leg pre-push preflight. Legs 3, 4 and 8 need the local stack. The api-gateway full vitest suite, the other services' suites and the platform suites.
- The author's 3 remaining mutants (G7, G8, G11: message-text only), and the author's runner as such. I re-implemented 8 of their 11 from its anchors.
- Windows itself, a CRLF checkout of check.cjs, and services on moduleResolution node16 or bundler.
- A real `npm ci` tree or a CI container (I used symlinked deps plus a tsc-built shared). TypeScript versions other than 5.9.3.
- `--update`, `--init` and `--rekey` with the new code beyond X17b's develop-made baseline. The paths themselves are unchanged code.
- A `tsc` that wraps lines: `--pretty false` is forced on the CLI and I found no tsconfig setting that overrides it. Locale cannot be set from tsconfig (TS6266), and the env LANG has no effect.
- No GitHub or Linear writes. Nothing written, checked out or fetched under !CODING. The only file I read from !CODING beyond the repo was the author's `5_Project_History/2026-10-12_seatV-5th/tools/mutants1517r3.py`, read only.

Evidence: `evidence/out/` (tables, mutant log, leg-16 and arm outputs, crash traces) and `evidence/tools/` (harness, tables, mutant runner).
