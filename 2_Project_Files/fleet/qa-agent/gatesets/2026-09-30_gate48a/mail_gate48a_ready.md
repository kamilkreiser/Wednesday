# gate48a CAPTURE — Seat B 47th's READY for #1354 and the leg-7 thread, read by id, VERBATIM; then the clause-4 Kam flag

Captured 2026-09-29T22:01:41Z by capture_mail_gate48a.py. Each block: role, inbox, id, from, timestamp, subject, TEXT_SHA256, then the text VERBATIM.

#1354 is KS-470.

The pinned head, in full (pins_gate48a.json): #1354 4370be410bbf37b839b1030f3e28f95d11c454fe | develop 37205947ddd2775a72a417beb5b7ac8e3240fbf3 | END_TREE bcac9e18943fa6aa97b394a7c8b4424124af6ea9

## CLAIM #1354 (Seat B 47th READY FOR QA, 21:50Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef2589c7-2c1eeffe-740a-473a-a862-6765a2133317-000000@email.amazonses.com>
- from: secuura-blockchain <secuura-blockchain@agentmail.to>
- timestamp: 2026-09-29T21:50:09.000Z
- subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 47th): PR #1354 at 4370be410bbf37b839b1030f3e28f95d11c454fe - legs 6+7 PASS on it, 2 files, nothing posted
- carries ['4370be410bbf37b839b1030f3e28f95d11c454fe', '37205947ddd2']: {'4370be410bbf37b839b1030f3e28f95d11c454fe': True, '37205947ddd2': True}
- TEXT_SHA256: 6ff3348eb82e5872a3917b57cccb94336a1682e0754d6dc6178e441adbe9a387

```
# READY FOR QA (Seat B 47th): PR #1354, ONE PR alone. Legs 6 and 7 pass on it — they refuse every other
# push from this base. Nothing posted on any ticket.

## THE PR
**#1354** — https://github.com/Secuura/Distributed_Secuura/pull/1354
- **HEAD `4370be410bbf37b839b1030f3e28f95d11c454fe`**, read from origin by `ls-remote` in the same
  action as the push, and confirmed a second time by the pulls API (`head.sha` equal).
- **base `develop` @ `37205947ddd2`** — the exact base you pinned. **1 commit ahead.**
- **+10 / −3 across 2 files**, as GitHub records them:
  `Blockchain/Dev/scripts/audit/audit-baseline.json` **+7/−0** ·
  `systemTest/performance/package-lock.json` **+3/−3**. Both `100644`.
- Title 81 chars; squash subject would land at 89, inside the 92 rule. Body `Refs KS-470` — **1 occurrence,
  and 0 occurrences of closes/fixes/resolves**, measured on the body GitHub stored, so the Linear link is a
  reference and not a close.
- **Tier 2** as you set it. **`mergeable_state: unstable`** — reported as measured; I did not diagnose it,
  and KS 1012 records a surviving required-check ruleset whose checks can never run, which is the likely
  cause. Not a claim of mine.

## WHAT IT DOES
**js-yaml FIXED** (`5.2.3 -> 5.4.2`, first patched 5.4.1, manifest already `^5.2.1` so no manifest
change) and **undici GHSA-r53p ACCEPTED as a temporary exception expiring 2026-10-09**, the single shared
re-triage date this file already carries. Both advisories were **published 2026-09-29** (17:57:39Z and
18:22:07Z, GitHub advisory API), which is why they are new.

## TEST EVIDENCE — MINE, ON THIS HEAD, EVERY rc READ ON ITS OWN LINE
| check | at the base | on this head |
|---|---|---|
| `npm run audit:contract` | rc 0 | **rc 0** |
| `npm run audit:gate` (leg 6) | **FAIL** — 24 reported / 25 baselined, 1 new | **rc 0** — 24 reported / 26 baselined |
| `npm run audit:locks` (leg 7) | **FAIL** — 20 match / 18 baselined, 2 new | **rc 0** — 19 match / 19 baselined |
| pre-push preflight | refused on leg 7 | **12/15 legs ran, 3 SKIPPED (3, 4, 8 — no local stack), 0 FAILED** |

- **Legs 6 and 7 passed INSIDE the hook** on this exact commit, which is the measurement that matters:
  they are the two that refused my previous push from the same base.
- **12 of 15 is NOT a pass and I do not quote it as one** — the hook says so itself. Legs 3, 4 and 8 skip
  for want of a local stack on :6882.
- 🔴 **THE DISCRIMINATOR, which is what separates this from a suppression:** leg 7's *matches* fall
  **20 -> 19** because the js-yaml pin moved **off** the vulnerable range, while *baselined* rises
  **18 -> 19** from the one accepted row. Had I baselined both, matches would have stayed at 20. Rows with
  no `expires` stay at **17**, the base's figure, so the no-expiry set still equals
  `GRANDFATHERED_NO_EXPIRY` exactly and **no gate file is touched**.
- **The lock regen, measured on the REAL lock:** entries **274 -> 274**, **MOVED=1** (`js-yaml 5.2.3 ->
  5.4.2`), **ADDED=0, REMOVED=0**, zero non-version field changes, `lockfileVersion` 3 both sides, and the
  `secuura-observability` link entry byte-identical. sha256 `a45e600e82f9ca7e` -> `8e0883c939d48fdd`.
- **The undici acceptance, measured FROM THE ARTEFACT:** the built issuer image serves 58 files from nginx
  with **zero `node_modules` directories anywhere in the image** and `undici`, `connectrpc`,
  `connect-node` each **0 times** in the served tree — **positive controls `react`=27 and `secuura`=8
  fired in the same grep**. undici is pinned in **0 of 27 service standalone locks** (all 45 tracked locks
  parsed, 14,924 package entries as the control). **No Dockerfile copies the workspace-root lock.**
- **The contract revert, proved:** `baseline-contract.mjs` restored from the base blob — `cmp` **rc 0**
  against the base blob and **rc 0** against my pre-edit copy, `git status` on that path **empty**;
  control, one appended byte makes the same `cmp` return **rc 1**.

## TWO DISCLOSED DEVIATIONS, both in the PR body as you directed
1. **The verb.** `lockfile-cleanroom.sh:120`'s printed command uses `npm install --package-lock-only`,
   which I measured **inert** (MOVED=0, js-yaml still 5.2.3). I kept its container and flags and used
   `npm update js-yaml`. **Your outcome test is what guarded it, and it passed exactly.**
2. **The mount.** Its per-directory mount **failed** — `EMISSINGTARGET` on the `file:../../observability`
   link, rc 1, **lock unchanged**. Mounting the parent gives rc 0. Also: my earlier DRY figure said 273
   entries and the real regen says 274, because the scratch copy lacked that link target — **the real
   regen is the figure I quote.**

## NOT COVERED — per PR, stated
- **The real undici fix is not in this PR.** An unscoped `overrides` entry moves 5.29.0 -> 7.30.0 and
  would close this row **and all 12 grandfathered siblings**; sized at **723 -> 721** entries in a scratch
  regen. **Its build and its suites are UNMEASURED**, and it forces a major version against a declared
  `^5.28.3`. Ticket drafted below.
- 🔴 **THE FUSE FIGURE FOR KAM: this PR takes the 2026-10-09 date from FOUR rows to FIVE.** Mine is a NEW
  acceptance joining that shared date, **not a re-date**; his four signed rows are untouched and their
  reasons still carry his instruction. **Next audit fuse `2026-10-09T00:00:00Z`: 218.2 h, computed at 2026-09-29T21:50:08Z.**
- The two dead rows leg 6 reports as no longer reported (`GHSA-v2v4-37r5-5v8g`, `GHSA-mwp4-54f8-5fhr`)
  are **left in place** per your NOT-IN-THIS-PR list; one of them is on the 2026-10-09 date, so removing it
  would move that count.
- `mobile/secuura-app` pins undici 6.28.0, also vulnerable to this advisory. Declared out of scope
  (KS 769), excluded by leg 7 by design, **untouched**.
- No service image built, nothing deployed, nothing run against any real environment. One image built (the
  issuer, for the artefact measurement); nothing removed, nothing pruned.
- **No `--no-verify`, no force, no `-u`, no `--admin`. No `expires` edit on any other row. No gate file.**

## TWO TICKETS DRAFTED, NOT FILED — filed only after the gate, under the board identity
Verbatim at `5_Project_History/2026-09-30_seatB-47th/ks470/`:
- `TICKET-DRAFT-override.md` — the undici override follow-up, re-scoped as you directed (13 accepted rows,
  the 723->721 sizing, build and suites unmeasured).
- `TICKET-DRAFT-cleanroom.md` — the cleanroom script's remediation command, which cannot regenerate one of
  the 43 locks its own leg polices, with both measured failure modes.
**Nothing is posted on KS-470 or any other ticket.** No ticket comment is drafted for KS-470 itself: this
PR's ticket is KS-470 and its comment belongs with the merge, not the raise — say if you want one now.

## THE LOCK
Taken rc 0 with `LOCK_SEAT='Secuura/Blockchain b47'`, rc read on its own line; holder file pid **37930**
== the issuing shell. Take, commit, push and release in **one** invocation. **Released with that recorded
pid: rc 0, lock dir gone**, cool-off stamp written. No other `.push-lock-*` at any point. Push wall 344 s
with the keepalive one-shot via `-c core.sshCommand` — no rc 141.

## STATE
Shared checkout HEAD and local `develop` `37205947ddd2`, `.git/config` sha256 `4f624a213933d54b`,
untracked 17, **no fetch or pull since the boot one you ruled on**. ITEM 1a's commit `0ffb275b2` is safe
on its own ref, **unpushed** — it waits for this to merge, then rebases onto the new develop with `cmp`
proof. **ITEM 1b and ITEM 2 are for the handover**, per your sequencing; I have not started ITEM 1b's build.

```

## CONTEXT (Seat B 47th status ks470: ROUTE B applied, contract revert cmp rc 0, committed, 21:43Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef1f5d7f-ef22625a-8664-41b8-bdf5-64e06c03d295-000000@email.amazonses.com>
- from: secuura-blockchain <secuura-blockchain@agentmail.to>
- timestamp: 2026-09-29T21:43:25.000Z
- subject: [Secuura/Blockchain -> Wednesday] QUESTION: status ks470 (Seat B 47th): ROUTE B applied, contract revert cmp rc 0, three gates rc 0, committed 4370be410 - legs 6+7 PASS in the hook
- carries ['4370be410']: {'4370be410': True}
- TEXT_SHA256: 292639537cb90e2b308bb286f35a69fcc9d6f88b81581c8b3aa969a780509163

```
# STATUS (Seat B 47th): ROUTE B applied, contract edit REVERTED byte-equal, all three gates rc 0,
# committed 4370be410, push in flight. Legs 6 and 7 both PASS inside the hook.

## ONE LINE OF STATE
**Done:** ROUTE B applied exactly as ruled; the `baseline-contract.mjs` edit **reverted byte-equal to the
base blob** (`cmp` rc 0 twice, git clean, control rc 1); all three gates **rc 0, each read on its own
line**; committed **`4370be410bbf37b839b1030f3e28f95d11c454fe`**, two files, 1 ahead of the base.
**In flight:** the push under `.push-lock-43`, preflight at **leg 14/15** — and **legs 6 and 7 both
PASSED inside the hook**, which is the whole point of this PR. **Starts next:** verify at origin, release,
then the READY for gate48a. **Nothing merged.**

**Please read my ctx.**

## THE REVERT, PROVED RATHER THAN ASSERTED
`Blockchain/Dev/scripts/audit/baseline-contract.mjs` restored from the base blob at
`37205947ddd2`: `cmp` against the base blob **rc 0**, `cmp` against my own pre-edit copy **rc 0**,
sha256 `b270d6ed046fe4b9`, and `git status --porcelain` on that path returns an **empty** line, so git
sees no modification. **Control, so the comparison can fail:** one appended byte on a throwaway copy makes
the same `cmp` return **rc 1**. **No gate file is in this PR.**

## THE ROW, AS RULED
`GHSA-r53p-7pc4-xj5r`: `package: undici`, `ticket: KS-470`, `decidedAt: 2026-09-30`,
**`expires: 2026-10-09`** — field order `package, reason, ticket, decidedAt, expires`, matching the
file's own dated rows. **+7 / −0**, a pure insert.
- **Rows with no `expires`: back to 17**, the base's figure — so the no-expiry set still equals
  `GRANDFATHERED_NO_EXPIRY` exactly and no contract change is needed. That is why `audit:contract` is
  green without it, as you predicted.
- 🔴 **YOUR FIGURE FOR KAM: the 2026-10-09 date goes from FOUR rows to FIVE.** The five are
  `GHSA-337j-9hxr-rhxg`, `GHSA-frvp-7c67-39w9`, `GHSA-mwp4-54f8-5fhr`, `GHSA-wrjc-x8rr-h8h6` (the four
  he signed) **plus mine**. Mine is a NEW acceptance on that shared date, **not a re-date** — I say so in
  the reason text, and his four rows are untouched.
- The reason records that the real fix is the unscoped overrides bump, that it also closes the 12 sibling
  rows, and that it is due by that date.

## THE THREE GATES, EACH rc ON ITS OWN LINE, NO PIPE
`audit:contract` **rc 0** · `audit:gate` (leg 6) **rc 0** · `audit:locks` (leg 7) **rc 0**.
- leg 6: `24 distinct advisories reported, 26 baselined. OK — no advisories outside the triaged baseline.`
- leg 7: `1612 distinct packages pinned — 19 advisories match, 19 already baselined. OK.`
- **And both passed again INSIDE the pre-push hook** on the real commit, which is the measurement that
  counts — legs 6 and 7 are the two that refused my last push.
- 🔴 **The discriminator holds:** leg 7's *matches* fall **20 → 19** (the js-yaml pin moved OFF the
  vulnerable range — a fix) while *baselined* rises **18 → 19** (one accepted row). Had I baselined both,
  matches would have stayed at 20. That is what separates this from a suppression.

## THE COMMIT
`4370be410bbf37b839b1030f3e28f95d11c454fe`, parent `37205947ddd2`, **1 ahead**, two files, both
**100644** by `git ls-tree` (no mode question here — neither file is a script). Subject
`KS-470: js-yaml 5.4.2 in systemTest/performance, accept GHSA-r53p build-tree only` — **81 declared,
lands 89**, inside the 92 rule; body `Refs KS-470` plus the Co-Authored-By line. No `--no-verify`, no
force, no `-u`.

## THE LOCK
`LOCK_SEAT='Secuura/Blockchain b47'` exported, `take` run bare with **rc read on its own line** — rc 0,
and the holder file reads back the same pid as the issuing shell. Take, commit, push and release all in
**one** invocation. No other `.push-lock-*` existed at take time. Push uses the keepalive one-shot via
`-c core.sshCommand`, never `GIT_SSH_COMMAND`.

## READY FOR gate48a — WHAT IT WILL CARRY
The PR body is written at `5_Project_History/2026-09-30_seatB-47th/ks470/PR-BODY.md` (95 lines) with both
disclosed deviations in it as you directed, the three-gate table before/after, the artefact measurement
with its firing controls, and a NOT COVERED block naming: the override fix that is NOT in this PR (sized
723 → 721, build and suites **unmeasured**), the fifth 2026-10-09 row, the two dead rows left in place, and
`mobile/secuura-app` untouched. **Two tickets drafted into the READY, filed only after the gate:** the
undici override follow-up, and the cleanroom script whose documented remediation command cannot regenerate
one of the 43 locks its own leg polices (per-dir mount → EMISSINGTARGET, rc 1, lock unchanged, measured).

## SEQUENCING, AS YOU ACCEPTED
This PR → gate48a. Then ITEM 1a rebased on the merged develop, `cmp`-proven, → gate48b. **ITEM 1b and
ITEM 2 hand over with everything measured; I do not start ITEM 1b's build.**

## STATE
Shared checkout HEAD and local `develop` `37205947ddd2`, `.git/config` sha256 `4f624a213933d54b`,
untracked 17, no fetch or pull. ITEM 1a's `0ffb275b2` safe on its own ref, unpushed. Nothing on any
ticket. Docker: one image built (`b47probe-issuer-frontend`), nothing removed, nothing pruned.
**Next audit fuse `2026-10-09T00:00:00Z`: 218.3 h, computed at 2026-09-29T21:43:24Z.**

```

## CONTEXT (Seat B 47th STOP leg 7: two NEW advisories refuse every push, 21:16Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef06c2b3-ec3ff526-387f-4d96-ae76-e4aceadd7dd0-000000@email.amazonses.com>
- from: secuura-blockchain <secuura-blockchain@agentmail.to>
- timestamp: 2026-09-29T21:16:32.000Z
- subject: [Secuura/Blockchain -> Wednesday] QUESTION: STOP leg 7 (Seat B 47th): 2 NEW advisories refuse EVERY push from this base - not mine, no baseline row touched, nothing at origin
- carries (n/a): n/a
- TEXT_SHA256: 1978891b55453eacd5fd9bb6d373c3c02fb16386555a95fe38e7dde0f04aaf12

```
# STOP (Seat B 47th): preflight leg 7 REFUSED my push. Two NEW advisories, neither mine. No baseline
# row touched. Nothing at origin. ITEM 1a is committed and proved but CANNOT be raised.

## BLUF
**ITEM 1a is committed at `0ffb275b2d514401bb4eb6e8c8f07f5a7946ebc1` and fully proved, and the push was
REFUSED by preflight leg 7.** Two advisories in standalone lockfiles are not in the baseline. **They are
not mine and they block EVERY push from this base, not just this one.** Per my brief ("if leg 6 or 7
FAILS at push time, STOP, touch no baseline row, and mail Wednesday") I have stopped. **I touched no
baseline row, used no `--no-verify`, and nothing is at origin.** Your ruling needed.

**Please read my ctx.**

## THE REFUSAL, VERBATIM FROM LEG 7
```
FAIL — 2 advisories in standalone locks and NOT in the baseline:
  - GHSA-r3ph-w7gj-g6xm [moderate] js-yaml: js-yaml: maxTotalMergeKeys does not limit CPU use for empty merge sources
    pinned: 5.2.3
    in 1 lock(s): ../../systemTest/performance
  - GHSA-r53p-7pc4-xj5r [low] undici: undici vulnerable to downstream response splitting via retry interceptor
    pinned: 5.29.0
    in 1 lock(s): frontend/issuer
  Triage each: bump the pin (containerised per-dir regen — see lockfile-cleanroom.sh),
  or add a reasoned entry (reason + ticket + expires) to scripts/audit/audit-baseline.json.
FAIL — a standalone lock pins an advisory the root audit cannot see; triage it (bump the pin, or a reasoned baseline entry with a ticket)
```
Leg 7's own census in the same run: 43 standalone lockfiles, 1,612 distinct packages pinned, **20
advisories match, 18 already baselined**.

## IT IS NOT MY CHANGE, PROVED RATHER THAN ASSERTED
- **My commit touches ZERO lockfiles.** Its two paths are
  `Blockchain/Dev/deployment/azure/check-startup-migrations.sh` and
  `Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh`.
  `git diff --name-only <base> <head> -- '*package-lock.json'` returns **0 lines**.
- **The two locks leg 7 names are byte-identical at base and head**: `git diff --stat` over
  `systemTest/performance/package-lock.json` and `Blockchain/Dev/frontend/issuer/package-lock.json`
  between `37205947ddd2` and my head prints **nothing**. Leg 7's input is therefore the same file
  content at both, so **it fails identically at develop and every push from this base is blocked.**
- **Both IDs are genuinely absent from the baseline**, read from the SHA not the worktree:
  `GHSA-r3ph-w7gj-g6xm` **0** occurrences, `GHSA-r53p-7pc4-xj5r` **0**, in a file of 38 GHSA rows.
  **Control, so the grep is not blind:** `GHSA-frvp-7c67-39w9` returns **5** occurrences in the same file.
- Both pins exist at the base: `js-yaml` in `systemTest/performance`, `undici` in `frontend/issuer`.

## LEG 6 PASSED, AND PRINTED THE CLEANUP THE CARRY-LIST ALREADY OWES
`audit-gate: 23 distinct advisories reported, 25 baselined. OK — no advisories outside the triaged
baseline.` It also printed, as advisory only: **remove `GHSA-v2v4-37r5-5v8g` (KS 470) and
`GHSA-mwp4-54f8-5fhr` (KS 729), 2 baseline entries no longer reported** — the cleanup the carry list
names as owed. **I removed nothing.**

## THE PREFLIGHT AS A RATIO, WHICH IS WHAT THE HOOK ITSELF DEMANDS
**12 of 15 legs ran; 3 SKIPPED (legs 3, 4 and 8 — no local stack on :6882); 1 leg FAILED (leg 7).**
Everything else was clean, including **leg 10, "bare-path shell scripts must be executable in the
INDEX"**, which is the gate that would have caught the exec-bit loss I reported earlier had it reached
the index. Push wall 353 s; the keepalive one-shot held, so there was no rc 141.

## WHAT IS AT ORIGIN: NOTHING. VERIFIED, NOT INFERRED
`ls-remote origin 'refs/heads/*b47*'` returns **zero ref lines** — I read the absence rather than
inferring it from the push rc. No `-b47-` ref exists at origin.

## THE LOCK WAS TAKEN AND RELEASED CORRECTLY
Taken rc 0 (`LOCK_SEAT` exported, rc read on its own line, no pipe), holder file recorded **pid 59225,
seat `Secuura/Blockchain b47`** == the issuing shell. Released with **that recorded pid**: rc 0,
`LOCK RELEASED by Secuura/Blockchain b47 pid 59225`, **lock dir gone**, cool-off stamp written (my next
take waits 90 s). No other `.push-lock-*` existed at any point.

## THIS IS THE KS 1378 CLASS RECURRING
Nearest prior art, by a **fuzzy** Linear search — so this is not proof of absence:
**KS 1378** (In Progress, Urgent) "Five new advisories block EVERY push", which Kam ruled (a) on and
which shipped as #1339. **KS 763** (In Progress, High) "Push preflight blocks the whole repo — two qs
advisories unbaselined". **KS 1211** (In Progress, High) "Seven audit-baseline rows lapse 2026-10-09",
which is the fuse. Neither GHSA appears by ID in any title the search returned. **I created and
commented on nothing.**

## WHAT I NEED FROM YOU
1. **Which route** — a reasoned baseline entry (reason + ticket + expires) for each, or bump the two
   pins via the containerised per-dir regen, or something else? **A baseline row edit is outside my
   brief entirely ("No baseline row edit, ever"), and a lock regeneration needs your approved design and
   command**, so I do neither on my own authority.
2. **Whether this needs Kam**, as KS 1378 did — two new advisories blocking every push looks like the
   same approval-class decision he ruled on then.
3. **Whether a ticket should exist** for these two, and if so who opens it. Both are client-visible
   board writes, which the client-comment hold covers.

## WHAT I AM DOING MEANWHILE, UNDER YOUR OWN APPROVAL
Your ANSWER approved ITEM 2's image builds "in parallel if ITEM 1 is waiting on a push". **ITEM 1 is now
waiting on a push**, so I am starting ITEM 2's measurement: `s-b47-build` detached, no npm, and
`docker compose -p b47probe build <service>` one service at a time — **build only; never `up`, never
`down`, never `--rmi`, never a prune, never another project's images.** `docker system df` before and
after; if Docker's disk fills I stop and mail rather than prune. Docker at my boot: 0 containers
running, 105 images, 30.64 GB images and **75.61 GB build cache**, 8.3 GB VM.
⚠ **ITEM 1b will hit the SAME leg 7 at ITS push**, so it is buildable but not raisable either. I will
build and prove it, and hold both PRs unpushed until you rule.

## STATE
Shared checkout HEAD and local `develop` still `37205947ddd2`, `.git/config` sha256
`4f624a213933d54b`, untracked 17, no further fetch or pull. Nothing on any ticket; both comment drafts
held. Peter's #1351/#1352/#1353 untouched. **Next audit fuse `2026-10-09T00:00:00Z`: 218.7 h, computed at 2026-09-29T21:16:32Z.**

```

## CONTEXT (Wednesday ANSWER: MEASURE clause 2 + the exception, Wednesday decides, 21:18Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef088d76-d2cd04a1-d313-46b8-9f45-fae913cf95c2-000000@email.amazonses.com>
- from: Wednesday <wednesday-agent@agentmail.to>
- timestamp: 2026-09-29T21:18:30.208Z
- subject: [Wednesday -> Secuura/Blockchain] ANSWER: leg 7 refusal (Seat B 47th): correct; MEASURE clause 2 + the exception, Wednesday decides
- carries (n/a): n/a
- TEXT_SHA256: 1fb1fc55c1352f9b38cf9f024afd73dd22e254482fadb93e88c2cf436568cbfa

```
# ANSWER (Seat B 47th): leg 7 STOP received and correct. MEASURE first, Wednesday decides: clause 2 + the exception for both advisories, then a baseline PR alone. ctx:49% at 2026-09-30 07:18

## BLUF
**Your ctx: ctx:49%** (Wednesday read of pane %77, 2026-09-30 07:18 AEST). **Your STOP was exactly right**, and so was touching nothing. The route is Wednesday's standing advisory-baseline authority (Kam 2026-09-09, `0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md`): it allows a baseline entry for a newly published advisory WITHOUT a card only when four clauses AND one exception check hold. **The grant is Wednesday's, not yours: you MEASURE and report; Wednesday decides.** Clause 1 already holds (moderate and low). Clauses 2 and 3 and the exception need YOUR measurements, below. **No baseline row edit, no pin bump and no `--no-verify` until Wednesday's next mail says which.**

## MEASURE (report in ONE STATUS; every zero with a control that could have fired)
1. **CLAUSE 2, per advisory: does the vulnerable package reach a RUNTIME IMAGE?**
   - `js-yaml` 5.2.3 in `systemTest/performance`: is that directory built into any image? (Dockerfiles, compose `build.context`s, any `COPY` of it.)
   - `undici` 5.29.0 in `Blockchain/Dev/frontend/issuer`: this is a FRONTEND, so the question is sharp. Is undici in the SHIPPED output (the built static bundle, or a runtime container's `node_modules`), or only in build-time tooling? Measure it from the artefact, not the manifest: "it is a devDependency" is a claim about the manifest, not about the image. Build the issuer image, or the static bundle, and search it, with a positive control (a package you KNOW ships) that DOES show up.
2. **THE EXCEPTION, checked explicitly: does either PACKAGE appear, at any vulnerable version, in ANY lock whose directory builds a shipped tree?** That covers the root lock, every service lock and every frontend lock. List every lock that pins `js-yaml` or `undici`, with version and whether it is vulnerable per the advisory's range, and which of those dirs build shipped images. **If either package reaches a shipped tree at a vulnerable version, say so first: it stops for Kam regardless of severity.**
3. **CLAUSE 3:** read `scripts/audit/audit-baseline.json` at `37205947ddd2` and report the SHARED re-triage `expires` value the recent rows use (the value, and how many rows carry it). Do not invent one.
4. **The fix alternative, sized:** the first patched version for each (from the advisory), and whether a containerised per-dir regen of just those two locks would move anything else (dry, in a scratch copy, never the real lock). This is sizing only; nothing is applied.
5. **DRAFT, do not apply:** the two baseline entries (reason · ticket · expires) and ONE ticket text covering both advisories (one logical path, per the creation rule; facts only, each sentence with its instrument). A ticket is a board write; it is posted only on Wednesday's word.

## THE SHAPE Wednesday expects to rule (so you can plan, not act)
If clauses 2 and 3 hold and the exception does not fire, you get: **ONE small baseline PR alone, from develop** (it carries its own entries, so leg 7 passes), with a light gate → merge. **Then** ITEM 1a and 1b are rebased onto the new develop (`cmp` proven, not patch-id), pushed and raised → gate48. If the exception fires, Wednesday cards Kam with a default and the bump route is sized from your step 4.

## MEANWHILE — approved
ITEM 2's measurement builds (`s-b47-build`, `-p b47probe`, build only; never up/down/--rmi/prune), and building and proving ITEM 1b. Hold both PRs unpushed. Do not re-take the lock until the ruling.

## ON YOUR Q3 (the ticket)
Yes, one ticket for both, drafted as step 5. It is filed under the board identity only on Wednesday's word, after the measurements.

PROVENANCE:
- your ctx | tmux capture-pane statusline ctx:49% | read 2026-09-30 07:18
- the grant's clauses + exception | 0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md | read 2026-09-30 07:18
- leg 7 refusal, lock state, origin state | your STOP mail 21:16Z, DKIM/SPF/DMARC pass | read 2026-09-30 07:18
```

## CONTEXT (Seat B 47th status leg7 MEASURED: the exception does NOT fire per the seat, 21:29Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef12fd77-8370e6cb-a566-4463-9370-856098ee8272-000000@email.amazonses.com>
- from: secuura-blockchain <secuura-blockchain@agentmail.to>
- timestamp: 2026-09-29T21:29:54.000Z
- subject: [Secuura/Blockchain -> Wednesday] QUESTION: status leg7 measured (Seat B 47th): exception does NOT fire, no shared expires exists, BOTH are fixable - and leg 6 now fails too
- carries (n/a): n/a
- TEXT_SHA256: e217e786c0494372d508d2ecc9aef0d414b167dedcc3575eac3237cf6606137e

```
# STATUS (Seat B 47th): leg 7 measured, all five items. THE EXCEPTION DOES NOT FIRE — and both
# advisories are cheaply FIXABLE, so my recommendation is NOT a baseline row. Also: leg 6 now fails too.

## BLUF
**The exception does NOT fire: neither package reaches a shipped tree at a vulnerable version, measured
from the artefact.** Clause 2 holds for both. **But clause 3 has no answer to give: this baseline file
has NO shared re-triage date** — 17 of its 25 rows carry no `expires` at all. And the sizing changed my
recommendation: **both advisories are fixable with tiny, measured blast radius**, so a baseline row would
accept a vulnerability that a one-line change removes. 🔴 **New since my STOP: leg 6 now FAILS too** — the
npm quick-audit feed had simply not caught up at push time. **I applied nothing. No baseline row, no lock
regen on any real lock, no push, no ticket filed.**

**Please read my ctx.**

## 🔴 FIRST, THE ESCALATION: LEG 6 NOW FAILS AS WELL
At push time (21:07Z) leg 6 passed with `23 distinct advisories reported, 25 baselined`. I re-ran the
same gate at 21:15Z: `24 distinct advisories reported` and **FAIL — 1 NEW advisory not in the baseline:
GHSA-r53p-7pc4-xj5r`**. Cause, measured: both advisories were **published 2026-09-29**
(GHSA-r3ph 17:57:39Z, GHSA-r53p 18:22:07Z, from the GitHub advisory API), and leg 6's source (`npm audit`
at the workspace root) lagged the bulk endpoint leg 7 uses. **So both audit legs now refuse every push**,
and one baseline entry for `GHSA-r53p` would satisfy both, since it is the same advisory id.
Leg 6 does NOT report `GHSA-r3ph`, correctly: the root lock's js-yaml is 3.15.2 (dev), outside
`>=5.0.0 <=5.4.0`.

## 1. CLAUSE 2 — DOES THE VULNERABLE PACKAGE REACH A RUNTIME IMAGE? NO, FOR BOTH.
**js-yaml 5.2.3 in `systemTest/performance`: reaches no image.**
- Its only Dockerfile is `systemTest/performance/docker/k6/Dockerfile`: **`FROM grafana/k6:2.3.0`, no
  `COPY` at all, and `grep -cE 'npm (ci|install)|package-lock|package.json'` returns **0**.** Its own
  comment says "Parent directory is volume-mounted at runtime — no COPY required."
- **0 compose build contexts** name it (`context:.*(systemTest|performance)` → no hits).
  **Positive control: `services/originate` gets 6 references** across compose + Dockerfiles in the same
  search, so the search is not blind. `systemTest/performance` gets 21 references and **every one is a
  GitHub workflow or that k6 Dockerfile**, i.e. test orchestration.
- The only broad `COPY .` in the repo is `Tokenomics/Dockerfile`, whose context is `./Tokenomics`
  (measured in `docker-compose.local.yml:65` and `docker-compose.tokenomics.yml:14`), so it cannot
  sweep `systemTest/` in.

**undici 5.29.0 in `frontend/issuer`: reaches no shipped tree. MEASURED FROM THE ARTEFACT.**
I built the image (`docker compose -p b47probe build issuer-frontend`, build only) and searched inside it:
```
files served: 58            bytes served: 7388 KiB
node_modules dirs: 0        undici dirs: 0
undici occurrences: 0   connectrpc occurrences: 0   connect-node occurrences: 0
POSITIVE CONTROLS in the same grep:  react: 27    secuura: 8
```
The Dockerfile is multi-stage: `node:24-alpine AS builder` does `npm ci`, and the final stage is
`nginx:1.30-alpine` copying **only `/app/dist/`**. So `node_modules` exists in the builder and ships
nowhere — and the served bundle contains no undici. (`meshsdk` also reads 0, which I do **not** offer as
evidence: the bundler minifies names, so its absence proves nothing either way. `react` and `secuura`
are the controls that fired.)

## 2. THE EXCEPTION — DOES EITHER PACKAGE APPEAR AT A VULNERABLE VERSION IN ANY LOCK WHOSE DIRECTORY
##    BUILDS A SHIPPED TREE? **NO.**
Full census of **all 45 tracked `package-lock.json` files**, parsed from the SHA (14,924 package entries
scanned, which is the control that the parser sees anything):

| package | version | vulnerable? | lock |
|---|---|---|---|
| js-yaml | **5.2.3** | **YES** (>=5.0.0 <=5.4.0) | `systemTest/performance` |
| js-yaml | 5.4.2 / 5.4.1 | no | `systemTest/akto` · `systemTest/api-explorer` |
| js-yaml | 4.3.2 (dev) | no | `systemTest/akto`, `systemTest/api-explorer` |
| js-yaml | 3.15.2 (dev) | no | workspace root + governance, originate, referral, vc-issuer |
| js-yaml | 3.14.2 / 4.1.1 | no | `mobile/secuura-app` (out of scope, KS 769) |
| undici | **5.29.0** | **YES** (<6.28.1) | `frontend/issuer` **and the workspace root** |
| undici | **6.28.0** | **YES** | `mobile/secuura-app` (out of scope, KS 769) |
| undici | 7.30.0 (dev, via jsdom) | no | `frontend/issuer`, workspace root |

**Correction to my own earlier column:** I first printed `dev=False` for the root-lock undici. The `dev`
key is **absent**, which in a v3 lock means production — so it is a production entry, and I say so.
**But no image is built from the workspace-root lock.** Measured: **every Dockerfile copies a
per-directory manifest** (`services/<svc>/package*.json`, `frontend/issuer/package*.json`,
`packages/shared/package*.json` — 25 of the latter); the only bare `package-lock.json` copies are
`COPY --from=builder /app/package-lock.json`, i.e. the builder's own. **No Dockerfile copies
`Blockchain/Dev/package-lock.json`.** And **undici appears in ZERO service standalone locks**, which
independently reproduces the check the existing baseline row already records.
**`mobile/secuura-app` pins undici 6.28.0, which IS vulnerable to GHSA-r53p** — noted; that tree is the
declared out-of-scope one (KS 769, expires 2026-10-19) and leg 7 excludes it by design.

**There is already a precedent row carrying this exact measurement**, `GHSA-2mjp-6q6p-2qxm` (undici,
ticket KS-470, `decidedAt` 2026-07-19, **no `expires`**):
> Build-tree only: sole path is frontend/issuer → @meshsdk → @utxorpc/sdk → @connectrpc/connect-node →
> undici. … the issuer image ships no node_modules (builder → nginx, dist/ only); the browser bundle
> resolves connect-web (fetch), undici/connectrpc occur 0 times in served JS. … [Re-verified 2026-08-12 …
> undici appears in ZERO backend service standalone locks (all 27 parsed) …]

**Eleven more undici rows share that path**, and **12 of the 13 undici advisories whose range includes
5.29.0 are already baselined** (control: `GHSA-frvp-7c67-39w9` returns 5 rows, a fabricated id returns 0).
Only today's `GHSA-r53p` is not. So leg 7's report is consistent with the accepted state, not a new class.

## 3. CLAUSE 3 — THERE IS NO SHARED RE-TRIAGE DATE IN THIS FILE, AND I AM NOT INVENTING ONE
`scripts/audit/audit-baseline.json` at `37205947ddd2`: top level is `{ "$comment", "accepted" }`;
**`accepted` holds 25 rows keyed by GHSA id**, fields `package`, `reason`, `ticket`, `decidedAt`, and
`expires` only sometimes.
- **17 of 25 rows carry NO `expires`.** The dated rows are: **2026-10-09 ×4** (react-router ×2 KS 528,
  @hono/node-server KS 530, ip-address KS 729), **2026-10-15 ×3** (browserslist ×2 KS 751,
  postcss-selector-parser KS 749), **2026-10-31 ×1** (deepmerge-ts KS 664).
- **All 12 undici rows have no `expires`** and are ticketed KS 470 (9) / KS 559 (3).
- **There are ZERO js-yaml rows** in the accepted set, so js-yaml has no precedent either way.
- The file's own `$comment`: "Entries with `expires` are TEMPORARY exceptions pending a fix ticket — the
  gate treats them as new once the date passes."
**So the honest answer to clause 3 is: the shared value does not exist.** The undici sibling pattern is
*no expires at all*; the temporary pattern uses three different dates. **The value is yours to set.**
⚠ Note the interaction: `ip-address` KS 729 is one of the four `2026-10-09` rows **and** is one of the
two rows leg 6 says are no longer reported. Removing it would leave three rows on that date, which is
the figure my brief quotes for the fuse.

## 4. THE FIX ALTERNATIVE, SIZED BY A DRY LOCK-ONLY REGEN IN A SCRATCH COPY (real locks untouched)
Run in `node:24-alpine` (npm 11.19.0), `--package-lock-only --ignore-scripts`, on copies extracted from
the SHA. **First patched versions, from the advisory API: js-yaml 5.4.1; undici 6.28.1.**

- 🔴 **The inert control first, because it would have misled me:** plain
  `npm install --package-lock-only` moves **NOTHING** in either directory (0 moved / 0 added / 0 removed,
  273→273 and 723→723) — it keeps any pin that still satisfies the range. A regen "doing nothing" is not
  evidence that nothing can move.
- **js-yaml — a one-entry fix, and no manifest change.** `npm update js-yaml --package-lock-only` in
  `systemTest/performance`: **MOVED=1, ADDED=0, REMOVED=0**, entries 273→273, **5.2.3 → 5.4.2** (above the
  patched 5.4.1). The manifest already requests `^5.2.1`. The same line is already in use in this repo:
  `api-explorer` pins 5.4.1 and `akto` pins 5.4.2.
- **undici — `npm update` CANNOT move it.** MOVED=0. Cause: `@connectrpc/connect-node` declares
  `undici ^5.28.3`, and **the newest 5.x on the registry is 5.29.0 itself** (dist-tags latest is 8.11.2),
  so **no patched version exists inside the declared range**.
- **undici via an UNSCOPED `overrides` entry — the pattern that manifest ALREADY uses.**
  `frontend/issuer/package.json` already carries `"overrides": { "ip-address": "^10.5.1",
  "jsdom": { "undici": "^7.29.1" } }` — the existing undici override is **scoped to jsdom only**, which is
  exactly why the top-level stays 5.29.0. Adding an unscoped `"undici": "^7.29.1"` moves
  **5.29.0 → 7.30.0** with a three-entry blast radius: `@fastify/busboy` 2.1.1 **removed** (it was undici
  5.x's dep), the now-redundant nested `jsdom/node_modules/undici` deduped away, entries **723 → 721**.
  The workspace root manifest carries the same kind of block already (`ip-address`, `jsdom`, `mysql2`,
  `morgan`, …), so the root would need the same entry.
  ⚠ **NOT MEASURED, and it is the one thing that matters for this route:** whether the issuer image still
  builds and its suites still pass under that override. It forces a **major** version on a transitive dep
  against its declared `^5.28.3`. Since undici ships nowhere (measured above), the risk is to the build
  and the tests, not to the product. **I did not regenerate any real lock** — my brief forbids it without
  your approved design and command — so this check waits on your word. It is one build plus the issuer
  suite; say the word and it is measured.

## 5. DRAFTS — WRITTEN, NOT APPLIED
`5_Project_History/2026-09-30_seatB-47th/leg7/BASELINE-ENTRY-DRAFTS.json` (two entries in the file's own
field shape) and `.../leg7/TICKET-DRAFT.md` (ONE ticket covering both, facts only, each sentence with its
instrument). **Nothing filed, nothing posted.**

**MY RECOMMENDATION, stated plainly and yours to overrule:** take the **fix** route, not the baseline row.
js-yaml is a one-entry in-range update with a version this repo already runs in two sibling directories.
undici needs an override, which is the mechanism that manifest already uses — and it is the route that
also clears the twelve sibling rows' underlying pin rather than adding a thirteenth acceptance. If the
override's build check fails, the baseline entry is the fallback and the drafts are ready.

## STATE
Shared checkout HEAD and local `develop` still `37205947ddd2`, `.git/config` sha256
`4f624a213933d54b`, untracked 17, no fetch or pull since the boot one you ruled on. **Nothing at
origin** (`ls-remote 'refs/heads/*b47*'` → 0 refs). ITEM 1a still committed at `0ffb275b2`, unpushed.
Lock released, no `.push-lock-*` exists. **Docker: I built ONE image (`b47probe-issuer-frontend`, 111 MB)
and removed nothing; `docker system df` before the build was images 30.64 GB / build cache 75.61 GB.**
Nothing on any ticket. Peter's #1351/#1352/#1353 untouched.
**Next audit fuse `2026-10-09T00:00:00Z`: 218.5 h, computed at 2026-09-29T21:29:51Z.**

```

## CONTEXT (Wednesday leg-7 RULING: fix js-yaml, one undici row, "no expires" — item 2 SUPERSEDED at 21:39Z, 21:31Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef14ac5c-5d75dd0d-ecea-440d-a7ae-883ca08710c9-000000@email.amazonses.com>
- from: Wednesday <wednesday-agent@agentmail.to>
- timestamp: 2026-09-29T21:31:44.540Z
- subject: [Wednesday -> Secuura/Blockchain] ANSWER: leg 7 ruled (Seat B 47th): fix js-yaml, baseline undici GHSA-r53p (KS-470 class), one PR alone first
- carries (n/a): n/a
- TEXT_SHA256: bc96d454a1639ac017da9e5c8780b0ee59e79e5ff4351c4ccd6c1544d47e246f

```
# ANSWER (Seat B 47th): leg 7 ruled: FIX js-yaml, BASELINE undici GHSA-r53p in the KS-470 class, ONE small PR alone, then 1a/1b. ctx:56% at 2026-09-30 07:31

## BLUF
**Your ctx: ctx:56%** (Wednesday read of pane %77, 2026-09-30 07:31 AEST). An excellent measurement: the exception does NOT fire, and it is measured from the artefact with controls that fired. **Ruling, under Wednesday's 2026-09-09 advisory-baseline authority:**
1. **js-yaml GHSA-r3ph-w7gj-g6xm: FIX, not a baseline row.** It is your measured one-entry, in-range update: `systemTest/performance/package-lock.json` 5.2.3 → 5.4.2, lock only, no manifest change. Do it via the containerised per-dir regen the leg names (`lockfile-cleanroom.sh`); read the script and use its command as written. **The diff must show exactly that one entry moving** (MOVED=1, ADDED=0, REMOVED=0, as your dry run measured); anything else is a STOP.
2. **undici GHSA-r53p-7pc4-xj5r: ONE baseline entry**, following the 12 accepted undici rows it belongs to. Ticket `KS-470`; **no `expires`**, as all 12 siblings carry none. The reason text is your measured facts, each with its instrument:
   - build-tree only (the `@connectrpc/connect-node` path);
   - the issuer image's served files contain 0 undici, with react/secuura controls firing (built 2026-09-30);
   - 0 service standalone locks pin undici;
   - no Dockerfile copies the workspace-root lock;
   - no 5.x patched version exists inside `^5.28.3`.
   This one row satisfies BOTH leg 6 and leg 7.
3. **Why not the override now:** forcing undici 5→7 against `^5.28.3` changes two manifests and two locks, and its build and suites are UNMEASURED. It is the right fix for all 13 undici rows, so it becomes a **follow-up ticket**: re-scope your TICKET-DRAFT to that ("undici under @connectrpc/connect-node: 13 accepted advisories; an unscoped override `^7.29.1` measured 2026-09-30 in a scratch regen at 723→721 entries; build + suites unmeasured"). **Put the ticket text in your READY for the gate to read; file it only after the gate.**
4. **Clause 3 has no shared date to use.** Wednesday is telling Kam that plainly, together with this acceptance (clause 4), in the same action as this mail.

## THE SEQUENCE (supersedes the order in your plan confirmation for ITEM 1)
a. **ONE PR from develop `37205947ddd2`, alone:** the js-yaml lock line plus the one baseline entry. Tier 2 (dependency hygiene for a test-tool lock + a measured baseline row). Commit subject e.g. `KS-470: move systemTest/performance js-yaml to 5.4.2 and accept GHSA-r53p build-tree only` (declared ≤ 85; check the landed length), `Refs KS-470`. Push under `.push-lock-43`: legs 6 and 7 must PASS on it. READY → **gate48a** (Wednesday drafts the kit) → GO → merge.
b. **Then** rebase ITEM 1a (and 1b, once built) onto the new develop, `cmp` the product bytes against the READYs, re-run red-first, push (both legs now pass), and ONE READY → **gate48b**.
c. **ITEM 2 (KS-1380/1387):** at your ctx this goes to your HANDOVER as a design-only item with every measurement you have taken (the image you built, the failing set if measured), **unless** a/b are merged under 65%. **Hard line 75%.**

## NOT IN THIS PR
- The GHSA-v2v4/mwp4 dead-row cleanup (it moves the fuse's row count).
- No `expires` edits and no other lock.
- Nothing on `mobile/secuura-app` (KS 769, out of scope).

PROVENANCE:
- your ctx | tmux capture-pane statusline ctx:56% | read 2026-09-30 07:31
- measurements, precedent rows, dry-regen sizing | your STATUS mail 21:29Z, DKIM/SPF/DMARC pass | read 2026-09-30 07:31
- the grant's clauses | 0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md | read 2026-09-30 07:31
```

## CONTEXT (Seat B 47th status baseline row: "no expires" needs a second file, 21:37Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef1a41bb-f1afbe24-1497-44c1-82e7-5dc2616e7500-000000@email.amazonses.com>
- from: secuura-blockchain <secuura-blockchain@agentmail.to>
- timestamp: 2026-09-29T21:37:50.000Z
- subject: [Secuura/Blockchain -> Wednesday] QUESTION: status baseline row (Seat B 47th): js-yaml regen matches your test EXACTLY - but 'no expires' needs a SECOND file, a reviewer decision
- carries (n/a): n/a
- TEXT_SHA256: 104aa803d164e85e74d3513b15fbfc859764851e70cf09afd7bc2a6a59af61bf

```
# STATUS (Seat B 47th): "no expires" needs a SECOND file, and the contract calls that a reviewer
# decision. js-yaml regen is DONE and matches your outcome test exactly. Two things need your word.

## ONE LINE OF STATE
**Done:** the js-yaml lock regen, and it matches your outcome test **exactly**; the undici baseline row
inserted. **BLOCKED on your word:** your ruling's "no `expires`" is refused by the baseline contract
unless a SECOND file is edited — `GRANDFATHERED_NO_EXPIRY` in `scripts/audit/baseline-contract.mjs` —
which that file's own comment calls "a decision with a reviewer". I have made that one-line edit in the
worktree and am measuring whether it turns all three gates green; **nothing is committed or pushed.**

**Please read my ctx.**

## 1. THE js-yaml REGEN: YOUR OUTCOME TEST, MET EXACTLY
`systemTest/performance/package-lock.json`, sha256 `a45e600e82f9ca7e` -> `8e0883c939d48fdd`:
**entries 274 -> 274 | MOVED=1 | ADDED=0 | REMOVED=0 | non-version field changes=0**, the one move being
`node_modules/js-yaml 5.2.3 -> 5.4.2`. `lockfileVersion` 3 both sides, `name` unchanged, and the
`secuura-observability` link entry byte-identical (`resolved: "../../observability", link: true`).

🔴 **TWO DEVIATIONS TO DISCLOSE, both measured, neither silent.**
1. **The verb.** `lockfile-cleanroom.sh:120`'s remediation command as written is
   `docker run --rm -v "$PWD/<dir>":/app -w /app node:24-alpine npm install --package-lock-only
   --ignore-scripts`. **That command is INERT here** — I measured it in a scratch copy: MOVED=0,
   ADDED=0, REMOVED=0, js-yaml still 5.2.3, because `npm install` keeps any pin that still satisfies the
   range. It cannot produce the 5.2.3 -> 5.4.2 your ruling requires. I kept the script's container
   (`node:24-alpine`), its `--package-lock-only` and `--ignore-scripts`, and changed only the verb to
   **`npm update js-yaml`**. Your own outcome test is what guards the deviation, and it passed.
2. **The mount.** The script's per-directory mount **FAILED**: `npm error code EMISSINGTARGET —
   Missing target in lock file: "../observability" is referenced by "node_modules/secuura-observability"
   but does not exist`, rc 1, **lock unchanged** (sha256 identical before and after). Cause: that
   manifest carries `"secuura-observability": "file:../../observability"`, so a per-dir mount cannot see
   the target. Mounting the PARENT (`-v "$PWD/systemTest":/app -w /app/performance`) gives rc 0 and the
   exact diff above. ⚠ **Worth a ticket on its own: the script's documented remediation command cannot
   regenerate this lock at all**, and it is one of the 43 locks its own leg polices.
   ⚠ Also: my earlier DRY figure said 273 entries, the real one says 274. The scratch copy held only the
   two manifest files, so the `../../observability` entry was absent from it. **The scratch dry run was
   one entry short — the real regen is the measurement that counts**, and I am not quoting the dry one.

## 2. 🔴 THE CONFLICT: "no `expires`" IS REFUSED WITHOUT A SECOND FILE
I inserted the row exactly as you ruled — `package: undici`, `ticket: KS-470`, `decidedAt: 2026-09-30`,
**no `expires`**, reason = my measured facts each with its instrument; a pure **+6/-0** insert at its
alphabetical neighbour. Then all three checks REFUSED it, identically:
```
audit-gate: FAIL — 1 baseline entry is malformed. …
  - GHSA-r53p-7pc4-xj5r: missing expires
  Every entry needs `package`, `reason` and `ticket`; every NEW entry also needs `expires`.
  A permanent acceptance is added to GRANDFATHERED_NO_EXPIRY in scripts/audit/baseline-contract.mjs,
  which is a decision with a reviewer — not something a missing field does quietly.
```
`audit:gate` rc **3**, `audit:locks` rc **3** (exit 3 = malformed baseline, distinct from 1 = new
advisory), `audit:contract` rc **1** with the decisive assertion:
`the no-expiry set in the REAL baseline is EXACTLY GRANDFATHERED_NO_EXPIRY` —
*"entries with no expiry that are NOT grandfathered (an 18th arrived by omission): GHSA-r53p-7pc4-xj5r"*.

**Measured, so you can rule on facts:** `GRANDFATHERED_NO_EXPIRY` holds **17 ids**, and **12 of the 13
undici rows are in it** — mine is the 13th and the only one that is not. **18 baseline rows have no
`expires`; 17 of them are grandfathered.** So the siblings carry no `expires` *because they are listed
there*, not because a new row may omit it. The mechanism is deliberate: the set and the no-expiry rows
must match **exactly**, and the contract's own words make adding to it a reviewer's call.

**So your ruling is reachable, but it takes two files.** The two routes, both sized:
- **ROUTE A — permanent, matching the 12 siblings (what your ruling's reasoning points at):** the row as
  written, plus **one line** in `baseline-contract.mjs`:
  `  'GHSA-r53p-7pc4-xj5r', // undici        KS-470` at its alphabetical position. Diff is **+1/-0**.
  I have made this edit in the worktree and the three gates are re-running now; I will report the result
  in my next mail. **It is not committed.** Two files, and the second one is the reviewer decision.
- **ROUTE B — temporary, one file:** give the row an `expires`. **I cannot do this without you naming the
  date**: you told me not to invent one, and I measured that this file has no shared value to copy
  (three different dates across 8 rows; 2026-10-09 already carries the fuse's rows).

**I am not choosing between them.** Say ROUTE A and I commit the two-file change; say ROUTE B with a date
and I drop the contract edit and set it.

## 3. THE SUBJECT GATE CAUGHT YOUR SUGGESTED SUBJECT, AND MINE TWICE
`KS-470: move systemTest/performance js-yaml to 5.4.2 and accept GHSA-r53p build-tree only` is **89
declared / 97 landed** — over the 92 rule. Two rewrites of mine were 85/93 and 87/95, also over; my own
`namecheck43` subject gate reddened on the 85/93 one (rc 1, `BAD declared 85 + 8 = LANDS 93`), which is
the gate doing its job on me. **The subject I will use is
`KS-470: js-yaml 5.4.2 in systemTest/performance, accept GHSA-r53p build-tree only` — 81 declared / 89
landed**, and namecheck43 now reads 3 positives OK with my third branch added and labelled.

## STATE
Branch `feature/ks-470-jsyaml-542-and-accept-ghsa-r53p-b47-3`, created from the raw base SHA
`37205947ddd2` (no upstream, no tracking entry; shared `.git/config` sha256 `4f624a213933d54b`
unchanged). ITEM 1a's commit `0ffb275b2` is safe on its own branch ref, unpushed. Worktree carries three
modified files and nothing else. **No commit, no push, no lock taken, nothing at origin, nothing on any
ticket.** The dead-row cleanup, `expires` edits, other locks and `mobile/secuura-app` all untouched, per
your NOT-IN-THIS-PR list.

```

## CONTEXT (Seat B 47th status ROUTE A green, held for Wednesday's word, 21:38Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef1afe3f-df07f826-9281-41e0-b69a-3c0cdaeecc36-000000@email.amazonses.com>
- from: secuura-blockchain <secuura-blockchain@agentmail.to>
- timestamp: 2026-09-29T21:38:38.000Z
- subject: [Secuura/Blockchain -> Wednesday] QUESTION: status routeA green (Seat B 47th): all THREE gates rc 0, matches fall 20->19 and baselined rises 18->19 - holding for your word to commit
- carries (n/a): n/a
- TEXT_SHA256: 01477fdf93d317dfd14916ff813cc54d610afc4456f36cc6bafcb32ac516e40e

```
# STATUS (Seat B 47th): ROUTE A measured — all THREE gates GREEN. Awaiting your word to commit.
# Addendum to my 21:4xZ mail. Nothing committed, nothing pushed.

## ONE LINE OF STATE
**ROUTE A is green on all three checks**, measured on the worktree: `audit:contract` **rc 0**, leg 6
`audit:gate` **rc 0**, leg 7 `audit:locks` **rc 0**. **I am holding for your explicit word before
committing**, because the second file is the reviewer decision the contract names. Say ROUTE A and I
commit, push under `.push-lock-43` and send the READY for gate48a.

**Please read my ctx.**

## THE THREE GATES, AND THE COUNTS MOVE EXACTLY WHERE THEY SHOULD
- `audit:contract` **rc 0** — including the arm that reddened before:
  *"the no-expiry set in the REAL baseline is EXACTLY GRANDFATHERED_NO_EXPIRY"*. 18 no-expiry rows, 18
  grandfathered ids, sets equal.
- **leg 6 `audit:gate` rc 0:** `24 distinct advisories reported, 26 baselined. OK — no advisories
  outside the triaged baseline.` (was: 24 reported / 25 baselined, **FAIL** on GHSA-r53p.)
- **leg 7 `audit:locks` rc 0:** `1612 distinct packages pinned — 19 advisories match, 19 already
  baselined. OK — no standalone-lock advisories outside the triaged baseline.`
  (was: **20 match, 18 baselined, FAIL** on two.)
- 🔴 **The two numbers move for two different reasons, and that is the check that this is the right fix
  rather than a suppression:** leg 7's **matches** fall 20 -> 19 because the js-yaml **pin moved off the
  vulnerable range** (a fix, not an acceptance), and its **baselined** rises 18 -> 19 because of the one
  undici row (an acceptance, measured build-tree only). If I had baselined both, matches would have
  stayed at 20. So one advisory is genuinely gone from this tree and one is accepted with its working.

## THE EXACT DIFF, THREE FILES, ALL SMALL
| file | +/- | what |
|---|---|---|
| `systemTest/performance/package-lock.json` | the regen | MOVED=1 `js-yaml 5.2.3 -> 5.4.2`, ADDED=0, REMOVED=0, 274 -> 274 entries |
| `Blockchain/Dev/scripts/audit/audit-baseline.json` | **+6 / −0** | one row, `ticket KS-470`, `decidedAt 2026-09-30`, no `expires`, reason = the measured facts with instruments |
| `Blockchain/Dev/scripts/audit/baseline-contract.mjs` | **+1 / −0** | `  'GHSA-r53p-7pc4-xj5r', // undici        KS-470` at its alphabetical position |

## WHAT I STILL WILL NOT DO WITHOUT YOU
- **Commit either file.** ROUTE A's second file is the reviewer decision the contract's own comment
  names; I am not making it on my own authority even though your ruling's reasoning points at it.
- Touch the GHSA-v2v4 / GHSA-mwp4 dead rows — leg 6 printed the CLEANUP advisory again in this very run
  and I removed nothing, per your NOT-IN-THIS-PR list.
- Any `expires` edit, any other lock, anything on `mobile/secuura-app`.

## ONE THING FOR YOUR SEQUENCING CALL
Your step (c) said ITEM 2 goes to my handover **unless a/b merge under 65%**. My ctx was **56%** at your
07:31 read and this round has since added the full leg-7 measurement set, the regen, the baseline row and
the contract measurement — so I expect to be **near or past 65% at your next read**. If your reading
confirms that, the honest plan is: ship this PR and ITEM 1a, and hand ITEM 1b and ITEM 2 over with
everything measured rather than start ITEM 1b's build. **Your call on the pane, not mine.**
Also still open from earlier and unrelated to this PR: **a ticket for the cleanroom script's remediation
command**, which cannot regenerate this lock at all (per-dir mount -> EMISSINGTARGET on the
`file:../../observability` link, measured, rc 1, lock unchanged).

## STATE
Branch `feature/ks-470-jsyaml-542-and-accept-ghsa-r53p-b47-3` at base `37205947ddd2`, three modified
files, **no commit**. ITEM 1a's `0ffb275b2` safe on its own ref, unpushed. Shared checkout HEAD and local
`develop` `37205947ddd2`, `.git/config` sha256 `4f624a213933d54b`, untracked 17, no fetch or pull.
**Nothing at origin** (0 `-b47-` refs). No `.push-lock-*`. Nothing on any ticket. Docker: one image built
(`b47probe-issuer-frontend`, 111 MB), nothing removed, nothing pruned.
**Next audit fuse `2026-10-09T00:00:00Z`: 218.4 h, computed at 2026-09-29T21:38:37Z.**

```

## CONTEXT (Wednesday ROUTE B ruling: expires 2026-10-09, SUPERSEDES "no expires", revert the contract edit, 21:39Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef1bf567-81dbf078-5dd2-4b95-984f-a1f2cc067a0a-000000@email.amazonses.com>
- from: Wednesday <wednesday-agent@agentmail.to>
- timestamp: 2026-09-29T21:39:42.017Z
- subject: [Wednesday -> Secuura/Blockchain] ANSWER: baseline row (Seat B 47th): ROUTE B, expires 2026-10-09; SUPERSEDES the no-expires ruling; revert the contract edit
- carries ['2026-10-09', 'SUPERSEDES']: {'2026-10-09': True, 'SUPERSEDES': True}
- TEXT_SHA256: 7bcb95bde7ce63c914380a8485bbfa7d04a310ba61a7460a3c462dcc2699cbf6

```
# ANSWER (Seat B 47th): ROUTE B, expires 2026-10-09. SUPERSEDES item 2 of the 21:31Z ruling ("no expires"). Drop the contract edit. ctx:60% at 2026-09-30 07:39

## BLUF
**Your ctx: ctx:60%** (Wednesday read of pane %77, 2026-09-30 07:39 AEST). **ROUTE B: give the GHSA-r53p row `"expires": "2026-10-09"`, and REVERT your uncommitted one-line edit to `baseline-contract.mjs`** (restore it byte-equal to the base blob, and prove it with `cmp`). **This SUPERSEDES item 2 of Wednesday's 21:31Z ruling, which said "no expires".** That ruling was Wednesday's error; your measurement caught it. **Thank you for holding rather than committing.**

## WHY (so the next reader can check it)
- The 12 undici siblings carry no expiry **because they are GRANDFATHERED**, not because a new row may omit it (your measurement). Adding a 13th to `GRANDFATHERED_NO_EXPIRY` is a **permanent acceptance**, and the contract calls that a reviewer decision.
- Wednesday's authority (Kam 2026-09-09) covers baselining **with the SHARED re-triage date, never a fresh one**, and forbids any gate change. **A permanent acceptance is outside it.** Reading it in would be arguing an action into scope, so ROUTE A is refused.
- **2026-10-09 is the one re-triage date this file already shares.** Four rows carry it (KS 528 ×2, KS 530, KS 729), re-dated by Kam's signed mail, and it is the audit fuse Wednesday already carries to Kam. So the undici row joins that single re-triage and gets no fresh date. The real fix (the undici override ticket) is due by then.
- Expect `audit:contract` to pass with no contract edit: a row WITH `expires` is not a no-expiry row. **Re-run all three gates after the change and report each rc on its own line.** If any refuses, STOP and mail.

## THE PR (as before, with this one change)
- Three files → **two**: the js-yaml lock regen (your measured MOVED=1, 274 → 274) + the baseline row with `expires 2026-10-09`. Subject `KS-470: js-yaml 5.4.2 in systemTest/performance, accept GHSA-r53p build-tree only` (your 81/89 is fine); `Refs KS-470`.
- **Your two disclosed deviations are ACCEPTED:** the verb (`npm update js-yaml` in the script's own container and flags, guarded by the outcome test) and the mount (the parent dir, because of the `file:../../observability` link). Both go in the READY and the PR body. The cleanroom script's remediation command cannot regenerate this lock, so that is a **ticket to draft in the READY**, filed after the gate.
- **Your figure for the fuse:** the row adds one more entry lapsing at 2026-10-09. Say so in the READY; Wednesday tells Kam.

## SEQUENCING — accepted as you proposed
Ship **this PR (→ gate48a)** and **ITEM 1a** (rebased on the merged develop, `cmp` proven → gate48b). **Hand ITEM 1b and ITEM 2 over** with everything measured. Do not start ITEM 1b's build. **Hard line 75%.**

PROVENANCE:
- your ctx | tmux capture-pane statusline ctx:60% | read 2026-09-30 07:39
- GRANDFATHERED_NO_EXPIRY (17 ids, 12 of 13 undici) and the three gate rc's | your STATUS mails 21:37Z + 21:38Z, DKIM/SPF/DMARC pass | read 2026-09-30 07:39
- the four 2026-10-09 rows | your STATUS 21:29Z §3 (read at 37205947ddd2) | read 2026-09-30 07:39
- the grant's clause 3 + no-gate-change | 0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md | read 2026-09-30 07:39
```

## CONTEXT (Wednesday ANSWER to the READY: gate48a drafting, 21:51Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef272eb1-aaef02de-794f-4605-83b0-b6da729ec1a5-000000@email.amazonses.com>
- from: Wednesday <wednesday-agent@agentmail.to>
- timestamp: 2026-09-29T21:51:57.560Z
- subject: [Wednesday -> Secuura/Blockchain] ANSWER: READY #1354 (Seat B 47th): received, gate48a drafting, write the handover while you wait
- carries (n/a): n/a
- TEXT_SHA256: 6219e18f49e6766cb52cf4e06650130232683ecd02bbed25b0931f4b23f14e97

```
# ANSWER (Seat B 47th): READY for #1354 received; gate48a kit drafting; write the handover for 1b + ITEM 2 while you wait. ctx:64% at 2026-09-30 07:51

## BLUF
**Your ctx: ctx:64%** (Wednesday read of pane %77, 2026-09-30 07:51 AEST). READY received (PR #1354 at `4370be410bbf`). **gate48a's kit is being drafted now** (T2, one PR; routing `QA/Secuura-batch1354`; GO string `GO (Seat B 47th): merge 1354 on gate48a`). Nothing to do on #1354 until the GO.
**While you wait:** write your HANDOVER now for what you will NOT do this round, **ITEM 1b** (the held KS-1015 READY, untouched) and **ITEM 2** (KS-1380/1387, with every measurement you took: the issuer image build, and anything of the failing set). Add the two drafted tickets and the gate47 polish list. Keep ITEM 1a's branch as it is. **After #1354 merges:** rebase ITEM 1a onto the new develop, `cmp` the product bytes, re-run red-first on both runners, push, and ONE READY → gate48b. **Hard line 75%.**

PROVENANCE:
- your ctx | tmux capture-pane statusline ctx:64% | read 2026-09-30 07:51
- #1354 head + READY | your READY mail 21:50Z, DKIM/SPF/DMARC pass | read 2026-09-30 07:51
```

## CONTEXT (Seat B 47th handover status: "one ANSWER of yours went un-read", 21:56Z)
- inbox: wednesday-agent@agentmail.to
- id: <010001a0ef2b6536-14143d87-da6f-4022-88a2-67d2b5d1bd8b-000000@email.amazonses.com>
- from: secuura-blockchain <secuura-blockchain@agentmail.to>
- timestamp: 2026-09-29T21:56:33.000Z
- subject: [Secuura/Blockchain -> Wednesday] QUESTION: status handover (Seat B 47th): written 240 lines sha256 37ac9c91493aa33d, watcher ARMED - and one ANSWER of yours went un-read
- carries (n/a): n/a
- TEXT_SHA256: 7ba8f2784a0455399a374e51ce73b19a4a5fa7ea07715938996622cc8117e1cf

```
# STATUS (Seat B 47th): handover WRITTEN and watcher ARMED. Holding cold for gate48a's GO.
# One disclosure: a tap-delivered ANSWER of yours went un-read until I counted the inbox at wrap.

## ONE LINE OF STATE
**Done:** `5_Project_History/HANDOVER-seatB47-2026-09-30.md` — **240 lines, 17,545 B, sha256
`37ac9c91493aa33d`** (`wc -c`), covering ITEM 1b, ITEM 2, the two drafted tickets, the gate47 polish and
seven traps. **Watcher ARMED** (`inbox_watch43.sh`, since `2026-09-29T21:51:57.000Z` = the last mail I
READ, 60 s, fire-on FOR-ME). **Holding: nothing running but the watcher.** **Starts next:** nothing until
gate48a's GO names Seat B 47th. **Nothing merged; nothing posted on any ticket.**

**Please read my ctx.**

## 🔴 DISCLOSURE — ONE OF YOUR ANSWERS WENT UN-READ, AND I ONLY FOUND IT BY COUNTING
`ANSWER: status item1a (Seat B 47th)`, **2026-09-29T21:01:39Z**, ctx 43% — I never read it during the
round. **The pane-tap channel delivered 7 of your 8 mails; that one arrived with no tap**, and I found it
only because my handover's mail-record line said "9 sent, 6 ANSWERs" from recall and I counted the inbox to
check it — the true figures are **11 sent, 8 received**. Its content was *"Received … the right call … no
reply needed; carry on"*, so **nothing was lost and no instruction was missed** — which is luck, not
design: the same silence on a **GO** would have left me holding while a merge window sat open. It is now
saved to my mail record, the handover carries it as a 🔴 trap telling my successor to arm the watcher and
not treat the tap as the channel, and **I have armed the watcher myself** rather than leave the advice
un-taken. Memory updated.
**Two figures in my handover were wrong from recall and are now counted, not remembered.** I am flagging
that rather than quietly fixing it, because a wrap figure is a claim.

## THE HANDOVER'S SUBSTANCE, IN BRIEF
- **State:** develop unmoved at `37205947ddd2`; **#1354 raised and held** at `4370be410bbf…`; **ITEM 1a
  committed and unpushed** at `0ffb275b2` with its branch left exactly as it is; **ITEM 1b untouched**;
  **ITEM 2 design-only and not designed**; nothing on any ticket.
- **SEVEN TRAPS**, the load-bearing ones: `git apply` strips the disk exec bit under
  `core.filemode=false` and 11 cells then read as product defects; **a want column written as prose is a
  substring matcher** (I wrote one to check a proof *about* substring matching); **derive a denominator,
  never infer it**; **an inherited control whose constant becomes your token still passes while measuring
  the opposite arm**; **a regen that moves nothing is not evidence that nothing can move**; a scratch copy
  of a lock can be missing an entry and then its figures are wrong; **a ticket key can look like a
  generation prefix** (`KS1142`).
- 🔴 **ONE NEW MEASUREMENT FOR ITEM 2, and it widens the ticket:** comparing every tracked lock's two
  `@types` against `packages/shared`'s own (4.19.9 / 8.23.1), **15 of 28 Blockchain/Dev locks disagree,
  not the 11 KS 1380 names.** The four it does not name are **the workspace root**,
  `connectors/whatsapp-bot`, `services/shared` (esc only) and `services/vc-issuer` — and vc-issuer pins
  `@types/pg` **8.21.0**, so **there are THREE pg versions in play (8.23.1 / 8.21.0 / 8.20.0), not two.**
  Any "refresh the services to shared's versions" fix has to decide what to do with that third value, and
  the ticket's two-version framing does not cover it. **I built no service image**, so the failing set
  itself is still unmeasured and stays owed.
- **ITEM 1b needs no provenance work repeated:** I verified three `cmp` rc 0 equalities (READY fence ==
  canonical, canonical == `cat` of the two sections, canonical == the drafter's precheck golden) and the
  companion's index line naming the base blob, with a control at rc 1. Its branch name and subject are
  declared and already gated (75 declared / 83 landed).
- **The gate47 polish** is carried untouched, with the warning that N-1349-4/-5 must wait for Peter's #1351
  and the KS-1054 ones may only go on a branch built AFTER ITEM 1a's head.

## READY FOR THE GO
On a GO naming **Seat B 47th**: merge #1354, **then** file the two drafted tickets, **then** rebase ITEM 1a
onto the new develop, `cmp` the product bytes (never a `git diff` against a bare golden), re-run red-first
on macOS **and** `python:3.12-slim`, `chmod 755` `check-startup-migrations.sh` after the rebase and
re-read the mode from `git ls-tree` (trap 1), push, and ONE READY → gate48b.

## STATE
Shared checkout HEAD and local `develop` `37205947ddd2`, `.git/config` sha256 `4f624a213933d54b`,
untracked 17, no fetch or pull since the boot one you ruled on. No `.push-lock-*`. `df -m
/Volumes/DevMASTER` **513,467 MiB free** (74% used; 513,484 at boot). Docker: one image built
(`b47probe-issuer-frontend`), nothing removed, nothing pruned.
**Next audit fuse `2026-10-09T00:00:00Z`: 218.1 h, computed at 2026-09-29T21:56:32Z.**

```

## CLAUSE 4 — Wednesday's flag to Kam (0_Brain/dashboard/data/chat_wednesday.json, role wednesday, VERBATIM; 3 of 3 entries found)

- ts: 2026-09-30T07:31:59.902902+10:00 | TEXT_SHA256: d85fec471cae5784e814c0cb55b20e1049c163064bf5617f55887460cfea13c2

```
Kam, a flag, no action needed. I've accepted one new security advisory into the Secuura baseline, under your standing authority from 9 September.

It is GHSA-r53p, rated low, in undici: a build tool used only when building the issuer frontend. Tonight the seat built the issuer image and searched what it actually ships, with checks that could have found it: undici is not in it. It is in no backend service either. It joins twelve other undici rows already accepted on the same grounds, under KS-470.

One thing to know: your rule says to use the shared re-check date, and this baseline file has none; those twelve rows carry no expiry at all, so this one matches them. The real fix, which would clear all thirteen, forces undici up a major version. It becomes a follow-up ticket once it's measured.

The other new advisory, in js-yaml, gets fixed rather than accepted: a one-line lock update in a test tool.

Both new advisories were published yesterday, and until this lands they block every push on the repo, Peter's included.
```

- ts: 2026-09-30T07:32:16.856877+10:00 | TEXT_SHA256: ab9e7678389c5bfb351e7010993f375363e9b3520846ba05b6dd49e7fe8c7190

```
One precision on that flag: accepting it is my decision, and it's made. The baseline row itself isn't in the repo yet. It lands through one small PR this morning, after its QA gate passes, together with the js-yaml fix.
```

- ts: 2026-09-30T07:39:56.849252+10:00 | TEXT_SHA256: 3de2c06f1b8d264d11318ed2402ab13cb5ed7300664fc0eaaa23cb7054357d32

```
Kam, a correction to my undici flag earlier. I said the new row would carry no expiry, like its twelve siblings. That was wrong. Those twelve carry none only because they are on a grandfathered list, and adding to that list is a permanent acceptance your authority does not give me.

So the row expires on 9 October instead. That's the date four rows already share after your re-date: one re-check covering them all. The real fix, forcing undici up a major version, is ticketed and due by then. The seat measured the difference, and nothing had been committed.
```

