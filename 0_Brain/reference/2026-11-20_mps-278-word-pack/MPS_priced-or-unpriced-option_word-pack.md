# WORD PACK B1747 | MPSCALC-278 | the priced or unpriced option on the two purchase documents

Written by the build seat for Tuesday, to go to the product owner before any hosted deploy (the 2026-10-20 ruling on the fifteen recommendations: "Every new customer-facing word still comes to you as a word pack before it ships, and nothing is deployed without your card"). Nothing is deployed. Branch `b1747/mps-lane-mh-unpriced-proposal-278`. All text below is SYNTHETIC (the repo fixtures `s4Proposal` and the values built in the test file); no real price, quote or price book was read.

## FIRST: the gap between the words of the second choice and the document

The second choice reads **"Show SKUs and quantities only"**. The unpriced documents show **quantities but no part codes (SKUs)**. The purchase documents print `quantity x description` today (`detail()` in `ProposalDocument.tsx`, `detailCell` in `OnePager.tsx`); they never print the Api's `code`. This lane does NOT add a code column or put `code` into any text, because that needs a new heading word or a new text pattern, which this lane may not write. So a customer who is shown "SKUs and quantities only" sees descriptions and quantities. The alternative (Q3): print the Api's `code` before the description in each detail text where the Api sent one (one pattern change in `detail()` and `detailCell`, no new heading); it is a words decision for the product owner.

## (1) The three strings

| Id | String (exact, ASCII) | Where it shows | Source (quoted) |
|---|---|---|---|
| W1 | `Customer PDF option` | the visible legend of the option group, on the proposal page of a PURCHASE quote with a loaded proposal | gap row V-63 of the v13.4.1 gap analysis: `"Customer PDF option":` (whether the prototype shows it as a visible heading is not known to this lane; it is shown as a visible legend by default) |
| W2 | `Show customer unit and extended prices` | the label of the first radio (the priced choice, selected each time the page opens) | the same row: `"Show customer unit and extended prices"` |
| W3 | `Show SKUs and quantities only` | the label of the second radio (the unpriced choice) | the same row: `"Show SKUs and quantities only"` |

- **Screen:** `ProposalPage`, in the page toolbar block (the `page-head no-print` block), after the two print buttons.
- **Condition:** shown only when the loaded proposal is a purchase proposal with packages. **Hidden** on a rental quote, on a purchase proposal without packages (it falls back to the rental view), and while the proposal is loading.
- **Not printed:** the group is in a `no-print` block; none of the three strings appears in either printed document. No string for the choice is added to the printed documents: the choice shows by what the document omits, plus one attribute that is not a word (`data-price-option="unpriced"` on the document root when unpriced; no attribute when priced).
- Every other string the lane makes visible already existed on main. A test (U10) proves by program that every text of the unpriced render is a text, or a part of a text, of the priced render of the same proposal.

## (2) The printed-text excerpt reference

The test cells U7 (two of them: the short form and the full proposal) press the print button with the unpriced choice and read the text of the document that is in the DOM at the moment `window.print` is called; oracle P (no `$`, and none of the proposal's decimal values in any display form) passes on it. The same texts for the synthetic fixture `s4Proposal` are held in the scratch dump (written by a temporary, uncommitted test through the same print flow):

| Document | File | sha256 |
|---|---|---|
| unpriced full proposal | `.tools/b1747/out/dump/unpriced-full-s4.txt` (16389 bytes) | `331d7f4c0ae47292519e45e2097b379027f7af40776e740845a390e113dca68b` |
| unpriced short form | `.tools/b1747/out/dump/unpriced-short-s4.txt` (4823 bytes) | `9570d433f16b4c1a2e0b190439d7a08f8c67ef8a61e3a1fe236d161551cbdc7b` |

**The stated limit of the oracle.** It removes and detects the figures the Api sends and the templates merge. A figure a person TYPES into a free-text narrative field of the proposal content (executive summary, client context, outcomes, principles, confirmation register) is the staff's own text and is not scrubbed.

## (3) The remaining price words (existing words, unchanged)

Every leaf text of the two unpriced dumps (the synthetic fixture `s4Proposal`) that matches the case-insensitive pattern `pric|charge|rate|total|value|GST|upfront|acquisition`, one per line, with its document and count. These words stay in the unpriced document; some speak of price without a figure. The product owner may rule on them; this lane edits none.

### full proposal (330 leaf texts, 43 distinct match, 49 matches in all)

| Count | Text | Note |
|---|---|---|
| 1 | INTEGRATED OFFICE AND LARGE-FORMAT PRINT | existing word, unchanged |
| 1 | Proposal ref DEMO-S4 (Draft) • Issued 10 October 2026 • Standard-price validity: 45 days | existing word, unchanged |
| 1 | Prepared by Datasec Solutions / HP Solutions Centre / Standard-pricing edition / Indicative, non-binding | existing word, unchanged |
| 1 | What we propose, why it fits, and its price. | existing word, unchanged |
| 1 | Usage charges the operations manager can follow month by month. | existing word, unchanged |
| 1 | 04 · Operate | existing word, unchanged |
| 1 | Keep A3 office click charging separate from large-format ink economics and specialist media. | existing word, unchanged |
| 1 | Configuration included in indicative price | existing word, unchanged |
| 7 | In the package price | existing word, unchanged |
| 1 | Included at no charge | existing word, unchanged |
| 1 | Where software is bundled with a package, it is shown at its list value with an equal credit, so it does not change the package price. Section 6 shows the reconciliation. | existing word, unchanged |
| 1 | Marked-up sheets captured and shared without a separate scanner. | existing word, unchanged |
| 1 | 5. Fleet Schedule and Purchase Price | existing word, unchanged |
| 1 | Each package, its quantity and its price for the full term. | existing word, unchanged |
| 1 | Optional items are priced per unit and are not part of any package total. | existing word, unchanged |
| 1 | What the upfront package represents | existing word, unchanged |
| 1 | Customer purchases fleet upfront. No financing rate or monthly device rental has been supplied. | existing word, unchanged |
| 1 | Pricing currency | existing word, unchanged |
| 1 | Australian dollars (AUD), excluding GST. | existing word, unchanged |
| 1 | Standard price validity | existing word, unchanged |
| 1 | This proposal specifies 45-day validity. Supplier quote date, pricebook availability, stock and final written confirmation must be established before acceptance. | existing word, unchanged |
| 1 | Upfront package is distinct from variable MFP page charges and separately billed LFP ink consumption. | existing word, unchanged |
| 1 | 6. Usage Charges and Software Economics | existing word, unchanged |
| 1 | How page usage is charged, and how software is treated. | existing word, unchanged |
| 1 | Device-class usage rates | existing word, unchanged |
| 1 | Customer supply or separately quoted | existing word, unchanged |
| 1 | No monthly fleet rental, finance interest rate, annual uplift or minimum volume charge has been provided. | existing word, unchanged |
| 1 | No standalone monthly software subscription should be inferred from the net-zero upfront bundle line. | existing word, unchanged |
| 1 | Any agreed nonstandard freight, site works, additional licences, service enhancements or bespoke configurations require separate pricing. | existing word, unchanged |
| 1 | Consumption charges will follow validated meter and supplier billing data, subject to final service schedules. | existing word, unchanged |
| 1 | Toner and routine maintenance consumables handled under the MFP metered page charge arrangement. | existing word, unchanged |
| 1 | Ink, printhead and maintenance-cartridge supply workflow, subject to agreed separate usage billing. | existing word, unchanged |
| 1 | Structured approval and implementation process. Out-of-scope changes may be separately charged. | existing word, unchanged |
| 1 | The priced package specifies next-business-day hardware service, not an unconditional four-business-hour on-site fix or attendance SLA. Exact hours, remote locations, parts commitments, consumables logistics and remedies must be documented in the executed service schedule. | existing word, unchanged |
| 1 | Deploy in agreed waves, configure devices, deliver Large Format onsite training and migrate operations. | existing word, unchanged |
| 1 | Commercial: confirm invoice structure, usage measurement, rate schedule and acceptance of any implementation variations. | existing word, unchanged |
| 1 | Agree policy interactions and supported authentication methods. Any CA re-design or exception must be separately approved and scoped. | existing word, unchanged |
| 1 | Annual / strategic | existing word, unchanged |
| 1 | Confirm the large-format ink rate basis. | existing word, unchanged |
| 1 | Sets the usage charge for signage. | existing word, unchanged |
| 1 | Paper, wide-format roll media, specialist substrates and finishing consumables; electrical or structured-cabling works; customer networking or Microsoft subscriptions not specifically listed; Microsoft Conditional Access policy re-engineering; custom line-of-business integrations; non-standard or after-hours delivery; relocation; optional speed licences; and damage caused by misuse, unsuitable environmental conditions or unauthorised repairs. | existing word, unchanged |
| 1 | This proposal is for commercial and technical review, is not a tax invoice or binding offer, and remains subject to supplier approval, final Synthetic Regional Logistics Co configuration, executed MPS/support terms and confirmed usage-rate definitions. | existing word, unchanged |
| 1 | Price validity | existing word, unchanged |

### short form (105 leaf texts, 14 distinct match, 14 matches in all)

| Count | Text | Note |
|---|---|---|
| 1 | Proposal ref DEMO-S4 (Draft) • Issued 10 October 2026 • Standard-price validity: 45 days • Prepared by Datasec Solutions / HP Solutions Centre / Standard-pricing edition / Indicative, non-binding | existing word, unchanged |
| 1 | Proposed fleet and package price | existing word, unchanged |
| 1 | Pricing basis | existing word, unchanged |
| 1 | Standard pricing. Upfront customer purchase, not a financed monthly rental. Support for the 48-month term and any software listed are included in the package values; variable usage is additional. | existing word, unchanged |
| 1 | Standard price basis • AUD excluding GST | existing word, unchanged |
| 1 | Variable usage charges | existing word, unchanged |
| 1 | Customer supply or separately quoted | existing word, unchanged |
| 1 | No monthly total is stated because usage volumes are not yet confirmed. | existing word, unchanged |
| 1 | Separate customer Microsoft 365 / Universal Print subscriptions, extended analytics and bespoke integrations are not priced in the package unless expressly documented in the final agreement. | existing word, unchanged |
| 1 | Pricing validity | existing word, unchanged |
| 1 | 45-day standard pricing; commencement date to be confirmed | existing word, unchanged |
| 1 | Upfront purchase; separately metered usage charges. Finance terms and recurring fixed base charges are not quoted. | existing word, unchanged |
| 1 | Managed office toner and maintenance supply through metered page charging; large-format ink, printhead and maintenance-cartridge supply billed under the agreed separate model. | existing word, unchanged |
| 1 | 4. Accept & operate | existing word, unchanged |

**Sentences that point at content the unpriced document no longer holds** (listed for the product owner; not edited):
- Full proposal: "Where software is bundled with a package, it is shown at its list value with an equal credit, so it does not change the package price. Section 6 shows the reconciliation." (the credit callout, the reconciliation callout and the amount column are omitted when unpriced).
- Full proposal: "Each package, its quantity and its price for the full term." (the strapline of the schedule section) and the title "5. Fleet Schedule and Purchase Price".
- Short form: the heading "Proposed fleet and package price" and the "Pricing basis" callout (kept on purpose: existing words with no figure).
- Both documents keep "Included in the package price" style table cells and the validity lines (a day count, not a price).
- No heading is left with nothing under it: the closed list of omitted headings and callouts (test U5) is: Consumption and media; Package price by class; Reconciliation; How future usage charges will be calculated; Usage formula; Optional enhancement; Credit included in this proposal; and in the short form the class list label.

## (4) The removed sites, as built (by id)

Property: in the unpriced render no element prints an amount the Api sent and no template sentence is built from one; every other element is unchanged. As built (all in `ProposalDocument.tsx` unless the id starts S, which is `OnePager.tsx`; P is `ProposalPage.tsx`):

| Id | What was removed when unpriced |
|---|---|
| F1 | cover tile with the purchase total; the strip becomes a two-column grid (inline style, an element key so toggling back leaves no leftover style) |
| F2 | snapshot table: class subtotal columns, the package price column and the total row; heads `Fleet element`, `Qty` remain |
| F3 | the credit callout |
| F4 | the large-format consumption heading and its sentence (the ink rate) |
| F5 | schedule table: the line total column and the total row |
| F6 | the class-split heading and table |
| F7 | optional-items table: the unit price column (heading and the note stay) |
| F8 | the reconciliation callout |
| F9 | usage table: the customer rate column; the media row keeps component, class, basis |
| F10 | the rate-method heading and the usage-formula callout (the method note stays) |
| F11 | software reconciliation table: the amount column (a credit row is still labelled) |
| F12 | the optional-enhancement callout |
| F13 | summary table rows: price, class rows, inc-GST row, rate rows; customer, equipment, term, monthly, validity stay |
| S1 | cover tile with the purchase total; two-column grid as F1 |
| S2 | package table: the line total column, the total cell of the "more packages" row, the total row; the colgroup has three widths (25%, 67%, 8%) |
| S3 | the class list |
| S4 | the credit callout |
| S5 | rates table: the customer rate column; the more-rates row spans three columns; the media row keeps component, class, basis |
| S6 | the rate-method sentence; the no-monthly-total sentence stays |
| S7 | software table: the amount column (first head only) |
| P1-P3 | the page: state `priced` (true each time the page opens), the option group after the print buttons (purchase only), `priced` passed to both purchase documents |

No price site was found that the kit did not list (the oracle finds none on four fixtures: s4 draft, s4 approved, five classes with a deal pair, eight packages).

## (5) What is NOT in this lane

- **The rental documents** (the rental book and the rental short form) stay priced and the option is not shown on a rental quote (D2). A rental unpriced option is a separate lane.
- **A SKU column or the Api's part codes in any text** (D3): see the gap written first above.
- **A durable record of the choice** (D4): the choice is page state (default priced each time the page opens) plus the `data-price-option` attribute on the printed document's root; there is no member on the draft or the proposal, no audit event and no browser storage. So "the choice is recorded" is met in the page-and-document sense only.
- **A real print-to-PDF row** (Q6): the proof is a test over the printed text in jsdom, not a PDF.

