#!/bin/bash
# latest_models.sh -- newest Claude model ID per level (Opus/Sonnet/Haiku/Fable) from a
# LIVE source -> 0_Brain/dashboard/data/models_latest.json (Kam 2026-10-09: always choose the
# best model at its level). rc 0 ok | 3 no live source / required level missing | 4 sanity refusal.
# Source order: Models API (if ANTHROPIC_API_KEY present) -> public docs overview page.
# Failure keeps the previous JSON and prints its age. Details: latest_models.py header.
exec python3 -I "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/latest_models.py" "$@"
