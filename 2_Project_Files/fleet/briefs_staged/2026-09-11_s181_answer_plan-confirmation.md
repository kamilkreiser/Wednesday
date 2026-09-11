## BLUF
- **Plan CONFIRMED as written, with P1–P4 ruled below. Start item 0 now.**
- **Your #954 verify is accepted:** second parent, 9-file diff, merge-tree tree with its control. No STOP.
- **P3 corrects Wednesday's brief wording.** That is Wednesday's error, not yours.

## Rulings
- **P1 — YES.**
  - Amend root `:232` to: "Peter runs periodic formal test passes; demo (UAT) is updated after his nod."
  - At `:258`, append a dated note marking the rule sentence superseded by Kam's 2026-09-11 16:56 ruling. Keep its measurement that GitHub enforces nothing; delete nothing.
  - Reason: a third "no approval → no merge" sentence beside the amended `:234`/`:237` is the same file contradicting itself.
- **P2 — your default.** `:173` and `:178` are not edited this round. Put them in the handover as owed, named for the kintsugi deploy seat. This round deploys nothing.
- **P3 — CORRECTION, Wednesday's wording.** "base contained in develop" meant the standing line at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/brief-standing-lines.md:1401`: *"Before merging any PR, confirm its BASE branch is not already fully contained in the target."*
  - The column is about the PR's BASE ref. Base == develop → "n/a (base develop)".
  - Base != develop → is the base branch's tip an ancestor of develop (`git merge-base --is-ancestor <base tip> origin/develop`)? **Yes = ARMED:** a merge would land in a branch already merged away (#915 and #879 on 09-09) → UNTESTED, with that reason named.
  - **Your reading** (the head is already an ancestor of develop, so the content is already merged) is useful too. Keep it as its OWN column, never instead of this one.
  - TESTED requires both: base not armed AND head not already contained.
- **P4 — YES.** Post ONE facts-only BLUF comment on KS-1085 listing the launcher and hook sites you found, with line numbers and your search frame. A finding that lives only in a mail and a handover has not been delivered; the ticket is the channel.

## Added
- **Stuart draft, Status line only.** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-11_ks597/DRAFT-reply-to-stuart-ks597.md` line 11 currently reads "up for review as PR #954 … It is not merged or deployed yet."
  - Change it to: merged to develop on 2026-09-11 as `2600229ef`, a merge commit whose second parent is the tested head `355d82c8b`; not deployed yet; Kintsugi is next.
  - Change nothing else. Do not post it. Quote the new line in your STATUS mail.
- **KS-597** (In Review since the GitHub integration moved it at 07:49:58Z) → Done, NOT archived, per ADDENDUM 2 — as your plan says.
- **CONTRIBUTING.md and DEV-PROCESS.md approval lines:** owed via a PR, in the handover. Agreed.
- **After #953 merges, mail a STATUS.** Wednesday lifts the LEG-14 HOLD by name only after verifying #953 at source. The hold stands until that mail.

## Unchanged
The brief, ADDENDUM and ADDENDUM 2 stand, except where ruled above.
