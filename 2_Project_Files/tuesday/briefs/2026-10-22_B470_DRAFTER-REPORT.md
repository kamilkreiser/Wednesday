# B470 drafter report (read-only; two files written)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B470_SEAT-D27_hpsmpoc-uat-redeploy-login-partner-first.md` (71 lines). Cloned in shape and steps from B443's brief; B443 STATUS used for what really happened.

## Slots for Tuesday (3, four underscores each, in the Stamp)
Stamp time, launch authority, hard stop. Count 3 (`/usr/bin/grep -o -E '_{4}'`; control `a_____b` reads 1). The seat refuses if any remain. No READ-WHOLE-BY-TUESDAY line, as asked. B443's `@X@` slot check is replaced by the underscore check.

## Read whole
B443 brief, B443 drafter report, B443 STATUS (203 lines). Grepped B459 STATUS and B463 gate STATUS for colours, rects, verdict, finding. Quoted routing row C6 from `fleet/specs/model-routing.md`.

## MEASURED by me (read-only, ~17:46 AEDT)
- `gh api` main ref = `4695d7f2d50047770f2e8835172d14022d9e9622`; one parent `a93b926a`; tree `1776ac4c6d36cafde57eb2a96977c5ce920c9b52`; `26460869` tree = the same (EQUAL).
- Live sha being replaced: `a93b926ac8534bd0c9ae67fe63229ede46c39fd4` (B443 deployed it 00:03:07Z-00:05:14Z, live web BUILD_ID `KYp8vMyhkPvdtqsRLviqt`). No later UAT deploy STATUS exists in `Briefs/` (only B443 and earlier hit "DEPLOYED: UAT"; B459 and B463 are build and gate).
- Delta `a93b926a...4695d7f2` (`gh api compare`): ahead 1, behind 0, 1 commit, 2 files: `web/src/components/screens/UatStartScreen.tsx` (+29 -9) and `UatStartScreen.layout.test.tsx` (added, +193).
- CI at `4695d7f2`: `ci` push run `39735946599` and "Push on main" `39735945335` both in_progress at my read. The seat must wait up to 30 min and refuses a non-green run.
- B443's `a93b926a` rollback packages exist in `.tools/wt-b443/out/deploy-packages/a93b926a.../` and sha256 equal B443's STATUS (web `6766d085...`, api `dffa18a1...`). B443's kit files exist in `.tools/b443/`.
- load1 read 5.52 / 8.77 / 9.34 (fresh `uptime`), so the sweep may wait.

## Judgement calls to check
1. Rollback target is `a93b926a` (what B443 left live), primary copy from `.tools/wt-b443/`, plus independent `fetch`; `01dd9e4b` is the named second-level fallback.
2. Port block 8130-8139 (D26 used 8120-8129 and is done). B440 fence kept conditional ("if still live"); I do not know its state.
3. The start-page proof is a BEFORE read on the old page that the new-look asserts must FAIL against (so the instrument can fail), then an AFTER read of DOM order, one `role=separator`, computed colours `rgb(95, 107, 122)`, border `rgb(107, 118, 134)`, opacity 1, not disabled, Tab order, click-through per level, word `cmp` against the BEFORE text. Pixel rects are recorded, not asserted. Colours and rects come from B459/B463 STATUS (RELAYED), not re-measured by me.
4. The faint divider (1.39:1) is stated as B463's disclosed note: invisible at 390 is not a failure.
5. Badge and header sweep kept as a regression check (AppShell untouched); it is the heavy part, load-gated. Dropped the badge-390 screenshots and 700 Consultant shot; screenshots required are `login-390.png` and `login-1280.png` plus a BEFORE pair.
6. Failure severity copied from B443: a new two-row or start-page assert failing on a healthy site = STOP, no auto rollback; unhealthy site = rollback.
7. Hard stop left blank: the merge was 17:45 AEDT, later than B443's 12:30, so I did not invent one.

## Final-line markers the brief uses
- `DEPLOYED: UAT @ 4695d7f · start page Partner first + 1 divider + 3 of 3 dimmed rgb(95, 107, 122) · words unchanged · screenshots 390+1280 · badge 4 of 4 exact · one row 390+700+767+768+1280+1440 · residual rows 17 of 17 as B441 (new 0) · refusals 7 of 7 · Auth__UatOpen__Enabled true before+after · rollback package a93b926 kept` (B443's format, extended with the start-page and UAT-open facts)
- `ROLLED BACK: <reason>; ...`
- `STOPPED: NEEDS TUESDAY <one question>`

## UNMEASURED
CI result at `4695d7f2`; whether B440 is still live; the API package content diff vs `a93b926a`; the live site's current state; whether a Tuesday-side deploy happened after B443 outside `Briefs/`.

## Fenced
No `az`, no HTTP to any hosted host, no fetch/worktree/checkout, no decision queue, scoreboard, ack, or briefs_staged; no Artifact/Docs/mail/chat tools. Only `gh api` GETs under the project's `GH_CONFIG_DIR`. Two files written.
