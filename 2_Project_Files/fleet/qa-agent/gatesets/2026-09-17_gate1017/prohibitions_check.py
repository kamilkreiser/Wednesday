#!/usr/bin/env python3
"""prohibitions_check.py — every standing prohibition phrase of the #1016 prompt, checked in the #1016 prompt (control: must be present there) AND in the
#1017 prompt. Phrases are PR-neutral substrings; whitespace normalised."""
import re, datetime
B = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/'
n = lambda t: re.sub(r'\s+', ' ', t)
p16 = n(open(B + '2026-09-17_secuura-1016-ks1072-tier1.prompt.txt').read()); p17 = n(open(B + '2026-09-17_secuura-1017-ks1195-tier1.prompt.txt').read())
PH = ['ultrathink', 'READ-ONLY — git clone --shared --no-checkout by SHA into your own', 'git write verbs there only', 'never merge-tree --write-tree',
 'git apply in the checkout', 'never enter any seat', 'another gate', 'never vitest inside the checkout', 'pin by SHA, never origin/*',
 'node_modules per ENTRY', '.vite/.vitest/.cache skipped', '@secuura/* relinked into your tree', 'NEVER link a node_modules tree wholesale — not for any package; create no node_modules where nothing runs.',
 'You are FINDINGS-ONLY. You never fix, never merge, never push, never deploy, never comment, never file, never tick an ack box, never `@`, never write to Linear or GitHub, and nothing goes to Peter or Stuart.',
 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout or any of its worktrees.',
 'NEVER print a credential value, and never open, read or copy a secrets file into output', 'by NAME from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env',
 'AGENTMAIL_API_KEY by NAME from /Volumes/DevMASTER/WEDNESDAY/4_Credentials/.env', 'and never echoes them. Count, never echo.',
 'NO shared docker stack, no :6882 / :7082 slot, no kintsugi, no demo, no az, NEVER the wallet mnemonic (KS-535 HOLD).', 'This gate needs NO container',
 'Run `docker info` ONCE and print its rc on its own line (UP is NOT permission; create no container). LOOPBACK ONLY: every listener binds 127.0.0.1:0.',
 "No Akto, no k6, no Playwright, no Schemathesis run (Kam's 40% cap; NOT COMMISSIONED)", 'YOU rule whether Schemathesis/Akto are REQUIRED, with the measured reason.', 'Time-box',
 'Hygiene: /bin/bash here is 3.2 — write runners in Python.', 'no PIPESTATUS (`cmd > out 2>&1; rc=$?`), no timeout on macOS', 'never begin a line with `=====`',
 "Your tool shell's grep may be a function: /usr/bin/grep -i with a same-file positive control; `git grep -c` prints nothing for a zero — silence is unread, not 0.",
 'Never `cd` in your own tool calls; absolute paths; git write verbs only inside script files.', 'stderr is never discarded.', 'Clocks from `date`, never estimated.',
 'Every scripted edit asserts its anchor count = 1 and a marker.', "Quote the Secuura checkout's porcelain count, .git/config sha256, for-each-ref count, .git/worktrees count, origin develop SHA,",
 'as THREE timestamped readings, plus the checkout', 'STOP — the brief is about a different SHA. develop moving is expected; judge it by content, name it.',
 'Never `rm`: fresh mktemp -d per attempt; quarantine scratch tests and configs by rename. No container is created; never touch a secuura-* container.',
 "Do no memory maintenance of your own project's memory store inside this session.", 'NOT-TESTED.written-first.md written FIRST, BEFORE any run',
 'Every finding carries its evidence class (MEASURED AT RUNTIME / PROBED / READ ONLY / RELAYED), severity, target (PR or TICKET),',
 'Name every prediction slip against its predictor', 'Client-facing communication = ticket comments only, and not from you; anything needing a push goes to Wednesday as an escalation candidate.',
 'Never delete; cleanup means quarantine.', 'Verdict: ONE line — GO, GO WITH FINDINGS, or NO GO', 'MERGE ADDENDUM', 'linkKind contributes', 'stays In Progress on merge (§5f',
 'MAIL YOUR VERDICT to wednesday-agent@agentmail.to when the pass is complete.', 'the verdict MAIL is the END STATE and the wait signal. Send it FROM coagent@agentmail.to. Subject, EXACTLY:',
 'POST https://api.agentmail.to/v0/inboxes/coagent@agentmail.to/messages/send', 'Confirm the API answered 2xx and quote the message id in your final pane line.',
 'Timestamps in the mail come from `date`, never estimated.', 'The MAIL is the end state.']
print('prohibitions_check', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), 'phrases', len(PH))
miss16 = [x for x in PH if n(x) not in p16]; miss17 = [x for x in PH if n(x) not in p17]
print('control: phrases absent from the #1016 prompt (must be only #1017 additions or wording the #1016 prompt lacked):', miss16)
print('absent from the #1017 prompt:', miss17)
print('#1017 subject exact:', '[QA -> Wednesday] TIER 1 GATE #1017 (KS-1195) cbe29597d — <GO | GO WITH FINDINGS | NO GO>' in p17, '| first line ultrathink:', open(B + '2026-09-17_secuura-1017-ks1195-tier1.prompt.txt').read().split('\n')[0] == 'ultrathink')
