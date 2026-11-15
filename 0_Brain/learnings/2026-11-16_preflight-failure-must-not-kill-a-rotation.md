---
date: 2026-11-16
type: correction
source: "Kam, 2026-11-16 ~07:10, after the 07:04 --self rotation stalled at the preflight prompt: 'if the problem occurs it should not kill the rotation'"
status: live
tier: W
supersedes: ""
---

# A preflight failure must never stop a rotation; carry it into the new seat's boot instead

**The lesson:** a human-answered gate must never sit in an unattended path. When a seat is
launched by a rotation (`wednesday_rotate.sh --self|--dead`), a HARD preflight failure is
**carried forward, not gated**: the launcher continues, logs the ✗ lines, and puts them at the
top of the new seat's boot prompt as first work. A human launch (Kam at the keyboard) still gets
"Continue anyway?", because there someone can decide.

**Context:** the 07:04 --self respawn on the Mac Studio hit one hard failure: Homebrew's
unversioned `python3`/`pip3` links had gone, so `python3` fell back to macOS 3.9 (below 3.10).
The launcher stopped at "Continue anyway? Type yes" and the new seat sat unbooted until Kam
typed yes. The rotation liveness checker logged `LIVENESS OK … 0 agent-live`, so nothing flagged
the stall. Kam read it as a NAS fault because the "HARD FAILURES" line is printed directly below
the DEV-Working NAS warning. The NAS was only a WARN (reachable, simply not mounted).

**How to apply:**
- `wednesday_rotate.sh` inlines `SEAT_ROTATION=$MODE` into the respawn command. It has to be
  inlined: `respawn-pane` runs in the tmux server's environment, so an export would not reach it.
- `Launch_Wednesday.command`: with `SEAT_ROTATION` set, a non-zero doctor exit sets
  `PREFLIGHT_HARD`, appends it to `cockpit/logs/rotate_wednesday.log` and adds a 🔴 block to
  INITIAL_PROMPT. The seat that boots fixes those lines BEFORE the brain load and re-runs doctor.
  These are still failures (no-skip), just not a stop.
- Tested 2026-11-16 with a stub doctor that fails: rotation mode reached the end and logged the
  failures (rc 0); a human launch answering "no" exited 1, and one answering "yes" continued.
  Backups: `*.pre-1116-rotation-nogate`.
- Open gap, not fixed here: rotate_liveness.sh passed a seat that was still in its launcher.
  "Pane present" is not "seat booted". The `pane_is_booting` process check in monitor.sh is
  the right signal for it.
- When Kam names a cause ("the NAS"), verify which line actually failed before fixing the named
  thing. See [[2026-08-03_mental-model-not-source-of-truth]].

**Related:** [[2026-10-12_a-rotate-run-inside-its-own-pane-kills-itself]],
[[2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate]], [[../people/kam]]
