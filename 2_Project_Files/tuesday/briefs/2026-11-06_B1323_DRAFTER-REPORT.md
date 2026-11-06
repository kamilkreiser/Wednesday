STARTABLE: YES (after the Stamp; the builder's READY line is already in the STATUS file, last line begins `READY FOR QA: B1317 NEXUSAI RD-798 b1317/nexusai-rd798-log-sinks @ a5fdf1d4948a073f62b26fe7c75ffade8673c805`)

Drafted 12:35 to 12:45 AEDT 2026-11-06 (`date` in the actions). Files: kit `2026-11-06_B1323_SEAT-G351_nexusai-rd798-gate.md` (69 KB, ASCII, 8 four-underscore lines: 7 slots + last line), `2026-11-06_B1323_slots.json` (8 keys), this report.

## BLUF
Tier 1, row G1 (`model-routing.md:108`), Opus `claude-opus-5-5` (`models_latest.json:17`), `BRIEF_SEAT_LEVEL=opus` inside the quotes, pane `Datasec/NexusAI-G351`, round 1 of 2 on the new class "RD-798 log sinks" (census: 51 gate-verdict first lines, 0 class hits, control fires). The kit attacks the seven things asked: (1) the five wraps by an interpolation-classifier program plus the SARIF flows; (2) red-first re-run at the base blob, PL1 to PL5 (plus PL5b and PL5c) and eight own plants Y1 to Y8, with a proof the cells use the real server and no logger mock; (3) route status, HEADERS and body base against head; (4) the 2048 constant against a per-branch length matrix and a 5000-character table; (5) the table-name finding with four questions (who, reaches a 127.0.0.1 stand-in, gain beyond role, makes it worse); (6) the full verify under the lock, never `--update-counts`; (7) both C-190 thresholds on the 299 added lines. On GO: pr-title, pr-body, merge-subject, merge-body (MERGE commit, head-pinned, `CLARIFICATIONS.md:2067` quoted). On NO GO: residue.md + card-input.txt.

## Facts re-measured with instruments (controls named in the kit)
- Refs: branch `a5fdf1d4...` one row (control `heads/b129` length 1); main `aee39ec2...`; open PRs 0. `compare ffb67152...a5fdf1d4` ahead 1 behind 0, numstat 288/0, 8/5, 3/3. Main's two extra commits touch HISTORY.md only; blobs of server.js, logSafe.js, counts, deploy-demo.yml, build.yml at `aee39ec2` equal the base's.
- All five alerts still `open` at `aee39ec2` on lines 6191 6249 6308 6539 6550 (control: 220 `fixed`).
- SARIF (analysis 2108760635, 1.58 MB, 122 results) read by `python3 -I`: 182 and 183 one flow of 13 steps from `req.body` (base `:6838`) ending at `lowerCondition`; 174, 177, 181 four flows each (31/34/31/32 steps) ALL starting at `req.body` `server.js:14640` (`tableName`) via `getLogAnalyticsTable()` `:4092` to `baseKQL` `:5117`. The builder's finding is confirmed as to the flow. Head numbers are base + 3.
- The three KQL lines are the only two-argument `logSafe` calls in server.js (29 calls at the head). No earlier fixed alert is known to have closed through a two-argument call: the kit makes the gate look, and grades it a landing Condition, not a defect.
- Route facts: setup route `:14619`, gate `:14621`, `validTableName` `:14721` with no shape or length check; neighbours with the identifier regex at `:9741`, base `:15758-:15759`, `describeTable` (base blob `:229-:231`); `lawWriteRefusal` checks endpoint and tenant only. `adminGateRefuses` (`authEnforcement.js:634-648`) refuses nobody in setup mode. Jira: no ticket names the field; RD-830 is the same shape for `workspaceId`.
- Non-ASCII: the product diff's five added lines carry the existing emoji (set `{U+1F50D, U+1F916}` equals the removed lines' set), so a blanket "non-ASCII 0 in added lines" would be false; the kit states the exemption and asks for the proof.
- Commit message subject is 129 characters, ASCII, one trailer (Sonnet 5.5). The message's "No response body, status or header changes" is only measured for body and status 200 by the builder: headers are unmeasured, and C4 tests them.
- Model line 108/111, models_latest 17 printed by `awk NR==`. Landing lines 665, 2062, 2067, 2068, 2073, 2076, 2080 printed by `awk NR==`; deploy-demo.yml 26-33, 53, 91, 95 printed; `build.yml` `:83-:84` printed; repo variables 0, environments `dev`, newest three Deploy demo runs skipped.
- Ports: 9930-9939 `lsof` 0 (control all-listeners 15); word-boundary scan of the 33 non-`.pre-` SEAT kits of 5 and 6 Nov: one hit, the builder's own kit B1317 (control `991x` 7 hits). Panes: no `Datasec/NexusAI-*`; `G351`, `B1323` as whole words 0 files; `worktrees/*b1323*` and `session-tools/b1323` absent. Lock sha256 and fence sha256 as G344's; queue-jest empty. Free disk 134 GiB; load1 5.10 at 12:38.

## D-decisions
- D1 Tier 1 Opus, no Sonnet pre-gate (the surface is security; row G1 says O55 first).
- D2 The table-name finding is graded Note ("new ticket content") unless the head changes the stored value, the query sent to the stand-in, a status or a body, in which case Blocker. It goes in FOR TUESDAY on GO and on NO GO.
- D3 The gate never runs `--update-counts`; it checks the builder's single regeneration as a three-line diff and measured = committed.
- D4 Headers are included in the byte-equality check because the commit message claims them.
- D5 Time: target Step 0 + 110, hard stop Step 0 + 150 (verify up to 40 minutes plus three server boots plus the length matrix).
- D6 Trailer for the landing body: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (the previous NexusAI landings carry the gate seat's own model).
- D7 No person's name, card id, B-number or ticket key in the kit text the seat copies into landing files other than the project's own `RD-798:` convention (read from PR titles #169 and the merge `ef446f85`).

## Q-questions for Tuesday (each with a default)
- Q-1 Port block: the builder's 9930-9939 is free; reuse it for a probe of the gate's own, none typed. Default: reuse.
- Q-2 Run a Sonnet G2 pre-gate first? Default: no, Opus only.
- Q-3 Is a loopback Log Analytics stand-in permitted for C6 item 2 (127.0.0.1, no hosted host)? Default: yes; if `checkLawEndpoint` refuses loopback the seat reports UNMEASURED rather than work around it.
- Q-4 Should the table-name ticket content be written on a GO as well? Default: yes, in FOR TUESDAY, Tuesday files it.
- Q-5 Hard stop Step 0 + 150 and target + 110? Default: yes.
- Q-6 Moved main: HISTORY.md, CLARIFICATIONS.md, JIRA.md, BACKLOG.md and docs/** are fine; anything the change reads is a STOP. Default: as written.

## UNMEASURED
Hosted CodeQL on this branch (the only instrument for the two-argument form), hosted Build (Linux x64, node 24), whether Azure caps a table name at 63 characters (the builder's figure, RELAYED), the query lengths per template at their largest inputs (the kit makes the gate measure them), response headers base against head, and what a loopback Log Analytics stand-in receives (C6). The builder's trees, `session-tools/b1317/` and its logs were not read.

## Outside-the-fences disclosure
Wrote only the three files. Read: DRAFTER_RULES, the B1322 template and slots, the G344 NexusAI gate kit, the B1317 kit and slots, the builder STATUS named in the commission (read for the kit, as the commission and the G344 precedent allow), `model-routing.md`, `models_latest.json`, `CLARIFICATIONS.md` (local, by `awk NR==`), `EXPIRING-GRANTS.md` was NOT opened (the seat quotes it). `gh api -X GET` only, under the NexusAI `GH_CONFIG_DIR`: refs, compare, commits, contents (raw), code-scanning alerts and the SARIF of analysis 2108760635, workflows, variables, environments, pulls, branches (paged count only). Jira: one read-only `python3 -I` import of `b774lib.py` (`search`, `issue`, `adf_texts`; JQL with `project = RD AND ( ... )`; controls run). One local `lsof`, `tmux list-panes`, `df`, `uptime`, `shasum` of two tool files. Scratch files (raw fetches, SARIF, two Jira scripts) under the session scratchpad only. No decision-queue tool, no scoreboard, no ledger, no staged briefs, no WEDNESDAY or FRIDAY tree, no project git ref write, no hosted host.
