#!/bin/zsh
# redis_fake_search.sh — READ-ONLY: is there a loopback Redis fake in the repo at head (for A3's real-client leg)? git grep at the head SHA + a node_modules listing.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; H=cbe29597d11e59f2e1a14519e9ba3dbf6de9a756
echo "redis_fake_search $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "net.createServer / require(net) in Blockchain/Dev (non node_modules), -c per file:"; git -C "$R" grep -c -e 'net\.createServer' -e "require('net')" "${H}" -- 'Blockchain/Dev' ':!**/node_modules/**'; echo "  (rc $? — git grep prints nothing and rc 1 for zero)"
echo "control: 'from .net.' import lines (type imports), count of files:"; git -C "$R" grep -l -e "from 'net'" "${H}" -- 'Blockchain/Dev' ':!**/node_modules/**' | wc -l
echo "RESP literals '+OK' followed by CRLF escape, '+PONG':"; git -C "$R" grep -n -F -e '+OK\r\n' -e "'+PONG" "${H}" -- 'Blockchain/Dev'; echo "  (rc $?)"
echo "PONG anywhere in Blockchain/Dev (-c per file):"; git -C "$R" grep -c -e 'PONG' "${H}" -- 'Blockchain/Dev'
echo "ioredis-mock / redis-memory-server / redis-server in any package.json at head:"; git -C "$R" grep -n -i -e 'ioredis-mock' -e 'redis-memory-server' -e '"redis-server"' "${H}" -- '**/package.json'; echo "  (rc $?)"
echo "control: ioredis in api-gateway package.json:"; git -C "$R" grep -n -i -e '"ioredis"' "${H}" -- 'Blockchain/Dev/services/api-gateway/package.json'
echo "Dev/node_modules entries matching -i redis:"; ls "$R/Blockchain/Dev/node_modules" | /usr/bin/grep -i redis
echo "end $(date '+%H:%M:%S %Z')"
