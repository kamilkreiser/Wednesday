#!/bin/zsh
# consumer_read.sh — #1007 drafter: READ-ONLY census over the drafter's own clone worktree (head tree = merged tree): route mounts,
# auth in front of /system/status, consumers of the route and its services[].url, NODE_ENV=staging in any deploy/config, other
# dead-estate hits. /usr/bin/grep with a same-file positive control.
H=$(python3 -c "import json;print(json.load(open('/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1007/drafter_paths.json'))['trees']['head'])")
D="$H/Blockchain/Dev"
X=(--exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.git --exclude-dir=build --exclude-dir=coverage)
echo "consumer_read $(date '+%Y-%m-%d %H:%M:%S %Z') tree $H"
echo "## control: grep finds getServiceUrl in system-status.ts: $(/usr/bin/grep -c getServiceUrl "$D/services/api-gateway/src/routes/system-status.ts")"
echo "## 1 imports / mounts of system-status (whole repo)"
/usr/bin/grep -rn "${X[@]}" -E "system-status|systemStatus" "$H" | /usr/bin/grep -v '/__tests__/ks864' | head -60
echo "## 2 '/system' and '/status' mounts in api-gateway src/index.ts (with line numbers)"
/usr/bin/grep -n -E "app\.use\(|router|/system|/status|authenticate|requireAuth|requireAdmin|apiKey|rateLimit" "$D/services/api-gateway/src/index.ts" | head -150
echo "## 3 NODE_ENV staging anywhere (repo, excluding node_modules)"
/usr/bin/grep -rn -i "${X[@]}" -E "NODE_ENV[\"' ]*[:=][\"' ]*staging|NODE_ENV.{0,20}staging" "$H" | head -80
echo "## 4 consumers of /system/status (frontends, scripts, specs, tests)"
/usr/bin/grep -rn "${X[@]}" -E "system/status" "$H" | head -80
echo "## 5 ashypond | westeurope | secuura-staging- outside system-status.ts (count per file)"
/usr/bin/grep -rl "${X[@]}" -E "ashypond|westeurope|secuura-staging-" "$H" | while read -r f; do echo "$(/usr/bin/grep -c -E 'ashypond|westeurope|secuura-staging-' "$f") $f"; done | sort -rn | head -60
