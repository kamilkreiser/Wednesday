STARTABLE: YES (after Tuesday stamps; nothing in the kit blocks a launch today)
BLUF: B1286, seat D51 (both unused: `ls | grep -i` of briefs read 0 before writing). Kit `2026-11-04_B1286_SEAT-D51_hpsmpoc-demo-deploy-header-fix.md`, 124 lines, 12 four-underscore lines (11 slots + last line). Deploys fc2bc2fc (PR #285 squash) to the hosted demo only, from 77f56644, web+API by `deploy-from-ci.sh`; no schema step, no UAT touch, no feedback write or feedback-page screenshot. The demo gets UAT's exact bytes (web 8feea5b1.., API af8a43d1.., run 41792358518, build lTe-lsvVumX0lWioBKFc4). Opus (C6 row, model-routing.md:96, :145; models_latest.json:17). Ports 9870-9879. Hard stop = Step 0 + 150 min. Slots file has only fixed rulings plus @NOW@/@SEAT@.
Drafted Wed 4 Nov 2026 19:45 to 19:54 AEDT (clocks from `date`). Read-only: no az, no HTTP to any hosted host; gh `-X GET` only.

## Facts re-measured (instrument; control)
- Origin main = fc2bc2fc (`gh api -X GET git/ref/heads/main`, 19:46); `compare fc2bc2fc...main` identical, ahead 0 behind 0; open PRs 0; commit fc2bc2fc: 1 parent = 77f56644, 13 files (`commits/<sha>`; PR merged 07:27:03Z is RELAYED by B1283 STATUS and the commission).
- CI run 41792358518: ci, push, completed/success, attempt 1, head_sha = fc2bc2fc; artifacts deploy-web/api-fc2bc2fc expired=false (expire 2026-11-11T07:47:31Z / 07:40:22Z). I did not re-read the individual jobs or CodeQL/alerts (UNMEASURED by me; the kit makes the seat read them).
- Kept packages: `.tools/b1283/repo/out/deploy-packages/fc2bc2fc.../web/web.zip` sha256 8feea5b1e54a44fa.. (16,289,971 B), `api/api.zip` af8a43d1b95d649b.. (49,591,501 B), `RUN` 41792358518 (shasum -a 256, stat -f %z; control: both digests differ from the 22c3d9ab/d1b04fad way-back pair). Way-back pair b1268 == b1273 repo copy (web) and == b1283/rollback copy (api): `cmp` rc 0.
- `tail -n 1` of B1273 STATUS begins `DEPLOYED: DEMO @ 77f56644 (WEB + API)` (line 343); B1283 line 281 begins `DEPLOYED: UAT @ fc2bc2fc (WEB + API)`; deploy-STATUS listing (grep -l, tail -6): B1048 B1234 B1258 B1268 B1273 B1283. B1279 verdict line :191 printed by grep -n: GO WITH FINDINGS round 2 of 2.
- scripts/deploy-from-ci.sh:49,50,68,69, ci.yml:166,175, infra/README.md:140,105 at fc2bc2fc printed by `awk NR==n` over the raw file (gh api raw).
- Ports: lsof 9870-9879 = 0 at 19:46 and again 19:53 (control: whole-host listeners 21). Word-boundary scan over 120 non-.pre- SEAT kits of 3-4 Nov: 987x hits 0 files; 979x hits 3 (B1273, B1279, B1282: the template's block is NOT free), 982x 1, 983x 6, 984x 2, 980x 7, 990x 14 (so scan control fires). 986x/988x also hit; 987x, 989x, 991x, 992x were clean, 987x chosen.
- Panes at 19:45: %0 tuesday, %225 NexusAI-N99, %1 fleet-monitor; at 19:53 %226 Datasec/HPSM-POC-H120 has appeared (builder, kit B1285 :103 "No production, demo, UAT or hosted site; no az": does not fire the REFUSE). No HPSM-POC-D pane. `.tools/b1286` absent.
- Model/kit file shas printed for the kit: identity_pass a3dd8d43.., rollback1283uat.sh fcb8b1f9.., rollback_download (demo) e4f271e1.., azr.sh (demo) ac31696e.., presig1273b971 9f211d1d.., repoint1273.sed 9b8e840f.., repoint1283.sed 518349e2.., UAT after ring.json d276978c.., demo old-build ring.json c2998bef...
- Expected values in the kit are B1283's printed numbers (shell table :168-:181, page-height :191-:200, package checks :56-:65, words) and B1273's demo-specific ones (settings API 36/web 18, deployments 8bd6971e../ae00e194.., images _20261027.8, 156 visits, warm-up 25.3 s, deploy leg 8 min 38 s).

## D-decisions (all in the kit; defaults apply if Tuesday is silent)
- D-1 pin TARGET. Main-moved check: ONE parent each, no merged PR touching web/api/infra/scripts/.github/global.json, only README.md/records-type text; else STOP. (HPSM-POC main has no records tree: records are a separate repo, so any product path means STOP.) Control `compare PREV...main` must read ahead 1.
- D-2/D-3/D-4 as B1283 (two `az webapp deploy` lines only; API stamp-only; firewall list unchanged).
- D-5 database: the demo AUTO-PAUSES (autoPauseDelay 60, B1273) and was last read at 15:06; expect it PAUSED at Step 0. Default: wake by ONE `GET /health/ready` (curl -m 120) as B1273 slot 9(c) allowed; end state Online, all settings equal; pause/write rows listed with caller. This is a slight widening of "database untouched" (see Q-1).
- D-8 words by program (fbwords copy, expected exactly the two names); D-12 page height: demo BEFORE vs AFTER and demo AFTER vs UAT's AFTER FILE (never UAT hosts); D-13 shell probe with the demo's BEFORE as plant control; D-14 Demo-level alias count.
- Kit lineages (to avoid B1273's six name collisions): A = `.tools/b1283/` final files (they already hold TARGET/PREV/digests/runs/builds, so the sed only does UAT->demo names, stems 1283->1286, ports 982x->987x, hard stop); B = demo-pointed finals taken from `.tools/b1273/` by name (azr guard, rollback_download demo case, presig demo, measure* without the reset POST, demo minter, demoalias, hostedboot, demo-shaped pair).
- Slots: 11 (STAMP, LAUNCH AUTHORITY, HARD STOP, TARGET AND LANDING, UAT STATE, five RULINGs of which the new one is RULING 6 feedback `NO FEEDBACK WRITE OF ANY KIND; NO FEEDBACK-PAGE SCREENSHOT`). Slots-json holds only slots 1, 3, 6, 7, 10, 11 and READ-WHOLE; slots 2, 4, 5, 8, 9 are Tuesday's to write (they attest Tuesday's own reads).

## Q-questions for Tuesday (each with a default)
- Q-1 Wake of a paused demo database by one health read: default YES (B1273 precedent, covered by slot 9(c) if you confirm it). If you want "no wake at all", the seat must STOP when the database is paused; say so at the stamp.
- Q-2 Local pair: default = demo-shaped TARGET and PREV pairs on 9870-9879 (B1273's demo-shaped pair merged with B1283's shellprobe/ring edits); fallback written in the kit (B1283's UAT-shaped pair re-run plus a demo-shaped API boot). Accept the fallback up front?
- Q-3 Ports 9870-9879 (mine; you assigned none). Change at stamp if you prefer another block.
- Q-4 Hard stop: Step 0 + 150 min (B1283 took 75 min with a 17-minute CI wait; the demo adds a slower B1 deploy of ~9 min and a possible wake). Default 150.
- Q-5 Slot 4/5 are Tuesday confirmations (origin main, merge, CI, B1279; UAT last line and its public BUILD_ID x1 which you measured at 19:4x): please write them as your own reads only.

## UNMEASURED
- Everything hosted: the demo's current state (database paused or not, settings, deployments 8bd6971e/ae00e194, images, activity log since 03:41:49Z). No az/HTTP by rule.
- Whether the demo banner or plan B1 moves any D-13 property (header 72 px, logo 24 px, footer 252/88): UNMEASURED; the kit makes a difference a STOP unless the seat names the element and its own number.
- Whether B1273's demo-shaped local pair and B1283's edited pair merge cleanly (Q-2).
- CI job-level results, CodeQL and open alerts for fc2bc2fc (not re-read by me; the commission and B1283 relay them).
- The time the merge happened (07:27:03Z) is relayed, not mine.
- I did not run `git ls-remote` (needs the deploy key); main was read through `gh api`.

## Outside the fences
None. I read B1273/B1283 STATUS and kits, B1285/B1282 kits (grep for the no-hosted line only), `.tools/b1268/b1273/b1283` files (ls, shasum, stat, cmp, grep, sed -n), `fleet/specs/model-routing.md`, `models_latest.json`. No decision_queue, no briefs_staged, no scoreboard, no ledger, no WEDNESDAY/FRIDAY tree, no Jira, no HTTP to any hosted host. I wrote three files only, all in `tuesday/briefs/`: the kit, this report, the slots file. One slip: my first Bash call typed a `cd`; the hook refused it, nothing ran. One hook advisory (case-sensitive grep) seen; counts that mattered carry controls above.
