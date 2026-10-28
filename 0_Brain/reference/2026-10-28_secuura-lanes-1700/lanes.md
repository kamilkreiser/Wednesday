# Secuura Platform K wave-5 lanes - 2026-10-28 ~17:00-17:50 AEDT (drafter, read-only)

Drafter: claude-sonnet-5-5, row C8 (Agent-tool drafter for Wednesday). Nothing was written to any board, repo, mail, pane or other project's files. Written: this report, six lane briefs (lanes 19-24) under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/`, and a scratch clone at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/drafter-lanes1700` (a NEW path under `cache/work/`; `git -C <dir> rev-parse --show-toplevel` equals the dir, asserted). Git verbs used on the clone: `clone --no-checkout` of the local `cache/src`, `remote set-url`, `config core.sshCommand`, `fetch origin develop`, `ls-remote`, `cat-file`, `show`, `grep`, `ls-tree`, `log`. Nothing under `!CODING/` was touched. The Linear key was sourced transiently from the project `.env` inside a Python process and never printed or copied; `GH_TOKEN` likewise, into a scratch `GH_CONFIG_DIR`. No suite, build, mutant or script of the repo was run by me: every 'open' below is a read of source at the sha, not an execution.

## BLUF

1. **Develop read from origin: `bd6697e079fce41db6b21e094a9eddb3d0e1d08e`** (2026-10-28T15:29:56+11:00), equal to the expected sha (`git ls-remote origin refs/heads/develop` in the scratch clone, then fetched and `cat-file -e` rc 0).
2. **Board: 696 open KS issues** (backlog+unstarted+started; 696 unique ids of 696 nodes; 7 pages of 100, not capped): Backlog 352, In Progress 266, In Review 50, Todo 25, Blocked 3; assignees: our account 492, unassigned 183, peter@obeden.com 13, stuart.jamieson 8. Highest open number KS-1784. Pool (Backlog+Todo+In Progress) 643; without Peter's and Stuart's 624.
3. **Six lanes (14 queue items over 10 tickets) pairwise file-disjoint** (script: no shared path between any two lanes, none with R 6th's 'Yours' list, none with the 14 open PRs' files, a planted-overlap control fires). Letters used: X, Y, Z, AA, W, S (none live today: the pane list holds only `wednesday`, R, D, `fleet-monitor`).
   - **19 / X (Opus, C3):** KS-1240 on api-gateway (front door and proxies) and the auth social providers; 401-vs-503 and the unclassified `/social/link` rejection are the named defects of Spark passes M and O.
   - **20 / Y (Sonnet, C2):** KS-1240 on nft-certificate IPFS (body stall unmapped) and tenant-provisioning (key-less tenant answering 201): a QUESTION is built into item 2.
   - **21 / Z (Sonnet, C2):** KS-1382 (Todo): five Blockchain/Testing entry points default TARGET_BASE to slot 1; new shell suite for slots 1-4.
   - **22 / AA (Sonnet, C2):** KS-1472 (spec wording) + KS-1537 m-1, N-1, N-2 (reserved-key prose and two real-Postgres pins); N-4 carded.
   - **23 / W (Sonnet, C2):** KS-1702 (migration 055 cell file) + KS-1588 (ks1009 header and error-path cells): test-only, red-first mutants.
   - **24 / S (Sonnet, C2):** KS-1394 (audit-locks message) + KS-1113 (e2e DSR status): two small spelled-out fixes.
4. **A cheap fact for the board seat:** In Progress is 266 tickets, and the ones I opened were mostly MERGED and waiting on deploy (KS-1731 'Merged', KS-1658 'MERGED #1634', KS-1676 'MERGED #1644', KS-1456 fixed at the tip, KS-1602 'PR 1703 up, READY FOR GATE'). In Progress is not 'unbuilt'; I lane'd none of them. 164 In Progress tickets carry a comment opening with a MERGED marker (a lower bound, by a crude prefix match).
5. **Spark-briefable:** KS-1588, KS-1394, KS-1113 are Spark-sized (they sit inside lanes 23/24 as the Claude fallback; Wednesday strikes the item if she sends it to the Spark). Section 5 has the screen. None of the other 600+ was read below the title.
6. **Cards (need Kam/Wednesday/client rulings, NOT laned):** section 4.
7. **Open PRs read live:** 14, 93 file entries on 54 distinct paths, mostly dependency bumps and lockfiles; none intersects any lane.

## 1. Counts (predicate, cap, controls)

**FOUND** 696 open KS issues now. Predicate: `issues(first:100, after:$cursor, filter:{team:{key:{eq:"KS"}}, state:{type:{in:["backlog","unstarted","started"]}}})`, cursor loop until `hasNextPage` is false, 7 pages, 696 nodes, 696 unique ids. `comments(first:50)` read per ticket (a ticket with more than 50 comments would be truncated: the opened tickets have fewer; KS-1402 has 23, the largest I opened was KS-1682 with 10).
By state x assignee (the tally script is `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-28_secuura-lanes-1700/tools/gen.py`'s report step; the raw pull is `(not kept; re-pull with /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-28_secuura-lanes-1700/tools/pull.py)`, which holds ticket text and no key): Backlog 352; Blocked 3; In Progress 266; In Review 50; Todo 25.
**TESTED** Positive control: the open set contains KS-1240 and its text search `KS-1240` hits 0 tickets (fires). Zero control: the coined token `zzqz-wed-ctl-1700-5531` (written nowhere) hits 0. These are searches over the pulled open set (title, description, comments), NOT a board-wide text search; the 'search before filing' duty is the seats' and each brief carries it. State names sum to 696.
**HOW** Linear GraphQL as above; the same pull read assignee email, state, labels, description and the 50 newest comments in one pass; source read with `git -C <clone> show/grep/ls-tree/cat-file bd6697e079fc:<path>`; open PRs with `gh pr list -R Secuura/Distributed_Secuura --state open --limit 300 --json number,title,headRefName,author,files` and the project token in a scratch `GH_CONFIG_DIR` (read-only; rc 0, 14 PRs).
**NOT READ** The bodies of roughly 579 of the 624 pool tickets. I read in full about 45 (listed in sections 2 to 4) and screened the rest by title, file-path count and decision-word count (a heuristic, not a read). The lanes are the best-evidenced work I found, not the whole pool. Specifically NOT read: the ~45 `Security:` and tenant-isolation tickets (KS-1688 to KS-1704 and neighbours), which are Opus C3/C4 and mostly need Kam rulings.

## 2. Candidate table (the six lanes)

| lane | seat | slug | tickets | model, row |
|---|---|---|---|---|
| 19 | Seat X 3rd | `ks1240_gateway_and_auth_social_fetch_timeouts` | KS-1240 | opus 5.5, C3 |
| 20 | Seat Y 4th | `ks1240_ipfs_and_tenant_provisioning_fetch_timeouts` | KS-1240 | sonnet 5.5, C2 |
| 21 | Seat Z 3rd | `ks1382_blockchain_testing_target_base_follows_the_slot` | KS-1382 | sonnet 5.5, C2 |
| 22 | Seat AA 4th | `ks1472_ks1537_spec_prose_and_reserved_key_pins` | KS-1472, KS-1537 | sonnet 5.5, C2 |
| 23 | Seat W 5th | `ks1702_ks1588_mutant_pinned_test_cells` | KS-1702, KS-1588 | sonnet 5.5, C2 |
| 24 | Seat S 4th | `ks1394_ks1113_audit_locks_message_and_dsr_e2e_status` | KS-1394, KS-1113 | sonnet 5.5, C2 |

| ticket | files (tip bd6697e079fc) | size | routing row | why agent-actionable |
|---|---|---|---|---|
| KS-1240 (gateway + auth social) | gateway `middleware/auth.ts`, `routes/proxy.ts`, `admin.ts`, `batch.ts`, `audit-export.ts`; auth `providers/social/{github,google,linkedin,apple,facebook,microsoft-personal}.ts`; 3 NEW tests | 11 + 12 fetch sites, 3 new tests | C3 Opus | the ticket states the fix (timeout + decide refusal shape, 503); Spark passes M and O exist as reference with named defects; QUESTION route for the status code |
| KS-1240 (ipfs + provisioning) | `nft-certificate/.../ipfs.service.ts` (8 fetches), `tenant-provisioning/src/index.ts` (1), `meteringKey.ts` (1); 2 NEW tests | 10 fetch sites | C2 Sonnet | same; the Q behaviour is a named QUESTION, the bound is in the PR regardless |
| KS-1382 | 5 shell entry points + `tests/tenant-isolation/runner.ts` + 2 READMEs + 1 NEW suite | 8 files edited, 1 new | C2 | the ticket carries 'Fix' and 'Acceptance' sections (Kam's call recorded); one real flag: how to tell a named slot from the default 1 |
| KS-1472 | `auth.openapi.ts` (2 descriptions), generated `secuura-api.yaml`, ks839 + ks1210 tests | 3 sources + 2 tests | C2 | 'spec-text-only PR' with the exact wording points and `generate-openapi`/`check:openapi` |
| KS-1537 m-1, N-1, N-2 | `originate.openapi.ts` (4 operations), yaml, `ks1508-a-planted...integration.test.ts`, 1 NEW pin test | 2 sources + 2 tests | C2 | checklist with named gate mutants X1, A6b, X4; N-4 excluded (decision) |
| KS-1702 | `ks1557-055-backfill.integration.test.ts` (393 lines) | 1 file, 3 items | C2 | 'test-only', named mutants O3/O4, fix shape for REPORT and header |
| KS-1588 | `ks1009-wallet-status-reveals-only-existence.test.ts` | 1 file, 2 cells | C2 (Spark L6 possible) | 'Fix shape (the gate's, unchanged)' with measured expected header set and body |
| KS-1394 | `scripts/audit/audit-locks.mjs` (message at `:350-354`) | 1 file | C2 (Spark L1 possible) | ticket gives two measured problems and a suggested shape; gate-leg file, so message-only |
| KS-1113 | `tests/e2e/tests/gdpr-compliance.prelaunch.spec.ts` (`:464`, `:475`) | 1 file, 2 hunks | C2 (Spark L2 possible, but proof is an e2e run) | 'Recommendation' names the change |

## 3. Disjointness matrix

Script: `gen.py` builds each lane's 'Yours' set from the brief data, then `git cat-file -e bd6697e079fc:<path>` on every path (existing files rc 0; the NEW files rc 128 on purpose), then intersects. The two `Projects Documents/` HTML docs are excluded as the one shared append-only surface (as in waves 3 and 4).

| | 19 (X) | 20 (Y) | 21 (Z) | 22 (AA) | 23 (W) | 24 (S) | R 6th yours | R 6th reserved J-Q | open PRs |
|---|---|---|---|---|---|---|---|---|---|
| **19 (X)** | - | 0 | 0 | 0 | 0 | 0 | 0 | 11 | 0 |
| **20 (Y)** | 0 | - | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| **21 (Z)** | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 | 0 |
| **22 (AA)** | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 0 |
| **23 (W)** | 0 | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 |
| **24 (S)** | 0 | 0 | 0 | 0 | 0 | - | 0 | 0 | 0 |

All lane-vs-lane, lane-vs-R-6th-yours and lane-vs-open-PR cells are 0. Sizes: R 6th 'Yours' 24 paths (PRs A-I + H2; 55 is the count across all 23 passes); R 6th reserved J-Q 31 paths; open PR files 54 distinct paths (93 entries).
**The reserved column is nonzero BY DESIGN:** KS-1240's passes M, O, P, Q were INCLUDED in this wave by the drafting prompt, so lane 19 holds 11 reserved paths (M's five gateway files and O's six provider files) and lane 20 holds 3 (P's ipfs.service.ts, Q's index.ts and meteringKey.ts). No other lane touches the reserved set. Reserved files that stay UNCLAIMED after this wave: J (auth routes/auth.ts, KS-1776), K (api-gateway services/enforcement.ts, KS-1197), L (originate certifications.ts, documents.ts, helpers/sharedModuleMock.ts, KS-1701, WIDENS access: needs a ruling), N (tokenisation.ts, no callers).
**Control:** a planted overlap (lane 19's set plus one lane-20 file) vs lane 20 reports a nonzero overlap: control fires = True. The raw results are in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-28_secuura-lanes-1700/disj.json`. Path-existence defects found: none.
**Same-service adjacency worth a glance (not an overlap):** lanes 19 (X) and 23 (W) both work in `services/auth` on different files; lanes 19 and R 6th PR F/I/C also work in `services/auth` on different files; lane 22 (AA) edits `auth.openapi.ts` and the shared `secuura-api.yaml`: any other seat regenerating the yaml (none planned) would conflict.

## 4. Rejected and carded candidates (reason)

| ticket | verdict | reason (read) |
|---|---|---|
| KS-1743 | card | POST /api/documents 10,000-char title answers 500: cause assumed in its own text; a title limit is a product decision (schema + DB) |
| KS-1732 / KS-1657 / KS-1132 class | card (one ruling unlocks several) | a failed database read answering as empty/null: needs the convention ruling "let the error propagate" (named in KS-1657) |
| KS-1419, KS-1424 | card | updateDocument returns null for two meanings / a UUID update matches 0 rows silently for 12 callers; the ticket says "changing the other 12 needs its own decision" (changes what several callers report) |
| KS-1112 | card | PATCH DSR 200-vs-404: "One decision, then one small change" (align vs document) |
| KS-1473 | card | verify-batch is documented and nothing serves it: "Owner decision" (implement vs remove the row and two CSRF entries) |
| KS-1322 | card | keep or strip internal ticket keys in published spec text: "No change should be made on a seat's own judgement" |
| KS-1537 N-4 | card | the dropped value on /certifications/issue stays visible (echo, record, hash): "decide, then record" |
| KS-1463 | card | packages/shared test imports demo-service; "Suggested shapes (not prescribed)": move the test vs a root guard suite |
| KS-1389 | card | asks for a view on one coordinated change across systemTest and preflight leg 13; `stack_env.sh` coupling |
| KS-1593 | card | "Facts only, no fix shape chosen"; originate is outside the test-file type-check ratchet |
| KS-1357 | reject (collision, decision) | rotate-secret 200 omits `id`: add it or write a rotate-specific schema is a contract choice; the handler is in `routes/oauth.ts`, R 6th PR I's file |
| KS-1737 | card | vc-issuer compile target (commonjs vs es2022) "belongs to whoever owns the service's compile target" |
| KS-1742, KS-1670 | reject (collision) | m365 `index.ts` is R 6th PR D's file |
| KS-1776, KS-1197, KS-1701 | reserve | Spark passes J, K, L: shape alternatives / partial fix / WIDENS platform-admin access (L needs a ruling); a LATER Claude lane, not this wave |
| KS-1240 pass N (tokenisation.ts) | card | bounds code that has no callers at the pin (found by operator 3): is a PR for unused code wanted now? |
| KS-1481 | reject (collision, unmeasured) | dot-segment spellings forwarded verbatim; exposure unmeasured; the gate is in `proxy.ts`/`specRouteMap`, M's files |
| KS-1409 | reject (not fully read) | webhooks reject connector principals: facts only, "nothing here was measured live"; fix shape not chosen |
| KS-1676, KS-1642, KS-1658, KS-1731, KS-1456, KS-1602, KS-1449 | reject (already merged or fixed) | In Progress awaiting deploy/done-move: comment trail shows a merged PR; at the tip KS-1676 has four ks1676 test files and KS-1456 carries its own fix comment |
| KS-1727 (wallet-signature positive cell red) | reject (measure first) | fails only on Node v26.8.1 per its comments; not measured on the LTS line; verifier correctness is a security surface (C3) and the cause is not established |
| KS-1702 N1 | excluded | product-behaviour residue that stays on KS-1557 (kintsugi counting precondition) |
| KS-1721 / KS-1720 | reject | schemathesis: 1721 fails on Linux only and the QA gate saw it PASS on macOS; 1720 needs a decision on 317 mypy errors in 100 files (baseline or fix) |
| Security / tenancy tickets (KS-1688 to KS-1704, KS-1594, KS-1584, KS-1570, KS-1535, KS-1604, KS-1572, KS-1573, ...) | card (Kam) | auth/tenant DESIGN decisions or POLICY ("Kam's call"); excluded by the prompt (auth/credential DESIGN decisions); Opus C3/C4 at best, after rulings |
| Peter's (13) and Stuart's (8) | excluded | never queued |

**Candidate cards for Wednesday to put to Kam** (each is one decision, quoted from the ticket): the swallowed-DB-error convention (KS-1657 class); updateDocument's two-meanings null (KS-1419/1424); KS-1112 align-or-document; KS-1473 implement-or-remove; KS-1322 keep-or-strip; KS-1537 N-4; KS-1743 title limit; KS-1240 pass N (unused code); KS-1240 pass Q's key-less tenant (also asked inside lane 20 as a QUESTION, so Kam is only asked if Wednesday's reading is 'Kam').

## 5. Spark-briefable list (do not brief; for Wednesday)

Predicate (model-routing section 3, as used in wave 4): one to three product or test files, the ticket spells out the fix shape, a runnable in-process test nearby, NOT an auth/credential design surface, not owned by a lane or R 6th.

| ticket | file | why it passes | caveat |
|---|---|---|---|
| KS-1588 | `auth/src/__tests__/ks1009-wallet-status-reveals-only-existence.test.ts` | test-only (L6), two cells, header set and 500 body spelled out, mutants N3/N8 named | auth test file, route untouched; needs the L6 test_only wiring; is item 2 of lane 23 |
| KS-1394 | `scripts/audit/audit-locks.mjs` | one file, message text, two measured problems, suggested shape | preflight leg 7 file: message-only; the proof needs docker or a scratch lock tree; is item 1 of lane 24 |
| KS-1113 | `tests/e2e/tests/gdpr-compliance.prelaunch.spec.ts` | one file, two hunks, recommendation names the change | the proof is an e2e run against a stack, which no local checker does; is item 2 of lane 24 |
Nearest misses (not briefable): KS-1472 (generated yaml), KS-1456 (already fixed), KS-1702 (real Postgres). The same screen: ~45 ticket bodies read, the rest by title only (a floor, not a census).

## 6. What I did NOT verify (plainly)

- **Whether #1497 is merged** (lane 22 item 2 depends on it; the brief makes the seat read `gh pr view 1497`).
- **Every drafter line number and count** (`grep`/`show` at the tip; nothing executed). Ticket-quoted figures (e.g. 15 guard clauses, 14 mutants) are the authors'.
- **What `validateApiKey` timeouts and exchange failures answer end to end** beyond the call-site reading; lane 19 makes the seat measure it before choosing.
- **Whether `routes/auth.ts` can stay untouched** while classifying a provider timeout (lane 19 item 2 assumes the provider can throw the classified error itself; if no such error type exists the seat defines one).
- **Whether the per-lane test names collide with files other seats are creating** (the `ks1240b-` prefix avoids the Spark's held names `ks1240-...`).
- **Live seats beyond the pane list:** D 38th and R 6th only.
- **STANDING_LINES line numbers cited in the HOLDS block** (408, 536, 537, 539, 540, 348, 86) were copied from the wave-4 template, not re-checked; the briefs name each rule by text so a seat can find it.
- **The briefs' SELF-CHECK line is left blank on purpose** for Wednesday.
