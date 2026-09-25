--- comment 5826000701 by linear[bot] at 2026-09-25T03:05:39Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1288/ks781-leg-d-pins-api-gateway-indexts-by-line-number-moved-six-times">KS-1288 ks781 LEG D pins api-gateway index.ts by LINE NUMBER - moved six times; pin by TEXT instead</a></summary>
<p>

## BLUF

LEG D of the ks781 body-parser-order suite pins three `api-gateway/src/index.ts` sites **by line number**. Any edit above those sites moves the pins and reds the suite for a reason that has nothing to do with what it guards. **It has moved six times.**

## The most recent move, and why it is expensive

#1210 (KS-1239) removed 18 lines from `index.ts`, shifting all three pins by a uniform -18: 845 -> 827, 858 -> 840, 891 -> 873. The red surfaced in `packages/shared` while the **api-gateway** lane was green - a cross-package failure the author's own lane run could not see. The tier-1 gate NO GO'd the PR on it (Major, `LEGD-LINEPIN`).

Fixing it took re-keying the three `toEqual` line numbers, the CONTROL's `toContain`, and two adjacent comments that named the old numbers as live - all of which is work that a text pin would not have needed.

## Ask

Pin by **text** (the line's content, or a stable anchor) rather than by ordinal position, so an unrelated edit above the sites cannot red the suite.

**Where:** `Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts`, LEG D.

## Named, not related

**KS-1126** - "KS-953 instance 4: ks781 LEG D's hand-pinned api-gateway index.ts lines :854/:867/:900 drift" - is **Done and ARCHIVED**. It closed *one instance* of the drift, not the class. Archived issues refuse relations, so it is named here rather than linked.

## Searched before filing

`searchIssues`, `includeArchived: true`, every page literal-matched: **"LEG D pins by line number"** (40 hits), **"ks781 LEG D"** (40 hits). Nearest are KS-1126 (archived, an instance) and KS-1142 (Backlog - the entrypoint corpus pinned by two hand-maintained literals, a different class). **No open home; filed new.**

---

*Carried from Seat B 22nd (2026-09-23) as LEGD-BYTEXT. Filed by Seat B 24th, 2026-09-25, on Wednesday's ruling.*
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1288-legdbytext-leg-d-pins-its-three-api-gateway-sites-by-text-not-9af80ec17a7f">Review in Linear</a></p>

