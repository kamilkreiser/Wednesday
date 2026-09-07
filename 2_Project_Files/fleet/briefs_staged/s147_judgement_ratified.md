## BLUF — YOUR JUDGEMENT CALL IS RIGHT. Do not touch #890. The comments land after the merge, as KS-970 items 3 and 5.
**You read two of Wednesday's instructions as being in tension, and they were.** *"Merge #890 at the
gated head"* and *"fix the comment as part of F-2"* **cannot both be satisfied** — a comment-only
commit moves `refs/pull/890/head` off `4096bdd1a`, which is the SHA the round-2 gate drove and the SHA
the GO names. **You chose correctly, and you asked instead of assuming. Hold as you are.**

**No amendment, no re-gate. The merge GO still stands on `4096bdd1a`, and the wake is still a tap from
Wednesday once the #889 re-gate reports.**

## THE RULE THIS EARNS — Wednesday's, not yours
**When a GO names a specific head, any instruction in the same mail that would MOVE that head must say
explicitly whether it precedes the merge or follows it.** Wednesday's mail did not, so it read as
"do both", which was impossible. **That is a defect in the instruction, not in your reading of it** —
and it is the third time today a seat has had to resolve an ambiguity Wednesday shipped. The
mechanism catching them is the standing line, and it is earning its place.

## WHAT YOU DID THAT GOES BEYOND FILING
**You verified four of the six against the tree rather than relaying the gate's words**, and two of
those verifications changed the item:
- **Item 1 (F-3):** you did not just repeat it — you established **why `min(1)` cannot catch it**
  (`"   "` has length 3, and `claim()` trims to `''` → `null`, so `named` is FALSE and it falls back
  to `principalScope(caller)`). **That is the mechanism, and it is what makes the item actionable.**
- **Item 4 (F-4):** you did the arithmetic — **256 astral characters = 256 code points = 512 code
  units**, published valid and refused at runtime — **and wrote it up explicitly as NOT a reopening of
  the `maxLength` check the gate closed.** Naming what a finding is *not* is the half that stops a
  reader re-litigating a settled question.
- **Item 5 (F-5): you grepped AGAINST A CONTROL** and it changed the finding's shape — one stale
  sentence in one pre-existing cell (`ks952-rate-limit-scope.test.ts:90`), **not a pattern**, with
  `rateLimitScope.ts` showing **zero** stale hits (control: `base64url` appears 4×) and the other two
  percent-encoding mentions being yours **and correct**, because they describe the reverted state.
  **A lesser pass files "stale comments, several places" and sends someone hunting.**
- **Item 2 (F-1): you linked KS-759 as RELATED and said why it is not a duplicate** — that ticket is
  the type declaration, yours is runtime behaviour. **Correctly refusing a merge of two tickets is the
  same discipline as correctly merging six into one.**

## AND YOU WROTE YOUR OWN FALSIFICATION INTO THE TICKET UNSOFTENED
Item 3 records, in your words, that your published claim was wrong: *"My conclusion held; one of my
two supporting claims did not."* **You put that on the ticket rather than paraphrasing it into
something softer, and you read `if (!named) return principalScope(caller);` at source to confirm it
rather than accepting the gate's word.** That is the behaviour this fleet is built to protect.

## NEXT
**Nothing on #890 until the tap.** If you have capacity before it, start **KS-969 item 1** (wire actor
provisioning into a pre-suite step) — it is dependency-free and it is the unlock for the whole
systemTest credential story. **If no tap has arrived within the hour, mail and ask.**
Both #889's merge (Kam's Finding 1) and #891 (Kam's click) remain HELD and are not yours.
