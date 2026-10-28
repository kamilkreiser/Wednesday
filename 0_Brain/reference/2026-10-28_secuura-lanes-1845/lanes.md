# Secuura Platform K wave-6 lanes - 2026-10-28 ~18:30-18:55 AEDT (drafter, read-only)

Drafter: claude-sonnet-5-5, row C8 (lane-sweep drafter for Wednesday), gauge 73% (from the prompt). Nothing was written to any board, repo, mail or pane. Written: this report and three lane briefs (lanes 25, 26, 27) under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/`. A scratch clone at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/lanes-1845/c` (a NEW path under `lanes-1845/`, which did not exist: `ls` rc 1 before the clone; `git -C <clone> rev-parse --show-toplevel` equalled the path before any fetch) was used for `ls-remote`, `fetch` of develop and of the PR heads, `show`, `grep`, `ls-tree`, `diff`, `patch-id`, `log`; it is removed at the end (see the last line of this file). Scratch files (pull JSON, scripts) live in the session scratchpad. Nothing under `!CODING/` was touched. The Linear key was read inside a Python process by `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-28_secuura-lanes-1700/tools/pull.py` (reused unchanged) and never printed. **`gh` was not used and no GitHub token was read.** No suite, build, mutant or script of the repo was run: every claim about source is a read at the sha.

## BLUF

1. **Develop read from origin: `bd6697e079fce41db6b21e094a9eddb3d0e1d08e`** (`git ls-remote origin refs/heads/develop` in the scratch clone, then `fetch origin develop`, `rev-parse FETCH_HEAD` equal).
2. **Board: 693 open KS issues** (backlog+unstarted+started; 693 unique ids of 693 nodes; **7 pages** of 100, `hasNextPage` false on the last, not capped): Backlog 348, In Progress 271, In Review 46, Todo 25, Blocked 3. Backlog+Todo = 373; minus Peter's 12 and Stuart's 7 = **354 candidates** (assignees in the 373: our account 241, unassigned 113, Peter 12, Stuart 7).
3. **FOUR lanes, not six, reached the evidence bar** (three briefed, one not): every other ticket I opened either carries a decision, a ruling, an unmeasured cause, a file owned by a live seat, or a fix shape the ticket refuses to choose. Pairwise file-overlap total 0; no lane path in any live-seat brief, any wave-5 lane, or the open-looking PR set; a planted-overlap control fires (1).
   - **25 / Seat T 5th (Sonnet, C2), briefed:** originate real-Postgres integration pins: KS-1340 (DSN query-string bypass of the disposable-DB guard), KS-1499 F1/F2/F5, KS-1600 item 1. Three test files, no product file.
   - **26 / Seat U 4th (Sonnet, C2), briefed:** KS-1783 (three ks1634 cells that cannot tell a real hash from a placeholder) and KS-1494 items 1 and 4 (auth integration guard bypass and tsc errors). Four test files, no product file.
   - **27 / Seat K 13th (Sonnet, C2, tier-1 gate after), briefed:** KS-1458 items 1, 2, 4 (a wrong comment, a wrong test header, a TS1192 import) and KS-1459 item 2 (local level order -> shared, with a proof table). `users.ts` comment/import hunks plus one test file.
   - **28 / unassigned seat (Sonnet, C2), NOT briefed:** KS-1343 (eight docs overstatements), KS-1415 item 2 (a count cell), KS-1039 (re-aim a permanently red e2e assertion). Section 2.
4. **Spark-briefable single-file candidates: 10** (section 5), each with file:line read at the tip; nine of the ten sit inside lanes 26/27/28 (Wednesday strikes the item if she sends it to the Spark), as in the last sweep.
5. **A cheap fact for the board seat:** the open-PR instrument without `gh` is an UPPER bound (see section 1): of 1699 PR head refs, 1361 develop commits carry `(#N)`, 338 PRs matched no commit, and 251 of those settle by ancestry, blob equality or `patch-id`; **87 remain "open-looking"**, of which only about 10 are dated 2026-10-01 or later (`#572`, `#1726` dependency bumps, `#1775-#1778` the live seats' own PRs, and four more). Two that touch my files (`#930` for `users.ts`, `#898` for `prometheus_targets.test.sh`) are shown superseded in the develop log (`supersedes #930`; `#900` landed KS-971's k6 slot isolation).

## 1. Counts and the open-PR instrument

**FOUND** 693 open KS issues. Predicate: `issues(first:100, after:$cursor, filter:{team:{key:{eq:"KS"}}, state:{type:{in:["backlog","unstarted","started"]}}})`, cursor loop to `hasNextPage` false: **7 pages**, 693 nodes, 693 unique ids (pull.py's own print: `7 693 693`). `comments(first:50)` read per ticket. 135 of the 354 candidates carry at least one comment.
The previous sweep read 696 (7 pages); the board moved by three since 17:00.
**HOW (screen):** a flag screen over the 354 (decision words in title and body at most 1: `[Decision]`, `decide`, `Kam's call`, `ruling`, `POLICY`, `QUESTION`, `production`, `customer`, `Peter`, `Stuart`; a Fix/Recommendation/Suggested/Acceptance heading; 1-6 named file paths) gave 104; a second heading screen gave ~100 more; I then read the BLUF and fix section of about 45 tickets and the full body of about 20. **The other ~300 were read by title and flags only.** This is a floor, not a census.
**Open PRs (no `gh`):** `git ls-remote origin refs/heads/develop 'refs/pull/*/head'` -> 1699 PR heads (rc 0; a control: develop's own line present). Merged-by-subject: 1361 distinct `(#N)` and `Merge pull request #N` numbers in `git log --format='%s%n%b' bd6697e` -> 338 PRs unmatched. Their heads were fetched (`+refs/pull/N/head:refs/prs/N`, rc 0, 338 refs) and each diffed against its merge-base with develop. A PR counts as SETTLED if its head is an ancestor of develop (20), every changed file's blob at the head equals develop's (40, plus 2 empty), or its `git patch-id --stable` equals a develop commit's since 2026-08-15 (229; 1210 develop patch-ids). **87 are not settled; their union is 622 distinct paths** and is what every lane was checked against. It over-counts (closed-unmerged and superseded PRs stay in it) and cannot under-count a PR whose head differs from develop AND whose patch is not in develop since 2026-08-15 only if it is older than that; the 51 unsettled PRs dated before 2026-09-01 were not listed path by path.
**Files of the live seats:** their file sets were NOT available (as told); I avoided their DIRECTORIES entirely (api-gateway, auth social providers, nft-certificate, tenant-provisioning, packages/shared, services/security, Blockchain/Testing, scripts/audit, systemTest, stack-slot and `check-stack-safety`), and compared full paths with every path named in the six wave-5 lane briefs and R 6th's brief (115 paths): 0 hits.

## 2. The lanes

| lane | seat | slug | tickets | model, row |
|---|---|---|---|---|
| 25 | Seat T 5th | `originate_integration_guard_query_bypass_rls_pins_and_org_id_cells` | KS-1340, KS-1499 (F1 F2 F5), KS-1600 (item 1) | sonnet 5.5, C2 |
| 26 | Seat U 4th | `ks1783_ks1494_ks1634_real_hash_cells_and_auth_integration_guard` | KS-1783, KS-1494 (items 1, 4) | sonnet 5.5, C2 |
| 27 | Seat K 13th | `ks1458_ks1459_auth_users_route_comments_and_shared_level_order` | KS-1458 (items 1, 2, 4), KS-1459 (item 2) | sonnet 5.5, C2 (+ tier-1 Opus gate) |
| 28 | (not briefed) | `docs_overstatements_prometheus_count_cell_e2e_echo_assertion` | KS-1343, KS-1415 (item 2), KS-1039 | sonnet 5.5, C2 |

Seat letters and ordinals: the live letters are R, X, Y, AA, W, Z, S, D; T, U, K have `inbox_routing.conf` lines (`Secuura/Blockchain-T|U|K|secuura-blockchain@agentmail.to|yes`). **Ordinal greps** `/usr/bin/grep -i -c 'Seat <L> <N>'` over history.md and briefs_staged: `Seat T 4th` 3 and 5; `T 5th` 0 and 0, `T 6th` 0 and 0; `U 3rd` 2 and 4; `U 4th` 0 and 0, `U 5th` 0 and 0; `K 12th` 1 and 0; `K 13th` 0 and 0, `K 14th` 0 and 0. Positive control `Seat S 4th`: 3 and 57. Highest ordinals seen per letter by a regex pass: T 4, U 3, K 12. So T 5th, U 4th, K 13th.

| ticket | files (tip `bd6697e079fc`) | why it needs no Kam ruling (quoted) | routing row | risk |
|---|---|---|---|---|
| KS-1340 | `services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts` (guard `:185-:200`) | "Fix shape (not chosen here): Parse the DSN's query parameters as well as its authority, and apply the same host and port predicate to whichever finally wins." (a test guard, "Minor") | C2 Sonnet | the same hole exists at `ks1263...:591` (lane 25's file, not KS-1340's): flagged, not fixed |
| KS-1499 F1 F2 F5 | `.../ks1263-multi-write-rolls-back.integration.test.ts` (`:73`, `:89`, `:96`, `:174`, `:372`, `:583`) | "One small test-only PR, test first. Close F1 and F2 in the file itself; settle F5 by reading the KS-597 form too ... No product file is involved." | C2 | N1 (a decision) held out; real Postgres needed |
| KS-1600 item 1 | `.../ks1594-admin-mint-provisioning-and-org-bound.integration.test.ts` (`:288-:296`) | "**The implementation is correct today** - every item below is test coverage ... The fix (the gate's own minimal fix, two cells)" | C2 | item 2 (forged `x-tenant-id` reaches the router) is an untested observation, held out; mutants R9/R1/R7 are one-line descriptions only |
| KS-1783 | three `ks1634-*` originate tests (`:117`, `:107`, `:102`) | "Facts only. No fix is proposed." BUT the board already used the fix (`REAL_TX_SHAPE`, PR #1748) for two cells of the same file; test-only | C2 (Spark-sized, in-process) | measure-first: only one of three cells was measured by the ticket |
| KS-1494 items 1, 4 | `services/auth/integration/ks968-platform-admin-seed-with-both-rows.integration.ts` (`:29-:36`) | "Recommendation: One small PR: fix the guard (validate the parsed connection config, or reject any query string) ... either type-check the integration file or add it to `tsconfig.test.json`'s include." | C2 | items 2, 3 are in `userRepo.ts` (a credential-handling product file), item 5 needs a ruling: held out; `tsconfig.test.json` NOT granted |
| KS-1458 items 1, 2, 4 | `services/auth/src/routes/users.ts` (`:1177-:1178`), `.../ks1006-mfa-disable-refuses-when-no-secret-is-stored.test.ts` (`:10-:12`, `:62`) | "Items 1 and 2 are comment-only; item 3 needs a ruling." + comment: "Fix: `import * as userRepo from ...`" | C2 (items 1, 2, 4 Spark-sized) | an auth route file: tier-1 gate whichever model builds it; item 3 (an MFA-less account has no way to turn MFA off) is a ruling, held out |
| KS-1459 item 2 | `users.ts` (`:1376`, `:1385-:1386`, `:1488-:1489`, comments `:1374-:1375`, `:1484-:1485`) | "Do 2 as a comment-and-import fix." / "Replace the local list with the shared one and fix the comment." | C2 | must be PROVEN behaviour-neutral by a truth table; `VERIFICATION_LEVEL_ORDER` found at `policy-engine.ts:22` and `verification/index.ts:13`, NOT found by `grep -n -i` in `packages/shared/src/index.ts`: a written STOP if it is not at the package root (R 6th owns `packages/shared`) |
| KS-1343 | `docs/MULTI-TENANCY.md`, `docs/RLS-FAIL-CLOSED-PLAN.md` | "Eight non-blocking notes ... Done when: N-1286-3 and N-1286-4's overstatements are narrowed to what the code does" | C2 (doc_patch-shaped; Ornith 1.5 per model-routing section 3 line 3) | docs peers read: narrowing only, add no new claim; "off everywhere" must stay qualified "in the repository" (the gate could not run `az`) |
| KS-1415 item 2 | `scripts/__tests__/prometheus_targets.test.sh` (`:88-:90`, `:119-:121`) | "Fix shape (not applied here): a per-file count cell - `grep -c 'nginx-gateway:6882' <file>` asserted `== 0` ... Keep the existing first-line pin as well." | C2 (Spark-sized, in-process) | item 1 lives in the two shared HTML docs: held out |
| KS-1039 | `tests/e2e/tests/auth-exhaustive.spec.ts` (`:734` cell, `:751`) | "Suggested fix: Re-aim it at what it means to assert: no SQL error and `status < 500` (both already true), or assert the stored value equals the exact input. The output-escaping question is separate" | C2 | the proof is an e2e run against a stack (QUESTION: slot); the choice between the two assertions is the seat's, stated in the PR |

Lane 28 files: `Blockchain/Dev/docs/MULTI-TENANCY.md`, `Blockchain/Dev/docs/RLS-FAIL-CLOSED-PLAN.md`, `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh`, `Blockchain/Dev/tests/e2e/tests/auth-exhaustive.spec.ts`, plus the two shared HTML docs append-only for KS-1415 and KS-1039's test changes. The three tickets are three PRs. KS-1343 and KS-1039 are UNASSIGNED, KS-1415 is on our account.
**Routing rationale (model-routing section 4):** none of the lanes is Spark-routed: lanes 25-26 need a real Postgres or a mutant-on-a-copy proof (section 3 line 2 fails), lane 27 is an auth route file (section 3's auth rule: Spark MAY take a spelled-out mechanical edit, always with a tier-1 Opus gate), lane 28's e2e needs a stack. **Not Opus:** nothing here is an auth/credential DESIGN decision or a destroying path (P1-P4 all NO per the brief's routing receipt).

## 3. Disjointness

Script (scratchpad `lanes.json`, one pass): every lane path `git cat-file -e bd6697e079fc:<path>` rc 0 (13 of 13 exist); pairwise intersection of the four lanes' path sets; each path against `unsettled_files.json` (the 87 PRs' 622 paths), against the 115 paths named in the six wave-5 briefs and R 6th's brief, and against the live-seat directory list (section 1).

| | 25 | 26 | 27 | 28 | open-looking PRs | wave-5 + R 6th paths | live-seat dirs |
|---|---|---|---|---|---|---|---|
| 25 | - | 0 | 0 | 0 | 0 | 0 | 0 |
| 26 | 0 | - | 0 | 0 | 0 | 0 | 0 |
| 27 | 0 | 0 | - | 0 | 1 path (`users.ts` in `#930`) | 0 | 0 |
| 28 | 0 | 0 | 0 | - | 1 path (`prometheus_targets.test.sh` in `#898`) | 0 | 0 |

Pairwise overlap total 0. **Control:** lane 25's set plus one lane-26 file, intersected with lane 26's: 1 (fires).
The two nonzero cells are superseded PRs: `#930` (KS-1052 read-back, 2026-09-10) is named in the develop log as "supersedes #930" (`KS-1052 (r2)`, log line 27614 of the saved `git log` body); `#898` ("slot-isolate the k6 harness", 2026-09-07) was landed by `#900` (log: `Merge pull request #900 from Secuura/feature/ks-971-k6-harness-slot-isolation`; `056a98cf5 fix(KS-971)` is the last commit to touch the file in that window). Both are cited in the briefs; QUEUE 0 re-runs the intersection against `gh pr list` at boot.
**Same-service adjacency (not an overlap):** lane 27 edits `services/auth/src/routes/users.ts`, a file R 6th's PR C reaches by behaviour only (R 6th's brief, lines 93 and 251: `users.ts:993` "is NOT edited"); lane 26 edits `services/auth/integration/`, lane 25 the originate integration files next to Seat W 5th's `ks1557-055-backfill.integration.test.ts`. Lanes 25 and 26 each fix a loopback guard bypass by the same method: lane 26's brief tells the seat to match lane 25's decision.

## 4. Rejected and carded (reason; most were read to the BLUF and fix section, not in full)

| ticket | verdict | reason |
|---|---|---|
| KS-1323 | reject (not in the repo) | `push24.sh` and its siblings are seat tooling outside the repo: `git ls-tree` at the tip has no `push2x.sh`; Wednesday's tooling |
| KS-1030 | reject (collision, size) | needs root `package.json` (touched by open PR `#1726`, a dependency bump) plus new real-Postgres SQL scenarios for 048 |
| KS-1105, KS-1104, KS-1106 | reject (customer-facing words) | placeholder or accessible-name text on login/verifier screens |
| KS-1048 | card for Wednesday | rewrites a written project rule in two `CLAUDE.md` copies, one outside the repo; "the load-bearing half is 'say so'" is a rule wording choice |
| KS-1606 | reject (outside the repo) | `Setup and System/statusline.sh` is at the workspace root; the ticket says "this seat read it and did not edit it" |
| KS-1338, KS-1251, KS-1329 | reject (collision) | `packages/shared/src/__tests__/entrypoint-corpus.test.ts` is touched by open-looking `#1268` and `packages/shared` is R 6th's directory; KS-1251 needs the root eslint config |
| KS-1255, KS-1458 item 3, KS-1459 items 1 and 3, KS-1654, KS-1681, KS-1530, KS-1764, KS-1755 | card (decision) | each states "decide", "needs a ruling", "a maintainer call", "undecided" or "No shape is chosen" (KS-1255 "Decide the floor from the key formats"; KS-1654 "as a contract change with Platform S in the loop"; KS-1681 "which of the two ... is a maintainer call"; KS-1764 "is undecided") |
| KS-1712 | reject (measure first) | cause unknown, "No fix is proposed", Peter-reported, needs Postgres and a timezone; three cells unnamed |
| KS-1781 | reject (no fix) | "Facts only. No fix is proposed." and "source of neither identified" |
| KS-1718 | card | "make the redaction ... actually protect the generated test-account password, or say in a comment that it is cosmetic" is a choice of intent on credential handling |
| KS-1304 | reject | per-tenant-database routing (flag off, "appears in 0 tracked config files"): a tenancy design surface, Opus C3, not a lane for Sonnet |
| KS-1218 | reject (a choice, and open PR unmeasured) | "Either add the pip upgrade ... or pin pip"; a comment says schemathesis moved to 4.30.1 in `#1492` (not merged on 2026-10-12): not read |
| KS-1356 | card | "it's your suite, so whichever approach you'd prefer" |
| KS-1420, KS-1423 | reject (partial, gate kit) | six minors each across docs HTML (shared) and a gate-kit file in Wednesday's tree; not read below the minors |
| KS-1494 items 2, 3, 5 | held out | `userRepo.ts` credential-handling product file; item 5 changes seed behaviour (ruling) |
| KS-1600 item 2, KS-1499 N1 | held out | an untested observation about middleware wiring; "a decision, not code" |
| Wave-5 tickets (KS-1240, 1382, 1472, 1537, 1702, 1588, 1394, 1113) and R 6th's | excluded | live |
| Peter's 12 and Stuart's 7 | excluded | never queued |
| Security / tenancy tickets (KS-1688 to KS-1704, KS-1572, KS-1573, KS-1604, KS-1535, KS-1574, KS-1581, KS-1604, ...) | not read below the title | Opus C3/C4 at best; most name "Kam's call"; excluded by the prompt (auth/credential DESIGN, production) |

**Candidate cards for Wednesday to put to Kam** (one decision each, quoted): KS-1048's written exception (the wording is given, the rule is Kam's file); KS-1458 item 3 (leave / admin reset / re-enrol); KS-1255 (the floor); KS-1681 (add a deploy-preconditions doc or cite an external one). None blocks lanes 25-28.

## 5. Spark-briefable single-file candidates (do not brief; for Wednesday)

Predicate (model-routing section 3, as used in wave 4): one product or test file, the ticket or a sibling PR spells out the fix, a runnable test nearby, NOT an auth/credential design surface. Evidence is `git show bd6697e079fc:<path> | sed -n` / `grep -n -i` at the tip; nothing run.

| # | ticket | file:line | fix shape | test nearby | caveat |
|---|---|---|---|---|---|
| 1 | KS-1458 item 1 | `Blockchain/Dev/services/auth/src/routes/users.ts:1177-1178` | rewrite the sentence "an account in it can still disable through POST /api/auth/mfa/disable (password or backup code)" to what `routes/mfa.ts` allows; comment only | the ks1006 suite (mocked, in-process) | an auth route file: PR is a tier-1 gate; lane 27 item 1 |
| 2 | KS-1458 item 2 | `.../__tests__/ks1006-mfa-disable-refuses-when-no-secret-is-stored.test.ts:10-12` | replace "a latent shape, not a live bypass" and the "can still use" sentence with the `decryptMfaSecret` fact (`userRepo.ts:172-189`); comment only | same file | lane 27 item 1 |
| 3 | KS-1458 item 4 | same file `:62` | `import userRepo from '../repositories/userRepo'` -> `import * as userRepo from ...` (comment on the ticket) | the same suite plus `tsc` on a copy | lane 27 item 1; check `export default` absent (`-i`) |
| 4 | KS-1783 | `.../originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts:117-125` | add `expect(<reply hash>).toMatch(REAL_TX_SHAPE)` in the cell (`REAL_TX_SHAPE` already declared at `:49`; precedent at `:159`, `:173`) | the file itself (in-process) | measure whether the reply echoes the hash; lane 26 item 1 |
| 5 | KS-1783 | `.../ks1634-a-simulated-anchor-verified-by-hash-verify-route.test.ts:107-112` | same, but declare the shape beside `REAL_TX` (`:45`; `REAL_TX_SHAPE` absent from the file) | the file itself | lane 26 item 1 |
| 6 | KS-1783 | `.../ks1634-a-simulated-anchor-verified-by-hash.test.ts:102-107` | same (`REAL_TX` at `:44`) | the file itself | lane 26 item 1 |
| 7 | KS-1415 item 2 | `Blockchain/Dev/scripts/__tests__/prometheus_targets.test.sh:88-90` and `:119-121` | add `expect "<file> carries no active nginx-gateway:6882 line" "0" "$(grep -c 'nginx-gateway:6882' <file>)"` beside each `grep -m1` pin (the two example files are read from `$DEV_ROOT/../../observability/...`) | the script itself (bash 3.2, `./prometheus_targets.test.sh`) | the count must exclude commented lines if the examples carry one; item 1 of the ticket (HTML docs) is NOT this |
| 8 | KS-1494 item 1 | `Blockchain/Dev/services/auth/integration/ks968-platform-admin-seed-with-both-rows.integration.ts:29-32` | judge the parsed host/port (`pg-connection-string`) or refuse any query string naming `host`/`port` | a scratch `node`/`tsx` run with a planted DSN (refusal cells) | a database-safety guard: tier-1 gate; lane 26 item 2 |
| 9 | KS-1340 | `.../originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts:185-200` | same fix for `u.hostname` at `:186` and `u.port` at `:193` | the guard throws before any connection; the rest of the suite needs Postgres | not runnable by an in-process checker without extracting the predicate; lane 25 item 1 |
| 10 | KS-1039 | `Blockchain/Dev/tests/e2e/tests/auth-exhaustive.spec.ts:751` | replace `expect(body.toLowerCase()).not.toContain('drop table')` with `status < 500` plus no `sql`/`syntax error` (both already asserted at `:747-748`), or assert the stored value equals the input | an e2e run: none in-process | the checker cannot run Playwright against a stack; lane 28 |

Nearest misses (not briefable): KS-1459 item 2 (needs the proof table and a package-root check), KS-1499 and KS-1600 (real Postgres), KS-1343 (doc_patch tier: Ornith's, not the Spark's, per model-routing section 3 line 3).

## 6. UNMEASURED (plainly)

- **The live seats' file sets.** Not available to me. The lanes avoid their DIRECTORIES and every path in the wave-5 briefs and R 6th's brief; I did NOT see Z 3rd's `check-stack-safety.sh` 3c/3d or `tenant_isolation_stderr_own_file.test.sh` work, Y 4th's tenant-create files, or S 5th's. A live seat may have widened into a file named here; QUEUE 0 re-runs the PR intersection but cannot see an unpushed worktree.
- **Which PRs are actually open.** No `gh`: the "open-looking" set (87 PRs, 622 paths) is an upper bound; the 51 unsettled PRs dated before 2026-09-01 were not individually read, and a PR whose patch is in develop only after 2026-08-15 patch-id window may be mislabelled either way.
- **Every drafter line number** is a `git show`/`sed -n`/`grep -n -i` reading at `bd6697e079fc`; nothing was executed. Line numbers quoted from tickets (`:1654`, `:1589-1590`, `:172-189`, `:114`, `:147`, `:163`) are the authors' at older shas and were not re-read here except where a section above says so.
- **Whether `pg-connection-string` lets the query string win over the authority** (KS-1494's gate measured it; KS-1340 asserts it; nobody here ran it). Both briefs make the seat measure it.
- **Whether `VERIFICATION_LEVEL_ORDER` is importable from `@secuura/shared`'s package root** (lane 27 QUEUE 2 has a STOP for it).
- **The mutants R9, R1, R7, M5 as diffs** (one-line descriptions in the tickets only; the gate reports at `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-12_gate-pr1490/verdict.md` etc. were not opened).
- **Whether any of the 354 candidates not named here is lane-able.** About 300 were screened by title and flag counts; a keyword screen misses a ticket that states its fix in prose without a heading.
- **Rulings:** no `decision_queue.sh` was run (the prompt says read-only; the briefs' QUEUE 0 runs it). A Kam ruling on any of these tickets would be found there.
- **The briefs' SELF-CHECK line is left blank on purpose** for Wednesday; pane ids are `%__` for Wednesday to fill; HOLDS were copied from lane 24's with the seat identity, the Docker clause and the shared-inbox bullet rewritten, not re-diffed against STANDING_LINES line by line.
- **STANDING_LINES line numbers cited in the HOLDS block** (408, 536, 537, 539, 540, 348, 86) were copied from the lane-24 template, not re-checked.

Clone `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/lanes-1845` removed at the end of the run (see the final message for the `rm` and `ls` results).
