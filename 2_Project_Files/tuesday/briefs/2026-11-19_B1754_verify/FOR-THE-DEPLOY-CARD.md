# For the deploy card: what to measure before any write (after this change lands)

Each line: what to measure, how, the expected reading, and what to do otherwise. Values are compared by hash or by
boolean only; no id or setting value is printed.

1. **Live names.** List the site's app setting names (names only). Expected: exactly the 18 names of
   `infra/env/showcase.app-setting-names.txt` minus `MpsCalc__Templates__Path`, so 17 (equal to the 16 November saved set).
   Any extra live name: STOP (the apply would remove it). Any missing name: STOP and explain.
2. **Live feedback path.** Hash of the live `MpsCalc__Feedback__Path` equals the hash of `/home/data/feedback/`.
   Otherwise STOP (the apply would change it).
3. **The ids supplied are the live ids.** Before the what-if, hash of `MPSCALC_API_CLIENT_ID` equals the hash of the live
   `AzureAd__ClientId`, and hash of `MPSCALC_SPA_CLIENT_ID` equals the hash of the live `MpsCalc__Spa__ClientId`; the two
   differ from each other. Otherwise STOP. (The template refuses only a wrong LENGTH: any 36-character value, a swapped
   pair, or 36 spaces passes the local compile.)
4. **The other live values.** Each literal the file sets (10 shared names) and the derived `AzureAd__Audience`,
   `MpsCalc__Spa__ApiScope`, `AzureAd__Instance`, `AzureAd__TenantId`, `AllowedHosts` compare equal by hash to what the
   file would send with the supplied ids. Expected: all equal.
5. **Refusal without ids (first live proof).** Run the what-if command once with both id variables UNSET. Expected: it
   stops at the parameter file (`BCP427` naming each variable) before any request; rc non-zero. If it reaches Azure:
   STOP (the local refusal is not in the path).
6. **Apply-time length rule (UNMEASURED so far).** Optional: a what-if with `-f infra/main.bicep` and an inline empty id
   should be refused by template parameter validation (`minLength` 36) before any change is listed.
7. **What-if with the ids.** Expected: on the app settings resource, exactly one difference, the added
   `MpsCalc__Templates__Path` (no Delete, no Modify of any other setting; if the what-if masks values, rely on items 1 to
   4). The site, plan, both publishing policies and the resource group: no change (the template's other properties are
   byte-identical to main's compiled template). Budget: NO change on `properties.timePeriod.startDate` (expected
   `2026-10-01`; earlier what-if noise on `endDate` and `sku.tier` is the known kind).
8. **Budget start on an update (UNMEASURED).** The Consumption budget API's published rule refuses a past start date on
   create; whether it refuses the SAME past start on an update is unknown. If the what-if or the create reports a budget
   error, note that the budget and the app settings resource have no dependency, so the settings may already be written
   when the deployment ends Failed: read the live names and values back (items 1 to 4) after any failure.
9. **Scope.** The template deploys at subscription scope (`targetScope = 'subscription'`): it writes a subscription-level
   deployment record and re-asserts the resource group and its tags (unchanged by this change).
10. **Read back after the create.** Live names equal the full 18-name list; feedback path hash unchanged; ids hashes
    unchanged; budget start `2026-10-01`; then the template-store check needs a signed-in user (the only machine login is
    expired), which stays a separate question.
