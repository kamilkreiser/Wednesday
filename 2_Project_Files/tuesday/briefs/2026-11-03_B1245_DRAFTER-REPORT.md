STARTABLE: YES (after Tuesday fills the 14 stamp slots; no blocker found)

# B1245 drafter report (SEAT-H113, HPSMPOC-440). Drafted Tue 3 Nov 2026 23:13 to 23:26 AEDT (`date` at first and last reads).

## BLUF
- Kit: `2026-11-03_B1245_SEAT-H113_hpsmpoc-440-remediation-order-invisible-shape.md`. One file (`web/src/components/customer/remediation-store.test.ts`), 2 inserted lines (one word-joiner line per state in `CASES`, `"\u{2060}"` as an escape), 11 rows become 15. No product edit, no port, no PR.
- Template used: `2026-11-03_B1175_SEAT-H107_hpsmpoc-437-remediation-store.md` (the stamped H107 kit: same test file, test-only builder, same ticket family; H108/H110/H111/H112 are focus-ring, review-page or hygiene kits on other files). Shape copied, slots left as four underscores.
- Sweep's reason for BUILD (quoted, `SWEEP-1955:25`): "the gate's own fix shape is exact (its example: a word joiner) and adds no word, the same call as HPSMPOC-437 in 0408." **Does the ticket support it? Partly.** The ticket names the commit and the example, so building is within it. But it calls the commit "optional" and the example is "for example a word joiner", and it offers declining "since the order is one sequence of statements that three of the gate's plants already catch". The scope sentence says "Which is built is a scope call that is not made here", so BUILD is Tuesday's call, not the ticket's. "The gate's fix shape is exact" is a little strong: the shape is exemplary, not fixed. The kit carries the call as slot SCOPE-440 with a `decline` branch.
- Main moved since the sweep: now `69338b6476e2f9d0b5eaeb04742ca9181607121d` (squash of pull request 280, b1206, merged 09:19:03Z). The sweep read `f464376b`. The test file and product file are unchanged between them (blobs below).

## Re-measured facts (instrument; control)
1. Main sha: `gh api -X GET git/ref/heads/main` and `commits/main` agree (23:13). `git ls-remote` could not be used (Repository not found: no deploy key in the drafter's shell, correct by the fences).
2. Test file at that sha: 448 lines (`wc -l` over the raw `contents` read); blob `706f4877...` by `git hash-object` equals the `contents` sha. Product file 105 lines, blob `0c53005e...`, equal likewise. Control: `compare f464376b...69338b64` lists 36 files, 0 matching `remediation-store` (a count over the filename list; 36 = pull request 280).
3. `grep -n`/`awk NR==n` over the raw files: describe `:215`, `DATE_REFUSAL` `:217`, `CASES` `:218-223` (lines `:219-222`), tests `:225`, `:229`, `:233`, `:237`; product `:24` SHOWS_NOTHING, `:28` EVIDENCE_REFUSALS, `:44` trim, `:47` date, `:48-49` evidence. Rows 4 + 4 + 2 + 1 = 11 (matches the ticket); `CASES` is read by `:225` and `:229` only, so +2 lines gives +4 rows. Control: `Enter a real date.` found at `:190` and `:217`; `CASES` on 3 lines.
4. Shape behaviour by `node -e` over the regex copied from `:24`: U+200B, U+2060, U+200E, U+2800 stay length 1 after trim and read "shows nothing"; U+FEFF trims to length 0 (equals empty; matches the ticket's note); control `a` reads false.
5. CI: `ci.yml` 679 lines. `web-unit` `:450-451`, `npm ci` `:466`, `npm test` `:478`; `web/package.json:12` `vitest run`; `vitest.config.mts:10` jsdom, `:11` include. Build job: `npm ci` `:387`, audit-dev `:395`, lint `:396`, typecheck `:409`, build `:413`, check-shards `:426`. **SQL Server: not run there.** The SQL Server legs are `api-sqlserver-shard` `:165-166` and `api-sqlserver` `:353-354`, .NET `api/` tests only; this file runs in `web unit tests (vitest)`.
6. Partition: 295 branches read (`branches --paginate`), `compare 69338b64...<branch>` each; one read failed (b258, empty JSON), re-read once: 0 files on the path. Five branches name `remediation-store` (b955, b984, b1002, b1145, b1175), all landed or stale, 0 open PRs, 0 panes. Control: b1145 and b1175 listed. Open PRs: 0 (`pulls state=open` printed nothing; control `state=all` printed 280, 279, 278). b1097 @ `58ac1077` has 10 files (all under `web/e2e`, `web/src/app`, `web/src/components/partner`, `web/src/components/shell`); disjoint from the one path (filter output empty; control fires for b1145).
7. Ports: none needed (jsdom). `lsof -nP -iTCP:9600-9699 -sTCP:LISTEN` printed no row at 23:17 (the pipe made its exit status unreadable; the empty output is the instrument, no positive control run). Kits of 11-02/11-03 use 9630-9639, 9660-9663, 9670-9679, 9680-9689, 9690-9699 (a first-hit census over the 169 non-`.pre-` SEAT kits, not a full word-bounded scan per number).
8. Live panes (tmux, 23:17): tuesday, `Datasec/Security-Composer-G328`, `Datasec/NexusAI-N96`, fleet-monitor.
9. Ticket read by `.tools/b1007/jira.py HPSMPOC-440` (takes the key; the helper has no JQL entry point, so the `project = HPSMPOC AND ( key = ... )` form was not used): 0 comments, status Backlog, labels b1178-gate, b1188-2026-11-03. The scope sentence is quoted verbatim in the kit.
10. Gate record `B1178_STATUS.md`: verdict `:1` GO WITH FINDINGS, round 1 of 2 on class "remediation register tests and titles", NO GO 0 before; finding `:92`; plant table `:43-60` (qW `:51`, 0 red); proof `:64` (6 of 8 scratch rows fail under qW; BOM rows pass).
11. Landing: `CLARIFICATIONS.md:3617` of `datasecau/HPSM-POC-analysis` main `0e098d1f...` (5522 lines, raw by `gh api -X GET`): "The landing form is a head-pinned squash". Quoted in the kit.
12. status_watch: `status_watch.sh:56` case line includes `READY FOR QA:`, `STOPPED:`, `BLOCKED:`, `DONE:` (the kit's last-line forms).
13. Model: C2 `model-routing.md:92`, G2 `:109`, C8 `:98`; `claude-sonnet-5-5` at `models_latest.json:23`. Launch line has `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
14. Slot count of the kit: 14 lines carrying four underscores (13 stamp slots + the last line) by `grep -c -E '_{4}'`; the kit's REFUSE says 14.
15. Count guards: no `CalledTimes`/`CASES.length` guard on this subject (one unrelated `toHaveBeenCalledTimes(1)` at `:309`); no web count file in the 1746-path tree. The work adds table rows, not a named-function call.

## D-decisions (mine)
- D-1: word joiner only (the ticket's example; scope sentence says "one more"). Different regex range (2060-206F) from U+200B (200B-200F), so it adds a class.
- D-2: plants repeat the gate's: PJ (reversal limited to word joiner), PJV/PJS (per state), PW (the gate's qW), PA, PX, PU, P0, PC. PJ is the one the scope sentence demands ("a reversal limited to that shape turns a row red").
- D-3: kit forbids adding the byte order mark (equals empty) and any product edit; closed list stated as a property first.
- D-4: no port reserved (template reserved 9610-9619 "none needed"; this kit says none).
- D-5: pane REFUSE written as a test of what another live pane's kit writes (kit found by seat id, text outside "NOT yours" naming the path, control = the H107 kit).
- D-6: added a Step 3 check on commit author/committer host (the B1178 gate noted `localdomain` hosts on the earlier head; the project's configured email is a `users.noreply.github.com` address, read by `git config --get`, not printed here).

## Q-questions for Tuesday (each with a default)
- Q-1: SCOPE-440: word joiner only, or also the direction mark and braille blank (3 shapes, +12 rows instead of +4)? Default: word joiner only.
- Q-2: Gate round and tier: ROUND 1 OF 2 on class "remediation register tests and titles", G2 tier 2? Default: yes (NO GO 0 before).
- Q-3: Decline instead? Default: build (your named call; the ticket allows either).
- Q-4: Launch with the waiter (load1 below 7)? Default: yes; load was 5.31 at 23:20.

## UNMEASURED
Every test outcome and count at main (the 3892 in the B1178 record predates pull request 280); the expected 8 red for PA and the other plant red counts (stated as expectations; the seat prints them); hosted CI and CodeQL; `.tools/wt-b1113-fix/web/node_modules` size (`du -sk` timed out on a sweep of many trees and was stopped; the directory exists by `ls -d`); whether any decision card cites HPSMPOC-440 (no card read); the b1097 branch is disjoint by file list at 58ac1077 only; the first-hit port census was not per-number.

## Outside-the-fences disclosure
- Read-only: Jira GET by the project helper (key form), `gh api -X GET` under the HPSM-POC `GH_CONFIG_DIR` (main ref, commits, contents, trees, branches, compare x 297, pulls, the analysis repo's CLARIFICATIONS.md), reads of the HPSM-POC `1_Project_Definition/Briefs/` B1178 files, `ls`/`grep` of the `.tools` helpers, `tmux list-panes`, `lsof`, `uptime`, `df`, local `node -e` over scratchpad copies.
- One attempt, `git ls-remote` over SSH, failed (no key); no retry. No HTTP to hosted hosts.
- A `du -sk` loop over every `wt-*/web/node_modules` was started by mistake (slow), stopped by TaskStop; it only reads.
- One edit command (`sed -i`) was refused by a hook before running; I used the Edit tool instead. Nothing was deleted. Scratch copies live in the session scratchpad. No `cd`, no `decision_queue.sh`, no write to any project repo or HPSM-POC tree. Exactly two files written: the kit and this report.
