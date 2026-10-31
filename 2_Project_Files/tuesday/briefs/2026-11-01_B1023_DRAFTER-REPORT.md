STARTABLE: YES (once stamped; four Q-questions below each have a default that keeps it startable)

# B1023 drafter report: SEAT-G253, NexusAI RD-910 tier-2 gate of branch b1018/nexusai-rd910-null-roster-entry @ cc665c02

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1023_SEAT-G253_nexusai-rd910-gate-tier2.md`, 111 lines. Exact copy `.md.pre-stamp` (cmp equal, both sha256 `3d8ade1329807943b55b2b237fd6c470effb426bfa892c36ba350ff76554ee62`). Slot lines 8 (7 slots and the last line), `@X@` 0, non-ASCII 0. No person's name: a word-bounded grep for the owner's names reads 0 (control: 31 hits on TUESDAY/CLAUDE.md). No card id.
- Seat **G253**. G252 appears nowhere (0 in `tuesday/briefs`, 0 in the Datasec project Briefs; control G251 hits 5 and 3). B1022 has no file in `tuesday/briefs` yet. I left G252 for B1022's drafter and took G253 (Q-4).
- The subject is a BRANCH with no PR. One commit `cc665c02` on main `a4a227dc`, ahead 1, behind 0. It touches three paths: server.js +1 -0, the rd869 test file +28 -0, the counts file +2 -2. Main is unmoved since B1018 launched.
- **Would a merge deploy the demo? NO, but it would START a Deploy demo run.** The workflow triggers on `push: branches: [main]`. Its `paths-ignore` covers only `**.md`, `docs/**` and `tests/**`, so `backend/server.js` and `__tests__/` trigger it. Its `build` job (line 53) and `deploy` job (line 91) need `vars.CI_DEPLOY_ENABLED == 'true'`, and `deploy` is bound to `environment: demo` (line 95). As read at 06:44:
  - Repo variables 0. Organization variables visible to the repo 0. Environments `[dev]` only (no `demo`).
  - The last 5 Deploy demo runs were all push runs on main, and every `build` and `deploy` job was completed/skipped: 40971201513 (`8a812415`, the #143 merge, which touched server.js), 40870009819, 40845683861, 40834703288, 40802579782.
  - Positive control for the trigger rule: main `a4a227dc` (a HISTORY.md-only push) started no run.
  - The merge grant (EXPIRING-GRANTS.md line 30) says: "**NOT covered:** production, demo redeploys (a merge must not deploy -- check deploy-demo.yml each time), ...".
  - The kit makes a set variable or a `demo` environment a STOP, both at Step 0 and at C10.
- **New fact the B1018 seat did not have: the branch's only hosted check is RED.** `audit-production-deps` (npm-audit, push) failed at 2026-10-31T19:37:55Z.
  - Job 124637171427 lists moderate and high advisories in production dependencies, including follow-redirects high (GHSA-mrwp-f3q8-3g9p) and joi high (GHSA-4528-x5fx-h6hg).
  - `package.json` (`3908a828`) and `package-lock.json` (`050c1a2a`) are byte-equal at main and head.
  - Main's last npm-audit run (`a4a227dc`, 2026-10-30) was green.
  - So these advisories are against unchanged dependencies, not this branch's change. The kit grades this as a Note and carries it to Tuesday as a landing question (Q-3).
  - The ruleset's `required_status_checks` list is EMPTY, so the red does not block a merge mechanically. Earlier NexusAI landing preconditions did list `audit-production-deps` green.

## Facts re-measured (instrument; control)
- Pins (`git ls-remote` via the shared checkout's origin; `gh api -X GET` under the project GH_CONFIG_DIR, 06:40:38): main a4a227dc, branch cc665c02, `b1023*` and `b1022*` refs none. Open PRs 0 (control: `pulls/99999` 404).
- Blobs (raw GET + `git hash-object`):
  - server.js: head b673c3b4 (22411 lines), main dcaadacb (22410). `diff` gives exactly `8088a8089`, and the added line is byte-equal to the B1018 kit's line.
  - Test file: head e2b95919 (675 lines). Counts: head 7680a3ff = 5267/311.
  - Equal at main and head: build.yml e4e5c095, deploy-demo.yml 597b3487, verify-suite.sh eb9731f5.
  - Commit tree 84d2d04e. Main is the parent, so the merge tree must equal the head tree, and the kit asserts that.
- The patch: F2 has 8 expect lines, each with `// FAIL:`. The preload line returns the real rows followed by `[null, undefined]`.
- Head line numbers: read 8087, guard 8088, added line 8089, map 8094, return 8104. Route reuse 7275/7276/7283. Sibling 10185/10207 (main 10184/10206). `getAllPrinterLogs({ limit: 1000 })` appears on 12 lines.
- CI predicate (raw, at the head):
  - build.yml lines 3-9 trigger on `pull_request` to main and `push` to main only. The verify step is at lines 83-84.
  - verify-suite.sh: line 343 fails BELOW, line 354 fails ABOVE, line 366 prints `VERDICT: PASS`.
  - Check-runs on the head: total 1 (the npm-audit red). Main has 6, all green.
- Org ruleset 24139430 (`rules/branches/main`): deletion, non_fast_forward, code_scanning (errors / high_or_higher), required_status_checks [].
- Round count (first-line loop over 102 STATUS files): 35 verdicts. NO GO: B592, B647, B667, B906, B912, B926 (control: a scratch `GATE VERDICT x NO GO` line counts 1). The class grep hits only B927 (records) and B1018 (builder). No gate on `cc665c0`. So "0 of 2 before, round 1 of 2" stands, on a NEW class split out of B926-1.
- C-190 (CLARIFICATIONS.md): header 2062; item 2 at 2067 (merge commit, "Never squash, never rebase"); item 3 at 2068; the Analyze wait rule at 2073; the addendum at 2076; C-224 at 2412. The kit quotes items 2 and 3 without the header's name. No squash files: C-190 gives a merge commit, so the kit asks for `merge-subject.txt` / `merge-body.txt` with exactly one `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` trailer, asserted by program.
- Model: `levels.sonnet.model_id` claude-sonnet-5-5 at models_latest.json line 23. G2 is at model-routing.md line 109 and reads "follow-ups whose mechanism a prior gate already measured". G-cap is line 111.
- Lock tool: sha256 cf01bafb...971f (equal to B1018's stamp). Header read with `sed -n 1,40p` (FIFO, `--after`). `queue-jest/` was empty and no lock was held at 06:4x.
- B926 instruments for C5 (read-and-copy): shapeinject.js 1d2276f8 (47 lines, has the arrnull, arrundef and arrmixed shapes), shapedrv.js d8cabed6, classpred.js 808f52d2, shapes.sh 342ca53f (hard-codes `b926-$t` trees and `b926-gate-shape-*` tickets, so the kit has the gate change these by substitution only), r1-fence-quiet.js c16b65f9 (full hash matches B926's kit), b807 fence-preload.js 55eaafcb.
- Panes 06:43: Datasec/MPS-G251, Datasec/MPS-R105, fleet-monitor, tuesday. No NexusAI pane. The B1023 paths are absent (control: session-tools/b926 exists).
- Ports: none assigned. The harness bands ports from 39000 (test-server.js line 62 `BAND_BASE = 39000`). `lsof -iTCP:39000-39999 -sTCP:LISTEN` returned 0 lines (control: the unrestricted listing returned 14). load1 3.19 at 06:43.

## D-decisions
- **D1: added the builder's own null-holding shapes plus one mutant, MT.** MT drops `log !== null`, and `typeof null` is 'object', so it pins the other clause of the filter. MN pins only the `undefined` half.
- **D2: changed the reference for the `[{User_Name:'Admin'},null]` shape row.** It is the same boot's `[{User_Name:'Admin'}]` row, not the unarmed answer, because the cleaned list is a valid roster. B926's class predicate compared against the unarmed answer, and that is wrong for this shape.
- **D3: C2 runs red-first by copying the head's test file onto a main tree.** That gives the unmodified server.js. C3's MR also hashes to dcaadacb. So the red is proven twice, by two routes.
- **D4: the commit message's claim "every chat question that holds a name answered HTTP 500" goes to the gate to test.** It is tested against the C5 `show me admin's activity` rows. B926's table shows that question at 200 under null-holding shapes, so it is a likely overclaim, graded Minor (wording). I did not state my reading as a finding.
- **D5: no `npm audit` locally.** The lockfiles are blob-equal, so the outcome is equal by construction. The gate reads the hosted log and the GHSA pages by GET only.
- **D6: the B926 C6 engine census is NOT TESTED BY DESIGN** (optional if time allows), because the line is the identity on every list of objects, and C4 item 3 proves that.

## Q-questions for Tuesday (each with a default)
- **Q-1 Tier.** G2's O55 column says Opus is first "if the follow-up's mechanism sits on a G1 surface". `checkForCurrentUserQuery` was B926's tier-1 (data exposure) surface. **Default: Sonnet G2, as in Tuesday's B1018 Q-3 answer.** Reason: the change is availability-only, a filter that is the identity on every list of objects, and C4 item 3 proves that by element identity. The kit's Escalation hands any finding that changes WHICH user is shown to an Opus tier-1 gate.
- **Q-2 The builder's FINDINGS 1 token** in the commit message ("right after the existing check"). **Default: Note.** It is an ordinary English adverb used as a word, not a reference to anyone, and the seed is synthetic data. A rewrite would need a new branch and a new head. The gate prints the sentence either way.
- **Q-3 The npm-audit red at the head.** **Default: the gate grades it a Note (not this branch's; package files equal main) and Tuesday decides at landing.** The default recommendation: land, since the ruleset requires no status check and the red is the dependency set's, not the commit's, and file a separate dependency-upgrade ticket. If Tuesday wants a green npm-audit as a landing precondition, the landing waits for that ticket.
- **Q-4 Seat number.** G253, with G252 left for B1022's drafter. **Default: keep G253 even if B1022 takes no G-number.** A gap is harmless, and a renumber after stamping would break the pane-name REFUSE check.

## UNMEASURED
- RD-910's live Jira state (RELAYED from B1018: To Do, 0 comments). I did not load the Jira helper. The gate's C9 reads it.
- The GHSA publish dates (the gate reads them by GET if it can).
- The hosted Build, Gitleaks and CodeQL on a PR that does not exist.
- Whether B1022's drafter takes G252.
- Main's exact open-alert count (the `alerts?state=open` page cap of 100 was hit).

## Outside-the-fences disclosure
- **Write method.** I wrote the kit and this report with the Write tool. The `.pre-stamp` copy was made with `cp -p` and then `cmp`, because an exact copy was asked for. That is a Bash write of a third file, and the commission named it.
- **Builder's tree.** One `/usr/bin/grep -n` read of `worktrees/b1018-rd910-null-roster-entry/__tests__/helpers/test-server.js` (in the builder's tree) to confirm the 39000 band line. It was read-only, nothing was written, and the kit forbids the gate that tree. An `ls` of `session-tools/b1018/` and its lock directory was also read-only.
- **Hosted reads.** All `gh` calls were `-X GET` under the NexusAI GH_CONFIG_DIR, including one job-log GET. No HTTP to any hosted, demo or production host. No Jira call. No decision-queue call. No az, ssh or docker.
- **Scratch.** Files were written only in my session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2aa17213-e9fb-4717-99d9-8efe0dc321ab/scratchpad/b1023/`: raw blobs, the commit object, run lists, the audit log).
