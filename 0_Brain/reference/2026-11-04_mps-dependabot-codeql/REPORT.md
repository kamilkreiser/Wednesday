# MPS: CodeQL on Dependabot PRs - investigation (read-only, 2026-11-04)

## BLUF
- Default-setup CodeQL has NEVER analysed a Dependabot PR in any of the four Datasec repos (0 analyses on 8 of 8 bot PRs checked; 0 of ~163 PR-ref `dynamic` runs were by a bot). It is systematic, not an MPS quirk.
- The cause is NOT in anything we can read: MPS has no dependabot.yml, Actions are fully enabled, no Dependabot secrets exist. GitHub's docs do not state the reason (UNMEASURED/undocumented). Best-supported hypothesis: default setup's pull_request run is not started for Dependabot-actor PR events, so no `dynamic` run exists and the CodeQL check stays "neutral / 4 configurations not found".
- The "advanced setup repo scans its bot PRs" evidence DOES NOT EXIST: all four repos are on default setup (HPSM-POC included, contrary to the belief). No comparison repo.
- Cheapest satisfying route is the baseline (re-push the bot branch as the project account). An advanced-setup `codeql.yml` is the only durable fix, but it is untested for Dependabot here and trades away default setup.

## Recommendation
1. Keep the re-push route (a human/project-account push gives `dynamic` + 4 analyses; measured on #157, #158) as the standing procedure. Zero risk, zero config.
2. Do NOT adopt pull_request_target (docs steer to it only for secrets/write-token; CodeQL needs neither; it adds checkout-of-untrusted-code risk).
3. If the owner wants it automatic: a PILOT on one low-stakes repo (not MPS first, e.g. Composer which has 2 open bot PRs and no workflows dir) is not possible without switching it to advanced; so pilot on MPS only via a branch-scoped change, Datasec MPS seat to make it, owner-approved: disable default setup, add `.github/workflows/codeql.yml` (on: pull_request to main, push to main, schedule; `permissions: security-events: write, contents: read`; languages matrix as default setup's six; `queries: security-extended`). A Dependabot-triggered `pull_request` run gets a read-only GITHUB_TOKEN; CodeQL upload needs security-events:write, which GitHub grants to code scanning uploads on Dependabot PRs only in some cases - UNMEASURED, must be tried on a real bot PR before relying on it. Rollback = delete the file, re-enable default setup (PATCH, owner/seat action).

## Detail

### Q1 MPS measurements (repo datasecau/MPS-Commercial-Calculator, gh under MPS config dir)
- Default setup: GET repos/datasecau/MPS-Commercial-Calculator/code-scanning/default-setup -> state configured, languages actions,csharp,javascript,javascript-typescript,python,typescript, query_suite extended, threat_model remote, schedule weekly.
- Dependabot PRs ever: GET .../pulls?state=all&per_page=100 filtered user=dependabot[bot] -> only #121 (19893df0) and #120 (80f336a6), both closed, 2026-10-26.
- GET .../code-scanning/analyses?ref=refs/pull/120/head and /121/head -> 0 and 0. Same query for refs/pull/157/head -> 4.
- GET .../commits/80f336a6/check-runs -> ci jobs (package, python, web, dotnet) success; "CodeQL" neutral, title "4 configurations not found".
- GET .../actions/runs?event=dynamic&per_page=100 (total_count 359): PR-ref runs (head_branch refs/pull/N/head, e.g. 141-158) all actor kamilDatasec. The only dependabot[bot] dynamic runs are "npm_and_yarn in /web for undici|zod - Update #..." on main (GET .../actions/runs?actor=dependabot[bot]) - these are the Dependabot updater jobs, NOT CodeQL. Dependabot-actor `pull_request` runs: only workflow `ci` (undici-8.12.3, zod-4.6.7 branches; some failure, some success).
- GET .../contents/.github/dependabot.yml -> 404 (no version-updates config; PRs come from Dependabot security/alert updates). .github listing shows only workflows/ci.yml.
- GET .../actions/permissions -> enabled true, allowed_actions all, sha_pinning_required false. GET .../actions/permissions/workflow -> default_workflow_permissions read, can_approve_pull_request_reviews false. Neither blocks CodeQL.
- GET .../dependabot/secrets -> total_count 0 (secrets not a factor: CodeQL default setup needs none).
- Ruleset: GET .../rulesets/24139430 -> "Security scan rule", enforcement active, target ~DEFAULT_BRANCH, rules: deletion, non_fast_forward, code_scanning (CodeQL, security_alerts_threshold high_or_higher, alerts_threshold errors), required_status_checks (empty list), bypass_actors [] (current_user_can_bypass never). It gates the DEFAULT BRANCH code-scanning results; it is evaluated on merge into main, which is why a bot PR with no CodeQL result is blocked.
- Default-branch analyses exist: GET .../code-scanning/analyses (refs/heads/main 56 in first 100).

### Q2 Other repos (each under its own config dir)
| Repo | default-setup | workflows | dependabot.yml | bot PRs (analyses on refs/pull/N/head) | PR-ref dynamic runs by actor | a human PR analyses |
|---|---|---|---|---|---|---|
| datasecau/HPSM-POC | configured, extended | ci.yml, security/ (gitleaks.ignore only) | 404 | #209 closed: 0 | 54 all kamilDatasec | #284: 4 |
| datasecau/Reporting_Dashboard_Au (NexusAI) | configured, extended | arm-ttk, build, deploy-demo, deploy, gitleaks, npm-audit | 404 | #108 closed: 0 | 51 all kamilDatasec | #166: 3 |
| datasecau/Datasec-Security-Composer | configured, extended | none listed (404) | 404 | #91 open 0, #86 open 0, #55 closed 0, #54 closed 0 | 58 all kamilDatasec | #118: 2 |
Paths: GET repos/<r>/code-scanning/default-setup; contents/.github/workflows; contents/.github/dependabot.yml; pulls?state=all; code-scanning/analyses?ref=refs/pull/N/head; actions/runs?event=dynamic.
Conclusion: HPSM-POC is NOT advanced (belief corrected). No advanced-setup comparison exists; the pattern "bots 0, project-account PRs >0" is identical in all four repos. Composer's open bot PRs #86/#91 would hit the same block on any default-branch ruleset.

### Docs (WebFetch of docs.github.com; thin - several asked topics are absent)
- Troubleshooting Dependabot on Actions, https://docs.github.com/en/code-security/dependabot/troubleshooting-dependabot/troubleshooting-dependabot-on-github-actions : workflows triggered by Dependabot "receive a read-only GITHUB_TOKEN and do not have access to any secrets that are normally available"; "the only secrets available to the workflow are Dependabot secrets"; fix suggested: "a two-step process that includes pull_request_target which does not have these limitations". Page does not mention CodeQL.
- Automating Dependabot with Actions, https://docs.github.com/en/code-security/dependabot/working-with-dependabot/automating-dependabot-with-github-actions : Dependabot "is able to trigger GitHub Actions workflows on its pull requests and comments; however, certain events are treated differently"; Dependabot runs "bypassing both Actions policy checks and disablement at the repository or organization level"; advises requiring status checks for Dependabot PRs. No pull_request_target text there.
- Default setup, https://docs.github.com/en/code-security/code-scanning/enabling-code-scanning/configuring-default-setup-for-code-scanning : does NOT mention Dependabot or bot PRs. Switching to default "will disable the existing workflow file and block any CodeQL analysis API uploads" (so advanced and default are mutually exclusive).
- Customizing advanced setup, https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/customizing-your-advanced-setup-for-code-scanning : sample "uses the pull_request event to trigger a code scan on pull requests targeted against the default branch"; rulesets can block merge when "A required tool is not configured for the repository." Does not mention Dependabot, pull_request_target or "configurations not found".
- Page https://docs.github.com/en/code-security/code-scanning/troubleshooting-code-scanning/configuration-not-found returned 404 (UNMEASURED). The docs therefore give no statement of why default setup skips Dependabot PRs.

### Q3 Options for MPS
| # | Option | Change | Who | Risk | Cost | Reversible | Satisfies ruleset |
|---|---|---|---|---|---|---|---|
| A | Baseline: re-push bot branch as project account (or close bot PR, open own PR with the same bump) | none (procedure) | any seat with MPS push (MPS project seat; Tuesday only briefs) | none beyond the extra commit; bot PR history replaced | one `dynamic` run (4 analyses) per bump | n/a | Yes, measured (#157/#158 got 4 analyses) |
| B | Advanced setup codeql.yml on pull_request/push/schedule | disable default setup (repo setting), add .github/workflows/codeql.yml | MPS project seat, owner-approved | Dependabot run has read-only token; security-events:write may be withheld -> upload could fail (UNMEASURED); loses default setup auto language detection | similar to today (one analysis per language per PR) | Yes: delete file, re-enable default setup | Yes if upload succeeds on bot PRs - must be proven on a real bot PR |
| C | pull_request_target workflow running CodeQL | add workflow with write token | MPS seat | HIGH: runs base-branch workflow with write token/secrets; must not checkout PR head unvetted; analysing PR code via this trigger is the classic pwn-request pattern | same | Yes | Possibly; not recommended |
| D | Add Dependabot version-updates config (dependabot.yml) | file | MPS seat | none for scanning; may change PR shape/actor handling but no doc says it helps CodeQL (UNMEASURED) | none | Yes | Unknown |
| E | Weaken the org ruleset (remove code_scanning rule / add bypass) | org setting | owner only | removes the control; bypass_actors currently [] | none | Yes | Defeats it - not advised |

Ruleset note: it is org-level (source_type Organization), so any change is an owner/org-admin act, never an agent act.

### UNMEASURED
- Exact reason default setup skips Dependabot-actor PRs (no doc statement found).
- Whether an advanced-setup CodeQL job on a Dependabot PR can upload SARIF (token/permissions).
- Dependabot PR #120/#121 workflow-run detail beyond `ci` (Actions run logs not read).
