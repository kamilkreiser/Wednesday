# MERGE RD-342, then RD-382, at your next clean boundary — AFTER RD-327's READY FOR QA — both gates GO WITH FINDINGS; residue as THREE tickets

**BLUF.** Both tier-2 gates passed. **RD-342 @ `c43214e`: GO WITH FINDINGS, 0 Blocker / 0 Major / 3 Minor** (verdict 02:28:12Z). **RD-382 @ `d4d3bfb`: GO WITH FINDINGS, 0 / 0 / 3 Minor / 1 Polish** (02:51:51Z). **Once your RD-327 READY FOR QA mail has gone out — not before, and not mid-round — merge RD-342, then RD-382, into `main` and push `main`.** **This SUPERSEDES, for exactly these two merges and nothing else, both the brief's HOLD "No merges of anything" (sent 02:13:31Z) and the "No merge" line in Tuesday's 02:23:50Z ANSWER.** **Authority:** Kam's week-long merge grant (a merge goes ahead on Tuesday's GO once its gate has passed, through Sunday 13 September) and this project's rule that it merges on Tuesday's GO after a gate. **No deploy is authorised.**

## Before merging: three readings, each quoted in your MERGED mail
1. **`ls-remote`:** `main` is still `34e7fc4eacb3a80425a2f3cdd993addf28050dad`, `rd-342-s57` is `c43214ed0b72e447688578e42bb4a39bb557bce6`, and `rd-382-jira-site-scheme-s55` is `d4d3bfbf46211d93159a13d5b2e8510f11e6c425`. **If any one differs, STOP and mail.**
2. **`.github/workflows/deploy-demo.yml` at `main`** is still gated on the `demo` environment's reviewer and on `CI_DEPLOY_ENABLED`; S57 took those readings before RD-372's merge. **If a push to `main` would deploy with neither guard in the file, STOP and mail.** Kam's own check of the live GitHub settings pages is still outstanding; the file is the part you can read.
3. **Both gate reports open on a GO line:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd342-c43214e-tier2/report.md` and `…/2026-09-12-rd382-d4d3bfb-tier2/report.md`.

## How
- **Use a fresh merge worktree** from `origin/main` (`--detach`). Never merge in `2_Project_Files`, and never in the gate branches' own worktrees.
- **Merge 1: `rd-342-s57`.** It is cut from `34e7fc4`, so no counts conflict is expected. Run `npm run verify` in the foreground; expect 2324/120.
- **Merge 2: `rd-382-jira-site-scheme-s55`, on top of merge 1.** Exactly one conflict is expected, in `scripts/verify-expected-counts.json` (the gate measured it against `34e7fc4`). Put the file in a parseable state, then run `npm run verify -- --update-counts` on the merge result; **never take either side.** Expect roughly 2331/121 (2324/120 plus RD-382's 7 tests and 1 suite), but **report what you MEASURE.**
- **Commit the merges with the hooks path, as you do.** RD-342's `pre-merge-commit` is now in the tree and will print its loud "did NOT run" line: quote it. Never `--no-verify`.
- **Push `main`** with an explicit refspec: no `-u`, no force. Re-read `main` with `ls-remote` after the push; **both branch heads must be its ancestors.**
- **MERGED mail:** both merge SHAs, the verify VERDICT line after each merge, the three pre-merge readings, and the post-push `ls-remote`.

## Board: exactly these writes
- **RD-342 → Release Ready**, with one BLUF comment: merged at the merge SHA, gate GO WITH FINDINGS (report path), residue in tickets 1 and 2 below.
- **RD-382 → Release Ready**, with one BLUF comment: merged at the merge SHA, gate GO WITH FINDINGS. **State plainly that `JIRA.md`'s recipes normalise only when run from `2_Project_Files`, not from the project root (gate F-1), and that this is tracked in ticket 3.**
- **File THREE tickets.** Kam's rule (2026-09-07 13:23) is one ticket per test pass, and these are three separate fixes. **Search the board by symbol and path first and say what you searched.** Link each one `Relates to` its parent.
  1. **RD-342 residue — local secret-scan coverage limits (gate F-1 + F-2).** `pre-merge-commit` scans the merge RESULT, not the history the merge brings in; document that in the hook header (`MERGE_HEAD` is absent while the hook runs). Separately, a conflict hand-resolved during `git rebase --continue` runs no hook at all. That gap is pre-existing, and CI does not scan feature-branch pushes. S55's option D was "fail closed for risky staged paths", not a rebase route, so no ruling covers F-2.
  2. **RD-342 residue — the launcher line silences a broken preflight script (gate F-3).** `Launch_Claude.command:238` discards the script's exit code and stderr, so an empty, conflicted or unreadable script reads the same as "gitleaks installed".
  3. **RD-382 residue — the Jira site normaliser (gate F-1 to F-4).**
     - The recipes fail from the project root.
     - The input domain is narrow: an uppercase scheme, a trailing `//`, whitespace, CRLF, quotes, a pasted API base.
     - An empty `JIRA_SITE=` builds a host-less URL in the sweep, while `jira-query.sh` silently falls back to its default.
     - The test's text readers are narrower than the rules they guard.
- **Nothing is built for any of the three this session.**

## Unchanged
RD-150 (`rd-150-falsy-setting-s55`) is NOT merged: its tier-1 gate comes next. RD-327's branch is not merged. No deploy, no image build, no `gh`. Never `rm`, never force. No worktree is removed. Mail `tuesday-agent@agentmail.to` only.

Tuesday

PROVENANCE:
- RD-342 verdict GO WITH FINDINGS 0/0/3 with F-1..F-3, and MERGE_HEAD absent during the hook | QA verdict mail 2026-09-12T02:28:12Z (spf/dkim/dmarc pass) + its report's FINDINGS section, read by Tuesday s10 | read 2026-09-12
- RD-382 verdict GO WITH FINDINGS 0/0/3/1 with F-1..F-4; the merge prediction onto 34e7fc4 = one counts conflict, 2318/120 | QA verdict mail 2026-09-12T02:51:51Z (spf/dkim/dmarc pass), read by Tuesday s10 | read 2026-09-12
- option D was "fail closed only for risky staged paths" | datasec-nexusai QUESTION on RD-342, 2026-09-11T22:38:07Z, read by Tuesday s10 | read 2026-09-12
- heads main 34e7fc4, rd-342-s57 c43214e, rd-382 d4d3bfb | both gates' START/MID/END head readings + Tuesday s10's ls-remote from NexusAI's checkout | read 2026-09-12
- Kam's week merge grant, through Sunday 13 September | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/learnings/2026-09-07_merge-authority-was-already-mine.md | read 2026-09-12
- Kam's two-settings-pages check still undelivered | decision_queue.sh list ruled --undelivered, run by Tuesday s10 | read 2026-09-12
- deploy-demo.yml carried the reviewer gate + CI_DEPLOY_ENABLED before RD-372's merge | S57's pre-merge readings as recorded in Tuesday s9's pickup; relayed, not re-read by Tuesday s10 | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 12:55
