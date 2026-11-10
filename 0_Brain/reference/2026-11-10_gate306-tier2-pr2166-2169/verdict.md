PR 2166: GO
PR 2167: GO WITH NOTES
PR 2168: GO WITH NOTES
PR 2169: GO WITH NOTES

Gate 306, tier 2 (Sonnet), 2026-11-10 17:44 to 18:1x AEDT. Findings only. Nothing posted, mailed, pushed or fetched in !CODING (reads there: ls-remote, show, log, diff, ls-tree, cat-file, grep, rev-parse, cat; the objects came from the shared store of worktrees/s-r90-base by `git clone -s` into my scratch). All tests and mutants ran in my own scratch clone (`scratchpad/repo`, full tree at the pinned shas, node_modules COPIED read-only from s-r94-b with the self-looping `node_modules/node_modules` symlink removed in my copy).

## Pins (re-read at start 17:44:57 and end 18:08:47 by ls-remote; NONE moved)
- develop 0b55401ad5dcb748f9dc47189f9896209567eb75 (unmoved). Its one-commit move from b602c418296a (PR 2156 squash) changes 14 files (`git diff --name-status b602c418296a 0b55401ad5dc`): `.claude/hooks/*`, `.claude/settings.json`, `.gitignore`, `CLAUDE.md`, `ks1785_secret_guard_contract.test.sh`, `restore_local_secrets.test.sh`, two KS-1785 fragments, `systemTest/CLAUDE.md`, three `.env.example`. It touches NONE of the 7 files the four PRs write, and not `.githooks/pre-push` (the file PR 2166 reads).
- PR 2166 head a0ff676ebaae, PR 2167 head 86b0dde15f91, PR 2168 head 2ea098978a4a, PR 2169 head 3521d7889c93: all unmoved. Each: one commit, parent b602c418296a, base develop, state open, not draft.
- Machine: load1 high all session (a drive copy). Whole-suite legs started at: api-gateway develop 7.22 (<8); api-gateway head 10.05 and 12.20 (OVER the line, both 169 files / 1,897 passed) and then 7.79 (<8, same result); analytics head 7.67, develop 7.57; originate head 7.76, develop 7.81. The bash hook-suite runs for PR 2166 and the red-proof/mutant runs were short targeted runs at load 8 to 10 (not whole-suite legs). df DevMASTER 93 GiB available at start and end.

## Cross-cutting, FOUND
- File sets by the PR files API (GitHub REST, token read in-process from the Secuura .env, never printed) AND by `git diff --numstat b602c418296a <head>`: they agree.
  - 2166: `Blockchain/Dev/scripts/__tests__/pre_push_red_preflight_refuses_the_push.test.sh` added +80 -0. Nothing else. No product byte.
  - 2168: `.../analytics/src/services/exportService.ts` +3 -1 (PRODUCT) and `.../analytics/src/__tests__/ks1922-failed-export-stores-a-constant-reason.test.ts` +93. Nothing else.
  - 2167: `.../originate/src/routes/metering.ts` +7 -0 (PRODUCT) and `.../originate/src/__tests__/ks1875-a-repeated-from-or-to-on-metering-usage-is-refused.test.ts` +101. Nothing else.
  - 2169: `.../api-gateway/src/routes/audit-export.ts` +5 -2 (PRODUCT) and `.../api-gateway/src/__tests__/ks2015-audit-export-accepts-only-real-yyyy-mm-dd-dates.test.ts` +92. Nothing else.
- Held-Spark comparison, per file, changed lines (+ and -) extracted from each READY's fence and from `git diff b602c418296a <head>` (scratchpad `cmp.py`): 2166 EQUAL (80); 2168 EQUAL on both files (93 test, 4 product); 2167 EQUAL on both (101, 7); 2169 EQUAL on both (92, 7). No difference. (Hunk headers and context differ in width, as expected.)
- Open-PR census by the API: 84 open PRs, 374 file rows. Positive control: the four PRs themselves return for their own paths, and `Blockchain/Dev/docs/openapi/secuura-api.yaml` returns PRs 2131, 2099, 2073 (the 2156 control of gate 305 has since merged, so I used these). Each PR's two paths return only that PR. Files the cells read or the code touches around: `.githooks/pre-push` none; `api-gateway.openapi.ts`, `METERING-USAGE-API.md`, `analytics.openapi.ts`, `ExportDialog.tsx`, `preflight.sh` none; api-gateway `index.ts` is in open PR 2125 (and `secuura-api.yaml` in 2131/2099/2073) but no cell of 2169 reads either and 2169 does not write them. No sharing among the four or with any open PR.
- Merge trees onto develop 0b55401ad5dc (`git merge-tree --write-tree`): 2166 alone rc 0 tree 4941c98194a7; 2168 alone rc 0 tree 63cc85a5161c; 2167 alone rc 0 tree 89cef7439148; 2169 alone rc 0 tree aa7ec9502541; all four together (two-parent commits chained) rc 0, final tree e6f67c682dd0, and its numstat against develop is exactly the union of the 7 file rows above (80, 93/3-1, 101/7, 92/5-2) and nothing else. Planted control: 2168 merged onto a commit that rewrites the same line of `exportService.ts` returns rc 1 (conflict), so the instrument can fail. No conflict among the real trees.
- Closing words: searched title, body, commit message and the one GitHub comment of each PR (the Linear linkback) plus the four seat comments on the tickets, with `close/closes/closed/closing/fix/fixes/fixed/resolve/resolves/complete` (planted positive `Closes KS-1 and fixes it` hit). Title, body, commit: 0 hits on all four. The only hits are inside the Linear linkback, which quotes the ticket's own text (2166: "costs one cell to close", "Fix shape", "early-closing pipes"; 2168: "during the fix"); none is in closing form. All four say `Refs` and that the ticket stays open.
- Tickets (Linear, read-only, newest comment last): KS-2091, KS-1922, KS-1875, KS-2015 are In Progress, each with exactly the seat's one PR-naming comment. Nothing contradicts the PRs.

---
## PR 2166 (KS-2091): GO

FOUND
- Test-only, one new bash suite (4 cells), zero product bytes, hook not in the diff. It builds a bare remote and a clone, installs a COPY of `.githooks/pre-push` as the clone's hook, swaps the preflight for a stub exiting `PREFLIGHT_RC`, and checks: CONTROL green push lands, CONTROL red stub ran, red push does not land, hook prints `[pre-push] preflight failed`. Two cells are labelled CONTROL and two are the pins; the labelling is honest.
- It does what KS-2091 asks (the ticket's fix shape: fixture preflight with non-zero exit, assert the push did not land and the refusal text appears) and no more. Body claims the same and says the hook is correct today and the ticket stays open.

TESTED / HOW (scratch clone, hook as on develop 0b55401ad5dc, which equals b602c418296a for this file)
- `bash -n` rc 0. Suite at head: 4 passed, 0 failed. The 10 other pre-push hook suites at head: ks2127 12/0, ks884 10/0, ks998_judges 80/0, ks998_stale_base 21/0, base_fixture_guard 12/0, base_leg_comment 4/0, hook_base 36/0, current_develop 4/0, stack_legs_comment 4/0; `check_stack_safety_hook_env` 2 passed 3 failed, IDENTICAL on develop (it needs `Start_Up/` which my tree has... the failure text is `Start_Up/start-secuura.sh is missing`: an artefact of the scratch checkout, same on develop; not a PR finding). Shell-suite files on develop 101, with the PR 101 vs b602's 100 (+1).
- Seat's mutant reproduced with `HOOK_SH` on a scratch copy (final `exit 1` to `exit 0`, anchor found once): 3 passed, 1 failed, the failure is `a red preflight refuses the push`.
- My own mutants (each a copy in scratch, the tree's hook untouched, `cmp` rc 0 after): M2 `|| true; false || {` (refuse every push) reddens exactly `CONTROL a green preflight ...lands` (3/1); M3 text changed to `PREFLIGHT FAILED` reddens exactly `a red preflight is announced` (3/1); M4 `exit 1` to `exit 7` (still refuses) stays 4/0, correct (the cell pins refusal, not the code).
- Counts: suite 0 to 4 cells; hook leg-14 shell suites 124 to 125 per the seat's quote (not reproduced: the hook was not run).

NOT TESTED
- The real preflight or any real push through the hook; the other shell suites of leg 14; a mutant that makes the hook skip the preflight entirely (the CONTROL ran-cell would catch it by construction, not run).

Findings
- G306-2166-1 (Note): the cell "a red preflight refuses the push" detects refusal by whether the branch ref exists on the remote after the push; a hook regression that still exits 0 but is bypassed some other way is covered, a hook that exits non-zero for a different reason is also covered by the refuse cell yet the announce cell then reads the text; M4 shows exit code value is not pinned. Fine; noted only so nobody reads the suite as a pin of exit status.

---
## PR 2168 (KS-1922): GO WITH NOTES (tier 2 stands, no raise)

FOUND
- One product hunk (+3 -1) in the catch of `ExportService.processExport`: stored `exportResult.error` is now the constant `"Export failed"`; one new `logger.warn('Export failed', { error: <real message> })`; one new comment line. No auth, data, credential or deploy path. The body's claim (constant stored and returned; one log line added; unknown type no longer echoed) is exactly what I measured.
- Scope vs KS-1922: the ticket names line 160 of `exportService.ts` and the answer of `GET /api/analytics/exports/:id`. The PR changes that line and nothing else; routes untouched. The ticket's "check during the fix" neighbours (`dbSaveExport`, scheduledJobs) are not touched and the body says only the catch is in scope. No overclaim.
- BEFORE / AFTER, measured with a probe test (not in the PR) against the real `ExportService` with the DB, logger and metrics stubbed: thrown `Error('boom secret')`: before status failed, `error="boom secret"`, 1 failed DB write; after `error="Export failed"`, 1 failed DB write. Thrown string / null: before `"Unknown error"`, after `"Export failed"`. Unknown type: before `Unknown export type: <name>` (echoed), after the constant.

TESTED / HOW
- New file alone at head: 6 passed. Red-first (product put back to b602c418296a's bytes, test kept): `4 failed | 2 passed` = R1 R2 R3 R4 red, C1 C2 green. Reproduced.
- My own mutants (product restored byte-identical by `cmp` after each): M2 remove the `logger.warn` line reddens exactly R3; M3 log under `'Export failure'` reddens exactly R3; M4 stored text `'Export failed: ' + message` reddens R1, R2, R4 (3 failed); M5 log `{ error: 'x' }` reddens exactly R3.
- Whole analytics suite (vitest, `run`): develop 19 files / 117 passed / 0 failed (load1 7.57); head 20 / 123 / 0 failed (load1 7.67). One run each. The seat's develop red (`ks1868-...pool-error...`) did NOT recur for me; cause UNMEASURED.
- Callers of the stored `error` text, searched with `git grep` over the tree (hits for `analytics/exports` in 20 files, so the instrument works): the one UI reader is the issuer `ExportDialog.tsx` (lines ~300-302 render `Error: {exportResult.error}` for a failed export). The seat's body said this search was not made; made here.

NOT TESTED
- A real database or a real failed export; the routes; the Schemathesis effect (the analytics OpenAPI declares no error text for the record).

Findings
- G306-2168-1 (Minor): the added `logger.warn` is a new way for the catch to fail. `createExport` calls `this.processExport(...)` without awaiting or catching, so if the logger throws, the failed state is never saved. Measured with a stub logger that throws on `warn`: BASE saves the failed row (1 failed write, `error="boom"`); HEAD saves NOTHING (0 failed writes, in-memory `error` undefined, the DB row stays `processing`) and vitest reports an unhandled rejection. The repo's KS-1771 / KS-1868 lessons treat a hostile logger as a real class. Not pinned by any cell. Suggest setting the constant and saving first, or wrapping the log line. Does not block (a throwing logger is rare).
- G306-2168-2 (Minor, caller): the one reader of the text, the issuer Export dialog, will show `Error: Export failed` instead of the old message for every failed export. This is the intended effect of the ticket but is a user-visible change the body does not name (the body says readers were not searched). Nothing breaks.
- G306-2168-3 (Note): the real text now lives only in the server log; the persisted `svc_analytics_exports.error` column holds the constant, so a failed export can no longer be diagnosed from the record alone. Inherent in the ticket's ask.
- G306-2168-4 (Note): an Error whose `message` getter throws leaves the record `failed` with no error and no DB write, before AND after (measured identical); unchanged by this PR, still open.
- G306-2168-5 (Note): cell names carry `RED` permanently ("RED ks1922 R1 ...") though green after merge, the same cosmetic point as G305-2165-2; from a held patch not re-authored.

---
## PR 2167 (KS-1875 piece 2 of 3): GO WITH NOTES (tier 2 stands, no raise)

FOUND
- One product hunk (+7 -0) in `GET /api/metering/usage` of originate: `Array.isArray(req.query.from) || Array.isArray(req.query.to)` answers 400 `BAD_REQUEST` "from and to may each be given once" before the usage query. The check sits after the 401 user check, so an unauthenticated caller still gets 401. Read-only route; no insert/update/delete in the diff.
- Scope vs KS-1875: this is item 2 of the ticket's three ("a repeated from or to is silently ignored"). Nothing more is done.
- BEFORE / AFTER measured with a probe test (not in the PR; usage service stubbed, auth stubbed): `?from=2026-01-01&to=2026-02-01` 200 -> 200 (query called with both); `?from=A&from=A` 200 (bound open) -> 400, query not called; `?to=A&to=A` 200 -> 400; `?from[]=2026-01-01` (single-element array) 200 -> 400; `?from=&from=` 200 -> 400; `?from=A&from[x]=1` 200 -> 400; `?from[x]=2026-01-01` and `?to[x]=...` 200 -> 200, bound still OPEN (the disclosed residual, measured: unchanged); `?from=` 200 -> 200; `?from=2026-02-30` 200 -> 200 at the stub (the ticket's item 1; the real cast 500 is not exercisable here, UNMEASURED); `?from=2026-01-01,2026-01-02` 400 -> 400.
- Existing callers: a non-test search of the tree for `metering/usage` finds no caller in the repo's frontends or services; `systemTest` schemathesis tests send single `from`/`to` (`test_workflows_reporting.py`). Platform S (outside the repo, per the tenant-provisioning spec text) is UNMEASURED. Whether the gateway forwards a repeated parameter to originate unchanged (the ticket's "Not established") is still not established.

TESTED / HOW
- New file alone at head: 6 passed. Red-first (product = b602c418296a bytes, test kept): `3 failed | 3 passed` = R1 R2 R3 red; C1 C2 C3 green. Reproduced.
- My own mutants (restored by `cmp`): M1 check `from` only reddens exactly R2; M2 check `to` only reddens R1 and R3; M3 `&&` instead of `||` reddens R1 R2 R3; M4 status 422 instead of 400 reddens R1 R2 R3.
- Whole originate suite (jest): develop 220 suites / 2,592 passed / 0 failed (load1 7.81); head 221 / 2,598 / 0 failed (load1 7.76). Same counts the seat reports. The seat's note that the READY's 11 baseline reds did not reproduce also holds here (0 vs 0).
- Cells are pins (R green only with the change, C green both ways) and labelled as such.

NOT TESTED
- A real database, the gateway proxy, the `::timestamptz` 500, any real caller; `tsc` and eslint (carried from the seat).

Findings
- G306-2167-1 (Minor): `Blockchain/Dev/docs/METERING-USAGE-API.md` line 26 still states "a repeated `from` parameter is ignored and the call answers **200** with that bound open (KS-1875)". After this merges that sentence is false. The doc is not in the diff, no fragment pair is added, and `docs-fragments` does not cover this file. The ticket's own text says the doc records these as known deviations, so the doc line belongs to this piece or to the last piece; neither the body nor the comment names it.
- G306-2167-2 (Note, what the later pieces still owe): piece 1 (impossible dates such as `2026-02-30` / `2026-13-01` reach the cast and answer 500), piece 3 (no `/api/metering/usage` path in `secuura-api.yaml`), the bracketed `?from[x]=` residual (measured still open), the doc line above, and "does the gateway forward a repeated parameter". The body says piece 2 of 3, lists the first two as NOT in this PR and says the ticket stays open (`Refs`): confirmed. It does not list the doc line.
- G306-2167-3 (Note): the 400 also catches a single-element array (`?from[]=...`) and `?from=&from=`; these answered 200 with an open bound before. Same class, intended, not in the body's list of changed inputs.

---
## PR 2169 (KS-2015 piece 1 of 2): GO WITH NOTES (tier 2 stands, no raise); NO caller found that breaks

FOUND
- One product hunk (+5 -2) in `formatDate` of `routes/audit-export.ts`: the value must match `^\d{4}-\d{2}-\d{2}$` AND round-trip (`new Date(x).toISOString()` date part equals the input), else it throws and the route's existing catch answers 400 `Invalid date format. Use YYYY-MM-DD.` Auth and role checks (401/403) run before and are untouched. A LIVE admin API contract change, said in the body and the ticket comment.
- BEFORE / AFTER measured through the real router (stub admin user, stubbed security-service fetch; probe test not in the PR): `from=2026-09-01&to=2026-09-02` 200 -> 200; same day both (`2026-09-01`/`2026-09-01`) 200 -> 200; reversed range (from after to) 200 -> 200 (unchanged, not in scope); `0000-01-01`..`9999-12-31` 200 -> 200; a real leap day 2024-02-29 200 -> 200 (cell C3); `2026-09-01T00:00:00Z` 200 -> 400; `2026-1-01` 200 -> 400; `2026-02-29` (non-leap) and `2026-02-30` 200 -> 400; a trailing or leading space, trailing newline, or leading `+` on an otherwise plain date 200 -> 400; `from[]=2026-09-01` (single-element array) 200 -> 400; `2026-13-01`, empty, `from[x]=`, repeated `from`, a full-width digit 400 -> 400. A plain YYYY-MM-DD, the only shape the OpenAPI and the Stakeholder guide (`?from=2026-01-01&to=2026-02-15`) document, still answers 200.
- Q4 caller search, redone: `git grep -n 'admin/audit'` over the whole tree at the PR head returned 86 lines (control: the gateway's own `audit-export.ts`, `api-gateway.openapi.ts` and `index.ts:845 app.use('/api/admin/audit', authenticateToken(true), auditExportRouter)` hit, so the instrument works). The route mounts as `/export` under `admin/audit`; the admin frontend's export button (`frontend/admin/src/services/api.ts:939`) calls `/api/security/audit/export` with `format/action/resourceType` and NO from/to, handled by `admin.ts:1669`, a different route: CONFIRMED. The other hits are the audit-LOGS route (`/api/admin/audit-logs`, a substring match, different route), the gateway's own tests, the Schemathesis docs/baseline, the generated spec and doc text. The one real example of a call with dates is the Stakeholder guide's, which is plain YYYY-MM-DD. No frontend, other service, script or the Extranet sends a non-plain date to this route. Callers outside the repository: UNMEASURED.
- OpenAPI agrees with the new 400s: at the PR head `api-gateway.openapi.ts` lines 629-630 already declare `from` and `to` as required `z.string().regex(/^\d{4}-\d{2}-\d{2}$/)` and the operation declares `400: commonErrorResponses[400]`; the generated `docs/openapi/secuura-api.yaml` carries the same `pattern: ^\d{4}-\d{2}-\d{2}$`, `required: true`. So the route now matches the declared contract; before it was looser than the spec.

TESTED / HOW
- New file alone at head: 11 passed. Red-first (product = b602c418296a bytes, test kept): `8 failed | 3 passed` = R1 x6 (0, 1, -1, 2026-9-1, Sep 1 2026, the Z timestamp), R2, R3 red; C1 C2 C3 green. Reproduced.
- My own mutants (restored by `cmp`): M1 drop the round-trip clause reddens exactly R3 (1 failed); M3 invert the round-trip (`===`) reddens exactly C2 and C3 (2 failed); M2 drop the regex (leave the round-trip) stays 11/11 green (see G306-2169-3).
- Whole api-gateway suite (vitest): develop 168 files / 1,886 passed / 0 failed (load1 7.22); head 169 / 1,897 / 0 failed, three runs: load1 10.05 and 12.20 (over the line) and 7.79 (under); all three identical. Same counts the seat reports.
- Cells: R cells are red-first pins; C1 pins `20260901`/`x` (already 400), C2 and C3 pin that valid plain dates still answer 200. Honest.

NOT TESTED
- Callers outside the repo; the Schemathesis `positive_data_acceptance` / `negative_data_rejection` effect (predicted, not run); the security service behind the route (stubbed); a real stack; `tsc` (the seat's 25 errors are in other files; not re-run).

Findings
- G306-2169-1 (Minor): the body, the Linear comment and the ticket treat "the OpenAPI declaration (`api-gateway.openapi.ts` lines 629 and 630)" as the other piece of KS-2015, `NOT in this diff`. At the head those lines already declare the plain-date regex and a 400 response (and so does the generated yaml); there is nothing in the declaration left to change for this contract. Piece 2 of 2 is therefore undefined on the board; the ticket should say what remains (if anything), or the ticket can be closed by the board after merge.
- G306-2169-2 (Note, contract wording): the 400 message for `2026-02-30` / `2026-02-29` reads "Invalid date format. Use YYYY-MM-DD." though the shape is right and the day does not exist. Misleading for the one class of input the PR was written for; the status is correct.
- G306-2169-3 (Note): the regex clause is redundant: with the round-trip clause alone every non-canonical shape in the cells still answers 400 (mutant M2 stays 11/11), because the output is always the canonical date. Harmless; no cell can tell the two clauses apart, so a future edit that weakens the regex alone would go unseen.
- G306-2169-4 (Note, for the merge lane): live admin contract change. Anything sending an ISO timestamp, an un-padded date, a padded string or a bracketed array to `GET /api/admin/audit/export` will begin to get 400 after deploy; none was found in the repo. Callers outside the repo and the Schemathesis baseline (which already lists positive_data_acceptance failures on this route) are UNMEASURED. Worth a line in the deploy note; no caller found that breaks, so no NO GO.

---
## Declared limits of this gate
- No browser, no live stack, no container, no real database. The route behaviours above are the real routers with stubbed upstreams, in a scratch clone with a copy of the seat's node_modules (same dependency versions as the seat).
- The pre-push hook output in the bodies is the seat's quote, which I did not reproduce (the hook was not run).
- `tsc` and eslint not re-run (carried from the seat).
- Probes (BEFORE/AFTER tables) are my own test files in scratch, never in a PR.

## SPARK SHADOW
(see section appended below after the run; calibration rows in `calibration.md` in this folder)
