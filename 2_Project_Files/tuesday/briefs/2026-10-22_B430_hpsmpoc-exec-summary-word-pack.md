# HPSM-POC executive summary: before / after word pack (HPSMPOC-187)

For: Kam's approval. Card ruled: `hpsmpoc-exec-summary-opening-words-1021` = a.
Source read: HPSM-POC `origin/main` = `ae7a2c860a5e909b3430dadeacf1985c7142e4da`.
All paths below are under `2_Project_Files/`. Nothing has been changed, posted or sent.

## Read this first: the name is already drawn in

The stored template text says "the organisation" on purpose. Since PR #95 (C-48, your ruling on card 1003) the PDF and the screen swap the first "the organisation" for the customer's name when they draw the page. So today's printed opening should already read "The assessment of <customer name> produced...".

The ticket was filed on an older build (main 799cc3e). So the "name" half of your card may already be fixed on the page. I did not run the app, so I have not seen a PDF. Please treat this as a question (see DRAFTER NOTES).

Because of that rule, the AFTER words below keep the plain phrase **the organisation** as the name token. That phrase is the only name token in the code. There is no `{name}` variable. The drawing code finds the first "the organisation" or "The organisation" and swaps it. If the first one starts a sentence, the name gets a capital letter.

---

## String 1. The opening sentence (with a score)

BEFORE (verbatim), `api/src/HpsmPoc.Modules.Reporting/Narrative/Providers.cs:67` @ ae7a2c8:

```
$"The assessment of the organisation produced an overall current score of {Num(o.Current)}{(o.Target is null ? "" : $" against a target of {Num(o.Target)}")}{(o.Band is null ? "" : $", which places it in {o.Band}")}."
```

What the stored text reads, with sample numbers:
"The assessment of the organisation produced an overall current score of 62.5 against a target of 100.0, which places it in Red."

What the page should already read after name-drawing (sample customer "Sample Co"):
"The assessment of Sample Co produced an overall current score of 62.5 against a target of 100.0, which places it in Red."

### AFTER, option A (recommended)

Template: `The organisation scored {score} against a target of {target}. That places it in {band}.`
(The `{score}` `{target}` `{band}` parts stay as the existing `Num(...)` values. The target and band parts still drop out when they are missing.)

Page reads:
"Sample Co scored 62.5 against a target of 100.0. That places it in Red."

Why: it puts the customer first, as the subject. It is two short sentences. "Overall current score" and "assessment of" add nothing. The name token starts the sentence, so the code already capitalises a lower-case name.

### AFTER, option B

Template: `This assessment gives the organisation an overall score of {score} against a target of {target}, which places it in {band}.`

Page reads:
"This assessment gives Sample Co an overall score of 62.5 against a target of 100.0, which places it in Red."

Why: closest to today's shape. The name sits mid-sentence, so there is no capital-letter risk. Slightly longer.

## String 2. The opening sentence (no score)

BEFORE, `Providers.cs:66` @ ae7a2c8:
`"The assessment of the organisation did not produce an overall score."`

AFTER (recommended, goes with A or B):
`"The assessment did not produce an overall score for the organisation."`

Page reads: "The assessment did not produce an overall score for Sample Co."

Why: the name moves to the end, where it is the object. Same meaning. No alternative needed.

---

## String 3. The action sentence repeated once per finding

BEFORE (verbatim), `Providers.cs:99` @ ae7a2c8, inside `Describe(f, withRationale)`, called for each priority finding at `Providers.cs:75`:

```
text += $" Recommended action ({ReportVocabulary.BucketLabel(f.Bucket)}): {f.Action.Trim()}";
```

Fixture sample of what the page reads today (`api/tests/HpsmPoc.Modules.Reporting.Tests/Fixtures/b66-exec/exec-3-findings.base-output.json`):
"DRAFT: Regular firmware updates not confirmed. This is a high-severity finding. Recommended action (30 days): DRAFT: apply the HP Security Manager settings listed for this finding (the Datasec baseline). The partner's action wording is to be supplied by the Datasec security expert."

With the DRAFT content, every finding repeats that same action. That is the repeat you saw.

Also related, `Providers.cs:69` (the counts line, verbatim):
`$"Findings raised: {input.Findings.Count}. Findings needing priority attention: {priority.Count}."`

### AFTER, option A (recommended): say actions once, in the counts line

Each finding line keeps its title and severity only. The counts line carries one pointer to the roadmap.

Finding line template: `{Title}. This is a {severity}-severity finding.`
(If the risk was accepted, the existing sentence "The organisation has accepted this risk." stays after it.)

Counts line template:
`Findings raised: {count}. Findings needing priority attention: {priority}. Each finding has a recommended action. The actions are listed once, by timing, in the roadmap.`

The code change: the executive summary stops adding the action text. The finding explanations and the roadmap keep it. (`Describe` is also used for finding explanations at `Providers.cs:53`, with the rationale, so the action part should be dropped only for the summary.)

Sample for 6 findings, all high severity, no next engagement, sample customer "Sample Co". Under today's cap of 5 named findings, the sixth goes in the "further" line:

1. Sample Co scored 62.5 against a target of 100.0. That places it in Red.
2. Findings raised: 6. Findings needing priority attention: 6. Each finding has a recommended action. The actions are listed once, by timing, in the roadmap.
3. Trusted-firmware checks at start-up not confirmed. This is a high-severity finding.
4. Regular firmware updates not confirmed. This is a high-severity finding.
5. Identifying outdated or vulnerable firmware not confirmed. This is a high-severity finding.
6. Sample finding D. This is a high-severity finding.
7. Sample finding E. This is a high-severity finding.
8. Further priority findings are listed in the Priority Risks section.

(8 paragraphs. The cap was 8 when ADR-R18 was written. I did not confirm the current number; see notes.)

Why: the action is stated once and the page is shorter. Option A adds no new paragraph, so the paragraph cap is not touched. A reader still gets one place to look.

### AFTER, option B: a separate closing line

Keep the counts line as it is today. Add one closing paragraph after the findings:
`The recommended actions for these findings are listed once, by timing, in the roadmap.`

Why: it reads more cleanly, but it is one more paragraph. A summary with 5 priority findings and a next engagement is already at the cap (8) and would hit 9. It would need the cap or the "further" logic changed. Not recommended.

---

## What changes if you approve

- Wording in `Providers.cs` (lines 66, 67, 69 and the summary use of line 99).
- The golden files and tests that pin the old wording must change with it (about 20 hits across `api/tests` and `web/src`; the main ones are the `b66-exec` fixtures, `customer-name-at-render.json`, `B121*`, `B125*` and the web `name-at-render` tests).
- The stored text still keeps "the organisation", so the "name never reaches the model" rule is untouched.
- Each approved summary stored before the change keeps its old words until it is written again.

## DRAFTER NOTES

What I read:
- Card `hpsmpoc-exec-summary-opening-words-1021` (via `show` on that id only).
- HPSM-POC `origin/main` @ ae7a2c860a5e909b3430dadeacf1985c7142e4da: `Narrative/Providers.cs` (lines 40-102), `Report/CustomerNameAtRender.cs`, `Report/ReportModelBuilder.cs` (lines 85-125), the grep for the current strings, and the Reporting README row ADR-R05.
- Jira HPSMPOC-187 by GET (summary, description, comments). It says: first half (name) built and merged as PR #95 / main 26d5d1a; second half (repeated action) not ruled.

What I could not establish:
- Whether a PDF drawn from current main really shows the customer's name in the opening. I read code only, ran nothing.
- The current value of `NarrativeOutputValidator.MaxParagraphs` for the executive summary (I used 8 from the ADR-R18 text; I did not open the validator).
- Whether these template strings sit under an approved-text rule. The ticket says to check C-13, C-23 and C-26. I did not read those clarifications; Kam's approval on this card is the cover for the new words.
- The Jira ticket's code reference (799cc3e) is older than the sha I read. I did not check the ticket's evidence files (`B97_evidence`).

Questions for Tuesday:
1. Should the card say that the opening name is already drawn in on current main? If a PDF check shows it is, the opening change is a wording preference only, not a defect. I suggest Tuesday has a seat confirm that on a real PDF before Kam is asked.
2. Do you want option B for the opening (name mid-sentence) to avoid the capital-letter code path? Both work with the current code.
