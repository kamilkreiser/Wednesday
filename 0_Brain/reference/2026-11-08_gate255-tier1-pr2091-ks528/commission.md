# Gate 255, tier 1: PR 2091, KS-528 (react-router-dom 6 -> react-router 7, three portals). Launched 2026-11-08 by the 21:2x Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Two corrections to it: (1) develop is NOT b27f5fb30f4a now; by Wednesday's ls-remote at 21:33 AEDT develop is 14ac61bd1a4c854c17539f1cd0f518631f998fbb; re-read at your start and end. (2) The QA template's no-rm rule wins: leave your clone at /private/tmp/g255 and name its size. DevMASTER has about 24 GiB free and a NAS move is running; keep to one clone and one node_modules per portal you build, and stop if free space drops under 12 GiB. Never cd, even in a subshell.

Tier 1 because: a major-version router move across the admin, issuer and verifier portals (login and routing for every portal user) and two rows leaving audit-baseline.json (a security gate's input).

Head 258e049aaf75ff8f5009449eb918a7c0a98624fb (Wednesday's ls-remote 21:33, equal to the READY). One commit, 34 files, +486/-180, base b7d433fda83c by the seat.
READY: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatR-88th/mail/ready_ks528_r88.md (read whole). Builder of record: Seat R 87th, evidence in its record folder 5_Project_History/2026-11-06_seatR-87th*/ (find it). Cards: `secuura-react-router-rows-fallback-date-1106` and any card the READY or PR body cites, by `decision_queue.sh show`.

Questions, in order of cost if wrong:
1. Does every portal still BUILD and its existing unit tests pass at this head? Run each portal's own build and test commands from its package.json (install from its lock). The seat ran neither today; R 87th's runs are two days old. Say per portal: built yes/no, tests N of M.
2. v6 to v7 behaviour, from the diff and the react-router 7 changelog/upgrade notes read in the installed package (not from memory): removed or changed APIs (json/defer, future flags, relative splat paths, startTransition, fetcher and navigation state, ScrollRestoration, useNavigate in effects), and whether any portal code still relies on v6 behaviour. Name every call site you checked.
3. Auth paths: login redirect, protected-route guard, logout, deep link after login, 404 route, in each portal. Exercise them where a local run is possible without a stack (a dev server with the API mocked or absent: say what renders); otherwise read them and say UNMEASURED.
4. audit-baseline.json: are the two removed rows (GHSA-wrjc-x8rr-h8h6, GHSA-337j-9hxr-rhxg) actually unreachable at the head (npm ls / the lockfiles, all 4 locks), and does the repo's own audit gate pass at the head? Run the repo's audit check as preflight would. Is anything left in any lock still pulling react-router-dom 6?
5. The new 16-cell suite: can it fail, and for the right reason? Its develop run prints R0, R1, R2 by the seat; reproduce one red and plant one defect of your own.
6. Merge tree on develop 14ac61bd1a4c. The 11 open PRs sharing a path (575, 635, 639, 649, 945, 946, 947, 948, 949, 1360, 1965): R 87th's no-new-conflict claim is two days old and unrepeated; repeat merge-tree for at least 575, 1360 and 1965 after this PR, and say which you did not.
7. Every factual sentence in the PR body and the KS-528 ticket comment 2083ebbe (a client human may read both): true at this head? The ticket's own Done-when (react-router-dom 7.x, demo verification, three rows) differs from this PR; is the narrowing stated plainly enough that nobody reads the ticket as done?

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_gate255-tier1-pr2091-ks528/verdict.md, as the common rules say (line 1 of the table: PR 2091, head, GO / GO WITH NOTES / NO GO). Findings only; post nothing; write nothing outside this folder and your clone.
