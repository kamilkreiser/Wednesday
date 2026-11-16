# Drafter notes, Seat D 69th demo catch-up (2026-11-16 16:56 to 17:09 AEDT, Opus)
- Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatD69_demo_catchup.md (41,644 B, STAMP blank, SELF-CHECK 17:09 after the re-read).

## Measured
- develop eb27110fc6e4 (PR 2124), unchanged at 17:04:49 and 17:09 (gh api).
- Demo pin 07a2d62be6a0 (D 52nd, REVISION 128,642 B 6e89e4fb7e893c0f). Range to develop: 206 first-parent squashes, 0 merges, 178 KS keys, 737 files (398 A / 325 M / 14 D).
- Image map (.dockerignore-aware): REBUILD 29 of 33 (all shared-copying services, demo-service inside), UNCHANGED 4 (demo-overlay, nginx-gateway, pgbouncer, status-frontend). Build 28 (demo-service excluded), swap 27 (migrations built, not run).
- Migrations: 0 .sql in range; develop tops at 058; **058 already applied on demo by D 52nd (tracker 59 / 058)**: commission premise corrected. Boot DDL in non-test diff 0 (control 1). Nothing destructive.
- Infra: api-gateway Dockerfile (KS-1841), secuura-api.yaml changed (single-file bind orphan after rsync, re-bound by the gateway recreate), nginx-demo.conf/compose/.dockerignore unchanged.
- Kintsugi: 3 squashes past k32 (PRs 2123, 2127, 2124), scripts only, REBUILD 0 of 33: nothing owed. Anchoring: k29 (D 65th) swapped it 22:47Z = 09:47 AEDT 16 Nov, after Kam's 07:01 card (PRs 2230, 2240 in 6185f0f1ace8); 0 runtime change since: card executed (commission's "not restarted today" corrected).
- Client-visible list from 122 flow fragments: headline risks KS-1536 (platform_admin / lower-case admin tokens lose rights; demo count owed), KS-2081 (API keys refused on transfer writes; Platform S has 41 keys on demo), KS-1262 (personal notification settings reset to defaults), KS-1882 (wallet sessions need reconnect), KS-1699/KS-590 (verify), KS-528 (react-router 7 portals), KS-2196 (anchoring fee fix for Stuart's failed anchor).

## Slips
- One Bash call refused for an unquoted `======` separator (zsh hook); re-issued with `----`.
- First map run failed: python3 lacked yaml (used uv with network) and GH_CONFIG_DIR was not exported for lazy blob fetch; fixed, re-run rc 0.
- First D2 rollback-set line double-counted d12/d13 inside "17 older"; corrected before the SELF-CHECK.

## Unmeasured
Both boxes today; D8 counts (platform_admins spellings, key transfer writes, notif keys, wallet sessions, non-final anchors); demo build disk/time; d15 idfp; AA 6th anchoring revision-label conflict; Linear states; card texts (quoted from fragments / D 52nd).

Scratch: _work/ (repo.git blobless clone, fp.out, ns.out, map_d69.py + map_demo/k33/anch.out, svc_nontest.diff, flowfrags/flowtitles/visible.txt).
