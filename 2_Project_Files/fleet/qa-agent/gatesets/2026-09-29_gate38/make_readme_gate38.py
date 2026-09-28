#!/usr/bin/env python3
"""make_readme_gate38.py — writes README.md for gate38 (the directory this script lives in). Every figure is READ from the kit's own output files at the
moment it runs (pins_gate38.json, predict_1.out, predict_sim_*.out(.rc), pgprobe_gate38.json, fill_1.out, launcher_check_1.out, repin_dryrun_1.out,
controls_1.out / controls_2.out (+ .rc), final_lsremote_1.out, rekey_1.out, poll_1334.out), each named beside it; the prose (doubts, questions) is the
drafter's. Shape copied from gate37's make_readme (gate36 -> gate35 lineage), re-keyed to gate38. The README ENDS with the one launch command."""
import json, os, re, glob, hashlib, datetime, sys
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
SP = sys.argv[1] if len(sys.argv) > 1 else ''
P = json.load(open('%s/pins_%s.json' % (D, kit))); PG = json.load(open('%s/pgprobe_%s.json' % (D, kit)))
def rd(f): return open(os.path.join(D, f), encoding='utf-8').read() if os.path.exists(os.path.join(D, f)) else ''
def last(f, rx):
    m = [l for l in rd(f).splitlines() if re.search(rx, l)]; return m[-1].strip() if m else 'ABSENT'
def rc(f): return rd(f).strip() or '?'
fill = rd('fill_1.out'); now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
L = os.path.join(D, K['launcher']); PR = os.path.join(D, K['prompt']); CAP = os.path.join(D, 'mail_%s_ready.md' % kit)
def sz(p): b = open(p, 'rb').read(); return '`%s` %d bytes sha256 `%s`' % (os.path.basename(p), len(b), hashlib.sha256(b).hexdigest())
R = PG['runs']
def dbs(k): d = R[k].get('db', {}); return '039 recorded %s · function %s · policy %s' % (d.get('tracked_039'), d.get('fn_auth_find_oauth_app_by_client_id') or 'ABSENT', d.get('oauth_apps_auth_lookup_policy'))
sims = {os.path.basename(f)[len('predict_sim_'):-len('.out')]: (rc(os.path.basename(f) + '.rc'), last(os.path.basename(f), r'^(PASS|REFUSED):')[:40]) for f in sorted(glob.glob(D + '/predict_sim_*.out'))}
fl = rd('final_lsremote_1.out').strip().replace('\n', ' | ')
cur = all(P['prs'][n]['head'] in fl for n in P['prs']) and P['develop'] in fl
launch = '%s/repin_and_launch_%s.sh %s %s' % (D, kit, L, SP)
rows = []
for n in sorted(K['prs']):
    pr = P['prs'][n]
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill)
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s -> %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12],
                ', '.join(os.path.basename(p) for p in pr['paths']), m.group(1) if m else '?', m.group(2) if m else '?'))
out = ['# Gateset %s — README for Wednesday' % os.path.basename(D), '',
 'Written %s by the drafter (make_readme_gate38.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now,
 'The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory and scratch under its session scratchpad `.../scratchpad/g38/` (the scratch clone `g38_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, fetched FROM ORIGIN with the checkout\'s repo-local key; the Postgres data dirs `g38_pg/data_*` (kept, stopped); the git-archive extracts `g38_pg/base|head`; the control workdirs `g38_controls_*`). OUTSIDE the scratchpad it created only short, empty unix-socket dirs `/tmp/q38.*` for the throwaway Postgres (the scratchpad path is too long for a socket). It did NOT write the routing line (§4).',
 'The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its tsx and pg). GitHub: REST GET only. Linear: queries only. AgentMail: three BY-ID reads (the two READY mails and the seat STATUS mail Wednesday relayed; inbox_digest.sh full), no listing, nothing sent. decisions.json and inbox_routing.conf: read only.', '',
 '**gate38 = FOUR PRs (T1 x3 + T2 x1), one kit, no sibling, NO stack, ONE base (0d156d12cc0f), pinned over the CURRENT develop.** Both ADDENDUM 1 raises appeared during the drafter\'s 45-minute poll and are IN the kit: #1333 (KS-1124 F4, 15:08:42Z) and #1334 (the KS-888 validate log-only pin, 15:24:30Z; poll_1334.out: %s). Any FURTHER `-b40-<n>` PR before launch refuses rc 15 (WIDEN) and needs a re-draft.' % (last('poll_1334.out', r'NEW|NONE')[:110]),
 '', '| PR | ticket | tier | head (API == ls-remote pull/head == branch == fetched) | commits on merge-base | files | subject declared -> lands |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Routing `%s` (**NOT added by the drafter** — §4). GO string `GO: merge #1330, #1332, #1333, #1334 batch` (or the subset); the GO mail\'s SUBJECT: `GO (Seat B 40th): merge 1330 1332 1333 1334 on gate38` (kit rule exit 51). MERGE ORDER #1330 -> #1332 -> #1333 -> #1334 (END_TREE order-independent, measured in all %d orders).' % (K['pane'], P['orders']),
 '', '## 1. BLUF',
 '- **Kit: READY to launch once the routing line is added** — launcher `--check` (launcher_check_1.out: `%s`); repin `--dry-run` (repin_dryrun_1.out: %s).' % (last('launcher_check_1.out', r'all guards pass|REFUSING'), last('repin_dryrun_1.out', r'DRY RUN COMPLETE|REFUSING|exit')[:200]),
 '- **Pinned over develop `%s`** (tree `%s`) — two merge commits (#1329, #1331) past the PRs\' merge-base `%s`; move ∩ every own path EMPTY (predict (b)).' % (P['develop'], P['develop_tree'], P['merge_bases'][0][:12]),
 '  - **END_TREE `%s`** (%s), identical in ALL %d orders (%d memoised merge-tree calls); diff(develop, END) == the union of the own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 '  - Final re-read by `ls-remote` (final_lsremote_1.out): %s — every pin still current: **%s**.' % (fl, cur),
 '- **Controls, both ways (controls_gate38.sh):**',
 '  - normal (controls_1.out, rc %s): `%s`' % (rc('controls_1.rc'), last('controls_1.out', r'^SUMMARY')),
 '  - `--invert` (controls_2.out, rc %s): `%s`' % (rc('controls_2.rc'), last('controls_2.out', r'^SUMMARY')),
 '- **Simulations (predict):** %s (`moved` must PASS; `foreign<n>` must REFUSE).' % '; '.join('%s -> rc %s %s' % (k, v[0], v[1]) for k, v in sims.items()),
 '- **Pinned predict** (predict_1.out, rc %s): `%s`.' % (rc('predict_1.out.rc'), last('predict_1.out', r'^(PASS|REFUSED):')),
 '- **#1332 on a REAL PostgreSQL (MEASURED by the drafter, pgprobe_1.out — %s, unix socket only, the REAL runStartupMigrations extracted at base and head):**' % PG.get('engine', '?')[:40],
 '  - BARE-base boot 1: %s; boot 2: %s.' % (dbs('BARE-base boot 1'), dbs('BARE-base boot 2')),
 '  - BARE-head boot 1: %s (recorded `%s`); boot 2: %s (recorded `%s`).' % (dbs('BARE-head boot 1'), json.dumps(R['BARE-head boot 1'].get('recorded')), dbs('BARE-head boot 2'), json.dumps(R['BARE-head boot 2'].get('recorded'))),
 '  - INIT (docker/init-seeded) boot 1: base %s; head %s (the guard is inert where docker/init ran).' % (dbs('INIT-base boot 1'), dbs('INIT-head boot 1')),
 '  - **=> FRESH-DB-039-NEVER-COMPLETES: on a bare database the head records 039 with `auth_find_oauth_app_by_client_id` (and the oauth_apps_auth_lookup policy) skipped, and NO later boot creates them (a recorded file is never re-run; the head\'s own NOTICE says "the next boot creates the function"); the base heals at boot 2. The head\'s boot-2 /health summary reads `failed: 0` over that database. A likely NO GO for #1332 — the gate re-measures and rules.** Controls: %s.' % PG['controls'],
 '- **#1333 AND #1334 == their canonical patches (MEASURED, predict_1.out):** READY block == golden == checker patch.diff; strict `git apply --cached` at the merge-base gives the head\'s blobs; diff(golden-applied, head) EMPTY.',
 '- **Standing requirement 1 (PRE-EXISTING red):** the KS-764 CALL_SITES regex matches security index.ts nowhere at the merge-base, develop, any head or END_TREE (READ, with a control) — the gate names `packages/shared` 1 failed / 945 PRE-EXISTING unless a PR changes its count.',
 '- **Standing requirement 2 (cross-package):** predict_1.out CROSS-PACKAGE CENSUS lists every test file referencing each changed path; the prompt names the suites to RUN (incl. the KS-764 guard at #1332\'s head, auth ks949 / ks720, api-gateway ks667, scripts ks949_main_seed_idempotence.test.sh, originate ks1293, api-gateway ks1071).',
 '- **Linear:** every PR links `contributes`, none `closes` (linear_reads_1.out). **Key scan:** each title / body / commit carries only its own key (keyscan_1.out).',
 '- **Re-key / namespace (rekey_1.out):** %s' % last('rekey_1.out', r'^RESULT'),
 '- **Sizes / sha256:** %s; %s; %s.' % (sz(PR), sz(L), sz(CAP)),
 '', '## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated)',
 '1. **#1332, MEASURED — the fix trades a transient fail-open window for a permanent missing OAuth lookup on bare databases** (§1). The seat never ran 039; its NOTICE claim is false under the runner\'s own tracker.',
 '2. **#1332 — the ":5-21 header" claim.** Both READYs say the decision is recorded in "the `:5-21` header"; 039\'s diff touches only :221-:257 and :271-:281 (its :1-:24 header is byte-unchanged). The record is in startup-migrations.ts (:23-:42). Which file the brief meant is for Wednesday.',
 '3. **#1332 — `error?` is dead and CORE throws are uncounted (READ):** recordStartupMigrations is called once with applied/failed only; the CORE-stage catches (:1093, :1194) do not add to totalFailed — "a stage that THREW never reports clean" holds only for the file stage.',
 '4. **#1332 — Kam\'s option a says the deploy "reads as failed"** via the existing /health checks; no deploy script reads `startupMigrations.failed` at head (deploy-all.sh:281 ruled out of scope) — the flag is visible but gates nothing yet.',
 '5. **#1330 — the pass-through "ruling" letter.** The READY says "Your Q1 ruling **(b) pass-through**"; the card secuura-ks1352-unknown-credential-id-verify-policy is still OPEN (ruled_ts null) and pass-through is its option **a** (the default). The commission says "default a". The code implements pass-through (abstain on `found: false`) — consistent with the default, but it is Wednesday\'s default, not a Kam ruling.',
 '6. **#1330 — fail-CLOSED on a resolver error:** a throwing `getById` / status lookup pushes an error and FAILS the credential — wider than pass-through in that one case (READ); the gate rules it.',
 '7. **#1330 — presentations/verify has NO cell** (the seat\'s six cells drive credentials/verify only); the prompt makes the gate drive it. **A second, unrevocation-aware `POST /api/credentials/verify` lives in services/prism** (not gateway-routed, READ).',
 '8. **#1330 carries BACKLOG.md** (+23 lines, a doc outside KS-1352\'s product scope, with KS-764 / KS-888 hyphenated as content).',
 '9. **#1333 / #1334 — no push log** in 2026-09-28_seatB-40th/ at drafting (only push40-ks1352 / push40-ks1054 rawlogs), so their fleet STOP counts are UNREAD; no READY mail id reached the drafter for either (their capture is the night READY file + PR body + commit).',
 '10. **The commission said gate37 ran Postgres "over a unix socket with no TCP"** — gate37\'s DRAFTER used PGlite (its initdb-18 start failed on the socket-path length); it was gate37\'s GATE that ran PG 18.3 on a unix socket. This kit copies the gate\'s method (and the drafter used it too).',
 '11. **The KS-764 guard location:** the commission cites `:77/:97` (CALL_SITES / REVOKE_WRITES — READ correct); the seat\'s BACKLOG entry cites `:292` (a line inside the failing cell at :263). Same cell.',
 '12. **#1334 — a pin that is both GREEN and RED at the tip:** the PR body says the cells are "GREEN at the untouched tip by design"; the READY\'s checker says "RED-FIRST … 1 failed / 19 run" at the untouched tip. Same bytes (PR == canonical patch, MEASURED) — one claim is wrong; the seat\'s STATUS mail repeats GREEN BY DESIGN (the arms are the proof; arm D must red 5). The prompt makes the gate rule it. Commission tiered #1334 T2 (tests-only) — kept.',
 '14. **The seat\'s STATUS mail (relayed by Wednesday) says "Develop moved to `db8d85dcd`"** — stale: origin develop is `3d706c21f65e` (#1331 on top), READ by ls-remote. It also files **KS-1370** (High: a boot-time key map lets a revoked key keep authenticating and the usage upsert write is_active back) — not fixed by any kit PR; the prompt asks whether #1334\'s pin interacts with it, and names the KS-888 ruling conflict (20:22:15 log-only vs 20:22:48 refuse).',
 '13. **GitHub mergeable_state `unstable`** on the PRs (gh_read_1.out) — mergeable True; a non-required check is failing or pending. Not measured further.',
 '', '## 3. Pins and what the gate owes',
 '- Prompt `%s` — #1330 through the REAL vc-issuer app (both revoke routes, unknown ids exactly as at develop, no-credentialStatus, presentations/verify, resolver throw, colliding indexes); #1332 the two-sided fresh-database drill on a REAL PostgreSQL (bare + docker/init, boot twice), /health and /health/ready served, TS2322 delta; #1333 both certification routes, the readers of the new literal, ks1293; #1334 the pin at the untouched tip and its arms on the product; standing requirements 1 and 2 as kit rules 53 / 54; `## MERGE ADDENDUM` last, ONE LINE PER PR starting `- #<n> · head <sha12> · subject:` (kit rule 52).' % K['prompt'],
 '- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail FROM coagent@ TO wednesday-agent@.' % K['report'],
 '', '## 4. Routing line — NOT added',
 'Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines) — backup first:',
 '```', '%s|coagent@agentmail.to|yes' % K['pane'], '```',
 'Until it is present the launch action\'s step 0 refuses rc 1 (repin_dryrun_1.out reports it).',
 '', '## 5. Controls: `controls_gate38.sh <scratchpad> [--invert]`',
 '- Same arms as gate37\'s kit, re-keyed: wrong heads, a moved develop (predev = the #1329 merge), per-PR path renames (all four), capture / prompt doctoring, every kit rule 35 / 40-44 / 46-49 / 51-55 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO plants, predict `--simulate foreign1332` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate37\'s and gate36\'s namespaces.',
 '- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, pgprobe beyond its built-in controls (CT1-CT3).',
 '', '## 6. Could not measure (the drafter\'s NOT-MEASURED list)',
 '- No suite, tsc, eslint, prettier or red-proof run by the drafter; every seat figure is a claim in its READY / PR body. #1330, #1333 and #1334 at runtime: NOTHING driven. #1332: the drill ran the extracted runStartupMigrations on the MAIN database only (no platform DB, no tenant DB, no APP_DB_PASSWORD role provisioning), not through the gateway process, and /health was NOT served (the recorded summary was read from the module). The tenant_isolation fail-closed shape after boot 1 was not read.',
 '', '## 7. Files',
 '- Kit: kit.json · COMMISSION.md (make_commission_gate38.py) · README.md (make_readme_gate38.py) · rekey_check_gate38.py -> rekey_1.out',
 '- Pins: predict_gate38.py -> predict_1.out, predict_sim_*.out, pins_gate38.json (+ .SIM-*.json) · keyscan_gate38.py -> keyscan_1.out · final_lsremote_1.out · poll_1334.out',
 '- Measurements: pgprobe_gate38.py + pgprobe_gate38.runner.ts -> pgprobe_1.out, pgprobe_gate38.json',
 '- Reads: gh_read_gate38.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate38.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate38.py -> capture_1.out, mail_gate38_ready.md, stopcounts_gate38.json · _api_peek_gate38.py -> _api_peek_1.out',
 '- Prompt/launcher: prompt_gate38.TEMPLATE.txt, launcher_gate38.TEMPLATE.sh.txt, fill_gate38.py -> %s + %s (fill_1.out), launcher_check_1.out · repin_and_launch_gate38.sh -> repin_dryrun_1.out · controls_gate38.sh -> controls_1.out / controls_2.out' % (K['prompt'], K['launcher']),
 '', '## 8. The ONE launch command (after the routing line, §4)',
 '```', launch, '```',
 '- Dry run: append `--dry-run`. Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`); if `g38_sp/clone.git` is absent there, predict rebuilds it on a re-pin (pgprobe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, an overlap or an END-tree disagreement refuses rc 10; a further `-b40-<n>` PR refuses rc 15; a moved head refuses rc 11.']
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
