COMBINED CAPTURE (rebuilt 2026-09-25T03:22:33Z) for the round-21 tier-1 batch gate #1213 #1214 #1216 #1217: every READY FOR QA mail naming one of the four, verbatim from the per-mail file named in its header.


######## mail_seatB25_ready_for_qa_1_seat_b_25th_1213_ks_530_patchline_h_021019.md ########
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 1 (Seat B 25th): #1213 KS-530 PATCHLINE — head f2751859c, tier 1, audit-locks 24->22 frozen at 09-30
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T02:10:19.000Z
MESSAGE_ID: <010001a0d653eb51-b0d02189-73df-40c2-844d-e010324ce338-000000@email.amazonses.com>
CAPTURED: 2026-09-25T03:21:04Z by the gate21T1 drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 2599974473ca578556a536986deb14ea0877c2c594fa9b48bb60ce3f20fdeaa6
# READY FOR QA 1 (Seat B 25th): #1213 KS-530 PATCHLINE — tier 1

## The five standing items

**1. PR number** — **#1213**, `https://github.com/Secuura/Distributed_Secuura/pull/1213`, base `develop`, 3 files, `Refs KS-530`, Linear `linkKind=contributes` verified on the attachment.

**2. Head read from origin in the same action** — GitHub says `head=f2751859c01565df066a3cdbe008e7360de4205a`; `git ls-remote origin refs/heads/feature/ks-530-…-r21-patchline-1` in the same call reads **`f2751859c01565df066a3cdbe008e7360de4205a`**. Equal. `mergeable=True`, `mergeable_state=unstable` — which carries no testing claim (KS-660).

**3. Ticket comment naming the PR** — `6758d94b-e3a0-4285-9ff9-718487f81707` on KS-530, read back by id and **byte-equal**. Facts only, no seat named. *(Note: the Linear integration moved KS-530 Backlog → In Progress on branch/PR creation. That is the integration, not a state move by me.)*

**4. Test Evidence — run by me, at this head**
- **`audit-locks` frozen at 2026-09-30T00:00Z: `GHSA-frvp-7c67-39w9` no longer lapses.** Advisory matches **24 → 22**. Freeze = a `Date` preload outside the repo, replacing the whole constructor (in V8 `new Date()` bypasses a patched `Date.now`, so a `Date.now`-only patch would have been a check that could not fail). Controls: with the preload the repo's own `utcToday()` reads `2026-09-30`, without it `2026-09-25`, and `new Date('2020-01-02T03:04:05Z')` still honours its argument.
- `audit-locks` **bare: rc 0.**
- Independent second instrument: the repo's own `isLapsed()` with an explicit date — 0 lapsed at 09-29, exactly 3 at 09-30, 5 at 10-02; boundary, never-expiring and malformed controls all correct.
- **In-hook push preflight, 12/15 legs, zero FAIL-shaped lines.** Leg 2 lockfile clean-room: **all 35 standalone locks pass `npm ci --dry-run`**, with `services/mcp-server` and `services/originate` both in the covered list. Leg 5 audit-contract **59/59**. Leg 6 npm-audit gate **26 reported / 26 baselined, OK**. Leg 7 standalone-lock advisories **22 match, 22 baselined, OK**. Legs 1, 9, 10, 11, 12, 13, 14, 15 OK.
- **Scope, per lock: added 0 / removed 0 / version-changed 1.** Platform discriminators unchanged: `mcp-server` `libc 10→10, os 53→53, cpu 52→52`; `originate` `os 27→27, cpu 26→26`.
- Each lock proved self-consistent: an isolated resolution pass over it moves 0 versions.
- Push protocol: **PROTOCOL-CLEAN — first push: tracking ref added at origin's head**, worktrees IDENTICAL, heads IDENTICAL, 4 leaked `login_stub` listeners cleared, 0 remaining. Lock `worktrees/.push-lock-21` taken `01:49:22Z`, released `01:56:03Z`.

**5. What is NOT covered**
- The preflight's own verdict: **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`** and it prints `This is NOT a pass. Do not quote it as one — say which legs ran.` Skipped: **leg 3** spec-auth conformance, **leg 4** path resolvability, **leg 8** served-spec consistency — each `SKIP — local stack not up on http://localhost:6882`. None touches a lockfile.
- **No runtime booted on the new pin, no image built.** "It reaches a runtime image" is measured from the lock's PROD flag plus the Dockerfile's `--omit=dev`, not from an image inspect. A behaviour change in the library between 1.19.11/1.19.14 and 1.19.17 would not be caught here.
- Whether `originate`'s **devOptional** copy survives into its image is **not measured**.
- The four platform suites were not run — no service source, spec or route changed.
- **The root-lock residue is not cleared and the baseline row is NOT removed**, correctly: the workspace-root lock still reports the advisory through `@prisma/dev`'s nested 1.19.11, which no lock-only route moves. Kam's card `secuura-audit-root-lock-0930-remeasured`.

## Batch and the GO string
Tier 1. Per your ruling 2 the batch is the **five** PRs that do not depend on another's squash, gated together, with **KS-729 second on its merged-in head**. Two of the five are up (#1213, #1214); the three Ornith PRs follow. **I will send the tier-1 batch tree with READY 5, once all five heads exist** — a batch tree over two of five would not be the tree the GO acts on. Expected GO shape: `GO: merge #1213, #1214, #<o1>, #<o2>, #<o3> batch`.

## Merge exposure
Merging makes dependabot **#575** and **#949** dirty — both touch `services/originate/package.json`. Neither touched.

## State
Nothing merged, no ticket state moved by me, nothing deployed. Shared checkout `3bad652d1`, 17 `??` / 0 non-`??`. Lock FREE.



######## mail_seatB25_ready_for_qa_2_seat_b_25th_1214_ks_528_dompatch_he_021021.md ########
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 2 (Seat B 25th): #1214 KS-528 DOMPATCH — head 6fce4d0b1, tier 1, the ONE authorised baseline edit on the gate's own CLEANUP line
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T02:10:21.000Z
MESSAGE_ID: <010001a0d653f637-bab9981f-c9f3-47bf-9313-f630770787af-000000@email.amazonses.com>
CAPTURED: 2026-09-25T03:21:04Z by the gate21T1 drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 66e78854f4a992ba2d8f88792aea2f397f43b8e5bb7037c4b282f9e84691f4d9
# READY FOR QA 2 (Seat B 25th): #1214 KS-528 DOMPATCH — tier 1, and it carries the round's ONE authorised baseline edit

## The five standing items

**1. PR number** — **#1214**, `https://github.com/Secuura/Distributed_Secuura/pull/1214`, base `develop`, 5 files, `Refs KS-528`, Linear `linkKind=contributes` verified on the attachment.

**2. Head read from origin in the same action** — GitHub says `head=6fce4d0b188655a520e97447d3bfb1749d22a435`; `git ls-remote origin refs/heads/feature/ks-528-…-r21-dompatch-1` in the same call reads **`6fce4d0b188655a520e97447d3bfb1749d22a435`**. Equal. `mergeable=True`, `mergeable_state=unstable` — no testing claim in that field.

**3. Ticket comment naming the PR** — `a09d760e-d589-42e1-ad9b-398bf4bf1938` on KS-528, read back by id and **byte-equal**. It states in terms that this PR does not complete the ticket.

**4. Test Evidence — run by me, at this head**
- **The baseline removal is authorised by the repo, in that order.** With the four locks updated and the row still present, `audit-gate` printed, verbatim: `CLEANUP (advisory): 1 baseline entry is no longer reported - remove:` / `  - GHSA-jjmj-jmhj-qwj2 (react-router-dom, KS-528)`. **Only then** was the row deleted — **0 insertions / 7 deletions**, that one member.
- After the removal: `audit-gate` **bare rc 0, 25 distinct advisories reported, 25 baselined, no CLEANUP line.** Frozen at 2026-09-30: `GHSA-jjmj` **absent from the lapse list**. `audit-locks` frozen: matches **24 → 23**.
- **`npm run audit:contract` — the validator both gates import — 59 pass, 0 fail, rc 0.** The edited baseline satisfies every field rule.
- **The two rows expiring 2026-10-02 verified still present by name** after the edit (`GHSA-wrjc-x8rr-h8h6`, `GHSA-337j-9hxr-rhxg`).
- **In-hook push preflight, 12/15 legs, zero FAIL-shaped lines.** Leg 2 lockfile clean-room: **all 35 standalone locks pass `npm ci --dry-run`**, all three frontend locks in the covered list. Leg 5 **59/59**. Leg 6 npm-audit gate **25 reported / 25 baselined, OK**. Leg 7 **23 match, 23 baselined, OK**. Legs 1, 9, 10, 11, 12, 13, 14, 15 OK.
- **Scope, per lock: added 0 / removed 0 / version-changed 3** in all four — the two router packages plus their shared `@remix-run/router`. Platform discriminators unchanged: issuer `libc 13→13`, root `os 112→112, cpu 110→110, devOptional 84→84`, admin and verifier `os 26→26, cpu 26→26`.
- Each spliced lock proved self-consistent: an isolated resolution pass over it moves 0 versions.
- Push protocol: **PROTOCOL-CLEAN — first push: tracking ref added at origin's head**, worktrees IDENTICAL, heads IDENTICAL, 4 stubs cleared / 0 remaining. Lock taken `01:56:15Z`, released `02:05:34Z`.

**5. What is NOT covered — the gap here is real and I am naming it first**
- **No frontend was built and no browser was driven.** `react-router-dom` is client-runtime code in all three portals; nothing in this PR proves they still route correctly on 6.30.6. A vite build plus a real-browser pass on issuer, admin and verifier is the check this PR does not carry. If the gate wants that before a GO, say so and I will run it.
- The advisory's own open-redirect/XSS behaviour was **not reproduced** either way. The evidence is the published affected range and the pin.
- The three portals' unit suites were not run — no source or test file changed, which is a reason, not a result.
- Preflight verdict: **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`** Skipped: legs **3**, **4**, **8**, each `SKIP — local stack not up on http://localhost:6882`.
- The four platform suites were not run — no service source, spec or route changed.
- **This PR does not complete KS-528.** The other two rows need `react-router` **7.18.0**; no v6 release reaches it. They expire **2026-10-02**, five days after the row removed here. `Refs` for exactly that reason.

## One thing worth your eye
KS-528 already carried an attachment from **PR #1025** *"KS-528: re-date react-router audit rows 11 and …"* — which is where the "rows 11 and 12" numbering in the brief comes from. That PR re-dated the two rows this PR leaves alone, so the two changes do not overlap.

## Batch and the GO string
Tier 1, in the five-PR batch. **The batch tree comes with READY 5**, when all five heads exist. Expected GO shape: `GO: merge #1213, #1214, #<o1>, #<o2>, #<o3> batch`. **KS-729 is second, on a head that already contains this PR's squash**, per your ruling 1.

## Merge exposure
Merging makes dependabot **#572, #575, #635, #639, #649, #945, #946, #947, #948, #949** dirty — all ten touch `Blockchain/Dev/package-lock.json`. None touched.

## State
Nothing merged, no ticket state moved by me, nothing deployed. Shared checkout `3bad652d1`, 17 `??` / 0 non-`??`. Lock FREE.



######## mail_seatL2_ready_for_qa_1_2_seat_l2_1216_ks_975_head_c44b15dd_031447.md ########
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 1+2 (Seat L2): #1216 KS-975 head c44b15ddd, #1217 KS-976 head e83f34447, both tier 1, legs 3/4/8 OWED; KS-1171 census frame clean (no outside importer); a stale line-pin in Seat B's api-gateway file
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T03:14:47.000Z
MESSAGE_ID: <010001a0d68ef1cc-b3781fa9-3dde-4918-b9b9-0ab9d1062fba-000000@email.amazonses.com>
CAPTURED: 2026-09-25T03:21:04Z by the gate21T1 drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 61cc391ba6e936f3db241dc3efefa6876f00a5925b5e26602234b6687ca7a9a8
# READY FOR QA 1 + 2 (Seat L2) — #1216 KS-975, #1217 KS-976. Plus the KS-1171 census frame, enumerated.

## READY FOR QA 1 — #1216, KS-975 item 2, TIER 1
1. **PR:** #1216 · 2. **Head, read from ORIGIN in the same action:**
   `git ls-remote origin refs/heads/feature/ks-975-…-l2-scopenull-1` -> **`c44b15dddaddac3dec1d4deff224efd01b7565f2`**,
   and GitHub reports the identical head for #1216. Base `develop`.
3. **Ticket comment:** `ad9b5705-6331-42b2-98a3-7806e537fec0`, read back **byte-equal (1473)**. KS-975 stays
   **In Progress**; Linear `linkKind = contributes`, never a closing word.
4. **Test Evidence:** `services/security` **229/229 (21 files) -> 237/237 (22 files)**, +8 cells, 0 failures
   either side, BARE and SERIAL. `tsc --noEmit` rc 0 both. Red proof **4 failed / 4 passed at develop -> 8/8**,
   taken with the module still LOADING (product bytes reverted from the object store, not the file deleted).
5. **NOT covered:** legs **3/4/8 OWED at the gate** — `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED.
   Nothing failed.`, three identical `SKIP — local stack not up on http://localhost:6882` lines. Four
   platform suites not run. The arm is **not reachable at the wire** (the schema refuses `null` first).

## READY FOR QA 2 — #1217, KS-976 item 1, TIER 1
1. **PR:** #1217 · 2. **Head from ORIGIN:** **`e83f344474028215ae827b2f74fd3a06566d4c23`**, matching
   GitHub's head for #1217. Base `develop`.
3. **Ticket comment:** `bf3f5eb5-5363-4eb4-8d67-ddaea133b0b2`, byte-equal (2160). In Progress; `contributes`.
4. **Test Evidence:** **229/229 (21) -> 239/239 (22)**, +10 cells, 0 failures either side. `tsc` rc 0 both.
   Red proof **4 failed / 6 passed at develop -> 10/10**, helper module present so the file loads, only the
   CALL SITE reverted. Cells assert the message **TEXT**, not the status.
5. **NOT covered:** legs **3/4/8 OWED at the gate** (this changes a response message on a live route); four
   platform suites not run. `docs/openapi/` untouched — `'Key required'` is in **0** files under `docs/`
   while the route itself is present, so that check discriminates.

Both PR bodies carry the ticket-text corrections you asked for: `:1358 -> :1476`, and KS-976's stale
`must not be blank` with the KS-974 `.trim()` cause and the KS-974 comment id.

## KS-1171 — YOUR CENSUS CONDITION: the FRAME is enumerated, and it is clean
`git grep -l` over develop, not memory. Importers of `anchorSubmission`: 6 anchoring test files,
`anchoring/src/cardano/index.ts`, `anchoring/src/index.ts`. Importers of `cardano/confirmation`:
2 anchoring test files, `anchorSubmission.ts`, `cardano/index.ts`. Control: `waitForConfirmation` names 11 files.

**Two hits landed OUTSIDE `services/anchoring`, and I checked both rather than reporting a STOP on a grep:**
- `docs/REMAINING-BUILD-PLAN.md:386` — a markdown **table row**.
- `services/api-gateway/src/__tests__/ks1057-verify-confidence-is-status-aware.test.ts:29` — a **comment**.
  Its import block (lines 67-72) is vitest, express and node only. **It does not import anything of mine.**

So **neither is an importer**, the census frame stays entirely inside `services/anchoring`, and there is no
STOP. I will run the census at the patched product with **no test edits**, across the anchoring suite, and
report file:line / old / new / CONTROL-labelled as a table before rewriting anything.

## A FINDING IN SEAT B 25th's FILE — reported, not touched
That api-gateway comment pins line numbers in MY file:

    // every writer of the anchor row's `block_number` (anchorSubmission.ts:179, :254, index.ts:1734, :1744)

**Both pins are already wrong at develop, before my change.** Measured: the real `blockNumber` writers in
`anchorSubmission.ts` are **`:271`, `:405`, `:413`** (plus the type at `:138`). Line **`:179`** is a prose
comment about the wallet mutex; line **`:254`** is `});`.

My KS-1171 patch inserts the two exported constants before `export interface AnchorSubmissionDeps`
(**line 151**), so every real writer shifts by roughly +8 and the comment becomes *more* wrong. It is
`services/api-gateway/` — **Seat B 25th's file** — so I have changed nothing and am naming it instead.
**Ask:** ticket it, hand it to Seat B 25th, or leave it. My view: it is the line-number-pin class, worth a
ticket once the round is clear, and not worth blocking anything now.

## STATE
ks1129 `9c2021ba3` still queued — **533 s, 105 polls, 3 distinct holders (L3, L4, L1), all healthy**, no
bound while healthy. The 5 s poll is doing its job: 105 polls where the 60 s poll managed 9 in 481 s.
Nothing merged, no deploy, demo untouched.

