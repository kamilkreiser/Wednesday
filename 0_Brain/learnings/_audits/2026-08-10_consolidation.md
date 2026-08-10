# Consolidation audit — 2026-08-10 (evening session, post-wrap respawn)

Run by the fresh session commissioned at the day-close ("consolidation FIRST,
only big task"). Window: 22:10–23:00, deliberately budget-capped — this was
the densest week on record and the agenda was crowded; everything not done
tonight is named below with an owner, not left implicit.

## Changes made (deltas, per anti-collapse guard)

1. **wake_watch.sh pane leg is now ghost-text-aware** (the 16:3x blind spot:
   Vision idled 90 min with 5 unseen mails behind a dim machine suggestion).
   Delta: prompt line re-read from `capture-pane -e`, SGR-2 (dim) spans
   stripped — the same discriminator `pane_prompt_check.sh` uses — before the
   empty-prompt idle test. Exercised: 5/5 synthetic shapes (empty, ghost with
   reset, ghost without reset, TYPED-unsent → correctly still not-idle, bare
   empty). Live watcher cycled onto the new code with baseline preserved
   (11:52) and mode auto-correct to mail+chat-only (agents=0). **Validation
   per DGM guard: components proven; the composed fire on real ghost text
   waits for the next live occurrence — flag in the next audit.**
   Deliberate scope choice: TYPED-unsent text still reads as not-idle (a
   human mid-typing is not an agent waiting); the 08-05 unsent-line lesson
   covers that case by manual pane reads.

2. **Close bell now detects unwrapped sessions** (ledger w=5 forced item —
   "a ritual nothing triggers is not a ritual"). Delta in
   `close_wednesday.sh`: before stamping, it checks the three wrap artifacts
   (retro off its template placeholder · tree clean outside
   `0_Brain/dashboard/data` collector churn · today's note tracked by git),
   logs the verdict, writes `state/wrap_check_<date>`, appends a loud
   reconcile-first block to the daily note on failure, and names the flag in
   the spoken good-night. Exercised both directions in the real script
   (TEST_HOUR+DRYRUN): fire on the genuinely-dirty tree (counted exactly the
   2 real edits, ignored 10 churn files), verified after commit. **Tonight's
   live 23:00 fire is its first armed run.** Churn exclusion is deliberate:
   an alarm that fires every night is a check that cannot pass.

3. **Coordinator auto-rotation (Kam's post-wrap catch): verifier half built,
   respawn half deliberately NOT armed tonight.** The wrap-check state file
   is the gate the rotation step will read. Building a mechanism that kills
   my own pane, hastily, at 22:30, against exercise-mechanisms-before-arming
   — declined. Owner: next session, with both paths walked in a test tmux
   session first (the `WAKE_WATCH_TMUX_SESSION` hook exists for exactly this
   shape). Tonight's manual respawn was the dry run; the verifier it needs
   now exists and will have one night of live evidence by morning.

4. **Blanket-ack lesson generalised** (w=2 diagnosis executed): title and a
   new section state the CLASS — watermarks/baselines/cursors/seen-flags
   advance only over provably-processed events, never to "now" — so the
   retrieval handle is no longer the mark-seen script. Incremental edit; all
   original content and handles retained.

## Enforcement-vs-rule scope audit (the w=6 pattern: enforcement scoped
narrower than its rule)

| Enforcement | Rule it enforces | Scope verdict |
|---|---|---|
| wake_watch (mail+chat+pane+ctx legs) | "channels gated on my attention get watched" | **NOW matched** — chat leg added 08-10 morning, ghost gap closed tonight. Residual: dashboard chat file only; any future channel must be added the day it exists. |
| arm_wake_watch runner (launcher-armed) | watcher always on when panes live | matched (launcher in every session's path); doctor hard-fail is the backstop |
| close-bell wrap check | wrap ritual runs every day | **built tonight** — was the named gap |
| send_brief.sh provenance gate | every relayed fact carries provenance | **narrower by design**: gates briefs to agents only; instructions to humans rely on the lesson (08-06 extension). Mechanically ungateable — chat has no send gate. Accepted, named. |
| pre-commit artifact hook | artifacts gitignored at creation | **narrower**: this repo only; does not travel to fleet repos (each has its own hooks or none). Carried: propagate pattern via briefs, not by me editing their repos. |
| pane_prompt_check.sh | never read pane text as instruction | **run-on-demand = habit-gated.** Candidate: fold a SUGGESTION/TYPED report into the watcher cycle or launcher. Next consolidation. |

## Ledger review

- **No weights retired.** The week's active families (attention/enforcement
  w=4→5→6; verification family w=4) are too hot to retire anything; trend is
  the metric and this week's trend is: recurrences keep escalating INTO
  enforcement same-hour, which is the system working as designed, but the
  attention family needed three escalations in three days to get there.
- **Trend note for Kam:** corrections this week clustered on one root shape —
  mechanisms gated on my memory/attention. Every fix that held was a gate in
  the path of something that fires anyway. That doctrine is now written into
  three lessons; the scope audit above is its checklist.

## WED-36 boot-cost check — NUMBER CROSSED, recommendation attached

46 lesson files + ledger = **~65K tokens** (174KB) at this boot; total boot
(identity, people, tasks, INDEX, two daily notes, checks) lands ~90–100K.
At 08-06 the re-affirmation was made at 28 lessons / ~18K. The full-load
ruling stands (Kam's, twice), but the number has tripled in four days and
now costs roughly half a session window before work starts.
**Recommendation to Kam (no action taken tonight):** keep full load, but let
next week's consolidation MERGE the verification family — 5–6 files
(chain-not-legs · artifact-presence · local-proof · check-that-cannot-fail ·
enumerate-surfaces · valid-is-not-delivered) share one root discipline and
could become one file with named sub-cases, preserving every retrieval
handle as a heading. Est. saving ~15–20K boot tokens without losing a
handle. Needs your explicit go — it touches the "never delete a lesson"
discipline (supersede-with-links would be used, per the routing rules).

**KAM RULED, same night (~22:30): merge DEFERRED.** *"For now its fine but
will require review. Lets not rush to cutting this down until we can find a
system that gives us the best result and reduces the load. So a regular
review is wise."* → No cutting/merging until a load-reducing system is found
that provably loses nothing; boot-cost number + trend become a standing line
in every consolidation audit. Ruling folded into
[[../2026-08-03_context-loading-split]] and commented on WED-36.

## Deferred, with owners (nothing left implicit)

- **Boundary-reads → fleet doctrine (Vision's fix):** detail lives in
  Vision's 08-10 wrap thread; I did not have it in context tonight and
  declined to guess (mental-model rule). Owner: next consolidation, source
  named.
- **Launcher warnings → file agents can read** (structural find 08-10):
  WED ticket created tonight. Owner: next build session.
- **Rotation respawn step:** WED ticket created tonight (see §3).
- **Orphaned serve.sh collect loops (4):** left running per PORTS.md
  never-kill; cleanup needs a deliberate serve.sh restart in daylight.
  Queued for the morning session, Kam awake.
- **Weekly industry scan:** not run this week (WED-84 + Stage 3 consumed
  it). Owner: next 06:00 slot after the morning briefing, or explicitly
  dropped for the week by Kam's call.
- **INDEX.md Vision section** still headlines 08-08; Stage 3 LIVE facts are
  in today's daily note + scoreboard. Morning session folds them in.

## Session's own incident (honesty row)

Booting, I misread `ps` output as TWO wake_watch runners and nearly killed
one. Checked parentage first: the second PID was the runner's own
command-substitution subshell (ps shows forked subshells with the parent's
full script text). One healthy runner. Verify-before-kill held; filed here
as the behaviour to keep, not ledgered (nothing was acted on).
