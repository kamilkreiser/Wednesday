STARTABLE: YES (after Tuesday stamps; launch not blocked by anything measured; one standing watch item: CodeQL cannot scan, see Q-1)

# B736 drafter report (Security-Composer-G146, gate of PR #94 at eddebf34, the product owner's extra round)
Drafted 2026-10-26 12:33-12:40 AEDT by `date`. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B736_SEAT-G146_composer-94-round3-gate-tier2.md` (88 lines, shape of B707).

## BLUF
Short closure gate: B707-1 only, by the gate's own plants and mutants; no loosening and no lost kill vs the round-2 head; file and group green; names; CodeQL graded as NOT SCANNED (a condition, never clean, never a code failure). A NO GO goes to the product owner as a card. B707-2, the nine RULING-BOUNDARY shapes and the builder's two residue forms are ticket text, not re-gated.

## Facts re-measured (instrument, control)
- `ls-remote` 12:33: main 8347f91b (moved from 0b52848c), branch = pull/94/head = eddebf34fdab4852..., pull/94/merge b8286c8a (moved). Control: the same call printed three expected refs.
- `pulls/94`: open, 3 commits, 1 file, +510 -20 (= 384 + 126), mergeable true, mergeable_state `blocked`. `pulls/94/commits`: 0307e31a, 99585f7d, eddebf34 (control: the order matches the builder STATUS).
- `check-runs` at eddebf34: only `Analyze (csharp)` and `Analyze (javascript-typescript)`, both completed `failure`; the `CodeQL` check-run is absent. `code-scanning/analyses?ref=refs/pull/94/head`: newest are 99585f7d x2 and 0307e31a x2, none for eddebf34 (control: rows do come back for the older heads). The drafter did not see the annotation text (the `output.summary` column was empty in the GET); it is RELAYED from the builder and from the task brief.
- Head file via `git show` and `/usr/bin/grep -c -F`: `function closeOf` 1, `function endsWithName` 1, `textUntil` 5, `zoneEnd` 3, control string 0; `wc -l` 912; literal `it(` rows 46 (39 + 7).
- Panes (`tmux list-panes -a`): tuesday, MPS-G143, HPSM-POC-G144, G141, G142, Security-Composer-G139 (live, B724, not ours), MPS-G138, fleet-monitor. No Composer builder pane.
- Ports: `lsof -nP -iTCP:9700-9999 -sTCP:LISTEN` rc 1. Word-boundary scan of today's non-`.pre-` SEAT kits plus yesterday's B7xx kits: 9740-9749 hits only B707 (finished gate, same project); 9750 and 9760 and 9770 blocks hit 2 each, 9790/9800/9960 hit 3 to 5. Chosen 9740-9749. B735 is not yet a file; if it takes 9740-9749 the stamp must move this seat.
- Model: row G2 at `model-routing.md:109`, G-cap `:111` (both printed); `brief_seat.sh:24` default opus (printed), so the launch carries `BRIEF_SEAT_LEVEL=sonnet`.
- Squash source: `CLARIFICATIONS.md` line 1799 exists and describes the PR #88 landing (printed).
- Reuse files named in the kit all exist (loop with a MISSING echo printed nothing; the B699 `fuzz1.json` and `corpus1..3.json` listed).
- Slot lines: `/usr/bin/grep -c -E '_{4}'` = 9 (8 slots + last line); `@XXX@` pattern 0; non-ASCII bytes 0; person-name grep 0 (the only hits are the builder seat id J20).

## D-decisions
- D-1 Verdict wording: the table in the B707 template says GO WITH FOLLOW-UPS; the task said "GO WITH FINDINGS conditional". The kit uses `GO WITH FOLLOW-UPS (conditional: CodeQL not scanned)` (the repo's own grade word); Tuesday may rename.
- D-2 Class defined as a property with five limbs: B707-1 form still lost, kill lost vs the ROUND-2 head (not vs OLD), real DEPLOY.md red, loosening, a named row red under nothing. Kills both heads lose that are not B707-1 forms are Notes/residue. This is how the product owner's "one more round on the array-index miss" is kept narrow.
- D-3 The most likely regression the kit makes the gate attack: the new `${...}` text zone swallowing a REAL here-document in a `$(cat <<EOF` inside it (builder says `${` closes with `closeOf` only, no `$(` stop, whereas the subscript zone stops at `$(`). UNMEASURED by me; written as an attack, not a claim.
- D-4 Hard stop: target 90 min, hard stop 2.5 h after Step 0 (slot text); Tuesday names absolute clocks. Container budget about 25.
- D-5 REUSE: B707's finished evidence/scripts (renamed 707 to 736 by program in copies) plus B699 corpus; the builder's evidence and trees stay read-forbidden.

## Q for Tuesday (each with a default)
- Q-1 CodeQL: GitHub is not starting Actions jobs. Launch the gate now (default YES: the gate's C1-C4 do not need CodeQL) and land only after a real scan. The gate polls check-runs only by GET and never re-runs anything.
- Q-2 Accept the verdict word in D-1 (default: accept).
- Q-3 Accept port block 9740-9749 (default: accept; re-check against B735).
- Q-4 Should the gate also be told that B707-2 is to be ruled out or ticketed? Default: ticketed, not re-gated (as written).

## UNMEASURED
No build, test, container, pty, corpus or fuzz run by me; the claims 48/48, 507, 16189 shapes, 19/33/33 closed, red-proofs, lint/format/typecheck are all RELAYED. The mergeable_state `blocked` cause is inferred (missing required check), not read. The tree of pull/94/merge at b8286c8a not read. `compare` of main against the base: my own call returned 404 on a shortened sha, so the four moved main paths are RELAYED from the builder (the kit says so and tells the gate to re-list with a full sha).

## Outside the fences
None. Read-only: Read/grep/ls/tmux/lsof/uptime, `gh api -X GET` under the Composer `GH_CONFIG_DIR`, `git --no-optional-locks ls-remote` and `show` (counts only). I typed one `cd /dev/null` in a single command; the hook refused it (nothing ran) and I re-issued without it. I read `model-routing.md` lines 105-111 and `brief_seat.sh` grep lines only. I did not read `fleet/briefs_staged/`, the scoreboard, the ledger, or any card store. Wrote only the kit and this report (plus a `sed -i` of three time strings inside the kit).
