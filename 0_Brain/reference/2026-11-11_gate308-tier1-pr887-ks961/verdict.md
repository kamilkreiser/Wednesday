PR 887: NO GO

# Gate 308, tier 1 (Opus): PR 887 (KS-961, advisory workspace-suites job + DEV-PROCESS.md row)

| PR | head | base (merge-base) | verdict |
|---|---|---|---|
| 887 | 3aee3deed2e3ac557f0a52c0797c2a4a8df25f69 | 8861e62161466c40f08d2b10a30edeb203123993 (2026-09-13) | NO GO |

**Pins.** Start (03:47Z, ls-remote): develop 4a91ff3e1c56, PR 887 3aee3deed2e3. Both match the commission. End (03:52Z): both UNCHANGED.

**BLUF.** The workflow is safe in shape: `pull_request` (not `_target`), no secrets referenced, checkout SHA-pinned, advisory is real (`continue-on-error: true` at job level, and develop has no required-status-check rule). Two things block it.
- **The job cannot reach its test step at develop.** The lockfile still records only the macOS rollup binary, so two vite-6 frontend builds die on the Linux runner and the suites are skipped. That is exactly what the job's only GitHub run (2026-09-13) measured.
- **The doc text the PR adds claims "Actions resumed on 2026-09-09 … the job now executes on each push".** That is false today: jobs are again not started for billing. Once merged, it contradicts the same file's unchanged "GitHub Actions is retired" section.

Smaller findings: inherited write token scopes, a tag-pinned setup-node, no job timeout, and a stale 26/6 baseline (develop is 27/5).

## FOUND / TESTED / HOW

**Method.** I made a `git clone --shared --no-checkout` of the Blockchain checkout in this session's scratchpad (`.../scratchpad/r`). I fetched `refs/heads/develop` and `refs/pull/887/head` THERE into `refs/p/*`. Every merge-tree and archive ran in the scratch clone. In !CODING I used only `ls-remote` and read verbs, plus a read of the Secuura `.env` for the Linear key (never printed). GitHub and Linear were read-only GETs, using the Blockchain project's own `GH_CONFIG_DIR`. Nothing was posted, commented on, pushed or mailed. I made a scratch venv for PyYAML. Load1 stayed between 4.0 and 4.6.

1. **Touched set: exactly 2 files.** `diff --stat 8861e621..3aee3dee`:
   - `.github/workflows/pr-platform-suites.yml` +97 (one new job `workspace-suites`, inserted between `migrations` and `build`; the file already existed)
   - `Blockchain/Dev/docs/DEV-PROCESS.md` +50 -2
   - Commits: bb0502c80 (job), 6899de33d (build step + setup-node, Peter's review), cb7a3e3be and de376a9f1 (develop merges), 3aee3deed (doc re-stamp). The workflow file at head is byte-identical to cb7a3e3be's job, as the body says.
2. **Age, distance, merge.**
   - Created 2026-09-07; last updated 2026-09-30 (Peter's "LGTM" approval at 3aee3dee).
   - Merge-base 8861e6216 (2026-09-13). The PR is **5 ahead, 1296 behind** develop.
   - `merge-tree --write-tree` onto 4a91ff3e: **rc 0**, tree 71a5b1f2. The merged delta against develop equals the PR's delta line for line, on both files.
   - Develop touched both paths since the base, and both are disjoint from the PR:
     - workflow: 1 line, the playwright step name at :285 (91d3a0486)
     - DEV-PROCESS.md: 7 commits, f37214951 … 25f42d80b
   - GitHub reports `MERGEABLE`, `mergeStateStatus: UNSTABLE` (non-required checks red).
3. **Workflow safety (Q2).** PyYAML parse of the head file and the merged file: 7 jobs. Values below are identical in both.
   - **Triggers:** `pull_request` (branches develop and main), `push` (develop), `workflow_dispatch`. **No `pull_request_target`**, so no Critical.
   - **Permissions:** workflow level `contents: read, packages: write, checks: write, pull-requests: write`. The new job has **no job-level `permissions:`**, so it inherits all four. The `build` job alone narrows to `contents: read, packages: write`. See G308-887-3.
   - **Secrets:** the new job references **no** `secrets.*` and sets no env. The secret uses in this file are `secrets.GITHUB_TOKEN` (suite jobs), `secrets.TEST_ADMIN_PASSWORD` (schemathesis) and `secrets: inherit` (build); none of these reach the new job. Under `pull_request`, fork PRs get a read-only token and no secrets. The residual exposure is the implicit GITHUB_TOKEN on same-repo branches and develop pushes, which checkout persists into `.git/config` by default (G308-887-3).
   - **Pins:** `actions/checkout@9c091bb21b7c…` (v7.0.0, SHA, AUDIT D-7) is correct. `actions/setup-node@v6` is a **tag pin** (G308-887-4).
   - **Concurrency:** workflow level, `pr-platform-suites-${PR number || ref}`, cancel-in-progress. The new job shares it. This is fine.
   - **Timeout:** none, so the default is 360 min. Every other job in the file sets 25, 40, 25 or 45 (G308-887-5).
   - **Advisory is real:**
     - `continue-on-error: true` at job level, with no `|| true` in steps.
     - `GET /rules/branches/develop` returns only `deletion`, `non_fast_forward` and `pull_request`, with **no `required_status_checks`**. Classic protection: 404 "Branch not protected"; `required_status_checks.enforcement_level: off`.
     - The check still shows as **FAILURE** (red X) in the PR's rollup: "Workspace unit suites (advisory, non-blocking)" = FAILURE. It blocks nothing (G308-887-9).
4. **Does it run what it claims (Q3), read against develop 4a91ff3e.**
   - Scripts exist. Root `package.json` workspaces are `packages/*, services/*, frontend/*`, and `npm ci` has `Blockchain/Dev/package-lock.json` (present).
   - I ran the job's own counting logic over develop's package.json files: **32 workspaces carry `build`, 27 carry `test`, 5 are skipped** (frontend admin, demo-overlay, outlook-addin, verifier, website; `frontend/issuer` now has `vitest run`). At the PR head the same logic gives 26 and 6.
   - No step names a missing script.
   - **But the build step fails deterministically on ubuntu-latest** (G308-887-1).
5. **Doc vs workflow vs develop (Q4).** The new section claims the following:
   - (a) "Actions resumed on 2026-09-09 … runs have started on every PR and every develop push … the job now executes on each push of this branch". This is **false today**, and the merged file contradicts itself (G308-887-2).
   - (b) "what it prints is evidence, not a verdict" / advisory. This is true.
   - (c) The build-first command. It matches the job.
   - (d) Baseline 26/6/1-failing at de376a9f1. This is stale at develop (G308-887-6).
   - The "five ways" renumbering merges cleanly. Develop has only items 1 to 4, so item 5 is new and does not collide.
6. **Billing (Q5): estimate.** There is no matrix: 1 job, ubuntu-latest, 1x multiplier. The repo is **private**, so minutes are billed.
   - The only measured run, job 103803259738 (2026-09-13), took **4 min 15 s to its build failure**:
     - setup: 10 s
     - npm ci: 66 s, with no npm cache configured
     - build: 168 s before it failed (24 of 32 green)
     - test: skipped
   - **Estimate for a run that reaches and finishes the tests:** about 7 to 9 min wall clock. That is about **8 billed minutes per run** (whole-minute rounding per job), range 7 to 10. The basis is a full build of about 3 to 4 min (2 min locally on macOS) and a test step of about 1 to 2 min (40 to 58 s locally on macOS).
   - **As the job stands at develop** (build fails): about **5 billed minutes per run**.
   - **Frequency:** it fires on every PR open, synchronize or reopen to develop or main, AND every develop push.
   - **Context:** the same workflow's other 6 jobs on that run add up to about 45 billed minutes (build about 15, perf about 11, schemathesis about 8, akto about 7, playwright about 3, migrations about 1). The new job adds about 15 to 18% per run.
   - The run-timing API returned `total_ms: 0` for every job (unusable), so these figures come from step timestamps.
7. **Words (Q6).**
   - **Closing words in closing form: 0** across the 5 commit messages, the PR body, the PR comments and the 6 KS-961 comments. The control `KS-961` appears in each: 4, 1, 1, 1.
   - Bare closing words: body 1 ("gateway closed by HOLD"), ticket 3 (prose: "fixed before I approve", "closed by HOLD"). None of them is in closing form.
8. **PR and ticket read.**
   - Body: read whole. It honestly discloses the one GitHub run (build FAILED on rollup, so suites were SKIPPED) and that the YAML's "IT CANNOT RUN TODAY" comment is stale and deliberately left unedited.
   - Comments: linear-bot and the kksecura re-run comment.
   - Reviews: Peter's 4 (COMMENTED, CHANGES_REQUESTED, COMMENTED, APPROVED "LGTM" at 3aee3dee on 2026-09-30).
   - KS-961: state **In Review**, assignee Kam, 6 comments sorted client-side. The 2026-09-08 comment records the relayed Kam ruling that the billing fix is the only unblock.

## NOT TESTED
- **I cannot run GitHub Actions.** The job was not executed by me, at the head or at develop. G308-887-1 at develop is inferred from the lockfile content (one rollup platform binary, darwin-arm64), the unchanged vite ^6 pins in demo-overlay and outlook-addin, and the 2026-09-13 run's measured failure on the same lockfile shape. It is not re-measured.
- `npm ci`, build or test locally at develop or at the head. The 27/5 counts come from the job's own script logic over the package.json files, not from an npm run.
- actionlint: **absent** on this machine. YAML was validated with PyYAML only (head and merged file both parse; 7 jobs).
- Whether the GitHub org's spending limit or payment state changes before merge. I read only the current job annotation.
- Billing minutes are an **estimate**: there is no successful full run to measure, and the timing API returned 0.

## Findings
- **G308-887-1 MAJOR: the job never runs the suites it is named for, at develop.**
  - At develop 4a91ff3e, `Blockchain/Dev/package-lock.json` carries exactly one `@rollup/rollup-*` entry, `rollup-darwin-arm64`, and no linux-x64-gnu one (npm/cli#4828 class).
  - `frontend/demo-overlay` (vite ^6.0.0) and `frontend/outlook-addin` (vite ^6.4.3) still build with rollup.
  - On ubuntu-latest, step "Build workspaces" (`npm run build --workspaces --if-present`) fails, and step "Run every workspace test suite" is **skipped**. Measured on GitHub: run 34786655660, job 103803259738, step 6 failure, step 7 skipped.
  - So "This job is the same command, on the PR" (workflow comment) and the doc's lane are, in practice, an advisory build job that is always red. No unit suite executes on GitHub.
  - The PR body says the lockfile matter is "outside this PR (raised for filing)". I found no fix on develop.
  - Either the lockfile fix lands first, or the PR's text should stop implying the suites run.
- **G308-887-2 MAJOR: the doc claims Actions resumed; today jobs are not started, and the merged doc contradicts itself.**
  - New text (merged DEV-PROCESS.md :90): "**Actions resumed on 2026-09-09** — runs have started on every PR and every `develop` push … so the job now executes on each push of this branch."
  - Measured today:
    - run 42937313549 (`pr`, develop push, 2026-11-11 01:13Z) and run 42773788049 (`pr`, PR, 2026-11-10 07:13Z) each have 6 jobs with **0 steps**, finished in about 3 s
    - check-run annotation: "The job was not started because recent account payments have failed or your spending limit needs to be increased."
    - 0 `success` conclusions among the runs created since 2026-10-01 (first page of 100)
  - After merge, the same file says "## GitHub Actions is retired for this repository … a **decided state, not an outage**" (:69-71, unchanged on develop), and at :350 "With Actions retired no check can ever report". The new section says the opposite.
  - The doc is billed as the live contract, so this blocks. The sentence needs re-dating, or must agree with the retired section.
- **G308-887-3 MEDIUM: least privilege.**
  - `workspace-suites` has no job-level `permissions:`. It inherits `packages: write, checks: write, pull-requests: write` and runs `npm ci` (every dependency lifecycle script), 32 workspace builds and 27 test suites.
  - `actions/checkout` keeps its default `persist-credentials: true`, so the token sits in `.git/config` where any of that code can read it.
  - The exposure: on same-repo PR branches and develop pushes, a compromised dependency could write `ghcr.io/secuura/pk-ci-*` packages that the suite jobs in the same workflow pull by tag. Fork PRs are not exposed (read-only token).
  - This job needs `permissions: contents: read` and `persist-credentials: false`. The `migrations` job has the same inherited pattern (pre-existing).
- **G308-887-4 LOW: tag pin.**
  - `actions/setup-node@v6` (head :148) is a floating major tag, not a SHA. The job's comment cites the file's three other setup-node uses as the convention. They are also `@v6`, but the repo's AUDIT D-7 pin `48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e` (v6.4.0) is used by ci.yml, deploy-demo.yml, pr-security-gates.yml and security-scan.yml.
  - The comment's line references ":340, :423, :560" are stale; at the head they are :364, :460, :597.
  - Also `node-version: current` is unpinned (v26.8.2 on the measured run).
- **G308-887-5 LOW: no `timeout-minutes`.** The job gets the 360-minute default. Every other job in the file sets 25 to 45. A hung suite (for example the `threadTokenMint` emulator round-trip) bills up to 6 hours per run on a private repo.
- **G308-887-6 LOW: stale baseline.**
  - The doc table's "live contract" column is head de376a9f1 (2026-09-14): 26 with a `test` script, 6 skipped. It also says "the numbers above are what 'all of them' should look like".
  - The workflow comment says "six workspaces have no test script".
  - At develop the job's own logic gives **27 / 5** (`frontend/issuer` gained `vitest run`). The failing set was measured 1296 commits ago.
  - Develop's own row at merged :181 says "25 services carry a `test` script", a third number on the same page.
- **G308-887-7 LOW: the PR contradicts itself.** The workflow comment block (head :118-131) says "⚠ IT CANNOT RUN TODAY … GitHub Actions is RETIRED". The PR's doc says Actions resumed. The body acknowledges this and says it was deliberately not edited. Merging ships both statements.
- **G308-887-8 INFO: call sites overstated.**
  - "`deploy-demo.yml:140` … runs at DEPLOY — after merge" is overstated, at the base and at develop. deploy-demo.yml is `workflow_dispatch`-only, and `build-app` runs only with input `i_know_this_is_the_legacy_container_apps_path == 'true'` (the deleted Container Apps target, KS-552).
  - Both existing call sites are manual, so the real gap is wider than stated.
  - Also, ci.yml runs its workspace command from the repo root, not `Blockchain/Dev`.
- **G308-887-9 INFO: an advisory job still shows a red check.** With job-level `continue-on-error`, the check run reports FAILURE (the PR's rollup shows a red "Workspace unit suites (advisory, non-blocking)"). It is not required, so it does not block. Peter's 09-08 note that it "makes the job report green" is not what GitHub showed. The doc does not claim green.
- **G308-887-10 INFO: step label.** "Setup Node (latest; min v24.11.0 per engines)" is copied from other jobs. `engines.node` is `>=18.0.0` in the root and every workspace at develop. There is also no npm cache (`cache:` unset), which costs about 66 s per run.

Note: the merge of a `.github/workflows` PR is Kam's own click (card `secuura-891-workflow-scope-merge` = kam-merges).
