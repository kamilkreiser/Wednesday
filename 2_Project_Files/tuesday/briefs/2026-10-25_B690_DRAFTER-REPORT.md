STARTABLE: YES (stamp when you want it; the PR's CI is still running, so the seat will wait on it; read Q1 on the round count and D2 on the port block before stamping)

# B690 drafter report (SEAT-G123, Datasec / HPSM-POC, QA gate tier 2 on PR #218) -- drafted 2026-10-25 19:5x-20:2x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B690_SEAT-G123_hpsmpoc-218-gate-tier2.md` (93 lines; 8 lines carry the four-underscore pattern: the seven Stamp slots and the last line; control: a scratch line with the pattern counts 1). 0 non-ASCII bytes; 0 at-sign-capitals-at-sign tokens; 0 lines naming the product owner or any staff.

## BLUF
- PR #218 is open, one commit `daeed7e0` on main `4e63fc41` (ahead 1, behind 0), one path `.github/workflows/ci.yml` +1 -1, one hunk at line 392. `mergeable` true, `mergeable_state` blocked only because checks are still running (12 check-runs listed, 7 in progress; the CodeQL umbrella reads `neutral` while 3 of 4 Analyze runs are in progress). The seat must wait on them; the kit says so and caps the verdict at GO WITH FINDINGS while anything is pending.
- The gate re-measures the builder's headline claims with its own program: comment-only (strip program + ruby YAML equality, 9 planted controls that must fire including a comment-shaped `#` line inside a `run: |` block), identity of the edit (new == old minus the substring), added words empty, no record ids, readers 31/44/14/18, whole-infra suite through `test_security_baseline.py` with Bicep (which the builder could NOT run), CodeQL 4 of 4 on the head.
- Round count: **0 of 2 spent on this class; round 1 of 2.** B669/B677 spent 2 of 2 on a different class (reader test plus comment edit). See Q1.
- Phase rule: checked by program in Check 6d (no HP tool term in the added line; the diff is a developer comment of the CI workflow).

## Facts re-measured (instrument; control)
- PR #218 state, head, base, commits 1, files 1, +1 -1, mergeable true / blocked, merge_commit_sha `bef97a00...`: `gh api -X GET pulls/218` (project GH_CONFIG_DIR). Control: the PR number's own head equals `ls-remote origin refs/pull/218/head` = `daeed7e0...` and equals `refs/heads/b687/hpsmpoc-351-audit-comment`; main `ls-remote` = `4e63fc41...`.
- Files / hunk: `pulls/218/files` printed one file with the patch `@@ -389,7 +389,7 @@`; the removed and added lines are line 392, identical except ` under C-44 and C-99 POC-4`. Control: the compare `4e63fc41...daeed7e0` printed `ahead 1 behind 0 1 file`.
- Blobs: `contents?ref=` sha of `ci.yml` at main `135260d6...` (equals B687's and B677's blob), at head `0176b491...`. Control: the main blob equals the one the previous gate recorded.
- Who reads `ci.yml`: `git grep -F 'workflows/ci.yml' 4e63fc41` hit the reader, `web/scripts/e2e.mjs:541`, `web/src/audit-dev.test.ts:201` (parses the whole file), `web/src/e2e-runner.test.ts:149`, plus doc mentions. Control: `git grep -F 'zzz-no-such-7f3a'` printed 0 lines. Consequence: a comment edit with equal parsed structure and equal matrix line cannot change those readers; the kit makes the vitest job the check for the two web files, by log.
- Ticket HPSMPOC-351 (`jira.py`, GET, read whole): item 3 = the audit comment at lines 391-393; its one comment says item 3 "stays open here"; status Backlog (new). The Done-when quoted there is items 1 and 2, met by #217. Control: the helper printed the full ticket and the one comment (it would error on a wrong key).
- CI at 19:5x: 12 check-runs, listed in the kit with statuses; analyses stored 2 at `daeed7e`, 0 results, empty error. Branch protection: `rules/branches/main` has `required_status_checks: []`, strict false, `code_scanning` CodeQL errors / high_or_higher; classic protection lists five required contexts, strict false. Control: the same call format reproduced B677's recorded figure (empty list, strict false).
- Open PRs: `pulls?state=open` printed exactly `218`. Branch refs: `git/matching-refs/heads/b68` printed only the builder's branch.
- Ports: `lsof -nP -iTCP:9830-9839 -sTCP:LISTEN` printed nothing (rc 1). Control: I bound AND listened on 9840 from a python process; `lsof` on 9840-9849 listed it; then the process exited and `lsof` printed nothing again (rc 1). A first control on 9830 bound but did not listen and so was (correctly) not listed: a bound-but-not-listening socket is invisible to `-sTCP:LISTEN`; the kit now says to bind AND listen.
- Port scan of the non-`.pre-` SEAT kits of 10-24 and 10-25, `(^|[^0-9a-f])983[0-9]([^0-9a-f]|$)`: 7 hits: B633 (a finished Composer gate that owned 9830-9839; its pane G99 is not live), B627 / B631 / B640 / B641 (partition text only), B555 / B582 (hex tenant id false positives). Control: `972[0-9]` hit B621, B622, B648 as the previous kit reported. None of the live seats' kits (B682-B688) hit. `984[0-9]` and `985[0-9]` each hit five and three finished kits, so no cleaner decade.
- Live panes: `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` = tuesday, Security-Composer-J16, HPSM-POC-H27, HPSM-POC-H25, MPS-M25, MPS-M26, HPSM-POC-H26, Security-Composer-G122, fleet-monitor. No G123. B683 (H25) reads `ci.yml` but never edits it (its own kit says so); B684 (H26) is one Api test path.
- Tools: `bicep --version` 0.47.16 (`.tools/bicep/bicep`); `/usr/bin/python3` 3.9.6; `python3` 3.14.7. `.tools/b690` and `.tools/wt-b690-*` do not exist (control: `ls -d .tools/b660` lists).
- B687's claim "the previous gate's tests read the head's `ci.yml` via `src/audit-dev.test.ts`" is confirmed (line 201), but the test also contains the two labels in its own comments (lines 2, 3, 36, 71): not this PR; recorded as a Note in the kit.

## D-decisions (mine; override any)
- D1. One verdict for the whole PR, same four-state scheme as the template; the severity rule is decided in the kit: Blocker for structure / path / hunk / added-word / reader-red / CI-red / CodeQL; Major SAME only for a falsified comment-only claim or a comment edit that leaves a false statement (M1, M2); Major DIFFERENT for a contradicted builder figure; Note for unsigned commit, ticket key in the title, the lost record pointer, the web-file citations.
- D2. Port block 9830-9839 kept although a finished kit (B633) owns it, because every nearby decade also hits finished kits and the live panes hold none. This matches how the previous kit reused 9720-9729. No server is expected to start, so the block is a precaution.
- D3. Round count named as "0 of 2, round 1 of 2 on class comment-only edit of a CI workflow file", with a clause telling the gate to say so if it thinks the cap already bites (Q1).
- D4. Whole-infra suite is in scope even though the builder skipped it (no Bicep): the project's own Bicep binary is the one shared tool allowed. Expected N=259 at both trees, equal to the main push run's N; any difference is a Blocker.
- D5. The comment-only program must flag a comment-shaped `#` line inside a `run: |` block by the YAML step (builder's own layering note says its strip step alone would pass it); this is the one new instrument over the builder's.
- D6. Model row G2 (line 109), cap row G-cap (line 111), Sonnet `claude-sonnet-5-5` from `models_latest.json` (`levels.sonnet.model_id`, confirmed). Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes and `WED_USAGE_STOP=100`.
- D7. Target 1 hour, hard stop 2 hours, after the gate's own Step 0 and never later than 23:30; the CI wait (SQL Server shards) is the long pole. Shorter than the previous kit's 1h45/3h because there are no plants, mutants or sweeps.

## Q-questions for Tuesday (each with a default)
- Q1. Is this PR the same class as B669/B677 ("reader test for a CI job plus comment-only workflow edit"), so that the cap already bites? Default: NO. Those NO GOs were reader-test leaks; this PR has no reader test; the kit treats it as a new class, round 1 of 2.
- Q2. Should the gate be allowed to name the web-file citations of the two labels (`audit-dev.mjs:2`, `audit-dev.test.ts` lines 2, 3, 36, 71) as a follow-up? Default: YES, a Note only; no lane started.
- Q3. Launch now or after CI completes? Default: launch now; the seat waits on the polls and the verdict stays conditional until all four Analyze runs and the SQL Server shards are complete.
- Q4. Who words the squash message (PR title carries a ticket key)? Default: Tuesday, at landing, using the head-pinned squash command in the kit.

## UNMEASURED
- Nothing of the gate's own runs: no python test, ruby, clone, fetch, worktree, plant or Bicep suite was run by me.
- Whether CI will finish green (7 jobs were in progress; the e2e shards had not been created), and the final CodeQL umbrella conclusion (neutral while pending).
- ruby availability for the YAML step (builder claims 2.6.10; the kit tells the gate to mark the clause UNMEASURED if absent).
- The runner's Python and Bash versions, and the CI Bicep pin (the kit asks the gate to read it).
- The truth of the comment's remaining sentence ("lapsed when npm stopped reporting it") against the records entry the builder relays: the kit makes this a read-only Major SAME (M2) only if the repository contradicts it.
- B687's evidence files (claims) were not opened.

## Outside-the-fences disclosure
- Writes: only the two files above. Plus two scratch files in the session scratchpad (copies of `web/src/audit-dev.test.ts` and `web/src/e2e-runner.test.ts` from `contents?ref=main`, and a one-line control file for the underscore count); nothing in any project.
- Reads beyond the template and builder files: the B687 kit and drafter report (header lines), the B680, B683, B684 kits (grep for `ci.yml` and the one-path lines), all SEAT kits of 10-24 and 10-25 by port scan (names and a 30-character window around each hit), `tuesday/briefs/` listing, `CLARIFICATIONS.md` and `CLAUDE.md` of HPSM-POC by grep, the first lines of the `Briefs/*_STATUS.md` files by `head -1` filtered for `GATE VERDICT`, the first and last lines of B677's STATUS, `model-routing.md` rows 109 and 111, `models_latest.json` by grep, `jira.py` and `search.py` headers.
- Jira: GET of HPSMPOC-351 only, via `.tools/b653/jira.py` (`python3 -I`). No JQL run.
- GitHub GETs under the project GH_CONFIG_DIR: `pulls/218`, `pulls/218/files`, `pulls?state=open`, `compare`, `commits/<head>/check-runs`, `contents` (ci.yml at main and head; the two web test files at main), `rules/branches/main`, `branches/main/protection`, `code-scanning/analyses` for the PR head, `git/matching-refs/heads/b68`. The first `ls-remote` attempt used a bare `git@github.com` URL without the project's key and printed "Repository not found" (no effect); the working form was `git -C 2_Project_Files ls-remote origin ...`. One `gh` output line printed the PR author's login to my terminal; it is in neither file.
- Git in the shared repo: `cat-file -t`, `grep`, `show --stat --format` and `log` (read verbs, `--no-optional-locks`) only.
- Listeners: I opened loopback listeners for under a second on 9830 (bound, not listening) and 9840 (listening) from python as control; both gone (`lsof` rc 1 after).
- No Artifact, Docs, mail, chat, publish or decision-queue tool used; `fleet/briefs_staged/`, the scoreboard, the ledgers, WEDNESDAY / FRIDAY trees and non-Datasec projects were not read.
