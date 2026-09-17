# DRAFTER REPORT: #1020 (KS-769 fuse re-date) tier-2 gate set, 2026-09-17 15:42–16:01 AEST

**BLUF**
- **Files:**
  - brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1020-ks769-tier2.md`
  - prompt: `…/briefs/2026-09-17_secuura-1020-ks769-tier2.prompt.txt`
  - launcher: `…/launchers/launch_qa_secuura_ks769_1020.sh`, from `gatesets/2026-09-17_gate1020/gen_launcher_1020.py`. The template was the #1009 tier-2 launcher. The generator made 22 asserted substitutions and 59 output controls; `#1020` was enumerated at 9 first; the residual guard was clean; `bash -n` rc 0 (`gen_launcher.out`, 15:52:17).
- **Launcher `--check` (15:57:33, `check.out`): rc 0.** It was re-run at 16:00:46 on the final brief bytes (sha256 `a6779836f0eb95dc…`) and prompt (`2ee30e295c226dde…`) after two wording edits: rc 0, identical guard lines (`check_final.out`). Output of the first run, verbatim:

```
all guards pass:
  head on origin: #1020 71bd80a35b406b9c99c7b96955a7521032d33c20 at refs/heads/chore/audit-fuse-mobile-tree-dormant-redate
  compare (GitHub API): develop...#1020 = d7e95cd9f153e9036ed77935a73c93504fa6e3dc ahead=1 files=1
  lock-discovery.mjs 2f54840ce = base; lock-discovery.test.mjs f102d9d4c = base; baseline-contract.mjs 2504d9a28 = base; baseline-contract.test.mjs 2379c0aee = base; gate-exit-codes.test.mjs 40079f6fb = base; audit-locks.mjs aff23b042 = base; audit-gate.mjs 8e236ee70 = base; audit-baseline.json 03d1680e3 = base; expected-case-count 04f9fe460 = base; package.json d5977b6a1 = base; preflight.sh 28d3636c1 = base; package.json 769b7adbd = base | origin develop still d7e95cd9f153e9036ed77935a73c93504fa6e3dc (= the PR parent, the KS-1195 #1017 squash; git ls-remote)
  brief, prompt, QA project and repo all present
  brief and prompt agree on TIER 2 and ROUND 1
  prompt opens with the thinking directive and names the brief
  brief and prompt both name the head SHA
  prompt tells the agent to MAIL its verdict
  prompt forbids pushing / the real hook / preflight in the Secuura checkout
  prompt forbids memory maintenance inside the gate session
  prompt forbids printing a credential value
  a launch (not --check) will refuse unless stdin is a TTY (exit 21)
check rc 0
```

- **Negative controls, `--check` only (`controls_check.out`, 15:58:06):** each exits with its expected code.
  - head override: exit 6
  - prompt without MAIL: exit 12
  - brief without the full SHA: exit 20
  - brief without TIER 2: exit 7
  - prompt without the push/preflight ban: exit 11
- **The launcher's develop arm (new for this set):**
  - It judges 12 `scripts/audit` + preflight + Dev `package.json` blobs. `lock-discovery.mjs` at `3dd903b52` → exit 19 LANDED.
  - If develop moves, it refuses only on a delta under `Blockchain/Dev/scripts/audit/` (prefix), `preflight.sh`, the Dev `package.json` or `.githooks/pre-push`.
  - Lockfiles are deliberately not guarded: a bump changes which advisories report, and the gate re-measures that on the merged tree.
- **Mail subject in the prompt and brief:** `[QA -> Wednesday] TIER 2 GATE #1020 (KS-769) 71bd80a35 — <GO | GO WITH FINDINGS | NO GO>`. It is sent from coagent@ via the AgentMail API, as in the #1009 set.
- **Origin did not move:** ls-remote at 15:42:00 and 15:59:52 shows `refs/pull/1020/head` = `71bd80a35`, develop = `d7e95cd9f`.

**Wednesday's five questions: what the drafter measured (all in a `--shared` scratch clone; raw runs in `out/`)**
1. **Red-proof reproduces exactly** (`drafter_run.out` §C, counts via `reparse.out`).
   - base: lock-discovery 10/5/5, audit:contract 59/49/10, audit-locks rc 3 LAPSED.
   - head: 10/10/0, 59/59/0, audit-locks rc 0, 43 = 45 − 1 − 1.
   - Seat tampers T1–T5 match their predictions, all sha-restored.
   - Drafter's own tampers also match: T6 `'2026-10-18'` is green at today's clock (nothing today separates 10-18 from 10-19); T7 `'2026-10-18'` at 2026-10-18T00:00Z reds 5 with rc 3; T8, the head value at the same instant, keeps the fuse live (rc 1 from baseline rows, not rc 3).
2. **Date arithmetic, through the code.** `isLapsed` accepts `today` as an argument, so injection by argument works: 10-18 false, 10-19 true. `utcToday()` takes no parameter, so the drafter injected the clock at process level with `fakeclock.mjs` via `NODE_OPTIONS=--import`, with a 2020 control that changes `utcToday`.
   - At 2026-10-18T23:59:59.999Z (Mon 10:59:59 AEDT) the fuse is live: the unit probe passes, the whole lock-discovery suite is 10/0, and audit-locks is not rc 3.
   - At 2026-10-19T00:00:00.000Z (Mon 11:00 AEDT) it lapses: `validateOutOfScope` throws LAPSED, 5 cases red, audit-locks rc 3.
   - Intl and Python zoneinfo agree. **The lapse is 11 h after the end of Sunday 18 Oct Sydney time.** No date value can lapse at a Sydney midnight, so `'2026-10-19'` is the earliest value that keeps all of Sunday live. The brief carries this as a RECORD on wording ("the end of Sunday") for the gate to rule.
3. **Nothing else changed.**
   - 1 file, 1 commit. Plain, `-w` and `--ignore-blank-lines` numstat are all `5 1`.
   - The removed line is exactly the old literal. Of the 5 added lines, 4 are `//` comments and 1 is code.
   - A TypeScript comment-stripped transpile differs from base in exactly line 52 (the literal). Control: with the literal restored, the transpile is identical to base.
   - `audit-baseline.json`, `baseline-contract.mjs`, `expected-case-count` and `exceptions.yml` are byte-identical.
4. **Real `preflight.sh` in the drafter's clone** (`preflight_run.out`; closed loopback port):
   - **Leg 5 is OK (59 of 59 expected) at head and FAIL at base. Leg 7 is OK at head and FAIL (REFUSED, LAPSED) at base.** Leg 6 is OK on both.
   - Legs 3, 4 and 8 SKIP (no stack).
   - Both trees exit rc 1 for the same environment reasons: leg 1 DEPS MISSING, and leg 14 fails on `packages/shared is not built` plus `ks949_main_seed_idempotence.test.sh`. The fresh worktree has no Dev-root `npm ci`. This is identical on base and head. **Legs 1 and 14 are not measured green by the drafter.**
5. **Other fuses: a FINDING for the gate, not #1020's defect.** 15 `audit-baseline.json` rows lapse within 14 days.
   - **10 lapse at 2026-09-24T00:00Z = 10:00 AEST Thu 24 Sep** (KS-1024 ×7, KS-763 ×3). Measured with a 1 ms-before control: audit-gate rc 1 with 9 LAPSED, audit-locks rc 1 with 10 LAPSED. **So preflight legs 6 and 7 would refuse every Blockchain/Dev push from then**, and every push after it would need a waiver or a triage.
   - **5 more lapse at 2026-09-30T00:00Z** (KS-528 ×3, KS-530, KS-729): gate 14, locks 15.
   - audit:contract (leg 5) and lock-discovery stay green at 09-24.
   - No other dated `expires` sits under `Blockchain/Dev/scripts`.

**Where the READY disagrees with what I measured**
- Nothing measured disagrees. Two wording points go to the gate as predicted RECORDs:
  1. "End of Sunday" vs the 11:00 AEDT Monday lapse.
  2. The card's "your reason on KS-769" vs the unchanged `reason` field. The ruling itself is recorded on KS-769 in comment `bb69813e`.

**Also read**
- Linear: `attachmentsForURL(pull/1020)` returns KS-769 `contributes` (open); control pull/99999 returns 0; KS-769 is In Progress with `completedAt` null.
- 0 closing phrases in body, title, commit or comment (planted controls hit, and `Refs KS-769` does not).
- 0 files shared with the 19 other open PRs; none touches `scripts/audit/`, preflight or the pre-push hook.

**HOLDs I came near**
- **TAP parse.** The first parse in `drafter_run.py` used TAP `# tests` and read `?`: Node 24 prints the spec reporter when stdout is not a TTY. I did not re-run anything. I re-parsed the saved outputs with `reparse.py` (`ℹ tests/pass/fail`), and the brief and prompt carry the lesson.
- **Unverified cause.** I first wrote a reason for leg 5 staying green at 09-24 that I had not verified. I replaced it with the measured fact plus a labelled READ-ONLY guess.
- **Unused seed file.** An unused seed copy of the #1009 API script was quarantined by rename (`api_read.py.gen.quarantined-unused`), never deleted.
- **Clean boundaries:**
  - Launcher run with `--check` only (plus the 5 negative controls, all `--check`).
  - Write verbs only inside `scratchpad/gate1020_draft_vpwflmo3`.
  - No rm, no cd, no mail, no commit, no push, no credential echoed.
- **Secuura checkout readings:** 15:45:37 porcelain 0, config sha `d7e7298b02c45f52`, refs 918, worktrees 111. At 15:59:52 all four are identical.

**NOT measured**
- Legs 1 and 14 green (no Dev-root workspace install in the drafter's clone).
- The drafter did not explain why audit:contract ignores the lapsed baseline rows.
- A run under a non-Sydney TZ; the machine independence of `utcToday` is READ.
- Fuses outside `Blockchain/Dev/scripts` (CI workflows, other trees).
- Any develop newer than `d7e95cd9f` (a merged tree equals head today).
- `mergeable_state: unstable` on the PR (not investigated).
