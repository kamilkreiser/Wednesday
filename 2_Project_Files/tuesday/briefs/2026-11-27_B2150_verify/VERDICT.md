GATE B2150: GO WITH FINDINGS
@ 895da3f on main 279b223

Gate G1 (Opus), round 1 of 2 on the output-escaping class. This is lane 3 kit 1 (kit B2143 with its ADDENDUM-1, seat N184): RD-1016, and RD-1015 part (1). I graded the whole branch: A `08e67b7c`, B `2ec5fed1`, K `895da3f4` on BASE `279b2235`.

**RD-1016 holds under every adversarial shape the commission named.** No value reaches one of the five settings.js sinks unescaped. No scalar prints differently from BASE.

**RD-1015 part (1) holds for what the ticket's acceptance names**: a cell whose text STARTS with a formula character. No ordinary export changes by a byte.

But a text-fed number cell that holds a comma, a leading double quote or a line break is still written raw. A CSV reader then sees a cell that begins with `=` (Finding 1). This is pre-existing: these cells were raw at BASE, and the change makes nothing worse.

There is no Blocker. I found one Major, one Minor and two Infos, and **none blocks landing**. All three commits may land, under landing.txt. Its step 0b is REQUIRED once pull request 267 has landed: this branch then conflicts on the counts file (Finding 3).

Every number the seat reported that I re-ran agrees:
- red first at BASE and green at K, in both shapes;
- the turned rd835 file;
- the 14 mutations;
- the neighbours (37 suites, 516 tests);
- local CodeQL rc 0 at K, with the control reading rc 1.

## Re-measured
All GitHub reads were `gh api -X GET` under the NexusAI GH_CONFIG_DIR (the login holds "datasec", count 1), from 13:57:10 to 14:09:31 AEDT on 27 Nov.
- **main:** 279b22352dbcbd85664534395aeb366fec719a50 = BASE, at the first read and the last.
- **The branch:** `refs/heads/b2143/lane3-kit1` = 895da3f4630e170e038a1b5b2c78008ae7633b93, at both reads.
- **Open PRs:** `[267]` (b2133/lane2-erasure, head 52040f2e, mergeable_state `unstable` while its build ran). Its nine files share only `scripts/verify-expected-counts.json` with this branch.
- **Compare BASE...K:** ahead 3, behind 0, six files, exactly the kit's:
  - settings.js 6/16;
  - index.js 14/6;
  - rd835 test 1/1;
  - new rd1016 test 168/0;
  - new rd1015 test 217/0;
  - counts 3/3.
- **Commits:** each is the parent of the next; author = committer = the repo's noreply address on all three. K's tree on GitHub, 115dd91a, equals my clone's.
- **Blobs at K:** settings.js 07c2d16b, index.js b60cdd12, rd835 968d6380, rd1016 86870556, rd1015 c8c904b1. All equal the kit's STATE AT DRAFTING.
- **Code scanning:** main's javascript-typescript analysis 2257151397 at 279b2235 reads 29 results, with 22 open alerts:
  - backend/server.js 13, emailService 2, entraProvisioning 2, jsonStorage 2, incidents 2, tests/uat-run.js 1;
  - none in either script.

## How I measured
**Trees.** My clone is a `git clone --no-checkout --no-hardlinks` of the seat's clone, at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/g2150/clone`. It has worktrees `t/base` (BASE), `t/head` (K) and `t/mut` (K), plus `t/ctl` (K, unused and clean, see Leftovers).
- `node_modules` in each is a symlink to the seat's `npm ci` (disclosed).
- Dot segments read 0 in every tree (control: the seat's `.tools/b2143/clone` reads 1).
- Node v24.22.2.

**Jest lock.** I took ONE acquisition, `g2150-lane`: acquired after 0 s, 14:03:27 to 14:04:08, `lock-wrapper rc=0`.
- `NODE_OPTIONS`, `MIN_TESTS`, `MIN_SUITES` and `VERIFY_EXPECTED_FILE` were unset.
- Linux shape = `TMPDIR=/tmp` plus a persistent dot-free `RUNNER_TEMP`. Own shape = `/var/folders/...`.
- No jest ran outside the lock. Afterwards the lock base held no lock and an empty jest queue, and no process of mine remained (14:09:31).
- Load was 1.7 to 2.2. Every log is in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/g2150/logs/`.
- The judge is `tools/gjudge.py`, an exact failed-set judge copied from gate B2149. It refuses a file that collected 0 cells.

**(1) The diff, read whole.**
- settings.js: the first `escapeHtml` with its comment and the blank line after it (lines 92-104 at BASE, 13 lines) is removed. The live one becomes `var s = typeof text === 'string' ? text : String(text || '');` ... `return s.replace(...)`, with its comment grown.
- index.js: `csvNumberCell` is added after `csvCell`, and the eight cells on six lines are routed through it.
- rd835: the helper list on line 100 gains `'csvNumberCell'`.
- counts: 6530/411 becomes 6558/413.

Nothing else changed.

**(2) Red first, green, turned file, rd778** (all `GJUDGE ... PASS`):

| Run | Result |
|---|---|
| rd1016 at BASE, linux and own | 13 cells, failed exactly E1, E2, E3, A1-A5, O1 |
| rd1015 at BASE, linux and own | 15 cells, failed exactly U1-U3, X1-X7, C1, C2 |
| rd835 at BASE, both shapes | 22 of 22 |
| at K, both shapes: rd1016, rd1015, rd835, rd778 | 13/13, 15/15, 22/22, 17/17 |
| rd835 as at BASE, run against K's product (the before-turn proof) | failed exactly X1, X4, X5, X8, K3 |
| neighbours at K: the 35 of `neigh.txt` (cmp-equal to the seat's) plus the two new files | 37 suites, 516 tests, 0 failed; rd778 17/17 inside it (Tuesday's point (d)) |

**(3) The 14 mutations, my own program.** `tools/gmut.py` uses anchors I typed from K's diff, each asserted once. Before the lane I confirmed each of my 14 is BYTE-EQUAL to the frozen `mutate2143.py`'s mutant of the same name. Each was run in the Linux shape and judged on all three files. All 42 judgements read PASS, each red on exactly the kit's cells:

| Mutation | rd1016 | rd1015 | rd835 |
|---|---|---|---|
| b01 | E2, E3, A1-A5, O1 | - | - |
| b02 | E5 | - | - |
| b03 | E3, E4, A1-A5, K1 | - | - |
| b04 | E2, E4, K1 | - | - |
| b05 | - | U1, X1-X7 | - |
| b06 | - | U2, U3, X4, X5, K1-K3 | X1, X4, X5, X8, K3 |
| b07 | - | U2, K3 | - |
| b08 | - | X1, X2, C1 | - |
| b09 | - | X3, C1 | - |
| b10 | - | X4, C1 | - |
| b11 | - | X5, C1 | - |
| b12 | - | X6, C1 | - |
| b13 | - | X7, C1 | - |
| b14 | - | X6, C1 | - |

After every revert the blobs read 07c2d16b and b60cdd12.

**Six extra mutants of mine:**

| Mutant | Red cells |
|---|---|
| `String(text)` without `\|\| ''` | E5 |
| the dead first definition restored | E1 only (the kit's D6 limit; the runtime keeps the last) |
| the comparison without quote doubling | U2 |
| a narrower own pattern `/^[=@]/` | U1 |
| `.trim()` inside the helper | U1, U3 |
| also quote a value holding `, " CR LF` | U2, U3 (see Finding 1) |

**(4) Adversarial probe.** `adv/g2150-probe.test.js` ran under jest inside the same acquisition, 5 cells green, and wrote `out/probe/probe.json`.
- **settings.js escapeHtml, BASE's live definition against K's.** I tried 25 inputs: an array of objects, a nested array, a Symbol, an object whose `toString`, `valueOf` (with toString removed) or `Symbol.toPrimitive` returns markup, a Proxy with a toPrimitive trap, a Proxy of an array, a String object, an Error, a Date, a function, 0, -0, NaN, false, true, null, undefined, '', 0n, 7n and 12.5.
  - At K, every markup-bearing input comes out escaped: 0 unsafe outputs. At BASE, 10 were unsafe.
  - Every scalar prints identically at BASE and K: 0 and false give '', true gives 'true', 7n gives '7'.
  - A Proxy whose toPrimitive returns an object throws TypeError at BASE and at K alike, so no unescaped output is possible.
- **Sinks.** I fed each of the five sinks (suggestion, message, suggestions, saved id, quick message) an array of objects, a nested array, a Symbol and a Proxy: 0 img elements in all 20 runs.
- **Scope.** Babel scope analysis (script mode): both BASE definitions sit in Program scope, so the runtime keeps the last. At K there is one definition, and all 39 calls bind to it.
- **The other scripts on settings.html.** None of the ten other scripts the page loads defines `escapeHtml`: local-date, csp-helpers, mail-address, dark-mode, sustainability-ui/-mount, entra-provisioning-ui/-mount, feedback-widget, open-access-banner. So no later script replaces the fixed function at runtime.
- **csvNumberCell at K.**
  - `+1+1`, `-1+cmd`, `\t=1+1`, `\r=1+1`, `=1+1`, `@SUM(1)`, `-$1.20` and `--1` are prefixed.
  - `1e5`, `+1`, `-1` and `+1%` stay bare. A spreadsheet reads these as constants; no function can be called.
  - Raw, as before: ` =1+1`, `\n=1+1` and the three look-alikes (part (2)); `1,=1+1`, `1\n=1+1`, `1\r=1+1`, `"=1+1"`, `"=1+1`, `a"b` and `1;=1+1` (Finding 1).
- **Ordinary bytes.** I built 12527 ordinary values: integers -3 to 2500 as numbers, as strings and with en-US thousands commas, two-decimal figures, currency texts, '', '-', '--', 'N/A' and '0.00'. 0 of them changed.
- **Whole exports, fed ordinary rows** (zero, 999, 1000, 12345 and 1500 sheets; dash and decimal sizes; `1,234` and `$-1.00` risk cells): job history, scanning, anomalies and all-tabs are BYTE-EQUAL at BASE and K (590, 243, 214 and 1202 bytes).

**(5) Local CodeQL.** I used Tuesday's `pr_codeql_check.sh` (cli 2.27.4, javascript-security-extended), with the control first:
- **Control:** round 1's erasure K `6675c397` against BASE gave rc 1: KEPT/NEW js/file-system-race HIGH+ 7.7 in the rd745 test.
- **BASE against K `895da3f4`:** results head 29, base 29; KEPT 0, NEW 0, GONE 0; rc 0 PASS.
- **Main's SARIF** (analysis 2257151397; 29 results, 1648 locations including related and flow steps): 0 in `static/js/settings.js`, 0 in `static/js/index.js`, 0 under `static/`, 0 in the three test files (control: backend/server.js 346).
- **Tuesday's point (c).** No changed line sits on a data-flow path of the 22 open alerts, by SARIF and by the local run. The PR's CodeQL run stays the authority, and main's analysis at the merge commit is the check that can fail.

**(6) gitleaks 8.30.1** over `git log -p BASE..K` (32016 bytes, the three messages included) and over the three messages alone: `no leaks found`, rc 0 for each. Control: the same patch with a planted access-key-id line and secret line gave `leaks found: 2`, rc 1.

**(7) Name scan.** I used the frozen names2142.py (sha256 b0ae9573... as ADDENDUM-1 states): `names 4 found [True, True, True, True]`, rc 0, and the file was never printed.
- The underscore-aware pattern hit 0 of the 4 names in the patch and in the messages. Each name's planted `_by_<name>_` control fired.
- Who-decided and id words (product owner, ruling, ruled, Tuesday, Wednesday, seat, card, B2xxx, N18x, s33x): 0 (control fired).

## Findings (round 1 of 2)
**Finding 1: Major, does NOT block landing (pre-existing; not a regression).** A number cell that holds a comma, a leading double quote or a line break is still written raw. A CSV reader then sees a cell that begins with `=`.
- **What happens.** `csvNumberCell` hands back the raw text whenever `csvCell` would not prefix it. `csvCell`'s test reads only the FIRST character. So a text-fed cell can carry a working formula by structure instead of by its first character.
- **Measured at K.** I ran the real exports in jsdom and read the output with Python's `csv` reader:
  - `1,=1+1` gains a column whose cell is `=1+1` (job history, scanning, anomalies, all-tabs);
  - `"=1+1"` is read as a quoted field: the Sheets/Pages cell ITSELF is `=1+1`, with no prefix;
  - `1\n=1+1` starts a new row whose first cell is `=1+1`.
- **Reach.** The same sources the ticket worries about reach these cells: `job.totalSheetsUsed`, and table text rendered raw (`${scan.totalSheets || 0}`, `${anomaly.sheets}`, `${sheets.toLocaleString()}`). Whether outside text reaches them is NOT measured (as RD-1015 says). Whether Excel or LibreOffice evaluates the quoted field is UNMEASURED (no spreadsheet). RD-835's own design (a prefix INSIDE the quotes) assumes it does.
- **Why it is not a regression.** At BASE these eight cells were fully raw. Commit B's message claims exactly the leading-character shape, and that claim is true.
- **Why it exists.** It comes from the coordinator's Q-4 choice (bare unless formula-shaped). The ticket's own recommendation ("write the six cells through csvCell") would have closed it, but would quote every number.
- **The tests pin it.** U2 pins `1,234` and `a"b` as "as before". My mutant that also quotes a value holding `, " CR LF` turns only U2 and U3 red, so the fix is small and changes bytes only for rows that are already broken.
- **Disposition.** File it with Finding 2 as one new ticket (FOR-RECORDS). Tuesday may instead prefer a round 2 before RD-1015 part (1) is called met.

**Finding 2: Minor, does NOT block (pre-existing; Tuesday's point (b)).** The thousands-comma row split.
- At BASE, `index.js` lines 8903, 8953 and 9003 write `${sheets.toLocaleString()}`, and lines 5977 and 6145 write the anomalies cells raw. Blame on both names `9b58261f`, 2026-04-25. So it predates BASE, and is at least that old.
- Measured: an ordinary anomalies export with a `1,234` row reads data row widths 7, 7, 8, 7 under a 7-column header. It is byte-equal at BASE and K, as the kit says (U2 pins it).
- This is data integrity, not a security path on its own; with Finding 1, one fix closes both.

**Finding 3: Info (landing).** After PR 267 lands, this branch CONFLICTS on the counts file.
- `git merge-tree --write-tree --name-only 52040f2e 895da3f4` in my clone gives `CONFLICT (content): Merge conflict in scripts/verify-expected-counts.json`, rc 1, the only path.
- So "a new commit by Tuesday" must be a MERGE of main into the branch, resolved by regeneration. A commit on top of K cannot remove the conflict, and "Update branch" cannot resolve it.
- verify-suite.sh parses the file before `--update-counts` (lines 237-256) and fails on conflict markers. The resolution therefore writes main's file first, then regenerates.
- The expected pair is 6634 / 419 (PREDICTED). landing.txt step 0b spells it out, with the checks that keep the gate's reads valid: the five non-counts blobs at M2 equal K's, and diff M1..M2 = the six paths.

**Finding 4: Info.** The kit's "35 other callers" of `escapeHtml` in settings.js are 34 calls plus one comment line (line 3631 at K).
- Count: 41 occurrences at K = 1 definition + 39 calls (scope analysis) + 1 comment; 39 calls = 5 sinks + 34.
- All 34 write into HTML text or a double-quoted attribute (read from the listing). No unquoted `=${escapeHtml(` site exists.

## Tuesday's points
**(a) Q-6: right for every sink.**
- No sink receives a user-meaningful 0. suggestion, message and the quick message are strings, and suggestions is a string or an array.
- savedConditionId comes from `jsonStorage.addRiskCondition`, which starts ids at 1 (`backend/jsonStorage.js` line 3756: `... Math.max(...) + 1 : 1`).
- 0 and false wrote '' at BASE's live definition too, so nothing vanishes that showed before.
- Among the other 34 calls, no argument is numeric by reading.
- One inconsistency, out of scope: index.js's own `escapeHtml(0)` returns '0'.

**(b)** Finding 2: confirmed pre-existing, graded Minor.

**(c)** No changed line is on a data-flow path of the 22 open alerts (SARIF 0 locations; local CodeQL 0 new, with the control rc 1). The PR's CodeQL run is the authority.

**(d)** rd778 is green under jest: 17/17 at K in both shapes and inside the neighbour run.

## Three shapes outside each property
**(A) RD-1016:**
1. **The other 34 callers fed a non-string.**
   - Covered for the function: probe P1, where every scalar is identical and every array or object comes out escaped.
   - Named limit for the sites: they were read, not run. All are HTML or quoted-attribute contexts.
   - The visible text changes only for an array or object whose text holds markup. `& " '` display the same once escaped.
   - The validator's real arrays hold plain sentences with `"`, which display identically.
2. **A later script redefining the global `escapeHtml`:** covered by measurement. None of the ten other scripts on settings.html defines it.
3. **A conversion that throws (a Proxy returning an object):** covered by P1. TypeError at BASE and K alike; no output, so nothing unescaped.

**(B) RD-1015:**
1. **A comma, a leading quote or a line break in a cell:** NOT covered. This is Finding 1 (measured).
2. **A semicolon-separated reader** (spreadsheets in locales whose list separator is `;`): `1;=1+1` is raw. Named limit, UNMEASURED (no spreadsheet).
3. **`+1`, `-1`, `1e5`, `+1%` left bare:** covered by P3. They are numeric constants to a spreadsheet; `+1+1` and `-1+cmd` are prefixed.

## Named limits and NOT RUN
NOT RUN by the gate:
- The whole suite. I relay the seat's two runs: `VERDICT: PASS — 6558/6558 tests passed across 413 suites`, Linux shape at B and plain shape at K. The PR's hosted build is the authority.
- Any merge-of-main tree (step 0b is Tuesday's, after PR 267).
- Real Linux.
- A real browser and the dashboard's content security policy.
- A spreadsheet.
- Jira.

The seat's STATUS deviations were read: REFUSE 7's listeners, the one `git add` in the throwaway chk tree, and two early `cd`s, read-only. None bears on the head.

## Leftovers (never deleted)
- Under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/g2150/`:
  - the clone with four clean worktrees;
  - `t/mut-saved/` (my mutant program's saved originals);
  - `out/mtcheck*` (the anchor pre-checks);
  - `_quarantine/head-copies` and `_quarantine/base-newfiles` (the probe file, the BASE copy of rd835 and the two new-file copies, moved out of the trees after the lane).
- The `t/ctl` worktree briefly held a control edit. Its commit was refused for lack of a configured identity, and I never overrode the identity. I restored the file by copying K's blob, and porcelain reads 0.
- The control used instead was round 1's erasure K.
- No process and no lock remain.
