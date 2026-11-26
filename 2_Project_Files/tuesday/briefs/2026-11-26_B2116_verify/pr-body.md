Two commits on `main` `15bca4ec` (behind 0, ahead 2): `a596c626`, the dev stub, then `184eff58`, the two spec paths. Six
paths, 295 lines added and 15 removed: `web/src/api/stub/heldRentalFlow.ts` (new), `web/src/api/stub/stubApi.ts`,
`web/src/api/stub/purchaseQuotes.ts` (one comment), `web/src/api/stub/stubApi.test.ts`, `web/e2e/smoke.spec.ts` and
`web/playwright.config.ts`. No package, no lock file, no workflow, no setting, no contract member, no screen, no document.

## Why

- **MPSCALC-135.** The smoke journey (create, five lines over two sites, calculate, submit, approve, proposal) was left
  out of CI because, with the dev stub on, calculate went to a real API that was not there (502), and with no API the
  New quote dialog stayed. It was also red against an API on a synthetic store since the short proposal was capped at
  three device lines (MPSCALC-110): the spec still counted five rows, and nothing noticed because CI never ran it.
- **MPSCALC-297.** The exact-nav spec needs no edit (it is green at 1440 and 390 px in stub mode and skips itself with
  the stub off, by its own rule); the smoke spec has to be green at desktop and phone width.

## What changed

- **The stub answers the journey of a rental quote it created itself.** A new module, `heldRentalFlow.ts`, answers
  calculate, submit, approve and the proposal, in the manner of the purchase stub's own "not priced" answer: nothing is
  priced (every figure is zero, every line is marked `STUB`, one Info issue says so). A quote moves Draft, Submitted,
  Approved by the caller's role, and the proposal is a draft until Approved. A purchase draft, and an id the stub did not
  create, go on to the real API exactly as before. Eight new rows pin it; three comments that said calculate still goes
  to the real API are corrected.
- **The smoke spec.** The proposal's first table reads 4 rows (three device lines and the pointer row; the cap is not
  imported because that module reaches a stylesheet Playwright cannot load). With the stub on, the one console message
  of the stub's create (a refused proxy request) is allowed once, as `bom.spec.ts` already allows it. With the stub
  off and no API behind the proxy the test skips itself, with its reason, because nothing can answer the journey.
- **The config.** The smoke entry leaves the list of specs CI leaves out (its reason was half stale) and joins the specs
  of both modes: it runs in the dev stub step and skips in the stub-off step. `ci.yml` is unchanged.
- **No word a customer reads changes.** One new string exists, a dev-stub Info issue ("STUB: not priced ..."); a
  production build (`VITE_MPSCALC_AUTH=entra`) holds it in 0 files, and a build with the stub on holds it in 1.

## Choices (the coordinator's, as coordinator; none is the product owner's)

- The stub answers four things (calculate, submit, approve, the proposal), not calculate alone, because the journey
  needs all four.
- With no API and no stub the spec skips with its reason rather than failing or being left out of that step. **Clause 4
  of MPSCALC-135 ("green in all four legs") is read as: green where an API or the stub can answer the journey, and
  skipped with its reason where neither can.** The ticket stays open for the product owner's reading of its own
  wording.
- The journey against an API on a synthetic store stays a hand-run leg; there is no third CI step.
- The literal 4, with the cap named in a comment; the screen's cap is not changed.
- The stub's new string is not put to the product owner (a dev double's text, in no production build).

## What proves it

- The new rows: against the unchanged stub 7 of the 8 fail (the eighth guards the pass-through on purpose); with the
  change `src/api/stub` reads 136 passed, the whole `vitest` run 149 files and 1750 tests, `tsc -b` and `eslint` rc 0.
- Six planted mutants of the module (submit without a current calculation, submit ignoring the calculation id, approve
  ignoring the role, a proposal always a draft, calculate ignoring the revision, a proposal of one line) each turn the
  named rows red.
- The journey: against an API on a synthetic store, green at the default width, 1440 and 390 px; with the stub on and
  no API, green at the default width and 390 px; with neither, 1 skipped with its reason. The two CI modes, as the
  builder ran them locally (the review did not repeat them): the stub step 261 passed and 17 skipped, the stub-off step
  162 passed and 1 skipped (one gained pass, one gained skip).
- The production build and its bundle check: `markers found 0/57`.
- An independent review re-ran the stub rows, the mutants, the three no-hosted legs, the production build and the
  string check in its own clone, with the same figures; secret scan (planted control first): no leaks in the six paths
  or the commit messages.

## Still open (records, not this change)

- The first hosted run of the smoke spec is this pull request's own, in both Playwright steps on Linux; a red there is
  read, never skipped.
- In stub mode the stub answers an Approver's `reject` as offered but has no reject (it goes to the real API); the stub's
  calculate and submit do not check the caller's role; the stub-off skip also covers a live API that answers 502, 503
  or 504; the console allowance admits one 502 message from any resource. Each is a dev double's fidelity, none reaches a
  production build.
- Two stub fidelity follow-ups of an earlier landing, and `npm audit` (not run by the builder: it calls the registry),
  which the web job runs.

Who decides: the coordinator lands this change; nothing is deployed and no hosted site changes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
