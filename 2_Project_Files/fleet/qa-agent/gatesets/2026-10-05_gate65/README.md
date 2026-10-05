# Gateset 2026-10-05_gate65 — README for Wednesday

Drafted 2026-10-05 12:15Z – 12:5xZ (23:15 – 23:5x AEDT) by one Wednesday drafting subagent. Every figure names the kit file it came from. Every builder statement is a CLAIM the gate re-measures; the prompt says so.

## 0. What this gate is, and its status

**gate65 is a T1 gate over ONE Secuura/Blockchain PR: #1393, KS-1278, "revoke decides already-revoked in the UPDATE, not only on the read".** T1 because it is an audit / integrity path: the revoke route decides whether an `action_provenance` row (`email_enc`, `display_name_enc`, `email_hash`) is written and whether a revoke anchor is emitted.
- Six paths, all 100644 (`c1_pr1393_devd784_ex2.out`): the new `ks1278-revoke-is-one-atomic-transition.test.ts` (+157), the `ks1293` register (+1), `repositories/documentRepo.ts` (+9/-1), `routes/documents.ts` (+6/-1), the flow doc (+111) and the cheat sheet (+42).
- Author: Seat B 63rd, wrapping after the READY. Merger: **Seat B 64th** (not yet launched).
- **GO string:** `GO (Seat B 64th): merge 1393 on gate65`. The launcher refuses a prompt that names `GO (Seat B 63rd)` (exit 8).
- **NO GO string:** `NO GO (gate65): 1393 at 4a1620588819 — <N-1393-n: the blocker, one line>`.
- head `4a1620588819a35c180fb1a4a3d98d35f4814f3f`, END_TREE `79b51d3f777f90d8bfb725455e84fc504037d3c9`. Its ONE parent is the base `32e058975d4e`, **not develop**, so every merge of #1393 needs a docs merge-in first.
- **develop MOVED while drafting.** At the READY it was `3cb93b9c731e`. **#1388 (KS-1404) merged at 12:24:04Z as `d784b613c81e2e17d2071ddb18296d7bd27c97ce`**, tree `f65ddbbd560c` (that is the tree of D 9th's merge-in `a1c0927cabf3`). The drafter's ls-remote read it at 12:33:17Z. `32e0..d784` is 35 paths: both platform-k docs, 0 code paths, 0 hook paths. **The kit is keyed to d784** (`kit.json` `develop_at_draft`). The READY's develop is kept as `develop_at_ready`.

**Status: KIT COMPLETE, NOT LAUNCHED.**
- Every checker's self-test fires on its planted defects and passes the clean case (section 3).
- The dry run against live origin returns rc 0 (section 5).
- Wednesday owns the routing line (section 4) and the launch (section 7).

**What the drafter did:**
- **Writes:** only inside this directory, plus `/private/tmp`. That covers `/private/tmp/g65/clone`, a `clone --shared` of the checkout whose origin is set to GitHub and which fetched by SHA, and the session scratchpad `…/scratchpad/g65/{clone,wt}`, a second shared clone plus one detached worktree at the head. In the worktree the drafter ran `npm ci --ignore-scripts` (1937 packages, rc 0) and the `packages/shared` build (`dist/index.js` 17,746 B). SIM commits and predicted trees exist as objects in the scratch clone only. No ref was written anywhere.
- **In `/Volumes/DevMASTER/!CODING/`:** read verbs only (`ls-remote`, `show`, `cat-file`, `rev-parse`, `config --get`, `merge-base`, `diff`, `log`, `ls-tree`), plus the clone source.
- **Network:** GitHub REST GETs (pulls/1393, its files, pulls/1388, the open-PR census, one compare GET in a repin arm), `ls-remote`, and SHA fetches into the /private/tmp clone. No Linear read, no mail, no launch, no routing edit, no `rm`.

## 1. Drafter predictions at 4a1620588819 (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1393_devd784_ex2.out` (rc 0, 12/12, origin read, develop d784) | P1 origin agrees · P2 one parent 32e058975d4e · P3 6 paths exact both ways + 3-dot · P4 END_TREE 79b51d3f777f · P5 trailers 1 byte (control bf277eead268 = 55; the READY's "53 bytes" control is unnamed, D11) · P6 0 Co-Authored-By · P7 75 chars · P8 one `Refs KS-1278`, only key KS-1278, 0 closing · P9 100644 ×6 · P10 hooks unchanged · P11 advance (35 paths) code-disjoint. Real control `c1_basehead_ex1.out`: rc 1, 7 FAIL. Absent object: `c1_refuse_absent_ex1` rc 2 by name |
| C2 product | `c2_pr1393_ex2.out` (rc 0, 6/6) | W1 exactly the 5 added / 1 removed code lines · W2 the guard is inside the `$executeRaw` tagged template, 2 `${guardStatus}` bindings, unquoted, not concatenated · W3 1 of 14 `updateDocument(` callers opts in (count equal at base and head) · W4 the guard 400 is byte-identical to the read-time 400 · W5 the manifest line is sorted · W6 4 cells, none skipped. INFO W4-db: the route reads with `req.db` (:2359), and the guarded write passes `undefined` |
| C3 red-first | `c3_redfirst_ex1.out` (rc 0) | base + both head test files: **R1, R2 red BY ASSERTION, C1, C2 green, 4 executed, ks1293 10/10**; overlay restored by content; head 14/14 |
| C3 tampers | `c3_tamper_ex1.out` (rc 0) | builder table reproduced exactly: T1 → R2, T2 → R2, T3 → C2, T4 → R1; T6 (route ignores null) → R1; **T5 BLIND SPOT: `TRUE OR …` guard no-op → all 4 GREEN** (cells pin SQL text, not semantics); each landed, restored, status clean |
| C3 suite / tsc | `c3_suite_ex1.out`, `c3_tsc_ex1.out` (rc 0) | 90/1063/0 → 91/1067/0, 0 new reds · tsc 5.9.3 rc 0 both ends, planted TS2322 rc 2; tsconfig EXCLUDES `src/__tests__` |
| C3b security | `c3b_pr1393_ex1.out` (rc 0, 3/3) | S1 order 401 :2350 < read :2359 < 404 :2362/:2367 < 403 :2371 < 400 :2375 < OBO :2393 < write :2398 < null :2399 < 400 :2400 < record :2404 < anchor :2410 < json :2417 · S2 two identical 400s, nothing between write and check · S3 both SELECTs + the UPDATE tenant-scoped, `!doc → null` before the UPDATE ⇒ **no cross-tenant path to the new 400** |
| C3b N2 probe | `c3b_probe_n2_ex2.out` (rc 0; template `c3b_probe_n2_gate65.test.ts.txt`) | **a LIVE owned document revoked by its UUID: base 200 + 1 provenance row; HEAD 400 BAD_REQUEST + 0 rows** (control by external_id 200/1 both ends). PROBED with `$executeRaw` planted 0 for the UUID (the UPDATE's WHERE is `external_id = ${id}` only, read at head). v1 of the probe was a LOAD FAILURE (TS6133), quarantined |
| C4 docs | `c4_docs_pr1393_ex1.out` (rc 0, 8/8) | D1 skill · D2 one commit · D3 flow head−block == base, 15. between 14. (KS-1388) and 19. (KS-1005), ascending · D4 cheat head−block == base, KS-1278 LAST after KS-1005 · D5 both blocks carry the figures · D6 no ordering-invariant claim · D7 timing 0/0, auth 76/75, Akto 71/83. INFO D8: neither block names KS 1419; the flow says "a null can only mean the row became revoked" (see D2) |
| C4 predict | `c4_predict_*_ex1.out`, `gitmerge_crosscheck_ex2.out`, `gitmerge_devd784_ex1.out` | develop 32e0 → **79b51d3f777f == END_TREE** · 3cb9 → `d7f7d5eee4cb6beaf7195347f3677fa9c5665607` · **d784 → `6e5de2a1395b86bd1f790ce4e1f32a37eb47ecb0`** (controls: tail `558a76317e29`, succ `f20f2612c8d5` differ) · the CHEAT blob equals `git merge-tree --write-tree`'s auto-merged cheat on both 3cb9 and d784 (`806e4a4d6de1`). **The FLOW conflicts under git** (15. vs develop's 18. at the same place), so the flow is cross-checked only by the ascending invariant. Refusals: absent develop rc 2 "develop unresolvable" (`c4_refusal_unresolvable_ex1`); clone inside `!CODING` rc 2 (`c4_refusal_forbidden_ex1`) |
| C5 / C6 PR text | `c5_pr1393_ex2.out` (**rc 1**, 7/8) | T1-T4, T6, T7, C6 PASS on the live body (8,514 bytes, sha `9088067183c5e57f` == the READY). **T5 FAIL: the residual is not named by its ticket** ("being filed separately"; KS 1419 was filed after the raise). INFO: the body is 8,435 *characters*, not bytes |
| census | `gh_census_ex1.out` (rc 0) | 26 others: 0 OVERLAP, 0 NEAR, 3 DOCS (#1390 KS-1408, #1385 KS-938, #1383 KS-1401); control FIRES. #1388 is merged and no longer open |

## 2. Doubts for the gate (the drafter rules none; the prompt carries D1-D11)

- **D1 Tier.** T1 (audit / integrity). The drafter sees nothing that argues for lower.
- **D2 The UUID-addressed revoke (N2): the most important item.**
  - Mechanism: `getDocument` falls back to `id = ${id}::uuid`, but the guarded UPDATE matches only `external_id = ${id}`.
  - Effect at the head: a live, owned document revoked by its UUID answers **400 "Document is already revoked"** (PROBED).
  - At the base the same request answered 200, recorded a provenance row and anchored, but never wrote the status. That is a pre-existing integrity defect, and it is now surfaced with a false message.
  - The body's and the flow block's sentence "a `null` can only mean the row became revoked in between" is false of the code.
  - It is not a cross-tenant leak (C3b S1/S3).
  - Whether any client revokes by UUID is UNMEASURED.
- **D3 Multi-tenancy (N3).** The route reads with `req.db` (the tenant pool when `MULTI_TENANCY_ENABLED=true`), but the guarded write uses the default prisma. Under that flag every revoke may now answer 400 where it used to answer a silent 200. `index.ts` calls single-tenant "the live config". The drafter did not read any deployed env.
- **D4 KS-1419 unnamed** in the PR body (C5 T5). Is that a blocker, or a squash-body item?
- **D5 T5 blind spot.** The cells pin the SQL text, not its semantics, and R2 does not check which value is bound. The NOT COVERED section already declares serialisation UNMEASURED.
- **D6** The READY's "8,435 bytes" is a character count. The UTF-8 size is 8,514 bytes, and the sha agrees.
- **D7 Cheat-sheet DIVERGENCE.** #1385, #1383 and #1390 are open and touch both docs. If one of them lands a cheat section after KS-1005 first, the key tree puts KS-1278 ABOVE it (OURS above THEIRS, the #1387 ruling), while the builder's "LAST" would put it below. `predict` prints `DIVERGENCE`. **Wednesday rules.**
- **D8** PREFLIGHT-INCOMPLETE 12/15 (legs 3, 4, 8) on a T1 change.
- **D9** The flow merge-in CONFLICTS under git. Seat B 64th must reproduce the predicted tree by hand. Only M1 (the tree) proves it.
- **D10** The body says "completes the ticket's scope" beside `Refs`. Is the wording true, given D2?
- **D11** The READY's trailer control printed "53 bytes", but it does not name its commit. The kit's control is `bf277eead268` = 55.

## 3. Kit files

| file | role | self-test (planted defects fire, clean passes) | live run |
|---|---|---|---|
| `kit.json` | every pin, blob, tamper, claim and prediction | — | — |
| `lib_gate65.py` | read-verb `git`; write verbs only outside `!CODING`; GH GET by token name | — | — |
| `c1_pin_gate65.py` | C1 P1-P11 | `c1_selftest_ex2.out` rc 0, **25/25** | `c1_pr1393_devd784_ex2` rc 0; control `c1_basehead_ex1` rc 1; `c1_refuse_absent_ex1` rc 2 |
| `c2_product_gate65.py` | C2 W1-W6 (hunks, parameterisation, opt-in) | `c2_selftest_ex2.out` rc 0, **13/13** | `c2_pr1393_ex2` rc 0 |
| `c3_tests_gate65.py` | C3 redfirst / tamper / suite / tsc (jest JSON judges) | `c3_selftest_ex1.out` rc 0, **22/22** (16 judge arms + 6 tamper-landing arms on the real head) · refusal `c3_refusal_forbidden_ex1.rc` = 2 | redfirst / tamper / suite / tsc ex1, all rc 0 |
| `c3b_security_gate65.py` | C3b S1-S3 + N1-N3 | `c3b_selftest_ex2.out` rc 0, **10/10** (includes one must-NOT-fire arm) | `c3b_pr1393_ex1` rc 0 |
| `c3b_probe_n2_gate65.test.ts.txt` | the N2 jest probe (copy into the gate's worktree, run, quarantine) | v1 LOAD FAILURE quarantined | `c3b_probe_n2_ex2` |
| `c4_docs_gate65.py` | docs D1-D8; KEY-ANCHORED predict; qm M1-M7 | `c4_selftest_ex4.out` rc 0, **31/31** (11 docs arms + predict(base)==END_TREE + real-develop controls + merge-tree cheat cross-check + ascending + SIM post-#1388 == real d784 + SIM append-after-KS-1005 DIVERGENCE + 4 predict refusals incl. **develop unresolvable BY NAME** + Q-M positive + 7 Q-M arms + qm absent-M refusal) | docs ex1 rc 0; predicts above |
| `c5_prtext_gate65.py` | C5 T1-T7 + C6 | `c5_selftest_ex2.out` rc 0, **17/17** | `c5_pr1393_ex2` rc 1 (T5, a predicted finding) |
| `gh_census_gate65.py` | collision census | `gh_selftest_ex1.out` rc 0, **12/12** | `gh_census_ex1` rc 0 |
| `launch_qa_secuura_ks1278_1393.sh` | the launcher (static prompt) | `launcher_arms_ex1.out` **10/10** + `launcher_arm_noreadme_ex1` (8) | `--check` rc 0 |
| `repin_and_launch_gate65.sh` | the launch action | `repin_arms_ex1.out` **7/7** | `dry_console_ex2.out` rc 0 |
| `prompt_gate65.txt` | the gate's prompt | — | — |
| `api/` | the PR body + meta as read 12:2xZ, census JSON | — | — |

Kept in history, never deleted (`_quarantine/`):
- c2 ex1: a docstring escape warning, plus a db-line scan that covered the whole file.
- c3b ex1: an arm anchor that was not unique across handlers.
- c4 ex1-ex3: the DIVERGENCE note firing on the flow too, and the SIM post-#1388 arm built on a develop that already had it.
- c5 ex1: the T7 regex was blind to a line break.
- the first merge-tree cross-check: a zsh `:P` modifier instrument error.
- the N2 probe v1: a LOAD FAILURE.
- the pre-README dry run.
- `pre-develop-d784/`: runs keyed to 3cb9.

`_arms_artifacts/` holds the arms' stand-ins. `routing_standin.conf.ARM-ONLY-…` is NOT the routing file.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1278-1393|coagent@agentmail.to|yes
```
Until it is present, step 0 of the real launch refuses rc 1 (`repin_arms_ex1`: proved). The dry run reports it instead.

## 5. Dry run (against live origin)
`dry_console_ex2.out`, rc in `dry_console_ex2.rc`. The run must show:
- the routing line reported missing (0 of 154 agentmail lines)
- census rc 0: 26 others, 0 OVERLAP, 3 DOCS; control FIRES
- API, pull/head and branch agree with the head
- develop UNMOVED at d784; predicted tree `6e5de2a1395b`
- C1 at the head rc 0. In the repin, c1 runs against the base, because d784 is not in the shared checkout's store. The output names this.
- launcher `--check` rc 0
- `DRY RUN COMPLETE`

The full figures are in the file.

## 6. The merge-in: KEY-ANCHORED, never div-anchored
- The merge ALWAYS needs Seat B 64th to merge develop IN first: a merge commit M, never a rebase, never a force push. The head's parent is `32e058975d4e`.
- **Target tree** = develop's tree, with the 4 code paths at the head's blobs. Each doc is develop's doc with the head's KS-1278 block inserted immediately after the section of the **key that precedes it at the head**: flow `(KS-1388)` = 14., cheat `&mdash; KS-1005`. Sections are found by their h2 KS key, never by `<div class="section">` or tail position. On the flow, the result must also satisfy the readable ascending invariant, or predict refuses.
- **Predictions:**
  - develop 3cb9 → `d7f7d5eee4cb…`
  - **develop d784 (current) → `6e5de2a1395b86bd1f790ce4e1f32a37eb47ecb0`**
- **For any later develop D:**
  - fetch D by SHA into your OWN clone
  - run `G65_SCRATCH=<scratch> python3 …/c4_docs_gate65.py predict --repo <own clone> --develop-after <D>`
  - it refuses `develop unresolvable` BY NAME, rc 2, if D is not there
- The GO covers M only if `c4_docs_gate65.py qm --repo <clone> --merge-in-head M --develop-after D` passes M1-M7. Anything else re-gates.
- `repin_and_launch_gate65.sh` refuses rc 10 on a moved develop unless `--repin-develop <that sha>` is given. It is a hard rc 10, not re-pinnable, if:
  - the advance touches a code or hook path, or
  - develop does not descend from d784.

## 7. How Wednesday launches it (after section 4's routing line)

Pane `QA/Secuura-ks1278-1393`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1278-1393-g65/`. Verdict subject `[QA -> Wednesday] GATE65 #1393 (T1 KS-1278: revoke decides already-revoked in the UPDATE; author Seat B 63rd wrapping, merger Seat B 64th)`.

**Dry run** (no usage gate, no cockpit):
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate65/repin_and_launch_gate65.sh 1393 4a1620588819a35c180fb1a4a3d98d35f4814f3f --dry-run
```
**THE launch command:**
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate65/repin_and_launch_gate65.sh 1393 4a1620588819a35c180fb1a4a3d98d35f4814f3f
```
If develop has moved past d784, both commands refuse rc 10 and print `re-run with: --repin-develop <new sha>`. Read the printed advance, then append `--repin-develop <that sha>`.

Exit codes:
- 1 routing
- 9 input
- 2 ls-remote
- 3 API, or a blind census control
- 15 OVERLAP
- 11 head moved (RE-DRAFT)
- 10 develop moved (re-pin), or not re-pinnable
- 13 C1, or the launcher's `--check`
- 16 override
- 12 usage gate
- 14 cockpit

Add `WED_USAGE_STOP=…` only with Kam's recorded authority.

**Rung 5 (verify at rung 5 or 6, never below).** Read the pane and find content only THIS gate would produce:
- KS-1278 / #1393
- `…/2026-10-05_gate65/README.md` or `QA_AGENT_CHARTER.md` read
- head `4a1620588819`
- a `*_gate65.py --selftest`

Rung 6 is `NOT-TESTED.written-first.md` in the report dir.

## 8. Re-draft recipe (the head moved, or develop is not re-pinnable)
1. Re-measure `kit.json`: `head`, `end_tree`, `files`, `head_blobs`, `parent`, the tamper `from` strings, `claims`, `merge_in_predicted`.
2. Edit the head in `prompt_gate65.txt` and `launch_qa_secuura_ks1278_1393.sh`. Both are static.
3. Re-run every `--selftest`, then c1, c2, c3b, c4 docs + predict, c5, the census, and a `--dry-run`.
4. A merge-in head on top of 4a1620588819 is NOT a re-draft. It is judged by `c4 qm`.

## 9. NOT COVERED by this kit (the gate's, or nobody's)
- The C3 / C3b runs above are the DRAFTER's (this host, node from PATH, jest via npx, tsc 5.9.3). The gate re-runs them; none is evidence.
- **No live sweep, no real PostgreSQL:** two concurrent transactions on the guarded WHERE (the atomicity itself) are UNMEASURED by the builder and by this kit. The N2 probe plants the 0-row result that a real WHERE would give. It is PROBED, not measured on a database.
- No read of any deployed env for `MULTI_TENANCY_ENABLED` (D3). No measure of whether any client revokes by UUID (D2).
- No Linear read (KS-1278, KS-1419). The READY's claim that KS-1419 was filed is unverified here.
- No preflight run. Legs 3 / 4 / 8 need a stack.
- No predict / qm on a REAL merge-in M: none exists yet. Q-M is proven on SIM merge-ins only.
- No independent second implementation of the predictor. Its cheat output agrees with `git merge-tree` on 3cb9 and d784. Its flow output has no git cross-check (git conflicts there); the only check is the ascending invariant plus the SIM arms.
- The repin script's rc 2 / 3 / 13 / 14 / 12 / 15 paths were not driven. The real-launch rc 16 path was driven through a routing stand-in.
- The four platform suites (Schemathesis, Akto, Playwright, k6) — no scan surface.
