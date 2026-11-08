import difflib, os, sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/gen/tip/'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
TIP=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/tip_start.out').read().split()[0]
B='Blockchain/Dev/'
def rd(n): return open(G+n,encoding='utf-8').read()
def dd(p,old,new):
    assert old!=new
    return 'diff --git a/%s b/%s\n'%(p,p)+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),'a/'+p,'b/'+p,n=3))
def rep(src,old,new):
    assert src.count(old)==1,(src.count(old),old)
    return src.replace(old,new)
def brief(tag,ks,title,origin,files,what,change,patch,expect,unm,hard=''):
    d=BR+tag+'/'; os.makedirs(d,exist_ok=False)
    open(d+'golden.diff','w',encoding='utf-8').write(patch)
    fl=''.join('File: `%s`\n'%f for f in files)
    md='''# %s

DRAFT by Spark operator 106 for Wednesday, 2026-11-09 AEDT. Secuura (Platform K) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: %s. Counter: this is round 1 of 2 (original).

Tier: `doc_only`
Runner: vitest
Tip: `%s`
%s
## The mode
doc_only: prose and comments only. Every changed line of a code file is a whole-line comment; no code line changes.
%s
## What is wrong
%s

## The exact change
%s

The whole diff, to copy EXACTLY (the hunk header counts are correct: 3 lines of unchanged context before and after each change, so `git apply` takes it with no fuzz; do not shorten the context, do not recompute the headers):

```diff
%s```

## Expect
%s
## UNMEASURED
%s

## Scope
Exactly the File lines above. Nothing else changes in any file: no other comment, no re-wrapping, no code. The new text is given above verbatim: copy it.

## Output
ONE unified diff in a ```diff fence.
'''%(title,origin,TIP,fl,hard,what,change,patch,expect,unm)
    open(d+'%s.md'%ks,'w',encoding='utf-8').write(md)
    print('wrote',d)

# ---- KS-2107 originate documents.ts: five comments -------------------------------------------------------------
DF=B+'services/originate/src/routes/documents.ts'
od=rd('documents.ts')
# P1: doc block (1390), custody transfer (2501), shared emitter (3149)
n=rep(od," * (share / transfer-custody / revoke) — KS-319. Anchoring is idempotent per\n"," * (share / transfer-custody / revoke) — KS-319. The anchor id is idempotent per\n")
n=rep(n," * it as ExternalRef and its CardanoAnchorRefresher can upgrade it to a tx hash.\n"," * it as ExternalRef and its CardanoAnchorRefresher can upgrade it to a tx hash.\n * Idempotent for the anchor id only: a repeat admitted event may still build and\n * send its own transaction, and the row then names that one (KS-1384).\n")
n=rep(n,"      // return a resolvable anchor id (idempotent — reuses the document's\n      // existing anchor). Replaces the previously-deferred anchoredTxHash:null.\n",
       "      // return a resolvable anchor id (idempotent for the id only: it reuses the\n      // document's existing anchor, but a repeat admitted event may submit its own\n      // transaction, KS-1384). Replaces the previously-deferred anchoredTxHash:null.\n")
n=rep(n,"      // KS-319 shared emitter: idempotent per (document, network) — the event\n      // anchors against the document's existing anchor, returning a resolvable\n      // anchor id (GET /api/anchors/{id}); null when anchoring is down (S falls\n      // back to POST /api/anchors, its existing HTTP-failure path).\n",
       "      // KS-319 shared emitter: the anchor id is idempotent per (document, network) — the event\n      // anchors against the document's existing anchor, returning a resolvable\n      // anchor id (GET /api/anchors/{id}); a repeat admitted event may still submit\n      // its own transaction (KS-1384). The id is null when anchoring is down (S falls\n      // back to POST /api/anchors, its existing HTTP-failure path).\n")
p1=dd(DF,od,n)
brief('ks_2107_o106_p1_originate_anchor_emit_comments_doc_block_custody_shared_emitter','KS-2107',
 'KS-2107 pass 1: three originate lifecycle-anchor comments call the emit idempotent, but only the anchor id is (DOC-ONLY: routes/documents.ts)',
 'KS-2107 (seat S 37th filing, 2026-11-08; Backlog; Low). Pass 1 of 2 on this file; pass 2 (O106-P2) covers the share and revoke sites',
 [DF],
 'Five comments in `routes/documents.ts` say the lifecycle-event anchor emit is "idempotent" and "reuses the document\'s existing anchor". That is true of the anchor ID. It is not true of the transaction: Seat AA 5th\'s probe shows a repeat ADMITTED event builds and sends a new transaction and the row then names the second. Kam ruled (card secuura-ks1384-share-pays-second-tx-before-stage2-1106 = a) that this behaviour stays until stage 2 (KS-1384), so the comments are the only thing out of line. This pass fixes three of the five: the doc block of `emitLifecycleAnchor` (line 1390), the custody-transfer site (line 2501) and the shared-emitter site (line 3149). Text only; no behaviour change.',
 'Three edit points, comment text only. (1) The doc block above `emitLifecycleAnchor`: line 1390 "Anchoring is idempotent per" becomes "The anchor id is idempotent per", and two comment lines are added after the line ending "tx hash." saying idempotent for the anchor id only (KS-1384). (2) The custody-transfer comment (lines 2501-2502) says idempotent for the id only. (3) The shared-emitter comment (lines 3149-3152) says the anchor id is idempotent and a repeat admitted event may still submit its own transaction. The new text is in the diff below, verbatim.',
 p1,
 "expect_absent: `KS-319. Anchoring is idempotent per`\nexpect_absent: `return a resolvable anchor id (idempotent — reuses the document's`\nexpect_absent: `KS-319 shared emitter: idempotent per (document, network)`\nexpect_present: `KS-319. The anchor id is idempotent per`\nexpect_present: `Idempotent for the anchor id only: a repeat admitted event may still build and`\nexpect_present: `a repeat admitted event may submit its own`\nexpect_present: `KS-319 shared emitter: the anchor id is idempotent per (document, network)`\n",
 'No test run: comments only. That a repeat admitted event builds a second transaction is Seat AA 5th\'s probe (stand-in chain), quoted by the ticket and not re-run here. The share (line 2921) and revoke (line 3023) comments are pass 2. Line 700 also says "idempotent", about an external-id match: a different subject, untouched.')
# P2: share (2921), revoke (3023)
n=od
old="      // resolvable anchor id (idempotent — reuses the document's existing anchor).\n"
assert n.count(old)==2
new="      // resolvable anchor id (idempotent for the id only: it reuses the document's\n      // existing anchor, but a repeat admitted event may submit its own transaction, KS-1384).\n"
n=n.replace(old,new)
p2=dd(DF,od,n)
brief('ks_2107_o106_p2_originate_anchor_emit_comments_share_and_revoke','KS-2107',
 'KS-2107 pass 2: the share and revoke comments in originate call the anchor emit idempotent, but only the anchor id is (DOC-ONLY: routes/documents.ts)',
 'KS-2107 (seat S 37th filing, 2026-11-08; Backlog; Low). Pass 2 of 2 on this file; pass 1 (O106-P1) covers the doc block, custody-transfer and shared-emitter sites. The two passes touch disjoint hunks (more than 400 lines apart)',
 [DF],
 'Two of the five comments in `routes/documents.ts` that call the lifecycle-event anchor emit "idempotent" and "reuses the document\'s existing anchor": the share site (line 2921) and the revoke site (line 3023). Both carry the SAME line, `// resolvable anchor id (idempotent — reuses the document\'s existing anchor).` That holds for the anchor ID but not for the transaction: a repeat admitted event builds and sends its own (Seat AA 5th\'s probe; Kam ruled it stays until stage 2, KS-1384). Text only.',
 'Two edit points, ONE LINE EACH becoming two comment lines. Replace the line `// resolvable anchor id (idempotent — reuses the document\'s existing anchor).` at line 2921 (share) and at line 3023 (revoke) with the two lines in the diff below. The other comment lines around them do not change. The new text is in the diff, verbatim.',
 p2,
 "expect_absent: `resolvable anchor id (idempotent — reuses the document's existing anchor).`\nexpect_present: `resolvable anchor id (idempotent for the id only: it reuses the document's`\nexpect_present: `existing anchor, but a repeat admitted event may submit its own transaction, KS-1384).`\n",
 'No test run: comments only. The probe behind the claim is not re-run. The doc block, custody-transfer and shared-emitter sites are pass 1.')

# ---- KS-2109 item 3: stale pointers (trustHeaders.ts, docs) ------------------------------------------------------
TF=B+'services/api-gateway/src/utils/trustHeaders.ts'; DOC=B+'docs/security/AGENT-DOCUMENT-OPERATION-RULES.md'
ot=rd('trustHeaders.ts'); nt=rep(ot," * SUPER_ADMIN_ROLES before doing so. The blanket strip added 2026-04-25\n"," * `isPlatformRole` (from @secuura/shared) before doing so. The blanket strip added 2026-04-25\n")
od2=rd('AGENT-DOCUMENT-OPERATION-RULES.md')
nd=rep(od2,"(`enforceAdminProxy` with `PROXY_ADMIN_ROLES` in `services/api-gateway/src/routes/proxy.ts`, which lists human roles only)","(`enforceAdminProxy` in `services/api-gateway/src/routes/proxy.ts`, which asks `isPlatformOrOrgAdminRole` and so admits `SYSTEM_ADMIN`, `SUPER_ADMIN` and `ORG_ADMIN` only: human roles)")
p3=dd(TF,ot,nt)+dd(DOC,od2,nd)
brief('ks_2109_o106_p1_two_stale_role_list_pointers_trustheaders_and_agent_rules','KS-2109',
 'KS-2109 item 3 (two of three): a comment and a doc line still name role lists PR 2060 removed (DOC-ONLY: trustHeaders.ts and AGENT-DOCUMENT-OPERATION-RULES.md)',
 'KS-2109 (seat S 37th filing, 2026-11-08; Backlog; Medium) item 3, "Three stale pointers". The third pointer, `services/api-gateway/src/index.ts` lines 327-329, is NOT in this pass: PR 2083 lists that file',
 [TF,DOC],
 'KS-2109 item 3. After PR 2060 (KS-1536 3a) the one platform-role list is `PLATFORM_ROLES` behind `isPlatformRole` in `packages/shared/src/security/keyRevokePolicy.ts`. (a) `services/api-gateway/src/utils/trustHeaders.ts` line 37 still says the tenant override is gated on `SUPER_ADMIN_ROLES`, a name that no longer exists (the gate is `isPlatformRole(decoded.role)` at `middleware/auth.ts` line 697). (b) `docs/security/AGENT-DOCUMENT-OPERATION-RULES.md` line 55 says `enforceAdminProxy` uses `PROXY_ADMIN_ROLES`; at the tip `enforceAdminProxy` (`routes/proxy.ts` lines 1256-1263) asks `isPlatformOrOrgAdminRole(user.role)`, which is true for `SYSTEM_ADMIN`, `SUPER_ADMIN` and `ORG_ADMIN` (keyRevokePolicy.ts line 163-167), and `PROXY_ADMIN_ROLES` appears once, in a comment at line 1255 that says it was the local list.',
 'Two edit points, ONE LINE EACH, text only. (1) trustHeaders.ts line 37: `SUPER_ADMIN_ROLES before doing so.` becomes `` `isPlatformRole` (from @secuura/shared) before doing so.`` (2) AGENT-DOCUMENT-OPERATION-RULES.md line 55: the parenthesis after "role-gated against connectors at the gateway" is replaced as shown. The new text is in the diff below, verbatim. Comment line only in the .ts file; no code line changes.',
 p3,
 "expect_absent: `SUPER_ADMIN_ROLES` in `%s`\nexpect_absent: `PROXY_ADMIN_ROLES` in `%s`\nexpect_present: `isPlatformRole` (from @secuura/shared) before doing so` in `%s`\nexpect_present: `which asks `isPlatformOrOrgAdminRole` and so admits` in `%s`\n"%(TF,DOC,TF,DOC),
 'No test run: text only. The docs fragments check does not apply (the doc is not under Projects Documents/fragments). The third pointer in api-gateway/src/index.ts (lines 327-329) is left because PR 2083 lists that file. Whether the rest of AGENT-DOCUMENT-OPERATION-RULES.md is current is not re-read beyond line 55.')

# ---- KS-2117: SDK README + transfers.ts docstrings ----------------------------------------------------------------
RF=B+'sdk/javascript/README.md'; SF=B+'sdk/javascript/src/modules/transfers.ts'
orr=rd('README.md')
nr=rep(orr,"// Initialize with API key\n","// Initialize with an API key (the transfer write routes refuse API keys: see Transfers & Delegations)\n")
nr=rep(nr,"### Transfers & Delegations\n\n```typescript\n","### Transfers & Delegations\n\nThe transfer write routes (`initiate`, `approve` and `cancel`) refuse every API key with 403 (KS-2081). Build the client with an `accessToken` for these calls; the `apiKey` setup in Quick Start does not work for them.\n\n```typescript\n")
brief('ks_2117_o106_p1_sdk_readme_transfer_example_is_403_for_an_api_key','KS-2117',
 'KS-2117 pass 1: the JavaScript SDK README sets up an API key and then shows transfer calls that PR 2077 now answers with 403 (DOC-ONLY: sdk/javascript/README.md)',
 'KS-2117 (seat S 38th filing, 2026-11-09; Backlog; Low; from gate 240 F1). Pass 1 of 2; pass 2 (O106-P2) is the SDK docstrings in src/modules/transfers.ts',
 [RF],
 'PR 2077 (KS-2081) made the six transfer write doors refuse every API key with 403. `sdk/javascript/README.md` Quick Start (lines 18-29) builds a client with `apiKey`, and "Transfers & Delegations" (line 128 on) then shows `client.transfers.initiate` and `client.transfers.approve`. A reader who follows both gets 403. `src/client.ts` sends the key as `X-Api-Key` when no access token is set; `src/modules/transfers.ts` posts to `/api/transfers/initiate`, `/api/transfers/{id}/approve` and `/api/transfers/{id}/cancel`. The 403 is measured at the transfer service by gate 240; the SDK path itself is read, not run.',
 'Two edit points, text only. (1) Quick Start, line 20: the comment `// Initialize with API key` is replaced by a comment that says the transfer write routes refuse API keys. (2) Under the heading `### Transfers & Delegations` (line 128), ONE paragraph is inserted before the code fence saying the transfer write routes (`initiate`, `approve`, `cancel`) refuse every API key with 403 and the client must be built with an `accessToken`. The new text is in the diff below, verbatim. No code line of the examples changes.',
 dd(RF,orr,nr),
 "expect_absent: `// Initialize with API key`\nexpect_present: `// Initialize with an API key (the transfer write routes refuse API keys: see Transfers & Delegations)`\nexpect_present: `refuse every API key with 403 (KS-2081). Build the client with an `accessToken``\n",
 'No SDK run, no request sent. Whether the other SDK modules or any docs site carry an API-key example on these doors is not searched (the ticket says the same). The docstrings in src/modules/transfers.ts are pass 2.')
ot2=rd('transfers.ts')
nt2=rep(ot2,"   * Initiate a new transfer\n","   * Initiate a transfer. A client built with an `apiKey` is refused with 403 (KS-2081); use an `accessToken`.\n")
nt2=rep(nt2,"   * Approve or reject a transfer\n","   * Approve, reject or accept a transfer. A client built with an `apiKey` is refused with 403 (KS-2081); use an `accessToken`.\n")
nt2=rep(nt2,"   * Cancel a transfer\n","   * Cancel a transfer. A client built with an `apiKey` is refused with 403 (KS-2081); use an `accessToken`.\n")
brief('ks_2117_o106_p2_sdk_transfers_docstrings_say_an_api_key_is_refused','KS-2117',
 'KS-2117 pass 2: the SDK transfer docstrings do not say that an API key is refused with 403 (DOC-ONLY: sdk/javascript/src/modules/transfers.ts)',
 'KS-2117 (seat S 38th filing, 2026-11-09; Backlog; Low; from gate 240 F1). Pass 2 of 2; pass 1 (O106-P1) is the README',
 [SF],
 'PR 2077 (KS-2081) made the transfer write doors refuse every API key with 403. In `sdk/javascript/src/modules/transfers.ts` the one-line docstrings of `initiate` (line 85), `approve` (line 111) and `cancel` (line 128) say nothing of it; `initiate` posts to `/api/transfers/initiate` (line 88), `approve` to `/api/transfers/${transferId}/approve` (line 121) and `cancel` to `/api/transfers/${transferId}/cancel` (line 131). The method `approve` takes `action: \'approve\' | \'reject\' | \'accept\'`.',
 'Three edit points, ONE LINE EACH, comment text only (the docstring text line inside each `/** ... */` block). Each becomes a sentence that keeps the original subject and adds that a client built with an `apiKey` is refused with 403 (KS-2081) and should use an `accessToken`. For `approve` the subject also becomes "Approve, reject or accept a transfer", which is what its `action` parameter allows. The new text is in the diff below, verbatim. No code line changes.',
 dd(SF,ot2,nt2),
 "expect_absent: `* Initiate a new transfer`\nexpect_absent: `* Approve or reject a transfer`\nexpect_present: `* Initiate a transfer. A client built with an `apiKey` is refused with 403 (KS-2081); use an `accessToken`.`\nexpect_present: `* Cancel a transfer. A client built with an `apiKey` is refused with 403 (KS-2081); use an `accessToken`.`\n",
 'No SDK run, no request sent. The `reject`, `execute` and delegation methods are not changed (this module has no separate reject or execute method for the doors named). Whether the other doors on the transfer service refuse keys is the ticket\'s claim, not re-measured.')

# ---- KS-2120: transferAccess.ts comment ---------------------------------------------------------------------------
TA=B+'services/transfer/src/services/transferAccess.ts'
oa=rd('transferAccess.ts')
na=rep(oa," *     A person cannot gain them, because the login mints read role and level through closed tables that hold neither.\n",
" *     A person cannot gain them through the closed users tables, which hold neither. The platform-admin login does not read those tables: it mints\n *     platform_admins.role as stored, so a person there could carry a connector role only if someone wrote one into that row (KS-2120). The docker\n *     schema (docker/init-platform/01-platform-schema.sql) CHECKs that column to three values; the Azure migrate script (deployment/azure/migrate/run-platform.sh) declares it with no CHECK.\n")
brief('ks_2120_o106_p1_transfer_access_comment_names_the_platform_admin_login','KS-2120',
 'KS-2120: a comment in transferAccess.ts says no person can carry a connector role, but the platform-admin login mints platform_admins.role as stored (DOC-ONLY: transfer/src/services/transferAccess.ts)',
 'KS-2120 (seat S 38th filing, 2026-11-09; Backlog; Low; gate 240 note N2). The file is the transfer service\'s access decision (an authorization surface): the change is ONE COMMENT, and the hold note should name a tier 1 gate',
 [TA],
 'The doc comment of `isNonUserPrincipal` (transferAccess.ts, the second bullet of the signal list, lines 111-112) says a person cannot gain a connector role "because the login mints read role and level through closed tables that hold neither". That is wrong for one login: `services/auth/src/routes/auth.ts` lines 470-471 build the platform-admin token with `role: platformAdmin.role as any`, and `repositories/userRepo.ts` line 1941 returns `role: row.role` straight from the `platform_admins` row. The docker platform schema CHECKs `platform_admins.role` to three values (`01-platform-schema.sql` lines 79-80); the Azure migrate script declares it `VARCHAR(50) DEFAULT \'admin\'` with no CHECK (`run-platform.sh` line 69). Nothing changes at runtime.',
 'ONE edit point: the single comment line `A person cannot gain them, because the login mints read role and level through closed tables that hold neither.` is replaced by three comment lines that say what is true (new text in the diff below, verbatim). HARD LIMIT: this is a COMMENT inside the `/** ... */` block above `isNonUserPrincipal`. No code line of transferAccess.ts may change in any way: not the regex, not `isNonUserPrincipal`, not a single `if` or `return`.',
 dd(TA,oa,na),
 "expect_absent: `A person cannot gain them, because the login mints read role and level through closed tables that hold neither.`\nexpect_present: `The platform-admin login does not read those tables: it mints`\nexpect_present: `declares it with no CHECK.`\n",
 'No test run: comment only. Not re-read: whether any `platform_admins` row on any box holds a connector value (the ticket does not measure it). Whether to constrain the Azure column is KS-1536\'s question, not this pass. A tier 1 gate is recommended because the file is an authorization decision, even though the diff is a comment.',
 hard='\nHARD LIMIT: the diff touches ONE comment line in `transferAccess.ts`; no code line changes.\n')
