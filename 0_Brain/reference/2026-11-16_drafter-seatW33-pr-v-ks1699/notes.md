# Drafter notes, Seat W 33rd PR-V (KS-1699), 2026-11-16 10:48 AEDT

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatW33_pr_v_ks1699.md (44,958 bytes). Scratch and copies: ./_work/.

## Decisions for Wednesday at the stamp
1. STAMP block is blank. The brief says the stamp either pre-sets OVL_IGNORE_PRS="2225 2160" for PR-V's push only (as she did for PR-N) or the seat mails the refusal.
2. Whether the seat writes a GitHub comment on PR 2225 (the commission says "a facts comment that 2225 is superseded"); the brief makes it conditional on the stamp keeping that line. The KS-1855 Linear comment is firm.
3. D8, D9, D10 are MY defaults, not rulings: D8 charge discriminator `req.user` (not `getUserFromRequest`); D9 new limiter skips Bearer-carrying requests (anonymous only); D10 CSRF cookie refusal pinned as a stated limit, csrf.ts not edited. D1-D7 and G-A5 carried as Wednesday's plan ANSWER settled them.

## Findings that differ from W 32nd's brief or HANDOVER
- develop moved 9ddba202bb15 -> cf2b2a1a5d5f by ONE commit (PR 2064, KS-1205): rateLimitEnforce.ts, a new gateway test, two fragments. No PR-V file. The new ks1205 test pins audit-mount order from index.ts text.
- Charge discriminator trap: `if (verifier)` (getUserFromRequest) would stop charging a signed-in token without userId (develop charges it as 'anonymous'). Gate on req.user.
- Limiter: global is 300/min/IP production and counts cert verify today; a separate 60/min limiter on all callers cuts signed-in callers 5x.
- Door missed: the OpenAPI auth gate is NOT a door (spec has no /{id}/verify; checked yaml and the `[^/]+` regex). Limit missed: CSRF 403 for an anonymous POST carrying a cookie (read in csrf.ts and index.ts lines 372-379; CSRF is off in NODE_ENV=test, so cells need development).
- W 32nd's "SDK and issuer UI declarations of chargeEventId (~line 129, ~481)": not found; 11 repo hits, none reads the verify response.
- Originate has app-level rejectNulBytes(), so ks815's three NUL cells can be deleted or moved rather than rewritten (to be measured by the seat).
- PR-V touches neither file of PR 2249 (originate verification.ts / verificationV2.ts); the same-basename gateway verification.ts is PR 2225's file.
- W 32nd's test file is unchanged (sha256 bb7fa1a7... equal to the evidence draft, tree HEAD 9ddba202bb15, one untracked file).

## Measurement instruments and controls (this session)
- develop sha: gh api branches/develop at 10:33:44 and re-read 10:47:45, both cf2b2a1a5d5f (no movement during drafting). compare 9ddba202bb15...cf2b2a1a5d5f = ahead 1, 4 files.
- Open PRs: gh pr list = 60; file rows 340 via pulls/<n>/files; positive control PR 2249 = 11 rows; overlap by grep -F over rows (0 for proxy.ts, gateway index.ts, originate middleware/auth.ts, originate index.ts; control routes/verification.ts -> 2225).
- Ordinal: grep -a -c -i on history.md: W 33rd 0; controls W 32nd 1, W 31st 1, C 42nd 2 (C 42nd read 1 at 09:2x per the older brief, now 2: the control drifted, a count not a defect).
- Branch name: grep -c -x over 1,539 branches = 0; control (PR 2249 branch) = 1.
- OpenAPI: grep -c -i '^  /api/certifications.*verify' = 0; control '^  /api/' = 313; certifications paths 3 (issue, list, {id}).
- checkDocumentExists in gateway verification.ts = 3; control function makeCheckDocumentExists = 1.
- chargeEventId: grep -r -i over sdk, frontend, originate routes, gateway src (non-test): 11 hits (control: certifications.ts createChargeEvent = 9).
- Linear: read-only GraphQL, key read in-process, never printed (KS-1699 In Progress, KS-1855 In Progress, KS-834 Backlog, KS-1280 Backlog, KS-1995 Backlog).
- Not run: any suite, tsc, eslint, merge-tree (needs a tree; no write in !CODING), coagent inbox (no mail key used).

## Limits of this draft
- Gateway cell designs (G-A1..G-A8, G-L1, case cell) are designs from reading, never run. Predicted mutant sets are predictions.
- The brief is 44,958 bytes after three trimming passes; the provenance uses brace lists for some sibling files in one directory.
- The hoist-vs-wrapper choice for registering the originate route before line 66 is a drafter reading (function declarations hoist; a const handler would be in TDZ); the seat states its diff shape in the plan.
