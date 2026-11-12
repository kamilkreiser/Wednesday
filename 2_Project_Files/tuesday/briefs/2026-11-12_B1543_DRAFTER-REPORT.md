STARTABLE: YES (after the stamp; every slot is `____`, nothing in the kit is pre-attested)

# B1543 SEAT-R223 drafter report (HPSM-POC records, Sonnet). Drafted 19:03 to 19:15 AEDT 2026-11-12 (`date`; hard stop 20:30).

## BLUF
- Kit: `tuesday/briefs/2026-11-12_B1543_SEAT-R223_hpsmpoc-records-deploys-1112.md` (269 lines, 16 slots, model Sonnet, level inside the quotes, pane `Datasec/HPSM-POC-R223`). Form copied from R222 (B1539) and R219 (B1523), both read; R222's STATUS and Hand-off items read for what was already written.
- Content: THREE C-entries (expected C-367 landings of 314/315/316; C-368 the UAT deploy of 576231b7; C-369 the follow-ups) in one records PR, and SIX Jira writes: four creates (W1 minimatch override with removal condition, W2 coach row re-worded, W3 deploy-script failed-upload ticket, W4 presenter-only lines) and two comments (W5 on HPSMPOC-477 map drift, W6 on HPSMPOC-467 real-name reader).
- **Item 5 shrank to two items:** R210 (B1493) already wrote the user guide v0.4 entry (C-339, records main line 6021), the D60 deletion entry (C-340, line 6033) and both FOUND tickets (HPSMPOC-468, now Done; HPSMPOC-469, Backlog). Only the T7 re-word and the H6 drift note were still owed.
- Scan of all six bodies, six summaries and three entries by my own program: 0 problems; controls fire (planted C-9999, B170, Tuesday, Kam, `_by_Kam_`, C-347, prose HP, U+202E, U+00A0, e-mail-shaped `@`, 24-hex run). Summary lengths 218/197/214/213/163/144 (all <= 255). Body lengths 2605/3376/2321/1601/1648/946.

## What I read
DRAFTER_RULES whole; R222 kit whole (472 lines) and its STATUS (BLUF, T7 rows, Hand-off items 1-6, Deviations); R219 kit by its structure (R222 is its descendant); B1493 STATUS head/tail; B1540 STATUS lines 1-35 and 196-247 (second attempt, FOR TUESDAY final), kit stamp slots S1-S16; ANSWER-1 whole; VERDICT heads of B1535 (to line 22), B1538 (to 22), B1541 (to 24); minimatch `ticket-text.txt` whole; NEXT-PICKUP (DELTA 1147/1148 HPSM lines); records main `CLARIFICATIONS.md` (raw, 6286 lines, 2064063 bytes) by grep and the C-365 entry whole.

## Facts re-measured (instrument; control)
| Fact | Instrument | Control |
|---|---|---|
| Jira highest key HPSMPOC-477, nothing above; 471-477 are R222's (T1-T4, T6, T8, T9) | own GET-only reader `d_hpsmrec/jget.py` (credentials by name in-process), `project = HPSMPOC AND (key >= HPSMPOC-465)` = 13 keys | `qqzzxx9` 0; `REC-LAND4-461-11NOV` = HPSMPOC-461 |
| Records main 5d2fade9, C-366 newest (line 6278), 0 open analysis PRs | `gh api -X GET` commits/main, pulls?state=open, raw contents | `^### C-263 ` 1; `^### C-366 ` 1; `pull request 313` 2 |
| #314/#315/#316 not in records | `grep -c -i -F` c6b5c8cf, 60d442e2, 576231b7 = 0, 0, 0 | `pull request 313` 2 |
| C-339 (guide v0.4) line 6021, C-340 (backup deletion) line 6033 present; 468 Done, 469 Backlog | grep -n; jql | headings printed |
| #314 squash c6b5c8cf merged 03:54:03Z, head 9308afa0, 24 files +199/-151; #315 squash 60d442e2 merged 04:39:57Z, head 61ce4c3d, 2 files +17/-4; #316 squash 576231b7 merged 06:17:24Z, head b34737f4, 9 files +100/-86; main = 576231b7 | `gh api -X GET pulls/<n>`, commits/main | `pulls/999999` 404 |
| Dependabot alert 9: minimatch, medium, state fixed, fixed_at 2026-11-12T05:30:17Z | `gh api -X GET dependabot/alerts/9` | alert 99999 returns "No alert found" |
| Override present at 576231b7: web/package.json line 52 `"overrides"` -> typescript-estree -> minimatch 11.0.1; lock line 2845 version 11.0.1; nonrecursive-glob-match 3 lines | raw contents + grep -n | `"engines"` 1 |
| Claim "21 stable releases 8.60.0 to 8.72.2 declare ^10.2.2" | PR 315 body grep: 8.72.2 / alpha present (1 line) | **RELAYED only: npm registry not read (no HTTP outside api.github.com and Jira); the ticket says so** |
| Coach: ConversationCoach.tsx:126 renders `{t.opener}`, :174 lead; content.ts SAMPLE_TRACKS from :134 holds 8 `opener:` lines; the document's opener (MA:297) and talk track (MA:94) phrases appear 0 times in content.ts | raw contents; awk NR>134; grep -c -i of 3 phrases = 0 | `opener:` = 9 (8 + type line) |
| MA:94 and MA:297 are source lines 94 and 297 (also 93 and 296 headings) of the 302-line source (sha256 prefix 51e65b119447d396); map rows C-coach (line 145), H6 (line 83), Q8 (line 209) | awk NR | quoted CODE lines are substrings of map/source (program, True x5) |
| H6 drift: parts.tsx:14-16 `IllustrativeTag` renders `Sample {what}`, `title={SHOWCASE.notice}`; notice (showcase json line 5) = "Sample data for demonstration only..."; "booked or recognised" 0 in that file | raw contents + grep | `"notice"` 1 |
| Deploy script: `set -euo pipefail` line 25; uploads lines 68 (web), 69 (api); header says web then api | raw contents grep -n | header printed |
| Walkthrough steps.ts holds 15 `say:` lines | grep -c -E | 17 lines contain "say" (superset) |
| Open tickets: minimatch 0, typescript-estree 0, "account manager opener" 0, GatewayTimeout 0, deployments/latest 0, "walkthrough panel" 0; deploy-from-ci open: 57, 58, 303; HPSMPOC-467 (open) already decides alias on all seven and lists the Home pipeline table (comment 41018) | jql phrase form | controls above |
| Model rows: routing lines 97 (C7) and 110 (G3) printed; model id claude-sonnet-5-5 at models_latest.json line 23 | awk NR | printed |
| Ports: none; panes: %0 tuesday, %1 fleet-monitor, %28, %29; B1543 / SEAT-R223 files: 0 before mine | tmux list-panes; ls | -- |

## Items: source and verdict
1. **C-entry landings #314/#315/#316** (entry 1): sources GitHub API reads, three VERDICT first lines, PR bodies. VERIFIED (numbers above). The kit fills rows by program and requires each parent to equal the previous squash (chain c717ba1a, c6b5c8cf, 60d442e2, 576231b7: DERIVED from VERDICT B1538 and B1540 S1; the seat re-measures).
2. **C-entry deploy** (entry 2): source B1540 STATUS (final sections), ANSWER-1, the deploy kit's S2 authority slot (10:51, 11:21:32, 14:38:06, 14:54:12 and the terminal "the steps are good.  go ahead", which I read in the stamped B1540 kit). VERIFIED as RELAYED; every deploy figure is to be checked by the seat as a substring of the deploy record. The terminal word is attributed to "the product owner" in the kit text (no name).
3. **Minimatch ticket** (W1): VERIFIED at source except the npm release claims (RELAYED, marked). The ticket text was rewritten from `ticket-text.txt`: its BLUF said "pushed, no pull request" (stale), now landed; its "premise correction" (braces exception) was dropped to avoid an unverified absence claim. Label `dependabot` follows HPSMPOC-218.
4. **B1540 item 6**: (a) -> W3 create, VERIFIED (script lines, Kudu 504 and times RELAYED from the deploy record); (e) -> W4 create, RELAYED (the eight row ids are the deploy seat's own and are not named; the ticket says "eight lines" and cites the 15 `say:` lines I counted); (d) -> **comment W6 on open HPSMPOC-467** instead of a ticket, because 467 already decides the same thing (search before create); **(b) and (c) DROPPED** (see Q1).
5. **Owed from earlier:** T7 re-worded -> W2 (VERIFIED, wording corrected to "not among the sample talk tracks", the map row's false "no coach slot" is quoted and corrected inside the ticket); H6 drift -> W5 comment on 477 (VERIFIED); user guide v0.4 C-entry, its two FOUND tickets and the D60 deletion C-entry -> **DROPPED, already written** (C-339, C-340, HPSMPOC-468, -469). The "13 records" in NEXT-PICKUP's OWED line is not defined anywhere I read; I took it to mean the landings/deploy/held-row records (Q4).

## D-decisions (mine)
- D1: three entries (landings, deploy, follow-ups) rather than one, so each is independently citable; E-3 is written last so it carries real Jira outcomes.
- D2: used R222's stricter naming rules, hence no gate names, brief numbers, C-numbers or "seat" in any added line; added two scanner exemptions the texts need (npm scope `@`, 40-hex commit shas in entries) with controls, stated in the kit.
- D3: W5/W6 are comments with a fixed named target (not search-named), with a "target still open" re-check.

## Q for Tuesday (defaults)
- Q1: file deploy-record points (b) and (c) (fleet deploy-template fixes)? Default NO: they concern the coordinator's own templates, and `kit`/`seat` are banned words on the board. Say so in your own brain notes instead.
- Q2: W4 (presenter-only lines) is a "gather" question to the product owner. Default WRITE (cheap, decides nothing); HOLD it if you prefer not to open a new question on his board tonight.
- Q3: labels: new `rec-2026-11-12` (precedent `rec-2026-11-11`), `dependabot` (HPSMPOC-218), `hosted-demo`. Default as drafted.
- Q4: if "the 13 records" meant something else (e.g. the 13 C rows), say so; they are already C-366 / HPSMPOC-471..477.
- Q5: REC-MERGE FF (seat lands its own records branch by the B1523 route) as for R222: default FF.

## UNMEASURED
npm registry facts in W1 (release range, canary list); deploy times and 504 text in W3 (read from the deploy record only); W4's "eight lines on no page" and W6's 5/5 reading (the review site must not be read); whether any HP reviewer was in session during the deploy.

## Outside-the-fences disclosure
Read-only only: GET Jira (own helper, token never printed), `gh api -X GET` under the HPSM `GH_CONFIG_DIR`, raw file reads, `tmux list-panes`. Scratch files (clones of raw files, scripts) only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s273/d_hpsmrec/`. One refused heredoc (a hook blocked an unquoted `$P` and `====`), no side effect. No decision card, no `decision_queue.sh`, no `fleet/briefs_staged/`, no scoreboard, no ledger read. Nothing written in any repo or Jira.
