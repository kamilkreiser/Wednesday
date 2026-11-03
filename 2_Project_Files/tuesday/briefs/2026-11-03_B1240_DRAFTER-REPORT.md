STARTABLE: YES

# B1240 drafter report (kit SEAT-R163, HPSM-POC records seat after UAT deploy B1234 and PR #280)

Drafted 2026-11-03, reads 22:03 to 22:12 AEDT (every clock below from `date`). Kit: `2_Project_Files/tuesday/briefs/2026-11-03_B1240_SEAT-R163_hpsmpoc-records-uat-deploy-69338b64-and-442.md` (85 lines, 12 stamp slots including the last line; `grep -c -E '_''_''_''_'` 12). Model row C8 (`model-routing.md:98`), no gate (G3 `:110`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes.

## BLUF
- Startable now. G325 (focus-ring gate) is live and the two seats do not collide in either direction: G325's REFUSE and STOP lines do not fire on a new pane named `Datasec/HPSM-POC-R163`, and this kit's pane REFUSE (7) is written as a test of what another pane's kit WRITES, so it prints OK for G325 and for its own pane.
- Two C-entries are owed, not one: **C-288** (PR #280 landed; no entry exists) and **C-289** (the UAT deploy). Records main is `468bcd7b` (B1216's landing), so C-287 is the highest and C-288 / C-289 are free.
- **HPSMPOC-442 may move to Done under the Done rule C-263** (`CLARIFICATIONS.md:5114`: "Done means merged to main (each ticket's done-when checked first; nothing deploys)"). The deploy is not required. Five done-when clauses are MET by gate B1227 `:115`, the words clause is MET-ON-A-READING, and "merged to main" was NOT MET at the gate and is MET now (PR 280 merged 20:19:03 AEDT). Default Q-1: MOVE on the coordinator's reading, the C-286 form, with a COMMENT-ONLY alternative text.
- Relay, not re-test: no HTTP to UAT or the demo was made; every deploy fact is RELAYED from the B1234 STATUS (349 lines).

## Two answers asked for
1. **Would launching this seat now make G325 stop? NO.** G325's kit (`B1228` kit `:40`) refuses at Step 0 on: a four-underscore run, pane not G325, `Datasec/HPSM-POC-H111` listed, head moved, builder STATUS, `.tools/b1228` pre-existing, "a listener, pane or kit on 9110-9119", a PR for the branch, `df`, model. Tested by program against the live names with `Datasec/HPSM-POC-R163` added: H111 count 0 (control: planted H111 gives 1), G325's own name 1. R163 uses no port (lsof 9110-9119 reads 5, all G325's; none assigned to R163). G325's branch re-scan stops only for a branch naming its 10 web paths with an open PR or live pane; R163's branch `records/b1240` is in the records repository and names none of them. G325's `.tools/.git-lock` use is fetch-only; R163 takes it only for ref writes through `lock.sh` (waits, no stop). G325's REFUSE items run at Step 0 only, and it says "Main moving is no REFUSE".
2. **Would this kit's own same-project REFUSE fire on G325 or on its own pane? NO.** B1188's REFUSE 7 ("any `Datasec/HPSM-POC-*` pane other than your own", `B1188 kit :28`) is the wording that stopped a seat; B1216's REFUSE 6 was a write-set test. This kit's REFUSE 7 is a property (a pane whose kit WRITES a path of the partition) plus an exact procedure: skip own name, take the id after the last hyphen, find the newest non-`.pre-` kit, count `b1240|wt-b1240|records/b1240`; STOP on count above 0 or kit not found. I wrote it as `/Volumes/Laptop-DEV/.../scratchpad/refuse7.sh` and ran it: `Datasec/HPSM-POC-G325` prints OK count 0 (the real G325 kit: `grep -c` 0); own `Datasec/HPSM-POC-R163` skipped; `tuesday` skipped; planted `R164` with a planted kit naming `.tools/b1240` prints STOP (count 1); planted `Z999` with no kit prints STOP kit not found. I avoided the tokens "CLARIFICATIONS.md", "records" and "BACKLOG" in the test, because G325's kit names CLARIFICATIONS.md as a read.
- **Disjointness proof (program `disjoint.py`):** R163 write set (three records files, `Briefs/*B1240*`, `.tools/b1240`, `.tools/wt-b1240`) against G325's (`.tools/b1228`, `.tools/wt-b1228-*`, `.tools/heavy-slot-*`, `Briefs/*B1228*` and its evidence folder): overlaps `[]` (rc 0); control with one planted shared path: 1. Reads: G325 cites `CLARIFICATIONS.md:3617`; an append does not move it, and the kit's `apply1240.py` must assert every old line byte-equal at its old number. One soft overlap, disclosed: C-288 will plausibly contain the words "head-pinned squash", so the count G325 quotes ("99 lines say it") becomes 100 or more. That count is a drafting-time measurement in G325's kit, not a gate (the 5491-line total it also quotes equals records main today and will grow by this seat's append); it is not a stop.
- **Observation for Tuesday about G325, not this seat:** code main moved `f464376b` -> `69338b64` (PR #280, 36 files, merged 20:19:03 AEDT). G325's MAIN-MOVE property regex (kit `:33`) counts 0 over those 36 files (control: a planted `web/src/app/layout.tsx` line gives 1), so it is a Note for G325 ("other web/ paths and api/: name them, re-derive the landing tree"), not a stop. The 36 files are in `scratchpad/files.txt`.

## Facts re-measured (instrument; control)
| fact | instrument | control |
|---|---|---|
| records main `468bcd7b0f6393a8121acb9ec0fa9685c2590f00`, "Merge pull request #175 from datasecau/records/b1216"; open records PRs 0 | `gh api -X GET .../branches/main`, `pulls` length (22:03:56) | `pulls/99999` 404 |
| `records/b1240` ref absent | `git/matching-refs/heads/records/b12` | `records/b1216` listed |
| CLARIFICATIONS raw main 5491 lines; BACKLOG 3355; history 2719; local checkout CLARIFICATIONS 192 lines (STALE, never read) | `gh api ... contents ... raw` into scratch; `wc -l` | `C-287` heading found at `:5479`, C-263 at `:5114` |
| C-288 / C-289 absent; no entry for `#280`, `69338b6`, `B1234`, `41610041882` | `/usr/bin/grep -c -F` and `-E '^### C-(28[5-9]|29[0-9])'` | `#278` 3 lines; headings C-285, C-286, C-287 print; each of #271-#279 has a landing heading (C-264, C-267, C-268, C-275, C-278, C-280, C-281, C-282, C-286) |
| PR 280 merged_at 2026-11-03T09:19:03Z = 20:19:03 AEDT; head `f0000f54...`; merge commit = main `69338b64...`; 36 files, +2209 -69, 2 commits | `gh api -X GET pulls/280` | plus-10 reading would be 19:19:03 (planted, differs); code open PRs 0, `pulls/99999` 404 |
| squash: 1 parent `f464376b`, tree `47af0b97...`, `verification.reason` valid, subject "Feedback: a review category held for an Admin, who approves (sent on) or deletes (text erased) it (#280)" (names no key; PR title does) | `gh api commits/69338b64` | tree equals B1227 `:156` "merged tree 47af0b9" |
| 19 check-runs: 18 success, 1 skipped, 0 other; three `api on SQL Server` jobs success; run 41610041882 ci/push/main/success/attempt 1; open code-scanning alerts 0 | `commits/.../check-runs`, `actions/runs/41610041882`, `code-scanning/alerts` | `state=fixed` returns 1 |
| Jira: HPSMPOC-442 Backlog, 0 comments, labels `b1216-2026-11-03`,`po-feedback`, transition `Done` id 41 offered; the 17 keys of B1234 `:307`: 9 Backlog (442, 431, 428, 420, 417, 412, 409, 405, 322), 8 Done (437, 435, 433, 430, 429, 425, 424, 421); `key = HPSMPOC-443` 0; `text ~ "B1234" OR "B1240"` 0 | `.tools/b1216/{desc1014,read,search}.py`, JQL with parentheses | `key = HPSMPOC-268` 1; `text ~ "qxv9k2zzprobe"` 0 |
| B1234 STATUS 349 lines, sha256 prefix `cd98dc76deb65e7b`; `:1` `DEPLOY B1234: DONE`; `:349` begins `DEPLOYED: UAT @ 69338b64`; FOR TUESDAY `:298`, item 5 `:307`, 6 `:308`, 7 `:309` | `grep -n`, `awk NR`, `sha256sum` | |
| B1221 `:164` NO GO round 1; B1227 `:156` GO WITH FINDINGS round 2 of 2 on class "held review page and erase"; B1227 `:115` grades 442 part by part | `grep -n '^VERDICT:'` | |
| `FeedbackReview.tsx` at `69338b64`: `:24` the 403 sentence template, `:56` the code comment on the review copy's Delete | `gh api contents ?ref=` raw, `grep -n` | the file is 137 lines |
| ruled card, option a "Admin opens the page for now", ruled_ts 2026-11-03T11:18:52+11:00; DETAIL read | `decision_queue.sh show <exact id>` into scratch, read through id/option filter | status `ruled`, choice `a` |
| ports: lsof 9110-9119 = 5 (G325); 9240-9249 = 0; R163 none | `lsof -nP -iTCP:... -sTCP:LISTEN \| wc -l` | |
| model: C8 `model-routing.md:98`, G3 `:110`, `models_latest.json:23`, `brief_seat.sh:24` | `awk NR`, `grep -n` | |

Landing rule for the records repository quoted in the kit: B1168 kit `:3` "landed by you by head-pinned merge commit"; B1216 kit `:48`; evidence B1216 STATUS (`PR #175 merged as 468bcd7b`). Code repository: head-pinned squash (`CLARIFICATIONS.md:3617`, `:5467`). The kit says a squash on a records branch drops the merge commit.

## D-decisions (mine, for Tuesday to overrule)
- D-1 **Two entries** (C-288 landing, C-289 deploy), in event order (merge 20:19, deploy 21:14 to 21:34), instead of one, because the commission says "one per event" and B1234 `:307` owes both.
- D-2 **Done-state source line:** C-263 at `CLARIFICATIONS.md:5114`, quoted in the kit (S5). That entry's text also says a key with an unmet clause is commented and left open, which is the COMMENT-ONLY branch.
- D-3 **The card DETAIL** is quoted with one name replaced by "[the reviewer]" (fence 7 forbids a person's name in kit text); the id is not written; the ruling time is. The detail's "roughly 17 files" is compared with the measured 36.
- D-4 **Comment shape:** `post.py` posts one paragraph only, so the comment is one fixed line with two variants (MOVE, STAY), BLUF first, marker `REC-DONE-442-03NOV-B1240`; numbers C-288 / C-289 are cited, so REFUSE 5 stops if those numbers are taken. It writes none of the stamped words and not the review label.
- D-5 **Move gate inside the seat:** before the transition the seat re-reads the six clauses and does not move if any clause other than the words clause reads NOT MET (belt and braces over the Stamp's MOVE).
- D-6 **Hard stop** 45 / 75 / 120 minutes (shorter than B1216: no cookie job, one Jira comment), and not after 23:59.
- D-7 **The 17-key DONE-MOVES list** inside B1234 `:307` is NOT executed here (the commission names only 442). C-289 lists the 17 keys with their Jira status.
- D-8 **Records branch** `records/b1240`, three files (CLARIFICATIONS, BACKLOG, history); landing by head-pinned merge commit by the seat (slot LAND default SEAT).

## Q-questions for Tuesday (each with a default; all are Stamp slots or answered there)
- Q-1 Does HPSMPOC-442 move? Default **MOVE** (coordinator's reading, open to the product owner's veto; C-286 precedent). The words clause is the reason it is not a plain MET: B1227 `:115`, `:117`, `:130` (24 of 24 stamped strings match; one reused on-screen sentence; two API-only texts unstamped and never shown). COMMENT-ONLY if you read that as unmet.
- Q-2 Approve the comment text byte for byte. Default APPROVED for the variant the Stamp selects.
- Q-3 FOR TUESDAY 6 (a) and (b) (and (c)) are candidates, not judged: default **ROWS-ONLY** (BACKLOG rows B1240-1 to -3, no new ticket); a ticket needs its own kit with fixed text. Item 7's two (webhook references; HPSMPOC-428's wake) also become rows B1240-4 and -5, as a pointer to an existing open row where BACKLOG already has one (the drafter saw `SecretNotFound` in 6 BACKLOG lines).
- Q-4 The 17-key DONE-MOVES step: default none in this kit.
- Q-5 B1234's words table (17 strings not reached) and the one test item left on UAT: default recorded in C-289 only.
- Q-6 RECORDS default WRITE. Q-7 LAND default SEAT.

## UNMEASURED
- Everything hosted: UAT and demo (no HTTP by rule); every deploy fact in C-289 is RELAYED from B1234 with its line.
- That `post.py` and `move1188.py` (re-pointed to `move1240.py`) work for this ticket; the helper edits are the seat's and are not run.
- The comment's phrases against each cited file (times and counts were checked by the drafter, not each phrase). The kit makes a mismatch a Correction that holds the comment.
- Whether the wording "MET" for part 3 (delete) is acceptable when UAT refuses Delete by design (the done-when is merge-based; the gate proved erasure 4 of 4 in code, B1227 `:79`).
- Whether another seat is launched between this draft and the stamp (REFUSE 7 re-tests at the seat's Step 0).
- Hard-stop clock arithmetic is the seat's, written absolute at its Step 0.

## Outside-the-fences disclosure
- No fence broken. I never ran `decision_queue.sh list`; one `show <exact id>` into a scratch file. No `fleet/briefs_staged/`, scoreboard, `_ledger.md`, WEDNESDAY / FRIDAY tree or non-Datasec project read. No HTTP to any hosted host; no az/ssh/docker. Git: none run in the project repo; GitHub only by `gh api -X GET` under the HPSM-POC `GH_CONFIG_DIR`. No `cd`. Jira: reads only through `.tools/b1216/` helpers (`desc1014.py`, `read.py`, `search.py`; each JQL `project = HPSMPOC AND ( ... )`), no token printed.
- Writes: the two files above, plus scratch (session scratchpad: `CLARIFICATIONS.md`, `BACKLOG.md`, `history.md`, `card.txt`, `files.txt`, `fr.tsx`, `disjoint.py`, `refuse7.sh`, `names.txt`, `kits/`). One command (`sed -i` plus `rm -f`) was REFUSED by a hook before running, so nothing was deleted; the kit was edited with the Edit tool instead.
- Reads outside my two files that go beyond the named inputs: the project Jira helper scripts' first lines (`.tools/b1216`, `.tools/b1188` `post.py`, `move1188.py` headers), the G325 kit lines 33-49, the B1216 and B1168 kit lines for the landing rule, `tmux list-panes -a` (read), `lsof` (read).
- One slip: the first draft of the kit quoted a card option label containing a person's first name; it was caught by my own grep and replaced before the report. The B1216 kit's file name (which contains a first name) is cited as a path in the kit with a note, as B1216 did. The kit contains one non-ASCII character (a long dash inside a quoted history heading) outside the Jira comment lines; both comment variants are ASCII, one line, no tab or backtick, marker once at the end (checked by program).
- The Stamp slots are all four underscores; no clock is typed in any slot.
