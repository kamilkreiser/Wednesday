## WEDNESDAY'S SEND AMENDMENT (2026-10-07, brief read WHOLE by Wednesday before send; it SUPERSEDES the lines it names)
1. **Q-TARGET: RULED, the LOWEST clearing version** (shell-quote 1.11.0, @modelcontextprotocol/sdk 1.31.0, pbkdf2 3.1.7): the smallest delta inside Kam's "in-range" ruling. Latest-in-range is not wanted this round.
2. **Q-METHOD: ruled from YOUR measurement, in the ANSWER to your plan mail.** Measure both paths in ITEM 0 (d) and propose one with its collateral. The card's words name a "containerised per-dir regen"; Docker was down at draft. A host-node-24 regen in a scratch copy, or the surgical editor, is a technical choice inside the same ruling as long as the committed result is field-for-field identical to the planned entry set with 0 collateral (cross-checked by the other path). Wednesday rules it and discloses the method to Kam. **Do not start Docker Desktop.**
3. **Q-TESTS: WIDENED.** Beyond the five `npm ci --ignore-scripts` runs and mcp-server's build + unit suite: also `services/anchoring` build + unit suite and `packages/shared` unit suite (pbkdf2 is a prod dependency in both locks), and `frontend/issuer` `npm run build` (whether pbkdf2 reaches the served `dist` is a question your ITEM 0 (c) answers). Anything not run goes in Test Evidence as NOT run, with why.
4. **Q-TKT: RULED.** ONE ticket, board account (the same assignee as KS-1425, the 2026-09-06 rule: new Platform K tickets go to our account), priority Urgent, project "Dependency and Version Currency". Filed only after the ANSWER and after the duplicate search reads 0 (name the search terms and the control that proves the search returns hits).
5. **Q-WT, Q-PF: confirmed as written.**
6. **CORRECTION to the partition table:** R 5th's watcher pid 22699 is NOT armed; Wednesday stopped it 2026-10-07 05:16 (identity by command line). There is no live R seat. **Live at send:** %0 wednesday, %1 monitor, **%73 Seat D 14th** (demo deploy, never yours).
7. Kam's tap is 06:46:01 on the live board; the card store records the reconcile at 06:47:10. One ruling.

LAUNCH BRIEF (Seat G 3rd): pane `Secuura/Blockchain-G`. You have ONE job: **unfreeze the repo's pre-push gate, again.** Preflight legs 6 (npm-audit, KS-470) and 7 (standalone-lock advisories, KS-531) FAIL on develop `b39051390ff6` for three newly published advisories. You do an **in-range, lock-only refresh** of shell-quote, @modelcontextprotocol/sdk and pbkdf2, you **measure whether each reaches a runtime image**, and you raise ONE PR on ONE new ticket. You stop at ONE READY for a T1 (security) QA gate. That PR merges FIRST, before #1404, #1398 and PRs 3-5 can push. **No baseline row this round.** Secuura NEVER force-pushes.

# LAUNCH BRIEF: Seat G 3rd, Secuura/Blockchain, pane `Secuura/Blockchain-G`. DEPENDENCY seat: lock refresh ONLY. From Wednesday

## 🔴 READ FIRST
- **The refusal, WHOLE:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatR5_ctx_preB5.txt` (106 lines, P1). Seat R 5th's push of #1404's merge-in was refused `PREFLIGHT FAILED on leg(s) 6 7 - fix the above before pushing. (12/15 legs ran)` (`:21`). Its legs, verbatim (`:33`-`:51`):
  - leg 6: `audit-gate: 12 distinct advisories reported, 24 baselined.` / `FAIL — 3 NEW advisories not in the baseline:` GHSA-6qxp-vccf-f47h [high] @modelcontextprotocol/sdk; GHSA-477h-4r7f-fvrx [moderate] pbkdf2; GHSA-pqg4-j6r4-53mv [critical] shell-quote.
  - leg 7: `audit-locks: 43 standalone lockfiles, 1613 distinct packages pinned — 9 advisories match, 7 already baselined.` / `FAIL — 2 advisories`: `@modelcontextprotocol/sdk, pinned 1.29.0, in 1 lock: services/mcp-server`; `pbkdf2, pinned 3.1.6, in 3 locks: frontend/issuer, packages/shared, services/anchoring`. The hint: `bump the pin (containerised per-dir regen), or a reasoned baseline entry`.
  - R 5th proved it is develop's red four ways (`:56`-`:67`): D..M is #1404's four paths only; 0 lock/manifest/baseline paths; baseline blob `4af041e8d74a` equal at D and M; the three names 0 times in the diff. Wednesday ACCEPTED it (P14).
- **The precedent round, which is your method:** Seat D 10th, KS-1425, #1397, squashed as `add9a3b8bec3` by Seat D 11th (P10). Read, read-only:
  - its brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_seatD10_advisory_lock_refresh.md` (METHOD `:178`-`:193`, HOLDS `:241`-`:259`);
  - its ITEM 0 `…/briefs_staged/2026-10-06_seatD10_ITEM0.txt` and WRAP `…/2026-10-06_seatD10_WRAP.txt`;
  - its handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatD10-2026-10-06.md` (87 lines), above all §FINDINGS 1-10 and D1/D2;
  - Seat D 11th's WRAP `…/briefs_staged/2026-10-06_seatD11_WRAP.txt` (the merge path).
- **Your lane's kit and its traps:** Seat G 2nd's handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatG2-2026-10-06.md` (121 lines). §3 "WHAT TO CHECK FIRST IN GENERATION `g3`" is addressed to YOU. Kit: `5_Project_History/2026-10-06_seatG-2nd/raise/` (49 entries, generation `*g1`, P11).

## BLUF
**Ruling:** Kam's card `secuura-advisory-freeze-3-ghsa-1007` is ruled **(a)** (see RULED BY KAM). This brief exists for that ruling.

**What's broken.** origin `develop` = **`b39051390ff6f252601d6f7b45f0ea6c21c31023`** ("Merge pull request #1405", tree `780e919fea30`), by `ls-remote` at 2026-10-06T19:48:49Z (= 06:48 AEDT 10-07, P3). At that develop, second-hand (P4-P6):

| Advisory | Sev | Lock (leg) | Pinned | dev? | Vulnerable (bulk API) | Lowest clearing | Parent's declared range | In range? |
|---|---|---|---|---|---|---|---|---|
| GHSA-pqg4-j6r4-53mv shell-quote | **critical** | `Blockchain/Dev` root (leg 6) **only** | 1.9.0 | dev | `>=1.8.4 <1.11.0` | 1.11.0 (latest 1.12.0) | `concurrently@8.2.2` `^1.8.1` | **YES** |
| GHSA-6qxp-vccf-f47h @modelcontextprotocol/sdk | **high** | root (leg 6) + `services/mcp-server` (leg 7) | 1.29.0 | prod | `>=1.12.0 <1.31.0` | 1.31.0 (latest 1.32.1) | **DIRECT**: `services/mcp-server/package.json:18` `^1.27.0` | **YES** |
| GHSA-477h-4r7f-fvrx pbkdf2 | moderate | root **3.1.5** (leg 6); `frontend/issuer`, `packages/shared`, `services/anchoring` 3.1.6 (leg 7) | 3.1.5 / 3.1.6 | prod | `<=3.1.6` | 3.1.7 (= latest, 2026-09-29) | `@cardano-sdk/crypto` `^3.1.3`; `crypto-browserify` `^3.1.2`; `parse-asn1` `^3.1.5`; `@cardano-sdk/key-management` `^3.1.3` | **YES** |

- Bulk-API control (P5): the three lowest-clearing versions together return `{}`; the pinned versions all fire.
- `Blockchain/Dev/mobile/secuura-app/package-lock.json` pins shell-quote **1.8.3**. It is **OUT OF SCOPE** (`OUT_OF_SCOPE_LOCKS`, `lock-discovery.mjs:193`, expires 2027-01-01). **Do not touch it.**
- **0** baseline rows name any of the three (baseline blob `4af041e8d74a`, 24 rows, P8).

**The change set, predicted (yours to re-measure): 5 locks, 7 entries, 0 manifests, 0 baseline, 0 source.**
- root: shell-quote, sdk, pbkdf2;
- `services/mcp-server`: sdk;
- `frontend/issuer`, `packages/shared`, `services/anchoring`: pbkdf2.

**🔴 THIS ROUND BREAKS D 10th's "THREE FIELDS PER ENTRY" (P6).**
- sdk 1.29.0 -> 1.31.0 changes its own `dependencies["@hono/node-server"]` from `^1.19.9` to `^1.19.9 || ^2.0.5`. The pinned `@hono/node-server` 1.19.17 satisfies both ranges.
- pbkdf2 3.1.5 -> 3.1.7 (root only) changes `dependencies["to-buffer"]` from `^1.2.1` to `^1.2.2`. Root pins to-buffer 1.2.2.
- pbkdf2 3.1.6 -> 3.1.7 and shell-quote 1.9.0 -> 1.11.0 leave every lock-relevant field equal.
- Root entries carry **no** `resolved`/`integrity` (D 10th's D1). So root changes `version` (+ `dependencies` where above) only.
- D 10th's editor `applylocksd10.py` writes `version`/`resolved`/`integrity` ONLY (`:70`). As it stands, it would leave two `dependencies` ranges stale.

**Order:**
1. ITEM 0 (read-only). It ends in the plan-confirmation QUESTION; STOP for the ANSWER.
2. ITEM 1: file the ticket, create the worktree.
3. ITEM 2: build and prove.
4. ITEM 3: commit, push, open the PR.
5. ITEM 4: ONE READY.
6. WRAP.

You do NOT merge on this brief. The merge happens only on the GO below.

**Budget, by MAIL HANDSHAKE.** You cannot read your own context. Mail `QUESTION: ctx read (Seat G 3rd)` and HOLD for Wednesday's pane reading at these points: before ITEM 2's first lock edit, before the push, after the PR is raised, and before the merge if a GO reaches you.
- Never START a build past 45%.
- Never START a push past 50%.
- WRAP COLD at ~55%, naming every built commit (sha, tree, trailer proof) as UNPUSHED unless pushed.
- Never estimate ctx. Never end a turn on a "next up" line with nothing running.

**IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO.** If ITEM 0 contradicts any row above, the measurement wins: HOLD that row and mail.

**WAKE:** your re-seated `inbox_watchg1.sh` (`SINCE` required), armed in the background at boot. It EXITS on every FOR-ME match. RE-ARM IN THE SAME ACTION THAT READS THE MAIL. `SINCE` is the newest mail you have READ, never a wall clock (STANDING_LINES `:399`).

RULED BY KAM
- **Standing direction to bump rather than accept**: cards `secuura-four-advisories-ruled-after-measurement` (bump, 2026-09-09) and `secuura-five-new-advisories-block-every-push-0929` (a), both cited in KS-749's merged body (`fe6daca34`). Plus `secuura-five-new-advisories-freeze-every-push-1006` = (a), which is yesterday's precedent (P10).
- **Ticket creation, one ticket per TEST PASS** (Kam 2026-09-07 13:23, STANDING_LINES `:86`-`:93`). This is ONE pass, so ONE ticket.
- **Kam 2026-10-06 19:30:43, verbatim:** *"No one else is sharing this seat, so you can use up to 100%, but do it as the recommendation above with Spark on all tickets and one or maybe two deployers."* (daily `2026-10-06.md:317`, P15).
  - You are launched with `WED_USAGE_STOP=100` under that grant's EXPIRING-GRANTS row; the override gates the launch tool only. Report your own reading; do not set it.
  - The grant lifts Wednesday's usage stop. **It does not loosen your ctx lines.**
  - Card (a) below names this as "one build seat beyond your 19:30 card-(a) shape", so the tap covers you.
  - Necessity of a Claude seat: a Spark cannot raise a PR, re-prove legs 6/7 in-hook, or file a ticket.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Live board 2026-10-07 06:46:01 AEDT view=wednesday: "Decision secuura-advisory-freeze-3-ghsa-1007: a — Fix the dependencies: one Claude seat does an in-range lock refresh"
- Card option (a) text: "A dedicated seat bumps the three packages within range in the affected locks (containerised per-dir regen), measures whether each reaches a runtime image, then raises ONE PR gated T1 and merged first. #1404, #1398 and PRs 3-5 then push."
- That ruling **must land in YOUR PR body and your ticket** (the authority line), verbatim.
- The board record reads `ruled_choice "a"`, `ruled_ts 2026-10-07T06:47:10.502745+11:00` (`0_Brain/dashboard/data/decisions.json:27583`ff, P2). That is the recording time. Kam's tap is 06:46:01.

RULED BY WEDNESDAY FOR THIS ROUND
- **No baseline row.** Option (b) was NOT chosen. `audit-baseline.json` stays byte-identical (blob `4af041e8d74a`). No row is added, re-dated or removed. The 15 stale CLEANUP rows leg 6 prints stay out (disposition KS-767), named in the PR's NOT-DONE list.
- **No range change.** If ANY of the three needs a major bump, an `overrides` entry or a `package.json` edit to clear, **STOP and mail.** That is not an in-range refresh.
  - 🔴 sdk is a DIRECT dependency of mcp-server. `npm install @modelcontextprotocol/sdk@<v>` REWRITES `package.json`, so it counts as a manifest edit. Any npm verb you use must leave every manifest byte-identical, asserted by blob.
- **`mobile/secuura-app` is out of scope.** Never touch it, `OUT_OF_SCOPE_LOCKS`, `baseline-contract.mjs` or `expected-case-count` (59 at `b3905`).

## THE PARTITION AND THE LOCK
| Seat | Pane | Lock | Never yours |
|---|---|---|---|
| **G 3rd (you)** | `Secuura/Blockchain-G` | `.push-lock-g1`, `LOCK_SEAT='Secuura/Blockchain-G g3'` | — your new branch + new worktree + the 5 locks only |
| **D 14th** (deploys develop `d75bfe2deb80` to the DEMO box, concurrently) | `Secuura/Blockchain-D` | its own | **`deploy-clones/`, `local-deploy/`, the demo box, any build clone** |
| R lane (#1404 M, #1398, PRs 3-5; R 5th WRAPPED, its watcher STOPPED by Wednesday 05:16, see amendment 6) | `Secuura/Blockchain-R` | `.push-lock-d8` (`lockra1.sh:217`) | **worktree `s-ra4-ks1436` (holds UNPUSHED M `7849f0a23d06` for #1404: never read-write, never remove)**, `s-ra3-ks1136` (#1398), every `ra*` branch |
| G 1st's merged worktree | — | — | `s-g1-ks1330`: removal was PROPOSED by G 2nd §5, not ruled. Leave it |

- `d75bfe2deb80` is an ancestor of `b3905` (P3). D 14th's deploy does not depend on your PR, and your PR does not depend on it.
- **At draft (19:53Z):** 0 `.push-lock-*` in `worktrees/`.
  - G kit: `lockg1.sh:212` takes `.push-lock-g1`; its WAIT set is `-56`, `-e4`, `-f3`, `-d8` (`:279`-`:282`).
  - R kit: `lockra1.sh:303` WAITs on `-g1`. So R and G wait on each other, which is correct.
  - Re-measure both halves at ITEM 0, and extract the WAIT set from BOTH `lockg1.sh` and `pushg1.sh` and assert parity, with `-g1` absent from both (STANDING_LINES `:414`).
- **Attribute every lock by its holder file's `seat` field, never by path** (`:408`). A `.push-lock-g1` whose `seat` is not `Secuura/Blockchain-G g3` is a STOP-and-mail.
- Hold the lock short: never across `npm ci`, a gate run or a suite. Never pipe a lock take.
- **Your PR moves develop for everyone.** On merge, #1404's M `7849f0a23d06` is VOID (Wednesday's 18:07:45Z ANSWER rule 3, P14), and R 6th re-predicts. That is Wednesday's relay, not yours.
- **Re-seat (G 2nd §3, §4):**
  - generation stays `*g1`; seat tokens `g2`->`g3`, `2nd`->`3rd`, by hand with a receipt;
  - `rekey_checkg1.py` keys on a TWO-DIGIT generation, so there is **no independent auditor**. Say so (§3.9);
  - `armsg1.py:65` and `mergeg1.py:120` default `SCRATCH` into a DEAD session. Re-point both to YOURS (§3.3);
  - matcher: `MINE = "g 3rd"`. Add `g 2nd`, `g 4th`, `r 5th`, `r 6th`, `d 13th`, `d 14th` to `OTHER_SEATS`. Keep an untagged arm with an addressee in NEITHER list (`(Seat G 9th)`, §3.4). Prove 9 of 9 must-fire controls fire. A real `GO (Seat G 2nd): …` subject must read FOREIGN (`:400`);
  - STALE KNOBS: list every module-level knob with its value before any run; grep literals for 36-char UUIDs and `/private/tmp/`; AST-parse every Python tool.

## ITEM 0 — plan confirmation (QUESTION `plan confirmation (Seat G 3rd)`). STOP until Wednesday's ANSWER.
Before the ANSWER, do NONE of these: lock take, fetch into the shared store, worktree add, ref write, `npm` write into any tracked tree, ticket write, comment, PR. You MAY write in your record folder and in YOUR `git clone --shared --no-checkout` scratch clone.

ITEM 0 carries:
- **Refs by `ls-remote`, instrument and time named:** develop, `refs/pull/{1398,1404}/head`. At draft: `b39051390ff6` / `9414aa54e92c` / `c117c0160684` (P3).
  - **If develop moved, re-measure every row above on the new develop**, and mail any new advisory or lock.
  - `b3905` is in the shared store (`cat-file -t` = commit), so no fetch is needed unless develop moved. If it did, fetch BY SHA from `git@github.com:Secuura/Distributed_Secuura.git` into YOUR scratch clone, `--no-tags --no-write-fetch-head`, with `-c core.sshCommand=` taken from the checkout. **Never export `GIT_SSH_COMMAND`.**
- **(a) Lock census.** For every tracked lock (45 at draft) and each of the three packages, give:
  - path, pinned version, `dev`/`devOptional`;
  - every parent whose dependency resolves to that path (nearest-`node_modules` walk) with its declared range;
  - in range: yes/no for the target version, by `semver.satisfies` with a must-pass and a must-fail control.
  - At draft: 8 entries over 6 locks, mobile included (P4).
- **(b) Fixed version per advisory, instrument named.** Use leg 7's own instrument: `POST https://registry.npmjs.org/-/npm/v1/security/advisories/bulk` (`audit-locks.mjs:101`). Leg 6 is `npm audit --json` at the workspace root (`audit-gate.mjs:10`, `:126`). Give:
  - the `vulnerable_versions` range and the GHSA url per id;
  - control A: the targets alone return `{}`;
  - control B: the pinned versions fire;
  - registry metadata for the target version: tarball URL, `dist.integrity`, and its lock-relevant fields diffed against the old version (`dependencies`, `peerDependencies`, `peerDependenciesMeta`, `engines`, `license`, `funding`, `bin`, `os`, `cpu`).
- **(c) 🔴 RUNTIME REACH. UNMEASURED; this is ITEM 0's job.** For each package and each lock, does it reach a runtime image? Use `git show <develop>:<Dockerfile>` reads only. **No `docker build`.** Give:
  - which Dockerfile stage copies which `package*.json` / `package-lock.json`;
  - whether that stage runs `npm ci --omit=dev`;
  - whether the stage's `node_modules` (or a `COPY --from=` of it, e.g. `shared-builder` `/shared`) lands in the final stage;
  - for frontends, whether the package is in the served `dist` (an import-graph read; say UNMEASURED if you cannot settle it without a build).
  - **Drafter's leads, not measurements:**
    - `services/mcp-server/Dockerfile:45`, `:56`-`:57` runs `npm ci --ignore-scripts --omit=dev` from mcp-server's own lock in the final stage, and sdk is non-dev there;
    - `services/anchoring/Dockerfile:35`, `:38`-`:39` does the same, and pbkdf2 is non-dev there;
    - both copy `/shared` from a `shared-builder` that ran a full `npm ci` (`mcp-server:59`, `anchoring:41`);
    - `frontend/issuer`'s final stage is nginx serving `dist`;
    - no Dockerfile COPYs the `Blockchain/Dev` root `package*.json` (8 `COPY --from=builder` hits, 0 root);
    - so shell-quote (root, dev, plus out-of-scope mobile) may reach no image;
    - mcp-server imports only `@modelcontextprotocol/sdk/server/mcp.js` and `server/stdio.js` (6 import lines). GHSA-6qxp is about the OAuth CLIENT.
  - Quote each finding at `file:line`.
- **(d) Method proposal (Q-METHOD) with measured collateral.** Docker was DOWN at draft (`docker info` rc 1, P13), so the card's "containerised per-dir regen" cannot run as written. Measure `docker info` again and state which path you propose:
  - **(i) Surgical**, the precedent: extend a copy of `applylocksd10.py` under your own name. It is data-driven by a plan file generated from (a)+(b). It writes the measured field set per entry, which now includes `dependencies` where (b) shows it moves. It refuses anything else.
  - **(ii) Regen**, per lock directory in a SCRATCH copy, with `--no-workspaces` (B 55th §13.2: in a member, npm writes the ROOT lock without it). Host node 24 or `node:24-alpine` (§6e LTS).
  - Whichever you build with, cross-check the other in scratch and prove the result **field-for-field identical** on each planned entry, with 0 collateral entries. Precedents:
    - `npm update … --package-lock-only` produced 13 collateral dev-flag flips (B 56th §3a);
    - host npm 11.5.1 was INERT for it on the root lock (B-successor1 `:22`).
- **(e) Base control.** In your scratch clone at `b3905` (`npm ci --ignore-scripts` in `scripts/audit` only), run:
  - `node scripts/audit/audit-gate.mjs`;
  - `node scripts/audit/audit-locks.mjs` (from `Blockchain/Dev`; preflight `:420`, `:461`).
  - Quote the counts. Expected per P1: leg 6 `12 … 24 baselined … 3 NEW`; leg 7 `43 … 1613 … 9 match, 7 … 2`.
- **Toolchain and disk:** `node -v`, `npm -v` (v24.7.0 / 11.5.1 at draft), `docker info`, `df -m /Volumes/DevMASTER` (697,786 MiB free at 19:52Z).
- **Project rules, quoted from develop with blob ids:**
  - `.claude/skills/secuura-test-discipline/SKILL.md` (blob `b59b74a592e9…`, P9) is the ONLY skill under `.claude/skills/` at `b3905`. Its MUSTs that touch a lockfile change:
    - **§1** (`:13`-`:28`): a written plan grounded against ticket, reviewer comments, `.md` files and code, before any edit. Your ITEM 0 IS that plan.
    - **§5d** (`:507`-`:516`): every changed line carries a WHY + ticket comment; the ticket URL goes in PR summaries; a CVE / dep-drift finding goes to the matching project register. JSON locks cannot carry comments, so the WHY goes in the commit body and the PR (KS-1425 precedent). Say so.
    - **§5e** (`:518`-`:538`): no branches, merges, MD files or tickets "unless explicitly instructed". Branch and ticket ARE instructed here, on the ANSWER. No `.env` read or staged.
    - **§5f** (`:540`-`:552`): a runtime-behaviour change does not go to Done on offline green. sdk is a prod dependency of a shipped service. Report numbers, not adjectives, and name what is unverified.
    - **§6e** (`:645`-`:659`): LTS only. Node 24 / `node:24-alpine` for any regen.
  - repo `CLAUDE.md` (blob `ff426ce6097d…`):
    - `:330`-`:352` the register rule (KS-485 / KS-493 H dependency stream);
    - `:355`-`:384` the preflight rule ("baseline entries need a reason + ticket");
    - leg 6 audits the HOISTED root tree; leg 7 reads each standalone lock;
    - `npm audit` inside a member does NOT read that member's lock.
- **Linear, read-only** (key from the project's `4_Credentials/.env`, sourced transiently, never printed):
  - `searchIssues(term, first:20, includeArchived:true)` over the three package names, the three full GHSA ids, short ids `pqg4`/`6qxp`/`477h`, "advisory freeze" and "lock refresh";
  - a census of KS issues created since 2026-10-06T00:00Z;
  - KS-1425 and KS-1426 state.
  - **If a ticket for these advisories exists, STOP; never file a duplicate.**
- **The ticket draft** (filed only on the ANSWER): title, body (every sentence measured or "unmeasured"; Kam's ruling verbatim; cross-references KS-470, KS-531, KS-1425 hyphenated), project, priority. Board account. Precedent: KS-1425 = Urgent, "Dependency and Version Currency", assigned `kamil.kreiser@secuura.ai` by Wednesday's ruling.
- **Also:** watchers from a ps FILE; your watcher pid; your pane id from `$TMUX_PANE` and `tmux display-message -t "$TMUX_PANE" -p '#{@cockpit_name}'` (never the bare form, STANDING_LINES `:394`); every launcher preflight warning VERBATIM; `WED_USAGE_STOP` as read; "Please read my ctx". **Refuse the launcher's step-1 pull** on the shared checkout and say so.
- **QUESTIONS.** Each pre-ruled answer stands unless your measurement contradicts it:
  - **Q-TARGET (PROPOSED):** the LOWEST version that clears per control A: shell-quote 1.11.0, sdk 1.31.0, pbkdf2 3.1.7. That is the smallest delta. If you propose latest-in-range (1.12.0 / 1.32.1), give its measured field diff.
  - **Q-METHOD:** (d) above. Wednesday rules.
  - **Q-WT: yes.** ONE worktree `worktrees/s-g3-advlock`, ONE branch `feature/ks-<new>-advisory-lock-refresh-g3-1`, from `b3905` (or the develop the ANSWER names), via `wtaddg1`-class tooling under the lock. Run namecheck on both names (D 10th finding 1: substring collisions).
  - **Q-PF (PROPOSED):** accept the in-hook `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` with legs 3/4/8 stack-skipped (R 5th's push showed exactly those three skipped, P1 `:22`). Legs 2, 5, 6 and 7 must RUN and pass. A `FAILED` anywhere is a STOP. The same ratio with `FAILED` is a refusal: never read the ratio alone.
  - **Q-TESTS (PROPOSED):** `npm ci --ignore-scripts` from each of the 5 committed locks (rc 0, lock byte-unchanged). Plus mcp-server `npm run build` and its unit suite in its own dir against the committed lock, because sdk is a direct runtime dependency and that compiles the code against 1.31.0. Every other service suite, the frontend build and any live sweep go in Test Evidence as **NOT run**. The T1 gate decides what more is owed.
  - **Q-TKT:** confirm the ticket draft, project and priority.

## METHOD (precedent traps, carried; P10)
1. **The legs read different locks.** Leg 6 = the `Blockchain/Dev` workspace root via `npm audit` (shell-quote is ONLY there). Leg 7 = the 43 standalone locks (root and mobile excluded). A fix that clears leg 7 can leave leg 6 red. Prove both.
2. **Per-dir regen writes the ROOT lock unless `--no-workspaces`** (B 55th §13.2; `lockfile-cleanroom.sh:80`-`:87` calls it load-bearing). Never run npm against a tracked tree outside the plan. Regen only in scratch, and copy back only planned entries.
3. **Integrity from the tarball, not the clean-room.** `npm ci --dry-run` returns rc 0 on a bogus integrity (B 56th). Download each target tarball once into your scratchpad, compute sha512, and cross-check `dist.integrity`. Use the OLD version's tarball as a firing negative control.
4. **Semantic differ AND line differ.** Per lock, the JSON diff must be exactly the planned (entry, field) set: 0 added, 0 removed, 0 other. Key order must equal base; no `libc`/`os`/`cpu` array lost.
5. **Indent is per file** (D 10th D2: `Blockchain/Dev` locks indent 2, systemTest indent 4). Detect it, and require a byte-for-byte round-trip before any edit. None of your 5 locks is under systemTest at draft; assert it.
6. **The baseline is not touched.** Assert blob `4af041e8d74a` before and after. `audit:contract` must still report 59 cases.

## QUEUE (after the ANSWER)
1. **ITEM 1: ticket and worktree.**
   - Re-run the Linear search. File the ONE ticket, then read it back. ⚠ The Linear GitHub integration moves a ticket's state on PR link (D 10th disclosure). Report it; do not "fix" it.
   - Under the lock: worktree add, then release.
   - Outside the lock, in the worktree:
     - `npm ci --ignore-scripts` at `Blockchain/Dev` and in `scripts/audit` (KS-691);
     - `npm run build --workspace=packages/shared`, asserting `dist/index.js` (STANDING_LINES `:396`);
     - `npm ci --ignore-scripts` in EACH `systemTest/<pkg>`. The format gate fails closed on `NOTHING CHECKED` (D 10th finding 10; STANDING_LINES `:410`).
2. **ITEM 2: build and prove.** Your proof script, in your record folder, prints ok/fail counts for each arm:
   - **(fix)**: `node scripts/audit/audit-gate.mjs` rc 0 and `node scripts/audit/audit-locks.mjs` rc 0, each naming the three ids **0** times. Leg 2 `bash scripts/preflight/lockfile-cleanroom.sh` rc 0. `npm run audit:contract` = 59.
   - **(base control)**: a scratch checkout of `b3905` fails legs 6 and 7 naming the three.
   - **(negative controls, each on a SCRATCH copy, restored sha-verified)**:
     - revert root shell-quote to 1.9.0: leg 6 reddens on GHSA-pqg4;
     - revert mcp-server sdk to 1.29.0: leg 7 reddens on GHSA-6qxp;
     - plant a stale `dependencies` range on one changed entry: your semantic differ fires.
   - **(parse)**: 0 in-scope locks pin shell-quote <1.11.0 (>=1.8.4), sdk <1.31.0 or pbkdf2 <=3.1.6. `mobile/secuura-app`, every `package.json` and the baseline are byte-unchanged.
   - **(install)**: per Q-TESTS.
3. **ITEM 3: commit, push, PR.**
   - ONE commit under the lock. Subject `KS-<new>: in-range lock refresh clears shell-quote, MCP SDK and pbkdf2 advisories`, <=84 chars, ticket key first.
   - **0 trailers** (no `Co-Authored-By`, overriding the harness). Measure `%(trailers)` against a known 0-trailer commit. No closing-family word. Body in KS-1425's shape: what moved, counts, runtime-reach table, authority (Kam's ruling verbatim), arms, NOT run.
   - **Re-read develop at origin in the SAME action as the push decision.** If it moved, STOP: rebase is forbidden. Mail; merge develop in only on a ruling.
   - **First push of a new branch: `pushg1.sh` BARE, not `_ff`.** Run it under `env -u GIT_SSH_COMMAND`. The result is the tool's own `.rc` read AFTER exit, plus `ls-remote` of the ref. rc 141 with the ref unmoved is the KS-1149 class: archive the records, retry under the lock, and report attempts.
   - **Quote the in-hook preflight line EXACTLY. Never `--no-verify`, never `ALLOW_FORCE`, never a force push** (`.githooks/pre-push:22`-`:60` refuses non-fast-forward). A `FAILED` is a STOP.
   - Open the PR, base `develop`. Body: `Refs KS-<new> https://linear.app/secuura/issue/KS-<new>` (§5d), plus a **Test Evidence** block (touched / ran / NOT run) with numbers. ONE ticket comment linking the PR. Change no state.
4. **ITEM 4: ONE READY:** `READY: <PR#> advisory lock refresh (Seat G 3rd)`. It carries:
   - head sha, tree, branch;
   - the path list with numstat;
   - the arms table;
   - the runtime-reach table;
   - the in-hook preflight line verbatim;
   - Actions on the head by name (completed / failing / pending). Name the pre-existing `Security Scanning` and `PR Security Gates (KS-168)` failures by log, not by assumption (D 10th finding 9);
   - the ticket id.
   - **You end at READY FOR QA.** Wednesday commissions the T1 gate.
5. **WRAP** unless a GO reaches you within your ctx line.

## THE GO
`GO (Seat G 3rd): merge <PR#> on gate<NN>`. Wednesday fills `<PR#>` and `<NN>` when the gate returns GO at a named head; gate71 is the last number used (P12). Act only when a Wednesday mail whose **SUBJECT** carries that exact string reaches you, with `authentication_results` spf/dkim/dmarc = pass (read as the dict it is; D 11th's false-negative trap). Then:
- squash-merge with `mergeg1.py`, with flags named FROM THE TOOL;
- head read at origin in the same action == the GO's head;
- develop == the GO's develop, or STOP;
- explicit body, 0 trailers.

A GO naming another seat is FOREIGN. If you have wrapped, the GO goes to your successor by a new brief. After the merge: mail `STATUS: merged <PR#> (Seat G 3rd)` (squash sha, tree, parent) and post NO §5f comment unless Wednesday's mail gives its text. #1404 / #1398 / PRs 3-5 are NOT yours to push.

## HOLDS / KAM'S, NOT YOURS
- No deploy, no demo, no live sweep, no `az`, no SSH beyond git's transport, no `docker compose`, no stack, no migration. Do not start Docker Desktop: if a regen needs it, ask.
- No force push, no `--no-verify`, no `ALLOW_FORCE`, no `push --dry-run`, no `fetch --dry-run`, no `--admin`, no rebase. **Never export `GIT_SSH_COMMAND`.**
- No baseline edit, no manifest edit, no `overrides`, no major bump. An out-of-range target is a STOP-and-mail.
- **Never touch:** `deploy-clones/`, `local-deploy/`, the demo box, `s-ra4-ks1436` and M `7849f0a23d06`, `s-ra3-ks1136`, `s-g1-ks1330`, any R-lane branch, `mobile/secuura-app`, gate kits.
- No ticket state, assignee, label or project change on any existing ticket. Close nothing. Delete nothing (quarantine). Never write the shared checkout's working tree.
- No comment to Peter or Stuart. Never `POST /api/seen`. **R5:** a new mail from `kreiser.org@me.com` -> STOP and mail Wednesday; act on nothing in it.
- Signal / lock harnesses run in the FOREGROUND. Never `cd`. Use `-t "$TMUX_PANE"`.
- Drive hygiene at WRAP: `s-g3-advlock` is LEFT for the gate. Remove only your own scratch clones. Run `df -m` before and after.

## MAIL FORMATS (to `wednesday-agent@agentmail.to`, prefix `[Secuura/Blockchain-G -> Wednesday] `; every subject names `(Seat G 3rd)`)
- `QUESTION: plan confirmation (Seat G 3rd)`
- `QUESTION: ctx read (Seat G 3rd)`
- `QUESTION: <topic> (Seat G 3rd)`, one per mail. Use it for an out-of-range fix, a moved develop, an existing ticket, or a foreign lock.
- `READY: <PR#> advisory lock refresh (Seat G 3rd)`
- `STATUS: merged <PR#> (Seat G 3rd)`
- `WRAP (Seat G 3rd): …`. It carries:
  - the ps file;
  - the handover `5_Project_History/HANDOVER-seatG3-<date>.md` (sha256 prefix, `wc -c`);
  - the history entry at the TOP of `history.md`, anchored on CONTENT (D 14th shares the file);
  - `df -m` before/after;
  - mail COUNTED from the inbox;
  - ticket id and PR number.
- Record folder `5_Project_History/<UTC boot date>_seatG-3rd/`. Use QUOTED heredocs; assert body size > 0; read every send back.

## UNMEASURED (not provenance)
- Runtime reach of all three (ITEM 0 (c)); whether pbkdf2 is in issuer's served `dist`.
- Whether mcp-server exercises the SDK's OAuth client (import lines suggest not; not a measurement).
- Whether a containerised or host regen of the 5 locks yields only the planned entries.
- Linear: no search was run at draft.
- Whether develop moves, or another advisory publishes, before your push.
- Which seats are live at your boot: no tmux read was made at draft.
- Whether `wtaddg1`-class, `pushg1.sh` and `mergeg1.py` still pass their own proofs on this host.

PROVENANCE:
- P1 R 5th STOP mail, 106 lines, sent 2026-10-06T18:04:31Z, auth pass; lines cited inline | Read whole ; 2026-10-07 drafting | read 2026-10-07
- P2 Kam's ruling text as relayed by Wednesday's drafting order; card record `decisions.json:27583`ff (option a detail, `ruled_ts 2026-10-07T06:47:10.502745+11:00`) | `grep -n`, `sed -n 27575,27640p` ; 2026-10-06T19:5xZ | read 2026-10-07
- P3 `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1404/head refs/pull/1398/head`, rc 0, 2026-10-06T19:48:49Z-19:48:55Z, `GIT_SSH_COMMAND` count 0 → develop `b39051390ff6f252601d6f7b45f0ea6c21c31023`, /1404/ `c117c0160684d1ae72b2…`, /1398/ `9414aa54e92ca2435…`. `log -1`: tree `780e919fea30`, "Merge pull request #1405". `merge-base --is-ancestor`: d75bfe2deb80 rc 0, add9a3b8bec3 (KS-1425) rc 0 | drafter scratch `git clone --shared --no-checkout` | read 2026-10-07
- P4 lock census at `b3905`: 45 locks; 8 entries listed in the BLUF incl. mobile shell-quote 1.8.3 | `python3 -I census.py` over `git show b3905:<lock>`, drafter scratchpad `…/0e6aaa67-…/scratchpad/census.out` | read 2026-10-07
- P5 bulk advisory API HTTP 200 at 19:49:24Z (pinned versions fire: pqg4 `>=1.8.4 <1.11.0`, 6qxp `>=1.12.0 <1.31.0`, 477h `<=3.1.6`) and at 19:49:42Z (1.11.0, 1.12.0, sdk 1.31.0, pbkdf2 3.1.7 → `{}`). Registry metadata 19:49:33Z-19:49:41Z: latest shell-quote 1.12.0, sdk 1.32.1, pbkdf2 3.1.7; concurrently 8.2.2 `shell-quote ^1.8.1` | `curl -X POST …/advisories/bulk`, `curl https://registry.npmjs.org/<pkg>`, `python3 -I` | read 2026-10-07
- P6 field diffs old→target: sdk `dependencies["@hono/node-server"]` only; pbkdf2 3.1.5→3.1.7 `to-buffer` only; 3.1.6→3.1.7 and shell-quote equal. Root entry keys lack `resolved`/`integrity`; root to-buffer 1.2.2, @hono/node-server 1.19.17 | registry JSON + `git show b3905:<lock>`, `python3 -I` | read 2026-10-07
- P7 Dockerfiles: 38 tracked; `mcp-server/Dockerfile:10`, `:28`-`:29`, `:45`-`:59`; `anchoring/Dockerfile:8`-`:13`, `:35`-`:44`; `frontend/issuer/Dockerfile:11`-`:31`; root-`package*.json` COPY census 0 of 111 COPY-package lines. mcp-server imports `server/mcp.js` ×5, `server/stdio.js` ×1; 0 importers of shell-quote/pbkdf2 (control: express, 336 files) | `git show`, `git grep` at `b3905` | read 2026-10-07
- P8 baseline blob `4af041e8d74a`, 24 rows, 6 dated (all 2026-10-31), the three ids absent; `expected-case-count` 59 | `git show`, `python3 -I` | read 2026-10-07
- P9 blobs at `b3905`: SKILL `b59b74a592e9`, repo CLAUDE.md `ff426ce6097d`, preflight.sh `270b8913c009` (== D 10th's), lockfile-cleanroom.sh `518bffeeaf4a`; `.claude/skills/` holds 1 file; `.githooks/pre-push:22`-`:60` | `git ls-tree`, `git rev-parse`, `grep -n` | read 2026-10-07
- P10 D 10th brief (320 lines), ITEM 0 (322), WRAP, handover (87 lines); D 11th WRAP (91); `applylocksd10.py` 157 lines sha256/16 `64da21c09e6f8aa7`, `:70` three-field set | Read / `sed -n` / `shasum` | read 2026-10-07
- P11 G 2nd handover (121 lines) §3, §4, §5; kit `2026-10-06_seatG-2nd/raise/` 49 entries; `lockg1.sh:212`, `:279`-`:282`; `lockra1.sh:217`, `:303` | `ls`, `grep -n` | read 2026-10-07
- P12 history.md: G seats only G 1st (`:728`, 2026-10-05) and G 2nd (`:456`); 0 G seats in lines 1-400. Gatesets newest `2026-10-06_gate71`. `worktrees/` at 19:53Z: 0 `.push-lock-*`; `s-ra4-ks1436` HEAD `7849f0a23d06`; `s-ra3-ks1136` HEAD `9414aa54e92c`; `s-d10-advlock` absent | `grep -n`, `ls -a`, `git rev-parse HEAD` (read) | read 2026-10-07
- P13 `docker info` rc 1; node v24.7.0; npm 11.5.1; `df -m` 697,786 MiB free | 2026-10-06T19:52:34Z | read 2026-10-07
- P14 Wednesday's ANSWER to R 5th `…/briefs_staged/2026-10-07_seatR5_ANSWER_freeze_wrap.md` (rule 3: M VOID if develop moved) and R 5th WRAP (watcher pid 22699) | Read | read 2026-10-07
- P15 Kam 19:30:43 grant, `0_Brain/daily/2026-10-06.md:317` | `sed -n` | read 2026-10-07
- P16 STANDING_LINES `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` `:86`-`:93`, `:394`-`:420` (cited: `:394` identity, `:395` no force, `:396` packages/shared build, `:399` SINCE, `:400` trap-4, `:408` holder seat, `:410` format gate, `:414` WAIT parity) | `sed -n` | read 2026-10-07
- KS-1149 (rc 141 push class), KS-168 (the PR Security Gates workflow name), KS-691 (npm ci in scripts/audit): cited as TRAP LABELS carried from the precedent, not as work items in this round | D 10th brief + handover (P10) and STANDING_LINES (P16), not re-read on the board by Wednesday | read 2026-10-07
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 06:58
