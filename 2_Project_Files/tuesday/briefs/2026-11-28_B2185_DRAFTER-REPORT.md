STARTABLE: YES (after the stamp answers Q1 and Q2 in words; the seat itself STOPS cleanly at Step 1, with nothing written, if the jar's real contents fall outside the envelope)

# B2185 (seat X94, lane L1c) drafter report: OXPd 1.x agent-side, accessories-callback and scan descriptions

Read-only drafter (Opus) for Tuesday s336. Commission `tuesday/briefs/2026-11-28_B2184-B2189_OXPD-WEEKEND-KITS_COMMISSION.md`, section 2. First `date`: Sat 28 Nov 2026 00:07:34 AEDT. Kit written 00:2x; sidecar and `stamp_check.py` (exit 0, `110 claims, 110 measured`) at 00:24:29 AEDT by `date`.

- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2185_SEAT-X94_oxpd2-l1c-contracts.md` (191 lines, sha256 `c1032a61...`), sidecar `.measured` beside it (sha256 `702d0095...`).
- Seat tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2185/seat-tools/` (seven files; hashes in the kit's THE TOOLS and in `d2185/seat-tools.sha256`). `l1c.py` (sha256 `3b2a6f26...`) and `commit-message.txt` (`7fb1be0b...`) are new. The other five are kit X84's, byte for byte (`heavy.py` = `31adedc8...`, the canonical runner).

## BLUF
1. **I could not read the jar, so the kit freezes a PROPERTY and not the bytes.** The commission fences the NAS library off from drafters. The jar's file names, their number f, their hashes and the new binding ports are therefore UNMEASURED. At Step 1 `l1c.py inventory` selects every entry of the one `authenticationagent` folder, every entry of the one `scan` folder, the accessories entries whose name holds `callback`, and their non-committed imports (at most 8). It replicates the stub's reads and prints `ENVELOPE: PASS` or STOPS. Every later count (C01 = 23 + f, port pin p, rules 679 + f) comes from that inventory. Q1 (STOP-class) default **a**: the seat measures. Alternative **b**: a B2012-style measurement pass first, then a re-draft.
2. **The commission's owned paths are not enough. The stub's port pin must move too (Q2, STOP-class, default IN).** `StubDevice.cs:200` holds `if (ports != 7 || used.Count != 1)`, and every stub-backed cell calls it (`:250`). Any new `*Soap12Binding.wsdl` turns them all red. Lane CT hit the same pin at 4→7 and Tuesday widened its paths by lines 200 and 202. The kit does the same.
3. **Main risk, written as a STOP: WS-Addressing 2004.** C1:177 says the authorization AGENT is "SOAP 1.2 with WS-Addressing 2004". If the authentication-agent or callback bindings use the 2004 namespace, the stub throws (`used.Count != 1`) and C07 fails (`uses2004 == 0`). The envelope catches this before any write: its control plants 2004 in a committed binding and it FAILS (MEASURED). How to fix it then is NOT DECIDED 1: a stub that reads device-side bindings only (a logic change in OX-A's folder), or another folder.
4. **L1c does not need L0.** Its paths are `contracts/oxpd1/**`, `ContractTests.cs:66`, `StubDevice.cs:200/202` and `contracts/oxpd1/README.md`, and none of them is an L0 path. Its base is main now (`7d652c5f`), and it may run beside X84 and X93 (plan r2 line 83).
5. **OX-A** is SWEEP-0446's lane "the OXPd 1.x client". It owns `src/Datasec.Suite.Adapters.Oxpd1/**`, `tests/Datasec.Suite.Adapters.Oxpd1.Tests/**` and that README (SWEEP-0446:195). Its kit 1 (B2109, X77) landed as PR 54, and no later OX-A kit exists. The kit REFUSES any OXPd2 pane but X84, X93 and those S3 names. It also refuses any open PR or unlanded branch that touches `contracts/oxpd1`, `src/Datasec.Suite.Adapters.Oxpd1` or `tests/Datasec.Suite.Adapters.Oxpd1.Tests`, which covers OX-A, L1x and L6 (plan r2 lines 83 and 87).

## The rule on reading the jar (quoted, as the commission asks)
- `OXPd_2/CLAUDE.md:46`: "**Self-contained:** read and write inside this folder only, plus read-only use of the NAS library copy named above."
- `:38` (the library row): "A read-only backup copy is on the NAS: `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd`. Never write there; never search the whole of it (it is slow): open the path a report cites."
- `:50`-`:51`: "Nothing under `Source_Documents/` is ever committed or copied into `2_Project_Files/`, with ONE exception: the files of HP's OXPd 2 specification that `contracts/oxpd2/inputs.sha256` lists ...". **The jar is NOT under `Source_Documents/`.** It sits in the NAS library, at `.../OXPd/OXPd1-NET-Java/SDK/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/Java/lib/OXPdLib-1.8.4.jar`. That is the path lane CT's kit (project Briefs, B2014 line 7) and measurement B2012 (line 23) cite. Its pin `f2bb325f...c3d341` is in `contracts/oxpd1/README.md:9` at main.

## FACTS re-measured (instrument; clock)
- Origin (`gh api -X GET`, 00:08:04): main `7d652c5f0f8d9854aaf49b43df79e77855eccb46`, tree `760295e3...`, one parent `760e1a64`. Open PRs 0. `heads/b2185` 0 rows. No `b2159/l0` branch at that read.
- BASE's push run (`hosted3.py`, 00:17:06-00:17:15): `HOSTED 7d652c5f...: PASS` at `--total 2433 --rules 679`. The control at `--total 2434` gave `FAIL 4`.
- BASE tarball: 679 files. Its scratch commit's tree `760295e3...` equals main's.
- Stub replica at BASE (`l1c.py --control`): ports 7, one namespace (2005/08), 2004 uses 0, 2004 declared in 14 files, used-namespace uses 14, non-Get operations 51. These agree with the green cells' assertions (C07 0 / ≥4 / ≥8, T01 ≥40, the `ports != 7` pin).
- Oxpd1 test project at BASE: 48 indented `[Fact`, 13 `[Theory`, 85 indented `[InlineData`, 0 `MemberData`. So the predicted executable total is 133 (DERIVED). The hosted log gives no per-project total.
- Readers of the contract folder (`grep -n`): `ContractTests.cs:98,155,196,205,209`, `ClientTests.cs:45`, `WriteTests.cs:43`, `TestServiceTests.cs:30,51`, `CaStoreTests.cs:38,48`, `TopLevelButtonTests.cs:39,61`, `EchoTests.cs:17`. `repo_rules.py` R5 covers `contracts/oxpd2/` only.
- Panes at 00:11:09: `tuesday`, `Datasec/OXPd2-X84` and four unnamed. The wave lock was absent. X84's STATUS last line was `WORKING: Step 4 ...`. X88 had ended READY.
- `words.py --control`: 13 of 13. gitleaks 8.30.1: the control showed `leaks found: 1`; the seven tools under neutral names gave `no leaks found`, rc 0.

## Prototype (over a SYNTHETIC jar; `d2185/proto/final.out`)
I built `synthetic.jar` from BASE's 23 files plus agent, scan, callback and closure files that I wrote myself (not HP's text, so not the jar's real shape). The tool copy differed only in its pin line (`diff` 4 lines). Results: `inventory` gave 11 ROW lines and `ENVELOPE: PASS (11 files, 4 new ports)`, and it ignored a decoy `copy` folder. `fetch` gave 11 of 11 and refused a second run. `apply red` and `apply fix` each applied once and refused a second run with nothing written. `checks` over BASE gave 2 of 9 with every control fired; over the applied, staged tree it gave 9 of 9 with 9 of 9 fired. `redproof list` gave 11 rows. `words.py` over the 28 added lines plus the message: clean. The real tool on that jar printed `REFUSED: the jar is not the pinned jar`. **NOT RUN: any mode over the real jar; `redproof run`; any dotnet job.**

## CHAIN INPUTS (each input exists at BASE or comes from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, Stamp S2/S3/S4/S8 | Tuesday's stamp |
| 1 | `<src>` (7 files), `<jar>`, `<repo>` local values, origin, BASE push run | drafter scratch; NAS (REFUSE checks `test -f`); `<repo>`; GitHub |
| 2 | BASE files, `l1c.py` | Step 1 clone and gate |
| 3 | inventory, restored clone | Step 1 |
| 4 | `<jar>`, inventory, the red tree | Step 1, Step 3 |
| 5 | the green tree, red-proof files undone | Step 4 |
| 6 | staged tree, `l1c.py`, `words.py`, message, inventory | Step 5, Step 1 |
| 7 | commit, `origin/main`, `run_step.py`, `hosted3.py` | Step 7a, fetch, Step 1 |

## D-decisions (mine)
- **D-a:** I wrote one tool, `l1c.py` (inventory, fetch, apply, stub, checks, redproof), instead of lane CT's three. The red-proof log parse is copied from `redproof_ct.py`, whose format was MEASURED on real logs (`rp-1.log`: `Total: 40, Errors: 0, Failed: 2`, `Actual:   3`).
- **D-b:** The selection takes the scan folder WHOLE, its callback pair included, because L6's scan "to the server's receiver" may need `ScanJobEvent` (C1:276). The Test callback pair stays out.
- **D-c:** The README text is frozen in the tool, three exact replacements with counts filled in. A `fix` applies all of them or none.
- **D-d:** The seat does not read HP's files whole. It prints each new binding's service, port names and action count by script.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP):** the seat measures the jar by `l1c.py inventory`. Default **a**. Alternative b: a measurement pass, then a re-draft.
- **Q2 (STOP):** widen the owned paths by `StubDevice.cs:200/202`. Default **IN**. If OUT, the lane cannot be green.
- **Q3:** the scan folder whole. Default yes.
- **Q4:** closure files allowed, up to 8. Default yes.
- **Q5:** the three frozen README replacements. Default yes.
- **Q6:** one gate, G2 on Opus (`model-routing.md:109`); READY Step 0+180, push by +150; pane `Datasec/OXPd2-X94`. Default as stated.
- **Q7:** the names `.tools/b2185-x94`, `b2185/x94-oxpd1-contracts-l1c`, `2026-11-28_B2185_X94_*`. Default as stated.
- **Q8:** adopt the B2172 counting runner. Default **NO**. The single wave lock is shared with X84 and X93, with about 90 minutes of waits budgeted.
- **Q9 (for Tuesday, not in the kit):** X84's S3 lets "any later OXPd build seat Tuesday names in an ANSWER file" run beside it. Should Tuesday name X94 in such an answer? Default: yes, if that is the practice. X84's REFUSE ran only at its Step 0.
- **Q10:** after L1c lands, drop L6's "commit the scan description" step from the plan. Default yes. L6 keeps the client call.

## UNMEASURED
- All of the jar's real contents: names, f, hashes, ports, the addressing namespace of the agent and callback bindings, the import closure, whether any file holds non-ASCII bytes or anything gitleaks or `repo_rules.py` would flag.
- The Oxpd1 executable's real total (133 is DERIVED). The pin-red count k.
- Whether the NAS is mounted when the seat runs. The kit REFUSES if it is not.

## Outside the fences (disclosure)
- **Writes:** the kit, its `.measured` and this report under `tuesday/briefs/`. In scratch `fleet/state/s336/d2185/`: `base.tgz` and `src_7d65/` (BASE by `gh api -X GET`); `seat-tools/`; `proto/`, which holds the synthetic jar and scratch git repositories `sim`, `sim2`, `simbase` (`git init`/`add`/`commit` with a `-c user.*` identity INSIDE my scratch only, never in a project repo); hosted logs; gitleaks folders. The gitleaks control file `gl-control/c.txt` is a synthetic token left in scratch. Nothing was deleted.
- **Reads:** project `CLAUDE.md`; lines of `CLARIFICATIONS.md` by grep; `Analysis/C1` by grep and line prints; the lane CT kit and the X84 STATUS tail and X88 STATUS last line in project Briefs; Tuesday-tree kits, plans and SWEEP-0446 by grep.
- **Not read:** the NAS library, `Source_Documents/`, `4_Credentials/` (beyond `GH_CONFIG_DIR` for `gh`), key folders.
- **Not run:** no az, no dotnet, no lock, no device, no Jira, no card, no mail. One wide grep tried to cover `5_Project_History` and was refused by a hook; it was re-run per file.
