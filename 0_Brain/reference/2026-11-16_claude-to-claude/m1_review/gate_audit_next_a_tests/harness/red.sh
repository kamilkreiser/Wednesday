#!/bin/bash
W=/private/tmp/claude-501/qana
date "+start %F %T"; git -C $W/c rev-parse HEAD; echo "status lines: $(git -C $W/c status --short | wc -l)"
echo "heavy counter: $(bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh)"
ps -axo pid,command | grep red-controls-daemon | grep -v grep
RED_ONLY='^(audit_always_on|recreate_on_restore|record_causer_always_local|record_full_raw|nothing_to_seal_retried|limits_changed_read_as_done|landed_unknown_retried|commit_failed_retried_blind|seal_err_retried|seal_on_peer_message|seal_error_ends_the_engine|segment_before_falls_back|creation_reason_overwritten|row11_text_before_reopen|member_less_never_reopened|nothing_text_guessed)$' \
  bash $W/r.sh $W/c $W/tr bash scripts/red-controls-daemon.sh
echo "exit=$?"; date "+end %F %T"
