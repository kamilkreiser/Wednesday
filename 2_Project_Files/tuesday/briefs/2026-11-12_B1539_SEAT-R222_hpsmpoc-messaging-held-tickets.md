From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail; a launch message that names a mailbox is overridden). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file or stated by the stamp; **UNMEASURED** = nobody has. In this kit, **MEASURED-BY-DRAFTER** = printed by the drafter's instrument at drafting (2026-11-12, 11:3x to 11:5x by `date`; the end clock is in the drafter report); you re-measure every one before you use it. Files naming another B-number are READABLE claims only.

**LAUNCH ONLY WHILE no pane runs a kit that writes Jira HPSMPOC or the analysis `CLARIFICATIONS.md`.** At drafting (`tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'`, 11:38): `%0 tuesday`, `%1 fleet-monitor`, `%168 Datasec/HPSM-POC-H161`, `%162 Datasec/HPSM-H160`, `%165 Datasec/MPS-M131`, `%159 Datasec/MPS-M130`, `%153 Datasec/MPS-M129`, `%147 Datasec/NexusAI-N125` and unnamed keep-alive panes. **Two HPSM-POC builder panes are live and neither writes Jira or the analysis file** (MEASURED-BY-DRAFTER, `grep` of their kits: the minimatch kit says "no Jira write by you"; the messaging-alignment kit says "Jira: you read and write none" and "Jira writes: none"; each names `CLARIFICATIONS` once, read-only context). They write the CODE repository only. Tuesday re-reads this at the stamp (REFUSE 7). This seat runs alone on HPSMPOC and on the analysis repository.

# BRIEF B1539 | SEAT-R222 (records): HPSM-POC. **Records and Jira only, no code: file the HELD rows of the messaging map as tickets "for later" on the HPSM-POC board (at most NINE writes: nine tickets, each created OR, where an open ticket already decides the same thing, posted as one comment on it), and record the product owner's 2026-11-12 11:21 ruling in ONE entry through a records pull request.** MODEL SONNET (records form of B1523). NO CODE BYTE, NO CODE-REPOSITORY WRITE, NOTHING BUILT, NOTHING DEPLOYED, NO AZ, NO REQUEST TO ANY APP HOST, NO MESSAGE TO ANY HUMAN. **Nothing is moved, closed, built or re-labelled. No HP-facing text is posted anywhere but Jira** (and no text at all goes to the customer: the tickets are on the project's own board). **No dotnet command is needed or run by this seat.**

**BLUF.** The product owner's words on the live board, 2026-11-12 11:21:32 AEDT (RELAYED by the commissioning message, which quotes them; the drafter did not read the board chat; the stamp slot RULING-1121 carries the sentence Tuesday read): *"messaging mapping looks good. deploy based on this and ticket anything left for later"*. The map (`2026-11-12_hpsm-messaging-map.md`, 267 lines) puts **59 rows to change or hold: A 22, B 13, C 13, D 11** (the drafter re-counted them by `awk -F'|'` over the map's table rows: A 22, B 13, C 13, D 11, total 59; the printed total of the map's own BLUF agrees). The text pass (44 rows: 22 A, 13 B, 9 D) is a separate builder's work and is NOT this seat's. **This seat tickets what the pass leaves: 15 HOLD rows of the map (the 13 C rows plus the 2 D rows K2 and K3; the 11 D rows less the 9 built in qualified form leave exactly K2 and K3) plus H6b, the held half of row H6** = **16 held items in NINE tickets** (grouped by workload, see THE TICKETS). **Difference from the coordinator's list: none in the 15; the list's `H6b` is NOT a row of the map** (the map has no row of that id: `grep -c 'H6b'` over the map prints 0, control `grep -c 'H6'` prints 5): it is the half of row H6 (the Illustrative tag's title attribute in `web/src/components/partner/parts.tsx`) that the builder's kit holds out of the text pass as `NEEDS-SHARED` (RELAYED from that kit, line 12 and line 169). Its ticket (T9) is conditional (Step 2).

**Board and records facts at drafting (MEASURED-BY-DRAFTER, 11:35 to 11:41).** Jira: `search/jql` `project = HPSMPOC AND (key >= HPSMPOC-1)` returns **470** issues, highest key **HPSMPOC-470** (Done 347, Backlog 120, In Progress 3; the earlier drafter's 11:25 export also read 470, so the board has not moved); no `messaging-2026-11-12` label on any ticket (0), `next-phase` 3, `gather` 7, `awaiting-hp` 9, `follow-up` 6, `needs-kam` 16. Phrase searches: the nonsense token `qqzzxx9` reads 0 and the marker `REC-LAND4-461-11NOV` reads exactly HPSMPOC-461 (the controls); `REC-HELD-` markers: none to find yet (0). Code main `c717ba1a945191ffa31f13320c19967a6cf7f15a` (`gh api -X GET .../commits/main`; unchanged since the map's reading). Records main **`75ae17d5b0bf438f5855527626c0a22a51da07c7`** (R219's merge of #198), `CLARIFICATIONS.md` 6276 lines, 2060302 bytes, 365 headings, newest `### C-365` at line 6263, `### C-263 ` once at line 5114 (the control), open analysis pull requests 0. **Your entry is expected C-366 (one)** (highest + 1; derive it again by program). Seat id R222 and number B1539: 0 files among the non-`.pre-` briefs use them (`ls | grep -c B1539` prints 0 before this kit). Disk free 1271 GiB. Ports: **none** (this seat starts no listener). Your STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-12_B1539_STATUS.md`.

**What this is NOT.** Not the text pass (the builder), not the phase decision document's items (they are not ticketed here; a ticket only NAMES the D-item beside its held row), not any answer to a held question: every ticket says "keep held" and the map's default stands. The product owner's 11:21 words are an instruction to ticket, not a ruling on any held question.

**Launch (Tuesday), ONE waiter, after the Stamp, level inside the quotes:** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/HPSM-POC-R222 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1539_SEAT-R222_hpsmpoc-messaging-held-tickets.md'"`. Model row: `fleet/specs/model-routing.md` line 97, row C7 (client-board ticket text: Sonnet drafts first and posts only a body the coordinator approved byte for byte: the nine texts below, the dry run and the slots are that approval) and line 110, row G3 (ticket hygiene, no gate); model id `claude-sonnet-5-5` (`0_Brain/dashboard/data/models_latest.json` line 23). `brief_seat.sh` defaults to Opus (line 24: `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`); the level is written inside the quotes. Arm `status_watch.sh` on your STATUS.

**Context band and handover.** At about 70% context start no new step; at about 75% stop at a safe boundary (files whole, no write half-done, no process left, no lock held) and write `1_Project_Definition/Briefs/2026-11-12_B1539_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps, including every created key, comment id and the entry state already written), last line `HANDOVER B1539: next <step> <ticket> | done <steps>`, and make that the STATUS last line too. **A successor never re-files:** it runs the marker search of all nine markers first and skips a ticket whose marker already reads (it never creates a second ticket; it searches the marker and the summary first).

## READ WHOLE FIRST (read-only; they are the form and the truth, this kit is a relay)
1. **The form:** the last HPSM records pass, `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1523_SEAT-R219_hpsmpoc-records-313.md` (145 lines, stamped) with its STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-11_B1523_STATUS.md` (last line `RECORDS COMMITTED: records/b1523 @ 81697a19... | PR #198 merged as 75ae17d5... | C-365 to C-365 | Jira: commented: HPSMPOC-470, HPSMPOC-271; ...`) and the earlier `2026-11-11_B1518_SEAT-R217_hpsmpoc-records-309-312.md` (the one that created a ticket: its CREATE form). **Read its Deviations first** (the phrase form of every marker search `text ~ "\"REC-...\""`, never the unquoted form; the scanner's credential-word refinement; the poster's counted-write cap; **a Jira create is refused above 255 characters of summary**; `gh api -X GET --allow-escape-sequences` is needed to read a job log). Its closed list, helpers, text rules, dry run, read-back, snapshot diff and landing **bind you wherever this kit is silent**, with `b1523` read as `b1539`.
2. **The helpers it left, as a reference to copy and adapt, never import and never edit:** `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1523/` (`jira1523.py`, `closing1523.py`, `entries1523.py`, `diff1523.py`, `build1523.py`) and `.tools/b1518/` (`jira1518.py`, `scan1518.py`, `post1518.py`, `snap1518.py`; **its CREATE path is the only one that created a ticket**). Copy `scan1518.py` into `.tools/b1539/` (`cp -n`) and use THE COPY with these changes only: the marker regexes read `\[REC-HELD-T[1-9]-12NOV\]`, your own number set is `{<CE>}`, the `HP`-as-a-word ban is applied as THE TEXT RULES below say (quotes and product names exempt), and the name list is its `NAMES` plus `Wednesday`, `Friday`, `Marco`.
3. **The map and the source** (read WHOLE; the ticket texts below were generated from them by program and every quoted fragment is a substring): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_hpsm-messaging-map.md` (267 lines), `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1112/messaging_alignment.txt` (302 lines), and the phase decision document `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_v21_gap_analysis/DECISION-DOCUMENT.md` (1872 lines; read only the D-items a ticket names). **In every Jira text and the entry these three are named only by their titles** ("the messaging map", "the source document", "the phase decision document"): no path of the coordinator's tree, no file name, no brief number.
4. The project's `CLAUDE.md` and `JIRA.md` (JIRA.md holds the board key `HPSMPOC`, the issue types Epic, Story, Task, Bug, Sub-task, board id 606 and the BLUF format; **neither holds a label rule nor a ticket-creation rule**: `grep -n -i` for `label` and `one ticket` over both prints nothing relevant; the labels and the grouping below come from the board's own practice, MEASURED-BY-DRAFTER below, and are a question for Tuesday, see the report), and records main's `CLARIFICATIONS.md`: `### C-263` (the project's own Done rule; anchor at line start) and `### C-365`.
5. The builder's STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-12_B1535_STATUS.md` (READABLE claims only; at drafting it was 11 lines, `PROGRESS B1535: ... HOLD`, still working): read its `## HELD` section when it exists (Step 2).

## BINDING HOLD
You deploy nothing and touch no hosted host, no database, no Azure, no review site (not even a GET). The only hosted reads allowed are `gh api -X GET` against `api.github.com` and GETs to the project's Jira. You write nothing in the CODE repository (`datasecau/HPSM-POC`: `gh api -X GET` only, under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config'`). You write: (1) Jira project HPSMPOC through the CLOSED LIST below; (2) `1_Project_Definition/CLARIFICATIONS.md` of the ANALYSIS repository (`datasecau/HPSM-POC-analysis`) through one records branch `records/b1539` in your own clone `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1539/analysis`; (3) files under `.tools/b1539/` and your STATUS. **`CLARIFICATIONS.md` is over 2 MB: read it only with the raw media type (`gh api -X GET -H 'Accept: application/vnd.github.raw' 'repos/datasecau/HPSM-POC-analysis/contents/1_Project_Definition/CLARIFICATIONS.md?ref=<sha>'`) or from your clone; an empty read is a STOP, never a zero.** No `az`, docker, ssh, sqlcmd, no request to any URL but `api.github.com` and the project's Jira. No message to any human. Never delete (quarantine to `.tools/b1539/_quarantine/`); no force-push, amend, reset or rebase; **never type `cd`**. **This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only.** **Read no decision card.** **Git identity is never overridden:** the repo's own configured identity only; never `git -c user.name/user.email`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*`. Your clone's identity must equal the project analysis checkout's own (`git -C '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' config user.email`): print both before the commit; if the clone reads none, copy the checkout's `user.name` and `user.email` into the clone's repo-local config exactly and print before and after; any other value is a STOP. READY prints `git log --format='%h %ae | %ce'` for the new commit, each equal to that email.

## THE JIRA CLOSED LIST (property first, then at least these; any other shape: prove it meets the property or STOP)
**Property:** HPSMPOC only; **exactly ONE write per ticket T1 to T9, either one create or one comment, never both** (a create of a Task for a ticket whose search found no deciding open ticket; one comment on ONE existing open ticket when the search found one); **at most 9 writes in all; the 10th is refused**; no transition, no label edit, field edit, link, assignee, attachment, priority, parent or component on any existing key; no PUT; no DELETE; no edit of any existing description, summary or comment; no write to a Done ticket; nothing on any ticket not named by a search hit under the rule below; nothing about the build of the text pass. **A create** is `POST /rest/api/3/issue` with `fields` = `project` `HPSMPOC`, `issuetype` `Task`, `summary` (the frozen summary), `description` (the ADF built from the frozen body), `labels` (exactly the ticket's labels), and **no other field** (no priority, no assignee, no parent, no link). **A comment** is `POST /rest/api/3/issue/<KEY>/comment` (ADF; the frozen summary as the first paragraph, then the frozen body). **Helpers written fresh** under `.tools/b1539/` (`jira1539.py` with the fence `allowed(method, path, body)`, `scan1539.py`, `post1539.py`, `snap1539.py`, `diff1539.py`, `entries1539.py`, each with `--selftest`) from the forms in READ WHOLE item 2; credentials `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` read BY NAME in-process from `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.env`, never printed, never on argv; every request logged to `.tools/b1539/logs/jira-requests.log` BEFORE it is sent (method, path, body sha256; never the token). The poster refuses a ticket outside T1 to T9, a second write for a ticket, a create or comment whose marker already reads, any text that fails the scan or differs from its frozen sha256, a summary above 255 characters, a label outside the ticket's list, any POST to a transitions path, any write while its slot is HOLD, a PUT or DELETE, a comment on a Done key or on a key the search rule did not name, any call while `.tools/b1539/HOLD` exists, the 10th write. **Every JQL is `project = HPSMPOC AND ( ... )` with the parentheses; every marker and phrase search is the phrase form `text ~ "\"...\""`** (a search that needs two phrases is `text ~ "\"a\"" AND text ~ "\"b\""` inside the parentheses); GETs at no more than 5 per second; paginate `GET /rest/api/3/search/jql` with `nextPageToken` until `isLast`. **Controls for a zero:** `qqzzxx9` reads 0 (the nonsense control) and `REC-LAND4-461-11NOV` reads exactly HPSMPOC-461 (the positive control); both printed with every batch of searches.

## THE JIRA TEXT RULES (R217's `scan1518.py`, copied with the changes of READ WHOLE item 2; a hit is a STOP for that text)
Banned in every Jira text and in the entry's added lines: every `\bC-[0-9]{1,4}[a-z]?\b` except your own entry citation `entry C-<CE>` (the map's row ids such as `C-landing` and `C-rename` are not matches and stay), `Tuesday`, `gate`, `seat`, `brief`, `coordinator`, `kit`, `drafter`, `lane`, any brief number (`B` plus digits), any seat id, `@`, any host or URL, a 20+ hex run, `hpsmpoc-` followed by a letter, a path of the coordinator's tree, a board card id, `.NET` as a host suffix, and every ban-list name (underscore-aware `(?<![A-Za-z])<name>(?![a-z])`, case-insensitive; at least `Kam`, `Kamil`, `Kreiser`, `Friday`, `Wednesday`, `Marco`). **`HP` as a word is banned in the summary and in the prose of a body, with two exemptions that the drafter's scan applies and yours must: (a) a `CODE:` line (a verbatim quotation of a map row, a source-document line or a map question), and (b) the exact product names `HP Security Manager`, `HP Security Services Playbook`.** The quoted lines are exempt because the task is to quote them verbatim; the drafter's own scan over the nine frozen texts below printed 0 problems and 0 `HP` hits outside the exemptions. Controls that must fire: a planted `entry C-9999`, `B170`, `Tuesday`, `gate`, the first ban-list name, `_by_Kam_`, `C-347`, `.NET`, and a prose `HP` outside a `CODE:` line; your own `entry C-<CE>` passes and a `CODE:` line with `HP` passes. **Characters:** the only non-ASCII characters allowed are those the source document's quoted lines hold: U+2014, U+2019, U+201C, U+201D, U+2192, U+2022 (the drafter's census over the quoted lines read only U+2014, U+201C, U+201D and U+2192); print a census over every payload, with controls: a planted U+202E, U+200B and U+00A0 must each fire; any other character is a STOP (the project's hidden-character tests scan every tracked file, and a Jira text is not tracked, but the same rule applies). **Summaries: print each frozen summary's length; a create is refused above 255 characters** (the ledger rule that bit the earlier records pass, whose create was refused at 339). The nine summaries read 202, 231, 186, 192, 211, 195, 158, 208 and 211 characters at drafting (program count). **No absence claim ("gone", "no longer", "none exists") in any text unless a grep at stamp time prints it with a control**: the texts below make these absence claims, and only these: **(i)** T1 "the phase decision document holds no landing or hero item" (MEASURED-BY-DRAFTER: `grep -i -c -E 'landing|hero'` over the phase decision document prints 0; control: the same pattern over the messaging map prints 10 lines, and `grep -i -c 'talk track'` over the document prints 3); **(ii)** T1 "the site has no landing, about or marketing page (56 page routes read; none is one)", **(iii)** T3 "it has no introduction", **(iv)** T7 "no slot in the conversation coach". Claims (ii) to (iv) are RELAYED from the map, which measured them at code main `c717ba1a` (page census 56 `page.tsx`, 0 landing/about/welcome routes, control the 56); the drafter did NOT re-measure them. **At Step 2 you re-measure each at your code main** (`gh api -X GET repos/datasecau/HPSM-POC/git/trees/<main sha>?recursive=1`, paths under `web/src/app` named `page.tsx` (expect 56) and, among all paths, `landing`, `about`, `marketing` (expect 0 page routes), the report's source files for an introduction, `ConversationCoach.tsx` for an opener), each with its positive control; **a claim whose re-measure prints a hit HOLDS: that ticket is posted with the sentence removed by program, or HOLDS if it carries the claim in the summary (none does), and STATUS names it.** Re-run (i) too.

## THE TICKETS (frozen texts; fill by program only: `<<RELATED>>` = the keys your searches found as related, each as `HPSMPOC-<n> (<its status as read>)`, minus the ticket's own target, or the words `none found` when there are none; `<<READ-DATE>>` is not used; nothing else is filled)

**The rule for all nine (SEARCH-BEFORE-CREATE, per ticket, before any write):** (1) run the marker search `text ~ "\"REC-HELD-<Tn>-12NOV\""` (0 expected; a key that already carries it means the ticket is done: skip and name it); (2) run the ticket's phrase searches below (each phrase form, each with the controls printed); (3) read EVERY hit whole (summary, status, labels, description, comments) and apply the ticket's HIT rule: a **hit** is an OPEN ticket (Backlog or In Progress, never Done) that decides or asks for the SAME page or change as the held row; a ticket that is only nearby is **related**, not a hit; (4) **one hit: the write is ONE comment on it** (the frozen summary as the first paragraph, then the frozen body; a hit that is Done gets no comment: create instead and name the Done key as related); **two or more hits: write nothing for that ticket, name them in STATUS and go on** (never choose between them without Tuesday); **no hit: ONE create**. Print the search table (ticket, phrase, count, keys, status of each, hit yes/no and why) into STATUS before the write.

**Fields common to every create:** type `Task`; no parent, link, assignee, priority or attachment. **Labels** are per ticket below: `messaging-2026-11-12` is new (0 uses at drafting; the board's own pattern is a dated campaign label such as `catalogue-2026-11-09`, 13 uses), `next-phase` (3 uses; "backlog only; not built in this phase"), `gather` (7 uses; "needs input"), `awaiting-hp` (9 uses) and `follow-up` (6 uses) exist already.

**Body form:** BLUF, Recommendation, Detail (the project's ticket form). A line starting `CODE: ` becomes an ADF `codeBlock` with that prefix removed; every other line is one ADF paragraph; the marker is the last paragraph. The frozen sha256 you print is over the body lines joined by `\n` (UTF-8). **The drafter's sha256 over each body at drafting (before the `<<RELATED>>` fill) is printed in the table below; yours differs after the fill and is the one you freeze.**

| Ticket | Held items (16 in 9) | Labels | Summary length | Drafter's body sha256 prefix | Expected outcome |
|---|---|---|---|---|---|
| T1 | C-landing, H-hero | `messaging-2026-11-12`, `next-phase`, `gather` | 202 | 8d393549a751c8ce | create |
| T2 | C-rename, C-training | `messaging-2026-11-12`, `next-phase` | 231 | 58c005bd2120a2a8 | create |
| T3 | R6, R7 | `messaging-2026-11-12`, `gather` | 186 | abd6148f38117b45 | create |
| T4 | C-modes, C-phase3 | `messaging-2026-11-12`, `next-phase` | 192 | 7b5009885032cb95 | create |
| T5 | C-gbb | `messaging-2026-11-12`, `next-phase` | 211 | e160c74c3442d3e0 | comment on HPSMPOC-392 (expected hit) |
| T6 | C-stages, C-metrics | `messaging-2026-11-12`, `next-phase` | 195 | c250acab757f2134 | create |
| T7 | C-coach | `messaging-2026-11-12`, `next-phase` | 158 | a97076b641153988 | create |
| T8 | C-deck, K2, K3 | `messaging-2026-11-12`, `awaiting-hp` | 208 | 768b6c51d7e071e2 | create |
| T9 | H6 | `messaging-2026-11-12`, `follow-up` | 211 | 40cbad639d8546f7 | create (conditional, Step 2) |

**Why nine and not sixteen (the creation rule, applied):** one ticket per logical path; rows that one test pass proves are one ticket with a checklist, split only for separate workloads. T1 = one placement decision (a new page or a new Home block); T2 = one rename across the journey and the Training labels; T3 = one surface (the customer report); T4 = one pair of content files (the partner showcase); T6 = the metrics count the stages; T8 = one hash-pinned content file and one new content version; T5, T7, T9 are single rows. The drafter's choices on the grouping are open questions for Tuesday in the report; a different grouping changes the texts, so it is decided at the stamp, not by you.

### T1: C-landing, H-hero
- **Marker:** `REC-HELD-T1-12NOV`. **Labels:** `messaging-2026-11-12`, `next-phase`, `gather`. **Summary (202 characters):**

  SUMMARY-T1: Messaging, held for later: place the partner landing page copy (headline, introduction, six modules, closing) and the Home hero block; the site has no slot for either, so a location must be chosen first

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"landing page"`; `"hero block"`; `"copy deck"`; `"YOUR CUSTOMERS TRUST YOU"`.
- **HIT rule:** an open ticket whose description asks for the partner landing page copy or a hero block on Home. Expected: no hit. HPSMPOC-310 (Done) holds the words landing page and is not a hit.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** HPSMPOC-457 (partner dashboard rebuild, Backlog).
- **Body (frozen, 5869 characters before the fill):**

BEGIN BODY-T1
BLUF: the document's partner landing page copy (headline, introduction, six modules, closing copy) and the Playbook home hero block have no place on the site today, so nothing is changed. The words are the document's and are ready to place once a location is chosen. Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: nowhere; Home gets only the promise, the call to action and the closing copy. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | C-landing | "Primary partner landing page": headline "YOUR CUSTOMERS TRUST YOU WITH THEIR PRINT ENVIRONMENT. HELP THEM SECURE WHAT COMES NEXT.", the introduction, the six modules (Start with a conversation / Turn uncertainty into clarity / Connect findings to action / Help decision-makers act / Create opportunity your way / Stay valuable beyond the first project) and the closing copy | no landing, about or marketing page (56 `page.tsx` routes read under `web/src/app`; none is one; no `web/public` folder) | not built: a new page or a new Home block. The words are the document's and are ready to place once a location is chosen | MA:208-231 | C |
CODE: | H-hero | Home, new block under the greeting: trust-led promise, three lifecycle phases, partner models, short proof points | none exists | none proposed (a new block is layout; the document gives the emphasis, not the words, for this block) | MA:172-175 | C |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 172: Playbook home / hero
CODE: line 173: HP account managers, resellers, partner principals
CODE: line 174: Trust-led promise, three lifecycle phases, partner models, short proof points.
CODE: line 175: Start a customer assessment
CODE: line 208: 7  Approved-for-review copy deck
CODE: line 209: Draft language for HP / Datasec editorial and product-owner review. This is proposed wording—not evidence of final HP approval.
CODE: line 210: Primary partner landing page
CODE: line 211: YOUR CUSTOMERS TRUST YOU WITH THEIR PRINT ENVIRONMENT. HELP THEM SECURE WHAT COMES NEXT.
CODE: line 212: Introducing the HP Security Services Playbook. A simpler way to start meaningful security conversations, turn customer concerns into practical action and create new opportunities for your business.
CODE: line 213: Your customers rely on you to keep their print environments moving. As security requirements evolve, they also need help understanding potential gaps, evidence and priorities. The Playbook gives your team a guided way to lead that conversation and agree the next step.
CODE: line 214: Six reusable modules
CODE: line 215: Module headline
CODE: line 216: Supporting copy
CODE: line 217: Start with a conversation.
CODE: line 218: Guided discovery helps sellers ask the right questions, understand the print environment and involve relevant customer stakeholders—without presenting them as cybersecurity specialists.
CODE: line 219: Turn uncertainty into clarity.
CODE: line 220: Evidence-linked assessments distinguish reviewed risks from unknowns and out-of-scope conditions, helping customers understand priorities and limitations.
CODE: line 221: Connect findings to action.
CODE: line 222: Recommendations identify relevant technical options and applicable HP capabilities, with prerequisites, responsibilities and verification needs made clear.
CODE: line 223: Help decision-makers act.
CODE: line 224: Customer-facing executive reports explain reviewed findings in business terms, while technical detail supports engineering and delivery teams.
CODE: line 225: Create opportunity your way.
CODE: line 226: Use the same methodology for product-led selling, managed services or specialist security delivery. Each model supports different commercial paths.
CODE: line 227: Stay valuable beyond the first project.
CODE: line 228: Ongoing reviews, remediation follow-up and periodic optimisation give partners a continuing reason to engage customers.
CODE: line 229: Closing copy
CODE: line 230: LANDING PAGE CTA
CODE: line 231: You have the customer relationship. You have the HP expertise. Now you have a clearer way to turn both into customer value.Start with one customer. Build what comes next.
Phase decision document (v2.1), item(s): D-043 - Rebuild the partner dashboard around the commercial pipeline (NEXT PHASE). No D-item names the landing page or the hero block (a search of the phase decision document for the words landing and hero reads 0). The map links D-043, the partner dashboard rebuilt around the pipeline, to the hero row; D-043 is Next phase.
Why it is held: The map's hold reason, row C-landing: the site has no landing, about or marketing page (56 page routes read; none is one), so this is a new page or a new Home block. Row H-hero: a new block is layout, and the document gives the emphasis for the hero block, not the words. The map's text pass gives Home only the promise, the call to action and the closing copy (its rows H1 to H4).
The map's question and default, quoted verbatim:
CODE: 2. **Landing copy deck (C-landing, H-hero).** Where should the six-module landing copy live: a new block on Home, or a new page? Default: nowhere; Home gets only the promise, the CTA and the closing copy (H1-H4).
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T1-12NOV]
END BODY-T1

### T2: C-rename, C-training
- **Marker:** `REC-HELD-T2-12NOV`. **Labels:** `messaging-2026-11-12`, `next-phase`. **Summary (231 characters):**

  SUMMARY-T2: Messaging, held for later: rename the in-app journey to Discover, Assess, Recommend, Engage (customer workspace steps and the Training page's three labels); a layout and workflow change held by the product owner's 2026-11-10 ruling

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"Discover, Assess, Recommend"`; `"Discover and scope"`; `"journey rename"`; `"Eight-step journey"`.
- **HIT rule:** an open ticket whose description asks to rename the journey or the Training labels to Discover, Assess, Recommend, Engage. Expected: no hit. HPSMPOC-453 (journey rail numbering), HPSMPOC-452 (Training page header and steps) and HPSMPOC-394 (Training principles) are related, not hits; HPSMPOC-465 is Done.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** HPSMPOC-452 (partner pages, Backlog); HPSMPOC-453 (customer register and workspace, Backlog); HPSMPOC-394 (Training principles, needs input, Backlog).
- **Body (frozen, 4834 characters before the fill):**

BEGIN BODY-T2
BLUF: the document asks for the same four terms (Discover, Assess, Recommend, Engage) across the partner workflow, the customer workspace's eight-step journey and the Training page's three labels. That is a rename plus the layout and workflow it implies, held by the product owner's 2026-11-10 ruling, so nothing is changed. Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: no, held with the 2026-11-10 ruling; he may say 'rename too'. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | C-rename | the customer workspace's eight-step journey labels (`components/shell/customer-nav.ts`, `components/shell/CustomerShell.tsx`) and every "Discover / Assess / Recommend / Engage" use | Profile, Assessment, Score & findings, ... | held: the journey RENAME and any layout or workflow change | MA:99-121, MA:206-207; the product owner's 2026-11-10 ruling; D-064 | C |
CODE: | C-training | `components/partner/TrainingScreen.tsx:12` (`TRAINING_STEPS`: "Discover and scope", "Assess and verify", "Advise and deliver") | three labels | the partner workflow Discover, Assess, Recommend, Engage (MA:106-121, MA:207) | MA:106-121, MA:207 | C |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 99: 4  Connect the messaging to the Playbook journeys
CODE: line 100: Separate the journey that opens a commercial opportunity from the lifecycle that delivers a security outcome.
CODE: line 101: Partner sales and engagement journey
CODE: line 102: Stage
CODE: line 103: Partner action
CODE: line 104: Customer value
CODE: line 105: Playbook support
CODE: line 106: Discover
CODE: line 107: Select account, open discussion, capture environment and stakeholders.
CODE: line 108: A relevant conversation tied to business priorities.
CODE: line 109: Account workspace, guided discovery and customer context.
CODE: line 110: Assess
CODE: line 111: Gather responses, collect evidence and determine applicability.
CODE: line 112: Initial view of gaps, unknowns and verified risks.
CODE: line 113: Assessment model, evidence capture and review workflow.
CODE: line 114: Recommend
CODE: line 115: Prioritise findings, identify options and propose next steps.
CODE: line 116: Actionable plan with dependencies and ownership.
CODE: line 117: Reviewed recommendations, report narrative and HP solution mapping.
CODE: line 118: Engage
CODE: line 119: Agree decision, propose scope and manage follow-up.
CODE: line 120: Clear accountability and a practical route to improvement.
CODE: line 121: Tasks, service offers, opportunity pipeline and next-action visibility.
CODE: line 206: UX consistency
CODE: line 207: Within the Playbook, use the same terms for the journey and underlying artifacts: Discover, Assess, Recommend and Engage for the partner workflow; Assess, Implement and Optimize for the customer service lifecycle. Use short summaries, contextual help, clear workflow states and explicit distinctions between an identified opportunity and recognised revenue.
Phase decision document (v2.1), item(s): D-064 - Journey rail: "Eight-step journey", numbered headings, Metrics set apart (NEXT PHASE); D-047 - Training page: descriptions, a six-part learning pathway and five assessment principles (NEXT PHASE). The map links D-064 to the rename and D-047 to the Training page. As the phase decision document reads, D-064 covers the rail heading, the numbered step headings and Metrics set apart, and D-047 covers the Training page descriptions, pathway and principles; neither names the Discover, Assess, Recommend, Engage rename itself. Both are Next phase.
Why it is held: The map's hold reason, row C-rename: the journey rename and any layout or workflow change are held by the product owner's 2026-11-10 ruling (he may say 'rename too'). Row C-training: the three labels would become the partner workflow Discover, Assess, Recommend, Engage.
The map's question and default, quoted verbatim:
CODE: 1. **Journey rename (C-rename, C-training).** Do you want the in-app journey renamed to Discover, Assess, Recommend, Engage now, with the layout and workflow it implies? Default: no, held with your 2026-11-10 ruling; he may say 'rename too'.
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T2-12NOV]
END BODY-T2

### T3: R6, R7
- **Marker:** `REC-HELD-T3-12NOV`. **Labels:** `messaging-2026-11-12`, `gather`. **Summary (186 characters):**

  SUMMARY-T3: Messaging, held for later: the customer report's introduction (the document gives emphasis, no sentence) and whether the Next Engagement section stays in the customer's report (a ruling)

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"report introduction"`; `"customer report" AND text ~ "introduction"`; `"Next Engagement" AND text ~ "customer report"`.
- **HIT rule:** an open ticket whose description decides or asks whether the Next Engagement section stays in the customer report, or asks for the report introduction. Expected: no hit.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** none.
- **Body (frozen, 3553 characters before the fill):**

BEGIN BODY-T3
BLUF: two held points on the customer report: it has no introduction and the document supplies no sentence for one (row R6), and the Next Engagement section (section 8 of 9) waits on a ruling whether it belongs in the customer's report (row R7). Nothing is changed. Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: none for the introduction (the report keeps its cover and methodology); the Next Engagement section stays. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | R6 | the customer report (PDF, `api/.../ReportModelBuilder.cs`; screen `components/screens/ReportScreen.tsx`): a new introduction | no introduction exists. The cover is "Security Assessment [em dash] Executive Report", section 1 opens with key figures | none proposed: the document names "customer report introductions" as an activity (MA:273) and lists emphasis for the surface (MA:192-195) but gives no sentence | MA:192-195, MA:273 | C |
CODE: | R7 | the report's section "Next Engagement" (`api/.../Report/ReportModel.cs:25`, `ReportScreen.tsx:139`) | section 8 of 9 | held for the phase document's ruling on whether it belongs in the customer report | MA:161; D-019 | C |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 161: Customer executive and technical reports must not display partner margins, opportunity pipeline or internal sales attribution by default.
CODE: line 192: Customer executive report
CODE: line 193: CIO, IT, business and security leaders
CODE: line 194: Business exposure, scope, confidence, reviewed findings and recommended priorities.
CODE: line 195: Approve the action plan
CODE: line 273: Update hero, partner page, talk track, demo narrative, EDM copy and customer report introductions. Build concise product-led and MPS journeys.
Phase decision document (v2.1), item(s): D-019 - Decide whether "Next engagement" belongs in the customer's security report (THIS PHASE). Row R7 is D-019, Decide whether 'Next engagement' belongs in the customer's security report; the phase decision document recommends THIS PHASE (a ruling rather than work). Row R6 has no D-item.
Why it is held: The map's hold reason, row R6: the document names customer report introductions as an activity and lists emphasis for the surface but gives no sentence. Row R7: held for the phase document's ruling on whether the section belongs in the customer report. The phase document recommends this phase for D-019; the product owner's 2026-11-12 11:21 instruction puts it for later.
The map's question and default, quoted verbatim:
CODE: 3. **Customer report introduction (R6).** Do you want to supply the introduction sentence, or approve one drafted from MA:192-195? Default: none; the report keeps its cover and methodology.
CODE: 4. **Next engagement in the customer report (R7, D-019).** Does the section stay in the customer's report? Default: it stays.
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T3-12NOV]
END BODY-T3

### T4: C-modes, C-phase3
- **Marker:** `REC-HELD-T4-12NOV`. **Labels:** `messaging-2026-11-12`, `next-phase`. **Summary (192 characters):**

  SUMMARY-T4: Messaging, held for later: three partner operating modes (product-led, managed services, security specialist) as a switchable commercial mode, and the Phase 3 Managed service / Optimize naming

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"operating modes"`; `"Phase 3 - Managed service"`; `"product-led"`; `"managed service" AND text ~ "Optimize"`.
- **HIT rule:** an open ticket whose description asks for the three operating modes or for the Phase 3 rename. Expected: no hit. HPSMPOC-167 (phase pages, awaiting the customer's deck), HPSMPOC-456 and HPSMPOC-452 are related, not hits.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** HPSMPOC-167 (phase pages, awaiting the customer's deck, Backlog); HPSMPOC-452 (partner pages, Backlog); HPSMPOC-456 (commercial pages, Backlog).
- **Body (frozen, 5199 characters before the fill):**

BEGIN BODY-T4
BLUF: the document's three partner motions are a switchable commercial mode, not a label swap (row C-modes), and renaming Phase 3 Managed service to Optimize would drop managed service as the only third phase (row C-phase3). Nothing is changed. Both rows edit the same pair of partner showcase content files, so they are one ticket with a checklist. Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: yes, next phase; the wording rows already stop presenting fees as the standard motion. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | C-modes | `content/client/partner-showcase.v0.1.0.json:121-134` (delivery models "Partner delivered", "Co-delivered", "Referral") | three delivery models | the document's three motions (product-led reseller, managed services partner, security services specialist, MA:142-157) are a switchable commercial mode, not a label swap; D-023 is next phase | MA:142-163 | C |
CODE: | C-phase3 | `content/partner/partner-showcase.v0.1.0.json:55-63` and the client copy `content/client/partner-showcase.v0.1.0.json:55-63` (phase labels "Phase 1 - Assessment", "Phase 3 - Managed service"), and the page title "Phase 3 - Managed service" at `app/(app)/services/managed/page.tsx:4` | "Phase 3 - Managed service" | a rename to "Optimize" would drop managed service as the only third phase (MA:140-157 has three motions); held with D-056 | MA:84, MA:142-157 | C |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 84: Assess. Implement. Optimize.
CODE: line 140: 5  Partner-led commercial architecture
CODE: line 141: The same evidence-led methodology should support different reseller economics.
CODE: line 142: Partner operating model
CODE: line 143: Starting engagement
CODE: line 144: Commercial opportunity
CODE: line 145: Message to partner
CODE: line 146: Product-led reseller
CODE: line 147: No-fee or bundled security review that supports a hardware/software discussion.
CODE: line 148: HP security software and features, secure release, authentication, appropriate refresh, renewals and account retention.
CODE: line 149: “Use security to make your next product conversation more relevant.”
CODE: line 150: Managed services partner
CODE: line 151: Security review built into an MPS/service relationship.
CODE: line 152: Policy assurance, remediation projects, ongoing reviews, managed services and software renewals.
CODE: line 153: “Extend the contract from uptime and cost to continuous security value.”
CODE: line 154: Security services specialist
CODE: line 155: Scoped discovery or formal technical assessment, followed by implementation.
CODE: line 156: Paid assessment, integration, remediation, advisory and ongoing assurance.
CODE: line 157: “Create repeatable, evidence-led engagements with a clear delivery pathway.”
CODE: line 158: Opportunity management principles
CODE: line 159: Commercial opportunity stages remain distinct: identified → qualified → quoted → booked → recognised.
CODE: line 160: Opportunity estimates must not be equated with contracted revenue, gross profit or employee commission.
CODE: line 161: Customer executive and technical reports must not display partner margins, opportunity pipeline or internal sales attribution by default.
CODE: line 162: Partner choice changes the offer and commercial motion—not the underlying assessment evidence, severity or technical finding.
CODE: line 163: Support a zero-consulting-invoice journey, consistent with the reseller validation feedback.
Phase decision document (v2.1), item(s): D-023 - Three reseller operating modes that change the commercial pages but never the findings (NEXT PHASE); D-056 - Delivery phases page: phase descriptions and an inline offer sheet (NEXT PHASE). The map links D-023 (three reseller operating modes that change the commercial pages but never the findings) to C-modes and D-056 (Delivery phases page: phase descriptions and an inline offer sheet) to C-phase3. Both are Next phase.
Why it is held: The map's hold reason, row C-modes: a switchable commercial mode, and D-023 is Next phase. Row C-phase3: a rename to Optimize would drop managed service as the only third phase because the document has three motions; held with D-056.
The map's question and default, quoted verbatim:
CODE: 5. **Three operating modes (C-modes, D-023) and the Optimize / managed-service naming (C-phase3).** Next phase as the phase document says? Default: yes, next phase; the wording rows (P3, P5, W12-W13) already stop presenting fees as the standard motion.
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T4-12NOV]
END BODY-T4

### T5: C-gbb
- **Marker:** `REC-HELD-T5-12NOV`. **Labels:** `messaging-2026-11-12`, `next-phase`. **Summary (211 characters):**

  SUMMARY-T5: Messaging, held for later: Good / Better / Best as partner-selected packages (a page); tiers appear today only as groups of recommended settings, and no automatic need for paid consulting or hardware replacement

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"packages page"`; `"Good / Better / Best"`; `"partner-selected"`.
- **HIT rule:** an OPEN ticket whose description decides or asks for the Good / Better / Best packages page. Expected: HPSMPOC-392 (Backlog, needs input, 'packages page, pricing reading of the words') is a HIT: the text is posted there as ONE comment and nothing is created. HPSMPOC-456 (its item P2-070 is the packages page) and HPSMPOC-165 are related, not the target.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** HPSMPOC-392 (packages page decision, Backlog); HPSMPOC-456 (commercial pages, item P2-070, Backlog); HPSMPOC-165 (modular services content, Backlog).
- **Body (frozen, 2205 characters before the fill):**

BEGIN BODY-T5
BLUF: the document describes Good / Better / Best as partner-selected packages informed by risk and scope. A packages page is new, so nothing is built; the wording rule is already applied to the existing tier sentence (map row R2). Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: yes, next phase; row R2 applies the wording rule to the existing tier sentence. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | C-gbb | Good / Better / Best as partner-selected packages (a page) | tiers appear only as groups of recommended settings | a packages page is new; D-027 is next phase. The wording rule is applied in R2 | MA:250 | C |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 249: Good / Better / Best offers
CODE: line 250: Describe as partner-selected packages informed by risk and scope; no automatic requirement for paid consulting or hardware replacement.
CODE: line 251: Channel, services and commercial owners.
Phase decision document (v2.1), item(s): D-027 - Good / Better / Best service packages page (NEXT PHASE). D-027, Good / Better / Best service packages page, is Next phase (it reverses an earlier ruling and the tier descriptions need the product owner's approval as content).
Why it is held: The map's hold reason, row C-gbb: a packages page is new; D-027 is Next phase.
The map's question and default, quoted verbatim:
CODE: 6. **Good / Better / Best packages page (C-gbb, D-027).** Next phase? Default: yes; R2 applies the wording rule to the existing tier sentence.
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T5-12NOV]
END BODY-T5

### T6: C-stages, C-metrics
- **Marker:** `REC-HELD-T6-12NOV`. **Labels:** `messaging-2026-11-12`, `next-phase`. **Summary (195 characters):**

  SUMMARY-T6: Messaging, held for later: commercial stages (identified, qualified, quoted, booked, recognised) as dashboard states, and the success metrics to instrument; both are new records and new behaviour

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"commercial stages"`; `"success metrics"`; `"recognised"`; `"attribution preview"`.
- **HIT rule:** an open ticket whose description asks for the five commercial stages as states or for the success metrics. Expected: no hit. HPSMPOC-454, HPSMPOC-456 and HPSMPOC-457 (the opportunity record, commercial pages and dashboard rebuild) are related, not hits.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** HPSMPOC-454 (opportunity record and pipeline, Backlog); HPSMPOC-456 (commercial pages, Backlog); HPSMPOC-457 (partner dashboard rebuild, Backlog).
- **Body (frozen, 4322 characters before the fill):**

BEGIN BODY-T6
BLUF: the document wants five commercial stages as dashboard states and a set of success metrics to instrument. Both need new records, states and instrumentation, so nothing is built; the language rule is carried meanwhile by the text pass (map rows H6, R4 and R5). Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: yes, next phase; H6, R4 and R5 carry the language rule meanwhile. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | C-stages | commercial stages identified, qualified, quoted, booked, recognised, as dashboard states (and the attribution preview, `components/screens/AttributionPreviewScreen.tsx`) | none; the preview is labelled next phase and sample | new records and states; D-024 to D-026 and D-043 are next phase. R4/H6 carry the language rule meanwhile | MA:159-163, MA:256 | C |
CODE: | C-metrics | the document's success metrics to instrument (MA:281-287) | none | instrumentation is new behaviour; D-059 is next phase | MA:281-287 | C |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 159: Commercial opportunity stages remain distinct: identified → qualified → quoted → booked → recognised.
CODE: line 160: Opportunity estimates must not be equated with contracted revenue, gross profit or employee commission.
CODE: line 161: Customer executive and technical reports must not display partner margins, opportunity pipeline or internal sales attribution by default.
CODE: line 162: Partner choice changes the offer and commercial motion—not the underlying assessment evidence, severity or technical finding.
CODE: line 163: Support a zero-consulting-invoice journey, consistent with the reseller validation feedback.
CODE: line 255: Commercial dashboard
CODE: line 256: Separate lead/forecast values from booked and recognised revenue; do not expose partner economics in customer reports.
CODE: line 257: Channel operations / finance / privacy.
CODE: line 281: Success metrics to instrument
CODE: line 282: Adoption & experience
CODE: line 283: Customer value
CODE: line 284: Commercial progression
CODE: line 285: Partners activated; sellers trained; discovery starts; assessments completed; time-to-first-engagement.
CODE: line 286: Assessment completion and evidence-confidence rates; reports approved; agreed action plans; remediation follow-up.
CODE: line 287: Qualified opportunities by model and offer; quotes issued; booked/recognised amounts; renewals; service attachment.
Phase decision document (v2.1), item(s): D-024 - Opportunity register and pipeline (deals separate from assessments) (NEXT PHASE); D-025 - Quote builder, contracts and renewals, sales dashboard (NEXT PHASE); D-026 - Revenue attribution by participant (replaces the attribution preview) (NEXT PHASE); D-043 - Rebuild the partner dashboard around the commercial pipeline (NEXT PHASE); D-059 - Automation metrics: add four summary tiles (NEXT PHASE). The map links D-024 to D-026 and D-043 to C-stages and D-059 to C-metrics; all are Next phase. D-059 as the phase decision document reads is 'Automation metrics: add four summary tiles' on the existing runs table, which is related to but not the same as the document's success metrics (lines 281-287).
Why it is held: The map's hold reason, row C-stages: new records and states; D-024 to D-026 and D-043 are Next phase. Row C-metrics: instrumentation is new behaviour; D-059 is Next phase. Both rows stay together because the metrics count the stages.
The map's question and default, quoted verbatim:
CODE: 7. **Commercial stages and success metrics (C-stages, C-metrics).** Next phase? Default: yes; H6, R4 and R5 carry the language rule meanwhile.
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T6-12NOV]
END BODY-T6

### T7: C-coach
- **Marker:** `REC-HELD-T7-12NOV`. **Labels:** `messaging-2026-11-12`, `next-phase`. **Summary (158 characters):**

  SUMMARY-T7: Messaging, held for later: the account-manager opener and the 30-second talk track have no slot in the conversation coach; add them or keep the coach as it is

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"account manager opener"`; `"conversation coach"`; `"talk track"`.
- **HIT rule:** an open ticket whose description asks to add the opener or talk track to the coach. Expected: no hit. HPSMPOC-395 (audience testing of the coach output) is related, not a hit.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** HPSMPOC-395 (audience testing, needs input, Backlog).
- **Body (frozen, 2562 characters before the fill):**

BEGIN BODY-T7
BLUF: the document's account-manager opener and talk track have no slot in the conversation coach, whose guides are general and marked as sample. Nothing is changed. Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: no; next phase. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | C-coach | `components/customer/ConversationCoach.tsx:174` and the coach content | "Practise customer conversations: messaging, objection handling and next steps." | the document's account-manager opener (MA:297) and talk track (MA:94) have no coach slot; D-069 is next phase | MA:297, MA:94 | C |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 94: The HP Security Services Playbook gives partners a guided way to start customer security conversations, identify and review print security risks, connect findings to relevant HP solutions and plan next steps. It supports product-led sales, managed service reviews and specialist engagements across Assess, Implement and Optimize.
CODE: line 296: Option C — Account manager opener
CODE: line 297: “We already help you manage your print environment. We can also help you review how its security controls align with your current needs. The first step is a guided conversation to identify what is working, what needs evidence and where action could add value.”
Phase decision document (v2.1), item(s): D-069 - Conversation coach: add the HTML's five talk tracks (NEXT PHASE). D-069, Conversation coach: add the HTML's five talk tracks, is Next phase (a content choice: add the five, replace the eight, or keep the eight).
Why it is held: The map's hold reason, row C-coach: no coach slot exists for the opener or the talk track; D-069 is Next phase.
The map's question and default, quoted verbatim:
CODE: 8. **Coach opener (C-coach, D-069).** Add the account-manager opener to the coach now? Default: no; next phase.
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T7-12NOV]
END BODY-T7

### T8: C-deck, K2, K3
- **Marker:** `REC-HELD-T8-12NOV`. **Labels:** `messaging-2026-11-12`, `awaiting-hp`. **Summary (208 characters):**

  SUMMARY-T8: Messaging, held for later: the Playbook deck's own sentences (automatic deployment, trusted advisor wording) and the firmware update question; need a Security Manager expert sentence and a new content version

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"deploys them automatically"`; `"regular or automated updates"`; `"trusted advisor"`; `"playbook-placeholder"`.
- **HIT rule:** an open ticket whose description asks to change the deck's deployment or firmware sentences. Expected: no hit. HPSMPOC-167 (phase pages awaiting the customer's deck), HPSMPOC-259 and HPSMPOC-240 (firmware tool answers) are related, not hits.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** HPSMPOC-167 (phase pages awaiting the deck, Backlog); HPSMPOC-259 (next-phase integration, Backlog).
- **Body (frozen, 4965 characters before the fill):**

BEGIN BODY-T8
BLUF: the deck's own sentences (rows K2 and K3) say HP Security Manager deploys settings automatically and ask whether firmware is kept current through automated updates; the document says these claims need a Security Manager expert, so they are not changed. Row C-deck records that the deck's marketing voice is kept as it is. All three are the same hash-pinned content files, so a change is one new content version. Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: unchanged; they ride with D-004 to D-006. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | C-deck | `content/client/playbook-placeholder.v0.7.0.json` (117 case-insensitive hits for revenue, consult, HP-backed, automatic, recurring, trust; for example `:83`, `:92` "trusted advisor", `:110`, `:159`, `:315`) | the deck's marketing voice | no change: it is HP's deck, not the product's own positioning (D-058 keeps it) | MA:11; D-058 | C |
CODE: | K2 | `content/client/playbook-placeholder.v0.7.0.json:2108` and `:2129` | "The good news is that HP Security Manager deploys them automatically across the entire fleet. It's not a manual process for each device. For most customers, the deployment takes less than an hour..." (`:2108`); "Protect Devices [em dash] Firmware updated and HP Security Manager policy deployed for continuous compliance" (`:2129`) | hold: needs an HP Security Manager SME sentence on what is deployed, to which devices, with what prerequisites. The document gives the rule, not the sentence. Not changed in this pass | MA:62, MA:241-245, MA:64 ("Automatic remediation" under Avoid) | D |
CODE: | K3 | `content/client/playbook-placeholder.v0.7.0.json:4182` (question "Is your printers' firmware kept current through regular or automated updates?") and the 13 findings that say "Apply the HP Security Manager settings listed..." | as is | hold with D-004 and D-005 (this phase, needs HP SME wording) | MA:244 | D |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 11: Draft copy supplied for review (12 November 2026); HP Security Services Playbook v2.2 internal recommendations (9 November 2026). Proposed public-facing statements remain subject to HP brand, product and legal approval.
CODE: line 62: “Every finding maps to an HP Security Manager setting”
CODE: line 64: Automatic remediation / mandatory hardware refresh
CODE: line 240: HP Security Manager
CODE: line 241: Mapping to named settings only when supported for the relevant device, firmware and HPSM edition; distinguish assessment/configuration from deployment.
CODE: line 242: HP Security Manager SME.
CODE: line 243: Firmware and device features
CODE: line 244: Do not imply HPSM deploys firmware or that trusted startup can be universally enabled with a switch. Confirm supported hardware, firmware and management tooling.
CODE: line 245: HP print hardware / WXP / Web Jetadmin SMEs.
Phase decision document (v2.1), item(s): D-058 - Keep the site's Playbook module names and text (DROP (keep the site as it is)); D-004 - Correct the firmware update question and its recommendations (THIS PHASE); D-005 - Stop implying that HP Security Manager deploys firmware (THIS PHASE); D-006 - Trusted startup: verify by model instead of "enable", and send unsupported devices to a lifecycle or exception review (THIS PHASE). Row C-deck is D-058, which the phase decision document recommends to DROP (keep the site's module text as it is). Rows K2 and K3 ride with D-004, D-005 and D-006, which the phase document recommends THIS PHASE and which need a subject-matter expert on the customer's print hardware and Security Manager.
Why it is held: The map's hold reason, row K2: it needs an HP Security Manager expert sentence on what is deployed, to which devices and with what prerequisites; the document gives the rule, not the sentence. Row K3: held with D-004 and D-005 (this phase, needs expert wording). Row C-deck: no change; it is the customer's deck, not the product's own positioning (D-058 keeps it). Changing the deck's text is a new content version.
The map's question and default, quoted verbatim:
CODE: 10. **Deck sentences (K2, K3).** Can an HP Security Manager SME supply the sentence on what the product deploys and to which devices? Default: unchanged; they ride with D-004 to D-006.
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T8-12NOV]
END BODY-T8

### T9: H6
- **Marker:** `REC-HELD-T9-12NOV`. **Labels:** `messaging-2026-11-12`, `follow-up`. **Summary (211 characters):**

  SUMMARY-T9: Messaging, held for later: the Illustrative tag's title attribute (Estimate, not booked or recognised revenue) on the Home tile and panel; held from the text pass because the tag lives in a shared component file

- **Phrase searches (each as `text ~ "\"<phrase>\""`):** `"Illustrative tag"`; `"IllustrativeTag"`; `"not booked or recognised"`.
- **HIT rule:** an open ticket whose description asks for the Illustrative tag's title attribute text. Expected: no hit.
- **Related (expected, the drafter's reading at 11:3x; you re-read):** none.
- **Body (frozen, 2224 characters before the fill):**

BEGIN BODY-T9
BLUF: the second half of map row H6, the Illustrative tag's title attribute (H6b), was held out of the text pass because the tag is defined in a shared component file that the pass does not edit; the first half, the tile sub line (H6a), is part of the text pass. Nothing else about row H6 is held. Held, not built, filed for later on the product owner's instruction of 2026-11-12 11:21 AEDT.
Recommendation: keep held. The map's default if the product owner does not answer: build it in the next pass that may edit that shared file. Nothing is built, deployed or tested by this ticket. The product owner's words, 2026-11-12 11:21 AEDT: "messaging mapping looks good. deploy based on this and ticket anything left for later".
Detail. Held row(s) of the messaging map prepared 2026-11-12 (columns: ID, Where, Today, Proposed, Source, Class), quoted verbatim:
CODE: | H6 | `components/partner/PartnerDashboard.tsx:135` (tile "Managed service run-rate, end of year 3") and `:180` (panel "Revenue mix"); both already carry the Illustrative tag | tag text "Illustrative" | add to the tag's title attribute and the tile `sub` line: "Estimate, not booked or recognised revenue." (new words; the tag stays) | MA:160, MA:256 | B |
Source document: Messaging Alignment & Channel Activation Approach, version 1.0, 12 November 2026. Lines of its extracted text, quoted verbatim (the only change: the character sequence for an ampersand is shown as &). In the map rows, MA:n means line n of this text:
CODE: line 160: Opportunity estimates must not be equated with contracted revenue, gross profit or employee commission.
CODE: line 255: Commercial dashboard
CODE: line 256: Separate lead/forecast values from booked and recognised revenue; do not expose partner economics in customer reports.
CODE: line 257: Channel operations / finance / privacy.
Phase decision document item: No D-item.
Why it is held: Why held: the tag's title attribute lives in the shared file web/src/components/partner/parts.tsx (IllustrativeTag), which the text pass does not edit. This ticket exists only if H6b is still unbuilt at the time of filing (a stamp-time check, Step 2).
Related on the board (read at filing): <<RELATED>>.
Marker: [REC-HELD-T9-12NOV]
END BODY-T9

## PART 2: THE ENTRY (CE only, appended after one blank line; `<<...>>` filled by program from the reads named; a value you cannot print makes its sentence `NOT CONFIRMED: <what was read>` and is named in STATUS; heading form `### C-<n> - HPSM-POC: ...` is C-352's)
**The entry's second line (mandated):** `Recorded by the B1539 seat (records) from the Jira reads and writes of <<READ-DATE>>, the messaging map and the source document it cites (kept outside this repository; the map <<LM>> lines, sha256 prefix <<SM>>; the source document <<LS>> lines, sha256 prefix <<SS>>), the phase decision document (kept outside this repository; <<LD>> lines, sha256 prefix <<SD>>), the ruling as relayed by the stamp of the brief B1539 (the board chat and the decision store were not read), and the brief B1539. No board card id is written. This seat built nothing, ran no test, ran no dotnet command, sent nothing to any human and made no request to any app host, database or to Azure.` **The entry's last line:** `Recorded by B1539 SEAT-R222 (records), <<WRITE-DATE>>.` **The other added lines carry neither `Tuesday` nor `FOR TUESDAY` nor any path under the coordinator's tree nor any brief number or seat id nor a person's name nor a card id nor a host name or URL** (closing check as `closing1523.py`, case-insensitive, underscore-aware, with controls). The entry quotes the facts of a stamp slot, never the word of the slot's author. Every figure from a record is a substring of that record (program check) or its sentence reads `NOT CONFIRMED`. The entry cites no other entry by number.

BEGIN <E-E>
### C-<<CE>> - HPSM-POC: the product owner's 2026-11-12 11:21 ruling on the messaging map ("deploy based on this and ticket anything left for later"): the held rows are filed as tickets for later; no held question is decided; <<E-SHORT>>
<second line as above>
- **The ruling (RELAYED, stamp slot RULING-1121; no card id is written).** <<RULING-1121, the slot's sentence verbatim>>. It is an instruction to deploy on the map and to ticket what the map leaves; it decides none of the map's held questions.
- **What is held (DERIVED from the messaging map, which this seat read whole).** The map puts 59 rows to change or hold (A 22, B 13, C 13, D 11). The text pass covers the A rows, the B rows and 9 D rows in their qualified form and is recorded elsewhere, not here. Held and not built: the 13 C rows (C-landing, H-hero, C-rename, C-training, R6, R7, C-modes, C-phase3, C-gbb, C-stages, C-metrics, C-coach, C-deck), the 2 D rows K2 and K3, and H6b (the held half of row H6) when it was still unbuilt at the filing: <<H6B-LINE>>.
- **What was filed (Jira, MEASURED by this seat at read-back, <<READ-DATE>>).** <<E-PER-TICKET>>
- **Why nine tickets.** Rows that one test pass proves are one ticket with a checklist and the tickets split only on separate workloads: <<GROUPING-LINE>>.
- **What each ticket does not do.** None builds, deploys, tests, renames, moves or closes anything; each records the held row verbatim, its source lines, the phase decision document's item where one exists, the reason it is held and the map's question with its default (hold).
- **Not settled.** Every held question of the messaging map (the journey rename, where the landing copy lives, the report introduction, Next Engagement in the customer report, the operating modes and the Phase 3 naming, the packages page, the commercial stages and metrics, the coach opener, the deck sentences): each stays at the map's default, hold. Hosted: nothing is put on a host by this entry or by the tickets; UAT is held.
Recorded by B1539 SEAT-R222 (records), <<WRITE-DATE>>.
END <E-E>

`<<E-SHORT>>` = a short clause counting the tickets by program (e.g. `eight tickets created and one comment on an existing ticket`). `<<E-PER-TICKET>>` = for T1 to T9 in order: `T<n> (<rows>): HPSMPOC-<key> created` or `T<n> (<rows>): comment <id> on HPSMPOC-<key>` or `T<n> (<rows>): not written (<reason>)`, joined by `; `. `<<H6B-LINE>>` = `T9 filed as HPSMPOC-<key>` or `not filed (<the Step 2 reading that it was built or the slot word>)`. `<<GROUPING-LINE>>` = the nine groupings in one clause, copied from the table above. `<<LM>> <<SM>> <<LS>> <<SS>> <<LD>> <<SD>>` = `wc -l` and the first 16 hex of sha256 you print for the three files. `<<WRITE-DATE>>` = your write date. `<<RULING-1121>>` = the stamp slot with the word `Tuesday` and any card id removed by program (and the removal named in STATUS).

**Text rule for the added record lines:** the scanner over every added line with the exemptions of R217's closing check (the mandated second and last lines), plus every double-quoted fragment that is a substring of the file it quotes (program check; the sources are this kit, the three files above, the Jira reads). Controls fire on a planted `Tuesday`, `B1497`, `H157`, `_by_Kam_`, an `https://` URL, a coordinator-tree path and the card slugs of R217's closing check.

## THE WORK (B1523's steps, in this order)
**Step 0.** `date`; `df -g /Volumes/Datasec_DEV` (STOP under 25 GiB); copy this kit unchanged to `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-12_B1539_SEAT-R222_hpsmpoc-messaging-held-tickets.md` (`cmp`, sha256); REFUSE 1 to 3; create `.tools/b1539/` (`_quarantine/ logs/ facts/ scratch/ base/ texts/ dry/ records/`). `dotnet run: none`. Absolute JIRA DONE, RECORDS COMMITTED and HARD STOP clocks from `date -v+..M`. STATUS first line `RECORDS B1539: PENDING | JIRA pending`, rewritten after each step.
**Step 1. Helpers** with `--selftest` (a key outside the search-named keys, a second write for a ticket, a create AND a comment for one ticket, ANY transition, a PUT, a DELETE, a label write on an existing key, a field outside the create list, a priority, a parent, a link, a summary of 256 characters, a label outside the list, a banned word, `entry C-9999`, `C-347`, `.NET`, `_by_Kam_`, a prose `HP`, an existing marker, a body one character off its frozen sha256, a comment on a Done key, a comment with two search hits, the 10th write, a lost key and a changed comment each make them refuse or report).
**Step 2. Facts and PRIOR WORK.** Records main `CLARIFICATIONS.md` raw: highest heading (control `^### C-263 ` once at line start); `<CE>` = highest + 1 (expected 366); a heading of yours taken, `refs/heads/records/b1539` present, or an open analysis pull request touching the file is a STOP. Code main (`c717ba1a...` or a descendant; if later, name it). Jira: issue count and highest key (`snap_before.json`: every key's status, comment count, summary/description hash). **The map and the source:** `wc -l` and sha256 prefixes of the three files; re-run the class count (`awk -F'|'` over the map's table rows: A 22, B 13, C 13, D 11, total 59) and **count the map's HOLD rows by program (the C rows 13 and the D rows K2, K3: 15) and print them against the 16 items of the table** (a map that has changed since the drafting: name every difference in STATUS; a row added to the HOLD set has no ticket, say so). **Every quoted fragment of the nine bodies is re-checked as a substring of the map, the source document or the phase decision document** (program; controls: a one-character mutant fails). **T9:** read the builder's STATUS `## HELD` (and, if it has landed on code main, grep the tag's `title` text): T9 is written only when H6b still reads held/unbuilt and the T9 slot says WRITE; else T9 is `not written (built)` or `not written (slot)` and the entry says so. **T1's one absence claim:** re-run the grep above. PRIOR WORK: `ls Briefs | grep -E 'B1535|B1539'`; the newest C-entries (headings printed); `/usr/bin/grep -c -i -F` over records main for `REC-HELD` (0), `messaging map` (the drafter did not measure it: print it), with controls (`pull request 313` 1 or more; `qqzzxx9` 0); Jira: no `REC-HELD-` marker on any key (0), no key above 470 (a key above 470 is named; it is a stop only if it carries your marker or is the twin of a create: the duplicate rule handles it). A READY without a `## PRIOR WORK` section is returned unread.
**Step 3. Searches and texts by program (dry run):** run the searches of every ticket, print the table, apply the HIT rules; build the nine payloads (the fills by program) and the entry; print them; run the scan (0 problems, controls fire); no `<<` or `@..@` left; the table (ticket, outcome create/comment/not written, key, length of summary, length of body, sha256, marker, labels, scan yes/no). Run the WHOLE write path against a FAKE transport (canned 2xx) and print the request list; the fence tests of Step 1 refused there too. JIRA slot HOLD stops here (`RECORDS DRY RUN ONLY`).
**Step 4. Jira writes** in the order T1, T2, T3, T4, T5, T6, T7, T8, T9, each only when its slot reads WRITE. For each ticket: marker search (0, else skip and name it); re-read the hit key if the outcome is a comment (status and newest comment as at Step 3, else HOLD that ticket); post (HTTP 201, create returns the key; comment returns the id); **read it back** (a create: GET the key, summary, description, labels and type byte-equal to the frozen values, status Backlog, issue count +1; a comment: GET by id, byte-equal; a one-character mutant is unequal). One write per command, logged first; stop at the first non-2xx; never write twice on an error (run the marker search before anything else). Re-read the pane list before the first write (REFUSE 7). After the last: `snap_after.json` and the diff over ALL keys (new keys exactly the created ones; lost none; changed exactly the commented keys; comment +1 on each; status unchanged on all; Done count unchanged at the value read at Step 2; labels on every old key unchanged).
**Step 5. Records** (RECORDS slot): clone `datasecau/HPSM-POC-analysis` shallow into `.tools/b1539/analysis` with the deploy key as the clone's repo-local `core.sshCommand` copied by program from the previous records clone `.tools/b1523/analysis` (the key path is never printed; the fallback is a `cp -R` of the previous clone, then `git fetch origin main`); branch `records/b1539` from `origin/main` (print its sha); the entry with ids, outcomes and keys filled; old lines byte-equal (program: the new file starts with the old file's bytes; `### C-365` once, `### C-367` 0); ONE commit (`git diff --name-only origin/main..HEAD` is exactly `1_Project_Definition/CLARIFICATIONS.md`, added lines only; the closing check); the identity print from BINDING HOLD. Commit message: plain ASCII, no person names, no seat ids, no card ids, no B-numbers; end with your session's attribution line.
**Step 6. Landing** (REC-MERGE slot; `FF` is the commissioned word and means "this seat lands its own records branch by the B1523 route", not a fast-forward): print the kit form and the last three merged analysis pull requests' parents (#198 `75ae17d5`, #197 `25f76852`, #196 `dfff014b`, each 2 parents, read by `gh api -X GET .../commits/<sha>`; MEASURED-BY-DRAFTER only for #198: the sha is records main and its parents are for you to print); disagreement is a STOP. Push your branch only, plain push (no force); open the pull request; checks on its head all completed success through CodeQL (never bypass, never dismiss an alert); merge with `gh pr merge <n> -R datasecau/HPSM-POC-analysis --merge --match-head-commit <your head>`. Read-back after the merge: `C-<CE>` once, old headings once each, the file byte-equal to your scratch copy, open analysis pull requests 0. REC-MERGE `HOLD`: stop at the committed and pushed branch; Tuesday lands it.
**Step 7. STATUS** sections: Questions, BLUF, Step 0, PRIOR WORK (Jira, records), Facts re-measured (the 59 / 15 / 16 counts), Searches (the table), Jira (per ticket: created key or comment id, byte-equal; every marker search), Records, Closing checks, Landing (with the identity print), HELD, NOT TESTED, Hand-off items (**list: the 16 held questions are NOT answered; the builder's text pass and its landing are not recorded here; any ticket not written and why**), Deviations, Corrections.

## CLOCK AND HARD STOP
JIRA DONE by your Step-0 date plus 40 minutes, RECORDS COMMITTED plus 80, HARD STOP plus 110 (the Stamp's Hard stop slot gives the absolute outer limit; whichever is earlier). No Jira write from HARD STOP minus 15. **Cut line:** Jira first (T1 to T9 in order); if the records are not committed by plus 80, commit the entry with the Jira outcomes known and say what was dropped. At the hard stop with work left: the HANDOVER form above.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, one question; each count with a control that fires; items 1 and 2 before `.tools/b1539` is created, items 3 to 8 before the first write)
1. `/usr/bin/grep -c -E '_''_''_''_'` of your Step-0 copy prints 0 on the STAMPED copy (the unstamped copy reads one such line for each Stamp slot and the last line; control: a planted line adds 1); `/usr/bin/grep -o -E '@[A-Z_0-9]+@' <copy> | wc -l` prints 0; the last line begins `READ-WHOLE-BY-TUESDAY: DONE`; the JIRA, T1 to T9, RECORDS and REC-MERGE slots each read one of the words their line offers; RULING-1121 holds one sentence. A slot left at its default: every one -> HOLD.
2. `tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'` is not `Datasec/HPSM-POC-R222` (control `-t %1` differs); `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC`.
3. `gh auth status` fails under the project's `GH_CONFIG_DIR`, or `repos/datasecau/HPSM-POC-analysis/pulls/99999` is not 404 (control: `pulls?state=open` 200); the Jira reader cannot GET `HPSMPOC-1` with 200 or does not refuse `HPSMPOC-99999`; a token printed by any tool: "a value was shown", STOP.
4. Prior Jira state differs from the drafter's reading in a way that matters: a key above 470 that carries a `REC-HELD-` marker, or the board's issue count below 470; a hit key that is now Done or moved (that ticket becomes a create or HOLDS, named in STATUS).
5. An OPEN analysis pull request touches `CLARIFICATIONS.md`; `refs/heads/records/b1539` exists; the heading you would write is taken; the raw read of `CLARIFICATIONS.md` is empty or under 2060302 bytes.
6. A map or source file that no longer matches (`wc -l` of the map not 267, of the source not 302) AND a quoted fragment of a body that is no longer a substring of it: that ticket HOLDS (no write), named in STATUS; a changed count with every fragment intact is named and goes on.
7. **Property: another pane whose own kit WRITES Jira HPSMPOC or the analysis `CLARIFICATIONS.md`** (any `Datasec/HPSM-POC-` pane other than yours; resolve every such pane's kit by its project prefix and the kit file name's `hpsmpoc` word, never by the newest file alone). Re-read before the first Jira write, before the push and before the merge.
8. `df -g /Volumes/Datasec_DEV` under 25 GiB, or you start a listener.

## PARTITION (from both sides)
**OWNED by you (records):** ANALYSIS repository `1_Project_Definition/CLARIFICATIONS.md` (ONE appended entry only, via `records/b1539`); Jira project HPSMPOC: at most nine writes, one per ticket T1 to T9 (a create, or a comment on the one open ticket that already decides the same thing), nothing else.
**NOT yours:**
- **The text pass builder** (the whole code repository, its clone, its branch, its change list, its landing) and every later builder: the 44 rows are not recorded or ticketed here; nothing in a ticket says they are built, merged or deployed.
- **Every earlier records seat:** entries up to C-365 are never edited; comments and descriptions on existing tickets are never edited; the Done tickets are never touched.
- **The phase decision document's items:** never ticketed, commented or touched (a ticket only NAMES the D-item beside its held row); the board's Phase 2 catalogue tickets (HPSMPOC-448 to -460) are never edited and receive no comment unless the T5 rule names one as the single hit.
- You never edit any STATUS file but yours, `BACKLOG.md`, `5_Project_History/history.md`, `JIRA.md`, `2_Project_Files/`, `Deliverables/`, `*_evidence/`, the decision store, UAT, Azure, the review site. (This pass appends nothing to BACKLOG, JIRA.md or history; if the project's own end-of-session rule requires them, say so in STATUS and leave them to Tuesday.)

## HOLDS
No Jira write outside the closed list; no transition; no label or field edit on an existing key; no statement that anything is built, deployed, restored or removed that a record or a GitHub read does not show; **no ruling put in the product owner's mouth beyond the words the stamp slot quotes (his 11:21 words are an instruction to ticket; they answer none of the map's held questions: say "keep held" and the map's default)**; no person's name and no card id in any Jira text or entry (the authority is "the product owner"); no customer name beyond the product names the rules allow; nothing about the text pass's progress. If a post, push or merge fails or reads back unequal: stop that item, fix the root cause, re-verify; never retry blindly. **PRIOR-WORK CHECK (standing line):** see Step 2; a READY without a `## PRIOR WORK` section is returned unread. Shell: no `cd`; absolute single-quoted paths; `python3 -I -B`; `/usr/bin/grep -i` with a positive control for every count; never `echo ====` (use `echo ----`); never name a shell variable `path`.

## STATUS FILE AND LAST LINE
`/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-12_B1539_STATUS.md`. First line `RECORDS B1539: PENDING | JIRA pending`, rewritten after every step. **Last line, exactly one of** (each matched by `tuesday/tools/status_watch.sh`): `RECORDS COMMITTED: records/b1539 @ <sha40> | PR #<n> merged as <sha40> | C-<CE> to C-<CE> | Jira: created: <keys or none>; commented: <keys or none>; moved: none | PRIOR WORK section present` | `RECORDS PUSHED: records/b1539 @ <sha40> | PR not landed (<reason>) | ...` | `RECORDS DRY RUN ONLY: <n> payloads built, nothing posted` | `HANDOVER B1539: next <step> <ticket> | done <steps>` | `STOPPED: NEEDS TUESDAY <one question>`.

## Stamp
Tuesday stamps; leave every slot as it stands.
- STAMP: STAMPED 11:45 AEDT 2026-11-12 by Tuesday s272; this kit read whole by Tuesday s272 (472 lines) and the drafter report's seven questions (all defaults taken: nine tickets; labels as drafted; T9 written only if Step 2 shows H6b still unbuilt; R7, K2, K3 ticketed as held with the phase document's THIS PHASE stated; the loose D-064/D-059 links said plainly; off-site assets and SIEM not ticketed; the entry via a records pull request).
- LAUNCH WINDOW: launch at the first cool load until 13:30.
- BASE (code main, records main, Jira issue count and highest key, analysis open pull requests, `Datasec/HPSM-POC-` panes, as Tuesday reads them): code main c717ba1a945191ffa31f13320c19967a6cf7f15a; records main 75ae17d5b0bf438f5855527626c0a22a51da07c7; analysis open pull requests 0; records/b1539 absent (control records/b1523 present); Jira count and highest key NOT re-read by Tuesday (the drafter's 470 / HPSMPOC-470 at 11:35-11:41 is relayed: re-measure at Step 2); Datasec/HPSM-POC- panes: H161 (B1538, no Jira write) and Datasec/HPSM-H160 (B1535, no Jira write).
- JIRA (exactly `WRITE` or `HOLD`; default HOLD; HOLD runs Steps 0 to 3 and posts nothing): WRITE
- T1 (landing copy and hero block: exactly `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE): WRITE
- T2 (journey rename and Training labels: `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE): WRITE
- T3 (customer report introduction and Next Engagement: `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE): WRITE
- T4 (operating modes and Phase 3 naming: `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE): WRITE
- T5 (packages page: `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE, expected as ONE comment on HPSMPOC-392): WRITE
- T6 (commercial stages and success metrics: `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE): WRITE
- T7 (coach opener and talk track: `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE): WRITE
- T8 (deck sentences, firmware question, deck voice: `WRITE` or `HOLD`; default HOLD; the drafter recommends WRITE): WRITE
- T9 (the Illustrative tag's title attribute, H6b: `WRITE` or `HOLD`; default HOLD; the drafter recommends HOLD until the builder's result shows H6b still unbuilt): WRITE
- RECORDS (exactly `WRITE` or `HOLD`; default HOLD; HOLD drops the branch, the pull request and the entry; the Jira steps stand, then the `entry C-<CE>` citation is not used because the texts above carry none): WRITE
- REC-MERGE (exactly `FF` or `HOLD`; default HOLD; FF = this seat lands its own records branch by the B1523 route): FF
- RULING-1121 (one sentence, as Tuesday read it on the board, the exact words and the clock, no card id; the drafter was relayed: the product owner, 2026-11-12 11:21:32 AEDT, "messaging mapping looks good. deploy based on this and ticket anything left for later"): The product owner, live board 2026-11-12 11:21:32 AEDT (view=tuesday, read by Tuesday through the board rulings tool), verbatim: "messaging mapping looks good. deploy based on this and ticket anything left for later".
- Hard stop (the absolute outer limit AEDT; JIRA DONE 40, RECORDS COMMITTED 80, HARD STOP 110 minutes after your own Step-0 date, whichever is earlier): 15:30 AEDT 2026-11-12 (or your Step-0 date plus 110 minutes, whichever is earlier).
- Panes and live seats at the stamp: %168 Datasec/HPSM-POC-H161 (B1538 minimatch, code repo only), %162 Datasec/HPSM-H160 (B1535 messaging text pass, code repo only), %165 MPS-M131, %159 MPS-M130, %153 MPS-M129, %147 NexusAI-N125; none writes Jira HPSMPOC or the analysis CLARIFICATIONS.md.

READ-WHOLE-BY-TUESDAY: DONE 11:45 AEDT 2026-11-12 by Tuesday s272 (472 lines)
