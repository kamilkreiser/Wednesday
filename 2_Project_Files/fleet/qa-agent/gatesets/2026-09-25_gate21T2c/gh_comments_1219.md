--- comment 5826138536 by linear[bot] at 2026-09-25T03:22:27Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1277/documentsts-two-stale-comments-about-on-behalf-of-recording-2327-2334">KS-1277 documents.ts: two stale comments about on-behalf-of recording (:2327-2334 inside /revoke, and the KS-480 §6 docblock :60-66)</a></summary>
<p>

**BLUF:** two comments in `Blockchain/Dev/services/originate/src/routes/documents.ts` (read at develop `3c447abc7`) describe how on-behalf-of recording used to work. Code is unaffected.

1. `:2327-2334`**, inside** `/revoke`**.**
   * It says "handleOnBehalfOf writes an action_provenance row …". That function was deleted by #1060 (KS-1264).
   * It says "Writing it here means a row exists only for a call that was going to succeed". That now sits above the CHECK, while the row is recorded after `updateDocument` (\~:2342).
   * Risk: a reader who trusts it could move the record back up. #1060's 🔴 cell would catch that.
2. `:60-66`**, the KS-480 §6 docblock.**
   * It says the hook "appends the provenance row fire-and-forget". `checkOnBehalfOf` appends nothing since KS-1228; `recordOnBehalfOf` does, after the action.
   * It lists `lifecycle-events`, which has been on the connector pattern since KS-566. `checkOnBehalfOf` is called only from /version, /share, /transfer-custody and /revoke.
   * It omits `/revoke`.

Harmless, so not in scope: `:121` (past tense, still accurate), `:2341`, and the ks1228 / ks1264 test narration.

## Fix shape

One comment-only change covering both sites. No behaviour change. It was not done inside #1060 because that head is the verbatim local-model patch.

## Provenance

Batch gate `2026-09-19-batch1050-1060-tier1-r1` (report: `Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1050-1060-tier1-r1/report.md`), finding **N60-1** (G1, Polish). Raised by Seat B 2nd in the READY and confirmed by the gate, which added site 2. Wednesday's GO 2026-09-18 23:14:38Z. Refs KS-1264, KS-1228.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1277-correct-two-stale-on-behalf-of-comments-in-the-originate-e3e508a4fd45">Review in Linear</a></p>

