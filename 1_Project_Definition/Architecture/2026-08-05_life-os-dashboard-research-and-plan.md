# Life-OS Day Dashboard — research + architecture plan

**Date:** 2026-08-05 (laptop session, KK_DEV_Local)
**Commission:** Kam, verbatim in `Discovery/00_prompt-log.md` (2026-08-05 entry).
**Status:** APPROVED — Kam, 2026-08-05 in-session: "yes, go ahead with phase 0 tonight. document and plan now." Tickets: WED-58 (epic, In Progress) · WED-59 Phase 0 (tonight) · WED-60..63 Phases 1-4 · WED-64 Kam input queue · WED-65 later-today sitting.

---

## 1 · The commission, distilled

1. Extend Wednesday beyond coding to **all of Kam's life and companies** — *in addition to* the existing coding/fleet system, never instead of. Kam chooses the interaction mode per moment → **the two systems must be interoperable**.
2. Study Eric Michaud's "Build an Obsidian SYSTEM Not a Second Brain!" (youtube OZ3ZNhrPbF4) — **visuals, not just transcript**.
3. Find the code from his resource repository (Skool / easymachineai).
4. Deliverable: an **Obsidian dashboard or a web page** — whichever is optimal for Kam AND Wednesday. Local-first, **remotely available**, secure.
5. Wednesday **controls, adds to, and manages** the dashboard — and through it, Kam's day-to-day.
6. Overnight work is welcome: things ready by 06:00. Mac Studio will be dedicated (always-on, local + remote login).
7. Access: **API-first**, own phone, etc.; raw credentials only as last resort.

## 2 · Video findings (visual pass, 15 frames + zooms)

Chapters: The Vault as a Workspace → Daily Focus Dashboard → Metrics and Insights → Daily Agent Commands → Systems vs. Workflows → Eliminating Friction → The Intelligence Layer → Vault Access.

**The one-window "Command Center" layout** (Obsidian workspace): left file tree · center dashboard · right column stacked: Telegram web + terminal panes (agent) + month calendar · bottom-left graph view. Everything happens inside one app — browser tabs (YouTube Studio etc.) open in Obsidian's web viewer. "Eliminating friction" = never leave the workspace.

**Daily Focus Dashboard components** (center pane):
- Header: date · big title · status strip (`12:49 PM · Now: <current block> · 0 done · 7 open · 0 inbox`)
- **CURRENT FOCUS** card — the one thing right now, with context chips (7 open tasks · 6 scheduled) and actions (Open Today · Context Pack · Log Time)
- **Today's Priorities** — 3 ranked items with complete/promote/note controls
- **Today's Schedule** — time-blocked list with category labels and NOW/NEXT badges
- **Metrics** — tabs Overview / Audience / Business / Personal / Ops; KPI cards with deltas + sparklines
- **Daily Drivers** — recurring checklist with completion % bar
- **Quick Capture** — inline box straight to inbox
- Recent Activity feed

**Metrics views:** per-tab dashboards (consistency line chart, streaks, done/open counts, work-time) — **all data sourced from daily notes' YAML properties**; drill-down to a per-date table with source links.

**Daily template properties** (his tracked fields): business (youtube_subs, skool_members, revenue…), personal (weight, sleep_score, energy_score, focus_quality, mood_score), **family (family_connection, wife_score, daughter_score, boy_1_score, boy_2_score, time_loved_ones)**. Directly relevant: Kam wants a family section too.

**Agent layer:** `pi` coding agent (open source: github.com/badlogic/pi-mono) in the terminal panes; `AGENTS.md` context; skills (brainstorming, systematic-debugging, verification…); slash prompts. `/today` builds the day plan from vault + calendar + inbox + carry-overs; `/closeday` closes it. His thesis: without the intelligence layer a vault "turns into a graveyard" — the agent is what keeps the system alive. **This is precisely the Wednesday role — we already have the intelligence layer; he built one to get there.**

## 3 · Code findings

**Skool:** Kam's account is on the free Standard plan. The full "Obsidian Life OS" (incl. the custom dashboard plugin `emai-command-center` seen in the video) is Premium **$57/mo**. The free packs live behind an email gate at easymachineai.com/links.

**Downloaded** (Kam-approved, alias `kreiser.org+emai@me.com`, → `Research/emai/`):
- `emai-starter-vault` — sanitized vault: `00 Human/` (Inbox, Daily Notes, Tasks, Projects, Resources, People, Areas, Context incl. Calendar Events, Templates, Content) · `Machine/` (Workflows, Templates, Personalization, Outputs) · `System/` docs. **Claude-Code-native**: ships `.claude/commands/` (start, interview, today, new, closeday, meeting-notes) + `CLAUDE.md`/`AGENTS.md`. Personalization model: `/interview` compiles preference files into single compiled prompts (`today-prompt.md`, `closeday-prompt.md`) so daily workflows read ONE file. Plugins: dataview, tasks, templater, kanban, full-calendar, calendar-bases, obsidian-git, excalidraw, terminal, clipper…
- `five-skills-pack` — content/marketing skills (mostly his niche; the `skill-creator` meta-skill is the useful one).
- `pi-harness-pack` — architecture notes for his pi+OpenRouter setup (reference only; we're Claude-native).

**`emai-command-center` is intentionally excluded from the free edition** — the pretty dashboard UI is the premium artifact.

**Premium verdict: NOT needed.** His plugin renders a single-operator content-business dashboard; Kam's spec (3 calendars across 2 tenants + personal, per-company work sections with R0 isolation culture, family/school, bills, news, remote access) is beyond its scope — we would rewrite nearly all of it. The free vault gives us the conventions; the video gives us the design language; our own build gives us the requirements. Revisit only if we later want his plugin as a UI base (unlikely).

## 4 · Architecture recommendation

**Hybrid: markdown data layer + Wednesday-generated web dashboard. The vault is the database; the web page is the view; Wednesday is the intelligence layer that writes both.**

- **Data layer** — extend `0_Brain/` with a `dashboard/` data area (or sibling `6_Dashboard/` — decide at build): one markdown/YAML file per feed (calendar snapshots, per-company worklists, flags, family dates, bills, news digest), plus the existing brain files (tasks, projects_index, decision_queue) which are already half of the spec. Everything plain files → git-versioned, portable, syncs with the existing drive flow.
- **View layer** — a static-generated local web dashboard (self-contained HTML/JS, no external CDNs) served on the Mac Studio. Wednesday regenerates it on every data change / on schedule. Drill-down = linked sub-pages per area. Mobile-friendly.
- **Obsidian stays fully usable** on the same files (0_Brain is already an Obsidian vault) — Kam can open the vault directly whenever he prefers that mode. Interoperability requirement satisfied structurally: **files are the API**; both views read the same truth; there is nothing to keep in sync.
- **Why not Obsidian-only:** remote access would depend on Obsidian Sync + mobile app rendering of plugin dashboards (weak on mobile); web gives us full control of the day-view UX and works in any browser. Why not web-only: Kam already lives partly in Obsidian patterns, and markdown editing (his and mine) is the cheapest write path.

**Remote access + security:** dashboard binds to localhost/LAN only; remote via **Tailscale** (WireGuard mesh, zero public exposure, free tier, MagicDNS URL like `https://studio.tailnet/dashboard`) — no ports opened, no public web server. Secrets stay in `4_Credentials/.env`. Fallback option: Cloudflare Tunnel + Access if Tailscale doesn't suit. Decision point for Kam at build time.

**R0 note:** the dashboard is Kam's own aggregated view — he sees everything. R0 (no client bleed) still governs the *pipes*: per-client data is fetched with that client's credentials, stored in clearly separated files, and never flows into another client's briefs or sessions.

## 5 · Dashboard information architecture (v1 target)

Mapped to Kam's spec:
1. **Top strip** — date/time, "now/next" from calendars, today's flag count.
2. **Calendars** — merged day/week view of: personal iCal (macOS Calendar/CalDAV), Datasec Microsoft 365 (Graph API), Secuura Google (Calendar API). Color-coded by world.
3. **Today's flags** — tickets due/overdue (Linear WED + read-only client boards — access already granted 2026-08-03), meetings, outstanding tasks, upcoming bills, key dates. Wednesday curates this list each morning.
4. **Work life** — one section per company (Datasec, Secuura, Side) → per project: state line, follow-ups, waiting-on, emails needing attention. Sources: projects_index entries, wrap mails, boards digest — all already flowing.
5. **Coding projects** — fleet view: scoreboard, active sessions, decision queue.
6. **Family** — kids' key dates: exams, homework due, school events. Sources phase-wise: manual/dictated entries first; school WhatsApp + portal later (needs Kam decisions on access).
7. **Personal** — ideas, personal projects, errands (e.g. ALDI SIM).
8. **News** — daily digest: war/geopolitics, tech, quantum, security, biotech+medicine. Wednesday-curated with links; no doomscroll surface.
9. **Drill-down** — every section links to a detail page (and to the underlying markdown in the vault).

## 6 · Phasing (proposed)

- **Phase 0 — skeleton + first light (overnight-able now):** data-layer layout, generator, v1 dashboard from data I already hold (Linear, fleet state, decision queue, daily note, manual calendar stub). Serves locally on the laptop/Studio.
- **Phase 1 — calendars:** iCal read; MS Graph app registration (Datasec tenant — needs Kam once); Google Calendar API (Secuura — needs Kam once). Read-only scopes.
- **Phase 2 — work sections + drill-down + news digest.** Mail surfacing (Agent Mail + which of Kam's mailboxes, API/OAuth — needs Kam decision).
- **Phase 3 — family + bills.** Inputs needed from Kam (see §7). School portal/WhatsApp integration design (dedicated number / WhatsApp Business API is the likely clean path — ties into WED-51).
- **Phase 4 — polish: remote access hardening, phone-first layout, Wednesday's own management loops (morning generation, flag curation, retro-driven layout evolution).**

Overnight expectation: fine — precedent exists (08-04 overnight envelope). On the Studio, scheduled overnight runs still need the **WED-16 TCC grant** (1-minute GUI action, machine-local); until then overnight work happens inside live sessions like tonight's.

## 7 · Inputs needed from Kam (queued, one at a time)

1. Calendar API access: MS 365 app registration (Datasec) + Google Cloud OAuth (Secuura) — 5-10 min each, one-time, at his keyboard.
2. Which mailboxes are in scope for the email sections, and via what (Graph/Gmail API preferred).
3. Bills: where do they live today (mailbox? folder? bank exports?).
4. Kids' school: names of portals, whether a dedicated WhatsApp number for Wednesday should join the school groups (WED-51 tie-in).
5. News: preferred sources/level of depth per topic.
6. Tailscale (or alternative) for remote access — his call before anything is reachable off-LAN.

## 8 · Access log (transparency)

- Entered `kreiser.org+emai@me.com` into the easymachineai.com free-resource gate (Kam-approved in-session) — expects marketing mail to the +emai alias; sender is Beehiiv.
- Downloaded 3 free packs (12 MB + 7 KB + 6 KB) → `1_Project_Definition/Research/emai/` (archives gitignored).
- No Skool purchase; no premium content accessed; nothing entered anywhere else.
