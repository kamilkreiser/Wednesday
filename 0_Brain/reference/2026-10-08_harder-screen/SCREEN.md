# Harder-work screen for the Spark and Ornith 1.5 — 2026-10-08 evening (2 briefs delivered: 1 Spark, 1 Ornith 1.5; target was 3 + 3)

Written 2026-10-08 20:05 AEDT (shell `date` 20:04:37) by a drafting sub-agent for Wednesday, on Kam's 18:12 ruling (verbatim): *"go with Ornith 1.5 and deploy it. use this instead of the old model. Keep pushing it and see how far it can go. The old Ornith has been rather dormant with the spark doing a lot of work. see if you can give it harder tasks and run both the Spark and Ornith 1.5 as much as possible"*. Secuura only (Platform K, `Secuura/Distributed_Secuura`).

**Read-only on client systems.** Linear: GraphQL reads only (key sourced from the Blockchain `4_Credentials/.env` in a subshell, never printed). GitHub: REST GET only (open PRs + their files; `GH_TOKEN` from the same file, same way). Git under `!CODING/`: `ls-remote`, `status` only; every write verb ran in `git clone --shared` copies under this session's scratchpad (`…/scratchpad/harder/`). The Secuura checkout reads 0 tracked-modified lines at 20:04. **Not touched:** `spark/queue.md`, `night/queue.md` (git status: unmodified), `night/inputs/`, mail, Linear, GitHub. No model round. Nothing deleted.

## BLUF

1. **Tip:** develop `0a6177ea5482227e83d5045b68b8577a56326ffc`, read by `ls-remote` at 19:28:20, 19:50:27 and 20:04:37 AEDT, unchanged.
2. **Delivered: 2 briefs, both one rung harder than the tier's recent passes, both proven.**

   | brief | ticket | for | tier · rung | files | dry run | golden check |
   |---|---|---|---|---|---|---|
   | `spark/briefs_2026-10-08_harder/KS-1438-html-docs-check-resolved-paths/` | KS-1438 (Backlog, Kamil, 0 comments) | **Spark** | bash_patch2 · rung 3 tier, **first non-shell product on it** (`.mjs` product + bash RED suite) | `systemTest/__tests__/support/html_docs_check.mjs` (2 hunks), `systemTest/__tests__/html_docs_matrix.test.sh` (MODIFIED, RED, 2 hunks) | `round.sh --dry-run` **rc 0** (DRY-RUN OK) | `round.sh --control` **rc 0, CONTROL-PASS 9/9, golden BYTE-IDENTICAL**, A2a 4/4 |
   | `night/briefs/KS-937.md` (+ `KS-937.golden.diff`) | KS-937 (In Progress, Kamil; #874/#876 not open) | **Ornith 1.5** | bash_patch · **rung 2** (two hunks at two sites in one script + its existing suite) | `Blockchain/Dev/scripts/check-shared-relink.sh` (2 hunks), `…/__tests__/check_shared_relink.test.sh` (MODIFIED, 1 hunk) | `build_bash_input.sh` **rc 0**; `ticket.description` == the brief byte for byte (the prompt is the brief, not the ticket) | `tasks/bash_patch/checker.sh` on the fenced golden **rc 0, RESULT: PASS (7/7)**, strict |

3. **Why only 2 of 6.** The pool, again, not the tiers. 487 tickets screened (predicate below); every other candidate failed a named clause (table below). The two dominant blockers this round were **"named in or attached to an open PR"** (the KS-591 / KS-1364 / KS-593 / KS-565 / KS-1015 / KS-1410 registers, which hold most of the remaining mechanical work, are all named by #1427-#1431 or R 19th's KS-1410 raise) and **"no harness runner"** (node:test, `.mjs` node tests, Playwright, Linux-only reds).
4. **Wednesday decides (not acted on):**
   - **(a) Ornith 1.5 cannot climb to rung 3 on today's harness.** `night/night_run.sh` runs only the single-file tiers (code_patch, bash_patch via `input=`/`task=`, doc/comment), and `spark/round.sh:298` hard-wires `LM_BACKEND=spark`. So every multi-file brief (code_patch2, bash_patch2 — including KS-1438) is Spark-only. A backend switch on `round.sh` (e.g. an env var passed through to `local_model_task.sh`, which already supports `LM_BACKEND=omlx`) would let 1.5 take rung 3; that is a harness change, Wednesday's call. KS-1438's brief would run on 1.5 unchanged.
   - **(b) KS-937 on 1.5 is ~130 KB of input** (`input.json` 130,513 B: the script 40 KB + the suite 61 KB carried whole). The 1.5 server caps context at 65,536 and the deploy report lists ">28K-token prompts" as NOT TESTED. If 1.5 fails on length, that is a harness fact; the brief also fits the Spark's bash_patch path unchanged.
   - **(c) KS-1345's deliveries half is a real decision, not a missing brief** (see rejections): `ks423-contract-alignments.test.ts:102-108` pins a well-formed NON-UUID id (`wh_12345`) as 200 + envelope, while the file's own `rejectInvalidWebhookId` (KS-431) answers 404 for exactly that id on its four sibling routes. Which contract wins is the owner's; the brief writes itself once ruled (code_patch2: `webhooks.ts` + ks1341c flip + ks423 flip).
   - **(d) Standing line to update after KS-1438 merges:** live raise briefs quote `html_docs_matrix.test.sh 12/0` (STANDING_LINES `:439`, e.g. `seatE12_raise_ks591_ks1364.md`, `seatR19_raise_r3r5_ks1410_ks1139.md`). With KS-1438 the suite reads **16/0**.
   - **(e) Queue lines, if you take them** (not written by me): Spark — `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/briefs_2026-10-08_harder/KS-1438-html-docs-check-resolved-paths` (pins in its `spark.pins`). Ornith 1.5 — build the input into `night/inputs/` first (`bash tasks/bash_patch/build_bash_input.sh KS-937 night/inputs/bash_patch_937RELINK-R1.json night/briefs/KS-937.md product=Blockchain/Dev/scripts/check-shared-relink.sh ref=Blockchain/Dev/scripts/__tests__/check_shared_relink_case.test.sh test_file=Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh ctx=65536`), then `KS-937 input=<that> task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/bash_patch/task.md ctx=65536` — the KS-1081/KS-1040/KS-1033 shape (`night/done.md:463`-`:489`). `PAUSE_QUEUE` state was not read.

## Tickets read

- **Pull:** GraphQL `issues(first:50)`, filter team `KS`, `state.type in [backlog, unstarted, started]`, paginated to `hasNextPage=false`: **11 pages, 506 nodes, 506 distinct** (Backlog 244 · Todo 29 · In Progress 214 · In Review 14 · Blocked 5; 0 archived). Comments `first:50`, sorted client-side; one ticket (KS-485) hit the 50 cap.
- **Predicate (the commission's): state name in {Backlog, Todo, In Progress} → 487.** Then excluded:
  - assigned to Peter or Stuart: **23**;
  - attached (Linear attachment) to an OPEN PR: **11** — KS-1449 #1429, KS-1401 #1383, KS-1355 #1431, KS-1328 #1430, KS-1303/KS-1302 #1250, KS-1297 #1253, KS-1274 #1427, KS-973 #989, KS-741 #995, KS-593 #1428;
  - named in an open PR's title/body (treated as attached): KS-591, KS-1364, KS-1449 (#1429); KS-565, KS-593, KS-1015 (#1428); KS-1136, KS-1274 (#1427); KS-1155, KS-1164, KS-1328 (#1430); KS-1355 (#1431); KS-4, KS-1376, KS-1401 (#1383); and older #995/#989/#927/#923/#920/#887/#809/#1129/#1360 keys; plus **KS-1410 and KS-1139** (R 19th's raise, per `briefs_staged/2026-10-08_seatR19_*`).
- **Open PRs:** 27 (#1427-#1431, #1383, #1360, #1253, #1250, #1129, #995, #989, #949, #948, #947, #946, #945, #927, #923, #920, #887, #809, #649, #639, #635, #575, #572), **143 file entries**. Positive control: the census sees `systemTest/__tests__/` (#927) and `Blockchain/Dev/scripts/` (#1431).
- **Screened by title:** all 487 minus the exclusions. **Read in full this session (description and comments):** KS-1451, 723, 730, 1345, 1346, 1129, 1333, 1074, 1213, 1171, 1101, 679, 794, 968, 1123, 1382, 1322, 1424, 1443, 1438, 1326, 1340, 1082, 1359, 1269, 1371, 1098, 937, 1284, 1296, 1388, 1314, 1180, 1347, 1364, 1409, 1423, 1444, 1441 (39). Round-counter / held-work history read for each (`spark/done.md`, `night/done.md`, `night/briefs/`, `night/READY_*`).
- **Prior verdicts honoured** (not re-proposed): `2026-10-08_spark-screen/SCREEN_0300.md`, `2026-10-08_spark-hold-census/CENSUS.md`, `2026-10-07_spark-screen/SCREEN_{1120,1520,2300}.md`, `2026-10-05_internal-tooling-screen/screen.tsv`, `2026-10-05_ks-ticket-audit/` (used to rank the genuine-defect residue), and the `night/queue.md` rejection list.

## Per candidate (delivered)

### KS-1438 → Spark · bash_patch2 · rung 3 tier (new shape: non-shell product)
- **Defect (measured at the tip):** `html_docs_check.mjs:120` guards its command block with ``import.meta.url === `file://${process.argv[1]}` `` — resolved, percent-encoded URL vs the typed path. Through a symlink, or from a directory whose name has a space, a page with an unbalanced Mermaid bracket exits **0 with no output**; through the real path it exits 1 and names the finding.
- **Fix (the ticket's):** `fileURLToPath(import.meta.url) === realpathSync(process.argv[1])` (guarded for a missing `argv[1]`), two imports.
- **Why it fits / why harder:** spelled by the ticket; in-process (node + bash, no stack); not security; 0 rounds; the 10-07 screens held it only as "just filed". Harder: bash_patch2 has never carried a non-shell product, and the model must keep JavaScript and bash apart in one diff (4 hunks, 2 files).
- **Measured:** suite at tip 12/0; test hunks alone **rc 1, 14/2** (exactly the two RED cells); golden **rc 0, 16/0**; a partial fix without `realpathSync` reds only the symlink cell, one that keeps the `file://` string form reds only the space cell (15/1 each). Control run dir: `runs/spark_secuura_2026-10-08_KS-1438-html-docs-check-resolved-paths-control`. sha256/16: brief `e974ff387e9f4001`, golden `8d5479a051db3ada`, pins `dbbd1beb9624493d`.
- **Dry-run rc 0; control rc 0.**

### KS-937 F-C + F-E → Ornith 1.5 · bash_patch · rung 2
- **Defects (measured at the tip; F-A and F-D of the same ticket are already fixed at `:236`-`:237` and by the suite's "mirror" cell):** F-C — the re-link regex at `check-shared-relink.sh:418` requires a LEADING slash in its optional destination prefix, so `ln -s /shared ./node_modules/@secuura/shared` (and `app/node_modules/...`) is a false BLOCK ("final stage has NO ..."). F-E — `:435` keeps `USER root:root` / `USER 0:0` whole and `effective_user_is_unprivileged` (`:526`) accepts only `root`/`0`, so root-with-group is a false BLOCK ("runs after a non-root USER").
- **Fix (the ticket's shape):** prefix group `([^ \t]*\/)?`; a third `sub(/:.*$/, "", u)` on `:435`. Each a one-line replacement with a 2-line comment; no apostrophe in any `+` line (the edits sit inside a single-quoted awk program).
- **Why it fits / why harder:** spelled; one product file; the guard's own suite is in-process (throwaway Dockerfiles, no docker); not security; 0 rounds; no open PR or live seat touches the guard or its suites (checked against the 27 PRs and every `briefs_staged/2026-10-08_*` seat brief). Rung 2 for 1.5 per the 10-08 learning ("start at multi-hunk"): two hunks at two separate sites.
- **Measured:** suites at tip 106/0, 6/0, 6/0; test hunk alone **rc 1, 107/4** (exactly the four RED cells, 0 load errors); golden **rc 0, 111/0**, siblings unchanged, the guard over the real `Blockchain/Dev` tree 25/25 clean; E1 alone leaves the F-E pair red, E2 alone the F-C pair (109/2 each). sha256/16: brief `cfc60fbe6ad8b40f`, golden `49f69f7d29a4f628`.
- **Dry run:** `build_bash_input.sh` rc 0 (`MODIFY-IN-PLACE`, sites 6 (2 must_change), expected '+' 6, must_remove 2). That builder prints no prompt-source line outside self-testing mode, so the check was done directly: `input.ticket.description` equals `night/briefs/KS-937.md` byte for byte (True, 18,369 chars). **Golden through `tasks/bash_patch/checker.sh`: RESULT PASS (7/7), strict, B4 rc 1 with 4 FAIL, B6 3 sibling suites no new failure.**

## Rejections (every candidate considered, with its clause)

| ticket | verdict · clause |
|---|---|
| KS-1410 (remaining 18 sites: transfer, tenant-provisioning ×7, mcp-server ×10) | NOT: **attached to R 19th's open raise** (KS-1410 R3+R4 pushed this evening); and tenant-provisioning/mcp-server have no in-process seam (10-07 SCREEN_1520) |
| KS-1364 / KS-591 / KS-1449 (spec `required`/format carves) | NOT: **named in open #1429**; 19 held passes of this class are UNRAISED (CENSUS); a fresh-file scan at the tip (`services/*/src/*.openapi.ts`, 22 files) found no non-security file with ≥2 bodies whose handler refuses an absent body (api-gateway privacy/notifications settings: both handlers use `req.body \|\| {}` and accept it; originate sign-cert: every field optional) |
| KS-565, KS-593, KS-1015 | NOT: **named in open #1428** |
| KS-1345 deliveries half | NOT: **decision** — ks423 `:102-108` pins `wh_12345` → 200, KS-431's helper answers 404 (see BLUF 4c) |
| KS-1451 five slot guards | NOT: the ticket requires **all five in one change** across bash, two vitest packages, Playwright and pytest (no single runner; a carve makes the guards disagree, which the ticket forbids) |
| KS-723 remaining ~150 ops | NOT: declaring a path changes the gateway's spec-driven method/auth gate (the 10-05 anchors-get REVIEW measured two live POSTs going 405); security-adjacent, routed to a Claude seat by that review; "Peter-sized" per the ticket |
| KS-730 (tokenisation ×2, api-gateway) | NOT: tokenisation is the PII key vault with `app.listen` at import (no seam); the api-gateway half moved to `middleware/errorHandler` (KS-727) |
| KS-1346, KS-1129, KS-1333, KS-1074, KS-1213, KS-1171, KS-1101, KS-679, KS-794, KS-968, KS-1123, KS-1284, KS-1296 | NOT: **merged; only a live sweep or a ruled residue remains** (KS-1171 B1 is a held unraised Spark pass; KS-1333's measurement landed as #1380; KS-1346 F-2 is ruled residue) |
| KS-1424 updateDocument 12 callers | NOT: **decision** ("Changing the other 12 needs its own decision") |
| KS-1322 ticket keys in spec text | NOT: **decision** ("the owner's call") |
| KS-1382 Blockchain/Testing TARGET_BASE | NOT: 5+ files (over bash_patch2's 3), shared-guard group acceptance, waits on KS-1162's decision |
| KS-1443 two Linux-only test faults | NOT: **red is Linux-only** (lsof thread names; pg_isready in /usr/bin) — cannot be red-proven on this host |
| KS-1326 childSuiteCounts | NOT: **residue of a capped round** (counter exhausted; the KS-1338 precedent) |
| KS-1314 readYaml routing | NOT: **capped** (#1278 round 2 of 2, NO GO at the cap) |
| KS-1340 ks597 DSN guard | NOT: "Fix shape (not chosen here)" — decision; integration-config file |
| KS-1082 Playwright env guard | NOT: systemTest Playwright (Peter's authority per the ticket); guard exists only on unmerged #896 |
| KS-1359 audit-log limit=201 | NOT: **decision** ("refuse … or align the spec with the 500 clamp. Your call") |
| KS-1371, KS-1269 status revoke/unrevoke | NOT: merged; Peter's 10-05 sweep says still reproducing — **measure-first**; revocation records (security-adjacent) |
| KS-1098 k6 echo mask | NOT: fix shapes are "proposals, not decisions", name set is Peter's; only QA-958-3 (a PASSWD pin) is spelled — rung 1 test-only, not harder |
| KS-1347 proxy/server.ts `.pathname` | NOT: **no harness runner** (`scripts/openapi-examples` tests are `node:test` via tsx); module exits at import without `HARVEST_EXAMPLES` |
| KS-1388 observability.sh `down` | NOT: "Fix direction (suggestion, not done)", two options; observability tests are `.mjs` node tests (no runner) |
| KS-1423 gate64 minors | NOT: the actionable defect is in the QA kit (`c4_docs_gate64.py`, outside the repo); the rest are test-wording items |
| KS-1444 untagged images | NOT: "for Kamil's judgement" design; needs docker |
| KS-1441 Akto LOW results | NOT: classification decision |
| KS-1409 webhooks connector principals | NOT: **decision** (4xx vs keyed on org, "the owner's") |
| KS-937 F-B, F-F | NOT in the KS-937 brief: F-B is a test-target cell with no product change; F-F (`find . -name Dockerfile`, `:90`) needs a choice of which names count |
| KS-1186, KS-1210, KS-1005, KS-938, KS-1009, KS-1107, KS-1195, KS-1402, KS-1448 and the other auth/oauth/token/MFA/credential/tenant/KYC titles | NOT: **security surface** (for Ornith always; for the Spark none came with a fully spelled fix) |
| decision / question titles (KS-582, KS-775, KS-782, KS-834, KS-1141, KS-1358, KS-767, KS-595, KS-651, …) | NOT: **decision** (title states it) |

## Tooling findings (none edited)

1. **`spark/round.sh:298` hard-wires `LM_BACKEND=spark`** — the multi-file tiers exist only for the Spark. Opening them to Ornith 1.5 is one pass-through env var away (see BLUF 4a).
2. **bash_patch (tier 1) B5a runs `bash -n` on the product** (`tasks/bash_patch/checker.sh:433`), so a non-shell product is only gradable on bash_patch2, which skips it with an INFO line (`tasks/bash_patch2/checker.sh:238`). Measured on KS-1438's control: "INFO B5a html_docs_check.mjs is not a .sh — bash -n not applicable".
3. **bash_patch2 cannot use the declared RED suite as its `ref=`**: it runs the tier-1 builder first, which refuses `test_file equals ref` (first dry run of KS-1438, rc 2). Fixed in the brief by pointing `ref=` at a sibling suite (`no_secret_prefix_echo.test.sh`); KS-1274 avoided it by using a SUPPORT suite. The spark README's "it may be a declared one" holds only for a non-RED declared suite.
4. **`build_bash_input.sh` prints no "prompt source" line outside self-testing**, so the commission's Ornith check ("must NOT print prompt source: the ticket description") cannot be read off its output; it was done by comparing `input.ticket.description` with the brief.
5. Two run artefacts were added by the commission's own proofs: `runs/spark_secuura_2026-10-08_KS-1438-html-docs-check-resolved-paths-control/` and `spark/cache/work/…-control_195347/` (~1 clone), plus `spark/state/dry/KS-1438-…` dry dirs. Nothing was removed. The Spark cache fetched develop `0a6177ea5482` (round.sh: "fetching develop from origin … not yet local") — a fetch into the Wednesday-side cache, not the Secuura checkout.

## UNMEASURED

- **No model round** on either brief; whether the Spark keeps JavaScript and bash apart, and whether 1.5 handles a ~36K-token bash prompt (130,513 B input / ~3.6 chars per token, estimated, not tokenised), is what the rounds measure.
- **Linux:** both briefs measured on macOS (bash 3.2.57, node v24.7.0) only.
- **`night_run.sh` dry run** for KS-937 was not run (it reads `night/queue.md`, which this sub-agent may not edit); the builder and checker were run directly.
- **Live seats' unpushed work:** only open PRs and the staged seat briefs were read; a seat's unpushed edits to these four files would not show.
- The 448 tickets screened by title only were not re-read in full this session; their earlier verdicts (10-05 to 10-08 screens) were relied on where the title and `updatedAt` gave no reason to doubt them.
- `PAUSE_QUEUE` and the Spark endpoint's queue state were not read (the endpoint answered 200 at 19:52).
