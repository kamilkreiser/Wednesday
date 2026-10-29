STARTABLE: YES

# B913 drafter report (kit: 2026-10-30_B913_SEAT-G210_hpsmpoc-241-regate-on-new-main-tier2.md), drafted Fri 30 Oct 2026 about 02:06-02:20 AEDT

## BLUF
The kit is startable now. The part you most wanted to know is already fixed: the PR was closed and reopened at 15:05:38Z / 15:05:40Z (02:05 AEDT, `issues/241/events`), so `pulls/241` now has base `9659148c`, the hosted merge ref `7d5f605cf507...` has parents `9659148c` + `59625e5f`, and a NEW `ci` run `40898052875` was in_progress at 02:06. The kit still tells the gate to re-verify that at Step 0 and to STOP with a named line if it reads otherwise. The head is unchanged (`59625e5f`), main is `9659148c`, and the 20 moved paths share 0 with #241's 20 (control 20 of 20). Kit is 69 lines (long lines, B901 shape); four-underscore line count 8 (control 1), 0 non-ASCII bytes, 0 `@X@` tokens.

## Facts re-measured (instrument; control)
- Main: `ls-remote` `refs/heads/main` = `9659148c4faf8f285df4e50dc5a0b5c7fea2a04f`; `commits?sha=main`: `9659148c` (#240, 11:40:30Z), `afe49a3b` (#242, 11:40:04Z), `88569299`. `compare 88569299...9659148c`: ahead 2, behind 0, 20 files (listed in the kit).
- Overlap: `/usr/bin/grep -c -x -F -f moved.txt f241.txt` = 0; control (f241 against itself) = 20. Frame: `pulls/241/files --paginate`, 20 rows.
- Head: `ls-remote` branch and `refs/pull/241/head` = `59625e5f...`; `pulls/241` head the same, open, draft false, mergeable true, mergeable_state blocked.
- Hosted merge ref: first `ls-remote` read at 02:05 showed the old `d4fd300c`/base `88569299`; the read at 02:06:22 showed `7d5f605c`, base `9659148c`, parents `9659148c`,`59625e5f` (`git/commits/<full sha>`; control: the 8-char form returns 404, so the parent read needed the full sha). This is the staleness the kit guards against; it was refreshed in the minutes between my reads.
- CI: old run `40827172158` failure (the B901 timed-journey red); new run `40898052875` in_progress (infra, web unit, web build, api, two SQL Server in progress; dependency review and gitleaks success). The head's check-run list still shows only the OLD CodeQL/Analyze rows (06:06-06:09Z) at 02:06, so whether a CodeQL run exists for the new merge ref is open: the kit makes C8 read it and call the gap.
- Post-landing main run `40867205920` (push, 9659148c) = success; its `web e2e (journey-and-prototype)` job `123425476268` success.
- `globals.css` at 9659148c line 65: `[data-scroll-x] { position: relative; }` inside the base layer (read via `contents?ref=`). `journey.spec.ts` at 9659148c line 44 prints `[journey-spans]` (grep control: line found).
- Ports: `lsof -nP -iTCP:9920-9929 -sTCP:LISTEN` empty, rc 1 (the positive control is the gate's). Word-boundary scan over 30 non-`.pre-` SEAT kits of 10-29 and 10-30 (controls `x 9920 y` 1, `a9920` 0): 7 hits, all 10-29 and all finished (B901, B903, B905, B908, B909, B910, B911); none from 10-30. Panes: `tuesday`, `fleet-monitor` only; no G210. Block 9920-9929 assigned.
- Model: row G2 `model-routing.md:109`, G-cap `:111` (`grep -n` hits); `models_latest.json` shows `claude-sonnet-5-5`. Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- Helpers `.tools/b198/lock.sh` and `.tools/b267/waitload.sh` exist (`ls` rc 0).

## D-decisions (mine, Tuesday may strike)
- D-1 Round count: B901 was GO WITH FINDINGS, so the loop should read "NO GO 0 of 2 before; this is the re-gate of round 1 on a moved base"; a regression caused by the merge makes it NO GO round 1 of 2. Written into C9(6).
- D-2 The old `wt-b901-combo` probe is gone: the merge tree IS the combination now. Worktrees are base (main), head, merge, mut; fetch refspecs two (main, b891), not three.
- D-3 B901's p1-p9 and p11 are NOT re-run in full (head bytes identical; none of the moved files are read by those rows). The kit runs the 9 + 2 unit files at the merge tree, three new plants (p-a remove the `[data-scroll-x]` rule; p-b the min-w width plant; p-c drop `tags`) and c0/c1/c-fail. Listed in UNMEASURED by design.
- D-4 B901-2 (2 px at 1024 on /workspace and /customers) is a Major in the re-gate if it reproduces at the true merge (wider than main), per B901's own rule; a Blocker only if wider than the viewport.
- D-5 A new Blocker: a #240 sidebar spec row red at the merge and green at main; and a walk locator resolving to a Previous or sidebar link (B910 only read this by text, the kit makes the gate count it at runtime).
- D-6 The kit also asks for the 40 px control, the lint unused-variable control and the 3x unit stability run that B901 skipped.
- D-7 GitHub state must be read on the NEW run, never the old one: stated in C8 because the old run's checks (4 of 5 success) would otherwise be quoted.

## Q-questions for Tuesday
- Q-1 Do you want the sidebar-present Previous check to cover all four roles? Default: at least Partner/Admin plus one customer-facing role (named in STATUS); the kit says so.
- Q-2 Is it acceptable that the merge-ref analysis may not exist at the gate's verdict (old Analyze rows are for the old base)? Default: the gate reports the gap and verdicts GO WITH FINDINGS "CodeQL PENDING/absent for the new merge ref", landing hold stands, you decide on the gap.
- Q-3 Squash text lines: default as B901's, with counts re-measured by the gate; the PR body's "eight new test files" is corrected there (nine unit files plus one spec).

## UNMEASURED
Whether the new `ci` run goes green; the new base's unit/e2e totals (B908 reports 3099 unit and 456 listed at the #240 head, not at main 9659148c: the kit makes the gate quote its own); whether the 2 px of B901-2 reproduces; the contrast ratios on the new tokens (nobody has run them); the walk locators at runtime; hosted spans of the new run; CodeQL on the new merge ref. I built and ran nothing.

## Outside-the-fences disclosure
None crossed, to my knowledge. All `gh` calls were `-X GET` under the HPSM-POC `GH_CONFIG_DIR`, including those with `-f` fields (a first attempt wrote `pulls?state=open` unquoted and zsh refused it; it did not run). Git reads: `ls-remote` only, via `--no-optional-locks` on the shared checkout. I read the B901 kit and STATUS, B908/B910 STATUS lines (grep and `sed -n`), `model-routing.md`, `brief_seat.sh` lines 20-32, `CLARIFICATIONS.md` (grep). No card was read, no `decision_queue.sh`, no briefs_staged, no scoreboard, no ledger, no hosted host, no mail. One scratch file under the session scratchpad (`moved.txt`, `f241.txt`). I did not `cd`. One advisory (non-blocking) hook note on a case-sensitive grep: the match fired (G2 and G-cap printed), so it is not a false zero. Only the two named files were written.
