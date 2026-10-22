# B497 ADDENDUM-2 drafter report (2026-10-23, ~07:0x AEDT)

File: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B497_ADDENDUM-2.md` (a clone of B425; read B425 brief + STATUS whole, M1's brief addenda and STATUS whole). Nothing built, pushed, landed or written to Jira/gh.

## Stamp slots (two lines, both must be filled before launch)
- Line 1: `GO: ____` -> Tuesday fills exactly `GO: land #105 at 6a69fdf4 (Tuesday s146)`, only after the checks are green.
- Line 2 (my addition): `GATE BASIS: ____`. Kam's 2026-10-16 grant is "merge-once-tested on Tuesday's GO after a QA gate verdict at the head"; B497 named a tier-2 gate after any build, and I found no gate STATUS for #105. Tuesday states the basis (gate or own at-source verification). Delete line 2 if you do not want it; the slot-count check then still reads 1 slot.
- Count check: `grep -c -E '_''_''_''_'` on the file = 2 now (control: planted four underscores = 1); must be 0 after stamping. No other line contains four underscores.

## Measured (read verbs, GET only)
- `ls-remote`: main `7c11c78f`; branch and `refs/pull/105/head` both `6a69fdf4…`; `refs/pull/104/head` `c139e4a8`.
- `gh api pulls/105`: open, draft false, base `7c11c78f`, 1 commit, 1 file, +16/-6, mergeable true but `mergeable_state` **blocked** (checks pending).
- `gh run list --commit 6a69fdf4` / `check-runs`: Gitleaks and npm-audit (`audit-production-deps`) success; **Build `39843092249` and CodeQL `39843087969` (Analyze javascript-typescript) were still running**; actions and python analyses present, 0 results.
- `code-scanning/alerts?ref=refs/pull/105/head&state=open`: EMPTY (not a clearance yet, JS analysis not in). Control `refs/pull/58/head` fixed = 259 258 257 256. Alert 151 on main: open, `:43`; open alerts on main 141.
- git: `cat-file -t` commit; tree `fec59297…`; parents `6a69fdf4 7c11c78f`; ancestor rc 0 / reversed 1; `0 1`; delta `package-lock.json`, 1958 bytes, sha256 `e179e8b6…` (head -c 100: `05a78cfb…`); counts blob `a2f40639…` identical at main and head, 4971/305; `c139e4a8` ancestor of main rc 0, reversed rc 1.
- `deploy-demo.yml`: `paths-ignore` is md/docs/tests only, so a Deploy demo run WILL exist for the push; last three on main all skipped.
- `land.sh` (s100o): 48 lines, sha256 `ae98c68f…` (= B425 pin). One-line `S=` edit (`b497-land`) would hash `bf463438…` (computed by pipe, nothing written).
- Jira GET: RD-879 To Do, Highest, 1 comment (39869), transitions include 31 (Testing) and 51 (Declined trap). JQL: both GHSA ids 0 hits; `nodemailer` hits RD-412/419/432 (SMTP features); `ip-address` hits include RD-732 (earlier, different advisory, Medium). Create meta: Task id 10030. Priority chosen Medium (matches RD-732).

## #151 answer
**Probably not needed.** #105 changes only `package-lock.json` and PR analyses are diff-scoped (C-209), so #151 should not appear on the PR ref, and the unedited control path of `land.sh` runs (only Edit A, the `S=` path). I wrote Step 2 as two branches: empty list -> Edit A only; exactly the B425 #151 row -> add B425's Edit B block with its seven controls; any other row -> STOP. The list must be re-read once the JS analysis completes (REFUSE 9).

## Assumptions / flags
- Pane `Datasec/NexusAI-M1` is assumed live and still holding the B497 session; if not, Tuesday relaunches under a new seat name and edits REFUSE 2 and the STATUS path.
- Worktree `b497-land105` is new (not `b497-fix`, which holds `node_modules`); scratch dir `session-tools/b497-land/`.
- RD-879 comment is posted after the landing; the new ticket is created after the landing (its description states the landing sha); if a ticket already covers either GHSA the seat comments instead.
- Umbrella `CodeQL` check-run read `neutral` at drafting; I had no baseline, so the addendum compares it to PR #101's head and STOPs on an unexplained difference.
- The statement "about 17 hours" and "audit rc 1 -> 0" in the new ticket come from M1's STATUS and are asserted by grep there.
- `CLARIFICATIONS.md` lives at `1_Project_Definition/CLARIFICATIONS.md` (2368 lines, last entry C-218 at :2362, line numbers re-read).
