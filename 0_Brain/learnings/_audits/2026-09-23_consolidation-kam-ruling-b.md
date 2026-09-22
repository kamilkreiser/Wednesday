---
date: 2026-09-23
type: audit
source: Kam's ruling (b) on card `tuesday-boot-digest-outgrew-the-window` (2026-09-20T16:44) — "keep the whole read, shrink the corpus to fit". Continues _audits/2026-09-20_consolidation-kam-ruling-b.md.
status: live
---

# Consolidation audit — ruling (b), session 2026-09-23 (Tuesday seat, s82)

**Why this session touched it at all:** the 09-20 audit ended with four merge clusters marked
*"a proposal for Kam, not a completed action."* **Kam had already ruled (b) three days earlier.**
Holding ruled work as a proposal is how it sat untouched while the corpus grew — 193 → 200 files,
887,534 → 924,927 B source, digest 500,655 → 518,028 B. Executing it is the job, not re-proposing it.

## 1. EXECUTED — `2026-09-02_rotate-in-the-70-80-band-conditionally.md`

This is cluster 4 ("superseded-in-place rotation rules"), which the 09-20 audit called highest-risk
and said to do **by hand, with the live rule quoted in the audit**. Done that way.

**It was a correctness hazard, not just bytes.** The H1 and the whole operative paragraph stated the
**70–80** band — dead since 2026-09-05 and superseded again on 2026-09-07. The **live** rule sat in
the last section. The digest renders headline + operative paragraph first, so every seat reading it
met a band that was two rulings dead. That is the documented mechanism by which *"seats duly rotated
early"*, recorded inside that very file.

**THE LIVE RULE, quoted as this audit is required to (Kam, 2026-09-07 10:49):** *"the Wednesday
window is between 80 and 90% context. Use this as your rotation window."* Band **80–90**, ceiling
90, **70% is a CHECKPOINT ONLY**, the only unconditional respawn is the DEAD case.

**What changed:** the H1 and operative case now carry the live band. The two rules the file earned
that outlive any number are kept in the lesson (the other-panel blind spot; *a number that lives in
both a lesson and a mechanism must be fixed in the mechanism first*). The dead bands moved to
`_cases_2026-09-02_rotation-band-history.md` — the `_` prefix keeps it out of `boot_digest.py`'s
`2026-*.md` glob, the same mechanism Kam ruled for `_ledger.md`.

**The filename still says `70-80`. Deliberate: 21 files link to that stem**, and a broken handle is a
destroyed memory (`weekly-consolidation.md` step 4). The file opens with a line saying the filename's
band is dead.

**CONSERVATION, asserted by measurement, not by intention:** 30 substantive sentences of the original
checked against lesson + companion after whitespace normalisation → **0 lost**, negative control
clean. 5,908 B in → 4,591 + 7,706 = 12,297 B out. It GREW; nothing was deleted, this is a move.

**A correction to my own method, recorded because the first attempt was wrong.** My first
conservation check reported 30 of 36 lines "lost". It was a false absence from my own instrument —
lines beginning with `-` were parsed as grep options, and I had *reflowed* the prose, so exact line
matching could not succeed. The second check (sentence-level, normalised) found 13 genuinely
reworded sentences, which meant I had **regenerated live sections rather than moved them** — a
breach of the anti-collapse (ACE) guard. Remedy: the 2026-09-07 section and the original frontmatter
and Related line were appended to the companion **verbatim**, making it a true move. Only then did it
reach 0 lost.

## 2. 🔴 FINDING 5 — CLUSTER 3 MUST NOT BE MERGED. It is four distinct rules, not one rule said four times.

The 09-20 audit proposed merging *mechanism-vs-intention*: `a-promise-is-not-a-mechanism` ·
`an-enforcement-you-must-arm-is-not-one` · `a-ritual-nothing-triggers-is-not-a-ritual` ·
`a-refusal-nobody-reads-is-indistinguishable-from-working`. **I read all four before merging, and
they do not overlap:**

| file | its rule — and nothing else carries it |
|---|---|
| `a-promise-is-not-a-mechanism` | a commitment about the FUTURE needs a trigger; report a shortfall **while it can still be acted on** |
| `an-enforcement-you-must-arm-is-not-one` | a safeguard that must be armed is not a safeguard |
| `a-ritual-nothing-triggers-is-not-a-ritual` | anchor a ritual to an event that happens anyway; **untracked is worse than uncommitted** |
| `a-refusal-nobody-reads…` | ask what a guard does when its condition becomes **the normal state**; a log is not a channel; prefer DEGRADE over BLOCK |

Merging these buys ~12 KB of source and destroys four retrieval handles that fire on different
triggers. **The family relation is already carried by their `Related:`/`Family:` links, which is what
that field is for.** A future seat should not re-explore cluster 3; this table is the answer.

## 3. 🔴 FINDING 6 — THE MEASURED RATE OF (b), which is the number Kam should have

| | bytes |
|---|---|
| `_boot_digest_by_tier.md` before this session's work | **518,028** |
| after | **515,587** |
| **delta for one file of careful hand work** | **−2,441 (−0.47%)** |

**One file, done properly, buys half a percent.** Halving the digest at this rate is ~106 more such
files, against a corpus that added ~27 KB in a single busy day (09-20 audit, Finding 4). Stated
plainly and without re-arguing a ruling that is his: **the mechanical and structural work inside (b)
does not reach the target.** What reaches it is retiring whole rules — which option (b) itself
anticipated in its own words, *"it spends lessons to buy tokens"*. **That is a judgement about which
rules to stop keeping, and it is Kam's, not mine to make silently.**

**Checked and closed, so nobody re-explores it:** Unison conflict copies are NOT in the digest
(6 exist in `learnings/`; 0 render as blocks — the glob's exclusion works, per
`2026-09-10_a-sync-conflict-copy-is-an-input-to-every-glob`). There is no free duplication to remove.

**Stale-headline sweep, the correctness half of this pass:** 6 lesson files carry a
`SUPERSEDED/AMENDED/REFINED/CORRECTED` section. Only the rotation file's **headline** stated a dead
rule; the other five state general rules that their amendments sharpen rather than replace. **That
hazard class was one file, and it is fixed.**

## 4. State at the end of this session

- 199 lesson blocks; source 924,927 B; by-tier digest **515,587 B**; default digest **520,206 B**.
- Both digests regenerated (rule 3b — the `--by-tier` one is the file the boot prompt reads).
- 1 file restructured, 1 companion created, 0 lessons deleted, 0 merged.
- **Nothing retired.** Retirement is the only remaining mechanism that meets (b), and it needs Kam.
