# Drafter notes, Seat D 65th k29 (2026-11-16)
- Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatD65_kintsugi_k29.md (about 42 KB).
- Drafter clone: _work/repo.git (copy of the k28 drafter's blobless bare clone, fetched over https with the Secuura gh credential helper; remote URL and helper set in that copy's own config only). No ssh to any box.
- Measured: develop 9942bae93563 (unchanged 07:05); 18 first-parent merges since 61a3953e6d66; 7 services change (anchoring, transfer, analytics, wallet-connector, kyc, billing, originate); no migration, no Dockerfile/compose/nginx path; api-gateway/auth/vc-issuer/admin-frontend 0 change.
- Divergences from the commission: (1) card ks1703-ac4 is WITHDRAWN at 07:04:27 (Kam's 07:03:38 audit/verification public-read rule), not OPEN; (2) PR 2081 and 2239 are merged and in range; (3) api-gateway is not swapped so KS-1233/KS-1407 reads do not apply; (4) the "AC6 export marker" was not located in source.
