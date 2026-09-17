# QA GATE BRIEF — Secuura/Blockchain PR #1021 (KS-1211, row 6 of the audit-baseline fix work, GHSA-2wm5-q62r-hmrv colord 2.9.3 → 2.10.0 in two systemTest harness locks, Seat B) — TIER X (through code), ROUND 1

**Charter — read first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Drafted 2026-09-17 17:46–18:0x AEST (from `date`) by a Wednesday drafting subagent. Every fact carries its instrument inline. **"The seat" or "the READY" means relayed, not re-derived: an input to falsify.** "Drafter-measured" means the drafter read or ran it: read-only `git` on the Secuura checkout, GitHub REST GETs, Linear GraphQL queries, or scripts in the drafter's OWN `git clone --shared`. It is still yours to re-derive. Drafter scripts and outputs: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1021/` (below: `GS/`), raw runs under `GS/out/`. The READY mail, verbatim, spf/dkim/dmarc pass: `GS/mail_1021_ready.md` — its NOT COVERED list is quoted under THE SEAT'S CLAIMS.

**Method lessons, binding:**
1. **rc 0 is not a moved pin; only the parse is evidence.** Diff the parsed `packages` maps, not the text, and plant a change to prove the differ can see one.
2. **A zero needs a control that can fail on the same instrument.** `audit-gate.mjs` is blind to colord BY CONSTRUCTION (colord is `scope: standalone-locks`, reported only by `audit-locks.mjs`), so an audit-gate rc 0 proves nothing about this row unless you also show audit-gate reds when a row it CAN see is removed.
3. **Compare versions with semver, never as strings.** `'2.10.0' < '2.9.4'` is TRUE as strings (drafter-measured). Use the `semver` that `scripts/audit` ships.
4. **A dependency that is installed is not a dependency that is loaded.** Prove whether the harness run actually imports colord, with a positive control on the same trace.
5. Node 24 `node --test`/vitest print human reporters when not a TTY: read the `Tests N passed (N)` / `ℹ pass` lines, never a TAP `# tests` parse.
6. Re-read Linear's `attachments.metadata.linkKind` immediately before the mail.

## WHY TIER X, AND HOW MUCH

- **Tier 2, as Wednesday's receipt set it** (`GS/receipt_1021.md`): dev-only harness locks plus one security-gate baseline row, checked through code. A wrong removal re-breaks preflight leg 7 for every Blockchain/Dev push; a wrong pin leaves the advisory live under a deleted acceptance.
- **Budget: proportionate. Three files, +6 −14, no manifest, no source. Time-box 30 minutes.** Priority if time runs short: item 1 → item 2 → item 3 → item 5 (linkKind/merged tree) → item 4 → item 6. Report anything not reached as **NOT RUN, with the blocker named**.
- **NOT REQUIRED, said before running:** docker or any stack; preflight.sh whole (the three changed bytes reach legs 2, 6 and 7 only, and you run those commands directly); Schemathesis, Akto scans, Playwright, k6; any service or `packages/*` suite (no workspace byte moved); the Playwright, Performance and Schemathesis `quality` gates (their trees are byte-identical). List each under NOT TESTED as *not-applicable (why)*.

## TARGET

**Repo READ-ONLY:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. Clone by SHA into your OWN fresh `mktemp -d` (`git clone --shared --no-checkout`), add detached worktrees there, run every write verb there from a script file. Never enter Seat B's worktrees (`worktrees/raise-0917-b-audit*`), Seat A's, or any other gate's clone. 🔴 **NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout or any of its worktrees.**

**A PR is gated at a SHA. Your first act is to verify the head at origin:** `git ls-remote origin refs/heads/feature/ks-1211-bump-colord refs/pull/1021/head`, plus the PR API's `head.sha`. If it differs, STOP, mail the moved head, gate nothing.

| | PR #1021 |
|---|---|
| ticket | KS-1211 (In Progress), "Seven audit-baseline rows (hono x3, js-yaml, vitest, baseline-browser-mapping, colord)…". Body "Refs KS-1211" ×1, 0 closing phrases; title, commit message and the one `linear[bot]` comment 0 as well (regex with planted controls `Fixes KS-1211`, `closes #12` hit and `Refs KS-1211` does not; `GS/api_read.out` 17:48:46) |
| branch | `feature/ks-1211-bump-colord`, author `kksecura` |
| head | **`742e1c6080f2527973268146611930e4a70edef2`** (ls-remote 17:46:03 and 17:57:02; PR API 17:48:46), tree `6cf9a150b` |
| parent = merge-base | `f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed` (tree `4d406fb1c`). Compare `develop...head` 17:48:46: ahead 1, behind 0, files 3 |
| **develop moved** | **origin develop = `581c9db0db4201c42cbbf702f339b750989acdb1` from ≤17:54:41** — #1019 (KS-1187, Seat A) squashed on `f8c7aaa39`, 3 files, all `Blockchain/Dev/services/api-gateway/` (`routes/proxy.ts` + two tests). 0 files shared with #1021 |
| files | `Blockchain/Dev/scripts/audit/audit-baseline.json` `03d1680e3` → `c73fcebed` (+0 −8); `systemTest/akto/package-lock.json` `6b348adcc` → `c4d30077f` (+3 −3); `systemTest/api-explorer/package-lock.json` `8be03ee9c` → `78589de7e` (+3 −3). PR API and `git diff --numstat` agree; `-w` numstat identical |
| reviews / comments | 0 / 1 (`linear[bot]`). `mergeable_state` unstable. **GitHub Actions is retired for this repo** (workflow header, Kam 2026-08-27): all 6 runs on the head ended `failure`, 1 `skipped` (`GS/checks_read2.out`) — **there is no CI signal; your local run is the only one** |

## LEGITIMATE SHAPES

| shape — the real event | expected verdict | the clause that yields it | predicted-by |
|---|---|---|---|
| head locks + head baseline (37 rows) | audit-locks rc 0 OK, 0 CLEANUP; audit-gate rc 0 | 2.10.0 not in `<2.9.4`; the row is gone | seat, drafter |
| head locks + develop baseline (38 rows) | audit-locks rc 0 with `CLEANUP — 1 … GHSA-2wm5-q62r-hmrv (KS-1024)` | `audit-locks.mjs:299` stale `scope: standalone-locks` rows | seat, drafter |
| base locks (2.9.3) + baseline without the row | audit-locks **rc 1**, exactly GHSA-2wm5, pinned 2.9.3, 2 locks | `semverSatisfies('2.9.3', '<2.9.4')` | seat, drafter |
| audit-gate with the colord row removed, any tree | rc 0 — **blind by construction** | root `npm audit` never sees systemTest locks; `audit-gate.mjs:204` skips `standalone-locks` rows | drafter |
| a harness lock whose colord is outside stylelint's `^2.9.3` | clean-room FAIL | `npm ci --dry-run` checks declarer ranges | drafter (planted) |
| a harness lock whose colord `integrity` is garbage | clean-room **OK** (dry-run fetches no tarball); a real `npm ci` must FAIL | dry-run semantics | drafter measured the first half only |

## THE SEAT'S CLAIMS (from the READY and PR body; inputs to falsify)

1. colord 2.9.3 → 2.10.0 in both harness locks, "inside stylelint's `^2.9.3`", written by `npm update colord --package-lock-only --ignore-scripts --no-workspaces` in `node:24-alpine` (npm 11.19.0), one member per container; akto mounted with repo-root `observability/`. No manifest.
2. Parsed diff: 1 entry moved per lock, 0 others, entry counts 423 / 361 unchanged, no `packages[""]` drift.
3. Baseline 38 → 37, 0 added, 0 altered, `$comment` unchanged; round-trips byte-identically through `json.dumps(indent=2, ensure_ascii=False)`.
4. Gates: fix run audit-locks rc 0, audit-gate rc 0 with 0 CLEANUP; control (develop baseline) audit-locks rc 0 listing the row under CLEANUP; negative control (develop locks, row removed) audit-locks rc 1 exactly GHSA-2wm5, 2.9.3 in 2 locks.
5. `lockfile-cleanroom.sh ../../systemTest/{akto,api-explorer}`, host node-24 route: 2/2 OK. `npm test -w packages/shared` 851/851. In-hook preflight INCOMPLETE 12/15 (3, 4, 8 skipped), nothing failed; the KS-989 systemTest format gate SKIPped (deps not installed).
6. Advisory "medium; fixed in 2.9.4" (PR body cites the GitHub advisory DB).
7. attachmentsForURL(pull/1021) = KS-1211 contributes; 0 closing phrases; 0 open PRs touch the three files; KS-1211 Backlog → In Progress by the GitHub bot 07:43:03Z.
8. **NOT COVERED, verbatim from the READY:** *"The akto and api-explorer harnesses' own unit suites, and stylelint, colord's only declarer. Their node_modules are not installed; verification is by parse + clean-room only."* · *"Preflight legs 3, 4 and 8, and all four platform suites (no stack, per the hold)."* · *"No image built. colord is dev-only in both harness trees."*

## DRAFTER-MEASURED INPUTS (re-derive them; a wrong one is Wednesday's error, so report it as one)

Substrate: clone `--shared`, detached worktrees base `f8c7aaa39` and head `742e1c608` (`GS/out/setup.out`); `scripts/audit` `npm ci --ignore-scripts` rc 0 in each; node v24.7.0, npm 11.5.1; porcelain 0 on both worktrees after every probe. Secuura checkout at 17:46:03: porcelain 0, `.git/config` sha256 `d7e7298b02c45f52…`, refs 922, `.git/worktrees` entries 112 (refs move as seats fetch).

- **D1 Scope (`GS/out/parse_probe.py` → `.out`, 17:47:21).** Per lock, the `packages` map: akto 423 = 423 entries, api-explorer 361 = 361; exactly 1 key changed each, `node_modules/colord`, fields `version`, `resolved`, `integrity` only, `dev: true` both sides. `packages[""]` identical; every non-`packages` top-level key identical. Control: a planted version change in another entry is detected (changed count 2). Baseline (`accepted` map): 38 → 37, removed exactly `GHSA-2wm5-q62r-hmrv`, 0 added, 0 altered, survivor order identical, non-row keys identical; control: a planted expiry change is detected. Standalone-locks rows: base `GHSA-q8mj-m7cp-5q26` + `GHSA-2wm5`, head `GHSA-q8mj` only. Rows expiring ≤ 2026-09-30: 15 → 14. The seat's byte round-trip claim (3) was NOT re-run by the drafter.
- **D2 Gates (`GS/out/audit_runs.sh` → `.out`, 17:54:35–17:54:47, live registry):**

  | run | tree | baseline | result |
  |---|---|---|---|
  | L1 | head | head (37) | audit-locks **rc 0** "43 standalone lockfiles (45 − 1 − 1)", OK, 0 CLEANUP |
  | L2 | head | develop (38) | rc 0, OK, `CLEANUP — 1 … GHSA-2wm5-q62r-hmrv (KS-1024)` |
  | L3 | base | develop (38) | rc 0, OK |
  | L4a/L4b | base | 37, colord row removed | **rc 1** ×2, "FAIL — 1 advisory … GHSA-2wm5-q62r-hmrv [moderate] colord … pinned: 2.9.3 … in 2 lock(s): ../../systemTest/akto, ../../systemTest/api-explorer" |
  | L5 | head | 37, the OTHER standalone row `q8mj` removed | rc 1, exactly `GHSA-q8mj-m7cp-5q26` (qs, 26 locks), plus CLEANUP GHSA-2wm5 (second negative control: the scan still sees standalone rows at head) |
  | G1 / G2 | head / base | real | audit-gate rc 0, "36 reported, 37 baselined" / "36 reported, 38 baselined", 0 CLEANUP lines |
  | G3 | base | 37, colord removed | audit-gate **rc 0** — blind to colord, as predicted |
  | G4 | head | 36, js-yaml `GHSA-2883-xcg3-v3hh` removed | audit-gate **rc 1**, "1 NEW advisory … GHSA-2883" — the control that audit-gate can red (`GS/out/gate_ctrl.out`) |

  L4 was run twice because the removed row's own reason records the scan reporting colord, then not, on an unchanged tree (KS-1025); both runs agreed today. **The CLEANUP behaviour is as the code says:** audit-locks prints CLEANUP only for a `standalone-locks` row the scan no longer matches (L2), and audit-gate never prints one for such a row (G1–G3).
- **D3 Advisory range, from the gate's own fetch (`GS/out/tee_fetch.mjs` preload, which tees the bulk-advisory responses `audit-locks.mjs` receives, unchanged).** At base the request carries `colord: ["2.9.3"]` and the response is `GHSA-2wm5-q62r-hmrv`, severity `moderate`, **`vulnerable_versions: "<2.9.4"`**, CWE-1333. At head the request carries `["2.10.0"]` and the response has no colord key. No extra URL. Shipped `semver` 7.8.5 (`GS/out/semver_probe.mjs`): `satisfies('2.10.0','<2.9.4')` false; controls `2.9.3` true, `2.9.4` false; `satisfies('2.10.0','^2.9.3')` true; controls `3.0.0` false, `2.9.2` false. Lexical trap `'2.10.0' < '2.9.4'` = true. Declarer, parsed from both head locks: `node_modules/stylelint` 17.14.1 (`dev: true`) `dependencies.colord = "^2.9.3"`, the ONLY declarer; each harness root declares `stylelint ^17.14.1` in devDependencies. Severity: the gate's feed says `moderate`, the PR body says `medium` (GitHub DB's word for the same level) — RECORD, not a finding.
- **D4 Clean-room sufficiency (`GS/out/harness_probe.sh` → `.out`, 17:48–17:55).**
  - `lockfile-cleanroom.sh ../../systemTest/akto ../../systemTest/api-explorer` (host route, node 24): head 2/2 OK, base 2/2 OK. Its default corpus is `services packages frontend scripts` only (`lockfile-cleanroom.sh:46`), so leg 2 and `pr-lockfiles.yml` never check these two locks — explicit dirs are the only way.
  - Controls on the head api-explorer lock, sha-restored (`ecc4d1180d65623b` before and after): **C1** bogus colord `integrity` → clean-room **rc 0 OK** (dry-run does not verify the tarball). **C2** `stylelint.dependencies.colord` planted `^3.0.0` → **rc 1 FAIL** (it does check declarer ranges). **C3** manifest `stylelint ^99.0.0` → `npm ci --dry-run` hung >5 min; the drafter SIGTERMed it by verified pid, so its rc 1 is the kill, **not a control result**.
  - So the clean-room is **not sufficient alone**: it proves lock ↔ declared-range consistency, not that the pinned tarball exists and matches its integrity. A real install does.
  - **Real install, head and base, each harness (`npm ci --ignore-scripts --no-audit --no-fund`):** all 4 rc 0, lock sha unchanged by the install; installed colord 2.10.0 (head) / 2.9.3 (base); `npm ls colord` = `stylelint@17.14.1 └── colord@<ver>`; `colord('#ff0000').toHsl()` = `{h:0,s:100,l:50,a:1}` on both.
  - **`npm run quality` (format:check → lint incl. tsc + eslint + stylelint → knip → test:unit → `npm audit --omit=dev --audit-level=high`):** head akto rc 0, 69 files / **1233 passed (1233)**; head api-explorer rc 0, 17 / **58 passed (58)**; base: the same counts, rc 0; `found 0 vulnerabilities` on all four. **The READY's NOT COVERED gap is closable in about 3 minutes, and the drafter measured it green.**
- **D5 Is colord ever loaded? (`GS/out/trace_colord.mjs`, a `module.registerHooks` resolve logger).** Running each harness's own `stylelint "src/**/*.css"` (1 css file each): **0 colord resolutions**; positive control on the same trace: 1151 (akto) / 1154 (api-explorer) `node_modules/stylelint/` resolutions. colord is imported only by stylelint's `color-named` rule (`lib/rules/color-named/{index,colordUtils}.mjs`), which the harness configs do not enable. Forced: a scratch config `{"rules":{"color-named":"never"}}` on a planted `a { color: red; }` → 5 colord module resolutions, `Disallowed named color "red"`, stylelint rc 2, on 2.10.0 AND on 2.9.3; the clean file rc 0 on both (`GS/out/cn/color_named.out`). **So in the shipped harness configuration the bump is inert, and where colord IS loaded, 2.10.0 behaves as 2.9.3 on this probe.**
- **D6 Reach.** Across all 45 tracked locks at head, `node_modules/colord` appears in exactly 2 (the two harness locks), both `dev: true`; control: `express` entries 30. 0 hits for `colord` in any tracked `package.json`, Dockerfile or workflow yml. Where the harness trees ARE installed: `pr-platform-suites.yml:515` runs a full `npm ci` in `systemTest/akto` (dev deps included) — a CI runner, not an image — and Actions is retired. api-explorer appears in no workflow. **Not measured by the drafter:** a byte search inside any built image (none built; by design).
- **D7 Linear and GitHub (`GS/api_read.out` 17:48:46–17:49:03).** `attachmentsForURL(pull/1021)` = 1, on KS-1211 [In Progress], `linkKind='contributes'`, status open; control pull/99999 = 0. KS-1211 `completedAt` null, one attachment (#1021), comments `0ec33ad8` (07:21:14Z, the rows' BLUF) and `996f401f` (07:43:25Z, names #1021 as 1 of the ticket's 7 rows); history Backlog → In Progress 07:43:03.840Z by GitHub. 21 open PRs: 0 of the 20 others share a file with #1021 (7 touch other lockfiles; none touches `scripts/audit/`, preflight, or either harness).
- **D8 Merged tree (`GS/out/merged.sh` → `.out`, 17:54:41, own clone).** `merge-tree --write-tree 581c9db0d 742e1c608` = **`207ba797c`** (clean). It differs from the head tree `6cf9a150b` by exactly #1019's 3 api-gateway files, and from develop's tree by exactly the 3 PR files, each at the PR's own blob. Control: develop merged with itself = develop's tree `99df1503e`. **Prediction: every count above is identical on the merged tree**; the drafter did not re-run the gates there.
- **D9 The project's own harness rule (`systemTest/CLAUDE.md:449–470` (rule 2 at :465), blob `357015b94`, READ).** *"The PR CI runs a quality gate for Playwright only (KS-399); the other three suites run none."* Rule 1: *"After changing any file in a systemTest project, run that package's `quality` gate and make it pass before committing."* Rule 2: *"Creating OR updating a systemTest PR → run ALL FOUR full gates."* Also `systemTest/CLAUDE.md:824` "Upgrading a tool or dependency (MUST)". The READY says the harness suites and stylelint were not run.

## WHERE THE READY DISAGREES WITH THE DRAFTER (weigh; do not assume either side)

1. **"Verification is by parse + clean-room only."** D4 measured that the clean-room passes a lock with a garbage integrity (C1). The parse plus clean-room therefore cannot tell a correct 2.10.0 pin from a wrong tarball hash; only a real install can, and the drafter's real install passed. PREDICTION: the gap is **real as evidence, empty as a defect**. Rule it.
2. **The harness `quality` gate is a written MUST at source (D9), and the READY lists it as NOT COVERED.** The drafter measured it green at head and base (D4). PREDICTION: a **Minor process FINDING against the PR's evidence** (target: the seat's Test Evidence, not the bytes), cured by your own re-run; not a NO GO. Whether the lock-only nature of the change exempts it is for you to rule, citing the rule text. The "all four" sweep (rule 2) over Playwright, Performance and Schemathesis is NOT measured by anyone; their bytes are identical base/head.
3. **"colord's only declarer" is right, and "the harness suites exercise colord" would be wrong:** D5 measured 0 colord loads in the harness's own stylelint run. PREDICTION: RECORD — the unit suites and stylelint cannot red on this bump at the current config, which also bounds what a green run proves.
4. **develop moved after the READY** (#1019). PREDICTION: merged == develop + the 3 files, no interaction; re-derive on the merged tree.

## WHAT THIS GATE MUST ESTABLISH (minimum set)

1. **Scope control, both locks and the baseline.** Parse each lock at base and head: exactly one `packages` entry changes (`node_modules/colord`: `version`, `resolved`, `integrity` only; `dev` unchanged), 0 others, `packages[""]` and every non-`packages` key identical, entry counts equal — each with a planted-change control. Baseline: 37 rows, only `GHSA-2wm5-q62r-hmrv` removed, 0 added, 0 altered, with a planted-alteration control. Check the seat's byte round-trip claim (3). `git diff -w` equals the plain diff; 1 commit, 3 files.
2. **The advisory is gone, through the shipped gates.** On the head tree: `node scripts/audit/audit-locks.mjs` and `audit-gate.mjs` (from `Blockchain/Dev`) rc 0. Control: head with the develop baseline → audit-locks rc 0 with the one CLEANUP line naming GHSA-2wm5. Negative control: base with the row removed (`AUDIT_BASELINE_PATH` to a scratch copy) → audit-locks rc 1 naming **exactly** GHSA-2wm5, 2.9.3, 2 locks; run it twice (KS-1025). Show audit-gate is blind to this row (rc 0 at base without it) AND can red on a row it sees (remove a root-reported row, e.g. `GHSA-2883-xcg3-v3hh`, → rc 1). State the CLEANUP behaviour for `scope: standalone-locks` in both scripts, by line.
3. **Is 2.10.0 fixed and in range, and is the evidence enough?** Read `vulnerable_versions` from the bulk-advisory response the shipped `audit-locks.mjs` receives (tee it inside the process; no extra URL), and evaluate it with the shipped `semver`, with controls on both sides of the boundary. Read stylelint's declared colord range from both locks and evaluate `2.10.0` against it, with an out-of-range control. Then rule the READY's gap: run `lockfile-cleanroom.sh` on both harness dirs with **one planted control that must FAIL** and one that shows what it cannot see (e.g. bad integrity); then a **real `npm ci --ignore-scripts`** per harness at head (lock sha unchanged after), `npm ls colord`, and each harness's `npm run quality` at head, with base as the control. Say whether colord is actually loaded during the harness lint (trace it, with a positive control), and whether the clean-room alone would have been sufficient. Rule the systemTest/CLAUDE.md MUST (D9) as FINDING or RECORD.
4. **Reach.** colord across every tracked lock at head (count, `dev` flag, with a positive control), in any `package.json`, Dockerfile or workflow; which CI jobs install either harness tree and whether they run today. Confirm it reaches no service, frontend, package or image.
5. **linkKind, merged tree, overlap.** `attachmentsForURL(pull/1021)` exactly KS-1211 `contributes`, `completedAt` null; control pull/99999 = 0. Closing phrases in title, body, commit message and every comment = 0 (planted controls). Merge head onto the THEN-CURRENT develop in your own clone: name the tree, the develop delta, and re-run item 1's parse and item 2's four gate runs on the merged tree (or show tree/blob identity for every input and say why a re-run is redundant). File overlap of #1021 with every other open PR via the PR files API, including any PR touching `audit-baseline.json` (Seat B's next row PRs will — name any now open).
6. **§5f and ticket state.** `.claude/skills/secuura-test-discipline/SKILL.md:526` at develop: *"A runtime-behaviour change is not done — and the ticket does not move to Done — on offline quality-gate green alone."* Rule whether a dev-only harness bump is a runtime-behaviour change (drafter's prediction: NO — no image, no service, colord not loaded by the harness config). State plainly: KS-1211 stays **In Progress** after the merge (it carries 6 more rows: hono ×3, js-yaml, vitest/@vitest/mocker, baseline-browser-mapping), and **no ticket moves to Done** on #1021.

## BOUNDS

- **Network:** no docker, stack, kintsugi or demo. No `az`. Never the wallet mnemonic. Outbound network is only: `npm ci` in `scripts/audit` and the two harness trees, what the audit scripts do themselves (`npm audit`, the registry bulk-advisory POST), the harness `quality` gate's own `npm audit`, plus GitHub and Linear GETs.
- **Credentials:** GH_TOKEN and LINEAR_API_KEY are read by NAME inside a script from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env`. Never echo them. GET and queries only. The token cannot read check-runs (403, drafter); `/actions/runs?head_sha=` works.
- **Scratch hygiene:** never `rm` (fresh `mktemp -d` per attempt; quarantine by rename); never `cd` in your tool calls (`env -C <dir>` or script files); no write-verb git from the tool line; `/usr/bin/grep -i` with a same-file positive control; zsh has no PIPESTATUS (`rc=$?` on its own line); never begin a line with `====`. **`timeout` is not installed on this host**: a hung `npm` must be ended by verified pid (drafter's C3).
- **Checkout readings:** quote the Secuura checkout's porcelain count, `.git/config` sha256, for-each-ref count and `.git/worktrees` entry count at start and at close.

## REPORT

Write to `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1021-742e1c608-tier2-r1/` (`report.md`, `evidence/`). Include FOUND / TESTED / HOW with controls; the parse table per lock; the gate-run table (tree, baseline, rc, lines); the advisory/semver table; the clean-room control table and the real-install + quality counts per tree; the colord load trace; the reach census; seat-claim dispositions; **NOT TESTED at the same prominence as findings.** Every finding carries evidence class, severity, target (PR, seat evidence, or TICKET) and oracle.

## VERDICT DESTINATION

ONE mail to `wednesday-agent@agentmail.to`, subject EXACTLY:
`[QA -> Wednesday] TIER X GATE #1021 (KS-1211) 742e1c608 — <GO | GO WITH FINDINGS | NO GO>`

The body holds:
1. the report's BLUF;
2. plain statements on items 1–6;
3. the merge ADDENDUM: "squash `742e1c608` onto develop `<then-current SHA>` (file-disjoint from every open PR); #1021 attaches to KS-1211 only, linkKind contributes; KS-1211 stays In Progress (6 rows remain; Refs, never Closes; no ticket to Done under §5f); equality targets `audit-baseline.json` blob `c73fcebed` (37 rows), `systemTest/akto/package-lock.json` `c4d30077f`, `systemTest/api-explorer/package-lock.json` `78589de7e`; audit-locks rc 0 with 43 scanned and 0 CLEANUP (re-measure); Records: <yours>";
4. the NOT TESTED block and the report path.

**Mechanism note.** The QA project has no `send_brief.sh` of its own. Verdict mails reach Wednesday from `coagent@agentmail.to` via the AgentMail API:
- `POST https://api.agentmail.to/v0/inboxes/coagent@agentmail.to/messages/send`
- JSON body `{"to": ["wednesday-agent@agentmail.to"], "subject": "...", "text": "..."}`
- header `Authorization: Bearer $AGENTMAIL_API_KEY`, the key read by NAME by your script from `/Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env`, never echoed.

**The MAIL is the END STATE.** Confirm the API answered 2xx and quote the message id in your final pane line. Timestamps come from `date`, never estimated.

## NOT COMMISSIONED

- **Any fix:** editing a lock, the baseline, a harness config or the PR body; re-dating any row. Those belong to Seat B and to Kam.
- **The other 14 lapsing rows** and their PRs (hono is Seat B's next); the KS-1025 gate reshape; Akto/Playwright/k6/Schemathesis runs; any deployed environment; messages to anyone but Wednesday (nothing to Peter or Stuart).
