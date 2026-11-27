# B2153-B2155 COMMISSION (three in-session READ-ONLY agents, Opus per OXPd CLAUDE.md line 7) -- Datasec/OXPd: Kam wants a WORKING COPY BEFORE CHRISTMAS

Kam's words (Tuesday terminal, 2026-11-27, verbatim):
- "please keep prioritising OXPd as I would like a working copy before chistmas"
- "use as many agents as possible."

Commissioned by Tuesday (s333).

**Rules for all three agents:**
- `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` binds whole.
- READ-ONLY everywhere except your own outputs under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/` and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/d<your B number>/`.
- No write in the OXPd project folder, Jira, GitHub, cards or mail.
- GitHub reads only by `gh api -X GET` under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.gh-config'`.
- Never read `Source_Documents/`, `4_Credentials/` or key folders.
- Never type `cd`; never delete.
- Every clock is printed by `date`.
- Main is `760e1a644ce9a419cf1b9132d0776e9e5eac1cac` (PR 58 landed); re-read it.
- **One OXPd build seat runs at a time** (the shared wave lock). So drafters run NO dotnet job: every expectation is PREDICTED, with the assertion each must break named.
- Return 10 lines, first line `DONE` or `STARTABLE: YES|NO`, then Questions with defaults.

## B2154 (lane P, the plan): the critical path to a WORKING COPY by 2026-12-24
Write `2026-11-27_B2154_OXPD-WORKING-COPY-PLAN.md`.

**Read:**
- `<OXPd_2>/CLAUDE.md`;
- `1_Project_Definition/Design/02_architecture.md` and `03_plan-of-attack-and-build.md` whole;
- `CLARIFICATIONS.md` (the last twenty entries whole);
- `BACKLOG.md` (the open owed items);
- `SETUP_RUNBOOK.md`;
- the newest `history.md` entries;
- OXPD2 Jira by GET (open issues);
- `tuesday/briefs/2026-11-26_SWEEP-0446_datasec-actionable-lanes.md` (the OX-A to OX-D lanes).

**Answer:**
- (a) What "a working copy" can mean against the plan's own phases and acceptance criteria. Quote them; never invent one. Name the smallest end-to-end flow that would count, and say which reading you took.
- (b) What is BUILT on main (by module, with the merged PRs), what is MISSING for that flow, and what is owed.
- (c) A dated critical path of lanes from now to 2026-12-24, each lane with:
  - its files, kept DISJOINT so parallel seats do not collide;
  - its size;
  - its dependencies;
  - whether it needs a device run, an HP answer, an Azure action or a word of Kam's. Each of those needs a card with a default; list them separately, with the question in one sentence each, and the C-entry or card that already rules it if one exists (search `decision_queue.sh prior` read-only, or the project's CLARIFICATIONS).
- (d) Which lanes can run IN PARALLEL despite the one-wave-lock rule. For example: text and records lanes need no heavy job; a lane whose dotnet jobs are short. Propose a schedule.
- (e) The risks to the date.

Say plainly where the plan or the records disagree with the code.

## B2153 (lane C2, the code kit): OXPd lane OX-C kit 2 PART 2, owed 137 and 121
**Form:** kit 1 `2026-11-27_B2134_SEAT-X80_oxpd2-lane-c-kit1-hygiene.md` and part 1 `2026-11-27_B2138_SEAT-X81_oxpd2-lane-c-kit2.md`, with their commissions. Read all whole.

**Scope:**
- Owed 137: the Server tests' per-cell bound on `HostRig.StartAsync`/`StopAsync`.
- Owed 121: the other device handlers' chain-policy README line in three modules.
- Read both items whole at BACKLOG.md.

**Write:** `2026-11-27_B2153_SEAT-X82_oxpd2-lane-c-kit2-part2.md` (check that X82 is free, by program), its `.measured`, and the drafter report.

Owed 138 (the heavy-job runner `heavy.py`, a process group per job) is NOT in this kit: name it, and say whether its fix should land before 137's (Question with a default).

## B2155 (lane D, the code kit): OXPd lane OX-D, kit 1
Read SWEEP-0446's OX-D block and every owed item it lists, whole. Check each against the records passes since 11-26 (B2124, B2132, B2140, B2146's kit) and against main. **An item already closed is DROPPED, said so with the line that closes it.**

Draft kit 1 of whatever remains buildable with no device, no HP answer and no ruling. The form is the same as B2153's.

**Write:** `2026-11-27_B2155_SEAT-X83_oxpd2-lane-d-kit1.md` (check that X83 is free), its `.measured`, and the drafter report.

**Partition:** B2155 shares NO path with B2153's or with B2146's records files. State both sides; a shared path is a STOP for the drafting.
