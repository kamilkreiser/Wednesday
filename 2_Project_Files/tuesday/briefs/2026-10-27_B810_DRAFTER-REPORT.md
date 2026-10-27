STARTABLE: YES after your stamp, but NOT before B804 ends. The kit refuses any hosted write until B804's last line begins `DEPLOYED: UAT + demo @ d415a3fe` (MEASURED 10:5x: B804 STATUS is at "PART A: not started", last line a CHECKPOINT). Stamp slots: 9 plus the last line = 10 runs of four underscores (MEASURED `grep -o -E '_{4}' | wc -l` = 10). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B810_SEAT-D38_hpsmpoc-demo-chooser-deploy-switch-on.md` (140 lines). Drafted 10:4x-11:0x AEDT Tue 27 Oct 2026.

# B810 DRAFTER REPORT

## BLUF
- Deploy `S` = `bf4a7bdd` (squash of #232, one parent `d415a3fe`, 5 paths) to BOTH demo apps from CI artifacts, then give the demo its own key, then switch on, API first and web second. UAT untouched and not requested: the gate measured UAT unchanged by #232 (UAT cells differ 0).
- **CI run `40420821396` was still `in_progress` at 10:52** (15 jobs listed, 0 incomplete, both deploy artifacts already `expired=false`). The kit waits up to 40 minutes for `completed/success`.
- **One hazard the gate did not name, built into the kit:** a Key Vault reference that fails to resolve reaches the app as its literal text, which is longer than the 32-byte minimum and would be accepted as the shared key on both apps and agree between them. The kit forbids any switch write until both references read `Resolved`, and the live check tries that literal as a key and expects 401.
- **Entra on the demo stops while the switch is on** (gate: `/api/auth/signin` and callback 404). See Q-2.
- Key mechanism copies the project's own runbook (README step 1 and 4): secret by file descriptor in the DEMO vault (`demo-open-key`), a vault reference setting on each app, refresh, then stop/start (not restart), switch last. Ways back: `rollback810off.sh` (settings only, web first) then `rollback810build.sh` (the `d415a3fe` packages).

## Facts re-measured (instrument; control)
1. `pulls/232`: merged true, `merge_commit_sha` = `bf4a7bdd...`, head `23d5a276` (`gh api -X GET`). `commits/S`: one parent `d415a3fe`; 5 files as listed. `compare d415a3fe...S`: ahead 1 behind 0; reversed: behind 1 (control fires).
2. `ls-remote origin refs/heads/main` = `bf4a7bdd...`. Open PR #222 exists (unrelated paths per gate). Open code-scanning alerts on main: 0 (information; no positive control run).
3. `deploy-from-ci.sh` blob `0024302d1ea3` and `deploy-package.py` blob `77dc49939859` equal at `d415a3fe` and `S` (`contents?ref=`).
4. CI run list for `S`: `ci` push 40420821396 `in_progress`; `Push on main` dynamic 40420820704 completed success.
5. Ports 8970-8979: `lsof` 0 listeners; word-boundary scan of non-`.pre-` SEAT kits of 26 and 27 Oct: 0 hits; control `890[0-9]` hits 1 (B804), fires. Live panes: tuesday, Datasec/Security-Composer-J25, -R58, Datasec/NexusAI-M20, Datasec/HPSM-POC-G170, -D37, Datasec/MPS-R57, Datasec/NexusAI-G169, fleet-monitor (none holds 897x).
6. Model: row C6 at `model-routing.md` line 96 (Opus `1st`); `claude-opus-5-5` at `models_latest.json` line 17.
7. Bicep at `S` (`appservice.bicep`): `:147` / `:148` API switch and key reference uat-only; `:211` / `:213` web switch and key reference uat-only; `:212` `HPSM_ENVIRONMENT = environmentName`; `:221` `AUTH_SECRET` is a reference to `bff-session-key` in the environment's own vault; `:100` `Assessment__Environment = environmentName`. Header `X-Uat-Assertion`, `MinKeyBytes` 32, demo API name constant (`UatOpenAuthentication.cs`). Demo Key Vault role: RELAYED B410 STATUS (Secrets Officer on the demo vault since 3 Oct), UNMEASURED today.
8. B783 STATUS: the five UAT-only setting names are ABSENT on the live demo, so the kit writes those names itself (D-4), not just flips values.

## D-decisions
D-1 pin `S`. D-2 key = vault secret by fd + vault reference settings (the project runbook), not a plain app-setting value. D-3 secret named `demo-open-key`. D-4 additive settings only, names listed. D-5 API first for ON, web first for OFF. D-6 live check mints assertions in-process, proven first against a local pair of the exact zips. D-7 no destructive probe live; one harmless `DELETE` of a random GUID. D-8 wake databases, last read `/health/ready`. D-9 LIVE-BEFORE tags, no Azure/git tags. D-10 UAT/demo skew accepted.

## Q-questions for Tuesday (each with a default)
- **Q-1 Hard stop and B804 timing.** B804's own hard stop is 13:30. Default: stamp B810 hard stop 16:00, and launch B810 only when B804 shows a final `DEPLOYED:` line (the kit waits 20 min then stops).
- **Q-2 Demo Entra sign-in is replaced while the switch is on** (gate-measured: signin/callback 404). Anyone relying on the demo Admin Entra login (including HP-facing rehearsal) loses it until switch-off. Default: accepted as part of "switch it on" (slot 9(c) says so); say NO at the stamp if it is not.
- **Q-3 Key mechanism:** vault + references (default) vs plain app-setting values. Default: vault + references, because it is the runbook's own pattern and keeps the key out of settings; costs one extra refresh and stop/start cycle (a few minutes more).
- **Q-4 Entra BEFORE visit** needs the three `HPSM_POC_DEMO_*` names in the project `.env`. Default if unavailable: continue, using the Consultant row count as the post-switch baseline, recorded UNMEASURED-before.
- **Q-5 UAT vault read for the "not UAT's" compare** works only if the login already holds a data role there. Default: compare if readable, else prove by construction (separate vaults, creation times, version ids) and say so.
- **Q-6 Landing note:** the seat does not rewrite the template; the card for the template change (so a later template deploy keeps the switch) is yours. Default: raise it from the seat's FOR TUESDAY.

## UNMEASURED
Live state of both demo apps and their settings today; the demo vault's contents and the login's data role; whether CI `40420821396` finishes green; whether the `PREV` artifacts (run 40383065653) are still unexpired when the seat needs them; B804's outcome; whether the demo holds non-sample data (B799-3); the exact path of the chooser's POST (the seat reads it from the page).

## Outside-the-fences disclosure
Read-only only: `gh api -X GET` (pulls/232, commits, compare, actions runs/jobs/artifacts, contents of appservice.bicep, README.md, UatOpenAuthentication.cs, config.ts, code-scanning alerts) under the project `GH_CONFIG_DIR`; `git --no-optional-locks ls-remote`; `lsof`; `tmux list-panes`; reads of B799/B804/B410/B783 STATUS, the B804 kit and report, `rollback783demo.sh`, `model-routing.md`, `models_latest.json`. Scratch copies of bicep/README/source fetched into the session scratchpad only. No HTTP to hosted hosts, no az/ssh/docker, no decision-queue command, no briefs_staged, no ledger. One advisory hook (case-sensitive grep) fired once; no effect on any count in this report. Wrote only the two files.
