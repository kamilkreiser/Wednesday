GATE B1964: GO WITH FINDINGS @ 27d49f7 on main 3c3be15

Independent review, tier G1 (one Opus reader), round 1 of 2, no rendered leg. Lane NX-P (RD-1030), kit B1958, seat
N164. Branch `b1958/nexusai-nx-p-permission-table`, head K `27d49f706af3a29af5625626ead70afa383e9be1`, A
`9e348b22063ff3eaf502fd4d274b319345ac36ea`, BASE = main `3c3be156e8ea36ad297fdadd3055c6e00252ba38` (unmoved at
07:42 and 07:49).

Clocks (AEDT, 2026-11-23, from `date`): first read 07:42:27; jest lock ONE acquisition (`g1964-gate`, base
`session-tools/locks-laptop-1017`, queue empty, "acquired after 0s") 07:47:09 to 07:48:01; CodeQL after the lock;
written 07:50.

Trees: `git clone --no-hardlinks --no-checkout` of the seat's clone `.tools/b1958/clone` (read verbs only toward it;
push URL set to `invalid://no-push`) under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/g1964/`;
K's tree `de159e84...` and parents equal GitHub's by `gh api` GET. `git archive` extracts of BASE, K and BASE+frozen
program (`arch/`); worktrees `t/r1` (BASE + `apply1958.py tests`, slot 0), `t/h1` (K, slot 12), `t/m1` (K, plants,
slot 4), slots by the project's own `worktreeSlot()` formula. `node_modules` a symlink to the seat clone's (lockfile
blob `2d7dbece2ecd` at BASE = K = the seat clone's). Node v24.22.2 first on PATH, `NODE_OPTIONS`, `MIN_TESTS`,
`MIN_SUITES`, `VERIFY_EXPECTED_FILE` unset. Nothing written in the project but the lock queue's own files.

Blocker 0 | Major 0 | Minor 0 | Info 8

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| Info | **I-1. Only the viewer is pinned not to hold `admin.read`.** P2 asserts `ROLE_CAPABILITIES.viewer` lacks `admin.read`; C-OPP and C-CTL read the viewer only. My probe Q2 (`print_operations: [...READS_TODAY, 'admin.read']`) leaves all 42 cells of the plant set GREEN. At the head only `admin` holds `admin.read` (every role's list read by program), and the five proposed roles are not accepted by the user store, so no wire effect today. | None for landing. RD-929's wiring matrix (every route x role) is where a per-role pin belongs; named in FOR-RECORDS.md and the PR body. |
| Info | **I-2. The move also takes the two reads from the five proposed roles** that hold `READS_TODAY` (print_operations, finance, security, executive, department_manager): `decide(enforced)` allows `[admin, viewer, + those five]` at BASE and `[admin]` at the head. That is what "administrator-only" (C-311) means for them, and Q3's "today's viewer keeps what it can read" is not broken (the viewer was already refused on the wire). | Note for the Roles UI design (FOR-RECORDS.md). |
| Info | **I-3. Sign-in-unproven mode (RD-535).** `decide({mode:'unproven', role:'viewer'})` on the two reads goes `allow` -> `forbidden` (reads follow the enforced rules). The inventory has no unproven column, and I did not measure what `requireAdminFor` answers a viewer in that mode. The direction is the stricter one. | None; NOT TESTED below. |
| Info | **I-4. Both commit messages carry a `Co-Authored-By: Claude Sonnet 5.5` trailer after the frozen text.** By program: message A == `msg-A.txt` + the trailer, message K == `msg-K.txt` with `@T@`=6237, `@S@`=394 + the trailer (control: A without the trailer reads unequal). The kit says "never reword"; the trailer is the session's attribution rule, disclosed in STATUS COMMITS, and B1942's lane commits carry the same form. | None. |
| Info | **I-5. The seat's STATUS has three clerical faults.** Its first line reads "final 07:50 AEDT" but the file's mtime is 07:40:20 and I read it at 07:42; Step 0 says "I printed no lines of [CLARIFICATIONS.md] this session" while Correction 5 says it printed them after the pre-lock STATUS; Correction 1 is an `rm -f` of its own 1.5 KB scratch copy (rule: quarantine). No product effect: every number I re-measured equals the STATUS. | None. |
| Info | **I-6. LEFT FOR OTHERS 1 and 2 are now slightly stale text, as the kit says.** `capabilities.js:96` `admin.read` about text names no data-source read; the RD-1011 header (lines 9-10) still calls refusing all four the coordinator's default, now true only of the two TEST routes. Also pre-existing: the table header says "the 205 routes" where table and inventory hold 203. | Records items (FOR-RECORDS.md). |
| Info | **I-7. The cells divide the pins correctly.** P2 and the table comment are the two HOLD 47 citations; the message of A is the third. My probe Q1 (both rows under `tenant.write`, a capability the viewer also lacks) reds P2 alone, so P2 is what pins the destination `admin.read` (the coordinator's default) and C-OPP pins only "not viewer-held": correct division. | None. |
| Info | **I-8 (gate's own process).** One `grep -r` was refused by the recursive-scope hook; I re-ran it scoped to `__tests__/helpers` with `--include='*.js'`, the form the hook names. One `git log` format line printed the commits' configured author address (a GitHub noreply address, not a secret) into my own output; it appears in no file of this folder. | None. |

## WHAT WAS MEASURED

### Scope and text (item 1)
- `gh api compare main...b1958/...` (07:42): `ahead`, ahead 2, behind 0, merge base `3c3be156` = main; commits A
  (parent BASE) and K (parent A); exactly 4 files: RD-1011 test +4 -2, census test +20 -0, `capabilities.js` +5 -2,
  counts +2 -2. 0 open pull requests; `matching-refs`: the branch at `27d49f70`, main at `3c3be156`.
- Frozen text: the six fenced files extracted by program from the kit (`progs/extract.py`) are byte-equal (sha256) to
  the seat's `.tools/b1958/frozen/` copies (apply `f0f9234984db`, plants `f6e569d8d1ae`, runlist `45516db3cdaf`,
  opp `88bab7af812b`, msg-A `c05167086870`, msg-K `c88dba1cd71b`). `apply1958.py all` on a BASE extract printed the
  three `applied` lines (18704->18956, 14362->14576, 5522->6898) and the three blobs equal A's and K's
  (`8c0da99119fe`, `e2d5ab0035de`, `99d2d5faaa01`; control: one appended byte reads DIFFERENT). `diff -r` of that
  extract against K's extract: only `scripts/verify-expected-counts.json` differs, which moves exactly `_updated`
  (`2026-11-22T20:15:23.513Z`) and `tests` 6235 -> 6237; `suites` 394.
- The table diff is exactly two hunks: the two rows leave lines 155-156 (the line-156 sibling `GET /api/debug/data-sources`
  stays, alone on its line) and join the end of `admin.read` under the frozen two-line comment.
- Text scans over the 31 added lines and both messages (`progs/textscan.py`, every pattern with a control that fires):
  owner attribution (`product owner|owner's ruling|ruled by|decided by`): **exactly 2** added (the table comment, P2's
  title), **exactly 1** in A's message, 0 in K and its message (HOLD 47); "owner chose/picked/decided ... admin.read /
  capability / placement": 0 (HOLD 48; control fires); B-number/seat ids 0; decision-queue/card ids 0, the word "card"
  0; person names 0 (the project scanner's alternatives plus the gh login, read as text, values not printed; each
  alternative planted fires); non-ASCII added 0 / removed 0; bidi/zero-width 0; `new RegExp(`, `eval(`,
  `new Function(`, `child_process`, timers, `.only(`/`.skip(` 0; CR 0. A's message says the existing capability is "a
  default, not a decision on a new one"; nothing says the product owner chose `admin.read` or the placement.

### Attack (item 2; `progs/attack.js` over the BASE and K extracts)
- **Readers of the table at the head:** pattern `services/capabilities|require(...capabilities)|ROUTE_CAPABILITY|ROLE_CAPABILITIES|PENDING_GATE|OWN_CALLER_CHECK|WRITE_SPLIT_PROPOSED`
  over every file, the table itself excluded: `backend/` 100 files 0 hits, `static/` 65 files 0, `scripts/` 84 files 0,
  `tests/` 49 files 0, `.github/` 6 files 0, root-level js 0. **Positive control:** `__tests__/` 457 files, exactly the
  6 the kit names (rd1011, rd691, rd793, rd929, rd958-viewer-write-gates, rd988), none under `__tests__/helpers/`; the
  pattern fires on a planted `require('../backend/services/capabilities')` and not on `const x = 1;`. The inventory
  generator `scripts/role-capability-inventory.js` requires only `fs os path crypto child_process`, the seed helper,
  `rd395-server-harness.js` and `test-server.js`; none reads the table.
- **Every role's capability list at the head:** `admin.read` is held by `["admin"]` only (BASE the same);
  `config.read` by admin, viewer and the five proposed roles; end_user and the two partner roles hold neither. Only
  `ROUTE_CAPABILITY` changed among the exports (`ROLES`, `CAPABILITIES`, `ROLE_CAPABILITIES`,
  `WRITE_SPLIT_PROPOSED`, `PENDING_GATE`, `OWN_CALLER_CHECK` JSON-equal BASE vs head; control: `ROUTE_CAPABILITY`
  reads unequal). Table 203 rows at both, the same key set; **changed rows exactly 2**: describe-table and
  discover-tables `config.read -> admin.read`.
- **Sibling rows untouched:** `GET /api/debug/data-sources` (RD-1021, inventory viewer 200), `GET /api/setup/data-sources`,
  `/setup/discover-tables`, `/setup/schema`, `/setup/expected-columns`, `/setup/column-mapping`, `/setup/domain`,
  `/setup/mail-config` all `config.read -> config.read`.
- **The inventory:** `git diff --stat BASE K -- docs/ scripts/role-capability-inventory.js backend/server.js static/`
  empty. It should not move: it records the wire (statuses by HTTP), the wire is unchanged, and the generator does not
  read the table. `opp.js` (frozen): BASE `tableRows 203, inventoryRows 203, viewer403 79, viewerHeldBy403 2`, bad =
  exactly the two keys `-> config.read`; head `viewerHeldBy403 0`; control `viewer200 rows 71` at both.
- **The wire at the head:** `backend/server.js:15991` and `:16060` register the two handlers; their first statement
  (`:15994`, `:16063`, after a two-line RD-1011 comment) is `if (!(await requireAdminFor(req, res))) return;`;
  `requireAdminFor` (`:19106`) answers 403 when `adminGateRefuses(...)` says so (setup-mode aware).
- **The later wiring (RD-929):** for every inventory row I compared `decide()` with the committed status for the
  viewer, the administrator, no session (enforced) and the open window (own-credential routes excepted). Viewer
  disagreements BASE 13 -> head 11: **resolved exactly the two rows (wire 403, table allow), introduced 0.** The 11 left
  are the 10 `PENDING_GATE.L1` writes and the 1 `OWN_CALLER_CHECK` route, each listed. Administrator 0 -> 0, no session
  4 -> 4, open 16 -> 16, none changed. So the wired table would give a viewer a 403 on these two routes exactly where the
  wire already refuses, and nowhere new.
- **C-OPP and C-CTL:** C-OPP reads RED at BASE+tests on exactly the two keys (below) and GREEN at head; C-CTL is GREEN
  at BASE by design (synthetic table) and is proven able to fail by plant M4 (received all 79 viewer-403 keys) and by my probe Q3
  (its 403 precondition fails).

### Jest (item 3; one lock acquisition; colours from the JSON `assertionResults` by title; `progs/chain.py`)
Every run by absolute path with `--runTestsByPath`, `--maxWorkers=2`, own `--cacheDirectory`; `numTotalTestSuites` =
paths passed every run; `EADDRINUSE` 0 every run; the tree's band (20000 + 640 x slot) had 0 listeners before and
after every run (machine-wide control 11 listeners).
| run | tree | cells | result |
|---|---|---|---|
| red-first | r1: BASE + `apply1958.py tests` (porcelain ` M` x2) | 36 (27 + 9) | **2 RED, 34 GREEN**: C-OPP received exactly `describe-table`, `discover-tables`; P2 received `config.read`, `config.read`. C-CTL GREEN. |
| green-1, green-2 | h1 = K | 36, 36 | 36 of 36 GREEN, twice |
| run list | h1 = K, `runlist1958.py` (frame 394 files, 21 listed, the kit's 21) | **284** | 284 of 284 GREEN; census 9, RD-1011 27, the other 19 files 248 (per-file counts in `raw/results.json`) |
| P0 | m1 = K, plant set (RD-1011, census, roles-foundation-route-census) | 42 | 0 red |

Plants (the kit's `plants1958.py`, asserted matches; then my probes; each reverted by copying back the saved original,
blobs of table, inventory and both test files proved equal to K's and porcelain empty after every one):
| plant | change | RED received | kit predicted |
|---|---|---|---|
| M1 | describe-table back under config.read | C-OPP (that one key), P2 | same |
| M2 | both rows back where BASE had them | C-OPP (both keys), P2 | same |
| M3 | debug sibling moved to admin.read | census PENDING_GATE cell only | same |
| M4 | viewer given admin.read | C-OPP (the 17 `admin.read` rows), C-CTL (all 79 viewer-403 rows), P2 (`not.toContain`) | same |
| M5 | describe-table dropped | census table-complete, dropped-row, PENDING_GATE; P2 | same |
| **Q1 (mine)** | both rows under `tenant.write` instead | P2 only | (probe) P2 pins `admin.read`; C-OPP pins "not viewer-held" |
| **Q2 (mine)** | `print_operations` given admin.read | **none** (42 green) | (probe) I-1 |
| **Q3 (mine)** | inventory JSON: describe-table viewer 403 -> 200 | roles-foundation C5 (page vs JSON), census PENDING_GATE, C-CTL (403 precondition), RD-1011 I2 | (probe) an inventory drift is caught four ways |

**Full verify: NOT run by the gate** (not required by the commission). The seat's step 6 (`--update-counts` in `vupd1`
at A, VERDICT PASS 6237/6237, 394 suites, 23 min) and step 8 (plain verify at K, PASS 6237/6237, 394 suites, 22 min,
porcelain empty, `EADDRINUSE` 0) are RELAYED from its STATUS. The committed pair 6237/394 = BASE 6235/394 + the two
census cells, which my per-file counts confirm (census 7 -> 9, the other 20 run-list files equal).

### CodeQL (item 4)
`pr_codeql_check.sh --repo datasecau/Reporting_Dashboard_Au --checkout <my scratch clone> --base 3c3be156e8ea36ad297fdadd3055c6e00252ba38 --head 27d49f706af3a29af5625626ead70afa383e9be1 --lang javascript --work <scratch>/cq/run1 --threads 4`,
one CodeQL process, after the lock was released: **rc=0** (CLI 2.27.4; "diff pack: 4 files with added lines, 5 ranges").
```
VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
  results   head 29   base 29
  KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
  NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
  GONE      total 0
  RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
```
Equal to the seat's CQ run. Open code-scanning alerts on main: 22 (13 `backend/server.js`, 2 each `incidents.js`,
`jsonStorage.js`, `routes/entraProvisioning.js`, `services/emailService.js`, 1 `tests/uat-run.js`), none in a lane
path (GET 07:48). A local approximation; the hosted CodeQL on the PR and the merge commit is the authority.

### Gitleaks
gitleaks over `3c3be156..27d49f70` in my clone (2 commits): no leaks, rc 0. Control: a planted AKIA-shaped pair in a
scratch folder reports a finding (rc 1).

### Records at source (`awk NR`, the project's CLARIFICATIONS.md, never read whole)
C-190 lines 2062-2067 ("Never squash, never rebase"); C-224 line 2412 (no NexusAI demo deploy until RD-876 part 2);
C-311 line 3148 (the 2026-11-20 ruling: "Keep both reads administrator-only") and line 3151 (its point (1) names this
table change as owed); C-312 line 3158 (PR 240's record). The decision-record detail quoted in the commission was not
re-read by me (Tuesday's print, relayed).

## LANDING TEXTS (item 5)
`landing.txt` (head-pinned MERGE COMMIT, never squash (C-190); `pr_checks_wait.sh ... --min-checks 7`, the 7 names /
8 runs read from PR 240's head; hosted counts 6237/394; no new alert against main's 22; Deploy demo run: build and
deploy jobs both must read skipped, `deploy-demo.yml:29-32` ignores only `**.md`, `docs/**`, `tests/**`, jobs gated at
:53 and :91, last three runs on main skipped, newest jobs `build skipped`, `deploy skipped`), `merge-subject.txt`
(`(#PRNUM)` placeholder), `merge-body.txt`, `pr-title.txt`, `pr-body.md`, `FOR-RECORDS.md` (RD-1030's state, the two
LEFT FOR OTHERS items, the RD-1011 header comment quoted). Who decided: the coordinator's defaults, except the
2026-11-20 ruling cited by date and C-311. Scans (`progs/landscan.py`, controls fire): pr-title, pr-body, merge texts
carry 0 names, 0 B-numbers/seat ids, 0 card ids, **0 owner-attribution phrases**, 0 bidi, no address but the merge
body's Co-Authored-By line, no non-ASCII but the pr-body's robot mark. `landing.txt` and `FOR-RECORDS.md` are internal
and carry the gate id and branch name by design; FOR-RECORDS' 2 owner-phrase hits are the quoted RD-1011 header.

## FOUND / TESTED / NOT TESTED
**FOUND:** no Blocker, Major or Minor; I-1 to I-8 (Info).
**TESTED:** scope, commits, trees and parents against GitHub; the frozen program and messages byte-equal to the kit; the
text scans (HOLD 47/48, names, ids, non-ASCII); readers of the table with a positive control; every role's capability
list; every export; the sibling rows; the inventory and its generator; the wire's two handlers; the table-vs-wire
comparison for four callers over all 203 rows at BASE and head; red-first, green twice, the 21-file run list; the kit's
five plants and three probes of mine; CodeQL; gitleaks.
**NOT TESTED:** a full verify (relayed from the seat's steps 6 and 8); sign-in-unproven mode on the wire (I-3); Linux;
Jira (not read; RD-1030's state is relayed from the kit STAMP); the hosted Build and CodeQL on the PR and merge commit;
the later wiring of the table (RD-929); the Deploy demo run a landing starts.
**HOW:** read this commission, the kit (352 lines, two pages), the drafter report (72 lines) and the seat's STATUS (122
lines) whole; B1942's verify folder for the landing form; GitHub GET only under the NexusAI `GH_CONFIG_DIR`; nothing
pushed, opened, merged, re-run or deployed; nothing sent to any human; nothing of HPSM-POC; nothing deleted.
