# Gate brief: GATE AA1 = PR #1615 (KS-1603), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat J 15th's READY FOR GATE of 07:59Z. The author's CLAIM is beside this brief: `J15_READY_0759Z.txt`. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/aa1/`.

**What it is:**
- **The defect:** anchoring's `dbPersistAnchor` `ON CONFLICT (document_id, network) DO UPDATE` let any authenticated caller from any tenant overwrite twelve columns of another tenant's anchor row (status, hashes, block, simulated, …).
- **The fix:** an interim ownership check in `anchorOverwriteGuard.ts`, called from `dbPersistAnchor` (the one persist site for the flat `:507` and batch `:804` routes). It has four parts, as ruled by Wednesday:
  1. a transaction-scoped `set_config(..., true)` bypass GUC around ONE EXISTS read;
  2. tenant-equality narrowing only;
  3. fail-OPEN plus a warn on a probe fault (the worst case = develop's behaviour);
  4. the batch route reads every id up front, so there is no partial write.
- **The residue:** the TOCTOU race and originate's second upsert go to KS-1650.
- **Kam's ruling:** card `secuura-ks1384-schedule-per-event-anchors-1019` = b says "the interim ownership check (KS-1603) goes ahead now on its own".
- **Heads:** #1615 head `4db96203546b76e383b40b4e3806cca8ba4171b0`. **Develop MOVED after the author's READY:** it read `31cfb44dce840caf8ae8a6a4c1468efa7e78e247` at Wednesday's ls-remote 19:0x AEDT (most likely #1613 merging; confirm with `git log`). The author predicted landing tree `1cd95487cc12` on the OLD tip `722e07f19cee`, so that prediction is void.

## Questions (each with its instrument; name what you did NOT run)
1. **Does the bypass stay inside its transaction?** Read the code. Then run the D1 cell, plus one cell of your own on the same pooled connection: after the guarded write's transaction ends, a fresh query on that connection as `secuura_app` must again be refused by FORCE RLS on another tenant's `documents` row. A GUC that outlives the transaction on a pooled connection is the blocker class here.
2. **Is the narrowing right for every caller shape?**
   - same tenant: allowed;
   - another tenant's document: refused 403;
   - an `anchor_store` row whose `document_id` names NO document (S's flat rows): allowed, as today (the residual is KS-1384's);
   - batch with a mix: refused before any write, so no partial write (count rows before and after).
3. **Fail-open is bounded:** a probe that throws allows the write AND logs the warn naming KS-1603. Prove it with the author's cell, and plant your own fault.
4. **Red-first and controls are real.** Re-run the 14 cells with the two product files parked at develop's copies and expect 8 red / 6 green as claimed. Plant one mutation of your own (for example, drop the tenant equality) that must red a cell. Restore byte-identical, by sha256.
5. **Suites on the LANDING tree:**
   - merge-tree #1615 onto the LIVE develop: re-read ls-remote at start and again before the verdict;
   - anchoring integration (claim: 103/103 at the head) and unit (379/380, one failure the author says pre-exists at develop; re-prove it on the landing parent);
   - tsc, including the test files;
   - the three-dot file list must be exactly the 4 files.
   Use a scratch PostgreSQL on a port in 55410-55419, built from `docker/init/*` + the repo's migrations. Confirm the per-file `[main] Applying` lines (the prefix is `[main] ` / `[platform] `).
6. **Overlap:** #995 (KS-741, stale since 09-14) also touches `anchoring/src/index.ts`. Confirm #1615 does not make #995's state worse in a way that matters, by naming its conflict hunks. This is a note, not a blocker, unless you find otherwise.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 4db96203546b... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of the file with its first and last lines removed, computed as `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`.
- No `cd` (use absolute paths and `git -C`), no `rm` (quarantine), no stderr to /dev/null, no Docker on this Studio.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS, so redirect to a file and read `$?`.
