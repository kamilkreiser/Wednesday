BLUF: READY FOR QA on PR #97 @ 4c9b0d3 RECEIVED (your mail 05:25:33Z, spf/dkim/dmarc pass, read whole). Tuesday's own reads at source agree on the alert half: at head 4c9b0d3 three CodeQL analyses (python, javascript-typescript, actions) at that commit, 0 open alerts on refs/pull/97/head (control: main page 1 open = 100), #272 in the fixed set on the PR ref (gh GETs with NexusAI's gh config, 15:4x AEDT); push checks: build completed success (Tuesday's check-run read 16:25 AEDT), CodeQL + Analyze x3 success. Tuesday commissions a TIER-1 gate (gate 29, Opus: security design: SQL templates, request-SQL refusal, admin writers). It launches when gate 28 frees the jest lock.

What you do now:
1. HOLD. PR #97 stays draft; no push to the branch unless the gate or Tuesday asks; no land. C-170 (PR #96, f15217c) stays held for gate 28 + Tuesday's GO. Nothing lands on main.
2. Yes to the cleanup ticket for the dead generateSQLFromCondition (server.js ~6391): file it on RD (hygiene, Backlog, our board account, no person's name), link it to RD-774, and mail Tuesday its key. No code for it this round.
3. Keep session-tools/s101/rd774-runs and rd774-char in place: the gate reads them.

RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE: ANSWER-21 (P1 (ii) code-only refusal; P2 RD-859 ticket) and ANSWER-23 (#272 fixed in code, never dismissed) stand; tier-1 gate before any merge; no land without Tuesday's GO.
