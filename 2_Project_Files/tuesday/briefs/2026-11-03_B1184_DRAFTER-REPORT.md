STARTABLE: YES (after the stamp; all five slots are four underscores, defaults HOLD)

# B1184 drafter report (Sonnet, C8 row `model-routing.md:98`), 2026-11-03, clock 06:40:24 to about 06:50 AEDT

## BLUF
Seat R148 (next free R-number) records the product owner's 06:38:29 and 06:39:15 ruling on MPSCALC-359: one Jira comment and one C-entry, C-86, on `records/b1184`, fast-forwarded into root main. A wording card with three candidate sentences is drafted; nothing ships until he picks one.

Files: kit `.../briefs/2026-11-03_B1184_SEAT-R148_mps-359-ruling-records.md` (5 stamp slots: STAMP, LAUNCH WINDOW, authority and hard stop, REC-359, REC-CLAR); this report; `.../briefs/2026-11-03_MPS-359-WORDS-CARD.json` (parses; option labels are 20, 19 and 17 words; recommended a).

## Facts re-measured (instrument)
- R-number: `ls briefs | grep -E 'SEAT-R(14[89]|1[5-9][0-9])_'` printed nothing; word-boundary scan for `R148` in today's and yesterday's non-pre SEAT kits: 0 (control `MPS-R147`: 4). Newest is R147 (B1171).
- C-number: C-86. `grep -n '^### C-'` tail: C-85 at CLARIFICATIONS.md:2325; `### C-86` 0 on 60 of 60 local branches; file 2473 lines. Root main `ccf68fb3eed5ddc5ccc83f393526cc3631e5a38c` (R147 has landed; its commit touched CLARIFICATIONS.md only).
- Records mechanics, measured at source: `git ls-files --error-unmatch` prints the path, `check-ignore -v` prints nothing. So the file is tracked and R147 committed on a records branch then ff-only (`git show --stat HEAD`: 1 file, 39 insertions). The kit copies that.
- Code main re-measured: `gh api git/ref/heads/main` = `314b53f6ddaaa9005e1015479882ff35e33b631e` at 06:41:27 (unchanged). Lines (from a tarball at that sha): PurchaseCalculator.cs:338 (site refusal, code :66), :333 (check skipped for an empty list), :336 (usable-site test), :391 (quantity-rule refusal, code :63), :589 (SITE ALLOCATION DIFFERS Review issue); PurchaseInput.cs:40-47 (3 rule members); ENGINE.md:166, :169.
- perSite is not in the code: `grep -rni persite` over src, web/src, docs prints only ENGINE.md:166 and :169 (control `InvalidSiteAllocation`: 2 lines in src).
- Where a note shows: PurchaseResultView.tsx:200-206 (the Issues list under the result, not under a line); sub-line precedent under a device line PurchaseBomEditor.tsx:483-485 and PageEstimateRow.tsx:30. No editor control for a quantity rule: 0 non-test, non-generated `quantityRule` lines in web/src (control: generated copy 4).
- MPSCALC-359 live GET: Backlog, labels lane-v4, mpscalc-b1082, plan-b1082-t2, tier-1, 0 comments, updated 2026-11-02T03:32:13.870+1100.
- Pane list: no `Datasec/MPS-R` pane; MPS-M85, M86, G307 live. Ports: 0 listeners on 9900-9999.

## D-decisions
- D-1: the seat's Jira client is NARROWED to one verb (one comment on -359, MAX_WRITES 1). -359 comes out of R147's NEVER list for that comment only.
- D-2: the card id that opens the 06:38:29 message is dropped from the comment and the entry (DRAFTER_RULES fence 7); the words after the colon are quoted verbatim, the second message whole. The long dash is written `--` (Jira ASCII), said in one clause.
- D-3: one BACKLOG row, one JIRA.md section and one history entry, uncommitted as R147 did; not asked for, easy to cut.
- D-4: card option a is closest to the existing refusal style (:338) and the shortest with both cause and fix.

## Q for Tuesday
- Q-1: your brief said "quote both verbatim"; fence 7 says no card id in kit text. Default: the id is dropped (D-2). Override at the stamp if you want it kept.
- Q-2: the screen. Default in the card: the Issues list (the existing path); the sub-line under the line is the alternative. The kit settles neither.

## UNMEASURED
MPSCALC total/Done/Backlog counts; the scope of pane MPS-G307 and the branches of M85/M86; the decision store; hosted state; whether the ruling changed after 06:39:15; whether the project's Jira text scan accepts the text (the seat tests it).

## Outside-the-fences disclosure
Read-only: the briefs folder, DRAFTER_RULES, `model-routing.md` rows, `models_latest.json`, R147's kit, the MPS project's CLARIFICATIONS.md and `.tools/b1171/*.py` headers (not run); `2026-11-03_MPS-CARDS-0600.md` lines 22-60 (an earlier draft of this same card, used only for the card shape). Jira GET through a scratch reader in the session scratchpad (token read in-process, not printed). `gh api -X GET` tarball of main extracted into the scratchpad. No `decision_queue.sh`, no write in any project folder, no git write verb, no cd. A hook refused one command containing `cd`, and an advisory fired on case-sensitive greps (re-run case-insensitively where it mattered).
