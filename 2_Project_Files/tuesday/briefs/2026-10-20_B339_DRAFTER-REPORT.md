# B339 drafter report (SEAT-W17R, Composer records: fold records/b328, three B320 rows, PR #82 landing, history)

Drafted 2026-10-20 19:46 to 19:55 AEDT. Read verbs and `gh api` GET only (GH_CONFIG_DIR = Composer `4_Credentials/.gh-config`). Nothing written outside the brief and this report. Brief: `2026-10-20_B339_SEAT-W17R_composer-records-fold-b328-b320-rows.md` (34 KB, over the ~25 KB ask: the exact row texts, the shas and the REFUSE inputs are load-bearing; B328's was 42 KB). One slot: `@SLOT:STAMP_TIME@` (`grep -c` = 1, control on a planted slot line = 1). `READ-WHOLE-BY-TUESDAY` line is left for you.

## Sources read whole
Template B328 brief; `Briefs/2026-10-20_B321_STATUS.md` (fold method, worked example); B320 STATUS (all 137 lines); project `CLAUDE.md`; B298 brief lines 25-38 (A1, A3, A3a); B328 STATUS root After block; B328 drafter report. Partial: `main`/`records/b328` BACKLOG rows 84, 320-322, 326, 327, 330, 353; B301 records commit `git show f18c6fff -- BACKLOG.md` and its history entry (the "landing" convention); head and tail lines of B322/B331/B333 STATUS.

## Measurements (instrument, time)
- Root `main` = `d59cfb53c6bf69251d8c22f670e92b89b7e79366` (`rev-parse`, 19:46:10). `records/b328` = `447f5a0781f60f3b34b73170398eb030714d6fd9`, `rev-list --count main..records/b328` = 1, `merge-base --is-ancestor records/b328 main` rc 1, `records/b321` ancestor rc 0 (control). Trees: b328 `f76399931a39…`, main `37c09ffb…`. Remotes 0. Root status 1006 lines; ` M`: B26 STATUS, B298 STATUS. Newest ref by date: `records/b328`; `records/b339*` count 0.
- `diff --name-status main records/b328`: 46 = 42 A + 4 M (BACKLOG, CLARIFICATIONS, history, B321 STATUS), all 4 clean in root. By my own script (`cmp`-equivalent bytes compare): of 42 A paths, **12 exist untracked in the root, 11 byte-equal, 1 differs** (B328 STATUS: 25,417 committed vs 30,125 root, `startswith` True); 30 absent. Five root-only evidence files not on the branch (B328's own After block names four; disk holds five: `hidden-scan-status-after.txt` is the fifth). Hidden-char scan of those five, B328 root STATUS, B320 STATUS, B320 brief: 0 hits; control `chr(0x202E)` fires.
- BACKLOG on `main` and `records/b328`: 352 numeric ids, last `| 362 |`; C-96 is the last entry on `records/b328`, C-85 on `main`. Rows #326/#327 have 5 awk fields (3 cells).
- PR #82 (`gh api` GET, 19:46:41): closed, merged true, merged_at 2026-10-20T07:22:28Z = 18:22:28 AEDT, merge_commit_sha `318df1767035e92a55f633824927ce01b9986293`, one parent `d8d2a2c7…`, tree `d0df075e2dd8fc3cb2fa6a562555b63c3405da8f`; head `e6288983…` tree identical; main ref = `318df176…`. PR #81 merged 2026-10-19T18:13:48Z (05:13 AEDT). Only those two commits on main since 2026-10-19T13:00Z. PR #83 open, draft, head `8e062d94…` (19:47).
- sha256 (19:48): B328 root STATUS `5b5fd939…`; B320 STATUS `069c52c4…`; B320 brief copy `40992007…` (equals Tuesday's original and B320 STATUS line 14); B301 root STATUS 31,161 bytes `87f390fa…` = `main` blob size; `grep -c -i 'RECORDS COMMITTED'` on it 0; B320 evidence folder 1,868 KB, 376 files.
- Live at 19:46 (`ps`, `tmux list-panes`): B323 (pane `%135`, sonnet, since about 18:57), B335 (pane `%137`, opus, since about 19:01), plus other projects (HPSM-POC B337, NexusAI gate 32). No Composer records seat. `.tools` holds b320, b321, b328, b331, b335 trees; no b339. Load 8.82 / 5.25 / 3.54 (19:47).
- `AGENTMAIL_API_KEY` count 0 (control 1).
- Tool note: this session's no-cd hook refused a `git worktree list` (counted as a write verb); I did not retry it.

## Decisions I made in drafting (all reversible by editing the brief)
1. **Fold method = merge on root `main` with 12-path quarantine**, as B328 did for b321 (not a stacked branch): B328 is finished, collisions are measured and clean. Added the `main^{tree}` = branch tree assertion as a stronger check.
2. **Rows: #363 B320-1, #364 B320-3, #365 B320-6**; B320-2/-4/-5/-7 no row, source = row #327's own "(Notes, no row)" (B297-1/-3) plus B320's severities. No C-entry (Tuesday's rulings are coordinator rulings, no Kam tap).
3. **Beyond your three items, two additions, each named in the brief so you can strike them:** (a) State cells of #326 and #327 flip to MERGED with `Was:` (the B301 convention for #320-#322; leaving "FIXED ON A BRANCH, NOT MERGED ... Nothing is closed until Tuesday lands the PR" would be a false cell); (b) the seat files the B320 STATUS and brief copy (2 files) so the rows' cited path is tracked.
4. **One network step allowed for the seat** (4 `gh api` GETs, project gh config): measures the landing so the records say MEASURED. A `gh` failure is not a STOP (marked RELAYED); a "not merged"/different sha IS a STOP.
5. Launch line is yours verbatim (no `WED_USAGE_STOP=100`; the B328 line had it). Full path to `cockpit.sh` used.

## Open questions, each with a recommended answer
1. **Flip #326/#327 to MERGED?** Rec: yes (B301 convention; brief Step 2). If no, strike that bullet and the two #326/#327 asserts.
2. **File the B320 STATUS + brief now?** Rec: yes, these two only. The 376-file evidence folder (and the untracked B322, B331, B333 records, plus B323/B335 when done) should go in one later catch-up round, B298-style, after B335 and B323 finish.
3. **Stale cells #340 ("ASSIGNED to brief B322") and #353 ("ASSIGNED to brief B323 (queued ...)")**: both now wrong (B322 built PR #83; B323 is live). Rec: not in this seat (they change again at B335/B323 close); FOR TUESDAY line, handled in the catch-up round.
4. **B323 and B335 REFUSE checks** may name "a live Composer seat" as a STOP for them if re-read. Rec: addendum naming B339 as an allowed records seat (root repo only) before launch, as the stamp section says; or launch after confirming neither re-checks.
5. **Optional separate linear-class test** (B320 STATUS "Fix-shapes and regressions in prose"): not requested, not a row. Rec: leave to your call; the brief only lists it under FOR TUESDAY.
6. **B320-4/-5 (comment wording Notes)**: no rows (you said Notes). Row #364 carries a one-line pointer to them. Rec: keep; if you want them untouched, drop the "Related Notes" sentence.
7. **Load**: 8.8 with B335's gate running. Records work is light; no action. Rec: launch now.
8. **Brief size 34 KB.** Rec: accept; the cut candidates are the Standing lines and the history bullets if you want it under 30 KB.
