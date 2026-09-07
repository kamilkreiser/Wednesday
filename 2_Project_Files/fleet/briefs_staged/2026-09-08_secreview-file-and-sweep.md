# BRIEF — Datasec / Security Review, 2026-09-08. **Kam ruled this himself at ~07:1x: "go ahead with option a".** Two jobs, both bounded. Nothing else.

## BLUF
1. **File the 22 delta findings from 2026-09-07 into the Consolidated Findings Register.**
2. **Finish the missing-`Bearer`-scheme sweep** across CypherSharePoint, MailFlow and UniversalPrint.
**That is the whole commission.** It is what Kam approved and it is deliberately narrow — do not widen
it without coming back to Wednesday.

**Read first, in full:**
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/_Working/delta-review-2026-09/_BATCH2_REPORT.md`
and its five component files in the same folder. The previous session's `_Working/PROGRESS.md` carries
the open list.

---

## JOB 1 — file the 22 into the register, and do NOT break its headline doing it
**Target:** `Deliverables/13_Consolidated_Findings_Register_2026-09.md` (the register is a DOCUMENT;
the previous session was correctly read-only on Jira and nothing here changes that).

**Verified by Wednesday before this brief, so you can start from measurements rather than re-count:**
- The 22 exist and reconcile: `grep -h "^### D-"` across the four delta files returns **22**;
  `grep -h '^\*\*Severity:\*\*' | sort | uniq -c` returns **4 High · 4 Medium · 7 Low · 7 Informational**.
  Both re-derived by Wednesday in the same action as writing this brief.
- The register **does not know about them**: `grep -cE 'D-OD-|D-TM-|D-CVL-|D-CC-'` returns **0**.
- The register currently states an **ESTATE TOTAL of 219** (31 June + 188 new).

🔴 **THE CONSTRAINT, AND IT IS THE POINT OF THIS JOB.** The register's line 15 reads:
> **VERIFICATION IS COMPLETE — see §2.1. 149 findings re-derived at source by independent verifiers;
> ZERO refuted.**
**That sentence has no frame on it.** The 22 delta findings **have not been independently verified** —
they were written by one session and nobody has re-derived them. **If you file them into that register
as it stands, you make its headline false**, and a reader who stops at the BLUF will believe 241
findings are verified when 22 are not.

**So filing has two halves and the second is not optional:**
- **(a)** add the 22 with their severities, evidence paths and a status that says plainly they are
  **filed, pending independent verification**;
- **(b)** **amend line 15 and §2.1 to carry their frame** — verification is complete *over the 149
  re-derived in the re-run*, and the 22 delta findings of 2026-09-07 are filed and **not** in that set.
**Every total you touch must reconcile after the edit** — 219 + 22 = 241, and the per-severity table
must sum to it. **Re-read the totals off the document after editing; do not carry them forward from
this brief.** State the arithmetic in your report.

**Do NOT verify the 22 yourself as part of this job.** That is a separate commission and Kam has not
approved it — filing them honestly is what he approved. If you think verification should happen next,
say so in your report and Wednesday will put it to him.

## JOB 2 — finish the Bearer sweep
The previous session found a **missing-`Bearer`-scheme defect in TWO siblings** and recorded that it is
*likely* in **CypherSharePoint / MailFlow / UniversalPrint — not checked.** Check them.
- **Search by SHAPE, not by the word.** A name-grep found half the instances of a different defect on
  this fleet last night; look for the header construction, not for the string `Bearer`.
- **State your frame** — which repos, which extensions, which paths — in the sentence that carries any
  "none found" result. **A zero needs a positive control**: prove your search finds the two known
  instances before you believe it does not find a third.
- Anything found is a **new finding**, filed the same way as job 1 (with the same pending-verification
  status), not folded into an existing one.

## WHAT IS EXPLICITLY NOT IN SCOPE
- **No verification pass** on the 22 (see above).
- **No live cloud pass.** It is blocked on the tenant question `fc05dcdd` vs `0c57ab37`, which the
  workspace `CLAUDE.md` marks **UNRESOLVED — do not assert which.** Kam's call, not yours.
- **The two severity-gating questions stay open**: the CVL print-source storage location (D-CVL-02 is
  Medium **on an assumption**; external would make it High) and MailFlow's `error.codeLink` origin.
  **If job 2 happens to answer the MailFlow one, say so — but do not go looking.**
- **RD-18's Privacy Act package** and **whether to re-issue the June deliverables**: Kam's decisions.
- **The HPSM credential-bearing PRD** is already on Kam's desk as a card; leave it.

## HOLDS — the previous session observed all of these and so do you
- **Read-only on `Source_Code/`** — nothing under it created, modified or deleted.
- **Static only** — nothing built, executed, flashed or networked. No device, no card, no tenant,
  **no `az`**. **Datasec has NO production grant.**
- **Read-only on Jira.**
- **No secret value copied** — report secrets as file, line, variable name and credential class only.
  Never a value, never a prefix of one.
- **Never delete — quarantine.** Nothing needed it last time.
- **FOUND / TESTED / HOW** on every finding, with the controls named under HOW, and **state what you
  did NOT test**. **NAME THE FRAME** in every completeness claim.
- **Count the CAUSE, never the damage**, and **read why a GREEN is green** — a zero from a broken
  instrument looks identical to a zero from a clean estate.

## REPORTING — read this, the channel is unusual
**This project has NO fleet inbox.** `send_brief.sh` will refuse it and the previous session recorded
that correctly. **So your report IS the deliverable, on disk**, under `_Working/`, and you name its
path. Wednesday reads it there.
**If you need Wednesday mid-session**, write the question into `_Working/PROGRESS.md` and say so in the
pane — Wednesday reads the pane. **Do not wait silently.**

## PROVENANCE
- Kam's approval | Kam, in conversation with Wednesday at ~07:1x AEST 2026-09-08, verbatim: "go ahead with option a" — where option (a) was stated to him as "launch a Security Review session to file the 22 findings and finish the Bearer sweep" | read 2026-09-08
- The 22 findings, the 4H/4M/7L/7I split, that the register carries 0 of them, and the ESTATE TOTAL of 219 | `grep -h "^### D-"`, `grep -h '^\*\*Severity:\*\*' | sort | uniq -c`, and `grep -cE 'D-OD-|D-TM-|D-CVL-|D-CC-'` over the delta folder and the register, all run by Wednesday in the same action as writing this brief | read 2026-09-08
- The register's unframed "VERIFICATION IS COMPLETE" at line 15 | `grep -n` on /Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/Deliverables/13_Consolidated_Findings_Register_2026-09.md, read by Wednesday | read 2026-09-08
- The Bearer defect in two siblings and the three unchecked components, and the open list | the previous session's `_Working/PROGRESS.md` and `_BATCH2_REPORT.md` - that session's own words, RELAYED, not re-derived by Wednesday | read 2026-09-08
- That the tenant mapping is unresolved | /Volumes/KK_T9_External_HDD/CLAUDE.md, hard rule 4 - the workspace's own file | read 2026-09-08

SELF-CHECK NOTES: the scope is exactly what Kam approved and the out-of-scope list names the things a reasonable agent would otherwise fold in; the register's unframed completeness claim is made a condition of filing rather than left to be discovered, because filing without it would make a true document false.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 07:20
