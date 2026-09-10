# Brief — Security Review registers: the evidence appendix, table widths, sub-item spacing

**Commissioned by Kam, 2026-09-10 11:25:53, on the Tuesday panel tab. Relayed here verbatim
by Tuesday. This is a PRESENTATION round plus ONE GENUINE ADDITION (the appendix). No
finding, severity, score, CVSS vector or count moves. The estate must still reconcile to
28 C / 76 H / 126 M / 73 L / 39 I = 342 across the pair — re-derive it, do not trust this line.**

## KAM'S WORDS, VERBATIM

> With regards to the security review documents, please make the following changes. One,
> before sub items, so 3.1, 3.2, etc. only create two spacelines. Also, review the tables,
> as some tables are not wide enough. I found that making the field column larger, so about
> 6 on the ruler, was wide enough for most of the text to fit. And most importantly, please
> add to the appendix, create an appendix B or C, where if there is a finding such as header
> row issue, it references an appendix item and each appendix itemizes exactly which line of
> code, which file and which project the problem was found in. This makes addressing the
> issues much simpler. So make the appendix as detailed as possible to find and resolve the
> issues. Once you finish, please email me the documents again.

## YOUR FILES

`Deliverables/13A_HPAM_Consolidated_Findings_Register_2026-09.md` and
`Deliverables/13B_Datasec_Products_Consolidated_Findings_Register_2026-09.md`, plus their
`.docx` via `_Working/build-doc13A.sh` and `_Working/build-doc13B.sh`.
**`03_Findings_Register.*` is NOT yours this round. Do not touch it.**

Quarantine before the first edit, per the project's own convention:
`.pre-appendix-2026-09-10_<name>` beside each file. Never delete anything.

---

## ITEM 3 IS THE IMPORTANT ONE — THE EVIDENCE APPENDIX

Kam's purpose, in his words, is that *"addressing the issues much simpler"*. The test of
this appendix is not whether it is thorough; it is whether an engineer holding it can open
the right file at the right line without asking anyone a question.

### The evidence already exists — use it, do not reconstruct it from the register's prose

`_Working/findings-seed-2026-09/` holds one seed file per component, written under
`_AGENT_RULES.md` rule 4: *"Evidence for every claim — `component/path/file.ext:line`. No
claim without a citation."* Tuesday measured **1,248 `file:line` citations across 14 files**
(13 component seeds plus `_REVERIFICATION_19.md`) — **re-derive that count yourself; it is
Tuesday's measurement, not yours, and the frame was `*.md` in that one directory.**

Each seed finding already carries: an ID (`RD-01`, `INFRA-02`), severity + CVSS vector,
Confirmed/Suspected, an `### Evidence` block with `file:line` and quoted code, why it
matters, and remediation. **That is the appendix's raw material.** The register's own rows
also cite lines inline (e.g. `DataContext.cs:67`) and name the component in the header row.

### What each appendix entry must carry

One entry per finding that has locatable evidence, keyed by an id the finding row cites:

1. **The appendix id** (e.g. `B-014`), and the finding it belongs to.
2. **The PROJECT / component** — the repository or component slug as it appears under
   `Source_Code/`, so the reader knows which checkout to open.
3. **The FILE**, as a repo-relative path.
4. **The LINE or line range.**
5. **What is at that location** — one sentence, and where a short code excerpt genuinely
   helps, the excerpt. **Subject to the secret rule below.**
6. **What to change there**, in one sentence, consistent with the finding's existing
   "How to resolve" — do not invent new remediation, and do not contradict what the
   register already says.

Where a finding has several locations, list them all under that one entry. Where a finding
has NO locatable evidence — a process observation, a design judgement, a documentation gap
— **say so explicitly in the appendix** (`no code location: this is a <process/design>
finding`) rather than omitting it silently or inventing a plausible file. An honest gap is
worth more than a manufactured citation, and a fabricated line number will be discovered
by the first person who opens it.

### The cross-reference, both ways

Each finding row gains a reference to its appendix entry, and each appendix entry names its
finding. Kam's example is *"if there is a finding such as header row issue, it references an
appendix item"*. A reader must be able to travel finding → appendix and appendix → finding
without a search.

### 🔴 THE SECRET RULE, AND IT IS NOT NEGOTIABLE

The engagement hold forbids reproducing a secret's **value, prefix or length**. Several
findings are about committed credentials. **For those, the appendix gives the LOCATION ONLY**
— project, file, line, variable name, and the class of credential. **Never the value, never
part of it, and never a length.** `_AGENT_RULES.md` rule 6 says the same thing and is the
authority. Quoting a code excerpt is fine where the excerpt contains no secret; where it
would, describe the line instead of quoting it.

This is the one place where Kam's "as detailed as possible" and the hold are in tension.
**The hold wins, and the appendix says so once, plainly, so the reader knows why a line is
described rather than quoted.** Tuesday has already told Kam this is how it will be built.

---

## ITEM 1 — SUB-ITEM SPACING

Currently every `###` and `####` heading is preceded by a raw-OpenXML block of three empty
paragraphs (`<w:p/><w:p/><w:p/>`), and every `##` section by a page break.

- **`###` sub-items (`1.1`, `2.3`, `3.1` …): TWO empty paragraphs, not three.** This is
  Kam's explicit instruction.
- **`####` findings: LEAVE AT THREE.** He did not mention them, and Tuesday has told him
  they are being left alone because each is a large block with its own table. If he says
  otherwise it is a one-line change.
- **`##` sections keep their page break. Do not touch that** — it is the change he asked
  for this morning and approved.

## ITEM 2 — TABLE WIDTHS

Kam: *"making the field column larger, so about 6 on the ruler"*. There is exactly ONE table
with a literal `Field` header, so he means **the LEFT column of the finding tables** — the
one carrying `The issue`, `Suggested fix`, `What was tested`, `How it was tested`, `How to
resolve`. Those labels currently wrap.

**Set that column to 6 cm** (Tuesday's reading of "6 on the ruler"; six inches would leave
almost nothing for the text on A4, which is what settles the unit). Pandoc emits tables
with autofit; you will need explicit `<w:tblGrid>` / `<w:tcW>` widths and
`<w:tblLayout w:type="fixed"/>`, applied in the post-build step where `w:updateFields` is
already set, or via the reference document.

**Then check EVERY table in both documents**, which is the rest of his instruction: any table
whose content is being squeezed gets sensible column widths. Report how many you changed.

---

## VERIFY IN THE RENDERED `.docx`, NOT IN THE MARKDOWN

**This document has now shipped wrong twice while the markdown was correct** — three tables
rendering as paragraphs of pipes, then 38 literal `**` and 16 literal `~~` printing as text.
Both were invisible from the source. So:

- Extract `word/document.xml` and assert the appendix entries are present, the table widths
  are what you set, and the sub-item spacing is two paragraphs where it should be.
- **Every check gets a control that fires**, on the pre-edit file, so a zero is a zero you can
  vouch for and not an instrument that cannot see.
- Re-assert the things that must NOT have moved: table count and row counts, heading counts,
  the severity bands, the estate reconciliation, zero emoji, zero literal `**`/`~~`/backticks.

## CONSERVATION, ASSERTED BEFORE YOU WRITE

Counts by band per document and across the estate, re-derived from the tables themselves and
then re-read out of the RENDERED files. If your numbers disagree with 210 / 132 / 342, stop
and report — do not reconcile them to match this brief.

## WHAT TO REPORT

Mail your wrap to **`tuesday-agent@agentmail.to`** — not to Wednesday, not to Kam. Tuesday
verifies and sends the documents to Kam. Include:

- the exact paths of the four files you changed;
- how many appendix entries you created, and **how many findings had NO locatable evidence**,
  listed by id — that number is a finding in itself and Kam should see it;
- how many tables you re-widthed;
- the conservation figures, re-derived;
- every control you ran, and anything you could NOT verify.

**RAISE, do not silently fix:** anything where the seed evidence and the register's own
citation disagree. That is a real defect and Tuesday wants it named, not reconciled
([[establish authority before reconciling]] — the disagreement is the signal).

## HOLDS

- No merges, no deploys, nothing outside this project's folder.
- Read-only on `Source_Code/` — you are citing it, never changing it.
- Read-only on Jira. Do not create or transition tickets.
- Do not email Kam. Do not post to the extranet.
- If a decision is approval-class or you find yourself arguing an action into scope, stop
  and mail Tuesday.
