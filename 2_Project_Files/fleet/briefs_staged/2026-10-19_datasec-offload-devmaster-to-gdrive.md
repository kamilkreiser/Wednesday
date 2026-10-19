# BRIEF — move Datasec off DevMASTER to G-DRIVE (copy → verify → remove)

**Commissioned by:** Wednesday seat 18:2x, 2026-10-19.
**Authority:** Kam, live board 2026-10-19 18:22:11 AEDT, view=wednesday, verbatim:
*"It looks like we are starting to run out of space on a more regular basis. From now on, this drive will not hold any Datasec files. Keep the efficiency rules alive and offload anything old / unnecessary to G drive or clear but do not sync or keep any Datasec files on this drive. Remove Datasec from this drive"*
This instruction is your authority to edit the sync profile (step 1) and remove the source (step 4) — **and only those two things**.

**Model:** Opus. Routing row C4 (a path that destroys data).

## SCOPE (exact)
- SOURCE: `/Volumes/DevMASTER/!CODING/Datasec` — the whole folder, 23 entries, ~99 GB by du. Measured 18:2x: no file modified in the last 2 days (node_modules and .git excluded).
- DESTINATION: `/Volumes/G-DRIVE/DEVELOPMENT WORK/DevMASTER-Datasec-offload_2026-10-19/Datasec` (create it; G-DRIVE had 3.3 TiB free at 18:2x).
- SYNC PROFILE: `/Volumes/DevMASTER/!SYNC FILES/devnas.prf`.
- **OUT OF SCOPE — do not touch:** `/Volumes/DevMASTER/TUESDAY`, `/Volumes/DevMASTER/Notes (MASTER)/` (any of it), anything under `/Volumes/DevMASTER/WEDNESDAY` except your report, every other `!CODING` client, and every other file on G-DRIVE.

## HARD RULES
1. **Never print, cat, grep or copy-paste a file's CONTENTS from Datasec.** Use names, counts, sizes and hashes only. `.env` files and keys get copied like any other file, and their contents never appear in output.
2. **No git write verbs in any Datasec repo** (no commit, checkout, stash, gc, fetch). Read verbs only: `rev-parse`, `status --porcelain`, `stash list`, `for-each-ref`. Use `git -c safe.directory='*'` on the G-DRIVE side.
3. **Stop on any mismatch** in step 3. Remove NOTHING. Report what differs.
4. **G-DRIVE is additive.** Never delete or overwrite anything outside the new destination folder.
5. Never discard stderr. Log each step to `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_datasec-offload/logs/`.
6. zsh is the Bash tool's shell: it has no `PIPESTATUS`. Redirect to a file and read `$?`.

## STEPS
**0. Preflight. Any failure here means STOP.**
- `pgrep -fl unison` and `pgrep -fl devnas-sync`. If either returns anything, STOP (a sync is running).
- `lsof +D "/Volumes/DevMASTER/!CODING/Datasec"`. If any process has a file open there, STOP and name the process.
- `df -k /Volumes/DevMASTER /Volumes/G-DRIVE`: record both.

**1. Make the sync engine ignore Datasec. This MUST happen before step 4.** Without it, the next "Sync All Drives" would propagate the deletion to the NAS, the T9 and the laptop.
- `cp -p devnas.prf devnas.prf.pre-1019-no-datasec`.
- Append to the ignores section a dated comment citing Kam's 18:22:11 instruction, followed by `ignore = Path !CODING/Datasec`.
- Verify the line is there with `/usr/bin/grep -n`, using a positive control (an existing ignore line in the same file).
- Read `devnas-sync.sh` and `Sync All Drives.command` (read only) to confirm `devnas.prf` is the profile the engine actually uses. If it uses another profile, STOP and report.

**2. Copy.**
- Prefer `/opt/homebrew/bin/rsync -aHX --info=progress2` if it exists; otherwise `/usr/bin/rsync -a`.
- Source with a trailing slash, into the destination folder. Log to a file.
- If it is interrupted, re-running is safe.

**3. Verify. All checks must be EQUAL on both sides.**
- Counts: `find … -type f | wc -l`, `-type l`, `-type d`.
- Total bytes of regular files: sum `stat -f %z` over the files, on both sides.
- Content: sha256 over a random sample of 300 files, PLUS every file under 1 MB whose name contains `.env`, `key` or `cred`. Compare the hashes and print only the PASS/FAIL count.
- Every git repo (`find SRC -name .git -prune`; it may be a directory or a file). On both sides, compare: HEAD sha, `status --porcelain | wc -l`, `stash list | wc -l`, and the sha256 of the `for-each-ref` output.
- Run the controls first:
  - one known-different pair must read UNEQUAL (for example, compare the two sides' first repo HEAD against a different repo's HEAD);
  - a missing-file case must be detected.

**4. Remove. Only if step 3 is all-EQUAL and step 1 is verified.**
- Re-run the step-0 preflight checks.
- Then `rm -rf "/Volumes/DevMASTER/!CODING/Datasec"`.
- Confirm the path is gone, and that the destination's counts are unchanged.
- If a hook refuses the removal, STOP and report the hook's message verbatim. Do not work around it.

**5. Report.** Write `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-19_datasec-offload/REPORT.md`, BLUF first, covering:
- df before and after;
- every count and sum on both sides;
- the sha PASS count;
- the repo table (folder name, HEAD sha, dirty count, stash count, equal yes/no);
- the profile diff;
- anything you did NOT do.

Names, counts and hashes only; no file contents.
