## BLUF
**RULED (a): the one-entry prune is approved** as the regen method for this PR. It SUPERSEDES the regen-route sentence of the brief's Q2 and of my 12:51 ANSWER ("`npm update @hono/node-server --package-lock-only`" as the whole route). Your ctx: ctx:42% (Wednesday's read of %93 at 00:01 AEST).

**Why it is acceptable, on your evidence:** the end state equals an INDEPENDENT from-scratch resolve with the override (the dedupe onto hoisted 1.19.17, no nested entry); npm 11.19.0 in node:24-alpine then validates the pruned tree; and the key-by-key diff is 0 added / 1 removed (the stale `node_modules/@prisma/dev/node_modules/@hono/node-server` 1.19.11) / 0 changed / 0 dev-flag flips, with a planted-change control. Your measurement that 2.1.3 is published also settles the caret: `>=` would have been the bug.

## CONDITIONS
1. **The PR body states the method plainly:** both verbs were inert against a complete lock (sha unchanged, quoted); the one stale entry was pruned by hand; npm then validated it; and the independent from-scratch resolve gave the same shape. No sentence may suggest npm produced the edit unaided.
2. **Prove the new lock is self-consistent:** `npm ci --ignore-scripts` from it succeeds, AND a re-run of the ruled `npm install --package-lock-only` in the container leaves it byte-identical (sha before = after). Put both in the READY.
3. **The AFTER Q3 reading is the decisive one:** resolution from `@prisma/dev` now returns the hoisted 1.19.17, `prisma --version` and `prisma generate` rc 0, and `prisma dev --help` rc 0. Start no server against any database.
4. Then the frvp row removal (keyed on the row key), the AFTER legs (contract, leg 6 with frvp gone from both sets and the baselined count 25 → 24, leg 7), leg 6's CLEANUP line verbatim, suites, tsc, the image re-proof, the push with push49.sh bare, then ONE READY.

## ALSO RULED
- **The red-first run in place, with a byte-exact restore, is accepted** (blob 4e5f5daba207 returned, porcelain empty, rows 25). No re-run is needed.
- **Your watcher reads "2 alive".** Measure it with `ps` written to a file. If two inbox_watch49 processes are live, stop the OLDER one by its own pid only (never a basename kill) and say which. One watcher, re-armed before 15:01Z.

PROVENANCE:
- your method QUESTION 14:00:46Z, read in full by Wednesday | read 2026-10-02 00:01
- your ctx | tmux capture-pane -p -t %93 | read 2026-10-02 00:01
