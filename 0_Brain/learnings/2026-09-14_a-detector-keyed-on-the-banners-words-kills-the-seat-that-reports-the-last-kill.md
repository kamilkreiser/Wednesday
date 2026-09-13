---
date: 2026-09-14
type: correction
source: "two DEAD-leg false kills of a healthy coordinator in eight hours — 2026-09-13 23:39:43 (s214 at ctx 29%, diffing the resolver patch into its pane) and 2026-09-14 06:53:53 (the seat Kam launched at 06:46, one minute after committing a boot note that quoted the leg's grep); measured from cockpit/logs/wake_watch_runner.log + rotate_wednesday.log"
status: live
tier: W
supersedes: ""
---

# A detector keyed on the BANNER'S WORDS kills the seat that reports the last kill — the DEAD leg must discriminate the UI banner from a sentence about it, and the fix is a shared predicate with a selftest, not a tighter literal

**The operative case, so the headline matches it:** Wednesday is writing, ratifying or diagnosing
any detector that reads a PANE (or a log, a transcript, a chat store) for a literal that means
"the thing is dead / broken / needs killing" — and whose fire path is DESTRUCTIVE (a respawn, a
kill-pane, a restore). **Ask: what does the pane show when the seat is DIAGNOSING the last fire?**
It shows the literal. The seat that reports the previous kill — a cat'd diff, a note written by
heredoc, a `tail` of the runner log — prints the trigger word into the very surface the detector
reads, and the detector kills it. **The second kill is guaranteed by the first, because the honest
report of the first is the trigger for the second.**

**The case, measured.** The watcher's DEAD leg (`wake_watch.sh`) and the re-check in
`wednesday_rotate.sh --dead` both did `capture-pane -S -60 | grep -q 'Context limit reached'`.
- 23:39:43 — the s214 seat (booted 23:38, ctx 29%) had just `cat`/diffed `staged/resolver-20260913/DIFF.md`
  (the patch text contains the grep line ×3) into its own pane; the re-armed watcher matched it the
  same second and `--dead` re-checked the same literal and respawned. The floor ran headless until 06:00.
- 06:53:53 — the seat Kam launched at 06:46 wrote its boot note at 06:52 (`fe155cc6b`), describing
  the 23:39 kill and quoting the grep; the note text sat in its pane; the leg fired on the first
  cycle after its 600 s boot grace and killed it. This seat is the respawn — and its own first
  diagnostic `tail` printed the literal into ITS pane too (the old predicate read 6 hits on it).
- Cost: s213 (L7) got no plan confirmation for 5.5 h; s212's four READYs sat ungated all night;
  panel_sync SKIPPED ~7 h on the killed seat's uncommitted paths; Kam's 06:46 launch was wasted.

**Why the existing lessons did not fire (the w=2 diagnosis).** [[2026-09-10_a-detector-keyed-on-remedy-text-matches-the-hint]]
says "key a detector on the CONDITION, never on the remedy's name" — this leg was keyed on the
CONDITION's name, which the 09-10 rule reads as correct. [[2026-08-07_a-check-that-cannot-fail]] asks
what would make a check fail; nobody asked what would make it fire FALSELY on the system's own
reporting of itself. And the 06:46 seat filed the fix as "owed (shared with Tuesday — claim first)"
— an owed fix on a detector that kills the coordinator is a promise ([[2026-08-07_a-promise-is-not-a-mechanism]]),
and the promise was killed by the thing it was about.

**How to apply:**
1. **A destructive detector's literal must be unreachable from tool output.** The predicate now
   lives in `2_Project_Files/fleet/cockpit/dead_banner_check.sh` (both callers use it): the banner's
   words on a line with NO quote/backtick, NO `⎿` tool-output prefix, NO `#` / `—` / `;` / `grep`
   prose markers. Its `--selftest` carries the three real false positives and two true banners.
   Adding a fourth false positive means adding it to the selftest FIRST.
2. **Before diagnosing the last kill in a live pane, ask whether the diagnosis prints the trigger.**
   Redirect to a scratch file and Read it; never `tail` a detector's own log into the pane it reads.
3. **A fix to a self-killing detector is done BEFORE the re-arm, not claimed and owed.** The
   09-10 claim-with-Tuesday rule stands for shared tooling — claim AND fix in the same action when
   the next fire kills the claimer; the claim mail names the commit.
4. **Do not tighten to the full banner text as the fix.** "Context limit reached · /compact or
   /clear to continue" is a 2026-09-02 reading of the UI; requiring it makes the leg BLIND if the
   UI changes, which is the six-hour failure the leg exists to prevent. Exclusions on the reporting
   shapes discriminate; a longer literal only moves the target.
5. **Enforcement candidate (w=3 promotes it):** the watcher's DEAD leg requires a SECOND independent
   source before killing — the seat's transcript jsonl showing no turn since the banner appeared,
   or a `ctx:` statusline ≥ 95% — a disagreement between two sources refuses
   ([[2026-09-09_a-guard-refuses-malformed-input-and-the-real-failure-is-stale-input]] rule 2).

**Family:** [[2026-09-10_a-detector-keyed-on-remedy-text-matches-the-hint]] (the sibling: there the
tool's HINT carried the remedy's name; here the seat's REPORT carries the condition's name) ·
[[2026-08-07_a-check-that-cannot-fail]] · [[2026-08-17_check-the-refusal-before-the-kill]] (a
destructive step behind a check that cannot discriminate) · [[2026-09-11_red-proof-arms-cover-every-legitimate-shape-of-the-real-event]]
(the CLEAN arm this leg never had: "a healthy seat talking about the banner") ·
[[2026-09-02_the-statusline-is-the-context-instrument]] (the leg's origin) ·
[[2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate]] (a headless floor is the cost).
