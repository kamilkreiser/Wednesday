STARTABLE: YES (comment-only defaults; every Jira write and the C-entry wait on stamp slots; no MPS pane is live, the HPSM-POC panes G354 and H131 are another repository)

# B1331 drafter report: SEAT-R183, MPS records for #159 and #160

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-06_B1331_SEAT-R183_mps-records-159-160.md (91 lines; 13 four-underscore runs = 12 slots plus the last line, by `grep -c -F`; 0 non-ASCII bytes by `LC_ALL=C grep -c '[^ -~]'`). Slots: 2026-11-06_B1331_slots.json (13 keys, safe defaults, no angle-bracket placeholder, nothing attested for Tuesday). Shape copied from the B1316 (R180) kit `.pre-stamp`. Clocks (date, AEDT): 15:05:42 first read, 15:08:39 last `date`; nothing in the kit is later.

## BLUF
- One records pass, next number **C-96** (highest heading C-95 at `CLARIFICATIONS.md:2571`, anchored C-96 count 0). Root main `40c01265` (R180's commit), code main now `aa7fd175` (the #160 squash).
- #159 (MPSCALC-116, squash `7648e03a`, 14:08:58 AEDT) and #160 (MPSCALC-107, squash `aa7fd175`, 14:09:15 AEDT): both merged, one parent each, 8 check-runs success each, `ci` and `Push on main` on `aa7fd175` success attempt 1. The review (`B1325_STATUS.md`) marks every Done-when clause of both MET (item 2, `:76`-`:78`). The clause text is the builder kit's, relayed; the tickets carry no Done-when line (read whole). Both are movable under C-79 if the stamp names them. MPSCALC-107 is the only one with a contradiction candidate: M2 is GO WITH FINDINGS with three Minors, so reading (k) (slot ROW-RESIDUAL) decides; default NO means comment only.
- Minors B1325-1, -2, -3 (`:62`-`:64`): rows by default (`[B1331-M-1..3]`), one ticket if slot MINORS-AS = TICKET (one create at most, searched first). Pointers re-printed at `aa7fd175` by me: `cssColourGuard.test.ts:100-103`, `:101`, `cssColourGuard.ts:58-65` all match the review's.
- MPSCALC-118: one comment carrying the 13:14 reasoning (second implementation of the cent rounding; the narrowed form adds only strings and does not hold the stub equal to the engine; purchase half stays open; not a ruling). Never moved.
- MPSCALC-374 and -375: R180's two comments (40777, 40778) already state most of what each move rests on. The kit makes this a **gap table** and writes a comment only for a MISSING item. My eyeball read: -375 has all five checklist items; -374 lacks "reversible and what reverses it" and does not name reading (k) or call it the coordinator's reading. Expect one comment (-374), probably none on -375. No transition on either, ever.
- Writes: at most 8 (1 create, 5 comments, 2 moves).

## Facts re-measured (instrument; control)
- Jira by paging all keys (scratch reader copying the project `.env` read in-process, GET only, no token printed): 384 issues, Backlog 232, Done 152. Control: highest key MPSCALC-384 equals the count. Keys: -107 Backlog 1 comment (39427); -116 Backlog 0; -118 Backlog 0; -374 Done, comments 40723, 40777; -375 Done, 40724, 40778; transitions 11/21/31/41 on all (41 = Done). `text ~ "B1331"` 0 and `"B1325"` 0, `"readVars"` 0, control `"B1196"` printed 5+ keys (list cut at 5 by my 100-char print, R180 had 6), `key = MPSCALC-269` 1. `PROPOSAL_COLOUR_TOKENS` -> MPSCALC-107 only (a name match, its own text states the token-list defect, not the Minors).
- GitHub by `gh api -X GET` under the MPS `.gh-config`: main `aa7fd175230ccff72f82bb17267785e49f84b665`; open PRs 0; control `pulls/99999` 404. Merged times converted by `date -r` from the API's UTC. Code-scanning open 0 and fixed 0: **a zero with no control that fires**, written into the kit as such.
- Root by `git --no-optional-locks`: HEAD = main = `40c01265`; dirty tree exactly `history.md`, `BACKLOG.md`, `JIRA.md` (+4645 lines); CLARIFICATIONS 2581 lines, BACKLOG 5028, JIRA 624, history 1388. `.tools/b1331`, `records/b1331`, `.tools/.git-lock` absent. `df -g /` 357 GiB.
- Panes (tmux): `tuesday`, `Datasec/HPSM-POC-G354`, `fleet-monitor`, `Datasec/HPSM-POC-H131`; no MPS pane. Port scan: `lsof` over 9900-9999 printed 0; word-boundary scan of 40 non-`.pre-` SEAT kits of 5-6 Nov for `R183`, `B1331`, `b1331`: 0 each; control `R180`: 4. No port block needed (records seat).
- Pointers printed by `awk NR`/`grep -n`: C-79 `:1712 :1714 :1716 :1727 :1839 :1957 :2218`; `B1325_STATUS.md` `:1 :62 :63 :64 :74 :76 :77 :78 :79`; `B1316_STATUS.md` `:358 :368 :369 :374`; `B1316-DONE-1/OPEN-1/BATCHES` `BACKLOG.md:5011 :5017 :5023`; the daily note 13:14 line is line 64 of `0_Brain/daily_tuesday/2026-11-06.md`; model `model-routing.md:97 :98 :110`, `models_latest.json:23`, `brief_seat.sh:24`.
- R180's FOR TUESDAY item 5 (a)/(b) read whole at `B1316_STATUS.md:374`; comments 40777 and 40778 read whole from Jira (GET) into the scratchpad.

## D-decisions
- D-1 C-79 is the rule; readings only as worded; (k) is a slot, default NO.
- D-2 Defaults are comment-only (MOVE-KEYS NONE). The recommended stamp for the two moves is MOVE-KEYS "MPSCALC-107, MPSCALC-116" with ROW-RESIDUAL YES (as the 11:38 pass stamped for -335 and -374).
- D-3 Minors as rows, not tickets (earlier Minors were rows; R180 had no create); a ticket is the stamp's choice and then exactly one, searched by symbol first.
- D-4 The 374/375 job is a gap table, not a rewrite, and a clause read unmet is reported, never a back-move (fence: no transition on 374, 375 or 118).
- D-5 One C-entry, C-96, in the landing-entry shape of C-93 and C-94 ("a landing recorded by the coordinator; no product-owner ruling"), with RULING-REF able to override.
- D-6 Kit text avoids "deployed": the review's item 3 sentence for MPSCALC-116 and -107 ends "nothing is deployed", which trips the word ban; the kit substitutes "nothing is in any hosted build".
- D-7 I named "Tuesday" nowhere in the text the seat copies; the 118 comment says "the coordinator's judgement of 2026-11-06". The comment's "not a ruling" line is the user's own instruction.
- D-8 READY 90 / HARD STOP 180 minutes as R180 (a comparable job with up to 8 writes).

## Q-questions for Tuesday (each with a default)
- Q-1 Does model row C7 (client-facing comment) apply to these Jira comments? Default: no; C8 as R180 (the MPS board is Datasec's own; no human outside the team is messaged).
- Q-2 Stamp MOVE-KEYS for MPSCALC-107 and -116? Default: both, with ROW-RESIDUAL YES so the three Minors held as rows do not hold -107; the kit's own default is NONE/NO until you stamp.
- Q-3 Minors as ROWS or TICKET? Default: ROWS. Say TICKET only if you want a Jira key to hang a later fix on (B1325-3 is a simplification the review said you could close).
- Q-4 Should the 118 comment also say the narrowed form is "available to build if the product owner wants stub fidelity"? Default: no; the kit states only the judgement and that the purchase half is open, because the user's instruction was to prevent a re-proposal and not to invite one.
- Q-5 -374 and -375: stamp FILE-GAPS (write only the missing items)? Default: FILE-GAPS.
- Q-6 Should -374's missing "reversible" sentence also record that the product owner was told at 11:38? Default: no (a person-reach claim is Tuesday's to attest; the kit forbids naming a card or a person).

## UNMEASURED
- The seat's gap table is not run (my read of 40777/40778 was by eye); no Jira write; no test; hosted CI/CodeQL beyond the check-run names on the squashes; whether the review's evidence folder holds more than its STATUS lines for the clause marks (the kit tells the seat to read it); hosted MPS state; whether any demo uses the in-app stub; the B1327 report's stub pointers (relayed until the seat prints them); whether a new MPS seat appears before launch.
- I did not read the full -374 and -375 "Earlier" comments 40723/40724 (only the R180 comments 40777/40778).

## Outside the fences
Wrote only the kit, the slots file and this report (Write tool; one Edit on the slots file to remove a "by" that read as an attestation). Reads: DRAFTER_RULES.md; the B1316 `.pre-stamp` kit and its slots.json; the B1316 STATUS (grep lines, FOR TUESDAY block); the B1325 STATUS whole; the B1327 DRAFTER-REPORT; `model-routing.md` lines by `awk`/`grep`; `models_latest.json:23`; `brief_seat.sh:24`; the daily note by `grep -n` on `13:14`, `B1325`, `#159`, `MPSCALC-118`; the headers of `.tools/b1316/j1316.py`, `showjira.py`, `jsnap1316.py` (read only; not run); the R172 kit lines for the create form (`grep -n`); `CLARIFICATIONS.md`, `BACKLOG.md` lines by `awk`/`grep`; the five Jira issues and counts via a scratchpad GET-only script reading the project `.env` in-process (no token printed); `gh api -X GET` under the MPS `.gh-config` (pulls, ref, commits, check-runs, compare, actions/runs, code-scanning, contents at `aa7fd175`, raw copies to the scratchpad); `tmux list-panes`, `lsof`, `df`, `uptime`, `ls` of `.tools` names. No decision_queue.sh, no briefs_staged, no scoreboard.md, no _ledger.md, no WEDNESDAY or FRIDAY tree, no hosted host, no mail, no Artifact or Docs tool. Hook refusals: one `cd` (stopped before running), one unquoted `=====` word (stopped), re-issued.
