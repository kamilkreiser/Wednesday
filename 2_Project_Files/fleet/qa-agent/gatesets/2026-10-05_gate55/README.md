# Gateset 2026-10-05_gate55 — README for Wednesday

Drafted 2026-10-05 AEDT. The work ran 2026-10-04 15:46Z – 16:13Z UTC (`date -u`). Each figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate55 is a T2 gate over ONE Secuura/Blockchain PR: #1375, KS-1015, Seat B 58th's PR B** — "the delegation GET spec declares the envelope its handler returns". Seat B 58th is author and merger.
- **Head:** `16784d620080b331c0f6adc669b943015bde5dde` on `feature/ks-1015-delegation-get-spec-declares-envelope-b55-2`, tree `4e35c85604231119a7848ade639a934a45642ff2`.
- **Base:** develop `2d85b84e1012961c880daa3de70d8491fc0a2ff9` (#1374's squash; tree `082190611d1f` == gate54a's END_TREE).
- **PR number:** #1375, from Seat B 58th's READY (2026-10-04T15:55:00Z). The commission said the PR was not raised yet. It was raised while this kit was being drafted: the drafter's `ls-remote` read `refs/pull/1375/head` == the branch == `16784d620080` at 15:54:29Z and again at 16:11:19Z.
- **The READY's head matches the drafted head.** So there is no re-draft: the kit is ready for #1375 at `16784d620080`.

**Status: KIT COMPLETE, NOT LAUNCHED.** Two things are Wednesday's: the routing line (section 4) and the launch (section 5).
- The dry run against #1375's real origin refs returns **rc 0** (`repin_dryrun_ex2.out`, 16:12:18Z – 16:12:32Z). Its API and census half is a SIM replay; see section 6.
- The only thing the dry run reports is the missing routing line.

**What the drafter did:**
- **Kit files.** It wrote only into this directory and its scratch dir `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8e88f5e9-abc4-4750-a2ee-28cce52428dd/scratchpad/gate55/`.
- **Git verbs in `!CODING/`.** It ran only `ls-remote`, `show`, `log`, `diff`, `cat-file` (including `--batch`), `ls-tree`, `rev-parse` and `grep`. `lib_gate55.git` refuses any other verb.
- **Stat-only checks.** The SIM launcher `--check` also ran two stat-only `[ -d ]` tests on `!CODING/` directories. They read no file content.
- **Not done:** no clone or fetch, no worktree in the Secuura repo, no mail sent, no launch, no edit to `inbox_routing.conf`, no `rm`.
- **No secrets read.** It did not read the Secuura `.env`. Every GitHub answer in the exercises is a SIM replay (section 6).
- **Npm cache.** The npm cache was redirected to scratch. Nothing in `~/.npm` is newer than `kit.json`.
- **Refusal arms.** Every refusal arm used a path under scratch, with `G55_FORBIDDEN_ROOT` pointing at a scratch stand-in. **Nothing was created by any refusal.** `c3_refusals_created_ls_ex1.out` shows the stand-in holds only the `ws/` fixture. `ls scratch/ev` shows no `x1`, `x2`, `x3`, `x4` or `out_*` directory.

**The runtime half was MEASURED, unlike gate54a's.**
- **The export.** The drafter exported both trees into scratch with `git cat-file --batch`, committed them in a scratch repo, and proved the trees identical by hash: `write-tree` == `082190611d1f` (base) and `4e35c856` (head).
- **What then ran there:** `npm ci`, the cells, both suites, tsc, `generate-openapi`, the drift control and `check:openapi`.
- **What the tester still does:** re-run all of it in its own clone (the prompt says so).

## 1. Drafter predictions on #1375 at 16784d620080

| check | file | result |
|---|---|---|
| C1 pin | `c1_live1375_ex1.out` | **PIN PASS 14/14** (details below this table) |
| C2 regenerated | `c2_plan_ex1`, `c2_regen_ex1`, `c2_control_ex1`, `c2_checkopenapi_ex1` | **PASS** (details below) |
| C3 cells / suites / tsc | `c3_runbase_ex1`, `c3_runhead_ex1`, `c3_tscbase_ex1`, `c3_tschead_ex1`, `c3_tsccontrol_ex1` | **PASS** (details below) |
| C4 docs §4 | `c4_pred_simbody_ex2.out` | **15/15 PASS** (details below) |
| C5 spec == handler | `c5_pred_ex1.out` | **8/8 PASS** (details below) |
| C6 not covered | `c6_pred_simbody_ex1.out` | **6/6 with the SIM body** (details below) |
| census | `census_*_ex1` | **SIM only** (details below) |

**C1 pin:**
- The live `ls-remote` half reads `refs/pull/1375/head` == the branch == HEAD.
- The PULLS API half is a SIM replay.
- ONE commit over develop; head and tree == drafted.
- The 5 paths match by numstat == the builder's figures: yaml +38/-1, test +79/-0, openapi.ts +23/-1, flow +145/-0, cheat +35/-0.
- 0 trailers; the control prints 1.
- 0 of #1373's 4 files (the control lists 4).
- 0 `services/timestamping/**` paths (the control lists 8).
- Modes are 100644 (control 100755).

**C2 regenerated:**
- `generate-openapi` reproduces the YAML byte-identically: sha256 `373ef7805f88…` before and after, 39,928 lines, 219 `required: true`, 0 dirty.
- `--check` returns rc 0 with CHECK PASS.
- **Reverted-YAML control: rc 1** with `CHECK FAIL: generated YAML differs`. The sha256 `e761a0b3c1ea…` is unchanged by the check.
- The YAML was restored to `373ef780`.
- `check:openapi` returns rc 0 (405 example blocks); a planted line gives rc 1.

**C3 cells, suites and tsc:**
- **Base:** the suite is 4 files / 70 tests with 0 failed. With the head test planted (sha256 `d55f7ef4be4e…` == B 58th's anchor), **D1-D3 are red, 3 of 3 AssertionError, 0 load markers, and C1-C3 are green.**
- **Head:** 6/6 cells; 5 / 76 tests; +1 file and +6 tests, which are exactly the cells; **0 new reds.**
- **tsc 5.9.3** (named binary) gives rc 0 / 0 errors at both base and head. The program has 475 files, 10 under `transfer/src`, and **0 under `__tests__`**.
- **The control:** a planted type error gives rc 2 with 2 errors naming `delegations.ts`; the file was restored by blob.

**C4 docs §4:**
- One insert hunk per doc, after the KS 1402 block: flow before base `:1734 <script>`, cheat before base `:3689 </body>`.
- The KS 1402 block is **byte-identical at the same lines**: flow 1626-1732 (107 lines), cheat 3661-3687 (27 lines).
- Timing figures (`373–375 ms`, `0.79–0.83 s`) are dated and name host Kamils-Mac-Studio.
- The base timing grep reproduces 1/1/1 per doc, all inside KS 1402. `KS 1015` is 0 and `delegation` is 0. The must-hit control `auth` is 68 / 67.
- **D5b: 0 suite-term hits outside the KS 1402 and KS 1015 blocks at head, and 0 table rows added.**

**C5 spec == handler:**
- `delegations.ts:138` is `router.get('/:id'`.
- `:148-:152` is `res.json({ success: true, data: { delegation, chain } })`.
- `:146` binds `chain = buildDelegationChain(delegation)`.
- `:142` is the 404 `NOT_FOUND` envelope.
- In `index.ts`, `:438` `jwtAuthenticate` is registered before `:441` `/api/delegations`.
- `delegationService.ts:471` returns {rootDelegatorId, chain, totalDepth, isValid, invalidReason}. In `delegation.types.ts:77-82`, `invalidReason?` is optional.
- The YAML's 200, 401 and 404 match.
- The runtime files are blob-equal base == head.
- **The control on the base YAML FAILS, as it must.**

**C6 not covered:**
- The classifier reads 0 runtime source paths here. Its controls read 2 for #1374 and 0 for #1373.
- **The real PR body was not read** (section 6).

**Census:**
- clean replay: 0 OVERLAP, Seat D 4th's KS-1404 classed EXPECTED, #1360 classed client-human.
- over-reach replay: OVERLAP, launch refuses rc 15 (`repin_dryrun_census15_ex1`).
- second KS-1015 PR: OVERLAP.

## 2. Doubts for the GATE to rule
The drafter rules none of these. All are in the prompt.

- **D1 — the body claim.** The READY claims the PR body is 6,940 B, sha256 `a3b4b49b7d66…`. The tester hashes the body the launch action saves.
- **D2 — "the other 27 KS-1015 pairs remain unowned"** appears in both doc blocks and the READY. **KS-1015 was ALREADY narrowed once**, by #1367 (squash `ed268a995a88`, the referral lookup pair, merged 2026-10-01 and on develop; `git log`). If 28 was the sweep's original total, the true remainder is 26. This is a factual claim inside a §4 doc block. The drafter cannot tell what "28" counts.
- **D3 — KS-1402 is hyphenated in the new doc prose** ("the KS-1402 block of section 9"). Docs are not squash surfaces. This is information.
- **D4 — the `Delegation` component's required set (7) is narrower than the TS `interface Delegation`'s non-optional fields (12)** (`c5_pred_ex1.out` INFO). This is pre-existing and unchanged by the PR.
- **D5 — `GET /:id` is async with no try/catch on Express ^4.18.2.** The operation declares the shared 400/403/429/500/502/503 set; this handler emits none of them. This is pre-existing and READ ONLY.
- **D6 — `.passthrough()` on the zod `data` / `chain` objects** is not rendered as `additionalProperties`. OpenAPI's default already permits extra keys.
- **D7 — the flow block's timing paragraph** quotes base-side counts and says a head-side count cannot be reproduced by construction. The kit's D5b measures the stable claim instead.
- **D8 — B 58th's own instrument faults** (the self-falsifying sentence, the vacuous 2-line span). The kit re-measures the KS 1402 identity independently (`c4` D3c, with MIN_LINES 20).
- **D9 — the push preflight ran 12/15 legs.** It skipped leg 3 (Spec-auth conformance), leg 4 (Path resolvability) and leg 8 (Served-spec consistency), because no local stack was up. These are the three legs nearest a spec change. The holds forbid a live server, so they stay NOT COVERED; the gate rules whether that blocks a T2.

## 3. The kit's instruments
Every tool was exercised both ways. Outputs sit beside it as `<name>_exN.out/.err/.rc`.

| script | what it does | exercised runs (rc) |
|---|---|---|
| `lib_gate55.py` | Shared helpers: `git()` allows 8 read verbs only. `guard_out()` tests the lexical path first, then the realpath, then runs mkdir. `GH` does read-only GETs or an `--offline-dir` replay. | imported by all |
| `guards_gate55.sh` | Sourced guards: the WS must be outside `!CODING/`, clean, with HEAD^{tree} == the side's tree. The OUT goes through `guard_out`. Blob plant / restore and quarantine (never rm). | through c2/c3 |
| `c1_pin_gate55.py` | C1 P1-P9 and END_TREE | help (0); short sha (2); **SIM all-pass (0)**; **live origin + SIM API for #1375 (0)**; live origin with a fake PR number (1: P1); **moved head 2971e504 (1: P3b + P4)**; **#1374's head as control (1: 7 FAIL)**; bad body: hyphenated KS-1402, `Closes`, no Refs (1: P6 ×2) |
| `gh_census_gate55.py` | API line, body save, census classes | help (0); bad PR number (2); clean (0, 0 OVERLAP); over-reach (0, 1 OVERLAP); a second KS-1015 PR (0, 1 OVERLAP) |
| `c2_regen_gate55.sh` | C2 plan / regen / control / checkopenapi | help (0); **plan (0)**; plan on the scratch repo, where the base and head commits are absent (1: R1-R3 — rev-parse's echo caught); **regen (0)**; **control (0: --check rc 1, writes nothing)**; **checkopenapi (0; planted rc 1)**. Refusals: wrong tree (2); dirty WS (2); OUT through a symlink into the forbidden stand-in (2) |
| `c3_cells_gate55.sh` + `c3_parse_gate55.py` | C3 install / run / tsc / tsc-control; the parser has 14 self-test arms | help (0); **parse-selftest ex1 (1, BROKEN 13/14: an unexpected cell id was ignored — fixed) → ex2 (0, 14/14)**; **install base/head (0, 0)**; **run base (0)**; **run head (0)**; **tsc base/head (0/0)**; **tsc-control (0)**. Refusals: WS in the forbidden stand-in (2); OUT in the stand-in (2); OUT through a symlink (2); wrong tree (2) |
| `c4_docs_gate55.py` | C4 D0-D7 | help (0); **selftest ex1 (1, BROKEN 14/15: D5b assumed line numbers — fixed) → ex2 (0, 15/15)**; **base-vs-base (1: D1, D3, D3b)**; pred with the SIM body (0, 15/15); pred without a body (0, D7 NOT RUN, said so) |
| `c5_handler_gate55.py` | C5 H0-H7 + INFO | help (0); **pred (0, 8/8)**; **selftest (0, 9/9)**; **head == base (1: H5)** |
| `c6_notcovered_gate55.py` | C6 N1-N6 | help (0); no body (2); **selftest (0, 6/6)**; SIM body (0); bare body (1: 5 FAIL) |
| `fill_gate55.py` | fills the prompt, launcher and pins | help (0); bad args (1); stale base (1); **moved head (1)**; previous-report sha mismatch (1); **SIM #1375 (0) ×2** |
| `launcher_gate55.TEMPLATE.sh.txt` | the launcher: gate54a's guards, re-keyed, plus `G55_COMPARE_FILE` (--check only) | SIM `pr1375.SIM.launcher.sh`. **ex1: all rc 8, because README/COMMISSION were not written yet (a real arm: a missing kit file refuses).** ex2/ex3: `--check` (0); wrong head (6); moved develop (17); bad compare (10); a missing keyword (33); a missing C-phrase (34); no charter (8); a missing hold (39); moved kit (2); stale pin (9); **no TTY (21; the only non-`--check` run, stdin `/dev/null`)** |
| `repin_and_launch_gate55.sh` | the launch action | help (0); bad args (9); **real path, routing absent (1: refuses at step 0)**; **dry run #1375 / 16784d620080 (0) ×2**; wrong head (11); moved head (18, via `G55_EXPECTED_HEAD`); census over-reach (15) |
| `prompt_gate55.TEMPLATE.txt` | the tester's prompt (24 by-name keywords) | filled as `pr1375.SIM.prompt.txt` and `dry16*.SIM.prompt.txt` |
| `sim/` | exercise inputs: `make_sim_gate55.py` (reads real numstat / shas), the SIM body, the replays, `compare_ok.txt` | `sim_make_ex1-3` (0) |

- `*.SIM.*`, `pins_gate55.SIM-*.json`, `dry_*`, `sim/` and `c3_selftest_console.fixture.txt` are exercise artefacts. They are never launched.
- The real `pins_gate55.json` does not exist yet.
- No `__pycache__` was created (`PYTHONDONTWRITEBYTECODE`).

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1015-1375|coagent@agentmail.to|yes
```
Until that line is present, step 0 refuses with rc 1 (`repin_realrouting_ex1`).

## 5. How Wednesday launches it
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate55/repin_and_launch_gate55.sh 1375 16784d620080b331c0f6adc669b943015bde5dde --dry-run
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate55/repin_and_launch_gate55.sh 1375 16784d620080b331c0f6adc669b943015bde5dde
```
- **Set no `G55_*` variable.** A real launch refuses on any (rc 16).
- **The sequence:** PULLS API + census → ONE ls-remote → rc 11 head guard → rc 10 stale base → **rc 18 moved head** → fill → race re-read → override (16) → usage gate (12) → launcher `--check` (13; STALE PIN exit 9) → `cockpit.sh add` (14).
- **First real reads.** The real dry run is the first to read GH_TOKEN, the live census and gate54a's report hash (section 6).
- **If Seat D 4th's KS-1404 PR merges first, develop moves.** That is rc 10, a RE-DRAFT, and THE DOC RULE applies.
- GO subject: `GO (Seat B 58th): merge 1375 on gate55`.
- END_TREE `4e35c85604231119a7848ade639a934a45642ff2` while develop == `2d85b84e1012`.

## 6. UNMEASURED, and why

**GitHub (live API never called):**
- **No live GitHub API call was made.** The drafter did not read the Secuura `.env`, because the commission allows only read-only git verbs under `!CODING/`.
- So these are all SIM replays built from real git numstat: C1 P2/P4's API half, the census (the real open-PR list, including whether Seat D 4th's PR is open and what it touches), and the launcher's compare.
- **The real PR body was never read.** C4 D7 and C6 N2-N6 ran only against `sim/SIM_body_ok.md`. Their regexes may FAIL on wording the drafter did not predict; the tester rules on the sentence. B 58th's body hash is only its claim (D1).

**Files under `!CODING/` not read:**
- **gate54a's report hash `5d4896bc…` was not re-hashed by the drafter.** It is taken from the gate54a verdict mail. The real fill hashes the file; a mismatch is rc 10 at launch.
- **The default forbidden-root refusal (`/Volumes/DevMASTER/!CODING/`) was never driven with a real path.** That is by the commission's rule. Only the scratch stand-in was used; the code path is the same, with the root from `kit.json`.

**Where the runtime arms ran:**
- **They ran in a SCRATCH EXPORT, not a clone.** The trees are identical by hash, but the `.git` metadata and hooks differ. The tester's clone is the measurement.

**Launch steps:**
- **Not exercised:** the real launch steps 4-7 (override, usage gate, `cockpit.sh add`) and the routing-present path. These need Wednesday's routing line and a real launch.

**Live behaviour:**
- **No live handler response; no live service, so no §5f sweep.**
- **The preflight legs 3/4/8 were not run.** They need a local stack (D9).
- No Linear read. No read of Platform S.

## 7. Defects seen (commission and B 58th's plan)

**In the commission:**
- **"The PR is NOT raised yet" was already stale.** #1375 was pushed 15:44:44–15:51:01Z and READY'd 15:55:00Z.
- **B 58th's brief names Seat D 3rd as the co-tenant, but the 15:29Z mail shows Seat D 4th now.** The kit names D 4th, same lane.

**In B 58th's plan:**
- **The doc blocks' "other 27 pairs unowned" ignores #1367** (D2).
- **Its pathgate's co-tenant must-hit control fires on #1373's lock and baseline paths ("co-tenant-filter 4").** So it never shows the `services/timestamping/**` arm can hit. This is READ ONLY, from its READY. The kit's P8 control uses Seat D 3rd's pushed KS-1404 diff (8 timestamping paths) instead.
- **Nothing in its plan runs the spec-live legs** (D9).

**In this drafting:**
- **Two of the drafter's own self-tests fired BROKEN first:**
  - the c3 parser ignored an unknown cell id;
  - c4 D5b assumed the KS 1402 block keeps its line numbers.
  Both were fixed, and the `_ex1` → `_ex2` runs are kept.
- **A stray line in `c2 plan` would have written into the kit dir** (gate54a's N-1374-5 class). It was removed before any run.

## 8. Timeline (UTC, 2026-10-04)
| time | event | source |
|---|---|---|
| 15:37:38Z | B 58th STATUS item1: pre-doc head `2971e504`, all green | mail |
| 15:42:52Z | amend into the doc'd commit (lock taken) | 15:44Z mail |
| 15:44:11Z | STATUS item2: head `16784d620080`, docs +145/+35 | mail |
| 15:44:44–15:51:01Z | push, preflight 12/15 (legs 3 4 8 SKIPPED) | READY |
| 15:46:17Z | drafter `ls-remote`: develop `2d85b84e`, branch ABSENT, highest pull 1374 | `lsr1.out` (scratch) |
| 15:54:29Z | drafter `ls-remote`: branch + `refs/pull/1375/head` = `16784d62` | scratch `lsr2.out` |
| 15:55:00Z | READY FOR QA (Seat B 58th) #1375 → gate55 | mail |
| ~15:57Z | scratch export: `write-tree` `082190611d1f` / `4e35c856` == real trees | scratch repo |
| 15:59:35–16:00:36Z | `npm ci` base (29 s) and head (22 s), 1,934 packages each | `c3_install_*_ex1` |
| 16:00:43–16:01:31Z | cells, suites, tsc, regen, drift control, check:openapi | `c3_*`, `c2_*` |
| 16:03–16:05Z | c4, c5, c6 | `c4_*`, `c5_*`, `c6_*` |
| 16:09–16:12Z | fill, SIM launcher arms, dry runs | `fill_*`, `launcher_*`, `repin_*` |
| 16:11:19Z | `ls-remote` re-read: unchanged | — |

## 9. Re-draft recipe (develop moved, or a new head)
1. **On a new head:**
   - Update kit.json: `expected_head`, `expected_tree`, `drafted_head_blobs` and `numstat_claim`.
   - Update `prev_blocks_base` / `new_block_anchor_base` only if the base docs moved.
   - Re-run `sim/make_sim_gate55.py`, `c1` (SIM + live), `c4 --selftest` / base-vs-base, `c5 --selftest`, `c6 --selftest`, and the C2/C3 runtime arms in a fresh scratch export (prove both tree hashes first).
2. **On a develop move** (e.g. Seat D 4th's squash): also update `base`, `base_tree`, `base_parent`, `base_blobs`, `prev_blocks_base` (re-hash), `timing_base_counts` / `timing_control_counts`, and `suite_claim`. Under THE DOC RULE a KS 1404 block may now sit beside KS 1402; D3b's anchor and D5b's "inside a block" set then need the KS 1404 block too.
3. Run `fill_gate55.py --simulate`, then the SIM launcher `--check`, then `repin_and_launch_gate55.sh … --dry-run`.
