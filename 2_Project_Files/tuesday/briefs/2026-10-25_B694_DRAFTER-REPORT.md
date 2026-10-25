STARTABLE: YES

# B694 DRAFTER-REPORT (SEAT-M27, MPS: MPSCALC-290 openapi sentence + MPSCALC-334 part B exact label)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B694_SEAT-M27_mps-290-openapi-sentence-334b-e2e-exact.md` (95 lines; 8 lines carry the four-underscore pattern: 7 slots plus the last line; control: the same grep prints 0 for the REFUSE line itself because the pattern is split).

## BLUF
Startable. Both fixes are still unlanded on origin main `a85f8bd5` (positive controls fired). The approved sentence was found in the record (C-67, CLARIFICATIONS.md line 1338 heading, text on line 1343) and compared by program. The snapshot does NOT need to be touched (D1). Part B has a known trap: the spec does not load under Playwright (gate finding), so the e2e proof is likely UNMEASURED; the kit says so and forbids fixing the load.

## Facts re-measured (instrument, control)
- main = `a85f8bd5f172af494f05d8ffc1e0ee64b26fcf68` (`ls-remote`). Open PRs: #115 (1 file StoreFirstUseAbsent.cs, head fdbe9b21) and #112 (4 files, head f2102e35), via `gh -X GET api pulls?state=open` and `pulls/<n>/files`; control: `docs/API.md` appears in #112. Neither touches `docs/api/openapi.json` or `web/e2e/bom.spec.ts`. `compare main...b630|b614|b69`: no hit on either path.
- PRIOR-WORK, MPSCALC-290: raw read of `docs/api/openapi.json` at main (python `str.count`): old sentence 1 (line 218), approved sentence 0, `MANUAL_ITEM_FORBIDDEN` 5 (matches the sweep), control string 0. 2164 lines, blob `1831d47a0b66ca593c10544b7cd4ef245ffe340d`. Replace on a scratch copy: parses as JSON, line count unchanged, approved text has no quote/backslash/non-ASCII.
- PRIOR-WORK, MPSCALC-334 B: raw read of `web/e2e/bom.spec.ts` (381 lines): line 180 is `await page.getByLabel('Quote type').selectOption('purchase');` with no `exact: true`; 11 other lines carry `exact: true` (positive control: 211, 212, 256 ... 379). 44 lines hold `getByLabel(` without it (python), so 43 besides 180.
- Approved wording: python found the kit's replacement sentence inside CLARIFICATIONS.md line 1343 (True) and no non-ASCII byte in it. C-number confirmed C-67 (sweep said C-67; also the ticket's 11:42 comment).
- Snapshot: `web/scripts/sync-contract.mjs` (38 lines) copies docs at a ref and rewrites SOURCE.txt and the schema.ts header, then runs `npx openapi-typescript`. The snapshot is byte-equal to docs now (`cmp` rc 0, same blob). `web/src/api/contract.test.ts` only checks snapshot sha against SOURCE.txt and the schema.ts header; `git grep` at `dd0ce36d` found no test comparing snapshot to docs; the dotnet tests link `docs/api/openapi.json` directly (csproj line 29). So a docs-only edit breaks nothing; sync would touch `SOURCE.txt` and `schema.ts` (web/src, not the seat's).
- CI predicates read from `ci.yml` (123 lines): web job lines 44-66 (npm ci, lint = `eslint .` which covers `e2e/`, vitest, build + check-bundle; exit 0 each); dotnet job exit 0. `e2e/` is in no tsconfig include, so `tsc -b` does not cover the spec.
- Model: row C2 at `fleet/specs/model-routing.md` line 92 (`/usr/bin/grep -n` of the row ids: C1 91, C2 92, C3 93, G1 108, G2 109, G-cap 111); id `claude-sonnet-5-5` at `models_latest.json` lines 23 and 38.
- Ports 9960-9969: `lsof` rc 1 (control: lsof lists the OS listener on 7000). Word-boundary scan over 142 non-`.pre-` SEAT kits of 10-24/25: 8 hits (B640, B645, B646, B647, B648, B650, B654, B655), all finished lanes (B645 = gate of landed #110; B654 = builder of open #112, no pane). Live panes: MPS-G125, HPSM-POC-G124, NexusAI-M11, Security-Composer-J16, MPS-M26, Security-Composer-G122, fleet-monitor, tuesday: none holds that block. No `MPS-M27` / `SEAT-M27` / `b694` in any kit. Branch `b694*` absent on origin (`ls-remote` rc 0, empty; control `matching-refs/heads/b6` lists ten refs). Heavy slots: none present; no `.tools/b694*`. Load1 at 21:24 was 13.83 (kit says the launch waits for below 7).
- Jira (in-process python, `project = MPSCALC AND ( key in (MPSCALC-290, MPSCALC-334) )`): both Backlog; 290 has 2 comments, the newer (11:42) records the approved sentence and "not built"; 334 has 1 comment: parts A and C met, part B not landed, and the spec list fails to load (css import chain).

## D-decisions (override at the stamp)
- D1 Snapshot, SOURCE.txt, schema.ts untouched (script does not require it; those two are web/src; contract test unaffected). Consequence: snapshot differs from docs by that one sentence until the next sync.
- D2/D3 Exactly 1 line changed per file (`numstat 1 1`), line 180 becomes `getByLabel('Quote type', { exact: true })`; the other 43 non-exact lines are not touched.
- D4 Two commits, Part A then Part B; `0 2` from base.
- D5 Branch `b694/mps-unchanged-save-sentence-and-bom-spec-exact-label`.
- D6 No Jira write.
- D7 (kit choice) The seat runs no dotnet; the dotnet job is judged by Tuesday on the PR. Web proof: `npm ci` in the seat worktree, eslint on the spec at base and head, the contract test, a differential `tsc` of the spec via a scratch tsconfig, and `playwright test --list` before and after (no host).
- D8 Words: the approved sentence contains the shipped prefix `B309 T-V0-3 (MPSCALC-209):`, which stays (the record says so). The kit allows that one key inside the file only and bans keys in commit messages.
- D9 Target READY 2 h, hard stop 3 h (smaller than B685).

## Q for Tuesday (each with a default)
- Q-1 Gate tier: default TIER 2 (Sonnet, G2). Caveat: the sentence is customer-visible API text, but it is word-approved verbatim and docs/spec-only.
- Q-2 Snapshot drift: default leave the snapshot unsynced (D1). Alternative: a later seat syncs after #112 and the 176 work land, so the sync is done once.
- Q-3 The record (CLARIFICATIONS.md line 1408 (b)) says the lane "making `bom.spec.ts` load under Playwright, then `exact: true`" is NOT ruled. The kit commissions the one-line `exact: true` only and forbids fixing the load. Default: proceed under the sweep's S-size classification; if you read line 1408 as blocking the one-line fix too, do not launch.
- Q-4 `npm ci` needs the npm registry (not an app host). Default: allowed in the seat worktree, seat-local cache. If you want no registry traffic, drop the web proofs and accept "UNMEASURED: lint not run".

## UNMEASURED
No npm, tsc, eslint, playwright, dotnet or edit was run in the project. Not measured: eslint/contract test green at base after a fresh `npm ci`; that the spec still fails to load at main; that `getByLabel('Quote type')` currently matches two elements (RELAYED from the ticket; names read in `web/src` at `dd0ce36d` via `git grep` on the stale-but-present object); dotnet job; CodeQL; load below 7.

## Outside-the-fences disclosure
Writes: only the two files named in the task, plus scratch files in the session scratchpad (`openapi.json`, `bom.spec.ts`, `snap.json`, `sync.mjs`, `ci.yml`, `tree.txt`, `kits.txt`, `jira_read.py`, `x.txt`). Reads outside the project: the template kit, the sweep, the B692 kit (greps only), B640/B645/B654/B655 kits (one `-o` grep each to see what they say of the port block), `model-routing.md`, `models_latest.json`, `usage_tuesday.json`, `brief_seat.sh` line 24. Project reads: CLARIFICATIONS.md, CLAUDE.md, `.env` (Jira variable NAMES printed redacted; values read in-process by `jira_read.py`, never printed), `ls` of `.tools` and `web/node_modules/.bin`. Git: `ls-remote` and `git grep`/`log -1` on the local checkout (read verbs). `gh -X GET` only under the project GH_CONFIG_DIR, including `compare`, `git/trees`, `contents` raw reads. `lsof`, `tmux list-panes`, `uptime` locally. One Jira GET host call (the Jira site, per the rules). No fetch, no ref write, no `cd`, no HTTP to a hosted app host. One tool call failed on a zsh `=` word and one on a stray `?` in a comment; neither ran anything.
