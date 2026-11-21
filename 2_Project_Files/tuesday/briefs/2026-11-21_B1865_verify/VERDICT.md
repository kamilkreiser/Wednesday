GATE B1865: GO WITH FINDINGS @ 8578d96 on main 977cbeb (second reader)

# Second reader, round 2 (delta): P01 to P11, the free race, the ring check, D22 (a), at `8578d96c`

Reader B1865 (Opus), in session, 2026-11-21 21:11 to 21:28 AEDT. This round follows round-1 reader B1855. Yardstick: `2026-11-21_B1855_verify/VERDICT.md` and its probe file. Scope: the kit B1857 FOR TUESDAY items for B1865, D22 (a), the scope and frozen-file checks, the suite, the hosted run, and deviations 1 and 4. The merge build, the 72 rows, G11, G12 and the landing texts belong to B1864.

## BLUF
- **GO WITH FINDINGS. There is no Blocker and no Major.** Round 1's Major F1 is closed: no measured shape removes a record that reads. P11 (the round-1 Major's shape) now ends with a typed `KeyNotAvailable`, and the file is kept and reads after the release. A sweep of 0 to 24 free descriptors over 2 runs, with the decoder warm (P11C), removed nothing. With the ring check removed (mNoRing), the same shape ends `StorageFailed` and the file is still kept. So the record is guarded twice.
- P08 and P09 now end `KeyNotAvailable` with nothing removed, and a restart reads both of P09's records. In P12 (new), after the OTHER store rotated, the stale store refused 50 of 50 removals, while the current store still removed each corrupted record. The one-store races still show 0 readable-at-removal: P04 0 of 60, and the free race 0 of 891 removals. mR1 now turns U21 red.
- **D22 (a): graded a records limit (Minor), not Major** (reasoning below; my P13 measured the Unix analogue).
- New finding F1 (Minor, records, store-wide, already on main): a process with no free descriptor and a JSON decoder not yet loaded throws an untyped `FileNotFoundException` from every read member. That includes the frozen `TryGet` and `ListNames` as well as this lane's two members. The runtime keeps that failed load, so after the descriptors are freed it goes on until the process restarts. Nothing is removed.

## How it was measured
- **Clone.** In my session scratchpad (`.../scratchpad/b1865/clone`), cloned from the seat's clone, read only, with push URL `invalid://no-push`, checked out at `8578d96c7881b7023d707600c5e2f0b03722d8d1`. Its parent is `a5ba020b...` and only that one. Tree `63b412f6...` equals GitHub's tree for the branch head, read by `gh api -X GET` at 21:12:27. Main is `977cbeb2...`, and 0 pull requests are open.
- **Lock.** Every dotnet job went through kit B1857's `heavy.py`, copied unchanged (sha256 `31adedc8...`). It takes the wave lock by `mkdir`, writes `owner.txt` and releases the lock by a move. Three batches ran, each as one job: A 21:16 to 21:23, B 21:23 to 21:25 (after 1 wait), C 21:26 (after 6 waits). The restore ran with `-p:NuGetAudit=false`: rc 0, and `git status` was empty before and after, so no lock file changed. `--source-documents` was never passed and no key folder was opened. Every value is synthetic and nothing printed holds a value.
- **Probes.** The round-1 file was carried forward with the kit's expected changes, plus P11B, P11C, P12 and P13. It is scratch only, never committed, with a copy at `evidence/SecondReaderProbes.cs.txt`. The P11 family runs only with `PROBE_EMFILE=1`, each probe alone in its own process.

## Results at the new head
| Item | Result | Evidence |
|---|---|---|
| **The whole suite (solution), probes aside** | build 0 warnings and 0 errors; `Passed!`, `total: 920`, `failed: 0`, `succeeded: 916`, `skipped: 4` | `A-suite.log` |
| **The store's test project plus my probes** | `total: 104` (the project's 89 and my 15), `failed: 0`, `skipped: 4` | `B-test-head.log` |
| **Hosted run of 8578d96c, by GET** | `HOSTED 8578d96c...: PASS` with `--total 920 --rules 295 --skipped-linux 4 --skipped-windows 19 --unit 60 --floor 60`; 4 jobs `success`, `Ran 60`, floor 60, `RULES: clean (295 files)`. Control `--total 921`: `FAIL 4`. No skipped test on the Windows log names a lane test | `hosted-8578d96c.txt` |
| P01 hard link from p2 | removed this path only; p2 still reads (unchanged) | `probe-out/head.txt` |
| P02 readable again after the listing | `DeleteUnreadable` false and the record kept; `Delete(StatedName)` removes it, as the README now says | same |
| P03 hostile texts | 6 null, the escaped name set, 200 characters set, 201 null (unchanged) | same |
| **P04 planted interleaving, one store** | 60 iterations, 60 removals, **0 readable-at-removal**, 0 lost | same |
| **P05 free race, one store** | about 20 s: **2101 passes, 901 `DeleteUnreadable` calls, 891 removals, 891 oracle checks, 0 readable-at-removal**, 1318 corruptions, 2273 repairs, 92 rounds of RotateKey, Rewrap and RevokeOlderKeys, 0 errors | same |
| P06 two stores, planted | 200 of 200 removals took a record the removing store read (the named limit H28, still able to remove, as expected) | same |
| P07 two stores, free race | 2000 passes, 40 calls, 33 removals, 0 readable-at-removal this run, 0 refusals (no rotation, so no `KeyNotAvailable`, as expected) | same |
| **P08** (U14's shape) | the second store refuses `Put` AND `DeleteUnreadable` with `KeyNotAvailable`; the first store and a fresh store read the record | same |
| **P09** (revocation moved out) | the running store lists 2 unreadable and refuses `Put` and both removals with `KeyNotAvailable`; **a restart reads both** | same |
| P10 | the record put again is kept; the abandoned one is removed (unchanged) | same |
| **P11** (round 1's Major), alone, 2 runs | `ListAll` `StorageFailed`; `DeleteUnreadable` `KeyNotAvailable`; file kept; reads after. Under mNoRing it is `StorageFailed`, kept. Under mRound1 (round 1's path) it is `True`, removed (positive control) | `probe-out/B-head-alone.txt`, `B-mNoRing-alone.txt`, `mRound1-...-p11.txt` |
| **P11C** (new) decoder warm, free descriptors 0 to 24, 2 runs | 0 removals (k0 `KeyNotAvailable`, k1 to k24 false); after release this store and a new store read both values | `B-head-alone.txt` |
| P11B (new) decoder cold, the same sweep, 2 runs | **0 removals** (k0 `KeyNotAvailable`; k1 to k24 untyped `FileNotFoundException`, see F1); file kept | `probe-out/C-p11b.txt`, `C-p11b-1.log` |
| **P12** (new) after the other store rotated | 50 iterations: stale-store removals 0, `KeyNotAvailable` 50; the current store removed each corrupted record | `head.txt` |
| P13 (new) D22 (a) Unix analogue | see D22 (a) below | `B-head.txt` |

## Mutants (mine, re-made independently; each one heavy run; the store's test project with my probes; each undone and proved by `git diff --quiet` rc 0)
| Mutant | Change | Red, by assertion |
|---|---|---|
| **mR1** | `Judge` moved before the lock (the ring check and the removal stay under it) | **U21**, P04 (60 of 60 readable-at-removal), P05 (112) |
| **mR2** | the removal trusts the last `ListAll` verdict | U04, U07, U15, U19, U21, P02, P04, P05, P06, P12 |
| mOneTry | `Judge` back to one `try` (D14 undone), ring check kept | U04, U15, U19. U16 and P11 stay green: the ring check meets the fault first |
| mRound1 | one `try` and no ring check (round 1's path) | U04, U14, U15, U16, U17, U18, U19, P08, P09, P12, P11 and P11B (removed) |
| mNoRing | the ring check in `DeleteUnreadable` removed (the seat's mutant, re-made) | U14, U17, U18, P08, P09, P12. U16 and P11 stay green (D14 gives `StorageFailed`) |
After the last undo, `src` is clean and the head is rebuilt (0 warnings). Logs: `batchA.log`, `batchB.log`.

## Scope and frozen parts (item 3)
- `a5ba020b..8578d96c`: exactly 4 `M` rows (`ISecretStoreInventory.cs`, `LocalSecretStore.cs`, `README.md`, `InventoryTests.cs`), with no `A`, `D` or `R`.
- `git diff --quiet a5ba020b 8578d96c` over `FileSecretRecordStore.cs`, `ISecretStore.cs`, `ISecretStoreMaintenance.cs`, the other five frozen source files, `*.csproj`, `*packages.lock.json`, `Datasec.Suite.slnx`, `Directory.Packages.props`, `.github` and `build`: rc 0.
- The three named frozen files against `61b17ec0`: rc 0. Control: `README.md`, rc 1.
- Test files changed since `61b17ec0`: only `InventoryTests.cs`.
- The `ListNames()` block (61b17ec0 lines 199 to 218: 20 lines, 715 bytes, sha256 `5f03bc97...`) occurs exactly once in the head file. The control with one more space occurs 0 times.
- The 568 added lines and the commit message:
  - `words.py`: control `CONTROL FIRED: 13 of 13`, then `WORDS: clean (2 files)`, with 0 `_gate` tokens.
  - gitleaks 8.30.1: control rc 1, `leaks found: 1`. The two files under neutral names: rc 0. The evidence folder: rc 0.
- Main since `61b17ec0`: 76 files, 0 under the store's two folders. `git merge-tree --write-tree 977cbeb2 8578d96c` gave rc 0 and tree `20c68f46...`, so the merge is clean. The merged tree was not built: that is B1864's item.

## D22 (a), graded: a records limit (Minor), not Major
The concern: on Windows the ring check does not prove DPAPI-NG can decrypt, so a transient decryption fault that is not the record's own reads as `DoesNotRead` and the record is removed. `Open` maps every library failure to `UnreadableRecord`.
1. **Nothing calls the removal.** `git grep -E 'DeleteUnreadable|ListAll\(|ISecretStoreInventory' 977cbeb2 -- src tests` finds 0 lines. Control: `ListNames(` has 1 caller in `src/Datasec.Suite.Sessions/SecretStoreSessionRecordStore.cs:52`. In the head, only the store and its own test file name `DeleteUnreadable`.
2. **Measured, Unix analogue (P13).** A key source of the probe's own refuses exactly once, and only when the key-ring decryptor asks it, so the ring check's own question is still answered. In a new store over records under an older key and under the current key, the decryptor was called **2 times at open and 0 times at the removal**, and the refusal never fired. `DeleteUnreadable` returned false and both records read, in that store and in a fresh one. The library opens the key-ring entries when the store opens, not once per record. DERIVED for Windows: the same library path calls the DPAPI-NG decryptor in the same place, so the moment it can fail is the store's open, which fails the open, or a later reload of the key ring by the library. A reload after the library's cache expires is UNMEASURED: it is the residual window.
3. **Measured: a process fault does not reach `Open`'s catch-all.** P11C, with the decoder warm, ran 25 steps of descriptor headroom twice, and the removal reached `Open` at k1 to k24 with no removal.
4. Ruling 1 counts "does not open/decrypt with the ring" as a record failure. The README names the limit in plain words ("not measured here").
- **Why not Major:** no caller exists. The measured analogue shows decryption is not done per record at the removal. The residual window, a key-ring reload that fails for one key, is narrow and named.
- **Precondition before any caller is wired (NOT DECIDED item 1):** the smallest fix, if it is ever graded Major, is this. When the `DoesNotRead` verdict came from `Open` (not from `ReadHeader` or the name rule), the removal first requires that the record's key id is a key of this store's ring that is not revoked, and that a protect and unprotect round trip of a probe value succeeds under the current key. Failing either gives `StorageFailed`, with nothing removed. About 10 lines in `LocalSecretStore.cs`, with no frozen file touched.

## Deviations
- **1 (U16 runs both calls in one `Bounded` thread started before the limit is lowered): accepted.** I read the cell. The guarded thread lowers the limit, fills the table, makes both calls and restores the limit in its own `finally`. The test thread restores it again unless rc was 0, and asserts `restored == 0`. The 10 s bound still covers every call. The reason was measured (`Thread.Start` threw `OutOfMemoryException` with no descriptor left). Note: U16 tests 0 headroom only, inside a warm test host. P11B shows a cold process gives untyped throws at 1 or more headroom (F1), so U16 is stable as written.
- **4 (mNoRing's undo proved only together with mBoth): accepted.** I re-made mNoRing alone. It turned U14, U17 and U18 red (and P08, P09 and P12), and left U16 and P11 green because D14 alone gives `StorageFailed`. The undo was proved by `git diff --quiet` rc 0.
- 2, 3, 5 and 6: read, and nothing against them (B1864 rules on them). 2 widens `Fresh` and `Bounded` to `internal` and changes no behaviour. 3 is a label split, a choice the kit left to the seat. 5 was an invocation error the seat re-ran in the kit's form. 6 is wrappers around the unchanged `heavy.py`.

## Findings
| # | Severity | Finding | Fix shape |
|---|---|---|---|
| F1 | Minor (records; store-wide; already on main in the frozen `SecretRecord.cs`; nothing removed) | **Untyped `FileNotFoundException` under descriptor exhaustion with a cold decoder, kept by the runtime.** Suppose the first record decode in a process happens while 1 or more descriptors are free but too few for a load. Then `System.Text.Json`'s `JsonDocument.Dispose` fails to load `System.IO.Pipelines`. `SecretRecord.Decode` catches only `JsonException`, `KeyNotFoundException`, `InvalidOperationException` and `FormatException`, so `FileNotFoundException` leaves `ListAll` and `DeleteUnreadable`, and the frozen `TryGet` and `ListNames` too. **After the descriptors are freed the runtime has kept the failed load, so every decode in that process keeps throwing, for a new store too, until restart.** Measured 2 of 2 in P11B. The record file was kept, and 0 removals were made. This lane's members inherit it, and the lane cannot fix it, because the cause is in the frozen decoder. A server that decodes at start-up is unlikely to meet it. | A later store kit, not this lane: type a runtime fault inside `Decode` (`FileNotFoundException`, `FileLoadException`, `TypeInitializationException`) as **`StorageFailed`, never `UnreadableRecord`**. Typed as `UnreadableRecord`, the kept failure would make EVERY record `DoesNotRead` in that process, and `DeleteUnreadable` would remove them all. Optionally warm the decoder when the store opens. |
| F2 | Minor (text) | The README's `DeleteUnreadable` sentence lists "no file descriptor left" among the cases that throw `StorageFailed`. With the ring check first, that shape throws **`KeyNotAvailable`**: P11, 2 of 2, and the kit's own D17 note. It is `StorageFailed` only when the ring check passes and the record's own open fails (mNoRing). Nothing is removed either way. | One clause: "(with no descriptor left, the ring check usually refuses first: `KeyNotAvailable`)". It can wait for the next store change. |
| F3 | Minor (records) | D22 (a) as graded above: a named limit with a residual window (a key-ring reload that fails for one key), unmeasured on Windows. | The precondition above, before any caller. |
Round 1's F2 to F5 are closed by text and cells (README bullets read; P02, P06, P08, P09 and U21 measured). F1 of round 1 is closed (above).

## NOT tested
- Windows and Linux locally (this machine is macOS arm64). DPAPI-NG itself. The library's key-ring reload after its cache expires. `EIO`, `ENFILE`.
- The merged tree's build, its total of 1191 and the rules count of 370, the 72 rows, G11, G12 and the landing texts (B1864's items). I measured only the merge's cleanness.
- A second PROCESS (only two stores in one process stand for it, as in round 1). CodeQL: NOT RUN.
