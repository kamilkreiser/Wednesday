---
date: 2026-09-18
type: principle
source: "Measured at the 10:0x Wednesday boot: the files the boot prompt orders read WHOLE total ~886 KB ≈ 220K tokens — more than a whole context window. The boot as specified cannot be executed by the seat it is written for."
status: live
supersedes: ""
tier: W
---

# A boot read that outgrows the window is not a thorough boot, it is a dead seat

**The lesson:** Every file the boot prompt says to read WHOLE is a file that grows. Measure the
boot's total cost at every boot, and when the sum approaches the window, **fix the files — do not
obey the instruction into a dead seat, and do not quietly skim and call it a boot.** Say which
reads were bounded and why.

**Context (measured 2026-09-18 10:0x, not estimated):**

| file | bytes | ~tokens |
|---|---|---|
| `learnings/_boot_digest_by_tier.md` | 487,906 | ~122,000 |
| `tasks/NEXT-PICKUP.md` | 219,735 | ~55,000 |
| `learnings/_ledger.md` | 169,163 | ~42,000 |
| the three small ones | 10,286 | ~2,600 |
| **TOTAL** | **~886 KB** | **~220,000** |

That exceeds the context window outright. A seat that complied would hit "Prompt is too long" during
its own boot, having done no work — the same death the 06:39 seat suffered on 2026-09-02, arrived at
by obedience rather than by neglect. This seat instead booted bounded and finished the boot at
**ctx 14%**, with the fleet fed and two agents moving.

**Two of the three were bloat against rules already written, and both are now fixed:**
- **`NEXT-PICKUP.md` — 220 KB, of which 19 KB was live.** Its own frontmatter says
  `supersede: replace wholesale at the next pickup; do not append`. Sixty-two blocks had been
  APPENDED, each declaring itself to supersede every block below it, so 91% of the file was
  self-declared dead weight that every seat was ordered to read whole. Split 10:0x, 600 lines moved
  verbatim to `NEXT-PICKUP-archive.md`, conservation asserted (70 + 600 = 670).
- **`_ledger.md` — wrap rule 3c had not been run.** 18 rows dated ≤ 2026-09-15 moved to
  `_ledger_archive.md`, conservation asserted both ways (1073 rows before and after). 169 KB → 146 KB.
  **Honest limit: rule 3c barely touches this file now** — 100 of 118 rows are inside the 3-day
  window and rows run ~1.4 KB of prose each, so the ledger regrows past 3 days' worth in about a day.
  The rule addresses age; the cost is driven by row size and row rate.

**The third is a design problem and needs Kam:** `_boot_digest_by_tier.md` is **53% of the 916 KB
lesson corpus it exists to summarise**, because 144 of 182 lesson files are tier **W** (carried at
full digest-block width) against 33 tier M. WED-139 built the digest to cut boot cost; at a 53%
compression ratio it has stopped doing that. Tiering more lessons down is a judgement about which
lessons must fire cold, which is his call, not a seat's.

**How to apply:**
1. **Measure before reading.** `stat -f%z` every mandated whole-read and sum it FIRST. Bytes ÷ 4 ≈
   tokens. If the sum is a large fraction of the window, stop and bound the reads deliberately.
2. **Bound by structure, not by truncation.** Read the live head of a superseded-block file, the
   headline index of a digest, the newest rows of a ledger — then say exactly what you bounded.
3. **Report the measurement in the boot note**, as WED-139 asks. A boot cost that is asserted rather
   than measured is how this grew to 220 KB over the window unnoticed.
4. **A file whose own frontmatter states a discipline is evidence that discipline is not running.**
   Check the file against its own rule before obeying an instruction to read it whole.

**Related:** [[2026-09-02_statusline-is-the-only-context-instrument]], [[2026-09-06_a-scoped-override-carries-its-own-expiry]], [[2026-09-18_an-authorised-sweep-does-not-authorise-its-cascade]]
