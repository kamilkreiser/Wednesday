# DRAFTER REPORT — seatDep advisory lock refresh (3 GHSA), 2026-10-07

Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-07_seatDep_advisory_lock_refresh_3ghsa.md` (280 lines; 252 non-empty. Slightly over the ~250 target because of the runtime-reach leads and the provenance block).

## What I verified and how (all read-only on `!CODING`; writes only to my scratchpad and these two files)
- **develop** = `b39051390ff6f252601d6f7b45f0ea6c21c31023`.
  - Instrument: `git -C …/2_Project_Files ls-remote origin refs/heads/develop refs/pull/1404/head refs/pull/1398/head`, rc 0, 2026-10-06T19:48:49Z–19:48:55Z (= 06:48 AEDT 10-07). `GIT_SSH_COMMAND` was unset.
  - /1404/ = `c117c0160684`; /1398/ = `9414aa54e92c`.
  - `d75bfe2deb80` (D 14th's deploy target) and `add9a3b8bec3` (KS-1425) are both ancestors of develop.
- **Lock census at develop.** Instrument: `git clone --shared --no-checkout` in my scratchpad, then `python3 -I` over `git show b3905:<lock>` for all 45 locks.
  - shell-quote is ONLY in the root workspace lock (1.9.0, dev, under `concurrently@8.2.2 ^1.8.1`) and in the out-of-scope mobile lock (1.8.3).
  - The sdk is 1.29.0 in root + `services/mcp-server`. It is a DIRECT dependency there (`package.json:18 ^1.27.0`).
  - pbkdf2 is 3.1.5 in root and 3.1.6 in issuer/shared/anchoring. All non-dev.
- **Fixed versions.** Instrument: the registry bulk advisory API, which is leg 7's own (`audit-locks.mjs:101`). Leg 6 uses `npm audit --json`.
  - Vulnerable ranges: pqg4 `>=1.8.4 <1.11.0`, 6qxp `>=1.12.0 <1.31.0`, 477h `<=3.1.6`.
  - Control: shell-quote 1.11.0/1.12.0, sdk 1.31.0 and pbkdf2 3.1.7 together return `{}`.
  - **All three have an in-range fix.**
- **Field diffs (new finding).** sdk 1.29→1.31 changes its `dependencies["@hono/node-server"]` range. pbkdf2 3.1.5→3.1.7 (root only) changes the `to-buffer` range. So D 10th's three-field editor (`applylocksd10.py:70`) would leave two ranges stale. The brief flags this as the round's main trap.
- **Toolchain.** `docker info` rc 1, which means Docker is DOWN. node v24.7.0, npm 11.5.1. 697,786 MiB free.
- **Project rules.** `.claude/skills/` at develop holds ONE skill: secuura-test-discipline, blob `b59b74a592e9`. It changed since the precedent's `eaf43dfd`, and its §5e is now "CLAUDE.md diff audit", which contains the "no branches/tickets unless instructed" line. MUSTs are cited at §1/§5d/§5e/§5f/§6e line ranges.
- **Seat identity.** Only G 1st (`history.md:728`) and G 2nd (`:456`) have ever existed, and the first 400 lines show 0 G seats. G 2nd's handover §3 is literally headed "WHAT TO CHECK FIRST IN GENERATION `g3`". **I recommend `Secuura/Blockchain-G`, Seat G 3rd, with no conflict.** The G kit lock `.push-lock-g1` is distinct from the R lane's `.push-lock-d8`, and each lane's tools WAIT on the other's.
- **Floor at 19:53Z.** 0 push-locks. `s-ra4-ks1436` HEAD = `7849f0a23d06`. `s-ra3-ks1136` HEAD = /1398/ head. `s-d10-advlock` is gone.
- **Every STANDING_LINES citation was re-checked by `grep -n`.** I corrected 5 line numbers from my first draft.

## Contradictions with the card text / STOP mail
1. **"containerised per-dir regen" cannot run as carded.** Docker is down. The precedent shipped a surgical edit anyway. The brief makes the method a Q-METHOD for you to rule, with a field-for-field cross-check either way. It also tells the seat not to start Docker without asking.
2. **"in the affected locks" understates the set.** The STOP mail's lock list comes from leg 7 only. The root lock (leg 6) also pins all three packages, and it is the ONLY in-scope home of shell-quote. Predicted change set: 5 locks, 7 entries.
3. **The card's "pbkdf2 3.1.6" is only the leg-7 locks.** Root pins 3.1.5.
4. **The mail calls this the "transitive" class, but the sdk is a direct dependency.** That is still in range. However, `npm install sdk@x` rewrites `package.json`, so the brief names it as a manifest-edit STOP.
5. **Ruling time.** Kam's tap is 06:46:01. `decisions.json` records `ruled_ts 06:47:10.502745+11:00`, which is the recording time. Both are stated.
6. **The card's option-(a) detail has one more sentence than the text I was given verbatim:** "Costs one build seat beyond your 19:30 card-(a) shape … usage is 95%, under this seat's 100% line." The brief quotes the text as given and cites that sentence only for authority.

## Open questions for Wednesday
- **Q-TARGET:** lowest clearing (1.11.0 / 1.31.0 / 3.1.7, which I proposed) or latest-in-range (1.12.0 / 1.32.1)?
- **Q-METHOD:** surgical with the `dependencies` field added, or regen in scratch with `--no-workspaces`? Rule it once ITEM 0 has measured the collateral.
- **Q-TESTS:** I proposed adding the mcp-server build and unit suite, because the sdk is a direct runtime dependency. Does T1 want anchoring/shared suites too?
- **Ticket placement:** a new ticket (one test pass), project "Dependency and Version Currency" as with KS-1425. Assignee per your KS-1425 ruling, or unassigned?
- **G lane residue:** `s-g1-ks1330` removal is still unruled (G 2nd §5). The brief tells G 3rd to leave it.
- **Not run by me:** a Linear search, a tmux floor read (forbidden), and any runtime-reach measurement beyond Dockerfile/import leads. All of these are marked UNMEASURED in the brief.

Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/0e6aaa67-f803-42db-8f5a-54406fea138e/scratchpad/` (`sc/` clone, `census.out`, `net/` registry JSON, `brief.bak`). Safe to remove.
