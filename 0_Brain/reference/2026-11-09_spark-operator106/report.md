# Spark operator 106 report (2026-11-09 01:57-02:35 AEDT). Secuura only.

## BLUF
- Job 1: 22 tickets read whole at source (every KS ticket numbered 2105 or higher: KS-2105..KS-2126, all Backlog; instrument: Linear paginated read, `number gte 2105`, 22 nodes, contiguous 2105..2126, tickets_ge2105.txt). 6 tickets briefed as 8 passes; ALL 8 PASSED round 1 and are HELD (target was 3). Original-only: no rebrief used. One brief was REBUILT before any model call (README: fence lines in diff context broke the control; control FAIL, nothing sent to the model; old dir moved to night/_quarantine_2026-11-09/briefs_unused/).
- Job 2: all six shadow reviews written BEFORE the Claude verdicts were opened, then compared. Verdict match 3/6 exact (2093, 2095, 2096); the other 3 differ by ONE grade (2094 GO vs GWN, 2097 and 2098 GWN vs GO). 0 NO GO, 0 Majors raised, 0 false Majors; the 10-30 checklist amendment held (the "not in facts.json = Major" shape did not recur). Calibration rows below.
- Pin: develop 01b26bc7 (start) -> c0e6e744 (~02:09) -> 5302a802 (end). Disk is the problem: DevMASTER free 21.4 GiB at start, 18.2 GiB after the rounds, **15.85 GiB at the end (under the 18 GiB STOP)**; other seats were also writing (load1 reached 15.9 at 02:32). I stopped all work; nothing is running. My 8 direct-control work clones (about 0.36 GiB each) in spark/cache/work cannot be pruned by prune_work.py (no verdict row) and I did not delete them: see UNMEASURED.

## Job 1: every ticket read (KS-2105 and up; reading = description + all comments, newest first)
| ticket | verdict | reason |
|---|---|---|
| KS-2105 | not briefed | governance castVote race: DB/concurrency design; governanceService.ts is in PR 2076 (B 102nd), erasure lane U 18th. Claude seat |
| KS-2106 | not briefed | a measurement (whole akto suite on a clean install), no edit to make. Needs a seat that can build |
| KS-2107 | BRIEFED, 2 passes | five "idempotent" comments in originate documents.ts (doc_only). O106-P1 sites 1390/2501/3149, O106-P2 sites 2921/3023 |
| KS-2108 | not briefed | items 1-3 probe/behaviour readings (reconciler, DEMO_MODE, nft getTransaction); item 4 (delete unused `UNREADABLE` const in an anchoring test) fits no tier (doc_only is comments only; test_only_input needs a red cell). Claude seat (trivial) |
| KS-2109 | BRIEFED item 3, 2 of 3 pointers | trustHeaders.ts comment + AGENT-DOCUMENT-OPERATION-RULES.md line. Third pointer (api-gateway index.ts 327-329) is in PR 2083. Item 1 (guard blind spots) is a design choice |
| KS-2110 | drafted, NOT run | brief lints rc 0 (night/briefs/ks_2110_o106_p1_requireplatformrole_undefined_role_row_and_per_route_pin, test_only_input, M4 + G5b cells, plant = golden_red.diff). Stopped at target + disk. Security gate tests: tier 1 gate to be named. Files free (no open PR, no READY). Next operator can dry-run, control, queue it |
| KS-2111 | not briefed | prototype pollution fix = security surface plus a gateway decision |
| KS-2112 | not briefed | portal routing behaviour, no spelled shape (decision) |
| KS-2113 | not briefed | browser/jsdom cells (no frontend test script, KS-1391); item 6 edits an HTML fragment (excluded) |
| KS-2114 | not briefed | behaviour change in security's rotate (High, ruled direction but fix shape is service logic) |
| KS-2115 | not briefed | ks1152 test file is in open PR 2073 (B 102nd merging) |
| KS-2116 | not briefed | tenant-provisioning.openapi.ts and the cheat HTML fragment are in PR 2073; yaml regeneration |
| KS-2117 | BRIEFED, 2 passes | SDK README (P1) and SDK transfers.ts docstrings (P2) say an API key is refused with 403 |
| KS-2118 | not briefed | stranded-row exit: owner decision (expiry vs admin cancel) |
| KS-2119 | not briefed | cross-tenant notification read: security surface |
| KS-2120 | BRIEFED | transferAccess.ts one comment (authorization file: tier 1 gate recommended) |
| KS-2121 | BRIEFED | one cell across the six transfer doors (test_only_input) |
| KS-2122 | not briefed | High cross-tenant identity: security |
| KS-2123 | BRIEFED item 1, 2 of 3 mutants | ADMIN row + per-type cell. NOT covered: x-user-id header mutant (needs the real middleware) and item 2 (OpenAPI example) |
| KS-2124 | not briefed | PR 2066 is open and the code is not on develop |
| KS-2125 | not briefed | two-number edit in a JSON baseline: no tier accepts a .json file. Claude seat (trivial) |
| KS-2126 | not briefed | auth OAuth scope check: security |
Counts: read 22 / briefed 6 (8 passes) / drafted-not-run 1 (KS-2110) / not briefed 15. Next screen starts at KS-2127.

## Held passes (8; `ls night | grep O106`)
All: doc_only or test_only_input, strict apply rc 0 at tip c0e6e744b7b2 (hold_ready STRICT-APPLY leg), golden TREE-IDENTICAL, 9 of 9 checker legs, CONTROL-PASS first (direct `round.sh --control`, run dirs `...-control`; KS-2123's control went through queue.sh).
1. READY_KS-2107-KS-2107-O106-P1_spark-dsv4flash_BRIEFED-DOCONLY-DOCUMENTS-PASS-9of9_2026-11-09.diff.md
   hold_ready: `golden: TREE-IDENTICAL; touched=[originate routes/documents.ts] plus=9 minus=5 legs=9 expectations=7`. NOT covered: the share (2921) and revoke (3023) comments (P2); line 700's unrelated "idempotent". Tier 2. Text ties to KS-1384 (Kam's ruling).
2. READY_KS-2107-KS-2107-O106-P2_...DOCUMENTS-PASS-9of9_2026-11-09.diff.md
   `plus=4 minus=2 legs=9 expectations=3`. NOT covered: the other three comments (P1). Disjoint hunks from P1 (>400 lines apart): raise together.
3. READY_KS-2109-KS-2109-O106-P1_..._DOCONLY-TRUSTHEADERS-PASS-9of9_2026-11-09.diff.md
   `touched=[api-gateway trustHeaders.ts, docs/security/AGENT-DOCUMENT-OPERATION-RULES.md] plus=2 minus=2 legs=9 expectations=4`. NOT covered: index.ts 327-329 pointer (PR 2083) and item 1 (guard). Tier 2 (comment/doc; new text claims `isPlatformRole` gates the override: checked at gateway middleware/auth.ts line 697).
4. READY_KS-2117-KS-2117-O106-P1_..._DOCONLY-README-PASS-9of9_2026-11-09.diff.md
   `touched=[sdk/javascript/README.md] plus=4 minus=1 legs=9 expectations=4`. NOT covered: the Quick Start `// Initialize with API key` line (its diff context holds a code fence which breaks the one-block check) and other SDK docs. Tier 2.
5. READY_KS-2117-KS-2117-O106-P2_..._DOCONLY-TRANSFERS-PASS-9of9_2026-11-09.diff.md
   `touched=[sdk/javascript/src/modules/transfers.ts] plus=3 minus=3 legs=9 expectations=4`. NOT covered: delegation methods, other modules. Tier 2. Raise with P1.
6. READY_KS-2120-KS-2120-O106-P1_..._DOCONLY-TRANSFERACCESS-PASS-9of9_2026-11-09.diff.md
   `touched=[transfer transferAccess.ts] plus=3 minus=1 legs=9 expectations=3`. Comment only, but the file is the transfer authorization decision: recommend a tier 1 gate (rule: security surface). NOT covered: whether any platform_admins row holds a connector value; the Azure column CHECK (KS-1536's question).
7. READY_KS-2121-KS-2121-O106-P1_..._TESTONLYINPUT-INDEX-PASS-9of9_2026-11-09.diff.md
   `touched=[transfer ks2081-...test.ts] plus=15 minus=0 legs=9 red_cells=1 products_unchanged=1`. Plant: per-door header in refuseNonUserPrincipal. NOT covered: other key kinds across doors (R1 pins bytes for all three). Tier 2.
8. READY_KS-2123-KS-2123-O106-P1_..._TESTONLYINPUT-NOTIFICATIONS-PASS-9of9_2026-11-09.diff.md
   `touched=[api-gateway ks1448-...test.ts] plus=9 minus=0 legs=9 red_cells=2 products_unchanged=1`. Plant: guard only security/system and exempt ADMIN (my reading of the gate's plants, not its files). NOT covered: x-user-id header mutant; OpenAPI example. Tier 2.
Overlap: P1 and P2 of KS-2107 share documents.ts (disjoint hunks). Overlap with O105-P1 (originate email.ts) and KS-2099: none (different files). No READY in night/ named any of my files before I started (positive control: accountLockout.ts found 1).

## Job 2 calibration rows (Spark review written first; heads = gate heads, all unmoved by ls-remote; deterministic half = spark_gate.sh targeted red/green on base vs head, vitest/jest; facts in j2/pr*/facts.json)
Instrument note: spark_gate.sh needed a hand-built node_modules farm (shared package built in scratch) and, for the docs-only PR 2097, a hand-written facts.json (the runner refuses a run with no test file). Reviews: 25-44 s, 9-21K prompt tokens, all valid JSON, attempt 1, no loop.

CALIBRATION 6 (2026-11-09 ~02:2x, tier 2, six PRs, Spark = deepseek-v4-flash-0731 via spark_review.py; Claude = gate 264 / 265, Sonnet)
| PR | Spark | Claude | match | recall of Claude's findings | Spark findings checked at source | facts match |
|---|---|---|---|---|---|---|
| 2093 (KS-2053, cell) | GWN, 4 Notes | GWN, 1 Low | yes | 1/1: Note 4 "mountLine returns first occurrence" = Claude's decoy-comment finding | Notes 1,2 (test reads index.ts text, harness mounts its own strip) are TRUE (test lines 155-156, 340-350) but are the PR's declared design: noise, not false. Note 3 "red-proof not in facts" = UNMEASURED, allowed | 8/8 head and base = Claude 8 of 8 |
| 2094 (KS-2099 item 3, cell) | GO, 4 Notes | GWN, 1 Low (E8 asserts a domain substring only, title overstates, local part uncaught) | no (one grade lenient) | 1/1 at Note level: Note 2 says E8 checks the domain substring only; it did NOT say the title overstates or that a local-part leak passes | all 4 true, none false | 10/10 = Claude 10 of 10 |
| 2095 (KS-2012, cell) | GO, 5 Notes | GO, N-1 Low flake, N-2 Note 201 only | yes | 1/2: flake Note 4; not the "201 only" note | Note 5 ("RED label misleading") restates the PR body; the rest true | 8/8 = Claude 8 cells |
| 2096 (KS-2016, cell) | GO, 3 Notes | GO, N-1 Low (lower-case header key gives a false red), N-2 Note (3 pages, Bearer only, upstream refusal unread) | yes | 1/2: N-2 recalled twice (Notes 1,2); N-1 not found | Note 3 ("only checks mocked fetch calls, does not prove the route sends it") is overstated: the route is real (http.get to the server), only fetch is mocked, and Claude's six mutants all went red. Notes 1,2 true. One note text is garbled ("form...header)Skip") | 13/13 = Claude 13 cells |
| 2097 (KS-2077, docs) | GWN, 3 Notes | GO | no (one grade strict) | n/a (Claude's only observations are the same two: singular /api/referral and /api/pool not mounted, item 2 not done, all disclosed) | all 3 true, none a defect (the Notes restate "item 2 left open", "source read only", singular/plural, which the PR body says). Spark could NOT check the one thing that matters (is the new row true of proxy.ts): proxy.ts was not in its prompt | no run exists (docs); hand-built facts |
| 2098 (KS-2022 r2, comments) | GWN, 6 Notes | GO, 2098-1 INFO duplicate sentence, dated-figures claim | no (one grade strict) | 1/2: dated claim (Note 5) recalled; duplicate sentence not | all six Notes are "claim not in facts.json" (UNMEASURED, per the amended checklist); true; none a defect. The central fact (zero non-comment lines changed in 4 files) was NOT established by the Spark: it asked for it (Note 4) and Claude proved it three ways | 31/31 targeted = Claude (suite 1736/1736 not run by the Spark) |
Totals: verdict exact 3/6, adjacent 3/6, NO GO 0/6, Major 0 raised (0 false Majors, 0 missed Majors: Claude's worst finding was Low). Findings recalled 5 of 8 distinct Claude findings (counting Notes). False findings at source: 1 overstated Note (2096 Note 3), 0 false Majors, plus 1 garbled string. Failure mode seen: the Spark converts "unmeasured" into Notes (benign under the amended checklist) and cannot do the decisive reading when the file is outside its prompt (2097 row truth, 2098 zero-code-change). It never found the mutant-found blind spots Claude measured (2094 local part, 2096 lower-case key): those need planted mutants, which the runner does not do. Tier 2 comment/test/doc PRs: the Spark shadow agrees with Claude on "no blocker" 6/6. This is a calibration; it does not by itself promote tier 2.

## Round log (done.md row times, 2026-11-09)
02:15:16 PASS ks_2107_o106_p1 (83 s, model 70.5 s) | 02:16:36 PASS ks_2107_o106_p2 (80 s, 63.7 s) | 02:17:13 PASS ks_2109_o106_p1 (36 s, 25.8 s) | 02:17:30 PASS ks_2117_o106_p1b (16 s, 6.5 s) | 02:17:50 PASS ks_2117_o106_p2 (19 s, 8.5 s) | 02:18:14 PASS ks_2120_o106_p1 (22 s, 12.7 s) | 02:19:17 PASS ks_2121_o106_p1 (63 s, 29.3 s, test_only_input) | 02:20:34 CONTROL-PASS ks_2123_o106_p1 (76 s) | 02:22:39 PASS ks_2123_o106_p1 (87 s, 18.8 s).
Direct controls (not in done.md; verdict lines in ctl_*.out): all CONTROL-PASS, golden BYTE-IDENTICAL, except ks_2117_o106_p1 (first draft) CONTROL-FAIL A1/A2a/A5 (fence lines in diff context), and ks_2120 first attempt HARNESS VOID (develop moved mid-prep; rerun passed).
Preparatory: build_deps.sh run once (deps store was at abd044f6, lock key stale vs 01b26bc7; 40 npm ci rc 0).

## Tickets listed for a Claude seat (not briefed), with the reason
KS-2105 (concurrency, PR 2076 file) · KS-2106 (measurement run) · KS-2108 (item 4 trivial, no tier fits; items 1-3 behaviour) · KS-2111, 2119, 2122, 2126 (security surfaces) · KS-2112, 2114, 2118 (decisions/behaviour) · KS-2113 (browser/HTML) · KS-2115, 2116 (PR 2073 files) · KS-2124 (PR 2066 open) · KS-2125 (JSON baseline 2 numbers: users.ts 11->9, oauth.ts 2->1, recount at edit time).

## UNMEASURED
- No model-pass hunk was read by me beyond the checker/hold legs: the goldens are mine (the model output is TREE-IDENTICAL to them); Wednesday reads the goldens. Prose accuracy of the new comment/doc text is not machine-checked (doc_only does not prove it).
- None of the 8 READYs was tier-gated; the KS-2107 claim (repeat admitted event builds its own transaction) rests on Seat AA 5th's probe quoted in the ticket, not re-run.
- The 8 held patches were applied by the checker at c0e6e744; develop is now 5302a802 (not re-checked; 105 saw the same drift). Raise seats re-run the strict check.
- Plants for KS-2121/2123 are mine; KS-2123's plant is my reading of the gate's two variants (gate 246 files not read).
- Disk: 15.85 GiB free at 02:32 (under the 18 STOP), cause not measured (other seats active; load1 15.9). My own footprint: 8 un-pruned control work dirs in spark/cache/work (`ls | grep o106`, ~0.36 GiB each, ~2.9 GiB) because prune_work.py refuses dirs without a done.md verdict row; I did not delete (rule). Wednesday may prune them or run each as a queue `--control` line first. Load1 was above 8 for part of the queue run (9.4 at 02:16, 15.9 at 02:32): I did not wait on it because the rounds were model-bound and brief.
- Scratch (boot volume, not DevMASTER): clone and worktrees at /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02f26010-3405-430b-9101-389a22dcbb3d/scratchpad/j2 (repo, work*, nm_* farms, shared_src). Left in place.
- Not checked: the Claude verdict facts for suites (2592/2593/2594, 1736, 1869/1870) because the Spark runner runs targeted files only.

## Limits record
Pins: tip_start.out 01b26bc7 · tip_r1/r2 01b26bc7 · tip_r3 c0e6e744 · tip_end.out 5302a802. Open-PR scans (planted control services/originate: 9 entries every time): start 46 PRs / 277 files, end 44 PRs / 271 files; my product/test files hit 0 open PRs at start, before the rounds (prs_r1) and at end (the only hits are unrelated files: `ks1171-...` test in PR 2081 for the "anchoring/src/__tests__" probe, lockfiles for services/transfer). No push, PR, ticket write, comment or mail; Linear read-only (key sourced transiently); nothing written under !CODING; nothing deleted (moves: gen_documents.err and the first README brief dir). queue.sh drained and exited; queue.md holds only comment lines; nothing running at the end.
