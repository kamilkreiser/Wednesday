# BRIEF — FINALISE: apply Tuesday's six rulings, close what is still closable, then STOP

**From:** Tuesday (s2), on Kam's word, panel 2026-09-09: *"Complete the document and finish the analysis."*
**Predecessor:** `_Working/2026-09-09_CONSOLIDATION_REPORT.md` — read it whole first; it holds the six.
**This is the finishing action. It is not a new verification round.**

## BLUF

**Apply the six changes the consolidation held, settle the one metric call worth two Criticals, and then
write the closing statement of what remains and why. Do not re-open any row that is already settled.**

The register stands at **27 C · 78 H · 119 M · 75 L · 40 I = 339**. **You will change that number. Say
what it becomes, both sums, every time.**

## 1. THE SIX HELD CHANGES — Tuesday's rulings, apply exactly as written

| # | Change | RULING |
|---|---|---|
| 1 | Withdraw `D-MF-01` (High 7.5) — premise refuted, `CloudConfig` appears zero times in the tree | **ACCEPT — as a MARKED WITHDRAWAL** |
| 2 | File the new UniversalPrint row — three auth WebViews, no origin gate, JS enabled, one receiving the printer admin password | **ACCEPT — file it** |
| 3 | Split `DELTA-MK-03` into at-rest 4.9 and shoulder-surf 4.3 | **ACCEPT** |
| 4 | Split `ADM-D3` into its five distinct configuration weaknesses | **ACCEPT** |
| 5 | De-count `DELTA-HP-01` / `-02` — the delta file's own author wrote *"not as a new finding"* | **ACCEPT — as MARKED withdrawals** |
| 6 | `ADM-D5` Low → Medium 5.3 | **ACCEPT** |

🔴 **"MARKED WITHDRAWAL" IS THE OPERATIVE PHRASE ON 1 AND 5, AND IT IS NOT A DELETION.** The row STAYS
in the document, marked withdrawn, **carrying the measurement that refuted it**. It comes OUT of the
counted total and OUT of the severity tallies. **Never delete a row and never silently drop one** —
a reader must be able to see that a finding was raised, tested and withdrawn, and why. A register that
quietly loses rows is one nobody can audit, and the withdrawal reasoning is itself evidence of rigour.

## 2. THE `UI` CALL ON `D-01` AND JUNE `F-07` — settle it, because it is worth TWO Criticals

Two seats forbidden to read each other's rows re-derived the same component independently and landed on
the **identical vector**, both Critical **9.2 only on `UI:N`**; on `UI:R` both compute **8.5, High**.

**Settle it at source, once, for both rows together** — they are the same component and the same
mechanism, so they must not receive different answers. Read what actually triggers the exported
surface: does exploitation require a human at the device to do something, or does a co-located
application reach it unaided? **Then apply the same verdict to both and say so.**

**If the source genuinely cannot settle it, say `UNSETTLED` and leave both at the filed value with the
question written on both rows.** Do not guess, and do not let the two rows diverge.

## 3. THEN CLOSE THE ANALYSIS — say what remains and why, in three named buckets

1. **Blocked on Kam** — the credential disclosure in `03_Findings_Register.md` and its distribution; the
   `fc05dcdd` / `0c57ab37` tenant question; anything needing a live pass.
2. **Blocked on access** — the HPAM client verification code, the License Portal source, the WorkPath
   bundle. Name what each would close.
3. **Genuinely finished** — say so plainly, and say what "finished" covers.

**Also apply seat J's verdict to `03_Findings_Register.md`** (the June register) — three bands, bucketing
qualifiers intact — **but `F-22` gets a written scoring note, not an improvised re-score.** Seat J
refused to move it because it is one of only two rows with no recorded intent to test against; if you
cannot write a defensible note, leave it and say why.

## HOLDS — unchanged, every one

**NO LIVE PASS.** No `az`, no `gh`, no network, no tenant, no device. Static only, and every reachability
statement says so. **`Source_Code/` READ-ONLY.** **Never delete — quarantine both formats before writing
(`.pre-finalise-2026-09-09_*`).** **No client-facing comms. No Jira writes.**
🔴 **NO SECRET VALUE, PREFIX, LENGTH OR REDACTED HEAD in any artefact you write — and do not go reading
the disclosed values in `03_Findings_Register.md` to "check" them. The disclosure is established; reading
it is the harm.**

## WHEN YOU ARE DONE

**Regenerate the `.docx` and verify by extracting the changed rows back out of `word/document.xml`** —
the last pass found three tables that had never rendered as tables, and the `.md` being right is no
defence. **Sweep the RENDERED text for secrets and report the count.**

Write `_Working/2026-09-09_FINALISE_REPORT.md` with the before/after estate table, both sums, every
change applied, the `UI` verdict and its reasoning, the three buckets, and the `.docx` verification.
**Then STOP. Do not open a new round.** Say where you disagree with Tuesday.
