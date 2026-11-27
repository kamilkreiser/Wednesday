# B2149 GATE COMMISSION (G1 on Opus, one reader, in-session, READ-ONLY) -- Datasec / NexusAI: lane 2 kit 2 ROUND 2 OF 2, the data-erasure group (RD-744 Major 1, RD-824 Major 2, three unheld branches) (kit B2142, seat N183)

Commissioned by Tuesday (s333) after N183's READY (`READY B2142: 52040f2ed92734a450f64d39fb5610451a135bd5`, status_watch FINAL 12:16:49).

**Tier and model:** G1 (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md` line 108: data destruction; the kit's row C4, line 94), on Opus.

**Round 2 of 2 on this class.** Round 1 was B2136 (`2026-11-27_B2136_verify/`, GO WITH FINDINGS, NOT landed by Tuesday because of its Majors 1 and 2). Grade each finding Blocker / Major / Minor / Info and say whether it blocks landing. After a round-2 NO GO the rule is: ship what is closed, ticket the rest. So, for any finding that blocks, say exactly which commits (A to E of round 1; F, G, K2 of round 2) could still land safely.

**Output:** re-commission if `VERDICT.md` is absent. Its first line is `GATE B2149: GO`, `GO WITH FINDINGS` or `NO GO`, then `@ <head7> on main <main7>`. Return a 10-line summary.

**Form:** round 1's commission `2026-11-27_B2136_GATE_COMMISSION.md` and its folder (read both whole: every rule there applies here). Its landing form: MERGE COMMIT pinned to the head, never squash (C-190, `CLARIFICATIONS.md` line 2067). `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` binds you as a reader. Do NOT save any print of `kam_rulings_today.sh` or `kam_msgs.sh` to a file.

## THE LANE (Tuesday's reads by gh api -X GET after the READY; re-measure every one)

**Kit and records** (read whole, in pages):
- Kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2142_SEAT-N183_nexusai-lane2-kit2-round2.md`. Its stamp: Q-1 to Q-11 the drafter's defaults, plus Tuesday's own probes C1 to C6 at the stamp, which you may re-run (`/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/2ebf980d-d4c0-44c2-ac93-edacde66990b/scratchpad/st2142/t2142-probe.test.js`, if still present).
- Drafter report `2026-11-27_B2142_DRAFTER-REPORT.md`, including F-1: round 1's `names4.txt` held two names with a stray leading `b`. Re-run a name scan with the right four over BASE..head (`fleet/state/s332/d2142/frozen/names2142.py`).
- Seat record `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-27_B2142_STATUS.md` (read whole, its deviations first).

**Branch `b2133/lane2-erasure` at `52040f2ed92734a450f64d39fb5610451a135bd5`:**
- Round 1's six commits on BASE `279b22352dbcbd85664534395aeb366fec719a50` (A to E, ending at E `abef7000`), then F, G and K2 (G `76515f5b`, K2 `52040f2e`).
- Compare E...K2 reads ahead 3, behind 0, 4 files: `backend/dataErasure.js` +49 -9; the new `rd744-a-refusal-resolves-on-the-inode-this-run-removed.test.js` +242; the new `rd824-a-lexical-null-is-confirmed-by-the-kernel.test.js` +283; the counts file +3 -3.
- Main is still BASE; 0 open PRs.
- The seat reports local CodeQL at K2: results head 29, base 29, rc 0. Its control at round 1's K read rc 1. Both verifies `VERDICT: PASS - 6606/6606 tests passed across 417 suites`.
- No hosted build exists for a pushed branch: the PR's build is the first Linux run.

## WHAT TO DO

1. **Round 1's two Majors, now.** Can ANY re-drive still certify `purged` while a name outside DATA_DIR holds the erased bytes? Shapes to try:
   - an inode replaced at any of the four removal sites, before or after the snapshot;
   - a non-normalised or symlinked DATA_DIR, where the recorded key (`path.resolve(p)`) and the looked-up key (`path.resolve(dataDir, prior.file)`) may differ;
   - inode reuse after an unlink within one run;
   - a name refused, replaced and refused again.

   Can ANY link now be removed and certified purged while the kernel reaches data through it?
   - P14 and P14b;
   - longer and mixed chains;
   - a symlinked directory in the middle of a chain;
   - an absolute link text;
   - a link whose kernel target is itself inside DATA_DIR.

   Re-run round 1's gate probes (`fleet/state/s332/g2136/adv/g2136-probe.test.js`) at the new head.

2. **The new code's own risks.**
   - (a) `_noteRemovable` now records at the one-link return too: does any path record a name it then does NOT unlink, so that (b) of the property can be satisfied falsely? Consider a site that records, then refuses or throws before the unlink.
   - (b) `_kernelTargetOrNull` throws on any kernel answer other than ENOENT/ENOTDIR: does every caller catch that and keep the link as a failure, or can it abort the whole purge run?
   - (c) The walk's unnormalised join: can a crafted link text escape the loop key or the 256-link cap, or produce a path the walk never re-canonicalises?
   - (d) Does any changed line sit on a data-flow path of an open code-scanning alert? (The PR's CodeQL run is the authority.)

3. Red first at E and green at the head for the two new files, both shapes. Re-run all twelve mutations yourself. The whole suite once, with the pair 6606 / 417 compared against the project command's output. Every jest run happens inside `nexusai-lock.sh jest <tag>`, in dot-free trees. Another NexusAI build seat (lane 3, B2143, static/js only) may queue on the same lock: the FIFO wait is correct.

4. Three shapes outside each of THE PROPERTY (A2), (D2) and (E2): each covered or a named limit.

5. gitleaks (control first, rc 1) over `E..K2` and the three commit messages, plus the name scan with the right four names.

6. **Landing texts** into your folder, in round 1's form:
   - `landing.txt`: PR from the branch; MERGE COMMIT pinned to the head; the check names to expect (read from the last merged NexusAI PR); code scanning on the PR ref against main's baseline; the merge's Deploy demo run read as not deploying, approve NOTHING (C-224); the counts file regenerated by Tuesday if main's pair moved.
   - `pr-title.txt`.
   - `pr-body.md`: the whole branch, all nine commits, rounds 1 and 2. Say that commit A's pushed message reads "or this run purged it" and that commit F corrects it. No person's name, card, seat or build id. The choices are the coordinator's. Include the named limits.
   - `FOR-RECORDS.md`: RD-744, RD-750, RD-745 (its dataErasure half) and RD-824, each with its comment and whether it moves to Testing (project `CLAUDE.md` line 302); round 1's Minor 1 (P9) to a new ticket; your own findings to file.
   - Round 1's `landing.txt` and `pr-body.md` are SUPERSEDED.

## WRITE ONLY

Your outputs:
- `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2149_verify/` (evidence and landing texts).
- Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/g2149/`.

Boundaries:
- READ-ONLY toward the project checkout, Jira and GitHub (`gh api -X GET` only under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'`).
- Your own clone of the branch in scratch; dot-free trees for jest; every jest run inside the lock with `NODE_OPTIONS` unset; every cell in its own temp folder.
- No pull request, no push.
- No `cd`. Never delete (quarantine). A hook refusal is a STOP for that action.
- No Azure, no demo host, nothing to any human.
- No typed clocks (print `date`).
- If your context nears its limit, write `VERDICT.md` with what is measured and mark the rest NOT RUN.
- Leave no background process running and no lock held.
