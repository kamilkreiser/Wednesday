STARTABLE: YES

# B2097 DRAFTER REPORT: OXPd records pass for the landing of PR 52 (first-run row 3) and the heavy-runner gates (kit for seat R326)

Drafter: in-session, read-only, for Tuesday s327. Clock at start `Wed 25 Nov 2026 20:30:18 AEDT`; last measurement `20:44:57`. Both were printed by `date`. The kit has no typed clock in any slot; its MEASURED-BY-DRAFTER clocks are `date` prints.

Files written (nothing else outside scratch):
- kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2097_SEAT-R326_oxpd2-records-pr52.md` (sha256 `d13fb549...`, 90725 bytes, 314 lines)
- its sidecar `.measured` (107 claims, 0 TODO; `stamp_check.py <kit>` rc 0)
- this report
- scratch only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s327/d2097/`

## BLUF
- **What the kit writes:**
  - **ONE C-entry, C-87.** It is a "Tuesday's note", following the precedent of C-64 (line 626), and carries no new word of the product owner's. Its first paragraph records the first-run rows after the landing, which brings C-84's line-1108 sentence "rows 2, 3 and 4 are not built" up to date. Its second paragraph records FOUND 3: the coordinator changed one phrase of the subject, and the landed subject (read at source) carries the corrected phrase.
  - **FOUR new owed items, 141 to 144** (inserted after item 140, 28 lines):
    - 141 is FOUND 1 (the undo-owed key).
    - 142 is FOUND 2 (the 64 KiB bound).
    - 143 is FOUND 4 (the no-break space; it names item 133, the same class).
    - 144 holds the landing facts, Info 5 to 7, the named limits, the route of the later device run for item 103 (plus the gate's three additions), and row 4 serial.
  - **ONE history entry** (9 lines). It includes H-ROWS (the state of rows 1 to 4) and H-138 (item 138 stays open after the two NO GO rounds; the canonical runner is kept; no fix is claimed).
  - **ONE Jira comment on OXPD2-1.** No create: Q6.
- **What the kit does not touch:** no tick, no `Closed in part`, no existing line of BACKLOG.md, and no CLAUDE.md edit.
- **Each FOUND goes to exactly one place:**
  - F1 → item 141; F2 → item 142; F3 → C-87; F4 → item 143.
  - Info F5, F6 and F7 → item 144.
  - Item 103's route → item 144 and J-1.
  - Item 138's two refusals → H-138.
- **No ruling of the product owner bears on this pass. This holds.** `kam_rulings_today.sh` was printed to my session only, filtered, and never saved. It shows no row after 14:30, and the 14:30 row is the wording tap already in C-86. Two older words of his are named by their C-84 lines and are not re-quoted beyond them: line 1088 (row 4's button waits for his word) and line 1078 (the set-up grant for the device run).
- **The squash subject (commission item 1):**
  - The landed first line of 1ccf6d0c holds "refuses a file holding the words PRIVATE KEY" once and "a private key" 0 times.
  - The gate's `squash-subject.txt` holds the reverse.
  - The two subjects are equal after that one swap.
  - C-87, H-LAND and H-OWNER record the change as the coordinator's.
- **Seat R326 is free.** It appears in 0 of the 42 SEAT kits of 11-24 and 11-25; the controls R325 and R324 were each found in 2. At 20:34:18 no pane name held OXPd2 (the panes were `%0 tuesday`, `%491 Datasec/NexusAI-N176` and 4 unnamed) and 0 PRs were open.

## Facts re-measured, with instruments
- **GitHub** (`gh api -X GET`, GH_CONFIG_DIR of the project, account kamilDatasec, from 20:30:44):
  - PR 52: closed and merged, `merged_at` 2026-11-25T08:24:39Z (19:24:39 AEDT), merge commit 1ccf6d0c.
  - Its head is be650e1b on `b2091/row3-ca-store`: 1 commit, 11 files, +1224/-60.
  - The 11 paths are 2 added and 9 modified (the whole list).
  - main is 1ccf6d0c: 1 parent baa32eae, tree 385c1922, which equals be650e1b's tree.
  - `pulls/53` returns 404; `pulls/51` returns 200; 0 PRs are open.
- **The PR run 45575107921** (pull_request, success, attempt 1): every one of its 4 job logs holds `HEAD is now at 7f6d497 Merge be650e1b... into baa32eae...` once. This is a MATCH. The push run 45576025564 logs hold it 0 times (the control).
- **The main push run 45576025564:** success.
  - linux: total 2297 ×2, succeeded 2293, skipped 4, failed 0, GUARD 14.
  - windows: total 2297 ×2, succeeded 2276, skipped 21, GUARD 15.
  - rules: RULES 677, Ran 117, FLOOR 117/117.
  - secret-scan: no leaks found ×3.
  - `failed Datasec.` appears 0 times and `total: 9999` 0 times in every log.
  - Check-runs: 7 of 7 success.
  - Code scanning at 1ccf6d0c: csharp, python and actions each have 0 results. Open alerts: 0.
- **The tarball of 1ccf6d0c** (1754754 bytes, 677 files): `facts.py` found `POINTERS 12 of 12`, and its one-line-off control FIRED.
- **The project files:** every file equals B2087's READY.manifest by sha256: CLARIFICATIONS 63e4e89c, BACKLOG f829020b, history d4540a80, CLAUDE 0f1fccc0, register, HP draft, deviation register, 02 and 03.
  - B2087 READY: `bb1c284c... | C-86 | jira created OXPD2-63, comments 41490 41491`.
  - B2091 READY: `be650e1b...`.
  - No `.tools/b2097` folder exists, and no B2097 file exists in Briefs.
- **Jira** (GET only, through the project reader `b1785.py` as a cat copy with `cmp` equal; the fence refused POST, PUT, DELETE and PATCH):
  - Census: 63 issues (OXPD2-63 is new since B2087).
  - Done: OXPD2-33, 39, 41 and 47.
  - The kamil-action label is on 56 to 61 and 63.
  - OXPD2-1 has 13 comments, the newest 41491.
  - These phrases are each in 0 issues: undo-owed, AgentId, agent-id, FileInfo, ReadAllBytes, IsNullOrWhiteSpace, ExportCertificatesResult, ImportCaCertificate, RemoveCaCertificate, ExportCertificates, keyCertSign, CA store, ImportCertificate, development root, pull request 52, heavy.py, "Records pass after pull request 52".
  - Controls: MASTER finds OXPD2-1, "chase HP" finds OXPD2-56, and "home screen" finds OXPD2-62.
- **The runner gates:**
  - B2090: line 1 reads `GATE B2090: NO GO @ 70933ea1b513a637`, and F1 is MAJOR (a signal to the group orphans the job, and Ctrl-C releases the lock).
  - B2092: line 1 reads `GATE B2092: NO GO @ c0c00bb9f88b70c8`, and it says "This is NO GO 2 of 2" on the class "a signal to the runner releases the lock while the job runs" (F1: a second signal during end_group).
  - B2091's stamp S8 keeps the canonical runner 31adedc8.
- **The dry build** (`dry.py`):
  - CLARIFICATIONS goes from 1186 to 1196 line feeds, with C-87 at line 1188.
  - BACKLOG goes from 1044 to 1072 (+28). Items 141 to 144 start at lines 1028, 1035, 1042 and 1049; the anchor moves to 1057. There are 99 open and 45 ticked items. `Closed: ticked in place` stays at 42 and `Closed in part` at 19. The proof by position is equal.
  - history goes from 358 to 368, and B2087's heading moves to line 13.
  - `scan_record` found 0 problems on 42 lines, with 0 bytes above 126. J-1's `scan_jira` codes are empty.
  - The six scanner controls fired.

## D-decisions (the drafter's)
- D1: the form is B2072 (a records pass for a landed build PR) combined with B2087's one append and one comment shapes.
- D2: C-87 is written as a Tuesday's note (the C-64 precedent), because the commission asks for one C-entry and no new word of his exists. The alternative is Q1.
- D3: the J-1 prefix is "Records pass after pull request 52", so the SKIP RULE cannot mistake comment 41485 ("Records pass, 2026-11-25") for a near-duplicate.
- D4: J-1 is written with no name and no double quotes, so its `scan_jira` codes are the empty set.
- D5: the write order is CLAR, BACKLOG, Jira, history (history names all three).

## Chain inputs (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Source |
|---|---|---|
| 0 | kit, sidecar, project files, df, python3 | BASE |
| 1 | `b1785.py` copy, scratch copies | Step 0 |
| 2 | SOURCES files, GitHub, tarball, Jira GETs, B2087/B2091 STATUS | BASE (origin) |
| 3 | frozen texts, C-number (P-7), BL-OLD8 (the before-copy), BL-NEW8 (the dry BACKLOG) | Steps 0 and 2 |
| 4a | live CLARIFICATIONS, C-87 filled | Step 3 |
| 4b | live BACKLOG, BL-141 to BL-144 | Step 3 |
| 4c | J-1 filled (C-87 from Step 2) | Step 3 |
| 4d | live history, BL-OLD8 and BL-NEW8 (4b), CMT-1 (4c), C-87 | 4b, 4c |

## Q-questions for Tuesday (defaults as written in the kit)
- Q1: C-87 as a Tuesday's note. Default: yes. Alternative: no C-entry (B2072's form).
- Q2: FOUND 3 goes to C-87 only, with no owed item. Default: yes.
- Q3: FOUND 4 becomes its own item 143, which names item 133. Default: yes. Alternative: a sub-line under item 133.
- Q4: no line under item 103; its route goes in item 144 and J-1. Default: yes.
- Q5: item 138 is recorded open in H-138 and item 144, with no sub-line under 138. Default: yes.
- Q6: Jira gets one comment on OXPD2-1 and no new ticket. Default: yes.
- Q7: CLAUDE.md line 62 is not edited; it describes the 2026-11-24 run. Default: yes.
- Q8: items 141 and 142 are filed as the gate proposed, in the 7-line form. Default: yes.

## UNMEASURED
- The seat's helper and selftest, HOLD R and R2 on the live files, and the one live POST.
- Whether a third runner round exists: I found none commissioned in the files I read, and did not search further.
- The hosted check names beyond the 7 check-runs (the landing form's 8th name "CodeQL" is not among the check-runs of 1ccf6d0c; I did not read the commit statuses).

## Outside the fences (disclosure)
- One Bash call was refused by the no-`cd` hook. It did nothing.
- Searching the coordinator's own tree:
  - `find -maxdepth 5` over `/Volumes/Datasec_DEV/TUESDAY`, for file names only, to locate `kam_rulings_today.sh` and `kam_msgs.sh`.
  - `find -type f` over my own extracted tarball in scratch.
  - Neither touched the project folder or Source_Documents.
- `kam_rulings_today.sh` ran twice, each piped through `awk` filters into my session. Nothing was saved to a file, no message text was printed except the one 14:30 OXPd decision line, and `kam_msgs.sh` was not run.
- The tarball of the code repo (which may hold test-only synthetic key code) is extracted under scratch `tar/x/`, as B2072's drafter did.
- No write to the project, Jira, GitHub or the card store. No `decision_queue.sh`. Nothing was deleted. Nothing went to any human or device.
