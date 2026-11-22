STARTABLE: YES

# B1922 DRAFTER REPORT: lane E (seat Datasec/OXPd2-X34), the OXPd 2 adapter README's named limits

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1922_SEAT-X34_oxpd2-e-adapter-readme-limits.md` (65016 bytes, 207 lines, sha256 `a3c962c2...635b`), sidecar `.measured` beside it (`stamp_check.py <kit>`: 147 claims, 147 measured, rc 0). Scratch and tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1922/` (`gate/` is the seat's `<src>`, ten files; `tools/` holds proto.py, proto2.py, proto3.py and fill.py; `logs/`). Drafted 21:30:34 to 21:45:42 AEDT 2026-11-22, by `date`. Read-only toward the project, Jira (no call made) and GitHub (`gh api -X GET` only).

## BLUF
- The kit is docs only: ONE file, `src/Datasec.Suite.Adapters.Oxpd2/README.md`, frozen as `1-readme-limits.diff` (+48 -1, two hunks, 108 lines to 155). It adds thirteen limit sentences under three new `###` headings of `## Limits`, and corrects line 63. Line 63's full stop becomes a semicolon, and the line names tolerant device answers as "an open question".
- Every sentence is proved against the code at `4a0a9717`. There are 60 `file:line` token rows in `2-proofs.tsv`, checked by the kit's one new program `proofs.py`: `PROOFS: 60 of 60 PASS`. Its moved-line control prints `PROOFS-CONTROL: 60 of 60 FAILED when moved`. The census prints `CENSUS: 13 of 13 as required`. The first draft of the rows had two line numbers one short (`Oxpd2Json.cs` 181 and 188). The program caught both, and they were corrected to 182 and 189 by `grep -n -F`.
- Item 45 (5) is a claim about the tests: "removing Issue's generation bump alone turns no cell red". It is MEASURED by mutant. With `mIssueNoBump` the Adapters.Oxpd2 tests give `Total: 58, Errors: 0, Failed: 0`. `mNoFill` alone also gives `Failed: 0`. The two together turn exactly `A06_Issue_during_a_check_that_reads_the_vault_takes_effect` red (`Failed: 1`). That is the positive control: the cell is held by both mechanisms.
- Totals do not move. Locally, the whole solution on the patched tree gave `total: 1579`, `failed: 0`, `succeeded: 1575`, `skipped: 4`. The publishes gave `GUARD: clean (10 files)` and `GUARD: clean (11 files)`. `RULES: clean (500 files)`, `Ran 111 tests` OK. The PREDICTED hosted run is the same as main's: `--total 1579 --rules 500 --skipped-linux 4 --skipped-windows 19 --unit 111 --floor 111`.

## Facts re-measured (instrument, control)
- Origin by GET at 21:35:08: main `4a0a9717277f60647dfc174e60ec04fc7008e615`; private true and push true; 0 open PRs; 21 branches. `matching-refs/heads/b1922` has 0 rows (control: `heads/b19` has 3). The README is touched by PR 13 and PR 14 (1 row each, the control) and by PRs 15 to 19 (0 each).
- README at BASE: sha256 `0efd979f...28a4aa`, blob `f82311be`, 108 lines. It has `## Limits` once and `### Limits of the` 0 times. It has 0 `.cs:N` pointers. The four Adapters files the sentences cite were read whole or in part.
- Census: 37 of 37 specification inputs parse; there are 206 `additionalProperties` and every one is `false`. The generator files hold 0 `additionalProperties` (control: `Unsupported` 2). `Oxpd2RefusalKind` and `DeviceTokenError` hold 0 `JsonStringEnumMemberName` and 0 `Oxpd2Unrecognized` (control: `Generated/Application/Enums.cs` holds 20). `DeviceTokenHolder.cs` writes `Generation` once (in `Forget`). `StoreRefreshValue` has 0 `Flight.` and 0 `Generation` (control: 1 `_vault.Put`).
- No file in `tests`, `build`, `src`, `contracts` or `.github` reads the adapter README (`git grep -i readme`). ci.yml has no paths filter (`grep -c -i paths` 0), so a README-only push runs all four jobs.
- Words and secrets: `words.py` prints `WORDS: clean (2 files)` over the 48 added lines and the commit message (control 13 of 13). gitleaks 8.30.1 finds no leaks in the clone or in the neutral copies; the planted control gave rc 1 and was quarantined.
- Heavy jobs: 16 through heavy.py and the wave lock, with lock waits of up to 2 polls; load1 stayed between 5.98 and 7.46. No test ran while another holder had the lock.

## Chain inputs (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit and its Stamp | Tuesday |
| 1 | `<src>` (10 files), the origin, main's hosted run, BASE's code | the drafter's scratch; GitHub; the clone of Step 1 |
| 2 | the patch and BASE's lines | Step 1 |
| 3 | `1-readme-limits.diff`, `2-proofs.tsv` | Step 1's tools copy |
| 4 | the patched tree, `3-mutant.txt`, the baseline build | Steps 3 and 1 |
| 5 to 7 | the patched tree with the mutant undone; `commit-message.txt`; origin/main | Steps 4, 1 and the fetch of 7 (b) |

## D-decisions (Tuesday's as coordinator)
- D1: item 45 (1) to (11), README halves only. (4) is already in the README. The `IDeviceSecretVault.TryGet` doc line of (10) is OUT because it is a `.cs` file.
- D2: item 46 IN: the full stop, the map census line, the enum wire names, the printer UNMEASURED line, and NOT DECIDED 1 named as open. OUT: records (1), (3) and (5), and NOT DECIDED 2 and 3.
- D3: no `file:line` in the README. The proofs live in `2-proofs.tsv`.
- D4: "is an open question" in place of "not decided", because `words.py` refuses the word "decided" in added lines. My first wording tripped it, and I measured that.
- D5: the seat re-runs the survivor mutant.
- D6: the sentences are grouped by the code's three parts.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS, S4 in words): item 45 scope.** Default: (1) to (11), README halves only. Alternative: (1) to (6) as the commission row reads. That drops 5 sentences (L7, L8, L11, L10, C9) and 23 rows; the alternative was not built.
- Q2: item 46 extension. Default: IN as in D2. Alternative: none of it.
- Q3: no `file:line` in the README. Default: none. Alternative: pointers, which go stale.
- Q4: the seat re-runs `mIssueNoBump`. Default: yes, on macOS.
- Q5: Opus (project CLAUDE.md:7); READY by Step 0 + 90 minutes, push by Step 0 + 60; pane X34; gate G2 on Opus.
- Q6: the enum sentence (E12) rests on the converter's source. Its examples are NOT RUN as a serialisation. Default: keep it. Alternative: drop the example clause.

## UNMEASURED / NOT RUN by the drafter
- Anything hosted on this lane's head.
- The restore with `--force` and the lock-file comparison.
- The `run_step.py` neutral-object scan; its wordings are RELAYED.
- Whether the hosted Linux and Windows legs keep `mIssueNoBump` green. It never lands, so this is not a landing condition.
- Behaviour with a real vault (sentence L3 says UNMEASURED).
- Any printer behaviour (sentence G3 says UNMEASURED).
- What the generator would do with an input that has a map (sentence G1 says UNMEASURED; D8's guess in kit B1863 was not copied).
- E1's "can get the same result" stays DERIVED. The reader's measured case is RELAYED from item 45 (1).
- The proof rows prove that a token is on a line. Whether each sentence is TRUE is a reading: mine, then the seat's (Step 2), then the gate's.

## Outside-the-fences disclosure
- I wrote these files only: the kit, its `.measured`, this report, and the scratch folder `fleet/state/s311/d1922/`. That folder holds the clone (push URL `invalid://no-push`, its README modified there only), gate, tools, logs, out, scratch and `_quarantine`.
- Earlier sidecar drafts were moved to `_quarantine`, not deleted.
- I made no write to the project, its `.tools`, Jira or GitHub. I had no `cd`, no az, no docker, and opened nothing under Source_Documents or the NAS.
- My heavy jobs (16) took the shared wave lock through heavy.py, one at a time. I never broke another holder's lock.
- `words.py` over `2-proofs.tsv` and `proofs.py` prints 181 hits (code tokens such as names and ids). Neither file is ever committed; the seat scans only the added lines and the message.
- Other drafters' lanes (S, D) were not touched.
