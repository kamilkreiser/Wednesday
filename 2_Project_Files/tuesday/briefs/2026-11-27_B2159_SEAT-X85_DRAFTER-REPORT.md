STARTABLE: YES

# B2159 lane L9 DRAFTER REPORT: OXPd network-path device run on the M577 (first-run row 3 + async echo callback), seat X85

Drafted 2026-11-27 by an in-session read-only drafter (Opus) for Tuesday s334, commission `2026-11-27_B2159_OXPD-LANEP-FIRST-KITS_COMMISSION.md`, section "Lane L9 (seat X85)". First `date`: `Fri 27 Nov 2026 17:39:07 AEDT`; the sidecar's first line carries the write clock. Kit: `tuesday/briefs/2026-11-27_B2159_SEAT-X85_oxpd2-l9-network-path.md` (202 lines), sidecar `.measured` (`stamp_check.py` exit 0: "94 claims, 94 measured, 0 not measured"). Scratch: `fleet/state/s334/d2159-L9/` (the seat's tools are in `seat-tools/`). The report is named with the seat because four drafters share B2159 (a bare `2026-11-27_B2159_DRAFTER-REPORT.md` would collide).

**STARTABLE means:** the kit is complete and stamp-checked. Its launch waits only on the stamp. It needs no lock-free window to START: its two heavy jobs (restore and build of the Lab project) queue on the wave lock through `heavy.py`, which holds the lock only for each job. B2157 held the lock at 17:40, and B2153's X82 is next by the commission.

## BLUF
- **What it runs (in this order).** R01 reads the pins. R02 reads the Test service state. L01 runs `lab-cert`: a fresh one-day CA with its private key never written. W31 is the import dry run. W32 runs `ImportCaCertificate --execute`, which reads the store before and after. W33 runs the printed undo `RemoveCaCertificate`. Then W22 turns the Test service on, only if it is off. E01 is one sync echo as guest. E02 is one async echo with its listener on `192.168.20.220:18627`. W23 runs the printed undo to disable the service. R04 reads the service state back. U01 runs `undo-owed`. Every write is undone in the same run.
- **Findings are not STOPs.** A REFUSED or UNCLEAR import, a refused guest echo and a callback that does NOT arrive are what the lane exists to measure. The seat records each one, runs the undos and ends READY with the outcome in the READY line. A callback that does not arrive also adds `NEEDS KAM: N4`, asking Kam to open the router route he chose on 11-24 14:58.
- **Main finding for M-a: the TLS half cannot be measured with what is on main.** The echo listener is plain HTTP only (`Commands/Oxpd1/README.md:331`-`:332`), and no TLS host is built. This run can show (a) whether the store ACCEPTS the self-signed dev root and (b) whether the printer can open a connection to the Mac. It cannot show whether the M577 then TRUSTS a TLS server signed by that root. So owed 103 is NARROWED, not closed, and that half of M-a moves to L1d.
- **Credentials (commission: read BY NAME).** The new `envsecret.py` reads `OXPD_M577_ADMIN_PASSWORD` and `OXPD_M577_ADMIN_USER` in-process, from the environment first and otherwise from their one line in `TUESDAY/4_Credentials/.env`. The new `lab_run_env.py` (B2044's `lab_run.py` with docsecret swapped out) hands the password to the lab through a named pipe, under the lab's default name. It refuses to run (exit 31) unless the user name is exactly `admin`, because the lab sends HTTP Basic for `admin` only. The echo verb refuses any credentials source that holds a name containing `ADMIN` (exit 12). So echo runs get a separate `@GUEST@` pipe with 16 random hex digits; HP says the guest password can be anything.
- **The lab is built, not published.** `src/Datasec.Suite.Lab/Datasec.Suite.Lab.csproj:5` is `<IsPublishable>false</IsPublishable>` (MEASURED). So the seat restores and builds the Lab project in its own `.tools/b2159-x85/clone`, in two heavy jobs (B2068's measured form). That meets the commission's "published once into its own `.tools/b<n>/`" in substance. The lab runs themselves are not heavy and never take the lock.

## FACTS RE-MEASURED (instrument, then what it printed)
- Origin (`gh api -X GET`, OXPd GH_CONFIG_DIR, 17:39:48): main `760e1a644ce9a419cf1b9132d0776e9e5eac1cac`, tree `8e3985c1`, PR 58. Open PRs: 0. `matching-refs/heads/b2159`: 0 rows.
- BASE tarball (by GET) extracted to `<d>/src_760e`: 679 files. Every `file:line` in the kit was printed by `grep -n` or `awk NR==` over that tree.
- Seat name X85: free. A program scan of the briefs folder plus the OXPd Briefs folder (non-`.pre-` files) found `SEAT-X85` only in the B2159 commission. Control X83: 4 files.
- Prior runs: across 118 OXPd `*STATUS.md` files, `ImportCaCertificate --execute` appears in 0 and `--echo async` in 0. Control `EnableTestService --execute` appears in 2 (B2048, B2068). BACKLOG has exactly 1 line starting with `103. - [ ] ` and 1 with `118. - [ ] `.
- B2068 (the last device run, READY) gives the pins `a36e8cb9...2d96` on both ports and shows `--addressing 2004` works for the Test service on this printer. That is the kit's PREDICTED R01.
- This Mac (17:42:57 and 17:51:24): en0 `192.168.20.220`. The route to 192.168.8.157 goes through `192.168.20.1` on en0. The application firewall reports `Firewall is disabled. (State = 0)`. `lsof` shows no listener on 18620-18629 (control: 15 LISTEN sockets in total). Load averages: `12.42 8.38 8.56`, then `6.75 11.61 10.50`. B2157 held the lock (`owner.txt` 17:40:20).
- `dscacheutil -q host -a name npi5a4e46.local` returned `ip_address: 192.168.8.157`.
- Project root has no `.git`, so run folders under `.tools/` pass the lab's exit-9 rule.
- Port scan: no 2026-11-26/27 SEAT kit (82 files across both folders) names 18620-18629. The scan's own control (`7627`) found 0 files, so the control did NOT fire. Treat this scan as weak; the `lsof` read is the one that counts.
- Seat tools: `clone.py` and `heavy.py` are B2068's bytes (same sha256; canonical heavy `31adedc8...`). `envsecret.py` is `53174619...` and `lab_run_env.py` is `7d97985b...`. The harness ran them against SYNTHETIC env files and a fake lab, 8 cases in `<d>/test/harness-run2.out`:
  - an admin run read the pipe;
  - a guest run got a 16-hex value;
  - a leak gave exit 30, with nothing saved;
  - a non-admin user gave exit 31 before any pipe;
  - `@CRED@` together with `@GUEST@` gave exit 2;
  - a duplicate name was refused;
  - an environment-only value worked;
  - `--shape` printed `user is admin: True`.
  The first harness run found a pipe left behind when the value read failed. I fixed the order (value read first, pipe second) and re-ran. The first run's folder is in `<d>/_quarantine/lane-run1`.
- Names in the kit: a case-insensitive scan for `kamil|kreiser|steve|paul` found 0. No control was planted. The only person-word is `NEEDS KAM:`, the template's own channel token.

## D-DECISIONS (all coordinator defaults, each a Q)
D1: row 3 runs first, then the echo, so at most one change is live on the printer at a time. D2: a one-day placeholder CA named `oxpd-lab-ca-test.local`. D3: the store's before-count `<k>` is read and must return after W33. D4: every printed undo runs token for token, including after a fault (applied Unknown). D5: credentials by name through a pipe; guest password random. D6: one session folder plus `undo-owed`. D7: findings are not STOPs. D8: no retries.

## Q-QUESTIONS FOR TUESDAY (each with its default; Q1 and Q2 STOP-CLASS)
- **Q1** Order and scope. Default **a**: row 3 first, then the echo; findings end READY. Alternatives: b, echo first; c, any finding is a STOP.
- **Q2** Credentials. Default **a**: `envsecret.py` reads by name (environment, then `.env`), checks user == `admin`, and hands the password over by pipe. Alternative b: B2068's `docsecret.py` reading from Kam's doc. The grant row still says "password (from his doc)", and whether the `.env` value equals the device password is UNMEASURED. One refusal stops all admin use.
- Q3: if the Test service is found ON, leave it on. Q4: an import fault is a finding, and the undo always runs. Q5: no callback means N4 and no retry. Q6: host `npi5a4e46.local` if it resolves to .157, otherwise the IP. Q7: port 18627, bound to en0, 60 s wait (**DRAFTER_RULES says Tuesday assigns ports; this is a proposal**). Q8: restore plus build (not publishable). Q9: names `.tools/b2159-x85` and `2026-11-27_B2159_SEAT-X85_STATUS.md`, READY `READY B2159-X85:`, to avoid a collision across the four B2159 seats. Q10: no gate, records by the next records pass, Opus, READY at Step 0 + 120 min, pane `Datasec/OXPd2-X85`, runs beside the builder (plan Q3). Q11: the CA name and days.

## CHAIN INPUTS (each from BASE or an earlier step): kit section CHAIN INPUTS, 7 rows; only one input is not produced by the drafter or by an earlier step: the credentials (RELAYED to exist by the commission; never read by the drafter).

## UNMEASURED
- Whether the `.env` value is the device's current admin password, and whether `OXPD_M577_ADMIN_USER` is `admin`. If it is not, the seat stops at Step 1 with exit 31 or a `--shape` False, before any request.
- Whether the M577 accepts guest for echo, whether it sends the async callback over plain HTTP, and whether the router forwards 192.168.8 to 192.168.20. That last point is the measurement itself.
- Whether HP's store takes a self-signed root, and how it exports an entry.
- Whether `dotnet build` of the Lab alone still succeeds at 760e1a64. B2068 measured it at 217286f3, and the hosted CI builds the solution at 760e1a64.
- Whether the plan's "runbook load check (two reads 120 s apart, under 24)" exists in a runbook. It is not in the OXPd `SETUP_RUNBOOK.md` (only 3 lines mention load, none of them this rule). The kit cites it as RELAYED from plan B2154 section D.

## OUTSIDE-THE-FENCES DISCLOSURE
- **One name lookup:** `dscacheutil -q host -a name npi5a4e46.local`, which may have sent an mDNS query on the LAN that the printer answers. No OXPd, HTTP or TLS request went to the printer.
- **Local reads only:** `ipconfig`, `route -n get`, `socketfilterfw --get*`, `lsof`, `uptime`, `tmux list-panes`. I also read the lock's `owner.txt`.
- **Not read:** no dotnet job, no lock taken. I never read `TUESDAY/4_Credentials/.env`, `<project>/4_Credentials`, Source_Documents or key folders.
- **Writes:** only the kit, its `.measured`, this report, and scratch under `fleet/state/s334/d2159-L9/` (tarball, tools, harness, `gen/`, `_quarantine/`). The harness created `__pycache__` under `seat-tools`; I moved it to `_quarantine`.
- **Not read whole:** B2138's kit (read lines 1-90; its shape is the same as B2153's, which I read whole) and the B2153 sidecar (first 5 KB). I read B2068's kit and STATUS whole as the closer device-run template.
