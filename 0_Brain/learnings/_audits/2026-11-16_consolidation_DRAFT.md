---
date: 2026-11-16
type: audit
status: DRAFT (measurement drafter; no lesson edited, nothing moved, nothing deleted)
window: 2026-10-19 .. 2026-11-15 (previous audit 2026-10-19_consolidation.md; this is the first consolidation since it, 28 days)
scope: Wednesday's seat (Secuura + general). `_ledger_laptop_datasec.md`, `daily_tuesday/`, `daily_friday/` and every Datasec project were NOT opened. One exception, disclosed: `git log --name-status` over `0_Brain/learnings/` lists Datasec ledger backup file NAMES (`_ledger_laptop_datasec.md.pre-*`); names only, no content read.
---

# Consolidation measurements, window 2026-10-19 .. 2026-11-15 (DRAFT)

Scratch (parse scripts, rows.json, ks2.json): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/cb1c74cc-6aba-47b1-a2ff-11511ec82c21/scratchpad/c/`.
Every number below names its instrument and frame. "Row" = a line matching `^| 2026-MM-DD` in `_ledger.md` + `_ledger_archive.md`, date taken from the row's first cell (not the archive section it sits in). Python parsed with `-I`; greps are `/usr/bin/grep` with a control where an absence is claimed.

## 0. Frame decisions (read first)

- **Window** is 10-19 .. 11-15 inclusive (28 days). The previous draft's window ended 10-18, so no row is counted twice. Rows dated 11-16 exist (boot day) and are excluded.
- **Files counted:** `_ledger.md` (70 lines, 24,928 B now, 19 rows of which 12 are window rows; the rest are 11-16) and `_ledger_archive.md` (2,797,313 B now; 348 of the 360 window rows sit there). `_ledger_friday.md` was not counted.
- **Datasec contamination check:** the archive holds sections moved from `_ledger_laptop_datasec.md`. Grouping the 360 window rows by archive section heading: **0 window rows sit in a heading containing "datasec"**; the top headings are all "Archived <date> ... Wednesday seat / rule 3c" (largest: 11-03 05:3x, 61 rows). Control: the same grouping lists the 6 Wednesday headings with 22-61 rows each, so it can see sections.
- **Row format:** `| Date | What happened | Type | w | Lesson | Status |`. The w column is the 4th cell. 6 rows have a pipe inside the first cell/prose and parse to fewer cells (3 on 10-28, 3 on 11-11); they are counted as rows (date from cell 1) but their w/Lesson cells were not parsed, so they add to the "no link" count in 1.3. Weight cell mix: **329 of 360 start `+1`**, 7 hold a bare cumulative number or a status phrase, the rest are `+N` or prose.
- **Seat attribution:** 355 of 360 rows carry `[W]` in the first 700 chars; `[W]` marks the Wednesday seat as the author, not a sub-seat, so **rows per seat below Wednesday are not attributable from the rows** (seat letters like "B 184th" are the subject of the row, not its author).

## 1. Ledger

### 1.1 Rows per day (instrument: `led.py`, both files, dates 10-19..11-15)

| date | rows | date | rows | date | rows | date | rows |
|---|---|---|---|---|---|---|---|
| 10-19 | 27 | 10-30 | 16 | 11-05 | 22 | 11-11 | 17 |
| 10-20 | 18 | 10-31 | 7 | 11-06 | 19 | 11-12 | 25 |
| 10-21 | 3 | 11-01 | 15 | 11-07 | 4 | 11-13 | 12 |
| 10-22 | 4 | 11-02 | 23 | 11-08 | 6 | 11-14 | **0** |
| 10-23 | 7 | 11-03 | 19 | 11-09 | 25 | 11-15 | 12 |
| 10-24 | **0** | 11-04 | 17 | 11-10 | 10 | | |
| 10-25 | **0** | | | | | | |
| 10-26 | 14 | | | | | | |
| 10-27 | 17 | | | | | | |
| 10-28 | 10 | | | | | | |
| 10-29 | 11 | | | | | | |

**Total: 360 rows (12 in `_ledger.md`, 348 in the archive), 12.9 rows/day over 28 days.** Peak 10-19 (27), then 11-09 and 11-12 (25 each).
**Controls for the three zero days:** 10-24 and 10-25 (Sat/Sun): `ls daily/` has no `2026-10-24.md` or `2026-10-25.md`, and `grep -c -F` of each date over both ledger files returns 0, so these are no-session days. **11-14 is NOT a no-session day**: `daily/2026-11-14.md` exists (40 lines) and says "Ledger: no Kam correction this session; no increment"; `grep -F 2026-11-14` over both ledger files = 0; the same instrument returns 12 for 11-15, so the parser sees single days. The 11-14 zero is a real quiet session, not a miss.

Per 7-day block from 10-19 (instrument: same rows; bytes = UTF-8 length of row line + newline):

| block | rows | row bytes | mean B/row |
|---|---|---|---|
| 10-19..10-25 | 59 | 57,613 | 976 |
| 10-26..11-01 | 90 | 91,691 | 1,019 |
| 11-02..11-08 | 110 | 131,579 | 1,196 |
| 11-09..11-15 | 101 | 120,802 | 1,196 |

### 1.2 Ledger bytes added

**401,685 B of row text in 360 rows over 28 days (14.3 KB/day).** Largest single row 2,212 B. Previous window (same instrument family, 10-19 draft): 255 rows / 271,758 B / 25 days = 10.2 rows/day, 10.9 KB/day. **This window is +26% on rows/day (12.9 vs 10.2) and +31% on KB/day (14.3 vs 10.9).** Mean row size grew 1,066 -> 1,116 B, and weeks 3 and 4 run at ~1,196 B/row; weekly bytes went 57.6 -> 91.7 -> 131.6 -> 120.8 KB. The 09-14 audit (697 rows / 1.41 MB in 15 days) remains the high-water mark (46.5 rows/day); this window is 28% of that row rate. Archive file growth: 2,390,794 -> 2,797,313 B (+406,519 B) over the window (file-size diff; includes archive headings, so it exceeds row bytes by ~4.8 KB).
`_ledger.md` is 24,928 B, **3.6% of the 691,468 B by-tier digest** (3.2% last time).

### 1.3 Families (instrument: `fam2.py`, first `[[link]]` in the Lesson column)

Distinct families by first link: **80** (incl. a "(none)" bucket of 8 rows with no link); distinct lessons linked at all: **79** (all 79 target files exist, `os.path.exists`). Top 12:

| # | rows | family (lesson) | first..last |
|---|---|---|---|
| 1 | 54 | 2026-08-14_i-read-representations-they-read-sources | 10-19..11-15 |
| 2 | 30 | 2026-08-04_validate-brief-pointers | 10-19..11-15 |
| 3 | 18 | 2026-09-10_i-endorse-things-i-have-not-read | 10-19..11-13 |
| 4 | 17 | 2026-08-26_mirror-reports-state-not-intent | 10-26..11-06 |
| 5 | 13 | 2026-11-01_a-note-is-its-own-message (NEW in window) | 11-02..11-15 |
| 6 | 13 | 2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour | 10-19..11-06 |
| 7 | 12 | 2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it | 10-19..11-09 |
| 8 | 10 | 2026-08-09_an-enforcement-you-must-arm-is-not-one | 10-19..11-12 |
| 9 | 10 | 2026-08-16_classification-is-the-field-that-grants-authority | 10-20..11-09 |
| 10 | 10 | 2026-09-10_surprising-measurements-are-selector-errors | 10-26..11-05 |
| 11 | 9 | 2026-09-08_a-false-absence-is-usually-my-own-instrument | 10-19..11-13 |
| 12 | 8 | 2026-10-31_never-invoke-a-write-command-to-read-what-it-would-say (NEW) | 11-09..11-13 |

(also 8 x check-the-refusal-before-the-kill, 8 x census-complete-over-a-frame.) **Top 5 = 132 of 360 rows (37%); top 10 = 187 (52%).** Last window: 48% / 63%. Families 1-3 are the same three that led last window (08-14, 09-10, 08-04); the 08-14 representations family went 46 -> 54 rows despite 4 more days. Two top-12 families are lessons filed inside the window (note-alone 13 rows in 14 days; invoke-to-read 8 in 5).

### 1.4 w>=3 / REGRESSION families and enforcement (instrument: `fam2.py` + manual read of the cited rows)

Detection: weight cell number >=3, or `w=N>=3` anywhere in the weight cell, or the word REGRESSION in the weight cell (19 rows say REGRESSION in the w cell). **The numeric-only test finds 7 rows; the extended test finds 14 families.** The `+1`-prefixed cell with the cumulative weight in prose is the dominant format (215 `+1` cells carry no `w=` at all), so every count here is a FLOOR (same limitation as 09-14 and 10-19).

| family (lesson) | rows | max w seen | enforcement named in the rows | exists? (find / ls) |
|---|---|---|---|---|
| use-the-fleets-own-tool (routing token in a subject) | 7 | **21** (10-20; also 20, 19, 18, 17 on 10-19/20; 5-6 on 11-04..06 under a different costume) | `fleet/send_brief.sh` gate; `tools/newmail.sh`, `fleet/inbox_digest.sh` for the mail-read costumes | YES all three |
| mirror-reports-state-not-intent (receipt chained to a send / composed receipt) | 9 | **12** (11-02) | `fleet/hooks/receiptguard.py`; later `note_entry.sh` ack/receipt-verb guards (`note_entry.sh.pre-1105-ackguard`, `.pre-1105-receiptverb` backups date the change) | YES `receiptguard.py`, `tools/note_entry.sh` |
| never-invoke-a-write-command-to-read-what-it-would-say (INVOKE-TO-READ) | 6 | 5 (11-13) | `fleet/hooks/pretooluse_cockpit_verb.sh` (refuses an invented cockpit.sh verb; commit aa5dc0b7b7 11-12, wired per `.claude/settings.local.json` grep count 1) is built. **The row-named mechanism for the original shape (`decision_queue.sh` refuses an `add` whose bluf is under 40 chars; override title must equal the refused attempt's title) is NOT built: `grep -c -i -E 'under 40|40 char|bluf.*(short|length)' tools/decision_queue.sh` = 0** (control: file exists, same grep with `QUESTION` hits). | hook YES; decision_queue guard **NO** |
| a-note-is-its-own-message (NOTE-ALONE) | 3 (w 3,4) | 4 (11-05) | `receiptguard.py` refusal named once; `tools/act_then_note.sh` named. **Row-named candidate (11-02): a PreToolUse hook refusing a Bash call containing both `send_brief.sh` and `note_entry.sh`: `grep -l note_entry fleet/hooks/*.sh *.py` returns only `pretooluse_no_cd.sh` and `receiptguard.py`; no such hook** (no_cd hit not read for logic) | `act_then_note.sh` named; **hook NO** |
| never-keep-the-spark-idle (quota and capability) | 2 | 4 | none; lesson RETIRED 11-15 (the Spark is gone) | n/a (dead) |
| never-blanket-markseen-mid-monitoring (MAIL-LAPSE, 11-15) | 2 (w=2 at ~17:00, **w=3 REGRESSION at 22:34**) | 3 | `tools/seat_mail_watch.sh` (built 11-15 17:01, commit 1c9d402996; a Monitor-driven poller). **It is opt-in: `grep -c seat_mail_watch` = 0 in `Launch_Wednesday.command`, `doctor.sh`, `send_brief.sh` and 20 in `tasks/NEXT-PICKUP.md` (control: the same grep finds the 20)**. Nothing arms it and nothing checks it is armed (the family of `2026-08-09_an-enforcement-you-must-arm-is-not-one`). Second candidate (launch tools refuse while a seat QUESTION is >15 min unanswered): `grep -c -i -E 'unanswered|QUESTION' fleet/brief_and_launch.sh` = 0; decision_queue.sh 4 hits (mentions, not read for logic). The 22:34 slip was a NEW costume (batch read, INDEX not), which a watcher would not have caught. | tool YES, **not armed**; refusal gate **NO** |
| a-sync-conflict-copy-is-an-input-to-every-glob (unbounded output; 11-13, w=3 REGRESSION) | 1 | 3 | candidate: a PreToolUse advisory on ls/grep/find/ps pipelines with no head/wc/-c bound; hooks dir has `pretooluse_grep_cut.sh` (a different guard: cut hiding a hit) and `pretooluse_recursive_scope.sh`; no unbounded-output advisory found (`ls fleet/hooks` read whole). | **NO** |
| an-enforcement-you-must-arm-is-not-one (stray gate tree, SHORT TMPDIR, w=3-ish) | 3 | 3 | `fleet/gate_stray_check.sh` + `fleet/tests/gate_stray_check_arms.sh` (named). Candidate (11-02): send_brief refuses a TMPDIR brief without 'SHORT': `grep -c -i -E 'SHORT|TMPDIR' fleet/send_brief.sh` = 2 (not read for logic); 11-15: a 123-char TMPDIR still broke a pre-push. | gate_stray YES; TMPDIR refusal UNVERIFIED |
| validate-brief-pointers (push route ruled without reading the pre-push hook; 10-19 w=3) | 3 | 3 | row-named OWED: a send_brief advisory (body naming push/force-push with no `pre-push:` citation warns). `grep -c 'pre-push' fleet/send_brief.sh` = 2 (counts, not read for logic) | UNVERIFIED |
| i-endorse-things-i-have-not-read (ENDORSED-UNREAD) | 1 prose row at w=3 (11-04); 18 rows total | 3 in window (21 on 10-13 per the 10-19 audit) | the 10-19 audit promoted a `send_brief.sh --kind answer` advisory (RULED + code noun, no `read <path>`). greps of fleet/send_brief.sh: RULED 13, unread 1, advis 3; **not read, so whether it is that advisory is UNMEASURED** | UNVERIFIED |
| surprising-measurements-are-selector-errors (11-05 REGRESSION), a-ruling-can-be-voided-by-removing-its-precondition (10-30), check-the-refusal-before-the-kill (11-12, 3 REGRESSION rows), a-false-absence (11-10) | 1-3 each | 3 | none named in the rows beyond `pane_close.sh` / `brief_and_launch.sh` (check-the-refusal); the 11-11 row names `wed_push.sh`: **`find` returns nothing** (control: the same find returns `friday/seat_idle.sh`) | **NO** |

**Reading, as numbers only:** 14 families reached w>=3 or REGRESSION. Of the 4 families whose row text names a mechanism as OWED/candidate, **0 have it fully built and armed**; one has the tool built and unarmed (seat_mail_watch), one a hook for a neighbouring shape (cockpit_verb). The 11-11 retro lists `wed_push.sh`, a `--help` advisory hook, a launchd watcher keepalive + doctor FAIL and a morning-card check as OWED; none located (`ls fleet/hooks | grep -c -i help` = 0; `grep -c -i 'seat_mail_watch\|newmail' doctor.sh` = 0). **Whether a gate that refuses at zero cost is "working" or "the lesson never lands" is the looping-vs-working question Kam ruled is decided by outcome. Not a verdict.**

### 1.5 Families flagged for an open candidate/OWED mechanism (instrument: `grep -E 'OWED|candidate|CANDIDATE|not built|unbuilt'` over the row text of window rows; 61 of 360 rows, 17%)

| family | what the rows say is owed | built? |
|---|---|---|
| MAIL-LAPSE (never-blanket-markseen / a-promise-is-not-a-mechanism, 11-15) | newmail/seat-mail watcher armed per session; launch tools refuse while a seat QUESTION is >15 min unanswered | watcher built, **unarmed anywhere**; refusal NOT built (see 1.4) |
| NOTE-ALONE (a-note-is-its-own-message) | PreToolUse refusal of a Bash call containing both send_brief.sh and note_entry.sh | NOT built |
| INVOKE-TO-READ (never-invoke-a-write-command...) | decision_queue refuses a stub `add` and an override whose title differs from the refused attempt | cockpit_verb hook built (neighbour); decision_queue guard NOT built |
| ENDORSED-UNREAD / stamp-without-reading-cells | send_brief advisory on a ruling naming code with no read clause | UNVERIFIED (1.4). **No row in the window names a "stamp-without-reading-cells" family**: a regex over w+Lesson cells for `stamp-without|without reading cells|unread cells` = 0 rows (control: the same instrument returns 18 for `endors`). Rows mentioning "stamp" in the body: 52 (stamping briefs is routine, not a family label) |
| representations family (11-06 retro) | "consolidation should look at whether it needs a mechanism for commissions (quote the ruled pattern's code lines)" | no mechanism; 54 rows this window |
| script candidate `fleet/verify_pr_head.sh` (10-30 retro) | verify-at-source-then-GO script | `find` returns none (control as above) |

### 1.6 What this instrument cannot see

- 329 of 360 rows start `+1`: cumulative weights live in prose; every w>=3 figure is a floor. The loose bound from the previous draft (a regex for `w ?= ?N` anywhere in the row) was not re-run here.
- First-link family counting undercounts rows with two links and puts the 8 no-link rows (6 malformed) in one bucket.
- "Enforcement exists" is file existence (`find`/`ls`/`grep -c`), not "it fires". I did not run any hook arms.

## 2. Lessons (instrument: `git -C /Volumes/DevMASTER/WEDNESDAY log --since='2026-10-19 00:00' --until='2026-11-16 04:30' --name-status -- 0_Brain/learnings/`, 1,690 output lines, read-only)

- **Created in window (A, dated lesson files): 28, 85,101 B total.** Status: **27 `live`, 1 `retired`** (`2026-10-28_never-keep-the-spark-idle-quota-and-capability-data`, retired 11-15). Last window: 40 files / 111,713 B. The other 19 `A` paths are non-lessons (Datasec ledger backups, 2 audit files).
- **Modified in window (M, existing before): 18 lessons** (list in scratch `mod.txt`): `2026-09-07_an-instruction-to-wait-must-name-what-wakes`, `2026-09-08_a-false-absence-is-usually-my-own-instrument`, `2026-09-10_a-single-file-bind-mount-binds-the-inode`, `2026-09-13_as-many-agents-as-possible-partitioned-by-code`, `2026-09-20_ks1175-hold-lifted-make-the-fix`, `2026-09-24_decisions-go-on-the-fleet-activity-panel`, the four 10-19 headline fixes (`10-06_past-70pct`, `10-06_use-to-100pct`, `10-08_use-to-100pct`, `10-09_spark-ornith-sonnet-only`), `2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle`, `2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark`, `2026-10-22_tuesday-sonnet-default-usage-is-a-guide`, `2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice`, `2026-10-28_never-keep-the-spark-idle...`, `2026-10-31_never-invoke-a-write-command...`, `2026-11-06_clear-the-secuura-board-over-one-to-two-weeks`, `2026-11-12_spark-for-harness-and-token-heavy-simple-tasks`. **0 deletions (D), 0 renames.**
- Corpus now: **272 dated `20*.md` lesson files, 1,161,062 B** (`ls | grep -c '^20.*\.md$'`; `cat | wc -c`). Last audit: 244 / 1,064,978 B. **+28 files, +96 KB in 28 days.**
- **Kind of the 28 (my reading of filenames, not a measurement):** about 24 Kam grants/rulings; about 4 corrections of Wednesday (`never-invoke-a-write-command...`, `a-note-is-its-own-message`, `one-api-outage-idles-every-mid-turn-seat-sweep-all-panes`, `a-seat-scoped-hook-in-the-shared-template-binds-every-seat`).

### 2.1 Live lessons whose headline states a dead rule (candidates only; nothing edited)

Instrument: loop over `learnings/20*.md`, H1 = first `# ` line, status = first `status:` line; headline matches `spark|ornith`; AND status `live`; AND `head -20` carries none of `spark is gone|retired|HISTORICAL|2026-11-15`. Per `2026-11-15_the-spark-is-gone-checks-retired-no-local-spark-tier.md` (its "How to apply" item 1: "a Spark-first / Spark-max / Spark-target line in any older lesson... is historical"), these are **dead-rule headlines with `status: live` and no marker in the first 20 lines (marker count 0 for all 16)**:

1. `2026-09-23_spark-kit-running-a-local-coding-model` ("The Spark is FRIDAY'S to run")
2. `2026-09-23_use-the-local-model-as-much-as-possible` ("Route tasks and tickets to the LOCAL model (the Spark) first")
3. `2026-09-25_spark-calibrate-like-ornith-start-high-oversight`
4. `2026-09-25_three-tier-routing-ornith-spark-cloud-always-on` (the lesson itself says "its Spark tier is gone" in the family line; the headline does not)
5. `2026-10-04_as-much-secuura-work-as-possible-spark-and-claude` ("Do as much Secuura work as possible with the Spark AND Claude agents (standing until Kam changes it)")
6. `2026-10-05_spark-target-50-tasks-a-day`
7. `2026-10-08_ornith-15-replaces-10-push-it-harder` (headline "run it AND the Spark as much as possible"; the Ornith half is alive, the Spark half is dead)
8. `2026-10-08_sonnet-trials-and-a-shared-model-routing-definition` ("against the Spark and Opus")
9. `2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis`
10. `2026-10-10_today-mainly-spark-and-sonnet-double-check-everything` (also date-scoped to 10-10)
11. `2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark`
12. `2026-10-18_new-account-tickets-backlog-routing-definition-spark-max` ("give the Spark as many tickets as it can handle")
13. `2026-10-22_tuesday-sonnet-default-usage-is-a-guide` (Datasec seat; headline says "no Spark, no Ornith on this seat", so it is not dead, only names the tier; listed because it matched, not because it states a dead rule)
14. `2026-10-22_usage-is-a-guide-outcomes-over-rules-route-by-learnings` ("lean on Sonnet and the Spark past 70%")
15. `2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice` ("move QA validation, review and test to the Spark")
16. `2026-11-12_spark-for-harness-and-token-heavy-simple-tasks` (four days old; the 11-15 lesson itself names it "historical")

The same loop matched 22 live files in all (the other 6 are `ornith-*` lessons and the 11-15 retirement lesson itself, which are not Spark-routing rules; the 09-14 90%-stop lesson was not among the 16 I checked). **Of the 16 checked, 15 state or half-state a dead Spark rule (item 13 does not: it excludes the Spark).** The by-tier digest carries the headlines, so a seat reading only the digest meets 15 live-headlined routing rules for a box that is no longer there. The 10-19 audit fixed four such headlines by prefixing a SUPERSEDED line and keeping the original verbatim beneath; the same delta is the candidate here. The 11-15 lesson retired `2026-10-28_never-keep-the-spark-idle...` (status retired) but did not mark these 14.
Instrument limit: the loop matches the headline only; a lesson whose H1 does not name Spark/Ornith but whose body routes to it is not found (e.g. the 09-14 90%-stop lesson body was not read).

### 2.2 Expired or end-evented grants still `status: live` (candidates)

Instrument: `tasks/EXPIRING-GRANTS.md` rows with an EXPIRED/DEAD marker, matched by hand to lesson filenames in the window.
- `2026-11-06_clear-the-secuura-board-over-one-to-two-weeks`: the EXPIRING-GRANTS row is live (1-2 weeks from 11-06, i.e. 11-13..11-20); not yet expired. Date-bound; becomes dead on or about 11-20. Flag for the next consolidation.
- `2026-10-18_new-account-tickets-backlog...-spark-max`: the grant is tied to the 10-18 account; EXPIRING-GRANTS lists the 10-18 renewal rows as EXPIRED 10-18, and the Spark half is dead (2.1 item 12).
- `2026-10-10_today-mainly-spark-and-sonnet...`: scoped to "today" (10-10), still `live`.
- `2026-10-26_spark-gate-pilot...` (a conditional grant, "if it works"): the pilot subject (Spark) was returned 11-15.

### 2.3 Candidate merges (read the H1 only; nothing merged)

1. **Three 11-11 NAS lessons:** `nas-dev-working-dated-offload` ("Backups and offloads go to the DEV-Working NAS, in a dated, named folder"), `wednesday-offloads-to-dev-working-nas` ("...dated folders under Secuura/Wednesday or General/Wednesday, through the tool only"), `wednesday-lives-on-the-mac-mini` (the always-on seat). The first two are one rule at two scopes; candidate: one lesson with a Wednesday paragraph.
2. **Two 10-22 usage lessons:** `tuesday-sonnet-default-usage-is-a-guide` and `usage-is-a-guide-outcomes-over-rules-route-by-learnings`: the same "usage is a guide, never a stop" sentence in two headlines; one is Datasec-seat, one general.
3. **Two 10-23 Kam-items lessons:** `kam-items-on-fleet-activity-morning-card-48h-email` and `tuesday-never-wait-on-kam-cards-morning-card-48h-email-priorities`: the same morning-card/48-hour rule, one scoped to Tuesday.
4. **Never-wait cluster:** `2026-10-24_every-boot-works-the-actionable-tickets-unprompted`, `2026-11-10_never-wait-a-green-item-ships-and-every-wait-watches-the-board`, `2026-10-30_wednesday-go-counts-as-kams-word-for-starting-work`, `2026-10-27_design-changes-inside-a-ruling-are-mine`: four grants about not waiting on Kam; separate scopes, flagged because they are read together.
5. **Merge rules:** `2026-11-13_premerge-do-not-merge-sentence-dropped-nine-released` is an instance of `2026-11-15_recent-merge-rules-override-historic-holds`.
6. Cross-link only: `2026-10-31_never-invoke-a-write-command...` and `2026-08-26_mirror-reports-state-not-intent` (both: my own receipt/tool output read as something it is not; different mechanisms).
No merge is recommended against Kam's 2026-08-10 ruling (no reduction without evidence it loses nothing); these are listed for his call.

## 3. STANDING KPI 1-4 (Secuura board, KS; Linear read-only under the 2026-08-03 tracker grant)

**Instrument and provenance.** Key read in-process from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` (variable `LINEAR_API_KEY`, never printed; the env file named exactly, no search). Totals come from `fleet/board_count.sh linear` per partition; the title predicate and the closed/created/outcome/duplication figures come from a python fetch of all 2,215 KS issues (including archived, with createdAt/completedAt/canceledAt/description) in `ks2.json`. **Reconciliation (the two instruments agree):** board_count per state (archived excluded by default): Backlog 497 (a single query refuses "MORE PAGES EXIST", so it is a createdAt partition: <06-01 2 + 06-01..08-31 24 + September 118 + October 185 + November 168 = 497), In Progress 229, Todo 35, In Review 6, Blocked 3 = **770**; python live (archivedAt null) with state type backlog/unstarted/started = **770**, state-by-state identical. Controls: `title eqIgnoreCase "zzqqxx"` -> the script refused an unvalidated zero (no control attested); `In Test` and `Tested Not Deployed` returned 0 and were reported only with the attestation "Todo state (same field state.name) -> 35" (`TOTAL=0 (UNVALIDATED-ZERO discharged by control...)`). The `zzqqxx` zero was NOT discharged separately in this run, so I make no "zero tickets contain X" claim from it; the closed-state counts (In Test 0, Tested Not Deployed 0 in board_count) compare to the python fetch's `Tested Not Deployed` = 6 including archived, so those 6 are all archived.
**"Open" predicate:** state type in {backlog, unstarted, started} and not archived (same definition as 09-14: active 108 + backlog 272 = 380). Done / Deployed to UAT / Deployed To Prod / Tested Not Deployed / Canceled / Duplicate are closed.

### KPI 1. The split (title predicate, boundary stated)

Predicate (the 09-14 one, fixed): `\b(guard|gate|harness|preflight|hook|red-proof|red proof|census|lint|ci)s?\b`, case-insensitive, over the title only.

| set | n | instrument-subject by word predicate | share |
|---|---|---|---|
| **open (all)** | **770** | **204** | **26.5%** |
| active (In Progress 229 + Todo 35 + In Review 6 + Blocked 3 = 273) | 273 | 84 | 30.8% |
| backlog | 497 | 120 | 24.1% |

**The boundary:** the substring form (`containsIgnoreCase` of the same words, no `ci`) gives **276 (35.8%)**; adding bare "ci" gives 325 (42.2%). **The class is 204-276 depending on the boundary** (09-14: 98-128). 77 open titles hit a term only inside a longer word (`delegatedFrom`, `eslint` is not one, `investigate`, `aggregate`, `webhook`, `gateway`). The "product" side is the complement (770 - 204 = **566**) by negation of a title word, not a count of product defects; no field on the board carries that. A title-or-description form was not computed (09-14 called it not a subject predicate).

### KPI 2. The trend

| date | open | instrument-subject (word) | share | instrument |
|---|---|---|---|---|
| 09-07 | 293 | 88 | 30% | human catalogue (s147), per the skill baseline |
| 09-14 | 380 | 98 | 25.8% | 09-14 audit, board_count + word predicate |
| 10-05 | 529 | not split | | Wednesday's own KS audit in `daily/2026-10-05.md` ("64 defects vs 237 tooling"), a different instrument, quoted not reproduced |
| 11-16 | **770** | **204** | **26.5%** | this draft |
| (reconstruction, same predicate, from createdAt/closed dates; archive time invisible so runs high) | 09-07 365 / 92 (25.2%) · 09-14 410 / 110 (26.8%) · 10-19 735 / 222 (30.2%) · 11-15 832 / 219 (26.3%) | | | `kpi.py` |

**Reading, numbers only:** the ratio is flat against 09-14 (25.8% -> 26.5%, +0.7 pt). Open total is up **+390 since 09-14** (380 -> 770; +241 since the 10-05 figure of 529); instrument-titled up +106 (98 -> 204), non-instrument-titled up +284 (282 -> 566). The reconstruction shows the ratio peaked near 30% at 10-19 and fell to ~26% by 11-15, while the open total kept rising: 735 -> 832 in the reconstruction (+97 in 27 days) and 770 now. **Window flows (python, KS, createdAt/closedAt in 10-19..11-15):** 589 tickets created (144 instrument-titled, 24.4%), **440 closed** (Done 431, Canceled 7, Duplicate 2), of which **132 instrument-titled (30.0%)**. Net open change over the window by the reconstruction: +97 (735 -> 832, includes archived-open). Per the skill, "ratio rising with no fall in product defects" is the looping signal; the ratio did not rise against 09-14, and whether product defects fell is not measurable from titles. Not a verdict.

### KPI 3. The outcome test (instrument-titled tickets CLOSED in the window; did they later catch a real product defect?)

Closed in window with the word predicate: **132** (substring form 175). Proxy only, same as 09-14: for each, the later tickets (createdAt on/after its close date) whose TITLE or DESCRIPTION contains its identifier as a word:
- **44 of 132** are named by at least one later ticket; **31 of 132** by at least one later ticket whose title is not instrument-worded; later-naming tickets total 92: **51 non-instrument-titled / 41 instrument-titled**.
- Examples ranked by later non-instrument tickets: KS-1628 (Gate I1 follow-ups; 7 later, 5 non-instrument), KS-1746 (preflight.sh:722 filter; 7 / 3), KS-1643 (Gate S1 residue; 6 / 3), KS-1621 (Gate E2 follow-ups; 4 / 3), KS-1620 (Gate D follow-ups; 3 / 3), KS-1558 (gate follow-ups; 5 / 3).
- **09-14 comparison (not the same frame):** 55 closed in 15 days, 46 named by a later ticket, 32 by a non-instrument one. This window is 132 closed in 28 days, 44 / 31. The named-by-later fraction fell from 84% to 33%; the denominator frame differs (descriptions now included, the window is longer), so this is directional only.
- **A proxy, not the answer.** "Did it catch a real defect" is Wednesday's read of those titles. Note the top rows are gate FOLLOW-UP tickets: a gate that produces follow-up tickets is counted here as instrument-titled, so the proxy credits a gate for the work it itself generated; this predicate cannot separate "the gate caught a product defect" from "the gate's own residue".

### KPI 4. Duplication rate

Two instruments, because the 09-14 one does not survive the board doubling:
1. **09-14 instrument re-run (>=4 shared significant title words or a shared file path):** now **986 pairs, 478 of 770 tickets in at least one pair (62%)**; strong pairs (>=6 words or same path) 111 pairs, 125 tickets, 39 clusters (largest 18, 10, 9, 5). **The same instrument over the reconstructed 09-14 open set** (410 tickets): 135 pairs, 137 tickets (33%), strong 30 pairs / 34 tickets / 14 clusters. So by this instrument the share roughly doubled (33% -> 62%).
2. **But the largest strong clusters are topic families, not duplicates** (I read the top four: 18 titles about documents/analytics routes; 10 mixed gate-follow-up titles; 9 api-gateway degraded-mode; 5 auth-login catch/log): long titles share vocabulary. **The 62% is an upper bound driven by title length and the board's concentration on one codebase.** 
3. **Near-identical titles (Jaccard of significant-word sets >=0.5): 1 pair, 2 tickets of 770** now; 2 pairs, 4 tickets of 410 at 09-14. At >=0.6 and above: 0 now, 0 then (control: the 0.5 run does return pairs, so the code finds them). **By the strict instrument duplication did not rise; by the loose one it doubled; which is the real duplicate rate needs a human read of descriptions, not done.** Per the skill, "duplication is the cheapest looping signal" depends on the predicate; I do not choose one.

## 4. KPI 5: Wednesday's own volume vs rows later cited

- **Volume:** 360 rows / 401,685 B in 28 days (12.9 rows/day, 14.3 KB/day) vs 255 / 271,758 B in 25 days last window (+26% rows/day, +31% KB/day). 28 new lessons / 85,101 B (last window 40 / 111,713 B), by-tier digest +70,896 B (620,572 -> 691,468; section 5). Rows per seat below Wednesday: not attributable (355 of 360 carry `[W]` as author).
- **Retrieval, proxy only (nothing records that a row was read):**
  1. Lessons linked by window rows: **79**. Named by short stem in a daily note dated on/after the lesson's first window row: **17 of 79** (by full filename: **9 of 79**). Last window: 9 of 63. Weak by construction (daily notes rarely cite a stem).
  2. Lessons whose stem appears in the body of a LATER window ledger row: **54 of 79** (68%; last window 37 of 63, 59%).
  3. Rows whose first lesson link was already linked by an earlier row in the window (known lesson, repeated): **273 of 352 rows with a link (78%)**; last window 81%. This measures that the lesson existed and the repeat happened, not whether it was read.
  4. By load rule (not a measurement of reading): `_ledger.md` is read whole at every boot (it is 24,928 B now, 12 of 360 window rows, 3.3%); archive rows (348 of 360) are read on demand only.
  5. Rows with explicit retrieval wording (`lesson fired|read at boot|retriev`): **3 of 360**.
- Reading, as numbers only: ledger volume per day rose a quarter above last window; 78% of rows repeat a lesson already linked earlier in the same window; top-5 concentration fell to 37%; two lessons filed in the window (note-alone, invoke-to-read) are already top-12 families. 11-11..11-15 retro notes carry five OWED mechanisms none of which `find`/`grep` locates (1.4).

## 5. Boot cost

### 5.1 By-tier digest size at each Sunday (instrument: `git -C /Volumes/DevMASTER/WEDNESDAY log -1 --before="<day> 23:59:59" --format=%h -- 0_Brain/learnings/_boot_digest_by_tier.md`, then `git show <sha>:<path> | wc -c`)

| as of | sha | bytes | delta |
|---|---|---|---|
| Sun 2026-10-18 (previous baseline) | 53966eb5d4 | 620,572 | |
| **Sun 2026-10-25** | 57d21cc35f | 642,959 | +22,387 |
| **Sun 2026-11-01** | 96feb8b061 | 664,337 | +21,378 |
| **Sun 2026-11-08** | 54af8021c6 | 668,192 | +3,855 |
| **Sun 2026-11-15** | f116926448 | 691,468 | +23,276 |
| working tree 2026-11-16 | | 691,468 | (`wc -c`) |

**+70,896 B (+11.4%) over the window** (last window +17.0% / +90,307 B). The bare `_boot_digest.md` is 696,950 B (was 626,441). The by-tier file was regenerated **489 times** in the window by `git log` count (291 last window); each regeneration is a commit. The week to 11-08 grew only +3.9 KB (cause not isolated). **The digest is still ~11.6x `_ledger.md`.**

### 5.2 Statusline after the brain load (instrument: regexp over `daily/2026-10-19..11-16.md`, `ctx[: ]NN%` near "after the load/digest/brain load/boot"; written by seats in prose; the regex misses days that word it differently)

- **10-19..10-23:** 33, 33, 38, 26, 38, 40, 39, 35 (n=8), range 26-40%.
- **10-26..10-30:** 33, 38, 37, 42, 35, 42, 45, 49, 41, 42 (n=10), range 33-49%.
- **11-01..11-08:** 18 (a "partial load"), 43, 39, 22, 13, 46, 44, 44, 41, 41, 39, 44 (n=12), range 13-46%.
- **11-09..11-16:** 46, 41, 44, 43, 26, 43, 35, 26, 52, 36, 36, 39 (11-11 "7% -> 39% after the brain load"), 24 (11-16) (n=13), range 24-52%.
- **Reading:** last window the band was 21-42%; this window it is 33-52% in the weeks that were not partial/lean loads. **The upper edge rose ~10 points (42 -> 52) while the digest grew 11.4%.** The 80-90% rotation band still stands far above it; retro lines on 10-19, 11-05, 11-06 and 11-09 show seats rotating at 77-82% ctx, so boot cost is still not what decides rotation, but boots now start at 40-50% instead of 30-40%. Missing: 10-27, 10-31, 11-04, 11-07, 11-08, 11-13, 11-14 gave no match by this regex (UNMEASURED for those days, not "no load"; the regex could not fire, since the same regex fires on adjacent days). Caveat: prose, not the statusline log; some lines hold two figures (before -> after) and I took the figure the regex bound to the load phrase.

## 6. Drive hygiene (policy `1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md`; template `0_Brain/reference/2026-10-05_dev-drive-survey/SURVEY.md`; read-only: df + du, no move)

- **Weekly survey cadence:** `ls 0_Brain/reference | grep -i survey` = `2026-10-05_dev-drive-survey`, `2026-10-19_dev-drive-survey` (the 10-19 re-run, in the window) and nothing later; `daily/` hits for survey/hygiene/NAS words are 10-19 (11), 10-20, 10-29, 11-03, 11-04, 11-08, 11-09, 11-11 (control: 10-05 returns 3). **No survey on 10-26, 11-02 or 11-09**; storage work in between was `storage_dryrun_secuura.sh` (dry-runs 10-19, 11-04) and NAS offload scripts (`archive_gate_clones_20261103*.sh`, `..._20261108_nas.sh`, `archive_spark_work_20261109_nas.sh`). `doctor.sh` has no drive-survey cadence check (not grepped beyond the 85% trigger text).
- **df (2026-11-16, read-only):** `/Volumes/DevMASTER` is now a NEW drive (the 11-11 swap): **3.6 TiB, 1.6 TiB used, 2.0 TiB free, 46%**, 75 M inodes (was 1.8 TiB, 91% on 10-19). `/Volumes/DEV-Working` (NAS, SMB): 11 TiB, 66 GiB used, 1%. `/Volumes/G-DRIVE` (the policy's destination) is **not mounted** (`ls /Volumes/G-DRIVE` fails); the 11-11 NAS lessons name DEV-Working as the destination. The 85% trigger is not met.
- **du -sk (GiB; Wednesday's scope + general; 420 s cap per path):** `WEDNESDAY/2_Project_Files/tools` **202.1** of which `tools/omlx` **200.7** (`omlx/models` 198.2: Qwen3.8-Flash-Next 99.0, Qwen3.5-122B 64.8, Ornith-1.5-35B 34.3; models last written 10-08; `omlx/cache` 0.2); `WEDNESDAY/2_Project_Files/local-model` **430.9** (of which `spark-ab` 146.9, `runs` 20.7, `omlx` 2.0, `hosted` 0.64, `night` 0.09; **~260 GiB by subtraction, `local-model/spark` not measured separately inside its timeout**); `2_Project_Files/fleet` 15.9; `5_Project_History` 7.5; `0_Brain/learnings` 0.03, `daily` 0.02; `0_Brain/reference` **TIMEOUT at 420 s (UNMEASURED)**; `!CODING/Secuura/Blockchain/worktrees` **264.3**, `deploy-clones` 37.1; `!CODING/Testing Agent MAIN` 25.2; `SYSTEM` 131.8; `QA_AGENT` ~0. (Last time `Blockchain` total 658.9 and `Testing Agent MAIN` 294.9.)
- **Proposals, none executed:** (a) the Spark returned 11-15 and the 11-15 lesson says never run its tools: `local-model/spark-ab` (146.9) and `local-model/spark` (~260 by subtraction) are the largest Wednesday-scope classes; move through `tools/nas_offload.sh` into a dated folder (policy 11-11), after Kam names whether any run record in them is a record to keep (the Spark archive lives in `0_Brain/reference/2026-11-15_spark-return-archive`, 105 files, per the 11-15 lesson). (b) `tools/omlx/models`: Qwen3.5-122B (64.8) and Qwen3.8-Flash (99.0) have no use I can find in `doctor.sh`/NEXT-PICKUP grep (omlx mentioned once in NEXT-PICKUP; doctor names only Ornith 1.5 as the night backend); the Ornith 1.5 model stays. (c) `Blockchain/worktrees` 264.3 GiB: re-run the 10-05 class A/B classification (the 11-04 dry-run lists `deploy-clones` candidates, 5+ at 600 MB to 3.2 GB merged and clean) before moving. Move cost: node_modules dominates, regenerate rather than move (10-05 note).
- **Receipt line per drive (policy):** DevMASTER 1.6/3.6 TiB (46%), moved 0 GB, removed 0 GB (this draft), kept-and-why: not decided; DEV-Working 66 GiB/11 TiB; G-DRIVE not mounted.

## 7. Retro "Candidate new lesson" lines, 2026-10-19 .. 2026-11-15 (26 daily notes present; 10-24 and 10-25 absent)

Instrument: `/usr/bin/grep -i -c 'candidate new lesson'` per note, plus `grep -i -E 'candidates?[*:]+|mechanism candidate|enforcement candidate'` over the 26 notes (73 hits, 61 after dropping the template line); positive control: the template line (`- Candidate new lesson? (only if it changes future behaviour)`) is found in 25 of 26 notes (not 11-01, where the answer was written in place: "Candidate lesson: none new — all mapped to existing lessons; FILED as ledger rows").

- **25 notes still carry the unfilled template line** (every note 10-19..11-15 except 11-01; 10-19 carries it twice). It is template residue: the seat retros answer elsewhere in the same note in a `Candidates:` line (see below). Rule 2a in `CLAUDE.md` ("FILED or DISCARDED in the same action") is met in most retros by wording like "FILED as ledger rows / no new lesson needed".
- **Answered in place as FILED/DISCARDED (spot-checked 6):** 10-29, 11-04 (ledger rows); 11-14 (a) FILED as `2026-11-13_a-seat-scoped-hook-in-the-shared-template-binds-every-seat` (in the git added list), (b) DISCARDED; 11-09 and 11-13 "none unfiled".
- **Candidates that name a thing and have no `learnings/` file or built mechanism (checked by `find`/`ls`/`grep -c` with controls named in 1.4/1.5):**
  - 10-30 retro: `fleet/verify_pr_head.sh` (script candidate, "owed to a WED tooling seat; claim first"): no file.
  - 11-06: "consolidation should look at whether [the representations family] needs a mechanism for commissions": no mechanism, no lesson; 54 rows (1.3). Raised, not resolved.
  - 11-11 (retro, "PROMOTIONS they earned are OWED WORK, carried in NEXT-PICKUP"): `wed_push.sh` (w=3), a launchd keepalive for the watchers outside the drive plus a doctor FAIL, a `--help` advisory hook (w=3), a morning-card checkpoint check (w=2). `find` for `wed_push.sh` returns nothing; no help hook; `grep -c` of doctor.sh for `seat_mail_watch|newmail` = 0. The launchd list (`~/Library/LaunchAgents`) shows `com.wednesday.chatsync|close|dailysweep|dmlinkwatch` plists and no watcher keepalive among the first five lines I read (a bounded `head -5`, so UNMEASURED beyond that).
  - 10-31 retro / 11-01: "ALL SEATS mail 'start push drivers with a short TMPDIR'": 11-15 rows show a 123-char TMPDIR still caused a pre-push failure (R 121st, 23:22): the mail did not prevent recurrence.
  - 11-15 22:34: the mail-lapse family at w=3 REGRESSION: tool built (seat_mail_watch), unarmed, and the new failure shape (batch index unread) is not covered by it.
- Everything else I scanned reads "none unfiled" / "FILED as ledger row" / "DISCARDED: <reason>".

## 8. Items needing Kam (proposals only; each with its measurement)

1. **15 live lessons headline a Spark routing rule for a box that was returned 11-15** (2.1). Measure: loop over headlines, marker count 0 on all. Proposal: the 10-19 delta again (a SUPERSEDED line above the verbatim original) on items 1-12, 14, 15, 16 and the Spark half of 7; Wednesday's call, Kam's if he wants any kept.
2. **The weekly consolidation lapsed again by 28 days, but the doctor check fired** (the 10-19 DGM validation owed: did the check fire?). Evidence: the claim commit `6f54c3f38b` on main states "weekly consolidation 2026-11-16 (lapsed since 10-19)", and no `*_consolidation*` audit newer than 10-19 exists in `learnings/_audits/` (ls: the newest non-DRAFT is `2026-10-19_consolidation.md`). I did NOT run `doctor.sh` to see the WARN text, so "the WARN printed" is UNMEASURED; "the audit file was absent for 28 days" is measured. If the WARN printed at boots 10-27, 11-03, 11-10 and was not acted on, the mechanism caught it and no human/seat reading acted: that is a different finding than 10-19's.
3. **Five owed mechanisms, none built, three families at w>=3** (1.4/1.5): the note-alone hook, the decision_queue stub guard, `wed_push.sh`, a launcher/doctor arming of `seat_mail_watch.sh`, and a launch-tool refusal on an unanswered QUESTION. The 11-15 w=3 mail-lapse row shows the one that WAS built is not armed by any launcher/doctor line.
4. **KS board: 770 open (+390 since 09-14, +241 since 10-05), instrument share flat at 26.5% (title word), 132 instrument-titled tickets closed in the window, 31 later cited by a non-instrument ticket** (3). The ruling on what this means is his (09-07: decided by outcome). Proposal: keep the 09-14 predicate as the fixed instrument; add the substring form only as a boundary note.
5. **By-tier digest 691 KB (+11.4% in the window, +30% since 09-23's 530 KB) and boots now start at 33-52% ctx.** Measure: 5.1, 5.2. The 09-23 audit said halving needs retiring whole rules (his call); 15 dead Spark headlines are the cheapest first candidates (a SUPERSEDED headline is shorter than the live rule it replaces, though the digest carries headlines, not bodies, so the saving is small and unmeasured).
6. **Drive state:** see section 6 (the 85% trigger is no longer met on DevMASTER; the new drive is 46% used, G-DRIVE is not mounted).

## UNMEASURED (reason for each)

- **Whether any ledger row was READ by a seat:** no instrument records it (the proxies in section 4 are the closest; none is retrieval).
- **Rows per seat below Wednesday:** `[W]` marks the author only; sub-seat attribution is not in the rows.
- **True weight of the 329 `+1` rows:** cumulative weights live in prose; every w>=3 count is a floor.
- **Whether the mechanisms I marked UNVERIFIED (send_brief RULED/unread advisory; pre-push citation advisory; TMPDIR 'SHORT' refusal) are the ones the rows promise:** I counted greps (13, 1, 3 / 2 / 2) and did not read `send_brief.sh` (42,448 B) for logic. Existence of a file or grep hit is not "it fires"; no hook arms were run.
- **Whether `doctor.sh` printed "weekly consolidation LAPSED" at any boot in the window:** not run (running doctor writes state; I did not risk it); only the audit file's absence and commit `6f54c3f38b`'s wording are measured.
- **Product-defect count on the KS board:** no field carries it; titles can only say "instrument-worded or not".
- **Real duplicate rate on the KS board:** the loose instrument gives 62% (an upper bound that over-counts topic families), the strict one gives 2 tickets of 770; a human read of descriptions was not done.
- **The `zzqqxx` zero on the KS board:** the script refused it without an attested control and I did not re-run it with one; no "zero tickets match" claim is made from it.
- **Statusline after load for 10-27, 10-31, 11-04, 11-07, 11-08, 11-13, 11-14:** the regex found no value; not read by hand.
- **Full-filename citation count for the 28 new lessons:** not recomputed (last window 26 of 40).
- **The loose regex upper bound for w>=3 rows (last window: 47):** not re-run.
