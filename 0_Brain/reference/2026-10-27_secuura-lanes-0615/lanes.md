# Secuura Platform K lane sweep - 2026-10-27 ~06:15 AEDT (drafter, read-only)

Nothing was written to any board, repo, mail or pane. Only this file was written. The API key was used from the env and never printed.

## BLUF

- **Board: 705 open KS issues** (paginated, 29 pages of 25, hasNextPage=false; 705 unique ids). By type: **backlog 350 + unstarted 25 + started 330 = 705** (positive control: sums match). By name: **Backlog 350, Todo 25, In Progress 288, In Review 39, Blocked 3 = 705**. Baseline 2026-10-12 15:0x was 509 (Backlog 240, Todo 29, In Progress 222, In Review 13, Blocked 5): **+196 open since**, so "most of the board cleared by Sat 31 Oct" is a 705-issue board, not 509. Backlog+Todo (375) minus Peter/Stuart (17) = **358 lane candidates**.
- **Triage of the 23 tickets: 17 DONE-READY (10 clean + 7 with an unfiled post-merge gate note that is outside the ticket's own ask), 5 RESIDUE, 1 already Done** (KS-1636, state Done, merged #1707). Every attachment PR on the 22 open ones is merged into develop `ec3313a80440` (verified in git history). None of the 23 is assigned to Peter or Stuart (all are the board account, or unassigned).
- **Develop read: `ec3313a80440d0eee9fd07204c024518417ff9d7`** (ls-remote after `git fetch origin develop` in Wednesday's clone; equals the expected tip). It is the KS-1331 squash.
- **Spark-strict pool: 0 again.** 358 candidates, four clauses, automated first-fail cascade plus hand reads of every survivor (details in section 4).
- **Claude lanes: 5 core, pairwise disjoint by path, plus 2 spare** (section 3). All are Sonnet C2 rows of model-routing v1.0; none touches a file reserved by a live seat (Seat D 34th is deploying, no code edits).
  1. Shell guard/runner cells: KS-1745, KS-1738 (cond.), KS-1465
  2. Preflight leg 14 and pre-push base suites: KS-1643, KS-1563
  3. services/security test-hook budgets: KS-1734
  4. Published-spec generator seat: KS-1700, KS-1531, KS-1705 (cond.)
  5. Test-type ratchet checker: KS-1523
  - spare 6: packages/shared test pins KS-1589, KS-1463 (cond.); spare 7: comment truth KS-1505, KS-1667 (cond.)
- **Open-PR overlap: gh is NOT usable.** `gh auth status` = not logged in; the unauthenticated public API returns HTTP 404 for the repo's pulls (private repo). I used **Linear attachments + git history of develop** instead (section 5). A truly open PR that has no Linear attachment, or an attachment on a ticket I did not read, is UNMEASURED.

---

## 1. Paginated count

**FOUND** 705 open. Backlog 350 / Todo 25 / In Progress 288 / In Review 39 / Blocked 3. Assignee: board account 478, unassigned 208, Peter 11, Stuart 8. Backlog+Todo split: Backlog (unassigned 132, board 204, Peter 10, Stuart 4); Todo (board 22, Stuart 3).
**TESTED** Positive control: type counts (350+25+330) and name counts (350+25+288+39+3) both sum to 705; 705 identifiers, 705 unique.
**HOW** Linear GraphQL, `issues(first:25, after:$after, filter:{team KS, state.type in backlog/unstarted/started})`, cursor loop until `hasNextPage=false` (29 pages). Page size 25 because each node carries `comments(first:50)` and `attachments(first:25)`; full descriptions and comments of all 705 are in the scratchpad `open.json`.
**NOT READ** Closed/Done/Canceled issues (except KS-1636 and KS-1736, fetched by number). Comments beyond the first 50 on any issue (none of the 23 triage tickets has more than 5).

## 2. Triage of the 23 tickets

Definitions: **DONE-READY** = the ticket's own ask is fully covered by merged PR(s). **(+note)** = ask covered, but a post-merge gate note names residue the ticket did not ask for and that I found no ticket for. **RESIDUE** = part of the ask is open.
Merge proof for every PR below: `git log ec3313a80440 --grep "(#N)"` matched a squash commit for each of 1711, 1714, 1710, 1709, 1708, 1706, 1705, 1703, 1704, 1701, 1689, 1697, 1695, 1692, 1699, 1698, 1693, 1715, 1713, 1718, 1717, 1719, 1712, 1716. States are all "In Progress" on the board (the board rule: Done waits for deploy/verify).

| Ticket | PR (merged) | Verdict | Quote / what is open |
|---|---|---|---|
| KS-1735 | #1711 | **DONE-READY** | Ask: "its `generated_guard_restore()` has the two defects the two inline copies already had fixed. The restore copy is unchecked, and the stash is then deleted". #1711: restore `cp` checked, stash kept on both failure paths; 15-cell suite 10/5 red on old guard. Its LOW (chained trap loses the suite's status) is already filed as KS-1738. |
| KS-1729 | #1714 | **DONE-READY** | Ask: "first vitest run ... skips 110 cells ... three files cold-import the routers inside their first beforeAll". #1714 gives each of the 3 hooks a 120 s budget with the reason (constant present 2x in each file). Shape (i) was blocked by `module: commonjs` and is filed as KS-1737. Caveat: reproduction is 1 in 6 cold runs, so "green" is not provable by one run. |
| KS-1551 | #1710 | **DONE-READY** | Items (a) missing baseline = exit 2, (b) leg 16 comments, (c) `CLAUDE.md` wording are all in; gate GO, no Major/Minor. |
| KS-1554 | #1709 | **DONE-READY** | Three boxes: fix the two errors, enrol `services/security` in leg 16 + `check:test-types`, leg-16 cells cover it. All in (m365-integration enrolled too). The "6 errors" count was never reproduced by anyone; not a residue. |
| KS-1566 | #1704 | **DONE-READY** | Ask: "Add `expect(MAX_EVIDENCE_LOOKUPS).toBe(8)` ... Re-run mutant G6; it must go red." #1704 adds that cell, G6 red. (No merge comment on the ticket; merge confirmed from git: `b1afcb9bc`.) |
| KS-1527 | #1697 | **DONE-READY** | Checklist is exactly (a) pin rc-1 wording, (b) stub logs whole argv. Squash title: "KS-1527 items a and b". Minors 2/3 "accepted as written". |
| KS-1443 | #1715 | **DONE-READY** | Items 1 (lsof prefilter -> PIDs the run started) and 2 (pg_isready hiding) fixed; gate GO nothing above INFO; Linux proved in a `node:24-bookworm` container. INFO only. |
| KS-1726 | #1713 | **DONE-READY** | Five comments (bicep x3, compose, env doc) corrected plus the sixth `@description`; gate GO. Only INFO ("comment-only" is prose, not code, for the .md). |
| KS-1324 | #1718 | **DONE-READY** | Ask: "assert from the verdict, not the clock". Cell now asserts the child is alive when the runner returns; `T1303_ELAPSED` gone. LOW carried by the gate (pass path still needs the runner to return inside 15 s) is declared, not hidden. |
| KS-1331 | #1719 | **DONE-READY** | Ask: forward the signal to the suite's process group. Merged `ec3313a80440` with the round-2 guard cell. Its three LOW residues are already filed as **KS-1745**. |
| KS-1714 | #1706 | **DONE-READY (+note)** | Ask met (both suites exit non-zero after a failed restore). Unfiled gate notes N-1 "no committed test holds the new failed-restore exit code" and N-2 "`snapshot_ok != 1` branch still just `return`s". |
| KS-1578 | #1705 | **DONE-READY (+note)** | Ask met (two near-miss cells). Gate: "suffix variants of the filter survive all 20 cells" (`endsWith` mutants), at `services/security/src/index.ts:1486`. Unfiled. |
| KS-1713 | #1701 | **DONE-READY (+note)** | Ask met (mutant M3 red). Gate: a header-existence-only guard is still credited (mutant G6), and the `/api/nft` entry is unpinned (mutant M6). Unfiled. |
| KS-1716 | #1689 | **DONE-READY (+note)** | Ask `check-package-format.sh:730` fixed. Gate: `:874` is the same early-exit `printf | grep -qxF` and mislabels "(NOT in this push — inherited red)". Unfiled. |
| KS-1438 | #1717 | **DONE-READY (+note)** | Ask met (guard resolves both sides; symlink arm). Gate: always-true-guard mutants M2/M4/M5 survive; becomes live once something imports the module. Unfiled. |
| KS-1513 | #1695 | **DONE-READY (+note)** | Closing step done (SKIP line, rc 0, 23/0). Gate M-3 suggestion: the last line "does not say that the real-checker cells were not run". Unfiled, optional. |
| KS-1602 | #1703 | **DONE-READY (+note)** | Title ask (hook lapse skips 21 cells + misleading `close` TypeError) covered by `HOOK_BUDGET_MS = 60_000` and `if (!server) return;`. The description also names two other faces (the `:521` repo-walk cell at a 5 s default and the `:597` ECONNRESET cell, now `:530-559` and `:605-606`); the gate says both are untouched. If Wednesday reads those as ask, this is RESIDUE. I call it DONE-READY (+note) because the fix shapes the ticket lists (1, 2) were taken and shape 3 is optional. |
| **KS-1524** | #1699 | **RESIDUE** | PR is "item b" only. Open: "(a) Guard the log call ... `routes/platform.ts:995` is unguarded" ; "(c) A cell that throws `null`"; "(d) Cap the line length, or decide not to"; "(e) Measure the limiter key on the deployed ingress ... after the deploy". (d) is decision-shaped, (e) needs a deploy. |
| **KS-1548** | #1698 | **RESIDUE** | PR is "item m2" only. Open: "m1, a stalled response BODY is outside every timer ... bound the body read by the remaining budget"; "m3 a final window that answers AFTER the deadline keeps the platform half" (a "ruling-interpretation question as well as a fix"); the nit "cell G's second assertion cannot fail". |
| **KS-1560** | #1692 | **RESIDUE** | PR is "item M1" only; ticket stays open per its own comment. Open: M2 `ks1347_proxy_out_dir_spaced_checkout.test.sh` import grep "reds 4 cells while server.ts still works" (fix: tolerate both quote styles / parse the import list). Plus gate note: census `grep -qF 'bin/jq'` is satisfied by a comment (mutant B). M3 is "information, not work". |
| **KS-1391** | #1693 | **RESIDUE** | PR is "item 1" (issuer `test` script). Open: item 2 "Decide for the other five whether a unit tier is wanted at all" (Kam-shaped), item 3 `--if-present` / note, item 4 rename `frontend/admin/src/__mocks__/`; Acceptance "The intended unit-test posture for the other frontends is stated in the repo". |
| **KS-1728** | #1708 | **RESIDUE (ruled: stays open)** | Title says 150 lines in 29 files; #1708 is "the four observed lines only". |
| KS-1636 | #1707 | **Already Done** | Linear state Done. Not in the open set. |

Counts: DONE-READY **17** (clean 10: 1735, 1729, 1551, 1554, 1566, 1527, 1443, 1726, 1324, 1331; +note 7: 1714, 1578, 1713, 1716, 1438, 1513, 1602); RESIDUE **5** (1524, 1548, 1560, 1391, 1728); already Done 1.
Peter/Stuart check: assignees of all 22 open tickets are `kamil.kreiser@secuura.ai` or unassigned. **None is Peter's or Stuart's**, so no "stays theirs" flags.
Note: the unfiled "+note" items (1714 N-1/N-2, 1578, 1713, 1716, 1438, 1513) are ~6 small candidate tickets for Wednesday to file or discard; I did not file anything.

**TESTED** Each PR number resolved to a develop squash commit; every comment sorted client-side by `createdAt`; checklist boxes in descriptions compared to PR titles/bodies in the merge comments.
**HOW** Linear descriptions, `comments(first:50)` and attachments from `open.json`; `git -C <clone> log ec3313a80440 --grep "(#N)"`.
**NOT READ** PR diffs (no gh). I relied on the ticket authors' merge comments for "files = the PR's own" and on squash-commit titles. The gate verdict files under `0_Brain/reference/2026-10-26_gate-*` were not opened. Description text past ~2,000 characters was read only for the tickets I classified RESIDUE or flagged.

---

## 3. Lane sweep (Claude seats)

Routing for every lane: **model-routing.md v1.0 row C2** ("Multi-file build or feature that fails the local predicate, not decision-shaped, not auth-design and not a destroying path": 1st = Sonnet 5.5, gate Opus tier 1/2 per the G rows, esc = C1 counter). Gate rows G1+ were not re-read (I read the file through row C10). P1-P4 checks: none of these is production/money/external-comms; P4 applies only to the Spark.
Disjointness: each lane owns the path set below; no path appears in two lanes (checked by writing the sets side by side). Order inside a lane is easy to hard.

### Lane 1 - shell guard and runner cells (Sonnet, C2)  Order: KS-1745, KS-1465, KS-1738
| id | what | files / lines at `ec3313a80440` | test target | size |
|---|---|---|---|---|
| KS-1745 | 3 LOW residues of the merged #1719: no cell for the empty-pgid branch (mutants M3/M4 survive 70/0); a TERM-ignoring suite; two precision gaps in the KS 1330 comment. Gate approach given: PATH-shadowed `ps` stub that prints nothing, against a fixture copy of the runner. | `Blockchain/Dev/scripts/run-shell-suites.sh` (guard `:319-321`, pgid read `:400`, reset `:404`; comment edit only) ; `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` | that suite (70 cells), mutant M3/M4 must go red | S-M |
| KS-1465 | run-schemathesis test leaks one temp dir per run; wrapper header does not document the default. | `Blockchain/Testing/ci/tools/run-schemathesis.sh` (header `:15-16`, default at `:26`) ; `Blockchain/Dev/scripts/__tests__/ks1405_run_schemathesis_default_findings_dir.test.sh` (`WORK` `:19`, EXIT trap `:20` removes only `$WORK`, default case `:47`) | that suite, count `run-schemathesis.XXXXXX` dirs under a private `TMPDIR` before/after | S |
| KS-1738 | `generated_guard_restore` reads `local rc=$?` (`generated_guard.sh:37`) but `bootstrap_login_diagnosis.test.sh:55` chains `trap 'stop_stub; generated_guard_restore' EXIT`, so the suite's own status is flattened to 1 (measured table A/B/C in ticket). | `systemTest/__tests__/support/generated_guard.sh` ; `systemTest/__tests__/bootstrap_login_diagnosis.test.sh` (`:55`) ; `systemTest/__tests__/generated_guard_restore.test.sh` | new/extended cell asserting a chained trap preserves status 3 under a fake failing `cp` | S-M. **Conditional:** ticket lists three shapes, none chosen; shape 3 is "Leave it". Builder picks 1 or 2; if Wednesday reads "leave it" as a live option, drop it. |

Why disjoint: no file is shared with Lanes 2-5; the runner is *called* by `preflight.sh` (Lane 2) but Lane 2 does not edit it. It does not share a file with any merged-or-attached PR I could see (all merged). `Blockchain/Testing/ci/tools/` and `systemTest/` are touched by no other lane.
**FOUND** line numbers above (drifted from the tickets: trap is `:55`, not `:52`).
**TESTED** `git show`/`git grep` at the sha: pgid guard text, `local rc=$?`, trap line, `mktemp`/trap lines in the ks1405 test, FINDINGS_DIR lines in the wrapper. Nothing executed.
**NOT READ** KS-1465's fix-shape paragraph (I read item 1 and the file lines); `run_shell_suites.test.sh` body.

### Lane 2 - preflight leg 14 and pre-push base suites (Sonnet, C2)  Order: KS-1563, KS-1643
| id | what | files / lines | test target | size |
|---|---|---|---|---|
| KS-1563 | Three Minors from the #1530 gate, all in test files: a comment promises a restore nothing performs; "the only pinned tally in this directory" is false; CASE 12 asserts only the first `REFUSED` line. | `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` (comment `:697-700`, CASE 12 `:687-719`) ; `.../pre_push_hook_base_fixture_guard.test.sh` (`:126-130`) | both suites; CASE 12 gets the path-line assertion | S |
| KS-1643 | Gate S1 residue on #1606: Minor 1 the refusal message prints while the suites run (guard sits after the `fi`); Minor 2 no cell proves the stripping (mutant M3 survives 61/61; the cell named `SHORT-CIRCUITS` passes while suites run); 4 nits. | `Blockchain/Dev/scripts/preflight/preflight.sh` (refusal block just above the `env "${env_clear[@]}" bash scripts/run-shell-suites.sh` call, ~`:722-732`) ; `Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh` (`:492`, `:509`, `:518`) | `preflight_deps.test.sh` (61 cells at ticket time), M3 must go red | M |

Why disjoint: Lane 2 owns `preflight.sh`, `preflight_deps.test.sh`, `pre_push_hook_base*.test.sh`; Lane 1 owns `run-shell-suites.sh` and its own test. KS-1643's ticket path `scripts/preflight.sh` is wrong at this tip: the file is `scripts/preflight/preflight.sh`.
**FOUND/TESTED** the `preflight.sh` block shows the `fail=1` message inside an `if` and the suite call after the `fi` (Minor 1 still true at the tip); `SOMETHING_ELSE`, `SHORT-CIRCUITS` lines found at `:509`, `:492`, `:518`.
**NOT READ** the KS-1643 nits' detail beyond the first 3,700 characters; whether KS-1483 (the pre-push-on-unchecked-out-branch bug, Backlog) wants `preflight.sh` too (it is in the Spark/Claude "not selected" pile; if a seat takes it, merge it into Lane 2).

### Lane 3 - services/security test-hook budgets (Sonnet, C2)  Single ticket
| id | what | files | test target | size |
|---|---|---|---|---|
| KS-1734 | First whole-suite run after `npm ci`: 11 of 33 files failed, 10 s hook lapsed in ten files, a 5 s test in an eleventh (`ks578-ks643-revoke-authorization.test.ts:70`). Two shapes, none chosen: per-file budgets (as #1703 did for ks742) or one `hookTimeout`/`testTimeout` in the service vitest config. | `Blockchain/Dev/services/security/vitest.config.ts` (**no `hookTimeout`/`testTimeout` set**: verified; the sibling `vitest.integration.config.ts:16-17` sets 60_000) and/or the ten named `src/__tests__/ks*.test.ts` files (37 `ks*test.ts` files exist) | `npx vitest run` in services/security; a cold-run proof needs a fresh `npm ci` (state in brief). Wednesday ruled it one ticket. | S (config) to M (ten files) |

Why disjoint: only `services/security/vitest.config.ts` and its unit tests; Lane 4's `security.openapi.ts` is a different file. `ks742` is not touched (already merged).
**Conditional** on Wednesday accepting a builder choice between the two shapes (neither is a Kam decision; the ticket says "none chosen, none measured").
**NOT READ** the table of the ten files in full (I read the header and tail); whether security `src/index.ts` is held by an open PR (UNMEASURED).

### Lane 4 - published-spec generator seat (Sonnet, C2; one seat because `docs/openapi/secuura-api.yaml` is generated and shared)  Order: KS-1700, KS-1531, KS-1705
| id | what | files / lines | test target | size |
|---|---|---|---|---|
| KS-1700 | `M365Connection.status` enum lists `expired`/`revoked`, which nothing assigns, and omits `error`/`disconnected`, which the service assigns. | `Blockchain/Dev/services/m365-integration/src/m365-integration.openapi.ts:112` (the other enum at `:89` already matches); stored type `index.ts:94`; then regenerate `docs/openapi/secuura-api.yaml` | `npm run generate-openapi` + preflight leg 1 (spec vs Zod); the ticket states "facts only; nothing built", so the exact enum is the builder's reading of `index.ts:94` | S |
| KS-1531 | Document `GET /api/connector/info` (new operation, 200 schema, 401/403). Confirmed absent: no match for `connector/info` in the yaml or `api-gateway.openapi.ts` at the tip. | `Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts` ; yaml ; spec-route-map test ; route at `services/api-gateway/src/services/health.ts:39` | generate + preflight leg 1 | M |
| KS-1705 | Three operations (`POST /api/security/keys`, `PUT /api/security/keys/admin-scopes/{userId}`, `POST /api/timestamps/verify`) need `requestBody.required: true`; `POST /api/security/keys` also needs its real body properties. | `Blockchain/Dev/services/security/src/security.openapi.ts:788,816,889,912` ; the timestamping openapi ; yaml | offline spec checks. **Conditional:** its acceptance 3 is a Schemathesis sweep on a running slot, which an agent seat may not have; and KS-1364 "closes this as covered" if its blanket fix lands first. | M |

Why disjoint: this lane owns the three `*.openapi.ts` files named and the generated yaml; no other lane edits a spec or the yaml. It deliberately does not touch api-gateway `index.ts`.
**Excluded from this lane:** KS-1514 item 1 ("Decision needed: which side is the contract") and KS-1322 ("a ruling is recorded: keep, or strip") are Kam-shaped.
**FOUND/TESTED** `m365-integration.openapi.ts:112` and `:89`, yaml still contains `expired` at 5 places (not all M365; I did not map them), `connector/info` absent, the four `security.openapi.ts` path lines.
**NOT READ** the generator (`scripts/generate-openapi.ts`) beyond its output path; whether the yaml has a drift check that rejects a hand edit (assume yes: regenerate, never hand-edit).

### Lane 5 - test-type ratchet checker (Sonnet, C2)  Single ticket
| id | what | files | test target | size |
|---|---|---|---|---|
| KS-1523 | Residue from the #1506 gate: (a) no killing cells for `withoutRoots` (lookahead, `g` flag, regex escaping: mutants R6/R8/R9/W1 survive 29/29); (c) header and `CLAUDE.md` list the wrong codes that print absolute paths; (d)/(e) recorded floors sit below current counts (auth 93 vs 105, api-gateway 111 vs 122, vc-issuer 17 vs 19; security and m365 are at 0 slack). Item (b) "decide whether to widen the lookahead or document it" is the builder's call, not Kam's. | `Blockchain/Dev/scripts/typecheck-tests/check.cjs` (`withoutRoots` `:254`) ; `services/auth/src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts` ; `Blockchain/Dev/CLAUDE.md` (wording near `:398-403`) ; the per-service `baseline-*.txt` floors | ks1000 suite (70 cells after #1710), leg 16 | M |

Why disjoint: owns `check.cjs`, the ks1000 test, the baselines and the CLAUDE.md lines; no other lane touches them. **Caution:** #1710 and #1709 (both merged) edited the same files; start from the tip, not from the ticket's line numbers.
**NOT READ** KS-1523 items (d)/(e) detail past the evidence table; whether raising floors is a ruled policy (the table says "under-protects" but the ticket is the filer's, not a ruling) - put the floor change to Wednesday before the seat edits baselines.

### Spare lane 6 - packages/shared test pins (Sonnet, C2)
- **KS-1589**: the ks1564 source guard is satisfied wrongly by five surviving mutants (parenthesised argument, an alias, a commented-out guard). File `Blockchain/Dev/packages/shared/src/__tests__/ks1564-admin-api-keys-page-sends-no-default-org.test.ts` (`fetchApiKeysArgs` `:93`, `racesAreGuarded` `:114`). Test-only. Description wording items (A.x) were read at the top only.
- **KS-1463** (conditional): move `ks781-p3-3-body-parser-order.test.ts` out of `packages/shared` (needs `cors` from demo-service). Ticket: "Suggested shapes (not prescribed)". Do not declare `cors` in shared (it would ship in 25 images).
- Disjoint from all lanes (two different test files in packages/shared). Not in the core 5 only because the lane count target is 3-5.

### Spare lane 7 - comment truth (Sonnet, S)
- **KS-1505**: api-gateway `Blockchain/Dev/services/api-gateway/src/index.ts` hot-reload comment block `:614-643` still says replacement "fires neither watch ... reads ENOENT". Free now: the KS-1635 PR (#1702) that held `index.ts` is merged. Part 2 ("if it is cheap" hash compare) is optional and has no test nearby; recommend the comment fix only.
- **KS-1667** (conditional): originate `routes/documents.ts` comment at `~:1957-1959` ("originate's only call sites are in routes/adminConfig.ts" - ticket says `gdprService.ts` also calls it, 5 call sites) plus the `ks1662-tenant-predicate-without-rls.integration.test.ts` header. The previous sweep's PR-overlap worry (#1654/#1680) is cleared (both merged by 10-23). Still conditional on no open PR editing `documents.ts` (UNMEASURED). Note: the ticket's file name for the header is `ks1662-...`; at the tip it is `ks1662-tenant-predicate-without-rls.integration.test.ts`.

### Carried, NOT re-verified: Opus lane
- **KS-1727** `packages/shared` wallet-signature test (CIP-8 verifier) from the 10-26 sweep: crypto surface, row C3 (Opus). I did not re-read it today. Keep it out of the Sonnet lanes.

### Excluded (with reason; counts are from the automated pass in section 4)
- **Peter/Stuart: 17 Backlog/Todo tickets (Peter 10 backlog; Stuart 4 backlog + 3 todo)**, e.g. KS-1741, 1711, 1609, 1446. Stay theirs. KS-1712 (TZ test) was reported by Peter and needs Postgres with the cause unestablished.
- **Decision-shaped (needs Kam), examples read:** KS-1322 (keep or strip ticket keys in the spec), KS-1514 item 1 (which side is the contract), KS-1535 (POLICY), KS-1625 (Node floor), KS-1562 (QUESTION), KS-1522 (decide production VC verification), KS-1646 (fix shapes "the decision is not mine"), KS-1737 (compile target belongs to the service's owner), KS-1738 shape 3. Automated hit count for decision wording: 163 of 358.
- **Production / money / external-comms:** KS-1730 and KS-1665 and KS-1083 (Azure secret provisioning, deploy order), KS-1079 (kintsugi demo flag), KS-1413/1608 (credential banners/reports), KS-1606 (`Setup and System/statusline.sh`, outside the project folder; hard rule 1).
- **Security/auth surface:** the "Security:" titles (KS-1703, 1704, 1696, 1699, 1688, ...) and auth-service tickets (KS-1690, 1691, ...). Not Spark-eligible; if built at all, Opus (row C3), not Sonnet.
- **Todo (25):** KS-1393, 1392, 1390, 1382, 1372, 1076 and old review/plan tickets (772, 770, 735, 725, 716, 696, 683, 598, 583, 582, 581, 580, 579, 576, 491, 485, 188, 135, 61). Titles read only. KS-1382 (Testing entry points default `TARGET_BASE` to slot 1) is a plausible Sonnet candidate I did not read; KS-1372 is security.

---

## 4. Spark-strict pool: 0 (WHY, with counts)

Predicate (rule 2 of `2026-09-23_spark-kit-running-a-local-coding-model.md`): one product file; the ticket spells out the fix shape (anything "decide whether" is a human card); a runnable in-process test nearby to copy; not auth/token/credential/security; not at the round counter; a test runner the checker can run. Routing §3 adds: not frontend, no real Postgres / docker rebuild, <=3 edit points, Spark takes Secuura only with P4 satisfied (RULED 09-25).

**FOUND** Of **358** candidates, an automated first-fail cascade (clause order A, B, C, D) left **6 survivors**, and each survivor then failed on a hand read: **0 qualify.**

| Clause (in cascade order) | first-fail | any hit (not exclusive) |
|---|---|---|
| A no `services/<x>/src` or `packages/shared/src` path in the ticket (tooling, scripts, systemTest, infra, docs, process) | **207** | 207 |
| B fix shape not spelled out (facts only / none chosen / decide / QUESTION / POLICY / "whether to") | **82** | 163 |
| C needs Postgres/Redis/docker (not in-process) | **21** | 96 |
| D auth/security/tenant/key/money surface | **42** | 293 |
| survivors of all four | **6** | |

Survivor hand read (clause failed):
- KS-1505 - comment fix is prose (no line-by-line), part 2 is "if it is cheap", and no test touches the hot-reload block (only `index.ts` mentions it). Fails: fix not spelled, no nearby test. Near-miss.
- KS-1463 - "Suggested shapes (not prescribed)", two shapes, one is "move the test". Fails: fix not spelled.
- KS-1644 - needs the real `anchor_store` upsert statement (Postgres) and `index.ts` listens at import. Fails: not in-process.
- KS-1640 - "hard-code `anchored: true`" in chain-first verify blobs: behaviour change with a status vocabulary choice, 6 KB. Fails: not spelled, >3 edit points.
- KS-1431 - "waits on KS-1427's ruling". Fails: ruling.
- KS-1290 - lockfile edits (tooling), 7 KB. Fails: A on a closer read (the cascade's A regex missed it).
Additional hand-checked near-misses that the cascade rejected only on weak signals: **KS-1700** (one-line enum at `m365-integration.openapi.ts:112` but "facts only; nothing built" and the second edit is the *generated* yaml, which the checker cannot regenerate), **KS-1667** (comment-only, 3 sites, test is an integration test needing a DB), one-line tooling fixes like KS-1438 are already merged. The `doc_patch` rung (Ornith's night path) is not wired on the Spark (`brief_lint.py:18`, per routing §3), so comment-only tickets stay off the Spark.

**TESTED** No positive control was run for the cascade (no known Spark-qualifying ticket exists to feed it), so "0" is a suspect until Wednesday supplies one; the 6 survivors were each checked by hand. The cascade is an approximation: B and D match on words anywhere in a ticket, so "any hit" over-counts and the first-fail column depends on clause order.
**HOW** `spark3.py` over `open.json` (scratchpad); description text, first 1,500 characters for C and D, whole text for A and B; survivors read by hand at the clone.
**NOT READ** About 340 of the 358 candidate descriptions were not read by a human; I read titles of all 358 and full text of ~45. A ticket that the cascade rejected on a weak keyword (e.g. "token" in an unrelated sentence) is not individually cleared. If Wednesday wants a recount, the most likely misses are tickets of 700-2,000 characters in `services/*` that mention "tenant" or "scope" only in passing; KS-1593, KS-1588, KS-1587 are examples (all "facts only" or Postgres anyway).

## 5. Open-PR overlap

**Used:** Linear attachments (all 705 issues' `attachments`) plus develop's git history. **Not used:** `gh` (not logged in; the unauthenticated REST call to the repo's pulls returned HTTP 404 because the repo is private). `git ls-remote origin 'refs/pull/*/head'` showed the highest PR number is **#1724**; #1700-#1724 are all visible in develop history as squash or merge commits (#1720-#1724 are merge commits and docs).
**FOUND** Every PR attached to the 23 triage tickets is merged. PRs numbered 1640-1683 attached to other tickets (e.g. #1654, #1680, #1655) have no `(#N)` squash subject but their ticket keys appear in develop commits dated 2026-10-20 to 10-23 (checked KS-1673, 1660, 1500, 1676, 1557, 1407, 1157, 1659, 1558, 1677, 1687, 758, 1682, 1692, 1116, 1679, 1689, 1706, 1508, 1707, 1709, 1622): they landed as merge-style commits. So I found **no open PR reserving a file**.
**NOT READ / UNMEASURED** A currently open PR with no Linear attachment, or an attachment on an unchecked ticket (I did not key-check all ~190 attachment PRs). Closed-unmerged PRs would look identical to open ones here. Before launching any lane, Wednesday (who has `gh`) should list open PRs and intersect with the path sets in section 3; the likeliest collisions are the shell/preflight lanes with whatever seat is deploying, and Lane 4 with any seat editing `*.openapi.ts`.

## 6. What was read and not read

- Read in full: previous sweep, Spark predicate rule 2, model-routing.md through §4b/C10, descriptions and all comments of the 23 triage tickets (the longest read at 1,800-5,000 characters, tails read for the residue ones), KS-1700, KS-1505, KS-1463, KS-1644, KS-1667, KS-1738, KS-1734, KS-1643, KS-1646, KS-1563, KS-1523, KS-1322, KS-1514, KS-1705, KS-1531 (all at least partially, noted per lane).
- Titles only: all 358 candidates. Full text: about 45.
- Source: only the lines named in section 3, at `ec3313a80440`. Nothing was executed (no test, no build, no `npm`).
- Not read: model-routing G rows, `HANDOFF`/`SPARK_LADDER.md`, the gate verdict folders, any PR diff, Linear history of state changes.
