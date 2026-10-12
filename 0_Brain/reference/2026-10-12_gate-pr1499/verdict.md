# QA gate: Secuura Platform K PR #1499 (KS-1487)

- **Head:** `8802326a9a540c99e38dea71bb45fdb6b4418ac8` (from bundle `ks1487-8802326a9a54.bundle`, sha256/16 `93afefe0f97dca3e`, which matches; prerequisite `361537ee`, verified)
- **Base gated against:** current `origin/develop` = `06d33fb4b321c77270ff958f9db6accc5a622da8`. The merge is clean: merge-tree gives tree `e7aae958…`, the same as a real merge in my scratch worktree.
- **Develop delta since 361537ee:** one commit (`06d33fb4b`, KS-1477). It touches **nothing in `scripts/`, `.githooks/` or `.github/`**. It does change `services/auth/src/routes/users.ts` and four auth **test** files, one of them new (277 lines). Those are exactly the files leg 16 type-checks, so I ran the leg on the merged tree: 144 files, 93 under `__tests__`, 42 errors, all 42 in the baseline, 0 new, 0 stale, rc 0.
- Gate: Opus tier, independent, 2026-10-12.

## VERDICT: GO WITH NOTE

Leg 16 does what the PR says. It refuses a planted test-file type error with file, line and TS code. It cannot turn a real red into a skip: in all 9 environment cases I built, a SKIP only happened when leg 1 also refused. All 12 tampers turn the suite red (7 of the author's, 5 of mine). No in-repo consumer of the ratio is hard-coded to 15. There are no Majors. There are two Minors: the new suite goes red in a tree with no install, and the push cost is about twice what the PR claims.

## By my runs

1. **Provenance.** I cloned into the scratchpad (`--no-hardlinks`), pointed origin at `Secuura/Distributed_Secuura`, ran `fetch origin develop` (read-only, rc 0, `40ed3573b..06d33fb4b`) and fetched the bundle. The head is exactly `8802326a9a540c99e38dea71bb45fdb6b4418ac8`, `361537ee` is an ancestor of origin/develop (rc 0), and the diff is 6 files, +288/−17, as claimed.
2. **New suite** `preflight_test_types_ratchet_leg.test.sh`: **23 passed, 0 failed**, rc 0, about 4.9 s. It is also 23/23 on the merged tree.
3. **Repaired suites:** `preflight_deps` 56/56 and `preflight_leg4_sweep_not_run` 5/5, at the head and on the merged tree. The other ratio suites on the merged tree: `failure_verdict_keeps_ratio` 8/8, `ratio_excludes_leg1_no_install` 6/6, `verdict_names_real_failures` 5/5, `state_is_initialised` 5/5. `--check-unreached`: "all 83 tracked shell suite(s) are reached".
4. **Full `run-shell-suites.sh`** at the head, with the workspace install linked read-only from the project checkout: **82/83**. The one failure is `ks949_main_seed_idempotence` ("packages/shared is not built … dist/index.js missing"), which is an environment gap in my clone. With `packages/shared/dist` linked, that suite gives 27/27, rc 0. **Net 83/83, which agrees with the author.** (`evidence_shell_suites.txt`)
5. **Leg on the real baseline:** rc 0, "tsc examined 143 files, 92 of them under `__tests__`; 42 errors: 42 in the baseline, 0 new; 0 stale". On the merged tree (144 files, 93 under `__tests__`) it also has 0 new and 0 stale.
6. **Planted error** appended to `services/auth/src/__tests__/auth.integration.test.ts`: rc 1, with `src/__tests__/auth.integration.test.ts(1637,14): TS2322: Type 'string' is not assignable to type 'number'.` and "FAIL — services/auth … exited 1". I restored the file byte-identical (sha256 `4e0af82b…` before and after), and the clean tree passed again (rc 0). (`evidence_planted_error.txt`)
7. **Skip matrix**, run with the real `test-types-ratchet.sh` and the real `deps-present.sh` (the leg 1 precondition) in a scratch worktree. (`evidence_skip_matrix.txt`)

   | case | leg 16 rc | leg 16 class | leg 1 deps-present rc |
   |---|---|---|---|
   | a. no install | 0 | SKIP | **1** (leg 1 refuses) |
   | b. partial: root tsx present, nested `@types/node` missing | 0 | SKIP | **1** |
   | c. tsx and nested types present, typescript unresolvable | **1** | FAIL (checker rc 2: "cannot resolve typescript/bin/tsc") | 0 |
   | d. full install, `DEPS_PRESENT_ROOT` set to an empty tree | 0 | SKIP | **1** |
   | d2. no install, `DEPS_PRESENT_ROOT` set to a complete tree | **1** | FAIL (rc 2, tsc unresolvable) | 0 |
   | e. tsc exits 1 with no diagnostic | **1** | FAIL (rc 2: "without a single parseable diagnostic") | 0 |
   | e2. tsc exits 0 and lists no files | **1** | FAIL (rc 2: "examined 0 files and NONE under `__tests__`") | 0 |
   | f. full install (control) | 0 | RUN-PASS | 0 |
   | g. full install, `GIT_DIR` and `GIT_WORK_TREE` set to `/nonexistent` | 0 | RUN-PASS (the leg uses no git) | 0 |

   **Every SKIP row has leg 1 at rc 1, and every row where leg 1 passes either runs the checker or FAILs.** Case d is the author's attack point 1, so I drove it end to end. I took the real helpers, the leg-1 block, the leg-16 block and the verdict block from the head's `preflight.sh`, planted an auth test error and exported `DEPS_PRESENT_ROOT=<empty>`. Result: leg 16 is "counted as SKIPPED (advisory)", and the run ends "PREFLIGHT FAILED — but leg 1 could not RUN", rc 1. **The push is refused.**
8. **Tampers.** I re-ran the suite against tampered copies, passed in through `PREFLIGHT_SH`/`LEG_SH`. The product files were byte-identical afterwards. (`evidence_tampers.txt`)
   - The author's tampers, all red: A1 wiring commented out (20/23), A2 script swallows failures (17/23), A3 stops at the first failure (22/23), A4 install precondition removed (22/23), A5 `run_delegated` bypassed (22/23), A6 `TOTAL_LEGS` left at 15 (18/23), A7 missing service treated as OK (22/23).
   - My tampers, all red: G1 rc 2 ("examined nothing") waved through (21/23); G2 rc 2 turned into a SKIP (21/23); G3 leg ignores its arguments and always checks auth (15/23); G4 baseline pointed at a wrong path (21/23, and it fails safe: all 42 errors become "new"); G5 a leg-16 header placed ahead of leg 15 (18/23).
9. **A service path with a space** (`…/svc dir/my svc-error`): the clean fixture gives rc 0 and the error fixture gives rc 1 with the error named. Quoting holds.
10. **New suite in a tree with no install** (a fresh worktree at the head, which is what CI or any fresh checkout sees): **13 passed, 9 failed**. Every behaviour cell that expects rc 1 gets rc 0, because the leg correctly SKIPs. Full runner, no install: head 81/83 (ks949 and the new suite fail); base `361537ee` 81/82 (ks949 only). (`evidence_new_suite_no_install.txt`, `evidence_shell_suites.txt`)
11. **Timing**, measured with the leg script alone:
    - Cold (first run in a fresh clone): 9.1 s.
    - Warm: 2.65, 2.64 and 2.52 s.
    - `deps-present.sh`: 0.02 s.
    - The new suite, which leg 14 also runs on every push: about 4.9 s.
12. **Consumers of the leg count.** I grepped every width (`x/15`, `15 legs`, `TOTAL_LEGS`, `legs ran`, `PREFLIGHT PASSED|INCOMPLETE|FAILED`) across the head tree, `.github/`, `.githooks/pre-push`, the CLAUDE.md files and the WEDNESDAY fleet tools.
    - All in-repo consumers read `TOTAL_LEGS` dynamically. That covers the five ratio suites, the step() header check and the verdict.
    - `.githooks/pre-push` does not parse the ratio.
    - No CI workflow parses it.
    - No live hard-coded 15 was found.

## Findings

**Major: none.**

**Minor 1: the new suite is red in any tree with no workspace install.** Evidence: run 10, "preflight_test_types_ratchet_leg: 13 passed, 9 failed".
- **Cause:** the BEHAVIOUR cells (planted error, empty service, first/last service, missing directory, and the "install present" control) assume an install. With none, `deps-present.sh` fails, the leg SKIPs with rc 0, and those cells read 0 where they want 1. Only the last cell guards that case: "note no workspace install here".
- **Why it does not change any push outcome today:** in such a tree leg 1 already refuses, and leg 14 was already red because of `ks949` (base no-install run: 81/82).
- **Why it is still a defect:** `pr-security-gates.yml` and `security-scan.yml` run `run-shell-suites.sh` with no `npm ci`, only a global tsx. Actions is retired, but those files say they are wired "so a restored CI is correct on day one". This suite breaks that promise in a new way, and it adds a second permanent red to any no-install run of the runner.
- **Fix (one line of intent):** when `deps-present.sh` fails, emit `note`/skip for the BEHAVIOUR cells, as the final cell already does. Better still, give the BEHAVIOUR cells `DEPS_PRESENT_ROOT=<a complete fixture>` and stop depending on the host install. Follow-up ticket; it does not block merge.

**Minor 2: the push cost is understated.** The PR says "about 4 seconds".
- Measured, leg 16 alone: about 2.6 s warm and 9.1 s cold.
- The new suite also runs inside leg 14 on every push: about 4.9 s, which runs tsc once on auth and six times on fixtures.
- So the real added cost per Blockchain/Dev push is about 7.5 s warm and about 14 s cold.
- That is small next to the 414 s shell-suite leg, but the squash body should say so.

**Note 1: a failing leg can also be counted as skipped.** `run_delegated` classifies a leg as skipped if `SKIP (advisory)` appears **anywhere** in its output. check.cjs echoes tsc diagnostic text, which can quote a string literal from the test file. I planted `export const __g: 1 = "SKIP (advisory) — planted";`. Result: leg 16 FAILED **and** was "counted as SKIPPED (advisory)", and the ratio read 1/16 where it should read 2/16. The push was still refused (`PREFLIGHT FAILED on leg(s) 1 16`, rc 1). So the impact is a wrong ratio, not a pass. (`evidence_skip_string_in_diagnostic.txt`.) The matching is older than this PR, but this is the first delegated leg that echoes text controlled by the pusher. A fix would anchor the match to the start of a line from the script itself.

**Note 2: the gated service is named in two places.** The services list lives in the script's default (`services/auth`) **and** in `package.json` `check:test-types`. The comment in preflight.sh says "add it to the script's default list" and does not mention the npm script, so the two can drift.

**Note 3: things inherited from KS-1000 and not changed by this PR.**
- The baseline is keyed by file + code + count. Fixing one TS2322 and adding another in the same file passes.
- The baseline is named by the service directory's basename, so two services with the same basename would share one baseline.
- A missing baseline counts as empty. That fails safe (tamper G4), but it is silent about it. KS-1489 is the place for these.

**Note 4: the hook checks the working tree, not the ref being pushed.** Pushing a branch that is not checked out evaluates the checked-out tree. This is true of every leg and is older than this PR. Leg 16 adds no git calls, so the linked-worktree `GIT_DIR` class cannot affect it (matrix row g).

**Note 5: stale docs.** `Blockchain/Dev/CONTRIBUTING.md:606` still says "N/13 legs ran", and `.githooks/pre-push:157,163` says "13-leg". Both were already stale before this PR (15 legs), and neither is parsed.

**Note 6: CLAUDE.md is accurate.** The new sentence matches the code: `check:test-types` exists in `Blockchain/Dev/package.json:44`, and `--update` refuses to admit anything new (check.cjs:113-118). It names no ratio.

## Fleet consequence

- **Every seat's preflight verdict now reads `N/16`.** An unchanged tree with the stack down reads `13/16 legs ran, 3 SKIPPED` where it used to read `12/15`. That is consistent with the author's real push log ("PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed.").
- **No live tool parses the ratio as a number.** Wednesday's fleet tools do contain the literal `'12/15'`, but only in **26 historical Secuura QA launchers** (`2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_batch1147-1161.sh`, `…1148-1166.sh`, `…1182-1201.sh`, `…922r2.sh`, and others; newest 2026-09-23). They use it as a must-carry word in READY mails and refuse with exit 27 if it is missing. Re-running or copying one of those templates for a new batch would wrongly refuse a mail that says `13/16`. Whoever writes the next Secuura QA launcher should not copy the `12/15` literal.
- **A push touching `Blockchain/Dev/` and adding a test-file type error in `services/auth`** is now refused locally. The message names the file, line and TS code, and the fix hint says `--update` cannot silence it.
- **A docs-only push outside `Blockchain/Dev/`:** the hook exits before the preflight (`[ -z "$changed" ] && exit 0`), so leg 16 never runs. A push touching only docs *inside* `Blockchain/Dev/` runs the full preflight, leg 16 included (about 2.6 s on top of the existing about 7 min).
- **A fresh worktree with no `npm ci`:** leg 1 refuses (as today), leg 16 SKIPs, and leg 14 now has one more failing suite (Minor 1). The verdict stays "PREFLIGHT FAILED" with the npm ci remedy.
- **The merge seat** should quote "13 of 16 legs with 3 skipped (local stack not up), not a full pass" (as the handover already plans) and name this verdict's head.

## NOT tested

- The full real `preflight.sh` end to end. Docker and the stack are down, and I did not run the real pre-push hook. Legs 2–15 were exercised only through the shell suites and the extracted-block harness, not as one run.
- A real `npm ci` install. The install was symlinked read-only from the project checkout (`2_Project_Files`, HEAD `40ed3573`). A lockfile skew between that install and `06d33fb4` is possible; no symptom appeared in leg 16. Leg 1 failed spec-drift inside one harness worktree (`fx`) but passed (`CHECK PASS`) in the main scratch clone at the same head. I attribute that to the harness environment and did not chase it.
- GitHub PR checks for #1499 (no GitHub API use), and the Linux or Ubuntu-VM bash. Everything ran on macOS bash 3.2 with Node from PATH.
- The two remaining author tampers by name ("script skipping even with an install", "header denominator skewed"). They are covered in kind by A4/A5 and A6/G5.
- Services other than `services/auth`; none is gated.
- The platform suites (Schemathesis, Akto, Playwright, k6).
