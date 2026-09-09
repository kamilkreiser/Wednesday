# Security Review register — PROOFREAD AND REFORMAT (presentation pass, not a re-analysis)

## BLUF

Kam has read the consolidated findings register and sent it back. **His complaint is the WRITING and the FORMATTING, not the findings.** This round rewrites how the document reads and looks, matched to an existing model, and changes nothing about what it says. It ends when a revised `.md` and a correctly-rendered `.docx` exist and the wrap mail names them.

**His words, verbatim, across three messages on 2026-09-09:**

> *"With regard to the security review, please proofread the document as it's poorly written with no punctuation and grammar applied to it, and make sure the document is formatted properly. You can use the previous July or June report as a basis, but I need the document to be formatted. Once the revised version is done, please email me another copy."*

> *"Also, do not use emojis as part of this document. Use tables and references so that it's properly formatted. Research security reviews as a basis, and you should be able to, in the folder, find a security review put together by My Empire for references."*

## THE TARGET AND THE MODEL, both located and measured

- **The document to revise:** `Deliverables/13_Consolidated_Findings_Register_2026-09.md`, and the `.docx` built from it. 1,297 lines.
- **The MODEL Kam names, and it EXISTS — he spelled it as two words and it is one:** `Test Related Documents/Datasec - Penetration Test Report - 1.0.pdf`, 3.2 MB, first page reads *"Prepared by MyEmpire on behalf of Datasec"*, Version 1.0, release date 15 August 2023. **It opens with a Document Control block — effective date, next review date, and a version-control table — before any content.** That is the professional shape to match.
- **The in-house precedent already exists too:** the June register `Deliverables/03_Findings_Register.md` carries `## 1. Executive Summary` at line 32, and this project's own `_Working/PROGRESS.md` records it was *"styled on the MyEmpire 2023 pen-test report (engagement & scope, methodology, per-ToE risk ratings table, severity distribution, key findings)"*. **So the house style is already defined; you are applying it, not inventing it.**
- **The `.docx` is built by `_Working/build-doc13.sh`.** The rendered file is what Kam opens, so it is the artefact that must be right.

## WHAT IS WRONG TODAY, measured rather than asserted

1. **The document reads as an internal working note, not a client deliverable.** Its current top-level sections include `## BLUF`, `## 2. The 15 new Criticals`, `## 2.3.3 THE 62 BATCH-1 DELTA FINDINGS ... PENDING INDEPENDENT VERIFICATION`, `## 3. What the coordinator personally verified at source`. Section titles carry our internal process vocabulary and our own session history.
2. **It contains 458 emoji-class characters, 16 distinct.** The heaviest are the warning sign (58), the red circle (32), the white check (25), the no-entry sign (17), the wrench (16) and the red triangle (15). **Kam's prohibition is flat and unqualified. Remove all of them.** The right-arrow character appears 181 times; it is punctuation rather than an emoji, so that is a judgement call — **make it, and state in your report which way you went and why.**
3. **Headings are inconsistently cased** — some sentence case, many full capitals mid-document.

## THE HARD CONSTRAINT NOBODY CAN SEE BY READING THE MARKDOWN

**On 2026-09-09 this register's `.docx` was found to have been shipping with three tables not rendering as tables — including the entire 62-row table holding both headline Criticals — because GitHub-flavoured Markdown needs a BLANK LINE before a table header and pandoc read the run-on as one paragraph of pipes. Every review of the Markdown missed it because the Markdown was correct. The customer got the broken file.**

**Kam is now explicitly asking for tables.** So:

- **A blank line before every table header, without exception.**
- **A raw `|` inside a cell truncates that row.** It must be escaped as `\|`. Ten rows carried one before.
- **VERIFY IN THE RENDERED FILE, NOT THE SOURCE.** Extract the tables back out of `word/document.xml` and count the rows against the Markdown. A table that renders as a paragraph is the failure this round exists to prevent, and it is invisible from the source.

## HOLDS

- **DO NOT CHANGE ANY FINDING, SEVERITY, SCORE, VECTOR OR COUNT.** The estate totals are `28 Critical, 76 High, 126 Medium, 73 Low, 39 Informational = 342`, and they balance by row and by column. **If the numbers move, something is wrong with your edit, not with the register.**
- **If the proofread turns up a SUBSTANTIVE error — a wrong claim, a contradiction, a broken reference — RAISE IT SEPARATELY. Do not quietly fix it inside a formatting pass.** A presentation round that silently changes meaning is worse than one that reports a defect.
- 🔴 **MATCH THE JUNE REGISTER'S FORMAT. DO NOT INHERIT ITS CONTENT.** The June register is the subject of an open, ruled finding: it prints live secret values verbatim. **Take its structure, its section order and its tone. Copy none of its evidence text.** Never reproduce a secret value, a key prefix, or a secret's length into the revised document, and if you notice the current register doing so, report it rather than pasting it forward.
- **Nothing is emailed to anyone by you.** Tuesday sends the copy to Kam. **Kam is the principal, so that is not external communication — but it is still Tuesday's to send, not yours.**
- **No changes to source code, no board writes, no deploys.**

## METHOD

1. **Read the MyEmpire report first** — at least its document control, contents, methodology and findings-presentation sections — and write down the specific structural properties you are matching. `pdftotext` is available on this machine.
2. **Read the June register's section order** as the in-house application of that model.
3. **Then restructure.** Suggested spine, but the model decides: document control and version table, executive summary, scope and methodology, severity definitions, per-component risk table, the findings themselves as tables with citations, then appendices. **Our internal process history belongs in an appendix or nowhere, not in a top-level section title.**
4. **References:** every finding cites its evidence location. Kam asked for references explicitly; a finding that asserts without citing is the thing he is objecting to.
5. **Rebuild the `.docx` with `_Working/build-doc13.sh` and verify the render.** Zero emoji in the output, every table a real table, the row counts matching.
6. **Quarantine, never overwrite blind:** take a dated `.pre-reformat-2026-09-09` copy of both formats before you start, exactly as previous rounds did.

## DELIVERABLE

A revised `.md` and a rebuilt `.docx`, plus a short report naming: what you restructured, the emoji sweep result with its control, the table-render verification with row counts, the arrow judgement call, and any substantive defect you found and did NOT fix.

## WHERE TO SEND IT

**Mail your wrap to `tuesday-agent@agentmail.to`.** Not `wednesday-agent@`, which is the fleet default your tooling still points at — Datasec is Tuesday's seat and Wednesday is a different coordinator on another client. Name the exact paths of both revised files in the mail.

If anything here is wrong or contradicts itself, say so rather than resolving it silently.

PROVENANCE:
- Kam's three messages, verbatim | 0_Brain/dashboard/data/chat_kam.json in Tuesday's own tree, entries 2026-09-09T15:40:49 and 15:41:28, read first-hand after a pull (relayed by the other coordinator, then confirmed at source) | read 2026-09-09
- the MyEmpire report exists, its title page and shape | pdftotext pages 1-3 of 'Test Related Documents/Datasec - Penetration Test Report - 1.0.pdf' | read 2026-09-09
- the June register carries a MyEmpire-styled Executive Summary at line 32 | grep of 03_Findings_Register.md, corroborated by _Working/PROGRESS.md line 55 | read 2026-09-09
- 458 emoji-class characters, 16 distinct, with the per-character counts | a Unicode-range scan of 13_Consolidated_Findings_Register_2026-09.md | read 2026-09-09
- the estate totals and that they balance | the ESTATE TOTAL rows at lines 102 and 761 of the register, which agree | read 2026-09-09
- the .docx table-rendering defect and its two causes | Tuesday's own measurement of 2026-09-09, recorded in the seat handover | read 2026-09-09
- the June register discloses secret values | the ruled card secreview-june-register-discloses-credentials, and Tuesday's own re-derivation at source today: eight value-bearing lines, F-16 six and F-12 two | read 2026-09-09

Tuesday has NOT read the MyEmpire report beyond its first three pages, and has NOT opened the current register's body except to count emoji and read its headings. Re-derive at source; do not trust this brief's characterisation of what any of these documents say.
