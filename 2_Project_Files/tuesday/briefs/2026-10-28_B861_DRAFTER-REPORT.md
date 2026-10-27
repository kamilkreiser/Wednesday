STARTABLE: YES (once stamped; no open ruling, no new customer-facing word, no port, no product byte; the one judgement call is Q-1)

# B861 drafter report (MPS MPSCALC-347, publish-output deps.json row, seat Datasec/MPS-M51)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B861_SEAT-M51_mps-347-publish-deps-row.md` (148 lines; `.pre-stamp` copy beside it, 8 lines with the four-underscore pattern, as the B843 shape). Drafted 2026-10-28 (clock = `date`, first read 02:36 AEDT).

## BLUF
- One test file (`tests/MpsCalc.Api.Tests/PublishOutputTests.cs`), no product byte, +1 test name. Default shape: move the 12 assertion lines 74-85 of the B160 Fact into a private helper that takes the output folder, and add one Fact that publishes, copies the output, removes only the Pkcs entry from the copy's `MpsCalc.Api.deps.json` (DLL kept), and asserts the helper throws with the line-83 message. Reusing the real line 83 is the point: a duplicated check would prove nothing about it.
- Red-proof is by five mutants of the helper (weaken 83, reorder 83 after 84, delete 83, make the row's removal a no-op, trip line 78 first) plus two plants, all in a mutant worktree; one informational csproj cell.
- Model Sonnet `claude-sonnet-5-5` (`models_latest.json` line 38), L6 `model-routing.md:85`, C2 `:92`, gate G2 `:109` tier 2, G-cap `:111`, round 1 of 2. SDK path named for every dotnet call: `<project>/.tools/dotnet/dotnet` (10.0.401). Ports none. Branch `b861/mps-347-publish-deps-row`.

## Facts re-measured (instrument, control)
- Main: `gh -X GET api .../git/ref/heads/main` = `080f1608abc7278969ec34950f7357534536d448` (the sweep's value); `pulls/131` closed, merged true.
- Jira: MPSCALC-347 read whole through the project `.env` in a scratchpad reader (GET, no token printed): Backlog, Medium, created 2026-10-26, labels mpscalc-b751 / plan-b751-b722-1 / tier-2, 0 comments, 0 links. Control: MPSCALC-99999 returns 404. Scope and Done-when quoted verbatim in the kit (Acceptance check matches the lane text).
- Test file at main (raw): 87 lines, 4,952 bytes, blob `38b23babcfed...` equal to the ticket's `38b23bab`. Lines read whole: assertion 83, existence 75, version 78, file version 85, `PublishAsync` 33-47 (`--no-build`, `DOTNET_HOST_PATH`).
- Open PRs #121, #120: each lists only `web/package-lock.json`; `compare main...` of `b820` (FeedbackTriageTests.cs), `b821` (QuoteWalkCaps.cs) and the stale `b843` branch (FeedbackTicketTests.cs, ahead 1 behind 1, landed as #131) share 0 with Yours. `heads/b861` 0 refs; no `.tools/b861`; control `.tools/b789` lists.
- Csproj (raw): pin `System.Security.Cryptography.Pkcs` 10.0.14 at line 28, `PreferPinnedPkcsOverSharedFramework` target at 35-39. `Directory.Build.props`: `TreatWarningsAsErrors` true, `AnalysisLevel latest-recommended`. `ci.yml` 38-43: build Release then test `--no-build`.
- Gate table (B722 STATUS lines 121-128 and 178) read: line 83 unpinned because every csproj edit that drops the DLL fails at 75 first, hence the copy approach.
- Model-routing lines 85/92/109/111 printed and match. Panes at drafting: `tuesday`, `Datasec/HPSM-POC-H48`, `Datasec/NexusAI-M50`, `Datasec/NexusAI-M49`, `fleet-monitor` (no M51). Kit scan for `M51` over 26-28 Oct non-`.pre-` kits: 1 hit, the B843 kit, where it only appears in a list of names that read 0. Heavy slot / git lock: none at drafting (`ls .tools | grep -E 'heavy|git-lock'` empty); load1 5.07 at the last read.
- Hygiene: kit has 0 non-ASCII bytes, 0 person names, 0 Wednesday/Friday, 0 `PHASE`, 0 `D-` card ids; 8 lines hold the four-underscore pattern (7 slots + last line).

## D-decisions (override at the stamp)
- D1 Sonnet. D2 +1 added name, 0 lost. D3 add the row; "accepted as structural" is NOT taken (Tuesday's call). D4 extract the 12 assertion lines verbatim into a helper (the only way the row exercises the real line 83). D5 base is main at Step 0; STOP only if Yours, the csproj, `global.json` or `Directory.Build.props` moved. D6 one commit, subject suggested. D7 name multiset lost 0 added 1. D8 pane `Datasec/MPS-M51`. D9 one push, new branch. D10 no ports. D11 helper name is the seat's.

## Q-questions for Tuesday (each with a default)
- Q-1: the helper extraction moves 12 existing lines (byte-equal modulo `_out` -> `outputDir`), unlike an insert-only lane. Default: accepted; the alternative (a duplicated check in the new row) would not pin line 83.
- Q-2: ports. Default: none (publish plus file reads); the seat STOPs and asks if it finds it needs one.
- Q-3: round count. Default: round 1 of 2 on the new PR, tier 2 (the originating gate B722 was round 1 of 2, GO WITH FOLLOW-UPS, no Major).
- Q-4: seat name `M51`. Default: keep; re-scan panes and kits at the stamp (the wave's other drafters pick names in parallel).
- Q-5: should "accepted as structural" ever be recorded instead? Default: no; the row is cheap, the ticket's own first alternative needs a Tuesday decision and none is on file.

## UNMEASURED
- Nothing was built or run (no dotnet, no publish, no compile). Not measured: that the extraction compiles at 0 warnings; the xunit major version and the exception type/message shape (kit tells the seat to measure it, not guess); that SDK 10.0.401's publish lists exactly one Pkcs entry; the runtime added by one more publish; whether the csproj product-side cell differs on 10.0.401 (the ticket's tie is a 10.0.403 shape).

## Outside-the-fences disclosure
Read-only: Jira GET via a scratchpad reader that loads the MPS `.env` in process (no token printed, file `jm.py` in the session scratchpad), `gh -X GET api` under the project `GH_CONFIG_DIR` (ref, contents raw, pulls, pulls/files, compare, matching-refs, commits), `tmux list-panes`, `uptime`, local reads of the B843 kit/report/STATUS, the sweep, `model-routing.md`, `models_latest.json`, B722 STATUS lines. Two Bash calls were refused by the no-`cd` hook and re-issued; one `rm` of my own `.pre-stamp` copy was refused and the copy was kept (sibling kits keep one). Wrote only the kit, its `.pre-stamp` copy and this report.
