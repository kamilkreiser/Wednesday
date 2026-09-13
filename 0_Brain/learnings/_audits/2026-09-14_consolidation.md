---
date: 2026-09-14
type: audit
status: REVIEWED by Wednesday 2026-09-14 07:3x (drafted by a Wednesday-assistant subagent; numbers spot-checked at source below)
window: 2026-08-31 → 2026-09-14
source: measured by a drafting subagent on 2026-09-14 (raw outputs in `2026-09-14_consolidation_measurements.txt` beside this file); nothing merged, cut, superseded or executed — proposals only, per Kam's 2026-08-10 ruling
previous: "[[2026-08-30_consolidation]] (the 09-07 board KPI baseline lives in `skills/weekly-consolidation.md`)"
---

# Weekly consolidation — 2026-09-14 (two weeks overdue: covers 08-31 → 09-14)

Every number below names the instrument that produced it; the command and its raw output are in the
measurements file. Counts of Linear tickets come from `fleet/board_count.sh` wherever it would print a
total; where it refused (>250 rows) the count is the SUM of two disjoint board_count partitions, stated
as such. Nothing in `learnings/` was edited. Two consolidations were missed (09-06 and 09-13); this note
covers both weeks.

## BLUF

1. **Ledger volume: 697 rows / 1.41 MB written by Wednesday's seat in 15 days** (`grep -c '^| 2026-'` over
   `_ledger.md` + `_ledger_archive.md`, window dates) — 46/day mean, peak **112 on 09-09**; the ledger
   family grew **+1.79 MB in 669 commits** (`git cat-file -s` at the pre-window commit vs HEAD). The
   09-07 KPI note measured ~65 KB in one afternoon; the fortnight ran at ~120 KB/day.
2. **Boot cost is now governed by rule 3c, not by the digest:** ctx after the brain load fell from
   **45–53 %** (09-10 → 09-12, ledger 191–256 rows) to **28–33 %** (09-13 → 09-14, ledger 101 lines) while
   the by-tier digest itself grew **291 KB → 418 KB (+44 %)** in the same week (`git cat-file -s`).
3. **Board (KS): 380 open (108 active + 272 backlog), 98 instrument-subject by the word-boundary
   title predicate (25.8 %), 125–128 by the substring form** (board_count.sh; the substring form counts
   `gateway` as `gate`, 25 titles). Baseline 09-07 was 293 open / 88 (30 %) by a HUMAN catalogue, so the
   ratio is flat-to-down and the absolute count is up — **286 of the 380 open tickets were created inside
   this window.**
4. **36 window-born lesson families reached w≥3** (strict Lesson-column tally); the four largest are
   `a-false-absence-is-usually-my-own-instrument` (67 rows), `qa-gate-before-my-verification` (47),
   `a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact` (42), `a-retraction-inherits-the-scope-
   of-its-measurement` (35). Of the mechanisms the rows themselves named, **8 are built and 14 are not**
   (grep of the named tool; §Promotions).
5. **Rituals: the 23:00 close ran 13 of 14 nights (09-12 has no close block) and the WRAP CHECK FAILED on
   10 of the 12 that carry a check line** (`grep 'WRAP CHECK'` per daily note; 09-04's close has none) — an alarm that fires every night is the 08-30
   audit's own "alarm that always fires". 86 self-rotations, 9 DEAD respawns (5 on the live floor, of which
   **2 were false kills of a healthy seat**, 09-13 23:39 and 09-14 06:53), 11 refusals (rotate log).

## Boot-cost line (the standing item)

| Instrument | 08-30 audit | 09-07 (KPI note) | 09-10 | 09-14 now |
|---|---|---|---|---|
| lesson files (`ls 2026-*.md`, excl. conflict copy) | 84 | — | 138 | **159** (77 created in window; 410 KB of the 811 KB total — **51 % of all lesson bytes are 15 days old**) |
| `_boot_digest_by_tier.md` (`git cat-file -s` / `wc -c`) | (built 09-02) | 291,126 | 395,157 | **418,347** |
| `_boot_digest.md` | — | 317,538 | 422,578 | **445,930** |
| `_ledger.md` (own seat) | 254 KB / 219 rows | 332 KB (391 KB at commit) | 612 KB | **98 KB / 68 rows** (rule 3c) |
| ctx after brain load (daily-note lines, `Statusline after the brain load` / `Boot (measured)`) | ~45–50 % | — | 45 % (06:11) | **28 %** (06:54) |

The full series (file:line in the measurements file): 09-08 21 % · 09-09 41/22/22 % · 09-10 45 % · 09-11
29/47/44/40/46 % · 09-12 47/53/47/40 % · 09-13 33/29 % · 09-14 28 %. Every reading above 40 % had a ledger
of 190–256 rows in the load; every reading below 34 % had ≤168. **The digest is ~14–21 % of context on its
own (09-08 and 09-09 measured it directly); the rest is the ledger.** Tier split: W 121 files / 535 KB ·
M 33 / 144 KB · MIXED 5 / 132 KB · **P: none** — no lesson has been tiered P, so the "single handle" tier
carries nothing. One file, `2026-08-07_a-check-that-cannot-fail.md`, is 77,770 B — 9.6 % of all lesson
bytes on its own (MIXED tier, so its cases are already reduced to handles in the by-tier digest).

**Full load STAYS** (Kam 08-06, 08-10, 08-21). The archive cadence is holding the ledger; the digest is the
number now rising. Card `wed-ledger-boot-cost` is still the open lever.

## Ledger review

### Volume (instrument: `grep -c '^| 2026-'` on `_ledger.md` + `_ledger_archive.md`; bytes `wc -c`)

- **Now:** `_ledger.md` 98,288 B / 68 rows (09-11 31 · 09-12 12 · 09-13 24 · 09-14 1). Archive 1,569,816 B /
  848 rows; its headings confirm every date ≤ 2026-09-10 has been moved (last move 09-13 22:1x, 76 rows of
  09-10, conservation asserted in each heading).
- **Window rows (Wednesday seat): 697** — 08-31 4 · 09-01 34 · 09-02 52 · 09-03 38 · 09-04 32 · 09-05 38 ·
  **09-06 97** · 09-07 71 · 09-08 75 · **09-09 112** · 09-10 76 · 09-11 31 · 09-12 12 · 09-13 24 · 09-14 1.
  The fall after 09-10 coincides with the Tuesday split (09-07) and the 09-11 case-sensitive-zero day; it
  is not yet a trend (three days).
- **Rows per seat:** only 16 of 697 rows name their seat by clock and 80 carry the `[W]` tag, so per-seat
  attribution is NOT measurable from the rows. Proxy — rows/day ÷ (rotations that day + 1) from the rotate
  log: 09-06 97/18 ≈ 5 · 09-07 71/7 ≈ 10 · 09-08 75/5 = 15 · **09-09 112/7 = 16** · 09-10 76/3 ≈ 25 · 09-11
  31/9 ≈ 3. **Proposal:** the row template gains a mandatory seat column (`seat: HH:MM`) — it costs nothing
  and makes KPI line 5 measurable next time.
- **Bytes added to the family this fortnight: +1,791,548 B** (`_ledger.md` 253,543 → 98,288; archive 0 →
  1,569,816; laptop 0 → 49,716; laptop archive 0 → 236,975; fleet_insights 0 → 90,296), across 669 commits
  touching the family. numstat: `_ledger.md` +783/−928 lines, archive +920/−2.
- **Severity (fixed-string grep per marker):** 🔴 189 · 🟠 79 · 🟡 177 · 🟢 88 · 🔵 1 · unmarked 163. Type
  keyword: correction 475 · praise 61 · positive 50 · insight 45 · finding 18 · grant 13 · ruling 10.
- **Tuesday's seat (`_ledger_laptop_datasec*.md`, ROW COUNTS ONLY, bodies not read): 118 rows in the
  window** — 09-07 27 · 09-08 33 · 09-09 21 · 09-10 13 · 09-11 4 · 09-12 8 · 09-13 9 · 09-14 3. The fleet
  insights file holds 42 rows (09-03 33, 09-04 9) and nothing since.

### Families (instrument: Lesson-column `[[link]]`s, one count per row; strict = field 5, loose = anywhere in the row)

Top 15 (strict / loose): `08-14_i-read-representations-they-read-sources` **275**/284 ·
`08-07_a-check-that-cannot-fail` **176**/190 · `08-09_an-enforcement-you-must-arm-is-not-one` **139**/147 ·
`08-04_validate-brief-pointers` 69/71 · `09-08_a-false-absence-is-usually-my-own-instrument` 67/80 ·
`08-13_headline-must-match-the-operative-case` 58/63 · `08-16_classification-is-the-field-that-grants-
authority` 57 · `09-01_qa-gate-before-my-verification` 47/49 · `08-16_an-overstated-record-gets-discounted-
wholesale` 46/49 · `08-15_a-cap-is-never-neutral` 46/51 · `08-16_a-recorded-blocker-is-not-a-boundary` 43/47 ·
`09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact` 42/45 · `08-21_challenge-me-when-you-
think-im-wrong` 36/38 · `09-06_a-retraction-inherits-the-scope-of-its-measurement` 35/38 · `08-06_exercise-
mechanisms-before-arming` 34/36. 128 distinct lessons cited (strict), 140 (loose); 1,952 links in the Lesson
column. 43 rows (all 09-11) use a pipe form the strict split cannot read — the loose tally covers them.

**Three families carry 590 of 1,952 links (30 %).** The 08-30 audit said representations was w=46; it is
now cited by 275 rows in 15 days. That is not a weight, it is the ledger's default classification — see the
merge/supersede proposal.

### w≥3 in the window — the 36 window-born families (strict count ≥3)

67 `09-08_a-false-absence-is-usually-my-own-instrument` · 47 `09-01_qa-gate-before-my-verification` · 42
`09-05_a-relayed-ruling…artefact` · 35 `09-06_a-retraction-inherits-the-scope-of-its-measurement` · 29
`09-07_a-census-complete-over-a-frame-that-is-not` · 22 `09-04_decisions-held-narration-drifted` · 20
`09-01_a-tap-is-a-pointer-not-a-message` · 16 `09-02_coo-actionable-tickets-never-wait-for-kam` · 13
`09-08_a-safety-claim-names-the-property-it-checked` · 13 `09-07_a-mechanism-is-recorded-by-its-path-not-its-
runtime-id` · 12 `09-08_the-check-ran-and-was-not-checking-the-thing` · 11 `09-07_git-topology-is-a-
measurement-not-a-model` · 11 `09-07_an-instruction-to-wait-must-name-what-wakes` · 11 `09-07_a-prior-
ruling-gate-refusal-is-a-research-prompt` · 11 `09-06_other-projects-repos-are-read-only-git-verbs-that-
write` · 9 `09-09_my-authority-and-the-targets-rules-are-two-checks` · 9 `09-02_the-statusline-is-the-
context-instrument` · 9 `09-02_rotate-in-the-70-80-band-conditionally` · 8 `09-09_the-seat-resolver…` · 8
`09-08_a-new-rule-is-most-dangerous-just-after-adoption` · 8 `09-07_name-the-field-that-says-whose-it-is` ·
8 `09-03_a-pane-close-is-a-session-kill` · 7 `09-10_i-endorse-things-i-have-not-read` · 7 `09-07_a-
classification-list-is-a-representation…` · 7 `09-05_qa-gate-tiers-and-the-two-nogo-cap` · 6 `09-10_a-
refusal-nobody-reads…` · 6 `09-08_a-ruling-can-be-voided…` · 6 `09-02_style-guides-never-mixed` · 5 ×3
(`09-07_a-rule-for-creation…`, `09-06_a-scoped-override…`, `09-05_tickets-are-the-channel…`) · 4 ×2
(`09-10_a-detector-keyed-on-remedy-text…`, `09-09_acknowledge-panel-instructions…`) · 3 ×3.

**Regressions named as such by the rows (🔴 + "w=3" / "REGRESSION" in the headline), with the owed
mechanism verbatim:**

- **09-11 — "THIRD CASE-SENSITIVE FALSE ZERO IN ONE DAY — w=3, a REGRESSION"** (family: false-absence /
  check-that-cannot-fail). The rows' own rule: `/usr/bin/grep -i` and a positive control for every zero.
  **Mechanism: none found** — `Launch_Wednesday.command`'s initial prompt (298 lines) has 0 hits for
  `usr/bin/grep`, `positive control`, `PIPESTATUS`, `never cd`. The rule lives in briefs and in this
  drafting brief, not in the boot.
- **09-11 — "I GATED A LAUNCH ON `${PIPESTATUS[0]}` IN A ZSH SHELL — the exact check-that-cannot-fail an
  existing lesson names by title"** and **"IN THIS TOOL'S zsh, `grep` IS NOT `/usr/bin/grep`"**: same
  family, same absence of a boot-prompt line.
- **09-11 — "I BRIEFED A SEAT TO POST TO THE EXTRANET SIX DAYS AFTER KAM RULED IT IS NOT A CHANNEL — w=3
  of the family, so this is a REGRESSION"** (family `09-05_tickets-are-the-channel…`, and the 09-11 row
  "A RULE KAM WITHDREW ON 09-06 WAS STILL LIVE IN `fleet/STANDING_LINES.md`"). Mechanism named 09-06:
  *"`send_brief.sh --kind brief` greps the previous ANSWERs to the project for lines beginning 'RULED' and
  refuses when none of them is quoted"* — **partly built** (the undelivered-rulings gate exists at
  `send_brief.sh:484`; 09-13 found seats C–E were skipping it and fixed the prefix). STANDING_LINES.md
  (17,443 B, 247 lines) has no expiry column.
- **09-13 — `git -C $VAR commit` "the w=3 costume, again … the habit-level rule has now failed on the
  variable-path costume at four seats; only the in-path hook has ever held."** Mechanism: **built**
  (`hooks/pretooluse_no_cd.sh`, the 09-07 gitwrite + 09-08 scratch revisions; `cd` refusal at line 22,
  `git -C` outside-tree refusal at line 32). The rows' remaining candidate: *"treat `cp SRC DST` by DST
  only"* in `pathguard.py` — **not built** (`"cp"` still sits in the plain write-verb list, line 47).
- **09-14 — "THE DEAD LEG KILLED A SECOND HEALTHY COORDINATOR IN EIGHT HOURS"** (w=2 → lesson filed the
  same boot; family `09-10_a-detector-keyed-on-remedy-text-matches-the-hint`). Mechanism: **built and
  wired** (`cockpit/dead_banner_check.sh`, 3,637 B, 07:04; wired in `wake_watch.sh` and
  `wednesday_rotate.sh`, 2 hits each; `.pre-0914-deadbanner` backups kept). Validation pending a real fire
  (DGM rule).

### Praise / positive rows (instrument: type column contains `praise` = 61 rows; 🟢 = 88 rows)

Kam's verbatim praise, all dated 09-03 → 09-07: *"With regards to Secura, that is fantastic. Please adopt
this as the process going forward"* (09-03 11:59) · *"That's amazing progress … Today is a great day"*
(09-03 12:53) · *"this is a good sign of agent collaboration"* (09-04 11:08) · *"the process we've built
works"* (09-05 16:45) · *"move your restart threshold to 80%"* (09-05 20:28, grant) · **"Great find. This is
another proof point that the process is working well. Please continue."** (09-07 10:46) · *"Great
learning."* (09-07 13:36). **Zero praise-typed rows after 09-08** and one verbatim Kam quote in the
09-09 → 09-14 rows (a ruling). The 09-08 cluster (15 🟢 rows in one day) is agent-caught behaviour, not
Kam's voice. The praise cluster to protect is unchanged from 08-30: honesty un-hedged; measurement raised
as HIS decision, not a verdict; a gate refusal read instead of overridden (09-10 found a two-day-old
unexecuted grant that way).

## Promotions EARNED (proposals only — nothing executed)

Each: family · weight (strict rows) · the mechanism the rows named (verbatim) · built? (grep of the named
path, count in the measurements file §7).

| # | Family | w | Mechanism named by the rows | Built? |
|---|---|---|---|---|
| 1 | composed invocation / `cd` / `git -C` outside tree (`08-09_an-enforcement-you-must-arm…`) | 139 | 09-02: *"a PreToolUse hook that refuses a Bash call beginning with `cd `"*; 09-06/07: *"the pretooluse hook refuses `git -C <path outside WEDNESDAY> (fetch…"* | **YES** — `hooks/pretooluse_no_cd.sh` (both legs) |
| 2 | same, `cp` false positive (09-13) | +1 | *"treat `cp SRC DST` by DST only"* (pathguard) | **NO** — `"cp"` in the write-verb list, `pathguard.py:47` |
| 3 | validate-brief-pointers, carried-prediction costume (`08-04_validate-brief-pointers`) | 69 (+5 +7 +1 +1 on 09-13 alone) | 09-13: *"the brief template's tamper table gains a column `predicted-by` (drafter / Wednesday-read), and the gate reports slips only against Wednesday-read rows"* | **NO** — 0 hits in `send_brief.sh` and `qa-agent/BRIEF_TEMPLATE.md` |
| 4 | carried-control costume (09-13, #975) | +1 | *"the gate-set install check greps each §4 control token against the head tree (`git grep -c` at the head SHA) before `--check` — a 0 refuses the install"* | **NO** — `gen_launcher_from_template.py` checks its OUTPUT pins (line 81) not the head tree |
| 5 | HOLDS blanket bans (09-09 "w=4") | ≥4 | *"`send_brief.sh` refuses a HOLDS section containing a bare 'nothing else' or an unqualified verb-class ban"* | **NO** — 0 hits |
| 6 | card carried into HOLDS unread (09-08 "w=3") | ≥3 | *"`send_brief.sh` requires a card carried into HOLDS to name the artefact checked and the date read, or be listed as UNKNOWN rather than asserted"* | **NO** |
| 7 | undelivered rulings (09-06 "w=2 … now the build") | — | *"`decision_queue.sh --delivered <artefact>` … `send_brief.sh --kind brief` refusing a project brief while that view is non-empty"* | **YES** — `decision_queue.sh` (35 hits), `send_brief.sh:484`; seats C–E hole closed 09-13 |
| 8 | listing cap on the inbox (09-06 "w=3 of this costume") | 3 | *"`inbox_digest.sh --inbound` unbounded, and the boot prompt names it"* | **YES** — `inbox_digest.sh:9,89` |
| 9 | pane close on a live turn (09-03 "at w=3", 09-06 "w=2 promotes it") | ≥3 | *"`pane_close.sh` refuses when the last 8 lines of the pane carry a spinner glyph … or when `cockpit.sh say`'s last receipt for that pane was 'queued'"* | **NO** — refuses tty/self/listener only |
| 10 | detector keyed on its own words (`09-10_…remedy-text`, 09-13 ×2, 09-14 w=2) | 4+ | 09-14: `dead_banner_check.sh`; 09-13: *"those tokens [STOP/HOLD/HAND OVER NOW/CHECKPOINT] appear in a subject only as the instruction itself"* | **YES** (banner check) / **rule only** (subject tokens) |
| 11 | brief clock vs artefact (09-06 "w=7 would promote it") | 7 | *"`send_brief.sh` refuses a body whose SELF-CHECK timestamp predates the file's mtime by more than N minutes"* | **NO** — 0 hits for `mtime` |
| 12 | sequencing contradiction between mails (09-05 "at w=3") | 3 | *"send_brief's self-check refuses a sequencing verb … on a PR id the previous mail to that agent sequenced differently unless the body says SUPERSEDES"* | **NO** |
| 13 | universal negatives about deployed state (09-08) | — | *"refuse a body containing a universal negative … unless the PROVENANCE block carries a line naming the instrument that WOULD have seen the positive"* | **NO** |
| 14 | BLUF arrow-to-incident (09-07 "w=3 would promote it") | — | *"`decision_queue.sh` refuses a BLUF containing an arrow-or-`means` construction to an INCIDENT/BLOCKER word unless … `does not exclude` / `necessary but not sufficient`"* | **NO** |
| 15 | case-sensitive false zero (09-11 w=3 REGRESSION) | 3 in a day, 67 family | rows: `/usr/bin/grep -i` + a positive control per zero | **NO** boot-prompt line; **no** hook |
| 16 | quiet-claim corpus (09-01) | — | *"board_watch_peter.sh prints its corpus line at start"* | **NO** — 0 hits for `corpus` |
| 17 | felt-clock stamps (09-13, clock-composition sub-class) | +1 | `tools/note_entry.sh` "exists and was not used" | **BUILT 08-30, unused** — a promise-shaped mechanism |
| 18 | backtick in unquoted heredoc (09-01) | — | *"a pre-commit check that refuses a backtick inside any unquoted heredoc body in tracked .sh/.command files"* | **NO** — `hooks/pre-commit` covers conflict markers only |

**Recommendation to Wednesday (not to Kam — these are inside her own tools):** items 3, 5, 6, 9, 15 have
the weight and a named, bounded refusal each; build order by cost-of-miss: 15 (a false zero on "no outage"
is the worst-direction error) → 3 → 9 → 5 → 6. Item 17 needs no build — it needs the note-writing habit to
call the tool that exists; a boot-prompt line is the cheapest form.

## Lessons: merge / supersede PROPOSALS (none executed — Kam's 2026-08-10 ruling stands)

1. **The three "default" families are absorbing everything.** `i-read-representations`, `a-check-that-
   cannot-fail`, `an-enforcement-you-must-arm` take 590 of 1,952 Lesson-column links; rows cite them
   alongside a specific lesson in most cases. **Proposal:** no merge — instead a ledger-row rule that the
   FIRST link is the most specific lesson and the parent family is optional; the family index
   (`_family_index.md`, generated 09-10) can then rank by first-link. Loses nothing; sharpens retrieval.
2. **Three lessons are one mechanism at three dates:** `09-10_a-detector-keyed-on-remedy-text-matches-the-
   hint` · `09-14_a-detector-keyed-on-the-banners-words-kills-the-seat-that-reports-the-last-kill` · the
   09-13 subject-token rule (row only, no file). **Proposal:** the 09-14 file gains a `parent:` pointing at
   09-10 and the 09-13 subject-token rule becomes a section in 09-10 (append, not merge). Kam's word needed
   only if "append a section" counts as a merge.
3. **`08-07_a-check-that-cannot-fail` (77,770 B, MIXED) vs `09-08_a-false-absence-is-usually-my-own-
   instrument` (21,888 B, W) vs `09-08_the-check-ran-and-was-not-checking-the-thing` (5,034 B, M):**
   three files, one lesson family, 255 rows between them. **Proposal:** cross-link only (`related:` lines);
   the 08-07 file's 28 project CASE sections are already reduced to handles by the by-tier digest, so its
   size costs the boot little. A split of the 08-07 file into rule + case-book would be a rewrite —
   forbidden.
4. **Four dangling handles in the ledger** (links to files that do not exist): `2026-09-02_launcher-quote-
   truncation` (2 rows; nearest file `08-29_unquoted-heredoc-executes-backticks`), `2026-09-06_a-cap-is-
   never-neutral` (1 row; the file is dated 08-15), `2026-09-08_a-decision-stays-on-the-page-while-the-
   world-moves` (1 row, cited as "parent family … is high" — **no file exists**), `2026-09-09_a-hold-
   names-the-property-it-protects` (1 row; nearest `09-08_a-safety-claim-names-the-property-it-checked`).
   **Proposal:** add the two missing files (09-08 decision-stays, 09-09 hold-names) from their rows — they
   were cited as families and never written — and leave the two mis-dated links as they are (a row is never
   edited); the family index can carry an alias line.
5. **Conflict copy** `2026-09-02_coo-actionable-tickets-never-wait-for-kam (conflict_on_2026-09-04).md`
   still sits beside its original; never-delete rule → quarantine by the 08-26 lesson's method when Kam
   says so. Not counted in any total above.
6. **`status: superseded` is on 3 of 159 files** (07-31 portable-drive, 08-06 morning-shift-change, 09-13
   rotation-never-blocks) and six more carry a superseding NOTE inside a `status: live` line. **Proposal:**
   the census tool (`_tier_census.md`) reports "live-with-supersession-note" as its own class so the count
   is honest; no file edits.

## Retrieval / never-fired (KPI line 5 — did a row or lesson ever fire?)

Instrument: every `[[2026-…]]` link in a window row (loose tally) vs `ls learnings/2026-*.md`.

- **134 of 159 lessons were cited by at least one window row** (140 distinct handles cited, 6 of them dangling). 12 pre-09-01 lessons were cited by **no
  Wednesday row in 15 days**: `07-31_fully-portable-drive` (superseded) · `07-31_one-question-at-a-time` ·
  `07-31_parent-child-learning-model` (linked from 7 other lessons) · `08-03_contemplation-the-cockroach` ·
  `08-05_life-os-commission-principles` · `08-06_morning-shift-change` (superseded) · `08-07_autonomy-grant-
  ship-decisions` (Tuesday cited it once) · `08-07_valid-is-not-delivered` · `08-12_hpsm-continuous-
  readiness-grant` · `08-13_containment-never-run-is-a-claim` (Tuesday ×4) · `08-22_vendor-asks-scale-to-
  leverage` · `08-28_contemplation-mistakes-and-the-fixed-will`. Most are grants, contemplations and
  principles — the kind that fire in behaviour, not in a correction row — so "never cited" is weak evidence
  of "never fired". **Nothing proposed for deletion.** Candidates for a `tier: P` (handle only) are the
  three grants (08-07 autonomy, 08-12 hpsm, 08-22 vendor) and the two contemplations, IF Kam agrees P is
  the right shelf for a text he wrote to be re-read whole.
- **13 window-born lessons have never been cited by a later row** (list in the measurements file) —
  expected for files days old; check again at the next audit.
- **A row that fired:** the 09-08 praise row *"THE LOOP CLOSED: s151's LAST lesson was applied by its
  SUCCESSOR within thirty minutes, on the identical situation, and it prevented the exact…"* is the one
  documented instance this fortnight of a row being read by the next seat and changing its act. That is
  the number the KPI asks for and **it is 1 measured instance in 697 rows** — not because the others did
  not fire, but because nothing records a retrieval. **Proposal:** a boot step that appends `retrieved-by:
  <seat>` to a row it acted on (one line in the row's last column), so the next audit can count.

## STANDING KPI — the five lines (measured; the ruling on what they mean is Kam's)

1. **The split.** Open KS tickets: **380** (`board_count.sh`: active 108 + backlog 40 + 232 by createdAt
   partition; positive control `zzqqxx` = 0). Instrument-subject by TITLE, predicate stated:
   `\b(guard|gate|harness|preflight|hook|red-proof|red proof|census|lint|ci)s?\b` case-insensitive →
   **98 (25.8 %)**; the substring form (`containsIgnoreCase` for the same words, no CI) → **125**; with
   bare-substring "CI" → 150. **The boundary is `gateway`:** 25 titles hit `gate` only inside
   `gateway`/`aggregate`/`delegate`, 4 hit `hook` only inside `webhook`. **The class is 98–128 depending on
   the boundary.** Active-only: 35 (word) / 32 (substring). A title-OR-description form gives 289 and is
   not a subject predicate. Description-based classification (the 09-07 catalogue's "ours / product /
   both") was human judgement and is not reproduced here.
2. **The trend.** 09-07 baseline **293 open / 88 (30 %)** by the s147 catalogue → now **380 / 98 (25.8 %)**
   by the word predicate. Ratio flat-to-down; absolute count of instrument tickets +10; **open total +87**.
   Reconstructed from createdAt/closedAt (archive time invisible, so these run high): 08-31 190 open /
   15.3 % instrument → 09-07 354 / 24.9 % → 09-14 438 / 25.6 %. **The ratio doubled between 08-31 and 09-07
   and has been flat since.** 286 of the 380 open were created inside the window (84 instrument-word);
   174 closed in the window (Done 88 · Deployed to UAT 63 · Tested Not Deployed 10 · Duplicate 9 · Canceled
   4), of which 124 were also created in it. **Net +112 open in 15 days.** Whether product defects fell is
   not measurable from titles — the LOOPING signal in the skill's words needs a product-defect count that
   no field on the board carries.
3. **The outcome test.** Instrument-subject tickets CLOSED in the window (title-word predicate,
   `completedAt`/`canceledAt` ≥ 08-31, archived included): **55** (62 by substring). Full list with titles
   is in the measurements file §5 and, for Wednesday's judgement, the 55 are: KS-691 (preflight from a
   worktree) · KS-703 (NUL-byte guard bodies only) · KS-685 (process while CI unavailable) · KS-815 · KS-827 ·
   KS-831 · KS-832 · KS-822 · KS-830 (canceled) · KS-850 · KS-833 · KS-853 · KS-842 · KS-879 · KS-873 ·
   KS-881 · KS-857 · KS-859 · KS-490 (Review E, CI/CD supply chain) · KS-899 · KS-914 (SSRF guard not
   rebind-proof) · KS-923 · KS-921 · KS-644 (/api/events no admin gate) · KS-803 (dup) · KS-892 (dup) ·
   KS-858 (scope gate bypass by `//`) · KS-989 · KS-1001 · KS-860 (55 listeners bind all interfaces) ·
   KS-970 · KS-854 · KS-818 · KS-1056 (dup) · KS-1067 · KS-909 · KS-936 · KS-778 · KS-1086 · KS-687 · KS-971 ·
   KS-1002 · KS-927 · KS-1029 (PATCH dsr 200→500) · KS-1070 · KS-941 · KS-876 · KS-885 · KS-886 · KS-828 ·
   KS-800 (body parser after guard) · KS-992 · KS-1024 · KS-877 · KS-901.
   **A proxy, not the answer:** 46 of the 55 are named by at least one LATER ticket; those later tickets
   split **68 instrument-titled / 71 not** — and **32 of the 55 have at least one later non-instrument
   ticket naming them** (e.g. KS-858 → 6 product tickets, KS-859 → 5, KS-971 → 5, KS-490 → 10). The
   inverse also shows: KS-800 → 10 instrument tickets / 3 product; KS-860 → 6 / 1; KS-879 → 4 / 0. **"Did it
   catch a real defect" is Wednesday's read of those titles, not this proxy.**
4. **Duplication rate.** Open tickets sharing ≥4 significant title words or a file path: **67 pairs, 31
   clusters, 88 of 380 tickets in some cluster** (largest 6, 6, 5, 5, 5); 26 strong pairs (≥6 words or the
   same path). The strongest: the `tsconfig excludes src/__tests__` family **KS-1122 / KS-848 / KS-1000 /
   KS-933** (one cause, four services, four tickets — 7–8 shared words each); `POST /api/verification/verify`
   **KS-1119 / KS-1118 / KS-1114**; TOTP-recovery **KS-809 / KS-783** (7 shared words, near-identical);
   consent-page redirect **KS-841 / KS-798**; api-gateway spec bind mount **KS-1021 / KS-987**;
   `run-shell-suites.sh` ×4 (KS-1127 / 1088 / 1089 / 1135); `check-stack-safety.sh` KS-1093 / KS-1034;
   `withGeneratedActors` KS-1026 / KS-994; `start-secuura.sh` KS-1096 / KS-1011 / KS-972. Baseline 09-07:
   "5 findings across 14 tickets". **Now: ~31 clusters / 88 tickets by a mechanical predicate** — not the
   same instrument, so not a trend line yet; the predicate is now written down and re-runnable.
5. **Wednesday's own volume, beside the board number.** Board: 286 new open tickets in 15 days, 98
   instrument-subject. Brain: **697 ledger rows / 1.41 MB in the same 15 days** (Tuesday's seat 118 more),
   **77 new lesson files / 410 KB**, 669 commits to the ledger family. Rows per seat: not attributable from
   the rows (16 name a seat); proxy 3–25 per seat by day. **Retrieved:** one measured instance of a row
   changing a later seat's act (09-08); 134 of 159 lessons cited at least once; **no instrument records
   that a row was read** — the same gap as the board's outcome line. Working hard or talking to itself is
   Kam's call; the number that would settle it (retrievals) is the one the brain does not yet keep.

## Rituals health (instrument: daily notes + `cockpit/logs/rotate_wednesday.log`)

- **23:00 close:** a close block exists on 13 of 14 nights (08-31 → 09-13); **09-12 has none** (`grep -ci
  '23:00 close|close bell'` = 0). **WRAP CHECK FAILED on 10 of the 12 nights that carry a check line**
  ("retro still on its template placeholder" ×8, "NO retro section at all" ×1, uncommitted files named on
  4 of the 10 — 08-31 was uncommitted-only); verified/OK on 09-01 and 09-11 only; 09-04's close block has
  no check line. The 08-30 audit built the close bell to stop an alarm that always fires; this one now does.
- **Retro sections:** counted per note (H2/H3 "retro"): 08-31 1 · 09-01 9 · 09-02 12 · 09-03 4 · 09-04 3 ·
  09-05 → 09-14 mostly 1 — the per-seat retro of early September became a per-day retro; the wrap check
  reads the template placeholder because the seat that closes is not the seat that wrote the day's retro.
- **Seats per day:** not cleanly countable from the notes (three formats across the window); by the rotate
  log, self-rotations per day: 09-02 5 · 09-03 9 · 09-04 4 · 09-05 7 · **09-06 17** · 09-07 6 · 09-08 4 ·
  09-09 6 · 09-10 2 · 09-11 8 · 09-12 5 · **09-13 13** · 09-14 0 (to 07:00) — **86 in the window** (median
  ~6/day; 3.4 h per seat at 20 h/day).
- **DEAD respawns: 9** — 5 on the live floor (09-02 16:20 + 16:30, 09-05 13:32, **09-13 23:39, 09-14
  06:53**), 4 in test sessions (`wedtest_*` ×3, `rtest`). The last two live ones were false kills of a
  healthy seat (the 09-14 lesson); fix built 06:58 same day.
- **REFUSED: 11** — 9 `--self` (3 dirty tree, 6 `HEAD != origin/main` — all 09-11/09-13, i.e. the push-
  first rule refusing correctly), 2 `--dead` ("pane does not show 'Context limit reached'" — the guard's
  positive-control side, both correct). 10 LIVENESS FAIL lines, all in test harness sessions.
- **Consolidation:** 0 of 2 due ran on time (09-06, 09-13); this note is the catch-up. The 08-30 scope note
  asked Kam whether Sunday is the slot — unanswered, and moot since neither Sunday ran it.
- **Ledger archive rule 3c:** ran 9 times (headings), each with a conservation assertion; the ~3-day
  cadence held (09-10 rows moved 09-13). The ledger sits at 98 KB, under the digest for the first time
  since the rule was written.

## For Kam's decision

1. **Client/Project: Secuura / Blockchain (Platform K).** *Question:* the board is 380 open, +87 since
   09-07, 286 of them created in 15 days; 98–128 are about gates/guards/harnesses; 88 sit in mechanical
   duplicate clusters. *Options:* (a) keep watching (his 09-07 ruling) with this predicate as the fixed
   instrument; (b) a one-off dedupe pass on the 31 clusters by a Secuura seat (read-only proposal list →
   Peter/Stuart decide); (c) a creation-side rule: a new instrument ticket must name the product defect it
   exists to catch or carry a `meta` label. *Recommendation:* (b) now — it is judgement-free by his own
   words — and (c) as a question to Peter, not a rule Wednesday sets.
2. **Wednesday (own project).** *Question:* the by-tier digest is 418 KB and rising 15 % a week; the
   ledger is under control by rule 3c; no lesson is tiered P. *Options:* (a) leave it (full load stays);
   (b) tier the 12 never-cited pre-09-01 files and the grants/contemplations P — handle at boot, whole on
   demand; (c) a byte budget for the digest with a doctor warning at 500 KB. *Recommendation:* (b) for the
   five grants/contemplations only, with his word on whether a text he wrote may be a handle at boot.
3. **Wednesday (own project).** *Question:* may the 09-14 audit's retrieval instrument be built — a
   `retrieved-by:` mark a seat appends to a ledger row it acted on (append-only, one token)? It touches
   ledger rows, which the 3c rule treats as immutable. *Options:* (a) yes, append-only column; (b) a
   separate `_retrievals.md` log keyed by row date+headline hash; (c) no. *Recommendation:* (b) — it leaves
   rows untouched and is countable.
4. **Wednesday (own project).** *Question:* the WRAP CHECK fails 10 nights in 12 on the retro placeholder
   because the closing seat is not the retro-writing seat. *Options:* (a) the check reads the LAST retro
   block of the day, not the template; (b) the 23:00 close writes the retro itself from the day's blocks;
   (c) leave it and read the failures as real. *Recommendation:* (a) — it is a check aimed at the wrong
   property (his 09-08 lesson), not a failing ritual.
5. **Wednesday (own project).** The 2026-08-10 no-merge ruling: the four proposals above are appends and
   cross-links, not merges. *Question:* does "append a section / add a `parent:` line" fall under the
   ruling? *Recommendation:* treat appends as allowed, merges and cuts as forbidden, and say so in the
   skill file.

## Method (every command, so Wednesday can re-run one)

All in zsh via the Bash tool; `/usr/bin/grep` throughout; absolute paths; no `cd`; the Linear key read
from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` into `LINEAR_API_KEY` inside the
one call that used it, then `unset`; read-only queries only. Scratch files under the session scratchpad
(`window_rows.txt`, `family_counts*.txt`, `ks_issues.json`, `ks_dups.json`, `rotlog.txt`).

- Ledger rows: `/usr/bin/grep -c '^| 2026-' _ledger.md` · per date `/usr/bin/grep -o '^| 2026-[0-9-]*' … |
  sort | uniq -c` · window rows `cat _ledger.md _ledger_archive.md | /usr/bin/grep -E '^\| 2026-(08-3[01]|09-)'`
  → `window_rows.txt` (697 lines, 1,409,222 B) · archive headings `/usr/bin/grep -n '^#' _ledger_archive.md`.
- Seat attribution: `/usr/bin/grep -cE 'the [0-9]{2}:[0-9]{2}(-rotation| respawn)? seat|…'` = 16; `[W]` tag = 80.
- Severity: `/usr/bin/grep -c "^| 2026-[0-9-]* | 🔴"` per marker (fixed string; an `-oE` alternation
  miscounted emoji and was discarded).
- Types: `awk -F' \| ' '{print $3}' window_rows.txt | sort | uniq -c`.
- Bytes: `git -C /Volumes/DevMASTER/WEDNESDAY log -1 --before='2026-08-31 00:00'` → `7f8ab76f6`; `git cat-file
  -s <sha>:0_Brain/learnings/<file>` at that sha and HEAD; `git log --since='2026-08-31 00:00' --numstat
  --format= -- <five files>`; commit count via `git log --format=%h -- <files> | wc -l`.
- Digest sizes over time: `git log -1 --format=%H --before='<date> 23:59' -- _boot_digest_by_tier.md` then
  `git cat-file -s`.
- Families: `awk -F' \| ' '{print $5}' window_rows.txt` then split on `[[`, strip `|alias` and `#anchor`,
  dedupe per row, `sort | uniq -c | sort -rn` (strict); loose = same over the whole row, links matching
  `^2026-` only.
- Enforcement phrases: awk over each row for `/[Ee]nforcement candidate[^|]*/`, cut at the next sentence,
  printed with the row date → `enforcement_candidates.txt` (49 phrases in 42 rows).
- Lesson census: `ls 2026-*.md | grep -vc conflict_on_`; `head -12 | grep '^tier:'` per file; `status:` the
  same way; bytes `wc -c`; per-tier sums by awk.
- Boot ctx: python over `daily/2026-0[89]-*.md` matching `Statusline after the brain load|Boot \(measured\)|
  Boot, measured|BOOT COST MEASURED|Brain load MEASURED` and `ctx:?\s*\**\s*(\d{1,2})%` on the same line;
  file:line kept.
- Retrieval: `comm -23 all_lessons.txt cited_loose.txt`; cross-check per never-cited name with
  `grep -c` over window daily notes, Tuesday's two ledger files (count only), and other lesson files.
- Board: `fleet/board_count.sh linear LINEAR_API_KEY '<filter>'` for every total quoted (filters copied
  verbatim in the measurements file §5, including the instrument predicate and the `zzqqxx` control);
  full walk for lists: GraphQL `issues(first:250, after:$cursor, includeArchived:true, filter:{team:{key:
  {eq:"KS"}}})` with `pageInfo.hasNextPage` (5 pages, 1,137 issues) → `ks_issues.json` (no key stored);
  predicates, closed list, reconstruction and duplication pairs by python over that file (word predicate
  `\b(term)s?\b`; duplication = ≥4 shared title words after a stop-list, or a shared `*.ts|sh|py|md…` path;
  union-find for clusters).
- Rituals: `/usr/bin/grep -ciE '23:00 close|close bell'`, `'WRAP CHECK'`, `'WRAP CHECK[^.]{0,60}(FAIL|…)'`
  per daily note; rotate log filtered to window dates → `rotlog.txt`, then `grep -c` per line class
  (`respawned OK (--self)`, `respawned OK (--dead)`, `REFUSED`, `[liveness]`, `LIVENESS FAIL`).
- Mechanism existence: `/usr/bin/grep -ciE '<predicate>' <tool>` per row-named mechanism (§7 of the
  measurements file; the non-zero rows in the same run are the positive controls).

**Could not measure:** rows per seat (rows do not name seats) · retrievals of a row by a later seat (no
instrument) · product-defect count on the board (no field) · the 09-07 catalogue's "ours / product / both"
split (human classification, not re-run) · Tuesday's ledger content (another client's seat — counted, not
read).

## Wednesday's review (2026-09-14 07:3x AEST) — what was checked, what was decided, what goes to Kam

**Checked at source by Wednesday, same action:** KS active 108 (`board_count.sh`, 07:00) = the draft's 108; backlog re-derived by a different partition (createdAt < 2026-09-01: **51**; ≥ 2026-09-01: **221**; the single-filter query paged past the cap and refused a total) = 272, so **380 open holds**. The DEAD-respawn line (9 respawns, 2 false kills) matches `rotate_wednesday.log` as Wednesday read it at boot. Not re-derived: the 697-row / 1.41 MB ledger figures, the 36 families, the 55 closed instrument tickets (the measurements file carries the commands; a later seat can re-run one).

**Decided inside Wednesday's authority (reported, not requested):**
- Promotions **15** (a boot-prompt line + a pretooluse check flagging a multi-word quoted `grep`/`grep -c`/`grep -q` without `-i`) and **3** (the `predicted-by` column on the QA template's tamper table) are commissioned to a Wednesday-assistant agent today; **17** becomes a boot-prompt line ("note stamps come from `tools/note_entry.sh`"). The rest stay tabled with their weights.
- Kam-decision item **4** (the WRAP CHECK reads the template placeholder, so it fails on every multi-seat day): fixed as option (a) — the check reads the day's LAST retro block — commissioned with the same agent; it is Wednesday's own tool and a check aimed at the wrong property, not a ritual change.
- Kam-decision item **5**: Wednesday's reading of the 2026-08-10 no-merge ruling — **appends and cross-links are allowed; merges, cuts and wholesale rewrites are not** — applied from today and stated to Kam on the panel; his word corrects it. The four supersede/merge PROPOSALS in this note are NOT executed.
- Item **3** (a retrieval instrument): option (b), a separate `_retrievals.md` — deferred to the next consolidation with a design; nothing built.
- Item **2** (P-tier for grants/contemplations): NOT taken — a text Kam wrote as a grant is loaded whole until he says a handle is enough; his to say, raised as one line on the panel, no card.

**To Kam, as ONE card:** item 1 — the Secuura board's 31 mechanical duplicate clusters (88 tickets) and the 25.8 % instrument-subject share; recommendation (b), a read-only dedupe proposal list by a Secuura seat for Peter/Stuart to decide, plus the creation-side question (c) as a question to Peter through Kam. Card id: `secuura-board-dedupe-31-clusters`.

**Both due consolidations (09-06, 09-13) are discharged by this note.** Next: the first session after Sunday 2026-09-20.
