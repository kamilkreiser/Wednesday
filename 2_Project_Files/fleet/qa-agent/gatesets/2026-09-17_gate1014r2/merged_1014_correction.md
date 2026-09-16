matches 1
=====MSG 2026-09-16T22:47:59.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 981
Seat A

## BLUF
Correction to my "MERGED: #1014 KS-1176" mail (22:47:27Z). Three code spans were blanked out of its text; no fact changed. I built the body with an unquoted heredoc to expand three variables, so the shell ran each backtick span as a command.

## Recommendation
No action needed. Read these three lines as below.

## Detail
- Line "Develop-moved check" should read: `git log 7e89318bc..fa887f382^ -- enforcement.ts verification.ts` = 0 (develop was still 7e89318bc when the merge started).
- Line "R-g extended" should read: R-g extended (`type` absent from DocumentCreateRequest; the 403 text omits the allow-list refusal).
- Line "b. KS-1202" should read: the untyped carrier `{"data":{"documentType":"DEGREE"}}` is 201 for every principal, including the NONE human, base = head.
- The ticket bodies and the KS-1176 comment were written through quoted heredocs and read back with anchors, so they are not affected. This correction was built with a quoted heredoc.

