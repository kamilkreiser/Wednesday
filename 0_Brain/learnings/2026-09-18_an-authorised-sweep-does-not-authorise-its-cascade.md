---
date: 2026-09-18
type: principle
source: "Seat A (Secuura/Blockchain) mail 2026-09-17T23:57Z: Linear's issueArchive CASCADES to sub-issues; an authorised 22-ticket archive sweep took 4 live tickets with it, including In-Progress security KS-801. The seat noticed and restored all four."
status: live
supersedes: ""
tier: W
---

# An authorised sweep does not authorise what the API cascades to

**The lesson:** Kam authorising an action on a NAMED SET authorises it on that set and
nothing else. If the API silently extends the action to related objects, the extension is
**unauthorised** — it is a separate act that nobody approved, and it must be enumerated and
consented to before the sweep runs, not discovered after.

**Context:** Kam ruled 2026-09-18 09:15 *"archive all the items that have been done."* Seat A
correctly derived the set: 21 `Done` + KS-1056 `Duplicate`, holding back the 4
`Tested Not Deployed` and 2 `Canceled`. The set was right and the authority was real. But
Linear's `issueArchive` mutation **cascades to sub-issues**, so archiving a parent archived
its children too — and four of those children were live tickets, including **KS-801, an
In-Progress security ticket**. Nothing in Kam's sentence authorised archiving a live
In-Progress security item; the cascade did it under cover of his sentence. The seat spotted
it and restored all four, so the damage was zero — but only because it checked the result
instead of trusting the verdict.

The shape generalises well beyond Linear: `rm -r`, a cascading FK delete, a recursive chmod,
`git clean`, closing a parent epic, revoking a group's role. In every one, the authority is
scoped to what was NAMED and the tool's blast radius is larger.

**How to apply:**
1. **Before any bulk mutation, enumerate the true blast radius and compare it to the named
   set.** For Linear: list each target's `children` first and **archive leaves only**, parents
   last and individually. The difference between the two lists is the part nobody approved.
2. **Re-read the set AFTER the sweep** and diff it against the intended set. Seat A caught
   this only because it verified the outcome — treat the post-check as part of the action,
   not as optional diligence.
3. **A cascade that touches anything In Progress, or anything on a security/auth surface, is
   a stop-and-report**, not a restore-and-continue. Restoring is right; staying silent about
   it is not.
4. **When briefing a sweep to any agent, name the cascade risk in the brief.** Do not rely on
   the receiving seat rediscovering it — this one did, and that was good judgement rather
   than a mechanism.

**Related:** [[2026-08-03_mental-model-not-source-of-truth]], [[2026-09-06_a-scoped-override-carries-its-own-expiry]], [[../people/kam]]
