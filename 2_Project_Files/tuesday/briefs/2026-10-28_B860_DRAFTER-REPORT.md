STARTABLE: YES (pins hold: main df1dc0fe25e87dda4a9748c14870f942371a58a5, no b860 ref, 0 open PRs, ports 9880-9889 have 0 listeners; one fetch is owed by the seat if its clone lacks df1dc0fe)

# B860 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H50: HPSMPOC-361, chooser logo unit arm plus a permanent browser corner check)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B860_SEAT-H50_hpsmpoc-361-chooser-logo-tile-pins.md` (125 lines). Shape: the stamped chooser-logo kit (112 lines) for the web side and the stamped module-binding kit (136 lines) for current conventions (stamp block, launch line, STATUS-NOW, heartbeat, partition). Read-only: no write to any project, Jira, GitHub or git.

## BLUF
- Startable, one commit, test-only, paths: `web/src/components/shell/HpLogo.test.tsx`, a NEW `web/e2e/logon-chooser-corners.spec.ts`, and `web/playwright.config.ts` only under D-2. No product byte; touching `HpLogo.tsx`/`UatStartScreen.tsx` is a STOP.
- The hole is real by the gate's own measurement (relayed, not re-run by me): m7 (inline `style` background on the chooser wrapper) and m8 (`sm:`-prefixed tile classes) both left 3036 rows green; the browser render caught m7 (4 of 4 corners, 1024 and 576 white pixels). I read the cause in source: `PAINT` is anchored at the token start and the chooser arm's ancestor walk reads classes only, never `style`, and stops before `main`.
- One honest limit written into the kit: m8 cannot be seen by a browser check at 390 px (the `sm:` variant starts at 640 px), so the unit arm must carry m8; the plant table says so.
- Design constraint found: a new Playwright PROJECT would trip `scripts/e2e.mjs --check-shards` and `ci.yml`'s matrix (both outside the lane). A new spec in the existing `desktop`/`tablet` projects lands in the shard `journey-and-prototype` with no change there. Hence D-2 (third `webServer` entry, no new project).
- Load read 3.98 (shared machine); heavy runs need load1 below 7 under the seat-local lock.

## Facts re-measured (instrument, control)
- main: `gh api -X GET commits/main` = `df1dc0fe...`; `pulls?state=open` printed nothing; `git/matching-refs/heads/b860` printed 0 (control: a bad ref path returned the API's 404 body); `lsof -nP -iTCP:9880-9889 -sTCP:LISTEN | wc -l` = 0.
- Ticket HPSMPOC-361 read whole by the project's Jira helper (`python3 -I .tools/b649/jira.py`, GET only): Backlog, 0 comments, labels `b833-gate`, `b841-2026-10-27`, `test`; scope, fix shape and Done-when quoted verbatim in the kit.
- Files at main read through the API: `HpLogo.test.tsx` 433 lines (`PAINT` line 51, `expectLogoFirst` line 98, chooser caller `expectLogoFirst(..., false)`), `playwright.config.ts` 85 lines, `logon-logo-top.ts` 59 lines (exports `CHOOSER_MARK_WIDTH = 3000`), `logon-logo-top.spec.ts` (its header says the UAT start page has no e2e project), `UatStartScreen.tsx` lines 71-72 (wrapper `div`, `HpChooserMark`, `h-24 sm:h-32`), `scripts/e2e.mjs` (SHARDS, `shardProblems`), `package.json` scripts. `web/e2e/` lists 55 entries, none names the chooser (grep on the listing: lines for logon/chooser/start were only `logon-logo-top.*` and a playbook file).
- UAT mode env (relayed from the gate's and builder's STATUS; `config.ts` lines 79-92 seen in the API read): `HPSM_API_MODE=mock HPSM_UAT_OPEN_SIGNIN=on HPSM_ENVIRONMENT=uat` plus a random key of at least the minimum length; page colour `rgb(246, 247, 249)`.
- Model: `models_latest.json` `levels.sonnet.model_id` = `claude-sonnet-5-5`; rows C2 line 92, L6 line 85, G2 line 109 (`grep -n` on the row ids; C2 matched).
- Kit hygiene by program: stamp-slot lines (four-underscore pattern) = 8; at-sign tokens = 0; clock-time and name patterns = 0 hits.

## D-decisions (taken by the drafter; Tuesday accepts or changes at stamp)
- D-1 Unit arm first, browser spec second, one commit.
- D-2 Third `webServer` entry in `web/playwright.config.ts` (UAT env, per-run random key, own port setting `E2E_CHOOSER_PORT`, `reuseExistingServer: false`), spec points `baseURL` at it. Fallback: a spec that starts its own server. No new project.
- D-3 Page colour read from the page, not typed.
- D-4 Two widths only, as the ticket names (no tablet/360 cells).
- D-5 Sonnet builder (C2), tier-2 gate, no Opus.
- D-6 Four plants (m7, m8 from the gate; m9 an arbitrary-property class `[background:#fff]`; m10 inline style on `main`) so the fix is not tuned to two shapes; the unit arm walks up to and including `main` for paint tests only.
- D-7 Target READY 120 minutes after Step 0, hard stop 210 (browser build, plant table, repeats behind a heavy lock).

## Q-questions for Tuesday (each with a default)
- Q-1 Gate round. Default: NO GO 0 of 2 on a new class (permanent browser check plus weak-assertion pins); the ticket's own provenance reads round 1 of 2; tier 2.
- Q-2 Is a third `webServer` in the shared Playwright config acceptable, given every CI shard then starts it? Default: YES (D-2); if not, the spec-spawned server fallback.
- Q-3 Port block. Default: 9880-9889 as assigned (web, stub, hosted, chooser all set inside it).
- Q-4 Jira write by the seat. Default: NO.
- Q-5 Is m8's honest green at 390 acceptable for "red on a unit row or on the browser check"? Default: YES (the unit arm carries it; the Done-when says "or").
- Q-6 Launch order beside the two sibling lanes (infra test rule; wording lane touching `web/src/server/auth/config.ts`). Default: launch independently; no shared path; this lane only reads `config.ts`.

## UNMEASURED
Web suite count at main (3036 is the gate's), Chromium availability here, behaviour of the extra `webServer` entry in the playbook shards, pixel method choice (canvas vs zlib), exact minimum key length, whether the project's clone holds `df1dc0fe`.

## Outside-the-fences disclosure
- Read-only everywhere except the kit and this report. `gh api -X GET` only, under the project's `GH_CONFIG_DIR` (commits, contents, matching-refs, pulls); one Jira GET through the project's helper, saved to the session scratchpad; no credential printed. Local reads: the sweep, two kits, two drafter reports, the gate and builder STATUS files (grep and ranges). `lsof` and `uptime` read-only. No git command inside a project's `.git`, no `az`, no HTTP to a hosted host, no npm, build or browser.
- One bash call was refused by the no-cd hook and one by the zsh-word hook; both re-issued without the offending word.
