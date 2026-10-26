# QA gate (tier 2, findings-only), round 1 of 2: Secuura PR #1710 (KS-1551), missing type-check baseline is exit 2

Gate model: claude-sonnet-5-5, row G2. Run 2026-10-26 20:36 to 20:43 AEDT. Findings only: nothing pushed, merged or commented.

## Pins

| | Wednesday's pin (20:36:17) | Start reading (ls-remote, ~20:37) | End reading (ls-remote, 20:43:03) |
|---|---|---|---|
| develop | 444813665a09a5f27b7953009c94ee9fe57beb6b | same | same |
| #1710 head | 8666077d17a666599c8ec972524a5a54338e8379 | same | same |

`git rev-parse HEAD` of the checked-out `pr1710` = 8666077d17a6...; nothing moved.

## BLUF

**GO.** #1710 at 8666077d17a6 does what it claims; no Major, no Minor; two Info notes.

## FOUND

No Major. No Minor.

- **Info 1: vc-issuer floor 17 vs 19 examined, confirmed, out of scope.** Real `services/vc-issuer` examines 19 test files (`--init` on a removed baseline wrote `examined-test-files 19`, `tsc examined 33 files, 19 of them under __tests__`) while the committed `scripts/typecheck-tests/baseline-vc-issuer.txt` records floor 17 (the failing floor message reads "16 examined, examined-test-files 17"). So deleting 1 or 2 vc-issuer test files with the baseline present still passes. This is a pre-existing floor value, not changed by #1710 (no baseline file is in the diff). Not KS-1551's change; worth its own ticket (re-`--update` the floor to 19, reviewed).
- **Info 2: my "old checker" `--rekey` contrast is not a clean red.** In my sequence the old checker's `--update` had already created the baseline, so the old `--rekey` returned rc 2 ("no count-only lines to convert") on an existing file, not on a missing one. The new checker's `--rekey` refusal is proven (rc 2, nothing created, see HOW 2); the old-vs-new contrast for `--rekey` and `--init` is carried by the suite's own cells (see HOW 4), not by my sequence. The old `--update` on a missing file silently created a fresh baseline with floor "none -> 19" and rc 0, which is the exact hole being closed.

Lines read (all at pr1710):
- `Blockchain/Dev/scripts/typecheck-tests/check.cjs` +11/-2: new guard `if (!base.exists && !init) { die(2, \`${baselinePath}: no baseline, so the check cannot be trusted ...\` ... (update ? '--update does not create one: write it with --init.' : 'Write it with --init.')); }` placed after `const base = readBaseline();` and before `if (init) {`. Usage header gains "(missing, ...)" in the exit-2 list.
- `CLAUDE.md:399` old: `... EMPTY baseline, so any type error in its tests is new), and` new: `... EMPTY baseline, so any type error in the program the check compiles, its tests plus the sources they import, is new), and`. `git diff -U0` shows exactly one hunk, `@@ -399 +399 @@`. Nothing else in the file changed.
- `scripts/preflight/test-types-ratchet.sh`: comment-only edits (header :7-8, :19-20, rc-2 reason list adds "missing"); the `why` string for rc 2 adds "missing,". No logic change.

## TESTED

1. **Diff census: PASS.** `git diff --numstat origin/develop...pr1710`: check.cjs 11/2, ks1000 suite 63/0, leg suite 48/9, leg script 7/7, CLAUDE.md 1/1 = 5 files, `130 insertions(+), 19 deletions(-)`. Only path under `typecheck-tests/` is `check.cjs` (no `baseline-*.txt` in the diff). CLAUDE.md single hunk at 399.
2. **Behaviour on real vc-issuer: PASS** (table in HOW 2).
3. **Suites on HEAD: PASS.** ks1000 70/70 (develop 64/64, measured); leg suite 46/0 (develop 43/0, measured); ks1513 5/0; ks1527 4/0; `npm run check:test-types` rc 0 with 5 checker lines; leg default run "OK - 5 service(s) type-check against their baseline."
4. **Condition 3, planted-error cell cannot pass for the wrong reason: PASS** (HOW 4).
5. **Fixture-root claim: PASS** (HOW 5).
6. **vc-issuer floor note:** confirmed, Info 1.
7. **merge-tree: PASS.** `git merge-tree --write-tree origin/develop pr1710` gave tree 8aafeb7be94a6ce19c628e0e36bce445a7eb4d56, rc 0, no conflict lines.

## HOW

Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_v1710_20261026/` (`repo` = `git clone --shared` of the cache `src`, origin and core.sshCommand copied, then `fetch origin develop refs/pull/1710/head:refs/heads/pr1710`). Load1 was 3.07 to 6.5 (< 10). Every suite run used a fresh private `TMPDIR=$(mktemp -d <ws>/tmp.XXXX)`. Install: `npm ci --ignore-scripts` ("added 1806 packages") plus `npm run build --workspace=packages/shared`; `packages/shared/dist/index.js` exists (20634 bytes, written 20:37, fresh). `git status --porcelain` was empty after the install. Scripts used: `beh.sh`, `suites.sh`, `mut.sh`, `dev.sh` in the workspace.

**2. Behaviour (beh.sh), real `services/vc-issuer`, baseline `baseline-vc-issuer.txt` sha256 7df980d8...ad9f7, new check.cjs sha 491449f2...ced5, develop's check.cjs (from `git show origin/develop:...`) sha 458b26cd...ff3d.** Same setup run with each checker swapped into place:

| Setup | HEAD checker | develop checker |
|---|---|---|
| baseline removed, plain run | rc 2, names the baseline file, "no baseline, so the check cannot be trusted" | rc 0 (19 test files, 0 errors) |
| baseline removed, `--update` | rc 2, "--update does not create one: write it with --init.", file NOT created (`ls` -> No such file) | rc 0, "examined-test-files none -> 19", file CREATED |
| baseline removed, `--rekey` | rc 2, names the file, file NOT created | rc 2 but on a file the earlier `--update` had made (see Info 2) |
| baseline removed, `--init` alone | rc 0, "wrote ... (0 errors in 0 entries; examined-test-files 19)", file created | rc 2 "exists: use --update" (file already created by old `--update` in the sequence; sequence artefact) |
| baseline kept + 3 test files removed (control) | rc 1, "16 examined, examined-test-files 17" | rc 1, same |
| baseline removed + 3 test files removed | rc 2, names file | rc 0 (the hole: floor gone with the file) |

Restore: baseline and check.cjs sha256 identical to the start values; the 3 moved test files returned; `git status --porcelain | wc -l` = 0.

**3. Suites (suites.sh, HEAD):** leg suite `46 passed, 0 failed` rc 0; ks1513 `5 passed, 0 failed`; ks1527 `4 passed, 0 failed`; `npm run check:test-types` rc 0, 5 lines starting `typecheck-tests:`; leg default tail `OK — 5 service(s) type-check against their baseline.`; ks1000 via `vitest run --root services/auth src/__tests__/ks1000`: `Tests 70 passed (70)`. Develop control (detached `git worktree` of origin/develop with the HEAD install symlinked in, including every `services/*/node_modules`): ks1000 `64 passed (64)`, leg suite `43 passed, 0 failed`. (First attempt scored 40/3 because my worktree lacked the per-service node_modules symlinks; after adding them it was 43/0, so that was my harness, not develop.)

**4. Condition 3 mutation (mut.sh):** deleted line 156 `baseline_fx "$tmp/ks1487-svc-error"` from the leg suite (the error service left unbaselined). Result `42 passed, 4 failed`. The planted-error cell failed: `want "1 yes yes no", got "1 no no yes"` (leg rc is still 1, which the old rc-only assertion would have passed; the output contained "no baseline" and not `exited 1:` or `a.test.ts`). Dependent cells also went red: "names the error" (want "yes yes", got "no no"), "error in the FIRST service" (want "1 yes yes", got "1 no yes"), and the install-present CONTROL (want "1 no yes", got "1 no no"). Suite file restored from `.bak`, sha256 prefix 4422a76e75c59017 before and after, porcelain 0. Control for the zero: the unmutated suite is 46/0, and the new "NO baseline" cell asserts `exited 2:` + the checker's own line + the file name `baseline-ks1487-svc-nobase.txt`, followed by a CONTROL cell passing once `--init` wrote the baseline.

**5. Fixture root (suites.sh snapshots):** before, after-leg-suite and after-all each read `porcelain=0 tc-files=6 nm-top=987 tc-sha=1d131a8878e1` (porcelain count, entries in `scripts/typecheck-tests/`, entries at `node_modules` top level, combined sha of that directory). Read in the suite: `mkroot` copies the leg, `deps-present.sh` and `check.cjs` into `$tmp/ks1551-root` and does `ln -s "$DEV/node_modules"` and `ln -s "$DEV/packages/shared/node_modules"`; baselines are written by `--init` inside that root; the control cell asserts the repo's `scripts/typecheck-tests/baseline-ks1487-svc-clean.txt` does not exist (it passed).

## NOT TESTED

- The full shell-suite runner (94 tests) and the pre-push hook legs; only the suites named in the brief.
- The rest of services/auth vitest, security and m365-integration vitest, database-backed tests, Docker, the stack, image builds, Node 24 (this machine's Node only).
- The builder's SIGINT/SIGTERM/SIGKILL residue trials (condition 5); not asked of this gate.
- CI checks on the PR (the builder reports mergeStateStatus UNSTABLE, cause unmeasured; I did not read GitHub checks or Linear).
- Old-checker run of the leg suite (builder's "exactly one cell fails" claim); I measured the old checker against real vc-issuer instead.
- Leftover: a detached develop worktree remains at `<ws>/devtree` (my hook refused `git worktree remove` outside the project); it only holds symlinks to the HEAD install and is inside the gate workspace.
