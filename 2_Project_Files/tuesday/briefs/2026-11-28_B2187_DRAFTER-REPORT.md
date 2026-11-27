STARTABLE: YES, once lane L0 has LANDED on `main` (seat X84 is READY at `f08eabf4765dbb37c01fcad6532d70442b5e7c54`, no pull request open at 00:29:54 AEDT). Until then the kit's own REFUSE stops the seat at Step 0 (Stamp S2 must name a `main` holding the two Entra folders).

# B2187 DRAFTER REPORT: seat X96, lane L2 (Entra sign-in), for Tuesday s336

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-28_B2187_SEAT-X96_oxpd2-l2-entra-sign-in.md` (sidecar `.measured` beside it: `stamp_check.py` printed `215 claims, 215 measured, 0 not measured`, rc 0, at 00:32:26 AEDT). Seat tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/d2187/seat-tools/` (8 files). Scratch: `fleet/state/s336/d2187/`. Clocks by `date`: first `Sat 28 Nov 2026 00:07:44 AEDT`; sidecar written 00:32:26 AEDT.

## BLUF
1. **The kit is a product lane of the X86 form**: the seat writes 16 source files and 2 test files to a full specification (C1 to C18, cells E01 to E19, 13 Facts and 6 Theories with 38 rows = 51 cases), NuGet writes the two lock files, eleven mutants with frozen red cells. Base: `main` after L0 lands; the Entra executable goes from `Total: 1` to `Total: 52` (PREDICTED); whole solution `<BASE total + 51>` (2496 if L0 lands at its own prediction of 2445); RULES `<BASE files + 18>` (757).
2. **What it builds**: `EntraSignIn` (auth code + PKCE S256, state and nonce, `prompt=login`, state single use and timed, both tokens required, id-token aud/tid/iss/nonce/oid checked), `EntraTokenRefresher : ITokenRefresher` (the broker's missing refresher), `AppTokenSource : IGraphTokenSource` (the card store's app token), `SessionGraphTokens : IGraphTokenSource` (a session's token from the broker, refreshed after a 401), `SecretClientCredential` (read from `ISecretStore` per call) and `CertificateClientCredential` (RS256 assertion, `x5t#S256`, 600 s). Hand-written over the caller's `HttpClient`, the landed `DeviceTokenClient`'s form; no package.
3. **Two STOP-CLASS questions** (Q1 device code, Q2 where the object id comes from); both defaults "a" are built.
4. **The simulated BASE is exact**: `main 7d652c5f` + L0's frozen 61 files gave tree `fc101f81...`, EQUAL to the tree of L0's pushed head `f08eabf4` (gh api, 00:29:54). Lane L0's six Entra files on that head match FACTS 3's sha256.

## Facts re-measured (instrument; outputs in `<d>/gen/`)
- Origin (`gh api -X GET`, 00:08:07 and 00:29:34): `main` `7d652c5f0f8d9854aaf49b43df79e77855eccb46`, tree `760295e3...`, parent `760e1a64`; open PRs 0; `matching-refs/heads/b2187` 0 rows; `contents/src/Datasec.Suite.Identity.Entra?ref=7d652c5f` -> HTTP 404 (L0 not landed), control `src/Datasec.Suite.Identity` -> 12 (`origin.out`).
- L0 (`l0-branch.out`, `l0-six.out`): `refs/heads/b2159/l0-scaffold` = `f08eabf4...`, compare main...head ahead 1 behind 0, 61 files; head tree `fc101f812f5eab212074fc18e39c9d0a5c6ee1cb`; the two Entra folders 3 entries each, six sha256 equal to L0's `scaffold_l0.json`. X84 STATUS last line `READY B2159-L0: f08eabf4...` (`machine.out`, 00:29:42).
- Simulated BASE: `<d>/sim` (tarball of `7d652c5f`, `HEAD^{tree}` `760295e3...`), then L0's `apply_l0.py` -> `APPLIED scaffold: 61 files, 61 of 61 equal to the frozen sha256`, commit `fc669848...`, 739 files; a clean clone `<d>/simbase` for the BASE-index control.
- `checks_l2.py`: over `<d>/simbase` index `CHECKS: 2 of 10 PASS`, 10 of 10 controls FIRED, rc 1 (`checks-base.out`); over the staged prototype `CHECKS: 10 of 10 PASS`, rc 0 (`checks-sim.out`). The prototype is anchors plus stubs: NO compiler has read it.
- `mutants_c3.py --list`: prototype rows -> `LIST: 11 mutants, 1 suites, 19 cells` rc 0; a row under `src/Datasec.Suite.Graph` -> `LIST REFUSED: rows mBad` rc 1; `apply` then `undo` of all eleven -> `equal True` 11 of 11 (`apply-undo.out`), working tree unchanged after.
- `words.py`: `--control` -> `CONTROL FIRED: 13 of 13`; commit message -> `WORDS: clean (1 files)`; prototype `added-words.txt` clean, `added.txt` `WORDS: 2 hits` (the two `S256`); a probe of `S256`, `x5t#S256`, `RS256`, `x64` -> `seat ids 4` (`RS256` not counted).
- `gitleaks dir` 8.30.1: control (a `ghp_` token of random characters) rc 1, twice; the seat tools rc 0; the synthetic values of THE NEW CELLS in C# form rc 0 (`<d>/gl/probe2/`). Control folders moved to `<d>/_quarantine/`.
- RFC 7636 Appendix B by `hashlib`: `dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk` -> `E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM` (`pkce.out`).
- Toolchain: `<project>/.tools/dotnet/dotnet --version` 10.0.404; gitleaks 8.30.1. Load 8.45 at 00:29:42; 833 GiB free; heavy lock folder ABSENT; panes `Datasec/OXPd2-X93`, `Datasec/OXPd2-X94` live (X84's pane gone).
- Six common tools `cmp`-equal to `fleet/state/s334/d2159-L5/seat-tools/` (clone, heavy 31adedc8, hosted3, mutants_c3, run_step, words).
- Pointers by `grep -n` over `7d652c5f` (FACTS 4 of the kit); A1 lines 136, 151, 155, 156, 158, 173, 174, 175, 363; 02 lines 368, 376, 423, 424, 620, 695, 1225, 1227; plan r2 lines 70, 71, 83, 84, 87; B2154 lines 87, 93, 172; CLAUDE.md 7, 25, 55-56, 82, 83; model-routing 108 (G1).

## Chain inputs (DRAFTER_RULES MEASURED LITERALS 4)
| Step | Inputs | Produced by or present at |
|---|---|---|
| 0 | kit, Stamp S2 (main after L0), S3, S4, S8 | Tuesday's stamp |
| 1 | `<src>` 8 files; `<repo>` local values; origin with L0's six files; BASE push run | drafter scratch; `<repo>`; GitHub after L0 lands |
| 2 | BASE files; A1, 02 | Step 1 clone; project folders |
| 3 | THE CODE, THE NEW CELLS; `CSPROJ` in `checks_l2.py` | kit; Step 1 tools |
| 4 | pinned tree; C18; `mutants_c3.py`; rows file written in Step 4 before its run | Steps 3, 1, 4 |
| 5 | green tree, mutants undone | Step 4 |
| 6 | staged tree; `checks_l2.py`, `words.py`, message | Steps 5, 1 |
| 7 | commit; origin/main; `run_step.py`, `hosted3.py` | Step 7a; fetch; Step 1 |

## D-decisions (Tuesday's defaults in the kit)
D1 hand-written over the caller's HttpClient (B2154 Q6 "over the existing Graph HTTP layer" cannot hold as worded: `GraphClient` binds every call to its base origin and always adds the Bearer; the token address is another host with no Bearer). D2 no device code. D3 object id from the id token, signature not checked. D4 pending state in memory, single use, 10 min, max 64. D5 refresh keeps held renewal state / subject when absent. D6 app token kept to 5 min before expiry. D7 session token from the broker, null on any broker refusal after a 401. D8 both credentials. D9 base scopes + `prompt=login`, A1 presets, no DoD preset. D10 new cells only.

## Questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS) device code**: default **a** NOT built. Source conflict for you: plan B2154 line 87 lists "device code (fallback)" and plan r2 line 71 plans the live token check "device code; no FQDN needed", but 02 line 1225 says "Default: device code is not built before test 1 reports" (N-3 open). With a, the live check uses the app token or waits for AZ-7's redirect address. Alternative b: build it (+0.5 lock-day, needs public client flows).
- **Q2 (STOP-CLASS) object id source**: default **a** the id token's claims (aud/tid/iss/nonce/oid), signature not checked. b access-token claims (Workpath's way, A1 line 136); c a Graph `me` call.
- Q3 credentials: default both (secret per call + certificate assertion). Alt: secret only now.
- Q4 refresh answer without refresh token / id token: default keep held. Alt: fail closed.
- Q5 scopes `openid profile offline_access` + extras, `prompt=login`, no `hsu`. Alt: drop `prompt=login`.
- Q6 authority presets per A1 line 363, DoD none. Alt: a DoD preset from another source.
- Q7 one G1 gate, Opus, READY Step 0 + 360 min, push + 330, pane `Datasec/OXPd2-X96`, ~90 min of lock waits. Alt: G2.
- Q8 canonical heavy.py, NOT the B2172 counting runner (default NO per the commission). Alt: adopt it.
- Q9 base `main` after L0 lands, launched beside the panes S3 names (L1x per plan r2 line 84). Alt: hold until L1x lands.
- Q10 `SessionGraphTokens.GetNewTokenAsync` null on ANY `TokenBrokerException`. Alt: null only for refresh reasons.

## UNMEASURED (named in the kit's R17 and Limits)
How Entra answers: the `iss` form `{authority}{tenant}/v2.0`, whether `x5t#S256` and a 600 s assertion are accepted, whether a refresh answer carries an id token or a new refresh token, `expires_in` as a JSON number, the error words. Whether each hosted leg makes the in-memory RSA certificate the same way. Every total, count and mutant red is PREDICTED (no build, no test). The lock files' exact bytes (NuGet's; the drafter's predicted ones in the prototype were made by program only to exercise check 4).

## Notes for the stamp
- The S2 slot must name a `main` AFTER L0's squash; the kit's Step 1 then checks the six sha256s. If L0 is rebased before landing, the tree may differ from `fc101f81...`; only the six Entra files and the absence of other files under the two folders matter to this kit.
- `words.py` counts `S256` as a seat id (MEASURED): `checks_l2.py` writes `added-words.txt` with standalone `S256` replaced (count printed) and keeps lock lines out (`x64`), as kit X84 did. A gate that runs `words.py` over raw added lines will see exactly the `S256` hits.
- Card ids (report only): the tenant-pieces ruling is card `datasec-oxpd-tenant-pieces-k2-1127` (daily note 2026-11-27 line 94); the kit cites it as "the product owner's 2026-11-27 ruling".

## Outside-the-fences disclosure
- One Bash call sent stderr to `/dev/null` on a `grep -P` attempt (macOS grep took no `-P`, so it printed nothing, the control included); the result was discarded and the count redone by `python3` (an underscore-aware scan, control fired).
- One command was REFUSED by the no-cd hook (`git -C $D/sim init` with a variable path it could not resolve); nothing ran; redone with literal paths inside the TUESDAY tree.
- The harness saved one long tool output (lines 140-249 of the X86 kit) under `/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude/projects/.../tool-results/` and I read that file with the Read tool; it held only that kit's text, no credential. A second saved output (a grep of the Tuesday daily note) was not opened.
- Git write verbs (init, add, commit, clone) ran ONLY in my scratch `fleet/state/s336/d2187/` (sim, simbase). In the OXPd project: read verbs only (`ls`, `cat`, `tail` of X84's STATUS, `shasum`, `grep`, `sed`, `awk` of CLAUDE.md, CLARIFICATIONS.md lines 784-800 and 1188-1236 plus a grep, A1 and 02 by line); `gh api -X GET` under the project GH_CONFIG_DIR only. No `Source_Documents/`, no key folder, no NAS, no `<project>/4_Credentials/` beyond GH_CONFIG_DIR, no az, no dotnet, no lock taken, no device, no mail, no Jira, no card store call.
- Read beyond the commission's list: `0_Brain/daily_tuesday/2026-11-27.md` (named by the commission) by grep and by `awk` of lines 94, 97, 99; the X84 and X86 kits (the forms), plans B2154 and B2174 by grep and part reads.
