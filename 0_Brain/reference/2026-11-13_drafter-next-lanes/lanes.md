# Next lanes after the B-lane merge queue emptied (Secuura/Blockchain), read-only sweep, 2026-11-13

Drafter output for Wednesday. Nothing was written, merged, commented or pushed anywhere but this file.

## BLUF

- **Step 1, merge candidates: 79 open PRs have a GO or GO WITH NOTES verdict at their current head** (14 GO, 65 GO WITH NOTES; tier 1: 24, tier 2: 47, tier not in folder name: 8). All kksecura, all base develop, all MERGEABLE. 2 are CLEAN (2198, 2197); the rest are UNSTABLE (CI red or skipped, see Caveats). Plus 1 open PR whose verdict at head is NO GO (887).
  - The "queue is empty" premise is about briefed merges, not about verdicted PRs: **79 verdicted PRs are open and unmerged.** Why they were never briefed for merge is UNMEASURED (no inbox, no Linear access).
- **Step 2, gate candidates: 1** kksecura PR with no verdict of its own at its current head: **2079** (KS-657). Everything else of ours has a verdict at head (after correcting a 12-hex-only matcher, see Method). 0 PRs have a READY FOR GATE mail measured: UNMEASURED (inbox not available).
- **Step 3, raise candidates: 5 held Ornith/Spark passes, dated 2026-10-28 to 2026-11-11, with no PR evidence** (KS-1105, KS-1912, KS-1913, KS-1197, KS-1776). 434 READY_* files sit in night/; 248 of them have no `diff --git` header so their target file is UNMEASURED; older than 2026-10-19 the merged-PR window (500 PRs back to 2026-10-19) does not reach, so those are UNMEASURED too.
- **PR 2075 and PR 2099: both are mergeable candidates now** (verdict at head, Kam cards ruled `a`). Owed items below.
- develop = 410feda1a85e54b82a65464607f4761c2da3bb1b (git ls-remote origin refs/heads/develop, at this sweep, equals the commission's pin).

## Method and instruments (every figure)

- Open PR list and heads: `gh pr list -R Secuura/Distributed_Secuura --state open --limit 500 --json ...`, GH_CONFIG_DIR = Blockchain project's. Result: 92 open (81 kksecura, 10 dependabot, 1 StuJam-Secuura). Per-PR detail (files, mergeable, mergeStateStatus, body): `gh pr view <n> --json ...` x81; heads from the two reads agreed on all 81 (mismatch list empty).
- Verdicts: 600 `verdict.md` files under `0_Brain/reference/*gate*/` (`ls | wc -l`). A verdict counts as AT HEAD only when one line names the PR number and the live head hex (12 first; a second pass with 8 hex caught short-form heads such as 2142's `3ea830e7e22`) and the file states a verdict for that PR. Where a gate folder holds several rounds, the highest gate number wins. Verdict word for 15 PRs (2142, 2092, 2090, 2089, 2088, 2087, 2085, 2081, 2080, 2075, 2073, 2066, 2064, 2059, 2052) was read by hand from the folder's own table or first line because line 1 does not use the `PR n:` form. Positive control: the matcher returned 79 hits on known-verdicted PRs; the 8-hex pass found 2142 that the 12-hex pass missed (so the first pass was not blind-proof, which is why the second pass exists).
- File overlap census: set intersection over the 81 kksecura PRs' `files` lists (instrument: `gh pr view --json files`). Overlap with merged-since or develop moves is not measured; mergeable=MERGEABLE for all 81 is GitHub's own reading.
- Kam cards: `decision_queue.sh prior --title "<title minus Refs KS-n>" --client-project Secuura/Blockchain` per PR, plus `decision_queue.sh list`. The `prior` matcher is a fuzzy word matcher over past messages (a long phrase gave hits, a bare ticket key gave 0 for all 81, a bare "role change" gave 0), so a hit count is NOT a hold. The last column is that hit count; it is noise except where a named ruled card is cited below. `list` shows 1 `[open ]` card in total, and it is Datasec/Security-Composer, not Secuura. Control: `list` returned the Secuura KS-2060 and KS-2083 cards, so reading works.
- CI: `gh pr checks 2177` (all failures at 2-3 s plus skipped suites) and `gh pr checks 2198` ("no checks reported"). Cause of the failures UNMEASURED.

## Step 1. Merge candidates (79)

Sorted newest PR first. "head match yes" for all rows (the filter). Tier "?" = the gate folder name carries no tier. Kam-card column is the noisy dq hit count; see the special section for real cards.

| PR | ticket | verdict | tier | head match | gate folder | files | overlaps open PR | mergeStateStatus | dq prior hits |
|---|---|---|---|---|---|---|---|---|---|
| 2198 | KS-1868 | GO WITH NOTES | 1 | yes | 2026-11-12_gate321-tier1-pr2197-2198 | 3 | - | CLEAN | 6 |
| 2197 | KS-1868 | GO WITH NOTES | 1 | yes | 2026-11-12_gate321-tier1-pr2197-2198 | 2 | - | CLEAN | 1 |
| 2196 | KS-2125 | GO WITH NOTES | 2 | yes | 2026-11-12_gate320-tier2-pr2196 | 4 | - | UNSTABLE | 4 |
| 2195 | KS-1988,KS-2075 | GO WITH NOTES | 1 | yes | 2026-11-12_gate319-tier1-pr2195 | 4 | - | UNSTABLE | 0 |
| 2194 | KS-1663 | GO WITH NOTES | 2 | yes | 2026-11-12_gate318-tier2-pr2194 | 3 | - | UNSTABLE | 3 |
| 2193 | KS-1497 | GO WITH NOTES | 2 | yes | 2026-11-12_gate317-tier2-pr2193 | 4 | - | UNSTABLE | 5 |
| 2192 | KS-1104 | GO WITH NOTES | 2 | yes | 2026-11-12_gate316-tier2-pr2190-2192 | 2 | - | UNSTABLE | 0 |
| 2191 | KS-1090 | GO WITH NOTES | 2 | yes | 2026-11-12_gate315-tier2-pr2191 | 9 | - | UNSTABLE | 0 |
| 2190 | KS-678 | GO WITH NOTES | 2 | yes | 2026-11-12_gate316-tier2-pr2190-2192 | 3 | - | UNSTABLE | 1 |
| 2188 | KS-2167 | GO WITH NOTES | 2 | yes | 2026-11-12_gate314-tier2-pr2188-2189 | 2 | - | UNSTABLE | 2 |
| 2187 | KS-1163 | GO WITH NOTES | 2 | yes | 2026-11-12_gate313-tier2-pr2183-2187 | 3 | - | UNSTABLE | 3 |
| 2185 | KS-2011 | GO WITH NOTES | 2 | yes | 2026-11-12_gate313-tier2-pr2183-2187 | 2 | - | UNSTABLE | 3 |
| 2177 | KS-2163 | GO | 2 | yes | 2026-11-11_gate311-tier2-pr2176-2177 | 2 | - | UNSTABLE | 3 |
| 2176 | KS-1927 | GO WITH NOTES | 2 | yes | 2026-11-11_gate311-tier2-pr2176-2177 | 2 | - | UNSTABLE | 2 |
| 2170 | KS-1954 | GO WITH NOTES | 2 | yes | 2026-11-11_gate307-tier2-pr2170 | 2 | - | UNSTABLE | 0 |
| 2169 | KS-2015 | GO WITH NOTES | 2 | yes | 2026-11-10_gate306-tier2-pr2166-2169 | 2 | - | UNSTABLE | 0 |
| 2162 | KS-2122 | GO WITH NOTES | ? | yes | 2026-11-10_gate301 | 5 | 2149 | UNSTABLE | 2 |
| 2161 | KS-1991 | GO WITH NOTES | ? | yes | 2026-11-10_gate302 | 11 | 2138 | UNSTABLE | 4 |
| 2160 | KS-2017 | GO WITH NOTES | ? | yes | 2026-11-10_gate303 | 2 | - | UNSTABLE | 4 |
| 2159 | KS-2111 | GO WITH NOTES | ? | yes | 2026-11-10_gate301 | 6 | - | UNSTABLE | 0 |
| 2158 | KS-2145 | GO WITH NOTES | ? | yes | 2026-11-10_gate302 | 4 | 2087 | UNSTABLE | 10 |
| 2155 | KS-1984 | GO WITH NOTES | ? | yes | 2026-11-10_gate303 | 2 | - | UNSTABLE | 0 |
| 2154 | KS-2094 | GO WITH NOTES | ? | yes | 2026-11-10_gate303 | 2 | - | UNSTABLE | 1 |
| 2153 | KS-1413 | GO WITH NOTES | 1 | yes | 2026-11-10_gate299-tier1-pr2153-ks1413 | 2 | - | UNSTABLE | 4 |
| 2152 | KS-1516 | GO WITH NOTES | 1 | yes | 2026-11-10_gate300-tier1-pr2152r2-compare | 3 | - | UNSTABLE | 0 |
| 2151 | KS-2138 | GO WITH NOTES | 2 | yes | 2026-11-10_gate297-tier2-pr2148-2149-2151 | 1 | - | UNSTABLE | 4 |
| 2150 | KS-1970 | GO WITH NOTES | 1 | yes | 2026-11-10_gate298-tier1-pr2150-2152 | 2 | - | UNSTABLE | 3 |
| 2149 | KS-2123 | GO WITH NOTES | 2 | yes | 2026-11-10_gate297-tier2-pr2148-2149-2151 | 1 | 2162 | UNSTABLE | 5 |
| 2148 | KS-716 | GO WITH NOTES | 2 | yes | 2026-11-10_gate297-tier2-pr2148-2149-2151 | 1 | - | UNSTABLE | 7 |
| 2147 | KS-2148 | GO | 2 | yes | 2026-11-09_gate296-tier2-pr2145-2147 | 1 | - | UNSTABLE | 0 |
| 2146 | KS-2147 | GO WITH NOTES | 2 | yes | 2026-11-09_gate296-tier2-pr2145-2147 | 1 | - | UNSTABLE | 0 |
| 2145 | KS-2066 | GO WITH NOTES | 2 | yes | 2026-11-09_gate296-tier2-pr2145-2147 | 1 | - | UNSTABLE | 3 |
| 2144 | KS-2153 | GO | 2 | yes | 2026-11-09_gate295-tier2-pr2141-2144 | 2 | - | UNSTABLE | 2 |
| 2143 | KS-2150 | GO WITH NOTES | 2 | yes | 2026-11-09_gate295-tier2-pr2141-2144 | 2 | - | UNSTABLE | 1 |
| 2142 | KS-2142 | GO WITH NOTES | 2 | yes | gate295-tier2-pr2141-2144 | 1 | - | UNSTABLE | 1 |
| 2141 | KS-2027 | GO | 2 | yes | 2026-11-09_gate295-tier2-pr2141-2144 | 3 | - | UNSTABLE | 3 |
| 2140 | KS-2144 | GO WITH NOTES | 2 | yes | 2026-11-09_gate293-tier2-pr2137-2139-2140 | 1 | - | UNSTABLE | 1 |
| 2139 | KS-2146 | GO WITH NOTES | 2 | yes | 2026-11-09_gate293-tier2-pr2137-2139-2140 | 1 | - | UNSTABLE | 0 |
| 2138 | KS-590 | GO WITH NOTES | 1 | yes | 2026-11-09_gate294-tier1-pr2138r1-compare | 9 | 2161 | UNSTABLE | 3 |
| 2137 | KS-2089 | GO | 2 | yes | 2026-11-09_gate293-tier2-pr2137-2139-2140 | 1 | - | UNSTABLE | 1 |
| 2136 | KS-2151 | GO WITH NOTES | 2 | yes | 2026-11-09_gate291-tier2-pr2135-pr2136-docs | 3 | 2073,2135 | UNSTABLE | 3 |
| 2135 | KS-1807 | GO WITH NOTES | 2 | yes | 2026-11-09_gate291-tier2-pr2135-pr2136-docs | 3 | 2073,2136 | UNSTABLE | 0 |
| 2134 | KS-1976 | GO | 2 | yes | 2026-11-09_gate289-tier2-pr2133-pr2134 | 1 | - | UNSTABLE | 0 |
| 2133 | KS-1415 | GO WITH NOTES | 2 | yes | 2026-11-09_gate289-tier2-pr2133-pr2134 | 1 | - | UNSTABLE | 0 |
| 2132 | KS-1473 | GO WITH NOTES | 1 | yes | 2026-11-09_gate288-tier1-pr2132-pr2127r2 | 7 | - | UNSTABLE | 1 |
| 2131 | KS-625 | GO WITH NOTES | 1 | yes | 2026-11-09_gate287-tier1-pr2131-ks625 | 6 | 2073,2099 | UNSTABLE | 0 |
| 2130 | KS-624 | GO WITH NOTES | 1 | yes | 2026-11-09_gate286-tier1-pr2129-pr2130 | 4 | - | UNSTABLE | 0 |
| 2129 | KS-784 | GO WITH NOTES | 1 | yes | 2026-11-09_gate286-tier1-pr2129-pr2130 | 4 | 2080 | UNSTABLE | 0 |
| 2128 | KS-1208 | GO WITH NOTES | 1 | yes | 2026-11-09_gate290-tier1-pr2128r2-ks1208 | 4 | - | UNSTABLE | 1 |
| 2127 | KS-785 | GO WITH NOTES | 1 | yes | 2026-11-09_gate288-tier1-pr2132-pr2127r2 | 5 | 2052 | UNSTABLE | 4 |
| 2126 | KS-1718 | GO | 2 | yes | 2026-11-09_gate284-tier2-pr2124r2-2125-2126 | 1 | - | UNSTABLE | 0 |
| 2125 | KS-2109 | GO | 2 | yes | 2026-11-09_gate284-tier2-pr2124r2-2125-2126 | 3 | - | UNSTABLE | 0 |
| 2124 | KS-1794 | GO WITH NOTES | 2 | yes | 2026-11-09_gate284-tier2-pr2124r2-2125-2126 | 2 | - | UNSTABLE | 0 |
| 2123 | KS-1902 | GO WITH NOTES | 2 | yes | 2026-11-09_gate282-tier2-pr2122-2123-2124 | 2 | - | UNSTABLE | 8 |
| 2102 | KS-1864 | GO WITH NOTES | 2 | yes | 2026-11-09_gate269-tier2-pr2101-pr2102 | 5 | - | UNSTABLE | 0 |
| 2101 | KS-1783 | GO WITH NOTES | 2 | yes | 2026-11-09_gate269-tier2-pr2101-pr2102 | 3 | - | UNSTABLE | 0 |
| 2100 | KS-1868 | GO WITH NOTES | 1 | yes | 2026-11-09_gate270-tier1-pr2100-r2 | 4 | - | UNSTABLE | 0 |
| 2099 | KS-2060 | GO WITH NOTES | 2 | yes | 2026-11-09_gate267-tier2-pr2099-words | 25 | 2073,2131 | UNSTABLE | 0 |
| 2098 | KS-2022 | GO | 2 | yes | 2026-11-09_gate264-tier2-t15-batch | 4 | - | UNSTABLE | 3 |
| 2097 | KS-2077 | GO | 2 | yes | 2026-11-09_gate264-tier2-t15-batch | 1 | - | UNSTABLE | 0 |
| 2096 | KS-2016 | GO | 2 | yes | 2026-11-09_gate265-tier2-pr2095-pr2096 | 1 | - | UNSTABLE | 0 |
| 2095 | KS-2012 | GO | 2 | yes | 2026-11-09_gate265-tier2-pr2095-pr2096 | 1 | - | UNSTABLE | 2 |
| 2094 | KS-2099 | GO WITH NOTES | 2 | yes | 2026-11-09_gate264-tier2-t15-batch | 1 | - | UNSTABLE | 2 |
| 2093 | KS-2053 | GO WITH NOTES | 2 | yes | 2026-11-09_gate264-tier2-t15-batch | 1 | - | UNSTABLE | 0 |
| 2092 | KS-1209 | GO WITH NOTES | 2 | yes | gate262-tier2-pr2092-ks1209 | 7 | - | UNSTABLE | 3 |
| 2090 | KS-692 | GO | 2 | yes | gate252-tier2-batch | 2 | - | UNSTABLE | 0 |
| 2089 | KS-1493 | GO | 2 | yes | gate252-tier2-batch | 1 | - | UNSTABLE | 2 |
| 2088 | KS-1797 | GO WITH NOTES | 2 | yes | gate252-tier2-batch | 2 | - | UNSTABLE | 3 |
| 2087 | KS-1600 | GO WITH NOTES | 1 | yes | gate251-tier1-pr2087-ks1600 | 4 | 2158 | UNSTABLE | 0 |
| 2085 | KS-2074 | GO WITH NOTES | 1 | yes | gate248-tier1-pr2081-ks1171 | 6 | 2066 | UNSTABLE | 1 |
| 2081 | KS-1171 | GO WITH NOTES | 1 | yes | gate248-tier1-pr2081-ks1171 | 6 | - | UNSTABLE | 5 |
| 2080 | KS-1670 | GO WITH NOTES | 1 | yes | gate246-tier1-services | 4 | 2129 | UNSTABLE | 0 |
| 2075 | KS-2083 | GO WITH NOTES | ? | yes | gate254-compare-pr2075-r2 | 4 | - | UNSTABLE | 1 |
| 2073 | KS-1152 | GO WITH NOTES | 1 | yes | gate257-tier1-pr2073-r2 | 8 | 2099,2131,2135,2136 | UNSTABLE | 3 |
| 2067 | KS-2071 | GO WITH NOTES | 1 | yes | 2026-11-07_gate246-tier1-services | 6 | - | UNSTABLE | 0 |
| 2066 | KS-2032 | GO WITH NOTES | 1 | yes | gate245-tier1-y-auth | 14 | 2085 | UNSTABLE | 3 |
| 2064 | KS-1205 | GO WITH NOTES | 1 | yes | gate253-tier1-pr2064-r2 | 4 | - | UNSTABLE | 0 |
| 2059 | KS-1410 | GO WITH NOTES | 1 | yes | gate250-tier1-pr2059-r2 | 14 | - | UNSTABLE | 3 |
| 2052 | KS-1081 | GO WITH NOTES | 1 | yes | gate259-tier1-pr2052-r2 | 32 | 2127 | UNSTABLE | 1 |

Not a candidate: **887** (KS-961, NO GO at head 3aee3deed2e3, gate308 tier 1).

### File-overlap census (the merge-order constraints)
Open PRs that share a file (all other verdicted PRs are file-disjoint from every other open PR):
- 2099, 2073, 2131 share `Blockchain/Dev/docs/openapi/secuura-api.yaml` (all three). 2073 and 2135 and 2136 share `Blockchain/Dev/docs/S-K-OWNERSHIP-CONTRACT.md`. (2135 and 2136 share files with each other as well.)
- 2162 / 2149 share `services/api-gateway/src/__tests__/ks1448-notification-create-own-id-only.test.ts`.
- 2161 / 2138 share `services/originate/src/routes/verification.ts` and `verificationV2.ts`.
- 2158 / 2087 share `services/originate/src/routes/adminConfig.ts`.
- 2129 / 2080 share `services/m365-integration/src/index.ts`.
- 2127 / 2052 share `scripts/check-slot-credentials.sh`.
- 2085 / 2066 share `services/security/src/index.ts`.
Whether a gate's merge-tree reading already covers a pair: some do (gate342 measured 2218 vs 2099; gate286 and gate296 are multi-PR gates), the rest UNMEASURED here.

### PR 2075 (gate 254; Kam card = a)
- Open, MERGEABLE/UNSTABLE, head 32aa0d06bc0a. Verdict **GO WITH NOTES** at that exact head (gate254 compare round 2, tier 2, wording only, 2 fragment files changed since d2245bf37fe0). Four files in the PR: the KS-2083 test, `services/auth/src/routes/users.ts`, and two KS-2083 fragments. Overlaps no other open PR.
- Kam card `secuura-ks2083-session-end-race-in-flight-1107` is ruled `a` (2026-11-08 20:32): merge with honest wording and a ticket. So it is a mergeable candidate now, on measured evidence.
- Still owes: the ticket for the in-flight race (gate 245 F1) that ruling `a` requires. Whether it has been filed is UNMEASURED (Linear not read). Also the gate verdict was for the wording delta only; the product and test were gated at gate 245 (tier 1) at an earlier head, and I did not re-establish that the earlier tested bytes equal today's (gate254 Q1 says the delta is exactly two fragment files, which implies they do).

### PR 2099 (KS-2060)
- Open, MERGEABLE/UNSTABLE, head 8967de8b1755, 25 files. Verdict **GO WITH NOTES** at that exact head (gate267, tier 2, doc-only delta, round 1 of 2). Gate266 (tier 1) was the substantive gate on the earlier head.
- Kam cards, all ruled `a`: KS-2060 erased-user wallet (2026-11-06 15:29, delivered), clear-wallet null migration (2026-11-08 20:28), address-in-history DPIA (2026-11-08 20:28).
- PR 2218 is merged. gate342 (read) reports the 2218 vs 2099 merge rc 0 in both orders with the same tree 825f70fefb78, so the combined check passed at gate time. The combined check was run before 2218 merged; the post-merge state of 2099 against develop 410feda1a85e is GitHub-reported MERGEABLE only (no merge-tree run by me: UNMEASURED).
- Still owes: gate267 W1, fix two BLUF lines (the PR body's and the held ticket comment's) that still said the flat thing. The PR body's BLUF now reads "...from governance unless a legacy participant row ... holds it or a stale write puts it back", which suggests the PR-body half is fixed (read from `gh pr view`). The ticket comment half is UNMEASURED. Also shares `docs/openapi/secuura-api.yaml` with 2073 and 2131, so merge order matters (hunks UNMEASURED).

## Step 2. Gate candidates (1)

kksecura PRs with no verdict of their own at current head, newest first:

| PR | ticket | files | READY FOR GATE mail | PR body has "Notes for the gate" | note |
|---|---|---|---|---|---|
| 2079 | KS-657 | 18 | UNMEASURED (inbox digest not available) | no (proxy) | head 0fffdfba0f95. Only appearance: gate322 (tier 2, PR 2199) Q3 measured it as a compared neighbour (a floor `toBeGreaterThan(500)` to `(494)` in a test file plus a comment), not a verdict on 2079. It touches 18 files (services/shared drops its Redis cache section). Overlaps no open PR. |

Proxy note: only 37 of 81 kksecura PR bodies contain "Notes for the gate", so the proxy cannot sort READY FOR GATE state. Weak spots worth a regate review, not gate candidates by the definition: round "1 of 2" verdicts on 2087 (gate251), 2085 and 2081 (gate248), 2080 and 2067 (gate246), 2066 (gate245; also a combination compare gate258). Whether a round 2 was owed is UNMEASURED.

Also not ours: 10 dependabot PRs (575, 635, 639, 649, 945-949, 1965) and StuJam-Secuura 1129 (docs history). Not gated; out of scope.

## Step 3. Raise candidates

Instrument: `ls local-model/night/ | grep ^READY` = 434 files; target paths from `diff --git a/` headers (186 have them, 248 do not: those are UNMEASURED); open-PR file overlap against the 81 PRs' files; ticket key against open-PR titles and the last 500 merged-PR titles (`gh pr list --state merged --limit 500`, oldest mergedAt 2026-10-19T15:07Z); and, for the residual, `gh api contents/<path>?ref=develop` on each target. Control: that call returns a sha for `services/auth/src/routes/auth.ts` and 404 for a made-up path, so absence is real.
Counts: 93 READY files have a target in some open PR, 178 name a ticket in an open PR title, 214 name a ticket in a merged PR title since 2026-10-19, and 162 have no evidence of any of the three (most of those are dated before 2026-10-19 or have no header, so UNMEASURED, not "held").
`local-model/spark/` holds the harness (queue.md has no live queue lines in its tail; done.md rows to 2026-11-10 show PASS). Its raised/held passes land as READY_* in night/ (the `_spent_2026-11-12` folder holds 2 spent ones).

Held, in the window where the measurement is complete (dated 2026-10-19 or later, header present, no PR evidence, new test file ABSENT on develop 410feda):

| ticket | READY file (date) | target files | test file on develop | in an open PR |
|---|---|---|---|---|
| KS-1105 | O136-P1 CODEPATCH2 LOGIN.TSX (2026-11-11) | admin `pages/Login.tsx`, new ks1105 test | ABSENT | no |
| KS-1913 | O136-P1 PLATFORMAUDITLOG.TSX (2026-11-11) | admin `pages/platform/PlatformAuditLog.tsx`, new ks1913 test | ABSENT | no |
| KS-1912 | O137-P1 CLIENTLIST-APITS (2026-11-11) | admin `ClientList.tsx`, `services/api.ts`, new ks1912 test | ABSENT | no |
| KS-1197 | ks_1197_p1 CODEPATCH ENFORCEMENT (2026-10-28) | api-gateway `services/enforcement.ts`, new ks1197 test | ABSENT | no |
| KS-1776 | ks_1776_p1 CODEPATCH AUTH (2026-10-28) | auth `routes/auth.ts`, new ks1776 test | ABSENT | no |

Their 5 target-file sets are disjoint from each other and from every one of the 81 open PRs' files (census). Whether each diff still applies at 410feda1a85e is UNMEASURED (no `git apply --check`; the raising seat runs the builder).
Three more with a header, no PR evidence, but the test file already exists on develop (probably edits to an existing test or raised some other way): KS-1855 O125-P4 (verification.ts), KS-805 PATCHREDIRECTMIN (oauth.ts), KS-1642 H9PIN-2 (originate test). Treat as UNMEASURED, check before raising.
The rest (no diff header, or dated before 2026-10-19): UNMEASURED.

## Caveats
- 79 of 81 kksecura PRs are `UNSTABLE`; the sampled 2177 had 11 checks failing at 2-3 s and 8 skipped (`gh pr checks`). Several earlier merges this week landed from UNSTABLE (gate344 records 2184 as UNSTABLE), so UNSTABLE did not block them. Cause of the CI reds UNMEASURED, and the PR bodies carry a "do not merge until the pre-merge suites run" block (read in 2075's body), so a merge seat should check the acknowledgements the workflow parses.
- Gate verdicts are findings at a head; a merge seat re-pins head and develop at merge time.
- Mail inbox, Linear, and the 15-ish PRs whose later-round verdicts I could not order by hand are UNMEASURED.

## Step 4. Proposed lanes (file-disjoint from each other)

1. **Merge seat, tier 1 and GO first.** Candidates: the CLEAN pair 2198 and 2197 (tier 1, GWN, gate321, no overlaps), then the GO-verdict, overlap-free set (2177, 2147, 2144, 2141, 2137, 2134, 2126, 2125, 2098, 2097, 2096, 2095, 2090, 2089), then tier 1 GWN overlap-free ones. Hold the overlap pairs/triples for ordered merges (2099 with 2073 and 2131 last, because of `secuura-api.yaml`). Reason: 79 verdicted PRs sit idle, every one head-verified; this is the largest board-clearing lever.
2. **Gate seat on 2079** (KS-657, tier 2 or 1 by file count), then on whatever the raise lane opens. Reason: it is the only open PR of ours without its own verdict at head, and its 18 files are disjoint from every other open PR and every raise target.
3. **Raise seat on the five held passes, in two batches: KS-1105 + KS-1913 + KS-1912 (admin frontend), then KS-1197 + KS-1776 (gateway enforcement, auth routes/auth.ts).** Reason: PASS 7/7 held passes with no PR, absent test files on develop, disjoint from every open PR. Needs an applies-check at 410feda first (UNMEASURED).

Lane files are disjoint: lane 1 touches only files listed in the merge table (the five raise targets and 2079's 18 files are in none of those PRs), lane 2 touches 2079's files only, lane 3 touches the five raise target sets only. Lane 1 must exclude 2079 itself, which is not in the merge table.
