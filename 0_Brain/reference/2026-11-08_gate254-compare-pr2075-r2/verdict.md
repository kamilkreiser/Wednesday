GO WITH NOTES

# Gate 254: COMPARE, PR 2075 round 2 (KS-2083), wording only. Tier 2, Sonnet.

Nothing blocks. Head 32aa0d06bc0a is a wording-only move of two fragment files, every citation the new words make is true at that head, and the checks pass. Notes are minor (below).

Method: my own fresh clone (by sha, via refs/pull/2075/head; FETCH_HEAD = 32aa0d06bc0aceccb790443bbf16384ff0c8e930; d2245bf37fe0c9a096dd8e90fb006035d454e753 is an ancestor of it; develop a65ae7ed1d6083bde60c4198a60a528129277c40 resolves). Nothing fetched into anyone else's checkout. Nothing pushed, posted or edited.

## Q1. Exactly the two fragment files, 0 product or test bytes: YES
`git diff --stat d2245bf37fe0..32aa0d06bc0a`: 2 files, 4 insertions, 4 deletions: `Projects Documents/fragments/cheat/KS-2083-a-role-change-ends-the-sessions.html` and `.../flow/KS-2083-a-role-change-ends-the-sessions.html`.
Counts: paths not matching the KS-2083 fragment name = 0; matching = 2. Planted control: the same counter on `d2245bf37fe0 vs develop` returns 32 non-KS-2083 paths, so it does count what it should. Matches the seat's claim.

## Q2. Each changed sentence against code at 32aa0d06bc0a (path prefix `Blockchain/Dev/services/auth/src/`)
- session.ts:286 `updateSessionActivity`: line 289 `redis.get`, lines 291-293 parse, set lastActivityAt, `redis.setex(..., SESSION_TTL_SECONDS, whole record)`. Reads then writes the whole record, no isActive check, not atomic. TRUE. `revokeSession` (313-328) writes isActive false then `srem`s the id from user_sessions (324), so a stale write after it restores an active record with a fresh TTL that no revoke-all can find. TRUE. TTL = SESSION_EXPIRY_HOURS default 24 (session.ts:102, 119): "fresh 24 h" TRUE at the default.
- Called per request from middleware/authenticate.ts:160 after `validateSession` at 154. TRUE.
- "On develop today for every revoke": `git diff a65ae7ed1d60 32aa0d06bc0a -- session.ts` is empty, so the race code is develop's. TRUE.
- session.ts:332 `if (!redisAvailable) return 0;` TRUE. routes/users.ts:846 `const sessionsRevoked = await revokeAllUserSessions(id);` and :847 logs `sessionsRevoked` via `logger.info`. TRUE: 200, role written (earlier), nothing revoked, info level.
- routes/users.ts:844 `roleChanged = safeUpdates.role !== undefined && safeUpdates.role !== target.role` compares to the row, not the token. TRUE.
- Fail-closed line "401 with the store flag down, 500 with the store rejecting (measured by gate 245)": gate 245 verdict line "flag down 401, store rejecting 500, peer unchanged both ways". Code agrees: `getSession` returns null when `!redisAvailable` (session.ts:270). Matches. (I did not re-measure the 500 myself.)
- "Their next request gets 401 ... unless one of their requests was in flight" (cheat): consistent with F1.
- "Does not close" list in both fragments covers F1, F2, F4 as gate 245 asked. F3 (constructor/__proto__ roles) is not in the wording; the seat said it is a filing seat's, and it is old behaviour. Not a finding.

## Q3. Unqualified "closes the walk-around": NONE
Searched both fragments for clos / walk-around / resolved / fixed / prevent. Hits:
- flow line 3: "For a request sent after the change, it closes the walk-around KS-2063 names ... It does not close it for a request already in flight when the sessions end ..." (qualified, and the next sentence withdraws it for in-flight).
- flow line 5 heading "What this does not close." and "Auth's own check fails closed on a store outage ..." (not the walk-around claim).
- cheat: only "Not closed:". No "closes" at all.
The old unqualified sentence ("It closes the walk-around KS-2063 names") is gone. The PR body and ticket comment are out of scope (live body still says it, per the seat; staged).

## Q4. docs-fragments check at the head
`node Blockchain/Dev/scripts/docs-fragments.mjs check` (run with the clone as working dir): rc 0. Last lines: `docs-fragments: flow 117 legacy + 199 new, cheat 112 legacy + 199 new; lint clean, render passes html_docs_check` then `OK`. Two ADVISORY lines (committed page differs at flow line 6249 and cheat line 6235), the same lines the seat reported.
Planted defect: `<!--n-->` replaced by `99.` in the flow fragment: rc 1, `FAIL — 2 finding(s) in the fragments`, naming the fragment ("the <h2> must start with <!--n-->" and "carries a literal section number"). Fragment restored byte-for-byte (git status clean, check rc 0 again).

## Q5. Merge tree
`git merge-tree --write-tree a65ae7ed1d60 32aa0d06bc0a`: rc 0, tree `2737b8fb022303833c404a5740066f2fd9c1eb9d` (matches the seat's 2737b8fb0223). It differs from develop in exactly 4 paths: the two fragments, routes/users.ts, and the ks2083 auth test.

## Notes (none blocks)
1. N1, MINOR. "session.ts:286" is the function declaration line; the read is at 289 and the write at 293. It points at the right function and "read then write" is true, but a reader checking the exact line sees a signature, not the read.
2. N2, MINOR. The flow fragment ships "to be ticketed High by a board seat" and "Kam's card ..., option a" with no ticket key (none existed at the seat's read). A ticket key should replace the phrase once it exists; a later wording round, not this merge. I did not check Linear.
3. N3, NOTE. The page text says "measured by gate 245" and "Gate 245 measured this on a stand-in store, not on real Redis": internal process wording in a shipped doc fragment. Harmless and honest about the evidence level; Kam's call.
4. N4, NOTE. The 2 ADVISORY lines and the stale committed pages are unchanged by this round (committed pages lag fragments by design).

## What I did NOT test
- The auth code itself, the auth suite, the 29 cells, tsc, eslint (all unchanged since gate 245; no byte of product or test differs).
- The 500-on-store-rejecting and 401-on-flag-down behaviours at runtime (relied on gate 245's measurement plus reading `getSession`).
- Real Redis; the race rates.
- The PR body, the ticket comment, Linear state, develop's other 30 changed paths (only that they do not touch KS-2083 files: develop-vs-d2245 list shows the 4 PR paths plus other fragments; I did not audit them).
- Whether the live GitHub PR matches the pin beyond FETCH_HEAD = 32aa0d06bc0a at my fetch time.

My clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02fe044e-b48b-4f7e-8397-447f163806d4/scratchpad/g254clone`, 646 MB, detached at 32aa0d06bc0a, not removed. Scratch files beside it: chk1.txt, chk2.txt, flow.orig in the same scratchpad directory. (An earlier failed clone attempt left at most an empty `/private/tmp/claude-501/g254/`.)
