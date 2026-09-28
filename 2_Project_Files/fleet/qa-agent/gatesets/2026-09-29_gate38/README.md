# Gateset 2026-09-29_gate38 — README for Wednesday

Written 2026-09-28T16:23:50Z by the drafter (make_readme_gate38.py; every figure below is read from the kit's own output files at that moment, each named beside it).
The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory and scratch under its session scratchpad `.../scratchpad/g38/` (the scratch clone `g38_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, fetched FROM ORIGIN with the checkout's repo-local key; the Postgres data dirs `g38_pg/data_*` (kept, stopped); the git-archive extracts `g38_pg/base|head`; the control workdirs `g38_controls_*`). OUTSIDE the scratchpad it created only short, empty unix-socket dirs `/tmp/q38.*` for the throwaway Postgres (the scratchpad path is too long for a socket). It did NOT write the routing line (§4).
The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its tsx and pg). GitHub: REST GET only. Linear: queries only. AgentMail: three BY-ID reads (the two READY mails and the seat STATUS mail Wednesday relayed; inbox_digest.sh full), no listing, nothing sent. decisions.json and inbox_routing.conf: read only.

**gate38 = FOUR PRs (T1 x3 + T2 x1), one kit, no sibling, NO stack, ONE base (0d156d12cc0f), pinned over the CURRENT develop.** Both ADDENDUM 1 raises appeared during the drafter's 45-minute poll and are IN the kit: #1333 (KS-1124 F4, 15:08:42Z) and #1334 (the KS-888 validate log-only pin, 15:24:30Z; poll_1334.out: NEW Tue 29 Sep 2026 01:25:32 AEST 9b41a5fcc8fa20070aeff975a07a6f7aa13f7d99	refs/pull/1334/head). Any FURTHER `-b40-<n>` PR before launch refuses rc 15 (WIDEN) and needs a re-draft.

| PR | ticket | tier | head (API == ls-remote pull/head == branch == fetched) | commits on merge-base | files | subject declared -> lands |
|---|---|---|---|---|---|---|
| #1330 | KS-1352 | T1 | `699acfb804729f80da8aa4f4034f3cd58d99f40e` | 1 on `0d156d12cc0f` | BACKLOG.md, verifier.ts, ks1352-revoked-credential-fails-verify.test.ts, credentials.ts, presentations.ts, status.ts, revocationResolvers.ts | 66 -> 74 |
| #1332 | KS-1054 | T1 | `f5381338359da43784f01f625772abafccdf97b6` | 1 on `0d156d12cc0f` | 039_rls_fail_closed.sql, ks1054-startup-migration-failure-on-health.test.ts, ks1062-startup-migrations-tenant-summary-first-error.test.ts, ks1125-api-gateway-startup-migrations-the-tenant.test.ts, ks1128-platform-tenant-seed-failure-warns.test.ts, ks1272-platform-dedup-uuid-tenant-id.test.ts, health.ts, startupMigrationStatus.ts, startup-migrations.ts | 76 -> 84 |
| #1333 | KS-1124 | T1 | `91ceb5bc0a79fd3dceb044837955c07d553771fb` | 1 on `0d156d12cc0f` | ks543-certify-boundary-strip.test.ts, certifications.ts | 70 -> 78 |
| #1334 | KS-888 | T2 | `9b41a5fcc8fa20070aeff975a07a6f7aa13f7d99` | 1 on `0d156d12cc0f` | ks888-failed-mint-save-issues-no-key.test.ts | 69 -> 77 |

Routing `QA/Secuura-batch1330` (**NOT added by the drafter** — §4). GO string `GO: merge #1330, #1332, #1333, #1334 batch` (or the subset); the GO mail's SUBJECT: `GO (Seat B 40th): merge 1330 1332 1333 1334 on gate38` (kit rule exit 51). MERGE ORDER #1330 -> #1332 -> #1333 -> #1334 (END_TREE order-independent, measured in all 24 orders).

## 1. BLUF
- **Kit: READY to launch once the routing line is added** — launcher `--check` (launcher_check_1.out: `all guards pass:`); repin `--dry-run` (repin_dryrun_1.out: DRY RUN COMPLETE 2026-09-28T16:23:38Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add).
- **Pinned over develop `3d706c21f65e7eb8e136fc8703ce10fd91f62480`** (tree `49211e66ba2311d074a8319ea4d2ab81f9c0869a`) — two merge commits (#1329, #1331) past the PRs' merge-base `0d156d12cc0f`; move ∩ every own path EMPTY (predict (b)).
  - **END_TREE `ee7836b803f65cc049ef3d78c8f38b9866a578e3`** (19 files changed, 864 insertions(+), 14 deletions(-)), identical in ALL 24 orders (32 memoised merge-tree calls); diff(develop, END) == the union of the own paths and every END blob == its PR's head blob (MG-1).
  - Final re-read by `ls-remote` (final_lsremote_1.out): 2026-09-28T16:23:38Z | 3d706c21f65e7eb8e136fc8703ce10fd91f62480	refs/heads/develop | 699acfb804729f80da8aa4f4034f3cd58d99f40e	refs/pull/1330/head | f5381338359da43784f01f625772abafccdf97b6	refs/pull/1332/head | 91ceb5bc0a79fd3dceb044837955c07d553771fb	refs/pull/1333/head | 9b41a5fcc8fa20070aeff975a07a6f7aa13f7d99	refs/pull/1334/head — every pin still current: **True**.
- **Controls, both ways (controls_gate38.sh):**
  - normal (controls_1.out, rc 0): `SUMMARY gate38: 178 controls, OK 178, MISMATCH 0`
  - `--invert` (controls_2.out, rc 1): `SUMMARY gate38: 178 controls, OK 0, MISMATCH 178 (inverted: every control must MISMATCH-then-flip to OK; a MISMATCH here is a control that could not fail)`
- **Simulations (predict):** foreign1330 -> rc 1 REFUSED: FAIL=18 -> pins_gate38.SIM-fore; foreign1332 -> rc 1 REFUSED: FAIL=4 -> pins_gate38.SIM-forei; foreign1333 -> rc 1 REFUSED: FAIL=18 -> pins_gate38.SIM-fore; foreign1334 -> rc 1 REFUSED: FAIL=4 -> pins_gate38.SIM-forei; moved -> rc 0 PASS: FAIL=0 -> pins_gate38.SIM-moved.js (`moved` must PASS; `foreign<n>` must REFUSE).
- **Pinned predict** (predict_1.out, rc 0): `PASS: FAIL=0 -> pins_gate38.json | develop 3d706c21f65e | END_TREE ee7836b803f65cc049ef3d78c8f38b9866a578e3 | merge-bases ['0d156d12cc0f']`.
- **#1332 on a REAL PostgreSQL (MEASURED by the drafter, pgprobe_1.out — PostgreSQL 18.3 (Homebrew) on aarch64-ap, unix socket only, the REAL runStartupMigrations extracted at base and head):**
  - BARE-base boot 1: 039 recorded 0 · function ABSENT · policy 0; boot 2: 039 recorded 1 · function auth_find_oauth_app_by_client_id(text) · policy 1.
  - BARE-head boot 1: 039 recorded 1 · function ABSENT · policy 0 (recorded `{"ran": true, "applied": 81, "failed": 6, "lastRunAt": "2026-09-28T15:08:01.370Z"}`); boot 2: 039 recorded 1 · function ABSENT · policy 0 (recorded `{"ran": true, "applied": 45, "failed": 0, "lastRunAt": "2026-09-28T15:08:01.509Z"}`).
  - INIT (docker/init-seeded) boot 1: base 039 recorded 1 · function auth_find_oauth_app_by_client_id(text) · policy 1; head 039 recorded 1 · function auth_find_oauth_app_by_client_id(text) · policy 1 (the guard is inert where docker/init ran).
  - **=> FRESH-DB-039-NEVER-COMPLETES: on a bare database the head records 039 with `auth_find_oauth_app_by_client_id` (and the oauth_apps_auth_lookup policy) skipped, and NO later boot creates them (a recorded file is never re-run; the head's own NOTICE says "the next boot creates the function"); the base heals at boot 2. The head's boot-2 /health summary reads `failed: 0` over that database. A likely NO GO for #1332 — the gate re-measures and rules.** Controls: {'CT1 a wrong socket dir does not connect': True, 'CT2 no TCP listener (listen_addresses is empty)': True, 'CT2b lsof: the postmaster holds 0 inet sockets': True, 'CT3 BARE-base boot 1 FAILS 039 (the defect reproduced)': True}.
- **#1333 AND #1334 == their canonical patches (MEASURED, predict_1.out):** READY block == golden == checker patch.diff; strict `git apply --cached` at the merge-base gives the head's blobs; diff(golden-applied, head) EMPTY.
- **Standing requirement 1 (PRE-EXISTING red):** the KS-764 CALL_SITES regex matches security index.ts nowhere at the merge-base, develop, any head or END_TREE (READ, with a control) — the gate names `packages/shared` 1 failed / 945 PRE-EXISTING unless a PR changes its count.
- **Standing requirement 2 (cross-package):** predict_1.out CROSS-PACKAGE CENSUS lists every test file referencing each changed path; the prompt names the suites to RUN (incl. the KS-764 guard at #1332's head, auth ks949 / ks720, api-gateway ks667, scripts ks949_main_seed_idempotence.test.sh, originate ks1293, api-gateway ks1071).
- **Linear:** every PR links `contributes`, none `closes` (linear_reads_1.out). **Key scan:** each title / body / commit carries only its own key (keyscan_1.out).
- **Re-key / namespace (rekey_1.out):** RESULT CLEAN: 0 hit(s)
- **Sizes / sha256:** `2026-09-29_secuura-batch1330.prompt.txt` 63540 bytes sha256 `a030d9a0eb81089ac2aefc660cbe8b4901be5d5c9788ca1d1564290e9253c41c`; `launch_qa_secuura_batch1330.sh` 23507 bytes sha256 `8bdd4aa0ac299dacbc99217f6802fbe1840c8e7c67608ed720de2b031dc5830b`; `mail_gate38_ready.md` 95435 bytes sha256 `0e848b185f7d051a231e8dc796b2cee223fc7b4d20c24f50124fd102a48b5ce1`.

## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated)
1. **#1332, MEASURED — the fix trades a transient fail-open window for a permanent missing OAuth lookup on bare databases** (§1). The seat never ran 039; its NOTICE claim is false under the runner's own tracker.
2. **#1332 — the ":5-21 header" claim.** Both READYs say the decision is recorded in "the `:5-21` header"; 039's diff touches only :221-:257 and :271-:281 (its :1-:24 header is byte-unchanged). The record is in startup-migrations.ts (:23-:42). Which file the brief meant is for Wednesday.
3. **#1332 — `error?` is dead and CORE throws are uncounted (READ):** recordStartupMigrations is called once with applied/failed only; the CORE-stage catches (:1093, :1194) do not add to totalFailed — "a stage that THREW never reports clean" holds only for the file stage.
4. **#1332 — Kam's option a says the deploy "reads as failed"** via the existing /health checks; no deploy script reads `startupMigrations.failed` at head (deploy-all.sh:281 ruled out of scope) — the flag is visible but gates nothing yet.
5. **#1330 — the pass-through "ruling" letter.** The READY says "Your Q1 ruling **(b) pass-through**"; the card secuura-ks1352-unknown-credential-id-verify-policy is still OPEN (ruled_ts null) and pass-through is its option **a** (the default). The commission says "default a". The code implements pass-through (abstain on `found: false`) — consistent with the default, but it is Wednesday's default, not a Kam ruling.
6. **#1330 — fail-CLOSED on a resolver error:** a throwing `getById` / status lookup pushes an error and FAILS the credential — wider than pass-through in that one case (READ); the gate rules it.
7. **#1330 — presentations/verify has NO cell** (the seat's six cells drive credentials/verify only); the prompt makes the gate drive it. **A second, unrevocation-aware `POST /api/credentials/verify` lives in services/prism** (not gateway-routed, READ).
8. **#1330 carries BACKLOG.md** (+23 lines, a doc outside KS-1352's product scope, with KS-764 / KS-888 hyphenated as content).
9. **#1333 / #1334 — no push log** in 2026-09-28_seatB-40th/ at drafting (only push40-ks1352 / push40-ks1054 rawlogs), so their fleet STOP counts are UNREAD; no READY mail id reached the drafter for either (their capture is the night READY file + PR body + commit).
10. **The commission said gate37 ran Postgres "over a unix socket with no TCP"** — gate37's DRAFTER used PGlite (its initdb-18 start failed on the socket-path length); it was gate37's GATE that ran PG 18.3 on a unix socket. This kit copies the gate's method (and the drafter used it too).
11. **The KS-764 guard location:** the commission cites `:77/:97` (CALL_SITES / REVOKE_WRITES — READ correct); the seat's BACKLOG entry cites `:292` (a line inside the failing cell at :263). Same cell.
12. **#1334 — a pin that is both GREEN and RED at the tip:** the PR body says the cells are "GREEN at the untouched tip by design"; the READY's checker says "RED-FIRST … 1 failed / 19 run" at the untouched tip. Same bytes (PR == canonical patch, MEASURED) — one claim is wrong; the seat's STATUS mail repeats GREEN BY DESIGN (the arms are the proof; arm D must red 5). The prompt makes the gate rule it. Commission tiered #1334 T2 (tests-only) — kept.
14. **The seat's STATUS mail (relayed by Wednesday) says "Develop moved to `db8d85dcd`"** — stale: origin develop is `3d706c21f65e` (#1331 on top), READ by ls-remote. It also files **KS-1370** (High: a boot-time key map lets a revoked key keep authenticating and the usage upsert write is_active back) — not fixed by any kit PR; the prompt asks whether #1334's pin interacts with it, and names the KS-888 ruling conflict (20:22:15 log-only vs 20:22:48 refuse).
13. **GitHub mergeable_state `unstable`** on the PRs (gh_read_1.out) — mergeable True; a non-required check is failing or pending. Not measured further.

## 3. Pins and what the gate owes
- Prompt `2026-09-29_secuura-batch1330.prompt.txt` — #1330 through the REAL vc-issuer app (both revoke routes, unknown ids exactly as at develop, no-credentialStatus, presentations/verify, resolver throw, colliding indexes); #1332 the two-sided fresh-database drill on a REAL PostgreSQL (bare + docker/init, boot twice), /health and /health/ready served, TS2322 delta; #1333 both certification routes, the readers of the new literal, ks1293; #1334 the pin at the untouched tip and its arms on the product; standing requirements 1 and 2 as kit rules 53 / 54; `## MERGE ADDENDUM` last, ONE LINE PER PR starting `- #<n> · head <sha12> · subject:` (kit rule 52).
- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-29-batch1330-g38/`; mail FROM coagent@ TO wednesday-agent@.

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines) — backup first:
```
QA/Secuura-batch1330|coagent@agentmail.to|yes
```
Until it is present the launch action's step 0 refuses rc 1 (repin_dryrun_1.out reports it).

## 5. Controls: `controls_gate38.sh <scratchpad> [--invert]`
- Same arms as gate37's kit, re-keyed: wrong heads, a moved develop (predev = the #1329 merge), per-PR path renames (all four), capture / prompt doctoring, every kit rule 35 / 40-44 / 46-49 / 51-55 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO plants, predict `--simulate foreign1332` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate37's and gate36's namespaces.
- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, pgprobe beyond its built-in controls (CT1-CT3).

## 6. Could not measure (the drafter's NOT-MEASURED list)
- No suite, tsc, eslint, prettier or red-proof run by the drafter; every seat figure is a claim in its READY / PR body. #1330, #1333 and #1334 at runtime: NOTHING driven. #1332: the drill ran the extracted runStartupMigrations on the MAIN database only (no platform DB, no tenant DB, no APP_DB_PASSWORD role provisioning), not through the gateway process, and /health was NOT served (the recorded summary was read from the module). The tenant_isolation fail-closed shape after boot 1 was not read.

## 7. Files
- Kit: kit.json · COMMISSION.md (make_commission_gate38.py) · README.md (make_readme_gate38.py) · rekey_check_gate38.py -> rekey_1.out
- Pins: predict_gate38.py -> predict_1.out, predict_sim_*.out, pins_gate38.json (+ .SIM-*.json) · keyscan_gate38.py -> keyscan_1.out · final_lsremote_1.out · poll_1334.out
- Measurements: pgprobe_gate38.py + pgprobe_gate38.runner.ts -> pgprobe_1.out, pgprobe_gate38.json
- Reads: gh_read_gate38.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate38.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate38.py -> capture_1.out, mail_gate38_ready.md, stopcounts_gate38.json · _api_peek_gate38.py -> _api_peek_1.out
- Prompt/launcher: prompt_gate38.TEMPLATE.txt, launcher_gate38.TEMPLATE.sh.txt, fill_gate38.py -> 2026-09-29_secuura-batch1330.prompt.txt + launch_qa_secuura_batch1330.sh (fill_1.out), launcher_check_1.out · repin_and_launch_gate38.sh -> repin_dryrun_1.out · controls_gate38.sh -> controls_1.out / controls_2.out

## 8. The ONE launch command (after the routing line, §4)
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate38/repin_and_launch_gate38.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-29_gate38/launch_qa_secuura_batch1330.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/24014037-1954-4f3d-a19e-71dd4e50a1cf/scratchpad/g38
```
- Dry run: append `--dry-run`. Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`); if `g38_sp/clone.git` is absent there, predict rebuilds it on a re-pin (pgprobe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, an overlap or an END-tree disagreement refuses rc 10; a further `-b40-<n>` PR refuses rc 15; a moved head refuses rc 11.
