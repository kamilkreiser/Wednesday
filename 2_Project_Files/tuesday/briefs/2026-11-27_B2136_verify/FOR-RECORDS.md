# FOR-RECORDS: RD-744, RD-750, RD-745 (its backend/dataErasure.js half) and RD-824, for the records pass AFTER the landing

After the landing, fill in `<n>` (the pull request number) and `<M>` (its merge commit). Take the Deploy demo line from landing.txt step 4, and the gate line from the first line of VERDICT.md.

This gate did NOT read or write Jira. Before writing each comment, the records seat reads the ticket's current comments and state. No person's name and no card, seat or build id goes in a comment. Name every choice as the coordinator's default.

## Ticket state, read against the project's rule
The project rule is `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/CLAUDE.md` line 302, under "When completing work": a code change goes to `Testing`. The product side moves it on to `Release Ready` after verification.

- **RD-744 (High): Testing once ticket candidate 1 below is filed and linked ("Relates to").** The scope sentence is built at all four sites: carry the refusal keyed by the DATA_DIR name plus dev:ino; resolve only when the same inode is ours with nlink 1; a changed or missing inode keeps purged_incomplete with an operator text. The gate's Major 1 is a residual window *during* a re-drive: an app write after the snapshot and before the purge reaches the name certifies purged. The ticket's defect (a replacement at any time between runs) is closed.
  - The coordinator may instead keep RD-744 open for that window. Either way, LEFT FOR OTHERS 1 (an admin surface to record the confirmation) stays owed on this ticket.
- **RD-750: Testing.** Its scope ("settle each file to one list, with an h10-shaped cell red first") is met:
  - O1 to O6 red at the base and green at the head;
  - the gate found no file in both lists in any of its 40 probe records.
  - LEFT FOR OTHERS 3 (the catch path's union, and a pre-change record that already names a file twice) stays owed. File it as a follow-up if the coordinator wants it tracked apart.
- **RD-745: comment, do NOT move.** The `backend/dataErasure.js` half (C-F2) and the C-F3 cells (inside() always true -> K8; statSync -> K9) are met. The Dockerfile part belongs to lane 4 (the sweep, row RD-745) and is not built. The ticket moves when lane 4's part lands, or when the coordinator splits it.
  - Comment 39111's question, whether RD-424's mapping now traces a relative DATA_DIR's labels, is UNMEASURED. At the head the labels are relative to the resolved directory (K11, K14), but RD-424 code was not read.
- **RD-824: Testing once ticket candidate 2 below is filed and linked.** The question is answered by the coordinator's default:
  - ENOTDIR joins at the resolver call and both steps of the chain walk;
  - EACCES and EPERM stay failures;
  - the file a path runs through is never unlinked (gate probe P13).
  - The gate's Major 2: the resolver's first call is lexical, so a link whose text holds `<symlinked dir>/..` can be removed while the kernel's target holds data. The same is already true at the base for ENOENT.
  - CLARIFICATIONS.md line 1508 ("Not decided here: whether ENOTDIR should join ENOENT ...: RD-824") should gain an addendum recording the coordinator's decision. That is records text, not code.

## RD-744: comment
Pull request <n> landed as merge commit <M>, the merge of the reviewed head `abef7000` (six commits; `b96228b9` is this ticket's).
- Every hard-link refusal entry now records `refusedInode` (device:inode, the census key). This holds at the live store, a file inside a directory store, a recovery copy and an interrupted-write sibling.
- Before it unlinks anything, a re-drive `lstat`s each earlier-refused name: our own listed name, never followed.
- A refusal resolves only when the name still has that inode AND (nlink is 1 OR this run purged the name). Otherwise the refusal is carried into `filesFailed`, unless this run refused the same inode again. The carried text names the inode and asks an operator to confirm the other name is removed.
- A record written before this change is read from its text (the refusal prefix, then `inode N on device D`).

New file `__tests__/rd744-hard-link-refusal-is-carried-by-its-inode.test.js` has 21 cells.
- H1 to H4, R1, R2, R4 to R7 and R9 to R16 were red at the base and green at the head, in a Linux-like temp shape and in the machine's own (the gate ran both). R3, R8 and C1 are controls, green on both sides.
- Thirteen mutations each turned red exactly their named cells (gate re-run with its own program).
- Gate shapes outside the cells, all carried at the head (each certified `purged` at the base):
  - a relative `./data`, `./data/`, a doubled slash, a dot segment and a dot-dot segment;
  - a directory placed at the refused name;
  - an unreadable name (EACCES injected at the snapshot only);
  - a name refused, replaced by a second hard-linked file and refused again: two entries, and the first inode's entry survives the next run.

**Named limits (the coordinator's defaults):**
1. No admin surface records the confirmation; the record is edited by hand.
2. An entry with no recoverable inode is settled as before.
3. Inode numbers above 2^53.
4. The gate's Major 1: a replacement of the refused name *during* the re-drive, after its snapshot and before the purge reaches it, certifies purged. Measured by an onPurge hook: the outside canary survives, status `purged`; the base does the same.
5. A carried entry whose `refusedInode` field were removed by some later writer would be dropped on the next run: the carried text does not start with the refusal prefix the legacy parser reads. No writer in `backend/` strips fields today (gate grep). Info.

Hosted build of the pull request: <the `VERDICT: PASS` line, the first Linux run>. Deploy: none; Deploy demo run for <M>: <conclusions>. State: per the reading above.

## RD-750: comment
Same landing; `cdcf3b9c` is this ticket's.
- After both settle steps (the surviving-target settle and RD-744's), a name that is in `filesFailed` is removed from `filesPurged`: "failed wins", the coordinator's default.
- The re-created file is still removed, and the carried failure still names its surviving target.
- The audit row counts the settled lists.

New file `__tests__/rd750-a-file-is-named-once-in-the-erasure-record.test.js` has 9 cells. O1 to O6 were red at the base and green at the head in both shapes; O7 to O9 are green on both sides. Three mutations each turned red exactly their named cells (gate re-run).

**Named limits:**
1. The catch path's union (a purge that dies part-way) can still name a file twice.
2. A record written before this change that already names a file in both lists is repaired only by the next run's write.
3. Two failures with one `file` are not merged.
4. Info from the gate: when a carried failure wins, the record does not show that this run deleted the replacement file at that name. The deletion happens, as the kit states.

State: Testing.

## RD-745 (the backend/dataErasure.js half): comment
Same landing; `21db2207` and `abef7000` are this ticket's.
- `purgeNow` resolves DATA_DIR once (`path.resolve`).
- The census resolves its root and each listed name, so `inside()` compares resolved paths. Under a trailing slash, a doubled slash, a dot or dot-dot segment, or a relative `./data`, two of our own names on one inode are purged instead of refusing each other, and the ledger labels are relative to the data directory.

New file `__tests__/rd745-non-normalised-data-dir-names-do-not-refuse-each-other.test.js` has 14 cells.
- K1 to K4, K6, K7, K11, K12 and K14 were red at the base and green at the head; K5, K8 to K10 and K13 are green on both sides.
- C-F3's two mutants are pinned: inside() always true reddens K8, and statSync instead of lstat reddens K9.
- Commit `abef7000` moves K8's unchanged link-count assertion after the cell's two reads. A local static analysis had flagged the earlier order as a check-then-use race on the test file. K8 still reads red under the inside()-always-true mutant (gate re-run).
- Gate matrix, at the base and the head: seven DATA_DIR spellings x three plants. Only "two of our own names" changes, from refused to purged. A store hard-linked outside, and one hard-linked to a legacy copy in a sibling folder whose name starts with the data directory's, are refused on both sides.

**Not in this change:**
- the Dockerfile part (lane 4);
- DATA_DIR `/`;
- a case-insensitive file system or Windows separators;
- a relative DATA_DIR whose working directory changes during a run;
- whether RD-424's mapping now traces the labels (UNMEASURED).

State: unchanged until lane 4's part lands.

## RD-824: comment
Same landing; `471d8655` is this ticket's.
- `_linkTargetOrNull` and both steps of `_walkLinkChain` now treat ENOTDIR (the target path runs through a regular file) like ENOENT: the link is removed and recorded purged.
- EACCES and EPERM stay failures, and the link is kept. The file the path runs through is never unlinked.
- The existing cell U2 of `__tests__/rd838-chain-canonical-key-and-cap.test.js` is turned, as its own header asked.

New file `__tests__/rd824-link-through-a-file-resolves-to-nothing.test.js` has 14 cells.
- N1 to N9, N13 and N14 were red at the base and green at the head; N10 to N12 are green on both sides. The turned U2 was red at the base and green at the head.
- Five mutations each turned red exactly their named cells (gate re-run).

**Named limits:**
1. A recovery copy whose own parent is a regular file stays "could not stat".
2. A carried failure whose target now runs through a file stays carried (RD-684 F7).
3. EACCES and EPERM are injected in the cells, not real. The walk's lstat step answering EACCES or EPERM is held by no cell, the same as at the base (gate mutation).
4. The removal log still says "dangling or looping".
5. The gate's Major 2: the resolver's first call (`fs.realpathSync`) resolves link text lexically. A link `sd/../f/x`, where `sd` is a symlinked directory and the local `f` is a regular file, is removed and recorded purged, while the kernel's target (`<sd's real parent>/f/x`) holds data. Measured: canary intact, status `purged`; the base kept it as a failure. The ENOENT twin (no local `f`) already certifies at the base.
6. Info, macOS only: a link into `<file>/..namedfork/rsrc` (a resource fork holding bytes) answers ENOTDIR and is removed.

State: per the reading above.

## LEFT FOR OTHERS (the kit's list, carried)
1. An operator surface to RECORD RD-744's confirmation (owed on RD-744).
2. RD-745's Dockerfile part (lane 4), and RD-424's label mapping for a relative DATA_DIR (comment 39111; UNMEASURED).
3. The catch path's union in `purgeNow`, and a pre-change record naming a file in both lists (RD-750 follow-up if wanted).
4. A recovery copy whose own parent is a regular file; RD-684 F7.
5. The removal log wording for an ENOTDIR link ("dangling or looping"; its line holds a non-ASCII marker).
6. The records: these four comments and moves (this file).
7. The deploy: none.
8. RD-455, RD-728 and RD-981, the later kits of lane 2.

## Ticket candidates from the gate (dup-check RD-744, RD-685, RD-640, RD-838 and RD-824 neighbours before filing)
1. **RD-744 follow-up: "this run purged it" checks the name, not the inode.**
   - Gate probe: run 1 refuses `settings.json` (hard-linked outside). On run 2, an `onPurge` hook stands in for an app write landing after the snapshot: it replaces the name by tmp+rename. The run unlinks the new inode, `purged.includes(name)` holds, `same` is true from the snapshot, and the refusal resolves. Status `purged`, outside canary intact. The same at a recovery copy.
   - Fix shape for the decision: resolve on "purged" only when the inode this run unlinked at that name equals `refusedInode`. For example, record the dev:ino at the unlink, or re-`lstat` immediately before the unlink and compare.
2. **RD-824 / RD-640 follow-up: the resolver's null is lexical.**
   - `fs.realpathSync` (the JS implementation) joins link text with `path.resolve`, so `<symlinked dir>/..` is collapsed before the kernel would follow the symlink.
   - At the head, ENOTDIR and ENOENT on the lexical path both remove the link and certify, while `fs.realpathSync.native` and a plain read through the link reach real data (gate probes P14, P14b).
   - P14c, with a real local `f/x`, shows the same lexical resolution naming the wrong surviving target in the failure text.
   - Fix shape: confirm a null by the kernel-faithful walk (`_walkLinkChain`, which already resolves each hop's directory with realpath) or by `realpathSync.native` before removing the link.
3. **Pre-existing RD-685 census: one physical name counted twice.**
   - A recovery directory that aliases another listed directory makes the census count one physical name twice, so `ours >= nlink` and an outside hard link is never refused. Gate probe P9: legacy folder inside DATA_DIR, `.emergency-backup -> emergency-backup`. At the base and at the head alike the first run certifies `purged` with the outside canary intact.
   - Reachable only when the legacy folder sits inside DATA_DIR. With the default DATA_DIR (`/var/lib/printer-dashboard/data`) it does not.
   - Fix shape: key the census's name set by the real path of each name's parent plus basename.
4. **Info, no ticket unless wanted:**
   - the key-match in RD-744's "this run refused it again" check is held by no cell (a file-only match turns nothing red, though it would forget the first inode);
   - the "unreadable" branch is held by no cell (carried, measured by the gate);
   - RD-750's dedupe of ordinary failures is held by no cell.
