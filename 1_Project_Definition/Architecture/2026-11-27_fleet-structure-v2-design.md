---
date: 2026-11-27
type: design proposal (for Kam's ruling; nothing here is built)
ticket: WED-170
author: Wednesday (Fable 5.2)
status: proposed
sources: 0_Brain/reference/2026-11-27_fleet-structure-research/ (current_structure_census.md read whole; video_postgres_memory.md comparison section read; linkedin_twelve_repos.md by its summary table)
---

# Fleet structure v2: how Wednesday, Tuesday and Friday wake, remember, brief and load skills

## The short version

1. **The wake routine is the real cost, and it is fixable without a database.** A seat is told to read 229K to 430K tokens at boot. Most of that is handover history and expired rows, not knowledge. Fix: a fixed-size wake pack and a handover that a tool keeps to one block.
2. **Use Postgres where it wins: for records that are rows, written by three seats at once.** Cards, chat, ledger rows, scores, grants and checkpoints. Keep lessons, identity and briefs as markdown under git, with Postgres as a search index over them. This is the pattern of the project the video itself holds up as the markdown failure (GBrain): its own README says markdown is canonical and the database is rebuildable from it.
3. **Give every project two briefs it does not have today:** a full one for coordinators and a generated cut-down one that every worker loads, plus one card per kind of seat. Task briefs then carry only the task.
4. **Skills become a registry with roles, pinned versions and an update check at load.** A security reviewer loads the security set; every agent loads the general set.
5. **The twelve repos are all security tools.** Three are usable for the security specialist, one of them as the checker for every other third-party skill. None is a general skill.

## What was measured today (census, bytes divided by 4 as tokens)

| | Wednesday | Tuesday | Friday |
|---|---|---|---|
| Mandated boot reads | ~229K tokens | ~430K | ~305K |
| Largest item: the handover file | 287 KB | 937 KB | 372 KB |
| Rules card | 113 KB | 112 KB | 115 KB |

- The handover file says of itself "never stack"; mine holds 106 stacked blocks from 14 days. A rule nothing enforces.
- A lesson's rule is held in up to seven places. Two generated digests of 740 KB each are committed on every launch.
- The two rules files still say "read ALL learnings"; the launcher says read the card instead.
- The median commissioning brief is 38 KB. Holds, mail rules, wrap rules and routing are rewritten in fresh words every time; no standing file is pointed at.
- The three seats launch workers three different ways (mail, absolute file path, relative file path).
- No project has a brief for coordinators or for workers. A worker gets the project's rules file plus whatever the task brief restates.
- No skill or standard has a version, a source or an update check. The QA charter and gate templates name no security standard.
- 72% of the brain's size outside `reference/` is backup copies.

## What the video does and does not show

It is a 15-minute vendor talk (Cognee). No schema, no measurement; the demo failed; its Postgres graph store is labelled a demo feature in its own repository. Its useful ideas, which the comparable projects share:

- **Retrieve per task, never load everything at boot.** None of the five projects read describes a boot-time digest.
- **Two memory kinds:** a session scratch area and permanent memory, with a distil step between them.
- **Scopes with promotion:** agent, then team, then organisation. We already have this shape (project, management, Wednesday tiers) but only as a tag in a file.
- **Never hard-delete; supersede and re-weight.** We already do this by rule.
- **Writes happen by hooks, not by the agent remembering to write.**

## The design, item by item

### 1. Seat structure: one wake routine, sized by a budget

| Today | Proposed |
|---|---|
| The boot prompt names files to read whole; files grow without limit | A generated **wake pack** per seat with a hard size budget (target 40K to 60K tokens); the launcher refuses to hand over a pack above budget and says which part grew |
| Handover = a file blocks are stacked onto | **STATE**: one current block per seat, written through a tool that moves the previous block to the archive in the same action. Stacking becomes impossible, not forbidden |
| Grants file read whole (87 KB, mostly expired rows) | Live grants only in the pack; expired rows stay in the record and are looked up on demand |
| Rules card read whole (113 KB) | The "most reinforced" section in the pack; the rest fetched by trigger at the moment of action (the lookup already exists; decision cards and briefs already call it) |
| Project index and entries read whole (320 KB) | Replaced by the coordinator project briefs of item 3 |
| Prompt written in Wednesday's voice for all three seats; five contradictions between rules files | One seat-neutral template with per-seat values; the rules files corrected in the same change |
| Three worker launch paths | One: brief by mail, verified at destination, then launch (the gated path), for all three seats |
| A wake watcher that can go deaf silently (it did today) | Its health is part of the wake pack check; a deaf watcher shows on the live board |

Measure of success: the census re-run shows mandated boot reads at or under 60K tokens for every seat, and a seat's statusline reads under 15% after boot.

### 2. Memory: markdown stays the master for knowledge, Postgres holds the rows

| Kind of memory | Examples | Home | Why |
|---|---|---|---|
| Knowledge a person edits and reviews | lessons, identity, project briefs, skills | **Markdown in git**, indexed into Postgres | history, review and diff matter; three machines already sync by git |
| Records that are rows, written concurrently | decision cards (1,706), chat, ledger rows (2,700+), delegation scores (1,810), grants, checkpoints, wake log | **Postgres tables** | today these are JSON and markdown tables merged by six purpose-built union tools; an automatic stash corrupted two of them twice in one day |
| Retrieval | "what do we know about X", "which lessons fire on a deploy" | **Postgres index** (full text first; vectors only if full text proves too weak) | replaces boot-time loading with lookup at the moment of action |

Isolation: one schema or row policy per client, so a Datasec seat physically cannot read Secuura rows. Today that separation is an instruction plus hooks.

**Where Postgres runs is the decision I cannot make for you.** The standing rule says no project state off the drive and nothing may start a Postgres service on this Mac. Two ways to satisfy the intent:

- **Local, rebuildable:** each machine runs Postgres as an index built from the files. Nothing to sync, no cost, a lost database is rebuilt. It gives retrieval; it does not give shared rows.
- **One hosted database** beside the live board in the Wednesday Azure resource group: the single shared home for the row-shaped records, reached by each seat with its own certificate as the board is today. It costs money each month (not yet priced) and puts client-tagged records in a cloud database, so encryption and residency need designing before it is switched on.

Recommended order: local index first (proves retrieval, no spend), then a priced, written design for the hosted row store for your ruling.

### 3. Project briefs: full for coordinators, cut-down for workers

Per project, in the project's own repository, written by that project's own agent and reviewed by its coordinator (Tuesday for Datasec):

| File | Reader | Size target | Holds |
|---|---|---|---|
| `PROJECT_BRIEF.md` | coordinators | no hard cap | intent, architecture, environments and who may touch each, people, your standing rulings for the project, known traps, where state lives |
| `WORKER_BRIEF.md` | every worker, at load | about 6 KB | generated from the full brief: intent, architecture map, environments and hard holds, how to report. A check fails if it is older than its source |
| Lane cards | one per kind of seat (deploy, box read, merge, build, QA gate) | 5 to 10 KB each | the standing mechanics that every brief re-writes today |
| Task brief | the one worker | target median 12 KB (38 KB today) | only the task, its authority, its provenance |

Pilot on Secuura/Blockchain, where today's deploy and demo-read briefs (57 KB and 34 KB) are the baseline.

### 4. Specialist skills, with an update check at load

- **A registry** (one tracked file): skill id, roles it serves, source, pinned version or date, content hash, last checked.
- **Roles:** every agent loads the general set (verify before done, no skipped failures, git hygiene, credentials, client isolation). A specialist adds its set at launch.
- **Security reviewer set, first build:** OWASP ASVS and Top 10, NIST (CSF 2.0, the secure software development framework, 800-53 where relevant), the Australian Essential Eight maturity model, GDPR, the Australian Privacy Principles. One skill per standard, each a checklist the reviewer works through and cites by control number in its findings.
- **The update check:** at each load (cached for a day) the loader compares the publisher's current version or date with the pinned one. On a difference the agent still reviews against the pinned text, says so at the top of its report, and a ticket is raised to re-pin. Nothing is pulled in automatically: a skill is loaded into an agent with repository and credential access, so every change is read first.
- A skill that maps a review to OWASP, NIST CSF, GDPR and the Australian Privacy Principles is already listed for this seat's session (by its description; its body is not yet read); it is the candidate starting point. Essential Eight is the gap.

### 5. The twelve repositories

| Verdict | Repositories | Use |
|---|---|---|
| Adopt for the security specialist, after a full read | Cloudflare security-audit-skill; Anthropic claude-code-security-review (its command matches a skill already present here) | source-audit and diff-review procedures |
| Adopt as the gate for every third-party skill | NVIDIA SkillSpector | no outside skill enters the registry without its scan and a human-readable report |
| Call as tools from a gate, not load as skills | TruffleHog, Trivy, Semgrep | secrets, dependencies and static analysis inside the QA gate |
| Do not adopt | Strix (its skills tell the agent to pipe a remote installer into a shell), the OpenAI plugin as a plugin (passes cloud credentials through), Comp's configuration, PyRIT, Nuclei (active probing of live targets), Infisical | load-time risk or not a skill |

General skills for all loaders do not come from this list; they come from refreshing our own fifteen vault skills, ten of which have not changed since April.

## How it would be built

- Each piece is built by a Fable seat in a cockpit pane, claimed, gated, and proven on one seat before the others.
- Order: (1) wake pack and enforced handover, on Wednesday first; (2) project briefs and lane cards, Secuura/Blockchain pilot; (3) skills registry and the security specialist; (4) local Postgres index; (5) the hosted row store, only on your ruling.
- Shared launcher changes are claimed with Tuesday and Friday first. Nothing shared changes before you rule.
- Every step ends with the census re-run, so the gain is measured.

## What I am not recommending, and why

- **Moving lessons into a database as the master copy.** The measured pain is boot size and stacking; a database does not shrink what a seat is told to read. Git gives lessons history and review for free. If retrieval over the index proves this wrong, it can be revisited.
- **Adopting Cognee or any memory product whole.** Its Postgres store is a demo by its own label, and our isolation and never-delete rules are stricter than any of the five projects read.

## Decisions for you

1. Go ahead with steps 1 to 3 (no money, each reversible)?
2. Where Postgres runs: local index now and a priced hosted design later (recommended), hosted from the start, or local only.

## Input from the other seats (added after the design was shared)

**Tuesday (mail, 2026-11-27 00:39Z; saved at 2_Project_Files/fleet/briefs_staged/2026-11-27_in_003900.txt). Her figures are her own measurements at her boot today.**

Her three biggest boot costs, in her order, each matching a step-1 item:
1. The handover file (940 KB, a new block every checkpoint; read "whole" is impossible, so each successor re-derives where the live list ends). She names the one-block, tool-written handover as the single biggest win for her seat.
2. The grants file and the project index, read head-only in practice. She asks for a generated per-seat live view (her live grants, her client's index rows).
3. Rules card plus her ledger: 14% of context after those two, 21% after the bounded handover. She proposes a ledger row cap (headline plus one rule line, detail in the lesson).

Constraints she sets, all accepted into the build rules:
- The current worker launch path must keep working until the briefs already in flight have landed; cut-over at a boundary she names.
- Watchers whose exit wakes the seat must stay tracked background tasks, not detached processes.
- A shared brief template must not bypass the seat-local guards in the path and must resolve the seat name from the tree, never hardcode it.

**Friday:** no reply yet at the time of this addition.
