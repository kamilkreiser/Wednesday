# KS screen for the Spark — 2026-10-05

Written 02:32 AEDT 2026-10-05 (shell `date`; daylight saving began 2026-10-04, so the shell says AEDT, UTC+11) by a Spark brief-writer sub-agent for Wednesday (seat 8e88f5e9, Secuura scope). Authority: Kam 2026-10-04 (*"do as much work with the spark and claude agents on the secura projects as you can"*), the three-tier routing rule (2026-09-25) and the Spark kit counter (original + ONE rebrief, then Opus 5.5).

**Read-only on the client systems:**
- Linear was read over GraphQL with the Secuura Blockchain project's `LINEAR_API_KEY`, sourced by name from its `4_Credentials/.env` and never printed. No mutation, no comment.
- GitHub was read with REST `GET` (`/branches/develop`, `/pulls?state=open`, `/pulls/N/files`, `GH_TOKEN` from the same file) and `ls-remote` (the deploy key, in the scratch clone's `core.sshCommand` only).
- Nothing was written under `!CODING/`. The Blockchain checkout reads 0 tracked-modified lines (`git status --porcelain --untracked-files=no`) and its HEAD is still `c56dd7c32`. Its `.git/FETCH_HEAD` carries a 02:26:57 mtime: that is NOT this sub-agent (whose only fetch ran in its scratch clone at 02:10:03, `src/.git/FETCH_HEAD`). Two Blockchain launcher seats were live in `ps` (started 01:52 and 02:21).
- Nothing was raised, pushed, merged, posted or mailed.

## BLUF

1. **What was screened** (at develop `2d85b84e1012`, as expected: #1374, KS-1402, merged 2026-10-04T14:30:25Z):
   - **Delta: 3 tickets** (`fleet/board_count.sh`, `team KS, state.type in [backlog, unstarted], updatedAt gt 2026-10-02T20:00:00Z`: TOTAL=3, a real count against the 250 limit). All three were CREATED inside the window, so there is no old ticket with a content change (thin, as the 10-03/10-04 sweeps predicted). **Positive control:** KS-1404 is known to be new (it is Seat D's lane) and it is in the 3, so the filter fires. Same instrument, all states: 5 (adds KS-1402 and KS-1403, both In Progress).
   - **The named candidate KS-1388 §1**, read in full at source.
   - **A full-board one-file-carve pass:** Backlog 244 + Todo 33 = **277** (`board_count.sh`, both real counts; the paginated pull returned 277 nodes). A scripted pre-filter (`rank.py`, filed here) excluded 149 (commission IDs 9; Peter/Stuart 24; a security/auth-shaped TITLE 130; overlapping). Of the 128 left: **14 read in full this session**, 106 carry a prior screen verdict (09-26 to 10-02) with no change since (the delta above is empty for them), and 8 were never named before and are all non-code by title (KS-305, 339, 582, 602, 603, 604, 605, 767: a DPA, an access grant, `[Decision]`s, business-model notes, stakeholder docs). **The pass is exhausted at 2 briefable tickets.**
2. **Spark-briefable: 2 tickets, 3 carves.**
   - **KS-1345 (GET / list half):** one product file (`services/originate/src/routes/webhooks.ts`), the ticket's own fix shape ("drop the `.catch`"), and the ticket's own regression cell (flip `control KS-1341 A0`) in an existing jest file.
   - **KS-1388 §1, as two one-file carves** (`observability/.env.example:47`, `observability/config/alerting.env.example:55`; `:6882` → `:80`, the ticket's spelled fix). A failable in-process test DOES exist: a new cell in `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh` (the KS-971 suite that already guards this exact host-port mistake for Prometheus). The 10-02 verdict ("2 files, no failable test") is superseded on both clauses: split per file, and a bash cell that goes red at the tip.
3. **Rounds: 3 Spark rounds, 3 PASSES on round 1, all BYTE-IDENTICAL to the golden** (`cmp` rc 0; hold_ready "golden: BYTE-IDENTICAL"). No rebrief needed. Thinking off, temperature 0, one request at a time, `done_reason=stop` each.

   | Carve | Tier | Verdict | Wall | Prompt / completion tokens |
   |---|---|---|---|---|
   | KS-1345-list | code_patch (jest) | PASS 7/7 strict + A2a; red 1/9 → 9/9; originate suite 1062 → 1063, 0 failed; tsc rc 0 | 45.67 s | 23,875 / 1,358 |
   | KS-1388-envexample | bash_patch | PASS 7/7 strict; A2a by hand ok 2/2; red rc 1 (1 FAIL) → rc 0 (5 ok); B6 2 sibling suites no new red | 18.28 s | 8,796 / 520 |
   | KS-1388-alerting | bash_patch | PASS 7/7 strict; A2a by hand ok 2/2; red rc 1 → rc 0 (5 ok) | 17.74 s | 8,894 / 510 |

   Total model time: 81.7 s; 41,565 prompt and 2,388 completion tokens.
4. **HELD (PASS = candidate, never a merge):**
   - `2_Project_Files/local-model/night/READY_KS-1345-LIST-1_spark-dsv4flash_BRIEFED-CODEPATCH-WEBHOOKS-PASS-7of7_2026-10-05.diff.md` (hold_ready rc 0, no hand edit).
   - `2_Project_Files/local-model/night/READY_KS-1388-ENVEXAMPLE-1_spark-dsv4flash_BRIEFED-BASHPATCH-ENVEXAMPLE-PASS-7of7_2026-10-05.diff.md`
   - `2_Project_Files/local-model/night/READY_KS-1388-ALERTING-1_spark-dsv4flash_BRIEFED-BASHPATCH-ALERTING-PASS-7of7_2026-10-05.diff.md`
   - The two KS-1388 READYs carry ONE marked hand edit each: hold_ready's bash path wrote `Ornith`/`ornith35b-q4` (a known, owed defect); corrected to the Spark, as-written copies kept in each brief folder.
5. **To a Claude seat (Opus 5.5), with the reason:**
   - **KS-1345's deliveries half** (`webhooks.ts:412`, `GET /:id/deliveries`). NOT a counter escalation: the half is not spelled out safely. Its `:402` pattern guard admits a well-formed NON-UUID id, `${req.params.id}::uuid` then raises 22P02, and the `.catch(() => [])` turns that into `200 []` today. Dropping the `.catch` alone would make every such id a 500, while the KS-431 sibling routes answer 404 via `rejectInvalidWebhookId`. Choosing that guard is a decision, and `ks1341c-...test.ts:147` pins the current swallow.
   - **The raise itself:** the Spark cannot raise. A Claude raise seat takes the three READYs (KS-1345 as one PR `Refs KS-1345`; the two KS-1388 carves as one PR `Refs KS-1388`, which apply strict in either order, measured), then a QA gate.
6. **Ornith-tier: 0.** The two KS-1388 carves were Ornith-shaped (one line, spelled out, a failable cell) but ran on the Spark and passed, so nothing is left for Ornith. A measured WHY line was appended to `night/queue.md` (backup `queue.md.pre-1005-why`). `PAUSE_QUEUE` was not touched (it lapses 06:00 10-05).
7. **Harness:** 5 findings in `local-model/IMPROVEMENTS.md` (backup `.pre-1005-spark-screen`). Three are recurrences: hold_ready's bash model tag, no bash A2a leg, and the round scripts lost with their scratchpad. Two are new and measured: the bash tier takes a non-`.sh` product, and the "blank line as a `-`/`+` pair" plus "in-place test hunks under `## The test`" brief convention. None reached the model.

## Method

- **Tip:** develop `2d85b84e1012961c880daa3de70d8491fc0a2ff9`, read by `ls-remote` (deploy key) and by GitHub REST `GET /branches/develop` at 02:09 AEDT. Both agreed, and both matched the commission's expected value.
- **Source clone:** `git clone --shared --no-checkout` of the Blockchain checkout into `8e88f5e9…/scratchpad/spark1005/src`.
  - Origin was set to `git@github.com:Secuura/Distributed_Secuura.git`, with the deploy-key `core.sshCommand`, IN THE SCRATCH CLONE ONLY. Then `fetch origin develop` and a detached checkout at the tip. This avoids the stale-origin defect (09-29, 10-01 rows).
  - node_modules: `Blockchain/Dev`, `packages/shared` and `services/originate` were symlinked FROM the Blockchain checkout's install (read-only reference), excluded via the clone's `.git/info/exclude` (porcelain 0). `prepare_clone.sh` farmed them onward and built shared in each clone.
- **Round scripts — REBUILT, not reused.** The 10-02 copies (`73252fd5…/scratchpad/r/`) and batch 3's (`79817561…/scratchpad/b3/`) no longer exist. The only survivor was `a010e904…/scratchpad/mkclone.sh`, which was read. These were written fresh in `spark1005/` from the 10-02 SCREEN's documented shape:
  - `mksrc.sh`: the source clone above.
  - `mkclone.sh`: a shared clone of `src`, detached at the tip.
  - `linknm.sh`: the node_modules links.
  - `ap.sh`: `git apply` inside a spark1005 clone only. It exists because the `pretooluse_no_cd.sh` hook refuses `git -C $VAR <write>`, as recorded 10-02.
  - `precheck.sh`: golden CONTROL then NEGATIVE, each in a fresh clone. The NEGATIVE takes `NEG_FROM`/`NEG_TO` and asserts the line CHANGED, the 10-02 fix.
  - The model call is the tracked `local_model_task.sh` with `LM_BACKEND=spark SPARK_THINK=0`. The checkers are the tracked `spark_checker.sh` (code_patch) and `bash_patch/checker.sh`, unchanged. A2a was run by hand for bash.
- **Per brief, before the model round:** build_input (rc 0; code_patch printed "prompt source: WEDNESDAY BRIEF … the ticket description is NOT the prompt") → golden CONTROL (PASS 7/7; + A2a on code_patch) → NEGATIVE (FAIL, with the mutation asserted to have changed a line):
  - KS-1345: `` `; `` → `` `.catch(() => []); `` FAIL A3c "1 of 4 … ABSENT".
  - KS-1388 ×2: `:80/` → `:8080/` FAIL B3b "brief '+' line(s) ABSENT".
- **Spark:** `http://127.0.0.1:47788`, `/health` 200 and no other Spark client in `ps` before each round; one request at a time; no retry.
- **Brief timestamps:** shell-stamped by `night/new_brief.sh` (02:20 for KS-1345; 02:26 for both KS-1388), then the skeleton was filled. For KS-1388 the fill script (`mkbrief.py`) kept the stamp and cut every diff fence from the verified golden. For KS-1345 a python `==` confirmed both brief fences equal the golden's hunks.
- **Collision census:** 21 open PRs (REST, ~02:1x AEDT). None touches `routes/webhooks.ts`, the ks1341a test, `observability/*` or `prometheus_targets.test.sh`. **Positive control:** the same census finds 11 PRs touching some `package.json`, the same number as 10-02. Seat B 58th's KS-1015 PR B is not open yet; its files (transfer/delegations, `*.openapi.ts`, the YAML, platform-k HTML) were excluded by commission, as were Seat D's `services/timestamping/` and Seat C's KS-1382/KS-1355 files. No brief here touches any of them.
- **Rounds before today:** `KS-1345` and `KS-1388` in `SPARK_LADDER.md` 0 each, and 0 in `night/briefs/`. Control: `KS-1015` = 2 in the ladder.

## Verdict table — the delta (frame: KS Backlog+Todo, updatedAt > 2026-10-02T20:00Z, TOTAL=3)

| Ticket | State | What it is | Spark verdict · failing clause | Ornith |
|---|---|---|---|---|
| KS-1404 | Backlog (new 10-04 10:09Z) | Timestamping accepts an unsigned TST | NOT: **excluded by commission** (Seat D 4th's lane, `services/timestamping/`); also a **security surface** | NOT |
| KS-1405 | Backlog (new 10-04 10:37Z) | A `Blockchain/Testing` run leaves an untracked `schemathesis.json` | NOT: **decision**. The ticket says *"Suggested fix (not prescribed): either add the artefact path to `.gitignore`, or default `FINDINGS_DIR` … Whoever picks it up should decide which"*. It is also in the KS-1382 harness neighbourhood (Seat C's parked lane). | NOT |
| KS-1406 | Backlog (new 10-04 14:32Z) | Cross-tenant guard fails open for tenantless tokens | NOT: **auth/token security surface**, excluded by commission | NOT |

## KS-1388 §1 (the named candidate)

Read in full: description plus 0 comments, at Linear, and both lines at the tip (`git grep SECUURA_NGINX_STATUS_URI` = the two example lines + `observability/docker-compose.yml:331`). §1 spells the fix ("change both examples to `:80`"). §2 waits on KS-984. §3 (`alloy.river`'s `unslotted` default) is a question for Kam, OUT. **Verdict: SPARK, carved per file, BRIEFED ×2, PASS ×2, HELD ×2.**

## Verdict table — the carve pass, tickets read in full this session

| Ticket | Verdict · clause |
|---|---|
| **KS-1345** | **SPARK — GET / half BRIEFED, PASS round 1, HELD.** The deliveries half goes to Claude (see BLUF 5). Not auth: the list GET's error path; `authenticate()` (`:143`) and the SSRF/HMAC code in the same file are unchanged. |
| **KS-1388** | **SPARK — §1 carved ×2, PASS ×2, HELD.** §2/§3 OUT. |
| KS-1338 | NOT: **the product text is not at the tip.** The entrypoint-corpus guard's "rule-3 / concise arrow" reader is in an unmerged PR ("the pull request that attempted it stays open"). `git grep "concise arrow"` at `2d85b84e` hits no guard reader; `packages/shared/src/__tests__/entrypoint-corpus.ts` (175 lines) has no `guarded`/rule-3 text. Control: `git grep -l guarded` finds 10 files, so the grep is not blind. |
| KS-1356 | NOT: **decision** ("whichever approach you'd prefer"); needs Postgres binaries/Docker. |
| KS-1340 | NOT: "Fix shape (not chosen here)"; a DSN guard for non-disposable databases (security-adjacent). |
| KS-1328 | NOT: three fix shapes, "not chosen here" (**decision**). |
| KS-1197 | NOT: token-claim coercion in `middleware/auth.ts` (**auth surface**), and two files. |
| KS-940 | NOT: launcher suite (Kam's fleet tooling); four items, each with "or" fixes. |
| KS-1343 | NOT: docs on multi-tenancy/RLS (security-adjacent); "overstated" wordings with no spelled replacement; 2 files. |
| KS-1145 | NOT: "the builder's call on both fix shapes, which are the gate's PROPOSALS, not ratified"; needs real Postgres. |
| KS-998 | NOT: four items on the pre-push formatting gate, two MAJOR; no single spelled edit. |
| KS-987 | NOT: a deploy-runbook/bind-mount inode defect; no in-process test (docker). |
| KS-784 | NOT: "No fix attempted; not investigated" (**no fix shape**). |
| KS-1405 | (delta table) |

Re-used without re-reading: 106 prior verdicts. The leading NOT reasons were decision 61 (marker-flagged by the pre-filter, confirmed by prior screens), Playwright/live-stack, multi-file, `.github`/`.githooks`, and `package.json`.

**Positive control for "exhausted at 2":** the same predicate, applied the same way, passed KS-1345 and KS-1388 at source and both passed on the Spark. So the screen can say yes.

## Round evidence

| Step | KS-1345-list | KS-1388-envexample | KS-1388-alerting |
|---|---|---|---|
| Brief | `night/briefs/KS-1345-list/KS-1345.md` (3 hunks: 1 product, 2 test) | `night/briefs/KS-1388-envexample/KS-1388.md` (2 hunks) | `night/briefs/KS-1388-alerting/KS-1388.md` (2 hunks) |
| Golden at tip | test alone 1 failed / 8 passed / 9 (A0, by assertion); golden 9/9; suite 90/1062 → 90/1063; tsc rc 0 both | test alone rc 1, 1 FAIL; golden rc 0, 5 ok; portability checker rc 0 (103 scripts) | same, 1 FAIL → 5 ok |
| Strict apply | `git apply --check -v` rc 0; applied files `cmp` = hand golden | rc 0; `cmp` = | rc 0; `cmp` =; both KS-1388 carves stacked a→b and b→a: rc 0, files identical, suite 6 ok |
| build_input | rc 0, WEDNESDAY BRIEF, expected '+' 4, red cells 1 | rc 0, MODIFY-IN-PLACE, expected '+' 1, must_remove 1 | same |
| CONTROL / NEGATIVE | PASS 7/7 + A2a / FAIL A3c | PASS 7/7 / FAIL B3b | PASS 7/7 / FAIL B3b |
| Spark round 1 | PASS 7/7 + A2a, BYTE-IDENTICAL | PASS 7/7 (+ A2a by hand), BYTE-IDENTICAL | PASS 7/7 (+ A2a by hand), BYTE-IDENTICAL |
| Run dir | `runs/spark_secuura_2026-10-05_KS-1345-list` | `runs/spark_secuura_2026-10-05_KS-1388-envexample` | `runs/spark_secuura_2026-10-05_KS-1388-alerting` |

Kit rule 4, six clauses, all held on all three:
1. Strict apply at a known commit, with the mode recorded.
2. Added lines byte-identical (`cmp` to the golden).
3. Touched set = the 2 named files.
4. RED at the tip, GREEN with the product hunk.
5. Suite no worse: originate 1062 → 1063 with 0 failed; bash B6 had 2 siblings with no new red.
6. Every assertion's output is kept in `out.md.checker/`.

The diffs were read against the briefs by this sub-agent before holding: each is byte-identical to a golden whose fences were proved equal to the brief's.

No FAIL, so no model/harness/brief classification was owed. Counter: round 1 of 2 used on each carve.

## Departures from the commission

1. **Round scripts rebuilt** in `spark1005/`, because the earlier copies were lost with their scratchpads. Stated above, and an IMPROVEMENTS recurrence.
2. **KS-1388 §1 was carved into TWO briefs**, so 3 briefs/rounds, not "up to 3 candidates" of one brief each. The two carves count as one candidate (KS-1388). The predicate's "one product file" forced the split.
3. **Tier:** both KS-1388 carves ran on `bash_patch` with a non-`.sh` product (a commented `.env.example`). The builder and checker accept it. This is a first use, measured, not a harness edit.
4. **Hand edits to two READYs** (the model tag only, marked, with backups). They were not written by the hold tool alone, because the hold tool's bash path still mislabels Spark runs.
5. **`SPARK_LADDER.md` was NOT updated.** It is not in this commission's write list. The ladder rows for these three rounds are owed to Wednesday. The last row is 58 (10-02), and the 10-04 owner-list round has no row either, so the next free numbers start at 59.
6. **PAUSE_QUEUE was not touched** (not in the write list).

## UNMEASURED

1. No Schemathesis, no live stack, no real Postgres. KS-1345's 500-on-rejection is driven through a mocked `$queryRaw`. KS-1388's `:80` connecting is the compose default's reasoning, not a started exporter.
2. **KS-1345 behaviour change:** a non-UUID `userId` (22P02 on `::uuid`) answered `200 []` at the tip and answers 500 with the fix. Whether any real principal reaching originate carries one was not measured.
3. Test-inclusive `tsc` and the package lint were not run on the modified ks1341a test. The checker's informational line said `tsc on the test file alone (--types node,jest): rc=0`.
4. node_modules are the Blockchain checkout's own install (its develop at `c56dd7c3`), not a fresh `npm ci` at `2d85b84e`.
5. The 130 tickets excluded by the broad security/auth TITLE regex were not opened this session. Prior screens opened 16 such tickets and none passed. The regex over-excludes (e.g. "tenant", "audit", "session", "admin"), so a carve hiding behind such a title would be missed.
6. The 106 re-used verdicts were not re-read. The delta frame shows none of them changed since 2026-10-02T20:00Z, but their bodies were not re-checked against the new tip.
7. Open PRs were read at ~02:1x AEDT; a later PR is not covered. Seat B 58th's PR B files are excluded by name, not by census.
8. `hist.py` (filed here) was not run: all 3 delta tickets were created inside the window, so there was no history to read.
9. The CI path that runs `prometheus_targets.test.sh` (`run-shell-suites.sh` / the workflow) was not run.

## Instruments filed here

`pull.py` (paginated Linear pull), `hist.py` (Linear issue history, cutoff 2026-10-02T20:00Z; not run), `rank.py` (the pre-filter and ranker over the pulled board) and `prs.py` (the open-PR census with files). All read their keys from the environment and never print them.
