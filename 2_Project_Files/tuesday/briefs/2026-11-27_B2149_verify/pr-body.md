RD-744 RD-750 RD-745 RD-824: changes to the erasure purge in `backend/dataErasure.js`, in two rounds

Nine commits on `279b2235`, nine paths. The one product file, `backend/dataErasure.js`, reads 137 lines added and 14 removed against the base (both rounds together). There are six new test files (76 cells), one turned cell in an existing test file, and the counts file. No workflow, helper or other file changes, and nothing is deployed.

| Commit | Ticket | What |
|---|---|---|
| `b96228b9` | RD-744 | a hard-link refusal is carried by its inode |
| `cdcf3b9c` | RD-750 | an erasure record names a file once |
| `21db2207` | RD-745 | a non-normalised DATA_DIR no longer makes two of our names refuse each other |
| `471d8655` | RD-824 | a link whose target path runs through a regular file resolves to nothing |
| `6675c397` | - | counts, 6588 tests in 415 suites |
| `abef7000` | RD-745 | one test assertion moved after the reads it guards |
| `934c7f5b` | RD-744 | round 2: the refusal resolves on the inode this run removed, not on the name |
| `76515f5b` | RD-824 | round 2: a link ends at nothing only when the kernel's own resolution agrees |
| `52040f2e` | - | counts, 6606 tests in 417 suites |

## RD-744: a hard-link refusal is carried by its inode
- **The problem.** When the purge refused a name because a name outside the data directory shared its inode, a later run saw only the name. If an app write had replaced the file, or an operator had deleted it, the re-drive recorded the erasure `purged` while the outside name still held the erased bytes.
- **Each refusal records its inode.** Every refusal entry records `refusedInode` (device:inode). This applies at all four removal sites: a live store, a file inside a directory store, a recovery copy, and an interrupted-write sibling.
- **The re-drive reads before it removes.** Before it removes anything, a re-drive reads each refused name's identity with `lstat`, never following it.
- **When a refusal resolves.** Only when that name still held the refused inode at that read AND either that inode had one link, or this run itself removed that same inode at that name. The inode is the one the removal's own hard-link check read immediately before the unlink.
- **Otherwise it is carried.** A changed inode, a missing name or an unreadable name keeps the failure, with a text asking an operator to confirm the other name is gone.
- **Older records.** A record written before this change names the inode only in its text, and is read from there.
- **Commit A's message is corrected by commit F.** Commit A's message says a refusal resolves when the inode is still ours with one link "or this run purged it". The first round's code checked the NAME there. An app write that replaced the name during the re-drive therefore still certified. Commit F keys that clause to the inode the removal read, and corrects the code comment. Commit A is not rewritten; F's message says what the code does.
- **Tests.** `__tests__/rd744-hard-link-refusal-is-carried-by-its-inode.test.js` has 21 cells. `__tests__/rd744-a-refusal-resolves-on-the-inode-this-run-removed.test.js` has 7 cells:
  - V1, V2, V6 and V7: a name replaced during the re-drive at each of the four sites;
  - V3: refused, replaced, refused again (one entry per inode);
  - V4: unreadable to the snapshot, so carried;
  - V5: the control (the outside name removed during the run, so it certifies).

## RD-750: an erasure record names a file once
- After both settle steps, a name that stays in `filesFailed` is taken out of `filesPurged` ("failed wins"). The re-created file is still removed.
- `__tests__/rd750-a-file-is-named-once-in-the-erasure-record.test.js` has 9 cells.

## RD-745 (the `backend/dataErasure.js` half): a non-normalised DATA_DIR
- **Resolved once.** The data directory is resolved once at the top of the purge, and the census resolves both sides of its comparison.
- **What that fixes.** Under a trailing slash, a doubled slash, a dot segment, a dot-dot segment or a relative `./data`, two of our own names on one inode no longer refuse each other.
- **Tests.** `__tests__/rd745-non-normalised-data-dir-names-do-not-refuse-each-other.test.js` has 14 cells. Commit `abef7000` moves one unchanged assertion of cell K8 after the cell's two reads.
- **Not in this change:** the Dockerfile part of RD-745.

## RD-824: when a link ends at nothing
- **Round 1.** ENOTDIR (the link's target path runs through a regular file) joins ENOENT as "nothing behind the link", at the resolver and at both steps of the chain walk. EACCES and EPERM stay failures, and the link is kept. The file the path runs through is never touched. Cell U2 of `__tests__/rd838-chain-canonical-key-and-cap.test.js` is turned, as its header asked.
- **Why round 2 was needed.** The resolver (`fs.realpathSync`, Node's JavaScript implementation) joins link text lexically. It collapses `<symlinked dir>/..` before following the symlink. So a link whose text runs into a symlinked directory and back up could be removed and recorded purged while the path the kernel reaches through it held data. The chain walk joined each hop the same way.
- **Round 2: the kernel confirms.** An ENOENT or ENOTDIR from the resolver is confirmed by the kernel's own resolution (`fs.realpathSync.native`):
  - a path the kernel reaches is the link's target, and is a failure while it survives;
  - only a kernel ENOENT or ENOTDIR removes the link as resolved to nothing;
  - any other kernel answer keeps the link.
- **Round 2: the walk.** It joins each hop's text without normalising it, and resolves each hop's directory with the kernel.
- **Tests.** `__tests__/rd824-link-through-a-file-resolves-to-nothing.test.js` has 14 cells. `__tests__/rd824-a-lexical-null-is-confirmed-by-the-kernel.test.js` has 11 cells:
  - W1 to W4: the four sites;
  - W5: the ENOENT twin;
  - W6: a short chain;
  - W7 and W8: 41-link chains;
  - W9: EACCES and EPERM at the walk's lstat;
  - W10: the control;
  - W11: a kernel EACCES.

The counts file moves from 6530 tests in 411 suites to 6606 in 417. The project's own command wrote it.

## Choices made by the coordinator (no product owner ruling rests on this change)
- **Shape.** One change for the four tickets, in two rounds. The second round adds commits after the first; nothing is rewritten.
- **RD-824.**
  - ENOTDIR joins ENOENT, and only when the kernel's resolution agrees.
  - EACCES and EPERM stay failures.
  - A kernel answer other than ENOENT or ENOTDIR keeps the link.
- **RD-744.**
  - The inode "this run removed" is the one the removal's own hard-link check read.
  - A carried refusal is a dead end with an operator text; there is no admin surface for the confirmation yet.
- **RD-750 and RD-745.**
  - "Failed wins" in the record.
  - DATA_DIR is resolved at the top of the purge and in the census.

## Reviewed
An independent review did the following:
- **Red first, then green.** Re-ran both rounds' new files at their base and at the head, in a Linux-like temp setup and in this machine's own. The red cells at each base were exactly the named ones, and every cell was green at the head.
- **Mutations.** Ran the twelve round-2 mutations with its own program. Each turned red exactly the cells named for it.
- **The whole suite.** Ran it with the project command: 6606 of 6606 in 417 suites.
- **Probes.** Drove shapes the cells do not use:
  - A refused name replaced during the re-drive, at each of the four sites, under six DATA_DIR spellings and a symlinked DATA_DIR. Every one was carried; the first round certified each.
  - The same with the outside name removed instead. Every one certified, as it should.
  - A symlinked directory in the middle of a chain, an absolute link text, and 41-link chains with `..` mid-chain or at the end. Every one is now a failure or kept; the first round certified each.
  - A kernel error injected at each site. The link was kept and the run went on to purge the other stores.
  - The remaining shapes are in the named limits below.
- **Secrets.** gitleaks found nothing in the commits or their messages.

## Named limits (not addressed here)
- **The resolver's SUCCESS answer is still lexical.** When `fs.realpathSync` succeeds, its answer is used as the link's target. For a link like `sd/../<name>`, that answer can be a local path while the kernel reaches a different path through the link, and the failure then names the wrong path. The review measured two ways this certifies `purged` while the kernel's target keeps the data:
  - the local path is another listed store that the same run removes later;
  - the operator removes the named local path, as the failure text asks, and re-drives.
  Both shapes were already there before this change. The fix shape: take the kernel's resolution as the target whenever the two answers differ.
- **A store replaced during the FIRST run.** If a store hard-linked outside the data directory is replaced by an app write after the run starts and before the purge reaches it, the run never sees the outside link of the old inode. It certifies `purged` while that outside name keeps the earlier bytes. No refusal exists to carry, and this was already true before this change.
- **A replacement in the instant between the removal's own `lstat` and its unlink.** The two are adjacent synchronous calls. Only another process can reach that window, and the check passing means no outside name existed at that read.
- **The census.** The census of our own names is built once per run. A recovery folder that aliases another listed folder counts one name twice. Both were already true before this change.
- **A resolver answer that changes between the two calls** (a race).
- **A kernel ELOOP after a lexical ENOENT or ENOTDIR.** The link is kept; no plant reaches it.
- **A link through a kernel loop beyond `..`.** It is kept as a failure, and the erasure does not finish on it until an operator removes the loop. The first round removed it; the base kept it (by reading the code).
- **macOS named forks** (`<file>/..namedfork/rsrc`) read as ENOTDIR.
- **The production image's libc.** It is Alpine (musl). Its `realpath(3)` has not run any of these cells: the hosted build is glibc, and the review was macOS.
- **No admin surface** exists to record an operator's confirmation.
- **The catch path's union** (a purge that dies part-way) can still name a file twice.
- **The removal log wording** for an ENOTDIR link still says "dangling or looping".
- **Real Linux.** The hosted `build` job of this pull request is the first run of the new files on real Linux: hard links, inode keys, glibc `realpath(3)`, 41-link chains. A red result on a new cell there is a fix round.

## Deploy
None. The merge touches `backend/` and `__tests__/`, which the Deploy demo workflow does not ignore, so a run starts on the push. Both of its jobs are expected to read skipped, because the switch variable is not set.
