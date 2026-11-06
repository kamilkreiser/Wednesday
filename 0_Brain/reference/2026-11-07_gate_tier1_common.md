# Common commission for tier 1 batched gates, Secuura / Blockchain, 2026-11-07

Written by Wednesday. Model: Opus, row G1. Batched under Kam's 2026-09-18 no-duplicate-gates rule: one session, ONE VERDICT PER PR. Root H = /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History. Each seat's READY is a set of claims to test; Wednesday has re-run none of them. Develop b27f5fb30f4a by the seats' reads about 18:25Z 6 Nov. Re-read every head and develop at origin at start and end; a moved head voids that PR's verdict only.

QA GATE: findings only; fix nothing; write nothing outside your gate folder and your clone; post nothing; no box; no docker; network only for git fetch. Absolute paths, never cd. /usr/bin/grep -i with a positive control beside any zero. DISK: DevMASTER about 25 GiB free: one clone in /private/tmp/<your gate number> on the boot volume; remove it at the end and say so. Repo: read the remote from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files and use its configured deploy key; that checkout is read-only, do not fetch there. Keep load1 under 8.

Read first: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md. Kam's words decide scope: read every card a READY cites with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show <id>`, read verb only. A ruling marked as Wednesday's is not Kam's; say if it is wider than his card.

## For each PR
1. Read the diff whole. Does it do what the ticket and the card say, and nothing else? Enumerate the surface from the code, not from the READY's list.
2. Try to break it. For an authorization or error-text change: every door, principal type, malformed input and failure path, measured at runtime where the suite allows. Name who loses access and whether any real caller does.
3. Test quality: reproduce a sample of the seat's reds and tampers, plant at least one defect of your own. Does any cell pass for the wrong reason?
4. Every factual sentence in the PR body and the ticket comment that a client human will read: true at this head?
5. Merge tree on develop; paths shared with any other PR in your batch or an open PR; the merge order.
Depth is proportionate: spend where a wrong answer costs most. If a finding needs Kam's ruling, say so at the top of that PR's verdict and keep going.

## Output
verdict.md in your gate folder: a table first, one row per PR: PR, head, GO, GO WITH NOTES or NO GO. Then per PR: BLUF, findings with severity, file:line, FOUND / TESTED / HOW, what was NOT tested. Then your own conduct. Final message: one verdict line per PR plus one line per finding. Severity is yours; priority is not.
