# B279 DRAFTER REPORT · HPSM-POC · QA gate, tier 2 through code (tests only), draft PR #161 `b276/l1-tests-291-227` @ b8362d7 (HPSMPOC-291, -227)
Drafter (Sonnet 5.5), 2026-10-19 12:4x AEDT. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-19_B279_SEAT-G7_hpsmpoc-gate-pr161-tier2.md` (61 lines, 8 distinct slots, 10 slot occurrences, `grep -o` count). **No `.pre-stamp` copy was written** (I was limited to two files): Tuesday runs `cp` of the brief to `<brief>.md.pre-stamp` BEFORE filling slots, or the REFUSE control has nothing to fire on.

## Read whole
B271 gate brief (189 lines, both pages) and ADDENDUM-1 (opus48 switch, STATUS per-model rule); B276 STATUS (163 lines, Part A, FOUND, NOT TESTED, FOR TUESDAY); B276 brief `:1-61` (Part A and slot lines) plus its `.pre-stamp` slot grep. Not read: the diff itself (the branch is not in any local store I may fetch into; no fetch is allowed to me), `ci.yml`, the live Jira tickets, comments 39677/39678. So r1 and r4 are written from B276's description of the diff, not from the diff: RELAYED, not MEASURED.

## Measured by me (read verbs only)
- `ls-remote` (project `2_Project_Files`, 12:46): main `befd45e77b391467a1313af8b7b5e0fc580f7b63`; branch `b8362d7e1ad1632c4a9c2409d62a117493c2bcda`. MEASURED.
- `gh api` GETs under the project's `GH_CONFIG_DIR` (`kamilDatasec`): `pulls/161` open, **draft true**, head `b8362d7`, base `befd45e`, 4 changed files, 2 commits; `compare/main...branch` ahead 2, behind 0, merge-base `befd45e`, the 4 file names. MEASURED. Matches Tuesday's relay.
- `models_latest.json` `levels.sonnet.model_id` = **`claude-sonnet-5-5`**; `levels.opus.model_id` = `claude-opus-5-5`. MEASURED.
- `brief_seat.sh:21-23` reads `levels.opus.model_id` and `exec claude --model "$MODEL"` (`:26`): the pane launches on OPUS. **Tuesday switches the pane with `/model` to `claude-sonnet-5-5` after launch (session only, as ADDENDUM-1 did for 4.8), or keeps Opus; the gate's STATUS must record which model ran.** The routing row (G2, Sonnet) is satisfied only after the switch.
- Ports: `lsof -nP -iTCP:7190-7199 -sTCP:LISTEN` rc 1 (12:46). B276 used 7180-7189 (`B276_STATUS.md:45`); B271 7170-7179. No B27x brief names a port in 7190-7199 (the word-grep hits for `719x` were the range text `7170-7199` in B273 files). MEASURED.
- Load 12:46: `5.22 4.14 4.57` (so the gate will often wait under the < 6 rule). `date` AEDT.
- `B279` free: 0 hits in Tuesday's `briefs/` and in HPSM-POC `Briefs/` (`ls | grep -c`). B277 and B278 exist (composer work), so 279 is the next free number. MEASURED.
- `/opt/homebrew/bin/gitleaks` present; `.tools/b198/lock.sh` present (mode 755, the lock B276 copied). MEASURED.
- `4_Credentials/.env` was NOT read; the AGENTMAIL claim in the brief is B276's (RELAYED), the gate re-counts.

## Slots (values for Tuesday; the brief keeps the tokens)
| Slot | Recommended value | Basis |
|---|---|---|
| MODEL | `claude-sonnet-5-5` (and say in the line that `brief_seat.sh` launches Opus; `/model` switch after launch) | MEASURED |
| STAMP_TIME | Tuesday's clock at stamping, `date` AEDT | Tuesday |
| PANE | `Datasec/HPSM-POC-G7` | Tuesday's assignment; cockpit name list NOT checked by me for a live `-G7` (the brief_seat list shown in B271 had G6) |
| PANE_SUFFIX | `G7` | same |
| PORT_BLOCK | `7190-7199 (lsof: 0 listeners at 12:46)`; suggested use: 7190 API showcase-on, 7191 web live, 7192 API showcase-off, 7193 web second, 7194-7199 spare | MEASURED |
| CODE_MAIN_SHA | `befd45e77b391467a1313af8b7b5e0fc580f7b63` | MEASURED |
| HEAD_SHA | `b8362d7e1ad1632c4a9c2409d62a117493c2bcda` | MEASURED |
| B_NUMBER_CONFIRM | `B279 confirmed free: 0 hits in Tuesday briefs/ and HPSM-POC Briefs/ at 12:4x` | MEASURED |
Re-run `ls-remote` and `gh api pulls/161` immediately before stamping; the head or main may move.

## Design choices (and why)
- Copied B271's skeleton: REFUSE check with split-quote slot grep and `.pre-stamp` control, Step 0 copy, findings-only charter, LOAD rule, PINS, CLAIMS-as-attack, HOLDS, verdict as first and last lines, release-before-end list. Dropped the Docker, SQL Server and Azurite machinery (tier 2, SQLite only) and listed them as NOT TESTED by design.
- Verdict line follows Tuesday's requested shape (`GATE VERDICT B279: <...> @ b8362d7 (...)`) as the STATUS first line, with B271's `VERDICT:` last-line style kept per ticket.
- r2 uses "revert the helper hunk inside the head file" for the red-proof, because `PackageVersionOf` lives in `PkcsInPackageTests.cs` (B276 `:50`); B271's "tip test onto base" pattern cannot work for a single-file helper+test change.
- r3 forbids `scripts/showcase.sh` (builder FOUND 10: it reads `4_Credentials/.env`) and the builder's `.tools/b276/live/*` kit; the gate writes its own dummy-env start script from B276 STATUS `:58`. It includes the by-name control (showcase-off API green, `E2E_LIVE_API` unset skipped) and the base control for `override:109` (builder FOUND 5).
- r5 control: CodeQL analyses on a merged PR/main must be non-empty, so "0 analyses" on #161 reads as "not scanned yet", never "clean".

## Doubts
1. **I did not read the diff** (no fetch available to me), so traps T-a to T-c are inferred from the builder's STATUS; if the real helper change differs (e.g. threshold other than `Build >= 10,000`), the named mutants need adjusting. The gate reads the diff first (r1) and may amend the mutant boundaries; say so in STATUS.
2. **Pane model**: if Tuesday keeps Opus, the G2 Sonnet row is not met; the STATUS must say so. If Sonnet is flagged by the classifier on r3/r4 (crafted-input style), the B271 ADDENDUM-1 route (Opus 4.8 per session) applies.
3. **Builder's mutants are not in a readable evidence directory** I could name (B276 STATUS gives sha256 and results, not file paths), so the brief asks for the gate's own re-creation, not a byte copy of the builder's texts. Weaker lineage control, but the gate's own two are independent by design.
4. **r3 is heavy and load was 5.22**: the live set (build + Playwright, two API modes) may exceed one window; r3(a)/(b) are ranked first in the priority line, r5/r6 are cheap and can run while waiting.
5. **PR #161 is draft**: CodeQL / required checks may not have run on a draft; r5 treats absence as "not scanned", and the verdict is conditional on Tuesday's CI. Tuesday may prefer to mark it ready before the gate.
6. **B276 FOUND 5 (`override:109`)**: if the base control shows it fails the same at `befd45e`, it is a ticket candidate for Tuesday, not part of either token; the brief says so.
7. Jira text for -291 is the records drafter's, -227 has no Done-when: both quoted RELAYED; the gate reads the live tickets and the live text wins.
