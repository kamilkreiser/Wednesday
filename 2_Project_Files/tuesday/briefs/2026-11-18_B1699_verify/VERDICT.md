GATE B1699: GO WITH FINDINGS @ dc688f7 on main 36c557a

G1 gate (Opus 5.5, in-session), 2026-11-18 09:07-09:20 AEDT (clocks from `date`). Target datasecau/HPSM-POC, branch b1695/hpsmpoc-picomatch-dev-audit-exception, head dc688f765fb2da0eec8a8a6d2aada9c2ce1d3a57 over main 36c557ad9255125793bfeb99abdea3b0b4d988e2.

**Landing condition (from F1): do not land until Tuesday has the HPSM-POC scope of the ruling on record (see F1).** The code, the tests and the narrowness all pass. The one open item is authority, not code.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Major (authority; not code) | **The ruled card does not name HPSM-POC.** `decision_queue.sh show nexusai-picomatch-advisory-audit-1118` (and the store row read-only: no `amendments` key, no `ruling_note`) prints client `Datasec/NexusAI`, title "NexusAI: a new advisory ... fails every PR's production audit check", option a detail **"This advisory only, lapses 18 Dec or on a fix; gated and merged; then #219 and #220 land"**, ruled a at 2026-11-18T08:36:26+11:00. The kit's quotation of that detail ("This advisory only, **in NexusAI's production audit and HPSM-POC's dev-tools audit**; lapses 18 Dec ...") is NOT the card's text: the HPSM clause is not on the card (the kit marked its quote RELAYED). The card's BLUF even contrasts the two: HPSM's braces case "was in the developer-tools check; this one is in the production check". The HPSM scope is supported only by context: the morning-plan card `datasec-morning-plan-1118` (ruled "a, Noted, carry on" at 08:35:38, 48 s earlier) told the owner the advisory "fails NexusAI's production audit and, as measured this morning, HPSM's developer-tools audit too ... The card on that is your most useful tap today". So the owner was shown both audits immediately before ruling, but the ruled words cover "this advisory" with no repo named. The shipped comment, test titles, ALLOWED line and commit message all say "under the product owner's 2026-11-18 ruling: this advisory only, in this dev-tooling audit". | Before landing, Tuesday records the HPSM-POC scope on the product owner's word: a one-tap confirm card ("the 18 Nov picomatch exception also covers HPSM-POC's dev-tools audit, last day 18 Dec: yes / no"), or Tuesday's own record that cites the morning-plan card as the scope link if Tuesday rules that sufficient. No code change is needed either way. If the answer is no, this PR is not landed. Correct the kit's quotation in Tuesday's records (the words were never on the card). |
| F2 | Minor | **The date is a reading.** The card says "lapses 18 Dec" (option a) and "until 18 Dec" (BLUF). The entry allows the advisory through the end of 18 Dec (Sydney) and fails from 19 Dec. That matches Tuesday's drafting reading and the braces precedent's `lastDay` meaning, but "lapses 18 Dec" could also be read as 17 Dec being the last allowed day. | Put the reading on the F1 confirm card ("last allowed day 18 Dec, failing from 19 Dec") so one tap settles both. |
| F3 | Minor | **"Or on a fix" is enforced only indirectly.** The entry stops applying when npm reports a different range or package (planted and measured). If picomatch publishes a fixed version while the advisory text keeps `<=4.0.7`, the entry still allows it until 18 Dec although an upgrade exists. Measured today: GitHub `first_patched_version` null, `withdrawn_at` null, npm `latest` 4.0.7. | Calendar line (below) includes `npm view picomatch dist-tags` and the advisory's `first_patched_version`. No code change. |
| F4 | Minor | **Landing drafts were incomplete.** Builder's `pr-body.md` has no `Generated with` footer; `squash-body.txt` has no Co-Authored-By trailer; `squash-subject.txt` has no `(#PRNUM)`; `landing.txt` uses `--body "$(cat ...)"`, not `--body-file`; the PR body states the ruling's scope as "in this dev-tooling audit", which the card does not say (F1). | Corrected texts are in this folder. |
| F5 | Info | **The fixture cast is type-only, weakens nothing, and has a cleaner alternative.** `SYNTHETIC ... as unknown as NonNullable<Parameters<typeof evaluate>[2]>[number]` changes only the static type of the synthetic braces fixture; every expectation is unchanged, and all 41 old rows plus the 5 new rows still run on real values. It is needed: with the cast removed, typecheck rc 2 with 2 `error TS2322` (test lines 18 and 66, the literal-typed shipped entry). Cleaner (measured in a probe copy): a JSDoc line above `EXCEPTIONS` in the .mjs, `/** @type {ReadonlyArray<Readonly<{ id: string, package: string, range: string, lastDay: string, ruling: string }>>} */` (allowJs is true in web/tsconfig.json), with no cast in the test: typecheck rc 0 (0 TS errors), the file 46/46 passed, eslint clean on both files. It sits above `const BLOCKING`, so `evaluate()` stays byte-identical. | Optional follow-up (next time the file is touched, e.g. when the entry is removed). Do not block this landing on it. |
| F6 | Info | The old row's `expect(Array.isArray(EXCEPTIONS)).toBe(true)` was dropped. `toEqual([...])` already fails for a non-array (type tag check), and frozen list plus frozen entry are both asserted. Severity changes on the same id (high to critical) stay allowed (measured), which is within "this advisory only". | None. |
| F7 | Info (process) | The gate's scratch is the session scratchpad `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/88023a68-b8d2-4ab6-842c-42b77da43a9d/scratchpad/b1699/`, not `HPSM-POC/.tools/b1699/`. The seat's hooks (`pretooluse_no_cd.sh`, pathguard) refused `mkdir` and git write verbs under the HPSM-POC project folder. No override was used. Nothing was written in the HPSM-POC folder. | None. |

## Ruling-scope result (CHECK 1 and 5)
- Card at source: ruled a "Narrow, dated exception", 2026-11-18 08:36:26 AEDT. Detail: "This advisory only, lapses 18 Dec or on a fix". No amendments. Repo not named (F1).
- Entry at head, imported by program: `EXCEPTIONS.length` 1, list and entry frozen (push and mutate both throw TypeError): `{"id":"GHSA-fc5q-39xc-vjpf","package":"picomatch","range":"<=4.0.7","lastDay":"2026-12-18","ruling":"the product owner's 2026-11-18 ruling"}`. Not wider than the card: one advisory, one package, one range, one date. The production audit step is unchanged, and no other step or advisory is touched.
- "the product owner's 2026-11-18 ruling": a real ruling of that Sydney date exists (true at source). Whether its scope includes this repo's audit is F1.

## Measured rows (this gate, own clone; node v24.21.0, npm 11.19.0; load1 9.9-17.5, all under the 24 cap and every start under 16)
| Check | Main 36c557a | Head dc688f7 |
|---|---|---|
| refs | ls-remote main = 36c557ad... | ls-remote branch = dc688f76...; ahead 1 behind 0 |
| merge | - | `merge-tree --write-tree` clean, tree b4df5a60 = head tree |
| diff | - | 3 paths: ci.yml +4 -3, audit-dev.mjs +10 -7, audit-dev.test.ts +81 -9 |
| ci.yml | - | 7 changed lines, all `#` (3 del, 4 add); 569 non-comment lines identical (control: planted run-line change flips it); both step names and both run lines present once each |
| audit-dev.mjs | - | bytes from `const BLOCKING` to EOF identical (3971 B; control: planted `>=` differs); import lines identical |
| real `node scripts/audit-dev.mjs` | rc 1, `FAIL GHSA-fc5q-39xc-vjpf (high) in picomatch <=4.0.7`, counts high 17 total 17, exactly 1 advisory object in `npm audit --json` | rc 0, exactly one `ALLOWED ... allowed until 2026-12-18 (Australia/Sydney) by the product owner's 2026-11-18 ruling`, `dev-tooling audit passed (1 allowed by a dated exception)` |
| plants on the real step (copies) | - | control copy rc 0; lastDay 2026-11-17 rc 1 (lapse text); id `...vjpg` rc 1 (FAIL plus NOTE no longer reported); range `<=4.0.6` rc 1 (advisory changed); package `micromatch` rc 1 (advisory changed) |
| Sydney boundary, real report via head evaluate() | - | 12-18T00:00+11 allowed; 12-18T23:59:59+11 allowed; 12-19T00:00+11 fail; 12-18T12:59:59Z (=18 Dec Sydney) allowed; 12-18T13:00Z (=19 Dec Sydney) fail |
| second high advisory beside it (real report + synthetic) | - | another package (critical): fail 1 allowed 1; second advisory on picomatch: fail 1 allowed 1 |
| production audit `npm audit --omit=dev --audit-level=high` | rc 0 `found 0 vulnerabilities` | rc 0, `cmp` identical |
| lint | rc 0 | rc 0 |
| typecheck | rc 0 | rc 0 |
| vitest whole | 304 files, 4340 passed, 0 failed, 0 skipped | 304 files, 4345 passed, 0 failed, 0 skipped; by title lost 1, added 6, changed 0 (control: one row dropped gives lost 2) |
| audit test file alone | 41 passed | 46 passed |
| red without the entry (head tests, main script) | - | 6 failed, 40 passed: the E5 row plus the 5 new rows |
| test date plants | - | lastDay 2026-12-19: 3 failed (pin, allow, lapse rows); 2026-12-17: 3 failed |
| infra (python 3.14.10) | not run | hidden characters `Ran 14` OK; whole `Ran 325` OK; validate.sh `validate: OK`, ResourceWarnings 0, files open 0 |
| scans over 95 added lines + commit message | - | names (9-name ban list, underscore-aware): 0 (controls 9/9 fire); B-numbers, seat, coordinator names, card ids, C-/POC-/RD- keys: 0; non-ASCII and control chars: 0; secret, tenant and host patterns: 0; phrase present 6x added lines (plus ci.yml wrapped across a line), 1x message |
| CodeQL hand rows | - | new RegExp / `\$&` / innerHTML / child_process / chmod on added lines: 0 |
| CodeQL CLI 2.27.4 `javascript-code-scanning.qls` over the two changed JS/TS files | - | 0 results (87 rules); control plant: 2x js/incomplete-sanitization fired |
| live state at 09:19 | - | open PRs 0; advisory high, `<= 4.0.7`, patched null, withdrawn null; npm picomatch latest 4.0.7; head check-runs 0 (no PR yet) |

## Builder STATUS claims
True: diff numstat; entry text; tail byte-identity; real step red at main / green at head with the exact ALLOWED line; plants date/id/range rc 1; 40/6 red, 46 green; 4340 -> 4345, lost 1 added 6 changed 0; lint/typecheck rc 0; prod audit identical; infra 14 OK, 325 OK, validate OK; npm 11.19.0; first typecheck red without the cast (reproduced). False: none of the measured claims. The kit's ruling quotation (with "HPSM-POC's dev-tools audit") is not the card's text (F1), but it is the kit's claim, not the STATUS's.

## NOT RUN
`npm run build`, e2e shards, api .NET jobs, SQL Server shards, docker jobs, hosted CodeQL: hosted CI is the proof. CodeQL csharp not applicable (no C# changed).

## Calendar (CHECK 6)
On or before 2026-12-18 (Sydney): re-check the advisory (`first_patched_version`, `withdrawn_at`) and `npm view picomatch dist-tags`. If fixed, upgrade and remove the entry. If still unfixed, the dev audit goes red on 19 Dec unless the product owner gives a NEW ruling. Do not extend without one.
