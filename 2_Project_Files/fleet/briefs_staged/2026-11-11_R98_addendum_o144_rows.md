Seat R 98th

ADDENDUM: two held Spark passes queued as rows 41 and 42 (Seat R 98th). They come AFTER your round-1 rows 13, 14, 15 and 10, which are unchanged. This mail changes nothing about round 1.

Row 41: KS-1927, demo-service, ONE product file Blockchain/Dev/services/demo-service/src/routes/persona.ts (+4 lines in 3 insert-only hunks), plus ONE new test file. Held diff: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1927-O144-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-DEMO-SERVICE-PERSONA-SWITCH-500-AFTER-COOKIE-NO-SET-COOKIE-PASS-5of5_2026-11-11.diff.md
- Scope: a POST /demo-api/persona/switch that fails AFTER the auth service's refresh-token cookie was copied no longer hands that Set-Cookie out on the generic 500 (the ticket's own clear-in-the-catch shape, made conditional on a flag so the merged ks1868 persona test's stub without removeHeader stays green). Refs KS-1927 (the PR closes what the ticket asks; it does not close the ticket by itself).
- Tier 2 gate. Merge to develop only; demo is FROZEN and a demo-service deploy is not granted.
- Wednesday read the product + lines at the held diff: a let cookieCopied = false before the try, cookieCopied = true after the copy, and in the catch `if (cookieCopied && !res.headersSent) res.removeHeader('Set-Cookie')`.

Row 42: KS-2163, originate, ONE product file Blockchain/Dev/services/originate/src/utils/idNamespaceCollision.ts (one line becomes a 10-line catch), plus ONE new test file. Held diff: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-2163-O144-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-IDNAMESPACECOLLISION-UNREADABLE-NODE-FOLLOWS-OTHER-CHILDREN-PASS-7of7_2026-11-11.diff.md
- Scope: when the read probe meets a node it cannot read, it still follows that node's cause and NOW also its other own enumerable children, each read in its own try, with the same depth bound and seen-set; a readable migration 050/051 refusal under any of them is found, so the caller answers 409 instead of 500. Refs KS-2163.
- RULED BY WEDNESDAY: the ticket offers two outcomes (accept gate AU1's N2 and close, or build). Wednesday rules BUILD: the change is one helper, it only widens which nested errors count as the refusal, and the match still needs the constraint AND the message. Say this in the PR body as Wednesday's ruling.
- Tier 2 gate. Merge to develop only.
- Wednesday read the product + lines at the held diff: the catch keeps the cause visit, then `Object.keys(o)` inside its own try, `if (key === 'cause') continue`, and `visit(o[key], depth + 1)` in a try per key.

For both rows: the Spark operator's measurements are its own (o144 report, 0_Brain/reference/2026-11-11_spark-operator-o144/report.md): demo-service suite 103 to 108 with 0 red, originate suite 2592 to 2602 with its 11 baseline reds unchanged, tsc rc 0, both at develop 2e998b8d9aea. Re-run them yourself at your cut. File sets: no open PR and no held READY touches either file by o144's census at 22:1x (its census, not re-derived by Wednesday); re-check at your cut and STOP and QUESTION on any overlap. Apply the held diffs as your kit applies held passes, tests and docs fragments by your repo's rule, then READY FOR GATE as for round 1.

PROVENANCE:
- KS-1927 held pass, product hunk read by Wednesday | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1927-O144-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-DEMO-SERVICE-PERSONA-SWITCH-500-AFTER-COOKIE-NO-SET-COOKIE-PASS-5of5_2026-11-11.diff.md | read 2026-11-11
- KS-2163 held pass, product hunk read by Wednesday | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-2163-O144-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-IDNAMESPACECOLLISION-UNREADABLE-NODE-FOLLOWS-OTHER-CHILDREN-PASS-7of7_2026-11-11.diff.md | read 2026-11-11
- KS-1927 and KS-2163 both Backlog on Linear, and the suite counts | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_spark-operator-o144/report.md | read 2026-11-11
