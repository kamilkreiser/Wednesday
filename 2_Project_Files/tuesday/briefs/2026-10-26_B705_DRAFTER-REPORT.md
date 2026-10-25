STARTABLE: YES (after Tuesday stamps the 8 slots and the last line; the unstamped kit reads 9 lines with the four-underscore pattern, measured)

# B705 drafter report (SEAT-J18, Composer PR #94 fix round 2 of 2)

## BLUF
Kit `2026-10-26_B705_SEAT-J18_composer-94-fix-round-2.md` (133 lines, ASCII only, 0 hits for the owner's name) is cloned in shape from B695 and B679. It writes Tuesday's rulings (a), (b), (c) verbatim, makes B699-1, B699-2, B699-5 MUST FIX with the gate's regression rows (red at head 0307e31a, green after), and adds the three B699-7 pin-gap rows (Q1, Q5, Q7) with named swaps. The kill-lost sweep re-runs the gate's corpus (142 shapes) and its 5000-block fuzz (token-exact), plus a fresh-seed fuzz of the builder's own. A same-class NO GO at the round-2 gate means the closed instances ship and the residue is ticketed or goes to a product-owner card (stated in the kit, citing model-routing line 111).

## Facts re-measured (instrument, control)
- Origin pins (git ls-remote, 00:0x 26 Oct): main 0b52848c; branch b695/composer-deploy-guard-pins and refs/pull/94/head both 0307e31a. Control: 'refs/heads/b631*' prints one line; 'refs/heads/b705*' prints nothing.
- PR #94 (gh GET): open, not draft, mergeable true, state clean, base 667830ed, 1 commit, 1 file. Open PRs: #94, #92, #91, #86, #85 (draft) only.
- compare 667830ed...0b52848c lists exactly PR #93's three paths (schema.d.ts, document.ts, openapi.json); none under packages/db.
- Test file at head (gh raw contents): 616 lines; 29 literal `it(` plus the 3-tag loop = 31 runtime rows; anchors at :64, :150, :203, :218, :113, :531-:557 confirmed by grep -n. Control: an absent string counts 0.
- Model: model-routing.md:92 row C2 (Sonnet "1st"), :109 row G2, :111 G-cap; models_latest.json levels.sonnet.model_id = claude-sonnet-5-5.
- Ports 9720-9729: lsof rc 1 (control: the same lsof lists a listener on 7000). Word-scan of 2026-10-24/25 non-pre SEAT kits: six finished kits name the block (B621, B622, B648, B657, B677, B678), none of B700-B704; none of their panes is live. Live panes: tuesday, Datasec/HPSM-POC-R45, Datasec/MPS-G131, fleet-monitor. No Composer seat live.
- Pane name Security-Composer-J18: 0 kits name it (control: J17 kit names J17, count 1). `.tools/b705` absent, `wt-b705-*` absent; `.tools/b695`, `b698`, `b699` and their worktrees exist (finished seats) and are fenced off in the kit.
- Gate evidence reusable: corpus1-3.json, fuzz1.json, instr/scripts/* exist under Briefs/2026-10-25_B699_evidence/runs/. The kit allows a named subset and forbids the mutant drivers (mkmut.py, mutres.py, etc.), as the template does.
- Builder-script source `.tools/b695/scripts/` holds common.sh, dbtest.sh, dbone.sh, heavy.sh, names.py (21/74/12/42/49 lines).

## D-decisions
- D1 The union design (gate's alternative) is allowed only if no existing expected value changes. Reason: the head's rows at :502-503, :537 and :544 pin `[]` for shapes the old reading flags, so a union flips them and that is a loosening. Targeted fixes are the default. This narrows the instruction slightly ("allowed if it proves kill-lost 0"); it is a STOP-with-question in the kit, not a ban.
- D2 Rows are written FIRST and run red at the head, then the fix (the gate's requirement), so the three regression groups are proven red by name with the text reporter's assertion quoted.
- D3 Ruling (a) allows one comment sentence above :537 and nothing else; (b) and (c) need no edit. Ruling (c)'s BACKLOG row is Tuesday's to file.
- D4 B699-7 pin gaps are ruled IN this round (rows plus named swaps), as the task required; D1 and D2 gate mutants are Notes, not required.
- D5 Round count text: "round 2 of 2 on PR #94's own count" per the B695 stamp ruling; the gate's cumulative-read caveat is quoted once, not relitigated.

## Q-questions for Tuesday
- Q1 (the one that matters). The task said the builder must "bring the branch up to main the way earlier fix rounds did, quoting the rule". I found NO such step in any earlier fix-round kit: B679 (PR #92 round 2) line 5 forbids merge/rebase and pushes one fast-forward commit on the PR head (base stays the head, line 110); B641 line 43 treats main moving on other paths as "not a refuse by itself". So the kit does NOT merge or rebase main; it quotes those lines, requires compare-of-main and `mergeable` reads at start and before the push, and relies on the gate's recompute (merge tree f689812e, no conflict) plus the head-pinned squash. DEFAULT: as drafted. If you want main actually merged in, that is your decision and a new instruction (the kit's own prohibition on merge/rebase would need lifting).
- Q2 Stamp: gate tier 2 (G2) and the target READY / hard stop clocks are yours (suggestion 2.5 h / 4 h after Step 0). DEFAULT: tier 2.
- Q3 Whether to keep the optional macOS bash 3.2.57 host-pty report for A01/A03/A13/A14/A17/A18 (kit makes it optional, "MEASURED or not measured"). DEFAULT: optional.

## UNMEASURED
No build, test, container, mutant, pty or corpus ran. Not measured: that the renamed scripts run; npm ci cache; that each regression group is red at head in the file's own scanner (RELAYED from the gate's old/new cells); that the Q1/Q5/Q7 swaps are each killed by exactly their row; the head group baseline 38/490 (RELAYED); that the gate's harness files run under a renamed kit; pre-commit hook inside a worktree commit. The `git log` of the file is stated as "expected two commits" without my having run it.

## Outside-the-fences disclosure
- Read-only everywhere except my two files. One scratch copy of the test file at head was written to the session scratchpad (`.../scratchpad/head.ts`) by redirecting `gh api -X GET` raw output; it is outside the project and the briefs tree.
- Read: DRAFTER_RULES whole, B695 kit whole, B699 STATUS whole (385 lines), B679 kit lines 1-60 and greps of the rest, model-routing rows, models_latest.json, B641/B623/B646 kit greps for the main-moved rule, evidence directory listings. No decision-queue, scoreboard, ledger, briefs_staged, Wednesday or Friday tree touched. No HTTP to hosted hosts; gh GET only under the Composer GH_CONFIG_DIR; git read verbs only (ls-remote). Two tool hooks fired (a grep-case advisory, and one refusal of an unquoted `====` word in a command I typed); the refused command was re-run.
- The date rolled over to 26 Oct mid-session (clock 00:00); the kit is dated 2026-10-26.
