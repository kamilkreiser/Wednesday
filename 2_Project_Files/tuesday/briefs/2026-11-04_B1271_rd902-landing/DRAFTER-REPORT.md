STARTABLE: YES (all reads at 12:38-12:39 AEDT 2026-11-04, `date` in the same actions)

# B1271 drafter report: RD-902 landing kit (branch b1238/nexusai-rd902-risk-conditions-get-sync-admin-only)

## BLUF
Branch `bcdf835fa15c42300a2e5133d7efcad95b1faa01` and main `efcf86c59b7851e393da2472e1a73120fcdb3cbd` re-read by `gh api -X GET` (branches/main and git/ref/heads/...) at 12:39:06: both unmoved. Open PRs 0 (for the head filter and overall). Five files drafted beside this report. Nothing was posted, filed or pushed.

## Facts re-measured (instrument)
- Repo actions variables: `actions/variables` total_count 0; org variables via `actions/organization-variables` total_count 0; environments `["dev"]`. (No control that can fail was run on the variables endpoint; the gate's control was `variables/zzqxnonexist` 404, relayed.)
- Open code-scanning alerts on main: 123 (`--paginate`, ref refs/heads/main, state=open, `wc -l`); equals the gate's 123. Alerts on the changed paths: the gate read 0 (relayed, not re-read by me).
- Does a merge to main deploy anything? Read from `deploy-demo.yml` on main via `gh api contents | base64 -d | grep -n`: `:26 on:`, `:27 push:`, `:28 branches: [main]`, `:29-:32 paths-ignore ('**.md','docs/**','tests/**')`, `:33 workflow_dispatch:`; build job `:53 if: ${{ vars.CI_DEPLOY_ENABLED == 'true' && ...`; deploy job `:91 if: ${{ always() && vars.CI_DEPLOY_ENABLED == 'true' && ...`; `:95 environment: demo`. The branch changes backend/server.js and a test, so paths-ignore does not skip the run: **a merge starts a Deploy demo run, whose build and deploy jobs are skipped while CI_DEPLOY_ENABLED is unset (variables 0). Nothing deploys.** Other triggers on main push: build.yml `:7-:9` (push to main) and `:4-:6` (PR to main), gitleaks.yml `:32-:33`, npm-audit.yml `:9-:10`, arm-ttk.yml `:17-:18`; `deploy.yml:15` is workflow_dispatch only. I did not read their bodies for deploy steps.
- Last deploy-demo runs: my runs query returned null (jq error); NOT re-read. The gate's run list (41611324246 ... both jobs skipped) is relayed.
- Last 10 merged PR titles (pulls?state=closed, merged_at set): #164 "Records B1235: ...", #163 "RD-922: the reset script empties all six tables, pinned by a failure-path test", #162 "Records: ...", #161 "Records: ...", #160 "RD-917: streamExport rejects ...", #159 "Records B1187: ...", #158 "RD-904, RD-905, RD-906: retire ...", #157 "Records B1149: ...", #156 "RD-915, RD-920, RD-922: pin ...", #155 "RD-923: retire the legacy docker compose path". Code PRs carry `RD-nnn: lower-case sentence`; title therefore starts `RD-902:`.
- Merge-commit convention on main (commits API): f3ab00bd (#163) is a 2-parent merge with subject `RD-922: ...`, a body of short sentences, and exactly one trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; 682a7b01 and 2567293f likewise (the latter Sonnet 5.5). efcf86c5 (records PR) kept GitHub's default "Merge pull request #164 ..." subject. I followed the RD-code form.

## Landing rule, quoted (confirms the handover; no correction)
`/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:2067` (printed by `grep -n -i 'Merge path'`): "  2. Merge path: open a PR from the gated branch, wait for CodeQL (a background wait that EXITS), then land the SAME commit. Never squash, never rebase ([[C-68]]). The exact landing step is confirmed by Tuesday once M's pilot (merge 1, RD-681, PR #32) lands." Same entry at `:2062` (C-190) and `:2076` ADDENDUM: pre-scan both thresholds; a wait must require every `Analyze (<language>)` run completed (the `CodeQL` summary run shows neutral early). Recent landings (#163, #160, #158) are merge commits, which confirms MERGE, not squash.

## The gate record (B1260 STATUS; read whole)
NO GO round 2 of 2 on the class "the risk-conditions read path syncs only for the administrator check (RD-902)"; earlier round: B1246 NO GO round 1 of 2 on the same class (STATUS census line). Residue: one item B1260-1 (Major, restrictive, gate-added mutant MK): 24 of 1008 census cells; survives 399 tests in 17 files (219 + 180). Four round-1 holes closed. Verify at the merge result 5311/317 = committed. Hosted CodeQL/Build/Gitleaks, node 24/Linux, real-flow reachability, concurrent syncs, dashboard rendering of the empty list: UNMEASURED by the gate.

## Commands Tuesday would run (not run by me)
All under `GH_CONFIG_DIR='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`; verify `gh auth status` first.
```
D='/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-04_B1271_rd902-landing'
gh pr create --repo datasecau/Reporting_Dashboard_Au --head b1238/nexusai-rd902-risk-conditions-get-sync-admin-only --base main --title "$(cat "$D/pr-title.txt")" --body-file "$D/pr-body.txt"
# wait until every Analyze (<language>) check run is completed (C-190 item 2 note), plus Build, Gitleaks, npm-audit; read for new high+ and rule-severity error alerts; never dismiss
gh pr merge <n> --repo datasecau/Reporting_Dashboard_Au --merge --match-head-commit bcdf835fa15c42300a2e5133d7efcad95b1faa01 --subject "$(cat "$D/merge-subject.txt")" --body-file "$D/merge-body.txt"
```
Before merge: re-read main (expected efcf86c5; if it moved, stop and tell the product owner's coordinator, because the gate's merge-result verify was at efcf86c5), and branch head (bcdf835f; `--match-head-commit` refuses otherwise). After merge: read the deploy-demo run for the merge commit, both jobs skipped. A ref write on the project repo through `gh pr merge` is Tuesday's landing per DRAFTER_RULES; this drafter ran none.

## D-decisions
- D1: merge subject differs from PR title (adds "read-path"); both start `RD-902:`.
- D2: PR body and merge body name the ruling as "the product owner's 2026-11-04 ruling" with no person or card id; merge-body says "gap ticketed" without a ticket number (none exists yet).
- D3: ticket.md cites `backend/server.js:20993` and `:462` as the gate's line numbers at bcdf835f (relayed from STATUS, labelled so; I did not re-grep them at the sha).

## Q-questions for Tuesday
- Q1: Add the ticket key to pr-body/merge-body once a records seat files it? Default: no; land first, the ticket cites the merge.
- Q2: The branch's second commit has a personal local author identity (gate note). Default: land as is (history must not be rewritten; the merge commit is authored by the merge actor).
- Q3: If hosted CodeQL flags a new high+ or rule-error alert in the test file: default STOP, report, no dismissal, no third review round without the product owner's word.

## UNMEASURED
Hosted Build/CodeQL/Gitleaks for this head; Linux node 24; recent deploy-demo run list (my query failed); alerts on changed paths (relayed); whether the PR body's behaviour-difference sentence matches the dashboard (V2 shape, gate-measured at the API only); `deploy.yml`, `arm-ttk.yml` bodies for deploy steps (only triggers read); the gate's numbers other than the ones I re-read are relayed from B1260 STATUS and not re-run.

## Outside-the-fences disclosure
One Bash call of mine contained a `cd` and was refused by the hook (no effect). One call with an unquoted `==` was refused by the hook. No other fence touched; no git in a project repo; `gh api -X GET` only; no card store, Jira or HTTP to hosts. Wrote only the six files in this folder. The tool-results spill file for the STATUS read lives under the harness's own directory.
