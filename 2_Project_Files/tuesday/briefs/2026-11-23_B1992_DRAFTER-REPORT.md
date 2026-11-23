STARTABLE: YES (on Q1 = "a" at Stamp S4)

# B1992 DRAFTER REPORT (lane L4, the lab `print` command, seat X53)

Written by Tuesday (s317) from the drafter's final message, because the harness refused the report file to the subagent. Text below is the drafter's, unchanged in substance; nothing was re-measured by Tuesday in writing it.

Kit: `2026-11-23_B1992_SEAT-X53_oxpd2-l4.md` (88,867 bytes) + `.measured`; stamp_check 222 of 222 (drafter's run). Gate tier G2 by the commission (Q7 offers G1: first lab command that writes to a device). Size XS-S: 13 paths, +796/-6, 26 test cases in 14 methods, 14 mutants.

## BLUF
- The commission's paths alone cannot land (probes): the Lab project does not reference the transport assembly (removing it: CS0234 / CS0246), and landed cell P13 (`tests/Datasec.Suite.Lab.Tests/ProbeTests.cs:207`) pins the registry to exactly ["probe"] (with the registry line added: Failed 1, P13 'Collections differ').
- Q1 default a adds six paths: (a) one ProjectReference in `Datasec.Suite.Lab.csproj`; (b) the two Lab lock files (project entries only); (c) P13's list to ["probe","print"]; (d) `DeviceChannel.cs:37` comment "The tool's ONE way to a device" -> "The probe's ..."; (e) Lab README print bullet, Trust and run-folder sentences limited to probe.
- The command: `print <host> --run <new folder> --pin <sha256> --port <631|443> [--path] [--pages 1..600] [--timeout-seconds] [--execute]`; ONE IPP Print-Job of an in-memory synthetic PDF through the landed HttpIppTransport and PrintJobSender; dry run without --execute (connects to nothing); writes only summary.txt; exit 0 accepted, 2 usage, 4 TLS refused, 5 run folder exists, 6 refused or busy (not re-sent), 7 other.
- Could reach the M577: `print --execute` (IPP, either generation; B1968 first-run step 6). Dry run reaches nothing.

## Facts re-measured (drafter)
- main d804de5e (gh api, 17:53:19); no b1992 ref; 0 open PRs; 0 open alerts; private + push true. BASE hosted PASS 1942 / rules 628 / guards 14, 15.
- Frozen patches in fresh clone8: red 1968 / failed 8 / passed 1956 / skipped 4 (all 8 assertion failures in PrintTests); green 1968 / 0 / 1964 / 4; MUTANTS 14 of 14 MATCH, 14 of 14 undone equal; 34 of 34 lock files unchanged after --force; GUARD 14 and 15; Ran 111; RULES clean (634 files); CHECKS 6 of 6; WORDS clean; gitleaks control rc 1 then rc 0; run_step neutral scan on a prototype commit 25 of 25, not among them 0.
- Rulings: 9 rows, none on printing; CLARIFICATIONS none on this command (controls found).
- Partition: FK has no Lab consumer; O1 owns slnx; the transport already has its slnx line.

## Questions with defaults
Q1 (STOP-class) the 13 paths: a yes / b drop (d),(e) and re-draft 2-fix.diff / c commission paths only (refused: does not compile, P13 red). Q2 dry run unless --execute: yes. Q3 pin and port required, one port per run: yes. Q4 synthetic PDF only, 1-600 pages, default 1: yes. Q5 ReasonKeepingTransport wrapper: yes. Q6 the false registry comment `CommandRegistry.cs:19` to the records seat: yes. Q7 Opus, READY Step 0 + 110, push by Step 0 + 80, X53, G2 round 1 of 2, hard stop 23:30: yes (alt G1). Q8 the kit's commit-message.txt (251 bytes): yes.

## UNMEASURED
Every hosted leg of this lane's head (PREDICTED total 1968, rules 634, linux succeeded 1964, windows 1947); R06/R07 on Windows; any real printer (port, path, chunked bodies, HTTP auth, rendering); never run on this lane: clone.py seat, the commit under the repository identity, the push, hosted3 on its head, the rebase.

## Outside the fences (drafter's disclosure)
Kit and sidecar written by the drafter's scripts (fill_kit.py, sidecar.py), not the Write tool; one prototype commit as draft@invalid.example in scratch clone8 (push URL invalid://no-push, nothing pushed); clone7 broken by the drafter's own edit, quarantined; nothing deleted; no project write, no printer, no host but GitHub; observed `.tools/b1993` (another seat's) listed only; every heavy job through heavy.py (lock waits 0-11, load1 peak 18.02).

## Tuesday's note (s317)
L4 and L5 (B1997) BOTH touch the Lab csproj, the Lab lock files, P13's command list and the Lab README: they land SERIALLY, L4 first (ready first); L5's drafter was told by message to plan its kit on main after L4 lands.
