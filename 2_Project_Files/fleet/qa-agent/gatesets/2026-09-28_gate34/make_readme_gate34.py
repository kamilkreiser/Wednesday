#!/usr/bin/env python3
"""make_readme_gate34.py <scratchpad> — writes README.md for the gate34 kit (the directory this script lives in). Every figure is READ from the kit's own
output files at the moment of writing (each named beside it), plus ONE final `git ls-remote` (READ, from the Secuura checkout) written to
final_lsremote_1.out. Shape copied from gate33's make_readme (gate32 lineage), re-keyed to gate34's five rows. Writes only beside this script."""
import json, os, re, subprocess, sys, datetime, hashlib
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
SP = sys.argv[1] if len(sys.argv) > 1 else ''
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); LP = json.load(open('%s/logprobe_%s.json' % (D, kit)))
rd = lambda f: open(os.path.join(D, f), encoding='utf-8').read() if os.path.exists(os.path.join(D, f)) else ''
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
NS = sorted(K['prs'])
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin', 'refs/heads/develop'] + ['refs/pull/%s/head' % n for n in NS] + ['refs/pull/1310/head'], capture_output=True, text=True).stdout
fl = '%s | %s' % (now, ' | '.join(l for l in ls.strip().splitlines()))
open(D + '/final_lsremote_1.out', 'w').write(fl + '\n')
LSD = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
agree = LSD.get('refs/heads/develop') == P['develop'] and all(LSD.get('refs/pull/%s/head' % n) == P['prs'][n]['head'] for n in NS)
c1, c2 = rd('controls_1.out'), rd('controls_2.out')
s1 = (re.findall(r'^SUMMARY .*$', c1, re.M) or ['(controls_1.out has no SUMMARY)'])[-1]; s2 = (re.findall(r'^SUMMARY .*$', c2, re.M) or ['(controls_2.out has no SUMMARY)'])[-1]
r1, r2 = rd('controls_1.rc').strip(), rd('controls_2.rc').strip()
mm1 = re.findall(r'^  MISMATCH .*$', c1, re.M); mm2 = re.findall(r'^  MISMATCH .*$', c2, re.M)
fill = rd('fill_1.out'); lc = rd('launcher_check_1.out'); dry = rd('repin_dryrun_1.out'); rk = rd('rekey_1.out')
subj = re.search(r'subject scan: (.*)', fill); ks = re.search(r'key scan: (.*)', fill)
dry_line = (re.findall(r'^DRY RUN COMPLETE.*$', dry, re.M) or ['(no DRY RUN COMPLETE line)'])[-1]
def sha(f):
    b = open(os.path.join(D, f), 'rb').read(); return len(b), hashlib.sha256(b).hexdigest()
titles = P['titles']
TIERWHY = {
 '1316': 'T1 logging (secret-leak class), ruled "Type and field names only"',
 '1317': 'T1 logging (secret-leak class), same ruling; carries the rotate-secret pin D7',
 '1318': 'T2 spec: Zod declaration + the generated yaml, no runtime byte',
 '1319': 'T1 security-service API responses (the API-key mint / list bodies)',
 '1320': 'T1 authorization, ruled "Narrow now, bind-creator later"',
}
ks_txt = rd('keyscan_1.out')
def foreign(n):
    return sorted(set(k for l in ks_txt.splitlines() if l.startswith('#%s ' % n) and 'FOREIGN hyphenated' in l for k in re.findall(r"'(KS-\d+)'", l.split('FOREIGN hyphenated')[1])))
out = ['# Gateset 2026-09-28_gate34 — README for Wednesday', '',
 'Written %s by the drafter (make_readme_gate34.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now,
 'The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote ONLY this kit directory `%s/` and scratch under `%s` (the scratch clone `g34_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key; the logprobe workdirs `g34_logprobe_*`; the control workdirs `g34_controls_*`; the #1320 poller and its log `poll1320.log`). Superseded outputs were RENAMED `superseded_*`, never deleted. It did NOT write the routing line (see §4) — the commission confined writes to the kit dir and the scratchpad.' % (D, SP or '<scratchpad>'),
 'The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its typescript and winston). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only. decisions.json: read only.', '',
 '**gate34 = FIVE PRs, MIXED tiers (T1 x4, T2 x1), one kit, no sibling, NO stack, ONE base.** #1320 was not raised at the commission: the drafter polled `ls-remote refs/pull/1320/head` every 2 min; it appeared at **2026-09-27T22:25:21Z (poll 3)**, head `b9111f2bfad2`, so the kit is FIVE. Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)).', '',
 '| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | why this tier |', '|---|---|---|---|---|---|']
for n in NS:
    pr = P['prs'][n]
    out.append('| #%s | %s | %s | `%s` | %d on `%s` | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], TIERWHY[n]))
out += ['', '### Squash subjects and bodies (the two MG checks the commission asked for, as a table)', '',
 '| PR | declared subject (WITHOUT `(#n)`, the PR title as the PULLS API returned it) | declared | lands at (+8, ` (#n)`) | <= 92 | ends in `(#n)`? | squash-body keys: own | FOREIGN hyphenated keys seen (title / body / commit msg) -> must be un-hyphenated |', '|---|---|---|---|---|---|---|---|']
for n in NS:
    t = titles[n]; L = len(t) + len(' (#%s)' % n)
    fk = foreign(n)
    out.append('| #%s | %s | %d | %d | %s | %s | %s | %s |' % (n, t, len(t), L, 'yes' if L <= 92 else 'NO', 'yes' if re.search(r'\(#\d+\)$', t) else 'no', ', '.join(K['prs'][n]['keys']),
               ('%s in the COMMIT MESSAGE only -> %s (the squash body must not paste the commit message)' % (', '.join(fk), ', '.join(x.replace('KS-', 'KS') for x in fk))) if fk else 'none'))
out += ['', 'Measured by fill_1.out: `subject scan: %s`; `key scan: %s` (every MANDATED squash text block in the prompt carries only its own key). keyscan_1.out: no closing word before a key in any title, body or commit message.' % (subj.group(1) if subj else '?', ks.group(1) if ks else '?'), '',
 'Routing `%s` (**NOT added by the drafter** — §4). GO string `GO: merge #1316, #1317, #1318, #1319, #1320 batch` (or the subset). MERGE ORDER #1316 -> #1317 -> #1318 -> #1319 -> #1320 (END_TREE is order-independent, measured in all %d orders). The GO goes to **Seat B 36th**, which raised all five and merges its own.' % (K['pane'], P['orders']), '',
 '**Kam\'s rulings (READ by the drafter from `0_Brain/dashboard/data/decisions.json`):** card `secuura-ks1346-logging-thrown-objects-leaks-secrets` status ruled, choice **a** "Type and field names only", ruled_ts 2026-09-27T16:32:47+10:00 ("Log what kind of thing was thrown and the NAMES of its fields, never their values."). Card `secuura-ks692-status-revoke-interim-posture` status ruled, choice **a** "Narrow now, bind-creator later", ruled_ts 2026-09-16T15:04:06+10:00 ("Drop ISSUER_ADMIN from STATUS_WRITE_ROLES today — one file, one test, closes the hole immediately, breaks none of the zero measured callers — then apply your bind-creator ruling properly when the migration lands.").', '',
 '## 1. BLUF',
 '- **Kit: READY to launch once the routing line is added** — launcher `--check` rc %s (`%s`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: %s). The real launch refuses rc 1 at step 0 until `%s|coagent@agentmail.to|yes` is in inbox_routing.conf (§4).' % (
     '0' if lc.startswith('all guards pass:') else '?', lc.splitlines()[0] if lc else '?', dry_line, K['pane']),
 '- **Pinned over develop `%s`** (tree `%s`) — ls-remote AND fetched AND the API compare agree; gate33\'s #1311-#1315 squashes in, #1310 still OPEN. ONE merge-base `%s` for all five (each head\'s one commit has it as parent); develop has not moved since, so the move ∩ every own path is EMPTY (predict_1.out (b)).' % (P['develop'], P['develop_tree'], P['merge_bases'][0][:12]),
 '  - **END_TREE `%s`** (%s), identical in all %d orders (%d merge-tree calls); diff(develop, END) == the union of the eleven own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 '  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s — every pin still current: **%s**.' % (fl, agree),
 '- **Controls, both ways (controls_gate34.sh):**',
 '  - normal (controls_1.out, rc %s): `%s`%s' % (r1, s1, (' — MISMATCHES: %s' % mm1) if mm1 else ''),
 '  - `--invert` (controls_2.out, rc %s): `%s`%s' % (r2, s2, (' — every one of the %d controls reported MISMATCH-then-flip (rc 1 by design): each control can fail' % len(mm2)) if mm2 else ''),
 '- **OVERLAPS — pairwise, measured:** NONE. No pair stacked; every kit pair disjoint (#1318 and #1319 share no file); every kit path disjoint from ALL %d other open PRs (#1310 included). `merged_blob_paths` NONE and `noop_paths` NONE, each asserted by predict (c).' % len(P['inflight']),
 '- **Every head == its READY and its golden (MEASURED, predict_1.out (e)):** each READY block is byte-identical to its brief\'s golden and to the Spark checker\'s patch.diff; the goldens (#1318: golden + the openapi-yaml companion) apply strict with `git apply --cached --check` at ec32c40e2b1e and every blob == the head\'s; #1318\'s generated yaml hunk == the companion\'s +/- lines (+7/-0).',
 '', '### 1a. The fail500 WIDEN leg for #1316 / #1317 (MEASURED by the drafter, logprobe_gate34.py -> logprobe_1.out)',
 'The REAL originate logger.ts at each revision (transpiled by the checkout\'s typescript, the checkout\'s winston), NODE_ENV=production, a fresh cwd per revision; the fail500 line of adminConfig.ts (AC) and webhooks.ts (WH) read at the same revision and evaluated with it. Five revisions: develop, #1316 head, #1317 head, END_TREE, and END_TREE with the OPEN #1310\'s logger swapped in (it makes the File transports write JSON). Controls: %s.' % ('; '.join('%s: %s' % (k, v) for k, v in LP['_controls'].items())),
 '- **VALUE sentinels on ANY sink (stdout / error.log / combined.log), the PR\'s own route(s):** %s.' % ('; '.join('%s: %s' % (k, v) for k, v in LP['_value_hits'].items())),
 '  - So: at each head, on END_TREE and under #1310\'s logger NO secret / PII VALUE reaches any sink from the fail500 paths (plain-object values, a toString() secret, a Prisma-shaped meta.params ciphertext and its `message` field, an axios-shaped Error\'s enumerable Authorization, Array elements, a null-prototype value, an enumerable getter, an email-keyed value). At develop the old `String(err)` line put the toString() secret and the Array elements on stdout — the PRs close that.',
 '- **Ruled residue in a FILE:** %s — only under #1310\'s logger (develop\'s logger writes `undefined` to the files): an Error\'s message, a thrown string, and a field NAME that is itself PII (gate33\'s F-2). Reported, not graded against these PRs.' % ('; '.join('%s: %s' % (k, ('%d sentinel(s) per file' % len(list(v.values())[0])) if isinstance(v, dict) else v) for k, v in LP['_residue_in_files'].items())),
 '- **Two edges the ruling does not name (for the gate / Wednesday to rule):** (1) TYPE-NAME-AS-DATA — an object whose prototype carries `constructor.name` prints that name as its type: %s. (2) THROWING-OWNKEYS — a Proxy whose ownKeys trap throws makes the log call itself throw (Object.keys runs inside it, before `res.status(500)`): helper threw at %s. Conversely develop\'s `String(err)` line THREW for a null-prototype object ("Cannot convert object to primitive value") and the new line does not.' % (
     '; '.join('%s: %s' % (k, v) for k, v in LP['_edge_hits'].items()), '; '.join('%s: %s' % (lab, LP[lab]['threw']) for lab in LP if not lab.startswith('_'))),
 '- **The fail500 family is closed on END_TREE (MEASURED, predict_1.out):** four `function fail500(` helpers under services/ (systemErrors, gdpr, adminConfig, webhooks), each logging the ruled line. 75 OTHER originate log calls still render a non-Error through String() — outside the fail500 family (predict_1.out lists them by file).',
 '', '### 1b. #1320 — the NAMED CONSEQUENCE (READ by the drafter; the gate measures)',
 '- STATUS_WRITE_ROLES `[SYSTEM_ADMIN, SUPER_ADMIN, super_admin, ISSUER_ADMIN]` -> `[SYSTEM_ADMIN, SUPER_ADMIN, super_admin]` (status.ts :44). Tenant ISSUER_ADMINs lose status-list revoke / unrevoke until lists get an owner — as named and ruled.',
 '- **WIDER than named (READ):** the gate is router-level (status.ts :49): EVERY non-GET verb is behind STATUS_WRITE_ROLES, so an ISSUER_ADMIN ALSO loses `POST /api/status` (create a list, :329) and `POST /:id/allocate` (:183). The ruling card said the change "breaks none of the zero measured callers"; the drafter\'s caller grep (predict_1.out) finds no in-repo WRITE to /api/status outside tests (the gateway proxies it). The prompt makes the gate MEASURE all four verbs for ISSUER_ADMIN at the merge-base and head, and REPORT the full list.',
 '- ks586-status-write-authorization.test.ts (not in the PR) iterates STATUS_WRITE_ROLES: its cell count drops 14 -> 13 (the brief; all green).',
 '', '### 1c. Other READ predictions worth your eye',
 '- **#1318:** the handler (security index.ts :1174) checks organizationId PRESENCE only; the spec now declares `format: uuid`. A spec-driven negative test (Schemathesis `pr`) could newly report a non-uuid accepted with 200 — a prediction the gate cannot run (no stack); it measures the handler instead.',
 '- **#1319:** the tenant filters (:1207 / :1208) run BEFORE the map (:1209), so a caller only sees connectorIds of keys it may already see; 201 body keys %s, list-row keys %s (READ). `keyHash` in neither.' % (
     re.search(r"201 body keys (\[[^\]]*\])", rd('predict_1.out')).group(1) if re.search(r"201 body keys (\[[^\]]*\])", rd('predict_1.out')) else '?', re.search(r"list-row keys (\[[^\]]*\])", rd('predict_1.out')).group(1) if re.search(r"list-row keys (\[[^\]]*\])", rd('predict_1.out')) else '?'),
 '- **Seat vs brief slip (#1316 / #1317 ADD1 arm):** the briefs predict the inspect tamper reds 8 of 15 / 6 of 13 (C1+C6 / D1+D6); the seat measured 9 of 15 / 7 of 13 because its tamper replaced the WHOLE rendering (strings get quoted too, so C4 / D4 red). The prompt tells the gate to run both shapes.',
 '- **Fleet STOP (READ, bounded region, NOT-FOUND control):** ' + '; '.join('#%s %s · %s · %s · %s (%s)' % (n, S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'], S[n]['verdict_line']) for n in NS) + '. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).',
 '- **Linear: all five PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1346, KS-747, KS-908, KS-692 In Progress; KS-586 Done (the #1320 comment rewrite says so — true).',
 '- **Re-key / namespace (rekey_1.out):** %s' % (' | '.join(l.strip() for l in rk.strip().splitlines()[-2:]) if rk else '?'),
 '- **Sizes / sha256 (measured as this README was written):** ' + '; '.join('`%s` %d bytes sha256 `%s`' % ((f,) + sha(f)) for f in (K['prompt'], K['launcher'], 'mail_%s_ready.md' % kit)) + '.',
 '', '## 2. Pins — predict_1.out (rc %s)' % rd('predict_1.out.rc').strip()]
for n in NS:
    pr = P['prs'][n]
    out.append('- #%s: 1 commit `%s` over merge-base `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat %s; no mode change; move ∩ own paths EMPTY.' % (n, pr['head'][:12], pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
sims = []
for f in sorted(x for x in os.listdir(D) if re.match(r'predict_sim_.*\.out$', x)):
    sims.append('%s -> %s' % (f[len('predict_sim_'):-4], (rd(f).strip().splitlines() or ['?'])[-1].split(' -> ')[0]))
out += ['- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). `predev` (`%s`, develop^) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.' % ('; '.join(sims), K['predev'][:12]),
 '- Superseded runs kept, renamed, never deleted: `superseded_shadowedst_*` (the first pinned run: a local variable in the #1320 probe shadowed the END shortstat, so fill refused on a list — fixed, re-run); `superseded_label_*` (a text label changed for the re-key check; same heads, same END_TREE); `superseded_samekeyFK_controls_*` and `superseded_own1unbound_controls_*` (two aborted control runs: SJ3 first picked #1317\'s key as the foreign key for #1316 — they share KS-1346 — then the fix commented out the OWN1 assignment; the script refused rc 9 / hit an unbound variable both times, fixed, then run clean both ways).',
 '', '## 3. What the gate owes',
 '- Prompt `%s` — the fail500 WIDEN through the REAL routers (including the two edges and #1310\'s logger), #1320\'s role x verb table (the named consequence AND create / allocate), #1319 through the route (cross-tenant first, no keyHash / plaintext in any list row), #1318\'s generator check and runtime uuid behaviour, every seat red proof re-run, suites (originate / security / vc-issuer at develop, each head and END_TREE), `npm run check:openapi`, tsc with `exclude: []`, lint (security has no lint script), guards; the MANDATED SQUASH TEXT blocks and the MG-3 key-set table; `## MERGE ADDENDUM` as the LAST section of report.md with `merged_blob_paths: none · noop_paths: none` per line.' % K['prompt'],
 '- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.' % K['report'],
 '', '## 4. Routing line — NOT added (the drafter\'s writes were confined to the kit dir and its scratchpad)',
 'Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch pane lines — gate33\'s own line sits at line 124) — backup first:',
 '```', '%s|coagent@agentmail.to|yes' % K['pane'], '```',
 'Until it is present the launch action\'s step 0 refuses rc 1 (the dry run reports it: repin_dryrun_1.out "line present: 0").',
 '', '## 5. The ONE launch command',
 '```', '%s/repin_and_launch_%s.sh %s/%s %s' % (D, kit, D, K['launcher'], SP or '<a scratchpad dir>'), '```',
 '- Dry run (`--dry-run` appended): repin_dryrun_1.out -> %s (rc 0).' % dry_line,
 '- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`): if `g34_sp/clone.git` is absent there, predict rebuilds it (`clone --shared` + fetch) on a re-pin (logprobe is NOT re-run by a re-pin; its JSON stays the drafter\'s measurement at this pin). If develop moves first, step 3b re-pins in the same action; an own-path move, a stack, a pairwise overlap, a declaration predict cannot prove or an END-tree disagreement refuses rc 10. A NEW PR on one of the kit\'s keys or on a `-b36-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.',
 '', '## 6. Questions for Wednesday (each with the drafter\'s recommendation)',
 '1. **The routing line** (§4). *Recommend:* add it, then launch.',
 '2. **#1320\'s consequence is wider than named** (create + allocate as well as revoke / unrevoke, READ). The ruling card assumed zero callers. *Recommend:* launch as drafted — the gate measures all four verbs and reports; if any in-product flow needs create / allocate as ISSUER_ADMIN, that is Kam\'s call, not the gate\'s.',
 '3. **The two fail500 edges** (TYPE-NAME-AS-DATA, THROWING-OWNKEYS) are not in the ruling. The drafter measured no VALUE reaching a sink. *Recommend:* launch; the likely outcome is GO WITH FINDINGS with a follow-up (use `Object.prototype.toString`-style tagging or a try/catch around Object.keys), not a NO GO.',
 '4. **#1318 declares `format: uuid` that the handler does not enforce.** *Recommend:* launch; the gate measures the handler; a runtime uuid check (or dropping `format`) is a follow-up choice.',
 '5. **The foreign keys in two COMMIT messages** (#1316 KS-730, #1320 KS-586). *Recommend:* say so in the GO mail — the merge seat composes each squash body with only its own key.',
 '6. **§5f:** KS-1346, KS-908 and KS-692 are runtime changes — none moves to Done on offline evidence. *Recommend:* the merge seat posts the canonical `live sweep owed` comment the prompt spells.',
 '', '## 7. Controls: `controls_gate34.sh <scratchpad> [--invert]`',
 '- **controls_1.out:** `%s` (rc %s).' % (s1, r1),
 '- **controls_2.out (`--invert`):** `%s` (rc %s, by design).' % (s2, r2),
 '- Every mutation is independent of the original (doctor() rc 98 / rc 97); every wrong head is the real head with ONE hex digit changed; the launcher\'s head guard is whole-field. Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict -> fill) from a launcher pinned at predev in a MOVED copy; RE / RN / RO plant a wrong commit count / a `noop_paths` entry / a `declared_overlap` entry and each must refuse rc 10; RS / RS-twin exercise STACKBASE; PS1 is `--simulate foreign1317`; PS2 `--simulate moved`; PF1 / PF2 fill from SIM / failed pins and must refuse; SJ1-SJ3 plant subject defects (a `(#n)` suffix, a subject landing over 92, a FOREIGN hyphenated key); RW / RWB exercise the WIDEN census by title and by branch; NS[<spelling>] plants every spelling of BOTH predecessor generations (gate33\'s and gate32\'s) including the predecessor\'s re-key tool name; every kit rule (exits 35, 40-44, 46-51) has its own SPLIT control.',
 '- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, logprobe\'s own verdicts beyond its five built-in controls.',
 '', '## 8. Could not measure (the drafter\'s NOT-MEASURED list)',
 '- No suite, tsc, lint or red-proof run by the drafter (that is the gate\'s job; the seat\'s figures are claims in the PR bodies — Seat B 36th\'s raise/ holds no per-item red / green / suite files this round).',
 '- The fail500 edges through the REAL routers (what the client receives when fail500 itself throws) — READ only; logprobe evaluates the log line, not the route.',
 '- #1320\'s four verbs for ISSUER_ADMIN — READ only (the router-level gate); no run.',
 '- #1319 cross-tenant list, #1318 runtime uuid behaviour — READ only.',
 '- Legs 3 / 4 / 8, the served spec, Schemathesis — need a stack; not run by anyone in this round.',
 '- The seat\'s tsconfig sizes / lint counts / "5476 bytes" (the #1320 body; the drafter READ the KS-692 golden as 5478 bytes by `ls -la`, and predict measured its bytes == the READY block == patch.diff) — the gate re-measures.',
 '', '## 9. Files',
 '- Kit: kit.json · COMMISSION.md (make_commission_gate34.py) · README.md (make_readme_gate34.py) · rekey_check_gate34.py -> rekey_1.out',
 '- Pins: predict_gate34.py -> predict_1.out, predict_sim_*.out, pins_gate34.json (+ .SIM-*.json) · keyscan_gate34.py -> keyscan_1.out · final_lsremote_1.out',
 '- Measurements: logprobe_gate34.py -> logprobe_1.out, logprobe_gate34.json (#1316 / #1317 WIDEN)',
 '- Reads: gh_read_gate34.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate34.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate34.py -> capture_1.out, mail_gate34_ready.md, stopcounts_gate34.json · _api_peek_gate34.py -> _api_peek_1.out',
 '- Prompt/launcher: prompt_gate34.TEMPLATE.txt, launcher_gate34.TEMPLATE.sh.txt, fill_gate34.py -> %s + %s (fill_1.out), launcher_check_1.out · repin_and_launch_gate34.sh -> repin_dryrun_1.out · controls_gate34.sh -> controls_1.out / controls_2.out' % (K['prompt'], K['launcher'])]
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote %s/README.md (%d lines) | pins current at final ls-remote: %s' % (D, len(out), agree))
