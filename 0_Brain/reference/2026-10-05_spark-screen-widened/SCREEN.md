# KS screen for the Spark, WIDENED predicate — 2026-10-05

Written 2026-10-05, 11:3x-11:4x AEDT (brief stamps from the shell: 11:35 AEDT), by a Spark brief-writer sub-agent for Wednesday. It follows `0_Brain/reference/2026-10-05_spark-screen/SCREEN.md` (02:32), which found 2 briefable tickets of 277 under the one-file predicate.

**Read-only on client systems.** Linear: GraphQL reads only (`LINEAR_API_KEY` sourced from the Blockchain `4_Credentials/.env`, never printed). Git: read verbs on the Blockchain checkout (`show`, `grep`, `ls-remote`, `cat-file`, `rev-parse`, `status`); every write verb ran in a `--shared` clone in this session's scratchpad. The checkout reads 0 tracked-modified lines before and after (`git status --porcelain --untracked-files=no`). Nothing was raised, pushed, posted or mailed. No Spark round was run by this writer; Wednesday ran KS-1278 herself (her message, ~11:35).

## BLUF

1. **Read:** the whole KS Backlog + Todo board: **276 issues** (243 Backlog, 33 Todo), pulled with `issues(first:100)` and `pageInfo` pagination until `hasNextPage` was false, `comments(first:50)` per issue. The count is NOT capped. (The 02:32 screen counted 277; one ticket left the frame since.)
   - Excluded first: 24 held by Peter/Stuart; KS-1250 and Seat B 59th's KS-1345 and KS-1388 (KS-528 and KS-769 are not in Backlog/Todo). 249 left.
   - All 249 were given a fix-section and file-mention pass (`fix.py`). About 45 were read in full, and 9 were read at source in the code.
2. **Briefable, per rung:**

   | Rung | Briefs | Runnable on today's harness? |
   |---|---|---|
   | 1 | KS-948 carve (bash_patch), KS-1333 pin (code_patch, test-only) | yes |
   | 2 | none | — |
   | 3 (2+ product files) | KS-1278 revoke-atomic (2 product files + new test + 1 manifest line = 4 files) | **NO**, see point 3 |
   | 4 (fix shape only) | KS-723 anchors-tx, KS-723 anchors-get (carves of a 157-operation ticket) | yes |

   That is 5 briefs, 3 of them at rung 3 or higher. The 6-8 asked for were not reached; point 4 says why.
3. **The honest reason the pool looked empty.** The "one product file" clause is not only a screening habit. It is hard-coded in the harness.
   - `tasks/code_patch/checker.sh` A3 requires the touched set to be `{ product_file, ONE test }` (`:14`, `:561`), and `night/build_input.sh` takes one `product=` (`:178`-`:198`).
   - `tasks/bash_patch/checker.sh` B3 has the same rule (`:353`-`:355`). B6 then reds any sibling suite that the fix breaks.
   - `tasks/bash_patch/build_bash_input.sh:90` REFUSES a brief with no fenced `+` lines, so rung 4 cannot run on bash at all.

   So **rung 3 cannot run on any tier today**, and rung 4 runs only on code_patch.

   **At source, tickets that read as one-file are often multi-file.** Measured on two of them:
   - **KS-1274** (trivy `{}`) says "one guard + a cell". But three sibling suites stub a CLEAN scan as `{}` (`container_trivy_failed_scan_is_loud.test.sh:57`, `container_trivy_exit_code_env_keeps_findings.test.sh:67`, `container_trivy_image_filter.test.sh:76`). Any fix reds all three, so the real change is 4 files and 6 hunks.
   - **KS-1278**'s new test must also be named in `ks1293`'s SUBJECTS manifest, or the golden reds MANIFEST-DRIFT (measured).

   **Recommendation (Wednesday's call; this writer edited no harness):** extend A3/B3 to `product_files=[…]` plus a list of modified tests. That one change opens rung 3. KS-1278 is the ready test case, and KS-1274 is the next.
4. **Why not 6-8.** Every other ticket fails a clause (see the table). The leading reasons:
   - a decision or a ruling (the largest group);
   - a security, auth or tenant surface;
   - no runner the checker has (Playwright, frontend without a test script, real Postgres, docker or CI);
   - over the 3-edit cap;
   - already fixed;
   - a held READY already exists.
5. **⚠ KS-1278 was queued and run by Wednesday before this screen was written.** The brief says it is NOT runnable on today's A3: it touches 4 files. Expect a harness refusal (A3 touched-set), not a model verdict. Read the run's `checker.out` with that in mind, and do not spend the counter on it.

## Briefs (paths under `2_Project_Files/local-model/night/briefs/`)

| Brief | Rung | sha256 | Golden measured (scratch clone at 57fa9e31d7ce) | Queue status |
|---|---|---|---|---|
| `KS-723-anchors-tx/KS-723.md` | 4 | `cde0bd9bdd1c…` | red 3/5 → 5/5; anchoring 353 → 364 (+11, both carves stacked), the 1 failure the same pre-existing threadTokenMint/KS-562; tsc rc 0; YAML regen + spec-examples OK; strict | see Addendum |
| `KS-723-anchors-get/KS-723.md` | 4 | `fae4c8ff635c…` | red 4/6 → 6/6; same suite figures; strict; stacks with tx | see Addendum |
| `KS-1278-revoke-atomic/KS-1278.md` | 3 | `e949f1506da0…` | red 2/4 → 4/4; originate 90/1062 → 91/1066, 0 failed; tsc rc 0; negative control (no manifest line) → 1 failed; brief fences produce files sha1-identical to the golden | queued by Wednesday (see BLUF 5) |
| `KS-948-mixed-backtick/KS-948.md` | 1 | `5488890f243a…` | red rc 1 (1 FAIL) → rc 0 (5 ok); subject suite 106/0 both sides; strict | see Addendum |
| `KS-1333-blocknumber-pin/KS-1333.md` | 1 (test-only) | `8a65c5cb229f…` | green 3/3 at the tip; under the `:1317` tamper 1 red (B1) and 2 controls green | see Addendum |

Each folder holds `golden.diff` (the writer's verified golden, git form). The KS-723 folders also hold `yaml_companion.diff` (the served YAML, which the raise seat regenerates). Folders that needed builder pins hold `spark.pins`.

**Measured finding: KS-1333's question is answered.** `GET /api/anchors/:id` reports blockNumber as a number or null:
- `rowToAnchor` at `index.ts:1317` converts it with `Number()`;
- both lookups the handler uses map through `rowToAnchor` (`:1439`, `:1451`);
- the handler answers `:881` `anchor.blockNumber || null`.

So the ticket's own rule applies: pin it, do not coerce. The Linear reason comment is Wednesday's to post. The `|| 0` → `??` question remains a decision.

**Other routing found:**
- **KS-1186** already has a held Ornith PASS, `night/READY_KS-1186_ornith35b-q4_AUTH-5SITE-LINEKEYED-PASS-7of7_2026-09-17.diff.md`. The five unawaited `fromRow` sites are still at the tip (`userRepo.ts:446/512/585/594/627`). This needs a raise seat, not a Spark round. It is in `services/auth`, so Wednesday judges the surface.
- **KS-1387** is fixed by KS-1380 (Stuart's 10-02 comment: 35/35 images build). **KS-1149** has its launcher keepalive applied (s220 comment). Both are close candidates, not work.

## Verdict table — the tickets read in full (failing clause named)

| Ticket | Verdict · clause |
|---|---|
| KS-723 | **BRIEFED ×2** (carves: GET /{id}, GET /tx/{txHash}, which Stuart named as Platform-S hot path). ⚠ The body says "routed to Peter"; the assignee is Kamil. Wednesday confirms. Next carve candidate: `POST /api/anchors/batch`. It needs `batchAnchorSchema` exported from `index.ts` first (no restating), so 2 files. |
| KS-1278 | **BRIEFED, rung 3** (harness-blocked, BLUF 3). |
| KS-948 | **BRIEFED, rung 1 carve** (the #879 finding-3 fail-open grep). The re-home into `run-shell-suites.sh` stays open. |
| KS-1333 | **BRIEFED, test-only pin** (measurement: already a number). |
| KS-1274 | NOT: **multi-file** (4 files, 6 hunks: three sibling suites stub clean as `{}`) and **over the 3-edit cap**. Rung 3 after the harness extension, or a Claude seat. |
| KS-1186 | NOT a Spark task: **a held READY exists** (Ornith PASS 09-17). Needs a raise seat. |
| KS-1340 | NOT: the guard is **inline in an integration test** (`ks597-issuer-organization-id.integration.test.ts:84`-`:181`), so there is **no unit-reachable seam and it needs Postgres**. It is DSN/credential-adjacent, and the ticket says "Fix shape (not chosen here)". |
| KS-1304 | NOT: **tenant-pool selection, a data-isolation surface** (treated as security). |
| KS-1112 | NOT: **decision** ("align or document"). |
| KS-1114 | NOT: Kam ruled `implement-title`, but the ticket names two **open design questions** (duplicate titles, anonymous disclosure). |
| KS-1115 | NOT: needs a **live-row census first**; a migration (no runner). |
| KS-1200, KS-1184, KS-1243, KS-1249, KS-1322, KS-1389, KS-1162, KS-1320, KS-807, KS-1022 | NOT: **decision** (each says decide / "the owner's call" / "not ratified" / "your view"). |
| KS-1387, KS-1149 | NOT: **already fixed** (see above). |
| KS-678 | NOT: **decision** ("Calls needed from @PeterD": domain ownership, `example.com`). It is also 6 files. |
| KS-709, KS-716 | NOT: **Peter's active area** (he changed the adjacent code 09-28/09-30) and multi-item. KS-716's item 2 sits in `secrets.example.yml` (credential-adjacent). |
| KS-1010, KS-1038, KS-1039, KS-1113 | NOT: **no runner**. These are Playwright e2e, which the checker cannot run. |
| KS-1104, KS-1105, KS-1106, KS-735 | NOT: **no runner** (frontend; no frontend declares a `test` script, KS-1391). KS-735 also needs Peter's contract call. |
| KS-1391 | NOT: a `package.json` edit. **No tier checks it.** |
| KS-1392, KS-1162 | NOT: `.github` workflows (**no runner**). |
| KS-1289 | NOT: `.dockerignore`. **No in-process test can red it**; the ticket's own verification is an image rebuild. |
| KS-1030, KS-1356, KS-1145 | NOT: need **real Postgres**. |
| KS-1259, KS-1328, KS-1324 | NOT: **timing or isolation flakes**, which cannot red-prove deterministically. |
| KS-1326, KS-1330, KS-1331, KS-1332 | NOT: **residue of capped rounds** with an OPEN PR for the owner's disposition (#1245 etc.). The builder refuses an open attached PR. |
| KS-1329, KS-1251 | NOT: tsc- or eslint-only. **No runtime red** is possible. |
| KS-1048 | NOT (for now): it edits the repo `CLAUDE.md` (agent governance). It is two copies, one outside the repo. Kam's call. |
| KS-1394 | NOT: **Seat B 59th's lane** (`scripts/audit/*`). |
| KS-1323 | NOT: fleet push tooling, **not Secuura repo code**. |
| KS-1381, KS-1382, KS-1355, KS-1389 | NOT: the **slot-tooling lane** (Seat C, parked) and multi-file. KS-1381 also touches the Entra redirect URI (auth-adjacent). |
| KS-1385, KS-1384 | NOT: **decision** (the per-document-anchor ruling on KS-1384 gates both). |
| KS-1333 follow-on (`|| 0` → `??`) | NOT: **decision**, named by the ticket. |

**The remaining ~200 by clause** (title + fix-section pass via `fix.py`, plus the 02:32 screen's 106 prior verdicts; none was re-read in full):
- **security/auth/token/tenant surface:** for example KS-263, 304, 329, 485, 526, 576, 618, 619, 623, 625, 627, 636, 668, 746, 756, 759, 782, 785, 787, 805, 824, 825, 834, 836, 838, 840, 870, 902, 915, 918, 919, 938, 951, 959, 967, 977, 986, 1000, 1003, 1005, 1009, 1017, 1032, 1053, 1055, 1080, 1083, 1091, 1100, 1102, 1107, 1116, 1119, 1132, 1146, 1148, 1157, 1161, 1168, 1174, 1177, 1189, 1190, 1191, 1197, 1208, 1210, 1214, 1219, 1225, 1235, 1240, 1241, 1242, 1255, 1256, 1262, 1280, 1357, 1358, 1372, 1376, 1377, 1383, 1400, 1401, 1406.
- **decision/ruling/business:** KS-305, 339, 579-583, 595, 598, 602-605, 621, 624, 651, 655, 658, 696, 699, 748, 761, 765, 767, 829, 837, 846, 866, 889, 925, 939, 953, 955, 956, 995-997, 1012, 1023, 1025, 1044, 1076, 1079, 1082, 1085, 1088, 1141, 1178, 1216, 1224, 1290, 1305, 1327, 1379, 1390, 1393, 1398, 1405.
- **no runner, live stack or ops:** KS-491, 562, 565, 591, 593, 607, 638, 648, 683, 724, 725, 749, 752, 757, 758, 760, 770, 772, 777, 783, 784, 812 (connectors/ path the builder refuses), 884 (round counter 2), 903, 940, 960, 964, 987, 998, 1014, 1051, 1138, 1154, 1163 (counter 4), 1218, 1247, 1307-1309, 1317, 1325.

## FOUND / TESTED / HOW

**FOUND**
- The harness enforces one product file in every tier (A3 `checker.sh:561`; B3 `bash_patch/checker.sh:353`-`:355`; `build_input.sh` one `product=`). The bash builder refuses rung 4 (`build_bash_input.sh:90`).
- Two "one-file" tickets are multi-file at source (KS-1274: 4 files; KS-1278: 4 files).
- KS-1333's measurement: already a number (`index.ts:1317`, `:1439`, `:1451`, `:881`).
- KS-1186 has an unraised Ornith PASS. KS-1387 and KS-1149 are already fixed.

**TESTED**
- Every golden in a `--shared` scratch clone at `57fa9e31d7ce` (tree `6d96b6e8…`, the same tree as develop `14d40d4455c7`; develop re-read by `ls-remote` at 11:35 AEDT). Each was tested:
  - red at the tip by assertion, green with the golden;
  - with the full service suite before and after (originate 90/1062/0 → 91/1066/0; anchoring 26/353/1 → 28/364/1, the same pre-existing failure);
  - with tsc rc 0;
  - with `git apply --check` strict;
  - for KS-723, also with generate-openapi (`--check` PASS at the tip) and spec-examples OK.
- Each brief's test block was byte-compared to the measured file (5/5 EQUAL). KS-1278's and KS-948's fences were assembled and applied strict; KS-1278's files are sha1-identical to the golden.
- `night/build_input.sh` ran rc 0 on KS-723-tx with the prompt source "WEDNESDAY BRIEF" (0 expected `+` lines, 3 red cells).
- `spark/round.sh --dry-run` results are in the Addendum.

**HOW**
- `pull.py` (paginated `first:100`), `tab.py` (round counts from `night/done.md`/`SPARK_LADDER.md` plus holder flags), `show.py`/`show2.py`/`fix.py` (fix-section extraction). These lived in the scratchpad and are not filed.
- `tasks/code_patch/prepare_clone.sh` farmed node_modules into the scratch clone. Goldens were written as python line-asserted edits, and diffs were taken with `git add -N`.

## UNMEASURED

- About 200 tickets were judged from title + fix-section + the prior screen, not opened whole this session.
- Open PRs were NOT censused (GitHub was not read). Wednesday's queue step should run `prs.py` on the briefs' files.
- No Schemathesis, live stack or real Postgres. KS-1278's `$executeRaw` affected-count semantics and KS-723's declared shapes versus real bodies are reasoned.
- node_modules come from the checkout's own install (HEAD `c56dd7c32`), not a fresh `npm ci`.
