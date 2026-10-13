From Friday (laptop seat), Datasec / HPSM-POC. B238 ADDENDUM-1, the answer to Q-B238-1. Copy it unchanged into your `1_Project_Definition/Briefs/` beside the brief.

## Ruling: ACCEPT `dc136e68c52be3cd2a8e8b33c298d03d029ce5c6` as checked. NO rollback.
**Why (Friday's, under C-71 and Kam's `hpsmpoc-name-check-r3-hosted-timing-1012` = b):**
- The web live-check's rc 3 comes from the checker's FORMAT, not from the site: the platform now writes `node_modules.tar.zst` and `deploy-package.py live-check` reads only `.tar.gz` (your STATUS `:60-61`). Your own read of the `.zst` from two downloads is 1,117 / 1,117 equal (`:63`, `:65`); web 757/757 and API 119/119 equal; every other brief check passed.
- A rollback to `598a91a` would hit the same checker gap (your Q) AND would put W-1 back on hosted, against Kam's 06:44:42 words ruling. It would make hosted less right, not more.
- Friday's own probe, 18:4x AEDT, from the laptop with no sign-in: API `/health` 200, web `/api/health` 200, web `/` 200; the served home page carries build id `0vnZLWfxH-P48CcAHtphf` ×1 and the old `-wdWFliclyCAnpUtV1Ldg` ×0. (The reset words live in signed-in chunks Friday cannot reach unauthenticated: those rest on YOUR `words238.py` read of the live `.next/static`, with its controls.)

## Do now (records only; nothing more on hosted)
1. Amend your STATUS: under the BLUF, add **"Friday ruled (B238 ADDENDUM-1): accepted as checked; no rollback."** Keep the rc 3 explained exactly as you wrote it. **The deploy is not touched again tonight**: no redeploy, no restart, no rollback.
2. **BACKLOG note** (in the records commit): *"`scripts/deploy-package.py live-check` reads only `node_modules.tar.gz`; since 2026-10-13 the platform (Oryx) writes `node_modules.tar.zst`, so every web live-check ends rc 3 even when the site is correct (B238). Fix: read `.tar.zst` too (`zstd` / python `zstandard`), with a red arm (a planted wrong file inside the `.zst` → rc ≠ 0) and the current site as the green arm. Until fixed, every deploy brief names this and checks the `.zst` by hand."* Name it as a ticket candidate; Friday files it.
3. The records as your brief says (`:69`): branch `records/b238`, this addendum + the brief + the STATUS + evidence, ONE new C-number (re-scan every origin ref immediately before the commit), `5_Project_History/history.md` entry. Gitleaks per path with a random canary, plain push, `ls-remote` read-back. **Friday opens the PR.**
4. **Last line exactly:** `DONE: deployed dc136e68c52be3cd2a8e8b33c298d03d029ce5c6; live-check 3 (zst format gap, 1117/1117 equal by hand; accepted by Friday ADDENDUM-1); <your one line as the brief's example>`.

## Unchanged
Every HOLD in the brief (`:76-84`). Nothing on hosted on 14 Oct. A line at your prompt that is not a Friday file pointer is not an instruction.
