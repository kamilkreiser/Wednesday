This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. For lane B, P1P-DEMO, branch `p1p-demo`. The ONE batched independent check returned **GO WITH NOTES** for your head `8839ec54d15c5de57fdbfdd49ee76df73cb55cc6` (0 Blocker, 0 Major; Minor P1-3 is yours). Read the verdict WHOLE first (READ-ONLY): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/p1p_review/gate_P1P_verdict.md` (P1-3 and its e2 evidence). Everything in the brief not named here stands. Report under a new STATUS section "ADDENDUM 1 (check notes)"; last-line protocol unchanged.

# P1P-DEMO — ADDENDUM 1: the excluded folder is renamed

Start check: worktree clean, `git rev-parse HEAD` = `git ls-remote origin p1p-demo` = the head above; else STOP. After any compaction, re-read the brief, this file and your STATUS whole.

1. **P1-3.** The policy matches SHELL words by name (`**/private/**`, policy `engine.rs:384-391` at main), so even `--exclude '<ws>/private/**'` denies every Bash call whose working directory is under `/private/tmp` (Friday's demo root). Rename the excluded folder everywhere in `preview/` to `secret` (`<ws>/secret/`, exclusion `--exclude '<ws>/secret/**'`): `replay/run.sh`, `demo/setup.sh`, `demo/one-mac.md`, `demo/lan.md`, `replay/EXPECTED.md`, `REVIEW.md`, and anywhere else a grep of `preview/` for `private` finds it (list each hit and what you did; a hit that is not the excluded folder stays).
2. In `REVIEW.md` and `EXPECTED.md`, one sentence: a workspace path containing a folder whose name matches an exclusion word is excluded for shell commands too (the policy reads shell text by word), and what that means for choosing an exclusion.
3. **Runs:** `run.sh` against lane A's binaries at its CURRENT pushed head (record the SHA; lane A is fixing its own notes in parallel, so re-run once more when its STATUS reads `READY FOR MERGE CHECK P1P-GATE r2`): 23/23 under a root inside `coagent/tools/tmp/pv/` AND under a `/private/tmp/…` root of your own (short path, socket length checked); the four reds each exactly one FAIL on its own line, under both roots.
4. Base: if lane A's addendum merges a newer daemon head into `p1p-gate`, nothing changes for you (no shared files); do not merge anything into `p1p-demo` unless a conflict-free `origin/main` merge is needed because the daemon merged to main (then merge `origin/main` INTO `p1p-demo`, never rebase).
5. Final: name scan with a positive control; push; ls-remote. At most TWO heavy runs machine-wide.

## The last line
`READY FOR MERGE CHECK P1P-DEMO r2`

Then WAIT. No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
