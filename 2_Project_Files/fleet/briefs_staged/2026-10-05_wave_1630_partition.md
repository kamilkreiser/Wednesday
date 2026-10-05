# Secuura wave 16:3x 2026-10-05 — partition (Wednesday, the single source for every brief in this wave)

Authority (Kam, live board, verbatim, all view=wednesday):
- 16:21:39 card `secuura-connector-allowlist-missing-setting-ks1256-1005` = **b** "Keep 'no restriction' when unset" | note: *"for the month of October, keep pushing, keep publishing, deploy all that works and is ready but only when its ready.  Deploy to both servers, demo and kintsugi"* → grant `0_Brain/learnings/2026-10-05_october-deploy-both-boxes-when-ready.md` (expires end of Sat 2026-10-31; Wednesday's reading: ready = merged on a gate GO + verified at source; kintsugi first + live sweep, then demo; KS-535 wallet rule; production/money/comms to Peter-Stuart/irreversible unchanged).
- 16:21:47 card `secuura-tenant-isolation-migration-ks1401-1005` = **a** "Write the migration now, apply with the kintsugi deploy".
- 16:21:55 card `secuura-tooling-tickets-off-product-board-1005` = **a** "Move the 192 of ours to a separate Linear project 'Internal tooling'".
- 16:22:05 card `secuura-kintsugi-deploy-for-31oct-1005` = **a** "Deploy develop to kintsugi now, then a live-sweep seat".
Read each card with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show <id>` for its full options/BLUF.

develop at origin: `46c3e20cfbd21acee0c67d544180c33deaa4c8ef` (Wednesday ls-remote 16:2x; re-read it).
Audit: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-05_ks-ticket-audit/` (SUMMARY.md, audit_{A,B,C}.tsv — the 192 tooling list is derived there).

## Seats (live + new). Every brief names every row here, from BOTH sides.
| Seat | Pane (cockpit name) | Token / lock | Scope (files) | Ref writes |
|---|---|---|---|---|
| **Seat E 2nd** (LIVE, %24) | `Secuura/Blockchain-E` | `e2` / `worktrees/.push-lock-e2` | auth: `routes/users.ts`, `routes/oauth.ts`, `services/oauth.ts`, `routes/mfa.ts`, ks1005/1210/938 tests; doc blocks 18./19./20. (21. reserved KS-1256) | yes |
| **Seat B 61st** (NEW) | `Secuura/Blockchain` | `b61` / `worktrees/.push-lock-56` | merge #1381; B 60th's rows 3-6 (KS-1388 observability/scripts tests, KS-1278 documentRepo/documents.ts, KS-723 anchoring.openapi + YAML, KS-948 scripts test); Spark HOLDs; doc blocks 13.-17. + new by ticket | yes |
| **Seat F 2nd** (NEW) | `Secuura/Blockchain-F` | `f2` / `worktrees/.push-lock-f2` | KS-1401 / KS-1376 tenant-isolation MIGRATION: `Blockchain/Dev/services/*/migrations/` (new numbered migration only) + its test; doc block by ticket number | yes |
| **Seat D 7th** (NEW) | `Secuura/Blockchain-D` | `d7` / NO git lock (box work only) | kintsugi DEPLOY of develop + live sweep; demo only after kintsugi sweeps clean (October grant) | NO ref writes in the repo |
| **Seat C 23rd** (NEW) | `Secuura/Blockchain-C` | `c23` / none | Linear BOARD ONLY: create project 'Internal tooling', move our 192 tooling tickets (never Peter's/Stuart's) | NO git |

Lock rule for the three pushers (E 2nd, B 61st, F 2nd): each takes its own lock; WAIT on the other two live pushers' locks (20-min bound, take/re-check order); STOP on every other `.push-lock-*` incl. `-55` (B 60th WRAPPED 05:23Z), `-e1`, `-f1`, `-54`, `-d6`, `-d5`, `-c21`, `-d4`, `-d3`, `-d2`, `-53`, `-52`, `-51`. Wednesday sends Seat E 2nd the mirror ADDENDUM (add `-56`, `-f2` to WAIT; `-55` to STOP) before either new pusher's first ref write; each new seat's ITEM 0 proves the mirror.

Doc protocol: blocks numbered by TICKET (Q-E1), merge-ins place by number order, never renumber; catch up by MERGING develop IN; NO force push ever.

Ordering: D 7th deploys develop as it stands NOW (46c3e20c) to kintsugi; #1381 and the KS-1401 migration reach the box in a LATER deploy after they merge (the migration is applied "with the kintsugi deploy": D 7th's brief names that as its follow-up round, not this one).
