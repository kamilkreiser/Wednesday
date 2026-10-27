# Secuura Platform K wave-3 lanes - 2026-10-27 ~15:45-16:00 AEDT (drafter, read-only)

Drafter: claude-sonnet-5-5, row C8 (Agent-tool drafter for Wednesday). Nothing was written to any board, repo, mail, pane or other project's files. Written: this report, five lane briefs (W, X, Y, Z, AA), the board brief G 24th, all under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/`, plus one superseded first draft of Y moved (not deleted) to `briefs_staged/_drafter_scratch_c8_1545/`. The Linear key was read from the environment file and never printed or copied. The only git verb that writes was `git fetch origin develop` in Wednesday's cache clone (permitted). No suite, build, mutant or script was run by me: every "open" or "done" below is a read of source at the sha (`git show`, `git grep`, `git ls-tree`), not an execution.

## BLUF

0. **UPDATE 16:00 AEDT: develop moved to `b6366c12a8abd0000931ca3ee787e41f804deaaf`** (KS-1753 #1740, committed 15:57:12 +1100; `git diff --name-only` against `362f95dd7` = `api-gateway.openapi.ts` and `secuura-api.yaml` only, no lane file; KS-1757 may now be built once the board seat has it assigned, but it is not queued). Everything below was read at `362f95dd7`.
1. **Develop read: `362f95dd71c1fdd6fb691647cb541f5adada4c42`** (`ls-remote origin refs/heads/develop` equals `rev-parse FETCH_HEAD`, fetched 15:46 AEDT and again 15:54 AEDT: unmoved between them; it is the KS-1738 squash #1741, committed 15:45:10 +1100). **The prompt's `3b48991cd` is one commit behind**: #1741 merged at 15:45, minutes before the fetch.
2. **Board: 691 open KS issues** (types backlog+unstarted+started, 691 unique ids of 691 nodes, 7 pages of 100, not capped; names Backlog 343, In Progress 278, In Review 42, Todo 25, Blocked 3). The actionable pool (Backlog + Todo + In Progress, my predicate) is **646**.
3. **Five lanes, 13 tickets, ~31 items**, all Sonnet C2, pairwise disjoint file families (checked programmatically from the owned-path sets: no overlap). Easy to hard inside each lane. Lane summary below.
4. **A finding that changes the plan: much of the "In Progress" gate-follow-up pool is already worked.** The fleet rule keeps a merged ticket In Progress until it is deployed, so In Progress does not mean open. Reading each item at the tip found: KS-1621 items 1 and 2 on develop (cells F5, D4); KS-1503's action on develop (cell M1); KS-1524 (b) on develop (L5); KS-1595 part 1 on develop (the `ks1595-gdpr-...` test exists); KS-1620 item 1 on develop (`8a093d1de`); KS-1155's `walkTimeouts` setup on develop. **Every lane item below states which of its items the drafter confirmed OPEN at the tip**, and every brief tells the seat to build only what is open and report the rest as DONE-READY evidence.
5. **DONE-READY candidates (for the board seat, G 24th item 6): KS-1750, KS-1738, KS-1667, KS-1159** (merged, all items, test or comment only), **KS-1621 after lane X**. KS-1525 was on my first list and came off it: its own comment records an open product question.
6. **G 24th findings:** finding 1 is already covered by **KS-1329** (comment, not a ticket; KS-892 is its Duplicate, KS-872 adjacent); finding 4's sibling is recorded only inside a KS-1750 comment (file a ticket before KS-1750 moves Done); findings 2, 3, 5 read as comment/new-ticket by their parents KS-1748, KS-1752, KS-1589. **KS-1757 and KS-1758 already exist** (the #1740 findings, created 04:48Z): do not file them again.
7. **Letters W, X, Y, Z, AA are NOT in `inbox_routing.conf`** (its Blockchain lanes are B, C, D, E, F, G, J, K, R, S, T, U, V and BOARD; my grep for `Blockchain-(W|X|Y|Z|AA)|` returned 0 for each). Wednesday adds five lines before launching. An earlier occupant of W exists (`2026-10-09_seatW_ks1385-first-anchor-identity_DRAFT.md`); the ordinals come from `history.md`, which I did not open: **unverified**.
8. **Open PRs are UNMEASURED** (no usable `gh` in Wednesday's shell): every brief's QUEUE 0 measures them under the project's identity and stops on any intersection. Linear attachments were not read for PR links beyond the ticket comments I quoted.

## 1. Counts (predicate, cap, controls)

**FOUND** 691 open KS issues now: `issues(first:100, after, filter:{team KS, state.type in [backlog, unstarted, started]})` cursor loop to `hasNextPage` false, 691 nodes, 691 unique. Created since the 11:15 report: KS-1752..KS-1758 exist (7), highest KS number KS-1758 at the 15:5x read.
**TESTED** Positive controls: state names sum to 691; the board search tokens that fire (`KS-1531` 4 hits, `fetchApiKeys` 4); zero control `zzqz-wed-ctl-4417` returned 0 (searched uncapped, includeArchived, title OR description OR any comment body); `api.fetchApiKeys` 0 and `member call` 0 (genuine zero, not a broken query: the same shape returned hits for `fetchApiKeys`). The earlier 06:15/11:15 zero token `zzqqxx-no-such-symbol-9931` is burned (7 hits at 11:2x) and the briefs say so.
**HOW** Linear GraphQL (`comments(first:50)` sorted client-side, never `last:N`); source read with `git show origin/develop:<path>` / `git grep` / `git ls-tree` in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_1719_r2_20261027`.
**NOT READ** The bodies of ~600 of the 646 pool tickets: I filtered titles by keyword (test, cell, gate, residue, nit, guard, ...) and read in full or in large part about 45 (KS-1155, 1159, 1329, 1484, 1491, 1493, 1503, 1505, 1524, 1525, 1529, 1548, 1558, 1560, 1568, 1583, 1587, 1593, 1595, 1605, 1611, 1613, 1614, 1620, 1621, 1622, 1634, 1637, 1642, 1667, 1671, 1676, 1712, 1720, 1721, 1728, 1737, 1745, 1746, 1750, 1752-1758). **The lanes are therefore the best-evidenced work I found, not the whole pool**; a deeper pass would find more (see section 6).

## 2. The lanes

All paths below were checked with `git cat-file -e 362f95dd71c1:<path>` (table at the end of this section; every path rc=0 except the one NEW file, which is rc=128 on purpose). Docs: the two `Projects Documents/` HTML docs are **append-only for every test change** and their **section number is set at MERGE time**; each brief grants them for appending and carries the escape clause for comment/doc-only PRs.

| lane | seat | brief | tickets (order) | file family | difficulty |
|---|---|---|---|---|---|
| 9 | W | `2026-10-27_seatW_lane9_auth_test_residue.md` | KS-1529 (a,b), KS-1484 (1,2; 3 optional) | `services/auth` tests + `userRepo.ts` | medium |
| 10 | X | `2026-10-27_seatX_lane10_gateway_comment_truth_and_pins.md` | KS-1621 (item 3), KS-1637 (N1,N2,N4,N5, Minor 1), KS-1493 (N1) | api-gateway `index.ts` comment, ks1543/ks1628 tests, a NEW ks1493 test, `deployment/azure/RUNBOOK.md`, `Blockchain/Testing/USER SIMULATED TEST/02-verifier.md` | medium; KS-1493 hardest |
| 11 | Y | `2026-10-27_seatY_lane11_originate_and_mcp_test_residue.md` | KS-1634 (residue), KS-1491 (1,2), KS-1620 (3 then 2) | originate ks1061/ks1634 tests, mcp-server ks1620 test + `info.ts` comment | easy |
| 12 | Z | `2026-10-27_seatZ_lane12_shell_residue_wave3.md` | KS-1756, KS-1560 (M2), KS-1558 (m2, m1) | `preflight_deps.test.sh`, ks1347 and ks1355 suites, `check-compose-stack-safety.mjs` | easy to medium |
| 13 | AA | `2026-10-27_seatAA_lane13_platform_route_deadline_and_log.md` | KS-1548 (m2 + nit, then m1), KS-1524 ((c) then (a)) | api-gateway `routes/platform.ts`, ks1510 and ks1512 tests | medium |

(Ticket order in each brief's BLUF equals the order in this table.)

### Lane 9 (W): auth tests
- **KS-1529** (Backlog, unassigned, 0 comments). Scope, quoted: "**(a) Widen the 'no cell compares a run as one array' guard (the gate's Minor 1).** The guard is `/expect\(\[[^\]]*\.status[^\]]*\.out/` applied **line by line**. ... an **object** shape ..., a **reversed** array ... and an array **split over several lines** all pass." Files: `services/auth/src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts` (rc=0; the old regex is still at `:919-920`: OPEN). No input: the ticket spells shapes and the bracket-bounded fix. Proof: planted shapes red on a copy of the guard, benign shape green, file and `services/auth` ratios.
- **KS-1484** (Backlog, unassigned, 0 comments). Scope: "One small PR on `userRepo.ts` and `ks1186-userrepo-fromrow-sites-are-awaited.test.ts`: 1. Rewrite the comment ... 2. Widen the controls ... 3. Decide `listUsersInner`, then fix or file it". Open at the tip: the stale comment (`userRepo.ts:372-373`, "unawaited: KS-1186") and the missing catch (`:1040`). Item 3 is a code change: the brief makes it last, optional and a QUESTION if the seat judges it needs a ruling. Proof: ks1186 ratios (12/12 per the gate), `services/auth` suite, comment-only token-stream compare.

### Lane 10 (X): api-gateway comment truth and pins
- **KS-1621 item 3** (In Progress, on our account, 0 comments): "**INFO (#1571): stale header** ... `ks1543-...test.ts` **lines 1-6.** It still says the catch uses `String(err)`". Open (header read at the tip). Items 1 and 2 are ON DEVELOP (cells F5, D4): the PR leaves the ticket complete.
- **KS-1637** (In Progress, our account, 1 comment by Peter): "**Gate N1's residue on #1589 ... the removal pin reads only the router, the quarantine README's O1 count was wrong, and three nits.**" Open at the tip (read): N1 header, N2 `RUNBOOK.md:263`, N4 `index.ts:417-418`, N5 `02-verifier.md:71`, Minor 1's app-level cell (not re-checked for a landed fix). N3 does not apply (Peter says so; KS-1635 removed it). No input: Peter's comment states the state of each item and that the fixes are assigned to our account.
- **KS-1493 N1** (Backlog, our account, 0 comments): "Moving the verification limiter **below** the audit middleware ... turns **0 cells** red" and the recommendation names the behavioural cell and the tamper. N2 is an owner decision and is held. A NEW test file (path checked absent). The brief tells the seat to stop and ask if the real app cannot be driven without editing `index.ts`.
- Edits `index.ts` (one comment at :417) and the ks1628 test: **api-gateway is shared at service level with lane 13 (AA owns `routes/platform.ts` and ks1510/ks1512); the two lanes share no file.** The in-flight #1740 edits `api-gateway.openapi.ts` and the yaml: not touched here.

### Lane 11 (Y): originate and mcp-server tests
- **KS-1634 residue** (In Progress, unassigned, 3 comments): from its own 2026-10-19T16:10 comment, "The fix is one assertion in each of the two tests, checking that the hash is real ... It belongs in the next change to that file." One file, `ks1634-v2-chain-only-match-carries-simulated.test.ts` (rc=0).
- **KS-1491 items 1, 2** (Backlog, unassigned, 0 comments): the two fixtures with named mutants (loosen `VIA_HELPER`; drop `/g` on `ROOT_MOCK`). A case-insensitive grep finds no such cell (control found the T6b cell): OPEN. Item 4 (widen blind spots?) is a decision: held.
- **KS-1620 items 3, 2** (In Progress, our account, 0 comments): item 1 is ON DEVELOP (`8a093d1de`); the H1-M3 and H1-M8 cells are absent (grep, control fired) and the `info.ts:129` comment still overclaims. **Wednesday-ruled in the brief:** keep the word "refused", correct the comment, pin it (a reversible comment/test shape; Wednesday may override).
- No shared file with any other lane.

### Lane 12 (Z): shell and stack-tooling residue
- **KS-1756** (Backlog, our account, 0 comments, created after the 11:15 sweep): "the `nocontrol` hook fixture mode ... does not model an empty derivation ... it derives `[NAME]` ... Test-truth only; LOW." File `preflight_deps.test.sh` only. The ticket chooses no shape; the brief carries Wednesday's lean (make it truly empty so the `-z` disjunct gets a cell) and leaves the choice with the seat. `preflight.sh` read-only.
- **KS-1560 M2** (In Progress, unassigned, 1 comment): "the KS-1347 probe is brittle to a harmless respelling ... **reds 4** **cells while** `server.ts` **still works perfectly**"; the line-shape grep is still at `ks1347_...test.sh:53`: OPEN. M1 landed (#1692), M3 is information.
- **KS-1558 m2, m1** (In Progress, unassigned, 2 comments): two tamper survivors; m4 merged (#1661); m3 and m5 are NOT in the brief. m1 edits a checker (`check-compose-stack-safety.mjs`) and needs the checker's own suite (the seat finds it: I did not).
- KS-1755 (the nit-3 successor) is HELD: "It cannot be closed by widening the pattern" (its own text).

### Lane 13 (AA): `routes/platform.ts`
- **KS-1548 m2 + nit** (In Progress, unassigned, 0 comments): "the guard 'no window starts once nothing is left' ... is unpinned ... survives **all 18 cells**" and "cell G's second assertion cannot fail": nit OPEN (`ks1512-...test.ts:214`). **m1** (a stalled body vs the "never hangs" comment): the ticket allows "at minimum soften the comment"; the brief takes that unless a QUESTION is answered. **m3 is HELD** ("a ruling-interpretation question as well as a fix").
- **KS-1524 (c) then (a)** (In Progress, unassigned, 0 comments): (b) is on develop (L5). (c) a `null` throw cell (absent), (a) guard the log call (`platform.ts:1143`, unguarded; a code change on a request path: QUESTION if it needs a ruling). (d), (e) held (decision; post-deploy measurement).

### Paths checked (`git cat-file -e 362f95dd71c1:<path>`)
| lane | path | result |
|---|---|---|
| W | `Blockchain/Dev/services/auth/src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts` | rc=0 |
| W | `Blockchain/Dev/services/auth/src/__tests__/ks1186-userrepo-fromrow-sites-are-awaited.test.ts` | rc=0 |
| W | `Blockchain/Dev/services/auth/src/repositories/userRepo.ts` | rc=0 |
| W | `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` | rc=0 |
| W | `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` | rc=0 |
| X | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts` | rc=0 |
| X | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` | rc=0 |
| X | `Blockchain/Dev/services/api-gateway/src/index.ts` | rc=0 |
| X | `Blockchain/Dev/deployment/azure/RUNBOOK.md` | rc=0 |
| X | `Blockchain/Testing/USER SIMULATED TEST/02-verifier.md` | rc=0 |
| X | `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` | rc=0 |
| X | `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` | rc=0 |
| X | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1493-verification-limiter-sits-above-the-audit-middleware.test.ts` | rc=128 |
| Y | `Blockchain/Dev/services/originate/src/__tests__/ks1061-shared-mock-completeness.test.ts` | rc=0 |
| Y | `Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts` | rc=0 |
| Y | `Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts` | rc=0 |
| Y | `Blockchain/Dev/services/mcp-server/src/tools/info.ts` | rc=0 |
| Y | `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` | rc=0 |
| Y | `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` | rc=0 |
| Z | `Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh` | rc=0 |
| Z | `Blockchain/Dev/scripts/__tests__/ks1347_proxy_out_dir_spaced_checkout.test.sh` | rc=0 |
| Z | `Blockchain/Dev/scripts/__tests__/ks1355_slot_blind_launchers.test.sh` | rc=0 |
| Z | `Blockchain/Dev/scripts/check-compose-stack-safety.mjs` | rc=0 |
| Z | `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` | rc=0 |
| Z | `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` | rc=0 |
| AA | `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` | rc=0 |
| AA | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts` | rc=0 |
| AA | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1512-platform-audit-log-pages-the-upstream-past-its-200-clamp.test.ts` | rc=0 |
| AA | `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` | rc=0 |
| AA | `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` | rc=0 |

## 3. DONE-READY candidates for the board seat (evidence at source; none moved by me)

| ticket | evidence read at `362f95dd7` | caveat |
|---|---|---|
| KS-1750 | `3b48991cd` "Refs KS-1750 ... (#1739)": +27 lines in `pre_push_hook_base.test.sh` + the two docs; the ticket is one item | its comment records the sibling grader: file it first (G24 item 4) |
| KS-1738 | `362f95dd7` (#1741): `generated_guard.sh` +32, restore test +78, `bootstrap_login_diagnosis.test.sh` +7/-1 | merged 15:45, minutes old |
| KS-1667 | `dd893cfa2` (#1738): `documents.ts:1959` names `services/gdprService.ts`; READY comment: all three items | comment-only in a runtime file |
| KS-1159 | `50662382c` (#1482): cells T6b, T6c, T7, T8 at `ks1061-...test.ts:161-174` | residue is KS-1491 (lane 11) |
| KS-1621 | items 1, 2 on develop (cells F5 `:162`, D4 `:142`) | item 3 is lane 10: Done only after it merges |
**Looked done, are not:** KS-1525 (open product question on G7/G8, its own comment; pre-existing defect is KS-1639), KS-1746 (item 4), KS-1752 (item 2), KS-1620 (items 2-3), KS-1155 (auth and security instances), KS-1503 (the action is on develop, cell M1; "decide notes 2, 3, 5" remain: a decision ticket now), KS-1595 (part 1 on develop, part 2 open), KS-1671 and KS-1642 (merged runtime fixes, undeployed: fleet rule). **Possibly done, unverified:** KS-1583 and KS-1605 Minor 1 (the shapes they ask for are in `check-package-format.sh`'s header at `:111-:274`; per-item state not established).

## 4. Held, with reasons (not in any lane)

| ticket | why held |
|---|---|
| KS-1329 | its own text: the `ssrf-guard.ts` TS2349 fix "Decide it here, with the guard's owner"; the ks781 errors "blocked until PR #1268 merges" (G24 comments on it) |
| KS-1593 | "Facts only, no fix shape chosen"; originate is not in the test-type ratchet's default list |
| KS-1595 part 2 | 27 JWT-claim reads through `any`: a product typing change, not a cell |
| KS-1587, KS-1568, KS-1712 | need a real Postgres (integration cells, advisory-lock waits, TZ run) |
| KS-1737 | "belongs to whoever owns the service's compile target" |
| KS-1755 | nit-3 successor: a design question (caller-read vs internally-assigned) |
| KS-1757 | sibling of the in-flight #1740 (same file, `api-gateway.openapi.ts`): after #1740 merges |
| KS-1758 | "A decision and a test, not a defect report" |
| KS-1676 | its remaining row is "Undecided" (`!chain`) |
| KS-1614 items 1-3, KS-1548 m3, KS-1524 d/e, KS-1493 N2, KS-1491 item 4 | decisions or post-deploy measurements the tickets themselves name |
| KS-1720, KS-1721 | Python 3.14 Linux-only behaviour (needs a Linux run); KS-1720's fix surfaces 317 mypy errors: a scope call |
| KS-1748, KS-1749, KS-1747, KS-1705, KS-1751, KS-1745(b), KS-1589 B/C, KS-1727 | as in the 11:15 report (unchanged) |
| KS-1728 | 150 sites in 29 files, mechanism "the explanation that fits, not a proven one" |
| KS-1155 | partly on develop; remainder is cross-service |

## 5. What I did NOT verify (plainly)
- **Open PRs** (no `gh`): unverified. A PR on any lane file would collide; each brief's QUEUE 0 measures it.
- **Every ratio** in the briefs (10/10, 35 of 35, 18 cells, 68/0, ...) is a ticket author's or seat's figure; I ran nothing. "OPEN" means the text the ticket describes is still present at the tip when read by `git show`/`git grep`, not that a mutant survives today.
- **Seat ordinals** and the `inbox_routing.conf` additions: unverified (`history.md` not opened).
- **KS-1558 m1's test suite** (which suite exercises `check-compose-stack-safety.mjs`): not found; the brief tells the seat to find it.
- **KS-1637 Minor 1** and **KS-1524 (a)'s neighbour `routes/batch.ts`**: not read for a landed fix / the same hazard.
- **G24 finding 2's run record** (1 stall in 9, 60000 ms vs 1-5 s) and finding 4's "4/0 at base": from Wednesday's message only.
- **Pool coverage:** ~45 of 646 ticket bodies read; the rest by title only.

## 6. Where the next wave should look (not queued)
The gate-follow-up family (KS-1583, 1587, 1605, 1612, 1613, 1614, 1619, 1622, 1623, 1642, 1658, 1676) is where this wave's misses were: many are partly worked and need a per-item read at the tip; a board pass that marks each item done/open would unlock the next lanes more cheaply than building. G 24th item 6 starts that for six tickets.

## 7. What Wednesday has wrong in this prompt
1. Develop is `362f95dd7`, not `3b48991cd` (#1741 merged at 15:45).
2. KS-1738 is no longer "in flight": #1741 merged. KS-1753 #1740 and KS-1754 #1742 are still on the floor (state read In Progress; PR state unmeasured).
3. Finding 1 of the G24 list is covered by KS-1329 (comment, not a filing); finding 4's sibling is recorded inside a KS-1750 comment; the two #1740 findings are already KS-1757 and KS-1758.
4. Letters W-AA are unrouted.
