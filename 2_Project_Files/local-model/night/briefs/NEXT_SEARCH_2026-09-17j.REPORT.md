# NEXT SEARCH 2026-09-17j (14:52-15:02 AEST): widened past auth (gate pins, bash/doc, non-auth)

**BLUF: NO FITS. Nothing briefed, built or queued.** The rejection table is appended to `night/candidates.md` as `## SEARCH 17j` (backup `candidates.md.pre-1502-search17j`).
- **Closest, blocked on the partition only: KS-928.** It is a test-only jest pin with its fix shape and red-proof spelled out, in originate `routes/adminConfig.ts:1893`. That file belongs to the held READY_KS-730-B.
- **Next closest: KS-1179 F-6.** The builder's title-slug test path is the new file of the held READY_KS-1179-F1.
- **Freeing it up:** Wednesday's call on test-only tamper targets frees KS-928; KS-730-B merging frees both KS-928 and the KS-730 follow-ons. KS-1140 and KS-1131 carry a stale partition reason (see the flag below).

## Instruments
- **Tip:** `d7e95cd9f153e9036ed77935a73c93504fa6e3dc`. `git ls-remote` of the source's origin URL from scratch clone `/private/tmp/claude-501/night/s17j/clone`, read at 14:53:39 and 15:01:13; it did not move.
- **Linear** (GraphQL read, first:50): 328 KS Backlog/Todo at 14:53:49, 7 pages, hasNextPage false on the last. The newest updatedAt is 02:27Z (KS-1202), so no ticket moved after 17i's 13:33 pull.
- **Open PRs** (REST GET, 14:54:14): 20 PRs, 102 paths. 0 name adminConfig.ts, demoSeedGate, ssrf-guard, run-shell-suites or ks879/ks963/ks781/ks860. Control: 55 paths under services/. PRs #780, #874, #879 and #888 are closed and merged (15:00:25).
- **Seat A heads** (`diff --name-only` only, 14:54:14): the same 15 paths as 17g-17i.
- **09-17 READYs:** 24 diffs, 30 `+++` paths.
- **Source porcelain:** 0 at 15:01. Control: the scratch clone read 1 with one edit and 0 after restore.
- **Checker:** not run, because no FITS. No checker, builder, queue.md or night_run.sh was touched.

## FOUND / TESTED / HOW
- **HOW (widening predicate):** the pool minus every KS id named in a recorded record. Records are the comment blocks of git 3e68f4132 and today's candidates.md, the HELD and SET ASIDE lists, NEXT_SEARCH 17/b/c/d and DEFAULTS.
  - That left 22 tickets: 18 are Peter's or Stuart's, and 4 were excluded only as "PR attached" (KS-749, KS-928, KS-948, KS-964). Their PRs are merged, so all four were read.
  - Also read: the unrecorded residues of held gate follow-ups, and the 21:0x title-level-only doc and script rows.
- **FOUND:**

| ticket | verdict | reason | instr |
|---|---|---|---|
| KS-928 | NEAR-FIT, partition | Test-only jest pin with shape (a) spelled: mount the router with env stubbed, ks444/ks445 pattern.<br>Call site moved :1824 → :1893 `    if (!isDemoSeedEnabled()) {` (ASCII, count 1). 0 executable tests hit seed-demo-users, and ks764 already mounts the router.<br>Blocked: adminConfig.ts is READY_KS-730-B's file (hunks -184,7 / -216,19; net +3 lines above :1893).<br>Slug: ks928-the-demo-seed-gate-s-predicate. Peter's comment asks to keep 403 + DEMO_SEED_DISABLED. | measured |
| KS-1179 F-6 | refused | Product fix at ssrf-guard.ts:482-483 (clearTimeout after the await).<br>The slug test path is READY_KS-1179-F1's new file (code_1179.json; build_input.sh:310-312).<br>A test_file= modify-in-place breaks the name rule. | measured |
| KS-1179 F-4/F-5 | refused | Docblock is comment-only. F-5's error wording is unspelled, and ks932 (READY F2F3) reads it. | read |
| KS-948 | refused | Hoist location and mode are unpicked. The mixed-backtick fail-open needs a regex design. The + lines would carry backticks and backslashes. run-shell-suites.sh is in READY_KS-1089 and READY_KS-1127. | read + tip |
| KS-964 / KS-749 | refused | KS-964 is an investigation. KS-749 is a lockfile change plus a frontend build. | read |
| KS-1040 reset half | refused | The fix site is path-resolvability.mjs:86, a .mjs that no tier grades. | git grep |
| KS-987 items 2-4 | refused | Notes outside the repo, a post-deploy assertion with no named script, and an audit. | read |
| KS-709 KS-770 KS-1155 KS-872 KS-1102 KS-903 KS-846 KS-785 KS-768 KS-1154 KS-829 KS-725 | refused | Live run, review checklist, owner's call, either/or, survey or harness owner. | read |
| KS-1180 1181 1182 1185 1188 1192 1193 1199 | stand | Every finding row is held or recorded. | read |

- **STALE-REASON FLAG** (not re-derived; updatedAt unchanged):
  - KS-1140 (the 284-line ks879 guard) and KS-1131 (the 327-line ks963 auth test) were refused on 09-16 only as "seat A partition". Neither file is in today's partition.
  - KS-1143 and KS-1144 stay partitioned, because ks781-p3-3 is in seat A's heads.
- **TESTED:** tip, pool, PRs, partition, READY hunks and PR states, as listed above. Also: the KS-1179 slug, from code_1179.json and the builder source.
- **NOT tested:**
  - no premeasure of KS-928's gap (no suite run under the tamper);
  - the KS-1179 F-6 rejection path, which was read, not driven;
  - no builder or checker runs.

## Queue line
None.
