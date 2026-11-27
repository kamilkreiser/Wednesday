# B2192 install steps: the candidate jest lock (RD-1052), AFTER the RD-1051 merge

Who: a NexusAI seat on Tuesday's commission (Tuesday manages and does not write into NexusAI's `session-tools/`). When: only after the merge commit M of the RD-1051 pull request is on main (landing.txt step 3), and only while the live base is idle. What: the candidate replaces the live script; **`slots-jest` is NOT written**. With the file absent the candidate runs one jest slot, which is exactly today's mutual exclusion. The gate proved this in A6, and N186 proved it in S4 and ARM I. Writing `slots-jest` is a separate step, held by VERDICT.md M-1 and m-2.

The form is N186's dry-run script `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b2175/lock/install-b2175.sh` (B702's install-847 form, run once against a stand-in at 23:53:45, `INSTALLED OK`). For the real run, the seat's copy changes only these values:
- `ST` becomes `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools`;
- `LB` becomes `$ST/locks-laptop-1017`;
- `OUT` becomes the seat's own log.

Every other line stays token for token.

## Values (gate read, 01:13 AEDT 28 Nov)
- LIVE  `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/nexusai-lock.sh`, sha256 `cf01bafbc51f555ca0f14d1711f01885bcec5bc6293b177fe24702226bb4971f`, 391 lines.
- CAND  `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b2175/lock/nexusai-lock.sh.candidate`, sha256 `52713e55345726abc769c4601cc52daf5b5496eab96b346ebacaada300356260`, 498 lines.
- LB    `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017`. At 01:15 it held `queue-docker queue-jest released`, with no lock directory, no tickets and no `slots-jest`.

## Steps
0. **Preconditions.** Main = M and contains `fc5975f631bb1fdd2536345f8eeee9e2e4eec165`. Check this with `gh api -X GET .../compare/fc5975f6...main` and expect `ahead` or `identical`, behind 0. `$LB/slots-jest` must not exist (`[ ! -e "$LB/slots-jest" ]`); if it does, STOP and report.
1. **Idle read, twice, 10 s apart, immediately before the swap.** Both reads must show:
   - no `nexusai-jest.lock*` and no `nexusai-docker.lock*` directory;
   - 0 tickets matching `^[0-9]` in `queue-jest` and in `queue-docker`.

   Any lock script is either queued or holding, so two idle reads prove no copy of the old script is live. Any other reading: STOP, wait for the base to drain, never break or `--replace` a holder.
2. **Pre-copy (kept, never consumed).** `cp -n -p "$LIVE" "$ST/nexusai-lock.sh.pre-b2175-<UTC stamp>"`. Its sha256 must be `cf01bafb...4971f` and its mode `-rwxr-xr-x`. First run the `cp -n` control from the dry run: an existing name is left alone.
3. **The copy.** `cp -p "$CAND" "$ST/nexusai-lock.sh.new-b2175"`. The copy goes into the SAME directory as the live file, so the rename that follows is atomic. Its sha256 must be `52713e55345726abc769c4601cc52daf5b5496eab96b346ebacaada300356260`. `.new-b2175` must not exist beforehand.
4. **One atomic rename, never a copy over the live file.** `mv -f "$ST/nexusai-lock.sh.new-b2175" "$LIVE"`. Why `mv`: bash reads a script by offset while it runs. A copy or an editor save that writes in place could let a process still running the old script read bytes of the new file at old offsets. A rename gives the live path a new inode, and any old process keeps reading its own.
5. **Sha check and read-back:**
   - sha256 of LIVE = `52713e55...356260`;
   - sha256 of the pre-copy is still `cf01bafb...`;
   - `stat -f '%Sp %u %g'` of LIVE = `-rwxr-xr-x 501 20`;
   - the inode has CHANGED;
   - `.new-b2175` is gone;
   - `bash -n "$LIVE"` and `/bin/bash -n "$LIVE"` both give rc 0;
   - `$LB/slots-jest` is still absent.
6. **Smoke run, the first real acquisition.** Use a no-op job: `NEXUSAI_LOCK_BASE="$LB" bash "$LIVE" jest b2192-install-smoke /usr/bin/true`. Expect `jest lock acquired ... after 0s`, then `released`, rc 0. The record `released/done-jest-b2192-install-smoke-*/owner` must hold `slot=1` and a `wslot=` line. The seat's cwd is the NexusAI root, which has no `__tests__`, so expect `wslot=unknown`.
7. **The rollback line.** Use it on ANY red in step 5 or 6, or on any lock behaviour a seat reports as wrong after the install:
   `cp -p "$ST/nexusai-lock.sh.pre-b2175-<stamp>" "$ST/nexusai-lock.sh.new-b2175" && mv -f "$ST/nexusai-lock.sh.new-b2175" "$LIVE"`
   This never consumes the pre-copy. Then the sha256 of LIVE must be `cf01bafbc51f555ca0f14d1711f01885bcec5bc6293b177fe24702226bb4971f`. Roll back only while the base reads idle; if a holder is live, wait for it, because the rename does not disturb it either way.
8. **Tell the fleet in the same step.** Kits that pin the live lock's sha256 (N187's Step 0 and READY lines do) will now read `52713e55...`. The kit template's expected value changes with the install. Otherwise the next seat's REFUSE check stops it for a reason that is not a fault.

## What the install changes for a seat (with `slots-jest` absent)
- Nothing in who runs when: one jest holder at a time, the same FIFO, `--after`, `--replace` and MERGE-FIRST.
- The owner file gains `slot=1` and `wslot=<n|unknown>`. The waiting line names every holder and, when the head waits for a reason, gives that reason.
- Each call runs `node` once in the caller's cwd when `__tests__/helpers/test-server.js` is there. It never fails the lock.
- A seat started under the old script, at the install moment:
  - an old WAITER keeps running the old code. It competes for slot 1 only, which with one slot is the same lock;
  - an old HOLDER's owner file has no `wslot`, so a new head waits for it (X1b).

  Neither can make two holders while `slots-jest` is absent.

## Not in this step
- Writing `$LB/slots-jest`. Before anyone writes it, VERDICT.md M-1 must be answered (a tree from before M still uses 38900-38939, and two such holders collide whatever their slots). m-2 must also be answered, or slots buy nothing. Writing it also needs its own idle-twice read, because an old-script waiter beside a slotted base can take slot 1 next to a holder on the same worktree slot (X1).
