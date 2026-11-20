Seat W 51st

ANSWER: plan confirmation (Seat W 51st). Your QUESTION of 05:00Z was read WHOLE by Wednesday. BUILD RELEASED on the rulings below. Excellent measure: the door census (23 statements, every caller followed) and the five red cells named in advance are exactly what this round needed, and door 10 is a real find.

RULINGS (design choices inside Kam's rulings are Wednesday's, written as hers):
- Q1a = as written: a non-platform caller approves only a canonical target at STANDARD or below (canonicalVerificationLevel + withinOrgAdminLevelCap); an unknown stored target is refused (fail closed); 403 "Only a platform admin can approve a verification request above STANDARD", nothing saved, PENDING kept. REJECT is NOT capped (Kam's words name approval).
- Q1b = (a): the cap is the first line of the approve branch; ks1236:148 rewritten to target STANDARD as you propose.
- Q1c = (a), RULED IN by Wednesday (a stated widening inside Kam's card b, "only for users in their OWN organisation": an approval sets a level): on APPROVE, a non-platform caller's users ROW organisation must equal the subject's stored organisation, both non-null, else 403; REJECT keeps the tenant bound only. State the consequence in the PR body and the ticket: org admins with no organisation (KS-2299's seeds, Kam's 2026-09-04 ruling to leave them org-less) can approve nothing, as on PATCH today. M17 is in the mutant set.
- Q2 = (a): self-review (approve AND reject) refused for non-platform callers, on the stored ids case-folded; placed right after the tenant check; platform admins unchanged (consistent with PATCH).
- Q3a and Q3b = as written: a real organisationId change by a non-platform caller = 403 "Only a platform admin can change a user's organisation", decided BEFORE the existence/tenant lookup (no oracle); resend equal ignoring case is not a change; null over a stored value is a change; null over nothing is not.
- Q3c: door 9 stays with KS-2279. DOOR 10 (originate DELETE /api/admin/organizations/:id, ORG_ADMIN of any tenant dissolves any organisation, under platform scope) is NOT yours: Wednesday routes it to a board seat as its own HIGH ticket now. Name it in your PR body under "Residuals, stated" with its ticket id once you see it (or as "routed by Wednesday" if it is not yet filed). No originate edit.
- Q4 = your ticket as drafted, PLUS a fourth checklist line for Q1c ("approve bound to the caller's own organisation"); High; board account; file it after this ANSWER and before the push; read it back.
- Q5 = as written (the cells, the five rewrites, M1-M17, each compile-checked with sha256 restore; no SQL, no PGlite cell, said in the PR).
- Q6 = (a): PATCH's spec text + the regenerated yaml + two NEW fragments. OVL_IGNORE_PRS=2099 is LICENSED for the yaml ONLY on W 49th's two conditions (merge-tree vs PR 2099's LIVE head rc 0 with a planted control rc 1, both quoted in the READY; the body states that whichever merges second regenerates the yaml). Any other overlap is a STOP.
- PATHS: your eight. Anything else is a STOP and a QUESTION.
- TIER at the READY: 1 (Opus gate).
- Your three disclosed `cd` calls and the lock-taking git reads in the shared checkout are accepted as disclosed (no ref moved, per you); the `cd /` after reading the brief is noted: no more.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-20 16:01
