# QA Agent Invocation Brief — Secuura/Blockchain · KS-930 · PR #876 · TIER 1 RE-GATE

**TIER 1.** `check-shared-relink.sh` is **preflight leg 13, blocking every push**. A previous tier-1
pass PASSED this PR at head `af954c691` — **and the head then moved twice while that gate was
running.** The verdict you are re-running describes a SHA the branch has moved past. Two commits are
UNGATED. That is the whole reason this brief exists, and Wednesday states it first because it was
Wednesday's instruction that caused the push mid-gate.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. **Findings-only —
you never fix.** NOT-TESTED at equal prominence to findings.

## 1. Target — measured by Wednesday with `ls-remote` in the same action as writing this line
- Repo `/Volumes/DevMASTER/!CODING/Secuura/Blockchain` (Platform K).
- **PR #876 head `a0ad0a084e7ecdd772d106740a283f738ccdadf7`**, base develop
  `306d0db923183f3b62b053f0242549e37bdf362c`.
- **No builder seat is live in this repo right now** (both panes closed ~01:2x/01:4x). The worktrees
  `worktrees/seat-a` and `worktrees/seat-b` may still exist on disk — touch neither. Work only in
  YOUR OWN clone/worktree **pinned to the literal SHA above**. In a clone taken from the local project
  repo, `origin/develop` resolves to the SOURCE's local develop — pin `refs/qa/base` to the literal
  `306d0db92` and use only that.
- **If a push lands on this branch while you are running, STOP and mail Wednesday.** Do not fold a
  moving head into a verdict.

## 2. What is ungated — the delta, measured read-only by Wednesday (`git log`/`diff --stat`)
```
a0ad0a084  KS-930 F-3: give the substring argument an actual red-proof, and correct the comment
           that overstated it
ff7704135  KS-930 F-6 + F-5: the nginx exemption, granted positively — and the CASE axis closed
```
`af954c691..a0ad0a084` = 2 files, +235/-10:
`Blockchain/Dev/scripts/check-shared-relink.sh` (+90) and its
`scripts/__tests__/check_shared_relink.test.sh` (+155).

**The earlier tier-1 verdict covers `af954c691` and nothing after it.** Everything in those two
commits — the F-5 case axis, the whole F-6 nginx exemption, and the F-3 fifth cell — has never been
gated. Treat this as a first gate on those two commits, plus a confirmation that the previously-passed
behaviour still holds at the new head.

## 3. Scope — press these, in this order

**(1) THE F-6 NGINX EXEMPTION — an exemption is a hole granted on purpose, and the question is
whether it is exactly as wide as it was meant to be.**
Establish, from the script: what the exemption matches, what it lets through, and **what else in the
real 25-file tree it now matches that nobody intended.** An exemption written for one file that also
covers a second file is a silent false-clean on the second. Enumerate every real file the exemption's
pattern reaches — not the files the author had in mind.
**Red-proof it in both directions:** remove the exemption → the nginx case must be the ONLY thing that
reds; keep it → construct the clobber shape the exemption is NOT meant to permit and confirm it is
still BLOCKED.

**(2) THE F-5 CASE AXIS.** Establish what "the case axis closed" actually means in the code, then
attack it: mixed case, unusual whitespace, the same directive spelled with different casing in a
single file. A case-insensitivity fix is the classic place where a widened match starts catching
neighbours.

**(3) THE F-3 FIFTH CELL — and read this one carefully, because Wednesday got it wrong here once
already.**
The previous tier-1 verdict's FINDING 2 established, by running it, that stripping the substring
argument from the four then-existing cells gives **byte-identical failure lines** (27 passed / 3
failed both ways, every failure reading "expected exit 1, got 0") — the substrings were **INERT** on
those fixtures. The tester recommended a fifth cell on a single-write fixture, where exit-code-only
DOES pass against the unfixed guard. `a0ad0a084` is the commit that adds it.
**So: does the fifth cell actually discriminate?** Tamper its expected substring away and confirm it
then PASSES against the pre-fix guard, and that the unstripped version FAILS. If it does not
discriminate, the cell is decoration and this is a real finding even though the fix stands.
Also check the corrected comment now says something true about which fixtures the substring is
load-bearing on.

**(4) EVERY RED-PROOF ISOLATES.** For each fix in these two commits: the tamper must red ONLY that
fix's cells. A tamper that reds a cell alongside its neighbours proves nothing about what the cell
adds. Re-derive them; do not accept the numbers from the commit message.

**(5) THE PREVIOUSLY-PASSED BEHAVIOUR STILL HOLDS AT THE NEW HEAD.** The real tree is
**25 of 25 clean in BOTH default and STRICT modes**; `npm init -y` stays CLEAN; the three false-clean
shapes from the original finding (`COPY ["--from=builder", ...]`, `COPY --from=builder [...]`,
`RUN npm i --omit=dev`) are still BLOCKED. Rebuild the two-write fixture — **the fixture shape is the
finding**: a single-write fixture exits 1 through the "unexpected shape" fallback and hides the hole.
Build both, report both.

**(6) NEW FALSE BLOCKS.** The mirror risk of closing false cleans is blocking something legitimate.
Known and deliberately left (NOT findings): heredoc shapes and non-final-stage shapes. Anything else
newly blocked IS a finding.

## 4. Credentials (POINTER ONLY)
`4_Credentials/.env`. You should not need any.

## 5. State-mutation & cleanup
- **No `rm`** — quarantine by rename ([[never-delete-cleanup-means-quarantine]]).
- **Restore any tamper by INVERSE EDIT verified with sha256, never by checkout — and then RE-RUN the
  suite.** A hash proves the bytes; only a run proves the file still works.
- Touch neither `worktrees/seat-a` nor `worktrees/seat-b`, and push nothing.
- Copy any launch wrapper you need into your own `state/` — do not edit Wednesday's.
- Use `python` string replacement rather than `sed` for multi-line edits.

## 6. Report
ONE mail to `wednesday-agent@agentmail.to`, subject exactly:
`[QA -> Wednesday] Secuura KS-930 re-gate (#876 @ a0ad0a084, tier 1)`
Structure: BLUF (GO / NO GO + why in one line) · FINDINGS (severity, evidence, the command that
produced it) · **NOT-TESTED at equal prominence** · the SHA you actually gated (re-read `ls-remote`
at the end and say if it moved).
**Every claim carries the instrument that produced it, inline.** A measurement travels; an
explanation of it does not — if you report someone else's reasoning, quote it verbatim including its
hedges, and label anything you add as yours.
