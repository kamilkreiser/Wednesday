STARTABLE: YES (after Tuesday stamps the 8 slots; load1 10.86 at 17:06 so launch_when_cool waits; one HPSM-POC gate, G203, is live beside it)

# B901 DRAFTER REPORT - kit for seat G204, tier-2 gate of PR #241 (Thu 29 Oct 2026, read at 17:0x AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B901_SEAT-G204_hpsmpoc-241-v12-shared-primitives-gate-tier2.md` (71 lines, long paragraph lines in the B868/B896 shape). Read-only drafter: GETs only, `git --no-optional-locks` read verbs, no clone, no run, two files written.

## BLUF
The kit is complete and follows the B868 (web tier-2) and B896 (today's lock/load) shape. Its new weight sits in C5, the B900-1 risk: a scrollWidth probe at 390/768/1024/1440 on every page the restyle touches, base vs the gate's own merge, with a width plant (p10) as the control that can fail, plus a PROBE tree that combines the sidebar branch and this head. Main has moved (PR #239 landed): the branch is ahead 6, behind 1, so the gate builds its own merge over `88569299` and runs the suites on that tree.

## Facts re-measured (instrument; control)
- PR #241: open, draft false, `mergeable_state` blocked, head `59625e5f...`, base `c00e2828...`, 6 commits, 20 files, +1103 -44 (`gh api -X GET pulls/241`). `pulls/241/files` printed 20 rows, all under `web/` (10 modified source paths, 2 new primitives, 9 added test files + the spec). Control: the two path lists below.
- Main now `885692995df9...` (`gh api branches/main` and `ls-remote`); `compare c00e2828...88569299` = `infra/README.md` + `infra/tests/test_security_baseline.py` (2 paths, PR #239). `compare 88569299...59625e5f`: ahead 6, behind 1, merge base `c00e2828`. `refs/pull/241/merge` = `d4fd300c7ad3...`.
- Overlap with PR #240 (19 paths): `grep -c -x -F -f` of the two `pulls/<n>/files` lists = 0 shared; control: #241's list against itself = 20. Open PRs: #240, #241.
- Required contexts (`branches/main/protection/required_status_checks`): 5, `strict` false, as the earlier kits. Repo merge settings `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`, squash allowed. `ci.yml` at main: `web-build` 371, `--check-shards` 426, `web-unit` 450, `web-e2e` 483-484 (job name `web e2e (${{ matrix.shard }})`), run line 515, `web (Next.js)` 527.
- Check-runs on the head at 17:0x (12 listed): dependency review and secrets success; CodeQL queued; api, two SQL Server jobs, infra, web build, web unit, four Analyze in progress; no `web (Next.js)` or e2e jobs yet. Nothing is finished; C8 waits.
- Ports 9920-9929: `lsof` rc 1 (empty). Word-boundary scan over 46 non-`.pre-` SEAT kits of 10-28/10-29: one hit, the 10-28 Composer gate kit B879 (it cites 9920-9939 as a stale scan result; another repo, no pane). Controls: `x 9920 y` = 1, `a9920` = 0. Panes: tuesday, HPSM-POC-G203, Security-Composer-G202, NexusAI-G200, NexusAI-G198, fleet-monitor; G204 count 0. So the block is free; if a live seat claims it the kit says pick another and say so (it does not include that line explicitly in Port block: Tuesday can reassign at stamp).
- Head source (raw at `59625e5f`): PageHeader :11/:19/:21-24, NextStep `StepNav` :14, `previousStep` :40, `NextStep` :49, Table `TableScroll` :13, Progress :9/:14. Consumer counts at base (`git grep -F -l`, tests excluded, control `NOSUCH-zz7f3a` 0): `<PageHeader` 39, `<StatusPill` 14, `<NextStep` 12, `<StatTile` 6, `<KpiTile` 3, `<ScoreBar` 2, `<BarChart` 2, `<Tag` 28. The shared checkout does NOT hold the head (`cat-file` error) but does hold both bases.
- Round count: first-lines loop over `Briefs/*_STATUS.md`: 454 files, 92 GATE VERDICT lines; control B805 and B817 both printed (count 2). Loose scan for primitive/restyle/PageHeader/Previous/NextStep/design-system/v1.2/shared component: one hit, B896 (infra README gate, other class). So "no earlier NO GO on this class".
- Builder STATUS B891 read whole (156 lines): its READY line, PRIOR WORK, 10 plants, 80 of 143 red at base, 3182 vs 3039, 356/46/0 vs 352/46/0, three disclosed flaky specs, and the disclosed gap (unsubmitted Assessment and unapproved Narrative mount no step bar, so no Previous there). B900 STATUS read as data: finding B900-1 is a CI-only `shell-sidebar.spec.ts:186` failure, `customers 1024: 1083px > 1024px`, 59 px with a 228 px sidebar.
- Kit self-checks: `grep -c '____'` = 8 (control on a scratch line = 1); `@[A-Z_]+@` = 0; non-ASCII bytes = 0; no person/customer name (grep 0); the quoted launch line carries `WED_USAGE_STOP=100` both outside the quotes (before `bash .../launch_when_cool.sh`) and inside, and `BRIEF_SEAT_LEVEL=sonnet` inside; the pattern matched once.

## D-decisions (mine, for Tuesday to strike)
- D-1 The gate builds its OWN merge (`wt-b901-merge`, local object in its own clone, never pushed) and runs suites there; the head tree is used for byte-equal and diff checks. Reason: the branch is behind 1 and only the merged tree will land.
- D-2 C5 is "never cut" and is a Major/Blocker class ("a shared primitive that widens content"). A combined probe tree (main + sidebar branch tip + this head) is a PROBE, not a verdict item; fetched by branch refspec `b885/...` (the template forbids pull refs), never #240's trees.
- D-3 Plant list: p1-p9 and p11 are verdict plants, p10 is the width plant that must turn C5 red (instrument-can-fail). p9 (wrong Previous target) and p10 are not the builder's.
- D-4 Escalation: tier 1 on anything role/auth-shaped; C7(d) greps the added lines for role/session/cookie/auth as the instrument.
- D-5 The Assessment/Narrative no-Previous gap is a Note with the builder's hand-off text, not a finding against this PR, unless the commission reads otherwise.
- D-6 Hard stop 210 min (target 150), longer than B868 (180/120) for 20 paths, one whole e2e run (about 5 min unloaded), 11 plants.
- D-7 No customer name: the kit says "the sample customer". The sidebar branch name and B-numbers appear in the kit (as in B896/B868), not in text the seat copies into commits.

## Q-questions for Tuesday (each with a default)
- Q-1 Does anything count toward the class? Default: no earlier gate on this class; "NO GO 0 of 2, round 1 of 2".
- Q-2 Is the combined probe tree (main + sidebar branch tip + head, scratch only, never pushed) approved for G204? Default: yes, as written (a PROBE; it fetches one extra branch refspec). If no, strike the third refspec and `wt-b901-combo`.
- Q-3 The Assessment and Narrative gap: Note or finding? Default: Note.
- Q-4 Order against #240: independent (0 shared paths). Default: whichever is ready first; if #240 lands first the kit rebuilds the merge on the new main and redoes C5 and the contrast table (the kit says so; a #240 landing is not a refuse).
- Q-5 Is G2 (Sonnet, tier 2) right for 20 paths / +1103 of UI code? G2's row lists tests/docs/config/tooling and "follow-ups whose mechanism a prior gate already measured"; a UI restyle is not named. Default: you ruled tier 2 in the order, kit follows; the kit carries the escalate-to-tier-1 rule.
- Q-6 If G203's heavy jobs hold load above 7 for hours: the kit says at most one heavy job of the gate at once, waits, and calls the verdict conditional. Default: accept.
- Q-7 Ports: B879 hit is stale; if you prefer to avoid even a stale-block reuse, name another block at stamp. Default: keep 9920-9929.

## Slot count
Unstamped kit: 8 lines with the four-underscore pattern (S1-S7 + the last line) - instrument `/usr/bin/grep -c -E '_''_''_''_'`; control a scratch line `a____b` = 1. The kit text says "8" in REFUSE.

## UNMEASURED
- CI and CodeQL results (none finished at 17:0x); the runner log of any e2e shard; whether the new spec file lands in `journey-and-prototype` or another shard (the gate reads `e2e.mjs` SHARDS).
- Any consumer's rendered look, the routes of the register and engagements pages (the kit tells the seat to find them; the sibling gate reads the register at `/workspace`, relayed).
- Whether `step-previous.spec.ts` or the restyle changes widths at 1024 (the whole of C5).
- The state of `b885` at the gate's fetch (its tip may differ from #240's head if the builder pushes again).
- Contrast numbers (builder's only).
- `restyle.contrast.test.ts` coupling to `contrast.ts` if #240 lands first (flagged in the kit).

## Outside the fences
None. Read: DRAFTER_RULES, the B868/B896/B900/B891 kits, B891/B900 STATUS, the design delta T05 section, `model-routing.md` (G2 :109, G-cap :111), `models_latest.json` lines 21-25, `brief_seat.sh` lines 20-26, GitHub GETs under the project `GH_CONFIG_DIR`, `git --no-optional-locks` read verbs on the shared checkout (`cat-file`, `grep`), `lsof`, `tmux list-panes`, `date`, `uptime`. Scratch files only in the session scratchpad (the two PR path lists and the verdict-lines list). No decision queue, no Jira call, no hosted host, no Artifact/Docs/mail.
