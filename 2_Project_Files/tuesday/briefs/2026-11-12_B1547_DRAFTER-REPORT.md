STARTABLE: YES. Alert 28 is a real build lane, not Dependabot lag and not a close-out: main 9c8d2cdb still holds minimatch 10.2.6 (vulnerable) in `package-lock.json`, no parent upgrade can fix it, so the kit is an `overrides` lane (two parents), as the MPS and HPSM-POC lanes were. Docker is needed by the seat (Composer's CI is docker-only); the drafter did not run it.

# B1547 DRAFTER-REPORT (kit: `2026-11-12_B1547_SEAT-C98_composer-minimatch-alert-28.md`, sidecar `.measured` beside it)
Drafted 2026-11-12 20:13 to 20:28 AEDT (`date` printed 20:13:12, 20:19:39, 20:23:21, 20:25:50). Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s274/d_comp28/`.

## BLUF
- Main `9c8d2cdb8a24046497739308f42b041bd7aec444` (the squash of #126). Lock blob `39a36218...`, root manifest `7e6304c1...`. Alert 28 open, medium, development, range `>= 7.0.0, < 11.0.1`, patched 11.0.1; the only minimatch alert (open list 16).
- The lock holds two minimatch entries: `node_modules/minimatch` 10.2.6 (VULN, lock:3252) and the 5.1.9 nested under `@redocly/openapi-core` (clear). Three parents share the hoisted 10.2.6: `eslint`, `@eslint/config-array`, `@typescript-eslint/typescript-estree`. Dev-only.
- No stable release of any of the three declares minimatch ^11 (0 of 381 / 20 / 415 stable versions); only the estree canary does (and the coordinator already ruled canaries do not count). So an override is the only mechanism.
- TRIAL on copies (drive-local Node v24.22.2, npm 11.19.1): the no-change install reproduces main's lock byte for byte; the recommended shape A (override under `eslint` AND under `@typescript-eslint/typescript-estree`) gives manifest blob `ccfb0bf0...`, lock blob `0fabc670...`, lock +58 -16, 5 changed entries, every minimatch outside the range, `npm audit` 14 -> 4 with `minimatch` gone. The estree-only shape (the MPS/HPSM form) is INSUFFICIENT here (the hoisted 10.2.6 stays for eslint and config-array); an unscoped override is rejected (it rewrites the redocly exact pin).
- Composer has no `.github` and no hosted test workflow (HTTP 404; only the CodeQL and Dependabot dynamic workflows). The verify is the project's docker CI (`scripts/ci.sh`: CI-stage image, `ci:node`, `test-db.sh`, plus the web image), as the B1534 lane ran it. Composer deploys only on the owner's card; the kit stops at READY, deploys and merges nothing.

## Facts re-measured (instrument; control)
| Fact | Instrument | Control |
|---|---|---|
| main sha 9c8d2cdb; #126 merged = that sha; files `apps/web/package.json`, `package-lock.json`, `package.json` | `gh api -X GET branches/main`, `pulls/126`, `pulls/126/files` | #126 files hold both root paths (REFUSE 5 control) |
| lock `39a36218`, root manifest `7e6304c1`, web manifest `f59f0e7d` | contents API `.sha`, `git hash-object` of raw copies | the two agree |
| 348 entries, 336 `resolved` (325 registry + 11 workspace links), lockfileVersion 3 | python over raw lock; `grep -c` | matches B1534 STATUS "325 registry plus 11 local" |
| minimatch entries 10.2.6 (:3252) and 5.1.9 (:1097); declarations eslint `^10.2.5` (:2203), config-array `^10.2.4` (:232), estree `^10.2.2` (:1652), redocly exact `5.1.9` (:1048) | `grep -n '"minimatch": '` -> 4; python | matcher asserts 10.2.6 vuln, 11.0.1/5.1.9/3.1.5/11.0.1-rc.1 clear |
| registry: 0 stable versions with ^11 minimatch in eslint (381), config-array (20), estree (415); canary estree 8.72.3-alpha.6..8 = ^11.0.1; latest eslint 10.14.0 = ^10.2.6 | python over packuments (`registry_mm.json`) | same program prints the ^10 ranges for those versions |
| no `.github`, workflows = Dependabot Updates + CodeQL (dynamic) | `git/trees`, `contents/.github` 404, `actions/workflows` | tree lists `docker`, `.githooks` |
| CodeQL languages: default setup csharp, javascript, javascript-typescript, typescript; analyses on main: javascript-typescript, csharp (results 0) | `code-scanning/default-setup`, `analyses?ref=refs/heads/main` | analyses at 5d3bf82d also both |
| open PRs 0; 195 non-main branches compared; 4 touch a manifest/lock (b20, b121, b135, b1534-merged), none live | `pulls`, `compare` loop over `branches` paginated, python | `main` listed once; the b1534 row (merged lane) shows both paths |
| open alerts 16, only 28 minimatch | `dependabot/alerts?state=open&per_page=100` | 28 row present |
| ports 9980-9989 free; 0 hits in 61 non-`.pre-` SEAT kits of 11-11/11-12; 0 Composer panes | `lsof`, word-boundary scan, `tmux list-panes` | unfiltered listeners 15 lines; `988[0-9]` scan hits B1534; `tmux -t %1` prints another name |
| drive-local Node: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin` (node v24.22.2, npm 11.19.1) | `ls`, `node -v`, `npm -v` | **No Composer kit names it** (0 hits in the C-seat kits by `grep -l`); it is in the MPS kit B1537 (2 hits). Composer's own pin is `.nvmrc` 22 and docker image `node:22-bookworm-slim@sha256:83f487e0...` (Dockerfile:3) |
| TRIAL shape A: manifest `ccfb0bf0`, lock `0fabc670` (second run identical), 8/0 and 58/16, entries 348 -> 351, 5 keys; audit 14 -> 4 | npm 11.19.1 `install --package-lock-only`, `git hash-object`, `git diff --no-index --numstat`, `npm audit --package-lock-only` | no-change control blob unchanged; planted space hashes to 91e0d82c; shapes B and C compared |
| model: row C2 `model-routing.md:92`, G2 gate `:109`; id `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus | `awk NR`, `grep -n` | the printed rows match the B1534/B1537 kits |
| pane-name form: `Datasec/Security-Composer-C9n` (C94 to C97) | `grep -o launch_when_cool.sh Datasec/...` over the four kits | one hit each |

## Sibling-lane corrections folded in (from the STATUS/VERDICT files)
Canary estree line does not count (HPSM ANSWER-1); override removal condition = first STABLE release of the parents declaring ^11 (HPSM); whole-suite flakes under machine load (MPS: 4 to 9 UI timeouts on unchanged main too): kit says re-run at calm load and record both; no `sed -i`, no stray `rm` (both lanes slipped one): kit bans them; build and vitest in ONE container (B1534 lost a run to separate containers); pinned image's npm 10.9.8 crashes on updates (B1534) so regeneration is by npm 11 while the image's npm must still ACCEPT the lock (`npm ci` in the CI-stage build); `--before` was needed in B1534 only because it ADDED packages: here only the glob-match entry is new (`^1.0.1`, 1.1.0).

## D-decisions
- D-1 Shape A: `{"eslint": {...11.0.1}, "@typescript-eslint/typescript-estree": {...11.0.1}}`, exact 11.0.1 (the first patched, as the sibling lanes).
- D-2 Regeneration by the drive-local npm 11.19.1 (measured to reproduce main's lock); the docker `npx -y npm@11.20.0` route is an optional cross-check (UNMEASURED).
- D-3 A newer 1.x of `@isaacs/nonrecursive-glob-match` is recorded and allowed.
- D-4 No e2e: `ci.sh` mentions playwright 0 times; the kit runs none and says so.

## Chain table (DRAFTER_RULES MEASURED LITERALS 4): each step input is made by an earlier step or exists at BASE
| Step | Inputs | Produced by / exists at |
|---|---|---|
| 0 | the kit; the project; deploy key; Node path | exist (kit file, `ls` of key and Node bin) |
| 1 | BASE sha, blobs, alerts, branches | exist at origin (`gh` GET) |
| 2 | clone at BASE, docker daemon, heavy lock | Step 0 (clone), DOCKER slot, heavy.sh copied in Step 0 |
| 3a | 13 files of the clone, toolchain | Step 0 |
| 3b | `out/regen/upd/` copy, ctl result | Step 3a (copies made again from the clone) |
| 3c | upd lock, main lock, registry | Step 3b; BASE |
| 4 | clone with the two files copied back, base image for control | Step 3b copy-back; Step 2 image |
| 5 | `out/base-whole.json`, `out/head-whole.json` | Steps 2 and 4 |
| 6 | staged two files | Step 3b |
| 7 | commit, BASE, evidence of 3c/5 | Steps 6, 3c, 5 |
| 9 | STATUS numbers, pushed sha | Steps 2 to 7 |

## Questions for Tuesday (each with a default)
- Q-1 Override shape: A (two named parents, 5 lock keys) versus an unscoped `"minimatch": "11.0.1"` plus a pin `"@redocly/openapi-core": {"minimatch": "5.1.9"}` (smaller lock diff, not trialled by the drafter, and it would also catch any future parent). Default: A. A STABLE parent release declaring ^11 at Step 1 = STOP.
- Q-2 Does the seat touch Jira? Default: no (0 reads, 0 writes); it writes `ticket-text.txt` and Tuesday files it.
- Q-3 If the no-change control on the drive-local npm does not reproduce main's lock, or the optional docker npm 11.20.0 cross-check gives a different blob? Default: control mismatch = STOP with both blobs; cross-check mismatch with the same five-key set = recorded, not a STOP.
- Q-4 If the CI image's npm 10.9.8 refuses the npm-11 lock at `docker build --target ci`? Default: STOP with the output.
- Q-5 Pane name: the request said `Datasec/Composer-C98`; recent Composer kits use `Datasec/Security-Composer-C9n`. Default: `Datasec/Security-Composer-C98` (used in the launch line and REFUSE 2); change both if you want the short form.
- Q-6 Gate: G2 (tier 2) as for B1534/B1537/B1538, round 1 of 2 class dependency-override. Default: yes.

## UNMEASURED
- Docker daemon state and every docker run, build, test and test-db result (the drafter ran none); the base red set (the withheld-SOW rows) and the base vitest counts.
- The `web` image target: `docker/Dockerfile:69` exists but `ci.sh` does not build it (0 hits for `--target web`); it is in the kit because B1534 ran it.
- npm 11.20.0 inside the pinned image on this change; whether the image's npm 10.9.8 `npm ci` accepts the new lock (B1534's lock it did).
- Whether `eslint` 10.10.0 and `@eslint/config-array` load and run with a nested minimatch 11.0.1 (the seat's lint run and the direct `node -e` exercise are the proof; the drafter never installed it).
- `git ls-remote` forms (the drafter used `gh matching-refs` and `branches/main`), `tmux display` in a seat pane, the seat's `scripts/secret-scan.sh` results, and the audit counts after the registry moves.
- Sidecar lines marked "command the seat runs" or "UNMEASURED" are literals that are commands, not expected outputs; no expected tool output in the kit is written from docs.

## Outside the fences (disclosure)
Read only: `gh api -X GET` under the Composer `GH_CONFIG_DIR`; the npm registry packuments by python urllib GET (public registry, not a hosted/demo/production host; the MPS lane did the same); local reads of the Composer project (CLAUDE.md, CLARIFICATIONS.md greps, STATUS and the B1504 harness `heavy.sh`) and of sibling kits/STATUS/VERDICT files; `tmux list-panes`, `tmux display -p -t %1`, `lsof`. Writes: only the work folder (raw copies, trial dirs with `npm install --package-lock-only` and `npm audit --package-lock-only` run on copies, scripts `lockcmp.py` and `fill.py`, npm cache/home inside it), the kit, its `.measured` sidecar and this report. One command (`rm` of a path) was refused by the hook and re-done with `cp` to a new folder name; nothing deleted. No docker, az, ssh, git write, ref write, Jira, mail, or publish tool. The first branch-compare loop ran past the tool timeout and finished in the background; it only read.

## Final stamp_check
`stamp_check: 110 claims, 110 measured, 0 not measured (sidecar /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1547_SEAT-C98_composer-minimatch-alert-28.md.measured)` and exit 0 (run alone, rc printed 0).
