#!/bin/sh
# statusline.sh — Claude Code statusLine for this dev workspace.
#
# Reads a JSON blob from stdin (as Claude Code invokes statusLine commands)
# and emits a single line of the form:
#
#   [Client/Project] Opus 4.7 (1M context) | <branch-or-empty> | ctx:18% | azure:- | 7d:14% renews:3d 23h
#
# Intended to replace ~/.claude/statusline-command.sh for launched project
# sessions — each project launcher writes a .claude/settings.local.json that
# points at this script with the project's label as arg 1.
#
# Design notes:
#   - context_window.* and rate_limits.seven_day.* are provided by Claude
#     Code itself in the stdin JSON — no external API calls needed for those.
#   - `az account show` IS an external call; cached to /tmp for 60s so the
#     status line stays snappy on refresh.
#   - Optional segments append only when their data is present.

set -u

LABEL="${1:-${LABEL:-[session]}}"

input=$(cat)

# Model display name (e.g. "Opus 4.8")
model=$(printf '%s' "$input" | jq -r '.model.display_name // .model.id // empty')

# Thinking / reasoning mode shown right after the model ("Opus 4.8 | Ultrathink").
# Prefer a value Claude Code passes in the JSON; else derive from the session's
# MAX_THINKING_TOKENS / effortLevel (set per-project in .claude/settings*.json).
# Claude Code passes the effort as either a string ("high") or an object
# ({"level":"high"}) — extract the scalar level either way (don't dump the JSON).
level=$(printf '%s' "$input" | jq -r '(.effort // .thinking_mode // .model.effort // .reasoning_effort) as $e | (if ($e|type)=="object" then ($e.level // $e.effort) else $e end) // empty' 2>/dev/null)
case "$(printf '%s' "$level" | tr '[:upper:]' '[:lower:]')" in
  xhigh|ultra*|high) thinking="Ultrathink" ;;
  medium)            thinking="Think hard" ;;
  low|minimal)       thinking="Think" ;;
  *)                 thinking="" ;;
esac
if [ -z "$thinking" ]; then
  mtt="${MAX_THINKING_TOKENS:-}"
  if [ -n "$mtt" ] && [ "$mtt" -gt 0 ] 2>/dev/null; then
    if   [ "$mtt" -ge 30000 ] 2>/dev/null; then thinking="Ultrathink"
    elif [ "$mtt" -ge 10000 ] 2>/dev/null; then thinking="Think harder"
    elif [ "$mtt" -ge 4000 ]  2>/dev/null; then thinking="Think hard"
    else thinking="Think"
    fi
  fi
fi
[ -z "$thinking" ] && thinking="-"

# Context usage percentage (pre-calculated by Claude Code; null before first API call)
used_pct=$(printf '%s' "$input" | jq -r '.context_window.used_percentage // empty')
if [ -n "$used_pct" ]; then
  used_pct_fmt=$(printf "%.0f" "$used_pct")
  ctx_str="ctx:${used_pct_fmt}%"
else
  ctx_str="ctx:-"
fi

# Context compaction hint when usage climbs — mirrors ~/.claude/statusline-command.sh
ctx_total=$(printf '%s' "$input" | jq -r '.context_window.total // empty')
ctx_used=$(printf '%s' "$input" | jq -r '.context_window.used // empty')
renew_str=""
if [ -n "$used_pct" ] && [ -n "$ctx_total" ] && [ -n "$ctx_used" ]; then
  used_int=$(printf "%.0f" "$used_pct")
  if [ "$used_int" -ge 90 ]; then
    renew_str="renew:imminent"
  elif [ "$used_int" -ge 70 ]; then
    renew_str="renew:soon"
  elif [ "$used_int" -ge 50 ]; then
    renew_str="renew:~later"
  fi
fi

# Weekly plan usage + countdown to plan reset
week_pct=$(printf '%s' "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
week_resets=$(printf '%s' "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')
week_str=""
if [ -n "$week_pct" ]; then
  week_pct_fmt=$(printf "%.0f" "$week_pct")
  if [ -n "$week_resets" ]; then
    now_ts=$(date +%s)
    secs_left=$((week_resets - now_ts))
    if [ "$secs_left" -le 0 ]; then
      countdown="renews now"
    else
      days_left=$((secs_left / 86400))
      hours_left=$(( (secs_left % 86400) / 3600 ))
      mins_left=$(( (secs_left % 3600) / 60 ))
      if [ "$days_left" -gt 0 ]; then
        countdown="${days_left}d ${hours_left}h"
      elif [ "$hours_left" -gt 0 ]; then
        countdown="${hours_left}h ${mins_left}m"
      else
        countdown="${mins_left}m"
      fi
    fi
    week_str="7d:${week_pct_fmt}% renews:${countdown}"
  else
    week_str="7d:${week_pct_fmt}%"
  fi
fi

# Azure account — cached to keep the status line fast
azure_cache="/tmp/.claude_azure_user_cache"
azure_ts_cache="/tmp/.claude_azure_user_ts"
now=$(date +%s)
last_ts=0
if [ -f "$azure_ts_cache" ]; then
  last_ts=$(cat "$azure_ts_cache" 2>/dev/null || echo 0)
fi
age=$((now - last_ts))
if [ "$age" -ge 60 ] || [ ! -f "$azure_cache" ]; then
  az_user=$(timeout 5 az account show --query user.name -o tsv 2>/dev/null || true)
  if [ -n "$az_user" ]; then
    printf "%s" "$az_user" > "$azure_cache"
  else
    printf "" > "$azure_cache"
  fi
  printf "%s" "$now" > "$azure_ts_cache"
else
  az_user=$(cat "$azure_cache" 2>/dev/null || true)
fi
if [ -n "$az_user" ]; then
  azure_str="azure:${az_user}"
else
  azure_str="azure:-"
fi

# Base line: "[Client/Project] Model | Thinking | ctx:X%"
# (git-branch segment removed 2026-06-05 per Kam — noisy, low value.)
# Azure is appended LAST so it sits at the tail of the line.
line=$(printf "%s %s | %s | %s" \
  "$LABEL" "$model" "$thinking" "$ctx_str")

# Optional mid-line segments (only when data is available)
[ -n "$renew_str" ]   && line="${line} | ${renew_str}"
[ -n "$week_str" ]    && line="${line} | ${week_str}"

# Env-driven extras (the global script's convention — keep them)
[ -n "${PORT:-}" ]        && line="${line} | local:localhost:${PORT}"
if [ -n "${DEV_URL:-}" ]; then
  line="${line} | dev:${DEV_URL}"
elif [ -n "${DEV_HOST:-}" ]; then
  line="${line} | dev:${DEV_HOST}"
fi
if [ -n "${STAGING_URL:-}" ]; then
  line="${line} | staging:${STAGING_URL}"
elif [ -n "${DEMO_URL:-}" ]; then
  line="${line} | staging:${DEMO_URL}"
fi

# Azure last — always present (shows `azure:-` when not logged in).
line="${line} | ${azure_str}"

printf "%s" "$line"
