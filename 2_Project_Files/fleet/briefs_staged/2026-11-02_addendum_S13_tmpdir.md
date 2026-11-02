Seat S 13th

ADDENDUM to your brief's PUSH section (one line; everything else stands):
The push's TMPDIR must be SHORT: a path like /private/tmp/s13t (under ~40 characters), NEVER your scratchpad or evidence folder. The pre-push hook's tsx IPC socket path must stay under macOS's ~104-byte limit (KS-1135). Seat R 74th's first push today failed preflight leg 1 ("spec drifted", over a 'port -1' pipe error) on a 122-character TMPDIR and lost ~24 min of the shared lock. "Created and asserted present" means mkdir it and test -d it, not move it.

Wednesday
