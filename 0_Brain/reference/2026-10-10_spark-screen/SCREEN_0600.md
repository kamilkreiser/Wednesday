# KS screen for the Spark, 06:00 delta: 1 ticket fits (KS-1456), drafted two ways (rung 2 exact, rung 6 loose); the rest of the backlog does not

Written 2026-10-10 06:1x AEDT (shell `date`; Linear read 06:03, open-PR census 06:05) by a screening and brief-writing sub-agent for Wednesday. Commission: Kam 2026-10-09 23:12 "keep pushing harder and harder tickets to the spark as a way of testing it". Secuura only. Method template: `SCREEN_0040.md` (same folder). Rules: `learnings/2026-09-23_spark-kit-running-a-local-coding-model.md` (selection predicate, brief shape, checker contract, counter) and `learnings/2026-09-25_spark-calibrate-like-ornith-start-high-oversight.md` (ladder).

**Read-only on every external system.** Linear: GraphQL queries only (key sourced transiently from the Blockchain `4_Credentials/.env`, never printed or written). GitHub: REST GET only (open PRs and their files; token from the same `.env` in a subshell, scratch `GH_CONFIG_DIR`). Code: `git show 613070f29112:<file>` and `git grep ... 613070f29112` against the Secuura checkout, nothing else (no fetch, pull, checkout, worktree, commit; no `cd`). The checkout's own HEAD is `1fba82dd...`, NOT the tip; every line number below was read at `613070f29112a40a0d8d9684cd50c7c2ae54592c` (develop, 2026-10-10 "KS-1402: originate resolves a transfer-custody holder email itself"). Files were measured in scratch copies written with `git show`. Nothing queued, no model run, no `round.sh` (it writes `spark/state/`), no mail, no tmux, no commit, nothing deleted, nothing written under `!CODING/`. Only `brief_lint.py` (read-only) was run, on both drafts: rc 0.

## BLUF

1. **One ticket fits the predicate: KS-1456** (run-migrations.sh failed-run message, `:187-188`). Drafted twice from the same ticket, same new test, same hand-derived golden:

   | draft dir (under `drafts_0600/`) | rung | what is hard | status |
   |---|---|---|---|
   | `KS-1456-run-migrations-failed-run-message/` | **2** bash_patch: one product hunk (2 lines to 1), every line spelled, plus a new 92-line stub-PATH suite given whole | easy: this is the "ladder floor" for tonight, easier than KS-808's 3 hunks | DRAFT, NOT QUEUED |
   | `KS-1456-run-migrations-failed-run-message-loose/` | **6** bash_patch: NO line number, NO quoted product text, NO hunk for the product file; behaviours plus the whole test | the model must find the two `echo` lines in a 201-line script from prose, keep the sentence grammatical, and not over-reach | DRAFT, NOT QUEUED |

   **Queue ONE of the two, never both** (same ticket, same golden). Red-first/golden figures (scratch tree, bash 3.2): new suite at the tip **rc 1, 3 passed / 1 failed** (the failing cell is the one named for the defect); with the golden **rc 0, 4/4**. Sibling suites at tip vs golden: `run_migrations_failure_exit_code` **7/7 both**, `ks808_run_migrations_counts_skips_apart` **5/5 both**. `git apply --check` STRICT on a scratch repo holding the tip file: rc 0; reverse check rc 0; applied files byte-equal to the hand-edited ones. `sh -n` rc 0. `brief_lint.py`: rc 0 on both.
2. **No second ticket and no genuinely multi-file ticket survived.** Kam asked for harder rungs; the backlog cannot supply one at this tip (see WHY THE POOL IS THIN). The harder rung offered is the *looser brief* form (rung 6) of the one real ticket. The harder briefs that already exist and are not yet used: `night/briefs/KS-1432-apigw-documents-body-predicate-export/` (rung 5, multi-file, loose; written 01:06, NOT queued because KS-1432 already has a held rung-1 PASS: raise that or queue this, never both, per the `queue.md` 01:1x note), which is the right next climb if Wednesday wants a rung above 2 that is not a loose rewrite of a one-line text fix.
3. The candidate is a text fix, so a PASS tells us little about capability beyond "finds and edits two echo lines without breaking a branch"; the loose variant is what measures anything (rung 6 finding behaviour from prose).

## FRAME: tickets read, states, filters, counts, controls

- **Enumerated:** Linear GraphQL, team `KS`, state type in `backlog, unstarted, started`, `first:100` with `pageInfo`, paginated until `hasNextPage=false`: **6 pages, 509 tickets** (Backlog 245, In Progress 217, Todo 29, In Review 13, Blocked 5). Control: In Progress **217** equals the 00:40 screen's count and `board_count.sh`'s certified figure; the total is **+1** vs 00:40's 508 (the new ticket is KS-1456 itself, filed by R27's follow-up). Comments connection used `first:50`, sorted client-side.
- **Waterfall (ordered; each row is what that filter removed from what was left):**

  | step | removed | left |
  |---|---|---|
  | open KS tickets | | 509 |
  | the 14 named live/just-raised lanes (KS-1345 1346 1410 998 937 1432 1402 808 1355 1328 1449 1148 1250 1175) | 14 (all 14 were in the open set: a control that the list matches the board) | 495 |
  | assigned to Peter (18) or Stuart (8) | 26 | 469 |
  | In Review (13) and Blocked (5), net of the above | 15 | 454 |
  | title keyword for an auth/credential/security surface or a decision card: `auth, mfa, oauth, token, credential, secret, password, jwt, session, decid(e/ion), policy` | 111 | 343 |
  | already named in a `night/briefs/` dir, a `night/READY_*` file, a `night/_quarantine_*` file, a `spark/briefs_*` dir or a `spark/done.md` row (215 ticket numbers) | 108 | **235** |

- **Control on the title filter:** all 111 keyword-excluded titles were read in full (not just counted). Eleven looked like false positives by title (KS-1351, 1124, 1074, 1158, 1225, 1131, 1139, 1360, 1357, 759, 855). Bodies read for 1351, 1124, 1074, 1158: all already merged. The rest judged from title and ticket text only: 1139 (already a done.md PASS, 10-07), 1225 and 1131 (auth-service test files), 1360 and 1357 (response fields on the wallet-session and OAuth routes), 759 and 855 (JWT and OAuth types). None was a fit.
- **Control on the prior-art filter, and a gap it has:** it is by ticket number, so it removed KS-1136 and KS-808 but NOT KS-1436, whose fix appears to be the held READY `KS-1136-06-TENANT-STDERR-OWN-FILE-1` (same file, same defect, different number). Verified at the tip: `Blockchain/Testing/jobs/06-tenant-isolation.sh:71-74` already carries the KS-1436 fix. See Harness findings 1.
- **Descriptions read: 92 distinct tickets** (the first 1.3-9K characters; KS-1451 and KS-1382 whole), chosen from the 235 survivors by fix-shape keywords and service paths, plus the false-positive titles above. Comments read (last three, sorted) for the same set. The other 143 survivors were screened on title and on a mechanical pass (below).
- **Mechanical pass over all 235:** a description citing a `services|packages|scripts|connectors|frontend/<path>.<ext>:<line>` = **57**; of those, none of "decide / not chosen / your call / owner's call / a ruling / question / survey / audit the / measure first / unmeasured" = **22**; of those, no comment saying "merged to / squash / MERGED" = **11**. Those 11: KS-1456, 1392, 1218, 1113, 1105, 752, 678, 581, 580, 579, 526. Read at source, **1 passes** (KS-1456). The other ten: 1218, 1113, 1105, 752 and 1392 are in the table below; 678 is a spec-example synthesiser with a published-URL decision; 581, 580, 579 and 526 are platform-admin / key-custody design on `platform.ts` and `anchoring` (security surface, and design not task).
- **Open-PR collision census (GitHub REST GET, 06:05 AEDT): 26 open PRs, 133 file entries.** None touches `run-migrations.sh` or `scripts/__tests__/run_migrations_*` (0 hits for `run-migrations|run_migrations`; the one `migrations` hit is #1383's migration 049). Positive control: the census finds `run-shell-suites.sh` and `run_shell_suites.test.sh` on #1250 (so KS-1302/1303/1324/1331 are blocked). Negative control: a nonsense filename returns 0.
- **Staged-lane check:** `fleet/briefs_staged/` greps for `run-migrations` and `KS-1456`: only R27's wrap asking for KS-1456 to be FILED (it is: Backlog, board account) and J1's note that KS-808's PR touched this script. No seat holds KS-1456.
- **Not checked:** live seats' unpushed work on these files (only PRs and staged briefs); whether the 486 `READY_*` files in `night/` were ever raised.

## Candidate table (the survivors that reached a source read, and why each does or does not fit)

Predicate clauses: **P1** one product file · **P2** the ticket spells out the fix shape (no "decide whether") · **P3** a runnable in-process test nearby to copy · **P4** not an auth/token/credential/security surface · **P5** not already at the round counter / not already shipped or held · **P6** a runner the checker can run (vitest/jest/bash in-process) · **P7** no open-PR/lane collision.

| ticket | file(s) at 613070f29112 | proposed rung | verdict, by clause |
|---|---|---|---|
| **KS-1456** | `Blockchain/Dev/scripts/run-migrations.sh:187-188` + NEW `scripts/__tests__/ks1456_...test.sh` | **2** exact / **6** loose | **FIT.** P1 one product + one new test; P2 ticket says "text only, the two echo lines at :187-188, exit code and counting stay"; P3 `ks808_run_migrations_counts_skips_apart.test.sh` and `run_migrations_failure_exit_code.test.sh` stub psql/pg_isready on a private PATH; P4 an echo in a migration runner; P5 round 0, Backlog, no READY; P6 bash, ran in scratch; P7 0 of 26 PRs. |
| KS-1436 | `Blockchain/Testing/jobs/06-tenant-isolation.sh:71-74` | none | P5 FAIL: already shipped at the tip (`2> "$OUT.stderr"`, comment "KS-1436"); also a held READY under KS-1136-06. Stale board state. |
| KS-1324 | `scripts/__tests__/run_shell_suites.test.sh` (test-only edit) | none | P7 FAIL (#1250 edits it); no product file, test-only is not wired in `round.sh`. |
| KS-1331, 1303, 1302 | `scripts/run-shell-suites.sh` | none | P7 FAIL (#1250 is the open PR for 1302+1303); 1331 is signal handling (process-group forwarding), the runner's traps are in that same PR. |
| KS-1340 | guard inside a `beforeAll` of `ks597-issuer-organization-id.integration.test.ts:61-77` | none | P6 FAIL: the guard is in a DB-backed integration suite's setup; no in-process cell can drive it; fix shape "not chosen" in the ticket. |
| KS-1382 | five `Blockchain/Testing` shell scripts | none | P2 FAIL: "Kamil's call", sourcing `stack_env.sh`, a shared static guard owned jointly with KS-1355/1381/1389/1162, and an unresolved workflow decision (KS-1162). Five-ticket coordination, not a task. |
| KS-1451 | five slot-literal guards (bash, 2 TS, Python, Akto TS) | none | P1/P6 FAIL: five implementations in three languages that must change together; the ticket says a one-guard fix is wrong. Under `systemTest/` (Peter's authority). |
| KS-1454 | `anchoring/src/anchorSchema.ts` + CIP-674 metadata + read-back + verify | none | P1 FAIL (4 work items across anchoring/originate); P4 on-chain metadata minimisation ("if K's minimisation review disagrees, say so before building"); the schema-only slice would accept the field and not anchor it, which is the exact failure the ticket warns about. |
| KS-1424, 1419 | `repositories/documentRepo.ts` + 13 callers | none | P2 FAIL: "separate the two meanings" (discriminated result OR a re-read) and "needs its own decision" in the ticket. |
| KS-1213, 1385, 1304, 1263 | `originate/src/routes/documents.ts` | none | P2 FAIL: shape ratified by neither the ticket nor a ruling (1213 "decide the fix shape"), or multi-write transaction design (1263). The #1437 collision that blocked these at 00:40 is gone (not among the 26 open PRs). |
| KS-1296, 1204, 1155, 1319, 1293, 1291, 872, 1351, 1124, 1074, 1158, 934, 1311, 679 | various | none | P5 FAIL: In Progress only because a runtime/live-sweep residue is owed; the code change is merged (squash SHAs in each ticket's comments). |
| KS-1443 | `systemTest/__tests__/bootstrap_login_diagnosis.test.sh`, `run_migrations_failure_exit_code.test.sh` Cell 5 | none | P1/P6 FAIL: tests only (no product file) and the failure exists only on a Linux runner, which cannot be reproduced on this Mac to prove red-first. |
| KS-812 | `connectors/whatsapp-bot/src/index.ts:21` | none | P3 FAIL: the connector has no test directory, no test runner and no entry in the tip's tree besides `src/` and the lock; "repoint or drop the fallback" is also a choice. |
| KS-1394 | `scripts/audit/audit-locks.mjs:352` message | none | P3 FAIL: no test drives `audit-locks.mjs`; the ticket's second problem (`--package-lock-only` does not move a pin) makes the message itself a content decision. |
| KS-1105 | `frontend/admin/src/pages/Login.tsx:81` | none | P4/P6 FAIL: the admin login page of the auth surface; no frontend declares a `test` script (KS-1391). |
| KS-1113, 1010, 1039 | `tests/e2e/...spec.ts` | none | P6 FAIL: Playwright against a live stack. |
| KS-752, 1218 | `systemTest/schemathesis/scripts/run.py`, `constraints.txt` | none | P6 FAIL: Python harness with no in-process runner wired here (cf. 00:40's KS-1447); under `systemTest/`. |
| KS-1306, 1423, 1297, 1332, 1300, 1314, 1316, 1319 | test files, guard ASTs, integration cells | none | P1/P6: test-only edits to guards, or DB-backed integration suites; the guard-AST tickets (1314/1316/1332) are the "reader must discriminate" kind (fix shape = a new AST reading), and PR #1253 is open for 1297. |
| KS-1377, 1256, 1189, 1176, 1174, 1119, 1372, 1433 | `security`, `api-gateway` | none | P4 FAIL: API-key validation, connector allow-list, rate-limit lockout, verify hashing: credential/auth surface. |
| KS-1427, 1114, 1112, 1243, 1249, 1072, 1334 (5th), 1322 | various | none | P2 FAIL: "ruling for you", "decide", "the owner's call". |
| KS-1453, 1399, 1400, 1425, 1437, 1378, 1403, 1211, 1224, 1154, 1317, 846 | `package.json` / lockfiles | none | P6 FAIL and push-freeze lane: lockfile and dependency edits, advisories (a lane of its own). |
| remaining ~170 survivors | | | Reviews/roll-ups/gate-record residues (KS-1420, 1415, 1412, 1418, 1343, 1307-1309), docs (604-605, 603, 602), infra and CI (1392, 1138, 1012, 1076), launchers outside the repo (655, 939, 940, 911, 912), designs (KS-1384, 1200, 1336, 1055), epics (485, 491, 770-772). Read by title; none has a P2 fix shape in a single in-process-testable file. |

## Top fits, ordered by rung

1. **KS-1456, rung 2 (exact)** - `drafts_0600/KS-1456-run-migrations-failed-run-message/` (`KS-1456.md`, `golden.diff`, `spark.pins`). Edit points: 1 product hunk (`:187-188` two lines to one) + 1 new test file = 2 files. **DRAFT, NOT QUEUED.**
2. **KS-1456, rung 6 (loose)** - `drafts_0600/KS-1456-run-migrations-failed-run-message-loose/`. Same ticket, same test, same golden (reference only; the product wording is the model's, so `golden DIFFERS` for the product file is the expected outcome and not a fail). **DRAFT, NOT QUEUED.** Queue this one instead of the rung 2 if the point is to measure; queue the rung 2 if the point is a quick candidate for raising.
3. **(not a new draft) `night/briefs/KS-1432-apigw-documents-body-predicate-export/`** - rung 5, multi-file, loose; written 01:06 by the 00:40 screen, dry-run rc 0, parked because KS-1432 has a held rung-1 PASS. If Wednesday wants a real harder rung tonight, this one exists; its golden was verified by its writer (00:40), and Wednesday has not read it yet.

Both KS-1456 drafts deliberately went under the reference folder, not `local-model/spark/` or `night/briefs/`: the canonical home is `night/briefs/<ticket-slug>/` (outside the write scope), `spark/briefs_<date>_<name>/` is a second precedent, and a draft that has not been dry-run falls under the commission's "if in any doubt". To queue: copy the chosen dir to `local-model/night/briefs/KS-1456-run-migrations-failed-run-message/` (Wednesday, after reading the golden), then run `round.sh <dir> --dry-run` and `--control` (neither done here).

## WHY THE POOL IS THIN

- **509** open; **235** after assignee / state / lane / auth-keyword / prior-art filters; **57** of those cite a file and line; **22** of those with no decision wording; **11** of those with no merged-PR comment; **1** that survives a source read and the 26-PR census. The wall is not the filters, it is that the backlog's remaining content is overwhelmingly (a) residue of work that already merged and is waiting on a live sweep (14 In Progress tickets read: 1296, 1204, 1155, 1319, 1293, 1291, 872, 1351, 1124, 1074, 1158, 934, 1311, 679), (b) gate-record roll-ups ("six Minors carried forward"), (c) cards whose own text says "decide" or "the owner's call", (d) harness, CI, lockfile and advisory work with no in-process runner, and (e) the auth/credential/security surface the commission excludes.
- **Product-code tickets with a spelled-out shape are consumed faster than they are filed.** Since 10-05 `spark/done.md` holds 53 rounds (47 PASS); every ticket-shaped product fix the 00:40 screen found has been briefed and run. 00:40 already said "the honest residue for the Spark on this board is close to exhausted"; this screen confirms it: **the one ticket filed since 00:40 (KS-1456, apparently filed from R27's follow-up 3) is the one that fits.**
- **Collision removed but nothing unlocked.** #1437 (the `documents.ts` PR that blocked KS-1291/1419/1424/1263/1304 at 00:40) is no longer open, but those tickets then fail P2 (shape not chosen) or P5 (already merged), so the unlock yields no new fit.
- **What would widen the pool:** (a) more `started_ok` accepts for In Progress tickets whose only open item is a live sweep (not a code item, so no gain), (b) re-briefing HELD PASSes in looser shapes as 00:40 proposed (their goldens exist; the held ones now number 486), (c) wiring `test_only` into `round.sh` (many gate-record tickets are test-only edits), (d) a Python/pytest tier for `systemTest/schemathesis` (KS-752, KS-1218, KS-1447), (e) a decision from Kam on whether Peter's `systemTest/` tickets assigned to the board account may go to the Spark.

## HARNESS FINDINGS

1. **The prior-art gate is by ticket number, so a duplicate under another number slips through.** KS-1436 (06-tenant-isolation stderr) is the same defect as the held `READY_KS-1136-06-...` and is already merged, yet it survived the number filter and stayed In Progress on the board. Same class as 00:40's KS-1432 finding. A content-level check (grep the product file's line at the tip for the ticket's own key, e.g. `KS-1436` in `06-tenant-isolation.sh:71`) found it in one command; worth adding to the screen as a standing step: for every candidate, `git grep -n "<KS-key>" <tip> -- <file>` before drafting.
2. **A ticket's "In Progress" state is not a signal for or against.** At least 14 of the 217 In Progress tickets (the 14 above) are In Progress only because a post-merge live sweep is owed (comment text: "NOT Done per secuura-test-discipline 5f - live sweep owed"). The screen has to read the last comment to tell, which costs most of the reading. The board has no field that separates "work open" from "sweep owed"; a label would turn the 217 into a count that means something.
3. **`brief_lint.py` checks shape only.** It passes a brief whose product hunk does not apply, whose test fence differs from the golden, or whose `ref=` pin names a file that does not exist. The brief generator therefore has to assert those itself; mine did (fence vs test file `cmp` equal; golden `git apply --check` strict, forward and reverse). A lint warning for "golden.diff present: does `git apply --check` pass against the Tip: file?" would catch the commonest drift, and `round.sh --dry-run` only catches it after state is written.
4. **The checkout is not at the tip and the tip is not named anywhere.** The Secuura checkout's HEAD is `1fba82dd...`; the commission names `613070f29112`. Anything done with a working-tree read (a `grep`, `cat`) would silently read the wrong tree. Reading via `git show <sha>:<path>` and `git grep <sha>` was the only safe form. The 00:40 screen made the same point by cloning; with read-only git verbs only, the rule is "never read the working tree".
5. **`pretooluse_no_cd.sh` matches the two letters, not the command.** Twice a whole Bash call was refused (nothing in it ran, including heredoc writes): once for a real `cd`, once for a scratch helper merely NAMED `cd_safe`. The refusal text points at the command, not the name, so the second one took a moment to see.
6. **The previous screen's convention is not documented for where drafts go.** the `queue.md` header says queue lines resolve against `night/briefs/`; `spark/briefs_2026-10-08_harder/` exists as a second convention; the commission allows a third (reference folder). One sentence in the README on which is canonical for a not-yet-queued draft would remove the doubt.
7. **`board_count.sh` still cannot count above 250** (00:40 finding 7); my 509 and 6-page count are from my own paginated query, with the In Progress 217 cross-check.

## UNMEASURED

- `round.sh --dry-run` and `--control` for both drafts (they write `spark/state/` and `runs/`, outside this commission). The builder (`build_bash_input.sh`) has not read either brief: whether the `ref=` and `test_file=` pins resolve, and the `Tier:` / `Runner:` header parse, are owed. `brief_lint.py` rc 0 on both is the only harness contact.
- No real PostgreSQL, no compose `migrations` service: psql and pg_isready are stubs (the KS-1031 and KS-808 suites' method). The failed-run text was never read in a live container log.
- Whether a model given the loose brief finds the right two lines: that is the experiment, not a measured fact.
- The 143 survivors not individually opened were screened on title and the mechanical pass; a ticket whose title hides a fit could have been missed. The mechanical pass requires a `path:line` in the description; a good ticket that names a symbol but no line would not be found by it.
- The 14 live lanes were taken as given by the commission; I did not re-verify their state.
- Description reads were partial (first 1.3-9K characters) for 92 tickets.
- Live seats' unpushed work on `run-migrations.sh` was not checked; only open PRs and staged briefs.
- Judgement calls to confirm: KS-1456's new wording drops "the remaining ... defect is KS-808." and leaves the `# KS-808 (3)` source comment (`:190-196`, "KS-808 carries what is left") as is; the ticket scopes the edit to the two echo lines. Not approval-class (no prod, money, external comms).

## Scratch (session scratchpad, not durable)

`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/45262932-2aa6-4254-821d-057e81431f6a/scratchpad/`: `q/ks.json` (the 509 tickets with 50 comments each), `q/rows.txt` (the 235), `q/prs.tsv` and `q/prfiles.tsv` (26 PRs, 133 file entries), `w1456/` (tip copies, edited file, new test, `golden.diff`), `fetch.py`, `filt.py`, `mech.py`, `mk1456.sh`, `mkbrief.py` (the generators: fences copied from the golden and the test file, never retyped).

Draft files written (sha256 first 16):

| file | sha256/16 |
|---|---|
| `drafts_0600/KS-1456-run-migrations-failed-run-message/KS-1456.md` | `a0b7f550fe25d821` |
| `drafts_0600/KS-1456-run-migrations-failed-run-message-loose/KS-1456.md` | `597433559e1f21ee` |
| `golden.diff` (identical in both dirs) | `09e903c53a5d5901` |
| `spark.pins` (identical in both dirs) | `b2cb13d4d5b0d35a` |
