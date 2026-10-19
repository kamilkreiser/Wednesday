# Gate brief: GATE AH1 = PR #1620 (KS-1402 invited-stub holder) DELTA, Opus, tier 1, round 2 of 2 (THE CAP)

Commissioned by Wednesday after Seat C 26th's READY FOR DELTA GATE (09:34Z). The author's CLAIM is beside this brief: `C26_READY_DELTA_0934Z.txt`. Round 1's verdict (gate AF1, NO GO, 2 blockers, 9 notes) and its brief are in `../2026-10-19_gate-AF1-pr1620-ks1402/` (read `verdict.md` there WHOLE first). Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/ah1/`. Fresh clone: `git config core.hooksPath .githooks` is not needed (you never push), but build `packages/shared` first and run Prisma via `npm run generate --workspace=services/originate`.

**Heads:** #1620 head `217967041265881fc011987d2b47245b76f8a16b` (round 1 was `dbb00e65dfb04abf6886237a76aaf3b2860ac3cb`). develop `f321e95aa9958153cfd8312223694e5e40b906b3` at the READY (re-read at start and before the verdict). The author predicts landing tree `1647a604848ef6f5ed0ed617bbcd571eaad8d404`.

**This is round 2 of 2 under the cap.** A NO GO here ships nothing and the residue is ticketed; there is no round 3 without Kam. So be exact about what blocks.

## Questions (each with its instrument; name what you did NOT run)
1. **B1 (race fallback) closed?** Auth `createUser` upserts `ON CONFLICT (email_lookup_hash) DO UPDATE` and leaves `id` out of the SET list (author cites `userRepo.ts:692-698`, `:732`, `:768`; READ them yourself). The fix: on a re-read miss, retry the local resolve by `email_lookup_hash` once, refuse only if that misses too. Measure on scratch PostgreSQL (55410-55419, `docker/init/*` + every migration incl. 052), not only with mocks: the race loser records the WINNER's id, no false "outside this tenant" alarm/log line fires, no second user row. Is the retry bounded (exactly once) and does a genuine foreign-tenant miss still refuse 404 with no disclosure? Kill mutant B1m yourself and plant one of your own (e.g. retry by email but with no tenant predicate).
2. **B2 (200 alreadyExisted branch) closed?** Run mutant A1 (skip the re-read only on a 200): it must red the new B2 cell and nothing else (author: 1 failed / 13 passed). Plant your own variant (re-read on 200 but ignore the result).
3. **Notes the author says it fixed:** N5 (non-UUID id -> 502 via the file's UUID_RE), N4 (auth 400 mapped back to 404: is that right for Platform S's contract? read the route's format check), N3 (scope lines at `platform.ts:591-595`; the real tripwires are api-gateway `ks843-erasure-scope-gate` F-2 and auth `ks564-connector-stub-auth`: confirm both exist and red if `certifications:write` is withdrawn, or say you could not run auth), N8 (20 re-pinned cells, not 19), N1 on KS-1655 (by the PR body's claim only; no Linear read needed).
4. **Delta discipline:** diff round 1 head -> round 2 head. List every changed file and hunk. Any change to a re-pinned cell's non-status line, to `lookupCalls` / `custodyInsertCount` / `anchorCalls` / writes-nothing assertions, or outside the files C names, is a blocker unless it is one of the stated fixes.
5. **Regressions of round 1's GO parts:** tenant re-read authority, PII (email only, encrypted path, nothing new logged or echoed), the failure arms (timeout 503, other 502, both before the transaction, no custody row, no owner flip), repeat transfer = no second user row.
6. **Red-first, mutants, landing:** the delta's red-first at the round-1 head (author: 3 red / 12 green, B2 green by design); the 7 author mutants (M1, M2, M3', M4, A1, B1m, N5m') each compiling and killing exactly its cell; merge-tree on LIVE develop; originate unit suite on the landing tree (author: 1481/1481); the new integration suite in both tenancy modes on your scratch PG (author 15/15) and the sibling (6/6); tsc including tests; the three-dot file list.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 217967041265... (tier 1 delta, round 2 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`, no push.
- No `cd`, no `rm`, no stderr to /dev/null, no Docker.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS.
