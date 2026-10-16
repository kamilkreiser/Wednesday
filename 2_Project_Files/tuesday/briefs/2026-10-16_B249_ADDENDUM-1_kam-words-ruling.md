From Tuesday. Datasec / HPSM-POC. ADDENDUM-1 to B249 (hosted deploy of main d916baf). It answers B249 step 3's approval condition; everything else in B249 stands.

## Kam's ruling on the words (live board, view=tuesday, 2026-10-16 12:11:53 AEDT, read by Tuesday with kam_msgs.sh, source=live)
> *"Decision hpsmpoc-hosted-words-9-b241-1016: a — Approve all 9 as written; deploy main to hosted"*

The card listed these nine, verbatim (from B243_STATUS.md:95, the strings #152 adds):
- Admin feedback screen: "Filter by state" · "All states" · "Waiting to be sent" · "Sent" · "Failed" · "Withdrawn" · "No feedback in this state." · "Choose All states to see every item."
- Follow-up message: "At most 1 follow-up can be open at once; withdraw one first."
Plus the already-approved "The report is taking longer than usual" (POC-12).

## How step 3 now reads
1. Your sweep is still the measurement. Any customer-facing string you find that is NOT one of the ten above is unapproved.
2. **The -229 reason sentence** ("The upload stopped before it finished, so nothing was read. Upload the files again.") was NOT on the card. If your step 2a/4 measurements show imports are OFF on hosted (ImportsEnabled false, no override), the sentence cannot reach a hosted screen: it does NOT block this deploy. Record it in STATUS under "Open: words for Kam". If imports would be ON: STOP.
3. If the sweep finds any OTHER unapproved, reachable customer-facing word: STOP as B249 says, listing it with file:line.
4. If your sweep's text for any of the nine differs from the card's by even one character (e.g. the follow-up sentence's pluralisation), report the exact text you found and STOP: Kam approved the card's wording.

## Records
B250 (seat G) owns records. Name this ruling (verbatim, with its time) in your STATUS so G can record it as a C-entry.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 12:2x
