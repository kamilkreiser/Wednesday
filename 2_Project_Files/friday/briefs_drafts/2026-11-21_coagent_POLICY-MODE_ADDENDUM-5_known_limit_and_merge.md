This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat POLICY-MODE only. It closes the branch on the owner's word. Report under "## ADDENDUM 5 (known limit, then merge)" in your STATUS file.

# POLICY-MODE — ADDENDUM 5: write the open spelling down as a known limit, then the merge check

## 0. Before anything
Re-read WHOLE: your brief; addenda 1 to 4; your STATUS file; the short re-check's verdict `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_POLICY_MODE_r2_verdict.md` (READ-ONLY), sections 4 and 12.

## 1. The authority
- The re-check: `VERDICT: NO GO — head 443549ca955a617a0ae50d1a825afa737af1e990`: M-1b (Major) a RELATIVE hook working directory is allowed in the mode with the sandbox verified; m-A (Minor) where the shell was never allowed, an unresolvable working directory now gets a refusal instead of a card.
- The owner (Kam), card `general-c2c-policy-mode-recheck-nogo-1120`, verbatim: "b — Write it down as a known limit and merge". The option as shown to him: "The docs name the limit and why; one test pins today's behaviour; the fix goes to the piece that switches the mode on. Then my own merge check before it lands."
- So: NO change to the policy's decisions in this round. Docs, one test, BACKLOG only. A change to `src/` is a STOP.

## 2. What to write
1. **`docs/POLICY.md` §11 (stated limits): M-1b**, in plain words: with the mode on and the sandbox verified, a shell command whose working directory arrives as a relative name is allowed, because the gate normalises that directory against `/` and so treats it as resolved. Say why it is accepted for now, in the re-check's three reasons (the host fills the working directory, normally absolute, not yet seen on a real host; shell is allowed in the mode only with the sandbox verified, the owner's ruling D2; an agent can already spell the same through shell text, which is outside the class by ruling), and that the fix (refuse a shell command whose hook working directory was not absolute, without changing the mode-absent card) belongs to the lane that switches the mode on.
2. **§10 rule 33: m-A**, one sentence: where the mode never allows a shell command (sandbox not verified, or a shell tool other than `Bash`), a shell command whose working directory the gate cannot resolve is REFUSED in the mode instead of shown as a card, because step 7c runs before step 7d.
3. **One `t21` test pinning today's behaviour**, named so that it reads as a known limit (for example `known_limit_relative_shell_cwd_is_allowed_with_verified_sandbox`): `Bash` from hook cwd `"rel"` with the sandbox verified is a mode ALLOW today, and the same command with the mode absent is today's card. Its doc comment says: "This pins a KNOWN LIMIT (owner's card general-c2c-policy-mode-recheck-nogo-1120 = b). When the switch-on lane fixes it, this test is replaced, not deleted." Add one more `t21` row for m-A: the same unresolvable `cwd` with the sandbox NOT verified is `Deny(BypassRefused "a path the gate could not resolve")` in the mode and today's card with the mode absent.
4. **`BACKLOG.md`**: one entry for M-1b in the file's own form (where, symptom, why deferred: the owner's card = b, owner: the switch-on lane), one for the re-check's notes n-B (non-ASCII hosts refused in the mode) and n-C (a bare IP such as the cloud metadata address is mode-allowed: inside the rule as ruled, for the switch-on lane to weigh).

## 3. Then
1. Merge `origin/main` INTO the branch (never rebase). Main is now `16e83fbe5592658ddcda769d7827895941eca678` (the roster lane). `git diff --stat 2bba2a4 16e83fb -- crates/coagent-policy docs/POLICY.md` must be empty (check it; if not, STOP). Expected conflict: `BACKLOG.md` only.
2. On the merged head, once: `scripts/check.sh` (before it, `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/heavy_runs.sh` below 3; a tool failure = FULL; the relay lane goes before you today). Record totals against your last run (1,286 / 0 / 21 over 172 lines) plus the roster lane's tests merged in and your two new rows. The 60-row runner is NOT re-run: no `src/` change.
3. Your brief's final checks (protected hashes, scope, the dark grep, name scan with control, push, ls-remote, ancestor, re-read main).

Last line when all is done, exactly: `READY FOR MERGE CHECK POLICY-MODE r3`. Friday then runs her own clean-clone merge check (runner `crates/coagent-policy/red-controls.sh`) before any merge GO.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
