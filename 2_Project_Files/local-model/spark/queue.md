# spark/queue.md — briefs waiting for the Spark, drained by spark/queue.sh (one round at a time, first line first).
#
# FORMAT: one brief per non-comment line:   <brief_dir> [pin=value ...]
#   brief_dir  absolute, or relative to local-model/night/briefs/ (e.g. `KS-1388-envexample`). The dir holds exactly
#              one KS-<n>.md brief (kit 03 shape) and, optionally, golden.diff and spark.pins.
#   pins       builder pins (product= ref= test_file= line= ctx= started_ok= supersedes= ...) plus the round-only
#              tier=code_patch|bash_patch and allow_drift=1. No spaces inside a value. Pins in the brief dir's
#              spark.pins are read first; pins here win per key.
# When a round ends its line is REMOVED from here and a row goes to spark/done.md. Lines starting with # are ignored.
# Only queue a brief whose builder already ran rc 0 on it (kit 03 "BEFORE HAND-OVER"): `round.sh <dir> --dry-run` does that.
# 2026-10-07 17:38 WHY EMPTY (evening seat): the 11:20 and 15:20 screens read the whole KS Backlog+Todo (276, paginated) at develop 147ae442074c and found 2 briefable tickets, both run and PASSED; develop is unmoved and only KS-1438 is new since 11:20, so a third screen now repeats them. Re-screen when develop moves (gate73 merges) or new KS tickets are filed.
