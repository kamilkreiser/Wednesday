From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to.

# BRIEF B199 (SEAT G): HPSM-POC RECORDS: land the nine unmerged records branches as ONE catch-up branch, post Friday's item 1c ruling on HPSMPOC-232, record the owed items
**From:** Friday (laptop seat), 01:31 AEDT 2026-10-11. **Seat:** Datasec/HPSM-POC-G (your commission is the newest `Briefs/` file containing `_SEAT-G_`). Datasec / HPSM-POC only. Report `Briefs/2026-10-11_B199_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · Records). **The last line is `READY FOR REVIEW` or `STOPPED: NEEDS FRIDAY` followed by ONE question.**
**Tier:** records + Jira only. **No product code, no deploy, no setting, nothing on Azure.** Nothing pushed to any `main`.

## 1. Records catch-up (analysis repo `datasecau/HPSM-POC-analysis`)
**What Friday measured (GitHub API via the Datasec identity, 01:3x AEDT 2026-10-11; re-read it yourself first):**
- Merged PRs list (`gh pr list --state merged`): records PRs merged through **#110 records/b194** (10-10 02:12Z). There are **0 open PRs**.
- Records branches on origin with NO merged PR: `records/b186-a3`, `records/b186-a4`, `records/b187`, `records/b188`, `records/b190`, `records/b192`, `records/b195`, `records/b196`, `records/b198` (nine).
- `compare main...records/<b>` ahead/behind at 01:3x: b186-a3 1/4 · b186-a4 2/4 · b187 1/2 (277 files) · b188 2/2 · b190 1/2 · b192 1/1 · b195 2/0 · b196 3/0 · b198 1/0. **Ahead counts do NOT prove "unlanded"** (a later branch may carry the same content, e.g. b186-a34 was merged as #108). Measure per file.
- origin main's `CLARIFICATIONS.md` ends at **C-82** (B194); `records/b198` adds **C-83** (`Briefs/2026-10-11_B198_STATUS.md` § Records).

**Do:**
1. For each of the nine, classify every file it changes against origin main: SAME BLOB on main (landed by another route) · DIFFERENT (main has a newer version; say whose) · ABSENT from main (unlanded). Table in the STATUS: branch · files · same/different/absent · verdict (LANDED / PARTLY / UNLANDED).
2. Build ONE branch `records/b199-catchup` from origin main in your own worktree. Cherry-pick the UNLANDED commits in C-number order. Conflicts are resolved ADDITIVELY: `CLARIFICATIONS.md` keeps every C-entry once, in number order (a duplicate number from two branches is a STOP, not a renumber); `5_Project_History/history.md` keeps every entry, newest at top; nothing a branch added is dropped. A file that is DIFFERENT on main is left as main has it, and named.
3. Before pushing: gitleaks per staged path (with a canary that must be caught), and a content check for the HOLD below (counts only; never print the matched text). Push `records/b199-catchup` only. Friday opens the PR and merges it after CodeQL and the checks.
4. **Never delete a branch or a worktree.** The nine source branches stay on origin.
5. **Also from Friday's 2026-10-10 pre-HP-review screen, item 15** (`FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-10_hpsmpoc_screen_pre-hp-review.md:27`, read by Friday 01:3x): the **B189 and B193 STATUS files and their evidence are UNTRACKED in the root working tree and on no branch**. Check that this is still true (`git --no-optional-locks status --short` in the root checkout; never a git verb that writes there), then COPY them (never move) into `records/b199-catchup`, through the same scans.

## 2. HPSMPOC-232: post Friday's item 1c ruling (one BLUF comment; read the ticket and its newest comments first, `first:`-style newest-first read, and do not duplicate anything already there)
Post this text verbatim under a `## BLUF` heading, then `## Detail` with the C-83 line from B198_STATUS (quote the log line, do not retype it):
> Item 1c, Friday's ruling (2026-10-11): reading (b) is accepted on ONE start. C-83: the first signed-in `GET /api/v1/customers` after the a50b22d start took 2,298 ms; the caller stage was 1,679 ms = lookup 582 + write 1,035 (the write is 61.6 %), against C-82's 6,197 ms. The write is the demo user's app_user create/refresh (ADR-A15). The warm-ups' "reads only, no write" rule is Friday's own design rule from brief B182 (2026-10-07), not a Kam ruling or a C-number, so the remedy is Friday's to rule. Nothing changes before HP's layout review on Tue 13 Oct (fixes only until then). After it, the candidate is a start-up warm-up that exercises the app_user write path inside a transaction that is ROLLED BACK, with a test that fails on any committed write and a before/after row count; the B182 rule becomes "no persisted write", it is not dropped. A second hosted start's number is wanted before building, because one start is one data point.

## 3. Record the owed items (BACKLOG.md on `records/b199-catchup`, one row each, with source + date; the gate notes go to Jira)
- **B197 M-1** (gate B197's Minor: test coverage) — copy the gate's own wording from `Briefs/2026-10-10_B197_STATUS.md`; do not paraphrase.
- **Dependabot alert #1 (high), dev-only, no fix published:** npm `braces`, `web/package-lock.json`, scope `development`, GHSA-vfj7-8cjw-p6xm, `first_patched_version` null (Friday's read of `GET /repos/datasecau/HPSM-POC/dependabot/alerts?state=open`, 01:3x). Re-read it; record which top-level dev package pulls it in (`npm ls braces` in a scratch copy, never in place). **Do not dismiss the alert** and change no dependency this round.
- **Gate B189 notes m-1 and N-1..N-6, and gate B193 notes N-2..N-7** (screen item 15: Jira text "B189" had 0 hits on 10-10). Search Jira for each note first (by the gate id and by the note's key words); file what is unfiled as ONE HPSMPOC ticket per gate with the notes as a checklist (Kam's one-ticket-per-logical-path rule), copying the gates' own wording. Name the searches and hits in the STATUS.
- **HSTS on the hosted web root:** measure `Strict-Transport-Security` on the hosted web root and on the API root (`curl -sI`, 3 reads each), and find whether any earlier STATUS (B191, B194, B198) recorded it. Record the measurement and the comparison; change nothing.

## HOLDS
- **No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool — Claude seats, subagents, the product's model, Ornith or the Spark — without HP's written approval (signed SOW §4.1.4(c)).**
- Datasec only; no other client's names, tickets or paths anywhere.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert; never ask for a bypass.
- Nothing to HP or any human outside the team; Jira comments are BLUF-first and say what was measured and how.
- Never delete; quarantine. Never edit a running script. Processes you start are stopped by PID with a cwd check.
- If a measurement contradicts this brief, the measurement wins: say so in the STATUS and STOP if it changes what you would do.
