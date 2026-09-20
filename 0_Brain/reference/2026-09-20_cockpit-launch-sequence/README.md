---
date: 2026-09-20
type: reference
source: Kam, panel/pane 2026-09-20 ~21:30 — "please look into the launch sequence for cockpit, in the Wednesday folder"
status: live
---

# The cockpit launch sequence — what it does, and four defects

**FOUND / TESTED / HOW** per Kam's 2026-09-07 rule. Everything below was read or run
at 21:3x–21:4x on 2026-09-20 from this drive; nothing is recited from memory.

## The sequence, in order

1. **`Launch_Cockpit.command`** (double-click). Preflight, in this order:
   self-heal exec bits on `cockpit.sh`, `monitor.sh`, `Launch_Wednesday.command` ·
   cockpit.sh + cockpit.conf present · `claude` CLI on PATH · brew (soft) ·
   **tmux (hard fail)** · iTerm2 (soft, falls back to plain tmux).
   Failures `pause_exit` so they are read rather than lost with the window.
2. **Resume / Fresh / Quit** prompt, only if a `fleet` session already exists.
   Reads a full line (not `read -n 1`) — that was fixed after Kam hit
   "clicked fresh but it resumed" on 2026-08-06.
3. **`cockpit.sh up`** → reads `cockpit.conf` (`name|cmd` per line):
   - line 1 `wednesday|bash "${PROJECT_DIR}/Launch_Wednesday.command"` becomes
     **pane 0, created directly by `tmux new-session`**
   - line 2 `fleet-monitor|.../monitor.sh --interval 60 --stall-min 10` goes
     through `add_pane`
   - `apply_layout` (wednesday left column 45%, agents/monitor right)
4. **Attach**: iTerm2 `tmux -CC attach -t fleet`, else `exec tmux attach`.

`add_pane` (the guarded path) does: skip if `@cockpit_name` exists → **usage gate**
(rc 3 at/over the 90% cut; stale tolerated during `up` only) → **wait up to 90 s for
`.git/rebase-merge` / `rebase-apply` / `MERGE_HEAD` to clear, else refuse rc 7** →
`split-window` → set `@cockpit_name` → layout.

`cockpit.sh launch <Client/Project>` resolves `launchers.conf`, has a travel-drive
volume fallback (fixed 2026-09-09 by Tuesday — it had been keyed on the literal
`WEDNESDAY` and so never matched her tree), then calls `add_pane`.

## D1 — pane 0 is created OUTSIDE `add_pane`, so the coordinator seat bypasses BOTH gates

**FOUND.** In the `up` branch, the first `cockpit.conf` entry is started with
`tmux new-session` directly; `add_pane` is only called for entries 2..n. So the
**Wednesday seat itself** — the pane that matters most — is launched with no usage
gate and, more importantly, **no rebase/merge gate**.

**Why the rebase half is the serious one.** That gate's own comment says it exists
because "a launcher that reads tracked files must not start into a moving tree":
on 2026-09-14 a gate launcher read its brief one second after a commit let
panel_sync's rebase fire, the tree was rewritten under it, and the pane sat as a
bare shell for 45 minutes. **`Launch_Wednesday.command` is the heaviest reader of
tracked files in the whole system** — at this boot it read ~660 KB (boot digest,
ledger, pickup, expiring grants, week instruction, daily notes). And
`panel_sync.sh loop` is running right now (pid 1775) doing exactly that rebase.

**TESTED.** Read, not inferred: `cockpit.sh` `up` branch vs `add_pane`;
`cockpit.conf` line order; `pgrep -fl panel_sync` → pid 1775 live.
The usage-gate half was already measured and recorded on 2026-09-17
(the ledger row about `up` creating pane 0 ungated); **the rebase-gate half
appears not to have been named before.**

**NOT TESTED:** I did not force a rebase mid-launch to reproduce it. The claim is
that the gate is absent on that path, which is a property of the code, not a
prediction about frequency.

## D2 — `doctor.sh`'s root-folder check reports CLEAN while two strays sit in the root

**FOUND.** `doctor.sh` prints `✓ root folder: only rules, portability and launchers`
**right now**, and the root actually holds:

- `Launch_Wednesday (conflict_on_2026-09-18).command` — a unison conflict copy of
  the launcher. 46,296 B, 16 Sep 14:33, **not executable**, **106 diff lines behind**
  the live `Launch_Wednesday.command` (50,766 B, 19 Sep 09:06).
- `logs/` — a stray directory (`combined.log`, `error.log`, 17 Sep 23:03).

**Two independent holes in one guard**, both in its exclusion set (`doctor.sh:806`
and the loop above it):
1. the allow-list pattern `Launch_*.command` **matches the conflict copy** — this is
   the 2026-09-10 "a sync conflict copy is an input to every glob" lesson pointed at
   a guard's ALLOW-LIST rather than at a reader's glob;
2. `[ -f "$f" ] || continue` **skips directories entirely**, so `logs/` is invisible
   to a check whose whole job is stray root entries.

**HOW.** Ran `doctor.sh` and grepped its root verdict while both strays were on disk
(the positive control is that they are demonstrably there: `ls -la` output above).
A check that returns ✓ with its subject present is the `a-check-that-cannot-fail`
shape.

**Blast radius, stated narrowly:** nothing EXECUTES the conflict copy. Both consumers
name the launcher literally — `Launch_Cockpit.command:34` and
`wednesday_rotate.sh:59` — and the copy has no exec bit. The cost is a stale
duplicate of the boot prompt sitting unflagged in the root, where a human (or a
future seat looking for "the launcher") can pick the wrong one.

## D3 — 17 conflict copies of launch-path mechanisms

`find 2_Project_Files -name '*conflict_on*' \( -name '*.sh' -o -name '*.command' \)`
returns **17**, including `doctor.sh`, `usage_gate.sh`, `monitor.sh`,
`wednesday_rotate.sh`, `arm_wake_watch.sh`, `safe_push.sh`, `note_entry.sh`,
`speak.sh`, `session_start_compact.sh`, `install_all_jobs.sh`, `close_wednesday.sh`.
Same class as D2: none is invoked by name today, but every one is a stale copy of a
mechanism, and the guards that would notice glob by extension.

**Do not delete them** (2026-08-26). Quarantine is a MOVE into a sync-ignored
directory, never a rename in place (2026-09-09).

## D4 — already on record, restated so the set is complete

- `add_pane` returns **0** on "pane already present — skip", and
  `brief_and_launch.sh` prints `launched:` after it — a false receipt (ledger 09-19).
- `cockpit.sh say --mail` refuses **rc 1 with no output** when the pane name is
  absent from `inbox_routing.conf` (ledger 09-20, second cause for the same silence).
- The **Fresh** branch offers to kill live agent panes to restart a coordinator whose
  pane has merely exited — it cost two Datasec agents on 2026-09-17.

## What I recommend, in order

1. **D1:** route pane 0 through the same two gates — simplest correct shape is for
   `up` to create the session with a placeholder and call `add_pane` for every
   entry, or to hoist the rebase-wait above the `new-session`. Needs arms: a
   planted `.git/rebase-merge` must refuse the seat launch, and a clean tree must
   still launch it.
2. **D2:** tighten the allow-list to the exact launcher names (or exclude
   `*conflict_on*` explicitly) and stop skipping directories. Arms: the current root
   must WARN on both strays, and a clean root must stay ✓.
3. **D3/D2 strays:** move the conflict copies into a dated quarantine directory the
   sync engine ignores — a move, verified at every replica, never a rename.
