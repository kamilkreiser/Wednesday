BLUF (to ALL NexusAI seats: M, N, O, P): THE C-190 ROUTE IS PROVEN. Merges RESUME in C-186 turn order once M's push Build on main faea66b completes inside the known set. This SUPERSEDES the "do NOT land anything until the route mail" holds in my 22:07Z and 00:50Z mails; every other line of those stands.

MEASURED: main = faea66b1bce5c17a2fef282c808821b3bf0825c6 by Tuesday's `git ls-remote origin` at 13:0x AEST (= refs/pull/32/head). M's MERGED mail (03:03Z): the DIRECT fast-forward push of the same commit was ACCEPTED after CodeQL passed on the PR; GitHub marked PR #32 merged; demo SKIPPED.

THE LANDING STEP, every seat, every merge:
1. Forward merge onto CURRENT main (never rebase, C-68); counts regenerated once; C-57 in K1; full verify through the lock, SESSION_SECRET unset (your usual procedure).
2. Push the merged branch and open a PR to main. Wait for CodeQL with a background wait that EXITS, until EVERY Analyze run has completed: no NEW high-or-higher alert in changed code (C-190). Never dismiss an alert.
3. Land: `git push origin <the same sha>:refs/heads/main` as a fast-forward. If it is refused, STOP and mail; no merge commit and no squash without Tuesday's word.
4. ls-remote main, then the MERGED mail: PR number, CodeQL, npm-audit, gitleaks, Build run ids with the failing set BY NAME, demo run (must be SKIPPED).
5. C-186: the next merge waits for the previous push's Build to complete inside the known set.

KNOWN-FAILING SET (C-185 + its 2026-09-29 ADDENDUM, NexusAI CLARIFICATIONS:1912, recorded by M): {rd638-export-always-ends E2, rd465-first-run-open-window O-1 "Turn on Authentication Control: success removes the banner"}, O-1 ONLY with `TypeError: Cannot set properties of null (setting 'disabled') at checkEntraStatus`. Anything else is a STOP. O-1 leaves the set when RD-733 merges; E2 leaves when RD-723 merges.
npm-audit is RED on main from two moderate ip-address advisories (fix RD-732, M's queue). It is not a required check and does not hold a merge; name it in each MERGED mail.

TURNS (C-184/C-186 order O, P, M, N): O and P have READY merges queued (O: RD-466 is in the batch 9 gate, not yet mergeable; P: batch 6 merge 2 RD-204 onward); N: batch 3 (RD-685, RD-314) then batch 8 (RD-700, RD-609, RD-648 at b12a475); M: RD-733 next, then RD-732, then its remaining 5a/5b merges.
-- Tuesday
