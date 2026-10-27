# Secuura Platform K wave-2 lanes - 2026-10-27 ~11:15-11:55 AEDT (drafter, read-only)

Drafter: claude-sonnet-5-5, row C8. Nothing was written to any board, repo, mail, pane or other project's files. Written: this report and four briefs under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/`. The Linear key was used from the environment and never printed. No suite, build or git write verb was run; the only git verb that writes was `git fetch origin develop` in Wednesday's cache clone (permitted).

## BLUF

1. **Develop read: `c3eb63c9d23b08132482f3211dbf8755312a7ca0`** (`ls-remote origin refs/heads/develop` equals `rev-parse FETCH_HEAD` after the fetch, 11:18 AEDT; it is the KS-1531 squash #1732, committed 09:33 +1100). It had not moved by 11:18.
2. **Board: 687 open KS issues now** (7 pages of 100, 687 unique; types backlog 347 + unstarted 25 + started 315 = 687; names Backlog 347, Todo 25, In Progress 272, In Review 40, Blocked 3 = 687). At 06:15 it was 705. **Tickets created since 06:15+11: 6** (KS-1746..KS-1751, all Seat G 22nd, all Backlog, board account); highest KS number is KS-1751.
3. **Spark-strict: 0 again**, with a control: of the 12 tickets read, each Spark clause fired on named tickets (below). The Spark cannot take comment-only tickets (`doc_patch` not wired) and every code-shaped candidate is a test-only multi-edit, a generated-file regeneration, a frontend file, or a security/schema surface.
4. **Three Claude lane briefs written, letters R, S, T** (W, X, Y are NOT in `inbox_routing.conf`: it lists B, C, D, E, F, G, J, V, R, S, T, U and BOARD; the check printed 0 for W/X/Y and 3 for R/S/T). Lane 6 (R) shell residue: KS-1746 item 5, KS-1750, KS-1738. Lane 7 (S) connector contract and m365 pin: KS-1746 items 2, 3, 1. Lane 8 (T) comment truth and the shared pin: KS-1589 A, KS-1505 part 1, KS-1667 (cond.). Their owned path sets are pairwise disjoint (checked by listing them side by side; the only repeat was a markdown artifact, not a path).
5. **Board seat brief G 23rd written**: file the KS-1643 nit-3 successor (board search done by me: no ticket covers it), split KS-1746 by suite (keeps item 5, three new tickets), triage report (the drafter proved **0 true duplicates** among KS-1746..KS-1751).
6. **KS-1751 does not fit any lane brief, and the prompt is wrong about it:** the sentence is on line 9 of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md`, a file OUTSIDE the git repository (the repo root is `Blockchain/2_Project_Files`), and that line already says "zero rows **on demo**" (re-measured 2026-08-21, KS-683). No PR can carry it. The measured fact and instrument are recorded in the lane 8 brief's PROVENANCE for whoever edits the file.
7. **A standing control is dead:** the zero-control token `zzqqxx-no-such-symbol-9931` used by Seat G 22nd now returns 7 hits (it is quoted in the "Searched" sections of KS-1746..KS-1751). A fresh token `zzqz-wed-ctl-4417` returned 0. All four briefs say not to use the old one.
8. **The earlier lane briefs carry a rule that contradicts a newer standing line:** they say pin the git identity with `git config` in every worktree; Seat V 2nd's line says a worktree has no per-worktree config, so that writes the SHARED checkout. The new briefs use `git -c`.
9. **Not queued, with reasons:** KS-1705 (needs a running slot; Peter's 10-26 comment says classification is open), KS-1749 (needs a Schemathesis sweep on a slot; systemTest may collide with Peter), KS-1745 item (b) (TERM-ignoring suite: a declared limit, behaviour change), KS-1747 (whether it is a defect is the board's call), KS-1746 item 4 (schema default), KS-1463 (no shape prescribed), KS-1589 B and C, KS-1505 part 2, KS-1727 (Opus, carried).
10. **Everything is UNMEASURED where it needs `gh`:** open PRs. I did not run `gh` myself (the 06:15 sweep and your prompt both say it is unusable here); no candidate ticket has a Linear attachment (KS-1746..51: 0; KS-1589, 1463, 1505, 1667, 1738, 1705: 0 PR links read). Every brief's QUEUE 0 measures it under the project's identity.

## 1. Counts

**FOUND** 687 open now; 6 created since 2026-10-26T19:15Z (06:15+11); 687 and 6 were each unique (687 unique ids of 687 nodes, 6 of 6).
**TESTED** Positive controls: type counts and name counts both sum to 687; the createdAt filter discriminates (control: open issues created since 2026-10-12 returned 248, against 6 for the cutoff; KS-999999 returned 0 nodes). Zero control for the cutoff: KS-1746 (created 2026-10-26T23:17:08Z, after the cutoff) is in the six, and the 06:15 sweep's last pre-cutoff ticket KS-1745 (created 14:48Z) is not.
**HOW** Linear GraphQL, `issues(first:25/100, after, filter:{team KS, state.type in backlog/unstarted/started, createdAt gte})` cursor loop until `hasNextPage` false. Comments read with `comments(first:50)` sorted client-side.
**NOT READ** Closed issues except the named ones; comments past 50 (none of the tickets has more than 8).

## 2. The new tickets (KS-1746..KS-1751)

Read in full, description and comments (no comments on any). All Backlog, all assigned to `kamil.kreiser@secuura.ai`.

| key | what | decision |
|---|---|---|
| KS-1746 | five gate LOW/INFO items across four suites (its own scope note) | lane 7 (items 1, 2, 3), lane 6 (item 5), item 4 held; G 23rd splits it |
| KS-1747 | `specRouteMap.ts:47` arms the edge gate only for `bearerAuth`; `GET /api/connector/info` (connectorApiKey only) is unarmed | needs the board: the ticket itself says "whether this is a defect is for the board" |
| KS-1748 | CLASS: module-level `beforeAll` router imports pay the cold Vite transform inside the hook budget; asks for ONE convention decision | needs Kam/Wednesday: "The decision this ticket asks for" is the convention |
| KS-1749 | retire the Schemathesis `unexpected-methods = []` suppression (Kam ruled 405 before auth stands, KS-1358); three places carry the superseded rationale, plus a stale pin path | decided, but not offline-provable: retiring turns ~1,760 probes into coverage and the record has an unexplained `401 x2` tail; needs a sweep on a slot; holds |
| KS-1750 | `pre_push_hook_base_leg_comment.test.sh` grades another suite's comment by three `grep -c -F` strings and the graded file does not say so | lane 6 |
| KS-1751 | kintsugi `anchor_store`: 2 rows `simulated=true` AND `confirmed` (mock_tx_, 2026-08-20), a shape KS-587's Done-when passes over | not a lane item (below); product questions in the ticket are Kam's |

### KS-1751 and the CLAUDE.md correction (FOUND / TESTED / HOW)

**FOUND** The sentence "zero rows are simulated=true AND confirmed" is on line 9 of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md` (the project-folder file, 306 lines, dated 11 Sep), reading "zero rows on demo are (simulated=true, confirmed). Re-measured read-only 2026-08-21 (KS-683)". The repository's own `CLAUDE.md` at c3eb63c9d23b does not contain it.
**TESTED** `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain rev-parse --show-toplevel` fails ("not a git repository"); `git -C .../2_Project_Files rev-parse --show-toplevel` succeeds, and `git ls-files --error-unmatch ../CLAUDE.md` says "outside repository". Control: the repo's `CLAUDE.md` exists at the sha and `git grep -i simulat` finds two unrelated lines (29, 97); `git grep -i confirmed` in it returns nothing.
**HOW** `git cat-file`, `git grep`, `grep -n` on the outer file.
**Consequence:** it cannot ride a lane PR; a seat could edit the outer file directly (it is in the project folder) but with no gate path, and it is the instruction file every seat boots from, so I left it to Wednesday. The measured fact for whoever edits it is Seat D 35th's (relayed on KS-1751, not re-measured by me): 2 kintsugi rows, `transaction_hash` `mock_tx_a6435a40...` and `mock_tx_2081b052...`, created 2026-08-20, `simulated=true`, `status='confirmed'`, `block_number` NULL; instrument: its read-only STATUS A of 2026-10-26T23:13Z with a classifier control (31 real 64-hex, 0 mock among kintsugi's non-simulated rows). Line 9 already scopes the zero to demo, so the correction is "say kintsugi differs", not "the zero is wrong".

## 3. Classification table

Spark-strict = one product file, fix shape spelled, in-process test nearby, not auth/token/credential/security, runner the checker can run. Read at source: ticket (description + comments) and the code it names at c3eb63c9d23b.

| ticket | class | why (the fact that decides) | lane |
|---|---|---|---|
| KS-1746 item 2 | Claude C2 | test comment/assertion text; no fix shape in ticket, builder rewords to what the cell pins; ks1531 file | 7 |
| KS-1746 item 3 | Claude C2 | new source-pin test, mutants per copy; export not allowed (QUESTION) | 7 |
| KS-1746 item 1 | Claude C2 | generator prose + regenerated 40,453-line yaml (checker cannot regenerate); not live until a later deploy | 7 |
| KS-1746 item 4 | needs a decision | `startup-migrations.ts:376` default `'active'`, a different column set than the four other DDLs; ticket names no proving suite | held |
| KS-1746 item 5 | Claude C2 | fixture-hook cell in `preflight_deps.test.sh`; gate mutant G2; fixture machinery exists (`preflight_fixture_run` :283) | 6 |
| KS-1750 | Claude C2 | add a warning comment without quoting the three graded strings (CELL 2 needs exactly 1 hit); or loosen; builder picks | 6 |
| KS-1738 | Claude C2, conditional | A/B/C measured table is the spec; shapes 1 or 2 live, shape 3 ("leave it") ruled out BY THE DRAFTER'S BRIEF, Wednesday may override | 6 |
| KS-1589 A | Claude C2 | test-only, five mutants with named survivors, shape spelled (parse or balanced parens) | 8 |
| KS-1505 part 1 | Claude C2 (comment) | comment block now `index.ts:614-643`; part 2 is a code change with no test, excluded | 8 |
| KS-1667 | Claude C2 (comment), conditional | 3 comment sites; `gdprService.ts` call sites drifted (:435/:558/:949/:1348/:1633); needs the open-PR check on `documents.ts` | 8 |
| KS-1463 | Claude C2 or needs a shape | "Suggested shapes (not prescribed)"; shape 1 (move the test to demo-service) is concrete, but not chosen; not queued | none |
| KS-1705 | needs a client human / a slot | acceptance 3 is a Schemathesis sweep on a running slot; Peter's 2026-10-26T12:53Z comment widens it to 3 more failing checks and says "Classification is open: spec drift ... or a service defect"; KS-1364 (In Progress) may close it as covered | none |
| KS-1749 | needs a slot (decided ruling) | see section 2 | none |
| KS-1747 | needs the board | see section 2 | none |
| KS-1748 | needs Kam/Wednesday | convention decision | none |
| KS-1745 (b) | needs a decision | the TERM-ignoring suite is a declared limit ("Not tested"); a fix escalates the runner's kill (a behaviour change) | none |
| KS-1589 B | not a unit-testable item | `ApiKeys.tsx:98` (ticket said :99); the frontend has no unit tier (KS-1391) and a wall-clock cell is the KS-1324 flake class; also a regex DoS, arguably a security surface | none |
| KS-1589 C | needs Docker | three Playwright cells that need the stack | none |
| KS-1643 nit 3 | needs a design call | caller-read versus internally-assigned; ticket unfiled; G 23rd files it | board |
| KS-1727 | Opus (row C3) | carried from 06:15, not re-read | none |
| KS-1751 | needs Kam/Wednesday | product call on rows; the doc edit is outside the repo | none |

**Already fixed:** none of the candidates. KS-1700 and KS-1531 are Done; KS-1745 stays open (item b); KS-1734, KS-1465, KS-1523, KS-1563 Done; KS-1643 stays open (nits 2, 3).

### Spark-strict, 0 with a control (FOUND / TESTED / HOW)
**FOUND** 0 of the 12 tickets/items read qualify (KS-1746 item 2, 3, 1, 4, 5; KS-1750; KS-1738; KS-1589 A; KS-1505; KS-1667; KS-1463; KS-1589 B).
**TESTED** Each clause fired on at least one named ticket, so the cascade is not blind: one-product-file fails on KS-1746 item 3 (new file plus a read of two others), KS-1738 (3 files), KS-1589 A; fix-shape-spelled fails on KS-1750, KS-1738 (3 shapes), KS-1746 items 2/3 ("nothing here is a fix"); security surface fails on KS-1589 B (regex DoS) and KS-1746 item 4's neighbours; runner-the-checker-can-run fails on KS-1746 item 1 (needs `generate-openapi`, 40,453-line yaml) and KS-1589 B (no frontend unit tier); `doc_patch` not wired fails KS-1505 and KS-1667 (comment-only). No known Spark-qualifying ticket exists, so a positive control for the whole cascade is absent: treat the 0 as a hand read, not an instrument.
**HOW** Read each ticket whole; read the named lines with `git show c3eb63c9d23b:<path>`; applied the predicate in `model-routing.md` section 3 as quoted in the 06:15 report.
**NOT READ** The other ~340 open Backlog/Todo ticket bodies (the 06:15 sweep read titles of 358 and full text of ~45); I did not recount.

## 4. Open-PR overlap

**Used:** Linear attachments (all candidates 0) and develop's git history (`git log -1 --format ... c3eb63c9d23b -- <path>` for every granted path). **Not used:** `gh`: I did not run it; the 06:15 sweep recorded `gh auth status` not logged in and the unauthenticated API 404 on the private repo, and the 22nd Seat G found the launcher's `GH_CONFIG_DIR` logged out. So **open PRs are UNMEASURED**.
**FOUND** Last commits touching the granted paths (all merged, newest first): `preflight.sh` and `preflight_deps.test.sh` d766f6dfd (#1733, 10-27); `pre_push_hook_base.test.sh` 1b550684f (#1729, 10-27); `pre_push_hook_base_leg_comment.test.sh` 3916eacd1 (09-22); `generated_guard.sh` 5f6899918 (10-26); `api-gateway.openapi.ts`, ks1531 test and yaml c3eb63c9d (#1732, 10-27); `m365-integration.openapi.ts` 7ae92bbb6 (#1725); `ks1564...test.ts` a7cffc8d9 (10-13); `index.ts` (api-gateway) 20ee6605b (#1702, 10-26); `documents.ts` (originate) 28e2d27de (#1690, 10-26); the ks1662 test 115797747 (10-19). Nothing newer than the 10-27 morning merges.
**HOW** the briefs' QUEUE 0 puts the `gh pr list --json files` intersection first.

## 5. The lanes

All Sonnet C2 (model-routing row C2; gate tier 1 or 2 per the G rows, which I did not re-read). Every file path below was checked with `git cat-file -e c3eb63c9d23b:<path>` (outputs listed in each brief; all rc=0, plus one deliberately-absent new-file path rc=128).

| lane | letter | brief | owns (edits) | read-only |
|---|---|---|---|---|
| 6 shell residue | **R** | `2026-10-27_seatR_lane6_shell_residue.md` | `scripts/__tests__/preflight_deps.test.sh`, `pre_push_hook_base.test.sh`, `pre_push_hook_base_leg_comment.test.sh` (only if loosening), `systemTest/__tests__/support/generated_guard.sh`, `systemTest/__tests__/bootstrap_login_diagnosis.test.sh`, `systemTest/__tests__/generated_guard_restore.test.sh` | `preflight.sh`, `.githooks/pre-push`, `run-shell-suites.sh`, `pre_push_hook_base_fixture_guard.test.sh` |
| 7 contract + m365 pin | **S** | `2026-10-27_seatS_lane7_connector_contract_and_m365_pin.md` | `services/api-gateway/src/api-gateway.openapi.ts`, `.../__tests__/ks1531-connector-info-is-in-the-published-contract.test.ts`, `docs/openapi/secuura-api.yaml` (generated), one NEW test under `services/m365-integration/src/__tests__/` | m365 `index.ts` and `*.openapi.ts`, `generate-openapi.ts`, `auth.ts`, `health.ts`, `specRouteMap.ts` |
| 8 comment truth + shared pin | **T** | `2026-10-27_seatT_lane8_comment_truth_and_shared_pin.md` | `packages/shared/src/__tests__/ks1564-admin-api-keys-page-sends-no-default-org.test.ts`, a comment block of `services/api-gateway/src/index.ts` (~:614-643), comment blocks of `services/originate/src/routes/documents.ts` (~:1955-1975), the header of `ks1662-tenant-predicate-without-rls.integration.test.ts` | `ApiKeys.tsx`, `walkTimeouts.setup.ts`, `gdprService.ts`, `adminConfig.ts`, `db.ts` |

**Disjointness:** the three owned sets share no path (checked). **api-gateway is shared at service level between S and T** (S: openapi file, ks1531 test, yaml; T: `index.ts` comment block): stated in both briefs, with each seat told it never edits the other's file. Seat D 35th: no code. Seat G 23rd: no repo write.

**Why these three letters:** W, X, Y are absent from `inbox_routing.conf` (grep for `Blockchain-(W|X|Y)|` = 0; for `(R|S|T)|` = 3), and the prompt's own rule says use R, S, T, U, V then. I used R, S, T; U and V stay free for a third wave. File names do not clash with the five existing `seat{R..V}_lane1..5` briefs (new ones are `lane6..8`).

**Best-value order:** R first (gate-found residue of code merged this morning, every fix with a red-first mutant and a runner that runs offline), S second (it touches the published contract: the yaml needs a later deploy, so its value is lower per hour), T third (comment-only and test-pin work; KS-1667 conditional on the PR check).

### Seat G 23rd (board)
Brief `2026-10-27_seatG23_board_followups.md`.

**KS-1746 split (read at source, whole, 10,963 characters).** Items as the ticket numbers them and the pass that proves each (the ticket names four suites in its own scope note; the item-to-suite mapping is mine, from each item's files and commands):
- item 1 (401 description) -> OpenAPI contract-conformance (`generate-openapi`, `check:openapi`): new ticket B
- item 2 (U2 cell text) -> api-gateway unit: new ticket A
- item 3 (m365 enum pin) -> m365-integration unit: new ticket C
- item 4 (DDL default `'active'`) -> the ticket names no suite ("a source read only"); provisional api-gateway unit (`ks1062-...startup-migrations...` and `ks1125-...startup-migrations...` exist at the tip): ticket A, the seat verifies or asks
- item 5 (nit-2 filter cell) -> shell/preflight: **stays in KS-1746** (KS-1643's comment already says nit 2 "is now filed as KS-1746, item 5")
- The ticket's original sixth item (`allowedDocumentTypes`) was already moved to KS-1534 item (b) by G 22nd.

**KS-1643 nit-3 board search (FOUND / TESTED / HOW).** FOUND: no ticket covers it. `${NAME:?}` 1 hit (KS-1643), `NAME:?` 1 (KS-1643), `hook_controls` 1 (KS-1746), `caller-read` 1 (KS-1643), `hook controls` 4 (KS-772, KS-1634, KS-1638, KS-1643), `read from the caller` 2 (KS-772, KS-1643), `nit 3` 4 (KS-544, KS-1385, KS-1643, KS-1746), `bare $NAME` 0, `assigns itself` 0. KS-1634 and KS-772 contain the phrase only as quoted log text/digest. TESTED: controls fired in the same session: `KS-1531` 12 hits, `run_shell_suites` 42 hits; zero control `zzqz-wed-ctl-4417` 0 hits, against the dead old token `zzqqxx-no-such-symbol-9931` which returned 7. HOW: `issues(includeArchived:true, filter: team KS and (title OR description OR any comment body containsIgnoreCase))`, paginated (every query one page of 50, hasNextPage false).
Facts measured at the tip for the ticket (git show/grep, not run): the derived set is [ALLOW_FORCE] from the single `${NAME:-` ALL-CAPS read at `.githooks/pre-push:77`; the hook assigns `ZERO=` at `:52` and reads it bare as `$ZERO` at :60, :61, :113 (the code comment's own "assigned internally" example).

**Duplicate triage:** 0 proven. Pair table is in the brief. The one overlap is KS-1746 item 5 and KS-1643's nit 2 (same residue in two open tickets): double tracking, not a duplicate ticket.

## 6. What I did NOT read or do

- **Open PRs (see section 4).** `gh` not run by me.
- Gate verdict files under `0_Brain/reference/2026-10-27_gate-*`; model-routing G rows; any PR diff; Linear state history; `history.md` (seat ordinals are UNVERIFIED in every brief and the briefs say so); `docker`, boxes, Seat D 35th's handover.
- `migrations/039_rls_fail_closed.sql` lines 156-157 (the lane 8 brief tells the seat to read them); the evidence files of KS-1505 under `5_Project_History/2026-10-12_seatD-18th/`; KS-659's board state.
- `systemTest/schemathesis` files for KS-1749 beyond what its ticket quotes (the drafter did not open them; it classified from the ticket and a last-commit read on `schemathesis.toml`).
- Label/project/priority values of KS-1746..KS-1750 (the G 23rd brief tells the seat to read a template).
- I did not execute any test, mutant, build or script. Every file:line cite is `git show c3eb63c9d23b:<path>` or `git grep` in the cache clone; counts I derived (ks1531 has 7 `it(` lines, the ks1564 file 9, the yaml 40,453 lines, `runWithPlatformScope` 29 matches) are text counts, not run results.

## 7. What Wednesday has wrong in this prompt (and in the neighbouring briefs)

1. **KS-1751's CLAUDE.md fix is not a repo change.** The file is outside the git repository (section 2). Did not fit a lane; reported instead.
2. **"Lanes routed in inbox_routing.conf are B, D, G, R, S, T, U, V"** omits C, E, F, J and BOARD, which are also routed. The W/X/Y premise holds (none routed).
3. **The G22 brief's claim that one test pass proves its six items** is contradicted by KS-1746's own scope note (four suites); the prompt's "KS-1746 spans four suites" is right.
4. **The `zzqqxx-no-such-symbol-9931` zero control** that every G-seat brief carries is dead (7 hits); the nit-3 search and any new G brief need a fresh token.
5. **The 06:32 lane briefs' identity line** (`git config user.*` in every worktree) contradicts STANDING_LINES (Seat V 2nd).
6. **KS-1738's "conditional" is not resolved anywhere:** I queued it in lane 6 on a stated reading (shapes 1 or 2 live, shape 3 out). If Wednesday disagrees, drop item 3 from the R brief before pasting.
7. **Pane ids:** the newest standing line (Seat D 35th) wants each brief's first line to carry the pane id; I cannot know it, so each brief says "Wednesday fills it in". Seat ordinals are likewise placeholders `<N>th`.
8. **The prompt said KS-1746..KS-1751 were filed by "Seat G 22nd this morning" and asked for tickets created since 06:15+11:** exactly six exist; no ticket numbered above KS-1751 existed at 11:2x.
