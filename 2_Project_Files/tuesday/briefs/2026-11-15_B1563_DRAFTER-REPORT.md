STARTABLE: YES (the slice choice, Q1, and the reading of "reads audited", Q2, need your eye at the stamp; the kit holds both defaults and STOPs on any other reading)

# B1563 DRAFTER REPORT (SEAT-N128, NexusAI lane S, the permission core, slice 1), drafted Sun 15 Nov 2026 09:58 to 10:16 AEDT (`date` at start 09:58:37, last `date` 10:15:48)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1563_SEAT-N128_nexusai-permission-core.md` (169 lines, sha256 prefix 7589b1868ef617d4, 5 lines with the four-underscore slot pattern: four slots and the last line; ASCII 0 non-ASCII characters; ban-list name scan 0 with the `_by_kam_` control firing 1; no card id). Sidecar `.md.measured` (238 lines): `stamp_check.py` prints `171 claims, 171 measured, 0 not measured`, rc 0 (run alone, not through a pipe). The sidecar also carries 51 S-lines (S01 to S50 plus S17b) and 14 census lines (C0 to C13), each a real read at main `4ba2e03c`.

## BLUF
- **Scope IN (one seat, about 3 hours of build plus about 95 to 110 minutes of lock hold, red-first):** RD-932 row I-122, part: every 401 and 403 the server answers (reads included) writes ONE audit row `REQUEST_DENIED`; a role change through `PUT /api/auth/users/:email` writes ONE `ROLE_CHANGED` row with the role before and after. New `backend/services/accessAudit.js` (pure), three edits in `backend/server.js` (AUDIT_ACTIONS, the audit middleware, the user PUT), three new test files (13 cells PREDICTED), counts commit K. No status changes, no new gate, inventory proved byte-equal (no commit I PREDICTED). Branch `b1563/nexusai-permission-core-audit`, one push, no PR, nothing deployed.
- **Scope OUT, named in the kit and in READY:** RD-932 I-120 (field grants and the audit of a granted read); the audit of ordinary reads; RD-930 row scope; RD-931 (assistant scope, the answer-cache key, server-built exports and reports); the CSRF refusal (answered above the audit middleware); `POST`/`DELETE` users and SCIM role paths.
- **Why this slice and not row scope:** all three tickets say "Starts after: Roles: capability model and write checks" (RD-929), and RD-929's build is still owed (its comment 41174: "The build this ticket asks for is still owed: one capability check per route, the role source, ..."; `capabilities.js:6` "STATUS: DESIGN ONLY"). The product has only `admin` and `viewer` (`server.js:3501`). The denials and role changes that exist today are the one part of RD-930 to RD-932 buildable with no role source.
- **The ruling, quoted with its comment ids:** RD-930 comment 41029, RD-931 comment 41030, RD-932 comment 41031 (each 2026-11-11 14:58): "the proposed server-side permission model is approved as proposed: every data read, assistant answer, export and report is limited to the signed-in role's department, site, device or person; sensitive fields are masked unless granted; and reads and denials are audited." The accepted recommendation, verbatim on all three: "Approve as proposed. It follows your first Roles ruling (server permissions first)." Recorded as CLARIFICATIONS C-248 (`:2671-2677`).
- **Next slice I propose (B-next):** if you rule Q3 (who holds a field grant), RD-932 I-120: sensitive fields (filenames, fax numbers, named-user evidence) projected on the server by grant on the `data.read` routes that return them, plus the granted-read audit row (Q2's reading). If Q3 is not ruled, the next lane-S kit should be **RD-929's L1 build** (the role source and one capability check per route through `capabilities.decide()`), which is the stated prerequisite of RD-930 and RD-931; RD-930 row scope (first target: the whole-dataset reads, then the normalised-data routes) follows it, then RD-931.
- **Prior work found:** none for RD-930/931/932 in code. 0 commits name the tickets or their row ids on any ref (controls fire); 38 `origin/b1*` refs, 2 ahead of main (the `b1480/*` pair, 58 behind, viewer write-gates and column mapping, not audit); open PRs 0; the Briefs folder names the tickets in 11 files, all as held or owed. RD-929's design-as-data landed (PR 197); its build is owed.
- **Census summary:** nothing pins the absence of the new rows (`REQUEST_DENIED`, `ROLE_CHANGED`, `AUDIT_ACTIONS`, `user_updated`: 0 lines in `__tests__/` and `tests/`); 4 log-injection suites wait for the `STATE_MUTATION` stdout line, so that row must stay byte-identical (the kit holds it and plant P7 proves it); 2 suites filter `[AUDIT]` by their own action and full email; 2 pin the export route's status only; 5 audit-buffer/erasure files are marker-based (a row-count assertion scan printed 0); `rd972` drives the user PUT. All 14 are run in step 4. The inventory holds no audit field and must regenerate byte-equal.

## Facts re-measured (instrument; control)
1. Main `4ba2e03cc88e928c2c6fdf6694ebed0e7cadf2e5`, tree `b52c8378...` (`gh api -X GET .../commits/main`, 09:59:36); my own clone in the work folder detached at it (rev-parse equal). Counts 5636 / 349. Open PRs 0. CodeQL analyses on main: javascript-typescript 64, python 0, actions 0 (default setup; no codeql workflow file). 64 open alerts; inside the edit windows only #237 `js/http-to-file-access` at `server.js:389` (the audit flush, which new rows reach and which the kit does not edit).
2. Tickets read whole by my own GET-only reader `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s276/d1563/jget.py` (credentials read in-process from the project `.env`, never printed; JQL refused unless it starts `project = RD AND (`): RD-929, 930, 931, 932 (To Do, one comment each), plus two searches (a text/link search, 80 issues; `labels = roles-ui-2026-11`, 40 issues).
3. Source at main: `auditLog` `:304`, ring `:300-301`; `AUDIT_ACTIONS` `:415`; `auditMutationMiddleware` `:493`, read early return `:495`, `STATE_MUTATION` block `:502-511`, mount `:1567`; CSRF refusal `:1550` (the only 401/403 site above the mount; 41 sites in all); `requireAdminFor` `:18828`/`:18833`; global gate 401 `:2637-2638`; export route `:2026-2041`; user PUT `:3486`, `:3501`, `:3505`, `:3529-3535`; `getAuthorizedUser` `jsonStorage.js:3934`. Each in the sidecar with its text.
4. **A naming trap found and fixed in drafting:** `ACCESS_DENIED` already appears 3 times in `server.js` as a Log Analytics error code (`:14894`, `:14948`, `:17235`), so the kit names the audit action `REQUEST_DENIED` (0 occurrences repo-wide, as is `ROLE_CHANGED`).
5. Inventory by program (203 rows): GET viewer-refused 20, GET anonymous-401 98, non-GET viewer-refused 59; control GET viewer-200 70. Gate tokens `role !== 'admin'` / `role === 'admin'` at `role-capability-inventory.js:107-108`: the new user-PUT code must contain neither (else `gateInHandler` and `rd978` move).
6. Slot 1 names by program (control `b1430-nodot/b1` -> 6, equal to the precedent): `old12 new16 mut18 inv3 chk4 v62 chk16`. Band and port block free: `lsof` 20000-32200 0 rows, 9790-9799 0 rows (control machine-wide 13); word-boundary scan of the 11 non-`.pre` SEAT kits of 11-14/15 for `979[0-9]` 0 (control `977[0-9]` 3). `b1563` paths absent (control `b1555-nodot` present). Live panes: `tuesday`, `fleet-monitor` only.

## Chain step inputs (each produced by an earlier step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| Commit A | BASE clone, `npm ci`, the line pointers re-read | Step 1 |
| 1 red-first (`old12`) | BASE tree; the three new test files | Step 1; commit A (copied untracked) |
| 2 inventory (`inv3`) | tree at A; `invdiff.py` with its two synthetic controls | commit A; Tools (before the waiter) |
| 3 new-cells (`new16`) | tree at A | commit A |
| 4 related (`new16`) | tree at A; step 2 green (the inventory unchanged) | commit A; step 2 |
| 5 mut (`mut18`) | tree at A; step 3 green | commit A; step 3 |
| 6 mainmove | steps 1-5 green | steps 1-5 |
| 7 plain verify (`chk4`) | head of step 6 (A or M) | step 6 |
| 8 update-counts (`v62`) | step 7's counts refusal | step 7 |
| 9 K (`wt`) | step 8's counts file | step 8 |
| 10 plain verify (`chk16`) | K | step 9 |
No step reads a file a later step makes (the B1545 trap); the inventory runs before the related set.

## D-decisions (drafter, at source)
- D1 One global hook in the existing audit middleware rather than per-site audit calls: every permission denial below the mount (all 40 non-CSRF sites, `requireAdminFor`, the router-level gates, the global sign-in gate) is covered by one change. Reads use `res.once('finish')` so no streaming GET route has its `res.json`/`res.send` wrapped.
- D2 The `STATE_MUTATION` row stays byte-identical, and a refused write gets an ADDITIONAL `REQUEST_DENIED` row (two rows), because four log-injection suites use that line as their end-of-request marker.
- D3 A new pure module (`backend/services/accessAudit.js`) so the classification is unit-testable and the server edit stays small; the existing masking expression is reused verbatim (linear: `[^@]*` then `@`).
- D4 No inventory commit: the slice changes no status; the inventory must regenerate byte-equal, with a BASE control drive only if it does not.
- D5 Model Opus, row C3, gate G1 (security design surface; same as the precedent).

## QUESTIONS FOR TUESDAY (each with a default)
- **Q1 Slice choice.** Build RD-932 I-122 (denials and role changes) first, leaving I-120, RD-930 and RD-931 for later kits? **Default: yes** (it is the only part buildable before RD-929's role source; the tickets' own "Starts after" says the rest waits).
- **Q2 "Reads audited".** Is it every read, or the granted sensitive-field read of RD-932's description ("a request with it gets the field and an audit row")? **Default: the granted read, built with I-120 in the next slice;** this kit audits no ordinary read and its cell D4 pins that.
- **Q3 Who holds a field grant** while the earlier Roles ruling keeps "today's viewer keeps what it can read" (RD-929 text; `capabilities.js:21-22`)? Masking filenames from today's viewers would remove reads they have. **Default: the next slice does not start until this is ruled (a product-owner question); B-next then falls back to RD-929's L1 build.**
- **Q4 Flood shape.** A refused anonymous GET now writes a row into the 10,000-row export ring (98 GET routes answer anonymous 401), so a scanner can push older rows out of the export window faster than today (it can already do so with refused writes). **Default: accept for this slice** (every row also goes to the `winston` log through `auditLog`'s `logger.info`, the durable store; the general limiter caps each address); a coalescing rule, if wanted, is a later ticket.
- **Q5 Work tracking.** The kit forbids Jira; RD-932 stays To Do and is moved by your records seat at landing. **Default: yes** (the project rule `CLAUDE.md:288-292` is met by the existing ticket).
- **Q6 Model and gate.** **Default: Opus, C3, gate G1 on Opus.**

## UNMEASURED
- Every cell's received value (PREDICTED red-first 8 red / 5 green; 13 cells; pair about 5649 / 352); the inventory drive time on this change; whether `req.route`/`finish` timing produces any duplicate row on a HEAD request (the kit asks for HEAD; no cell drives HEAD: the seat may add one).
- Whether CodeQL's hosted analysis adds a path to #237 (`js/http-to-file-access`) from the new rows: the sink is the existing flush; the gate reads the PR head and main's analysis after landing.
- The B1561 records seat's live state (not running at drafting).

## Outside-the-fences disclosure
- Writes: the kit, its sidecar, this report; scratch only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s276/d1563/` (my Jira reader, ticket texts, alert TSV, port and census outputs, the S-line and sidecar programs, and a clone of the repository by SSH with the project's deploy key, push URL set to `invalid://no-push-drafter`, detached at `4ba2e03c`, never pushed). Nothing written under `/Volumes/Datasec_DEV/!CODING/`; the project checkout was not fetched or touched; no Jira write; no GitHub write; no message; no az; no tmux send-keys (one `tmux list-panes` read).
- Reads in the project folder (read-only): `CLAUDE.md`, `CLARIFICATIONS.md`, the Briefs folder (grep), `session-tools/nexusai-lock.sh` header, the lock directory listing, `.env` variable NAMES only (values read in-process by my reader, never printed).
- Hook events: a `cd` refused (nothing ran); an unquoted `======` refused (nothing ran); a `git -C $D/clone checkout` refused because the hook did not expand the variable (re-issued with the literal path inside the TUESDAY tree); several advisories on case-sensitive greps and `grep | cut`. No fence was bypassed.
- `DRAFTER_RULES.md` names `/Volumes/Laptop-DEV/...`; I used `/Volumes/Datasec_DEV` everywhere.
- Weakest parts: Q2 and Q3 (readings of the ruling), the PREDICTED red-first split, and plant P8 (U2's stub must carry a planted cookie for it to fire).

DRAFTED B1563: kit 169 lines, sidecar rc 0, questions 6
