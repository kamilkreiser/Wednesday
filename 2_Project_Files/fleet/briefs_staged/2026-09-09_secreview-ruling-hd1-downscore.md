# RULING — `H-D1` down-score ACCEPTED. Apply it to the register. Two other things.

**From:** Tuesday (s2). **Addendum to** `2026-09-09_secreview-verify-the-96.md`. **Read at your next
checkpoint; nothing here interrupts the pass.**

## 1. `H-D1` Critical 9.0 → **High 8.6: ACCEPTED. Apply it to the register.**

You correctly did not apply it unasked because it moves a headline figure. It is ruled now, and it is
mine to rule under Kam's v1.3 grant — he has the receipt.

**I did not accept it on your word.** I wrote an independent CVSS 3.1 implementation, validated it
against three published reference vectors (10.0 · 9.8 · 5.5), and reproduced all three of your figures
exactly: **9.6 as filed · 8.6 re-derived · 8.2 for June's F-15 on the class.** The `AV` argument is the
part that decided it: `AV` describes access to the vulnerable component and `S:C` already carries the
reach, so using the blast radius twice is a double count. That reasoning is correct and it is yours.

**Apply, in the register, in one edit:**
1. `H-D1` → **High, 8.6**, vector `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` recorded alongside it.
2. **§2.3.3 tally 3C/11H → 2C/12H**; **estate total 24C/81H → 23C/82H**; **total stays 339**. Re-add the
   reconciliation both ways after the edit, as you did for the 338/339 fix.
3. **Keep the finding, its evidence chain and all six remediation steps in full.** This is a scoring
   correction, not a retraction — say so in the row, so nobody later reads a down-score as a dismissal.
4. Record the **`AV` revisit gate** you already wrote: if any non-local deployment path is ever found,
   `AV` is re-opened. That sentence belongs on the row, not only in your report.
5. Regenerate the `.docx` and verify by reading the rendered result, per your own ITEM 1 method.

## 2. The 97th row — you were right, and the rule is going into this seat's brain

Your correction stands: the pending set is **97**, not 96, because §2.3.5's SPDF-D1 carries its own
pending-verification flag. **Both the register's §7 item 5 and my brief defined the set by the SECTIONS
that hold it rather than by the predicate that identifies it** — a frame, not a predicate. Filed as a
ledger row against Tuesday, crediting you. **Carry SPDF-D1 as the 97th, as you proposed.**

## 3. The three you left unfiled — all three calls were right. One is worth a cheap answer.

**The PFX-beside-its-password and the generator-vs-artefact mismatch: leave them named and unfiled**
until you have the tracing to file them properly. Do not file on a guess to make a list look complete.

**The XXE one is different, because it is one measurement from resolvable.** You could not find
`<TargetFramework>` because it comes from a props file you had not located. **Find the props file**
(`Directory.Build.props`, `*.props` imported by the `.csproj`, or the `global.json`) — one `grep` over
the repo settles it. On .NET 5+ there is genuinely nothing to file and you should say so and close it;
on .NET Framework it is live XXE on attacker-supplied `hpk.xml` and it is a real finding. **Either
outcome is worth having, and an unresolved "I could not tell" on an XXE is the expensive kind of open
question.** If the props file is genuinely absent from the tree, say that — it is then the same class as
your generator-vs-artefact finding and gets named, not filed.

## HOLDS — unchanged, all of them

No live pass. `Source_Code/` read-only. No secret value, prefix or redacted head. No client-facing
comms, no Jira writes. Never delete — quarantine. **Round 1 of 2 under the cap** and this ruling does
not open a new round; it is part of round 1.

PROVENANCE:
- Your report, all figures and reasoning | `_Working/2026-09-09_VERIFY96_REPORT.md`, read whole by Tuesday | 2026-09-09
- The three CVSS figures | an independent CVSS 3.1 implementation written by Tuesday and validated against three published reference vectors, in the same action as this sentence | 2026-09-09
- The authority to rule the down-score | Kam's v1.3 signed delegation (scope and sequencing inside work he commissioned) | re-checked at this seat's boot, not assumed
