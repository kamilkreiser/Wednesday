STARTABLE: YES

# B1973 DRAFTER REPORT: lane TA (OXPd 2 device sign-in), seat Datasec/OXPd2-X47

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1973_SEAT-OXPd2-X47_oxpd2-ta.md` (+ `.measured`). Tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1973/seat-tools/` (9 files). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1973/`. Drafted 10:31 to 11:30 AEDT 2026-11-23 by a read-only drafter (Opus) on the commission `2026-11-23_B1971-B1974_OXPD-KICKOFF-WAVE1-KITS_DRAFTER_COMMISSION.md`.

## BLUF
- The lane is built and proved on the drafter's prototype (macOS arm64): `DeviceTokenClient` (password grant, install-code exchange inside a 5-minute window on the client's `TimeProvider`, refresh), `DeviceSolutionTokenEndpoint` (the landed holder's `ISolutionTokenEndpoint`), TLS trust by leaf SHA-256 pin only, no proxy, no redirect, strict answer reading; README Part 3 plus Limits; the owed `TryGet` doc line (BACKLOG item 45(10)) and item 65's `finally` limit.
- The sweep's "check first" is answered: the only adapter network rule (cell L03) forbids a `System.Net.Sockets` reference, not HTTP; L03 and N03 stay green, so TA stays in the adapter (Q1 STOP-CLASS, default a). No csproj, lock file, package or `slnx` line.
- Red first by skeleton (B1934's precedent): at BASE + `1-red.diff` the whole solution reads `total: 1837`, `failed: 27`, all 27 `DeviceAuthCellTests.DA` cases (DA16, a census, green against the skeleton). Green after `2-fix.diff`: `total: 1837`, `failed: 0`, `succeeded: 1833`, `skipped: 4`.
- 17 mutants, every row MEASURED MATCH but NOT in one run: run 1 (`<d>/clone2`) 16 of 17 (`mSpaceAllowed` REFUSED: its OLD text named the escape form of 0x21 while the file holds the character); run 2 (`<d>/clone3`, the shipped program) 16 of 17 (`mSpaceAllowed` red on DA02 and DA13, expected DA13 only: DA02's second answer holds a space, so the row's expected cells were corrected to `DA02 DA13`); the corrected row alone MATCH in `<d>/clone4` on the final bytes. So the seat's one-run `MUTANTS: 17 of 17 MATCH` is PREDICTED (the kit says so). After run 2 one comment word of the test file changed (`gate task` to `hold task`, a `words.py` hit) and the patches were regenerated; it compiles to nothing.
- Generation: OXPd 2 only; it will first meet the simulator or a FutureSmart 6 printer, never the product owner's M577 (OXPd 1.x / FutureSmart 5 by B1968). Nothing connects to any device.

## FACTS RE-MEASURED (instrument, control)
- Origin `main` `da8d64a83bf9f58e4b02fa2c11526dd6a7c7261b` (three `clone.py ... draft` runs 10:32 to 11:01, unmoved); 0 `b1973` branches (control: `b1961/...` listed).
- BASE hosted run 45068273700: `hosted2.py ... --total 1809 --rules 553 ...` last line `HOSTED da8d64a8...: PASS` (10:52).
- Toolchain: dotnet `10.0.404`, gitleaks `8.30.1` (10:51). Disk 958 GiB free.
- `CLARIFICATIONS.md` (720 lines, C-1 to C-71): `oauth`, `token endpoint`, `password grant`, `install code`, `install-code`, `ntAuthCode`, `admin password` 0 each; controls `tolerant` 5, `OQ-6` 3. `kam_rulings_today.sh` (10:51): 5 rows, the only OXPd ones OQ-6 (06:59) and the 10:10 kick-off message; nothing on device sign-in.
- C-24's reading for OXPd 2 (`02_architecture.md:251`, `:615`): the admin password is held for the install and discarded; a stored copy is OQ-2, open. The lane stores nothing (DA16).
- The tools: the five reused programs are byte-equal to kit B1961's table (sha256 printed side by side).
- Prototype numbers (clone3): red `total: 1837`, `failed: 27`, `succeeded: 1806`; adapter exe red `Total: 86, Errors: 0, Failed: 27`; green `total: 1837`, `failed: 0`, `succeeded: 1833`; exe green `Total: 86 ... Failed: 0`; cells 16 methods, 13 rows, column 1 0. Chain (clone4): restore --force rc 0, 28 of 28 lock files equal; publishes rc 0; `GUARD: clean (10 files)` / `(11 files)`; `Ran 111 tests` OK; `RULES: clean (562 files)` on the staged tree (553 before staging); checks clean (11 rows: 9 A, 2 M; SHARED rc 0 over 51 paths, control rc 1; ASCII 0; `WORDS: clean (2 files)`; gitleaks control rc 1 then rc 0 on the clone and on 15 neutral files; neutral scan 25 of 25, `objects of this commit not among them 0`). `stamp_check.py <kit>` exits 0 (150 claims, 150 measured). Kit predictions for hosted: `--total 1837 --rules 562`, linux `succeeded: 1833`, windows `succeeded: 1816` (PREDICTED; nothing run off macOS).

## D-DECISIONS (Tuesday's as coordinator; each a Question)
D1 adapter placement (Q1); D2 pin-only TLS trust, pin private to the client (Q5); D3 the three grants' forms, bytes not strings, no retry; D4 strict answer reading, 400/401 refusal (Q3); D5 the endpoint reads the refresh bytes before returning its task (closes item 65's limit for this binding); D6 red by skeleton (Q7); D7 one commit.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- Q1 STOP-CLASS: where TA lives. Default a, the adapter's `DeviceAuth/`. S4 must answer in words.
- Q2: the wire field names (form and answer) are OAuth 2.0's (RFC 6749), DERIVED; the committed reports name only `grant_type`, `client_id`, `refresh_token_requested` and the path. Alternative: Tuesday reads the guide lines the reports cite (`G/securityModel` 149 to 292) before the stamp; a drafter may not open `Source_Documents/`. **This is the lane's largest residual risk: if HP's device uses other names, every grant fails at first contact (safely: `AnswerInvalid` or `Refused`), and a new round follows.**
- Q3: 400 and 401 = refusal; Q4: `client_id` sent on the refresh; Q5: the pin coded three times in the wave, folded later; Q6: Opus, READY Step 0 + 110, push Step 0 + 80, pane X47, G1 round 1 of 2, hard stop 15:30; Q7: red by skeleton.

## THE CHAIN-INPUTS TABLE
Printed in the kit (section CHAIN INPUTS): every step's inputs exist at BASE or come from an earlier step.

## UNMEASURED
- Every cell on Linux and Windows (the TLS stub: certificate loading by `X509CertificateLoader.LoadPkcs12`, SChannel and OpenSSL server handshakes). A one-leg red is a STOP to Tuesday by the kit.
- What any HP device answers to any grant; which token path it serves; whether its refresh needs `client_id`; HTTP/2.
- Whether .NET would route a loopback request through `heavy.py`'s closed proxy (so the green under it is not proof of `UseProxy = false`; that is by construction, H5).

## SIZE
One seat: two `git apply`, about 8 heavy jobs plus 34 for the mutants (the drafter's mutant run took about 25 minutes with the wave's load and lock waits), the chain, the checks, one push and one hosted run: inside about 2 hours if the lock is shared by at most four seats. The kit allows about 60 minutes of waits.

## OUTSIDE-THE-FENCES DISCLOSURE
- Read only, outside my two files and my scratch: the commission, the sweep B1969, the needs list B1968 (section 2a and the header), DRAFTER_RULES, the form kits B1961 (whole) and B1953 (pages), the wave-4 commission, the project's `CLAUDE.md` (lines), `CLARIFICATIONS.md` (by program and three entries), `BACKLOG.md` items 45 and 65, the reports B1 and B2 (lines), `02_architecture.md` (lines), `kam_rulings_today.sh` output, `models_latest.json`, `model-routing.md`, `brief_seat.sh` (lines). Nothing under `Source_Documents/`, no key folder, no sibling project, no card store, no ledger.
- Git: three scratch clones by `clone.py ... draft` (push URL `invalid://no-push`, no identity); in them `git add`, `git apply`, `git diff` only; no commit, no push, no ref write. `gh api -X GET` only (through `hosted2.py`).
- Heavy jobs: every dotnet job and test executable through `heavy.py` and the shared wave lock (`.tools/wave1-heavy.lock.d`), one at a time; I waited on other drafters' locks (B1976 among them) and broke none. The tests listened on 127.0.0.1 only; no other connection.
- Files written: the kit, its sidecar, this report, and my scratch folder. The `seat-tools/` folder is mine (the kit's `<src>`).
