# Gate queue — Secuura round 21 + lanes L1-L4 (2026-09-25)

Batched per tier (the 09-18 batch rule). A row enters on its READY mail and only after Wednesday reads the head at origin (`ls-remote`) in the same action. Gate brief shape: `fleet/qa-agent/BRIEF_TEMPLATE.md`. Carry into every gate brief: the anchoring wording (KS-562), legs 3/4/8 (the stack comes up ONCE per gate for surfaced PRs; Docker is down now), and the load false-red note (KS-1155).

| tier | PR | key | seat | head (origin, read by Wednesday) | surface → legs 3/4/8 | READY at |
|---|---|---|---|---|---|---|
| 1 | #1213 | KS-530 | B 25th | f2751859c015 (ls-remote 13:1x) | none (lockfile/overrides) | 02:10Z |
| 1 | #1214 | KS-528 | B 25th | 6fce4d0b1886 (ls-remote 13:1x) | none | 02:10Z |
| 2 | #1215 | KS-1288 | L3 | 5e3419a46db5 (ls-remote 03:0x) | none (packages/shared test) | 03:06Z |
| 1 | #1216 | KS-975 it.2 | L2 | c44b15dddadd (ls-remote 13:1x) | security module; legs 3/4/8 OWED | 03:14Z |
| 1 | #1217 | KS-976 it.1 | L2 | e83f34447402 (ls-remote 13:1x) | /reset 400 message; legs 3/4/8 OWED | 03:14Z |
| 2 | #1218 | KS-897+896 | L4 | 999623d28f7c (ls-remote 13:1x) | none (scripts test) | 03:17Z |

| 2 | #1220 | KS-1129 | L2 | 9c2021ba3e77 (ls-remote 13:3x) | anchoring response field; legs 3/4/8 OWED; anchoring wording | 03:29Z |
| 3 | #1219 | KS-1277 | L1 | 5d5129a03af0 (ls-remote 13:2x) | none (comment-only) | 03:23Z |

**TIER 1 = 4 READY at 13:1x -> gate commissioned (drafter writing the brief).** 
Pending READY, known: B 25th ×3 Ornith PRs (tier 1 batch with #1213/#1214) · L1 A/B/C/J (tier 3/2/2/2) · L2 KS-975, KS-976 (tier 1), KS-1129 (tier 2) · L3 GF-2 (stacked on #1215) · L4 PR 1 (tier 2).
Rule for launching: launch a tier's gate when ≥4 of that tier are READY, or when the oldest READY in it is 60 min old, whichever is first.
