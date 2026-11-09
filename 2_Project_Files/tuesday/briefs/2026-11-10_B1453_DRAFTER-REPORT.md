STARTABLE: YES

# B1453 DRAFTER REPORT (seat G377, HPSM-POC tier-2 gate of the L4 CI and tooling builder branch)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1453_SEAT-G377_hpsmpoc-ci-tooling-gate.md`, 79 lines. Tier 2, Sonnet. Branch `b1395/hpsmpoc-ci-tooling` @ `0cdfc74e`, cut from `fa401da9`, judged on main `884fd72b`, on M1 (main + branch) and on M-ALL (M1 + b1392-d + b1392 + b1393).

Drafted 04:42-04:53 AEDT 2026-11-10 (`date`). Refs re-read at 04:52:25 and unchanged. One change since the first read: PR 298 is now open, on b1393 (another lane, 0 overlap). The kit records it.

## BLUF
- **The kit is startable.** The branch shares 0 paths with main's PR 297 move and with each of b1393, b1392, b1392-d and b1394.
- **It touches no `.github/` path.** All 5 changed files are test or spec files that L4 owns. Step 2 still proves by program that no job's run or predicate changes: blob equality across 5 trees, a job-predicate extract hash with two controls, and a count of the three line-break characters in ci.yml.
- **There is one real coupling that is not in the paths.** L1's b1392 rewrites the mock's customer-name guard (`customer-detail.ts`), which is exactly what this branch's mock rows and the Xm12b mutant test. After b1392 lands, the Xm12b anchor (`b.name === held) return null;`) no longer exists.
  - That is why the kit builds M-ALL.
  - On M-ALL it runs the mock rows and plants Xm12b in L1's new `hiddenName`.
- **Two tools the kit needs are missing on this machine:** shellcheck and pytest. The kit has the seat install both locally:
  - shellcheck 0.11.0 from the GitHub release asset, with its sha256 pinned to the digest GitHub lists;
  - pytest into a seat venv from PyPI.
- **Ports 9570-9579.** Free by `lsof`, by a word scan and by a range scan, each with a control that fired.

## FACTS RE-MEASURED (instrument and control)
- **Refs** (`gh api -X GET git/ref/heads/...`, 04:42:22 and 04:52:25):
  - main `884fd72b238ec8dc0d566b0e9c18b5362f920a2b`
  - b1395 `0cdfc74e32e9e68f93c1876de36d19b50f24e794`
  - b1393 `d7df877a`, b1392 `121ee236`, b1392-d `aca2290c`, b1394 `c0a5fa17`
  - Open PRs: 0 at 04:42, then 1 at 04:52 (PR 298, b1393, 3 files). Control: the closed list showed 297, 296, 295; `pulls/99999` rc 1.
- **Compares** (`compare/` JSON):
  - fa401da9...0cdfc74e: ahead 4, behind 0, 5 files, +209 -9.
  - 884fd72b...0cdfc74e: diverged, ahead 4, behind 1, base fa401da9.
  - Main's move: 16 files.
  - b1393: 3 files. b1392: 5 files. b1392-d: 2 files. b1394: 3 files (all api/).
- **Overlap** (`comm -12` of sorted lists): 0 with each of the five lists above. Control: a planted `web/src/lib/walkthrough.ts` against main's move counted 1. Parent directories shared:
  - `web/e2e` with main's move;
  - `web/src/server/mock` with b1392;
  - `api/tests/HpsmPoc.Api.Tests/Assessment` with b1394.
- **The 5 changed files are blob-identical at fa401da9 and 884fd72** (raw by `gh api contents`, `cmp`, 5 of 5). So are the cited CLOSED files, plus `customer-detail.ts` and `Requests.cs`: 0 of 7 are in main's move (`comm`).
- **Commit messages:** 4 commits, 0 non-ASCII lines, 0 `B<digits>`, 1 Opus 5.5 trailer each. Control: a planted U+200B counted 1. Added lines: 209, of which 0 are non-ASCII, 5 carry a `B<digits>` comment and 4 a ticket key. Commit 7d04c76d's message describes only the 356 change; the builder disclosed this.
- **CLOSED lines:** 5 (`grep -c '^CLOSED-WITH-EVIDENCE '`; control `-i 'closed-with-evidence hpsmpoc'` also gave 5). Each has 4 fields by `awk -F' [|] '` (5 of 5).
  - The cited lines re-printed at 884fd72 land on the named constructs: `Hpsmpoc178...cs:579`, `customer-name.test.ts:373`, `e2e-runner.test.ts:132,135,939,216,220`, `e2e.mjs:96`, `test_ci_workflow.py:388-389,412,431,339,789,792-793`.
  - I did not grade the claims.
- **X12b / Xm12b definitions:**
  - Source: B622 STATUS:8 and B683 STATUS:56 (literal X12b edit), B683:59 (X12b on its branch: 3 red of 108).
  - The anchor `Requests.cs:146` is printed at 884fd72.
  - The Xm12b anchor `b.name === held) return null;` is at `customer-detail.ts:58` (count 1). In b1392's diff, that line is replaced by `hiddenName`, which ends `b.name !== held;`.
- **CI** (`ci.yml` at 884fd72, 682 lines, `grep -n`): every line number in the kit's FACTS was printed. The `infra` job is at `:578-630`.
  - `validate.sh:21` runs `tests/test_security_baseline.py`.
  - That file loads every `infra/tests/test_*.py` (`:2856-2858`) at verbosity 2, so the new `WorkflowLineModel` row runs inside the CI predicate by name. The kit has the seat prove this.
  - `validate.sh:22-24` has an `az` path when `WHATIF=1`, so the kit pins `WHATIF=0`.
- **Main's hosted CI at 884fd72** (`gh api -X GET commits/.../check-runs`): 22 runs, 21 success, dependency review skipped (push).
- **ci.yml line-break characters** (python count): 0 of U+0085, U+2028 and U+2029, and 2 other non-ASCII characters.
- **Tools:**
  - Present: Node 24.21.0; dotnet 10.0.402; bicep 0.47.16 (= ci.yml); gitleaks 8.30.1 (= ci.yml); python3.14 and `.tools/venv` 3.14.10.
  - Missing: shellcheck (`which` empty); pytest (import fails in venv, 3.14 and 3.9).
  - `uname -m` arm64. The shellcheck darwin.aarch64 tar.gz digest is `339b930f...` (`gh api -X GET` releases/tags/v0.11.0). Control: the same listing gives linux.x86_64 as `b7af85e4...`, equal to ci.yml `:590`.
- **Ports 9570-9579:**
  - `lsof`: 0 rows. Control: all listeners gave 16.
  - Scanned set: 55 non-`.pre-` SEAT kits of 9 and 10 Nov.
  - Word scan `957[0-9]` over that set: 0 hits. Control `959[0-9]`: 2.
  - Range scan over every `NNNN-NNNN`: 0 hits. Control (9590-9599): hit B1375 and B1376.
  - 9940-9999 and 9680-9699 were excluded as you said. Every block from 9600 to 9939 had at least one kit hit.
- **Round loop** (175 `GATE VERDICT` first lines):
  - Narrow pattern `b1395|ci-tooling|ci and tooling`: 0 hits. Control "a new sign-in entry point": B1385 and B1390.
  - Broad pattern: 7 hits (B478, B693, B734, B833, B868, B1301, B1306). B734 is the capped class (round 2 of 2, GO WITH FINDINGS) whose residues B734-6 and B734-9 this branch answers.
- **Model row:** `model-routing.md:109` G2 (`awk NR==109`). Model id `claude-sonnet-5-5` at `models_latest.json:23`.
- **Landing rule:** CLARIFICATIONS.md (5799 lines) `:3617` "The landing form is a head-pinned squash" (`grep -n -i`).
- **Kit hygiene:**
  - Four-underscore lines: 5 (S1-S4 and READ-WHOLE).
  - `@VAR@`: 0.
  - Non-ASCII lines: 0, after a fix (see the disclosure). Control: a planted U+200B counted 1.
  - Card ids: 0.
  - Underscore-aware name scan: 0 hits over 3 candidate first names drawn from the project's CLAUDE.md and JIRA.md (list sha256 prefix 5550be7b1c71). Control: `_by_<name>_` counted 1. The candidate list is small, so the seat repeats the scan with its own list.

## D-DECISIONS (taken in the kit)
- **D1 Tier G2, Sonnet** (`model-routing.md:109`): tests, spec and tooling only, on mechanisms earlier gates measured (B478, B622, B693, B734). Escalation to G1 is on a security-shaped finding. A workflow-predicate change is a STOP, not a verdict.
- **D2 Ports 9570-9579**, the first block below 9600 with 0 kit hits and 0 listeners.
- **D3 Merges:**
  - M1 = main + this branch.
  - M-ALL = M1 + b1392-d + b1392 + b1393, in the landing order their kits assume.
  - b1394 is still building, so it gets overlap only.
  - The Api and infra trees of M-ALL are proven equal to M1's, so the dotnet and infra runs at M1 stand for M-ALL.
- **D4 X12b and Xm12b at four trees** (main, head, M1, M-ALL). Survival anywhere is a Major. On M-ALL, Xm12b moves to L1's `hiddenName`, and the unplanted mock rows must stay green there.
- **D5 Load race: interleaved OLD/NEW pairs**, at least 5 each, same build, `--workers=12 --retries=0`, with load1 printed.
  - No synthetic CPU burner, so other seats are not hurt.
  - OLD not reproducing is a Minor, not a pass of the red-without-fix.
  - The whole changed shards are also run 5 times at head, as the builder kit asked, plus once at main and once at M1, because PR 297 added specs that shift the shard halves.
- **D6 Seat-local tools:** shellcheck 0.11.0 from the GitHub release asset, sha256-pinned; pytest from PyPI into a seat venv. If either fails, that tool is NOT RUN, which is not a stop. `validate.sh` (unittest) remains CI's predicate. A pytest-only red is a Note.
- **D7 HARD STOP at Step 0 + 210 minutes; target verdict at +180.** The e2e load pairs (at least 20 runs), three web builds, four web-unit runs and the Api builds are the bulk; the template's +120 for one tier-2 branch was judged too short (DERIVED, not timed).
- **D8 SQL Server:** NOT RUN (no docker). The Api rows are in the `api-assessment` part (`ci.yml:251-252`). The seat writes a DERIVED reading of whether any row depends on a database string compare (rows send up to 20 trailing spaces, and SQL Server pads `=`). The hosted part is a landing condition.
- **D9 R-LOGO-3** (out of ticket, a path L4 owns) gets the same proof as follow-up (a), with its scope noted as a Note.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q1 Class and round.** Default: a NEW class, round 1 of 2, NO GO 0 of 2 before. The alternative is counting it as a round of B734's class, which is already at the cap, so a NO GO would need a decision card. S1 says which.
- **Q2 Tier.** Default: G2 Sonnet. Choose Opus only if you want the held-name rows treated as a G1 surface; B478 was tier 1 for the guard itself, but this branch adds tests only.
- **Q3 Tool downloads** (shellcheck release asset, pytest from PyPI) into `.tools/b1453/`. Default: yes. They are package or release feeds, not product hosts. Both are machine-local and seat-scoped, not the project's.
- **Q4 Landing order.** Default: b1392-d, b1392, b1393 (PR 298 is open now), then this branch, then b1394 after its own gate. Paths are disjoint, so any order is valid, and M-ALL is the common end tree.
- **Q5 The HELD B734-6 closed-shape lane, and 352 Done-when clause 2 (built rows vs "ruled or recorded as not wanted").** Default: neither is graded as a finding. The gate grades only "stated correctly". Both stay Tuesday's decisions for the records lane.
- **Q6 The squash message.** Default: the gate's squash-body must describe all four changes, because commit 7d04c76d's message omits the html-layout waits.

## UNMEASURED
- Which shard halves hold `html-layout.spec.ts` and `logon-logo-link.spec.ts` at 884fd72 and M1 (needs `playwright --list`; the builder's fa401da9 reading is RELAYED).
- Whether M1 and M-ALL are clean (needs `merge-tree --write-tree`, which is forbidden to the drafter). On paths, DERIVED: disjoint.
- Whether L1's `customerTextShape` keeps the mock rows' single-error list (DERIVED yes for names of 120 characters or fewer, not run).
- X12b at any tree.
- The new rows on SQL Server.
- Whether the old race reproduces at the seat's load.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Writes:** only the two files. Scratch reads (raw files, compare JSON, path lists) went to the session scratchpad.
- **Kit fix before finishing:** my Write tool turned the escapes `\u2028`, `\u2029` and `\u202E` in the kit text into raw characters (2 non-ASCII lines). I rewrote them as escape text with a python replace; the non-ASCII count is now 0, and the control fired.
- **GitHub reads:** all were `gh api -X GET` under the project's GH_CONFIG_DIR. One read went to a non-project public repo: `repos/koalaman/shellcheck/releases/tags/v0.11.0`, for the asset digest.
- **Other reads:** `brew info --json` on the shellcheck formula (local metadata, no install). `tmux list-panes` (read). `lsof` and `sysctl` (read).
- **Not done:** no git verb in any project repo, no `merge-tree`, no `cd`, no `decision_queue.sh`, no ledger read, no recursive grep in `0_Brain/learnings/`, no token printed.
- **Reads in other seats' records:** the B622, B683, B693 and B734 STATUS files and the B622 evidence folder were read for the mutant definitions, with read-only greps. The builder's `.tools/b1395/` was listed (directory names only), not read.
