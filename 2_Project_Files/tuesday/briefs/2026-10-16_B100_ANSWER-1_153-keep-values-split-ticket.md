From Tuesday, 2026-10-16 16:5x AEDT, to lane A (B100). ANSWER to your QUESTION 05:48Z "B100 MPSCALC-153 governed setting".
# B100 ANSWER-1: (a). Keep the two ruled values in the words file for this PR, and SPLIT the ticket

**Ruling:** keep the two typical click rates in `web/src/components/infoHintWords.ts` as they are at `7c7ff9f`. **Do not build a governed setting.** But MPSCALC-153 does **NOT close** on this PR, because its acceptance ("values live in a governed setting or source table, not in code", your Jira GET, 16:5x) is not met.

**Why (a), not (b):** Kam ruled the values (13:14 note on the data-asks card: use the values in the 16 Oct review quote and spreadsheet) and approved the hint words. Taking them out would drop something he asked to see. The acceptance's "not in code" clause is about where the value is governed, and that belongs to the lane that owns the server and price-book files, not lane A.

**Do:**
1. Keep the source and the date in the hint, as the acceptance asks ("shows the value with its source and date"). Check it shows both. If it does not, add them in words already approved (the source string at `infoHintWords.ts`) and say so in STATUS.
2. In your STATUS and the Jira comment you post (your own lane's Jira write, as your lane brief allows), say: "153 PARTLY DONE: hint built with Kam's ruled values in code; the governed-setting half is NOT built and needs a server field + source table (outside lane A's files)." Propose ONE new BACKLOG row/ticket for that half, with the acceptance clause quoted. Leave 153 open. Do not transition it to Done.
3. Carry on with items 1-3 of ADDENDUM-1, then READY as that addendum says.
