#!/bin/zsh
# consumer_read.sh — READ-ONLY census at the head blob (git grep / git show, read verbs) of who calls the approve route,
# how the route is mounted, the spec, and originate's POST /api/documents. Every count paired with a same-file control.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H=dd7086d5aa574285beffc515f9371a438621f25d
D=Blockchain/Dev
echo "consumer_read $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "--- 1. every line naming workflow-instances at head (whole repo, not only Dev)"
git -C "$R" grep -n 'workflow-instances' "$H" | sed "s/^$H://"
echo "--- 1b. 'approve' near a workflow call in frontends / mcp (grep -n approve in the two consumers)"
git -C "$R" grep -n -i 'approve' "$H" -- "$D/frontend/issuer/src/components/DocumentList.tsx" "$D/services/mcp-server/src/api-client.ts" | sed "s/^$H://"
echo "--- 2. spec: workflow-instances in docs/openapi/*.yaml (count) + control 'paths:'"
for f in $(git -C "$R" ls-tree -r --name-only "$H" -- "$D/docs/openapi" | /usr/bin/grep -E '\.ya?ml$'); do
  n=$(git -C "$R" show "$H:$f" | /usr/bin/grep -c 'workflow-instances'); c=$(git -C "$R" show "$H:$f" | /usr/bin/grep -c '^paths:'); echo "  $f workflow-instances=$n control(^paths:)=$c"
done
echo "--- 3. mount of createVerificationRoutes + authenticateToken definition in api-gateway src (non-test)"
git -C "$R" grep -n -E 'createVerificationRoutes|function authenticateToken|const authenticateToken|authenticateToken =' "$H" -- "$D/services/api-gateway/src" ':!*__tests__*' | sed "s/^$H://"
echo "--- 4. originate POST /api/documents handler location"
git -C "$R" grep -n -E "post\(['\"]/api/documents['\"]|post\(['\"]/['\"]" "$H" -- "$D/services/originate/src" ':!*__tests__*' | sed "s/^$H://"
echo "--- 5. tests that import verification routes (who else constructs the router)"
git -C "$R" grep -l 'routes/verification' "$H" -- "$D/services/api-gateway/src/__tests__" | sed "s/^$H://"
echo "--- 6. nginx /api/ location to api-gateway (count) + control (location count)"
for f in docker/nginx-gateway/nginx.conf docker/nginx-gateway/nginx-demo.conf; do
  n=$(git -C "$R" show "$H:$D/$f" 2>/dev/null | /usr/bin/grep -c -E 'location[[:space:]]+(\^~[[:space:]]+)?/api/[[:space:]]*\{'); c=$(git -C "$R" show "$H:$D/$f" 2>/dev/null | /usr/bin/grep -c 'location'); echo "  $f location /api/ =$n control(location)=$c"
done
echo "--- 7. http.request timeouts in verification.ts at head: 'timeout' count, control 'http.request' count"
echo "  timeout=$(git -C "$R" show "$H:$D/services/api-gateway/src/routes/verification.ts" | /usr/bin/grep -c -i 'timeout') http.request=$(git -C "$R" show "$H:$D/services/api-gateway/src/routes/verification.ts" | /usr/bin/grep -c 'http.request')"
echo "--- 8. setWorkflowInstance before the forward (line numbers at head)"
git -C "$R" show "$H:$D/services/api-gateway/src/routes/verification.ts" | /usr/bin/grep -n -E "instance.status = 'approved'|setWorkflowInstance|resolveStatus|deletePendingDocument|ORIGINATE_FORWARD_FAILED|Workflow already completed"
echo "--- 9. vitest config / tsconfig of api-gateway (exclude)"
git -C "$R" show "$H:$D/services/api-gateway/tsconfig.json"
git -C "$R" ls-tree --name-only "$H" -- "$D/services/api-gateway/" | sed 's#.*/##'
