#!/bin/bash
export GH_CONFIG_DIR="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config"
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0="http.https://github.com/.extraheader" GIT_CONFIG_VALUE_0="Authorization: Basic $(printf 'x-access-token:%s' "$(gh auth token)" | base64)"
F=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatS78-hono-core; C=$F/clone2
git -C $C show origin/develop:.claude/skills/secuura-test-discipline/SKILL.md | sed -n 478,486p | cut -c1-600
