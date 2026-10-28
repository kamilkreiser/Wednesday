## BLUF
MERGE GO, Seat R 7th: #1793 (KS-1250, the smoke-test.sh SMOKE_BASE_URL fix) at head **87ec5aa213ae575c826af64aacc243a6b8c414ef**, onto develop **41b984e0f5223b3936bc9356766033152198ad2e**. Squash with `--match-head-commit 87ec5aa213ae575c826af64aacc243a6b8c414ef` (or merge_one.py, dry run first); read develop by ls-remote first. Five reads, then mail MERGED. Do not run smoke-test.sh against any box (KS-1250's pause, unchanged). Next: Seat U 5th takes one turn (#1800). Your #1797 waits for its turn mail.

## Wednesday's completion check (in Wednesday's own cache clone, this action)
- fetch rc 0: head 87ec5aa213ae. Its parents are 29989b01ab05 (gate 8's pin) and 41b984e0f522. Both are ancestors of the head.
- 4 files differ from develop. smoke-test.sh and smoke_test_honours_smoke_base_url.test.sh equal 29989b01ab05's blobs.
- Docs: Flow +16/-0 and Cheat Sheet +19/-0. One h2: "101. smoke-test.sh reads SMOKE_BASE_URL for its gateway and prints the target it ...".
- push_queue.sh list was read before this GO: empty.

## Provenance
- Gate 8 (tier 2): #1793 GO WITH NOTES, 0_Brain/reference/2026-10-29_gate8-batch/verdict.md. Merge authority: Kam's TESTED grant (2026-09-11, widened 17:50) plus the 2026-10-10 merge-and-archive grant. Your PUSHED mail, 20:29Z.
