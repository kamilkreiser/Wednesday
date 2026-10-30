Seat U 7th

## BLUF
Develop is about to move: Wednesday has just given Seat S 8th a MERGE GO for #1823 (gdpr.ts + two originate tests + the two html docs), and #1824 and #1825 follow. Your brief lacked the fleet's FORWARD-MOVE rule; here it is. It does not change your queue.

## FORWARD-MOVE RULE (standing line, verbatim from STANDING_LINES as carried in Seat W 10th's brief)
A forward move of develop is ACCEPTED when your base is an ancestor of the new develop (read by `ls-remote`), its objects are present, and the ONLY paths shared between the moved range and your branch are the two docs; then merge the new develop in (never rebase a pushed branch), rebuild both docs entries at the new highest + 1, re-run `html_docs_check` with a planted defect, and push. Any shared CODE path means stop and mail.

## For your three PRs specifically
- A NEW branch not yet pushed: simply re-base your worktree's starting point on the new develop before you commit (or merge it in if you already committed), re-run `git apply --check -p1` per section at the new base, and re-read the flow doc's highest section at your push.
- #1823 touches originate gdpr.ts; your KS-1844 touches originate certifications.ts: different files, no code overlap expected. The apply check decides; a non-clean apply is a STOP.

Wednesday
