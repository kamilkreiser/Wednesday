STARTABLE: YES (the slice is three test-only pins; Q1 and Q2 below need your eye at the stamp, the kit holds both defaults)

# B1567 DRAFTER REPORT (SEAT-N129, NexusAI lane B, slice 1), drafted Sun 15 Nov 2026 10:54 to about 11:10 AEDT (`date` at start 10:54:42, last `date` 11:08:01)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1567_SEAT-N129_nexusai-lane-b-test-pins.md` (156 lines, 5 lines with the four-underscore pattern: four slots and the last line; ASCII 0 non-ASCII characters; ban-list name scan 0 with the `_by_<name>_` control firing 1 for every name; the card/decision-id scan hits only the kit's own descriptions of that scan, as in the template). Sidecar `.md.measured`: `stamp_check.py` prints `89 claims, 89 measured, 0 not measured`, rc 0 (run alone, not through a pipe); it also carries S01 to S25, each a real read at main `4ba2e03c`.

## BLUF
- **Slice (one Sonnet seat, test-only, about 2 hours of build plus about 70 to 90 minutes of lock hold after N128's):** RD-576 (add the mode to the security-fixes cell that no longer reaches its own check), RD-590 residue (the `dAlias` label at `rd486...:357` is stale), RD-826 item 2 (two new cells in `rd791` pinning the withheld-link warning). **Three existing test files change; no product file does.** Branch `b1567/nexusai-lane-b-test-pins`, commit A (three files), optional merge M, commit K (counts +2: 5636 -> 5638 PREDICTED, suites 349 unchanged). Seat `SEAT-N129`, Sonnet, row C2 (`model-routing.md:92`), gate G2 (`:109`). Slot 7 (trees `old39 new5 mut35 chk2 upd10 fin22`), port block 9830-9839.
- **Every ticket proved by MUTATION, not by a red-first run** (a test fix has no source to go red on): step 1 shows the UNFIXED tests miss the mutants (the ticket's own finding, re-measured), step 4 shows the FIXED tests kill them.
- **Not built before, one fact the sweep had as UNMEASURED:** the earlier lane-B seat left three LOCAL, never-pushed commits in its own clone `.tools/b1433/clone` for exactly these items (`15124bec` RD-576, `4897282a` RD-590 label, `ae6836b4` RD-826 items 1 and 2). All three are `commit` objects there and absent from origin (my clone, which holds origin refs only, prints "not an object"). The kit says: **fresh build, no tree takeover; the diffs may be read once as a RELAYED reference.** I found none of these on any origin ref.

## The 13 lane-B keys, by program and reason (the sweep named 13; RD-577 and 578 are one pair)
| key | verdict | reason (instrument in the sidecar) |
|---|---|---|
| RD-576 | IN | the cell at `security-fixes.test.js:536` has no `mode` at main (S25); ticket fix is one line; proof run comment 37869 [S04, S10] |
| RD-590 | IN (residue only) | its main body is ALREADY ON MAIN: RD-574 round 2 `7728d69` is an ancestor of main (rc 0) and the cells `:222-224` are single-variable variants of the stored name; what is open is the `dAlias` label `:357` (stale text count 1) [S05, S12] |
| RD-826 | IN (item 2) | `logger.warn` at `dataExport.js:310`; 0 test files hold its text; `rd791` mocks the logger at `:37` and never reads it [S13, S25]. LEFT: item 1 (customer-visible manifest wording plus a helper exported from `backend/dataErasure.js`; the build exists as local `ae6836b4`) and item 3 (a question "Tuesday's to rule") |
| RD-577 | ALREADY ON MAIN | `keyVaultStatus` at `backend/server.js:18301` reads `encryptionKeyVaultState()` (RD-518 merge `aae041a`), the comment at `:18296-18300` names RD-577; the only `KEY_VAULT_NAME` reads left are `:712`, `:740` (RD-578) and a comment [S07] |
| RD-578 | LEFT | the wrong-name reads are `backend/server.js:712` and `:740`: lane S (server.js), and the ticket says the sign-in one is reviewed on its own |
| RD-728 | LEFT | its target `rd-628-two-machine-id-derivations-s86m` is NOT on main (0 lines for `rd-?628` in `__tests__` and `backend`, control `rd-?486` fires; branch still on origin) [S07]. Taking RD-628's commits would be Tuesday's landing, not a lane-B cherry-pick |
| RD-744, 745, 750, 824 | LEFT | the erasure family. `model-routing.md:94` row C4 ("Data-destroying path") gives Sonnet "no", Opus first; the sweep put 745, 750, 824 in a Sonnet lane. RD-824 is also a question ("Tuesday's to rule"). RD-750's ticket gives no reproduction and no rule for which list wins (`filesPurged` or `filesFailed`): a design call on the ledger (`dataErasure.js:259-278`, `:1488-1494`). **Finding: RD-745's ticket text names the Dockerfile only as evidence ("the Dockerfile (/app/data) are normalised", 1 mention); its fix is `path.resolve(DATA_DIR)` in `_collectListedNames` (`dataErasure.js:311-313`) plus two cells. It does not appear to need a Dockerfile edit: Tuesday may re-lane it to the Opus erasure kit** |
| RD-804 | LEFT | alerts #138 to #141 read `fixed`, #142 `open` at `azureLogAnalytics.js:798` (the Log Analytics query POST, designed egress); the ticket's own recommendation is "read and record for the product owner; dismissal is his" |
| RD-805 | LEFT | alerts #143 to #150 all `open` (gh api -X GET each); a CodeQL set whose own text says read each site and record the second kind for the product owner; the earlier local build `942204d1` is absent from every ref on this machine and, per the earlier seat's STATUS, failed 27 tests in 6 suites because `backend/routes/entraProvisioning.js` needs a carrier-gate review-list entry. Not reusable |
| RD-455 | LEFT | acceptance 1 is "Decide and record whether an omitted token means keep the stored token" on the SCIM credential path, "gets a security review"; 0 lines in CLARIFICATIONS for RD-455 or `INVALID_SCIM_TOKEN`; a credential design surface is row C3 (Opus) |

## Facts re-measured (instrument; control)
1. Main `4ba2e03cc88e928c2c6fdf6694ebed0e7cadf2e5`, tree `b52c8378...` (`gh api -X GET commits/main`; my own clone, which fetched every origin ref over the project's deploy key with its push URL set to `invalid://no-push-drafter`, rev-parse equal). Counts 5636 / 349 (`git show origin/main:scripts/verify-expected-counts.json`). Open PRs 0. 64 open alerts on main, 0 in `__tests__/`, 0 in any file the kit edits (control: 29 in `backend/server.js`) [S01, S09].
2. Tickets read whole with all comments by my own GET-only reader `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1567/jget.py` (credentials read in-process by name from the project `.env`, never printed; JQL refused unless it starts `project = RD AND (`; this run used issue-by-key GETs only): RD-576, 577, 578, 590, 728, 744, 745, 750, 804, 805, 824, 826, 455. All To Do.
3. Seat id by program: the highest earlier `SEAT-N<n>` in the Briefs folder is N128 (sorted numerically), so N129. Slot: `sha256(realpath).readUInt32BE(0) % 19` (`test-server.js:89-94`), controls `b1430-nodot/b1` -> 6 (the precedent) and `b1563-nodot/old12` -> 1 (N128's own slot); yours `old39 new5 mut35 chk2 upd10 fin22` all -> 7, band 24480-25119, `lsof` 0 rows [S17-S19]. Ports 9830-9839: `lsof` 0 rows, scan of the 16 non-`.pre` SEAT kits of 11-14 and 11-15 (this kit excluded) 0 hits, control `979[0-9]` 1 hit; the live panes at the last read: N128, MPS-M135, HPSM-POC-H164 (R231 not listed) [S16, S21].
4. Deploy demo: `paths-ignore` is `**.md`, `docs/**`, `tests/**` (`deploy-demo.yml:30-32`); by a glob program the four OWNS paths are NOT ignored (control `docs/x.md` is), so a merge would start Deploy demo and both jobs gate on `CI_DEPLOY_ENABLED` (`:53`); the demo hold stands [S14]. Landing rule `CLARIFICATIONS.md:2067` quoted [S15].
5. `jest.config.js` has no `clearMocks`, `resetMocks` or `restoreMocks` (0, control `testPathIgnorePatterns` 1): the new cells clear the warn mock themselves [S13].
6. **Collision with N128 handled in the kit:** N128 and this seat both end with a commit K on `scripts/verify-expected-counts.json`. 62 ahead-of-main refs touch that file (control fires) [S24]. HOLD 20 of the kit: main moving before K allows a clean merge M and a rebuilt K at the merged head; a conflict, or main moving AFTER K and touching the counts file, is `git merge --abort` and a STOP naming the landing order; Tuesday rebuilds the second counts file at landing (the sweep's "regenerated by Tuesday at landing").

## Census of existing tests pinning behaviour the slice changes (by program; frame: every tracked file under `__tests__/` and `tests/` at main, `git grep -l -E` on `origin/main`; each list in S23)
| pattern | files | status |
|---|---|---|
| `same machine by another name` (the label RD-590 renames) | 1 (`rd486-ai-test-key-forwarding.test.js`) | nothing pins the label elsewhere |
| `incomplete override (missing apiKey)` (the cell name, unchanged) | 1 (`security-fixes.test.js`) | unchanged |
| `security-fixes.test` or `rd791-export-store-links` named in tests | 2 (`synthetic-isolation.test.js`, `table-discovery.test.js`), prose comments only | unaffected |
| tests that read every test file (`TESTS_DIR = __dirname`) | 1 (`sustainability-stand-in-labels.test.js`, acorn-parses every `*.test.js`) | step 3 runs it |
| tests that read tracked files (`ls-files`) | 10 | step 3 runs `rd731`, `rd342`, `rd737` and the full verify is the proof for all 10 |
| tests that call `applyLLMOverrides` | 4 (`rd395-llm-mock-preload.js`, `rd464-rd549-unconfirmed-not-probed`, `rd503-r2-doc-claims-against-product`, `security-fixes`) | product unchanged; step 3 runs the three tests |
| tests that require `backend/dataExport` | 9 | product unchanged; step 3 runs all 9 |
| the withheld-link warning text in tests | 0 (control: `backend/dataExport.js` holds it once) | the gap the ticket names |
Controls that fire: the patterns for dataExport requirers and `ls-files` readers return rows; the zero for the warning text is paired with the source file reading 1.

## Chain step inputs (each produced by an EARLIER step or present at BASE)
| step | inputs | produced by |
|---|---|---|
| Commit A | BASE clone, `npm ci`, the line pointers re-read | Step 1 |
| 1 survive (`old39`) | BASE tree; the plant scripts G and WARN | Step 1; Tools (before the waiter) |
| 2 new-cells (`new5`) | tree at A | commit A |
| 3 related (`new5`) | tree at A | commit A |
| 4 mut (`mut35`) | tree at A; step 2 green | commit A; step 2 |
| 5 mainmove | steps 1 to 4 green | steps 1-4 |
| 6 p-plain (`chk2`) | head of step 5 (A or M) | step 5 |
| 7 u-update (`upd10`) | step 6's counts refusal | step 6 |
| 8 kstep (`wt`) | step 7's counts file | step 7 |
| 9 p-plain-K (`fin22`) | K | step 8 |
No step reads a file a later step makes. There is no inventory step: the diff holds no `backend/` path, so the route inventory cannot change (stated in the kit; the inventory-reading suites run in the verify).

## D-decisions (drafter, at source)
- D1 Fresh build, no cherry-pick and no tree takeover: each diff is 3 to 150 lines of test text; reading the old commits (`git show` of a sha in another seat's clone, read-only) costs one command, taking over the clone would break the per-seat tree rule and drag in `ae6836b4`'s item-1 words.
- D2 The new cells go into the existing `rd791` file, not a new suite: the harness, the mock and `freshDir` are there, the suites count stays 349 and the counts change is tests only (+2). The earlier seat's version was a new 150-line file mixing item 1.
- D3 W1 pins three things the ticket names plus one it implies: one warn per link (exact count 2), the store named (`file`), no path in the call (substring checks on four paths), and exactly the keys `file` and `resolves` (so a later field cannot smuggle a path in). W2 is a pure pin.
- D4 Proof is by mutation with a BASE survival run (step 1) before the FIXED-test kill run (step 4), the two-sided form of the ticket's own proof run: a plant that does not survive at BASE would mean the diagnosis moved, and the kit makes that a Corrections line, not a silent pass.
- D5 No inventory, no CodeQL claim on the PR head (HOLD 2 repeats the rule: main's analysis after landing is the check that can fail). CodeQL's CLI is named with its real binary path `.../tools/codeql/codeql/codeql` (the path in the commission, `.../tools/codeql/codeql`, is the directory) and the suite file `javascript-code-scanning.qls` found by `find` in the pack.

## QUESTIONS FOR TUESDAY (each with a default)
- **Q1 Erasure family and model row.** The sweep puts RD-745, 750, 824 in a Sonnet lane; row C4 (`model-routing.md:94`) says Sonnet "no" for a data-destroying path. **Default: leave all four (744, 745, 750, 824) out of every Sonnet kit; one Opus erasure kit later takes 744 and 745 (745 not Dockerfile-bound by its own text), 750 after a rule on which list wins, 824 after your ruling.**
- **Q2 RD-826 item 1 (manifest wording).** The words come from a gate round ("YES, planned here"), not from a product-owner ruling, and they are customer-visible export text. **Default: LEFT; if you rule they are not "new" words, a second Sonnet kit rebuilds `ae6836b4` fresh (it also exports `_walkLinkChain` from `dataErasure.js`).**
- **Q3 Counts collision with N128.** Both branches end with a commit K on `scripts/verify-expected-counts.json`. **Default: as in the kit (HOLD 20): neither seat resolves a counts conflict; whichever lands second has its counts rebuilt at landing.**
- **Q4 RD-590.** The kit builds only the label residue and says the main body is already on main (proved at source). **Default: the records seat closes RD-590 after landing; you may prefer to close its main body now.**
- **Q5 RD-804 and RD-805.** Both read "record for the product owner". **Default: LEFT; a later Opus kit reads each site and a records seat writes the reading for the owner, with the review-list entry for `entraProvisioning.js` in the same kit.**

## UNMEASURED
- Every jest result: cell counts (rd791 6 -> 8, tests 5638 / suites 349) and every mutation result are PREDICTED; I ran no jest (the project lock is N128's for about 100 minutes and the drafter fences forbid it). The BASE survival of mutant G (the cell at `:536` was re-anchored by RD-794 since the ticket's proof run) is the ticket's finding at commit `2edde62`, RELAYED, re-measured only by step 1.
- The exact wording of the new `dAlias` label (the kit demands it be TRUE and gives the facts to word it).
- CodeQL CLI results on the three edited files (NOT RUN by me); hosted CodeQL on the PR head and on the merge commit; Linux; the Deploy demo run a landing would start (reads `skipped`, RELAYED).
- Whether R231 is running (its pane was absent at the last `tmux list-panes`).

## Outside-the-fences disclosure
- Writes: the kit, its sidecar, this report; scratch only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1567/` (my Jira reader, the ticket texts, `g.sh` and `at.sh` read-only git wrappers, the alert TSV, slot, port, ref and fill programs, a clone of the repository by SSH with the project's deploy key, push URL `invalid://no-push-drafter`, fetched from origin only, never pushed). Nothing written under `/Volumes/Datasec_DEV/!CODING/`; the project checkout was not fetched or touched; no Jira write; no GitHub write; no message; no az, docker, hosted HTTP or `tmux send-keys` (one `tmux list-panes` read, one `tmux` read for S16).
- Reads in the project folder (read-only): `CLARIFICATIONS.md` (line 2067, C-224 line, greps), the Briefs folder (greps and `2026-11-10_B1433_STATUS.md` of the earlier lane-B seat), `.tools/b1433/clone` via `git cat-file` and `git show` of three shas (another seat's clone, read verbs only), `.tools/b1555/clone` `config --local --get user.name` and `user.email` as lengths only, `session-tools/nexusai-lock.sh` header, the lock directory listing, `.env` variable NAMES only (values read in-process by my reader, never printed), `gh api -X GET` for commits, pulls and code-scanning alerts under the project's own `GH_CONFIG_DIR`.
- Hook events: a `$D` variable in a `git -C` fetch command was refused unexpanded (re-issued with the literal path); one zsh word-splitting refusal (a wrapper script replaced it); several advisories on case-sensitive greps and `grep | cut`. One slip of mine: a fill program ran against a sidecar when stamp_check printed `OK` instead of `MISS` lines and wrote an empty sidecar; I fixed the parser and rebuilt all 89 lines plus S01 to S25 from real reads. No fence was bypassed.
- `DRAFTER_RULES.md` names `/Volumes/Laptop-DEV/...`; I used `/Volumes/Datasec_DEV` everywhere.
- Weakest parts: the BASE survival prediction for mutant G; the label wording; the lock-wait length (N128's hold has not started); Q2 (what counts as a "new" customer-facing word).

DRAFTED B1567: kit 156 lines, sidecar rc 0, questions 5
