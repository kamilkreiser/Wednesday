STARTABLE: YES

# B806 drafter report (Datasec / Security Composer, lane C-ROUTEB, seat J25)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B806_SEAT-J25_composer-routeb-pcomp99-101.md` (127 lines). Drafted 2026-10-27 10:3x-10:5x AEDT.

## BLUF
One new branch `b806/composer-routeb-words-and-pins`, one commit on main `422ecf37` (PR #96's squash), two paths (`DEPLOY.md`, the b778 test). Work: (1) PCOMP-99 pin paragraph rewritten so it is TRUE, backed by a block-line/token census (the lesson of two NO GO rounds was a "pins only ... nothing else" sentence the test falsified); (2) PCOMP-100 rows E and P strengthened so M30, M33, M35, M37 (plus my M30b, M35b) turn red, file stays 10 `it`s; (3) PCOMP-101 row 250 first cell, under an 88-character property because the gate's sentence breaks prettier (see Q1). Sonnet (C2, line 92; L6 line 85 for the test half), gate tier 1 (G1), round 1 of 2 on the Route B class per your ruling; the launch line carries `BRIEF_SEAT_LEVEL=sonnet`. The Route B fenced block must stay byte-equal.

## Facts re-measured (instrument; control)
- Main `422ecf373e866728348a76d5854d864f591dd35d` by `git ls-remote` at 10:35 (sweep's 422ecf37 holds); `b806*` absent; control `b778*` printed `635fcdc3`. PR #96 `closed`, merged true, `merge_commit_sha` = that sha, by `gh api -X GET`. Open PRs #95, #91, #86, #85: 0 shared paths each with DEPLOY.md or the b778 test; control (#95's `apps/api/test/b712-setup-target-locked.db.test.ts`) 1.
- Blobs by `gh api` raw + `git hash-object`: DEPLOY.md `8c5a3fc3...` (620 lines, 59344 bytes, 55 non-ASCII bytes), the test `314f0ba1...` (418 lines, 10 `it(`, 0 non-ASCII); both equal to the same paths at `635fcdc3` (the gate's head). b616 `ee282782...`, support.ts `13eb5f3e...`, package.json `32fea116...`, package-lock `53305eb4...` via `contents --jq .sha`. `completeness check` 2 lines (235, 251), `PostgreSQL database dump` 1, `Nothing else in the command is pinned` 1; six "Nothing pins Route B's command." lines at 302, 343, 389, 443, 503, 551. Control string `zzz-no-such-string-7f3a` 0.
- Layout on main: block 198-209 (check 203, echo 204, DROP 205, cat 206, apply 207); pin claim 222-227; Proven-on heading 233; paragraph 235-239; table 241-252 (row 250 = old pointer, row 251 = "without the completeness check"); next `##` 254. Test rows E 291-297, S 299-308, P 347-365.
- Tickets PCOMP-99, -100, -101 read by the project's own Jira client (`.tools/b791/scripts/jira791.py`, `get` only, in-process credentials). All Backlog, 0 comments each, JQL `project = PCOMP AND ( key in (...) )` returned the four keys PCOMP-99..-102; control PCOMP-1 returned 1.
- Mutants M30/M33/M35/M37 definitions copied from the B787 STATUS table (lines 124-127) and tickets; B787 line 1 reads "NO GO round 2 of 2" and B779 "round 1 of 2" on this class.
- Prettier (local `node_modules/.bin/prettier`, scratch copies, config `printWidth 100` from main's `.prettierrc.json`): unedited main copy passes (0 changed lines, the control). The gate's row-250 sentence (cell 107 chars) FAILS and would rewrite 12 table lines; an 86-char cell padded to 88 passes; a 96-char padded cell fails; a 92-char unpadded fails (padding matters).
- 0019's one-step command is at `DEPLOY.md:102` and carries `--exit-on-error` besides the three flags the cell names (read from the main copy); the kit makes the seat prove the words by reading it (STEP 3(d)).
- Ports 8920-8929: `lsof` printed nothing, rc 1, 10:37; control: a `python3 -I` listener on 8929 was printed, then freed. Word-scan `892[0-9]` over non-`.pre-` 26/27 Oct SEAT kits: 0 hits; control `963[0-9]` printed five kits. Panes at 10:37: `tuesday`, `Datasec/HPSM-POC-D37`, `Datasec/MPS-R57`, `Datasec/NexusAI-G169`, `Datasec/HPSM-POC-H44`, `fleet-monitor` (no Composer pane). Load1 3.5-4.9.
- Cockpit name form: J22/J23/J24 kits all use `Datasec/Security-Composer-J<n>` (hyphen), so `Datasec/Security-Composer-J25`.
- Landing rule: CLARIFICATIONS.md line 1799 holds the quoted squash sentence (count 1, control 0). CI: `ci.sh:117-118` node chain and `scripts/test-db.sh` (both vitest runs must exit 0; step passes only on exit 0); no GitHub Actions workflow (contents 404).
- Plumbing: `.tools/b781/scripts/` holds common.sh, dbtest.sh, dbone.sh (13 lines, already mounts DEPLOY.md), heavy.sh, names.py, nodeonly.sh, unit.sh; line counts 21/74/13/42/49/10/31. Kit self-check: four-underscore line count 9, non-ASCII bytes 0, "kam|kreiser" 0.

## D-decisions (mine, for Tuesday to accept or strike)
- D1: PCOMP-101's words are held by a PROPERTY (first cell names the one-step command and is at most 88 characters, padded) rather than the gate's verbatim sentence, because the verbatim sentence reformats the whole table (a STOP in the kit's own fence). The suggested 86-char cell keeps the ticket's meaning.
- D2: PCOMP-99 is made a census-backed claim (every line or token whose edit turns a row red is named; "Nothing else..." kept only for what the census found green; may be dropped if not statable). Reason: the same sentence failed two gates.
- D3: Row P gains three pins (scoping words in the same sentence as "was run on a local stack"; `completeness check` exactly twice in the sub-section; `tail -n 6` at most once). The kit says openly that a sentence implying the check by other words is still not caught and the paragraph must say the rows pin WORDS. I added M30b and M35b as my own mutants.
- D4: Row E pins the whole text of the line after the check, whitespace-collapsed, so M30 turns red but an equivalent spacing change stays green (control c2).
- D5: No new `it` expected (group stays 39/524, RELAYED by the gate); a new `it` is allowed only with a reason.
- D6: The six "Nothing pins Route B's command." sentences stay byte-equal; listed under FOR TUESDAY.
- D7: Branch is new (not the old b778 branch); the seat pushes it but opens no PR (Tuesday opens it); CodeQL is read on the commit and the branch ref since no PR exists yet.
- D8: I did not add a row-P assertion against "the command above it" (the ticket says no regression row needed); Tuesday may want it (Q4).

## Q-questions for Tuesday (each with a default)
- Q1: Accept D1 (88-character property for row 250 instead of the gate's verbatim 107-character cell)? Default: yes. The alternative is letting prettier rewrite the whole table (12 lines) which the diff-scope fence refuses.
- Q2: Model: Sonnet via C2 (as you instructed), though B781 ran the neighbouring kit on Opus because the document guards a destroying restore (C4). Default: Sonnet, since the command is byte-equal and the tier-1 Opus gate is the backstop.
- Q3: Keep the "Nothing else in the command is pinned." sentence only if the census proves it, and allow dropping it (D2)? Default: yes.
- Q4: Add a row-P assertion that refuses a first cell holding "the command above it"? Default: no (scope).
- Q5: Stamp clocks. Default: target READY 2.5 h and hard stop 4 h after the seat's Step 0, as absolute AEDT clocks you fill. Heavy jobs launch at load1 under 7 (3.5-4.9 at 10:40).

## UNMEASURED
No vitest, container, image, mutant or census run: whether M30/M30b/M33/M35/M35b/M37 are red under the strengthened rows as specified; the census result itself; whether the whitespace-collapsed row E pin matches the block's real three-space spacing; whether the edited pin-paragraph prose lines stay prettier-clean (only the table cell was measured); the group count 39/524 on the seat's machine (RELAYED); the demo VM; a real restore.

## Outside the fences
None known. Writes: the kit and this report only (scratch files only in the session scratchpad). Reads: drafter rules, the 09:30 sweep file, B781/B778 kits and reports, the B787 and B779 STATUS files, `model-routing.md`, `models_latest.json`, `brief_seat.sh:24`, JIRA.md of the Composer project, CLARIFICATIONS.md line 1799, `.tools/b781/scripts/dbone.sh` and `nodeonly.sh`, `.tools/b791/scripts/jira_read791.py` and `jira791.py` (read) and `jira791.py` imported by a scratchpad script for three issue GETs plus two JQL GETs (no write call). `gh api -X GET` only for contents, pulls, commits, `pulls/<n>/files`. Prettier was run from the project's `node_modules/.bin` on scratchpad copies only (a tool run, not a project write). `tmux list-panes`, `lsof` (with a transient local listener on 8929, freed), `uptime`, `date`. A `git cat-file -t` ran once in the project repo (read verb; it failed because the local checkout is stale). No `decision_queue.sh`, no az/ssh/docker, no `cd`.

READ-WHOLE-BY-TUESDAY: ____
