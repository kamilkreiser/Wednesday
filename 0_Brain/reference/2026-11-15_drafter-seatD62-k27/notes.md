# Drafter notes: Seat D 62nd, Kintsugi k27 (2026-11-15, Sonnet drafter, read-only)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatD62_kintsugi_k27.md (46.6 KB). Scratch in `_work/` (12 MB blobless bare clone `repo.git`, lists, compose, Dockerfiles).

## What I measured (pin read: develop 48883ba5976b, ls-remote 15:3x AEDT)
- a6b62841d699..48883ba5976b = 35 non-merge commits, 95 files, 56 outside tests/docs. No migration, Dockerfile, compose, nginx, openapi path.
- Per-service count table (nontest files vs k26 base: own / shared; "new since k26" = vs a6b62841d699). Shared since k26 is only packages/shared audit-logger.ts + tsconfig.json (0 callers outside shared).
  - REBUILD 8: auth (6 own), api-gateway (2: verification.ts behaviour, index.ts comment), originate (1), governance (1), kyc (1), tokenisation (1), vc-issuer (2), mcp-server (1 lock: hono bump).
  - UNCHANGED 25 incl. EXCLUDED anchoring (card 1107, PR 2081 open) and demo-service. NOIMAGE 3. Predicted 8 / 25 / 3 = 36.
- Wallet var only on anchoring + nft-certificate (compose 1311, 1694): no swap carries it.
- Single-file binds: api-gateway yaml, nginx-gateway conf; neither changed.
- Disk: 8 images x 1,397 to 1,848 MB = 11.2 to 14.8 GB; from 74.4 GB free -> 59.6 to 63.2 GB after; floor 45 GB; pre-build STOP under 60,000 MB.

## Findings that contradict the commission or the board brief (Wednesday must see)
1. Prune card 1007 is ruled **b = one-off**, not the "standing rule" the commission names (option a was the standing rule). Brief says prune NOT authorised, forecast does not need one.
2. 058 is NOT pending on Kintsugi: Seat D 53rd applied it 2026-11-05 (history.md line 4302, count 0 of 14). Card 1104's duty is discharged; tracker 59 / max 058. The migration gate is therefore a standing gate (any file not in the tracker), not a 058 gate.
3. S 79th board brief RULING 2 says the October grant ended 31 Oct and k27 needs Kam's tap; EXPIRING-GRANTS.md line 37 shows the 2026-10-19 extension "until further notice". Commission is right.
4. Card 1113 (verify = c): "guard reverted before 2225 deploys". PR 2228 CLOSED, PR 2225 (KS-1855 half two, api-gateway verification.ts) OPEN: if the pin carries 2225, Wednesday confirms.
5. PR 2099 (KS-2060, migration 059 + openapi yaml + governance/auth) is OPEN: if it lands the round changes (059 before governance, Wednesday's word to apply, yaml inode rule). PR 2195 edits scripts/run-migrations.sh (originate and migrations deltas). Admin-frontend PRs 2220-2222 and staking PR 2067 would add REBUILD rows.
6. D 61st never names a kyc container; KS-2166 and KS-1931 cannot close on this round if kyc does not run on Kintsugi.
7. Card 1112 (notice = b) covered k26 only; no standing notice ruling for k27.

## Calls the brief makes (flag if you disagree)
- vc-issuer REBUILD (own runtime source differs; also meets KS-1973 "only caller"); m365-integration and prism stay UNCHANGED.
- No sweep of Linear: A2 states are the S 79th drafter's 15:19 read, relayed.

## UNMEASURED (final)
- The box (Kintsugi) entirely: images, priors, REVISION, tracker, free disk, whether kyc runs, whether D 61st's `_d61` tools still run.
- Linear state of every ticket (A2 states relayed from the board brief; KS-1868, KS-2173, KS-1959, KS-2194, KS-2195, KS-1923, KS-2177 not read).
- Gate verdicts for the 35 commits (not re-read).
- The pin at the GO and which of the 86 open PRs the two merge seats land before it.
- Compiled forms and exact counts of every census literal (source forms only).
- Real image sizes and build cost; whether packages/shared tsconfig change builds in each image.
- Registry/local digests of node:24-alpine and nginx:1.30-alpine.
- The text of the KS-2166 / KS-1931 board comments (gate 85's two extra points).
