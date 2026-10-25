STARTABLE: YES (after the stamp; two things to decide first: Q1 hard-stop clock and Q2 the PR body; CI on #112 was still running at 12:33, so the seat opens while checks may be pending, which its kit handles)

# B663 DRAFTER-REPORT: MPS PR #112 tier-1 gate kit, round 1 of 2 (seat G114)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B663_SEAT-G114_mps-112-gate-tier1.md` (77 lines; long lines). Drafted 12:31-12:37 AEDT by `date`. Read: DRAFTER_RULES.md whole, B645 kit whole, B645 STATUS first and last line only, B654 kit and STATUS whole, C-70 entry, the PR diff. Wrote only the kit and this report.

## BLUF
The kit gates #112 in B645's shape with seven checks (R1 delta, R2 docs bytes, R3 cap against the ticket's done-when, R4 red-first rows, R5 mutants, R6 whole line, R7 checks/CodeQL/merge/process). Opus, `BRIEF_SEAT_LEVEL=opus` inside the quotes, pane `Datasec/MPS-G114`, B663/G114 unused, ports 9060-9069 free. One substantive thing I found reading the diff that the builder's mutants may not catch: the committed repeated-number row has pairs of repeated numbers from line 1 (`i / 2 + 1`), so a `.Take(20)` placed BEFORE the `.Where(g => g.Count() > 1)` (caps groups examined, not entries listed) would probably survive all 10 rows; likewise a BOM counter that counts lines instead of its own entries survives when every line is bad. The kit names both as predicted survivors the gate must try to kill with a scratch distinguishing row. UNMEASURED by me (I ran no mutant).

## Facts re-measured (instrument; control)
- Refs 12:31 `ls-remote` (read verb; control: the 4 refs I asked for all printed): main `dd0ce36d`, branch = `refs/pull/112/head` = `6618f119c807a68cbf06c6ba8306c21420247247`, merge ref `406012bd...`. Same as the builder's push.
- `pulls/112` GET: open, not draft, mergeable true, **mergeable_state `blocked`**, 1 commit, 4 files, +137 -4 (kit's "+137 -4" is the PR number; the task text said per-file +1 -1, +14 -1, +2 -2, +120 -0: I measured the same four lines by `pulls/112/files`, sum 137 and 4). Builder STATUS says src patch +16 -3 (14/1 + 2/2): equal to the files, consistent. No difference from your numbers.
- `commits/406012bd` GET: parents `dd0ce36d`, `6618f119`; tree `992cf611...` = `commits/6618f119` tree (equal, main unmoved).
- `compare dd0ce36d...6618f119`: ahead 1 behind 0.
- Check-runs 12:33:23 and 12:33:30 (final state NOT reached): python success, 3 CodeQL analyses (js-ts, actions, python) success, CodeQL umbrella neutral, dotnet / web / Analyze (csharp) in_progress. `code-scanning/analyses?ref=refs/pull/112/head`: 4 rows at `6618f119`, results_count 0, error empty (so csharp analysis was already uploaded although its check-run was in progress). Open alerts on the PR ref: 0 (no control but the listing sees analyses).
- Ruleset 24139430 GET: code_scanning CodeQL `errors` + `high_or_higher`; required_status_checks list empty. `ci.yml` at the head: dotnet job build + test, no filter. `grep -c -i sql` over the file: 0 (control run returned 0 for a nonsense string, which is not a positive control; UNMEASURED-with-weak-control).
- Docs diff read in the compare diff: the one line is `... with one error per repeated number, the first 20 listed, e.g.` exactly the C-70 text; the line is longer than its wrapped neighbours (style).
- C-70: read at `1_Project_Definition/CLARIFICATIONS.md:1368` (working copy) and `git show 87e4cf14:...` count of the heading 1 (control: nonsense string 0). Root repo HEAD = `87e4cf14` at 12:3x. The card named line 275; the sentence is at 274 (C-70 says so).
- Landing rule: `CLARIFICATIONS.md:809` (read as a line: "squash with the head pinned (`--match-head-commit`, the MPS convention...)") and project `CLAUDE.md:50-52` (CodeQL rule; the seat name there is stale). The builder cites the same lines.
- Jira GET (`project = MPSCALC AND ( key = MPSCALC-325 )`): 1 issue, Backlog; done-when quoted in the kit. The ticket's own text says the supplies-null site was not measured and the rows only cover four walks.
- Helpers: `QuoteRefusalOrder.cs` blob `68f356d8...` equal at main and at the #112 head; `B102Audit.cs:58` and `GateB36.cs:109` read at the head (one-entry assertions).
- Open PRs: #110 (head `650ddfb7`, 5 paths, none shared) and #112. `ls-remote refs/heads/b6*`: b60, b603, b614, b62, b630, b654, b69; no b663.
- B645 STATUS first/last line: NO GO round 2 of 2 on #110 (survivors G13, G13a, G13b, G6, G4, G3). A different class; so round 1 of 2 here.
- Model: `models_latest.json` `levels.opus.model_id` = `claude-opus-5-5` (line 17). Routing rows G1 `:108`, G-cap `:111` (read from the file).
- Ports: kits scanned = 111 non-`.pre-` SEAT kits of 10-24 and 10-25 (`ls` count), census of every 9xxx word (226 distinct); block 9060-9069 not named in any of them (python census; control: 9930 appears in the B643 kit by `grep -w`); `lsof -nP -iTCP:9060-9069 -sTCP:LISTEN` empty rc 1, control: a python listener on 9060 was listed, then gone. Your assigned blocks (9020s, 9570-9589, 9950-9959, 9990-9999, 9330-9339, 9300-9319, 9960-9969) all have hits in kits, so I chose from the free set. Free blocks by this census: 9000, 9010, 9030-9080. Note 9020-9029 you listed as taken.
- Panes 12:31: tuesday, NexusAI-G113, HPSM-POC-G112, HPSM-POC-G111, Security-Composer-G110, NexusAI-M9, fleet-monitor. No MPS pane. `grep -l 'B663|G114'` over the kits: none; no B663 file in the project Briefs. `.tools` had no `heavy-slot-*` at 12:33 and still had `b654`, `wt-b654-fix`, `wt-b654-mut` (builder's, finished).
- uptime 12:31 load1 6.61.

## Decisions (stamp can override)
- D1. B-number B663, seat G114, findings `B663-n` (both unused, measured).
- D2. Ports 9060-9069 (free per census), not any of the listed blocks: every listed block was taken by some kit.
- D3. Template B645 with its shape; round 1 of 2 on class "draft-validation walk caps"; B645's NO GO class was different (governed nulls); stated in the kit.
- D4. Order of priority R1, R4(rows)... in the kit the "WHAT THE GATE JUDGES" lists R1, R4, R3, R2, R5, R6.
- D5. The gate re-runs the builder's C1-C8 from the TEXT and must add at least ten own mutants; it must try to kill two predicted survivors (Take-before-Where, line-counting counter) with scratch rows. Q-1 YES needed.
- D6. R3 probes CREATE and DUPLICATE routes with scratch rows, because the rows only exercise PATCH.
- D7. Sibling uncapped walks (other per-line BOM errors, OutOfRange loop, supplies-null site) graded Minor/Note unless one of the four named walks is uncapped; the done-when says "such lines".
- D8. No absolute hard-stop clock typed in the kit; the stamp fills it (2 h target / 3.5 h hard stop suggested, same as B645).

## Questions for Tuesday (default in brackets)
- Q1. Hard stop: any outside constraint (B645 had 12:30)? [none; stamp fills 3.5 h after Step 0]
- Q2. The PR body names "Builder B654 (seat M21)"; if the squash body is taken from it, a brief number lands in main's history. The kit tells the seat to report it as a Note and says PR text is yours. [you edit the PR body before the squash, as for #110]
- Q3. Launch window: CI on #112 was still running at 12:33 (dotnet in progress). Open the gate now or after green? [open now; the kit makes checks R7, and a pending check caps the verdict at GO WITH FINDINGS]
- Q4. Q-1 (scratch mutants in the seat's own trees). [YES]
- Q5. May the seat make the one explicit-refspec fetch into its own clone (needed for the merge-ref object, as B645 Q-4)? [YES, written into Step 0]

## UNMEASURED
Everything runtime: the 10 cases red/green, the mutants (including my two predicted survivors, which are reading, not runs), the whole line and its counts (the builder's 435/183/2847 are relayed), the Entra host on Linux, `mergeable_state` once checks finish, SQL Server (no leg seen in ci.yml; weak control), the final CodeQL state (csharp check-run in progress), the memory of 100,000-line bodies, whether the shared-cap row's 20 fleet entries pin the fleet-before-hardware order beyond the fleet side. I did not check that the builder's `.tools/b654/` scripts exist (fenced).

## Disclosures (outside the fences?)
- Read: the project's `CLAUDE.md:50-52`, `CLARIFICATIONS.md` (lines 809 and 1368-1395 only), `JIRA.md` (grep of two lines for a helper), root repo `git log -1` and `git show 87e4cf14:` with a count (read verbs, root repo = the project folder).
- Jira: one GET through a helper I wrote in my scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/0642a44c-c521-4651-9987-831028b00c43/scratchpad/jget.py`) that reads the project `.env` in-process (JIRA_ names listed with `grep -o` of the key names only, no values printed). The project had no helper of its own that I could find; the B654 drafter did the same. JQL has the parentheses.
- `lsof` bound a short-lived python listener on 127.0.0.1:9060 (6 s) as the control. Reported, not hosted.
- I `cat`-ed the 111 SEAT kits to /dev/null and a pipe (to make the port census) and wrote census files in the scratchpad only. Kits read: no content disclosed here.
- I did not read the card store, fleet/briefs_staged, scoreboard.md, _ledger.md, any WEDNESDAY or FRIDAY tree, or another client's material. Two hook advisories on case-sensitive grep fired; the counts they concerned were paired with controls elsewhere or are noted above as weak.
- No Artifact, Docs, mail, chat, publish or upload tool was used. Nothing written in any project folder.
