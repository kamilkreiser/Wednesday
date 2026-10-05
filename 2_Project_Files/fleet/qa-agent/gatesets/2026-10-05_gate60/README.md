# Gateset 2026-10-05_gate60 — README for Wednesday

Drafted 2026-10-05, 07:23Z – 07:58Z UTC (18:23 – 18:58 AEDT; times from `date -u`). Every figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate60 is a T1 gate over ONE Secuura/Blockchain PR: #1384, KS-1210, "close OAuth app scopes to the published nine, gate the by-id routes".**
- Built by Seat E 2nd as ONE unpushed commit; pushed AS BUILT and raised by Seat E 3rd, who is also the merger. Pane `Secuura/Blockchain-E`.
- **The head is a SINGLE-PARENT commit on develop** (no merge-in folded):
  - head `852fc927632095fb603583cb543050d5edd66111`, parent `46c3e20cfbd2` (== develop), END_TREE `632b07492c9501ad4e36bd5f20b62e4240b7394e`
  - branch `feature/ks-1210-oauth-app-scopes-and-ownership-e3-1`
- **Exactly 6 paths differ from develop** (`c1_pr1384_ex1.out`): the new ks1210 test (+291), ks431 (+18/-6), ks451 (+7/-1), `routes/oauth.ts` (+93/-8), flow doc (+84), cheat doc (+36).
- **#1381 and #1382 are ruled to land FIRST.** Each conflicts with #1384 on the two docs only, so #1384 WILL need a docs-only merge-in before it merges. The gate judges the head itself, and that later merge-in with `c4_docs_gate60.py qm` (Q-M M0-M7 + Q-M+, kit `q_m`).

**Status: KIT COMPLETE, NOT LAUNCHED.**
- Every checker has a positive control and must-fail tamper arms; all were run and all fire (section 3). Selftests only: no suite, no tsc, no vitest, no probe was run by the drafter (the commission's rule).
- The live dry run returns rc 0 and reports only the routing line as missing (`dry_console_ex1.out`; section 7).
- Two things are Wednesday's: the routing line (section 4) and the launch (section 5).

**What the drafter did:**
- Wrote only into this directory and into `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g60/`.
  - That scratch holds a `git clone --shared --no-checkout` of the checkout (`clone/`), with THREE fetches (07:24:03Z develop + pull/1384 + pull/1381 + pull/1382; 07:47:23Z pull/1383; 07:48:36Z pull/1385), each with the checkout's own `core.sshCommand`. No worktree, no install.
  - It also holds the PR body (`pr1384_body.md`), the census JSONs, and the type-stripped probe used for the syntax check.
- In `/Volumes/DevMASTER/!CODING/`: only read verbs (`ls-remote`, `config --get`, `show`, `ls-tree`, `cat-file`, and the `clone --shared` source read).
- Read (never wrote) Wednesday's `scratchpad/e3/vclone` with `cat-file` / `ls-tree`, to identify the READY's "predicted trees" (section 2, D6).
- Network: GitHub REST GETs only (pulls, files, the open-PR census). GH_TOKEN read by name, never printed. **No Linear read** (the gate's X8).
- Not done: no launch, no routing edit, no mail, no comment, no ticket change, no `rm`. Python wrote `__pycache__/` here on import, as gate59's kit did.

## 1. Drafter predictions on #1384 at 852fc9276320 over develop 46c3e20cfbd2 (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1384_ex1.out` (rc 0, 9/9) | ls-remote pull/head == branch == API == input; open, base develop == ls-remote develop, changed_files 6; ONE parent == develop, rev-list 1; 6 paths by numstat AND API; END_TREE equal (control develop tree `dab6adb69ea3` differs); 0 trailers (control `bf277eead268` = 53 bytes stripped / 55 raw); subject 76 chars, `(#` 0; ONE `Refs KS-1210`, only KS-1210 hyphenated (`KS 431`, `KS 451`), 0 attribution lines |
| C2 hunk + class hunt | `c2_pr1384_ex3.out` (rc 0, 7/7) | services/oauth.ts, users.ts, authenticate.ts byte-identical; oauth.ts removes exactly 4 non-comment lines; both schemas = the closed enum; real AVAILABLE_SCOPES == the nine; the 3 copied lists == users.ts (independent parser); **4 of 4 by-id handlers gated before any service call, 404 on falsy**; PATCH 404 before 403; POST gate on the FOUR list; siblings fixture-only (it() 13→13 / 4→4, expect() multisets equal). INFO: 0 tenant mentions in all four handlers; /authorize + /token resolve by client_id; listApps(undefined) is unfiltered; users.ts has FOUR `const ADMIN_ROLES` (:439 :495 :551 :583, 2 distinct lists) |
| C3 red-first | (not run — prediction) | at develop: A1-A4 A6 B1 B2 B5 C1-C4 C8 D1 (by `expected 201/200 to be 400/403/404`) and E1 E2 E4 (THROWN `declaration not found`) = **17 red**, A5 B3 B4 C5 C6 C7 E3 = **7 green** — derived cell-by-cell from the develop source; equals the author's 17 \| 7. Judge selftest `c3_selftest_ex2.out` 17/17 |
| C3 siblings / suite / tsc / openapi | (not run) | predicted: develop's ks451 red at head (`analytics:read`), develop's ks431 red or load-failing at head (`AVAILABLE_SCOPES: []`); head's two green at develop. Suite develop 840 / 78 (gate59's measurement) → head 864 / 79; ks949 blob `4f03e6f4f132` identical base/head (C2 read). tsc and check:openapi: the author's figures only |
| C3b probe | (not run — syntax-checked) | 23 cells over the REAL services/oauth + an in-memory oauth_apps table. Predicted develop: **V1 P1 P2 P3 O1 O3 O4 O7 L2 red**, 14 green; head 23/23. Syntax: type-stripped + `node --check` rc 0; planted-error control rc 1 (`scratchpad/g60/probe_syntax*.{out,err}`) |
| C4 docs | `c4_docs_ex3.out` (rc 1, 2 FAIL of 20) | PASS D1-D7 (one pure insert 84 / 36 lines before `  </body>`, flow [1..12, 18], h3 18.1-18.4, cheat unnumbered + wrapped + balanced, self-contained both docs), D8b (PR regex: services/auth 7 mentions / 0 near a duration; Akto control 134 / 11 — the body's figures reproduce). **FAIL D8** (2 units: flow 18.3 "5000&nbsp;ms timeouts", cheat "5000 ms" row — no date+host) and **D9** (docs "864 passed, 0 failed" + "did not recur" vs body run 1 "862 passed, 2 failed" at the same head) |
| C4 predict | `c4_predict_ex4.out` (rc 0, 6/6) | MP0 no-op merge == END_TREE. Independent number-order resolutions: vs #1381 `bded1f6b95d0` (13 above 18), vs #1382 `ad1b013939b2` (18 above 19), vs #1383 `2edfcaf8bed6` (18 above 22), vs #1385 `a97e22330e36` (18 above 20); each a docs-only conflict; wrong-order controls all differ. **MP3 chained (#1381 → #1382 → #1384): SIM develop2 == gate59's own SIM tree `df1344507d8c` (cross-check), #1384's predicted merge-in tree `552970edf014dd88d9c9e9bb3c47ce97345c7980`**, flow numbers [1..13, 18, 19] |
| C4 qm control | `c4_qm_basevsbase_ex1.out` (rc 1) | the head judged AS IF a merge-in over develop: FAILS M2 / M3 / M6 — the judge can fail on real objects |
| C5 PR text | `c5_pr1384_ex1.out` (rc 1, 1 FAIL of 8) | PASS T1-T7 (Refs + URL, 0 closing, own key only, title == subject, method stated, 6 sha/blob claims, Q-1210 rulings). **FAIL T8**: the DELETE-of-a-missing-id 404 (was 200) is NOT in the body although the DELETE handler's comment says it is. INFO: 1 of the 6 destructive scopes named. Body 7,275 bytes / 7,231 chars, sha256 `75c76aa6f87c095f…` |
| C6 NOT COVERED | `c6_pr1384_ex2.out` (rc 1, 1 FAIL of 3) | one section; all 4 required items inside it. **FAIL N3**: the "tenant bound" item is about the ROLE LISTS ("Both role lists were verified by reading users.ts"), not the tenant boundary |
| census | `census_ex3.out` (rc 0) | 25 others; **0 touch routes/oauth.ts or services/oauth.ts** (control FIRES on #1384); 4 EXPECTED OVERLAPS, docs only: #1381, #1382, #1383, #1385 |

**Drafter's reading:** every artefact claim in the READY reproduces except the "predicted trees" (D6). The open items are rulings (D1-D3) plus three text findings (D4, D5).

## 2. Doubts for the GATE to rule (the prompt carries all of them), most important first

- **D1 TENANT BOUND of the six-role bypass.** `appVisibleTo` admits ORG_ADMIN / ISSUER_ADMIN with no tenant comparison; the four handlers carry 0 tenant predicates (C2 INFO). An ORG_ADMIN of tenant B is held off tenant A's apps ONLY by oauth_apps FORCE RLS (039) + `seedTenantGuc`. Kintsugi measured "oauth_apps rls true, force true, 2 policies" on 2026-09-30 (quoted in #1383's migration 049 header; not re-measured). The PR's own "tenant bound" line is about the role lists (C6 N3). The probe's R1 is a MODEL. Major, residue, or a question for Wednesday?
- **D2 The six-role bypass is not scope-aware.** Gate 1 reads only the scopes in the REQUEST. So a tenant-level ORG_ADMIN / ISSUER_ADMIN may re-point redirectUris of, and rotate the secret of, a PLATFORM ADMIN's admin:write app (probe H1 records it). The ruling's "ORG_ADMIN PATCH in-tenant → 2xx" did not name admin-scoped apps. A consequence the ruling may not have considered: escalate as a question, not a silent NO GO.
- **D3 Legacy apps + token time.** Rows already holding refused scopes are not migrated. /authorize + /token mint any scope the row holds; only `*` grants nothing (KS-839). The probe's L1-L4 measure what a plain-user owner keeps: the scopes survive a PATCH, the real validateScopes mints `subjects:erase` + `admin:write`, and the owner can rotate the secret. So the sev-5 is closed for NEW registrations only. Named in NOT COVERED; is a live row count owed before Done?
- **D4 PR body omission.** The DELETE-of-a-missing-id 404 (was 200) is not stated, though the product comment says "stated in the PR body" (C5 T8). The body also names only `subjects:erase` of the six destructive scopes the brief asked it to list.
- **D5 Doc figures.** Both docs say "864 passed, 0 failed" and that the ks949 reds "did not recur", while the PR body at the SAME head reports run 1 at 862 / 864 with 2 ks949 timeouts (C4 D9). The docs' 17 \| 7, tsc control and 864 are E 2nd's, but they read as measured at this head. Two units carry undated durations (D8).
- **D6 READY contradictions.**
  - "predicted tree 299fd1c2de24 / 7904aab89f15" are `merge-tree`'s CONFLICTED toplevel trees, conflict markers in both docs (measured against Wednesday's `e3/vclone` objects and reproduced by `c4_predict_ex4.out` INFO). They are NOT resolutions; the kit's resolutions are `bded1f6b95d0` / `ad1b013939b2`.
  - "7,231 bytes" is the character count (7,275 bytes).
  - Two more open PRs overlap the docs and are not in the READY: #1383 (KS-1401, block 22.) and #1385 (KS-938, block 20., E 3rd's own row 2, raised after the READY).
- **D7 Drift-cell fragility.** E1 / E2 / E4 go red at develop by a THROWN Error, not an AssertionError. The drift cell reads the FIRST `const ADMIN_ROLES` in users.ts, which declares it four times; the :583 one is a DIFFERENT four-role list. That is positional, not by name. The test mocks AVAILABLE_SCOPES with a literal; ks855 pins the real list.
- **D8 Not measured by anyone.** PREFLIGHT-INCOMPLETE 12/15 (legs 3 / 4 / 8). The live sweep §5f is owed. tsc was not run by the author at this head. The gateway has no role gate. listApps(undefined) returns every app, reachable only through a userId-less principal.

**For Wednesday (not the gate's):**
- **W1 sequencing.** If #1381 and #1382 land as ruled, #1384's head becomes a docs-only merge-in. Launching gate60 BEFORE they land judges `852fc9276320`, and the merge-in is then covered only by `qm` + Q-M+. Launching AFTER they land refuses rc 10 (re-draft). Predicted chained tree: `552970edf014…` (if both land as their current trees).
- **W2 #1383 and #1385** were added to `reported_overlaps` by the drafter so the launch does not refuse rc 15 on a known fact. Neither is in Q-ORDER3 before #1384; rule their order.
- **W3** D1 / D2 may be questions for Kam via you (the ruling's scope), not the gate's to settle.

## 3. The kit's instruments (each exercised; outputs beside it as `<name>_exN.out/.err/.rc`)

| script | what it does | positive control | must-fail tamper arms (all fired) |
|---|---|---|---|
| `lib_gate60.py` | gate59's lib re-keyed: read-verb `git()`, scratch-only `wgit()`, `guard_out`, GH, `move_out` | — | `refusal_arms_ex1.out`: c3 worktree under the stand-in root, c3b `--out` under it, c4 `--repo` via a SYMLINK into it → rc 2 each, nothing created |
| `c1_pin_gate60.py` | P1-P9 | `c1_pr1384_ex1` rc 0; T0 | `c1_selftest_ex1` **12/12**: base-vs-base, 7th path, +/- drift, two parents, trailer, `(#1384)`, 93 chars, 2nd Refs, KS-855 hyphenated, develop moved, API head moved |
| `c2_hunk_gate60.py` | H1-H7 + class-hunt INFO | `c2_pr1384_ex3` rc 0; T0 | `c2_selftest_ex3` **10/10**: rotate ungated (H4), PATCH order swapped (H5), create gate on the SIX list (H5), ORG_ADMIN in the platform list (H3), update schema reopened (H2), services/oauth.ts edited (H1), an expect() removed (H7), owner test dropped (H6), **real develop as head (H4: 0 of 4 gated)**. `_ex1` = history (H1 count 43 from `git diff -U0` vs SequenceMatcher's 41; /revoke INFO over-read) |
| `c3_redfirst_gate60.py` | redfirst / siblings / suite / tsc / openapi | R-0, R-8, G-0, S-0, S-1 | `c3_selftest_ex2` **17/17**: loadfail, A5 red, C1 by timeout, green develop, A1 wrong status, E1 wrong throw, 23 cells, ks451 stays green (R3), ks431 red at develop (R4), unknown new red, ks1210 missing, ks949 blob changed |
| `c3b_probe_gate60.py` + `c3b_probe_ks1210_gate60.test.ts.txt` | the gate's own 23 cells at develop and head | D-0, H-0 | `c3b_selftest_ex1` **9/9**: O1 no flip, V2 red, loadfail, P1 by timeout, unmodelled SQL (B0), 22 cells, L1 red at head. The develop run IS the must-fail arm on real code |
| `c4_docs_gate60.py` | docs D1-D9, predict MP0-MP5, qm M0-M7 | `c4_predict_ex4` rc 0; T0 / Q0 | `c4_selftest_ex3` **13/13**: 2nd block edited (D3), 18→17 (D4), block duplicated, cheat h2 numbered (D6a), live sweep removed (D7); Q-M on SIM develop2: extra oauth.ts edit (M1 + M3), 18 below 19 (M1), single parent (M2), trailer (M4), develop through oauth.ts (M7). Real control `c4_qm_basevsbase_ex1` rc 1. `_ex1`/`_ex2` = history (the READY's trees mistaken for resolutions; `404s` read as a duration; M7 assumed 2 declarations) |
| `c5_prtext_gate60.py` | T1-T8 | T0 baseline-aware; T8c control | `c5_selftest_ex1` **9/9**: Refs removed, `Closes`, KS-855 hyphenated, `(#1384)`, "Run by me" removed, head sha altered, webhooks:manage ruling removed |
| `c6_notcovered_gate60.py` | N1-N3 section-bounded | T0 baseline-aware; T5c control | `c6_selftest_ex2` **6/6**: live sweep removed, gateway line above the heading, heading removed, 2nd heading. `_ex1` = history (N3 read the whole section, not the item) |
| `gh_census_gate60.py` | API line + census (focus: routes/oauth.ts, services/oauth.ts) | `census_ex3` (control FIRES on #1384) | `census_selftest_ex1` **6/6**. `census_ex1/2` = history (#1383, then #1385, unreported until added) |
| `fill_gate60.py` | fills prompt + launcher + pins (33 keywords) | the dry fill | changed READY / moved develop / moved head → rc 1 |
| `launcher_gate60.TEMPLATE.sh.txt` | gate59's launcher re-keyed (compare ahead 1 / behind 0 / 6 files) | SIM `--check` rc 0 (`dry_console_ex1.out`) | `launcher_arms_ex1.out`: stale pin 9, develop moved 17, head moved 6, no TTY 21 (never reached `exec claude`) |
| `repin_and_launch_gate60.sh` | the launch action | `--dry-run` rc 0 | `launcher_arms_ex1.out`: short sha 9, wrong PR 9; fill with a moved develop rc 1 |

All `*.SIM.*` and `pins_gate60.SIM-*.json` files are exercise output and never launched. The real `pins_gate60.json` does not exist until the real launch writes it.

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1210-1384|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. Not adapted / not measured
- No suite, no tsc, no openapi, no probe, no preflight was run by the drafter. Every C3 / C3b expectation is derived from source, and the probe from a syntax check.
- No real Postgres or stack: RLS, the tenant GUC, the BYPASSRLS question and the live sweep are all NOT TESTED. R1 is a model.
- `qm` has run only on SIM merge-ins; no real merge-in of #1384 exists yet.
- The c6 seed-list match is a KEYWORD HEURISTIC, labelled as such.

## 6. Re-draft recipe (the head or develop moved)
1. Re-fetch into a scratch clone.
2. Re-measure kit `head`, `end_tree`, `develop`, `develop_tree`, `files` (+/-), `blobs`, `flow_numbers_*`, `block_lines`, `pr_body_read`, `reported_overlaps` (re-run `gh_census_gate60.py --json`), and `seat_ready_sha256` if a new READY is the input.
3. A merge-in head changes C1 P3: two parents [852fc9276320, new develop]. Judge it with `c4 qm`, or rewrite P3 to the gate57 / gate59 merge-in shape.
4. Re-run every `--selftest`, then `c1`, `c2`, `c4 predict`, and a `--dry-run`.

## 7. How Wednesday launches it (after section 4's routing line)
The pane is `QA/Secuura-ks1210-1384`. The report dir is `…/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1210-1384-g60/`. The GO the gate expects is `GO (Seat E 3rd): merge 1384 on gate60`. The verdict subject is kit `verdict_subject_template`.

Exit codes:
- rc 1: routing.
- rc 9: input.
- rc 11: the head moved, or is not the kit head.
- rc 10: develop moved (#1381 / #1382 landed → RE-DRAFT), or the fill refused.
- rc 15: an unreported overlap, or a reported overlap's head moved (#1381 / #1382 / #1383 / #1385).
- rc 12 / 13 / 14 / 16: usage gate / `--check` / cockpit / override.

Add `WED_USAGE_STOP=…` only with Kam's recorded authority.
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate60/repin_and_launch_gate60.sh 1384 852fc927632095fb603583cb543050d5edd66111 --dry-run
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate60/repin_and_launch_gate60.sh 1384 852fc927632095fb603583cb543050d5edd66111
```
