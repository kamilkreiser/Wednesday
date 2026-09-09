# AMENDMENT — you are now SEAT A of four. Your partition narrows. You own the register.

**SUPERSEDES the QUEUE section of `2026-09-09_secreview-round2-vectors-at-source.md`** (items 3 and 4,
"the 91 rows, Highs first"). **Nothing else in that brief changes** — the method, the controls, the
holds and the June exclusion all stand exactly as written. Read this at your next checkpoint; it does
not interrupt what you are doing right now.

## WHY

Kam, panel, verbatim: *"yes, run multiple agents on the security review."* Three more seats are
starting now. **Your work so far is untouched and none of it is repeated.**

## YOUR PARTITION — 19 rows, and it is the highest-value one

- **HPAuthenticationManager** (8 rows) — you are mid-`D-01` and it stays yours.
- **infra_hpam** (11 rows) — `I-D1` and `I-D2`.

**That is deliberate: all three rows that would move High → Critical are in your partition** (`D-01`,
`I-D1`, `I-D2`), and you are already inside the first of them having found its `[ASSUMPTION]` about
`targetSdk`. **Everything else is another seat's. Do not read, score or form a view on a row outside
those two components** — B has the License pair, C has the client apps, D has the services plus
SPDF-D1.

## 🔴 AND YOU OWN THE REGISTER — you are the ONLY seat that may touch it

`Deliverables/13_Consolidated_Findings_Register_2026-09.md` is one shared mutable file and **four seats
are live**. B, C and D are under written instruction never to edit it; they write verdicts to
`_Working/verification-2026-09/round2-<b|c|d>.md`. **You are the single writer.**

1. **Your D-04/D-05 transcription fixes and anything you have already applied: keep them.** Done is done.
2. **From now, write your own verdicts to `_Working/verification-2026-09/round2-a.md`** like the others,
   and **do not apply anything further to the register until the consolidation.**
3. **The consolidation is one action at the end, on Tuesday's word** — you read all four verdict files
   and apply them together, re-adding the reconciliation both ways and verifying the rendered `.docx`,
   exactly as you did for `H-D1`. **Do not start it before Tuesday says so:** a seat may still be
   running and a partial consolidation is the worst of both worlds.
4. **`_Working/PROGRESS.md` is also shared by four seats now — leave it alone.** Your progress goes in
   your verdict file.

## WHAT HAS NOT CHANGED

Vectors re-derived at source, then computed — never the recorded column. FOUND · TESTED · HOW · NOT
TESTED. Validate the CVSS implementation against published reference vectors. No live pass; the tenant
question is Kam's. `Source_Code/` read-only. No secret value or prefix in any artefact. June out of
scope and carded. **Round 2 of 2 under the cap.** Say where you disagree with me.

PROVENANCE:
- The instruction to parallelise | Kam's panel message, 2026-09-09 | read by Tuesday in the same action as writing this
- The row counts per component | counted mechanically off the §2.3.3/§2.3.4 tables, 96 rows total reconciling to the register's own tally | measured by Tuesday 2026-09-09
- That you are mid-`D-01` and inside its `targetSdk` assumption | your own pane, captured by Tuesday | 2026-09-09 11:3x
