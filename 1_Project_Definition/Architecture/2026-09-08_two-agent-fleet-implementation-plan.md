---
date: 2026-09-08
type: architecture / implementation plan
source: Kam, dashboard chat 11:50 — "architect and come up with a plan to make this happen"
status: PROPOSAL. Nothing built. Four decisions needed from Kam (§7).
---

# Two agents, one panel — implementation plan

**Kam's design, restated so it can be checked:**
- **Main agent** = this Wednesday, on the Studio. **All projects EXCEPT Datasec.**
- **Datasec agent** = a second Wednesday on a headless Mac, on the **Datasec Claude account**.
  **All Datasec projects, defined as living inside the Datasec folder.**
- **A strong gate** between the two.
- **One website**, served from the Studio, with a **top-right toggle: Main | Datasec**.
  Each agent posts its conversation into its own view and its fleet activity under its own flag.
  Datasec activity must not appear on Main, and vice versa.
- The headless machine is built from a **Time Machine restore of the Studio**.
- 🔴 **Hard constraint: both agents must still run from a SINGLE DRIVE when travelling.
  Nothing here may damage that.**

---

## 1. What already exists — measured, so we build the delta and not the whole thing

**This is most of it. The plan is smaller than it looks.**

| Piece | State | Evidence |
|---|---|---|
| **Dashboard reachable off-machine** | **ALREADY BUILT AND RUNNING** | Tailscale serving `→127.0.0.1:47787` on tailnet `tail99c01e.ts.net`, added 2026-08-20. The Studio is `mac-studio`. |
| **New-Mac bring-up** | **ALREADY WRITTEN AND EXERCISED END TO END** | PORTABILITY.md "New-Mac bring-up", 10 steps, run for real on 2026-09-02 when the laptop died. |
| **`agent`/`project` flag on chat entries** | **PARTLY THERE** | `seat` + `project` fields already on entries written by `chat_reply.sh` — 91 of the last 400. Kam's own messages carry neither. |
| **One-writer-per-file pattern** | **PROVEN TODAY** | `0_Brain/fleet/claims/claims_studio.md` — never conflicted once. The two SHARED files corrupted twice in one morning. |
| **Path enforcement in the tool path** | **EXISTS, extendable** | `pretooluse_no_cd.sh` already refuses git write verbs outside WEDNESDAY. |
| **Marker guard before commit** | **EXISTS, machine-local, UNTRACKED** | `.git/hooks/pre-commit`. 🔴 **A Time Machine restore carries it; a fresh clone does not.** |
| **Two seats already running** | **LIVE SINCE 09-07** | Studio=Secuura, laptop=Datasec, per Kam's 11:01 split. |

**Correction to what Wednesday told Kam at 11:45:** the private-mesh access was described as
"an evening's work". **It was built on 2026-08-20 and is running.** The recommendation stands;
the cost estimate was wrong and it was wrong in the direction that made it sound harder.

---

## 2. Phase 0 — the data model. Everything else depends on it.

**The single change that makes the toggle possible AND removes the corruption class:
one writer per file, merged at render.**

    NOW                                  PROPOSED
    chat_log.json      (2 writers) ->    chat_main.json      (main writes only)
                                         chat_datasec.json   (datasec writes only)
                                         chat_kam.json       (the panel writes only)
    fleet activity     (shared)    ->    fleet_main.json / fleet_datasec.json

- **Every entry carries `agent: main | datasec`, DERIVED from the seat, never typed.**
  The `seat` field already exists; `agent` is a lookup from it, so it cannot be got wrong by hand.
- **Kam's own messages need a flag too** — currently they carry none. The panel stamps the
  message with **whichever view was active when he sent it**. That is what makes "when I am on
  the Datasec view, the Datasec agent will paste the conversation into that view" work in both
  directions: his side is addressed to a view, not broadcast to both.
- **Merge happens in the browser at render.** Two files in, one timeline out, filtered by the toggle.
- **Why this matters beyond the feature:** two seats writing one JSON file is what corrupted
  `chat_log.json` and `decisions.json` today. One writer per file makes that **impossible by
  construction**, not merely unlikely. It is the claims-file design, which is the only thing in
  this system that has never conflicted.

**`decisions.json` is the exception and stays shared** — it is Kam's ruling queue and he must see
one queue, not two. It keeps today's `store_guard` (refuses a stale or marker-bearing store) and
gains a `agent` field per card for the toggle's filtering.

---

## 3. Phase 1 — the toggle

- Top-right control: **`MAIN | DATASEC`**. Persisted per browser (`localStorage`), default MAIN.
- Filters **chat AND fleet activity AND the tickets/board tiles** on `agent`.
- **A visible, unmissable indicator of which view is live** — a coloured header band, because the
  cost of Kam typing a Datasec instruction while looking at the Main view is a
  cross-client message, and that is his severity-max class. The toggle must never be a subtle chip.
- **Nothing is deleted by filtering** — the other agent's stream is present and one click away.

---

## 4. Phase 2 — the strong gate. What is structural and what is not.

Kam asked for a **strong** gate. Here is what each layer actually buys, honestly:

**Structural (cannot be violated, not merely forbidden):**
1. **Two machines, two Claude accounts** — his design. Different auth, different sessions.
2. **One writer per data file** (Phase 0) — neither agent can write the other's stream.
3. **Path guard in the tool path** — extend `pretooluse_no_cd.sh`: the Datasec agent refuses any
   WRITE whose path is outside `!CODING/Datasec/` (plus its own WEDNESDAY tree); the Main agent
   refuses any write INSIDE `!CODING/Datasec/`. **Kam's folder definition is what makes this
   checkable** — it is a path test, not a judgement.
4. **Per-project `gh`/`az` config dirs** — already in every launcher.
5. **Per-agent mail inbox**, or a tag filter enforced in the poller (the 2026-08-13 rule).

**NOT structural — discipline only, and it should be named as such:**
6. **What each agent READS.** A path guard stops writes. Nothing stops a `cat`. Reading is where
   the isolation is a rule, and rules lose to reflexes — today's own record shows that repeatedly.

### 🔴 The finding Kam most needs from this section
**On two machines the gate is partly physical. On ONE DRIVE while travelling it is not.**

When both agents run from a single drive, both clients' folders are mounted for both agents.
The physical layer disappears and only the hook remains. **So the travel mode is the weaker
mode, and it is the mode he uses when he is least able to supervise.**

That is not an argument against travelling. It is an argument for the hook being real
enforcement rather than a comment, and for the travel configuration being **tested deliberately**
rather than discovered at an airport.

---

## 5. Phase 3 — the headless Datasec machine

**Good news: the run-sheet exists and has been executed for real** (PORTABILITY.md, "New-Mac
bring-up", 2026-09-02). A Time Machine restore of the Studio carries far more than that fresh-Mac
path had to install.

**What a Time Machine restore does NOT carry, and each is a real gap:**
1. **The Claude account.** This machine logs into the **Datasec** account — a deliberate change,
   done by Kam, not inherited.
2. **🔴 `.git/hooks/pre-commit` — UNTRACKED BY DESIGN.** It is the guard that refuses staged
   conflict markers. A restore carries it *if* the restore includes `.git`; a fresh clone does not.
   **If the headless machine lacks it, it will push conflict markers exactly as happened twice
   today.** Verify it exists and exercise BOTH refusals before the machine does any work.
3. **GUI-only, per machine:** Matilda Premium voice · the scheduler's Full Disk Access grant ·
   Calendar TCC · Docker's first-launch approvals · **Tailscale's two approvals and tailnet login**.
4. **Keychain / ssh-agent state**, and `gh auth login` / `az login` under the Datasec identity.
5. **Headless specifics not yet on the checklist:** it must not sleep (`caffeinate`, or Energy
   Saver), it needs Screen Sharing enabled so Kam can attach a monitor-equivalent remotely, and
   **Tailscale's GUI variant starts at LOGIN, not boot** — a known limit already recorded, and on
   a headless box it means auto-login must be on or the machine is unreachable after a reboot.

**Deliverable: a `PORTABILITY.md` section "Headless second agent — bring-up", written from the
above and then EXERCISED on the machine before it is trusted**, plus a `doctor.sh` check that
fails when the pre-commit hook is missing.

---

## 6. Phase 4 — naming

**Recommendation: keep ONE persona, give the SEATS names.**
`Wednesday (Main)` and `Wednesday (Datasec)` — the same Wednesday, two seats.

**Why not two different names:** the identity, the voice protocol, the lessons and the working
relationship are one thing, built over five weeks. Splitting the name splits the relationship and
implies two personalities where there is one person at two desks. The chat already stamps `seat`,
so Kam can always see which is speaking.

**What DOES split, and already has:** the correction ledgers (Kam ruled this on 2026-09-08 09:57
— each seat reads its own scope), the daily notes, the pickups, and the claims files.

### The brain question, which is a real decision and is Kam's
The lessons are **three-tier** (2026-09-05): **W** = Wednesday's own method, **M** = fleet method,
client-neutral, **P** = a project's cases, which live with that project.

**Recommended: both seats share W and M; P never enters either seat's brain.** That keeps one
Wednesday who learns once. **The honest cost: some W-tier lessons carry a Secuura example in
their prose**, so a Datasec seat reading them sees Secuura's name. If Kam wants zero cross-client
text anywhere, the alternative is to strip W-tier prose to client-neutral form — which is real
work and loses the specificity that makes the lessons fire.

---

## 7. The four decisions, all with safe defaults

1. **Mesh or hosted?** — **Mesh, and it already exists.** Default: use what is running.
2. **Shared W/M brain, or fully separate brains?** — Default: **shared W/M**, P stays with the
   project. The cost is named above.
3. **Naming** — Default: **one persona, two seat labels.**
4. **Does the path guard REFUSE, or WARN, on the travel drive?** — Default: **refuse**, same as
   on two machines. A gate that softens when supervision is lowest is the wrong way round.

**If Kam says nothing, nothing is built.**

---

## 8. Order of work, and what is genuinely small

    Phase 0  data model, one writer per file          ~half a day   ALSO fixes today's corruption class
    Phase 1  the toggle + filtering                   ~half a day   depends on Phase 0
    Phase 2  path guard in the hook                   ~2 hours      exercised both directions before arming
    Phase 3  headless bring-up + PORTABILITY section  ~an evening   mostly EXECUTING an existing run-sheet
    Phase 4  naming + brain split                     ~1 hour       mostly a decision, not a build

**Phase 0 is worth doing even if Kam changes his mind about everything else** — it removes the
failure that cost two file repairs this morning.

**Travel test, and it is not optional:** before this is called done, unmount everything, run BOTH
seats from the single drive on ONE machine, and verify that (a) the toggle still separates them,
(b) the path guard still refuses, (c) neither corrupts the other's stream. **The travel mode is
the weaker mode; it gets tested, not assumed.**
