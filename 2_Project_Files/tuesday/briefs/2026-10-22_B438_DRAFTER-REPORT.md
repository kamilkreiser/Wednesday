# B438 drafter report

Brief written: SEAT-L2 B438, pane Datasec/HPSM-POC-L2, Sonnet, tier-2 gate after. Structure and fences copied from B434 (refuse block, standing lines, partition, base/branch/identity, stamp, launch, report sections). Changed: commission (B435-1), build (UAT compact tokens to `md`), measure matrix (head vs `01dd9e4b` vs pre-badge `35b2b73`), regression test, mutants, ports.

Measured by me (read-only):
- `ls-remote origin refs/heads/main` = `01dd9e4b4d9225999a2830343b1d4bf9f29966ac` (matches the task).
- Ports 8090-8099: no listener (no positive control run; the brief tells the seat to run one).
- Local checkout `web/e2e/` lists only `smoke.spec.ts`; `playwright.config.ts` has one chromium Desktop Chrome project, `webServer` = `npm run start`, no UAT env. B434 STATUS says `e2e/responsive.spec.ts` exists (mock only). So a UAT e2e row may not be possible without editing `playwright.config.ts`, which is outside the partition.

Decisions for you to check:
1. Item 4 fallback: if no e2e can switch UAT on without the config, the seat does not edit the config. It records why, puts the measure evidence under `Briefs/…_evidence/`, and adds jsdom class-token tests in `shell/`. If you want the config in Yours, widen the partition.
2. Unmeasured: line numbers are the gate's (at `683a6ba`); main moved, and the seat is told to re-measure them. I did not read AppShell.tsx at main.
3. Measure tool: B434's `measure.mjs` and B435's `measure.cjs` live in other seats' `.tools/b4*` trees, which I may not open and the seat may not open either, so the seat rebuilds the tool from the STATUS text.
4. The brief adds `35b2b73` as a third build (reference for "one row where base had one row"), so five servers (8090-8094) plus `35b2b73` on 8092.
5. Tier stays 2, per B434 (UAT-only class tokens, no words).

Stamp slots: 6 occurrences of the slot token (5 in the Stamp paragraph: stamp time, authority, hard stop, target READY, trailing; 1 in the final `READ-WHOLE-BY-TUESDAY` line). Fill all six.

Paths:
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B438_SEAT-L2_hpsmpoc-uat-header-compact-to-md.md
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B438_DRAFTER-REPORT.md
