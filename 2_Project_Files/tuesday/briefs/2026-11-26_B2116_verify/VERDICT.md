GATE B2116: GO WITH FINDINGS @ 184eff5 on main 15bca4e

Gate G2 (the stub is a dev double; the production build proves it absent), ROUND 1 OF 2 of lane L2 (kit B2111, seat M177;
stamp S5: Q3 the no-API leg skips with its reason and MPSCALC-135 stays open on clause 4's wording, Q5 the four stub answers,
Q10 G2; every choice the coordinator's). One Sonnet reader, in-session, read-only. Head `184eff58b9a099908e8e7a2535633629f3554b3e`
on `b2111/m177-mps-l2-e2e-smoke`, two commits, on main `15bca4ec3526cf609f50915221664c0231b5cc12` (PR 229). Read and measured
2026-11-26 10:02 to 10:10 AEDT (`date`) in `fleet/state/s329/g2116/`: clones `clone` (the head), `base` (main), `frozen` (main + the
kit's frozen script), `mutscratch` (scratch copy of `web`, never pushed); clone made by the project's deploy key in one process,
push URL `invalid://no-push`. Toolchain: node v24.22.2 / npm 11.19.1 from Tuesday's `tools/node-v24.22.2-darwin-arm64/bin`; dotnet
10.0.404 from the project's `.tools/dotnet-10.0.404`; `TZ=UTC`. Heavy jobs one at a time under `.tools/.heavy-lock-1` (four jobs;
two load1 reads 30 s apart, not 120 s as the kit says, and not independent: 3.10/3.60, 3.58/3.16, 4.70/5.09, all far under 24);
holders moved to `logs/`, lock folders absent at the end (count 0).

**AGREES WITH WHAT TUESDAY ENDORSED?** Yes on every number and every blob (below). One reading is narrower than endorsed: Tuesday's
Q3 reading is that the skip is "the honest result" where "nothing can answer it". The skip as written (F1) also fires when an API IS
behind the proxy and answers 502, 503 or 504; the gate measured it. That does not undo Q3 (the lane's own CI legs have no API) but the
"nothing can answer" sentence in the PR body and the records is only true as written for a proxy with no API; the landing texts say so
in the open list. No Blocker, no Major; it does not change the verdict.

## BLUF
The head is main plus the kit's frozen text, byte for byte (six blobs equal). The stub module prices nothing (every figure `'0'`,
every line `STUB`) and is absent from the production build (0 of 8 files; control: a stub build holds it in 1 file; bundle check
`markers found 0/57`). Stub rows 136 passed; all six mutants red on the named rows; whole vitest 1750 passed; legs A (default x3, 390
x1), B (default x3, 390 x1) green; C `1 skipped` with its reason. gitleaks clean (control rc 1 first); scans2111 295 added lines, every
control fired. No change reaches a production build, a customer word or a server path, so G1 is not needed. No Blocker, no Major,
four Minor, three Info. **None blocks landing.** The one condition on the landing: the first hosted Linux run of the smoke spec is the
pull request's own (UNMEASURED here); a red `web` job there is a STOP, not a retry.

## 1. THE DIFF AGAINST THE FROZEN TEXT (MEASURED)
- `apply_edits_l2.py`, `mutate_l2.py`, `scans2111.py` extracted from the kit by program (python blocks 0, 1 and 6 of the kit file).
  `apply_edits_l2.py` replayed once on a clone at main: created `heldRentalFlow.ts`, edited the other five (A1-A6, P1, T1-T2, S1-S4,
  C1-C2). Blobs after = the head's: smoke `1dc81da4`, playwright.config `02f7fec4`, heldRentalFlow `d0861e5f`, purchaseQuotes
  `0872d653`, stubApi.test `e0813e88`, stubApi `96acdba5`; each `cmp` equal to the head's file (6 of 6).
- `git diff --numstat 15bca4ec HEAD`: 20/5, 3/2, 89/0, 1/1, 141/2, 41/5 = the kit's; exactly 6 paths; no `.tmp-l2` file left.
  compare API (10:08): ahead 2, behind 0, 6 files; open pull requests 0; main = `15bca4ec`; head tree `3aaed431e80b0d346f3baa57bcb0224b6443674b`.
- Identity: `git log --format='%h %ae | %ce'` both commits `kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au`; one parent each.
  Commit messages equal the kit's subject + body (33 lines incl. two attribution lines); name scan 0 hits (control fired), no B-number, seat id or card id.
- Paths read by changed files (rule 8, tests that read the changed files): `src/test/pdftotextTimeout.test.ts` reads
  `playwright.config.ts`; the whole vitest run (below) includes it and is green. No CI job other than `web` reads a changed path.

## 2. WHAT I RE-RAN (MEASURED unless marked RELAYED)
| Claim | Instrument | Result |
|---|---|---|
| tsc, lint | `npx tsc -b`, `npm run lint` | rc 0, rc 0 |
| stub rows | `npx vitest run src/api/stub` | 1 file, `Tests  136 passed (136)` |
| whole vitest | `npx vitest run` | `Test Files  149 passed (149)`, `Tests  1750 passed (1750)` (the kit's) |
| mutants m1-m6 | `mutate_l2.py` on `mutscratch`, `npx vitest run src/api/stub/stubApi.test.ts`; control: clean copy 136 passed | m1 6 failed (the three permission rows of the held quote, `calculate at a stale revision`, `getQuote then returns the stored draft`, `the Seller may submit after calculating`); m2 1 failed (`submit with another calculation id`); m3 1 failed (`approve by the Approver`); m4 1 failed (`the proposal is a draft until`); m5 1 failed (`calculate at a stale revision`); m6 1 failed (`the proposal is a draft until`). Restored, `cmp` equal. All six = the kit |
| leg B (stub on, no API), web 59330, API origin default 5080 (nothing listening, checked) | `playwright test e2e/smoke.spec.ts --repeat-each=3`; `-c pw-390.config.ts` | 3 passed rc 0; 1 passed rc 0 (390) |
| leg C (stub off, no API) | same, no stub | `1 skipped` rc 0; reason "No API answers behind the proxy and the dev stub is off: the journey needs one or the other." |
| leg A (API on the synthetic store) | synth store built from the kit's two files: `devices 4`, sha256 `7c67faea...f76a` = the kit's; API built Release (0 warnings, 0 errors), started from its build folder on 127.0.0.1:59340 (pid 41130), web 59330 | default x3: 3 passed; 390 x1: 1 passed; API stopped by pid, 59340 and 59330 read free, no `MpsCalc.Api.dll` process |
| production build | `VITE_MPSCALC_AUTH=entra npm run build`; `check-bundle.mjs dist` | rc 0; `dist: 8 files, 1112909 bytes; markers found 0/57` |
| stub string absent | `grep -rl 'STUB: not priced' dist` | 0 files; control: `VITE_MPSCALC_API_STUB=1 vite build --outDir <scratch>` 1 file |
| gitleaks | `gitleaks dir` on a planted `ghp_` canary rc 1 first; `gitleaks git --log-opts=15bca4ec..184eff58` | rc 1 (control); rc 0, 2 commits, no leaks; the two messages as a file: rc 0 |
| scans2111 | `python3 -I scans2111.py base clone <6 paths>` | added lines 295; non-ASCII 0 (control 1); Cf 0 (control 1); GUID 0 (control 1); names 12 quiet, 12 controls fired; tabs 0; longest line 279 |
| CI modes (stub step 261/17, stub-off 162/1), A at 1440, `b46-home`, base-red table (A `:78`, B `:52`, C `:27`), `npm audit`, Linux | not run by me | **RELAYED** from the seat's STATUS (equal to the kit); hosted Linux UNMEASURED; `npm audit` NOT RUN by the seat or me (registry) |

Added-line scan by eye (rules): `test.skip(` 1 (the S2 line, `smoke.spec.ts:28`), no `.only`, no `eslint-disable`, no `waitForTimeout`,
no `@ts-ignore` in the diff (read whole); one `code as never` cast, in the module's `refusal` (typed against the contract; `tsc -b` rc 0).

## 3. ATTACK
**(a) Does the new answer change anything for an id the stub did not create, or a purchase draft?** No, as far as measured. Source: each
of `calculate`, `submit`, `approve` reads `createdQuotes()[id]` and falls to `real.*` when it is absent or `draft.quoteMode === 'purchase'`;
`getProposal` reaches the held rental module only for such a created, non-purchase id and otherwise takes the old expression unchanged.
Probe (scratch only, `GATE PROBE` block appended to a copy of `stubApi.test.ts` in `mutscratch`, never committed): a created PURCHASE
draft's calculate, submit and approve each reached the real API mock (3 calls, status 418 echoed) and its proposal is still the old
stub proposal (`STUB-PROPOSAL`, draft). The committed pass-through row covers calculate, submit and approve for an unknown id only. Changed
for a CREATED rental id: `getQuote` permissions (now by state and calculation), and `getProposal` (was `stubProposal`, now the held module).
Three shapes outside the tested property: (1) a created id whose draft is later edited to purchase mode (`updateDraft` hands such a draft to
the real API, so the stored quote stays rental: the stub then keeps answering calculate for it); (2) a quote created in a stub session and
the API brought up later in the same tab session (sessionStorage still holds it: the stub keeps answering, with zeros, for a real API that
could answer); (3) storage unavailable (`storeCreated` swallows the error: calculate then answers once and the next `getQuote` shows the quote
unchanged, so submit after calculate would be refused as stale). All three are dev-stub edges, none measured beyond the probe above.

**(b) Can the S2 skip hide a real failure where an API IS behind the proxy? YES (F1).** The probe is `GET /api/v1/quotes` and skips on 502,
503 or 504. I put a loopback server on the proxy origin (`MPSCALC_API_ORIGIN`, my port 59332, pid stopped, port read free) answering every
request 503: `1 skipped`, rc 0. The same with 500: `1 failed`, rc 1 (so only the three gateway codes hide). A live API that is up but
failing (a dependency down behind a 503) makes the hand-run leg A read as a skip. The stub-on test is also decided by page text
(`API STUB ON`), not by the environment, so a renamed banner makes the stub CI step skip smoke silently (the stub step would read
260 passed, 18 skipped, and no CI line asserts the count; the landing text tells Tuesday to read that count). The environment is available to
the spec (`process.env.VITE_MPSCALC_API_STUB`) and would be a firmer predicate. Three shapes outside the tested property: a live API
returning 502 from a failing upstream; the banner rendering after the Persona label (a race: the count would read 0 on a stub-on leg, the
proxy gives 502, and the journey is skipped; not seen in 3 of 3 runs at default and 1 at 390 on B); a 504 from a slow API (a timeout is a
real failure).

**(c) Can the S4 filter swallow a console error that is not the stub create's one 502? Yes, one, in stub mode only (F4).** The regex
`^Failed to load resource: the server responded with a status of #+ \(Bad Gateway\)$` (digits are masked to `#`) names no URL: it matches the
first 502 console message of any resource (regex checked: matches the 502 text, not the 503 text), is applied only when the banner is present,
removes every match but the assertion allows at most one. So a stub that no longer asks the API first (no create 502) would let one other
502 through unseen; and with a live API plus the stub on, a single 502 from any call is hidden. Nothing else in the console is swallowed
(other messages, a `pageerror` and a second 502 all fail the final `toEqual([])` or the `<= 1`). Three shapes: a 502 on a font or image
request; a 502 from a poll the page makes on its own; a page error text that happens to end in `(Bad Gateway)` masked the same way.

**(d) The seat's 'reject' finding: CONFIRMED (F3, Minor).** Probe: a held quote calculated, submitted by the Seller, then read as the Approver:
`permissions ["approve","reject"]`; `reject(id, 'why')` went to the real API mock once (with no API: 502). `client.ts:76-80` has `reject`,
`newVersion`, `getSnapshot`; the stub overrides none for a held quote. After Approved the permissions are empty (no button for the other two).
Dev stub only; the smoke journey never presses reject. Three shapes: reject by an Approver on a Submitted quote (measured); `newVersion`
on an Approved held quote (not offered, so unreachable by button; a direct call goes to the real API; DERIVED); the snapshot link of an
approved proposal (`approvedSnapshotId: 'snap_stub'` is not answerable by `getSnapshot`; the journey does not open it; DERIVED).

## 4. FINDINGS (graded; "blocks" = blocks landing)
| # | Grade | Blocks | Finding |
|---|---|---|---|
| F1 | Minor | no | The skip hides a live-but-failing API (502/503/504) and depends on banner text, not the environment (3(b)). Fix in a later lane: read `process.env.VITE_MPSCALC_API_STUB` and skip only when the probe reports no API AND stub off; count the stub step (261 passed). |
| F2 | Minor | no | The stub's `calculate` and `submit` check no role: an Approver persona calculated (`Succeeded`), an analyst persona submitted (`Submitted`) a held Draft; `approve` does check. The 8 rows do not cover it. Permissions hide the buttons; the answers do not refuse. Dev stub only. |
| F3 | Minor | no | The seat's 'reject' finding confirmed (3(d)). Records line. |
| F4 | Minor | no | The S4 console allowance admits one 502 from any resource (3(c)). |
| F5 | Info | no | The first hosted run of smoke is on Linux in two CI steps; the builder's local runs and mine are macOS. A red `web` job is a STOP. UNMEASURED. |
| F6 | Info | no | RELAYED from the seat: commit 1 was made after the mutants (the kit orders it before); one heavy job's first load read was 32.44 (over the gate of 24; my own four reads were all under 5); `npm audit` NOT RUN (the web job runs it; no package file changes). The blobs equal the frozen text, so none of these changes the diff. |
| F7 | Info | no | Test gaps: the pass-through row does not cover a created purchase draft (probe above: passes), `getProposal` for an unknown id, or the persona-less case. |

## 5. LANDING TEXTS (in this folder)
`landing.txt` (the form of B2107's: Tuesday opens the PR from the branch; nine distinct check names expected, read from PR 229's head
`b740f548` at 10:08: Analyze (actions), Analyze (csharp), Analyze (javascript-typescript), Analyze (python), CodeQL, dotnet, package,
python, web; code scanning read on the PR ref and on main after; SQUASH pinned to the head; nothing deploys: MPS hosted is a card per
deploy), `pr-title.txt`, `pr-body.md` (no person, card, seat or build id; the choices named as the coordinator's; clause 4 as Q3 reads it;
the named limits), `squash-subject.txt` (ends `(#PRNUM)`; scanned with #230), `squash-body.txt`, `FOR-RECORDS.md` (135 and 297
readings, the FACT 7 lines, the four findings, and MPSCALC-195's drop of 09:14 for Tuesday's records kit). Texts scanned: gitleaks
rc 0 (control rc 1), the twelve-name underscore-aware scan quiet (control fired), no B-number, seat id or card id.

## 6. NOT RUN
CI-mode runs (stub step, stub-off step), A at 1440, `b46-home.spec.ts`, base-red legs, `npm audit`, hosted Linux; the review of
`ci.yml` was reading only. No pull request, push, merge, comment, Jira call, hosted request or Azure call was made.

## 7. RESIDUE
Processes I started: the synthetic-store API (pid 41130, stopped by pid), a fake loopback API (two runs, stopped by pid), Vite servers
started and ended by Playwright. At the end: ports 59330 to 59340 listening 0; `.tools/.heavy-lock-*` count 0; no `MpsCalc.Api.dll`
process. Nothing deleted (one stray `sed -i` backup of my own text was moved to `g2116/_quarantine/`). The project checkout was not written
except the two heavy-lock folders the kit names (created and removed by `mkdir`/`rmdir`, holders moved to my `logs/`).
