GO (Seat D 15th): deploy 69f2045af2a4 to kintsugi. KINTSUGI ONLY. Your ctx by Wednesday's pane read of %78 at 02:03:09Z: 37%. develop 69f2045af2a4 and pull/1398 240d4dfd5b7b by Wednesday's ls-remote 02:03:09Z.

AUTHORITY: Kam ruled card `secuura-followup-deploy-disk-archive-1007` = **a** on the live board at 13:02:37 AEDT (02:02:37Z), verbatim: "Decision secuura-followup-deploy-disk-archive-1007: a — Archive to G-Drive then remove: kintsugi's 3 oldest rollback sets, and demo's pre-20260910". Plus his October deploy grant (`learnings/2026-10-05_october-deploy-both-boxes-when-ready.md`).

THE FIELDS:
- DEPLOY_SHA: 69f2045af2a4f5f0b83b2f76c62514512abdc7b5 (ruling (a) of 00:57Z: #1398's single squash on top is pre-agreed, not a STOP; anything else is).
- KINTSUGI sets to ARCHIVE then UNTAG, exactly these three and nothing else: `pre-20260910`, `pre-2026-09-12`, `pre-20260918` (your Q-DISK15 measurement: frees 20,218 MiB, F0 → ~26,464).
- KEPT, proven intact BEFORE and AFTER (count + fingerprint): `pre-20261006` ×30 fp `940224dfab79711d`, every other older set by your 11/11 reconciliation, `latest`, and your new `pre-20261007`.
- KS-535 C2 control literal: `7d8958f1e48a608c` (both boxes).

ORDER:
1. Re-read develop (69f2045af2a4 or the pre-agreed squash; anything else STOP). Phase 0: `pre-20261007` re-tag of the 29, count derived, fingerprint recorded, every older set fp-identical.
2. ARCHIVE, per brief ITEM 0 (e) (i): for each of the three sets, `.dockerignore` excludes `*.env`/`*.env.*` at each archived image's SHA AND a `find` in one archived image reads 0 `.env*` with a planted control; then ONE `docker save <every ref of the set>` streamed over SSH to `/Volumes/G-DRIVE/Secuura/Blockchain/archive/2026-10-07_kintsugi_<set>/` (create the folders), with a MANIFEST beside it (refs, ids, bytes, sha256 of the tar). Verify each tar on G-DRIVE: size == the streamed byte count, sha256 recorded, `tar -tf` lists the expected manifest. A failed or short archive = STOP, untag nothing.
3. UNTAG by REFERENCE only, the three sets' refs (`docker rmi <repo>:<tag>`, never by id, never `-f`), guard + a planted out-of-set reference arm first (D 14th ITEM 1b discipline). After-asserts: the three sets 0; kept sets unchanged; 0 container image ids moved; dangling report; settled F0 re-read. F0 must clear 15,466 (354/image) with originate's 10,000 ADMIT; else STOP.
4. rsync → **Gate B** (mail, HOLD for the ANSWER). Then build/migration/Gate S/swap/verify/DEPLOYED/Gate W/sweep exactly as your brief.

A REFUSAL or STOP at any step costs nothing; never force, never free more than the three named sets. Demo's `pre-20260910` archive is NOT in this GO: it rides in GO-DEMO (Kam's (a) covers it; the demo GO will name it).
