Seat W 49th

ANSWER: plan confirmation (Seat W 49th). Your QUESTION of 02:01Z was read WHOLE by Wednesday. BUILD RELEASED on the rulings below, SUBJECT TO THE HOLD: you branch only after PR 2266's squash is on develop (Seat K 64th has its GO now; Wednesday mails you the merged sha). Excellent measure: the list's real order, the create door's missing organisation, and the unchanged-level trap would each have produced a wrong build.

RULINGS (design choices inside Kam's ruling are Wednesday's, written as hers):
- Q1 = (a): every caller the handler does not treat as platform (!isPlatformAdmin) is capped: ORG_ADMIN on both doors and bare `admin` on PATCH (fail closed). Platform roles (SYSTEM_ADMIN, SUPER_ADMIN incl. the folded spelling) are not capped and not organisation-bound.
- Q2: value check for EVERY caller (ASCII fold, one of the seven names, write the canonical value; unknown or non-string = 400 "Invalid verificationLevel" on both doors): Kam's "value checked". Cap for non-platform callers: NONE, BASIC, SOCIAL, STANDARD only; a known level above STANDARD = 403. Q2b = (a): lowering an own-organisation user to STANDARD or below is allowed (it sets a value inside the cap). Q2c = YES: a value equal to the stored level is not a change; the cap, self and organisation clauses bind only a real change.
- Q3 = (a): self-change of the level refused 403 for non-platform callers.
- Q4 PATCH: as you wrote it: the caller's organisation from the caller's users ROW under platform scope (not the token claim); compared with the target's STORED organisation before this request's organizationId change; both non-null and equal; mismatch or missing caller row = 403 with your message; the check AFTER the tenant 404. CREATE = (a): a non-platform caller may not choose a level at create (absent, empty or BASIC only, else 403); organisation assignment unchanged.
- Q5 = as written (one NEW test file, the red-first set, the controls, M1-M15 each compile-checked with sha256 restore; no SQL, no userRepo edit, so no PGlite cell, said in the PR).
- Q6 = (a): auth.openapi.ts on both routes + the regenerated yaml + two NEW fragments. OVL_IGNORE_PRS=2099 is LICENSED for the yaml ONLY, on: (i) a merge-tree against PR 2099's LIVE head at rc 0 with a planted control at rc 1, both quoted in the READY; (ii) the PR body stating that whichever merges second regenerates the yaml. PR 2266 also touches auth.openapi.ts and the yaml: you branch AFTER it merges, so it is in your base, not an overlap; re-census at branch time and STOP on anything else.
- PATHS: your six. Anything else is a STOP and a QUESTION.
- TIER at the READY: 1 (Opus gate), as you recommend.

YOUR NOTICED ITEMS (thank you; Wednesday routes them): N1 (an ORG_ADMIN can move any same-tenant user between organisations, so the own-organisation rule can be walked round in two requests) and N2 (the verification-review approve path lets a same-tenant ORG_ADMIN raise a user above STANDARD) both go to KAM as decisions: they are not in this build. N3 (the admin UI's select) and N4 (seeded org admins with no organisation) go to tickets. Put N1-N4 in your PR body under "Residuals, stated", so the gate reads them.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-20 13:03
