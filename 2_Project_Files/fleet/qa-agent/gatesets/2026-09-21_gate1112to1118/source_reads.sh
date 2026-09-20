#!/bin/bash
# source_reads.sh — READ-ONLY `git show <sha>:<path>` reads in the Secuura checkout at develop 362e51fe0 (every PR's parent AND origin develop
# now — no develop move this round) and at each head, for the lines the gate will measure: the 27 tamper `from` lines with their scope anchors
# (exact-line counts), the new cells' it( titles at each head, the develop cells the three measured covers name (F1 ks1215, F2 ks480-connector-auth,
# F3 readback + ks1284-cardano-metadatum), the T11/T12 source-text guards' targets, the trivy job's :62 line, the pre-push hook's preflight call,
# preflight.sh's skip_stack call sites (the three skipped legs). Nothing written to the checkout. Derived from gatesets/2026-09-21_gate1106to1111/source_reads.sh.
R='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV=362e51fe0db7e73d5557924902763fe3f10fd8c7
HA=3a28d2a3c4d030cb73b7775bb19c5844ce190e56; HB=abf8321a9ca426a1d623a54a41453824dce34def; HC=762a70117c6cf40545f8a4ac5f24708e7fcd91fe
HD=b008489e4fbc72bb8b68cb3bb925557978399780; HE=9a485cfe77406f47103ed6ab65c14ec01144cb68; HG=b3f94f14a0cf3e0236284481b85781417fd233f3
HF=f132c92147b5005c36e405d0116faa541d978a67
D=Blockchain/Dev; A=$D/services/api-gateway; O=$D/services/originate; N=$D/services/anchoring; U=$D/services/auth
g() { git -C "$R" "$@"; }
cnt() { # $1 sha:path, $2 exact line text -> count of exact-line matches
  g show "$1" | /usr/bin/grep -c -x -F -- "$2"
}
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== TAMPER FROM LINES at develop: exact-line count (want 1 each) + the line as read"
while IFS='|' read -r file line text; do
  c=$(cnt "$DEV:$file" "$text"); printf '  count=%s %s:%s | %s\n' "$c" "${file##*/}" "$line" "$(g show "$DEV:$file" | sed -n "${line}p")"
done <<'EOF'
Blockchain/Dev/services/api-gateway/src/services/enforcement.ts|100|  const typeRefRaw = body.documentType || body.type || '';
Blockchain/Dev/services/api-gateway/src/services/enforcement.ts|114|  const typeRef = (typeRefRaw || '') as string;
Blockchain/Dev/services/api-gateway/src/routes/platform.ts|64|const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];
Blockchain/Dev/services/api-gateway/src/routes/platform.ts|97|  if (SUPER_ROLES.includes(user.role)) {
Blockchain/Dev/services/api-gateway/src/middleware/auth.ts|276|    const apiKey = req.headers['x-api-key'] as string | undefined;
Blockchain/Dev/services/api-gateway/src/middleware/auth.ts|279|    if (presentedKey && !meta && required) {
Blockchain/Dev/services/api-gateway/src/middleware/auth.ts|322|      (req as any).connectorMeta = meta;
Blockchain/Dev/services/originate/src/originate.openapi.ts|1740|    action: z.enum(LIFECYCLE_EVENT_ACTIONS).openapi({
Blockchain/Dev/services/originate/src/originate.openapi.ts|1765|    action: z.enum(LIFECYCLE_EVENT_ACTIONS),
Blockchain/Dev/services/anchoring/src/anchorReadback.ts|52|    identity: Object.keys(identity).length > 0 ? identity : null,
Blockchain/Dev/services/anchoring/src/anchorReadback.ts|74|  const explorerBase = ctx.network === 'mainnet'
Blockchain/Dev/services/anchoring/src/anchorReadback.ts|75|    ? 'https://cardanoscan.io/transaction'
Blockchain/Dev/services/anchoring/src/anchorReadback.ts|111|    documentId: sec.documentId || row?.document_id || null,
Blockchain/Dev/services/anchoring/src/anchorReadback.ts|112|    certId: sec.certId || sec.documentId || row?.document_id || null,
Blockchain/Dev/services/anchoring/src/cardano/cardanoMetadatum.ts|81|  return (value as string[]).join('');
Blockchain/Dev/services/anchoring/src/index.ts|890|          ...anchorIdentityView((anchor.metadataPayload as any)?.secuura),
Blockchain/Dev/services/anchoring/src/index.ts|699|        const sec: any = fromCardanoMetadatum(secEntry?.json_metadata?.secuura);
Blockchain/Dev/services/anchoring/src/index.ts|701|        const onChainHash = String(sec.hash || '').replace(/^sha256:/i, '').toLowerCase();
Blockchain/Dev/services/anchoring/src/cardano/transaction.ts|114|  const metadataJson = JSON.stringify(toCardanoMetadatum(metadataPayload));
Blockchain/Dev/services/auth/src/routes/users.ts|1105|    if (user.mfaSecret && !verifyTOTP(user.mfaSecret, code)) {
Blockchain/Dev/services/auth/src/routes/users.ts|1267|    if (targetIndex <= currentIndex) {
EOF
echo "--- 04-container-trivy.sh :60-64 at develop (the :62 grep line; the seat's S5 was a TYPED anchor)"; g show "$DEV:Blockchain/Testing/jobs/04-container-trivy.sh" | sed -n '60,64p'
echo "--- 04-container-trivy.sh: count of lines containing \"grep -E '^dev-\" :"; g show "$DEV:Blockchain/Testing/jobs/04-container-trivy.sh" | /usr/bin/grep -c -F "grep -E '^dev-"
echo "--- positive controls (substring counts at develop): SUPER_ROLES.includes / x-api-key / connectormeta -i / LIFECYCLE_EVENT_ACTIONS / anchorIdentityView / toCardanoMetadatum / verifyTOTP / LEVEL_ORDER / latest"
printf '  SUPER_ROLES.includes %s\n' "$(g show $DEV:$A/src/routes/platform.ts | /usr/bin/grep -c -F 'SUPER_ROLES.includes')"
printf '  x-api-key %s\n' "$(g show $DEV:$A/src/middleware/auth.ts | /usr/bin/grep -c -F 'x-api-key')"
printf '  connectormeta -i %s\n' "$(g show $DEV:$A/src/middleware/auth.ts | /usr/bin/grep -c -i -F 'connectormeta')"
printf '  LIFECYCLE_EVENT_ACTIONS %s\n' "$(g show $DEV:$O/src/originate.openapi.ts | /usr/bin/grep -c -F 'LIFECYCLE_EVENT_ACTIONS')"
printf '  anchorIdentityView (index.ts) %s\n' "$(g show $DEV:$N/src/index.ts | /usr/bin/grep -c -F 'anchorIdentityView')"
printf '  toCardanoMetadatum (transaction.ts) %s\n' "$(g show $DEV:$N/src/cardano/transaction.ts | /usr/bin/grep -c -F 'toCardanoMetadatum')"
printf '  verifyTOTP (users.ts) %s\n' "$(g show $DEV:$U/src/routes/users.ts | /usr/bin/grep -c -F 'verifyTOTP')"
printf '  LEVEL_ORDER (users.ts) %s\n' "$(g show $DEV:$U/src/routes/users.ts | /usr/bin/grep -c -F 'LEVEL_ORDER')"
printf '  latest (04-container-trivy.sh) %s\n' "$(g show $DEV:Blockchain/Testing/jobs/04-container-trivy.sh | /usr/bin/grep -c -F 'latest')"
printf '  tenantId: (security index.ts, a same-file duplicate control from the previous gate) %s\n' "$(g show $DEV:$D/services/security/src/index.ts | /usr/bin/grep -c -F 'tenantId:')"
echo "=== where anchorIdentityView is DEFINED (T11's target; drafter's shape_1 guessed a file that does not exist)"; g grep -n -E 'export (function|const) anchorIdentityView' $DEV -- "$N/src" | sed "s#$DEV:##"
echo "=== the scope anchors (exact-line counts at develop)"
printf '  enforceDocumentTypeRules( : %s\n' "$(g show $DEV:$A/src/services/enforcement.ts | /usr/bin/grep -c -F 'enforceDocumentTypeRules(')"
printf '  requireOrgProvisioner : %s\n' "$(g show $DEV:$A/src/routes/platform.ts | /usr/bin/grep -c -F 'requireOrgProvisioner')"
printf '  export function rowToApiKey( (security index.ts, control from the previous gate): %s\n' "$(g show $DEV:$D/services/security/src/index.ts | /usr/bin/grep -c -F 'export function rowToApiKey(')"
printf '  handleAnchorVerifyByHash : %s\n' "$(g show $DEV:$N/src/index.ts | /usr/bin/grep -c -F 'handleAnchorVerifyByHash')"
printf "  app.get('/api/anchors/:id' : %s\n" "$(g show $DEV:$N/src/index.ts | /usr/bin/grep -c -F "app.get('/api/anchors/:id'")"
echo "--- platform.ts :60-66 and :90-100 at develop"; g show $DEV:$A/src/routes/platform.ts | sed -n '60,66p;90,100p'
echo "--- platform.ts :485-492 (the :489 mount)"; g show $DEV:$A/src/routes/platform.ts | sed -n '485,492p'
echo "--- middleware/auth.ts :270-284 and :318-326"; g show $DEV:$A/src/middleware/auth.ts | sed -n '270,284p;318,326p'
echo "--- users.ts :1100-1108 and :1262-1270"; g show $DEV:$U/src/routes/users.ts | sed -n '1100,1108p;1262,1270p'
echo "--- anchorReadback.ts :48-56, :72-78, :108-114"; g show $DEV:$N/src/anchorReadback.ts | sed -n '48,56p;72,78p;108,114p'
echo "--- cardanoMetadatum.ts :76-84"; g show $DEV:$N/src/cardano/cardanoMetadatum.ts | sed -n '76,84p'
echo "--- anchoring index.ts :695-703 and :886-892"; g show $DEV:$N/src/index.ts | sed -n '695,703p;886,892p'
echo "--- transaction.ts :110-116"; g show $DEV:$N/src/cardano/transaction.ts | sed -n '110,116p'
echo "--- originate.openapi.ts :1738-1742 and :1763-1767"; g show $DEV:$O/src/originate.openapi.ts | sed -n '1738,1742p;1763,1767p'
echo "=== NEW CELLS at each head (it(/test( titles the patches add) — diff lines starting with '+' that carry it( or test("
for pair in "A $HA" "B $HB" "C $HC" "D $HD" "E $HE" "G $HG" "F $HF"; do set -- $pair
  echo "--- PR $1 $2"; g diff $DEV $2 | /usr/bin/grep -E "^\+.*\b(it|test|describe)\(|^\+.*RED KS-|^\+.*CONTROL|^\+.*ok \"|^\+  (pass|ok)\b" | cut -c1-200
done
echo "=== DEVELOP CELLS the three measured covers name (F1 / F2 / F3) — exact titles at develop"
echo "--- F1: ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts (tenant ADMIN 403 cell)"; g show $DEV:$A/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts | /usr/bin/grep -n -F "tenant ADMIN" | cut -c1-220
echo "--- F2: ks480-connector-auth.test.ts (the #1106 INFOEMPTY cell)"; g show $DEV:$A/src/__tests__/ks480-connector-auth.test.ts | /usr/bin/grep -n -F "KS-1232" | cut -c1-220
echo "--- F3: ks1175-anchor-readback.test.ts cells (chain source / CONTROL / absent-identity) at develop"; g show $DEV:$N/src/__tests__/ks1175-anchor-readback.test.ts | /usr/bin/grep -n -E "^\s*(it|test)\(" | cut -c1-200
echo "--- F3: ks1284-cardano-metadatum.test.ts cells at develop"; g show $DEV:$N/src/__tests__/ks1284-cardano-metadatum.test.ts | /usr/bin/grep -n -E "^\s*(it|test)\(" | cut -c1-200
echo "--- anchoring: the pre-existing red (threadTokenMint) — where it lives at develop"; g grep -n -F "deterministic per-seed policyId" $DEV -- "$N/src" | sed "s#$DEV:##" | cut -c1-200
echo "=== identity test at head E: the new cell (it( titles with KS-1175)"; g show $HE:$N/src/__tests__/ks1175-identity-anchoring.test.ts | /usr/bin/grep -n -F "RED KS-1175" | cut -c1-200
echo "=== the three NEW anchoring files at head E: line counts + it( counts"
for f in ks1175-getid-view-wired ks1284-chain-read-order ks1284-attach-point; do printf '  %s lines %s it( %s\n' "$f" "$(g show $HE:$N/src/__tests__/$f.test.ts | wc -l | tr -d ' ')" "$(g show $HE:$N/src/__tests__/$f.test.ts | /usr/bin/grep -c -E "^\s*(it|test)\(")"; done
echo "--- T13 imports / mocks (attach-point) at head E"; g show $HE:$N/src/__tests__/ks1284-attach-point.test.ts | /usr/bin/grep -n -E "import|vi\.mock|buildAnchorTransaction|label" | cut -c1-200 | head -30
echo "--- T11 (getid-view-wired) at head E: what it reads"; g show $HE:$N/src/__tests__/ks1175-getid-view-wired.test.ts | /usr/bin/grep -n -E "readFileSync|index\.ts|anchorIdentityView|app\.get|it\(" | cut -c1-200
echo "--- T12 (chain-read-order) at head E: what it reads"; g show $HE:$N/src/__tests__/ks1284-chain-read-order.test.ts | /usr/bin/grep -n -E "readFileSync|index\.ts|handleAnchorVerifyByHash|fromCardanoMetadatum|it\(|scan\(" | cut -c1-200
echo "=== the trivy suite at head G: the new cell (:140-:160) and the TRIVY_JOB_SH / jq lines"; g show $HG:$D/scripts/__tests__/container_trivy_image_filter.test.sh | /usr/bin/grep -n -E "TRIVY_JOB_SH|jq|KS-1137|KS-867|dev-auth2|dev-m365" | cut -c1-200
echo "=== file line counts (develop -> head)"; for p in "$A/src/__tests__/ks501-enforcement-non-string-doctype.test.ts $HA" "$A/src/__tests__/ks480-org-provisioner-gate.test.ts $HB" "$A/src/__tests__/auth.test.ts $HC" "$O/src/__tests__/ks978-published-contract-organizationuuid.test.ts $HD" "$N/src/__tests__/ks1175-anchor-readback.test.ts $HE" "$N/src/__tests__/ks1175-identity-anchoring.test.ts $HE" "$D/scripts/__tests__/container_trivy_image_filter.test.sh $HG" "$U/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts $HF"; do set -- $p; echo "  $(basename $1): $(g show $DEV:$1 | wc -l | tr -d ' ') -> $(g show $2:$1 | wc -l | tr -d ' ')"; done
echo "=== .githooks/pre-push at develop: which preflight.sh a push runs (grep preflight)"; g show $DEV:.githooks/pre-push | /usr/bin/grep -n -E "preflight|show-toplevel|run-shell-suites" | cut -c1-200
echo "=== preflight.sh skip_stack call sites at develop (the three skipped legs 3/4/8)"; g show $DEV:$D/scripts/preflight/preflight.sh | /usr/bin/grep -n -E 'skip_stack|step "(3|4|8)/' | cut -c1-200
echo "=== originate jest config (runner) + anchoring/auth vitest versions in locks"
g show $DEV:$O/package.json | /usr/bin/grep -n -E '"(test|jest|vitest)"' | head; for s in anchoring auth api-gateway; do printf '  %s lock vitest: %s\n' "$s" "$(g show $DEV:$D/services/$s/package-lock.json | /usr/bin/grep -A1 -F '"node_modules/vitest"' | /usr/bin/grep -o '"version": "[^"]*"' | head -1)"; done
printf '  originate lock jest: %s\n' "$(g show $DEV:$O/package-lock.json | /usr/bin/grep -A1 -F '"node_modules/jest"' | /usr/bin/grep -o '"version": "[^"]*"' | head -1)"
echo "=== CSL dependency in anchoring package.json"; g show $DEV:$N/package.json | /usr/bin/grep -n -F 'cardano-serialization-lib'
echo "=== checkout porcelain / worktrees / for-each-ref (a moving reading)"; echo "  porcelain $(g status --porcelain | wc -l | tr -d ' ') | .git/worktrees $(ls "$R/.git/worktrees" | wc -l | tr -d ' ') | s-b12-* $(ls "$R/.git/worktrees" | /usr/bin/grep -c '^s-b12-') | for-each-ref $(g for-each-ref | wc -l | tr -d ' ') | branch $(g rev-parse --abbrev-ref HEAD)"
date -u +%Y-%m-%dT%H:%M:%SZ
