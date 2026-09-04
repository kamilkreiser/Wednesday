---
date: 2026-09-05
type: preference
source: Kam, panel 2026-09-05 08:1x — "please look at your root folder. please ensure (create a rule) to file things properly. the images in the root folder do not belong there."
status: live
---

# The project root holds only rules and launchers — every file Wednesday writes has a folder, and the root is never it

**The operative case, so the headline matches it:** Wednesday is about to write, copy
or `mv` a file and the destination path is `/Volumes/DevMASTER/WEDNESDAY/<file>` — a
screenshot for Kam, a render, an export, a "temporary" artefact. **Stop. The root is
the front door: `CLAUDE.md`, `PORTABILITY.md`, `.gitignore`, the `Launch_*.command`
launchers, and nothing else.** Kam opened the folder this morning and found four PNGs
(two NexusAI Sustainability screens from 09-04, two WED-82 dashboard shots from 08-07)
sitting beside the launchers — one pair had even been *committed* there.

**The case.** The 09-04 screenshots were rendered for Kam's eye (the 09-03 lesson on
mocks: "his eye is the only instrument that has ever caught this class") and dropped
in the root because it was the shortest path to a file he could open. The 08-07 pair
were gitignored by a pattern (`wed*-dark.png`) that made them invisible to `git
status` and therefore to every wrap — a gitignore hides a filing miss as well as a
secret. A screenshot's proper home already existed by precedent:
`0_Brain/reference/2026-09-01_nexusai-s12-screens/` is tracked in the repo.

**Why the existing lessons did not fire.** [[2026-08-04_gitignore-artifacts-at-creation]]
says "decide the artefact's fate at creation" — it was read as a question about
*committing*, not about *where*. The folder map in `CLAUDE.md` names what each folder
is for but never said what the root is NOT for, so a file in the root violated nothing
written.

## How to apply

1. **Every write names its folder before its filename.** Screenshots and renders →
   `0_Brain/reference/<date>_<topic>/` (the s12 precedent); session artefacts
   (PDFs, handover docs, drafts) → `5_Project_History/`; anything transient → the
   session scratchpad, never the tree. If the file is for Kam to open, the path
   still goes in the folder and the *pointer* goes in the panel message.
2. **A backup of a root script may sit beside it** (`Launch_Wednesday.command.pre-*`,
   the cockpit's `cockpit.sh.pre-0902-*` precedent) — that is the one exception, and
   it is a backup of a root file, not a new kind of file.
3. **Enforcement, not intention:** `2_Project_Files/doctor.sh` now warns at every
   launch on any root file outside the allow-list (exercised both ways on
   2026-09-05: a probe file fired it, its removal cleared it). The rule also stands
   in the `CLAUDE.md` folder map as a *(root)* row.
4. **Cleanup means quarantine/move, never delete** ([[2026-08-26_never-delete-cleanup-means-quarantine]]):
   the four images were `mv`'d into their reference folders, the git move recorded.
5. **Test by its handle:** if the path has no folder segment after `WEDNESDAY/`, it
   is wrong.

**Family:** [[2026-08-04_gitignore-artifacts-at-creation]] (fate at creation — now
including *location*) · [[2026-08-26_never-delete-cleanup-means-quarantine]] ·
[[2026-08-07_a-check-that-cannot-fail]] (the doctor check was fired before it was trusted).
