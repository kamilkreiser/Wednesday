# Registers 13A and 13B — ROUND 2: front matter, pagination, and every finding restructured on BLUF

## BLUF

**Kam has read the two registers you delivered and called the revised structure "great".** This round is his follow-up: **five changes, four of them presentation and one of them a genuine rewrite of every finding's internal shape.** Both documents get the same treatment. **No finding, severity, score, vector or count moves.**

**His words, verbatim, 2026-09-09 17:03:**

> *"This revised structure and document is great. A couple of additional changes. Please create the front page as a single page with the title and subtitle and revision history including when it was created. Second page should be the table of contents, ideally clickable as references throughout the document. And then make sure that you start every section on a new page so insert page ranks throughout the document. Within the actual document, please review the My Empire document and use this as a reference. In addition to that, I'd like each finding and each item to be structured using the bluff principle. Essentially, the issue and the suggested fix with details below of what was tested, how it was tested, and details of how to address it or resolve it. I understand this will take a while to change."*

**"bluff" is BLUF** — bottom line up front. **"page ranks" is page breaks.** Both are dictation; neither is ambiguous in context.

## THE FIVE CHANGES

1. **A single title page.** Title, subtitle, and a **revision history table including the creation date**. One page, nothing else on it. **The MyEmpire report opens exactly this way — document control with effective date, next review date and a version table — so match its shape rather than inventing one.**
2. **The table of contents on page two**, cross-referenced and clickable through the document.
3. **Every section starts on a new page.** Page breaks throughout.
4. **The MyEmpire report as the reference for the body**, again and explicitly. Read it properly this round if you took it only structurally last time.
5. 🔴 **EVERY FINDING AND EVERY ITEM RESTRUCTURED ON BLUF.** This is the real work. His shape, in his order:
   - **the issue**, and **the suggested fix** — first, together, at the top;
   - then **below it**: what was tested · how it was tested · how to address or resolve it.

   **A reader who stops after the first block must know what is wrong and what to do about it.** Everything else is supporting detail underneath. **He said he understands it will take a while — so take the time and do it properly rather than mechanically reordering cells.**

## 🔴 THE TRAP THIS ROUND WILL HIT, and it is the same one twice already today

**This document has now been wrong TWICE in the rendered `.docx` while being correct in the Markdown** — three tables that rendered as paragraphs of pipes, and 38 literal `**` printing as text. **Both were invisible from the source and visible to Kam.**

**Every one of this round's five changes is exactly that shape.** Specifically:

- **A pandoc-generated `.docx` table of contents is a FIELD.** Word may show it empty or stale until the field is refreshed. **A TOC that is perfect in the source and blank on his screen is this round's most likely failure.** Verify what the file actually contains, and if the field cannot be made to populate on open, say so and use a generated static TOC with working internal links instead.
- **Page breaks must be real `w:br w:type="page"` runs in the rendered file**, not a source directive pandoc silently dropped. **Count them in `word/document.xml` and check the count matches your section count.**
- **Internal links must resolve.** A clickable TOC whose anchors do not match its headings is worse than a plain one, because it looks finished.

**So: verify every one of the five in `word/document.xml`, and run each check against the CURRENT 13A/13B as a control so you know the check can fail.** The project already has precedent for raw OpenXML blocks (the branded cover page), so the mechanism exists.

## HOLDS

- **Nothing about the findings changes but their PRESENTATION.** Totals stay **13A 210, 13B 132, estate 28 C / 76 H / 126 M / 73 L / 39 I = 342**. Report them from the rendered files.
- **Everything won last round is preserved:** zero emojis, real tables, commands formatted separately from commentary, no literal markup in the render, the section concordance, F-21 counted once in 13A and cross-referenced uncounted in 13B.
- **Never reproduce a secret value, prefix or length.** The `"length deliberately not reproduced"` note in 13B stays as it is. A public key fingerprint is not a secret and stays.
- **A substantive error found while restructuring is RAISED, not fixed quietly.**
- **Quarantine both formats before the first edit** (`.pre-round2-2026-09-09_*`). Never delete.
- **Nothing is emailed to anyone.** Tuesday sends Kam the copies.

## ⚠ ANOTHER SEAT IS LIVE IN THE SAME DIRECTORY — the boundary, stated from your side

A second seat is scrubbing **`Deliverables/03_Findings_Register.{md,docx}`** — the June register — right now. **That file is NOT yours: do not read it as a model this round, do not edit it, do not rebuild it.** **Yours are `13A_*` and `13B_*` only.** If you find yourself needing to touch `03_*`, stop and mail Tuesday instead.

## DELIVERABLE

Revised `13A_*` and `13B_*` in both formats, plus a report naming: the five changes and how each was verified in the rendered file with its control, the BLUF template you applied, any finding whose content resisted the template and why, and any substantive defect raised-not-fixed.

## WHERE TO SEND IT

**Mail the wrap to `tuesday-agent@agentmail.to`.** Not `wednesday-agent@`. Name the exact paths.

If anything here is wrong or contradicts itself, say so rather than resolving it silently.

PROVENANCE:
- Kam's instruction, verbatim and complete | the panel message delivered to tuesday-agent@ at 2026-09-09T07:03:44Z, quoted unedited | read 2026-09-09
- the MyEmpire report opens with document control, effective date, next review and a version table | pdftotext pages 1-2 of `Test Related Documents/Datasec - Penetration Test Report - 1.0.pdf` | read 2026-09-09
- the current documents are clean on emoji, tables and literal markup | Tuesday's own extraction from word/document.xml of both files, with the pre-reformat file as a control at 462 emoji | read 2026-09-09
- the totals | the ESTATE TOTAL rows read out of both rendered .docx files | read 2026-09-09
- another seat is live on 03_Findings_Register | Tuesday launched it and holds its brief | read 2026-09-09

SELF-CHECK: re-read end-to-end for contradictions; the render-verification requirement is attached to each of the five changes rather than stated once | 2026-09-09 17:12
