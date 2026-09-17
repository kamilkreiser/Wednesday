SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (Seat B)
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

BLUF
Boot is clean, and the brief holds at the tip.
- develop is f8c7aaa39.
- Exactly 15 rows: 10 expire 2026-09-24, 5 expire 2026-09-30. The GHSA set is the same as your table.
- Both controls reproduce your F1 numbers:
  - real baseline: gate rc 0, locks rc 0;
  - minus-15: gate rc 1 with 14 new, locks rc 1 with 15 (colord is locks-only).
Three questions need your call before step 1. Q1 gates the whole queue.

QUESTIONS (each carries my default)

Q1. Registry reads: the project rule at source forbids them unless explicitly instructed.
- 2_Project_Files/CLAUDE.md:164 at develop (AI Behaviour Rules > Scope discipline): "Do not fetch external URLs, changelogs, GitHub releases, or package registries unless the current message explicitly instructs it".
- Your brief is an explicit instruction. It relays Kam's 16:37:41 note, though; it is not his own message.
- The shipped gates already read the registry on every push: audit-gate.mjs:124-127 runs `npm audit --json`, and audit-locks.mjs:101 posts to the bulk advisory endpoint. I ran both, because your step 5 names them.
- Default, only on your ANSWER:
  (a) `npm view <pkg> versions` and `npm view <pkg>@<v> dependencies`, from the host, read-only;
  (b) `npm update <pkg> --package-lock-only` inside the bounded node:24-alpine containers;
  (c) `gh api /advisories/<GHSA>` (GitHub advisory DB, kksecura PAT) for severity and patched range, with the npm registry's severity as the cross-check.
  No changelog, release-note or other URL fetches.
- Question: are (a)-(c) authorised under this brief, or does this need Kam's own instruction?

Q2. The KS-769-excluded mobile lock carries two of these families, and the shipped gates cannot see it.
- I parsed all 45 tracked locks (control: 5 carry lodash). `Blockchain/Dev/mobile/secuura-app/package-lock.json` carries baseline-browser-mapping 2.9.14 and js-yaml 3.14.2 + 4.1.1, all non-dev.
- That lock is in OUT_OF_SCOPE_LOCKS until 2026-10-19 (Kam: dormant but kept). So "gone from every lock", as audit-gate + audit-locks measure it, excludes this one.
- Whether those three versions fall inside the GHSA-w5vr / GHSA-2883 ranges is UNMEASURED; it needs Q1.
- Default: no bump in the dormant tree. The fixability table and each affected PR body record the lock's presence by parse, and whether each version is in range, labelled "not scanned by the gate (KS-769)".
- Question: confirm, or should the dormant lock move in the same PRs?

Q3. Skill §6 (tool updates) and the vitest bump.
- secuura-test-discipline SKILL.md §6 covers "every test tool ... and anything added later": catalog diff, new result fields, HTML report, live run, register. None of that fits a package.json/lock-only write scope.
- Default: if the fix is an in-range patch or minor, treat the vitest / @vitest/mocker move as a dependency security bump, not a tool-capability update. Each PR body carries a §6 line: "0 new tests: vitest has no test catalog; runner patch only; §6b/§6c not applicable". That last claim is only written after a grep shows no harness report parses vitest output. If the fix needs a major, it becomes a per-row QUESTION anyway.
- Question: confirm, or does §6 bind in full?

DEFAULTS I apply unless you veto (no question)
- KS-1025 churn: the advisory set moves on an unchanged tree. Every removal is measured with the shipped scripts plus a real-baseline control, twice: at build and just before READY. It is measured again after any develop merge-in, and the timestamps are recorded. A new advisory in the same family mid-work comes to you as STATUS. I never add a row.
- §5d (WHY comment + ticket on every changed line): JSON cannot carry comments. The WHY lives in the commit message, the PR body and the ticket comment, as in #915.
- §4 (HTML docs move with a test change): a pin bump changes no test. Each PR body says so explicitly, per §4's own last rule.
- Severity: the npm registry data the shipped gate printed at 07:05Z reads ip-address HIGH, js-yaml HIGH, and every other row moderate (hono x3 and mysql2 included). That is one instrument. Step 1 re-measures from the advisory itself (Q1c) and names both.

MEANWHILE
Continuing read-only. No branch, lockfile, ticket or comment before your ANSWER.
- Per-row lock parses for declaring parents and their ranges (local files only, no registry).
- The open-PR overlap check on the locks and audit-baseline.json (GitHub PR files API: a repo read, not a registry).
- Copying the KS-1201 stub killer into my records with only WT changed. I read the diff; nothing runs until a push.

NEEDED-BY
Q1 gates step 1. The Sep-24 row QUESTIONs are due to you Mon 21 Sep 18:00 AEST.

DETAIL

Boot
- The preflight file stamp `# launch 2026-09-17T07:01:36Z` is my own launch (this session's ps lstart is 17:01:36 AEST). Warnings, verbatim:
[F-02] No SSH identity available for git (keychain not seeded, on-disk fallback off).
       Run: ssh-add --apple-use-keychain ~/.ssh/secuura_blockchain_deploy_rw
       Or temporarily: export SECUURA_ALLOW_ONDISK_KEY=1 before launching.
       (git will use whatever core.sshCommand is already in the repo config.)
[KS-907] 1 other live session(s) on this project: PID 52998 (up since Thu 17 Sep 15:20:50 2026).
         The boot git-sync is READ-ONLY this launch — it will NOT pull in 2_Project_Files.
- PID 52998 is Seat A (launched 15:20:50 AEST). F-02 needed no action: the repo's core.sshCommand key fetched rc 0.
- Shared checkout 2_Project_Files: feature/ks-597-b-caller-scoped-externalref, porcelain 0. Fetch only; not pulled or switched.
- v1.3 grant re-verified at source: <096604C5-237F-4467-9ECF-B79F975FCB11@me.com>. The raw Authentication-Results show spf=pass, envelope-from=kreiser.org@me.com, dkim=pass header.i=@me.com and dmarc=pass header.from=me.com; all 5 controls fail. Your brief's structured auth: spf/dkim/dmarc pass.
- Inbox isolation: own inbox 200, coagent@ 404, inbox count 1.
- Worktree `worktrees/raise-0917-b-audit`, detached at f8c7aaa39 (ls-remote matches your read), porcelain 0.
  - npm ci rc 0 (1937 packages, 19 s).
  - packages/shared build rc 0.
  - deps-present.sh rc 0 "OK"; the empty-tree control gives rc 1 "DEPS MISSING".
- Controls at 07:05Z (porcelain 0 before and after):
  - gate REAL rc 0: "36 distinct advisories reported, 38 baselined." / "OK"
  - locks REAL rc 0: "43 standalone lockfiles ..." / "OK"
  - gate MINUS-15 rc 1: 14 NEW (colord absent, locks-only)
  - locks MINUS-15 rc 1: 15
- Baseline at the tip: 38 rows (21 dated, 17 undated), sha256 6409a37c4dbd9ba8. The <=2026-09-30 filter selects 15. The same filter at <=09-23 selects 0, and at <=12-31 it selects 21.

Queue, re-derived at the tip (lock counts from the gate at 07:05Z, matching your table)
- Sep-24 rows:
  - qs x2 (28 locks) and mysql2 (originate): KS-763.
  - KS-1024: vitest/@vitest/mocker (26); baseline-browser-mapping (7); colord (2, systemTest, locks-only); js-yaml HIGH (4: governance, originate, referral, vc-issuer); hono x3 (mcp-server, originate).
- Sep-30 rows: react-router x2 + react-router-dom (3 frontends, KS-528); @hono/node-server (mcp-server, originate, KS-530); ip-address HIGH (frontend/issuer + root, KS-729).
- The parse also finds these families at OTHER versions (whether they are in range is Q1 work):
  - vitest 4.1.11 in systemTest/akto.
  - baseline-browser-mapping 2.11.14 in frontend/demo-overlay and services/vc-issuer; 2.10.29 in root; 2.9.14 in mobile.
  - js-yaml 3.14.2 + 4.1.1 in mobile; 4.3.2 + 5.4.1 in systemTest/akto and api-explorer; 5.2.3 in systemTest/performance.
  - ip-address 10.4.0 in root, packages/shared and anchoring; 10.7.0 in mcp-server.
- Plan, at most 3 of my PRs open:
  1. Fixability table, mailed as STATUS.
  2. File the KS-1024-rows ticket (search first).
  3. Sep-24 BUMP blocks, one PR at a time, in the order your ANSWER sets. Your starting grouping stands until the measurement says otherwise.
  4. Per-row QUESTIONs for majors, an override against a declared range, or a source change.
  5. Sep-30 blocks.
- Linear re-read:
  - KS-763 In Review.
  - KS-1024 Done, archived 2026-09-13T11:22Z.
  - KS-528 Backlog; KS-530 Backlog.
  - KS-729 In Progress; KS-775 In Progress.
  - KS-1025 Backlog; KS-768 Backlog.
  - Seat A's four comments are present: 1cf3d871, b8337268, 87d66048, c892a6e7.
- Board:
  - 74 active on the board account (87 team-wide).
  - Backlog 300 (U1 H75 M158 L61 N5).
  - Completed <24h: KS-1130, KS-810, KS-793. PS assigned: 0.
  - Extranet (hook read): 6 tasks / 0 replies / 1 doc, all pre-existing. /api/seen NOT called.

Reads done
- Project CLAUDE.md, and 2_Project_Files/CLAUDE.md at develop.
- secuura-test-discipline SKILL.md, the only skill: §1-§6 whole.
- Blockchain/Dev/CONTRIBUTING.md: PR process, merge flow, template, review requirements.
- history.md top entry.
- BACKLOG.md 975-1176, whole.
- HANDOVER-s164 §5.

Record vs brief: no disagreement.
- The fast-uri record's install moved members 1-6 only because the branch had added an `overrides` entry to their package.json. The root needed `npm update`.
- HANDOVER-s164: install does not bump a satisfied transitive.
- No row here has an override, so every attempt starts with `npm update <pkg> --package-lock-only`, verified by parse.
- Mounts: stated per member, with the parse deciding.

Records: 5_Project_History/2026-09-17_seatB-audit/

Seat B
