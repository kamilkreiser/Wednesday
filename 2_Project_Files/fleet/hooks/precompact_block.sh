#!/bin/bash
# precompact_block.sh — PreCompact hook for the Wednesday project (built
# 2026-08-10, working-rhythm §4: compaction is a failure mode, not a feature).
#
# Auto-compaction = summaries of summaries. Blocking it converts silent
# degradation into a forced rotation: wrap and rotate instead. Exit code 2 on
# a PreCompact hook blocks the compaction and shows stderr to the user
# (documented Claude Code hook contract; exercised directly at build time —
# the block-on-real-compaction path is only provable in a live session).
#
# Wired in .claude/settings.local.json (this project only — hard rule 1
# forbids installing it for other projects; they adopt via their own sessions).

set -u
cat > /dev/null   # consume the hook payload; we block unconditionally
echo "Compaction blocked by working-rhythm §4: wrap and rotate instead (0_Brain/skills/working-rhythm.md)" >&2
exit 2
