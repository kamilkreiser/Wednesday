# DRAFTER REPORT: #1025 (KS-528, re-date of react-router rows 11 and 12) tier-2 gate set, 2026-09-17 19:23–19:39 AEST

**BLUF**
- **Files:**
  - brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1025-ks528-tier2.md` (sha256 `4ae73d60fb2d6bda…`, 22.1 KB)
  - prompt: `…/briefs/2026-09-17_secuura-1025-ks528-tier2.prompt.txt` (`00f029c5985c6583…`, 7.1 KB; #1021's was 7.2 KB)
  - launcher: `…/launchers/launch_qa_secuura_ks528_1025.sh` (`2aa672ca75e038ba…`), from `gen_launcher_1025.py` with the #1021 launcher as template: 26 asserted substitutions, 69 output controls, `#1025` enumerated at 12 first (`gen_launcher.enumerate-to-scratch.out`), residual guard clean, `bash -n` rc 0 (`gen_launcher.out`, 19:34:20). The first write (19:33:35) is kept as `launch_qa_secuura_ks528_1025.sh.pre-0917193420`. It was re-generated for one label fix: two JUDGED entries both printed as "package-lock.json", so the state line now prints the path.
- **`--check` rc 0** at 19:33:35 (`check.out`, first write) and **rc 0 at 19:38:53 on the final bytes** (`check_final.out`). Develop line: all 15 judged blobs `= base` | *origin develop still efaaa6034 (= the PR parent)*.
- **Negative controls, `--check` only (`controls_check.py` → `.out`, 19:34:41–19:38:32):** head override exit 6; prompt without the exact subject, without NOT-TESTED.written-first.md, and without MERGE ADDENDUM exit 23 each; prompt without MAIL exit 12; brief without the full SHA exit 20; brief without TIER 2 exit 7; a launcher COPY with the TTY guard removed (in the session scratchpad) exit 22. **8/8 as expected. No bare launch was run.**
- **Launcher, beyond #1021's guard family:**
  - **exit 22:** `--check` reads the launcher's own bytes and asserts the `[ -t 0 ] ||` refusal exists exactly once, before the `exec`. The TTY guard is proven without a launch.
  - **exit 23:** brief and prompt carry the exact verdict subject and report dir, and the prompt names NOT-TESTED.written-first.md and the MERGE ADDENDUM.
  - **JUDGED:** 15 blobs, every tracked file under `Blockchain/Dev/scripts/audit/` plus `Blockchain/Dev/package-lock.json`. The own baseline blob `e6f2184d2` gives exit 19 LANDED.
  - **GUARDED:** `Blockchain/Dev/scripts/audit/` and `Blockchain/Dev/package-lock.json` only, as commissioned.
- **Mail subject in prompt and brief:** `[QA -> Wednesday] TIER 2 GATE #1025 (KS-528) 9954a7069 — <GO | GO WITH FINDINGS | NO GO>`, FROM coagent@ TO wednesday-agent@ via the AgentMail API. Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks528-1025-9954a7069-tier2-r1/`.
- **Drafter's likely verdict: GO** (RECORDs only, no defect in the bytes).

## The six items: drafter predictions (raw runs in `out/`)

1. **Conservation: PASS** (`out/parse_probe.out`, from git blobs).
   - Rows 34 → 34, 0 added, 0 removed. Altered = exactly wrjc and 337j, each on `[expires, reason]`.
   - Row order, per-row field order and `$comment` are kept. Both prior reasons (249 chars) are exact prefixes of the new ones (873 chars).
   - **6/6 planted alterations flip the verdict.** Expires census 09-30: 5 → 3, 10-02: 0 → 2. `decidedAt` stays 2026-07-29.
   - Byte round-trip holds on both blobs.
2. **Expiry: PASS** (`out/islapsed_probe.out`: shipped `baseline-contract.mjs`, `Date` shim; freeze control 2030-01-01 took).
   - `isLapsed` = `expires <= utcToday()` (UTC date string).
   - Head: wrjc and 337j are live at every instant through **2026-10-01T23:59:59.999Z (02 Oct 09:59:59.999 AEST)** and LAPSED at **2026-10-02T00:00:00.000Z = 10:00 AEST**.
   - Controls: jjmj (and frvp) LAPSED from 2026-09-30T00:00Z; rgwj from 2026-09-24T00:00Z; on develop both target rows LAPSED from 2026-09-30T00:00Z. Malformed expires → true.
   - `date -j`: 2026-10-01 Thursday, 2026-10-02 Friday. UTC midnight 02 Oct = 10:00:00 AEST +1000. DST control: 05 Oct = 11:00 AEDT, so DST starts after the lapse.
3. **Gates: PASS** (`out/audit_runs.out` 19:27:24–19:27:55; `out/locks_reach.out` 19:28:28).
   - audit-gate rc 0, "33 distinct advisories reported, 34 baselined", 0 CLEANUP, identical for head/head, head/develop-baseline and develop/develop.
   - audit-locks rc 0 ×3, "43 standalone lockfiles … 1592 distinct packages pinned — 32 advisories match, 32 already baselined". The READY's "32/32" is confirmed.
   - `npm run audit:contract` `ℹ pass 59`, fail 0, on head and develop.
   - Red controls: head − wrjc → audit-gate rc 1 and audit-locks rc 1, exactly GHSA-wrjc NEW.
   - Through-gate clocks: head at 10-01T23:59:59.999Z gives rc 1 with LAPSED 9 and neither target (the rc comes from other rows, so the brief makes the LAPSED list the oracle). Head at 10-02T00:00Z gives LAPSED 11 including both "(expired 2026-10-02)", and audit-locks agrees. Develop at 10-01T23:59:59.999Z gives LAPSED 11 including both "(expired 2026-09-30)".
   - react-router 6.30.4 is in 4 tracked locks (root + 3 portals); control: express 30.
4. **Reason text: PASS on meaning, with two RECORDs** (`out/parse_probe.out`).
   - Present: KS-528, "RE-DATED 2026-09-17", `Kam ruled on 2026-09-17 18:31:25 AEST (decision secuura-audit-rows-react-router-v7-migration, relayed by Wednesday): "Commission the v7 migration AND date both rows to its planned landing (recommended)"`, landing 2026-10-01, lapse 2026-10-02T00:00Z (Fri 02 Oct 10:00 AEST), and "if it slips past 2026-10-01 the seat reports to Wednesday before then and does not re-date again on its own".
   - Absent: closing phrases, Peter/Stuart, credential-shaped strings.
5. **Linking: PASS** (`api_read.out` 19:28:48–19:29:06).
   - attachmentsForURL(pull/1025) = KS-528 contributes, open. Controls: pull/1021 → KS-1211 (merged); pull/99999 → 0.
   - KS-528 In Progress, `completedAt` null, history `09:21:22.262Z GitHub Backlog -> In Progress`.
   - 0 closing phrases in title, body, commit and the linear[bot] comment (planted controls). The body's KS-1201 is plain text, not an attachment.
6. **Merge: clean** (`out/setup.out`). `merge-tree --write-tree efaaa6034 9954a7069` = `23b56bac07faf84165882176e63436e1c470826e` = the head tree. Control: develop × develop = `38ea11907`. Open PRs: 21; **0 of the 20 others share a file, and 0 touch scripts/audit/**.

## Where the READY disagrees with what I measured
1. **"slip -> report, no second re-date"** is the READY's paraphrase. The literal string is not in the bytes, but both clauses are there in prose. Predicted RECORD. The brief tells the gate to test the meaning, so a literal grep does not produce a false NO GO.
2. **"Kam's ruling verbatim":** the reason quotes the panel LABEL including "(recommended)". This matches `answer_kam_rulings_1831.md`, the decision card and `kam_rulings_today.sh`. The option key `migrate-and-date` is not in the reason; it names the card id instead. My commission worded the ruling as "migrate-and-date — Commission … landing" (key + label, no suffix). That form was never meant to be a byte match. RECORD.
3. **Ruling second:** the reason and Wednesday's relay say 18:31:25, while Wednesday's decision store reads `ruled_ts 18:31:32.038`. Both are Wednesday's own instruments, 7 s apart. RECORD, target Wednesday. Nothing in the bytes depends on it.
4. **"0 of 19"** open-PR overlap is now 0 of 20 (#1026, KS-839, opened since). The population grew; this is not a slip.

## FOUND
- No defect in the bytes. Three RECORDs (above, 1–3).
- One launcher cosmetic defect in my own first write (ambiguous "package-lock.json" label), fixed by regeneration.

## TESTED
Everything under the six items, with the controls named there. Launcher `--check` twice and 8 negative `--check` controls.

## HOW (instruments and controls)
- **Clone:** `git clone --shared --no-checkout` of the Secuura checkout into `mktemp -d` `/private/tmp/claude-501/drafter1025.WYm0w5`, with detached worktrees `base` (efaaa6034) and `head` (9954a7069). Write verbs came only from `setup.sh`. `scripts/audit` `npm ci --ignore-scripts` rc 0 in each. Porcelain 0 on both worktrees at close.
- **Freeze:** `out/freeze_clock.mjs` freezes `Date` only when `process.argv[1]` is audit-gate/audit-locks, so the `npm audit` child is not frozen. Every frozen run prints its `[qa-freeze] … toISOString=` line as proof.
- **Credentials:** GH_TOKEN and LINEAR_API_KEY were read by NAME in `api_read.py` (adapted from #1021's by asserted substitutions) and never printed. Calls were GETs and GraphQL queries only.
- **Instrument fault, corrected in the open:**
  - The first `out/audit_runs.out` ran 6 of 10 gate runs, because `/bin/bash` 3.2 errors on an empty array under `set -u` ("unbound variable"; G1, G3, L1 and L3 never ran).
  - It is quarantined by rename (`audit_runs.out.bash32-unbound-quarantined`). The script was patched by an asserting edit and the whole set re-ran. Every number here comes from the re-run.
  - The brief carries the bash 3.2 warning for the gate.
- **Hooks:** a `cd` inside a heredoc was refused by the no-cd hook, so `locks_reach.py` uses `subprocess(cwd=)`. A panel-chat read was refused by the seat-scoped hook, so I used `tools/kam_rulings_today.sh`.
- **Secuura checkout, start 19:24:23 → close 19:38:57:** porcelain 0 → 0; `.git/config` sha256 `d7e7298b02c45f52` → same; refs 929 → 929; `.git/worktrees` 112 → 112. Origin head and develop are unchanged at both readings.

## NOT TESTED (the gate must, or must say it did not)
- Any run on a merged tree other than the head tree (develop had not moved; identity argued by tree OID).
- In-hook preflight whole (legs 3/4/8 need a stack; legs 2/5/6/7 were run as their commands, not through preflight.sh).
- Whether Wednesday's ANSWER was really sent at 08:59:16Z, as the reason says (`answer_rr7_date_ruled.send.out` carries no timestamp; file mtime 18:59 AEST agrees to the minute only).
- The react-router v7 migration, any portal, any browser or image (not commissioned).
- Whether the registry advisory feed changes between now and the gate's run.

## Decision for Wednesday
- **None blocking.** Two things to know before launch:
  1. My commission's item 4 asked for the literal "slip -> report, no second re-date". The bytes carry that meaning in prose, and the brief tells the gate to rule on meaning. If you want the literal string, that is a re-date instruction to Seat B, not a gate finding.
  2. The ruling time differs by 7 s between your relay (18:31:25) and your decision store (18:31:32.038). Nothing in the PR depends on it.
- **Re-run `--check` right before launching.** Exit 18 means develop moved into `scripts/audit/` or the root lock (e.g. PR-3 pushed and merged early). That calls for a re-pin, not a bypass.
