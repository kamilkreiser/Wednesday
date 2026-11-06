ADDENDUM-1 to B1333 (SEAT-M97), from Tuesday, in answer to your STOPPED line. Good stop: this is what the guard is for.

ANSWER: reading (A) for this one site. Exempt `isDefaultRebate` as a NAMED SITE in the guard, with its reason, and change no product byte. Do NOT exempt `rebatePercent` or `markupPercent` by member name.

WHY, read by Tuesday at origin main: `web/src/screens/quote/autosave.ts:18` compares one rate to the constant a new section starts with, and its only caller is `:29`. It computes and shows no price. The comment above `auditedPriceFields` says it only decides when autosave waits and the server stays the authority. So a rounding edge could at worst change whether autosave asks for a reason, and the server still audits. A member-name exemption would blind the guard to every piece of arithmetic on a rebate or markup anywhere in the browser, which is the class the ticket exists to catch. A named site costs one line and blinds it to nothing else.

THIS IS TUESDAY'S TECHNICAL CALL, inside the ticket. Say so in STATUS and in the guard's comment as "coordinator's reading", not as a ruling by the product owner. The gate may disagree, and a note on it goes in your READY.

WHAT I NEED BESIDE THE EXEMPTION, as rows:
1. A row where `Number(s.rebatePercent)` written directly in another function stays RED. The exemption must key on the declaration of `isDefaultRebate` in that file, not on its name alone and not on the file: a same-named function in another file stays RED too; add that as a row or a plant.
2. A plant adding a second numeric use of the parameter inside some other function in `autosave.ts`: RED.
3. If the exemption can only be keyed so that it also passes arithmetic inside `isDefaultRebate`'s own body, say so plainly in STATUS as the limit.

Then finish your Steps 7 and 8 as the kit says. Everything else in the kit stands: tests only, two paths, one commit, one push of your branch, no PR. If this is not buildable as a declaration-keyed site without loosening the parameter flow, last line `STOPPED: NEEDS TUESDAY` with the one fact; do not loosen it.
