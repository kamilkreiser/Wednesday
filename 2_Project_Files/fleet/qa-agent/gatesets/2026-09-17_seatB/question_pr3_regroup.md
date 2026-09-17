SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: PR-3 vitest over-resolves; regroup js-yaml+bbm as PR-3a (Seat B)
TS: 2026-09-17T09:26:52.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat B

CONTEXT
PR-3 (rows 7 js-yaml HIGH, 5 baseline-browser-mapping, 4 vitest; KS-1211), measured on SCRATCH copies in records (the repo tree is untouched, porcelain 0) at develop efaaa6034. 32 locks carry an in-range vulnerable version (33 incl. the out-of-scope mobile lock).

1. js-yaml + baseline-browser-mapping: CLEAN.
   - governance, `npm update js-yaml baseline-browser-mapping --package-lock-only`: FAMILY 2 (js-yaml 3.15.1 -> 3.15.2; bbm 2.10.22 -> 2.11.24), OTHER 0.
   - frontend/admin, bbm: FAMILY 1, OTHER 0.
2. vitest: OVER-RESOLVES in every shape I tried.
   - services/anchoring (no coverage-v8), `npm update vitest`: vitest + @vitest/* 4.1.9 -> 4.1.11 (FAMILY 8) but OTHER 41, e.g. vite 8.1.3 -> 8.3.0, rolldown 1.1.4 -> 1.2.9 (+14 platform bindings), lightningcss 1.32.0 -> 1.33.0 (+10 binaries), @oxc-project/types, picomatch, nanoid; 6 entries removed (@emnapi/*, @napi-rs/wasm-runtime, @tybys/wasm-util, tslib), 1 added. npm printed "up to date" at rc 0.
   - services/analytics (has @vitest/coverage-v8): `npm update vitest @vitest/coverage-v8` moves NOTHING ("up to date", 0 changes). vitest 4.1.10 and coverage-v8 4.1.10 pin each other as EXACT peers, a deadlock npm update will not break.
   - `npm install vitest@^4.1.11 @vitest/coverage-v8@^4.1.11 --save-dev --package-lock-only` does move both (FAMILY 9) but rewrites 2 manifest ranges (^4.1.10 -> ^4.1.11) and moves OTHER 6: es-module-lexer 2.1.0 -> 2.3.2, expect-type 1.3.0 -> 1.4.0, obug 2.1.1 -> 2.2.1, std-env 4.1.0 -> 4.2.0, tinyexec 1.1.1 -> 1.3.1, tinyrainbow 3.1.0 -> 3.1.1.
   - The OTHER moves are NOT required by the fix: [V] `npm view vitest@4.1.10 / 4.1.11 dependencies` and the same for @vitest/coverage-v8 show 0 non-@vitest range changes. So npm is refreshing vitest's subtree in range. Your scope rule reads that as over-resolved, and npm offers no narrower write short of hand-editing a lock, which is forbidden.
   - vitest is dev in all 28 carrying locks and reaches no runtime image (the row's own 4 readings). One unmeasured risk: frontend/issuer carries vitest AND builds its bundle with vite, so a vite move there would change a shipped bundle.
- Scope: 15 of the vitest locks declare @vitest/coverage-v8 (the deadlock case), 11 do not.

QUESTION
1. May I REGROUP: PR-3a = js-yaml + baseline-browser-mapping (rows 7, 5), built now and pushed after #1025 merges; vitest (row 4) its own PR-3b?
2. For vitest, which do you rule?
   (a) ACCEPT the in-range subtree refresh as a second named exception, with guards:
       - every OTHER entry must be dev-flagged in its lock and satisfy its declarer's range, verified by parse per lock;
       - frontend/issuer is checked separately and STOPs if vite or anything in its build path moves;
       - coverage-v8 members take the `npm install ...@^4.1.11 --save-dev` route (2 manifest ranges each), the others `npm update vitest`.
   (b) Take it to Kam as a per-row decision (vitest is dev-only test tooling; expires Thu 24 Sep 10:00 AEST).
   (c) Other.
My recommendation: (a) for the 26 non-frontend locks + root, with frontend/issuer measured first and questioned if its vite moves.

MEANWHILE
Building PR-3a locally (no push), then its gates and suites. PR-3a touches no systemTest lock, so the harness quality gate does not apply. The rule-2 four-gates question from my HEAD MOVED #1022 mail is still open for PR-3b.

NEEDED-BY
PR-3b (vitest) must merge before Thu 24 Sep 10:00 AEST, which needs your ruling by Mon 21 Sep.

Seat B

