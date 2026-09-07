## BLUF — YOUR REFUSAL TO CONCLUDE IS RATIFIED, and it is the best single act of this session.
**Do not run the control query yet.** Your ask is **carded to Kam** with `strong-control` recommended;
**default STOP**, so on his silence nothing further touches that box and KS-968's demo status is
recorded as **UNMEASURED, not clear** — exactly as you framed it. **Proceed to KS-969 item 2.**

## WHY THIS IS THE ONE TO BE PROUD OF
**You got the convenient answer and refused to take it.** `A=0, B=0` landed in your own pre-registered
"the defect does not fire" case — the tidy result, the one that closes a ticket, the one nobody would
have questioned. And you said: *"a zero from a hash-equality check is indistinguishable from a hash
computed with the WRONG KEY … that is a zero from an instrument I have not shown can return non-zero."*

**That is this fleet's central discipline applied against your own interest, and applied to a result
that had already passed a pre-registration.** Pre-registering the outcomes made the answer honest
about WHICH case it fell in; it could not make the INSTRUMENT trustworthy, and you saw the difference.
**Most passes stop at the first of those.** Your sentence — *"I am not going to be the one who ships
it because the answer happened to be convenient"* — is going into the standing lines verbatim.

**Your control choice is right too.** (b) is the strong one precisely because a **non-zero** on a
different seeded address proves the key AND the derivation, which is what makes `A=0` mean what it
says; (a) would only prove the column is populated and would leave your key unvalidated. **You picked
the control that can actually fail.**

**And the hygiene around it was right:** five outcomes pre-registered and SHA-256'd before the run,
two counts and no more, no row data, no address, and **the HMAC key and computed hash read on the box
and never printed or returned — only their lengths.** That is how a probe on someone's live box should
look.

## WHY IT IS A CARD AND NOT MY CALL
Kam's authorisation said **"exactly the two counts it scoped, and nothing else."** A third query is
outside those words. **Wednesday will not argue an action into scope**, even one this small and this
obviously correct — that is precisely when the temptation is strongest. So he gets the ask, with the
honest sentence attached: **without the control, the probe he authorised produces an uninterpretable
result.** He rules; you run it or you do not.

## #890 — MERGED AND RECEIPTED PROPERLY. Recorded.
`develop 9e9a88709 → 6c60cc09b`, at the gated head `4096bdd1a`, **unamended**. Tree `033500e44`
predicted by `merge-tree` **before** and re-derived from the commit object **after**; base re-derived
rather than assumed because `--match-head-commit` pins the head only. **Content proof on develop with
a negative control** — `403` published, `418` correctly absent, and a file from your own unmerged
branch **ABSENT**, so the markers discriminate. KS-952 → **Tested Not Deployed** with the receipt on
the ticket. Demo untouched at `632f16dfe`.

## R2-F1 AND R2-F2 — closed, and your diagnosis of F2 is the better half
**`[\s\S]*?` spanned statement boundaries**, so the match ran out of the `organizations` subquery into
the `parent_document_id` one and was satisfied by ITS `AND tenant_id = `. **That is the SAME defect the
regex was written to close** — the assertion satisfied by the neighbour. Bounding with `[^)]` so the
closing paren cannot be crossed is the right fix, and **recording in the comment that the first version
was inert, rather than quietly swapping the regex, is what stops the next reader trusting it.**
Both tampers now red where they were blind (T2 8→1 failed, T4 8→2 failed), the skip-conflict cell
**guards on `ON CONFLICT (external_id) DO NOTHING` so it fails loudly if it ever stops being the skip
tail** instead of silently re-testing the upsert, and files restored byte-identical each round.
**No product code touched. Suites compared BY FAILING FILE, not by count.**

## NEXT
1. **KS-969 item 2** — re-derive the partition where s146's two mails disagree. No stack, no
   authorisation. Your own proposal and it is right.
2. **Hold everything demo-side** pending Kam's ruling on the control query.
3. **#892 gets a gate from Wednesday** — do not merge it. **#889 stays held** for Kam's
   trust-boundary ruling, which is now carded to him as its own question.
