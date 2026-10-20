# B381 drafter report (2026-10-21 ~07:48 AEDT)

Brief: `2026-10-21_B381_SEAT-D13_hpsmpoc-lane2-formgate-mock.md` (112 lines). Shape copied from B372 (read whole, with its drafter report) plus `BRIEF_SKELETON.md` and `model-routing.md` v1.0 (read whole).

## Stamp slots
Two, `@MAIN@` (main sha at launch) and `@STAMP@` (stamp time, launch authority, answered questions). Control: `grep -o -E '@[A-Z_]+@'` on the draft printed `@MAIN@` 1 and `@STAMP@` 1. Fill both; the stamped copy must print 0.

## Questions for Tuesday (each with a recommended answer)
1. Q1. Gate tier. I wrote **tier 1** (G1, Opus 5.5) because the -289 commit changes a request-size defence in the BFF, the PR is to be deployed before HP sees it, and the mechanism is not measured by a prior gate (B267 swept only 1 to 3 header lines). Recommend YES tier 1. Alternative: tier 2 only if -289 is split to its own PR.
2. Q2. Should -289 go in Thursday's PR at all? The ticket calls it "optional", "harmless" and "pre-existing", and it is not HP-visible. A mis-mirrored limit would be a bypass of the files' 20 MiB total at the BFF. Recommend KEEP, as the third and last commit, with the brief's decision rule (measure first; mirror only if exact; else comment-only fallback plus a pin test). If the gate slot is tight, drop it first.
3. Q3. Model row. Proposed **Sonnet 5.5, row C2 (pilot)**, gate G1 Opus; P1 NO, P4 no local tier for Datasec; P2/P3 gauge is yours (I did not read it). Recommend YES. Row C3 (Opus build) only if you judge the limit a security design; I wrote "STOP if it needs a design decision".
4. Q4. Commit order is -288, -148 N-9, -289 (easy to hard; the risky one last so a STOP still leaves two commits). The ticket list in your task is 288, 289, 148. Recommend my order.
5. Q5. -148 is NOT a close-out. Its newest comment (2026-10-19) and main both show two items left: C-2 (ActionPlanScreen words, a web component and the product owner's words, outside the lane) and N-9 (the mock's link 404 has no detail, `follow-up.ts:411`). I scoped N-9 only (one added argument: the API's existing sentence "Check that the whole link was copied."). Recommend YES; the ticket stays open for C-2. Confirm the existing API sentence needs no new approval under C-105.
6. Q6. Jira comments: one each on -288, -289, -148 after the push is read back (B372's pattern, "not merged"). Recommend YES.
7. Q7. The CR/LF row for -288 (B271-2) cannot use undici's FormData to inject a bare CR (I believe it percent-encodes; UNMEASURED), so I told the builder to hand-build the body bytes. Recommend YES.
8. Q8. Load was 13.30 / 10.78 / 8.02 at my last read (over 8). The brief keeps the 8 line and lets a single-file vitest run under 12. Recommend YES, or tighten if other lanes pile on.

## Measured (instrument, control)
- **Main = `54fbceac12393f503fae8c5810af9609bac44548`** by `git ls-remote origin refs/heads/main` at 07:41:08. Same call also showed `refs/heads/b372/...` (`91cbbcb1`, merged) as its positive control; 0 refs for `b381*`.
- **The local checkout lacks `54fbceac`** (`git cat-file -t` failed), so all code was read through `gh api` GETs at that sha (contents and a recursive tree). Control: file sizes in the tree listing match the line counts read (formGate.ts 373 lines, 19,937 bytes).
- **Open PRs: 0** (`gh pr list --state open`, empty; control `--state merged --limit 2` returned 167, 166). No `.tools/*b381*` (`ls -d`, none; control: `.tools/b372` exists).
- **Tickets by Jira GET** (`python3 -I`, `JIRA_*` read in-process, not printed): -288 and -289 Backlog, 0 comments, 0 links; -148 Backlog, 4 comments.
- **Ticket cites hold at main**: `formGate.ts:185` (exact-length), `:179` (CR/LF strip), `:195` (MAX_PART_HEADERS), `:142` (isFilePart). One drift: the API's `HeadersCountLimit = 16` is at `FeedbackFiles.cs:338` at main (ticket said `:300`).
- **-148 N-9 still open at main**: `mock/follow-up.ts:411` has no detail; API `ClientFollowUpEndpoints.cs:188-190` sends it; `problem()` takes the detail as its 4th argument (`mock/api.ts:54`); the mock files are unchanged since PR #152 (`gh api commits?path=`).
- **Existing test that -289 will disturb**: `formMeter.test.ts:285` (memory bound) builds about 16,300 one-byte lines `a` with no colon; a line limit turns it red (rule a) or leaves it green (rule b). The brief names it.
- Model id `claude-sonnet-5-5` from `models_latest.json` (`checked_at_local` 07:37:24, warnings []); `lsof` on 7410-7419 printed nothing (no listener-positive control run, so not proof).
- Helpers present: `.tools/b198/lock.sh`; `.tools/b267/{webrun,webfull,mutweb,waitload}.sh`; `.tools/b300/{jira,post,read}.py`; B267's `dnlimit` probe.

## Could not verify (all marked UNMEASURED in the brief)
- **What the API's `HeadersCountLimit` counts.** My recollection of ASP.NET Core's `MultipartReader` is that it counts DISTINCT header names (case-insensitive), not lines, which would make the ticket's "17 lines is refused" wrong for repeated names and a plain 17-line BFF limit a bypass. I could not run dotnet. This is the brief's M1 and its decision rule.
- Web baseline count, typecheck and lint at main; whether undici FormData escapes CR/LF in names; whether any screen renders the 404 `detail`; whether e2e specs assert the 404 body (Lane 5's tree); the weekly gauge; which panes are live.
