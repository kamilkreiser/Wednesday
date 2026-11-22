# B1913 SWEEP COMMISSION (Opus, in-session, READ-ONLY) -- Datasec / OXPd_2: every no-hardware work package still open, split into file-disjoint lanes for tonight

Commissioned by Tuesday (s310), written at 2026-11-22 20:05:18 +1100, on the product owner's live-board word of 2026-11-22 20:03:36, verbatim: "great.  Please keep going on OXPd through the night and use as many agents as you can". Model OPUS (the project's `CLAUDE.md` line 7). Return a 10-line summary; write the full result to `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1913_OXPD-OVERNIGHT-LANES.md`.

## THE QUESTION
Which OXPd work can a build seat do tonight with NO hardware (no printer, no device, no HP or Microsoft portal, no Azure or tenant action, no message to any person, no spend), and how does it split into lanes that share no file, so several seats can run at once?

## SOURCES (read each yourself; nothing here is a fact until you read it)
- The project: `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/` -- its `CLAUDE.md` (whole: the rules, the landing rule, what a seat may do), `BACKLOG.md` (the work-package table under `## The no-hardware work packages and their Jira keys` and the owed items 1 to 58), `5_Project_History/history.md` (head: what landed), `1_Project_Definition/CLARIFICATIONS.md` (the product owner's rulings; read the entries a lane would rest on), and the plan and architecture under `1_Project_Definition/Design/` (find them by `ls`; read the work-package sections you cite, not the whole files).
- Origin `datasecau/OXPd_2` by `gh api -X GET` under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.gh-config'`: main (Tuesday read `bf6b441e30900127487145c3b65b29d8cc9eb5ea` at 20:00), the tree (`git/trees/main?recursive=1`), merged pull requests 1 to 17 and their file lists.
- Jira OXPD2 by GET only (credentials by name in-process from the project's `4_Credentials/.env`, never printed): every issue (25 at 19:34; Tuesday read 0 Done), status, parent, labels.
- Live right now: seat `Datasec/OXPd2-X27` (kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1912_SEAT-X27_oxpd2-f13-test-race.md`) owns `tests/Datasec.Suite.Sessions.Tests/Fakes.cs` and `RefreshBoundCellTests.cs`: no lane of yours may touch them.

## WHAT TO PRODUCE (the lanes file)
1. **BLUF**: how many lanes, which work packages, and the order.
2. **Per lane**: id, work package(s) and Jira key(s), the scope sentence quoted from the plan or ticket, the exact set of paths it would create or change (by directory, from the tree), the paths it must NOT touch, its dependencies on other lanes or on main, the review tier (G1 for security, credential, network or parsing surfaces; G2 for tests, docs, config), a size estimate, and what in the plan or a ruling authorises it (quote it).
3. **The partition table**: every lane against every other, proving no shared path (shared project files such as `Datasec.Suite.slnx`, `Directory.Packages.props`, lock files and `.github/workflows/ci.yml` are the hard cases: name which single lane owns each, or say the lanes must be serial on that file).
4. **Owed items 1 to 58** that are agent-actionable now as small lanes (for example B1904 F1 and F2, B1905 F2: fix rounds with cells), each sized, with its files.
5. **EXCLUDED, with the reason** for each: needs hardware, needs a ruling or new words for a person, needs Azure, waits on another lane.
6. **PRIOR WORK**: for each lane, what already exists on main for it (by path and pull request), so no seat rebuilds what landed.
7. **Machine notes**: one heavy dotnet job at a time across seats (the project's `.tools/wave1-heavy.lock.d` rule in today's kits); say how many seats can usefully run at once given that.

## RULES
READ-ONLY: no write to any project file, Jira or GitHub; `gh api -X GET` and Jira GET only; no `cd` (absolute single-quoted paths, the path holds `!`); never delete; `python3 -I`; every count by program with a positive control; never open, list or hash anything under `Source_Documents/` (its one PROVENANCE file excepted) or the NAS library; nothing to any human. Write only the lanes file above and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1913/`. Who-decided lines name the coordinator unless a card print or a dated board message of the product owner says otherwise.
