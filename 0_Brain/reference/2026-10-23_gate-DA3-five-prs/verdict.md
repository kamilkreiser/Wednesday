VERDICT #923: GO WITH NOTE at head 64fea11d09c2... (tier 2, round 1 of 2; landing tree b0dce3d9281f on develop 95a2dff1d784; 0 blockers, 1 note)
VERDICT #927: GO WITH NOTE at head bc72a2ee543e... (tier 2, round 1 of 2; landing tree 0e042f7e8f27 on develop 95a2dff1d784; 0 blockers, 1 note)
VERDICT #1253: GO at head 8f71eaf1b8c3... (tier 2, round 1 of 2; landing tree d9ff9184f209 on develop 95a2dff1d784; 0 blockers, 0 notes)
VERDICT #809: NO GO at head 736442fa9158... (tier 2, round 1 of 2; landing tree 0a79f5c60fbe on develop 95a2dff1d784; 1 blocker, 1 note)
VERDICT #920: GO WITH NOTE at head f62c0767f039... (tier 2, round 1 of 2; landing tree 50691f173c96 on develop 95a2dff1d784; 0 blockers, 2 notes)

# Gate DA3 verdict (Sonnet, tier 2, round 1 of 2), 2026-10-23

## BLUF
- **#809 is NO GO, and it is a real one.** It writes `checks.not_a_server_error.enabled = false` on seven operations. Develop's own toml header (KS-1170, 2026-09-15) says that exact key is DEAD under an explicit `--checks` list on Schemathesis >= 4.26.1, and develop has unit tests that red on it. Run through the project's own helper functions, the PR head fails two of them and develop passes them. The PR was written before KS-1170 and the merge-in did not notice. Fix is to express the seven as `expected-statuses = ["2xx","3xx","4xx","503"]` (the neighbouring entries' shape). I applied that in a scratch copy and the same checks went clean. I did not commit or push anything.
- #923: the hardening works against the mutants the author names, but the new "behavioural leg" is WEAKER than the old check for one class (details below). Note, not blocker.
- #927: passing runs do not reach the new branches (author is honest about that); I drove both with a forced `cp` failure and the stash is kept and named. Note: exit code stays 0 after a failed restore.
- #1253: GO. 6 -> 12, four mutants all redden by assertion.
- #920: refusal is real (rc 1) and narrows correctly when the deps are installed. Two gaps in the "ready" path (notes).
- Scope and merge integrity are clean for all five (section A). No PR changes product runtime behaviour: all five stay tier 2.

## A. Scope and merge integrity (all five)
- `git ls-remote` of develop and the five PR heads at start and at end: identical, and equal to the brief's table (develop 95a2dff1d784974061c547a291833006c361b703).
- Each head's diff vs develop is exactly the listed files (1 / 2 / 1 / 2 / 7). The file sets are pairwise disjoint. (#920's `package.json` is `Blockchain/Dev/package.json`, not a repo-root one; the brief's wording "root" means Dev root.)
- Landing trees derived by `git merge-tree --write-tree` against live develop equal each head's own tree, all five: b0dce3d9, 0e042f7e, d9ff9184, 0a79f5c6, 50691f17 (match the author's).
- Parents: 923, 927, 1253, 920 are `[old head, develop]`. 809's head is a single-parent fix commit on top of merge `2272a3986d62` whose parents are `[aa2270fe14cf, develop]`.
- Line-multiset check (PR's own +/- lines on its files, before the merge vs against develop after): identical for 923 (153), 927 (76, both files, develop also rewrote them), 1253 (261), 920 (265). For 809 the merge-in alone is identical too (checked on `2272a3986d62`); the fix commit then differs by exactly the five edits it claims (3 lines in, 11 out): "eight" to "seven" in two comments, the `connections/complete` frozenset entry removed, its toml block removed, and the duplicate webhook-config block replaced by one added line in the existing block. Nothing else.

## #923 (KS-736)
FOUND / TESTED / HOW
- Re-ran the file on develop and on head (vitest 4, api-gateway, `npm exec --prefix`, deps installed inside my clone): 5 passed -> 5 passed, same five names.
- Mutant M1: `/api/stake` `authenticateToken(true)` changed to `authenticateToken(false)` in `proxy.ts`. New test: RED by assertion (`every /api mount either requires auth...`: "Unauthenticated /api mount(s) with no recorded reason"). OLD test on the same mutant: 5 passed, GREEN. So the old check would have stayed green, as the author says.
- Mutant M2: delete the `authenticateToken(true)` line from `/api/stake`. New: RED. Old: RED. Both detect a plain skip.
- Restore asserted by sha256 of `proxy.ts` (5372064b8cba7758 before and after each).
- **NOTE (a hole the new test opens that the old test did not have).** Mutant M3: delete the `authenticateToken(true)` line (443) from the `/api/webhooks` mount. NEW test: 5 passed, GREEN. OLD test: RED naming `/api/webhooks`. Why: the new "leg 2" scores a mount as authenticated if any non-final handler answers >= 400 to a headerless request, and `/api/webhooks` still carries `attachScopes` and the real `requireScope('webhooks:manage')`, which refuses an anonymous request. So a mount can lose `authenticateToken` (and with it the gateway's session-revocation check, the KS-570 header's own concern) and still score "authed" whenever another guard on the mount refuses anonymous callers. The PR closes one false-green (`(false)` scored as auth) and opens this one. I did not count how many real mounts fall in the class. It is a test-sensitivity regression, not a runtime change, so a note; Wednesday may want it ruled as accept or as round-2 work.

## #927 (KS-1027)
- Develop vs head: `pre_suite` 28 -> 28, `quarantine_call_sites` 17 -> 17, rc 0, no failed; the `ok` cell lists are identical by name (one line differs only by a random stub port number in a harness cell).
- Branches driven (the author's claim that passing runs miss them is right). I put a fake `cp` first on PATH that fails only when the destination is `.../generated/` (restore) or `.../stash/` (snapshot), and passes through otherwise; `FAKE_MODE=none` is the positive control (rc 0, no `!!` lines).
  - Forced restore failure, head: both suites print `KS-1027: restoring ... FAILED — it may now be EMPTY` and `the snapshot is KEPT at: <tmp>/stash`. With a sentinel file placed in `generated/`, the kept stash contains it and `generated/` was left empty, so the message is true and the copy is recoverable.
  - Forced snapshot failure, head: `KS-992 ... FAILED` plus `KS-1027: the partial snapshot is KEPT at: <path>`. On develop the same fault prints only the KS-992 lines and the temp dir is deleted: the behavioural difference the PR claims is real.
- **NOTE:** after a failed restore the suite still exits rc 0 (the report is stderr only). A caller that checks only the exit code never learns `generated/` may be empty. The ticket asks for non-silence, which is met on stderr; flagging for completeness.
- The kept stashes were moved into my scratch dir (no files left in /var/folders from my runs beyond what the suites' own `mktemp` did before I moved them).

## #1253 (KS-1297)
- Develop 6 passed -> head 12 passed, rc 0; the first six names are identical, 0 vanished, six new ones (NB-1218-a, -b, -c, CONTROL, R2 five-shapes, R2 CONTROL).
- Mutants (each asserted applied by `git diff --stat`, restore asserted by sha256 of both files):
  - M1 subject `build_fixture` call wrapped as `( ... )`: cell 9 (`NB-1218-c`) RED, plus cell 10 control and the two pre-existing cells that rely on a real abort; 7 passed / 5 failed.
  - M2 subject call given a trailing `| cat`: same 5 reds (this is the shape round 1's blacklist missed).
  - M3 widened `repo_state` reverted (status/ls-files lines removed): `NB-1218-b` RED by assertion; 11 passed / 1 failed.
  - M4 `T1_NAMED` anchor loosened: `NB-1218-a` RED; 11 passed / 1 failed.
- Cosmetic only, no note counted: a cell-9 comment says "12 bare call sites", the cell itself measures 14; the "one line of context" bound is declared in the comment.

## #809 (KS-693 interim) — read hardest
The static items the brief listed all pass:
- Both files parse (`ast`, `tomllib`, Python 3.14.5, `-I`). `connections/complete` appears 0 times in either file.
- Exactly one `POST /api/teams/webhook-config` toml entry, carrying both `positive_data_acceptance` and `not_a_server_error.enabled = false`. 49 toml entries, 21 frozenset entries, no duplicates in either; every frozenset entry has a toml entry and vice versa.
- Each of the seven POST operations is in `docs/openapi/secuura-api.yaml` with a declared 503 (all list 503 among 500/502/503); `POST /api/m365/connections/complete` is ABSENT from the spec, as the fix says. All seven service routes in `m365-integration/src/index.ts` carry `requireM365`.
- Stale comment: confirmed. `index.ts:229` is not the gate; the gate is `requireM365` at line 261, with `if (!isConfigured())` at line 262. The PR's comment (in both files) still says 229. **NOTE** (stale line reference only), also because a comment citing a file:line in a different service file than the one it lives next to ages fast.

**BLOCKER.** The seven entries use `checks.not_a_server_error.enabled = false`, and that is the key develop declares dead.
- Evidence in develop's own `schemathesis.toml` (lines ~338-342): "KS-1170 (2026-09-15) ... These entries used to read `checks.not_a_server_error.enabled = false`. Schemathesis 4.26.1 made an explicit `--checks` list mark the check EXPLICITLY ENABLED, and that marker wins over a per-operation `enabled = false`." Every existing 503 entry on develop uses `expected-statuses = [..., "503"]` instead.
- Develop has tests that pin this: `tests/unit/checks/test_integration_5xx_guard.py` (`test_the_dead_disable_key_is_not_reintroduced` and `test_every_guard_entry_tolerates_503_in_the_toml`, plus the two lockstep tests).
- I ran the project's own helper functions from `tests/support/by_design_tolerances.py` (`operations_tolerating`, `operations_still_using_enabled_false`) on the toml and the frozenset parsed from `check_predicates.py`, WITHOUT pytest (conftest guard blocks on this machine's 3.14.5). Control, develop: frozenset 14, toml tolerates 503 on 14, orphaned [], enabled=false ops []. PR head: frozenset 21, toml tolerates 503 on 14, **orphaned = all seven new ops, `enabled=false` ops = the same seven**. Those are exactly the two assertions above, so the unit suite (NOT RUN as such) would be red on this head and the CI/pre-push gate that runs it would refuse the PR. Positive control from another angle: in a scratch copy, rewriting the seven lines to `expected-statuses = ["2xx","3xx","4xx","503"]` makes the helper report 21/21, orphaned [], enabled=false [] (restored by sha256).
- Net: as written, the seven declared 503s would not be tolerated at run time on current Schemathesis, so the PR does not deliver what KS-693 asks, and it contradicts the repo's own gate. The fix commit (`736442fa`) went through the hook with no check, which is how this got past: the author's STATIC list checked parse/duplicates/spec membership but not the lockstep helpers.
- Not run: the pytest suite itself, the live 503 claim (no stack).

## #920 (KS-734)
- Dependency/lockfile lines: 0. The diffs to root (`Blockchain/Dev/package.json`) and `tests/e2e/package.json` add only scripts (`e2e:install`, `e2e:check`, `e2e`, `check:ready`, `pretest`, `playwright:install`); no `package-lock.json` is in the file list.
- Refusal is real. In my clone (no e2e deps): `node check-e2e-ready.mjs` -> rc 1, stdout empty, stderr names `@playwright/test, otplib` as not installed and that `playwright` cannot be resolved. After `npm ci --ignore-scripts` of `tests/e2e` inside the clone, with `PLAYWRIGHT_BROWSERS_PATH` pointed at an empty dir: rc 1, now naming only "the chromium browser binary is missing (expected at ...)". Same on this machine's default path. So the check separates the two gaps rather than always saying the same thing. (On this clone the message differs from the author's "otplib and Chromium" because my clone has no hoisted root install; the logic is the same.)
- "Ready" path, read plus driven:
  - **NOTE 1:** the browser check is `existsSync(chromium.executablePath())`. With a zero-byte, non-executable file at that path the script printed OK and rc 0. A truncated or non-runnable download passes. Also it checks chromium only, while the `mobile` project uses `devices['iPhone 13']`, whose `defaultBrowserType` is webkit (measured), and `e2e:install` installs only chromium. A mobile run on a fresh checkout would pass this gate and then fail.
  - **NOTE 2:** `global-setup.ts` now calls the same check for every project, so an API-only run (`--project=api`, which needs no browser) is refused when chromium is absent. Read from code, not run. Also, the dependency check is `require.resolve` of three declared names: presence, not version.
  - Neither is a defect in the "refuse" direction the ticket asked for; both are false-green or over-refusal edges.
- Playwright suite NOT RUN (no stack); `global-setup.ts` edit read only.

## NOT RUN
- Docker and any local stack; hook legs 3, 4, 8; integration/live runs; Playwright suite (#920); #809 pytest suite and its live 503 claim; whole-workspace test suites (only the touched suites above); PR bodies and GitHub/Linear state (no reads, no writes beyond `ls-remote` and fetching the five PR refs).
- #923: I did not enumerate which real mounts fall in the "other guard refuses anonymous" class. #927: no run on a machine where `cp` fails for real. #920: no check on `docs` (`BASELINE.md`, `DEV-PROCESS.md`) content beyond the file list.
- Environment notes: I used the project's deploy key via `GIT_SSH_COMMAND` for read-only `ls-remote`/`fetch` of the Secuura origin (the key file was only read, not copied). Installs: `npm install` of the api-gateway and shared workspaces, `npm ci` in `tests/e2e`, `npm run build` of shared, all inside my scratch clone.

## Wall-clock
Started 12:18 AEDT, finished about 12:30 (shell clock). Scratch clone left in `scratchpad/gate_da3/` (outside the WEDNESDAY tree). `git -C /Volumes/DevMASTER/WEDNESDAY status --short` showed no paths outside the allowed set from my work.

sha256 of `sed '1,5d;$d' verdict.md | shasum -a 256`: 6d69a46c91e8446f21deecbbc789a9480fc88a2f60391f6089f0420817d6bd4f
