STARTABLE: YES (after Tuesday stamps the seven slot lines and the last line, all four underscores; launch through launch_when_cool with BRIEF_SEAT_LEVEL=sonnet inside the quotes; expect a long wait: load averages 7.5 to 12.6 while the engine builder runs mutants)

# B1070 DRAFTER REPORT - SEAT-G265 tier-2 QA gate of B1063 (MPSCALC-317, Add section waits for the price list, web)

Drafted 2026-11-01 23:30-23:55 AEDT by a read-only drafter. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1070_SEAT-G265_mps-317-add-section-gate-tier2.md` (32 lines, 57 KB; 8 four-underscore lines = 7 stamp slots + the last line; 0 non-ASCII bytes).

## BLUF
- A tier-2 web gate kit (G2, `model-routing.md:109`; G-cap `:111`) for branch `b1063/mps-317-add-section-waits-for-price-list` @ `35996bc106e70fb82cf84e351bd56214ff7beb9a` on main `3496da33ab3d7d2c6b7d7ec2c3014ae03518e020`. **Round 1 of 2 on class "web: Add section waits for the price list", NO GO 0 before** (70 `GATE VERDICT` first lines, 0 match; control 1). Seat `Datasec/MPS-G265`, Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes. Ports: none bound (reserved block 9780-9789, free).
- The kit makes the gate settle your seven points: (1) the ticket's two Done-when clauses against its own hand rows H1-H11 written before it reads the builder's tests, including the six-click row three ways and a click after the answer; (2) the failed-read row and the never-answers row, graded (never-answers is Minor by the kit's SEVERITY: finding for the product owner, no word written); (3) its own mutants GW1-GW12, GW5 (= MW5) proved or refuted by call-site census plus DOM and React-props paths, and MW11 measured by run count per load band AND by injected read latency (the instrument that stands for load); (4) the edited endActions row (+1 -0) and the whole suite at least 6 runs at head, 3 at main; (5) Node; (6) no-word, HOLDS and hygiene counts and the 12-sentence commit message; (7) the four squash files, with a program check that no "NOT TESTED", "hosted CI" or "CodeQL" line survives into the squash body.
- Two things I found by reading the head that the builder STATUS does not say, both put into the kit as things to measure: (a) while the read is pending, a pricing-eligible caller already sees, at main too, the pricing note whose second sentence reads "The server has not granted them to this sign-in." (`PurchaseBomEditor.tsx` :211-226, constants :24-27), so a never-answering read shows a disabled button beside a misleading existing note; (b) `web/src/api/client.ts` `call` passes no `signal` to `fetch` (0 hits), so only the browser or a proxy ends a stalled read. Also: a section added after a failed read has a DISABLED Rebate field (`disabled={!pricing}`, :320), not just no default.

## Facts re-measured (instrument; control)
- Remote (`gh api -X GET`, project `GH_CONFIG_DIR`, account active, ssh), 23:3x-23:50:
  - main `3496da33...`; `compare 3496da33...main` 0 files (unmoved); `matching-refs/heads/b1063` 1 ref at `35996bc...` (control `heads/b10` 61); `ls-remote origin` in `2_Project_Files` agrees.
  - `compare 3496da33...35996bc`: ahead 1, behind 0, 5 files: `QuoteScreen.addSectionWait.test.tsx` +161 -0, `QuoteScreen.endActions.test.tsx` +1 -0, `QuoteScreen.tsx` +7 -2, `PurchaseBomEditor.addSectionWait.test.tsx` +142 -0, `PurchaseBomEditor.tsx` +8 -2; sum +319 -4, equals the builder's.
  - Parent `3496da33` only; `verification.verified` false; open PRs 121 and 120 (dependabot, `web/package-lock.json` only each); PRs for the head branch 0; `actions/runs?head_sha` total 0; squash settings COMMIT_OR_PR_TITLE / COMMIT_MESSAGES.
  - `ci.yml` blob `212b0da1...` at head and main. `on:` push to main, pull_request, workflow_dispatch; no deploy job (line 1 says so; the package job only keeps an artifact on main).
- Commit message read whole: subject 55 characters, 12 body sentences by a split at a full stop followed by a capital (python `re.split`, printed), one trailer `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`, 0 non-ASCII. The #136 squash on main `3496da33` holds "NOT TESTED: hosted CI and CodeQL." once (control for the stale-line check).
- Jira GET (GET-only reader, project `.env` read in process, no token printed): `project = MPSCALC AND ( key in (MPSCALC-317, MPSCALC-99999) )` returned 1 issue (the absent key is the control). MPSCALC-317 Backlog, labels `lane-v0 mpscalc-b509 plan-b509-b483-q8 tier-2`, 0 links, 0 comments, updated 2026-10-23. Acceptance check text read whole and quoted as clauses 1 and 2 in the kit.
- Source at the head (raw `contents?ref=35996bc`): read effect `[api, purchase]` with rejection handler `(setInventoryFailed(true), setCatalogueError(e))`; `onAddSection` referenced once (the button `onClick`, :178; control `zzz-no-such-string-7f3a` 0); `App.tsx:20` keys `QuoteScreen` on quote id and persona; `main.tsx:17` `<StrictMode>`; `fakeApi.tsx:34` default `listInventory` answers `internalMetricsIncluded: false`; `web/package.json` `test` = `vitest run`, `lint` = `eslint .`, `build` = `tsc -b && vite build`, `engines.node` `>=20.19.0`. Files mentioning `Add section` under `web/src`/`web/e2e` (blob census, 666-entry tree): 7 existing unit test files, 2 new, 8 e2e specs.
- Round census: bash loop over the project `Briefs/*_STATUS.md`, first lines starting `GATE VERDICT` (case-insensitive): 70; hits on `add section|price list|b1063|35996bc|MPSCALC-317`: 0; control `purchase recurring projection`: 1 (B1051).
- Seat name and number: `G265` and `B1070` absent from the 101 non-`.pre-` SEAT kits of 10-31 and 11-01 (and from the B1068/B1069 kits); control `G260`/`B1051` 3 files. Project `Briefs/` `B1070`/`G265`: 0 (control `B1051` 3). `.tools` names `b1070|g265`: none (control `b1063` lists 3). `.tools/.git-lock` absent. `heavy-slot-1` existed at 23:34 (holder `B1062 ... mut-MQ16`) and was gone at 23:50.
- Ports: `lsof -nP -iTCP:9780-9789 -sTCP:LISTEN` 0 rows (control: unrestricted listing 18 rows at 23:30, 16 at 23:50). `-w -E '978[0-9]'` over 101 kits: 0 files (control `976[0-9]` 2 files).
- Panes 23:43: `%0 tuesday`, `%17 NexusAI-G264`, `%16 HPSM-POC-R121`, `%15 MPS-R120` (launched since I started), `%14 Security-Composer-G263`, `%11 MPS-M66`, `%10 HPSM-POC-H93`, `%2 Security-Composer-J38`, `%1 fleet-monitor`. No `Datasec/MPS-G265`.
- Node: `which -a node` only `/opt/homebrew/bin/node`; v26.8.1, npm 11.19.0; Cellar and opt hold `node`/`node@26` only; nvm, fnm, volta, asdf, `/usr/local/n`, `~/n` all absent; `brew` 7.0.9. The one Node 24 on disk is `.tools/b75/node-v24.21.0-linux-arm64.tar.xz` and its unpacked `node-arm64/bin/node`, `file` reads ELF aarch64 GNU/Linux (cannot run on this Mac; another seat's tree). Docker forbidden.
- Model: `models_latest.json:23` `levels.sonnet.model_id` = `claude-sonnet-5-5` (`:17` opus is `claude-opus-5-5`); `brief_seat.sh` line 24 defaults to opus, level read from `BRIEF_SEAT_LEVEL`; `launch_when_cool.sh` header: `usage: launch_when_cool.sh <cockpit name> <command string for cockpit.sh add>`, waits for load1 below 7 on two reads 20 s apart, 120 s spacing, one waiter.
- Landing rule lines: `CLARIFICATIONS.md:758` ("LANDED #91 by squash --match-head-commit 5295ff7a (MPS convention)", "Not deployed (MPS hosted is card-per-deploy)") and `:774` ("squash with the head pinned (`--match-head-commit`, the MPS convention ...)") read at 23:4x; C-79 heading at `:1712`; C-46 question 8 at `:889`.
- Builder STATUS: 167 lines, last line the READY line for `35996bc...`, `## PRIOR WORK (Step 2, base 3496da33)` at line 56.
- Kit hygiene: four-underscore lines 8 (control: the stamped B1063 kit 0); non-ASCII 0 (python byte count); person-name tokens 0 except the GitHub login `kamilDatasec` (see Q-6); decision-card ids 0 (two hits are the words "decision-card id" in rule text).

## REFUSE and STOP lines tested now (each against what is live and installed)
- RF four-underscore count: kit reads 8, control stamped B1063 kit reads 0. PASS (correct pre-stamp state: it would refuse this unstamped copy, as designed).
- RF last line / `## Stamp`: last line is `READ-WHOLE-BY-TUESDAY: ____` (would refuse unstamped, correct); control B1063 stamped last line starts `READ-WHOLE-BY-TUESDAY: DONE`. PASS.
- RF pane: 0 panes named `Datasec/MPS-G265`; control `-t %0` prints `tuesday`. PASS.
- RF head moved: `ls-remote` prints `35996bc106e70fb82cf84e351bd56214ff7beb9a`. PASS (not moved).
- RF PR exists: 0 for the head branch. PASS.
- RF main moved: `compare 3496da33...main` 0 files; control `compare 3496da33...35996bc` 5 files. PASS.
- RF `.tools/b1070`/`wt-b1070-*` exist: 0; control `b1063` names 3. PASS.
- RF builder last line: the `READY FOR QA: B1063 ... @ 35996bc...` string matches 1; control wrong sha 0. PASS.
- RF PRIOR WORK present: line 56; control absent heading 0. PASS.
- RF `gh auth`: account `kamilDatasec` active, 1 match. PASS.
- RF model: line 23 `claude-sonnet-5-5`. PASS.
- RF versions: node v26.8.1, npm 11.19.0, gitleaks 8.30.1 all print. PASS (and Node 26 is NOT a refuse, by design).
- RF MPSCALC-317 Backlog, 0 comments, 0 links: re-read at 23:43. PASS.
- RF `records/*` in the code repo: 0; control `main` 1. PASS.
- STOP listener: block 9780-9789 0 rows. PASS (nothing to stop on). STOP git lock: `.tools/.git-lock` absent. PASS.
- NOT testable now: the "security-shaped finding you cannot classify: STOP" line, the STOP on a dirty mutant tree, the 15-minute lock poll, and the PR-exists-then-add-checks branch (no PR, no tree, no lock yet); they are behaviours of the running seat.

## D-decisions
- D-1 Shape: tier-2 trim of the B1051 tier-1 kit (steps 1-7) with the B848 web-hold gate as the web shape. Dropped as not applicable: byte-equal rebuild across serializers, sweep, reconciler, dotnet CI line. Added: Node statement, hand rows H1-H11, failed-read and never-answers steps, MW11 measurement by injected latency, whole-suite runs.
- D-2 Hand rows are written before the seat reads the builder's two new test files (the seat may read the source diff and the existing test helpers first). Mutants are named GW1-GW12 (the builder's MW1-MW11 map: GW1-GW4, GW5=MW5, GW6-GW9, GW10=MW10, GW11=MW11, GW12 new: only the top copy held).
- D-3 Clause 1 is graded by the builder's SECOND branch ("not offered until the price list has loaded"); the failed-read case is a Note carried as the stamped residual unless the seat finds the hold ends while the read is pending or a wrong rebate, in which case Major.
- D-4 SEVERITY puts "never answers, disabled button, no explanation" at Minor (the ticket's own second branch; no word added on purpose) with a finding for the product owner and a prose fix-shape that writes no word.
- D-5 Suite proof: at least 6 whole-suite runs at head and 3 at main; each of the seven existing "Add section" files 10 runs; the edited row 20 runs by the builder's addendum is re-measured only through MW11's 30 runs plus the with-wait 30.
- D-6 Heavy slot: any free of `heavy-slot-1..3`; the engine builder may hold slot 1 (it did at 23:34).
- D-7 Squash body: program check that `NOT TESTED|hosted CI|CodeQL|not run` count is 0; trailer must equal the head commit's own (Claude Sonnet 5.5), not the Opus line of the B1051 template.
- D-8 Gate time: target 2 hours, hard stop 4 hours after Step 0 (suggested; Tuesday stamps).

## Q for Tuesday (each with a default)
- Q-1 Gate tier: G2 as the builder kit stamped (the change is not tests-only but it is a follow-up whose mechanism the B457 probe measured; the ticket is labelled `tier-2`; nothing deploys; no security surface). Default G2. If you read the 7 percent rebate default as a "money surface" you hold at G1, the kit's launch line changes to Opus.
- Q-2 Install a Node 24 for the seat? Default NO. No Node 24 runs on this Mac; installing one is a machine change that is not the seat's. The kit says the hosted web job judges on Node 24 and the local run is v26.8.1 (the B1063 ADDENDUM-1 precedent).
- Q-3 Words question for a held button with no explanation: default is the kit's: a Minor finding for the product owner with the exact page text; the seat writes no word.
- Q-4 PR title and squash subject may carry MPSCALC-317 (both bodies may not), as at B1051. Default YES.
- Q-5 Whether a dependabot lock-file PR (#120 or #121) landing first should force a re-run of the web job: the kit asks the seat to say what merging either first means; default: the hosted job at the head judges, no gate re-run.
- Q-6 The GitHub login `kamilDatasec` appears in the kit twice (the REFUSE check for the project account, as the B1063 kit has it). Default: keep it (a handle, needed for the check); it is not copied into commits or comments.
- Q-7 R120 launched at 23:43 beside M66. The kit says R120 never touches MPSCALC-317 or -253 (its own kit excludes them) and never `2_Project_Files`. Default: no action; if R120 later records the 317 Done move it does so after the merge, not before.

## UNMEASURED
- Everything runtime: no test, lint, build or mutant was run by me. The never-answers and failed-read behaviours are read from source, not exercised. Whether `check-bundle.mjs` needs the working directory (it takes `dist` from `process.argv`). The real read latency on the hosted site (fenced). Playwright behaviour on a disabled button (e2e not a CI step). Whether the whole web suite has skipped tests at main (the kit asks the seat to record skipped at both). The B1063 builder's own load figure (about 14) is its claim. Whether `waitFor`'s default timeout is overridden in `web/src/test/setup.ts` (the kit asks the seat to read it).

## Outside-the-fences disclosure
- I wrote only the two files named. One command of mine was refused by the no-`cd` hook (a `cd /tmp` I typed at the start of one scan loop); the call did nothing and was re-issued without it.
- I wrote scratch files in the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/e425ac47-23fd-4e01-8dc9-817758c59316/scratchpad/` with prefix `b1070_` (a GET-only Jira reader `b1070_jira.py`, raw source copies, tree list, commit message). The scratchpad also holds other drafters' files; I read none of them except noting that `jget.py` of the B1067 drafter exists and I did not import it. The Jira token was read in process and never printed.
- I read the B1063 and B1062 STATUS files (B1062: the first 600 bytes and last 2 lines only, to see that M66 is working), the B1062 and B1067 kit partition and holds sections, the B1067 drafter report, and `.tools` directory listings by name (and `file` on one unpacked Node binary under `.tools/b75/` to prove it is a Linux ELF). I opened no builder worktree and no other seat's tree contents.
- No decision_queue call, no briefs_staged, scoreboard or ledger, no WEDNESDAY or FRIDAY tree, no non-Datasec project, no mail, no Artifact, no write to Jira or git, no HTTP to any hosted app host (GitHub API and the Jira API GETs only).

STARTABLE: YES
