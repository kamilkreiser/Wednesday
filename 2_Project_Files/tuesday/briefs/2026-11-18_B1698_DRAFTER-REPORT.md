STARTABLE: YES (at main b746cb92d541a65ee4bb2120334249c20c2a60b8; one practical wait: heavy-lock slot 1 was held by gate B1697 at 09:08, and the kit makes the seat do the dotnet step last)

Drafter: Sonnet 5.5 Agent-tool drafter for Tuesday. Clock: started 09:06:43 AEDT, kit and sidecar finished about 09:14 (`date` reads: 09:06:43, 09:06:50, 09:07:49, 09:09:00, 09:13:14). Files written: the kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1698_SEAT-M158_mps-lane-m-d3-source-version-unique-clause.md`, its sidecar `.measured` (97 lines, all filled), this report; scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1698/`.

## BLUF
- Lane M-D3 (MPSCALC-410) is startable at main `b746cb92` (#211 is on it): TWO replacements (E1 `docs/API.md:708`, E2 inside `docs/api/openapi.json:751`), TWO commits (commit 1 the two hand edits, commit 2 the three generated files by `web/scripts/sync-contract.mjs` only), five changed paths, push only, same shape as the staff-column lane that landed today.
- The ruling is verified by the READ verb: the card reads `ruling: choice='a'` at 2026-11-18T08:38:02+11:00, with the text "Yes to all three: contract changes with the docs; 195 recorded as agreed; 207's three words added with a test". Items 2 and 3 (195, 207) are OUT of this lane and the kit says so.
- The clause is wrong in both directions, as the ticket says: the code (`SourceDocumentChecks.cs:82-94`, `:406-407`) counts every state except `Draft`, `Failed Validation` and `Expired`, so `Validating`, `Active`, `Superseded` AND an unknown state word count; a `Draft` or `Expired` version "did not fail" yet does not count.
- Model row C2 (`model-routing.md:92`), gate G2 (`:109`), model id `claude-sonnet-5-5` (`models_latest.json`, sonnet entry), launch level `sonnet` inside the quotes.

## THE FROZEN WORDS
- E1 `docs/API.md:708` (count 1 before, 0 after). OLD: `across every governed version that did not fail;` NEW (two lines, second with the two-space indent):
  `across every governed version in the state `Validating`, `Active` or `Superseded``
  `  (or in a state word the server does not know); a `Draft`, a `Failed Validation` and an `Expired` version do not count;`
- E2 `docs/api/openapi.json:751`. OLD: `across governed versions that did not fail)` NEW: `across governed versions in the state Validating, Active or Superseded, or in a state word the server does not know; a Draft, a Failed Validation and an Expired version do not count)`
- Source of each word (printed with awk NR== at main): `SourceDocumentChecks.cs:82-85` (`others` = other versions where `CountsAsDuplicate(g.State)`), `:86-94` (`seen` set plus `others`, issue `DUPLICATE_SOURCE_VERSION_ID`), `:406-407` (`state is not (SourceStates.Draft or SourceStates.FailedValidation or SourceStates.Expired)`), the doc comment `:399-405` ("an unknown state fails closed"), `SourceGovernance.cs:11-16` (six state words), pinned by `SourceLifecycleTests.B520States.cs:47-54` (`Retired`, `validating` count), `:56-64` (Draft, Failed Validation, Expired do not), `:66-` (Validating, Active, Superseded do).

## Facts re-measured with instruments
- Main by `gh api -X GET .../git/ref/heads/main` = `b746cb92d541a65ee4bb2120334249c20c2a60b8` (09:06:50); compare to main `0 0`; open PRs 0; `matching-refs/heads/b1698` 0 rows (control `heads/b1671` 1 row).
- MPSCALC-410 read whole by my own GET-only helper (`jira_get.py` in the scratch; credentials in-process): Backlog, updated 2026-11-17T15:35, label records-pass-1117, **0 comments**; control `key = MPSCALC-361` printed Done (every JQL `project = MPSCALC AND ( ... )`). Its Recommendation text is the source of the unknown-state clause.
- Old-phrase census (the "tests or generated files that pin the OLD clause text" ask): `grep -rl -i -F 'did not fail'` over the whole extract = **4 files**: `docs/API.md:708`, `docs/api/openapi.json:751`, `web/src/api/generated/openapi.snapshot.json:751`, `web/src/api/generated/schema.ts:774`. All four REWRITE (two by hand, two by the generator); `SOURCE.txt` carries only the hash line and changes with the sync. **0 test files** hold the phrase; **no test reads `docs/API.md` as text**; the contract is read as data only by `Contract.cs:15` (shapes) and the web tests `contract.sync.test.ts` and `contract.test.ts` (bytes and sha256). The code-side tests (`B520States.cs`, `B105.cs`, `Stage.cs`) are UNAFFECTED (no code changes). Control for the grep: it prints the four rows; the positive control phrase `every source version id` reads the same four files (1 1 1 1, SOURCE.txt 0).
- **Red/green MEASURED in my scratch** (tarball of main + a scratch git repo with a scratch identity; Node v26.13.0; deps by `npm ci --offline --ignore-scripts`, from the local npm cache, 0 vulnerabilities; `npx openapi-typescript --version` v7.13.0): base `Test Files  2 passed (2)`, `Tests  4 passed (4)`; after the two hand edits `Test Files  1 failed | 1 passed (2)`, `Tests  1 failed | 3 passed (4)` (row "the snapshot is byte-identical to docs/api/openapi.json", 227631 vs 227492 bytes); after `node scripts/sync-contract.mjs <scratch commit 1>` `Tests  4 passed (4)`, `cmp` rc 0. Hand edits `git diff --stat`: 3 insertions, 2 deletions (`docs/API.md | 3 ++-`, `docs/api/openapi.json | 2 +-`); generator output exactly 3 files, 6 insertions, 6 deletions (SOURCE.txt 2 lines, snapshot 1, schema.ts 3: two header lines and the one `@description`). Added hand-edit lines: 0 non-ASCII; `json.load` ok; `git diff --check` rc 0.
- Phrase table (columns API.md, openapi.json, snapshot, schema.ts, SOURCE.txt; `grep -c -i -F`): `did not fail` base 1 1 1 1 0, after sync 0 0 0 0 0; `a state word the server does not know` base 0 0 0 0 0, after 1 1 1 1 0.
- Disjointness (both sides, `gh api -X GET compare`): b1671 (head `7e4845b2...`, diverged 1/1) touches ONLY `src/MpsCalc.Import/PriceBookImporter.cs` and `tests/MpsCalc.Import.Tests/PanelSectionEndTests.cs`; my five paths are `docs/API.md`, `docs/api/openapi.json` and the three generated files: 0 shared. A stale ref `b1693/mps-lane-m-d5-stale-v2-text` (c69c4a8c, diverged, ahead 1: `docs/API.md` and one test file) is the pre-squash branch of the lane that landed as #211; its line is `:379`, mine `:708`.
- Toolchain by path: dotnet `10.0.404` at `<project>/.tools/dotnet-10.0.404/` (printed); the project has NO drive-local node (0 names with `node` under `.tools`; control 3 names with `dotnet`); machine node `/opt/homebrew/bin/node` v26.13.0; CI Node 24 (`ci.yml:58`).
- CI predicate: `ci.yml:42` `dotnet build MpsCalc.slnx -c Release`, `:43` `dotnet test MpsCalc.slnx -c Release --no-build`, `:61-63` `npm ci`, `npm run lint`, `npm test`. Landing rule from the project `CLAUDE.md:50-51`.
- Machine: load 8.25 at 09:09 (12.96 at 09:13 after my vitest runs and others), 1081 GiB free, ports 9970-9979 0 listeners, 0 `Datasec/MPS-` panes, `gh` Datasec account active, git email domain Datasec. **Heavy slot 1 held at 09:08 by a gate (holder file `gate-B1697 G2 verify`, 09:06:32).**

## Inputs table (rule 4: every step's inputs and where each comes from)
| Step | Inputs | Produced by |
|---|---|---|
| 1 setup | base sha, SSH remote, deploy key, `npm ci` output | exist at BASE / Stamp S2; `node_modules` made in step 1 |
| 2 predictions | FACT 5 numbers | exist in the kit |
| 3 base measures | clone, `node_modules`, five paths | step 1 |
| 4 pre-edit reads | `SourceDocumentChecks.cs`, `SourceGovernance.cs`, `docs/API.md`, `openapi.json`, `B520States.cs` | exist at BASE |
| 5 commit 1 | the two hand paths, frozen strings, JSON | exist at BASE |
| 5(f) dotnet | built solution, heavy slot, edited contract | step 5 edits; slot per HEAVY |
| 6 commit 2 | commit 1's 40-hex sha, `node_modules`, generator | commit 1 (step 5(g)); step 1 |
| 7 checks | both commits, five-path list, ban list in the gate-verifier standard step 7 | steps 5-6; the standard file exists |
| 8 push | both commits, deploy key | steps 5-7 |

## D-decisions
- D1: **two commits**, hand then generated, because the sync reads the contract from a committed ref (the template lane's shape).
- D2: **the unknown-state clause is IN** (the ticket's Recommendation names it; the code comment `:403-404` states it; `B520States.cs:47-54` pins it). E1 and E2 use the same words.
- D3: **one dotnet run only**, after commit 1 and last in the order (the lane edits no code; the Api tests copy the contract and parse it, so the whole-solution run is the check that the edited contract still loads). No base dotnet run.
- D4: the kit does NOT touch `docs/API.md:713-716` (the case-and-accent paragraph), which is true and adjacent.
- D5: the clause is a developer sentence about an Administrator-only operation, so no customer-visibility hold; the seat measures the 4-file spread of `did not fail` anyway (step 4(b)).

## Q-questions for Tuesday (each with a default)
- Q1: keep the words `or in a state word the server does not know` in the sentence? Default IN (see D2). If OUT, E1 and E2 lose that parenthetical and the sentence is then narrower than the code by exactly the unknown-state case the ticket asks to name.
- Q2: gate tier G2? Default G2 (docs, a contract description, generated copies; same as B1689).
- Q3: other stale text seen, reported and not edited? Default report only. I saw none new in this clause's neighbourhood; the paragraph's other sentences were not audited.
- Q4: `npm ci` in the seat's own clone allowed? Default yes (the same restore the hosted web job does).
- Q5 (timing): heavy slot 1 is held by a gate; the kit says to take the slot last. Default launch when you want; no change to the kit.

## UNMEASURED / NOT RUN
- `npm test`, `npm run lint`, `dotnet build`, `dotnet test` (the heavy slot was held; I took none). The kit's expected counts for those are RELAYED from the earlier lane's STATUS (Engine 743, Import 196, Api 3663 at its base) and marked as such.
- A Node 24 reading of the generator (CI's version); mine ran on Node 26.13.0.
- gitleaks (not run by me); the git-identity line (I made no commit in any project repo; the scratch repo has a scratch identity).
- The seat's SOURCE.txt/commit-sha values differ from mine (my scratch commit sha `2516dfaf...` is not meaningful to the seat).

## Outside-the-fences disclosure
- No write outside my two files, the `.measured` sidecar and `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/d1698/`. I read the card with `decision_queue.sh show mps-410-openapi-195-wording-1117` into a scratch file in the session scratchpad and filtered it by the id and its ruling lines; no add/rule/amend/withdraw, no `list`.
- Hosted/network use: `gh api -X GET` only (main ref, matching-refs, pulls, compare, the tarball of main) under the project `GH_CONFIG_DIR`; Jira GETs by my own helper; `npm ci --offline` read the local npm cache (no registry call). Two `ls` reads of a project folder: `<project>/.tools` names and `HPSM-POC/.tools/node*` (to measure the `node24` name, a read of a listing only); and one read of `.heavy-lock-1/holder.txt` (read, not touched).
- One mistake, contained: my first command line contained an `rm -rf` of a scratch path that did not exist; the hook refused it before it ran. Nothing was deleted anywhere. I did not use `cd`.
- I read the earlier lane's kit, STATUS and gate VERDICT as the template; I opened none of the fenced files (`briefs_staged/`, `scoreboard.md`, `_ledger.md`, WEDNESDAY/FRIDAY trees).

Paths: kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1698_SEAT-M158_mps-lane-m-d3-source-version-unique-clause.md`; sidecar the same name plus `.measured`; this report `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1698_DRAFTER-REPORT.md`. `stamp_check.py <kit>` exits 0 (97 claims, 97 measured).
