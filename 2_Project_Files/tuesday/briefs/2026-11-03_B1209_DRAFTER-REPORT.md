STARTABLE: YES

# B1209 drafter report (Security Composer records seat R155, PR #114 / PCOMP-116, plus the DEPLOY.md:255 finding)

Drafted by an Agent-tool drafter. Clocks are the `date` lines printed in each action (13:26 to 13:32 AEDT 2026-11-03); the kit types none.

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1209_SEAT-R155_composer-records-pcomp116.md`, 90 lines, 6 stamp-slot lines (5 slots + last line; control by `grep -c -E '_''_''_''_'` = 6). Sonnet, C8, `BRIEF_SEAT_LEVEL=sonnet` in the launch line, no ports.
- Writes: up to 4 Jira creates (NEW-A to NEW-D, labels plan-comp-458 to -461), 1 comment on PCOMP-116, BACKLOG rows #457 to #462, State append on #434, entry C-123, a history entry, one JIRA.md bullet.
- DEPLOY.md:255 (part B) is NOT in the kit. Finding below: line 255 STILL holds the old sentence at 2f63b2f6.
- NOTE for Tuesday: B1189 (R151) already folded (root main is now 628dfbf4, not 0406d583 as in the R151 kit); next ids are BACKLOG #457 and C-123, Jira highest PCOMP-123 (R151's four tickets exist).

## Part B: the DEPLOY.md:255 finding (for a one-line builder)
- Card (read by `decision_queue.sh show composer-deploy-md-255-pinned-sentence-1103` into a scratch file, 13 lines): status `ruled`, `choice='b'`, ruled_ts 2026-11-03T06:40:34+11:00. Option b = "Approve the proposed sentence (recommended)"; detail: "The round-2 seat writes it verbatim on line 255, nothing else in DEPLOY.md changes". The card's default clause: a later tap on b "becomes a one-line docs change in its own small PR".
- **Approved sentence, verbatim from the card's "Proposed text":** `Nothing else in the command is pinned, except that the check line holds no exclamation mark and does not end in a backslash, and that each piece of the check line that the test edits to prove it (listed in the test file) is on that line exactly once.`
- **Where it goes (MEASURED: `gh api -X GET .../contents/DEPLOY.md?ref=2f63b2f6...`, 652 lines, printed with `awk NR==n`):** line 255 at 2f63b2f6 begins `Nothing else in the command is pinned. Measured with a throwaway \`postgres:16\``; the line continues `(16.15), not on the demo VM: the script ...` on :256 onward. So the OLD sentence is still at :255 after #114 (control: `grep -c -i -F 'Nothing else in the command is pinned'` = 1 at f5f33e18 and 1 at 2f63b2f6, both at :255; PR #114 changed only DEPLOY.md :203, `diff` of f5f33e18 vs 2f63b2f6 shows one hunk `203c203`).
- **Exact replacement for the builder:** on line 255 replace only the first sentence `Nothing else in the command is pinned.` (up to and including the period, keeping ` Measured with a throwaway \`postgres:16\`` and the rest of the paragraph on :255 to :263) with the approved sentence above, which ends with `exactly once.` A literal prefix replace, not a whole-line replace. Surrounding context: :250 to :254 is the pin paragraph; the word-wrap of :255 will lengthen (builder may re-wrap only if the b616 scanner does not pin line breaks: unchecked, UNMEASURED here).
- Builder cautions (not measured by running anything): the b616 scanner test (109 rows) reads DEPLOY.md prose in places, so the one-line change needs a run of that test; the sentence contains the words "exclamation mark" and "backslash" in words only (no `!` or backslash character), which is the property the project cares about.
- Other pointers at 2f63b2f6: :203 the check line; :259 (`\unrestrict` line whose key is the one on the script's first `\restrict` line ...) true but not the whole rule (residue row 7); :263 "before 16.10" stays with PCOMP-117; :265 the Proven-on heading dated 2026-10-10.

## Facts re-measured (instrument, control)
- PR #114: `gh api -X GET repos/datasecau/Datasec-Security-Composer/pulls/114`: merged true, merged_at 2026-11-03T00:07:47Z = 11:07:47 AEDT (`TZ=Australia/Sydney date -r`: printed `Tue 3 Nov 2026 11:07:47 AEDT`), merge_commit_sha 2f63b2f6..., base f5f33e18, head ce523783, branch `b1170/composer-pcomp115-116-db-typecheck-awk`, 2 files +346 -5. Control `pulls/9999` 404.
- Squash: one parent f5f33e18, tree 82639749eeb7edb16e23c96f6c3b944831979f12 (equals the gate's merge-result tree 82639749 as `B1197_STATUS.md` line 1 D2 / `residue.md` line 5 state), verified true, DEPLOY.md +1 -1 blob 4a1bae95, b778 test file +345 -4 blob 2348719a; contents API blobs at head and squash equal for both files. Squash message states the limit and "A records step tickets all four after this merge" and "Landed under the product owner's 2026-11-03 decision to land the change as it is and ticket the four shapes".
- Check-runs: head ce523783 CodeQL, Analyze (csharp), Analyze (javascript-typescript) success (completed 00:05:06Z to 00:06:26Z, before merged_at 00:07:47Z); squash: both Analyze success. Open alerts main 0, `refs/pull/114/head` 0; control `state=fixed` 20. Open PRs [91, 86, 85]. `git/ref/heads/main` = 2f63b2f6.
- Gate verdict lines (`grep -n -E '^VERDICT'`): B1173 `:161` NO GO round 1 of 2 @63fe0b9; B1181 `:183` NO GO round 2 of 2 @643c389; B1197 `:169` NO GO round 3 (granted, final) @ce52378. Same class on all three: "Composer: Route B completeness check (0021) header-key rule". B1197 flips: "56 cells, all A->R" (`:81`), realcuts 2 flips (`:78`).
- Residue table rows at `residue.md:10-17`; findings `B1197_STATUS.md:12-14`; FOR TUESDAY `:163`, decisions stated `:165`.
- Root records repo: main 628dfbf4 (B1189 fold, B1189 commit 3b9b8f14), porcelain over the four record paths 0 lines (control: whole-repo porcelain prints other lines), staged 0, MERGE_HEAD/index.lock absent (ls printed two errors), no remote (`git remote | wc -l` 0), BACKLOG 452 lines highest #456 at :452, CLARIFICATIONS 2314 lines highest C-122 at :2293, JIRA.md 44 lines, history top entry :3. `PR #114` count over the four paths 0,0,0,0 (control `PR #113` in JIRA.md = 1). `:1799` holds "squash-merges PR #88" (the line; grep -n -F; control: C-101 heading at :1797).
- Jira (read-only GETs via the project's `jira1189.py` read module in-process, no token printed): `myself` 200; total 123, held 19, seed 94, Done 26, highest PCOMP-123; plan-comp-457 to -460 0 each, -461 0, control -446 1 and -450 1; zzqxvbw 0, composer 58. PCOMP-116 Task Backlog labels [plan-comp-434] 0 comments 0 links.
- Seat name: `grep -l -w -i 'R155'` over briefs minus `.pre-`: 0 files (control R151: 1); `B1209` 0 files before this write (the kit file now exists). Ports: none assigned. Live panes: %0 tuesday, %150 Datasec/MPS-G316, %144 Datasec/HPSM-POC-G313, %1 fleet-monitor; no Composer pane; `ps` printed only the grep's own line and a shell wrapper.
- Model row: `model-routing.md:98` C8, `:97` C7; `models_latest.json:23` claude-sonnet-5-5; `brief_seat.sh:24` default opus.
- Text scan of the posted (`> `) lines: backtick, backslash, non-ASCII, B-number (only the exempt file name b778 and a SHA), seat/brief/lane/gate, person names, production/live: 0 (control: a planted `> x B1209 gate` line fires the pattern; file has 0 non-ASCII bytes by python byte count).

## D-decisions (mine)
- D-1: ONE ticket for the two Majors? No: two tickets (NEW-A the indent + x--y, NEW-B the VT/FF/NBSP lines), because the gate's findings, cells and repair shapes are B1197-1 and B1197-2; x--y shares the same mutated comment test as the indent, so it rides with NEW-A. "The four shapes" of the ruling = indent, VT, FF, NBSP; the squash text names them the same way.
- D-2: B1197-3 gets its own ticket (NEW-C), Minor and safe-direction, because the residue table row 3 says "ticket under the Security Composer BACKLOG".
- D-3: gawk + demo VM + line 259 in ONE ticket (NEW-D) with three numbered parts: all three are conditions or words needing a go or the product owner, none is code, they close together. Backlog row #461 holds them as one row; the residue table asks for a ticket on each, so Q-1.
- D-4: PCOMP-116 is commented, NOT moved. Convention quoted in the kit: C-111 (3) `CLARIFICATIONS.md:2029` and C-112 `:2049` ("A move needs three things: the brief's slot reads MOVE for that key, the seat's Done-when table reads MET, and no gate line contradicts it; otherwise the ticket is commented only."). Last gate line is NO GO, no MOVE slot. Prior pattern: PCOMP-23 (R151) was commented not moved on the same ground.
- D-5: line 255 is out of the records kit and listed in row #462 as "a separate code change" with no sentence text.
- D-6: not a "typed clock" anywhere; the merge time in the comment is marked "[converted]" for the seat to re-derive by program.
- D-7: row numbers #457 to #462 and C-123 pinned in the texts; the kit has a REFUSE if highest is not #456 / C-122.

## Q-questions for Tuesday (each with default)
- Q-1: gawk, the demo VM and DEPLOY.md:259 as ONE ticket (NEW-D, default) or three tickets? Default: one; if three, the kit needs a fifth create, MAX_WRITES 7, labels -461 to -463 and the rows re-cut (I did not draft that).
- Q-2: Should PCOMP-116 move to Done? Default NO (comment only, C-112: no MOVE slot, last gate NO GO). If yes, Tuesday must add a MOVE slot, a transition 41 arm and a Done-when line; the squash lands the ticket's own fix, but the review ended NO GO x3.
- Q-3: Is the R151 B1189 fold the baseline you want (root main 628dfbf4)? Default yes; REFUSE 3 pins it.
- Q-4: Who commissions the DEPLOY.md:255 one-line builder, and does it go before or after any lane for rows #458 to #461? Default: separate small PR first, own gate not required beyond the b616 test run.
- Q-5: Should the hosted CI be recorded as "NOT RUN on the branch" in row #462? Default yes (B1197_STATUS.md condition), already in the kit.

## UNMEASURED
Hosted site; gate cells (RELAYED); whether main or Jira moved after 13:31 AEDT; who merged #114; the b616 scanner's sensitivity to the :255 re-wrap; whether the ruling board message at 10:57:21 is exactly as the commission quotes (not re-read; the kit cites the date only); the Co-Authored-By line says Opus 5.5 (unrelated).

## Outside the fences
None. Reads only: the drafter-rules file, the R151 kit, BACKLOG/CLARIFICATIONS/JIRA.md/history of the Composer root, the three B1173/B1181/B1197 STATUS files and residue, Jira GETs, `gh api -X GET`, `decision_queue.sh show <exact id>` (one id, output to a scratch file under the session scratchpad), lsof/tmux/ps/stat. The fetched DEPLOY.md copies and a Jira read script live only in the session scratchpad. One loaded `jira1189.py` module from `.tools/b1189/scripts/` (read module, GET only; no token printed; no bytecode written). No `decision_queue.sh list`, no vault, no ledger, no WEDNESDAY tree.
