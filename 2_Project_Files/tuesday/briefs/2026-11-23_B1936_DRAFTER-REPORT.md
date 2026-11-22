STARTABLE: YES

# B1936 DRAFTER REPORT | kit `2026-11-23_B1936_SEAT-X38_oxpd2-f2.md` (OXPd 2, lane F2 of wave 3, seat X38, gate G1 round 1)

Drafted 2026-11-23 00:01 to 00:31 AEDT by a read-only Opus drafter (clocks by `date`: 00:01:20, 00:01:48, 00:19:00, 00:20:16, 00:24:49, 00:26:32, 00:30:32). Kit 82884 bytes, 240 lines (sidecar last line); sidecar 165 claims, `stamp_check.py <kit>` rc 0 (165 measured, 0 not). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s312/d1936/` (below `<d>`). Tools for the seat: `<d>/gate/` (13 files, hashed in the kit's THE TOOLS).

## BLUF
- **(a) gate B1927 Minor closed by a second judgement.** `RemoveUnopened` keeps the probe; after a PASSING probe it calls `Judge` again under the same lock: `DoesNotRead` removed, `Reads`/`Absent` kept (false), `NotHandedOver` `StorageFailed`. `LocalSecretStore.cs` +19 -3. New cell U23 with a test-only `DamagingRecordStore` (injected through the public `LocalSecretStoreOptions.RecordStore`, as U07/U08/U20/U21 already do). RED at `main` by its own assertion (Secrets `Total: 95, Errors: 0, Failed: 1`, message `U23: a record that reads when judged again after the probe was removed`), GREEN after the fix (95 / 0). Secrets README: the removal paragraph says it, and the residual is narrowed per B1927 Info 2 (an older active key failing alone AFTER the start, with the start's full check and the pre-removal check cited).
- **(b) gate B1933 FOUND 1 as Tuesday's default: a NAMED LIMIT with a cell pinning today's behaviour.** No code line of the Data library changes (doc comment only, +5 -2). README audit sentence gets "unless that handler or interceptor catches the refusal (see Limits)"; a new Limits line names the catching handler and save interceptor. Limit cell `C15_limit_asserted_a_SavingChanges_handler_that_catches_the_refusal_keeps_its_change_and_the_save_writes_it`: green at `main`, red under `mNoStateChanged` (Data `Failed: 7`: it and kit B1932's six). The latch is Q1 (STOP-class) alternative b, not built.
- **(c) gate B1926 Minor: the map sentence rewritten** to name the 150 open object schemas (75 components generated as models with no property, 75 inline generated as `JsonElement`; 66 such properties in `Generated/`) and that an unlisted key is skipped on read. Every number by `census.py` (control `CONTROL FIRED: 2 of 2`).
- **Totals MEASURED (macOS arm64):** Secrets 94 -> 95, Data 63 -> 64, Adapters.Oxpd2 58 unchanged; whole solution `total: 1664`, `failed: 0`, `succeeded: 1660`, `skipped: 4` (main 1662 + 2). PREDICTED hosted: `--total 1664 --rules 530 --skipped-linux 4 --skipped-windows 21`.
- **THE SURFACE CHECK (commission STOP-check) by reflection on three assemblies, BASE vs green, each `cmp` rc 0:** Secrets `160 lines, cd5625c8...` (equal to kit B1920's / gate B1927's line), Data `107 lines, 6acf7547...`, Adapters.Oxpd2 `22915 lines, cefd886f...`; plant control `161 lines, 88feb4f6...` (the extra `SurfacePlant` line). Plus `surface.py` (Data PUBLIC 85 equal, SCHEMA 8 files equal, control 2 of 2) and a text count of public/protected changed lines 0 of 28 (control 1). No migration, no snapshot.

## FACTS RE-MEASURED (instrument -> result)
- Origin by `gh api -X GET` under the project GH_CONFIG_DIR (00:01:48, 00:19:00): `main` = `c480a0c81466f88102cb9d15a506b738615ebcbb` (= the commission's), open PRs 0, newest 25/24/23 closed; `.private` true, `.permissions.push` true; `matching-refs/heads/b1936` 0 (control `b19` 8).
- Scratch clones `<d>/clone` (work) and `<d>/clone2` (fresh `git apply` of both patches at `c480a0c8`, rc 0 each, second `--check` refused), both `clone.py ... draft` (push URL `invalid://no-push`).
- Every dotnet job through B1932's `heavy.py` unchanged (about 30 jobs; lock waits up to 10 polls behind other drafters, the lock seen held by `B1935 drafter`; never broken). Logs `<d>/logs/`; mutant summary `<d>/logs/mutants.out`; chain `<d>/logs/chain.out`.
- Mutants (`<d>/gate/mutants3.py`, each `undone ... equal True`, `diff --stat` equal): `mNoRejudge` U23; `mRejudgeKeepsAll` U23 + U04; `mRejudgeLosesFault` U23; `mProbeIgnored` U22; `mNoStateChanged` 7 Data cells (listed by name in the kit).
- Chain: restore `--force` rc 0, 26 lock files `cmp` rc 0; both publishes rc 0; `GUARD: clean (10 files)` / `(11 files)`; `Ran 111 tests` OK; `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)` then `RULES: clean (530 files)`.
- Words: `words.py --control` 13 of 13; over the 181 added lines and the commit message `WORDS: clean (2 files)`. gitleaks 8.30.1: planted control rc 1 (`leaks found: 1`, quarantined), 12 neutral files rc 0, `<d>/clone2` rc 0.
- Census: `CENSUS: inputs 37; object schemas 1616, with properties 1442; additionalProperties 206, false 206; patternProperties 0; propertyNames 0; open 150 (components 75, inline 75); generator reads ... 0, 0, 0 (control "properties" 3); generated JsonElement properties 66 in 21 Models.cs; Any(true) 66`. The gate's 150 is reproduced only in the frame that excludes `allOf` objects (with them: 174); the kit states the frame.
- Rulings check (commission line 9): `CLARIFICATIONS.md` case-insensitive literal counts for every subject word of this lane are 0 (catch, latch, interceptor, SavingChanges, probe, DeleteUnreadable, removal guard, additionalProperties, open object, JsonElement, judge); positive control `tolerant` 5. Nothing in the kit calls a ruled item undecided.

## STOP-SEVERITY CHECKS RUN ON THE PROTOTYPE (stamp checklist item 12)
- SURFACE equality x3: PASS; plant control FIRED (161 lines, other hash).
- Text public/protected count: PASS (0 of 28); control FIRED (1).
- `surface.py`: PASS (rc 0); `--control` FIRED 2 of 2.
- RED first: PASS (`[FAIL]` 1, U23, by its own message); control `Total:` line present.
- Mutants each red on exactly the listed cells: PASS (5 of 5).
- Name-status 7 `M` rows (on `git diff --name-status <BASE>` of `<d>/clone2`, unstaged): PASS; planted Migrations row FIRED (FAIL, rc 1).
- SHARED FILES `diff --quiet`: PASS (rc 0); control over `tests/Datasec.Suite.Data.Tests` FIRED (rc 1).
- ASCII/tab/CR/final LF on seven files: PASS; planted U+200B FIRED (1).
- gitleaks: PASS; control FIRED. words: PASS; control FIRED.
- Lock files byte for byte: PASS. Census equal: PASS; control FIRED.
- Prior-work greps: three rc 1 PASS; control `RemoveUnopened` count 2 FIRED.
- **NEVER RUN by the drafter (marked so in the kit):** `run_step.py` neutral scan of stored objects (wordings RELAYED from B1932/B1920), `hosted2.py` on a head of this lane, commit identity check, push read-back, the staged-tree (`--cached`) form of Step 6 (no commit was made; the same checks ran on the working-tree diff).

## D-DECISIONS (each Tuesday's default as coordinator; kit D1 to D7)
- D1 second judgement only on the active-key (probe) branch; revoked/foreign keys unchanged. D2 red-first via the tests' own record store (one damaged read). D3 named limit with a cell (Q1). D4 cell is the handler's; interceptor named from the gate's N5b (RELAYED). D5 `SavedChanges` line unchanged (DERIVED: never written by that save; the next save's pre-check refuses; UNMEASURED). D6 map sentence as a census in the stated frame. D7 one commit on new branch `b1936/f2-store-audit-map-follow-ups` from `main`.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS, S4 answers in words):** default **a** named limit with its cell, no Data code change; alternative **b** the gate's latch (not built; a library-owned command interceptor, ordering against a host's interceptors UNMEASURED, new cells and gate read).
- Q2 red-first shape: default the tests' own record store; alternative a timed data-protection fault or a product seam.
- Q3 interceptor shape: default named only; alternative a second limit cell (+1, 1665).
- Q4 `SavedChanges` catching case: default line unchanged; alternative probe/cell first.
- Q5 map sentence: default as built (8 lines); alternative one shorter line.
- Q6 Opus by `<project>/CLAUDE.md:7`; READY Step 0 + 150, push by + 120, pane `Datasec/OXPd2-X38`, 40 min lock waits, gate G1 round 1.

## CHAIN INPUTS (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp slots | Tuesday |
| 1 | `<src>` 13 files; `<repo>` local values; origin; BASE's push run | `<d>/gate` (exists); `<repo>`; GitHub |
| 2 | BASE files | Step 1 clone |
| 3 | `1-cells-red.diff`; baseline build | Step 1 |
| 4 | red tree; `2-fix.diff`, `mutants3.py`; `surface-out`, three `surface-base-*.txt` | Step 3; Step 1 |
| 5 | green tree, mutants and plant undone; lock hashes; `census.py` | Step 4; Step 1 |
| 6 | staged tree; `commit-message.txt`; `run_step.py` | Step 5; Step 1 |
| 7 | the commit; `origin/main` | Step 7 (a); fetch |

## UNMEASURED
- Both new cells on Linux and Windows (PREDICTED green; windows skipped 21 PREDICTED). DPAPI-NG for U23 on Windows.
- The gate's window as a real timed fault inside the data protection library (U23 reaches the same code path by a damaged read).
- A catching save interceptor as a cell (gate's N5b RELAYED); a catching `SavedChanges` handler (D5).
- How a declared map would be generated (no input has one).

## DEVIATIONS AND NOTES FOR THE STAMP
- The commission's form kits: B1932 is a fix round on a pushed branch; this lane is a NEW branch from `main`, so its WORK, rebase rule and REFUSE list follow B1920's (lane S) form, and B1932's tool set. B1914 was hashed, not read (it is the form for a lane that creates a library; this lane creates none).
- The surface program must load the Data assembly from its TEST project's bin (package dependencies are copied there); loading it from `src/.../bin/` ends rc -6 (`Microsoft.EntityFrameworkCore.Relational` not found). The kit says so and points every surface run at the test bins.
- The commit subject is 238 bytes (under GitHub's 256-character title), so the squash can carry it unshortened.
- Spot lines for the stamp's sidecar check: `c064aaa1` (red total), `a9a5b07a` (red message count 1), `95669ef3` (whole 1664), `fa13a5f9` (surface cmp x3), `8a7b8534`/`dcd2797d` (prior-work and control), `85db7e46` (ASCII), `5d0af435` (the zsh `:s` modifier hit the drafter once; recorded in STANDING LINES).

## OUTSIDE THE FENCES (disclosure)
- Writes: only this report, the kit, its `.measured` sidecar, and scratch under `<d>/` (two clones, logs, tools, surface build). Nothing written to the project, `<repo>`, GitHub or Jira; no commit, no push, no pull request; no `cd`; nothing deleted (the gitleaks control moved to `<d>/_quarantine/gl-control`).
- Reads of the project: `CLAUDE.md` lines, `CLARIFICATIONS.md` (counts and line numbers), `BACKLOG.md` (item first lines), `.tools/` listing (no `b1936`), `Briefs/` listing by count, the lock folder's `owner.txt` once. No `Source_Documents/`, no key folder, no sibling project, no card store, no ledger.
- GitHub: `gh api -X GET` only, under the project GH_CONFIG_DIR. `git clone` of the origin twice (the draft mode; fetch only).
- Heavy jobs: all through `heavy.py` with the wave lock while three other drafters ran; the commission allows drafter runs beside the lock (it names the shared lock and "expect waits").
