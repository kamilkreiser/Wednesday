# Correction ledger — frequency-weighted reinforcement

Design per Kam (2026-08-03, voice): *"similar to when people learn, frequency is
used for reinforcement — if a mistake happens once, that could be isolated; if it
happens more than once, an increased weight is given."*

## The weight scale

Weight = number of occurrences. Each recurrence escalates the response:

| w | Meaning | Required response |
|---|---|---|
| 1 | **Isolated** — could be noise | Log it. Write a lesson file only if it would change future behaviour (importance filter). |
| 2 | **Reinforced** — a pattern, not noise | Lesson file mandatory. If one existed and didn't fire, diagnose *why* (wrong file? too abstract? bad retrieval handle?) and fix the lesson, not just the mistake. |
| ≥3 | **Regression** — the system is failing to learn | Treat like a failing test (no-skip rule). Automatic promotion candidate: move the rule into `identity/` or into *enforcement* (launcher check, hook, CLAUDE.md line). Raise it with Kam at the next briefing. |

Rules:
- Same *underlying* mistake in a new costume still increments the weight — match
  on root cause, not surface form.
- Weights never decay automatically. They are only retired at weekly
  consolidation, with the reasoning written in the audit note.
- Positive reinforcement counts too: when Kam explicitly praises a behaviour,
  log it as `praise` — repetition there tells us what to *keep* doing.

## Ledger (newest at top)

| 2026-10-04 | 🟡 **I TOLD KAM "about thirty Secuura merges over the week" WITHOUT COUNTING; the day totals in my own notes/pickup sum to ~52 (09-27 9 · 09-28 18 · 09-29 13 · 09-30 6 · 10-01 5 · 10-02 1).** [W] Self-caught one action later; corrected on the panel with the instrument named (notes, not a GitHub recount). Zero cost beyond his attention. 🔑 [[2026-09-14_do-not-guess-a-comparison-a-citation-you-did-not-open-is-a-guess]] + [[2026-09-04_decisions-held-narration-drifted]] (no quantity reaches Kam without its measurement in the same breath). The warm-message costume: a figure in a thank-you feels like colour, not a claim. | correction (self-caught, zero cost) | +1 (no-quantity-without-measurement: the warm-reply costume) | [[2026-09-14_do-not-guess-a-comparison-a-citation-you-did-not-open-is-a-guess]] | corrected on the panel 17:4x |
| 2026-10-04 | 🟢 **PRAISE, Kam (terminal, verbatim): "thank you!  I am back from Melbourne.  Thank you for holding down the fort while I was away".** [W] For the travel week run from the live board (2026-09-27 → 10-04): Spark-first routing, every merge gated and verified at source, every decision of his carded with a default so nothing stalled on his silence. Behaviour to protect: run an away week through cards with defaults and a daily value-first receipt, and own misses plainly in the receipt. **Also:** he is BACK, so the week instruction's "while I'm away" premise has ended (the renewal card stands for him to rule). | praise | 1 | [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] | — |
| 2026-10-04 | 🟡 **I TOLD KAM (morning receipt) THAT ONE SEAT STARTS WHEN THE ALLOWANCE RENEWS ~13:30, AND NAMED NOTHING THAT WOULD WAKE ME AT THE RENEWAL; it renewed and the seat sat unlaunched until Kam's 17:4x wrap request.** [W] Self-caught at the wrap (statusline `7d:0%`). Cost: ~4 h of an owed, Kam-ruled seat (KS-1402) not started. 🔑 [[2026-09-07_an-instruction-to-wait-must-name-what-wakes]] (a wait with no wake is dormancy; here the wait was MINE) + [[2026-08-07_a-promise-is-not-a-mechanism]]. Rule: a promise tied to a clock event (a renewal, an expiry) gets its wake in the same action: a background `sleep`-until job that exits at the event, or a watcher leg. Systemise: a wake_watch leg on the 7d gauge crossing back under the cut. | correction (self-caught, ~4 h delay) | +1 (wait-must-name-what-wakes: the coordinator's own wait) | [[2026-09-07_an-instruction-to-wait-must-name-what-wakes]] | carried to the next boot as act 1 |
| 2026-10-03 | 🟡 **I WROTE A HUMAN DATE ('2026-10-04 06:00') ON LINE 1 OF `night/PAUSE_QUEUE`, the slot the runner reads as an EPOCH: the exact defect the 10-02 screen had just reported (the 10-01 file never took effect for the same reason).** [W] Self-caught one action later by reading the runner's own reader (`night_run.sh:114-135`, which documents the format and refuses an over-bound value, so it would have failed open: taps, not silence); rewritten with `date -j … +%s` and read back (`date -r` = 2026-10-04 06:00). Zero cost. 🔑 [[2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour]] + [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]] (the finding was 23 h old and I repeated it). Rule: a file with a machine-read first line is written from the reader's FORMAT comment, read before writing; the owed `pause_queue_write.sh` (refuses a non-epoch line 1) is now overdue. | correction (self-caught, zero cost) | 1 | [[2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour]] | rewritten 06:0x |
| 2026-10-02 | 🟠 **A PREMISE UNDER A CARD TO KAM WAS FALSE FOR A MONTH: the 2026-09-02 card `secuura-ks739-lookup-role-scope` option (b) said S's connector key needs only `users:read` because "K's lookup already honours it". It does not: `users.ts:266` is `authenticate()`, access tokens only, so a connector token is refused (401) before any scope is read. Kam ruled (b) on that sentence; the ruling could never take effect, and every S transfer-custody has fallen back to a flat anchor since.** [W] Client-caught (Peter, KS-1402, measured 4/4 on a local S+K pair, 2026-10-01). Confirmed by Wednesday reading users.ts:266 + :357-359 at develop 88e8877a2a0d. Cost: a month of S custody transfers unrecorded on K (no data lost: the fallback anchored). 🔑 [[2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it]] (the option detail was a mechanism claim nobody read at source) + [[2026-09-10_i-endorse-things-i-have-not-read]]. Rule kept: an option detail that says what code DOES ("already honours", "already rejects") names the file:line it was read at, or says unmeasured; a scope check is only real if the authenticator in front of it admits the token. Corrected on the new card `secuura-ks1402-lookup-refuses-connector-tokens` in its BLUF, as Wednesday's error. | correction (client-caught, latent product defect) | +1 (premise-under-a-question: the option-detail costume) | [[2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it]] | new card filed 06:0x with the correction |












**Rows dated 2026-10-01 and earlier live in [[_ledger_archive]]** (10-01 moved 2026-10-04 05:30 by seat 73252fd5 at its 05:30 wrap, 8 rows, conservation asserted; 09-30 moved 2026-10-03 05:30 by the morning seat 73252fd5 at its 05:30 wrap, 9 rows, conservation asserted; 09-29 moved 2026-10-02 05:30 by seat 79817561 at its 05:30 wrap, 11 rows, conservation asserted; 09-28 moved 2026-10-01 05:30 by the evening seat cb6b682a at its 05:30 wrap, 6 rows, conservation asserted; 09-27 moved 2026-09-30 19:14 by the day seat cab52cfa at its rotation, 6 rows, conservation asserted; 09-26 moved 2026-09-30 00:05 by the overnight seat at boot, 10 rows, conservation asserted; 09-25 moved 2026-09-29 05:3x by the overnight seat at its wrap, 15 rows, conservation asserted; 09-24 moved 2026-09-28 05:3x by the overnight seat at its wrap, 2 rows, conservation asserted; 09-23 moved 2026-09-27 05:3x by the 09-26 evening seat at its wrap, 19 rows, conservation asserted; 09-22 moved 2026-09-26 at the 05:30 shift-change wrap, 28 rows, conservation asserted; 09-21 moved 2026-09-24 05:3x by the 00:00 seat at its wrap, 22 rows, conservation asserted; 09-19 moved 2026-09-22 07:22 by the 03:45 seat at its rotation handover, 15 rows, conservation asserted; 09-18 moved 2026-09-22 03:3x by the 00:05 seat at its rotation handover, 20 rows, conservation asserted (1192 == 1192); 09-17 moved 2026-09-21 00:50 by the 23:4x seat at its 70% checkpoint, 37 rows, conservation asserted; 09-16 moved 2026-09-20 03:5x by the 03:3x Sunday seat at its 50% checkpoint, 55 rows, conservation asserted (1104 = 1104); 09-15 moved 2026-09-18 10:0x; 09-14 moved 2026-09-17 05:10 by the 05:03 seat at boot, 28 rows, conservation asserted; 09-13 moved 2026-09-16 00:49 by the 00:1x seat at its checkpoint, 24 rows, conservation asserted; 09-12 moved 2026-09-15 11:08 by the 05:3x seat at its wrap, 12 rows, conservation asserted; (09-10 moved 2026-09-13 22:1x by the 17:48 seat, 76 rows, conservation asserted; 09-09 moved 2026-09-12 10:4x at the 09:15-rotation seat's 70% checkpoint under rule 3c, 112 rows, conservation asserted; 09-08 moved 2026-09-11 05:3x; 09-07 moved 2026-09-10 05:3x at the overnight wrap under CLAUDE.md rule 3c, 71 rows, conservation asserted; 09-06 moved 2026-09-09 12:5x; 09-04 moved 09-06 08:0x; 09-03 moved 09-06 00:06; 09-02 moved 09-05 08:1x; 09-01+08-31 moved 09-04; ≤08-29 moved 08-31 and 09-02.)

**Fleet-insight and agent-credit rows dated ≤ 2026-09-05 live in [[_ledger_fleet_insights]]** (moved 2026-09-05 under WED-145 Phase 0; conserved, never deleted).



| Date | What happened (root cause) | Type | w | Lesson | Status |
|---|---|---|---|---|---|
