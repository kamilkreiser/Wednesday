# QA GATE BRIEF — Secuura/Blockchain PR #1009 (KS-864, the #1007 gate's F-1007-1 follow-up, Seat A) — TIER 2 (through code), ROUND 1

**Charter — read first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Drafted 2026-09-17 01:27–03:06 AEST (from `date`; a network outage paused drafting between about 01:42 and 03:03, and origin was re-read at 03:03:43 with no move) by a Wednesday drafting subagent. Every fact carries its instrument inline. **"The seat" or "the READY" means relayed, not re-derived: an input to falsify.** "Drafter-measured" means the drafter read or ran it (read-only `git` on the Secuura checkout, the GitHub REST API with GET only, Linear GraphQL queries, or scripts in the drafter's OWN `git clone --shared`), and it is still yours to re-derive. Drafter scripts and outputs are in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1009/` (below: `GS/`). The READY mail, saved verbatim with spf, dkim and dmarc all passing: `GS/mail_1009_ready.md`.

**The gate this follows:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1007-b28ed490a-tier2-r1/report.md`. Read its **F-1007-1** (nothing pinned the portal env-var arm; tamper G-2 compiled and reddened 0 of 388), **P-1007-1** (TS1378 top-level await and a dead TS2554 `10_000` in ks864a/b) and **C-1** (a tamper that does not compile is VOID: run `tsc` on every tamper row), plus its §7 tamper method.

**Method lessons, binding:**
1. "Behaviour-neutral" is proven by an instrument that runs or parses the code, never by a regex.
2. `tsc -p services/api-gateway` **excludes `src/__tests__`**, so its rc 0 says nothing about test files. Use an **including** program, prove inclusion with `--listFilesOnly`, and plant a positive control.
3. Place tampers by **TEXT anchor with the count asserted = 1**. Run each against the **whole api-gateway suite** with the denominator asserted. Put **project `tsc` rc on every row** (C-1), read **numFailedTests AND numPendingTests**, and restore **sha256-identical**. For a test-file tamper, `tsc -p .` is blind, so give the including program's line count for that file instead.
4. Re-read Linear's **`attachments.metadata.linkKind`** immediately before the mail.

## WHY TIER 2, AND HOW MUCH

- **Tier 2, as Wednesday agreed on receipt** (`GS/answer_1009_receipt.md`). **Test only, drafter-measured:** `git diff --numstat 0308b7a04 6ec0cb198` lists 3 files, all under `services/api-gateway/src/__tests__/`. `system-status.ts` has blob `956083916` at base, head and develop (`GS/git_read.out`). No product byte changes.
- **Budget: proportionate.** Kam's 40% weekly usage cap applies (relayed). #1007 was already gated and this is its follow-up. **Time-box about 30 minutes.** Priority if time runs short: item 1 → item 3 → item 4 → item 2 → items 5–8. Report anything you did not reach as **NOT RUN, with the blocker named**.
- **NOT REQUIRED, said before running:** the parity grid (#1007's gate measured it, and no product byte changed); Schemathesis, Akto, Playwright and k6; docker or any stack; preflight legs 3, 4 and 8; the `packages/shared` suite; the real-app auth probe. List each under NOT TESTED as *not-applicable (why)*.

## TARGET

**Repo READ-ONLY:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. Clone by SHA into your OWN fresh `mktemp -d` (`git clone --shared --no-checkout`) and run every write verb there, from a script file. Never enter Seat A's worktree or the #1008 gate's clone, which is live in pane QA/Secuura-1008. Never touch `gatesets/2026-09-17_gate1008/`. 🔴 **NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout or any of its worktrees.**

**A PR is gated at a SHA. Your first act is to verify the head at origin:** `git ls-remote origin refs/heads/feature/ks-864-f1-portal-env-var-cells refs/pull/1009/head`, plus the PR API's `head.sha`. If the SHA differs, STOP, mail the moved head, and gate nothing.

| | PR #1009 |
|---|---|
| ticket | KS-864 (In Progress). Body has "Part of KS-864" ×2 and 0 closing phrases; title and commit message have 0 as well (regex with planted controls `Fixes KS-864` and `closes #12`, `GS/api_read.out` 01:29:57) |
| branch | `feature/ks-864-f1-portal-env-var-cells` |
| head | **`6ec0cb198`** (Wednesday's ls-remote 01:26:47; drafter's ls-remote 01:28:30 and 03:03:43; PR API 01:29:57) |
| parent = merge-base | `0308b7a0447a2c01c12aad358c9b4d04a5178210` (#1007's squash); one commit (`git log`, `merge-base`) |
| develop | `73d3fcb902d2a78fe68a4349903ff6c6bd24d4d5` (#1006's squash, child of 0308b7a04). Compare API `develop...head`: diverged, ahead 1, behind 1, files 3 |
| files | ks864a +3 −4 (`eb6ea8c22`→`6d119d23d`); ks864b +3 −4 (`a073703d2`→`3cfb1da89`); **ks864c-portal-env-vars.test.ts +80, new (`f886bdadf`)**. PR API +86 −8 |
| reviews / comments | 0 / 1 (`linear[bot]` linkback, 0 closing phrases) |

## THE SEAT'S CLAIMS (from the READY; inputs to falsify)

1. ks864c has two describe blocks (staging, development). Each beforeAll runs `vi.resetModules()`, sets all three `*_PORTAL_URL`, and imports a fresh `routes/system-status`. There is one red-proof cell per portal per env, 6 in all.
2. P-1007-1 in ks864a/b: the dead `10_000` Promise argument is dropped (TS2554); the top-level `await import` moves into beforeAll (TS1378); the server is typed as express's `listen()` return (TS2741, "pre-existing on develop").
3. Tamper table with tsc rc on each row: T0 12/12; G-2 issuer / verifier / admin each tsc rc 0 and reds only that portal's 2 ks864c cells; T0-after 12/12. AssertionErrors only, 0 skipped.
4. **Including tsc** (the seat's scratch tsconfig, include `src/**/*`): **53 → 47 overall**; KS-864 files **6 → 0** (TS1378 ×2, TS2554 ×2, TS2741 ×2); the new file adds 0.
5. api-gateway **46 files / 397 tests** (baseline 45 / 391 at 0308b7a04); shared 842/842; `tsc -p` rc 0; eslint clean on the three files.
6. Develop 73d3fcb90 is file-disjoint (#1006). Link: contributes KS-864. Preflight INCOMPLETE: 12/15 legs, with legs 3, 4 and 8 SKIPPED.

## DRAFTER-MEASURED INPUTS (re-derive them; a wrong one is Wednesday's error, so report it as one)

Substrate: `GS/drafter_setup.py` → `drafter_setup.out` (01:30:36). The trees are base `0308b7a04`, head `6ec0cb198`, and merged = head plus a local `--no-ff` merge of `73d3fcb90`, never pushed. node_modules is farmed per entry with `.vite` skipped, and `@secuura/shared` resolves IN TREE. Node v24.7.0, vitest 4.1.10, typescript 5.9.3, express 4.22.2.

- **D1 Suites (whole api-gateway):** base **45/391**, head **46/397**, merged **46/397**, all pass, 0 pending (`GS/drafter_run.first-run-resetModules-marker-matched-docblock.out`, 01:32; repeated identically in `drafter_run.resetModules-rows.out`, 01:33). The 6 new cells are exactly the 6 ks864c cells. **Merged = head for api-gateway by content:** the api-gateway tree hash is `2f3b012cc` on both, and base and develop share `fc77cc4ac`. Develop's delta 0308b7a04→73d3fcb90 is 5 files: 2 in `packages/shared/src/__tests__`, 3 in demo-service (`GS/git_read.out`).
- **D2 Tampers on head** (whole suite, denominator 46/397 asserted, `tsc -p .` rc 0 on every product row, sha-restored). Output: `drafter_run.first-run-…out` and `drafter_run.resetModules-rows.out`; summaries in `drafter_run_summary*.json`.

  | row | edit | reds (predicted = measured) |
  |---|---|---|
  | G-2 issuer | `url: process.env.ISSUER_PORTAL_URL \|\| 'http://issuer-frontend:80'` → `url: 'http://issuer-frontend:80'` | **2**: ks864c issuer staging + development |
  | G-2 verifier / G-2 admin | same shape | **2** each: that portal's two ks864c cells only |
  | S-A (#1007 seat's, re-run) | helper staging branch restored | **2**: ks864a staging-localhost + no-internal-ashypond. **P-1007-1 left the ks864a cells live** |
  | S-B (#1007 seat's, re-run) | issuer staging ternary restored | **3**: ks864b issuer-default, ks864b no-dead-estate, **ks864c issuer staging** |
  | Q-dev | issuer ignores its var only when `NODE_ENV === 'development'` | **1**: ks864c issuer development |
  | **Q-reset+dev** | Q-dev **plus** `vi.resetModules();` removed from ks864c | **0**. The development block reuses the module loaded under staging, so the Q-dev regression goes unseen |
  | Q-reset alone | `vi.resetModules();` removed | **0** |
  | Q-after | ks864c sets the vars AFTER the import | **6**: all ks864c cells, so the cells read import-time state |
  | Q-prod (residual) | issuer ignores its var only when `NODE_ENV === 'production'` | **0** |
  | Q-nullish (residual) | issuer `\|\|` → `??` (the empty-string arm) | **0** |
  | Q-probe | appended describe asserting NODE_ENV and the 3 vars equal `savedEnv` after both blocks | **0** reds (46/398) |
  | Q-probe CONTROL | Q-probe **plus** the afterAll restore removed | **1**: the probe (`expected ['development', …]`) |
  | T0-after | none | 0, 46/397 |

  First run: the reset rows ABORTED on a marker, because `resetModules` also appears in the docblock. They were re-run with the marker `vi.resetModules();` (the first-run output was kept by rename).
- **D3 Red-before-green:** ks864c alone on head, with `system-status.ts` swapped to the pre-#1007 blob `5b39da2ee` → **3 staging reds, 3 development green** (the development arm already honoured the var before #1007). Restored sha-identical (`drafter_run.resetModules-rows.out`).
- **D4 Including tsc** (`tsconfig.qa-including.json` extends `./tsconfig.json`, include `src/**/*`, exclude only node_modules and dist; `GS/drafter_static.py` → `drafter_static.out`, 03:04). `--listFilesOnly` lists 45 / 46 / 46 `__tests__` files, with ks864c listed at head and merged. **Raw error lines: base 34 → head 30 → merged 30.** In the ks864 files: base **4** (TS1378 ×2 at `(13,17)`, TS2554 ×2 at `(18,131)`) → head **0**. NEW base→head 0, GONE 4; head→merged 0/0. **0 TS2741 in any tree.** Positive control: `const qaPlanted: number = 'qa'` planted in ks864c gives TS2322 + TS6133 on ks864c; restored sha-identical. `tsc -p .` rc 0 in all three trees.
- **D5 P-1007-1 neutrality by parser** (`GS/parser_proof.cjs`, typescript 5.9.3). ks864a and ks864b each have `it()` 3/3 and `expect()` 3/3, identical base vs head. Applying only the typing edit to base leaves the transpile **identical** (control: `port = 1` differs). The JS delta is exactly 2 lines per file: the import moved into beforeAll, and the dead Promise argument dropped. Base plus those three edits reproduces head's source byte-for-byte.
- **D6 eslint:** 0 errors / 0 warnings on all three head files.
- **D7 Linear** (01:30:12): `attachmentsForURL(pull/1009)` = 1, on KS-864 (In Progress), `linkKind='contributes'`, open. KS-864 has attachments #1009 and #1007 (merged), both `contributes`, `completedAt` null. Facts comment `f4b9e646` present.
- **D8 Disjointness** (PR files API, 01:29:57): 0 files shared with #1008 (`dd7086d5a`, 2 api-gateway files) or with any of the 18 other open PRs.
- **D9 Env isolation, READ:** `vitest.config.ts` sets no `pool` and no `isolate`, so vitest 4 defaults apply (forks, isolate true). ks864a/b also restore `savedEnv` in afterAll.

## WHERE THE READY DISAGREES WITH THE DRAFTER (weigh; do not assume either side)

1. **Including tsc counts.** The seat has 53 → 47 overall and 6 → 0 in the KS-864 files, including **TS2741 ×2 "pre-existing on develop"**. The drafter's program has **34 → 30** and **4 → 0**, with **0 TS2741** anywhere, and the #1007 gate also recorded 4 NEW errors, not 6. The direction agrees: the KS-864 files go to 0 and ks864c adds 0. Find what program yields 53 and TS2741: a different include or exclude, different type resolution in the seat's worktree, or a counting key. State your program verbatim. PREDICTION: a counting or type-resolution difference with no product effect, a RECORD or at most a Polish on the seat's evidence.
2. **"vi.resetModules gives a fresh module per block" is true but not pinned.** Removing it reds nothing, and with a development-only regression present it hides that regression (Q-reset+dev = 0 vs Q-dev = 1). At head the portal expressions have no NODE_ENV branch, so the two blocks are near-duplicates today. PREDICTION: Polish at most (test quality); the gate weighs it.

## WHAT THIS GATE MUST ESTABLISH (minimum set)

1. **F-1007-1's red-proof, re-derived.** Run G-2 issuer, verifier and admin on the WHOLE suite with tsc rc per row (C-1), anchor count 1, sha256 restore, numFailed AND numPending read. Each must red exactly its portal's two ks864c cells and nothing else. Add **at least one tamper of your own aimed at the cells' SETUP** (the drafter used env-after-import, resetModules removed, and resetModules removed plus a development-only regression), and rule whether the cells observe a fresh module or are vacuous. Also re-run #1007's S-B (predicted to add ks864c's issuer staging cell).
2. **Coverage honesty (a residual, not necessarily a finding).** The cells pin the env-var arm under staging and development only. Say what stays unpinned: a production / test / unset / dev / demo-specific branch (drafter Q-prod = 0 reds), the empty-string arm (Q-nullish `??` = 0), and the default arm under development (ks864b pins defaults under staging only). The live gateways run `dev` and `demo` (#1007 report §0, READ ONLY).
3. **P-1007-1 is behaviour-neutral for the cells.** Prove it by parser (transpile compare with a control, `it`/`expect` identity) AND by the whole-suite counts. Show the ks864a/b cells are still live after the import move (S-A → 2 reds). Show the typing change is type-only.
4. **Including tsc**, with inclusion proven by `--listFilesOnly` and a planted positive control. Re-derive or refute 53 → 47, 6 → 0, TS2741 and "the new file adds 0" (see the disagreement above).
5. **Env leakage.** ks864c sets `NODE_ENV` and the three `*_PORTAL_URL` vars in beforeAll. Are they restored in afterAll (use a probe WITH a control that removes the restore), and does a whole-suite run as configured show any cross-file leak? Read the effective pool and isolate settings. Optional, only if time allows: a `--no-isolate` run, stating the file order.
6. **Merged tree.** Head plus CURRENT develop (73d3fcb90, or the then-current develop, judged by content) in your own clone. Run the suites on base 0308b7a04, head and merged, naming each tree.
7. **linkKind:** `attachmentsForURL(pull/1009)` must be exactly KS-864 `contributes`. Any closing phrase naming any ticket (body, title, commit message, comments) is a **Major**. Re-read before the mail. Never write.
8. **File-disjointness from #1008** (and the other open PRs), by the PR files API.

## BOUNDS

Loopback only; no docker, stack, kintsugi or demo; no `az`; never the wallet mnemonic. GH_TOKEN and LINEAR_API_KEY are read by NAME inside a script from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`, never echoed, GET and queries only. Never `rm`: use a fresh `mktemp -d` per attempt and quarantine scratch files by rename. Never `cd` in your tool calls, and use no write-verb git from the tool line. Use `/usr/bin/grep -i` with a same-file positive control. zsh: no PIPESTATUS (`rc=$?` on its own line), and never begin a line with `====`. Quote the Secuura checkout's porcelain count, `.git/config` sha256, for-each-ref count and worktree count at start and at close (drafter at 01:28:30: porcelain 0, config sha `e0fa706f…67632d1a`, refs 891, worktrees 111; refs move as other sessions fetch).

## REPORT

Write to `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks864-1009-6ec0cb198-tier2-r1/` (`report.md`, `evidence/`). Include FOUND / TESTED / HOW with controls; the tamper table (tsc rc, reds, pending and predicted-by on every row); the suites per tree; the including-tsc program verbatim; seat-claim dispositions; and **NOT TESTED at the same prominence as findings**. Every finding carries its evidence class, severity, target (PR or TICKET) and oracle.

## VERDICT DESTINATION

ONE mail to `wednesday-agent@agentmail.to`, subject EXACTLY:
`[QA -> Wednesday] TIER 2 GATE #1009 (KS-864) 6ec0cb198 — <GO | GO WITH FINDINGS | NO GO>`

The body holds the report's BLUF, then plain statements on items 1–8, then the merge ADDENDUM: "squash `6ec0cb198` onto develop `73d3fcb90` (or the then-current develop; file-disjoint from #1008); #1009 attaches to KS-864 only, linkKind contributes, and KS-864 stays In Progress; equality targets ks864a `6d119d23d` / ks864b `3cfb1da89` / ks864c `f886bdadf`; api-gateway 45/391 → 46/397 (re-measure); Records: <yours>". Then the NOT TESTED block and the report path.

**Mechanism note.** The QA project has no `send_brief.sh` of its own. The verdict mails that have reached Wednesday were sent from `coagent@agentmail.to` through the AgentMail API:
- `POST https://api.agentmail.to/v0/inboxes/coagent@agentmail.to/messages/send`
- JSON body `{"to": ["wednesday-agent@agentmail.to"], "subject": "...", "text": "..."}`
- header `Authorization: Bearer $AGENTMAIL_API_KEY`, with the key read by NAME by your script from `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env` and never echoed

**The MAIL is the END STATE.** Confirm the API answered 2xx and quote the message id in your final pane line. Timestamps come from `date`, never estimated.

## NOT COMMISSIONED

Any fix (a production-arm or empty-string cell, pinning resetModules, the seat's tsc program): those are the owner's. Also not commissioned: #1008 and its gate; the parity grid and the real-app probe (done on #1007); Akto, Playwright, k6 and Schemathesis; any deployed environment.
