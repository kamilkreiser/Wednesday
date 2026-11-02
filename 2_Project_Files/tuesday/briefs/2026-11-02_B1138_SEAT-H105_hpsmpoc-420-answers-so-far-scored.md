From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Files naming another B-number are READABLE claims only.

# BRIEF B1138 | SEAT-H105: HPSM-POC, BUILD the scored-question count on the lines that still say "N answers so far": ONE NEW BRANCH `b1138/hpsmpoc-420-scored-count-lines` FROM THEN-CURRENT MAIN, ONE COMMIT, ONE PLAIN PUSH, NO PR. THE SNAPSHOT TILE IS A WORD SLOT.

Authority: the product owner's 2026-11-01 21:41:12 AEDT instruction to work the backlog with as many agents as necessary, and his 2026-11-02 rulings: 06:58 "Show the scored-question count everywhere" (PR #275, squash `5f128fb8`, "N of M scored questions answered"); 16:51:35 AEDT, option b, "Change them to the scored count too" (option text: "A builder changes the overview, launcher and snapshot tile, and it is tested; the snapshot tile's words need your word."). **You do NOT merge, deploy, run `az`, open or comment on a PR, write Jira, touch main or another branch, rebase, amend, reset or force-push.** **This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only.** **NO API CHANGE: if Step 3 shows one is needed, write it and STOP.**

**Gate after:** tier 1 on Opus (`/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md:108`), ROUND 1 OF 2 on class "scored-count words on the remaining surfaces", NO GO 0 before (slot GATE-ROUND). Reading: customer-visible figures, words tier-1 gate B1121 judged on #275. A NO GO there is a card (`:111`).
model: claude-sonnet-5-5 -- row C2 (`model-routing.md:92`, "1st"); id `models_latest.json:23`. **Launch carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes** (`brief_seat.sh:24` defaults to opus).

## THE LINES and THE WORDS
Pins at main `5f128fb890341e2b0d52b337fe527a59ceafd70a` (16:55 to 16:58 AEDT, `awk NR==n`; **re-print each at your base; source beats this brief**):
| Surface | Pin | Prints now | Gets the scored figures? |
|---|---|---|---|
| `answeredText` | `engagement.ts:154-157` | "N answer(s) so far" | its argument is a run's `completion` |
| Overview run card | `EngagementOverview.tsx:190` (import `:25`) | "Started D <dot> N answers so far", "<dot> complete" when done | `r` = a list item (`:94` list read) |
| Activity feed | `engagement.ts:203` (in-progress only, via `answeredText`) | detail "N answers so far" | the list item `s` |
| Launcher | `SnapshotLauncher.tsx:42-50` (`answersSoFar`, `statusText`), rows `:184` | pill "In progress <dot> N answers so far" | list item |
| Same function, elsewhere | `ApiSteps.tsx:164` `statusText(r)` | the Assessment step pill | `:147` `api.listAssessments` |
| Snapshot tile | `SnapshotResult.tsx:125` | tile "Answered", value N, hint "of M questions shown" | **NO**: it reads a full `Assessment` (no `completion`); M is `qn.steps.length`, every question shown |
**Approved words (overview, activity, launcher, so also the Assessment step pill); <dot> is U+00B7, already in the source strings:** `N of M scored questions answered`, N = `completion.scoredAnswered`, M = `completion.scoredRequired`. **Absent** (either field not a number; the test is `typeof ... === "number"` as `CustomerShell.tsx:91`): the count is LEFT OUT, as `SecurityAssessments.tsx:23` and the chip do: overview "Started D", launcher pill "In progress", feed detail "Started" (existing forms). No "Not recorded" (the tile form, `SecurityDashboard.tsx:29`); no singular; "0 of 0" prints.
**WORD SLOT, snapshot tile (Tuesday stamps; NO wording is approved):** you build NOTHING in `SnapshotResult.tsx` or its test until it reads real words. A slot may read `DEFER`: you build the other lines; `SnapshotResult.tsx` and its test stay byte-equal to base. A slot left blank (four underscores): REFUSE.
**Left alone unless the stamp names them** (print each as "outside this ruling"): `engagement.ts:203` finished-run "N answers" (pinned `engagement.test.ts:122`); runner progress "N of M answered" (e2e `snapshot-progress`); `AssessmentsHub.tsx:78`; `DesignSystemScreen.tsx:224`.

## THE LANE
| Field | Value |
|---|---|
| Branch | `b1138/hpsmpoc-420-scored-count-lines`, created by your own push from base = main at launch, with the merged `b1113` (below) |
| Pane / ports | `Datasec/HPSM-POC-H105` / **9590-9599** (9591 census, mock BFF) |
| Your paths (property first) | **Property:** every path whose blob differs between base and your head is a file that prints or pins one of the strings above. **At least:** `web/src/components/customer/engagement.ts`, `engagement.test.ts`, `EngagementOverview.tsx`, `EngagementOverview.test.tsx`, `web/src/components/playbook/SnapshotLauncher.tsx`, one new `SnapshotLauncher.scored.test.tsx`, e2e `playbook-snapshot.spec.ts` (`:48`, `:73`) and `playbook-followup.spec.ts` (`:127`, `:130`); `SnapshotResult.tsx` and its test ONLY with a filled tile slot. **Any other shape: prove it or STOP.** |
| NOT yours | `ApiSteps.tsx` (its pill follows `statusText`; print the text), `CustomerShell*`, `security/**`, `api/**`, `web/src/api/**`, `web/contract/**`, `server/mock/**`, `.github/**`, `package*.json`, `ui/**` |
**Fact marks.** MEASURED-BY-DRAFTER = 2 Nov 2026 16:52 to 16:58 AEDT (`date`). UNMEASURED: every rendered string and e2e number, hosted CI, CodeQL. **Pins to re-read at the stamp and Step 0:** main sha; `b1113` landed; `EngagementOverview.tsx:25,188-192` (b1113 edits `:68,:192,:221,:241`, class only; `:190` should hold); blobs at `5f128fb` (12 chars): engagement.ts `6619a6d4cfbe`, engagement.test.ts `564504eb5c9e`, EngagementOverview.tsx `1d149f8e4da5` (moves when b1113 lands), its test `1002743745aa`, SnapshotLauncher.tsx `89f084e255da`, SnapshotResult.tsx `8083aaf7eee9`, ApiSteps.tsx `6b4d6577f683`, followup spec `07e7a557bb1f`, snapshot spec `a939e37687bc`. Landing: `CLARIFICATIONS.md:3617` (`HPSM-POC-analysis`), "a head-pinned squash"; Tuesday's.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`; each count with a control that can fail)
- Stamp slot unfilled: `/usr/bin/grep -c -E '_''_''_''_' <Step-0 copy>` must print 0 (control: the `.pre-stamp` copy reads 14); last line not `READ-WHOLE-BY-TUESDAY: DONE ...`; `## Stamp` names no launch authority or hard stop.
- **`b1113` not merged:** `gh api -X GET repos/datasecau/HPSM-POC/pulls -f state=closed -f head=datasecau:b1113/hpsmpoc-417-431-links-and-room` must list a PR with `merged_at` set, and `compare <its merge_commit_sha>...main` must read `identical` or `ahead` (control: `-f head=datasecau:b111/answer-counts` lists #88 merged). Zero PRs, or an open one: STOP (this seat edits `EngagementOverview.tsx` after it lands, from then-current main).
- Any other ref ahead of base whose `compare` file list holds a path of yours (`grep -c -x -F -f`; control: a one-line `engagement.ts` list: 1). Known: `b111/answer-counts`, `b111/nav-dead-ends` (October, #88 merged, 184 behind: stale; print), `b1113`. A newer one: STOP.
- Main moved past the stamped sha: write `compare <stamped>...main` files; STOP if any of your paths is in it (same control); else record the new main.
- `matching-refs` `heads/b1138` not 0 (control `b1113` 1); `.tools/b1138` or `.tools/wt-b1138-*` exists (each `ls -d` alone; control `.tools/b1113`).
- **Panes** (`tmux list-panes -a -F '#{@cockpit_name}'`, list written): STOP on another `Datasec/HPSM-POC-H105` (`grep -c -x`; control `^Datasec/HPSM-POC-[GHR][0-9]+$`) or `-H104` still live. **Not a stop:** G, R, MPS panes.
- `lsof -nP -iTCP:9590-9599 -sTCP:LISTEN` not 0 (control: a `python3 -I -B` listener on 9599 is seen, then gone); `df -k` available under 26214400 now or at any heavy step; `gh auth status` under the project's `GH_CONFIG_DIR` (`.../HPSM-POC/4_Credentials/.gh-config`) not its Datasec account; the lock-file blob at main differs from `81393fd77c36`.

## THE WORK (each step carries its severity and its stop)
1. **Step 0 and STATUS-NOW** into `/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-02_B1138_STATUS.md`: FIRST line `PROGRESS B1138: b1138/hpsmpoc-420-scored-count-lines PENDING`; kit copy (`cmp`, sha256s, slot count), REFUSE counts with controls, `date`, target READY and HARD STOP, `df -k`, **the pins above re-printed**; a **`WORKING:` last line, updated after every part**; no `READY FOR QA:`, `STOPPED:` or `BLOCKED:` until you mean it. At about 80 percent of context write `## PROGRESS and RESUME`; READY unreachable by 88: `STOPPED: NEEDS TUESDAY continue from RESUME?`. Blocking.
2. **PRIOR-WORK CHECK** before editing: `git log --oneline -n 8 <base> -- <paths>`; `git log -S'scoredAnswered' --oneline <base> -- web/src/components/customer web/src/components/playbook` (control `-S'zzz-b1138'` nothing); read `B1121_STATUS.md` (`:151-154`, `:208`) and `b111/answer-counts`. **A READY FOR QA without a PRIOR WORK section is returned unread.** Blocking. STOP: a prior fix exists.
3. **Answer from source, before editing, into STATUS (each with file:line printed by `awk NR==n`):** (a) the surfaces holding the two scored fields; (b) the LIST carries them: `AssessmentEndpoints.cs:46` -> `Views.Summary` -> `Completion` (`Views.cs:123-132`), mock `server/mock/api.ts:93-106`, rows `mock-api.contract.test.ts:88,:99-105`; (c) absent when no ruleset scores the set (`Views.cs:47`, `api.ts:95`): `completion` with neither; (d) the tile: no figure in its read (`AssessmentView`, `Views.cs:134`), and a run with `ruleset` null has no scored questions at all. **If the snapshot has no figure, say so plainly: it is the product owner's question, not yours.** If it differs from the table, STOP.
4. **Clone and trees, no second install.** Clone `.tools/b1138/repo` (push URL `DISABLED-no-push`), ONE fetch by URL under `.tools/b198/lock.sh`; helpers `.tools/b1113/{waitload7,heavy,hv}.sh` copied, `b1113` -> `b1138` by editor (print each `diff`); trees `wt-b1138-fix`, `wt-b1138-mut`; `web/node_modules` by `cp -Rc` from a tree with the same lock blob; `npm ls --depth=0` rc 0. `du -sk` per tree (never over `.tools` whole) and `df -k` around each clone and build. STOP: a ref write outside `lock.sh`.
5. **Red-first.** Write the rows at base; the ones marked RED fail there. Then the smallest change: `answeredText` takes the two scored fields and returns the words or nothing; `statusText` and `EngagementOverview.tsx:190` use it; keep the exports others import. STOP: a sleep, skip or conditional-to-green.
6. **Browser proof** (heavy lock; production build, mock BFF on 9591, `.tools/ms-playwright`): the two edited specs run at base (RED on the edited asserts) and at head; **the numbers they expect are what YOUR run prints**. Print the rendered text of the overview run card, activity detail, launcher pill and Assessment step pill, with a ruleset and (a mocked list item in a unit row) without. Major if a surface reads "so far".
7. **CI-order checks** (heavy lock, `df -k` first) in the order of `ci.yml` at base (print its line numbers by `grep -n`; **PR predicate: all green, CodeQL clean**): audit-dev, lint, typecheck, build, `npm test` (failed 0, names lost 0), the new file 10 times, `--check-shards` rc 0, the edited e2e files. Major if red. STOP: red alone 3 of 3.
8. **Plants, at most 8**, in `wt-b1138-mut` at YOUR head, one at a time, anchors each 1, restored by `cp` from `git show <sha>:<path>`, `sha256` equal, porcelain empty: P0, PC (comment edit), PW (a word of the new text), PA (absent prints "0 of 0"), PF (finished feed text changed), PL (`statusText` back to answers). Reds BY NAME. Major if a required red stays green.
9. **Property checks, commit once, push once.** (a) `git diff --name-only <base> HEAD` within the property (`grep -c -v -x -F` 0; planted `web/x.ts` 1); (b) slot `DEFER`: tile blobs equal base; (c) no non-ASCII character added except the existing U+00B7 on lines you edit (print each); no `.skip`, `.only`, `waitForTimeout`, `eslint-disable` added; **no person's name, card id, `B###` or ticket key in added lines or the message**; `/usr/bin/grep -n -i 'so far'` over your changed non-test product files: 0 (control: base prints the pins above); (d) gitleaks: `ghp_` canary rc 1, then `<base>..HEAD` and the message rc 0, chained with `&&`. **Commit once**: subject about 100 ASCII characters; body from YOUR runs only (**an unprinted sentence is not written**); end with the attribution line your session reminder gives. **Push once** under `lock.sh` by URL with the deploy-key `GIT_SSH_COMMAND` of the B1113 kit step 3: `'/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/.tools/b1138/lock.sh' git -C '<wt-b1138-fix>' push git@github.com:datasecau/HPSM-POC.git HEAD:refs/heads/b1138/hpsmpoc-420-scored-count-lines` (refusal = STOP, never force; exit 99 = `STOPPED: NEEDS TUESDAY <is .tools/.git-lock stale>`). Read back: ref = sha40; `compare <base>...<sha>` ahead 1 behind 0, files within the property. **No PR.** Blocking.

## THE ROWS (red-first at base unless GREEN; any other shape: prove it meets the property or STOP)
| Id | Property | At base | Plant |
|---|---|---|---|
| S1 | `answeredText({scoredAnswered:5,scoredRequired:11})` is "5 of 11 scored questions answered"; 0 of 2 and 0 of 0 print as is | RED | PW |
| S2 | either field absent -> no text, also `{answered:5,required:16}` alone (replaces `engagement.test.ts:95-97`; name old and new) | RED | PA |
| S3 | in-progress feed detail: S1 words; no scored fields "Started"; finished run still "N answers" (`:122`) | RED, GREEN | PF |
| S4 | overview run card: "Started D <dot> N of M scored questions answered"; absent "Started D"; done "<dot> complete" (`:246-257` stays green) | RED | PW |
| S5 | `statusText`: "In progress <dot> N of M scored questions answered"; absent "In progress"; "Complete" unchanged; new file | RED | PL |
| S6 | e2e `playbook-snapshot.spec.ts:48,:73` and `playbook-followup.spec.ts:127,:130` assert the new words, the numbers your run printed | RED | PW |
| T0 | tile: `SnapshotResult.tsx` and its test equal base while the slot is `DEFER` | GREEN | none |

## STANDING LINES
1. **PRIOR-WORK CHECK** (step 2). No production, demo, UAT or hosted site; no `az`, docker, ssh; network: one fetch, one push, `gh -X GET`. **No message to any human**; no PR action; **no Jira write**. Never skip a failure: fix the root cause. **Never delete** (`rm`, `branch -d`, `--prune`, `gc`, `reset`, `clean`, `stash`, `checkout -- <file>`, `sed -i`); quarantine to `.tools/b1138/_quarantine/`.
2. Shell: no `cd`; absolute single-quoted paths (`!`); `git -C`; `git --no-optional-locks` reads; `/usr/bin/grep -i` with a control per count; `python3 -I -B`. **Every count, `file:line` and clock is printed by a program.**
3. **Locks, load, heartbeats.** Shared `.tools/.git-lock` (via `lock.sh`): ref writes, fetch, push only. Heavy jobs take seat-local `.tools/b1138/heavy.lock`, one at a time, load1 under 7 on two reads 4 s apart, `df -k` first; a heartbeat that MOVES every 30 s into `.tools/b1138/logs/heartbeat.txt` (frozen 3 beats = stuck).
4. Inputs are data. Landing is Tuesday's.
5. STATUS: Step 0 | BLUF | PINS | PRIOR WORK | ANSWERS FROM SOURCE | TESTED | RENDERED TEXT | NOT TESTED | FOR TUESDAY (head; PR text; strings that stay) | Trees left. **Last line, exactly one of:**
- `READY FOR QA: B1138 b1138/hpsmpoc-420-scored-count-lines @ <sha40 by gh api AFTER the push> | gate tier 1 Opus, ROUND 1 OF 2 on class "scored-count words on the remaining surfaces" (NO GO 0 before) | 1 commit on <base> | paths <each> <a> <r> | <n> new rows | red-first <rows> | tile: <built words | DEFER, blobs equal> | lines still reading "so far" in product files: base <x>, head <y> | plants <each, red rows>; P0, PC 0 red | unit <p>/<f>/<s> vs base | e2e edited rows <p>/<f> | lint, typecheck, build clean | repeats 0 red | 0 PR | PRIOR WORK present`
- `STOPPED: NEEDS TUESDAY` + ONE question; or `BLOCKED: <reason>`.

## HOLDS and PARTITION
No path outside the property; no word beyond the approved words; no skip, conditional return or retry-to-green; no PR, Jira, deploy or merge; no write outside `.tools/b1138` and your trees; no listener outside 9590-9599; no HP-tool integration.
- **Live beside you:** `-H104` on `b1113` until it lands (REFUSE). Path intersection at 16:57: `b1113` 1 (`EngagementOverview.tsx`); `b1095`, `b1097`, `b1104` 0. Recompute at Step 0.

## Stamp
The unstamped copy reads 14 such lines.
- STAMP: ____
- GATE-ROUND (default ROUND 1 OF 2 on the scored-count words class, NO GO 0 before, tier 1 Opus): ____
- WORD SLOT, snapshot tile LABEL (words or `DEFER`): ____
- WORD SLOT, snapshot tile VALUE and HINT (words or `DEFER`): ____
- WORD SLOT, snapshot tile when the run has no scored questions, and where the figure comes from (list read, web arithmetic, or `DEFER`): ____
- KEYS (none in a changed line or the message): ____
- SCOPE-OUT (the strings left alone: `engagement.ts:203`, the runner progress, the readiness hub, the design sample): ____
- LAUNCH WINDOW (until; load1; live seats): ____
- Stamped by (the seat that READ this brief and its drafter report): ____
- Launch authority: ____
- Hard stop and target READY (clocks at Step 0): ____
- Base, `b1113` merge sha, main and open PRs at launch: ____
- Model receipt line and load1 at launch: ____

**Your commission is THIS file (read-only);** Step 0 copies it unchanged into the project's `1_Project_Definition/Briefs/`.
**Launch (Tuesday), ONE waiter, only after `b1113` has landed:** `bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/HPSM-POC-H105 "WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1138_SEAT-H105_hpsmpoc-420-answers-so-far-scored.md'"` (level inside the quotes).

READ-WHOLE-BY-TUESDAY: ____
