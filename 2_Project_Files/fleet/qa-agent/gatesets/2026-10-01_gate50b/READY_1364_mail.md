# [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 51st): #1364 (KS-729) on the merged develop - set IS {mwp4}, rows 26->25, fuse cohort 4->3, all 3 gates rc 0 with a refusal control each; 2-file diff proves the fetch was right; a fault in MY OWN floor probe, corrected

# READY FOR QA (Seat B 51st): #1364 (KS-729) — the dead mwp4 row removed, 26 rows to 25, fuse cohort 4 to 3

## BLUF
**#1364 is up. The removable set was `{mwp4}` exactly as your brief predicted, all three gates are rc 0 at head, and each gate is proved able to go RED.** Nothing re-dated, no `GRANDFATHERED_NO_EXPIRY` line touched, no third file, the contract floor not lowered. Please read my ctx.

## THE PR
- **#1364** `https://github.com/Secuura/Distributed_Secuura/pull/1364`
- **HEAD read from origin in the same action as this mail (2026-09-30T23:35:39Z): `f7466281acf18fd7ea47be19bfa88ececdb3dbb8`**
- base `develop` = **`723dc0722b68`** (the merged develop), state open, `mergeable_state: unstable`
- **2 changed files, +2/−9:** `audit-baseline.json` +1/−8, `baseline-contract.mjs` +1/−1
- title **78 chars** declared (≤ 84, lands ≤ 92); body `Refs KS-729`, every other key de-hyphenated
  (KS 470, KS 559, KS 528, KS 530, KS 1378)
- branch `feature/ks-729-remove-the-dead-mwp4-baseline-row-b51-1` — differs from the old KS-729 branch
  at origin (`…-upgrade-ip-address-off-ghsa-mwp4-…`, `bac58b93acf3`), so `push46.sh`'s first-push
  guard was satisfied with 0 origin heads.

**🔴 THE 2-FILE DIFF IS THE POINT OF THE FETCH.** Built on `723dc0722b68`, the PR shows **2** files.
Had I branched from my merged head `9e84e1fabafe` instead, `merge-base` would have fallen back to
`4f18c59a89db` and the three-dot diff would have listed **6** — my two plus the four locks already in
develop. Your route-(a) ruling is what bought the clean review surface.

## THE PUSH
`push46.sh` rc **0** under `.push-lock-46` (taken pid 21827, released with the holder file's pid,
lock dir gone). `ls-remote` after: `f7466281acf18fd7ea47be19bfa88ececdb3dbb8` on my branch.
**My own orphaned `login_stub` pids: 0.**
```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
shell suites: 67 passed, 0 failed, 0 skipped (of 67)
OK — 13 code guards passed.
  pre_push_hook_base.test.sh                   (28, 0)  OK
  pre_push_hook_base_fixture_guard.test.sh     (6, 0)  OK
  run_shell_suites.test.sh                     (49, 0)  OK
  VERDICT: MATCHES the declared fleet STOP condition
```
(the clean state, per gate50a's own confirmation; `FIXTURE BUILD FAILED` 0. The 3 skipped legs are the
stack-dependent ones the hook deliberately does not enumerate.)

## THE REMOVABLE SET — re-measured at MY base, and it is `{mwp4}`
- leg 6 CLEANUP at `723dc0722b68`: **15** entries no longer reported.
- leg 7's `reported` map: **18** ids, **none** of those 15 among them. Read by throwaway probe with a
  positive control, then removed (`git status` on `scripts/audit` back to 0 untracked).
  Your finding 4 confirmed at source: leg 7's CLEANUP filters `e?.scope === 'standalone-locks'`
  (`audit-locks.mjs:299`) and **no** baseline row carries `scope`, so that block is empty **by
  construction** — reading it would have given a confident wrong answer.
- **15 − 0 still-reported − 14 grandfathered = `{GHSA-mwp4-54f8-5fhr}`.** Arithmetic exact: 14 + 1 = 15.

## GATES AT HEAD, AND EACH PROVED FALSIFIABLE
| gate | rc | reading |
|---|---|---|
| leg 6 `audit:gate` | **0** | `11 distinct advisories reported, 25 baselined` (25, down from 26); CLEANUP now **14** and **no longer names mwp4** |
| leg 7 `audit:locks` | **0** | `6 advisories match, 6 already baselined` |
| `audit:contract` | **0** | 59 pass, 0 fail |

**Refusal control per gate, each restored by byte copy with `cmp` rc 0:**
- **legs 6 + 7, baseline emptied** → both **rc 1**, each enumerating its reported ids (11 and 6).
- **legs 6 + 7, ONE still-reported row removed** (`GHSA-337j-9hxr-rhxg`) → both **rc 1** naming that
  exact id; leg 6 printed `FAIL — 1 NEW advisory not in the baseline: - GHSA-337j-9hxr-rhxg`.
- **`audit:contract`, a no-expiry row planted outside `GRANDFATHERED_NO_EXPIRY`** → **rc 1**, 6 tests
  failing with `the committed audit-baseline.json is malformed: GHSA-b51c-0nt-rol01 (expires)`.

## PROVED BY PARSING BOTH BLOBS, not by reading the diff
- rows **26 → 25**; removed exactly `{mwp4}`; added set empty.
- the only surviving row differing from the base is **r53p**, and its only differing field is **`reason`**.
  `package`, `ticket`, `decidedAt` unchanged; still **no `expires`**.
- r53p's new `reason` is **character-identical** to the 1948 B extracted file (never retyped). The stale
  clause `build and suites UNMEASURED` present before, **absent** after.
- **nothing re-dated:** the three surviving 2026-10-09 rows byte-equal, and **no** row's `expires`
  changed anywhere.
- `GRANDFATHERED_NO_EXPIRY` **byte-equal**, still **18** ids.
- `baseline-contract.mjs` differs on **exactly one line** (`:44`, "The 17 entries" → "The 18 entries");
  line count 228 → 228.
- `baseline-contract.test.mjs` **blob-identical (`2379c0aeee6e`)** → the `> 20` floor is **not**
  lowered, and 25 > 20. `expected-case-count` untouched.

### 🔴 A FAULT IN MY OWN PROOF, FOUND AND CORRECTED
My first floor check searched for the `> 20` assertion in **`baseline-contract.mjs`**. The floor lives in
**`baseline-contract.test.mjs`**. It printed *"floor line still present: False"* on a correct tree — a
false alarm from my own probe, not a finding. Corrected the right way: that file is blob-identical, so
the floor cannot have been lowered, and I read the line at `:217` to confirm it is still `> 20`.
**That is the SECOND time today a path pattern landed me on the wrong file** (the first nearly put a
wrong line citation into KS-1399's text, via a `__tests__` sibling). Both were caught by reading the
filename I had landed on rather than the content I expected. **Worth a STANDING_LINES line in its own
right:** when a probe asserts a string's presence in a file, assert the FILENAME too — a
presence check on the wrong file fails open or closed for the wrong reason, and in a client-visible
artefact it would have shipped.

## YOUR RESIDUE CORRECTION, NOW CONFIRMED BY THE GATE ITSELF
leg 6's CLEANUP at my head names **14** ids: **13 undici + `GHSA-v2v4-37r5-5v8g`** (by-package count
read off the block). So the brief's "12 undici + v2v4" was one short and the total 14 was right. The
residue sentence I carry, word for word: *dead grandfathered rows; removal needs the contract floor
`:217` revisited; Wednesday's to propose.*

## NOT COVERED
- No service suite and no image build: this touches only `scripts/audit/`, which ships in no image and
  is read by no service at runtime.
- No Schemathesis, Akto, Playwright or k6 — none reads the baseline.
- No deploy. No ticket comment. KS-729 stays In Progress and untouched.
- The 14 grandfathered rows are **not** removed here.

## FUSE
**192.4 h, computed at 2026-09-30T23:35:39Z.** **3** rows at #1364's head, down from 4: `GHSA-frvp-7c67-39w9`
(KS 530), `GHSA-wrjc-x8rr-h8h6` and `GHSA-337j-9hxr-rhxg` (KS 528). The date is unchanged and the real
fixes stay on those tickets. I re-dated nothing.

## STATE
Holding for the gate. Two PRs open from this seat: **#1363 MERGED**, **#1364 READY**. KS-1399 filed.
ITEM 4's text is next if it fits under 75%; ITEMs 2 and 3 to my successor as UNRAISED per your ruling.
Watcher, `ps` in the same action as this sentence:
```

```
