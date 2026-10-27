# Secuura Platform K wave-4 lanes - 2026-10-28 ~01:40-02:10 AEDT (drafter, read-only)

Drafter: claude-sonnet-5-5, row C8 (Agent-tool drafter for Wednesday). Nothing was written to any board, repo, mail, pane or other project's files. Written: this report and five lane briefs (lanes 14-18) under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/`. The Linear key was read from the environment file and never printed or copied. No git verb that writes was used (read verbs only: `show`, `grep`, `ls-tree`, `cat-file`, `log`, `rev-parse`, `merge-base`); no suite, build, mutant or script of the repo was run by me: every "open" or "done" below is a read of source at the sha, not an execution.

## BLUF

1. **Develop read: `3a71a1c920cd8e80f226cde635d8314f07342fd6`** (merge of #1758, committed 2026-10-27T13:50:50Z = 00:50 AEDT, read in the already-fetched clone, no fetch by me). **`061c3a4f62d5` (the deployed sha) is an ancestor** (`merge-base --is-ancestor` rc 0). Between the wave-3 base `362f95dd7` and this tip `git rev-list --count 362f95dd71c1..3a71a1c920cd` is 26 (20 non-merge); the ones that touch the board's lane tickets are #1743-#1755 (the wave-3 PRs, all landed) and Akto/KS-1762/KS-1608 work in `systemTest`, which no wave-4 lane touches.
2. **Board: 693 open KS issues** (types backlog+unstarted+started; 693 unique ids of 693 nodes; 7 pages of 100, not capped; Backlog 353, In Progress 265, In Review 47, Todo 25, Blocked 3; assignees: our account 489, unassigned 183, peter@obeden.com 13, stuart.jamieson 8). Highest open number KS-1773. The actionable pool (Backlog + Todo + In Progress) is 643.
3. **Five lanes, 8 tickets**, pairwise disjoint file sets (checked by a script that parsed each BRIEF's own "Yours" list and re-ran `git cat-file -e` on every path: no overlap, a planted overlap control fires; the two `Projects Documents` HTML docs are the one deliberately shared, append-only surface, as in wave 3).
   - **14 / W** KS-1765 (auth ks1000 test residuals) Sonnet C2.
   - **15 / X** KS-1769 (`countUsersInner` catch, request-path behaviour change) **Opus** C3, gate G1.
   - **16 / Y** KS-1766 then KS-1771 (api-gateway stale text; six log-line describers) Sonnet C2.
   - **17 / Z** KS-1772 then KS-1767 (originate five describers; mcp-server error type) Sonnet C2.
   - **18 / AA** KS-1757 then KS-1760 (connector/info prose + regenerated yaml; R2 cell title) Sonnet C2.
4. **Letters chosen: W, X, Y, Z, AA.** `inbox_routing.conf` has these Blockchain letters: B, C, D, E, F, G, J, K, V, R, S, T, U, W, X, Y, Z, AA and BOARD (lines 36-47, 55, 215, 243-247). Excluding D and G leaves B, C, E, F, J, K, R, S, T, U, V, W..AA. I chose W-AA because (a) their routing lines exist already (243-247, so Wednesday adds nothing), (b) the wave-3 lanes that used them are merged (#1743-#1755), so the letters are free of live work, and (c) the older letters carry long histories and tools keyed to old generations. **Cost, stated in each brief:** each letter has an earlier occupant (`Seat W 1st`... `Seat AA 1st`), so the new seat's ordinal is not 1st and mail naming the earlier occupant must read FOREIGN. Whether any wave-3 seat in those panes is still alive was NOT measured.
5. **Two tickets in the prompt's candidate list are held, not queued, and why:** KS-1770 (a renumber of an append-only doc whose numbers are set at merge time: a decision, read) and KS-1764/KS-1773 (undecided owner questions, read: KS-1764 "delete it or keep it as a documented refusal is undecided"; KS-1773 "No fix is proposed and no posture is decided" on an auth surface).
6. **Spark: 0 briefable** among the 18 tickets whose bodies I read (list and reasons in the SPARK SCREEN below); nearest miss KS-1657.
7. **Done candidates for a board seat:** KS-1634 (fix deployed, see section 3, with one open sibling finding to read first). Wave-3's other tickets stay open for held decisions (section 3).
8. **Open PRs are UNMEASURED** (no usable `gh`): every brief's QUEUE 0 measures them under the project's identity and stops on any intersection.

## 1. Counts (predicate, cap, controls)

**FOUND** 693 open KS issues now: `issues(first:100, after, filter:{team KS, state.type in [backlog, unstarted, started]})`, cursor loop until `hasNextPage` false (7 pages), 693 nodes, 693 unique ids. Last read of the same predicate (previous report, 2026-10-27 ~15:5x): 691. Tickets created since: KS-1759..KS-1773 exist and are open or Done (KS-1759..KS-1761 and KS-1764..KS-1773 are Backlog; KS-1762 Done, Peter's; KS-1763, KS-1768 Peter's). Of the 12 occurrences of the describer expression the tickets describe, `git grep -c 'getPrototypeOf(err)?.constructor?.name'` over `Blockchain/Dev` at the tip finds exactly 12 lines in 9 files (api-gateway 7 incl. `platform.ts:1148`, already fixed; originate 5): every open site is in a lane.
**TESTED** Positive controls: the state names sum to 693 (353+265+47+25+3). Board text search (title OR description OR any comment body, `includeArchived: true`, paged to the end): `KS-1531` returned 40 hits (fires); `countUsersInner` 4 (KS-1168, KS-1484, KS-1769, KS-968); `getPrototypeOf(err)` 3 (KS-1621, KS-1771, KS-1772); `ks1531-connector-info` 3 (KS-1748, KS-1752, KS-1760). **Zero control** `zzqz-wed-ctl-0140-9281` (coined by me, never written to any ticket) returned 0 on the same query shape. That token is now used; do not reuse it.
**HOW** Linear GraphQL (`comments(first:50)` sorted client-side, never `last:N`, `includeArchived:true` for lookups, `number` filter per ticket); source read with `git -C <clone> show/grep/ls-tree/cat-file 3a71a1c920cd:<path>` in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src`. Every brief provenance ticket line was read live in one pass at 2026-10-28 ~01:40 AEDT.
**NOT READ** The bodies of about 620 of the 643 pool tickets: I read in full KS-1634, 1743, 1757, 1759, 1760, 1761, 1764, 1765, 1766, 1767, 1769, 1770, 1771, 1772, 1773, 1657, 1648, 1647, 1681 and the comments of 1491, 1493, 1524, 1548, 1558, 1560; the other 103 non-Peter tickets numbered 1640 and above were screened by TITLE only (list printed during the read). The lanes are the best-evidenced work I found, not the whole pool.

## 2. The lanes

All paths checked with `git cat-file -e 3a71a1c920cd:<path>` (table at the end of this section; the three NEW files are rc=128 on purpose and are said so in the briefs). Docs: each brief grants the two `Projects Documents/` HTML docs for appending (test changes) and carries the skill's escape clause ("say so explicitly and why") for prose-only PRs.

| lane | seat | brief | tickets (order) | file family | model / row | difficulty |
|---|---|---|---|---|---|---|
| 14 | W | `2026-10-28_seatW_lane14_auth_ks1000_expectrun_residuals.md` | KS-1765 (items 3, 1, 2) | auth `ks1000` test only | Sonnet 5.5, C2 | medium |
| 15 | X | `2026-10-28_seatX_lane15_auth_count_users_503.md` | KS-1769 | auth `userRepo.ts` (`countUsersInner`) + `ks1186` test | **Opus 5.5, C3**; gate G1 | medium (request path) |
| 16 | Y | `2026-10-28_seatY_lane16_gateway_stale_text_and_log_describers.md` | KS-1766, KS-1771 | api-gateway ks1543/ks1628 tests, 5 route files, a NEW ks1771 test | Sonnet 5.5, C2 | easy then medium |
| 17 | Z | `2026-10-28_seatZ_lane17_originate_describers_and_mcp_error_type.md` | KS-1772, KS-1767 | originate 4 route files + a NEW ks1772 test; mcp-server `api-client.ts`, `info.ts`, a NEW ks1767 test | Sonnet 5.5, C2 | medium |
| 18 | AA | `2026-10-28_seatAA_lane18_connector_info_contract_prose.md` | KS-1757, KS-1760 | `api-gateway.openapi.ts`, regenerated `secuura-api.yaml`, ks1531 test | Sonnet 5.5, C2 | easy |

### Lane 14 (W): KS-1765
Backlog, our account, 0 comments. All three residuals OPEN at the tip: the substring branch (`ks1000...:89`) and `AUTH_GREEN_SUMMARY` (`:129`); the one-value guard still bracket-bounded (`:102`), its own comment at `:100` records the nested-bracket gap; only the REAL cell is pinned (`:1284`); 43 `expectRun(` occurrences (42 call sites). Item order 3, 1, 2 (easy to hard). **Honest note:** the ticket says "no fix is proposed"; the shapes (boundary on the summary, a bracket-depth scan, a syntax-tree census) are mine, labelled as a lean, with a QUESTION route for item 2's extent.

### Lane 15 (X): KS-1769 (Opus)
`countUsersInner` (`userRepo.ts:1067-1094`) has no `try`/`catch`; `listUsersInner` has the model (`:1042`, `:1049`). Callers `routes/users.ts:464-465` and `:520-521`. The edit is the list's catch copied; **the model choice is Wednesday's instruction** (the drafter's note in the brief: by content it is near C2 and could be downgraded). The ticket records "whether the count's errors should map to 503 ... not decided"; the brief lets the seat stop with a QUESTION. The ten other names in the ticket's unclassified scan are explicitly NOT touched.

### Lane 16 (Y): KS-1766 then KS-1771
KS-1766: ks1543 `:109` and ks1628 `:178` text, both OPEN; fix by naming the log line by message (the line number would move). KS-1771: six sites open (audit-export `:28`, `:184`; batch `:28`; notifications `:30`; platform `:508` ONLY; verification `:1067`), same shape as #1754's `platform.ts:1148`; the existing `ks1346` and `ks1510` tests are read-only controls that must stay green. The seat MEASURES each site first (the ticket says none was driven) and reports UNPROVEN rather than skipping a site it cannot drive.

### Lane 17 (Z): KS-1772 then KS-1767
KS-1772: five originate sites open (`adminConfig.ts:111`, `:2235`; `gdpr.ts:211`; `systemErrors.ts:94`; `webhooks.ts:573`). `:2235` also sits in KS-1462's call site; the brief tells the seat to read KS-1462 and change only how the text is built. KS-1767: the three `error?: string` declarations and the `info.ts:130` cast; the ticket does not establish the wire shape of two routes, so the brief widens to a union and has the seat record the wire reads. **The seat may find no cell can honestly go red for a type-only change; the brief says to say so rather than write a cell that cannot fail.**

### Lane 18 (AA): KS-1757 then KS-1760
KS-1757 (unblocked now that #1740 is Done): sentence still at `api-gateway.openapi.ts:904-905` and `secuura-api.yaml:15968`; the ticket's recommendation is quoted in the brief; the yaml is regenerated, never hand-edited; ships only on a deploy plus gateway restart (the seat does not deploy). KS-1760: reword the R2 title to what the cell observes, move the reasoning into a comment; NOT adding an observable (product change; KS-1747 owns that). The reword is the drafter's lean, labelled not-a-ruling.

### Paths checked (`git cat-file -e 3a71a1c920cd:<path>`)
| lane | path | result |
|---|---|---|
| 14 (W) | `Blockchain/Dev/services/auth/src/__tests__/ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts` | rc=0 |
| 14 (W) | `Blockchain/Dev/services/auth/src/__tests__` | rc=0 [read-only] |
| 14 (W) | `Blockchain/Dev/services/auth/src/__tests__/ks1186-userrepo-fromrow-sites-are-awaited.test.ts` | rc=0 [read-only] |
| 15 (X) | `Blockchain/Dev/services/auth/src/repositories/userRepo.ts` | rc=0 |
| 15 (X) | `Blockchain/Dev/services/auth/src/__tests__/ks1186-userrepo-fromrow-sites-are-awaited.test.ts` | rc=0 |
| 15 (X) | `Blockchain/Dev/services/auth/src/routes/users.ts` | rc=0 [read-only] |
| 15 (X) | `Blockchain/Dev/services/auth/src/repositories/dbErrors.ts` | rc=0 [read-only] |
| 15 (X) | `Blockchain/Dev/services/auth/src/middleware/errorHandler.ts` | rc=0 [read-only] |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts` | rc=0 |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` | rc=0 |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` | rc=0 |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` | rc=0 |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` | rc=0 |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/routes/platform.ts` | rc=0 |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` | rc=0 |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1771-api-gateway-log-line-describers-cannot-hang-a-request.test.ts` | rc=128 (NEW, on purpose) |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts` | rc=0 [read-only] |
| 16 (Y) | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts` | rc=0 [read-only] |
| 17 (Z) | `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` | rc=0 |
| 17 (Z) | `Blockchain/Dev/services/originate/src/routes/gdpr.ts` | rc=0 |
| 17 (Z) | `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` | rc=0 |
| 17 (Z) | `Blockchain/Dev/services/originate/src/routes/webhooks.ts` | rc=0 |
| 17 (Z) | `Blockchain/Dev/services/originate/src/__tests__/ks1772-originate-log-line-describers-cannot-hang-a-request.test.ts` | rc=128 (NEW, on purpose) |
| 17 (Z) | `Blockchain/Dev/services/mcp-server/src/api-client.ts` | rc=0 |
| 17 (Z) | `Blockchain/Dev/services/mcp-server/src/tools/info.ts` | rc=0 |
| 17 (Z) | `Blockchain/Dev/services/mcp-server/src/__tests__/ks1767-api-client-types-the-gateway-error-body.test.ts` | rc=128 (NEW, on purpose) |
| 17 (Z) | `Blockchain/Dev/services/originate/src/__tests__/ks1346a-systemerrors-fail500-logs-type-and-field-names.test.ts` | rc=0 [read-only] |
| 17 (Z) | `Blockchain/Dev/services/originate/src/__tests__/ks1346b-gdpr-fail500-logs-type-and-field-names.test.ts` | rc=0 [read-only] |
| 17 (Z) | `Blockchain/Dev/services/originate/src/__tests__/ks1346c-adminconfig-fail500-logs-type-and-field-names.test.ts` | rc=0 [read-only] |
| 17 (Z) | `Blockchain/Dev/services/originate/src/__tests__/ks1346d-webhooks-fail500-logs-type-and-field-names.test.ts` | rc=0 [read-only] |
| 17 (Z) | `Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts` | rc=0 [read-only] |
| 17 (Z) | `Blockchain/Dev/services/mcp-server/src/__tests__/ks1620-get-info-bounds-the-relayed-gateway-text.test.ts` | rc=0 [read-only] |
| 18 (AA) | `Blockchain/Dev/services/api-gateway/src/api-gateway.openapi.ts` | rc=0 |
| 18 (AA) | `Blockchain/Dev/docs/openapi/secuura-api.yaml` | rc=0 |
| 18 (AA) | `Blockchain/Dev/services/api-gateway/src/__tests__/ks1531-connector-info-is-in-the-published-contract.test.ts` | rc=0 |
| 18 (AA) | `Blockchain/Dev/services/api-gateway/src/index.ts` | rc=0 [read-only] |
| 18 (AA) | `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` | rc=0 [read-only] |
| 18 (AA) | `Blockchain/Dev/services/api-gateway/src/services/health.ts` | rc=0 [read-only] |
| 18 (AA) | `Blockchain/Dev/scripts/generate-openapi.ts` | rc=0 [read-only] |
| all five | `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` | rc=0 (shared, append-only) |
| all five | `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` | rc=0 (shared, append-only) |

## 3. DONE-READY candidates for the board seat (evidence at source; none moved by me)

| ticket | evidence read | caveat |
|---|---|---|
| KS-1634 | the three chain-first sites carry `simulated: chain.simulated` at `originate/src/routes/verification.ts:724`, `:1267` and `verificationV2.ts:240`; #1597 (`722e07f19cee`) and #1621 (`f321e95aa`) are ancestors of the tip; its own comment of 2026-10-27T13:34:27Z says the same; the prompt says both boxes run the fix | **Read the 13:34 comment before moving it:** its item 1 records that the sibling cell "simulated true with a real hash reads NOT on-chain" (`ks1634-v2-...test.ts:117`) takes its hash from the same helper default and asserts nothing about it, and two sibling files were not examined. The code fix is done; that test finding is open and not a lane in this wave. The board seat decides whether the finding is filed as its own ticket first. |

**Wave-3 tickets that are NOT Done-ready (each still holds a named item):** KS-1493 (N2 an owner decision; the v2-alias cell from gate f's INFO is open), KS-1491 (item 4 a decision; gate f's survivors L, B, G, H unclaimed), KS-1560 (M3 is information; M2 landed as #1749 - the board seat can check the rest), KS-1558 (m3, m5 not built; m1, m2 landed as #1753), KS-1548 (m3 held; m2 and the nit landed as #1746), KS-1524 ((d), (e) held; (a), (c) landed as #1754). Confirmed Done on the board just now: KS-1753, KS-1484, KS-1621, KS-1529, KS-1756, KS-1637, KS-1620, KS-1746.

## 4. Held, with reasons (not in any lane)

| ticket | why held |
|---|---|
| KS-1764 | its own title: "delete it or keep it as a documented refusal is undecided" (`preflight.sh:731`) |
| KS-1773 | "No fix is proposed and no posture is decided" on an unauthenticated route; its own search found no ruling; an auth-posture decision |
| KS-1770 | a renumber of an append-only doc whose "section numbers are assigned at merge time" (its own text): a decision |
| KS-1759 | "Not decided ... a warning comment in the hook or loosening the three strings"; the file is `.githooks/pre-push` |
| KS-1761 | the property-access exclusion is deliberate; "Not decided"; a different package (`packages/shared`) |
| KS-1747, KS-1758 | decisions (edge gate arming; degraded-mode posture) |
| KS-1749, KS-1748, KS-1751, KS-1755 and the earlier hold list | unchanged from the 10-27 15:45 report (section 4 there) |
| Peter's: KS-1763, KS-1768 (Backlog), KS-1762 (Done) | assignee peter@obeden.com, read: NOT ours, never queued |

## 5. What I did NOT verify (plainly)
- **Open PRs** (no `gh`): unverified. A PR on any lane file would collide; each brief's QUEUE 0 measures it.
- **Every ratio** in the briefs (1305 lines, 69 cells, 42 call sites, 12/12, 7/7, 140 suites / 1656 tests) is a `git grep` reading at the tip or a ticket author's figure; I ran nothing.
- **Whether the six api-gateway and five originate describers can actually hang a request**: the tickets say none was driven; neither did I. The briefs make the seat measure first.
- **KS-1767's wire shape** on `registerDocument` and `getWorkflowInstance` (the ticket says not traced; I did not trace it either).
- **Whether the wave-3 seats in letters W-AA are still alive**, and their next ordinals (`history.md` not opened).
- **That both boxes run `061c3a4f62d5`**: from the prompt; I only verified it is an ancestor of the tip.
- **Whether `generate-openapi` regenerates only the one sentence** (lane 18): not run.
- **Pool coverage:** see NOT READ in section 1.

## 6. Where the next wave should look (not queued)
- A 6th lane's worth of test-only hardening with named mutants, all on files no wave-4 lane owns: KS-1493 (v2 alias cell: mutant ME, `ks1493-...test.ts`), KS-1491 (gate f's survivors L, B, G, H in `ks1061-...test.ts`; L is the unsafe direction), KS-1634 (the sibling cell and two sibling files). They live in ticket COMMENTS, not in the tickets' scope sentences, so I did not queue them; a board seat could first confirm each is wanted.
- KS-1657 and its class (KS-1018, KS-1132, KS-888): a "swallowed database error answers as absence" convention. Worth one ruling from Kam; it unlocks several one-file fixes.

## 7. What Wednesday has wrong in this prompt
1. The prompt says "Seat G 25th ... moved KS-1621, 1529, 1756, 1637, 1620, 1746 to Done": confirmed on the board.
2. KS-1634 is still **In Progress** on the board (13 comments, last 13:34Z): the Done move is for the board seat, as the prompt says; the one caveat is the sibling-cell finding above.
3. KS-1769 is a good lane but the ticket itself says "Not decided" on whether the count maps to 503; the brief carries a QUESTION escape. It is Opus by your instruction; I noted that by content it reads as C2.
4. KS-1765 and KS-1767 both say "Facts only. No fix is proposed": the briefs state the fix shapes as the drafter's lean, not as a ruling.

## SPARK SCREEN

**Predicate:** one product file; the ticket spells out the fix shape; a runnable in-process test nearby; NOT an auth/token/credential/security design surface; not owned by a lane.
**Result: 0 briefable.** I read the bodies of 18 tickets (13 filed by Seats G 24th/25th that look small, plus 5 pulled from the pool by title) and screened the other 103 non-Peter tickets numbered 1640+ by title only (none looked one-file-and-spelled-out; a title is not a body, so this is a floor, not a census).

| ticket | file:line read at the tip | why it fails |
|---|---|---|
| KS-1765 | `auth/src/__tests__/ks1000-...test.ts:89,102,129` | not a product file; no fix shape ("none proposed"); owned by lane 14 |
| KS-1766 | `ks1543...test.ts:109`, `ks1628...test.ts:178` | test text in two files; owned by lane 16 |
| KS-1767 | `mcp-server/src/api-client.ts:57,105,125`; `tools/info.ts:130` | two product files; no in-process cell can fail on a type change; wire shape of 2 routes not established; owned by lane 17 |
| KS-1769 | `auth/src/repositories/userRepo.ts:1067-1094` | auth service (excluded class); request-path behaviour change; owned by lane 15 |
| KS-1771 | `api-gateway/src/routes/audit-export.ts:28,184`, `batch.ts:28`, `notifications.ts:30`, `platform.ts:508`, `verification.ts:1067` | five product files; owned by lane 16 |
| KS-1772 | `originate/src/routes/adminConfig.ts:111,2235`, `gdpr.ts:211`, `systemErrors.ts:94`, `webhooks.ts:573` | four product files; owned by lane 17 |
| KS-1757 | `api-gateway.openapi.ts:904-905`; `secuura-api.yaml:15968` | two files (one generated); no in-process test proves prose; owned by lane 18 |
| KS-1760 | `ks1531...test.ts:163` | test only; shape is a choice; owned by lane 18 |
| KS-1759 | `.githooks/pre-push:386` (graded by `pre_push_stack_legs_comment.test.sh`) | shape "not decided"; shell hook, no in-process test |
| KS-1761 | `packages/shared/src/__tests__/ks1564-...test.ts:193,224,365` | test only; "Not decided"; deliberate exclusion |
| KS-1764 | `scripts/preflight/preflight.sh:731` | "delete or keep: undecided" |
| KS-1770 | `Projects Documents/...Flow_Diagrams.html` | a renumber is a decision |
| KS-1773 | `api-gateway/src/routes/platform.ts` (document-lookup) | auth posture, undecided |
| KS-1657 | `originate/src/routes/anchors.ts:83-94` (the swallow-to-null, `:92`) | **nearest miss.** One product file with in-process tests nearby, not auth. Fails the shape predicate: the ticket lists two options and "Worth deciding as a convention" with KS-1018/KS-1132/KS-888. It would pass the day Kam or Wednesday rules "let the error propagate". |
| KS-1743 | `originate.openapi.ts` `DocumentCreateRequest.title` (no `maxLength`) | cause "assumed" in its own text; a limit is a product decision; touches schema + DB |
| KS-1648 | `api-gateway/src/middleware/auth.ts:249`, `rateLimitEnforce.ts:67` | two files on an authentication/rate-limit surface; which fallback is right is undecided |
| KS-1647 | `originate/src/routes/documents.ts:772-777`, `verification.ts:515-537` | two files; "no fix shape chosen" |
| KS-1681 | five files citing `DEPLOY-BLOCKERS.md` | "a maintainer call, not an agent one" |

Count: 18 bodies read, 0 pass; 103 titles screened, 0 selected for a body read.
