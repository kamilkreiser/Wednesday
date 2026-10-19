# Gate brief: GATE O1 = five TIER-1 PRs, batched, Opus, round 1 of 2

Commissioned by the Wednesday seat, 2026-10-19 ~11:4x AEDT. Routing v1.0 row G1 (tier 1: verify honesty, an auth middleware log, an OAuth input schema, a GDPR route). Seat R 50th raised them. Its READY mail of 00:37Z is the author's claim, NOT evidence; the evidence table in it is what you measure against. develop = 78cb3c3939e319332e387ffecb075a169edd4a39 (Wednesday ls-remote ~11:4x; re-read it).
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

| PR | ticket | head (Wednesday ls-remote, equal to R's) | what (R's description) | author's suite figure |
|---|---|---|---|---|
| #1597 | KS-1634 | 8ec96bbac643dcb69ba90b2d81634f6cd40e85f1 | originate chain-first verify: `=== true` + carry `simulated`, at both sites (:712, :1191) | originate 1454/1454 |
| #1590 | KS-1628 item 3 | 68270e124aac103f0d56519b4cbee25d4ea7f544 | anchoring anchorReadback reads placeholders through the exported prefix | anchoring 379/380 (the 1 = KS-562, pre-existing) |
| #1596 | KS-1595 item 1 | 83b5758bc77959c22603c4c1db736db032a32eda | test only: GDPR erasure routes pass the principal's context | originate 1412/1412 |
| #1598 | KS-1471 | 35a5fcb93c538dd2dfe113c1228f93d7e1d43c23 | api-gateway refused connector Bearer logs `req.baseUrl + req.path` | api-gateway 1111/1111 |
| #1599 | KS-805 | 73101f01c32e90b554dfa694b511fa4075a441fe | auth PATCH oauth apps refuses `redirectUris: []`: route, spec source, regenerated yaml | auth 1068/1068 |

#1590 and #1596 were built on develop 83ed01af70fd; develop has moved 3 merges since (#1588, #1587, #1589, all in originate/api-gateway). **Re-predict each merge onto the live develop (tree id) and run the owning suites on the PREDICTED tree, not the head.**

## Gate (per PR, then across them)
1. Diff each at its head; nothing outside its named files; the five pairwise file-disjoint (check it, do not assume).
2. Red-first yourself on each: the RED cells fail on develop's code for the RIGHT reason (an assertion), the controls pass on both.
3. One mutant per product hunk, killed by a named cell.
4. **#1597 (KS-1634) questions:** (a) is `=== true` right everywhere a reply is read on the chain-first path (`confirmStalePendingAnchor` :454 already `!== true`); (b) does carrying `simulated` change ANY answer for a real anchor: measure it; (c) can anchoring's Blockfrost chain-scan branch (the step taken when the local DB misses) return a placeholder hash, and if so does `presentBlockchainHonestly`'s hash rule still catch it; (d) gate N1 found an external caller migrating to the advertised successor POST /api/verification/verify lands on this defect on a registry miss: does this PR close that route? Verdict N1: 0_Brain/reference/2026-10-19_gate-N1-pr1589-r2/verdict.md. (e) NOTE, not a finding: the head's single commit carries a non-Secuura author identity (disclosed; Kam ruled a later author-only force-push, deferred behind KS-1638). After that, the tree stays b64be7e50092 and this verdict carries over by the same-tree rule. Record the tree id you gated.
5. **#1598 / #1599:** confirm neither changes an authorisation decision. For #1599: PATCH `redirectUris: []` answers 400, an omitted field is still allowed, and the yaml diff is exactly one line (`minItems: 1`). Bite it: remove `.min(1)` from `auth.openapi.ts` and `check:openapi` must fail. Is #1599 the whole of KS-805? Name the route-vs-spec hand-written duplication as a design observation.
6. **#1590:** confirm the 1 failing anchoring cell is KS-562's (install-layout) and fails identically on develop.
7. Merge prediction: all five onto live develop in the order above, tree ids. Then check #1597 and #1590 against each other (originate vs anchoring: disjoint?).

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/o1/. Use nothing else in that scratchpad** (o2/ is the tier-2 gate running beside you; n1/, spark_*/ and drivecleanup/ belong to other work). Clone there with `git clone --shared` from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git in YOUR clone, and fetch with that checkout's `core.sshCommand` (`git config --get`) plus `-o ServerAliveInterval=30`. Build `packages/shared` before any suite.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker, no servers. No cd. Never send stderr to /dev/null. Loops go in script FILES run with /bin/bash. Every zero needs a control that fired. One heavy suite at a time (o2 runs beside you).

## Output
- Write 0_Brain/reference/2026-10-19_gate-O1-tier1-five/verdict.md.
- Lines 1-5: one verdict per PR (GO / GO WITH NOTE / NO GO), each naming its FULL head.
- Line 6: `sha256/16: <16 hex>` of the report with line 6 deleted.
- Then FOUND / TESTED / HOW per PR, the merge-prediction table, NOT tested, severities with file:line. Final lines: `MODEL:` and `WALL-CLOCK:`.
