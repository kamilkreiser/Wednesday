# In Progress screen, Secuura (KS), 2026-11-15

Read-only. Sources: Linear GraphQL (state "In Progress", team KS, 6 pages of 50, hasNextPage ended false), GitHub GraphQL (22 pages of 100, all PRs, filtered client-side to updatedAt >= 2026-09-01: 1480 PRs), gate verdicts under 0_Brain/reference/*gate*/verdict.md matched by the 12-hex head. Full per-ticket rows: inprogress.json. Method and gaps: notes.md.

## 1. Counts

Total In Progress: **253** (note: board_count.sh refuses over 250; this count is from my own fully paginated query).

| bucket | n |
|---|---|
| L landed | 105 |
| P open PR (P-GATED 70, P-UNGATED 1) | 71 |
| B buildable | 53 |
| H human | 12 |
| D duplicate/stale | 1 |
| X live lane (skip) | 11 |

Sum: 105 + 71 + 53 + 12 + 1 + 11 = 253.

## 2. L list (archive queue for the board seat)

Rule applied: all linked PRs merged AND last comment has no partial-scope wording (my regex, see notes.md). Done rule (card secuura-done-rule-unit-pinned-deployed-no-live-check = a, ruled 2026-10-13): Done is allowed when unit tests pass on develop AND the fix is in the running Kintsugi build; the closing comment must say "no live check possible" where true. I could NOT verify Kintsugi deploy per ticket; rows whose last comment cites a Kintsugi deploy are "Done-rule candidate", the rest are "Tested Not Deployed" until the board seat checks the deploy record.

| key | PR(s) merged | proposed state | facts |
|---|---|---|---|
| KS-2195 | #2227 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-13; "Hono advisories on hono 4.13.13 (GHSA-4m76-xfj5-7975, GHSA-h7mg-cq63-v" |
| KS-2194 | #2226 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-13; "Two new @hono/node-server advisories (GHSA-qv5m-9pm6-hqp3, GHSA-jpvv-r" |
| KS-2182 | #2210 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "KS-1398 step one, L2b: tests/connectors moves from jest to Vitest (roo" |
| KS-2179 | #2208 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "KS-1398 step one, L7: sdk/javascript gets a tsconfig, a standalone loc" |
| KS-2177 | #2207 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "KS-1398 step one, L5: tsconfig cleanup that also works on TypeScript 5" |
| KS-2176 | #2205 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "KS-1398 step one, L1: remove dead ts-jest (referral, vc-issuer) and mo" |
| KS-2169 | #2203 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "transfer cancel after PR 2182: the code comment credits Kam with the w" |
| KS-2168 | #2189 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "docs: Blockchain/Dev/docs/METERING-USAGE-API.md line 26 says a repeate" |
| KS-2166 | #2214 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "kyc: four routes never compare the signed-in caller with the user they" |
| KS-2164 | #2171 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "GHSA-chp3-j5qr-2vfr: effect platform 0.71.7 ships in 25 images and the" |
| KS-2163 | #2177 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "originate 409 mapping: a readable 050 or 051 refusal under any child b" |
| KS-2160 | #2186 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "ks1547 abort-text cell says it pins the whole line but tests a substri" |
| KS-2158 | #2172 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "ks570 mount-auth cells count upstream hits when the response ends, so " |
| KS-2155 | #2179 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "The ks1534 test row labelled "a number LAST of four strings" is three " |
| KS-2153 | #2144 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-09; "KS-2055's two fragments disagree: the cheat says the product code chan" |
| KS-2149 | #2178 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "The cell named RED KS-2121 F1 passes on develop, so by the test file's" |
| KS-2148 | #2147 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-09; "No cell pins verify() resolving verified:false where it used to reject" |
| KS-2141 | #2114, #2183 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-11; "ks1560 jq-link census predicate: legitimate ln spellings judged no lin" |
| KS-2136 | #2208 | Tested Not Deployed | 1 merged PR(s); last ticket comment none; "SDK package: its test command runs vitest with no test files and exits" |
| KS-2121 | #2110 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-08; "transfer: no cell compares the 403 refusal's headers across the six wr" |
| KS-2117 | #2106 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-08; "The JavaScript SDK README shows an API-key setup and then a transfer e" |
| KS-2109 | #2111, #2125 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-09; "KS-1536 follow-up: the one-role-vocabulary guard counts one shape only" |
| KS-2098 | #2164 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-10; "Pre-push hook leg 14 refused a push on 4 failed controls of the slot-l" |
| KS-2095 | #2165 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-10; "Both portals print Block 0 for a document with no block: the verifier'" |
| KS-2089 | #2137 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-09; "Gate 234 residue on merged PR 2053 (KS-957): a stale comment, an overb" |
| KS-2058 | #2051, #2076 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-06; "governance: gate 219's notes on PR 2039: an erased owner can be bound," |
| KS-2038 | #2048 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-06; "transfer service: reject and approve admit any signed-in caller of any" |
| KS-2029 | #2217 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "tests/e2e fixtures: Blockchain/Dev/tests/e2e/tests/fixtures/test-helpe" |
| KS-2027 | #2141 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-09; "originate ks1868 tests: three eslint-disable-next-line no-require-impo" |
| KS-2021 | #2209 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "auth HIBP check: the range-body match compares the suffix only and ign" |
| KS-2016 | #2096 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-08; "api-gateway audit export: no PR 2012 cell asserts the caller's Authori" |
| KS-2012 | #2095 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-08; "api-gateway approve-forward warn line logs error: err.message and no c" |
| KS-2005 | #2206 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "originate seed-demo-users: no cell pins created 1 with failed above 0 " |
| KS-1981 | #1997 | Tested Not Deployed | 1 merged PR(s); last ticket comment none; "Review the mobile/secuura-app audit exclusion before it lapses on 2027" |
| KS-1976 | #2134 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-09; "health-dashboard checkService: no test pins the DOMException name prob" |
| KS-1973 | #2108 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-08; "vc verifier: when the resolver also throws an unreadable value at the " |
| KS-1959 | #2005, #2184 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-11; "vc-issuer: revoke() swallows a failed DB UPDATE — the route answers 20" |
| KS-1937 | #2056 | Done (deploy cited; confirm build) | 1 merged PR(s); last ticket comment 2026-11-06; "originate notificationClient writes the recipient's email address to t" |
| KS-1931 | #2211 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "kyc: dbGetVerificationsByUser returns [] on any read error, so the GDP" |
| KS-1841 | #1907, #2036 | Done (deploy cited; confirm build) | 2 merged PR(s); last ticket comment 2026-11-06; "api-gateway Dockerfile:35: the backup `rm -f` glob misses six name sha" |
| KS-1814 | #1814 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "POST /api/documents/:id/anchor has no role, owner or revoked-document " |
| KS-1785 | #2156 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "Claude Code sessions have no secret-file guard on platform-k: add the " |
| KS-1728 | #1708, #2047, #2074, #2202 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-11-12; "Shell suites grade with `printf ... / grep -q` under pipefail: two unr" |
| KS-1718 | #2126 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-09; "test-account password is derivable from the redacted message, and the " |
| KS-1707 | #1679, #1682, #1683, #2037, #2050 | Tested Not Deployed | 5 merged PR(s); last ticket comment 2026-11-12; "Six baselined advisory rows lapse 2026-10-31 and 15 stale rows need re" |
| KS-1677 | #1647, #1650, #1653, #1663, #1668 | Tested Not Deployed | 5 merged PR(s); last ticket comment 2026-10-20; "m365: the OAuth callback lets any holder of a connection id rebind it " |
| KS-1666 | #1822, #2018, #2055 | Tested Not Deployed | 3 merged PR(s); last ticket comment 2026-11-06; "KS-1633 follow-ups (PR #1623, gate AK1's nine notes): the row left beh" |
| KS-1623 | #1579 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-18; "KS-1114 follow-up (PR #1576 gate F1): stale summary comment, btrim tri" |
| KS-1622 | #1629, #1681, #2033 | Done (deploy cited; confirm build) | 3 merged PR(s); last ticket comment 2026-11-06; "Gate E1 follow-ups: KS-1545 logs nothing for an upstream error status;" |
| KS-1614 | #1567, #2028 | Done (deploy cited; confirm build) | 2 merged PR(s); last ticket comment 2026-11-06; "KS-1542 follow-up (PR #1554 gate): Map/Set/RegExp/Error print {}, {toJ" |
| KS-1568 | #1628 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-19; "KS-1556 follow-up (#1529 round-2 gate m1): four rotate-chain guards ha" |
| KS-1555 | #1528 | Tested Not Deployed | 1 merged PR(s); last ticket comment none; "Four scripts/openapi-examples *.test.ts suites are in no runner path -" |
| KS-1550 | #1526 | Tested Not Deployed | 1 merged PR(s); last ticket comment none; "start-environment.sh and stop-environment.sh run the platform compose " |
| KS-1548 | #1698, #1746 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-05; "KS-1512 follow-up: post-deadline discard, pin the no-window guard, bod" |
| KS-1545 | #1572, #1629 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-06; "GET /api/platform/audit-log drops the platform half invisibly: HTTP 20" |
| KS-1544 | #1600, #1852, #2035 | Done (deploy cited; confirm build) | 3 merged PR(s); last ticket comment 2026-11-06; "platform_audit_log is paged without a tie-break (ORDER BY created_at D" |
| KS-1536 | #1779, #2060, #2061, #2111 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-11-08; "One role vocabulary, seven divergent lists: platform_admin is a super-" |
| KS-1525 | #1601 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-19; "security converters: four rowToApiKey boundary gaps survive the whole " |
| KS-1511 | #1520 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-22; "audit-log limit follow-up: retire the stale accepted baseline entry af" |
| KS-1499 | #1790, #1792, #1794, #1796 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-11-04; "KS-1311 test gaps: RLS asserted on documents only, setup guard bypasse" |
| KS-1494 | #1800, #2024 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-05; "KS-968 follow-ups: the integration suite's loopback guard can be bypas" |
| KS-1490 | #1573, #1580 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-06; "102 tracked files still name a deleted Container Apps host: 22 shipped" |
| KS-1485 | #1583 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-18; "authoritativeTxHash accepts mock_batch_tx_, and nothing pins the place" |
| KS-1466 | #2204 | Done (deploy cited; confirm build) | 1 merged PR(s); last ticket comment 2026-11-12; "api-gateway: an untyped create never meets the catalogue's DOCUMENT ru" |
| KS-1448 | #2072 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-08; "Security: POST /api/notifications still creates a notification for ANY" |
| KS-1402 | #1374, #1437, #1614, #1620, #1638 | Done (deploy cited; confirm build) | 5 merged PR(s); last ticket comment 2026-10-29; "auth GET /api/users/lookup refuses connector tokens, so every Platform" |
| KS-1398 | #2205, #2207, #2208, #2210 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-11-11; "Suggested: move platform-k (outside systemTest + observability) to Typ" |
| KS-1391 | #1693 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-12; "No frontend declares a `test` script — six package.json files, none wi" |
| KS-1387 | #1581 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-19; "A clean image build of platform-k develop fails: services/governance d" |
| KS-1385 | #1549, #1568, #1607 | Tested Not Deployed | 3 merged PR(s); last ticket comment 2026-11-10; "KS-1175 follow-on: the anchors K emits for share / transfer-custody / " |
| KS-1384 | #1838, #1853, #1854, #1857, #1858, #1868, #1874, #1884 | Tested Not Deployed | 8 merged PR(s); last ticket comment 2026-11-10; "One anchor row per (document_id, network): a repeat POST /api/anchors " |
| KS-1377 | #1602, #2031, #2046 | Tested Not Deployed | 3 merged PR(s); last ticket comment 2026-11-06; "validate route follow-ups from the KS-1370 gate: usage_count lost upda" |
| KS-1374 | #1347, #1349 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-09; "Akto scans are now paced to fit the platform's rate limit — test times" |
| KS-1370 | #1338, #1602, #2031, #2071 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-11-05; "Security: validate reads API keys from a boot-only memory map, so a re" |
| KS-1364 | #1365, #1368, #1452 | Tested Not Deployed | 3 merged PR(s); last ticket comment 2026-10-27; "Spec: 85 of 145 request bodies are not marked `required: true`, so Sch" |
| KS-1346 | #1311, #1312, #1316, #1317, #1443 | Tested Not Deployed | 5 merged PR(s); last ticket comment 2026-10-09; "fail500 family: a non-Error throw is logged as [object Object], so its" |
| KS-1337 | #1291, #1295 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-09-26; "k6 runner: the pre-suite path is taken from URL.pathname, so a checkou" |
| KS-1336 | #1286 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-02; "Per-tenant DB readiness: the dormant per-tenant-database path, and the" |
| KS-1300 | #1243 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-09-25; "k6 readYaml adoption: the unit suite that proves it is run by no gate," |
| KS-1292 | #1226 | Tested Not Deployed | 1 merged PR(s); last ticket comment none; "Nothing runs `tsc -p packages/shared` — the push preflight has no proj" |
| KS-1256 | #1396, #2001 | Done (deploy cited; confirm build) | 2 merged PR(s); last ticket comment 2026-11-05; "Connector allow-list still fails OPEN when Redis closes or errors at r" |
| KS-1253 | #1227 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-09-25; "Spec-example guard E7: the secret-name deny list in PREFIXED_UUID_RE i" |
| KS-1233 | #1038 | Done (deploy cited; confirm build) | 1 merged PR(s); last ticket comment 2026-11-06; "In Redis mode platform-settings expires 24 h after the last admin writ" |
| KS-1232 | #1106, #1120, #1517, #1566, #1842, #2020 | Tested Not Deployed | 6 merged PR(s); last ticket comment 2026-11-05; "GET /api/connector/info tells a connector [] (all types permitted) for" |
| KS-1187 | #1019 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-06; "Security: an absolute-form request target bypasses the KS-843 erasure " |
| KS-1157 | #1657, #1665 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-10-20; "Add an OAuth marker to sessions minted by the OAuth grants (so a futur" |
| KS-1155 | #1254 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-27; "packages/shared tree-walking guards exceed vitest's 5 s default under " |
| KS-1129 | #999, #1220, #1280, #1323 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-10-18; "anchoring's raw pg BIGINT reaches persisted and live readers unshaped" |
| KS-1087 | #1008, #1010 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-11-05; "workflow-approve deletes the pending document and answers 200 "Documen" |
| KS-1084 | #1211 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-09-25; "READ ONLY / unverified: the gateway's own Authorization-only calls to " |
| KS-1054 | #1332, #1346, #1348, #1350, #1357, #1359, #1624 | Done (deploy cited; confirm build) | 7 merged PR(s); last ticket comment 2026-11-06; "Fresh databases are FAIL-OPEN until the second boot — 039_rls_fail_clo" |
| KS-1032 | #1546 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-13; "Security: 9 trust-header reads outside auth middleware (pen-test F-04)" |
| KS-1031 | #1183 | Done (deploy cited; confirm build) | 1 merged PR(s); last ticket comment 2026-11-05; "KS-754 gate F-4: DEPLOY CONDITION — apply 048 BEFORE rolling the origi" |
| KS-1015 | #1367, #1375 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-10-23; "Sweeps 2026-09-08: 28 check/operation pairs have no live owner — 18 un" |
| KS-1000 | #874, #1480, #1499, #1506 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-11-02; "services/auth tsconfig EXCLUDES src/__tests__ — every 'tsc: 0 errors' " |
| KS-969 | #892, #989 | Done (deploy cited; confirm build) | 2 merged PR(s); last ticket comment 2026-11-02; "systemTest actor/credential path: provisioning is never invoked, so th" |
| KS-965 | #1202 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-09-25; "87 documentary sites still publish the retired admin credential — wron" |
| KS-864 | #1007, #1009, #1064, #1073, #1148, #2032, #2062 | Tested Not Deployed | 7 merged PR(s); last ticket comment 2026-11-06; "Dead-estate pointers in RUNTIME SOURCE outside deployment/azure — syst" |
| KS-843 | #841, #845, #854, #1019 | Tested Not Deployed | 4 merged PR(s); last ticket comment 2026-11-05; "KS-695 F5: build the dedicated `subjects:erase` scope gate on POST /ap" |
| KS-758 | #1666 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-10-20; "Connector erasure: three permanent failures present as retryable and n" |
| KS-736 | #923, #2086 | Tested Not Deployed | 2 merged PR(s); last ticket comment 2026-10-26; "Gateway mount-auth check scores authenticateToken(false) as green — si" |
| KS-709 | #2065 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-06; "Akto reports a PASS for a test that executed NOTHING — 'clean 0 / not-" |
| KS-692 | #1320, #2017, #2090 | Tested Not Deployed | 3 merged PR(s); last ticket comment 2026-11-06; "Security: /api/status revoke/unrevoke has no tenant ownership check — " |
| KS-663 | #808 | Tested Not Deployed | 1 merged PR(s); last ticket comment 2026-11-11; "The OpenAPI spec is now a consumed contract, but nothing in CI stops i" |
| KS-591 | #1410, #1422, #1451 | Tested Not Deployed | 3 merged PR(s); last ticket comment 2026-10-30; "positive_data_acceptance recurs at scale — 734 failures across 64 ops " |

## 3. P lists

### P-GATED (verdict file names the PR's current head; merge-ready subject to the verdict being GO)

| ticket | PR | head12 | gate file | line 1 |
|---|---|---|---|---|
| KS-2174 | #2052 | b61674e7b763 | 2026-11-12_gate339-tier2-pr2215/verdict.md | PR 2215: GO WITH NOTES (at head ba847c2ef9f9; tier 2; round 1) |
| KS-2173 | #2099 | 8967de8b1755 | 2026-11-13_gate349-tier1-ks2194-hono/verdict.md | PR 2226: GO WITH NOTES (at head 15914b780cb605df02895eb173aeaa2a70c35262; tier 1) |
| KS-2167 | #2188 | 6e5c116d9b9d | 2026-11-12_gate314-tier2-pr2188-2189/verdict.md | PR 2188: GO WITH NOTES (at head 6e5c116d9b9d7c5b2d15d0a4b25ddb9be41210d3; tier 2 stands, N |
| KS-2151 | #2136 | b907ba03bea2 | 2026-11-09_gate291-tier2-pr2135-pr2136-docs/verdict.md | PR 2135: GO WITH NOTES; PR 2136: GO WITH NOTES |
| KS-2150 | #2143 | a9c3bec846c8 | 2026-11-09_gate295-tier2-pr2141-2144/verdict.md | PR 2141: GO; PR 2142: GO WITH NOTES; PR 2143: GO WITH NOTES; PR 2144: GO |
| KS-2147 | #2146 | 20a2e3b32aae | 2026-11-09_gate296-tier2-pr2145-2147/verdict.md | PR 2145: GO WITH NOTES; PR 2146: GO WITH NOTES; PR 2147: GO |
| KS-2146 | #2139 | 65954df16a35 | 2026-11-09_gate293-tier2-pr2137-2139-2140/verdict.md | PR 2137: GO; PR 2139: GO WITH NOTES; PR 2140: GO WITH NOTES |
| KS-2145 | #2087 | 954af815c7b7 | 2026-11-07_gate244-tier1-ks1536/verdict.md | # Gate 244, tier 1, round 1 of 2: KS-1536, PRs 2060 and 2061 |
| KS-2145 | #2158 | 74364b18dcf4 | 2026-11-10_gate302/verdict.md | PR 2158: GO WITH NOTES |
| KS-2144 | #2140 | 83f861da299c | 2026-11-09_gate293-tier2-pr2137-2139-2140/verdict.md | PR 2137: GO; PR 2139: GO WITH NOTES; PR 2140: GO WITH NOTES |
| KS-2138 | #2151 | 5b52d46eeb21 | 2026-11-10_gate297-tier2-pr2148-2149-2151/verdict.md | PR 2148: GO WITH NOTES; PR 2149: GO WITH NOTES; PR 2151: GO WITH NOTES |
| KS-2125 | #2196 | fed1d35ce95c | 2026-11-12_gate320-tier2-pr2196/verdict.md | PR 2196: GO WITH NOTES (at head fed1d35ce95c4983952a8a780b92dc4e2c522e16; tier 2 stands, N |
| KS-2123 | #2149 | d9b899f268a6 | 2026-11-10_gate297-tier2-pr2148-2149-2151/verdict.md | PR 2148: GO WITH NOTES; PR 2149: GO WITH NOTES; PR 2151: GO WITH NOTES |
| KS-2122 | #2162 | 30048d8b295e | 2026-11-10_gate301/verdict.md | PR 2159: GO WITH NOTES |
| KS-2111 | #2159 | 7b54e7cbb6f0 | 2026-11-10_gate301/verdict.md | PR 2159: GO WITH NOTES |
| KS-2099 | #2094 | a84acd840404 | 2026-11-09_gate264-tier2-t15-batch/verdict.md | PR 2093: GO WITH NOTES; PR 2094: GO WITH NOTES; PR 2097: GO; PR 2098: GO |
| KS-2094 | #2154 | 75e8295d8508 | 2026-11-10_gate303/verdict.md | PR 2156: GO WITH NOTES |
| KS-2083 | #2075 | 32aa0d06bc0a | 2026-11-12_gate320-tier2-pr2196/verdict.md | PR 2196: GO WITH NOTES (at head fed1d35ce95c4983952a8a780b92dc4e2c522e16; tier 2 stands, N |
| KS-2075 | #2195 | 3eed5f75fa28 | 2026-11-12_gate319-tier1-pr2195/verdict.md | PR 2195: GO WITH NOTES (at head 3eed5f75fa28cb9b27feeedbe38c4181525faaef; tier 1) |
| KS-2074 | #2085 | 4d4726ca41d9 | 2026-11-07_gate248-tier1-pr2081-ks1171/verdict.md | # Gate 248, tier 1, round 1 of 2: verdicts |
| KS-2071 | #2067 | 0d08681c616d | 2026-11-07_gate246-tier1-services/verdict.md | # Gate 246, tier 1, round 1 of 2: verdict |
| KS-2066 | #2145 | 47cd344c6942 | 2026-11-09_gate296-tier2-pr2145-2147/verdict.md | PR 2145: GO WITH NOTES; PR 2146: GO WITH NOTES; PR 2147: GO |
| KS-2053 | #2093 | afb5f1ef4afe | 2026-11-09_gate264-tier2-t15-batch/verdict.md | PR 2093: GO WITH NOTES; PR 2094: GO WITH NOTES; PR 2097: GO; PR 2098: GO |
| KS-2032 | #2066 | baf577c78e7f | 2026-11-07_gate248-tier1-pr2081-ks1171/verdict.md | # Gate 248, tier 1, round 1 of 2: verdicts |
| KS-2017 | #2160 | b02bd2716cc2 | 2026-11-10_gate303/verdict.md | PR 2156: GO WITH NOTES |
| KS-2015 | #2169 | 3521d7889c93 | 2026-11-11_gate307-tier2-pr2170/verdict.md | PR 2170: GO WITH NOTES |
| KS-2011 | #2185 | 6e9281eb7e24 | 2026-11-12_gate313-tier2-pr2183-2187/verdict.md | PR 2183: GO (at head 16a5be1fafa0e5c37ddf5872849b236e7456529b; tier 2 stands, not raised) |
| KS-1991 | #2161 | 0e50defb7819 | 2026-11-10_gate302/verdict.md | PR 2158: GO WITH NOTES |
| KS-1984 | #2155 | ad404a5a87bb | 2026-11-10_gate303/verdict.md | PR 2156: GO WITH NOTES |
| KS-1970 | #2150 | ef2e7e75b26d | 2026-11-10_gate298-tier1-pr2150-2152/verdict.md | PR 2150: GO WITH NOTES; PR 2152: NO GO |
| KS-1954 | #2170 | 52f482a83436 | 2026-11-11_gate307-tier2-pr2170/verdict.md | PR 2170: GO WITH NOTES |
| KS-1927 | #2176 | 69aca3e281a4 | 2026-11-11_gate311-tier2-pr2176-2177/verdict.md | PR 2176: GO WITH NOTES (at head 69aca3e281a40d3607a1c4b3d054e1b30df90776; tier 2 stands, n |
| KS-1902 | #2123 | 3e8265bae0a1 | 2026-11-09_gate282-tier2-pr2122-2123-2124/verdict.md | PR 2122: GO WITH NOTES; PR 2123: GO WITH NOTES; PR 2124: GO WITH NOTES |
| KS-1868 | #2100 | eb4a08362cfb | 2026-11-09_gate270-tier1-pr2100-r2/verdict.md | PR 2100: GO WITH NOTES |
| KS-1864 | #2102 | 247e62dc7337 | 2026-11-09_gate269-tier2-pr2101-pr2102/verdict.md | PR 2101: GO WITH NOTES; PR 2102: GO WITH NOTES |
| KS-1855 | #2225 | 7d4a82f27063 | 2026-11-13_gate348-tier1-pr2224-2225/verdict.md | PR 2224: GO WITH NOTES (at head a160347eab6655cccac7882bc6933372a475716e; tier 1) |
| KS-1807 | #2135 | e2ada9bf1ea9 | 2026-11-09_gate291-tier2-pr2135-pr2136-docs/verdict.md | PR 2135: GO WITH NOTES; PR 2136: GO WITH NOTES |
| KS-1797 | #2088 | 0f0933afd24b | 2026-11-07_gate252-tier2-batch/verdict.md | # Gate 252 verdict, tier 2 batch round 1 (Secuura/Blockchain) |
| KS-1794 | #2124 | 17f43f1be684 | 2026-11-09_gate284-tier2-pr2124r2-2125-2126/verdict.md | PR 2124: GO WITH NOTES; PR 2125: GO; PR 2126: GO |
| KS-1783 | #2101 | 7e0396990dfd | 2026-11-09_gate269-tier2-pr2101-pr2102/verdict.md | PR 2101: GO WITH NOTES; PR 2102: GO WITH NOTES |
| KS-1670 | #2080 | 83ee8509c985 | 2026-11-09_gate286-tier1-pr2129-pr2130/verdict.md | PR 2129: GO WITH NOTES; PR 2130: GO WITH NOTES |
| KS-1663 | #2194 | fef6e751bf7a | 2026-11-12_gate318-tier2-pr2194/verdict.md | PR 2194: GO WITH NOTES (at head fef6e751bf7a1e5aa5cf5575e78544394c214103; tier 2 stands, N |
| KS-1516 | #2152 | e3534ff2ad91 | 2026-11-10_gate300-tier1-pr2152r2-compare/verdict.md | PR 2152: GO WITH NOTES |
| KS-1497 | #2193 | b6397499151d | 2026-11-12_gate317-tier2-pr2193/verdict.md | PR 2193: GO WITH NOTES (at head b6397499151ddcd9df67ff322f322d5678c8f143; tier 2 stands, N |
| KS-1473 | #2132 | ba0ab4f45349 | 2026-11-09_gate288-tier1-pr2132-pr2127r2/verdict.md | PR 2132: GO WITH NOTES; PR 2127: GO WITH NOTES |
| KS-1415 | #2133 | b6f0c319c5d4 | 2026-11-09_gate289-tier2-pr2133-pr2134/verdict.md | PR 2133: GO WITH NOTES; PR 2134: GO |
| KS-1413 | #2153 | 7a061f5e3f01 | 2026-11-10_gate299-tier1-pr2153-ks1413/verdict.md | PR 2153: GO WITH NOTES |
| KS-1410 | #2059 | 5d8969b36a24 | 2026-11-07_gate250-tier1-pr2059-r2/verdict.md | / PR / Head / Verdict / |
| KS-1209 | #2092 | 3d8423f71024 | 2026-11-08_gate262-tier2-pr2092-ks1209/verdict.md | GO WITH NOTES |
| KS-1208 | #2128 | c7e84537d2ae | 2026-11-09_gate290-tier1-pr2128r2-ks1208/verdict.md | PR 2128: GO WITH NOTES |
| KS-1205 | #2064 | 6c8856baf102 | 2026-11-07_gate253-tier1-pr2064-r2/verdict.md | GO WITH NOTES |
| KS-1163 | #2187 | 8de22966e7f9 | 2026-11-12_gate313-tier2-pr2183-2187/verdict.md | PR 2183: GO (at head 16a5be1fafa0e5c37ddf5872849b236e7456529b; tier 2 stands, not raised) |
| KS-1152 | #2073 | 2684a29d8f57 | 2026-11-08_gate257-tier1-pr2073-r2/verdict.md | # Gate 257, tier 1, round 2 of 2: verdict |
| KS-1104 | #2192 | 311a3d892ee7 | 2026-11-12_gate316-tier2-pr2190-2192/verdict.md | PR 2190: GO WITH NOTES (at head df46ac0e892328e61adc840dd15a56518d4d2558; tier 2 stands, N |
| KS-1090 | #2191 | 96ac07b0cd0d | 2026-11-12_gate315-tier2-pr2191/verdict.md | PR 2191: GO WITH NOTES (at head 96ac07b0cd0daf45a8a27580ca0750de8c826f17; tier 2 stands, N |
| KS-785 | #2127 | 7dc6ff72cf61 | 2026-11-09_gate288-tier1-pr2132-pr2127r2/verdict.md | PR 2132: GO WITH NOTES; PR 2127: GO WITH NOTES |
| KS-784 | #2129 | 902b3161e435 | 2026-11-09_gate286-tier1-pr2129-pr2130/verdict.md | PR 2129: GO WITH NOTES; PR 2130: GO WITH NOTES |
| KS-716 | #2148 | 3746791ca8f0 | 2026-11-10_gate297-tier2-pr2148-2149-2151/verdict.md | PR 2148: GO WITH NOTES; PR 2149: GO WITH NOTES; PR 2151: GO WITH NOTES |
| KS-678 | #2190 | df46ac0e8923 | 2026-11-12_gate316-tier2-pr2190-2192/verdict.md | PR 2190: GO WITH NOTES (at head df46ac0e892328e61adc840dd15a56518d4d2558; tier 2 stands, N |
| KS-625 | #2131 | 89081fae75e5 | 2026-11-09_gate287-tier1-pr2131-ks625/verdict.md | PR 2131: GO WITH NOTES |
| KS-624 | #2130 | 11a394026233 | 2026-11-09_gate286-tier1-pr2129-pr2130/verdict.md | PR 2129: GO WITH NOTES; PR 2130: GO WITH NOTES |
| KS-590 | #2138 | fdf80425e9d5 | 2026-11-10_gate302/verdict.md | PR 2158: GO WITH NOTES |

### P-UNGATED (needs a gate)

- KS-2142 PR #2142 head 3ea830e7e221: no verdict file contains this head (note: verdicts that say NO GO are not merge-ready either; read line 1 above).

Note: a verdict file naming the head does not mean GO. Rows whose line 1 says NO GO or GO WITH NOTES need reading before merge; I did not classify verdicts.

## 4. B list in code-disjoint lanes (develop path measurement: see notes.md UNMEASURED)

### LANE 1 gateway/mcp/security
Globs: Blockchain/Dev/services/api-gateway/**; Blockchain/Dev/services/mcp-server/**; Blockchain/Dev/services/security/**; Blockchain/Dev/services/auth/src/index.ts; Blockchain/Dev/services/auth/src/routes/internal.ts
Model: Opus 5.5 (routing C3: auth/credential/security design surface; KS-1524/1369 mechanical items could drop to Sonnet 5.5)
Tickets (11):
- KS-1369 (P1) api-gateway crashes under load: onProxyReq calls setHeader after the proxied req [merged PR(s) but last comment says part/]
- KS-1533 (P2) Security: an organisation-scoped admin can mint a key for ANOTHER organisation,  [merged PR(s) but last comment says part/]
- KS-1952 (P2) api-gateway: with Redis unavailable, enforceDocumentTypeRules passes every docum [merged PR(s) but last comment says part/]
- KS-1156 (P3) AUTH4 gate records (#983 r2 / #984 r2 / #986 / #987): H-limiter MACHINE_AUTH_MET [merged PR(s) but last comment says part/]
- KS-1524 (P3) KS-1510 gate follow-ups: guard the document-lookup log call, pin the Error text  [merged PR(s) but last comment says part/]
- KS-1553 (P3) KS-1533 follow-up (#1521 gate): the key list compares a raw organisation id with [merged PR(s) but last comment says part/]
- KS-1585 (P3) KS-1570 PR A follow-up (pull request 1535 gate m1-m3, n1-n3): 503 on an infrastr [merged PR(s) but last comment says part/]
- KS-1928 (P3) mcp-server MCP tools return the thrown error text to the client: eight catch blo [merged PR(s) but last comment says part/]
- KS-745 (P3) api-gateway audit export calls /api/audit/logs — a route the security service do [merged PR(s) but last comment says part/]
- KS-1788 (P4) KS-1240 gate follow-ups (#1785): exchange timeout still reads as a downstream 40 [merged PR(s) but last comment says part/]
- KS-1724 (P0) Request-body arrays are uncapped: a JSON array of failing elements costs time an [merged PR(s) but last comment says part/]

### LANE 2 auth + m365
Globs: Blockchain/Dev/services/auth/** EXCEPT src/index.ts and src/routes/internal.ts (Lane 1); Blockchain/Dev/services/m365-integration/**
Model: Opus 5.5 (C3: auth, MFA, OAuth, tenant binding)
Tickets (6):
- KS-1381 (P2) Slot-1 URLs outside KS-1355's four spots: m365's Entra redirect URI defaults to  [merged PR(s) but last comment says part/]
- KS-1673 (P2) m365: no connection is bound to its organisation - any authenticated user can li [merged PR(s) but last comment says part/]
- KS-1968 (P2) auth: the breached-password check (isPasswordBreached, pen-test F-12 item 3) has [merged PR(s) but last comment says part/]
- KS-1500 (P3) ks963 wallet ordering guard (KS-806 round 4): the purity pin on canonicalWalletA [merged PR(s) but last comment says part/]
- KS-1617 (P3) auth social sign-in (Google / Microsoft / Apple): failures in a live environment [merged PR(s) but last comment says part/]
- KS-1458 (P4) KS-1006 follow-ups: two inaccurate statements in the merged change, and the pass [merged PR(s) but last comment says part/]

### LANE 3 originate + governance + transfer
Globs: Blockchain/Dev/services/originate/** EXCEPT src/routes/certifications.ts (live seat) and src/originate.openapi.ts (Lane 5); Blockchain/Dev/services/governance/**; Blockchain/Dev/services/transfer/**
Model: Sonnet 5.5 (C2 multi-file build/test pins); KS-1938 retention sweep and KS-1508 touch data-destroying/security shape: Opus 5.5 read-only first (C4)
Tickets (7):
- KS-1508 (P2) versionedById is caller-controlled but is now an erasure selector: reserve it as [merged PR(s) but last comment says part/]
- KS-1938 (P2) originate retention sweep: one unreadable thrown value stops the whole sweep and [merged PR(s) but last comment says part/]
- KS-1491 (P4) ks1061 mock-completeness guard: negative twin for a wrong helper path, a two-fac [merged PR(s) but last comment says part/]
- KS-1733 (P4) governance GET /api/governance/proposals can still be silently unfiltered or und [merged PR(s) but last comment says part/]
- KS-1875 (P4) GET /api/metering/usage: impossible dates answer 500 not 400, a repeated from/to [merged PR(s) but last comment says part/]
- KS-1904 (P4) Six guarded catch sites of the first KS 1868 batch still pass a non-string messa [merged PR(s) but last comment says part/]
- KS-2085 (P4) transfer after PR 2048: no cell pins the executor reject row, the restart proof  [merged PR(s) but last comment says part/]

### LANE 4 shared package
Globs: Blockchain/Dev/packages/shared/**
Model: Sonnet 5.5 (C2); KS-1459 policy-engine atomicity is security-shaped: Opus 5.5
Tickets (5):
- KS-1589 (P3) KS-1564 follow-ups (pull request 1537 round-2 gate): the ks1564 source guard is  [merged PR(s) but last comment says part/]
- KS-1923 (P3) AuditLogger.flush: an event can still be lost when logging the failure throws; m [merged PR(s) but last comment says part/]
- KS-1459 (P4) KS-1236 follow-ups: the approve level check and write are not atomic, and the lo [merged PR(s) but last comment says part/]
- KS-1972 (P4) event-indexer: isRateLimited reads the thrown value before handleError, so for t [merged PR(s) but last comment says part/]
- KS-1974 (P4) An Error instance with a non-string message passes the new guards in the credent [merged PR(s) but last comment says part/]

### LANE 5 scripts, docs, non-Schemathesis systemTest, tests
Globs: Blockchain/Dev/scripts/**; Blockchain/Dev/docs/**; Blockchain/Dev/Projects Documents/**; Blockchain/Dev/systemTest/** EXCEPT systemTest/schemathesis/**; Blockchain/Dev/tests/**; Blockchain/Dev/services/originate/src/originate.openapi.ts; Blockchain/Dev/services/*/Dockerfile
Model: Sonnet 5.5 (C2/C8: tooling, docs, spec; routing says the Spark/local tier is retired)
Tickets (24):
- KS-1035 (P2) The merge gate cannot see a WITHDRAWN approval — #813 reads approved+clean again [merged PR(s) but last comment says part/]
- KS-1036 (P2) The review-stream overlay covers 57 of 114 active tickets, and DEV-PROCESS still [merged PR(s) but last comment says part/]
- KS-1175 (P2) Anchor / originate / lifecycle-event schemas: accept and anchor platform-s's non [merged PR(s) but last comment says part/]
- KS-665 (P2) KS-256 review follow-ups: 5 example-fixable 400s, the tsx transpile-only spec-ga [no PR]
- KS-723 (P2) Declare the remaining ~157 routed-but-undocumented /api operations in the OpenAP [merged PR(s) but last comment says part/]
- KS-937 (P2) KS-921 residue: the re-link guard's awk parser is still case-sensitive — a lower [merged PR(s) but last comment says part/]
- KS-1033 (P3) KS-926 residue: the three guards that could NOT be wired, and what each needs fi [merged PR(s) but last comment says part/]
- KS-1098 (P3) k6 runner echo mask: -e=NAME=VALUE and -qe NAME=VALUE still print the value, con [merged PR(s) but last comment says part/]
- KS-1316 (P3) ks781 LEG F: a guard DEFINED but never called inside the parser continuation sti [no PR]
- KS-1579 (P3) KS-695 erase-connector round 6 gate follow-ups (pull request 1497): description  [merged PR(s) but last comment says part/]
- KS-1605 (P3) KS-998 item 3 gate follow-ups (#1545): the three Minors of the Opus gate, the ks [merged PR(s) but last comment says part/]
- KS-851 (P3) KS-386 residues from the round-2 gate: G-1 column ordinal drift, G-2 the second- [merged PR(s) but last comment says part/]
- KS-920 (P3) `/shared` ships the TypeScript compiler and a 267 MB dev tree into all 24 runtim [no PR]
- KS-972 (P3) start-secuura.sh banner prints admin@secuura.com / admin123, which has returned  [merged PR(s) but last comment says part/]
- KS-973 (P3) KS-969 round-1 gate residue: the pre-suite step and its own test suite — six ite [merged PR(s) but last comment says part/]
- KS-1145 (P4) ks949 suite coverage (KS-950 / KS-962, #973): ID3's capture half has no size ass [merged PR(s) but last comment says part/]
- KS-1343 (P4) Multi-tenancy docs: eight non-blocking overstatements and Polish notes left by # [merged PR(s) but last comment says part/]
- KS-1468 (P4) ks963 wallet ordering guard: three blind spots in the source scan (template inte [merged PR(s) but last comment says part/]
- KS-2077 (P4) Docs: the architecture reference sends /api/rewards to Staking, the gateway send [merged PR(s) but last comment says part/]
- KS-2079 (P4) launcher census, gate 224 notes on PR 2045: non-shell lifecycle calls, missed sh [merged PR(s) but last comment says part/]
- KS-2156 (P4) ks1728 closed-pipe suite: cell names and header still say printf-only, and the s [merged PR(s) but last comment says part/]
- KS-1366 (P0) PR template still says to dispatch pre-merge-platform-suites.yml and has no Test [merged PR(s) but last comment says part/]
- KS-1388 (P0) observability/ reaches the platform by slot 1's container names (documented), an [merged PR(s) but last comment says part/]
- KS-1449 (P0) POST /api/nft/ipfs/upload: the spec doesn't mark the request body required, so a [merged PR(s) but last comment says part/]

Avoided (live seats): services/anchoring/**, certifications.ts, services/billing/src/**, services/kyc/src/**, services/vc-issuer/src/**, systemTest/schemathesis/**. Lane 1 and Lane 2 split services/auth by two named files; Lane 3 and Lane 5 split originate by originate.openapi.ts. Priority numbers are Linear (1 urgent ... 4 low, 0 none).

## 5. H list

### Waiting on: Live seats (path collision)
- KS-2196: Live-seat path collision, wait for that seat: anchoring path (services/anchoring/**) is the live anchoring seat's
- KS-1933: Live-seat path collision, wait for that seat: services/billing/src/** is a live seat's
- KS-1659: Live-seat path collision, wait for that seat: services/originate/src/routes/certifications.ts is a live seat's
- KS-1451: Live-seat path collision, wait for that seat: systemTest/schemathesis/** is a live seat's
- KS-1375: Live-seat path collision, wait for that seat: services/vc-issuer/src/** is a live seat's
- KS-1295: Live-seat path collision, wait for that seat: services/vc-issuer/src/** is a live seat's
- KS-1284: Live-seat path collision, wait for that seat: anchoring path (services/anchoring/**) is a live seat's
- KS-629: Live-seat path collision, wait for that seat: services/kyc/src/** is a live seat's
### Waiting on: Deploy seat
- KS-1971: Deploy: m365-integration image not rebuilt (done-rule condition ii); needs the deploy seat
### Waiting on: Coordinator/Kam (live sweep)
- KS-1695: Likely touches services/originate/src/routes/certifications.ts (live seat path); gap 2 left open per comment; wait for that seat
- KS-593: Production-adjacent: needs a live Schemathesis sweep on a shared box commissioned by Kam/coordinator; 4 negative-offset sites remain buildable (services/auth users.ts etc.)
### Waiting on: Kam
- KS-915: Kam: close condition not met; KS-1983 (breached demo passwords) needs Kam's ruling per last comment 2026-11-05

Kam items worth a card: (1) KS-915 + KS-1983 breached demo passwords ruling; (2) KS-1226/KS-1313 the :127 15 s budget decision; (3) KS-593 whether to commission a live Schemathesis sweep. KS-1971 is a deploy (rebuild m365-integration), not a Kam ruling.

## 6. D list

- KS-1226: Superseded: last comment says round 2 NO GO, PR 1241 closed, residue moved to KS-1313; item 1 (:127 budget) is an open decision (Kam/Wednesday), so close only after that decision is carded

Only one D found. I grepped titles and first 1500 chars of descriptions for GitHub Actions / workflow_dispatch / .github/workflows / Superseded / duplicate of: only KS-1366 (partial, a template edit still outstanding: stays B in Lane 5) and KS-663 matched. No source-level duplicate proof was run across the board; see notes.md.

## X list (skipped)
KS-1105, KS-1171, KS-1176, KS-1197, KS-1493, KS-1699, KS-1776, KS-1912, KS-1913, KS-2022, KS-657
