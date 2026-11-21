This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-MODE only. Report under "## ADDENDUM 6 (merge main, then the merge check)" in your STATUS file.

# POLICY-MODE — ADDENDUM 6: take in the new main, one check.sh, then Friday's merge check

## 0. Where you stand
Friday's own clean-clone merge check of your r3 head `4b3c62720923342ab23da9635916c75c03988fe4` PASSED (2026-11-21 16:09): `check.sh` exit 0, 1,322 / 0 / 21 over 174 result lines; `crates/coagent-policy/red-controls.sh` all 60 red, normal build green; scope 14 files against main `16e83fb`; `src/` unchanged since `443549c`. Evidence: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/merge_check_policy_mode_r3/`. The merge was held only so that the relay lane, which the owner was waiting on, landed first. It has: main is now `104dd394c390b614410cdba76ac45eeffa6bb220` (relay-reconnect). Main may move once more before you finish, when W-KIT merges (scripts, docs and BACKLOG only; no crate, no Cargo file). That move does NOT require you to re-run anything: merge it in if it lands, keep BACKLOG's both sides, and say so.

## 1. Do
1. `git fetch`; confirm `git ls-remote origin main` by SHA (`104dd39`, or a W-KIT head on top of it). Merge `origin/main` INTO your branch (never rebase). Expected conflict: `BACKLOG.md` only, both sides kept. A conflict anywhere else: STOP.
2. Do NOT edit any file of yours. Nothing in `crates/coagent-policy/` changes in this round (check: `git diff 4b3c627 HEAD -- crates/coagent-policy docs/POLICY.md` prints only what came from main, which should be nothing).
3. ONE `scripts/check.sh` on the merged head. Before it, `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` must print below 3 (a tool failure = FULL). The policy runner is NOT re-run: your crate and its tests are unchanged, and the relay change does not touch the policy crate.
4. Push; `git ls-remote origin policy-mode` = HEAD; `git merge-base --is-ancestor origin/main HEAD` exit 0; re-read main by SHA.

Last line when done, exactly: `READY FOR MERGE CHECK POLICY-MODE r4`.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
