#!/bin/bash
# session_start_compact.sh — SessionStart hook, matcher "compact" (built
# 2026-08-10, working-rhythm §4). If a session ever comes back from an
# emergency compaction despite the PreCompact block, its context is summaries
# of summaries — re-ground it immediately from disk. stdout from a
# SessionStart hook is injected into the session's context.
#
# Wired in .claude/settings.local.json (Wednesday project only). The matcher
# does the filtering; this script just emits the pointer.

set -u
cat > /dev/null   # consume the hook payload
echo "Context was compacted. Re-ground: read CLAUDE.md boot ritual + today's 0_Brain/daily/ note before continuing."
exit 0
