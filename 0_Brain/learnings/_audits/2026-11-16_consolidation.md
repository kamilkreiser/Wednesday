---
date: 2026-11-16
type: audit
source: weekly consolidation, CATCH-UP for 2026-10-19 .. 2026-11-15 (28 days; the 10:0x Wednesday rotation seat, from the measurement DRAFT)
status: live — for Kam to skim; nothing here takes silent effect
---

# Consolidation 2026-11-16 (catch-up over four missed Sundays, again)

**Measurements:** `_audits/2026-11-16_consolidation_DRAFT.md` (a measurement drafter commissioned by the 04:19 seat; every
number there names its instrument and frame). This note records what Wednesday CHANGED and what is Kam's.
Scope: Wednesday's seat only (Secuura + general). No Datasec file was opened.

## 0. The headline finding: the ritual lapsed for 28 days a second time, with a doctor check in place

The 10-19 audit built a `doctor.sh` check for exactly this (lines 652-666: WARN "weekly consolidation LAPSED" when the
newest audit is over its age limit). The newest non-DRAFT audit stayed `2026-10-19_consolidation.md` for 28 days.
Measured: the audit was absent. **Not measured:** whether the WARN printed at the boots of 10-27, 11-03 and 11-10 (doctor
was not run for this note). If it printed and no seat acted, the mechanism caught it and the reading failed: a WARN in
boot scrollback is the "warning nobody acts on" shape the workspace rule already names. **Validation owed (section 4).**

## 1. Changes made (deltas, never rewrites; nothing deleted)

1. **15 live lessons that headlined a Spark rule were marked** (DRAFT 2.1; the Spark was wiped and returned to HP 2026-11-15,
   [[2026-11-15_the-spark-is-gone-checks-retired-no-local-spark-tier]]). Same delta as the 10-19 audit: status line changed,
   original headline kept verbatim. Script and dry run: session scratchpad `spark_supersede.py` (dry run, then `--apply`).
   - **SUPERSEDED (do not apply), 7** (the rule's subject was the Spark itself): `09-23_spark-kit-running-a-local-coding-model`,
     `09-23_use-the-local-model-as-much-as-possible`, `09-25_spark-calibrate-like-ornith-start-high-oversight`,
     `10-05_spark-target-50-tasks-a-day`, `10-10_today-mainly-spark-and-sonnet-double-check-everything`,
     `10-26_spark-gate-pilot-if-it-works-put-it-into-practice`, `11-12_spark-for-harness-and-token-heavy-simple-tasks`.
   - **PARTLY SUPERSEDED, 8** (every Spark clause dead; the non-Spark rest stands: an Ornith half, a Claude half, the
     routing definition, the usage band or the ticket grant): `09-25_three-tier-routing-ornith-spark-cloud-always-on`,
     `10-04_as-much-secuura-work-as-possible-spark-and-claude`, `10-08_ornith-15-replaces-10-push-it-harder`,
     `10-08_sonnet-trials-and-a-shared-model-routing-definition`, `10-09_spark-first-model-choice-is-wednesdays-after-sonnet-analysis`,
     `10-14_80-to-90pct-limited-cloud-wednesday-and-spark`, `10-18_new-account-tickets-backlog-routing-definition-spark-max`,
     `10-22_usage-is-a-guide-outcomes-over-rules-route-by-learnings`.
   - Not touched: `10-22_tuesday-sonnet-default-usage-is-a-guide` (Datasec seat; it EXCLUDES the Spark, so it states no dead rule).
   - Both digests regenerated (`boot_digest.py --by-tier` rc 0, bare rc 0). Check: "the Spark was returned" appears 26 times in
     the by-tier digest (>= 15 expected: headline + status per file).
   - **Honest cost:** the by-tier digest grew 691,468 -> 698,888 B (+7.4 KB), because the digest carries status lines and the
     new ones are longer. Marking dead rules makes the boot more correct, not smaller.
2. No merges of lessons (Kam's 2026-08-10 ruling: no reduction without evidence nothing is lost). The six candidate merges in
   DRAFT 2.3 are listed for his call only.
3. No grant moved: `2026-11-06_clear-the-secuura-board-over-one-to-two-weeks` stays live; its outer read is **Friday
   2026-11-20** (EXPIRING-GRANTS), and the next seat after that date re-asks.

## 2. The numbers (from the DRAFT; frame = Wednesday's seat, window 10-19..11-15)

| measure | this window | last window (10-19 audit) | instrument |
|---|---|---|---|
| ledger rows | 360 (12.9/day) | 255 (10.2/day) | `led.py`, both ledger files, date from cell 1 |
| ledger bytes | 401,685 B (14.3 KB/day) | 271,758 B (10.9 KB/day) | UTF-8 length of row lines |
| top-5 family share | 37% | 48% | first `[[link]]` per row |
| leading family | 08-14 representations, 54 rows | same, 46 | as above |
| families at w>=3 / REGRESSION | 14 (a floor: 329 rows carry `+1` with weight in prose) | | weight cell + prose |
| new lessons | 28 (85 KB) | 40 (112 KB) | `git log --name-status` |
| by-tier digest | 620,572 -> 691,468 B (+11.4%) before this audit's edit | +17.0% | `git show <sha>:<path> | wc -c` per Sunday |
| ctx after boot load | 33-52% (full loads) | 21-42% | regex over daily notes (prose; misses some days) |
| KS board open | 770 (204 instrument-titled by word, 26.5%) | 380 / 25.8% on 09-14 | board_count per state + python fetch, reconciled |
| KS closed in window | 440 (132 instrument-titled) | | python fetch, createdAt/closedAt |
| KS duplication | strict 2 of 770; loose 62% (topic families) | strict 4 of 410 | Jaccard >= 0.5 / >= 4 shared words |
| DevMASTER disk | 46% of 3.6 TiB (new drive) | 91% of 1.8 TiB | `df` |

## 3. For Kam (each is information unless marked; nothing waits on him)

1. **The KS board doubled since 09-14 (380 -> 770 open), while 440 tickets closed in 28 days.** The instrument share is flat
   (25.8% -> 26.5%), so the growth is not the fleet filing tickets about its own tooling faster than before. Whether
   product defects fell is not measurable from titles. His 09-07 ruling (decided by outcome) stands; no proposal.
2. **The boot is heavier (33-52% context after the load) and the digest is 699 KB.** The 09-23 audit said halving it needs
   retiring whole rules, which is his call. No proposal today beyond the dead-headline marking above.
3. **About 570 GiB of local-model files (sum of the three classes below, one of them estimated by subtraction) remain on DevMASTER from the Spark and the Studio era** (`local-model/spark-ab`
   146.9 GiB, `local-model/spark` ~260 GiB by subtraction, two unused models in `tools/omlx/models` 163.8 GiB). The drive
   is at 46%, so nothing is urgent. **Proposal (a card only if he wants it moved):** offload through `tools/nas_offload.sh`
   to a dated DEV-Working folder; never deleted. Default: nothing moves.

## 4. Owed by Wednesday (mechanisms; WED work, claimed before starting)

The DRAFT found **five promised mechanisms, none built and armed**, in three families at w>=3:
1. **Arm `seat_mail_watch.sh` from the launcher, with a `doctor.sh` check that it is armed** (mail-lapse family, w=3 REGRESSION
   on 11-15). Measured today: `grep -c seat_mail_watch` = 0 in `Launch_Wednesday.command` and in `doctor.sh`. Every seat arms
   it by hand from the pickup today.
2. **A PreToolUse advisory on fleet write tools called with `--help`/`-h` or a flag absent from their usage header**
   (invoke-to-read, w=3 TODAY: 01:04, 04:4x, 07:19).
3. The note-alone hook (send_brief + note_entry in one Bash call), the `decision_queue.sh` stub-add guard, `wed_push.sh`.
4. **The doctor consolidation WARN must reach a reader**: validation owed at the next Sunday boot (2026-11-22): did the
   WARN print, and did the seat act? If a WARN printed for three weeks unread, the fix is to put it on Kam's panel or the
   morning card, not to write a louder WARN.

Next consolidation: the first session after Sunday 2026-11-22.
