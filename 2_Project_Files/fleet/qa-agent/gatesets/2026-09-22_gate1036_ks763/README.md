# Gateset 2026-09-22_gate1036_ks763 — README for Wednesday (the drafter launched NOTHING, sent NOTHING, tapped NOTHING, posted NOTHING, wrote NOTHING under !CODING/)

ONE TIER 1 ROUND 1 gate (full weight) over Secuura/Blockchain PR #1036 — KS-763 PR-4, qs in range on express 4: 20 manifests `overrides.body-parser`
1.20.6 → 1.20.8, 29 regenerated locks (express 4.22.3 / body-parser 1.20.8 / qs 6.16.0 / side-channel 1.1.1), `scripts/audit/audit-baseline.json` 29 → 26
(GHSA-4mjr + GHSA-x5fp = KS-763, EXPIRING 2026-09-24; GHSA-q8mj = KS-531 / KS-775 on your 13:50:18Z ruling). Head `4b251997a96034ee8a3359aac357ee17d222c3ef`
(three commits; the second is a merge of develop 3961c2add). Produced in the shape of `gatesets/2026-09-17_gate1033/` (the same lock class; its report is the
prompt's method template) with the gate16B/16C file-set conventions. Everything below is read-only evidence or a file for YOU to run.

## 0. THE PINS (head strict; develop by CONTENT — it moves by design)
- Head `4b251997a…` = `refs/pull/1036/head` = `refs/heads/feature/ks-763-qs-in-range` at every read 07:42 → 08:12 (`lsremote_1.out`, `lsremote_final.out`, the
  fill / generator / `--check` outputs). The launcher refuses (exit 6) if it moves: a moved head is a different gate — re-draft.
- Develop `3916eacd12af23bfd464440b4c770f7da0f2dd96` at generation. The launcher does NOT pin develop's SHA: it judges the 49 non-audit PR paths + the 3 reach
  Dockerfiles + all 13 scripts/audit files by BLOB at the current develop (30 contents listings; `--check` ~25 s). develop moving on OTHER paths (the seats'
  test-only merges) is OK and printed; **the gate re-predicts the merged tree over the tip it reads and names it BASE_GO** in the addendum. A move ON a PR path
  (a Dependabot PR landing first — #949 #948 #947 #946 #945 #649 #639 #635 #575 #572 share paths) → exit 18 GUARDED; #1036 itself landing → exit 19.
  **If 18 fires:** read the refusal's unpinned paths, decide with the seat (a re-merge under the push-window lock), then re-pin: re-run
  `predict_merge_gate1036.py <scratchpad> <head> <new develop>` (a fresh `--shared` clone; it will report the conflict by path), edit the template's THE SHAPE
  bullets, `fill_prompt_gate1036.py`, `gen_launcher_gate1036.py`, `--check`.
- Merged tree over 3916eacd1 = `04b05e093ad8b3d6e55b0fe553d7deb96b247050` (0 conflicts, both orders; baseline 29 → 26 conserved; develop's 164-path delta
  touches none of the 50). GitHub's `refs/pull/1036/merge` is stale (over e2d0672af, 47 commits back; reproduced as a control) — not an input.

## 1. Read WHOLE before launching
- The prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-1036-ks763-qs-tier1.prompt.txt` (236 lines, 33925 B,
  sha256 `f88ae264d1577e81d78b045933d0014a0bb63d385a6f7a5359dc8e043f44f695`; first line `ultrathink`; no PENDING / deadbeef; the ELEVEN by-name items exactly as
  commissioned, each with its instrument and the drafter's measured prediction; the MERGE ADDENDUM shape verbatim with the 50 `path blob (mode)` targets on one
  line; the CONTEXT RULE; the CENSUS RULE v2 with :5432 (3 foreign LISTEN rows at 07:48 — never connect); Docker DOWN at 07:48 → the gate probes and says NOT
  TESTED for the image build if still down, runs the load trace on the host; the GO string `GO: merge #1036` naming the head + BASE_GO; the exact subject
  `[QA -> Wednesday] TIER 1 GATE #1036 (KS-763) 4b251997a — <GO | GO WITH FINDINGS | NO GO>`).
- The launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks763_1036.sh` (474 lines, mode 755, sha256
  `280817161f50aadac940d94cf3ec26a2d552853c8235881e5a48cb6854eeb8ab`) — exits 2..36 (19 = LANDED); BRIEF = the READY capture
  `gatesets/2026-09-18_gate1036/mail_1036_ready.md`; ladders: 93 by-name keywords, 46 BOTH tokens (READY AND prompt), all 50 head blobs.
- `DRAFTER_REPORT.md` — the drafter's slips FIRST (S1–S5), every value beside its command, the leads, what is NOT MEASURED.

## 2. The exact `--check` command (headless; run it yourself before the launch action)
    /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks763_1036.sh --check
  Drafter's run: `launcher_check_1.out` rc 0 at 08:00:52–08:01:16 AEST. Controls: `launcher_controls_gate1036.sh` (17 controls, ~9 min; `launcher_check_controls.out`
  + `launcher_check_controls_2.out` — 0 MISMATCH after the drafter's S3 correction): wrong sha → 6 · CUR_DEV=head → 19 · CUR_DEV=c9e034744 → 18 ·
  CUR_DEV=merge-base → 0 · CUR_DEV=#949's head → 18 · deadbeef → 34 · PENDING → 33 · no addendum → 25 · wrong target blob → 35 · no REACH FIRST → 27 ·
  by-name / CONTEXT / CENSUS miss → 30 · BOTH miss → 36 · no ultrathink → 8 · launch without TTY → 21.

## 3. The routing line — NOT WRITTEN BY THE DRAFTER: add it FIRST
  Append to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (backup beside, `$(date +%H%M)` stamp):
    QA/Secuura-1036|coagent@agentmail.to|yes
  `repin_and_launch_gate1036.sh` step 0 asserts it (rc 1 if absent; control: the batch1148 line's count = 1 at the drafter's read; the 1036 line's count = 0).

## 4. The exact launch command (the re-pin and the launch are ONE action — you run it, in a shell that can reach tmux; not the drafter)
    /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate1036_ks763/repin_and_launch_gate1036.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks763_1036.sh
  It reads its pins FROM THE LAUNCHER (no second copy; the sed dry-read is in the drafter's transcript: head 4b251997a…, develop 3916eacd1…, merged 04b05e093…,
  the branch, the prompt path): (0) asserts the routing line, refuses a PARTIAL / deadbeef prompt (rc 8); (1) `git ls-remote` develop + pull head + branch
  (READ, `lsremote_launch.out`); (2) re-reads the head from the PULLS API (`api_heads_launch.out`); (3) refuses rc 11 if the head moved or the PR is not open —
  develop moving is PRINTED, not refused (the launcher's content judgement decides); (4) `fleet/usage_gate.sh --check` (rc 12); (5) the launcher's own `--check`
  (rc 13, `launcher_check_launch.out`); (6) `cockpit.sh add QA/Secuura-1036 <launcher>` (rc 14, `cockpit_add.out`) + a pane census. `bash -n` rc 0; NOT RUN.
  Other gates (gate16B/16C) may be live on the same `.git`: each gate clones `--shared` into its own dir; independent.

## 5. What is in this directory
  COMMISSION.md — Wednesday's commission (07:40 AEST)
  read_shape_gate1036.py (+ `.pre-0744-twodot`, S1) / read_shape_1.out (S1) / read_shape_2.out — local object reads: commits, merge-base, the 50 paths NUL-safe (+ the
    wc -w control = 50), the raw records + the 50 equality targets, numstat, the baseline rows at dev/mb/head + the removed set + byte-equal re-derivation,
    scripts/audit 13 files, every tracked lock's family versions dev vs head, the 20 manifests' override diff, the 37 Dockerfiles' npm lines
  predict_merge_gate1036.py / predict_merge_1.out — THE ONLY WRITE VERBS, in a `--shared --no-checkout` scratch clone: merge-tree both orders, conservation,
    the deltas, count-objects before/after (identical); predict_merge_2_ghmergeref.out (S2) / predict_merge_3_ghmergeref.out (the GitHub merge ref fetched from the
    GitHub URL into the scratch clone) / predict_merge_ghcontrol_gate1036.py + predict_merge_4_ghcontrol.out (the instrument reproduces GitHub's tree)
  api_read_gate1036.py / api_read_1.out / out/gh/* / out/linear/* — GitHub + Linear reads (PR, files, commits, compare, open PRs + overlap, attachments, the two
    comment ids, KS-531, histories); closing-phrase regex with planted controls
  host_probe_1.out — node/npm/docker/load/:5432 at 07:48 · dockerfile_anchors_1.out — the runtime install lines + CMD/EXPOSE of the three reach Dockerfiles, the
    manifests' overrides, the root workspaces, lockfile-cleanroom's path, scripts/audit's package.json
  prompt_gate1036.TEMPLATE.txt (+ `.pre-0759-wraps`, S4) / fill_prompt_gate1036.py / fill_prompt_1..2.out — the template + the fill (pins re-read at origin, the
    merged tree recomputed in the scratch clone, the 50 targets from diff --raw; refuses on any residue)
  gen_launcher_gate1036.py / gen_launcher.run1..4.out — the generator (runs 1–3 refused: wrapped phrases, two self-control miscounts; run 4 wrote)
  launcher_check_1.out (rc 0) · launcher_controls_gate1036.sh (+ `.pre-0810-ladderorder`, S3) / launcher_check_controls.out / launcher_check_controls_2.out
  repin_and_launch_gate1036.sh — the launch action (NOT run)
  lsremote_1.out / lsremote_final.out / checkout_counts_before.txt / checkout_counts_after.txt — origin at 07:42 and 08:12; the checkout's counts (equal)
  DRAFTER_REPORT.md — slips first; every count with its command; NOT MEASURED

## 6. Leads for the gate (the gate grades them; full text in DRAFTER_REPORT.md)
  1 commit c9e034744's subject is 112 chars (> 92) — the squash subject is what lands · 2 `Refs KS-775` is absent from the body; the KS-775 link is by attachment
  · 3 GitHub's merge ref is 47 commits stale; mergeable_state "unknown" · 4 Docker DOWN at 07:48 → item 6(a) likely NOT TESTED; 6(b) on the host · 5 the READY's
  251 is unreproduced (wc -w = 50) · 6 develop's 29 rows: after this PR the next expiries are 2026-09-30 (GHSA-frvp KS-530, GHSA-jjmj KS-528, GHSA-mwp4 KS-729)
  and 2026-10-02 (GHSA-wrjc / GHSA-337j KS-528) · 7 3 foreign :5432 LISTEN rows on the host · 8 the whole-entry lock diff outside the family (3(e)) is the gate's.

## 7. What the drafter did NOT do
  No launch, no mail, no tap, no board write, no routing-conf write, no write into the Secuura checkout (ls-remote / show / diff / diff-tree / rev-parse / rev-list /
  merge-base / ls-tree / log / status / for-each-ref / count-objects / config --get only; every write verb in the scratch clone `predict1036.4e710_tb_c`, which was
  the only place a `fetch` ran — from the GitHub URL, into the scratch clone), no key printed, no port connected beyond `git ls-remote`, the scratch-clone fetch and
  the GitHub / Linear READ APIs; no Datasec file or mail. Nothing deleted anywhere.

## 8. Re-finishing from disk after any change (a cold successor)
  In order: (a) `python3 …/read_shape_gate1036.py <head> <develop> > read_shape_N.out`; (b) `python3 …/predict_merge_gate1036.py <scratchpad> <head> <develop>` (note
  the clone path it prints); (c) `python3 …/api_read_gate1036.py <head> <develop>`; (d) edit `prompt_gate1036.TEMPLATE.txt` if THE SHAPE changed (a moved develop:
  the merged tree, the delta counts, the GitHub merge-ref note); (e) `python3 …/fill_prompt_gate1036.py <clone> <head> <develop> <prompt path>`; (f) `python3
  …/gen_launcher_gate1036.py <launcher path> <head> <develop> <clone>`; (g) `<launcher> --check`; (h) `bash …/launcher_controls_gate1036.sh <launcher> <prompt>`
  (~9 min; "controls end … MISMATCH=0"); (i) read the prompt WHOLE; (j) section 3, then section 4.
