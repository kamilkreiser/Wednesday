# Drafter notes: Seat D 79th, Kintsugi k37 (2026-11-20 14:0x-14:2x AEDT)

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-20_seatD79_kintsugi_k37.md (about 44.9 KB). Scratch and evidence: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-20_drafter-seatD79-kintsugi-k37/_work/ (own clone of Secuura develop, range.txt, prs_range.txt, reach_d79.out, reach_range.out, compose_pin.yml, trim*.py edit scripts).

## For Wednesday (discrepancies and judgement calls)
1. Range is 17 first-parent commits (d4ffc8308249..038425cafaec), not 19; the commission's 19 counts from an earlier point. Develop re-read at 14:17 = still 038425cafaec.
2. Every commit lists open PR 2267 in `gh api .../pulls` (its branch contains them); PR 2267 is not in develop.
3. Services that change by own code: api-gateway, originate, nft-certificate, timestamping (+ auth, held). Shared-only (production-guard, runtime-role-guard, index.ts) reaches every other node service: held under option (i). vc-issuer therefore returns to the held list.
4. Auth hold (gate 389 G389-2266-1, only deploy block among all gates read). Dependency measured: the gateway's served yaml carries PR 2266's 202 text (the only yaml change); gateway uses the spec for a method map only: documentation ahead of behaviour (W5 asks acceptance).
5. B207-W3: the guard only fires under NODE_ENV=production. Compose hard-codes development for 26 services; only api-gateway reads NODE_ENV from .env. Kintsugi runs CARDANO_NETWORK=preview legitimately, which the guard refuses, so a production-NODE_ENV rebuilt nft-certificate would crash-loop: brief section 5 makes the seat measure booleans first. The box's docker-compose.override.yml effect is UNMEASURED.
6. KS-2277 live check = the exact KS-772 request D 75th ran at k36 (count 1, ISS3 absent): after k37 expect count 2. That is the positive control. Licence needed for up to three anonymous POSTs (+3 audit_logs, no billing): W6.
7. KS-2280: Kintsugi role is secuura_app f/f, so the new check is silent: expected 0 `(KS-2280)` lines; the positive proof is image content + role re-read; warn/refuse branches unit-proven only.
8. KS-1936: real 403 needs an ORG_ADMIN token; UNMEASURED. Brief offers image-content proof and an unauthenticated 401 control.
9. Originate lock change (effect 3.22.5) will be the first real image build of that override (gate 388 built none): named as a stop-and-root-cause item.
10. nft-certificate rebuild carries KS-535 env: default REBUILD with before/after fingerprints (W2); Wednesday may hold it.
11. Compose diff is two comment lines: `docker compose config` sha16 should stay ab0598fd3392b393; moved = STOP.
12. migrations shares the originate Dockerfile so the census will show it changed; it is a one-shot, never swapped.

## Not done / limits
No box touched, no ssh, no send tool, nothing written under !CODING. The brief's STAMP is blank. Compiled-file strings named in section 7 are guesses at dist names; the seat reads dist first (listed in UNMEASURED). Kam's KS-2277 card text was taken from the merged code comment, card not re-read.
