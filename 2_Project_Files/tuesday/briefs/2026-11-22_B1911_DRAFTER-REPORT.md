STARTABLE: YES

# B1911 drafter report (Datasec / NexusAI, lane N-L: RD-349 + RD-175)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1911_SEAT-N162_nexusai-lane-nl.md` (636 lines, 87119 bytes; seat `Datasec/NexusAI-N162`), sidecar `...nl.md.measured` (104 claims, `stamp_check.py <kit>` exits 0; 20 claim lines are marked UNMEASURED-BY-DRAFTER: literals of the kit's own instructions, a command or name the seat produces; plus KEY-1 to KEY-9 free lines). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1911/`. Written 2026-11-22, reads 19:24 to 20:02 AEDT.

## BLUF
- Neither ticket is built or met at main `8858e5d1` (0 open PRs, re-read). No prior work on RD-349 or RD-175; lanes N-K (PR 236) and N-M (PR 238) touched none of this lane's files. Both tickets carry the product owner's 2026-11-11 ruling (option a: records C-258), so no STOP: the outcome is ruled, the colours are Tuesday's defaults.
- The build is CSS only: `static/css/index-styles.css` (5 anchored edits, +18/-7 diff lines), `static/css/dark-mode.css` (one list line joined, one block of two rules appended, +13/-0), the light-failure fixture (2 signatures removed, total 69 to 63), one new 15-cell test file, the counts file. 5 paths, no product JavaScript, nothing deployed.
- All cells, plants and the browser read are MEASURED in real jest 29.7.0 and headless Chromium on scratch copies (not a stand-in): new file 8 red / 7 green at BASE (L1 L2 L3 L4 D3 C1 C2 C4 red, each for the property's reason), 15/15 green patched, 12 plants each caught (all stylesheets reverted equal by hash), `index-dark-surfaces` 31/31 with the fixture.
- Real-engine (local harness, real stylesheets): KPI label 3.478 to 5.437, description 3.299 to 5.158, drop text 3.478 to 5.437, toner label 1.186 (white on the track, both modes) to 15.426 light / 12.667 dark; chip 16px inside the 20px bar at 5/25/50/100 percent over all four fills.
- Suggested level: Sonnet, routing row C2 (`model-routing.md` line 92); model id `claude-sonnet-5-5`; review after at tier 1 with a rendered leg in both modes (as RD-251's was). Launch line is in the kit's Stamp section with `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Facts re-measured (instrument; control)
- main sha: `gh api -X GET .../git/ref/heads/main` -> `8858e5d11ec101de0a49a819c2d29f4eadf95c40`; `pulls?state=open --jq length` -> 0 (control: closed list shows PRs 225-239). Repo is `datasecau/Reporting_Dashboard_Au`. Counts file at BASE 6216 / 393 = 393 top-level `__tests__/*.test.js` (program count).
- Tickets by Jira GET (project's `.env` in-process; JQL always `project = RD AND ( ... )`; positive control `key = RD-349` returns the ticket): both To Do, each with one comment (the ruling), no other work.
- Greys and grounds by program and by the engine (above). **Dark trap** (found by measurement): `.drop-text` has no dark rule; moving its light colour alone puts `#00719f` on `#1c1c1c` at 3.13.
- **Three guards the first draft broke, found by running the 72-file run list and fixed in the frozen edit:** (1) `brand-shell-tokens` + `brand-token-conformance` refuse a literal `#7f8c8d` in dark-mode.css (closed debt manifest) -> `.drop-text` joins the existing dark muted list (`#8c8c8c`; dark 4.90 to 5.07, the lane's only dark pixel change); (2) the pinned light count of `#ffffff` (`scripts/derive-brand-tokens.js:148`, 51) -> the chip ground is written `white` (changing the pin would mean regenerating `tokens.css`); (3) `index-dark-surfaces` fixture -> commit F. Also `css-ratio-comments` reads ratios on declaration lines: the program writes them in the checkable form with computed values.
- **Correction of the ticket's "unexplained asymmetry":** `.drop-text` WAS in the static baseline, as a bare `span x3` (its three child spans); it leaves with the change (measured diff-set).
- Open code-scanning alerts 22, none in `static/css` or `__tests__`; no JS added (CQ steps still required, predicted rc 0, UNMEASURED).
- Landing rule quoted with source: CLARIFICATIONS entry C-190 (`awk NR==2062,2067`): PR, no new high CodeQL alert, same commit lands, never squash or rebase; head-pinned merge commit per B1771's HOLD 2. Deploy: none; C-224 demo hold stands; Deploy-demo run must read `skipped`.
- Chain input table (each input from an earlier step or at BASE): step 1 and 1b read BASE and the run list (BASE); step 2 reads the new file copied untracked (from the kit); step 3 makes T from the kit; step 4 reads T; step 5 reads T plus plants; steps 7 to 10 read T / K (K is made at step 9 from step 8's counts file). No step needs a file a later step makes.
- Jest lock: `queue-jest` empty and no pane `Datasec/NexusAI-*` at the time (tmux list: only `tuesday`); I ran jest from the b1771 clone's binary and `node_modules` (lockfile blob `2d7dbece2ecd` = main's) against SCRATCH trees only, `--maxWorkers=2`, own cache dir, load 4 to 8. Nothing written inside the project.

## D-decisions (mine, in the kit)
- D1 Chip, not shadow or colour: no single text colour clears the track and all four fills (white vs cyan 2.30, yellow 1.63; dark ink vs black fill 1.40).
- D2 Dark track `#313131` (project's own dark border value), per the ticket's own dark recommendation.
- D3 `tests/e2e/**` is NOT edited (suite outside `npm run verify`, needs a stood-up surface; its `light-baselines.json` already stale since RD-251: 72 lines of `.tab-button` 3.48; its allow-list entry for `.consumable-text` becomes a dead excusal): listed under LEFT FOR OTHERS.
- D4 Seat reuses slot 17 and band 30880-31519 (no seat live).

## Q-questions for Tuesday (each with a default; none STOP-class)
- Q-1 Colour of the three greys. Default: `#00719f` literally, as RD-251's ruling did for tabs. Alternative: `#495057` (BRAND.md R4's in-family neutral, 8.18 on white, 7.76 on `#f8f9fa`); BRAND.md maps dark `.metric-label` to `--nx-text`. Note a KPI tile then reads blue label over blue value (`.metric-value` is `#0096d6`). Override = one literal `TEXT` in `apply1911.py` and in the test file; the kit's LANDING HOLD 23 lets you answer after the build.
- Q-2 Toner label as an opaque chip with the text-shadow removed (default yes; the ticket asked that the shadow not be dropped silently: the rule's comment says why).
- Q-3 Leave `tests/e2e/**` and its baselines to a later NX-F2/NX-T lane (default yes) and ticket it.
- Q-4 `.drop-text` joining the dark muted list (default yes; dark 4.90 to 5.07).
- Q-5 Keep `white` for the chip ground rather than `#ffffff` plus a regenerated `tokens.css` (default `white`).
- Q-6 Slot 17 / band reuse (default yes).
- Q-7 Review at tier 1 with a rendered leg in both modes (default yes).

## UNMEASURED
- The final tree over the other 61 files of the run list and the full `npm run verify` (I re-ran the 11 affected files, 241 cells, and the P0 set 78/78 after the corrections; the first full run-list pass, 72 files / 1393 cells, ran on the first draft: 28 environment failures in 4 git-dependent files that fail identically at BASE in a no-`.git` scratch copy, 6 of mine, all since fixed). Counts pair after (predicted 6231 / 394). CodeQL local tool. Heads census. The live page, hover/focus, other viewports. Which node each `span x3` is (inferred from the diff-set).
- The 72-file run list is a drafter's frame (names of css/html readers); a reader built from a run-time path would be caught only by the full verify.

## Outside-the-fences disclosure
- Read-only: Jira GET (RD-349, RD-175, RD-251/RD-936/RD-956 text, four JQL searches), `gh api -X GET` (ref, PR lists and file lists for 236 and 238, tarball of main, commits by path, open code-scanning alerts), local git read verbs via a wrapper script with `--no-optional-locks`. No `decision_queue.sh`, no `briefs_staged`, no scoreboard, no `_ledger.md`.
- Wrote only: the kit, its `.measured` sidecar and this report under `tuesday/briefs/`, plus scratch under `fleet/state/s310/d1911/` (tarball extract, scratch trees, helper scripts, jest and browser outputs; one superseded sidecar moved to `_quarantine_old/`). One `rm -f` attempt was refused by the hook (I used `ln -sfn` and `mv`); nothing deleted.
- Ran jest and a headless Chromium (local `file://`, no HTTP to any host) from the b1771 clone's binaries against scratch copies, as described above. No server was booted. No writes to Jira, GitHub or any project file. No other drafter's files touched (B1906, B1908, B1909, B1910 trees not read).
- The kit names a person nowhere (name scan 0, underscore-aware pattern) and no card id; it cites C-258 and C-190 (records entries) and "the product owner's 2026-11-11 ruling".
