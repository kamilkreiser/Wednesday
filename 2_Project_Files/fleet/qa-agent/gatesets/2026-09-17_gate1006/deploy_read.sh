#!/bin/zsh
# deploy_read.sh — READ-ONLY census: where demo-service is built/deployed/proxied, so a response change's reach is
# READ, not assumed (brief Q9). git grep at head, read verbs only. Every count is paired with a positive control.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=86fe59e6bf07108142fb3dbd06bef8747d2a4687
echo "deploy_read $(date '+%Y-%m-%d %H:%M:%S %Z') at head $H"
echo "--- A. config/deploy files naming demo-service (compose, deployment/, workflows, nginx, bicep, k8s, scripts) — excluding src/ and docs/"
git -C "$R" grep -n -I -F -i 'demo-service' "$H" -- ':!*/src/*' ':!*node_modules*' ':!*.md' ':!docs/*' ':!*package-lock.json' ':!*/dist/*' > /tmp/claude-501/deploy_read_A.txt 2>&1
echo "A count $(wc -l < /tmp/claude-501/deploy_read_A.txt | tr -d ' ')"
cat /tmp/claude-501/deploy_read_A.txt | cut -c1-260
echo "--- A positive control: the same instrument finds the demo-service Dockerfile's own directory name in its package.json (expect >=1)"
git -C "$R" grep -c -I -F -i 'demo-service' "$H" -- 'Blockchain/Dev/services/demo-service/package.json'
echo "--- B. port 4030 / demo-api in compose + deploy + gateway + nginx (non-test)"
git -C "$R" grep -n -I -E '4030|/demo-api' "$H" -- '*docker-compose*' '*compose*.yml' '*compose*.yaml' 'Blockchain/Dev/deployment/*' 'Blockchain/Dev/services/api-gateway/src/*' '*nginx*' '*.bicep' '.github/*' ':!*__tests__*' ':!*node_modules*' 2>&1 | cut -c1-260
echo "--- B positive control: app.ts's own health comment names 4030 (expect 1)"
git -C "$R" grep -c -I -F '4030' "$H" -- 'Blockchain/Dev/services/demo-service/src/app.ts'
echo "--- C. NODE_ENV set for demo-service in compose/deploy (KS-658: the demo VM runs development)"
git -C "$R" grep -n -I -E -A12 '^\s*demo-service:' "$H" -- '*compose*.yml' '*compose*.yaml' 2>&1 | /usr/bin/grep -i -E 'demo-service:|NODE_ENV|image|build|profiles|ports|environment|DEMO_SERVICE_ENABLED' | cut -c1-240
echo "--- D. frontend callers of /demo-api (who reads the response)"
git -C "$R" grep -n -I -F '/demo-api' "$H" -- 'Blockchain/Dev/frontend/*' ':!*node_modules*' ':!*/dist/*' ':!*__tests__*' 2>&1 | cut -c1-220 | head -40
echo "--- E. rejectControlBytes body (does it answer or next(err)?)"
git -C "$R" show "$H:Blockchain/Dev/packages/shared/src/middleware/index.ts" | awk '/export function rejectControlBytes/{p=1} p{print NR": "$0; n++} n>45{exit}'
