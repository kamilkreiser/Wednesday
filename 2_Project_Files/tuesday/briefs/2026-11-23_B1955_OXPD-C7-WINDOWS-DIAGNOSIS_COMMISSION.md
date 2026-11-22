# B1955 DIAGNOSIS COMMISSION (Opus, in-session, READ-ONLY toward the project) -- OXPd: Contracts cell C7 red on hosted Windows at the A2-F2 head

Commissioned by Tuesday (s314). Model Opus (OXPd `CLAUDE.md`: every agent on this project runs on the newest Opus). Output: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1955_DIAGNOSIS.md`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/c7diag/`. Return a 10-line summary whose first line is one of: `TIMING-FLAKY ON HOSTED WINDOWS` / `A2-F2 REACHES C7` / `OTHER: <one line>` / `UNDETERMINED: <what would settle it>`.

## What happened (Tuesday's handover, `/Volumes/Datasec_DEV/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md` DELTA 1361 item 1(b), and today's note `/Volumes/Datasec_DEV/TUESDAY/0_Brain/daily_tuesday/2026-11-23.md` line '05:01'; reported, re-check each at source)
- Lane A2-F2 (kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1953_SEAT-X43_oxpd2-a2-f2.md`, Identity paths only: one catch boundary for a malformed name escape in the card store) pushed branch `b1953/a2-f2-malformed-escape` at `10f446f3` (one commit on main `49f686a8`).
- Its hosted run 45052136167 is red on WINDOWS ALONE, on a cell outside the lane: `Datasec.Suite.Contracts.Tests.GatewayStubTests.C7_one_send_reaches_every_connection_once_and_bad_bodies_send_nothing`, message "no hub message arrived within 5 s" (`GatewayStubTests.cs:114`, job 137299375943). Reported green at BASE, on linux, in every local run; Identity green.
- No earlier record of C7 failing (BACKLOG 'GatewayStub' count 0). The cell came from lane WP04, kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1829_SEAT-X17_oxpd2-wp04-clients-and-gateway-stub.md`.
- OXPd main has since moved: `5b66a7b16f9c35a48f7feef504c0fa69e5701dcc` (PR 30, README + one test file in Universal Print, no Contracts path). Re-read it.

## The question
Is C7's Windows failure (i) a timing flake of the cell on hosted Windows runners (the 5 s hub wait), independent of A2-F2; (ii) something A2-F2's change can reach; or (iii) neither (say what)?

## What to read (all read-only)
1. The cell and the gateway stub's hub wait: the test file and the stub it drives, at `10f446f3` and at `49f686a8` (`gh api -X GET repos/datasecau/OXPd_2/contents/<path>?ref=<sha>`). What does "arrived within 5 s" wait on (a SignalR connection start, a send, a polling loop)? Is there a start/handshake race before the send?
2. The failing Windows job's log (job 137299375943, `gh api -X GET repos/datasecau/OXPd_2/actions/jobs/137299375943/logs`): the C7 lines, timing around it, other slow cells, the runner image.
3. The Windows legs of main's recent push and PR runs (at least the last 10 runs that ran the Contracts tests, list them by program): C7's duration and result in each (the trx or the test log line). A cell near its 5 s bound on green runs is the flaky signature; give the distribution.
4. Can A2-F2 reach it at all: the diff `49f686a8...10f446f3` by file; does any Contracts project reference Identity (the .csproj ProjectReference graph), or share a static, a port, a fixture or a process-wide resource with the changed code?
5. Optional, only if 1-4 do not settle it: one local run of the Contracts test project in a scratch clone at `10f446f3` (push URL `invalid://no-push`, clone under the scratch folder) through `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/.tools/` heavy lock if it exists (never break another holder's lock), C7 run 20 times by filter (print the Total line; Total 0 is a STOP). Linux/macOS results do not stand in for hosted Windows: say so.

## Deliver
FOUND / TESTED (and what was NOT tested) / HOW (instrument, command, positive and negative controls). If TIMING-FLAKY: the minimal fix shape for a follow-up lane (e.g. awaiting the hub connection's start before the send, or a bounded wait keyed on the connection state, NOT simply a longer timeout unless the evidence says the bound is the only defect), with file:line, and a test that would prove it. Name whether a re-run of 45052136167's Windows job would be a MEASUREMENT worth taking (a re-run to turn it green is never the fix; Tuesday decides).

## Rules
READ-ONLY toward the project, Jira and GitHub (`gh api -X GET` only, under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.gh-config'`); git in the project checkout: read verbs only (`git --no-optional-locks`); no re-run, no push, no PR, no comment; no `cd` (absolute single-quoted paths; project paths hold `!`); `python3 -I`; never delete (quarantine); every count by program with a positive control; nothing under `Source_Documents/` or the NAS library; nothing to any human; no other client's material. Write only the output file and the scratch folder.
