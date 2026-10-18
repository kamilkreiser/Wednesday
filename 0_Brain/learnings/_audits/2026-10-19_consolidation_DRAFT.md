---
date: 2026-10-19
type: audit
status: DRAFT (measurement drafter; no lesson edited, nothing moved, nothing deleted)
window: 2026-09-24 .. 2026-10-18 (catch-up; previous audit 2026-09-23_consolidation-kam-ruling-b.md)
scope: Wednesday's seat (Secuura + general). Tuesday's ledger, daily_tuesday/ and every Datasec project were NOT opened.
---

# Consolidation measurements, catch-up 2026-09-24 .. 2026-10-18 (DRAFT)

Scratch (parse scripts, rows.json): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ff943889-d9ba-463a-a66e-300867d673bd/scratchpad/consol/`.
Every number below names its instrument and frame. "Row" = a line matching `^| 2026-MM-DD` in the ledger files, parsed by `ledger.py`/`l2.py` (python3 -I), date taken from the row's first cell (NOT the archive section it sits in).

## 0. Frame decisions (read first)

- **Files counted:** `learnings/_ledger.md` (61 lines, 19,666 B now) + `learnings/_ledger_archive.md` (1,646 lines, 2,390,794 B now). `_ledger_friday.md` was not counted (a separate seat file; no row from it enters any number here).
- **Datasec contamination check:** the archive also holds three sections moved from `_ledger_laptop_datasec.md` (headings at archive lines 1559, 1574, 1596). Those hold rows dated 2026-09-18 and earlier. Grouping window rows by archive section heading: **0 window rows sit in those three sections** (so no Tuesday rows leaked into the count, and I did not read them). Control: the same grouping found 245 window rows in Wednesday sections and 12 in `_ledger.md` top.
- **Seat attribution:** 246 of 255 window rows carry the `[W]` marker inside the first 600 chars of the "what happened" cell; the other 9 are older-format or card-style rows (e.g. three 2026-10-12 rows beginning "Carded Kam…", "Kam had to repeat…", "Kam tapped…"; five "THREE/FIVE SELF-CAUGHT SLIPS" rows without `[W]`). Both groups are in the Wednesday files, so all 255 are counted as Wednesday's. Rows per seat finer than that are not attributable from the rows.
- **Family** = the FIRST `[[lesson]]` link in the Lesson column (6 rows carry no link). Counting every link instead gives 63 distinct lessons linked; counting first links gives 65 family keys because 6 no-link rows add placeholder keys. Treat "65" as the first-link figure and "63" as the all-links figure.
- **The weight column is not clean.** It mixes `+1 (costume)`, a bare cumulative number (`16 (routing token in a subject…)`), and 3 rows that hold a status phrase instead (`correction (self-caught…)`). "w>=3" below is: the cell starts with N>=3 or +N>=3. `+1` rows whose cumulative weight lives only in the prose are NOT detectable by this instrument (see section 1.5).

## 1. Ledger

### 1.1 Rows per day (instrument: `l2.py`, both files, dates 09-24..10-18)

| date | rows | date | rows | date | rows |
|---|---|---|---|---|---|
| 09-24 | 2 | 10-01 | 8 | 10-09 | 18 |
| 09-25 | 15 | 10-02 | 1 | 10-10 | 15 |
| 09-26 | 10 | 10-03 | 1 | 10-11 | 10 |
| 09-27 | 6 | 10-04 | 12 | 10-12 | 18 |
| 09-28 | 6 | 10-05 | 28 | 10-13 | 25 |
| 09-29 | 11 | 10-06 | 14 | 10-14 | 2 |
| 09-30 | 9 | 10-07 | 16 | 10-15 | 5 |
| | | 10-08 | 11 | 10-16 | 3 |
| | | | | 10-17 | **0** |
| | | | | 10-18 | 9 |

**Total: 255 rows** (12 in `_ledger.md`, 243 in the archive). Peak day 10-05 (28), then 10-13 (25).
**Positive control for the zero on 10-17:** the same parser returns 1 row for each of 10-02 and 10-03 (so it can see single-row days); and `daily/` has no `2026-10-17.md` at all (ls of `0_Brain/daily/`), i.e. no session note exists for that day, so the zero is a no-session day, not a parser miss.
Rows dated after the window are present (3 on 10-19 in `_ledger.md`) and excluded.

Per week (instrument: same rows, bytes = UTF-8 length of the row line):

| 7-day block | rows | row bytes | mean B/row |
|---|---|---|---|
| 09-24..09-30 | 59 | 74,133 | 1,256 |
| 10-01..10-07 | 80 | 83,450 | 1,043 |
| 10-08..10-14 | 99 | 96,901 | 979 |
| 10-15..10-18 (4 days) | 17 | 17,274 | 1,016 |

### 1.2 Ledger bytes added

**271,758 B of row text in 255 rows over 25 days** (10.2 rows/day, 10.9 KB/day). Largest single row 1,933 B (09-26). Instrument: sum of `len(row_line.encode())` for window rows; it counts the rows themselves, not the file diff (the `3c` moves are verbatim, so file-diff and row-bytes agree, but the file also gained archive headings).
Frame comparison, same instrument family: the 2026-09-14 audit measured **697 rows / 1.41 MB in 15 days** (46.5 rows/day, ~94 KB/day). This window is **about one quarter of that row rate** (10.2 vs 46.5) and about **one ninth of the byte rate** (10.9 vs ~94 KB/day). Current sizes: `_ledger.md` 19,666 B (15 rows: 3 x 10-16, 9 x 10-18, 3 x 10-19), so the live ledger is **3.2% of the 620,572 B by-tier digest** (the 09-07 KPI note had it larger than the digest).
Caveat: the 09-14 figure counted 697 rows across Wednesday files in a differently-bounded window; the rate comparison is directional only.

### 1.3 Families (instrument: `l4.py`, first link per row)

Top 10 by row count:

| # | rows | family (lesson) | first..last row |
|---|---|---|---|
| 1 | 46 | 2026-08-14_i-read-representations-they-read-sources | 09-25..10-18 |
| 2 | 23 | 2026-09-10_i-endorse-things-i-have-not-read | 09-26..10-18 |
| 3 | 23 | 2026-09-08_a-false-absence-is-usually-my-own-instrument | 09-29..10-18 |
| 4 | 18 | 2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour | 09-25..10-18 |
| 5 | 13 | 2026-08-04_validate-brief-pointers | 09-25..10-16 |
| 6 | 10 | 2026-08-26_mirror-reports-state-not-intent | 10-08..10-13 |
| 7 | 8 | 2026-09-07_a-census-complete-over-a-frame-that-is-not | 09-24..10-10 |
| 8 | 7 | 2026-08-17_check-the-refusal-before-the-kill | 09-26..10-12 |
| 9 | 7 | 2026-09-11_red-proof-arms-cover-every-legitimate-shape-of-the-real-event | 09-25..10-09 |
| 10 | 6 | 2026-09-09_my-authority-and-the-targets-rules-are-two-checks | 10-04..10-09 |

(next: 5 x headline-must-match-the-operative-case, 5 x classification-is-the-field-that-grants-authority, 4 x unquoted-heredoc-executes-backticks, 4 x artifact-presence-is-not-execution.) **Top 5 families = 123 of 255 rows (48%); top 10 = 161 (63%).** Every one of the top 10 pre-dates the window (08-04 .. 09-18): the window's volume is recurrence of old lessons, not new ones. The 40 new lesson files of section 2 are almost all Kam grants/rulings, not corrections.

### 1.4 Rows with w>=3 (regressions), and whether each family has an enforcement

Instrument: `l3.py`, weight cell begins with N>=3 or +N>=3. **49 rows**. Grouped by the costume named in the weight cell; the enforcement column is "named in the row text AND file exists" (checked with `find`):

| costume (weight cell) | rows >=3 | highest w | enforcement named in rows | file exists? |
|---|---|---|---|---|
| routing token in a subject (lesson use-the-fleets-own-tool) | 14 | 16 on 10-18 (17 on 10-19, outside window) | `send_brief.sh` gate (13 of 14 rows name it; weight cell says "enforced by the gate") | YES `2_Project_Files/fleet/send_brief.sh` |
| ruling on a seat's tool/design without reading it (i-endorse-things-i-have-not-read, validate-brief-pointers, my-authority) | 18 | **21 on 10-13** | **none.** Rows name only one-off push wrappers (pushd8.sh, pushk2.sh…) as the thing being ruled on, not as a guard. `daily/2026-10-10.md` line 21 states "the owed mechanism (send_brief flags a ruling that names a tool path the sender has not opened) stays a CANDIDATE"; `learnings/2026-09-10_i-endorse-things-i-have-not-read.md` has 0 hits for it. | n/a: **NO enforcement; highest weight in the window** |
| receipt chained to a send (mirror-reports-state-not-intent) | 9 (w 3..10) | 10 on 10-13 | `receiptguard.py` (9 of 9 rows) | YES `2_Project_Files/fleet/hooks/receiptguard.py` |
| dashboard state swept by a stash (classification-is-the-field…) | 4 (w 3..5) | 5 on 10-09 | `pretooluse_no_autostash.sh`, `safe_pull.sh`, `tests/safe_pull_arms.sh`, `wed_claim.sh` | YES all four (`fleet/hooks/…`, `tools/safe_pull.sh`, `tests/safe_pull_arms.sh`, `tools/wed_claim.sh`) |
| check-the-refusal, subject-token costume | 3 (w 4..6, 09-30..10-01) | 6 on 10-01 | none named in these three rows (the same subject-token habit is the routing-token row family, gated by send_brief.sh) | n/a |
| instrument slips / inbox read through a frame (a-false-absence…) | 4 (w 3,5,+3,+3) | 5 on 10-13 | `newmail.sh` named in 2 of 5 rows (seen-id mail reader with FAILED-on-zero refusal, built 10-13) | YES `2_Project_Files/tools/newmail.sh`; the other slip classes (zsh/rc/f-string) have only the generic hooks `pretooluse_no_cd.sh` + `pretooluse_zsh_wordsplit.sh` which exist but are not named by those rows |
| brief contradicts the project's boot-pull rule (my-authority…) | 1 (w 3, 10-09) | 3 | none named | n/a |

**Reading, as numbers only:** 2 of the 7 costume groups (routing token, receipt chain) have a named, existing, per-row-cited gate and their weight is still climbing (16 and 10), i.e. the gate catches the instance but the habit that triggers it does not fall; 1 group has no enforcement at all and carries the window's highest weight (21). Whether a gate that fires 17 times is "working" (it refuses at zero cost) or "the lesson never lands" is the same looping-vs-working question Kam ruled is decided by outcome (skill KPI). Not a verdict.

### 1.5 What this instrument cannot see

- 124 of 255 window rows have a weight cell starting `+1`, where the cumulative weight is only in prose (sometimes "w=N" in the text); w>=3 above is therefore a FLOOR. A loose regex `w ?= ?(3-9|NN)` over the whole row text matches 47 rows (it also catches rows quoting other w values), a rough upper bound on how many rows mention a weight >=3 in prose, not reconciled row by row.
- First-link family counting undercounts rows with two links.

## 2. Lessons (instrument: `git -C /Volumes/DevMASTER/WEDNESDAY log --since='2026-09-24 00:00' --until='2026-10-19 23:59' --name-status -- 0_Brain/learnings/`, 2,408 output lines; read-only)

- **Created in window (status A in git, dated-lesson files `20*.md`): 40**, total 111,713 B. Status frontmatter: **39 `live`, 1 `superseded in its MODEL half`** (`2026-10-09_spark-ornith-sonnet-only-until-monday`).
- **Modified in window (M, existing before): 6 lessons:** `2026-08-06_ghost-suggestions-in-panes` (22,271 B, the largest single lesson), `2026-08-26_a-sync-that-cannot-refuse-a-deletion`, `2026-08-29_unquoted-heredoc-executes-backticks`, `2026-09-07_read-the-clock-at-boot`, `2026-09-18_ornith-works-constantly-standing-rule`, `2026-09-23_spark-kit-running-a-local-coding-model`. All `live`.
- Other files touched but not lessons: `_boot_digest(.md|_by_tier.md)`, `_ledger.md`, `_ledger_archive.md`, `_ledger_friday.md`, `_ledger_laptop_datasec*.md` (Tuesday's, listed by git only, not opened), plus `.pre-*` backups and three `conflict_on_2026-09-22` copies added in the window. **0 deletions.**
- Corpus now: 244 dated lesson files, 1,064,978 B source (instrument: `ls 20*.md | wc -l`, `cat | wc -c`). The 09-23 audit ended at 199 blocks / 924,927 B, so **+45 files / +140 KB in 26 days**.
- **Kind of the 40 new files (my reading of filenames/headlines, a classification not a measurement):** the large majority are Kam grants/rulings about usage allowance and model routing (spark/ornith/sonnet/100pct/80-90pct/push-to-demo/storage). Few are behavioural corrections of Wednesday (e.g. `a-rotate-run-inside-its-own-pane-kills-itself`, `an-agent-parked-on-its-own-question-dialog-cannot-read-mail`, `a-sync-is-not-done-until-every-folder-is-counted-on-both-sides`, `a-correction-to-a-client-is-a-new-claim-gate-it-like-code`).

### 2.1 Live lessons whose headlines may contradict (candidates only; nothing edited)

1. **Weekly-allowance thresholds, five headlines, three different numbers:** `2026-10-06_past-70pct-spark-takes-80pct-of-tasks` ("Past 70%… the Spark takes 80%") vs `2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark` ("From 80% to 90% cloud agents are LIMITED… above 90% the hard stop stands") vs `2026-10-06_use-to-100pct-spark-all-tickets-one-or-two-deployers` and `2026-10-08_use-to-100pct-raise-gate-merge-seats-only` ("may spend to 100%") vs `2026-10-01_friday-cloud-threshold-90` ("70% to 90%"). Each is scoped (seat / until-renewal) but all are `status: live`, and `tasks/EXPIRING-GRANTS.md` records the 70% row as "PREMISE ENDED 2026-10-07", the 10-06 and 10-08 100% grants as EXPIRED (2026-10-07 and 2026-10-09 respectively, allowance renewals), and the 10-15 Spark-only row EXPIRED 2026-10-18. A seat reading only the digest meets live-headlined grants that are dead.
2. **Model for new agents:** `2026-10-09_spark-ornith-sonnet-only-until-monday` (H1: "no new Opus seats, gates or drafters", frontmatter says superseded in its model half ~15 minutes later, with Opus 5.5 for all) vs `2026-10-10_today-mainly-spark-and-sonnet-double-check-everything` (default seats to Sonnet) vs `2026-10-08_sonnet-trials-and-a-shared-model-routing-definition` (extension 10-09 23:12 resumes Sonnet trials) vs `2026-10-18_model-routing-v10-approved-route-by-the-table` ("Opus 5.5 for every agent override is lifted"). Four live headlines name four model defaults; the last is the in-force one.
3. **Spark volume:** `2026-10-05_spark-target-50-tasks-a-day` vs `2026-10-18_new-account-tickets-backlog-routing-definition-spark-max` ("as many as it can handle") and `2026-10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis`. Compatible in spirit, different units (a number vs "as many as").
4. **Push without a card:** `2026-10-05_october-deploy-both-boxes-when-ready` / `2026-10-06_push-to-demo-when-ready-no-card` (Friday/Datasec scope) vs `2026-10-16_tuesday-inherits-push-to-demo…`; scope differs by seat, flagged only because one workspace brain serves both.
5. **Storage:** `2026-09-29_regenerable-build-leftovers-are-not-kept` vs `2026-10-07_archive-bulky-leftovers-to-g-drive-clear-after-a-month` vs `2026-10-15_storage-policy-for-old-blockchain-files-and-tests-monday` (keep vs archive vs clear-after-a-month).

### 2.2 Superseded/narrowed headlines whose headline was not updated

- **`2026-10-09_spark-ornith-sonnet-only-until-monday`: HEADLINE STATES THE DEAD RULE** ("no new Opus seats, gates or drafters"). Frontmatter `status:` and a top block say the model half was superseded ~09:4x the same morning, but the H1 and "operative case" paragraph still say Sonnet-only. This is the same hazard class as the 09-23 audit's finding on the rotation-band file.
- `2026-10-08_sonnet-trials-and-a-shared-model-routing-definition`: carries an "EXTENSION 2026-10-09 23:12:40" section; H1 unchanged and still compatible, but the routing question was settled by v1.0 on 10-18 (see 2.1 item 2).
- Grants whose end event happened but whose lesson file still says `status: live` and whose headline is written as active: `2026-10-06_past-70pct…`, `2026-10-06_use-to-100pct…`, `2026-10-08_use-to-100pct…` (expiry recorded in `tasks/EXPIRING-GRANTS.md`, not in the lesson).
- Checked and OK: `2026-09-29_datasec-github-commits-go-through-codeql` carries a "NARROWED 2026-09-29 13:3x" paragraph but its H1 already has the narrowed wording ("a commit reaches main only after CodeQL has scanned THAT commit on a PR"), so no stale headline.
- Instrument for this section: `grep -i -E '(SUPERSEDED|AMENDED|NARROWED|REFINED|CORRECTED|EXPIRED|ENDED|OVERRULED|LIFTED)'` at line start over the 46 touched dated files, plus manual reads of headlines; 3 files hit besides ghost-suggestions (an older file whose "timeline corrected" is body-only). A line-start grep misses a mid-line marker; this list is a floor.

## 3. STANDING KPI 1-5

### KPI 1-4 (Secuura board split, trend, outcome test, duplication): **UNMEASURED**

Why: `fleet/board_count.sh linear <KEY_ENV_VAR> '<filter>'` reads whatever Linear key the named env var holds. Wednesday's `4_Credentials/.env` defines only `LINEAR_API_KEY/TEAM_ID/TEAM_KEY/WORKSPACE` (plus AgentMail, MSGraph, one Secuura Google-Calendar ICS URL, TRMNL, Kintsugi QA creds); **no Secuura/KS Linear key**. A read-only `teams { nodes { key name } }` query with the one key it holds returned exactly `[{"key":"WED","name":"Wednesday"}]`, so the KS board is not visible to any key Wednesday's tools read. The 09-14 audit's KS counts (380 open, 98 instrument-subject) cannot be extended or compared from here. No KS ticket count, instrument predicate, closed-instrument-ticket outcome, or duplicate-cluster figure is stated in this draft. Positive control for the "not visible" claim: the same query against the same key does return the WED team, so the call worked.
To measure: someone who holds the Secuura Linear key (the Secuura seat, or Kam) runs `board_count.sh linear <ENV_VAR> …` with the 09-14 predicate (title regex `\b(guard|gate|harness|preflight|hook|red-proof|red proof|census|lint|ci)s?\b`, case-insensitive) and the `zzqqxx` zero control.
Context only, NOT a KPI measurement: `daily/2026-10-05.md` (15:25 retro) records Wednesday's own KS audit for Kam on 10-05, "529 open; 64 defects vs 237 tooling". That is a quoted note, produced by a different instrument at a different date; I did not reproduce it.

### KPI 5: Wednesday's own volume vs rows later seats retrieved

- **Volume:** 255 rows / 271,758 B in 25 days, 40 new lesson files / 111,713 B, by-tier digest +90,307 B (530,265 -> 620,572; section 4). Rows per seat: not attributable beyond the `[W]` tag (246 of 255).
- **Retrieval, proxy only (no instrument records that a row was read, as the 09-14 audit also found).** Three proxies, none of which is "a seat read this row":
  1. Lessons linked by window rows: **63**. Of those, how many are named (short stem, date prefix stripped) in a daily note dated on/after the lesson's first window row: **9 of 63** (71 of the 280 link-slots). A daily note almost never cites by stem (positive control: the family with the most-gated costume, `use-the-fleets-own-tool…`, appears in 1 daily note by full name and 0 by short stem), so this proxy is weak and low by construction.
  2. Lessons whose stem appears in the BODY of a later window ledger row: **37 of 63**; neither a daily mention nor a later-row mention: **24 of 63**.
  3. Rows whose lesson link was already linked by an earlier row inside the same window (recurrence of a known lesson): **206 of 255 rows (81%)**. This measures that the lesson existed and did not stop the repeat; it does not say it was or wasn't read.
  4. By load rule (not a measurement of reading): each boot reads `_ledger.md` whole (seats report 33-110 KB loads in `daily/`), and the by-tier digest whole; archive rows (here 243 of the 255) are read on demand only. So 12 of 255 window rows (4.7%) are in the file every boot reads today; the rest left the boot path via the 3c rule.
  Rows with explicit retrieval wording (`lesson fired`, `read at boot`, `retriev`): **1 of 255**.
- Of the 40 new lessons: **14 are not named by full filename in any daily note** (instrument: substring over `daily/2026-*.md`), 26 are.
- Reading, as numbers only: ledger volume is down to about a quarter of the 09-14 row rate, but 81% of rows repeat a lesson already linked earlier in the same window and the three highest-weight families (21, 16, 10) are all in the top 6 by row count.

## 4. Boot cost

### 4.1 By-tier digest size at each Sunday (instrument: `git -C /Volumes/DevMASTER/WEDNESDAY log -1 --before="<day> 23:59:59" --format=%h -- 0_Brain/learnings/_boot_digest_by_tier.md` then `git show <sha>:<path> | wc -c`)

| as of | sha | bytes | delta vs previous row |
|---|---|---|---|
| Sun 2026-09-20 (previous baseline day) | fcac53c83 | 511,613 | |
| Wed 2026-09-23 (previous audit) | 8f61bde1c | 530,265 | +18,652 |
| **Sun 2026-09-27** | eb6431989 | 544,162 | +13,897 |
| **Sun 2026-10-04** | 008c2610f | 558,845 | +14,683 |
| **Sun 2026-10-11** | 1767f7492 | 590,772 | +31,927 |
| **Sun 2026-10-18** | 53966eb5d | 620,572 | +29,800 |
| working tree 2026-10-19 | | 620,572 | (`wc -c` of the file) |

**+90,307 B (+17.0%) from the 09-23 audit to 10-18**; the last two weeks added 61,727 B, more than double the first two (28,580 B). The default digest `_boot_digest.md` went 534,841 -> 626,441 B (+91,600) over the same days. The by-tier file was regenerated **291 times** in the window (`git log` count). The 09-23 audit's reported 515,587 B was an intra-day figure; the 09-23 end-of-day commit is 530,265 B. Digest lines per boot reads: 6,670 (09-25) -> 7,297 (10-16), "Read in 25K-token chunks" by 10-08.

### 4.2 Statusline after brain load (instrument: regexp over `daily/2026-09-24..10-18.md` boot lines; seats write `Statusline after the load: ctx:NN%`; 186 candidate lines scanned, explicit "after the load/digest/brain load/boot" values extracted by eye from the output)

- **09-24..09-30:** 33, 29, 36, 37, 29, 34, 32, 38, 35, 37, 29, 40, 32, 34 (n=14), range **29-40%**.
- **10-01..10-08:** 39, 38, 32, 34, 40, 31, 34, 31, 33, 35, 36, 33, 32, 36, 34 (n=15), range **31-40%**.
- **10-09..10-18:** 38, 34, 35, 42, 35, 31, 36, 31, 24 (a Sonnet seat reading the ledger only, 10-13), 27/30/25 (10-13 13:36 successor; three figures in one line, ambiguous), 37, 21/39, 15 (10-15, "lean" boot at 7d:93%), 22/41 and 11/35 (10-16, two figures per line), 39 (10-18): range **21-42%** with several lines giving two numbers (before/after).
- **Reading:** the post-load statusline has stayed in the 24-42% band while the digest grew 17%; the load itself has not yet pushed a seat past ~42% of context. The 80-90% rotation band (Kam, 2026-09-07) is far above it, but the 10-13 successor seats rotated at 80% (13:32) after ~6 hours, i.e. boot cost is not what decides rotation. Caveat: this is prose written by seats, not the statusline log; several 10-13..10-16 lines state two figures and I did not resolve which is "after load".

## 5. Drive hygiene (policy `1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md`; ritual line in `skills/weekly-consolidation.md`)

- **Did the weekly survey run in the window? Only the initial one.** Instrument: `grep -n -i -E 'drive[- ]survey|drive[- ]hygiene|SURVEY\.md|G-DRIVE/Scratch'` over `daily/2026-09-24..10-18.md`, plus `ls 0_Brain/reference | grep -i survey`. Hits: `daily/2026-10-05.md` lines 84, 106 ("Dev-drive survey DONE", `0_Brain/reference/2026-10-05_dev-drive-survey/SURVEY.md`), 115, 118 and the 10-05 follow-ups (Docker.raw, Ollama duplicate moved 13:43). **No hit on any later date (10-06..10-18 = 0)** and `reference/` holds one survey dir (`2026-10-05_dev-drive-survey`) and one policy file. Positive control: the identical pattern returns the 10-05 lines, so a re-run entry would have shown. The only later storage items: `learnings/2026-10-15_storage-policy-for-old-blockchain-files-and-tests-monday` and WED-154 (commit `d0eb42d72`, 10-19, a policy + dry-run tool + first report for old Secuura/Blockchain files), which are a different survey, and a 10-10 R 27th mail about four ~2.7 GB worktrees.
- Cause consistent with the record: this is the first consolidation since the policy was written (previous audit 09-23), so the "every weekly consolidation" trigger had no event to fire on in the window.
- **df -h (2026-10-19, read-only):**
  - `/Volumes/DevMASTER`: 1.8 TiB size, 1.6 TiB used, 178 GiB avail, **91% capacity** (past the policy's 85% "immediately" trigger).
  - `/Volumes/G-DRIVE`: 11 TiB, 7.3 TiB used, 3.6 TiB avail, 67%.
  - `/Volumes/G-DRIVE/Scratch Files`: `du -sk` = 165,824,084 KB (about 158 GiB) is the destination of earlier moves; four 10-05 sub-folders exist there (DevMASTER_cleanup, nexusai-O_merged-worktrees, nexusai-O_qa-extracts, WEDNESDAY_spark-work-clones).
  - No receipt line per drive (used/size, GB moved, GB removed, kept-and-why) exists for the window because no survey ran.

## 6. Retro "Candidate new lesson" lines, 2026-09-24 .. 2026-10-18 (instrument: `grep -n -i 'candidate new lesson'` and `grep -i 'candidates?[:-]'` over the daily notes; 23 notes present, 10-17 absent)

- **18 notes still carry the unfilled template line** `- Candidate new lesson? (only if it changes future behaviour)` with nothing after it: 09-24, 09-25, 09-26, 09-27, 09-28, 09-29, 09-30, 10-01, 10-02, 10-03, 10-04, 10-05, 10-07, 10-08, 10-11, 10-12, 10-16, 10-18. (Template line 20 in each; `10-06` and `10-14` have no such line.) Several of those same notes DO carry a later seat-retro `**Candidates:**` line elsewhere in the file that answers the question (09-27, 09-28, 09-29, 09-30, 10-01, 10-02, 10-14), so the template line is stale rather than the candidate unfiled; 09-24, 09-25, 09-26, 10-03, 10-04, 10-05, 10-07, 10-08, 10-11, 10-12, 10-16, 10-18 have a seat retro without a `Candidates:` line.
- **Answered at the template line (4):** 10-09 "None new"; 10-10 "None new… owed mechanism stays a CANDIDATE in that file's family" (the i-endorse mechanism, see 1.4: still unbuilt at w=21); 10-13 "DISCARDED… extension of 2026-08-26_mirror-reports-state-not-intent"; 10-15 "'lean boot at >=95% weekly' DISCARDED as a lesson… put to Kam as a question on the panel (bf-f955bd7b56aa959f), unanswered".
- **Candidates that name a thing and were never filed as a `learnings/` file** (key words grepped across `learnings/20*.md`; zero hits = never filed; each marked as filed elsewhere in its own note where the note says so):
  - 09-26 04:27 "`cockpit.sh say` reporting 'queued behind a running turn' is NOT delivered" (grep 'queued behind' 0 lesson hits; also carried 09-28/09-29 as owed tooling "cockpit.sh say refuses a pane id silently": 'pane id' hits 4 older lessons, none this).
  - 09-28 17:13 "explicit 'never end a turn on a next-up line with nothing running'" (grep 'next up' 0 hits; 09-29 note: "a Stop-hook for the next-up stall (proposed to Kam, another project's launcher)"; no Stop-hook found in any lesson).
  - 09-27 / 09-28 / 09-29 / 09-30: `hold_ready.py` support for test-only / comment_patch / in-place-test runs ("5 by-hand holds tonight"): "FILED as IMPROVEMENTS rows (owed tooling, not a lesson)"; the 09-28 line says the script `night/hold_ready.py` still assumes product-only '+'. 1 lesson hit for 'hold_ready'; not a lesson by design.
  - 10-01 "`stamp.sh` that fills `@NOW@` safely": `tools/` has no `stamp.sh` (ls grep 'stamp|dkim' empty); 'stamp.sh' appears in 1 older lesson only.
  - 10-02 "DKIM check helper for Kam's signature mails": no helper in `tools/`; the topic is covered by 12 older lessons that mention DKIM.
  - 10-02 "briefs drafted by subagents should mark every tool-behaviour claim with its probe; drafter prompt template gains that line (owed, small)": 'probe' appears in 16 lessons, none dated in the window; the template change is not verifiable from the brain.
  - 09-30 "kintsugi brief template should carry `/health/deep` as the KS-1054 probe and the 5.6 GB disk dip": 0 lesson hits for '/health/deep'.
  - 10-15 "lean boot at >=95% weekly": discarded as a lesson by design; open as a panel question to Kam.
  - 10-10 "send_brief flags a ruling that names a tool path the sender has not opened": the owed mechanism for the highest-weight family (w=21). Not filed anywhere as a lesson or an IMPROVEMENTS row that I could locate; the retro files it by name only.
- Everything else in the "Candidates" lines reads "none left unfiled", "every miss is a ledger row", or "FILED". I confirmed three filings by file existence: the 80-90% rule (`2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark.md`), the storage rule (`2026-09-29_regenerable-build-leftovers-are-not-kept.md`), the client-correction rule (`2026-09-29_a-correction-to-a-client-is-a-new-claim-gate-it-like-code.md`). Weekly rule 2a in `CLAUDE.md` says every candidate is FILED or DISCARDED in the same action; 18 notes' unfilled template lines are residue of the template, not necessarily of the rule.

## 7. Items needing Kam (for the final audit, not decided here)

1. KPI 1-4 cannot be measured from Wednesday's seat: a Secuura Linear read key is not in her `.env`; the KS board is invisible to the key she holds.
2. The highest-weight family in the window (i-endorse-things-i-have-not-read, w=21) has an owed mechanism that has not been built for 9+ days; the two gate-backed families (routing token w=16, receipt chain w=10) show the gates catching a habit that does not fall.
3. Grants/rulings with expired end events still `status: live` with active headlines; the 10-09 headline states a rule dead for 10 days.
4. DevMASTER at 91% against the 85% trigger; no weekly survey since 10-05.
5. By-tier digest +17% in 25 days and accelerating (+61.7 KB in the last two weeks vs +28.6 KB in the first two); the 09-23 audit said halving needs retiring whole rules, which is his call.
