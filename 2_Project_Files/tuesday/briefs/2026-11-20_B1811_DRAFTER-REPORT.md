STARTABLE: YES

# B1811 DRAFTER REPORT (re-commissioned drafter, Fable, read-only) - OXPd 2, WP1.1 round 2, the key-ring fix kit

Written 2026-11-20, 21:12 to 21:43 AEDT (clocks by `date`). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1811_SEAT-X11_oxpd2-wp11-round2-key-ring-checks.md`, 111590 bytes, 307 lines, sha256 `44aaaedff595288facc8a89fc140bfb9b31cc4701da716874ac280a55bed93d1`, 8 unfilled slot lines (S1 to S7 and the last line), ASCII. Sidecar `.measured` beside it: 42536 bytes, 209 claims, `stamp_check.py` exits 0 (168 lines carry a run or a RELAYED source, 41 are instructions with nothing to run). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s301/d1811/`.

## BLUF
1. The kit is startable after a stamp, on its defaults. It is a LARGE round for one seat (16 decisions, at least 41 new tests, a spike first): the windows are 240 minutes to READY and 200 to the push (Q16), with the context band and a handover form.
2. **Nothing in the kit about the fixed code is proven by a run.** The drafter built nothing and ran no test. The mechanism rests on a READ of the library's public source at tag `v10.0.15` and of one documentation page, both fetched by GET today. The seat's Step 2 (a spike of nine rows) is the first proof, and the kit stops the seat if a row contradicts D1 to D4.
3. **Three places where Tuesday should look before stamping, because the default is not what the commission's wording expects:**
   - **Q8: the owner check of the key file is NOT delivered (ruling 4(b) asks for it in bold).** Default: a named limit. Reason: this framework has no call that returns a file's owner (from memory; spike row s5 prints what it offers), and no test of this repository can make a file owned by another account that still opens, so the check could not be seen red. The alternative (an indirect probe on the open handle) is written in Q8 with its cost.
   - **Q7 and D7: "every check on the open handle" cannot be delivered either.** At the head the length, the mode and the bytes are ALREADY read from the open handle; the link check and the plain-file kind are by path, and the drafter knows of no open in this framework that refuses a link. The link window stays a named limit; the review's race row will still count loads through a link at the new head.
   - **Q2: switching automatic key generation off (ruling 2's example) forces a second decision.** By the library's source, a ring whose newest key has passed its end date can leave the library with nothing to protect under, and the store would refuse every write from day 90. Default: every key the store makes gets 36500 days, replaced by `RotateKey` only. This changes Tuesday's own D13 of the first kit (90 days).
4. **Two things the drafter found by reading that the verdict does not hold (both UNMEASURED, both in the kit as cells):**
   - A decoy key file: the store's own protected element moved one level deeper and a clear `masterKey` beside it would, by the library's source, open and name the store's decryptor exactly once. The review's one-line rule for finding 2 ("exactly one encrypted element naming the store's own decryptor") would let it through. D4 (c) asks four things for that reason; cell R08.
   - The library re-reads its key folder on its own and can then seal under another key (the review's own refresh log shows 11 of 12 writes moving to the second key). A guard after that re-read can only be tested by waiting for it. D3 therefore gives the library no folder at all: the store hands it a repository that serves only verified entries. This is more code than the commission's example; the cheaper alternative is Q1's C.
5. The review's own attack program will STOP at two lines when run unchanged at a fixed head (`Program.cs:286` and `:617`), because the fix works. The kit tells the seat to show that and run a copy with only that statement guarded. The round-2 review will meet the same two lines.

## The re-commission: what the earlier drafter left
- No kit, no sidecar and no report existed. The earlier drafter's scratch `fleet/state/s301/d1811/` held: `gate/` (152 files), `gate-manifest.txt`, `tools/copy_gate.py`, `tools/scan_gate.py`, `docs/` (two documentation pages).
- Nothing was deleted, moved or overwritten. I read both tools, then re-ran them: the copy program found every file already present and byte-equal to its source (it refuses on a difference) and rewrote the manifest with the same 152 rows; the scan ran fresh. I continued from that copy. `docs/configuration-overview.md` is byte-equal to my own GET of the same page (`cmp`).

## The copy of the review's files (commission, bold paragraph)
- `fleet/state/s301/d1811/gate/`: **152 files, 605053 bytes** (scratch 14 files 52904 bytes; logs 131 files 366300; probes/Attack 2 files 66495; api 4 files 112838; api/docs 1 file 6516). Each byte-equal to its source at 21:12:33; sizes and sha256 in `gate-manifest.txt`; re-checked at 21:38 (152 rows, 0 differ; control: a changed byte is seen).
- The 37 mutants are the entries of `scratch/mutants.py` (53 entries: the builder's 16 and the review's 37). The second reader's notes: only `scratch/second-reader-contract.md` exists as a file; the second reader's findings are in VERDICT.md itself.
- **Left out on purpose:** `stores/` and `tmp/` (the review's throwaway stores, key files and key rings), `clone/`, `probes/Attack/bin` and `obj`, `mut/tree`, `nuget-packages/`, `dotnet-home/`, `out/`, `_quarantine/`.
- **Key-material scan of the copy:** needles read in memory from the review's own stores (40 distinct 32-byte key files; 510 distinct encrypted-entry texts of its key rings), searched raw, as hex in both cases and as base64: **0 of 152 files hold one.** Control: a planted random value was found in 152 of 152 in-memory copies and in 0 files as they are. 0 files are named like a key file, a ring entry, a revocation or a record (control fires). Three files hold long hex runs (two hosted logs and `scope.py`): identifiers and hashes, not needles.

## What is proven by a run, and what is not
**Measured by the drafter (instrument beside each; outputs under the scratch folder):**
- The origin, `gh api -X GET`, 21:24:24 to 21:24:27 (`origin.out`): `main` 7bf37526, the lane branch 42f926d5, compare ahead 1 behind 0 files 30, four check runs success, one pull request (number 1, merged), 0 tags, six branches (the logging branch has moved to 6bcd02ed, the card-decoder branch exists).
- The source at the head, in the review's clone (HEAD 42f926d5, clean, 55 files): every `file:line` of the kit, by program (`facts.out`); 25 indented `[Fact`, 0 at column 1, no theory.
- The solution file order (`facts.out`): the review's reading is RIGHT. File order Core, Server, Secrets; ordinal order Core, Secrets, Server (index 20: `c` 0x63 against `r` 0x72). Block SLNX 11 lines, 501 bytes, sha256 147fe7ac...593b4, equal to the review's own file; numstat from the head 1 added 1 removed.
- The review's logs, recounted: 53 mutant rows, 36 killed, 17 survived; 4 `RUNNING` rows; 39 `KEYRING` rows (18 started, 20 typed, 1 raw); 41 `KEYFILE` rows; 6 hangs.
- The library's public source at `v10.0.15` (12 files by GET) and the documentation page: the lines the kit cites.
- Toolchain by path (10.0.404, 8.30.1), the neighbours, the pane list (one OXPd2 pane at 21:38: X9), the reading load 464869 bytes, the commit subject 91 bytes (scanner rc 0).
- The checks of FACT 12 marked PASS, each with its control fired (`proto.out`).

**NOT proven by any run (all in the kit as DERIVED or UNMEASURED):** every statement about what the fixed store does; that `DisableAutomaticKeyGeneration`, a custom repository and a 36500-day key behave as the source reads; what the head does with the decoy and with a key under another protection; that a named pipe reads length 0 by path on this machine in the seat's hands (RELAYED from the logging lane) and on Linux; anything on Windows; every "after" row of the review's table; the cost of the checks in time.

## Every STOP-severity check NOT run on a prototype (marked so in the kit, FACT 12)
The baseline of Step 1(d) (the review's numbers, RELAYED); the build and seven runs of the review's attack program and the equality rule of Step 1(e); every spike row; every "Its red"; every "after" of table RING; the scope program and the two `diff --cached` commands of Step 6(c); the ASCII scan and the name scan on the seat's files; the two expected stops of Step 7; the scans of Step 8(b); the fast-forward proof and the push; the hosted lines and the Windows answer of Step 8(f).

## Chain inputs (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the stamped kit; the three clarification entries | Tuesday; BASE |
| 1 | the origin; the first seat's `clone.py`; the copies under `gate/` | BASE (all exist, measured) |
| 1(e) | the head built in 1(d); `gate/probes/Attack/*` | Step 1(d); BASE |
| 2 | the built head; the restored packages | Step 1(d) |
| 3 | the cells' design; `gate/scratch/mutants.py` | the kit; BASE |
| 4, 5 | the red table of Step 3; the spike rows; the extracted block | Steps 3, 2, 1(f) |
| 6 | the green tree | Steps 4, 5 |
| 7 | the Attack program of 1(e); the new library | Steps 1(e), 5 |
| 8 | the staged tree; the first seat's `run_step.py` | Step 6; BASE (exists: listed) |
| 9 | `history.md` | BASE (exists) |

## Questions for Tuesday, each with its default (all assumed in the kit)
- Q1 mechanism: generation off and the store's own repository. Alternative: the library's file repository with two guards no test can see red without a wait.
- Q2 key lifetime: 36500 days. Alternative: 90 days kept; writes refused from day 90 until a rotation.
- Q3 entry rule: all four parts. Alternative: the review's one-line rule.
- Q4 reads over a broken ring: `TryGet` under a still-held key returns the value. Alternative: the check on reads too.
- Q5 the start: the ruled form (an empty ring beside any record refuses). Alternative: the review's wider rule (every record's key id must be in the ring).
- Q6 an entry of another partition or root under the same key source at a start: a named limit. Alternative: bind the partition into the entry (changes the stored form; not on Windows).
- Q7 the key file's link window: a named limit, no native call.
- Q8 the key file's owner: a named limit. Alternative: an indirect probe, unproven.
- Q9 the pipe: the length rule if the spike reads 0; the swap a named limit.
- Q10 value limit: 1 MiB (the review's 64 MiB row becomes a refusal). Alternative: no limit, a read bound of 256 MiB.
- Q11 new public members: `StorageFailed = 7`, `ValueTooLarge = 8`, `RecordsUnderOlderKeys = 9`, `RevokeOlderKeys(bool abandonRecordsUnderOlderKeys)`, `LocalSecretStore.MaxValueLength`.
- Q12 `ListNames`: opens every record. Alternative: the name rule only, said as unverified.
- Q13 the guard on `RevokeOlderKeys`: in.
- Q14 the three mutants the review calls equivalent (g1, g9, g10): a cell each.
- Q15 the review after: G1 on Fable, round 2.
- Q16 windows: 240 and 200 minutes, pane `Datasec/OXPd2-X11`.

## Where the verdict differs from the commission's summary
1. **Finding 1 (c) is wider than "an emptied key folder":** the verdict also lists a start with the current key revoked through the library, and with the keys folder replaced by a link to another partition's. The kit covers the link (R10) and names the revoked case.
2. **The key file:** the verdict says the length and the mode are ALREADY read from the open handle at the head; only the link and plain-file checks are by path. The summary reads as if every check were by path.
3. **The mutants:** the verdict calls three of the 17 survivors equivalent, "not gaps" (g1, g9, g10). Ruling 4(f) asks a cell for each of the 17; the kit does that by pinning the stored form (Q14).
4. **The guard:** the verdict RULES that the documentation is enough for this lane and a guard is owed before any operator surface. Tuesday's ruling 6 puts the guard in; the kit follows Tuesday.
5. **The key file fix is not on the review's own same-round list.** Its records file names findings 3, 4, 6, 8, 9 and 13 for the same commit; for finding 7 it recommends a README sentence and a backlog line.
6. **`ListNames`:** the verdict recommends the name rule and a README sentence that the listing is unverified; ruling 4(c) is stricter. The kit follows the ruling (Q12).
7. **Two more hangs and one more raw error than the summary names:** a pipe named like a key file stops a new store from starting; a dangling link in the key folder makes `Put` throw AFTER its record was written. Both are in the kit (F06, F02).
8. **The severity in the verdict's own words:** finding 1 is "Blocker by the commission's rule; by its harm a Major".
9. **Not found by the review:** a silent new key at the library's periodic re-read; both of its readers had predicted one. What its log shows instead is the store moving to a second, already opened key.
10. The solution-file numstat: the verdict's "2 added, 0 removed" is against `main`; against the head it is 1 and 1 (measured).

## What I did NOT read
- The first kit whole: I read lines 1 to 10, 126 to 165, 179 to 192 and the lines a search for the lifetime decision returned. Its THE WORK, THE CONTROLS, HEAVY and HOLDS sections are RELAYED through the B1798 kit's form, which I read whole.
- The builder's STATUS beyond lines 116 to 170 and two searches.
- `Program.cs` lines 115 to 217 and 373 to 554 (the record, name, two-store, crash, key-file, pipe, size and algorithm modes); I read 1 to 114, 218 to 372 and 555 to 630.
- `FailClosedTests.cs` and `RoundTripTests.cs` beyond their case heads; `SecretValue.cs`; `KeyRingProtectionTests.cs` lines 126 to 204; `RotationTests.cs` lines 1 to 29.
- The review's landing texts, its commission, its job logs beyond the lines counted; the design files; the kits B1802 and B1810 (the B1802 commission only, as told).
- Of the library's source: only the lines searched for in the twelve files.

## Outside the fences, and my slips
- **No git write, no Jira, no GitHub write, no build, no test, no message.** Hosted reads: `gh api -X GET` only (the origin; `dotnet/aspnetcore` at a tag; `dotnet/AspNetCore.Docs`), under the project's `GH_CONFIG_DIR`. No request carried a name or a project detail beyond the token's own identity.
- **I read the review's `stores/` and `tmp/` in memory** (key files and key-ring entries) to build the needles of the key-material scan, as the earlier drafter's tool does. Nothing of them was copied, written or printed; counts only.
- **I ran the local tool binaries for their versions** (`dotnet --version`, `gitleaks version`) and one `gitleaks dir` over a one-line file of my own. No dotnet build or test.
- **Slip 1:** one `sed -i ''` on my own scratch program (`prog/sidecar.py`), where the rules ask for the Edit tool or a rebuild. No other file touched; the line it changed was rebuilt by program afterwards.
- **Slip 2:** my first sed set the load figure in that program two bytes low (464741 for 464743); caught by the load program in the same step, and the figure is now read from the kit, not typed.
- **Slip 3:** the first draft of the kit put a paraphrase of the review's wider start rule inside quotation marks, said a count of 45 new tests where the arithmetic gives 41, said 5 lines hold `skipped` where 6 do, and quoted a library comment with one tag reworded. All four were found by my own checks before this report and corrected by program.
- **Slip 4:** at 21:25 my pane filter printed no row and the first draft said no OXPd2 pane existed; at 21:38 the same command listed X9. The kit carries the later reading with both clocks.
- The kit and the sidecar were written by the Write tool and then corrected by small programs that rebuild the whole file and `os.replace` it (four passes), not by the Edit tool.
- I did not run `decision_queue.sh`, read no ledger, no staged brief, and no file of another seat's tree.

## Ten-line summary
1. STARTABLE YES. Kit 111590 bytes, sidecar 42536 bytes, `stamp_check` rc 0, 8 open slots.
2. The earlier drafter left a verified copy of the review's files and two tools; nothing was deleted; I continued from it.
3. Copy for round 2: `fleet/state/s301/d1811/gate/`, 152 files, 605053 bytes, no key material (scan with a planted control).
4. The fix is by property: generation off, the library given no folder, a full check at start and key operations, a light check before every write.
5. Nothing about the fixed code is proven by a run; the seat's spike is the first proof and can stop it.
6. Ruling 4(b) is NOT delivered as worded: no owner check (Q8) and the link window stays (Q7).
7. Switching generation off forces a key lifetime decision (Q2); the default changes the first kit's D13.
8. A decoy key file the review's rule would let through is in the kit as cell R08 (unmeasured).
9. The value limit of 1 MiB turns the review's 64 MiB row into a refusal (Q10).
10. The review's attack program stops at two lines against a fixed head; the kit says how the seat shows it.
