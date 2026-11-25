STARTABLE: YES

# B2113 DRAFTER REPORT (Sonnet drafter, read-only, for Tuesday s329): Composer PCOMP-23 policy PDF footer, seat C110

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2113_SEAT-C110_composer-pcomp23-pdf-footer.md` (76575 bytes; seven Stamp slots as four underscores, last line `READ-WHOLE-BY-TUESDAY: ____`). Sidecar: the same name plus `.measured` (98 claims, 98 lines, `stamp_check.py` exit 0). Times: `date` printed 09:02:59 at the start, 09:11:47 and 09:18:09 later.

## BLUF
The defect is real and reproduces by render on code main `d06508f8a69267542b92959a2048198055a7b473`: a policy PDF with a 250-character policy name and a 200-character company prints NO `manifest <hash>` line on 22 of 22 pages (ordinary words) and 23 of 23 pages (wide letters); a seeded probe of 192 cells loses it in 96 at main and 0 after the fix. The fix is small and reuses the change report's own fitting: export `footerFirstLine` from `change-report.ts` (one word), import it in `policy-document.ts`, wrap the first footer line (two edits) and add one new renderer test file of five cells. `document-pdf.ts` needs NO edit. Short names are byte for byte unchanged (PDF and DOCX sha256 equal at main and with the fix). Branch only, G2 proposed, nothing deploys.

## Facts re-measured with instruments (each is in the sidecar with its source)
- Main sha, open PRs 0, the three file blobs, the four release blobs and the two CONTENT_HASH value prefixes: `gh api -X GET` under the Composer GH_CONFIG_DIR (control: a missing path returned HTTP 404; `pulls?state=closed&per_page=5` returned 5).
- Ticket PCOMP-23: Jira GET (description and both comments read whole; control `PCOMP-9999` 404). Both comments say the policy half is not done. Rows 450 to 453: PCOMP-120, 121 and 122 are Done in Jira, only PCOMP-123 (row 453, owner's choice, 0 hash lines lost) is Backlog.
- Pointers by `grep -n` over the raw files at main: `policy-document.ts:835` (footer), `:10` (import), `change-report.ts:750`, `:665`, `:499`, `:502`, `:809`, `document-pdf.ts:187`, `:189`, `:257`, `document-docx.ts:181`, `package.json:21`.
- Reproduction and fix (host, scratch copy of main, project's own vitest 5.0.0, prettier 3.9.6, eslint): T0 (new test over unfixed product) `3 failed | 2 passed (5)` (P1, P2, P5); fixed `5 passed (5)`; whole renderers project 296 passed, 1 skipped, 34 files (291 and 1 and 33 without the new file); prettier and eslint rc 0; mutants C0 5 passed, M1 3 failed, M2 2 failed, M4 3 failed, each restored and `cmp` equal.
- The kit's own scripts ran on the host over the scratch copy: `mut_build.py` (anchor count 1 for M1, M2, M4), `mut_job.sh` (C0, M1, M2, M4), `edit_job.sh` (T0 and FIXED), `ck7_compare.py` (host JSON of base and head, PASS with controls), `ck345.py` (simulated base and head pair in a scratch git repository: PASS on every line with controls; it first FAILED its bytes check on whole files, which the drafter fixed to read the added lines only).
- PRIOR WORK: pull requests 113 and 120 built the change report half and the mechanism reused; 85 touched `policy-document.ts` and `document-pdf.ts` for content, not the footer; 203 branches, 4 footer-named (all change report or deploy guide), 0 for this lane; 0 open PRs; Seat id C110 free (0 file names before the kit, control C109 3 and 1).

## D-decisions (the drafter's, each open to Tuesday)
- D1 The fix is at the footer STRING (the change report's shape), not in the PDF writer. Why: the writer is shared by the cover, contents page and every table; the string fix keeps all of that byte for byte for names that fit.
- D2 `footerFirstLine` is exported in place from `change-report.ts` (a third source path, one word). The change report's own tests (22 cells) stay green with it (drafter's run).
- D3 The DOCX shares the footer string (`...parts.spec` in both spec builders), so the DOCX footer is clipped the same way; the change report does the same.
- D4 One new test file `policy-footer-budget.test.ts`, five cells (P1 PDF every page released and draft in three shapes, P2 string within budget and modelled rows for PDF and DOCX spec, P3 DOCX hash line, P4 short name byte for byte, P5 exact budget versus one over). P3 and P4 pass at BASE on purpose (controls).
- D5 Mutants M1, M2, M4. The row-count mutant (`FOOTER_FIRST_LINE_ROWS` 2 to 3) is left out: the new file does not kill it (5 passed, drafter's run) and `change-report.test.ts` does (6 of 22 failed); it is the change report's cell.
- D6 Branch `b2113/policy-footer-budget`, test path `packages/renderers/test/policy-footer-budget.test.ts` (no ticket key in a path or text a commit will carry).
- D7 Launch row `BRIEF_SEAT_LEVEL=sonnet` (routing row C2, line 92), gate G2 proposed (line 109).

## Questions for Tuesday (each with a default)
- Q1 Where does the reused fitting live? Default: export `footerFirstLine` in place from `change-report.ts` (the kit's closed list holds three paths). Alternative: move it to a new shared module (larger diff, touches the change report's bytes).
- Q2 Is `document-pdf.ts` really left unedited though the commission and the sweep named it as owned? Default: yes, no edit (CORRECTIONS 1); a seat that finds a reason STOPs.
- Q3 Does this kit's Done reading need the 18-cell residue (rows 450 to 453)? Default: NO. The kit builds the policy half only; 450 to 452 are Done tickets for the change report, 453 is an owner's choice that loses no hash line. Whether PCOMP-23 itself is Done stays Tuesday's records pass. The drafter's own probe of the policy PDF after the fix (192 cells, 0 lost) is a small frame, not the gate's 9,508.
- Q4 Model and gate tier: Sonnet seat (row C2) and G2 (`model-routing.md:109`, a follow-up whose mechanism prior gates measured) or G1 (line 108, customer PDF and DOCX bytes change for a long first line)? Default: Sonnet and G2; G1 if you read "handed to a client tester" as covering any customer-facing byte change.
- Q5 The clipped footer line ends in three ASCII dots (the change report's shape, which the product owner let land on 2026-11-03). Default: accept it as no new customer word; if you want the product owner's eyes on it, hold the lane at the pull request.
- Q6 Landing: as a squash pinned to the tested head through CodeQL, no deploy (C-160's shape). Default: yes, Tuesday opens and lands; nothing deploys because customer PDF bytes for long names change only on a deploy.

## Inputs of each chain step (each from an EARLIER step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| 0 | the kit, `.tools/b2033/scripts/*` (read-only), project files | present at drafting |
| 0c | seven b2033 scripts (copied with counted replacements), eight scripts written from the kit | Step 0 dir `.tools/b2113/scripts` |
| 2 | clone at BASE, `docker/Dockerfile` | Step 0 clone |
| 3 | clone, the three edits and the new test file, mut_build inputs (the two edited source files) | the edits of Step 3 itself, before `mut_build.py` and `edit_chain.sh` run |
| 4 | the three edited paths | Step 3 |
| 5 | the commit, base JSON (`base_steps_*.json`) | Step 4 and Step 2 |
| 6 | the commit and its head | Step 4 |

## UNMEASURED (a stamp must know)
- Docker, the image build, `run_job.sh`, `heavy.sh`, `docker cp`, `ck67_job.sh`, `run_steps.sh`, `head_chain.sh`, `scripts/secret-scan.sh`, `content:check` and the real workspace project run: never run by anyone; the kit's expected counts for the image (renderers base 291 passed 1 skipped, workspace 3041 passed 2 failed) are RELAYED (C-160) and derived from the host. The in-image `npx tsc -b tsconfig.build.json` rc 0 is expected, not measured (host rc 2 is a stale host `node_modules` at `apps/api`).
- `git ls-remote` and any ssh: not run (fences); the drafter used `gh api -X GET git/matching-refs` as the equivalent. The seat's own REFUSE checks are theirs.
- The workspace half of `ck7_compare.py` was exercised on a copy of the renderers JSON (a comparator test), not a workspace run; `ck67_job.sh` and the chain wrappers (`mut_chain.sh`, `edit_chain.sh`) were `bash -n` checked only.
- Typecheck of the new test file: CI's `tsc` covers `src` only; the drafter's host `tsc` over the test file reported no error in it and one pre-existing error in `test/support/pdf-text.ts` (host `pdfjs-dist` types); not an in-image run.
- Host node v26.13.0 versus the image's node 22: PDF text positions could differ in principle; the new test reads the text layer as `change-report.test.ts` does.
- Load at drafting 22.92 near the lock's 24 gate (the seat will wait).

## Checks of the kit never run on a real output
The STOP-severity checks were each run once on prototype output with controls firing: CK2 mutant table (host, four cells), CK3 to CK5 (`ck345.py`, simulated pair), CK7 comparator (host JSON). Never run on a real output: CK1 (image), CK6 in-image controls, the head-image halves, `secret-scan.sh --tree`. A failure the seat can trace to the kit's wording is `STOPPED: NEEDS TUESDAY`.

## Outside-the-fences disclosure
Writes: only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s329/d2113/` (scratch: tarball and extracted main, pristine, proto, seat_scripts, sim2, ck7run, hosttmp, `_quarantine` with the moved probe and repro tests) and the three files named in the commission. Read-only uses of the Composer project: `4_Credentials/.gh-config` (gh GET), `4_Credentials/.env` (Jira, in-process through the b1959 helper imported by `importlib`, nothing printed), `2_Project_Files/node_modules` (copied INTO scratch), `.tools/b2033/scripts` and `.tools/b2033/clone` (read), `CLAUDE.md`, `CLARIFICATIONS.md`. One early `ls` over the project's briefs and `.tools` folders ran past its timeout and was moved to the background by the harness (it wrote nothing). No Jira write, no GitHub write, no docker, no ssh, no hosted request, no card store, no other seat's tree, no mail, nothing deleted (probe and repro tests moved to scratch `_quarantine`). One call of mine was refused by the no-cd hook (a stray `cd` in a command) and one by the no-rm hook (an `rm -rf` of a scratch folder I then did not need); neither ran.
