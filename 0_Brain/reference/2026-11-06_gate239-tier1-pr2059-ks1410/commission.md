# Gate 239 commission: Secuura / Blockchain, PR 2059 (KS-1410 with KS-1214), TIER 1, round 1 of 2

Written by Wednesday 2026-11-06. Model: Opus, row G1. Tier reason: a security surface, removing server file-path reads from the mcp-server web interface, and a client-visible refusal. Head 7a644a2dd246055ed5c725a3da8be88639dd04bf, develop b27f5fb30f4a912ec2b4b78f5c27281d11e47a87, by Wednesday's ls-remote at 23:12:46 AEDT. Seat Z 4th's READY is saved at ready_z4.txt here.

QA GATE: findings only; fix nothing; write nothing outside this folder; post nothing; no box; no docker; network only for git fetch. Absolute paths, never cd. /usr/bin/grep -i with a positive control beside any zero. DISK: DevMASTER about 25 GiB: one small clone, in /private/tmp/g239 on the boot volume, never under this folder. A commit voids this verdict. verdict.md holds the INCOMPLETE stub; overwrite it at the end.

Read first: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md; `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-ks-1410-ks-1214-mcp-rest-mirror-file-reads-1106` (read verb only), ruled a: 'Remove file-path reading from the web interface; fixed error sentence on /hash and batch items'.

## Questions
1. Is every path that reads a server file by a caller's value gone from the web interface, at the head? Enumerate the routes from the mounts, not from the PR's list. Is the stdio surface, which the seat says still takes filePath, reachable over HTTP by any route?
2. The seat's flag 1: a truthy filePath is refused even beside content, documentId or contentHash, where it was ignored before. Inside Kam's words, or a behaviour change he did not rule? A falsy filePath passes: any value that reads falsy here and still reads a file elsewhere?
3. The fixed sentences: does any path still echo a path, an error message or a stack, including the /hash 500 and batch items? Does the real error reach the log without leaking a secret?
4. Six existing cells were inverted, not deleted. Does each still test what it is named for? Reproduce three of the seat's 14 planted defects and one of your own.
5. Spec, its byte copy and the guides: what still offers filePath? 14 of 21 outside files were not opened by the seat: open them. Who breaks: any client inside the repo, Platform S's snapshot at /Volumes/DevMASTER/!CODING/Secuura/platform-s-main read only, saying what a June snapshot cannot show.
6. Merge tree on current develop; any open PR or queued path it shares.

## Output
verdict.md: line 1 GO, GO WITH NOTES or NO GO, line 2 the head, then BLUF, findings with severity, file:line, FOUND / TESTED / HOW, what was NOT tested, your own conduct. Final message: the verdict line plus one line per finding.
