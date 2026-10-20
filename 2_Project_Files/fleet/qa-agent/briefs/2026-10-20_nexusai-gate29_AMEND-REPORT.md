# Gate 29 (RD-774 + RD-836, PR #97) — AMENDMENT 1 report (RE-PIN 4c9b0d3 → 278afc25), for Tuesday

Drafted 2026-10-20 from 12:56:14 AEDT (by `date`) to about 13:15 AEDT by a read-only drafting agent (Sonnet 5.5). This agent only read and measured. It wrote the files listed in §1. Nothing was launched, mailed or published; the launcher, `inbox_routing.conf` and every other file were not touched.

## 0. BLUF

- **PR #97's head is `278afc25dda22ed8511d33e3e1cd12b0afde3487` (tree `ee819f2126593465b352d91ae293fb3c55b9a75b`); main is `39653db4b56adb6d4e526c90531cd4cdf23022e0` (tree `704c442b78a36baea66fef2349a5acbdbff114b5`).** `ls-remote` read both at 12:56:23 AEDT (rc 0, first attempt) and again at 13:10:40, unchanged. Both match the relayed mail. The kit now pins `278afc25` and its tree everywhere, and keeps the history in one line near the top plus the `.pre-repin-278afc2` backup (cmp-identical).
- **Mode 0 still applies.** `39653db` is an ancestor of `278afc2` (`merge-base --is-ancestor` rc 0; `rev-list --left-right --count` `0 7`; GitHub compare `ahead_by 7, behind_by 0`). The head is the gated tree; nothing is merged and no counts are regenerated. The MAIN pin stays a slot (`@SLOT:MAIN_SHA@` ×2, `MAIN_TREE`, `MAIN_LANDED`); the stamp line now reads `landed since 39653db`. **The C-57/C-133 counts-conflict handling no longer applies** (WRONG 2 superseded: every gate-28 head is on main, and S101O's own TURNs `2566713` and `f1a2e76` took the counts conflicts).
- **Rows 5 and 6 of the builder's census are IN scope and gated; rows 7-11 are OUT (RD-868, relayed).** The kit's census (r2) and admin-gate matrix (r7, r7S) now attack POST `/api/settings/risk-definitions` and POST `/api/validate-condition` with and without `saveToDatabase`. The gate's own whole-backend census stays the instrument. My own `git grep` reproduces the builder's call sites and finds none outside its 11 rows, and lists what the builder's method did not cover (WRONG 7a). **T6 existed because the Settings path bypassed RD-836 at 4c9b0d3; e884516 gated it, so T6 and r7S now test the new gate.**
- **CR/LF log forging is now a checked property (r10).** The builder routes 23 risk-condition log lines through `logSafe`; `git grep -n 'logSafe('` at the head gives 24 call lines (the 23 + the #272 line), listed in the kit. The gate must build its own sink census and forge via PUT, the settings writer and validate-condition, with positive controls on base and on the pre-gate tree `2566713`. New mutants M13-M16 attack the two new gates and two of the new sinks.
- **CodeQL at `278afc2` reads clean:** three analyses listed (js/ts `1985321634`, actions `1985312931`, python `1985312531`, all results 0), 0 open alerts on `refs/pull/97/head`, #273 and #272 `fixed`. **One landing-checklist fact changed: ten more main alerts (#172, #173, #175, #176, #178, #179, #180, #184, #185, #186) sit on lines that no longer exist at the head,** so the old kit's "#172 still open" control is wrong. Closure stays unclaimed (C-209); the kit swaps the control to #171, #174, #177, #181.
- **The launcher `launch_qa_nexusai_gate29.sh` still pins the old head, main, counts and READY copy and MUST be re-pinned before `--check` (§4).** I did not touch it (outside my write list). Counts at the head: 4910/303 (relayed; blob `57659c6c…` is measured), M0 4880/302, so a moved M0 predicts **M0 + 30 / + 1**, no longer + 24.

## 1. Files written

| file | what | sha256 |
|---|---|---|
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate29-rd774-rd836.md` | the kit, AMENDED (250 → 265 lines, 116,977 → 153,791 bytes, 124 substitutions, 46 diff hunks) | `2e519e8916b199a104bebf33c7e897e5c71c77badb8ddf5e785efdc209fb6ccd` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-19_nexusai-gate29-rd774-rd836.md.pre-repin-278afc2` | `cp -p` copy of the pre-edit kit; `cmp` against the original printed `CMP_EQUAL` | `0efe6a52e0d9048068f54b9bddfe120d08132cf4ace8a605fbe5d6a7dc6e2e3e` |
| `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-20_nexusai-gate29_AMEND-REPORT.md` | this report | — |

The slot multiset is identical before and after (diffed): 17 occurrences, 17 names. I filled none and added none.

## 2. What changed in the kit

The full edit list (124 substitutions, old → new, original line numbers) is in §2a at the end of this report. By area:

- **Top:** title now names the re-pin; a new **RE-PINNED 2026-10-20** paragraph after line 3 gives the reason, the four commits (`2566713`, `e884516`, `f1a2e76`, `278afc2`), the main move, the mode-0 proof, what was rewritten, and the launcher warning. The "What is new here" paragraph and the item paragraph carry the new head, tree, base, the seven-commit first-parent chain with every tree, and "backend/ is byte-identical from e884516 to 278afc2".
- **READY paragraph:** the new-head mail is cited as RELAYED with the seat file's size and sha256; the kit says it is not yet saved as a delivered copy.
- **THE RE-PIN STEP, MAIN-STAMP line, PIN-HEADS RD774 row, "Every head is a pin":** re-based to `39653db` (7 commits, `0 7`, 21 over `888203c`). The MAIN row is still the slot.
- **TIER / 2a-T:** six gated routes; line anchors re-measured; the Settings-viewer row (expected 200 at 4c9b0d3) replaced by five rows: settings POST as viewer (403) and admin (200), validate-condition save as viewer (403), validate-condition without a save (200, open), both routes in the C-01 window (200).
- **WRONG items:**
  - **1, 2, 3:** gate 28 complete and landed; WRONG 2 superseded; three forward merges now.
  - **4:** 8-path set re-measured (same 8 paths); new numstat; new blobs for `server.js` and the rd774 test; unchanged blobs listed.
  - **5:** counts 4880/302 (M0), 4910/303 (head, blob `57659c6c`), +30/+1.
  - **6:** `PLANTED_SQL` re-read, unchanged.
  - **7:** line numbers marked moved. **New 7a:** the builder's 11-row census against my grep.
  - **8:** superseded by e884516.
  - **9:** three HTTP sources confirmed by the builder; 24 `logSafe(` lines listed.
  - **12:** CodeQL fully re-measured.
  - **13, 14, 15, 16:** the 403 for viewers' Settings add; the `configure()` helper; the floor at 12:58; the new builder evidence files.
  - **New 18:** this amendment's own actions.
- **T-rulings:** T0 rewritten (mode 0 default at `39653db`, mode (a) predicts M0 + 30 / + 1); T1 notes the counts-conflict handling does not apply; **T6 rewritten as a test of the new gate**; T8's alert list extended. `RULED:` slots untouched.
- **Properties 3, 5, 9:** six routes; the 23 log sinks; the builder's census as a claim. Carried (b), (k), (p), (q) updated for the move, the lock holder and the model re-read.
- **Charter, §1, §2 severity:** Blocker for a viewer or out-of-window anonymous write through any of the six routes; Major for any of the 23 sinks forgeable; Major for a reader-caused store change only if an ungated settings writer exists; N29 re-scoped (client KQL RD-859, `/api/chat` raw lines RD-868).
- **Rows:** r0 (range and tree), r1 (three forward merges rebuilt), r2 (census expectation), r5 (extraction source), r7 (six routes; pre-gate tree as a second positive control), r7S (rewritten), r9 (M13-M16, 83/83), r10 (rewritten), r11 (rewritten), r12 (4910/303, 43 NEW names), r13 (gitleaks range), r14 (new-head claims), b1 (viewer 403 on add/remove), §3.
- **§8, verdict lines, limits:** landing checklist re-based (#70, #220, #221 STOP if open; the ten others NOTE; four same-rule controls); the verdict line gains the census, matrix (6/6), new-gate, log-sink, CodeQL, forward-merge and 43-NEW clauses; a separate "Also not tested" line was added beside the verbatim NOT TESTED line (which stays exactly one line, because the launcher greps for it).
- **PROVENANCE, FILL AT STAMP:** an Amendment 1 provenance block; FILL AT STAMP gains a new-head READY item and the launcher re-pin list.

Everything else is verbatim (T2-T5, T7, T9, T10, §2b, §3a H-rules, the clarification quotes, the model rule, r3, r4, r6, r8, r12b, r13 except the range, b2, b3).

## 3. Measurements, with sources

All NexusAI reads used `git --no-optional-locks -C <2_Project_Files>` read verbs only. All `gh` calls were GETs, with `GH_CONFIG_DIR='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`, repo `datasecau/Reporting_Dashboard_Au`. `.git/objects` = 257 files (`find -type f`) at 12:56:23 and again at 13:10:40.

1. **Heads** (`ls-remote origin`, 12:56:23 AEDT, rc 0, 1 attempt; again 13:10:40): main `39653db4b56adb6d4e526c90531cd4cdf23022e0`; `refs/heads/rd-774-risk-sql-templates-s101o` = `refs/pull/97/head` = `278afc25dda22ed8511d33e3e1cd12b0afde3487`. All objects present locally (`cat-file -t` = commit for the head, main, `29c5ee8`, `f1a2e76`, `e884516`, `2566713`, `4c9b0d3`, `7700caf`).
2. **Chain** (`log --format='%H %T | %P'` over `4c9b0d3..278afc2`):

   | commit | tree | parents |
   |---|---|---|
   | `278afc2` | `ee819f2126593465b352d91ae293fb3c55b9a75b` | `f1a2e76` |
   | `f1a2e76` | `5c80bbcf1abc678a08fc6b51bd067d51111c59ee` | `e884516` + `39653db` |
   | `e884516` | `3571969baa7bc2fdbec8364a26750fc1ebd4618f` | `2566713` |
   | `2566713` | `f5322b49a61c5269a0b4f9fbd194b72c27a68bfe` | `4c9b0d3` + `29c5ee8` |
   | main `39653db` | `704c442b78a36baea66fef2349a5acbdbff114b5` | `f15217c` + `29c5ee8` |

3. **Ancestry / mode:** `merge-base --is-ancestor 39653db 278afc2` rc 0; `merge-base` = `39653db`; `rev-list --left-right --count 39653db...278afc2` = `0 7`; `rev-list --count 39653db..278afc2` = 7, `888203c..278afc2` = 21, `7700caf..278afc2` = 19, `--first-parent 888203c..278afc2` = 7; `7700caf` and `888203c` are ancestors of `39653db`; `4c9b0d3` is not; the head is not on main (rc 1). `gh api pulls/97`: open, `draft: true`, `mergeable: true`, `mergeable_state: clean`, `commits 7`, `changed_files 8`, base = `39653db`. `gh api compare 39653db...278afc2`: `ahead`, `ahead_by 7`, `behind_by 0`. `7700caf..39653db` = 12 commits; `f9649dc`, `1da0bd4`, `f15217c`, `29c5ee8` are all on main.
4. **Gated paths vs main:** `diff --numstat 39653db 278afc2` = the same 8 paths: spy preload +23; rd774 test +564; `security-fixes` +77/−77; `server.js` +95/−434; `riskSqlTemplates.js` +300; `simpleDb.js` +17/−72; `validators.js` +3/−2; counts +3/−3. Blobs at the head: `server.js` `5fdf2912eceb186066e8c297c5234540eeaba25c` (main `8193f799be4ce843b2f404cd1e4c748ba9bf0d33`); rd774 test `0cfd42ee6fd1b8ae32c659f430cbcf9372e56321`; `simpleDb`, `validators`, `riskSqlTemplates`, spy and `security-fixes` blobs unchanged from 4c9b0d3; `package.json`, lock, `deploy-demo.yml`, `logSafe.js`, `jsonStorage.js`, `settings.js`, `testing.js`, `testing.html`, `authEnforcement.js` equal main's. `diff --stat e884516 278afc2 -- backend` and `f1a2e76 278afc2 -- backend` are empty. `278afc2` itself: one file, `__tests__/rd774-risk-sql-templates.test.js` +8/−5.
5. **Counts** (`show <c>:scripts/verify-expected-counts.json`): `39653db` 4880/302 (blob `2cc09485…`); `29c5ee8` 4733/295; `2566713` 4757/296; `e884516` 4763/296; `f1a2e76` = `278afc2` 4910/303, blob `57659c6cfc51d7ddffeb3e8ed31f1b7db4ef901c` at both. Static `test(`/`it(` lines in the rd774 file: 15 at 4c9b0d3, 21 at the head. Head − M0 = +30/+1.
6. **New gates, source:** `app.post('/api/settings/risk-definitions', requireRiskConditionAdmin, …)` :20753; validate-condition destructure :6947, `if (saveToDatabase && !(await requireAdminFor(req, res))) return;` :6950, save block :7037, add :7053 (the route is `app.post('/api/validate-condition', validateInput, async …)` :6945, so `validateInput` runs before the gate). `static/js/settings.js:1563` sends `saveToDatabase: false` only. The full anchor map is in the kit's §1.
7. **My census grep** (`grep -nE 'addRiskCondition|updateRiskCondition|deleteRiskCondition|riskConditionsFile|risk_conditions\.json|syncRiskConditionsToDatabase|ensureRiskCondition|INTO risk_conditions|UPDATE risk_conditions|DELETE FROM risk_conditions'` over `backend scripts` at the head): every server.js call site maps to a builder row (list in the kit's 7a); `simpleDb.js` :678/:730/:776 have no caller. Not covered by the builder's method and listed for r2: `scripts/fix_risk_conditions.js`, `jsonStorage` `getDataFiles()` users (:2263, :2308), `customerDataFiles.js`/`dataExport.js`. The three settings keys the GET replays are written only at :20767-:20769 (inside the gated route).
8. **Log sinks:** `git grep -n 'logSafe('` over `server.js` gives 24 call lines, listed in the kit. Raw sink left: :7116 `logger.info('User confirmed suggestion:', context.lastSuggestion)` (the builder's RD-868 :9011 not re-read).
9. **CodeQL** (`gh api`, 12:57-12:59): analyses on `refs/pull/97/head` at `278afc2`: js/ts `1985321634` (0, 103 rules), actions `1985312931` (0), python `1985312531` (0). Earlier: `f1a2e762` js/ts `1984710358` results 1; `4c9b0d36` js/ts `1978185235` 0; `360cd824` js/ts `1977664006` results 1. Open alerts on the PR ref: 0. #273 (`js/file-access-to-http`, warning/medium, `rd774…test.js:246`) instance `fixed@f1a2e762`; #272 instance `fixed@360cd824`. Open on main at `39653db`: #70 (`simpleDb.js:859`), #172 (`server.js:5409`), #220 (:21341), #221 (:21641). PR #58 control #256-#259 `fixed`. Check runs on `278afc2` all completed/success (ids in the kit).
10. **Main alerts vs head lines:** I took each of the 73 open main alerts on `backend/server.js`, read its source line at `39653db`, and tested whether that exact line text exists in the head's `server.js`. 12 do not: #172, #173, #175, #176, #178, #179, #180, #184, #185, #186, #220, #221. The other 61 do (including #171, #174, #177, #181, which the kit uses as same-rule controls). This is a line-text heuristic (READ-ONLY-INFERRED); closure is never claimed.
11. **Floor (12:58 AEDT):** `/Volumes` = Laptop-DEV, Macintosh HD, Recovery (T9 unmounted); tools unchanged (lock `3c33f5ae…`, c57 `1ae84a10…`, c133 `6f938bfc…`); `uptime` 4.29 / 5.25 / 7.28; jest lock HELD by `s101o-rd863-verify` (pid 14018, since 01:52:13Z), `queue-jest/` empty, `released/` 292; Node v26.8.1; gitleaks 8.30.1; Chrome 155.0.8059.84; `levels.opus.model_id` = `claude-opus-5-5`; `inbox_routing.conf` 234 lines, last is gate 28's; CLARIFICATIONS.md 435,914 bytes, 2026-10-18 22:35 (unchanged); gate 28's report line 3 = `STATUS: COMPLETE 2026-10-19`.
12. **Builder files hashed (METHOD only):** `mail-39-pr97-newhead.txt` 6352 bytes `714452848af0ac31e6806f0a8c5a74e5829aad4b2f2c348b678b61894f882d4c`; `rd836-census-ecb6b1e.txt` 4959 `013000db4256d53b64b46f371abef60579dc9da9184104a8dfa922bd68d7267b`; `rd836-census-4c9b0d3.txt` 2551 `9fa57a6070d9…`; `rd836-census-verify.log` 981783 `72caf9f272cf…`; `jc-rd836-census.txt` 2337 `1522b944d337…`; `jc-rd836-outside.txt` 2565 `5a8fa495c335…`; `mail-40-rd863-plan.txt` 2577 `7386a4c1810e…` (hashed, not read).
13. **Tuesday's briefs read:** ANSWER-26 (1808 bytes) and ANSWER-28 (1678 bytes), whole.

## 4. Launcher: not touched, must be re-pinned

`/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate29.sh` (792 lines, mtime 19 Oct 16:56, unchanged). `grep` shows these pin points (launcher line numbers):

- header comments :4, :8, :9, :27, :28, :30-:32;
- `READY_774_SHA` :71 and the READY greps :505-:507 (`ee6d589c…`, the head sha, `verify: PASS 4700/4700 across 293 suites`);
- `FLOOR_MAIN`/`FLOOR_TREE` :115 (`7700caf`/`ba9581ab…`), `H774`/`T774` :118, `M360`/`T360` :119 (still a chain member), `B63` :120, counts blobs `CB_FLOOR`/`CB_HEAD`/`CB_360` :123;
- the PIN-HEADS check :277 (base `7700caf`, 3 commits);
- the MAIN-STAMP regex :286-:289 (`landed since 7700caf`);
- head-moved check :309-:310;
- main-ancestry and mode-0 logic :321-:348 (`FLOOR_MAIN` as the mode-0 main and the merge-tree-onto-M0 check);
- chain guards :350-:357 (head chain and "3 commits over 7700caf"), now a seven-commit chain with three merge parents;
- the 8-path set over `7700caf` :391; counts 4676/292 → 4700/293 and blobs :401-:402; mode-a prediction `M0T+24` :405;
- blob pins :415 (server.js, rd774 test) and anchor counts `cntF` :421 (at 4c9b0d3);
- the SUMMARY/prompt text :748, :780.

Mode 0 is now "M0 = `39653db`, which is an ancestor of the head"; the guard that the PR #97 head is NOT on M0 stays. The launcher was not run, so there is no `--check` transcript from this amendment.

## 5. Left for Tuesday

**Slots remaining: 17 occurrences, 17 names, identical to the original** (`MAIN_SHA` ×2, `MAIN_TREE`, `MAIN_LANDED`, `REPORT_DATE` ×2, `RULING_T0` … `RULING_T10` ×11, `SELF_CHECK_STAMP`, `SELF_CHECK_NOTE`). The MAIN pin value is now probably `39653db4b56adb6d4e526c90531cd4cdf23022e0` (tree `704c442b…`, landed `none`) but it is yours to read at stamp. The route line `QA/NexusAI-gate29|tuesday-agent@agentmail.to|no` is still needed after gate 28's line (:234).

### Open questions (each with my recommended default)

1. **Launcher re-pin.** Who does it and when? *Default:* commission one more read-only drafter to re-pin the launcher against this kit (§4's list), run `--check` on a scratch copy as gate 28's amender did, and launch only after that. Do not launch on the old launcher.
2. **New-head READY copy.** The launcher's READY guard is built around the 4c9b0d3 delivered body. *Default:* save the delivered mail body as `briefs/2026-10-20_nexusai-gate29-READY-pr97-278afc2.txt`, `cmp` it against `mail-39-pr97-newhead.txt` (the seat's file may differ, as it did last time), and re-point the guard.
3. **If main moves again before stamp (RD-863 is S101O's next build): mode (a) or (b)?** The kit's T0 default stays (a) (the gate builds the merge in its store, +30/+1). *Default:* keep (a) for a landing that touches no risk-condition code; ask S101O for the counts-only forward merge (b) if the landing touches `backend/server.js` near the risk block, because (b) gives the gate a real branch head and a CodeQL run to read.
4. **T6 severity.** The kit now says a viewer or out-of-window anonymous write through any of the six routes is a Blocker (same class as the four), and a reader-caused store change (GET auto-sync) is a Major only if an ungated settings writer exists. *Default:* as written. Say if you want the e884516 routes held at Major.
5. **Row 7 (GET auto-sync) in or out of RD-836's verdict?** The builder files it OUT (RD-868). *Default:* the gate tests it as a claim and reports an N29 candidate, or a Major if an ungated writer of the three settings keys exists.
6. **Gate order in validate-condition.** `validateInput` runs before the admin gate, so an anonymous or viewer caller with a malformed body gets 400 before 403. I did not run it. *Default:* the gate records the order in r7; a Polish note at most.
7. **Landing checklist.** The kit expects ten more main alerts to close on land (heuristic) and treats an open one as a NOTE, not a STOP; #70, #220 and #221 stay STOPs. *Default:* as written; the "still open" control moves from #172 to #171/#174/#177/#181.
8. **The NOT TESTED line.** It stays the single verbatim line (the launcher requires exactly one `  Not tested by this gate: ` line), so it does not mention the ten extra alerts; a separate "Also not tested" line carries them. *Default:* leave it, or fold them into the verbatim line yourself and re-pin the launcher's check.
9. **REPORT_DATE.** *Default:* `2026-10-20`, or the launch date if later (the slot is yours).
10. **Lock wait.** S101O holds the jest lock for the RD-863 verify. *Default:* the gate queues FIFO behind it; no `qa-g28-*` ticket exists, so nothing else blocks the launcher's lock guard.

### UNMEASURED (named, not run)

- The conflict sets of the forward merges `2566713` and `f1a2e76`, and of any future M0 (I ran no `merge-tree`; the commission's verb list excluded it). The gate's r1 measures them.
- The delivered mail body (no AgentMail GET). Everything from `mail-39` is RELAYED: verify 4910/4910 across 303 suites, C-133 "accounted 13 then 32, missing 0", the red-first results on `2566713`, the five forged lines from four raw sinks, "No new alerts in code changed by this pull request" (check-run text). "backend/ identical from e884516 to 278afc2" I measured true.
- Any runtime behaviour of the two new gates (403 text, truthy `saveToDatabase` variants, anonymous behaviour per setup state, S4 "unproven"). All of it is source reading.
- Whether the 29 rd774 cells exist as 29 runnable tests (I counted static `test(` lines only: 15 → 21).
- The closure of #70, #172, #173, #175, #176, #178-#180, #184-#186, #220, #221 on main after the land.
- Any non-HTTP writer of `risk_conditions.json` (backup/rotation/restore at `jsonStorage` :2263/:2308, `scripts/fix_risk_conditions.js`) and any route that writes the three settings keys elsewhere than :20767-:20769 (my grep found none; the gate classifies).
- The remaining raw `/api/chat` log lines beyond :7116 (:9011 is relayed, not re-read).
- The 10,000-row cap and the other runtime properties of WRONG 11 (unchanged, not re-run).
- Whether the clarification quotes are still byte-exact in CLARIFICATIONS.md (size and mtime are unchanged; I did not re-grep the quotes).
- The `~/Library/Caches/ms-playwright` entry list (directory mtime only).
- The launcher as a whole (not run, not edited).

## 6. Hard limits kept

- **NexusAI repo:** read verbs only, each with `--no-optional-locks`: `ls-remote`, `cat-file -t`, `rev-parse`, `log`, `show`, `diff --numstat/--stat`, `merge-base [--is-ancestor]`, `rev-list`, `grep`, `for-each-ref --contains`. No `merge-tree` of any kind, no fetch, pull, checkout, worktree, commit or write. `.git/objects` 257 files before and after.
- **gh:** GETs only (pulls/97, compare, code-scanning analyses/alerts/instances, check-runs).
- **No** AgentMail, HTTP to an app host, jest, npm, server boot, browser or lock ticket. No credential file content opened (the `.gh-config` directory path was only passed as `GH_CONFIG_DIR`).
- **Datasec only.** I read only the NexusAI repo and session-tools files and the Tuesday briefs the commission and the kit name.
- **Writes:** only the three files in §1, plus scratch under the session scratchpad.
- Nothing launched, mailed or published.

## 2a. Edit list (key, original line, old → new; both truncated; sorted by original line)

| key | original line | old (first 70 chars) | new (first 100 chars) |
|---|---|---|---|
| E1a | 1 | `draft PR #97 @ 4c9b0d3. One gated tree` | `draft PR #97 @ 278afc2 (RE-PINNED 2026-10-20 from 4c9b0d3). One gated tree` |
| E1b | 1 | `RD-836 (admin-only risk-condition writers), draft PR` | `RD-836 (admin-only risk-condition writers: four routes at 4c9b0d3, six since e884516), draft PR` |
| E2 | 3 | `the drafter typed no clock into a stamp position.` | `the drafter typed no clock into a stamp position.  **RE-PINNED 2026-10-20 from 4c9b0d3 to 278afc25 (` |
| E3a | 4 | `the gated head ALREADY CONTAINS today's main ('7700caf' is its ancesto` | `the gated head ALREADY CONTAINS today's main (at the RE-PIN 2026-10-20 '39653db' is its ancestor, 7 ` |
| E3b | 4 | `and a sibling-writer row (T6), because the Settings page's own "add ri` | `and a sibling-writer row (T6): at 4c9b0d3 the Settings page's own "add risk rule" path (POST '/api/s` |
| E4a | 5 | `branch 'rd-774-risk-sql-templates-s101o' @ **'4c9b0d36993f1e78c8f23cd9` | `branch 'rd-774-risk-sql-templates-s101o' @ **'278afc25dda22ed8511d33e3e1cd12b0afde3487'** (tree **'e` |
| E4b | 5 | `Three own commits on the first-parent line over '888203c8c50e13938ca55` | `Seven own commits on the first-parent line over '888203c8c50e13938ca557e8aa0f1faf2101ff31' (21 in '8` |
| E5 | 6 | `the gate reads the DELIVERED copy and treats the seat file as METHOD o` | `the gate reads the DELIVERED copy and treats the seat file as METHOD only. **READY FOR THE NEW HEAD ` |
| E6 | 7 | `ANSWER-2{0,1,3,4}_*.md', read whole by the drafter.` | `ANSWER-2{0,1,3,4}_*.md', read whole by the drafter. **Added at the re-pin (read whole by the amender` |
| E7 | 9 | `At drafting origin main = '7700cafd33ca8a329e1e7905081d869e83c6ccb5' (` | `At the RE-PIN (2026-10-20 12:56:23 AEDT, 'git ls-remote origin', rc 0, first attempt) origin main = ` |
| E8 | 14 | `landed since 7700caf: @SLOT:MAIN_LANDED@` | `landed since 39653db: @SLOT:MAIN_LANDED@` |
| E9 | 20 | `\| RD774 \| nexusai \| rd-774-risk-sql-templates-s101o \| 4c9b0d36993f` | `\| RD774 \| nexusai \| rd-774-risk-sql-templates-s101o \| 278afc25dda22ed8511d33e3e1cd12b0afde3487 \` |
| E10 | 23 | `The 'base' column is main at drafting: 'rev-list --count 7700caf..4c9b` | `The 'base' column is main at the RE-PIN: 'rev-list --count 39653db..278afc2' = 7 ('63bef65', '360cd8` |
| E11a | 27 | `the builder's 23 + 14 cells are red-first at main and green at the hea` | `the builder's 29 + 14 cells (23 + 6 added at e884516) are red-first at main and green at the head` |
| E11b | 28 | `'backend/simpleDb.js:859' at '7700caf', MEASURED)` | `'backend/simpleDb.js:859' at '7700caf' and again at '39653db', MEASURED)` |
| E11c | 28 | `it introduces a new authorisation gate on four routes,` | `it introduces a new authorisation gate on SIX routes (four at 4c9b0d3; the Settings writer and the v` |
| E11d | 28 | `ADMIN-MATRIX (r7), RED-PROOF (r9) or BROWSER (b1-b3) rows did not run.` | `ADMIN-MATRIX (r7, r7S), LOG-SINK (r10), RED-PROOF (r9) or BROWSER (b1-b3) rows did not run.**` |
| E12 | 31 | `'refuseSqlText' at 'backend/server.js:20973'; PUT allow-list 'RISK_CON` | `'refuseSqlText' at 'backend/server.js:21027'; PUT allow-list 'RISK_CONDITION_PUT_FIELDS' at :21037; ` |
| E13 | 41 | `\| Settings → "add risk condition" as it ships ('settings.js:1878' POS` | `\| Settings → "add risk condition" as it ships ('settings.js:1878' POSTs '/api/settings/risk-definit` |
| E15 | 48 | `**Head check ('git ls-remote origin', 16:28:10 AEDT, first attempt, rc` | `**Head check at the RE-PIN ('git ls-remote origin', 2026-10-20 12:56:23 AEDT, first attempt, rc 0):*` |
| E16 | 49 | `1. **MAIN MAY MOVE BEFORE LAUNCH (MEASURED state, READ-ONLY-INFERRED c` | `1. **RE-PIN 2026-10-20 (MEASURED 12:56-12:58 AEDT): SUPERSEDED IN PART.** Gate 28 is COMPLETE (its r` |
| E17a | 50 | `2. **PR #97 against each gate-28 head conflicts in the counts file ONL` | `2. **SUPERSEDED 2026-10-20 (RE-PIN): every gate-28 head is now on main ('39653db') and PR #97's head` |
| E17b | 50 | `which is why r12 still runs the full verify on the rebuilt tree).` | `which is why r12 still runs the full verify on the rebuilt tree). **What happened (MEASURED from the` |
| E18 | 51 | `r1 re-proves it in the gate's store with the seat's counts blob '7436f` | `r1 re-proves it in the gate's store with the seat's counts blob '7436f51c1d0c8f3b39da13db1e84c41be99` |
| E19a | 52 | `4. **The gated file set (MEASURED, 'diff --numstat 7700caf 4c9b0d3'), ` | `4. **The gated file set (MEASURED, RE-PINNED: 'git diff --numstat 39653db 278afc2' 12:56 AEDT — the ` |
| E19b | 52 | `A '__tests__/rd774-risk-sql-templates.test.js' (+441)` | `A '__tests__/rd774-risk-sql-templates.test.js' (+564; was +441)` |
| E19c | 52 | `M 'backend/server.js' (+66/−410)` | `M 'backend/server.js' (+95/−434; was +66/−410)` |
| E19d | 52 | `'server.js' '05af86ceabfd0b012cdab6d75a1c4c3570212552' (main 'f2da6e00` | `'server.js' '5fdf2912eceb186066e8c297c5234540eeaba25c' (main '8193f799be4ce843b2f404cd1e4c748ba9bf0d` |
| E19e | 52 | `rd774 test '3a62151eab3e6261a27e8e84fa47bf23ffb99d95'` | `rd774 test '0cfd42ee6fd1b8ae32c659f430cbcf9372e56321' (was '3a62151e…')` |
| E19f | 52 | `'static/testing.html' '376bfee891372ea14692c9a1c4efaff2f30be350'.` | `'static/testing.html' '376bfee891372ea14692c9a1c4efaff2f30be350'. **RE-PIN (MEASURED 'rev-parse <c>:` |
| E20a | 53 | `5. **Counts (MEASURED, 'git show <c>:scripts/verify-expected-counts.js` | `5. **Counts, RE-PINNED (MEASURED 12:56 AEDT, 'git show <c>:scripts/verify-expected-counts.json'):** ` |
| E20b | 53 | `Predicted for a moved M0 (ARITHMETIC): M0 + 24 / + 1 — the launcher re` | `Predicted for a moved M0 (ARITHMETIC): **M0 + 30 / + 1** (it was + 24 / + 1 before e884516) — the la` |
| E21 | 54 | `and comment forms (r4, T3).**` | `and comment forms (r4, T3).** **RE-PIN: re-read at '278afc2' — 'PLANTED_SQL' is unchanged (MEASURED,` |
| E22a | 55 | `7. **THE SQL-PATH CENSUS IS WIDER THAN THE READY'S (MEASURED by 'git g` | `7. **THE SQL-PATH CENSUS IS WIDER THAN THE READY'S (MEASURED by 'git grep' at '4c9b0d3'; classificat` |
| E22b | 55 | `'generateSQLFromCondition' (:~6391) is dead (READY; ANSWER-24 item 2 f` | `'generateSQLFromCondition' (:~6391) is dead (READY; ANSWER-24 item 2 files the cleanup). 7a. **RE-PI` |
| E23 | 56 | `8. **RD-836's gate is bypassable for the risk-condition STORE by two u` | `8. **SUPERSEDED BY e884516 (RE-PIN 2026-10-20): both paths below are GATED at '278afc2' (MEASURED so` |
| E24a | 57 | `9. **The two HTTP-reachable sources of a CR/LF condition text the READ` | `9. **The HTTP-reachable sources of a CR/LF condition text the READY says do not exist (READ-ONLY-INF` |
| E24b | 57 | `the gate measures the realistic sources (r10).` | `the gate measures the realistic sources (r10). **RE-PIN: a viewer can no longer reach the settings w` |
| E26 | 60 | `12. **CodeQL state (MEASURED, 'gh api' GETs 16:32 AEDT, NexusAI's 'GH_` | `12. **CodeQL state, RE-PINNED (MEASURED, 'gh api' GETs 2026-10-20 12:57-12:59 AEDT, NexusAI's 'GH_CO` |
| E27a | 61 | `('settings.js:1843-:1890', ungated — WRONG 8)` | `('settings.js:1843-:1890', **gated since e884516** — WRONG 8)` |
| E27b | 61 | `and template rows where main errored.` | `and template rows where main errored. **RE-PIN: a viewer's Settings add / remove (POST risk-definiti` |
| E28 | 62 | `(BRIEF_TEMPLATE §7: name the one each plant lands in).` | `(BRIEF_TEMPLATE §7: name the one each plant lands in). **RE-PIN: the harness's setup moved into a 'c` |
| E29 | 63 | `NexusAI '.git/objects' = 90 files at 16:3x.` | `NexusAI '.git/objects' = 90 files at 16:3x. **RE-PIN reading (MEASURED 12:56-12:58 AEDT):** '/Volume` |
| E30 | 64 | `'session-tools/s101/' is LIVE (S101O writes there): hash at start and ` | `'session-tools/s101/' is LIVE (S101O writes there): hash at start and end. **RE-PIN additions (METHO` |
| E31 | 65 | `**No fetch, worktree, checkout, merge, commit, '--write-tree', jest, n` | `**No fetch, worktree, checkout, merge, commit, '--write-tree', jest, npm, server boot, browser, lock` |
| E32 | 69 | `RULED: @SLOT:RULING_T0@ (default: **mode 0** if the stamped M0 is '770` | `RULED: @SLOT:RULING_T0@ (default: **mode 0** if the stamped M0 is '39653db' (RE-PINNED 2026-10-20; w` |
| E33a | 70 | `base 'merge-base(M0, RD774)' = '7700caf'` | `base 'merge-base(M0, RD774)' = '39653db' (RE-PINNED; was '7700caf')` |
| E33b | 70 | `In mode 0: not run, named "not needed (no merge)".)` | `In mode 0: not run, named "not needed (no merge)".) **RE-PIN: in mode 0 the C-57/C-133 counts-confli` |
| E34 | 75 | `RULED: @SLOT:RULING_T6@ (default **(a)**: IN SCOPE as a test of RD-836` | `RULED: @SLOT:RULING_T6@ (default **(a)**: IN SCOPE as a test of RD-836's claim *"admin-only writers"` |
| E35 | 77 | `alerts #70, #172, #220, #221, #272 BY NUMBER and their instances on bo` | `alerts #70, #172, #173, #175, #176, #178, #179, #180, #184, #185, #186, #220, #221, #272, #273 BY NU` |
| E36a | 81 | `(3) **RD-836's ADMIN GATE** — viewer 403, admin 200, unauthenticated, ` | `(3) **RD-836's ADMIN GATE ON SIX ROUTES** — POST / PUT / DELETE '/api/risk-conditions', POST '/sync'` |
| E36b | 81 | `(5) **#272** red-proof re-run and **CodeQL** re-read at source with a ` | `(5) **THE 23 RISK-CONDITION LOG SINKS (#272 and e884516's logSafe)** — red-proof re-run, the gate's ` |
| E36c | 81 | `the builder's census (a241d25 F-10 grammar; three planting paths; thre` | `the builder's census (a241d25 F-10 grammar; three planting paths; three executors) checked (r14), an` |
| E37 | 86 | `(gate 28's RELEASEs are the likeliest movers)` | `(S101O's next landings are the likeliest movers; gate 28's RELEASEs and C-170 have already landed)` |
| E38 | 94 | `read 2026-10-19 16:31 AEDT).` | `read 2026-10-19 16:31 AEDT and again 2026-10-20 12:58 AEDT: still 'claude-opus-5-5').` |
| E39 | 98 | `(16:31 drafter reading: 6.73 / 9.55 / 9.78 — gate 28 is running).` | `(16:31 drafter reading: 6.73 / 9.55 / 9.78 — gate 28 was running; 2026-10-20 12:58 reading: 4.29 / 5` |
| E40 | 99 | `**THE GATE WAITS FOR GATE 28 TO RELEASE IT:** at drafting the lock is ` | `**GATE 28 HAS RELEASED IT (RE-PIN 2026-10-20):** at the original drafting the lock was held by 'qa-g` |
| E41 | 108 | `the #272 log line can be forged;` | `any of the 23 risk-condition log lines (the #272 line and e884516's sinks) can be forged from PUT, t` |
| E42 | 112 | `435,914 bytes, mtime 2026-10-18 22:35 at drafting)` | `435,914 bytes, mtime 2026-10-18 22:35 at drafting and unchanged at the RE-PIN, MEASURED 12:58 AEDT)` |
| E43 | 119 | `**The builder's census misses the writers of WRONG 7-8** (the risk-def` | `**The READY's census missed the writers of WRONG 7-8** (the risk-definitions sync, validate-conditio` |
| E44a | 123 | `## 1. Target — verified at drafting (16:27-16:33 AEDT)` | `## 1. Target — verified at drafting (16:27-16:33 AEDT, 2026-10-19); RE-PINNED 2026-10-20 12:56-13:00` |
| E44b | 124 | `→ '4c9b0d3' (tree '26f5dd7e…'). Lock tool sha256 above. In mode 0 **M0` | `→ '4c9b0d3' (tree '26f5dd7e…'; the previous gated head) → '2566713' (tree 'f5322b49…', parents '4c9b` |
| E45 | 125 | `- **Anchors at '4c9b0d3' ('backend/server.js', READ):** 'logSafe' impo` | `- **Anchors at '278afc2' ('backend/server.js', MEASURED by 'git grep -n' 12:56 AEDT; RE-PINNED — eve` |
| E46 | 126 | `(*"forgedLineStarts true, rawEscape true, logged false"*).` | `(*"forgedLineStarts true, rawEscape true, logged false"*). **RE-PIN (RELAYED, mail-39):** verify 491` |
| E77 | 126 | `- **Builder's results (RELAYED; yours decide):** verify 4700/4700, 293` | `- **Builder's results (RELAYED; yours decide), at the original head 4c9b0d3:** verify 4700/4700, 293` |
| E47a | 130 | `'g29/rd774' = '4c9b0d3…', 'g29/b63' = '63bef65…', 'g29/m360' = '360cd8` | `'g29/rd774' = '278afc25…', 'g29/prev4c9' = '4c9b0d36…' (the previous head), 'g29/b63' = '63bef65…', ` |
| E47b | 130 | `(90 at drafting); S101O is live` | `(90 at drafting; 257 by 'find -type f' at the 2026-10-20 re-pin); S101O is live` |
| E48 | 131 | `'7700caf' for the red-first arms if M0 moved` | `'2566713' ('g29/m256': main merged, the e884516 gates absent) as the PRE-GATE control tree for r7S a` |
| E50a | 136 | `a signed-in viewer or an anonymous caller (outside the C-01 window and` | `a signed-in viewer or an anonymous caller (outside the C-01 window and the RD-437 state) changing th` |
| E50b | 136 | `a log line forgeable through the #272 call on the gated tree is a **Ma` | `a log line forgeable through ANY of the 23 risk-condition log sinks on the gated tree (the #272 call` |
| E50c | 136 | `the KQL sibling log line and client KQL (RD-859) are **N29**, never fi` | `client KQL (RD-859) and the '/api/chat' raw log lines :7116 and :9011 (RD-868) are **N29**, never fi` |
| E50d | 136 | `holding PR #97 draft (ANSWER-24); C-170 waits on gate 28.` | `holding PR #97 draft (ANSWER-24); C-170 has landed (main '39653db').` |
| E81 | 143 | `'--name-status'/'--numstat' over '7700caf..<gated>'; every path in tha` | `'--name-status'/'--numstat' over '39653db..<gated>' (RE-PINNED; was '7700caf..'); every path in that` |
| E82 | 143 | `in mode 0 the gated tree = '26f5dd7e…' \|` | `in mode 0 the gated tree = 'ee819f21…' (RE-PINNED; was '26f5dd7e…') \|` |
| E51a | 144 | `mode 0: 'merge-base --is-ancestor <M0> 4c9b0d3' rc 0 and the tree pin;` | `mode 0: 'merge-base --is-ancestor <M0> 278afc2' rc 0 and the tree pin 'ee819f21…'; **EACH of the thr` |
| E51b | 144 | `**mode 0: the head IS the gated tree; '360cd82''s rebuild equals the s` | `**mode 0: the head IS the gated tree; each of the three forward merges' rebuilds equals the seat's t` |
| E52a | 145 | `the writer list = WRONG 7's (or the difference named)` | `the writer list = WRONG 7a's 11 rows (rows 1-6 gated, rows 7-11 OUTSIDE per RD-868) — or the differe` |
| E52b | 145 | `POSITIVE: the same census at '7700caf' finds 'executeRiskQuery(conditi` | `POSITIVE: the same census at M0 ('39653db'; the ×4 / ×1 were MEASURED at '7700caf', M0's 'server.js'` |
| E54 | 148 | `(extracted from '7700caf''s 'backend/server.js' into YOUR scratch modu` | `(extracted from M0's ('39653db''s) 'backend/server.js' into YOUR scratch module — the generator is t` |
| E55a | 150 | `ROUTES = POST '/api/risk-conditions' (no SQL), PUT '/:id' (allowed bod` | `ROUTES = the SIX gated writers: POST '/api/risk-conditions' (no SQL), PUT '/:id' (allowed body), DEL` |
| E55b | 150 | `**BRANCH: S3 viewer → 403 *"Admin access required"* on the 4 gated rou` | `**BRANCH: S3 viewer → 403 *"Admin access required"* on the 6 gated routes (validate-condition: 403 o` |
| E55c | 150 | `**POSITIVE:** BASE S3 viewer on POST/PUT/DELETE/sync → 200 and the sto` | `**POSITIVE:** BASE S3 viewer on POST/PUT/DELETE/sync/settings/validate-save → 200 and the store CHAN` |
| E56 | 151 | `**THE SIBLING WRITERS (T6), in the same hold:** in S3 as a signed-in V` | `**THE NEW GATES (T6), in the same hold:** in S3 as a signed-in VIEWER and as ANONYMOUS (and S1 / S2 ` |
| E57a | 153 | `**M12** a branch reordered in 'buildRiskSql' (cost before the statisti` | `**M12** a branch reordered in 'buildRiskSql' (cost before the statistical block); **M13** 'requireRi` |
| E57b | 153 | `restored → green 77/77 (the READY's count across the two files — re-co` | `restored → green 83/83 (the READY's 77 across the two files at 4c9b0d3 + the 6 cells of e884516 — AR` |
| E57c | 153 | `M12 and M10 are the likeliest gaps (say which cells, if any, see them)` | `M12 and M10 are the likeliest gaps (say which cells, if any, see them); the e884516 cell names FIVE ` |
| E58 | 154 | `\| r10 \| **#272 — THE LOG LINE (property 5), lock-free READ + r9's M9` | `\| r10 \| **THE 23 RISK-CONDITION LOG SINKS + #272 (property 5), lock-free READ + HTTP arms in H4 + ` |
| E59 | 155 | `\| r11 \| **THE CODEQL ROW (property 5), lock-free, 'gh' READ:** on 'r` | `\| r11 \| **THE CODEQL ROW (property 5), lock-free, 'gh' READ:** on 'refs/pull/97/head' = the pin '2` |
| E60a | 156 | `**'VERDICT: PASS' 4700/4700, 293 suites in mode 0 (the READY's; mode (` | `**'VERDICT: PASS' 4910/4910, 303 suites in mode 0 (the builder's, RELAYED mail-39; the gate's own ru` |
| E60b | 156 | `NEW = the 23 rd774 names + the 14 F-10 names; nothing else**` | `NEW = the 29 rd774 names + the 14 F-10 names (43); nothing else**` |
| E61 | 158 | `over '888203c..g29/rd774' in YOUR store (and '<M0>..g29/m774' in mode ` | `over '<M0>..g29/rd774' = '39653db..g29/rd774' (7 commits) in YOUR store (and once over the wider '88` |
| E62a | 159 | `*"verify: PASS 4700/4700 across 293 suites"* (r12);` | `*"verify: PASS 4910/4910 across 303 suites"* (r12; mail-39 — the READY's 4700/293 was the 4c9b0d3 cl` |
| E62b | 159 | `check every new response body string) \| stated \| — \| READY \|` | `check every new response body string); **the new-head mail's claims (RELAYED, each VERIFIED / FALSE ` |
| E63 | 160 | `VIEWER add: per WRONG 8 / T6 (drafter's reading: succeeds on both tree` | `VIEWER add / remove (Settings' POST risk-definitions): **403 on the branch** (gated since e884516; t` |
| E64a | 171 | `r11's '360cd82' results-1 read,` | `r11's '360cd82' and 'f1a2e76' results-1 reads,` |
| E64b | 171 | `r2's census at '7700caf',` | `r2's census at M0 and at '7700caf',` |
| E80 | 171 | `the jest lock's holder (gate 28 released?).` | `the jest lock's holder (gate 28 released it; S101O's 's101o-*' hold is FIFO ahead of you).` |
| E65 | 184 | `**Gate 28's 'inst/' is LIVE (gate 28 is running): never read as a sour` | `**Gate 28 is COMPLETE (RE-PIN 2026-10-20; its report line 3 reads 'STATUS: COMPLETE 2026-10-19', MEA` |
| E66a | 190 | `**Count '<NexusAI>/.git/objects' files (90 at drafting)` | `**Count '<NexusAI>/.git/objects' files (90 at drafting; 257 by 'find -type f' at the 2026-10-20 re-p` |
| E66b | 190 | `'mail-31-ready-rd774.txt' at start and end` | `'mail-31-ready-rd774.txt', 'mail-39-pr97-newhead.txt', 'rd836-census-*.txt', 'jc-rd836-*.txt' at sta` |
| E67a | 193 | `(iii) **after the land, main's push CodeQL: #70 ('js/sql-injection', '` | `(iii) **after the land, main's push CodeQL: #70 ('js/sql-injection', 'backend/simpleDb.js'), #220 an` |
| E67b | 193 | `(vi) gate 28's RELEASEs and C-170's TURN, if they land first, re-pin t` | `(vi) gate 28's RELEASEs and C-170 HAVE landed (main '39653db', the head carries it); any LATER landi` |
| E79 | 196 | `is shared with S101O, gate 28 (until it releases) and any landing hold` | `is shared with S101O and any landing hold (gate 28 has released it; S101O holds it as 's101o-rd863-v` |
| E78 | 198 | `every live peer 'QA/*' pane — gate 28's included while it runs)` | `every live peer 'QA/*' pane — gate 28 is COMPLETE at the re-pin, so none from it)` |
| E68 | 209 | `(gates 25-27 are COMPLETE and read-only to you; gate 28 is LIVE)` | `(gates 25-28 are COMPLETE and read-only to you)` |
| E69a | 220 | `@ <4c9b0d3 (mode 0, M0 7700caf)\|M774 <commit7> rebuilt onto M0 <m0-7>` | `@ <278afc2 (mode 0, M0 39653db)\|M774 <commit7> rebuilt onto M0 <m0-7> (mode a)\|<head7> (T0 b)> tre` |
| E69b | 220 | `CENSUS: writers <k> (gated <g>, ungated <u>: list), executors <e>,` | `CENSUS: writers <k> (gated <g>, ungated <u>: list), builder's 11 rows <confirmed\|differs: …>, rows ` |
| E69c | 220 | `ADMIN MATRIX: S3 viewer 403 on <4/4>, store unchanged <yes\|no>,` | `ADMIN MATRIX: S3 viewer 403 on <6/6> (validate-condition WITH a save; WITHOUT a save open <yes\|no>)` |
| E69d | 220 | `SIBLINGS (T6 <a\|b>): viewer writes via risk-definitions <yes\|no>, vi` | `NEW GATES (T6 <a\|b>): viewer / anonymous writes via risk-definitions <yes\|no>, via validate-condit` |
| E69e | 220 | `restored <77/77\|…>; #272: forged line on branch <no\|yes> from <k> so` | `restored <83/83\|…>; LOG SINKS: forged line on branch <no\|yes> from <k>/3 sources (PUT, settings, v` |
| E69f | 220 | `CODEQL: PR head analyses <3/3>, open 0 = 0 NEW, #272 fixed on PR ref, ` | `CODEQL: PR head analyses at 278afc2 <3/3>, open 0 = 0 NEW, #272 and #273 fixed on PR ref (not dismis` |
| E69g | 220 | `LOST <13 F-10 accounted\|…> NEW <37\|…>;` | `LOST <13 F-10 accounted\|…> NEW <43\|…>;` |
| E69h | 221 | `after the land, main push CodeQL #70, #220, #221 BY NUMBER = fixed and` | `after the land, main push CodeQL #70, #220, #221 BY NUMBER = fixed (STOP if open), #172/#173/#175/#1` |
| E69i | 221 | `gate-28 lands first => re-pin (mode a); N29 candidates: <sibling write` | `a later landing => re-pin (mode a, M0 + 30 / + 1); N29 candidates: <RD-868 outside rows: GET auto-sy` |
| E70 | 226 | `**L-B1** (CodeQL closure of #70, #220, #221:` | `**L-B1** (CodeQL closure of #70, #220, #221 and #172, #173, #175, #176, #178-#180, #184-#186:` |
| E70b | 232 | `  **The report's LAST two lines are the two verdict lines above, verba` | `    Also not tested (RE-PIN 2026-10-20; appended outside the verbatim line above, which the launcher` |
| E71 | 238 | `Jira (RD-774/RD-836 ticket text).  ## FILL AT STAMP` | `Jira (RD-774/RD-836 ticket text).  ## PROVENANCE — AMENDMENT 1 (RE-PIN), 2026-10-20 12:56 AEDT onwar` |
| E72a | 241 | `('none' if the sha is '7700caf', else what landed: 'git log 7700caf..<` | `('none' if the sha is '39653db', else what landed: 'git log 39653db..<sha>').` |
| E72b | 241 | `if '7700caf'/'888203c' are not in its ancestry, if its tree ≠ the stam` | `if '39653db'/'888203c' are not in its ancestry (once re-pinned; the launcher as it stands still chec` |
| E72c | 241 | `It recomputes the predicted counts from that main's own counts blob an` | `In mode 0 it needs no merge check; if main is past '39653db' it recomputes M0 + 30 / + 1 from that m` |
| E73 | 243 | `recommended '2026-10-19';` | `recommended '2026-10-20' (the original kit said 2026-10-19; the gate has not launched);` |
| E74 | 244 | `the launcher refuses on any other sha256). ` | `the launcher refuses on any other sha256). - ★ **the NEW-HEAD READY:** save the DELIVERED body of S1` |
| E75 | 245 | `Tuesday reviews it before stamping ('--check' first).` | `Tuesday reviews it before stamping ('--check' first). **★ RE-PIN REQUIRED (2026-10-20): the launcher` |
| E76 | 248 | `- **Gate 28 must have released the jest lock:** the launcher refuses w` | `- **Gate 28 HAS released the jest lock (RE-PIN 2026-10-20):** the launcher still refuses while the L` |
