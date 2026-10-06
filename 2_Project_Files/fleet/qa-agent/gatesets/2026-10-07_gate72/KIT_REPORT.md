# gate72 KIT REPORT — drafter to Wednesday

- **Target:** #1406 (KS-1437, author Seat G 3rd), head `4a400d7aa9dd273d91fb62375cb4b0598aa4405f`, tree `85820a21f80c`, ONE parent = develop `b39051390ff6f252601d6f7b45f0ea6c21c31023`.
- **Drafted:** 2026-10-06T21:06Z–21:36Z (host clock UTC; = 2026-10-07 08:06–08:36 AEDT) by one Wednesday drafting subagent.
- **Built, not launched.** Nothing merged, pushed, commented, mailed, ticketed or added to routing. No tmux, no cockpit.
- **Every drafter figure below is a PREDICTION** (files in `predictions/`). The gate re-measures each one.

## 0. Bottom line

- Kit complete. Every self-test green, each with planted arms that FAIL: c1 15/15, c2 25/25, c3 6/6, c5 19/19, c6 7/7, gh 20/20.
- Every check script also has a RED arm proven to fire on REAL data (§5b).
- Dry run rc 0 at the final pins (`dry_run_console_ex2.txt`, 21:33:50Z–21:34:30Z). Launcher `--check` rc 0, 10 pins EQUAL.
- 21 repin arms and 23 launcher arms, every one firing as intended (§5).
- **Routing line NOT added** (§6). A real launch refuses rc 1 until it is.
- Wednesday's mid-task input (the two red Actions) is folded in: `gh_gate72.py actions` re-verifies "pre-existing" from its own log reads. The prompt states that the in-hook legs 6/7 and CI's `Dependency Audit` step are different instruments.

**Launch command (Wednesday runs it; the drafter did NOT).** Run it under `script -q /dev/null`, after adding the routing line:
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-07_gate72/repin_and_launch_gate72.sh --pr 1406 --head 4a400d7aa9dd273d91fb62375cb4b0598aa4405f --branch feature/ks-1437-advisory-lock-refresh-g3-1 --base b39051390ff6f252601d6f7b45f0ea6c21c31023 --parents-n 1 --end-tree 85820a21f80c02d542ca1cf62e194750f2779c28 --develop b39051390ff6f252601d6f7b45f0ea6c21c31023
```
If develop has moved, the script refuses rc 10 and prints the `--repin-develop <sha>` to pass. It refuses rc 13 if the advance touched the 5 paths or the tooling.

**Pins re-verified** (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1406/head <branch>`, GIT_SSH_COMMAND count 0):

| reading (UTC) | develop | pull/1406/head | branch |
|---|---|---|---|
| 21:06:25Z–21:06:30Z (manual) | b39051390ff6 | 4a400d7aa9dd | 4a400d7aa9dd |
| 21:29:56Z (dry run ex1) | b39051390ff6 | 4a400d7aa9dd | 4a400d7aa9dd |
| 21:33:50Z (dry run ex2, final) | b39051390ff6 | 4a400d7aa9dd | 4a400d7aa9dd |

API at 21:2xZ: open, unmerged, base develop, mergeable true, `unstable`, 1 commit, +18/-18, 5 files.

## 1. What I carried from gate70, and what I changed

**Carried (the shape):**
- `lib_gate72.py`: read-verb-only `git()`, write verbs only outside `!CODING`, the independent semver subset (unchanged), npm's nearest-node_modules walk, per-file indent + byte-exact round-trip, the registry / GitHub / Linear readers (tokens by name), `Tally`.
- `c1` P1–P12 shape; `c2` `diff` + `parse`; `c3` `tarballs` + `advisories`; `c5` `legs` / `contract` / `cleanroom` / `nc`; `gh` `api` / `actions` / `census` / `prtext` / `linear`.
- The launcher's pin hashing (rc 30/31), prompt guards (rc 8/33/39/25), TTY rule (rc 21), override rule (rc 16).
- The repin flow: READY → one ls-remote → API + census → develop → kit clone + c1 → render → routing → `--check` → usage gate → cockpit.
- The prompt's structure: pins, authority, rules, checks, holds + named exceptions, by-name items, verdict format, MERGE ADDENDUM, REPORT-HASH-LAST, mail.

**Changed:**
- **Every PR-specific constant is a REQUIRED argument.** That covers the repin script (7 arguments) and every check script (`--head`, `--base`, `--develop`, `--end-tree`, `--parents-n`). Nothing defaults to a kit value; gate70's scripts defaulted to the drafter's head.
  - Each argument has a wrong-value arm (§5).
  - The launcher holds **no** PR literal. It reads P / B / T / D lines from `head_at_launch.txt` and compares each with kit.json (rc 7).
- **c1:**
  - P2 is split into three facts: is a commit, exact parent count, first parent (STANDING_LINES, R 5th).
  - P10 reads blobs with `ls-tree`, where an absent path is its own state, never a sha echo (STANDING_LINES, R 5th). It covers 25 tooling paths, including the baseline blob (P10b == `4af041e8d74a`), the 4 member manifests, the 3 Dockerfiles and `vite.config.ts`.
- **c2** derives the plan from **base + registry**, never from the head or the builder's `plan.json`. It builds the expected entry from the base entry's shape plus the new version's packument.
  - M0 control: the model fed the OLD packument reproduces every base entry.
  - L3 compares every leaf and the key order. This is what catches the non-uniform field set (`dependencies` moves) and a stale range.
  - New LT: the `-U0` line diff, the textual half.
  - New W1f: the must-fail next-major arm.
  - New W4: no cascade.
- **c3:** A1 requires the bulk API to answer exactly `{}`. New A5 covers the mobile 1.8.3 sentence.
- **c4 (baseline rows) dropped.** This round has no baseline row; c1 P10/P10b guard the file instead.
- **gate70's `realci` replaced by `c5 iso`.** Each changed standalone lock is installed **outside the workspace root**, the way its Dockerfile does it: no ancestor `package.json` (asserted), and the version is read off disk.
  - New `rootci`.
  - New `suites`: isolated and Dockerfile-shaped.
  - New `wsuites`: the builder's workspace mode, where KS-562 says threadTokenMint fails.
  - New `compare`: KF (the known failure identical at base and head) and BD (issuer bundle delta).
  - New `nc` NC3: pbkdf2.
- **c6_reach_gate72.py (new):** a Dockerfile stage parser with build contexts taken from compose, or inferred and named. It answers R1 root lock / R2 per-package images / R3 positive / R4 negative.
- **gh `actions` re-written per Wednesday's mid-task input:**
  - Logs are fetched by the tool, with the 302 followed **without** the auth header.
  - A `##[group]` positive control; a failure **signature** (error lines with timestamps and durations stripped).
  - Comparators read by the tool: develop's own run and #1397's head `3e7be2044fe8`.
  - Change needles, a fabricated needle, and history (12 runs).
  - A red is PRE-EXISTING only if a comparator's signature covers the head's, on the same job + step, and the head's log names none of the changed packages or ids.
- **gh `prtext` T3 is strict** (only KS-1437 hyphenated). T7 dumps every factual sentence for the gate. `linear` reads the KS-1437 **comment** (item 7) and KS-562.
- README.md, RULINGS_wednesday.md and LAUNCHER_ARMS.txt are folded into this file (§5, §7). The launcher requires `KIT_REPORT.md` instead (unpinned; Wednesday may edit it).

## 2. Drafter predictions (all at head 4a400d7aa9dd / develop b39051390ff6, files in `predictions/`)

| Check | Instrument → file | Result |
|---|---|---|
| C1 | `c1_pin_gate72.py` → `c1_real.out` | 13/14. **P8 FAILS: the commit message hyphenates KS-1425, KS-470, KS-531, KS-767, KS-769** (§3 D-1). P10: 25 tooling paths identical. P10b: baseline `4af041e8d74a`. P12: base..develop 0 paths. Subject 80, squash 88 |
| 1 lock diff | `c2 diff` → `c2_diff.out` | 12/12. The plan from base + registry is 7 entries in 5 locks, == the head. M0 reproduces 7/7 base entries. 18 leaf writes; per-entry field sets == the kit's prediction; LT line diff clean; indent 2 everywhere, round-trip exact |
| 2 integrity | `c3 tarballs` → `c3_tar.out` | 5/5. 3 new tarballs == `dist.integrity`. Negative control: 4 old tarballs differ and equal the base's 4 integrity-carrying entries (the root carries none). 4/4 changed integrity, 4/4 resolved |
| 3 advisories | `c3 advisories` → `c3_adv.out` | 5/5. Targets → `{}` (21:15Z). Old → the 3 ids with the brief's ranges and severities |
| 3 legs | `c5 legs` → `c5_legs_base.out` / `_head.out` | BASE: leg 6 rc 1 (`12` / `24`), leg 7 rc 1 (`43` / `1613` / `9 match, 7 baselined`); ids 6× in leg 6, 2× in leg 7 (== the builder's "6 and 2"). HEAD: rc 0 / rc 0 (`9` / `24`; `7` / `7`); ids 0× |
| 3 contract / leg 2 | → `c5_contract.out`, `c5_cleanroom.out` | 59/59 == expected-case-count. "All 35 standalone lock(s) pass", 0 tracked changes |
| 3 NC | → `c5_nc.out` | 4/4. NC1 pqg4 only; NC2 6qxp, not 477h; NC3 477h only. All restored sha-identical; porcelain 0 |
| 4 range | c2 W1/W1f/W2/W4 | 0 out of range; 0 ranges admit the next major; 0 cascade. Widened: `^1.19.9 \|\| ^2.0.5` ×2 and `^1.2.2` |
| 5 iso | → `c5_iso.out` | 4/4 rc 0, locks unchanged, no ancestor package.json. On disk: issuer / shared / anchoring pbkdf2 3.1.7, mcp-server sdk 1.31.0 (added 720 / 349 / 460 / 300) |
| 5 root | → `c5_rootci.out` | rc 0, 1937 packages, lock unchanged. Hoisted: shell-quote 1.11.0, sdk 1.31.0, pbkdf2 3.1.7 |
| 5 suites, isolated | → `c5_suites_*.out`, `c5_compare.out` | mcp-server 5/5 at both; anchoring **362/362 at both: threadTokenMint does NOT fail in Dockerfile-shaped isolation**; issuer build rc 0 at both. **packages/shared cannot run isolated: `vitest: command not found`, rc 127 — vitest is not its dependency** |
| 5 suites, workspace | → `c5_wsuites_*.out`, `c5_wcompare.out` | shared 945/945, mcp-server 5/5, anchoring **1 failed \| 361 (362), threadTokenMint, identical at base and head** (KF PASS) — the builder's numbers reproduce in this mode |
| 6 reach | `c6 reach` → `c6_reach.out` | 4/4. Dockerfiles: 37 by basename, 38 by substring. 82 package-COPY lines. Root lock → 0 images. sdk → mcp-server. pbkdf2 → 25 images, every one via `COPY --from=shared-builder /shared` from a FULL `npm ci` (anchoring also installs it in its own final stage; whatsapp-bot's context was inferred, not in compose) |
| 6 bundle | `c5 suites` + `compare` | 4 literals, each 1× in `dist/assets/dist-FCYm59UH.js`; provenance: pbkdf2 only; `createElement` 75; must-not-hit 0. **BD: the issuer dist is BYTE-IDENTICAL at base (pbkdf2 3.1.6) and head (3.1.7), 56/56 files** |
| 7 PR text | `gh prtext` → `gh_prtext.out` | T1 / T2 / T4 / T5 pass. **T3 FAILS: KS-1425, KS-470, KS-531, KS-562, KS-767, KS-769 hyphenated.** T6: 4 OK, **CL-COPYLINES MISMATCH (38 vs 37)**. Body sha256/16 `49f0ab69c4c1d541` == the READY |
| 7 ticket | `gh linear` → `gh_linear.out` | KS-1437 In Progress, not archived, 1 comment (2,492 B, sha256/16 `ab0aaf2d368ec843`). KS-562 Backlog |
| 8 Actions | `gh actions` → `gh_actions.out` | **Both reds are PRE-EXISTING by signature.** `PR Security Gates (KS-168)`: 9 signature lines identical at develop's run 37483332608 and #1397's. `Security Scanning`: 15 lines identical at #1397's run 37408769083 (no develop push run exists). Change needles 0, `##[group]` 24 / 19. History 12/12 failure for each. **`pr` still in_progress at 21:23Z → rc 1 (PENDING)** |
| census | → `gh_census.out` | 24 others: 11 OVERLAP, all on the root lock (#1360, Dependabot #945–#949, #572, #575, #635, #639, #649). #1404 / #1398 are not overlap |

## 3. Claim defects the drafter measured (each a claim for the gate to rule; the drafter rules none)

- **D-1 hyphenated foreign keys.**
  - The head's commit message hyphenates KS-1425, KS-470, KS-531, KS-767, KS-769 (c1 P8).
  - The PR body hyphenates the same keys plus KS-562 (gh T3).
  - STANDING_LINES:278-279: a hyphenated foreign key ATTACHES in a title, body or commit message.
  - The gate70 precedent required de-hyphenation (its P8/T3), and #1397's head commit message (3e7be2044fe8) de-hyphenated every foreign key.
  - The merge seat's explicit squash body can be clean, and a PR-body edit does not move the head.
- **D-2 "82 COPY lines … across 38 Dockerfiles"** (PR body :41, commit body, KS-1437 comment).
  - Measured: **37** files named Dockerfile.
  - The 38th is `Blockchain/Dev/scripts/check-dockerfile-non-root.sh` (a case-insensitive substring census).
  - 82 holds.
- **D-3 "the moderate pbkdf2 advisory had a browser-facing surface in the Issuer Portal"** (PR body :113; KS-1437 comment: "pbkdf2 was also reaching the browser … client-side surface").
  - pbkdf2 **in** the bundle HOLDS: 4 literals, provenance pbkdf2-only.
  - The issuer dist is **byte-identical at base and head**, 56 files (MEASURED AT RUNTIME, `c5_compare.out`).
  - The 3.1.6→3.1.7 JS delta is `lib/sync.js` only (tarball read). pbkdf2's `browser` map replaces `./lib/sync.js` with `./lib/sync-browser.js`, which is unchanged.
  - GHSA-477h's title is "pbkdf2 rehashes long passwords on every iteration" (bulk API). `sync-browser.js` already hashes a long key once, in its `Hmac` constructor (READ ONLY).
  - So "this advisory had a browser-facing surface" looks unsupported. The fix changes nothing the browser receives.
  - This claim is client-facing and already posted, on Wednesday's ANSWER_push instruction.
- **D-4 "it pins shell-quote 1.8.3, below the advisory's 1.8.4 floor, so it is not vulnerable to this one either"** (PR body :61, commit body).
  - Literally true for pqg4.
  - But the bulk API (21:08:19Z) returns **GHSA-w7jw-789q-3m8p (critical, `>=1.1.0 <=1.8.3`) and GHSA-395f-4hp3-45gv (high, `<=1.8.4`)** for 1.8.3, and the mobile lock pins it as PROD (c2 parse).
  - Mobile is out of scope (KS-769). The sentence's reassurance is the risk (STANDING_LINES:352).
- **D-5 "PR body … 11,393 B"** (READY :11). It is 11,393 **chars** = 11,489 UTF-8 bytes. The hash holds.
- **D-6 threadTokenMint "fails on develop"** HOLDS in workspace mode (identical at base and head). It is ABSENT in Dockerfile-shaped isolation (362/362), consistent with KS-562's "only under root-visible npm install": no image is affected.
- **D-7 packages/shared "945 tests"** HOLDS in workspace mode only. The package declares no vitest, so it cannot run isolated.
- **D-8 issuer install divergence.** Its Dockerfile `:18` runs `npm ci --no-audit` WITH install scripts. Both the builder's reproduction and the kit's use `--ignore-scripts` (X1). The build succeeded anyway; the divergence is named.
- Not a defect: the root pbkdf2 parent walk finds 6 declarers (nested `@cardano-sdk/crypto` copies). The brief lists 4 distinct ranges; the range set is the same.

**Hold by the drafter's instruments:**
- 5 / 7 / 18; +18/-18;
- the non-uniform field table;
- the integrity values;
- `{}`;
- the legs before / after text;
- 59;
- 35 OK;
- NC1 / NC2 specificity;
- 4/4 isolated installs with on-disk versions;
- 25 images;
- the sdk → mcp-server reach;
- the root lock → 0;
- 82 COPY lines;
- 945 / 5;
- the Actions "pre-existing" classification (re-derived, not copied).

## 4. Kit files and pins

`kit.json` `script_sha256` pins 10 files. The launcher refuses rc 31 on a mismatch and rc 30 on a missing, empty or unpinned file. `kit.json` and `KIT_REPORT.md` are not pinned.

| File | sha256/12 | What |
|---|---|---|
| `lib_gate72.py` | 73858ac3a851 | helpers (§1) |
| `c1_pin_gate72.py` | 99829490781f | C1 P1–P12 + P2 split + P10b |
| `c2_locks_gate72.py` | e3179f39e1cc | checks 1 + 4, parse |
| `c3_registry_gate72.py` | 2b82aef2643b | check 2, advisories |
| `c5_legs_gate72.py` | 5733c528996a | legs, contract, cleanroom, rootci, iso, suites, wsuites, compare, nc |
| `c6_reach_gate72.py` | 5310223f8a3b | runtime reach |
| `gh_gate72.py` | 79aba5a87658 | api, actions, census, prtext, linear |
| `prompt_gate72.txt` | 8cd6a1d09d07 | 46 lines; `{{HEAD}}` ×12, `{{DEVELOP}}` ×2 |
| `launch_qa_secuura_gate72.sh` | e43b0c036381 | launcher, `--check` |
| `repin_and_launch_gate72.sh` | 4bb6e6b5de48 | launch action, `--dry-run` |

Also in the kit:
- `ROUTING_LINE.txt`;
- `predictions/` (every drafter run);
- `arms/` (arm outputs and the two arm runners);
- `dry_run_console_ex2.*` + `dry_213345.*` (the final dry run; `dry_2134{33,39,40,41}.*` are the repin arms' partial outputs).

`_quarantine/` holds the superseded first dry run and arm set from before c6's message fix and re-pin, plus the superseded self-test copies. Nothing was deleted.

## 5. Every arm, with its command and result (final pins)

**Self-tests** (`PYTHONDONTWRITEBYTECODE=1 python3 <script> --selftest`):
- c1 15/15;
- c2 25/25;
- c3 6/6;
- c5 19/19;
- c6 7/7;
- gh 20/20.

Every result is rc 0, and each run includes planted defects that must FAIL:
- stale `dependencies` range;
- resolved added to a root entry;
- reorder, reindent, a non-canonical byte, `overrides`;
- an extra changed line (LT);
- an out-of-range parent, `*` admitting the next major, an orphan, a cascade;
- a merge commit, a wrong `--base`, a wrong `--parents-n`;
- an absent tooling path;
- a missing required argument;
- an unread log, a change needle, a different failing step, no comparator, an extra failure line;
- 38 vs 37;
- 21 field writes.

**5b. Red arms on REAL data** (`arms/red_*.{out,rc}`; each must FAIL or refuse):
| arm | rc | fired |
|---|---|---|
| c1 `--end-tree 0b06d3c18a1e…` (gate70's tree) | 1 | P4 |
| c1 `--base 4eaf7741a6a4…` | 1 | P2 first parent, P3 239 paths |
| c1 `--parents-n 2` | 1 | P2 count |
| c1 without `--end-tree` | 2 | REFUSED: required |
| c2 diff `--head <base>` | 1 | L1, L3, L5 |
| c2 diff without `--base` | 2 | REFUSED |
| c2 parse at base `--expect-clean` | 1 | S2 (4 / 2 / 1) |
| c3 tarballs `--head <base>` | 1 | T3, T4 |
| c3 tarballs into a reused dir | 2 | REFUSED |
| c5 legs at wtBase `--expect pass` | 1 | G-HEAD |
| c6 with the root lock planted as packages/shared's (`G72_KITJSON`) | 1 | R1, 50 stages |
| gh prtext on a body planted with "21 field writes" | 1 | CL-SET MISMATCH |
| gh actions `--compare-head <develop>` (no #1397 comparator) | 1 | Security Scanning UNCLASSIFIED |

**Repin arms** (`bash arms/arms_repin.sh`; every arm is `--dry-run`; outputs in `arms/repin_*`):
| arm | rc |
|---|---|
| missing `--pr` / `--head` / `--branch` / `--base` / `--parents-n` / `--end-tree` / `--develop` (7 arms) | 9 ×7 |
| WRONG VALUE `--pr 1397` / `--head 3e7be…` / `--branch …d10-1` / `--base 4eaf…` / `--parents-n 2` / `--end-tree 0b06…` / `--develop 4eaf…` (7 arms) | 11 ×7 |
| short `--head` | 9 |
| `--no-api` on a real launch | 9 |
| stale `--repin-develop` | 10 |
| ls stand-in: pull/head moved | 11 |
| ls stand-in: branch moved | 11 |
| develop = 3e7be2044fe8 (not a descendant: c1 P2b, P10, P12) | 13 |
| develop = the head (advance touches the 5 paths: P12) | 13 |

**Launcher `--check` arms** (`bash arms/arms_launcher.sh`; stand-ins in `_scratch/arms/`; outputs in `arms/launcher_*`):
| arm | rc |
|---|---|
| rendered | 0 (10 pins EQUAL, 39 keywords) |
| bad pin (c2's pin first hex flipped) | 31 |
| no pin (gh's pin removed) | 30 |
| missing file (c3 absent) | 30 |
| tampered file (one newline appended to c6) | 31 |
| unrendered prompt | 8 |
| a forbidden GO (Seat G 2nd) added | 8 |
| head file: good | 0 |
| head file: wrong pr / branch / head / base / parents-n / end-tree | 7 ×6 |
| head file: wrong develop | 8 (the rendered prompt does not name it) |
| head file: malformed | 7 |
| head file: two P lines | 7 |
| ls real | 0 |
| ls: head moved | 6 |
| ls: branch moved | 6 |
| ls: develop moved | 17 |
| moved kit | 2 |
| a launch (not `--check`) with stdin not a TTY | 21: nothing launched |

**Dry run:** the launch command above with `--dry-run`, giving `dry_run_console_ex2.txt`, rc 0. Its steps:
- V: 7 arguments == kit;
- A: READY sha256/16 `56371be81fbeb4c4`;
- 2: ls-remote rc 0;
- 1: API rc 0, census 11 OVERLAP reported;
- 3b: develop UNMOVED;
- 3c: c1 13/14 (P8 reported, not refused), c2 diff 12/12, parse rc 0;
- R: HEAD ×12, DEVELOP ×2;
- 0: routing ABSENT, reported;
- launcher `--check` rc 0.

## 6. Routing line needed (NOT added)

Back up `inbox_routing.conf`, then add the line from `ROUTING_LINE.txt`:
```
QA/Secuura-gate72|coagent@agentmail.to|yes
```

## 7. Open questions for Wednesday (the drafter rules none)

- **Q1 (D-1) Hyphenated foreign keys** in the head's commit message (P8) and the PR body (T3). Is this a blocker, or polish fixed by the merge seat's explicit squash body plus a PR-body edit (neither moves the head)?
  - The repin script reports P8 and does not refuse on it; every other c1 FAIL refuses.
- **Q2 (D-3) The "browser-facing surface" claim is already on KS-1437**, posted on your ANSWER_push instruction. If the gate rules it unsupported, STANDING_LINES:352 says EDIT the earlier comment rather than stack another. Who drafts the edit, and is that gated?
- **Q3 (D-4) The mobile sentence.** Do you want the gate to treat a literally-true but misleading reassurance as a finding against this PR, or as residue for KS-769?
- **Q4 `Security Scanning`** has no run on develop's push, so its only comparator is #1397's head. Does the same rule as gate70's Q1 apply (pre-existing proven by a log line on a develop-side head → named, does not block)?
- **Q5 The issuer Dockerfile runs install scripts; X1 allows `--ignore-scripts` only.** Accept the divergence (named), or grant scripts in the gate's isolated issuer copy?
- **Q6 `pr` workflow** was in_progress at 21:23Z. The gate waits for it or names it PENDING; its develop and #1397 runs are `failure`.
- **Q7 Disclosure: drafter reads.** These were read-only, under the same classes as the gate's X2 / X6 / X8:
  - GitHub GETs: pulls/1406, actions runs, jobs and logs, workflows, the open-PR census;
  - Linear: KS-1437 + comments, KS-562;
  - registry: packuments, tarballs, bulk POSTs;
  - GH_TOKEN and LINEAR_API_KEY read by name inside the helper, never printed. The only other `.env` read was `grep -c` of the two key names.
  - Writes went to the session scratchpad: clone, worktrees, npm installs, the suites in isolated copies.
  - The dry run created the gitignored `_scratch/clone` inside the kit.
  - Nothing under `!CODING` was written.
- **Q8 Docker is DOWN** (`docker info` rc 1 at 21:0xZ). The four platform suites are NOT RUN by commission. The prompt says Do NOT start Docker.

## 8. Pane, report and rung 5

- **Pane:** `QA/Secuura-gate72`.
- **Report directory:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-07-gate72/` (the gate seat writes it).
- **Verdict mail:** FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE72 (T1): #1406 KS-1437 advisory lock refresh`. Pre-ruled GO `GO (Seat G 3rd): merge 1406 on gate72` (ANSWER_ready.md:3).
- **Rung 5, in the pane:**
  - #1406 and KS-1437 named;
  - the charter being read;
  - head `4a400d7aa9dd`;
  - a `*_gate72.py --selftest` run;
  - its own clone and worktrees under `/private/tmp/claude-501/`, never `worktrees/s-g3-advlock`.
- **Rung 6:** `NOT-TESTED.written-first.md`.

## 9. UNMEASURED by the drafter

- Whether develop moves before launch (it was b39051390ff6 at 21:33:50Z).
- The `pr` workflow's outcome.
- Whether mcp-server exercises the SDK OAuth client.
- Runtime behaviour of any image.
- Preflight legs 3 / 4 / 8.
- The repo's own semver cross-check: c2 uses the independent subset; the gate runs the repo's.
- The real-launch path: usage gate and cockpit add were not run.
