STARTABLE: YES

# B796 DRAFTER REPORT (HPSM-POC records seat R56), drafted 2026-10-27 08:47 to about 09:20 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B796_SEAT-R56_hpsmpoc-records-229-231-planb.md` (135 lines). Shape copied from B771's kit. Every Stamp slot is left as four underscores. The `.pre-stamp` copy is NOT made (my fence allowed two files only): make it before stamping. **Slot count: 15 lines with the four-underscore pattern** (14 slot lines at kit lines 107-120, plus the last line `READ-WHOLE-BY-TUESDAY`), `/usr/bin/grep -c -E '_''_''_''_'` = 15 (control: a scratch file holding the pattern reads 1).

## BLUF
- One records seat (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` written in the launch line, no ports) records three landings, the 04:54 instruction and the Plan B deploy: **C-206 #229, C-207 #230, C-208 the instruction, C-209 the B783 deploy, C-210 #231** (default C-206 upward; the previous seat's PR #145 landed at 01:57:53 AEDT, records main now `940f229a`, highest heading C-205). Plus BACKLOG rows, one history entry, six catch-up STATUS files (B767, B768, B772, B782, B783, B784), three Jira comments (HPSMPOC-355, -356, -228), no new ticket by default.
- **The one trap in the commission:** #229's own push run (`ci` 40355489825 on `80ed6b42`) is a FAILURE, so the Done rule's push-run check fails for HPSMPOC-355. The kit makes the Done move conditional on a slot (`RULING-DONE-355`, drafter default `HOLD`: comment only). Tuesday may read the job log and rule `DONE-ON-FLAKE-READING`.
- **The 80ed6b42 CI finding, one line:** the failing job is `web e2e (journey-and-prototype)`, cell `[tablet] e2e/attribution-preview.spec.ts:31` at 1280 px ("a Consultant opens the preview from the menu"), a `locator.click` timeout of 30 s ("element was detached from the DOM, retrying") on the attempt and on retry #1 (118 passed, 1 failed, 9 skipped), which failed the aggregator `web (Next.js)`; #229 touched no web path; dfdcfa27 and d415a3fe push runs are green. No fix, no cause claimed beyond the log.

## Facts re-measured (instrument, control)
- Records: `branches/main` `940f229ad03d1ab29dfd066017b834e41c5adf10`; `pulls?state=all` newest #145 (records/b771, merged_at 2026-10-26T14:57:53Z), none open; `matching-refs/heads/records/b` lists `b771` as the newest by numeric reading (control: `b756` and `b701` listed); `records/b796` absent. Raw files via `gh api contents?ref=940f229a`: CLARIFICATIONS 4,020 lines, C-205 at `:4008`; BACKLOG 1,971; history 2,484. Term counts in the kit (positive controls `B607-1` and `68ebdbf7` found).
- Code: main `d415a3fe...` (`compare` identical 0/0). #229: squash `80ed6b42`, merged_at 16:04:01Z = 03:04:01 AEDT, 3 paths +116 -3, head `784dc978` 20/20 check-runs success. #230: `dfdcfa27`, 17:44:47Z = 04:44:47 AEDT, 2 paths +222 -16, head `a3fa1c0e` 50 check-runs all success (three `ci` runs on the head, one is `run_attempt` 2; the kit says so). #231: `d415a3fe`, 19:01:58Z = 06:01:58 AEDT, 9 web paths +174 -47, head `87716de6` (moved from `9754d9c7`), 20/20 success. All three: one parent, `verification.reason` valid, trailer form printed in the kit.
- Push runs: 80ed6b42 `Push on main` success, `ci` failure (19 check-runs: 16 success, 2 failure, 1 skipped); dfdcfa27 both success (18 + 1 skipped); d415a3fe both success (18 + 1 skipped). Job-level read of run 40355489825 via `gh api .../runs/<id>/jobs` and `gh run view --job 121687793643 --log`.
- CodeQL: open alerts 0 (control `state=fixed` 1); analyses with `results_count` 0 x4 at 784dc978, 80ed6b42, 87716de6 (the first-100-rows page did not reach a3fa1c0e, dfdcfa27, d415a3fe: stated UNMEASURED in the kit).
- Branch protection: `enforce_admins` true; 5 required contexts printed.
- STATUS files: lines, mtime, sha16, `HP Restricted` 0 each (control 1) for the six; last lines are their own `READY FOR QA:` / `VERDICT:` / `DEPLOYED:` lines; `git check-ignore` rc 1 on B767.
- Verdicts (last lines): B772 GO WITH FINDINGS both classes, round 1 of 2, findings B772a-1..3 and B772b-1..3, all Note; B784 GO WITH FINDINGS at `87716de`, B784-1 Major SAME FIXED by the builder's one fix commit, B784-2 Minor (6 of 16 phone header cells wrap); B783 DEPLOYED, web only, UAT 05:27-05:28, demo 05:42-05:44 AEDT, both at `68ebdbf7` / `MZVikiC3U2dPSa26VhgyK`.
- Jira (GET): HPSMPOC-355 (0 comments, B733 residue, Done-when quoted in the kit and met by B767's account), HPSMPOC-356 (0 comments; B734-2 reworded by #230, B734-3/-6/-9 untouched: Done-when NOT met), HPSMPOC-228 (1 comment, the Gate B243 N-8 note; #230 commit 2 does that note's fix except the run-time proof). Zero control `kwpf8rrzzmarker` 0; positive control `UatOpenTests` 23.
- Register scan (inclusion filter only): 12 HPSM-POC hits at the same lines as B771's census, none dated 26 or 27 Oct.
- Panes (`tmux list-panes`): `tuesday`, `Datasec/MPS-G167`, `Datasec/NexusAI-R55`, `fleet-monitor`; no HPSM-POC pane. `lsof` on 8660-8669 empty. Load1 7.58 at 08:50 (above the 7 launch threshold: Tuesday's queue rule). `.tools/b796`, `.tools/wt-b796` absent (control `.tools/b771` lists). Helpers: 0 missing of the 38-name list in `.tools/b701`.
- Model: row C8 `model-routing.md:98` (records seats B649..B771 used it), id `claude-sonnet-5-5` from `models_latest.json` line 23 (Opus is line 17); launch line carries `BRIEF_SEAT_LEVEL=sonnet`.

## D-decisions (mine, for Tuesday to keep or strike)
- D-1: one C-entry per PR (C-206, C-207, C-210) in time order around a standalone instruction entry (C-208) and the deploy entry (C-209), as B756/B771 did; `FOUR` folds the instruction into the deploy entry.
- D-2: comments on all three tickets (355, 356, 228) as landing records; moves: none except the slot-gated Done of 355. HPSMPOC-356 and -228 stay open (Done-when not met / other items open).
- D-3: no new ticket (`TICKETS-RESIDUE` NONE): B772 findings are all Notes, B784-2 is a Minor that Tuesday's earlier B749 ADDENDUM-2 ruling file calls an expected wrap; Notes ride on parent-ticket comments and BACKLOG rows (B771 precedent: notes "not ticketed"). `ONE` is spelled out in the kit (search-first queries, labels).
- D-4: the 80ed6b42 failed push run is a fact in C-206 and in the Done check, not a BACKLOG row or ticket (you asked for an information item with no fix).
- D-5: N-1 (a bigger header logo) carried only in C-210 and the seat's FOR TUESDAY, as B771's Correction 8 settled; I added that it concerned the two-line header logo that #231 replaced.
- D-6: "merged and NOT deployed; open with the product owner", no card id, nothing on hosted state after 05:59.

## Q-questions for Tuesday (each with a default)
- Q-1: `RULING-DONE-355`? Default HOLD (comment only). Alternative `DONE-ON-FLAKE-READING <time> by <seat>` after you read the job log; the kit then replaces check (5) with (5b).
- Q-2: `C-SCOPE`? Default FIVE.
- Q-3: `TICKETS-RESIDUE`? Default NONE. `COMMENT-KEYS`? Default NONE.
- Q-4: should the failed push run become a BACKLOG row or ticket (a flake class, cf. the existing `B544-d1` row)? Default: no, fact only.
- Q-5: stamp the launch when load1 is below 7 (7.58 at 08:50).

## Differences from the commission
- The commission says the previous records seat's work is "the last records seat"; it is already landed (PR #145), so the kit's baseline is `940f229a` and numbering starts at C-206.
- The commission names HPSMPOC-228 as a handover key: verified as the B176/R11-guard ticket (its comment is the N-8 note); it is a comment target only.
- The Done-rule check (push run completed success) FAILS for #229 today; the commission did not say so; the kit handles it by slot.
- B785 (Track A deploy of #231) and B792 (demo chooser settings) kits exist, unstamped, no STATUS in `Briefs/`: stated as not launched.
- Six catch-up files (not three).
- The kit cites a few STATUS line numbers I read (B784 `:73`, `:104`, `:107`, `:108`, `:116`; B768 `:187-:190`; B772 `:116-:121`, `:125-:126`, `:142`; B782 `:110`; B783 `:17-:24`, `:236-:248`, `:292`); the seat re-reads each.

## UNMEASURED
Who ran the three merge commands; CodeQL at three of the six shas; whether the failed cell recurs (one run read; the same job passed on the PR head and on later pushes); the 08:05 demo (whether it ran, from which site); hosted state after 05:59; whether B785 or B792 has been stamped since 09:00; the board time of the 04:54 instruction (only the B782 kit's time is known).

## Outside-the-fences disclosure
Wrote only the two named files with Write, plus one `python3 -I` in-place edit of the kit (corrections of cited line numbers; same file). Bash redirections wrote to the session scratchpad only: raw copies of the three records files (`CLARIFICATIONS.md`, `BACKLOG.md`, `history.md`), the failed job log (`ci80_job.log`), two tiny control files (`hpr_ctl.txt`, `ctl.txt`). Reads: `gh api -X GET` and `gh run view --log` under the project's `GH_CONFIG_DIR`; Jira reads through `.tools/b701/search.py` and `jira.py` (every JQL `project = HPSMPOC AND ( ... )`; `jira.py` prints a comment author's display name, which I did not copy); `git --no-optional-locks -C <project> check-ignore` once; `tmux list-panes`, `lsof`, `stat`, `shasum`, `uptime`, `/usr/bin/grep`; one inclusion-filter read of the clarifications register; Tuesday's briefs tree (B771..B795 kits, addenda, this folder). No `decision_queue`, no Artifact, Docs, mail, chat; no HTTP to any hosted, UAT, demo or production site; no git fetch, pull, worktree, checkout, merge-tree, commit. Nothing outside Datasec paths and this seat's tree was read other than the register and `model-routing.md` / `models_latest.json` lines (both in this seat's tree). Name scan of the kit: "Kam", "kamil", other names, e-mail shapes: 0 each; decision-card id shape 0 (control: a planted id reads 1).
