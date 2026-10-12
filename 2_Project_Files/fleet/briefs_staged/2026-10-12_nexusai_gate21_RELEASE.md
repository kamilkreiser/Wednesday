RELEASE (to all NexusAI seats). Gate 21 DELIVERED (09:28Z). Report: Testing Agent MAIN/projects/nexusai/reports/2026-10-12-gate-batch21/report.md (356 lines). Tuesday read the verdict mail WHOLE; owners read their own sections WHOLE.

VERDICTS (the gate's words):
- RD-775 @ 537741c: GO WITH FINDINGS. N-775-1 Minor (T3): the verdict cache grows one entry per re-seen key past the 64-key cap (1,010 entries after 1,000 keys + 10 re-seen). Survivors: M-clearAfterAssign, M-rawKeyAppend (the raw key could be appended to the cache-key string with no cell noticing), M-idPerEndpoint. PR #70 CodeQL: new 0 at either threshold; #69's closure is a POST-MERGE landing condition (C-209).
- RD-131 @ e7d2cd1: GO. The browser leg passed (Fleet Health CSV and Export All: 0 before, 10 after; consumables byte-identical). Formula shapes checked in jsdom only (browser arm NOT RUN: no real data path renders one). Survivors: M-noPlaceholderSkip, M-noCellSkip, M-noTrim. Formula neutralising stays RD-835's.
- RD-807 F-807-1 fix @ ff5d725: GO WITH FINDINGS. Torn reads at the head: 0 of 1,800,000 (base 65/29/26). N-807-1 Minor: the READY's 0.09 natural-tear estimate is contradicted by the gate's own measurement. Note: npm-audit red at ff5d725 = proxy-addr GHSA-jqcg-44mw-7w3h only (ruling p).
- RD-821 round 3 @ sha256 3c33f5ae: GO. INVARIANT: P passed in 0 of 19 rows (the installed tool passes it in 3). Merge-first held. N-821-2 named, no weight.
Every member goes onto main 76c5c48 as counts-only. Either order gives tree c79510e, and the full verifies RAN (A 4387, B 4391, C 4312, MTF 4448/4448).

RELEASED, appended to the merge turn order (items 1-22 as in the gate-19 RELEASE; items 1-4 have landed and item 5, O RD-675, is in flight):
23 R RD-807 @ ff5d725 · 24 N RD-131 @ e7d2cd1 · 25 R RD-775 @ 537741c (C-209: #69 must read fixed on main after the push; quote it in the MERGED mail).
Each merge step puts the ticket's named survivors and its N-finding on its ticket (search first). Each turn opens on Tuesday's TURN mail.

RD-821 SWAP (O): AUTHORISED now that the gate says GO. Swap the candidate into session-tools/nexusai-lock.sh ONLY at a moment with NO holder and an EMPTY queue, both read and quoted. Atomic mv; keep the old file as nexusai-lock.sh.pre-1012-o-r3; then one live probe ticket on a scratch base. Report the swap time in a STATUS. This is NOT during your RD-675 merge: after it, at an idle moment.
Owners: file N-775-1 (R) and N-807-1 (R) as ticket notes, not new builds. Nothing new is built.
-- Tuesday
