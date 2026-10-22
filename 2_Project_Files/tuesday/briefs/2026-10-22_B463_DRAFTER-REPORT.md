# B463 drafter report (2026-10-22 ~16:10 AEDT)
- Kit: `2026-10-22_B463_SEAT-G36_hpsmpoc-b459-login-gate-tier2.md`, cloned from B441 (G34); 9 checks, pane `Datasec/HPSM-POC-G36`, ports 8160-8169, hard stop 19:00, target verdict 18:00.
- MEASURED read-only 16:04: main `a93b926a` unmoved; branch `26460869` = 1 commit, 2 files (+222/-9); `b463*` none; `.tools/b463` absent; ports 8160-8169 0 listeners; load1 7.33.
- Telemetry branch now `473bfaca` (was `39d4d1a2` at the B441 stamp): the kit reads it only; overlap check is live, not assumed.
- Stamp slots (four underscores x4) and the final READ-WHOLE line are blank for Tuesday; the REFUSE grep uses the split pattern.
- Source read: the head `UatStartScreen.tsx` (levelItem helper, one `li role=separator`); the "form markup byte-for-byte" claim is set up as an attack in check 4.
- Load threshold set to 8 (the B459 brief's), since the machine sits at 7-8.
- Not run: tests, builds, browser. Nothing else written.
