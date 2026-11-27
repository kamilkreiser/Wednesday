# FOR-RECORDS: RD-744, RD-750, RD-745 (its backend/dataErasure.js half) and RD-824, for the records pass AFTER the landing (gate B2149, round 2 of 2)

This file SUPERSEDES round 1's `2026-11-27_B2136_verify/FOR-RECORDS.md`. Its ticket candidates 1 and 2 are closed by commits F and G; its candidate 3 is carried below as a new ticket.

After the landing, fill in:
- `<n>`, the pull request number;
- `<M>`, its merge commit.

Take the Deploy demo line from landing.txt step 4. Take the hosted build line from step 2. Take the gate line from the first line of VERDICT.md.

This gate did NOT read or write Jira. Before writing each comment, the records seat reads the ticket's current comments and state. No person's name and no card, seat or build id goes in a comment, and every choice is named as the coordinator's default.

## Ticket state, read against the project's rule
The rule is `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/CLAUDE.md` line 302: a code change goes to `Testing`, and the product side moves it on to `Release Ready` after verification. The gate re-printed the line with grep -n at 12:2x.

**RD-744 (High): Testing.**
- Round 1 carried the refusal by its inode.
- Round 2 resolves "this run removed it" on the inode the removal read, not on the name. That closes the gate's round-1 Major 1.
- Measured at the head: a refused name replaced during the re-drive is carried, under six DATA_DIR spellings, a symlinked DATA_DIR and all four sites (28 shapes, every one certified `purged` at round 1's head).
- LEFT FOR OTHERS 1, the operator surface to record the confirmation, stays owed on this ticket.

**RD-750: Testing.** It is unchanged since round 1. Across 101 probe records at the head, no name is in both lists.

**RD-745: comment, do NOT move.**
- The `backend/dataErasure.js` half is met.
- The Dockerfile part belongs to lane 4 and is not built.
- RD-424's mapping question (comment 39111) is still UNMEASURED.

**RD-824: Testing.**
- The ENOTDIR decision (round 1) stands: it holds only when the kernel's resolution agrees (round 2). That closes the gate's round-1 Major 2, measured on P14 and P14b and on five further shapes.
- CLARIFICATIONS.md line 1508 ("Not decided here: whether ENOTDIR should join ENOENT ...: RD-824") should gain an addendum recording the coordinator's decision, as records text.
- The gate's Finding 1 below (the resolver's SUCCESS answer is lexical) is pre-existing. It is the same lexical-resolver class, so file it before RD-824 moves, and link it ("Relates to").

## RD-744: comment
Pull request <n> landed as merge commit <M>. That is the merge of the reviewed head `52040f2e`: nine commits, of which `b96228b9` (round 1) and `934c7f5b` (round 2) are this ticket's.

**What changed:**
- Every hard-link refusal entry records `refusedInode` (device:inode) at all four removal sites: the live store, a file inside a directory store, a recovery copy, and an interrupted-write sibling.
- Before it unlinks anything, a re-drive `lstat`s each earlier-refused name (never following it).
- A refusal resolves only when that read found the refused inode AND either that inode had one link, or this run removed that SAME inode at that name.
- "Removed" means: the device:inode that the removal's own hard-link check read immediately before the unlink, at any of the four sites.
- Otherwise the refusal is carried into `filesFailed`, with a text asking an operator to confirm the other name is removed.

**Commit messages.** Commit `b96228b9`'s message says "or this run purged it". Round 1's code checked the name there. Commit `934c7f5b` keys that clause to the inode and corrects the code comment. The first commit was not rewritten.

**Tests:**
- `__tests__/rd744-hard-link-refusal-is-carried-by-its-inode.test.js` (21 cells) and `__tests__/rd744-a-refusal-resolves-on-the-inode-this-run-removed.test.js` (7 cells).
- V1, V2, V6 and V7 were red at round 1's head and green at the head, in a Linux-like temp shape and in the machine's own (the gate ran both).
- V3, V4 and V5 hold branches no cell held before.
- Five round-2 mutations each turned red exactly their named cells (gate re-run with its own program).

**Gate shapes outside the cells:**
- Carried at the head: a replacement during the re-drive at every site under `dir/`, `dir//`, `dir/.`, `dir/zz/..`, a relative spelling and a symlinked DATA_DIR. Also a name replaced by a directory, and an unlink that fails after the check. Every one of these certified `purged` at round 1's head.
- Certified at the head: the outside name removed during the re-drive, under every one of those spellings. That is the liveness the change must keep.

**Named limits (the coordinator's defaults):**
1. No admin surface records the confirmation; the record is edited by hand.
2. A replacement in the instant between the removal's own `lstat` and its unlink. The check passing means no outside name existed at that read.
3. The census is built once per run.
4. A recovery folder aliasing another listed folder counts one name twice (pre-existing; new ticket A below).
5. A store hard-linked outside and replaced by an app write during the FIRST run: no refusal exists to carry (pre-existing; new ticket C below).
6. A carried entry stripped of `refusedInode` by a later writer is dropped. No writer strips fields today.

Hosted build of the pull request: <the `VERDICT: PASS` line>. Deploy: none; Deploy demo run for <M>: <conclusions>. State: Testing.

## RD-750: comment
Same landing; `cdcf3b9c` is this ticket's. Nothing in round 2 touches it.
- After both settle steps, a name that is in `filesFailed` is removed from `filesPurged` ("failed wins", the coordinator's default).
- `__tests__/rd750-a-file-is-named-once-in-the-erasure-record.test.js` has 9 cells.
- Across 101 probe records at the head, no name is in both lists.

**Named limits:**
1. The catch path's union (a purge that dies part-way).
2. A pre-change record that already names a file twice.
3. Two failures with one `file` are not merged.
4. When a carried failure wins, the record does not show that the replacement file at that name was deleted.

State: Testing.

## RD-745 (the backend/dataErasure.js half): comment
Same landing; `21db2207` and `abef7000` are this ticket's.
- `purgeNow` resolves DATA_DIR once, and the census compares resolved paths. Under a trailing slash, a doubled slash, a dot or dot-dot segment, or a relative `./data`, two of our own names on one inode are purged instead of refusing each other.
- `__tests__/rd745-non-normalised-data-dir-names-do-not-refuse-each-other.test.js` has 14 cells.
- The gate's seven-spelling matrix reads the same at round 1's head and at this head.

**Not in this change:**
- the Dockerfile part (lane 4);
- DATA_DIR `/`;
- a case-insensitive file system;
- a working directory that changes during a run;
- RD-424's label mapping (UNMEASURED).

State: unchanged until lane 4's part lands.

## RD-824: comment
Same landing; `471d8655` (round 1) and `76515f5b` (round 2) are this ticket's.
- **Round 1.** ENOTDIR joins ENOENT as "nothing behind the link", at the resolver and at both steps of the chain walk. EACCES and EPERM stay failures. Cell U2 of `__tests__/rd838-chain-canonical-key-and-cap.test.js` is turned.
- **Round 2, the resolver.** The resolver (`fs.realpathSync`) is lexical, so its ENOENT or ENOTDIR is confirmed by the kernel's resolution (`fs.realpathSync.native`):
  - a path the kernel reaches is the target, and a failure while it survives;
  - only a kernel ENOENT or ENOTDIR removes the link;
  - any other kernel answer keeps the link.
- **Round 2, the walk.** It joins each hop's text without normalising it, and resolves each hop's directory with the kernel.

**Tests:**
- `__tests__/rd824-link-through-a-file-resolves-to-nothing.test.js` (14 cells) and `__tests__/rd824-a-lexical-null-is-confirmed-by-the-kernel.test.js` (11 cells).
- W1 to W8 and W11 were red at round 1's head and green at the head, in both shapes.
- Seven round-2 mutations each turned red exactly their named cells (gate re-run).

**Gate shapes outside the cells:** each was certified `purged` at round 1's head, and is a failure (link removed) or kept at this head:
- a symlinked directory in the middle of a chain;
- an absolute link text through `sd/..`;
- a 41-link chain with `sd/..` mid-chain;
- a 41-link chain with an absolute `sd/..` text at its end;
- a kernel target inside the data directory.

A kernel error injected at each of the four sites and at the walk keeps the link, and the run goes on.

**Named limits:**
1. The resolver's SUCCESS answer is still lexical (pre-existing; new ticket B below).
2. A resolver answer that changes between the two calls.
3. A kernel ELOOP after a lexical null.
4. A link through a kernel loop beyond `..` is kept, so the erasure does not finish until an operator removes it.
5. macOS named forks.
6. The production image is Alpine (musl). Its `realpath(3)` has run no cell.
7. The removal log still says "dangling or looping".
8. EACCES and EPERM are injected in the cells, not real.

State: Testing, once new ticket B is filed and linked.

## New tickets to file (dup-check RD-685, RD-640, RD-838, RD-824 and RD-744 neighbours first)
**A. (round 1's Minor 1, P9, pre-existing) The RD-685 census counts one physical name twice when a recovery folder aliases another listed folder.**
- Gate probe P9: legacy folder at `<DATA_DIR>/emergency-backup`, and `.emergency-backup -> emergency-backup`. The emergency copy, hard-linked outside, is counted as two of our names. The first run certifies `purged` with the outside canary intact.
- The same at the base, at round 1's head, and at this head (re-run 13:0x).
- Reachable only with the legacy folder inside DATA_DIR.
- Fix shape: key the census by each name's real parent plus basename.

**B. (gate B2149 Finding 1, pre-existing) The resolver's SUCCESS answer is lexical, so a link can be removed and certified while the kernel reaches data through it.**
- Gate probe L1: `feedback.json -> sd/../learning_data.json`, where `sd` is a symlink to a folder outside and the local `learning_data.json` is a listed store.
  - `fs.realpathSync` answers the local store, while `fs.realpathSync.native` (and a read through the link) reaches `<outside>/real/learning_data.json` holding the canary.
  - The run records a surviving-target failure on the LOCAL path, then purges that local store later in the loop, and the settle resolves the failure.
  - Status `purged`, `filesFailed: []`, kernel canary intact. The same at round 1's head.
- Gate probe L3 (round 1's P14c): the failure names the local `f/x`. The operator removes it, as the text asks, and re-drives: status `purged`, kernel canary intact.
- When the local store is processed BEFORE the link (probe L2), this head now reports a failure, because the resolver then answers ENOENT and the kernel confirms.
- Fix shape: in `_linkTargetOrNull`, take `fs.realpathSync.native` as the target whenever it differs from the JS answer, or use it first and keep the chain walk for ELOOP.
- One new cell per shape (L1 and L3).

**C. (gate B2149 Finding 3, pre-existing, outside RD-744's carry) A store hard-linked outside DATA_DIR and replaced by an app write during the FIRST run hides the outside link.**
- Gate probe P1c: an `onPurge` hook replaces `settings.json`, which is hard-linked outside, by tmp+rename. The run removes the new inode and certifies `purged`, while the outside name keeps the earlier bytes.
- The same at round 1's head and this head.
- Fix shape for the decision: read the identity and nlink of every listed name before the purge hooks run, then refuse a name whose snapshot inode had an outside link and is no longer at the name. Alternatively, run the hooks after the census.

**D. (gate B2149 Finding 2, Minor) Branches held by no cell** (each mutant turned no cell red in 40 suites, 568 tests):
- the `purged.includes` guard in round 2's "removed here" (a noted-then-failed unlink; gate probe R5 measures today's correct behaviour);
- the inode note at the "every name is ours" return;
- recording only names the check passed;
- `path.resolve` on the recorded key.
Info unless the coordinator wants them tracked.

## LEFT FOR OTHERS (carried)
1. An operator surface to record RD-744's confirmation.
2. RD-745's Dockerfile part (lane 4), and RD-424's label mapping (UNMEASURED).
3. RD-750's catch-path union and pre-change double records.
4. A recovery copy whose own parent is a regular file; RD-684 F7.
5. The removal log wording for an ENOTDIR link.
6. The records: this file.
7. The deploy: none.
8. RD-455, RD-728 and RD-981, the later lane-2 kits. B2139 must name this landing in its stamp (the drafter report's F-2).
