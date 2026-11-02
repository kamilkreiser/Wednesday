STARTABLE: YES (after the stamp; nothing in the kit blocks a launch, five questions below carry defaults)

# B1172 / SEAT-G303 drafter report (drafted 2026-11-03 03:48 to 03:55 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1172_SEAT-G303_nexusai-rd904-906-gate-tier2.md` (about 63 KB; 9 lines read the four-underscore pattern: eight slots and the last line, control by construction). Template: B1155 / SEAT-G297 (`2026-11-02_B1155_SEAT-G297_nexusai-rd923-retire-gate-tier1.md`, the newest NexusAI gate kit; found with `ls -t | grep -i 'G2[0-9][0-9]_nexusai\|G30[0-9]'`), lowered to tier 2 (Sonnet) and re-aimed at a deletion plus four rewritten test cells. Builder kit B1167 and its STATUS read whole.

## BLUF
The gate is G2 / Sonnet, round 1 of 2, class "NexusAI: retire the unused SQLite risk-condition writers" (NO GO before: 0). It works in its own clone and head worktree under the jest lock. It re-runs the builder's reds and greens in five file states (R, X, Y, M, H), checks the 20 removed rd913 lines one by one, **proves S6 by raw SQL** (the builder swapped S6 to `addCostCenter(null, 'x')`, so the cell no longer touches `risk_conditions`), runs the builder's two mutants plus its own plants (split-line, nested-dir, OR-clause, assigned prototype method, renamed control method, and five cell-bite plants run at head AND at main so a weakened cell shows as red-at-main, green-at-head), runs the verify, and on GO writes four landing files.

## Facts re-measured (instrument; control)
- Origin: `ls-remote` main `0dd5dacf...`, branch `b692f32a...` (03:48:52). `gh api -X GET git/ref/heads/main` agrees. compare: ahead 1, behind 0, 4 files (numstat 0/74, 78/0, 15/20, 3/3). Control: `matching-refs/heads/b1167` = 1, `heads/b1172` = 0; `pulls/99999` 404; open PRs 0.
- Blobs by `git hash-object` over tarball extracts, branch blobs equal the compare API's shas (simpleDb `572b4e0d`, rd913 `4a47b115`, new `f9f9bca0`, counts `b384e09b`); `scripts/clear_db.js` `fb277a16` equal at main and head; workflow files equal.
- Line counts: simpleDb 880 -> 806 (= 74 removed). rd913 cells 20 and 20 (regexp; control new file reads 2). `__tests__/*.test.js` 313 -> 314. `backend/**/*.js` 94 and 94.
- Name census at head (case-sensitive, stated): 0 hits in `simpleDb.js` and in rd913; callers remain only as `jsonStorage.` calls on `server.js` (12 lines incl. one comment), the browser functions in rd395 and `static/`, `rd407` (JsonStorage receiver). Double-quoted-literal lines in simpleDb 5 -> 3.
- Deploy: `deploy-demo.yml` `:26`-`:32` push to main with paths-ignore md/docs/tests only; `workflow_dispatch` at `:33`; `vars.CI_DEPLOY_ENABLED` `:53`, `:91`; `environment: demo` `:95`. Repo variables 0, org (repo-scoped) 0, environments `["dev"]`, last five Deploy demo runs all push/skipped (jobs unread, the gate reads them). A merge starts the workflow; its jobs skip.
- Landing rule: C-190 `CLARIFICATIONS.md:2067` quoted in the kit: "Never squash, never rebase". Open code-scanning alerts on main 123.
- Class census (`python3 -I`): 120 STATUS files, 41 gate verdicts, 7 NO GO; verdict lines naming risk-condition/simpleDb/sqlite/retire/rd913/RD-904..906: 6, none a NO GO on this class (B1069 is a NO GO naming sqlite3, class "archiver 8 and sqlite3 6 upgrade").
- Ports 8560-8569: `lsof` rc 1 (control: listener on 7000 shows); scan of the 98 non-`.pre-` SEAT kits of 11-02 and 11-03 for `856[0-9]`: 0 (control `855[0-9]`: 1, B1155). Panes: tuesday, MPS-M83, Security-Composer-C81, fleet-monitor; `G303`/`B1172` in kits: 0 (control G302: 1). No `b1172` worktree or session-tools dir. Lock tool sha256 and fence preload sha256 as in B1155 (equal); jest queue empty at 03:51.

## Findings from reading the branch (given to the gate as aims, not verdicts)
1. S6 now proves the `SQLITE_CONSTRAINT` code through `cost_centers.name`, not `risk_conditions.condition_text` (head `:404`). The kit's Step 6 allowed this if the code matched; the gate re-proves it and proves the raw null-text insert gives the same name, code and errno (Major if they differ, Note otherwise).
2. The builder added one expectation beyond its kit's list: S3 `:360` (the seeded deactivated row exists). Strengthening; the gate plants a fault to show it can fail.
3. Git shows two hunks in `simpleDb.js`, not three (ranges 2 and 3 are adjacent); the builder reported it. The header comment changed main `:28`-`:30`, one line past the build kit's `:26`-`:29`; same sentence.
4. The new test has an em dash on lines 2 and 47 (the rd913 file has the same character on 12+ lines): Note.
5. Builder deviations in its STATUS (a typed `cd`, one `rm -r` of its own scratch dir, some scratch under /private/tmp): the kit tells the gate to record them as process Notes.
6. Q3 plant (dropping `is_active` from `getRiskConditionsByLevel`) is predicted green at both main and head: an older gap, equal across states.

## D-decisions (mine, in the kit)
- D1. Five file states (R, X, Y, M, H) instead of G297's three; **Y (head's rewritten rd913 over main's `simpleDb.js`) must be 20/20** because that is the build kit's property "expectations about remaining code keep their values at main", and no one else tests it.
- D2. Cell-bite plants run at H and at M so "red at M, green at H" = weakened cell = Major.
- D3. Node 24 is UNMEASURED by design (the installed `sqlite3` is a native binary built under the node that ran `npm ci`); S8 is the NO form with no node-24 suffix.
- D4. Landing files are written only on GO or GO WITH FINDINGS (none on NO GO).
- D5. Class name used verbatim as given.

## Q-questions for Tuesday (default in brackets)
- Q-1. Tier 2 / G2 / Sonnet as asked [yes]. The kit escalates to G1 only on a security-shaped finding or a not-red B1/B2.
- Q-2. Hard stop: 120 target and 210 absolute minutes after Step 0, plus an absolute latest time you write in S5 [default: you write the absolute latest time in S5; I left it blank]. About 30 jest tickets plus the 25-minute verify.
- Q-3. Allow a second `npm ci` under node 24 to measure the hosted version [no; stays UNMEASURED].
- Q-4. Include `merge-subject.txt` / `merge-body.txt` although C-190 prescribes no merge message [yes, same shape as B1155].
- Q-5. Kit size 63 KB (B1155 was 45 KB, B1054 73 KB) [accept].

## UNMEASURED
Hosted Build, Gitleaks and CodeQL (no PR); node 24 and Linux x64 `sqlite3`; the gate's own jest results (nothing was run, cloned or installed); whether anyone runs `scripts/fix_risk_conditions.js` by hand; the jobs of the last five Deploy demo runs (the gate reads them); the shared checkout `2_Project_Files` is stale (`origin/main` there reads `6a69fdf`), so every origin fact above came from `ls-remote` and `gh api -X GET`, not from it. The `file:line` pointers in the kit come from `awk NR` and `grep -n` over the tarballs at main and the branch; the pointers into the main-side simpleDb ranges (`:682`-`:791`) are the build kit's, stamped by Tuesday at 02:46, and the kit tells the gate to reprint them.

## Outside-the-fences disclosure
Read-only throughout. I wrote two files (the kit and this report) and, outside the project, extracted two `gh api -X GET` tarballs plus scratch into the session scratchpad (`.../scratchpad/br`, `.../scratchpad/mn`, `br.tgz`, `mn.tgz`); that scratchpad already held other files that are not mine. Git in the shared checkout: `ls-remote` and one `rev-parse --short origin/main` only. `tmux list-panes -a` and `lsof` were read-only. One Jira census ran through `b774lib.py` in-process (GET only; printed issue summaries, no token). No `decision_queue.sh`, no `fleet/briefs_staged/`, no scoreboard, no WEDNESDAY/FRIDAY tree, no mail or Artifact. I did not type `cd` in any command (one command carried a harmless shell variable named `cd_unused`, a no-op assignment, not a `cd`). A PreToolUse advisory about case-sensitive greps fired on several of my greps; the counts it concerned were cross-checked by program (diff, awk, hash) and none rests on a bare zero.
