BLUF: RULED (a): fix the 6 alerts in the TEST code, on rd-460-c170-turn-s101o on top of fd8ff2a; never dismiss (Kam's rule: a CodeQL alert is fixed in code, never dismissed by a seat or by Tuesday; option (b) refused). Then HOLD the land: the changed test bytes get a tier-2 through-code delta check as an extra item of gate 28 (the RD-476/856/857 batch), which Tuesday launches next. Land C-170 only on that verdict + Tuesday's GO. SUPERSEDES ANSWER-18 item 3's "then land with land.sh" for this turn.

Do, in this order:
1. ONE test-only commit: a single full regex-escape helper (escape . * + ? ^ $ { } ( ) | [ ] and backslash; the standard `s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')` shape) used at the 5 RegExp sites (#266-#270), which should also clear #271's three flows. No product byte changes; no assertion's MEANING changes (each regex must still match exactly what it matched before for the real constants: show it with one line per site, old regex vs new regex, against the same input).
2. Red-first: each touched cell still goes RED on its existing planted-FAIL input, and GREEN restored. The 19 gate-26 suites by name (412/412 expected), the full verify, C-57/C-133 (expect the same 33 accounted).
3. Push to rd-460-c170-turn-s101o; CodeQL on refs/pull/96/head = 0 new at any severity with your fired control; #266-#271 read by number (expected fixed on the PR ref).
4. Mail "READY FOR QA: C-170 delta" with: the new head sha + tree, `git diff fd8ff2a <new>` numstat (expect 4 paths: 3 tests + helpers/shipped-plan-build.js or a new helper file; name it), the per-site old/new regex lines, the red/green evidence, the verify line, the CodeQL read. Then hold. Your correction on gate 26's branch claim is accepted (record it as a finding in HISTORY.md at wrap).

Unchanged: no product byte, no dismissal, no merge until Tuesday's GO, Deploy demo must skip at the eventual land (gate 26 checklist item v).

-- Tuesday
