STARTABLE: YES

# B720 DRAFTER REPORT (seat M30, MPS Commercial Calculator, CI-red fix on main 1ac8ab8a)
Drafted 2026-10-26 08:56-09:1x AEDT (clock from `date`). Kit: `2026-10-26_B720_SEAT-M30_mps-b160-pkcs-publish-runtime-10014.md` (132 lines, 8 four-underscore slot lines, 0 non-ASCII bytes, 0 person names).

## BLUF
- The break is the B160 guard doing its job: it says the SDK's framework Pkcs is now newer than the pin (10.0.13), so the publish drops the app copy. The recorded fix (B160 STATUS "BACKLOG new" line and the test's own doc comment, PublishOutputTests.cs:67) is (a): raise the pin to 10.0.14. The kit commissions (a), one path (`src/MpsCalc.Api/MpsCalc.Api.csproj`), one commit.
- (b) is the wrong fix: with the app copy dropped, a host older than the SDK (last recorded 10.0.12) runs its own unpatched Pkcs, the exact thing the pin exists to stop. (c) is weakest: setup-dotnet installs the runtime by `--channel 10.0` whatever global.json says, and a pin freezes CI's patches.
- No product-owner ruling on Pkcs, B160 or the SDK pin exists in CLARIFICATIONS (grep with control). So the (a)/(b) choice is technical and inside the delegated scope.
- The mechanism (framework file version above the pin's, so rank is never consulted) is UNMEASURED until the seat's Step 3. The kit STOPs if (a) does not keep the DLL, rather than falling back to (b) or (c).
- Builder Sonnet (C2, routing line 92), gate Tier 1 Opus (G1, line 108). Ports 9870-9879, listens on nothing.

## Facts re-measured (instrument; control)
1. Main = `1ac8ab8aca9573aacf022860b3963e867e559fb1` (`git ls-remote`; its parent is `f5a27af0`, `gh -X GET commits/...`.parents). The local checkout is stale: `git cat-file -t 1ac8ab8a` printed "Not a valid object name", so everything was read from origin.
2. Red job 121301097414 (run 40237171081, 21:48Z), log read with `gh api -X GET --allow-escape-sequences`: runtime `Installed version is 10.0.14` via `--channel 10.0`, SDK `10.0.403`, build 0 warnings, Engine 435 passed, Import 183 passed, Api `Failed: 1, Passed: 3011, Total: 3012`; the failure is the B160 test with the message at line 75.
3. Green control: run 40193990286 (main `f5a27af0`, 12:38Z, success): runtime 10.0.13, SDK 10.0.402, Api 2972 passed. #118's run 40234991031 is `failure` (its failing test not re-read).
4. Pin and target: csproj line 27 `Version="10.0.13"`, lines 34-39 the `PreferPinnedPkcsOverSharedFramework` target. Counts by `grep -n -F` over the raw file; control `zzz-no-such-string-7f3a` printed 0.
5. Test: `PublishOutputTests.cs` line 70 (name), 78 (`new Version(10, 0, 13)`, the first patched version, stays), 67 (doc comment: raise the pin).
6. nuget flat-container lists 10.0.14 (the list also holds 10.0.13, the control).
7. B160 STATUS (merged `25de7c1c`): SDK order is override, assembly version, file version, package rank, platform (STATUS line 26). That is why a higher framework file version beats the ranking target. B160 FOUND 4 explains why SDK 10.0.401 kept the DLL; the kit uses the project's `.tools/dotnet` (10.0.401, `--list-sdks`) as the old-SDK control.
8. Census of "10.0.13"/"Cryptography.Pkcs" in 259 raw files (scripts, infra, docs, tools, .github, test csproj/cs): 10 hits, all PublishOutputTests.cs or the Api.Tests Xml pin (not published). Frame excludes `src/**/*.cs` and `web/`; the src project files hold no PackageReference except Api's. Control: non-empty hit list.
9. Open PRs: #117 (1 test file) and #118 (ParityProof.cs + new Import test). Disjoint from the one path. `refs/heads/b720*`: 0 (`matching-refs` length 0). `.tools/b720`, `wt-b720-*` absent; `.tools/b711` exists (control for the REFUSE ls-d). heavy-slot-1 holder reads `B715 08:44:47 mutants`; slots 2 and 3 absent.
10. Ports: `lsof -nP -iTCP:9870-9879 -sTCP:LISTEN` printed nothing (rc 1); control: a python listener on 9870 was listed, then freed. Word-boundary scan of non-`.pre-` SEAT kits of 25 and 26 Oct (110 kits): hits B637 (G102), B642 (M8), B691 (G124), B693 (G126), all other repositories (NexusAI/HPSM-POC); none MPS. Control: the same scan of B711 reports its own 978x (4 lines). Live panes: MPS-G135 only for MPS; MPS-M29 not launched yet.
11. Load 7.98 at 09:00 (`uptime`): the seat waits for below 7.
12. Routing lines 92 (C2), 108 (G1), 111 (G-cap) read; model id `claude-sonnet-5-5` in models_latest.json lines 23 and 38; `brief_seat.sh` line 24 defaults to Opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet`.

## D-decisions (Tuesday accepts or overrides at the stamp)
- D1 Fix (a), pin 10.0.14; (b) and (c) only on Tuesday's word after a STOP.
- D2 No test added or edited (the committed B160 row is the red-then-green proof and the mutant killer). Names lost 0, added 0.
- D3 Reproduce with SDK 10.0.403 installed seat-local under `.tools/b720/dotnet-403` via the project's own `.tools/dotnet-install.sh`; the project's 10.0.401 is the old-SDK control.
- D4 Gate Tier 1 Opus; builder Sonnet (C2, since C3 is "the decision, not a spelled-out edit"; the kit says a bump that is not enough is C3 and STOPs).

## Q-questions for Tuesday
- Q-1 Is the recurrence out of scope? Each runtime/SDK patch release that outruns the pin re-breaks the guard (10.0.15 will). Default: YES out of scope; the seat records it under NOT TESTED; Tuesday decides separately whether to ask the product owner to make the guard self-adjusting (that would touch a security posture, so it is not the builder's call).
- Q-2 #118's dotnet check is red on the same row. Default: after B720 lands, Tuesday re-runs #118's check on a head containing main (or updates the branch by the project's rule) before the Opus gate verdict is landed; B720 does not touch #118.

## UNMEASURED
No build, SDK install, publish or test ran (drafter read-only). Not measured: the framework-vs-package Pkcs file versions under 10.0.14/10.0.403 (the hypothesis); that 10.0.14's file versions are equal so the ranking target wins the tie; deps.json key count of 2 at 10.0.14; P2 outcome (target still load-bearing at a tie); whether 10.0.14 carries another Pkcs advisory; #118's failing test name; CodeQL; hosted host's current runtime (last record 10.0.12, CLARIFICATIONS 909 and 920).

## Outside the fences
- Read-only GETs to the project's GitHub repo under its own GH_CONFIG_DIR (`-X GET`; two job-log downloads saved in the session scratchpad).
- One HTTP GET to `https://api.nuget.org/v3-flatcontainer/.../index.json` (public package index, not a hosted/demo/production host of Datasec) to confirm 10.0.14 exists.
- A 4-second local listener on 127.0.0.1:9870 as the lsof positive control, then freed.
- Read-only reads of the project's local `1_Project_Definition/CLARIFICATIONS.md`, `BACKLOG.md`, `CLAUDE.md`, and `Briefs/2026-10-16_B160_STATUS.md` (published STATUS files). Did NOT open `.tools/b160/adv-*.json` or any other seat's `.tools` tree beyond `ls`/`-e` existence checks and reading heavy-slot-1's `holder` file. No git write verbs, no fetch. No decision card, queue, ledger, briefs_staged or scoreboard read. No Artifact/Docs/mail use. Scratch files only in the session scratchpad.
