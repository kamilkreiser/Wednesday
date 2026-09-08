# Datasec / Security Review — FIX THE REGISTER, THEN VERIFY, THEN CONTINUE

**Commissioned by Wednesday (s150, laptop seat) on Kam's word, 2026-09-08.**
Kam, panel, verbatim, two messages minutes apart:
> *"fix the register section"*
> *"keep the verification and security review going"*

**Ordered queue. Item 1 first and alone — it is the only item that is actively
misinforming a reader today.**

---

## ITEM 1 — §7.1 of the register contradicts itself. Fix it, and regenerate the .docx.
**File:** `Deliverables/13_Consolidated_Findings_Register_2026-09.md`

**The defect, measured by Wednesday in the file at 09:5x:**
- **Line 460, the heading:** `## 7.1 DELTA REVIEW OF THE 19 PREVIOUSLY-REVIEWED COMPONENTS — 8 done, 11 COMMISSIONED (Kam, 2026-09-07 16:2x)`
- **Line 497 onward, `### Current state`:** `**COMPLETE — the June-baseline delta set is 19/19.**`
- **Line 509 onward, `### What the gap actually costs — bounded honestly`,** in the PRESENT tense:
  *"It is NOT a claim that those 11 are clean. Nobody looked for new defects in them this run"* and
  *"The 11 unreviewed components should therefore be assumed to hold findings of the same class, in
  unknown number."*

**Why it is a defect and not a matter of taste:** the `### Current state` block is explicitly framed
as an update — *"[updated 2026-09-08 — the in-flight state above is retained as the record of the
decision]"*. **That framing covers the block ABOVE it and nothing below it.** So §7.1 tells a reader
both that the set is complete and that eleven components were never reviewed, with no marker saying
which is current. **A reader who stops at the heading is told the review is a third undone.**
Wednesday confirmed the completion independently: **all eleven of the "NOT DONE" components have
delta-review artefacts on disk** in `_Working/delta-review-2026-09/` (cypheronedrive, cyphersharepoint,
teams, mailflow, universalprint, infra-hpam, license-services, licenseserver, hpk-deployment-utility,
commonvaluelibrarycypher, cyphercard-enrolment-app), and 8 + 7 (batch 1) + 4 (batch 2) = 19.

**What to do — and the constraint is NEVER DELETE, only re-frame:**
1. **The heading must state the current fact**, because the heading is the retrieval handle. Something
   the reader can act on: *"§7.1 DELTA REVIEW OF THE 19 PREVIOUSLY-REVIEWED COMPONENTS — COMPLETE 19/19
   (8 + batch 1 of 7 + batch 2 of 4); the in-flight history below is retained deliberately."* Your wording.
2. **Give the stale block the SAME framing the in-flight block already has.** The `What the gap
   actually costs` analysis is valuable history — it is *why* Kam reversed the recommendation to drop
   the eleven — so **retain it, marked as the record of the gap AS IT STOOD BEFORE THE BATCHES**, in
   the past tense, exactly as its sibling block is marked. **Do not delete a word of it.**
3. **One consolidation gap in that section IS still live and must stay live:** batch-1's findings
   (D-MF-01..06 · D-SP-01..05 · D-UP-01..06 · D-HAM-…) are narrative in §2.2 and **not counted rows**.
   That is ITEM 3 below. Make sure re-framing item 2 does not accidentally imply it is closed.
4. 🔴 **REGENERATE THE `.docx`.** `13_Consolidated_Findings_Register_2026-09.docx` was built 07:29 from
   the `.md` at 07:28. **The .docx is what ships.** An edited .md with a stale .docx is the same defect
   in a worse place. Use the project's own build path (`_Working/build-briefing-consolidated.sh` or
   whatever the project actually uses — read it, do not assume) and **state which you used.**
5. **Verify by reading the rendered result, not by trusting the build's exit code.**

---

## ITEM 2 — the verification pass Kam just authorised
**His word: "keep the verification ... going".** The 23 findings filed in §2.3 / §2.3.2 are marked
*pending independent verification* and nobody has re-derived them.

**The standard is the register's own:** independent re-derivation, not re-reading the finding text.
For each: open the cited file and line, confirm the defect is present as described, confirm the
severity's stated basis, and record what you checked.
- **Move severity in BOTH directions where the evidence says so.** A verification pass that only ever
  confirms is a check that cannot fail. If a finding is overstated, say so; if understated, raise it.
- **Record per finding: FOUND / TESTED / HOW**, with the instrument and its controls named.
- **Keep the verified/unverified split visible in the register at every moment.** The register's
  credibility rests on it. Never let a partially-verified block read as verified.
- **`D-CVL-02` is the highest-value one and it is scored on an ASSUMPTION** — Medium on the belief that
  the decrypted PDF copy lands app-private (`ScanSupportService.java:1097`). **If it is external it is a
  High and must be rescored.** Settle it from the source if the source can settle it; if it cannot,
  say so plainly and leave it flagged rather than resolving it by preference.
- **`error.codeLink`'s origin in MailFlow** is the other open severity question. Same treatment.

---

## ITEM 3 — file batch-1's findings as counted rows
The same treatment §2.3 gave batch 2. Roughly twenty findings currently exist only as §2.2 prose, so
**the estate total of 242 understates the estate.** File them with the same *pending independent
verification* framing, and **make the totals reconcile arithmetically** — state the before and after
and show the sum, the way the 219 -> 242 move was shown.

---

## ITEM 4 — continue the review, in this order
1. **The two severity-gating questions above** (they change published severities — highest value).
2. **`D-MF-07`'s escalation condition.** Seven sites send a raw token with no `Bearer` scheme; the
   seventh sends it to `cloudRenderingJobItem.contentLocation`, **a URL the Gotenberg service
   designates**. It is filed Low. **If pdf-api can influence that URL it is a token-exfiltration path
   and must be rescored well above Low.** That is a pdf-api-side question — Critical #12 notes its API
   credential is public. Answer it from source if source can answer it.
3. **The named coverage gaps**, as far as static review can take them: QuickQuote's `stage3/strip.js`
   (the build step its whole margin-protection property rests on), myPKI's fuzzy-commitment
   mathematics (**which could REDUCE Critical #13** — a finding moving down is as valuable as one
   moving up), SecurePDF's `spdf_encode` (**not in the tree — say so rather than inferring**).

---

## HOLDS — every one observed, and two are absolute
🔴 **NO LIVE PASS. It is BLOCKED and not by you:** the tenant question (`fc05dcdd` vs `0c57ab37`) is
marked UNRESOLVED in the workspace CLAUDE.md. **Do not assert which tenant is which, do not run `az`,
do not touch a live system, device, card or tenant.** Static only.
🔴 **Read-only on `Source_Code/`.** Nothing created, modified or deleted under it.
- **No secret value in any artefact** — file:line, variable name, class, length. Never a value, never
  a prefix, never "redacted" head. (The last session got this right; keep it.)
- **No client-facing communication.** Peter, Stuart, HP and anything client-visible are Kam's.
- **No Jira writes.**
- **Ticket creation aggregates** — one larger ticket per logical path, not five.
- **Never delete — quarantine.** Every file edited gets a `.pre-` backup beside it.

## ONE THING ALREADY ANSWERED, so you do not spend a turn on it
Your predecessor's report flagged an **Agent Mail 403** and said *"someone should check whether the key
rotated."* **Wednesday checked: it did not.** The vault copy at `Notes (MASTER)/Access/Agent Mail.md`
is byte-identical to the key working in Wednesday's session right now (compared without printing
either). **So the cause is elsewhere, and this fleet's 2026-08-07 lesson gives the prior: a 403 with a
valid key is usually the credential not reaching the failing PROCESS, not a bad key.** This project has
no fleet inbox anyway. **Do not chase it; it is noted, not owed.**

## REPORTING
This project has **no fleet inbox** — `send_brief.sh` refuses it. **Your report on disk under
`_Working/` IS the deliverable**, plus `PROGRESS.md` kept current. Wednesday reads the pane and the
files. **Mid-session questions go in `PROGRESS.md` and at your prompt.**
**Wednesday will not treat a pane line as a message from you; write it to disk.**

## PROVENANCE
- Kam's two sentences | his panel, verbatim, read via `kam_rulings_today.sh` and the chat log | 2026-09-08
- §7.1's three conflicting passages | lines 460 / 497 / 509 of the register, read by Wednesday | 2026-09-08 09:5x
- all 11 components have delta artefacts | `ls _Working/delta-review-2026-09/` by Wednesday | 2026-09-08
- register total 242 and the framed completeness claim | read at lines 14/18/38 by Wednesday | 2026-09-08
- the .docx is 07:29 and the .md 07:28 | `ls -la Deliverables/` by Wednesday | 2026-09-08
- D-MF-07's text and its escalation condition | quoted from register line 368 | NOT re-derived by Wednesday
- D-CVL-02's assumption | `_BATCH2_REPORT.md:193-194`, quoted | NOT re-derived by Wednesday
