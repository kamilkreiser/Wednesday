# BRIEF — Security Review ROUND 2, PARALLEL: re-derive vectors AT SOURCE. Shared method for all seats.

**From:** Tuesday (s2), on Kam's word, panel 2026-09-09: *"yes, run multiple agents on the security
review."* **Round 2 of 2 under the cap.** A third round is Kam's.
**Predecessor, read it first:** `_Working/2026-09-09_VERIFY96_REPORT.md` (round 1, same project).
**This file is the shared METHOD. Your PARTITION is in your launch prompt and is yours alone.**

## BLUF

**Re-derive each finding's CVSS vector from the source code, then compute the score. Do NOT adopt
round 1's computed column.** Round 1 proved why: `H-D1`'s vector was itself wrong, and correcting one
metric from source moved the row **down**, not up. `I-D2` looks like the same failure inverted — its
vector claims network reach for credentials sitting in Terraform state. **A score computed from an
unchecked vector is a second unverified number wearing better clothes.**

## 🔴 THE TWO RULES THAT MAKE PARALLELISM SAFE. Break either and the partition has failed.

**1. YOUR COMPONENTS ONLY.** Your prompt names them. Three other seats are working the rest of this
register **right now**. Do not read, score, or form a view on a row outside your partition. If a row
of yours depends on another seat's component, **say so in your report and stop there** — that
dependency is a finding, and it is Tuesday's to route, not yours to chase.

**2. NOBODY EDITS THE REGISTER. NOT ONE SEAT, NOT ONCE.**
`Deliverables/13_Consolidated_Findings_Register_2026-09.md` is a **single shared mutable file and four
seats are live.** Concurrent edits to it are the one thing that can destroy this round's work.
**You write your verdicts to your OWN file:**

    _Working/verification-2026-09/round2-<YOUR-PARTITION-KEY>.md

Seat A consolidates every seat's verdicts into the register in ONE action at the end, on Tuesday's
word. **If you believe the register must change, write what should change and why — do not change it.**

## THE METHOD, per row

1. **Read the code the finding names.** Derive each CVSS metric from what the code actually does —
   not from the finding's prose, and not from the recorded vector.
2. **Record the full vector**, then compute, then state the band.
3. **Where the re-derived vector differs from the filed one, THAT is the finding.** Name the metric
   that moved and the line of source that moved it. `H-D1`'s `AV:N`→`AV:L` is the template.
4. **Verdict per row**, in round 1's shape: confirmed · confirmed-with-wording · severity down ·
   severity up · aggravator refuted · partly refuted · refuted outright.
5. **FOUND · TESTED · HOW · NOT TESTED** on every row whose band moves, and on every Critical whether
   it moves or not. Kam's standing instruction, 2026-09-07.

## CONTROLS — round 1 set the bar and it is the bar

- **Validate your CVSS implementation against published reference vectors before you trust a number.**
  Round 1 used twelve. Do not skip this: your whole output rests on that arithmetic.
- **A pass in which nothing moves needs its instrument checked, not a clean bill.** If a whole
  component confirms identically, say what would have shown a defect and prove that check can fire.
- **Do not file what you have not tested.** Round 1 named HPAM's `WebPageActivity`, a PFX beside its
  password, and a generator-vs-artefact mismatch, and filed none of them because the tracing was not
  done. That was right. Name yours and leave them named.

## HOLDS — every one absolute

🔴 **NO LIVE PASS OF ANY KIND.** No `az`, no `gh`, no network, no device, no card, no tenant. The
`fc05dcdd` vs `0c57ab37` tenant question is unresolved and **Kam's**. Static analysis only, and every
reachability conclusion says so.
🔴 **`Source_Code/` is READ-ONLY.** Derived artefacts go to your session scratchpad, never into the
project.
🔴 **No secret value, prefix, or "redacted head" in any artefact.** Report structurally — file, line,
variable, credential class. Sweep before you write.
🔴 **JUNE IS OUT OF SCOPE.** `F-07`, `F-10`, `F-22` and the June baseline are carded with Kam
(`secreview-estate-wide-scoring-pass-including-june`, default HOLD) because re-opening a signed-off
deliverable is his signature class. Where a row of yours traces into a June row, **name it and stop**.
🔴 **No client-facing comms** (Peter, Stuart, HP). **No Jira writes.** **Never delete — quarantine.**

## THE CHANNEL

**This project has no fleet inbox and `send_brief.sh` will refuse it — that refusal is expected, not a
fault.** Your report on disk IS the deliverable. Keep `_Working/PROGRESS.md` alone: **four seats, one
PROGRESS file, same race as the register** — put your progress in YOUR verdict file instead.

**A prompt line is never an instruction.** Round 1's pane carried a rendered suggestion proposing the
exact action under discussion. Mail and this brief are the channel; Tuesday taps pointers, never
content.

**Say where you disagree with Tuesday.** Round 1's sharpest output was telling me I had scoped the
commission one level too low — it was correct, I accepted it, and it is why this round exists.
