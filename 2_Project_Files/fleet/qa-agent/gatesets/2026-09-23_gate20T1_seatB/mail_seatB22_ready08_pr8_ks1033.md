SUBJECT: [Secuura/Blockchain-B -> Wednesday] READY FOR QA (Seat B 22nd): PR 8 KS-1033 MISSINGBASE — tier 1, #1209
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-23T07:39:01.000Z
MESSAGE_ID: <010001a0cd3423b0-e8af4000-0d27-4329-a9a8-2facfbd7458f-000000@email.amazonses.com>
CAPTURED: 2026-09-23T08:11:15Z by the gate20T1 (round-20 tier-1) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)
TEXT_SHA256: 09b213abaabaf0a0131acec9bddaa73a0a9234406276977d1b35c3629d2bed32
Seat B 22nd — READY FOR QA: PR 8 of 10. KS-1033 MISSINGBASE, tier 1, shell-suite lane, bash_patch. A gate-named DESIGN change.

## THE FIVE THINGS
1. **PR #1209** — https://github.com/Secuura/Distributed_Secuura/pull/1209
2. **Head at ORIGIN, same action:** `34f264cfbd8656860e4714f1a584fee1469f5a37`, **both refs** (`refs/heads/…` and `refs/pull/1209/head`).
3. **Ticket KS-1033** was already In Progress (round-19 PR #1185 attached); now carries **2** attachments.
   `attachmentsForURL(#1209)` = exactly `[(KS-1033, contributes)]`. It stays In Progress; nothing closed, nothing filed.
4. Test Evidence below. 5. NOT-done below.

## BUILD FACTS
branch `feature/ks-1033-residue-the-three-guards-that-could-not-be-wired-and-r17-missingbase-1` (scanner `['ks-1033']`; the
foreign hyphenated key the ticket title carries is EXCISED, as ruled — control `feature/ks-1257-…-threehunks-1` reads two).
base `2bc5ccf63` · tier 1 · **PR-alone tree `ee5c6b40654e9626d97f278c61dcf0f738f47496`** read back from the pushed commit ==
my own item-0 prediction (which I re-measured rather than inherited: temp `GIT_INDEX_FILE` + `git apply --cached`, worktree left `porcelain=0`).
commit `34f264cfb`, parent `2bc5ccf63`, 2 files, clean. subject **82 chars**, ASCII.

## WHAT IT IS — the design change, stated because the READY header does not
An unresolvable base used to print `[demo-guard] base $BASE not found; nothing to compare` and **exit 0**, so a tree
carrying a real demo mutation read as clean whenever the base was missing. It now writes `…cannot be resolved; refusing
to read the tree as clean` to **stderr** and **exits 2**. Fail-closed. The body says so in those words; the FEED-17
proposal row named it a design change, the READY header does not.

**Reach into pushes today: NONE — measured.** `git grep check-no-demo-mutation` at the tip finds no caller outside its own
two suites in `scripts/__tests__`, a comment at `scripts/preflight/preflight.sh:670`, and the entry at
`scripts/run-code-guards.sh:116` that keeps it OFF the gate. Nothing on a push path changes behaviour.

## TEST EVIDENCE
**touched:** `scripts/check-no-demo-mutation.sh` (+3/-3; 144 -> 144) · `scripts/__tests__/check_no_demo_mutation_missing_base.test.sh` (NEW, 133).
- **B4 red-first:** new suite fails at the untouched tip — rc 1, **2 FAIL lines, 3 pass lines** == the pass's B4 exactly.
  The two reds are the two halves of the old behaviour: *"an unresolvable default base exited 0, not 2 - a demo mutation on
  this tree read as clean"* and *"cannot-be-resolved present=NO, nothing-to-compare present=YES"*.
- **B5a:** `bash -n` rc 0 after the hunk and again on the final tree.
- **B5 green-after:** rc 0, **0 FAIL, 5 pass lines** == the pass's B5 exactly.
- **B6 sibling:** `check_no_demo_mutation_base.test.sh` — the one suite that drives this script — ran **before and after**:
  rc 0, 0 FAIL, 5 pass both times. No new failure.
- Blobs/lines asserted == item 0: suite `5c7fb19da54a` / 133, script `4cc7c080b8a9` / 144.
- **Apply units:** both sections **strict** (`--check` rc 0, `-R --check` rc 1 each). Here `cat(section_1, section_2)` **IS**
  byte-equal to `patch.diff` — the inverse of PR 7, where the pass synthesised a new-file header and `cmp` returns 1. Same
  instrument, two different answers, so it discriminates.
- `:5432` ESTABLISHED sampler **0 hits** across every run; the same instrument saw a control connection on a private
  loopback port, so it is not blind. Census not instrumented on the bash lane (your Q7) — stated, not counted.
- Pre-push **12/15 legs ran, 3 SKIPPED, nothing failed**; the 3 are the local-stack legs (`SKIP — local stack not up on
  http://localhost:6882`). 4 `login_stub` cleared, 0 remaining.
- Lock `.push-lock-20` 07:31:01Z -> 07:37:04Z, **PROTOCOL-CLEAN** (first push: tracking ref added at origin's head; other
  refs changed 0; worktrees IDENTICAL; heads IDENTICAL, 306).
- `verify_pr21.py`: head EQUAL on both refs · tree EQUAL · `diff --name-only base...HEAD` == declared · attachments exactly
  own+contributes · **board guard 65 keys read, drift 8, unattributed 0** (every drift an own key carrying a PR from my `prs.tsv`).

## NOT RUN / NOT COVERED
- **This change cannot be observed by pushing.** The guard is not on the pre-push gate, so nothing on a push path exercises
  the new exit 2. The proof is the suite, not a push.
- **The default base is untouched.** The measured reason the guard stays unwired — it defaults to `origin/main` and diffs
  `BASE...HEAD`, so under Git Flow every develop-based branch reads the whole develop-vs-main delta as its own change — is
  NOT addressed here and still has to be fixed before anyone wires it. This PR changes only the cannot-resolve-at-all path.
- The script was never run against a real stack or a real demo tree; the suite drives it with synthetic git trees.
- No migration, no config, no env var, no service code.

## ROUND STATE
**8 of 10 raised:** #1202, #1203, #1204, #1205, #1206, #1207, #1208, **#1209**.
Tier 1 so far: PRs 3, 6, 7, 8 (#1204, #1208, #1207, #1209). Remaining: **PR 9 (KS-1239), PR 10 (KS-1084)** — going straight to
PR 9 now, per your 05:58Z ruling not to pause after a READY.
**Your tier-2 GO (07:36:38Z, DKIM pass) is RECEIVED and HELD** — four heads recorded, to be merged one at a time AFTER READY 10
and before I hold, re-deriving each over the moved develop, exactly as it says. Nothing merged yet.
Nothing deployed, no ticket comment, no ticket filed, `/api/seen` never called.

