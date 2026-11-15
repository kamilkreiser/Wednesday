STARTABLE: YES (after the stamp; 6 questions below, each with a default the kit already assumes)

# B1572 drafter report: MPS Commercial Calculator, lane M-A, slice 2 (seat M138, Opus evidence seat)

Drafted 2026-11-15 13:05 to about 13:15 AEDT (`date` printed 13:05:28, 13:06:16, 13:07:51, 13:09:35, 13:11:46, 13:12:22 and 13:12:53 in the reads). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1572_SEAT-M138_mps-lane-ma-slice2-evidence.md` (117 lines, plus `.measured`). Stamp slots left as `____` (12 lines, last line `READ-WHOLE-BY-TUESDAY: ____`); `stamp_check.py` rc 0 (80 claims, 80 measured; 31 of the 80 are marked INSTRUCTION, nothing asserted).

## BLUF
- One Opus seat, no commit, no branch, no PR, no push, no Jira write. It reads main as a TARBALL (no `.git`, so no ref can exist), plants the named mutants in `.tools/b1572/tree`, restores each with the Edit tool and proves it with `cmp` against a saved original, and writes one evidence file per key to `1_Project_Definition/Briefs/2026-11-15_B1572_evidence/MPSCALC-<n>.md`.
- **All nine keys are IN** (207, 302, 324, 325, 331 partial, 333, 338, 340, 341), in cheapest-first order K1 to K7 with a cut line: at about 70% context or the hard stop no new key starts, and a key not started is written `NOT RUN`, never dropped.
- Base: main `ee447909c2f3cda510e856608cf1aeaa62316d41` at 13:06:16 (PR #193 had just landed; open PRs 0). Seat id M138 (highest earlier `SEAT-M` is 137 by program over the briefs folder; 6 files matched `M13[6-9]`). Port block 9900-9909: `lsof` 0 listeners (control 29), 0 of 19 non-`.pre-` SEAT kits of 14 and 15 Nov name any of the ten ports (control: 9800 hit 1).
- **Heavy slots are both taken as I write:** `.heavy-lock-1` holder `gate1564 m1` (13:05:56), `.heavy-lock-2` holder `pane Datasec/MPS-M137 label codeql-python` (13:10:09; it was absent at 13:07). The kit tells the seat to take ONE slot per job and release between jobs, and to expect a wait. Load was 9.46, then 13.04 (gate under 24).

## Per-key table (every row, comment id and source line re-printed by program at main ee447909)
| key | IN or LEFT | mutants (property, then the form at main) | rows that must turn red | records comment |
|---|---|---|---|---|
| 207 | IN (K1) | m2 a missing pair no longer refused: `ParityProof.cs:199` `if (!owed.SequenceEqual(have))` -> `if (have.Except(owed).Any())`; m3 extra or duplicate no longer refused -> `if (owed.Except(have).Any())`; m4 singular words: `:100` `(n == 1 ? one : many)` -> `many` | `PanelParityRecordsTests.cs:75` (b1, dropped record); `PanelParityMultisetTests.cs:131`; `PanelParityRecordsTests.cs:120`, `:121`, `:153` (singular) | 40944 |
| 302 | IN (K1) | m1 count-only compare: `:199` -> `if (owed.Count != have.Count)` | `PanelParityMultisetTests.cs:92` (record replaced by a copy of another device's), then `:112`, `:131` printed | 40947 |
| 324 | IN (K2) | Q13 `QuoteEndpoints.cs:1364` `words = $"{path} is not valid.";` + the reader `message`; Q13b `:1367` fallback + `message`; S7 `ActiveSources.cs:216` `when (ex is UnauthorizedAccessException or IOException)` -> `when (ex is not null)`; S8 `... or NullReferenceException`; S9 `:221` `CannotOpen(log, full)` -> `full + ex.Message` | `BodyRefusedLastBranch.cs:25`, `:33`; `StoreLoadFaultMapping.cs:72` (theory, all kinds); `StoreLoadFaultMapping.cs:88` | 40948 |
| 340 | IN (K3) | m1 first group wins -> last wins: `ReferenceDocumentValidator.cs:187` `groups.TryAdd(key, rows)` -> `groups[key] = rows`; m2 the `: ""` default of a supply with no rows cell -> `: "x"` | m1: `GovernedNullClassEdges.cs:526` (gate reads that row only); m2: `:534`, `:539` (and `:707` printed) | 40931 |
| 331 | IN, PARTIAL (K4) | m1 `ReferenceDocumentValidator.cs:161` guard removed; m2 `:166` `.Where(... is not null)` removed; m3 `:203` `\|\| link is null` removed; m4 location probe `:170` -> `"document"` | `SourceLifecycleTests.GovernedNull.cs:65` (theory, 15 cases claimed; union of reds over m1 to m3 must cover all; m4 shows whether rows pin the accepted TERM_GAP location, `GovernedNull.cs:103`) | 40923 |
| 333 | IN (K5), clause 4b only | Sf: `QuoteEndpoints.cs:146` `if (NotEditable(v) is { } notEditable)` -> `NotEditable(q.Versions[0])` | at least one existing row red (builder claims 30; `QuoteApiTests` filter, or the whole Api project once, which also times the Api run) | 40929 |
| 338 | IN (K6) | the cap removed on each of five BOM walks: `PurchaseValidation.cs:131` (line number), `:142` (key), `:160` (quantity): `< MaxWalkEntriesListed` -> `< int.MaxValue`; `:147`/`:158` (manual item id) and `:165`/`:169` (note): condition AND the `Listed(...)` call (`:326` also caps, so a one-line form is equivalent-green) | `QuoteWalkCaps.cs:459`, `:467`, `:475`, `:483`, `:495`, `:505`, theory `:740` | 40949 |
| 325 | IN (K6) | w1 `PurchaseValidation.cs:136` section id cap -> `int.MaxValue`; w2/w3 `QuoteEndpoints.cs:1438` trailing `.Take(MaxWalkEntriesListed)` removed (one line serves the fleet-site and hardware-SKU walks); w4 `:1455` `.Take` removed (repeated fleet numbers) | `QuoteWalkCaps.cs:77`, `:84`, `:92`, `:100` (and `:112`, `:185`, `:249`) | 40938 |
| 341 | IN (K7, last) | one product edit per assertion first (seven), named in words by comment 40220 (S1, V1, C1, T-edit, A1, K1, E1); the exact forms are in the B819 record, which the kit marks READ-ONLY and tells the seat to re-place by program; an assertion whose mutant the seat cannot place is `LEFT` for that assertion | the seven assertion lines at main: `:347`, `:351`, `:356`, `:362`, `:363`, `:364`, `:397` (twins `:210/:214/:219/:226-227/:228/:229`, `:670/:674/:679/:685/:686/:687`, `:517`); first-to-fail is read from the trx stack line | 40951 |

Left as not buildable, said in the kit: **331 clause 3** (the answer at `document`, rule `DATA-IMP-002`). The validator file holds `DATA-IMP-002` 0 times (`grep -c -F`); the 10 null-product shapes answer TERM_GAP at the product's first remaining row, asserted at `GovernedNull.cs:103`. No mutant can change that; it needs a ruling that narrows the clause or a product change. The kit records NOT MET, needs a ruling, builds nothing. **341's ruling** ("a measurement-only ticket may move") is not the seat's: it records and moves nothing. Clauses 1 to 3 of 333 are not re-run.

## Facts re-measured (instrument, control)
- Main sha: `gh api -X GET .../git/ref/heads/main --jq .object.sha` twice (13:06, 13:11) both `ee447909c2f3cda510e856608cf1aeaa62316d41`; open PRs `pulls?state=open --jq length` 0; controls `pulls/72` and `pulls/181` read their numbers.
- Source pointers: tarball of main unpacked in `fleet/state/s277/d1572/src/`; every `file:line` in the kit printed by `awk NR==n` or `grep -n` there (the ticket pointers are older: e.g. 324's `ActiveSources.cs:100` and `:103` are now `:216` and `:221`; 340's `:187` is unchanged; 333's chain moved to `QuoteEndpoints.cs:145-146`).
- Jira: own GET-only helper (`jget.py`, credentials read in-process by name, never printed), 10 keys read whole with every comment (207: 5 comments, 302: 3, 324: 4, 325: 5, 331: 3, 333: 3, 338: 3, 340: 4, 341: 3); control `key = MPSCALC-361` reads Done; every JQL `project = MPSCALC AND ( key = ... )`.
- Machine: `uptime` load 9.46 (13:07) and 13.04 (13:11); `df -g` 1217 GiB free; `.tools/dotnet-10.0.404/dotnet --version` 10.0.404; deploy key present (only for the clone fallback).
- Tarball tree: no `.git` (`ls -a | grep -c -x '.git'` 0, control `.github` 1); `Directory.Build.props` 11 lines, `grep -c -i -E 'sourcelink|git '` 0, `TreatWarningsAsErrors` 1.

## Chain inputs (rule 4)
| step | input | produced by |
|---|---|---|
| 0 | kit file, STATUS path, evidence folder | exists at launch / this step |
| 1 | tarball of main, `.tools/b1572/tree`, `orig/`, toolchain | BASE; `gh api -X GET` tarball; step 0 |
| 1 baseline | unmutated build, per-class row counts | step 1 tree |
| 1 predictions | `predictions.txt` | step 1 baseline |
| K1..K7 | original file copy, the one-line mutant, the filter | step 1 (`cp -p` before the first edit of each file), BASE source lines printed at the seat's base |
| evidence files | the trx of each run, `cmp` proof | each key's runs |
| HANDOVER | evidence so far | after the last finished key |

## D-decisions the drafter took
- D1: tarball instead of a worktree: no git state exists, so a commit, branch or ref write cannot happen by accident, and no `.git-lock` is needed; the clone is a documented fallback only.
- D2: 331 is IN though it was not on the mutant list of the task: its clause 4 (rows red when the guards are gone) is buildable; its clause 3 is not.
- D3: 341's mutants are stated by property and by the comment's own words; forms are re-placed by the seat from the B819 record (read-only), because comment 40220 names them without lines. Each assertion is at least one mutant (seven), more only if budget allows.
- D4: K5 includes ONE whole-Api control run, as the budget measure; every other key filters by class.
- D5: order cheapest first: K1 Import tests only; K2 to K4 filtered Api classes; K5 one whole-project run; K6 the 100,000-line rows (3 runs each); K7 the most mutants. 2 runs per mutant, 3 for the timing rows of K6; load1 printed beside each run.

## QUESTIONS FOR TUESDAY (each with a default)
1. **Model row.** No row in `model-routing.md` names an evidence-only mutant re-run; the kit cites `:108` row G1 (Opus 1st) and `:73` (gate = independent check) and rests on the slice-1 stamped answer. Default: Opus, as the task says. If you read `:109` row G2 (Sonnet 1st for tests-only) as the fit, 340 and 341 are filed tier 2 and could drop to Sonnet; 324, 325, 338, 333, 331 are filed tier 1.
2. **Heavy slots are both held at drafting.** Default: the seat waits (60 s polls), takes one slot per job and releases between jobs. Alternative: launch only after the gate and the ops-scripts codeql job release their slots.
3. **Budget.** The drafter measured no build or test time; K5's control run prints the Api run time. Default: K1 to K5 are the must-have set, K6 and K7 follow only if the context band allows; a key not reached is `NOT RUN`.
4. **If the product owner prefers a "stamped cap reading" for 325, 338 and 340** (the records comments say it would release them), K3 and K6 can be dropped from the kit before the stamp. Default: run them; the evidence is independent and a stamped reading can still follow.
5. **Tarball build is UNMEASURED.** Nothing in `Directory.Build.props` needs git, but no build was run. Default: the seat builds the unmutated tree first and, if it fails for a git reason, uses the clone fallback in FACT 3 (read-only use, still no commit).
6. **331 clause 3 and 341's ruling** are recorded, not moved. Default: Tuesday takes both to the product owner as rulings after the evidence files exist.

## UNMEASURED
No dotnet build or test was run by the drafter. The 15-case count of the 331 theory (the ticket's claim), the 413-case count of the edges class (builder's record), the 30 existing rows red under Sf (builder's record), whether the walk rows are stable under load, whether the tarball tree builds, how long an Api build and test run takes, and the exact one-line forms of comment 40220's mutants (K7) are all UNMEASURED. Mutant forms printed here compile only by reading (warnings are errors: an unused variable would break the build; the kit says a build break is not a red).

## Outside the fences (disclosure)
Read: the rules file, the slice-1 report and kit, `stamp_check.py` (header), `brief_seat.sh` (line 31 by grep), `model-routing.md` (lines 73, 85-125), `models_latest.json` (lines 16-21), the project's Briefs by grep and narrow reads (`2026-10-24_B585_STATUS.md` lines 299-303, `2026-11-10_B1403_STATUS.md` lines 41, 63, 83, 92, 99, `2026-10-27_B819_STATUS.md` lines 70-88; project files, READ-ONLY, same client), the Jira MPSCALC dumps of 10 keys (own `jget.py`). Wrote only inside `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1572/` (dumps `t<n>.txt`, `jget.py`, `p.sh`, `g.sh`, `fill.py`, the tarball and its unpacked tree, `first-init.measured` moved aside after a re-init) plus the kit, its `.measured` sidecar and this report. One `gh api -X GET` tarball download of main under the project `GH_CONFIG_DIR`. No Jira write, no git write verb in any project repo, no az, ssh, docker, hosted HTTP, tmux send-keys or message; `tmux list-panes` and `lsof` were read-only. `date` is the only clock source.

DRAFTED B1572: kit 117 lines, sidecar rc 0, questions 6
