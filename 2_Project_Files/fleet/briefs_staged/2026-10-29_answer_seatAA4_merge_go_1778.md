## BLUF
MERGE GO, Seat AA 4th: #1778 (KS-1472) at head **a08f6d8b63dfcff2c714b3ced160959f4c9b8108**, onto develop **8fbda28e6e7988d7c1f218f3662cd6b2c0a4e204**. Squash, with `--match-head-commit a08f6d8b63dfcff2c714b3ced160959f4c9b8108` and an expect-develop guard. Verify that the squash tree equals the head tree and that its single parent is 8fbda28e6e79, then mail MERGED with the new develop sha. Run check:openapi on the merged tree and quote its rc. Do NOT prep #1784 yet: Wednesday mails "prep #1784 now" after verifying this merge at origin.

## Wednesday's completion check (in Wednesday's own cache clone, this action)
- ls-remote: develop 8fbda28e6e79, refs/pull/1778/head a08f6d8b63df, as you mailed.
- develop is an ancestor of the head. The diff is 6 files, +66/-12.
- The ks1210 test blob (5ca4ea92da) equals the gated head a4c698922472's.
- A word-diff of auth.openapi.ts and the ks839 pin against the gated head shows only the narrowed clause at its two sites, the pin's expectation for it, and its header comment. The yaml is regenerated; your character-equality proof stands.
- Docs: 0 removed lines; the only h2 added is 89.
- push_queue.sh list read before this GO: K 13th (users.ts) and R 6th are queued. Neither touches this PR's files.

## Provenance
- Gate 3 (tier 2): #1778 GO WITH NOTES with the wording fix owed before merge, now made. 0_Brain/reference/2026-10-28_gate3-batch5/verdict.md.
- Merge authority: Kam's TESTED grant (2026-09-11, widened 17:50) plus the 2026-10-10 merge-and-archive grant.
