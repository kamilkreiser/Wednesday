# Gateset 2026-10-01_gate50a — README for Wednesday

Written by the drafter, 2026-10-01 AEST (all times UTC from `date -u`; the host clock reads 2026-09-30T21:xxZ). Every figure below comes from the kit's own output files, each named beside the figure.

## 0. Status and what remains

**KIT COMPLETE — READY to launch once the routing line (section 4) is added.** Launcher `--check` rc 0 before and after the controls (launcher_check_1.out, launcher_check_2.out). Launch-action `--dry-run` rc 0 (repin_dryrun_1.out): the ONLY report is the missing routing line; `BOTH INSTRUMENTS AGREE with the pin, 1 of 1`; census `0 touch a kit path … outside reported_overlaps | 11 expected overlap(s)`. Controls normal **rc 0, 144/144 OK**; `--invert` **rc 1, 144/144 MISMATCH** (section 5). Final ls-remote 2026-09-30T22:12:50Z: develop `4f18c59a89db`, #1363 `9e84e1fabafe` (final_lsremote_1.out). **Still Wednesday's: the routing line and the launch (section 9).**

The kit was drafted **PINNED** (no `pinpr` step, unlike gate49a): Wednesday named **PR #1363, head `9e84e1fabafe1ecc1963953051759c4038f88db2`**, and the drafter re-read it at 2026-09-30T21:23:51Z by `ls-remote` (branch AND `refs/pull/1363/head`) and by the PULLS API (gh_read_1.out). A new head is a RE-DRAFT (section 8).

**What the drafter did and did not do.** It launched nothing, added no routing line, sent no mail, tapped no pane, merged / committed / pushed nothing, posted nothing, changed no ticket or PR, deleted nothing (a superseded output is renamed `superseded_*`). It wrote only this kit directory and its session scratchpad (`g50a_sp/`: a `git clone --shared --no-checkout` of gate49b's scratch clone, with develop, `refs/pull/1363/head` and `refs/pull/1363/merge` and the census PR heads fetched from origin ONLY there; the control plants). In `/Volumes/DevMASTER/!CODING/` it ran `ls-remote`, read files, and ran the seat's `gatelines46.py` with python3 on SCRATCH logs (read-only, controls GL0/GL1). External reads: GitHub REST GETs, public advisory-API and npm-registry GETs, AgentMail listing and GETs by id (read-only). No install, audit, regen, build or suite.

## 1. The PR and the BLUF

| PR | ticket | tier | head | parent | ahead / behind | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1363 | KS-1378 | T1 | `9e84e1fabafe1ecc1963953051759c4038f88db2` | `4f18c59a89db` (= develop, #1361's merge) | 1 / 0 | 4 locks, **+19/-19** | 75 -> 83 (PR title == commit subject) |

- Pane `QA/Secuura-batch1363` (**not routed** — section 4). GO string (the GO mail's SUBJECT): `GO (Seat B 51st): merge 1363 on gate50a`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-01-batch1363-g50a/` (does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE50A #1363 (Seat B51 author and merger, round 50a; T1 in-range lock refresh: axios 1.20.0 in 4 locks, dompurify 3.4.16 in the root lock; the new-ticket text ruled)`.

**END_TREE `2a874956406ca974f3090b24392f6dbfdc8bc4d6`** — computed as gate49a did (pin_gate50a.py (F): `git merge-tree --write-tree develop head`, then `commit-tree -p develop` as the simulated squash; `4 files changed, 19 insertions(+), 19 deletions(-)`), and cross-checked two more ways in end_tree_crosscheck_1.out: the head's own tree (parent == develop, 0 behind) and GitHub's test-merge `refs/pull/1363/merge` (`7467f431d12b`, parents develop + head) — all three `2a874956406c`; develop's own tree `25e343e81412` is the control that differs.

**Drafter predictions (the gate re-derives each):**
- pin_1.out `PASS`: develop `4f18c59a89db16cb8b06b7850aeb64e6f81f95ee` (tree `25e343e8141241ae6f617b92c3b3f612c28a2c8a`), 4 paths all 100644 (control `.githooks/pre-push` 100755), 12 hook / audit / Dockerfile paths identical, 12 unchanged pins byte-equal (baseline `6fc1e1c95ca7`, contract `16ad64fd42b0`, stub, kyc Dockerfile, 5 manifests, issuer's lock, `sanitize.ts`, mobile's lock `2f5f8c1f4edf`).
- lockdelta_1.out `LOCKDELTA PASS: 0 FAIL of 50 checks`: 4 locks, **5 moves (all PROD)**; MOVED / ADDED / REMOVED = root 2/0/0 (1968 entries), admin 1/0/0 (329), verifier 1/0/0 (308), kyc 1/0/0 (262); == the seat's claim one to one. **The drafter's own finding: each axios entry ALSO changes `dependencies.form-data` `^4.0.5` -> `^4.0.6`** (axios 1.20.0's registry manifest, L5d) — the extra +1/-1 per axios lock that makes +19/-19; form-data 4.0.6 already resolves in all four locks (L4d; control L4dc 17/17). 9 dependant ranges satisfied (control refused 9/9). Registry-true for axios 1.20.0 and dompurify 3.4.16 with both controls False. All 13 advisory ranges read from the API: every to-version outside, every from-version inside. **Residue at the head: only `mobile/secuura-app` axios 1.13.2 (PROD), inside 6 of the 12 axios ranges** (KS 769). The fast-uri stub fixture still covers 7 entries (leg 7 refusal control stays live).
- reach_1.out `REACH READ`: 3 Dockerfiles copy a moved lock (admin, verifier, kyc); **0 copy the root lock** (kyc's own COPY found as the control); at develop the same read gives 0 (control). kyc's final stage `npm ci --omit=dev` ships axios. 7 test files name the root / generic lock.
- overlaps_1.out `OVERLAPS READ: 11 PR(s)`: 10 dependabot PRs on the root lock + **Peter's #1360** (KS-1380 "revert #1358 (15 lockfiles)", root AND kyc locks). All clean after #1363 except #649 (already CONFLICT today). **None touches an axios / dompurify entry.**
- keyscan_1.out `KEYSCAN PASS: 6 checks, 0 FAIL, 0 FLAG`; the PR body `gh_body_1363.md` == the seat's record `pr-body.md` byte for byte (sha256 `d366bcab3f00…`, as the READY says).
- capture_1.out `CAPTURE OK`: 18 mails by id from one listing (the LAUNCH BRIEF id + sha256 only; route (a) 20:54Z present; the READY 21:21:17Z names the head in full and the base; the captured READY is contained in Wednesday's `READY_1363_mail.md`).
- gh_read_1.out: 22 other open PRs; Peter's open PRs are now **#1360 and #1362** (gate49a's #1351-#1353 are gone): kit.json `client_human_prs` updated.

## 2. What the gate must rule (by name in the prompt; the launcher refuses a prompt missing any of the 32 keywords)
1. **LOCK-DELTA-4, OWN-DEPENDENCIES, DEPENDENT-RANGES, REGISTRY-TRUE, REPRODUCE-REFRESH, PRISTINE-CONTROL** — the four diffs re-derived and regenerated in `node:24-alpine` / npm 11.19.0 against a pristine control, byte-identical; only axios / dompurify moved; MOVED/ADDED/REMOVED per lock; **the form-data range line ruled**. The prompt carries gate49a's root-mount finding (N-1356-4): root lock with the root mount, admin / verifier / kyc (workspace members) with the per-directory mount.
2. **AUDIT-LEGS-BASE-HEAD, THIRTEEN-IDS-ABSENT, GATE-STILL-REFUSES, NO-BASELINE-ROW** — develop 1/1/0, head 0/0/0; a refusal control PER LEG (leg 7: the stub; leg 6: an empty baseline, N-1356-5; contract: a planted baseline defect).
3. **ADVISORY-MAP** — the 13 re-derived one to one with an empty-baseline discriminator, compared to the READY's table.
4. **RUNTIME-REACH, ROOT-LOCK-CONSUMERS, SUITES, NPM-CI-HEAD** — kyc / admin-frontend / verifier-frontend / issuer-frontend built develop vs head (`-p g50aprobe-base|head`, build only); served axios in kyc; the root lock's workspace consumers (issuer build + resolved dompurify); kyc suite; the untested dompurify half probed only if a DOM lib is already installed.
5. **MOBILE-UNTOUCHED** (KS 769).
6. **CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS** (incl. what Peter's #1360 would do after the merge).
7. **SUBJECT-*, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS** — every factual line of the body and Test Evidence; both MG-3 key sets (with / without the new key).
8. **NEW-TICKET-TEXT** — POST AS-IS / POST AMENDED (full text) / DO NOT POST, sentence by sentence; client-visible.
9. **GATELINES-VERDICT** — a tooling finding, not this PR.
10. FUSE-COUNT, TIERING, DISK-ENOSPC, REPORT-HASH-LAST. The prompt tells the gate the change is SMALL and the pass must be proportionate (usage 76%); the launcher refuses a prompt without that line (exit 38).

**Doubts the drafter found (all in the prompt for the gate to rule):**
- (a) **The form-data range line** in each axios entry: not in the READY, the PR body or the commit message; the brief's "ONLY axios and dompurify entries moved (plus integrity/resolved)" is met at entry level but not at line level. Consistent (4.0.6 resolved everywhere; registry manifest matches). Likely Polish/Information.
- (b) **The publish window is wrong on client-visible text.** The PR body and the proposed ticket say "between 15:03:21Z and 15:37:57Z" (commit: "15:03-15:37Z"); the advisory API reads GHSA-542g-h47m-68v8 at **15:01:07Z**, GHSA-3pq3 15:02:14Z, GHSA-x97p 15:02:45Z, GHSA-mghh 15:03:02Z (lockdelta_1.out L6). The ticket needs POST AMENDED at least for this sentence.
- (c) "moderate" (npm audit's word) vs the API's `medium`; "every one with first_patched 1.20.0" — two (x97p, 9fr6) also list 0.34.0 for the 0.x line.
- (d) The 11 / 14 / 15 counts (leg 6 reported / dead grandfathered rows / "15 distinct ids") need reconciling to their source lines.
- (e) Peter's #1360 touches two kit locks; clean after the merge and does not touch axios/dompurify — report only.
- (f) The seat's record keeps no root-lock before/after copy and refresh46.out does not state the mount per lock; the gate's reproduction settles the bytes.
- (g) **X6 is a drafter addition**: read-only GitHub REST GETs for the census (gate49a said it could not re-read PR state without them). Remove it from the template and re-fill if you do not want it granted.

## 3. Pins and what the gate owes
- The prompt `2026-10-01_secuura-batch1363.prompt.txt` and the launcher `launch_qa_secuura_batch1363.sh` are FILLED by `fill_gate50a.py` (fill_1.out rc 0; sha256 in fill_1.out). The fill refuses unless gate49a's report still hashes to `ddbb07ecd9de…`, `end_tree_crosscheck_1.out` carries END_TREE three times, and every drafter read ends in its PASS/READ/OK line at this head.
- The launcher refuses on everything gate49a's did (exits 2-39) plus **37** (the NEW-TICKET ruling missing) and **38** (the proportionality line missing); the authority check is now route (a) (`ROUTE (b) IS REFUSED.`, `No manifest change.`, the survive-STOP line).
- Named exceptions: X1 registry reads; X2 refresh containers on a scratch `git archive`; **X3 TWO builds** `docker compose -p g50aprobe-base|g50aprobe-head build kyc admin-frontend verifier-frontend issuer-frontend`; X4 advisory / registry GETs; **X5 read-only Linear queries (≤5)** for the ticket text; **X6 read-only GitHub GETs** (see doubt g).
- `reported_overlaps` (kit.json): the 11 PRs with their heads, filled at the pin. An overlap OUTSIDE that set refuses rc 15. `sequenced_out_of_kit` is EMPTY.

## 4. Routing line — NOT added (gate49a's drafter did not add one either)
Back up the file first (`inbox_routing.conf.pre-<date>`). Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (currently 161 lines, the last `QA/Secuura-batch1357|coagent@agentmail.to|yes`):
```
QA/Secuura-batch1363|coagent@agentmail.to|yes
```
Until it is present, step 0 of the launch action refuses rc 1 (control R1); R8 shows a routed temp file passing step 0 and stopping after 3b.

## 5. Controls: `controls_gate50a.sh <scratchpad> [--invert]`
- **144 controls, one unedited script** (`controls_gate50a.sh`, sha256 `b829ef982f82…`, identical before run 1 at 21:51:47Z, before run 2 at 22:00:23Z and after run 2 at 22:12:14Z: controls_sha.txt). Normal (controls_1.out) **rc 0: `144 controls, OK 144, MISMATCH 0 | ssh-denied retries 0`**. `--invert` (controls_2.out) **rc 1: `144 controls, OK 0, MISMATCH 144 | ssh-denied retries 1`**.
- Side effects, kept: R1 / R8 wrote `launch_<HHMMSS>.*` step outputs here; the PN simulations wrote `pins_gate50a.SIM-*.json`.
- **Coverage:** PN0-PN7 (pin: the real head as a simulation; `--develop` refused without `--simulate`; kyc Dockerfile edited -> (K); a develop move on kyc's lock -> (C); kyc's lock recorded 100755 -> MODE MISMATCH; an unrelated develop move -> NONE; kyc package.json added -> (B); mobile's lock edited -> (K)). LD0-LD8 (lockdelta: the real head incl. the allowed form-data line, L4dc, L5d, L5c, the 15:01:07Z publish time, the mobile-only residue; another kyc entry edited -> L2 + 6 moves; dompurify integrity flipped -> L5 online; admin's form-data range ^4.0.7 -> L2x NOT ALLOWED + L4d; a dev flag on root axios -> L2 flags; verifier axios 2.0.0 -> L4; admin reverted -> L0 missing; develop as head -> L0 0 paths; the semver table). RE0-RE1, OV0 (+CT pair, #1360 line), KS0-KS8, **GL0/GL1/GL1b + GLS** (gatelines46.py's sha256, MATCHES on 28/0 6/0 49/0, `MISMATCH — STOP` on 28/1). L0-L23 + LK1-LK32 (launcher: every exit incl. new 37 and 38). R0-R8 (launch action). PNZ/KJZ/PRZ (pins, kit.json, filled prompt unchanged).
- **The drafter's own instrument error, caught by its control and kept:** the first normal run read 143/144 — LD4 (a `dev: true` flag planted on root axios) crashed lockdelta with `TypeError: 'bool' object is not iterable` in the new L2x code (a scalar field treated as a dependency map). Fixed; the real-head reading is byte-identical before and after the fix (`diff` of the two outputs, timestamp line excluded). Kept as `superseded_controls_0_ld4_scalarfield.*` and `superseded_lockdelta_0_scalarfield.*`. Also kept: `superseded_fill_0_dockerfilenames.*` / `superseded_launcher_check_0_dockerfilenames.*` (the HOOK line printed four bare `Dockerfile` names).
- **Not controlled:** on a real launch the usage gate (12), `cockpit.sh add` (14) and the override refusal (16); a `mergeable=False` refusal; a real re-pin across a develop move (the dry run's rc 10 only); capture_mail_gate50a.py, gh_read_gate50a.py and fill_gate50a.py are exercised by their real runs, not by plants.

## 6. Could not measure (the drafter)
No audit leg, install, regen, image build, served-file read or suite: each is the seat's claim until the gate runs it. Nothing checked against Linear (the ticket-text sources KS-1378 / KS-1395 are quoted from the READY only).

## 7. Files
- **Config:** kit.json · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md (this) · READY_1363_mail.md (Wednesday's copy of the READY; unchanged).
- **Pin:** pin_gate50a.py -> pin_1.out, pins_gate50a.json (+ `pins_gate50a.SIM-*.json` from the controls) · end_tree_crosscheck_1.out.
- **Reads:** gh_read_gate50a.py -> gh_read_1.out / gh_read_1.json / gh_body_1363.md · capture_mail_gate50a.py -> capture_1.out, mail_gate50a_ready.md.
- **Instruments:** lockdelta_gate50a.py -> lockdelta_1.out · reach_gate50a.py -> reach_1.out · overlaps_gate50a.py -> overlaps_1.out, overlaps_gate50a.json · keyscan_gate50a.py -> keyscan_1.out (each with its .rc).
- **Prompt and launcher:** prompt_gate50a.TEMPLATE.txt + launcher_gate50a.TEMPLATE.sh.txt, filled by fill_gate50a.py (fill_1.out) -> `2026-10-01_secuura-batch1363.prompt.txt`, `launch_qa_secuura_batch1363.sh`, COMMISSION.md; launcher_check_1.out (before the controls), launcher_check_2.out (after).
- **Launch:** repin_and_launch_gate50a.sh -> repin_dryrun_1.out (rc 0).
- **Controls:** controls_gate50a.sh -> controls_1.out / controls_2.out (+ .rc), controls_sha.txt.
- All scripts are NEW COPIES of gate49a's (re-keyed by the scratchpad's `rekey.py`, then edited); gate49a's kit is untouched. No `pinpr` (drafted pinned).

## 8. Re-draft recipe (a new head on #1363, or a develop move that reaches a kit path)
Keep kit.json as `kit.json.pinned-9e84e1fa`, set `prs.1363.head` (and `pinned`) to the new head, then: `pin_gate50a.py <sp>` -> `gh_read_gate50a.py` -> `lockdelta_gate50a.py <sp>` -> `reach_gate50a.py <sp>` -> `overlaps_gate50a.py <sp>` (refresh `reported_overlaps` if the census changed) -> `keyscan_gate50a.py <sp>` -> `capture_mail_gate50a.py` -> re-run the three END_TREE instruments into a new `end_tree_crosscheck_1.out` -> `fill_gate50a.py` -> the controls both ways (update the head-specific patterns: `9e84e1fabafe`, counts) -> `--check` -> dry run. A develop move that does NOT reach the 4 paths is re-pinned by the launch action itself (step 3b).

## 9. The ONE launch command (run it after the routing line in section 4 is added)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate50a/repin_and_launch_gate50a.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-01_gate50a/launch_qa_secuura_batch1363.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/cb6b682a-5afd-4a5e-a1e3-be903cfa4469/scratchpad
```
- Append `--dry-run` for a dry run (rc 0 today, repin_dryrun_1.out). Argument 2 may be ANY existing Claude session scratchpad; if `g50a_sp/clone` is absent there, pin_gate50a.py rebuilds it on a re-pin.
- After the gate's verdict and a GO: Wednesday files the NEW ticket per the gate's POST ruling BEFORE the merge, and the GO / addendum names which MG-3 key set applies.
