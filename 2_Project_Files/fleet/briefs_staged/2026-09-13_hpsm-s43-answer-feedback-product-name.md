BLUF. **(b) is RULED.** Every user-facing feedback string takes the product name from `brand.ts` (`PLATFORM_DEFAULT_BRAND.productName`, currently "Policy Composer"). Feedback stays registered against HPSM internally: the API, the sweep and the stored records.
- **SUPERSEDES** the line in Tuesday's S43 brief (07:05:44Z) that required "HPSM Policy Composer" in every feedback string. That wording was Tuesday's, not Kam's.

## Why
- **Kam's own words** (Tuesday's terminal, 16:53 AEST, verbatim): *"Naturally change all settings so that any feedback is registered against HPSM and works properly."*
  - He asked for feedback to be registered against HPSM. He did not ask for "HPSM" in the on-screen name.
- **`apps/web/src/brand.ts`** (read by Tuesday on the main checkout) sets `productName: "Policy Composer"`. Its header comment says "No HP marks in any profile we ship (Q-03)".
  - HPSM `5_Project_History/history.md:581` records Q-03 as a working assumption Kam accepted.
- The result is one product name on screen, and the page title no longer reads "HPSM Policy Composer feedback · Policy Composer".

## How
- Take the name from `brand.ts` (`PLATFORM_DEFAULT_BRAND`, `documentTitle`). Do not hardcode "Policy Composer" anywhere in feedback/**.
- A copy change inside feedback/** only, before the feedback READY FOR QA, as you proposed.

## Not decided here
- **W45-p2** ("HP Security Manager" in the S1 and S7 subtitles, checked against Q-03) stays Kam's decision. This ruling does not touch it.
