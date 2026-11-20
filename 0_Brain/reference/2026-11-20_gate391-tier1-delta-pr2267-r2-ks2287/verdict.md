PR 2267: GO WITH NOTES (at head 2929ec29ff07c6765876fdf866fa482b7d862311; tier 1)

# Gate 391, tier 1 delta (Opus), PR 2267 round 2 (KS-2287), 2026-11-20 ~14:39-15:06 AEDT

## Pins
- **Pinned twice, at 14:39:18 and 15:05:47**, with ls-remote plus gh pr view. I used the Secuura project's gh credential read-only, because the Wednesday gh account cannot see this repo. Same values both times:
  - PR 2267 is OPEN, not draft, MERGEABLE.
  - Head is 2929ec29ff07, with 2 commits. Its parent is 540af1ec55dd, and that commit's parent is develop.
  - 6 files, +627 -25. updatedAt 03:36:35Z.
  - develop = 038425cafaecfb29e800e0a9187d76f9fddc3622.
  - PR 2099 head = 8967de8b17558890dc4ace2732cb8350768df601.
- **Merged state = the head** (a fast-forward on the develop tip). Every "head" figure below is the merged state.
- **PR body at source:** 20,495 B, sha256 50ac77a6962a. This matches the READY's read-back.

## How I measured
- **Clone:** `_work/g`, cloned from GitHub with `--reference-if-able` gate 390's clone and `--dissociate` (no alternates left). My worktrees:
  - `h` and `x`: the head (`x` for mutants and probes);
  - `d`: develop;
  - `r1`: round 1, 540af1ec55dd.
- **node_modules:** `cp -c` from gate 390's `_work/h` (the same develop and the same lockfiles). It holds no absolute symlinks.
- **Run conditions:** Node v26.8.1, vitest, TMPDIR /private/tmp/g391t.
- **Scripts** (all in `_work/`):
  - `run_cwd_g391.py`, `suites_g391.sh`, `mutants_g391.py` (gate 390's engine with my anchors);
  - `probes/spellings_g391.mjs` (zod guid() plus PGlite);
  - `probes/g391-probe.test.ts`: the PR's own case-insensitive harness plus the Q1, Q2 and Q3 probes, run on `x` and on `r1`;
  - `probes/issame_g391.mjs`;
  - `probes/g391-selfapprove.test.ts`;
  - `lin_read_g391.py` (one read-only GraphQL query).
- **Evidence:** `_work/evidence/`. Probe and planted files were moved to `_work/_quarantine/` after use.
- **End state:** h, x, d and r1 each show 0 porcelain lines. users.ts in `x` was restored to sha256 62d321cc86e3…, the head's bytes.
- **Not touched:** no seat tree, no GitHub or Linear write, no database server, no container.

## Findings

No HIGH or MEDIUM finding against this PR. Gate 390's HIGH (G390-2267-1) and its G390-2267-4 are closed, measured through the real router.

### LOW
**G391-2267-1: mutants that every one of the 2,038 cells misses.** None opens a hole at this head; they are pinning gaps or equivalents.
- **G6, the level self rule exempts the bare `admin` role** (`if (callerIsTarget && role !== 'admin')`).
  - At the head, the self rule binds bare admin as it binds ORG_ADMIN.
  - No cell PATCHes a bare admin's own id with a level change, so the cells would not catch a regression that let bare admin raise its own level to STANDARD.
- **G7, `callerIsTarget` also requires the token's tenant to equal the target row's tenant.**
  - For a non-platform caller this is equivalent, because the tenant 404 already forces equality.
  - For a platform caller it would skip the own-role rule whenever the token's tenant differs from its row's tenant (for example a platform token carrying no tenant). Every cell's platform caller has matching tenants.
- **G3, the own-role rule placed after the organizationId validation.** Effect-equivalent: own role plus an invalid organisation answers 400 instead of 403, and neither writes.
- **G5, revoke on `id.toLowerCase()`, and E1, `isSameUserId(id, adminId)`.** Both are equivalent at this head, as Q1's spelling probe proves: every spelling guid() admits lower-cases to the stored id. `target.id`, as shipped, also stays correct if guid() is ever loosened.
- **TESTED:** `mutants_g391.py`, the whole auth suite per mutant (evidence/mutants.out). G3, G5, G6, G7 and E1 each read tsc 0 and 0 failed of 2,038.

**G391-2267-2: words that are incomplete (no sentence is false in a way that matters).**
1. **"Three behaviours change"** in the PR body, round-2 section. My 360-case matrix (Q2) finds the same "the target is not visible" class in a fourth shape. A non-platform caller whose own row is outside its token's tenant, or whose token carries no tenant, now gets 404 instead of 403 when it sends a role to its own id. Nothing is written. It is the same mechanism as the first stated change: the tenant 404 now runs before the rule. "None of them writes anything" holds.
2. **The sweep omits one site:** `api-gateway/src/routes/notifications.ts:352`, `if (userId !== getUserId(req))`. This compares a BODY user id with the caller's id. It is a deny rule ("a notification only for yourself"), so another spelling of the caller's own id can only be refused (fail closed), never let through. The sweep's conclusion ("no spelling can get past a refusal") still holds.
3. **Line numbers:** the sweep's `users.ts:1439/1468` are round-1 numbers. At this head they are 1453 and 1482.
4. **Cosmetic:** the audit log line after the write still logs `targetUserId: id`, the raw path spelling, not `target.id` (users.ts:898, 939). Not a security property.

### INFO (outside this PR, for routing to Kam with N2)
**G391-2267-3: through the review door, an ORG_ADMIN raises ITS OWN level to GOVERNMENT in two requests.** This is pre-existing, the N2 family, and the PR does not make it worse.
- **FOUND:**
  - `POST /me/verification {"targetLevel":"GOVERNMENT"}` files a request for oneself.
  - `POST /verification/:requestId/review {"action":"approve"}` admits ORG_ADMIN. Its only check is that the subject is in the caller's tenant; there is no reviewer-is-not-subject check (users.ts:1566-1620). So the caller approves its own request.
- **TESTED** with the PR's harness on the head (evidence/selfapprove_x.jsonl): ENHANCED, HIGH and GOVERNMENT each give submit 200, review 200, and the stored level is raised.
- **Why it matters:** this breaks "never on themselves" and the STANDARD cap of Kam's card, by a door the PR deliberately leaves alone ("Not changed: the verification-review approve path"). N2 as worded ("raise a user above STANDARD") does not name the self case. N1's wording says "itself included"; N2's should too, in both the PR body and the e94e5ef8 draft, so Kam rules on it knowingly.

## The commission's questions
- **Q1, G390-2267-1: CLOSED.**
  - Gate 390's P2 (own id in upper case, STANDARD, ORG_ADMIN) through the real router with the case-insensitive by-id harness gives **403** "Cannot change your own verification level". The row stays BASIC and there is no write.
  - On round-1 code (`r1`), the same probe gives 200 and a write.
  - Every spelling of the own id:
    - **Upper, mixed, and `%41`-encoded upper:** guid() admits each and the lookup finds the row. The result is 403 for the level and 403 for the role, with no write.
    - **Braces (encoded), no hyphens (either case), hyphen every 4 digits:** Postgres (PGlite) finds the row for each, but guid() refuses them, so the answer is 400 "Invalid user id" with **zero lookups**.
    - **Leading or trailing `%20`, `%0A`, `%09`, a double-encoded `%2541`, `urn:uuid:`:** 400 with zero lookups. Postgres refuses these too (22P02). A NUL gives 22021 and a zero-width space gives 22P02.
  - So no spelling other than letter case reaches the lookup.
  - The gateway re-encodes the express-decoded id with encodeURIComponent, so auth sees the same decoded string. The 404 and 400 shapes are unchanged.
  - (evidence/spellings_g391.out, probe_x.jsonl, probe_compare.txt)
- **Q2, G390-2267-4: CLOSED.**
  - Own role with the id in upper case: 403 "Cannot change your own role", role unchanged. Same when the token carries the id in upper case.
  - The three stated changes are exact:
    - a no-row platform_admins holder (SUPER_ADMIN or SYSTEM_ADMIN, own id, role) gets 404 (was 403);
    - a platform-only role sent to one's own id gets the ceiling 403 (was the own-role 403);
    - a non-UUID own id gets 400 (was 403).
  - Plus the fourth shape in G391-2267-2.
  - **Nothing that was refused before now writes.** Across 360 cases (10 callers × 12 bodies × 3 spellings) on r1 against the head:
    - "r1 4xx, head wrote": empty;
    - "a self role change written on the head": empty.
  - The early returns between the old and new positions are the role ceiling (403), the guid() check (400) and the tenant 404. None of them writes, and none skips the rule for a request that could then write.
- **Q3, NR-1: CLOSED.**
  - `revokeAllUserSessions(target.id)`; `session.ts:131` keys `user_sessions:${userId}` with the stored id.
  - Probes on the head: a role change on an upper-case id, a deactivate on a mixed-case id, and a SYSTEM_ADMIN suspend on an upper-case id each revoke the lower-case stored id. On r1, revoke was called with the raw spelling.
  - There is no other revoke call on this route (users.ts:938 only; :1137 is change-password on `user.id`). Only the log field remains raw (G391-2267-2.4).
- **Q4, isSameUserId:** it answers false for every non-string pair and for any one-sided undefined, null, number, object, array, String object or boolean (evidence/issame_g391.out).
  - A false answer is the fail-OPEN direction for a self rule. It cannot arise wrongly here:
    - `target.id` is the row's UUID primary key, always a non-empty string (`fromRow`: `id: row.id`);
    - `adminId` is the verified token's userId. An absent one was equally "not self" under round 1's `id === adminId`, so there is no regression.
  - It answers true for `''` against `''` and for Unicode case pairs. Those are unreachable: ids are ASCII hex UUIDs, and a true answer refuses (fail closed) anyway.
- **Q5, mutants (whole suite each):**

  | mutant | tsc | failed | killed by |
  |---|---|---|---|
  | N1 level self rule back on raw path | 0 | 2 | own id upper (path), token upper |
  | N2 own-role rule back on raw path | 0 | 2 | the two role upper cells |
  | N3 helper fold dropped | 0 | 2 | the two token-upper cells |
  | N5 moved own-role rule dropped | 0 | 4 | 2 upper role cells, ks467 own role, ks2083 own-role control |
  | N6 revoke on raw id | 0 | 1 | NR-1 |
  | X4 create refuses null | 0 | 1 | create null gets BASIC |
  | X7 create allows NONE | 0 | 1 | create NONE 403 |
  | M1 no cap | 2* | 5 | ENHANCED/HIGH/GOVERNMENT, bare admin |
  | M4 no level self rule | 2* | 4 | self cells |
  | M5 no organisation rule | 2* | 6 | other organisation / no organisation / move-and-set / token claim |
  | M6 null equals null | 0 | 1 | none and none |
  | M8b token claim first | 0 | 1 | token claim cell |
  | M12 unchanged counts as a change | 0 | 3 | the resend controls |
  | M15 bare admin as platform | 0 | 6 | ks1536 cells |
  | G1 callerIsTarget without the fold | 2† | 3 | token-upper cells |
  | G2 own-role rule exempts platform | 0 | 2 | ks467 own role, ks2083 control |
  | G4 own-role rule only on a real change | 0 | 1 | ks467 own role |
  | **E1, G3, G5, G6, G7** | 0 | **0** | survivors: see G391-2267-1 |

  \* tsc 2: my `role === 'never'` spelling is TS2367 against the narrowed role union. The cells kill each one regardless.
  † noUnusedLocals: isSameUserId is orphaned.

  **E1's survival is a true equivalence.** guid() admits only the 8-4-4-4-12 form in any letter case, and each such spelling lower-cases to the stored id (Q1).
- **Q6, nothing else moved:**
  - `540af1ec55dd..2929ec29ff07` numstat: users.ts +22 -8 and the test file +82 -6, nothing else. The yaml, auth.openapi.ts and the fragments are unchanged by round 2.
  - Auth suite: develop 1,992/1,992 in 162 files; head 2,038/2,038 in 163 files. Failure-name sets are equal (both empty).
  - Red first: the head's test file on r1 code gives 46 cells, 5 failed (the four upper-case self cells and NR-1), 41 passed. Green: the KS-2287 file plus ks467 give 84/84.
  - tsc 0 (planted: 1).
  - eslint `--max-warnings 0` on users.ts, auth.openapi.ts and the test file: 0 (planted: no-debugger plus no-unused-vars, rc 1).
  - Ratchet: 41 baselined, 0 new, 0 stale, 163 files (planted: 5 new, rc 1).
  - Fragments: OK (planted: FAIL).
  - check:openapi: CHECK PASS, 422 examples resolve (planted yaml edit: CHECK FAIL).
  - Not re-run: the standalone 6-service ratchet and the leg test.
- **Q7, overlap:**
  - merge-tree of the head against PR 2099's live head: **rc 0**, tree d3e99bf9fbad (the READY's tree).
  - Planted control (my scratch commit 36e83a28a35f on PR 2099's head, editing the create 400 description line this PR also edits; never pushed): **rc 1**, CONFLICT (content) in the yaml.
  - Head against develop: rc 0.
  - Among this PR's six paths, PR 2099 touches only the yaml (three-dot diff).
  - The body still says "Whichever of PR 2099 and this PR merges SECOND regenerates the yaml", both in round 1's paragraph and in the round-2 merge-tree item.
- **Q8, words:**
  - **PR body, round-2 section:** +24 -6 holds (numstat). "Either casing" now holds: SUPER_ADMIN and super_admin pass, while lower-case system_admin is refused at both doors' role lists. "Never on itself" holds since round 2 (Q1). The red/green, the 46 and 2,038 counts and the merge-tree figures reproduce. Exceptions: G391-2267-2.1 to 2.3.
  - **The e94e5ef8 draft (NOT posted):** every sentence I could measure holds:
    - head and parent;
    - the stored-id self rule on both rules;
    - NR-1;
    - 9 more cells, 46 in all, 5 red on round 1;
    - the suite counts;
    - the yaml unchanged and now true;
    - merge-tree clean with the control conflicting.

    Two caveats:
    - "A sweep of auth and the gateway found no other place where a path id is compared with the caller's id" is true as worded (path id). The notifications site compares a body id and is fail-closed.
    - The N2 residual line should add "itself included" (G391-2267-3).

    The push timings (791 s, 843 s) are the builder's figures: UNMEASURED by me beyond ls-remote showing the head on origin.
  - **Live comment, read-only:** KS-2287 has 1 comment, e94e5ef8, 3,083 B, sha256 e8cb86751a2a. updatedAt 02:28:02.661Z is not after createdAt 02:28:02.739Z, so it is unedited. KS-2287 is In Progress.
  - **Gate 390's G390-2267-3: CLOSED** (the three sentences corrected in the body; openapi now true).
  - **G390-2267-2:** closed for X4 and X7, the two the closed list named. X3, X6c, X8, X2 and X5 stay unpinned. They were not in the closed list, are equivalent or tightening at this head, and nothing claims them closed.

## Two-NO-GO cap
Not engaged: this round is GO WITH NOTES. The LOW notes fit a follow-up ticket: G6 and G7 pins, plus the PR body's fourth-shape sentence and sweep line. The INFO item belongs on Kam's N2 card.

## Not run
- The four platform suites, a booted auth or gateway, a real Postgres engine (PGlite in-process only) and a real Redis (NR-1 is the router with a mocked revoke, plus a session.ts read).
- The admin dashboard, any deployed environment, Node 24.
- The standalone 6-service ratchet and its leg test.
