---
date: 2026-08-07
type: correction
source: "Kam, 2026-08-07: 'please double check and make sure everything is as expected' — the check found the WED-82 rollout incomplete. Four client area subpages still carried the legacy colours (49 marks) because they render through sub_ev_row()/area_tickets_html(), not the functions I had converted and verified."
status: live
supersedes: ""
---

# Before calling a rollout done, enumerate every SURFACE that renders the data

**The failure:** I converted the dashboard's colour system, verified `index.html`
thoroughly — every mark measured against its real surface, both themes, console
clean — and reported the rollout complete. It wasn't. The subpages
(`area_datasec`, `area_secuura`, `area_family`, `area_personal`) have their own
row renderers, `sub_ev_row()` and `area_tickets_html()`, which I never touched
and never looked at. 49 legacy identity marks were still live when I told Kam it
was done.

**Root-cause family: [[2026-08-05_verify-the-chain-not-the-legs]].** There I
verified per-leg exit codes instead of the artifact at the final destination.
Here I verified the surface I happened to be holding in my head instead of every
surface the change reaches. Both are the same error: **the depth of a check says
nothing about its coverage.** My verification of `index.html` was genuinely
rigorous — measured, not eyeballed — and rigour on one surface reads,
subjectively, exactly like rigour on all of them. That is what makes this
failure mode invisible from the inside.

**Why the existing lesson didn't fire (diagnosis, per the w=2 rule):** the chain
lesson is written in the vocabulary of *data plumbing* — syncs, hops, legs,
destinations. This was a *code change*, so nothing in the retrieval handle
matched. The underlying question is the same in both costumes: **what else
touches this, that I have not looked at?**

**How to apply:**
1. **Before declaring any cross-cutting change done, list the render paths.**
   `grep` for the thing being replaced across the whole output tree, not just
   the file being edited — `grep -rn '<the old pattern>' site/` would have found
   all 49 marks in one command, and is now the closing step of a rollout.
2. **The closing check is absence, not presence.** "The new colours appear on
   the page I looked at" is a presence check and always passes early. "Zero
   instances of the old pattern remain anywhere" is the one that catches this.
3. **A shared-looking helper is not proof of a single path.** Ask which
   functions actually call it — parallel renderers for alternate surfaces
   (print views, subpages, exports, emails) are the standard hiding place.
4. **When someone asks me to double-check, treat it as a real hypothesis that
   something is wrong**, not as an invitation to re-assert. The re-assertion
   version of this check would have passed: every claim I had made was true.
   The gap was in what I never claimed because I never looked.

**The honest note on credit:** this was not self-caught. Kam asked. The lesson
is worth more for that, not less — but the record should say so plainly.

**Related:** [[2026-08-05_verify-the-chain-not-the-legs]] (family parent),
[[2026-08-06_local-proof-is-not-target-evidence]],
[[2026-08-06_artifact-presence-is-not-execution]], [[_ledger]]
