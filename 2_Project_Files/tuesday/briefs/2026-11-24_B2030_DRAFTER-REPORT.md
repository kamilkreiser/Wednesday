STARTABLE: YES

# B2030 DRAFTER REPORT (seat Datasec/OXPd2-R310, records and Jira): PR 45 records, five ticks, seven new owed items, C-80 and C-81, 29 Jira creates for the Workpath product owner

**Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2030_SEAT-R310_oxpd2-r-records-and-jira.md`
- 147632 bytes, 1174 line feeds, 10 `____` lines (nine slots and the last line). 18 bytes above 126, all inside frozen texts the seat copies verbatim (his curly apostrophe in C-80, the em dash in his board words in T-27 to T-29 and in the kit's rule that names it).
- 85 frozen texts, all re-parsed from the written kit equal to the built ones; the frozen table matches 85 of 85; a one-character mutant differs. 32 SOURCES rows, every row hashed. 18 REVIEW MAP rows with 0 failures. 11 code facts at `e2a20aef` with 0 failures.
- Sidecar `.measured` beside the kit: `stamp_check.py <kit>` exits 0, with 142 claims and 142 measured.

**Scratch:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s320/b2030/`. It holds `parse_drafts.py`, `jira_get.py`, `jira_probes.py`, `jira_texts.py`, `gen_c.py`, `maps.py`, `proto.py`, `build_kit.py`, `sidecar.py`, `texts.md`, `kit_template.md`, `dry/`, `get/`, `cards/`, `rtf/` and the board print.
**Drafted:** from 10:38:52 to about 10:55 AEDT, Tue 2026-11-24, by `date`.

## BLUF
- **Form:** the form of B2022, self-contained, plus one new part. PART 4 is the Jira creates, gated by slot JIRA. Records are written in place by HOLD R. Write order: CLARIFICATIONS, then Jira T-01 to T-29, then BACKLOG, then history. History goes last because it names the keys, which come from the write log only.
- **Landing (GET 10:40:31):** main is `e2a20aef`. There are 45 PRs and 0 are open; `pulls/46` returns 404. PR 45: head 28b25332, one commit, merged as e2a20aef with parent b0b26b60 and tree ec57df8b. That tree equals the one in the B2026 landing.txt. Compare: ahead 1, 5 files. Push run 45284683760 succeeded: linux and windows both 2112 with 0 failed (2108 and 2091 succeeded, 4 and 21 skipped), RULES 657, Ran 111 at floor 111. csharp, python and actions analyses at e2a20aef are all 0, and there are 0 open alerts.
- **Ticks (slot TICKS, default all five):** 98 (B2016 FOUND 1, "CLOSED"), 99 (closed for child elements; the remainder goes to new item NONELEM), 100 (the agent name is closed; the host goes to HOSTCHAR), 101 (closed), and 102 (the hold, lifted by the coordinator; RELAYED from pickup-log DELTA 1391). Each tick changes only `[ ]` to `[x]` and adds a Closed line in the form of the 27 earlier ones.
- **Seven new owed items (106 to 112 PREDICTED):** NONELEM, HOSTCHAR and DIRPERM (B2026 FOUND 1 to 3, Minor); NONASCII, UTF16 and R2CELLS (FOUND 4 to 6, Info, one item each as the commission says); and FIRSTRUN (the three preconditions of the lift, as one item for the first-run commission).
- **C-80** is his answers file whole: 55 lines, quoted line by line in C-58's form. Its quote reverses to answers.txt byte for byte, and answers.txt equals my own `textutil` conversion of his RTF. **C-81** holds his 08:33:59, 08:34:10 and 10:37:19 messages, plus his eight taps in C-78's form (no card id), each with the board's time stamp. The four doubled taps (kd2, kd1, ka4 and ka1 were each sent twice) are noted as such. The coordinator's readings are marked as Tuesday's.
- **Jira:** one POST per ticket to `/rest/api/3/issue`. It carries fields project, issuetype 10030, summary, description (ADF), assignee `626881c70f0cc0006f8ee5c9`, duedate 2026-12-08 and labels `oxpd-workpath-question`, plus `update.issuelinks` add Relates (id 10003) to OXPD2-1. So the link is set from the new issue's side and nothing is written to OXPD2-1.
  - Each create is idempotent: before it, a label search and a phrase search for its summary run. An equal summary means SKIP; a near match means STOP.
  - After each create, every field is read back.
  - The fence refuses every other request; the selftest lists each refusal case.
- **Prototype from live bytes into dry/** (the live files were unchanged during the run):
  - CLARIFICATIONS 838 -> 978 lines (+140), with C-80 and C-81 headings at 840 and 902.
  - BACKLOG 778 -> 832 lines: +54 added (5 Closed lines and 49 item lines), 5 changed, ticked 30 -> 35, owed 1 to 112 with no gap.
  - history 274 -> 287 lines (+13).
  - The project `scan_record` reports 0 problems, apart from S-NAME and S-ASCII on quoted lines, which are allowed and have C-58 as precedent. All controls fire.

## FACTS RE-MEASURED (instruments in scratch)
- **Record files:** CLARIFICATIONS `d1d35576...`, BACKLOG `bfda041f...`, history `18cd1563...` and the register `e2621f1b...` each equal `.tools/b2022/READY.manifest`. CLAUDE.md is `1a2e5629...`. The last line of R309's STATUS is `READY B2022: 24353d93... | C-79`. There is no `.tools/b2030`.
- **Jira (GET only, through b1785's `real_transport` with a GET-only wrapper):**
  - Census: 25 issues, max OXPD2-25.
  - Label `oxpd-workpath-question`: 0 (control: `no-hardware` 23). Assignee search: 0.
  - Steven Molnar is active with account `626881c70f0cc0006f8ee5c9` and is assignable (control: `zzqxnonexist` gives 0 rows).
  - Relates is link type id 10003. The Task createmeta offers assignee, duedate, labels and issuelinks.
  - OXPD2-1 is in Backlog with 0 links.
  - All 29 summary phrase searches return 0 (control: the `MASTER: questions...` phrase finds OXPD2-1). All 14 probe phrases return 0 (control: `CI/CD skeleton` finds 7).
- **Board:** `WED_AGENT=tuesday kam_msgs.sh 40` at 10:39:55 shows 16 rows on 2026-11-24, all view=tuesday. `decision_queue.sh show` for the 8 exact ids shows each card ruled, with the key his tap names.

## D-DECISIONS (the drafter's)
- **D1: two corrections to the Fable-reviewed drafts (Q2).**
  - C1: T-27 to T-29 said "(tap at 10:34)". The board stamps his ka5 tap at **10:32:43**; 10:35:06 is the store's ruling time.
  - C2: T-29's "Why the build needs it:" was **empty**. Pack v3 gives W43's reason as "As the item above.", so I copied T-28's reason in by program.
- **D2: no first comments and no OXPD2-1 index comment (Q3).** The commission says "writes nothing else to Jira".
- **D3: Jira text rule.** The project's `scan_jira` fires S-NAME, S-DQUOTE, S-WORD:tuesday (the weekday of the due date) and S-WORD:lane (T-26), plus S-ASCII (the em dash, T-27 to T-29) on every ticket, by design. The kit pins each ticket's code set: any new code is a STOP. Added checks: no `.env` value appears, and no card id, URL, B-number or backtick.
- **D4: tick 99 by default, with the remainder in NONELEM (Q4).** The commission says to tick "IF closed", and the verdict reads it closed only for child elements. Item 99's own three shapes are all child elements.
- **D5: CLAUDE.md lines 12-13** ("never sent to a person") are named in the kit as superseded for these tickets only, by his later C-80 instruction.
- **D6: the hold lift is RELAYED from the pickup log.** The commission points at "the 10:04 entry of Tuesday's note", but it also says no daily-note folder may be read. DELTA 1391 of the pickup log carries the lift and its three preconditions word for word.
- **D7: H-DOCS is relayed and vague on purpose.** The project has no `Meeting/` folder; the pack lives in the coordinator's tree. The seat only runs `ls -lT` on the 02 and 03 files. I did not verify "03 rounds 1-4", so the text does not say it.
- **D8: C-81 reading on kd1.** His note says "kamil@datase-rd.com" (sic). The kit does not read it as datasec-rd.com, and C-78's one test VM stands until a wider ruling (Q7).

## Q-QUESTIONS FOR TUESDAY (each with a default; the Q-ANSWERS slot lists Q1 to Q8)
Q1 JIRA WRITE (default). Q2 corrections C1 and C2 kept (default). Q3 no comments posted (default). Q4 tick all five (default). Q5 three Info items (default). Q6 C-81 scope as frozen. Q7 the kd1 reading as frozen. Q8 pinned to e2a20aef.
Slot defaults for safety: RECORDS HOLD, JIRA HOLD, TICKS none. Tuesday must stamp WRITE, WRITE and `98 99 100 101 102` to run the work as recommended.

## CHAIN INPUTS
| Step | Inputs | Where from |
|---|---|---|
| 0 | kit, sidecar, b1785.py, record files | BASE |
| 1 | b2022.py and b1785.py (models, read only), scratch copies, fake transport | BASE; Step 0 |
| 2 | SOURCES, origin GETs, live record files, pickup log (search), Jira GETs | BASE / GET |
| 3 | frozen texts, live numbers (Step 2), scanner copy (Step 0) | Steps 0-2 |
| 4a-4d | dry builds (Step 3), before-copies (Step 0), re-read origin, P-8, write log (4b, then 4d) | Steps 0, 3, 4b |
| 5 | proofs, write log | Step 4 |

## UNMEASURED / NEVER RUN
The seat's `b2030.py` and its selftest. The fence and skip rule against live Jira. Any POST: whether Jira accepts `update.issuelinks` together with the assignee in one create; the read-back; the email Jira sends the assignee. HOLD R and R2 on live files. The numbers and keys at the seat's run. A partial-write stop. The REFUSE 2 and 5 pane checks (panes at drafting: `%0 tuesday`, `%127`, `%128`, none of them OXPd). Whether the ADF read-back keeps the double spaces in his quotes. Whether any OXPd pane is live at launch.

## OUTSIDE THE FENCES (disclosure)
- **Read whole:** the commission, DRAFTER_RULES, the B2022 kit (three pages), the B2022 drafter report, the B2010-B2012 commission, answers.txt, B2026 FOR-RECORDS and landing.txt.
- **Read in parts:** B2026 VERDICT (lines 1-80), JIRA-DRAFTS (lines 1-70, 225-284, 520-684; all 29 were parsed by program), the pickup log (lines 1-12 and 55-80), b1785.py (lines 1-60 and 186-600), BACKLOG and CLARIFICATIONS by range.
- **HTTP to a hosted host:** `kam_msgs.sh` reads the live board (Azure-hosted). DRAFTER_RULES fence 4 forbids that, but the commission named that tool explicitly, so I ran it once into scratch.
- **Design/:** I listed it with `ls -lT` and opened no file. I also ran `ls` on `1_Project_Definition` and `.tools`.
- **Cards:** `decision_queue.sh show` on 8 exact Datasec ids, into scratch. No `list` was run.
- **Writes:** only the kit, its sidecar, this report and scratch. Nothing was written to the project, GitHub or Jira (all Jira calls were GET, through a wrapper that raises on any other method).
- **Hook refusals:** `pretooluse_no_cd.sh` refused one `cd`; I re-issued the command with absolute paths.
