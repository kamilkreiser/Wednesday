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
KS-1435-transfer-reject-signature-typed
KS-591-transfer-custody-holder-id-uuid
KS-1432-apigw-ks529-guard-real-predicate
KS-591-platform-tenant-id-uuid
