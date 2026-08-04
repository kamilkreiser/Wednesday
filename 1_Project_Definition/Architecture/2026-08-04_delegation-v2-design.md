# Delegation v2 — the two-layer cockpit (proposal for Kam)

Date: 2026-08-04 evening · Ticket: WED-50 (Urgent) · Status: PROPOSAL
Commission: Kam, after the 08-04 delegation day — "approach a little lacking;
get this right before more delegation." Research: iTerm2 · Claude Code Agent
Teams · Cole Medin video (youtube.com/watch?v=-1K_ZWDKpU0, studied via notes
+ docs) · Kam's screenshot layout. Standing constraint until approved: NO new
delegations.

**R0 (Kam, verbatim): "ensure no bleed between clients" — "datasec cannot
know about secuura."** Structural, not instructional. Every choice below is
tested against R0 first.

---

## The decisive research fact

**Agent Teams teammates inherit the team lead's process environment.** No
per-teammate `GH_CONFIG_DIR`/`AZURE_CONFIG_DIR`/env override exists (verified
against code.claude.com/docs/en/agent-teams.md, v2.1.178+ behaviour). One
team = one identity envelope. Therefore:

> **A team may exist WITHIN a client. A team may never SPAN clients.**

This isn't a limitation to work around — it's R0 enforced by construction,
which is exactly what Kam asked for. The launcher-per-client pattern (own
`gh`/`az` state) remains the only R0-safe cross-client runtime.

## The design: two layers + a cockpit

### Layer 1 — Fleet layer (cross-client): iTerm2 cockpit, launcher-isolated

One iTerm2 window = the whole fleet. Each PANE runs a client project's OWN
launcher (unchanged env isolation — R0 holds exactly as today). Wednesday
runs in her own pane, same window.

- **Kam's view (the ask):** everything visible at once, like the screenshot —
  no more scattered terminal windows. Click any pane to talk to that agent
  directly. iTerm2 badges name each pane (client/project); tab/pane titles
  carry live status.
- **Wednesday's insight (the other ask):** the monitor reads panes via the
  **tmux CLI** (`capture-pane`, `list-panes`, `list-sessions`) — no GUI
  dependency, works headless (the 06:00 scheduler can attach), portable
  (pure tmux, travels with the drive; nothing to pip-install). Alerts:
  no-output-for-N-min = stall; prompt-pattern = waiting on input; pane gone
  = death. The Tokenomics silent death (2h unnoticed) becomes a ~2-minute
  alert. iTerm2's Python API (`it2`) stays available as optional garnish
  (badges, native notifications) — not load-bearing. Reading panes is
  read-only observation; it feeds MY routing, never crosses client contexts
  (each pane is its own process).
- Mail Q&A (QUESTION/ANSWER, wraps, scoreboard) stays — it's the durable,
  mount-independent record. The cockpit adds the live layer on top.

### Layer 2 — Within-client: Agent Teams (where the parallelism lives)

Inside one client's session (launched by its launcher → that client's env),
the project agent can spawn an agent team for genuinely parallel
single-codebase work. Teammates inherit *that client's* identity — R0 holds.

- Enable per project, project-scoped (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
  in the project's launcher/settings — never user-global).
- Display: `tmux -CC` inside iTerm2 (docs-recommended) or native
  `--teammate-mode iterm2` (v2.1.186+) — teammate panes appear in the same
  cockpit window.
- What teams buy us: shared dependency-aware task list (file-locked
  claiming), peer-to-peer SendMessage, own 200K context per teammate,
  **quality-gate hooks** — `TaskCompleted` (exit 2 blocks completion) can
  RUN OUR VERIFIER: verifier-first delegation becomes machine-enforced,
  not brief-enforced.
- Where teams fit (per docs + Cole's video): implementation-parallel work —
  multi-module builds, competing-hypothesis debugging, N-lens reviews
  (his demo: 3 reviewers + cross-challenge + consensus). Subagents stay for
  research; single sessions for small tasks (our day-3 finding stands:
  one-shot territory needs no team).
- Cole's **contract-first spawning** pattern adopted into brief templates:
  identify the dependency chain, spawn upstream first, wait for its
  contract, then parallelize — matches our verifier-first culture.

### What Wednesday does in v2

Unchanged: briefs (verifier-first, pre-answered questions, §7 routing),
scoreboard, wraps, Kam-escalation classes. New: cockpit-composer (open the
window, arrange panes per active work), live monitor (tmux watcher — stall /
input-wait / death alerts), and teams appear in briefs as a RESOURCE the
project agent may use ("this is 3-way parallelizable; consider a team,
teammates on Sonnet, tasks pre-listed below").

## Costs and limits (from docs — honest numbers)

- Teams ≈ 3–7× tokens of a single session; scale with teammate count.
  Kam: money ≠ constraint, but teams only where parallelism is real.
  Default teammates to Sonnet; 3–5 max; 5–6 tasks each.
- Teams don't survive `/resume` (task list does) → bounded team runs only,
  which our close-before-full discipline already demands.
- Same-file conflicts are real → briefs assign file ownership per teammate.
- Experimental feature — expect breakage; keep the mail layer as fallback.
  Version-gated: iTerm2 mode + effort inheritance v2.1.186+, error
  notification v2.1.198+.

## R0 enforcement checklist (structural, per the rule)

1. Cross-client = separate launcher processes, always. No exceptions.
2. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled per-project only — a
   Wednesday-session team could only ever contain Wednesday-context
   teammates; she still never edits other projects (manage-don't-do).
3. Team/task state lives in `~/.claude/teams|tasks/{name}/` (machine-local,
   session-derived names): one client per session ⇒ one client per team
   state dir. PORTABILITY.md note: this state is machine-local and
   non-portable — acceptable (teams are bounded, in-flight only).
4. Cockpit monitor reads panes for STATUS routing only; pane content from
   client A never enters a brief, answer, or context destined for client B
   (existing single-client-working-set rule, delegation-monitoring skill).
5. Hard rule #4/#5 files (launchers) remain the identity source — untouched
   by v2.

## Rollout (supervised, go-slow)

1. **Kam signs off this design** (or amends).
2. **Cockpit v0:** tmux-based script on-drive (`2_Project_Files/fleet/cockpit/`) —
   opens the window, panes for Wednesday + active projects, badges. Manual
   trial with Kam watching. (PORTABILITY: tmux + iTerm2 are machine-local
   installs — checklist items; the cockpit/monitor scripts themselves are
   pure shell + tmux CLI and travel with the drive.)
3. **Monitor v0:** stall/input-wait/death alerts to Wednesday's pane +
   spoken tap for red flags. Success test: a deliberately-killed session is
   flagged < 5 min (the Tokenomics case, replayed).
4. **First team pilot, single client:** one Kam-chosen task inside ONE
   project (candidate: KS-560's 11 e2e residuals — parallelizable,
   verifier built-in). Their agent leads; Wednesday briefs; TaskCompleted
   hook runs the test suite. Metrics to scoreboard.
5. Review with Kam → adopt/adjust → delegation constraint lifts.

## Rejected on the way (reject-nine discipline)

- **One mega-team under Wednesday spanning clients** — fails R0 (shared env).
  Rejected regardless of observability gains. (The video's layout is
  single-codebase; ours is multi-client — the layout survives, the topology
  doesn't.)
- **Moving fleet comms into team mailboxes** — `~/.claude/teams/` is
  machine-local + cleaned on exit; mail is durable + mount-independent. Keep
  mail as the record, teams as the runtime.
- **"tmux OR iTerm2" as an either/or** — they're different layers that
  compose. Full evaluation (Kam asked, 2026-08-04):

  | | tmux (engine) | iTerm2 (glass) |
  |---|---|---|
  | Persistence | **Sessions survive terminal quit, GUI crash, even logout** — agents keep running detached; reattach any time (incl. the 06:00 scheduler) | None alone — close the app, sessions die |
  | Scriptability | **CLI: capture-pane / send-keys / list-sessions** — the whole monitor in portable shell, no dependencies | Python API (`it2`) — richer but pip-installed, GUI-bound, macOS-only |
  | Agent Teams support | The primary, most-tested mode; docs' suggested entrypoint is `tmux -CC` inside iTerm2 | Native mode newer (v2.1.186+), less battle-tested |
  | Portability | Linux too (future Mac Studio/server) — fits the portability rule | macOS-only |
  | Kam's UX | Ctrl+B navigation, clunky mouse/scroll | **Native panes, click-to-focus, scrollback, search, badges, notifications** |

  **Verdict: tmux is the load-bearing choice — but we don't have to give up
  the glass. `tmux -CC` inside iTerm2 renders tmux sessions as NATIVE
  iTerm2 panes:** persistence + scriptability underneath, click-and-scroll
  on top. If ever forced to one: tmux (survivability and scripting beat
  UX). iTerm2 alone is the only rejected configuration.
- **Building WED-46 dashboard first** — the cockpit IS the short-term
  dashboard; the web dashboard stays queued behind it.
