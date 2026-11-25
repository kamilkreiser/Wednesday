# DRAFTER COMMISSION — brief for Seat K 93rd (Secuura/Blockchain-K, MERGE seat: PR 2092 then PR 2142)

Written by Wednesday 2026-11-25 evening. You are a DRAFTER: write ONE brief file and nothing else. Read-only everywhere else; never cd; never discard stderr; no git write verbs; never copy a secret.

## Output
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-25_seatK93_merge.md`

## Templates (read each WHOLE first)
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-24_seatK92_merge.md`: the last merge brief (kit, GO form, expected-tree rule, two-gate squash line, WRAP). Copy its shape and discipline.
- `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-24_drafter-seatK92/commission.md`: how that one was commissioned.
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-24_K92_wrap.txt` item 3: kit gaps G1-G7 that THIS brief must carry fixed.

## Authority (quote verbatim)
- Kam, live board 2026-11-25 18:21:21: "Please close and merge and archive what you can. That looks like great progress."
- Standing: "We approve and merge our own TESTED Platform K work" (Kam 2026-09-11); Stuart's four merge rules agreed 2026-11-16 on KS-2196 (rule 1 gate at exact head + author's test evidence; rule 2 recent merge rules override older holds; rule 3 we run the suites and say which were NOT run; rule 4 demo behind Stuart's nod).

## The two PRs (from Seat S 124th's census, B.tsv sha256 23ba9c9a766e; RE-MEASURE everything)
1. PR 2092 (KS-1209), head 3d8423f71024af5bbaf9b12d733923d86d7d14b0, gate 262 GO WITH NOTES at that exact head; 7 paths under scripts/audit plus two fragments; merge-tree against develop 9c1ecde5abd6 clean (S 124th's clone).
2. PR 2142 (KS-2142), head 3ea830e7e221 (full sha: measure), gate 295 (a 4-PR gate; its PR 2142 line reads GO WITH NOTES); ONE test file, +4 -1, comments only; merge-tree clean.
Both gates ran on OLDER develops (7eda23b34d3b and d0b4825cc244). The brief must make the seat run the affected legs on the MERGE of each head with the live develop before its READY (the 11-22 lesson: a merge's verification covers every suite the change can turn red; for a scripts/audit or test-only change, name which suites that is and which are NOT run). Find the gate verdict files under /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/ (search '*gate262*' and '*gate295*'); cite them by absolute path.

## Sequence the brief must enforce
Plan QUESTION -> ANSWER -> STATUS -> READY TO MERGE for PR 2092 (expected tree = merge-tree of its head on the live develop, measured in the sending command) -> GO from Wednesday with develop + head asserted -> MERGED -> Wednesday verifies at source -> then the same for PR 2142 on the NEW develop -> WRAP. One PR at a time. Squash merges, the commit message carries the gate line(s) as K 92nd's did. A conflict, a red leg or a moved head = STOP + QUESTION. No force-push, no --admin, no deploy, no demo, no other PR.

## Routing
Model: Sonnet (newest; Wednesday fills the id at launch). Lane -K. Seat name exactly `Seat K 93rd` (ordinal measured 2026-11-25: K 92nd 1, K 93rd 0).

## Return
Reply with the output path, byte count, and every fact you could not validate (also marked UNVALIDATED in the brief).
