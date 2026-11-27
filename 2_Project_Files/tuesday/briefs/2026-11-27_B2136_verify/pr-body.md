RD-744 RD-750 RD-745 RD-824: four changes to the erasure purge in `backend/dataErasure.js`

Six commits on `279b2235`; seven paths. One product file, `backend/dataErasure.js`, gains 93 lines and changes 10. There are four new test files (58 cells), one turned cell in an existing test file, and the counts file. No workflow, helper or other file is changed, and nothing is deployed.

## RD-744: a hard-link refusal is carried by its inode
- When the purge refused a name because a name outside the data directory shared its inode, a later run saw only the name. If an app write had replaced the file, or an operator had deleted it, the re-drive recorded the erasure `purged` while the outside name still held the erased bytes.
- Every refusal entry now records `refusedInode` (device:inode, the key the census already uses). It does so at all four refusal sites: a live store, a file inside a directory store, a recovery copy, and an interrupted-write sibling.
- Before it removes anything, a re-drive reads the identity of each refused name with `lstat`. It never follows the name, and reads nothing outside the data directory but that name.
- A refusal resolves only when that inode is still ours with nlink 1, or when this run purged the name. A changed inode, a missing name or an unreadable name keeps the failure, with a text that asks an operator to confirm the other name is gone.
- A record written before this change names the inode only in its text, and is read from there.
- New file `__tests__/rd744-hard-link-refusal-is-carried-by-its-inode.test.js` has 21 cells. 18 read red before the change; R3, R8 and C1 are controls.

## RD-750: an erasure record names a file once
- A name the run removed (a re-created store beside a surviving target) could appear in both `filesPurged` and `filesFailed`.
- After both settle steps, a name that stays in `filesFailed` is taken out of `filesPurged`. The re-created file is still removed, and the audit row counts the settled lists.
- New file `__tests__/rd750-a-file-is-named-once-in-the-erasure-record.test.js` has 9 cells. O1 to O6 read red before the change; O7 to O9 are controls.

## RD-745 (the `backend/dataErasure.js` half): a non-normalised DATA_DIR
- With DATA_DIR spelled with a trailing slash, a doubled slash, a dot segment, a dot-dot segment or a relative `./data`, two of our own names on one inode refused each other on every run.
- The data directory is now resolved once at the start of the purge, and the census resolves both sides of its comparison. Ledger labels are relative to the data directory under any spelling.
- New file `__tests__/rd745-non-normalised-data-dir-names-do-not-refuse-each-other.test.js` has 14 cells. It includes the two census guards the ticket asked for: a listed name outside the data directory is not ours, and a symlink to a hard-linked copy is not a name of that inode.
- The last commit moves one unchanged assertion of cell K8 after the cell's two reads, so the cell no longer checks a path before reading it.
- The Dockerfile part of RD-745 is not in this change.

## RD-824: a link whose target path runs through a regular file
- Such a link (the resolver answers ENOTDIR) was kept as a failure on every run, so the erasure stayed `purged_incomplete` forever.
- ENOTDIR now joins ENOENT as "nothing behind the link". This applies at the resolver call and at both steps of the chain walk. EACCES and EPERM stay failures, and the link is kept. The file the path runs through is never touched.
- One existing cell is turned: U2 of `__tests__/rd838-chain-canonical-key-and-cap.test.js`. Its own header said to change it with this ticket.
- New file `__tests__/rd824-link-through-a-file-resolves-to-nothing.test.js` has 14 cells.

The counts file moves from 6530 tests in 411 suites to 6588 in 415. The project's own command wrote it.

## Choices made by the coordinator (no product owner ruling rests on this change)
- One change for the four tickets.
- ENOTDIR joins at the resolver and at both steps of the chain walk; EACCES and EPERM stay failures.
- DATA_DIR is resolved at the top of the purge and in the census.
- A name that is failed is not also listed as purged ("failed wins").
- A carried refusal is a dead end with an operator text. There is no admin surface for the confirmation yet: the record is edited by hand.
- The one existing cell, U2, is turned rather than kept.

## Reviewed
An independent review did the following:
- Re-ran the four new files and the turned cell at the base and at the head, in two shapes: a Linux-like temp setup (`TMPDIR=/tmp` with a persistent `RUNNER_TEMP`) and this machine's own temp folder. The red cells at the base were exactly the ones named, and every cell was green at the head.
- Ran 27 mutations of the four hunks with its own program. Each turned red exactly the cells named for it; one (the census resolving its own copy) is equivalent and turns nothing red.
- Ran the whole suite with the project command: 6588 of 6588 in 415 suites.
- Drove shapes the cells do not use. Each is either carried or refused at the head:
  - a relative, a doubled-slash, a dot and a dot-dot DATA_DIR for the carry;
  - a directory placed at a refused name;
  - an unreadable name;
  - a name refused, replaced by a second hard-linked file, and refused again.
- gitleaks found nothing in the commits or their messages.

## Named limits (not addressed here)
- **During a re-drive.** If an app write replaces a refused name after the re-drive has read its identity and before the purge reaches it, the run removes the new file and resolves the refusal. The resolution checks the name, not the inode it removed. Before this change, every such replacement certified; now only one inside that window does.
- **Lexical link resolution.** A link whose text runs through a symlinked directory and then `..` is resolved lexically by the resolver, not as the kernel resolves it. If the lexical path then runs through a regular file (ENOTDIR), the link is removed and recorded purged, while the kernel's target may hold data. The same was already true before this change for the lexical path that ends at nothing (ENOENT).
- **Two entries for one name.** A name refused, replaced by a second hard-linked file and refused again holds two failure entries, one per inode. Neither is lost.
- **No admin surface** exists for an operator to record the confirmation.
- **Not handled:** the catch path's union of a purge that dies part-way; a recovery copy whose own parent is a file; the removal log wording for an ENOTDIR link (it still says "dangling or looping").
- **Real Linux.** The hosted `build` job of this pull request is the first run of the new files on real Linux (hard links, inode keys, a 41-link chain). A red result there on a new cell is a fix round.

## Deploy
None. The merge touches `backend/` and `__tests__/`, which the Deploy demo workflow does not ignore, so a run starts on the push. Both of its jobs are expected to read skipped, because the switch variable is not set.
