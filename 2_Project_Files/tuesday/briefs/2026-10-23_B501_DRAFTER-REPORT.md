# B501 drafter report (read-only; two files written)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B501_SEAT-T1_hpsmpoc-telemetry-smaller.md` (121 lines). Cloned in shape from B493 (read whole) with the B496 Api-suite rule and `apiq.sh`.

## What the design note says (5 lines)
1. Turn the automatic recorder off; each app writes one small record of its own.
2. Three fixed events only: `request`, `error`, `call`.
3. Fields are numbers or values from fixed lists in code: route template (else `unmatched`), method (else `OTHER`), status, duration, outcome, a server-generated reference id; `call` target is `api`/`sql`/`agent`. No free text, no value from a request, customer, model or library.
4. The record is built once, as a new read-only object, at response finish; OpenTelemetry spans are never read.
5. Seven proof tests (field type, late write, odd method/tag, no recorder, exact payload with a stock control, README, mutation). Keep: start-up guard, outbound switches, Entra sign-in, corpus, capture transport/canary harness. Discard: all clean-up layers. Option A (build) is what the product owner tapped.

## Findings that ended the earlier lane, and the rule that closes each (the table is in the brief; R-numbers are my grouping of the note)
- R1 closed record (no free-text field, no host name): B431-1/-2 (frames carry values), B431-7 and B436-4 (log template), B436-1/-2 (runtime-built frame/type names), B447-1 (`error.type`), B447-2 (span event name), B447-3 (log category), B431-9 (host name), B471-7.
- R2 template-or-constant (route, method, call target): B471-2 (web names a call by `http.method`), B471-3 (API names a span by a tag value), B447-4, B447-6, B471-9.
- R3 build once at response finish, never read spans: B471-1 (the decisive Blocker, write after span end), and B447-1/-2 via that path.
- R4 no automatic recorder: B471-2/-3 (Next fetch instrumentation, `Azure.*` sources), B447-4, B431-4 (unstated outbound).
- R5 exact-membership checks plus mutation test: B471-5, B447-10/-11, B436-6.
- R6 README equals the type: B431-5, B436-5, B447-5, B471-4.
- R7 keep the guard/outbound pieces that passed: B431-3, B436-3, B447-9 (start-up must not stop the app or print the value).

## Model and tier
Builder: Opus (`claude-opus-5-5`), routing row C3 (build on a data-handling design surface; Sonnet is "no" there). Gate: tier 1 (row G1), because the record leaves the box to Azure Monitor and the design is about what may leave; a NO GO ends it (the note's option A rule). The brief states this on the model line.

## Assumptions and things Tuesday should decide at the stamp
- **Dependencies:** the note names NO package, and main has no telemetry or Azure Monitor package (MEASURED). Sending with Entra sign-in almost certainly needs one. I made the default "zero new packages", added a stamp slot "Dependency ruling" and told the seat to STOP with its transport proposal before any `dotnet add`/`npm install` if the ruling is `none`. b429's package list is given for reference only. `web/package.json` must keep `next` 16.4.2 (b429 holds 16.3.8; do not copy its file).
- **Existing request log:** main already has `app.UseRequestTimingLog()` (Program.cs:116); the brief makes PRIOR WORK read it (it may overlap or log request values).
- **Scope calls I made:** `request` and `error` rows on both apps; `call` row for the web-to-API call required; API `sql`/`agent` rows only where one existing choke point sits inside `HpsmPoc.Api`, else Deferred. Reference id on screen and any response header are NOT built (customer-facing surface, a question for Tuesday). A$10/month stop line and the 900-line product-code guard are mine (carried from the earlier lane / reading of "few hundred lines").
- Minimal additive edits allowed to `web/src/server/bff.ts` (the only place a web-to-API `call` can be timed) and `web/src/instrumentation.ts`; no `gitleaks.ignore` edits.
- `BRIEF_SEAT_LEVEL=opus` in the launch line is my reading of B493's `sonnet` form; Tuesday confirms the spelling.
- Main read `486e74e6d433662649cb09aee7112f434722feb1` and b429 head `4c02e8b9...` at 07:2x; 0 open PRs; cockpit name `Datasec/HPSM-POC-T1` free (live: D29 and one other client's seat); ports 8490-8499 free; `.tools/b501` absent; no `b501*` ref. b496 (next advisory bump) touches `web/package*.json`, flagged for overlap.
- Jira HPSMPOC-224: Backlog, two outcome comments (read only, key not printed). Nothing run: no build, test, fetch, worktree.

## Stamp-slot lines (Tuesday fills; the unstamped brief counts 9 lines with the four-underscore pattern, verified)
1. Stamp time
2. Stamped by (the Tuesday seat that READ this brief whole)
3. Launch authority (who, under which grant)
4. Hard stop and target READY (suggested 11:00 / 12:00 AEDT)
5. Main at launch (ls-remote, with time)
6. Jira HPSMPOC-224 state at launch
7. Dependency ruling (`none` or exact ids/versions per app)
8. Model receipt line and load1 at launch
9. Last line: `READ-WHOLE-BY-TUESDAY: ` followed by the four-underscore slot
