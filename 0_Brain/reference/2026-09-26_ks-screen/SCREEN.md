# KS board screen for local models, 2026-09-26 (develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`)

Screening drafter for Wednesday. Read-only on the Secuura repo and board. Nothing was posted, moved, launched, mailed or committed.

## BLUF

- **Board read: 284 distinct KS issues.** That is 264 in backlog+unstarted (3 pages of 100, paginated to `hasNextPage=false`) plus 38 created since 2026-09-25T03:00Z in any state (1 page, to the end), with 18 in both sets. Full description + `comments(first:50)` (sorted client-side) were fetched for all 284. One issue has more than 50 comments (KS-485, a security-review epic that is excluded anyway), so its tail was not read.
- **Titles triaged: 284. Read in full or to the fix shape: 49. Citations opened at d7cdecf1: 9.**
- **Candidates: Ornith 0 · Spark 1 (KS-766) · Claude: everything else read.** The board's residue is almost entirely auth, security, class-wide, decision or live-stack work. Every small, spelled-out item I found fails one clause: no in-process test, it is in a live lane, it is under an open PR, or it is at the round counter.
- **Briefs written: 1**, `briefs/KS-766/KS-766.md` (Spark rung 2: one file, three hunks, self-testing). The golden was EXECUTED in a `git archive` of the tip. E3 alone gives rc 12 (2 FAIL). The full golden gives rc 0 (22 PASS). The ticket's clamp tamper gives rc 12 on exactly the FUTURE cell.

## Exclusions (counts; the lane and decision columns come from a text scan and were then confirmed per ticket where it mattered)

| # | Rule | Count | Tickets |
|---|---|---|---|
| 1 | Live lane (originate / packages/shared / systemTest/performance) | 75 **mention-matched** (an over-count: a description that merely names the path matches). Per-ticket confirmation was done only for tickets read in full. | Confirmed in-lane among those read: KS-1319 (packages/shared walkTimeouts, KS-1155), KS-1306 + KS-1309 (originate `ks597-issuer-organization-id.integration.test.ts`), KS-1326 (perf `capturedChildOutput.ts`), KS-1112 (originate `routes/gdpr.ts`), KS-1304/1305/1312/1293/1298/1299/1321/1310/1311 (originate), KS-1300/1313/1314/1315 (perf), KS-1316/1317/1318/1329/1292 (shared) |
| 2 | Target file under an OPEN PR | **37 open PRs** (GitHub API, all pages; file lists in `prs.txt`) | KS-1324 + KS-1088 + KS-1302 + KS-1303 (#1250 `run-shell-suites.sh` / `run_shell_suites.test.sh`), KS-1327 (#1272 `kyc/src/index.ts`), KS-981 + KS-982 (#989 `fixtures/provision.ts`/`pre-suite.ts`, #927 `pre_suite.test.sh`), KS-1297 (#1253), KS-1295 (#1267), KS-1313 (#1245), KS-1326 (#1245), KS-1315 (#1265), KS-1316/1318 (#1268), KS-1310/1311 (#1262), KS-1321 (#1273) |
| 3 | Assigned to Peter or Stuart | **19** | KS-61 101 135 139 188 239 492 502 525 568 571 572 588 590 608 983 984 985 1042 |
| 3 | Decision / Kam / owner's-call marker (label, `[Decision]`/`QUESTION` title, or text) | **19 flagged by scan**, plus these found by reading: KS-1322 ("the owner's call"), KS-1243 ("decide whether the family is meant to exist"), KS-1249 ("decide the vocabulary"), KS-1225 ("decide the shape"), KS-1224 ("decide whether the pin is stale"), KS-1328 ("fix shapes, not chosen here"), KS-1320 ("proposals, not ratified"), KS-1218 ("either ... or"), KS-752 ("Peter's triage input wanted"), KS-655 ("Kam's call") | scan: KS-239 329 485 491 582 588 593 608 651 658 770 782 834 997 1116 1141 1162 1290 1294 |
| 4 | Round counter (done.md rows + `night/READY_*`) | **14 at 2+ rounds**: KS-692 794 884 908 938 987 998 1074 1121 1145 1163 1168 1222 1227. **17 more have 1 round AND a READY file** (already produced, awaiting raise, so not re-briefed): KS-623 747 866 888 960(READY x3) 1009 1090 1108 1186 1190 1196 1205 1212 1219 1220 1221 1250 | |
| 5 | "live sweep owed" in a comment | **1** | KS-1296 |

## Every ticket read in full (or to its fix shape), with tier

| Ticket | Tier | Reason (the clause that decides it) |
|---|---|---|
| **KS-766** | **SPARK** | One file (`Blockchain/Dev/scripts/base-image-watch.sh`), fix shape spelled out by its Done-means, in-process `--self-test`, not auth, 0 open PRs, 0 rounds. It is a 37-line move plus 18 new lines, so it is past Ornith's 3-small-edit ceiling. **Brief written.** |
| KS-1274 | Claude | Fix shape is clear (job 04 `:116` guard, confirmed). But **4 files**: all three trivy suites use a bare `{}` as their CLEAN stub (`container_trivy_failed_scan_is_loud.test.sh:57`, `..._exit_code_env_keeps_findings.test.sh:67`, `..._image_filter.test.sh:76`), so the ticket's fix reds 3 existing controls unless every stub changes. There is also an unmeasured premise: whether real trivy omits `Results` on a clean image (`omitempty`), which decides between the ticket's two keys. |
| KS-755 | Claude | Fix shape NOT given ("I did not finish isolating which"). **Measured today: the cell PASSES at d7cdecf1 in a clean scratch copy (14/14)**, so the red depends on a local `.env` chain (`loadEnvFiles`), not the code. A comment-worthy finding; not a task. |
| KS-1105 | Claude | One line, confirmed at `frontend/admin/src/pages/Login.tsx:81`. But the admin frontend has **no test runner** (package.json has `lint` only, no test files), and it is the admin login's credential field (security rationale). Better as a human one-liner. |
| KS-1104 | Claude | One file (`frontend/verifier/.../VerifyPage.tsx:265-279`, confirmed `hidden sm:inline` labels, no aria-label), and the fix is spelled. But the verifier has **no test runner**, so there is no in-process red. |
| KS-812 | Claude | **Citation stale:** the ticket says `index.ts:21`; the URL is at `:26` and is only a `console.log` of the fallback. The fix gives two options (repoint, or drop the fallback). No tests in `connectors/whatsapp-bot`. The same dead host is also in 3 sibling connectors (euro-office-plugin `api.js:4`, flutter `auth_service.dart:11`, and a doc). |
| KS-1289 | Claude | One line (`Blockchain/Dev/.dockerignore:13` = `tests`, confirmed). The verification is a docker rebuild, and there is no in-process test. |
| KS-1328 | Claude | "Fix shapes, not chosen here" (3 options). A timeout budget has no in-process red. |
| KS-1326 | excluded (lane + PR) | perf `capturedChildOutput.ts`, under #1245. |
| KS-1319 | excluded (lane) | packages/shared walkTimeouts (KS-1155). |
| KS-1306 / KS-1309 / KS-1307 / KS-1308 | excluded (lane) / Claude | originate integration test (needs Postgres) / process findings about PR bodies, no code. |
| KS-1249 / KS-1243 / KS-1225 / KS-1224 / KS-1322 / KS-1320 / KS-1218 | Claude | Each is shaped as "decide" or "owner's call". |
| KS-1323 / KS-765 / KS-655 / KS-939 / KS-940 | Claude | Seat/fleet tooling (push24.sh, merge helper, the launcher): outside the Secuura repo or Kam's call. |
| KS-1113 / KS-1039 / KS-1010 | Claude | Playwright e2e specs need a live stack, so there is no in-process test. KS-1010 is also 5 files. |
| KS-1112 | excluded (lane) | originate `routes/gdpr.ts`, and a decision (align or document). |
| KS-1115 / KS-1030 | Claude | Migrations: one needs a live-row census first, the other needs Postgres. |
| KS-954 | Claude | "Mechanism NOT determined. Reproduce before fixing." |
| KS-1106 / KS-1178 / KS-1191 | Claude | UX design, privacy model, audit-log canonicalisation (security surface, class). |
| KS-1138 / KS-1063 / KS-948 / KS-752 / KS-709 | Claude | CI runner, gate class, 9-suite class, run.py eager-eval needing an invalid-run rehearsal, Akto class. |
| KS-1082 | Claude | Guard exists only on unmerged #896; `systemTest/` is Peter's. |
| KS-1327 | excluded (PR) | #1272 touches `kyc/src/index.ts`. |
| KS-1162 / KS-918 | Claude | Retired workflows plus a slot-rule decision / an auth package.json and lockfile move. |
| KS-1294 / KS-1301 | done | Both are already shipped (#1247, #1255 merged); nothing is left for a model. |

## Briefs written

1. `briefs/KS-766/KS-766.md`: base-image-watch self-test cannot red the DB-age PRODUCER. It is **Spark rung 2**. The golden is `briefs/KS-766/golden.diff` (sha256 prefix `12bba2fd25f273d1`); the drafter checked it byte-equal to the brief's diff block.

No Ornith brief: no ticket passed all five Ornith clauses. I did not stretch a Claude-class item to fill the quota.

## Side findings worth a board comment (not posted; Wednesday's call)

- **KS-755:** the "standing red" does not reproduce at d7cdecf1 in a clean copy (14/14 pass). The cause is likely environmental (the `.env` chain in `src/config/env.ts:88-111`). The ticket may be stale or need re-scoping.
- **KS-812:** the line citation is stale (`:21` -> `:26`), and the dead host is in 3 more connector files.
- **KS-1274:** the ticket's fix shape reds the three existing trivy suites' clean controls (they stub a bare `{}`). The ticket should say so.
- **base-image-watch.sh `:34-:36`:** the header claims 18 self-test PASS lines, but the tip has 20 (measured).

## NOT MEASURED

1. The lane rule was applied by a text scan (75 matches, an over-count) and then confirmed by reading only for the 49 tickets read in full. The ~235 tickets triaged by title alone were ruled out on title shape (auth/OAuth/security, class, decision, feature, live-stack), not by opening their files.
2. KS-485's comments past the first 50 were not read.
3. For tickets read to the fix shape only (description cut at 1.1k to 1.8k chars: KS-1191, 1178, 1063, 948, 709, 655, 1082, 1327, 1224, 1138, 1115, 1112, 1113, 1106, 1030, 954, 1010, 939, 940, 1162, 918), the verdict rests on the part read.
4. The open-PR check compares file paths only, not hunks. A PR editing the same file in a disjoint region still counts as an exclusion.
5. For KS-766, no `build_input.sh`, Spark round or `spark_checker.sh` was run, and neither was the full docker path (see the brief's UNMEASURED).
6. The round counter was matched by ticket id at line start in `done.md` plus `READY_*<id>*` filenames. Rows naming a ticket elsewhere in a line, and quarantined READY files, were not counted.
7. Linear `state.type` for the "In Progress" tickets created since 09-25 was not re-checked against seats' live claims beyond their open PRs.

Artefacts in this directory: `board.json` (the ids and states of all 284), `full.json` (descriptions + comments), `tags.json` (the exclusion scan), `prs.txt` (37 open PRs + files), `biw/` (the golden, its variants and the self-test run logs), `scratch/` and `tree/` (git-archive copies of the tip, used only to execute tests).
