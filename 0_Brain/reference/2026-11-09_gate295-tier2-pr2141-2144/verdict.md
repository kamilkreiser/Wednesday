PR 2141: GO; PR 2142: GO WITH NOTES; PR 2143: GO WITH NOTES; PR 2144: GO

# Gate 295 (tier 2, relaunch): PRs 2141, 2142, 2143, 2144. Findings only. Post nothing.

Method: blobless clone in this session's scratchpad (`.../scratchpad/r`, wrapper `g.sh`), refs `refs/p/<n>` = PR heads. Nothing written in !CODING. Never cd'd (subshell `(cd ...)` only inside scratch dirs for eslint/jest/node). Load1 peaked ~13.7 during my own jest and eslint run (see NOT TESTED for the breach); every later run waited for it to fall under 8.

## PINS (ls-remote, start 22:22:23 AEDT and end 22:39:39 AEDT, diffed): NO HEAD MOVED
develop d0b4825cc244; 2141 40f946de9749; 2142 3ea830e7e22; 2143 a9c3bec846c8; 2144 ca3b5e7fee82; round 1: 2137 8dfe859d9c7, 2139 65954df16a35, 2140 83f861da299c. All equal the commission's pins. (`pins_start.txt` and `pins_end.txt` are in the scratchpad, `diff` rc 0.)
Merge-bases: 2141/2142/2143 = f98afb113c2d; 2144 = 1b3a3ec34a5b (matches the READY).

## Diff versus the held Spark diffs (every difference named)
Command: `cmp.py` extracts the last ```diff fence of each READY_KS-* file and compares the +/- lines per file against `git diff dev...refs/p/<n>`.
- KS-2027 vs PR 2141: 3 files, all IDENTICAL. No difference.
- KS-2142 vs PR 2142: 1 file, IDENTICAL. No difference.
- KS-2150 vs PR 2143: 2 files, both IDENTICAL. No difference.
- KS-2153 vs PR 2144: 2 files, both IDENTICAL. No difference.
Caveat: this compares changed lines only, not hunk headers or context (the PR rebases the same lines onto a newer develop). Numstat per PR: 2141 three files 0/1 each; 2142 one file 4/1; 2143 two files 1/1 each; 2144 cheat 2/2, flow 1/1. These match the READY's table.

---------------------------------------------------------------------------------------------------
## PR 2141 (KS-2027): GO
FOUND: three originate ks1868 test files each lose one `// eslint-disable-next-line @typescript-eslint/no-require-imports` line above `return require(...)`. No other change.
TESTED / HOW:
1. No executable byte changed. TypeScript `transpileModule` with `removeComments`, develop tree vs PR tree: IDENTICAL for all three files (4,286 / 3,660 / 3,615 bytes, sha prefixes 943f4c8e2ce7, 4f42d4eba774, 628fa10dc8a7; the PR body's longer prefixes agree on those 12 characters). Controls (same script): a planted code line is detected as a difference; a planted comment line is not. Run at ES2020 and ES2022, same result.
2. eslint 10.7.0 with the repo's `eslint.config.mjs` (run from the originate package dir), `--report-unused-disable-directives-severity warn`:
   - BEFORE (develop): "62:3, 44:3, 45:3 warning Unused eslint-disable directive (no problems were reported from '@typescript-eslint/no-require-imports')", 0 errors, 3 warnings.
   - AFTER (PR): no output, rc 0.
   - Why they were unused, read at source: `Blockchain/Dev/eslint.config.mjs` line 37 sets `'@typescript-eslint/no-require-imports': 'off'` in `sharedRules` (header comment line 18 says the same). Control: a planted `return require('fs')` in `src/zzplant.ts` and `src/__tests__/zzplant.test.ts` produces NO eslint output, so the rule really is off and the directives suppressed nothing.
   - Whole package `eslint src`: develop 29 warnings, PR 26 warnings, 0 errors both (the 3 are the directives).
3. jest 29.7.0, the three suites, `--rootDir` the package: develop 3/3 suites, 15/15 tests; PR 3/3, 15/15.
4. Merge trees (git merge-tree --write-tree onto develop d0b4825): clean alone (tree 48d2c33e). Clean in the chain of all four, and in the chain of all four plus 2137/2139/2140 (see MERGE section).
5. Questions (4): the PR body and ticket comment 3670f802 claim: three lines deleted (true, numstat), 0 errors and 3 warnings to 0/0 (true), emit identical (true), 15 of 15 (true), "whole-package npm run lint NOT run" (it was not; I ran it, 26 warnings, 0 errors, no objection). Nothing claimed beyond the change. Body "Scope" sentence about PR 2100 and 2079: both exist in my census and touch other files (2100 `ks1868-originate-email-acs-and-smtp...`, `email.ts`; 2079 `services/shared` files). True.
NOT TESTED: see section at end.
Findings:
- G295-2141-1 (Info): the three directives were disabled-by-config, not merely unused: the rule is `off` globally. If someone later turns `no-require-imports` on, these three `require` lines will fire. That is a property of the config, not of this PR (the PR does not change what would have been reported). No action.

---------------------------------------------------------------------------------------------------
## PR 2142 (KS-2142): GO WITH NOTES
FOUND: file `ks1370-two-replicas-and-a-real-boot-race.integration.test.ts`, +4 -1, comments only: the 4 s window comment is reworded (1 line replaced, 1 line added, i.e. 2 lines) and a 2-line may-change mark is added above `it('pin B2 ...')`.
TESTED / HOW:
1. No executable byte changed: `transpileModule` removeComments emit IDENTICAL, 14,704 bytes at ES2022, sha prefix 6e12b7b4938b (exactly the PR body's 14,704 and 6e12b7b4938b975f prefix; at ES2020 it is 14,701, an option difference only). Controls: code line detected, comment line not. With comments the files differ (18,372 vs 18,768), as expected.
2. Each new sentence against the code it describes:
   - "db.ts backs off 1 s, 2 s, 4 s" (pre-existing text) vs `services/security/src/db.ts`: `DB_RETRY_INITIAL_MS = 1_000` (line 93), `DB_RETRY_MAX_MS = 30_000` (94), `retryDelayMs = Math.min(retryDelayMs * 2, DB_RETRY_MAX_MS)` (154, in the failure branch, which logs 'Database still unavailable'). First retry is scheduled at 1 s by `initDb`; fails then doubles, so the third timer is 4 s away after the second failed retry. TRUE.
   - "the database answers while the flag is still down": relay opened after two failed retries (test lines 278-279), then `seen.flagAtWarm = inst.db.isDbAvailable()`. TRUE.
   - "If the event loop stalls past that 4 s, the retry timer can fire first, flip the flag and fail pin B2": see finding G295-2142-1. Partly accurate.
   - Pin B2 mark: "pins what develop does today in that window. A later fix under KS-1370 or KS-1377 may change it; B2 going red then is that change being made, not a regression." The cell (lines 326-333) asserts `flagAtWarm false, flagAfterWarm false, warm valid, cachedAfterWarm true, reloadsBeforeFlip 0, connectionsAfterWarm > 0`: that is what the comment says it pins. TRUE.
   - Line width: longest line in the file is 165 characters before and after (`awk`), new comment lines are 136, 104, 124, 133 wide. Within the body's width claim.
3. Merge: clean alone (tree 6d178274); clean in the combined chains. Open PR sharing the path: PR 2071 appears in my census on this path but it is the merged original (blob at the path in refs/q/2071 equals develop's blob; same subject as develop commit 425ea1d3). No open PR shares it.
4. Bodies: "+4 -1" true; "one comment line reworded and three added" true (1 deleted, 4 added); "Flakiness is UNMEASURED" is the honest statement and the code comment does not claim a measurement; "ticket stays open (Refs)" consistent. The claim "gate saw host load reach 15 but did not run the file" is not checkable by me.
Findings:
- G295-2142-1 (Low): the new mechanism sentence is imprecise about when a stall matters. In the setup, `waitFor('two failed retries')` then `relay.open()` (line 279) then the flag read. The retry timer only flips the flag if it fires AFTER `relay.open()` has bound the listener and BEFORE `flagAtWarm`/`flagAfterWarm` are read. A stall that ends before `relay.open()` makes the timer fire against a closed port, the probe fails again (db.ts 150-160) and the delay doubles to 8 s: B2 does not fail. The comment says only "the retry timer can fire first", which reads as if any stall past 4 s suffices. "Can" keeps it technically defensible and the flakiness is declared UNMEASURED, hence Low. Suggest, if edited: "a stall after relay.open() ...".
- G295-2142-2 (Low): the comments cite `F-2071-1` and `F-2071-2` as if they were findable. I could not resolve them: `git grep -n F-2071` over develop's `Blockchain` returns nothing, and a grep of the brain `learnings/` and `daily/` returns nothing. They are gate-finding IDs from PR 2071's gate (not in the repo). A future fixer reading the file cannot look them up. Not a defect in behaviour; the held diff and PR 2071's ticket text carry them. (A wider grep of 0_Brain and the project history was still running when I wrote this and had returned nothing.)
- G295-2142-3 (Info): the new comment text hyphenates two other tickets (KS-1370, KS-1377). The seat reports this as held, PR text spaces them. Not tested whether a linking integration would attach them from file content (GitHub does not read file contents for linking; Linear attaches by PR title/branch/body). No action.

---------------------------------------------------------------------------------------------------
## PR 2143 (KS-2150): GO WITH NOTES
FOUND: one Figures row of the cheat fragment and one sentence of the flow fragment for KS-2109 reworded: "2 files ... +2 -2" becomes "4 files ... +32 -2: the two edited files +2 -2 (...) plus these two fragments"; "in two files" becomes "in two files besides these fragments".
TESTED / HOW:
1. No executable byte: the two files are `.html` fragments under `Projects Documents/fragments/`, nothing under `Blockchain/Dev` (numstat 1/1 each; `diff --name-only`). Not applicable beyond that.
2. The "real size" figure, checked at the squash commit: `git show --numstat 204e62ac` (subject "Refs KS-2109: two pointers no longer name the role lists that PR 2060 removed", the commit PR 2111 became on develop): AGENT-DOCUMENT-OPERATION-RULES.md 1/1, trustHeaders.ts 1/1, cheat fragment 19/0, flow fragment 11/0. Sum: 4 files, 1+1+19+11 = 32 added, 1+1 = 2 deleted. Matches "+32 -2" and "+2 -2" for the two edited files. The pull head of PR 2111 in my census is 4fff98cb (the body's 4fff98cb12f2); its fragment blobs equal develop's. Fragment line counts on the PR head: cheat 19, flow 11 (unchanged by this PR, so 19 and 11 still describe the merged additions).
   Other sentences in the fragments I scanned for stale sizes (regex for "N files", "+a -b", "one/two lines"): cheat line 3 "one line in AGENT-DOCUMENT-OPERATION-RULES.md" (true), flow line 3 "The two files are independent" (true). No stale 2-file figure left.
3. docs-fragments check, run from a scratch git repo (base commit then all-four-merged commit, with `html_docs_check.mjs` and the two committed pages from develop): base rc 0 "flow 117 legacy + 229 new, cheat 112 legacy + 229 new; lint clean, render passes html_docs_check OK"; after rc 0 with identical output (including the same two ADVISORY lines). Control: appended `<div>unclosed` to the flow fragment gives rc 1 "tags are not balanced: <div> opened 1, closed 0 ... FAIL - 1 finding(s)"; file restored (checked by `git checkout`).
4. Merge: clean alone (tree f1dd3f75), clean in chains. No open PR shares the two paths (PR 2111 on the path is the merged original; fragment blobs equal develop's).
5. Bodies: all claims match (numstat, rc 0 before and after, same counts). One wording difference: body says the ADVISORY line is "the committed cheat page differs from the render at line 6235"; my run printed "the committed page has content after its last rendered entry (hand-appended); run ... adopt" for BOTH flow and cheat, identical before and after. I ran at develop d0b4825, the seat at f98afb11, so the pages differ in state; not reproduced verbatim, and it is identical before and after, so not from the change.
Findings:
- G295-2143-1 (Low): the cheat row now says "4 files against develop, +32 -2". That is the size PR 2111 had when it merged (the fragments in it are the fragments being edited), but "against develop" no longer holds as a present-tense statement: today's diff of those paths against develop is zero. The sister PR 2144 words the same idea better ("as PR 2113 merged"). A reader of the cheat sheet could take +32 -2 as a current diff. Suggest "as PR 2111 merged".
- G295-2143-2 (Info): the READY says PR 2143 is not attached to a Linear issue (read at 11:16). Linear is not reachable from this session; not tested.

---------------------------------------------------------------------------------------------------
## PR 2144 (KS-2153): GO
FOUND: cheat fragment 3 lines (+2 -2: the "Product code changes, by one line" sentence becomes "by two lines (one added, one changed)", and the Figures row "2 files against develop: ... +2 -1 ... +134" becomes "4 files, +165 -1, as PR 2113 merged ... and these two fragments (+18 and +11)"); flow fragment 1 line (+1 -1: "The product change is two lines (one added, one changed; +2 -1)").
TESTED / HOW:
1. No executable byte: fragments only, nothing under `Blockchain/Dev`.
2. Figures against source: `git show --numstat e8d23ce3` (PR 2113 as squashed on develop): test file 134/0, `services/transfer/src/index.ts` 2/1, cheat fragment 18/0, flow fragment 11/0: 4 files, +165, -1. Matches. The product hunk read (`git show e8d23ce3 -- .../transfer/src/index.ts`): one added line `const previousStatus = transfer.status; // KS-2055 ...` and one changed line `fromStatus: transfer.status` to `fromStatus: previousStatus`: "two lines (one added, one changed)" and "+2 -1" are both exactly right, and the old "by one line" in the cheat fragment was the stale one. The two fragments now AGREE: cheat "by two lines (one added, one changed)" with "(+2 -1)" and flow "two lines (one added, one changed; +2 -1)". Fragment line counts on the PR head: cheat 18, flow 11 (match "+18 and +11").
   The whole-fragment scan for stale sizes found none left (the remaining "+134" and "five cells" statements are correct per the 134-line test file).
3. docs-fragments check: same scratch-repo method as PR 2143, rc 0 OK, flow 117 legacy + 229 new, cheat 112 legacy + 229 new, ADVISORY lines identical base vs after; planted unclosed `<div>` in this PR's flow fragment fails (rc 1, 1 finding), restored.
4. Merge: clean alone (tree 6c9ec400) and clean in all chains. Base is 1b3a3ec34a5b (PR 2144 was cut later than the others); no open PR shares the two paths (PR 2113 on the paths is the merged original).
5. Bodies and comment d31bf66d: "+3 -3 over the two files (2 lines in the cheat, 1 in the flow)" matches numstat; "+165 -1" matches. "gate 276's finding G276-1" is not checkable by me. Nothing claimed beyond the change.
Findings:
- None above Info.

---------------------------------------------------------------------------------------------------
## MERGE TREES (question 3), all on develop d0b4825cc244
Method: `git merge-tree --write-tree` chained through synthetic `commit-tree` merge commits (scratch repo only).
- Alone: 2141 rc 0 (48d2c33e), 2142 rc 0 (6d178274), 2143 rc 0 (f1dd3f75), 2144 rc 0 (6c9ec400).
- All four together: clean, commit 315c3c4c. `diff --numstat dev <merged>`: 8 files +9 -9 = sum of the four PRs' own numstats (per PR: 2141 0/3, 2142 4/1, 2143 2/2, 2144 3/3). For each of the 8 files the merged blob equals the PR head's blob (`rev-parse` compare, 8 of 8 "ok").
- All four plus round 1 (2137, 2139, 2140): clean, commit be64c830; 11 files +16 -12 = 9/9 + 7/3 (round 1 numstat: 2/1, 3/1, 2/1). Path overlap between round 1 and round 2 file sets: 0 (`comm -12`).
- Planted control: a synthetic commit editing the same line as PR 2141's db-init file: merge-tree with 2141 CONFLICTS (rc 1, "Auto-merging ..."); the same plant merged with 2142 (a different file) rc 0.
- Open PRs sharing a path: no authenticated GitHub, so no API list of open PRs. Substitute: fetched the heads of every pull ref numbered 2060 and above (86 refs) and listed each one's changed paths against develop (407 path/PR pairs). Paths overlapping ours: only the PRs themselves, and six MERGED originals whose subjects appear on develop (2060, 2105, 2109, 2111, 2113, 2071; blob equality with develop shown for five, 2060 differs only because a later merge edited the file). Round 1's own paths appear with 2137/2139/2140 only. Control: that census contains PR 2127's `start-environment.sh` and two other paths (so the method sees a known PR's files).

## NOT TESTED (said, not inferred)
- The security integration test (needs the security service database, not run, by the same reasoning as the seat); the flake itself is unmeasured by me too. So G295-2142-1 is a reading of the setup order, not a reproduction.
- The 3 originate suites ran under a symlinked shared `node_modules` (read-only use of the project's install). A broader `ks1868` jest run showed 3 other suites failing (documents-lookup-routes, documents-signing-routes, system-errors-ingest) with an identical failing set on develop and on PR 2141 (`diff` of the FAIL lists is empty). I did not diagnose why (likely the borrowed install or a type mismatch); they are not the PR's files and not in the three suites under review.
- The platform suites, tsc for the originate and security files (emit compare used instead), and the PR 2111/2113 "real size" figures from the GitHub files API (read from the squash commits on develop instead: same files, same numbers).
- GitHub PR bodies as posted and the four Linear ticket comments (3670f802, fe750623, 1d206b14, d31bf66d) as posted: `gh` has no login here and no Linear tool. I read the seat's saved copies (`5_Project_History/2026-11-09_seatR-92nd/push/pr_body_ks*.md`, `linear_comment_ks*.md`), which still contain the `@@HOOK@@` placeholder, so the posted bodies may differ. The "all four attach to exactly one ticket" census was not checked.
- Open-PR census covers pull refs 2060 and above only, and cannot tell open from closed without the API.
- Load1: my first jest and eslint runs on develop and the PR ran together, and the load average read 13.67 afterwards (over the limit of 8); I waited until it was 7.77 before continuing and ran the later jest passes with `-w 2`.
- The Spark shadow was not required (commission).
