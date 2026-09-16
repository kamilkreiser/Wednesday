# [Wednesday -> Secuura/Blockchain] SEAT C: raise Ornith's held diffs for scripts, hooks, Start_Up, systemTest tooling and the merge-rule docs as PRs, plus three record closes
# STAGED 2026-09-16 21:06. Plan and measurements: `WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-16_raise_PLAN.md`.
# Kam approved this work (panel 2026-09-16 20:40:59, confirmed 20:41:47 "yes. claude agents"): *"you have the approval to spin up other local agents to test, approve, merge and move things forward"*. Approval of each PR = Wednesday's GO naming the head SHA, after a QA gate verdict at that head plus your Test Evidence block (Kam's 2026-09-11 TESTED grant; CONTRIBUTING.md "Adopted merge flow" step 6).

## BLUF
- **What:**
  - **22 PRs**, one per ticket: 17 shell/tooling + 5 docs.
  - **2 more when their READY files land:** KS-1034 and KS-789. Wednesday sends an addendum.
  - **3 record closes and 1 verify-only.** You are the ONLY seat doing record closes.
- **Your partition: you write ONLY in**
  - `Blockchain/Dev/scripts/**`
  - `.githooks/**`
  - `Start_Up/**`
  - `systemTest/akto/**`, `systemTest/performance/**`, `systemTest/schemathesis/validate-lint.sh`
  - `Blockchain/Dev/deployment/**`
  - `Blockchain/Dev/CONTRIBUTING.md`, `Blockchain/Dev/docs/DEV-PROCESS.md`
  - repo-root `CLAUDE.md` (the tracked one inside the repo)
- **NOT yours. Two other seats run in parallel on these, so never edit them:**
  - Seat A: `Blockchain/Dev/services/api-gateway/**`, `Blockchain/Dev/services/demo-service/**`, `Blockchain/Dev/packages/shared/**`, `Blockchain/Dev/services/auth/**`
  - Seat B: `Blockchain/Dev/services/{security,originate,anchoring,vc-issuer,kyc}/**`, `Blockchain/Dev/docs/openapi/secuura-api.yaml`, `Blockchain/Dev/docs/VOCABULARY.md`
  - Also not yours: the **untracked project CLAUDE.md** outside the repo (see KS-1097).
  - If your work seems to need a file outside your partition, STOP and mail a QUESTION.
- **Your changes reach every seat's push.** `.githooks/pre-push`, `run-shell-suites.sh` and `check-stack-safety.sh` run in the other seats' pre-push. Hooks land per clone on the next `install-hooks`, not on merge. Still, **KS-1093 (P0) goes first**: it removes a false red in the stack-safety gate.
- **WHOSE / WHERE:**
  - Remote: `origin` = `git@github.com:Secuura/Distributed_Secuura.git`, identity `kksecura`.
  - Base: `origin/develop`, which was `0b25f823f` at drafting. Re-read it before every branch.
  - Branches: `feature/ks-<n>-ornith-<slug>`.
  - Tickets: team KS, on the board account.
  - Local work happens ONLY in your own worktree: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-c`. Never the shared checkout `2_Project_Files`.
- **Your files did NOT move between M55 `48e65c435` and the tip** (GitHub compare API: the 36 changed files are 34 under `systemTest/schemathesis/**`, plus `systemTest/CLAUDE.md` and one `Projects Documents/*.html`; `validate-lint.sh` is not among them). `0b25f823f` is not in the local object store, so fetch first.
- **Collisions:** open PRs **#887** (KS-961, head `3aee3deed`) and **#920** (KS-734, head `2112a99e3`) both change `Blockchain/Dev/docs/DEV-PROCESS.md`. Their hunks are at :80+/:117+ and :139; yours are at :62-65, :187-189 and :259-263. There is no textual overlap, but line offsets will shift. **Neither PR is yours** (#887 also touches `.github/workflows`, which is Kam's to merge). Just update from develop if one merges first.

PROVENANCE:
- Kam's approval for Claude seats to test, approve, merge | Kam panel chat 2026-09-16 20:40:59 + 20:41:47 (kam_msgs.sh, view=wednesday) | read 2026-09-16
- origin/develop = 0b25f823f; 36 files changed since 48e65c435, none touched by any READY file | GitHub REST branches + compare 48e65c435...0b25f823f (2026-09-16_raise_PLAN.md lines 17-19) | read 2026-09-16
- the held diffs and their PR NOTES | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_*.diff.md + night/done.md | read 2026-09-16
- partition: no file in two seats (111 paths, 0 overlaps) | 2026-09-16_raise_PLAN.md partition table (mechanical check) | read 2026-09-16
- merge rule: TESTED = QA gate verdict at head + Test Evidence + Wednesday's GO naming the head SHA; feature PRs squash | Blockchain/Dev/CONTRIBUTING.md:107 + "Adopted merge flow" step 6 at develop | read 2026-09-16
- Kam rulings carried verbatim in this brief | decision_queue.sh list ruled --undelivered | read 2026-09-16

## ITEM 0: before any PR
1. **Plan confirmation.** Mail `wednesday-agent@agentmail.to`, subject `[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (seat C)`. Body: this queue re-derived at the tip, any bundle that no longer applies (named), and **every warning your launcher printed at boot, verbatim**. Start on the ANSWER. This is approval-class, so wait.
2. Set up the worktree:
   ```
   git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" fetch origin > f.out 2>&1; rc=$?
   git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" worktree add --detach "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-c" origin/develop
   ```
   Then run `npm ci` in `<wt>/Blockchain/Dev` once (KS-691). Also run `npm ci` in `<wt>/systemTest/akto` and `<wt>/systemTest/performance` before C15–C17.
3. **Baseline** at `origin/develop`: `npm run test:shell` (in `Blockchain/Dev`), `bash scripts/run-shell-suites.sh --list`, `npm run test:unit` in `systemTest/akto` and in `systemTest/performance`. Record what is already red.

## HOW TO APPLY A READY FILE (all bundles)
READY files are in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`. Read them; never edit them.
1. Copy the fenced diff body or bodies into a scratch patch. **Split it into one patch per file** at each `--- ` / `+++ ` pair (hunk headers are miscounted in several).
2. **Many bash READYs name an accommodation** ("apply the REANCHORED section_1", "the RECOUNTED section_2"). The body in the READY IS that section. Apply it as held.
3. Apply each section: `git -C <wt> apply --3way --recount --ignore-whitespace <section>` (redirect output, read `rc`). If that fails, try `patch -p1 --fuzz=2 -d <wt> < <section>`. If that also fails, **apply the `-`/`+` lines by hand at the line named** and say so in the PR body. `git -C <wt> diff` must show every READY `+`/`-` line and nothing unintended.
4. **Red-proof before green:** add the new suite first, run it and record the red lines; apply the product hunk, run again and record all green.
5. **Accommodations measured by Wednesday's apply check** (scratch copy at M55, your queue in order):
   - 46 of 48 sections apply clean.
   - `READY_KS-1117` product hunk (`systemTest/performance/utils/yaml.ts` ~:108): **fuzz only**, as the READY says. Re-apply from the `-`/`+` lines.
   - `READY_KS-1097-A` hunk 2 (`docs/DEV-PROCESS.md` ~:259): a blank context line was dropped, and even fuzz reports it malformed. Apply the one `-`/`+` pair by hand.
   - Everything else applies clean in queue order.

## THE FLOW, per PR (no step skipped)
1. `git -C <wt> fetch origin`, then `git -C <wt> switch -c feature/ks-<n>-ornith-<slug> origin/develop`. **Same-file bundles are strictly serial:** the next branch is cut only after the previous PR on that file merged. At most 3 PRs open awaiting GO (PLAN Q2).
2. Apply, do the PR-NOTES edits, run the tests named. `cmd > out 2>&1; rc=$?`, then read the file. No pipes on a status; zsh has no `PIPESTATUS`. macOS has no `timeout`.
3. Commit and push. The pre-push preflight runs. **Never `--no-verify`. Never force-push.** If the hook refuses with `check-stack-safety.sh` "… is missing — … deleted" lines, that is **KS-1034** (pending, yours) under a worktree hook: STOP and mail a QUESTION.
4. Open the PR against `develop`. The body must carry:
   - the ticket
   - the READY filename(s)
   - the checker run dir from the READY header
   - *"authored by the local model (Ornith) from a Wednesday-written brief; source-read by Wednesday; re-run by seat C at `<sha>`"*
   - the bundle's PR-must-say lines
   - the **Test Evidence block** in DEV-PROCESS form. For shell/docs PRs the platform-suite lines read `not run — <why: no runtime/route change>`. Do not tick them.
5. Comment on the ticket naming the PR (facts only, no @-mentions).
6. Mail `wednesday-agent@agentmail.to`, subject **`[Secuura/Blockchain -> Wednesday] READY FOR QA: #<n> <ticket> @<head sha>`**. Read the head from origin in the same action. Body:
   - first line `Seat C`
   - PR URL, ticket plus comment
   - Test Evidence summary
   - **what was NOT done or NOT covered**
   - accommodations used
7. **STOP that PR** until Wednesday's GO. You may start the next file-disjoint bundle meanwhile.
8. GO arrives in `coagent@agentmail.to` as `[Wednesday -> Secuura/Blockchain] GO: #<n> <ticket> @<sha>`. **Merge only if `<sha>` equals the PR head read from origin now.** To merge: `gh pr merge <n> --squash --match-head-commit <sha>` (CONTRIBUTING.md:107). No `--admin`. If GitHub demands a review, STOP and mail. Never approve your own PR (422).
9. After the merge: fetch, confirm `MERGED` and the merge commit, set the ticket state, move on.
10. **Findings:** fix on the same branch (merge develop in; no rebase plus force-push), re-run, and send a new READY FOR QA mail with the new head.

**Never merge without a GO naming the head SHA. Never deploy. Never `--no-verify`. Never force-push.**

## Ticket state on merge
Close (Done) **only if the PR delivers the ticket's WHOLE scope sentence**. Otherwise comment what landed (PR plus merge commit) and leave it open. Per-bundle defaults are below; the ticket's words win.

## Test commands
- **Shell** (from `<wt>/Blockchain/Dev`):
  - the new suite: `bash scripts/__tests__/<suite>.test.sh`
  - reachability: `bash scripts/run-shell-suites.sh --list` must list the new suite
  - everything: `npm run test:shell`
  - syntax: `bash -n <script>`
  - `shellcheck <script>` if installed; say if not
- **Tooling:**
  - `systemTest/akto`: `npm run test:unit` (= `vitest run --config vitest.unit.config.ts`; the default config includes integration suites, so do not use it) plus `npx tsc -p tsconfig.json --noEmit`
  - `systemTest/performance`: `npm run test:unit` plus `npx tsc -p tsconfig.json --noEmit`
- **Docs:**
  - `npm run test:shell` (some suites read the docs)
  - plus `git -C <wt> grep -n "<changed sentence fragment>" -- 'Blockchain/Dev/scripts/__tests__' 'Blockchain/Dev/packages'` to find any pin on the text you changed. That is read-only there, not your partition.

## QUEUE
Scope sentences are the Linear titles, read 2026-09-16 ~21:1x with `issue(id){title state comments(first:50)}`, sorted client-side. All open.

### C1. KS-1093 (P0): `scripts/check-stack-safety.sh`, chain 1 of 2
- **READY:** `READY_KS-1093_ornith35b-q4_BASHPATCH-B3CREPAIRED-RECOUNTED-PASS-7of7_2026-09-16.diff.md` (apply the B3c-REPAIRED section 1 and the RECOUNTED section 2 as held)
- **Scope:** "check-stack-safety.sh 6f reports a FALSE red once a real Playwright run exists — git check-ignore refuses a path beyond the latest-slot<N> symlink"
- **PR must say:** §6f now probes the `results/latest-slot${slot}` symlink ITSELF. `:321` gains two comment lines. 100 invariants before and after. CELL 4 creates or removes a `latest-slot4` symlink under the ignored `systemTest/playwright/results/` only if none exists. The reference's set-but-empty refusal block for `CHECK_STACK_SAFETY_SH` is an optional 4-line nit.
- **Tests:** `bash scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh` (3/6 at the tip → 6/6), `bash scripts/check-stack-safety.sh` (rc 0, "100 shared-stack safety invariants hold"), `--list`, `npm run test:shell`.
- **On merge:** Done.
- **(Pending) KS-1034** is chain 2 on this file, after C1. Add it only when Wednesday names its READY file.

### C2. KS-1089: `scripts/run-shell-suites.sh`, chain 1 of 2
- **READY:** `READY_KS-1089_ornith35b-q4_BASHPATCH-REANCHORED-RECOUNTED-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "run-shell-suites.sh polish from #953's tier-2 gate: make `--list` survive a tree with no suites on bash 3.2 (QA-8, `:72`) and give the git-list refusal a headline per cause (QA-7)"
- **PR must say:** `:72` uses the empty-array form; `:197–:202` give a headline per cause; `--list` on an empty tree prints ONE blank line with rc 0. Do not touch `:203–:206`.
- **Tests:** the new `run_shell_suites_polish.test.sh` (4 FAIL at the tip → 7/7), `--list`, `npm run test:shell`.
- **On merge:** Done (both checklist items).

### C3. KS-1127: `scripts/run-shell-suites.sh`, chain 2 of 2
- **READY:** `READY_KS-1127_ornith35b-q4_BASHPATCH-REANCHORED-RECOUNTED-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "run-shell-suites.sh counts an exit-0 SKIP as `passed` — a suite that ran 0 of its cells reads identically to one that ran all of them in `shell suites: N passed`"
- **PR must say:** the verdict is now `N passed, M failed, S skipped (of K)` plus a `SKIPPED:` line. **Each suite's output is now CAPTURED and printed after it finishes (no longer live), with stderr merged into stdout.** The skip policy stays rc 0 (as recorded in the READY: ruled 2026-09-13 for the ks949 suite). Preflight leg 14's `shell suites:` prefix is unchanged.
- **Tests:** the new `run_shell_suites_skip_tally.test.sh` (3 FAIL → 8/8), `--list`, `npm run test:shell`.
- **On merge:** Done.

### C4. KS-884: `.githooks/pre-push`, chain 1 of 2
- **READY:** `READY_KS-884_ornith35b-q4_BASHPATCH-REANCHORED-INDENTSHIFT-PASS-7of7_2026-09-16.diff.md` (**r2 only**; the r1 run dir is SUPERSEDED)
- **Scope:** "pre-push resolves the bare name `develop`, so a TAG named develop beats the branch — and --quiet suppresses the ambiguity warning"
- **PR must say:** fully qualified refs at `:160–:168`. **The hook lands per clone on the next `install-hooks`, not on merge.**
- **Tests:** the new `pre_push_qualified_develop.test.sh` (2 FAIL → 4/4), the six sibling pre-push suites via `npm run test:shell`, `bash -n .githooks/pre-push`.
- **On merge:** Done.

### C5. KS-1047: `.githooks/pre-push`, chain 2 of 2
- **READY:** `READY_KS-1047_ornith35b-q4_BASHPATCH-RECOUNTED-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "pre-push:230 names the stack-dependent legs as (3, 4, 7); measured they are 3, 4, 8 — a comment asserting a corpus that moved"
- **PR must say:** a comment only. `(3, 4, 7)` becomes a pointer at the KS-1046 verdict line. **The ticket named `:230`; at M55 it is `:268`** (grep: one hit).
- **Tests:** the new `pre_push_stack_legs_comment.test.sh` (2 FAIL → 4/4), `npm run test:shell`, `bash -n`.
- **On merge:** Done.

### C6. KS-865
- **READY:** `READY_KS-865_ornith35b-q4_BASHPATCH-REANCHORED-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "check-no-latest-tags.sh silently skips a missing input — it scans 5 of the 6 files it advertises and still prints OK"
- **PR must say:** a missing listed input is an ERROR, and the OK line reports N of M. **It REMOVES the retired `.github/workflows/deploy-staging.yml` entry** (it exists nowhere at the tip; retired per KS-1162). The ticket's "or the path is corrected" branch was resolved by measurement. The five remaining files exist at the tip. `run-code-guards.sh:82` is unchanged.
- **Tests:** the new `check_no_latest_tags_inputs.test.sh` (2 red → 4/4), `bash scripts/check-no-latest-tags.sh`, `--list`, `npm run test:shell`, shellcheck if available.
- **On merge:** Done.

### C7. KS-958
- **READY:** `READY_KS-958_ornith35b-q4_BASHPATCH-REANCHORED-RECOUNTED-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "The re-link guard matches the JS runtime name case-sensitively — every UPPERCASE spelling is exempt, and ENV NODE_ENV is in 13 of 35 Dockerfiles"
- **PR must say:** `tolower(L)` at `:338` and `:342`. **Say "latent (every class file writes node_modules in its final stage), closed", not "live defect fixed".** Do NOT bundle with KS-957. The suite copies the reference's helpers because there is no source seam.
- **Tests:** the new `check_shared_relink_case.test.sh` (rows 1–4 red → 6/6), the 1,228-line reference suite via `npm run test:shell`, `--list`.
- **On merge:** Done.

### C8. KS-1139, A + B (`deployment/azure/sync-secrets.sh` + `systemTest/schemathesis/validate-lint.sh`)
- **READY:**
  - `READY_KS-1139-A_ornith35b-q4_BASHPATCH-REANCHORED-PASS-7of7_2026-09-16.diff.md`
  - `READY_KS-1139-B_ornith35b-q4_BASHPATCH-NEWFILE-SYNTH-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "Bare arithmetic-command `((X++))` under `set -e` — exits 1 at 0 and bash ≥ 4.1 errexit kills the script: 10 errexit-live sites remain in `sync-secrets.sh` (×8) and `validate-lint.sh` (×2) after #977's docker-build.sh fix"
- **PR must say:** 8 + 2 sites become `X=$((X + 1))`. **Fix the `:222` typo in A's suite header** (the site is `:221`). Rule 8 in `check-script-portability.sh` is a follow-up, not this PR. The ticket's 2026-09-13 addendum (CELL 4 whitespace variant in `docker_build_empty_table.test.sh`) is not in this PR; say so.
- **Tests:** both new suites (2 red → 3/3 each), `bash -n` on both scripts, `--list`, `npm run test:shell`.
- **On merge:** Done, unless the addendum is ticket scope. In that case, comment and leave open.

### C9. KS-972: `Start_Up/start-secuura.sh`, chain 1 of 2
- **READY:** `READY_KS-972_ornith35b-q4_BASHPATCH-REANCHORED-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "start-secuura.sh banner prints admin@secuura.com / admin123, which has returned 401 since PR #888"
- **PR must say:** `:712` now points at `systemTest/fixtures/provision-actors.ts`. **The admin login CHECK at `:610–:620` still uses the retired credential. That is KS-966 item 3, not this PR.** Peter's 2026-09-10 comment on the ticket (`ADMIN_USER_PASSWORD` is never forwarded to the auth container) is not addressed here; say so.
- **Tests:** the new `start_secuura_banner.test.sh` (2 red → 4/4), `bash -n Start_Up/start-secuura.sh`, `--list`, `npm run test:shell`.
- **On merge:** Done if the scope sentence (the banner) is met. Otherwise comment.

### C10. KS-1011: `Start_Up/start-secuura.sh`, chain 2 of 2
- **READY:** `READY_KS-1011_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "KS-666 stack marker reads "unknown" for owner/branch/commit/started_at whenever the stack is not started via start-secuura.sh"
- **PR must say:**
  - Implements Kam's ruling `secuura-ks1011-stack-marker-unknown-on-restore` = **b** (verbatim below): WARN loudly, by name, and print the recreate command. It must not fail the start.
  - A 14-line insertion after `:720`.
  - KS-1163 (a Claude BUILD item) also edits this file at `:63-82`; whichever is second updates.
- **Tests:** the new `start_secuura_marker_unknown_warning.test.sh` (4 FAIL → green; reads the script as text, no Docker), `npm run test:shell`.
- **On merge:** Done, citing the card.

### C11. KS-1031
- **READY:** `READY_KS-1031_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "KS-754 gate F-4: DEPLOY CONDITION — apply 048 BEFORE rolling the originate image, or every connector erasure shreds the DEK then aborts forever (and run-migrations.sh exits 0 when migrations fail)"
- **PR must say:**
  - **Fix 2 only:** `run-migrations.sh` exits 3 on a failed migration, as its own header `:26` documents. The suite stubs `psql`/`pg_isready`, so no Postgres is needed.
  - Why a hard exit is safe: the closing block's "schema-drift migrations (e.g. 002…) are non-blocking" excuse is resolved (`BACKLOG.md:131` ✅; 002/005 were made idempotent). **The workaround outlived its problem.**
  - Fix 1 (the deploy-ordering condition written where a deployer reads it) is not here.
  - Incidental: `/tmp/migrate-err.log` at `:101` is a fixed shared path. File it separately after a board search.
- **Tests:** the new `run_migrations_failure_exit_code.test.sh` (red → 5 pass lines incl. completeness), `bash -n`, `npm run test:shell`.
- **On merge:** **leave OPEN** (fix 1), with a comment.

### C12. KS-1081
- **READY:** `READY_KS-1081_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "CONFIG DRIFT: two tracked env templates disagree by ~39 vars — bootstrap-env.sh reads .env.example, CLAUDE.md documents env.example"
- **PR must say:**
  - Implements Kam's ruling `secuura-ks1081-two-env-templates-which-is-canonical` = **a** (verbatim below), **in part:** `bootstrap-env.sh` reads `env.example` canonically, with a NAMED legacy fallback.
  - **The fallback is deliberate:** `bootstrap_env_slot_ports.test.sh:91` and `verify-slot-credential-isolation.sh:59` build scratch trees holding only `.env.example`.
  - **The ticket's variable lists are INVERTED:** making `env.example` canonical DROPS ~30 variables a fresh clone used to get (`ALLOW_DEFAULT_SEED_PASSWORDS`, `ENABLE_DEMO_SEED`, `ENCRYPTION_SALT`, `ADMIN_USER_*`, the PGBOUNCER trio, `FRONTEND_URL`, `VC_SIGNING_KEY`).
  - The ticket's docs evidence is `README.md:25`, `CONTRIBUTING.md:26`, `docs/DEPLOYMENT.md:130`, `docs/DEVELOPER-GUIDE.md:53` and `docs/ENVIRONMENT-VARIABLES.md:13-15`, not `CLAUDE.md`. The counts are 65 vs 102 distinct vars, 37 different each way.
  - Not in this PR: the ruling's pointer file and guard cell, and the 30-variable reconciliation. File the reconciliation as its own ticket (after a board search) before `.env.example` is ever deleted.
- **Tests:** the new `bootstrap_env_canonical_template.test.sh` (red → 6/6), `bash scripts/__tests__/bootstrap_env_slot_ports.test.sh`, `npm run test:shell`.
- **On merge:** **leave OPEN**, with a comment.

### C13. KS-1033, item 1
- **READY:** `READY_KS-1033-item1_ornith35b-q4_BASHPATCH-RECOUNTED-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "KS-926 residue: the three guards that could NOT be wired, and what each needs first — a wrong diff base, a self-contradicting default, and a whole-machine read"
- **PR must say:**
  - **Closes item 1 only.** `check-no-demo-mutation.sh:58` default base `origin/main` → `origin/develop`.
  - Item 2 (`check-no-trust-header-reads.sh`, decision-class) and item 3 (`check-container-isolation.sh`, a relocation) stay open.
  - **The DEFERRED reason at `run-code-guards.sh:116` goes stale and is deliberately NOT edited.** The follow-up is "wire the guard or rewrite its DEFERRED reason".
  - `:98`'s two-dot scan is untouched.
- **Tests:** the new `check_no_demo_mutation_base.test.sh` (2 FAIL → 5/5; local bare remote only), `npm run test:shell`.
- **On merge:** **leave OPEN**.

### C14. KS-910
- **READY:** `READY_KS-910_ornith35b-q4_BASHPATCH-REANCHORED-REBRIEF-PASS-7of7_2026-09-16.diff.md`
- **Scope:** "Preflight leg 12 executes ZERO suite cells — it is a reachability check, so with Actions retired no shell suite runs on a gated push" (Backlog)
  - ⚠ The title's "Actions retired" premise was measured FALSE at source on 2026-09-16 20:05: the Actions API shows 23 workflows active and runs through 2026-09-15, all concluding failure. Do not repeat that premise in the PR.
- **PR must say:**
  - Kam ruled option **a** (2026-09-16 09:53): *keep preflight leg 12 as reachability, correct the comment; close on the comment fix.*
  - `pre_push_hook_base.test.sh` `:49-:51` now says leg 12 proves the suite REACHABLE and leg 14 RUNS it.
  - Preflight leg numbering was read at develop `48e65c435`: `preflight.sh:521` leg 12 = `--check-unreached`; `:544`/`:631` leg 14 runs the suites.
  - The staged 09-15 note that KS-910 was "blocked at this checkout under systemTest/" is obsolete: the change is under `Blockchain/Dev/scripts/__tests__/`.
- **Tests:** the new `pre_push_hook_base_leg_comment.test.sh` (2 FAIL → 4/4), `bash scripts/__tests__/pre_push_hook_base.test.sh`, `npm run test:shell`.
- **On merge:** **Done** (Kam: close on the comment fix).

### C15. KS-1108: `systemTest/akto`
- **READY:** `READY_KS-1108_ornith35b-q4_TOOLING-AKTO-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "Akto harness: loadSecretsYml() parses config/secrets.yml with no catch — the KS-1099 shape, whole-file print not yet measured in this package"
- **PR must say:** `src/config/secrets.ts:40` wraps the parse. A malformed `secrets.yml` throws naming only the file and position. The ticket's "measure first" is answered by the red arm (at the tip, `inspect(err)` carried the sentinel).
- **Tests:** the new `tests/unit/config/ks1108-…` red→green, `npm run test:unit` in `systemTest/akto`, `npx tsc -p tsconfig.json --noEmit`.
- **On merge:** Done.

### C16. KS-1117: `systemTest/performance`
- **READY:** `READY_KS-1117_ornith35b-q4_TOOLING-PASS-7of7-FUZZY_2026-09-15.diff.md` (**fuzz; re-apply from the `-`/`+` lines**)
- **Scope:** "k6 YAML loader: a BOM immediately followed by a comment is a marked syntax error in js-yaml 5.2.3, so a comments-only config prints "at line 1, column 2" — strip a leading U+FEFF in readYaml() (QA-963-2)"
- **Tests:** the new `tests/unit/utils/ks1117-…` red→green, `npm run test:unit` in `systemTest/performance`, tsc.
- **On merge:** Done.

### C17. KS-1164, A + B: `systemTest/performance`
- **READY:**
  - `READY_KS-1164_ornith35b-q4_TOOLING-PASS-7of7_2026-09-15.diff.md` (`gate/report.ts:325`)
  - `READY_KS-1164-B_ornith35b-q4_TOOLING-PASS-7of7_2026-09-15.diff.md` (`runner/k6_docker.ts:241`)
- **Scope:** "gate/report.ts writeGateReport overwrites the input summary when --summary does not end in -summary.json"
- **PR must say:** both DoD sites are handled the same way. **The ticket's Follow-up (ruled by Wednesday 2026-09-14 10:11Z: `reportFailedGateBreakdown` `String(n)` vs `toLocaleString()`) is not in this PR.** Say so.
- **Tests:** both new unit tests red→green, `npm run test:unit` (existing gate cells and goldens unchanged), tsc.
- **On merge:** Done if the three DoD boxes are met and the Follow-up is not a DoD box. Otherwise comment and leave open.

### C18. KS-1097: DOCS, one PR (CONTRIBUTING.md, DEV-PROCESS.md, repo-root CLAUDE.md)
- **READY:**
  - `READY_KS-1097-A_ornith35b-q4_DOCPATCH-PASS-6of6_2026-09-15.diff.md` (**hunk 2 by hand**)
  - `READY_KS-1097-B_ornith35b-q4_DOCPATCH-REFLOW-INFERRED-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1097-C_ornith35b-q4_DOCPATCH-MERGED-PASS-7of7_2026-09-15.diff.md` (the B and C bodies are the APPLIED patches)
  - `READY_KS-1097-Da_ornith35b-q4_DOCPATCH-STRICT-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1097-Db_ornith35b-q4_DOCPATCH-RECOUNT-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "Merge-rule docs after #957: the v4 footer and two gate statements gloss TESTED weakly, 'the reviewer' has no referent, one sentence lets a person sign off (QA-957-1..5, W-2)"
- **PR must say:**
  - QA-957-1..5 + W-2, as the READY headers list.
  - **NOT in the PR:** `CONTRIBUTING.md:531-532` and `DEV-PROCESS.md:26` (Kam's 2026-08-27 red-pen lines), and `.github/workflows/`.
  - Db's line says Kam's `raise-to-1` ruling is NOT APPLIED. That is still true: `required_approving_review_count: 0`, measured 2026-09-16. Re-measure before merge with `GET /repos/Secuura/Distributed_Secuura/rules/branches/develop`.
  - **The ticket's "mirror into the project-root untracked CLAUDE.md by hand" is NOT done by you** (PLAN Q5). Say it is left for Kam.
- **Tests:** docs. `npm run test:shell`; the `git grep` pin search (Test commands above); state that `CONTRIBUTING:455`'s `(16:56):` prefix is still byte-identical.
- **On merge:** Done.

### C19. KS-1037: `CONTRIBUTING.md`, after C18
- **READY:** `READY_KS-1037_ornith35b-q4_DOCPATCH-PASS-6of6_2026-09-15.diff.md`
- **Scope:** "The NO-FORCE-PUSH rule exists only in .githooks/pre-push and in no .md — document it in CONTRIBUTING.md with its ALLOW_FORCE escape and the merge-in alternative"
- **PR must say:** eight lines after the Merge method bullet (`:107`). **Before merging, check the quoted ruling's scope against the card text below** (`secuura-force-push-own-branch-standing`); if it differs, correct it to the card. Cite KS-1035 for the stale-approval cost.
- **Tests:** docs, as C18.
- **On merge:** Done.

### C20. KS-1049 Part A: `CONTRIBUTING.md`, after C19
- **READY:** `READY_KS-1049-A_ornith35b-q4_DOCPATCH-PLACED-BY-WEDNESDAY-D8-PASS_2026-09-16.diff.md` (apply strictly; the placement is Wednesday's)
- **Scope:** "A PR's Test Evidence must state whether the preflight RAN — the hook skips systemTest/docs/vault-only pushes and emits nothing at all"
- **PR must say:** one preflight bullet after `CONTRIBUTING.md:579`. The ticket's optional hook skip notice is a separate shell change. `.github/pull_request_template.md` has no evidence block, so there is nothing to mirror.
- **Tests:** docs, as C18.
- **On merge:** **leave OPEN**.
- **(Pending) KS-789 r2** is on this file after C20. Add it only when Wednesday names its READY file.

### C21. KS-1035 Part D: `docs/DEV-PROCESS.md`, after C18
- **READY:** `READY_KS-1035-D_ornith35b-q4_DOCPATCH-REANCHORED-PASS-6of6_2026-09-15.diff.md` (tip-exact context; apply strictly)
- **Scope:** "The merge gate cannot see a WITHDRAWN approval — #813 reads approved+clean against the reviewer's written refusal"
- **PR must say:** one paragraph after `DEV-PROCESS.md:189`, inside `### 2.`. Cite the ticket's #813 measurement (2026-09-08 14:52→14:56). Items 1–3 and 5 remain; dismissing the stale approvals on #813/#785 is a maintainer's click.
- **Tests:** docs, as C18.
- **On merge:** **leave OPEN**.

### C22. KS-1045, A + B: `deployment/KINTSUGI-DEV-SERVER-PLAN.md`
- **READY:**
  - `READY_KS-1045-A_ornith35b-q4_DOCPATCH-RECHECK-PASS-7of7_2026-09-15.diff.md`
  - `READY_KS-1045-B_ornith35b-q4_DOCPATCH-PASS-7of7_2026-09-15.diff.md`
- **Scope:** "KINTSUGI-DEV-SERVER-PLAN.md still says the VM "has NOT been created" — Stage B ran ~3 weeks ago and the credit-expiry warning has lapsed"
- **PR must say:** `:3` Status, `:50` credit line, `:173` Stage-B row. Cite KS-1044. **Re-measure the VM read-only first** (PLAN Q6): run `az account show`. **Only** if it is on tenant `efc17e5f-7637-4118-b92c-c5236d591cad`, run `az vm list -o table`. **No `az login`, no write verb.** If not signed in, write "facts are the ticket's 2026-09-09 measurements, not re-measured" in the PR and the mail.
- **Tests:** docs.
- **On merge:** Done.

### RECORD CLOSES (no code; after C1–C22 or in any gap)
Each is ONE facts-only ticket comment, no @-mentions, then a state move. Re-read the ticket before writing.
- **KS-777** "QA pass F-1/F-3/F-4/F-7: two vacuous guards, an unasserted statement tail, and an un-normalised org comparison (fixed on #795)" (Todo)
  - Verify: `gh pr view 795 --json state,mergedAt,mergeCommit`. Measured 2026-09-16: merged 2026-09-03T11:55:42Z, merge commit `7dd304b7c3efab9b12805df43fcf13a88d05eb86`, title "QA F-3/F-1/F-7/F-4: guard the four things last night's merges left unpinned".
  - Then comment the receipt and move to **Done**.
- **KS-813** "\"PREFLIGHT PASSED\" is unconditional — step() only prints a banner, and skipped legs read as passes" (Backlog)
  - Already fixed by `f09b62945` ("KS-1046: the preflight verdict must not outlive its corpus — name the legs that ran (#925)"). Found with `git log -S 'legs ran' 48e65c435 -- Blockchain/Dev/scripts/preflight/preflight.sh`.
  - **Re-read `scripts/preflight/preflight.sh` at the tip** and quote the lines: `TOTAL_LEGS=15` (~:130), the checked TOTAL (~:159-167), the "N/15 legs ran" and "PREFLIGHT INCOMPLETE" verdict (~:704-753).
  - Then comment and move to **Done**.
- **KS-683** "Anchor-status standoff: …" (Todo)
  - Kam ruled on 2026-09-16 at 15:04 (card `secuura-ks683-blockfrost-key-per-environment` → **a**, "Leave it as it is"). There is no separate Blockfrost key per environment; the quota pressure is gone (HOBBY, 300,000 calls/day, 2026-08-31, KS-670). KS-683 has no K-side work left: layer 1 is PS-644/#581 merged on S; layer 2 is done in K and pinned by `ks587-honest-anchor.test.ts`; layer 3 is Stuart's estate call.
  - **Before closing, comment:** the ticket's terminal-state argument (2026-08-21) reasons over `confirmed`/`failed` only, but KS-726 added `submitting` and `submitted` to the published contract. Verify at the tip with `git -C <wt> grep -n "submitting" origin/develop -- 'Blockchain/Dev/services/*/src/*.openapi.ts'` and quote the enum. A consumer writing a terminal-state table from this ticket today would miss two live states.
  - Then move to **Done**.
- **KS-1076: verify only, NO write.** Item 1 is already recorded on the ticket (comment 2026-09-13T22:19Z, s215: fixed by `6a047445b` + `ec61abf8e`). Item 2 stays open (a CI item).

## RULED BY KAM, NOT YET IN AN ARTEFACT
Source: `bash 2_Project_Files/tools/decision_queue.sh list ruled --undelivered`, filtered to Secuura and to this seat's bundles. Rulings verbatim from `decision_queue.sh show <id>`.
- **`secuura-ks1011-stack-marker-unknown-on-restore` → `b`** (ruled 2026-09-16T09:54:30). For C10.
  - *"[b] start-secuura.sh only WARNS (loud, named) when it finds unknown markers and prints the recreate command for the operator"*
  - detail: *"no automatic restart; the operator decides"*
- **`secuura-ks1081-two-env-templates-which-is-canonical` → `a`** (ruled 2026-09-16T09:54:27). For C12.
  - *"[a] env.example (the larger, the one CLAUDE.md documents) is canonical"*
  - detail: *"bootstrap-env.sh is repointed to it, .env.example becomes a one-line pointer file (kept, not deleted), and a guard cell asserts the two never diverge again:the docs stay right; one script line + a pointer"*
- **`secuura-force-push-own-branch-standing` → `narrow-allow`** (ruled 2026-09-07T18:56:50). For C19; also governs you.
  - *"[narrow-allow] Allow it on an agent's OWN unshared branch, under exactly those checks (your 18"*
  - detail: *"03:38 ruling):The agent's two controls are the standing precondition: no PR on the branch, proven with a discriminating control query; and no live gate on the SHA, proven from the run's conclusion and job count. Anything shared - develop, main, a branch with an open PR - stays yours."*
  - **Every branch in this brief has an open PR, so force-push is never allowed here.**
- **`secuura-required-approvals-zero-after-the-untick` → `raise-to-1`** (ruled 2026-09-10T10:38:57). For C18 Db; also governs merges.
  - *"[raise-to-1] Raise required approving reviews from 0 to 1 on the require-pr-gates ruleset"*
  - Not yet applied (measured 0 on 2026-09-16). If it flips, merges refuse: STOP and mail.
- **`secuura-agent-github-identity` → `identity`** (ruled 2026-08-26T17:12:33):
  - *"[identity] Create an agent GitHub identity in the Secuura org (rec) + Stuart approves today's two"*
  - Not executed. Self-approval returns 422. Do not try.
- **`secuura-891-workflow-scope-merge` → `kam-merges`** (ruled 2026-09-07T18:56:50). This is why #887 is not yours and why no bundle touches `.github/workflows`.
  - *"[kam-merges] You merge #891 yourself - one click (Recommended)"*

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Every PR waits for Wednesday's GO after its QA gate. One merge at a time, head pinned.
- Client-facing communication is ticket comments only. No @-mentions to Peter or Stuart.
- Never delete; quarantine.
- Kintsugi first, demo behind gates. **No deploy in this brief.**
- `.github/workflows` untouched.
- KS-1164's Follow-up (`toLocaleString`), ruled by Wednesday 2026-09-14 10:11Z, stays out of the PR.
- KS-1097: the Kam red-pen lines `CONTRIBUTING:531-532` and `DEV-PROCESS:26` stay out.
- KS-865: the retired-entry removal, resolved by measurement.
- KS-1093 lands first (P0).

## HOLDS
- **Signature classes pause for Kam, always:** production · money · external communication to any human · anything irreversible.
- **Client-facing communication is TICKET COMMENTS only.** The extranet is input only. Nobody but Kam messages Peter or Stuart.
- **Handovers to Peter/Stuart are TEST BLOCKS, never a list of PRs.** Wednesday composes them; you do not hand over.
- **No `--no-verify`, no force pushes, no `--admin`.**
- **Never deploy.** No kintsugi or demo, no `deploy.sh`, no `sync-secrets.sh` run against Azure. KS-1139 is `bash -n` plus suites only. Project hold: no deploy without migration 048 first (KS-1031). `az` is read-only (`account show`, `vm list`) and only as C22 says.
- **Other authors' PRs, and open PRs not in this queue (#887, #920, #989, #927, #809 …), are not yours.**
- **Parallel seats share one inbox** (`coagent@agentmail.to`, prefix `Secuura/Blockchain`). **A mail naming a PR or ticket not in YOUR queue is not yours.**
- **Your own `git worktree` only.** Never the shared checkout.
- Before filing any ticket, search the board by SYMBOL, path or error string, and say what you searched. One ticket per test pass (Kam, 2026-09-07 13:23). New and unassigned tickets go to the board account.
- A control must be able to fail. `cmd > out 2>&1; rc=$?`. macOS has no `timeout`. zsh has no `PIPESTATUS`.
- **If a line in this brief looks wrong at source, say so** (QUESTION mail). Approval-class items wait for the ANSWER.
- **Session end:** send the wrap mail `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-1x` (first line `Seat C`) listing every PR (number, head, state, ticket state) and every record close.

SELF-CHECK: claim-bearing lines re-read via self_check_view.sh (repeated ticket ids, numbers, close/open dispositions) - no contradiction found; the whole brief was NOT re-read end-to-end by Wednesday (the drafter mechanically checked 111 paths / 0 overlaps and replayed each queue at the base) | 2026-09-16 21:06
