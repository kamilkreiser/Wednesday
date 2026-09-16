#!/bin/bash
# READ-ONLY git reads (show / diff / ls-tree / ls-remote / for-each-ref) against the Secuura checkout for the #1002
# drafter. No write verb, no checkout, no fetch. Usage: git_read.sh <gateset dir>
set -u
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
G="${1:?gateset dir}"
B=80686962828197acf305e4010a2ed5b401285743
H=a376756aba1e1ae32c49ed47ba057fd80c7ed136
D=5b4f38a48aeb40c2295895aaa5cd08e273aa7a08
V=Blockchain/Dev/services/api-gateway/src/routes/verification.ts
echo "read at $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "## checkout bounds (read verbs)"
echo "porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ')"
echo "config_sha $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1)"
echo "for_each_ref $(git -C "$R" for-each-ref | wc -l | tr -d ' ')"
echo "## ls-remote"
git -C "$R" ls-remote origin refs/heads/develop refs/heads/feature/ks-1123-ornith-verify-status-pins
echo "## base..head raw (whole tree, no renames)"
git -C "$R" diff --raw --no-renames "$B" "$H"
git -C "$R" diff --numstat --no-renames "$B" "$H"
echo "## head parent"
git -C "$R" rev-parse "$H^" "$H^@"
echo "## base..develop raw (the develop move)"
git -C "$R" diff --raw --no-renames "$B" "$D"
git -C "$R" log --format='%H %P %cI %s' "$B..$D"
echo "## merge-base head develop"
git -C "$R" merge-base "$H" "$D"
echo "## blob shas of the 3 files at base / head / develop"
for f in "$V" Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-f2-anchor-failed-stale-confidence.test.ts Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts; do
  for c in "$B" "$H" "$D"; do echo "$(git -C "$R" rev-parse "$c:$f" 2>/dev/null || echo ABSENT) ${c:0:9} $f"; done
done
echo "## F1/P1 citations at base 80686962: anchoring index.ts :1590-1600, migrations 001:710-716, 003:24-28"
git -C "$R" show "$B:Blockchain/Dev/services/anchoring/src/index.ts" | sed -n '1588,1602p' | cat -n | sed 's/^ *\([0-9]*\)/L+\1/'
echo "-- grep status: anchor.status in anchoring index.ts at base"
git -C "$R" show "$B:Blockchain/Dev/services/anchoring/src/index.ts" | /usr/bin/grep -n -i 'status: anchor.status'
echo "-- grep formatAnchorResponse in anchoring index.ts at base"
git -C "$R" show "$B:Blockchain/Dev/services/anchoring/src/index.ts" | /usr/bin/grep -n -i 'function formatAnchorResponse'
for m in 001 003; do
  p="$(git -C "$R" ls-tree -r --name-only "$B" -- Blockchain/Dev/services/anchoring/migrations 2>/dev/null | /usr/bin/grep -i "/${m}_" | head -1)"
  [ -z "$p" ] && p="$(git -C "$R" ls-tree -r --name-only "$B" | /usr/bin/grep -i "migrations/${m}_" | head -3 | tr '\n' ' ')"
  echo "-- migration $m path(s): $p"
done
echo "## anchor counts in the head verification.ts (fixed strings)"
git -C "$R" show "$H:$V" > "$G/verification.head.ts"
git -C "$R" show "$B:$V" > "$G/verification.base.ts"
for a in \
  "const persistedStatus = (doc as any).blockchain?.status ?? null;" \
  ": persistedStatus == null && persistedConfidence === 'pending-onchain'" \
  "(persistedStatus === 'confirmed' || persistedStatus == null)," \
  "status: latest.status," \
  ": confidenceForAnchorStatus(persistedStatus) === 'pending-onchain'" \
  "persistedStatus === 'confirmed' || " \
  "persistedStatus == null" \
  "(line 265)" \
  "index.ts:1503" \
  "index.ts:1596" \
  "BACKLOG #G6"; do
  echo "head=$(/usr/bin/grep -c -F -- "$a" "$G/verification.head.ts") base=$(/usr/bin/grep -c -F -- "$a" "$G/verification.base.ts")  <$a>"
done
echo "-- positive control (a known single line): head=$(/usr/bin/grep -c -F 'export function confidenceForAnchorStatus(' "$G/verification.head.ts")"
echo "## line numbers at head / base of the load-bearing lines"
for a in "?? null;" "persistedStatus == null && persistedConfidence" "|| persistedStatus == null)," "status: latest.status," "function makeFetchDocFromAnchorStore" "BACKLOG #G6"; do
  echo "head: $(/usr/bin/grep -n -F -- "$a" "$G/verification.head.ts" | cut -d: -f1 | tr '\n' ' ') base: $(/usr/bin/grep -n -F -- "$a" "$G/verification.base.ts" | cut -d: -f1 | tr '\n' ' ') <$a>"
done
echo "## stale line refs inside the new test files (head numbering check)"
for f in ks1123-f2-anchor-failed-stale-confidence ks1123-f3-empty-status-is-off-chain; do
  git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/src/__tests__/$f.test.ts" | /usr/bin/grep -n -i -E '(line [0-9]+|:[0-9]{3})' | sed "s/^/$f: /"
done
echo "## existing api-gateway cells that name an empty / 0 / false status (census at head)"
git -C "$R" grep -n -i -E "status: ?(''|\"\"|0|false)[,} ]" "$H" -- Blockchain/Dev/services/api-gateway/src/__tests__ | head -40
echo "-- control (status: 'confirmed' hits): $(git -C "$R" grep -c -i "status: 'confirmed'" "$H" -- Blockchain/Dev/services/api-gateway/src/__tests__ | wc -l | tr -d ' ') files"
echo "## tsconfig exclude"
git -C "$R" show "$H:Blockchain/Dev/services/api-gateway/tsconfig.json"
echo "## #1001 test cell count at develop"
git -C "$R" show "$D:Blockchain/Dev/services/api-gateway/src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts" | /usr/bin/grep -c -E "^\s*(it|test)(\.each)?\("
echo "## bounds again"
echo "porcelain $(git -C "$R" --no-optional-locks status --porcelain | wc -l | tr -d ' ') config_sha $(shasum -a 256 "$R/.git/config" | cut -d' ' -f1) for_each_ref $(git -C "$R" for-each-ref | wc -l | tr -d ' ')"
echo "done at $(date '+%H:%M:%S %Z')"
