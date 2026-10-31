From Tuesday (the Datasec coordinator seat), Datasec / Security Composer. **Your STATUS file is the channel and the wrap** (no mail channel). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`.

# BRIEF B975 - SEAT-J34: SECURITY COMPOSER, PCOMP-40 (L3-2, ATTRIBUTE OVERRIDES STORAGE): **NOT LAUNCHABLE AS A BUILD. MEASURED: THE WORK IS ALREADY ON MAIN. THIS KIT IS A SHAPE-HOLDER; TUESDAY RE-POINTS OR DROPS IT AT THE STAMP.**

## STATUS-NOW (measured 2026-10-31 12:0x AEDT, read-only, drafter claude-sonnet-5-5)
- Composer main `d70edf70fc43bb69737b2a242ba56480ce79f0d8` (the B917 words change, 2026-10-29 19:13Z). `packages/db/migrations` holds **0025_attribute_overrides.sql** (table `attribute_override`, RLS forced, draft-only guard, CHECK value sets, grants) and `packages/db/rollback/0025_attribute_overrides.down.sql`; last migration on main is 0027.
- PR #87 (merged, merge sha `e019ac3abf628cbb6a50eb871b8f65b86a58ff6e`) "Structure: version numbers, engagement governance record, stored attribute overrides (migrations 0023-0025)". It covers L3-2, L3-3 and L3-5 (PCOMP-40, -41, -43). C-ruling record (CLARIFICATIONS ~1821-1836) names it merged, NOT deployed.
- `packages/api-contract/src/document.ts:114` now describes putControl as no longer refusing overrides; the only remaining hit of ATTRIBUTE_OVERRIDE_NOT_BUILT is that comment (count 1; control putControl 3).
- Jira PCOMP-40: Backlog, 0 comments, text still says "NOT started", files named `0022_*` (stale; 0022 is L3-1). PCOMP-41, -42, -43 also Backlog. PCOMP-44 (L3-6) is open but is NOT a clean structure lane (see PRIOR-WORK CHECK).

## REFUSE (this kit, at once)
1. If `/usr/bin/grep -c -i 'attribute_override'` over `git ls-tree` of main for `packages/db/migrations/0025_attribute_overrides.sql` is 1 (it is, control: 0026 name prints 1), then **there is nothing to build**: last line `STOPPED: NEEDS TUESDAY PCOMP-40 already built by 0025`.
2. Stamp slot unfilled (`/usr/bin/grep -c -E '_''_''_''_'` must print 0) or last line not `READ-WHOLE-BY-TUESDAY: DONE ...`: `STOPPED: NEEDS TUESDAY unstamped brief`.

## IF TUESDAY RE-POINTS IT (options, in order of value; none is a builder lane today)
A. **Records, not code:** a Composer records seat checks PCOMP-40/-41/-43 Done-when against 0023-0025 and the contract, then moves them on the rule "Done = merged to main, not deployed". No code branch.
B. **PCOMP-44 (L3-6, sm_policy_json / sm_policy_csv):** `OUTPUT_KINDS` (`document.ts:284`, 12 kinds, 0 sm_policy) is not alone: `apps/api/src/outputs.ts:33-37` makes the contract enum and the renderer `OutputKind` union equal in both directions (a compile error otherwise), so a contract-only add is NOT possible without a renderer-side change. That is a design call (words-free, but a stub renderer or a widened union), so it needs Tuesday's ruling first. No DB enum holds output kinds (migrations/rollback/src scan: 0 files name `change_report_pdf`). Migration 0028 would NOT be needed.
C. PCOMP-42 (L3-4): waits on K5 and L2 (held). Do not start.

## MODEL / GATE / PANE (for any re-pointed code lane)
model: claude-sonnet-5-5 (row C2; id `levels.sonnet.model_id`, models_latest.json) -- a migration or contract change is a tier-1 surface: **gate row G1** (Opus 5.5 first; routing table line 108), not G2. Seat J34 (J33 is the highest Composer seat, B917). Pane `Datasec/Security-Composer-J34`. Ports: none (node-only, `--network none`; 9710-9719 is NOT free: named by HPSM-POC kits). Kit dir `.tools/b975/`, worktrees `.tools/wt-b975-*`, containers `pc-b975-*`.

## HELD / SHARED (unchanged if re-pointed)
No UI words (any visible word = STOP). Held items untouched: PCOMP-19, -20, -91, -68..73, -76, -79, -84..90, -92, draft PR #85. One migration/contract lane at a time (project lock `.tools/composer-heavy.lock`). Open PRs #95, #85, #91, #86: 0 paths under `packages/db/` or `packages/api-contract/` each (measured). No live branch of mine to collide with: `b917/...` is the only `b9*` Composer ref of note.

## PRIOR-WORK CHECK
Done: migration 0025 + down, PR #87, document.ts comment. Not done: re-read `packages/db/test/*attribute*` and `apps/api/src/routes` putControl tests to confirm overrides round-trip (UNMEASURED by the drafter).

## STANDING LINES
Never `cd`; absolute single-quoted paths; python only `python3 -I -B`; /usr/bin/grep -i with positive control; no SOW, `Source_Documents/`, `inbound/`; no person's name or card id; ASCII only; no Jira/GitHub write; Tuesday opens the PR and commissions the gate; identity per REFUSE 7 of the B917 kit.

## Stamp
- STAMP (Tuesday, time and what was read): ____
- LAUNCH WINDOW: ____
- Stamped by (decisions accepted or struck): ____
- Launch authority: ____
- Items struck at the stamp: ____
- Hard stop and target READY: ____
- Main at launch: ____
- Model receipt line and load1 at launch: ____
Launch (only if re-pointed): `WED_USAGE_STOP=100 bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/Security-Composer-J34 "WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer' '<this file>'"`

READ-WHOLE-BY-TUESDAY: ____
