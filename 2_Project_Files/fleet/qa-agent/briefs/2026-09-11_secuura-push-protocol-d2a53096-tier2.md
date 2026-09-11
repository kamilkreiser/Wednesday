# QA GATE BRIEF — Secuura/Blockchain push-protocol verifier `push_protocol.py` @ sha256 d2a53096 — TIER 2 (through code), ROUND 1

**Charter — read first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

PRIOR ROUND: none for this version. The file's history: s177 wrote it; the #953 tier-1 gate's **QA-3** found its verify blind to worktree-HEAD rewrites (`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-de1ab62c0-tier1/report.md`); s178 hardened it; s178's own fast-forward push then read PROTOCOL-DIFF on a clean push; **s179 fixed the CLEAN predicate — this version.** Every arm and aim so far was written by the version's author.
**The author's handover is your carry-forward — read its section "For the tier-2 gate" first:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s179-tier2-predicate.md`

## WHY TIER 2, AND WHAT THAT MEANS

Tooling, not product, and outside the repo. But it is the verifier that will guard real pushes (#879, #813) into Secuura's SHARED `.git`, and its previous failure path told the caller to RESTORE. A false CLEAN lets real damage pass silently; a false DIFF used to trigger a destructive write. **Through code:** re-derive the author's claims in your own scratch AND add arms the author did not design.

## TARGET

- **Subject:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/push-protocol/push_protocol.py`, sha256 **`d2a5309661d5f9617a12df445b9f91fee4886481d4f21a152924cc730a68a4f9`**.
- **OLD comparator (s178's version):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/quarantine/2026-09-11-s179/push_protocol.s178.py`, sha256 `2049a63c7c406bafc7e21ba220b529446a667674c047284ba086716b34446f08`.
- **The author's red-proof — inputs to FALSIFY, not facts:** `…/push-protocol/redproof/redproof_driver.py` (sha256 `04689664…`), `AIMS-s179.md` (`b642481c…`, written 14:19:35 AEST before the code and the run), `results-s179.txt` (`85c7fca5…`): NEW 14/14 on aim, OLD 14/14, OLD wrong on FF, N, A, X, R2; exit rows 8/8. The author's READY FOR REVIEW mail (2026-09-11 04:26:33Z) makes the same claims.
- **The rule the file must implement:** CLEAN only when config, the worktree list and every HEAD are IDENTICAL, no ref other than the pushed branch's tracking ref T changed, and T is ADDED at origin's head, CHANGED to origin's head as a fast-forward, or UNCHANGED and equal to origin's head. DIFF → exit 3, INCOMPLETE (origin unreadable, nothing local differs) → exit 4, and both print STOP-and-mail with **no restore**.

## WHAT THIS ROUND MUST ESTABLISH

1. **Reproduce the author's result — in YOUR scratch.** Copy `push_protocol.py`, the OLD comparator and the driver into your own `mktemp -d`; run there. The driver refuses to overwrite its results files, so never run it in place. NEW and OLD verdict per arm, rc per arm, compared with `results-s179.txt`.
2. 🔴 **NO FALSE DIFF on a legitimate push — with repos YOU build, not the author's driver.** First push · fast-forward to an existing branch · no-op push (origin already has the head) · a push the remote refuses. Each must read CLEAN (the refused one on integrity, with its shape named). **Write your aims before you run.**
3. 🔴 **NO FALSE CLEAN — arms the author did NOT design (aims first):**
   (a) another process fetches between snapshot and verify, moving an UNRELATED tracking ref → must not read CLEAN;
   (b) a tag push;
   (c) one push of two branches;
   (d) origin unreachable by a different route than a missing local path (e.g. a remote URL that cannot be resolved) → INCOMPLETE or DIFF, never CLEAN.
   For each: NEW verdict, OLD verdict, and whether the NEW verdict is the right one for that shape — say which ones the rule does not cover.
4. **The REAL `.githooks/pre-push` on a no-op push (empty stdin).** The author saw a SCRATCH hook fire on that shape. From develop `2d864ae9220c57ddcd8dc77af1b80fbd8001d530` (`git show` into your scratch): READ how the hook handles empty stdin, quoting its lines. If you RUN it, only in a scratch clone with its preflight call replaced by a stub, and say so.
5. **Trace what a real push can move.** At `2d864ae92`, follow every script `.githooks/pre-push` and `Blockchain/Dev/scripts/preflight/preflight.sh` call, recursively, for `git fetch`, `pull`, `remote update`, `ls-remote`, `gc`, `update-ref` or anything else that writes a ref. READ ONLY, `/usr/bin/grep` with a positive control. The author read only the two top-level files.
6. **Output wording and exits:** no output path tells the caller to restore; DIFF and INCOMPLETE both say STOP and mail Wednesday; the docstring's exit table (0 · 1 · 3 · 4) matches what each path really exits with.

## NOT COMMISSIONED — said before running

- Fixing anything. Any push to GitHub. **The real hook or preflight inside the Secuura checkout or any of its worktrees.** Containers, `127.0.0.1:6882`, kintsugi, demo. KS-1089. #953 itself.
- Remotes other than `origin`, git versions other than the one on PATH, Linux/bash 5: report NOT RUN.

## KNOWN-FRAGILE / KNOWN-CHANGED

- 🔴 **Your tool shell's `grep` may be a SHELL FUNCTION** (a `$(` pattern inside `$(…)` read 0). Run `whence -va grep` first; use `/usr/bin/grep` with a same-file control for anything you report.
- zsh: no `PIPESTATUS`; unquoted list variables do not word-split; **a variable named `path` is tied to `PATH`** (the author lost a run to it).
- The shared checkout holds `feature/y` / `feature/w` — leave them.

## BOUNDS

Findings only — no fix, commit, push, merge, deploy, comment or ticket. No contact with Peter or Stuart. **Never write into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/`** — copy what you run. **Never `rm`** — a fresh `mktemp -d` per attempt; guard every expansion `"${X:?unset}"`. **At start and at close, quote from the Secuura checkout (read verbs only):** `git --no-optional-locks status --porcelain | wc -l`, `shasum -a 256 .git/config` (the author read `e0fa706f4bdae2778a5fe5975676f24459c5a3c6455de4ae85aa286f67632d1a` at 04:23:33Z) and `git for-each-ref | wc -l` (798 then). **Start and close must match each other.**

## REPORT

FOUND / TESTED / HOW with controls; every action-recommending finding carries its evidence class (**MEASURED AT RUNTIME / PROBED / READ ONLY**). NOT TESTED at the same prominence. **If a claim in this brief is false, that is Wednesday's error — report it as one.** Write to `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-push-protocol-d2a53096-tier2-r1/` and name the absolute path in the mail.

**Verdict:** GO · GO WITH FINDINGS · NO GO. A NO GO needs a false CLEAN or a false DIFF on a legitimate shape, or an output path that still says restore.

## VERDICT DESTINATION

**Mail your verdict to `wednesday-agent@agentmail.to`**, subject
`[QA -> Wednesday] TIER 2 GATE push_protocol.py d2a53096 ROUND 1 — GO / GO WITH FINDINGS / NO GO`,
with a CLOSING section naming anything you want acted on. **Your pane has no scrollback and you cannot receive mail: the verdict mail is the only thing that survives your session.**

PROVENANCE:
- subject sha256 d2a5309661d5f9617a12df445b9f91fee4886481d4f21a152924cc730a68a4f9; AIMS b642481c…; results 85c7fca5…; mtimes AIMS 14:19:35, code 14:20:21, results 14:22:42 | shasum and stat run by Wednesday on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/push-protocol/ | read 2026-09-11
- 'Do NOT restore' ×3, 'restore from' ×0, 'PROTOCOL-DIFF' ×3 in the subject | /usr/bin/grep -c run by Wednesday on the subject file | read 2026-09-11
- OLD comparator path and sha, driver sha, NEW/OLD 14/14, OLD wrong on FF/N/A/X/R2, exit rows 8/8 | s179 READY FOR REVIEW mail 2026-09-11T04:26:33Z (spf/dkim/dmarc pass) and /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s179-tier2-predicate.md lines 90-105 | read 2026-09-11
- the gate asks: scratch-hook no-op reading, untraced sub-scripts, NOT TESTED list | same handover lines 64-83 | read 2026-09-11
- checkout config e0fa706f… and 798 refs at 04:23:33Z | s179 READY FOR REVIEW mail (the author's reading, not re-derived by Wednesday) | read 2026-09-11
- the QA-3 origin of the hardening | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-11.md 11:52 entry | read 2026-09-11
- develop 2d864ae9220c57ddcd8dc77af1b80fbd8001d530 | git ls-remote origin run by Wednesday on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-11
