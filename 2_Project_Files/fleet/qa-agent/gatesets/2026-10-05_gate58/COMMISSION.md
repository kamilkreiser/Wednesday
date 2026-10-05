# gate58 — the commission (Wednesday -> kit drafter, 2026-10-05 ~14:14 AEDT), as received

Build the gate kit `gate58` for PR #1379 (KS-749): Seat F 1st's advisory bump — browserslist 4.28.7 (+ caniuse-lite / electron-to-chromium / node-releases where below its floors) in 6 lockfiles, postcss-selector-parser 6.1.4 in the workspace-root lock, and 3 baseline rows removed from `Blockchain/Dev/scripts/audit/audit-baseline.json` (GHSA-c83g, GHSA-73wf, GHSA-w9m9). Tier T1.

- WRITE ONLY under this directory (README.md first, kit.json, the checkers, a launcher `repin_and_launch_gate58.sh <n> <head> --dry-run|(real)`, a prompt template). Scratch only under the session scratchpad `…/scratchpad/gate58/`. Read-only in `/Volumes/DevMASTER/!CODING` (git write verbs only in a `git clone --shared` in the scratch, fetching with the checkout's own `core.sshCommand`). No `rm`. Never run a refusal arm with a path outside the scratch.
- TEMPLATE: `2026-10-04_gate54f/` (gated the identical class, #1373 KS-1403). Frozen-clock proof shape and launcher conventions from `2026-10-05_gate56a/`.
- THE READY (`fleet/briefs_staged/2026-10-05_seatF1_READY_1379.txt`) holds the builder's claims: the gate TESTS them. The builder's brief `fleet/briefs_staged/2026-10-05_seatF1_advisory_bump.md` + Wednesday's 13:30 ANSWER ruling: ONE PR Refs KS-749 with both bumps and all three rows; KS 751 is ARCHIVED and must not be referenced hyphenated.

THE CHECKS (each with a control that can fail):
- C1 pin — PR head == the READY's head, base == develop at origin, file set == exactly 7 paths.
- C2 lock diff semantic AND line, per lock: changed entries == exactly the 23 named, 0 added/removed, 0 flag flips, libc/os/cpu arrays unchanged, root lock key order (resolved+integrity after version, before license), dependencies maps alphabetical.
- C3 integrity — recompute sha512 of the 5 tarballs == registry == every lock carrying them, negative control with the OLD version's tarball.
- C4 baseline — exactly the 3 rows removed, the 22 remaining byte-equal.
- C5 legs 2/5/6/7 at head (leg 5 case count stated), base control legs 6+7 red naming the rows under a frozen clock 2026-10-15T00:01Z, head green under the same freeze, a bite arm reverting one lock; full `npm ci --ignore-scripts` at Blockchain/Dev from the committed root lock (installability).
- C6 scope: PR body names KS-749 only hyphenated, no KS 751 hyphenated anywhere (title, body, commit), NOT COVERED names mobile/secuura-app and the CSS build diff.
- Self-test every checker on base-vs-base (must FAIL where a change is required) and on a planted wrong edit.

Reply terse: kit path, files, each checker's self-test result, the exact launch command and routing line Wednesday must add, and anything in the READY already found contradicting itself.
