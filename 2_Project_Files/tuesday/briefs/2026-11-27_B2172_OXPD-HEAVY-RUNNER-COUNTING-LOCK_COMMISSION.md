# B2172 — OXPd heavy-job runner v2: counting lock of 2, light-project bypass, process-tree kill (tooling, in session, Opus)

From Tuesday s335 (Datasec coordinator), for one in-session Opus agent. Client: Datasec. Project served: OXPd_2. You write ONLY under your scratch `<d>` = `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/d2172/` (create it). Nothing outside it.

## Why
Kam asked (Tuesday terminal 2026-11-27, verbatim): "test if the heaby build can be pushed to 2-5.  your call but lets make the decision on what can be done". The experiment B2157 ran it; Tuesday decided (Fleet Activity card `datasec-parallel-builds-decision-1127`): OXPd = a counting lock of 2 for whole-solution jobs plus per-project locks for light app lanes, never 3+. This commission builds the OXPd runner change. It does NOT install it anywhere live.

## Read first, whole
1. `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2157_PARALLEL-HEAVY-BUILD-REPORT.md` — especially `## FOR TUESDAY` section 1 (heavy.py) and section 4. That section is your spec. Section 2 (nexusai-lock.sh) and 3 are NOT yours (another project's files; a NexusAI seat does them).
2. Today's runner: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s334/d2170/seat-tools/heavy.py` (sha256 `31adedc88371ae8dd9ccdf9553ccdfb22e822a9a3ec185c5eb4122f1b9fbfe9c`, measured by Tuesday s335 with shasum). Copy it; never edit it in place (live kit B2170 pins that sha).
3. B2157's own runners for reference only: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/` — find `x2157` by `find ... -maxdepth 3 -name 'x2157'`; read, do not run against any real project folder.

## Deliverable
- `<d>/heavy.py` — v2 implementing FOR TUESDAY section 1 items 1-6 exactly (slots file `<P>/.tools/heavy-slots`, lock names `wave1-heavy.lock.d` for slot 1 unchanged and `.d.2..` for the rest, `owner.txt` gains `slot <k>`, same-checkout refusal exit 96, load gate slot 1 load1<7 / slot>=2 two reads 120 s apart both <24, light-project bypass via `<P>/.tools/heavy-light-projects`, `Popen(start_new_session=True)` + killpg TERM, 15 s, KILL, then `ORPHAN <pid> <cmd>` report for any process whose command line holds the working folder). Add `HEAVY_LOCK_ROOT` (and, for tests only, an override for the load reader and the 120 s gap) so proofs run in scratch.
- `<d>/test_heavy.py` — runs every proof listed under section 1 "Proofs" in scratch only: two runners with slots=2 both acquire; a third waits then acquires on a release; a slot-1-only copy of TODAY's runner plus two v2 runners never exceed 2 held; same-checkout refusal exit 96; a job whose child forks a grandchild, with a short TIMEOUT, leaves no process behind (check by pgid and by command-line grep); `heavy-slots` absent = exactly today's behaviour. Each proof has a must-fail control (run today's runner where the property is new, show it fails that proof).
- `<d>/REPORT.md` — FOUND / TESTED (and what was NOT tested) / HOW (commands, controls, rc), the sha256 of the new heavy.py, a unified diff against today's runner, and a short "ADOPTION" section: what a future OXPd kit must change (its THE TOOLS row and Stamp S8 sha; who writes `<P>/.tools/heavy-slots` = `2` and `heavy-light-projects` — an OXPd seat, never Tuesday; the "one heavy job" sentence becomes "a heavy slot (at most 2 on this machine)").

## Holds
- No write, lock, mkdir or process anywhere in `/Volumes/Datasec_DEV/!CODING/` (read-only). Never touch a live lock folder. No dotnet job. No network.
- Never `cd` (write absolute paths); never delete (move to `<d>/_quarantine/`); macOS bash 3.2 / system python3 with `-I`.
- Never report a proof as passing without its printed output; a proof you could not run is written as NOT RUN with the reason.
- Final message: the REPORT path and one paragraph BLUF.
