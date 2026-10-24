# B615 DRAFTER-REPORT (Composer C-API, SEAT-J6), drafted 2026-10-25 01:2x-01:4x AEDT

## BLUF
Brief written, 120 lines, 9 stamp-slot lines (counted with the split pattern), startable tonight. Project folder confirmed: `Datasec Security Composer` (STATUS convention confirmed from B587/B593: `1_Project_Definition/Briefs/<date>_<B>_STATUS.md`, evidence beside it in `<date>_<B>_evidence/runs/`). Main `e019ac3abf628cbb6a50eb871b8f65b86a58ff6e` (ls-remote 01:30). Both items are in: I1 = B593-2, I2 = B593-3. The B593-2 fix mechanism is NOT measured (it depends on how the installed `@fastify/ajv-compiler` lets a custom `date` format win over the default one), so the brief states the constraints and makes the builder measure it.

## D-list (decisions for Tuesday at stamp)
- D1. Test file name: I kept `b593-year-zero-date.db.test.ts` (the finding id; the lane's intersection program ran on that name; the repo's `b587-*` files set the precedent that a B-number in a file name is accepted). Alternative: `b615-...`. Recommend: keep as written.
- D2. Hard stop/target: suggested target READY +3 h, hard stop +5 h from launch (the work is small; the db stack and one `ci:node` dominate). Recommend: accept; slot is yours.
- D3. Both Composer seats can start a database stack at the same time (separate seat-local locks by path, as you asked). Load rule is the only throttle (load1 below 7, two reads). Recommend: stagger the two launches by about 10 minutes, or accept the load-based self-throttle.
- D4. Image build: the brief has J6 build its own `pc-b615-node` image (`npm ci` must be a cache hit, else STOP). If J7 builds at the same time the machine pays two builds. Recommend: accept.
- D5. Kit source: copies `.tools/b593/{common,dbtest,groups,heavy}.sh` (the gate's kit, proven at this tree) with `b593` renamed to `b615` by program and a `cmp`. The B593 gate brief forbade the gate from using the builder's kit, but nothing forbids the reverse. Recommend: accept; confirm no G84 process is alive (no pane at 01:28).
- D6. I1 mutants: 5 (M615-1..5) plus one for I2 (M615-6); I2's red proof is on a mutant (the live `not.toBe` rows are green at main by design). Recommend: accept.
- D7. The builder's reading of "SAME answer as 2027-02-30": the existing 400 INVALID_REQUEST path through the Fastify validation branch; if the only way to get it is a new sentence, I1 STOPS. Recommend: accept.
- D8. Gate after: tier 1 as you said (it touches the validator every route shares). Recommend: accept; a tier-2 gate would also be defensible for a 3-path diff, but the validator is shared.
- D9. Launch queue: after J7's brief is stamped, or independently? No file conflict between the two (J7: `packages/db/**`, `DEPLOY.md`), only the shared `.git` and STATUS directory, which the brief handles.

## Facts in the brief, with instrument
- Main sha `e019ac3a...`, open PRs #85 (draft, 57 files) and #86 (2 files): `ls-remote` and `gh api -X GET pulls?state=open`, 01:30. Shared with my three paths: 0 and 0 (`grep -c -x -F -f`); control, a planted `apps/api/src/app.ts` in #85's list: 1; #85 has 4 `apps/api` files (non-empty).
- No `refs/heads/b6*` on origin at 01:30 (ls-remote with the pattern printed no b6 ref; control: the same call listed b5/b4 branches and the b587 branch).
- Ports 9650-9659: `lsof -nP -iTCP:9640-9669 -sTCP:LISTEN` printed nothing at 01:2x/01:30 (no positive control run; the builder runs one). Panes at 01:28: `tuesday`, `Datasec/NexusAI-G92`, `fleet-monitor` (no Composer pane yet).
- Counts printed by `grep -c -F` on the raw files fetched at the main sha: `app.ts` `customOptions: {` 1, `coerceTypes: false,` 1; `document.ts` the `date` const line 1, `CONTRACT_VERSION = "0.37.0"` 1; `openapi.test.ts` `it("pins the version", () => {` 4, the three tautology asserts 1 each, the live `toBe("0.37.0")` 1, the two stale comment phrases 1 each; `inputs.ts` `$6::date` 1; control `zzz-no-such-string-7f3a` printed 0.
- Row/comment line numbers at main: rows `:3323`, `:3429`, `:3575`, live `:3705`; stale comments `:3324`, `:3430` (the gate's `:3325/:3431/:3577` were at the PR head, so they differ by 2 and 2 and 2; the brief says so). `withoutB587T1/T2/T3` `:447/:472/:492`, set the version at `:455/:478/:503`, bases built `:522-532`.
- Body date fields (from `document.ts` at main, line-to-schema mapping by awk): EngagementCreate/Patch/Guided/CloneCreate `due_date`, FrameworksPut `effective_date`, ExceptionCreate `review_date` and `expiry_date`, EngagementGovernancePut x3. The brief tells the builder to re-derive by program. Only one literal `format: "date"` exists (`document.ts:191`).
- Validator: `app.ts:125` `ajv: {` with `customOptions`; Fastify `^5.12.5`; `apps/api/package.json` has no `ajv`; error handler maps `err.validation` to 400 INVALID_REQUEST (read from raw `app.ts`).
- Test glob: `apps/api/vitest.db.config.ts` includes `apps/api/test/**/*.db.test.ts`.
- C-DATES table (2027-02-30 etc. answer 400; 0000-01-01 answers 500): RELAYED from the gate file lines 320-335, not re-run.
- Baseline counts (db 32/400, API db 79/1410, contract 164, unit 311/3103+1): RELAYED from the B593 gate brief.
- Harness shape (`createHarness`, `h.call`, `problem(res, status, code)`, `createEngagement`): read from raw `harness.ts`, `flows.ts` and the B587 governance db test.
- No Jira ticket for these findings: RELAYED from the sweep file (PCOMP search for "B593" returned 0). I did not query Jira again; the brief says nothing is written there.

## UNMEASURED
Which mechanism makes a stricter `date` format win in the installed `@fastify/ajv-compiler` (customOptions.formats vs plugin order); whether the harness response contract check shares the same ajv; whether every body date field's operation is reachable through `flows.ts` fixtures; `npm ci` cache; b593 wrapper still runs at this base; whether a shared git-ref lock exists in the project (not found in the briefs read); whether a BACKLOG row covers year-zero dates; no test of `2027-02-30` exists under `apps/api/test` (the one code search I ran hit only three `apps/web` files, and GitHub code search can lag); the J7 brief's B-number and branch name (the brief names J7 by seat tag and by "any b6xx other than 15"); no CLARIFICATIONS grep was run by me for "year" (the builder's PRIOR-WORK CHECK does it).

## Not startable
Nothing in this lane. Not taken, as instructed: B593-1, -4, -5 (words/rulings), B593-9/-10 (J7). A note for the record: if the fix turns out to need a package or a contract text change, I1 stops and I2 still lands.

## Notes
- Local clone lacks object `e019ac3a`; the drafter used raw `gh api` content. Rule 2 tells the builder one fetch brings it.
- One advisory from the grep-case hook appeared on multi-word greps; counts that matter were printed with `grep -c -F` plus a zero control.
