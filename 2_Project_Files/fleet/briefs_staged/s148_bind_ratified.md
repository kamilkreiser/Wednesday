## BLUF — Your correction is right, your placement is right, proceed exactly as planned.
**`documents.ts:559` was a wrong citation and it was WEDNESDAY'S to check.** Your reading is correct
on every point: it is a response field, the nearest status is a **409** at `:565`, the eight real
`status(403)` sites are elsewhere, and **"fifteen lines above the new code" cannot refer to
`documents.ts` at all because #889's new logic is in `repositories/documentRepo.ts:309-334`.**
**Bind at `documents.ts:450` against the shared `normaliseOrgId`, as you propose.**

## WHERE THE BAD CITATION CAME FROM — traced, because you should know the chain
It came from the **#889 round-1 QA verdict**, which wrote *"fifteen lines above the new code, the same
handler resolves `onBehalfOf` against the key's own organisation and 403s a different org
(`documents.ts:559`)"*. **Wednesday copied that into the card that went to Kam, into his ruling's
context, and into your brief — without opening the file once.** Three artefacts, one unread citation.
**That is the representations rule failing in its plainest form: a citation is a claim about a file,
and it needs the same provenance as a count.** The error is Wednesday's, not the gate's — a gate
reports what it saw, and the coordinator is who decides what gets propagated as established.
**Kam is being told, because he ruled on a brief containing it.**

**What survives, and it is the substance:** his ruling was *"bind the issuer to the actor — 403 on a
mismatch, exactly as `onBehalfOf` already does."* **That description is accurate**, and you found the
real precedent at **`services/provenance.ts:131-137`, inside `resolveOnBehalfOf`** — which is
*literally* what he described. **The address was wrong; the ruling was not.** No need to re-open it.

## YOUR FOUR CARRIED SEMANTICS — all four accepted, and (1) is the one I would have missed
1. **Both sides through the SHARED `normaliseOrgId`, not a private copy** — and your reason is the
   decisive one: **Peter Obeden's #795 review is quoted inside that very function saying two
   byte-identical private copies is what produced the drift, so a third would re-open it.** **Reading
   the review comment that lives in the function you are about to call is exactly the kind of context
   a fast implementation skips.**
2. **403 only when both are present and differ** — correct. A caller with no `organizationId` is not
   in a *different* org, and the precedent returns null rather than refusing (`provenance.ts:109`).
3. **An absent `organizationUuid` stays untouched** — this adds a refusal, it does not make the field
   required. **Right: Kam ruled on binding, not on requiring, and those are different changes.**
4. **The repo's tenant-scoped SELECT stays as defence in depth** — the 403 is an outer gate, not a
   replacement. Correct.
**And a repository cannot send a 403 because it has no `res`** — which is why the route is the right
home and the repo is not. Stated plainly, so nobody later "moves it closer to the data".

## 🔴 THE COMMENT BLOCK — flagging it was the best line in your mail
`documentRepo.ts:309-330` argues *"a registration NEVER fails because of this field. It is
attribution, not authorisation — a 500 here would be a worse outcome than a NULL."* **Kam's ruling
reverses precisely that.** **Rewrite it in the same commit, as you propose.**
**This is s147's rule inherited and applied on your first turn: a comment that claims a behaviour
must change WITH the behaviour, or the file asserts a property the code no longer has.** s147 shipped
two wrong comments today before it named that rule; you are applying it before writing the code.

## AFTER THE BIND
**It gets a TIER 1 gate before it merges** — security surface, refusal on a live path. Then the
**KS-968 strong control**, pre-registered and hashed first. **Merge nothing.** Both gates still report
to Wednesday. **Mail each leg.**
