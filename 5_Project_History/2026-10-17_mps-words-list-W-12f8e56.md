# MPS calculator: new words that go live with the hosted deploy of main 12f8e56 (list W)

Card mpscalc-hosted-deploy-12f8e56-1017. Tapping a on that card approves these words. {…} is filled in by the app. Prepared by Tuesday from the merged code and the QA gates, 2026-10-17.

*Part 1: customer proposal, the short form (#50).*
1. "01 Proposed Solution" · "02 Commercial Schedule" · "03 Delivery, Service & Next Steps"
2. "The proposition"
3. "Proposed fleet and package price"
4. "TOTAL UPFRONT ACQUISITION"
5. "Pricing basis"
6. "{edition} pricing. Upfront customer purchase, not a financed monthly rental. Support for the {n}-month term and any software listed are included in the package values; variable usage is additional." (a pricing-policy claim)
7. "The proposed devices, coordinated through one service model."
8. "Device stream" · "Solution and quoted inclusions" · "{CLASS} · {n} DEVICE(S)"
9. "{edition} price basis • {currency} excluding GST"
10. "Variable usage charges"
11. "No monthly total is stated because usage volumes are not yet confirmed."
12. "Software bundle and credit" · "Software element" · "{n}-month value · ex GST"
13. "Separate customer Microsoft 365 / Universal Print subscriptions, extended analytics and bespoke integrations are not priced in the package unless expressly documented in the final agreement."
14. "Commercial conditions" · "Item" · "Proposal treatment"
15. "Pricing validity": "{n}-day {edition} pricing; commencement date to be confirmed" (or "To be confirmed")
16. "Invoicing / financing": "Upfront purchase; separately metered usage charges. Finance terms and recurring fixed base charges are not quoted."
17. "Standard exclusions": "Paper, large-format roll media, specialty consumables, cabling/building works, customer Microsoft subscriptions and custom integrations unless added by agreement."
18. "A practical transition from technical discovery to operational handover."
19. "{n}-month service approach" · "Service area" · "Proposed treatment"
20. "Hardware support": "{n}-month hardware support for the devices in this proposal, under final OEM and site coverage conditions."
21. "Consumables": "Managed office toner and maintenance supply through metered page charging." (with large format: "…; large-format ink, printhead and maintenance-cartridge supply billed under the agreed separate model.")
22. "Operations & reporting": "Remote triage where available, meter collection, incident coordination, service reviews and approved moves, adds and changes."
23. "Implementation sequence" · "Stage" · "Joint activity / key outcome"
24. "1. Validate": "Confirm the {n}-device BOM, site allocation, workflows, users and volumes."
25. "2. Design & stage": "Approve network and security prerequisites, configuration, reader mapping, consumables and installation schedule."
26. "3. Pilot & deploy": "Test print, scan and authentication workflows; deploy in agreed waves and provide training."
27. "4. Accept & operate": "Complete user acceptance, document support channels and commence meter-based service processes."
28. Cover sub-line "{packages} | {n}-month managed support" (the edition is removed)
29. "Credit included in this proposal"
30. "Each credit is already taken off the package price shown, ex GST."
Removed from the customer document (ruled under K-15): the pricing-interpretation callout on purchase, "not yet specified", recommended next steps, the acknowledgement note and the proposal basis. The editor drops "Proposal basis", "Still to be confirmed (one per line)" and "Next steps (one per line)", but stored values are kept.

*Part 2: screens.*
31. Home: "Deals won" / "Deals lost" (replace "Deals closed"); "Quotes marked Lost in {Month YYYY}." / "Quotes marked Lost since 1 July {YYYY}."; group name "{Deals won|Deals lost} period"
32. BOM: "Package name, e.g. Devices and supplies" (placeholder); "Type a package name before saving."; "{n} sections · {m} lines"; screen-reader endings " (end of page)" and " (end of BOM)"
33. Picker: "Tick several items and set a quantity for each, then add them together." · "Choose the device" · "Choose the device for every ticked option." · "Each quantity is a whole number from 1." · "{n} selected" · "Add 1 item" / "Add {n} items" · "Select" / "Select {sku}" · "Qty" · "Quantity of {sku}" · "Device for {sku}" · "For {device}"
34. Hint button "About {topic}"
35. Hint "Quote type": "Finance (monthly): the customer pays one monthly charge over the term, covering the devices with finance, software and printing. Outright purchase: the customer buys the items on the BOM up front, and printing is charged per page at the usage rates."
36. Hint "Optional": "An extra the customer may choose, such as a stapler or finisher. It is priced per unit and never added to a total."
37. Hint "Included": "Supplied at no charge to the customer. Its sell price is 0, but its cost still counts against the margin."
38. Hint "Credit": "A deduction, such as a trade-in or a bundle credit. Its sell price and its cost count as negative amounts."
39. Hint "Section markup" (internal): "The markup on cost for lines in this section that have no sell price, sell override or catalogue default markup of their own. After you save, each line shows the markup that will apply."
40. Hint "Section rebate" (internal): "A percentage of this section's total that is deducted from the margin. It does not change the customer's price."
41. Hint "Mono click": "The charge to the customer for each mono (black) page, in dollars ex GST. It is a price per page, not a number of pages. Leave it empty to have it calculated from supplies, or for no mono charge." It ends with "Typical: {rate} a page (an A3 colour MFP fleet quoted at standard pricing, October 2026)." The rate is the review quote's real customer mono rate, and it is written into the code.
42. Hint "Colour click": the same as 41 for colour, also with the review quote's real colour rate.
43. Hint "Ink rate": "For large-format devices: the charge to the customer for each unit of ink, in dollars ex GST. Set the unit beside it. Leave it empty for no ink charge."
44. Hint "Ink unit": "The unit the ink rate is charged per, for example ml."
45. Hint "Calculate click rates from supplies" (internal): "Works the click rates out from the consumables' cost and yield, the mono and colour margins and the pages per device. A click rate typed above is used instead of the calculated one."
46. Repeated line numbers: "Line number {n} is used by more than one line. Each line needs its own number before the quote can be saved." (plural "Line numbers {1, 2 and 3} are used by more than one line. …") · button "Give each line its own number"
47. Negative input: "{field} is below 0; enter 0 or more." It shows under the existing headline "The draft has values beyond the technical limits." with the raw code and field path on screen (to fix the headline, see card B3).
48. Licence term warning: "Line {n} ({sku}) is a {term}-month licence on a {quote term}-month quote. An outright purchase pays the software for the whole term upfront: choose the {quote term}-month licence."
49. "Supplies" (was "Supply") wherever an item class shows.

*Part 3: what a quote shows when it is calculated (#73).*
50. "This quote has usage rates per section and deal-level usage or page estimates. Use one: the deal's usage replaces the section rates."
51. "Mono pages per device per month must be a non-negative whole number." · "Colour pages per device per month must not be negative."
52. "Line {n} ({sku}) is not a device; page estimates belong on device lines." · "{model} is mono; colour pages are not allowed."
53. "A target click must be above 0." · "The target mono click is below the cost per page: the margin it needs is negative." (also colour)
54. Internal users: "Consumable {n} in the supplies list has a yield of 0; its cost per page is taken as 0." · "Consumable {n} in the supplies list has a negative cost or yield."
55. Everyone else: "A consumable in the supplies list has a yield of 0; its cost per page is taken as 0." · "A consumable in the supplies list has a negative cost or yield."
56. API-only refusals (no screen sends these yet): "usage.supplies is an internal input; setting it needs the Seller role and the internal-metrics permission (I-2)." · "usage: fixed rates are prices; setting or changing them needs the Seller role and the internal-metrics permission (I-2)." · "{path} is required (send [] for none)." · "{path}[{j}] must not be null." · "usage.inkUnit is 0 to 20 characters." · "sections, bomLines, manualItems, clickRates and usage need quoteMode 'purchase'." The .NET deserializer messages that name types (words 25-27 in gate B163) are a known Note, MPSCALC-195.

*For your information only, no yes needed (operator and deploy-log lines no browser shows):* the 9 server-start and source-store lines in gate B157 Check 11, the 11 deploy-check (PRE-1) lines in gate B161 Check 11, and the Entra script's 7 lines in gate B159 Check 10. Already ruled, so not asked again: "Finance (monthly)" / "Outright purchase" (K-20), "Customisation" (K-06) and "Add at least one device." (MPS-6).
