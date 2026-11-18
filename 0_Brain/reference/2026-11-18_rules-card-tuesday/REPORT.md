---
date: 2026-11-18
type: reference
source: in-session claude-fable-5-2 agent commissioned by Tuesday s290 (Kam, live board 11:28:59 "Use latest fable for this work"); text returned by the agent and saved verbatim in substance by Tuesday, because the agent's Write was refused for a report file
status: live
---

# Rules card for the Tuesday seat: adoption report

## BLUF
**Adopt: YES, as a trial, with the seat ledger still read whole and the fixes in section 6 made first or soon after.**
- Why yes: card 390 lines / 103,981 B (~26 K tokens) against the by-tier digest 8,045 lines / 714,293 B (~179 K tokens), which no seat reads whole. Tools run clean; card readable whole in one pass. Of this seat's 28 ledger rows since 2026-11-12: 13 COVERED, 12 PARTIAL, 3 LEDGER-ONLY; where checked, the missing stopping rule was in no lesson either, so the digest would not have carried it.
- Why "with fixes": 14 of 28 rows happen at the kit STAMP, and the card has ONE stamp line, whose text is in no lesson file. 9 rows have neither a card line for the act nor a tool that refuses.
- Adoption is in effect started: the launcher keys on the card file existing.
- Not tested: no seat has booted on a card; this is a paper replay by one reader.

## 1. Run (12:07-12:13 AEDT, `date`)
| Command | Output | rc |
|---|---|---|
| `rules_card.py --check` | `OK: rules index clean (357 rows)` | 0 |
| `rules_card.py --seat tuesday` | `rows on card: 285  bytes: 103981` | 0 |
| `rules_card.py --check --seat tuesday` | `OK: rules index clean (357 rows, card tuesday current)` | 0 |

Counts line: 282 lessons, 357 rule lines, 285 on this card, 1 enforced, 12 dead, 23 superseded, 36 other-seat-only. Index commit 2e9a881008.

## 2. Cost
| File | Lines | Bytes | ~Tokens |
|---|---|---|---|
| `_boot_digest_by_tier.md` | 8,045 | 714,293 | 178,600 |
| `_rules_card_tuesday.md` | 390 | 103,981 | 26,000 |
| `_rules_card_friday.md` | 411 | 109,417 | 27,400 |
| `_ledger_laptop_datasec.md` (still whole) | 40 | 27,055 | 6,800 |
| Card + 10 proposed rows (dry run) | 400 | 107,135 | 26,800 |

~152,600 tokens saved per boot (bytes/4 estimate). "Most reinforced" (20 repeated lines, 6,510 B) and "Not on this card" (file lists, 4,332 B) carry no new rule: 10% of the card.

## 3. Replay of this seat's rows since 2026-11-12 (28 rows; 6 dated 11-12/11-13 were archived into the SHARED `_ledger_archive.md` lines 2228-2233)
COVERED 13 · PARTIAL 12 · LEDGER-ONLY 3. Of the 15 not covered: 6 have a refusing tool (rows 4, 8, 9, 18, 26, 27); 9 have neither (1, 5, 7, 14, 16, 19, 20, 22, 23).

Card lines quoted: A (l.43 stamp: run command literals in the consuming tool; predicted figures dry-run or removed) · B (l.75 scope words; find the card before "by ruling") · C (l.74 generated timestamps/SHAs) · D (l.296 rule a tapped card in the same step) · E (l.79 premises of a card verified) · F (l.73 facts from a same-action read) · G (l.40 a check that cannot fail).

| # | Date | Row | Grade | Card line | Tool |
|---|---|---|---|---|---|
| 1 | 11-18 | B1695 stamped as covered by a ruling whose card names another project | PARTIAL | B; `show` + client_project + option detail + read-back of an amend are ledger-only | none |
| 2 | 11-18 | jest selector in grep syntax | COVERED | A | stamp_check passed it |
| 3 | 11-18 | '06:1x' typed | COVERED | C | note_alone advisory |
| 4 | 11-18 | ALL GREEN on 1 of 7 | PARTIAL | G, l.55; "table names every job" ledger-only | --min-checks |
| 5 | 11-17 | 'product owner's default' for Tuesday's approval | PARTIAL | B; who-decided grep at the stamp ledger-only | none |
| 6 | 11-17 | '15:1x' in BASE | COVERED | C | stamp_brief refused |
| 7 | 11-17 | READ-WHOLE label doubled | LEDGER-ONLY | G only | none |
| 8 | 11-16 | stamp emptied the kit | PARTIAL | G, l.25; atomic rewrite ledger-only | stamp_check empty-kit refusal |
| 9 | 11-16 | second waiter | LEDGER-ONLY | none | tool rc 5 |
| 10 | 11-16 | tapped cards open (w=3) | COVERED (under-weighted, G3) | D | tapped_but_open.sh |
| 11 | 11-16 | 'still needs approval' already approved | COVERED | E, l.117 | none |
| 12 | 11-16 | stamp clock typed | COVERED | C | note_alone advisory |
| 13 | 11-16 | rotation stalled at prompt | COVERED | l.385 | launcher |
| 14 | 11-15 | read whole through cut -c | LEDGER-ONLY | l.45 is about mail absence only | none |
| 15 | 11-15 | wake_ack on stale STATUS | COVERED | l.301 | none |
| 16 | 11-15 | drafter for a dropped lane | PARTIAL | l.81 | none |
| 17 | 11-15 | predicted diff stamped | COVERED | A | none |
| 18 | 11-15 | gates passed, hosted CodeQL failed | PARTIAL | l.48 | CodeQL CLI |
| 19 | 11-15 | kit stopped seat 3x | PARTIAL | l.231 | none |
| 20 | 11-15 | test behaviour sentence stamped (w=2) | PARTIAL | F | none |
| 21 | 11-15 | dummy add | COVERED | l.184 | queue refused |
| 22 | 11-15 | gate finding paraphrased | PARTIAL | F | none |
| 23 | 11-13 | 'missing' digest before due | PARTIAL | l.185, l.80 | none |
| 24 | 11-13 | other client's inbox listed | COVERED | l.281 | inbox_scope hook |
| 25 | 11-13 | cause from pattern | COVERED | F | none |
| 26 | 11-12 | expected output frozen unrun (w=3) | PARTIAL | A | stamp_check hard gate |
| 27 | 11-12 | count 'once' vs twice | PARTIAL | A | stamp_check |
| 28 | 11-12 | helper named without path | COVERED | l.215 | none |

Not in any index row: the 2026-11-06 s245/s247 irreversible row (archive l.94, w=10): grep the signed SOW before carding a removal.

## 4. Index rows for this seat
- 15 rows name tuesday (13 live): mostly correct. Opus-4.8 lesson step 2 still says switch with `/model` (unsafe; the row is right). HPSM readiness grant (2026-08-12) row: "until the project starts" vs a POC being built: Tuesday/Kam to say which, then mark dead or reword.
- Wrongly excluding tuesday: `2026-09-20_ks1175-hold-lifted-make-the-fix.md` ("the note IS the ruling") and `2026-11-16_audit-records-...#2` ("state what the field HOLDS"): propose `all`.
- `2026-10-05_board-taps-suffice-for-audit-redates.md`: a Secuura grant; widening would originate authority: a card, not a row edit.
- No row anywhere for `pr_checks_wait --min-checks` or reading kits whole.

## 5. Gaps
- G1 one stamp line for 14/28 rows, no lesson behind it.
- G2 the moment-of-action print never fires on this seat's path (stamp_brief.py, stamp_check.py, brief_seat.sh, launch_when_cool.sh, pr_checks_wait.sh do not call rules_card.py).
- G3 fleet-wide weights hide this seat's regressions: line D [x5] at l.296, cut from `--at card --top 8`. In this seat's 30-day top 20 but not the card's: shared-bus tag filter (21), never-invoke-a-write-command (12), zsh PIPESTATUS (9), red-proof arms (9), parallel seats (8), two-answer question (6), wait-must-name-what-wakes (4).
- G4 a `#n` row shows the whole lesson's count (line A [x379]).
- G5 64 of 619 seat ledger rows cite no indexed lesson: their rules live ~3 days.
- G6 five families on the card have no file.
- G7 this morning's archive of this seat's rows went to the shared `_ledger_archive.md`.
- G8 enforced section truncates at 120 chars.

## 6. Proposed (none applied: shared files need a claim)
- P1 `PROPOSED-ROW-FIXES.tsv`: 10 rows (2 scope widenings, 8 new #n rows). Dry run: `--check` OK 365 rows; card 107,135 B.
- P2 one Tuesday lesson consolidating the stamp rules of 11-11..11-18; point the stamp rows at it.
- P3 advisory print in stamp_brief.py and pr_checks_wait.sh (stderr, `|| true`, `--if-card`); a `stamp` trigger.
- P4 seat weight beside fleet weight; a "this seat, last 30 days" section; `--top N` never cuts a seat REGRESSION from the last 30 days.
- P5 trim the two non-rule sections to pointers/counts (~10.8 KB).
- P6 amend the Opus-4.8 lesson step 2; decide the HPSM readiness row; archive seat rows to the seat archive; regenerate or de-reference family files.
- P7 keep the seat ledger whole; read the stamp checklist at each rotation.

## 7. Trial watch
Any ledger row whose stopping rule was in the digest and not on the card; recurrence of the stamped-text family after P1/P2; statusline ctx after the brain load, before (17% headlines-only, s289) and after.
