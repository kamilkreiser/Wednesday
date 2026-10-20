# B390 drafter report (Sonnet 5.5), 2026-10-21 09:19-09:22 AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B390_SEAT-D18_hpsmpoc-vite-advisory-lockfile.md` (72 long lines, two stamp slots `@STAMP_HEADS@` / `@STAMP_AUTHORITY@` counted 1 each by `grep -o`, last line `READ-WHOLE-BY-TUESDAY: PENDING`). Pane `Datasec/HPSM-POC-D18`, C2 (`model-routing.md:92` quoted), gate tier 2 proposed.

## Findings that change the picture (read these first)
1. **The failing CI step is `node scripts/audit-dev.mjs`, not the production audit.** Step numbering: 1 set up job, 2 checkout, 3 setup-node, 4 `npm ci`, 5 `npm audit --omit=dev --audit-level=high`, 6 `node scripts/audit-dev.mjs` (all deps). Vite is dev-only, so step 5 passes. The brief makes the seat run both.
2. **`vite` is a PEER-installed package in the lock** (`"dev": true, "peer": true`, version 8.3.0, `:8401`) and `web/package.json` has no vite entry. It is pulled only through peer ranges (vitest `^6.4.0 || ^7.0.0 || ^8.0.0`, `@vitest/mocker` same, `@vitejs/plugin-react` `^8.0.0`), all of which admit 8.3.3. **Risk: `npm update vite` may not move a peer-only package** (UNMEASURED). The brief says that outcome is `STOPPED: NEEDS TUESDAY`, because adding vite to `package.json` or an `overrides` entry is forbidden by your instruction.
3. **`launch-editor` is not in the lock at all** (0 keys, nothing depends on it). Nothing to update for it.
4. **Time-dependent red:** advisory published 19:48Z but your own data shows web build success at 20:24Z and 21:15Z; the audit DB lagged. The brief makes the seat re-run the baseline and STOP if it is not red.
5. **Possible date inconsistency, flagged to the seat as FOR TUESDAY (c):** `ci.yml` comment says the braces exception lapses 2026-10-31; `web/scripts/audit-dev.mjs:14` has `lastDay: "2026-11-30"`. Nothing changed.

## Measurements (command, time)
All with `GH_CONFIG_DIR='/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config'` (`gh auth status`: kamilDatasec, 09:19).
- main: `git --no-optional-locks -C '.../HPSM-POC/2_Project_Files' ls-remote origin refs/heads/main` = `54fbceac12393f503fae8c5810af9609bac44548` (09:19:11).
- `ls-remote origin 'refs/heads/b390*'` = 0 lines; control `'refs/heads/b380*'` = 1 line (`b5ea627e7cd30511c48917f6e567a5c4eba64a48`) (09:19:11).
- Open PRs (`gh pr list -R datasecau/HPSM-POC --state open`): #170 b380 @ `b5ea627e...`, #169 b381 @ `bcff3e46992738aba35f2832d195b12c436f18cb`, #168 b382 @ `0f46875c0e704884db2c8be6f64c8adbd8f8333d` (09:19). `pulls/169/files` and `pulls/168/files` grep for `package(-lock)?.json` = 0 each (09:19:38).
- Lock at main: `gh api 'repos/datasecau/HPSM-POC/contents/web/package-lock.json?ref=main' --jq .content | base64 -d` = 313,562 bytes, lockfileVersion 3 (09:19). Parsed with `python3 -I`: `node_modules/vite` 8.3.0 `:8401`, dev, peer; `node_modules/vitest` 5.0.1 `:8779` (peerDeps `vite ^6.4.0 || ^7.0.0 || ^8.0.0`); no key containing `launch-editor`; vite deps `lightningcss ^1.33.0, picomatch ^4.0.7, postcss ^8.5.28, rolldown ~1.2.6, tinyglobby ^0.2.17` (09:19:27). 8.3.3 satisfies the ranges by reading them; no semver tool was run.
- `web/package.json` at main: scripts `test` = `vitest run`, `typecheck` = `next typegen && tsc --noEmit`, `lint` = `eslint --max-warnings=0`; no `vite` key, no `overrides` line (grep). `web/.nvmrc` = 24.
- CI: `gh api contents/.github/workflows/ci.yml?ref=main` lines 356-380 read (09:19:53); `web/scripts/audit-dev.mjs` (73 lines) read; it spawns `npm audit --json` and fails on high/critical except braces GHSA-vfj7-8cjw-p6xm.
- PR #170 lock patch (`gh api pulls/170/files`, 45 lines, +16 -6): hunks at `@@ -12`, `@@ -5989`, `@@ -8296` (root `undici` 7.29.1 dependency; nested jsdom undici 8.11.0; top-level undici -> 7.29.1). Vite entry at `:8401` is about 94 lines past the last hunk's end (`:8307`). **Prediction: clean textual merge** unless vite 8.3.3 changes lines inside those hunks. Not run.
- `.tools`: `b390` and `wt-b390-*` absent; `b389` and `node24/bin`, `b198/lock.sh`, `b267/{webrun,webfull,waitload,lock}.sh`, `b300/jira.py` present (09:20). Panes live (`tmux list-panes`): tuesday, MPS-G32, HPSM-POC-G18, D17, D15, G17, fleet-monitor. Load `3.60 6.62 8.78` (09:20). `lsof -nP -iTCP:7490-7499 -sTCP:LISTEN` printed nothing (no control run).
- `.env` key names (counts only): `^JIRA_` = 3, `^AGENTMAIL_API_KEY` = 0.
- B380 STATUS FOR TUESDAY item 6 read: nested undici 8.11.0 -> 8.12.3 re-resolve and six optional wasm entries; the brief relays it with a "revert or STOP" rule.

## Not measured
No npm/node/vitest/audit run; no Jira call (so the board search, ticket existence and counts are the seat's job); no registry call (8.3.3 existence and integrity, and vite 8.3.3's own dependency ranges, UNMEASURED); the CI log text; whether the merge with #170 is clean; no semver evaluation by tool.

## Questions for Tuesday (recommended answer)
1. If `npm update vite` does not move the peer-only entry, should the seat have a sanctioned fallback (e.g. `npm install --package-lock-only` with a one-off `npm update` flag)? **Recommend NO fallback: STOP.** Any route that adds vite to `package.json` or `overrides` is a package.json change your instruction forbids; a Tuesday/Kam call is cleaner, and the likely call is a `devDependencies` pin `vite ^8.3.3` (which would collide with #170's package.json edit region only if adjacent).
2. Jira priority for the one create? Brief says **Highest** (blocks every web PR before the freeze), copying B385's reasoning. **Recommend Highest.**
3. Gate tier: **recommend tier 2** (lockfile only), but Step 4 requires the whole web suite unchanged, which is the real instrument.
4. Order versus #170: **recommend landing B390 first**, then Tuesday forward-merges main into B380's branch (predicted clean). The seat reports the prediction and does not touch #170.
5. Should the fix be rebased onto a newer main when #168/#169 land before D18 finishes? **Recommend yes only if the new main touches `web/package-lock.json`; otherwise the seat STOPs on a moved main as written** (the brief lets `api/`-only movement through). Tell the seat otherwise if you want a looser rule.

## Notes
- The brief's launch line is B381's with pane, level path changed (`BRIEF_SEAT_LEVEL=sonnet` is already in B381's line) and the brief file name.
- The `@[A-Z_]+@` REFUSE grep does not match itself (the `[` after the first `@`); control relies on Tuesday's `.pre-stamp` copy reading 2.
