# B335 DRAFTER REPORT (Composer PR #83 round-2 tier-1 re-gate, SEAT-G22)

Drafted 2026-10-20 18:55-19:05 AEDT. Deliverable: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B335_SEAT-G22_composer-gate-pr83-round2-tier1.md` (about 60 KB, 2 slots on 3 lines). Nothing else written. No Artifact, Docs, mail, chat or publish tool used.

## What I read
- Whole: B331 gate brief (template, 101 lines incl. Tuesday's rulings at read), B331 STATUS (485 lines, in two reads), B333 STATUS (276 lines), B333 brief (150 lines), B332 brief (round-2 example, 93 lines).
- Read-only listings: Tuesday's `briefs/` (port grep, B335 absence, slot names in B331/B333/B334 `.pre-stamp` files), the project `.tools/` and `2_Project_Files/.tools/` directory names, `.tools/b331/sql/` file names and `.tools/wt-b331-probe/**/b331-*` file names (names only, contents not opened).
- Not read: `CLARIFICATIONS.md`, K ruling text C-86..C-96 (brief carries B331's and B333's quotation of them), any source file of the PR (no `git show` of the migration body, recipe or tests; I took their content from B333 STATUS as RELAYED and marked it so).

## Facts I measured (instrument, time)
All 2026-10-20 AEDT, read verbs and `gh api` GETs under the Composer `.gh-config`; no fetch, no worktree, no merge-tree.
- 18:55:20 `git ls-remote origin` main / branch / `refs/pull/83/head` / `refs/pull/82/head`: main `318df1767035e92a55f633824927ce01b9986293`; branch and PR ref `8e062d94549ee027c5ed66924bce45f33904e9e0`; #82 head `e62889831069135abc25e61b08f2f59f8196e4fd`.
- 18:55 `gh api pulls/83`: open, draft true, head 8e062d94, base `d8d2a2c74a909d508dbc593d5429ac0af1a484bb`, commits 5, changed_files 19, +2646/-41, mergeable null, mergeable_state unknown.
- 18:55 `gh api commits/318df176…`: parents = [d8d2a2c7], files = only `packages/content/src/b20-codeql-redos.test.ts` and `packages/engine/test/s47-crf2-linear-detector.test.ts` (squash message "B301 … (#82)"). Agrees with Tuesday's 18:2x read.
- 18:55 `gh api pulls?state=open`: only #83.
- 18:55 `git log 314f40d9..8e062d94` (3 commits, shas and subjects quoted in the brief) and `git diff --numstat 314f40d9 8e062d94` (6 files, +657/-12; sums check against PR totals: 2001+657-12 = 2646).
- 18:55 `pulls/83/files`: 19 paths with per-file additions/deletions (migration +80, recipe +70, DEPLOY.md +50).
- 18:55:41 `commits/8e062d94/check-runs`: CodeQL, Analyze (csharp), Analyze (javascript-typescript) all completed success. `code-scanning/analyses?ref=refs/pull/83/head`: both languages at 8e062d94 and at 314f40d9, results_count 0. Open alerts on the PR ref: 0.
- `git show 8e062d94:…/0022_exception_review_and_scope.sql | shasum -a 256` = `8195ecb7307b54001260d396a5f38b2b9f3331fa6dfe4d5e4a1ded0d4b539717` (equals B333's claim). `git grep` of that value at the head: `DEPLOY.md:280` and `down.sql:38`; old value `965a8ea1` file count 0.
- `gh api contents/packages/db/migrations?ref=318df176` and `…/rollback`: newest 0021 (`0021_policy_target.sql`, `0021_policy_target.down.sql`).
- `git cat-file -t 318df176` in `2_Project_Files`: "could not get object info" (object not local, so the gate must fetch it in its own clone; the brief says so).
- 18:55 `ls-remote 'refs/heads/b335*' 'refs/heads/b301*'`: only the b301 control line. `ls briefs | grep -c B335` = 0; project `Briefs/` has no B335 name.
- 18:55:41 `uptime`: 2.15 1.91 2.25.
- Slot check: `grep -c -E '@SLOT:[A-Z0-9_]+''@'` on the brief = 3 lines (STAMP_TIME once, MAIN_SHA twice); the B331 `.pre-stamp` control prints 1, so the control mechanism works.

## Port block chosen: 7570-7579
Justification: `grep -hoE` of all 4-5 digit numbers in `2026-10-20_*` files shows the named blocks 7230-7389, 7400-7549, 7550-7559 (B333), 7560-7569 (B334; confirmed in B334 brief text "Port block `7560-7569`"), 7620-7629, plus single 7637 (HPSM firewall addendum). `grep -nE '\b757[0-9]\b|\b758…|759…|760…|761…'` found hits only in the B333 files, which use "7550-7619" as a read range for `lsof`, not an assignment; no assignment anywhere names 757x. `lsof -nP -iTCP:7570-7579 -sTCP:LISTEN` rc 1 (unfiltered control: 11 lines). The block is a reserve; the db route binds nothing.

## Disagreements between sources (source wins)
1. **Tool location.** B331 put kit and trees at the PROJECT ROOT (`<project>/.tools/b331/`, `wt-b331-*`, confirmed by `ls`). B333 put its own at `2_Project_Files/.tools/` (confirmed: `b333`, `wt-b333-fix/-mut/-red` exist there). The brief follows B331 (project root) and tells the gate to say which it uses.
2. **PR 83 is not at main.** User's facts say main moved to 318df176 while PR base stays d8d2a2c7; confirmed. B333's merge predictions used main d8d2a2c7 and PR #82's head `e6288983`, not the squash; the brief makes r10 re-predict onto the new main.
3. **mergeable_state.** B331 saw `clean`; at 18:55 GitHub still reports `unknown` / `mergeable null` (B333 saw the same right after its push). Brief treats it as a value to report, not a refusal.
4. **B333 file-list wording.** B333 STATUS says the delta is "3 commits, 6 files"; both confirmed. B333 STATUS says its `git diff d8d2a2c7..HEAD` is "17 plus my 2 new files" = 19; confirmed by `pulls/83/files`.
5. **B333 census control number.** B333 says `device_group` appears in 191 files at 314f40d. The delta adds two test files naming it, so the gate may read 193 at head; the brief tells the gate to report what it reads.
6. **B331 STATUS lines vs B333's quoting.** B333 cites B331 STATUS `:395` for the "single-column FK" premise; confirmed at line 395. Line-number cites in the brief are to the files as I read them.

## Choices I made that you may want to change
- Added a "same-id DELETE then INSERT" path check inside r1 (the freeze does not stop a re-created group id in another engagement; the scope trigger fires only on `exception_record`). I did not measure it; I told the gate to measure, grade by the floor and put its reasoning in one paragraph. This is the one place the brief could produce a new Blocker against a ruling-adjacent behaviour (B331 already accepted stored ids of deleted groups as "narrowing").
- Allowed the gate to read and copy B331's probe files (named exception, modelled on B332's B319 exception), never run in place. Contents unread by me.
- r6 does not require re-running the base and round-1 suites (B331 measured them); only the head, unless a number differs.
- Merged-tree check is: merge-tree rc 0 plus tree-diff = #82's two files plus typecheck/lint/db/B333 tests, with the full suites optional if the tree equals head plus two files.

## Open questions for Tuesday, with my recommended answer
1. **Slot values.** Fill `STAMP_TIME` with the launch time and `MAIN_SHA` with `ls-remote main` at launch. Recommended: if main is still `318df176…`, use it; if it moved, read the diff and re-draft the main-related lines before launch.
2. **`PC_E8_SOW_TEXT` for the unit step.** Recommended: confirm exactly as for B331 (path in the brief's stamp section); if not, unit rows are NOT TESTED.
3. **Own-container removal.** Recommended: allowed, as B331 (exact names, after logs saved).
4. **Launch load.** Load was 2.15 at drafting; recommended launch while load1 < 7.
5. **Same-id delete+insert grading.** Recommended: keep the check but, if you want to keep the cap clean, rule beforehand that a same-id re-create is a Note (it needs a deliberate DELETE plus INSERT with a chosen old uuid, nothing in the API does it, no reader of the scope exists). I left it to the gate by the floor sentence; ruling now removes the risk of a late NO GO on something B333 was never asked to fix.
6. **Hosted database that applied round-1 0022.** The brief asks the gate to test that the recipe refuses the old checksum and raise it as FOR TUESDAY. Recommended: accept as written; no hosted database has run 0022 (B333 STATUS `:272`), so it informs only.
7. **Model.** Opus (G1) with `BRIEF_SEAT_LEVEL` unset, as B331. Recommended: yes, this is the cap round.
