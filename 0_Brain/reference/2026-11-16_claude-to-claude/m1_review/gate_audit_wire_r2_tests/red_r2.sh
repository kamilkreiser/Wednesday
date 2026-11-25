#!/bin/bash
W=/private/tmp/claude-501/qaw2
date "+start %F %T"; git -C $W/c rev-parse HEAD; git -C $W/c status --short | wc -l
RED_ONLY='^(audit_always_on|recreate_on_restore|record_causer_always_local|record_full_raw|nothing_to_seal_retried|limits_changed_read_as_done|landed_unknown_retried|commit_failed_retried_blind|seal_err_retried|seal_on_peer_message|seal_error_ends_the_engine|segment_before_falls_back)$' \
  bash $W/r.sh $W/c $W/tr bash scripts/red-controls-daemon.sh
echo "exit=$?"; date "+end %F %T"
