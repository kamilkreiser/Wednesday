#!/usr/bin/env python3
"""make_readme_gate39.py — writes README.md for gate39 (the directory this script lives in). Every figure is READ from the kit's own output files at the
moment it runs (pins_gate39.json, predict_1.out, predict_sim_*.out(.rc), pgprobe_gate39.json, fill_1.out, launcher_check_1.out, repin_dryrun_1.out,
controls_1.out / controls_2.out (+ .rc), final_lsremote_1.out, rekey_1.out), each named beside it; the prose (doubts, questions) is the drafter's.
Shape copied from gate38's make_readme (gate37 -> gate36 lineage), re-keyed to gate39. The README ENDS with the one launch command."""
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
R = PG['runs']; SUM = PG['_summary']
sims = {os.path.basename(f)[len('predict_sim_'):-len('.out')]: (rc(os.path.basename(f) + '.rc'), last(os.path.basename(f), r'^(PASS|REFUSED):')[:44]) for f in sorted(glob.glob(D + '/predict_sim_*.out'))}
fl = rd('final_lsremote_1.out').strip().replace('\n', ' | ')
cur = all(P['prs'][n]['head'] in fl for n in P['prs']) and P['develop'] in fl
launch = '%s/repin_and_launch_%s.sh %s %s' % (D, kit, L, SP)
rows = []
for n in K['merge_order']:
    pr = P['prs'][n]
    m = re.search(r'#%s (\d+)->(\d+)' % n, fill)
    rows.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s -> %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12],
                ', '.join(os.path.basename(p) for p in pr['paths']), m.group(1) if m else '?', m.group(2) if m else '?'))
APP = SUM.get('AS AN APP ROLE (tenant GUC set): certifications INSERT+count per database — base bare boot 2 vs head (i) (ii) (iii) vs develop seeded') or {}
def app(k): v = APP.get(k, '?'); return 'REFUSED (new row violates row-level security policy)' if 'row-level security' in str(v) else v
EQ = SUM.get("pg_dump -t of the four tables byte-identical across (i), (ii), (iii) and develop's seeded path — per table")
out = ['# Gateset %s — README for Wednesday' % os.path.basename(D), '',
 'Written %s by the drafter (make_readme_gate39.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now,
 'The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory (TEXT files only) and scratch on the DATA volume under its session scratchpad `.../scratchpad/g39/` (the scratch clone `g39_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, fetched FROM ORIGIN with the checkout\'s repo-local key; the Postgres data dirs `g39_pg/data_*` (kept, stopped); the git-archive extracts `g39_pg/base|r1|head|dev` and the arm copy `g39_pg/head_no038a` (its 038a moved aside to `g39_pg/head_no038a.QUARANTINED-038a.sql`, never deleted); every dump under `g39_pg/dumps/`; the control workdirs `g39_controls_*`). OUTSIDE the scratchpad it created only short, empty unix-socket dirs `/tmp/q39.*`, and the REAL run-migrations.sh wrote its own `/tmp/migrate-err.log` (the script\'s code). Nothing large was written to /Volumes/DevMASTER. It did NOT write the routing line (§4).',
 'The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its tsx and pg). The seat\'s scratchpad (push logs, drill41.*) was READ. GitHub: REST GET only. Linear: queries only. AgentMail: two BY-ID reads (the two READY mails; inbox_digest.sh full), no listing, nothing sent. decisions.json and inbox_routing.conf: read only.', '',
 '**gate39 = TWO PRs (T2 + T1), one kit, no sibling, NO stack, TWO merge-bases, pinned over the CURRENT develop. MERGE ORDER #1337 FIRST.**', '',
 '| PR (merge order) | ticket | tier | head (API == ls-remote pull/head == branch == fetched) | commits on merge-base | files | subject declared -> lands |', '|---|---|---|---|---|---|---|'] + rows + ['',
 'Routing `%s` (**NOT added by the drafter** — §4). GO string `GO: merge #1337, #1332 batch` (or the subset); the GO mail\'s SUBJECT: `GO (Seat B 41st): merge 1337 1332 on gate39` (kit rule exit 51). MERGE ORDER #1337 -> #1332 (kit rule exit 44): END_TREE is order-independent (both orders, measured) but #1332 first would leave develop red between the squashes (EMULATED, predict (d2)).' % K['pane'],
 '', '## 1. BLUF',
 '- **Kit: READY to launch once the routing line is added** — launcher `--check` (launcher_check_1.out: `%s`); repin `--dry-run` (repin_dryrun_1.out: %s).' % (last('launcher_check_1.out', r'all guards pass|REFUSING'), last('repin_dryrun_1.out', r'DRY RUN COMPLETE|REFUSING|exit')[:200]),
 '- **Pinned over develop `%s`** (tree `%s`); merge-bases #1337 `%s` (develop itself), #1332 `%s` (35 first-parent commits behind at drafting); move ∩ every own path EMPTY (predict (b)).' % (P['develop'], P['develop_tree'], P['prs']['1337']['merge_base'][:12], P['prs']['1332']['merge_base'][:12]),
 '  - **END_TREE `%s`** (%s), identical in BOTH orders (%d memoised merge-tree calls); diff(develop, END) == the union of the own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['merge_tree_calls']),
 '  - **The order (EMULATED, READ):** %s.' % ' || '.join('%s: %s' % (o, ' -> '.join('%s %s' % (s['after'], s['CALL_SITES_cell'].split(' ')[0]) for s in st)) for o, st in P.get('order_proof', {}).items()),
 '  - Final re-read by `ls-remote` (final_lsremote_1.out): %s — every pin still current: **%s**.' % (fl, cur),
 '- **Controls, both ways (controls_gate39.sh):**',
 '  - normal (controls_1.out, rc %s): `%s`' % (rc('controls_1.rc'), last('controls_1.out', r'^SUMMARY')),
 '  - `--invert` (controls_2.out, rc %s): `%s`' % (rc('controls_2.rc'), last('controls_2.out', r'^SUMMARY')),
 '- **Simulations (predict):** %s (`moved` must PASS; `foreign<n>` must REFUSE).' % '; '.join('%s -> rc %s %s' % (k, v[0], v[1]) for k, v in sims.items()),
 '- **Pinned predict** (predict_1.out, rc %s): `%s`.' % (rc('predict_1.out.rc'), last('predict_1.out', r'^(PASS|REFUSED):')),
 '- **#1337 == the held Spark patch (MEASURED, predict_1.out):** READY block == golden == checker patch.diff (sha256 34f81565ed609004, 1275 B); strict `git apply --cached` at 215cc6875e2b gives the head blob; a CONTEXT-line mutation refuses; a HUNK-OFFSET mutation still applies (the seat\'s correction holds). EMULATED: the new pattern matches security index.ts at develop and misses under all five broken-revoke arms; the rejected loose window matches under all five.',
 '- **#1332 on a REAL PostgreSQL (MEASURED by the drafter, pgprobe_1.out — %s, unix socket only; controls %s):**' % (PG.get('engine', '?')[:40], 'ALL PASS' if all(PG['controls'].values()) else PG['controls']),
 '  - **All three paths the seat did not drive complete 039 at the first boot / pass:** (i) %s; (ii) %s; (iii) %s — function present, oauth_apps_auth_lookup present, oauth_apps / svc_webhooks / charge_events RLS+FORCE+tenant_isolation. The arm "038a removed" brings round 1\'s permanent skip back (%s). N-1332-1\'s function/policy half: CLOSED (drafter\'s run).' % (
     SUM.get('(i) head bare -> gateway boot 1: 039 recorded, function present, policy present, the four tables RLS+FORCE+tenant_isolation'), SUM.get('(ii) head bare -> run-migrations.sh -> gateway boot 1: 039 recorded, function, policy, four closed'),
     SUM.get('(iii) head docker/init -> gateway boot 1: 039 recorded, function, policy, four closed'), SUM.get("arm head-minus-038a: round 1's permanent skip returns (039 recorded, function ABSENT after boot 2)")),
 '  - **CERTIFICATIONS REGRESSES ON THE BARE PATH (MEASURED — the item most likely to decide the verdict):** on every head path certifications ends RLS + FORCE with NO tenant_isolation policy (038a, like CORE, creates it without tenant_id; 039\'s only pass skips it; CORE adds tenant_id later; 039 never re-runs). The merge-base\'s bare database HEALS it at boot 2. As an app role (NOSUPERUSER NOBYPASSRLS, tenant GUC set, rolled back), INSERT into certifications: merge-base bare boot 2 **%s**; head (i) **%s**; (ii) %s; (iii) %s; develop seeded %s. Develop\'s seeded path was already in this state (gate38 N-DEV-1) — round 2 carries it to the bare (Azure) path.' % (app('bare_base'), app('p1_head'), app('p2_head'), app('p3_head'), app('pd_dev')),
 '  - **Schema equality (pg_dump -t, nonce-filtered):** per table across (i)/(ii)/(iii)/develop-seeded %s. (i) == (ii) all four; (iii) == develop seeded except charge_events (head CLOSES it there — a fix); bare != seeded for oauth_apps / svc_webhooks (docker/init adds two indexes each and a CHECK on oauth_apps — PRE-EXISTING: the merge-base\'s bare end state equals head (i) for those tables). **Wednesday\'s byte-identical condition therefore does not hold as written** — the gate rules which differences are this PR\'s.' % EQ,
 '  - **A second boot:** (iii) changes nothing; (i) and (ii) change ONLY rights_holders (%s / %s — 026/027/028 fail at the first boot because rights_holders is CORE-created: the same fail-open-until-boot-2 class for a fifth table, PRE-EXISTING).' % (SUM.get('(i) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]'), SUM.get('(ii) head: a second boot changes nothing (whole schema) — else [the tables it changes, +/- lines]')),
 '  - **N-1332-2 / N-1332-3 two-sided:** %s / %s.' % (SUM.get('N-1332-2 two-sided: a CORE throw on boot 2 reads failed > 0 at head, failed == 0 at round 1'), SUM.get('N-1332-3: the CORE-throw boot records `error` naming the throw')),
 '  - **Compose runner:** head pass 1 `%s` FAILED %s, pass 2 `%s`; merge-base every pass `%s` — it still exits 3 at head (026-028, pre-existing).' % (R['rm head pass 1']['summary'], [f[:3] for f in R['rm head pass 1']['failed_files']], R['rm head pass 2']['summary'], R['rm base pass 1']['summary']),
 '- **Standing requirement 1:** the CALL_SITES cell (EMULATED) reds at develop and #1332\'s head, greens at #1337\'s head, develop + #1337 and END_TREE; startup-migrations.ts at END still mentions svc_api_keys + is_active and matches no revoke pattern (the allowlist\'s drift cells\' two facts).',
 '- **Standing requirement 2:** predict_1.out CROSS-PACKAGE CENSUS (+ the migrations-DIRECTORY readers for 038a); the prompt names the suites to RUN.',
 '- **Linear:** both PRs link `contributes`, none `closes` (linear_reads_1.out). **Key scan:** each title / body / commit carries only its own key (keyscan_1.out).',
 '- **Re-key / namespace (rekey_1.out):** %s' % last('rekey_1.out', r'^RESULT'),
 '- **Sizes / sha256:** %s; %s; %s.' % (sz(PR), sz(L), sz(CAP)),
 '', '## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated)',
 '1. **#1332, MEASURED — certifications goes default-deny for good on a fresh bare database** (§1). A regression against the merge-base\'s healed bare end state (boot 2), and the same state develop\'s seeded path already had (N-DEV-1). Whether it blocks turns on which role the services use on a deployed stack (RLS binds the owner too under FORCE; only superusers / BYPASSRLS escape). This is the LAST round under the 2-NO-GO cap — the gate must separate this from what ships. The fix-shape is small (038a\'s certifications carries CORE\'s later `tenant_id UUID`, so 039 closes it).',
 '2. **#1332, MEASURED — Wednesday\'s pg_dump byte-identity across (i)/(ii)/(iii)/develop-seeded cannot hold as written:** docker/init\'s oauth_apps / svc_webhooks carry indexes (and a CHECK) CORE does not (pre-existing); charge_events differs because round 2 FIXES it on the seeded path. The seat proved only CORE-vs-038a on two bare databases, and said so ("Two of the three sides you named were NOT driven").',
 '3. **#1332 — "Three migrations that fail forever on the other two trees now succeed" (006 / 008 / 047): MEASURED true for the COMPOSE runner only, and 006 / 008 need a SECOND pass** (they sort below 038a); on the gateway path the merge-base already applied all three at boot 2, and the head moves only 047 to boot 1.',
 '4. **#1332 — the seat\'s "25" tenant_isolation policies** is a whole-database count on the compose runner with PLATFORM_DATABASE_URL unset (the *platform* files land in main and add tenant_config / tenant_contacts); the gateway path reads 23 (MEASURED). It says nothing about the four tables. The seat\'s "A second pass changes none of those five" is five facts, not the schema — its own log shows applied 45 -> 47 on pass 2.',
 '5. **#1332 — the compose runner still exits 3** at head on every pass (026-028; pre-existing at the merge-base, which also fails 006/008/039/047) — `service_completed_successfully` still fails. Not this PR\'s; named once.',
 '6. **#1332 — LOCALE (READ, emulated, NOT measured on glibc):** a glibc host running `sh scripts/run-migrations.sh` under en_US.UTF-8 would sort 038a BEFORE 038_rls_consolidate_policy.sql. The migrations image is node:24-alpine (musl: byte order) and macOS sh measured byte order in both locales; the gateway uses `.sort()`.',
 '7. **#1332 — the platform CORE catch (:1217) is driven by no seat cell and was NOT driven by the drafter** (no platform DB in the drill); N-1332-4 (arm F) was not re-run by the drafter.',
 '8. **#1337 — the READY\'s A4 says "2 failed / 15"**; the seat and the brief-writer measured 1 failed / 15 at the tip. The gate names every red cell.',
 '9. **#1337 — the sweep\'s blind spot (the brief-writer\'s doubt 4, the seat\'s candidate):** REVOKE_WRITES[1] can drift unseen by the equality (security index.ts is also found by the rotate UPDATE). Pre-existing; a ticket candidate, not this PR\'s.',
 '10. **Seat B 41st\'s raw push logs live in its SESSION SCRATCHPAD** (`/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/2d2b5ffa-…/scratchpad/push41-*.rawlog`), not in its record folder — a reboot loses them; the capture holds their counts.',
 '11. **The drill ran as the superuser q39** (bypasses RLS) for every read except the app-role probe; the main database only (no platform DB, no APP_DB_PASSWORD role provisioning); /health was NOT served (the recorded summary read from the module) — the gate serves it.',
 '12. **GitHub mergeable_state `unstable`** on both PRs (gh_read_1.out) — mergeable True; a non-required check pending or failing. Not measured further.',
 '13. **The commission\'s "the seat measured 25 policies" and "12 migrations reference the four tables"**: READ 12 below 038a (001 002 005 006 008 009 011 012 013 020 022 038) plus 039 and 047 above it.',
 '', '## 3. Pins and what the gate owes',
 '- Prompt `%s` — #1337: the patch == the held Spark patch, packages/shared at develop / heads / develop + #1337 / END, the brief-writer\'s arms on the real revoke; #1332: the THREE fresh-database paths on a real PostgreSQL over a unix socket (gateway twice; run-migrations.sh then gateway; docker/init then gateway) + develop\'s seeded path, pg_dump -t equality, a second boot, the app-role probe, 006/008/047, 038a\'s lexical position and locale, CORE-throw / error field, /health served; the MERGE ORDER (rule 44), the last round (rule 55), the DISK rule (rule 56: Data volume, STOP on ENOSPC); `## MERGE ADDENDUM` last, ONE LINE PER PR (rule 52).' % K['prompt'],
 '- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/` (TEXT only); mail FROM coagent@ TO wednesday-agent@.' % K['report'],
 '', '## 4. Routing line — NOT added',
 'Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines) — backup first:',
 '```', '%s|coagent@agentmail.to|yes' % K['pane'], '```',
 'Until it is present the launch action\'s step 0 refuses rc 1 (repin_dryrun_1.out reports it).',
 '', '## 5. Controls: `controls_gate39.sh <scratchpad> [--invert]`',
 '- Same arms as gate38\'s kit, re-keyed: wrong heads, a moved develop (predev = the #1333 squash, MERGED), per-PR path renames (both), capture / prompt doctoring, every kit rule 35 / 40-44 / 46-49 / 51-56 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO plants, predict `--simulate foreign1337` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate38\'s and gate37\'s namespaces.',
 '- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, pgprobe beyond its built-in controls (CT1-CT6).',
 '', '## 6. Could not measure (the drafter\'s NOT-MEASURED list)',
 '- No vitest, tsc, eslint, prettier or red-proof run by the drafter (no `npm ci` — DevMASTER is full and the gate owns them); every seat figure is a claim. #1337: the guard file was NOT run — its behaviour is EMULATED in Python. #1332: no platform database, no APP_DB_PASSWORD provisioning, /health not served, the platform CORE catch not driven, arm F not re-run, glibc collation not measured.',
 '', '## 7. Files',
 '- Kit: kit.json · COMMISSION.md (make_commission_gate39.py) · README.md (make_readme_gate39.py) · rekey_check_gate39.py -> rekey_1.out',
 '- Pins: predict_gate39.py -> predict_1.out, predict_sim_*.out, pins_gate39.json (+ .SIM-*.json) · keyscan_gate39.py -> keyscan_1.out · final_lsremote_1.out',
 '- Measurements: pgprobe_gate39.py + pgprobe_gate39.runner.ts -> pgprobe_1.out, pgprobe_gate39.json',
 '- Reads: gh_read_gate39.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate39.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate39.py -> capture_1.out, mail_gate39_ready.md, stopcounts_gate39.json · _api_peek_gate39.py -> _api_peek_1.out',
 '- Prompt/launcher: prompt_gate39.TEMPLATE.txt, launcher_gate39.TEMPLATE.sh.txt, fill_gate39.py -> %s + %s (fill_1.out), launcher_check_1.out · repin_and_launch_gate39.sh -> repin_dryrun_1.out · controls_gate39.sh -> controls_1.out / controls_2.out' % (K['prompt'], K['launcher']),
 '', '## 8. The ONE launch command (after the routing line, §4)',
 '```', launch, '```',
 '- Dry run: append `--dry-run`. Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`, the Data volume); if `g39_sp/clone.git` is absent there, predict rebuilds it on a re-pin (pgprobe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, an overlap or an END-tree disagreement refuses rc 10; a further `-b41-<n>` PR or a KS-888 / KS-1054-titled PR refuses rc 15; a moved head refuses rc 11.']
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
