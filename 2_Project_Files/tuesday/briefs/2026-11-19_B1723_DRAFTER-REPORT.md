STARTABLE: YES - the kit is complete (174 lines, ASCII, 11 four-underscore lines = 10 Stamp slots plus the last line, 0 `@TOKEN@`), stamp_check.py exits 0 (109 claims, 109 measured); the one live dependency (the hosted infra job of the squash) is a seat-time gate with a stated poll and HOLD, and it read success at drafting.

# Drafter report B1723 | SEAT-R275 | HPSM-POC records for pull request 336 (HPSMPOC-510)
Drafted 2026-11-19, `date` printed 00:00:20 at the first read and 00:11:08 at the last. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1723_SEAT-R275_hpsmpoc-records-336.md` (+ sidecar `.measured`). Rules (`DRAFTER_RULES.md`), B1712, B1713, both STATUS files and C-391/C-392 read whole or by grep; the records file was read only as a raw copy in the scratch folder, never whole.

## BLUF
- Records kit, form of B1713: ONE comment (W2) and ONE move (M1) on HPSMPOC-510 plus ONE entry C-393; at most 2 Jira writes, no create; records branch `records/b1723`, merge-commit landing by the seat (REC-MERGE FF) as B1713 did. Item names W2 and M1 are KEPT from B1713 so the copied fences stay valid (no W1 exists; D-3).
- The comment is three paragraphs in BLUF / Recommendation / Detail form (JIRA.md line 16), frozen with sha256 prefixes fcb6d9ece9da45e5, be440d165610e54c, c1e0ac2392cce5d1 (745, 319, 1908 bytes). B1713's `scan1713.text_problems` printed `[]` on each.
- Authority is written exactly as asked: "approved for this change by the Datasec fleet's coordinating agent", "not a ruling of the product owner"; and a new line states that no independent review of #336 exists (RELAYED by the stamp).
- No root append (B1712's list is CLARIFICATIONS.md only; B1712 and B1713 both made none).

## Facts re-measured (instrument -> result)
- `gh api -X GET pulls/336` -> merged, base main, merged_at 2026-11-18T12:58:48Z = 23:58:48 AEDT (date -r control), head aa7cfd78, 2 files +7 -3. Commit d8a1de6d26865c355cc9ca4772acbeb54fa521a0: one parent deef2d76; files deploy-package.py +5 -2, test file +2 -1. `compare d8a1de6d...main` identical 0/0; open code PRs 0.
- Blob shas (gh contents, deef2d76 / d8a1de6d / aa7cfd78): README 77aa3ea7 x3; script cb540f1c / 089c877e / 089c877e; test file 70d80f09 / 81a8e4fd / 81a8e4fd.
- My own AST program (docstrings blanked) on raw files at both shas -> script True, test file True; control `same += 2` -> False. difflib: script changed lines 536-540 only, test file 460-461 only.
- Head check-runs: 23, 23 success. Push run of the squash 44309089652 (`ci`) in_progress at 00:01 and 00:11; job `infra (Bicep validate)` completed success, step validate success; e2e, API and both SQL Server shards still running at 00:11.
- Builder STATUS (84 lines, sha256 prefix ea51927951eaf71f): `lost 0, added 0, changed 0`, 332 tests, rc 0, DOCDIFF OK each present. Commit message reads "approved by the coordinator" only after joining the line break with a space (the raw text breaks after "by the"); the kit says so.
- Jira (REST GET): HPSMPOC-510 Backlog/Task/Low, labels docs, follow-up, rec-2026-11-18, 0 comments, transitions 11/21/31/41 Done; HPSMPOC-509 Done/Done; HPSMPOC-511 404; 510 keys listed. Markers: REC-LND10-19NOV-W1 and -W2 0; REC-LND9-18NOV-W1 -> 510 only; -W2 -> 509 only; controls qqzzxx9 [] and REC-LND8-18NOV-W1 -> 509.
- Records main 2ea19503 (PR 214), 6567 lines, 2227249 bytes; `### C-392` at 6561, `### C-393` 0; `records/b1723` ref 0 (control b1713 1); open analysis PRs 0; last three merges are merge commits (parents measured). Branches of PRs 334/335/336 all still on origin (control b1639 2). Dependabot open: alert 12 only.
- JIRA.md (17 lines): no move rule, only line 16 BLUF form; the Done rule is C-263 line 5114 (quoted in the kit).
- Panes: no HPSM pane; no listener opened by me; names R275/B1723 appear in no briefs file.

## D-decisions
- D-1: the comment says the done-when is MET and the move follows only on a re-printed check; no NOT-MET variant (as B1713).
- D-2: no UAT-version sentence in the comment (I cannot read UAT); it says only "not deployed: on main only".
- D-3: marker `REC-LND10-19NOV-W2` with item names W2/M1 kept, so the helper edits are few.
- D-4: the "no other change" claim is proved by the AST block shipped in the kit plus a changed-lines-inside-span test; the word "comment" in P3 is covered by the span test (AST ignores comments).
- D-5: the entry cites entry C-263, C-391, C-392 (C-391 filed HPSMPOC-510; C-392 closed 509).
- D-6: branch names are not written in the entry (they trip the B-number ban); "three branches still on origin" is a note, nothing deleted.

## Q-questions for Tuesday (each with a default)
- Q-1: the squash's hosted run is still in progress (SQL Server shards, e2e); only the infra job is a condition (as B1712/B1713). Default: yes, infra job only; the rest is recorded as read. If you want the whole run green first, stamp later.
- Q-2: P3 relays "the builder's record reads 332 tests ... lost 0, added 0, changed 0" without re-running the suite. Default: RELAYED, stated as such.
- Q-3: marker series LND10-19NOV (the date is 19 Nov at drafting). Default: keep.
- Q-4: record the three leftover branches as a note only. Default: yes, delete nothing.

## UNMEASURED
- UAT/deploy state (no host reads, so no UAT sentence); the infra suite re-run (RELAYED); the other jobs of the squash run; Jira issue count by `search` was 510 listed keys, not a separate count; the seat's helper edits are untested by me (counts listed are line counts by grep -c -F at drafting).

## Outside-the-fences disclosure
Read-only reads only: `gh api -X GET` under the project GH_CONFIG_DIR (HPSM-POC and HPSM-POC-analysis, contents/commits/runs/refs), Jira GETs through a scratch reader that loads the project `.env` in-process (no value printed), the project's B1713 helper sources and STATUS files, the B1708 verdict, `tmux list-panes`, `lsof` (count only), `date`, `df`. Scratch under `fleet/state/s291/d1723/` (raw file copies, scripts, `measure.py`). Wrote the kit, its `.measured` sidecar, this report, and a `.measured` backup of the first sidecar pass (in scratch). No decision card read, no Jira write, no push, no mail.
