From Friday (laptop seat), Datasec / Security Composer. Replies and wraps go to friday-laptop-agent@agentmail.to (your STATUS file is the wrap).
# BRIEF B142 · SEAT-C: fix CodeQL alert #24 (js/incomplete-sanitization) on PR #75, in code — never dismiss
**Fired: 2026-10-13 06:38 AEDT.** Pane `Datasec/Security-Composer-C`. Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B142_SEAT-C_codeql-b139-test-regex-escape.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` as the project's record. QA tier 3 (Friday reviews the diff). Round 1. The last SEAT-C seat, B139, is finished (STATUS last line `READY FOR GATE: b139/comments-and-pdf-template-version d535fb18…`; gate B141 GO WITH NOTES).

## Why
PR datasecau/Datasec-Security-Composer#75 (head `b139/comments-and-pdf-template-version` d535fb187f9bb2a0a299ecf322e8152e7cbfb109) did not merge: merge_when_green "STOP — failing checks … CodeQL=failure". Code-scanning API (`?ref=refs/pull/75/head&state=open`, read by Friday ~06:4x AEDT): ONE alert:
`#24 js/incomplete-sanitization (warning) packages/renderers/test/b139-pdf-template-version.test.ts:35 — "This does not escape backslash characters in the input."`
Lines 32-36 at d535fb18 build `new RegExp(\`Document template\\s+${…replace(/[.()/]/g, "\\$&")}\`)` — the escaper covers `. ( ) /` only. Datasec org policy (Kam 2026-09-29): fix in code, never dismiss.

## Do
0. `git fetch origin`; `ls-remote origin refs/heads/b139/comments-and-pdf-template-version` must read d535fb18…; else STOP: NEEDS FRIDAY.
1. In a worktree on that branch (commit ON it so PR #75 picks it up; no rebase): escape EVERY regex metacharacter, backslash included (e.g. one local `escapeRegExp` with `/[.*+?^${}()|[\]\\]/g`), or match the row without building a regex from the value (a string `includes` on the normalised text) — say which and why. Test file only; no product change.
2. Prove: `packages/renderers` tests green (counts base vs head), the b139 test still FAILS on the brief's tamper (render a `/1` PDF row → red; restore, sha equal), typecheck + lint + format:check rc 0.
3. Push the branch only (fast-forward), read back with ls-remote. Write `Briefs/2026-10-13_B142_STATUS.md` (diff, counts, tamper, ls-remote line). Last line `READY FOR REVIEW: b139/comments-and-pdf-template-version <sha>` or `STOPPED: NEEDS FRIDAY`.

## HOLDS
- **Datasec only.** The product on screen is "Policy Designer" (C-62). No new words.
- No PR, no merge, no deploy, no demo, no Azure, no Jira, no history.md, never open 4_Credentials/.env, never delete, never force-push, never dismiss the alert. No stack or ports needed (unit tests only); if you run ci.sh, `install-hooks.sh` first in the fresh clone (B139's run 1 lesson).
