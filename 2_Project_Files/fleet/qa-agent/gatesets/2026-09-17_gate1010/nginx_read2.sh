#!/bin/zsh
# nginx_read2.sh — READ-ONLY follow-up: the /api/ location bodies, demo's aggregate-ceiling comment, the Azure bicep ingress, frontend proxy blocks.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=c3213b04e3ad96068c367f7e0ba426822d32cda9
N=Blockchain/Dev/docker/nginx-gateway
echo "nginx_read2 $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "## nginx.conf 176-205"; git -C "$R" show $H:$N/nginx.conf | sed -n '176,205p' | cat -n | sed 's/^/  +175 /'
echo "## nginx-demo.conf 214-232"; git -C "$R" show $H:$N/nginx-demo.conf | sed -n '214,232p'
echo "## nginx-demo.conf 405-420"; git -C "$R" show $H:$N/nginx-demo.conf | sed -n '405,420p'
echo "## nginx-production.conf 340-352"; git -C "$R" show $H:$N/nginx-production.conf | sed -n '340,352p'
echo "## issuer nginx.conf 118-140"; git -C "$R" show $H:Blockchain/Dev/frontend/issuer/nginx.conf | sed -n '118,140p'
echo "## bicep: ingress / timeout / targetPort / api-gateway"
for f in main.bicep services.bicep; do git -C "$R" show $H:Blockchain/Dev/deployment/azure/$f | /usr/bin/grep -n -i -E 'ingress|timeout|targetPort|api-gateway|gateway|nginx|external:' | head -30; echo "  ($f)"; done
echo "## docker-compose files naming nginx-production / nginx-demo / nginx.conf (which conf runs where)"
git -C "$R" grep -n -E 'nginx-production\.conf|nginx-demo\.conf|nginx-gateway/nginx\.conf|nginx\.conf:/etc' $H -- '*.yml' '*.yaml' '*Dockerfile*' '*.sh' ':!*node_modules*' | head -20
echo "## originate stub: express server.timeout / requestTimeout / keepAliveTimeout in originate index (READ)"
git -C "$R" grep -n -E 'keepAliveTimeout|headersTimeout|requestTimeout|server\.timeout|setTimeout\(' $H -- Blockchain/Dev/services/originate/src/index.ts | head
echo "## api-gateway: server timeouts in index.ts"
git -C "$R" grep -n -E 'keepAliveTimeout|headersTimeout|requestTimeout|server\.timeout|\.setTimeout\(' $H -- Blockchain/Dev/services/api-gateway/src/index.ts | head
echo "## openapi spec location + census (control ^paths:)"
git -C "$R" ls-tree -r --name-only $H | /usr/bin/grep -E 'openapi.*\.ya?ml$|secuura-api\.ya?ml$' | head
echo "end $(date '+%H:%M:%S %Z')"
