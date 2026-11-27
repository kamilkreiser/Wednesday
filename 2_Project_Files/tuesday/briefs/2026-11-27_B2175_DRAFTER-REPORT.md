STARTABLE: YES (after Tuesday answers Q-2, Q-3 and Q-4 in the STAMP; REFUSE 1 requires them)

# B2175 drafter report: kit `2026-11-27_B2175_SEAT-N186_nexusai-rd490-portband-jest-slots.md`

## BLUF
- One NexusAI seat kit, two parts. **Part P:** a new branch `b2175/rd490-portband` from main `d2aeecf8`: the rd490 browser guard claims its two server ports from the run's own `workerBand()` (the worktree slot's worker band) instead of the fixed 38900-38939; the reservation before the await and the listener-pid check are kept; one new cell asserts the band; the stale comments in the file header and in `test-server.js` lines 62-63 corrected; commit A plus a counts commit K (PREDICTED 6635 / 419); one push, no PR. Proof: a pair run of two copies on slots 9 and 12 at the same time, red-first at BASE (`shape=FIXED-BAND-SHARED` or `result=COLLISION-RED`) and green at A (`OWN-SLOTS-DISJOINT`, `BOTH-GREEN`), a cell control (the fixed band put back turns exactly the new cell red), the Linux-shape update run and the plain verify.
- **Part L:** a candidate `nexusai-lock.sh` with counted jest slots (FOR TUESDAY section 2 items 1-6), proved in scratch bases with the RD-847 arms (regression, no slot file) plus seat-written slot arms S1-S10 and mutants; an install script dry-run against a stand-in folder. **Not installed** (Q-3 default) and **`slots-jest` not written** (Q-8).
- Gate: one G1 gate reads both (the lock gates every NexusAI seat). No deploy; a merge of the branch starts a `Deploy demo` run (`__tests__/**` and `scripts/**` are not in `paths-ignore`), held by `CI_DEPLOY_ENABLED`, the `demo` reviewer and C-224.
- Tuesday's mid-drafting addendum (N182 / kit B2139 live) is folded in: the queue wait behind N182, the install-only-when-idle rule, the partition from N182's side, and serial landing with counts regenerated for the second branch.

## FACTS RE-MEASURED (instrument; control)
- Main `d2aeecf8cda67265cc316646953c45d92b861f77` = merge of pull request 268 (gh api GET 20:52:24; parents de39619c and 61612323). Open pull requests `[]`. PR 268 merged 2026-11-27T05:50:53Z.
- Blobs at BASE, tarball `git hash-object` equal to `contents?ref=` sha: rd490 `6de468f9`, test-server `ff854528`, rd573 `8aaa171b`, rd591 `d9d0693b` (control: a missing path answers 404). Counts 6634 / 419. `package-lock.json` sha256 prefix `37e5add354e5`.
- rd490 cells 72 by program (pages 12 + red 47 + identity 2 + 6 + 4 + 1; equals the 72 red cells in the measurement report); 14 indented call sites, 0 in column 1.
- Branch census: 528 branches, compare against BASE: 0 touch the rd490, test-server, rd573 or rd591 files (control: 63 touch the counts file); 155 ahead. Caveat: the compare `files` list is capped at 300 files per branch, so a branch with a very large diff could be under-read.
- Jira GET (`project = RD AND ( ... )` on every JQL; own helper reads `.env` in process): no ticket for the cross-copy rd490 collision or a counted jest lock; newest key RD-1050. RD-1047 (To Do) may later edit the rd490 file's tmpdir lines.
- Live lock sha256 `cf01bafb...` (391 lines); the live base held no lock directory and 0 jest tickets at 21:02:13. Default base line 84 names `/Volumes/Laptop-DEV/...`, not mounted (`ls -d` refused).
- Slots by the helper's rule (drafter's program; control mg 15, chk 17 as earlier kits printed): `pb` 9, `chk` 12, `p1` 7, `p2` 7. Edge scan of 46 SEAT kits of 26 and 27 Nov: slot 9 0 hits; slot 12 1 hit (B2142, READY); control 22560 7. lsof: bands free; 17 listeners total.
- Panes at 21:08:20: `tuesday`, `Datasec/OXPd2-X89`, `Datasec/NexusAI-N182` (launched during drafting). 27 NexusAI STATUS files of 24-27 Nov all end READY at 20:56:48 (B2139's STATUS appears once N182 starts).
- B2139's OWNS block (its kit lines 101-108): the two entraProvisioning files, simpleDb.js, rd455 and rd981 test files, counts file. No overlap with OWNS-B2175 except the counts file.
- Frozen scripts dry-run under a jest stand-in (three runs, the expected PAIRSUM lines; controls fire). msgscan2175 PASS on msg-A, msg-K and both ticket texts; a planted bad line gives FAIL rc 1. gitleaks 8.30.1: `no leaks found` on msg-A, `leaks found: 2` on a planted random pair.
- `stamp_check.py <kit>` exits 0 (132 claims, sidecar filled; many are instruction fragments marked "not a match literal", the rest measured, RELAYED or PREDICTED as stated).

## D-DECISIONS (the drafter's)
- D1 The red-first is deterministic: the sampler shows both copies' servers inside 38900-38939 even when the race does not fire; a fired race (`COLLISION-RED`) also counts.
- D2 The new cell's red-first comes from a mutation (the fixed band put back at A), because the cell does not exist at BASE.
- D3 The seat writes the product change and the candidate itself (no frozen code): the lock change is a design. Frozen are the pair runner and judge, the scanner, the messages and the ticket texts.
- D4 L5 "unknown slot runs alone": callers that do not declare a slot (every kit today) keep exactly today's one-at-a-time, so the semaphore opens only for kits that export `NEXUSAI_WORKTREE_SLOT`. An ownerless slot directory counts as an unknown holder.
- D5 The branch is pushed before Part L starts, so running out of context in Part L loses no product work.
- D6 Arms copies change exactly one line each (`fifo-arms.sh` 15, `arms8.sh` 8); `NEWDEF` (arms8 line 12) stays, because arm 14a checks that literal.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- Q-1 One kit with both parts? **Default a: yes** (as commissioned).
- Q-2 Builder model? **Default a: Sonnet, row C2 (line 92)**, as the table says. b: Opus. The measurement report's FOR TUESDAY title says "in-session, Opus", and the lock is a concurrency design that every NexusAI seat passes through.
- Q-3 Install the candidate in this run? **Default b: NO, held until the G1 gate's GO.** Installing an ungated mutex change before its G1 gate would invert the gate. a: install at idle after L3 to L5 green, B702's form, with the addendum's rule (no lock directory and 0 tickets in either queue, two reads 10 s apart; never while N182 holds or waits).
- Q-4 A caller with an unknown worktree slot runs only alone? **Default a: yes.**
- Q-5 Add the one new cell (+1 test, counts 6635 / 419)? **Default a: yes.** b: no cell (no counts commit; the pair run is the only proof).
- Q-6 Leave the rd573 and rd591 "RD-490's band" references unchanged (they still pass)? **Default a: yes**, left to a records or follow-up pass.
- Q-7 Two tickets (Task Medium; `test-infra`; `tooling` + `operations`; linked Relates)? **Default a: yes.**
- Q-8 `slots-jest` = 3: who and when? **Default: a follow-up NexusAI seat after (i) this branch is merged on main, (ii) the candidate is installed after GO, (iii) the N=3 re-run of the measurement report (`x2157/nxrun2.py`) is green.** This seat does not write it.
- Q-9 One red-first pair run at BASE (no repeats)? **Default a: yes** (D1 makes it deterministic).
- Q-10 One G1 gate for both parts? **Default a: yes**, round 1 of 2. The drafter found no earlier gate verdict on a lock-script change: the 10 VERDICT files that name `nexusai-lock` were read by file name only.
- Q-11 Jira writes: two creates and one link only, with no moves or comments (the records seat's after landing)? **Default a: yes.**
- Q-12 HARD STOP: about 4-5 h of work plus up to about 2.5 h queued behind N182. **Default: launch now and accept the wait**, or launch after N182's READY.

## CHAIN INPUTS (each step's inputs exist at BASE or come from an earlier step)
| step | inputs | made by |
|---|---|---|
| Step 0 | kit, frozen files, names2142.py, scanlib1114.py, b702 files, measurement report | drafter or existing |
| Step 1 | clone, npm ci | Step 1 |
| Step 2 tickets | ticket-*.txt, scripts/jira-adf.py (at BASE) | Step 0 |
| P0 trees | clone at BASE | Step 1 |
| P2 pair-base | pb, chk, pair2175.sh, pairsum2175.py, wrapper | P0, Step 0 |
| P3 edit | wt, KEY-P, msg-A, names.txt | P0, Step 2, Step 0 |
| P4 pair-head | A | P3 |
| P5 cell-control | A, mut2175.py (seat) | P3 |
| P6 linux-update | chk at A, v2152.sh, rt | P3, P0 |
| P7 K | counts from chk, msg-K | P6 |
| P8 plain | K | P7 |
| P10 push | K, P8 green, P9 | P7-P9 |
| L0-L6 | live script copy, b702 harnesses, p1/p2 | P0, Step 0 |

## UNMEASURED
Everything under real jest: the pair runs, the cell control, both verifies, the 6635 / 419 pair, the rd490 file's run time alone. The candidate lock and every slot arm and mutant (the seat writes them). The RD-847 arms on this volume (they last ran on Laptop-DEV). The Jira creates and link. Real Linux (the hosted build of Tuesday's PR is the first). Three real holders on the live base.

## OUTSIDE-THE-FENCES DISCLOSURE
- Wrote only: this report, the kit, its sidecar, and files under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/d2175/`: the BASE tarball and extract, frozen/, dry/ stand-in trees and logs, jsearch.py, jfields.py, slot.py, bcensus.sh/.tsv/.log/.done, branches.txt, kits2627.txt, card.txt, names.txt (it holds the four names; never printed), plant-bad.txt, fill.py. Nothing was deleted.
- The dry run's stand-in servers listened for about 6 s each on 38900-38903, 23200-23201 and 26400-26401 on this machine (21:00:24-21:00:42). No NexusAI seat ran jest at that time.
- The branch census ran as a shell background job (`&`) for about 6 minutes, with about 528 GET calls. GitHub and Jira were read by GET only. The card was read with `decision_queue.sh show datasec-parallel-builds-decision-1127` into card.txt: status open, no ruling, delegated "your call". No write in the NexusAI project, Jira, GitHub, cards or mail. No lock was taken and no jest was run.
- Read-only reads beyond the commission list: NexusAI `CLAUDE.md`, `JIRA.md` excerpts, `CLARIFICATIONS.md` lines, `.tools/b2152` wrappers and logs, `b702` files, kits B2143, B2152 and B2139 (OWNS), and `fleet/state/s333/d2143/jget.py` (form only).
Last `date` of drafting: Fri 27 Nov 2026 21:10:43 AEDT
