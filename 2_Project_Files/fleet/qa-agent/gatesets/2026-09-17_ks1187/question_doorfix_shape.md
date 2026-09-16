matches 1
=====MSG 2026-09-16T22:49:25.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 4019
Seat A

## BLUF
KS-1187 door-fix shape proposal, per your ANSWER 22:38:58Z; nothing built. Two parts, both in `services/api-gateway/src/routes/proxy.ts` only. No open PR touches `proxy.ts` or `normalisePath.ts`: GitHub API, 20 open PRs, 22:48Z, 0 hits (control: `middleware/auth.ts` → #1017). Develop is fa887f382 (#1014).
1. The door wrapper stops corrupting absolute-form targets: `proxy.ts:739` collapses `//` across the WHOLE `req.url`, so `http://h/erasures` becomes `http:/h/erasures` and the `/erasures` door never matches. It will use the existing absolute-form-aware `collapseRepeatedSlashes` (`middleware/normalisePath.ts`, already applied app-wide at `index.ts:235` for KS-858).
2. A fail-closed canonical check in the same wrapper: the sub-path is canonicalised (per-segment percent-decode, `;params` dropped, `.`/`..` resolved, repeated `/` collapsed, compared case-insensitively). If it names `/erasures` or `/erasures/<ref>`, the door's own chain runs (authenticateToken → attachScopes → requireScopeOrRole) whatever the raw spelling. Anything it cannot canonicalise (a malformed escape, `..` above the mount) is refused 400 before forwarding.

## Recommendation
**Question:** do you approve (1) + (2), with the red cells below? Or (1) only (the measured bypass), leaving the five spellings, which originate routes nowhere (measured 404), to a ticket?
**Flag, for Kam's authority:** his 07:40 ruling on KS-1187 was *"Wait for the two severity reads, then decide"*, and this build rests on the new card's DEFAULT, not a tap. I propose to build to READY as usual, with the MERGE waiting for Kam's tap, as KS-1194's does. If you read the default as his decision, say so and I merge on your GO alone.
Meanwhile: holding. My open PRs: #1017 (gate) and #1018 (gate queued). After this fix: the N-1 (KS-1202) measurement, then KS-1204, per your order.

## Detail
- **Mechanism, READ at develop 7e89318bc** (proxy.ts unchanged by #1014):
  - Inside `router.use('/api/gdpr', …)`, express has trimmed the mount but kept the protohost, so `req.url` = `http://h/erasures`.
  - `:739` `.replace(/\/{2,}/g, '/')` → `http:/h/erasures`, and `erasureDoor.use('/erasures', …)` (`:726-732`) does not match. The catch-all `router.use('/api/gdpr', authenticateToken(true), proxy)` (`:747-750`) forwards it.
  - The gate's evidence: the upstream receives plain `POST /api/gdpr/erasures`, which originate routes to its erasure handler (my read 2).
- **Red cells** (real app, recording upstream, a connector without subjects:erase, SUBJECTS_ERASE_SCOPE_ENFORCED=true, NODE_ENV test AND production):
  - the absolute-form POST and the GET status read (plus the arbitrary-host and v1 variants) → 403, 0 upstream hits (base: 200, hit);
  - the five spellings → refused, 0 upstream hits (base: 200, hit);
  - a malformed escape under `/erasures` → 400, 0 hits.
- **Controls:**
  - origin-form without the scope → 403 (green at base and head);
  - a connector WITH subjects:erase: origin-form AND absolute-form → admitted, 1 upstream hit each (absolute-form is admitted when authorised; RFC 9112 servers must accept it);
  - a non-erasure gdpr path (e.g. consent) → unchanged.
- **Also pinned:** `req.url` is still restored to the original before forwarding, as the comment at `:713-716` requires.
- **Tier 1.** PR body: `Refs KS-1187`, no closing phrase, no mentions, NO spelling in the description; the spellings live only in the test file. Nothing to Peter or Stuart.
- **KS-1202 (N-1):** Kam's measure-first ruling is posted as comment 2e694b57-36a1-4c5b-8b6d-8be2d626c6b0 (anchors 4/4). The MERGED receipt had already gone out, so I name it here. The body does not name KS-1187.
- **Precision on my 22:47:59Z correction:** it says the ticket bodies went through quoted heredocs. KS-1202/1203/1204's bodies actually went through an unquoted heredoc with every backtick escaped. Their code spans are intact (backtick counts 12 / 13 / 11 in the files, and the anchors read back). The outcome I stated is right; the method was not.

