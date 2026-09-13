# DIFF.md — coordinator pane-name resolver unification (built in scratch 2026-09-13, not applied)

Live files (read-only): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/{wednesday_rotate.sh,wake_watch.sh,arm_wake_watch.sh}`.
Patched copies + NEW `seat_resolve.sh` (sourced by all three, must be installed beside them): this directory.

## NEW: seat_resolve.sh (no live counterpart)
One function pair, one file, sourced by all three scripts. `seat_resolve [dir]` sets `TREE_SEAT` (folder name TUESDAY -> tuesday, else wednesday) and `SEAT` (`WED_AGENT`, else `TREE_SEAT`) — the exact rule the three scripts each held a copy of. `coord_pane_id <tmux-target> [seat] [tree]` prints the coordinator pane id: exact `@cockpit_name == seat` first; else, for seat != wednesday, the LEGACY `wednesday` pane if and only if (g1) `tree == seat` and (g2) the pane's `#{pane_start_command}`, when it names a `…/<TREE>/Launch_*.command`, comes from a tree of the same seat; else rc 1 with one stderr line naming every name it looked for.

## wednesday_rotate.sh (2 hunks)
- Hunk 1 (@@ -49 @@): the inline `_tree_seat`/`SEAT=` case is replaced by sourcing `seat_resolve.sh` + `seat_resolve "$PROJECT_DIR"` — same inputs, same outputs, one copy.
- Hunk 2 (@@ -64 @@): the `WROW=… awk '$1==s'` exact-name lookup becomes `PANE_ID=$(coord_pane_id "=$FLEET")`; a refusal is logged with the resolver's own wording (both names) and still exits 2. Gates after this point (--dead literal check, --self ancestor + clean-tree) are untouched; the post-respawn `set-option @cockpit_name "$SEAT"` (live line 151) is what retires the legacy name after the first rotation.

    --- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/wednesday_rotate.sh	2026-09-13 15:55:44
    +++ /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0f8f9fa8-eada-40b6-ad2d-8c8120bb3b2f/scratchpad/resolver/wednesday_rotate.sh	2026-09-13 20:34:42
    @@ -49,9 +49,11 @@
     # Tuesday's seat (same script, her own `fleet`) gets her pane name and her launcher.
     # No fallback to the other seat's launcher: a missing one REFUSES (a guess here
     # boots the wrong identity — the 2026-09-09 case).
    -_tree_seat=wednesday
    -case "$(basename "$PROJECT_DIR")" in TUESDAY|Tuesday|tuesday) _tree_seat=tuesday ;; esac
    -SEAT="${WED_AGENT:-$_tree_seat}"
    +# 2026-09-13 (Tuesday's 19:1x finding): the seat AND the pane lookup now come from
    +# the ONE shared resolver, seat_resolve.sh — the same rule as before (WED_AGENT,
    +# else the tree's own name), so Wednesday's tree still resolves to "wednesday".
    +. "$HERE/seat_resolve.sh" || { log "REFUSED: $HERE/seat_resolve.sh missing — cannot resolve the seat"; exit 2; }
    +seat_resolve "$PROJECT_DIR"
     case "$SEAT" in
       tuesday)   SEAT_LAUNCHER="$PROJECT_DIR/Launch_Tuesday.command" ;;
       wednesday) SEAT_LAUNCHER="$PROJECT_DIR/Launch_Wednesday.command" ;;
    @@ -64,9 +66,14 @@
     LAUNCH_CMD="${ROTATE_LAUNCH_CMD:-bash \"$SEAT_LAUNCHER\"}"
     
     "$TMUX_BIN" has-session -t "=$FLEET" 2>/dev/null || { log "REFUSED: no tmux session '$FLEET'"; exit 2; }
    -WROW=$("$TMUX_BIN" list-panes -s -t "=$FLEET" -F '#{@cockpit_name}|#{pane_id}' 2>/dev/null | awk -F'|' -v s="$SEAT" '$1==s' | head -1)
    -[ -n "$WROW" ] || { log "REFUSED: no '$SEAT' pane in '$FLEET'"; exit 2; }
    -PANE_ID="${WROW#*|}"
    +# The pane: @cockpit_name == $SEAT, else the legacy "wednesday" pane IF this tree's
    +# own seat is $SEAT (cockpit.conf still names pane 0 "wednesday" on the mini —
    +# the case that refused --self and --dead for Tuesday on 2026-09-13). The guard
    +# and the refusal wording live in seat_resolve.sh; the respawn below renames the
    +# pane to $SEAT, so after one rotation the legacy branch is no longer taken.
    +PANE_ID=$(coord_pane_id "=$FLEET" 2>"$LOG_DIR/.rotate_resolve_err.$$") || {
    +  log "REFUSED: $(cat "$LOG_DIR/.rotate_resolve_err.$$" 2>/dev/null) [session '$FLEET']"; rm -f "$LOG_DIR/.rotate_resolve_err.$$"; exit 2; }
    +rm -f "$LOG_DIR/.rotate_resolve_err.$$"
     
     if [ "$MODE" = "--dead" ]; then
       CAP=$("$TMUX_BIN" capture-pane -t "$PANE_ID" -p -S -60 2>/dev/null)

## wake_watch.sh (3 hunks)
- Hunk 1 (@@ -49 @@): inline tree/seat case replaced by sourcing the resolver; `SEAT` is the same string as before on both trees (`_tree_seat` had no other readers).
- Hunk 2 (@@ -76 @@): leg (d) DEAD check finds the coordinator via `coord_pane_id "$FLEET"` (legacy-aware); a missing pane still just skips the check, as before.
- Hunk 3 (@@ -154 @@): leg (b) idle tripwire additionally skips the coordinator by resolved PANE ID — on the mini the pane is named `wednesday` while SEAT is tuesday, so the name-only skip let Tuesday wake herself about her own prompt.

    --- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/wake_watch.sh	2026-09-10 09:12:51
    +++ /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0f8f9fa8-eada-40b6-ad2d-8c8120bb3b2f/scratchpad/resolver/wake_watch.sh	2026-09-13 20:34:58
    @@ -49,16 +49,16 @@
     # Resolved ONCE here; every use below reads $SEAT. Wednesday's tree resolves to
     # "wednesday", so every comparison is the same string it was before.
     _root="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
    -case "$(basename "$_root")" in
    -  TUESDAY)   _tree_seat=tuesday   ;;
    -  WEDNESDAY) _tree_seat=wednesday ;;
    -  *)         _tree_seat=wednesday ;;
    -esac
     # WED_AGENT if set, else the TREE'S OWN NAME. The tree is the discriminator
     # because the runner does NOT inherit WED_AGENT (measured 2026-09-09) and
     # because the two trees are clones of one repo — the checkout path is the only
     # thing that differs between them.
    -SEAT="${WED_AGENT:-$_tree_seat}"
    +# 2026-09-13 (Tuesday's 19:1x finding): the rule now lives in the ONE shared
    +# resolver, seat_resolve.sh (also used by wednesday_rotate.sh + arm_wake_watch.sh),
    +# which sets SEAT + TREE_SEAT exactly as the case above did and adds
    +# coord_pane_id — the pane lookup that also accepts the legacy "wednesday" name.
    +. "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/seat_resolve.sh" || { echo "wake_watch: seat_resolve.sh missing beside this script" >&2; exit 2; }
    +seat_resolve "$_root"
     _routing="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/inbox_routing.conf"
     case "$SEAT" in
       tuesday)   SEAT_INBOX=$(awk -F'|' '$1=="Tuesday"{print $2}'   "$_routing" 2>/dev/null)
    @@ -76,7 +76,10 @@
       # hard stop "Context limit reached". Every other wake is pointless while this
       # holds — the seat cannot read a tap. Fires every cycle it is seen (the runner
       # respawns via wednesday_rotate.sh --dead; a respawn clears the pane).
    -  wpane=$("$TMUX_BIN" list-panes -t "$FLEET" -F '#{pane_id}|#{@cockpit_name}' 2>/dev/null | awk -F'|' -v seat="$SEAT" '$2==seat{print $1}' | head -1)
    +  # Resolved through coord_pane_id: @cockpit_name == $SEAT, else the legacy
    +  # "wednesday" pane when this tree's seat IS $SEAT (the mini, 2026-09-13). An
    +  # absent coordinator pane is not fatal here — the check is simply skipped.
    +  wpane=$(coord_pane_id "$FLEET" 2>/dev/null || true)
       if [ -n "$wpane" ] && "$TMUX_BIN" capture-pane -t "$wpane" -p -S -60 2>/dev/null | grep -q 'Context limit reached'; then
         echo "WAKE: pane '$SEAT' DEAD — Context limit reached; the coordinator cannot act — respawn required"; exit 0
       fi
    @@ -154,6 +157,11 @@
         # Skip THIS seat's own coordinator pane (was the literal "wednesday", which
         # left Tuesday waking herself about her own prompt) and the monitor.
         case "$name" in "$SEAT"|fleet-monitor|'') continue;; esac
    +    # …and by PANE ID too (2026-09-13): on the mini the coordinator pane is still
    +    # named "wednesday" while SEAT is tuesday, so the name test above let the
    +    # idle tripwire wake Tuesday about her own prompt. $wpane is whatever
    +    # coord_pane_id resolved this cycle (empty = no coordinator pane found).
    +    [ -n "$wpane" ] && [ "$pid" = "$wpane" ] && continue
         key=$(printf '%s' "$pid" | tr -c 'A-Za-z0-9' '_')
         tail=$("$TMUX_BIN" capture-pane -t "$pid" -p 2>/dev/null | grep -v '^$' | tail -20)
         h=$(printf '%s' "$tail" | shasum | cut -c1-12)

## arm_wake_watch.sh (5 hunks)
- Hunk 1 (@@ -30 @@): derive `PROJECT_DIR`; refuse to arm at all if `seat_resolve.sh` is missing (a runner that cannot resolve its seat would silently tap nothing).
- Hunk 2 (@@ -103 @@): the runner body sources the resolver once and logs `runner seat=…`; the AGENTS count excludes the coordinator by seat name AND legacy name (Studio: `^(wednesday|wednesday|fleet-monitor)$` — same set as before).
- Hunk 3 (@@ -131 @@): DEAD case matches the wake SHAPE (`*"DEAD"*"respawn required"*`, which is what wake_watch prints for any seat) instead of the literal `wednesday`, and invokes `WED_AGENT="$SEAT" …/wednesday_rotate.sh --dead` explicitly.
- Hunk 4 (@@ -142 @@): tap target = `coord_pane_id fleet:0` instead of `grep "^wednesday|"` (the literal is gone: live=2 occurrences, patched=0).
- Hunk 5 (@@ -159 @@): log wording names `$SEAT` and the pane id instead of the literal.

    --- /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/arm_wake_watch.sh	2026-09-02 16:19:06
    +++ /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0f8f9fa8-eada-40b6-ad2d-8c8120bb3b2f/scratchpad/resolver/arm_wake_watch.sh	2026-09-13 20:35:30
    @@ -30,6 +30,8 @@
     
     set -u
     HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    +PROJECT_DIR="$(cd -P "$HERE/../../.." && pwd)"
    +[ -f "$HERE/seat_resolve.sh" ] || { echo "arm_wake_watch: $HERE/seat_resolve.sh missing — the runner cannot resolve the coordinator seat/pane" >&2; exit 2; }
     STATE_DIR="$HERE/state"
     LOG_DIR="$HERE/logs"
     PIDFILE="$STATE_DIR/wake_watch_runner.pid"
    @@ -103,8 +105,18 @@
       # about everything up to it). A refire on an already-read mail costs one
       # tap; a swallowed mail costs a 15-minute fallback. Always err toward refire.
       BASELINE=$(date -u +%Y-%m-%dT%H:%M)   # first arm only: session boot has read everything
    +  # SEAT + coordinator pane (2026-09-13, Tuesday 19:1x finding): this runner used
    +  # to HARDCODE the literal wednesday for the DEAD case and the tap target and
    +  # handed --dead no WED_AGENT, so a dead Tuesday seat could never be respawned.
    +  # The ONE resolver (seat_resolve.sh) now decides: WED_AGENT, else the tree name;
    +  # coord_pane_id accepts the seat name OR the legacy wednesday pane on this seat
    +  # own tree. On the Studio SEAT resolves to wednesday - byte-identical in effect.
    +  . "'"$HERE"'"/seat_resolve.sh || { echo "$(date "+%Y-%m-%d %H:%M:%S") FATAL: seat_resolve.sh missing - runner exiting"; exit 2; }
    +  seat_resolve "'"$PROJECT_DIR"'"
    +  echo "$(date "+%Y-%m-%d %H:%M:%S") runner seat=$SEAT (tree seat $TREE_SEAT)"
       while true; do
    -    AGENTS=$('"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}" 2>/dev/null | grep -vE "^(wednesday|fleet-monitor)$" | grep -c . || true)
    +    # agent panes = everything except the coordinator (by seat name AND the legacy name) and the monitor
    +    AGENTS=$('"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}" 2>/dev/null | grep -vE "^($SEAT|wednesday|fleet-monitor)$" | grep -c . || true)
         if [ "${AGENTS:-0}" -gt 0 ] 2>/dev/null; then N=3; else N=9999; fi
         echo "$(date "+%Y-%m-%d %H:%M:%S") armed: baseline=$BASELINE stable_n=$N agents=$AGENTS"
         OUT=$('"$HERE"'/wake_watch.sh "$BASELINE" "$N" 60 2>&1)
    @@ -131,9 +143,12 @@
           # DEAD coordinator (2026-09-02): do NOT tap a pane that cannot read a tap.
           # Respawn it through wednesday_rotate.sh --dead (which re-checks the
           # literal before killing anything) and give the boot ten minutes.
    -      *"wednesday"*"DEAD"*)
    -        echo "$(date "+%Y-%m-%d %H:%M:%S") DEAD coordinator detected — respawning via wednesday_rotate.sh --dead"
    -        if "'"$HERE"'"/wednesday_rotate.sh --dead >> "'"$LOG"'" 2>&1; then
    +      # 2026-09-13: matched on the wake shape, not the literal wednesday (the
    +      # message names $SEAT), and WED_AGENT=$SEAT is passed EXPLICITLY so the
    +      # rotate script respawns THIS seat with THIS seat launcher.
    +      *"DEAD"*"respawn required"*)
    +        echo "$(date "+%Y-%m-%d %H:%M:%S") DEAD coordinator ($SEAT) detected — respawning via WED_AGENT=$SEAT wednesday_rotate.sh --dead"
    +        if WED_AGENT="$SEAT" "'"$HERE"'"/wednesday_rotate.sh --dead >> "'"$LOG"'" 2>&1; then
               echo "$(date "+%Y-%m-%d %H:%M:%S") respawn issued; waiting 600s for the boot before re-arming"; sleep 600
             else
               echo "$(date "+%Y-%m-%d %H:%M:%S") respawn REFUSED or FAILED (rc=$?) — see rotate_wednesday.log; will re-check next cycle"; sleep 120
    @@ -142,8 +157,9 @@
           *) echo "$(date "+%Y-%m-%d %H:%M:%S") WAKE UNMATCHED by tap case (add a pattern): $OUT"; MSG="" ;;
         esac
         if [ -n "$MSG" ]; then
    -        if '"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}|#{pane_id}" 2>/dev/null | grep -q "^wednesday|"; then
    -          WPANE=$('"$TMUX_BIN"' list-panes -t fleet:0 -F "#{@cockpit_name}|#{pane_id}" 2>/dev/null | grep "^wednesday|" | head -1 | cut -d"|" -f2)
    +        # Tap target = the resolved coordinator pane id (seat name, else the guarded legacy name) - 2026-09-13
    +        WPANE=$(coord_pane_id fleet:0 2>/dev/null || true)
    +        if [ -n "$WPANE" ]; then
               # KAM-TYPING GUARD (2026-08-12): the tap presses Enter in the
               # wednesday pane — if Kam is mid-typing there, it SUBMITS his
               # half-written message (happened twice today, both truncated at the
    @@ -159,18 +175,18 @@
                   LC_ALL=C perl -pe "s/\x1b\[2m.*?(?=\x1b|\$)//g; s/\x1b\[[0-9;]*m//g; s/\xc2\xa0/ /g; s/^.*\xe2\x9d\xaf//" 2>/dev/null | tr -d "[:space:]")
                 [ -z "$PTXT" ] && break
                 TRIES=$((TRIES + 1))
    -            echo "$(date "+%Y-%m-%d %H:%M:%S") tap held - text at wednesday prompt (try $TRIES/20)"
    +            echo "$(date "+%Y-%m-%d %H:%M:%S") tap held - text at $SEAT prompt (try $TRIES/20)"
                 sleep 30
               done
               if [ -n "$PTXT" ]; then
                 echo "$(date "+%Y-%m-%d %H:%M:%S") WAKE LOG-ONLY (prompt still occupied after 10 min): $MSG"
               else
                 '"$TMUX_BIN"' send-keys -t "$WPANE" -l "$MSG" && '"$TMUX_BIN"' send-keys -t "$WPANE" Enter \
    -              && echo "$(date "+%Y-%m-%d %H:%M:%S") tapped wednesday pane $WPANE" \
    -              || echo "$(date "+%Y-%m-%d %H:%M:%S") FAILED to tap wednesday pane"
    +              && echo "$(date "+%Y-%m-%d %H:%M:%S") tapped $SEAT pane $WPANE" \
    +              || echo "$(date "+%Y-%m-%d %H:%M:%S") FAILED to tap $SEAT pane $WPANE"
               fi
             else
    -          echo "$(date "+%Y-%m-%d %H:%M:%S") no wednesday pane — WAKE logged only"
    +          echo "$(date "+%Y-%m-%d %H:%M:%S") no $SEAT coordinator pane (nor an adoptable legacy wednesday pane) — WAKE logged only"
             fi
             sleep 120   # give the session time to read before re-arming
         fi

## NOT built — the (b) half, proposed for cockpit.sh (outside this brief's deliverables)
The pane's name at CREATION comes from `cockpit.conf` line `wednesday|bash "${PROJECT_DIR}/Launch_Wednesday.command"`, read by `cockpit.sh up` (live lines 150-153), not from `Launch_Cockpit.command`. To name pane 0 after the seat where the launcher knows it, the smallest change is in `cockpit.sh up`, first-entry branch:

    -          "$TMUX_BIN" set-option -p -t "$pid" @cockpit_name "$name"
    +          # coordinator pane = the SEAT's name (WED_AGENT, else the tree name), so both
    +          # machines resolve it the same way; the legacy conf name "wednesday" still works
    +          . "$SCRIPT_DIR/seat_resolve.sh"; seat_resolve "$PROJECT_DIR"
    +          [ "$name" = wednesday ] && name="$SEAT"
    +          "$TMUX_BIN" set-option -p -t "$pid" @cockpit_name "$name"

Three other literal-`wednesday` readers would then need the same seat-or-legacy treatment before the rename is safe on the mini: `cockpit.sh apply_layout` (line 90, swaps the `wednesday` pane to the left column), `cockpit.sh rotate` (line 389, refuses only `rotate wednesday`), and `Launch_Cockpit.command:104` (AGENTS list excludes only `wednesday`). Until then, the legacy fallback in `coord_pane_id` carries the mini; the rotate script's post-respawn rename (`@cockpit_name "$SEAT"`) already flips it to `tuesday` after one rotation.
