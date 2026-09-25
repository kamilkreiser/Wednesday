--- comment 5826570425 by linear[bot] at 2026-09-25T04:12:45Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1291/documentsts844-the-post-save-issuername-guard-is-unreachable-dead-code">KS-1291 documents.ts:844: the post-save issuerName '@' guard is unreachable dead code since #1174 moved the check above saveDocument</a></summary>
<p>

## BLUF

**#1174 (KS-1265) added an** `@`**-guard on** `issuerName` **at** `services/originate/src/routes/documents.ts:611`**, before** `saveDocument` **at** `:695`**. The older guard it superseded is still at** `:844` **and can no longer be reached for that case.** #1174's own merge message says so, verbatim:

> *"The older post-save guard is now unreachable for that case and can be removed in a later cleanup."*

That cleanup was never filed. This ticket is it.

## Measured at develop `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (read-only)

* `:611-618` — `const topLevelIssuerName = typeof req.body?.issuerName === 'string' ? req.body.issuerName.trim() : '';` then `if (topLevelIssuerName.includes('@')) { return res.status(400)... }`, **before** the save.
* `:695` — `const saved = await saveDocument(document, tenantId, (req as any).db, {`.
* `:838-844` — `const suppliedIssuerName = ...` then `if (suppliedIssuerName.includes('@')) {` — **after** the save, so for a top-level `issuerName` carrying `@` the request has already returned at `:611`.
* Commit: `fd6335f08` *"KS-1265 EARLYGUARD: refuse an email-shaped issuerName before the document is saved (#1174)"*, +8/-0 in `documents.ts`.

## Why it matters

A dead guard is a claim. A reader auditing the create path finds two `@` refusals at different points and cannot tell from the file which one bites — and the `:844` copy reads as though a document can still be saved before an `@` is refused, which is exactly the behaviour #1174 removed. Same class as KS-1277: a correct rule beside a stale copy of itself is worse than the stale copy alone.

## Fix shape, and the proof the work must carry

Remove the `:838-851` post-save `@` branch (keeping the `issuerName` default assignment that follows it), and **prove the removal is safe before making it**:

1. A cell showing an `@`-carrying top-level `issuerName` is refused 400 at `:611` with `saveDocument` never called.
2. **Paired mutation:** delete the `:611` guard and that cell must fail. A guard whose removal reds nothing is not a guard, and a removal justified by an unproven check is not justified.

If the mutation shows `:844` is in fact still reachable by some other shape (a non-top-level `issuerName`), the guard stays and this ticket closes with that measurement recorded instead.

## SEARCHED BEFORE FILING

Literal census over **1,280** KS issues (823 archived; titles + descriptions) and **3,594** comments: `suppliedIssuerName.includes` → **1** hit (KS-1265, the ticket that created the situation); `suppliedIssuerName` → **1** hit (same); `#1174` → 2 hits (KS-772, KS-485 — both review-stream roll-ups, neither owns the cleanup). Controls: `KS-1265` → 4 hits, so the instrument matches; `zzqq-no-such-token-zzqq` → 0, so it discriminates. **Unfiled.**

## PROVENANCE

Found by Seat L1 on 2026-09-25 during the ITEM 0 residual measurement of KS-1265, from #1174's own merge message. Filed on Wednesday's ANSWER of 2026-09-25 02:20:37Z (Q6: *"Search first ... If unfiled, file one ticket assigned to the board account"*).

Refs KS-1265.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1291-remove-the-post-save-issuername-guard-that-is-unreachable-40041fd3b107">Review in Linear</a></p>

