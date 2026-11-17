This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends your brief and addendum 1. Report in a section "ADDENDUM 2 (notes before merge)" of `coagent/5_Project_History/STATUS_M1_RELAY_IDENTITY.md`; while working the last line is `IN PROGRESS: A2 <item>`, and when done exactly `READY FOR MERGE CHECK M1-RELAY-IDENTITY r3`.

# M1 RELAY-IDENTITY — second gate: GO WITH NOTES at afc2472. Close the notes, then Friday runs the merge check.

## 0. Where you stand

The second independent gate passed the branch: no Blocker, no Major; every round-1 finding closed; `scripts/check.sh` exit 0 on 5 of 5 runs (314 passed, 0 failed, 5 ignored); 102 of 102 red rows; 320 random kills leave no leftover after the next clean start; standard input consumed to exactly 16,385 bytes; no key in 555 captured outputs; every protected file and both manifests byte-identical to main. Kam ruled the Major of round 1 this morning, live board 2026-11-17 09:44:08, verbatim: "Decision general-c2c-relay-identity-acl-1117: a — Accept it for the beta and say so plainly".

Read the verdict WHOLE: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M1_RELAY_IDENTITY_r2_verdict.md` (334 lines). The gate's tests and drivers: `…/m1_review/gate_relay_identity_tests_r2/`.

No further gate runs. When you write the READY line Friday checks the result herself in a clean clone (check.sh, the gate files by `cmp`, the four mutants of item 4 re-applied) and then gives a merge GO for an exact SHA.

## 1. Rulings

- **The blob version line is `v3`: ACCEPTED** (your A1-DQ1). The gate confirmed the reason: its own unchanged test asserts that a `v2` line with a current body is refused. This SUPERSEDES the words "version line becomes `coagent-relay-identity v2`" in addendum 1 section 2 item 2.
- The wrappers and lint allows around the gate's two round-1 test files: accepted, as the gate ruled.

## 2. What to do (all small; nothing else changes)

1. **R2-1: never remove a leftover silently.** If the cleanup removes anything, the line saying how many were removed is printed even when the start is then refused (today it is printed only after the load or create succeeds). Test the gate's sequence (a valid identity at mode 0640 in a 0700 folder plus one 0600 leftover: exit 1, the refusal message, AND the removed line). Red row. Correct the STATUS sentence that claimed this already held.
2. **R2-2: stop the "edited" overclaim.** The CLI README says a damaged or edited certificate is refused. The hash catches accidental damage; someone who can write the file can change the certificate and store its new hash, and it loads as a new identity. The self-signature is not checked. Say exactly that, in both READMEs and in the help text if it makes the claim: the hash protects against corruption, not against a person who can already write the file (who could equally replace the whole file). Add the sentence to the text test that pins the wording.
3. **R2-3: the sharing-rule sentence.** Replace "an open decision for the owner" (CLI README lines 51-52 and your STATUS) with the ruling: access-control lists are not checked; this is an accepted limitation for the beta; keep the `ls -le` and `ls -led` commands. Text only.
4. **R2-4: guards for the four unguarded checks**, one test and one red row each: N20 (a leftover not owned by the current user is not removed and refuses the start; test by passing a different expected user id into the real check, as you did before); N21 (a leftover with any group or other bit, such as 0604, is not removed and refuses the start); N24 (the cleanup runs only AFTER the folder check: a start pointed at a folder that fails the folder check removes nothing there; this one matters most, because without it a start aimed at an open folder would delete the user's matching files before refusing); N36 (the early non-loopback refusal honours `--allow-non-loopback`: test it WITHOUT listening on a non-loopback address, at the level of the function that decides, and say how).
5. **R2-7: the misleading message.** When the link step fails because the temporary file is gone (another start cleaned it up), the message says so plainly ("another start of the relay was creating the same identity at the same time; start again") instead of "entity not found". Test with two concurrent creations on a new path in a loop; every run must end with exactly one valid file, as the gate measured.
6. R2-6 (a path that differs only in letter case on this file system keeps its leftover) and R2-8 and R2-9: record in BACKLOG and the README's limits; no code.
7. `scripts/check.sh` exit 0; the full red-control runner; the gate's files green and byte-identical; `git merge origin/main` into the branch if main has moved (it had not at the gate's run: main is 18005d6); push. Then STOP at the READY line.

## 3. Decisions you are NOT making

Not merging (Friday gives the GO for an exact SHA after her own check; then you fast-forward main and push, and nothing else). No access-control check, no dependency, no `unsafe`. Not weakening or editing a gate test. Not touching the must-not-touch files. No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.

## 4. Report

Section "ADDENDUM 2 (notes before merge)": per item what changed, the test and the red row with the failure text seen; the corrected sentences quoted; the totals of check.sh and the runner; head SHA and `git ls-remote origin m1-relay-identity`. Last line exactly:

`READY FOR MERGE CHECK M1-RELAY-IDENTITY r3`
