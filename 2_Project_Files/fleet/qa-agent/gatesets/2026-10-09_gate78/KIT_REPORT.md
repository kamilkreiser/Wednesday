# gate78 KIT REPORT — drafter to Wednesday

- **Target:** #1435 (KS-1452, author Seat V 1st), head `6f4adfe8835ec8ece51653f3f758d6a55ce12348`, tree `ccbb76460ad6`, ONE parent = develop `1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0`. handlebars 4.7.9 -> 4.7.10 in 5 locks.
- **Drafted:** 2026-10-09T00:36Z–01:14Z (= 11:36–12:14 AEDT) by one Wednesday drafting subagent, from the gate72 kit (#1406, same shape).
- **Built, not launched.** Nothing merged, pushed, commented, mailed, ticketed or routed. No tmux, no cockpit. `inbox_routing.conf` untouched (exact line count 0; control: 175 agentmail lines in the file).
- **Writes:** this folder only (scratch clone, worktrees, installs, SIM commits under `_scratch/`, gitignored). Nothing under `!CODING` was created or written: git READ verbs only against the checkout; no arm names a `!CODING` path. Post-run read: `ls !CODING` shows 0 `gate78` entries (control: 16 entries listed); the reports dir has 0 `gate78` entries (control: 7 `gate7x` dirs).
- **Every drafter figure below is a PREDICTION** (files in `predictions/`). The gate re-measures each one.

## 0. Bottom line

- **Kit complete.** Self-tests green, each with planted arms that FAIL: c1 19/19, c2 34/34, c3 10/10, c5 34/34, c6 15/15, gh 22/22.
- **Red arms on REAL data: 18/18 MATCH** (rc AND the named check line). **Repin arms 26/26 MATCH. Launcher arms 27/27 MATCH.**
- **Dry run rc 0** at the final pins (`dry_run_console_final.txt`, 01:11:41Z–01:12:33Z, §5), develop re-read by `ls-remote` immediately before it: `1e7f90e26137`, UNMOVED.
- **Every builder number the kit re-measured HELD** (§2). The drafter found **no blocker** and **no number that disagrees**. The claim defects (§3) are Polish/Minor: one attribution line in the PR body, an unreproduced control count (ts-jest 14), one ticket-comment sentence that over-reaches, 3 commit-body lines over 72 chars.
- **Actions have concluded since the READY** (it saw 3 pending at 00:30Z): `Security Scanning`, `PR Security Gates (KS-168)` and `pr` are red; all three classify **PRE-EXISTING by workflow path** (§2, check 8). `security-scan.yml` has no develop run, so its comparators are #1434's and #1433's heads; the planted develop-only rule prints "NEW" beside it, as the gate76 lesson predicts.
- **Routing line NOT added** (§6). A real launch refuses rc 1 until it is.
- **Model:** the exec line carries no `--model` (fleet convention). The prompt's MODEL-LINE tells the seat it is meant to run on Opus 5.5 and that Wednesday switches it; the launcher refuses rc 33 if that line is missing.

**Launch command (Wednesday runs it; the drafter did NOT).** Add the routing line first, then from a real terminal:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-09_gate78/repin_and_launch_gate78.sh --pr 1435 --head 6f4adfe8835ec8ece51653f3f758d6a55ce12348 --branch feature/ks-1452-handlebars-lock-refresh-v1-1 --base 1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0 --parents-n 1 --end-tree ccbb76460ad630ab9fdb74b31dfc16502eee94ac --develop 1e7f90e261379e58eadc3ca0bbcc8d7e9e6938b0
```
- `--develop` is ALWAYS the draft develop. If origin develop has moved, it refuses rc 10 and prints the exact `--repin-develop <sha>` to add; rc 13 if the advance touched the 5 paths or the 28 tooling paths (c1 P10/P12); rc 11 on a moved head (re-draft, never re-gate a stale pin).
- **After the pane is up:** type `/model claude-opus-5-5` at the gate pane's prompt and confirm the dialog (the CLI takes it mid-turn too). The seat reports `MODEL:` in report.md and the mail.

**Pins re-verified** (`env -u GIT_SSH_COMMAND git -C <checkout> -c core.sshCommand=<checkout's> ls-remote git@github.com:Secuura/Distributed_Secuura.git …`):

| reading (UTC) | develop | pull/1435/head | branch |
|---|---|---|---|
| 00:36:25Z–00:36:31Z (manual) | 1e7f90e26137 | 6f4adfe8835e | 6f4adfe8835e |
| 01:00:18Z (manual, before dry run 1) | 1e7f90e26137 | 6f4adfe8835e | 6f4adfe8835e |
| 01:11:30Z (manual, `predictions/final_lsremote.txt`) and 01:11:46Z (inside the final dry run) | 1e7f90e26137 | 6f4adfe8835e | 6f4adfe8835e |

API (`gh_gate78.py api`, 00:5xZ and in each dry run): open, unmerged, base develop, not draft, mergeable true, `unstable` (the three pre-existing reds), 1 commit, +18/-18, 5 files, body sha256/16 `02607867bcc12e90` (6,612 chars, 6,633 UTF-8 bytes). READY sha256/16 `ce6a5fe0d764f22d`.

## 1. What I carried from gate72, and what I changed

**Carried (the shape):** `lib` (read-verb-only `git()`, write verbs only outside `!CODING`, the independent semver subset, the nearest-node_modules walk, indent + byte round-trip, registry / GitHub / Linear readers with tokens by name, `Tally`); every PR constant a REQUIRED argument with a wrong-value arm; c1 P1–P12; c2 `diff` + `parse` with the base+registry model, M0, L1–L6, LT, W1/W1f/W2/W4; c3 `tarballs` + `advisories`; c5 `legs` / `contract` / `cleanroom` / `rootci` / `iso` / `nc`; gh `api` / `actions` / `census` / `prtext` / `linear`; the launcher's pin hashing (rc 30/31), prompt guards (rc 8/33/39/25), TTY rule (rc 21), override rule (rc 16), head file (rc 7); the repin flow (READY → one ls-remote → API + census → develop → kit clone + c1 → render → routing → `--check` → usage gate → cockpit); the prompt's structure, MERGE ADDENDUM, REPORT-HASH-LAST, verdict format and mail.

**Changed:**
- **Plan:** one package (handlebars) with THREE advisories (`plan.ghsas`), `field_delta_ready`, the READY's FULL integrity strings and tarball size.
- **c1:** P8b — the sibling KS-1453 must appear only unhyphenated (≥ 1). Tooling list 28 paths: the 4 member manifests, the 4 service Dockerfiles, and `security-scan.yml` / `pr-security-gates.yml` / `pr-platform-suites.yml`.
- **c2:** the model subtracts optionalDependencies from the packument's `dependencies`. **M0 caught this on the drafter's first real run**: the registry repeats `uglify-js` inside `dependencies`, npm's lock does not (first run quarantined in `_quarantine/c2_first_run_M0_fail/`). New **L7 MASKED BYTE COMPARE**: each changed entry's TEXT span swapped for the base's must give the base BYTES. My first L7 re-serialised the JSON, so its planted stray-byte arm did NOT fire; it was rewritten as a text-span splice. W1 prints the declaring-parent count. W4 names the skipped optional dep. parse covers all 45 locks and adds S3 (exactly 5 at 4.7.10).
- **c3:** T5 checks the FULL new and old strings and 712,317 B. A5 is now VERSION-FACTS: latest, the only release above 4.7.9, publish time, and the lock-field delta == `dependencies/minimist`. The mobile shell-quote A5 is gone.
- **c5:**
  - G-HEAD needs a printing control in EACH leg: leg 6's other GHSA ids, and leg 7's own `N advisories match`. **My first head run passed with leg 7 naming 0 other ids**, because leg 7 prints none at a pass. Quarantined.
  - G-BASE needs each id in EACH leg.
  - `nc` has FIVE arms, one per lock, and each runs BOTH legs and asserts specificity: own leg rc 1 naming the three, the other leg rc 0 naming none.
  - New `omit`: runtime reach by `npm ci --omit=dev`, plus a base control.
  - `wsuites` builds packages/shared (dist/index.js asserted) and each service, and parses suite-LOAD failures. **My first run skipped the shared build** and read governance 32 tests with 2 of 4 suites failing to load, rc 1. Quarantined.
  - `isuites` was dropped: the services resolve @secuura/shared only through the workspace (measured: `Cannot find module '@secuura/shared'`).
  - The issuer bundle and KS-562 known-failure code is dropped (no frontend lock, no shared member in scope).
- **c6:** a node_modules STATE model per stage. An `npm ci` REPLACES node_modules, from this lock only if the lock file sits in that dir (a `COPY --from` of the lock counts). `npm prune --omit=dev` makes it prod-only. `FROM <stage>` inherits state. R5 importer census with controls.
- **gh `actions`:** classifies by workflow PATH. The comparator is develop's own run if the workflow has one, else the newest failing pull_request runs of the same path on OTHER heads. Signature subset, change needles (handlebars, the 3 short ids, minimist), `##[group]` control, fabricated needle, history, and a printed develop-only planted rule. `--wait N` polls until nothing is pending.
- **gh `prtext`:** T3b sibling, T5b attribution lines, T6 claims (5/5/18, 7 parents, 45 locks, 712,317 B, literal 8, express 339, leg 6 9/24 and 15 other ids, cleanroom 35).
- **gh `linear`:** KS-1452 comment + attachment, and KS-1453 state + attachments.
- **Repin:** EVERY c1 FAIL refuses (gate72 let P8 through). A dry run driven by `G78_LSFILE` hands the same stand-in to the launcher (so a SIM develop is checked end to end).
- **Launcher:** the gate78 keyword set (45), the MODEL-LINE and by-path guards (rc 33), and two new holds (no `!CODING` writes; the builder's worktree named) (rc 39).

## 2. Drafter predictions (all at head 6f4adfe8835e / develop 1e7f90e26137; files in `predictions/`) — BUILDER'S CLAIM vs DRAFTER'S READING

| Check | Instrument → file | Builder's claim | Drafter's reading |
|---|---|---|---|
| C1 | `c1_pin_gate78.py` → `c1_real.out` | 5 files, 2/2 + 4×4/4; 0 trailers; subject 65 | **15/15 PASS.** 5 paths +18/-18 exact; tree ccbb76460ad6; trailers content 0 (control bf277eead268: 53 content bytes); 0 Co-Authored-By; subject 65 / squash 73; keys only KS-1452; KS 1453 unhyphenated ×1; 28 tooling paths identical at base/head/develop; baseline 4af041e8d74a; base..develop 0 paths |
| 1 lock diff | `c2 diff` → `c2_diff.out`, `c2_diff_L4b.out` | 5 entries, 18 writes; masked locks byte-identical | **13/13.** PLAN from base+registry = 5 entries in 5 locks (44 in-scope of 45 tracked); M0 5/5; L3 every leaf == model; L5 field sets == builder's; **L7 5/5 byte-identical when masked**; LT clean; indent 2 ×5; L4b == downloaded sri |
| 1 parse | `c2 parse` → `c2_parse_head.out` / `_base.out` | 45 locks: 0 ≤ 4.7.9, exactly 5 at 4.7.10 | head: 0 vulnerable over 5 entries, 5 at 4.7.10, 45 tracked; base: 5 vulnerable; mobile read, 0 handlebars |
| 2 integrity | `c3 tarballs` → `c3_tar.out` + `openssl dgst -sha512` | sha512-P5VJ…FtqXKg==, 712,317 B; 4.7.9 value reproduces the locks' | **5/5.** 4.7.10 712,317 B == registry == READY (openssl agrees); 4.7.9 662,780 B `sha512-4E71…sgnUQ==` == 4/4 base standalone entries, root carries none; T3 4/4; T4 4/4 |
| 3 advisories | `c3 advisories` → `c3_adv.out` | 4.7.10 → `{}`; 4.7.9 → 3 ids `>=4.0.0 <=4.7.9` | **5/5.** `{}`; 8r5x critical, p8wg critical, xw65 moderate, all on handlebars; latest 4.7.10, only release above 4.7.9, published 2026-10-05T22:37:37.837Z; delta `dependencies/minimist` `^1.2.5`→`^1.2.8` only |
| 3 legs | `c5 legs` → `c5_legs_base.out` / `_head.out` | base 6: 12/24 FAIL 3 NEW; 7: 43, 1613, 10 match / 7; head 6: 9/24 OK; 7 OK; "15 other ids" | base: leg 6 rc 1 (12 / 24), leg 7 rc 1 (43 / 1613 / 10 match, 7 baselined), each id 2× in leg 6 and 1× in leg 7. Head: rc 0 / rc 0 (9 / 24; 7 match / 7), ids 0×; controls: leg 6 names 15 other ids, leg 7 "7 advisories match" |
| 3 contract / leg 2 | → `c5_contract.out`, `c5_cleanroom.out` | 59/59; "All 35 standalone lock(s) pass" | TAP tests 59 / pass 59 / fail 0 == expected-case-count 59; leg 2 rc 0 "All 35 standalone lock(s) pass", porcelain identical |
| 3 NC | → `c5_nc.out` | root → leg 6 red, leg 7 green; originate → leg 7 red, leg 6 green | **5/5 specific.** NC1 root: leg 6 rc 1 (each id 2×), leg 7 rc 0 (0). NC2–NC5 originate / governance / referral / vc-issuer: leg 7 rc 1 (each id 1×), leg 6 rc 0 (0). Each landed, restored sha256-identical; porcelain 0 |
| 4 range | c2 W1/W1f/W2/W4 | "all 7 declaring parents say ^4.7.9" | 7 declaring parents (root lock: ts-jest + services/originate; originate standalone: root direct + ts-jest; 3 × ts-jest), 0 refuse 4.7.10, 0 admit 5.0.0, 0 moved; minimist ^1.2.8 → 1.2.8 in all 5; uglify-js 3.19.3 satisfies ^3.1.4 |
| 5 iso | → `c5_iso.out` | each standalone rc 0, lock unchanged, 4.7.10 | 4/4 rc 0, lock unchanged, no ancestor package.json; 4.7.10 ON DISK (added 439 / 699 / 576 / 576) |
| 5 root | → `c5_rootci.out` | root npm ci rc 0, 4.7.10 | rc 0, 1937 packages, lock unchanged, hoisted 4.7.10 |
| 5 omit | → `c5_omit_head.out` / `_base.out` | only originate carries it | head: originate **4.7.10**; governance / referral / vc-issuer ABSENT. Base control: originate **4.7.9**, the others ABSENT. All rc 0 |
| 5 suites | → `c5_wsuites_head.out` / `_base.out`, `c5_wcompare.out` | 115/115, 1,093/1,093, 34/34, 159/159; originate build rc 0 | **identical at base and head**: governance 115/115 (4 suites), originate 1093/1093 (96), referral 34/34 (7 files), vc-issuer 159/159 (17 files); 0 suite-load failures; all 4 builds rc 0; shared dist/index.js present |
| 6 reach | `c6 reach` → `c6_reach.out` | originate only; root lock 0 images; 31 lock-copying Dockerfiles; literal 8; 0 importers (express 339, ts-jest 14) | **5/5.** 37 basename Dockerfiles (38 by substring); 31 lock-copying; literal `package-lock.json` 8; `Dev/package-lock.json` 0; R1 0 root-lock stages; ships: **services/originate only** (runner `npm ci --omit=dev`, PROD there); governance / referral pruned, vc-issuer runner `--omit=dev`; importers **0**, express **339**, ts-jest **9** (my token instrument; see D-2) |
| 7 PR text | `gh prtext` → `gh_prtext.out`, `gh_sentences.txt` | — | T1–T5 pass; T3b KS 1453 unhyphenated ×2; **T5b 1 attribution line** (D-1); T6 10 claims: 9 OK, shortstat ABSENT (not stated); 84 factual sentences listed |
| 7 tickets | `gh linear` → `gh_linear.out` | KS-1452 one comment, In Progress; KS-1453 Backlog, 0 attachments | KS-1452 In Progress, not archived, 1 comment `59f4cc96` (971 B, sha256/16 `f75191164ea2e846`) links #1435, 1 attachment (the PR). KS-1453 Backlog, not archived, 0 comments, 0 attachments |
| 8 Actions | `gh actions` → `gh_actions.out` (00:54:32Z) | 3 pending at 00:30Z | 0 pending. **3 reds, all PRE-EXISTING by path:** pr-platform-suites.yml (`pr`) and pr-security-gates.yml by develop's own push runs (37760893371 / 37760892712); security-scan.yml by #1434's (37756331228) and #1433's (37753634990) heads, with 0 develop runs; the develop-only rule prints NEW. Change needles 0, fabricated 0, `##[group]` 19–31 per log. History: 12/12 failure for each path |
| census | `gh census` → `gh_census.out` | — | 29 others: 11 OVERLAP. Ten are Dependabot / older PRs on the root lock (#945–#949, #572, #575, #635, #639, #649). **#1360 (KS-1380 revert, opened 09-30) touches root + governance + referral + vc-issuer and carries handlebars 4.7.9** in root and governance (read at its head d0e99f181a4e) |

## 3. Claim defects the drafter measured (each a claim for the gate to rule; the drafter rules none)

- **D-1 Attribution line in the PR body:** the body ends `🤖 Generated with [Claude Code](https://claude.com/claude-code)` (gh T5b: 1). gate77 Q-ATTR77 precedent: rec drop it. It is not a trailer (T5 0); the commit carries none (P5/P6).
- **D-2 "controls: … ts-jest 14"** (PR body :44, plan mail §5). The builder named no instrument, and the drafter could not reproduce 14:
  - c6's token match in .js/.ts/.json excluding locks reads **9**;
  - `git grep -l -F ts-jest <head> -- ':!*package-lock.json'` reads **13**;
  - `git grep -l -F ts-jest <head>` reads **18**.
  - It is a CONTROL count: every reading is > 0, so the importer zero stands either way.
  - "express 339" reproduces exactly.
- **D-3 KS-1452 comment, sentence 4:** "Local unit suites on the edited locks: governance 115/115 …". The suites run in WORKSPACE mode and resolve against the ROOT lock. The four standalone locks (4 of the 5 edited) are exercised only by installs (iso / omit), not by any suite: isolated runs cannot resolve @secuura/shared (measured). The READY's own wording ("workspace install after the edit") is accurate. Rec Polish.
- **D-4 Commit body:** 3 of 34 lines are > 72 chars (the "Proof:" paragraph). Polish; the squash body the merge seat composes can rewrap it.
- **D-5 Not a defect, an instrument note:** the READY's trailer control "0861f8f83 prints 55 bytes" is a RAW figure; the kit's control `bf277eead268` reads 53 CONTENT bytes (55 raw). Both are true of their instrument.
- **D-6 Collision (report only):** #1360 is an open revert "at Peter's request" and carries handlebars **4.7.9** in the root and governance locks. Its merge-base is `a5ab2ca9aa11`. Landed after #1435, it would conflict on those locks, or, if resolved toward its side, re-introduce 4.7.9 and refreeze legs 6 / 7. Client-adjacent; not this PR's defect.
- **UNMEASURED by the drafter:**
  - the builder's regen cross-check ("churned up to 10 unrelated optional bindings");
  - the in-hook preflight lines (quoted from the builder's push log, not re-run as a hook);
  - legs 3 / 4 / 8.

**Held by the drafter's instruments:**
- 5 / 5 / 18 and +18/-18;
- the per-entry field set;
- masked-byte identity;
- the integrity string and 712,317 B;
- `{}` and the three ids / ranges / severities;
- 4.7.10 latest and the only release above 4.7.9;
- minimist the only field delta;
- 7 parents;
- legs 6 / 7 base and head counts (12/24, 43/1613/10/7, 9/24, 7/7) and the 15 other ids;
- 59;
- 35;
- the NC specificity both ways;
- 45 locks / 0 ≤ 4.7.9 / 5 at 4.7.10;
- iso 4/4;
- `--omit=dev` (originate only);
- the 4 suite counts and originate build rc 0;
- 31 lock-copying Dockerfiles;
- literal 8;
- root lock 0 images;
- 0 importers;
- express 339;
- KS-1452 / KS-1453 board state.

## 4. Kit files and pins

`kit.json` `script_sha256` pins 10 files. The launcher refuses rc 31 on a mismatch and rc 30 on a missing, empty or unpinned file. `kit.json`, `KIT_REPORT.md` and `RULINGS_wednesday.md` (if Wednesday writes one) are not pinned.

| File | sha256/12 | What |
|---|---|---|
| `lib_gate78.py` | 101109539eee | helpers (+ `linear_issue`) |
| `c1_pin_gate78.py` | ae4041e9e551 | C1 P1–P12 + P8b |
| `c2_locks_gate78.py` | d7311051a02f | checks 1 + 4, parse |
| `c3_registry_gate78.py` | 58e4d445d380 | check 2, advisories + version facts |
| `c5_legs_gate78.py` | f3206f7f81c5 | legs, contract, cleanroom, rootci, iso, omit, wsuites, compare, nc |
| `c6_reach_gate78.py` | 76998c55e982 | runtime reach + importers |
| `gh_gate78.py` | 4ad7e0dfa437 | api, actions (by path), census, prtext, linear |
| `prompt_gate78.txt` | c588af9502cd | 48 lines; `{{HEAD}}` ×13, `{{DEVELOP}}` ×2 |
| `launch_qa_secuura_gate78.sh` | 7de278d29c38 | launcher, `--check` |
| `repin_and_launch_gate78.sh` | 63688a9630fd | launch action, `--dry-run` |

Also in the kit:
- `ROUTING_LINE.txt`;
- `predictions/` (every drafter run + `selftest_*.out`);
- `arms/`: `arms_repin.sh`, `arms_launcher.sh`, `arms_red.sh`, their `*.summary` and every arm's `.out` / `.rc`; `repin_dry_partials/` holds the repin arms' partial dry outputs;
- `dry_run_console_final.txt` + `dry_<HHMMSS>.*` (the final dry run).

`_quarantine/` holds the superseded runs, each named for why. Nothing was deleted:
- c2's first M0 fail;
- c5's first head legs (leg-7 control gap);
- the suites without the shared build, and those without per-service builds;
- launcher arms run while the render held the SIM develop;
- the first two dry runs.

## 5. Every arm, with its command and result

**Self-tests** (`PYTHONDONTWRITEBYTECODE=1 python3 <script> --selftest`), all rc 0:

| script | result | planted / wrong-value arms |
|---|---|---|
| c1 | 19/19 | 13 |
| c2 | 34/34 | 21 |
| c3 | 10/10 | 3 |
| c5 | 34/34 | 16 |
| c6 | 15/15 | 3 |
| gh | 22/22 | 10 |

Examples of what the planted arms catch:
- a stale minimist `^1.2.5`;
- resolved added to the root entry;
- a dev-flag flip;
- a collateral entry or one stray byte (L7);
- a `*` parent admitting 5.0.0;
- a minimist cascade;
- a merge commit;
- a hyphenated KS-1453;
- a silent leg-7 control;
- an NC arm whose other leg also reddens;
- governance shipping handlebars;
- a removed prune;
- a re-install from a different lock;
- a suite-load failure behind 0 failed tests;
- a change needle in a CI log;
- a comparator-less red;
- an 8-parents body;
- a tarball off by one byte.

**Red arms on REAL data** (`bash arms/arms_red.sh` → `arms/arms_red.summary`): **18/18 MATCH**.

| arm | rc | fired |
|---|---|---|
| c1 `--end-tree` (gate72's tree) | 1 | P4 |
| c1 `--base b39051390ff6` | 1 | P2 (first parent) |
| c1 `--parents-n 2` | 1 | P2 (count) |
| c1 without `--end-tree` | 2 | REFUSED |
| c2 diff `--head <base>` | 1 | L1 |
| c2 diff without `--base` | 2 | REFUSED |
| c2 parse at base `--expect-clean` | 1 | S2 (5 vulnerable) |
| c3 tarballs `--head <base>` | 1 | T3 |
| c3 tarballs into a reused dir | 2 | REFUSED |
| c5 legs wtBase `--expect pass` | 1 | G-HEAD |
| c5 legs wtHead `--expect fail` | 1 | G-BASE |
| c5 omit wtHead `--tag base` | 1 | OMIT-BASE (4.7.10 where 4.7.9 is expected) |
| c5 nc with the legs swapped (planted kit) | 1 | NC1 |
| c6 with the reach claims planted (governance shipping) | 1 | R4 |
| gh prtext, body planted "all 8 declaring parents" | 1 | CL-PARENTS MISMATCH |
| gh prtext, body planted with hyphenated KS-1453 | 1 | T3 |
| gh actions with `##[error]` planted as a change needle | 1 | UNCLASSIFIED |
| gh linear with state planted `Done` | 1 | KS-1452 FINDING |

**Repin arms** (`bash arms/arms_repin.sh` → `arms/arms_repin.summary`): **26/26 MATCH**, every arm `--dry-run` or refused before any launch step.

| arm | rc |
|---|---|
| 7 × missing argument | 9 |
| 7 × WRONG VALUE (gate72's pr / head / branch / base / tree / develop, parents-n 2) | 11 |
| short head | 9 |
| `--no-api` on a real launch | 9 |
| stale `--repin-develop` | 10 |
| stand-in: head moved | 11 |
| stand-in: branch moved | 11 |
| develop not a descendant | 13 (P2b, P12) |
| develop touching audit-gate.mjs, via SIM commit `2f3fd22b580f` | 13 (P10, P12) |
| develop == the head | 13 (P12) |
| clean SIM develop `4765edf5d919` (docs only), no repin | 10 (prints the exact `--repin-develop`) |
| clean SIM develop, stale repin | 10 |
| clean SIM develop, repinned | **0** (DRY RUN COMPLETE, launcher check with the same stand-in) |
| `G78_LSFILE` in a real launch | 16 |

**Launcher `--check` arms** (`bash arms/arms_launcher.sh` → `arms/arms_launcher.summary`): **27/27 MATCH**.

| arm | rc |
|---|---|
| rendered | 0 (10 pins EQUAL, 45 keywords) |
| bad pin | 31 |
| no pin | 30 |
| missing file | 30 |
| tampered file | 31 |
| unrendered | 8 |
| a forbidden GO (Seat V 1st) | 8 |
| MODEL-LINE removed | 33 |
| by-path Actions rule removed | 33 |
| `!CODING` hold removed | 39 |
| MASKED-BYTES keyword removed | 33 |
| head file: good | 0 |
| head file: 6 × wrong value, malformed, two P lines | 7 ×8 |
| head file: wrong develop | 8 |
| ls real | 0 |
| ls: head moved | 6 |
| ls: branch moved | 6 |
| ls: develop moved | 17 |
| moved kit | 2 |
| non-TTY launch | 21 (nothing launched) |

**Order matters:** the repin SIM arm re-renders the prompt with the SIM develop. My first launcher-arm pass ran on that render (3 MISMATCH, rc 17; quarantined). The canonical dry run was re-run, and then the launcher arms gave 27/27. The real repin always re-renders from origin, so this cannot reach a launch.

**Final dry run** (`dry_run_console_final.txt` + `dry_011141.*`, 01:11:41Z–01:12:33Z), rc 0:
- V 7 args == kit;
- A READY names the head (1 line) and #1435 (2);
- 2 ls-remote rc 0;
- 1 API rc 0, census 11 OVERLAP reported;
- 3b develop UNMOVED;
- 3c c1 14 checked / 0 FAIL (P1 by name under `--no-remote`; the repin's own ls-remote is P1), c2 diff 13/0, parse rc 0;
- R HEAD ×13, DEVELOP ×2;
- 0 routing ABSENT (reported);
- launcher `--check` rc 0 with 10 pins EQUAL and 45 keywords.

## 6. Routing line needed (NOT added)

Back up `inbox_routing.conf`, then add the line from `ROUTING_LINE.txt`:
```
QA/Secuura-gate78|coagent@agentmail.to|yes
```

## 7. Open questions for Wednesday (each has the default the kit already assumes; rule them in `RULINGS_wednesday.md` beside this file — the prompt tells the gate to read it, and to use these defaults if it is absent)

- **Q-SEAT78 (merge seat):** no ANSWER names one.
  - **Default:** `GO (Seat V 2nd): merge 1435 on gate78`. Any other seat means editing `go_string` in kit.json (unpinned) AND the two GO lines in `prompt_gate78.txt` (pinned: re-pin with `_scratch/pin.py`). The launcher refuses rc 8 on a mismatch.
  - **Recommendation:** whichever seat holds `.push-lock-g1` next. V 2nd keeps the lane; the brief says no G seat launches while V is live.
- **Q-ATTR78 (D-1):** **default/rec** Polish, not a blocker. The squash body the merge seat lands carries no attribution line. No PR-body PATCH (the gate77 Q-ATTR77 shape).
- **Q-COMMENT78 (D-3):** **default/rec** Polish, no edit. If you want it corrected, the author seat edits comment `59f4cc96` in place to say "workspace mode (root lock)", before or after the merge. It is not client-facing prose about a defect.
- **Q-1360 (D-6):** **default/rec** report only in this gate.
  - Separately: whoever ever lands #1360 must re-run legs 6 / 7 on its merge result.
  - Your call whether Kam or Peter needs a line, since it is "at Peter's request".
- **Q-MODEL78:** the exec line has no `--model` (fleet convention), so the first minutes run on the default until you type `/model claude-opus-5-5`.
  - **Default:** as briefed.
  - **Rec:** consider `--model claude-opus-5-5` on the exec line from the next kit generation (a pin, a one-line launcher change, and a new arm).
- **Q-SUITES78:** the four service suites run in workspace mode (the root lock). The standalone locks are covered by installs only. **Default/rec:** accept, named in the report.
- **Q-ACTIONS78:** the security-scan.yml comparators are #1434's / #1433's heads (parent `0a6177ea5482`, one commit behind develop), because develop has no run of that path. **Default/rec:** accept (gate72 Q4 / gate76 R2 shape).
- **Q-DOCKER78:** Docker down (the builder's `docker info` rc 1; drafter UNMEASURED). The four platform suites are NOT RUN, and the gate does not start Docker. **Default:** as stated.
- **Q-DISCLOSE78 — drafter reads and writes:**
  - GitHub GETs: pulls/1435, actions runs / jobs / logs, workflow runs, open-PR census.
  - Linear reads: KS-1452, KS-1453.
  - Registry: packument, tarballs, bulk POSTs.
  - Tokens read by name inside the helper, never printed.
  - Writes: this folder's `_scratch` only. That covers the clone, two worktrees, npm installs, two SIM commits in the kit clone's object store, and a `git read-tree` index file. No ref was written in the shared store.

## 8. Pane, report and rung 5

- **Pane:** `QA/Secuura-gate78`.
- **Report directory:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-09-gate78/` (the gate seat writes it; absent at draft).
- **Verdict mail:** FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE78 (T1): #1435 KS-1452 handlebars lock refresh`.
- **Rung 5, in the pane:**
  - #1435 / KS-1452 named;
  - the charter being read;
  - head `6f4adfe8835e`;
  - a `*_gate78.py --selftest`;
  - its own clone under `/private/tmp/claude-501/`, never `worktrees/s-v1-hbslock`;
  - then the model switch confirmed on the statusline.
- **Rung 6:** `NOT-TESTED.written-first.md`.
- **Expected duration:** the suites take ~1.5 min a side, NC ~1 min, the Actions read ~1 min; the rest is the seat's own reading.

## 9. UNMEASURED by the drafter

- Whether develop moves before launch.
- Runtime behaviour of the originate image, and whether anything loads handlebars at runtime (the importer census is static).
- The regen cross-check.
- Preflight legs 3 / 4 / 8.
- `docker info` (drafter did not run it).
- The real-launch path: the usage gate and cockpit add were not run.
- Whether #1360 will ever be merged.
