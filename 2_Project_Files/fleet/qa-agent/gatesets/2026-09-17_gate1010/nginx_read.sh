#!/bin/zsh
# nginx_read.sh — READ-ONLY: every proxy/ingress config at head c3213b04e that could front the api-gateway, and its read/send/total bounds. git grep by SHA only.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=c3213b04e3ad96068c367f7e0ba426822d32cda9
echo "nginx_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "--- A. timeout directives in any tracked file (case-insensitive), excluding node_modules/lockfiles/tests/.ts/.js/.py/.md"
git -C "$R" grep -n -i -E 'proxy_read_timeout|proxy_send_timeout|proxy_connect_timeout|send_timeout|keepalive_timeout|proxy-read-timeout|proxy-send-timeout|read_timeout|response_header_timeout|timeouts?\s*\{|idle_timeout|client_body_timeout|uwsgi_read_timeout|fastcgi_read_timeout' $H -- ':!*node_modules*' ':!*.lock' ':!*package-lock.json' ':!*.ts' ':!*.tsx' ':!*.js' ':!*.py' ':!*.md' ':!*.go' ':!*.rs' ':!*.sol' 
echo "rc A $?"
echo "--- B. who proxies to the gateway: upstream / proxy_pass / reverse_proxy naming gateway or 3000/api"
git -C "$R" grep -n -i -E 'api_gateway|api-gateway|proxy_pass|reverse_proxy|upstream ' $H -- '*nginx*.conf' '*Caddyfile*' '*.yaml' '*.yml' ':!*node_modules*' ':!*.github*' ':!*openapi*' | /usr/bin/grep -i -E 'proxy_pass|reverse_proxy|upstream|ingress|service:|serviceName|backend' | head -120
echo "--- C. location blocks for /api in the nginx confs"
for f in Blockchain/Dev/docker/nginx-gateway/nginx.conf Blockchain/Dev/docker/nginx-gateway/nginx-demo.conf Blockchain/Dev/docker/nginx-gateway/nginx-production.conf Blockchain/Dev/frontend/admin/nginx.conf Blockchain/Dev/frontend/issuer/nginx.conf Blockchain/Dev/frontend/outlook-addin/nginx.conf Blockchain/Dev/frontend/status/nginx.conf Blockchain/Dev/frontend/verifier/nginx.conf Blockchain/Dev/frontend/website/nginx.conf Tokenomics/nginx.conf; do
  echo "## $f lines $(git -C "$R" show $H:$f | wc -l | tr -d ' ') location-lines $(git -C "$R" show $H:$f | /usr/bin/grep -c 'location') timeout-lines $(git -C "$R" show $H:$f | /usr/bin/grep -c -i 'timeout')"
  git -C "$R" show $H:$f | /usr/bin/grep -n -i -E 'location .*api|proxy_pass|proxy_read_timeout|proxy_send_timeout|proxy_connect_timeout|upstream |server_name|listen ' | head -40
done
echo "--- D. Caddyfile"
git -C "$R" show $H:Blockchain/Dev/deployment/caddy/Caddyfile | /usr/bin/grep -n -i -E 'reverse_proxy|timeout|api|gateway|:[0-9]+' | head -40
echo "--- E. k8s / helm / ingress manifests (names)"
git -C "$R" ls-tree -r --name-only $H | /usr/bin/grep -i -E 'ingress|helm|k8s|kubernetes|charts/|azure.*(yaml|yml|json|bicep)|\.bicep$|appgw|frontdoor|front-door|traefik|haproxy|envoy' | /usr/bin/grep -v node_modules | head -60
echo "--- F. positive control: the seat's cited line"
git -C "$R" show $H:Blockchain/Dev/docker/nginx-gateway/nginx-production.conf | sed -n '280,300p'
echo "end $(date '+%H:%M:%S %Z')"
