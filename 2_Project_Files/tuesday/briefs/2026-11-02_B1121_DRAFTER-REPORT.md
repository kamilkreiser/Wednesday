STARTABLE: YES (after Tuesday's stamp, with the label word in S1; see Q-1)

# B1121 drafter report (Sonnet, row C8), `date` Mon 2 Nov 2026 12:31 to 12:51 AEDT

**BLUF.** Kit `2026-11-02_B1121_SEAT-G285_hpsmpoc-scored-count-gate-tier1.md` is written, unstamped (8 four-underscore lines, control: 8 counted by `/usr/bin/grep -c -E '_''_''_''_'`; 0 `at-sign CAPS at-sign` placeholders; 0 non-ASCII), **20,241 bytes** (19.8 KiB; 241 over a decimal 20 KB, see Q-6). Tier 1 Opus, row G1 `model-routing.md:108`, round 1 of 2, NO GO 0 before, pane `Datasec/HPSM-POC-G285`, launch through `launch_when_cool.sh` with `BRIEF_SEAT_LEVEL=opus` inside the quotes. One load rule (RULE L, wording copied from B1118, adapted: `.tools/heavy-slot-N`, two reads two minutes apart, red re-run alone 3 times at merged and at base, timeout in an untouched file a Note) and one severity table. I read the severity table against steps 0-9 line by line: every grade a step states (2, 3, 4, 5, 9, Rule L) appears in the table; step 5 lacked a grade and now has one; load is judged only by Rule L.

## Facts re-measured (instrument)
- main `4b3cefae71ca...`, head `f762cc7a3021...` (`gh api -X GET git/ref`, 12:31); compare: ahead 2, behind 1, base `c1457349`, 24 files (11 + 13), commits `68de6001` then `f762cc7a`; open PRs 0 (`pulls?state=open` empty).
- Main's one move = 8 paths under `web/src/components/{customer,feedback,partner}/`; tarball `diff -rq` main vs head = 32 lines = 24 + 8, overlap 0; `ci.yml` `cmp` equal. Landing tree = main + the 24.
- Ports: 9730-9739 `lsof` 0 rows; word-bounded scan of 122 non-`.pre-` SEAT kits of 11-01 and 11-02: 4 hits, all 11-01 NexusAI seats (B1050, B1054, B1058, B1069), 0 today; control `972[0-9]` 8. Other blocks all had finished-seat hits (9760 to 9969: 2 to 12 kits), so 9730 was the cleanest near block. Live panes 12:31: tuesday, MPS-G283, MPS-G284, MPS-M76, HPSM-POC-H100, -G282, -G280, fleet-monitor. `df -g` 40 GiB. load1 6.1, 9.1, 7.1, 8.4 over four reads.
- Round count: 139 gate STATUS files with first line `GATE VERDICT`; class words in 0; control (wake-retry class) 1.
- Pointers (from the raw tarball at the pin): `CustomerEndpoints.cs:303/314/316`, `Views.cs:48-52/105/123-131`, `AssessmentEndpoints.cs:30/37-46/645/650/681/689`, `CustomerShell.tsx:84-92/174`, `SecurityAssessments.tsx:23`, `SecurityDashboard.tsx:29`, `SecurityReports.tsx:62`, `AssessmentScreen.tsx:45-46/99`, `ci.yml:86-87/165/175/251-255/303/314`, `AssessmentDbContext.cs:183/192/199`.
- CI parts: both new test classes are namespace `HpsmPoc.Api.Tests.Assessment`, so 28 of 28 land in `api-assessment` (filter `ci.yml:251-252`); the complement part gets none. The SQL Server leg cannot run locally (no docker): kit makes it a Condition and asks the gate to read the raw `UPDATE` tamper rows (71-character hashes against `HasMaxLength(71).IsFixedLength()`).
- Consumers of the saved read's `completion` (grep of main's tarball, `web/src` non-test): the customer read feeds only `CustomerShell.tsx:124` and its chip (main `:88` printed "0 of 0 questions answered", HPSMPOC-421). `useDirectory.ts:32` reads dates, `useSecurityData.ts:56` reads counts of printers and sites, the mock takes the list route's first item, `FirstVisitWarmup.cs:116` is server-side. The other `completion.answered` readers (`useSecurityData.ts:74`, `engagement.ts:203`, `SnapshotLauncher.tsx:48`, `AssessmentsHub.tsx:78`) appear to take the LIST route, which never sent zeros: **leads, not proven; the kit makes the gate prove each caller's route.** Zero readers found treating 0 and 0 as meaning; external API consumers UNMEASURED.
- Visible words by program (`diff` of the four web source files): chip and row "N of M scored questions answered" (changed), tile label "Scored questions answered" (changed from "Questions answered"). The only phrase allowed is the page's own, lowercase after a number (`AssessmentScreen.tsx:99`).

## Contradictions found
1. **"Both delta copies equal" is false as worded.** `api/tests/.../Contract/openapi.delta.json` and `web/contract/seat-a/openapi.delta.json` are not byte-equal at main nor at head (`cmp` differs at char 18, line 2, the root `$comment`). Parsed with python `json`, `schemaPatches`, `addedOperations`, `requestChanges`, `responseChanges` are equal at both. `SOURCES.md:8` holds the web copy's sha256 `77fc70d1...`, equal to the file at head. Kit grades parsed-equal a Note, any parsed difference a Major.
2. Builder: commit 1 says "14 of the 20" red; its Corrections 11 says the final file is 13 of 20 "by reasoning, NOT measured". Kit: the gate's own red-first run settles it; a false sentence is Minor.
3. Builder STATUS "READY" line and BLUF are consistent with `gh api` (head, 2 commits, 1 behind). No contradiction there.

## D-decisions (mine, for acceptance or strike)
- D-1 Merged-tree gate by `cherry-pick --no-commit` of both commits onto main (B1118 form), landing tree stated as main `4b3cefae` + 24.
- D-2 Cost judged by command COUNT only (EF interceptor), timings optional and grade nothing; threshold = the builder kit's (more than +1 stops), no N+1 check added (1 vs 16 answers).
- D-3 Unloadable package: customer read 200 with 0 and 0 plus the Warning is a **Note**; a 5xx there, or any change to the list route, is a Blocker; the list route's 500 goes to Tuesday as a backlog line (builder noticed, did not fix).
- D-4 The builder's two kit slips are stated as disclosed and not findings unless they had an effect.
- D-5 Own plants p1-p8 (p8 = label reverted, Minor if it survives).

## Q-questions for Tuesday (each with a default)
- **Q-1 Does the tile label "Scored questions answered" need your word? Yes.** It is a new literal (capital S, no number, was "Questions answered") beside the one allowed phrase; the builder judged it the same words and did not stop. Default: you rule it in S1; recommended wording "accepted as the page's own phrase in sentence case". If S1 is silent the kit makes it NOT RULED (Major, no GO).
- Q-2 Do the "N answers so far" lines (`engagement.ts:154-158`, `SnapshotLauncher.tsx:45-47`) and "Answered N of M questions shown" (`SnapshotResult.tsx:125`) fall under "everywhere"? Default: no, stay open as a words decision; the PR does not claim the ruling is complete, and HPSMPOC-420/-421 are described by what changed.
- Q-3 If the saved-mode browser cells (real API behind the proxy web) cannot be run for sign-in reasons, does the verdict stay GO WITH FINDINGS? Default: yes, as a Condition with the API-level equality of the two routes as the substitute; the kit as written bars a GO on any REQUIRED cell not run (the explicit "NOT TESTED" sentence was cut for size).
- Q-4 Port block 9730-9739. Default: accept.
- Q-5 The kit relies on the B1107 kit for fetch, lock, scripts, plants and landing-file forms instead of repeating them. Default: accept.
- Q-6 Size 20,241 bytes. Default: accept (19.8 KiB); the 8 stamp lines and RULE L are intact.

## UNMEASURED (by me)
Hosted CI, CodeQL, the SQL Server leg; whether the web sign-in lets the proxy form run; the real wake; external API consumers; the first sample customer's live figure (builder: 16 of 16 by the seeder, not read); overlap of H100, G282, G280 with the 24 paths (word scan only, not their Yours lines); the Jira done-whens were read from HPSMPOC-420 and -421 (GET, description only) but the kit quotes them in short, the gate re-reads them.

## Outside-the-fences disclosure
Read-only: `gh api -X GET` (refs, compare, pulls, branches, two tarballs of main and head saved under the session scratchpad, not in any repo), `lsof`, `tmux list-panes`, `df`, `uptime`. I imported `.tools/b1007/jira.py` from the project by path in a scratch script to GET two issues (summary, status, description, links only; comments never printed). I read the builder's STATUS and kit. I did not run `decision_queue.sh`, write Jira, touch a project file, or use Artifact/Docs/mail. Local `git ls-remote` failed (the deploy key path in the project config is missing); all remote facts came from `gh api -X GET`. Scratch scripts `jget.py`, `repl*.py`, `del*.py` sit in the scratchpad only.
