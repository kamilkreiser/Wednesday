STARTABLE: NO (until Stamp: the card `mpscalc-hosted-deploy-words-1112` reads `status: open`, `choice=None` at 15:1x, so the kit refuses at Step 0.3 by design; CI on 0bb3ed12 was still running with no package at 15:17)

# B1542 DRAFTER REPORT (MPS hosted deploy 0bb3ed12), drafted 2026-11-12 15:14-15:2x AEDT

## BLUF
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1542_SEAT-D62_mps-hosted-deploy-0bb3ed12.md` (104 lines, 12 stamp slots incl. the last line; `grep -c '_''___'` = 12 after the final edit). Followed B500 (newest MPS hosted deploy kit, `ls -t` and the STATUS last-line loop both say B500 is newest; B448 is its parent) plus the shape of today's B1536 (STATUS channel, launch_when_cool, S0-S10 stamp).
- Delta since the last hosted deploy (B500, `e027ebd0`): 91 first-parent commits, 258 files, +13,488 -493. **Migrations: none.** **Setting required: none.** One new OPTIONAL key (`MpsCalc:Templates:Path`; unset = in-memory store, so fleet templates are not persisted on the hosted site). Deploy tooling DID change (exit-3 meaning, two overlay GETs, no curl retry), so the kit does not assume B500's runbook.
- The real risk is not a migration but **stricter start-time loaders** (reference document, source versions, feedback triage, exact-enum snapshot read): kit Step 3f counts them against the backup before the swap.
- Findings that change how a seat must work: (1) `ci` run 43153226915 on 0bb3ed12 was `in_progress` at 15:17 (dotnet and web jobs), no artifact yet; (2) `.tools/qa-B500` does not exist, the counting tools must be rebuilt; (3) `wt-B500-release` and `wt-B448-release` have `.git` files pointing at `/Volumes/Laptop-DEV/...`, so `git -C` there is `fatal: not a git repository` (HEAD via `--git-dir` reads `e027ebd0`); (4) the proposal GET writes a `proposal-generated` event, so a live render of the one-page proposal is a write.

## What I read
DRAFTER_RULES.md whole; B500 kit whole (88 lines); B448 kit line count only (103) and its role; B1536 kit (stamp format, launch line, context band); B500 STATUS sections (BLUF, 3-pre/end, rollback note, addenda lines); project CLAUDE.md (grep deploy/hosted: no production classification); CLARIFICATIONS entries C-102, C-131, C-132, C-136 text and the heading list of word rulings; GitHub (GET only, project GH_CONFIG_DIR, account kamilDatasec): compare e027ebd0...0bb3ed12 (paginated), 91 per-commit file lists, patches of Program.cs, csproj, global.json, package.sh, deploy-from-ci.sh, ci.yml, Dtos.cs, ApiJson.cs, PricingPolicy.cs, ReferenceStoreDocument.cs, ActiveSources.cs, ReferenceDocumentValidator.cs; raw TemplateStore.cs, ProposalPage.tsx, QuoteEndpoints.cs, QuoteEvents.cs at 0bb3ed12; check-runs, runs, artifacts, code-scanning, open PRs. Local: `shasum`/`stat` on the rollback zip, `ls -A .tools`, worktree `.git` files. The card by `decision_queue.sh show <exact id>` into a scratch file (13 lines). No hosted HTTP, no az, no project-repo git other than rev-parse via --git-dir on the worktree HEAD.

## Facts re-measured (instrument; control)
- Main = 0bb3ed12808d72d3187c51d56852b7ecd2174666 (`gh api git/ref/heads/main`, 15:14); tree 3a6759b12e97fb22cb26807c4cd161ce975b0b9b; parent 3fb06085. Compare: ahead 91, behind 0, merge_base e027ebd0. Today's four (8 of 8 check-runs success each for #188 286795d7, #189 50c354ff, #190 3fb06085): #191 0bb3ed12 had 7 check-runs, 5 success, 2 in_progress at 15:17. Control for "check-runs read": the other three sha print 8 and 8.
- Migration scan: 0 file names and 0 added src lines containing `migrat`; control: the same regex matches planted `a Migration x`. No .bicep/.bicepparam file in the 258.
- Constants at main: ProposalPage.tsx:37 RENTAL_SHORT_LINE_CAP = 3, :43 RENTAL_SHORT_OPTION_CAP = 2, :39/:45 the "and N more" functions (singular `and 1 more line (see full proposal)`).
- #191 content: Dashboard.tsx wraps the follow-up table and QueueTable in `div.table-wrap`; styles.css media edges 698-1374, 918-1154 (was 1357, 1137) and a new 601-714 rule for five tiles.
- Rollback zip e027ebd0: sha256 2e73f4d62f099c0ef21a8d4d771b09ffa819820ef79fc029b841e776a41a908c = B500 STATUS line 146 value; 3186504 bytes; .RUN 39777968295.
- Ports: `lsof -nP -iTCP:8480-8499 -sTCP:LISTEN` printed 0 lines (control not run; the kit leaves the block to Tuesday, S7).

## D-decisions (mine)
- D1 Rollback target is `e027ebd0` (B500's package) under the standing roll-forward rule C-102; R-1 added the new-type-rows condition because the refusal build is not built.
- D2 Step 3f (new): start-refusal counts for the loaders that got stricter; any count > 0 stops before the swap.
- D3 rc 3 now means "deployed, start not proven": the kit forbids re-running `deploy`, runs `check` once.
- D4 Words check kept strict (B500 form, docs/log outside by ADDENDUM-2); staff-only unruled strings also stop unless S4 says otherwise.
- D5 Live check of the one-page proposal and home tiles is static in the live bundle/CSS with controls drawn from the e027ebd0 package; rendered reads are UNMEASURED unless S4 allows.

## Q for Tuesday (each with my recommended default)
- Q1 Words scope: does the 10:49 statement plus the card cover every new word in the 91 commits? Default: NO, only what the card lists; the seat runs the census and stops on unruled strings (S4 can relax staff-only ones).
- Q2 Allow ONE proposal view of ONE existing rental quote (writes one `proposal-generated` event) so the one-page claim is seen live? Default: no; static rows plus UNMEASURED; the claim rests on the gate's local measurement.
- Q3 Allow a signed-in browser read of Home for the #191 tiles/tables? Default: no (UNMEASURED, said plainly to the product owner).
- Q4 Deploy without `MpsCalc:Templates:Path` (templates in memory, lost at restart)? Default: yes, no setting change; tell the product owner. A setting card is a later deploy.
- Q5 CI: stamp S3 only after run 43153226915 is green with the package job and the artifact present; do not launch before. Default: yes.
- Q6 Rollback policy: R-1 only with an unchanged store, 0 new members, 0 new-type rows beyond the pre-count; else fix forward. Default as written.
- Q7 Path prefix: DRAFTER_RULES.md names /Volumes/Laptop-DEV; I used /Volumes/Datasec_DEV as today's B1536 does. Default: Datasec_DEV.
- Q8 Card id: rule 7 says no card id in kit text; the Step 0 command needs it (and the task required it). I kept it in Step 0.3 and told the seat STATUS only. Default: keep.
- Q9 Stale worktree gitdirs (Laptop-DEV paths) on wt-B500-release / wt-B448-release: leave unrepaired (a write into an old worktree); seat uses --git-dir reads. Default: leave.
- Q10 Hard stop and port block are slots S9 and S7 for you.

## UNMEASURED
- Live site state (settings, store counts, served bundle): not touched; B500's end values are RELAYED.
- Whether wt-B500-release's deploy script runs there (gitdir broken); whether e027ebd0 refuses a snapshot holding this delta's new members; what the template store logs at start.
- Web-file patches: the compare returns none for 106 files (all web and tests), so no word census was done; the kit makes it the seat's Step 0W. I did not count how many new customer-visible words the 91 commits hold.
- Whether the hosted reference.json/feedback store trips any new loader rule (Step 3f is the check).
- The commit-API file lists are capped at 300 per commit; no commit reached it (max 21 files).
- Fence disclosure: I did not read briefs_staged, scoreboard, ledger, any WEDNESDAY/FRIDAY tree, or run `decision_queue.sh list`; the model-routing and models_latest lines cited were printed by grep -n. I ran `git --git-dir ... rev-parse HEAD` (a read verb) on a project worktree, and one rejected `git worktree list` (refused by the hook, did not run).

## The 91 commits (first-parent order; files = commit API; migration column is the scan above)
| # | sha8 | files | migration | config / risk flag | subject |
|---|---|---|---|---|---|
| 1 | 4c593517 | 7 (src 0, web 4, tests 0, docs 3, ops 0) | no | none | Docs and contract words: rounding, inventory keys, unchanged save, readyToExpo |
| 2 | c4aa4cc7 | 4 (src 1, web 0, tests 3, docs 0, ops 0) | no | none | Deal-usage proposal prints a colour rate only for a class with estimated colou |
| 3 | 75d1c6e7 | 7 (src 1, web 0, tests 6, docs 0, ops 0) | no | stored default (7% rebate) | Pricing policy: restricted saves keep the base first-line rule; leak tests and |
| 4 | e3624f00 | 14 (src 3, web 0, tests 11, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | Source versions: one id per case and accent spelling; exact cost-per-page chec |
| 5 | a5b4bbb5 | 15 (src 0, web 15, tests 0, docs 0, ops 0) | no | none | Web BOM and fleet screens: rows kept by identity, class labels, in-place figur |
| 6 | 459db8b8 | 21 (src 6, web 0, tests 15, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | MPSCALC-215/-216/-210/-217/-196/-230: API input hardening |
| 7 | 94258c9e | 9 (src 3, web 2, tests 3, docs 1, ops 0) | no | none | Reconciliation: contract-scale supplies cost, reflection guard, readiness CSV  |
| 8 | b8625d3c | 7 (src 2, web 0, tests 4, docs 1, ops 0) | no | none | Importer and source-version pins; a map-held plain option code warns instead o |
| 9 | 05c598f3 | 17 (src 2, web 8, tests 4, docs 3, ops 0) | no | contract/stored-shape member | Proposal: one combined usage-rate pair per deal; docs clauses for 195 and 219 |
| 10 | 9cb6d9ba | 9 (src 1, web 0, tests 8, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | Store hardening: load retry, null tier pool and members refused at load, survi |
| 11 | 5fe35a05 | 9 (src 1, web 3, tests 3, docs 2, ops 0) | no | none | Refusal order on draft save (who and state first), one line at the decimal min |
| 12 | 93e1cab5 | 9 (src 0, web 4, tests 5, docs 0, ops 0) | no | none | Tests and dev stub: seven test-strength fixes (type-token row, threshold cases |
| 13 | dd0ce36d | 3 (src 0, web 2, tests 1, docs 0, ops 0) | no | none | Dev stub unit tests and bundle-check key; test header matches the recorded run |
| 14 | 8b046423 | 5 (src 1, web 0, tests 4, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | Refuse null product or null supplies link with the existing issue instead of a |
| 15 | ef9bfba4 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Pin the store file absent at first use and the vanished-file answer (tests onl |
| 16 | a85f8bd5 | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Dev stub: pin list order, session memory, held-create fields and the stale-ahe |
| 17 | 110ebecd | 2 (src 0, web 1, tests 0, docs 1, ops 0) | no | none | API description: approved unchanged-save sentence; BOM spec: exact Quote type  |
| 18 | f5a27af0 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Pin the empty-path no-store sentence and the relative store path read under th |
| 19 | 1ac8ab8a | 4 (src 2, web 0, tests 1, docs 1, ops 0) | no | none | Draft validation: cap the per-line validation walk and pin it (#112) |
| 20 | 2e7f9d8a | 1 (src 1, web 0, tests 0, docs 0, ops 0) | no | Pkcs pin (package content) | Raise the pinned System.Security.Cryptography.Pkcs to 10.0.14 so the deploy pa |
| 21 | 2d8fede4 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | MPSCALC-336: test rows pinning the refusal of null-class edge rows (#117) |
| 22 | 1137f119 | 2 (src 1, web 0, tests 1, docs 0, ops 0) | no | none | The parity proof refuses a count-preserving panel tamper (#122) |
| 23 | 45ecc9ca | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Replace the panel multiset rows' assertions that cannot fail with a refusal ch |
| 24 | 48bc62af | 1 (src 1, web 0, tests 0, docs 0, ops 0) | no | Pkcs pin (package content) | Update the example tie in the publish-target comment to the current Pkcs pin ( |
| 25 | 2d55ee19 | 2 (src 1, web 0, tests 1, docs 0, ops 0) | no | none | Pin that the line number, manual item id, note and supplies-null caps are spen |
| 26 | ac107e0d | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Pin that the first of two supply groups with the same references stays in forc |
| 27 | b8ae9011 | 19 (src 4, web 10, tests 3, docs 2, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f); contract/stored-shape member | Refuse a stored triage note the API could not have written, and pin the remain |
| 28 | 32b09108 | 3 (src 0, web 0, tests 3, docs 0, ops 0) | no | none | Pin the supply-group order, the draft-walk counters and the stored triage chec |
| 29 | 960141b3 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Pin that two fleet lines with one number and a control character each list tha |
| 30 | 44137f7a | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Pin that a priority spelled in another letter case is not loaded, and the whol |
| 31 | 080f1608 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Hold the fake Jira's create in the enabled-submit test so the 201 is read befo |
| 32 | 1a2a0294 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Pin the deps.json entry count with a published copy that lists no Pkcs entry ( |
| 33 | 5d96a3dc | 9 (src 6, web 0, tests 2, docs 1, ops 0) | no | none | MPSCALC-254 MPSCALC-256: page basis per device or per line, and the rental rec |
| 34 | edac7431 | 9 (src 4, web 0, tests 4, docs 1, ops 0) | no | none | MPSCALC-252 MPSCALC-258 MPSCALC-259 ENGINE HALF: purchase device groups, tier  |
| 35 | 5c64a442 | 5 (src 3, web 0, tests 1, docs 1, ops 0) | no | none | MPSCALC-255 ENGINE HALF: purchase managed-service fee per device per month on  |
| 36 | 3496da33 | 7 (src 3, web 0, tests 3, docs 1, ops 0) | no | none | MPSCALC-256 ENGINE HALF: purchase recurring projection, monthly, annual and co |
| 37 | 7f34130c | 6 (src 4, web 0, tests 1, docs 1, ops 0) | no | none | MPSCALC-253 ENGINE HALF: purchase component quantity rule, per device, fixed p |
| 38 | 6e0aa641 | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Web quantity audit: no flag in a purchase section with several device lines |
| 39 | b7cf1ad0 | 3 (src 0, web 3, tests 0, docs 0, ops 0) | no | none | Web generated contract copies regenerated from the current contract |
| 40 | 19d084fa | 4 (src 2, web 0, tests 1, docs 1, ops 0) | no | none | MPSCALC-257 ENGINE HALF: purchase sites on device groups, a Review issue on a  |
| 41 | f8f808c4 | 4 (src 0, web 0, tests 4, docs 0, ops 0) | no | none | Tests only: nine rows for MPSCALC-357, MPSCALC-362, MPSCALC-343 and MPSCALC-34 |
| 42 | 7104179f | 5 (src 0, web 5, tests 0, docs 0, ops 0) | no | none | web: hold Add section until the price list read has answered (#142) |
| 43 | 17fc0dbc | 3 (src 0, web 2, tests 0, docs 1, ops 0) | no | none | MPSCALC-366, MPSCALC-345: quantity audit rows for 13 against 12 devices and a  |
| 44 | e970f7eb | 3 (src 1, web 0, tests 1, docs 1, ops 0) | no | none | MPSCALC-257, MPSCALC-367: site allocation warning shown on every quote that pr |
| 45 | 0d4022b9 | 14 (src 5, web 3, tests 4, docs 2, ops 0) | no | NEW optional key MpsCalc:Templates:Path (absent=in-memory); contract/stored-shape member | MPSCALC-269: server store for fleet configuration templates (#145) |
| 46 | 80203089 | 1 (src 0, web 1, tests 0, docs 0, ops 0) | no | none | Test: snapshot equals contract, schema.ts body equals generator output (MPSCAL |
| 47 | 48b749fb | 3 (src 1, web 0, tests 1, docs 1, ops 0) | no | none | MPSCALC-361: the reconciler counts a fleet-total line's pages once, as the cal |
| 48 | b7eebb47 | 2 (src 0, web 0, tests 1, docs 1, ops 0) | no | none | Template-isolation scan reads code inside interpolated strings; three API doc  |
| 49 | 62fd49c7 | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Web quantity audit: a zero-quantity device line is not a counted device line ( |
| 50 | 314b53f6 | 13 (src 5, web 4, tests 2, docs 2, ops 0) | no | contract/stored-shape member; stored default (7% rebate) | A purchase line states its quantity rule by the engine's three names on the Ap |
| 51 | 987eb25c | 1 (src 0, web 1, tests 0, docs 0, ops 0) | no | none | Test only: one named row pins the counted-set boundary at one device line (MPS |
| 52 | 069751a0 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Test only: killing rows and guards for the template isolation scan (MPSCALC-37 |
| 53 | 9bdf4548 | 1 (src 0, web 1, tests 0, docs 0, ops 0) | no | none | Contract sync test: how-to-fix text names the next step for each of its three  |
| 54 | 5a483a90 | 3 (src 1, web 0, tests 1, docs 1, ops 0) | no | none | The rental reconciler counts a fleet-total line's pages once, as the calculato |
| 55 | 0d656f90 | 5 (src 3, web 0, tests 1, docs 1, ops 0) | no | none | A per-site purchase line counts once per site holding a device, and a quote wi |
| 56 | 511e6c03 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Test only: pin two line-break forms of the format guard, fix two comments (MPS |
| 57 | 60ac2e5b | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Test only: pin per-site rows for a missing site entry and today's repeated id  |
| 58 | 3b1ec832 | 1 (src 0, web 1, tests 0, docs 0, ops 0) | no | none | Bump undici to 8.12.3 and zod to 4.6.7 in /web (lockfile only) (#158) |
| 59 | 7648e03a | 1 (src 0, web 1, tests 0, docs 0, ops 0) | no | none | Test only: census renders the rental proposal and one-pager as S10 and S12 (MP |
| 60 | aa7fd175 | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Test only: colour guard reads var() fallbacks and filter, and takes a token li |
| 61 | e7038ad0 | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Proposal page: a print press while a print waits for its images is ignored (MP |
| 62 | 330a1c83 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Test only: overlay start gate rows for the collapsed path and the inside walk  |
| 63 | c55eb874 | 5 (src 0, web 5, tests 0, docs 0, ops 0) | no | none | Test only: bound every pdftotext call in the e2e specs, with a row that holds  |
| 64 | bb9bac9b | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Test only: pricing guard reads money by type, exemption keyed on a declaration |
| 65 | dc1b3f0c | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Proposal print: clear the pending flag when flushSync throws (MPSCALC-385) (#1 |
| 66 | 31234f5f | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Test only: pricing guard follows destructured, wrapped and carried money forms |
| 67 | 94b24e8b | 1 (src 0, web 0, tests 0, docs 1, ops 0) | no | none | Importer doc: the Not in this lane lifecycle line now points at the API Source |
| 68 | 089a6393 | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Template isolation test: the format guard reads a format after a literal or ne |
| 69 | 8d665e3f | 5 (src 0, web 0, tests 0, docs 0, ops 5) | no | none | Infra and script follow-ups: Bicep tests never call az, Entra group checked fi |
| 70 | 97cf7a9a | 5 (src 3, web 0, tests 2, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | Source lifecycle: lock waits hold no thread; canonical-singleton marks in ids  |
| 71 | 3a7a8048 | 10 (src 5, web 0, tests 5, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | Feedback backend hardening: overlap guard, retry race, download headers, uploa |
| 72 | c5cd009a | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Draft save refusal order: pin body checks before lookup and owner before state |
| 73 | 0b9aad04 | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Web tests: six slow BOM and price-reason rows type without timers and carry a  |
| 74 | dad90244 | 10 (src 3, web 3, tests 2, docs 2, ops 0) | no | contract/stored-shape member | Purchase result: recurring projection for internal-metrics callers; result qua |
| 75 | 54ed7627 | 3 (src 0, web 2, tests 0, docs 1, ops 0) | no | none | API.md: lifecycleEvents refusal, feedback limit and order sentences; generated |
| 76 | 5cd6002f | 1 (src 1, web 0, tests 0, docs 0, ops 0) | no | Pkcs pin (package content) | Raise the pinned System.Security.Cryptography.Pkcs to 10.0.15 so the deploy pa |
| 77 | acd6aec0 | 15 (src 7, web 0, tests 8, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | API stores: streamed feedback uploads, stage bound from arrival, repeated supp |
| 78 | 9a0c4ba8 | 1 (src 0, web 0, tests 0, docs 1, ops 0) | no | none | Engine register: add X-33 (page and margin refusals) and X-46 (colour-panel ki |
| 79 | aae420ff | 18 (src 0, web 17, tests 0, docs 0, ops 1) | no | CI workflow | Web: Playwright listing fixed and run in CI, print style fixes, unreadable fee |
| 80 | c7f5202e | 1 (src 0, web 0, tests 1, docs 0, ops 0) | no | none | Draft validation: pin the answer size of the supplies-null walk at the cap, no |
| 81 | 37656d8a | 6 (src 0, web 6, tests 0, docs 0, ops 0) | no | none | Web look and print fixes: site cards past Z, one-rate wording, home tiles thre |
| 82 | 893a3f29 | 14 (src 0, web 0, tests 0, docs 0, ops 14) | no | deploy tooling | Ops tooling: proven deploy start, overlay re-read, validate.sh without az, Ent |
| 83 | 454b5c6b | 3 (src 0, web 0, tests 0, docs 1, ops 2) | no | SDK pin (build only) | Pin the .NET SDK exactly (global.json 10.0.404, rollForward disable) |
| 84 | baf0aabe | 3 (src 1, web 0, tests 2, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | Source version ids: accent spellings with U+0344, two marks or marks in anothe |
| 85 | 793d0a9c | 4 (src 1, web 0, tests 3, docs 0, ops 0) | no | stricter LOAD rule (start-refusal class, Step 3f) | Make two flaky Api test rows deterministic: test host and feedback hourly limi |
| 86 | 52390202 | 4 (src 0, web 4, tests 0, docs 0, ops 0) | no | none | Rental short proposal: cap device lines at 5 so it prints one A4 page, with a  |
| 87 | 1515a71d | 11 (src 2, web 3, tests 3, docs 3, ops 0) | no | stored default (7% rebate) | Store the 7% rebate default for callers without pricing rights; Duplicate keep |
| 88 | 286795d7 | 4 (src 0, web 2, tests 0, docs 0, ops 2) | no | none | SDK pin guard: close the quoted-key, env, install-script and nested global.jso |
| 89 | 50c354ff | 4 (src 0, web 4, tests 0, docs 0, ops 0) | no | none | Rental short proposal: cap devices at 3 and each option table at 2 rows, with  |
| 90 | 3fb06085 | 2 (src 0, web 2, tests 0, docs 0, ops 0) | no | none | Override minimatch to 11.0.1 under typescript-estree (web manifest and lockfil |
| 91 | 0bb3ed12 | 10 (src 0, web 3, tests 0, docs 0, ops 7) | no | deploy tooling | Operator wording for deploy and seed dry run (MPSCALC-392); Home tiles never l |
