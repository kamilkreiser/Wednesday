# nas_sync fixtures (captured 2026-09-21)

- `2026-09-21_033004_tail_67failed.log` — the last 16,000 bytes of the real 03:30 run log
  `scheduler/logs/nas_sync_wednesday_2026-09-21_033004_25224.log`, raw (carriage returns kept: 223 of them).
  Holds unison's summary `Synchronization incomplete … 67 failed` and all 67 `  failed: <path>` lines
  (two leading spaces — a `^failed:` anchor matches 0). One path contains a space (`Notes (MASTER)/…`).
- `2026-09-11_033003_clean_skipped.log` — a real run log with NO unison output (the engine skipped on
  its lock). Zero `failed:` lines; the parser must return nothing and the retry must be skipped.
- `scratch_clean_complete.log` — a `Synchronization complete … 0 failed` run captured from the
  local scratch-pair probe of 2026-09-21 (no NAS involved): a clean log WITH unison output.
- `scratch_confirmbigdel_abort.log` — the same probe's abort: `The following paths have been completely
  emptied in one replica:` / `  'd/gone.txt'` / `Aborting...` (rc=3). What `nas_emptied_paths` parses.

Used by `fleet/tests/nas_sync_retry_arms.sh`. Never run unison against these; they are text.
