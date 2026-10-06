# Gateset 2026-10-06_gate69 — README for Wednesday

**gate69** is a BATCHED tier-1 gate (Kam 2026-09-18: minimise gate duplication; batch disjoint changes into one session). It covers two Secuura/Blockchain PRs:

- **PR A, #1395 (KS-1305, author Seat R 1st):** a diagnostic in originate `src/db.ts`, the tenant-isolation module.
- **PR B, #1396 (KS-1256, author Seat E 7th):** api-gateway fails closed with 503 when the connector allow-list cannot be read.

The two are disjoint in code: originate versus api-gateway, 0 shared paths. They share only the two platform docs.

The kit was drafted by one Wednesday drafting subagent, 2026-10-06 ~00:15Z–00:45Z (host clock UTC). Every author figure in this README is a **claim**. Every drafter figure names its instrument, and the drafter's results are **predictions**, not evidence.

## 0. Bottom line

**Status.**
- The kit is complete.
- Every self-test is green, and each one has planted arms that FAIL.
- The dry run was executed with PR B included (§5).
- The gate has **not** been launched.
- The routing line has **not** been added.

**PR B is a parameter.** If you run without `--b-pr/--b-head`, the kit renders an **A-only** gate:
- `[[B]]` blocks are cut from the prompt.
- The launcher requires "NOT IN THIS GATE".
- c4 runs with `--a-only`.

With `--b-pr 1396 --b-head e6eb53fe2658…` it renders the batch. #1396's READY landed during drafting, so the batch is the intended launch.

**The heads are parameters.** At launch the repin script re-reads, for each PR:
- the READY (it must name the head in full);
- the GitHub API;
- `refs/pull/<n>/head`;
- the branch.

It refuses unless all of them agree. A head other than the kit's expected one refuses unless `--accept-unexpected-head` is passed.

**Develop moved DURING drafting.** At 00:16Z and 00:26Z it was `3f9ff4e1e1b9`. By 00:35:15Z it was **`4eaf7741a6a4`**, after #1394 (KS-723) merged:
- one parent 3f9f;
- tree `6884601a03dc`, which equals gate67's own predicted tree;
- 0 batch paths touched, 0 hook paths touched.

The kit is keyed to 4eaf. The 3f9f-era figures are kept as superseded (`*_dev3f9f_*`). The launch reads develop again, recomputes every merge-in prediction (step 3c), and refuses a further move unless `--repin-develop` is passed.

**Pins** (drafter ls-remote from the shared checkout, 00:16:22Z / 00:26:32Z / 00:35:15Z / 00:41:20Z):

| | PR A #1395 | PR B #1396 |
|---|---|---|
| head | `1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660` | `e6eb53fe26587bc8375154a6acfd112ddea58278` |
| branch | `feature/ks-1305-prisma-not-generated-diagnosis-ra1-1` | `feature/ks-1256-thrown-settings-read-refuses-connector-create-e6-1` |
| END_TREE | `924908aeefe1` | `e034a458fa52` |
| chain | ONE parent 3f9f | e16c3133c296 (code, on 22b2) → c6564b8ff04f (merge of 3f9f, tree 9c6cf0171127, a CLEAN merge: `git merge-tree` of its parents reproduces it) → e6eb (docs + ks1195 title) |
| merge-base | 3f9ff4e1e1b9 | 3f9ff4e1e1b9 |
| files | 4: db.ts 19/0, ks1305 test 119/0, flow 90/0, cheat 41/0 | 11: verification.ts 22/1, ks1256 test 251/0, 6 doubles 33/0 total, ks1195 13/3, flow 92/0, cheat 41/0 |
| API (00:3xZ) | open, `dirty`, body e3e2ba5f26d1e033 (8,891 B = 8,839 chars) | open, `dirty`, body 4a3dc5d9ba5de7d9 (7,928 B = 7,876 chars) |
| GO (pre-ruled) | `GO (Seat R 2nd): merge 1395 on gate69` | `GO (Seat E 8th): merge 1396 on gate69` |

**Tier: T1 for both.**
- **#1395** is T1 because of *where* it lives: the change is a pure insertion, but db.ts is the tenant-isolation module.
- **#1396** is T1 because it is connector authorization: a fail-open path becomes fail-closed.

## 1. Drafter predictions

| Check | File | Result |
|---|---|---|
| C1 A | `c1_A_dev4eaf_ex1.out` | rc 0, 11/11 with P1 live (the dry run's `--no-remote` read is 10/10) |
| C1 B | `c1_B_dev4eaf_ex1.out` | rc 1: **P8 FAIL** (D-B1 below); the other 11 of 12 pass. P2 proves the clean merge, P3b proves the doubles 33/0 |
| C2 A (the T1 proof) | `c2_A_head1bdf_ex2.out` | 6/6. One hunk; head minus the 19 lines == develop; inside getPrismaClient. 0 added lines match the tenant/GUC/RLS regex, beside a must-hit control of 96 develop lines. All 96 tenant lines are unchanged (multiset). Guard = exactly 2 conjuncts + `throw err;`. ks458 is byte-identical |
| C2 B | `c2_B_heade6eb_ex2.out` | 8/8. The availability test (:1230) is before the read (:1235). The bare catch is gone. The second reader is untouched (develop :1283 = head :1304). Doubles +33/-0 with 0 `expect(`. ks1195 has 2 assertion pairs + title + header. isRedisAvailable has exactly ONE consumer outside redis.ts |
| C3 | — | **NOT RUN by the drafter** (no npm). Self-test 34/34. Every tamper lands exactly once on the real head blobs |
| C4 containment / h2 | `c4_containment_{A,B}_ex1`, `c4_h2proof_{A,B}_dev4eaf_ex1` | 6/6 each; 4/4 each |
| C4 merge-in | `MERGE_IN_PREDICTION.txt`, `c4_chain_dev4eaf_ex1.out` | On 4eaf: A alone **37773febc715**; B alone **b0214dad053d**; B-then-A **883d4b70343c**; A-then-B **622d7b8b4a60** (flow …22 21). git: **DIVERGENCE** (the cheat conflicts; the flow auto-merges equal to TAIL) |
| gh | `gh_api_*`, `gh_prtext_*`, `gh_actions_*`, `gh_census_ex1` | Both prtext pass (T1–T5). actions: `Security Scanning` FAILED at both heads with no develop baseline; KS-168 / `pr` fail on develop too. Census: 23 others, 0 OVERLAP, 2 DOCS (#1393, #1383) |

## 2. Defects in the authors' claims

### PR A (#1395, Seat R 1st)

- **D-A1 "three-term conjunction"** (the commit message, and the READY's "one red arm per conjunct" framing). The guard has **two** conjuncts, `code === 'MODULE_NOT_FOUND'` and `.includes('.prisma/client')`, plus the same-object rethrow. Arm B tampers the rethrow, not a conjunct. Measured by c2 WA4. The three arms are still the right three; the wording is wrong.
- **D-A2 the cells are order-dependent by READ.**
  - The shared module-level `prismaClient` is set only by C2's success path, and C2 runs last.
  - With any order that puts C2 first, D1, C1 and C3 never reach the probe.
  - Predicted red under `jest --randomize`; the gate measures it (c3 `order`).
  - Not claimed by the author either way.
- **D-A3 no cell asserts `{ cause: err }`.** ArmE is predicted BLIND. This is a named assertion-strength gap.
- **D-A4 the READY's "the same-line reader sees fewer".** True: old reader 13 vs tolerant 18 at the head. Its planted control is reproduced by c4 h2proof.

These A claims hold by the drafter's instruments:
- numstat 19 0;
- body sha256/16 e3e2ba5f26d1e033;
- subject 77 chars;
- trailers 1 raw / control 55 raw, 53 content;
- only KS-1305 hyphenated in the message, title and body;
- tolerant reader "1-14, 18, 19, 20, 22";
- 4 files.

Red-first, the arms, the suite and tsc are **unverified** here, because C3 was not run.

### PR B (#1396, Seat E 7th)

- **D-B1 FALSE: "Only KS-1256 is hyphenated in the title, body and both commit messages."**
  - e16c3133c296's message carries **KS-1231** and **KS-1233**.
  - e6eb53fe2658's message carries **KS-938**.
  - Measured by c1 P8.
  - The title and body are clean (gh prtext T3).
  - Risk: a squash body that keeps the commit messages would attach #1396 to three foreign tickets. See RULINGS Q3.
- **D-B2 contradiction in the red-first claim: "4 of 6 RED at base", yet "the two CONTROL cells are green at base BY DESIGN".**
  - CREAD ends `expect(availableSpy.mock.calls.length).toBeGreaterThan(0)`, which cannot hold where develop never calls isRedisAvailable. The drafter therefore predicts **RI RII RIIP CREAD** red.
  - That makes 4 of 6, but one of the 4 is a CONTROL.
  - The figure is Seat E 6th's, cited and not re-run by E 7th. The gate's run will be the first independent one.
- **D-B3 "Body 7,876 bytes".** 7,876 is the CHARACTER count. The body is 7,928 UTF-8 bytes, and the sha256/16 4a3dc5d9ba5de7d9 matches. This is the bytes-vs-characters class again.
- **D-B4 stale line number in COMMITTED text.**
  - The ks1256 test comment, the READY and the commit body cite "verification.ts:1283" for the second reader.
  - That is the DEVELOP line; at the head it is **:1304**.
  - Polish.
- **D-B5 Wednesday's relay versus the commit.** The relay said "7 api-gateway test files' doubles (33 insertions)". It is **6** doubles files totalling 33/0, plus ks1195 (13/3 at the head: the 2 assertion pairs, the title and a 10-line header comment).
- **D-B6 two different timing figures.** The e6eb commit message says 7.59 s / 51.16 s. The READY says 7.42 s / 52.88 s. Both are claimed as 92 / 818 on the same host and date. These are two runs; neither is wrong, but the doc carries one.
- **D-B7 the PR title is the DOCS commit's subject.** It does not describe the product change (RULINGS Q6).

These B claims hold by the drafter's instruments:
- the merge tree 9c6cf0171127, clean;
- trailers 1 raw;
- subject 81 → 89 squashed;
- "THESE TWO ARE THE ONLY ASSERTION CHANGES" (c2 WB6: exactly 2 pairs);
- doubles have 0 added `expect(`;
- the second reader is untouched;
- the availability test is before the read;
- body sha256/16.

## 3. Kit files

| File | What | Self-test (drafter) |
|---|---|---|
| `kit.json` | pins, both PR specs (A always; B a parameter), tampers, claims, predictions; `script_sha256` | — |
| `composee5_copy.py` | Seat E 5th's newline-tolerant readers, verbatim. sha256 `f9ab42d9…` equals the origin (`shasum` at drafting). Never executed | — |
| `lib_gate69.py` | read-verb git; write verbs outside `!CODING` only; GitHub GETs with the token read by name; `spec(A\|B)` | — |
| `c1_pin_gate69.py` | P1–P11 + P3b per PR | `c1_selftest_ex2` 9/9: planted A-at-B's-head, B-at-A's-head, B-at-its-merge, a numstat pin and a develop touching a code path all FAIL; B's real P8 FIRES |
| `c2_product_gate69.py` | WA1–WA6 (the T1 tenant proof), WB1–WB8 | `c2_selftest_ex2` 14/14: planted GUC edit, tenant line, third conjunct, new-Error rethrow, deleted line, ks458 edit, check-after-read, bare catch, hunk outside branch, added expect, third ks1195 assertion, second consumer — each FAILS |
| `c3_tests_gate69.py` | redfirst / tamper / suite / tsc / **realshape** (A) / **order** (A) / **dbretry** (B); 0 executed = LOAD FAILURE | `c3_selftest_ex2` 34/34 |
| `c4_docs_gate69.py` | containment, h2proof, predict, **chain** (both orders), mergetree (`--over-sim-of`), qm M1–M8, sim1394 | `c4_selftest_dev4eaf_ex1` 29/29: the positive controls reproduce BOTH heads' trees on 3f9f; the wrong-order, take-OURS, trailer, 1-parent, absent-develop and code-path SIMs FAIL. Planted `c4_selftest_planted_BheadAsA_ex1` rc 1 |
| `gh_gate69.py` | api / actions / census / prtext | `gh_selftest_ex1` 6/6 |
| `prompt_gate69.txt` | template: `{{HEAD_A}}` ×8, `{{HEAD_B}}` ×8, `{{PR_B}}` ×21, `{{DEVELOP}}` ×4, `[[B]]`/`[[NOB]]` blocks | — |
| `launch_qa_secuura_gate69_batch.sh` | per-kit launcher with `--check` | the arms in §5 |
| `repin_and_launch_gate69.sh` | the launch action with `--dry-run` | §5 |
| `RULINGS_wednesday.md`, `ROUTING_LINE.txt`, `MERGE_IN_PREDICTION.txt`, `api/` | pre-rulings + open questions, routing line, prediction, #1395 body snapshot | — |

`_quarantine/` holds superseded runs; nothing was deleted. `_scratch/clone` is created by the dry run and holds objects only.

## 4. What is NOT tested by this kit

- **C3 entirely.** Red-first, the tamper matrices, the suites, tsc, realshape, order and dbretry were not run (no npm install).
- **Linear.** KS-1305 and KS-1256 were not read.
- **Live sweep, preflight legs 3/4/8 and the four platform suites.**
  - For A: PostgreSQL, RLS and multi-tenant mode.
  - For B: a real Redis outage, and the fallbackMode race between the availability test and the read (READ-only doubt in the prompt).
- **`Security Scanning` job logs** were not read (X6 is the gate's).
- **No qm run on a real merge-in M**, because none exists yet.
- **The real-launch path of the repin script** (usage gate, cockpit) was not run.

## 5. Dry run and launcher arms

**Batch dry run** (`dry_B_console.txt` rc 0, plus the `dry_004920.*` files). It re-read develop as 4eaf and recomputed:
- c1 A: 10/10 with `--no-remote`.
- c1 B: P8 only, reported and not refused.
- The chain trees from §1.
- DIVERGENCE for both PRs.
- The launcher's `--check`: rc 0.

**A-only dry run** (`dry_Aonly/`, rc 0):
- The census runs with `--a-only`, so #1396 is just another DOCS PR.
- The rendered prompt says "NOT IN THIS GATE" and names #1396 0 times.

**Final state.** The rendered prompt and `head_at_launch.txt` on disk are the **batch** render. The real launch re-renders them anyway.

**Launcher `--check` arms.** All 8 fire as intended; see `LAUNCHER_ARMS.txt`.

Dry-run command (batch):
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate69/repin_and_launch_gate69.sh 1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660 --b-pr 1396 --b-head e6eb53fe26587bc8375154a6acfd112ddea58278 --dry-run
```

THE launch command (**NOT run**) is the same command without `--dry-run`, run under `script -q /dev/null` in a real terminal. If develop has moved past 4eaf, also pass `--repin-develop <sha>`.

## 6. Routing line (NOT added)

Back up `inbox_routing.conf`, then add the line from `ROUTING_LINE.txt`:
```
QA/Secuura-gate69-batch|coagent@agentmail.to|yes
```

## 7. Pane, report and rung 5

- **Pane:** `QA/Secuura-gate69-batch`.
- **Report directory:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-gate69-batch/`.
- **Rung 5, in the pane:**
  - #1395 and #1396 named;
  - the gate69 README or the charter being read;
  - both heads (`1bdfbe0f2f06`, `e6eb53fe2658`);
  - a `*_gate69.py --selftest` run;
  - `realshape` run BEFORE any prisma generate.
- **Rung 6:** `NOT-TESTED.written-first.md`.
