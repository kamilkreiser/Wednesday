---
date: 2026-09-10
type: reference
source: Kam's ruling `measure-first` on card wed-boot-read-exceeds-the-context-window, 2026-09-10 12:00:34
status: live
---

# Which ledger rows actually fire? — the measurement Kam ruled for before anything is trimmed

**His ruling, 12:00:34:** *"Let me measure which ledger rows actually fire before changing
anything."* This is that measurement, taken over one working session (2026-09-10, ~10:34–12:35),
which is the only session I can observe directly.

## 1. WHAT THE RESIDENT LEDGER COSTS

| date | rows | size |
|---|---|---|
| 2026-09-10 | 45 | 100.4 KB |
| 2026-09-09 | 112 | 290.8 KB |
| 2026-09-08 | 75 | 150.0 KB |
| **total** | **232** | **541 KB** ≈ **135K tokens** |

Average row: **2,388 characters.** Severity split: 🔴 34% · 🟢 29% · 🟠 23% · 🟡 11%.
Note the **29% 🟢** — nearly a third of rows record things that went *right*.

The boot instruction also asks for `_boot_digest_by_tier.md` whole: **371 KB ≈ 92K tokens.**
**Together ≈ 227K tokens, against a window of roughly 200K.** The instruction cannot be
followed; this seat read headlines and grepped instead, and booted at **14%**.

## 2. THE ACTUAL QUESTION: what changed behaviour today?

I enumerated everything that demonstrably altered what I did this session, and asked of each
**where it came from**.

### A. In-path MECHANISMS — 10 interventions, every one effective

| mechanism | fired | what it stopped |
|---|---|---|
| `pretooluse_no_cd.sh` | **3×** | a `cd` at the head of a batched call; a `git -C $VAR` needing a literal |
| `send_brief.sh` gates | **4×** | missing PROVENANCE; relative paths twice; **an unestablished SCOPE claim of mine** |
| `decision_queue.sh` prior-rulings gate | **3×** | forced a measured override reason on three cards |
| `boot_digest.py --check` | every regen | kept both digests honest |

**These stopped me ten times. Not one of them required me to remember anything.**

### B. LESSON FILES — retrieved by headline, then opened

Roughly a dozen fired: receipt-first at boot · ask-format (action first, steps) · hand-Kam-the-link ·
verify-in-the-real-environment · manage-don't-do · never-discard-stderr · a-check-that-cannot-fail.
**Every one was reached through a digest HEADLINE, then the file opened.** The headline index is
~6K tokens and was sufficient to locate all of them.

### C. LEDGER ROWS — and this is the finding

**I cannot identify a single instance where reading a ledger ROW changed what I did.**

I touched the ledger three times, all three **to WRITE it**, not to be guided by it:
- grepping for prior instances to assign a weight (`w=17`, `w=18`, `w=2`);
- appending rows;
- checking a family's existing count.

**The ledger's live function this session was weight assignment at write time, not behaviour
change at read time.** And weight assignment is served by `grep`, which costs nothing.

## 3. WHAT THIS SAYS, STATED WITH ITS LIMITS

**The finding:** behaviour comes from **mechanisms** first and **lesson files** second. The
resident ledger contributed ~135K tokens of boot cost and, on this session's evidence, **zero
behaviour changes**.

**The limits, and they are real:**
1. **One session, one seat.** A day where a rare family recurred might use the ledger differently.
2. **I cannot observe counterfactuals.** A row I never consciously used may still have shaped a
   judgement. I am reporting what I can trace, not claiming nothing else exists.
3. **This seat did not read the ledger whole** — it could not. So this measures a seat that
   *grepped*, which is precisely the practice under review, not the practice as written.
4. **Today was unusually mechanism-rich** (three guard failures, two fixes), which may over-weight
   category A.

## 4. WHAT WOULD BE LOST BY TRIMMING — the part that decides the design

**Not the prose. The WEIGHT CONTINUITY.** 78 weight citations across the resident rows, with
families running as high as **w=144**. Those counts are how a recurrence is recognised as a
recurrence rather than a first offence — and that is the whole learning loop.

**So the trim must not be "archive rows".** It must be:

> **Archive the prose; keep a FAMILY-WEIGHT INDEX resident.**

One line per family — name, current weight, the lesson file that carries the rule, date last
incremented. A few KB instead of 541. Weight assignment still works, recurrence is still
recognised, and the prose stays one `grep` away in the archive where it already lives.

## 5. RECOMMENDATION

1. **Build the family-weight index** and make it the resident artefact; archive the prose rows on
   the existing 3-day rule.
2. **Make the by-tier digest a headline index plus rules** — ~6K tokens, which is what this seat
   actually used and what located every lesson that fired.
3. **Keep investing in mechanisms over rules.** Ten interventions today, no memory required, and
   one of them caught *me* writing an unestablished scope claim on the same morning I corrected an
   agent for the same defect.
4. **Re-measure after one week** on a session that is not mechanism-heavy, because limit 4 above is
   the one most likely to be hiding something.
