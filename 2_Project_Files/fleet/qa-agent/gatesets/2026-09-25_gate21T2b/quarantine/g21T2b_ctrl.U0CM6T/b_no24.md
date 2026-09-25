COMBINED CAPTURE (rebuilt 2026-09-25T05:20:59Z) for the round-21 SECOND tier-2 batch gate #1225 #1227 #1229 #1231 #1232: every READY mail naming one of the five, verbatim from the per-mail file named in its header. (Seat B 25th's mail also carries #1230, tier 1, NOT in this gate.)


######## mail_seatL1_ready_for_qa_4_seat_l1_1225_ks_1291_head_120420a2e_041458.md ########
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 4 (Seat L1): #1225 KS-1291 head 120420a2e, tier 2, legs 3/4/8 OWED + PROTOCOL-DIFF #3 FALSE (your 04:06 rule); 6 worktrees added lock-free; 4 PRs now open
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T04:14:58.000Z
MESSAGE_ID: <010001a0d6c60d9d-704aaee5-7d19-4a83-9085-c0144963f8ee-000000@email.amazonses.com>
CAPTURED: 2026-09-25T05:20:59Z by the gate21T2b drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 3fbede15fdbe1045cc5b50a990dd5cee96ae019e6d59606bbfafb04b39fd7efa
# READY FOR QA 4 (Seat L1): #1225 KS-1291 — tier 2, legs 3/4/8 OWED; PLUS PROTOCOL-DIFF #3 (false, and your 04:06 rule is exactly why)

## Part 1 — READY FOR QA 4

**1. PR** — **#1225**, `https://github.com/Secuura/Distributed_Secuura/pull/1225`.
**2. Head, read from ORIGIN in the same action** — `120420a2e7b1a0d10dd41ee4320f7e88bc1529c6`. Base develop
`6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
**3. Ticket comment naming the PR** — posted on KS-1291.
**4. Test Evidence** — originate `jest --runInBand` **74 / 863, rc 0**, identical to the bare serial
baseline, so removing the branch reddens nothing. `tsc --noEmit` rc 0. `packages/shared` **46 files / 918,
rc 0** on a re-run (first run: 4 repo-walk timeouts at load 10.15, no assertion failure; both runs recorded,
class owned by KS-1155).
**5. NOT covered** — legs **3, 4, 8** NOT run. **This PR has a route-handler surface, so they are OWED AT
THE GATE**: `POST /api/documents` with an `@`-carrying `issuerName` must still answer 400 BAD_REQUEST, now
from `:616`, with nothing saved. Integration config not run. No image rebuilt.

**The three arms** (full detail in the PR body): static — 0 assignments to the field, controls scoring 1 and
0, same brace depth; canary with its own control — early guard reds the E-01 cell (1 failed / 862), late
guard **863/863 green**, i.e. never reached; paired mutation on the post-removal tree — deleting the early
guard reds E-01. **Tier 2.**

## Part 2 — PROTOCOL-DIFF #3 on the same push: FALSE, and it is the case your 04:06:46Z mail describes

**The push landed: rc 0, origin holds `120420a2e…`, match=yes.** Verdict:
`PROTOCOL-DIFF — worktree ADDED/REMOVED (3/0) — an add or remove needs the lock, in any namespace`.
That message is my **v3** predicate, written when an add/remove still required the lock. Your 04:06:46Z mail
removed that requirement while this push was in flight. Attributing the five rows:

| row | worktree | namespace |
|---|---|---|
| ADDED | `s-b25-ks1110` | **s-b25** |
| ADDED | `s-b25-ks1140` | **s-b25** |
| ADDED | `s-l4-ks1252` | **s-l4** |
| changed | `s-l2-ks1171` | s-l2 (already attributed) |
| changed | `s-l3-ks1288` | s-l3 (already attributed) |

**5 rows, 0 not attributable to another seat.** Refs leg: `5 ATTRIBUTED, 0 DIFF`. Heads: `4 ATTRIBUTED,
0 DIFF`. **Nothing restored.**

**`push_protocol_l1v4.py` already implements your rule** and is wired into `pushL1v6.sh` for every push from
here. Another seat's add/remove is ATTRIBUTED; one outside every namespace, or in MINE, stays a DIFF.

### The controls — and a correction, because my first set of v4 controls was ALSO invalid
My first attempt replayed the KS-1266 snapshot against the live repo. **Every control came back DIFF,
including the untouched one**, because an hour of other seats' work had moved `config` and the refs — the
same stale-replay trap I reported to you at 03:34Z and then walked straight into. Those runs proved nothing.
Redone with a **test seam** (`PUSH_PROTOCOL_WT_AFTER`, the same precedent the script sets with
`PUSH_PROTOCOL_REPO`, printed whenever active) so BOTH sides of the comparison are fixed:

| control | verdict |
|---|---|
| both sides identical | no worktree reason at all |
| ANOTHER seat's worktree REMOVED | **ATTRIBUTED s-l3** |
| ANOTHER seat's worktree ADDED | **ATTRIBUTED s-l4** |
| an UNNAMESPACED worktree ADDED | **DIFF** |
| an UNNAMESPACED worktree REMOVED | **DIFF** |
| **MY OWN** worktree REMOVED | **DIFF** |

## Part 3 — your "build while you wait" instruction, taken up
Six worktrees created for D, E, F, G, H, I — **no lock taken** (L3 held it throughout and was untouched;
`.git/config` byte-identical; each at develop, clean, no upstream; the transient-`index.lock` retry was
built in and not needed — 1 attempt each). Deps installing. **D, E and F edits are already applied**, every
anchor unique; F's five stale citations now read 0 residual with `d4cf7e3cf` kept as the date of the past
measurement.

## Scoreboard
**4 PRs open and READY: #1219 KS-1277, #1221 KS-1266, #1223 KS-1118, #1225 KS-1291.** Every push landed rc 0
first attempt, keepalive held, no rc 141. 3 tickets Done with evidence, KS-1291 filed, KS-1155 evidenced
instead of duplicated.

## NEEDED-BY
Nothing.



######## mail_seatL4_ready_for_qa_2_seat_l4_1227_ks_1252_ks_1253_e7pref_044053.md ########
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 2 (Seat L4): #1227 KS-1252 + KS-1253 E7PREFIX — head 69a72726e, tier 2, 58/58 suites, spec findings identical base/head
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T04:40:53.000Z
MESSAGE_ID: <010001a0d6ddc695-c1977b10-a778-4241-8ce3-e382ebee9a2b-000000@email.amazonses.com>
CAPTURED: 2026-09-25T05:20:59Z by the gate21T2b drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 1f3b8723c2d906a74485ecb784231801535215bd99d8aad08550bb02e78ebc13
# READY FOR QA 2 (Seat L4): #1227 KS-1252 + KS-1253 E7PREFIX — head 69a72726e, tier 2

## BLUF
**PR #1227**, head **`69a72726e8eee0711a56b782d04936bf647e9160`**, base `develop`, **tier 2**, 2 commits,
**2 files**, +193/−2: `scripts/spec-examples/check/contract.mjs` (+18/−2) and a NEW
`scripts/__tests__/ks1252_1253_e7_prefix_guard.test.sh` (+175). An independent `ls-remote` after my
tool's own confirms origin holds my sha. Both tickets walked Backlog → In Progress on PR open and
**both attachments read `linkKind: contributes` on the FIRST read** — the body was swept for a closing
keyword adjacent to an id before publishing, after PR 1 taught me that. **Push rc 0 at 8m45s, first
attempt.** Its verify read PROTOCOL-DIFF on `refs/remotes/origin/develop` — reported separately, nothing
restored, and it does not touch this PR's content.

## The five artefacts

**1. What changed.** Two defects in E7 — the guard's only **name-blind** secret rule — plus the first
cells that pin it from the scripts side.
- **KS-1252** `582ab9e5e`: the ULID-ish entry was `/^(?:[a-z]+_)?[0-9A-Z]{20,32}$/`, an **unbounded,
  name-blind** prefix. Bounded to `{2,12}` with the same two name guards as `PREFIXED_UUID_RE`.
- **KS-1253** `69a72726e`: the deny list admitted **14** credential names because none *contains* a
  listed substring (`sess` is not `session`). All 14 now refused as **exact** prefixes.
- **The new suite exists because the only cells pinning these patterns lived in `packages/shared`** — a
  lane I must not touch — so the guard could only be proved from another workspace. Its 8 cells drive the
  guard's own exports from beside it and run through `run-shell-suites.sh`, i.e. **leg 14**.

**2. Red-proof — of the suite as well as of the fix.** Three trees:

| tree | result |
|---|---|
| base `6ab9d5021e96` | **6 passed, 2 failed** (rc 1) — both defect cells red, all 6 controls green |
| `582ab9e5e` (KS-1252 only) | **7 passed, 1 failed** — cell 1 green, **KS-1253's cell still red** |
| this head | **8 passed, 0 failed** (rc 0) |

The middle row is the independence check: each cell is bound to its own ticket and neither fix masks the
other.

**3. The declared NARROWING, and the two rows that forced it.** KS-1253 recommends an **ALLOW list** of
the 13 minted prefixes. Measured against `packages/shared/src/__tests__/ks256-spec-example-contract.test.ts`
before writing anything:

| candidate | ks256 rows | prefix table | `refused===['key']` | the 14 probed | spec's `anchor_…` |
|---|---|---|---|---|---|
| current — the control | 0 mismatches | 0 | OK | **14/14 admitted** | benign |
| **A — the ticket's allow list** | **2 mismatches** | 0 | OK | 0/14 | benign |
| **B — this PR** | **0** | 0 | OK | **0/14** | benign |

A reddens `['len12','abcdefghijkl_<v4>',false]` and `['credit','credit_<v4>',false]`. **KS-1253 stays
OPEN** for the allow list, with those two rows named on the ticket (comment
`d37b0576-a575-411a-b642-3e82c12af835`, byte-verified).

**4. Suites.** `run-shell-suites.sh` at this head: **`shell suites: 58 passed, 0 failed (of 58)`** — 57 at
the tip plus exactly the one this PR adds; **zero SKIP lines**; git-env line *"cleared for the suites:
(none were set) — of 15 repository-local name(s)"*. The guard itself:
`node scripts/spec-examples/check-spec-examples.mjs` **rc 0**, *"docs/openapi/secuura-api.yaml — 405
example blocks / OK — every published example resolves to the fixture set."*
`check-script-portability.sh` **rc 0** across 102 scripts. `deps-present.sh` rc 0.
**Published spec census, base vs this head:** 1,242 distinct tokens of 20+ chars; E7 fires on **6** at
base and the **same 6** here — **0 new, 0 lost**. Controls: the tokeniser finds a known spec value and
does not invent an absent one.

**5. Gate, verbatim, copied from the hook's output, not retyped.**
```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```
Per your ruling: **legs 3, 4, 8 NOT run (local stack not up); this PR changes a check's regexes and adds
a shell suite — no route, no served spec, no runtime config**, so nothing is owed at the gate for it.

## The push
| | |
|---|---|
| lock taken | 04:28:51Z, **poll 139, waited 706 s** behind Seat L2 — healthy, holder alive throughout |
| push | 04:28:52Z → 04:37:37Z, **rc 0 at 8m45s**, first attempt, no retry |
| origin | holds `69a72726e8eee0711a56b782d04936bf647e9160` == mine |
| config | `4cd3b01ca1e71947 -> 4cd3b01ca1e71947` **identical** — the baseline-after-the-lock fix working |
| lock released | 04:37:44Z, cool-off stamp written |
| stubs | 8 orphaned `login_stub` listeners cleared, **0 remaining** |
| verify | **PROTOCOL-DIFF** on `refs/remotes/origin/develop` only; config/worktrees/heads all IDENTICAL. Reported separately; nothing restored |

## Two defects in the new suite, fixed before it was committed
Both would have failed **inside the push hook** rather than here:
1. The probe used `import { … } from process.argv[2]` — **not valid ESM**; an import declaration takes a
   string literal, so it would have failed to *parse*. Now `await import(pathToFileURL(…).href)`.
2. Cell 0 asserted **44** rows where the probe produces **41**. The cell failed rather than accepting the
   miscount.

## NEXT
**PR 4** (`ed85bd81d`, KS-865 + KS-808 (3)) is pushing now; **PR 2** (`6320a61d8`, tier 1, KS-1127 +
KS-1089 + KS-1135, self-test 41/8 base → 49/0 head) follows, one push per lock take.

## VERIFIED BEFORE SENDING
- PR number, head, base, state, file list, +/− | GitHub REST | 2026-09-25
- origin holds the sha | an independent `ls-remote` after the push script's own | 2026-09-25
- both `linkKind: contributes`, both In Progress | Linear GraphQL | 2026-09-25
- every tally, rc, census figure | run in `worktrees/s-l4-ks1252` and in scratch trees | 2026-09-25
- the gate block | copied from `KS12521253-push1.out` | 2026-09-25

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25



######## mail_seatL4_ready_for_qa_3_seat_l4_1229_ks_865_ks_808_3_head_e_050019.md ########
SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 3 (Seat L4): #1229 KS-865 + KS-808 (3) — head ed85bd81d, tier 2, suite 3/4 base -> 7/0 head, verify PROTOCOL-CLEAN
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T05:00:19.000Z
MESSAGE_ID: <010001a0d6ef8eea-6baee6ce-a31c-4f61-b850-bdc43b73ff9f-000000@email.amazonses.com>
CAPTURED: 2026-09-25T05:20:59Z by the gate21T2b drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 7f7ff6fddacb483825103e9d0793e925be7cab0b0d37679f7c644fb78ea98332
# READY FOR QA 3 (Seat L4): #1229 KS-865 + KS-808 (3) — head ed85bd81d, tier 2

## BLUF
**PR #1229**, head **`ed85bd81d0acb137c89e1257d05ef9c72855086b`**, base `develop`, **tier 2**, 2 commits,
3 files, +190/−5. Independent `ls-remote` confirms origin holds my sha. Both tickets In Progress, both
attachments **`linkKind: contributes` on the first read**. Push **rc 0 at 11m46s, first attempt**, and
its **verify read PROTOCOL-CLEAN** — which also tells you my PR 3 diff was a transient cross-seat
tracking-ref write, not a standing fault in my tool.

## The five artefacts

**1. What changed.**
- **KS-865** `099f9fb6b` — `check-no-latest-tags.sh` advertised **six** files and could only ever read
  **five**; `[ -f "$f" ] || continue` skipped the sixth in silence while it printed `OK`. Now: a listed
  input that is missing is an `::error::`, the dead entry is gone with its history in a comment, and the
  verdict says `examined N of M advertised file(s)`.
- **KS-808 (3)** `ed85bd81d` — `run-migrations.sh` did not merely cite a missing tracker, it **asserted a
  fact about a file** in two lines it printed: *"BACKLOG.md marks it resolved"*. Those lines now cite
  **KS-1031** (which made the `exit 3` change) and **KS-808** (which still carries the `applied=N`
  defect). **BACKLOG.md is not edited** — it is in no seat's lane.

**2. The ticket's other fix option does not exist, and that is measured.** KS-865's Acceptance offers
*"or the path is corrected to the repo root"*. `git ls-tree -r` at `6ab9d5021e96` finds **no** file named
`deploy-staging.yml` anywhere. It existed at **both** paths and both were deleted:

| path | added | deleted |
|---|---|---|
| `Blockchain/Dev/.github/workflows/deploy-staging.yml` — what the script looked for | `4d908483f` | **`b2c70381a`** (KS-318, #332), **2026-06-25** |
| `.github/workflows/deploy-staging.yml` — repo root | `1e3600359` | `da98e25aa` |

Control: the same query for `.github/workflows/ci.yml` returns commits, so the instrument works. **The
entry is not mis-rooted — its target is gone.** The other five all resolve at the tip. The only loosening
is removing an entry that could never be read; every readable input is now mandatory.

**3. KS-808's claim is false, measured.** Against `BACKLOG.md` at the tip (1,234 lines), fixed strings:
`BACKLOG #6` **0** · `run-migrations` **0** · `migration runner` **0** · `partial-failure` **0** ·
`partial failure` **0** · `exit semantics` **0** · `service_completed_successfully` **0**. Controls:
`Where:` **41** present, a nonsense term **0** — the search discriminates. Verified after the fix: the
script's `echo` lines name BACKLOG **0** times at this head and **2** at base; the single remaining
mention is inside a `#` comment recording what was removed.

**4. Red-proof and suites.** New `scripts/__tests__/check_no_latest_tags.test.sh`, 7 cells, under
`/bin/bash` 3.2.57:

| tree | result |
|---|---|
| base `6ab9d5021e96` | **3 passed, 4 failed** (rc 1) — both defect cells, the count-varies control, and the list control naming **line 7 of `CHECK_FILES`** |
| this head | **7 passed, 0 failed** (rc 0) |

Cell 3 is what makes the count real: **5** on a complete tree and **4** with one file deleted, so
`examined N of M` cannot be a hard-coded string. Cells 4 and 5 keep what the gate is for — a real
`:latest` still reds it, and a `:latest` on a comment line is still ignored, so cell 4 cannot pass by the
comment filter breaking.
`run-shell-suites.sh`: **`shell suites: 58 passed, 0 failed (of 58)`** — 57 at the tip plus exactly the one
this PR adds, zero SKIP lines. `check-script-portability.sh` **rc 0** across 102 scripts.
`deps-present.sh` rc 0.

**Disclosed — cell 6's first version was wrong and the cell caught it.** It grepped the **whole** subject
for `deploy-staging.yml` and reddened on the explanatory comment I had just added. The comment is the
point, so the cell now asserts about the `CHECK_FILES` **block** and additionally *requires* the comment
to be present.

**Also disclosed — KS-808 has no cell, and I am not pretending otherwise.** Its fix is a comment and two
`echo` strings; the check that matters is the BACKLOG.md measurement above, which is a property of that
file rather than of the runner. A cell asserting "the runner does not print the word BACKLOG" would pin a
spelling, not a defect. And **`run-migrations.sh` is exercised by no suite in this round** — it needs a
live PostgreSQL and a compose stack. The change has no control-flow edit, `bash -n` passes and `exit 3`
is untouched; that limit is stated rather than papered over.

**5. Gate, verbatim, copied from the hook's output.**
```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```
Per your ruling: **legs 3, 4, 8 NOT run (local stack not up); neither script has a route, spec,
served-spec or runtime-config surface**, so nothing is owed at the gate for this PR.

## The push
| | |
|---|---|
| lock taken | 04:46:42Z, after the 90-second cool-off from my previous release |
| push | → 04:58:28Z, **rc 0 at 11m46s**, first attempt, no retry |
| origin | holds `ed85bd81d0acb137c89e1257d05ef9c72855086b` == mine |
| config | `4cd3b01ca1e71947 -> 4cd3b01ca1e71947` **identical** |
| verify | **PROTOCOL-CLEAN** — *"first push: tracking ref added at origin's head"* |
| lock released | 04:58:58Z, cool-off stamp written |
| stubs | 8 orphaned `login_stub` listeners cleared, **0 remaining** |

## NEXT
**PR 2** (`6320a61d8`, **tier 1**, KS-1127 + KS-1089 + KS-1135) is pushing now — the last of the four.
Self-test **41 passed / 8 failed at base → 49 passed / 0 failed at this head**, with the controls holding
at both ends.

**Still open from my PROTOCOL-DIFF mail:** all four PRs are built on `6ab9d5021e96` and develop has moved
several commits past it. Pushing is unaffected and all three open PRs read `mergeable: True`; **merging**
is what needs your call — heads as given, or develop merged in first with new heads and a re-gate.

## VERIFIED BEFORE SENDING
- PR number, head, base, file list, +/−, mergeable | GitHub REST | 2026-09-25
- origin holds the sha | an independent `ls-remote` after the push script's own | 2026-09-25
- both `linkKind: contributes`, both In Progress | Linear GraphQL | 2026-09-25
- the deletion history of both `deploy-staging.yml` paths | `git log --diff-filter=A/D` per exact path, with a positive control | 2026-09-25
- the BACKLOG.md census and its two controls | fixed-string greps at the tip | 2026-09-25
- the gate block | copied from `KS865808-push1.out` | 2026-09-25

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25



######## mail_seatB25th_pushed_ready_3_4_5_seat_b_25th_1230_ks_1131_1231_k_051544.md ########
SUBJECT: [Secuura/Blockchain -> Wednesday] PUSHED + READY 3/4/5 (Seat B 25th): #1230 KS-1131, #1231 KS-1281, #1232 KS-1128 — ks1128 verify rc 3 ATTRIBUTED to Seat L1's -l1- namespace, nothing restored
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T05:15:44.000Z
MESSAGE_ID: <010001a0d6fdaeb1-613ac7c0-0e6c-4e27-abfa-dcfde8ba3742-000000@email.amazonses.com>
CAPTURED: 2026-09-25T05:20:59Z by the gate21T2b drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: f6e44ef8227974e94f960c7fa0b1629dd6bb8ede7ece68b4eaf8da21bf34f7a8
# PUSHED + READY FOR QA 3, 4, 5 (Seat B 25th): #1230 KS-1131, #1231 KS-1281, #1232 KS-1128. Plus one ATTRIBUTED protocol diff — nothing restored.

## BLUF
All three Ornith branches are at origin at exactly the committed shas, and three PRs are open. **ks1128's push-protocol verify returned rc 3 (PROTOCOL-DIFF); both attribution legs pass and it is Seat L1's namespace, so it is ATTRIBUTED, not a diff. I restored nothing.** The other two verified PROTOCOL-CLEAN.

## The ATTRIBUTED diff — leg (a) and leg (b), as you and L1 specified
The snapshot saw **4 refs change** during my ks1128 window and **4 worktree HEAD moves**:
```
~ feature/ks-1133-verify-alias-order-spec-l1-d-1       6ab9d5021 -> 6892124d9
~ feature/ks-1158-stale-header-lines-l1-f-1            6ab9d5021 -> 0f3ffbb09
~ feature/ks-1229-version-truthy-cell-l1-e-1           6ab9d5021 -> cfa16eb70
~ feature/ks-1263-share-transfer-transaction-l1-g-1    6ab9d5021 -> 42c20e998
```
- **leg (a): every one carries `-l1-`, i.e. Seat L1's namespace.** 4 of 4 attributable, 0 unattributable, none in mine.
- **leg (b): origin holds MY sha** — `at-origin=ec0d7efcf682… expected=ec0d7efcf682… match=yes`.
- The 4 worktree HEAD moves are those same four branches' own worktrees (count matches exactly). My own tracking ref was ADDED at my sha; `heads IDENTICAL (336)`.
- **Corroboration that this is L1 working, not damage:** none of those four branches is at origin yet — they are LOCAL commits in L1's own namespace, which your 2026-09-25 ref-scope mail allows at any time without the lock. That is precisely the case your coordination said my tool cannot yet distinguish.
**NOTHING RESTORED.** The snapshot at `raise/pushq-ks1128` is the record; `raise/ks1128-attribution.txt` holds the attribution run.

## The lock, measured
ks1128 waited **730 s across 129 polls** at the 5 s rate before taking it, then held it **12 min 4 s** for one push and wrote the cool-off stamp (`1790313066`). The queue cycled through L1, L2, L3 and L4 throughout; every holder pid was alive at every poll and **I never touched the lock dir**. Total wait for the three pushes was about **70 minutes**. Rule 1 held: one push per take, re-queue between.

## READY FOR QA 3 — #1230 KS-1131 CALLSHAPED (tier 1)
1. **PR** #1230, base `develop`, `Refs KS-1131`, Linear `linkKind=contributes` verified.
2. **Head read at origin in the same action:** `1116dab0466da48ce96c4811f8086b061a49aa70` == the commit. Push PROTOCOL-CLEAN.
3. **Ticket comment:** to follow on your word — say if you want one now or at the GO, since the round's comments-are-facts rule means I would be repeating the PR body.
4. **Test Evidence:** auth **bare 828/828 over 76 files -> patched 832/832**, `tsc` rc 0 both sides. **Red-proof one arm per conjunct: A both RED (1ms, 3ms) / B only F-B RED (3ms) / C all green**, arm C byte-identical (`cmp` rc 0) to the commit. Per-stage blobs asserted (`560bb49c242f`/354, `041396c7fce5`/381).
5. **NOT covered:** legs 3/4/8 NOT run (local stack down; no such surface). The residual is **MEASURED in both directions** rather than left UNVERIFIED — a comment with a paren inside the `!user` block still false-greens property 1, and the same shape in the gap false-reds. Items 3 (F-C) and 4 (P2) of the ticket remain open; `:218` untouched; `:206` kept.

## READY FOR QA 4 — #1231 KS-1281 EXISTENCECHECK (tier 2)
1. **PR** #1231, base `develop`, `Refs KS-1281`, `linkKind=contributes`.
2. **Head at origin:** `bd1d2daec2bf1b934437eae19c6239fe257305a6` == the commit. PROTOCOL-CLEAN.
3. Ticket comment as above.
4. **Test Evidence:** vc-issuer **bare 127/127 over 12 files -> patched 129/129 over 13**, `tsc` rc 0 both sides; red-first 1-of-2 at the tip, 2-of-2 after; blobs `8a46bbf7f0d5`/261 and `125b65f81aaf`/46. Covers the ticket's **second** shape (an existence check), stated as such in the body.
5. **NOT covered:** legs 3/4/8 NOT run. **No database touched**; a DB not built by migration 001 now falls back to memory on first store; **whether the least-privilege role can SELECT the table on every environment is NOT measured** (`provisionAppRole` read, not probed). §5f applies — Done waits for your closing pass after a kintsugi log observation.

## READY FOR QA 5 — #1232 KS-1128 SEEDWARN (tier 2)
1. **PR** #1232, base `develop`, `Refs KS-1128`, `linkKind=contributes`.
2. **Head at origin:** `ec0d7efcf682112639505cf45baec71b899b665f` == the commit. Verify rc 3, **ATTRIBUTED above**.
3. Ticket comment as above.
5. **NOT covered:** legs 3/4/8 NOT run. **No real PostgreSQL** — the ticket's own instrument; this proves the arm with an in-process fake pg, stated in the body. The `:1142` inner catch is the same class, not in the ask, untouched. No image built, so the WARN is unobserved in a real boot log.

## Two care points from writing the bodies
- **`KS-963` was in my first draft of #1230's body.** It is **Done and ARCHIVED**, so a hyphenated key there would have attached this PR to an archived ticket. Caught by scanning before opening; the body now says `ks963` un-hyphenated, as your own subject does. **Verified after: KS-963 holds only its three historical PRs (970, 913, 907) and gained nothing from mine.**
- Closing keywords scrubbed from all three bodies. One `resolve` survives inside a code span — `` `Module.createRequire(PRODUCT).resolve('pg')` `` — a real API name, so renaming it to satisfy a scanner would be worse than leaving it.

## State
KS-1140 and KS-1110 are committed and unpushed (next lock take, after my 90 s cool-off). develop `ecb1aa75aefa`. Nothing deployed. **Item 1, the two re-dates, still unbuilt and still Kam's own word.**
**Next wake:** the KS-1140/KS-1110 push, which I start now as a background job.

