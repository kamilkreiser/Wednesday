---
date: 2026-09-08
type: reference
source: two WhatsApp screenshots from Peter, relayed by Kam 2026-09-08 ~07:5x. Images at ~/Downloads/WhatsApp Image 2026-09-08 at 02.19.33.jpeg and 02.20.40.jpeg
status: live
---

# Peter's two queues, transcribed 2026-09-08 — Kam: "make sure that we action these before the end of the day"

**These are TRANSCRIPTIONS of screenshots. Every row is Peter's claim, not a measurement.**
Verify each against GitHub + Linear before acting. Times in the images are Peter's local rendering.

## TABLE 1 — "Your own PRs — awaiting Kamil" (Peter's PRs; we owe review/approval)
| PR | Ticket | Suites | Peter's last | Status (verbatim) |
|---|---|---|---|---|
| #900 | KS-971 (2/2) | false | today | CLEAN · 0 approvals — slot-isolate the k6 harness, proven by fault injection |
| #899 | KS-971 (1/2) | false | today | CLEAN · 0 approvals — observability stack tells the truth about the slot |
| #896 | KS-682 (2/2) | false | today 12:58 | CLEAN · 0 approvals |
| #895 | KS-682 (1/2) | false | today 12:58 | CLEAN · 0 approvals |
| PS #783 | — | n/a | none | CLEAN — sync the test-discipline skill |

## TABLE 2 — "Waiting on Kamil" (older; several are UNANSWERED QUESTIONS, not code)
| PR | Ticket | Suites | Peter's last | Hold (verbatim) |
|---|---|---|---|---|
| #785 | — | false ⚠ runtime | 3 Sep 13:49 | approval at `878081e98`, head `a27b3f9b3` |
| #793 | KS-365 follow-up | false | 3 Sep 08:36 | amended for QA F-5/F-6. **DIRTY** |
| #773 | QA F-1/3/7/8/10 | false | 2 Sep 14:05 | config-surface walk |
| #768 | — | false | 1 Sep 13:10 | routing to `main` is the real fix |
| #750 | — | false | 1 Sep 10:32 | your "close it" ask unanswered. **DIRTY** |
| #758 | KS-711 | false | 31 Aug 12:32 | the `2.22.2` pin disagreement |
| #728 | KS-671 | false ⚠ runtime | 31 Aug 12:25 | wouldn't have caught KS-670 |
| #721 | KS-660 | false | 31 Aug 13:01 | your framing point unanswered |
| #720 | KS-487 | false | 31 Aug 14:03 | baseline needs re-run. **DIRTY** |

## CROSS-CHECK against s149's independent measurement (2026-09-08 07:4x, `gh api ... --paginate`)
- s149 measured **45 open PRs**; "approved but STALE (approval not at head): #785 and #806".
  **Peter's row for #785 says the same thing in different words** — approval at `878081e98`,
  head `a27b3f9b3`. **Two independent instruments agree**, which is the control on this transcription.
- s149 measured **conflicted/dirty: #720, #750, #793, #806, #880.** Peter marks #793, #750 and #720
  DIRTY. **Agrees on all three that overlap.**
- **#895/#896/#899/#900 and PS #783 do NOT appear in s149's "approved at head" set** — consistent
  with "0 approvals": they are waiting on US to review, not on Peter.

## THE SHAPE OF THE WORK — 14 items, and they are NOT all the same kind
1. **Needs OUR review/approval (5):** #900, #899, #896, #895, PS #783. Peter's own work, clean, zero
   approvals. **The author merges, so we approve and Peter merges.**
2. **Needs a CONFLICT RESOLUTION first (3):** #793, #750, #720 — DIRTY, cannot merge as they stand.
3. **Needs an ANSWER from us, not code (4):** #750 ("your 'close it' ask unanswered"),
   #721 ("your framing point unanswered"), #758 (the `2.22.2` pin disagreement), #768 ("routing to
   main is the real fix"). **These are the ones that have sat longest — 31 Aug to 1 Sep.**
4. **Needs a re-run / walk (2):** #773 (config-surface walk), #720 (baseline needs re-run).
5. **Stale approval (1):** #785 — approved at a SHA that is no longer head. Re-review or re-approve.
