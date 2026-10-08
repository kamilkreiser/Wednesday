# gate75 KIT REPORT — drafter to Wednesday

- **Member:** #1426 KS-1450, the leg-14 guard's provenance exemption. Tier 2: a GUARD change.
  - Author: Seat R 16th. Branch `feature/ks-1450-slot-literal-guard-baseline-provenance-ra16-1`.
  - Head `dd31aa0c998ca43291c975dccb906a42e55c73c2`, END_TREE `5f456a0128feee7dd4e2f164f08f923f6a136742`, ONE parent `ddea005553bf65ffc284a9124a02ad53c5f88019`. That parent IS develop at draft.
- **Drafted:** 2026-10-08 12:28–13:15 AEDT (01:28Z–02:15Z) by one Wednesday kit-drafting subagent.
- **Built and dry-run only. Not launched.** Nothing was merged, pushed, commented, mailed, ticketed or routed. No tmux, no cockpit, no Linear.
- **Where it wrote:** this folder, plus the drafter's scratchpad (`…/scratchpad/gate75/`).
  - Every git write verb ran in the scratchpad's `clone --shared` copy: worktree, merge-tree.
  - Nothing was written under `!CODING`. The shared checkout saw read verbs only, plus `ls-remote` (×3: 01:28:23Z, 01:57:07Z in the dry run, 01:59:42Z).
- **GitHub:** GETs only, with GH_TOKEN read by name.
- **Every figure below is a PREDICTION.** The gate re-measures each one.

## 0. Bottom line

1. **Launch-ready. No ruling blocks the launch.** The dry run went rc 0 at 01:57:47Z: 10 pins EQUAL, 43 by-name keywords, launcher `--check` rc 0. Every open question in `RULINGS_wednesday.md` carries a default the kit already assumes.
   - The routing line is NOT added. `ROUTING_LINE.txt` holds it. The drafter measured 0 copies in `inbox_routing.conf` (gate74's line reads 1 as the control); a real run refuses rc 1 until it is added.
   - `merge_seat` = `Secuura/Blockchain-R`, ordinal `Seat R 17th` (Q-SEAT75). GO string: `GO (Seat R 17th): merge 1426 on gate75`.
   - **Usage:** the gauge read **96%**. The repin passes `WED_USAGE_STOP=100` to `usage_gate.sh` ONLY after reading Kam's grant file (`status: live` + the card id + the gate clause); rc 12 otherwise. Dry run: `usage_gate: OK — weekly usage 96% < 100%`.
2. **develop is UNMOVED: `ddea005553bf65ffc284a9124a02ad53c5f88019`**, read at 01:28:23Z, 01:57:07Z and 01:59:42Z.
   - `refs/pull/1426/head` and the branch read `dd31aa0c…` each time. #1383 is unmoved at `32e8459bc0f5`.
   - **Calibration:** develop's tree `d6ee60d91e2f` IS gate74's `predicted_both` tree. The lineage's last prediction landed byte for byte.
3. **The landing: NO merge-in. It is an API-only squash.**
   - `merge-tree --write-tree develop head` in the drafter's clone gives rc 0, **predicted T' = `5f456a0128feee7dd4e2f164f08f923f6a136742` == END_TREE**. The head's only parent is develop.
   - The CONTROL pair (gate73 #1407 × #1409) reads rc 1 naming both docs.
   - `c4 merged` M1-M3: 3 checked, 0 FAIL, `MERGE-IN NEEDED: no`.
   - base..develop = 0 paths, so there is no leg-14 exposure to carry.
   - #1383 (held) conflicts on both docs with develop AND with this head (rc 1 both ways). Its conflict pre-dates #1426.
4. **The guard, both ways, in REAL worktrees** (`c3_guard_gate75.py leg14`; macOS `/bin/bash` 3.2.57, `jq-1.7.1-apple`):
   - **develop** (tree `d6ee60d91e2f`): rc 1, **8 passed / 1 failed**. The SCAN cell names exactly :10 :11 :854 :859 :864 :869 :874 :879.
   - **head** (tree `5f456a0128fe`): rc 0, **11 passed / 0 failed**, `provenance exemption: 2 exempted line(s), all of them $generated.from_runs members`.
   - CONTROL: the same tool with a wrong `--expect-tree` REFUSES rc 2.
   - **CI corroborates it independently on a Linux runner.** PR Security Gates / Code Security Gates / "All shell test suites":
     - develop `shell suites: 64 passed, 7 failed` with `no_hardcoded_slot_literals: 8 passed, 1 failed`;
     - head `65 passed, 6 failed` with `no_hardcoded_slot_literals: 11 passed, 0 failed`;
     - the 6 remaining FAILED lines are byte-identical between the two (`diff` of the two blocks: identical). They are develop's own (ks949 aborts on `packages/shared is not built` in CI).
5. **THE RED-PROOF, re-driven at the head: 16/16 arms MATCH their declared want.** Each restore is proved by `git hash-object` == the HEAD blob and an empty porcelain. Restore is from SAVED BYTES (R 16th's checkout fault, made impossible). Detail in §2.
   - **Two GAP arms read GREEN:** A4v and N4v. These are NOT the ruled A5. The exemption is wider than its words in two ways:
     - **VALUE membership:** a REAL `from_runs` value copied into another array passes;
     - **PATH SUFFIX:** a new file at another root ending `/schemathesis/config/schemathesis-baseline.json` and holding a real value passes.
   - Novel values in either shape are caught (A4, N2, N4 RED on the membership cell ONLY). → Q-GAP75 (rec: Minor, non-blocking, wording corrected).
6. **The full preflight by hand at the head** (S-1 first, `c3_preflight_gate75.py preflight`, the hook's exact invocation, 01:43:03Z–01:49:13Z):
   - `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`
   - `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`
   - legs **3 4 8** skipped (local stack down) — **not a pass**
   - leg 14 `11 passed, 0 failed`; 0 `^FAIL` lines vs 670 `^ok ` lines; wall-clock 320 s. This reproduces R 16th's three runs.
   - The SIM squash tree == the head tree (T' == END_TREE), so this run IS the SIM's run while develop is unmoved. The gate builds the SIM commit and asserts the equality.
7. **The baseline's real consumer:** `baseline_gate.load_baseline()` (imported with `sys.modules` registration, R 16th's lesson 10).
   - 171 entries at develop and at head, identical key set, **6 differ, only field `reason`**.
   - `jq -e .` rc 0, with the CONTROL (a 3-byte-truncated copy) reading rc 5.
   - R 16th's claim HOLDS.
8. **Docs** (`c4 docs`: 13 checked, 0 FAIL; D6 4/4 planted arms REFUSED):
   - ONE differing line per doc (D1 :1268, D2 :2169). Each is ONE insertion: the head line minus the fragment == the base line.
   - Fragments: 375 B `88acf43d41deee07` / 376 B `9ddeeee472590d41`.
   - **The clause is byte-identical in both docs (373 chars).**
   - Tags: `<code…>` 1199/1199 → 1201/1201 and 759/759 → 761/761; `tr`/`td` unchanged.
   - CONTROL: a literal `<code>` count reads D2's untouched base as 602, which reproduces R 16th's lesson 5.
9. **Actions** (`gh_gate75.py actions`, 01:53Z, all runs completed): all three classes HOLD against `base` (== develop == union).
   - PR Security Gates class (2): {Code Security Gates} ⊆ {Code Security Gates}.
   - Security Scanning class (1): Dependency Audit; the ONLY failed step is "Audit-contract suites"; the needle is present; 12 of the last 12 repo-wide runs failed.
   - `pr` class (3): head {Akto, Performance, Playwright} ⊆ develop {the same + Schemathesis}. **The head PASSES Schemathesis where develop fails it** (develop's failing step: "Install Schemathesis suite"). Named, no cause claimed.
   - Fabricated-sha CONTROL: 0 runs.

## 1. The kit (this folder)

| File | What it is |
|---|---|
| `kit.json` | All pins, one row. Includes: the measured branch-message facts (`branch_trailer_bytes` 55, `branch_coauthor_lines` 1, `branch_keys_hyphenated`); the leg-14 block with the drafter's arms; Actions; `predicted_squash`; `merge_tree_control`; `neighbour_1383`; the usage grant path; `script_sha256` (10 files). |
| `lib_gate75.py` | Carried from lib_gate74 and re-keyed. composee5's h2 readers are DROPPED (no new block). Read-verb `git()`; `wgit()` refuses write verbs under `!CODING`; GH GETs; `Tally`; no default row. |
| `c1_pin_gate75.py` | P1-P15, self-test 9/9. P5/P6/P8 are PINS OF A FINDING (Q-TRAILER75, Q-KEYS75), not approvals. P10 asserts that EXACTLY the guard + baseline change among 21 tooling paths. P14 GUARD-ONLY. P15 the fix's own invariants. |
| `c3_guard_gate75.py` | NEW. `leg14` and `arms` (16 arms), self-test 8/8. It refuses: a non-worktree, a tree mismatch, a dirty start, `!CODING`, an anchor count != 1, an ignored plant. Restore by saved bytes, plants quarantined. A red only counts on the declared cell. |
| `c3_preflight_gate75.py` | Carried from c3_suites_gate74 (`preflight`, `pfcmp`, `format`; the parsers kept), plus NEW `baseline`. Self-test 6/6 on CAPTURED lines. |
| `c4_docs_gate75.py` | NEW. `docs` (D1-D6, insertion-only + parity + attribute-aware balance + 4 planted arms) and `merged` (M1-M4). Self-test 6/6. |
| `gh_gate75.py` | Carried from gh_gate74 and re-keyed (`api`, `prtext`, `actions`, `census`). Logs now carry the shell-suite lines. Self-test 11/11, on the REAL #1426 body as the fixture. |
| `fixture_body_1426_at_draft.md` | The live #1426 body, GET at draft, 10,110 B, sha256/16 `1775807b0378d835` (== R 16th's round-trip claim). |
| `prompt_gate75.txt` | The gate prompt template. `prompt_gate75.rendered.txt` + `head_at_launch.txt` are the dry run's render. |
| `launch_qa_secuura_gate75.sh` | The launcher, carried from gate74's. It holds no PR literal and reads P/B/D/S/C from the head file. |
| `repin_and_launch_gate75.sh` | The launch action. **Run only with `--dry-run`** by the drafter. NEW step 5: the usage grant. |
| `merge_inputs/1426.pr_body_keys_dehyphenated.DRAFT.txt` | The Q-KEYS75 (a) body: 10,094 B, sha256 `a36e00f5265b49f62f6121207e2cddeb6f019d3c3af280d2c7bc4cde435bb07a`. |
| `RULINGS_wednesday.md` | Carried rulings R1-R9, plus 12 OPEN questions with recommendations and defaults. |
| `ROUTING_LINE.txt` | `QA/Secuura-gate75\|coagent@agentmail.to\|yes`. NOT added. |
| `drafter_evidence_2026-10-08/` | `runs/`: every console, JSON, arm stdout/stderr, the launcher/repin arms (`r*.out`, `l*.out`) and `dry1.*`. `ci_logs/`: both Code Security Gates logs. `helpers/`: the drafter's probes. |

**Not carried from gate74:** `composee5_copy.py`, `t3check_1422.py`, the vitest modes of c3, and `fixture_body_1423_at_draft.md`. There is no flow/cheat BLOCK, no #1422, and no vitest change.

## 2. Arms: expected vs actual

**The guard arms** (`c3_guard_gate75.py arms`, wtHead, 01:36:07Z, 16/16 MATCH, every restore proved, final porcelain empty):

| arm | what | want | got |
|---|---|---|---|
| A0 | untampered | GREEN 11/0 | rc 0, 11/0 |
| A1 | slot value in a different key (`$generated.generated`) | RED on SCAN | rc 1, 10/1, names `:13` |
| A2 | from_runs id re-prefixed `nightly-` | RED on SCAN | rc 1, 10/1, names `:10` |
| A3 | literal appended to tracked `scripts/run-k6.sh` | RED on SCAN | rc 1, 10/1, names `run-k6.sh:217` |
| A4 | NOVEL id in a new array under `$generated` | RED on MEMB ONLY | rc 1, 10/1, MEMB FAIL, SCAN ok |
| **A4v** | a REAL from_runs value in a new array | GREEN-GAP | **rc 0, 11/0: VALUE membership** |
| A5 | bare marker in the quoted value at :859 | GREEN = named limitation | rc 0, 11/0 (occurrence 2 of 6 replaced, landed) |
| A6 | marker removed at :859 | RED on SCAN | rc 1, 10/1, names `:859` |
| A7 | exemption stage removed | RED on SCAN, exactly 2 lines | rc 1, 10/1, `(2 lines)` :10 :11 |
| A8 | jq shim exit 127 | RED | rc 1, **9/2** (MEMB + MEMB_CTL) |
| A8b | jq absent from PATH (1,881 tools symlinked; `command -v grep` control) | RED | rc 1, 9/1, `jq is required` |
| N1 | NEW untracked harness file (`playwright/tests/…spec.ts`, check-ignore rc 1; control rc 0) | RED on SCAN | rc 1, 10/1, names the new file `:1` |
| N2 | NOVEL id in a new array INSIDE an accepted entry, slot 3 | RED on MEMB ONLY | rc 1, 10/1 |
| N3 | slot literal in another key (an entry's `ticket`) | RED on SCAN | rc 1, 10/1, names `:880` |
| N4 | NEW file `fixtures/schemathesis/config/schemathesis-baseline.json`, NOVEL id | RED on MEMB ONLY | rc 1, 10/1 (the suffix filter exempted it; the value check caught it) |
| **N4v** | the same suffix-path file, a REAL value | GREEN-GAP | **rc 0, 11/0: PATH SUFFIX** |

**Self-tests** (final pass):

| Test | Result |
|---|---|
| c1 `--selftest` | 9/9 |
| c3_guard `--selftest` | 8/8 |
| c3_preflight `--selftest` | 6/6 |
| c4 `--selftest` | 6/6 (incl. the 602 naive-count control) |
| gh `--selftest` | 11/11 |

**Launcher / repin arms** (drafter, 01:58Z; outputs in `drafter_evidence_2026-10-08/runs/{r,l}*.out`):

| Arm | Result |
|---|---|
| wrong `--head-1426` (develop's sha) | rc 11 |
| missing `--develop` | rc 9 |
| `--no-api` without `--dry-run` | rc 9 |
| one pinned file altered by 1 byte (copy dir) | rc 31 `BAD PIN` |
| head file comparator != kit | rc 7 |
| keyword `VALUE-NOT-POSITION` missing from the prompt | rc 33 |
| the restore-to-head rule missing from the prompt | rc 33 |
| a launch with stdin not a TTY | rc 21, nothing launched |
| CONTROL: untampered `--check` | rc 0 |

## 3. The author's claims: HOLD / DO NOT HOLD (drafter's instruments)

**HOLD:**
- head / tree `5f456a01…` / ONE parent == develop / 4 files +81/-9;
- body round-trip sha256/16 `1775807b0378d835`;
- leg 14 8/1 → 11/0 (local AND CI);
- A1, A2, A3, A4 (membership cell only), A6, A7 (2 lines) as described;
- A5 GREEN, as the named limitation;
- the 54-literal control and the 5 negative controls pass;
- preflight 71/0 of 71, 12/15, legs 3/4/8 skipped;
- docs: one line each, insertion only, fragment 2/2, 1199→1201 / 759→761;
- baseline_gate 171 / identical keys / 6 differ / `reason` only;
- `$generated.from_runs` untouched (parsed-JSON equal, 7 ids);
- "exactly 2 marker lines" (predicate `slot-literal-ok:[[:space:]]*[",]`);
- the three R 17th traps, read by AST:
  - `OTHER_SEATS` :222 has 179 entries / 177 unique, `r 17th` + `seat r 17th` PRESENT, `r 16th` ABSENT, `r 18th` ABSENT, duplicates `['e 6th','seat e 6th']`;
  - `MINE` :102 = `r 16th`; `MY_PANE` :415 = `secuura/blockchain-r]`;
  - `sweepra16.py` carries `--show` ×1 and `args.show` reads 0; the class literal `(?:[1-9]|1[0-57-9])` appears ×9;
  - R 17th's class `(?:[1-9]|1[0-68-9])` fullmatches 1-16 and 18-19, NOT 17. That is proven on the BARE class only; the parsed patterns remain R 17th's job.
- the handover is 166 lines, sha256/16 `30d8e5cd6e4a61e1`.

**DO NOT HOLD:**
- "Every red arm reads 10p+1f". The drafter's A8 reads **9p+2f**: the non-vacuity control also needs jq. R 16th's shim may have differed; the gate decides.
- The DRAFT KS-1450 comment, sentences (a)–(e) in RULINGS Q-COMMENT75:
  - path suffix;
  - value membership;
  - A8;
  - "the hook does not run it", which contradicts R 16th's OWN READY/PR body;
  - "the same `\s*\S` shape in at least four other harness guards", where the literal shape is in 2, and the performance guard has NO reason test and no bare-marker control.
- "in that one file" / "every exempted line really is a `from_runs` member", in the guard comment :48-56, the PR body and both doc clauses (Q-GAP75).

**Not claimed by R 16th, found:**
- the branch commit carries a `Co-Authored-By` trailer (Q-TRAILER75);
- the commit message and PR body hyphenate KS-1386 (+ KS-1401 in the body), which ATTACH (Q-KEYS75).

**Correction to Wednesday's R 16th BRIEF (not to the commission):**
- "Your push is systemTest-only, so the hook will NOT run it (R 13th's finding)" was wrong for a FIRST push of a new branch. The hook fails safe and runs the preflight. R 16th found and disclosed it; the draft comment inherited the brief's premise.

## 4. The project's MUSTs for this change type (SKILL at develop == head, blob `b59b74a592e9`; `systemTest/CLAUDE.md` blob `45149683a381`, both unchanged by the PR)

| MUST | Where | Drafter's reading |
|---|---|---|
| Every test change updates its platform's two HTML docs IN THE SAME COMMIT | §4 :365 | HOLDS (one commit, both docs) |
| Both files, every time | §4 :378 | HOLDS (parity: byte-identical clause) |
| The update reflects what actually changed | §4 :415 | HOLDS in substance; the clause OVERSTATES the scope (Q-GAP75) |
| Never cross platforms | §4 | HOLDS (platform-k docs only) |
| Tests for the tests; every fix red-before/green-after | §5b | HOLDS (8/1 → 11/0; the new cell has its own non-vacuity control; A4 proves it load-bearing) |
| 400-line cap excl. blanks/comments; nesting 4 | §5c | HOLDS by reading: the guard is 248 lines total; the deepest nesting in the new block is 3. Not lint-measured. |
| Every changed line carries WHY + ticket | §5d | Guard: KS-1450 block comments. Six JSON reason lines: no comment syntax (Q-5D75, polish). |
| systemTest docs go in systemTest/CLAUDE.md | §5e | :1166-1169 not updated for the second exemption (Q-CLAUDEMD75) |
| No branches / tickets unless instructed | §5e | HOLDS: the branch and KS-1451 were both instructed (brief; ANSWER_A5) |
| Numbers not adjectives; name what is unverified | §5f | HOLDS in the PR body (NOT RUN section) |
| A runtime change needs a live sweep | §5f | NOT OWED (no runtime change) |
| A bare marker exempts nothing | systemTest/CLAUDE.md :1169 | VIOLATED pre-existing (A5) and wider in the performance guard. KS-1451's scope. |

## 5. NOT covered by the drafter (the gate owns these, or they are UNMEASURED)

- **The four platform suites, and the preflight's 3 stack legs:** UNMEASURED (stack down). Never a pass.
- **The preflight at DEVELOP by hand:** NOT RUN by the drafter. develop's 70/1 figures are on record, and CI's 64/7 → 65/6 corroborates.
- **The Schemathesis package pytest suite:** NOT RUN. Host Python not probed against `>=3.14.8`; R 16th's host was 3.14.5.
- **jq's version floor**, and behaviour under a jq without `--arg`/`index`: UNMEASURED.
- **The performance guard's bare-marker behaviour ON ITS SUITE:** PROBED on the predicate in isolation only (`helpers/perf_marker_probe.mjs`).
- **Ticket states:** KS-1450, KS-1451, KS-1386 — NO Linear read. KS-1451's body is unread.
- **The format gate:** fed the PR's 4 paths, it read rc 0 and `0 package(s) checked`, with the gate silent. That is NOT evidence of formatting. R 16th's `1 package(s) checked` came from the hook's no-base first-push path.
- **`html_docs_matrix`:** not re-run by the drafter (R 16th: 12/0; never tag-balance evidence).
- **eslint / shellcheck** on the guard: NOT RUN.

## 6. Drafter defects, caught and fixed (disclosed)

1. **c3_guard's first parser mapped the NOGIT cell to two cells.** Its needle `'scanned '` also matches "is REFUSED, not scanned some other way". Caught before the first run by reading the needles; fixed to `'files under:'`. Self-test re-run 8/8.
2. **c3_preflight `baseline` passed a `str` to `load_baseline(baseline_path: Path)`** and raised `AttributeError`. That is the instrument's fault, not the module's. Fixed to pass `pathlib.Path`; re-run 4/4.
3. **c1 P15's message read "CONTROL truncated copy parses: True"** when it meant "REFUSED". Wording fixed; logic unchanged.
4. **The first `actions_probe` counted `conclusion=None` jobs as failing** (the `pr` run was still in progress at 01:32Z). The kit's `gh_gate75.py classify` treats them as PENDING; the 01:53Z read had every run completed.
5. **RULINGS first cited builder lines :113 / :205-209 / :213-216.** Re-grepped: :126 / :207 / :216. Corrected.

## 7. Launch (Wednesday runs it; the drafter did NOT)

1. Rule or accept the defaults in `RULINGS_wednesday.md`.
2. Add `ROUTING_LINE.txt` to `inbox_routing.conf`.
3. Run:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-08_gate75/repin_and_launch_gate75.sh --head-1426 dd31aa0c998ca43291c975dccb906a42e55c73c2 --develop ddea005553bf65ffc284a9124a02ad53c5f88019
```
- **If develop has moved,** it refuses rc 10, prints the re-predicted squash, and gives the `--repin-develop <sha>` to pass.
- **If a merge-in becomes necessary,** it refuses rc 13: RE-DRAFT, never `--no-verify`.
- **The first real run creates `_scratch/clone`** (gitignored) inside this folder.

## 8. RUNG 5 (after launch)
- The pane is up under `QA/Secuura-gate75`, and the prompt's first line is `ultrathink`.
- The gate writes `NOT-TESTED.written-first.md` first, then runs its self-tests.
- Expect about 25-35 minutes of wall clock:
  - the arms take ~3 min;
  - the preflight takes ~6 min, plus ~1.6 GB of installs in wtHead;
  - S-1 took 31 s on the drafter's warm npm cache.
