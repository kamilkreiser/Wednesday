## SUCCESSOR — you are Seat R 55th (lane Secuura/Blockchain-R, the RAISE lane)

**Why you exist:** Seat R 54th was auto-compacted at about 11:30Z and wrapped at 11:54Z by Wednesday's rule (no new work on a compacted context). Its handover is `5_Project_History/2026-10-19_seatR-54th/HANDOVER.md` (22 KB): read its LATEST STATE and its "ROUND 2 OWED ON #1622" section FIRST. Develop is 115797747cb60009e781d80e9059dbbed69e1ac3 (Wednesday ls-remote 22:5x AEDT). **Live beside you:** Seat C 26th (Secuura/Blockchain-C) is wrapping and holds nothing open; no other Secuura seat is live. Send a short plan confirmation (preflight warnings verbatim) before your first write.

---
## BLUF

Fix **#1622 (KS-1641 finding 2) as round 2 of 2**: gate AM1 found that the new cap lets ONE unauthenticated request kill the m365-integration service. Then a census of the same shape elsewhere, then raise two held Spark passes (KS-1460, KS-1568).

## QUEUE

1. **#1622 round 2 of 2 (the cap)**, head `e065dc9e06d2b52b50944584e9505b95c897dee6` on branch of #1622. Read gate AM1's verdict WHOLE first: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_gate-AM1-pr1622-ks1641/verdict.md`.
   - **B1:** `services/m365-integration/src/index.ts:465` `String(error_description || oauthError).slice(0, 200)` cuts by UTF-16 code unit and can leave a lone surrogate; `encodeURIComponent` then throws `URIError`, Express 4 does not catch it from the async handler, m365 has no process handler, and the process EXITS (AM1 measured it on the real process; develop survives the same input; R 54th re-confirmed the mechanism in Node 24).
   - **Fix shape (yours to choose, say which):** cap by code point so no lone surrogate can remain (for example `Array.from(s).slice(0, 200).join('')`, or drop a trailing high surrogate), and/or guard the encode so a malformed string cannot throw. The redirect must still be bounded (AM1 measured 1,859 chars max on the BMP worst case; re-measure with your shape).
   - **Cells:** a multi-byte character straddling index 199/200 (AM1's input: `'A'*199` + U+1F600 + `'zz'`) answers 302 with a bounded, valid URL; a process-survives cell (the server still answers `/health` after that request); keep E1-E4.
   - **Also in this round, from AM1's notes:** N2 cap the `state` log at `:474`, N3 cap the log at `:464` (the auth.ts precedent caps its log). N4 (`connectionId` unencoded at `:508`) and N5 (two JSON bodies, authenticated) go in ONE follow-up ticket, searched first. N6 is the 199/200 cell above.
   - Then READY FOR DELTA GATE. A NO GO next round ships nothing.
2. **Census, read-only:** every place in `services/` and `packages/` where a `.slice(...)`/`.substring(...)`/`.substr(...)` result reaches `encodeURIComponent`, `encodeURI`, or another encoder that throws on a lone surrogate, including today's merged Spark passes (KS-1617 A.2 and A.3, KS-1622, KS-1641 p1). Give the search with a positive control, the list, and for each site whether it is reachable unauthenticated. Findings go to tickets (search first), not into this PR. Mail the list.
3. **KS-1460** (Backlog, p3, 0 comments): `night/READY_KS-1460-STUBCLAIMCONFIRM-1_spark-dsv4flash_BRIEFED-CODEPATCH-AUTH-PASS-7of7_2026-10-19.diff.md` (in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/`). R 54th's pre-raise readings are in its handover (patch == sections, golden byte-identical, pre-image blob equal at 115797747cb6). Refs KS-1460 only (1 of 8 callers). `routes/users.ts:1293` is in flight as KS-1194 part 2: check that PR before going near it. Tier 1 (auth).
4. **KS-1568** (Backlog, p3, 0 comments): `night/READY_KS-1568-ROTATEWAITPARSE-1_spark-dsv4flash_BRIEFED-CODEPATCH-INDEX-PASS-7of7_2026-10-19.diff.md`. Its golden bytes DIFFER: report applied-result identity and say why. Tier 2.
5. Per PR: READY FOR GATE (cause, cells, suite counts at the landing parent, files, predicted landing tree on live develop). One BLUF ticket comment per PR.

## PARTITION

Yours: `services/m365-integration/src/index.ts` and its tests; `services/auth/src/routes/auth.ts` (KS-1460's hunk only) and its new test; `services/security/src/index.ts` (KS-1568's hunk only) and its new test. Say so before touching any other file. No other Secuura seat is live; C 26th is wrapping. You share an inbox with every Secuura seat: a mail naming another seat is not yours.

## HOLDS

- **A fresh clone has NO pre-push gate.** Before any push: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`, then `git config --get core.hooksPath` read back in your plan confirmation (KS-1646).
- **Identity:** `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY before the first commit; read back `git config --show-origin user.email`.
- **Pushing:** `.githooks/pre-push:352-358` refuses a push whose tip is not the checked-out HEAD; `:76-80` refuses a non-fast-forward push. Never `--no-verify`; never `ALLOW_FORCE` without a mail from me naming it. Transport: `-c core.sshCommand='<the repo's ssh command> -o ServerAliveInterval=30'`.
- `tsc -p` in originate/m365 excludes test files (KS-1090): type-check tests another way, and treat `Tests: 0 total` as a load failure.
- Build `packages/shared` first in a fresh clone (KS-846).
- Merge only on Wednesday's head-pinned GO after a gate verdict. No deploy. Ticket comments are the only client-facing channel.
- No Docker on this Studio. Rotate inside your 80-90 band at a clean boundary; handover first. Mail every state change; a turn never ends on an unmailed report (R 54th's lapse).

## RULED BY KAM, NOT YET IN AN ARTEFACT

- None for these tickets.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- #1622 round 2 moved from R 54th to this seat by name (Wednesday's 11:5xZ NO GO mail): R 54th did not fix it.
- KS-1460 and KS-1568 moved from R 54th to this seat (Wednesday's 11:41Z ANSWER).

PROVENANCE:
- KS-1641 In Progress, priority 3, 3 comments, last 2026-10-19T11:52:47Z | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- KS-1460 Backlog, priority 3, 0 comments | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- KS-1568 Backlog, priority 3, 0 comments | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- KS-1194 In Review, priority 2, 9 comments, last 2026-10-12T05:57Z (named only as "check that PR before going near users.ts:1293") | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- KS-1617 In Progress, priority 3, 1 comment, last 2026-10-19T03:12Z (named only as a census subject) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- KS-1622 Backlog, priority 4, 0 comments (named only as a census subject) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-19
- #1622 head e065dc9e06d2 and develop 115797747cb6 | git ls-remote origin, run by Wednesday | read 2026-10-19
- gate AM1's B1 and notes | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_gate-AM1-pr1622-ks1641/verdict.md, sha recomputed EQUAL by Wednesday | read 2026-10-19
- pre-push refusals | your own .githooks/pre-push at 846ae2788b3b, lines 76-80 and 352-358, read by Wednesday earlier today | read 2026-10-19

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-19 22:57
