# O66 board screen 2026-11-02 ~09:10 AEDT (Linear read-only, Secuura; tip 03977e89a343, tip_start.out)

Basis: GraphQL `issues(filter:{state:{type:{in:["backlog","unstarted","started"]}}})`, all teams, paged to the end = 962 issues (board_all.json; KS: Backlog 410, In Progress 331, Todo 24, Blocked 3; PS: 142). Keyword filter on title/description for test-only/pin/docs/.sh/openapi/comment gave 249 KS candidates (cand.txt). In Progress treated as taken (the 2026-11-01 screen found those are merged-awaiting-closure). Open PRs: 22 / 125 files (prscan_start.out, planted control services/originate = 6, open_prs_start.json); no candidate file below is in it. The in-flight list was applied.
Finding: most Backlog tickets are "facts only, no fix proposed" or rulings, so few are Spark-briefable. The two best-looking test_only tickets from the 2026-11-01 screen are OVERTAKEN at the tip: KS-1812 (didJwkRefusal pattern clause) is pinned by the gate-15 "SHAPE_REFUSALS" cells in ks1175-identity-anchoring.test.ts :232-259 (`base64 padding (==)` expects exactly ['invalid_string']), and KS-1815's ks726:418 cell still uses the paraphrase but KS-1384 f0b tests now pin the "already been included" clause and Seat W's revision proposes dropping that clause (a product question). Neither briefed.

## Top 10 (best first)
| # | key | title (short) | tier | file | why it fits | caution |
|---|---|---|---|---|---|---|
| 1 | KS-1868 (umbrella, "Refs") | originate/src/routes/verification.ts, 8 unguarded catch reads | code_patch2 | services/originate/src/routes/verification.ts | read-only public verification routes; log + constant 500 or log + fall through; no pre-check; no open PR | originate was avoid-listed earlier; 880/917 return a fallback (still ordinary-Error behaviour) |
| 2 | KS-1868 | originate verificationV2.ts (441, 477) | code_patch2 | services/originate/src/routes/verificationV2.ts | 2 clean log-only sites | small |
| 3 | KS-1868 | originate signatories.ts 6 clean sites | code_patch2 | services/originate/src/routes/signatories.ts | log + constant 500 | revoke/update admin writes; :132 skip (error.code precedes) |
| 4 | KS-1868 | originate thirdPartyVerifiers.ts 6 clean sites | code_patch2 | services/originate/src/routes/thirdPartyVerifiers.ts | log + constant 500 | :193 is the approve (API key) route; :109 skip |
| 5 | KS-1868 | originate anchors.ts 3 route catches (203, 323, 418) + helpers 52, 91 | code_patch2 | services/originate/src/routes/anchors.ts | log + constant 500 | anchoring on-chain path; 91 rethrows |
| 6 | KS-1796 | change-password publishes no 422 | code_patch2 | services/auth/src/auth.openapi.ts:1012 | one file, sibling reset-password :813 is the citable source | docs/openapi/secuura-api.yaml is generated (scripts/ gen) so the yaml needs regen, a second file; contract change |
| 7 | KS-1105 | admin login placeholder shows SYSTEM_ADMIN seed address | code_patch2 | frontend/admin/src/pages/Login.tsx:81 | one-line neutral placeholder | no test home; a frontend text change, may need a UI test pin |
| 8 | KS-1473 | developer portal documents a verify-batch that does not exist | doc_only | services/api-gateway/src/docs/developer-portal.html:294 | remove one documented endpoint line | csrf.ts exclusions for the same path are a second file/decision; portal is a published page |
| 9 | KS-1775 | ks1000 ratchet test: 16 expectRun digit-led string predicates | test_only | services/auth/src/__tests__/ks1000-...baseline.test.ts | one test file | ticket says "no fix proposed", 1461-line file, mutation survivors need design |
| 10 | KS-1593 | nothing pins originate connectorContext reads stay type-checked | test_only | new test | a pin | facts only, fix shape not chosen; needs a tsc-based cell |
Considered and rejected: KS-1812/KS-1815 (above); KS-1681/KS-1770/KS-1764/KS-1415 (decision or append-only docs, "no fix proposed"); KS-1145/KS-1587 (real-Postgres harnesses the Spark cannot execute); KS-1931/KS-1889/KS-1845/KS-1814 (kyc/GDPR, authz, nft pin: signature class or design).
Order rationale: ranks 1-5 are KS-1868 supply from ks1868_remaining.md (verified at the tip). Ranks 6-10 are the only non-KS-1868 board tickets with a one-file shape, all with a caution.

## UNMEASURED
No ticket's fix was run. Descriptions were read to 700-1100 characters, not whole, for KS-1796/1105/1473/1775/1593. Whether a seat already holds a Backlog ticket (assignee/comment) is not visible beyond the comment count (c=0 on 1105/1473/1593/1775/1796).
