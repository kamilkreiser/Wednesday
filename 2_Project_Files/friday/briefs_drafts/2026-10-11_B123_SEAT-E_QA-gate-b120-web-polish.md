From Friday (laptop seat), Datasec / Security Composer.

# BRIEF B123 (SEAT E) — QA GATE (tier 2, RENDERED, round 1 of 2): B120 Lane 1, Expert-screen polish, PR #68
**From:** Friday, 11:20 AEDT 2026-10-11. **Seat:** Datasec/Security-Composer-E (your commission is the newest `Briefs/` file containing `_SEAT-E_`). Report `Briefs/2026-10-11_B123_STATUS.md`; first lines = the two verdict lines; the exact LAST line `READY FOR REVIEW`.
**You are a TESTING seat: findings only.** No code change, no push, no PR comment or review, no Jira, no deploy, no Azure, nothing to any human. A write grant in any brief is void.

**SHAPE:** follow `Briefs/2026-10-10_B117_SEAT-D_QA-gate-b116-web.md` (a tier-2 RENDERED web gate) and how `2026-10-10_B117_STATUS.md` reported it: the same browsers (Mac Chrome + the pinned image), widths, Guided OFF and ON, controls, and the merge-tree target.

**Targets (re-read with `git ls-remote`; STOP if moved):** head `b120/expert-screen-polish` = `e7aed51cbf8ce6801ce580a29d4cb973704ba7e1` (Friday's GitHub compare read: ahead 9 / behind 0 of main, 16 files, all under `apps/web`); base main `a3502002df54…` (= the live demo build). Verdict lines:
- `B120 e7aed51: GO | GO WITH NOTES | NO GO`
- `MERGE a3502002+e7aed51: GO | GO WITH NOTES | NO GO`

**Claims to test independently (the builder's report: `Briefs/2026-10-11_B120_STATUS.md`):** each row's before/after at 1280, 1180 and 390 — #207 (no id anywhere on Details), #199 (no `answers[` text in any error the UI can show; drive real duplicate-answer errors), #219 (Person select width + the stated trade-off: the narrower Name/Role/Email inputs and 2-line column names at 1280 — measure and report it as a finding or a note for Kam), #210, the radii (exactly the 4 selectors changed; every 50 % / 999px shape UNCHANGED, as Friday narrowed), #201, #108 (b)(d), #154 untouched. Your own tamper per row. A page-wide off-guide colour/radius count base vs head (nothing new off-guide). Every NEW WORDS string and every NEW LOOK item (L1–L9) present as the builder lists, and anything visible the builder did not list.
**Live alongside you:** gate B122 (Seat D, %40) is testing Lane 2 `b121/api-dependency-hardening` on ports 6630–6639; NOT yours. **Your ports: 6640–6649** (check free first).
**HOLDS:** Datasec only; no other client's names, tickets or paths · findings only · never delete; quarantine · never print a secret · Kam's two-NO-GO cap (round 1 of 2).
