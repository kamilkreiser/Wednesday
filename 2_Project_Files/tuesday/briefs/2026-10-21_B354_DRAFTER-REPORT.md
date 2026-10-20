# B354 DRAFTER REPORT (read-only drafter, 2026-10-21, clock from `date`: 00:55:03 first, 00:56:48 last before the brief was written; a few later GETs carry no clock read)

Brief drafted: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B354_SEAT-G28_mps-gate-pr91-tier2.md` (tier 2, routing row G2, pane `Datasec/MPS-G28`, STATUS `…/1_Project_Definition/Briefs/2026-10-21_B354_STATUS.md`, port block 7810-7819, two stamp slots, each once). Nothing was run, built, fetched or pushed. Not created: the `.pre-stamp` copy (it is outside my two-file fence). **Tuesday must make it before stamping**, or the gate's control for the slot count (`.pre-stamp` reads 2) cannot fire.

## Reads (with line refs)
- `fleet/specs/model-routing.md` whole (154 lines): G2 at `:109`, G1 `:108`, G-cap `:111`, C2 pilot `:92`.
- Builder STATUS `…/Briefs/2026-10-20_B352_STATUS.md` whole (206 lines): numbers `:3,25-29,67-157`, EDITED EXISTING EXPECTATIONS `:159-162`, NEW WORDS `:164-166`, FOR TUESDAY `:177-185`, corrections `:192-199`, last line `:206`.
- Builder brief `…/briefs/2026-10-20_B352_SEAT-W20_…md` whole (178 lines): rulings R-W20-1..6 `:145-151`, items `:73-137`, residue `:108`, partition `:58-66`.
- ANSWER-1 `…/briefs/2026-10-20_B352_ANSWER-1_leave-flush-existing-pin.md` whole (9 lines).
- Gate shape: B348 brief whole (110 lines: refuse `:6-11`, stamp `:13`, launch `:15`, load `:39`, checks `:68-91`, verdict and severity floor `:93-96`, holds `:98-104`), B347 brief `:1-57` (shape; its model line `:13`), B348 STATUS whole (205 lines; verdict line `:1`, matrices `:61-81`, mutant table `:108-123`, findings, UNMEASURED), B347 STATUS not re-read (its content is carried in `CLARIFICATIONS.md:724-727`).
- Project `CLAUDE.md` whole (82 lines: CodeQL rule `:50-52`, quarantine `:58`). `CLARIFICATIONS.md:693-746` whole (landing = squash `:744`; words gate `:660`, `:688`; the no-tree-change-commit and conditional-CodeQL precedent `:726-727`) plus a grep of the file for squash/words gate/e2e.
- Live GETs under the project's `GH_CONFIG_DIR` (00:55-00:57): `ls-remote` (main, branch, `refs/pull/91/head`, `b354*`, `b35*`), `pulls/91` (state, draft, head, base, counts, mergeable, title, body), `pulls?state=open`, `pulls/91/files` with patches for `QuoteScreen.tsx`, `Toolbar.tsx`, `QuoteList.tsx`, `quoteListCsv.ts`, the autosave test, `b46-home.spec.ts`, `QuoteList.columns.test.tsx`, `pulls/91/commits`, `commits/<head>/check-runs`, `code-scanning/analyses` and `alerts` for `refs/pull/91/head`; contents at the head of `quoteListCsv.ts`, `web/e2e/b352-followups.spec.ts` (253 lines, whole), `tests/MpsCalc.Api.Tests/QuoteApiTests.V2StaffDiffer.cs` (49 lines, whole), `web/src/main.tsx`, `App.tsx`, `api/client.ts` (grep), `screens/QuoteScreen.tsx` (`:96-110`, `:226-270`), `format/decimal.ts` (grep), `components/Shell.tsx` (grep); contents at main of `src/MpsCalc.Api/Quotes/QuoteFigures.cs` (grep `:23-128`).
- Local: `lsof` (7800-7859 and unfiltered), a port grep over `tuesday/briefs/2026-10-*.md`, `ls .tools` (no `heavy-slot-*`, no `b354*`), `uptime`, `models_latest.json` key check.

## Premises, with sources
| premise | mark | source |
|---|---|---|
| head `5295ff7aec9518a5da2b25db56fff0d7c5f7c042` = branch = `refs/pull/91/head`; main `7bd7046a3b509507ae9190a7a8e039511e66fbb1` = PR base | MEASURED 00:55 | `ls-remote`; `pulls/91` |
| PR open, draft false, 6 commits, 12 files, +738/-8, mergeable true, state blocked; 1 open PR | MEASURED 00:55 | `pulls/91`, `pulls?state=open` |
| check-runs: CodeQL neutral; Analyze python, actions success; csharp, js-ts, web, dotnet, python in progress; 2 analyses, 0 open alerts | MEASURED ~00:55 | check-runs, code-scanning |
| 8 removed lines = 1+2+1+1+3 | MEASURED | `pulls/91/files` |
| ports 7800-7859 free; no brief names 78xx; control grep finds 77xx | MEASURED 00:56 | `lsof`, grep |
| load 4.31 5.24 7.24; no heavy slot dirs | MEASURED 00:55-56 | `uptime`, `ls` |
| `main.tsx:17` StrictMode; `App.tsx:20` key = quoteId + persona id + label; `client.ts:106-108` identity per request | MEASURED (GET at head) | contents |
| `autosaveWanted`, `stopped = halt === 'conflict' or halt === draft`, `autosave()` re-checks field errors | MEASURED | `QuoteScreen.tsx` regions |
| `termMonths` goes `count(String(...))`; `count` bare only when `isDecimalString` | MEASURED | `quoteListCsv.ts:36-39,48` |
| `Staff(...)` swap site | MEASURED (grep) | `QuoteFigures.cs:125-128` |
| PR title omits MPSCALC-311; body does not name it | MEASURED | `pulls/91` title and body |
| builder counts 1083/111 -> 1106/112, names lost 1 / added 24, spec 38 (base 30/8), dotnet 394/151/1797 -> 1799 | RELAYED | `B352_STATUS.md:25,131,148,152-153` |
| tickets 306 307 308 309 311 live Done-whens; -313, -314 | RELAYED | `B352_STATUS.md:33-56` (not re-read) |
| the `refs/pull/91/head` ref is advertised to the deploy key (unlike PR #89) | MEASURED | `ls-remote` |
| model id key present in `models_latest.json`; I did not write the id | MEASURED | python key check |

## Choices the brief makes (each one is a ruling Tuesday can reverse at the stamp)
1. **Stub mode with routed fixtures, no API at all** (your instruction). Consequence stated in the brief: the server's own 409/revision/price-audit refusal on the flush is covered only by B348's real-API matrix on the same `save()` plus the gate's routed answers. It is listed under NOT TESTED BY DESIGN and UNMEASURED.
2. **T-a is the sharpest probe I could find, and it is a hypothesis, not a finding.** `client.ts:106-108` awaits `identity()` per request; if that reads the current persona at send time, a persona switch inside the window sends the old persona's edit under the new persona's headers. The builder's proof is a jsdom fetch stub (`B352_STATUS.md:102`). I did NOT read `identity()` itself. The gate reads headers on the wire in Chrome.
3. **Real `beforeunload`** (the builder did not drive one): the gate uses `page.close({ runBeforeUnload: true })` and reads the `dialog`.
4. **Severity floor** as you wrote it, extended: Blocker = wrong quote, wrong identity, refused/409/empty-reason leave-save, bare CSV formula cell, any weakened existing test other than the ANSWER-1 one, any product `.cs`; Major = a lost edit in a covered route (named), second save, save on clean, console error after unmount, overflow, Action unreachable, b46-home or the new spec not green, dotnet test not red on either host; Minor = a new word, an unnamed residue loss, CodeQL pending, landing-text omission; Note = wording, hint sentence, discoverability, rental not covered. Residue cases (invalid, reason pending, stopped, save out, read-only) are Note when the STATUS names them (the builder's brief required it), Minor when not.
5. **Mutants:** the builder's 15 (m1, m3-m15 incl. m6b; m2 does not exist) plus own x1-x7, at least three required, in a priority order whose first four target the unproven spots: x1 stale leave closure, x2 flush ignores the price-reason guard, x3 Clone control removed and x4 panel warning removed (the MPSCALC-309 Done-when says "removed"; the builder's m12 and m14 are different mutations).
6. **dotnet cost control:** `dotnet test --list-tests` at base and head for the name multiset (compile only), the new filter executed alone, m15 + d1 + d2, and the full result read from the CI `dotnet` leg (full suite only if that leg is pending or failed).
7. **CodeQL pending:** poll up to 45 minutes, then a conditional verdict with the suffix on both the first and last line, never a bare GO (the B347 ANSWER-1 precedent, `CLARIFICATIONS.md:727`), unlike B348's brief which stopped. This follows your "pending = conditional verdict".
8. **Port block 7810-7819** (stub web on tip 7811, base 7812, merged 7813, mutants 7814; no API port).
9. **Last-line shas are sha7** (B348 precedent), main read by `ls-remote` at verdict.
10. **Extra stub-only regression specs** the gate may run: `v1b-frame` (shares `QuoteScreen`) and the b28/b30 stub tests (base-vs-head identical). `smoke.spec.ts` is never run.

## QUESTIONS (numbered; recommended answer first)
1. **Real API on a synthetic store (B348's "Path B"): in or out?** Recommend OUT, as written (you said stub, routed fixtures, no real store). The flush reuses `save()`, whose real-server behaviour (revision, 409, price audit) B348 measured with two tabs. Cost of IN: a dotnet build plus an API process per gate, and a second port family. If you want the on-wire flush against the real server, say so and I add an r9 Path B in a minute.
2. **Last-line shas: sha7 (as B348) or the full 40?** Recommend sha7.
3. **CodeQL still pending when the gate finishes: conditional suffix on both lines (as drafted), or `STOPPED: NEEDS TUESDAY` (B348's rule)?** Recommend the conditional suffix; it matches your instruction and B347's ANSWER-1, and a stopped gate wastes its heavy work.
4. **MPSCALC-308's Done-when says "the same for New quote". New quote now WAITS (disabled) instead of saving.** Recommend: the gate rules "met by a different mechanism", Minor, and the records seat's comment on -308 says so; no fix round. Alternative: you rule that New quote must flush (a different rule, FOR TUESDAY 7 of the builder).
5. **The PR title and body omit MPSCALC-311 and the two ticketless items (B347-8, B347-9) by key.** Recommend: a landing-text Note; Tuesday puts all keys in the squash message. Alternative: ask the records seat for tickets for B347-8/-9 before landing.
6. **Escalation:** the gate (Sonnet, G2) hands the PR to G1 on any security-shaped Blocker (the list is in the Stamp paragraph: wrong quote, wrong identity, refused/409/empty-reason leave-save, bare CSV cell). Recommend keep G2: autosave is not on the G1 list (security, destruction, deploy, client tester) and B348 gated the same mechanism at G2. Confirm.
7. **Mutant breadth:** 15 builder + at least 3 own is about 20 mutant runs, several of them Playwright (e2e) runs. Recommend keep it (B348 ran 12 plus 21 probes inside the same envelope); if the load stays above 8, let the gate drop the e2e variants of m11-m14 and x6-x7 to NOT TESTED in that order.
8. **The unscrolled Action column** (outside the panel box until the wrapper scrolls) is a discoverability Note with an owner question (heading-wrap, sticky Action, or leave). Recommend: the gate reports it as a Note and Tuesday asks the product owner only if the screenshot looks bad. Confirm.

## What I could not establish
- Whether `identity()` in `client.ts` reads the current persona at send time (T-a): I read only the `identity()` call site.
- Whether the Approver persona holds `internal-metrics` or sees 13 columns (`personas.ts` not read); the brief asks the gate to report what each persona gets rather than assume.
- The exact Persona select behaviour while a quote is dirty (the select exists: `Shell.tsx` and the builder spec use `getByLabel('Persona')`).
- Whether `QuoteScreen.flush.test.tsx` (281 lines), `quoteMock.ts` (88 lines) or `autosave.ts` have gaps: not read, deliberately, so the gate's probes stay independent.
- The live ticket text and any comment added by the records seat since 23:53 (the Done-whens in the brief are RELAYED from `B352_STATUS.md:47-51`; the gate re-reads them).
- Whether `playwright.config.ts` is safe with `MPSCALC_E2E_BASE_URL` set (RELAYED by B348 and B352; the gate re-reads it in r6).
- Whether Chrome fires the `beforeunload` dialog under Playwright for this page (needs user activation); the gate drives it and says what it saw.
- CodeQL and CI results: 5 jobs were still running at 00:55.
- I did not read the QA charter or `brief_seat.sh`; the launch line is carried from B348 with pane, path and level changed (the files exist: `ls` confirmed `brief_seat.sh`, `cockpit.sh`, the charter and `gitleaks`).
