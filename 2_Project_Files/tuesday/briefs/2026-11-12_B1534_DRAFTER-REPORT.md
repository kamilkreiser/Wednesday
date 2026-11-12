STARTABLE: YES (with Q-1 to Q-4 defaults; docker must be running at launch, REFUSE 8)

# B1534 drafter report (SEAT-C94, Composer bot-updates re-push). Drafted 2026-11-12 10:57 to 11:06 AEDT (`date` 10:57:02 ... 11:05:52)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1534_SEAT-C94_composer-bot-updates-repush.md`, 113 lines (`wc -l`), 11 stamp slots plus the last line = 12 runs of four underscores (`grep -o -E '_{4}' | wc -l`), 0 non-ASCII bytes, 0 `Laptop-DEV`, 0 person names, 0 card ids. Scratch (mine only): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1534/` (PR JSON, lock copies, `closes.py`, `lockdiff.py`, `jira_get.py` GET-only, `overlap.tsv`, `closes.out`).

## BLUF
- Main `5d3bf82d` (squash 2026-11-11T09:13Z). Both bot PRs are lock-identical to main underneath: main's root `package-lock.json` blob `53305eb4` is exactly the base lock of #91 and of #86. Nothing moved.
- **#91** (open, 2026-10-25, head `301991a8`) = ROOT `package.json` (`vitest ^5.0.0` -> `^5.0.5`) + lock (13 entries; `@vitest/mocker` 5.0.0 -> 5.0.5, vitest, spy, and 8 transitive moves, `siginfo` and `stackback` removed). **#86** (open, 2026-10-20, head `fd24426d`) = `apps/web/package.json` (`vite ^8.2.2` -> `^8.3.4`) + lock (21 entries; vite 8.3.0 -> 8.3.4, rolldown and 15 bindings 1.2.8 -> 1.2.14, oxc types, nanoid, postcss). Union lock (derived by `git merge-file`, exit 0) = blob `39a36218`, 34 entries differ.
- **Alerts closed (23 open, 4 high; length and severity count re-read): #91 closes 2 (alerts 12, 11, both medium, `@vitest/mocker` < 5.0.3). #86 closes 6 (alerts 10, 9, 8, 7, 6 high, 5; `vite` 8.3.0 to 8.3.2). Together 8 of 23; 15 stay open, 3 of them high** (`undici` 6.28.1: 27 high, 26 high, 18 high, 25, 20; `fast-uri` 3.1.8 and 4.2.2: 24, 23, 22, 19, 17, 16, 15, 14; `ip-address` 10.7.2: 21; `fastify` 5.12.5: 13). Neither bot touches those four packages. The ruling closes only 1 of the 4 high alerts; Tuesday should know that before the product owner reads "alerts cleared".
- No live overlap: #85 (draft, HOLD K6, 57 files) holds 0 files with basename `package.json` / `package-lock.json`. Of 196 non-main branches (`compare` each), 5 touch a manifest or the lock: the two bot branches and three old branches whose PRs (#11, #67, #74) merged long ago (50 to 109 behind main). No other open PR.
- What runs CI: nothing hosted for tests (no `.github` in the 1044-path tree). Hosted = CodeQL `Analyze (csharp)` and `Analyze (javascript-typescript)` (both success on main's commit). The project's CI is `scripts/ci.sh` (docker), whose node predicate (`docker build --target ci` = `npm ci --ignore-scripts` in the digest-pinned `node:22-bookworm-slim`, then `npm run ci:node` = lint, format:check, typecheck, build, test) the kit runs step by step, plus `scripts/test-db.sh` and the `web` image target. The host (node 26.13.0, npm 11.20.0) is not the pin, so the lock is regenerated INSIDE the pinned image, after a no-change control that must leave the lock at `53305eb4` (otherwise the pinned npm is not the one that made the lock: STOP).
- The seat does NOT cherry-pick the bots' lock (differs from the MPS B1276 shape on purpose): it runs `npm install --package-lock-only -D vitest@5.0.5` (root) and `... -D -w @pc/web vite@8.3.4`, EXACT versions so a release published since the bots cannot change the result, then compares by program to the 34-entry union and the two bot manifest blobs (`7e6304c1`, `f59f0e7d`).

## Facts re-measured, with instrument and control
| Fact | Instrument | Control |
|---|---|---|
| main sha, lock blob 53305eb4 | `branches/main`; `contents?ref=` `.sha` and `git hash-object` of raw | the two agreed |
| open PRs 91, 86, 85 only | `pulls?state=open` | listing shows 3 |
| #91 / #86 / #85 files | `pulls/<n>/files` | `changed_files` 2/2/57 equal list length |
| bot lock diffs (13 and 21 entries) | python `-I -B` over raw lock blobs at head shas | blobs re-hashed to `7dbad553`, `32cbf3f7` equivalents via hash-object of fetched raw |
| union blob 39a36218 | `git merge-file -p` rc 0 | `merge-file base base #91` hashes to `7dbad553` (the #91 blob) |
| 23 open alerts, 4 high | `dependabot/alerts?state=open` paginate; `severity=high` | numbers 5 to 27 each once; matcher asserted on 4 range cases |
| alert -> lock version match | `closes.py` (version in range, every instance of the package in the lock, at main, #91, #86, union) | `VULN` at main for every alert; `clear` only where the version moved past the patched one |
| code scanning on bot heads | `code-scanning/analyses?ref=refs/pull/N/head` | 91: 0, 86: 0, #118: 2 |
| 196-branch overlap | `compare 5d3bf82d...<head>` per branch, filename regex `(^|/)package(-lock)?\.json$` | the two bot branches matched |
| Jira: no ticket for these bumps | GET-only helper, `project = PCOMP AND ( text ~ "dependabot" OR ... )` = 0 | `text ~ "Route B"` = 26 |
| ports 9880-9889 | `lsof -nP -iTCP:9880-9889 -sTCP:LISTEN` rc 1; kit scan of 48 non-`.pre` SEAT kits of 11-11/11-12 | `lsof` unfiltered lists rapportd; `968[0-9]` hits B1504, B1506, B1519 |
| panes | `tmux list-panes -a`: tuesday, fleet-monitor, MPS-M126, M128, M129, NexusAI-N125, R221; no Composer pane | n/a |
| model row | `awk NR==92` model-routing (C2), `awk NR==23` models_latest (`claude-sonnet-5-5`), `brief_seat.sh:24` | printed |
| landing rule | `awk NR==1799` CLARIFICATIONS.md (C-101 (1)) | quoted |
| load1 | `uptime` 10.37 (11:01), 10.33 (11:03) | n/a |

## D-decisions
- D-1 One commit, not two: lets the seat compare the result to the one-shot union and keeps the squash trivial. (Two sequential installs could produce an intermediate lock that differs.)
- D-2 EXACT-version installs (`vitest@5.0.5`, `vite@8.3.4`) rather than editing ranges and letting npm pick: the registry may now hold newer 5.0.x / 8.3.x; the ruling is the bots' updates, not "latest".
- D-3 Lock regenerated in the digest-pinned image (Dockerfile line 3) with a no-change control, not on the host (npm 11.20 / node 26 differ from the pin).
- D-4 Allowed deviation from the bots' transitive versions is narrow (same entry names, mocker >= 5.0.3, vite >= 8.3.3, transitive still inside its parent's range); a different SET of changed entries is a STOP.
- D-5 Test proof = whole-suite JSON at base vs head, `lost 0 / changed 0 / added 0`, with three planted controls; `scripts/ci.sh` is NOT run whole (it copies withheld SOW text into a container and starts a compose stack; B1506 precedent). Compose-stack, bridge (.NET) and egress sections are listed NOT RUN, reason stated.
- D-6 Heavy lock `.tools/composer-heavy.lock` and B1504's `heavy.sh` reused (RELAYED from B1422/B1495/B1504/B1506 kits); absent at 11:01.
- D-7 Evidence files for the PR (title, body, squash subject/body, landing.txt) written by the seat, Tuesday opens the PR. The seat does not close #86/#91.

## Q-questions for Tuesday (each with a default)
- Q-1 Should the seat also read Jira PCOMP? Default NO: 0 tickets cover these bumps (drafter GET 0, control 26); Tuesday decides whether to file one at landing. The kit gives the seat 0 reads, 0 writes.
- Q-2 If the pinned npm rewrites the lock on the no-change control (the lock was perhaps made with npm 11), what then? Default STOP with both blobs (the kit says so). Alternative if you want it to proceed: allow the seat to regenerate and accept a larger reformat diff, but that breaks the "34 entries" property and the one-commit-small-diff story; I did not draft that.
- Q-3 Run the compose-stack / bridge (.NET) / egress parts of `scripts/ci.sh`? Default NO (not read by these files; B1506 precedent forbids whole `ci.sh`); listed NOT RUN. Hosted CodeQL stays Tuesday's read.
- Q-4 The 15 alerts that remain (3 high, in `undici`, `fast-uri`, `ip-address`, `fastify`): open a separate bump kit? Default: not in this kit; flag to the product owner that option (a) closes 8 of 23 and 1 of 4 high.
- Q-5 (minor) Gate after: G2 (Sonnet) per the prompt; the kit leaves a GATE-ROUND slot for Tuesday. A bump with zero source change might need none; default G2 as ruled.

## UNMEASURED
- Whether docker is running and whether the pinned image `node:22-bookworm-slim@sha256:83f487e0...` is cached (no docker verb run); its node and npm versions.
- Whether the pinned npm reproduces main's lock byte-for-byte on a no-change install (the no-change control is Step 3a; if it fails, STOP).
- Whether npm's regenerated lock equals the merge-file union `39a36218` (predicted possible, not required).
- Whether the whole suite and the database suites pass at vitest 5.0.5 / vite 8.3.4 (bots' PRs show no CI because no workflow exists; nobody has run them on a Composer tree). The kit makes any red a STOP with no source edit.
- Hosted CodeQL on a pushed head; whether Dependabot closes alerts 5 to 12 after the landing (kit tells Tuesday to read `dependabot/alerts` at main).
- The reason default setup skips bot PRs (REPORT.md, still undocumented).
- A fine point: the local `2_Project_Files` `core.sshCommand` names a key path under the old drive name, so the kit makes the seat pass `core.sshCommand` explicitly (B1506 shape).

## Outside the fences disclosure
Reads only: the DRAFTER_RULES, REPORT.md, project `CLAUDE.md`, `JIRA.md` head, `CLARIFICATIONS.md` (grep and two `awk NR` prints), B1276 and B1506 kits (shape), B1504 harness files (`heavy.sh`, `j1_build.sh`, `j_db.sh`, `j_ws.sh`), repo files `scripts/ci.sh`, `scripts/test-db.sh`, `docker/Dockerfile`, `package.json`, `.nvmrc`, `.prettierignore` (local stale checkout, read only), `model-routing.md`, `models_latest.json`, `brief_seat.sh`. `gh api -X GET` only, under the project config; Jira via my own GET-only helper (python `-I`, token never printed, one JQL pattern with parentheses); `lsof`, `tmux list-panes`, `ls`, `uptime`, `date`. No git verb in any project repo; no docker, az, ssh, npm; no `decision_queue.sh` (the ruling text came in the prompt); I did not read `briefs_staged/`, scoreboard, the main ledger or any non-Datasec tree. One slip to disclose: my first `Bash` listing of the project dir printed a long `ls -la` (read only). Writes: the kit, this report, and files in my scratch folder only.
