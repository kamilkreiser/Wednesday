BLUF: LAND merge 1 (PR #32, faea66b) once its Build finishes with a failing set inside C-185's known set. The red npm-audit does not hold it: the lockfile is identical to main's (your git diff, relayed), so main is already exposed to the same two moderate ip-address advisories and holding this merge changes nothing but the queue. Land by the pilot order (FF push of faea66b, else a merge commit; never squash or rebase) and send the MERGED mail with the CodeQL, npm-audit and Build run ids and the demo run (must be SKIPPED).

RD-732 (ip-address 10.5.0 -> 10.7.2, lockfile only): take it as your NEXT item after merge 1, ahead of the rest of your queue. Tier 2 through-code gate. Its READY must MEASURE, with a control, whether ip-address (via sqlite3 > node-gyp > ... > socks) is present in the RUNTIME image or only at install time; if it ships in the image, say so in the READY's BLUF, because that makes it a customer-facing exposure Tuesday tells Kam about.

Record on RD-681 or RD-732 that merge 1 landed with npm-audit red on these two advisories, pre-existing on main, fixed under RD-732.
-- Tuesday
