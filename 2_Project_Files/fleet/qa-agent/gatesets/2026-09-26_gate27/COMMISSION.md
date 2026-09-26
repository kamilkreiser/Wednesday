# COMMISSION — DRAFT the round-27 batch gate kit "gate27" over 4 PRs (tiers 2 and 3). Do NOT launch.

Relayed by Wednesday to the drafter on 2026-09-26 (~03:0xZ) as FOUR PRs with heads she read by `ls-remote refs/pull/N/head`: #1278 (KS-1314 fix round, ROUND 2 OF 2 at the
cap), #1285 (KS-766), #1286 (docs, refs KS-1336) and #1287 (KS-1318 + KS-1142). No sibling kit. Shape copied from `gatesets/2026-09-26_gate26T2/` (and gate26T1): JSON pins,
routing-file override, controls both ways with `--invert`, per-PR merge-bases, a declared commit count, a NOT-STACKED check and the key scan; re-keyed to four rows,
an every-open-PR census, a DECLARED dead-open same-blob overlap (#1268) and `--simulate moved` (no older develop can host #1287).

## The batch — every head re-read by the drafter from origin (ls-remote + a fetch into a `--no-local` scratch clone + the PULLS API; all agree)
| PR | ticket | head | commits on merge-base | files | squash subject chars (`<title> (#n)`) | tier — why, from the DIFF |
|---|---|---|---|---|---|---|
| #1278 | KS-1314 | `18cca0a7e0fe1baddcd71cc26f8a10b032da9bd8` | 2 on `4db87c3e4b98` | sheddingCeiling.test.ts +123/-3, readYamlRouting.ts +138/-15 | 116 | **T2**: two systemTest/ test files (no product byte); a CHECKER (parserImportSites + the new callsReadYaml): THE READER RULE. **FIX ROUND — ROUND 2 OF 2, AT THE CAP** (gate26T2 NO GO B-1278-1 SEMICOLON-IN-BRACES, M-1278-a). The seat chose the AST. |
| #1285 | KS-766 | `c7779a33031813cac9dab62abd0cb8fd9d73f2f9` | 1 on `00de57baeb40` | base-image-watch.sh +60/-38 | 85 | **T2**: ONE operator script (not deployed, not imported; named only in a dead workflow's comments). Behaviour moves (the producer is extracted) + two self-test cases; the self-test is the red proof (no docker). |
| #1286 | KS-1336 | `27480bb649477435b4a683059d3fcbded3611377` | 1 on `00de57baeb40` | RLS-FAIL-CLOSED-PLAN.md +26/-10, MULTI-TENANCY.md +65/-24 | 84 | **T3**: two Markdown files, no code. DOC-CLAIM: every changed sentence against the code at develop; NO plan or recommendation may be added (Kam's decision). |
| #1287 | KS-1318 + KS-1142 | `4dac00147f8861250bab6abbea2fec34b14b62f2` | 1 on `e6056de7ed64` | entrypoint-corpus.test.ts +73/-29 | 80 | **T2 follow-up**: ONE test file, byte-identical to blob 8a4ce36a (graded in #1268 rounds 1-2); run on the current develop. #1268 (dead-open) carries the same path at the same blob — DECLARED. |

Linear: every PR links its ticket(s) as `contributes`; none `closes` (linear_reads_1.out); no PR body puts a closing word before a key (gh_read_1.out). No PR is stacked
on another (measured: no head is another's ancestor; every pair's merge-base is on develop).

## Develop at the pin
Pinned over develop **`e6056de7ed640e3a441bc7e33853601bf9040084`** (tree `544b7275c23fc2279349a5fb1f130eb4a8170bb6`), READ by ls-remote and fetched (gate26's eleven squashes over 00de57baeb40, ending #1284). END_TREE **`a0398f96de84fc7c94e3a5357651b1646af21703`** (6 files changed, 485 insertions(+), 119 deletions(-)), identical in all 24 orders (32 merge-tree calls). No sibling kit: END_TREE_WITH_SIBLING == END_TREE.
The launch action's step 3b re-pins on any move (Seat M1 merges on GOs).

## Overlaps — ONE DECLARED (byte-identical), NONE found
- Kit pairs: disjoint (6 pairs). Every other OPEN PR at the pin (22, the PULLS API census): disjoint from every kit path.
- **DECLARED:** dead-open **#1268** (head `5ac42fafeee11dec596e7e7d833ac82b8b478790`, NO GO at its cap in gate26T2) carries #1287's `entrypoint-corpus.test.ts` at the SAME blob `8a4ce36a3a96d2e511faf9b19eba14593d8e99fa` (== #1287's `8a4ce36a3a96d2e511faf9b19eba14593d8e99fa`). Merged-blob target = #1287's head blob. #1268 must close unmerged: merged after #1287 it would land its failed ks781 rule.

## Fleet STOP (READ, bounded region, NOT-FOUND control)
- #1278 `s-b30-ks1314-ff-18cca0a7e0fe-push.out` (7 lines, rc 0): a systemTest/ push, no preflight — NOT APPLICABLE
- #1285 `s-b30-ks766-c7779a330318-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1286 `s-b30-tenantdocs-27480bb64947-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- #1287 `s-b30-corpus-4dac00147f88-push.out` (1305 lines, rc 0): 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60); "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed."
- Declared at 00de57baeb40 (Seat B 30th handover, on #1285's and #1286's pushes; carried by gate26T2's report): 28/0 · 6/0 · 49/0 · 60 of 60. By path class no kit PR changes it:
  #1285 edits a .sh under scripts/ that is not a `*.test.sh` in run-shell-suites.sh's ROOTS and is invoked by no suite (READ) — its own self-test count 20 -> 22 is a SEPARATE count. The gate measures membership (`--list`).

## LEGITIMATE SHAPES — the drafter's predictions (the gate MEASURES every row)
| PR | shape | predicted | predicted-by |
|---|---|---|---|
| #1278 | S0 the captured prettier fixture | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | S6b line comment with ; in braces (fixture) | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | S6d JSDoc with ; in braces (fixture) | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | IE1 import-equals `import y = require(...)` | hits=0 (drafter wanted UNKNOWN) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | CR1 createRequire alias | hits=0 (drafter wanted UNKNOWN) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | TPL dynamic import of a template literal | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | NS namespace import | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | EXS export * from | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | SUB a subpath specifier | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | A4 the gate plant inside the REAL develop config_loader.ts | hits=1 (drafter wanted 1) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | L0 develop config_loader.ts unchanged | callsReadYaml=true (drafter wanted true) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | A2c the only real call replaced (doc comments left) | callsReadYaml=false (drafter wanted false) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | AL1 an alias `const r = readYaml; r(p)` | callsReadYaml=false (drafter wanted UNKNOWN) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | AL2 `readYaml.call(null, p)` | callsReadYaml=false (drafter wanted UNKNOWN) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1278 | DEAD a call inside a never-invoked function | callsReadYaml=true (drafter wanted UNKNOWN) | drafter PROBE (probe1278_1.out: the REAL head function under node 24, typescript 6.0.3; not vitest) |
| #1285 | self-test at the merge-base | rc 0 / PASS 20 FAIL 0; docker shim calls 0 | drafter PROBE (probe1285_1.out: git-archive extracts, /bin/bash 3.2) |
| #1285 | self-test at the head | rc 0 / PASS 22 FAIL 0; docker shim calls 0 | drafter PROBE (probe1285_1.out: git-archive extracts, /bin/bash 3.2) |
| #1285 | self-test test hunk ALONE on the merge-base | rc 12 / PASS 20 FAIL 2; docker shim calls 0 | drafter PROBE (probe1285_1.out: git-archive extracts, /bin/bash 3.2) |
| #1285 | self-test head with the producer clamp restored | rc 12 / PASS 21 FAIL 1; docker shim calls 0 | drafter PROBE (probe1285_1.out: git-archive extracts, /bin/bash 3.2) |
| #1286 | FLAG CENSUS at develop e6056de7ed64 (READ, `git grep`): PROVISION_PER_TENANT_DB appears on 5 line(s), all in code (['Blockchain/Dev/packages/shared/src/db/tenant-pool-manager.ts', 'Blockchain/Dev/services/tenant-provisioning/src/index.ts']) — set in NO config file; MULTI_TENANCY_ENABLED appears in config files ['Blockchain/Dev/deployment/azure/env.demo.json', 'Blockchain/Dev/deployment/azure/env.dev.json', 'Blockchain/Dev/deployment/azure/services.bicep', 'Blockchain/Dev/docker-compose.yml'] | | drafter READ (predict_1.out) |
| #1286 | DOC-CLAIM-TWO-FLAGS (a PREDICTION): the PR writes that MULTI_TENANCY_ENABLED and PROVISION_PER_TENANT_DB are "set in NO configuration file" (MULTI-TENANCY.md key points; RLS-FAIL-CLOSED-PLAN.md) — MULTI_TENANCY_ENABLED is "true" in deployment/azure/env.dev.json, env.demo.json and services.bicep (READ above); the gate measures and rules | | drafter READ (predict_1.out) |
| #1286 | ONBOARDING-CITE (a PREDICTION): a NEW tenant's tenant_config row is written by tenant-provisioning/src/index.ts (`provisionPerTenantDb` at line(s) [245], the INSERT at line(s) [272]), not by startup-migrations.ts, which the corrected onboarding step cites (READ) | | drafter READ (predict_1.out) |
| #1287 | BLOB (READ): head 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa / expected 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa -> EXACT / develop d81265b7f18c4f714a3a9b264ce5099a956bec73 / #1268 head 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa | | drafter READ (predict_1.out) |
| #1287 | K1b CONTENT COUPLING (READ): K1b reads ks781's `const CORPUS = [` from SOURCE TEXT — at develop ks781 is blob e96215365a6d with 25 CORPUS entries; at #1268's head (what rounds 1-2 graded against) 25 entries; the two literals are IDENTICAL | | drafter READ (predict_1.out) |
