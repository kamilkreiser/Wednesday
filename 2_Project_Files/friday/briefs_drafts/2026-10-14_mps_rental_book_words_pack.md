# DRAFT · MPS Commercial Calculator · rental full proposal book: words pack (card `mpscalc-rental-book-words-1014`)

**For:** Friday (laptop coordinator), to back the words card Kam reads. Datasec / MPS Commercial Calculator only. **Status:** DRAFT. Nothing deployed, nothing posted.
**What it covers:** the new words of the rental full proposal book (built by B94 @ `9e8fd68`, gated by B95 **GO WITH NOTES**, round 1 of 2, 0 Blocker, 0 Major; being merged as PR #40). The hosted site does not change until Kam rules the card.

**Sources (read only):**
- Gate: `Briefs/2026-10-14_B95_STATUS.md` (records worktree `.tools/wt-B95-records`): Check 8 NEW WORDS table `:342-368`, RETIRED `:372-374`, column-sum measurement `:232-242`, absent-parts edge `:154-156`, M-1 `:405-410`, M-4 `:419`.
- Mock words: `1_Project_Definition/Design/2026-10-13_rental-book/NEW_WORDS.md` §A, read with `git show main:<path>` (main `9db8db0`). Gives each phrase's full text with its merge fields.
- Builder: `Briefs/2026-10-13_B94_STATUS.md` NEW WORDS `:264-272`, `[B94-2]` `:202-209`.

**Counts (each read from the B95 STATUS):** **38** new phrases (`:343` "the mock's 38"; `:368` "38/38 rendered verbatim; 0 missing; 0 reworded"). **0** other new strings (`:369`). **1** retired string, plus its screen-reader link (`:13`, `:372-373`). Mock §A heading also says 38. B94 STATUS: "Other user-visible strings I added: 0".

---

## 1 · The 38 new phrases

`{term}`, `{customer}`, `{currency}`, `{n}`, `{letter}`, `{site}` are filled from the quote. Where the gate printed the filled-in sample (typical quote: 60 months, $1,826.20 a month), it is shown in brackets. Rows 8 and 29 are the two the gate flagged (see §3).

| # | Phrase (verbatim) | Where it shows |
|---|---|---|
| 1 | `{term}-month rental  \|  STANDARD PRICING` (sample: `60-month rental  \|  STANDARD PRICING`) | Cover, line under the title |
| 2 | `monthly charge · ex GST` | Cover, headline figure tile |
| 3 | `Component` | §1 snapshot, table heading |
| 4 | `Amount, ex GST` | §1 snapshot, table heading |
| 5 | `TOTAL MONTHLY CHARGE` | §1 and §4, total rows |
| 6 | `Contract value ({term} months), ex GST` (sample: `Contract value (60 months), ex GST`) | §1 row under the total; §10 label |
| 7 | `Datasec proposes a managed print fleet for {customer}, supplied as a {term}-month rental for one monthly charge, ex GST. The monthly charge is itemised: a base charge for the devices and their service, software where a line lists it, and mono and colour print at the quoted monthly page volumes and the agreed page rates.` | §1 executive summary (default text; the seller can edit it) |
| 8 | `The monthly charge is the sum of the four components above, for the fleet, options and software in this proposal. It includes print at the quoted monthly page volumes and the agreed mono and colour page rates. The contract value is the total of the monthly charges over the {term}-month term.` | §1 pricing note. **Fix M-4 applies to older quotes** |
| 9 | `Applicable tenant subscriptions and the detailed deployment calendar have not been supplied.` | §2 "Not yet specified" |
| 10 | `Stream {letter} · {site}` (sample: `Stream A · Sample site one`) | §2 fleet split, card title per site |
| 11 | `Site not stated` | §2 card for lines with no site |
| 12 | `Configured Fleet` | §3 title |
| 13 | `The options and software configured on each line.` | §3 line under the title |
| 14 | `Amounts are in {currency}, excluding GST.` (sample: `Amounts are in AUD, excluding GST.`) | §3, §4, §5 note |
| 15 | `Fleet Schedule and Monthly Charges` | §4 title |
| 16 | `Each line, its quantity and its monthly charge for the full term.` | §4 line under the title |
| 17 | `Devices and rates` | §4 sub-heading (first table) |
| 18 | `Monthly charges by line` | §4 sub-heading (second table) |
| 19 | `What the monthly charge includes` | §4 sub-heading |
| 20 | `The devices and the configured options listed for each line.` | §4 bullet |
| 21 | `Hardware support and service for the full term.` | §4 bullet |
| 22 | `Software where a line lists it.` | §4 bullet |
| 23 | `Mono and colour print at the quoted monthly page volumes.` | §4 bullet |
| 24 | `Customer rents the fleet for one monthly charge, ex GST, for the term.` | §4 supply model, "Supply model" row |
| 25 | `{term}-month term` (sample: `60-month term`) | §4 supply model, row label |
| 26 | `Monthly charges for {term} months; commencement and entitlements subject to final contracts.` | §4 supply model, row value |
| 27 | `Configured options` | §4 supply model, row label |
| 28 | `Base charge (device and service) $… + Software $… + Mono print $… + Colour print $… = $… ex GST per month.` (sample: `Base charge (device and service) $1,138.55 + Software $34.40 + Mono print $212.85 + Colour print $440.40 = $1,826.20 ex GST per month.`) | §4 reconciliation note |
| 29 | `The total monthly charge is the sum of the line monthly charges in the schedule above.` | §4 reconciliation note. **Fix M-1** |
| 30 | `Page rates by line` | §5 sub-heading |
| 31 | `Software is charged per device per month at the rates in section {n}.` (sample: `section 3`) | §5, when a line has software |
| 32 | `Each line's monthly charge = quantity × (base charge per device + mono pages × mono rate + colour pages × colour rate + software per device), ex GST.` | §5 formula note |
| 33 | `The monthly charge is quoted for the listed fleet, options, software and monthly page volumes; a change to any of them is re-quoted.` | §5 financial boundaries, line 1 |
| 34 | `{term}-month hardware support for the rented equipment as listed in the fleet schedule.` | §6 service, row 1 |
| 35 | `… No optional analytics licence has been included in the stated $… ex GST monthly charge.` (sample ending: `$1,826.20 ex GST monthly charge.`; the first part is existing template text) | §8 optional enhancement note |
| 36 | `Monthly charge` | §10 summary label |
| 37 | `Rental term` | §10 summary label |
| 38 | `Page rates` with the value `Per line, as listed in section {n}, ex GST` (sample: `section 5`) | §10 summary label and value |

Gate result: 38 of 38 print word for word; none missing, none reworded; no other new words (`:368-369`).

**Not new (reused, already approved):** the price-breakdown labels `Base charge (device and service) / month`, `Mono print / month`, `Colour print / month`, `Options are included in the base charge.`; `+{n} more`; and the existing device, option and software table headings and captions (B95 `:371`; B94 `:267-270`).

## 2 · Retired (1)

| | Sentence | Was |
|---|---|---|
| R-1 | `For purchase quotes only: a rental quote has no proposal template yet.` | The reason shown beside the greyed-out Short-form button on a rental quote, with its screen-reader link. Both are gone: rental quotes now have a proposal. |

Also no longer shown **on opening** a rental quote: today's one-page view. It now appears only when Short-form is printed (B95 `:374`). Not a word change.

## 3 · The two fixes the gate found (proposals; Kam rules)

### Fix 1 · M-1 (row 29, §4)

| | Text |
|---|---|
| Today | `The total monthly charge is the sum of the line monthly charges in the schedule above.` |
| **Proposed** | `The total monthly charge is worked out for the whole fleet. Each line's monthly charge is rounded to the cent, so the line charges above may not add up exactly to the total.` |

**Why it is wrong today (B95 measurement, `:232-242`, M-1 `:405-410`):**
- The gate made 60 random quotes on the live calculator engine (2 to 8 lines each).
- On **23 of 60 (38 %)**, the line charges as printed do not add up to the printed TOTAL. They are a cent out (±1 ¢).
  - Example CS04: lines add to `$9,058.32`, TOTAL `$9,058.33`.
  - Example CS07: lines add to `$3,721.23`, TOTAL `$3,721.22`.
  - Test fixture of two lines at $10.005: `$10.01 + $10.01 = $20.02` against a TOTAL of `$20.01`.
- Cause: each line is rounded to the cent on its own, and the total is worked out for the fleet, not by adding the rounded lines (B94 `[B94-2]`, `:205`).
- The same cause gives 87 column cents differences in the "Monthly charges by line" table's columns against its TOTAL row. No sentence claims those columns add up, so no word change.
- Still exact: the four parts add up to the monthly charge on **60 of 60** (Kam's cents ruling holds). Row 28's sum is true.

**Why "may not add up exactly" and not "by a cent":** the gate measured a cent at most on 2-8 lines. Each line can round by up to half a cent, so a fleet of many lines can be out by more. The proposed wording stays true at any size.

### Fix 2 · M-4 (row 8, §1, older approved quotes only)

| | Text |
|---|---|
| Today, on every quote | `The monthly charge is the sum of the four components above, for the fleet, options and software in this proposal. It includes print …` (row 8) |
| **Proposed, only when no breakdown is stored** | `The monthly charge covers the fleet, options and software in this proposal. This quote was approved before charges were itemised, so no breakdown is shown. It includes print at the quoted monthly page volumes and the agreed mono and colour page rates. The contract value is the total of the monthly charges over the {term}-month term.` |
| Quotes with a breakdown | Unchanged (row 8 as built) |

**Why (B95 `:154-156`, M-4 `:419`):** rental quotes approved before price breakdowns were stored keep only the monthly total and the contract value. Their book shows no components, yet §1 still says "the sum of the four components above". The hosted site has quotes like this. The gate tested a real one written by the older code.

### Also noticed (not one of the two fixes; for Kam's note under b if he wants it)
Row 8's last sentence, `The contract value is the total of the monthly charges over the {term}-month term.`, holds only for the unrounded charges. Printed monthly × term is a few cents away from the printed contract value. Example LIVE1: `$4,153.37 × 60 = $249,202.20` against `$249,201.99` printed (B95 `:241`, M-1 `:406`). The sentence does not say "monthly × term", so the gate did not grade it as a separate fix.

## 4 · What each option does
- **a**: approve all 38 and the retirement, with Fix 1 and Fix 2 as proposed. Friday has a seat change the two sentences, gets them re-checked, deploys to the hosted site, and tells Kam.
- **b**: approve with changes Kam lists in a note. Name rows by number (1-38) or "Fix 1" / "Fix 2". Changed words go through a seat and a check before the deploy.
- **c**: hold. The book stays merged on main and is not on the hosted site.

Default if no tap: nothing goes on the hosted site; the book stays merged but unseen.


## Fix 3 (added by Friday, 02:0x)
- **Today (row 8, last sentence):** "The contract value is the total of the monthly charges over the {term}-month term."
- **Measured (B95 STATUS :241):** $4,153.37 × 60 = $249,202.20; the book prints $249,201.99 (the server works the contract value out before rounding).
- **Proposed:** "The contract value is worked out for the whole {term}-month term, so it can differ by a few cents from the monthly charge multiplied by the term."
