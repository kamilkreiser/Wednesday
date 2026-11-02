DRAFTER REPORT B1140 | SEAT-C80 | Composer PCOMP-23, change-report half | drafter Sonnet 5.5 (row C8) | read-only | 16:41 to 16:59 AEDT Mon 2 Nov 2026

**STARTABLE: YES, after you stamp it and the heavy lock is free.** `.tools/composer-heavy.lock` absent (16:56, `ls -d` rc 1; control `P/.tools` exists). No Composer pane (`tmux list-panes -a`, 16:56). Load1 9.03 (`uptime` 16:57), above the launch rule of 7 on two reads: NOT met now; the kit also waits on the lock itself.

## BLUF
Kit `2026-11-02_B1140_SEAT-C80_composer-pcomp23-change-report-footer.md`, 12.8 KB, ASCII, 7 underscore runs (slots). Seat letter and number free: `ls` of the briefs folder, word-bounded for `B1140` and `SEAT-C80`, 0 hits (control `B1136` in the R140 kit prints 6); only `SEAT-C1` (10-23) used `C`. Form taken from B1136 (R140) and B1096 (J41). It narrows PCOMP-23 to the change report, two paths, red first, plants, one branch, one push, no PR, no deploy. The kit does not trust the ticket's cause: Step 2 measures it and STOPs if it differs.

## Facts (instrument; control)
- Main `69b01339237d` (`git ls-remote origin refs/heads/main` 16:57; equals the sweep's). Open PRs #91, #86, #85 draft (`gh api -X GET .../pulls`, GH_CONFIG_DIR of the project, account kamilDatasec).
- Local `P/2_Project_Files` is STALE: HEAD `0b2fca43` (27 Sep); `69b01339` is not a valid object there (`cat-file` fatal). All source below was read as `contents?ref=69b01339` raw (change-report.ts 553 lines, test 316 lines, document-pdf.ts 256, pdf-fit.ts 151). The kit tells the seat to branch from `origin/main`.
- `change-report.ts:532` builds the footer (printed by `grep -n`); `:488` title; `:483` `changeReportSpec` is exported. `document-pdf.ts:179-189` footer function, `fontSize: 6.5` `:185`, margin 22 `:187`, `pageMargins [MARGIN_X,60,MARGIN_X,56]` `:197`, `MARGIN_X = 40` `:17`, comment `:248`. DOCX writes `spec.footer` into `footer1.xml` (`document-docx.ts`).
- Test file: `footer` 0, `manifest` 33 by `grep -c` (the sweep wrote 35: a re-measure difference, the kit uses 33). It already has `pdfText` `:171`, `version2` `:30` and `readPdfTextLayer` with `baseline` and page `height` (`test/support/pdf-text.ts`), which is what lets a test say "inside the page".
- PCOMP-23 read whole through the Jira API (in-process on the project `.env`, no token printed): Backlog, Medium, Bug, 0 comments; fix-shape "Footer line budget, plus a test at 250 + 200 characters"; "not seen live". Ruling `CLARIFICATIONS.md:1333` (card option a).
- Ports 9993-9994: `lsof` 0 and 0 SEAT kits hold them, word-bounded over 907 non-`.pre-` SEAT kits; control `lsof` on a python listener at 9994 printed 2, then 0. The kit needs no port.
- Model: C2 (`model-routing.md:92`), G1 (`:108`), Sonnet id `claude-sonnet-5-5` (`models_latest.json:23`).

## D-decisions (mine, in the kit)
- D1. Fix only in `change-report.ts` (clip the first footer line, never the hash line). Reason: the shared footer function is in the held file. Cost: the policy PDF keeps the defect.
- D2. Budget in characters, derived by the seat from its own probe at worst-case glyph width, one named constant. A width-based measure would need `document-pdf.ts` or font metrics.
- D3. The DOCX footer takes the same clipped string (one string feeds both); row R3 pins it keeps the hash.
- D4. Ticket is NOT closed by this PR; the policy-PDF half stays owed (written in FOR TUESDAY).
- D5. Tuesday opens the PR, gate G1 tier 1 (customer-facing output), per the sweep.

## Q-questions (each with a default)
- Q1. Is the clip marker a user-facing word? Default: no, it is three ASCII dots, a mark. Slot `ELLIPSIS dots`; `none` clips silently (misleading to a reader). If you read the dots as a new word, STOP and card it.
- Q2. Should the clip also apply to the DOCX? Default: yes (same string).
- Q3. Does the 11-02 04:42 coordinator line T6 (CARDS-0440, "one lane, both documents") stay in force for the policy-PDF half later? Default: yes, a second kit after #85 lands or releases the file.

## UNMEASURED
- That the defect reproduces at 250 + 200 (the ticket says "not seen live"); the cause (wrap past the bottom margin is a PREDICTION from the margins); the budget number; whether `npm ci` and vitest run in this seat's container route; node version for tests; R1-R6 and the plants (nothing was run: no test, build, container).
- The base suite counts; `heavy.sh` correction (copy of `B1096`'s method, not re-read here).
- Whether PR #85's file list changed since 16:50 beyond the sweep's read (I did not re-read `pulls/85/files`; the kit's REFUSE 5 does at launch).

## Outside the fences
Read-only throughout. Wrote only this report and the kit, plus scratch under `/private/tmp/claude-501/.../scratchpad/` (`j.py`, raw file copies). Read the project's `4_Credentials/.env` in-process for the three Jira values (no value printed) and the project's `.gh-config` via `GH_CONFIG_DIR`; both are read only, GET only. Made no git write verb, no `du`, no decision_queue write, no Jira write, no message; typed no `cd`. Hook advisories about case-sensitive greps fired on several of my reads; the counts I rely on (0 for footer, 33 for manifest, B1140 0 hits) have controls named above, except the case-insensitive recheck of `footer`, which I did not repeat.
