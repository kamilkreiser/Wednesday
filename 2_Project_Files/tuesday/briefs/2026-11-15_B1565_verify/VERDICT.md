GO WITH FINDINGS
GATE B1565: GO WITH FINDINGS @ 349f7a7 on main b6c282e

G1 gate (security surface: whether the API believes a forwarded address), round 1 of 2, class HPSMPOC-193 forwarded-address trust. Ran 2026-11-15, 12:37 to about 13:00 AEDT.
- Head: 349f7a78f25cb1933214b277a80daa12bf9d15d3, 1 ahead and 0 behind main b6c282ee50086bc1ac7d773ccabf00fcf8c055cc.
- `git ls-remote` read both refs at 12:38. Open PRs: 0 (control: `pulls/99999` gives 404).
- My own clone and worktrees `head`, `mut` and `base` are under `fleet/state/s277/g1565`. The push URL is `invalid://no-push-gate`; nothing was pushed.
- Toolchain: dotnet 10.0.404 (the project's `.tools/dotnet-10.0.404`, equal to `global.json`), node v24.21.0 (`.nvmrc` 24), Python 3.14, bicep 0.47.16, CodeQL CLI 2.27.4.

## BLUF

The branch carries out the ruling. With the shared value absent, wrong, empty, sent twice, comma-joined, padded or in another letter case, a trusted peer's `X-Forwarded-For` is removed before anything reads it. That holds with the platform switch on or off, and for `FollowUp:TrustedProxies` too. The proof header is always removed. The compare is `CryptographicOperations.FixedTimeEquals` over the SHA-256 of each side. No value configured means nothing is believed. A malformed value stops the host with a message that names the key and not the value. The web sends the value only beside the address on the client session call. It never copies the browser's header and never logs the value.

Every mutant I planted except one went red. The exception is a value-equal plaintext `==` (Info 1), which no functional test can catch.

No Blocker, no Major. 2 Minor, 6 Info.

## Findings

| Sev | Where | Finding | Measurement |
|---|---|---|---|
| Minor | api/src/HpsmPoc.Api/Program.cs:130 | The new start-up line fires only when `KnownNetworks`/`KnownProxies` are set without a value. When `FollowUp:TrustedProxies` is set without a value, that reader also silently stops believing `X-Forwarded-For`, and nothing is logged. Hosted `FollowUp:TrustedProxies` stays empty (FollowUpLink.cs:43, :86), so there is no effect today. It is an operator-signal gap for whoever sets it later. | Source reading. Row `The_follow_up_link_own_trusted_proxy_is_believed_only_with_the_web_front_end_value` pins the behaviour, not the log. |
| Minor | builder evidence `landing.txt`, `pr-body.md` | `landing.txt` uses `<PR-NUMBER>`, relative `cat` paths and `--body "$(cat ...)"`. `pr-body.md` quotes a ticket comment id and drops the required emoji footer. The files here replace them in the precedent's form: absolute `--body-file`, `<N>`, and the standard's footer. | Read the files. |
| Info | api/src/HpsmPoc.Api/Auth/ForwardedClientAddress.cs:85 | The constant-time property is held by source and review only. Mutant M1b keeps the plaintext and compares it with `text == ProofPlain`. That is value-equal but not constant time, and it stays green: 98 of 98 (the 89 branch cases plus 9 probes). The reference `==` mutant M1a goes red (10 red). This is inherent: timing cannot be unit-pinned. The source is right, and the C# hand row finds 0 `==`/`Equals` on the value. | Mutant runs (`out/M1a_reference_eq.trx`, `out/M1b_string_eq_plaintext.trx`). |
| Info | builder FOR TUESDAY, deploy-ordering note | **My judgement: the behaviour is right, and it is NOT a finding for this branch.** It is a requirement on the later infra change. A literal `@Microsoft.KeyVault(...)` text, an unresolved reference, is outside the value form. The host refuses to start with `ForwardedHeaders:Proof must be 32 to 128 characters ...; refusing to start.` Neither the exception nor any captured log line holds the reference text (probe P7, measured with a Key-Vault-reference-shaped value). Refusing a malformed trust setting at start-up is this file's existing pattern for the three list keys, and it is loud rather than silently insecure. This branch sets no hosted value, so nothing can be unresolved yet. The infra change must (a) confirm that the API's identity can resolve the reference before it adds `ForwardedHeaders__Proof`, (b) store the secret with no trailing newline, which would also be refused, and (c) let its deploy check catch a stopped API. | Probe P7 green at head and red at main ("No exception was thrown"). |
| Info | web/src/server/bff.ts:32-33 vs ForwardedClientAddress.cs:69-75 | The two sides answer a malformed value differently. The web drops it silently (kit D-3) while the API refuses to start. A malformed web value therefore fails closed with no signal on the web side. The infra change should check both apps. | Source; web row "drops a value outside the form" (7 bad values, 3 edges sent). |
| Info | web/src/server/bff.ts:314-319 | Trust now rests on the web's choice of the LAST `X-Forwarded-For` entry. That choice is safe only if App Service's front end appends the real client address and passes `X-Hpsm-Web-Proof` unchanged to the API. Both are UNMEASURED: they are the hosted measurement on the backlog, not this branch. Nothing here changed the web's address choice. | Source reading; `git diff` shows the address lines unchanged. |
| Info | gate probes (not in the branch) | Edge cases the branch's own tests do not spell out all hold at head: a lower-case proof header name with the right value is believed (P1); a lower-case `x-forwarded-for` without proof is removed (P3); a comma-joined value (P2), a space-padded value (P4) and `[value, ""]` (P5) are not believed; whitespace-only config refuses and empty config starts believing nothing (P8, P9). P2-P9 are red at main, and P1 is green at both. | `probes/GateProbeTests.cs`: 9/9 at head; 8 red, 1 green at main. |
| Info | fail-closed consequence | Until the value is stored on both apps, unknown-link openings share one bucket per connecting address. Real links keep their per-token bucket (FollowUpLink.cs:269-273), and the global ceiling holds. The only other address-keyed limiter is the feedback limiter, which is keyed by tenant and object id (FeedbackModule.cs:197-198), so it is unaffected. | Source reading. |

## What I checked as an attacker, and the result

1. **The compare.** `ProofMatches` returns false unless exactly one non-empty value is sent. It then runs `FixedTimeEquals` over two 32-byte digests (ForwardedClientAddress.cs:81-86). Its early returns depend on the count and emptiness only, never on secret bytes.
2. **Removal on every path.** In the gate (ForwardedProofGate.cs:20-22), a value that does not match removes `X-Forwarded-For`, and `X-Hpsm-Web-Proof` is removed unconditionally. `HeaderDictionary` is case-insensitive (P1, P3). Each case was measured red-or-green by assertion: absent, wrong, empty, one character changed, another letter case, sent twice, `[value, ""]`, comma-joined, padded.
3. **No reader before the gate.**
   - Pipeline order: `UseRequestTimingLog` (it reads no header or address; RequestTimingLog.cs:12), then the gate (Program.cs:134), then `UseForwardedHeaders` with explicit options (:136), then the exception handler, authentication including the Development sign-in (:156), and the rate limiter (:158).
   - The platform switch's own start-up-filter middleware gets `ForwardedHeaders.None` (Program.cs:46-50, ForwardedClientAddress.cs:131-137). Mutant M4 gives it the lists, and 2 rows go red.
   - `FollowUpLink.ClientAddress` (FollowUpLink.cs:280) runs in the endpoint, after the gate.
   - No `IStartupFilter`, HTTP logging or W3C logging in `api/src` (grep 0).
4. **Logs.** I captured every log line at Trace across 4 hosts with right and wrong values and the switch on: 76 lines, 0 holding either value. A planted copy is found (P6). The start-up line and the refusal hold constants only. The refusal does not call `Refuse` (ForwardedClientAddress.cs:166), which writes values. No test name holds a value: the names are descriptive, and the values are built in code.
5. **Configuration.** A malformed value refuses and names the key (5 branch rows plus P7 and P8). No value configured is fail-closed (`With_trusted_proxies_and_no_value_configured...`, P9).
6. **Web.**
   - The value is set only inside `if (address)` on the client session path (bff.ts:314-319).
   - `FORWARD_REQUEST` (bff.ts:149) does not hold the header, so the browser's copy never passes.
   - Mock mode sends nothing upstream.
   - The value form is a regex literal (bff.ts:32), and the value is never in `console.*` (the grep finds 3 `console.warn`, each holding a route or a reason only).
   - `ApiMode` is never serialised or logged (`resolveMode` callers: bff.ts:68, :419).
7. **Infra line** (test_security_baseline.py:435). It is one dict entry, and its reason is true: bff.ts reads the variable, and no hosted setting exists. Control: head's code with main's file makes `rule_web_settings` fail (1 failure); with the line, 138 OK.

## Mutants (each in my scratch `mut` or `head` copy, restored after; the API ones ran the 3 branch classes plus 9 probes, 98 cases)

| Mutant | Result |
|---|---|
| M1a `SHA256.HashData(...) == ProofDigest` (reference `==`) | 10 red: right-value rows, the edited bucket row, H106, the switch row, 32/128, P1, P6 |
| M1b plaintext `text == ProofPlain` (value-equal, not constant time) | 0 red (Info 1) |
| M2 first spelling: did not compile (CS9113, an unread primary-constructor parameter) | its test run used stale binaries; DISCARDED, not counted |
| M2b removes `X-Forwarded-For` only when the header is absent, not when wrong | 12 red: all 5 wrong-value rows, no-value-configured, row 9, P2, P4, P5, P6, P9 |
| M3 the proof header not removed | 1 red: `The_web_front_end_value_is_gone_from_the_request_once_the_pipeline_has_read_it` |
| M4 the platform switch's middleware gets the lists (A4 undone) | 2 red: the switch row, P6 |
| M5 `sent.Count < 1` (several values accepted) | 2 red: "sent twice", P5 |
| W1 web sends the value without the address | 1 red: "is never sent on another path ... without an address" |
| W2 web form not checked | 1 red: "drops a value outside the form" |
| W3 browser's `x-hpsm-web-proof` added to `FORWARD_REQUEST` | 1 red: "never passes on the browser's own copy" |

## Measured (this gate)

1. **Refs, scope and merge.**
   - `merge-tree --write-tree main head` rc 0, tree 9d29cfe5, which equals head's own tree.
   - 9 changed paths, all on the kit's OWNS list.
   - `FollowUpHardeningTests.cs` hunks: `OpenFrom` (:302-307) and `TrustedProxyFollowUpFactory` (:347-361) only.
   - The infra file: +1 line, -0.
   - No bicep, `infra/modules`, `infra/env`, `.github`, `web/src/components`, `web/e2e`, `scripts` or `Modules.Assessment` path.
   - Sibling overlap: H-1 has landed, H-3 has no kit, open PRs 0.
2. **Commit.**
   - 1 commit with 1 parent (main).
   - Subject: 84 characters, ASCII.
   - 1 trailer (`Co-Authored-By`).
   - Author and committer email equal the project's configured email, compared by program locally and through `gh api -X GET commits/<sha>` (control: a wrong value differs).
3. **Red first** (head's 4 changed or new test files plus my probes on main's product code):
   - API: 16 of 22 `ForwardedProofTests` red, every one by assertion (Values differ, or No exception was thrown). The other 6 are green, and so are all 38 + 29 rows of the two edited classes.
   - Web: 3 of 23 red, exactly the builder's three.
4. **Head runs.**
   - The 3 API classes: 89 passed, 0 failed (22 + 29 + 38).
   - The web `src/server` files plus `web-settings.test.ts`: 41 files, 1336 passed, 0 failed, 0 skipped (`bff.client.test.ts` 23, `web-settings` 4).
   - Lint (max-warnings 0) on the 2 changed web files: rc 0. Typecheck: rc 0.
   - Infra `test_security_baseline.py`: 138 OK at main and at head. `test_hidden_characters.py`: 14 OK at both.
   - The API test project whole on the default host: see the next item.
5. **Whole API test project at head** (default SQLite host, no Azurite): rc 0, 2310 Passed, 0 failed, 13 NotExecuted. The 13 are the Blob tests ("Azurite not configured"), which matches the builder's 2310 + 13. Every one of these tests builds the changed `Program.cs` pipeline.
6. **CodeQL pre-scan (local CLI 2.27.4; a PRE-SCAN, not hosted CodeQL).**
   - `javascript-typescript`, `javascript-security-extended.qls` over the head clone: 0 results, 103 rules. The database holds 628 `web/src/**.ts(x)` files, including `bff.ts`, whose sha equals the head blob, and `bff.client.test.ts`. Control: a planted quote-only `.replace` escape gives 1 result, `js/incomplete-sanitization`.
   - `python`, `python-security-extended.qls`: 0 results, 50 rules. The database holds `test_security_baseline.py`.
   - **`csharp`: NOT RUN.** `database create --build-mode=none` fails with `Semmle.Autobuild.CSharp: Bad CPU type in executable`: the extractor is x86_64, and this arm64 machine has no Rosetta (`arch -x86_64 /usr/bin/true` fails).
7. **Hand rows** over all 505 added lines in 9 files, test files included:
   - C#: a value or header in a log call, exception or interpolation 0; `==`/`Equals` on the value 0; a regex from a variable 0.
   - JS/TS: `new RegExp(` from a variable 0; `$&` hand-escapes 0; `innerHTML` and `child_process` 0; a value in `console.*` 0.
   - **Sensitive-NAME row:** 44 added lines match the words. Each is the `HpsmPoc.Api.Auth` namespace, a follow-up link `token` argument sent in a request body, or `devAuth`. None writes a value whose name matches to a file, log, print or stdout. The proof constants are named `proof`, `Proof`, `browsers` and `value`.
   - Python: the one line is a dict entry; no write.
   - Hit count: 0.
8. **Names and hygiene.**
   - The underscore-aware name scan over the standard's ban list plus the configured user name: 0 on added lines and in the message (control: `_by_<name>_` fires for every name).
   - Work ids (`B[0-9]{3,4}`, `HPSMPOC-[0-9]`, the coordinator names, `SEAT`, `H164`): 0 in the message and 0 on added lines (control fires).
   - Non-ASCII on added lines and in the message: 0 (U+00A0 and U+202E controls fire).
   - GUIDs 0. Hosts 0.
   - Value-form string literals: 1 hit, a `cref` identifier in a doc comment (ForwardedProofGate.cs:7), not a value. The test values are built in code.
9. **Load.** load1 stayed between 6.6 and 16.2 at every heavy start, always under 24 (`logs/loadgate.log`).

## Claims (builder STATUS)

- **True, re-measured:** 9 paths in OWNS; 1 commit with the configured identity; 89 at head for the 3 classes; red-first 16/22 API and 3/6 web, by assertion; `ORDER: switch off ignored, switch on believed` (indirectly: M4 reds the switch row, so the switch's middleware does run ahead of `Program.cs`); the infra control; CodeQL JS and Python 0; C# not runnable locally; the kit's design names exactly.
- **Not re-measured (builder-only):** web whole 4264; the api job 4115 with Azurite; both SQL Server shards (1453 and 1348); the e2e shard `journey-and-prototype`; `validate.sh` with bicep; `npm run build` and the audits.
- **True with a note:** the builder's two control mutants are confirmed in kind by M2b and M1a.

## NOT RUN (by this gate)

- **SQL Server shards:** not rerun. No finding needed them, and no `g1565-*` container was started. The builder's whole-shard runs are relayed.
- **Web:** whole vitest (only `src/server` plus `web-settings`); `npm run build`; audit-dev; `npm audit`; `--check-shards`.
- **E2E:** all 8 shards.
- **Infra:** `validate.sh` and the full `unittest discover` (only the security baseline and hidden characters).
- **API job:** the api job with Azurite, and the Blob tests.
- **Secrets:** gitleaks (the hand secret and GUID scans ran).
- **CodeQL `csharp`** (see above). Hosted CodeQL (actions, csharp, javascript-typescript, python, extended) is the proof.
- **Hosted:** nothing hosted, by fence: no az, no Jira, no PR, no message.

## FOR TUESDAY

- Land through hosted CodeQL. Never bypass it, and dismiss no alert. C# has no local pre-scan.
- Card the infra change with the deploy-ordering requirements in Info 2: resolve before set, no trailing newline, a deploy check for a stopped API. Check both apps (Info 3).
- The hosted measurement (the front end's header shape) now also covers whether `X-Hpsm-Web-Proof` reaches the API unchanged.
- Optional follow-up for Minor 1: a start-up line when `FollowUp:TrustedProxies` is set without a value.
- Resources: everything is under `fleet/state/s277/g1565`: the clone, 3 worktrees, CodeQL databases, probes, logs and `_quarantine`; nothing deleted. No container was started and no server was left running. The three worktrees are porcelain-clean apart from my probe file in `mut` and `base` and the copied test files in `base`.
