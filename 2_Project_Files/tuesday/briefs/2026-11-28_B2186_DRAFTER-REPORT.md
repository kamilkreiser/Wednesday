STARTABLE: NO (the kit is complete and stampable: `stamp_check.py` exits 0 with 198 of 198 claims measured. It cannot START until its own base exists, because L1c (seat X94) has to land on `main` first. Its REFUSE fires on today's `main` `7d652c5f` by design. Once L1c lands, it is startable after the stamp answers Q1 and Q2 in words.)

# B2186 (seat X95, lane L1x) drafter report: the OXPd 1.x context calls

Read-only drafter (Opus) for Tuesday s336. Commission: `tuesday/briefs/2026-11-28_B2184-B2189_OXPD-WEEKEND-KITS_COMMISSION.md`, section 3. First `date`: Sat 28 Nov 2026 00:07:38 AEDT. Kit written from 00:22:59 AEDT; sidecar last written about 00:31 AEDT (its first line holds the clock printed by `date` in the writing process); this report 00:32 AEDT onward. Outputs: the kit `2026-11-28_B2186_SEAT-X95_oxpd2-l1x-context-calls.md` (sha256 at 00:32:06 `43c00bfa...`, about 99 KB, 9 stamp slots unfilled), its `.measured` (198 lines), and this report. Scratch: `fleet/state/s336/d2186/`.

## BLUF
1. **The lane in one line:** one NEW file `src/Datasec.Suite.Adapters.Oxpd1/Oxpd1Context.cs` adds a public `Oxpd1ContextCaller`. It makes six calls from a closed list (`Oxpd1ContextKind`): Reserve/ReleaseAuthenticationContext, HidOpen, HidStartReading, HidStopReading and HidClose. Each call is a dry run unless `Execute` is set, carries its undo when it may have taken effect, and goes out as `guest` through the landed internal `Oxpd1Client.SendGuestAsync`. This is the `Oxpd1Echo` form plus the `Oxpd1Writer` dry-run and undo rule. One NEW file `tests/.../ContextTests.cs` adds N01 to N10: 5 Facts and 5 Theories with 34 rows, 39 cases, run against the landed `StubDevice` through `ForceBody`/`ForceStatus`. There are eight mutants with frozen red cells. No landed line changes: the commit is two `A` rows and nothing else.
2. **Whether L1x needs L1c, judged from the paths: it does not need its files.** All six operations are already committed at `7d652c5f`: `authentication.wsdl:200` and `:238`, and `AccessoriesSoap12Binding.wsdl:61`, `:79`, `:97`, `:106` (MEASURED). The base after L1c is sequencing only, as the commission and plan line 111 set it, and the kit REFUSES as commissioned (Q3 records the alternative). Two runtime couplings make "after, never beside" the right call anyway:
   - the stub reads every committed binding at each start;
   - `StubDevice.cs:200` pins seven ports.
3. **OX-A was found and made a REFUSE.** It is SWEEP-0446's lane on the OXPd 1.x client, which "owns `src/Datasec.Suite.Adapters.Oxpd1/**` and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/**` and that module's README" (`2026-11-26_SWEEP-0446_datasec-actionable-lanes.md:195`, MEASURED by `sed -n`). The kit refuses in any of these cases:
   - a live L6, OX-A or L1c pane, even when S3 names it as allowed;
   - an OPEN pull request that touches either module folder;
   - a `main` that changed `src/Datasec.Suite.Adapters.Oxpd1/**` since `7d652c5f`.
4. **Finding for Tuesday about the sibling L1c:** the commission gives L1c `contracts/oxpd1/**` and `ContractTests.cs` but not `StubDevice.cs`. That file pins seven ports (`StubDevice.cs:200`), and PR 43 had to change it when it added three bindings (`gh api -X GET .../commits/c5b103ee` lists `tests/.../StubDevice.cs` as modified, MEASURED). X94's kit, read at 00:32, already handles this: "`StubDevice.cs` (M, lines 200 and 202 only ... ONLY with S4 Q2 = IN)". My kit's moved-main test admits L1c's edits to `ContractTests.cs` and `StubDevice.cs` and refuses any other change in the module folders. **If X94's Q2 is answered OUT and L1c adds a binding with a port, every stub cell (landed and mine) throws.** My Step 1 BASE local run then STOPs on `Failed:` above 0.

## Facts re-measured (instrument named)
- **Origin** (`gh api -X GET` under the project `GH_CONFIG_DIR`, 00:08:12 AEDT): `main` = `7d652c5f0f8d9854aaf49b43df79e77855eccb46`, tree `760295e3...`, parent `760e1a64`, PR 59. Open PRs: 0. `matching-refs/heads/b2` gives 20 rows, none `b2185` or `b2186`.
- **Hosted run of main** (`hosted3.py`, 00:21:18 AEDT, `<d>/gen/hosted-base.out`): `HOSTED 7d652c5f...: PASS` at `--total 2433 --rules 679 --skipped 4/21 --guard 14/15`. Control `--total 2434` gave `FAIL 4`, rc 1.
- **BASE tree**: the tarball by `gh api -X GET` holds 679 files. `git write-tree` in a scratch repository gives `760295e3`, equal to main's tree.
- **OXPd 1.x test project at `7d652c5f`** (python over every `.cs` file): `[Fact` 48, `[Theory` 13, `[InlineData` 85, column-1 0, `MemberData`/`ClassData` 0. Executable Total 133, DERIVED: the hosted log prints no per-executable total.
- **The client surface** (`grep -n`): `SendGuestAsync` at `Oxpd1Client.cs:139` and `SendAdminReadAsync` at `:120`, both `internal`. `InternalsVisibleTo` (`Datasec.Suite.Adapters.Oxpd1.csproj:6`) names the test project only. `ContractTests.C04` checks only `typeof(Oxpd1Client)`'s public methods (`ContractTests.cs:122` to `:135`, read), so a new public class does not trip it.
- **The stub admits `admin` only on its SOAP path** (`StubDevice.cs:369`). It answers `ForceStatus` and `ForceBody` before the credential check (lines 320 and 331), after recording the request (line 301). The guest cells therefore script every answer.
- **The M577 accepts guest for the echo**: "`SyncEchoString: Answered 200 after 424 ms`" (X88 STATUS line 28, RELAYED). Whether it accepts guest for the six calls is UNMEASURED.
- **gitleaks 8.30.1**: `Password = "synthetic-guest-0001"` is flagged `generic-api-key`, while the landed `synthetic-admin-0001` is clean (MEASURED, `<d>/gen/gitleaks-literal.out`). The kit makes the cells use the landed literal (D7). Without this the seat's pre-commit scan would have STOPPED.
- **Seat id**: `X95` appears in 0 file names in both briefs folders. In text it appears only in the commission (`grep -l` with a word-boundary ERE; control: X84 in 8 files).
- **Panes at 00:32**: `Datasec/OXPd2-X93`, `-X94` and `-X97` are live, and X84's pane is no longer listed. Tuesday reads S3 against this at the stamp.

## What the drafter ran (all in scratch, all NOT dotnet)
Each run and its result:
- **`checks_l1x.py` (new, nine checks, each with a control)**:
  - over BASE's own index: `CHECKS: 3 of 9 PASS`, every control FIRED (`<d>/gen/checks-base.out`, run under a temporary `GIT_INDEX_FILE`);
  - over the staged prototype: `CHECKS: 9 of 9 PASS` (`<d>/gen/checks-sim.out`).
- **`words.py`**: `--control` gave `CONTROL FIRED: 13 of 13`. Over the prototype's 710 added lines and the commit message: `WORDS: clean (2 files)`.
- **`mutants_c3.py`**:
  - `--list` over the 8 prototype rows: `LIST: 8 mutants, 1 suites, 10 cells`, rc 0;
  - a bad row under `src/Datasec.Suite.Lab/`: `LIST REFUSED: rows mBad`, rc 1;
  - `apply` then `undo` of each of the 8 over the prototype: `equal True` eight times.
- **gitleaks**: the control (a planted key pair) gave `leaks found: 2`. The seat tools, the prototype and the added lines gave `no leaks found`.
- **The prototype**: `<d>/proto/` holds `Oxpd1Context.cs` (sha `8954e2eb...`) and `ContextTests.cs` (sha `4c172491...`). The rows are in `<d>/gen/mutants_l1x.proto.json` (sha `377a9c6f...`). **No compiler has read the prototype, and it is NOT handed to the seat.** The seat writes to THE CODE and THE NEW CELLS, as in the X86 form.
- **Seat tools**: `<d>/seat-tools/` holds 8 files. Six are kit B2153's byte for byte (6 of 6 sha256 equal to `fleet/state/s333/d2153/seat-tools/`): `clone`, `heavy` (canonical `31adedc8...`), `hosted3`, `mutants_c3`, `run_step`, `words`. Two are new: `checks_l1x.py` (`4fbcd5e1...`) and `commit-message.txt` (`e7b3e6a7...`; 328 bytes, 3 lines, subject 270 characters).

## Chain inputs (MEASURED LITERALS rule 4)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp S1-S8 (S2 must hold main AND L1c's sha) | Tuesday's stamp |
| 1 | `<src>` (8 files), `<repo>` local values, the origin, BASE's push run | drafter scratch (exists), `<repo>` (exists), GitHub |
| 2 | BASE files, the committed descriptions | Step 1 clone |
| 3 | THE CODE, THE NEW CELLS; the restored and built clone | kit; Step 1 |
| 4 | the pinned tree; `mutants_c3.py`; the rows file the seat writes in Step 4 before its run | Step 3; Step 1; Step 4 |
| 5 | the green tree with mutants undone | Step 4 |
| 6 | the staged tree; `checks_l1x.py`, `words.py`, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit; `origin/main`; `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

No step needs a file that a later step makes.

## D-decisions (mine, for Tuesday to accept or refuse)
- **D1:** one class over the landed internal sender. No second client and no `InternalsVisibleTo` line: the X87 report's refusal stands.
- **D2:** the guest user (Q1, STOP-class). This is the least credential HP's text admits ("either guest or device administrator credentials", `authentication.wsdl:211`, `:244`, and 13 lines of `accessories.wsdl`). The echo precedent is guest too. Switching to admin is a one-word change (`mAdminUser` proves that the cells see the difference).
- **D3:** dry run plus undo, in the `Oxpd1Writer` form (Q2, STOP-class). The undo order follows HP's "Reading must be explicitly stopped before closing" (`accessories.wsdl:634`).
- **D4:** the nonce is checked on both sides by ONE `IsNonce`, HP `common:Nonce` (common.xsd:570-580). A reserve answered with anything else ends as `MalformedAnswer`, with no id and no undo.
- **D5-D6:** arguments are checked when the call is made (the echo's rule). No id appears in any `ToString`: the record's generated `ToString` is overridden. **The client's record file DOES hold the context ids** (named limit R10, Q5): a scrub needs `Oxpd1Client.cs`, which is OX-A's path.
- **D7:** new files only. The README is not touched, because the commission says "new files only" and SWEEP-0446 gives the README to OX-A (Q4). The cells use the landed literal `synthetic-admin-0001` (the gitleaks fact above).
- **D8:** the cell prefix is `N`. The landed prefixes in this project are A, B, C, K, T, V and W. `X`-digits is avoided because `words.py` reads it as a seat id.
- **Gate tier G1** (`model-routing.md:108`). The lane is a credential and device-state surface and handles context ids that let a holder sign a user out.
- **Lock waits:** about 90 minutes in total, not X86's 60, because the plan pairs L1x with L2 (X96) on one lock.

## Q-questions for Tuesday (each with a default; all already assumed in the kit)
- **Q1 (STOP-class): user.** Default **a**: guest. Alternative **b**: admin.
- **Q2 (STOP-class): safety form.** Default **a**: dry run unless `Execute`, with an undo. Alternative **b**: plain calls.
- **Q3: base.** Default: main after L1c lands, as commissioned. Alternative: any `main` before L1c, since L1x reads no L1c file.
- **Q4: README.** Default: unchanged. Alternative: one README section, as a third owned path.
- **Q5: context ids in the record file.** Default: named limit. Alternative: a later OX-A item.
- **Q6: callback binding.** Default: `Soap12`, as the echo. HP says the binding should come from `GetSupportedCallbackBindings` (`accessories.wsdl:540`), and that value is UNMEASURED.
- **Q7: gate, level, windows, pane.** Default: G1, Opus, READY at Step 0 + 240, push by Step 0 + 210, pane `Datasec/OXPd2-X95`, launched after L1c lands and beside L2 only.
- **Q8: names.** Default: `.tools/b2186-x95`, `b2186/x95-oxpd1-context-calls`, `2026-11-28_B2186_X95_*`.
- **Q9: B2172 counting runner.** Default: **NO**.
- **Stamp action (not a question):** S2 must name L1c's landing sha. It must also confirm that L1c's tree holds a `contracts/oxpd1/hp` path with `authenticationagent` in its name. X94's kit takes "the ONE jar folder matching `_service_authenticationagent_<date>`" (read at 00:32), which agrees, but the folder is UNMEASURED until it lands.

## UNMEASURED
- How an M577 answers any of the six calls.
- Whether it accepts guest for them.
- Which callback binding it takes for report events.
- Whether the prototype compiles: no compiler has read it. In particular:
  - whether a `[Theory]` with a `Func` switch over 16 shapes builds warning-free;
  - whether the record type's user-defined `ToString` compiles as written;
  - whether `Assert.Equal` over `string` and `string?` sequences raises a nullable warning. The kit makes any warning the seat's to fix in its own cells.
- Every total and every mutant red is PREDICTED and NEVER RUN.
- L1c's landed tree, which `ContractTests.Schemas()` and `StubDevice.cs` will be after L1c. The kit's Step 2 re-prints both.

## Outside the fences (disclosure)
- **Writes**:
  - the kit, its `.measured` and this report under `tuesday/briefs/`;
  - scratch under `fleet/state/s336/d2186/`: `base.tgz`, `src_7d65/`, `sim/` (a scratch git repository: `init`, `add`, one commit with a scratch-only identity, `read-tree` into a temp index file), `proto/`, `gen/`, `seat-tools/`;
  - two gitleaks control folders moved to `gen/_quarantine/`. Nothing was deleted.
- **No write** in the OXPd project, Jira, GitHub, Azure, cards or mail.
- **No dotnet job and no lock taken.**
- **Network**: `gh api -X GET` only (`hosted3.py` reads job logs by GET). No az, ssh or docker.
- **Project files read** (read-only):
  - `CLAUDE.md` (line numbers and hashes);
  - the X88 STATUS (`grep` lines, under `1_Project_Definition/Briefs/`);
  - `.tools/` listings, and `b2159-l0/gate/heavy.py` hashed.
- **Not opened**: `Source_Documents/`, `4_Credentials/` (beyond `GH_CONFIG_DIR`), key folders, the NAS library.
- **Two hook refusals, no effect**:
  - a `git -C "$D/sim" init` written with a variable path was refused and re-run with a literal path inside TUESDAY;
  - a stray `git -C "$S" stash list` was refused before it ran.
- **A background `grep -r`** over the briefs folder (looking for OX-A) timed out after 120 s. It writes only its own output file and was not needed: the answer came from `sed -n` of the SWEEP file.
- **Sibling files**: B2185's kit was read (by grep) for alignment only. No sibling file was written.
