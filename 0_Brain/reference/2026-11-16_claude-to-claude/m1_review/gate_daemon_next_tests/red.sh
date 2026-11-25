#!/bin/bash
export RED_ONLY='^(guard_line_panics|relay_url_untrimmed|relay_flag_empty_accepted|connect_reason_empty|pin_mismatch_dropped|identity_field_never_set|dead_relay_invite_old_text|help_no_cmd_prompt_line|refill_keeps_spent_clock|mcp_type_defaults|no_retransmit_timer|relay_orphan)$'
W=/private/tmp/claude-501/qdnx
echo "start $(date '+%F %T')"; t0=$(date +%s)
bash $W/r.sh $W/c $W/t bash scripts/red-controls-daemon.sh
rc=$?; echo "red exit=$rc ($(( $(date +%s)-t0 )) s) end $(date '+%T')"
