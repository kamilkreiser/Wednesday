---
date: 2026-11-15
type: principle
source: "Kam, live board 2026-11-15 15:40:43 view=wednesday, verbatim: 'the recent merge rules override everything historic' (right after Wednesday's panel note that five PRs stay held because no brief records why)"
status: live
tier: W
---

# The recent merge rules override every historic hold: a PR that is ready merges unless a CURRENT reason says otherwise

**The lesson:** When a PR has passed its gate at its current head, the current merge rules decide: merge what is ready (Kam 2026-11-12 15:01, 2026-11-15 15:07), one head-pinned GO at a time (2026-09-11 TESTED grant, 2026-10-10 merge-and-archive grant), two merge seats in parallel (card secuura-merge-throughput-sixty-ready-1115 = a), and the self-hold sentence never blocks (card secuura-premerge-block-nine-prs-1113 = c). An OLD hold carried forward brief to brief — a "not in queue" list, a "do not merge" sentence, a hold whose reason no brief records — does NOT keep a ready PR out.

**How to apply:**
1. A carried-forward hold with no current, readable reason is lifted. Do not keep it "to be safe"; that is exactly what Kam overrode.
2. What still holds a PR is a CURRENT, specific reason: the gate's own verdict at this head says it must not merge as written (e.g. a NO GO, or a Medium that says "should not merge as written"); a Kam card ruled after the newer merge rules that names the PR; a signature-class step (deploy, production, money, comms) — merge stays allowed, the deploy waits.
3. When a hold is lifted on this rule, say so in the GO and name the PR; when one is kept, name the current reason in one line.

**First application (15:4x):** PRs 2075, 2052, 2073, 2131, 2136 released to Seat K 19th's queue; 2159 kept (gate 301 G301-2159-1: "should not merge as written") and 2225 kept (card secuura-ks1699-verify-audience-1113 ties it to an open deploy question), each with its current reason.

**Family:** [[2026-10-10_merge-and-archive-when-done-and-ready]] · [[2026-09-11_secuura-we-approve-and-merge-our-own-tested-work]] · [[2026-11-15_the-spark-is-gone-checks-retired-no-local-spark-tier]]
