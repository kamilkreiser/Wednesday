From Tuesday (Kam's Datasec coordinator seat), Datasec / Security Composer. Your STATUS file is the channel: `1_Project_Definition/Briefs/2026-10-19_B289_STATUS.md`. A question = last line `STOPPED: NEEDS TUESDAY` + ONE question.
# BRIEF B289 · SEAT-R2: finish B287's records commit (one commit, local, nothing else)

**Model:** claude-sonnet-5-5 (routing C2). **Pane:** `Datasec/Security-Composer-R2`. **Stamp:** 2026-10-19 18:5x AEDT, by Tuesday. **Port block:** none.

**BLUF (MEASURED by Tuesday with read verbs, 18:5x AEDT):** B287's STATUS last line says `RECORDS DONE: B287 records/b287 @ <PENDING ...>`, but `records/b287` still points at `main` b57b6071 (no commit). In its worktree `.tools/b287/wt-rec`, `git status --short` shows ` M 1_Project_Definition/CLARIFICATIONS.md`, ` M 5_Project_History/history.md`, ` M BACKLOG.md` (C-79 and C-80 headings present, count 2). The brief copy, B287's STATUS and `2026-10-19_B287_evidence/` are not in that worktree's index. B287's pane is closed. Your job is to make B287's ONE records commit exactly as B287's brief specified, and nothing else.

**Read first, whole:** `1_Project_Definition/Briefs/2026-10-19_B287_SEAT-R1_composer-demo-minio-read-and-fix-draft.md` (section RECORDS and standing lines) and `1_Project_Definition/Briefs/2026-10-19_B287_STATUS.md` (its Records section and FOR TUESDAY 6, the fold collision).

**Steps:**
1. In `.tools/b287/wt-rec` (branch `records/b287`): read `git diff` of the three modified files and check against B287's RECORDS section: BACKLOG row #319 appended only (no old row changed: compare old rows' bytes, control a planted 1-byte change is reported); C-79 and C-80 in the C-entry shape with Kam's verbatim words; one history entry at the top. Anything that does not match: STOP and ask, change nothing.
2. Copy into the worktree (cp, then cmp): the brief copy `Briefs/2026-10-19_B287_SEAT-R1_…md`, `Briefs/2026-10-19_B287_STATUS.md`, `Briefs/2026-10-19_B287_evidence/` EXCLUDING anything B287 quarantined (`.tools/b287/_quarantine/` stays out). Also this brief's copy and your own STATUS are NOT part of B287's commit.
3. Words scan and gitleaks over the staged set (known false positive `CLARIFICATIONS.md:213` only; a planted canary fires), then ONE commit with B287's identity rule (`git -c user.name=… -c user.email=…` copied from `git log -1 --format='%an <%ae>' main`; never edit git config). Message: `Records: B287 C-79/C-80, BACKLOG #319, history B287, B287 brief + STATUS + evidence (B287, committed by B289)`. `git diff --stat main..records/b287` lists only those paths (quote it).
4. Do NOT fold into main, do not touch the root checkout's untracked collision files (Tuesday folds later), do not push (0 remotes), never delete (quarantine to `.tools/b289/_quarantine/`), never touch `.tools/b285*` or branch `b285/*` (B285 is live).
**Last line, exactly one of:** `RECORDS COMMITTED: B289 records/b287 @ <sha40 by git rev-parse records/b287>` · `STOPPED: NEEDS TUESDAY` + ONE question.
Shell: no `cd`; absolute paths; `/usr/bin/grep -i` with a positive control for every count; take times from `date`. No production, no demo, no network calls, no message to any human.
