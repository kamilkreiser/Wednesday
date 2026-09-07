---
date: 2026-09-07
type: correction
source: reconstructing the QA-gate launch after six gates had used it and nothing on disk said where it lived
status: live
tier: W
---

# A handover records a mechanism by its PATH, never by the id of the thing it produced — and tooling that lives in a gitignored directory is invisible to every search a successor knows how to run

**The operative case, so the headline matches it:** Wednesday is writing a handover, a note or a
brief and is about to name something it used — a QA gate, a watcher, a probe, a launch. **The
sentence is about to say `%135`, or a pid, or a port, or "the wrapper".** Stop. **Write the PATH of
the file that produced it.** A pane id is dead the moment the pane is; a pid is dead sooner. The
successor inherits a name for a thing it cannot reach, and the cost is not confusion — it is that the
successor's next best option is to *invent* the mechanism, which is how a guard gets bypassed by the
person it was built to protect.

## The case

Six tier-1 QA gates ran on 2026-09-07. The handover named two of them — **`%135` and `%136`** — and
never named the command. The successor seat looked, in order, at `launchers.conf` (no QA entry),
`inbox_routing.conf` (none), the Testing Agent project itself (no `Launch_*.command`), its own
`CLAUDE.md` (behaviour, not launch), `cockpit/logs` and `cockpit/state` (nothing), and the shared bus
(no outbound gate brief — **the QA agent is briefed by pane, not by mail**, which is itself a fact no
artefact stated). **~25 minutes.**

**The wrapper existed the whole time**, at `2_Project_Files/fleet/state/launch_qa_<topic>.sh` — one
per gate, prompt in its own file, a `--check` mode, and guards that refuse a prompt not beginning
with the thinking directive or not naming the brief path.

**It was found by grepping for the ENFORCEMENT TEXT, not for the thing's name** — the boot digest's
own sentence, *"a blind agent should be unlaunchable, not merely detectable"*
([[2026-08-06_artifact-presence-is-not-execution]] rule 2), is what proved a wrapper had to exist and
made the search worth continuing past the fourth dead end.

## The real cause, and the commit is what found it

`git add` refused the new wrapper: *"The following paths are ignored by one of your .gitignore
files."* **`2_Project_Files/fleet/state/` is gitignored.**

So **every QA launch wrapper this fleet has ever used is invisible to any git-based search, absent
from the repository, and does not travel with a clone.** A seat booting on the laptop, or from a
fresh clone, would find nothing — and the `state/` directory is *correctly* ignored, because it holds
runtime state: baselines, hashes, seen-markers. **The wrappers are TOOLING that was put in the
state drawer.**

## Why this is its own lesson and not another handover-quality row

The near-miss is the part worth keeping, and it is not "I lost 25 minutes". **The available
shortcut was to construct a `cockpit.sh add "claude …"` that looked entirely plausible** — the
cockpit's own usage invites it, and it would have worked. **It would also have bypassed the
blind-agent guard**, which exists precisely so an agent cannot be launched without its brief. The
guard would not have failed; it would have been *routed around*, by the coordinator, in good faith,
because the coordinator could not find it.

**So an undiscoverable enforcement is a defeated enforcement**, and this is the discoverability half
of [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] — that file says a safeguard needs something
to arm it and something to check it is armed. It needs a third thing: **something that tells the next
person it exists.**

## How to apply

1. **Any mechanism a seat invokes goes into the handover as its PATH.** Not a pane id, not a pid, not
   a port, not a prose noun ("the wrapper"). `fleet/state/launch_qa_<topic>.sh --check` is a handover
   line; `%135` is not. Runtime identifiers may appear *beside* the path, never instead of it.
2. **Before writing a tool anywhere, ask whether the directory is tracked** — and whether it is
   tracked *for the right reason*. `git check-ignore -v <path>` answers it in one command. This is
   [[2026-08-04_gitignore-artifacts-at-creation]] pointed the other way: that lesson stops artefacts
   being committed; this one stops **tooling being hidden**.
3. **State drawers hold state.** Baselines, hashes, seen-markers, scratch — ignored, correctly.
   Executables that a future seat must find are tooling and belong in a tracked path. **The fix when
   they are in the wrong place is a MOVE, not a gitignore change** ([[2026-08-26_never-delete-cleanup-means-quarantine]]),
   and it is not done while something is live on the mechanism.
4. **When a mechanism cannot be found, do not compose one.** The honest options are: keep reading the
   source, or say plainly that it is unrecorded. **A launch command that looks right is exactly what a
   generator produces best** ([[2026-08-06_ghost-suggestions-in-panes]]) — and here the invented one
   would have been *functional*, which is worse than one that fails.
5. **Test by its handle:** could a seat that booted on another machine, from a fresh clone, run this
   mechanism from what the handover says? If not, the handover names a ghost.

## Residual, stated rather than carried quietly

The wrappers are **still in `fleet/state/`**. The move to a tracked path was deliberately NOT done in
the session that found this, because a gate was live on `%151` and re-homing the mechanism it was
launched from, mid-pass, is the wrong moment. **Queued for the next quiet point** — and this
paragraph is the thing that expires: if a later reader finds the wrappers still there, the queue
failed, which is [[2026-08-07_a-promise-is-not-a-mechanism]].

**Family:** [[2026-08-06_artifact-presence-is-not-execution]] (its rule 2 is what proved the wrapper
existed) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the discoverability half) ·
[[2026-08-04_gitignore-artifacts-at-creation]] (fate at creation — now including *visibility*) ·
[[2026-08-03_mental-model-not-source-of-truth]] (kept reading the source rather than composing a
command) · [[2026-08-04_validate-brief-pointers]] (a pointer to a pane id points at nothing tomorrow) ·
[[2026-09-05_root-folder-holds-only-rules-and-launchers]] (the sibling: every file has a right folder).
