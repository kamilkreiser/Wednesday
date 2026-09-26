# Gateset 2026-09-26_gate27 — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing and wrote nothing inside any project folder or /Volumes/DevMASTER/WEDNESDAY.
It wrote only under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate27/` (this kit), the scratch clone `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g27_sp/clone.git` (a `--no-local` bare clone, no alternates), the control workdirs
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g27_controls_*`, and the probe dirs `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g27_probe1278/` (a SYMLINK to the Secuura checkout's systemTest/performance/node_modules, read-only use) and
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/g27_probe1285*/` (git-archive extracts). The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --no-local` as a source).

**gate27 = FOUR PRs, tiers 2 and 3, one kit, no sibling.** Heads Wednesday relayed (ls-remote at 03:0xZ) re-read here by TWO instruments at the pin (ls-remote AND the PULLS API, and fetched): all agree.

| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | squash subject chars | why this tier (from the DIFF) |
|---|---|---|---|---|---|---|
| #1278 | KS-1314 | T2 | `18cca0a7e0fe1baddcd71cc26f8a10b032da9bd8` | 2 on `4db87c3e4b98` | 116 | two systemTest/ test files; a CHECKER (reader rule). **FIX ROUND — round 2 of 2, at the cap.** The AST replaced the text joiner. |
| #1285 | KS-766 | T2 | `c7779a33031813cac9dab62abd0cb8fd9d73f2f9` | 1 on `00de57baeb40` | 85 | one operator script (no service imports it, no deploy runs it); its self-test is the red proof (no docker). |
| #1286 | KS-1336 | T3 | `27480bb649477435b4a683059d3fcbded3611377` | 1 on `00de57baeb40` | 84 | **T3** — two Markdown files, no code: every changed sentence vs the code; no plan may be added. |
| #1287 | KS-1318 + KS-1142 | T2 | `4dac00147f8861250bab6abbea2fec34b14b62f2` | 1 on `e6056de7ed64` | 80 | one test file == blob `8a4ce36a` (graded twice in #1268); run on the current develop. |

Routing `QA/Secuura-batch1278`. GO string `GO: merge #1278, #1285, #1286, #1287 batch` (or the subset). All go to a MERGE SEAT (Seat L7 wrapped; Seat B 30th is building).

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4). `--check` rc 0 (all guards pass:).
  - Controls: **124 controls, OK 124, MISMATCH 0** normally (rc 0); **OK 0, MISMATCH 124** under `--invert` (rc 1 — by design every control must flip).
- **Pinned over develop `e6056de7ed640e3a441bc7e33853601bf9040084`** (tree `544b7275c23fc2279349a5fb1f130eb4a8170bb6`) — read by ls-remote AND fetched AND agreed: it is the `e6056de7ed64` you named (#1284's squash, the last of gate26's eleven).
  - END_TREE **`a0398f96de84fc7c94e3a5357651b1646af21703`** (6 files changed, 485 insertions(+), 119 deletions(-)), identical in all 24 orders (32 merge-tree calls). No sibling kit, so END_TREE_WITH_SIBLING == END_TREE (measured).
- **OVERLAPS — pairwise, measured:** the 6 kit pairs disjoint; every kit path disjoint from ALL 22 other open PRs (PULLS API census, incl. dead-open #1245/#1241, Seat L5's #1250/#1253, dependabot); NOT STACKED (no head is another's ancestor; every pair's merge-base is on develop).
  - **ONE DECLARED overlap:** dead-open **#1268** (NO GO at its cap, still OPEN, head `5ac42fafeee1`) carries #1287's `entrypoint-corpus.test.ts` at the **same blob** `8a4ce36a3a96d2e511faf9b19eba14593d8e99fa` — asserted byte-identical in predict (hard). It cannot change what lands; but **#1268 must close unmerged** (merged later it would land its failed ks781 rule). §6.3.
- **#1278 at the cap (round 2 of 2) — the decisive item (PREDICTIONS, drafter_probe1278.sh: the REAL head function under node 24 + typescript 6.0.3, not vitest):**
  - The round-1 blockers look CLOSED at function level: S6b / S6d read 1 hit; the A4 plant inside the real develop config_loader.ts reads 1 hit; A2c (the only real call replaced) makes `callsReadYaml` false. The gate owes both arms through the REAL cells.
  - **NEW candidates under THE READER RULE — unvisited AND unnamed in either file (READ):** `CREATEREQUIRE-ALIAS` (`const req = createRequire(import.meta.url); req('js-yaml')`) reads **0**; `IMPORT-EQUALS` (`import y = require('js-yaml')`) reads **0**. The package is `"type": "module"` — createRequire is the standard ESM way to require CJS; reach today 0 (READ). If the gate finds either REAL (prettier-stable + tsc-clean + actually loads under tsx), the rule says **NO GO — at the cap it ships nothing**. §6.1.
  - callsReadYaml: an alias and `readYaml.call` read false (a loud false red); a call inside a never-invoked function reads **true** (a silent over-report). The loader list is still hand-written (declared).
    - `S6b line comment with ; in braces (fixture) hits=1 want=1 ["import { load, // the raw parser; do not use dump, } from 'js-yaml';"]`
    - `S6d JSDoc with ; in braces (fixture) hits=1 want=1 ["import { /** the raw parser; do not use */ load, dump, } from 'js-yaml';"]`
    - `IE1 import-equals `import y = require(...)` hits=0 want=UNKNOWN []`
    - `CR1 createRequire alias hits=0 want=UNKNOWN []`
    - `A4 the gate plant inside the REAL develop config_loader.ts hits=1 want=1 ["import { load, // the raw parser; do not use dump, } from 'js-yaml';"]`
    - `A2c the only real call replaced (doc comments left) callsReadYaml=false want=false (plant applied: true)`
    - `AL1 an alias `const r = readYaml; r(p)` callsReadYaml=false want=UNKNOWN`
    - `AL2 `readYaml.call(null, p)` callsReadYaml=false want=UNKNOWN`
    - `DEAD a call inside a never-invoked function callsReadYaml=true want=UNKNOWN`
- **#1285 KS-766 (PREDICTIONS, drafter_probe1285.sh: git-archive extracts, /bin/bash 3.2, a docker shim that exits 97):** the seat's red proof reproduces exactly.
    - `armT: the test hunk applied to the merge-base rc 0`
    - `armC: the producer clamp restored (anchor found once)`
    - `base: rc 0 | PASS 20 FAIL 0 | anchored ^PASS 0 | docker shim calls 0 | last: SELF-TEST PASSED — the gate fails on every known-bad input above.`
    - `head: rc 0 | PASS 22 FAIL 0 | anchored ^PASS 0 | docker shim calls 0 | last: SELF-TEST PASSED — the gate fails on every known-bad input above.`
    - `armT: rc 12 | PASS 20 FAIL 2 | anchored ^PASS 0 | docker shim calls 0 | last: SELF-TEST FAILED (2) — do not trust this gate until it is fixed.`
    - `armC: rc 12 | PASS 21 FAIL 1 | anchored ^PASS 0 | docker shim calls 0 | last: SELF-TEST FAILED (1) — do not trust this gate until it is fixed.`
  - **Fleet count: UNCHANGED (READ by path class).** base-image-watch.sh is not a `*.test.sh` in run-shell-suites.sh's ROOTS (scripts/__tests__, systemTest/__tests__) and no suite invokes `--self-test`; its own 20 -> 22 is a SEPARATE count. The gate measures membership with `--list` (§6.4).
- **#1286 docs, T3 — a PREDICTED FALSE NEW SENTENCE (READ):**
    - FLAG CENSUS at develop e6056de7ed64 (READ, `git grep`): PROVISION_PER_TENANT_DB appears on 5 line(s), all in code (['Blockchain/Dev/packages/shared/src/db/tenant-pool-manager.ts', 'Blockchain/Dev/services/tenant-provisioning/src/index.ts']) — set in NO config file; MULTI_TENANCY_ENABLED appears in config files ['Blockchain/Dev/deployment/azure/env.demo.json', 'Blockchain/Dev/deployment/azure/env.dev.json', 'Blockchai
    - DOC-CLAIM-TWO-FLAGS (a PREDICTION): the PR writes that MULTI_TENANCY_ENABLED and PROVISION_PER_TENANT_DB are "set in NO configuration file" (MULTI-TENANCY.md key points; RLS-FAIL-CLOSED-PLAN.md) — MULTI_TENANCY_ENABLED is "true" in deployment/azure/env.dev.json, env.demo.json and services.bicep (READ above); the gate measures and rules
    - startup-migrations.ts at develop: the tenant_config block opens at line [1116] and the seed log line is [1145] — the PR cites :1116-1144 (READ); the block seeds a FIXED list of 8 tenant ids at boot
    - ONBOARDING-CITE (a PREDICTION): a NEW tenant's tenant_config row is written by tenant-provisioning/src/index.ts (`provisionPerTenantDb` at line(s) [245], the INSERT at line(s) [272]), not by startup-migrations.ts, which the corrected onboarding step cites (READ)
  - The substance (every tenant on ONE shared DB; per-tenant path dormant) holds by READ: PROVISION_PER_TENANT_DB is set in no config file and gates the per-tenant path at tenant-pool-manager.ts:152 and tenant-provisioning/src/index.ts:245. §6.2.
- **#1287 (READ):**
    - BLOB (READ): head 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa | expected 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa -> EXACT | develop d81265b7f18c4f714a3a9b264ce5099a956bec73 | #1268 head 8a4ce36a3a96d2e511faf9b19eba14593d8e99fa
    - K1b CONTENT COUPLING (READ): K1b reads ks781's `const CORPUS = [` from SOURCE TEXT — at develop ks781 is blob e96215365a6d with 25 CORPUS entries; at #1268's head (what rounds 1-2 graded against) 25 entries; the two literals are IDENTICAL
- **Fleet STOP (READ, bounded region, NOT-FOUND control):** #1278 NOT APPLICABLE (systemTest/ push, 7 lines); #1285 28/0 · 6/0 · 49/0 · 60 of 60; #1286 28/0 · 6/0 · 49/0 · 60 of 60; #1287 28/0 · 6/0 · 49/0 · 60 of 60. Declared at 00de57baeb40 by Seat B 30th (handover "THE FLEET MEASUREMENT — TAKEN"): 28/0 · 6/0 · 49/0 · 60 of 60. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).
- **Linear: every PR links `contributes`; NONE `closes`; no body has a closing word before a key** (linear_reads_1.out, gh_read_1.out). KS-1314, KS-766, KS-1336, KS-1318, KS-1142 all In Progress.
- **MG-3 key scan:** key scan: 4 mandated squash text block(s), each carries only its own key: #1278 ['KS-1314'], #1285 ['KS-766'], #1286 ['KS-1336'], #1287 ['KS-1142', 'KS-1318']. Foreign keys to un-hyphenate if quoted: #1278 KS1300 (body + round-1 message), #1286 KS1055 (body). #1286's own commit says `Refs KS1336` (un-hyphenated) — the mandated block carries `Refs KS-1336`.
- **TITLE-OVER-92:** #1278 is 116 with ` (#1278)`; the kit mandates the drafter's short subject (90, key-scanned). The other three fit (85, 84, 80).

## 2. Pins — predict_1.out (rc 0)
- #1278: 2 commit(s) `c321bcce2a9a`, `18cca0a7e0fe` over `4db87c3e4b98b8e366c3dd60d5f399917bad5086`; 27 behind develop; merged tree `2615e5393dbcd69e85f9fd6f095f5c8fed6de6b9`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1285: 1 commit(s) `c7779a330318` over `00de57baeb405d0081fe8b6f192bd40d35acef61`; 11 behind develop; merged tree `81759e896af289f509270080a139796049451461`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1286: 1 commit(s) `27480bb64947` over `00de57baeb405d0081fe8b6f192bd40d35acef61`; 11 behind develop; merged tree `8e8cd3d3fb36a6240873dd4d13e8d5852cc5f7ce`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- #1287: 1 commit(s) `4dac00147f88` over `e6056de7ed640e3a441bc7e33853601bf9040084`; 0 behind develop; merged tree `13b91e3cf2595f99d56f337049e2dcb54ddb26d2`; every merged blob == its head blob; numstat equal; no mode change; move ∩ own paths EMPTY.
- Simulations: foreign1278 -> REFUSED: FAIL=2; foreign1285 -> REFUSED: FAIL=2; foreign1286 -> REFUSED: FAIL=2; foreign1287 -> REFUSED: FAIL=2; moved -> PASS: FAIL=0. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR's first own file (must REFUSE). No OLDER develop can host #1287 (it sits on the current develop), so gate26's `--simulate predev` became `--simulate moved`; `predev` (00de57baeb40) is still the moved-develop pin in controls D / RC / RD.
- Superseded runs are kept, never deleted: `predict_superseded_preprobefix.out` (the first pinned run, before a probe-text fix; same pins).

## 3. What the gate owes
- Prompt `2026-09-26_secuura-batch1278.prompt.txt` (39411 bytes) — per-PR sections, THE READER RULE, the #1278 cap rule (re-run A4 and A2c; the AST shape table), #1285's four self-test runs under a docker shim, #1286's TIER 3 sentence table, #1287's blob + K1b coupling, the MANDATED SQUASH TEXT blocks and the MG-3 key-set table.
- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1278-g27/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.

## 4. Routing line to add (the drafter did NOT write it)
`QA/Secuura-batch1278|coagent@agentmail.to|yes` → `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (absent at drafting: whole-line grep count 0, with the control line `QA/Secuura-batch1245|coagent@agentmail.to|yes` counting 1 in the same file). Also in PROPOSED_inbox_routing_line.txt.

## 5. The ONE launch command
```
/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate27/repin_and_launch_gate27.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/gate27/launch_qa_secuura_batch1278.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad
```
- Dry run (`--dry-run` appended): repin_dryrun_1.out → DRY RUN COMPLETE 2026-09-26T03:21:15Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add
- If develop moves (a GO lands first), step 3b re-pins in the same action; a move onto an own path, a stack or a pairwise overlap refuses rc 10 (controls RD / RE).
- If you copy the kit into `gatesets/2026-09-26_gate27/`, pass the copied paths: step 0b re-measures and re-fills there.

## 6. Decisions for Wednesday (each with the drafter's recommendation)
1. **#1278 at the cap: CREATEREQUIRE-ALIAS / IMPORT-EQUALS** read 0 and are unnamed. Reach 0 today. *Recommend:* do NOT pre-soften — the rule says reach does not soften; the prompt makes the gate decide REALNESS by instrument (prettier-stable, `npm run lint` clean, actually loads js-yaml under `npx tsx`). Be ready for NO GO at the cap (ships nothing; KS-1314 residue ticketed). If you would rather not lose the proven A4/A2c/S6b fix to a reach-0 shape, that is a Kam-level ruling on the reader rule — not the drafter's or the gate's.
2. **#1286 DOC-CLAIM-TWO-FLAGS:** the PR writes "MULTI_TENANCY_ENABLED and PROVISION_PER_TENANT_DB … set in NO configuration file"; MULTI_TENANCY_ENABLED is `"true"` in deployment/azure/env.dev.json, env.demo.json and services.bicep (READ). The conclusion (shared DB) survives; the sentence does not. *Recommend:* a false NEW sentence in a document whose whole job is correcting false sentences is blocking at T3 → NO GO with a one-line fix round (not at any cap). Let the gate measure it first. ONBOARDING-CITE (startup-migrations.ts seeds 8 fixed ids; new tenants go through tenant-provisioning/src/index.ts:245/:272) is a cite-accuracy finding, non-blocking in the drafter's view.
3. **#1268 disposition (dead-open, same blob as #1287):** its body says the disposition is Kam's. *Recommend:* ask Kam to close #1268 unmerged once #1287 lands (approval-class: it closes a PR). Until then the merge seat must never merge #1268 (it would land its failed ks781 rule). Same note stands for #1245 and #1241 (both dead-open, disjoint from this kit).
4. **`run-shell-suites.sh --list` in the gate's own worktree** — the standing rule forbids a STANDALONE RUN of run-shell-suites.sh over the real repo; the prompt carves out the read-only `--list` mode in the gate's OWN worktree as the membership instrument for #1285. *Recommend:* accept (it runs no suite and reads only its own clone). Reject → the membership stays READ ONLY.
5. **Mixed tiers in one kit (T2 x3 + T3 #1286).** *Recommend:* accept — four PRs, well under the cap of 8; the T3 rule is an explicit kit rule (exit 43) and the T3 row owes no red proof.
6. **#1278's short subject** («KS-1314: read parser imports from the AST; pin the readYaml call, not its spelling (#1278)», 90 chars) is the drafter's wording. *Recommend:* let the gate ratify or reword; re-run the key scan over whatever is mandated.
7. **#1285 LOCAL-MODEL-PROVENANCE** (the patch was produced by the local model under your brief, re-verified by the seat). *Recommend:* grade on merits, no special handling; the drafter's probe reproduced every figure.
8. **Routing name** `QA/Secuura-batch1278` (you specified it). Distinct and absent (measured). *Recommend:* keep.
9. **READY mails NOT read** (no message id reached the drafter; a listing marks mail seen). The seat claims come from PR bodies, commit messages and handovers (the capture).

## 7. Controls: `controls_gate27.sh <scratchpad> [--invert]`
- **controls_1.out:** 124 controls, **OK 124, MISMATCH 0** (rc 0).
- **controls_2.out (`--invert`):** **OK 0, MISMATCH 124** (rc 1 by design). Every control can fail.
- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed (same length, never a superset); the launcher's head guard is whole-field.
- Doctored arms are pinned to the launcher's own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev `00de57baeb40` in a MOVED copy; RE lists a kit PR in the (empty) sibling set too — a pairwise overlap — and must refuse rc 10. PS2 is `--simulate moved`; PF1 fills from its SIM pins and must refuse.
- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.

## 8. Files
- Kit: kit.json · COMMISSION.md (the LEGITIMATE SHAPES table) · PROPOSED_inbox_routing_line.txt · make_commission_gate27.py / make_readme_gate27.py (generate the two .md files from the kit's own outputs)
- Pins: predict_gate27.py → predict_1.out, predict_sim_*.out, pins_gate27.json (+ .SIM-*.json)
- Reads: gh_read_gate27.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate27.py → linear_reads_1.out, linear_KS-*.md · capture_mail_gate27.py → capture_1.out, mail_gate27_ready.md, stopcounts_gate27.json
- Prompt/launcher: prompt_gate27.TEMPLATE.txt, launcher_gate27.TEMPLATE.sh.txt, fill_gate27.py → 2026-09-26_secuura-batch1278.prompt.txt + launch_qa_secuura_batch1278.sh (fill_1.out), launcher_check_1.out
- Repin/controls: repin_and_launch_gate27.sh (repin_dryrun_1.out), controls_gate27.sh (controls_1/2.out + .rc)
- Drafter probes (PREDICTIONS): drafter_probe1278.sh → probe1278_1.out · drafter_probe1285.sh → probe1285_1.out

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, merge, commit, push, routing write, container or port bind. No inbox read. No write in any project folder or in /Volumes/DevMASTER/WEDNESDAY.
- **UNMEASURED:** every suite count (systemTest/performance unit, packages/shared) and tsc / lint / prettier — the seat's figures are READ only; the A4 / A2c / textreader arms through the REAL sheddingCeiling cells (the drafter probed the functions, not the cells); whether CREATEREQUIRE-ALIAS / IMPORT-EQUALS are REAL (prettier / tsc / tsx); a third loader beyond the hand-written two.
- **UNMEASURED:** #1287 on develop (the file alone, the package, the K1b drift plant); #1286 beyond the two predictions (the full sentence table, the 039 SQL text); `run-shell-suites.sh --list` and the scripts/*.sh guards over #1285; the usage gate and launch steps 4-6.
