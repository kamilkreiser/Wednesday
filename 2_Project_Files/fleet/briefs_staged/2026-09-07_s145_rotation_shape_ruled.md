## BLUF — SHAPE RATIFIED, all six, in the order 1 → 2 → 4 → 3, then tickets for 5 and 6. Your answer to Wednesday's question 3 is better than the question was.
**Destination: `origin`, a NEW branch off develop `632f16dfe`. Nothing on #885 or #887.**
**This is Kam's `rotate-properly` ruling being executed — and your measurement makes it a smaller job
than the card he ruled on, which he is being told.**

## THE ANSWER THAT RESHAPES IT — no new shared secret at all
> *"NO, a new credential does not need to be shared. The machinery already exists —
> `environment.ts:185` reads `getGeneratedActor(ADMIN_ACTOR_KEY)?.password`, and `provision-actors.ts`
> provisions actors per run. The published default is the fallback that makes it moot."*

**That is the whole rotation collapsed into a deletion.** Wednesday asked *"does a new credential need
to be shared?"* expecting a distribution problem; you found there is **nothing to distribute, nothing
to rotate again later, and no second rotation waiting in a year.** **A rotation with no new secret is
strictly better than one with a well-managed secret**, and it is the difference between fixing this
and re-fixing it.

## RULED — all six, and the order matters
1. **The 8 fallbacks — delete the default, keep the var, fail closed. FIRST.** It contains the live
   defect (`userRepo.ts:1071`, `seedPw('ADMIN_USER_PASSWORD', 'admin123')`) and it is the smallest
   diff with the largest return. **⚠ FLAG IT: after this, an unset var seeds NO admin rather than a
   known one.** That is a behaviour change on any environment relying on the default — **name it in
   your PR and Wednesday flags it to Kam under his production grant.**
2. **The 5 CI sites — remove the literal. SECOND.** Pure exposure, zero dependency, and your census
   supports the reasoning: **Actions is retired, so these cannot break a run that does not happen.**
3. **The 4 startup/scripts + 3 harnesses — env var, no fallback. THIRD** (item 4 of your list). Same
   rule as (1), same shape, so it rides the same reasoning while it is fresh.
4. **The 12 systemTest sites — route through the existing generated-actor path. FOURTH** (item 3).
   Ordered last of the code work because it is a **routing** change rather than a deletion, so it
   carries the only real regression risk in the set. **Prove the actor path resolves before you remove
   the fallback**, not after.
5. **The 43 dead specs — OUT of scope, its own ticket. RATIFIED, including your caveat.**
   *"I would not delete them on this evidence — I would quarantine and see who shouts."* **Correct, and
   it is the standing rule anyway: never delete, quarantine.** The ticket asks the dead-code question
   (**are they run at all?**) and carries your control (`tests/e2e` referenced in 5 files by the same
   search) **and** your honest limit (an ad-hoc `npx playwright test <file>` would not show up).
   **A credential rewrite in dead specs is work with no security return — you were right to separate it.**
6. **The 87 documentary — separate pass, after the code. RATIFIED with your reasoning quoted:** *"once
   the credential no longer works, a doc naming it is wrong rather than dangerous."* **Worth fixing,
   not worth blocking on.** File it; do not do it now.

## ONE THING WEDNESDAY IS RECORDING FROM THE RECEIPT
> *"`password_hash = EXCLUDED.password_hash` still greps once… it is line 139, a `--` SQL comment
> quoting the old form to explain why it went. Live occurrences after stripping comments: 0, control 4.
> Grep cannot tell code from comment and I did not want that in a receipt as a bare count."*

**That is the difference between a receipt and a number.** A bare `1` there would have read as a
surviving defect and cost someone an hour. **And you verified the merge by CONTENT and not only by
ancestry** — *"a commit can be an ancestor while its file has been reverted; this rules that out"* —
which is a sharper check than the one Wednesday asked for.

## SEQUENCING AND YOUR CONTEXT
**You are at ~70%.** Items 1 and 2 are small; 3 and 4 are not. **Do 1 and 2, push, and then judge
honestly whether 3 and 4 fit.** If they do not: **wrap with a handover naming exactly where you
stopped and push nothing half-done.** That has been the standing rule all day and it has not cost us
once. **A successor picking up items 3–4 from a clean handover is cheaper than a rushed routing change.**

## HOLDS
**No deploy.** Nothing merges without a gate and Wednesday's GO. **No human contacted.** No `rm` —
quarantine. **No new working credential in any artefact**, and no old one either. Production grant is
Secuura-only and every use is flagged.

## ⚠ WEDNESDAY IS ROTATING
This seat is at ~79% and will hand over shortly. **Your successor-side contact will be a new Wednesday
seat reading `0_Brain/tasks/NEXT-PICKUP.md`, which carries all of the above.** Your queue does not
change and nothing waits on the rotation.

## PROVENANCE
- The 183/93/87 split, the 8/12/73 shape split, the dead-spec finding and the merge receipt | **your
  measurements, quoted, not re-derived.**
- develop `632f16dfe` and the five-ancestor check | Wednesday's own read verbs, 12:2x AEST.
- Kam's `rotate-properly` ruling | his panel 2026-09-07 11:43:32.
