# Gateset 2026-10-06_gate67 — README for Wednesday

Drafted 2026-10-06 (UTC 2026-10-05 ~13:42Z onward) by one Wednesday drafting subagent. Every figure names the kit file it came from. Every builder statement is a CLAIM the gate re-measures; the prompt says so.

## 0. What this gate is, and its status

**gate67 is a T1 gate over ONE Secuura/Blockchain PR: #1394, KS-723 (slice 3), "declare GET /api/anchors/tx/{txHash} in the published OpenAPI contract".**

- **Tier T1, not T2:** the api-gateway builds its edge METHOD gate (405) and AUTH gate (401) from this spec (`services/api-gateway/src/specRouteMap.ts`, `index.ts` "SPEC-AWARE METHOD + AUTH ALLOW-LIST"). A declared operation therefore changes what the edge refuses on an authenticated read of the chain-integrity service (D1).
- Head `a94ec8f6a2c6ec382fb7b5dbafcf8a7f9ce68427`, END_TREE `644f23f36231`. It has ONE parent, `d784b613c81e`, **not develop** (`c1_pr1394_devf017_ex1.out`, rc 0, 11/11).
- 5 paths, +354/-0, all 100644:
  - `anchoring.openapi.ts` +43
  - the new `ks723-anchors-tx-lookup-is-declared.test.ts` +50
  - `docs/openapi/secuura-api.yaml` +86
  - flow doc +126
  - cheat sheet +49
- Author: **Seat B 64th**, wrapping cold. Merger: **a later B seat**, named at launch.
- **GO string (template):** `GO (Seat B <NN>): merge 1394 on gate67`. `repin_and_launch_gate67.sh --merge-seat <NNth>` fills `<NN>`. The template carries `{{MERGE_SEAT}}`, and the launcher refuses an unfilled token (exit 8).
- **Forbidden prefixes:** `GO (Seat B 64th)` and `GO (Seat B 63rd)`. The repin script refuses those seats (rc 9), and the launcher refuses a prompt that carries either (exit 8). Proof: `launcher_check_seat64_ex3`, `launcher_check_seat63_ex3`.
- **NO GO string:** `NO GO (gate67): 1394 at a94ec8f6a2c6 — <N-1394-n: the blocker, one line>`.
- **DEVELOP MOVED DURING DRAFTING.**
  - **At the READY / brief:** `f0179806494e42df254b9580168be3cd4a35f307` (Peter's #1391: history.md only, on top of #1390 `c5101866ef54`). Re-read by ls-remote at 13:42:45Z (host clock): unmoved then. `d784..f017` is 38 paths: both docs, history.md and 35 systemTest paths.
  - **Now:** `22b268143a6377c9a82cd03379daa596cd26d644`, "KS-1330: re-land round-2 signal handling". Read at 14:02:58Z and again at 22:11:39Z (host clock; the clock jumped between readings, so treat the times as host-reported). It has one parent, f0179806.
    - `f017..22b2` is exactly `Blockchain/Dev/scripts/run-shell-suites.sh` + `scripts/__tests__/run_shell_suites.test.sh`: 0 kit paths, 0 hook paths, both docs byte-identical.
    - `d784..22b2` is 40 paths. P11 is clean.
  - **22b2 is NOT in the shared checkout's store.** The drafter fetched it BY SHA into `_scratch/clone`.
  - **The kit is keyed to 22b2** (`kit.json` `develop_at_draft`). Every f017 figure is kept beside it.

**Status: KIT COMPLETE, NOT LAUNCHED, NOT DRY-RUN.**
- The repin script was not run, not even with `--dry-run`. The brief said do not run the launch command, and the dry run shares that script.
- The launcher's `--check` WAS run against a rendered prompt in the drafter's scratchpad (section 5).

**What the drafter did:**
- **Writes:** only inside this directory and `…/scratchpad/gate67drafter/`.
  - `_scratch/clone` is a `clone --shared --no-checkout` of the checkout. All three needed commits were already present via alternates, so no fetch was needed.
  - SIM commits and predicted trees exist as objects only. No ref was written.
- **In `!CODING`:** read verbs only (`ls-remote`, `config --get`, `show`, `cat-file`, `rev-parse`, `log`, `diff`, `grep`), plus the clone source. composee5.py was copied by `cat` READ.
- **Not done by the drafter:** no worktree, no npm, no vitest, no tsc, no generate-openapi. **C3 was NOT run by the drafter.**
- **Network:** GitHub REST GETs (pulls/1394, files, actions runs, the open-PR census) and one `ls-remote`. No Linear read, no mail, no launch, no routing edit, no `rm`.

## 1. Drafter predictions at a94ec8f6a2c6 (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1394_dev22b2_ex1.out` (rc 0, 11/11, own clone, develop 22b2) and `c1_pr1394_devf017_ex1.out` (rc 0, 11/11, shared checkout) | P1 origin pull/head == branch == head · P2 one parent d784 == merge-base · P3 5 paths, two-dot == three-dot · P4 END_TREE (base tree differs) · P5 trailers 1 byte (control bf277eead268 = 55) · P6 0 Co-Authored-By · P7 subject == title, 78 · P8 one `Refs KS-723`, only KS-723, 0 closing · P9 100644 · P10 hooks + skill identical at head/d784/develop · P11 advance 40 paths (22b2) / 38 (f017), kit-disjoint. Self-test `c1_selftest_ex2.out` 3/3: the base as head FAILS P2 P3 P4 P7; absent head refused BY NAME |
| C2 product | `c2_pr1394_ex1.out` (rc 0, 7/7) | W1 shape (+354/-0, registerPath +1, 0 registry lines removed, 3 RED + 2 control cells) · **W2 SECURITY:** declared `[{bearerAuth: []}]`; service `app.use('/api', jwtAuthenticate())` index.ts:457 precedes the route at :1089; gateway `router.use('/api/anchors', authenticateToken(true), …)` → declared == enforced at both hops · **W3 ENVELOPE:** handler `res.json({ success: true, data: formatAnchorResponse(anchor) })` == declared {success, data → Anchor}; 404 `{success:false, error:{code,message}}` → ErrorResponse; all 10 Anchor.required keys emitted · W4 SPEC: 309 → 310 paths, exactly the one new path, 0 other paths changed, components identical; **wc -c 1,351,218 → 1,354,452 bytes**; chars 1,346,487 → **1,349,709 (= the generator's "1349709 bytes")**; 2,375 non-ASCII chars; `/api/anchors/tx/` 0 → 1 · W6a `/api/anchors/{id}` NOT declared · W7 tsconfig excludes `src/__tests__` (NOT TESTED) |
| C2 INFO | same | W2-key: the gateway AUTH gate admits `x-api-key: sk_…`; the op declares bearerAuth only (as do its siblings) (D8) · W3-extra: formatAnchorResponse emits **merkleProof, merkleRoot, slot**, which are not in Anchor (D6) · W3-codes: the handler emits only 200 / 404, and a DB failure is swallowed into a 404 (D7) |
| C3b attacker | `c2_pr1394_ex1.out` W5 / W6b; port self-test `c2_selftest_ex1.out` 6/6 | Python port of buildSpecMethodMap / resolveSpecRoute; base spec vs head spec over 11 anchoring routes × 5 methods × bearer/no-bearer → **20 edge decisions CHANGED, 0 LOOSENED**, all on `/api/anchors/tx/*`: GET without credentials `pass → 401` at the edge (it was 401 one hop later at the proxy), POST/PUT/PATCH/DELETE `pass → 405`. **Nothing the route did not already serve is exposed.** Pre-existing: `dbGetAnchorByTx` has no tenant filter. **W6b what-if:** declaring `GET /api/anchors/{id}` would 405 **POST /api/anchors/batch and POST /api/anchors/verify**, which re-derives the PR's stated reason. The self-test plants two loosening spec edits and W5 catches both |
| C3 | `c3_selftest_ex1.out` (6/6), `c3_refusal_forbidden_ex1` (rc 2) | **NOT RUN by the drafter.** The judge's arms: assertion red; load failure ≠ red; skip ≠ pass; red without an AssertionError ≠ red; missing cell. The shared checkout is refused as a worktree |
| C4 h2 proof | `c4_h2proof_dev22b2_ex1.out`, `c4_h2proof_devf017_ex1.out` (rc 0, 4/4 each; identical counts) | **flow d784:** 16 `<h2`, 0 split, tolerant 16, old same-line 16 · **flow f0179806:** 16 `<h2`, **5 SPLIT**, tolerant 16, **old same-line 11** · **cheat:** 6 / 6, 0 split, at both. A planted `<h2>\n      99. … &mdash; KS-99999\n    </h2>` is a tolerant HIT and an old-regex MISS on both docs; the one-line plant control is hit by BOTH |
| C4 predict | `c4_predict_dev22b2_{key,wrong}_ex1.out` (live develop), `c4_predict_devf017_{key,wrong}_ex1.out`, `c4_predict_devd784_key_ex1.out` | **KEY-ANCHORED on 22b2 (live) → `e23888941fda2755a234590addfbeaaadf78bdcd`; wrong-order control `6d498828dc57`**; on f0179806 → `df1f8b7c61ad076c397de298c90b886ec8b2f554` (same two doc blobs, flow `397b77d94383`, cheat `2f03c4f2e340`): flow `1..14 16 18 19` (17 h2), cheat `KS-1404 KS-1333 KS-1345 KS-1388 KS-1210 KS-1005 KS-723` (7 h2), 0 markers, div +0 · **WRONG-ORDER control → `eb39b4f8c65f…`** (flow `…14 18 16 19`, cheat `…KS-1210 KS-723 KS-1005`), READ-BACK FAIL on both docs · **positive control: d784 → `644f23f36231` == END_TREE** |
| C4 merge-tree | `c4_mergetree_dev22b2_ex1.out`, `c4_mergetree_devf017_ex2.out` (rc 1) | `git merge-tree --write-tree` **rc 1, tree-with-markers `dd8ec72867a2` (22b2) / `1680a8a97dae` (f017), BOTH docs CONFLICT** → **DIVERGENCE** (section 6) |
| C4 batch SIM | `c4_predict_simpost1385_key_ex1.out`, `c4_mergetree_simpost1385_ex1.out` | SIM develop `d3dac1d1e737` = f0179806 + #1385 landed as gate66's key tree `fb6cb2c6992c` (computed with gate66's own c4 predict in this kit's clone) → gate67 KEY-ANCHORED **`7687fa98c69e`**: flow `1..14 16 18 19 20`, cheat `…KS-1005 KS-938 KS-723`; merge-tree conflicts on both docs again, DIVERGENCE |
| Q-M | `c4_selftest_dev22b2_ex1.out` (**16/16**, on 22b2), `c4_selftest_ex1.out` (16/16, on f017), `c4_qm_{goodsim,wrongsim,trailersim}_dev22b2_ex1.out`, `c4_qm_absentdev_sharedcheckout_dev22b2_ex1.out`, `c4_qm_*_ex2.out` (f017) | **GENUINE ABSENCE: qm on the SHARED CHECKOUT with develop 22b2 (really absent there) → `QM REFUSED: develop unresolvable: '22b26814…'`, rc 2, CHECKED 0.** This is exactly gate63/64's scenario, and it produces no false M6 · on 22b2 GOOD SIM `b9d7938d1841` 8/8, WRONG-ORDER FAIL [M1 M8], TRAILER FAIL [M4] · on f017 GOOD SIM `204f9ae6d29d` 8/8 (also by 12-hex abbreviations) · WRONG-ORDER SIM fails M1 + M8 · TAKE-OURS SIM fails M1 + M8 · TRAILER SIM fails exactly [M4] · single-parent fails M2 · **absent develop → `QM REFUSED: develop unresolvable: …` rc 2, CHECKED 0** · **a REAL kit-path change** (a SIM develop `cd2679556b36` that edits anchoring.openapi.ts) → **`FAIL M6 RE-GATE: develop advance touches kit path(s) [...]`**. The two messages differ, so gate63/64's false-M6 defect cannot recur · an absent merge-in head is refused BY NAME |
| PR text | `gh_prtext_ex2.out` (rc 1) | 62 sentences: **10 TRUE, 1 FALSE, 51 NOT RE-DERIVED** · T1 one `Refs KS-723` + URL · T2 0 closing · T3 only KS-723 (body 6, title 1) · T4 title == subject (78) · T5 0 Co-Authored-By. **FALSE:** "the registration (one hunk at `:406`)". The commit's hunk is `@@ -407,6 +407,49 @@` (-U0 `@@ -409,0 +410,43 @@`); `:406` is the held carve's header (D11) |
| Actions | `gh_actions_ex1.out` (rc 1) | **1 run at the head** (`Dependabot standalone locks`, skipped). `PR Security Gates (KS-168)`, `PR — Lockfiles`, `Security Scanning`, `pr` and `pr-premerge-ack` are ABSENT, so **NOT RUN**. No previous head exists. The planted-name control is reported (D5) |
| API | `gh_api_ex1.out` (rc 0) | open, not merged, **mergeable false / `dirty`** (consistent with merge-tree's two conflicts) · body sha256/16 `d6adc2a75838b7e7`, 6,437 bytes == READY · title == kit · 1 commit, +354/-0, 5 files |
| census | `gh_census_ex1.out` (rc 0) | 25 other open PRs: **0 OVERLAP, 0 SPEC, 3 DOCS** (#1393 KS-1278, #1385 KS-938, #1383 KS-1401); the control fires |

## 2. Doubts for the gate (D1-D12; the drafter rules none)

- **D1 Tier** T1 (the spec drives the edge gate). Arguable T2 if Wednesday reads it as contract documentation only; W5 shows the edge change is tightening only.
- **D2 THE MERGE-IN DIVERGENCE. Wednesday rules; this is the most important item.**
  - **Key-anchored on 22b2 (live):** `e23888941fda2755a234590addfbeaaadf78bdcd`. On f0179806 it is `df1f8b7c61ad…`; the doc blobs are the same on both.
  - **`git merge-tree --write-tree --name-only a94ec8f6a2c6 <develop>`:** rc 1, tree-with-markers `dd8ec72867a2` (22b2) / `1680a8a97dae` (f017). **Both docs conflict; the readings below are identical on both develops.**
    - **Flow, 1 region (:2734-:2867):** OURS is the 16. block plus the old one-line `<h2>18. …</h2>`; THEIRS is #1390's 4-line split `18.` h2.
    - **Cheat, 1 region (:4327-:4485):** OURS is the old-format tail of KS-1005 plus KS-723; THEIRS is #1390's reformatted KS-1005 tail (86 lines).
  - **Hand readings (`c4_mergetree_devf017_ex2.out`).** None of take-OURS, take-THEIRS, OURS+THEIRS or THEIRS+OURS equals the key blob.
    - **"Take OURS" READS BACK RIGHT on BOTH docs** (flow 1..14 16 18 19; cheat KS-723 last), but it silently reverts #1390's formatting of develop's own `18.` heading and of KS-1005's tail.
    - The composee5 readers cannot see that revert. The kit's M8 now also requires "M minus the KS-723 block == develop byte for byte", and the TAKE-OURS SIM fails M1 + M8.
  - The kit makes the key tree the M1 authority. If Wednesday rules otherwise, pass `--predicted <tree>` and say so in the GO.
- **D3 Reader limit.** composee5's cheat reader `<h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>` under re.S **straddles** an unkeyed h2: its match START would then be the wrong heading.
  - Today all 6 / 7 cheat h2s are keyed.
  - The kit's position reader REFUSES when `<h2` opens != keyed matches, rather than mis-anchoring.
  - The flow number reader cannot straddle, because only `\s` sits between `<h2>` and the digits.
- **D4 Mixed formatting.** The KS-723 blocks land in the OLD one-line formatting inside docs that #1390 reformatted. If the merger reformats the block, M1's tree changes and the prediction is void.
- **D5 Actions NOT RUN at the head.** A dirty PR gets no `pull_request` workflows. They first run on M, so the GO should require `gh_gate67.py actions --at M --prev a94ec8f6a2c6…` with NEW-FAILING NONE.
- **D6** formatAnchorResponse emits `merkleRoot`, `merkleProof` and `slot`, which are undeclared on Anchor. This is pre-existing; `/document/{documentId}` shares the same `$ref`.
- **D7** The declared 400/403/429/500/502/503 never come from the handler. `dbGetAnchorByTx` swallows DB errors and returns `undefined`, so a DB outage answers **404**, not 500/503 (pre-existing).
- **D8** The op declares bearerAuth only, while the gateway edge also admits `sk_` connector keys, and Platform S, the named poller, may use one. The siblings are declared the same way.
- **D9** The new test file is TYPE-UNCHECKED (tsconfig excludes `src/__tests__`). This is a named NOT TESTED item.
- **D10** PREFLIGHT-INCOMPLETE 12/15 (legs 3, 4, 8) on a T1 change.
- **D11** One FALSE body sentence (`:406`). The drafter's view is that it is polish, not a blocker; the gate rules.
- **D12 BATCHING with gate66.** Whichever PR merges first voids the other's prediction (section 6a).

## 3. Kit files

| file | role | self-test | live run |
|---|---|---|---|
| `kit.json` | pins, blobs, claims, predictions, expected Actions set | — | — |
| `composee5_copy.py` | Seat E 5th's composee5.py, **verbatim** (sha256 `f9ab42d9fc25f189e62ccb4ad8e738a136cf17fb743ce7cbcbb3ee11d73cfee1`, source `…/5_Project_History/2026-10-05_seatE-5th/raise/composee5.py`). **Never executed**: its top level writes to E 5th's scratch | — | — |
| `lib_gate67.py` | read-verb git; write verbs only outside `!CODING`; GH GET by token name; **extracts the :66 / :82 readers from composee5_copy.py and refuses on a hash mismatch** | — | — |
| `c1_pin_gate67.py` | C1 P1-P11 | `c1_selftest_ex2` 3/3 | `c1_pr1394_dev22b2_ex1` rc 0 (11/11, own clone), `c1_pr1394_devf017_ex1` rc 0 |
| `c2_product_gate67.py` | C2 W1-W4, W7 + C3b W5 edge-gate port, W6 sibling | `c2_selftest_ex1` 6/6 | `c2_pr1394_ex1` rc 0 |
| `c3_tests_gate67.py` | redfirst / suite / spec (regen == committed, drift control) / tsc (+ blind-spot proof) | `c3_selftest_ex1` 6/6, `c3_refusal_forbidden_ex1` rc 2 | **NOT RUN** (the gate's) |
| `c4_docs_gate67.py` | h2proof, predict (key / wrong), mergetree (AGREE / DIVERGENCE + hand readings), qm M1-M8 | `c4_selftest_dev22b2_ex1` 16/16, `c4_selftest_ex1` 16/16 | h2proof ×2, predict ×6, mergetree ×3, qm ×9 |
| `gh_gate67.py` | api / actions / census / prtext (sentence by sentence) | `gh_selftest_ex2` 7/7 | api, actions, census ex1; prtext ex2 |
| `prompt_gate67.txt` | the gate's prompt, as a TEMPLATE with `{{MERGE_SEAT}}` ×4 | — | — |
| `launch_qa_secuura_ks723_1394.sh` | the launcher; reads ONLY `prompt_gate67.rendered.txt` | `launcher_check_*_ex3` (4 arms) | — |
| `repin_and_launch_gate67.sh` | the launch action (adapted from gate65's): renders, routes, API, ls-remote, head, develop, c1, check, usage, cockpit | `bash -n` only | **NOT RUN** |
| `api/` | pull 1394 JSON, body, files, runs at head (as read at drafting) | — | — |
| `RESULT.txt` | the drafter's summary | — | — |

`_quarantine/` holds superseded outputs and is never deleted:
- c4 mergetree ex1, from before the strict-ascending fix: the duplicate `18 18` read as ascending.
- qm ex1, a zsh word-split arm error.
- gh selftest / prtext ex1, from before the splitter and trailing-newline fix.
- c1 selftest ex1, which crashed on an absent path.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks723-1394|coagent@agentmail.to|yes
```
Until it is present, step 0 of the real launch refuses rc 1.

## 5. Launcher check (drafter; nothing launched, repin script not run)
`G67_PROMPT=<rendered copy>` was used with `launch_qa_secuura_ks723_1394.sh --check`:
- **`launcher_check_rendered65_ex3`** (seat 65th, a placeholder): rc 0. It records origin develop 22b268143a63 as NOT in the local store.
- **`launcher_check_template_ex3`** (the unrendered template): rc 8, unfilled token.
- **`launcher_check_seat64_ex3`** (rendered with 64th): rc 8.
- **`launcher_check_seat63_ex3`** (rendered with 63rd): rc 8.

ex1 (no README yet) and ex2 (the prompt before the 22b2 update) are in `_quarantine/`.

## 6. The merge-in: KEY-ANCHORED, NEWLINE-TOLERANT, composee5's readers
- The merger merges develop IN to `a94ec8f6a2c6`: a merge commit M with parents `[a94ec8f6a2c6, D]`. Never a rebase, never a force push.
- **Target tree (kit):** D's tree with the 3 code paths at the head's blobs.
  - **Flow** = D's flow with the head's `16.` block (from its `16.` h2 to its `18.` h2) inserted immediately BEFORE the line where D's `18.` h2 opens. D's `14.` must sit directly below it.
  - **Cheat** = D's cheat with the head's KS-723 section inserted immediately before D's `  </body>`, i.e. LAST.
- **On 22b2 (live) the target is `e23888941fda2755a234590addfbeaaadf78bdcd`.** On f0179806 it is `df1f8b7c61ad…`. git CONFLICTS on both docs, so the merger must build this tree by hand (D2).
- **For any later develop D:**
  - fetch D BY SHA into your OWN clone (never the shared checkout)
  - run `G67_SCRATCH=<scratch> python3 …/c4_docs_gate67.py mergetree --repo <clone> --develop-after <D>`
  - run `… predict --repo <clone> --develop-after <D>`
  - both refuse `develop unresolvable` BY NAME (rc 2) until D is present
  - a develop that touched a kit code / hook path is refused as `RE-GATE: develop advance touches kit path(s) …`
- The GO covers M only if `c4_docs_gate67.py qm --repo <clone> --merge-in-head M --develop-after D` passes M1-M8. Anything else re-gates.

### 6a. BATCHING NOTE (gate66 + gate67 in one QA session)
gate67 may run in the SAME QA session as gate66 (#1385, KS-938, kit `…/2026-10-06_gate66/`), because the two PRs' **product files are disjoint**: #1385 touches `services/auth` mfa.ts / users.ts and its test, and #1394 touches the anchoring registry, its test and the yaml.

**BUT BOTH PRs EDIT BOTH PLATFORM DOCS.** Each merge-in is predicted against whatever develop is live **when that PR merges**, and **the first one to merge moves develop for the other.**
- **If #1385 lands first,** develop gains its KS-938 sections (flow `20.` after `19.`, cheat KS-938 after KS-1005). Then:
  - every gate67 figure keyed to 22b2 is VOID: `e23888941fda`, the merge-tree reading and the qm SIMs
  - the gate67 merger re-predicts on the new develop
  - on that develop, the cheat's last keyed section is KS-938, not KS-1005, so KS-723 goes after KS-938. The flow slot (16. between 14. and 18.) is unaffected.
  - **The drafter SIMULATED exactly this.** The SIM develop `d3dac1d1e737` is f0179806 + gate66's key tree `fb6cb2c6992c`, and it gives gate67 key tree `7687fa98c69e` (flow `…14 16 18 19 20`, cheat `…KS-1005 KS-938 KS-723`). It is valid only if #1385 lands as exactly that tree on f0179806; on 22b2 it would differ by the two script blobs.
- **If #1394 lands first,** the same applies to gate66's `fb6cb2c6992c` (its f0179806 prediction).
- **Develop also moved under BOTH kits during drafting (f017 → 22b2, KS-1330).** gate66's kit is keyed to f017. Its repin path must accept 22b2: the advance touches no gate66 code path.
- Neither kit's prediction survives the other's merge. Neither verdict is affected, because a verdict is about its head, not about develop.

## 7. How Wednesday launches it (after section 4's routing line and the D2 ruling)

Pane `QA/Secuura-ks723-1394`. Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-ks723-1394-g67/`. Verdict subject `[QA -> Wednesday] GATE67 #1394 (T1 KS-723: declare GET /api/anchors/tx/{txHash} in the published OpenAPI contract; author Seat B 64th wrapping, merger a later B seat)`.

Fill `<NN>` with the B seat Wednesday assigns (for example `65th`). Never `64th` or `63rd`: the script refuses those with rc 9.

**Dry run** (no usage gate, no cockpit; NOT run by the drafter):
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate67/repin_and_launch_gate67.sh 1394 a94ec8f6a2c6ec382fb7b5dbafcf8a7f9ce68427 --merge-seat <NN> --dry-run --repin-develop 22b268143a6377c9a82cd03379daa596cd26d644
```
**THE launch command (NOT run by the drafter):**
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate67/repin_and_launch_gate67.sh 1394 a94ec8f6a2c6ec382fb7b5dbafcf8a7f9ce68427 --merge-seat <NN> --repin-develop 22b268143a6377c9a82cd03379daa596cd26d644
```
- On an unmoved develop (22b2, the kit's `develop_at_draft`), `--repin-develop 22b2…` is accepted as a confirmation. A different sha is refused rc 10 (stale).
- If develop has moved, for example because #1385 merged first, the script refuses rc 10 and prints `re-run with: --repin-develop <new sha>`. Read the printed advance first: on a new develop the kit has NO prediction, and the gate predicts.

Exit codes (gate65's, plus rc 9 for a bad `--merge-seat`):
- 1 routing
- 9 input or seat
- 2 ls-remote
- 3 API, or a blind census control
- 15 OVERLAP
- 11 head moved (RE-DRAFT)
- 10 develop moved / stale / not re-pinnable
- 13 C1, or the launcher's `--check`
- 16 override
- 12 usage gate
- 14 cockpit

**Rung 5:** in the pane, find all of:
- KS-723 / #1394
- `…/2026-10-06_gate67/README.md` or `QA_AGENT_CHARTER.md` read
- head `a94ec8f6a2c6`
- a `*_gate67.py --selftest`

Rung 6 is `NOT-TESTED.written-first.md` in the report dir.

## 8. Re-draft recipe (the head moved, or develop is not re-pinnable)
1. Re-measure `kit.json`: `head`, `end_tree`, `files`, `head_blobs`, `base`, `claims`, `merge_in_predicted*`.
2. Edit the head in `prompt_gate67.txt` and `launch_qa_secuura_ks723_1394.sh`.
3. Re-run every `--selftest`, then c1, c2, c4 h2proof + predict + mergetree, and gh api / actions / prtext / census.
4. A merge-in head on top of a94ec8f6a2c6 is NOT a re-draft. It is judged by `c4 qm`.

## 9. CHECKS C1..C6 and NOT TESTED

**Checks:**
- **C1** PIN.
- **C2** PRODUCT: security scheme vs middleware, envelope vs handler, spec delta.
- **C3** red-first / suite at both ends, same binary / spec regenerated + drift control / tsc + the type-unchecked blind spot.
- **C3b** ATTACKER: edge-gate diff base→head, sibling `{id}` not declared plus its what-if.
- **C4** DOCS: h2 proof, placement, merge-in predict / mergetree, Q-M.
- **C5** PR TEXT: sentence by sentence, keys, closing words, Actions vs the PR's own runs, mergeable_state.
- **C6** NOT COVERED.

**NOT TESTED by this kit (the gate's, or nobody's):**
- **C3 entirely:** red-first, the suite, generate-openapi regen == committed, check:openapi + drift control, and tsc. The builder's figures are claims only.
- **No live sweep:** the gateway serving the op, and the runtime body vs the declared envelope, are UNMEASURED.
- **The W5 edge diff runs on a Python PORT of specRouteMap.ts.** Two fidelity arms back it (KS-118 union, 401 on bearer), but it was not executed as TS.
- **The new test file's types:** it is outside tsc.
- **No Linear read** (KS-723).
- **Actions at the head:** none ran.
- **No predict / qm on a REAL merge-in M** (none exists yet).
- **The repin script:** no paths driven, no dry run.
- **The four platform suites:** no scan surface.
- **GET /api/anchors/{id}:** out of scope by Kam's card.
