export GIT_OPTIONAL_LOCKS=0
D=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_drafter-seatB172
C=$D/clone
echo "--- proxy.ts api/rewards on develop"
git -C $C show origin/develop:Blockchain/Dev/services/api-gateway/src/routes/proxy.ts | grep -n 'api/rewards' | head -5
echo "--- 2079 importer regex hit files (develop 9105 / 410feda)"
for r in origin/develop 410feda1a85e; do echo $r $(git -C $C grep -l -E 'redis-security-store|redis-client|cache-middleware|connection-pool|security:bruteforce' $r | wc -l); done
git -C $C grep -l -E 'redis-security-store|redis-client|cache-middleware|connection-pool|security:bruteforce' origin/develop | sed 's#^origin/develop:##' | sort > $D/imp_dev.txt
git -C $C grep -l -E 'redis-security-store|redis-client|cache-middleware|connection-pool|security:bruteforce' 410feda1a85e | sed 's#^410feda1a85e:##' | sort > $D/imp_410.txt
echo diff-lines: $(diff $D/imp_dev.txt $D/imp_410.txt | wc -l)
echo "positive control resolveDocumentType in enforcement.ts: $(git -C $C grep -c resolveDocumentType origin/develop -- Blockchain/Dev/services/api-gateway/src/services/enforcement.ts)"
echo "--- fragments dir entry counts at develop"
echo flow $(git -C $C ls-tree --name-only origin/develop 'Projects Documents/fragments/flow/' | wc -l) cheat $(git -C $C ls-tree --name-only origin/develop 'Projects Documents/fragments/cheat/' | wc -l)
echo "--- enforcement.ts line 55 and 154 on develop"
git -C $C show origin/develop:Blockchain/Dev/services/api-gateway/src/services/enforcement.ts | sed -n '55p;154p'
echo "--- squashes since 410feda1a85e (gate 345 develop)"
echo count $(git -C $C rev-list --count 410feda1a85e..origin/develop)
git -C $C diff --name-only 410feda1a85e origin/develop | wc -l
echo "--- 2134 test file now on develop: it count"
git -C $C show origin/develop:Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts | grep -c -E "^\s*(it|test)\("
echo "--- history top"
H=/Volumes/DevMASTER/\!CODING/Secuura/Blockchain/5_Project_History/history.md
/usr/bin/grep -a -n -m5 '^## ' "$H" | cut -c1-120
echo "headings: $(/usr/bin/grep -a -c '^## ' "$H")  B171: $(/usr/bin/grep -a '^## ' "$H" | /usr/bin/grep -a -c 'Seat B 171st')  B172: $(/usr/bin/grep -a '^## ' "$H" | /usr/bin/grep -a -c 'Seat B 172nd')  R118: $(/usr/bin/grep -a '^## ' "$H" | /usr/bin/grep -a -c 'Seat R 118th')  S77: $(/usr/bin/grep -a '^## ' "$H" | /usr/bin/grep -a -c 'Seat S 77th')"
df -g /Volumes/DevMASTER | tail -1; uptime
