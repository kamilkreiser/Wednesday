STARTABLE: YES

# B2022 DRAFTER REPORT (seat Datasec/OXPd2-R309, records): the records of pull requests 43 and 44, eight new owed items, no tick, one C-entry (slot)

**Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2022_SEAT-R309_oxpd2-r-records-wave4.md`
- 102057 bytes, 431 line feeds, 0 bytes above 126, 9 `____` lines (eight slots and the last line).
- 22 frozen texts, 33 SOURCES rows (every row hashed at the build), 47 REVIEW MAP rows (0 failures), 26 code facts at `b0b26b60` (0 failures).
- Sidecar `.measured` beside it: `stamp_check.py <kit>` exits 0, 162 claims, 162 measured.

**Scratch:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s320/b2022/` (`gets.py`, `logs.py`, `blobs.py`, `facts.py`, `jira_search.py`, `proto.py`, `build_kit.py`, `sidecar.py`, `texts.md`, `kit_template.md`, `dry/`, `get/`, `jira/`, the extracts and prints).
**Drafted:** 08:17:45 to 08:32:46 AEDT, Tue 2026-11-24, by `date`.

## BLUF
- **Form:** B2010's (seat R308), self-contained. Records only; written in place by HOLD R (the project folder is not a git repo); order CLARIFICATIONS (if C-ENTRY WRITE), BACKLOG, history.
- **Landings (GET 08:18:39-08:18:54):** main `b0b26b60`; 44 PRs, 0 open, `pulls/45` 404. PR 43 head d3d10b71 -> c5b103ee (parent e39396f9, tree ab8093c6, 14 files); PR 44 head 67c24d18 -> b0b26b60 (parent c5b103ee, tree b2a09571, 6 files). Gate heads equal (d3d10b7, 67c24d1). PR 44's tree = the B2016 reader's measured merge tree.
- **Main runs:** 45185901474 (c5b103ee) 2054/0, skipped 4/21, RULES 656; 45187062667 (b0b26b60) 2093/0, 2089 and 2072 succeeded, RULES 657; 111 unit tests at floor 111 each; csharp 0 at both merges; 0 open alerts. Controls: `total: 2094` 0 lines in all six logs; `failed Datasec.` 0 in the four test logs, the C7 log 1 stripped / 0 raw.
- **Eight new owed items (98-105 PREDICTED):** W2EMPTY (B2016 FOUND 1, Major), W2SHAPE (FOUND 2), W2XMLCHAR (FOUND 3), W2UNDOARGS (FOUND 4), each "in round 2 of lane W2, the coordinator's lane B2021"; HOLD (the 00:33 coordinator hold, lift condition exactly FOUND 1 + FOUND 2, FOUND 3/4 named as not lift conditions, ticked by the pass that records the lift); SELFSIGNED (HP `certificatemanagement.wsdl:135`, step 3, open); REST43 (B2017 FOUND 1-6, kit B2014 FOR RECORDS incl. Test binding 17 live of 19, the three READ-first rules, R32/legal/beta reported); REST44 (B2016 FOUND 5-9, kit B2011 FOR RECORDS, the reader's MEASURED G1 answers).
- **No tick:** 93, 94, 95, 96 each stay open by their own words (table in the kit); P-4 proves them byte-identical after the write.
- **One C-entry, behind slot C-ENTRY (default WRITE):** C-79 PREDICTED = his 08:12 Tuesday-terminal words, verbatim (406 chars, byte-equal in the pickup log line 62 and the B2018 commission line 6), in the C-31 / C-56 terminal form. **The commission said none expected; this is the one deviation** (Q2).
- **Prototype (dry/, from live bytes, all three record files unchanged during the run):** CLARIFICATIONS 830 -> 838 (+8, prefix), BACKLOG 722 -> 778 (+56, 0 changed, old file back by position, owed 1-105 no gap, ticked 30 -> 30), history 262 -> 274 (+12, 0 changed); SKIP variant built too. Project `scan_record` 0 problems over 76 lines; controls fire.

## FACTS RE-MEASURED (instruments in scratch)
- Record files: sha256 of CLARIFICATIONS `cdfb76f2...`, BACKLOG `9bf84169...`, history `c44b041d...`, register `e2621f1b...` each = `.tools/b2010/READY.manifest`; CLAUDE.md `1a2e5629...` (= B2010's row 1). R308 STATUS last line `READY B2010: 103fec2d... | C-77 C-78`. No `.tools/b2022`.
- BACKLOG: 97 owed lines 1-97, 30 ticked; anchor intact (item 97's Discovered line before the empty line). CLARIFICATIONS: C-1 to C-78; `S-CARD` 80 old lines.
- Code facts at b0b26b60 (GET raw copies): every verdict line pointer of B2016 FOUND 1-4/6/9 and B2017 FOUND 2-4 re-found by program (LabFiles.cs 129/169/173/245; Oxpd1Command.cs 473/654-657/748; Lab Oxpd1 README 62-65/72/79/86-92/117; contracts README 21-23/27/33-34/43-44; ContractTests.cs 66/150-153; StubDevice.cs 180). `UndoLine` holds `--soap-port` and `--pin`, none of `--addressing`, `--password-name`, `--timeout-seconds`.
- **Drafter's own finding (filed in REST44 as "this pass's read"):** `src/Datasec.Suite.Adapters.Oxpd1/README.md:80-81` still says nothing lists what a session left registered and "the end-of-session undo list is a later lab command": stale since PR 44.
- Jira OXPD2 (GET only, b1785.py loaded in place, write logger refused): census 25, controls 200/404. 0 issues for every new subject; `hold` 4 (verb sense, contexts read), `development CA` 2 (the release guard's deny-list).
- Rulings reader (marker in my scratch): 0 Kam rows on 2026-11-24; none after 22:07:29 on 11-23; TAPPED-BUT-OPEN none.

## D-DECISIONS (the drafter's)
- **D1: C-entry proposed** despite "none expected": CLAUDE.md line 12; `different account` / `drive the meeting` 0 lines in CLARIFICATIONS (controls C-31, C-56); terminal precedent C-31 and C-56 msgs 8/9. Made switchable (slot C-ENTRY, -NOC history variants) so Tuesday can SKIP without a redraft.
- **D2: no tick.** The commission asks for none; THE NO-TICK READING names why 93-96 stay open.
- **D3: the hold is a BACKLOG item** (owed list, tickable on lift) plus a history line, written as the coordinator's; its text quotes no ledger, cites "the coordinator's own record of its holds".
- **D4: FOUND 1-4 one item each; Infos grouped per PR** (REST43, REST44) rather than one REST for both (B2010 used one; two read better here).
- **D5: B-number `B2021` stands in four BACKLOG lines** as the commission asks; `scan_record` has no B-number rule (the Jira scanner does; no Jira write here).
- **D6: the HP folder name holds `www.`**, which fires `S-URL`; texts name the file and say "the folder whose name ends ..." instead.
- **D7: facts pinned to b0b26b60**; a PR 45 (W2 round 2) landing first is not a stop.
- **D8: the morning-plan card (ruled a 08:13:40, Datasec/Fleet) is not entered:** its delivered artefact names his terminal message, so it is the coordinator's entry, not his tap (Q3).

## Q-QUESTIONS FOR TUESDAY (each with a default; the Stamp's Q-ANSWERS slot lists Q1 to Q8)
- Q1 no Jira ticket (default). Q2 C-ENTRY WRITE (default) or SKIP. Q3 morning-plan card not entered (default). Q4 nothing ticked (default). Q5 the grouping as frozen. Q6 the hold's lift condition FOUND 1 + 2 only. Q7 C-CONTINUE's reading "Use fable to review" = C-56's flag for reviews only, written as the coordinator's. Q8 pinned to b0b26b60.

## CHAIN INPUTS
| Step | Inputs | Where from |
|---|---|---|
| 0 | the kit, sidecar, scanner `b1785.py`, record files | BASE |
| 1 | `.tools/b2010/b2010.py` (model, read only), scratch copies | BASE; Step 0 |
| 2 | SOURCES files, the origin, live record files, the pickup log (search only) | BASE / GET |
| 3 | frozen texts, live numbers (Step 2), scanner copy (Step 0) | Steps 0-2 |
| 4 | dry builds (Step 3), before-copies (Step 0), re-read origin | Steps 0, 3 |
| 5 | proofs | Step 4 |

## UNMEASURED / NEVER RUN
- The seat's `b2022.py` and selftest, HOLD R / R2 on live files, numbers at the seat's run, write order and partial-write stop, the SKIP variant on live files, REFUSE 2/5 pane checks (panes at drafting: `%0 tuesday` and two unnamed; no OXPd pane).
- Whether W2 round 2 (B2021) lands first; every device answer; every Linux/Windows behaviour the items relay.

## OUTSIDE THE FENCES (disclosure)
- **Read whole:** the commission; the B2010-B2012 and B2005-B2006 commissions; DRAFTER_RULES; the B2010 kit (Read tool, one call) and report; B2016 and B2017 VERDICT and FOR-RECORDS. **In parts:** kits B2011 and B2014 (FOR RECORDS, FOR TUESDAY, Questions, NOT DECIDED, Stamp; B2014 line 31); B2010 STATUS last ~70 lines; NEXT-PICKUP-TUESDAY.md lines 62-82 (DELTA 1386-1389, for the hold and the 08:12 words); CLARIFICATIONS ranges (1-4, 182-192, 382-420 cut, 796-830 cut). **Not read:** the B1944-B1946 commission the B2005-B2006 FORM points at; the B2003 kit.
- **A read I should flag:** `0_Brain/daily/2026-11-24.md` in the TUESDAY tree, grepped for the hold; its matching lines were mostly another client's fleet work (Secuura seats). Nothing from it is used in the kit.
- **Card read:** `decision_queue.sh show datasec-morning-plan-1124` (exact Datasec id) into scratch, filtered.
- **Writes:** only the kit, its sidecar, this report, and scratch. Nothing to the project, GitHub or Jira.
- **Hook refusals (none retried by another route):** `pretooluse_no_cd.sh` refused a `cd` (re-issued with absolute paths); `pretooluse_zsh_wordsplit.sh` refused an `=====` separator (re-issued with `----`); `pretooluse_recursive_scope.sh` refused a `grep -r` over the daily folder, briefs and s320 (re-issued as `grep -l` on named files); pathguard refused `cp -n` of the project scanner into my scratch (it read the source path as a write target): the scanner was loaded in place by `importlib` instead, as B2010's drafter did. The SEAT's own `cp -n` into `.tools/b2022/` is the kit's step and was never run by me.
