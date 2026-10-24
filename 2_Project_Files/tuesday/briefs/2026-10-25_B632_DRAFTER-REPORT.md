STARTABLE: YES, with one caveat on deploy exposure that is not caused by this lane (see BLUF line 2). The change does not touch `deploy-demo.yml`, any deploy trigger, secret, environment or variable, and it cannot widen a permission. Recommend: launch, but confirm decision 1 at the stamp.

# B632 DRAFTER REPORT (Datasec / NexusAI, lane N-CI, RD-814, SEAT-M7)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B632_SEAT-M7_nexusai-ci-814.md` (UNSTAMPED, 136 lines, 9 lines carry the four-underscore pattern: 8 slots plus the last line; control: a scratch line with four underscores reads 1). 0 non-ASCII bytes in both files (control: a planted e-acute reads 1; one tab in the first draft was found and replaced). No person's name in the brief (program check, 0).

## BLUF
1. Startable: yes. RD-814's change is four added lines (`permissions: contents: read` plus a comment and a blank) before `jobs:` in `build.yml`, `deploy.yml` and `npm-audit.yml`. It touches no deploy trigger, no secret, no environment, no variable and widens nothing: the repo's default workflow token is already `read` (GET `actions/permissions/workflow`), and none of the three files has a `permissions` key today.
2. Caveat for Tuesday (not caused by this lane): `deploy-demo.yml` runs on every push to main that is not only `*.md`, `docs/**` or `tests/**`, so any merge (this one, PR #110) starts a `Deploy demo` run. All 14 past push runs are `skipped`; every job is gated on repo variable `CI_DEPLOY_ENABLED`, which is unset (repo variables 0, organisation variables 0). Also: `environments` lists only `dev`; `environments/demo` is 404, so the earlier fact that `demo` carries a required reviewer is not visible today. If the variable were ever set, the deploy job would bind an environment that does not exist by that name. That is the RD-815 / card-candidate question, not RD-814.
3. The sweep's UNMEASURED item is answered: none of the three jobs has an OIDC login (`id-token` appears only in `deploy-demo.yml`), so `contents: read` suffices by reading; the narrowed token itself is not yet run (see UNMEASURED).
4. Tier 1 gate kept as ordered (routing row G2 would allow tier 2 for config/CI; tier 1 because it is a CI-permission change and RD-814 asks for its own review).

## DECISIONS FOR TUESDAY AT STAMP
1. Accept the deploy-exposure caveat (BLUF 2): any merge starts a skipped `Deploy demo` run. Recommend yes, launch; it is the same exposure as PR #110. If you want zero such exposure, the answer is RD-815's separate ruling, not holding this lane.
2. Placement: workflow-level `permissions` (one job per file, same four lines in all three). Recommend yes; the brief's check program also accepts the job-level shape.
3. No whole verify (27 minutes of lock time) and no new test cell; instead a Ruby check program (red at main x3, green after, 7 mutants) plus one jest ticket over the three tests that read workflow files, and the PR's `Build` runs the whole verify. Recommend yes. A new cell would edit `scripts/verify-expected-counts.json`, which PR #67 edits.
4. `deploy.yml` (Package, `workflow_dispatch` only, last runs two `failure` from 2026-08) is never run automatically, so its narrowed-token behaviour is unproven until a dispatch. Recommend: Tuesday decides after landing whether to dispatch it once (a gh write; packaging only, deploys nowhere). The builder never dispatches.
5. Gate tier 1 (Opus), as ordered. Recommend keep.
6. Environment `demo` 404 finding: recommend Tuesday records it on the RD-815 card candidate. Not in the builder's lane.
7. Target READY 2 hours, HARD STOP 4 hours after launch (shorter than B617: no whole verify). Recommend yes.

## Facts and the instrument for each
- Main `19b7106b9f2930507185e0a231408cc11a986ecb` at 06:00:42 AEDT: `gh api git/ref/heads/main` and `ls-remote`. Open PRs #110 (head `2f9c3e1b`, 3 files, branch `b617/...`) and #67 (head `94b288cc`, 3 files): `pulls`, `pulls/<n>/files`. MEASURED-BY-DRAFTER.
- Intersection A (3 workflow paths) with B (6 paths of #110 and #67) = empty (`grep -x -F`, rc 1); planted control (build.yml appended to B) printed 1. The #110 branch compared with main lists the same 3 non-workflow paths, workflow overlap rc 1. Seats B628-B631 are not NexusAI.
- Workflow files and blob shas: `contents` GET (build 0cd3fbff, deploy eb43ac92, npm-audit d546ec2d; others in the brief). 80, 92, 47 lines; no `permissions` key; one `jobs:` line each. Read by `cat -n` of the raw files.
- No `GITHUB_TOKEN`/`github.token`/`npm.pkg.github` anywhere outside `node_modules` (program search of the extracted main tarball; no `.npmrc`): 0 files. Controls: the same family of searches found `permissions` in `gitleaks.yml`/`arm-ttk.yml` and `id-token` in `deploy-demo.yml`.
- Alerts #1-#3 open on main (`code-scanning/alerts`); ruleset 24139430 (CodeQL errors + high_or_higher, empty required status checks); default-setup CodeQL is not a file in `.github/workflows` so nothing to weaken. C-190 (`:2062`), addendum (`:2076`), C-68 (`:665`), C-209 (`:2270`) read by line.
- Which workflows run on a branch push: from the `on:` blocks and `actions/workflows/npm-audit.yml/runs` (two `success` runs on the PR #110 branch). Build and Gitleaks run on PR; Package dispatch only.
- Tests reading the workflows: program search of the tarball; `verify-suite-gate.test.js:487` (build.yml), `rd327...:324` (deploy-demo.yml), `rd630...` (arm-ttk.yml). A new permissions block matches none of their patterns.
- Prior work: `commits?path=` x3 (newest `a11eb5f1`, RD-641); JQL with parentheses, positive hits RD-814 plus six prose-only tickets, nonsense control 0. RD-814 has 0 comments, status To Do, and no "Done when" line (the brief's Done-when is Tuesday's, stated in THE LANE).
- Ports 9820-9829 free (`lsof` rc 1); word-boundary scan of 2026-10-24/25 briefs matched 0 files (no bind control run by the drafter; the brief makes the builder run one). Pane `Datasec/NexusAI-M7` not in `tmux list-panes`. Lock tool sha `3c33f5ae...` equal; `queue-jest` empty.
- Tools: `actionlint` not installed; Ruby 2.6.10 `yaml` works (and reads the key `on` as boolean `true`, handled in the brief); Python has no `yaml`; `js-yaml` 3.15.2 is in the lockfile.
- Model: row C2 (Sonnet first), `claude-sonnet-5-5` read from `models_latest.json`.

## UNMEASURED
- That the three jobs pass with the narrowed token (nothing was run; PR `Build`, the branch `npm-audit` run, and a Package dispatch would show it). Specifically upload-artifact@v4 and the setup-node cache needing no scope beyond `contents: read` is reasoned, not run.
- That a workflow-level block closes alerts #1-#3 (read on main after landing, C-209).
- That the deploy key may push a branch changing `.github/workflows/**` (earlier builders pushed none; the brief makes a refusal a STOP).
- GitHub's own parse of `deploy.yml` (no automatic run); `actionlint`.
- Org-level environment `demo` under another name; the drafter only GET-ed by name.
- The no-bind-control for ports (builder does it); other seats' (B628-B631) paths beyond the sweep's claim of disjointness (builder re-proves the intersection at launch and before push).
- The drafter parsed only `build.yml` with Ruby; the other five files were read, not parsed.

## Outside-the-fences disclosure
- Read-only throughout: gh GET only (one tarball GET of main, extracted in the session scratchpad, which is an `x-tar` download of repo content, not a clone or fetch), Jira GET, no git write, no build/test. Scratch files only in the session scratchpad (`.../scratchpad/n7/`).
- No other client's material shown. No decision queue, staged briefs or coordinator ledger opened. `CLARIFICATIONS.md` was read by line range (NexusAI project file). The three hook refusals met (`=====` echo, a `cd` inside a bash -c) were mine and blocked nothing.
- Not done: the brief was not stamped; no PR, Jira, mail or Artifact/Docs tool used.

Return summary: briefs `.../2026-10-25_B632_SEAT-M7_nexusai-ci-814.md` and `.../2026-10-25_B632_DRAFTER-REPORT.md`; 9 slot lines (8 slots plus the last line); startable yes; decisions listed above.
