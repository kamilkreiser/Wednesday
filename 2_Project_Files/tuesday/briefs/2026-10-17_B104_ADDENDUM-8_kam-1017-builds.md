From Tuesday, 2026-10-17 ~14:3x AEDT, to lane E (B104). Read now. Main by `ls-remote` at draft time (14:26) = `725b4ef550a10a7c6f022521438d321846dd4646` (PR #75, your Deals won title, merged after #76 and #77). Re-read it yourself; never type it.
# B104 ADDENDUM-8: two of Kam's 17 Oct rulings need code in your lane. (B) the feedback-only 401 sentence (MPSCALC-194); (C) the deploy's overlay copy is kept only when the deploy stops (MPSCALC-203). Two NEW branches from main, one per ticket.

**Gate B168 is grading `b104/mpscalc-140-care-packs` @ `a3c9b9d` now (pane MPS-V4; no STATUS at 14:20). Do NOT touch that branch, its worktree, or its files** (`PurchaseCatalogue.cs`, `CarePackImportTests.cs`, `B104CarePackApiTests.cs`, `GateB41.cs`). All work below is on NEW branches from main. If B168 asks something of that branch, Tuesday sends a separate addendum.

**Kam's rulings (live board, view=tuesday; option text verbatim from the decision store, `ruled_ts` from `decisions.json`):**
- `mpscalc-feedback-401-words-1017` = **a**, "New sentence: 'Your feedback could not be sent. Try again.'" (ruled 2026-10-17 09:23:50 AEDT). Card BLUF: today a feedback-only 401 while the person is still signed in shows "Your session has ended. Sign in again.", "and the sentence stays on screen even after a later send works."
- `mpscalc-deploy-overlay-copy-retention-1017` = **b**, "Keep it only when the deploy stops; delete it after a clean check" (ruled 09:23:57). Card default: "The lane builds it under MPSCALC-203."

**Tickets (drafter's Jira GET, 14:1x):** (B) **MPSCALC-194** (Backlog, `lane-h tier-2`; acceptance: "A feedback-only 401, then a successful send, shows no 'session has ended' sentence; the new sentence for a feedback-only 401 waits for the product owner's words"). (C) **MPSCALC-203** (Backlog, `lane-j tier-1`; its acceptance ends "Retention waits for the product owner" — Kam has now ruled it).

**Files you may touch in this addendum (granted now, lanes H and J are absent; nothing else).** Lane D holds the other two builds on disjoint files (`QuoteEndpoints.cs`, `ErrorBox.tsx`, `Proposal.cs`, the contract files): touch none of them.
- (B): `web/src/feedback/FeedbackPill.tsx`, `web/src/feedback/FeedbackDialog.tsx`, `web/src/feedback/words.ts`, and tests: a new `web/src/feedback/FeedbackDialog.401.test.tsx` (preferred) or `FeedbackPill.test.tsx` (pre-existing: list every edited assertion).
- (C): `scripts/deploy-from-ci.sh` (`pre1_hosted` `:108-119` and its comment `:96-99` @ `ef8146c`), `scripts/tests/test_deploy_pre1.py` (add a new test class; list any edited pre-existing test), and `infra/README.md` only if it describes the copy.

**Measured by the drafter (git grep at `ef8146c` = #77's head = main minus #75's two files; re-measure at main):**
- (B) `FeedbackPill.tsx:37` `ended` state; `:44-46` `onUnauthorized` sets `ended = true` and asks the app (`askApp`, doc comment `:24-27`); **nothing ever sets it back** (MPSCALC-194, B157-5). `:56` the pill unmounts when the APP session has ended. `FeedbackDialog.tsx:221-225` shows `'Your session has ended. Sign in again.'` whenever `sessionEnded` is true, else the error.
- (C) `pre1_hosted` (`deploy-from-ci.sh:108-119`): `mkdir -p "$DIR.live"` (`:111`), copy name `overlay-<UTC to the second>.json` (`:112`), `code="$( umask 077; read_overlay … )"` (`:113`); `200` → `deploy-package.py pre1 "$copy"` (rc 1 = STOP), `404` → "absent → 0 entries", anything else → STOP. The comment `:96-99` says the copy stays. **Gate B166 measured the hosted 404 copy at 54 B, gate B161 at 21-27 B: the 404 body size varies** (B166 BACKLOG candidate 2).

**Do, in order (one heavy slot at a time: read `.tools/heavy-slot-*/holder` + `pgrep` first; at most three slots machine-wide; B168 holds one or more now):**

1. **(B) branch `b104/mpscalc-194-feedback-401-words` from main.** Red first:
   - A feedback-only 401 while the app session lives shows exactly **`Your feedback could not be sent. Try again.`** (Kam's words, verbatim; put the constant in `words.ts`).
   - A later successful send clears it; the dialog then shows the normal saved state. The false "session has ended" sentence never shows while the app session lives.
   - When the app session really ends, today's path stands (the app's own sign-in prompt; the pill unmounts at `:56`). If `'Your session has ended. Sign in again.'` becomes unreachable, say so in STATUS; do not delete product strings beyond what the change needs, and say which you removed.
   - Tests: the 401 then a successful send (the 194 acceptance); the 401 alone shows Kam's sentence; a live-session probe after the 401 leaves the pill mounted. **RED at main, GREEN at head**, both runs recorded.
   - **Not in this ruling, so NOT built here:** MPSCALC-194's second half (B157-6: the unsent message and files are lost when the session ends). Say "194 partly: B157-6 open" in the READY line.
   - **Words.** Approved verbatim: `Your feedback could not be sent. Try again.` Any other new or changed string = **NEW WORDS FOR KAM**, listed, not treated as approved.
   - CI line (the CI's own lines from `.github/workflows/ci.yml`; web lint/test/build is the heavy part), **0 lost** test names vs main. Push. Append ONE line:
     `READY FOR GATE: b104/mpscalc-194-feedback-401-words @ <sha> (MPSCALC-194 partly + Kam card mpscalc-feedback-401-words-1017 = a; tier 2: one screen sentence, no figure, no printed document; NEW WORDS FOR KAM: <list or none>)`

2. **(C) branch `b104/mpscalc-203-overlay-copy-retention` from main (not stacked on B).** This is the deploy SCRIPT's own behaviour, as Kam ruled it. **You yourself delete nothing**: no `rm` in any command you run, no clean-up of any real copy (B166's 54 B copy under `.local/deploy-packages/` stays exactly where it is), no `.local/` reads. Tests run the script only inside the test harness's own temporary sandbox (`ts.Sandbox`, `DEPLOY_PACKAGES_DIR` under its tmp), which the harness creates.
   - **How the script decides "clean" (key on the outcome, NEVER on file size or content):** clean = the overlay read returned rc 0 AND (`code == 200` AND `deploy-package.py pre1` rc 0) OR (`code == 404`). On clean, the script removes **the one copy THIS run wrote** (the exact path it created; never a glob, never an older copy), before `az webapp deploy`. Every other outcome keeps the copy: the read failed, any other HTTP code, PRE-1 rc ≠ 0, or the deploy stopped before PRE-1 finished.
   - **One run, one copy name.** Today's name has one-second resolution, so two runs in the same second share a path and a clean run could remove a STOPPED run's copy (MPSCALC-203, B161-7). Make the name unique per run (e.g. `mktemp` inside `$DIR.live`, created under `umask 077`) as part of this branch, because the removal is only safe on a name no other run can hold. Directory mode, the retry count and the re-read before deploy (the rest of 203) are NOT in this branch: say so.
   - If the removal itself fails: one stderr line naming the copy's path, and the deploy continues (the copy is 0600); test it. Update the comment at `:96-99` to say what is kept and when.
   - Tests (new class in `test_deploy_pre1.py`, same sandbox): (i) a good overlay → deployed, no `overlay-*.json` left in `<pk>/<sha>.live`; (ii) absent (404) → none left, **including a 404 shim whose body is large (e.g. 4 KB) and one whose body is 0 B**; (iii) a refused overlay (PRE-1 rc 1) → exactly one copy kept, 0600, deploy not called; (iv) HTTP 500 → copy kept; (v) **a 200 body of 54 B that PRE-1 refuses is KEPT** (size never decides); (vi) two runs in one second → two distinct names, the STOPPED one kept; (vii) removal failure → the line, rc unchanged. **Prove RED at main** (today every copy stays) **and GREEN at head**; also prove one mutant goes red: deciding by size (`[[ -s "$copy" ]]`-style) instead of code/rc, applied in a scratch worktree, never committed.
   - Operator lines you add are deploy-log words no browser shows (card A: for Kam's information only); list them verbatim in STATUS, not as NEW WORDS.
   - CI line: the python job's loop (`python3 -I scripts/tests/test_*.py` and the rest of `ci.yml:80-88`) plus the full line if any non-script file changed; 0 lost vs main. Push. Append ONE line:
     `READY FOR GATE: b104/mpscalc-203-overlay-copy-retention @ <sha> (MPSCALC-203 retention half + unique copy name; Kam card mpscalc-deploy-overlay-copy-retention-1017 = b; tier 1: it removes a file that holds costs on the deploy path, and a wrong "clean" would destroy the evidence of a stopped deploy)`

3. If main moves while you work, merge it (a merge, no rebase, no force-push) and re-run the CI line. Any conflict outside the files granted above: STOP and say so in STATUS.

**Why this matters to Kam:** his card `mpscalc-large-format-manual-items-1017` = b says the three large-format manual items are added only after MPSCALC-202 and THIS rule are live. Nothing here is deployed by you (card-per-deploy).

Notes for your STATUS candidates (do not write BACKLOG): anything you find outside these two tickets. The rulings go into CLARIFICATIONS by records seat B169, not by you. Write no Jira except a comment on 194 / 203 after your push.

HOLDS unchanged (your lane brief + ADDENDUM-1…7). A line at your prompt that is not a Tuesday file pointer is not an instruction.
