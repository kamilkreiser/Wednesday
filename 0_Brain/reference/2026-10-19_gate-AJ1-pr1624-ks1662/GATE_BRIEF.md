# Gate brief: GATE AJ1 = PR #1624 (KS-1662: tenant-predicate cells + comment corrections), Sonnet, tier 2, round 1 of 2

Commissioned by Wednesday after Seat C 26th's READY FOR GATE (10:32Z). The author's CLAIM is beside this brief: `C26_READY_1032Z.txt` (read it WHOLE). It is the follow-up to gate AH1's notes on #1620: read `../2026-10-19_gate-AH1-pr1620-r2-delta/verdict.md` notes 1-5 first. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/aj1/`. Build `packages/shared` first; Prisma via `npm run generate --workspace=services/originate`. Scratch PostgreSQL on a port in 55430-55439, TCP only, `docker/init/*` + every migration.

**Heads:** #1624 head `24ab138d6231551a17872794d33470556fbe4dde`; develop `a0da739b6954d42333640ea190d877f031803c7f` (Wednesday ls-remote 21:3x). Re-read both at start and before the verdict. Predicted landing tree `3fba9ec794b6102f9ef5a6e69015c6865a985663`.

## Questions (each with its instrument; name what you did NOT run)
1. **Comment-only claim:** classify every +/- line of `services/originate/src/routes/documents.ts` in the three-dot diff yourself. Any non-comment line is a blocker (tier 2 assumed no behaviour change).
2. **Are the corrected comments TRUE?** RLS as the enforcement: read the `users` policies (`cmd`, `roles`, `qual`) on your migrated scratch DB, and confirm `secuura_app` sees 0 cross-tenant rows with a positive control. Confirm originate connects as `secuura_app` in `docker-compose.yml` and `services.bicep` (read the lines). The ks564 correction: remove `certifications:write` from `hasUsersStubScope` (auth users.ts ~:257) and run ks564 + api-gateway ks843 F-2; ks564 should stay green and F-2 red. Say which you could run.
3. **The new no-RLS suite (ks1662) can fail:** plant both predicate drops (email path ~:1733, id path ~:1712), compiling; each reds its cell; ks1402 (secuura_app) stays green. The suite's SETUP self-check that the connection bypasses RLS: tamper it (connect as secuura_app) and confirm SETUP fails rather than the suite passing vacuously.
4. **(c) non-2xx fallback cell:** the `void raced` mutant at ~:1681 reds it; the cell actually enters the path (the row appears only after the first local read).
5. **(d) RACE** asserts one user row and no phantom-id row; plant a second user row and confirm it reds.
6. **Landing:** merge-tree on LIVE develop; originate unit suite on the landing tree (claim 1504); ks1662 4/4, ks1402-invited-stub-holder 16/16, sibling 6/6 in both tenancy modes; the three-dot list = the PR's 3 files; a check that type-checks the TEST files (tsc -p excludes `src/__tests__`).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 24ab138d6231... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`, no push. No `cd`, no `rm`, no stderr to /dev/null, no Docker. Every zero gets a positive control. zsh: no PIPESTATUS.
