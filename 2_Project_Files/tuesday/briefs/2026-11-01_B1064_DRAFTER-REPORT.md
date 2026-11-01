STARTABLE: YES (after Tuesday stamps the six `____` lines; launch via launch_when_cool, level sonnet inside the quotes)

BLUF: the relayed "batch 4 = 63 evidence-only keys" is not a remaining list. B987's drafter defined the 63 as the `[B583]` "merged work names this ticket" set, which B1019 (3a, 39 keys) and B1021 (3b, 38 keys) already took whole (MEASURED: every Backlog key holding `[B583]` is `[B1019]`, `[B1021]` or one of -153, -261, -295). The real remainder, measured over all 357 issues: 257 Backlog, 158 with no comment, 99 with comments and no earlier records marker; of those 46 carry a landing comment, 16 say "merged" with no sha, 37 show no merged change (C-79 :1716 leaves them). The kit is **batch 4a = 30 keys** whose landing comments name MPS #109-#132 (the size earlier seats finished: 28 and 30). Remainder for following kits: **4b** 16 keys on older PRs (-33, -47, -49, -50, -53, -55, -78, -93, -98, -100, -140, -142, -155, -158, -194, -203; six are spec-seed, probably the relayed "6"), **4c** 16 merged-no-sha keys (-13, -35, -36, -48, -51, -57, -69, -95, -101, -202, -206, -227, -247, -248, -250, -251). The "5 others" were not identified separately.

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1064_SEAT-R118_mps-records-done-batch4.md` (seat `Datasec/MPS-R118`, B1064, sonnet C8 `model-routing.md:98`, 60 writes max, target 150 / hard stop 210).

Count proposed (lead only, from Jira comments, not a verdict): 14 MOVE likely, 12 CONDITIONAL, 4 HOLD (-310, -331, -333, -334). Expected about 14-22 moved, 8-16 held. Five keys (-207, -302, -336, -338, -339) are gates at the round-cap NO GO whose reading of the ticket is MET: they move only if Tuesday stamps `CAP-READING` YES (default NO).

FACTS RE-MEASURED (instrument: a GET-only urllib reader of the project `.env` in-process, scratch scripts under the session scratchpad; `gh api -X GET`; git read verbs; tmux)
- Root main 240acf35 (B1057's ff; its STATUS last line quoted), 48 heads, status 859, numstat BACKLOG +2378, JIRA +388, history +457, CLARIFICATIONS 1951 lines, C-79 at :1712, newest section :1931. Code main 3496da33, open PRs [121,120], 404 controls fire.
- Jira 357 issues, Done 100, Backlog 257; controls zzqxnonexist 0, MPSCALC-341 1, MPSCALC-357 1; text B1064 0, label 0; transitions on -218 and -356 list 41 Done.
- 17 PRs (#109-#132 set): all merged, base main, squash ahead of main, behind e027ebd0; check-runs 8/8/0 except **#116 (110ebecd) 8/6/1 with a failing ci push run**: bears on -290 and -334 (carve-out slot, failing test not read).
- Selection test returns exactly the 30 (control: dropping the marker filter adds the B583 77+3 and 15 other marked keys).
- Seat name: R118 and B1064 appear only in the B1062 kit line 126 as this seat's reservation; no rival. Live: MPS-M67 (pane %9); M66 may start. R117 pane gone.

HELD-BY-RULING FINDINGS the sweep did not carry (the "caught one" check)
- MPSCALC-221: `CLARIFICATIONS.md:1669` item (d) "secret-scan false positive of B866-9 ... with or without joining MPSCALC-221: not ruled". Kit makes it a quoted condition (slot `ROW-RESIDUAL`, default NO = comment-only).
- MPSCALC-335: its own comment 40153 says the marker line "is not ruled" (same slot).
- MPSCALC-331 and -333 landed on a "round-cap card default (a default executed, not a ruling)"; kit says a default does not close a clause.
- Rulings found by search and named at source: C-66 (-330, -332), C-67 (-290), C-72, C-73, C-74, C-75, C-76, C-77, C-78 (-336, -338, -339, -340, -346, -350 to -353).
- -310 comment 40156: "Not met and not built" (Part B). -334 part B unprovable (spec does not load).

D-DECISIONS
- D-1: split. 30 keys now (4a); 4b and 4c named above, drafted after this lands.
- D-2: reading (i) (cap NO GO) not applied by the drafter; made a Tuesday slot, default NO, because B1021's slot was stamped per batch.
- D-3: kit drops the create leg and the B1057 maps/donewhen/freeze files (not run by a records-only 30-key pass); the seat copies only files it reads first.
- D-4: the kit corrects the relayed batch map in the new CLARIFICATIONS section (item 3), without editing :1702.

Q FOR TUESDAY (each with default)
- Q-1 `CAP-READING` for -207, -302, -336, -338, -339. Default NO (comment-only); say YES only if you want reading (i) extended to these.
- Q-2 `ROW-RESIDUAL` for -221 and -335. Default NO.
- Q-3 `CARVE-OUT` for MPS #116 (-290, -334). Default YES, seat re-measures all four parts.
- Q-4 launch authority wording: name the product owner's 2026-11-01 ruling (C-79), else the seat treats DONE-SLOT as COMMENT-ONLY.
- Q-5 should 4b be drafted next, or do you want 4c first? Default 4b.

UNMEASURED: Acceptance sentences and diffs of the 30 (lead reads comments only); #116 failing test; whether 4b/4c lists are complete (regex census, not ruled); `lsof` (not at /usr/bin/lsof, so ports are "none assigned" only); the decision store (fenced); whether M66/M67 land first.

OUTSIDE-THE-FENCES DISCLOSURE: I wrote only the two files. Scratch scripts and a 357-issue JSON dump (comment text) sit in the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/b515b667-4f65-464e-8654-81c9fa9322e5/scratchpad/`. I did NOT import the project helper `j1026.py` (it writes a heartbeat into the project `.tools`); I wrote a GET-only reader instead. The Jira token was read in-process and never printed. One `tmux list-panes`, no ports opened, no git write, no decision_queue call, no fleet/briefs_staged, scoreboard or ledger read. I read the older SWEEP and B987/B985 drafter reports in `briefs/` for the batch definition (not fenced).
