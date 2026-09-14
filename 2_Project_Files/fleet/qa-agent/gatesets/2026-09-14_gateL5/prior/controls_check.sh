#!/bin/bash
# controls_check.sh — re-grep every §4 positive-control token of the #799 / #880 / #985 (L5) brief at the PINNED SHAs through
# the GitHub contents API (read-only; GH_TOKEN sourced by NAME from the Secuura .env, never printed). #799: head 6da848891,
# the merge commit e6e25421e, Peter's head 38f6377b9, develop M18 8861e6216. #880: head a704137de, develop. #985: head
# fcd8a01e4 and its parent 6da848891. Tokens were derived from the PRs' OWN files at these SHAs — never carried from another
# gate's brief. PRESENT tokens must grep the stated count; ABSENT tokens exactly 0; blobs / sizes / lines / sha256 must match
# TARGET; the named lines must read as quoted; the 11 #799 product/test files must be blob-identical at 38f6377b9 and the
# merge commit; the two #799 test files must differ between the merge and the head by exactly the fix commit's shape (re-derived
# with difflib); the ks860 :433/:440 regexes over both test files must read NO offender at head and ONE each at 38f6377b9; the
# #880 yaml must lack Peter's two false sentences at head and carry them at develop; the #985 delta must be the seven files.
# Exit 0 = every control holds · 1 = at least one control failed · 2 = a file could not be read.
set -u
H799="${QA799_HEAD:-6da848891924f859179d097d464a7b97c9783a6a}"
MRG="${QA799_MERGE:-e6e25421e98ba8f11153f5fc394fe79fc96549a0}"
P38="${QA799_P38:-38f6377b9c6429be2627cb5454e98a36104a25b8}"
DEV="${QA799_DEVELOP:-6e78961e1d04277ecbdb0537e630afa0bf63b13c}"   # M19 (#982's squash, services/auth only) — every develop blob below must read as at M18
H880="${QA799_HEAD_880:-a704137de38a3055e40ee62adc343c0239f34ea9}"
H985="${QA799_HEAD_985:-fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0}"
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
W="$(mktemp -d "${TMPDIR:-/tmp}/qa799ctl.XXXXXX")"
POL='Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts'
SHIDX='Blockchain/Dev/packages/shared/src/index.ts'
SHMW='Blockchain/Dev/packages/shared/src/middleware/index.ts'
GUARD='Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts'
KS860='Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts'
ORIG='Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts'
OAUTH='Blockchain/Dev/services/originate/src/middleware/auth.ts'
ADM='Blockchain/Dev/services/originate/src/routes/adminConfig.ts'
ARM='Blockchain/Dev/services/security/src/__tests__/ks764-key-revoke-organisation-arm.test.ts'
SEC='Blockchain/Dev/services/security/src/__tests__/ks764-revoke-organisation-route-contract.test.ts'
SIDX='Blockchain/Dev/services/security/src/index.ts'
SPOL='Blockchain/Dev/services/security/src/keyRevokePolicy.ts'
KS742='Blockchain/Dev/services/security/src/__tests__/ks742-keys-tenancy-route-contract.test.ts'
JWT='Blockchain/Dev/services/auth/src/services/jwt.ts'
YAML='Blockchain/Dev/docs/openapi/secuura-api.yaml'
TPO='Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts'
PLAT='Blockchain/Dev/services/api-gateway/src/routes/platform.ts'
GEN='Blockchain/Dev/scripts/generate-openapi.ts'
ORGID='Blockchain/Dev/packages/shared/src/security/orgId.ts'
OORGID='Blockchain/Dev/services/originate/src/services/orgId.ts'
KS695='Blockchain/Dev/services/originate/src/__tests__/ks695-erasure-by-external-ref.test.ts'
T780S='Blockchain/Dev/packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts'
T780O='Blockchain/Dev/services/originate/src/__tests__/ks780-org-id-is-the-shared-implementation.test.ts'

fetch() { # path ref outfile -> prints blob sha, or ABSENT, or UNREADABLE
  ( set -a; . "$SECUURA_ENV"; set +a
    P="$1" REF="$2" OUT="$3" python3 - <<'PY'
import base64, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/contents/" + os.environ["P"] + "?ref=" + os.environ["REF"]
try:
    o = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except urllib.error.HTTPError as e:
    print("ABSENT" if e.code == 404 else "UNREADABLE HTTP%d" % e.code); sys.exit(0)
except Exception as e:
    print("UNREADABLE " + type(e).__name__); sys.exit(0)
raw = base64.b64decode(o["content"]) if o.get("content") else b""
if not raw and o.get("download_url"):
    raw = urllib.request.urlopen(urllib.request.Request(o["download_url"], headers={"Authorization": "Bearer " + t}), timeout=120).read()
open(os.environ["OUT"], "wb").write(raw)
print(o["sha"])
PY
  )
}
FAILS=0
echo "controls_check.sh — #799 head ${H799:0:9} (merge ${MRG:0:9}, Peter ${P38:0:9}), #880 head ${H880:0:9}, #985 head ${H985:0:9}, develop ${DEV:0:9} — $(date '+%Y-%m-%d %H:%M:%S %Z')"
SPECS="pol:$POL:$H799 pol_p38:$POL:$P38 shidx:$SHIDX:$H799 shidx_dev:$SHIDX:$DEV shmw:$SHMW:$H799 shmw_dev:$SHMW:$DEV guard:$GUARD:$H799 ks860:$KS860:$H799 ks860_dev:$KS860:$DEV ks860_p38:$KS860:$P38 orig:$ORIG:$H799 orig_mrg:$ORIG:$MRG orig_p38:$ORIG:$P38 oauth:$OAUTH:$H799 adm:$ADM:$H799 adm_dev:$ADM:$DEV arm:$ARM:$H799 sec:$SEC:$H799 sec_mrg:$SEC:$MRG sec_p38:$SEC:$P38 sidx:$SIDX:$H799 sidx_dev:$SIDX:$DEV spol:$SPOL:$H799 spol_dev:$SPOL:$DEV ks742:$KS742:$H799 ks742_dev:$KS742:$DEV jwt:$JWT:$H799 jwt_dev:$JWT:$DEV yaml880:$YAML:$H880 yaml_dev:$YAML:$DEV tpo880:$TPO:$H880 tpo_dev:$TPO:$DEV plat880:$PLAT:$H880 gen880:$GEN:$H880 sidx880:$SIDX:$H880 orgid985:$ORGID:$H985 pol985:$POL:$H985 shidx985:$SHIDX:$H985 oorgid985:$OORGID:$H985 oorgid799:$OORGID:$H799 ks695_985:$KS695:$H985 ks695_799:$KS695:$H799 t780s:$T780S:$H985 t780o:$T780O:$H985"
for spec in $SPECS; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  sha="$(fetch "$p" "$ref" "$W/$n")"
  case "$sha" in UNREADABLE*|"") echo "CANNOT READ $p at $ref: $sha"; exit 2 ;; ABSENT) echo "FAIL $n ABSENT at ${ref:0:9}"; FAILS=$((FAILS+1)); continue ;; esac
  echo "read $n = ${p##*/} @ ${ref:0:9}: blob ${sha:0:9}, $(wc -c < "$W/$n" | tr -d ' ') bytes, $(wc -l < "$W/$n" | tr -d ' ') lines, sha256 $(shasum -a 256 "$W/$n" | cut -c1-16)"
  echo "${sha:0:9}" > "$W/$n.blob"
done
# the NEW files must be ABSENT where the brief says
for spec in "pol_dev:$POL:$DEV" "orig_dev:$ORIG:$DEV" "sec_dev:$SEC:$DEV" "arm_dev:$ARM:$DEV" "guard_dev:$GUARD:$DEV" "orgid799:$ORGID:$H799" "t780s799:$T780S:$H799" "t780o799:$T780O:$H799"; do
  n="${spec%%:*}"; rest="${spec#*:}"; p="${rest%%:*}"; ref="${rest#*:}"
  a="$(fetch "$p" "$ref" "$W/$n")"
  [ "$a" = "ABSENT" ] && echo "ok   $n ABSENT at ${ref:0:9} (HTTP 404 — the file is NEW there)" || { echo "FAIL $n at ${ref:0:9} read: $a (expected ABSENT)"; FAILS=$((FAILS+1)); }
done
blobis() { [ "$(cat "$W/$1.blob")" = "$2" ] && echo "ok   $1 blob $2" || { echo "FAIL $1 blob is $(cat "$W/$1.blob"), not $2"; FAILS=$((FAILS+1)); }; }
blobis pol dcd774a30; blobis pol_p38 dcd774a30; blobis shidx 8794bca5f; blobis shidx_dev 6731f0f2f; blobis shmw 3a67987a7; blobis shmw_dev b5932490c
blobis guard ab8e46d79; blobis ks860 e0dfadb9c; blobis ks860_dev e0dfadb9c; blobis ks860_p38 d8842e577
blobis orig 5a78c4181; blobis orig_mrg 3331f59ce; blobis orig_p38 3331f59ce; blobis oauth f08ee1a89; blobis adm 26cec03de; blobis adm_dev ccb3222a6
blobis arm 1fe8671b0; blobis sec 3bae312af; blobis sec_mrg 7a75d2c65; blobis sec_p38 7a75d2c65; blobis sidx 1bb567a09; blobis sidx_dev ed0239d79
blobis spol b0493aa67; blobis spol_dev 60bd9ef5e; blobis ks742 d35e2d5dc; blobis ks742_dev d35e2d5dc; blobis jwt d0d55c11b; blobis jwt_dev d0d55c11b
blobis yaml880 298d95e4a; blobis yaml_dev f14ab17ed; blobis tpo880 7b7e0be14; blobis tpo_dev 5903759c7; blobis plat880 4550401f8; blobis gen880 e84acdc9e; blobis sidx880 fb806451a
blobis orgid985 a42d7783d; blobis pol985 86b554052; blobis shidx985 aeaf90dad; blobis oorgid985 f87b261b8; blobis oorgid799 a40475112; blobis ks695_985 6d55452f2; blobis ks695_799 d377aa8c2; blobis t780s e3aa932f7; blobis t780o c1268e31b
for pair in "orig_mrg:orig_p38" "sec_mrg:sec_p38" "ks742:ks742_dev" "jwt:jwt_dev" "ks860:ks860_dev" "tpo_dev:tpo_dev" "ks695_799:ks695_799"; do a="${pair%%:*}"; b="${pair#*:}"; cmp -s "$W/$a" "$W/$b" && echo "ok   $a byte-identical to $b" || { echo "FAIL $a DIFFERS from $b"; FAILS=$((FAILS+1)); }; done
for pair in "orig:orig_mrg" "sec:sec_mrg" "pol:pol985" "shidx:shidx985" "oorgid799:oorgid985" "ks695_799:ks695_985" "yaml880:yaml_dev" "tpo880:tpo_dev" "ks860:ks860_p38"; do a="${pair%%:*}"; b="${pair#*:}"; cmp -s "$W/$a" "$W/$b" && { echo "FAIL $a byte-identical to $b (must differ)"; FAILS=$((FAILS+1)); } || echo "ok   $a DIFFERS from $b (as it must)"; done
for pair in "orig:32edded63a6bc739" "sec:4b68c363d7a517f8" "pol:9539d243958a9123" "shidx:707ff7ed71e87254" "adm:d08949fd4dba1bec" "sidx:6ed6dc98a9840db5" "ks860:fc62ca7410a06736" "orig_mrg:c1feaef34781718c" "sec_mrg:fe9b2b9bb5b853f2" "yaml880:228eb0c0e79ccfc1" "tpo880:d274e5d3f3ac39b1" "yaml_dev:343d694157771e1d" "orgid985:430e912ef5bb2772" "pol985:19bd8b1ad9789060" "ks695_985:f1bde33e2f01b105"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(shasum -a 256 "$W/$f" | cut -c1-16)" = "$want" ] && echo "ok   $f sha256 $want" || { echo "FAIL $f sha256 is not $want"; FAILS=$((FAILS+1)); }
done
for pair in "orig:293" "orig_mrg:237" "sec:214" "sec_mrg:192" "pol:268" "pol985:246" "guard:458" "arm:168" "ks860:784" "ks860_p38:545" "ks742:613" "jwt:374" "shidx:232" "shidx985:237" "adm:2133" "sidx:1496" "sidx880:1586" "yaml880:39552" "yaml_dev:39549" "tpo880:765" "tpo_dev:763" "orgid985:44" "oorgid985:40" "ks695_985:733" "ks695_799:729" "t780s:85" "t780o:49"; do
  f="${pair%%:*}"; want="${pair#*:}"
  [ "$(wc -l < "$W/$f" | tr -d ' ')" = "$want" ] && echo "ok   $f $want lines" || { echo "FAIL $f is not $want lines"; FAILS=$((FAILS+1)); }
done
lineis() { local got; got="$(sed -n "${2}p" "$W/$1")"; [ "$got" = "$3" ] && echo "ok   $1:$2 = $3" || { echo "FAIL $1:$2 is: $got"; FAILS=$((FAILS+1)); }; }
# --- #799: the cited lines at head
lineis orig 88 "        if (principal.tenantId) req.tenantId = principal.tenantId;"
lineis orig 110 "import { logger } from '../utils/logger';"
lineis orig 131 "const ADMIN_NO_TENANT = { userId: 'u5', role: 'ORG_ADMIN', organizationId: ORG_A };"
lineis orig 145 "    server = app.listen(0, '127.0.0.1', () => resolve());"
lineis orig 184 "    expect(typeof shared.decideKeyRevoke).toBe('function');"
lineis orig 188 "    expect(jest.isMockFunction(shared.decideKeyRevoke)).toBe(false);"
lineis orig 251 "  it('CASE 5 — a TENANT-LESS CALLER is refused on an org-owned key (\`caller has no tenant\`), and nothing is written', async () => {"
lineis orig 257 "    const warn = jest.spyOn(logger, 'warn');"
lineis orig 266 "      expect(warn).toHaveBeenCalledWith("
lineis orig 268 "        expect.objectContaining({ reason: 'caller has no tenant' }),"
lineis orig_mrg 121 "    server = app.listen(0, () => resolve());"
lineis sec 91 "const ADMIN_NO_TENANT = () => token({ role: 'ISSUER_ADMIN', organizationId: ORG_A });"
lineis sec 138 "    server = app.listen(0, '127.0.0.1', resolve);"
lineis sec 196 "  it('CASE 5 — a TENANT-LESS CALLER is refused on an org-owned key (403, the tenant floor)', async () => {"
lineis sec 205 "    expect(body.success).toBe(false);"
lineis sec_mrg 128 "    server = app.listen(0, resolve);"
lineis pol 122 "function normOrgId(v: string | null | undefined): string | null {"
lineis pol 175 "  if (!user?.tenantId) {"
lineis pol 176 "    return { allow: false, status: 403, reason: 'caller has no tenant' };"
lineis pol 229 "    if (!targetOrg) {"
lineis pol 239 "      return { allow: false, status: 403, reason: 'caller has no organisation' };"
lineis pol 242 "      return { allow: false, status: 403, reason: 'cross-organisation' };"
lineis shidx 230 "  decideKeyRevoke,"
lineis shmw 42 "  tenantId?: string;"
lineis oauth 36 "  tenantId?: string;"
lineis adm 38 "adminConfigRouter.use(authenticate(), requireRole('SYSTEM_ADMIN', 'ORG_ADMIN'));"
lineis adm 977 "adminConfigRouter.delete('/api-keys/:id', async (req: Request, res: Response) => {"
lineis adm 983 "    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';"
lineis adm 1009 "      return res.json({ success: false, message: 'Not found' });"
lineis adm 1030 "    const decision = decideKeyRevoke((req as any).user, {"
lineis adm 1035 "      organizationId: keyRows[0].organization_id == null ? undefined : String(keyRows[0].organization_id),"
lineis adm 1037 "    if (!decision.allow) {"
lineis adm 1038 "      logger.warn('API key revoke refused', {"
lineis adm 1047 "      return res.status(403).json({"
lineis adm 1049 "        error: { code: 'FORBIDDEN', message: 'Not authorised to revoke this key' },"
lineis sidx 910 "const KEY_ADMIN_ROLES = new Set(['SYSTEM_ADMIN', 'SUPER_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'ADMIN']);"
lineis sidx 1122 "app.delete('/api/keys/:id', requireKeyAdmin, async (req: Request, res: Response) => {"
lineis sidx 1135 "  const decision = decideKeyRevoke((req as any).user, {"
lineis sidx 1140 "  if (!decision.allow) {"
lineis sidx 1153 "    return res.status(decision.status ?? 403).json({"
lineis sidx 1155 "      error: { code: 'FORBIDDEN', message: 'Not authorised to revoke this API key' },"
lineis ks860 433 "  const re = /\\.listen\\(\\s*0\\s*(,|\\))/g;"
lineis ks860 440 "      const host = /^\\s*(['\"])127\\.0\\.0\\.1\\1/.exec(rest);"
lineis ks860 463 "  it('🔴 no test file under services/ or packages/ calls app.listen(0) without binding 127.0.0.1', () => {"
lineis ks860 477 "    ).toEqual([]);"
lineis ks860 515 "    expect(offendingListenSites(\"const s = app.listen(0, '127.0.0.1', () => {});\")).toEqual([]);"
lineis ks742 85 "const TENANTLESS = () => token({ role: 'ORG_ADMIN' });"
lineis ks742 596 "  it('a tenant-A admin revoking a tenant-B key gets 403 FROM THE ROUTE', async () => {"
lineis ks742 606 "  it('CONTROL: a platform admin revoking the same key gets 200', async () => {"
lineis jwt 173 "    tenantId: user.tenantId,"
lineis jwt 263 "    ...(meta.tenantId ? { tenantId: meta.tenantId } : {}),"
# --- #880
lineis tpo880 676 "      .openapi({ description: 'Mint a replacement key for an already-registered Organisation (§5 rotation). The prior active keys of the same connector are retired as part of the mint: deactivated at once by default, or left valid for at most the API_KEY_ROTATION_GRACE_SECONDS window when the security service sets one.' }),"
lineis tpo880 732 "    'existing org and NO key; \`rotate: true\` mints a replacement and retires the prior ' +"
lineis tpo_dev 676 "      .openapi({ description: 'Mint a replacement key for an already-registered Organisation (§5 rotation, step 1). The old key stays active until explicitly revoked.' }),"
lineis yaml880 10044 "          description: \"Mint a replacement key for an already-registered Organisation (§5 rotation). The prior"
lineis yaml_dev 10044 "          description: Mint a replacement key for an already-registered Organisation (§5 rotation, step 1)."
lineis yaml_dev 10045 "            The old key stays active until explicitly revoked."
lineis gen880 255 "  const newYaml = yaml.stringify(doc, { lineWidth: 100 });"
lineis sidx880 247 "  const graceRaw = Number.parseInt(process.env.API_KEY_ROTATION_GRACE_SECONDS ?? '0', 10);"
lineis plat880 748 "            rotated: rotate && existing.rows.length > 0,"
# --- #985
lineis orgid985 42 "export function normaliseOrgId(v: string | null | undefined): string | null {"
lineis orgid985 43 "  return typeof v === 'string' && v.trim() !== '' ? v.trim().toLowerCase() : null;"
lineis pol985 52 "import { normaliseOrgId } from './orgId';"
lineis pol985 153 "  if (!user?.tenantId) {"
lineis pol985 174 "    const targetOrg = normaliseOrgId(organisationScope.targetOrganizationId);"
lineis shidx985 237 "export { normaliseOrgId } from './security/orgId';"
lineis oorgid985 40 "export { normaliseOrgId } from '@secuura/shared';"
lineis ks695_985 39 "  normaliseOrgId: jest.requireActual('@secuura/shared').normaliseOrgId,"
lineis t780s 33 "const ORG = 'a1b2c3d4-e5f6-4a7b-8c9d-ef0123456789';"
chk() { # file token mode(present|absent|N)
  local f="$1" tok="$2" mode="$3" c
  c="$(/usr/bin/grep -c -F -- "$tok" "$W/$f")"
  if [ "$mode" = present ] && [ "$c" -ge 1 ]; then echo "ok   $f  present x$c  $tok"
  elif [ "$mode" = absent ] && [ "$c" -eq 0 ]; then echo "ok   $f  absent      $tok"
  elif [ "$mode" != present ] && [ "$mode" != absent ] && [ "$c" -eq "$mode" ]; then echo "ok   $f  exactly x$c $tok"
  else echo "FAIL $f  $mode expected, count $c: $tok"; FAILS=$((FAILS+1)); fi
}
# --- #799 tamper anchors and controls
chk orig "server = app.listen(0, '127.0.0.1', () => resolve());" 1
chk orig "expect(typeof shared.decideKeyRevoke).toBe('function');" 1
chk orig "if (principal.tenantId) req.tenantId = principal.tenantId;" 1
chk orig "jest.spyOn(logger, 'warn')" 1
chk orig "expect.objectContaining({ reason: 'caller has no tenant' })" 1
chk orig "jwt.ts:263" 1
chk orig "listen(" 1
chk orig "  it('" 10
chk orig "  it('CASE " 5
chk orig "  it('CONTROL" 5
chk orig_mrg "  it('" 9
chk orig_mrg "ADMIN_NO_TENANT" absent
chk orig_mrg "typeof shared.decideKeyRevoke" absent
chk sec "server = app.listen(0, '127.0.0.1', resolve);" 1
chk sec "const ADMIN_NO_TENANT = () => token({ role: 'ISSUER_ADMIN', organizationId: ORG_A });" 1
chk sec "listen(" 2
chk sec "  it('" 7
chk sec_mrg "  it('" 6
chk sec_mrg "ADMIN_NO_TENANT" absent
chk pol "  if (!user?.tenantId) {" 1
chk pol "reason: 'caller has no tenant'" 1
chk pol "reason: 'caller has no organisation'" 1
chk pol "reason: 'cross-organisation'" 1
chk pol "reason: 'cross-tenant'" 1
chk pol "reason: 'same-tenant'" 2
chk pol "status: 403" 4
chk pol "normOrgId(" 3
chk shidx "  decideKeyRevoke," 1
chk shidx "} from './security/keyRevokePolicy';" 2
chk shidx "export type { RevokeDecision } from './security/keyRevokePolicy';" 1
chk shidx "normaliseOrgId" absent
chk oauth "req.tenantId" absent
chk oauth "_secuuraUser" 3
chk adm "    const tenantId = ((req as any).tenantId as string | undefined) || 'a0000000-0000-4000-8000-000000000001';" 6
chk adm "      return res.json({ success: false, message: 'Not found' });" 3
chk adm "    if (!decision.allow) {" 1
chk adm "      logger.warn('API key revoke refused', {" 1
chk adm "      organizationId: keyRows[0].organization_id == null ? undefined : String(keyRows[0].organization_id)," 1
chk adm "UPDATE svc_api_keys SET is_active = false" 1
chk adm "jwt.ts:263" 1
chk adm_dev "decideKeyRevoke" absent
chk sidx "  if (!decision.allow) {" 1
chk sidx "message: 'Not authorised to revoke this API key'" 1
chk sidx "return res.status(decision.status ?? 403).json({" 1
chk sidx "app.delete('/api/keys/:id', requireKeyAdmin" 1
chk sidx "'Cross-tenant API key revoke refused'" 1
chk sidx_dev "message: 'API key belongs to another tenant'" 1
chk sidx_dev "keyOrganizationId" absent
chk spol "} from '@secuura/shared';" 3
chk spol "  decideKeyRevoke," 1
chk spol_dev "reason: 'caller has no tenant'" 1
chkre() { # file regex N  (a LINE-ANCHORED count; grep basic regex, never -F)
  local f="$1" re="$2" want="$3" c; c="$(/usr/bin/grep -c -- "$re" "$W/$f")"
  [ "$c" -eq "$want" ] && echo "ok   $f  exactly x$c /$re/" || { echo "FAIL $f  $want expected, count $c: /$re/"; FAILS=$((FAILS+1)); }
}
chkre guard "^  it('" 5
chkre guard "^      it('" 5
chk guard "revokeWrite:" 2
chk guard "rmSync" present
chk arm "  it('" 11
chk ks860 "  it('" 23
chk ks860 "WALK_ROOTS = ['services', 'packages']" 1
chk ks742 "app.listen(0, '127.0.0.1', resolve);" 1
chk shmw "jwt.ts:263" 1
chk jwt "export function generateConnectorToken(" 1
chk jwt "export function generateAccessToken(" 1
# --- #880
chk yaml880 "The old key stays active until explicitly revoked." absent
chk yaml880 "(revoke the old key separately)" absent
chk yaml880 "retires the prior active keys of the same" 1
chk yaml880 "API_KEY_ROTATION_GRACE_SECONDS" 2
chk yaml_dev "The old key stays active until explicitly revoked." 1
chk yaml_dev "(revoke the old key separately)" 1
chk yaml_dev "API_KEY_ROTATION_GRACE_SECONDS" absent
chk tpo880 "API_KEY_ROTATION_GRACE_SECONDS" 2
chk tpo_dev "API_KEY_ROTATION_GRACE_SECONDS" absent
chk gen880 "CHECK FAIL: generated YAML differs from on-disk version" 1
chk gen880 "CHECK PASS: on-disk YAML matches generated" 1
chk sidx880 "export async function revokePriorConnectorKeys(" 1
chk sidx880 "WHERE connector_id = \$1 AND tenant_id = \$2::uuid AND id <> \$3 AND is_active = true" 2
chk plat880 "priorKeysRevoked === null" 1
chk plat880 "rotated: rotate && existing.rows.length > 0," 1
# --- #985
chk orgid985 "v.trim().toLowerCase()" 1
chk pol985 "normaliseOrgId(" 2
chk pol985 "function normOrgId" absent
chk pol985 "reason: 'caller has no tenant'" 1
chk oorgid985 "export const normaliseOrgId" absent
chk oorgid985 "export { normaliseOrgId } from '@secuura/shared';" 1
chk oorgid799 "export const normaliseOrgId = (v: string | null | undefined): string | null =>" 1
chk ks695_985 "normaliseOrgId: jest.requireActual('@secuura/shared').normaliseOrgId," 1
chk ks695_799 "normaliseOrgId" absent
chkre ks695_985 "^ *it(['\"]" 40
chkre ks695_985 "^ *it('" 39
chk t780s "  it('" 7
chk t780o "  it('" 3
chk t780o "jest.mock(" absent
# --- the shapes re-derived in Python: the #799 fix-commit shape, the ks860 regexes, the #985 delta shapes, control bytes
cat > "$W/sim.py" <<'PY'
import re, sys, difflib
W = sys.argv[1]
R = lambda n: open(f"{W}/{n}", encoding="utf-8").read()
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
def changed(a, b):
    d = [l for l in difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    return sum(1 for l in d if l[0] == "-"), sum(1 for l in d if l[0] == "+")
ck(changed(R("orig_mrg"), R("orig")) == (1, 57), f"originate test merge->head = -1 +57 (got {changed(R('orig_mrg'), R('orig'))})")
ck(changed(R("sec_mrg"), R("sec")) == (1, 23), f"security test merge->head = -1 +23 (got {changed(R('sec_mrg'), R('sec'))})")
SITE = re.compile(r"\.listen\(\s*0\s*(,|\))"); HOST = re.compile(r"^\s*(['\"])127\.0\.0\.1\1")
def mask(src):
    src = re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), src, flags=re.S)
    return "\n".join(l if "//" not in l else l[: l.index("//")] + " " * (len(l) - l.index("//")) for l in src.split("\n"))
def offenders(src):
    m = mask(src); out = []
    for x in SITE.finditer(m):
        if not (x.group(1) == "," and HOST.match(m[x.end():])): out.append(m[: x.start()].count("\n") + 1)
    return out
ck(offenders(R("orig")) == [] and offenders(R("sec")) == [], f"ks860 :433/:440 over both test files at head -> offenders [] (got {offenders(R('orig'))}, {offenders(R('sec'))})")
ck(offenders(R("orig_mrg")) == [121] and offenders(R("sec_mrg")) == [128], f"at the merge commit (= 38f6377b9) -> [121] / [128] (got {offenders(R('orig_mrg'))}, {offenders(R('sec_mrg'))})")
ck(offenders("const s = app.listen(0);") == [1] and offenders("const s = app.listen(0, '127.0.0.1');") == [], "guard controls: bare listen(0) -> 1 offender; the shipped spelling -> 0")
ck(changed(R("tpo_dev"), R("tpo880")) == (3, 5), f"#880 .ts develop->head = -3 +5 (got {changed(R('tpo_dev'), R('tpo880'))})")
hunks = [l for l in difflib.unified_diff(R("yaml_dev").split("\n"), R("yaml880").split("\n"), lineterm="", n=0) if l.startswith("@@")]
ck(len(hunks) == 2, f"#880 yaml develop->head = 2 hunks (got {hunks})")
# the policy delta, judged by its CODE lines (git numstat reads -40 +18; difflib aligns the docblock differently — the code content is the control)
def code_lines(a, b):
    d = [l for l in difflib.unified_diff(a.split("\n"), b.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    def is_code(t):
        t = t.strip(); return t != "" and not (t.startswith("*") or t.startswith("/*") or t.startswith("//") or t.startswith("*/"))
    return sorted(l[1:].strip() for l in d if l[0] == "-" and is_code(l[1:])), sorted(l[1:].strip() for l in d if l[0] == "+" and is_code(l[1:]))
rm, ad = code_lines(R("pol"), R("pol985"))
ck(rm == sorted(["function normOrgId(v: string | null | undefined): string | null {", "return typeof v === 'string' && v.trim() !== '' ? v.trim().toLowerCase() : null;", "}", "const targetOrg = normOrgId(organisationScope.targetOrganizationId);", "const callerOrg = normOrgId(user.organizationId);"]), f"#985 policy: removed CODE lines = the private normaliser (3) + its two call sites (got {rm})")
ck(ad == sorted(["import { normaliseOrgId } from './orgId';", "const targetOrg = normaliseOrgId(organisationScope.targetOrganizationId);", "const callerOrg = normaliseOrgId(user.organizationId);"]), f"#985 policy: added CODE lines = the import + the two repointed call sites (got {ad})")
ck(changed(R("ks695_799"), R("ks695_985")) == (0, 4), f"#985 ks695 = -0 +4 (got {changed(R('ks695_799'), R('ks695_985'))})")
ck(changed(R("shidx"), R("shidx985")) == (0, 5), f"#985 shared index.ts = -0 +5 (got {changed(R('shidx'), R('shidx985'))})")
ck(changed(R("oorgid799"), R("oorgid985")) == (26, 29), f"#985 originate orgId.ts = -26 +29 (got {changed(R('oorgid799'), R('oorgid985'))})")
DEF = re.compile(r"^\s*(export\s+)?(function|const)\s+norm(alise)?OrgId\b")
n985 = sum(1 for f in ("orgid985", "pol985", "oorgid985") for l in R(f).split("\n") if DEF.match(l))
n799 = sum(1 for f in ("pol", "oorgid799") for l in R(f).split("\n") if DEF.match(l))
ck(n985 == 1 and n799 == 2, f"definitions census over the three modules: {n985} at #985's head (want 1), {n799} at 6da848891 (want 2)")
for name in ("orig", "sec", "pol", "pol985", "orgid985", "ks695_985", "tpo880"):
    b = R(name).encode("utf-8"); n = sum(1 for x in b if (x < 0x20 and x not in (9, 10, 13)) or x == 0x7f)
    ck(n == 0, f"{name}: 0 raw control bytes (got {n})")
sys.exit(1 if fails else 0)
PY
python3 "$W/sim.py" "$W" || FAILS=$((FAILS+1))
echo "work dir (kept): $W"
echo "controls_check: FAILS=$FAILS"
[ "$FAILS" -eq 0 ] && exit 0 || exit 1
