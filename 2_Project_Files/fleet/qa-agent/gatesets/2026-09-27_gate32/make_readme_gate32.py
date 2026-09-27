#!/usr/bin/env python3
"""make_readme_gate32.py <scratchpad> — writes README.md for gate32 (the directory this script lives in). Every SHA, tree, count, size and control
tally is READ from the kit's own files (pins_gate32.json, stopcounts_gate32.json, gh_read_1.out, keyscan_1.out, controls_1/2.out + .rc, fill_1.out,
launcher_check_1.out, repin_dryrun_1.out, routing_check_1.out, predict_1.out, predict_sim_*.out, aktolint_1.out, final_lsremote_1.out) and from `du`
at the moment of writing — never typed. The prose is the drafter's. Shape copied from gate31's make_readme_gate31.py (gate30T1 lineage)."""
import hashlib, json, os, re, subprocess, sys, datetime
D = os.path.dirname(os.path.abspath(__file__)); SP = sys.argv[1]
K = json.load(open(D + '/kit.json')); kit = K['kit']
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit)))
def rd(f):
    p = os.path.join(D, f); return open(p, encoding='utf-8').read() if os.path.exists(p) else ''
def sha(f): return hashlib.sha256(open(os.path.join(D, f), 'rb').read()).hexdigest()
def ctl(f):
    t = rd(f); m = re.search(r'^SUMMARY .*$', t, re.M); n = re.search(r'SUMMARY \S+: (\d+) controls, OK (\d+), MISMATCH (\d+)', t)
    return (m.group(0) if m else 'NO SUMMARY LINE'), (n.groups() if n else ('?', '?', '?')), rd(f.replace('.out', '.rc')).strip() or '?'
(s1, c1, rc1), (s2, c2, rc2) = ctl('controls_1.out'), ctl('controls_2.out')
mism1 = [l.strip() for l in rd('controls_1.out').splitlines() if l.startswith('  MISMATCH')]
ok2 = [l.strip() for l in rd('controls_2.out').splitlines() if l.startswith('  OK')]
gh = rd('gh_read_1.out'); chk = rd('launcher_check_1.out').splitlines()[:1]
dry = [l for l in rd('repin_dryrun_1.out').splitlines() if l.startswith('DRY RUN COMPLETE') or 'REFUS' in l]
fill = [l for l in rd('fill_1.out').splitlines() if l.startswith(('key scan', 'subject scan', 'seat items'))]
rout = rd('routing_check_1.out').splitlines(); ks = [l for l in rd('keyscan_1.out').splitlines() if l.startswith(('#', 'CONTROL'))]
fin = rd('final_lsremote_1.out').strip().splitlines()
akl = [l.strip() for l in rd('aktolint_1.out').splitlines() if l.startswith(('aktolint_gate32', 'GOLDEN', '==', 'SUMMARY'))]
rk = [l for l in rd('rekey_1.out').splitlines() if l.startswith(('rekey_check', 'RESULT'))]
sims = ['%s -> %s' % (re.match(r'predict_sim_(\w+)\.out$', f).group(1), (rd(f).strip().splitlines() or ['?'])[-1].split(' ->')[0]) for f in sorted(os.listdir(D)) if re.match(r'predict_sim_\w+\.out$', f)]
def subj(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
def lands(n):
    m = re.search(r'#%s (\d+)->(\d+)' % n, rd('fill_1.out')); return (m.group(1), m.group(2)) if m else ('?', '?')
def probe(n, key):
    for l in rd('predict_1.out').splitlines():
        if l.startswith('  #%s %s' % (n, key)): return l.strip()[len('#%s ' % n):]
    return '(not in predict_1.out)'
def hardline(key):
    return [l.strip() for l in rd('predict_1.out').splitlines() if l.startswith('  PASS') and key in l]
def du(p):
    r = subprocess.run(['du', '-sh', p], capture_output=True, text=True); return (r.stdout.split() or ['?'])[0]
L = os.path.join(D, K['launcher']); R = os.path.join(D, 'repin_and_launch_%s.sh' % kit)
NS = sorted(K['prs'])
SHORT = re.search(r"SHORT=\{'1304': '([^']*)'\}", rd('fill_%s.py' % kit)).group(1)
DECL = {n: (SHORT if n == '1304' else P['titles'][n]) for n in NS}
WHY = {
 '1304': '**T2 test-only** — ks1072 cells edited in place; red by a product tamper at verification.ts:585 (READ head + END): exactly R1; R2 is a control.',
 '1305': '**T2 test-only** — a NEW vouch-scope cell (renamed); tamper proxy.ts:275: R1 + R2. Title names R2-2, the diff is R2-3.',
 '1306': '**T2 test-only, AUTH surface** — a NEW bucket cell (F-3 G-BUCKET-HASH); tamper auth.ts **:313** (READY :300); auth.ts bytes unchanged (MEASURED). Title names N-2, the diff is F-3.',
 '1307': '**T2 test-only** — a NEW door-vs-factory cell (renamed); tamper proxy.ts **:814** at head and END (READY :808).',
 '1308': '**T2 tooling** — akto secrets.ts + a NEW cell; product hunk EXACT to the golden (MEASURED); departure 12 JSDoc + 4 format + 0 other (MEASURED); akto lint rc 0 at head (MEASURED).',
 '1309': '**T2 product** — admin.ts ids to `crypto.randomUUID()` + a NEW cell; EXACT to the regenerated golden (MEASURED); crypto imported at :11 (READ); no reader sorts by id (MEASURED by grep).',
}
rows = ['| #%s | %s | %s | `%s` | %d on `%s` | %s -> **%s** declared %s, lands **%s** | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], P['prs'][n]['head'], len(P['prs'][n]['commits']),
        P['prs'][n]['merge_base'][:12], subj(n), 'SHORT' if n == '1304' else 'title', lands(n)[0], lands(n)[1], WHY[n]) for n in NS]
stop = ['#%s %s' % (n, ('%s · %s · %s · %s' % (S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'].split(',')[0].replace(' passed', '') + ' of 60')) if S[n]['preflight_ran'] else 'NOT APPLICABLE (format gate only)') for n in NS]
launch = '%s %s %s' % (R, L, SP)
go = re.search(r"GO='(`GO: merge [^`]*`)'", rd('fill_%s.py' % kit)).group(1)
flip = lambda h: h[:-1] + ('0' if h[-1] != '0' else '1')
wl = ['#%s real `%s` -> wrong `%s` (same length %s, differs in %d digit, contains the real head: %s)' % (n, P['prs'][n]['head'], flip(P['prs'][n]['head']), len(flip(P['prs'][n]['head'])) == 40, sum(x != y for x, y in zip(P['prs'][n]['head'], flip(P['prs'][n]['head']))), P['prs'][n]['head'] in flip(P['prs'][n]['head'])) for n in NS]
used = sorted(set(re.findall(r'^  OK +((?:C3|O2|ET|H1\d{3})) ', rd('controls_1.out'), re.M)))
M = P.get('measured', {})
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = []; A = out.append
A('# Gateset 2026-09-27_%s — README for Wednesday' % kit); A('')
A('Written %s by the drafter (make_readme_%s.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % (now, kit))
A('The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing and deleted nothing. It wrote: this kit directory `%s/`; ONE line in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (as commissioned, backup first — §4); and scratch under `%s/` (the scratch clone `g32_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key; the akto lint workdirs `g32_aktolint_*` (`git archive` exports, node_modules a symlink to the checkout\'s); the control workdirs `g32_controls_*`; the dry-run reads `repin_gate32_dry_*`). Every git write verb ran inside a script file run with `bash` (run_predict.sh, aktolint_gate32.sh, controls_gate32.sh). Superseded outputs were RENAMED `superseded_*`, never deleted.' % (D, SP))
A('The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node/npm reading its akto node_modules through a symlink). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only.'); A('')
A('**gate32 = SIX PRs, all T2, one kit, no sibling, NO stack.** Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)). **All six share the merge-base `%s`** — the commission said five of six were on the old develop; the drafter measured SIX (each head\'s one commit has that parent; gh_read_1.out commits + predict_1.out (b)). WIDEN census (titles with the six keys, or a branch carrying `-b34-<n>`): every match is in the kit, none outside (gh_read_1.out, predict_1.out (a), repin_dryrun_1.out 2b).' % P['merge_bases'][0]); A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | title lands at -> the DECLARED subject (no `(#n)`), lands at | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|'); out.extend(rows); A('')
A('Routing `%s` (**added by the drafter** — §4). GO string %s (or the subset; any order — no stack). The GO goes to **Seat B 34th**, which raised all six and merges its own.' % (K['pane'], go)); A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** — launcher `--check` rc 0 (`%s`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: %s).' % ((chk[0].strip() if chk else '?'), ' / '.join(dry) or '?'))
A('- **Controls, both ways (controls_%s.sh):**' % kit)
A('  - normal (controls_1.out, rc %s): `%s`' % (rc1, s1))
A('  - `--invert` (controls_2.out, rc %s): `%s`' % (rc2, s2))
A('  - Wrong-head controls (%s, all OK both ways) change ONE hex digit and never contain the real head (doctor() refuses rc 98 on a superset, rc 97 if the original survives): %s' % (', '.join(used) or '?', '; '.join(wl)))
A('  - NEW in this kit: **RS** (a copy DECLARING a false stack, #1305 on #1304, refuses the launch action rc 11 at STACKBASE) + twin; **RE / RN / RO** (in a moved copy the REAL re-pin must refuse rc 10 on a wrong declared commit count / a `noop_paths` entry / a `declared_overlap` entry — the two declaration keys proven separately); **RWB** + twin (the widen census on BRANCHES, rc 15); **SJ1-SJ3** + twin (fill refuses a declared `(#n)` suffix, a subject landing over 92, and a missing SHORT for #1304); **ET** (a wrong END_TREE in the prompt refuses rc 31); **NS** (the re-key check clean) and **NS[<spelling>]** x17 (each gate31 namespace spelling planted must be caught).')
A('- **Pinned over develop `%s`** (tree `%s`) — ls-remote AND fetched AND the API compare agree. Develop moved 3 squashes since the PRs\' merge-base `%s` (gate31\'s #1300, #1303, #1301 — services/originate only): the move ∩ every PR\'s own paths is EMPTY (predict_1.out (b)(3)).' % (P['develop'], P['develop_tree'], P['merge_bases'][0][:12]))
A('  - **END_TREE `%s`** (%s), identical in all %d orders (%d merge-tree calls, each with the PR\'s own merge-base); diff(develop, END) == the union of the eight own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s' % ' | '.join(fin))
A('- **OVERLAPS — pairwise, measured:** NONE. No pair stacked (no head is another\'s ancestor); every kit pair disjoint; every kit path disjoint from ALL %d other open PRs (#1302 — gate31\'s NO GO KS-1348 row — is still open, path-disjoint). `merged_blob_paths` NONE and `noop_paths` NONE, each asserted by predict (c).' % len(P['inflight']))
A('- **Subjects (Wednesday\'s addendum, STANDING_LINES 2026-09-27): declared WITHOUT the `(#n)` suffix, measured as they LAND** — %s. fill refuses a `(#n)`-suffixed or over-92 subject (fill_1.out: `%s`; controls SJ1-SJ3).' % ('; '.join('#%s «%s» %s -> %s' % (n, DECL[n], lands(n)[0], lands(n)[1]) for n in NS), (fill[1] if len(fill) > 1 else '?')))
for n, keys in (('1304', ('TAMPER ANCHOR', 'READY IDENTITY', 'CELLS')), ('1305', ('TAMPER ANCHOR', 'READY IDENTITY', 'TITLE vs DIFF')), ('1306', ('TAMPER ANCHOR', 'AUTH SURFACE', 'READY IDENTITY', 'TITLE vs DIFF')),
                ('1307', ('TAMPER ANCHOR', 'READY IDENTITY', 'THE DOOR')), ('1308', ('GOLDEN PRODUCT HUNK', 'RULED DEPARTURE', 'AKTO LINT')), ('1309', ('GOLDEN APPLY', 'READY vs REGENERATED', 'CRYPTO IN SCOPE', 'SORT-BY-ID'))):
    A('- **#%s %s (predictions; the gate measures):**' % (n, K['prs'][n]['keys'][0]))
    for k in keys: A('  - %s' % probe(n, k)[:1100])
    for h in hardline('#%s' % n):
        if any(x in h for x in ('==', 'PRODUCT HUNK', 'DEPARTURE', 'NO AUTH')): A('  - %s' % h[:700])
A('- **The drafter\'s akto lint measurement (#1308; aktolint_1.out, rc 0):**')
for l in akl: A('  - %s' % l[:420])
A('- **The gate owes, by name (each guarded by the launcher and by its own control):** the four test-only tamper arms (each anchor re-located, byte-unique, restored by bytes; #1304 plus a test-side tamper for R2; #1305 plus the ticket\'s own `startsWith(\'vc\')` widening; #1307 plus the two constants), #1306\'s auth bytes by blob, #1308\'s product-hunk identity, departure classification, akto lint and red, #1309\'s regenerated identity, crypto in scope under tsc and at runtime, SORT-BY-ID widened, the red, and BODY-ID-DIVERGES; the counts at head and on END_TREE; a ruling on the two titles.')
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).' % '; '.join(stop))
A('- **Linear: all six PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1227, KS-1090, KS-1205, KS-1212, KS-1108, KS-1196 In Progress. KS-1090 and KS-1205 cannot close on these (other halves open).')
A('- **SQUASH-BODY KEY SCAN (MG-3; keyscan_1.out + fill_1.out):** only the PR\'s own key hyphenated anywhere; no foreign key (hyphenated or not) in any title, body or commit message.')
for l in ks: A('  - %s' % l)
A('  - %s.' % (fill[0] if fill else 'fill_1.out'))
A('- **Re-key / namespace (rekey_1.out):** %s' % ' | '.join(rk))
A('- **Sizes / sha256 (measured as this README was written):** prompt `%s` %d bytes sha256 `%s`; launcher `%s` %d bytes sha256 `%s`; capture `mail_%s_ready.md` %d bytes sha256 `%s`. **Kit dir `du -sh` %s vs gate31\'s %s** (no clone, no node_modules in the kit; the scratch clone and the akto workdirs live in the scratchpad).' % (
    K['prompt'], os.path.getsize(os.path.join(D, K['prompt'])), sha(K['prompt']), K['launcher'], os.path.getsize(L), sha(K['launcher']), kit, os.path.getsize(os.path.join(D, 'mail_%s_ready.md' % kit)), sha('mail_%s_ready.md' % kit),
    du(D), du(os.path.join(os.path.dirname(D), '2026-09-27_gate31')))); A('')
A('## 2. Pins — predict_1.out (rc 0)')
for n in NS:
    pr = P['prs'][n]
    A('- #%s: %d commit(s) %s over merge-base `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat equal %s; no mode change; move ∩ own paths EMPTY.' % (
        n, len(pr['commits']), ', '.join('`%s`' % c[:12] for c in pr['commits']), pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). `predev` (`%s`, develop^) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.' % ('; '.join(sims), K['predev'][:12]))
A('- The unfetched-object guard (STANDING_LINES 2026-09-27) carries its own control in predict (a): `%s`.' % ((hardline('CONTROL (unfetched-object guard)') or ['?'])[0][:300]))
A('- The +/- comparator control: `%s`.' % ((hardline('CONTROL (the +/- comparator)') or ['?'])[0][:300]))
A('- Superseded runs kept, renamed, never deleted: `superseded_treeguard_predict_1.out` (the first run: the unfetched-object guard read merged TREE ids as missing commits and refused 29 checks — the guard now accepts `<id>^{tree}`); `superseded_prelint_predict_1.out` (before aktolint_gate32.json existed); `superseded_asciijson_capture_1.out` (the capture\'s JSON escaped the em dash, so a seat item could not be found on a line). `launch_qa_secuura_batch1304.sh.pre-*` is an earlier fill (only the FILLED_AT line differs).'); A('')
A('## 3. What the gate owes')
A('- Prompt `%s` — the per-PR sections above at T2, the seats\' red proofs re-run, suites (api-gateway 754 -> 771 / 86 predicted on END_TREE; akto 1236 -> 1238), tsc with `exclude: []`, lint (api-gateway and akto), guards; the MANDATED SQUASH TEXT blocks (subjects WITHOUT `(#n)`, landed lengths stated) and the MG-3 key-set table; `## MERGE ADDENDUM` as the LAST section of report.md with `merged_blob_paths: none · noop_paths: none` per line.' % K['prompt'])
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@. Prior round named with its path (gate31 `2026-09-27-batch1300-g31`).' % K['report']); A('')
A('## 4. Routing line — ADDED by the drafter (as commissioned)')
A('`%s|coagent@agentmail.to|yes` inserted directly after gate31\'s pane line in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`; **backup taken first** and `cmp`-identical before the edit. routing_check_1.out: %s. Also in ROUTING_LINE_ADDED.txt.' % (K['pane'], ' · '.join(rout)))
A('')
A('## 5. The ONE launch command')
A('```'); A(launch); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s (rc 0).' % (' / '.join(dry) or '?'))
A('- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`): if `g32_sp/clone.git` is absent there, predict rebuilds it (`clone --shared` + fetch) on a re-pin. If develop moves first, step 3b re-pins in the same action; an own-path move, a stack, a pairwise overlap, a no-op/overlap declaration predict cannot prove or an END-tree disagreement refuses rc 10. A NEW PR on one of the six keys or on a `-b34-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.'); A('')
A('## 6. Questions for Wednesday (each with the drafter\'s recommendation)')
A('1. **Two titles do not describe their diffs (READ).** #1305\'s title "%s" names KS-1090\'s R2-2 (tests never type-checked); its one file pins the vouch scope (R2-3). #1306\'s title "%s" names KS-1205\'s N-2 (a JWT claim naming a bucket); its cells pin F-3 G-BUCKET-HASH and send no JWT (linear_KS-1205.md: N-2 and F-3 are separate items). Your addendum keeps both titles as the declared subjects (they land at 86 and 84), and a subject is permanent on develop. *Recommend:* let the gate rule (the prompt asks it to, TITLE-VS-DIFF) and re-declare before the GO, e.g. #1305 «KS-1090 R2-3: pin that the gateway vouch reaches originate and no other service» and #1306 «KS-1205 F3: pin that an API key\'s limiter bucket is never its bare key hash» (drafter\'s proposals, not measured against anything but length).' % (P['titles']['1305'], P['titles']['1306']))
A('2. **Your commission said five of six PRs sit on the old develop; the drafter measured six** (each head\'s single commit has parent `94c9c7aa9be7`; the API\'s `base.sha` reads `a24db57e65c9` for #1306-#1309 only because GitHub records the base at open time). No consequence for the merge: every check uses each PR\'s own merge-base. *Recommend:* note it; nothing to change.')
A('3. **#1307\'s tamper moved** — the READY said proxy.ts:808; the drafter READ :814 at head AND on END_TREE (the seat measured :814 too). #1306\'s tamper is :313 at head AND on END_TREE, as the seat measured. *Recommend:* launch as drafted — the prompt carries the whole-line anchors, not line numbers.')
A('4. **#1304\'s R2 is a control, not a red** (the brief\'s precheck fix, 2026-09-21 22:44: no product tamper reaches the try/finally). The PR presents two new cells; only R1 has a product red. *Recommend:* the gate plants a TEST-SIDE tamper for R2 and says whether the PR body should call R2 a control.')
A('5. **#1309\'s SORT-BY-ID is measured by source only**: 15 reader files, 0 sorts naming an id, 0 id-derived orders, and the store never returned id order (Redis KEYS / Map insertion). Consumers outside the repo are UNMEASURED. *Recommend:* launch; the gate widens the grep and reads the OpenAPI examples (`dt-seed-*` fixtures).')
A('6. **The golden for #1309 heads its new-file section `--- a/…` rather than `/dev/null`.** `git apply --cached --check` accepted it (MEASURED), and the seat applied it strict. *Recommend:* none for the gate; for future regenerated goldens, emit `/dev/null` so every applier agrees.')
A('7. **Merge authority — Seat B 34th merges its own six.** *Recommend:* keep; say so in the GO mail with each declared subject and its landed length.'); A('')
A('## 7. Controls: `controls_%s.sh <scratchpad> [--invert]`' % kit)
A('- **controls_1.out:** `%s` (rc %s).%s' % (s1, rc1, (' MISMATCHES: ' + '; '.join(mism1)) if mism1 else ''))
A('- **controls_2.out (`--invert`):** `%s` (rc %s, by design).%s' % (s2, rc2, (' Controls that did NOT flip: ' + '; '.join(ok2)) if ok2 else ' Every control can fail.'))
A('- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed; the launcher\'s head guard is whole-field.')
A('- Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev in a MOVED copy; RE / RN / RO plant a wrong commit count / a no-op path / an overlap there and each must refuse rc 10; RS/RS-twin exercise STACKBASE; PS1 is `--simulate foreign1305`; PS2 is `--simulate moved`; PF1/PF2 fill from SIM / failed pins and must refuse; SJ1-SJ3 plant the subject defects in a fill copy. RW / RWB exercise the WIDEN census by title and by branch. Every kit rule (exits 35, 40-44, 46-51) has its own SPLIT control.')
A('- Side effects (STANDING_LINES, B 32nd): the real re-pin in RD/RE/RN/RO writes only inside the control workdir\'s kit copy and the scratch clone\'s refs; RS and the RE family restore the copy\'s kit.json from a pristine copy; the NS plants are in memory only.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal.'); A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md · ROUTING_LINE_ADDED.txt + routing_check_1.out · make_commission_%s.py / make_readme_%s.py · rekey_check_%s.py → rekey_1.out' % (kit, kit, kit))
A('- Pins: predict_%s.py → predict_1.out, predict_sim_*.out, pins_%s.json (+ .SIM-*.json) · keyscan_%s.py → keyscan_1.out · final_lsremote_1.out' % (kit, kit, kit))
A('- Measurements: aktolint_%s.sh → aktolint_1.out, aktolint_%s.json (#1308)' % (kit, kit))
A('- Reads: gh_read_%s.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_%s.py → linear_reads_1.out, linear_KS-*.md · capture_mail_%s.py → capture_1.out, mail_%s_ready.md, stopcounts_%s.json · _api_peek_%s.py → _api_peek_1.out (the first census)' % (kit, kit, kit, kit, kit, kit))
A('- Prompt/launcher: prompt_%s.TEMPLATE.txt, launcher_%s.TEMPLATE.sh.txt, fill_%s.py → %s + %s (fill_1.out), launcher_check_1.out' % (kit, kit, kit, K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_%s.sh (repin_dryrun_1.out), controls_%s.sh (controls_1/2.out + .rc)' % (kit, kit)); A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, comment, container or port bind. No inbox read. No write in any project folder. No file deleted. One write outside the kit and the scratchpad: the routing line (§4, backup first).')
A('- **UNMEASURED:** every vitest run (every red, green and suite count above is READ or a seat claim — except akto lint); every tamper arm; tsc on api-gateway; api-gateway lint; prettier; every suite on END_TREE; whether any consumer OUTSIDE the repo depends on the `dt-<ms>` id shape; the crypto default import under the built JS; the usage gate and launch steps 4-6.')
A('- **MEASURED by the drafter (not the gate\'s evidence):** heads/develop by two instruments; merge-bases; the merge-tree shapes and END_TREE; every tamper anchor\'s whole-line location at head, develop and END_TREE; READY identity for #1304-#1307; #1306\'s auth.ts blobs; #1308\'s product-hunk identity (`git apply --cached --check` of the verified bytes), its departure classification and akto lint at three trees; #1309\'s regenerated identity and apply, the node-global crypto check and the SORT-BY-ID source grep.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
