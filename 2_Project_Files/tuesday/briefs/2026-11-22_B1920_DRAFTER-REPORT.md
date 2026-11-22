STARTABLE: YES

# B1920 DRAFTER REPORT | lane S (seat Datasec/OXPd2-X32): the secret store's removal guard, item 34 N7's cells, N3 and N5

Drafter: in-session Opus, read-only toward the project, Jira and GitHub; 2026-11-22 21:30:22 to 22:00:42 AEDT (both by `date`). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1920_SEAT-X32_oxpd2-s-secret-store-guard.md` (77870 bytes at the sidecar write; sidecar `.measured` beside it; `stamp_check.py <kit>` rc 0, 156 claims, 156 measured: 92 with a run and its output, 64 marked as pointer forms). Scratch and every program behind a number: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1920/` (`gate/` = the kit's `<src>`, `logs/`, `scratch/`, `tools/chain2.py`, `tools/fill.py`, `clone/`, `clone2/`, `_quarantine/`).

## BLUF
- **Six existing files, one commit, no public member changed (proved by reflection, with a control).** Product: `LocalSecretStore.cs` (+44 -2), `FileSecretRecordStore.cs` (+14), `README.md` (+16 -5). Tests: `InventoryTests.cs` (+35, U22), `KeyRingCheckTests.cs` (+67, R17 R18 R19), `GuardAndLimitTests.cs` (+31, G03). Frozen as `1-red-first.patch` and `2-fix.patch`.
- **The guard (42(2)):** before `DeleteUnreadable` removes a `DoesNotRead` record whose payload names an ACTIVE key of the verified ring, a random 32-byte probe must round-trip under the current key, else `StorageFailed`, nothing removed. **Red first at main, measured:** with the store's own data protection services released under it, main REMOVES a good record (U22 red). That is the D22 (a) shape, now measured on macOS.
- **N3 IN** (a linked partition folder is refused at the start, R18). **N5 IN** (the record folder is link-checked at every call, R19). **N2 OUT** (needs a decision: roll back a written key or adopt it). N1 out by the commission.
- **N7:** R17 (a revocation alone with no record) and G03 (the `RevokeOlderKeys` guard over a mixed set). Each is green at main's code, red under its mutant, and green under that mutant with BASE's tests (survivor control).
- **Q1 is STOP-class.** The second reader's sketch, read literally ("the record's key id is a key of this store's ring that is not revoked ... else StorageFailed"), turns two landed cells red: U04 row r2 and U13. Measured as `mLiteralSketch`. The default therefore scopes the guard to records under an active key.

## Facts re-measured (instrument, control)
- Origin (`gh api -X GET`, project GH_CONFIG_DIR, 21:44:44): main `4a0a9717277f60647dfc174e60ec04fc7008e615`, private true, push true, open PRs 0, 21 branches, `matching-refs/heads/b1920` 0. Lane U's pushed `b1915/up-registration-fix-round` is ahead 1 and behind 1, and changes eight `Registration/` files only (compare).
- RED (`<draft2>` at 4a0a9717, test patch only): the whole solution reads `total: 1584`, `failed: 3`, `succeeded: 1577`, `skipped: 4`. The three failures are U22, R18 and R19. Secrets executable: `Total: 94, Errors: 0, Failed: 3`.
- GREEN: `total: 1584`, `failed: 0`, `succeeded: 1580`, `skipped: 4`. Builds `0 Warning(s)`, `0 Error(s)`.
- Mutants (8, `mutants.py`, every `undo cmp 0`):
  - mGuardOff, mGuardKeyInverted, mProbeAlways: RED U22
  - mLiteralSketch: RED U04, U13, U22 (the U04 row is r2)
  - mPartitionLinkOff: RED R18
  - mFolderCheckOff: RED R19
  - mRevocationAloneTaken: RED R17
  - mGuardFirstRecordOnly: RED G03
- Survivor control at BASE's test files: 5 mutants, each `Total: 89 ... Failed: 0`.
- Surface by reflection: BASE = green = `SURFACE: 160 lines, sha256 cd5625c8...218c`. Planted public const: 161 lines, a different sha (control fired). `git diff -U0` public/protected line count: 0 (control 1). `ISecretStore` keeps its 4 members.
- Chain (`<draft2>`): `restore --locked-mode --force` left 24/24 lock files equal; publishes rc 0; `GUARD: clean (10 files)` / `(11 files)`; `Ran 111 tests` OK; `RULES: clean (500 files)`.
- Six files `cmp`-equal between the two clones. A second `apply --check` of the fix was refused (rc 1).
- `words.py`: clean over the patches, message and added lines (207). Control 13/13.
- gitleaks 8.30.1: rc 0 over 9 neutral files and over the clone. Planted control rc 1, quarantined.
- Heavy jobs: every one went through `heavy.py` and the wave lock. Load1 was 6.08 to 7.9; waits up to 4 polls (the lock was once held by X31). Never more than one of mine at a time. No test ran beside another lane's lock except by queueing.

## D-decisions (all coordinator defaults, each a Q in the kit)
- **D1:** the guard is scoped to records under an active key (Q1).
- **D2:** the guard runs on every `DoesNotRead` verdict, not only `Open`'s (Q5).
- **D3, D4:** `StorageFailed` for a linked partition folder and for a swapped record folder (Q3).
- **D5:** N2 out (Q2).
- **D6:** R18 and R19 are skipped on Windows, as R10's link half is. The predicted Windows skipped count goes 19 to 21 (Q6).
- **D7:** one commit.
- **D8:** four README places.
- U22's fault is injected by `((IDisposable)store.ProtectionServices).Dispose()`, an existing internal member (Q4).

## Q-questions for Tuesday (defaults in brackets)
- **Q1 STOP-CLASS (S4 in words):** what scope does the guard take? [Records under an active key; U04 and U13 unchanged.] Alternative: the literal sketch, which changes two landed cells.
- Q2: [N3 and N5 in, N2 out]
- Q3: [StorageFailed]
- Q4: [the released-services fault]
- Q5: [every DoesNotRead]
- Q6: [skip R18 and R19 on Windows]
- Q7: [Opus; READY +150, push +120; pane X32; G1]

## Chain inputs (each produced earlier or present at BASE)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit and its stamp | Tuesday |
| 1 | `<src>` (11 files), the origin, BASE's push run, the SDK `packs/` | `<src>` exists; GitHub; `.tools/dotnet` |
| 2 | BASE's files | Step 1 clone |
| 3 | `1-red-first.patch` | Step 1 |
| 4 | the red tree, `2-fix.patch`, `mutants.py`, `surface-out/` and `surface-base.txt`, BASE's test blobs | Steps 1 and 3 |
| 5 | the green tree, mutants and plant undone | Step 4 |
| 6 | the staged tree and `commit-message.txt` | Steps 1 and 5 |
| 7 | the commit and `origin/main` | Step 6; Step 7 (b) |

## UNMEASURED
- Anything on Linux or Windows. That includes all five cells on the hosted legs, and the Windows skipped total of 21 (PREDICTED).
- DPAPI-NG.
- The residual of the guard: an older active key that fails alone while the current key's probe passes. It cannot be produced on macOS without a fault inside the library.
- The toolchain's `--version` 10.0.404. This is RELAYED from kits B1915 and B1917; my jobs ran that SDK with rc 0 but I did not print the version.
- The neutral-scan wordings of `run_step.py`. These are RELAYED, and NEVER RUN on this lane.
- `hosted2.py` on any head of this lane.

## Outside the fences: disclosure
- **One self-made slip, caught and redone.** In zsh, `git show $B:tests/...` was read as the `:t` modifier, so the first survivor run had empty test files (`Total: 46`). Its output was moved to `_quarantine/survivors-INVALID-empty-test-files.out`, and the run was repeated with `"${B}:path"` (Total 89). The kit now warns the seat about this.
- One `git apply --check` was refused by the workspace no-cd/write hook because the path was given through a shell variable. It was re-issued with the literal path inside my own scratch clone.
- Writes went only to the kit, its sidecar, this report, and the scratch `d1920/`. Nothing was written to the project, its `.tools`, Jira or GitHub. Pushes: none. Both clones have push URL `invalid://no-push`.
- Nothing was read under `Source_Documents/`, the NAS or any key folder. No card was read. No mail or message was sent.
