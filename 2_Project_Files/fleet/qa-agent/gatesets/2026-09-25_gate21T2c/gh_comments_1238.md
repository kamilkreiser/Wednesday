--- comment 5827612765 by linear[bot] at 2026-09-25T06:00:17Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1158/l3a-gate-records-912-r2-937-the-placeholder-hash-anchoredat-carry-keys">KS-1158 L3a gate records (#912 r2 / #937): the placeholder-hash anchoredAt carry keys on string truthiness not authoritativeTxHash(), the network carry has one pin, stale line references in the ks1059 / ks1058 test headers</a></summary>
<p>

## BLUF

The three Records with NO existing home from the L3a tier-1 round-2 gate (PR #912 r2, KS-1004, head `609c44c55` — GO WITH FINDINGS, zero findings against the diff; PR #937, KS-1059, head `6fd3a8bec` — GO), filed as ONE ticket on Wednesday's ADDENDUM 05:10:18Z so each is searchable by symbol/path and none is rediscovered as new. **None is a finding against either PR.** #912 r2 landed as M35 `be83eacd7`, #937 as M36 `7d1fccfcc`.

Report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-14-ks1004-912-609c44c55-tier1-r2-ks1059-937-6fd3a8bec-stacked/report.md` (175 lines, 14:51 AEST; §RECORDS items 1, 3, 5; Section S "#937 Records").

**Search before filing (every KS issue incl. archived, 1,147 issues, title + description + comments, literal;** `5_Project_History/2026-09-14_s225/item8/symbol_search.log` **— the search the merge seat ran before closing KS-1004 stands as this ticket's search):** `prior?.txHash && prior?.anchoredAt` → KS-1004 only (its own gate comment); `authoritativeTxHash` → KS-587 (archived) and KS-589 (archived) only; `prior.network` → 0; `anchorStateSync.ts:325` → 0; `documentRepo.ts:480` → KS-1058 (archived), KS-1068 (In Review — the blob writers' `as any`, not the header), KS-1074 (Backlog — the poller writers, not the header); `stale line` → KS-570 / KS-722 comments (unrelated). Controls: a known title hits 1, a nonsense term 0. **The other two Records of the same gate have homes and are NOT this ticket:** R2 (`documentRepo.ts:61-62` comment incomplete for the hashed `anchor_failed` population) → routed to PR #939 / L2 by the gate; R4 (`persistedStatus == null` fail-open carve-out) → its existing home KS-1073 (Backlog), one facts comment posted there.

## The records, each with its symbol/path (the gate's text, verbatim where quoted)

### R1 — placeholder-hash `anchoredAt` carry (READ)

`services/originate/src/services/anchorStateSync.ts:170` keys on the hash STRING's truthiness (`prior?.txHash && prior?.anchoredAt`), not on `authoritativeTxHash()` (`:77-82` rejects `tx_` / `mock_tx_`); a `tx_sim_…` prior would keep its time. Not in any fixture; KS-1069 refuses such hashes on the verify side (E1/E2/E11 green). Symbol `prior?.txHash && prior?.anchoredAt`. Archived ancestors by symbol: KS-587 (the `mock_tx_` honesty corpus), KS-589 — named, no relation.

### R3 — the `network` carry has ONE pin (MEASURED, Tg-E)

`anchorStateSync.ts` — `...(prior?.network ? { network: prior.network } : {})` is pinned by the ks1004 K2 cell (`:116`) only; the gate's Tg-E tamper reddened exactly that one cell (1/32/33). One pin holds; a second, independent cell would make the carry survive a rewrite of K2. Symbol `...(prior?.network ? { network: prior.network } : {})`.

### R5 — stale line references in two test headers (READ; Polish)

`services/originate/src/__tests__/ks1059-sim-leg-must-not-resurrect-a-terminal-document.test.ts:6` "`anchorStateSync.ts:325 on develop`", `:10` `d4cf7e3cf`, `:28/:29/:32/:35` `:283/:285/:296/:325` (the guard sits at `:378` at head); and `ks1058-anchor-failed-preserves-thread-token.test.ts` header cites `documentRepo.ts:480` for the shallow spread, which sits at `:510-514` at head (`{...doc, ...updates}` multi-line). Logic is line-free; Record only.

## Definition of done

One test pass (Kam's 2026-09-07 rule): R1 decided (key the carry on `authoritativeTxHash()` or record why string-truthiness is the intended semantics, with a cell either way), R3 a second pin for the `network` carry, R5 the two headers re-pointed at the current lines. R2 closes with #939; R4 with KS-1073.

**Related:** KS-1059 (#937, M36 — the ks1059 header is R5's file). **Named, no relation (archived):** KS-1004 (#912 r2, M35 — R1/R3's file), KS-587, KS-589, KS-1058.

Filed by the merge seat s225 on 2026-09-14 after #937's squash (M36), before KS-1059's archive, so KS-1059's closing comment can name it.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1158-r5a-re-point-the-ks1059-header-citations-and-fix-the-two-code-4e8e83d6b571">Review in Linear</a></p>

