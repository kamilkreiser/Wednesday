STARTABLE: YES (after Tuesday's stamp; five questions, each with a default that lets it start)

# B1616 drafter report: HPSM-POC lane H-4, two stale developer statements (HPSMPOC-495), seat H174

Drafted 2026-11-16 from 14:57 to 15:04 AEDT (`date` printed 14:57:04, 14:57:25, 15:00:07, 15:00:39, 15:02:27, 15:03:26, 15:04:18).
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1616_SEAT-H174_hpsmpoc-lane-h4-two-stale-statements.md` (267 lines).
- Sidecar: `...two-stale-statements.md.measured` (87 lines: 63 stamp_check claims plus S01-S24). `stamp_check.py <kit>` exits 0 (run unpiped, `rc=0`).
- Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s282/r1616/` (the Jira read, raw files at main, the golden outlines at both commits, the head simulation copies).
- Template: the B1599 kit and its STATUS FOR TUESDAY (clone by URL; literal `<PR-NUMBER>`; the project checkout's `/Volumes/Laptop-DEV/` key; the python 3.9 resource-hygiene row).

## BLUF
- **Both statements are false, and the ticket is right, but its description of the second one is loose.**
  - **A. README ADR-R13 (`README.md:76`).** "The executive report's golden outlines are unchanged (asserted)." The drafter diffed the three executive outlines at `a9e0052f`'s parent `d607c8fb` against `a9e0052f` by program: PageCount 5 to 6, 9 to 10, 8 to 9, and all 9 headings of each moved by exactly +1, nothing else changed. The four readiness outlines have exactly one commit each (`8d65fece`), so they did not move. The kit's replacement sentence ties every clause to a measured line.
  - **B. `stamped-set.test.ts:17`.** The comment does NOT say "Q-CS-01 is asked first" (the ticket's and sweep's paraphrase). It says "control: the route's set is 0.5.0's". The real defect: `moduleSet` comes from `playbookPackage`, which is 0.7.2 (`registry.ts:92`); the array order still starts Q-CS-01 (same first five ids in 0.5.0, 0.6.0, 0.7.0 and 0.7.2), but the ASK order now starts Q-CS-13 (`content-072.test.ts:37`; section S1 order 1, question order 1). The B1597 gate's F1 says the same. **Line 9 carries the same stale `(0.5.0)`**; the kit includes it (Q-1).
- **No assertion, product, golden or content file changes.** One README line and two comment lines. G3 (no gate), so the kit makes the builder's proofs complete: a red-first program at BASE, a comments-only diff check with a planted control, lint, typecheck, the whole vitest by name before and after, the Reporting test project once, and the infra scans.
- **Drafter's simulation of the edit.** On scratch copies, with the kit's exact words: README OLD sentence 1 to 0, NEW 0 to 1, 2 changed lines, 238 characters, ASCII, no pipe; stamped-set `0.5.0's` 1 to 0 and `(0.5.0)` 1 to 0, left-of-comment code byte-identical on lines 9 and 17, line 17 now 241 characters (a lint line-length refusal is allowed to be broken onto its own comment line; the kit says so).
- **Model and gate.** Sonnet (`model-routing.md:85`, row L6; id `claude-sonnet-5-5` at `models_latest.json:23`), G3 (`:110`). `BRIEF_SEAT_LEVEL=sonnet` is inside the launch quotes.

## Facts re-measured with instruments
- **Main** `678a1153d28be006a088a3b1fba8f5aab52e8d0e` by `gh api -X GET branches/main` (14:57 and 15:02) and by `git ls-remote` with the deploy key from outside any repo (15:03). Open PRs 0 (length; control: `-i` printed `HTTP/2.0 200 OK`); `pulls/99999` is 404. `matching-refs/heads/b1616` length 0 (control: `heads/b1599` length 1).
- **Ticket** HPSMPOC-495 (Backlog; labels docs, rec-2026-11-16): read by the sweep's GET-only `jdesc.py` copied into my scratch. Its "Done when": both statements true again, or recorded as declined.
- **Held / dropped check** (grep of the pickup and today's daily note): the only hits are OWED lines naming 495 as new from B1600, the B1586 F1 README row and the B1597 F1 stamped-set row (pickup lines 81, 111, 126, 136; daily note lines 61, 87). No HELD or DROPPED line covers it. Pickup line 335 says "HPSM H-2/H-3/H-4 (H-4 drafts for Kam)": that is an older sweep's H-4 (which keys it meant is UNMEASURED; SWEEP-1450 puts the draft documents 91, 162 and 163 out of scope), not today's commission H-4. Control: `HPSMPOC-484` returned 2 hits in the same pickup.
- **Toolchain by path:** `<project>/.tools/node24/bin/node --version` printed `v24.21.0`; `<project>/.tools/dotnet-10.0.404/dotnet --version` printed `10.0.404`; CI `node-version: 24` at `ci.yml:384`. Drafter's python is 3.14.10.
- **CI predicates:** web lint `eslint --max-warnings=0` (`package.json:10`), typecheck `:11`, vitest `:12`; `api` job `ci.yml:87`; `infra` `validate.sh` at `ci.yml:630`, whose `test_hidden_characters.py` walks `git ls-files` (rule 8). The Reporting csproj has no README item (count 0, control `Content` 2), so the README is not a compile input.
- **Ports:** none needed. Lint, typecheck, vitest and one dotnet test project open no listener. I did not take a block and ran no `lsof` scan, so no port-block claim is made.
- **Seat id.** The highest existing `SEAT-H` in briefs/ at 14:57 was H172; H173 is B1615 (being drafted in parallel, UNMEASURED); H174 is the commission's.

## Step input table (MEASURED LITERALS rule 4)

| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit, REFUSE 1-7 inputs, the deploy key, node and dotnet paths | exist at BASE / Tuesday's stamp |
| 1 | origin refs, the two files, `Sxx` pointers | BASE (read-only gh/git) |
| 2 | Golden outlines at `a9e0052f^` and BASE; `playbook-placeholder.v0.7.2.json` and `v0.5.0.json`; the README and test file | BASE (all tracked; `git show` in the clone) |
| 3 | the clone, `node_modules` | Step 0 (`npm ci`) |
| 4 | Step 2's rows (the facts under the new words) | Step 2 |
| 5 | `h4.diff` and the edited files | Step 4 |
| 6 | the edited files, `base-unit.json` | Step 4, Step 3 |
| 7 | green Steps 2-6 | Steps 2-6 |
| 8 | the pushed sha, Step outputs | Step 7, Steps 2-6 |

## D-decisions (the drafter's)
- **D1 Replacement README sentence names the three files and the four readiness outlines**, so each clause maps to one measured line. The old sentence was true when written (B05); the new one states the present fact, not history.
- **D2 The comment wording avoids a version number** ("the current playbookPackage's"), so the next package bump cannot stale it again. Lines 1-3, 21 and 22 are true and stay.
- **D3 Red-first without a failing test.** There is no red test for a false comment. The red is a program that prints the old sentence's count 1 beside the golden-outline diff (A1, A3) and line 17's `0.5.0's` beside the ask-order read (B1); the head arm flips them. Each program row has a planted control that must fail.
- **D4 The Reporting test project runs once** at head (the README is not an input, so base equals head), to show the committed outlines the clause rests on are the ones the code renders.
- **D5 Heavy lock and load gate kept** even for an S lane: `npm ci`, the whole vitest and a dotnet test are the same heavy class as the other HPSM kits.

## Q-questions for Tuesday (each with a default)
- **Q-1 Line 9.** Include the stale `(0.5.0)` on line 9 (same file, same defect, comment only)? **Default: yes**, as the kit has it; otherwise line 17 would say "current" while line 9 says 0.5.0.
- **Q-2 README wording.** Is the replacement sentence acceptable developer text? **Default: yes** (the property in THE EDIT lets the seat use other words that meet it).
- **Q-3 Gate.** G3 means no gate. **Default: G3**, with Tuesday's completion check against the kit's Step-5 and Step-6 outputs. Alternative: a Sonnet G2 read.
- **Q-4 README test counts (lines 85 and 88: 208, 148, 60).** Whether they are current is UNMEASURED and outside the ticket. **Default: not touched**; the seat may name a mismatch in FOR TUESDAY.
- **Q-5 Window.** **Default: one window, READY target 120 minutes after Step 0, HARD STOP set at the stamp.**

## UNMEASURED
- Whether `npm ci`, lint, typecheck, the whole vitest run, the Reporting test project and `validate.sh` pass on this machine at BASE: the drafter made no clone and ran none of them (the kit makes them the seat's Step 3 and 6 and requires base and head equal). Expected test count of the file is 3 (counted from the `it(` lines, not run).
- Whether the Reporting test project needs SQL Server (the kit tells the seat to stop that job, not improvise a container).
- Whether eslint refuses the 241-character line 17 (the kit allows a comment line above).
- Lane H-1 (B1615) paths: RELAYED from the sweep, not read; no program was run over file sets.
- The B05-era assertion behind the old "(asserted)" wording: not traced; it is dropped from the new sentence, which claims no assertion.

## Outside-the-fences disclosure
Nothing outside the fences. Reads only: `gh api -X GET` under the HPSM-POC `GH_CONFIG_DIR` (files, trees, commits, branches, pulls, one code search that returned nothing useful and is not relied on), one `git ls-remote` with the project's own deploy key from outside any repo, the sweep's GET-only `jdesc.py` for HPSMPOC-495 (token read in-process, never printed), local tracked files (briefs, model routing, models_latest, pickup, daily note, the B1599 STATUS and the B1597 and B1586 VERDICTs). Writes: the kit, its sidecar, this report, and files in the scratch folder `r1616/`. No Jira write, no mail, no board, no `az`, no `cd`, no deploy, no `decision_queue.sh`, no ledger, no Artifact tool, no clone, no fetch, no checkout, no build, no docker. A hook advisory about case-sensitive greps fired several times; every count that mattered carries a positive control or was cross-read by program.

DRAFTED B1616: kit 267 lines, sidecar rc 0, questions 5
