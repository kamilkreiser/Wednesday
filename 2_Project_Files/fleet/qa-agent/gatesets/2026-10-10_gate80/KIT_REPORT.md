# gate80 KIT REPORT — kit builder to Wednesday

- **Target (one batch, tier 2, round 1):** #1441 (KS-1345, Seat G 6th) and #1442 (KS-998, Seat F 7th). Both have ONE parent, `613070f29112a40a0d8d9684cd50c7c2ae54592c`, which is also origin develop at build time.
  - #1441: head `7685e79af2c437b1e6cc8fe2e57b1b0771f576d5`, tree `4c5002a04c8c`, 4 paths +93/-7, branch `feature/ks-1345-webhooks-deliveries-failed-query-500-g6-1`.
  - #1442: head `a7ec5746cb8b43313d55d73185ada4931b17c5be`, tree `f400aabef2c3`, 4 paths +133/-1, branch `feature/ks-998-format-gate-npm-stdin-isolated-f7-1`, one `create mode 100644` (the new suite).
- **Built from:** the gate79 kit shape, and the reviewed draft `briefs_staged/2026-10-10_gate80_T2_1441_1442_DRAFT.md` (sha256/16 `17e96226f04b3eec`). Wednesday's four rulings are in `RULINGS_wednesday.md`.
- **Built and dry-run only. NOT launched.** No pane, no `cockpit.sh add`, no usage gate, no mail, no comment, no ticket move, no push. `inbox_routing.conf` is untouched (exact `gate80` line count 0, control: 179 agentmail lines). No `launch_<HHMMSS>.*` file exists in the kit.
- **Where I wrote:** only this folder. `_scratch/` (gitignored, **2.8 GB**: the kit clone, the #1441 worktree with `npm ci`, extracted trees with the 4 `systemTest` installs, raw Actions job logs) is NOT deleted (never `rm`); move it to a quarantine when you are done. `_quarantine/` holds five superseded runs, each named for why. Nothing under `!CODING` was created.
- **The Secuura checkout:** only read verbs were run against it (`ls-remote` via its own `core.sshCommand`, `config --get`, `log`, `show`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `archive`, `merge-base`, `status`, and `clone --shared`, which reads). No fetch, pull, checkout, worktree or commit there. Every `fetch` / `worktree add` / SIM commit went into the kit's OWN clone `_scratch/clone` (its `worktree add` for #1441 is registered in that clone, not in the checkout). Gate79's scripts contain no write verb against the shared checkout, so nothing was refused or dropped for that reason. (The checkout's `.git` shows recent object writes; the checkout's `.git/config` mtime 06:03:33 AEDT predates my first command, and other seats are active there. I cannot prove a negative beyond "I ran only read verbs".)

## 0. Bottom line

- **Dry run rc 0**, final run `dry_run_console_final.txt` (2026-10-09T19:47:48Z–19:48:38Z UTC), run AFTER every arm. It read origin by `ls-remote` inside the run: develop `613070f29112` UNMOVED, both pull/heads == both branches == the pins.
- **Refusal arms: 132/132 MATCH** (red 42/42, repin 40/40, launcher 50/50), each with a PLANTED wrong head, base, tree, develop, seat, prompt string or pin. Self-tests: c1 32/32, c2 20/20, c3 24/24, gh 23/23.
- **The run instruments were run for real**, not just self-tested (section 3). Several caught real bugs in my first drafts, which are quarantined (section 7).
- **Not made to work / not done:** see section 8. Nothing is claimed that was not run.

## 1. Files

| File | What it does | sha256/12 (pinned) |
|---|---|---|
| `kit.json` | the pins (both PRs: head, branch, tree, parent, numstat, subject, READY path), base, known docs overlap, 36 tooling paths, Actions needles, `script_sha256` of the 9 pinned files. Not itself pinned | — |
| `lib_gate80.py` | read-verb-only `git()` (+ `archive`), `wgit` that refuses `!CODING`, `extract` (git archive to a non-`!CODING` dir), `req` (every pin a REQUIRED arg), `PR(n)` (refuses a foreign PR), `span`, `code_only`, GH/Linear readers (tokens by name, never printed), `Tally` | `4e41ada4e127` |
| `c1_pin_gate80.py` | C1 per PR (`--pr`): P1 pull/head == branch == head, P2 one parent == base, P2b develop descends, P3 exactly 4 paths with numstat, P4 END_TREE, P5 0 trailers (control 53 B), P6 0 Co-Authored-By (control), P7 subject == kit, <= 92 as declared, no `(#`, P8 own key only, P9 modes + `create mode` list, P10 NO-NEW-LEG (36 paths at base/head/develop), P11 0 manifests/locks, P12 base..develop overlap ⊆ the two docs. `pair`: P13 the two PRs share exactly the two docs and no code path | `69c65877c296` |
| `c2_code_gate80.py` | `claims --pr`. #1441: W0 CODE-ONLY multiset diff of `webhooks.ts`, W1 `.catch(() => [])` 2 -> 1 with the survivor inside `dispatchEvent` and a planted control, W2 handler ORDER, W3 bound tagged template + 0 Unsafe, W4 outer catch + `fail500` identical, response constant, W5 `UUID_PATTERN` + the sibling helper identical, W6 regex PREDICTION table for 8 ids, W7 test titles base -> head. #1442: S0 CODE-ONLY diff, S1/S2 `< /dev/null` position, S3 loop-feed lines + `case` block, S4 stdin-consumer census of the `while read` loop (with a planted-`cat` control), S5 suite mode. Both: D1 each doc change is a pure insertion (control: an altered base byte fails) | `939c141e4147` |
| `c3_cells_gate80.py` | the RUN instruments: `setup1441`, `cells1441` (plants by content, asserts LANDED, restores by sha), `suite1441`, `tsc1441`, `probe32`, `tamper1441` (HEAD row, CONTROL no-op row, T1–T6), `suite1442` (4 ways + siblings + `--list` counts), `realpkg [--install]`, `hookpath`, `tamper1442` (U1–U5, process-group timeout), `docs` (both orders, KEEP-BOTH, `html_docs_matrix` on 5 trees) | `35443cde6cd9` |
| `probe_block_gate80.ts.txt` | appended to a COPY of the head's ks1341c test, in the gate's worktree, then moved out: sends 9 ids (UUID, UPPER, 32-hex no hyphens, wrong-place hyphens, 36-char non-hex, `0`, garbage, id-format-fail, 129 chars) and records status / body / db calls / bound value; plus P-ORDER and P-REJECT. Facts only | `d18701a1d162` |
| `gh_gate80.py` | `api`, `actions` (classified BY WORKFLOW PATH, log read without the auth header, KS-1148 `semver` evidence counters, a change needle counts only where the head EXCEEDS the matched comparator), `audit` (line 50 of `audit-locks.mjs`, with a CONTROL), `census` (OVERLAP-CODE / OVERLAP-DOCS / other + a WATCH list), `prtext` (T1–T8; body and commit message scanned SEPARATELY), `linear` | `b7afc9ea59c7` |
| `prompt_gate80.txt` | the prompt TEMPLATE built from the draft by `_scratch/mk_prompt.py` (section 2) | `9b5a161b5a9d` |
| `prompt_gate80.rendered.txt` | the launch-time render (heads, develop, seat, ls-remote time). Rewritten by every repin run | — |
| `launch_qa_secuura_gate80.sh` | the launcher, `--check`: re-hashes the 9 pins (rc 30/31), head file vs kit (rc 7), prompt guards (rc 8/33/39/25), re-reads origin (rc 6/17), TTY rule (rc 21), override rule (rc 16), moved-kit rule (rc 2). The two GO strings are DERIVED from the head file's seat | `6833d8f66ebb` |
| `repin_and_launch_gate80.sh` | the launch action, `--dry-run [--no-api]`, `--repin-develop` (section 5) | `98eef75ee794` |
| `pin_gate80.py` | rewrites `kit.json` `script_sha256` after any edit to a pinned file | — |
| `RULINGS_wednesday.md`, `ROUTING_LINE.txt` | Wednesday's rulings; the routing line `QA/Secuura-gate80\|coagent@agentmail.to\|yes` | — |
| `head_at_launch.txt` | written by the repin run (P x2, B, T x2, D, S); currently the real values + seat `Seat K 3rd` (a DRY-RUN test seat, not a ruling) | — |
| `dry_194748.*`, `dry_run_console_final.txt/.rc` | the final dry run's step outputs | — |
| `arms/` | `arms_gate80.py` + every arm's `.out` / `.rc` + `arms_<set>.summary`; `arms/dry_arm_outputs/` the dry-run files the SIM arms produced | — |
| `predictions/` | every real run of the instruments (section 3) and the selftests. **Every figure in it is the kit builder's PREDICTION; the gate re-measures.** | — |

**No `c4_tools` file:** gate79's c4 re-ran K-seat tool fixes. These two PRs change no tool, so there is nothing to port. The shell-script legs of #1442 (suite, siblings, tamper) live in c3.

## 2. How the prompt was made (the draft, minus its notes)

`prompt_gate80.txt` = the draft from its `ultrathink` line to the MAIL paragraph. Removed: the `DRAFT, NOT SENT` banner and everything from `DRAFTER NOTES FOR WEDNESDAY` down. Every `@@FILL@@` (7 of them) became a launch-time token, filled by the repin script exactly as gate79 fills `{{HEAD}}` / `{{DEVELOP}}`:

| Draft placeholder | Now | Filled from |
|---|---|---|
| origin develop at send + ls-remote time (2) | `{{DEVELOP}}` ×2, `{{LSUTC}}` | the repin run's own fresh `ls-remote` (develop) and its UTC time |
| heads at send, #1441 and #1442 (2 + the 2 literal heads in THE PINS) | `{{HEAD1441}}` ×2, `{{HEAD1442}}` ×2 | `--head-1441` / `--head-1442`, each == kit.json AND == pull/head AND == branch |
| "KIT SCRIPTS: there are NO gate80-specific scripts … @@FILL@@" | replaced by the kit paragraph (names the 8 kit files + KIT_REPORT + RULINGS, the exact commands, "brief wins over the kit") | static; the launcher requires every file be named |
| "FLOOR AND USAGE at send: floor, usage, seat count" | replaced by one sentence: the launch action runs `usage_gate.sh --check` and refuses rc 12 at/over the cut; the reading is in the console. **The "floor" and "seat count" fills were DROPPED**: gate79's sent prompt has no such line and nothing in the kit produces them | — |
| merge seat ×3 (`The merge seat is @@FILL@@`, the two GO strings) | `{{SEAT}}` ×3 | `--seat "Seat X nth"`, REQUIRED, no default |

Nothing else in the draft was edited. The trees are literal (they are pins in kit.json; the launcher compares them with the head file). The draft's base `613070f29112…` stays literal in full.

## 3. What the instruments measured on the REAL heads (all PREDICTIONS for the gate; files in `predictions/`)

All read-only except the kit's own scratch. Times are UTC 2026-10-09.

**C1 / pair / code claims** (`c1_*_real.out`, `c2_*_real.out`): c1 #1441 12/12 PASS, c1 #1442 12/12 PASS, pair 3/3 PASS, c2 #1441 13/13 PASS, c2 #1442 10/10 PASS. Selected readings: subject lengths 77 and 66; trailers 0 content bytes (control 53); modes all `100644`; 36 tooling paths identical at base/head/develop; the `ks1341c` file goes 6 -> 9 `it(` definitions (C0 gone; D0, D4, D3, control D new); `.catch(() => [])` CODE-ONLY 2 -> 1 (raw 3 -> 2); the loop census lists 11 command lines and no bare `cat`.

**Docs composition** (`predictions/docs/`, `c3_docs.out`): both docs are one pure insertion at the same base line (flow doc line 4321, cheat doc line 4403). Textual merge in **either order: CONFLICT, 1 hunk per doc** (as the draft predicted). KEEP-BOTH in numeric order composes: `48.` once, `49.` once, `48.` before `49.`; the reverse placement (`49.` before `48.`) also loads. `html_docs_matrix`: base tree 12/0, #1441 head tree 12/0, #1442 head tree 12/0, composed 12/0, composed-reverse 12/0. CONTROL: a composition with only #1441's block reads `49.` absent. **MERGE-SEAT NOTE measured here:** the flow doc's `<h2>NN.</h2>` tail at base/develop is `42, 43, 44`, so the next free number on develop is 45, while both PRs take 48 and 49. The draft expected a `47.` from another PR; there is none on develop. Renumbering is the merge seat's call, not a finding against either PR.

**#1441 cells** (`predictions/cells1441/`, worktree at the head, `npm ci --ignore-scripts` + shared build, rc 0):

| route / tests | measured | the draft / READY said |
|---|---|---|
| base / head | 11 tests, reds **D0, D3, D4** (3 of 11) | 3 of 11 — MATCH |
| head / head | 11/11 | 11/11 — MATCH |
| base / base | 8/8 | 8/8 — MATCH |
| head / base | **7 of 8, C0 RED** (`Expected: 200 Received: 500`) | the draft said "8/8 where C0 is replaced" — **a PREDICTION SLIP**: the base file's control C0 pins the swallow, which the head route removes |

Every plant LANDED (sha) and was restored by sha; worktree porcelain clean after each. Whole originate suite (`suite1441`): **head 97 suites, 1099/1099; base (route + tests from base) 97 suites, 1096/1096**, 0 load failures. `tsc --noEmit -p services/originate`: **rc 0**.

**32-hex probe** (`predictions/probe32/`, router real, `$queryRaw` MODELLED):

| id | head route | base route |
|---|---|---|
| hyphenated UUID, UPPERCASE UUID | 200, 1 db call, id bound as given | same |
| 32 hex, no hyphens | **200 `[]`, 0 db calls** | 200 with rows, 1 db call, bound `7a1f3d2b2c3d4e4f90516b7c8d9e0f1a` |
| 32 hex, wrong-place hyphens; 36-char non-hex; `0`; `not-a-uuid` | 200 `[]`, 0 db calls | 200 with rows, 1 db call |
| `-bad id`; 129 chars | 400, 0 db calls | 400, 0 db calls |
| REJECTED promise on a UUID | **500 constant body**, logged once, no leak | 200 `[]` (the defect) |
| synchronous throw on a UUID | 500 constant, logged once | 500 constant, logged once |

So the draft's READ holds at the router: the unhyphenated 32-hex id now answers `200 []` with 0 db calls. The body's T8 sentence names `0` as the example and **T8b is True: the body does name the 32-hex / unhyphenated case**; `gh prtext` prints the sentence for the gate to rule. **Whether Postgres's `::uuid` cast accepts unhyphenated hex is UNMEASURED** (no database): the gate cites the Postgres docs with a version or writes UNMEASURED. The base-route red of D4 reads `Expected 200 Received 500` because the mock's `$queryRaw` returns `undefined` and `.catch` of `undefined` throws a TypeError; it is NOT a `::uuid` cast error. That is a mocked-db artefact the gate should state.

**#1441 tamper** (`predictions/tamper1441/`): HEAD row all green; CONTROL (no-op comment) all green. T1 remove only the guard -> **D4 red** (D4's failure text is the missing `deliveries` key, not a cast error); T2 rows key missing -> D4; T3 **guard placed BEFORE the id-format regex -> ALL GREEN: no cell catches it** (a finding for the gate to rule: a malformed id would answer `200 []` instead of `400`); T4 404 -> D4; T5 swallow back -> D0, D3; T6 `err.message` in the 500 body -> **C1 GET, C2 GET, C3, D0** (the draft predicted D0 only: a prediction slip). Every anchor occurred exactly once, every tamper LANDED, every restore matched the sha.

**#1442 suite** (`predictions/suite1442/`, `/bin/bash` 3.2.57): (script head, suite head) **9/0 rc 0**; (script BASE, suite head) **6 passed / 3 failed rc 1** with the three reds "drain then green -> both packages checked", "drain then green -> green reports format:check OK", "drain then red -> the gate fails (exit 1)"; (head script with ONLY the redirect removed) the same 6/3 rc 1 — the suite is what fails. Siblings, base and head identical: `package_format_gate` 33/0, `ks998_..._push_label_is_literal` 8/0, `html_docs_matrix` 12/0. `run-shell-suites.sh --list`: **73 at base, 74 at head**, the new suite listed at head. **Homebrew bash is not installed here: that leg is NOT RUN.** The full shell-suite RUN (passed/failed/skipped) was not run by the kit (only `--list`); the READY's 74/74 is untested by me.

**#1442 real packages** (`predictions/realpkg/`): `npm ci --ignore-scripts` rc 0 in akto, api-explorer, performance, playwright (registry reachable); `prettier` asserted executable in all four. `--list` and `--all`, BASE script vs HEAD script: **identical rc, stdout, stderr** (`4 package(s) checked, 0 skipped, 0 failed`). Stdin-reader census: none of the four `format:check` scripts can read stdin. CONTROL in the SAME run (a fixture package that drains stdin, sorted first, plus the four real ones): **base `1 package(s) checked`, head `5 package(s) checked`.** So today the redirect guards nothing in the four real packages (no live consumer) and the fixture proves it works when there is one.

**Hook path** (`predictions/hookpath/`): the PR's own four paths fed to the gate script on stdin select **nothing: silent, rc 0**. One path under a real package (`systemTest/performance/package.json`) selects `performance` (before the installs: `SKIP`, then `NOTHING CHECKED` rc 1). The hook lines that decide are printed. The live `git push` path was not run (and cannot be).

**#1442 tamper** (`predictions/tamper1442/`): HEAD 9/0. U1 `< /dev/zero` -> **TIMEOUT (hang), process group killed**; U2 drop `2>&1` -> **ALL GREEN, no cell catches it** (the fixture prints its `[warn]` on stdout; a finding to rule); U3 redirect on `cd` only, U4 redirect on the assignment, U5 no redirect -> each 6/3 rc 1.

**gh readings** (live, read-only; `predictions/gh_*.out`):
- `audit`: `audit-locks.mjs` line 50 is `import { satisfies as semverSatisfies } from 'semver';` at base and at BOTH heads; CONTROL (line 99999) returns None; neither PR touches the file, a manifest or a lock. The reference `dce5fdc3c952` was not fetched (the gate fetches by sha; the arm shows it reads NOT IN THE STORE, never a pass).
- `actions` (both PRs have 6 runs at the head; both PRs are `mergeable true`, state `unstable`, so CI RAN — unlike gate79's dirty PR): `security-scan.yml` Dependency Audit step "Audit-contract suites" red on both, classified PRE-EXISTING by `pr1443@4547234c8c79` and `pr1444@12487cdcde15`, with `semver` x2 and cannot-find x8 in each log; `pr-platform-suites.yml` red (k6, Akto, Playwright) classified PRE-EXISTING by develop's own push run; **`pr-security-gates.yml` Code Security Gates / "All shell test suites" is UNCLASSIFIED on both PRs** — the same job and step as develop's red, but the head's log carries more `ks998` / `format:check` needle lines than develop's (#1442 also `stdin_isolated` x2), so the kit does not call it pre-existing; the gate must read that log (the draft says so).
- `census`: 25 other open PRs, **OVERLAP-CODE 0, OVERLAP-DOCS 4** (#1445, #1444, #1443, #1383), and one `other` row on a WATCHED path: **#1250 touches `Blockchain/Dev/scripts/run-shell-suites.sh`** (not a path of either PR, but the discovery script the new suite depends on).
- `prtext`: #1441 title `KS-1345: …` (77) EQUALS the commit subject — **the draft says the title is `KS <n>:` by design; for #1441 that is not so**; #1442 title is `KS 998: …` (66) (de-hyphenated, differs from the subject by design). Attribution line (`Generated with`) count: 1 on each. #1441 commit message carries 1096/1096, 1099/1099, 11/11, 3 of 11, 8/8: all OK vs the READY; the body states none of them. #1442 body and commit message figures all OK (6/3, 9/0, 33/0, 8/0, 12/0, 74/0/0, 73 -> 74). The #1442 body also says `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED` (a fact for the gate).
- `linear`: KS-1345 In Progress, 0 comments, PR #1441 attached; KS-998 In Progress, 1 comment (2026-09-25), PR #1442 attached; neither archived; neither has a comment naming the PR (Wednesday's batch).

## 4. Refusal arms (all MATCH; `arms/arms_*.summary`, per-arm `.out` / `.rc`)

`arms_gate80.py all` runs them. Nothing in them launches: every repin arm is `--dry-run`, or refuses before any launch step (rc 9 at V; rc 16 for an override on a non-dry call).

- **red 42/42** (c1 / c2 / gh / c3 on the REAL heads with one planted wrong input): c1 wrong end-tree -> P4 FAIL; parents-n 2 -> P2 FAIL; base == head -> FAIL; the OTHER PR's head under `--pr 1441` -> P3 FAIL; `--pr 1437` -> rc 2; no `--end-tree` -> rc 2; short head -> rc 2; unresolvable develop -> rc 2; `pair` with the same PR twice -> P13 FAIL; c2 head == base -> W0 / S0 FAIL; c2 with the other PR's head -> FAIL (both directions); `prtext` with a foreign hyphenated key, two `Refs`, a closing word, `+94`, `2 of 11`, no `Refs`, html `11/1`, shell `73` -> each FAILS; `audit` with a planted needle -> FAIL; an unfetched reference -> NOT IN THE STORE; `api` with a wrong head -> rc 1; c3 `--route main` -> rc 2; c3 `setup1441 --wt` under `!CODING` -> rc 2 and the path does not exist afterwards.
- **repin 40/40:** each of the 10 required args missing -> rc 9 (x10); wrong head / branch / tree (both PRs), base, parents-n, develop -> rc 11 (x9); short head -> 9; bad seat -> 9; `--no-api` on a real launch -> 9; unknown flag -> 9; stale `--repin-develop` on an unmoved develop -> 10; `G80_LSFILE` on a real launch -> 16; #1441 head moved / #1441 branch moved / #1442 head moved / #1442 branch moved / both moved -> 11 (x5); ls-remote with no develop -> 2; SIM develops (commit objects in the KIT CLONE): clean with no repin -> 10, stale repin -> 10, docs-only with no repin -> 10, touching `webhooks.ts` -> 13, touching `check-package-format.sh` -> 13, touching `run-shell-suites.sh` -> 13, an orphan (not a descendant) -> 13, and docs-only / clean WITH the right repin -> rc 0 (x9).
- **launcher 50/50:** real ls (0); stand-in (0); bad pin 31; no pin 30; missing file 30; tampered probe block 31; unrendered token 8; wrong / extra GO string 8; one head or the develop absent from the prompt 8; no ultrathink 8; kit file not named 8; six measurement rules removed 33 (x6); five keywords removed 33 (x5); four holds removed 39 (x4); addendum removed 25; verdict subject changed 25; head file good (0), then 10 wrong values -> 7 (x10, each reason read), one `P` line 7, no seat 7, a head-file seat that disagrees with the prompt's GO strings 8; head / branch / develop moved at origin -> 6 / 6 / 6 / 17; moved kit 2; non-TTY launch 21 (nothing launched).

## 5. LAUNCH (Wednesday runs it; the builder did NOT)

1. **Name the merge seat.** There is NO default (a rejected idea: copying gate79's "Seat K 3rd" would be inventing a ruling). `--seat "Seat X nth"` is required; the two GO strings `GO (<seat>): merge 1441 on gate80` / `... 1442 ...` are derived from it and the launcher refuses rc 8 if the prompt disagrees. The `Seat K 3rd` in the files now is only the dry-run test value; a real run re-renders both.
2. **Back up `inbox_routing.conf`, then add the line** from `ROUTING_LINE.txt`: `QA/Secuura-gate80|coagent@agentmail.to|yes`. A real launch refuses rc 1 until it is present.
3. **Run from a real terminal** (replace `Seat K 3rd` with the seat you name):
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-10_gate80/repin_and_launch_gate80.sh --seat "Seat K 3rd" --base 613070f29112a40a0d8d9684cd50c7c2ae54592c --parents-n 1 --develop 613070f29112a40a0d8d9684cd50c7c2ae54592c --head-1441 7685e79af2c437b1e6cc8fe2e57b1b0771f576d5 --branch-1441 feature/ks-1345-webhooks-deliveries-failed-query-500-g6-1 --tree-1441 4c5002a04c8cc11760f99a0ee66027c577e76f03 --head-1442 a7ec5746cb8b43313d55d73185ada4931b17c5be --branch-1442 feature/ks-998-format-gate-npm-stdin-isolated-f7-1 --tree-1442 f400aabef2c3dda518ceb9678786da18e5cee750
```
4. **A moved head (either PR) refuses rc 11** at the repin script (rc 6 at the launcher): re-draft; never re-gate a stale pin. **A moved develop refuses rc 10** and prints the exact `--repin-develop <sha>`; it refuses rc 13 instead if the advance touches a PR path outside the two docs or any of the 36 tooling paths.
5. **After the pane is up:** type `/model claude-opus-5-5` at the gate's idle prompt. The launch itself continues with the override check, `usage_gate.sh --check` (rc 12 if over the cut), the launcher `--check`, and `cockpit.sh add QA/Secuura-gate80`; **none of those four was run by the builder**.
6. **If you edit a pinned file** (including the prompt template), run `python3 pin_gate80.py`, then re-run the dry run. To rebuild the template from the draft: `_scratch/mk_prompt.py`.

## 6. Open questions for Wednesday

- **Q-SEAT80** (above): no default.
- **Q-FLOOR80:** the draft's "floor / usage / seat count" line has no source in the kit; I replaced it with a pointer to the launch console. Tell me if you want those numbers rendered into the prompt and where they come from.
- **Q-TITLE1441:** the draft says titles are `KS <n>:`; #1441's PR title is `KS-1345: …`. The kit measures both and rules nothing.
- **Q-PLAYWRIGHT-NEEDLES:** the Actions change-needle set includes the bare word `format:check` (it is a token of #1442). It appears 40 times in develop's own Playwright log, so the kit counts a needle only where the head EXCEEDS the matched comparator. Code Security Gates still reads UNCLASSIFIED on both PRs by design.

## 7. Bugs the dry runs caught in my own first drafts (all quarantined, all fixed, all re-run)

- `run1_docs_missing_from_tree`: my extracted tree lacked the two docs, so `html_docs_matrix` read 10/2 ("… is missing") on every single-PR tree and 12/0 only on the composed one. Fixed by extracting the two docs, and `docs` now prints TREE-INVALID if a doc is missing.
- `run2_docs_no_reverse_matrix`: the reverse placement was composed but not tested. Added.
- `run3_probe_once_queue_leak`: the probe's `mockClear` left queued `mockResolvedValueOnce` values from ids the head route never sent to the query; P-REJECT then read 200. Now `mockReset`.
- `run4_gh_before_classifier_fix`: the first change-needle rule made every Playwright log UNCLASSIFIED; the `prtext` claim regexes collided across suites (`74 passed` read as the 9/0 claim) and a true commit message masked a wrong body. Now needle excess vs the comparator, contextual claim regexes, body and commit scanned separately (arm `prtext_1441_three_of_eleven_wrong` is what caught the masking).
- `run5_zsh_split_refusals`: `set -- $var` did not word-split in zsh; the instrument refused cleanly (`--route must be base|head`), nothing ran.
- Also fixed before the arms: a `c2` crash (`ValueError` instead of a FAIL) when handed the wrong PR's head; the stdin census missed `$(cat)`; the `it(` regex missed `it.each(`.

## 8. What I could not make work, or did not do

- **Homebrew bash leg: NOT RUN** (not installed).
- **The full shell-suite RUN (`run-shell-suites.sh` run mode): NOT RUN**; only `--list` (73 -> 74).
- **The reference `dce5fdc3c952` and the failed-step logs' `semver` import error on the reference: not fetched/read here.** The kit read the logs of both heads and of PRs #1443/#1444, which carry the same step; the gate does the reference.
- **The live hook, a real push, Docker/platform suites (Schemathesis, Akto, Playwright, k6), a database, `check:openapi`, the real prettier on a NOT-clean file: not run.**
- **The real-launch path** (override check, usage gate, cockpit add, pane census): not run; the dry run stops before it by design.
- **No c4.** No kit instrument re-implements the gate's own independent probe (the prompt tells the gate to write one).
- **Docs, line `47.`:** none on develop; the draft's expectation could not be confirmed.

## 9. Every value I did not measure

- Whether develop or either head moves before launch (re-read at launch; the arms prove the refusals).
- Postgres `::uuid` acceptance of unhyphenated hex (no database).
- Any behaviour of the live hook, the GitHub merge ref, or CI re-runs.
- The Code Security Gates comparator question (whether the log difference is only the new suite's lines) — read by the gate.
- Linear's closing-word handling of `KS-1345:` / `KS-998:` subjects.
- Whether KS-1345 / KS-998 states change before launch (read live, now: both In Progress).
- The remaining 21 `other` open PRs' paths beyond the OVERLAP / WATCH classes.
- The usage reading and the cut at launch time (not read here).
- Opus 5.5 availability (the model switch is yours).
