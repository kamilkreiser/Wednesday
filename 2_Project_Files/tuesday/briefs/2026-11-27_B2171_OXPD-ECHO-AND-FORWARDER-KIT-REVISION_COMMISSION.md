# B2171 COMMISSION (one in-session READ-ONLY drafter, Opus per OXPd CLAUDE.md line 7) -- Datasec/OXPd: revise the forwarder-test kit X88 so the echo runs (guest credential by file), with the direct echo first

Commissioned by Tuesday (s334). `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` binds whole.

## What happened (read at source)
X85 (kit `tuesday/briefs/2026-11-27_B2159_SEAT-X85_oxpd2-l9-network-path.md`, stamped) ran on the M577. Its STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Briefs/2026-11-27_B2159_SEAT-X85_STATUS.md` (read it whole): **row 3 TAKEN** (store 11 -> 12 -> 11, removed by its undo), Test service off before and after, `undo-owed nothing is owed`; then **E01 hung and was killed at 300 s** (nothing sent): "`oxpd1 echo` opens the credentials file twice (Oxpd1EchoVerb.cs:288 and :296) while lab_run_env.py feeds the @GUEST@ pipe once". The async callback (owed 118) is therefore still UNMEASURED.

## Tuesday's answer to the seat's question (decided)
The guest credential is handed as a **mode-600 file holding only the random guest value** (written by the seat tool in the run folder, one line in the lab's own guest name `OXPD_TEST_PRINTER_GUEST_PASSWORD=`, 16 random hex digits, never the admin value; moved to `<lane>/_quarantine/` after the run, never deleted). Why: HP accepts any guest password ("guest (username=guest, password={anything})", the lab README line the kit cites), so the file holds nothing secret, and it needs no lab change. The ADMIN password keeps the named-pipe form (read once per open; the echo verb never takes the admin name).

## Draft
Revise kit `tuesday/briefs/2026-11-27_B2169_SEAT-X88_oxpd2-s14b-forwarder-test.md` (read it whole with its report and tools in `fleet/state/s334/d2169-T/`) into `2026-11-27_B2171_SEAT-X88_oxpd2-echo-and-forwarder-r2.md` (+ `.measured` + drafter report), SUPERSEDING it (first line says so):
1. Drop its "after X85 READY" precondition: X85 ended STOPPED with row 3 done and the printer clean; the new kit's precondition is that STATUS's last line as above and `nothing is owed`.
2. FIRST the direct echo pair X85 could not run (Test service on only if off by its printed undo, E01 sync guest, E02 async guest with the listener on the Mac at port 18627, service off by its printed undo), THEN the forwarder test as drafted (every request through `fwd.py` with a direct control).
3. The seat tool change: a `lab_run_env.py` variant (or a new small tool) that writes the guest file (mode 600, value only, the lab's guest name) and passes `--credentials-file <that file>` for echo runs; prove it on synthetic files only (a hang reproduction against a fake lab that opens the file twice, then the fix passing).
4. Every write still undone in the run; the printer grant (Kam 17:54:13 "this printer is yours for the project...") does not widen this kit (no reboot, firmware, reset, wipe).
5. Ports: 18627 (direct echo listener) and the X88 draft's own (18631, 18632) as assigned by Tuesday.

## Fences
READ-ONLY everywhere except your outputs under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/` and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s334/d2171/`. No device contact, no Azure, no write in the OXPd project, Jira, GitHub, cards or mail. Never read `Source_Documents/`, `4_Credentials/` or key folders. Never type `cd`; never delete. Every clock printed by `date`. Return 10 lines, first `STARTABLE: YES|NO`, then Questions with defaults.
