---
date: 2026-09-09
type: correction
source: Kam, dashboard panel 12:38:39 — "refreshed but I cannot see the change. if its easier, you can put % elswhere"
status: live
tier: W
---

# A fix written into a file that something else GENERATES lives until the next boot — before editing any file, ask what WRITES it

**The operative case, so the headline matches it:** you are about to edit a file to make a
change stick — a config, a statusline, a settings key, a launcher-managed copy, a generated
digest. **Before the edit, ask one question: what else writes this file, and when?** If a
launcher, a generator, an installer or a sync leg rewrites it, the change is not a fix. It
is a fix with a fuse, and the fuse is the next boot — **which is usually the person's next
interaction, so the report of success and the disappearance of the feature arrive in that
order.**

`git check-ignore` answers "is this tracked?"; nothing answers "is this GENERATED?" except
reading the thing that generates it.

## The case, measured

Kam asked at 12:32 for the weekly usage % on the dashboard's agent chips. The previous seat
built it, exercised it on three paths, verified `/api/usage` live, told him it was done, and
rotated at 12:37. He refreshed at 12:38 and saw nothing.

**Two independent defects, and both are this file's shape or its sibling.**

1. **THE WRITER.** The publish block went into `2_Project_Files/tools/statusline.sh`. That
   file is a **copy**: `Launch_Wednesday.command` refreshes it from
   `Setup and System/statusline.sh` at every launch, and points `settings.local.json` at the
   shared original *in preference to it*. So the feature was doubly dead — overwritten at
   the next boot AND never executed even before that. It lived about ninety seconds. **The
   rotation at 12:37 is what killed it**, which means the seat's own correct behaviour
   destroyed its own work. The published figure froze at the moment its writer died, so the
   symptom was not "no number" but "a number that never moves" — the quietest possible
   failure.

2. **THE SURFACE.** The chips were added to `chat.html` only. `cockpit.html` carries the
   identical `ag-wednesday` / `ag-tuesday` toggle and never got them — and the cockpit is the
   page Kam actually uses. He confirmed it with a screenshot: *"this is the view I live in."*
   That half is [[2026-08-07_enumerate-every-surface-before-done]] in its original costume, a
   second renderer of the same data in the same app, unlooked at. **The closing check is
   absence — `grep -l 'ag-wednesday' *.html` returns two files and always would have.**

## Why the existing lessons did not fire

[[2026-08-25_travel-drive-stale-pointers]] names the shape for PATHS — "what happens when
this file wakes up on a different volume?" — and [[2026-08-09_an-enforcement-you-must-arm-is-not-one]]
names it for safeguards. Neither asks the question for a file's **contents on the same
machine**. The predecessor did check portability, carefully: it replaced a hardcoded
`/Volumes/...` path with a self-locating one *specifically* because of the travel-drive
lesson. **It was reasoning about the right family and looking one layer too low.** The
question it did not ask is not "will this path survive a move?" but "will this FILE survive
a launch?"

This is [[2026-09-09_the-seat-resolver-is-the-layer-above-every-agent-aware-fix]] with the
layer changed: there the thing above the parameter was the resolver; here the thing above
the file is its writer.

## How to apply

1. **Before editing any file to make behaviour stick, grep the launcher and the generators
   for its name.** `grep -rn '<basename>' Launch_*.command 2_Project_Files/` is one command.
   A hit in a `cp`, a `>`, a template render or a `json.dump` means the file is an OUTPUT,
   and editing an output is editing a cache.
2. **When a file is generated, the fix goes in the GENERATOR or in a seam the generator does
   not own.** A wrapper beside it, a new file the launcher points at, a template input —
   never the artefact. Where the generator is out of scope (a shared file across clients),
   the wrapper IS the answer, not an argument for editing it anyway.
3. **Verify a "sticky" change by making the thing that overwrites it RUN.** A boot-surviving
   change is not proven by the feature working now; it is proven by the feature working
   **after the launcher, the generator or the sync has run once more.** That is the red-proof
   for this family and it costs one launch.
4. **A frozen value is this failure's fingerprint.** Not an error, not a blank — a number,
   a timestamp or a status that is present and never moves. When a live figure stops
   advancing, suspect that its WRITER is dead before suspecting the reader.
5. **The surface half, restated because it recurred:** before reporting any UI change done,
   `grep -l` the identifying markup across every page in the tree. Two renderers of one
   toggle is the standard hiding place, and "the page I looked at works" is a presence check
   that always passes.

## What went right, kept so the record is honest

The predecessor caught two of its own defects before shipping (a name bound only inside
other methods; a hardcoded absolute path) and stated Tuesday's blank chip as *expected*
rather than letting it look broken. Its design — one writer per file, staleness shown with
its age rather than hidden — was right and survived the repair untouched. **The failure was
not carelessness; it was a correct check pointed one layer below the defect.**

And the fix round found two more of the same family by running rather than reading: a log
directory created inside the failure handler, so every `2>>"$LOG"` before the first failure
could not open its target and the publish silently did nothing; and `resets_at` parsed as an
ISO string when it is epoch seconds. **Both were invisible to reading and obvious to one
run** ([[2026-08-06_exercise-mechanisms-before-arming]]).

**Family:** [[2026-08-07_enumerate-every-surface-before-done]] (the second defect, in its
original costume) · [[2026-09-09_the-seat-resolver-is-the-layer-above-every-agent-aware-fix]]
(the same "one layer up" shape) · [[2026-08-25_travel-drive-stale-pointers]] (the paths
version, which fired correctly and was not enough) ·
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] · [[2026-08-07_a-check-that-cannot-fail]]
(the log-directory bug: a publish that could not report its own failure) ·
[[2026-08-06_exercise-mechanisms-before-arming]].
