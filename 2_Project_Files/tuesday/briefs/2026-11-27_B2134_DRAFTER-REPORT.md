STARTABLE: YES

# B2134 DRAFTER REPORT: OXPd 2, lane OX-C kit 1 (owed 119, 120, 77, 131, 122; 84 not built), seat X80

Drafted 2026-11-27 by an in-session read-only drafter (Opus) for Tuesday s332. First `date`: `Fri 27 Nov 2026 03:20:58 AEDT`; the sidecar's first line carries the write clock. Kit: `tuesday/briefs/2026-11-27_B2134_SEAT-X80_oxpd2-lane-c-kit1-hygiene.md` (265 lines), sidecar `.measured` (178 claims, `stamp_check.py` exit 0: "178 claims, 178 measured, 0 not measured"). Scratch: `fleet/state/s332/d2134/` (the seat's tools are in its `seat-tools/`).

## BLUF
- ONE commit, ten files, all `M`: twelve FROZEN replacements (`edits_c1.json`, applied only by `apply_c1.py`, each result checked against a frozen sha256) in the Server README (119), the Jobs transport README and `IppTransportException.cs` doc comment (120), the Identity README (77), `GraphClient.cs` and `GraphFailure.cs` (131) and `DeviceTokenClient.cs` (122), plus two test-support edits in `HostRig.cs` (a `Broken` switch on the tests' `MemorySecretStore`). The seat writes two cells: a 6-row Graph Theory (3 rows PREDICTED red on BASE) and `HostCellTests.H16` (a pin of the new Server sentence, PREDICTED green on BASE and head). Seven FROZEN mutants (`mutants_c1.json`): five on the Graph loop key, two proving DA18 pins both revocation values.
- **Owed 84 is NOT built (D2/Q2):** its parts (1) and (3) were already closed by PR 46 (its own "Closed in part" line); the one open part (2) is a host-side log filter in `ServerHost.cs`, owed to the logging work, outside the owned paths. The sweep's row for 84 ("one-header-line sentence says 401 where a throwing vault gives 503") is stale.
- **Item 120's platform is found at source:** the review of PR 35 (gate B1983 `VERDICT.md:51`) says "on macOS"; that gate's same-session test log reads `(net10.0|arm64)` (`fleet/state/s316/g1983/logs/head-test.log` line 1). So "measured on macOS arm64; other platforms UNMEASURED".
- **Item 122:** CodeQL reads nothing on that line: `code-scanning/alerts` (every state) 0; the C# analysis of `38a031e5` `results=0`, 63 rule ids, none holding `revoc` or `cert` (SARIF by `gh api -X GET`). Default: drop the line (it set the property to its own default `NoCheck`; not read beside the chain policy, B2051 P02c/d), DA18 unchanged.
- **Gates' lessons applied:** every README sentence is frozen and was scanned (`words.py` clean) and is pinned where it states behaviour (H16 for 119's sentence; check 9 proves all eight Identity citations); every new rule has a mutant, and the over-wide and canonical-host shapes have their own mutants (`mLoopKeyUnescaped`, `mLoopKeyOriginal`); the empty `#`, `%23` and host-case shapes are rows.
- R337 (B2132) ended READY before drafting (`READY B2132: 1665ca86... | C-91 | ...`); no OXPd pane live. Launchable now, one OXPd seat at a time.

## FACTS RE-MEASURED (instrument, then what it printed)
- Origin (`gh api -X GET`, account `kamilDatasec`, 03:21:40 and 03:48:14 AEDT): main `38a031e589c8d71049756752e39eafc91ad59055`, tree `22c5f2141e7aa46d09eaeb97eef09f21127a5e69`, parent `504ca043`; open pulls 0; `matching-refs/heads/b2134` 0 rows (control b2128 1 row); private true, push true.
- BASE tree: tarball by `gh api -X GET`, 679 files, scratch `git write-tree` = `22c5f214` (equal to main's tree).
- BASE hosted: `hosted3.py 38a031e5 --total 2422 --rules 679 ...` -> run 45823255997, `HOSTED ...: PASS`; control `--total 2423` -> `FAIL 4` rc 1.
- BACKLOG.md (after R337): sha256 `ba8ab83e...`, 1192 lines; `84. - [ ] `, `119. - [ ] `, `120. - [ ] `, `77. - [ ] `, `131. - [ ] `, `122. - [ ] `, `121. - [ ] ` each on 1 line (control `131. - [x] ` 0). CLARIFICATIONS.md `dca1f3ad...`, 1228 lines, C-91 last (no new word of the product owner on OXPd since 2026-11-25 14:30, its own words). CLAUDE.md `0f1fccc0...` (line 7 newest Opus; 55-56, 82 landing).
- Frozen edits: each OLD once at BASE (12 of 12); `apply_c1.py` on a copy of BASE: `APPLIED support: 2 edits, 1 of 1 files equal`, `APPLIED product: 10 edits, 7 of 7 files equal`; second product apply `APPLY REFUSED` rc 1.
- `checks_c1.py`: BASE index `CHECKS: 1 of 9 PASS` (controls fire); simulated staged edit (frozen edits + prototype cells) `CHECKS: 9 of 9 PASS`.
- `mutants_c1.py --list` rc 0 (`LIST: 7 mutants, 2 suites, 2 cells`), bad row rc 1; apply/undo of all seven on the green files: 7 of 7 `equal True`.
- `words.py --control` 13 of 13; over the commit message and the 43 added lines of the frozen edits: `WORDS: clean (2 files)`; over the simulated 128 added lines (with prototype cells): clean; `B2[0-9]{3}` 0 and 0.
- gitleaks 8.30.1: control rc 1 (quarantined); the eleven tools and the simulated added lines rc 0, `no leaks found`.
- Toolchain: `<project>/.tools/dotnet/dotnet --version` 10.0.404; no other dotnet on the machine (`which dotnet` none; `~/.dotnet` holds no SDK).
- Seat id X80: in 0 of 191 non-`.pre-` SEAT kits of 2026-11-2x; in 1 file in all (this commission). Control X79: 2 of 191 SEAT kits, 8 files in all. (Tuesday's read said "X79 in 7"; my frame is SEAT kits, then all files: neither is 7. X80 is free either way.)
- Load at drafting `2.88 2.45 2.07` (03:26); `df -g` 863 GiB free; the OXPd wave lock absent; panes: `tuesday`, `Datasec/NexusAI-N181`, four unnamed.

## D-DECISIONS (all the coordinator's defaults; each is a Q below)
D1 one kit for the five items; D2 owed 84 not built; D3 edits and mutants frozen, cells the seat's; D4 119 by the cached-hash sentence (and the notification bullet, the same overclaim) pinned by H16; D5 131 compares without the fragment, requests the link as given; D6 122 drops the line with a two-line comment, DA18 unchanged; D7 120 "macOS arm64" from source; D8 77 numbers plus method names; D9 new cells only, `Broken` switch added lines only; D10 owed 121, the adapter README and the Server Services bullet stay outside.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS, S4 in words): one kit or two.** Default a: one kit, five items, ten files, 7 cases, 7 mutants, READY Step 0 + 150. Alternative b: 131+122 first, README items second.
- **Q2: owed 84.** Default: not built, stays open (logging work). Alternative: a `ServerHost.cs` filter + cell (outside owned paths; config precedence UNMEASURED).
- **Q3 (STOP-CLASS, S4 in words): who writes what.** Default a: edits and mutants frozen, cells the seat's. Alternative b: the seat writes the code to a specification (B2128's form).
- Q4: 119 cached-hash sentence + notification bullet + H16 (default) vs one clause only.
- Q5: 131 compare only (default) vs also request without the fragment (OneDrive's form) vs refuse a fragment.
- Q6: 122 drop the line + comment (default) vs keep line + comment.
- Q7: "macOS arm64" (default) vs "macOS" only.
- Q8: numbers + method names (default) vs numbers only.
- Q9: no early return, `Broken` switch (default).
- Q10: ONE G1 gate (default; 122 is a TLS surface, 131 code) vs G2 for README rows only under a Q1 split; Opus, `BRIEF_SEAT_LEVEL=opus` and `CLAUDE_CONFIG_DIR` inside the quotes; pane `Datasec/OXPd2-X80`.

## UNMEASURED (each named in the kit where it is used)
- No dotnet job ran: every red, green, total and mutant expectation is PREDICTED, each with the assertion it must break or pass (the OXPd wave lock is inside the project folder; the drafter may not write there).
- The Graph executable's BASE total (MemberData; the hosted log prints no per-assembly totals): the seat measures it at Step 1.
- Whether .NET's `AbsoluteUri` keeps an empty `#` (row 2 is built to be red on BASE either way; `mLoopKeyCompare`'s row 2 is marked UNMEASURED).
- `GetLeftPart(UriPartial.Query)` keeping `%23` escaped and lowering the host (DERIVED; rows 4 to 6 measure it; OneDrive's landed `O12` already keys a loop with the same call, green on both legs).
- Linux and Windows reading the revocation mode beside a policy (moot: the value is unchanged).
- The prototype cells in `d2134/gen/proto_*.cs.txt` were never compiled; they are NOT given to the seat and NOT frozen.

## CHAIN INPUTS (every step's inputs exist at BASE or come from an earlier step; the kit's table)
0 stamp; 1 `<src>` (exists), `<repo>` values, origin, BASE run, R337 STATUS (READY), BACKLOG; 2 BASE files + `edits_c1.json` (Step 1); 3 group support + the cells (this kit) on the Step-1 clone; 4 the red tree (3) + group product + frozen mutants (1); 5 the green tree (4); 6 the staged tree (5) + checks/words/message/edits (1); 7 the commit (7a), origin/main fetch, run_step/hosted3 (1).

## OUTSIDE THE FENCES (disclosure)
- Writes: only the kit, its `.measured`, this report, and scratch under `fleet/state/s332/d2134/` (including two scratch git repositories `base_repo` and `base_repo2` made by `git init` there, and quarantined control and check folders under `d2134/_quarantine/`). Nothing written to the OXPd project folder, Jira, GitHub or any card store; no push; no pull request.
- Reads of the project folder by path only (no recursive read): `CLAUDE.md`, `BACKLOG.md`, `CLARIFICATIONS.md`, `B2132_STATUS.md` (tail), `ls -d` of three `.tools/b*` folders, the absence of the lock folder, `<repo>`'s three local config values (`--get`, values not printed), the deploy key's existence (`ls`), and `.tools/dotnet/dotnet --version`. One listing `ls <project>/.tools/ | head -30` (depth 1, names only).
- Two hook refusals, each stopped that command before it ran: `git -C $D init` (the variable path read as outside TUESDAY; re-issued with the literal scratch path), and a command of mine that held a stray `git -C <scratch repo> stash list` (refused; nothing ran; re-issued without it). No `cd` typed. Nothing deleted (earlier check folders moved to `d2134/_quarantine/`).
- GitHub: `gh api -X GET` only under the OXPd GH_CONFIG_DIR (commits, pulls, matching-refs, code-scanning alerts and analyses, one SARIF download into scratch, the tarball, check runs and job logs via `hosted3.py`). No Jira call. No HTTP to any other host. No person, HP or device contacted.
- Read Tuesday-tree evidence for item 120 and the gates' lessons: gates B2123, B2130, B1983, B2051 verdicts; `fleet/state/s316/g1983/logs/{head-test.log,gate.log,probe-exe.log}` and `fleet/state/s331/g2130/logs/h-solution.log`. Did NOT read the ledger, the scoreboard, `fleet/briefs_staged/`, any card store, or any WEDNESDAY/FRIDAY tree.
