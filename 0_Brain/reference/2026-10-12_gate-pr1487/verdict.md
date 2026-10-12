# Gate PR #1487 (KS-1480) - GO WITH NOTE
Head 9b2a845291d7511f75e01546f957cb9c89d32293 (tree da9414f9, verified from bundle). Merge predicted vs 1b7b8d7d5 (newest develop found, in worktrees s-f17-ks1317; the shared repo itself lacks a28ed5d): clean, no gateway file touched by develop's 2 newer commits. No cloud CI (Actions down) - not a verdict input.

Scope: 2 files (rateLimitEnforce.ts +12/-2, new ks1480 test +118). No other change.
Runs: tests-first 96c35d977 = 9 cells, 4 RED (E1-E4) + 5 green; head = 9/9 green. Gateway suite head and merged: 108 files / 1028 tests pass; tsc rc 0 both; eslint 0 errors (36 warnings, none in this file) both; no-control-regex control file fails as expected (live).
Tampers (seat 5): T1 3 red, T2 1, T3 4, T4 1 reproduced; T5 (quotes re-kept) 0 red (seat claimed 1).
My own: M1 drop DEL 0x7f = 0 red (SURVIVES); M4 drop C1 0x90-0x9f = 0 red (SURVIVES); M2 NEL 1 red; M3 U+2029 1; M5 no-slice 1; M6 backslash unescaped 1.
Direct attack (27 inputs incl. CR LF CRLF NEL VT FF LS PS ESC[ TAB NUL DEL all C1 lone surrogates, 200KB value, JSON-closing payload, objects): 0 raw leaks, 0 collisions, control (identity) leaks. Ordinary ids byte for byte. NBSP/ZWSP/bidi/BOM kept raw (not line-splitting).
Source: no raw U+2028/2029/BOM/ctl; only em-dash and multiplication sign (comments/template, pre-existing).
All log sites: only warnNoAllowance interpolates into a string; logDegraded and the two logger.error pass clientId as structured meta (JSON-encoded in winston prod and dev format) - safe. authMethod unescaped but reachable only after MACHINE_AUTH_METHODS.has() (api_key, oauth_app), line 159.

Defects
1. Minor - ks1480 test: no cell pins DEL (0x7f) or C1 0x90-0x9f; the claimed "DEL, C1 controls" range survives narrowing (M1, M4). Test file E3 only covers 0x85.
2. Minor - test file: no cell has a double quote, so quote handling (seat attack 1) is unpinned; T5 survives, seat's "1 red" not reproducible by my equivalent tamper.
3. Minor - rateLimitEnforce.ts:123 / :61: no test pins MACHINE_AUTH_METHODS closed, so the unescaped authMethod is safe by construction only.
No Major.
