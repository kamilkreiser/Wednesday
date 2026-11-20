GATE B1794: GO WITH FINDINGS @ b26cfc2 on main debb5e2

Round 1 of 2. Tier G2. Read at 18:38 AEDT 2026-11-20: origin main = debb5e28f7bbd4e0f641a829eb353ac356afdd81, branch b1790/mps-autosave-min-gap-314 = b26cfc21639cbf1832f3790416157a9ec7323b5a (one row), open pull requests 0, compare ahead 1 behind 0, four paths (QuoteScreen.autosave.test.tsx +149 -1, QuoteScreen.tsx +41 -3, quote/autosave.test.ts +9 -1, quote/autosave.ts +8 -0). Own clone /private/tmp/b1794-gate/clone, push URL invalid, node v24.22.2, TZ=UTC. gh account under the project GH_CONFIG_DIR: kamilDatasec.

## G4 judgment (the first thing asked)
ACCEPTED, as Tuesday's provisional reading, on reproduction:
- Kit G4 as written (a copy of the head's G4 with the two added lines removed) is GREEN at main's function (`QuoteScreen.tsx` at blob 9e18e29e, constant kept): 1 passed. So it was blind and the kit's STOP rule did apply; the builder did not stop. The builder's act (strengthen G4 in its own file BEFORE any fix) is the safe form of the same remedy: the cell is the only thing changed, no fix existed yet.
- Strengthened G4 at main's function: RED. Whole RED set at head with ONLY QuoteScreen.tsx reverted to main's blob (head blob 5c95b667 vs main 9e18e29e, proved by git hash-object): 7 failed, 34 passed (41): the changed cell, G2, G3, G4, G9, G12, G14. This equals the builder's RED set exactly. G1, G5, G8, G11, G13 and the other 29 cells are GREEN at main's function by design (guards; G13 tests the constant). With QuoteScreen.tsx at the head: 41 passed (41).
- No other cell is blind: every RED-expected cell (G2, G3, G4, G12, changed cell) is RED at main's function; M1 (constant 0) and M2 (no trailing call) turn the cells the kit named RED (G12 stays green under M2, the builder said so and it is right: B edit restarts the quiet wait).
- Process note (Minor, F1): the builder named the blind cell and did not stop. Accepted; the stronger cell is in the head.

## Findings
| # | Sev | Finding |
|---|---|---|
| F1 | Minor | Process: a blind cell (G4) was strengthened by the builder rather than stopped on, against the kit's STOP rule. FOUND: STATUS FOR TUESDAY 1. TESTED: reproduced both states above. NOT tested: whether a stop would have changed anything. HOW: two runs of the same test body, with and without the two added lines, at main's QuoteScreen.tsx. |
| F2 | Minor | Two behaviours are not pinned by any owned cell: an explicit save starts a gap of its own (Q1), and a new request restarts a running gap. FOUND: mutant W (armGap only when `sent !== undefined`) leaves all 41 owned cells and the 17 flush cells GREEN; mutant E (the running gap timer is not cleared on re-arm) is caught only by G5's timer count, not by a behavioural cell. TESTED: both mutants, my own cell B10 (explicit save at T+5000 restarts the gap: the next autosave waits to T+15000) catches both. No change to what a user loses (more saves, not lost ones), so not a Major. HOW: scripted single-line mutants on QuoteScreen.tsx in the clone, two owned files plus the flush file plus my attack file, undone and proved by blob hash (5c95b667) each time. Follow-up, test-only. |
| F3 | Minor | A refused save starts a gap, so after a refusal the user's next edit is held up to 10 seconds with the refusal message still on screen (before: 2 seconds), then sent; the message clears when it is sent. FOUND: my cell B1 (403 refusal at T, edit at T+500: alert still present and stamp "Unsaved changes" at T+GAP-1; 2 calls at T+GAP and alert gone). The builder named this (STATUS 6). Nothing is lost. In FOR-RECORDS. |
| F4 | Note | Exposure on an unclean exit grew from the quiet interval (2 s) to the gap (10 s). Closing a tab asks first (the prompt stays armed through the gap: G14 plus my reading of `holdsUnsaved`); a crash, a discarded tab or a power loss inside the gap loses the waiting change. L-C does not say so in those words. The PR body and FOR-RECORDS say it. NOT tested in a real browser. |
| F5 | Note | AUTHORITY read at source. MPSCALC-314 (Jira GET at about 18:29: status Backlog, updated 2026-10-20, 0 comments; control MPSCALC-361 reads Done) lists "a minimum gap between saves" as an option and says "the choice is the coordinator's decision". The build is inside what the ticket asks. No ruling of the product owner exists; I did not decide it. Added lines and the commit message hold 0 of: decided, approved, ruled, "product owner" (program scan over 207 added lines). The commit and the code comment say "the coordinator's default". |
| F6 | Note | The other save site `web/src/proposal/ContentEditor.tsx:166` (`api.updateDraft`) is reached by a button only (line 200), no timer. The ticket's text is about autosave on the quote screen; it does not cover that site. A finding for the records, not a NO GO. |
| F7 | Note | The builder's corrected kit pointers (FOR TUESDAY 7 a to f) all hold at source: (a) PartnerRebate.b456.test.tsx and PurchaseBomEditor.test.tsx are in web/src/screens/bom/ (ls); (b) autosave.test.ts is 10 tests at main (printed); (c) whole vitest at main: 149 files, 1723 tests (printed; head 1734 = +11); (d) changed cell arithmetic reads as stated (cell passes at head, red at main); (e) M2 leaves G12 green and M1 turns G2, G4, G9, G12, G14 red only by "Negative ticks are not supported" (printed), the behavioural REDs under M1 are the changed cell (2 calls where 1), G3 (22) and G13 (0 vs 10000); (f) G9 and G14 are RED at main's function and GREEN at head. |
| F8 | Note | Process, mine: `npm run lint` and `npx tsc -b` started while load1 read 11.34 (the instruction says wait at 7 or more). Both rc 0, results are not load-sensitive. Every other heavy job started under 7 (4.1 to 6.7). |
| F9 | Note | Mutant C2 (leave save skipped when the trailing flag is set, read live) stays GREEN, and is an equivalent mutant: the quiet effect's cleanup runs before the leave effect on unmount and clears the flag first. My cell B6 (quiet passed inside the gap, then leaving) sends at once at head. No loss. |

No Blocker. No Major. The behaviour attack found no way to lose a change (below).

## THE BEHAVIOUR, attacked (own cells in a scratch test file in the clone, moved out after; names B1 to B13)
All GREEN at head, each a possible loss or wrong state:
- leaving inside the gap sends at once (G5), and leaving after the quiet interval already passed inside the gap (trailing owed) sends at once (B6), no timer left (`vi.getTimerCount()` 0);
- browser unload: the prompt is armed all through the gap and disarmed after the trailing save (G14); nothing is sent on unload (the screen has no unload save at main; the kit retracted it);
- explicit Save draft and Save & calculate inside the gap are not delayed (G8), and an explicit save with a trailing save owed leaves nothing more to send (B4: 2 calls, still 2 after 30 s);
- a refused save: gap started, next edit held and sent at gap end (B1, F3); a conflict stops it as before (existing cell);
- two quick edits around the gap's end make one save (G12, B3); an edit landing exactly when the gap ends makes one save, not two (B3);
- unmount and remount inside the gap: second request inside 10 s of the first (B12), the stated limit L-B, nothing lost;
- a save still out when the gap ends: no second request while busy, the newer edit stays Unsaved, is sent 2 s after the first returns, last value saved, nothing after (B2);
- the stamp never reads Saved while a change is pending (G9, and B2); the prompt stays armed (G14); no spurious save with nothing dirty over 50 s (B13); the gap reopens after it ends (B11).
Mutants of my own beyond the builder's nine (each caught by at least one cell, except W, E partly and C2 equivalent): A trailing flag never cleared (G4, B11); B gap armed only after a refusal (9 red, among them G2, G3, G4, G9, G12, G14); C and C2 leave save skipped when trailing set (C stale closure: equivalent; C2: equivalent, F9); D gap applied to Calculate (G8); E running gap not cleared on re-arm (G5, B10, B6); F gap armed after the response (B1, B2; no owned cell: see F2 family); H trailing fires without the flag (G4, G12, two existing refusal cells); Q gap never reopens (G3, G12, one existing cell); R change inside the gap dropped, no trailing flag (G2, G3, G4, G14, changed cell); S unmount does not clear the gap (G5, G11); T an edit opens the gap (G2, G3, G4, G9, G12, G14, changed cell); U quiet cleanup keeps the flag (G12); V gap applied to Save draft (G8); W explicit save starts no gap (B10 only: F2); M2 no trailing call (G2, G3, G4, G14, changed cell). Mutant F: no owned cell goes red (the gap armed after the response instead of at the request); my B1 and B2 do. It changes how many requests are sent when a save is slow or refused, not what a user loses; same family as F2.
A mutant that changes what a user loses and that no owned cell catches: none found (the survivors W, E-by-behaviour and F change request counts, not lost changes).

## The count the ticket is about
Reproduced by a program: the 22-burst script (2500 ms pauses, quiet 2000, gap 10000): 6 requests by 60000 ms, 7 by 62000 ms, the last carries "Site 22". The same script with the constant at 0: 22 by 60000 ms and 22 by 62000 ms.

## The whole web check at head b26cfc2 (node v24.22.2)
| Step | Result |
|---|---|
| npm ci --prefer-offline | rc 0 (cache) |
| npm audit --omit=dev --audit-level=high | rc 0, 0 vulnerabilities |
| npx vitest run | head: 149 files, 1734 passed; main (own worktree): 149 files, 1723 passed; +11 = ten cells in the new describe plus G13 |
| npx eslint . | rc 0 |
| npx tsc -b | rc 0, 0 bytes |
| stub browser step (port 9990, MPSCALC_E2E_MODE=stub, VITE_MPSCALC_API_STUB=1, MPSCALC_E2E_START_WEB=1) | list 277 tests in 19 files; run 260 passed, 17 skipped, rc 0 (4.1 min) |
| api-off browser step (port 9990) | list 161 tests in 8 files; run 161 passed, rc 0 (2.5 min) |
| listeners on 9990 to 9999 | 0 before, 0 after each step |
| VITE_MPSCALC_AUTH=entra npm run build, then node scripts/check-bundle.mjs dist | rc 0, 0, "dist: 8 files, 1112886 bytes; markers found 0/57" |
| ci.yml at head | web job steps as above; only workflow file in .github/workflows |
Browser steps ran with no Playwright artifacts kept in the project folder (all under /private/tmp/b1794-gate).

## Other rows of the standard
- Scope (1): exactly four paths, all four are the lane's OWNS (4 of 4); `.css`, package, setting, workflow paths: 0. Added lines holding a quote character in the two source files: 3 (one module path, two comments), 0 string literals reach the screen. blur, pagehide, visibilitychange, addEventListener over 207 added lines: 0 (the scan found the planted words in a control string). Date.now, performance.now, new Date: 0 added.
- Merge (2): `git merge-tree --write-tree debb5e2 b26cfc2` rc 0, tree e3b73c81795331e71a35be61cc2fe35c5aa3024c = the head's tree (the head is main plus one commit). Overlap with open pull requests: 0 (0 open); sibling lane (the B1791 kit, `infra/tests/test_infra.py`): no shared path.
- Scans (8): names Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Tuesday, Wednesday, Friday and B-numbers over added lines and the commit message: 0 each, with the underscore-aware control firing for each. Non-ASCII added lines 0; format (Cf) characters 0; `new RegExp(`, innerHTML, dangerouslySetInnerHTML, eval, child_process, eslint-disable, waitForTimeout, .only(, ts-ignore, localStorage, sessionStorage, fetch(, sendBeacon, keepalive, screenshot, video, trace, http, .local: 0 each (no per-row control run by me; the name and quote rows have one). gitleaks over the range: rc 0, no leaks (no canary control by me). Commit author and committer: the repo's configured address, equal (git log), no name in any landing text.
- CodeQL (9): local CodeQL 2.27.4, javascript-typescript database of the head, suite javascript-code-scanning.qls: 0 results over 305 JavaScript/TypeScript files and 1 Actions file (no planted control). Reasons to expect a hosted alert: none (timers and refs only, no new sink, no regular expression, no HTML, no file or process access). The hosted run on the pull request is the authority.
- Closed lines (5): none claimed ALREADY-ON-MAIN beyond `AUTOSAVE_MIN_GAP_MS` absent at main (it is added here).

## NOT RUN
CodeQL for python, csharp (not touched; csharp cannot extract on this box) and the hosted CodeQL run. The python and dotnet CI jobs (nothing they read changed). Any run against the real API or the real server (the browser steps use the dev stub and no API). A real browser tab closed, crashed or discarded inside the gap. A planted-canary control for gitleaks and CodeQL. The mutant runs cover the two files, the flush file and my attack cells, not the whole suite. Hosted CI.

## Landing files in this folder
pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt (merge pinned to the head; wait script with `--min-checks 9`, the 9 check runs on PR 222's head read by gh api -X GET), FOR-RECORDS.md. PRNUM is a placeholder to substitute.
