STARTABLE: YES (after the stamp; 7 questions below, each with a default the kit already assumes)

# B1582 drafter report: MPS Commercial Calculator, lane M-W1, slice 2 (seat M141)

Drafted 2026-11-15 15:52 to about 16:08 AEDT (`date` printed 15:52:24, 15:52:58, 15:53:15, 15:56:31, 15:56:43, 15:57:10, 16:00:49, 16:01:08, 16:04:54, 16:06:34). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1582_SEAT-M141_mps-lane-mw1-pdf-text-specs-in-ci.md` (87 lines, 12 stamp slots left as `____`) with sidecar `.measured` (109 lines: 94 claims plus F01 to F15). `stamp_check.py <kit>` rc 0 (94 claims, 94 measured).

## BLUF
- **Of the four keys commissioned (135, 297, 251, 57), only MPSCALC-57 is buildable, and only its clause 3: the four PDF-text browser specs (itemised-summaries, proposal-buttons, proposal-purchase, rental-book) go into CI.** Part A: each spec reads the PDF from a temporary file it makes with `mkdtempSync`, not from standard input (the fix comment 41141 suggests for the intermittent hang). Part B: the four move from `LEFT_OUT` to `STUB_OFF_ONLY` in `web/playwright.config.ts`, and `ci.yml` gets one inline step that installs `poppler-utils` before the stub-off e2e step. Six paths, two commits, one Sonnet seat (row C2), G2 gate. No product byte, no new word, no new package, no new action.
- **135, 297 and 251 are LEFT.** 135: with the stub on, Save of a created rental quote now works (landed with #193), but calculate still goes to the real API (502). Making the stub answer it means the stub prices something, which is a design nobody has approved. With the stub off and no API, a quote cannot be created at all. 297 waits on 135. 251 needs an Entra sign-in leg, which no seat can make. Q5 asks what happens to 135 next.
- **I proved the CI step text against the three python rows that read `ci.yml`.** In a scratch copy of main with the step added, all three exit 0. Control: swapping `command -v pdftotext` for `bash tools/get-poppler.sh` makes `test_sdk_pin_routes.py` exit 1 with the closed-script-list message. That makes rule 8 concrete: the gate has to run those three rows as well as the web job.
- **The pin that constrains the edit:** `web/src/test/pdftotextTimeout.test.ts` (not in this lane) needs exactly one `execFileSync('pdftotext', ...)` per spec, with an options object holding a literal `timeout` and `killSignal`. So the fix stays inside each spec, with no shared helper, and the pin stays unedited and green. The header of that pin (line 4) says "CI runs no Playwright", which has been stale since #178 (Q7).
- Seat `M141`, pane `Datasec/MPS-M141`, branch `b1582/mps-lane-mw1-pdf-text-specs-in-ci`, ports 9970-9979 (web server on 9971). Node is HPSM-POC's drive-local node 24, read-only, as in B1578's stamp. Load was 24.33 at 15:56 and both heavy slots were held (M139 since 14:15:51, M140 since 15:56:18), so the seat will queue.

## Scope, key by key (each ticket and all its comments read whole by Jira GET at 15:53, own GET-only helper `d1582/jget.py`)
| key | status | in slice? | reason (newest comment) |
|---|---|---|---|
| 57 | Backlog | **IN, clause 3 only** | 41141: the four PDF-text specs are outside CI because the runner's `pdftotext` is unmeasured, and the review saw about 1 run in 25 hang on stdin and suggested a temporary file. Clauses 1, 2, 4 and 5 of 40621 are "not re-derived" and are the records seat's to read. |
| 135 | Backlog | LEFT | 41135: the stub and no-API legs are NOT MET. Calculate in the stub is a pricing design (`stubApi.ts:338` comment, re-printed at main). The no-API leg cannot create a quote. A product-owner question (Q5). |
| 297 | Backlog | LEFT | 41139: clause 2 is smoke at both widths in CI; it is blocked by 135. |
| 251 | Backlog | LEFT | 41138: clause 1 needs the visits "after sign-in" (Entra), which is ruled out for the stub step and needs a hosted identity. |
Since #178 no PR names any of the four (194 PRs read, controls #72, #181 and #194 present). None of the four is `ALREADY-ON-MAIN`: the four calls still pass `input: pdf` (1 each), `LEFT_OUT` still holds 7 entries, and `ci.yml` names poppler 0 times. Jira control: `MPSCALC-361` reads Done.

## Facts re-measured with instruments (details in the sidecar, tags F01 to F15)
- Main `3a69065a6e35ed5b5f9ee76ea8f3648f60ee13cc` at 15:52:58; open PRs 0; `heads/b1582` 0 rows (control `heads/b1564` 1 row) [F01].
- **Main's `web/` tree equals the tree gate B1566 tested** (`8583c7af...` at both `a4cc7ff8` and `3a69065a`; control `ccc41367` reads `afd91143`) [F02]. That gate's counts (1575 vitest; `--list` stub 270/18 and api-off 117/4; its bundle line) are therefore RELAYED for this base, and the seat re-measures them.
- Hosted CI on main: 8 of 8 success, including `Analyze (actions)`, so CodeQL reads `ci.yml`. In the web job, the stub e2e step took about 8.9 min and the api-off step about 4.2 min (gate B1566's local runs: 4.2 and 2.5 min); the whole job took about 18.4 min of its 40 [F03].
- Rule 8 census: the only readers of `ci.yml` among the tests are `scripts/tests/test_ci_workflow.py`, `test_sdk_pin.py` and `test_sdk_pin_routes.py` (all exit 0 at main by `python3 -I -B`) [F10]. No test under `scripts infra tools tests src` reads `web/e2e` or `playwright` (0 files; control: `ci\.yml` 5 files) [F12]. `test_ci_workflow.py` red rows replace the literal line `      - run: npm ci` (count 1 in `ci.yml`), so the kit keeps that line exactly once.
- Toolchain: no MPS drive-local node; HPSM-POC `node24/bin` prints v24.21.0 and npm 11.19.0; `pdftotext` 26.11.0 at `/opt/homebrew/bin` (rc 0 on `-v`); Chrome present; dotnet not needed [F13].
- Mutant basis, measured: `pdftotext` on an empty stdin prints "Syntax Error: Document stream is empty" with rc 1 (this is mA1). A Node `execFileSync` timeout prints "spawnSync <cmd> ETIMEDOUT" with signal SIGKILL; this is the hang-count pattern.
- Ports: `lsof` 9970-9979 printed 0 listeners (unfiltered 24); the 28 non-`.pre-` SEAT kits of 14-15 Nov hold 0 `997x` (control: `993x` 8 hits in B1578) [F14]. CodeQL CLI and the javascript and actions code-scanning suites were found by `find`; I did not invoke them [F15].
- Partition, both sides: B1578's lane table (line 62) names `web/e2e/**` and `.github/**` NOT its own; B1573's (line 52) names `web/**` and `.github/**` NOT its own; M138 writes no repo file. None grants any of the six paths.

## Census: what reads or pins the six paths (frame: main `3a69065a`, by program)
- `web/src/test/pdftotextTimeout.test.ts`: reads all `e2e/*.spec.ts` and the config's `timeout`. **UNAFFECTED if the kit's shape is kept** (DERIVED from its scanner, lines 41-70; the seat proves it by running it unedited). Mutant mA2 makes it fire.
- `web/tsconfig.node.json` and `web/e2e/b83-feedback-attachments.spec.ts` name `playwright.config`. b83 stays in `LEFT_OUT`, so UNAFFECTED.
- The three python rows: UNAFFECTED, measured on the planted copy (rc 0, 0, 0), with a control that fires.
- `README.md:15`, `scripts/package.sh:8` and `scripts/deploy-from-ci.sh:50` name `ci.yml` in prose or as a workflow name: UNAFFECTED. One note: `deploy-from-ci.sh` needs a green main run, so a flaky new step would block a deploy package (Q3).

## Chain inputs (rule 4), in execution order
| step | inputs | produced by / exists at |
|---|---|---|
| 0 | the kit, the STATUS path | exists at launch / this step |
| 1 setup + baseline | `2_Project_Files` and its identity, deploy key, HPSM-POC node24 (read-only), `~/.npm`, Chrome, `pdftotext`, lock protocol | BASE and the machine (each printed present above) |
| 1 per-file `--list` counts | `node_modules` | `npm ci` earlier in step 1 |
| 2 Part A | the four specs, `predictions.txt`, the pin | BASE; the predictions file is written before the first run |
| 2e hang count at head | the Part A commit | step 2 |
| 3 Part B | Part A pushed; the config; `ci.yml`; the per-file counts | step 2; BASE; step 1 |
| 3c python controls | scratch copies of `ci.yml` and `scripts/tests` | step 3 (the seat makes them outside the clone) |
| 4 CHECKS + CodeQL | baseline counts, both e2e steps, bundle line | steps 1 to 3 |
| 5-6 properties and push | each part's diff, the gitleaks canary, the SARIF | steps 2 to 4 |

## D-decisions the drafter took
- D1: the slice is 57 clause 3 only; 135, 297 and 251 are LEFT with their reasons. D2: the four specs go into `STUB_OFF_ONLY`, not `BOTH_MODES` (they skip with the stub on, so the stub list stays unchanged; mB2 guards this). D3: the temp-file fix stays inside each spec because the pin's census forbids a shared helper; `mkdtempSync` is used because of CodeQL `js/insecure-temporary-file`. D4: one inline `run: |` step with no `.sh` script, because `CI_SCRIPTS` is a closed list. The exact text was measured against the three rows. D5: two commits (the fix first, then CI inclusion), so the CI change never lands without the fix. D6: the 1-in-25 hang cannot be proved red-first. The kit asks for `--repeat-each=5` counts at base and head as evidence only; a timeout at head is a STOP.

## QUESTIONS FOR TUESDAY (each with a default)
1. **Slice = MPSCALC-57 clause 3 only.** Default: yes; 135, 297 and 251 are LEFT.
2. **Node.** Default: HPSM-POC `.tools/node24/bin`, read-only, first on PATH (the B1578 stamp's precedent). The alternative is the machine node v26.13.0 with a CI-24 note.
3. **`apt-get` on the runner.** Every PR and main run gains a network install from the Ubuntu mirrors. A mirror flake would turn CI red, and `deploy-from-ci.sh` needs a green main run. Default: build it as written; hosted CI on the PR is its proof.
4. **Linux poppler differs from the Mac's 26.11.0** (`-layout` text can differ). The first Linux run of the four specs is hosted CI on the PR. Default: a red only there is a fix round for this seat (round 1 of 2), not a new kit.
5. **What next for 135?** Default: Tuesday puts a card to the product owner. Either the stub answers calculate with a marked synthetic figure (a design), or the four-legs clause is re-scoped to the legs that can exist. No seat builds until then; 297 follows.
6. **Gate tier.** Default G2 (`model-routing.md:109`: tests and CI). The gate runs every web step and, under rule 8, the three python rows that read `ci.yml`, plus a CodeQL `actions` pre-scan.
7. **Stale header `web/src/test/pdftotextTimeout.test.ts:4`** ("CI runs no Playwright"), outside this lane. Default: the MPS records seat tickets it; it is not edited here.

## UNMEASURED
I had no `node_modules` (an npm install is a hosted call), so I made NO vitest, lint, build or Playwright run. That the pin stays green under the temp-file shape is DERIVED from reading its scanner. I also did not measure: whether the four specs pass locally at base (the seat's baseline decides), the Ubuntu runner's poppler version, whether the runner image already has `pdftotext`, how long `apt-get update` takes there, how long the four specs and the `--repeat-each=5` runs take here, the hosted web job's new total, whether `npm ci --prefer-offline` finds every package, and the true cause of the stdin hang (the temp file is the reviewer's suggestion, not a measured root cause). The Playwright `Total:` line form comes from Playwright 1.63.0 source (`runner/index.js:4926`), not a run.

## Outside the fences (disclosure)
Read: the commission file, DRAFTER_RULES, the sweep's MPS section, the B1566 kit, report and VERDICT (template), the B1578 and B1573 lane tables and B1578's stamp slots, `model-routing.md:84-116`, `models_latest.json`, `brief_seat.sh` (grep), the gate standard's step 7, the `stamp_check.py` header and matcher, the project `CLAUDE.md:50`, the heavy-lock `holder.txt` files, and the Playwright list reporter line in gate g1566's `node_modules` under `fleet/state/s277/g1566/clone/web/` (TUESDAY state, read only). Jira: GET only for 57, 135, 297, 251, 334 and 361, with the token read in-process and never printed. GitHub: `gh api -X GET` only (ref, tarball, pulls, branches, compare, trees, check-runs, actions job) under the project `GH_CONFIG_DIR`. Ran locally: the three python rows on my scratch copy of the tarball (and a planted copy), `node24 -e` with `sleep` for the timeout text, `pdftotext` on an empty stdin and `-v`, plus `lsof`, `tmux list-panes`, `uptime` and `df`. Wrote only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1582/` (`jget.py`, ticket dumps, tarball and tree, `plant/`, `fill.py`, logs, `prs.jsonl`, `branches.txt`, `seatkits.txt`, `main.sha`, earlier sidecar inits `measured.init1/2`), plus the kit, its sidecar and this report. No Jira write, no git write verb in any project repo, no push, no PR, no az, docker or ssh, no hosted HTTP beyond the GETs above, no `decision_queue.sh`, no card read, no message, no WEDNESDAY or FRIDAY tree, no `_ledger.md`. `date` is the only clock source.

DRAFTED B1582: kit 87 lines, sidecar rc 0, questions 7
