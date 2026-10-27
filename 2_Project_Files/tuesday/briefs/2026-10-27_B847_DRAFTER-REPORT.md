STARTABLE: YES

# B847 drafter report (SEAT-J28, Composer, fix round for PR #99)

Drafted 2026-10-27 20:1x-20:2x AEDT by Tuesday's read-only kit drafter (Sonnet 5.5). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B847_SEAT-J28_composer-99-fix-round-whitespace-pins.md` (133 lines, 61233 bytes).

## BLUF
- The kit asks for ONE commit on top of `dc16530a` (same branch, plain fast-forward) touching only the test file: 13 rows stay 13; `sectionLines`, `collapse`, `routeB`, `STOP_LINE` and the ten old rows stay byte-equal to main (so no old row can change verdict, and the PR stays additions-only against main). New: `pinned()` (trims only ASCII blanks, collapses only runs of space and tab), `exactBlock()` (lines split on `\n` only, same count and indexes as `routeB`), `shown()` (escapes non-printable-ASCII in messages), `lostBy()` (a 0 to 0xFFFF loop proving `pinned` keeps every other character, with the `collapse` negative control), `oddEdits()` tables (NBSP after, CR after, NBSP before; a CRLF entry), titles W and G reworded.
- Red-proof is a closed family K stated as a PROPERTY: `KT` 40 ids (8 chars x lines 200/201/205/206/207), `KP` 10, `KI2` 50 (every ASCII space of those five lines), `KC-block`, `KC-all`; plus the round-1 battery, controls c0-c4 and a sixth control (swap `pinned` back to `collapse` in a scratch copy: the new reds must go green), plus the gap census (reported, not widened). Three files in one vitest call per mutant: main's file, the round-1 file, the new file.
- Identity: REFUSE 7 reads the author pair by program from the main squash commit, never typed, never printed; the commit uses `git -c user.name -c user.email commit`; after-checks require no `localdomain` in `%ae` and `%ce`.

## Facts re-measured (instrument, control)
- J28 free: `/usr/bin/grep -l -w -F 'J28'` over the `2026-10-2[67]_*` briefs printed nothing; control J27 printed 3 SEAT kits; J29 also nothing. Next free B-number: no B847 file or Composer `B847` STATUS existed.
- Ports 9410-9419: scan of 142 non-`.pre-` SEAT kits of 26/27 Oct with `grep -l -w -E '941[0-9]'` (run from a bash script file) = 1 kit (B758, prose, lists 9410 as a "zero-claim decade"); every other decade of 9400-9999 has at least 2 kits. `lsof -nP -iTCP:9410-9419 -sTCP:LISTEN` empty (rc 1); `python3 -I` bind of 9410 succeeded. Control `892[0-9]` = 2 kits. 9690-9699, 7700-7709 and 9960-9969 avoided as told.
- Branch: `ls-remote` main `cbe86ba6...`, `refs/heads/b839/composer-routeb-command-line-pins` = `refs/pull/99/head` = `dc16530a9c3c4e484a54e8d2e01717bad31c355b`, `refs/pull/99/merge` `8cdfdf8b...`; no `b845*`/`b847*`. PR #99: open, not draft, 1 commit, 1 file, +166 -0, `mergeable_state` clean. Open PRs #95/#91/#86/#85: 0 shared with the test path or `DEPLOY.md`.
- Blobs (hashed with `git hash-object` after `gh api -X GET` raw contents): test at `dc16530a` = `a6416face225a1aa28503059ac4597e15873e2ec` (708 lines, 31124 bytes, 13 `it(`, 0 CR, 0 non-ASCII, 0 tab); main's test `ef544f90...` (542 lines, 10 `it(`); `DEPLOY.md` `8359bace...` (628 lines, 0 CR). Block lines: write 200, redirect 201, stop 204, DROP 205, cat 206, apply 207 (repr printed).
- Identity: `gh api -X GET repos/datasecau/Datasec-Security-Composer/commits/cbe86ba6` author email domain = `users.noreply.github.com` (committer `noreply@github.com`); the 8 latest main commits all carry that same author email; `dc16530a` author and committer email domain = `<host>.localdomain` (control for the seat). The name/address is not written in the kit.
- Model: `model-routing.md:92` row C2 (S55 1st), `:85` L6, `:109` G2; `claude-sonnet-5-5` at `models_latest.json` lines 23 and 38. Panes: `%0 tuesday`, `%93 Datasec/NexusAI-R72`, `%90 Datasec/MPS-M48`, `%1 fleet-monitor` (no Composer pane). Landing rule `CLARIFICATIONS.md` line 1799 present. Load1 5.99 at 20:09.
- Stamp: 9 lines with four underscores (8 slots + last line), 0 non-ASCII bytes in the kit.
- Design check (scratchpad node script, a re-implementation of `pinned` + `wholeLineProblems` + `groupProblems` over the real DEPLOY.md text, NOT the test): real block gives no problem; the 100 K ids give a problem or lose a line (0 green); spaces per line 9/3/23/1/14 = 50, matching the gate's count of 50.

## D-decisions (mine, for Tuesday to accept or strike)
- D1: `sectionLines`/`collapse` NOT changed (the gate asked the drafter to decide and state). Reason: they are main's lines used by the ten old rows; changing them breaks additions-only and would change old-row verdicts on CR mutants (property 4 of round 1). A new `exactBlock` gives the new rows the `\n`-only split with identical indexes. Proof the seat must print: old10 column equals main's file on every mutant.
- D2: the stop line 204 gets a NBSP entry in the G table (G compares it with `pinned` now, so the title is true for it; it is not one of the gate's out-of-family Notes).
- D3: interior characters are backed at the `pinned` level by `lostBy` (all code points at the start, inside, end), not by per-line row entries (interior swap of the apply line's last space would break `APPLIES` and prove nothing about the new compare); battery KI2 covers every interior space from outside.
- D4: O table gets only duplicate-with-odd-character entries (write, DROP, apply); redirect and cat are not counted by O.
- D5: title wording fixed in the kit (binding words) so the seat does not invent claims; each backed by an assertion listed beside it.
- D6: sixth control (swap `pinned` for `collapse` in a scratch copy, KT-206-nbsp and KP-206-nbsp must go green) added so a new red cannot come from something else.
- D7: the round-1 battery is rerun in full plus the gap census (reported not widened), since the round-2 gate re-runs it.
- D8: gate tier stated as TIER 1 round 2 of 2 per the ruling; budget suggestion 14 container jobs, target READY 2h / hard stop 3.5h after Step 0.

## Q-questions for Tuesday (each with a default)
- Q1: the round-1 commit `dc16530a` keeps its machine-local author in PR #99's history, and a squash of #99 may list it as a `Co-authored-by` line; a new commit cannot change that (amend and force are forbidden). Default: the seat reports it under FOR TUESDAY; Tuesday reads the squash body before `gh pr merge` and removes the line if the web UI or `--body` leaves it in.
- Q2: the kit makes the seat rerun the round-1 gap census; it adds container time. Default: keep (cheap inside the same loop container).
- Q3: titles W and G are reworded, which edits round-1 lines only; if you want the old title text kept and only the claim narrowed, say so. Default: the kit's words.

## UNMEASURED
Whether the changed rows are green at main's DEPLOY.md and each K id red on the predicted row (no vitest, container or mutant against the test was run); how many KI2 ids make the extractor throw; the exact A9 text; psql's answer to `-q<NBSP>` or a DROP-only stdin; whether GitHub lists the round-1 author in a squash body; battery wall time; `lostBy` speed over 65536 code points.

## Outside-the-fences disclosure
Wrote only the two files above, plus three scratch files in the session scratchpad (`ports.sh`, `ports2.sh`, `kits.txt`, `head.ts`, `main.ts`, `DEPLOY.md`, `sim.mjs` under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/e99936d2-bd93-49e6-9ad3-72eeb5729550/scratchpad/`). Reads: the gate STATUS (98 lines) and ruling whole, the round-1 STATUS (first 14000 bytes) and kit, the gate's `mutant-table.txt` (grep of ids only), `launch_when_cool.sh` and `brief_seat.sh` headers, model-routing lines. `gh api -X GET` only under the Composer GH_CONFIG_DIR; `git ls-remote` only. A first port scan was invalid (zsh does not word-split `$F`; it printed a false zero, caught because the 892x control printed 0) and was rerun from a bash script with xargs; the kit carries that warning. No fetch, build, vitest, decision_queue, Jira, mail or tool outside the list.
