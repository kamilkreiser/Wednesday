STARTABLE: YES (pins hold: main df1dc0fe25e87dda4a9748c14870f942371a58a5, no b859 ref, no pane H49, ports 9830-9839 unlistened; one fetch is owed by the seat because the local clone lacks df1dc0fe; tier 1 gate, Tuesday states the round at stamp)

# B859 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H49: HPSMPOC-359 and HPSMPOC-360, open sign-in wording)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B859_SEAT-H49_hpsmpoc-359-360-open-signin-wording.md` (124 lines; shape of the stamped sibling kit B858, with four paths instead of one). Drafted Wed 28 Oct 2026, read-only: nothing built in a project tree, no fetch, no ref written; reads on a tarball extract of `df1dc0fe` in the session scratchpad.

## BLUF
- Startable. One commit, four paths, wording only: `infra/env/uat.bicepparam` line 3, `api/src/HpsmPoc.Api/Auth/UatOpenAuthentication.cs` line 134, `web/src/server/auth/config.ts` line 91, `infra/README.md` lines 227-233. All four texts confirmed at `df1dc0fe`.
- **Gate: TIER 1** (routing row G1, line 108): two of the four files are auth source, text only. Round 1 of 2 on a new class; Tuesday states it at stamp. Model Sonnet (C2 line 92, id `claude-sonnet-5-5` from `models_latest.json` line 23).
- The sweep's UNMEASURED item is now measured by reading: of the 13 files that mention `uat-open-key`, none asserts either old parenthetical. Test keys and `@Microsoft.KeyVault(SecretUri=.../uat-open-key/)` are INPUT strings; `UatOpenTests.cs` 184-186 asserts only the leading `unresolved Key Vault reference`; `uatOpen.test.ts` 70-73 asserts only `kind` is `off`. The web reason is read by `routes.ts:19` as an operator `console.warn`, and `uatOpen.demo.test.ts` 100 and 105 assert other texts. Still UNMEASURED by run; the kit makes the seat read all 13 and run the three suites before and after (Property T and R).
- Infra readers: `test_deploy_package.py` opens the README (474, 520, 686) but not the "two locks" paragraph; `test_security_baseline.py` line 1596 and `validate.sh` line 18 run `bicep build-params` on the bicepparam, so the comment edit is checked by a byte-equal params JSON for three environments.
- Test routes: api = dotnet restore/build/test of `HpsmPoc.Api.Tests` on SQLite (SDK pin 10.0.401); web = lint, typecheck, `vitest run` (`web/package.json` 7-12); infra = whole `test_security_baseline.py` run under both interpreters. Web e2e and `npm run build` are NOT run (a port and heavier than text needs).
- Ports: reserve 9830-9839, expected unused (`lsof` on the block printed nothing; the seat must not run e2e, whose config defaults to 3100).

## D-decisions (taken by the drafter; Tuesday accepts or changes at stamp)
- D-1 One commit, four paths; a fifth (a test file) only if the seat's Property T finds a pinned text, named in STATUS before it is edited.
- D-2 Defaults from the sweep: bicepparam "are on in uat and demo"; both parentheticals say "the open sign-in key" (the leading part of each text byte-equal, so the pinned substring survives); the README is worded by the seat from the code, the ticket's site-name sentence checked against `config.ts` and the API source (the code wins).
- D-3 The README edit covers both tickets' sentences (the "two locks" marker clause and the "uat-open-key ... UAT vault only" sentence), per ticket 360's own note that one edit covers both.
- D-4 Red-first is adapted to a wording change: suites before and after with equal counts and names lost 0 added 0, plus one scratch control that the existing row at `UatOpenTests.cs` 185 goes red when the LEADING words are changed (it guards the leading part, not the parenthetical). Chosen over inventing new tests (the lane is wording only).
- D-5 A program strips comments and string literals from the base and fix blobs of the two source files and compares them, so "no code token changed" is shown, not asserted.
- D-6 No `npm run build`, no e2e, no browser, no `az`: said in NOT TESTED. Whether api/web jobs are required checks on main is left for the seat to read from `rules/branches/main`.
- D-7 Hard-stop suggestion: target READY 150 minutes after Step 0, hard stop 240 (three suites behind a heavy lock that may wait on load 7+).
- D-8 `bicep` binary made an execute-only exception to the read-forbidden `.tools/b*` rule (as the sibling kit).

## Q-questions for Tuesday (each with a default)
- Q-1 Gate round. Default: NO GO 0 of 2 on a new class, round 1 of 2, tier 1 (G1 line 108); if Tuesday prefers tier 2, split the two auth-source texts into their own lane.
- Q-2 Is a test-file edit allowed if Property T finds an assertion on an old text? Default: YES in the same commit, named in STATUS first, never loosening; a pin that cannot move without a behaviour change is a STOP.
- Q-3 README wording: seat's own, in the file's voice, ASCII, true for uat and demo. Default: yes; the paragraph's heading "(B409)" and existing ids stay untouched.
- Q-4 Jira. Default: NO Jira write by the seat (records follow after landing).
- Q-5 Ports. Default: reserve 9830-9839, none expected; the seat STOPs if a route needs more.
- Q-6 Launch order beside the running infra-test lane (H48, one HPSM-POC path, none shared). Default: launch independently; load gate applies (3.82 at the read; a dotnet test is heavy, so the waiter's load1-below-7 rule matters).

## Facts re-measured (instrument, control)
- main `df1dc0fe25e87dda4a9748c14870f942371a58a5` (`gh api -X GET commits/main`); `ls-remote 'refs/heads/b859*'` printed nothing, `'refs/heads/b85*'` printed one ref, `b85/hosted-demo-wave2` (control: it lists). Panes: `tuesday`, `fleet-monitor`, `Datasec/Security-Composer-J29`, `Datasec/HPSM-POC-H48`, `Datasec/NexusAI-M50`, `Datasec/NexusAI-M49`; no H49. `uptime` load1 3.82.
- Blobs (hash-object of tarball bytes): uat.bicepparam `de8677f5...` (30 lines), UatOpenAuthentication.cs `a900d479...` (233), config.ts `0311447b...` (145), README `9f69fb3a...` (240). The seat re-measures with `rev-parse`.
- `grep -r -l -i -F 'uat-open-key'` printed 13 files (the sweep's 13); zero control printed 0. Role of each hit listed in the kit's Fact marks.
- Tickets read whole by the project's Jira helper (GET): both Backlog, 0 comments, scope, fix shape and Done-when quoted verbatim in the kit.
- Sibling partition named from both sides: H48 (B858) edits only `infra/tests/test_security_baseline.py`; H50 (B860, later) edits `web/src/components/shell/HpLogo.test.tsx` and one new `web/e2e` spec.
- Kit hygiene by program: four-underscore lines 8; at-sign tokens 0; clock-time pattern 0; person-name pattern 0; non-ASCII bytes 0 (python count); no card id.

## UNMEASURED
Any suite run (api, web, infra) at base or fix, base pass/skip counts, dotnet/node versions on this machine, whether api and web jobs are required checks on main, whether any host-start test beyond `UatOpenTests.cs` 185 reaches the refusal text (the seat reads all 13), the runner's Python, and GitHub's parser.

## Outside-the-fences disclosure
Read-only everywhere except the two files written here. `gh api -X GET` only under the project's `GH_CONFIG_DIR` (commit, tarball, auth status); `git --no-optional-locks ls-remote`; one Jira GET each for the two tickets through the project's helper (first 60 lines read with credential lines filtered), output saved in the scratchpad. A repository tarball of `df1dc0fe` was extracted in the scratchpad only. `tmux list-panes`, `lsof`, `uptime`. No `az`, docker, ssh, hosted HTTP, mail, Artifact/Docs tool, decision store or other project touched. The `gh auth status` read printed the account login; it is not written to either file. Several hook advisories (case-sensitive grep) appeared; every count that matters is a count of one literal paired with a control above.
