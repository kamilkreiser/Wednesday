From Tuesday (Datasec coordinator seat), Datasec / MPS Calculator. ADDENDUM-1 to your kit B1405 (SEAT-M106). Every hold, partition and housekeeping rule of the kit still binds you. HARD STOP 10:31:46 AEDT 2026-11-10 as you wrote it.

# ROUND-2 FIX: the MPSCALC-124 commit (4f61a22) writes attachment files outside the store's lock

The tier-1 gate returned **NO GO** on your branch at 2c7d5c2. Read its record WHOLE first: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1405_verify/VERDICT.md`.

What it measured, in throwaway copies (head vs main):
- 16 concurrent uploads with distinct keys, limit 1 per hour: head stores 1 item but leaves 16 attachment folders, 128 MiB on disk. Main: 1 folder, 8 MiB.
- 16 concurrent uploads with the same key and body: head leaves 7 folders, 56 MiB. Main: 1 folder.
- An upload held mid-write while a second is stored answers 429, and its files stay on disk.

So a refused upload (429, 200 replay, or 422 reused key) leaves files that are never removed. A signed-in user can fill the disk past the hourly limit. Your other four commits (MPSCALC-97, -102, -122, -125) passed every check.

## THE FIX (Tuesday's ruling, the gate's own recommended shape)
- **Under the FIRST acquisition of the store's lock**, before any attachment byte is written, reserve the (caller, idempotency key) pair and one hourly-limit slot. A request that is a duplicate, a replay or over the limit is refused **before it writes anything**.
- A reservation that does not complete releases its slot and key on every failure path. Prove this with a test that fails the write midway.
- **Do NOT** use the other shape, deleting the losing request's own folder. It conflicts with the project's "never delete" rule, and choosing it is the product owner's call. If you find the reserve-first shape impossible, STOP and say why.

## PROOF (in STATUS under `## ADDENDUM-1`, each with output)
1. **New test rows built from the gate's probes:**
   - (a) 16 concurrent distinct-key uploads at limit 1 per hour: exactly 1 attachment folder and 8 MiB;
   - (b) 16 concurrent same-key uploads: exactly 1 folder;
   - (c) the held-mid-write upload refused with 429: 0 files of its own on disk.

   Each row is RED at 2c7d5c2 (show the counts) and GREEN at your new head.
2. **The full dotnet job** (build with 0 warnings, all test projects), at the new head and at the merge with current main (re-read main; it was 089a6393). Counts compared: nothing lost.
3. **The 21 earlier new rows** still go red without their fixes, and the 249 existing Feedback tests stay green.
4. **Forward commits only:** no amend, rebase or force-push. Commit messages in plain ASCII with no B-number or name, ending with your attribution line. Then `git push origin <your branch>`.
5. **`docs/API.md:725` and `:749-750`** belong to lane M11. Do not edit them. Write one line in STATUS saying whether, after your fix, both sentences are true again, and read the file at main to decide.

**Last line** when done: `READY B1405: <new head sha40>`, or `STOPPED: NEEDS TUESDAY <one question>`.
