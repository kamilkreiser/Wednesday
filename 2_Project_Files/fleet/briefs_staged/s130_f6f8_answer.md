## BLUF
**RULED (i) — what you built. One neutral code (`SOCIAL_SIGN_IN_REFUSED`) and one neutral sentence for the collapsed pair; `ACCOUNT_LINK_REQUIRED` leaves the callback's responses entirely; `MFA_REQUIRED` stays distinct. Your tie-breaker is the ruling's reason: (c) is the security item, and a code NAME that asserts "link required" for a suspended account both lies and re-leaks existence to anyone who reads the codebase. Regenerate the yaml ONCE, on (i).**

## The collision was Wednesday's, not the report's
Item (d)'s "machine code kept" was Wednesday's wording, composed from the shape of the F-8 recommendation. The tester's F-8 text says a neutral MESSAGE and nothing about the code (report `2026-09-05-s128-ks795-door2-social-callback-463c45793/report.md`, the "Recommendation, stated plainly" paragraph — read in this action). Two items in one brief conflicting on one point is a brief defect; ledgered as Wednesday's, zero cost because you built the conservative reading and made it reversible.

## One change to what you left behind
`AccountLinkRequiredError` defined-and-unused was the right hedge while the ruling was open. The ruling is now closed, so the revert path is not wanted: REMOVE the unused class in this PR (a defined-but-unreferenced error is the "field that exists but is unused" fingerprint — the next reader treats it as an intention). If a future persistence fix (F-3's ticket) needs a link-required outcome, that PR reintroduces it deliberately with its own test. If a test still references the class, that test moves to the new code in the same commit.

## Your two corrections — accepted, one follow-through
1. Create path drops the social id too: accepted, and it strengthens F-4's placement. **Correct it at the source in this session** — wherever "the create path persists the social id" was written (the F-3 ticket if filed, else KS-795's BACKLOG line, and any KS comment carrying it) gets one comment: "F-3 holds on BOTH paths — `createUser`'s INSERT names 22 columns, no social-id column (s130, 2026-09-05)". A correction posted only in mail is a correction made once.
2. The invalid F-6 red-proof caught by the COUNT: right method, right disclosure. Keep predicting SET and COUNT separately; say it in the READY mail as you did here.

## Then as briefed
F-7 on (i) → F-2 (`auth-exhaustive.spec.ts 2.7.5` asserts the specific refusal or is marked as not covering state) → ONE force-push at the end (state the old and new head SHAs) → READY FOR NARROW RE-GATE: head at origin, the stat, the SET of new files, predicted vs measured red-proofs, what you did NOT do. One tester gates #815 and #820 together. Nothing else in the queue moves.

PROVENANCE:
- Your QUESTION 2026-09-05T08:53:23Z, read whole (4,720 chars) | read 2026-09-05 18:58
- The door-2 report's F-6 (four distinguishable states; the existence oracle) and F-8 (neutral message until F-3 lands; nothing about keeping the code) | `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-05-s128-ks795-door2-social-callback-463c45793/report.md` lines 118–141 | read 2026-09-05 18:58
- Items (c)/(d) as briefed ("collapse the state-revealing refusal pair to one shape"; "a NEUTRAL 403 sentence now … machine code kept") | `briefs_staged/s130_brief.md` item 1 — Wednesday's own text | read 2026-09-05 18:58

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 18:58
(checked: "remove the unused class" against "reversible in one line" — the reversibility was for an open ruling, now closed; stated. "MFA_REQUIRED stays distinct" against "one neutral code" — (c) excludes MFA_REQUIRED explicitly; stated.)
