This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_W-GATE-TEST_brief.md`. Seat W-GATE-TEST only.

# W-GATE-TEST ADDENDUM 11: the independent check says NO GO at `3838bd5a84e39523157f7877dc40fc5d6d22fc88`, FOR THE RECORDS ONLY; a fix round of text; NO runner change, NO PC run, NO model run

**Read the verdict WHOLE first:** `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_W_GATE_TEST_verdict.md` (353 lines; READ-ONLY; its scripts and outputs are in `m1_review/gate_w_gate_test_tests/`). Friday has read it whole.

**What it CONFIRMED, and what therefore is not to be touched:** every count in your record equals its own count on the PC's saved mails; all 14 raw copies differ from their mails in the ruled placeholders only; its own judge, written from the case table, agrees with the runner and with both your re-judges on all 64 cases; the test CAN fail (the made file, a missing error result, the wrong mode, a hook never called, and two deliberately broken builds of the real hook each came out FAIL; every refusal of the runner fired); the failure cases are what they say; the look-alike is named honestly and its list of what it does not prove stands whole in RESULT.md. Your work on the substance stood up to a hard check. Thank you.

## RULED BY FRIDAY: the fix list (CLOSED; anything else you think needs changing is a `STOP Q1`, not an edit)

**Rule over all of it: NO runner or code file changes** (`w1.py`, `run.ps1`, `cases.tsv`, the stub, the W4 program, any `.rs`, `.toml`, `.lock`): the committed runner must stay the one that ran on the PC. Only `.md` files, the `raw/` copies, `BACKLOG.md`, `docs/M0-OUTCOMES.md`, and the two additions named under m5 change.

**M1 (Major): session ids in the raw copies.** Friday rules they come OUT at the head (the other lane of today redacts them; this one will too).
1. In every committed raw copy replace each Claude Code session id by `<session-id>` wherever it stands (the `session_id` fields, inside `transcript_path`, the two stream init lines), each `prompt_id` value by `<prompt-id>`, and each `toolu_…` id by `<tool-use-id>`. Do it by PROGRAM, and count each class per file in that file's header, as you did for the work folder. A raw copy must still differ from its saved mail ONLY in the placeholders: say so with your own line-by-line comparison against the saved mails (the check's `rawcmp.py` shows one way).
2. Your names scan gains the classes session id, prompt id and tool-use id, each with a positive control taken from a saved mail; print its output over every added line at the new head.
3. NO history rewrite and no force-push: commits `3330813`, `462faca` and `8044dc0` keep them. Extend the BACKLOG history-sweep line to those three commits and this class, and add that `main` already carries session ids in older spikes' committed streams (the check counted 99 distinct; give the number as the check's, not yours, unless you count it), for the same sweep before any publication.

**M2 (Major): `RESULT.md:105-106`.** "Every blocked case's tool result names the exec-form command" is contradicted by the mails for W3, W6, P3 and P6. Say what the mails show: the hook-failure cases' results name the command (F3, F4, F7, F9: the hook program or the missing program; F5: the stub's crash command); for the four deny cases the result holds only the stub's reason, and it is the stub's log (the witness) that shows the real hook delivered the event. Check each case named in your new sentence against the saved mail before you write it.

**M3 (Major): `docs/M0-OUTCOMES.md:84-91`.** Add to the "W1 PASSED" statement: with the smallest model (`claude-haiku-5-5`), on one PC that is not a clean machine.

**m1 (Minor): the probe is judged on the first case only.** No code change. One BACKLOG line: in the look-alike configuration the runner's judge passes a later case whose own session lists Bash or Monitor; for this record it was covered by the per-case re-judges (yours and the check's, all 32 lists); before any future look-alike sitting the judge must FAIL such a case. Say in RESULT.md, in one sentence, that the tool-list claim for cases 2 to 32 rests on the re-judge of the returned lists, not on the runner.

**m2 (Minor): F6 and F8.** Tag the statement that they "fail open" REASONED in RESULT.md (and wherever else it stands as RAN): what was returned shows the files were made, and nothing returned shows the hook ran in those two cases; the reasoning is F5 and F7, the same cases apart from the failure rule. One BACKLOG line for a future run: a witness for the crash and missing roles.

**m3 (Minor): stale text.** Update the document lines the verdict names (BACKLOG's first C3b entry "nothing has run on Windows"; RESULT.md's "UNRUN ANYWHERE" and "`raw/` empty until"; M0-OUTCOMES' "never run anywhere" and "0 findings so far"; your STATUS is history and stays). `run.ps1:1` is code and stays as ruled in ADDENDUM 10.

**m4 (Minor):** `docs/M0-OUTCOMES.md` and `cases.md` each get one sentence naming the three things the look-alike did not exercise (shell-form hooks routed to PowerShell; the stricter failure rule of a PC without Git; how Claude Code finds Git Bash); `cases.md:9` says "Git present, then the look-alike".

**m5 (Minor): the two re-judge programs.** Commit both (`W_GATE_TEST_rejudge_returned.py`, `…_C.py`) into `spikes/W1-windows-exec-hook/` beside the raw copies, unchanged, after your names scan has read them; say in RESULT.md that they are record tools, not part of the runner. They are the ONLY new non-document files of this round.

**Notes:** n1 (say that 4,078 is the committed copy's length and 4,054 the PC's line); n2 (the symlink row worked because Developer Mode is on); n8 ("about 3.8 s for the others" becomes the measured range); n3, n4 and n5 each become one line in your "what C3b needs" list (a release build has not run on Windows; a plugin-loaded hook and a ConfigChange case; the real daemon's ask, halt and error answers); n6 one BACKLOG line for the policy's owner (a hard link inside the workspace to an outside file is classed inside, the same on POSIX). n7: no change.

## Rules of this round
- For every changed sentence give OLD and NEW in STATUS.
- `git fetch origin`; if `origin/main` has moved (the lane `allow-measure` may merge before you and appends to the same two documents), merge it INTO your branch (never rebase), keep both sides' lines, and say so. At this moment it is `3768a67d1d41b47439776657afbc114bd14bc439` by Friday's ls-remote.
- Print in STATUS at the new head: `git diff --name-only 3838bd5 HEAD` and, of those, the count of `.py`/`.ps1`/`.rs`/`.tsv`/`.toml`/`.lock` files that are NOT the two added re-judge programs (must be 0); `git diff --quiet 462faca HEAD -- spikes/W1-windows-exec-hook/w1.py spikes/W1-windows-exec-hook/run.ps1 spikes/W1-windows-exec-hook/cases.tsv` (exit 0); product diff 0 bytes; removed lines in the two documents against main 0; the widened names scan with its controls; the raw-copy comparison; `w1.py selftest` on the Mac (44 PASS expected: the runner did not change).
- Last two lines of STATUS: the full head sha, then `READY FOR QA W-GATE-TEST r2` (or `STOP Q1`). ONE short check of this round follows. Friday's clean-clone merge check of `3838bd5` is already running; because this round changes no runner and no product file, she will show the diff to your new head is documents, raw copies and the two record tools only, and not re-run it.

After ANY context compaction, re-read the brief, all addenda and your STATUS whole before writing anything more.
