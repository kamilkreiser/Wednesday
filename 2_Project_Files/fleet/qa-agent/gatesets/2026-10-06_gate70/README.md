# Gateset 2026-10-06_gate70 — README for Wednesday

**gate70** is a **T1 gate, round 1 of 2**, on one Secuura/Blockchain PR: **#1397 (KS-1425, author Seat D 10th)**. The PR is an in-range **lock-only** refresh plus **2 dated baseline rows**. It unfreezes preflight legs 6 (KS-470 npm-audit gate) and 7 (KS-531 standalone-lock gate), which fail on every push at develop `4eaf7741a6a4` because of five new advisories, one of them critical. #1393, #1395 and #1396 are held behind it.

**Why T1.** The PR edits two things:
- the security gate's own suppression list (`scripts/audit/audit-baseline.json`, +2 accepted advisories);
- the dependency set of 36 lockfiles. 16 of them carry proxy-addr, express's trust-proxy parser, as a PROD dependency.

A wrong row hides an advisory from every future push. A wrong lock entry ships an unverified tarball.

**What is not here.** gate69's doc merge-in machinery (TAIL rule, chain / mergetree / qm, composee5 readers) is absent on purpose. This PR touches **0 docs**, and its one parent IS develop, so the squash applies the head's tree exactly.

**How to read the figures.** The kit was drafted by one Wednesday drafting subagent, 2026-10-06 ~03:33Z–04:0xZ (host clock UTC). Every author figure here is a **claim**. Every drafter figure names its instrument, and the drafter's results are **predictions**, not evidence.

## 0. Bottom line

**Status.**
- The kit is complete.
- Every self-test is green, and each one has planted arms that FAIL.
- The dry run passed, rc 0 (§6).
- The launcher refuses a bad pin, a missing kit file and a tampered file (§6).
- The gate has **not** been launched.
- The routing line has **not** been added.

**Launch command (Wednesday runs it; NOT run by the drafter).** Run it in a real terminal, under `script -q /dev/null`:
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate70/repin_and_launch_gate70.sh 3e7be2044fe80ebced9c497bfc278a7333018a83
```
- Add the routing line first (§7), or the launch refuses with rc 1.
- If develop has moved past 4eaf, the script refuses with rc 10 and prints the `--repin-develop <sha>` to pass. It refuses outright (rc 13, c1 P12) if the advance touched any of the 37 paths or the audit / preflight tooling.

**What the launch re-reads.** At launch the repin script re-reads, and refuses on any mismatch:
- the READY;
- `refs/pull/1397/head` and the branch, by ONE `ls-remote` with GIT_SSH_COMMAND unset and the checkout's own `core.sshCommand`;
- the GitHub API (open, not merged, base develop);
- develop.

The launcher then re-hashes all 10 pinned kit files against `kit.json`, and re-reads origin itself.

**Pins** (drafter `ls-remote`, 03:33:51Z and 03:53:13Z, both identical):

| | |
|---|---|
| head | `3e7be2044fe80ebced9c497bfc278a7333018a83` (pull/head == branch `feature/ks-1425-advisory-lock-refresh-d10-1`) |
| tree | `0b06d3c18a1e116cb5c550a505e2cb8884315f63` |
| parent | ONE, `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe` == develop at both readings (tree `6884601a03dc`) |
| files | 37: 36 `package-lock.json` (every one +N -N) + the baseline +14/-0; +172 -158 in total |
| subject | `KS-1425: in-range lock refresh clears four advisories, baseline the other two`: 77 chars, 85 squashed, 0 trailers (control bf277eead268: 53 B) |
| API (03:5xZ) | open, mergeable true, `unstable`. Body sha256/16 `b33786f6a554af24`, 9,936 chars = 9,964 UTF-8 bytes (the READY's "9,936 chars" is EQUAL) |
| Linear | KS-1425 In Progress, not archived |
| GO (pre-ruled) | `GO (Seat D 11th): merge 1397 on gate70` |
| verdict subject | `[QA -> Wednesday] GATE70 (T1): #1397 KS-1425 advisory lock refresh`, FROM coagent@ TO wednesday-agent@ (RULINGS P5) |

## 1. Drafter predictions

All predictions are at (head 3e7be2044fe8, develop 4eaf7741a6a4).

| Gate check | Instrument / file | Drafter result |
|---|---|---|
| C1 pin | `c1_pin_gate70.py`, `c1_head3e7b_dev4eaf_ex1.out` | 13/13. P3: exactly the 37 kit paths. P10: 14 tooling paths identical at base / head / develop (hooks, preflight, cleanroom, every audit `.mjs`, expected-case-count, root manifest, mobile lock, skill). P12: base..develop touches 0 |
| 1 field-exact diff | `c2_locks_gate70.py diff`, `c2_diff_head3e7b_ex3.out` | 9/9. The plan derived **from the base alone** is 54 entries in 36 locks, and the head equals it. 0 added, 0 removed, key order kept. Every entry changes exactly version (+resolved +integrity where present). 158 writes; 2 version-only, both in the root lock (D1 holds). Indent kept and byte-exact round-trip in all 36 (D2 holds) |
| 2 integrity | `c3_registry_gate70.py tarballs`, `c3_tarballs_head3e7b_ex1.out` | 5/5. The 4 fixed tarballs' sha512 == registry `dist.integrity`. NEGATIVE CONTROL: the 4 old tarballs differ, and equal the base locks' 15 / 32 / 1 / 4 old entries. 52/52 changed entries == the downloaded sri. In-repo POSITIVE CONTROL: 12 proxy-addr 2.0.8 + 1 psp 7.1.6, 0 mismatches. The brief's prefixes match |
| 3 parent walk | c2 W1-W3 | 54 walked, 0 out of range, 0 orphans; parents identical base vs head. LIVE NEGATIVE CONTROL: the 4 psp 6.1.4 entries' parents (`^6.1.1`, `^6.1.2`) do NOT admit 7.1.6. The semver subset is independent of the repo's and self-tested on 22 hand cases |
| 4 legs | `c5_legs_gate70.py legs`, `c5_legs_base4eaf_ex2.out`, `c5_legs_head3e7b_ex2.out` | BASE: leg 6 rc 1, leg 7 rc 1 (43 locks, 1614 packages, 10 match / 5 baselined), the five ids printed **13** times (== the author's control). HEAD: rc 0 / rc 0, 7 match / 7 baselined, the five ids 0 times |
| 4 contract | `c5_contract_head3e7b_ex2.out` | rc 0. `ℹ tests 59 / pass 59 / fail 0` == expected-case-count 59 |
| 4 cleanroom | `c5_cleanroom_head3e7b_ex1.out` | rc 0, "All 35 standalone lock(s) pass", 0 tracked files modified. **But leg 2 is `npm ci --dry-run` over services/ packages/ frontend/ scripts/ only (D-7)** |
| 4 real npm ci outside leg 2 | `c5_realci_head3e7b_ex1.out` | the 5 changed standalone locks leg 2 never scans (connectors/whatsapp-bot, systemTest akto / api-explorer / performance / playwright): REAL `npm ci --ignore-scripts --no-workspaces` rc 0 each, added 99 / 413 / 360 / 272 / 219, every lock sha256 unchanged |
| 4 negative controls | `c5_nc_head3e7b_ex2.out` | 3/3, each ASSERTED LANDED and restored sha256-identical; `git status --porcelain` 0 lines after. NC1: whatsapp-bot's proxy-addr back to 2.0.7 → leg 7 rc 1 naming GHSA-jqcg. NC2: hp3w row removed → legs 6 AND 7 rc 1. NC3: psp 7.1.4 planted back into api-explorer → leg 7 **rc 0 (masked)** while c2 parse rc 1 with psp7 = 1 |
| 5 rows | `c4_baseline_gate70.py rows`, `c4_rows_head3e7b_ex2.out` | 7/7. A PURE INSERTION at byte 19,803 (3,581 B, 14 lines): head minus the span == base byte-for-byte, so `$comment` and all 22 old rows are byte-equal. 22 → 24. Shape == the KS-1403 braces row (same 5 keys, same order). KS-1425 / 2026-10-06 / 2026-10-31. Card + ruling verbatim in both reasons. rj75 says "6.1.4 ONLY". Nothing re-dated |
| 5 fuse | `c4_fuse_head3e7b_ex1.out` | 3/3 with the head's OWN `isLapsed` / `validateBaseline`. Live 2026-10-30, lapsed 2026-10-31. Control: GHSA-2mjp (no expires) at 2099-01-01 never lapses. validateBaseline `[]`, and its planted control (an expires deleted) is reported |
| 5 no high/critical | `c3_advisories_ex1.out` | 4/4. The fixed versions return 0 of the five ids; the old versions return all 4 (control). hp3w and rj75 are **moderate**. sprintf-js latest 1.1.3 is still affected. Severities match |
| 5 psp7 parse / mobile | `c2_parse_head_ex1.out`, `c2_parse_base_ex1.out` | HEAD: 0 proxy-addr / source-map-js / smol-toml / psp7 vulnerable; psp6 4 and sprintf-js 5 are the baselined copies. BASE control: 16 / 33 / 4 / 1. The mobile lock blob is unchanged, and the parser still sees source-map-js 1.2.1 there |
| 6 install | `c5_install_head3e7b_ex1.out` | rc 0, `added 1937 packages`, root lock sha256 `c7306d84307789ac` before == after |
| 7 PR text | `gh_gate70.py prtext`, `gh_prtext_head3e7b_ex2.out` | T1-T5 pass: `Refs KS-1425` on line 1, 0 closing words, only KS-1425 hyphenated, title == subject, 0 trailers. T6: 11 claims OK, **1 MISMATCH (D-1)**. rc 1 because of D-1 only |
| 7 Linear | `gh_linear_ex1.out` | KS-1425 In Progress (started), archivedAt null |
| 8 Actions | `gh_actions_head3e7b_ex1.out` | 7 runs at the head, 2 at develop's push. NEW-FAILING `Security Scanning` (ABSENT at develop's push runs: no baseline). `PR Security Gates (KS-168)` fails at BOTH (pre-existing). `pr` PENDING. `PR — Lockfiles` success |
| census | `gh_census_ex1.out` | 25 others: 11 OVERLAP, all long-open lockfile PRs (Dependabot #945-#949, #572, #575, #635, #639, #649, and #1360). #1393 / #1395 / #1396 are NOT overlap |

## 2. Claim defects the drafter measured (each a claim for the gate to rule; none blocks by the drafter's reading)

- **D-1 FALSE: "The 41 locks under `Blockchain/Dev` are indent 2; the 4 under `systemTest` are indent 4"** (PR body; also the ITEM-2 status and READY wording "41 x indent-2 / 4 x indent-4").
  - Measured over all 45 tracked locks at the head: **40 × indent 2** (all under Blockchain/Dev) and **5 × indent 4**.
  - The fifth indent-4 lock is `observability/package-lock.json`, outside both directories and untouched by this PR.
  - Instruments: c2 L6 census, and gh prtext T6 CL-INDENT.
  - No consequence for the change, since indent is detected per file. Polish.
- **D-2 FALSE PREMISE: "appended textually because the file does not survive a JSON round-trip (19,858 bytes at indent 2 and 20,586 at indent 4 against the file's 19,810)"** (commit body and PR body; inherited from B 56th §4).
  - The baseline **does** round-trip byte-exactly under node `JSON.stringify(j, null, 2) + "\n"` (19,810 = 19,810; the same at the head, 23,391), and under Python `json.dumps(ensure_ascii=False, indent=2)`.
  - 19,858 and 20,586 are Python's DEFAULT `ensure_ascii=True` sizes: it escapes the file's 16 non-ASCII characters.
  - The textual append is still a correct method and yields the same bytes (c4 B1 proves a pure insertion).
  - Instrument: c4 `B1rt` INFO line; a node one-liner at drafting.
  - Polish for this PR, but the precedent (B 56th §4) is wrong and will be re-cited.
- **D-3 DEFINITIONAL: "1,610 of its non-link entries have no `resolved` against 328".**
  - Measured: 1,937 non-link entries other than the root `""`: 328 with `resolved`, **1,609** without. 1,610 counts the root package's own entry.
  - Not a defect: prtext accepts either definition and says which matched.
- **D-4 "Body 9,936".** The READY says chars, and it is chars: 9,936 chars = **9,964 UTF-8 bytes** (sha256/16 b33786f6a554af24). Holds.
- **D-5 Actions.**
  - The repo `CLAUDE.md` premise "Actions are retired" is stale. The READY measured this; the drafter re-read 7 runs.
  - `Security Scanning` is NEW-FAILING by the comparator only because develop's push runs do not include it. The author measured the same 7-case `Cannot find package 'semver'` failure at #1394's merged head 585171bc2c29. The gate reads both logs (X6).
  - RULINGS Q1 / Q2.
- **D-6 Census.** 11 long-open lockfile PRs overlap the 37 paths and will conflict after the merge. Reported only (RULINGS Q3).
- **D-7 SCOPE of "leg 2 rc 0 — All 35 standalone lock(s) pass clean-room npm ci"** (READY arms table and PR body).
  - True as printed, but `lockfile-cleanroom.sh` runs `npm ci --dry-run --ignore-scripts` (:73 / :87). B 56th measured that it returns rc 0 on a planted bogus integrity, so it is not an integrity instrument.
  - It scans only `services packages frontend scripts` (:46). So **6 of the 36 changed locks are outside it**: the root (covered by the real install, check 6), `connectors/whatsapp-bot`, and the 4 systemTest locks.
  - The drafter closed the gap with c5 `realci` (a real install in those 5, every lock unchanged). Integrity for all 52 entries is proven separately by c3 T3.
  - Not a defect in the PR; a limit of the instrument the READY cites. The prompt requires the gate to read the script and run `realci`.

These author claims hold by the drafter's instruments:
- 54 entries / 36 locks / 158 writes / 2 version-only;
- +172/-158 over 37 paths, every lock +N -N;
- 16 / 33 / 1 / 4;
- 78 entries over 45 locks with 0 orphans;
- 12 locks already at proxy-addr 2.0.8;
- 8 tarballs == `dist.integrity`;
- base 10 match / 5 baselined → head 7 / 7, 43 locks, 1614 packages;
- the five ids 13 → 0;
- 59 / 59;
- 1,937 packages with the lock sha unchanged;
- the fuse;
- NC1-NC3;
- 0 trailers, subject 77;
- KS-1425 In Progress, moved by the integration and not by the author (the drafter saw updatedAt 03:24:57Z; who moved it is not re-measured).

## 3. Kit files and pins

`kit.json` `script_sha256` pins every executable and the prompt. The launcher refuses rc 31 on a mismatch and rc 30 on a missing, empty or unpinned file. `kit.json` itself, `README.md` and `RULINGS_wednesday.md` are not pinned: Wednesday may edit the README and RULINGS, and kit.json holds the pins.

| File | What | Self-test (drafter) |
|---|---|---|
| `kit.json` | pins, the PR spec, the 37-path numstat, the plan (4 packages, old→new, severity, the brief's integrity prefixes), baseline row spec, tooling paths, legs, GO, routing | — |
| `lib_gate70.py` | read-verb git; write verbs only outside `!CODING`; per-file indent + byte-exact round-trip; npm's nearest-node_modules walk; an INDEPENDENT semver subset; registry, GitHub, Linear reads (tokens by name) | via c2 |
| `c1_pin_gate70.py` | P1-P12 | `c1_selftest_ex1` 7/7 |
| `c2_locks_gate70.py` | `diff` (checks 1 + 3) and `parse` (check 5) | `c2_selftest_ex1` 16/16: planted added / removed entry, 4th field, reordered fields, resolved ADDED to a version-only entry, wrong version, reindent, a non-canonical byte, out-of-range parent and orphan all FAIL; 22 semver hand cases |
| `c3_registry_gate70.py` | `tarballs` (check 2) and `advisories` (check 5) | `c3_selftest_ex1` 4/4 |
| `c4_baseline_gate70.py` | `rows` and `fuse` (check 5) | `c4_selftest_ex2` 10/10: edited / re-dated / removed old row, reordered keys, 6th key, wrong ticket, no ruling, a critical id baselined and a canonical re-serialisation all FAIL |
| `c5_legs_gate70.py` | `legs`, `contract`, `cleanroom`, `realci`, `install`, `nc` (checks 4 + 6) in the tester's own worktrees | `c5_selftest_ex4` 10/10: rc 2 is NOT RUN, a silent rc 1 FAILS G-BASE, a head naming a fixed id FAILS |
| `gh_gate70.py` | `api`, `actions` (gate69's approach), `census`, `prtext` (with T6 claims vs c2's measured json), `linear` | `gh_selftest_ex2` 10/10 |
| `prompt_gate70.txt` | template: `{{HEAD}}` ×14, `{{DEVELOP}}` ×1 | — |
| `launch_qa_secuura_gate70.sh` | per-kit launcher with `--check` and pin verification | §6 |
| `repin_and_launch_gate70.sh` | the launch action, with `--dry-run` | §6 |
| `RULINGS_wednesday.md`, `ROUTING_LINE.txt`, `LAUNCHER_ARMS.txt` | pre-rulings + open questions, routing line, arms | — |

- `_quarantine/` holds superseded runs; nothing was deleted.
- `_scratch/clone` is the dry run's `--shared --no-checkout` clone (objects only).
- `_scratch/arms/` holds the arm stand-ins.
- The drafter's own worktrees, tarballs and evidence trees are in the drafter's session scratchpad, not here.

## 4. How the 9 required checks map onto the kit

1. **Field-exact diff:** c2 diff L1-L6, plus the gate's OWN independent parse (the prompt requires one).
2. **Tarball integrity:** c3 tarballs T1-T5.
3. **Parent walk:** c2 W1-W3, plus a cross-check against the repo's own semver.
4. **Legs 6 and 7, base vs head:** c5 legs. Also c5 contract (59), c5 cleanroom (leg 2) plus c5 realci (the 5 changed locks leg 2 never scans), and c5 nc.
5. **The 2 baseline rows:**
   - c4 rows: shape, byte-equal, expires;
   - c4 fuse;
   - c3 advisories: no high/critical;
   - c2 parse: psp 7.x < 7.1.6 count;
   - c1 P10 + c2 S1: mobile.
6. **Install:** c5 install.
7. **PR body and ticket:** gh prtext (T1-T6) and gh linear.
8. **Actions:** gh actions NEW-FAILING vs develop, and the job logs (X6).
9. **NOT-TESTED.written-first.md:** written first (prompt CHECK 9).

## 5. UNMEASURED by the drafter

- The job logs of `Security Scanning` and `PR Security Gates (KS-168)`, at this head and at 585171bc2c29. The `pr` workflow was still PENDING at 03:5xZ.
- `format:check` in the four systemTest packages (the author claims rc 0).
- The frontend CSS build, the service suites, preflight legs 3/4/8, the four platform suites, and the runtime trust-proxy behaviour of proxy-addr 2.0.8 (no live sweep).
- The parent walk cross-checked against the repo's OWN semver (the gate does it).
- Who moved KS-1425 to In Progress. The READY says the GitHub integration did; the drafter read only the state.
- Whether develop moves before the launch: it was 4eaf at 03:53:13Z.
- The real-launch path of the repin script (usage gate, cockpit add) was not run.

## 6. Dry run and launcher arms

**Dry run** (`dry_run_console_ex3.txt`, rc 0, plus the `dry_035839.*` files), 03:58:39Z–03:59:32Z, at the FINAL pins:
- READY names the head (2 lines);
- ls-remote rc 0: develop 4eaf, pull/head == branch == 3e7b;
- API open / unmerged / develop;
- census 11 OVERLAP, reported;
- develop UNMOVED;
- render HEAD ×14 DEVELOP ×1;
- routing line ABSENT, reported (a real launch refuses rc 1);
- kit clone: c1 12/12 (`--no-remote`), c2 diff 9/9, c2 parse rc 0;
- launcher `--check` rc 0 with **10 pins EQUAL**.

The render guard first refused rc 9 on the drafter's own wrong threshold. That run is quarantined in `_quarantine/dry_render_threshold_refused/`. An earlier passing dry run and arm set, from before c5 `realci` was added and the kit re-pinned, is in `_quarantine/pre_realci_repin_dry_and_arms/`.

**Launcher arms** (`LAUNCHER_ARMS.txt`, `launcher_check_*_ex2.*`, at the final pins): 15 arms, every one firing as intended.
- **bad pin:** rc 31 (c2's pin flipped).
- **tampered kit file:** rc 31 (one byte appended to c4).
- **missing kit file:** rc 30 (c3 absent from the hashed copy).
- **unpinned file:** rc 30.
- unrendered prompt rc 8; forbidden D 10th GO rc 8.
- malformed / doubled head file rc 7.
- pull/head moved rc 6; branch moved rc 6.
- develop not a descendant of 4eaf rc 17.
- moved kit rc 2.
- a non-`--check` launch from a Bash tool rc 21: nothing launched.

**Repin arms:**
- pull/head moved: rc 11 MISMATCH.
- wrong input head: rc 11.

### 6a. Cleanroom (leg 2) drafter run
`c5_cleanroom_head3e7b_ex1.out`: rc 0, 15 s, "All 35 standalone lock(s) pass clean-room npm ci.", tracked status 0 lines before and after. See D-7 for what it does not cover, and `c5_realci_head3e7b_ex1.out` for the real install that covers it.

## 7. Routing line (NOT added)

Back up `inbox_routing.conf`, then add the line from `ROUTING_LINE.txt`:
```
QA/Secuura-gate70|coagent@agentmail.to|yes
```

## 8. Pane, report and rung 5

- **Pane:** `QA/Secuura-gate70`.
- **Report directory:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-gate70/`.
- **Rung 5, in the pane:**
  - #1397 and KS-1425 named;
  - the charter or this README being read;
  - the head `3e7be2044fe8`;
  - a `*_gate70.py --selftest` run;
  - its own clone and worktrees under `/private/tmp/claude-501/`, never `worktrees/s-d10-advlock`.
- **Rung 6:** `NOT-TESTED.written-first.md`.
