STARTABLE: YES (after lane L4's pull request is merged: the kit's Step 1 STOPS until `main` holds L4's frozen files byte for byte; and only with Q1 and Q10 answered "a" in words at the stamp)

# B1997 DRAFTER REPORT: lane L5, the lab `oxpd1` command (older-printer read with a one-attempt lockout guard, the WS-Addressing switch, the lab host-name certificate), seat Datasec/OXPd2-X56

Drafter B1997 (Opus, in-session, read-only toward the project), 2026-11-23 17:36 to 18:29 AEDT. Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1997_SEAT-X56_oxpd2-l5.md` (98898 bytes, sha256 `e0a88096...`), sidecar `.measured` beside it (`stamp_check.py` 215 of 215 measured, rc 0). Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s317/d1997/` (below `<d>`). Gate tier G1 (an admin credential, TLS pinning, key material), round 1 of 2.

## BLUF
- One command `oxpd1` takes one line in the command table. It has two verbs. `read` fetches the discovery tree with no credentials, then makes exactly ONE request carrying the admin password, and stops on any result. A 401 or 403 exits 6 with a lockout message. The password comes from a credentials file only, and no option carries it. Without `--pin` it makes a first contact through the Lab's own `DeviceChannel`. `lab-cert` makes a development CA and a server certificate for a host name and keeps no CA key. Both refuse a run folder that is inside a git work tree. `--addressing 2004` uses a new public client option, `Oxpd1ClientOptions.Addressing`.
- **Re-based on your 18:05 order (L4 first, L5 second).** The patches are cut on `d804de5e` plus L4's FROZEN patches (`777b1674` / `83fe0d61`, the same hashes as in kit B1992's THE TOOLS), tree `d60819db`. I measured all of it on that tree in a fresh `<d>/clone6`:
  - RED: Lab 95/15, client 27/1, whole solution 2004/16 (the 16 lane cases only), each red by an assertion.
  - GREEN: 2004/0/2000/4.
  - Mutants: `MUTANTS: 15 of 15 MATCH, 15 of 15 undone equal`.
  - Chain: 34 of 34 lock files equal after `--force`, `GUARD: clean (14/15 files)`, `Ran 111 tests`, `RULES: clean (642 files)`.
  - Checks and scans: `checks_l5.py` 7 of 7, `WORDS: clean`, gitleaks rc 0 (its control fired).
- **Not one shared line but 19 owned paths, two of them landed L4 lines.** Besides the table line, the `.csproj` line, the lock files and the README entry, two lines change. One is P13 (`ProbeTests.cs:207`), which becomes `["probe","print","oxpd1"]`. The other is **L4's own cell R11 (`Print/PrintTests.cs:188`)**: it pins `["probe","print"]` exactly and reddens on ANY added command (measured). That second line is outside "those shared lines", so I made it Q10, STOP-class.
- The numbers on BASE are PREDICTED from the L4 tree: total 1968 + 36 = 2004, rules 634 + 8 = 642. Re-measure at the stamp: BASE's sha and its hosted numbers (S2), and that BASE's seven L4-touched files and four client files hash equal to THE CODE's "At BASE" column (the seat's Step 1 does this and STOPS otherwise).

## Facts re-measured (instrument)
- Origin `main` = `d804de5e303d62a78a8bcd677ec2cd66940b91f4` (`clone.py` at 17:36). `matching-refs/heads/b1997` returned 0 (`gh api -X GET`).
- `hosted3.py` on `d804de5e`: PASS at `--total 1942 --rules 628 --skipped-linux 4 --skipped-windows 21 --guard-linux 14 --guard-windows 15`. The hosted2 form, which expects guard counts of 10 and 11, printed FAIL 2 on that same green main, so the kit ships `hosted3.py`.
- The Lab project reads no secret at BASE (`git grep` rc 1; the control `readSetting` counted 7). "As the Lab already reads secrets" therefore had nothing to reuse (D4, Q4).
- `CLARIFICATIONS.md` has 720 lines (sha `5d556264`). Counts: lockout, addressing, host name, DNS, admin password, credentials file and run folder all 0; certificate 2 (C-9, the customer-authority certificate for the SHIPPED server). Controls: OQ-6 3, C-63 1.
- `kam_rulings_today.sh` (10 rows) has nothing on these subjects (printer 3). His 17:56 note on the OPEN card `datasec-oxpd-older-printer-hp-library-1123` reads "our license / commercial agreement allows us to use HP code as part of our code." The card is unruled. Every option on it keeps lab reads on today's client, so it is in NOT DECIDED.

## D-decisions (all yours as coordinator)
D1 one command, two verbs, one table line after L4's · D2 no fifth pin copy (first contact uses the Lab channel; the pinned read uses the client's own check) · D3 one password-bearing request per run, structural · D4 credentials file, name `OXPD_TEST_PRINTER_ADMIN_PASSWORD` · D5 the addressing switch as a client option (the 2004 anonymous address `.../role/anonymous` comes from the 2004 submission's text, not from an HP file) · D6 RSA 2048, no CA key kept · D7 refuse a run folder inside a git work tree instead of adding a `.gitignore` line · D8 key-file mode asserted off Windows only · D9 one commit.

## Q-questions for Tuesday (each with its default)
- **Q1 (STOP-CLASS):** landing order. Default a: L4 first, and BASE is main after L4 (built). Note: L4's `DeviceChannel.cs` comment "The probe's ONE way" becomes untrue once this lands.
- **Q10 (STOP-CLASS):** L4's R11 line 188. Default a: this lane changes that one line (built). Alternative b: L4 relaxes R11 before it lands, and I re-cut.
- Q2 pin check: default is the client's own check, with no seam. Q3 attempt count: default is per run. Q4 password source: default is the credentials file, not the environment. Q5 certificate: default is RSA 2048, 30 days, no CA key. Q6 records out of git: default is the refusal, no ignore line. Q7: default is one command. Q8 the landed flaky C7 (`GatewayStubTests.C7_healthcheck_answers_healthy`, failed once at load 6.72 on the superseded run): default is a STOP like any red. Q9: default is Opus, 120/90 minutes, X56, hard stop 23:30.

## Chain table (every step's inputs exist earlier)
Step 0: the kit and the stamp → Step 1: `<src>` (10 files), the origin, main-after-L4 → Step 2: the clone → Step 3: `1-red.diff` → Step 4: `2-fix.diff` and `mutants_l5.py` → Step 5: the green tree → Step 6: the staged tree and `checks_l5.py` / `words.py` → Step 7: the commit, `run_step.py`, `hosted3.py`.

## UNMEASURED
Anything on a device: certificates, addressing, endpoint path, answer, name resolution, acceptance of the certificate. Windows and Linux runs of L01's X.509 and file-mode asserts. Any `main` that holds L4's real landed commit. `run_step.py`'s neutral scan on a commit of this lane. Whether the HTTP layer can resend on a reused connection (H4, DERIVED no).

## Outside the fences (disclosure)
- I read L4's kit and its draft and frozen patches in `d1992/seat-tools/` (READ only). I wrote nothing of theirs.
- In my own scratch clones only: `git apply`, `git add`, `git write-tree` and local clones (`clone4`/`5`/`6`). No commit, and the push URL is `invalid://no-push`.
- I read one card with `decision_queue.sh show <exact id>` into scratch.
- I stopped my own superseded mutant run on `clone3` (no lock left held, verified). That clone may hold one mutant applied, and it is never used again. I quarantined the old gate and `hosted2.py` under `<d>/_quarantine/`.
- In my sidecar I corrected one shell slip of mine (a piped grep that printed 0) by re-running on a saved file.
- I connected to no printer and no host other than GitHub. I printed no secret. I deleted nothing.
