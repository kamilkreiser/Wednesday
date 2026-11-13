STARTABLE: YES

# B1551 drafter report (SEAT-C99, Datasec / Security Composer, Dependabot alerts 13 to 27)
Drafted 2026-11-13 13:00 to 13:12 AEDT (`date` 13:00:52 first, 13:10:45 last). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-13_B1551_SEAT-C99_composer-dependabot-alerts.md` (+ `.measured`). Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s274/d_comp15/`.

## BLUF
**All 15 open alerts clear with a lockfile-only update. No manifest change, no override, no major crossing, so nothing is out of the kit and nothing goes to the product owner for a major.** Main is `c2b231fa` (the landed minimatch lane). Every package's declared parent range already admits its patched version, so `npm update undici fast-uri fastify ip-address --package-lock-only` (drive-local npm 11.19.1, Node 24.22.2) is enough. Trial on copies: no-change control reproduces main's lock blob `0fabc670...`; the update gives lock blob `4364f1649bb96fafacec020a0e65d809b7090139`, 25 added / 25 removed lines, 351 -> 351 entries, 8 changed keys, all 12 `package.json` byte-identical; adding `--before=2026-11-13T02:00:00Z` gives the same blob. Matcher: 15 of 15 VULN at main, 0 of 15 on the trial lock; `npm audit` total 4 -> 0; integrity of all 8 changed entries equals `npm view`. Branch commits ONE path (`package-lock.json`); READY line ends `paths 1`.

**Runtime warning:** 7 of the 8 changed entries are runtime (fastify, fast-uri x2, ip-address, find-my-way, safe-regex2, ret); only undici is dev. Full CI predicate in the kit; Composer deploys only on the product owner's own instruction, so merging does not change the live site.

| Alert | Package | Scope (Dependabot) | Range -> patched | Fix route | In/out |
|---|---|---|---|---|---|
| 26 high | undici | development | `>= 4.0.0, < 6.29.1` -> 6.29.1 | lock 6.28.1 -> 6.29.1; parent json-schema-ref-parser `^6.28.0` admits it | IN |
| 27 high | undici | development | `>= 4.2.1, < 6.29.1` -> 6.29.1 | same entry | IN |
| 18 high | undici | development | `>= 6.23.0, < 6.29.1` -> 6.29.1 | same entry | IN |
| 20 med | undici | development | `>= 6.5.0, < 6.29.1` -> 6.29.1 | same entry | IN |
| 25 med | undici | development | `>= 5.15.0, < 6.29.1` -> 6.29.1 | same entry | IN |
| 14, 17 med; 15, 16 low | fast-uri (4.x) | runtime | `>= 4.0.x, < 4.2.3` -> 4.2.3 | lock 4.2.2 -> 4.2.3; parents `^4.0.0` | IN |
| 19, 22 med; 23, 24 low | fast-uri (3.x, nested under ajv) | runtime | `>= 3.x, < 3.1.9` -> 3.1.9 | lock 3.1.8 -> 3.1.9; ajv `^3.0.1` | IN |
| 13 low | fastify | runtime | `>= 5.12.2, < 5.12.6` -> 5.12.6 | lock 5.12.5 -> 5.12.8 (newest 5.x, inside `^5.12.5` in 4 workspaces); drags find-my-way 9.9.0 -> 9.10.0, safe-regex2 5.1.1 -> 5.1.2, ret 0.5.0 -> 0.5.1 | IN |
| 21 med | ip-address | runtime | `<= 10.7.3` -> 10.7.4 | lock 10.7.2 -> 10.7.6; @fastify/rate-limit `^10.2.0` | IN |

Seat level Sonnet (model-routing.md:92 row C2; models_latest.json:23); pane `Datasec/Security-Composer-C99`; gate G2 class dependency-bump (the kit's G2 row is model-routing.md:109); ports 9750-9759 (0 listeners, control 12 listener lines; 0 of 30 kits hit, control 98xx hit B1534 and B1547; no Composer pane).

## Questions for Tuesday (each with a default)
- Q-1 Fastify target: the kit takes npm's pick, 5.12.8 (inside `^5.12.5`, three patches above the patched 5.12.6, published 2026-11-02). Alternative: exact 5.12.6 (smaller blast radius, a different blob). Default: 5.12.8 as measured.
- Q-2 Manifest floors still read `^5.12.5` etc, so only the lock holds the fix (a fresh install without the lock could resolve lower). Raising them would touch 4 more manifests and cross this kit's one-path property. Default: leave, noted in FOR TUESDAY; a floor-raise is a separate lane if wanted.
- Q-3 `--before=2026-11-13T02:00:00Z` dated install (as the B1534 lane used). Default: yes; measured same blob with and without.
- Q-4 Gate: G2 round 1 of 2 class dependency-bump (fits the 11-12 precedent), but runtime packages changed; the gate can reasonably ask for the DB suites by name. Default: G2.
- Q-5 Pane/seat id C99 and launch window/hard stop slots left blank for you. Default: as the kit; READY target Step 0 + 150 min.

## Facts re-measured with instruments
- main `c2b231fa...` (`gh api branches/main`); 13 raw files hash equal to the contents API (mismatch 0); open PRs 1 (#85 draft held); `matching-refs/heads/b1551` 0 (control b1547 -> 1).
- Alerts: `dependabot/alerts?state=open&per_page=100` length 15, numbers 13..27, each `package-lock.json`.
- Overlap: 196 branches compared; 5 touch manifests/lock (b20, b121, b135 old; b1534, b1547 landed); none live.
- CI read at main: ci.sh:118 `--target ci`, Dockerfile:26 `npm ci --ignore-scripts`, Dockerfile:69 `AS web`; `--target web` appears 0 times in ci.sh (the kit asks the seat to build it); no `.github` path in 1044 tree paths.
- Prior lanes carried: funding.url metadata allowed in the hosts rule (none appears in this diff, 0 added funding lines); expected outputs copied from my runs only (e.g. `up to date in 357ms`, matcher VULN/clear, host-side exercise `5.12.8 4.2.3 10.7.6 / 200 {"ok":true} / example.com / 10.0.0.1`); dated install; drive-local Node 24 path; npm 10.9.8 acceptance via the `npm ci` image build; heavy lock with a rename check (`b1504|c95` count 3 on the original, must be 0 on the copy); default-user containers (B1547's `--user` EACCES finding); inputs table in Step 3.

### Inputs of the chain (each from an earlier step or present at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | the kit, repo clone | kit file; project repo |
| 1 | alerts, branches, registry | produces `out/alerts.json` |
| 2 | clone at BASE, Docker | BASE |
| 3a | 13 manifest+lock files | BASE (clone) |
| 3b | same 13 files copied again, registry | BASE |
| 3c | 3b lock, main lock, `out/alerts.json`, `closes.py` copy | Steps 1, 3b; closes.py exists in the drafter folder and is copied at the start of 3c |
| 4 | clone with the new lock | 3b copy-back |
| 5 | `base-whole.json`, `head-whole.json` | Steps 2, 4 |
| 6-7 | clone, evidence of 3c to 5 | earlier steps |
| 9 | all STATUS numbers | earlier steps |

## D-decisions
- D-1 One path only, no override: measured that no parent bump or override is required. D-2 Dated install in the kit. D-3 Containers run as the image default user (B1547 deviation). D-4 `docker image ls`/probes also under the heavy lock (B1547 slip). D-5 The kit's hosts rule allows npm's funding.url only if python shows it inside an added `funding` object.

## UNMEASURED
Docker, builds, lint, tests, DB suites, web image, `npm ci` under npm 10.9.8 (no docker run by me); whether any script under scripts/tools/docker reads the lock (the seat greps the clone at Step 1; B1547's gate printed 0 `npm ls`); behavioural effect of fastify 5.12.5 -> 5.12.8 and find-my-way 9.10.0 beyond a host-side inject/parse smoke test; hosted CodeQL; deploy impact; `git ls-remote` with the deploy key (I used `matching-refs`); `npm update` inside the image (forbidden in the kit; npm 10.9.8 crashed before).

## Disclosure (outside my two files)
Wrote only the kit, its `.measured`, this report and files under the work folder (raw copies, trial installs, scratch npm home/cache, `ex/` smoke test, quarantine of the first sidecar `measured.v1`). Network: `gh api -X GET` under the Composer `GH_CONFIG_DIR`; `npm view`, `npm audit --package-lock-only`, package installs from registry.npmjs.org into the scratch folder (drive-local Node 24). No docker, no ssh/git writes, no Jira, no mail, no az, no hosted-site request. Imprecisions: the first kit draft said nine changed keys and 13 manifests and six runtime entries; fixed to eight keys, 12 manifests, seven runtime entries before the stamp_check run. A `rm -rf` of a nonexistent trial folder was refused by the hook and not retried.

stamp_check final line: `stamp_check: 106 claims, 106 measured, 0 not measured` (exit 0, run standalone after the last edit).
