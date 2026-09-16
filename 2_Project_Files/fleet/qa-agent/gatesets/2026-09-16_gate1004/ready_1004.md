SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1004 KS-932 @6d077d3fe35cd5f3c09d394553d320e97b1abe32
TIMESTAMP: 2026-09-16T12:54:10.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
PR #1004 (KS-932) is READY FOR QA at head 6d077d3fe35cd5f3c09d394553d320e97b1abe32. One product file, packages/shared/src/security/ssrf-guard.ts (+12/-3), plus one test file. timeoutMs now bounds DNS resolution (the lookup races a timer), and DNS shares one budget with the request. shared is consumed by every service. Closes KS-932 (link: closes).

## Recommendation
Launch its QA gate at 6d077d3fe35cd5f3c09d394553d320e97b1abe32. Two things to weigh:
(1) a DNS timeout reports reason 'blocked', as other resolve failures on this path do, not 'request_failed';
(2) cell 2 is a wall-clock bound (550 ms vs ~400 ms measured), and cells 2 and 3 connect to 203.0.113.7, relying on it hanging.

## Detail
PR: https://github.com/Secuura/Distributed_Secuura/pull/1004
Branch: feature/ks-932-ornith-timeout-bounds-dns, one commit on develop 5b4f38a48. 2 files, both packages/shared.
Ticket: KS-932. Facts comment fd49db12-0fbc-4a99-bfe9-727db8e1fdee (no mentions; anchors read back).

Test Evidence summary:
- Red before green: test section alone 2/3 red (expected false to be true; expected 632 to be less than 550), control green. After the product hunk: 3/3.
- Tampers (ssrf-guard.ts restored to its sha after each row; AssertionErrors only):
  - DNS race removed (remainingMs kept): cell 1 only red.
  - Budget unshared (request deadline back to timeoutMs): cell 2 only red (637 < 550).
  - T0 and T0-after green.
- Stability: the new file 5 runs, 3/3 each.
- packages/shared 44 files / 842 tests pass (baseline 43 / 839). shared build rc 0. tsc -p packages/shared rc 0.
- Consumer smoke: api-gateway 39 / 371 pass (= baseline); tsc rc 0.
- eslint: 0 errors; 1 warning (ssrf-guard.ts:497 prefer-const), the same on develop.
- Pre-push (12:48:12Z -> 12:53:07Z): PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED (3, 4, 8). Nothing failed. PROTOCOL-CLEAN, first push.

NOT done / NOT covered:
- Other @secuura/shared consumers' suites.
- Platform suites (Schemathesis scoped to A7/A11 at 21:15).
- Preflight legs 3/4/8.
- The losing lookup promise is not cancelled; it runs on in the background after the call returns.

Accommodations: git apply --3way fell back to a direct apply ("repository lacks the necessary blob"), rc 0. The applied -/+ lines equal the READY's, 15 of 15 in sequence.

Slip, not affecting the PR: editing my PR body draft through an unquoted heredoc made zsh try to execute a backtick path ("permission denied"). The file came out correct (read back); noted in the records.

Seat A open PRs awaiting GO: #1002 (KS-1123), #1003 (KS-1165 F-1), #1004 (KS-932) = 3, at the limit. I start nothing new until a GO lands and a merge frees a slot. Next up then: A6 KS-844.
