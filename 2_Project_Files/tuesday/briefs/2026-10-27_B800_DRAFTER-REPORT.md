STARTABLE: YES

# B800 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H43: HPSMPOC-356 part B734-3 only, one branch, one commit)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B800_SEAT-H43_hpsmpoc-356-strip-invisible-space.md` (120 lines, shape of the B768 kit; 8 lines with the four-underscore pattern, control from the same file; 0 non-ASCII bytes; the at-sign pattern 0). Drafted Tue 27 Oct 2026 from 09:47 AEDT (`date`), Sonnet 5.5, read-only. Path: `infra/tests/test_ci_workflow.py` only. Branch `b800/hpsmpoc-356-strip-invisible-space` off main `d415a3fe172e3fe1e392c51e8c883f1a3d759990`.

## BLUF
- Startable now. Pins hold: main `d415a3fe` (ls-remote), no `b800*` ref (control: `b797*`, `b709*` list), open PRs #232 and #222 share 0 paths with the lane (control: planted path reads 1), ports 8870-8879 free, no kit names H43 or B800 (95 kits scanned, control fired), no `.tools/b800` yet.
- **Findings that change the design (all measured on copies in the scratchpad):** (1) The three invisible-space plants are GREEN on main (`r_trailing_nbsp`, `r_trailing_u3000`, `n_nbsp_trailing`, plus a leading U+00A0); the controls (trailing U+200B, inner U+00A0) are RED in the one test `test_the_shard_job_has_exactly_the_pinned_steps_in_order`. (2) Fixing line 322 alone turns all four red, but a U+00A0 right BEFORE the `@` of a `uses:` stays equal under line-322-only and differs only when line 336 (`uses.split("@", 1)[0].strip()`) is changed too; the kit therefore changes BOTH sites (both inside `step_identity`, within the gate's "in step_identity"). (3) A U+00A0 AFTER the `@` sha stays equal under both: the ref is not pinned (B734-6), so it is pinned in the kit as by-design behaviour. (4) A sibling strip site is NOT closed by the fix: the aggregator env test (line 697, `RESULT: ${{ needs.api-sqlserver-shard.result }}` plus U+00A0) is green on main and with the fix. Kept out of the lane (Q-1).
- Main moved since the B768 kit: the file is now blob `7a1563a6` (823 lines; B768's docstring edit landed as #230). Reader on main: 34 OK under 3.14.7 and 3.9.6.
- Narrowing said in the kit: B734-9 (line-break code points) and B734-6 (unread bodies, `with:` inputs) are rulings, NOT in scope; the ticket stays open; no Jira write.

## Facts re-measured (instrument; control that can fail)
- Main and blobs: `ls-remote` + `git rev-parse d415a3fe:<path>`; `ci.yml` raw bytes by `gh api -X GET contents` + `git hash-object` = `0176b491...` = the clone's rev-parse (the bytes-are-the-file control).
- Open PRs and files: `gh api -X GET pulls`, `pulls/<n>/files` under the project's `GH_CONFIG_DIR`; `grep -c -x -F` per list; planted-path control 1.
- Plants: one python program, `ci.yml` copy with ONE edit each (`count(old) == 1` asserted), run under `python3 -I` against the main reader, a `.strip(" \t")` at line 322 only (fix1) and at lines 322 and 336 (fix2). Table: control_unchanged OK/OK/OK; nbsp, u3000, leading-nbsp, name-nbsp OK on main, FAILED (1 red) on fix1 and fix2; benign trailing space+tab OK everywhere; zwsp and inner-nbsp controls FAILED everywhere.
- Direct `step_identity` probes (clean-equal = leak): NBSP before `@`: leak on main and fix1, red on fix2; NBSP after the `@` sha: equal everywhere; trailing NBSP on a `run:` or a name: leak on main, red on both fixes.
- CI predicate: `ci.yml` job `infra` (line 576, `BICEP_VERSION` line 581) runs `validate.sh`, which runs `test_security_baseline.py`, which runs every `infra/tests/test_*.py`; pass predicate written into the kit. Runner Python UNMEASURED.
- Ports: `lsof -nP -iTCP:8870-8879 -sTCP:LISTEN` empty (rc 1); word-boundary scan of 95 non-`.pre-` SEAT kits of 26 and 27 Oct: no hit (control `x 8871 y` 1, `x 18871 y` 0). The drafter ran NO positive lsof bind control in this pass; the kit makes the seat run it at Step 0.
- Panes: `tuesday`, `Datasec/HPSM-POC-G168`, `Datasec/NexusAI-M19`, `Datasec/MPS-G167`, `fleet-monitor`.
- Model: `model-routing.md` lines 85 (L6), 92 (C2), 109 (G2); `models_latest.json` `levels.sonnet.model_id` = `claude-sonnet-5-5`; `brief_seat.sh` line 24 defaults to Opus (so `BRIEF_SEAT_LEVEL=sonnet` is in the launch line).
- Landing: `rules/branches/main` = `deletion,non_fast_forward,code_scanning,required_status_checks`. Squash convention RELAYED from earlier landings (e.g. #230).
- Ticket: HPSMPOC-356 read whole through `.tools/b649/jira.py` (Backlog, 1 comment: the records note of #230's landing, which says the Done-when is NOT met).

## D-decisions (drafter's, for Tuesday to accept or change)
- D-1: change BOTH strips (lines 322 and 336), not line 322 only, because of the measured before-`@` leak.
- D-2: ONE new test method in `SqlServerShard` beside `test_the_shard_job_has_exactly_the_pinned_steps_in_order`; the existing method is not edited; delta 34 -> 35.
- D-3: rows at two levels: unit rows through `step_identity` and file-level rows over `shard_job()` text (the three named plants), all special characters as escapes so the file stays ASCII.
- D-4: red-first on a copy of main with only the new method; six listed mutants of the fix (strip back to default at either site, a tab no longer stripped, U+00A0 or U+3000 added to the strip set, a left-only strip); a survivor is a defect of the rows.
- D-5: a row pins "U+00A0 after the `@` stays equal" as by-design (the ref is not pinned), flagged as not a promise.
- D-6: target READY 80 min, hard stop 140 min, tier 2 gate, round 1 of 2 on a new class (the kit assumes NO GO 0 of 2; Tuesday states the round at stamp).

## Q-questions for Tuesday (each with a default)
- Q-1: close the sibling strip sites (the aggregator `RESULT` line 697, and lines 723, 725, 754) in the same commit? Default: NO. Not B734-3's named shape; the seat measures one NBSP plant per site and names them under FOR TUESDAY; Tuesday decides a follow-up.
- Q-2: write a Jira comment or transition? Default: NO Jira write (list B734-9 and B734-6 as left open under FOR TUESDAY; a records seat comments after landing).
- Q-3: gate round and tier? Default: tier 2, round 1 of 2 on the new class.
- Q-4: pane name? Default `Datasec/HPSM-POC-H43`, ports 8870-8879; the sibling builder is H44 (ports 8880-8889) and the gate G168 holds 8860-8869.

## UNMEASURED
No worktree, commit or new test was built. Not measured: the whole `test_security_baseline.py` run and its test count at `d415a3fe`; whether `.tools/bicep/bicep` is `v0.47.16`; the runner's Python; whether the 3.9 failure of `test_resource_hygiene` (RELAYED from the B772 gate) still holds at `d415a3fe`; GitHub's and MSBuild's handling of a trailing U+00A0; the six mutants (never run); the sibling strip sites beyond the one `RESULT` plant; no lsof positive control; the B801 kit does not exist yet (the sibling's paths are taken from the commission and PR #222's file list).

## Outside-the-fences disclosure
Wrote only the two files named. Read-only commands: `git --no-optional-locks` ls-remote, rev-parse, show, log, grep, config (with the key path elided) in the project clone; `gh api -X GET` under the project's `GH_CONFIG_DIR` (pulls, pulls/files, contents raw, rules/branches); `gh auth status`; one run of the project's Jira helper `.tools/b649/jira.py` for HPSMPOC-356 (output to the scratchpad, no token printed); `lsof`, `tmux list-panes`, `uptime`, `date`; python runs on copies in the session scratchpad (`tcw.py`, `ci.yml`, `plants.py`, `tcw_fix1.py`, `tcw_fix2.py`, layout folders) with the two interpreters. One slip, disclosed: the first Write of the kit turned the escape text for U+00A0 and U+3000 into raw characters (2 lines, 4 characters); I replaced them with the escapes and re-read 0 non-ASCII bytes. I also ran `ls` on `.tools/` to look for `b800`-named folders, and one earlier `grep -P` call failed on macOS grep (no effect). No decision_queue, staged-briefs, scoreboard, ledger, WEDNESDAY or FRIDAY tree, other project, hosted host, az, ssh or docker was touched. A glob of `.tools/` listed folder names `b80`, `wt-B80-*` (older, unrelated to B800; names only).
