STARTABLE: YES
# B972 drafter report | SEAT-R94 records kit: UAT deploy of e8ac3f29, PR #261, frame-chip ticket (Sonnet 5.5, read-only, 2026-10-31 after 11:50 AEDT)

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B972_SEAT-R94_hpsmpoc-records-uat-deploy-261.md` (79 lines, unstamped). **Unstamped slot count 13** (12 slot lines + the final `READ-WHOLE-BY-TUESDAY: ____`; MEASURED `/usr/bin/grep -c -E` 13, control `a____b` 1), 0 non-ASCII bytes by program, 0 `@X@` tokens. Launch: seat `Datasec/HPSM-POC-R94`, `BRIEF_SEAT_LEVEL=sonnet`, model claude-sonnet-5-5 (read from models_latest.json levels.sonnet.model_id).
- Scope: Jira = 1 create (T1, the frame chip), 1 label add, 29 comments (28 deploy comments + the PR #261 landing comment on HPSMPOC-399), 0 edits, 0 links, 0 transitions by default. Records = 2 C-entries (C-249 PR #261, C-250 the deploy), a BACKLOG section (README line is B972-2, a row not a ticket), 1 history entry, 3 or 4 catch-up STATUS copies (B968, B970, B971, optional B969).
- **Done decision default: COMMENT-ONLY.** The only precedent that moved keys after a deploy is C-223 (heading `CLARIFICATIONS.md:4653`, bullet `:4677`): HPSMPOC-359 and -360 moved to Done by the stamp AFTER B874 had deployed UAT and the demo, citing the rule at `:1904`. C-216 (B804, UAT + demo) moved nothing; C-138 (`:2269`, B437, UAT only) moved nothing. No precedent moves a key after a UAT-only deploy, and B971 holds the demo. MOVE-DEPLOYED stays available at your call (Q-1).

## Measured (all read-only)
- Records `569884a54a4198e214cdfcc8b3b20c4ec20850b7` (PR #156 merge), 0 open PRs, `records/b972` absent (control `records/b925` 1). `CLARIFICATIONS.md` 4890 lines, highest C-248 (control count 2); `BACKLOG.md` 2528; `history.md` 2587, top entry B969. Records tree lacks B968, B969, B970, B971 STATUS (0 each; control B967 present 1). Nothing of #261 or the deploy is in records (`B971|e8ac3f29` 1, inside C-248; `#261|HPSMPOC-399` 1, an older mention).
- Code main `feb3da655e12f604ef1c2b9ad65d6aaffb69c78f` = PR #261 (merged 10:55:39 AEDT, head `f7597aaa`, 1 commit, 1 path, +3 -0, 1 parent, verification valid, `localdomain` 0); check-runs 19 (18 success, 0 in progress); ci run 41147311348 and Push on main 41147311428 completed success; 0 open code PRs. S `e8ac3f29` is its parent; #261 ships nothing.
- STATUS files (lines, sha256 prefix, last-line family): B968 99 `c33f55cddebd587a` READY FOR QA; B969 132 `4b0c52224a8680f1` RECORDS COMMITTED; B970 238 `2127e13c2741cb1e` VERDICT GO WITH FINDINGS (7 Notes, none above Note); B971 273 `46e9bd3eafa4cd24` PARTIAL: UAT DEPLOYED. `HP Restricted` 0 in B968, B970, B971 (single grep, no firing control run by the drafter; the seat re-runs its scans with controls).
- Panes: only `%0 tuesday`, `%1 fleet-monitor` (no R94, no G, H or D pane). Gate B970 final; B971 is a deploy, not a gate.
- Jira GET (status, comment count; B969 helper `api("GET")` only): of the 29 keys, **HPSMPOC-110 Done; the other 28 Backlog, 1 comment each** (B969's landing comments). HPSMPOC-399 Backlog, 0 comments. HPSMPOC-405 to -420 Backlog; newest key HPSMPOC-420 (-421 reads 404). Controls: `key = HPSMPOC-268` 1, `qxv9k2zzprobe` 0, `UatOpenTests` many, `REC-DEPLOY-31OCT` 0. `text ~ "questions answered"` lists HPSMPOC-420 (B967-5, "1 of 3" vs "0 of 2"): a different observation, so T1 is new and names it as related.
- README: `infra/README.md:227` at S reads "UAT is the copy HP reviewers open (C-52)." (MEASURED via contents at e8ac3f29); C-52 is `CLARIFICATIONS.md:555`.

## The Done moves: candidate list (MEASURED status; MOVE-DEPLOYED applies only if stamped)
Rule used by the kit: the 28 Backlog keys of the UAT range, minus HPSMPOC-403 (PR #251 declines item 1: open residue the PR says is not built), minus any key whose Done-when is not met by its gate closure line (read by the seat at Step 5, else HELD). Never HPSMPOC-110 (already Done), -399 (PR #261, items B908-4/-7/-8 open), -405 to -420.
- Candidates, all currently **Backlog**: 357 365 366 367 368 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 401 (UI or style keys, in the deployed package), and the infra or test-only 363 364 398 404 (ship nothing a visitor sees; in the list only if their Done-when reads met, test-only precedent C-186). That is 27 at most. Excluded: 110 (Done), 403 (declined item).
- Their Done-when text was NOT read by the drafter (UNMEASURED); the seat reads each whole.

## Questions (Q) with defaults
- **Q-1 Done moves:** COMMENT-ONLY or MOVE-DEPLOYED? Default COMMENT-ONLY (precedent C-223:4677 followed a UAT + demo deploy; the demo is held; no UAT-only move precedent). If you choose MOVE-DEPLOYED, say so in the slot; consider that the product owner's veto review of the new words has not happened.
- **Q-2 test-only keys (363 364 398 404):** if MOVE-DEPLOYED, include them? Default include only when Done-when is met (kit text).
- **Q-3 B969-COPY-SLOT:** B969 STATUS is also missing from records main; copy it? Default COPY.
- **Q-4 HPSMPOC-110:** Done already; the kit gives it no comment (29 of 29 keys named by the deploy, 28 commented). Default keep.
- **Q-5 T1 grade:** filed ungraded ("observation, not graded"), no Priority set (create.py sets none). Default keep.
- **Q-6 README line:** BACKLOG row B972-2 only (no ticket, no Jira). Default keep.
- **Q-7 B971 FOR TUESDAY 7 (b) to (e) and 9** (Admin sidebar button at the fold, Feedback pill overlap, Demo chooser aliases, four unrendered words, two webhook references SecretNotFound): one BACKLOG row B972-4, no ticket. Default keep.
- **Q-8 C-number order:** C-249 = PR #261 (10:55:39), C-250 = the deploy (11:27:54), chronological. Default keep.

## Stamp values I recommend (Tuesday fills; the drafter filled none)
- DONE-MOVES-SLOT: COMMENT-ONLY. B969-COPY-SLOT: COPY. Hard stop: 90 min target, 180 min hard stop from the seat's Step-0 date. Heads: records `569884a5...`, code `feb3da65...`. GATE-CLEAR: CLEAR (B970 final; no gate pane). Launch window: any time load1 below 7 (launch_when_cool). AUTH-RULINGS: none beyond the launch authority. Sequencing: default accepted.

## Not measured
Done-when text of the 28 keys; whether Jira's text search tokenises the new markers (positive control is `UatOpenTests`); whether any pane or Jira write appears after ~12:00; the PR-to-key map for #239-#243 (the seat builds it by program and asserts the union is exactly the 29 keys); B971's screenshots (not opened, not needed). Nothing was written to any project, Jira or repo; no mail sent.
