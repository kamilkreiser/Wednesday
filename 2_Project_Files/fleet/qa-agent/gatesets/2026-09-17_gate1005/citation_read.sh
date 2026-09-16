#!/bin/zsh
# citation_read.sh — READ-ONLY: do the citations in #1005's rewritten comments hold at the head object? (git show, never the worktree)
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'; H=e5e7ff99dbc4881784ce0beacefb4e7e36c55cf9; D=Blockchain/Dev
echo "citation_read $(date '+%Y-%m-%d %H:%M:%S %Z') at $H"
echo "--- anchoring/src/index.ts:1590-1598 (formatAnchorResponse; comment cites :1596 status: anchor.status)"
git -C "$R" show $H:$D/services/anchoring/src/index.ts | awk 'NR>=1573&&NR<=1575 || NR>=1592&&NR<=1598 {printf "%d\t%s\n", NR, $0}'
echo "--- migrations 001:714 and 003:26"
git -C "$R" show $H:$D/migrations/001_initial-schema.sql | awk 'NR==714 {printf "001:%d\t%s\n", NR, $0}'
git -C "$R" show $H:$D/migrations/003_consolidate-anchors.sql | awk 'NR==26 {printf "003:%d\t%s\n", NR, $0}'
echo "--- the status column in the schema the containers build (docker/init) and azure init.sql — does any declare status NULLABLE?"
for f in docker/init/01-schema.sql docker/init/03-service-tables.sql docker/init/06-consolidate-anchors.sql deployment/azure/migrate/init.sql; do
  git -C "$R" show $H:$D/$f | awk -v F=$f '/CREATE TABLE IF NOT EXISTS anchor_store/ {on=1} on && /status/ {printf "%s:%d\t%s\n", F, NR, $0; on=0}'
done
echo "--- the statusless producers the block counts: documentRepo.ts seeded demo docs :790/:818/:846/:886 (blockchain blobs) and the retry route documents.ts:1313-1322"
P=$(git -C "$R" ls-tree -r --name-only $H -- $D/services/originate/src | /usr/bin/grep -i 'documentRepo.ts$'); echo "documentRepo path: $P"
git -C "$R" show $H:$P | awk 'NR>=788&&NR<=792 || NR>=816&&NR<=820 || NR>=844&&NR<=848 || NR>=884&&NR<=888 {printf "%d\t%s\n", NR, $0}'
git -C "$R" show $H:$D/services/originate/src/routes/documents.ts | awk 'NR>=1311&&NR<=1324 {printf "documents.ts:%d\t%s\n", NR, $0}'
echo "--- gateway response: source expression line at head (I-1 cited :752 on #1002's head)"
git -C "$R" show $H:$D/services/api-gateway/src/routes/verification.ts | awk '/source: liveTxHash/ {printf "verification.ts:%d\t%s\n", NR, $0}'
echo "--- does the verify response expose _source or _lookupSource? (control: the same awk finds verificationConfidence)"
git -C "$R" show $H:$D/services/api-gateway/src/routes/verification.ts | awk 'NR>=732&&NR<=761 && (/_source|_lookupSource/) {print "EXPOSED:", NR, $0} NR>=732&&NR<=761 && /verificationConfidence/ {print "control found:", NR}'
echo "--- every reader of _lookupSource (handler-owned tier marker)"
git -C "$R" grep -n -w -F '_lookupSource' $H -- $D ':!**/node_modules/**' ':!**/dist/**' | sed "s/^$H://" | cut -c1-200
echo "--- composeHonestBlockchainBlob: does originate's blockchain blob ever gain a doc-level key? (it is spread INSIDE blockchain: {...})"
git -C "$R" grep -n -F 'composeHonestBlockchainBlob' $H -- $D/services/originate/src ':!**/__tests__/**' | sed "s/^$H://" | cut -c1-200
