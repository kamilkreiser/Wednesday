# MPS Commercial Calculator: words review page (printed rental proposal vs the approved mock, plus one attachment sentence)

For: the product owner and Paul. Prepared 2026-11-12 from the app as it stands on its main branch (commit baf0aabe, read 10:20 AEDT today) and the approved mock folder (Design/2026-10-13_rental-book, four variants: typical, draft, small, large).
Marks are yours: tick one box per row. "App" = keep the app's words and the mock is edited to match. "Mock" = a builder changes the app to the mock's words. "Other" = write your own words.

## BLUF

- **9 wording differences** found between the printed rental proposal at main and the approved mock (the question put to you named 4; 5 more turned up). One more item, the large proposal printing 15 pages against the mock's 16, is a consequence, not a wording difference (see the end of the list).
- **3 of the 9 are words you approved on 14 Oct** (rows 2, 3, 5: all three are the "three fixes"; the app prints your 14 Oct words, the mock still shows the 13 Oct originals).
- **4 of the 9 are mock text the app no longer prints** (rows 4, 6, 7, 8). You approved those mock words on 14 Oct, then removed them on 16 Oct and approved the list of removals on 17 Oct (C-36), so the app lacks them on purpose. The mock was never updated.
- **1 of the 9 was never approved for the rental book** (row 1, the cover sub-line "| STANDARD PRICING" removed). 
- **1 of the 9 only shows on a local run** (row 9, the draft ribbon): the hosted site already prints "SHOWCASE", as the mock does.
- **You are asked to mark:** one box on each of the 9 rows, then choose the sentence for a PNG the browser cannot read (last section).
- One correction to the earlier note: the rounding note you were told the mock "lacks" is not missing from the mock. The mock has a different sentence in the same place (row 5); your 14 Oct fix replaced it.

## How this was compared

Frame: the rental full proposal, all four mock variants, every printed block, static words only. The app's words were read from its source on main (the text the page prints is built from those files), not from a rendered page, so nothing was printed or run. Customer names, prices, devices, SKUs and dates in the mock are sample data and are not compared. Mock-only marks (SAMPLE labels, the dagger and double-dagger notes) are not product words. Where a state is not in the mock (a quote with no itemised breakdown) it is listed because the app prints words there that the mock never shows. The purchase proposal is not in this page.

## The differences

Format of each row: where, app today, mock, was the app's wording approved on 14 Oct, mark. Text in braces is filled in by the app.

### Row 1. Cover, the line under the customer name
- App today: `{term}-month rental`
- Mock: `{term}-month rental  |  STANDARD PRICING`
- Approved on 14 Oct? **No.** On 14 Oct you approved the mock's version (with "STANDARD PRICING"). On 16 Oct you removed the pricing edition from the purchase sub-line; the builder applied the same removal to the rental book as its own reading ("the product owner's word corrects it", recorded in the build notes). The 17 Oct approved list names only the purchase sub-line. The edition still prints in the reference line and the prepared-by line.
- Mark: [ ] App  [ ] Mock  [ ] Other: ______________________

### Row 2. Section 1, box "Pricing interpretation", last sentence
- App today: `The contract value is worked out for the whole {term}-month term, so it can differ by a few cents from the monthly charge multiplied by the term.`
- Mock: `The contract value is the total of the monthly charges over the {term}-month term.`
- Approved on 14 Oct? **Yes.** The 14 Oct ruling (06:58, option "Approve all, with the three fixes as proposed"), third fix. The box itself was kept on the rental book by your 16 Oct 14:18 ruling, "Keep the box on the rental proposal (14 Oct wording)".
- Mark: [ ] App  [ ] Mock  [ ] Other: ______________________

### Row 3. Section 1, box "Pricing interpretation", first sentence, only for a quote saved before charges were itemised (the mock has no such variant)
- App today: `The monthly charge covers the fleet, options and software in this proposal. This quote was approved before charges were itemised, so no breakdown is shown.`
- Mock: nothing for this case. Every mock variant has a breakdown and reads `The monthly charge is the sum of the four components above, for the fleet, options and software in this proposal.` (the app prints that same sentence whenever a breakdown exists, so only the no-breakdown case differs).
- Approved on 14 Oct? **Yes.** Same 14 Oct ruling, second fix.
- Mark: [ ] App  [ ] Mock  [ ] Other: ______________________

### Row 4. Section 2, box "Not yet specified"
- App today: not printed.
- Mock: title `Not yet specified`, then `Applicable tenant subscriptions and the detailed deployment calendar have not been supplied.` and `These must be captured before a firm service schedule is issued.`
- Approved on 14 Oct? **No for the app's version** (the app prints nothing). The mock's first sentence was one of the 38 phrases approved on 14 Oct. The block was removed from the full proposals by your 16 Oct 13:03 ruling (option a, recorded on MPSCALC-157 in comments 39471 and 39484) and listed as removed in the words list you approved on 17 Oct (C-36).
- Mark: [ ] App (stay removed)  [ ] Mock (put it back)  [ ] Other: ______________________

### Row 5. Section 4, box "Reconciliation", second line
- App today: `The total monthly charge is worked out for the whole fleet. Each line's monthly charge is rounded to the cent, so the line charges above may not add up exactly to the total.`
- Mock: `The total monthly charge is the sum of the line monthly charges in the schedule above.`
- Approved on 14 Oct? **Yes.** Same 14 Oct ruling, first fix. (This is the "rounded to the cent" note said to be missing from the mock; the mock has the older sentence in the same place.)
- Mark: [ ] App  [ ] Mock  [ ] Other: ______________________

### Row 6. Section 10, "Recommended next steps"
- App today: not printed.
- Mock: heading `Recommended next steps`, then a numbered list. The typical mock's five steps start `Sample Customer R confirms its fleet allocation, site locations, volumes and output requirements.` and end `The parties complete contracting and agree pilot / rollout dates.` (the large mock shows eight sample steps).
- Approved on 14 Oct? **No for the app's version.** Same history as row 4: removed by the 16 Oct ruling, listed in the 17 Oct approved list (C-36).
- Mark: [ ] App (stay removed)  [ ] Mock (put it back)  [ ] Other: ______________________

### Row 7. Section 10, the note under the acknowledgement table
- App today: not printed (the table with "Authorised representative", "Title", "Date" is printed).
- Mock: `Acknowledgement indicates intent to progress final configuration and contracting; it is not acceptance of a binding MPS agreement.`
- Approved on 14 Oct? **No for the app's version.** Same history as row 4.
- Mark: [ ] App (stay removed)  [ ] Mock (put it back)  [ ] Other: ______________________

### Row 8. Section 10, "Proposal basis"
- App today: not printed.
- Mock: heading `Proposal basis`, then `Prepared from quote {reference}, version {n}, in the Datasec MPS calculator.`
- Approved on 14 Oct? **No for the app's version.** Same history as row 4.
- Mark: [ ] App (stay removed)  [ ] Mock (put it back)  [ ] Other: ______________________

### Row 9. Draft ribbon on the cover of a draft proposal
- App today: on the hosted site `SHOWCASE [middle dot] CONFIDENTIAL PRICING [middle dot] INTERNAL USE ONLY`; on a local run on a laptop `LOCAL DEMO [middle dot] CONFIDENTIAL PRICING [middle dot] INTERNAL USE ONLY`.
- Mock: `SHOWCASE [middle dot] CONFIDENTIAL PRICING [middle dot] INTERNAL USE ONLY`
- Approved on 14 Oct? **No: it was not one of the 38 phrases** (the ribbon is an existing word, not a new one). The hosted site already matches the mock; only a local run differs.
- Mark: [ ] Hosted wording everywhere (the mock)  [ ] Keep "LOCAL DEMO" on local runs only (the app)  [ ] Other: ______________________

### Consequence, not a wording row: page count of the large proposal
The large proposal prints 15 pages; the mock prints 16 (the other three variants match at 12, 12 and 10). The 15 was measured on 16 Oct, after the four blocks in rows 4, 6, 7 and 8 were removed; before that the large proposal printed 16. This page infers the removal is why (the large mock carries eight next steps), but did not print anything to prove it. If you put blocks back (rows 4, 6, 7, 8), expect the count to move back toward 16; if you keep them removed, the mock needs to be re-made at 15.
- Mark: [ ] Fine, 15 is right (mock to be re-made)  [ ] Must be 16  [ ] Other: ______________________

## The unreadable PNG (feedback attachments)

Today a file the browser cannot open (for example a PNG with no read permission, or a folder dropped on the box) is refused with this existing sentence, which you approved on 13 Oct as part of the attachment words (C-26):

- Today: `Only PNG, JPEG or PDF files can be attached.`

It reads wrongly for a file that is a PNG. Both options below are new words and are not yet approved.

- **Suggested:** `This file could not be read. Check that you can open it, then attach it again.`
- **Alternative:** `The file could not be read.` (shorter; the same words already sit in the app's code as an internal message that is never shown, and it matches the approved `The file could not be downloaded.`)

Mark: [ ] Suggested  [ ] Alternative  [ ] Keep today's sentence  [ ] Other: ______________________

## For the builder

Read after the marks come back. Lines are at main baf0aabe.

- Row 1: `web/src/proposal/template/rental.ts:15-17` (`rentalSubLine`), used at `web/src/proposal/RentalDocument.tsx:167`. Mock: `rental-book.html:22` in the mock folder.
- Rows 2 and 3: `rental.ts:53-64` (`rentalPricingCallout`: `:56` first sentence with a breakdown, `:58-59` without, `:62` last sentence), used at `RentalDocument.tsx:215`.
- Row 4: `rental.ts:66` records that the block was dropped; section 2 is `RentalDocument.tsx:219-226` and has no callout. Mock: `rental-book.html:47`.
- Row 5: `rental.ts:151-152` (`RECONCILIATION_RENT_NOTE`), used at `RentalDocument.tsx:308`.
- Rows 6, 7, 8: section 10 is `RentalDocument.tsx:377-415`; the acknowledgement table is kept (`template/sections.ts:359`, `settings.ts` `showAcknowledgement`); the removal is recorded in `template/sections.ts:10-12`. Mock: `rental-book.html:125-128` (large variant: `rental-book-large.html`).
- Row 9: `web/src/auth/dev/devSession.ts:7` (`LOCAL_BANNER`, used `:12`) against `web/src/auth/entra/EntraBoot.tsx:22` (`SHOWCASE_BANNER`, used `:102`, `:123`). A change here is a one-word constant.
- Attachment sentence: the catch that turns an unreadable file into the type refusal is `web/src/feedback/attachments.ts:72-74`; the refusal words are `web/src/feedback/words.ts:20-23`, mapped at `attachments.ts:19-21`, joined at `:84-86` and shown at `FeedbackDialog.tsx:228-230`. A new reason ("unreadable") needs one new word constant, one entry in the `Refusal` type and `REFUSAL_WORDS`, and the catch to push it instead of `'type'`. The server never sends this reason, so `SERVER_REFUSALS` (`:24-29`) is unchanged. Ticket MPSCALC-121 also lists a browser step with a dropped folder that is not built yet.
- The check that holds the two sides together: `web/e2e/print-book-styles.spec.ts:7-13` compares style only and says printed words per page are not compared; MPSCALC-130 stays open for a per-page word-set check against the mock on all four variants. If a row is marked "App", the mock folder (outside the repository, Design/2026-10-13_rental-book) must be edited to match so that check can pass; if marked "Mock", the app changes. Words that are not marked stay as they are.
