LAUNCH BRIEF (Seat R 2nd): successor of Seat R 1st on pane `Secuura/Blockchain-R`. R 1st raised #1395 (KS-1305) and WRAPPED cold at ctx 52%. You have TWO jobs, in this priority: **(1) merge #1395 on `GO (Seat R 2nd): merge 1395 on gate69`, but only AFTER Seat E 8th's `STATUS: merged 1396`,** with a docs-only merge-in of the develop that carries #1396's squash; **(2) meanwhile, and after, continue the RAISE lane: PR 2 KS-1136, then KS-998, KS-1313 (+KS 1326), KS-1164,** the Wednesday-held Spark passes R 1st did not raise, each file-disjoint from every live PR. cloud: merge + raise (Kam's 2026-10-06 09:37 80%-Spark rule). Secuura NEVER force-pushes.

# LAUNCH BRIEF: Seat R 2nd, Secuura/Blockchain, lane R (pane `Secuura/Blockchain-R`). MERGE seat for #1395 and RAISE seat for PRs 2-5. From Wednesday (DRAFT: staged by Wednesday's brief drafter, NOT sent, NOT launched)

## RULED BY WEDNESDAY AT STAGING (12:4x AEDT 2026-10-06, the drafter's open questions)
- **Q-1800: MOOT.** Kam ruled card `secuura-ks1256-redis-outage-stops-connector-creates-1006` = a at 10:22:01 ("Accept: fail closed (503) during a Redis outage"). The card's 18:00 default no longer applies; there is no time hold on the #1396 merge.
- **Q3 "closed":** "fail(s) closed" (including Kam's verbatim quote) STAYS. The closing-family rule is about a Linear magic word followed by a key. Your scan must show 0 `clos*` words within 3 lines above the `Refs` line, and 0 closing words immediately followed by a key. Quote both counts, each with a planted control that fires.
- **Q-SRC2: raise from the run directory's `out.md.checker/patch.diff`, as R 1st did.** Wednesday's earlier relay said "READY_ diff files". That was wrong for these four: no October READY_ file exists for them (the drafter measured it). Withdrawn by name.
- **Kit defect:** `c4_docs_gate69.py predict` exits 0 whenever it writes a tree, regardless of the read-back. Judge every prediction by its READ-BACK lines, never by its rc.

## 🔴 LAUNCH PARAMETERS. Wednesday fills the first two at send; the last three arrive LATER, in the mail that carries your GO. A brief sent with `@DEVELOP_LAUNCH@` or `@SEND_UTC@` unfilled is VOID: refuse it and mail. A GO that does not carry `@DEVELOP_1396@` and `@T1395@` is INCOMPLETE: ask, never guess.
| Placeholder | When | What | Instrument |
|---|---|---|---|
| `@DEVELOP_LAUNCH@` | at send | develop at origin at send, 40-hex, with its PR | `ls-remote` (shared checkout, its own `core.sshCommand`, `GIT_SSH_COMMAND` unset) + `GET /commits/<sha>` |
| `@SEND_UTC@` | at send | the send time | `date -u` |
| `@DEVELOP_1396@` | in the GO mail | develop at origin AFTER #1396's squash (E 8th's `STATUS: merged 1396` names it), 40-hex | E 8th's STATUS + Wednesday's `ls-remote` |
| `@T1395@` | in the GO mail | Wednesday's FIRST-HAND TAIL tree for #1395's merge-in on `@DEVELOP_1396@`, 40-hex | `c4_docs_gate69.py predict --pr A` in Wednesday's own scratch clone |
| `@RAISE_BASE@` | in the ITEM 0 ANSWER | the develop your raise PRs are built on (Q-BASE2) | as `@DEVELOP_LAUNCH@` |

**What the drafter predicted, CONDITIONALLY (P10).** If #1393 lands at its gate68 TAIL tree `0b4c3a265454343e8b39af71d2ee6e30bd1d6059` and #1396 then lands at the tree the drafter computed over it, `cee3fc9913199eeb7eebb1e1c058ff8062ee19a8`, then `@T1395@` should be **`3e708d1191ad652809cbef84215cd496ad1b74ea`**: flow blob `278694921bc4` tail `18 19 20 21 22`, cheat blob `e4ab72a1d4c6` tail `… KS-723 KS-1278 KS-1256 KS-1305`, both READ-BACK OK. **Computed on SIMULATED develops; a cross-check, never the authority.** If either real squash tree differs, this figure is void.

## 🔴 READ FIRST
- **The gate verdict WHOLE:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_mail_g69.txt` (155 lines, P1): the GO string `:5`, the merge ORDER (#1396 FIRST) `:17`-`:19`, "the second PR re-predicts on the develop that actually carries the first" `:23`, the divergence and its trap `:24`-`:28`, the Actions condition `:29`, the #1395 subject `:32`, the #1395 rows `:41`-`:51`, the tamper matrix `:74`-`:81`, cell order `:90`-`:93`, findings N-1395-1..4 `:109`-`:112`. The report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-gate69-batch/report.md` (sha256 `19d2167db31f504c…`, P2), especially the #1395 MERGE ADDENDUM line `:553`.
- **Wednesday's gate69 rulings:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate69/RULINGS_wednesday.md` `:48`-`:57` (P3), and the kit README beside it.
- **R 1st's handover WHOLE, read-only:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatR1-2026-10-05.md` (147 lines, 10,787 B, sha256 `a66399885d8abab5589a468c68078780c1b8816ac96028d285e59e59ea5f2eae`, mtime 2026-10-06T00:20:13Z, P5). **Re-hash it at ITEM 0 and say whether it moved.** It is the wrap artefact your squash names. Parts you need:
  - the PR table (`:10`-`:16`) and "All five held payloads are re-verified at this base" (`:22`-`:25`; at `3f9ff4e1e1b9`);
  - Findings 1-8 (`:38`-`:72`), especially 5 (one red arm per conjunct), 6 (53 vs 55 trailer control), 7 (KS-1422: install akto before a push), 8 (prettier is not a gate for originate);
  - ADDENDUM (`:86`-`:147`): **inherit `2026-10-05_seatR-1st/raise/`, do NOT re-copy from B 65th**; `inbox_matchra1.py` `MINE` must be changed BY HAND; `pushra1.sh`'s re-check must MIRROR `lockra1.sh`'s WAIT set.
  - 🔴 **Superseded in it:** `:101`-`:103` ("needs no merge-in while develop is still 3f9f … resolve ONLY those, keep every block") is replaced by the TAIL rule and `qm` (RULINGS Q2). `:95`-`:98` "merges only after #1394" is SATISFIED (#1394 is `4eaf`).
- **The original raise brief, for PRs 2-5:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_seatRaise_spark5.md` (461 lines, P6): the BLUF table `:129`-`:135`; DOC SEQUENCING `:148`-`:153`; PARTITION `:187`-`:204`; PUSH PROTOCOL `:217`-`:223`; PROJECT RULES `:248`-`:259`; ITEMS 2-6 `:290`-`:334`; Q-1326 `:354`; DEFECTS `:399`-`:407`. **Its base, seat name, token, tool generation and WAIT set are superseded below; its per-PR work (fences, red-first, siblings, bodies, NOT COVERED) stands.**
- **"#1395" means GitHub PR 1395 (ticket KS-1305).** #1396 (KS-1256) is Seat E 8th's and merges BEFORE yours. #1393 (KS-1278) is Seat B 67th's. **Never touch their branches, worktrees (`s-e6-ks1256`, `s-b63-ks1278`) or locks.**

## BLUF
You are **Seat R 2nd**. #1395's head at origin is **`1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660`** (P7):
- `refs/pull/1395/head` == `refs/heads/feature/ks-1305-prisma-not-generated-diagnosis-ra1-1` == it, at 01:22:18Z; the shared checkout also holds a LOCAL `refs/heads/…-ra1-1` at the same sha (P12);
- tree `924908aeefe1`, ONE parent `3f9ff4e1e1b9` (= the merge-base), 4 files (db.ts +19, the ks1305 test +119, flow +90 block `22.`, cheat +41), 0 trailers (P1 `:42`);
- the PR: open, `mergeable false / dirty`, title 77 chars == the gate-signed subject, body 8,891 B / 8,839 chars, sha256/16 `e3e2ba5f26d1e033` (P8).

**The head does not move until your merge-in.**

🔴 **develop moves TWICE before your merge, and every gate69 tree for #1395 is VOID for you.**
- gate69 predicted #1395's merge-in on `4eaf7741a6a4`: alone `37773febc715`, second over #1396 `883d4b70343c` (P1 `:18`-`:22`).
- Seat B 67th merges #1393 (KS-1278); then Seat E 8th merges #1396 (KS-1256) over it. Both edit BOTH docs. At draft (01:22:25Z) develop was still `4eaf7741a6a4` (P7).
- **So your merge-in target is `@T1395@`, predicted on `@DEVELOP_1396@`, and you RE-PREDICT it yourself as the second hand** with the gate69 kit before any ref write.
- **Your merge waits for E 8th's `STATUS: merged 1396`** and for Wednesday's GO mail carrying the two parameters. Until then you raise (QUEUE R-track).

🔴 **The merge shape to expect (drafter, P10, on the simulated develops):** `git merge-tree` of `1bdf` over #1396's squash gives **rc 1 with BOTH docs conflicted**. Hand readings: on the FLOW, "THEIRS then OURS" equals the TAIL blob; **on the CHEAT, "THEIRS then OURS" READS BACK OK BUT IS NOT BYTE-EQUAL** to the TAIL blob. That is the trap `qm` M8 exists to catch (P1 `:27`, RULINGS Q2). take OURS, take THEIRS and OURS-then-THEIRS fail the read-back on both. **So you resolve by CONTENT to the kit's TAIL blobs, never by a hand reading.**

**Order (two tracks; the M-track preempts the R-track at a commit boundary):**
1. ITEM 0 (read-only; ends in the plan-confirmation QUESTION; STOP for the ANSWER).
2. R-track: ITEM R2 (PR 2 KS-1136, T1) -> R3 (KS-998) -> R4 (KS-1313 + KS 1326) -> R5 (KS-1164), each ONE local commit; R6 push / raise / ONE READY.
3. M-track, when the GO mail arrives: ITEM M1 merge-in + `qm` + Actions + FF push; ITEM M2 squash with the EXPLICIT body; STATUS `merged 1395`. **Finish the commit you are building, then switch.** Never hold a lock across the switch.
4. WRAP.

**Budget.** 🔴 **The merge of #1395 is the priority: never let raise work spend the ctx the merge needs** (~20%). **Never START a new PR build past ~45%. Never START a push past ~50%. Hand over COLD at ~60%**, naming the NEXT unbuilt row and every built commit (head, tree, trailer proof, pathgate) as UNPUSHED unless pushed. Read ctx off YOUR statusline, or write "Please read my ctx." Never estimate it. Never end a turn on a "next up" line with nothing running (STANDING_LINES `:338`). Expect a successor (R 3rd): four PRs exceed one seat's budget.

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** 🔴 **Every tool below is named by the path you will copy. Where your copy of a tool and this brief disagree about a gate, a knob or a line number, THE TOOL WINS: run nothing on the disputed point, and tell Wednesday what the tool says.**

**WAKE:** your re-seated `inbox_watchra1.sh`, armed in the background at boot with `timeout: 7200000`. It exits on every FOR-ME match. **RE-ARM IN THE SAME ACTION THAT READS THE MAIL.** `SINCE` is the newest mail you have READ, never a wall clock (`:399`). After any long side-effecting action (install, suite, push, merge), LIST the inbox by API before the next ref write. **E 8th's `STATUS: merged 1396` goes to Wednesday, not to you: your release is Wednesday's GO mail, never E 8th's STATUS read off the shared inbox.**

RULED BY KAM, NOT YET IN AN ARTEFACT
- **Routing: cloud: merge + raise.** Kam 2026-10-06 09:37:54, live board, verbatim: *"we are past 70% of the weekly allowance. We now need to switch to using the spark for 80% of tasks"* (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-06_past-70pct-spark-takes-80pct-of-tasks.md` `:20`, P17). **Necessity:** the Spark cannot merge, cannot raise a PR, cannot write §4 doc blocks against measured timings, and cannot re-prove red-first at a new base. Your four raises CARRY four Spark tasks.
- **The 2026-09-11 TESTED merge grant:** each merge only on a gate's GO naming the head SHA. The GO naming `1bdfbe0f2f06` IS the approval for #1395. PRs 2-5 need their OWN gate and GOs.
- **Card `secuura-capped-prs-1245-1278-disposal-1005` = a** (ruled 2026-10-05 20:07:30 AEDT; text read by Wednesday, raise brief `:17`): "Close each one after its replacement merges. A seat closes it with one comment pointing at the new pull request. Nothing is deleted; the branches stay." **Your PR 4 (KS-1313) is #1245's replacement. Only AFTER PR 4 MERGES (not this round) does a seat close #1245 with ONE comment. #1278 is KS-1314's, not yours.**
- **No pre-push leg is added this round** (`secuura-pushgate-three-legs-1005` = a).
- Standing: Kam 2026-10-04 ~19:4x "do as much work with the spark and claude agents on the secura projects as you can"; drive hygiene 2026-10-05 12:13:55 (`:397`); 2026-09-18 09:22 batch the gates (`:257`); the 31 Oct goal.
- **Ticket creation, one ticket per TEST PASS** (Kam 2026-09-07 13:23, `:86`-`:93`). New and unassigned tickets go to the board account (`:94`).

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **gate69 RULINGS (P3):**
  - **P1:** the merge seat is Seat R 2nd, GO string `GO (Seat R 2nd): merge 1395 on gate69`. It supersedes the READY's "GO (Seat R 1st)". **A GO naming R 1st is NOT yours.**
  - **P4 / Q2:** TAIL. Your block goes last in merge order; `22.` stays `22.`. The TAIL tree is the target and `qm` M8 decides. A hand resolution that reads back OK but is not byte-equal FAILS.
  - **Q1 (a): #1396 BEFORE #1395.** The flow then ascends `… 20 21 22`.
  - **Q4:** X10 was granted to the GATE (it did not use it: the suite loads without a generated client). **Not a grant to you: never run `prisma generate` in a shared or adopted worktree.**
  - **Q5:** a pre-existing Actions failure is named with its log line and does not block; one caused by this diff BLOCKS.
- **The #1395 squash subject (P1 `:32`, gate-signed TRUE of the whole diff):** `KS-1305: diagnose a missing generated Prisma client instead of a module error` (77; 85 with ` (#1395)`).
- **Raise rulings carried from R 1st's round (raise brief `:9`-`:18`, `:416`-`:430`):** five PRs, not one bundle (Q-BUNDLE); **no two `Refs` in one PR** (the board guard); Q-1326: `Refs KS-1313` hyphenated, **KS 1326 de-hyphenated in words**, neither closes; Q-TIER KS-1136 T1, the rest T2; Q-N flow blocks `23.` KS-1136, `24.` KS-998, `25.` KS-1313, `26.` KS-1164, cheat sections KS-keyed at the TAIL; `17.` stays a gap; Q-A: KS-1313 is UNASSIGNED (P9), assign it to the board account on the ANSWER's word only; Q-F: no fetch in the shared checkout; Q-M: a tree-equal, docs-only merge-in head is covered by its gate.
- **Standing:** a gate that trips on the INSTRUMENT is fixed and resumed, one that trips on a READING is a STOP and a mail; any red not red at develop is a STOP; the GO composes squash subjects (no `(#n)`, `:318`); de-hyphenate every key but the PR's own (`:278`); a ticket that moves itself on PR creation is reported, never reverted; a client comment goes out only after its gate, on the GO's relay.
- **KS-1305 stays In Progress after the merge** (Refs, and §5f owes a live sweep). R 1st's handover `:105`-`:107`: KS-1305 moved Backlog -> In Progress at 00:13:05Z on PR open; not to be reverted. Done = STOP and mail at once.

## THE PARTITION AND THE LOCK
| Seat | Pane | Token / lock | Files | Doc blocks |
|---|---|---|---|---|
| **R 2nd (you)** | `Secuura/Blockchain-R` | `ra2` / `.push-lock-d8` (Q-LOCK2) | #1395: the docs-only merge-in on `feature/ks-1305-…-ra1-1` in `worktrees/s-ra1-ks1305` (ADOPTED) + the squash. PRs 2-5: the raise brief's P6 sets ONLY, in NEW worktrees `s-ra2-ks{1136,998,1313,1164}` | `22.` + cheat `KS-1305`; `23.`-`26.` + their cheat sections |
| R 1st (WRAPPED) | same pane | `ra1` | #1395's author | — |
| E 8th (merges FIRST) | `Secuura/Blockchain-E` | `e8` / `.push-lock-e4` (WAIT) | #1396 KS-1256: api-gateway `verification.ts`, the ks1256 test, 6 doubles files, ks1195, both docs | `21.`, cheat `KS-1256` |
| B 67th (live at draft, `%60`) | `Secuura/Blockchain` | `b67` / `.push-lock-56` (WAIT) | #1393 KS-1278: originate `documentRepo.ts`, `routes/documents.ts`, ks1278 + ks1293 tests, both docs | `15.`, cheat `KS-1278` |
| F / G (no pane at draft) | `-F` / `-G` | `.push-lock-f3` / `.push-lock-g1` (WAIT) | — | — |

- **Measured disjointness (P10):** the four raise product files are byte-identical at `3f9ff4e1e1b9` and in the simulated develop carrying #1393 + #1396 + #1395 (`check-package-format.sh` `cfae0cc`, `09-aggregate-report.sh` `739ebab`, `gate/report.ts` `ac59af3`, `unitSuiteSlotIndependence.test.ts` `00103d9`), and 0 of the 20 paths `3f9f..` that develop touches match a raise path. **Re-measure at `@RAISE_BASE@`.**
- **Semantic adjacency, #1393 x #1395 (raise brief `:201`):** #1393 adds `ks1293-originate-suite-is-hermetic.test.ts` with a MANIFEST-DRIFT cell (`:168`-`:179` at `b5adaba`): any originate test file mentioning `ANCHORING_SERVICE_URL` that is not in its SUBJECTS list reds it. **By READ, the ks1305 test mentions that key 0 times (control: ks520 2)**, so the cell should stay green. That is a read, not a run: **run the whole originate suite at M** (M-track) before the push.
- **Q-LOCK2 (pre-ruled: yes):** reuse `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-d8` with `export LOCK_SEAT='Secuura/Blockchain-R ra2'`. Tools keep generation `ra1` (as the B lane keeps `*56`); only the SEAT token moves `ra1` -> `ra2`.
  - Copy R 1st's tools from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatR-1st/raise/` into YOUR record folder's `raise/`, hashing every entry at copy. Do NOT copy `*.b65src`, `_b65_artefacts_NOT_MINE/`, `*.rc/.out/.start/.end/stubs` or R 1st's push records.
  - **`:414` WAIT parity.** At draft (P11), `lockra1.sh`: own `.push-lock-d8` `:217` with a NAME GUARD `:223`; WAIT `-f3` `:289`, `-e4` `:302`, `-g1` `:303`, `-56` `:307`; the foreign-holder STOP rc 12 `:496`-`:501`. **`pushra1_ff.sh` holds 0 `push-lock-*` literals** and delegates to `lockra1.sh take` (`:110`) / `release` (`:117`). `pushra1.sh` (first pushes) carries its own re-check set: assert it EQUALS `lockra1.sh`'s, with `-d8` in neither (R 1st handover `:122`-`:125`).
  - The foreign-holder guard reads the holder `seat`: **a `.push-lock-d8` held by `Secuura/Blockchain-R ra1` is now FOREIGN to you** (rc 12). R 1st released it (`lock-released.txt` in its record folder); confirm it is absent.
- **The lock rule:** every ref write needs `.push-lock-d8` HELD by you, the four WAITs absent and no unattributed lock. Ref writes: worktree add/remove, commit, merge-in, push, merge, a ruled object transfer.
  - **Push tools take the lock ITSELF: call them BARE** (`:373`). Never pipe a lock take. Hold it short: never across `npm ci`, a build or a suite.
  - Attribute every lock by its holder `seat` field (`:408`).
- **Matcher re-key (trap 4, both halves, `:400` `:407` `:411` `:413`)** on `inbox_matchra1.py`: `MINE = "r 2nd"` BY HAND (R 1st handover `:127`-`:129`: the map carries no seat token); `OTHER_SEATS` ADDS `"r 1st"` (predecessor) and `"r 3rd"` (successor), and co-tenants `"e 8th"`, `"e 7th"`, `"e 9th"`, `"b 67th"`, `"b 68th"` if absent; remove `"r 2nd"`. Prove on REAL subjects from the API: R 1st's own READY / WRAP reads FOREIGN; `GO (Seat E 8th): merge 1396 on gate69` on the `-E` tag reads FOREIGN; a constructed `(Seat R 3rd)` reads NOT FOR ME; `GO (Seat R 2nd): merge 1395 on gate69` on the `-R` tag reads FOR ME; an untagged `(Seat R 19th)` exercises the `_addr is None` clause; the DEFECT A 2x2 (`:413`). Fixtures pinned as WHOLE tuples.
- **`namecheckra1.py`:** TWO namespaces, as E 7th's handover §1 describes for lane E. Your SEAT token is `ra2` (new branches `feature/ks-<n>-<slug>-ra2-<k>`, worktrees `s-ra2-*`, `refs/seatra2/`), but you ADOPT ONE `ra1` ref and ONE `ra1` worktree for the merge. `MINE = "ra2"`; `ra1` moves to FOREIGN except the declared adoption. Controls on REAL names: the four `…-l3-r1-1` refs read NOT MINE; `s-e6-ks1256`, `s-b63-ks1278` read FOREIGN; a planted `s-ra2-x` / `-ra2-9` read MINE; the adopted `…-ra1-1` reads ADOPTED, and pulled out of the adoption it must read FOREIGN, never MINE.
  - Token `ra2`: 0 raw / 0 bounded over 2,092 origin refs, 0 bounded in `history.md`, 0 `s-ra2-*` worktrees (P13).
- **ADOPTIONS (Q-ADOPT2, pre-ruled: yes):** exactly ONE ref, `feature/ks-1305-prisma-not-generated-diagnosis-ra1-1`, and ONE worktree, `s-ra1-ks1305`, by EXACT name. At draft: HEAD `1bdfbe0f2f06` ON that branch (not detached), porcelain 0, dist/index.js, `Blockchain/Dev/node_modules` and `systemTest/akto/node_modules` present, `services/originate/node_modules/.prisma` ABSENT (the KS-1305 condition itself), pre-push `test -x` rc 0 (P12).
- 🔴 **STALE KNOBS (`:405`).** List every knob with its value BEFORE any run. Measured at draft (P11):
  - `mergera1.py:113`-`:118`: env name `MERGE56_SCRATCH` (a B-generation name) with a DEAD default (`…/4f1e7e2b-…/scratchpad/s-b65`). Set it to YOUR scratchpad and say the name you set.
  - `mergera1.py:194`-`:195`: its "never fetches" refusal names `.push-lock-56` (the B lane's). Your lock is `-d8`. Re-key the text; it changes no logic.
  - `mergera1.py:112` sets `GIT_SSH_COMMAND` in the TOOL's own subprocess env for its git reads; it never pushes. Do not export it in YOUR shell (`:412`).
  - **There is NO merge-in tool in R 1st's folder.** Copy B 66th's ORIGINAL `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatB-66th/raise/mergein66.sh` (13,248 B, sha256/16 `ad2b0e28cb498a22`; B 67th's copy differs, `a675a1330be808d8`, so do NOT copy B 67th's) as `mergeinra2_1395.sh`. Its eleven knobs are REQUIRED arguments (`:27`-`:32`). Its MERGE stage asserts `merge rc 1` (`:110`) and `exactly TWO conflicted files` (`:111`), which is the shape predicted for you. **Re-point its two `lock56.sh` calls (`:88`, `:93`) to YOUR `lockra1.sh`**, nothing else, and drive one wrong-value arm per changed line.
  - `raisera1.py`, `commitra1.sh`, `pathgatera1.py`: every per-PR value is a required argument (R 1st rewrote `pathgatera1.py`; `commitra1.sh`'s file-count arm must be passed).
  - Grep every string literal for 36-char UUIDs and `/private/tmp/` paths, print the count checked; AST-parse every `.py` with ok/fail counters; `$LOG` = `$REC/boot` first.

## ITEM 0 — plan confirmation (QUESTION `plan confirmation (Seat R 2nd)`). STOP until Wednesday's ANSWER.
Before the ANSWER, do NONE of these: lock take, fetch into the shared store, objects transfer, worktree add or write, ref write, install, ticket write, comment, PR edit. You MAY write inside your own record folder and YOUR scratch clone.

ITEM 0 carries:
- **Refs by `ls-remote`, instrument named:** develop, `refs/pull/{1383,1393,1395,1396}/head`, the `…-ra1-1` branch. At draft (01:22:18Z-01:22:25Z, P7): develop `4eaf7741a6a4`; `/1395/` == branch == `1bdfbe0f2f06`; `/1396/` `e6eb53fe2658`; `/1393/` `b5adaba751d8`; `/1383/` `32e8459bc0f5`. Identify develop by `git log -1` and its PR; it must equal `@DEVELOP_LAUNCH@`.
- **YOUR scratch clone, the `:406` way:** `git clone --shared --no-checkout /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files <scratch>/vclone`; `git remote -v`; fetch BY SHA (`@DEVELOP_LAUNCH@`, `1bdfbe0f…`, `e6eb53fe…`, `3f9ff4e1…`) from `git@github.com:Secuura/Distributed_Secuura.git` with `-c core.sshCommand="$(git -C <checkout> config --get core.sshCommand)"`, `--no-tags --no-write-fetch-head`; `cat-file -t` each plus the `deadbeef…` control; the shared `rev-parse --all` sha256 identical before and after. Shared-store census of `@DEVELOP_LAUNCH@` in the same call (at draft even `4eaf` was ABSENT, P12).
- **🔴 THE #1395 PREDICTION, provisional.** The gate69 kit BY PATH from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate69/`, sha256 == `kit.json` `script_sha256` (equal at draft, P4): `c4_docs_gate69.py` `aafe62fef4a410be…`, `lib_gate69.py` `4cee5441ff0a97f3…`, `composee5_copy.py` `f9ab42d9fc25f189…`, `gh_gate69.py` `21291d1b266daca9…`. `G69_SCRATCH=<your scratch>/g69`. **Never `--repo` inside `!CODING`.**
  - run 1: `python3 …/c4_docs_gate69.py chain --repo <clone> --pr A --head-a 1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660 --head-b e6eb53fe26587bc8375154a6acfd112ddea58278 --b-pr 1396 --develop-after @DEVELOP_LAUNCH@`. Its "A on SIM squash(B)" line is your provisional `@T1395@`. Mail it as PROVISIONAL; the real one is computed on `@DEVELOP_1396@` at M-track.
  - run 2 (control): the same `chain` on `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe` must reproduce gate69's `883d4b70343c` (B then A) and `37773febc715` (A alone).
  - run 3 (control): `predict --pr A --head 1bdf… --develop-after @DEVELOP_LAUNCH@ --order wrong` must print READ-BACK FAIL. 🔴 **Read the READ-BACK lines, not the rc: `predict` exits rc 0 whenever it wrote a tree** (`c4_docs_gate69.py:543`; measured rc 0 with both read-backs FAIL, P10).
  - Kit sha256 the same before and after.
- **The ADOPTED worktree, read WITHOUT writing** (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra1-ks1305`), the figures in ADOPTIONS.
- **The PR as it stands** (`GET /pulls/1395`): state, head, mergeable_state, title (chars), body bytes / chars / sha256. At draft (P8): open, `1bdfbe0f2f06`, `false / dirty`, 77, 8,891 / 8,839, `e3e2ba5f26d1e033`.
- **The #1395 squash body, re-scanned on YOUR copy** (THE SQUASH BODY).
- **The raise plan, re-measured at `@DEVELOP_LAUNCH@`** (the R-track's inputs):
  - each held payload's sha256 and size (P14): KS-1136 `…_KS-1136-aggregate-unreadable-artefacts/out.md.checker/patch.diff` 10,960 B `7c38ea016b155074`; KS-998 `…_KS-998-format-gate-grep-fixed/…` 5,599 B `a4905e4da54a6cf7`; KS-1313 `…_KS-1313-child-verdict-json-reporter/…` 9,252 B `59f5d73d68df586d`; KS-1164 `…_KS-1164-locale-count-cell/…` 4,643 B `5c5e586406ebe4b1` (run dirs under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_`); each REVIEW `VERDICT: HOLD`;
  - each STRICT apply at `@DEVELOP_LAUNCH@` in YOUR scratch clone (`read-tree` into a temp index, `git apply --cached --check`, then apply) with ONE tamper control that must fail (raise brief P6 method);
  - `git diff --name-only 3f9ff4e1e1b9 @DEVELOP_LAUNCH@` against the four product paths: 0 expected.
- **🔴 The Spark goldens are NOT evidence for KS-1136 or KS-998** (Wednesday's relay at draft, from a parallel Spark drafter at ~12:2x AEDT; UNMEASURED by this drafter): `bash_patch` goldens must not carry `diff --git` / `index` header lines, because the checker reads them as garbage on the previous file's section, and those two goldens carry such lines, so `round.sh --control` on them may FAIL for a reason that is the golden's, not the payload's. **Do not cite a golden `--control` run as evidence for either PR**, unless you strip those header lines first and say so in the evidence line. Your evidence is your own red-first and suite runs at your base. The `patch.diff` payloads themselves carry 0 such header lines (P14).
  - ⚠ **A contradiction for Wednesday to rule (Q-SRC2):** the relay also said to raise "from the READY_ diff files (as R 1st did)". Measured at draft: **no `READY_` file dated 2026-10-0x exists for any of the four** (the matching `READY_KS-1136…` / `READY_KS-1164…` files are dated 2026-09-15 to 2026-09-22, earlier rounds), and R 1st applied the run dir's `out.md.checker/patch.diff` (raise brief ITEM 1 `:283`; R 1st handover `:22`-`:25`). **This brief raises from `patch.diff` (the HELD payload) until Wednesday rules otherwise.**
- **Matcher / lock block** titled `ra2 on d8: 56 + e4 + f3 + g1 WAIT, 16 STOP, catch-all, foreign-holder rc 12, DEFECT_A 2x2 (Seat R 2nd)`: the arms above with controls each way; `twolockra1.sh` arms with counts (`0 checked` is a FAIL), driven in a SCRATCH copy of the worktrees dir only; the real `.push-lock-*` population attributed by holder `seat`, two readings a poll apart; the `:414` parity; the re-key receipt; the STALE KNOBS list before / after.
- **The project skill quoted from `@DEVELOP_LAUNCH@` with its blob id** (blob `eaf43dfd4d98…` at `4eaf` and in the simulated post-#1393 tree, P15): §4 (`:360`), review authority (`:30`-`:36`, systemTest -> Peter's comments take precedence), §5b, §5c (400-line cap), §5d (`:507`), §5e (`:518`), §5f (`:540`).
- **Read-only Linear re-reads:** KS-1305, KS-1136, KS-998, KS-1313, KS-1326, KS-1164 (state, assignee, project, `archivedAt`, newest comment sorted client-side, attachments). Name anything that contradicts LINEAR below.
- **The open-PR census** for the four raise paths and the five keys + KS 1326 (raise brief P9 tool `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-05_spark-screen/prs.py`, positive control `package.json`).
- **Also:** the watchers from a ps FILE (yours by ancestry; R 1st's, if any survives with ppid 1, named and left); `$TMUX_PANE`; `df -m /Volumes/DevMASTER` (695,285 MiB free at draft); every launcher preflight warning VERBATIM; the usage gate; your ctx; your restatement of the QUESTIONS.
- **QUESTIONS** (each pre-ruled answer stands unless your measurement contradicts it; then say so and HOLD that item):
  - **Q-LOCK2: yes. Q-ADOPT2: yes. Q-NAME2: yes** (Seat R 2nd, token `ra2`, tools generation `ra1`).
  - **Q-BASE2 (PROPOSED; Wednesday rules `@RAISE_BASE@`):** build PRs 2-5 as SIBLINGS on ONE base, the develop at the ANSWER. Each will need a docs-only merge-in after every later landing, covered by its gate only under Q-M. The alternative is to wait for #1395 to land and build on that develop (fewer merge-ins, later start).
  - **Q-MI2: yes,** conditional on the M-track mergetree run matching: `mergeinra2_1395.sh` as in STALE KNOBS, resolving BY CONTENT to the TAIL blobs (`git show @T1395@:<doc>`), STAGED blob ids asserted, `tree(M) == @T1395@`, parents `[1bdfbe0f…, @DEVELOP_1396@]`, 0 trailers, all before any push.
  - **Q-SQ2: confirm the #1395 squash body below.**
  - **Q-SRC2:** the payload source (above).
  - **Q-5F2 (PROPOSED, NOT pre-ruled):** after the merge, ONE `§5f` comment on KS-1305: `Merged <sha> (PR #1395, db.ts); offline gates green; NOT Done per secuura-test-discipline §5f — live sweep owed (torn-down rebuilt stack, all containers verified up), unverified: real PostgreSQL / RLS / multi-tenant; Prisma 7.10`. Posted only if ruled yes.
  - **Q-1326 / Q-A / Q-TIER / Q-N:** carried as ruled (above); restate them.

## THE GO (M-track)
- **The GO is gate69's** (P1 `:5`): `GO (Seat R 2nd): merge 1395 on gate69`, at head `1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660`.
- **Act on it only when a Wednesday mail whose subject carries that exact string reaches you** (addressee you, tag `-R`, spf/dkim/dmarc = pass) **AND it carries `@DEVELOP_1396@` and `@T1395@` AND it states that #1396 has merged.** Wednesday sends it after E 8th's `STATUS: merged 1396`. A GO that arrives while #1396 is unmerged is a STOP-and-mail.
- It covers a docs-only merge-in M ONLY if `qm --pr A` passes M1-M8 on the real develop (P1 `:1`), and Actions on M read NEW-FAILING NONE (or each failure classified pre-existing from its log, Q5) and PENDING NONE (P1 `:29`).
- **Before the merge, confirm that no live lane holds a signed GO pinned to the develop you would move** (R 1st handover `:96`-`:98`). At draft only #1393 and #1396 were in that position, and both merge before you.

## QUEUE
**R-track (from the ANSWER on; one PR at a time; ONE commit each).** Per PR, the raise brief's own item (`:290`-`:316`) stands, with these changes:
- **Base:** `@RAISE_BASE@`, not `3f9ff4e1e1b9` or `22b268143a63`. Bring it into the shared store by the `:404` objects-only transfer under the lock if absent. Worktree `git worktree add --detach /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra2-ks<n> <@RAISE_BASE@ full sha>` (absolute path, full SHA, never `-b`), then the branch `feature/ks-<n>-<slug>-ra2-<k>` at commit time.
- **Fresh worktree:** `npm ci --ignore-scripts` in `Blockchain/Dev`, then `npm run build --workspace=packages/shared`; ASSERT `dist/index.js` before the first test (`:376`, `:396`); the systemTest packages each PR's push will select, outside the lock (`:410`).
- **Doc blocks:** `23.` / `24.` / `25.` / `26.` + KS-keyed cheat sections at the TAIL of `@RAISE_BASE@`'s docs, read with the NEWLINE-TOLERANT reader and its planted control (`:409`). Never edit an existing block (`15.` `16.` `20.` `21.` `22.` included).
- **ITEM R2, KS-1136 (T1):** raise brief `:290`-`:297`. 🔴 The exec bit on `09-aggregate-report.sh` (100755): `[ -x ]` on disk after the apply, `chmod 755` that file only if `git ls-files -s` shows 100755, bytes `cmp`-unchanged; never `checkout-index -a` (`:259`-`:261`, `:355`). Prove `run-shell-suites.sh` discovers the new test (count +1). The guard is fail-closed on unreadable artefacts: one red arm per conjunct if it is a conjunction (`:253`). Body: `Refs KS-1136`, item 2 (R-3) only; item 1 merged as #1051; §5f `live sweep owed`.
- **ITEM R3, KS-998 (T2):** `:298`-`:303`. Peter's review authority (systemTest). **This PR's own push runs the gate it changes**: quote that push's gate lines. Wednesday may order its MERGE after the live lanes' pushes (raise brief DEFECT 6).
- **ITEM R4, KS-1313 + KS 1326 (T2):** `:304`-`:310`, per Q-1326. Credit #1245 by blob (the card's text is in RULED BY KAM above).
- **ITEM R5, KS-1164 (T2):** `:311`-`:316`, red BY TAMPER with a unique anchor and a sha256 restore (`:190`-`:215`).
- **ITEM R6, PUSH / RAISE / ONE READY** (`:317`-`:334`), with whatever PRs are built:
  - predict each PR's TAIL tree on the develop of that moment with the gate69 kit's method (or a kit Wednesday names), in YOUR scratch clone;
  - push each ONCE with `pushra1.sh` BARE under `env -u GIT_SSH_COMMAND` (`:412`); result = the `.rc` file + `ls-remote` (`:401`);
  - raise by REST: HTTP 201, head == origin, body sha256 read back (R 1st handover: `raisera1.py`; E 7th's `restraisee7.py` is the lane-E equivalent, not yours);
  - bodies: own key hyphenated once + URL; every other key de-hyphenated; Test Evidence by you; "raised from Wednesday-held Spark passes (round 1, PASS 7/7), re-proved by Seat R 2nd"; **no golden `--control` as evidence**;
  - ONE READY: `READY FOR QA (Seat R 2nd): #<a> (KS-1136) + … -> gate<NN>` (Wednesday names the gate; it is NOT gate69). Each head and develop read from origin in the same action; per PR: tier, END_TREE, trailer proof, pathgate with its firing control, the §5f lines, the lock census, the usage gauge.
- **If the GO arrives mid-PR:** finish the commit you are on (or stop before starting it), release nothing you do not hold, and switch to the M-track. Record the R-track state in a STATUS mail first.

**M-track (on the GO mail).**
1. **ITEM M1: the merge-in, under the lock.**
   - Re-read develop at origin: it must be `@DEVELOP_1396@`, and `git log -1` must show #1396's squash (subject `KS-1256: an unreadable connector allow-list fails closed with 503 (#1396)`). Otherwise STOP and mail.
   - **Second hand, in YOUR clone** (fetch `@DEVELOP_1396@` by SHA first): `predict --pr A --head 1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660 --develop-after @DEVELOP_1396@` must print `PREDICTED @T1395@`, both READ-BACK OK, flow tail `… 20 21 22`, cheat tail `… KS-1256 KS-1305`. `--order wrong` must print READ-BACK FAIL (read the lines, not the rc). `mergetree --pr A …` must show rc 1, TWO conflicted paths, the cheat's "THEIRS then OURS" `== tail-predicted blob: False` with `READ-BACK OK` (the M8 trap), and DIVERGENCE. **A different tree or shape: STOP and mail `QUESTION: merge-in 1395 predicted tree <T> (Seat R 2nd)`.**
   - If `cat-file -e @DEVELOP_1396@^{commit}` fails in the shared store: the `:404` objects-only transfer from YOUR clone; `rev-parse --all` sha256 byte-identical before and after; `.git/config` unchanged.
   - Re-read `s-ra1-ks1305` WITHOUT writing: HEAD `1bdfbe0f2f06`, porcelain 0.
   - Run `mergeinra2_1395.sh` ONCE with its eleven arguments, each named in a STATUS mail first: `--wt /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra1-ks1305`, `--br feature/ks-1305-prisma-not-generated-diagnosis-ra1-1`, `--ours 1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660`, `--dev @DEVELOP_1396@`, `--base 3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f`, `--predicted-tree @T1395@`, `--subj 'Merge develop <12-hex> into the KS-1305 branch (docs-only)'`, `--vclone <your clone>`, `--flow-blob <TAIL flow blob>`, `--cheat-blob <TAIL cheat blob>`, `--control-commit bf277eead268`. It resolves BY CONTENT to the key blobs and asserts the STAGED blob ids; **never accept a hand reading; never take OURS or THEIRS**; 0 trailers measured against `bf277eead268`, naming the instrument (53 / 55); `tree(M) == @T1395@` and parents `[1bdf…, @DEVELOP_1396@]` BEFORE the push.
   - **`qm`:** `G69_SCRATCH=… python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate69/c4_docs_gate69.py qm --repo <clone> --pr A --head 1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660 --merge-in-head <M> --develop-after @DEVELOP_1396@`. `cat-file -t M` in your clone first. **Not 8/8 = NO PUSH: STOP and mail.**
   - **The originate suite at M, in `s-ra1-ks1305`, outside the lock** (the #1393 adjacency): jest by named binary, files / tests / failed counted, the generated client absent as at the gate. Expected: gate69's 91 / 1,067 plus #1393's originate cells (ks1278 + ks1293). **Any red that is not red at `@DEVELOP_1396@` is a STOP.** Never `prisma generate`.
   - Before the push, read `:396`, `:410`; install any package the format gate SKIPs, in the worktree, outside the lock. Never `--no-verify`.
   - Re-read develop at origin in the SAME action as the push decision; if it moved, do not push.
   - Push with **`pushra1_ff.sh` BARE**: `env -u GIT_SSH_COMMAND bash <REC>/raise/pushra1_ff.sh /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-ra1-ks1305 feature/ks-1305-prisma-not-generated-diagnosis-ra1-1 1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660` with `LOCK_SEAT` exported (`pushra1_ff.sh:82`-`:84`). Result = `.rc` + `ls-remote` (`:401`); rc 141 with the ref unmoved = KS-1149 class (retry under the lock, report time + attempts). Quote the preflight ratio EXACTLY; 12/15 accepted for this DOCS-ONLY merge-in only, and you say so.
   - **Actions on M:** `python3 …/gh_gate69.py actions --at <M> --prev @DEVELOP_1396@`, planted-name control reported. Expected NEW-FAILING `Security Scanning` with the pre-existing `Cannot find package 'semver' imported from …/scripts/audit/audit-locks.mjs` cause (P1 `:100`-`:104`): **read the job log of EVERY new failure and quote the line.** Same cause = named, not blocking; any other = STOP. PENDING = wait.
2. **ITEM M2: the squash merge, same GO, after M is at origin and Actions are clear.**
   - The addendum for `mergera1.py`, built by a SCRIPT from git and API reads (copy `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-06_seatB-67th/raise/build_addendum66_1394.py` as `build_addendumra2_1395.py`, or B 67th's `build_addendum67_1393.py` if it exists by then; every regex re-derived from report `:553`, exactly-one-match, cross-checked against your git read, refusing by name):
     - `base_go` = `expect_develop` = `@DEVELOP_1396@`; `prs["1395"].head` = **M**; `merged_tree` = `@T1395@`;
     - `targets` = `{path: [blob, mode]}` for the 4 PR paths from `git ls-tree M`, equal to `GET /pulls/1395/files` (`mergera1.py:240` refuses otherwise);
     - `subject` = `KS-1305: diagnose a missing generated Prisma client instead of a module error`;
     - `own_keys ["KS-1305"]` (the PR body's own `Refs KS-1305` must agree, MG-3);
     - `no_trailer: true`; `body_verbatim` = THE SQUASH BODY below;
     - `merge_note` = `Merged by Seat R 2nd on the authority of HANDOVER-seatR1-2026-10-05.md sha256 a66399885d8abab5`, `wrap_artefact` = `HANDOVER-seatR1-2026-10-05.md`. **Re-measure the sha256 prefix in the same call that writes the addendum;** different = STOP and mail.
   - 🔴 **The tool APPENDS the note:** `body = body_verbatim.strip() + "\n\n" + merge_note + "\n"` (`mergera1.py:457`). The pre-written body carries NO `Merged by`; the sent body carries exactly ONE. If your copy composes it differently, the tool wins: tell Wednesday.
   - `mergera1.py --dry` first (`--seat 'Seat R 2nd'`, `--gate gate69`, `--go-ts <GO mail ts>`, `--expect-develop @DEVELOP_1396@`, scratch env set). READ the `.DRY` body: subject byte-equal (77, lands 85); body == `body_verbatim` + blank + note; the scan below re-run on the SENT body.
   - Merge with the head PINNED to M. Verify by `ls-remote` AND the API: tree == `@T1395@`, ONE parent == `@DEVELOP_1396@`, 0 trailers, exactly the 4 paths.
   - **Re-read KS-1305: still In Progress.** Done = STOP and mail at once.
   - Mail `STATUS: merged 1395 (Seat R 2nd)` (squash sha, tree, parent). Then return to the R-track if ctx allows.
3. **ITEM M3 (residue, drafts only; file nothing without the ANSWER):** gate69's N-1395-1 (the MESSAGE conjunct matches the Require stack; fix shape: match the FIRST line of the message), N-1395-2 (order-dependent cells; `jest.isolateModules`), N-1395-3 (no cell asserts `cause`). They are ONE test pass on one file plus one guard line: **ONE ticket** text, searched first BY SYMBOL (`.prisma/client`, `getPrismaClient`, `isolateModules`), in `QUESTION: residue texts (Seat R 2nd)`. N-1395-4 ("three-term conjunction" in both committed docs) is a docs line for the same ticket.
4. **ITEM M4 (optional, NOT on the critical path; only if ctx allows after M2):** a separate, unticketed bug relayed by Wednesday from the Spark drafter (UNMEASURED by this drafter beyond one read): **`Blockchain/Dev/scripts/dev-reload.sh:73`** reads `echo "▸ [3/3] restart $CONTAINER…"` (blob `f74b7aee6833…` at `4eaf`, under `set -euo pipefail` at `:21`); the claim is that bash 3.2 in a UTF-8 locale takes the bytes of `…` into the variable name, so `set -u` aborts with an unbound variable. **Search first BY SYMBOL** (`dev-reload.sh`, `$CONTAINER`, `unbound variable`) and say what you searched (`:98`-`:100`). KS-1355 (Todo) holds `dev-reload.sh`'s SLOT-container defect (`:45`); the Spark brief for it names `:73` as "a separate defect, not this brief" (P16): **cross-reference KS-1355 in the text, de-hyphenated in a title, and file ONE ticket on the board account** with a reproduction you RAN (`LANG=en_US.UTF-8 bash dev-reload.sh <svc>` against a stub, and the `LC_ALL=C` control), or say the reproduction is unmeasured. Its fix shape (`${CONTAINER}…`) is a candidate Spark task, not yours to build.
5. **WRAP** (MAIL FORMATS).

## THE SQUASH BODY (Q-SQ2, #1395). Pre-written by Wednesday's drafter from 1bdf's message, gate69's findings and its rows
Subject (passed separately): `KS-1305: diagnose a missing generated Prisma client instead of a module error`

The body is the text between the fence lines, ending in ONE newline: **2,543 B / 2,543 chars, 47 lines, sha256 `0fa8232f5abba4cc7d0b81b7e0a32a3459be4138a75ffd4b0cb6942c759a2b75`.** Copy it into `<REC>/squash_body_1395.txt` with a QUOTED heredoc and re-hash it.
```
A fresh worktree installs @prisma/client but never generates it (npm ci
runs with --ignore-scripts, so prisma generate does not run), and
getPrismaClient() in originate src/db.ts then threw "Cannot find module
'.prisma/client/default'", which reads like an originate defect. The
first load now names the cause and the generate command, and keeps the
original error as its cause. This is shape (3) of the ticket only; shapes
(1) and (2) are deferred by ruling, so the ticket stays open.

The guard is two conjuncts, code MODULE_NOT_FOUND and a message that
names .prisma/client, plus a same-object rethrow for everything the
guard does not match. One red tamper per conjunct, measured by gate69:
dropping the message test reds C1; dropping the code test reds C3;
rethrowing a new Error reds C1 and C3. A missing @prisma/client package
is rethrown unchanged (gate69, at runtime). Precision gap, measured by
gate69: the message test also matches .prisma/client in the Require
stack, so a PRESENT generated client whose own dependency is missing
gets the same "missing" sentence; its cause still carries the real
error.

db.ts is the tenant-isolation module. The change is one pure insertion
(numstat 19 0, inside getPrismaClient); gate69 measured that no GUC,
tenant or RLS line changed (all 96 develop tenant-regex lines unchanged)
and that the six KS 458 tenant-GUC cells are byte-identical and green.

Test evidence, measured by gate69 at 1bdfbe0f2f06:
- in a real fresh npm ci --ignore-scripts worktree the real error is
  MODULE_NOT_FOUND for '.prisma/client/default', both conjuncts fire on
  it, and the head db.ts returns the new sentence with that cause
- red-first against develop's db.ts: D1 red, 1 failed / 9 passed;
  head 10/10
- originate suite 91 files / 1,067 tests, 0 failed, jest 29.7.0,
  node v24.7.0; tsc rc 0
- tamper: dropping the cause leaves every cell green (no cell asserts
  the cause); the cells are order-dependent under jest --randomize
  (C2 sets the module-level client), green in declaration order
- in-hook preflight at the author's push, quoted and not a pass:
  PREFLIGHT INCOMPLETE, 12/15 legs ran (stack down)

Raised from a Wednesday-held Spark pass (round 1, PASS 7/7), re-proved
by Seat R 1st, who added the control cell C3.

NOT COVERED: no live sweep, so this change does not move its ticket to
Done (secuura-test-discipline 5f). No real PostgreSQL, RLS or
multi-tenant run; no withTenant cell against a database. Prisma 7.10
(#949) was not run.

Refs KS-1305 https://linear.app/secuura/issue/KS-1305
```
**The drafter's scan (P15). Re-run it on the body you SEND:** strict closing regex `\b(close[sd]?|fix(e[sd])?|resolve[sd]?|complete[sd]?)\b\s*:?\s+(#\d+|KS-\d+)` **0** (controls `Closes KS-1256` -> 1, `fixes: #12` -> 1); closing-family words ANYWHERE **0**; 0 within 3 lines above `Refs`; hyphenated keys only `KS-1305` (x2); `KS 458` de-hyphenated; 0 `Co-Authored-By`; 0 `Merged by` (the tool adds ONE); 0 "three-term"; ASCII only; longest line 73.

**Drafter's choices you may challenge at ITEM 0:**
- (a) The body corrects 1bdf's message where gate69 found it false: "three-term conjunction" (N-1395-4) becomes "two conjuncts plus a same-object rethrow", and "every other load error is rethrown as the same object" (N-1395-1) becomes the measured precision gap.
- (b) The gate's "is now covered" real fresh-worktree MODULE_NOT_FOUND is carried into the evidence (P1 `:150`), so it is not repeated in NOT COVERED.
- (c) `#949` is a PR reference with no closing word before it.

## THE PROJECT RULES THAT TOUCH THIS SCOPE (quote each from develop with its blob id at ITEM 0)
- **§4** both platform docs in the SAME commit as each test change (systemTest counts); timings STATED with the base grep and a must-hit control; each suite's figure with DATE and HOST.
- **Review authority `:30`-`:36`:** PRs 3, 4, 5 are `systemTest/`: Peter's comments take precedence; each body says so. Nothing goes to Peter or Stuart.
- **§5c** systemTest files under 400 lines (ESLint `max-lines`, or UNMEASURED). **§5d** WHY + ticket on every changed line; the PR's own ticket URL in each body. **§5e** nothing beyond what this brief instructs. **§5f** runtime changes (KS-1305, KS-1136): `live sweep owed`, nothing to Done.
- **No `Co-Authored-By`, no tool trailer** on any commit, merge-in or squash (`:371`).
- Repo `CLAUDE.md` / CONTRIBUTING: squash into develop; a branch behind develop gets develop merged INTO it; no force push (`:395`).

## HOLDS / KAM'S, NOT YOURS
- **No merge without the signed `GO (Seat R 2nd): merge 1395 on gate69`** carrying `@DEVELOP_1396@` and `@T1395@`, after #1396 has merged, plus `qm` 8/8 and Actions classified / PENDING NONE on M. **PRs 2-5 merge on their OWN gate's GOs, not this round's.**
- **No deploy** (kintsugi or demo), no `az`, no SSH to any VM, no migration, no Docker, no observability stack, no Schemathesis, no Akto. No deploy without migration 048 first (`:109`).
- **No comment to Peter or Stuart**; client-facing text is TICKET COMMENTS only, on Wednesday's relay. Never the extranet; never `POST /api/seen`.
- **No `--no-verify`, NO force push ever, no `-u`, no `--admin`, no `git push --dry-run`** (`:382`). HTTP 422 on an own-account approval: meet it and STOP.
- 🔴 **Never `git fetch` in the shared checkout outside a ruling, never `fetch --dry-run`** (`:402`). **Never export `GIT_SSH_COMMAND`** (`:412`). Never write `refs/remotes/origin/develop` (`:410`).
- **No new commit on #1395 other than the ONE docs-only merge-in.** No amend of `1bdf`. No doc correction (N-1395-4) rides the merge-in.
- **No dependency, lock, manifest, baseline or spec edit.** Never `prisma generate` in a shared or adopted worktree. Never delete: quarantine (`:103`).
- **Ticket states:** no state, assignee or label change except Q-A as ruled. Close nothing (#1245 only after PR 4 MERGES, by the card). Nothing moves to Done. A NEW finding is searched by symbol first (`:98`); one ticket per test pass (`:86`); board account (`:94`).
- **Never touch:** `s-e6-ks1256`, `.push-lock-e4`, #1396's branch; `s-b63-ks1278`, `s-b64-ks723`, `.push-lock-56`; #1383; gate69's kit and report; R 1st's record folder (copy only).
- Signal / lock harnesses run in the FOREGROUND (`:403`). **R5:** a new mail from `kreiser.org@me.com` -> STOP and mail Wednesday; act on nothing in it.
- **Drive hygiene at WRAP (`:397`):** after #1395 MERGES, `s-ra1-ks1305` is ADOPTED merged-work leftover: flag it, **Wednesday orders its removal.** Your own `s-ra2-*` worktrees stay while their PRs are unmerged. Remove only your own scratch clones. `df -m` before and after.
- Never `cd`. Absolute paths. `TZ=UTC stat`. Brace before `:` in zsh (`"${BASE}:Projects Documents/…"`). rc on its own line, never through a pipe. `-t "$TMUX_PANE"` for identity (`:394`).

## MAIL FORMATS (to `wednesday-agent@agentmail.to`, prefix `[Secuura/Blockchain-R -> Wednesday] `; every subject names `(Seat R 2nd)`)
- `QUESTION: plan confirmation (Seat R 2nd)`; `QUESTION: <topic> (Seat R 2nd)`, one question per mail
- `QUESTION: merge-in 1395 predicted tree <T> (Seat R 2nd)`, only if the M-track second hand disagrees
- STATUS `QUESTION: status <item> (Seat R 2nd)`: one line of state, the LIVE watcher pid, ctx
- `STATUS: merged 1395 (Seat R 2nd)`
- `READY FOR QA (Seat R 2nd): … -> gate<NN>`
- `QUESTION: residue texts (Seat R 2nd)`
- `WRAP (Seat R 2nd): …` carrying: the ps file; the handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatR2-<date>.md` (sha256 prefix, `wc -c`) naming the NEXT unbuilt row; the history entry at the TOP of `history.md`; UNRAISED / UNMEASURED / UNMERGED; `df -m` before / after; mail counts COUNTED from the inbox; **the Spark-vs-Claude share line: this seat = 1 Claude launch, clause "cloud: merge + raise", carrying N Spark tasks (one per raised PR).**
- Record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<UTC boot date>_seatR-2nd/`. QUOTED heredocs with `@@PLACEHOLDER@@` substitution; body size > 0 asserted; every send's response read back; every mailed figure computed in the SAME call that sends it.

## LINEAR (read-only at draft, P9)
- KS-1305: In Progress, kamil.kreiser@secuura.ai, project Internal tooling, updatedAt 2026-10-06T00:13:05.089Z, archivedAt none, 0 comments, attachment `pull/1395`.
- KS-1136: In Progress, board account, Internal tooling, 1 comment (2026-09-18), attachment `pull/1051`.
- KS-998: Backlog, board account, Internal tooling, 1 comment (2026-09-25), 0 attachments.
- KS-1313: In Progress, **UNASSIGNED**, Internal tooling, 4 comments (newest 2026-09-26), attachment `pull/1245`.
- KS-1326: Backlog, board account, Internal tooling, 2 comments (2026-09-26), 0 attachments.
- KS-1164: In Progress, board account, Internal tooling, 3 comments (newest 2026-09-25), attachments `pull/1271`, `pull/1200`.
- KS-1256 (#1396, E lane): In Progress, attachment `pull/1396`. Partition only.
- None is on Peter or Stuart.

## UNMEASURED (not provenance)
- `@DEVELOP_1396@` and `@T1395@`: neither #1393 nor #1396 had landed at draft; only the SIMULATED figure exists (P10).
- Whether the real merge shape over #1396's squash matches the simulated one (both docs conflicted; the cheat's THEIRS-then-OURS trap).
- `qm` on a real M; Actions on M; the originate suite at M with #1393's cells in it.
- The golden `--control` defect on KS-1136 / KS-998 (relayed, not measured here); the `dev-reload.sh:73` abort (one line READ, never run).
- Whether the four payloads still apply STRICT at `@RAISE_BASE@` (they are byte-unchanged in the product files through the simulated chain, P10, but the apply was not re-run).
- How many PRs this seat's ctx allows. Your ctx and pane id. Whether R 1st edits its handover after 00:20:13Z.

## RESOLVED (Wednesday's drafter, before staging)
- **Head as read: `1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660`** (== branch == pull head; local ref equal; P7, P12).
- **The conditional chain** on simulated develops: #1393 TAIL `0b4c3a265454` reproduced with gate68's kit; #1396 TAIL `cee3fc991319…`; #1395 over it `3e708d1191ad…`; merge-tree DIVERGENCE with both docs conflicted and the cheat trap reproduced (P10).
- **The raise inputs pinned:** four `patch.diff` sha256 equal to the raise brief's P4; the four product blobs unchanged `3f9f` -> simulated develop; token `ra2` clean (P13, P14).
- **Squash body pre-written and scanned** (P15).
- **Carried to Wednesday:** fill the placeholders; send the GO with `@DEVELOP_1396@` / `@T1395@` after E 8th's STATUS; rule Q-BASE2, Q-SRC2, Q-5F2; name the raise gate; order the removal of `s-ra1-ks1305` after the merge; the kit defect (predict's rc ignores the read-back).

PROVENANCE:
- P1 gate69 verdict mail, 155 lines: GO lines `:1`-`:2`; GO strings `:4`-`:6`; pins `:9`-`:13`; merge-in on 4eaf, the order and "second PR re-predicts" `:15`-`:23`; divergence `:24`-`:28`; Actions `:29`; subjects `:31`-`:34`; #1395 rows `:41`-`:51`; tamper `:74`-`:81`; cell order `:90`-`:93`; Security Scanning `:100`-`:105`; findings `:109`-`:112`; census `:140`; NOT TESTED / moved out `:142`-`:150` | Read whole `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_mail_g69.txt` | read 2026-10-06
- P2 gate69 report, 554 lines, sha256 `19d2167db31f504c555e90e338057f34c7f567510e2af47b8ad4345d3c94fd2c`; #1395 C1 `:82`-`:93`; C2-A `:114`-`:136`; C3-A `:170`-`:236`; N-1395-1..4 `:454`-`:470`; MERGE ADDENDUM #1395 `:553` | `shasum -a 256`, Read whole `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-gate69-batch/report.md` | read 2026-10-06
- P3 gate69 RULINGS: P1 `:5`, P4 `:11`, Q4 X10 `:33`-`:35` and its ruling `:52`, ruled Q1-Q9 `:48`-`:57` | Read whole `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate69/RULINGS_wednesday.md` | read 2026-10-06
- P4 gate69 kit: `kit.json` `script_sha256` == `shasum -a 256` of all 7 `.py`; `prs.A` files (4), `code_paths` (db.ts, the ks1305 test), `merge_base` 3f9f, `flow_num` 22, `cheat_key` KS-1305; `c4_docs_gate69.py` modes `:20`-`:38`, `predict` rc `:541`-`:543`, `qm` `:282`-`:328` | Read README / MERGE_IN_PREDICTION whole; `python3` read of kit.json; `sed -n` | read 2026-10-06
- P5 R 1st handover: 147 lines, 10,787 B, sha256 `a66399885d8abab5589a468c68078780c1b8816ac96028d285e59e59ea5f2eae`, mtime 2026-10-06T00:20:13Z | `wc -lc`, `shasum -a 256`, `TZ=UTC stat`, Read whole `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatR1-2026-10-05.md` | read 2026-10-06
- P6 the original raise brief, 461 lines (sections cited by line) | Read whole `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_seatRaise_spark5.md` | read 2026-10-06
- P7 origin at 2026-10-06T01:22:18Z-01:22:25Z, rc 0: develop `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe`; `refs/pull/1395/head` == `refs/heads/feature/ks-1305-prisma-not-generated-diagnosis-ra1-1` == `1bdfbe0f2f06bbf52f14ed5c6eab9f3261944660`; `/1396/` == its branch == `e6eb53fe2658…`; `/1393/` == its branch == `b5adaba751d8…`; `/1383/` `32e8459bc0f5…` | `env -u GIT_SSH_COMMAND git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" -c core.sshCommand="<checkout's value>" ls-remote git@github.com:Secuura/Distributed_Secuura.git <refs>` (`GIT_SSH_COMMAND` count 0) | read 2026-10-06
- P8 PR #1395: open, not merged, head `1bdfbe0f2f06`, mergeable False / `dirty`, title 77 chars == the signed subject, body 8,891 B / 8,839 chars, sha256/16 `e3e2ba5f26d1e033`, updated 2026-10-06T00:13:22Z; head commit message read whole (`git log -1 --format=%B 1bdf`) | `GET https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/1395` (GH_TOKEN by name from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` inside `python3 -I`, never printed); drafter's scratch clone | read 2026-10-06
- P9 Linear: KS-1305, KS-1136, KS-998, KS-1313, KS-1326, KS-1164, KS-1256 as in LINEAR | Linear GraphQL `issue(id:…)`, LINEAR_API_KEY by name from the same `.env`, never printed | read 2026-10-06
- P10 drafter's SIMULATION in its own `git clone --shared --no-checkout` scratch clone (fetch by SHA from the GitHub URL rc 0; `deadbeef` control rc 128): gate68 predict on `4eaf` reproduced `0b4c3a265454343e8b39af71d2ee6e30bd1d6059`; SIM develop `29430f58fa8f3cd5887d8d7d692123f6d650d5a3`; gate69 `chain`: B alone `cee3fc9913199eeb7eebb1e1c058ff8062ee19a8`, SIM squash(B) `5e2f113b78b5`, A over it `3e708d1191ad652809cbef84215cd496ad1b74ea` (flow `278694921bc4` tail 18 19 20 21 22, cheat `e4ab72a1d4c6` tail KS-938 KS-723 KS-1278 KS-1256 KS-1305, READ-BACK OK); `mergetree --pr A --over-sim-of B`: rc 1, tree `3409ada73811`, 2 conflicted, flow THEIRS-then-OURS == TAIL True, cheat THEIRS-then-OURS == TAIL **False** with READ-BACK OK, DIVERGENCE; `predict --order wrong` READ-BACK FAIL with rc 0; four raise product blobs equal at `3f9f` and `3e708d1191ad`; `3f9f..3e708d1191ad` 20 paths, 0 raise-path hits; ks1293 test at `b5adaba` `:168`-`:179` MANIFEST-DRIFT reads `ANCHORING_SERVICE_URL` mentions; ks1305 test at 1bdf mentions it 0 times (control ks520: 2) | `G68_SCRATCH` / `G69_SCRATCH=<drafter scratchpad>/g6x python3 <kit>/c4_docs_gate6x.py …`; `git show`, `grep -c`, `rev-parse --short=7` in the drafter's clone; outputs `<drafter scratchpad>/d/*.out` | read 2026-10-06
- P11 lane R tools: `mergera1.py` 585 lines, `:112` `GIT_SSH_COMMAND` in tool env, `:113`-`:118` `MERGE56_SCRATCH` dead default, `:194`-`:195` `.push-lock-56` message, `:240` files == targets, `:417`-`:428` note / artefact required, `:434` body_verbatim, `:457` `body = vb + "\n\n" + note + "\n"`; `pushra1_ff.sh` 128 lines, `:82`-`:84` LOCK_SEAT + WT TARGET EXPECT, `:110` take, `:117` release, 0 `push-lock-*` literals; `lockra1.sh` 559 lines, `:217` own `-d8`, `:223` name guard, `:289` `-f3`, `:302` `-e4`, `:303` `-g1`, `:307` `-56`, `:496`-`:501` foreign-holder; B 66th's `mergein66.sh` 13,248 B sha256/16 `ad2b0e28cb498a22` (B 67th's copy `a675a1330be808d8`), args `:27`-`:32`, `lock56.sh` `:88`/`:93`, `:110` rc 1, `:111` TWO conflicted | `wc`, `sed -n`, `/usr/bin/grep -n`, `shasum -a 256`, `diff` of `mergee4.py` vs `mergera1.py` | read 2026-10-06
- P12 worktree `s-ra1-ks1305`: HEAD `1bdfbe0f2f06` on `feature/ks-1305-…-ra1-1`, porcelain 0, dist/index.js + `Blockchain/Dev/node_modules` + `systemTest/akto/node_modules` present, `services/originate/node_modules/.prisma` absent, pre-push `test -x` rc 0; shared `refs/heads/…-ra1-1` `1bdfbe0f2f06` (`for-each-ref`); `refs/remotes/origin/develop` `32e058975d4e`; `cat-file -t 4eaf…` rc 128 | `git -C` read verbs, `[ -e ]`, `test -x` | read 2026-10-06
- P13 floor and token: panes `%0`, `%60 Secuura/Blockchain`, `%1`; 0 `.push-lock-*`, 388 `s-*`; `ra2` 0 raw / 0 bounded over 2,092 origin refs, 0 bounded in `history.md` (control `ra1`: 1 raw / 1 bounded over refs), 0 `s-ra2-*` | `tmux list-panes`, `ls -1A worktrees`, `/usr/bin/grep -c` (raw and `(^|[^0-9a-z])ra2([^0-9a-z]|$)`) over `<drafter scratchpad>/d/lsremote_all.txt` and `history.md` | read 2026-10-06
- P14 raise payloads: `out.md.checker/patch.diff` KS-1136 10,960 B `7c38ea016b155074`, KS-998 5,599 B `a4905e4da54a6cf7`, KS-1313 9,252 B `59f5d73d68df586d`, KS-1164 4,643 B `5c5e586406ebe4b1`; each REVIEW `VERDICT: HOLD`; KS-1136 / KS-998 `round.json` tier `bash_patch`, golden `DIFFERS`; 0 `diff --git` / `index` lines in either `patch.diff`; `local-model/night/` READY_ files matching the four keys: only 2026-09-15 / 09-18 / 09-22 rounds | `wc -c`, `shasum -a 256`, `/usr/bin/grep`, `python3` read of `round.json`, `ls … | grep` | read 2026-10-06
- P15 #1395 squash body draft: 2,543 B / 47 lines, sha256 `0fa8232f5abba4cc7d0b81b7e0a32a3459be4138a75ffd4b0cb6942c759a2b75`; strict closing 0 (controls 1 / 1); closing-family words 0; keys `KS-1305` only (x2); Co-Authored-By 0; Merged by 0; "three-term" 0 | `python3 -I <drafter scratchpad>/scan.py <drafter scratchpad>/d/squash_body_1395.txt KS-1305`; `shasum -a 256` | read 2026-10-06
- P16 `dev-reload.sh` at `4eaf`: blob `f74b7aee6833572673b6a65dee3ccaa9162f5968`, `:21` `set -euo pipefail`, `:73` `echo "▸ [3/3] restart $CONTAINER…"`; KS-1355 Spark brief `:55` "the `$CONTAINER…` progress line at `:73` (see UNMEASURED: a separate defect, not this brief)" | `git show 4eaf:Blockchain/Dev/scripts/dev-reload.sh | sed -n`; `/usr/bin/grep -n` on `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1355-dev-reload-slot-container/KS-1355.md` | read 2026-10-06
- P17 Kam's 09:37:54 rule and the clause line `:20`; card `secuura-capped-prs-1245-1278-disposal-1005` text as read by Wednesday (raise brief `:17`) | `/usr/bin/grep -n` on `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-06_past-70pct-spark-takes-80pct-of-tasks.md`; raise brief read whole | read 2026-10-06
- P18 STANDING_LINES 415 lines, read whole; cited `:86`-`:109`, `:190`-`:219`, `:253`, `:257`, `:259`-`:261`, `:269`-`:278`, `:318`, `:338`, `:355`, `:371`-`:376`, `:382`, `:394`-`:414` | Read `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` | read 2026-10-06
- P19 template: B 67th's brief (485 lines), structure copied | Read whole `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_seatB67_1393_merge.md` | read 2026-10-06
- P20 `df -m /Volumes/DevMASTER`: 695,285 MiB free | `df -m` | read 2026-10-06
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-06 12:38
