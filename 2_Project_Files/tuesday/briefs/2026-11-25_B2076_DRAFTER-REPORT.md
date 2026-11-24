STARTABLE: YES (once pull request 253, lane NX-S2, is on main: the kit refuses any BASE that does not hold `9d4ddb7f`)

# B2076 DRAFTER REPORT: NexusAI RD-1040, the plain data-source reads refuse roles without config.read (seat N173)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2076_SEAT-N173_nexusai-rd1040-datasources-roles.md` (164 lines, 0 non-ASCII bytes, 5 four-underscore lines: four slots and the last line). Sidecar `.measured`: 172 claims, 172 measured; `stamp_check.py <kit>` rc 0. Commission: `2026-11-25_B2076_NEXUSAI-RD1040-DATASOURCES-ROLES_DRAFTER_COMMISSION.md`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s326/d2076/` (frozen files in `frozen/`).

## BLUF
- **The build is small.** One product file gets 19 added lines and 0 removed. A helper `refuseDataSourceReadForRole(req, res)` sits beside the two routes. It reads `ROLE_CAPABILITIES` from `backend/services/capabilities.js` and answers 403 before the store is read, unless the session's stored role is an own key of the table whose entry holds `config.read`. Its call is the first statement of `GET /api/data-sources` and `GET /api/data-sources/:id`. With no session (open mode) nothing changes. Allowed roles get the same answer as before, field for field.
- **Tests.** One new test file with 21 tests.
  - Red-first: 8 failed of 21, the same 8 at main `4d8713e5` and at NX-S2's head `9d4ddb7f`.
  - Green: 21 of 21. The 59-suite set passed 834 of 834.
  - Red-proof: the same 8 failed.
  - Full verify at a prototype A on `9d4ddb7f`: `VERDICT: PASS`, 6362 of 6362 tests across 401 suites, `EADDRINUSE` 0.
  - Local CodeQL at the prototype K: rc 0 (NEW 0, KEPT 0).
- **Sequencing.** I drafted on main `4d8713e5` and proved everything on `9d4ddb7f`, the NX-S2 head (pull request 253, open). The kit's expected BASE is the merge commit of pull request 253. HOLD 20 requires `9d4ddb7f` to be an ancestor of BASE, and BASE may differ from it only in non-code paths. NX-S2 moves the two routes by +3 lines (15691/15703 to 15694/15706). The apply script anchors on text, so the move does not matter: it was applied to both blobs.

## Facts re-measured at source (instrument; control)
1. **Main.** Read at 08:07:59 and again at 08:20:26 (`gh api -X GET .../git/ref/heads/main`):
   - Main is `4d8713e5353d589a8680d328e2e00a69b8ea7480`, the merge of pull request 252, which changed `HISTORY.md` only (`compare/11149d3f...4d8713e5`).
   - In code, main equals `11149d3f`: `git diff --quiet` over `backend __tests__ scripts static package*.json jest.config.js .github` returned rc 0.
   - At 08:20, 1 pull request was open: 253 (`b2074/...`, head `9d4ddb7f`, base `4d8713e5`).
   - Gate B2075 reads `GO WITH FINDINGS @ 9d4ddb7` (I read only the first line of its VERDICT).
   - `b2076` refs at origin: 0 (control: `b2074` reads 1).
2. **NX-S2's move in `backend/server.js`.** `git diff --unified=0 11149d3f 9d4ddb7f` shows two hunks, `@@ -458,0 +459,2 @@` and `@@ -13775 +13777,2 @@`. Blobs: main `6d8e5139...`, `9d4ddb7f` `a7426b07...`. Counts at `9d4ddb7f`: 6341 / 400.
3. **The permission table** (`capabilities.js` at main):
   - Line 155 puts both routes in `config.read`.
   - Excluded, by program over `ROLE_CAPABILITIES`: `end_user`, `partner_manager`, `partner_technician` (lines 117 to 119).
   - Allowed: `admin`, `viewer` and the five proposed roles. `decide()` (line 249) answers `forbidden` for a role it does not name (line 258).
   - The header at line 6 reads `STATUS: DESIGN ONLY`. Control: `grep -c ROLE_CAPABILITIES` over server.js at main reads 0, and `requireAdminFor` reads 51.
4. **Which roles a real user can hold** (read; X1 to X3 run part of it):
   - Every request reads the role from the stored user (server.js lines 2787 and 2790). A missing user or an empty role reads as `viewer` (lines 2790 and 2793).
   - The create route (line 3607) stores whatever role an administrator sends (line 3645), capped at 32 characters (line 2826). No page offers that choice: `newUserRole` is read once, at settings.js:3165, and defined in no static file.
   - The update route accepts only `admin` or `viewer` (line 3693).
   - A first sign-in through the identity provider stores `viewer` (line 3511).
   - The provisioning modules write no role: 0 `role` lines in three files (control: `routes/entraProvisioning.js` prints 4).
   - So every table role, and any other string, can be held only through the create route's API. The cells cover all 10 table roles plus 7 other shapes.
5. **The region filter**:
   - `static/js/index.js` lines 4284 to 4303 run `apiFetch('/api/data-sources')` and fill the select only on `dsResp.ok`, inside a `try` whose catch does nothing.
   - The select starts with one option, All Regions (index.html 316 to 318).
   - The new test's cells F1 and F2 run that block in jsdom: with a 403 the filter keeps one option and nothing throws.
   - Other static callers of the two GETs: `admin.js` 246 (RD-1036's viewer list, which shows `HTTP 403` for a refused role, its cell T6) and `index.js` 4288. Nothing else (git grep).
6. **Sibling leaks (FINDING, not built).** I ran a program over all 35 `config.read` handlers.
   - `GET /api/setup/status` (line 14608) sends every signed-in role the Log Analytics workspace id and endpoint (lines 14630 and 14631) and the sign-in tenant and client ids (around 14680).
   - `log-analytics/diagnostics` (15397) sends the endpoint and a workspace display.
   - `validate-all`, `models/active` and `service-check` name an endpoint.
   - Wider: no route reads the table at all. The partner roles, which the table grants nothing, and end_user can read every route a viewer can read today.
7. **Ports and slots.**
   - Slots (`worktreeSlot` formula; controls `b2074-nodot/rf` 7 and `vupd` 16, as kit B2074 recorded): `b2076-nodot/rf` 16, `work` 14, `vupd` 15, `chk` 7.
   - All four bands had 0 listeners at 08:44 (control: 12 listeners machine-wide). No fixed port.
8. **Seat id N173 is free.** `ls briefs | grep -c N173` read 0 before this kit; a word grep finds N173 only in the commission. Control: N172 reads 3 files.
9. **Panes and status files.**
   - Live panes: `tuesday` and 2 unnamed; no `Datasec/NexusAI-*` pane.
   - NexusAI STATUS files of 22 to 28 Nov: 17 (16 `READY`, 1 `DEPLOYED`). The newest is `READY B2074: 9d4ddb7f...`.
10. **Model routing.** Rows C3 (line 93) and G1 (line 108); `claude-opus-5-5` (models_latest.json line 17). C-190 is at line 2067 ("Never squash, never rebase").
11. **Deploy demo.** Lines 26 to 32, 53, 91 and 95 of the workflow. The last 20 of 266 runs read `skipped`.
12. **Code scanning.** 22 open alerts, 13 of them in server.js, and none in lines 15685 to 15730.

## How it was run (where and at what load)
- **Jest.** Four jest-lock acquisitions (`d2076-proto1`, `-proto2`, `-lane`, `-verify-update`).
  - Each was acquired after 0 s, with `queue-jest` at 0 and no holder.
  - Load averages 1.1 to 2.5. Window 08:15:30 to 08:41:51.
  - All four are released (`released/` lists 4 `d2076` entries; 0 jest, codeql or lock processes left at 08:46).
- **CodeQL.** Run outside the jest lock, 08:42:11 to 08:43:14, with work in my scratch.
- **Not run:** the plain verify at K, the seat's own clone and `npm ci`, and the merge commit of pull request 253.

## D-decisions (the drafter's, within the commission)
- **D-1. The design reads the table itself** (`require('./services/capabilities')`) rather than a hard-coded role list. The refusal then follows the table when it changes, and S1 pins today's excluded set.
- **D-2. Allowed roles take the existing code path unchanged.** R2 asserts that each of the 6 allowed non-administrator roles gets an answer deep-equal to the administrator's, on both routes. This is the ruling's "keep fields as they are".
- **D-3. The helper's name is not an inventory gate token.** As a result, `rd978` (which counts gated handlers, line 88) and `rd929` stay true without touching them. Both are in the 834 green.
- **D-4. The refusal comes before the store read**, so an unknown id gets 403, not 404, for a refused role (X4). Without this, the status would reveal which ids exist.
- **D-5. The prototype ran on `9d4ddb7f`, not on main.** The commission puts NX-S2 first, so the counts K must carry are 6341 / 400 + 21 / 1 = 6362 / 401.

## Chain inputs (each step's inputs are made by an earlier step or exist at BASE)
| step | inputs | made by |
|---|---|---|
| Step 0 | the kit, the frozen folder, RD-1040 (Jira), STATUS Corrections of B2069 and B2074, B2071 VERDICT | at BASE / the drafter |
| Step 1 / 1b | the project checkout (clone source), the lock base, `.tools/b2074/clone` (identity read), origin main | exist at launch |
| 0 trees | BASE sha40, `apply2076.py`, the frozen test file | Step 1, Step 0 |
| 1 quiet | lock base | exists |
| 3 lane | `rf`, `work`, `lane2076.sh`, `judge2076.py`, `suites2076.txt`, `apply2076.py` | step 0, Step 0 |
| 4 astep | `work`'s two files, `wt`, `static2076.py`, `msg-A.txt`, names (scanlib1114.py line 20) | step 3, step 0, Step 0 |
| 5 update | A sha (vupd), `v2076.sh` | step 4 |
| 6 kstep | vupd's counts file, `msg-K.txt` | step 5 |
| 7 plain | K sha (chk) | step 6 |
| 8 mainmove-last | BASE | Step 1 |
| CQ / push | BASE, K, clone | Step 1, step 6 |

## Q-questions for Tuesday (each with a default)
- **Q-0.** A stored role that the table does not name is refused 403. Examples: another case (`End_User`, `Admin`, `VIEWER`), a built-in property name, a made-up word, a value with spaces. This is fail-closed, the same as the table's `decide()` (line 258). Today such a user is answered the list. **Default: accept** (X1 freezes it). The alternative is normalising case or space, which is a new behaviour that nothing asks for.
- **Q-1.** Model: Opus builder (C3, line 93) and a G1 gate after. **Default: as the commission says.**
- **Q-2.** The dashboard's region filter for a refused role keeps only "All Regions" and logs one console error. It is checked by F1 and F2, not changed. **Default: accept, build nothing.** Whether a refused role needs region names at all belongs to the later fields question.
- **Q-3.** The sibling leak `GET /api/setup/status` (workspace id, endpoint, sign-in tenant and client ids, to every signed-in role) and the fact that no route enforces the table (partners read everything a viewer reads). **Default: report, do not build.** Propose one ticket for the setup status fields and one for enforcing the table on every route (RD-929's L1).
- **Q-4.** `capabilities.js` line 6 (`STATUS: DESIGN ONLY ... Nothing in the product requires this file yet`) becomes untrue, and it is outside the partition. **Default: leave it.** The records pass names it, and a follow-up corrects the header.
- **Q-5.** The inventory (`docs/role-capabilities.json`) is not regenerated. Its four modes (anonymous, viewer, administrator, open) read the same before and after (N1, R2 for viewer, A1, O1), so no row's statuses move. Its `capability` text "handler gate: none" for the two rows stays as it is, which is the scanner's named blind spot for a helper with another name. RD-1040's acceptance says "regenerated if a row moves". **Default: not regenerated.**
- **Q-6.** The 403 body is `{ error: 'Data source settings are not available to this role' }`. It names no role and no field. **Default: accept.**
- **Q-7.** Deploy: none. A merge starts a `Deploy demo` run; reading it at landing is Tuesday's job (the C-224 hold stands). **Default: as stated.**
- **Q-8.** Launch only after pull request 253 lands. Tuesday re-pins `HEADS AT LAUNCH` to its merge sha. If NX-S2 is reworked (new commits), `9d4ddb7f` is no longer BASE content, HOLD 20 stops the seat, and a re-draft is needed. **Default: as stated.**

## UNMEASURED
- The merge commit of pull request 253. Its tree is PREDICTED to equal `9d4ddb7f`'s plus `HISTORY.md`.
- The plain verify at K (PREDICTED 6362 / 401).
- The seat's own `npm ci`.
- Roles from the identity provider's app roles or a restored store.
- OPTIONS requests.
- The sign-in-unproven state, and a session during the first run with sign-in configured.
- Any hosted instance, real browser or Linux.
- The full verify on `4d8713e5`, which is not an allowed BASE.

## Outside-the-fences disclosure
1. **Hook refusal.** One Bash call was REFUSED by `pretooluse_no_cd.sh`: a `git -C "$S/clone" checkout` whose variable path the hook could not resolve. Nothing ran in that call. I re-issued the clone and checkout with literal paths inside my scratch.
2. **Read-only reads of another seat's tree.** `git clone --no-hardlinks --no-checkout` of `.tools/b2074/clone`; `cat` of `.tools/b2074/runlane.sh` and `cq/runcq.sh`; `git config --get` of that clone's identity (lengths only). Also read: the project's STATUS files, CLARIFICATIONS (`awk NR==2067` and a grep only), and session-tools line 20.
3. **Writes outside my scratch and my three files.** Only the jest lock's own bookkeeping under `session-tools/locks-laptop-1017/` (4 acquisitions, released).
4. **Scratch identity.** I set a repo-local identity (`drafter scratch`) in my own scratch clone for the prototype commits A `3eeece6845de` and K `ff66c989528e`. They were never pushed.
5. **The card.** Read with `decision_queue.sh show <exact id>` into `card.txt`, then the whole of that one file printed. No `list` call. Nothing written to the card store, Jira (GET only: RD-1040, RD-1036, RD-1021) or GitHub (`-X GET` only, plus `gh api user`).
6. **Quarantine, nothing deleted.** The gitleaks plant (`_quarantine/plant.txt`) and the dot-path probe folder (`_quarantine/dotprobe`) are quarantined.
7. **Messages.** Nothing was sent to any human.
8. **Faults avoided.** No `cd` was typed. One `$?` was read after a pipe, on a control line whose output (`STATIC A FAIL`) was read directly. The hook flagged it as advisory, and no rc in the kit or the report rests on it.

Last `date` of the drafting: Wed 25 Nov 2026 08:46:06 AEDT
