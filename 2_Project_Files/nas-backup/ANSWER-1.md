# ANSWER-1 to the nas-backup seat (from Wednesday, 2026-11-27)

Read this file WHOLE before acting. It is a new, separate task. Your lane's code is under an independent QA check right now: do NOT edit any file of the lane's code, tests, proposals, STATUS.md, README.md or CENSUS.md while that check runs. Write only the new files this task names.

## RULED BY KAM (live board, 2026-11-27 13:36:06, view=wednesday, verbatim)

"Decision wed-nas-backup-share-holds-secuura-credentials-1127: a — Move them aside on the NAS and exclude them"

The card's option a, verbatim: "a seat moves the two folders into a quarantine folder on the same share (a move, never a delete; listed first, counted after), sweeps the mirror for any other credentials or keys folder and reports, and the job gets the two excludes".

This ruling licenses, on the REAL Backup share, exactly: the move of the two named folders (step 2) and a read-only sweep (step 3). Nothing else. Your BRIEF's hold "nothing written to the NAS" is lifted for step 2 ONLY.

## Already done by Wednesday (do not redo)

`2_Project_Files/scheduler/nas_push.sh` line 109 now carries `4_Credentials 3_Access_Keys` in its exclude names (backup beside it: `nas_push.sh.pre-1127-secrets-exclude`; `bash -n` rc 0; NOT exercised by a run). So tonight's 03:30 job will not re-copy them.

## Step 1: list first (read-only)

For each of
- `/Volumes/Backup/DevMASTER-mirror/!CODING/Secuura/Blockchain/4_Credentials`
- `/Volumes/Backup/DevMASTER-mirror/!CODING/Secuura/Blockchain/3_Access_Keys`

record, by a program (os.walk, hidden names included): entry count at the top level, total file count, total directory count, total bytes. NAMES ONLY: never open, cat, hash or copy the CONTENT of any file in them; COUNTS ONLY everywhere: do not print or write the file names inside them to your pane, to mail or to any file.

If either folder is absent, or `/Volumes/Backup` is not the smbfs mount (check with `mount`), STOP and write that into the result file.

## Step 2: the move (the only write)

- Destination: `/Volumes/Backup/_quarantine_2026-11-27_secuura-secrets/` (at the share's root, OUTSIDE `DevMASTER-mirror`, so the nightly job never sees it). Create it; refuse if it already exists with content.
- Move each folder with a same-share rename (`mv` / os.rename), to `<quarantine>/4_Credentials` and `<quarantine>/3_Access_Keys`. A rename, never copy-then-delete. If a rename fails (rc non-zero, cross-device error), STOP there: do not fall back to a copy, do not delete anything. Read rc after EACH move before the next step; never chain them.
- No `rm`, no `rsync --remove-source-files`, no delete verb of any kind, anywhere.
- First confirm no `nas_push.sh` or rsync process is running against the mirror (`pgrep -fl`), and say what you read.

Then count after: the same four figures for each folder at its new place must EQUAL step 1's; the two original paths must not exist (os.path.exists False for each, with a positive control: the `Blockchain` parent still exists). Any inequality: STOP and report; fix nothing.

## Step 3: sweep the mirror (read-only)

Walk `/Volumes/Backup/DevMASTER-mirror` and report every DIRECTORY named `4_Credentials` or `3_Access_Keys` (case-insensitive), and separately the COUNT (not names, not contents) of files named `.env` or starting `.env.` and of files whose name ends `.pem`, `.key`, `.p12`, `.pfx` or is `id_rsa`/`id_ed25519` (with or without `.pub` reported apart), grouped by the top two path levels under the mirror (for example `!CODING/Secuura`). Positive control: before step 2, the walk must find the two known folders; state that it did. This walk may be slow over SMB: run it as a background job that exits, and name that as your wake path. Do NOT move or touch anything the sweep finds: it is a report for Kam. Client care: you will see other clients' folder NAMES at the top levels; report paths only down to the secrets folder's own path, and nothing from inside any of them.

## Deliverable

`2_Project_Files/nas-backup/RESULT-secrets-move.md`: first line `DONE`, `STOPPED` or `WORKING`; then FOUND / TESTED (and what was NOT tested) / HOW (commands, controls, rc values), the before and after counts in one table, the sweep table, and anything you noticed. Evidence output under `evidence/secrets-move/`.

Also say plainly, as a limit: the quarantine folder is on the same share, so whoever can read the share can still read it; whether the keys in it should be rotated or the folder removed is Kam's next decision, not yours and not mine.

When the first line reads DONE or STOPPED, end your turn; the idle-pane wake brings Wednesday to you. Commit nothing, push nothing.
