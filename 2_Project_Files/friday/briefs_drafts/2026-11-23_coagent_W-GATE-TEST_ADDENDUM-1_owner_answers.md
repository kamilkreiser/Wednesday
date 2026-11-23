This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_W-GATE-TEST_brief.md`. Seat W-GATE-TEST only. Nothing in the brief is withdrawn; two things are added. Finish the step you are in, then read this whole.

# W-GATE-TEST ADDENDUM 1: the owner answered the card (the PC's model runs are allowed), and one sentence of his goes into the project's clarifications file

## 1. RULED BY THE OWNER: the model runs on his PC
The owner's answer on his board, 2026-11-23 12:10:32, card `general-c2c-windows-gate-test-runs-1123`, verbatim:

> Decision general-c2c-windows-gate-test-runs-1123: a — Yes, up to 70 runs, the helper on its own

Option a on the card read: "Yes, up to 70 runs, the helper on its own", detail "Two sittings of about 30 to 45 minutes each (estimate), no one at the keyboard; every run reported to me and summarised to you".

What it changes for you:
- Stages B and C of the brief's section 7 are no longer locked by the card. They are still ordered AFTER stage A: no model run on the PC before stage A's no-model results are back and you have recorded them. Write the lock line in your STATUS as `STAGES B AND C: ALLOWED BY THE OWNER (ADDENDUM 1); RUN ONLY AFTER STAGE A IS RECORDED`.
- The ceiling is 70 model runs in all, counted by the runner: 32 per set-up, 64 planned, at most 6 repeats for void cases. The runner REFUSES to start a run that would pass the ceiling it is given (a parameter, default 35 per sitting), and prints its count at the end.
- The helper runs them on its own: your command list for stages B and C must need no person at the keyboard (no prompt to answer, no window to switch). If a case cannot be run unattended, say which and why: `STOP Q<n>`.
- Unchanged: you make no model run yourself; the smallest model, its id passed in; the owner's settings files checksummed before and after; nothing installed; nothing needing Administrator; the "without Git" set-up only by hiding it from the test's own process tree, with its first case as the probe.
- When stage A's results are recorded and your tree is ready for the runs, your last line is `RUN ON PC REQUEST: <full sha> — STAGE B` (and later `— STAGE C`), with the exact command list above it, as for stage A.

## 2. The owner's product direction: his words go VERBATIM into the project's clarifications file as C-2
File: `coagent/1_Project_Definition/CLARIFICATIONS.md` (in the project folder, OUTSIDE the git repository; it exists and holds C-1; read it first and keep its form). Add, as the newest entry, numbered C-2 (or the next free number if the file has grown), dated 2026-11-23 12:10 (live board), naming the card `general-c2c-allow-mode-meaning-1123` and saying that he answered with a note and chose none of the card's options. His words, exactly, with his own spacing and spelling (two spaces after "permission." and after "choice."; "its" as he wrote it):

> one user clicks allow, Claude on that machine keeps displaying what its doing but no longer asks for permission.  the other user can do the same or approve each action depending on their choice.  The choice lasts the entire session but can be changed at any time

Add nothing of your own to his words: no reading, no summary. After writing, compare the sentence in the file by program with the sentence in THIS addendum (the quoted line above) and show that they are identical, with the character count; show the file's whole text in STATUS under "ADDENDUM 1"; report the C-number. C-1 must be byte-identical to what it was (show its checksum before and after, or a diff of the file limited to added lines).
This file is added to your owned list for this one entry only. It is not part of your branch.

Friday's reading of that sentence is NOT part of the file and is not an instruction to you: it changes nothing in what you build. One line for your "what C3b needs" section only, tagged as the coordinator's reading and not the owner's words: the product's two modes are chosen per machine by its owner (approve each action, or allow with the actions still shown), so a gate on Windows will need both, and the test you are building (can the hook block at all) is the precondition of both.

## 3. Also: main moved
`origin/main` is now `3768a67d1d41b47439776657afbc114bd14bc439` (documentation only: four `.md` files changed against `3164374`; lane SESSION-FINDINGS). When you next fetch, merge it into your branch (never rebase). Both lanes append to `BACKLOG.md`: keep both sides' entries.

After ANY context compaction, re-read the brief, this addendum and your STATUS whole before writing anything more.
