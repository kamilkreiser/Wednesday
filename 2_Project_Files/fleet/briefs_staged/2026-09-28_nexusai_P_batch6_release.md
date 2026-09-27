# BLUF — Datasec/NexusAI-P (lane 4): BATCH 6 IS BACK and you are its MERGE AUTHOR. RELEASE: merge FIVE of the six to NexusAI main, one at a time, in the order below. RD-686 is NO GO on words only (round 2 of 2 under the cap: correct three phrases, then READY). This SUPERSEDES the queue order of my 02:00 mail ("RD-430 -> RD-694 item 4 -> RD-719 (a) -> RD-721"): the merges and the RD-686 words come FIRST, then that queue unchanged.

Verdict: QA/NexusAI-batch6, 21:47Z, report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch6/report.md` (read whole by Tuesday). Read §0, §10, §11 and §16 yourself before the first merge.

## THE RELEASE — five merges, this order, one at a time (the gate's clone-1 order without RD-686)
Main at this mail = `02fe76a` (ls-remote by Tuesday 07:49 AEST). Heads at origin, read the same minute, EQUAL the gated heads:
1. **RD-286** `rd-286-ground-geometry-guards-s85p` @ `1645c69` — GO WITH FINDINGS (tier 2 + browser).
2. **RD-204** `rd-204-vendor-coverage-s84p` @ `fe47bb4` — GO WITH FINDINGS (tier 2).
3. **RD-197** `rd-197-emphasis-ground-guard-s84p` @ `43e729c` — GO (tier 2).
4. **RD-692** `rd-692-provisioning-token-guards-s85p` @ `4580829` — GO (tier 2).
5. **RD-693** `rd-693-token-clear-on-leave-s85p` @ `ddf1b75` — GO WITH FINDINGS (TIER 1).
The gate proved a second order gives the same tree except the counts placeholder; keep this one.

**Per merge (the batch-1/batch-4 pattern, C-68 / C-57 / C-89):** re-read `git ls-remote origin refs/heads/main`; merge the then-main FORWARD into the branch in a worktree (never rebase a gated commit, C-68); re-run the C-68 set the gate names for that ticket (§10 per-step sets); regenerate counts ONCE on the merged tree (never hand-edited); C-57 id-superset; full verify through `session-tools/nexusai-lock.sh` with SESSION_SECRET unset (queue, never take over); push; confirm `deploy-demo.yml` was SKIPPED for the push (vars.CI_DEPLOY_ENABLED was unset at the gate — a merge must not deploy; if it did NOT skip, STOP and mail); wait for the CI Build to go green before the next merge. The gate's arithmetic on the moved main: **4192/253 after all five plus nothing else** — a PREDICTION from 02fe76a; if O has merged more of batch 4 first, your numbers move with it and that is expected.
- **O (lane 3) is merging batch 4 on the same main in parallel.** If your push is refused because main moved, merge the new main forward again and re-verify. Never force-push. Name any O merge you absorbed in your MERGED mail.
- RD-692 then RD-693: re-run rd692 BY NAME after RD-693 lands (U1; the gate measured 5/5 with RD-693's listeners).
- Any missing id in the C-57 superset is a STOP: do not push, mail Tuesday the id.

**MERGED mail per merge**, to tuesday-agent@: ticket, new main sha (ls-remote), both parents, counts (predicted vs regenerated), C-57 result, deploy-demo SKIPPED (run id), CI Build run id and result. Then the next merge.

## RD-686 — NO GO, words only, ROUND 2 OF 2 (a further NO GO goes to Kam)
Correct the three phrases the gate measured false in the unsafe direction (report §7, §16 item 1), as WORDS — do not change the gates in this round:
- F-E1: "`dark-mode.css`: every colour" / "every rgba() … must resolve" -> say what is read: every hex, the FIRST rgb()/rgba() of each declaration, every `--*-rgb` triple; named colours and later functional colours in the same declaration are NOT read.
- F-E2: "pins how often each TOKEN value occurs" -> "each MEASURED token value"; name that `--nx-brand-chrome` `#00719f` has no pinned count.
- E8's closing sentence to match both.
Then READY FOR QA (tier 2, through-code). **Also file ONE ticket** for making the gates match the old words (read every functional colour, pin brand-chrome), citing E1A/E1C/E2A as the red cells; not built now.

## TICKETS FOR THE FINDINGS (after the merges; one ticket per fix one test pass proves)
- RD-693 A-F1 + A-F2 (Minor): the missing tab-switch, double-evaluation and second-restore cells (§16 item 3, red-proved against M-A7b, M-A5, M-A6).
- RD-286 B-F1/B-F2/B-F3 (Minor): RD-288 dark refused 3 of 11 runs; the population is unpinned; a per-element inverse (§16 item 4). B-F1 may belong to RD-701 (determinism) — say which.
- RD-204 C-F1/C-F2 (Minor): declare the element-selector skip (or include body and re-pin), note currentcolor grounds, and put the out-of-repo derivation (`session-tools/s84p/rd204/derive-families.js`) where the repo can reproduce it (§16 item 2).
- Note for RD-409/410's owner (a comment, not a ticket): first-run's provisioning panel is hidden in the default wizard state (a10).
- The `.text-danger` light colour `#dc3545` (not a token) is a BRAND note for Kam. Tuesday carries it to him. Not yours to change.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- rd104-gh-identity-acceptance-false-premise: "You check the two settings pages yourself - two clicks, links below (recommended)" (2026-09-07) -> Kam's own action; nothing for P to land. Carried for the record.
- t9-nas-leg-direction: "Make this drive's backup ONE-WAY, drive to NAS, additive" (2026-09-21) -> not P's work (drive backup tooling); nothing for P to land.

## HOLDS
- No deploy, no demo, no Partner Center, no `.github` change. Client-facing communication = ticket comments only.
- PRIOR-WORK CHECK before rebuilding or removing anything; every READY carries PRIOR WORK.
- Never delete; quarantine.

PROVENANCE:
- batch-6 verdicts + order + arithmetic | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch6/report.md §0 §10 §16 | read 2026-09-28 07:4x
- main 02fe76a + six heads equal to the gated heads | git ls-remote origin in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files | read 2026-09-28 07:49
- P's previous queue | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-28_nexusai_P_rd705_half_dropped.md | read 2026-09-28 07:4x
- per-merge procedure | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-27_nexusai_O_batch4_merges.md | read 2026-09-28 07:4x
Self-check note: five GOs merged in the gate's order, 686 held for words only, queue superseded by name, O's parallel merges named.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 07:50
