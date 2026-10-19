
#### originate (48)

- `937c7d10b` 2026-10-20 Refs KS-1679: drop a caller's certificationId and certifiedAt from the derived certification document (#1646)
- `c9ab6b36f` 2026-10-20 Refs KS-1660: drop a caller-supplied data.parentDocumentId from the derived certification document
- `a4187f0f6` 2026-10-20 Refs KS-1653: documents.ts comments that called the stub-scope admission incidental and uncovered
- `09336b240` 2026-10-20 Refs KS-1661: both anchor heal paths refuse a truthy incoming simulated flag (#1632)
- `05ad5d3ac` 2026-10-20 Refs KS-1658: an unreadable node no longer hides a readable refusal in its cause (#1634)
- `115797747` 2026-10-19 Refs KS-1662: gate AJ1 fix round - pin the two predicates INSIDE the mint helper, and correct two claims of mine
- `adb0dfd58` 2026-10-19 Refs KS-1633: the certify route writes its documents row before it anchors
- `a0da739b6` 2026-10-19 Refs KS-1402: a transfer-custody recipient K does not know is minted as an invited stub, not refused
- `f321e95aa` 2026-10-19 Refs KS-1634: the v2 chain-first fallback carries simulated, with Stuart's no-local-document case
- `52f8777b6` 2026-10-19 Refs KS-1557: The lineage certify path needs access to the PARENT document
- `6ec1b7bad` 2026-10-19 Refs KS-1642: a read probe on the 409 mapping helpers, and the H9 pin its constraint guard never had
- `66faac9ae` 2026-10-19 Refs KS-1629: the anchor read path writes nothing — GET /api/anchors/:documentId no longer mints an anchor_store row (#1617)
- `80868551e` 2026-10-19 Refs KS-1402: a Platform-S custody transfer whose holder resolves is recorded, not a 500 _(also: migrations)_
- `722e07f19` 2026-10-19 Refs KS-1634: label a simulated anchor on chain-first verify, and read verified strictly
- `04a4a3393` 2026-10-19 KS-1612: anchor guard reads external ids; migrations 050/051 bar id claims _(also: anchoring, migrations)_
- `78cb3c393` 2026-10-19 KS-1628 (2 of 2): retire the public POST /api/documents/:id/verify (#1589) _(also: api-gateway, deployment, shared)_
- `f95ad12fe` 2026-10-19 KS-1628 (1 of 3): retire originate's deprecated POST /api/documents/:id/verify (#1587)
- `09ef0612f` 2026-10-19 KS-1628 (precursor): harden the successor verify to the retired handler's rule (#1588)
- `840ac4182` 2026-10-19 KS-1626: read mock_batch_tx_ as a placeholder at all five honesty sites (#1585) _(also: anchoring, api-gateway)_
- `4a547a119` 2026-10-19 Refs KS-1485 item 2: authoritativeTxHash rejects the mock_batch_tx_ placeholder too
- `385fc288f` 2026-10-19 Refs KS-1623 N3: the title lookup's summary comment names every hidden status
- `d900972f2` 2026-10-18 Refs KS-1114: the title lookup hides deleted and expired, whatever the case
- `26378a403` 2026-10-18 KS-1509 (1 of 7 sites): the failed-anchor writer keeps an unknown height NULL (#1569)
- `833984fc9` 2026-10-18 KS-1114: verify finds a document by title, existence only, one tenant
- `d2ec786e6` 2026-10-18 KS-1462 item 1 of 2: migrate-tenant-data describes a thrown non-Error (#1561)
- `8cbadd8d4` 2026-10-15 Refs KS-1385: gate the stored anchor identity overwrite by ownership, hash and anchor type; Kam's custody ruling (c) (#1549) _(also: anchoring)_
- `92d1316ff` 2026-10-13 Refs KS-1594: bound originate's admin API-key mint to the minting admin's own scope
- `d53d80cbb` 2026-10-13 KS-1032: an unconfigured box refuses forged trust headers, and the deploy condition states the real failure mode
- `026c2d161` 2026-10-13 KS-1119: verify never claims a hash match it did not compare
- `d1d9d5561` 2026-10-13 KS-1453: originate stops declaring handlebars, so its runtime image stops shipping it
- `49a41f3cb` 2026-10-13 KS-759: connectorContext reads tenantId and organizationId off the declared JwtPayload
- `e4e320ba4` 2026-10-13 KS-1538: the legacy certify path needs access to the document
- `343a7b4e2` 2026-10-13 KS-695 ask 3 (ii): erase-connector erases in one transaction, key revoked last
- `3a8713376` 2026-10-13 KS-1557 read side: verify trusts certification evidence only if genuine
- `b2085e99f` 2026-10-13 KS-1508: versionedById is server-set; a caller can no longer plant it
- `037575399` 2026-10-12 KS-1333: anchorStateSync writers persist an unknown block number as null, not 0
- `1158045e5` 2026-10-12 KS-1305: npm run generate reaches a generated Prisma client from a fresh checkout
- `17e275ada` 2026-10-12 KS-695 ask 3 (i): erase-connector - the mount, the door and every refusal; nothing is erased yet _(also: api-gateway)_
- `22668829b` 2026-10-12 KS-1158 R1: the anchoredAt carry in markDocumentAnchorFailed keys on the authoritative hash
- `524db0ce6` 2026-10-12 KS-1124: every blob write that goes through updateDocument is atomic
- `a2f575a64` 2026-10-12 KS-1203: an untyped create from a restricted connector is checked as the default type _(also: api-gateway, shared)_
- `ba697cf3d` 2026-10-12 KS-1334: migrate-tenant-data answers a stable code for a failed tenant, not the thrown text
- `7834fd805` 2026-10-10 KS-1345: webhook deliveries answer 500 when the query fails, not an empty 200
- `613070f29` 2026-10-10 KS-1402: originate resolves a transfer-custody holder email itself
- `81d2e5f4c` 2026-10-09 KS-1452: in-range lock refresh clears three handlebars advisories _(also: governance, referral, vc-issuer)_
- `1e7f90e26` 2026-10-08 KS-593: originate refuses a negative offset, a null share recipient, a non-uuid id
- `4afefcbfb` 2026-10-08 KS-998, KS-1435, KS-591: add the 5d WHY comments to the three gate73 lines _(also: transfer)_
- `3d570510b` 2026-10-08 KS-591: declare newHolderId a uuid on the transfer custody request

#### api-gateway (40)

- `4abff9b1a` 2026-10-20 Refs KS-1677: bind the m365 OAuth state to the browser, user and organisation that started the sign-in (#1647) _(also: deployment, docker, m365-integration, migrations, shared)_
- `17ab917aa` 2026-10-20 Refs KS-1262: the per-user notification PUT refuses the reserved userId platform-settings (#1635)
- `88b8ceb9f` 2026-10-20 Refs KS-1622: the platform audit-log route logs an upstream error status on its first window
- `8323f2f70` 2026-10-19 Refs KS-1645 item 3 (partial): the audit export refuses an unknown or repeated type
- `31cfb44dc` 2026-10-19 Refs KS-1195: send the one-hour window explicitly, so "per hour" is this PR's property
- `846ae2788` 2026-10-19 Refs KS-1506: the audit export runs behind authenticateToken, and answers again
- `4e21ce65b` 2026-10-19 Refs KS-1539: the info reader logs the error CLASS of a thrown allow-list read
- `0e2bb271c` 2026-10-19 KS-1471: log the refused connector Bearer's full path, mount prefix included
- `cc2d5820a` 2026-10-19 Refs KS-1526: production File logs are JSON lines, not a column of undefined
- `5d1be7b06` 2026-10-19 Refs KS-1540: /api/connector/info answers 503 when Redis is unavailable
- `2a7e3baa9` 2026-10-19 Refs KS-1504: the no-allowance warning escapes authMethod through logField
- `1f73d7ac8` 2026-10-18 KS-1545 step 1: platform audit-log logs it when it drops the platform half (#1572)
- `9251ae54d` 2026-10-18 KS-1619 part 3: GET /api/document-types logs a non-Error as fail500 does (#1571)
- `36c77dc92` 2026-10-18 KS-1543 parts 2-3 of 3: the last three ESLint warnings in verification.ts (#1560)
- `695388d71` 2026-10-15 KS-1543 part 1 of 2: two deliberately ignored catches in verification.ts become a bare catch (#1556)
- `18de4b7ce` 2026-10-15 KS-1542: a refused array or object forward bound prints as JSON, not through String() (#1554)
- `29bb45342` 2026-10-13 KS-1584: a provisioning key is bound to one organisation _(also: security, shared)_
- `b08ee6299` 2026-10-13 KS-1512: audit-log reads the platform half past the upstream's 200 clamp
- `250596098` 2026-10-13 KS-1518: forward bound refusal message tells 1n from 1 and -0 from 0
- `898a1ae11` 2026-10-13 KS-1532: info reader answers 503 when the settings read throws
- `f39104e71` 2026-10-13 KS-1232: connector/info refuses a non-array allow-list like the create path
- `629349dac` 2026-10-13 KS-1510: document-lookup logs the thrown error and keeps its constant 500
- `88c348375` 2026-10-13 KS-1185: validate the approve forward timeout override at construction
- `1307d2907` 2026-10-12 KS-1180: the _source marker comment says the on-chain predicate reads it
- `8ea75e7cb` 2026-10-12 KS-1359: audit-log refuses a limit above the published maximum of 200
- `8d34fbf08` 2026-10-12 KS-1470: refuse a connector Bearer at the front door, before any mount
- `094d3435b` 2026-10-12 KS-1480: the no-allowance warning escapes its principal and tenant
- `9a958d5b1` 2026-10-12 KS-1479: the per-IP verification limiter counts every /api/v1/ spelling once
- `a28ed5d81` 2026-10-12 KS-1457: the audit finish callback reads the path captured at entry
- `d38302a9a` 2026-10-12 KS-1464: escape the jwt bucket's claims; throttle the no-allowance warning on it
- `0ae2339e6` 2026-10-12 KS-1469: spec gate, verification limiter and CSRF read the path as the router
- `00d27598b` 2026-10-12 KS-1198: authenticateToken refuses a connector JWT presented as a Bearer
- `c78c13d5f` 2026-10-12 KS-1461: gateway path checks fold case; CSRF exclusions end at a boundary
- `db0df4540` 2026-10-12 KS-1205: the per-key limiter buckets an API key only from the key branch
- `672352369` 2026-10-12 KS-801: a case variant of a gateway path gets the canonical path's guard
- `1df34b1bc` 2026-10-12 KS-1364: five POST request bodies are declared required in the published contract _(also: analytics, m365-integration)_
- `e27b9dcef` 2026-10-11 KS-1432: the non-object body guard test calls the route's own predicate
- `a78413d3d` 2026-10-10 KS-1410: audit-export 502 answers a constant message and logs the failed fetch
- `f247ff85b` 2026-10-10 KS-1346: api-gateway fail500 logs a thrown object's type and field names
- `eb19d99d3` 2026-10-09 KS-1410: api-gateway 500 bodies no longer carry thrown error text (10 of 28 sites)

#### security (12)

- `7e01fe495` 2026-10-20 Refs KS-1639: rowToApiKey reads a text form of false as inactive, never active (#1631)
- `390cc0a31` 2026-10-20 Refs KS-1568: ROTATE_CHAIN_WAIT_MS must be a plain number of milliseconds (o6)
- `af788a4c8` 2026-10-19 Refs KS-1377: count the API-key usage IN the database, not from the process-local copy
- `3c0a52221` 2026-10-13 Refs KS-1598: bound the admin-scope liveness guard with COLLATE "C" and pin the whole status vocabulary
- `0bf6ef764` 2026-10-13 KS-1570 (PR B): a platform role writes an ADMIN organisation scope, serialised
- `2cdf1d7a9` 2026-10-13 KS-1570 (PR A): an ADMIN acts on API keys only within its organisation scope _(also: migrations, shared)_
- `7550a969a` 2026-10-13 KS-1553 (a): the key list compares organisation ids in the form the mint stores
- `7c6b3d880` 2026-10-13 KS-1556: rotate changes memory only after COMMIT, per-connector chain, no undo
- `54db1d152` 2026-10-13 KS-1549: concurrent rotates keep exactly one active key
- `69878dc5d` 2026-10-13 KS-1533 arm 1: org-bounded key mint, and a provisioner may not rotate
- `92f68da94` 2026-10-13 KS-880: one home for the security row mappers; index.ts imports them
- `f8c86f859` 2026-10-10 KS-1434: ApiKeyCreateRequest declares rotate, which POST /api/security/keys acts on

#### auth (18)

- `da9e96ffa` 2026-10-20 Refs KS-1653: POST /api/users/stub admits a transfer-custody caller on its own scope (#1630)
- `46e4343a5` 2026-10-19 Merge remote-tracking branch 'origin/develop' into feature/ks-1668-docs-record-kamils-linear-rulings-that-platform-k-docs-omit
- `b40f9451b` 2026-10-19 Refs KS-623: the auth service takes a test token only in an explicit development or test env
- `618d720ec` 2026-10-19 Refs KS-1617 item A.2: log the provider's error_description beside its error on the callback
- `9b90f8ac7` 2026-10-19 Refs KS-1617 item A.3: the social profile-fetch failure names the HTTP status
- `37834600a` 2026-10-19 KS-805: PATCH oauth apps refuses an empty redirectUris, in the route and the published spec
- `61a0fda6e` 2026-10-13 KS-1009: the public wallet status answers whether the wallet is registered, and nothing else
- `06d33fb4b` 2026-10-12 KS-1477: the verification store is memory-only only when NO database is configured
- `efc84906f` 2026-10-12 KS-806: wallet accounts get a collision-free synthetic email; wallet.local is reserved
- `8f674b3c4` 2026-10-12 KS-968: with both platform-admin rows present the email row is neutralised
- `6fa9bf7bd` 2026-10-12 KS-1186: five userRepo reads await fromRow, so a DEK-read DB fault answers 503
- `5bfa5a804` 2026-10-12 KS-1188 F3: the 503 around a backup-code burn says the code may already be spent
- `8dcbddb5a` 2026-10-12 KS-1018 item 3: a configured database never answers a failed verification read from memory
- `96342090c` 2026-10-12 KS-1210: the published OAuth app request schemas carry the closed scope enum
- `f9c7880f9` 2026-10-12 KS-839: the published authorize contract states the wildcard allow-list rule
- `f5a240262` 2026-10-12 KS-1194 part 2: the MFA auto-approve never acknowledges an unpersisted level
- `a31b77577` 2026-10-12 KS-1236: approving a stale PENDING request never lowers the subject's level
- `44afaf482` 2026-10-12 KS-1006: /me/mfa/disable refuses when MFA is on but no secret is stored

#### vc-issuer (2)

- `89956fe92` 2026-10-20 Refs KS-1116: owner-less rows readable by the row tenant's administrators (Kam's ruling a); BH1's missing cells (#1649)
- `c66b834ed` 2026-10-20 Refs KS-1116: bind the presentation and credential GET /:id reads to the principal that created the row (#1648) _(also: deployment, docker, migrations)_

#### m365-integration (6)

- `e712972bc` 2026-10-20 Refs KS-1682: store the refresh token of the account that signed in, and fail closed when it cannot be identified (#1651)
- `2b205bead` 2026-10-20 Refs KS-1673: the four Teams statements on a real SQL engine, and the notify contract (gate AX1 N1, N2)
- `f7d35d628` 2026-10-20 Refs KS-1673: bind Microsoft Teams webhooks to the caller's organisation (PR B) + gate AS1's cell D
- `9207fe336` 2026-10-20 Refs KS-1673: bind every org-owned m365 resource to the caller's organisation
- `a66cd6a4d` 2026-10-20 Refs KS-1671: the m365 OAuth callback reads only string query values
- `5a205376c` 2026-10-19 Merge remote-tracking branch 'origin/develop' into feature/ks-1668-docs-record-kamils-linear-rulings-that-platform-k-docs-omit

#### anchoring (5)

- `ad784e702` 2026-10-19 Refs KS-1603: refuse an anchor write onto another tenant's document (the interim ownership check) (#1615)
- `7e2f8157c` 2026-10-19 KS-1385 (b): a holder's update keeps the first-anchored issuer fields
- `3a870ba75` 2026-10-19 Refs KS-1628 item 3: anchorReadback reads placeholders via the exported prefix
- `77a8b41ef` 2026-10-11 KS-591: six POST request bodies are declared required in the published contract _(also: staking, transfer)_
- `fa24bdded` 2026-10-07 KS-1437: in-range lock refresh clears shell-quote, MCP SDK and pbkdf2 advisories _(also: issuer, mcp-server, shared)_

#### referral (2)

- `06d0109c8` 2026-10-13 KS-1582: bound the referrer-wallet read in time, bind its tenant in SQL
- `c855cfc26` 2026-10-13 KS-1223: the referrer wallet is the user's linked wallet, not the header

#### transfer (2)

- `87f005901` 2026-10-10 KS-1410: transfer process-expired 500 logs the error text instead of returning it
- `2c27ddfee` 2026-10-07 KS-1435: transfer reject refuses a wrong-typed signature with 400

#### timestamping (1)

- `4c962a7e4` 2026-10-12 KS-753: a mock TSA token is no longer reported, stored or verified as verified

#### nft-certificate (1)

- `1fba82ddb` 2026-10-09 KS-1449: mark six nft request bodies required in the published contract

#### mcp-server (2)

- `8a093d1de` 2026-10-19 Refs KS-1620 item 1: bound the gateway text get_info relays to 200 characters
- `f998e343a` 2026-10-18 KS-1541: MCP get_info names a gateway refusal, not a missing endpoint (#1566)

#### governance (1)

- `b45b69171` 2026-10-19 Refs KS-1387: the governance router carries an explicit Router type

#### tenant-provisioning (1)

- `4f92eef4a` 2026-10-19 Refs KS-1544: page the platform audit log in a total order (created_at, then id)

#### admin (1)

- `a7cffc8d9` 2026-10-13 KS-1564: the Admin Dashboard API Keys page lists and mints for an organisation the operator chooses

#### shared (2)

- `cd63883c6` 2026-10-20 Refs KS-1677: pin the PKCE verifier's secrecy and randomness, and evaluate the bicep redirect's ternary (#1650)
- `29434e554` 2026-10-12 KS-1317: packages/shared npm test names the missing install instead of rc 127

#### whatsapp-bot (3)

- `b5742c3e1` 2026-10-19 Refs KS-1624 F1: the WhatsApp bot's banner prints the base it actually calls
- `8a9970511` 2026-10-19 Refs KS-1490: the WhatsApp bot builds one slash before /api, not two
- `aa9ca9de9` 2026-10-12 KS-812: whatsapp-bot defaults to demo-pk.secuura.net, not a dead Container Apps host

#### deployment (1)

- `94a8d4ff4` 2026-10-19 Refs KS-1668: record the maintainers' Linear rulings that the platform-k docs omitted or contradicted

#### docker-compose.yml (1)

- `af2366e7e` 2026-10-13 KS-1355: stack tooling derives the slot (spots 2b, 3, 4) + the shared guard

#### tooling / tests / docs / history only (105)

- `11af03696` 2026-10-20 Refs KS-1116: pin ruling (a)'s role set and whole-tenant compare (gate BJ1 NOTE 2) (#1652)
- `5ac66264b` 2026-10-20 Refs KS-1668: ROLES inventory recorded two superseded states of one decision (#1645)
- `640bc7efd` 2026-10-19 Merge pull request #1642 from Secuura/feature/ks-1607-schemathesis-4310-turns-6-systemtestschemathesis-unit-tests
- `292fe0b16` 2026-10-20 Refs KS-1676: pin the fifteen unpinned guard clauses in both anchor-heal functions
- `513371a34` 2026-10-20 Refs KS-1500 + KS-1468: pin the canonicalWalletAddress import source and read the SELECT pin through the blanked body
- `c129c63cf` 2026-10-20 Refs KS-1634: pin the v2 chain-first path and the truthy-simulated rule at its site (gate AG1 N2, N3)
- `0f472ec20` 2026-10-20 Refs KS-1671: cells for the OAuth callback's code read (gate AP1 note N3)
- `69e72e98d` 2026-10-19 Refs KS-1668: record the Done rule (tested + works + deployed) as skill section 5g
- `c0171028f` 2026-10-19 Refs KS-1668: docs say Redis 8 (KS-368 2026-07-02, KS-366 2026-07-03)
- `b01dbdf8a` 2026-10-19 Refs KS-1503 Minor 1: say what an unverifiable Bearer actually gets at the front door
- `072713896` 2026-10-19 Refs KS-1637 Minor 1: a real-app cell for the retired /api/documents/:id/verify
- `ce9860621` 2026-10-19 KS-1638: the pre-push hook no longer leaks its controls into leg 14, so ALLOW_FORCE=1 passes
- `9512cc70d` 2026-10-19 Refs KS-1507: pin what "configured" means for DATABASE_URL - empty is memory-only
- `b8168a871` 2026-10-19 Refs KS-1595 item 1: pin that the GDPR erasure routes pass the principal's context
- `1e914e2b6` 2026-10-19 Refs KS-1525: pin two rowToApiKey isActive boundaries (G1, G10) that survived the suite
- `7b6d479a5` 2026-10-19 Refs KS-1627 (2 of 2): pin the info reader's 200 with the REAL redis module in Redis mode
- `9f1794488` 2026-10-19 Refs KS-1621 (2 of 2): pin that a thrown class instance logs its constructor name
- `fae056052` 2026-10-19 Refs KS-1621 (1 of 2): pin that a real prior height of 0 is carried forward as 0
- `83ed01af7` 2026-10-19 KS-1627: pin the info reader's 503 against the real redis module in fallback (#1586)
- `6184eaa0a` 2026-10-19 Refs KS-1497: prisma-generate refuses a symlinked or non-directory staging dir
- `a3e6e0474` 2026-10-19 Refs KS-1482: pre-push judges a rename out of Blockchain/Dev by its old path too
- `ab55cba88` 2026-10-19 Refs KS-1619 p2: migrate-tenant-data goes on to the next tenant after one fails
- `8f57c6e24` 2026-10-18 Refs KS-1619 p1: the approve forward's reply is drained to its end in chunks
- `db9bd1602` 2026-10-18 KS-1613 items 1+2: preflight step() abort quotes the text after the slash (#1570)
- `1197ab38a` 2026-10-18 KS-724: quote Kam's Accept-as-built ruling beside the locked-account exclusion (#1565)
- `5002b06f7` 2026-10-18 KS-1614 item 4: a refused [1n] prints its type tag, not the accepted text 1 (#1567)
- `d0c5d2e0e` 2026-10-16 Merge pull request #1564 from Secuura/feature/ks-1618-systemtest-drop-verbatim-from-the-remaining-kamil-verbatim
- `fe0656b60` 2026-10-16 Merge pull request #1563 from Secuura/feature/ks-983-systemtest-no-suite-drives-a-path-spelling-variant-the-ks
- `a92f46e14` 2026-10-16 Merge pull request #1562 from Secuura/feature/ks-1616-systemtest-anchoring-orchestration-recreates-services-under
- `76698952a` 2026-10-15 Merge pull request #1559 from Secuura/feature/ks-1447-systemtest-schemathesis-implement-kams-2026-08-26-ruling-on-squashed
- `0543ff1e6` 2026-10-15 Merge pull request #1557 from Secuura/feature/ks-1615-akto-image-2382-2385-schemathesis-4310-4311-app-only-bump
- `0bb4f17ca` 2026-10-15 KS-1547: preflight step() reads the leg denominator as digits, not up to the first space (#1552)
- `53b429ed6` 2026-10-15 KS-1605 item 5: ks884 S4 and S10 build commits distinct from earlier cells (#1553)
- `e67e0dc19` 2026-10-14 Merge pull request #1551 from Secuura/feature/ks-1396-platform-k-systemtest-observability-typescript-702
- `458d6bcf3` 2026-10-14 Merge pull request #1550 from Secuura/feature/ks-1478-akto-image-2371-2383-release-v2383-2026-10-13-testing-image
- `0662f7213` 2026-10-13 KS-998 item 3: the gate checks lock sources and scrubs the install env
- `405e33a10` 2026-10-13 KS-998 item 2: the hook judges each pushed ref, the gate the pushed commit
- `0026a43e6` 2026-10-13 KS-998 item 1: the formatting gate installs an absent node_modules
- `b28bfaecf` 2026-10-13 KS-998 item 3: cover the hook's fail-closed missing-gate branch
- `5d5aea41f` 2026-10-13 KS-865 / KS-1347 / KS-1137 F-4: three tooling residues, one test pass each
- `81ac1ea60` 2026-10-13 KS-1521: the governance budget pin reads the timeout jest applies
- `05a72c85c` 2026-10-13 KS-1517: a stale @secuura/shared build reads CANNOT RUN, not NEW test-file type errors
- `559947aa2` 2026-10-13 KS-1351 item 3: vc-issuer joins the test-file type-check ratchet at every push
- `425ad3e00` 2026-10-13 KS-1511: pin that an array or repeated audit-log limit is refused
- `4ec53e187` 2026-10-13 KS-1519: auth ratchet cells fail with the checker's output as the message
- `551dc9808` 2026-10-13 KS-1520: pin leg 16's default run without an install, fix its failure text
- `f6f2a539f` 2026-10-13 KS-1489: the test-type ratchet refuses a swap, @ts-nocheck and a narrowed tsconfig
- `8573851a2` 2026-10-13 KS-1518: pin that a BigInt and negative zero are refused as the forward bound
- `bfd42c980` 2026-10-13 KS-1237: pin the refusal message of a non-array connector allow-list
- `c63cec1f6` 2026-10-13 KS-1328: the other 16 services' db.retry tests get a 60 s budget (15 vitest, 1 jest)
- `36f0f56f3` 2026-10-13 KS-1090: preflight leg 16 also gates the api-gateway test-file ratchet
- `cc2939bbf` 2026-10-12 KS-1090: type-check the api-gateway test files against a shrinking baseline
- `6b978ca38` 2026-10-12 KS-1487: the test-file type-check ratchet runs at push time (preflight leg 16)
- `361537eed` 2026-10-12 KS-1496: pin DEL, the C1 range, the quote and the machine set as closed
- `3fd441aa6` 2026-10-12 KS-1311: the KS-1263 route cells run as the app role, with RLS in the loop
- `092da3ae7` 2026-10-12 KS-811: the 403 code set of POST /api/documents is derived from source and pinned
- `bfd79774e` 2026-10-12 Merge pull request #1494 from Secuura/feature/project-history-2026-10-12-closeout
- `09ad9c840` 2026-10-12 Merge pull request #1493 from Secuura/feature/project-history-2026-10-12
- `4695b8d42` 2026-10-12 Merge pull request #1492 from Secuura/feature/ks-1476-bump-systemtest-schemathesis-pin-4300-4301-release-v4301-3
- `dd015e735` 2026-10-12 KS-1267: the /transfer-custody owner flip throwing is pinned to record no provenance row
- `50662382c` 2026-10-12 KS-1159: the shared-mock completeness guard has the regression cells its definition of done names
- `1b7b8d7d5` 2026-10-12 KS-884: pre-push names refs/heads/develop, so a tag named develop cannot be the base
- `8cfab55b0` 2026-10-12 KS-1000: the auth test files are type-checked, against a baseline that can only shrink
- `b4a245fba` 2026-10-12 KS-1131 items 3 and 4: the ks963 wallet ordering cell sees every call and its own body
- `2d151b08e` 2026-10-12 KS-1193 F3: the memory-fallback controls tell the entry from an empty return
- `c043929b7` 2026-10-12 KS-1405: run-schemathesis.sh defaults FINDINGS_DIR to a temp dir, not the CWD
- `65d7722f8` 2026-10-12 KS-1417: env.local.example drops API_GATEWAY_PORT, a key no tracked file reads
- `9a42ce02e` 2026-10-12 KS-1355: dev-reload.sh names the current slot's container, not slot 1's
- `4a7cc1f69` 2026-10-11 KS-1426: preflight clean-room leg names the tracked lockfiles it did not install
- `785cb6715` 2026-10-10 KS-1417: env.example no longer sets API_GATEWAY_PORT, a key no tracked file reads
- `8a7b7ece0` 2026-10-10 KS-1456: the runner's failed-run message no longer names a defect it does not have
- `40ed3573b` 2026-10-10 KS-937: the re-link guard accepts relative destinations and uid-0 users with a group
- `76b683c7d` 2026-10-10 KS-998: the format gate runs each format:check with an empty stdin
- `4aa5cb38b` 2026-10-10 KS-1328: pin the kyc db-retry suite to a 60 s describe budget
- `20c975012` 2026-10-10 KS-1355: stack_guard lists a project once when its owners disagree
- `ae9bf6828` 2026-10-10 KS-808: run-migrations.sh no longer counts skipped migrations as applied
- `09a7b2ec8` 2026-10-09 Merge pull request #1439 from Secuura/feature/project-history-2026-10-09-schemathesis-4-30-0
- `e919265db` 2026-10-09 Merge pull request #1438 from Secuura/feature/ks-1455-bump-systemtest-schemathesis-pin-4294-4300-or-later-release
- `44753e3e7` 2026-10-09 KS-1171: pin the inclusive 60s boundary where a second fee-paying tx may be minted
- `4db6c7743` 2026-10-09 KS-1139: smoke-test counters no longer abort the script under errexit
- `349b35c91` 2026-10-09 KS-1274: job 04 fails a scan when trivy reports neither Results nor ArtifactName
- `0a6177ea5` 2026-10-08 KS-1450: unblock preflight leg 14 - mark baseline reasons, exempt provenance run ids
- `ddea00555` 2026-10-08 KS-1164: assert the k6 status-code breakdown prints locale-grouped counts
- `eae08a3f4` 2026-10-07 Merge pull request #1425 from Secuura/feature/project-history-2026-10-07-k6-guard-observability-images
- `0eb04c31e` 2026-10-07 Merge pull request #1424 from Secuura/feature/schemathesis-baseline-triage-ks-1445-premerge-pairs
- `ed346e6d9` 2026-10-07 Merge pull request #1421 from Secuura/feature/ks-1445-pin-systemtest-k6-to-the-latest-release-or-later-the-macs
- `b280b74ff` 2026-10-07 Merge pull request #1420 from Secuura/feature/project-history-2026-10-07-schemathesis-baseline-reconciled
- `185d2d53e` 2026-10-07 Merge pull request #1419 from Secuura/feature/ks-1361-schemathesis-baselinejson-lags-the-linear-registers-37-of-90
- `652cf5f6e` 2026-10-07 Merge pull request #1418 from Secuura/feature/project-history-2026-10-07-pool-draw-guard
- `2feb749f6` 2026-10-07 Merge pull request #1417 from Secuura/feature/ks-1414-schemathesis-429x-reports-negative_data_rejection-on
- `eef784a32` 2026-10-07 Merge pull request #1416 from Secuura/feature/project-history-2026-10-07-schemathesis-4294-merged
- `5b8624615` 2026-10-07 Merge pull request #1414 from Secuura/feature/ks-1439-bump-systemtest-schemathesis-pin-4293-4294-fixes-only-35
- `9ce888c81` 2026-10-07 Merge pull request #1415 from Secuura/feature/project-history-2026-10-07-schemathesis-4294
- `eb67b9659` 2026-10-07 Merge pull request #1413 from Secuura/feature/project-history-2026-10-07-akto-2371
- `74a91addc` 2026-10-07 Merge pull request #1412 from Secuura/feature/project-history-2026-10-07-akto-2371
- `4132b84ad` 2026-10-07 Merge pull request #1411 from Secuura/feature/ks-1440-akto-image-23610-2371-release-v2371-2026-10-06-both-_local
- `841e4ab13` 2026-10-07 KS-1313: the child vitest verdict comes from the JSON report, never from its text
- `7bcc2ed54` 2026-10-07 KS-998: the format gate reads its in-this-push label literally, not as a regex
- `147ae4420` 2026-10-07 KS-1136: report a present but unparseable security artefact instead of a clean scan
- `69f2045af` 2026-10-07 KS-1436: the tenant-isolation runner's stderr goes to its own file
- `b39051390` 2026-10-06 Merge pull request #1405 from Secuura/feature/project-history-2026-10-06-systemtest-batch
- `40270d263` 2026-10-06 Merge pull request #1402 from Secuura/feature/ks-571-d-docs-and-html
- `2677a1258` 2026-10-06 Merge pull request #1403 from Secuura/feature/ks-571-a-schemathesis-harness
- `9d8bc3b85` 2026-10-06 Merge pull request #1401 from Secuura/feature/ks-571-b-package-refresh
- `8a8d7b969` 2026-10-06 Merge pull request #1400 from Secuura/feature/ks-571-c-observability-tests
