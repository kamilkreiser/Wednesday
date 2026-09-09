# JUNE register — SCRUB the disclosed secrets and RE-ISSUE. Kam's ruling, executing his own words.

## BLUF

**The June findings register prints live secret values in full, in the document itself.** Kam ruled `all-three` on 2026-09-09 12:09 — **rotate, re-issue, establish distribution.** This round is the **RE-ISSUE**: remove the disclosed values from the document and republish it. **Rotation is NOT yours and not Tuesday's.** Distribution is already answered.

**Kam, 2026-09-09 ~16:3x, verbatim, on where the document has gone:** *"no, nothing has been sent to anyone outside"*. **So the exposure is contained to people who already hold repository access. There is nothing to recall and nobody to notify — this is careful work, not an incident.**

## THE TARGET

`Deliverables/03_Findings_Register.md` and the `.docx` built from it. **This is a SIGNED-OFF deliverable**, so the re-issue is a new version that supersedes, with the original quarantined — never a silent overwrite.

## WHAT IS DISCLOSED — re-derive it, do not trust this count

**Tuesday measured eight value-bearing lines: six in F-16, two in F-12.** By class only: two Entra client secrets, one platform API key, App Configuration read and write master keys inside a committed Terraform state backup, one PFX password, and admin and database password literals.

🔴 **AND A NINTH DISCLOSURE THAT IS NOT A VALUE: F-16's evidence states a secret's CHARACTER LENGTH in prose. A length is a disclosure and it is in scope for this scrub.** The seat that reformatted register 13 hit the identical case this afternoon and handled it by replacing the length with an explicit note that it is deliberately not reproduced. **Do the same here.**

**RE-DERIVE ALL OF IT AT SOURCE.** Tuesday's first detector for this failed its own control — it returned twelve "disclosures" in a finding that has none, because it was matching prose punctuation. **The count above came from reading the evidence block with every value masked. Treat it as a starting point, not a census**, and report what you actually find, including anything outside F-16 and F-12.

## 🔴 THE HARD CONSTRAINTS

1. **NEVER REPRODUCE A VALUE, A PREFIX, OR A LENGTH — anywhere.** Not in the revised document, not in your report, not in a commit message, not in the wrap mail. **Class and location only.** If you must refer to a specific one, say *"the PFX password at `<path>:<line>`"*.
2. **DO NOT WEAKEN A SINGLE FINDING.** The finding is that these secrets are committed in source. **Every evidence location, file path, line number, severity, score and vector stays exactly as it is.** Only the literal secret is replaced, with a marker that says a value was there and was deliberately removed. **A reader must still be able to verify the finding by going to the cited location.**
3. **A PUBLIC key fingerprint is NOT a secret** and stays. If you meet one, keep it and label it public — removing it would weaken a finding. Flag it in your report rather than deciding silently.
4. **VERIFY IN THE RENDERED `.docx`, NOT THE MARKDOWN.** Tuesday confirmed all six F-16 sites are present inside `word/document.xml` of the shipped file. **A scrub proven only in the source has not been proven.** Extract the rendered text and assert the absence of each value you removed — **and run that same check against the PRE-SCRUB file to prove it can fail.** A zero from an instrument nobody has seen fire is not a zero.
5. **Quarantine both formats before the first edit** (`.pre-scrub-2026-09-09_03_*`), and never delete anything.
6. **Nothing is emailed to anyone.** Tuesday sends Kam the copy.

## WHY THIS MATTERS, stated so the care is proportionate rather than anxious

The finding that reported committed secrets **reproduced them into a document with wider distribution than the repository** — a signed-off deliverable, rendered to Word for circulation. So rotating the repository secrets and scrubbing git history would both leave this document untouched. **That is the gap this round closes.** Whether any of them is still live is NOT established and is not yours to test.

## DELIVERABLE

Revised `.md` and rebuilt `.docx`, plus a report naming: what you found and where by class, what you replaced and with what marker, the render verification with its control, anything you judged not-a-secret and kept, and any disclosure outside F-16 and F-12.

## WHERE TO SEND IT

**Mail the wrap to `tuesday-agent@agentmail.to`** — not `wednesday-agent@`, which is the pre-split fleet default. Name the exact paths of both revised files.

If anything here is wrong or contradicts itself, say so rather than resolving it silently. Two seats corrected Tuesday's briefs today and both were right.

PROVENANCE:
- Kam's ruling `all-three` | decision_queue card `secreview-june-register-discloses-credentials`, ruled 2026-09-09 12:09 | read 2026-09-09
- Kam's answer on distribution, verbatim | his reply to Tuesday, 2026-09-09 ~16:3x, quoted complete | read 2026-09-09
- eight value-bearing lines, F-16 six and F-12 two, by class | Tuesday's own re-derivation, reading the evidence block with values masked, after a first detector failed its control | read 2026-09-09
- all six F-16 sites are present in the shipped .docx | a marker check inside `word/document.xml` of `03_Findings_Register.docx`, with a positive and a negative control | read 2026-09-09
- rotation is not this seat's | Datasec production is ungranted to Tuesday, and rotating live credentials is Kam's signature class | read 2026-09-09

Tuesday has NOT read the June register's body beyond F-12 and F-16's evidence blocks, and read those with every value masked. Re-derive at source; do not trust this brief's characterisation.

SELF-CHECK: re-read end-to-end for contradictions; the no-weakening rule and the scrub rule are stated together because they are the pair most easily traded off | 2026-09-09 16:53
