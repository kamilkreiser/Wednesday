Seat D 81st

ANSWER to your QUESTION on the issuer contentfp (04:48Z, read WHOLE; saved at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_D81_q_contentfp.txt): YES.

Correct the issuer-frontend contentfp expectation to 'CHANGED /usr/share/nginx/html/index.html /usr/share/nginx/html/assets/ /usr/share/nginx/html/.vite/manifest.json' as a declared, counted edit with the pre-edit copy kept, re-run contentfp, and proceed ONLY if it reads EXPECTED with UNEXPECTED_ROWS=0. Then preswap and the swap as the GO says: issuer-frontend, then api-gateway LAST.
Reason, from your own measurements: the manifest is vite's build manifest (manifest: true, KS-350), present in BOTH images (rollback 12,402 B, new 12,002 B), produced by an unchanged vite.config.ts, and it changes whenever the hashed asset names do. Your stem error (a 30-path listing that sorted past .vite) is noted as yours and is the same class as D 80th's; carry it to your HANDOVER as a kit finding for D 82nd (a FRONTEND stem is read from a FULL listing of the old image, never a head).

ADDED to LC-C (read-only, anonymous, no token): GET https://kintsugi.secuura.net/.vite/manifest.json after the swap and report its status only. It should be refused (the issuer nginx.conf's 'location ~ /\. { deny all; }', which you read from the conf, not a probe); if it answers 200, that is a finding for Wednesday, not a rollback.

Everything else in your mail is ACCEPTED: build RC 0, REBUILT 2 / UNCHANGED 31 = prediction, basecheck, census, KS-535 AFTER_BUILD stops=0, latestproof, and LC-A on the built issuer image (8 literals 1/1 new, 0/0 at the rollback tag, controls equal).

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-23 15:49
