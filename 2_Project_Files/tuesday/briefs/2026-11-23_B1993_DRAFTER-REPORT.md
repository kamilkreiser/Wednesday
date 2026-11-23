STARTABLE: YES

# B1993 DRAFTER REPORT: lane FK (OXPd 2 contract runtime follow-ups), seat Datasec/OXPd2-X54

Drafted 2026-11-23 16:57 to 17:48 AEDT (clock reads by `date`: 16:57:57, 17:15:32, 17:30:36, 17:47:40) by the read-only drafter B1993 (Opus) on the commission `2026-11-23_B1992-B1994_OXPD-WAVE2-KITS_DRAFTER_COMMISSION.md` (sha256 `ed4cf64f...`). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s317/d1993/` (below `<d>`).

- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1993_SEAT-X54_oxpd2-fk.md` (84043 bytes)
- Sidecar: `...fk.md.measured`. `stamp_check.py <kit>` reports 133 claims, 133 measured, 0 not measured, and exits 0.
- Tools: `<d>/seat-tools/` (12 files). They are byte-equal to `<d>/gate2/`, the copy the drafter froze and ran (`diff -r` rc 0; control against the older `<d>/gate` rc 1).

## BLUF
1. **F1, F2 and F3 of owed item 36 are already on `main`.** Pull request 7 (`0804860b`, branch `b1834/wp04-oxpd2-fix-f1-f3`, merged 2026-11-21) closed all three. Its commit message names the read-only lists, the bounded body limit and the Unicode length rule. Their cells are present at BASE `d804de5e`, measured by `git grep`. `BACKLOG.md` mentions pull request 7 nowhere (0 lines; the control "pull request 6" finds 1), so item 36 is stale. The kit rebuilds none of the three (D0, Q1 STOP-CLASS), and FOR RECORDS carries the owed ticks.
2. **What the lane builds** is ONE commit with 19 paths: 18 changed and 1 added.
   - **F6:** the generator's client summary (`Oxpd2Unit.cs:917`) gains two `///` lines. They say that an `HttpRequestException` from the send, or an `IOException` while a success body is read, passes out of the method as it is (neither is a refusal), and that a non-success body is never read. The 16 generated `*Client.cs` files are regenerated, each `+2 -0`. Three new cells in `BodyReadTests.cs` pin this.
   - **Item 67's pull-request-20 part:** K8 now sends a null at every optional root property of every client model. Both counts are pinned: 716 models and 2117 properties.
   - No public member, signature or code line changes. C6 found 0 non-`///` lines under `src/`, and its planted control fired.
3. **The gap was real.** Mutant `mNullAfterFirst` survives the landed suite at BASE (`Total 149 Failed 0`, measured twice, in clone2 and clone3). It turns the new K8 red at the head.
4. **Red, green and the checks, all measured on a fresh clone with the frozen patches:**
   - Red: `total: 1945`, `failed: 1` (the text cell, by its own assertion).
   - Green: `total: 1945`, `failed: 0`, `succeeded: 1941`, `skipped: 4`.
   - Mutants: `MUTANTS: 4 of 4 MATCH, 4 of 4 undone equal`.
   - Regeneration on the applied tree writes nothing new (unstaged diff rc 0 after the regeneration; control rc 1 before staging).
   - Lock files: 34 of 34 equal after the forced restore.
   - Release guard: `GUARD: clean (14 files)` and `(15 files)`.
   - `Ran 111 tests OK`; `RULES: clean (629 files)`.
   - `CHECKS: 6 of 6 PASS`; `WORDS: clean (2 files)`.
   - gitleaks: control rc 1, then rc 0 on the clone and on 26 neutral files.
5. **Size and tier:** gate G1, round 1 of 2 of lane FK. Size S. One seat should finish well inside 2 hours: the drafter's whole chain, mutants included, took about 30 minutes of heavy jobs with lock waits. The kit sets READY at Step 0 + 100 minutes, the push by Step 0 + 75 minutes, and a hard stop of 23:30.

## FACTS RE-MEASURED (instrument; control)
- **Origin `main`:** `d804de5e303d62a78a8bcd677ec2cd66940b91f4`.
  - Read by `gh api -X GET .../git/ref/heads/main` and by three `clone.py ... draft` clones.
  - `matching-refs/heads/b1993` returns 0 (control: `b1972` returns 1).
  - Pull requests 37 down to 28 are all closed.
- **BASE push run** (`hosted3.py`): PASS at `--total 1942 --rules 628 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`.
  - The commission relayed 1942 and 628, and both re-measure.
  - **New: the guard counts are now 14 and 15.** `hosted3.py`'s defaults (10 and 11) print `FAIL 2` on a green `main` (saved in `<d>/scratch/evidence/`).
- **Contracts executable at BASE:** `Total: 149, Errors: 0, Failed: 0`.
- **Consumers (commission line 19):** no public member changes. The members pull request 7 changed (`Properties`, `EnumValues`, `RequestContentTypes`, `Operations`) have these consumers on BASE:
  - `tests/Datasec.Suite.Adapters.Oxpd2.Tests/CallbackCellTests.cs:88` and `:224` (they read `Operations`), plus the Contracts tests.
  - 0 lines in Lab, Server, DeviceAuth, Device or Callbacks (control: Serilog's `Properties` in `DenyListSink.cs`, 4 lines).
  - No product code constructs any of the 16 generated clients (control: the same pattern finds `DeviceTokenClient(`).
  - Lab references the adapter (`Lab.csproj:8`) but uses no generated type (0 lines).
- **Partition:** the FK paths are disjoint from L4's and O1's rows in the commission (derived from that table). FK touches no slnx line, `.csproj` or lock file.
- **Rulings:** `kam_rulings_today.sh` printed 9 rows (OQ-6 found). None names exceptions, K8, lists or the generator. In `CLARIFICATIONS.md` (720 lines) every subject word of this lane counts 0, except `regenerat`, which has 1 line (C-56's tolerant-reading entry, line 594). The controls `tolerant` (5), `oq-6` (3) and `c-63` (1) all fire. K8 protects C-63 ("Keep both strict for now", line 614).

## CHAIN INPUTS (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, stamp | Tuesday |
| 1 | `<src>` (12 files), `<repo>` local values, origin, BASE push run | drafter scratch, `<repo>`, GitHub |
| 2 | files at BASE | Step 1 clone |
| 3 | `<lane>/regen`, `mutants_fk.py`, `1-red.diff`; the restored clone | Step 1; Step 3's own restore |
| 4 | `2-fix.diff`, regen, `mutants_fk.py`; the red tree | Step 1; Step 3 |
| 5 | the green tree, mutants undone | Step 4 |
| 6 | the staged tree; `checks_fk.py`, `words.py`, message | Step 4; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted3.py` | Step 7 (a); 7 (b); Step 1 |

## D-DECISIONS (all Tuesday's defaults as coordinator, none the product owner's)
- **D0:** F1, F2 and F3 are not rebuilt.
- **D1:** F6 is stated and pinned, with no runtime change. This follows the verdict's own recommendation (`VERDICT.md:37`) and Tuesday's precedent for F3 (B1945).
- **D2:** one new test file, which reuses the `ClientTests.cs` helpers read-only.
- **D3:** K8's last block is rewritten in place, with both counts pinned exactly.
- **D4:** each mutant is applied identically to `Oxpd2RuntimeText.cs` and the generated file, so the regeneration cell stays green. The first lambda form of the mutant also reddened `No_static_field_of_the_adapter_is_writable`, so the frozen form uses a loop.
- **D5:** one commit, with the rebase rule applied before the first push.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 (STOP-CLASS, answer it in S4 in words):** F1 to F3 are not rebuilt; pull request 7 closed them. **Default: a.**
- **Q2 (F6):** state and pin it. **Default:** state and pin. The alternatives are not built:
  - (b) wrap a body-read `IOException` in an `HttpRequestException` (a runtime change, no public member change);
  - (c) add a new `Oxpd2RefusalKind` member (a public enum change).
- **Q3 (K8 counts):** pin exactly (716 and 2117). **Default:** exact. Alternative: a lower bound only.
- **Q4 (the sentence):** the patch's two lines. **Default:** keep them. Alternative: a single shorter line, which means re-drafting.
- **Q5 (gate):** **Default:** G1, round 1 of 2, on Opus. The reviewer re-runs the survivor at BASE and `mErrorBodyRead`.
- **Q6 (records):** **Default:** FOR RECORDS as written: tick F1 to F3 against pull request 7, and tick F6 and item 67's part against this lane's pull request.
- **Q7 (seat):** **Default:** Opus, READY by Step 0 + 100 minutes, push by Step 0 + 75 minutes, pane X54, hard stop 23:30.

## UNMEASURED
- Every hosted leg on this lane's head. The predicted result is total 1945, rules 629; linux succeeded 1941; windows succeeded 1924.
- `run_step.py`'s neutral scan on a commit of this lane.
- `git ls-remote` from a keyed clone: the drafter's draft clones hold no key and returned rc 128. The drafter read the same question through `gh api` matching-refs instead.
- What a real OXPd 2 device, or .NET's `HttpIOException`, does when a body ends mid-read.
- Whether Windows checks the generated files out with LF only. The `.gitattributes` is relayed, not measured on Windows. A CR LF checkout would redden the text cell on that leg alone, which the kit treats as a STOP.

## OUTSIDE-THE-FENCES DISCLOSURE
- **The OXPd project:** nothing written in its checkout or records. All git use there was read-only verbs with `--no-optional-locks`, and `gh` used `-X GET` only, under the project's own `GH_CONFIG_DIR`.
- **Clones:** three clones of the origin went into `<d>`. They were made by `clone.py draft` (push URL `invalid://no-push`, no identity), as the commission allows.
- **The shared heavy lock:**
  - Every heavy job took `<project>/.tools/wave1-heavy.lock.d` through `heavy.py` and moved it into `<d>/_quarantine/locks/` afterwards.
  - The drafter waited on B1994's lock once and broke no lock.
  - Restores used the project's package cache under `<project>/.tools/nuget-packages`, read-only in effect: locked mode, a closed proxy, and every lock file equal afterwards.
- **Reads:** no printer, no host other than GitHub, no Jira, nothing under `Source_Documents/`. The drafter read no card store, no scoreboard and no ledger.
- **A stopped background search:** one recursive grep over `tuesday/briefs` timed out and was stopped by the drafter, with no output.
- **A tool quirk:** the Bash tool showed a non-zero `git diff --quiet` as if it were rc 0. The drafter re-ran it and printed the rc through Python (1, as expected). The kit already tells the seat to print every silent command's rc by program.
- **Files written:** only the kit, its sidecar and this report under `tuesday/briefs/`, plus scratch under `<d>`. Nothing was deleted; the planted secret-scan controls were moved to `<d>/_quarantine/`.
