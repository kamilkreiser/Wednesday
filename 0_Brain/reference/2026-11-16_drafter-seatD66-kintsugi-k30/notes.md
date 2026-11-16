# Drafter notes, Seat D 66th k30 (2026-11-16)
- Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatD66_kintsugi_k30.md (about 43 KB).
- Clone: _work/repo.git (copy of the k29 drafter's blobless bare clone, fetched with the Secuura gh credential; no ssh to any box).
- Measured: develop 72aeaec533dd (= Wednesday's 11:50:45 read); 8 first-parent merges since 6185f0f1ace8; REBUILT 3 (billing, originate, api-gateway); UNCHANGED 30; NOIMAGE 3.
- Divergences from the commission's expectation: (1) PR 2128 also brings rateLimitEnforce.ts via PR 2064 (comment only); (2) originate IS in the set (PR 2247 null-permissions mint 400, PR 2100 email catches); (3) PR 2249 (KS-590, originate verification.ts) is OPEN and added to the must-not-be-in-pin list; PR 2225 touches the gateway; (4) api-gateway swap makes the yaml bind, KS-1233 read and a re-keyed gwttl tool apply (D 65th skipped them); (5) PR 2088 is auth tests only: auth UNCHANGED.
- Kintsugi's billing probe by direct call is UNMEASURED (W4).
