# Gate brief: GATE AW1 = PR #1635 (KS-1262: the per-user notification PUT refuses the reserved userId `platform-settings`), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat C 27th's READY FOR GATE (15:29Z). The author's CLAIM is beside this brief: `C27_READY_1529Z.txt` (read it WHOLE). The Spark pass it carries, byte-for-byte with no seat cells: `2_Project_Files/local-model/night/READY_KS-1262-NOTIFPLATFORMID-1_*`; the screen: `0_Brain/reference/2026-10-18_spark-screen/SCREEN_16.md`. Secuura only. Tier 1: it closes a path where a non-admin could overwrite the PLATFORM-WIDE notification record.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Make your clone INSIDE THIS SESSION'S SCRATCHPAD: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a3368218-953e-40df-ac8f-2e5abee5552f/scratchpad/gate_aw1/`. Use `git clone --shared` from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src`, then fetch `refs/pull/1635/head` with that clone's core.sshCommand, using LITERAL paths in every `git -C`. **EVERY npm / npx / vitest / tsc command runs INTO your clone (absolute `node <clone>/node_modules/.bin/<tool>` or `--prefix`). NEVER `npm exec` from your cwd: your cwd is Wednesday's tree.** Build `packages/shared` first.

**Heads (Wednesday's ls-remote via the cache clone, 02:3x AEDT 2026-10-20):** #1635 head `c2cfd51f3fb301642fbf1cd46ef2dfb644295b5d`; develop `09336b240721d8961d409dbd3c0de077d03ca959`. Re-read both at start and before the verdict. Author's predicted landing tree `22b9299dd24aa8ff8b1dd1c48a3acd6d9cfd1446`.

## Questions (each with its instrument; name what you did NOT run)
1. **Reach, the question that decides severity:** can any REAL principal carry `userId === 'platform-settings'`?
   - Read how auth mints userIds: UUIDs from the users table? Connector or service tokens with free-text subjects? `connector:...` ids? Test tokens?
   - Is the test-token path (`parseTestToken`) reachable in any non-test build? Read the env gates, and say what kintsugi/demo would need for it to be on. Read only; no server is touched.
2. **Completeness:** enumerate EVERY writer and reader of the `notif:<key>` namespace (setNotificationSettings, getNotificationSettings, and any raw Redis key use) across services/, with a positive control.
   - The author found two writers in api-gateway. Is any other path able to address the `platform-settings` key with a caller-chosen id (other routes, other services, case variants, whitespace, URL-encoding, `..`)?
   - The guard compares exactly: are `Platform-Settings`, ` platform-settings` or `platform-settings%00` distinct keys in Redis, or do they normalise onto it?
3. **The read side:** the per-user GET (`admin.ts:1478`) still returns the platform-wide record to a principal with that id. Is that an information leak to anyone real (see Q1)? Note it; it is not this PR's fix.
4. **Cells can fail:** run at least the guard-removed and role-conditional mutants yourself; confirm the 403 shape matches the house error shape and that nothing is written on refusal.
5. **Landing:** merge-tree on LIVE develop = the predicted tree; the full api-gateway suite at the landing by cell name; the test file type-checked; three-dot = the PR's 2 files.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head c2cfd51f3fb3... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings B1../N1.., what was tested and HOW, NOT RUN. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; nothing on any server; no `cd`; no `rm`; no stderr to /dev/null; no Docker; every zero with a positive control. Before you finish run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.
