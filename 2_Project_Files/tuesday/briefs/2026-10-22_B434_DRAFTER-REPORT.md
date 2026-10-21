# B434 drafter report (2026-10-22)

**Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B434_SEAT-L1_hpsmpoc-uat-badge-label.md`. Slots `@STAMP@` x4 (Stamp paragraph: time, authority, hard stop, target; final READ-WHOLE line) for Tuesday to fill.

**Findings**
- Base read: `ae7a2c86` (object present locally). `git ls-remote` FAILED (deploy-key path `/Users/kamilkreiser/1FILES TO SYNC/HPSM-POC/3_Access_Keys/analysis_deploy_rw` absent), so current origin main is UNMEASURED. The local `main` ref is the stale 23 Sep skeleton (`8869b1a9`). The brief tells the seat to re-read and report a failed fetch first.
- Mode flag already exists: `AppShell` takes `auth: "mock"|"entra"|"uat"`, so no new flag is needed; badge = `auth==="uat" ? displayName : ROLE_LABEL[role]`, guarded to the four strings.
- **Trap found:** `UatStartScreen.test.tsx:139` pins the badge as `Admin`. It goes RED by design; the brief allows that one assertion edit outside `shell/`.
- `hosted.test.tsx` uses `displayName: "Synthetic Reviewer"` on entra; the brief pins that it must not reach the badge. This is why the guard and the entra test exist.
- Tier: G2 (tier 2) kept: one prop-driven text choice, lock logic untouched.
- Ports 8040-8049 free at drafting (nothing listening 8000-8070; no positive control run, the seat must run one).
- Partition and B432 (`b429/telemetry-224`) named from both sides. B409/B410 named in PRIOR-WORK. Brief is about 70 lines of dense text.
- Not done by me: no tests, build, fetch, or HTTP. 390 px measurement method is left to the seat (jsdom cannot measure layout).
- Fence note: a zsh `$VAR:path` colon-modifier ate `:w` in my first git calls; the brief carries a line warning the seat.

Paths: the two files above.
