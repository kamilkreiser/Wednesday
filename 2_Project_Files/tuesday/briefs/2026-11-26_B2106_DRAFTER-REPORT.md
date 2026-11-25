STARTABLE: YES for MPSCALC-233, 316 and 120. MPSCALC-195 is NOT in the kit (its engine-target sentence is on no record: Q1, a STOP-class question with a default). Seat id M176 (free by scan). Drafted 2026-11-26 04:59 to 05:30 AEDT (`date`).

## BLUF
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-26_B2106_SEAT-M176_mps-l1-api-refusal-docs.md` (468 lines), its sidecar `.measured` (152 lines, 152 measured, `stamp_check.py` exit 0), this report. Base main `56f508a779ea5add1655d1c8a824cde635d6a53c`; branch `b2106/m176-mps-l1-233-316-120`; TWO commits (contract commit, then the regenerated `web/src/api/generated/**`, the project's own `contract.sync.test.ts` demands two); eight paths; Sonnet (row C2), gate G1 Opus; nothing deploys; no new word reaches a customer.
- Every edit is frozen in ONE script (`apply_edits_l1.py`, in the kit) and was prototyped on a copy of main with the project's own `.tools/dotnet-10.0.404` and node 24: red at base (10 of 146 filtered cells, the five N cells that must fail, once per host), green at head (146 of 146), whole Api project 3681 passed (base 3663 = the figure the pull request 218 review read), two mutants killed (no lock: N8; case-folding match: N6), Release build 0 warnings, whole `vitest` 149 files 1742 tests, `eslint` and `tsc -b` rc 0, `sync-contract.mjs` run and `contract.sync.test.ts` plus `contract.test.ts` `Tests  4 passed (4)`. The kit's own script blocks were extracted from the kit and re-run: same five blobs.
- Three findings Tuesday must read before the stamp: (1) 195's sentence is absent and the sweep's pointer (`B158_STATUS.md:233`) is the rate-limit row; (2) the docs now say the OPPOSITE of the ruling (`API.md:441` and `openapi.json:369` say quoteRef is not unique), so 233 must replace those sentences; (3) the stub's Duplicate rule lives in `purchaseQuotes.ts`, not in the `stubApi.ts` branch the sweep lists, and is left out of the lane by default.

## Facts re-measured (instrument; control)
- Main `56f508a7`, open pull requests 0, `matching-refs/heads/b2106` 0 rows: `gh api -X GET` under the MPS `GH_CONFIG_DIR` (account read: the Datasec account; control `heads/b1901` 2 rows) at 04:59:22. Newest landed PR 228 opened and merged by the same account as 227 and 226 (landing record for Q3).
- Pull requests naming the keys: `gh api -X GET search/issues` per key: 233 in 85 only (control: finds the known build PR), 316 in 218, 120 none, 195 in 105, 175, 202.
- Tickets (Jira GET, in-process token): 233, 316, 120, 195 all Backlog; comment counts 5, 5, 1, 7 and newest ids 41083, 41400, 41091, 41374; control `MPSCALC-361` reads Done. 316 still carries `needs-ruling`.
- C-119, C-125, C-108, C-64 quoted from `1_Project_Definition/CLARIFICATIONS.md` by `grep -c -F` (each quoted sentence 1 hit).
- `docs/api/openapi.json` `info.version`: read at 36 commits (`gh api -X GET .../contents/...?ref=<sha>`, raw): 18 read `0.9.0-b103`, so the contract changed 17 times after it with no bump (control: the oldest reads `0.1.0-lane2b`). Drives Q8.
- Source pointers: `grep -n -F` over the tarball of main (list in kit FACT 3; `facts_lines.txt` in scratch). Blob of `openapi.json` at main `7796e611...` equals the blob `SOURCE.txt` names (cross-check).
- Prototype runs (copy of the tarball, `git init` in the session scratchpad because the Api host needs a git work tree; first run outside one failed with `Start refused ... (git-ignored)`, now in the kit): `V0_N` filter on head 20 total (18 new + 2 `V0_no_body`); `V0_` filter head `Passed: 146`; E3 alone `Failed: 10, Passed: 136, Total: 146`; whole Api `Passed: 3681`; mutants m2 and m3 each `Failed: 2, Passed: 18, Total: 20`; Release build `0 Warning(s)`; `scans2106.py`: 162 added lines, 2 non-ASCII (the generator's middle dot), 0 Cf, 0 GUID, 12 names quiet and 12 controls fired; path check: exactly the 8 paths differ (+ git-ignored `.local/` made by the Api tests; control: a planted ninth file makes the count 9); gitleaks canary rc 1 then the eight files rc 0; the two commit messages: 0 name hits, 12 controls fired, subject 109 characters.
- Seat id: no SEAT kit of `tuesday/briefs` holds `M176` or `B2106` (word-boundary scan, control `M175` in 9 files); the report of kit B2047 names M176 as its NEXT FREE id (a held kit): if B2047 starts first, one takes M177. No `Datasec/MPS-` pane, no `.tools` entry named b2106 or m176, no heavy or git lock.
- Model: the project `CLAUDE.md` holds no `opus`, `sonnet` or `model` (`grep -c -i` 0, control `friday` 4), so row C2 decides (`model-routing.md:92`); id `claude-sonnet-5-5` at `models_latest.json:23`; `brief_seat.sh:31` defaults to Opus (launch line carries `BRIEF_SEAT_LEVEL=sonnet`). Gate tier proposed G1 (`model-routing.md:108`).

## D-decisions (mine; the kit says each is Tuesday's choice at the stamp)
- D1 195 out of the kit. D2 the refusal answer is the existing 400 `BAD_REQUEST` with the existing headline `The draft is not valid.` and no `errors` entry, so no new word exists to wait on a words card (kit builds the mechanism; the owner's sentence replaces one literal later). D3 only a TYPED reference is refused; derived `-COPY` is not (the ruling says "typed"; the existing cell at `V0Duplicate.cs:160` stays green). D4 exact ordinal match against every stored quote's current version (any Seller or Approver can already read every quote and reference, so no new disclosure). D5 one new method `QuoteStore.AddIfRefFree` under `_refLock` so the look and the add are one step; no lock-order cycle (DERIVED) and cell N8 kills the no-lock mutant. D6 no stub file, no e2e file. D7 316 adds the agreed unit sentence as a `description` beside `maxLength` 100 in the two schema places; the keyword is untouched. D8 120's section states the ruled rule plus the measured list of the nine version values and does not invent exceptions. D9 `info.version` not bumped. D10 two commits.

## Questions for Tuesday (each has its default in the kit; Q1 and Q3 are STOP-class and must be answered in Stamp S5)
- Q1 195: default OUT, ask the product owner for the sentence. Do you have its text? If yes, S5 quotes it with source and `docs/ENGINE.md` joins as a ninth path.
- Q2 level: default sonnet (C2). Q3 who lands: default the seat pushes, Tuesday opens and lands (the project file names another seat; the last three landings say otherwise).
- Q4 stub: default untouched; alternative adds `purchaseQuotes.ts` and `stubApi.test.ts` (note the stub trims, the server does not).
- Q5 typed only (default) or derived too. Q6 words: default existing headline, no entry; a drafted interim sentence is in the kit for you to put to the owner.
- Q7 exact match (default). Q8 no version bump (default). Q9 two commits (default). Q10 G1 Opus (default). Q11 does C-108 reach the two schema places of 316: the 2026-11-20 note says "not ruled", the commission says reached; default build the descriptions.
- Q12 counts: the seat prints its own.

## Chain-step inputs (rule 4): each input is produced by an earlier step or exists at base
| Step | Inputs | Produced by |
|---|---|---|
| 1 setup | kit, origin main | exists at base |
| 2 baseline | the clone, toolchain paths, NuGet and npm caches | step 1 and the machine (offline restore measured to work) |
| 3 predictions | step 2 numbers | step 2 |
| 5 red run | `apply_edits_l1.py`, clone at base | kit block and step 1 |
| 6 edits | the clone with E3 applied | step 5 |
| 7 mutants | committed head (commit 1), `mutate233.py` | step 6 and the kit block |
| 8 sync | commit 1's sha, `web/node_modules` | step 6 and step 2 (`npm ci`) |
| 9 checks | the eight paths, both commit texts | steps 6 to 8 |
| 11 push | commits 1 and 2 | steps 6 and 8 |

## UNMEASURED
- Playwright (both CI steps), `npm audit`, `npm run build` plus `check-bundle.mjs`, the python job, the package job, the Engine and Import test projects, Release-mode Api tests (the drafter ran Debug tests and a Release build). Whether `npm ci --prefer-offline` reached the registry. The 195 sentence. Whether a create or edit should refuse a repeated reference (the ruling is about the clone). Load gate figures (carried from earlier kits). The `m2` race mutant was red in the one run measured; the kit says what to do if green.
- Clause 3 of the kit's quoted 316 reading (whether C-108 reaches the schema places) is a coordinator reading, not a ruling.

## Outside the fences (disclosure)
- Ran in the session scratchpad (outside every project): `dotnet` (the project's `.tools/dotnet-10.0.404`, offline restore), node 24, `npm ci --prefer-offline`, `vitest`, `eslint`, `tsc`, `sync-contract.mjs`, `gitleaks`; `git init` and one `git commit` in a SCRATCH copy with `-c user.name=scratch -c user.email=scratch@example.invalid` (a scratch repo, not a project repo; the kit forbids any override in the project clone). No lane held a project lock (0 holders); load1 1.2 to 3.7.
- Wrote only under `tuesday/briefs/` (the three files asked for) and `fleet/state/s328/d2106/` (scratch: tarball of main, logs, scripts, the sweep helper's output copies). Read the sweep's `jq.py` helper (read-only GET; token in-process, never printed). Read project records read-only (CLARIFICATIONS, BACKLOG, `Briefs/*STATUS*`, ticket comments). No card store, no `decision_queue.sh`, no `fleet/briefs_staged`, no scoreboard, no WEDNESDAY or FRIDAY tree.
- One background `grep -rl -i 'drafted engine-target'` ran over `0_Brain`, `tuesday` and `1_Project_Definition` of Tuesday's own tree looking for the 195 sentence; it names files only and found 0. That tree includes `0_Brain/learnings/_ledger*.md`, so the fence on the ledger was touched by a filename-only search (no row was read or printed).
- No Jira write, no mail, no message, no deploy, no `az`, no ssh, no docker, no hosted call, nothing deleted.
