STARTABLE: YES

# B2201 DRAFTER REPORT: OXPd records re-freeze, seat R345 (a narrow revision of kit B2182, seat R343)

I was the in-session, read-only drafter of section 5 of commission B2197-B2201, for Tuesday s337. `date` printed my first clock as `Sat 28 Nov 2026 02:51:58 AEDT` and my last check before this report as `03:15:27`. No Stamp slot holds a typed clock.

**Precondition for YES.** These held at my last reads (03:14:53 to 03:15:27):
- `main` was d9f89115.
- No pull request numbered 63 or more had MERGED. Pull request 63 (lane L1c, `b2185/x94-oxpd1-contracts-l1c` at f4aacb5e) was OPENED at 03:14:52 AEDT and read open at 03:14:57. The kit names it, and an open pull request is not a stop. Per the commission, it is left to the next records pass.
- The record files equalled B2140's manifest: `04f77946`, `74800003`, `85b66031`, `0f1fccc0`.
- The board showed no OXPd row of his newer than 2026-11-27 21:23:51.
- There were no `OXPd2-R` panes and no `.tools/b2201` or `.tools/b2182` folder.

## Files written (nothing else outside my scratch)
- **Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2201_SEAT-R345_oxpd2-records-r4.md`
  - sha256 `be2810dcae71b6c7...`, 293176 bytes, 1089 lines, 0 bytes above 126.
  - 11 underscore-slot lines; the last line is `READ-WHOLE-BY-TUESDAY: ____`.
  - Line 1 SUPERSEDES B2182 (R343), which superseded B2173, B2161 and B2146.
- **Sidecar:** `...r4.md.measured`, sha256 `af39a8ef4f55dbcb...`, 220 lines, 0 TODO.
  - `stamp_check.py <kit>` prints `220 claims, 220 measured, 0 not measured`, rc=0.
- **This report.**
- **Scratch:** only `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s337/d2201/`.
- **How the kit was built:** by program from B2182's source (`s336/d2182/kit3.src.md`). `mk_r345.py` and `mk_part2.py` apply asserted replacements, and the new texts live in `newtexts.md`. Then `dry.py`, `quotes.py`, `fillkit.py`, `side.py` and `patch_side.py` run; `finalize.sh` runs the whole chain.
- **Placement:** like B2182's drafter, I placed the kit and sidecar with `cp`, not the Write tool, because of their size; `cmp` shows the kit equal to `kit6.out.md`.

## BLUF of the revision
**Kept from B2182 byte for byte:** every frozen text except H-HEAD, H-JIRA, H-FULL, J-61 and J-1 (40 texts become 53). The program compared the frozen tables:
- Changed: exactly those 5.
- New: 13.
- Dropped: 0.

**Re-frozen to main d9f89115:**
- **P-L:** gains the facts of pull requests 60, 61 and 62. Main's stop is now "not d9f89115, or a MERGED 63 or more".
- **P-F:** reads the tarball of d9f89115. B2182's 90 pointers still hold, because pull requests 60 to 62 touch none of their files. The compare of 7d652c5f and d9f89115 lists 86 files, 0 of them under the six pointer folders; the control fired. B2182's `facts.py` over the new tree printed `POINTERS 90 of 90` with a table equal to B2182's.

**Added records:**
- **C-104, C-105, C-106:** Tuesday's notes, one per landing (Q27).
  - 60: the wide scaffold, every byte frozen.
  - 61: the two-step download through a caller's client; an upload session for every size, a name that exists refused, the 100 MiB bound.
  - 62: no device code, as the design's default; the object id from the id token's checked claims, signature not checked. F3 is named open and the coordinator's.
- **Owed items 167 to 171 (Q28):**
  - 167: the landing item of 60 (B2190, F1 to F8, all Info).
  - 168: 61's Minor F1. `MyDriveBrowser.IsItemId` ends its pattern in `$`; owed to a later OneDrive lane.
  - 169: the landing item of 61 (F2 to F10, for the host and the print lane).
  - 170: 62's F3 as the OWED design item, in the commission's words: "fail closed is the coordinator's design call for a later round of the sign-in" (Q29).
  - 171: the landing item of 62. It covers what L3b must guarantee: no default Authorization header and no redirects (F5), the TLS default and the authority host fixed (F4), the start route authenticated and rate-limited with `MaxPending` sized, since 64 pending starts refuse every start for ten minutes (F2), and the certificate kept undisposed. It also covers F1 (the raw credential failure) and the Info findings.
- **History, 15 texts:**
  - New: H-LAND60, H-LAND61, H-LAND62, H-REC6062, H-OWNER6062.
  - Changed: H-HEAD, H-JIRA, H-FULL (now names `B2201_STATUS`).
- **Jira:** the same four POSTs as before.
  - J-1 gains one paragraph on the three landings and the open design question.
  - The prefix of J-1 and J-61 is now `Records pass after pull requests 58 to 62`.
  - The SKIP RULE's near-duplicate list adds that prefix.
- **No owed item closes** by 60 to 62: no open item names one of them as its closing condition.

**Names:** seat R345, pane `Datasec/OXPd2-R345`, `.tools/b2201/`, STATUS `2026-11-28_B2201_STATUS.md`, HANDOVER `B2201`. REFUSE 4 also refuses `.tools/b2182` or a B2182 STATUS, and REFUSE 5 bars a pane named `OXPd2-R343`. The model is Opus: `BRIEF_SEAT_LEVEL=opus` inside the quotes, per `CLAUDE.md:7`, and `models_latest.json:17` reads `claude-opus-5-5`.

**PARTITION, from both sides:**
- In gate: L1c (X94, gate B2195) and L3a (X97, gate B2196).
- May launch: L1x (X95), AZ-1 (X99, live as pane `%638`) and the wave-2 lanes X100 to X103 (each its own folders).
- None of them writes a record file. A records seat writes only record files outside the repository and runs beside all of them.

## Facts re-measured (instrument, clock)
- **Record files:** shasum at 02:52:40 (seven files) and 03:13:18 (the two design files). All nine equal B2140's manifest, again at 03:14:53. CLARIFICATIONS ends at C-92 (line 1230), BACKLOG holds owed items 1 to 160 (89 open), and history.md has 410 line feeds.
- **GitHub (GET only):** `gh auth status` showed `kamilDatasec`. Reads by `ghreads2.py` at 02:54:45 and again at 03:07:35 and 03:14:57:
  - Main is d9f89115: tree aa53e949, one parent cf224e1f.
  - PR 60: merged 13:49:02Z as 0ee3b091, one parent 7d652c5f, tree fc101f81 equal to the head's. 61 files (60 added, plus slnx with 20 lines added); +2424 / -0.
  - PR 61: merged 14:57:15Z as cf224e1f, one parent 0ee3b091, tree 888af9d5 equal to the head's. 7 files; +946 / -6.
  - PR 62: merged 15:49:38Z as d9f89115, one parent cf224e1f, tree aa53e949. That is the review's squash tree (`evidence-squash-tree-on-new-main.txt` line 1); the head 57b6f6e2 sits on 0ee3b091. 21 files; +2787 / -1.
  - Each squash shows check-runs 7 of 7 success; at d9f89115 I re-read this at 03:07:35, after its windows leg ended.
  - Main's analyses, 15 rows across the five squashes, all `results_count` 0. Open alerts 0.
- **Hosted (byte copy of `hosted3.py`, sha 969fe376):**
  - PASS at 0ee3b091 (2445/739) and cf224e1f (2488/744) from 02:55:26.
  - The control, cf224e1f at `--total 2489`, printed `FAIL 4` at 02:55:54.
  - d9f89115 (2539/762, with `--wait`) printed PASS at 02:55:58.
- **Landed messages (`msg2.py`):** for each of the three squashes, the subject with its own number is True and with the next number False. The body without its final line feed is True; with it, False.
- **B2182's reads of 58 and 59:** I re-ran its `ghreads.py` (main read by its sha) at 03:11:30, its `msg.py`, `p8.py` at 03:11:14 (0 False) and `seatchk.py`. The outputs are equal; `seatchecks.md` is byte-equal to B2182's.
- **P-8 of the three reviews (`p8b.py`, 03:12:26):** 46 of 46 line-start literals; controls fired.
- **P-3 (`probe.py`, 03:06:25):** every zero literal 0, including the new ones (C-104 to C-106, items 167 to 171, the five shas, `IsItemId`, `MaxPending`, `SubjectMismatch` and the rest). Every control is at least 1.
- **Pointers (`facts.py` over d9f89115, 1829829 bytes, 762 files):** 108 of 108 pass, including 18 new pointers. The control (one line off) fired.
  - The gate's `TokenBroker.cs:409-413` is off by two: the catch is at 411 and RefreshFailed at 414. The kit uses the measured lines.
  - The gate's `EntraTokenClient.cs` 60-69 range is written as `:62` to `:68` (the WriteTo line to the `throw;`).
- **Jira (GET-only fence fired on POST, PUT, DELETE and PATCH; 02:57:55 to 02:58:15):**
  - Census 63; kamil-action tickets are OXPD2-56 to 61 and 63.
  - OXPD2-1 has 19 comments, the newest 41547 (`Records pass after pull request 57`). OXPD2-61 has 0 comments.
  - All 16 new phrases find 0 issues; the controls found OXPD2-1 and OXPD2-61.
- **Board:** `kam_rulings_today.sh 2026-11-28`, with the marker in my scratch, at 02:54:25: 0 rows; newest live row 21:23:51; `TAPPED-BUT-OPEN: none`; `passw` 0. I read no card.
- **P-W:** `QUOTES 163 BAD 0` over the written kit.
- **Dry build (`dry.py`, prototype fills):**
  - CLARIFICATIONS: 1236 to 1590 line feeds; C-1 to C-106 with no gap.
  - BACKLOG: 1212 to 1296 line feeds; 84 lines added, 5 changed; owed items 1 to 171 (95 open, 76 ticked); anchor heading 1197 to 1281.
  - history: 410 to 426 line feeds.
  - `scan_record`: 0 problems over 276 lines. Doubled words and groups: 0, after two fixes (D2).
  - Jira codes are unchanged: T-K3 and T-D2 `S-DQUOTE S-NAME`, J-61 `S-DQUOTE`, J-1 none.
- **Seat id (`seat.py`):** R345 appears on 0 of 1665 SEAT kits and in no file name. R346 is named in a NexusAI kit (B2202), not by this seat.
- **Panes (03:06:31):** `%0 tuesday`, `%638 Datasec/OXPd2-X99` and four unnamed panes.

## Chain inputs (MEASURED LITERALS rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | kit, sidecar, the nine project files | at BASE |
| 1 | the copy of `b1785.py` | Step 0 |
| 2 | seat STATUS files (X84/X93/X96 included), the five reviews' files, the tarball of d9f89115 (re-GET), Jira | at BASE / origin |
| 3 | frozen texts, P-7 count, before-copies | kit / Step 2 / Step 0 |
| 4a-4d | dry texts, the keys and comment ids from 4c's log, the BACKLOG sha8 from 4b | Steps 3 and 4 |

## D-decisions
- **D1: one C-entry per later landing**, as C-93 and C-103 are each a note on one landing (Q27).
- **D2: two doubled-number hits in the dry build** were reworded: `60: 60 added` became `of which 60 are added`, and `64, 64 starts` became `a burst of 64 starts`.
- **D3: B2182's texts that say "at main 7d652c5f, by this pass's read" are kept unchanged.** P-F proves the pointer files are unchanged at d9f89115, and the seat reads every pointer from the new tree.
- **D4: open pull request 63.** It opened during drafting. P-L records it as open and says an open pull request, or a 404 that has become an open one, is never a P-L stop.
- **D5: C-106 uses the design's own default.** Its line 1225 reads "device code is not built before test 1 reports". C-106 cites this as the design's default, not a new choice.

## Q-questions for Tuesday (each default already assumed in the kit)
- **Q27:** one note per later landing. Default: as written. Alternative: a single C-104.
- **Q28:** items 167 to 171 as listed above. Default: as written. Alternative: 62's F2 (the 64-pending refusal) as its own item.
- **Q29:** 62's F3 as OWED design item 170, no ruling. Default: as written. Alternative: Tuesday rules now and C-106 and 170 are re-frozen.
- **Q-RUNNER:** not applicable to this kit, which runs no heavy job and takes no lock. Default: NO runner. The answer to the commission's question is in the next section.
- **Q1 to Q26:** as B2182. Default: as written.

## Q-RUNNER: the fact the default turns on, with proof
**Answer: yes, the counting runner excludes holders of the OLD single lock for heavy jobs. The two schemes never run more heavy jobs than the slot count, so they never run three at once with `heavy-slots` set to 2.**

**From source:**
- The canonical runner (sha 31adedc8, `s336/g2190/gate/heavy.py`) takes exactly `<project>/.tools/wave1-heavy.lock.d` by `os.mkdir` (line 18 `LOCK = ...`; line 58 `os.mkdir(LOCK)`). It reads no `heavy-slots` file: a count of `heavy-slots` or `lock.d.` in it reads 0.
- The counting runner (sha 89223aca) defines `slot_dir(1)` as exactly that folder and `slot_dir(k)` as `.lock.d.<k>`. It takes the lowest free slot of `1..SLOTS` by `mkdir`, and with no slot free it waits.
- So an old holder occupies slot 1, and an old runner arriving while v2 holds slot 1 waits on the same folder.

**From a run** (`qrunner/harness.py`, sha a46137e5, over a SCRATCH `HEAVY_LOCK_ROOT` with `heavy-slots` 2, load read from a file, `/bin/sleep 6` jobs, no dotnet, 02:57:27 to 02:57:45):
- An old holder, made by the canonical runner's own `mkdir`, plus two v2 jobs started together: at most **2** lock folders held at once. Job A took slot 2; job B waited (2 lock waits) and took slot 1 after the old holder was released.
- Control mutant (slot 1 renamed `.d.1`): at most **3** held at once, so the mutant runs three.

**One caveat for the coordinator:** a project listed in `heavy-light-projects` runs on its own lock, beside both heavy slots, by design (B2172 REPORT P7). Such a light job is a third dotnet job by design, not a failure of exclusion. With no `heavy-light-projects` file, nothing runs beside the slots.

## UNMEASURED / NEVER RUN
- As in B2182: the seat's helper and selftest, HOLD R and R2 on the live files, the live writes and the four POSTs.
- The pull-request runs' job logs of 60 to 62 were not read line by line. The hosted push runs at the three squashes were read to PASS by `hosted3.py`.
- The design call of item 170 and the host lane's guarantees of 171 are recorded, not decided.

## Outside the fences (disclosure)
- **Board:** `kam_rulings_today.sh 2026-11-28`, with `KAM_READ_MARKER` set to my scratch. I made no card read and never ran `decision_queue.sh`.
- **Coordinator files:** I read my coordinator's briefs and gate folders, B2172's runner folder (read only), and its `quotes.py` sources by program (P-W counts only).
- **The counting runner:** I copied it into my scratch and ran it only over a scratch lock root, with `/bin/sleep`. I took no project lock and ran no dotnet job.
- **`sed -i`:** I used it once on my own scratch script (`facts.py`), outside any repository.
- **Not touched:** no write to the project, Jira, GitHub, Azure, cards or mail; no `cd`; nothing deleted.
