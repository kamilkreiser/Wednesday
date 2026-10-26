STARTABLE: YES, but only after a heavy slot frees (both live slots are held by gates right now). Not startable at this minute for a heavy job; the kit's Step 0 and the reading steps are.

# B769 drafter report (kit for seat Datasec/MPS-M38, MPSCALC-346), 2026-10-27 00:4x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B769_SEAT-M38_mps-346-parity-assertions.md` (140 lines, 8 four-underscore stamp lines, counted by `/usr/bin/grep -c -E '_''_''_''_'`, matches the kit's own "8 lines" claim).

## BLUF
1. One path, `tests/MpsCalc.Import.Tests/PanelParityMultisetTests.cs` (main `1137f119`, blob `d37e2d60`, 312 lines; hash-object of the raw read matches the ticket). Edits EXISTING lines (this is not an append lane, unlike B757): the four `Assert.False(report.AllAgree)` at `:255 :271 :293 :309` become `Assert.True(report.Refused)` where a named mutant earns it, else are dropped; R2 `:229-230` kept only if a named mutant makes each first, else dropped; R5 guard `:290` dropped by default. No product byte.
2. Why `Refused` is the right replacement: `ParityProof.cs:34-36` defines `AllAgree => !Refused && ...`, so `Refused` true implies the old line and sits before the sentence; it is first to fail whenever a mutant empties the refusal (the gate's P1/P2 for R3).
3. MPSCALC-343/-344 are OUT and said so (HOLDS, twice): the gate's cap of two extra rows needs the product owner's word; same file, so serial after this lane.
4. Main still `1137f119`; no `b769*` ref; open PRs 120, 121 share 0; live `b7*` branches share 0 except the stale `b711` (the squashed #122's own head; kit says never touch). Ports 8630-8639: lsof rc 1, kit scan 0 hits (control 947x fires in 12 lines).
5. Heavy slots (00:43): `heavy-slot-1` = `B765 00:41:32 W2-wholeapi-xrows`, `heavy-slot-2` = `B766 00:39:58 q1`, slot 3 absent. The kit says wait by the standing mkdir mechanism (which includes slot 3), never touch a holder.
6. Q-questions: Q-1, Q-2, Q-3, Q-4 below.

## Facts re-measured (instrument; control)
- Main sha: `gh -X GET api .../git/matching-refs/heads/main` = `1137f11962c9adbee84c119fe7dd2f545bd4a42a`. `ls-remote` over ssh not usable by a drafter; matching-refs used (same as the B757 drafter).
- Test file: raw `gh contents` read, `wc` 312 lines 18151 bytes, `git hash-object` = `d37e2d60b51f...` (the ticket's abbreviation). `Assert.False(report.AllAgree)` on 9 lines `:103 :122 :143 :210 :228 :255 :271 :293 :309` (grep -c 9; control `zzz-no-such-string-7f3a` 0); `report.AllAgree` 10 lines in all (`:84` is the `Assert.True` control row); `Assert.Single(` 5 lines; `A4PanelRecords(doc)` 9 lines; `report.Refused` 0 lines.
- ParityReport: `:34 Refused`, `:36 AllAgree => !Refused && ...` (raw read, sed).
- CI: `ci.yml` lines 42 and 43 (`dotnet build MpsCalc.slnx -c Release`, `dotnet test MpsCalc.slnx -c Release --no-build`); `TreatWarningsAsErrors` 1 (control 0); `global.json` 10.0.100 latestFeature; main tip check-runs `success x8`.
- Landing rule: `CLARIFICATIONS.md:809` read with `sed -n 809p` and quoted in the kit (squash, head pinned `--match-head-commit`, "the MPS convention"); `:854` repeats it citing `:809`.
- Ticket MPSCALC-346: Backlog, Medium, labels `lane-e mpscalc-b751 plan-b751-b740-5 tier-2`, 0 comments; read with `project = MPSCALC AND ( key = MPSCALC-346 )` through the project `.env` in process.
- B740 STATUS: lines 80-120 and 170-185 read (pin table, B740-5, mutant table P1 P2 P2m P3 P4 P5 Q1-Q5 N2 N12 and their credited rows).
- Model: L6 row at `model-routing.md:85` (printed); `claude-sonnet-5-5` at `models_latest.json:38`.
- Intersection (`compare/main...<b>` against Yours, `/usr/bin/grep -c -x -F`): b711 2 files/1 shared (stale), b720 1/0, b74 1/0, b744 19/0, b745 2/0, b75 8/0, b757 1/0, b79 11/0; PR 120 and 121 0 each.
- Kit scan: 148 non-`.pre-` files dated 10-26/10-27; `863x` 0 hits; `B769` 0; `M38` 1 file (the B758 kit; the match is not a pane and no `Datasec/MPS-M38` pane exists: panes are tuesday, MPS-G158, HPSM-POC-D33, MPS-G157, fleet-monitor).

## D-decisions (override at the stamp)
- D1 Sonnet, L6 line 85, tier 2 gate, `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes.
- D2 Replace with `Assert.True(report.Refused);`, and drop when three honest mutants never earn the line; rows added 0, names lost 0, names added 0.
- D3 No product byte, no docs (the B740-4 wording finding stays with the records seat).
- D4 Base is main as read at Step 0; STOP only if the test file or `ParityProof.cs` is in the moved list.
- D5 R5 guard `:290` is dropped by default (a replacement after `:289` can never be first).
- D6 One push, plain, new branch `b769/mps-346-parity-assertions`.

## Q-questions for Tuesday (each with a default)
- Q-1 Heavy slot 3: the standing mechanism is `mkdir slot-1 || slot-2 || slot-3`, and slot 3 is absent now. You said both slots are held by live gates; the kit lets the seat take slot 3 if it is free under the load rule (load1 below 7). Default: accept the 3-slot mechanism as written; override at the stamp if you want the seat to wait for 1 or 2 only.
- Q-2 Gate round count: the parity file's earlier gate gave NO GO round 2 of 2 on #118 (landed as #122 on the product owner's ruling). This is a new PR, so default: "round 1 of 2 on a new PR", tier 2.
- Q-3 The older rows' `Assert.False(report.AllAgree)` at `:103 :122 :143` and R1/R2's `:210 :228` are not in the ticket (they run on stores where AllAgree could be true, and the gate pinned `:210 :228` under Q10inv, P4). Default: the seat prints their first-failure mutants as information and edits nothing.
- Q-4 Parallelism with M-PUBLISH (MPS-M37, B758): the kit declares share 0 with `MpsCalc.Api.csproj`; both builders want heavy slots, so they queue on the same mechanism. Default: parallel launch is fine, slot-limited.

## UNMEASURED
Nothing was built or run. Not measured: whether the gate's mutants P1/P2/P3/N2/N12/Q2 EMPTY the refusal for their credited row (the table says the row dies, not how), whether any mutant empties R4's refusal (the kit gives three own candidates; otherwise the line is dropped), whether `:203` `mine.Count + 1` makes `:230` the first failure, and the test-name counts. Kit line numbers of ParityProof.cs (`:148 :187-199 :203`) are from the raw read and flagged for re-print.

## Outside-the-fences disclosure
None crossed. Reads: DRAFTER_RULES.md, the B757 template kit, the SWEEP-0030 file (lines 70-90, 170-180 only, plus a count of two tokens), CLARIFICATIONS lines 805-812 and a `/usr/bin/grep -n -i` over that file that printed long matching lines (read-only), the B740 STATUS and its evidence directory listing (no evidence file other than the STATUS opened), the raw test file and `ParityProof.cs` through `gh -X GET` into the session scratchpad, a Jira GET through the project `.env` in process (token not printed), `ls`/`lsof`/`tmux list-panes`, heavy-slot holder files (read only), `compare` and `pulls` GETs. One Bash call was refused by the no-`cd` hook (nothing ran). No `decision_queue.sh`, no staged briefs, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree, no git verb on a project repo, no write outside the two files and the scratchpad (`jira346.py`, `t346.txt`, `parity.cs`, `ParityProof.cs`).
