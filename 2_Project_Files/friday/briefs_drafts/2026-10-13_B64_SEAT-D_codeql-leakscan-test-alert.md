From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B64 · SEAT-D: fix CodeQL alert #11 (py/clear-text-storage-sensitive-data) on PR #31, in code — never dismiss
**Fired: 2026-10-13 05:49 AEDT.** Pane `Datasec/MPS-D`. Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B64_SEAT-D_codeql-leakscan-test-alert.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` as the project's record. QA tier 3 (Friday reviews the diff). Round 1. The last SEAT-D seat, B62, is finished (`Briefs/2026-10-13_B62_STATUS.md`, `READY FOR REVIEW: b62/leakscan-versioned 65aced89…`).

## Why
PR datasecau/MPS-Commercial-Calculator#31 (head `b62/leakscan-versioned` 65aced89068ade8d40d7ea06dbf06d0b0a7f6d91, B62's versioned leak scanner) did not merge: merge_when_green "STOP — failing checks … CodeQL=failure". Code-scanning API (`?ref=refs/pull/31/head&state=open`, read by Friday ~05:5x AEDT): ONE alert:
`#11 py/clear-text-storage-sensitive-data (error) tools/leakscan/test/test_leakscan.py:275 — "This expression stores sensitive data (secret) as clear text."`
Line 275 at 65aced8 is `fh.write("\n".join(self.planted_lines()) + "\n")` in `test_files_mode_counts_every_class_and_prints_no_value`; `planted_lines()` (:262-265) includes `SECRET_LINES["aws"]`, a synthetic key-shaped fixture. The value is fake, but the Datasec org policy (Kam 2026-09-29) is: a CodeQL alert is FIXED IN CODE, never dismissed, never bypassed.

## Do
0. `git fetch origin`; `ls-remote origin refs/heads/b62/leakscan-versioned` must read 65aced89…; else STOP: NEEDS FRIDAY.
1. In a worktree on `b62/leakscan-versioned` (commit ON this branch so PR #31 picks it up; no rebase): change the TEST so CodeQL no longer sees a sensitive value flowing to a file write, WITHOUT weakening what the test proves (the scanner must still count exactly one secret-shaped hit and print no fixture value). Read first why CodeQL classifies it as a secret (the name `SECRET_LINES`/`secret`, the key shape, or both) and say which. Acceptable shapes: build the fixture line at the write site from inert parts under a neutral name, or load it from a non-tracked fixture generated at runtime — state which and why. Do NOT change `leakscan.py` unless the test cannot be fixed alone (then STOP: NEEDS FRIDAY first).
2. Prove: the full suite 25/25 (or the new count, explained) on macOS python3 and in `python:3.12-slim`; the secret class still counts 1 in this test; a mutant that drops the secret rule from `leakscan.py` still turns this test RED (run it, restore, show the sha matches).
3. Push the branch only (fast-forward), read back with ls-remote. Write `Briefs/2026-10-13_B64_STATUS.md`: why CodeQL flagged it, the diff, the counts, the mutant, the ls-remote line. Last line `READY FOR REVIEW: b62/leakscan-versioned <sha>` or `STOPPED: NEEDS FRIDAY`.

## HOLDS
- **Datasec only.** No other client's names, tickets or paths. No real price, SKU, key or customer value anywhere — synthetic fixtures only.
- No PR, no merge, no deploy, no Jira, no history.md, never open 4_Credentials/.env or `.local/pricebooks/`, never delete, never force-push, never dismiss the alert. No ports needed.
