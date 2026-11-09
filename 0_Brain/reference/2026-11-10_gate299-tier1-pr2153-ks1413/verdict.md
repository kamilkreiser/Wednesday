PR 2153: GO WITH NOTES

# Gate 299, tier 1 (Opus): PR 2153 (KS-1413, `start-local.sh` banner). Seat R 93rd round 2. RELAUNCH run.

| PR | head | verdict |
|---|---|---|
| 2153 | 7a061f5e3f017dc7e47d208636efe80bd82564b9 | GO WITH NOTES |

**This is a relaunch.** The first gate-299 session died with its coordinator seat at 08:57 AEDT and left nothing behind. This verdict was done from scratch.

**Pins.**
- Start (21:59:12Z, ls-remote): develop 07d4218e9776a5eced016f16330983c900e94fb3, PR 2153 7a061f5e3f017dc7e47d208636efe80bd82564b9.
- End (22:03:43Z, ls-remote): develop 07d4218e9776, PR 2153 7a061f5e3f01. The branch ref equals the PR ref.
- Both readings equal the commission's pins. **Develop has not moved since 07d4218e.** The merge below is computed onto that commit.

**Method.**
- I made a bare repo in this session's scratchpad (`.../scratchpad/g299/r.git`). Its `objects/info/alternates` points read-only at `worktrees/s-r90-base/.git/objects` (which holds both pins) and at the project's own object store. The project checkout itself does not have the PR objects.
- Inside !CODING I ran only ls-remote, show, log, cat-file and grep, plus reads of the alternates. I did no fetch, no worktree, no checkout and no write. Merge-tree, `git apply --cached` (into a scratch index) and `git archive` ran against the scratch GIT_DIR only.
- The tests ran on mini-trees (`scratchpad/g299/t/<name>`) holding the three files the suite reads: `Start_Up/start-secuura.sh`, `Blockchain/Dev/scripts/start-local.sh` and the test file.
- I posted nothing and mailed nothing. Nothing I print here is a credential value: the removed lines are shown masked, and the counts used the values only inside python, never echoed.
- One stray file of mine (`/tmp/x1`, a list of paths) was created by a redirect and removed by me. The scratch tree (1.6 MB) is left in place.

---

## BLUF
The commit does exactly what it says:
- Two literal `echo` lines inside `show_urls` change, and nothing else in `start-local.sh` changes.
- Under every env state, the banner now prints no Grafana or Admin value, and no other line of the script echoes a credential.
- The commit is byte-for-byte the held Spark patch at tree level.
- The three new cells are red-first and green at head, and my value-restoring mutants each redden exactly one named cell.

The notes:
- The guard is literal and matches `echo` lines only (G299-2153-1).
- The READY's census sentence is not supported by its own census record (G299-2153-2).
- The PR body mislabels the ticket's priority (G299-2153-3).

Nothing blocks.

## FOUND / TESTED / HOW

### 1. Touched set (Q1)
The diff d0b4825c..7a061f5e is exactly 2 files:
- `Blockchain/Dev/scripts/start-local.sh`: +2 -2, at lines 280 and 286. File mode is 100755 at both ends.
- `Blockchain/Dev/scripts/__tests__/ks1413_start_banners_print_no_demo_password.test.sh`: +11 -0. This file is MODIFIED; it already existed at base with 4 cells.

There is one commit. Its parent is d0b4825cc244.

**Held Spark patch.**
- I extracted the fence (lines 29 to 66) of `READY_KS-1413-KS-1413-O120-P1_spark-dsv4flash_..._2026-11-09.diff.md`: 2,321 B, sha256 6ce6cde2616553c0... This equals the canonical prefix the READY names, and it is byte-equal (`cmp`) to the seat's `evidence/row4/held.patch` and `fence.diff`.
- `git apply --cached --check -p1` onto d0b4825c in a scratch index gives rc 0, so it is **STRICT**: no `--recount` or `--ignore-whitespace` needed. The seat's claim holds.
- The apply gives tree c08992fbf93c6cf3dfe04fb2483c04449a495759, which **equals the PR head tree** and the Spark run's own golden tree. That is stronger than hunk-for-hunk.
- The `+`/`-` change lines, in order, are identical between the fence and `git diff base head`.

**Every byte that differs** between the held fence and the commit's diff is metadata only (G299-2153-5):
- **File order.** The fence lists `start-local.sh` first. Git lists `__tests__/...test.sh` first.
- **Missing header lines.** The fence has no `diff --git` line and no `index b765e5297..a7590df68 100644` or `index 187a94fb5..be8d6343b 100755` lines.
- **Hunk-header context.** The fence's hunk headers carry no function context. Git's carry ` show_urls() {` after `@@ -277,13 +277,13 @@`, and ` check "start-secuura.sh echoes no demo password value" "0" "$(echoed_secret "$ST` after `@@ -44,6 +44,17 @@`.

The fence has no CR, and both end with LF. No content byte differs.

### 2. The banner prints no value in any branch, and no other line prints one (Q2)
**The removed lines were literals.** They contained no variable (0 `$` expansions in them; the shape is `echo "    Grafana: http://localhost:6300 (<user>/<value>)"` and `echo "    Admin:   <email> / <value>"`). So "default/overridden/missing/empty" cannot change what those two lines print. I measured it anyway:
- I extracted `show_urls` from base, head and head-merged-on-develop and ran it in bash under 4 env states for 8 credential variables (`GRAFANA_ADMIN_PASSWORD`, `GF_SECURITY_ADMIN_PASSWORD`, `GRAFANA_PASSWORD`, `DEFAULT_GRAFANA_PASSWORD`, `ADMIN_USER_PASSWORD`, `BOOTSTRAP_ADMIN_PASSWORD`, `ADMIN_PASSWORD`, `DEFAULT_ADMIN_PASSWORD`):
  - **missing**: all unset.
  - **empty**: all set to "".
  - **default**: set to the repo's local default values.
  - **overridden**: each set to a distinct `SENTINEL_G299_<i>`.
- Predicate: a line counts if it contains either removed value token or the sentinel prefix.

  | Version | Lines printed | Value-bearing lines (all 4 states) |
  |---|---|---|
  | base | 42 | 2 |
  | head | 42 | 0 |
  | merged | 42 | 0 |

- rc was 0 in every run. Positive control: of 3 planted lines (a value line, a sentinel line and a clean line), the predicate reads 2.

**No other line of start-local.sh prints a value.**
- I grepped the whole head script (339 lines, case-insensitive) for pass|secret|grafana|admin|GF_|token|cred|key and the three literal default values. The only echo hits are the URL and label lines (252, 265, 269, 280, 283, 285, 286) and the KS-731/KS-762 warnings, which name variables but expand none.
- Every `echo`/`printf` that expands a `$` expands only colour codes, port variables (`GW`, `WEB`, `POSTGRES_EXTERNAL_PORT`, `REDIS_EXTERNAL_PORT`) or `$0`.
- There is no `set -x`, no `cat .env`, and no `env` dump.
- `source .env` (line 103) and `source stack_env.sh` (line 130) print nothing from this script. The child checkers it calls (`check-slot-credentials.sh`, `check-app-db-password-default.sh`) were not in scope and are unchanged.

### 3. Guard cells and mutants (Q3)

| Tree | Result |
|---|---|
| base (4 cells) | 4 pass |
| base + new test (red-first) | 5 pass, **2 FAIL**: "echoes no Grafana password value" and "echoes no admin password value". Control cell 4 is green. |
| head | 7 pass, 0 FAIL |
| head merged onto develop 07d4218e | 7 pass, 0 FAIL |

On these 3 files develop is byte-equal to base, which I checked with `cmp`.

**My own mutants** of head `start-local.sh`, one at a time. `bash -n` passed on every one.

| Mutant | Change | Result |
|---|---|---|
| M1 | restore the removed Grafana value line | exactly cell 5 ("no Grafana password value") red |
| M2 | restore the removed Admin value line | exactly cell 6 ("no admin password value") red |
| M6 | Grafana value printed reworded (`login: <user> pw <value>`) | cell 5 red |
| M8 | Grafana value line with tab indent and a double space after `echo` | cell 5 red |
| M3 | Grafana value line via `printf` instead of `echo` | **all green** (G299-2153-1) |
| M4 | Admin value line via `printf` | **all green** |
| M5 | Admin value reworded as `admin@secuura.com  (password: <value>)` (no `/`) | **all green** |
| M7 | Grafana value assigned to a variable, then `echo "$_gp"` | **all green** |

The red-first tree is M1+M2 together, and both cells go red there.

### 4. No other behaviour changed (Q4)
- Base and head `start-local.sh` are byte-identical outside lines 280 and 286 (diff of lines 1-279, 281-285 and 287-339: identical). The line count is 339 at both ends, and the mode is 100755 at both ends.
- Both changed lines are still a single `echo "<literal>"` inside `show_urls`. No variable, condition, command or exit path changed.
- The Issuer line (285) is untouched.
- The extracted banner still prints 42 lines.

### 5. Merge (commission)
- `git merge-tree --write-tree 07d4218e 7a061f5e` (in the scratch GIT_DIR) gives rc 0, tree 71d1765d18ec.
- `diff develop..merged` is byte-equal to `diff base..head`.
- Develop moved since the PR's base by 0d286210 (KS-2134, one auth test file) and 07d4218e (KS-2138, one cheat-fragment HTML). That is **0 shared paths** with this PR. Control: the PR against itself gives 2.

### 6. Words (Q5)
I compared the posted texts with the seat's records:
- **Body.** The PR record's body_sha1 541f937c94b3 equals the sha1 of the stripped `push/pr_body_ks1413.final.md`.
- **Ticket comment.** Comment 72845754's body_sha1 44b44f76323d equals the sha1 of the stripped `push/linear_comment_ks1413.md`.
- **Commit message.** It equals `push/commit_msg_ks1413.txt`, apart from git's trailing newline.

Closing words:
- 0 closing keyword + key in the title, the body, the commit or the comment. Control: `Closes KS-1413` planted reads 1. `Refs KS-1413` appears once in the title, the body and the commit.
- The only bare hits are "closing banner" (body and commit) and "partial fix of acceptance line 1" (comment). Neither is in closing form.

Values: 0 hits of any of the three literal default values in the title, body, commit or comment.

Claims checked against source:
- The `start-secuura.sh` lines 603 and 614 at head are `curl -d` login bodies, not echoes. That script has 0 echo/printf lines carrying a value.
- `repro.sh` line 143 (`Blockchain/Dev/systemTest/cross-tenant-isolation/repro.sh`) is the failure-path echo the body describes.
- `check-no-default-passwords.sh` line 28 greps `*.ts`, `*.tsx` and `*.js` only.
- The words in the new lines are the held patch's.
- "No variable, condition, command or exit code changes": true (item 4).
- The hook block is quoted as INCOMPLETE and never called a pass.

The body, comment and commit claim no more than the diff, except one label (G299-2153-3).

## Findings
- **G299-2153-1 LOW (guard reach).** Cells 5 and 6 are literal greps for `^\s*echo.*<grafana value>` and `^\s*echo.*admin@secuura\.com\s*/`. My mutants M3, M4, M5 and M7 each print a value again and leave all 7 cells green:
  - M3 and M4: the same value line through `printf`.
  - M5: the Admin value reworded without the `/`.
  - M7: the value moved into a variable.

  The PR does not claim more: the body and the commit name the captured-output guard (acceptance line 2) as open. Every value-restoring mutant of the *removed* lines (M1, M2) is caught. It is a reach limit to carry to acceptance line 2, not a defect in this change.
- **G299-2153-2 LOW (READY evidence, not the PR).** `ready_round2.md` line 14 says "Census: attached to exactly KS-1413". The seat's only census record, `push/census_ks1413.out` (08:46), reads `PR 2153 is attached to: [] | expected exactly ['KS-1413']: False`.
  - The comment 72845754 itself is VERIFIED (`comment_real_ks1413.out`: posted, read back equal, ticket state, priority and assignee unchanged).
  - Whether Linear's GitHub link has since attached the PR is UNMEASURED by me: I did not touch Linear.
  - Wednesday should re-census before relying on the sentence.
- **G299-2153-3 LOW (wording).** The PR body says the ticket is "(In Progress, High)". The seat's own census reads priority **1**, which is Urgent in Linear (2 is High), and the ticket text says "raised Urgent". The comment does not repeat it.
- **G299-2153-4 INFO.** The test file now carries the Grafana and Admin local default values as plant strings (cell 4) and in its matchers (cells 5 and 6). It already carried the demo issuer value at base.
  - The body says so plainly.
  - The Grafana value is also in `.env.example`, `env.example` and `env.local.example`.
  - `check-no-default-passwords.sh` cannot see `.sh` files.

  These are local seed defaults, not real secrets. The repo's literal count rises by two files' worth.
- **G299-2153-5 INFO.** The held fence differs from the commit's diff only in metadata (item 1): file order, no `diff --git` or `index` lines, and no hunk-header function context. The trees are identical.
- **G299-2153-6 INFO (box).** Load1 was 4.39 at my start and 9.03/8.71 at my end. The rise came from other seats: my own work was greps and a few millisecond bash runs, with no suite or vitest.

## NOT TESTED
- A real start of `start-local.sh`, any stack, Docker or database. Only the extracted `show_urls` was run, as the seat did.
- shellcheck (not run by me).
- The sibling suites `check_slot_credentials.test.sh` (32/0) and `ks1355_slot_blind_launchers.test.sh` (78/0). These are carried from the seat, not reproduced: my mini-tree lacks their inputs.
- The union with open PRs 2052 and 2127 (UNMEASURED, as the seat says).
- The seat's "no open PR touches either file" (70 open PRs read at the API). Carried: I made no API read.
- The PR's live attachment to KS-1413 in Linear (G299-2153-2), and the live GitHub PR body. I compared hashes from the seat's read-back records, not a fresh API read.
- The output of the child checkers `start-local.sh` calls (unchanged by this PR).

No ticket, GitHub write, mail or post by me.
