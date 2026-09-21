# wake_watch.sh idle leg — detector verdict in the wake text (2026-09-21)

Commissioned by Wednesday; tooling subagent. Change: the idle-at-prompt leg of
`fleet/cockpit/wake_watch.sh` runs `pane_prompt_check.sh` on the pane and appends
` — detector: <verdict>` to both idle wordings (HOLDING and plain). Swap at
2026-09-21 20:21:58 AEST. `.new` + `mv` — never in place; runner never touched.

## Slips
- None that changed the outcome. Two notes for honesty:
  1. A PreToolUse advisory fired on my two post-swap `grep -c` verifications
     (`'detector: \$det'` → 2, `'idle at prompt'` → 4) for being case-sensitive
     phrase greps. Both counts were non-zero and paired with each other as
     positive controls, so no false zero occurred; noted, not repeated.
  2. I created and then killed my OWN scratch tmux session `wwtest`
     (`tmux kill-session -t wwtest`). Nothing in `fleet` or `sync` was touched;
     `list-sessions` before and after is in the command log.
- Nothing was deleted or renamed except the deliberate `mv` of `.new` over the
  original after the backup existed and compared identical (`cmp` rc 0).

## Swap done?
YES. Backup: `wake_watch.sh.pre-0921-2021-idledetector` (29617 bytes, mtime
17 Sep 11:08 preserved by `cp -p`; `cmp` against the original rc 0 before the
mv). Live file after mv: 30494 bytes, exec bit intact, `bash -n` rc 0.
The running child (pid 53263, baseline 2026-09-21T09:34) keeps the OLD inode;
the runner (2600) loads the new file on its next `OUT=$(wake_watch.sh …)`
cycle. Runner-side `case` still matches: the new text contains
`idle at prompt` (4 occurrences in the file: 2 comments/wait wording, 2 idle
wordings); `wake_ack.sh $pid` wording unchanged.

## Runner pid before / after
- Before (20:19:49 AEST): runner `2600` (= state/wake_watch_runner.pid),
  command-substitution subshell `53262`, live child
  `53263 /bin/bash …/cockpit/wake_watch.sh 2026-09-21T09:34 3 60`.
- After the mv (20:21:58 AEST): `2600`, `53262`, `53263` all present;
  `arm_wake_watch.sh status` → `armed (runner pid 2600)` rc 0. Nothing killed.

## Diff (original vs .new)
```diff
--- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/wake_watch.sh	2026-09-17 11:08:05
+++ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/wake_watch.sh.new	2026-09-21 20:20:13
@@ -339,10 +339,20 @@
     # separate legs and are untouched.
     # (ackf/ack are read above the branches since 2026-09-16)
     if [ "$cnt" -ge "$STABLE_N" ] && [ "$ack" != "$h" ]; then
-      if [ "$holding" = 1 ]; then
-        echo "WAKE: pane '$name' ($pid) idle at prompt ~$((STABLE_N * INTERVAL / 60)) min — likely waiting on Wednesday (HOLDING: turn ended, only a background monitor/shell is live — check its inbox first; if it is holding by design, wake_ack.sh $pid silences this exact state)" > "$STATE_DIR/fired"
+      # DETECTOR VERDICT IN THE WAKE (2026-09-21, ledger w=3 -> enforcement): four
+      # times today a Claude ghost suggestion wearing the fleet's own tap prefix sat
+      # at a HOLDING seat's prompt and the idle wake carried no verdict, so the
+      # coordinator read the pane before the detector had. The idle leg now runs
+      # pane_prompt_check.sh on the pane itself and appends its one-line verdict
+      # (SUGGESTION / TYPED, UNSENT / prompt empty / MODAL) to BOTH idle wordings.
+      # Newlines are folded; a silent or failing detector reports NO VERDICT (rc N).
+      det=$(bash "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pane_prompt_check.sh" "$pid" 2>/dev/null); drc=$?
+      det=$(printf '%s' "$det" | tr '\n\r' '  ' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
+      [ -n "$det" ] || det="NO VERDICT (rc $drc)"
+      if [ "$holding" = 1 ]; then
+        echo "WAKE: pane '$name' ($pid) idle at prompt ~$((STABLE_N * INTERVAL / 60)) min — likely waiting on Wednesday (HOLDING: turn ended, only a background monitor/shell is live — check its inbox first; if it is holding by design, wake_ack.sh $pid silences this exact state) — detector: $det" > "$STATE_DIR/fired"
       else
-        echo "WAKE: pane '$name' ($pid) idle at prompt ~$((STABLE_N * INTERVAL / 60)) min — likely waiting on Wednesday" > "$STATE_DIR/fired"
+        echo "WAKE: pane '$name' ($pid) idle at prompt ~$((STABLE_N * INTERVAL / 60)) min — likely waiting on Wednesday — detector: $det" > "$STATE_DIR/fired"
       fi
     fi
   done
```

## Arms (scratch tmux session `wwtest`, never `fleet`)
Setup: `tmux new-session -d -s wwtest -x 140 -y 30 'bash --norc --noprofile'`
→ pane `%21`; `set-option -p -t %21 @cockpit_name testagent` (verified
`%21|testagent|wwtest`). Every watcher run: `WAKE_WATCH_TMUX_SESSION=wwtest`,
baseline `2099-12-31T23:59` (so the mail/chat legs cannot fire), stable_n 2,
interval 2; run in the background, polled for exit (bound 120 s, never hit),
rc read with `wait`. `coord_pane_id wwtest:0` finds no coordinator pane, so
the DEAD/EXITED legs skipped as designed.

### Arm a — ghost/dim line at the prompt → SUGGESTION  (PASS)
Pane content printed with `printf "\342\235\257\302\240\033[2m[Wednesday tap] GO mailed \342\200\224 test ghost suggestion\033[0m\n"`
(glyph + NBSP + SGR-2 dim span). `capture-pane -p -e` showed `^[[2m` on the
line. Detector alone: rc 0,
`  testagent: SUGGESTION (Claude ghost text — ignore) :: [Wednesday tap] GO mailed — test ghost suggestion`.
`.new` watcher (pid 96634) exited rc 0 after ~6 s with:
```
WAKE: pane 'testagent' (%21) idle at prompt ~0 min — likely waiting on Wednesday — detector: testagent: SUGGESTION (Claude ghost text — ignore) :: [Wednesday tap] GO mailed — test ghost suggestion
```

### Arm b — empty prompt → detector's empty verdict  (PASS)
Pane content: `printf "\342\235\257\302\240\n"` (glyph + NBSP only).
Detector alone: rc 0, `  testagent: prompt empty`.
`.new` watcher (pid 99605) exited rc 0 after ~6 s with:
```
WAKE: pane 'testagent' (%21) idle at prompt ~0 min — likely waiting on Wednesday — detector: testagent: prompt empty
```

### Arm c — control: pre-edit file, same pane → NO `detector:`  (PASS)
Ghost line restored (same printf as arm a). ORIGINAL `wake_watch.sh`
(pid 1951) exited rc 0 after ~6 s with:
```
WAKE: pane 'testagent' (%21) idle at prompt ~0 min — likely waiting on Wednesday
```
`grep -c 'detector:'` on that output → 0 (rc 1): the arm discriminates.

### Arm d (bonus) — HOLDING wording with ghost prompt, `.new`  (PASS)
The four real occurrences were on HOLDING seats, so the other wording was
exercised too. Pane content: `✻ Baked for 10s · done 9:59 pm · 1 monitor still running`,
blank line, then the ghost prompt line. `.new` watcher (pid 2535) exited rc 0
after ~7 s with the HOLDING wording and the verdict:
```
WAKE: pane 'testagent' (%21) idle at prompt ~0 min — likely waiting on Wednesday (HOLDING: turn ended, only a background monitor/shell is live — check its inbox first; if it is holding by design, wake_ack.sh %21 silences this exact state) — detector: testagent: SUGGESTION (Claude ghost text — ignore) :: [Wednesday tap] GO mailed — test ghost suggestion
```

## Not tested
- The TYPED-UNSENT and MODAL verdict shapes in the wake text (the detector's
  own output is passed through unchanged, and both arms above prove the
  pass-through; not driven separately).
- The `NO VERDICT (rc N)` fallback (detector always exits 0 and printed on
  every arm; the fallback branch was read, `bash -n`-checked, not fired).
- The live runner's tap of the longer wake text into the wednesday pane
  (`send-keys -l` + read-back). The wake text is longer by the verdict; the
  runner `case` match (`*"idle at prompt"*`) was verified by reading, and the
  `.new` was never run against `fleet`. First real fire will show it in
  `logs/wake_watch_runner.log`.
- Any leg other than (b) idle: mail, chat, ctx, DEAD, EXITED, frozen-busy,
  subagent-wait — untouched by the diff.
- The running child 53263 still runs the old code until the runner's next
  cycle; the first NEW-code cycle after this report has not been observed.

## Command log (command / rc)
- skeleton report written → rc 0; `date` 2026-09-21 20:19:49 AEST
- `pgrep -fl 'cockpit/wake_watch.sh'` → rc 0 (2600, 53262, 53263)
- `cat state/wake_watch_runner.pid` → 2600
- `cp -p wake_watch.sh wake_watch.sh.new` → rc 0
- python3 exact-match edit of `.new` (asserted each target occurs once) → rc 0
- `bash -n wake_watch.sh.new` → rc 0
- `diff -u wake_watch.sh wake_watch.sh.new > scratch/idledetector.diff` → rc 1 (differs, as intended)
- `tmux has-session -t wwtest` → not present; `tmux new-session -d -s wwtest …` → rc 0; pane `%21`
- `tmux set-option -p -t %21 @cockpit_name testagent` → rc 0
- arm a: `send-keys` ghost printf → rc 0; `pane_prompt_check.sh %21` → rc 0 (SUGGESTION); `.new` run → rc 0 (~6 s)
- arm b: `send-keys` empty-prompt printf → rc 0; detector → rc 0 (prompt empty); `.new` run → rc 0 (~6 s)
- arm c: ghost restored → rc 0; ORIGINAL run → rc 0 (~6 s); `grep -c 'detector:'` → 0, rc 1
- arm d: holding+ghost printf → rc 0; `.new` run → rc 0 (~7 s)
- `cp -p wake_watch.sh wake_watch.sh.pre-0921-2021-idledetector` → rc 0; `cmp` → rc 0
- `[ -x wake_watch.sh.new ]` → rc 0
- `mv wake_watch.sh.new wake_watch.sh` → rc 0 at 2026-09-21 20:21:58 AEST
- `bash -n wake_watch.sh` (live) → rc 0; `grep -c 'detector: \$det'` → 2; `grep -c 'idle at prompt'` → 4
- `pgrep -fl` after → 2600, 53262, 53263 present; `arm_wake_watch.sh status` → armed (runner pid 2600), rc 0
- `tmux kill-session -t wwtest` → rc 0; `list-sessions` → fleet, sync
- Scratch artefacts (outside the project): `$SCRATCHPAD/{idledetector.diff,arm_a.out,arm_b.out,arm_c.out,arm_d.out,det_a.txt,det_b.txt}`
