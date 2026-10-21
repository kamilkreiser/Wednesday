# B435 drafter report

Brief written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B435_SEAT-G32_hpsmpoc-b434-badge-gate-tier2.md`. Tier-2 findings-only gate, pane `Datasec/HPSM-POC-G32`, Sonnet.

Read whole: B421 template, B434 commission, B434 STATUS, fleet BRIEF_TEMPLATE (it is a Wednesday/QA-agent template, so I followed B421's structure, not its fields).

MEASURED by me (read verbs only), this session:
- `ls-remote origin`: main `35b2b73ebf570878be3aea999e0af08a3fcbbfbf`, `refs/heads/b434/uat-badge-label` `683a6ba3eeccfabddea627067986963bb1662ce1`, no `refs/heads/b435*`.
- `levels.sonnet.model_id` = `claude-sonnet-5-5`; routing row G2 at `model-routing.md:109`.
- `lsof` on 8010-8049: no listener (no unfiltered control run by me; the brief makes the tester run one).
- `.tools/b434` and `.tools/b198` exist; no `.tools/*b435*`.
- Not re-measured by me: the 3-file list and +/- counts (taken from your 07:36 verification), the builder's numbers (all marked RELAYED in the brief).

Choices for you to check:
- Port block **8050-8059** (not 8010-8049, per your fence). I did not check it is free; the brief's REFUSE makes the tester check with a control.
- Stamp slots: `@STAMP@` appears for stamp time, hard stop (twice) and the final `READ-WHOLE-BY-TUESDAY: DONE @STAMP@`; you fill them all (the REFUSE count must read 0). Hard-stop target is "90 minutes before" as a relative phrase only.
- Escalation to G1: a label shown for a foreign name, Entra name reaching the badge, a protected file changed, or any security-shaped issue.
- Added beyond your list: a mock-mode computed-style comparison for "non-UAT gap unchanged", 375/360/768 px as Notes, `web/e2e` badge-text grep, gitleaks and merge-tree (no PR so CI is stated as "none", never green), 12 off-diagonal role/label pairs in the probe, and an evidence-class tag on each finding.
- Last line carries `(no PR yet: CodeQL not run)` exactly as you specified.
- The brief says the builder's `webrun.sh`-style scripts and `.tools/b434` are off limits; the tester needs its own `npm ci` per worktree (builder measured Turbopack refuses a symlinked `node_modules`).

Length: the brief is over your ~70-line target in characters (long lines, about 45 lines); no wrapping.

Files written: the two paths above. Nothing else touched.
