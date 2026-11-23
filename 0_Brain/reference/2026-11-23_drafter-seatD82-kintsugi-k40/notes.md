# Drafter notes: Seat D 82nd, Kintsugi k40 (written 2026-11-23 16:27 AEDT)

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_seatD82_kintsugi_k40.md (44,972 bytes). Scratch: `_work/` (own clone, reach_d82.py, reach_d82_b8470.out, auth_base.ts).

## Findings for Wednesday (none is a STOP for the drafter)
1. **REVISION naming collision (new trap).** Box REVISION head is already `revision=b8470f5fd331` (k39). If the GO pin is b8470f5fd331 again, D 81st's `revwrite_d81.sh` (lines 48-49) names the preserved file `REVISION.pre-b8470f5fd331`, which already exists (the k38 file), and REFUSES after the swap. Brief makes the seat fix it before the GO (counted edit to `REVISION.pre-<SHORT>-k40`, dry-proved, W4).
2. **Invited users become unverified.** At the held auth (base d4ffc8308249 auth.ts 259, 299) an invited stub claimed by registering is written `emailVerified:false`. So the 9 invited users will be unverified when they claim, and with no mail transport cannot verify: documents addressed to them are hidden. Kam's card b text names only "unverified users"; brief section 8 states this for the panel receipt.
3. **PR 2286 (KS-2314) also changes originate** (`routes/adminConfig.ts`), gateway and admin-frontend. Open at 16:20, gate 410 GWN at 1d906e3c0a57, W 69th fix round running. If it merges before the GO, the GO must name b8470f5fd331 so it is excluded; the brief makes any originate delta other than the four files a STOP.
4. **Prune mechanics.** Precedent is D 65th's `prune_d65.sh plain` (`docker builder prune -f`, image/tag/volume fingerprints, once-only marker; reclaimed 92.5 GB in ~25 min). Brief removes its `all` arm, places the prune after Phase 0 and pre-build checks, immediately before the build; second prune or `--all` = STOP + new card. Expected ~48 GB freed (UNMEASURED). Not needed for the 60,000 gate (65,506 free) but ruled.
5. **Card timestamps** differ by seconds between the commission (board 16:18:18 / 16:18:02) and `decision_queue.sh show` (ruled_ts 16:18:54 / 16:18:14). Both quoted; same rulings (b and a). Both cards read `status: ruled`.
6. develop unmoved: b8470f5fd331 at 16:22 (`git ls-remote`). Originate's own code since 8389ed294629 = exactly 4 non-test files (PR 2274 systemErrors.ts; PR 2284 documents.ts, certifications.ts, new callerEmailVerified.ts); 0 `.sql`, no Dockerfile/package/compose change; packages/shared 0 changes. Predicted verify_build REBUILT 1 / UNCHANGED 32 / NOIMAGE 3.
7. Added a read-only ITEM 0 question (Q8): originate's DB role booleans (rolsuper, rolbypassrls, SELECT on users), since KS-2275's read fails closed to a 500 if the role cannot read `users`; gate 408 only proved it on a throwaway cluster.
8. No live render this round (finding e: it writes 2 audit rows); no LC-C.

## Not measured by the drafter
No box touched; all Kintsugi facts carried from D 81st's record. No test suite run. No ssh. Brief ordinal: `Seat D 82` = 0, `Seat D 81` = 1.

## Faults declared
- One Bash call used `====` as an echo separator and was refused by the zsh hook (nothing ran); re-issued without it.
- Two grep-then-`cut -c` views (advisory fired); no absence was claimed from them.
- First draft was 49 KB; trimmed to 44,972 B by removing prose, no rule removed.
