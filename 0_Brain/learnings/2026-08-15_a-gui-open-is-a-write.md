---
date: 2026-08-15
type: correction
source: "Self-caught via the HPSM agent's report: it noted 'the deck is frozen with PowerPoint holding it open right now (pid 6147)' as a constraint on ITS work. That process was mine, opened for Kam an hour earlier, and it had left a ~$ lock file inside the Datasec/HPSM project tree."
status: live
supersedes: ""
---

# Opening a file in a GUI application is a WRITE into the folder that holds it

**The operative case, so the headline matches it:** I am about to open a document belonging to
another project — a deck, a spreadsheet, a PDF — in a desktop application, and I have
classified the action as *reading*. **It is not.** A GUI open takes a lock, writes a sidecar
file next to the original, may autosave, and **leaves the file held until the application is
quit.**

**What happened.** Kam asked me to open the HPSM Monday deck and show him. I did, correctly —
it was the decisive test and it closed a two-day-old question. **What I did not consider is
that `open -a "Microsoft PowerPoint"` writes.** It created
`~$2026-08-13_HPSM-MVP_client-presentation_v1.pptx` in `Datasec/HPSM`'s tree and held the deck
open for an hour. **Hard rule 1 says my writes stay under my own folder.** This was a write
into a client project, caused by me, that I had reasoned about as a read.

**How it surfaced, which is the part worth keeping:** not by me noticing. The HPSM agent
mentioned it **as a constraint on its own work** — *"the deck is frozen with PowerPoint holding
it open right now (pid 6147)"* — and was factoring my stray process into its decision about
whether it could edit the file. **It read my mess as a property of the world.** An agent
working around my side effect is the same failure shape as an agent working around a stale
brief: it does not complain, it adapts, and the adaptation hides the cause.

**No harm done, verified rather than assumed:** file byte-identical before and after
(189,668 B, mtime unchanged, sha256 `a8ee84a7…`), PowerPoint reporting no unsaved changes,
lock file gone after quit, their repo clean.

**How to apply:**
1. **Before opening anything outside my own folder in a GUI app, ask what the open WRITES.**
   Office apps write `~$` lock files; many editors write swap/backup files; some autosave.
2. **Quit the application when the task is done — in the same action, not "later".** A held
   file is a live constraint on whoever owns it, and they will discover it before I do.
3. **Prefer a read-only path when one exists** — parse the package, render a copy into MY
   scratchpad, convert to PDF elsewhere. I did exactly that with LibreOffice into my own
   scratchpad in the same hour, which is the pattern; the PowerPoint open was necessary
   *because PowerPoint's own verdict was the question*, and that is the narrow case where it is
   justified.
4. **Verify the folder afterwards** — hash the file, check for sidecars, check their git status.
   "I only looked at it" is a claim, and it is checkable.
5. **Generalises past GUI apps:** anything that takes a lock, writes a temp file, or holds a
   handle in someone else's tree — editors, indexers, `qlmanage`, archive tools, a shell whose
   cwd blocks an unmount.

**Related:** [[2026-08-03_mental-model-not-source-of-truth]] (my model of "open = read" was the
error), [[2026-08-14_i-read-representations-they-read-sources]] (I classified my own action
without checking it, the same free pass), [[2026-07-31_manage-dont-do]] (the boundary this
crossed), [[_ledger]]
