STARTABLE: YES

# B1100 DRAFTER REPORT (SEAT-A1, NexusAI sqlite3 successor assessment)
Drafted 2026-11-02 06:10-06:16 AEDT (`date` 06:15:32 at the last check). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1100_SEAT-A1_nexusai-sqlite3-successor-assessment.md`.

## BLUF
One Sonnet measurement seat (pane `Datasec/NexusAI-A1`, ports 9990-9998, model row C2), 240 min target and 480 min hard stop, pushes nothing, writes a FOUND / TESTED / HOW report plus a recommendation to `1_Project_Definition/Briefs/2026-11-02_B1100_SQLITE3-SUCCESSOR-ASSESSMENT.md` (outside the product repo). Authority is the card ruled `b` "Assess now" at 2026-11-02T06:09:12+11:00 (read with `decision_queue.sh show` into scratch). The answer to "what does NexusAI use of sqlite3" is already small: ONE module, `backend/simpleDb.js`, callback API plus `this.lastID`/`this.changes`; the migration cost to a synchronous driver is the thing the seat must measure.

## Facts re-measured with instruments
- Main = `746dec442d2aac2237528a8b5f170c027e1c0321` (`gh api -X GET commits/main` and `git ls-remote` agree; control: two instruments). It is a records merge (#153) two commits after `a91753cd` (`compare`: 1 file, `HISTORY.md`). Open PRs 0.
- `backend/simpleDb.js` blob `0d07e81a...`, 876 lines; `:1` requires sqlite3, `:29` opens the DB (`grep -n`/`awk NR==n` over the tarball; `awk` control printed both lines). Census under `backend/`: only that file names sqlite3 (control: count flag printed `simpleDb.js:4`). 36 `this.db.(run|get|all|exec|prepare|serialize|close)(` lines.
- Lockfile (`python3 -I` over the tarball): sqlite3 6.0.1 `hasInstallScript` true, BSD-3-Clause, node `>=20.17.0`, deps bindings/node-addon-api/prebuild-install/tar; control: the same script printed None for the four deps.
- CI node `'24'` (`build.yml:29`, `npm-audit.yml:29`, `deploy.yml:31`), image `Dockerfile:2` node:24-alpine, `docker/Dockerfile.backend:2` node:18-alpine. Local `node -v` v26.8.1, npm 11.19.0.
- RD-919 and RD-918 read by the project's Jira helper in-process (heartbeat path redirected to scratch so nothing was written in the project; read-only), text quoted as RELAYED.
- Pane scan: no NexusAI pane live. Ports: `lsof -nP -iTCP:9990-9998 -sTCP:LISTEN` empty; a word-boundary scan of the 98 non-`.pre-` SEAT kits of 2026-11-01/02 for 9990-9998 hit nothing. Lock tool sha256 `cf01bafb...971f` read equal to B904's pin (drafter ran `shasum -a 256`). Briefs folder is not in a git repo (`rev-parse` fatal), so no landing is needed.
- Model ids from `models_latest.json` lines 22-23 (sonnet-5-5) and 17 (opus-5-5); routing rows C2 `:92`, C4 `:94`, C8 `:98` (printed by `grep -n`).
- Stamp-slot pattern count of the unstamped kit: 9 (8 slots plus the last line); no person name, no card id, no `@X@` pattern (grep counts 0).

## D-decisions
- D1: model row C2 Sonnet, not C8 (C8 is the drafter's own row); no table row names Opus for an assessment seat.
- D2: no PR, branch or push at all; the report stays in `Briefs/`; PR disposition has the single value `NONE`.
- D3: docker is allowed only for local unpushed scratch builds of a candidate's `package.json` on node:24-alpine, under the docker lock; otherwise NOT TESTED.
- D4: network is limited to the npm registry, GitHub (GET and the release assets a package names) and the official Node distribution; a purchase, account or login stops the seat.
- D5: launch line follows DRAFTER_RULES (`cockpit.sh add`); `BRIEF_SEAT_LEVEL=sonnet` is required inside the quotes.
- D6: the kit says cite the product owner's 2026-11-02 ruling and carries no card id.

## Q-questions for Tuesday
- Q1: Node 24 may not be installed on this machine (only v26.8.1 confirmed). Allow installing a Node 24 line through the version manager already here? Default: YES from the official distribution only, else NOT TESTED with reduced weight stated.
- Q2: Docker build of the candidates' scratch Dockerfile (D3) is allowed. Default: allowed, local only; strike if you want the image rows left as NOT TESTED.
- Q3: Recent NexusAI kits launch through `launch_when_cool.sh`; DRAFTER_RULES says `cockpit.sh add`. The kit uses the rules line. Default: swap to `launch_when_cool.sh` at stamp if that is the current practice.
- Q4: The seat's output could also feed a Jira comment on RD-919 later. Default: no, a records seat does that after you read the report.

## UNMEASURED
Every upstream fact (no registry or repository read was made by the drafter), every candidate, Node 24 availability, docker availability, whether any dynamic `require` of sqlite3 exists, and the Marketplace build script and gate contents (only a grep of the template files was done).

## Outside-the-fences disclosure
- Read the card via `decision_queue.sh show <exact id>` only (no `list`); the output went to a scratch file in the session scratchpad.
- Read the Jira helper `session-tools/b1056/b1056lib.py` header and loaded it in-process from a scratchpad script with `python3 -I -B` and its `HB` reassigned to scratch; performed Jira GETs for RD-919 and RD-918 only. No write anywhere in the project.
- Downloaded the main tarball with `gh api -X GET .../tarball/<sha>` into the scratchpad and extracted it there (untrusted data, read-only use). Fence breach to disclose: I typed `cd` once, as `(cd "$T" 2>/dev/null)` in a subshell inside one Bash call (the hook did not refuse it); nothing depended on it and no directory change persisted. I also used three throwaway shell variable assignments named `cd_unused`, `cd_none`, `cd2` (no effect). I read the B1088 and B904 kits, the B1069 pointer rows therein, and `model-routing.md`, `CLARIFICATIONS.md` lines 1354, 1362, 2062 and the project folder listing. I did not read `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, or any WEDNESDAY/FRIDAY or non-Datasec tree. `tmux list-panes` and `lsof` were read-only.
