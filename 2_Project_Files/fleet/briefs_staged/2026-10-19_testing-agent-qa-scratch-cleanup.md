# Brief: remove Testing Agent MAIN's old Secuura QA scratch clones (maintenance session, not a test session)

From: Wednesday (Kam's coordinator). Written 2026-10-19 for ONE Claude session started in
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/`. Model: claude-opus-5-5 (routing row C4, data-destroying path).

## BLUF
Kam ruled card `wed-devmaster-drive-cleanup-1019` = **b** on the live board at 2026-10-19 11:08:52 AEDT.
Its option text, verbatim: *"The regenerable QA clones and worktrees (285 GB) and gate runs older than 14 days
(11 GB) are removed, with counts and free space before and after. Reports, evidence and mail are kept."*
(The model half of (b) is already done by Wednesday.) Your job is the QA-clone half, inside THIS project only:
census first, then remove only what passes every test below, then report. This is a maintenance task, not a
human-emulation test session: the testing skill's persona moves do not apply, and there is nobody to answer an
AskUserQuestion dialog (Kam does not answer at agent prompts). If anything is ambiguous, STOP and write it in the report.

## Scope (the only paths you may remove)
Directories directly inside `projects/secuura/reports/<report>/` whose NAME starts with `wt`, `work`, `clone`,
`scratch` or `tmp`. Nothing else. Never a file at report level, never `evidence/`, never any `*.md`, `*.json`,
`*.png`, `*.log` or mail file, never anything under `projects/` other than `secuura/reports/*/<those dirs>`,
never anything outside this project folder.

## Step 1 — census (read-only)
For every candidate directory record: path, size (du -sk), newest mtime of any file inside, and what it is:
- `.git` is a DIRECTORY → a standalone clone (removable if it passes step 2);
- `.git` is a FILE → a git WORKTREE registered in another repository. **Do not remove these.** List them with the
  `gitdir:` line they contain. (Removing one would leave a stale registration in another project's repo, which is
  not yours to touch.)
- no `.git` → list it as "not a clone" and do not remove it.
Also record: `df -k /Volumes/DevMASTER` before; total count and size per class.

## Step 2 — the removal test (all must hold, per directory)
1. Standalone clone (`.git` directory).
2. Newest mtime inside is older than 7 days.
3. Nothing has it open: no process has a file or cwd under it (`lsof -nP +D <dir>` returns nothing; if lsof is too
   slow, check every `claude`/`node`/`git` process's cwd with `lsof -a -p <pid> -d cwd`). Re-check this immediately
   before each removal, not only once.
4. Its report folder still holds the report itself (a `*.md` at report level). If a report folder would be left with
   no report, keep its clone and list it.
**STOP conditions (remove nothing more, write the report):** a candidate you cannot classify; any process open
inside a candidate at removal time; the removed count or size disagreeing with the census by more than one entry;
any path outside the scope list appearing in your removal list.

## Step 3 — remove
Build the removal list as a FILE of absolute paths first. Remove each with `rm -rf -- "<literal path>"`, one at a
time, quoted, never a glob, never a variable that could be empty. Never send stderr to /dev/null. Record any failure.

## Step 4 — report
Write `projects/secuura/CLEANUP-2026-10-19.md` in this project: the census table (or its totals plus the kept list),
what was removed (count, size), what was kept and why (worktrees with their gitdir lines, too-recent, open, no-report,
not-a-clone), df before and after, and anything that stopped you. Then end the session; Wednesday reads the report.
Do not commit anything to any repository; do not touch any other project.

## Provenance
- Card text and ruling: read by Wednesday from `decision_queue.sh show wed-devmaster-drive-cleanup-1019` on 2026-10-19 (choice b, ruled 11:08:52).
- "285 GB, 20 to 26 days old": from Wednesday's 2026-10-19 drive survey `0_Brain/reference/2026-10-19_dev-drive-survey/SURVEY.md`, NOT re-measured; your census is the measurement.
- This project's rules (its `CLAUDE.md` line 82: reports are the user's record; rule 5: no destructive action on production data) were read by Wednesday; reports and evidence are therefore out of scope.
