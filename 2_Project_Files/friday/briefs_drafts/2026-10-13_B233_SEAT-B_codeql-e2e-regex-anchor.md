From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to (your STATUS file is the wrap).
# BRIEF B233 · SEAT-B: fix CodeQL alert #11 (js/regex/missing-regexp-anchor) on PR #147, in code — never dismiss
**Fired: 2026-10-13 03:26 AEDT.** Pane `Datasec/HPSM-POC-B`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B233_SEAT-B_codeql-e2e-regex-anchor.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. QA tier 2 (through-code; Friday reviews the diff). Round 1. The last SEAT-B builder, B231, is finished (STATUS last line `READY FOR GATE: b231/reset-words-bff-table-f22 545f010…`), and gate B232 passed it.

## Why
PR datasecau/HPSM-POC#147 (head `b231/reset-words-bff-table-f22` 545f010ab59c7eddd58519e840ba3305e2f9c5a5, gate B232 GO WITH NOTES) did not merge: the CodeQL check failed on ONE open alert, read by Friday from the code-scanning API (`?ref=refs/pull/147/head&state=open`) at 03:2x AEDT:
`#11 js/regex/missing-regexp-anchor (warning) web/e2e/hosted-reset.spec.ts:40 — "Misleading operator precedence. The subexpression '^Demo reset:' is anchored at the beginning, but the other parts of this regular expression are not"`
Line 40 at 545f010 reads: `  const said = page.getByText(/^Demo reset:|could not be reset/);`
The Datasec org policy (Kam 2026-09-29): a CodeQL alert is FIXED IN CODE, never dismissed, never bypassed. PR #146 (B230) has merged, so main is now a5fd6355122de2db155e6dd5c199f13bcf138cdd (GitHub refs API, 03:25 AEDT).

## Do
0. `git fetch origin`; `ls-remote origin refs/heads/main refs/heads/b231/reset-words-bff-table-f22` must read main a5fd6355… and head 545f010a…; else STOP: NEEDS FRIDAY.
1. In a worktree on `b231/reset-words-bff-table-f22` (under `.tools/`, named `wt-B233`; commit ON this branch so PR #147 picks it up; NO rebase, NO merge of main), change ONLY line 40's regex so the precedence is explicit and the same two outcomes match: the success sentence (starts with `Demo reset:`) and the failure sentence (contains `could not be reset`). Read the failure text(s) the web can actually show (`git grep -n 'could not be reset' web/src`) and pick a form whose meaning you can state in one line, e.g. `/^(?:Demo reset:|.*could not be reset)/` or two explicit alternatives. State which and why.
2. Prove it: run `web/e2e/hosted-reset.spec.ts` in the SAME Playwright project B231 used (B231 STATUS :58, "hosted project") at the new head, green ×3; plus web lint and typecheck. Counts and commands in the STATUS. If the spec cannot run on this laptop, say exactly why and run lint + typecheck + a node one-liner showing the new regex matches both real sentences and not an unrelated line.
3. No other file changes; no product code; no new words.
4. Push the branch only (`git push origin b231/reset-words-bff-table-f22`, fast-forward), read back with ls-remote. Write `Briefs/2026-10-13_B233_STATUS.md`: the diff, the commands + counts, the ls-remote line. Last line `READY FOR REVIEW: b231/reset-words-bff-table-f22 <sha>` or `STOPPED: NEEDS FRIDAY`.

## HOLDS
- **HP Restricted material.** No HP Restricted document is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)). Do not open `HP Reporting and Docs/` or the SOW file in the project root.
- **Datasec only.** No other client's names, tickets or paths.
- No PR comment, no merge, no deploy, no Jira, no history.md, never open 4_Credentials/.env, never delete, never force-push, never dismiss the alert.
- Ports if needed: 6970-6979 (`lsof` first); stop any process of yours by port + cwd, never by name.
