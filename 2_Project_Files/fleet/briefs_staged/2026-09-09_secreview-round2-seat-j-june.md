# SUPPLEMENT — SEAT J, the JUNE BASELINE. What is different about this partition.

**Read the shared method brief first** (`2026-09-09_secreview-round2-parallel-method.md`). Everything in
it binds you. This file carries only what June adds.

## KAM'S RULING, verbatim, 2026-09-09

> *"extend the scoring pass into the June baseline"*

Ruled `extend` on card `secreview-estate-wide-scoring-pass-including-june`, recorded in the queue at
11:40. **He was told, in the card, that this could raise the estate Critical count and that it re-opens
a deliverable already signed off. He ruled it anyway.** So the answer being uncomfortable is not a
reason to soften it — it is the reason he was asked.

## WHY THIS PARTITION IS THE HIGH-STAKES ONE

**June was signed off three months ago and somebody may still be relying on it.** Every other seat is
correcting a working document. **You are correcting a delivered one.** Two consequences:

1. **Precision matters more here than anywhere.** A row you move wrongly is a row we have to un-move in
   front of whoever received that report.
2. **This partition can move severities UP**, which none of the others is likely to. An under-scored
   Critical in a signed-off security report is the expensive direction.

## WHAT TUESDAY HAS MEASURED, so you do not start from zero — and one correction to round 1

`Deliverables/03_Findings_Register.md`: **31 findings, F-01…F-31, 6C / 14H / 9M / 2L as filed. All 31
carry a full `CVSS:3.1/…` vector string** — which is more than the 2026-09 register can say, and it
makes June the better subject for this method rather than the worse one.

**Three rows whose own filed vector crosses a band boundary. Tuesday computed these independently, with
four published reference vectors as controls, in the same action as writing this line:**

| ID | Filed band | Filed number | Its own vector computes | Band from that vector |
|---|---|---|---|---|
| `F-07` | High | 8.7 | **9.2** | **Critical** |
| `F-10` | High | 8.2 | **9.4** | **Critical** |
| `F-22` | **Medium** | 7.7 | **9.0** | **Critical** |

🔴 **CORRECTION TO ROUND 1, and take this one from here rather than from its report:** round 1's table
recorded `F-22` as filed **High** 7.7. **The June register says Medium** (its severity table at line 45,
and the row's own header). **So `F-22` is wrong twice over: it carries a High-band number (7.7) under a
Medium band, on a vector that computes Critical.** Round 1's *computed* figures are all three exactly
right — Tuesday reproduced 9.2, 9.4 and 9.0 independently — only its reading of `F-22`'s filed band was
wrong.

**None of that is a verdict.** It is arithmetic showing the documents disagree with themselves. **The
vector is the thing under test**, and on at least one of these the vector may be the wrong half: `F-07`'s
own scoring note argues `AV:L` deliberately, from the on-device attack surface. **Read the code.**

## THE ONE CHEAP SWEEP TO DO FIRST

`F-22` shows the **declared band contradicting its own printed number** — the same defect class round 1
found four times in the 2026-09 register. **Check all 31 June rows for it before anything else.** It is
one pass over the file, it needs no source reading, and it tells you immediately whether June has a
systematic banding habit or one slip.

## WHAT IS YOURS AND WHAT IS NOT

**Yours:** `Deliverables/03_Findings_Register.md`, all 31 rows, and the source trees they name.
**Not yours:** every row of the 2026-09 register — seats A, B, C and D hold those and are live now.
June covers 19 of the 32 components, so you will read source trees another seat is also reading.
**That is fine: `Source_Code/` is read-only for everyone.** Never comment on their rows.

**Write to `_Working/verification-2026-09/round2-june.md`. Edit NEITHER register.** June's 31 findings
are part of the estate's 339, so a band that moves here changes the estate split — **say what it changes;
seat A applies it.**

## THE HONEST QUESTION TO ANSWER AT THE END

**Was June's scoring systematically wrong, or wrong in three places?** Kam ruled `extend` partly to find
out. If the answer is "the vectors are sound and the numbers were transcribed badly", that is a very
different remediation from "the vectors were generous". **Say which, and say what you did not test.**
