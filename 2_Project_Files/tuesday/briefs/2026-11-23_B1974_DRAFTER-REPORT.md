STARTABLE: YES

# B1974 drafter report: lane H (host composition v0), seat Datasec/OXPd2-X48

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1974_SEAT-X48_oxpd2-h.md` (+ `.measured`). Tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1974/seat-tools/` (11 files). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1974/`. Drafted 10:31 to the sidecar's first-line clock, read-only toward the project, Jira and GitHub.

## BLUF
- H is buildable now and a seat can finish it in about 2 hours: 14 paths (3 M, 11 A) under `src/Datasec.Suite.Server/` and `tests/Datasec.Suite.Server.Tests/` only. The host gets `GET /health`, the five OXPd 2 callback routes bound to `Oxpd2CallbackHandler`, a notification route for `ntAuthCode` (credential first, bytes to a sink, never parsed), HTTPS only on both OXPd 2 routes, `IDeviceSecretVault` bound to `ISecretStore` (fresh copy per read, value disposed), and the TLS certificate from the framework's `Kestrel` configuration.
- **The slnx answer (the commission's line 20):** the new test project is NOT in slnx this round. Its 13 cells run by the project path (build of the test csproj, then its executable whole) on the seat's macOS only. The hosted legs still build, test, publish and guard the changed Server project, because Server is in slnx at BASE. They run none of the 13 cells until a later one-line slnx round after L1 (Q2). It is not a STOP.
- Red first, measured: at BASE + `1-red.diff` (the test project and shells) the Server test executable reads `Total: 13, Errors: 0, Failed: 12`, all by assertion. H12 (the project-reference pin) is green by design; its red is its own in-cell planted control. Green after `2-fix.diff`: `Failed: 0`. The whole solution stays `total: 1809`, `failed: 0`.
- Mutants: 12 rows, each red on exactly its cells (`MUTANTS: 12 of 12 MATCH, 12 of 12 undone equal`). One more mutant, `mFirstOfTwoHeaders`, survives: the .NET client sends two Authorization values as one header field, so the host's `Count == 1` rule is reached by no cell. It is named in the kit as a survivor and is not a row.
- Hosted predictions change in two places. Rules go 553 to 564. The release guard goes from 10/11 to 14/15 files, because the Adapters.Oxpd2 and Secrets dll/pdb pairs now ship (measured; no OXPd2Lib, no Lab, no test assembly). `hosted2.py` hardcodes 10/11, so the kit ships `hosted3.py`: two options, defaults unchanged. Its control was measured: PASS at BASE, and FAIL 2 at BASE with `--guard-linux 14 --guard-windows 15`.
- Generation, stated in the kit's purpose line: these are OXPd 2 routes. The M577 (FutureSmart 5, OXPd 1.x) will never call them. Their first real caller is the OXPd 2 simulator or a FutureSmart 6 printer. Nothing in the lane connects to any device.

- `stamp_check.py` on the kit exits 0: 133 claims, 133 measured. 8 slot lines are left as `____` for Tuesday. The shipped `mutants_h.py` ran in clone2 from 11:22:03 to 11:35:03 and printed `MUTANTS: 12 of 12 MATCH, 12 of 12 undone equal`.
- Trees left (drafter scratch only): `d1974/clone` (prototype, 14 paths, partly staged) and `d1974/clone2` (both patches applied, 14 paths staged). Both clones have push URL `invalid://no-push`.

## Facts re-measured (instrument; control)
- main `da8d64a83bf9f58e4b02fa2c11526dd6a7c7261b` (`gh api -X GET .../git/ref/heads/main`, 11:22); open PRs 0; `matching-refs/heads/b197` 0 rows (control `b196` 1); `.private` and `.permissions.push` true.
- BASE hosted run 45068273700 by `hosted3.py` (defaults): PASS at 1809 / 553 / skipped 4 and 21 / unit 111 / guard 10 and 11.
- clone2 chain: locked restores rc 0 (both lock files sha256-unchanged); builds 0/0; whole solution 1809/0/1805/4; publishes rc 0; guard 14 and 15; unittest 111 OK; `RULES: clean (564 files)`; `checks_h.py` 6 of 6, controls 4 of 4; gitleaks rc 0 (control rc 1); words clean over 979 added lines (the test lock file is left out by name: its `linux-x64`/`win-x64` lines count 2 under the seat-id class); neutral scan 25 of 25, `objects of this commit not among them 0`.
- Toolchain `10.0.404`, gitleaks `8.30.1`. The heavy lock was shared with three drafters; load reached 18.95. No test ran beside another lane's lock outside `heavy.py`.
- `kam_rulings_today.sh` at 10:56:57: 5 rows, none about routes, host or statuses. In CLARIFICATIONS (721 lines), 0 hits for health, ntauthcode, callback route, status code, notification target, host composition, kestrel and tls certificate. Controls: OQ-6 3, tolerant 5. C-71 (line 718) holds the 10:10 word.

## D-decisions (all Tuesday's as coordinator; none the product owner's)
- D1 route shape (Q1, STOP-class): the serial is a path segment, `/oxpd2/devices/{serial}/{target}/{operation}` and `/oxpd2/devices/{serial}/notifications`. The per-device credential is the only proof.
- D2: HTTPS only (403 first); `/health` on both schemes; no forwarded headers.
- D3: the status table (14 outcomes; spec lists 200 only).
- D4: TLS from the `Kestrel` section; no lane code reads a certificate.
- D5: notification bytes go to a sink, never parsed. There is no committed spec of the body; `ntAuthCode` is only in the solution manager enum.
- D6: the store is resolved per call: no `Secrets` config gives 503, not a failed start.
- D7: no logging library this round. The lane writes no log line, and H11 shows no credential or marker reaches any log at Trace.

## Q-questions for Tuesday (each with a default)
- **Q1 (STOP-class): route shape.** Default: (a) a serial path segment plus the D3 table. Alternatives: (b) a header macro; (c) credential lookup without a serial, which changes the adapter's public `Verify`.
- **Q2: slnx.** Default: no line this round. A one-line round after L1 adds it, and the hosted totals then rise by 13. Default is to LAND H's PR before that round; alternative: hold until it.
- **Q3: HTTPS.** Default: 403. Alternative: honour `X-Forwarded-Proto` (a proxy-trust decision).
- **Q4: notification credential.** Default: required (fail closed). Alternative: none, which lets anyone post a fake `ntAuthCode`.
- **Q5: logging library.** Default: none. Alternative: Datasec.Suite.Logging, which moves the lock file, the guard counts and the totals.
- **Q6: not-wired sinks.** Default: the callback sink throws (500) and the notification sink drops. Alternative: 503, which would need a new adapter outcome.
- **Q7: level and windows.** Opus; READY at Step 0 + 120 minutes; push by + 95; pane X48; G1 round 1 of 2; hard stop 15:30.

## UNMEASURED
- Every one of the 13 cells on Linux and Windows. In particular the framework's PEM certificate+key load on Windows, and H08's store behaviour under DPAPI-NG.
- On a device: whether it appends exactly the operation path to the target base, what it sends in `Authorization` to callback and notification targets, and what it does with each status.
- Whether the hosted CodeQL csharp build sees the new test project (it is not in slnx).

## Chain inputs
Step 0: the stamp. Step 1: `<src>`, `<repo>` local values, origin, BASE run. Step 2: BASE files. Step 3: `1-red.diff` (it carries both lock files). Step 4: `2-fix.diff`, `mutants_h.py`, the red tree built. Step 5: the green tree with mutants undone and rebuilt. Step 6: the staged tree, `checks_h.py`, `words.py`, the message. Step 7: the commit, `origin/main`, `run_step.py`, `hosted3.py`. Every input exists at BASE or comes from an earlier step.

## Outside-the-fences disclosure
- One Bash call held a `cd /dev/null` prefix and the `pretooluse_no_cd.sh` hook refused it. I stopped that action and read the same files with the Read tool, one call per file, with no cd. Nothing else was refused.
- I wrote only my kit, its sidecar, this report, and files under my own scratch `s315/d1974/`. The prototype files lived in my own draft clones (push URL `invalid://no-push`). In those clones I staged files (`git add`) and moved two prototype files to `d1974/_quarantine/red-moved/` while cutting the red patch. My first kit draft, filed under a seat name not in the precedent form, was moved to `d1974/scratch/kit-draft1.md`.
- Every heavy job went through `heavy.py` and the wave lock; no lock of another holder was touched. I made `gh api -X GET` reads only. No Jira call, no device, no write to the project, no message to anyone.
- The other drafters' kits B1972 and B1973 were read only to check path overlap. Neither touches `src/Datasec.Suite.Server/**`, and B1973 lists it as lane H's.
