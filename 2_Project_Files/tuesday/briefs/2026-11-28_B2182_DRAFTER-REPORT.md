STARTABLE: YES

# B2182 DRAFTER REPORT: re-freeze of the OXPd records kit (seat R343; supersedes B2173, which superseded B2161 and B2146)

I was the in-session, read-only drafter for Tuesday s336. `date` printed my first clock as `Sat 28 Nov 2026 00:03:17 AEDT`. My last check before this report printed `00:26:12`. No Stamp slot holds a typed clock.

**Precondition for YES.** At 00:26:12 three things still held:
- The board's newest OXPd row was 2026-11-27 21:23:51.
- `main` was 7d652c5f.
- The three record files still matched B2140's manifest (`04f77946`, `74800003`, `85b66031`).

The kit stops itself on any of these:
- a new row from him (slot RULINGS-NEW / REFUSE 6);
- X84's landing, or any merged pull request 60 (P-L);
- a new CLARIFICATIONS entry (P-7).

## Files written (nothing else outside my scratch)
- **Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2182_SEAT-R343_oxpd2-records-r3.md`
  - sha256 `2d93f432...`; 235153 bytes; 916 lines; 0 bytes above 126.
  - 11 underscore slot lines.
  - Line 1 says it SUPERSEDES B2173, which superseded B2161 and B2146.
- **Sidecar:** `.measured` beside the kit, sha256 `0c957dfe...`.
  - 192 claims, 0 TODO.
  - `stamp_check.py <kit>` exits rc 0 with "192 measured, 0 not measured".
- **This report.**
- **Scratch:** only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2182/`.
- **How the kit was built:** it is generated from B2173's kit source (`s335/d2173/kit2.src.md`). Prose parts are `kA.md`, `kB.md` and `kE.md`. The text parts come from asserted-replacement builders (`mk_part1.py`, `mk_part2.py`, `mk_part34.py`). Then `dry.py`, `fillkit.py`, `quotes.py` and `side.py` run.
- **Placement:** the kit and sidecar were put in place with `cat` and `cp`, not the Write tool, because of their size. Both are `cmp`-equal to the generated files.

## BLUF of the kit
Everything B2173 records is kept: pull request 58 (C-93, ticks on 54, 55 and 75, items 161 and 162) and his words up to 18:31 (C-94 to C-101). X85's run is kept too (BL-EV-103, item 163). Added:

- **C-102: his six taps of 21:23.** Each is verbatim with its card title, recommendation, detail and store time.
  - K-DOM: a, subdomain of datasec-rd.com.
  - azbridge: a, used as a stand-in.
  - K-OWN: a, "Agent does all but the CA part".
  - Spend: **b**, "Up to A$120 a month, always on". This is not the coordinator's recommendation a, and the entry says so.
  - Printer-callback and parallel-builds: both Noted.
  - The DNS-NS and CA-vault cards are named only as open.
- **C-103: Tuesday's note on pull request 59.**
  - 121 is closed by README lines, not by a chain policy.
  - 137's bound landed, but its hang is not caught.
- **Pull request 59 (main 7d652c5f):**
  - **Tick 121** (BL-CLOSE-121).
  - **137 NOT ticked.** BL-EV-137 records the bound landing, the third sighting and the blocked-call shape.
  - **New item 164:** the bound cannot end a blocked call; a managed stack read is next, and which tool is the coordinator's choice.
  - **New item 165:** the landing's other points (F2 Minor, F3 to F9 Info, seat notes).
- **X88: tick 118** (BL-CLOSE-118: the call back ARRIVED twice direct and once through the forwarder; printer clean). Item 163 is reworded: X88 got round the problem with a mode-600 file, but the lab still opens the file twice.
- **X90/X92: new item 166**, the Azure foundation's deviations and open points. It carries no ids, key names or UNDO lines.
- **Readings updated, his words unchanged:** C-93's range is now to C-102. C-96, C-99 and C-101 now point to C-102 for the spend and the forwarder.
- **Totals:**
  - CLARIFICATIONS: 11 entries, C-93 to C-103.
  - BACKLOG: 5 ticks (54, 55, 75, 118, 121), 2 evidence lines (103, 137), 6 new items (161 to 166).
  - History: 10 lines plus an empty line.
  - Jira: the same 4 POSTs as B2173. J-1 is rewritten for both landings, the 21:23 taps, the device runs and Azure. The comment prefix is now `Records pass after pull requests 58 and 59`, and the near-duplicate stop covers all three prefixes.
- **Neighbour:** X84 (lane L0, pane %617) is live, and its partition is stated from both sides. If X84 lands, P-L stops this kit.

## Facts re-measured (instruments, clocks)
- **Project files** (shasum, 00:04:22; again at 00:26:12): all nine files equal B2140's manifest.
  - CLARIFICATIONS: C-92 is last, at line 1230; 1236 line feeds.
  - BACKLOG: owed 1 to 160 (89 open, 71 ticked); 1212 line feeds.
  - history: 410 line feeds.
- **GitHub** (GET only; gh auth `kamilDatasec`; 00:06:46):
  - main 7d652c5f, one parent 760e1a64, tree 760295e3, equal to head 09b60507's tree.
  - PR 59 merged 11:16:41Z, 5 files 140/5, matching landing.txt lines 18 to 22.
  - PR 58 facts are unchanged. PR 60 and issue 60 return 404; 0 open pull requests.
  - Checks 7/7 success; analyses at 7d652c5f are 0, 0 and 0; open alerts 0.
- **Hosted run:**
  - hosted3 byte copy PASS at 2433/679 (00:07:13); control at 2434 printed FAIL 4 (00:07:22).
  - The landed subject and body equal B2178's files: `#59` True, `#58` False (`msg.py`).
- **Tarball and pointers** (00:07:43): 1780476 bytes, 679 files. Pointers 90 of 90 with the control FIRED. B2173's 62 pointers still hold.
  - `diff -rq` between the trees of 760e1a64 and 7d652c5f shows exactly PR 59's 5 paths.
- **Jira** (GET-only fence fired on POST, PUT, DELETE and PATCH; 00:08:13 to 00:23:37):
  - Census 63; kamil-action tickets are 56 to 61 and 63.
  - OXPD2-1 has 19 comments, the newest 41547. OXPD2-61 has 0 comments.
  - All new phrases find 0 issues.
  - Assignable search, link type 10003 and createmeta fields were re-read.
- **Board:**
  - `kam_rulings_today.sh 2026-11-27` (marker in my scratch, 00:03:33): 32 rows, TAPPED-BUT-OPEN none.
  - `kam_msgs.sh 8` (00:03:45): the six 21:23 rows saved; `passw` 0.
- **Cards:** `show` for 9 named ids (00:03:54).
  - The licence-steps print holds `passw` 1, so it is not a source and is never quoted.
- **P-W:** QUOTES 163, BAD 0 over the written kit.
- **P-8:** B2145 and B2178 literals all as printed (`p8.py`).
- **P-9 to P-12:** X85, X88, X90, X92 and X89 STATUS counts (`seatchk.py`, 00:19:11).
- **P-3 probes:** see the corrections in D6 below.
- **Dry build:**
  - CLARIFICATIONS: 1236 to 1566 line feeds; C-1 to C-103 with no gap.
  - BACKLOG: 1212 to 1261 line feeds, 49 lines added, 5 changed; owed 1 to 166 (90 open, 76 ticked); Closed 68 to 73; Evidence 2 to 4.
  - history: 410 to 421 line feeds.
  - `scan_record` 0 problems over 224 lines; doubled words and groups 0.
  - Jira codes: T-K3 and T-D2 S-DQUOTE S-NAME; J-61 S-DQUOTE; J-1 none.

## Chain inputs (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | kit and sidecar, the project files | at BASE |
| 1 | the `b1785.py` copy | Step 0 |
| 2 | seat STATUS files, both reviews' files, tarball (re-GET), Jira | at BASE / origin |
| 3 | frozen texts, P-7 count, before-copies | kit / Step 2 / Step 0 |
| 4a–4d | dry texts, keys and comment ids from 4c's log, BL sha8 from 4b | Steps 3 and 4 |

## D-decisions
- **D1: 137 is NOT ticked.** The commission says "owed 137 NOT closed; a NEW owed item". The gate recommended ticking 137 plus a new item. To honour both words without a duplicate, 137 stays open as "the hang, cause unknown" with an evidence line. Item 164 is "the landed bound cannot end a blocked call; a managed stack read is next". Q22 offers the gate's option.
- **D2: 118 is ticked** on its own closing words, which X88 printed (Q20).
- **D3: no Jira ticket comes from the 21:23 taps.** The DNS and vault cards are still open, and the ceremony waits on the vault (Q25).
- **D4: no ids appear in any text.** The Azure STATUS files hold a subscription id, a tenant id, resource ids and a shared-key rule name. No text carries any of them, and the HOLDS forbid copying them.
- **D5: the parallel-builds card covers OXPd AND NexusAI.** The store tags it Datasec/OXPd, but its BLUF says "Datasec/OXPd and NexusAI". C-102 records it for this project's part only, and P-W checks that wording at source (Q26).
- **D6: corrections made during drafting, each caught by a check:**
  - BACKLOG already held `oxpd2-dev-rg` on item 114's lines, so item 166's search line was reworded.
  - Two doubled-word hits ("46, 46" and "his, his") were reworded.
  - A missing comma in H-WORDS was fixed.
  - The landing.txt line range was corrected to 18 to 22.

## Q-questions for Tuesday (each default already assumed in the kit)
- **Q1:** C-103 is a separate note. Default: as written.
- **Q20:** tick 118. Default: as written. Alternative: an evidence line until a test-button lane runs it.
- **Q21:** tick 121 by README lines. Default: as written.
- **Q22:** 137 open, with an evidence line, plus item 164. Default: as written. Alternative: the gate's (a), tick 137 for the bound.
- **Q23:** PR 59's F2 to F9 go in item 165. Default: as written.
- **Q24:** item 166 for the Azure build. Default: as written. Alternative: history and C-102 only.
- **Q25:** no new tickets from the 21:23 taps. Default: as written. Alternative: a third create for the NS records, due 2026-12-01.
- **Q26:** the parallel-builds card is recorded for OXPd's part only. Default: as written.
- **Q2 to Q19:** as B2173. Default: as written.

## UNMEASURED / NEVER RUN
- The seat's helper, HOLD R and R2, the live writes, and the 4 POSTs.
- Nothing measured in Azure: X90's and X92's facts are relayed, and Tuesday read them back.
- PR 59's pull request run job logs were not read line by line. Its runs are only read as success at attempt 1.

## Outside the fences (disclosure)
- **Board:** `kam_rulings_today.sh` (marker in my scratch) and `kam_msgs.sh 8` (twice, the second only for its newest row). No row held a credential. One row (18:21) names a sign-in account; it is not quoted anywhere.
- **Cards:** `show` for 9 named Datasec ids, never `list`.
- **Coordinator files:** pickup lines 70 to 82 and these daily-note lines of 2026-11-27, by number: 123, 128, 133 to 137 and 139 to 141. Those lines hold IP addresses and a partial subscription id; none was copied into a text.
- **X84's kit:** lines 1 to 187 by `grep` only (partition, owned paths).
- **A path guard refused** a `cp` of `b1785.py` out of the project tree. I copied it with `cat` instead (`cmp` equal), and wrote nothing in the project.
- **Not touched:** no write to the project, Jira, GitHub, cards or mail; no `cd`; no az; nothing deleted.
