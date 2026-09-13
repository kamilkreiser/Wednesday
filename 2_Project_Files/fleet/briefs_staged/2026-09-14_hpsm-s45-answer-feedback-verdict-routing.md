BLUF. **The feedback gate on `d0466da` returned DELIVERABLES: GO WITH FINDINGS · SECURITY: GO WITH FINDINGS** (verdict 15:07:27Z, DKIM pass). Tuesday read the report whole.
- Counts on the feedback surface: 0 Blocker, 0 Major; 5 Minor (one KNOWN, re-rated) and 3 Polish.
- **Live-GO condition (1) is MET.**
- **None of its findings blocks the live upgrade.** Put all of them in BACKLOG, as listed below.
- **One new live condition (C5, below).**
- **The GO still waits on the delta gate for `b9c6464`**, now being prepared. HOLD unchanged.
- Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-d0466da-feedback-tier1/report.md` (§1 findings, with fix-shapes and regression tests).

## NEW LIVE CONDITION C5 (gate curio C5)
- An invalid `PC_FEEDBACK_RETENTION_DAYS` stops the api at start, a full outage. Measured by the gate: `0`, `36501`, `abc`, `007`, `-5` and `1.5` each exit 1.
- **Before each live deploy, read whether the live env file sets `PC_FEEDBACK_RETENTION_DAYS`.**
  - Absent is fine (it defaults to 365).
  - Present is fine only as a whole number from 1 to 36500 with no leading zero.
  - Anything else STOPs before deploy, with a mail.
- **Record the reading in the REPORT. Never print any other env value.**

## BACKLOG entries (none is a live blocker; you choose the lanes after the live upgrade, and none takes a docker step before the REPORT)
- **FB-S-m1 (Minor, first among these):** a credential-shaped `Idempotency-Key` is stored in `pc.feedback_item` AND in the append-only audit chain. That is permanent once written. `createEngagement` shares the class. The live exposure until it is fixed is low: the web client always sends `feedback-<32 hex>`.
- **FB-S-m2 (Minor):** attachment contents are not scanned (a `.log` carrying `password=` is stored). It is a design gap, and NexusAI has it too.
- **FB-D-m2 (Minor):** U+0000 in title, description or admin_notes answers 500 (pg 22021). It is product-wide (an engagement name too), and BACKLOG has no entry for it.
- **FB-D-m1 (Minor):** platform_admin and content_manager with no membership, the default, see a Feedback button that always gets 422.
- **FB-S-m3 (Minor, KNOWN, re-rated, L52):** api memory 79 -> 182 -> 295 MiB peak, and still 146 MiB 22 minutes later.
- **FB-D-p1 (Polish):** "HPSM" and developer wording on the no-tenant refusal banner, against naming (b).
- **FB-D-p2 (Polish):** C0 control characters are stored in titles.
- **FB-D-p3 (Polish):** the MUTANT-3 file-name sanitiser removal survives the feedback DB suites.

## For your records, stated plainly
- **Row 6 of this report says "PASS for every listed field", page path included.** Its shape set did not include the space- or quote-separated shapes G45 then found stored. **Do not cite this report as evidence that `page_url` scanning holds.** The delta gate measures that on `b9c6464`.
- **Its C3 (a quote in a file name, "real browsers percent-encode quotes… not tested")** is the path G45's second defect sits on.

## Unchanged
- HOLD for Tuesday's GO naming `b9c6464f73e8d7199152a1f9b0d04b9cd8894b0a`. It needs the delta gate's verdict (no Blocker or Major) first.
- The 14:13:38Z conditions, plus C5. No push. Do not contact either gate.
