STARTABLE: YES (once stamped; six Q-questions below each have a default that keeps it startable)

# B1030 drafter report: SEAT-G255, ATTIO tier-2 gate of branch b1028/attio-digest-route-tuesday @ fd9d4f9d

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1030_SEAT-G255_attio-digest-tag-gate-tier2.md`, 110 lines. Exact copy `.md.pre-stamp` (`cp -n`, `cmp` equal, both sha256 `47e4b930bb9b0c9e1c1286c7f1dea5da01fb0c11976bd10765845558c19def6f`). Four-underscore lines 8 (7 slots + last line; control: B1023 pre-stamp reads 8). `@X@` tokens 0 (control 1). Non-ASCII bytes 0 by `python3 -I` (control: ATTIO `CLAUDE.md` reads 51). Owner-name grep 0 (control: 19 on the workspace `CLAUDE.md`). Card-id-shaped tokens 0 (control: a planted card-shaped id reads 1).
- Seat **G255**, B-number **B1030**: both unused (G255 word-bounded: 0 files in `tuesday/briefs`, 0 in the Datasec project Briefs; control G253 14 and 10. B1030: 0 files; control B1028 3).
- The subject is a branch, no PR: one commit `fd9d4f9d` on main `fae239bb`, three paths, numstat 1/1, 1/1, 19/0, every other tracked path blob-equal. The gate re-measures all of it, re-makes the builder's NOOP/MR/MT/MS mutants with its own program, and adds three of its own: MC (case), MW (trailing space: predicted to redden ONLY the exact pin (a), showing the new cell (b) checks a prefix only) and MX (both tags: (b) reddens through its negative assertion alone).
- **Correction to the commission's premise: CodeQL is NOT absent.** There is no workflow FILE (0 of 87 tracked paths under `.github/`), but CodeQL default setup is `configured` on `datasecau/attio` (javascript-typescript, query suite extended), and org ruleset 24139430's `code_scanning` rule applies to main. So CodeQL WILL run on the PR. Its result is UNMEASURED until the PR exists. What is truly absent is any hosted TEST run: the gate's `npm test` is the only test verify.
- A merge deploys nothing: workflows are only the dynamic `CodeQL` and `Dependabot Updates`, environments [], repo webhooks [], deployments 0. The runbook deploy is a manual `az webapp deploy` zip.

## Facts re-measured (instrument; control)
- Pins (`git ls-remote origin` read from the builder's clone config, 10:1x): main `fae239bb...`, branch `fd9d4f9d...`, dependabot heads `123c73cc` (refs/pull/1) and `af5db7e1` (refs/pull/2). Parents `[fae239bb]`, tree `9023e02e`, `rev-list --count` 1. Main has 53 commits and 0 merges.
- Delta (`git diff -U0`): digest.js `@@ -214 +214 @@` (tag only), digest.test.js `@@ -95 +95 @@` (tag only), run.test.js `@@ -210,0 +211,19 @@` (one cell). Blobs: digest.js f3690b20 -> ef75add0; digest.test.js b7b99cab -> 542f2f7a; run.test.js e6a2f994 -> 67d47be0. Equal: run.js 2bd7248c, config.js 711ed462, mailer.js 846765f6, .env.example 675ce376, package.json 66aaa5d4, package-lock.json bbcc8061.
- Test sites (`git grep '^\s*test\('`): 280 at main, 281 at head (control `it(` 0). The script is `node --test $(find src -name '*.test.js')`. Local node v26.8.1; engines `>=20`.
- Commit message read whole: subject `ATTIO-29: route the daily digest to the Datasec coordinator tag (-> Tuesday)`, three body paragraphs, trailer `Co-Authored-By: Claude Sonnet 5.5`. One sentence to test is "does not touch config.js, run.js or any address": the new TEST cell adds the placeholder `coordinator-inbox@example.com`. That sentence goes to the gate's C5 as a possible wording point. I did not grade it.
- Other tag sites: the design doc `ATTIO-29_daily-followup-design.md:136` still reads `-> Wednesday` (outside scope); `run.test.js:407` matches the subject's tail.
- Hosted (`gh api -X GET` under `Vision_Sales_Portal/4_Credentials/.gh-config`, 10:10:30): one account logged in, scopes include `repo`; repo permissions admin/push true (control: a nonexistent repo 404). Open PRs #1 and #2 (dependabot; package files only), so the intersection with the three paths is empty. Head check-runs 0. Main check-runs 7 (`Analyze (javascript-typescript)` success x4, last 10-21). Open code-scanning alerts 0. Dependabot open: critical 1, medium 2. Variables 0, environments [], hooks [], deployments 0. Classic branch protection 404. Ruleset: deletion, non_fast_forward, code_scanning (errors / high_or_higher), required_status_checks [].
- ATTIO `CLAUDE.md` lines 21-32: the coupled pair ATTIO and Vision_Sales_Portal share one working scope; lines 54-56: ATTIO "is worked through Vision's session (coupled pair)". Datasec `CLAUDE.md` lines 31-37 declare the same pair. ATTIO `4_Credentials/` holds only `.env` and `.attio-sync-state.json` (no `.gh-config`; control: Vision's `.gh-config` is present).
- Grant: `EXPIRING-GRANTS.md` line 12, "merge-once-tested on EVERY Datasec project (this account)", with the condition "Merges: Tuesday's GO on a gated head, one at a time, CodeQL never bypassed."
- Round census: ATTIO Briefs STATUS files: 1 (B1028), 0 `GATE VERDICT` lines. So the count is 0 of 2 before, round 1 of 2.
- Model: `models_latest.json:23` `claude-sonnet-5-5`; `model-routing.md:109` G2; `:111` G-cap.
- Panes 10:11: `Datasec/Security-Composer-J37`, `fleet-monitor`, `tuesday`. `session-tools/b1030` absent. gitleaks present. load1 3.48.

## D-decisions
- D1: The gate builds its own clone, `base` and `head` worktrees, and its own mutant, hygiene, Jira and differential programs. The builder's `session-tools/b1028/` is read-forbidden to it.
- D2: MT uses a placeholder `example.com` address instead of the builder kit's real old inbox. The property is the same, and no real address enters the gate's files.
- D3: Three gate-own plants (MC, MW, MX). MW's prediction deliberately leaves (b) green, to measure the cell's prefix-only reach. (a) pins the exact string, so the tail is still covered.
- D4: The gate's hosted GETs are under the coupled Vision identity only if S4 says yes. If not, C7 and C8 become UNMEASURED and the verdict is conditional, not a STOP.
- D5: Target verdict 90 minutes, hard stop 150. The suite is small node tests and there are seven mutants. ATTIO has no lock tool, so the gate runs one test process at a time.
- D6: Landing files: pr-title/pr-body plus merge-subject/merge-body (one trailer, asserted), all for the Q-1 default.

## Q-questions for Tuesday (each with a default)
- **Q-1 Landing shape.** ATTIO has no landing rule and main has 0 merge commits, because every commit went straight to main. **Default: PR, then a MERGE commit, head-pinned (`--match-head-commit fd9d4f9d...`), never squash or rebase, after every `Analyze` run on the PR completes with CodeQL success. This would be the repo's first merge commit.** The alternatives (squash or rebase) put a new sha on main that no gate judged.
- **Q-2 Who opens the PR.** ATTIO has no `.gh-config`. **Default: Tuesday, under `GH_CONFIG_DIR='/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/4_Credentials/.gh-config'`.** Measured: one Datasec account, scope `repo`, admin/push on `datasecau/attio`. The coupling lines are ATTIO `CLAUDE.md` 21-32 and 54-56. The same identity serves the gate's GETs (S4).
- **Q-3 Dependency alerts** (dependabot critical 1, medium 2; `npm ci` reports 3). **Default: Note.** The package files are byte-equal to main, so this is not the branch's. Land, and keep the dependabot PRs #1 and #2 as their own lane.
- **Q-4 The stale design-doc line** (`ATTIO-29_daily-followup-design.md:136`, `-> Wednesday`). **Default: Note, a records follow-up for Tuesday.** It is outside the builder's exact scope, so no new head.
- **Q-5 Tier.** **Default: Sonnet G2.** The change is a subject string, its pin and a test cell. There is no auth, money or deploy surface, and a merge deploys nothing (C8). The Escalation hands any security-shaped finding to a tier-1 gate.
- **Q-6 Seat number.** **Default: keep G255.** G254 is in use (HPSM-POC).

## UNMEASURED
- CodeQL on the PR (no PR yet).
- The Azure-side deployment-center config of `datasec-attio-bridge` (az is fenced). The repo side shows no hook, workflow or deployment.
- ATTIO-29's live Jira state (RELAYED from B1028: In Review, 3 comments). I made no Jira call.
- Whether the suite is green on this machine now (I ran nothing).
- Org-level webhooks: 404, because the token lacks `admin:org_hook`.

## Outside-the-fences disclosure
- **Write method.** I wrote the kit and this report with the Write/Edit tools. The `.pre-stamp` copy was made with `cp -n` and checked with `cmp`.
- **Builder's tree, read-only.** I ran git READ verbs (`--no-optional-locks`: ls-remote, rev-list, diff, log, rev-parse, grep, show, ls-tree) against `session-tools/b1028/clone`, because the shared checkout's ssh config is broken and its objects lack `fd9d4f9d`. Nothing was written there. The kit forbids that tree to the gate.
- **Coupled identity.** All `gh` calls were `-X GET` under the Vision_Sales_Portal `GH_CONFIG_DIR`, on `datasecau/attio` only, plus one org-hooks GET that returned 404. No login was printed.
- I made no Jira call, no az, no mail, no HTTP to any hosted host, no push and no clone, and wrote nothing outside `tuesday/briefs/`.
