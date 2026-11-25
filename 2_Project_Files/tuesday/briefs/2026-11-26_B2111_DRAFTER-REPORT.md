STARTABLE: YES

# B2111 drafter report: MPS lane L2, kit `2026-11-26_B2111_SEAT-M177_mps-l2-e2e-smoke.md` (read-only drafter, Sonnet 5.5, for Tuesday s329)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2111_SEAT-M177_mps-l2-e2e-smoke.md` (91989 bytes). Sidecar: `...smoke.md.measured` (213 claims, `stamp_check.py <kit>` exits 0; 59 lines are "UNMEASURED by design", the seat's own commands and words). Scratch (every run, log, prototype tree): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s329/d2111/`. Seat id M177 is free (no SEAT kit in `tuesday/briefs/` names it: 0 hits of a word-boundary scan; `.tools/b2111*` absent; `matching-refs/heads/b2111` 0 rows, control `b2106` 1 row; the control kit M176 is B2106's).

## BLUF
1. The commission's premise (one stub change: calculate) is too small. **Four answers** are needed on the stub leg (calculate, submit, approve, the proposal): after #193 only the update of a stub-created rental quote is answered by the stub. Built and run on a prototype: one new module `web/src/api/stub/heldRentalFlow.ts` (89 lines, typed against the generated contract), spliced into `stubApi.ts`, eight new stub rows, six mutants all killed.
2. **The live leg (API on a synthetic store) is red at base for a reason nobody had**: `smoke.spec.ts:78` expects 5 rows in the proposal's first table; the short form has capped device lines at three plus a pointer row since MPS #189 (2026-11-12, MPSCALC-110), so it reads 4. The #178 review's green on 2026-11-11 predates it. One-literal fix; `print.spec.ts:87` already pins the same cap.
3. **The no-API leg cannot run the journey by construction** (stub off, nothing behind the proxy). The kit makes the spec skip itself there with a stated reason (the `b30` / `b46-home` pattern): whether that satisfies "green in all four legs" is Q3.
4. MPSCALC-297 clause 1 (`b46-home.spec.ts` exact nav) needs no edit: 15 of 15 green in stub mode, 15 of 15 skipped with the stub off, by its own rule.
5. No customer word changes. One new stub-only string (dev double); the production Entra build proves it absent (control fired).

## Facts re-measured (instrument; control)
- Main `15bca4ec3526cf609f50915221664c0231b5cc12` (`gh api -X GET git/ref/heads/main`); open PRs 0; #229 merged 2026-11-25T19:40:30Z; its 8 paths (`gh api pulls/229/files`) include none of this lane's. Commits by path (`commits?path=`): nothing after #228 on the owned paths. Local project tree HEAD `1807bec2` (C-193); `CLARIFICATIONS.md` equals HEAD by `git hash-object` (so C-133, C-149, C-168 read at root main).
- Tickets by Jira GET (in-process token, never printed): MPSCALC-135 Backlog, 2 comments (newest 41135), `updated` 2026-11-11T22:24:12; MPSCALC-297 Backlog, 6 comments (newest 41139). Read whole (description and every comment).
- **Four legs at base, one run each, node v24.22.2, installed Chrome, scratch copy of the tarball of main** (drafter's own run; the kit makes Step 2 the seat's): A default / 1440 / 390 red at `:78` (`Expected: 5`, `Received: 4`); B (stub on, no API) red at `:52`; C (stub off, no API) red at `:27`. API for leg A: a throw-away console project (kit block) builds the importer's own invented books into a reference store (`devices 4`, sha256 `7c67faea...`, two builds equal), the project's `.tools/dotnet-10.0.404` builds `MpsCalc.Api`; started from its build folder with the three store paths empty.
- **After the frozen script** (extracted from the kit by program and run on a pristine copy; blobs equal the tested tree; a second run STOPs "already exists"): leg A 3 of 3 at default, 1440, 390; leg B 3 of 3 and 1 of 1 at 390; leg C `1 skipped`; `b46-home` 15 passed (stub) / 15 skipped (stub off).
- CI modes as the workflow runs them (HEAVY, serial): stub step base `260 passed, 17 skipped`, prototype `261 passed, 17 skipped` (4.2 min each); stub-off step base `162 passed`, prototype `162 passed, 1 skipped` (2.5 min each). Whole `vitest`: base 149 files / 1742 tests, prototype 149 / 1750. `tsc -b` rc 0, `npm run lint` rc 0 at both. `src/api/stub`: 128 rows at base, 136 after. Seven of the eight new rows are red against base stub code (`7 failed | 129 passed (136)`); the eighth is the pass-through guard.
- Production build: `VITE_MPSCALC_AUTH=entra npm run build` rc 0, `check-bundle.mjs` `dist: 8 files, 1112909 bytes; markers found 0/57`; the stub's new string found in 0 `dist` files; control: a `VITE_MPSCALC_API_STUB=1` build into another folder holds it in 1 file.
- `scans2111.py` (copy of the B2106 scanner with this lane's paths): `added lines: 295`, non-ASCII 0, Cf 0, GUID 0, 12 names quiet and 12 controls fired, tab 0.
- Heavy-job rule: **no project file states it as a rule** (`CLAUDE.md`: 0 hits of `heavy`, control `friday` 4). It is carried in stamped kits; the kit quotes it from the L1 kit of 2026-11-11 (line 61: two slots, `.tools/.heavy-lock-1/-2`, load1 under 24 on two reads 120 s apart, "scales to this 18-CPU machine"), marked RELAYED, and Stamp S4 confirms or changes it. My runs: scratch-local lock, load1 2.3 to 7.2, never above one Playwright job plus one light job.

## D-decisions (mine, in the kit)
- D1: leg A is a hand-run leg with a frozen recipe (no CI step: the web job has no API or store).
- D2: stub answers are zero-figure, `STUB`-marked, in the manner of the purchase stub's `notPriced`; no pricing invented.
- D3: widen the lane's property from four named paths to six (`purchaseQuotes.ts` one comment line, `stubApi.test.ts` rows, new `heldRentalFlow.ts`): needed for rows and to correct three comments that said calculate "still goes to the real API".
- D4: two commits (stub, then specs and config); CI stays green after each (smoke is left out until commit 2).
- D5: proposed ports web 59311 / API 59310 (none listening; no SEAT kit of 2026-11-25/26 names them); the seat sets `MPSCALC_WEB_PORT` and `MPSCALC_E2E_BASE_URL` together (verified on 59311).
- D6: `mutate_l2.py` frozen for six mutants; all six turned a row red (m1 six rows, the others one each).
- D7: the kit does NOT claim the ticket moves: records seat's job.

## Questions for Tuesday (each with its default; also in the kit)
- **Q1 four legs.** Default: A (API on synthetic store), A at 390 px, B (stub on, no API), C (stub off, no API); Linux = hosted CI after landing. Alt: add A at 1440 and B at 390 (both green).
- **Q2 level.** Default sonnet (row C2, `model-routing.md:92`), `claude-sonnet-5-5` (`models_latest.json:23`); the project `CLAUDE.md` names no model (0 hits). Launch carries `BRIEF_SEAT_LEVEL=sonnet`.
- **Q3 (STOP-class) does a skip count for leg C.** Default: spec skips with its reason; ticket stays open on clause 4's wording. Alt: leave smoke out of the stub-off step; or a ruling that clause 4 means the three legs that can answer.
- **Q4 leg A in CI.** Default: hand-run. Alt: a later lane adds a CI step (a `ci.yml` change, outside this lane).
- **Q5 (STOP-class) stub scope.** Default: four answers, new module, eight rows (lane widened to six paths). Alt: calculate only, spec ends early in stub mode.
- **Q6 the new stub string a words card?** Default: no (dev double). **Q7** literal 4 with the cap named. **Q8** two commits. **Q9** ports 59311/59310. **Q10** gate G2 (`model-routing.md:109`) because the stub is dev-only and the production build proves it absent; alt G1/Opus.

## UNMEASURED (a stamp must know)
- **No hosted/Linux run**: `channel: chrome` smoke on `ubuntu-latest` and the two CI steps with smoke added are unproven on the runner (the same Chrome runs other specs there).
- One run each at base per leg and 3 repeats after (no 20-run flake census); smoke is a 1-test spec, about 1.2 s.
- The load-23 ruling and slot names are RELAYED from the 2026-11-11 kit, the ruling's own record not re-read; the drafter used a scratch-local lock, not the project's.
- The product owner's reading of clause 4 (Q3) and whether the stub string needs a words card (Q6).
- Stub rows' wording and mutants are of the prototype; the seat's run must equal or NAME the difference. The drafter did not run the Api test project, `dotnet test`, `npm audit` or gitleaks (kit steps for the seat).
- Stamp slots S0 to S8 and the last line are left as four underscores; the attribution lines in the commit bodies are for the seat's session reminder.

## Chain inputs (rule 4: each input is produced by an earlier step or exists at base)
| Step | Inputs | Where they come from |
|---|---|---|
| 1 clone | project checkout, origin, base sha | exist at base |
| 2 baseline and four legs | `node_modules`, store builder, Api build, store, legs configs | `npm ci` (step 2), kit blocks saved in step 2, `dotnet build` (step 2), `synthstore` run (step 2), `pw-*.config.ts` made in step 2 |
| 3 predictions | step 2 totals | step 2 |
| 5 edits | `apply_edits_l2.py` (kit block), six base blobs | kit; exist at base |
| 6 mutants | changed `web` copy, `mutate_l2.py` | step 5; kit block |
| 7 legs after, 8 CI modes, 9 build | edited clone, API build and store | step 5; step 2 |
| 10 checks | `scans2111.py`, base tree | kit block; step 1 |
| 11 commits, 12 push | edited tree, scan result, commit texts | steps 5 and 10; kit |

## Outside the fences (disclosure)
No write in the MPS project folder (reads only: `CLAUDE.md`, `CLARIFICATIONS.md`, `BACKLOG.md`, `1_Project_Definition/Briefs/` kits and status of B1502, `.tools` listings, `git rev-parse`/`hash-object` on the local repo). `gh api -X GET` only, under the project's `GH_CONFIG_DIR`. Jira GET only, through a scratch helper that read the project `.env` in-process (no token printed). Processes I started, all under scratch and loopback: `npm ci`, `tsc`, `eslint`, `vitest`, Playwright with the installed Chrome (ports 5183 and 59311), `dotnet build` of the importer-based store builder and of `MpsCalc.Api`, the API on 127.0.0.1:5180 (stopped by pid; port free; no `MpsCalc.Api.dll` left), a one-second API start from the wrong folder on 59319 (it refused and exited). Edits by `sed -i ''` and python on scratch copies only (not on repo files). One attempted `rm -f` of a scratch file was refused by the hook and never re-issued; the scratch lock folder's empty directory was `rmdir`ed (my own, scratch). Moved to `_quarantine` in scratch: superseded sidecars and my capture spec. No card store, no mail, no message, no Azure/ssh/docker/hosted request. `decision_queue.sh` never invoked.
