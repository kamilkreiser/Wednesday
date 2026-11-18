This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It answers the STOP QUESTION at the end of your STATUS section "BLOCKERS (ADDENDUM-9)". Everything in addenda 4 to 9 that is not named here stands.

# M1_DAEMON — ADDENDUM-10: push `feedc60` as it is and write the READY line; main is merged in later, once

RULING (Friday, 2026-11-18): do NOT merge `e354118` now and do NOT run section 3 again. Your own measurement decides it: the three commits touch only `crates/coagent-audit/`, `docs/AUDIT.md`, `scripts/red-controls-audit.sh` and `BACKLOG.md`; no crate you build names `coagent-audit` in its manifest; your trial merge shows no conflict. So the results on `feedc60` cover the daemon's code as it will merge. This SUPERSEDES, for this one move of main, addendum 9 section 3's "STOP for Friday if it moved" and addendum 7 item 4.

1. Push `feedc603ead01e8c6967f193c72deca49ba51c02` with `git push origin m1-daemon` (never force, never a rebase). Record `git ls-remote origin m1-daemon`.
2. In A5.5 record the ancestor check as it is (exit 1 against `e354118`, exit 0 against `c9a6653`) with one sentence saying why that is accepted here: this addendum.
3. Then the last line of STATUS, exactly: `READY FOR QA M1-DAEMON r4`. Then wait.

What follows, so that you know it: ONE independent check runs at `feedc60` (it also rules on your F-F test fix of `feedc60`, with the three items you listed). On its GO a notes addendum will tell you to merge the then-current `origin/main` INTO `m1-daemon` once and to run `check.sh`, the runner and the five-run test on that merged tree before Friday's own clean-clone check and the merge GO. More pieces may merge before then; you are not asked to follow main until that addendum.

Stopping on the moved main instead of pushing was the right call under your brief.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
