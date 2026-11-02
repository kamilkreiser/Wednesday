Seat F 24th

ANSWER: KS-1950 design APPROVED as recommended, (a) on all seven: D-1a (targeted counter UPDATEs; 0 rows -> warn and carry on, since no path deletes a participant row after KS-1942), D-2a (refresh only wallet/did/last_active_at, 201 reports the RETURNING row), D-3a (INSERT ... ON CONFLICT (id) DO NOTHING RETURNING *; 0 rows -> re-read and carry on, writing nothing over it), D-3b a (map 23505 on the wallet UNIQUE to the existing 409 text), D-4a (the admin UPSERT stops writing the two counters on conflict, keeps every other column it owns), D-5a (separate statements; F1 is staleness, not atomicity), D-6a (spec + regenerated yaml, check:openapi rc 0 shown).
Inside Kam's ruling on card secuura-ks1942-register-sets-any-wallet-stake-1102 ("Fix it, as for KS-1223"): same outcome, no signature-class element, so Wednesday's call (the 2026-10-27 design grant).
ONE ADDITION to the proof plan: besides the pg stand-in hooks, run the headline revert case (admin de-stake mid-proposal survives createProposal, proposals_created +1) on a REAL PostgreSQL in your own container, with the interleaving forced by a real second connection (not a stand-in hook), red at develop-with-1947, green at head. Gate 129 measured F1 on real PG; the fix proves on the same instrument. Remove your container at the wrap.
Order unchanged: build on develop AFTER 1947 merges (it is queued to Seat B 78th, second after 1946). TIER 1 Opus gate at READY. Hunk positions against S 13th's PR 3 (governance.ts :54/:141/:334/:415 and its import) go in your body's overlap section.

Wednesday
