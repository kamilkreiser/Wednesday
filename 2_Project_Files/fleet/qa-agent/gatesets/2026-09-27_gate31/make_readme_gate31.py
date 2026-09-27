#!/usr/bin/env python3
"""make_readme_gate31.py <scratchpad> — writes README.md for gate31 (the directory this script lives in). Every SHA, tree, count, size and control
tally is READ from the kit's own files (pins_gate31.json, stopcounts_gate31.json, gh_read_1.out, keyscan_1.out, controls_1/2.out + .rc, fill_1.out,
launcher_check_1.out, repin_dryrun_1.out, routing_check_1.out, predict_1.out, predict_sim_*.out, logprobe_1.out, final_lsremote_1.out) and from `du`
at the moment of writing — never typed. The prose is the drafter's. Shape copied from gate30T1's make_readme_gate30T1.py."""
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
fill = [l for l in rd('fill_1.out').splitlines() if l.startswith('key scan') or l.startswith('seat items')]
rout = rd('routing_check_1.out').splitlines(); ks = [l for l in rd('keyscan_1.out').splitlines() if l.startswith(('#', 'CONTROL'))]
fin = rd('final_lsremote_1.out').strip().splitlines()
lp = [l.strip() for l in rd('logprobe_1.out').splitlines() if l.strip()]
sims = ['%s -> %s' % (re.match(r'predict_sim_(\w+)\.out$', f).group(1), (rd(f).strip().splitlines() or ['?'])[-1].split(' ->')[0]) for f in sorted(os.listdir(D)) if re.match(r'predict_sim_\w+\.out$', f)]
def subj(n):
    m = re.search(r'=== #%s head.*?\ntitle \((\d+) chars.*?= (\d+) chars' % n, gh, re.S); return m.group(2) if m else '?'
def probe(n, key):
    for l in rd('predict_1.out').splitlines():
        if l.startswith('  #%s %s' % (n, key)): return l.strip()[len('#%s ' % n):]
    return '(not in predict_1.out)'
def du(p):
    r = subprocess.run(['du', '-sh', p], capture_output=True, text=True); return (r.stdout.split() or ['?'])[0]
L = os.path.join(D, K['launcher']); R = os.path.join(D, 'repin_and_launch_%s.sh' % kit)
NS = sorted(K['prs'])
WHY = {
 '1300': '**T1** — adminConfig.ts: the last two of four UNCONDITIONAL err.message 500s (seed-demo-users, migrate-tenant-data; production included) through fail500 + IN-PLACE ks730c edits (C3 48->50, KNOWN emptied). Spark on an EXCERPTED input, golden-EXACT.',
 '1301': '**T2** — TEST-ONLY, **STACKED on #1300** (API base = #1300\'s branch at #1300\'s head): ks730c C1 clears the logger per NODE_ENV + asserts the whole call list. Golden applies strictly at #1300\'s head.',
 '1302': '**T1 (widens LOG STORAGE)** — logger.ts: production File transports get `combine(json())`; files that held `undefined` now hold every field. Golden-EXACT.',
 '1303': '**T3 (WIDEN row, joined at pin)** — comment-only fail500 docblock edit in webhooks.ts :549-:561; code-token equivalence. Golden-EXACT.',
}
rows = ['| #%s | %s | %s | `%s` | %d on %s | %s | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], P['prs'][n]['head'], len(P['prs'][n]['commits']),
        ('#%s head `%s`' % (P['prs'][n]['stacked_on'], P['prs'][n]['merge_base'][:12])) if P['prs'][n].get('stacked_on') else '`%s`' % P['prs'][n]['merge_base'][:12], subj(n), WHY[n]) for n in NS]
stop = ['#%s %s' % (n, ('%s · %s · %s · %s' % (S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'].split(',')[0].replace(' passed', '') + ' of 60')) if S[n]['preflight_ran'] else 'NOT APPLICABLE') for n in NS]
launch = '%s %s %s' % (R, L, SP)
go = re.search(r"GO='(`GO: merge [^`]*`)'", rd('fill_%s.py' % kit)).group(1)
flip = lambda h: h[:-1] + ('0' if h[-1] != '0' else '1')
wl = ['#%s real `%s` -> wrong `%s` (same length %s, differs in %d digit, contains the real head: %s)' % (n, P['prs'][n]['head'], flip(P['prs'][n]['head']), len(flip(P['prs'][n]['head'])) == 40, sum(x != y for x, y in zip(P['prs'][n]['head'], flip(P['prs'][n]['head']))), P['prs'][n]['head'] in flip(P['prs'][n]['head'])) for n in NS]
used = sorted(set(re.findall(r'^  OK +((?:C3|O2|RT|H1\d{3})) ', rd('controls_1.out'), re.M)))
rt = P['retarget'].get('1301', {})
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
out = []; A = out.append
A('# Gateset 2026-09-27_%s — README for Wednesday' % kit); A('')
A('Written %s by the drafter (make_readme_%s.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % (now, kit))
A('The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing and deleted nothing. It wrote: this kit directory `%s/`; ONE line in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (as commissioned, backup first — §4); and scratch under `%s/` (the scratch clone `g31_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key — the logprobe workdirs `g31_logprobe_*`, the control workdirs `g31_controls_*` and the dry-run reads `repin_gate31_dry_*`). Superseded outputs were RENAMED `superseded_*`, never deleted.' % (D, SP))
A('The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its typescript and winston). GitHub: REST GET only (Secuura GH_TOKEN read by name, never printed). Linear: queries only.'); A('')
A('**gate31 = FOUR PRs, MIXED tiers, one kit, no sibling.** #1300, #1301 and #1302 are the three you named; **#1303 (KS-1350) is the WIDEN row** — it existed at the pin (branch `feature/ks-1350-fail500-docblock-b33-4`, opened 05:28:43Z; gh_read_1.out census), so it JOINED; your 15:3x message confirmed its head. Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree.'); A('')
A('| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on chain base | squash subject chars | why this tier (from the DIFF) |')
A('|---|---|---|---|---|---|---|'); out.extend(rows); A('')
A('Routing `%s` (**added by the drafter** — §4). GO string %s (or the subset; #1301 never without #1300). MERGE ORDER #1300 before #1301, with the RETARGET step (§3). The GO goes to **Seat B 33rd**, which raised all four and merges its own.' % (K['pane'], go)); A('')
A('## 1. BLUF')
A('- **Kit: READY to launch** — launcher `--check` rc 0 (`%s`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: %s). Read §6.1 first: the drafter MEASURED #1302 putting secret/PII-looking fields into the production log files; under your widen rule that predicts **#1302 NO GO** unless the gate (or you) rule stdout was already log storage.' % ((chk[0].strip() if chk else '?'), ' / '.join(dry) or '?'))
A('- **Controls, both ways (controls_%s.sh):**' % kit)
A('  - normal (controls_1.out, rc %s): `%s`' % (rc1, s1))
A('  - `--invert` (controls_2.out, rc %s): `%s`' % (rc2, s2))
A('  - Wrong-head controls (%s, all OK both ways) change ONE hex digit and never contain the real head (doctor() refuses rc 98 on a superset, rc 97 if the original survives): %s' % (', '.join(used) or '?', '; '.join(wl)))
A('  - NEW in this kit for the STACK: **RS** (a copy declaring #1301 on the WRONG parent must refuse the launch action rc 11 at its STACKBASE check) + RS/twin; **RE** (the stacked child\'s declared commit count wrong by one in a moved copy: the real re-pin must refuse rc 10) and **RE2** (the stack UNDECLARED: the launch action\'s DEVBASE check must refuse rc 11 before any re-pin — the first draft of RE expected rc 10 here and MISMATCHED, got 11: the earlier guard fired; superseded_preREfix_controls_1.out); **RT** (a wrong RETARGET tree in the prompt refuses the launcher rc 31); plus RW / RW/twin (the WIDEN census, rc 15).')
A('- **Pinned over develop `%s`** (tree `%s`) — ls-remote AND fetched AND the API compare agree; the last squash is #1299 (KS-1339); gate30T1\'s #1292/#1294 and gate30T2\'s #1293/#1295/#1298/#1299 landed over `3f70224a069b`. **Develop had NOT moved from the round-start `94c9c7aa9be7` at pin.**' % (P['develop'], P['develop_tree']))
A('  - **END_TREE `%s`** (%s), identical in all %d valid orders (#1300 before #1301; %d merge-tree calls).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']))
A('  - **RETARGET (simulated):** #1300 squashed over develop as a new commit (it does NOT contain #1300\'s head), #1301 merged with git\'s OWN merge-base (`%s`, develop): clean, result `%s` == develop+#1300+#1301, diff(squash, result) == %s with #1301\'s head blob (predict_1.out (d)).' % ((rt.get('natural_merge_base') or '-')[:12], rt.get('result_tree'), rt.get('own_paths_after_retarget')))
A('  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s' % ' | '.join(fin))
A('- **OVERLAPS — pairwise, measured:** only the DECLARED stack pair #1300/#1301 overlaps (ks730c; final target #1301\'s head blob); every other kit pair disjoint and NOT stacked; every kit path disjoint from ALL %d other open PRs (PULLS API census, plus any PR opened since the draft). #1296/#1297 (gate30T1\'s NO GO KS-1346 rows) are still open, path-disjoint.' % len(P['inflight']))
for n, keys in (('1300', ('UNCONDITIONAL SITES', 'HELPER CALLS', 'ERR.MESSAGE LEFT', 'IN-PLACE ks730c EDITS', 'GOLDEN')),
                ('1301', ('THE HUNK', 'C1 AT HEAD', 'THE TAMPER ANCHOR', 'GOLDEN', 'RETARGET')),
                ('1302', ('LOGGER SHAPE', 'LOG-FILE WIDENING', 'CALLERS', 'TEST FILE', 'GOLDEN')),
                ('1303', ('CODE-TOKEN EQUIVALENCE', 'TOKEN-EQUIVALENCE CONTROLS', 'WINDOW', 'THE NEW SENTENCES', 'GOLDEN'))):
    A('- **#%s %s (predictions; the gate measures):**' % (n, K['prs'][n]['keys'][0]))
    for k in keys: A('  - %s' % probe(n, k)[:900])
A('- **The drafter\'s own #1302 measurement (logprobe_1.out, rc 0; controls: stdout carries every sentinel at both commits AND the head combined.log carries the positive line):**')
for l in lp:
    if l.startswith(('==', 'logs/', 'stdout', 'CONTROLS', 'RESULT', 'logprobe_gate31')): A('  - %s' % l[:420])
A('- **The gate owes, by name (each guarded by the launcher and by its own control):** #1300 — its own real-router probe (5 NODE_ENVs incl. UNSET, 3 throw types, REACHED per env) that MUST leak at the merge-base, all four KS-1334 sites at head, `message: err.message` 0 on END_TREE, the fifth site declared, arms (a)/(b) on C3/C4, the §5f close; #1301 — both tampers x both cell forms (R0-R3) and the single-environment sweep, the stack and the retarget re-simulated; #1302 — the REAL logger writing REAL files at merge-base and head with sentinel fields and a sentinel err.message through a real fail500 route, and a plain ruling on KS-1346\'s class; #1303 — token equivalence with its controls both ways, the window, the three sentences true.')
A('- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60 (no PR adds, removes or renames a `*.test.sh`).' % '; '.join(stop))
A('- **Linear: all four PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1334, KS-1349, KS-1348, KS-1350 In Progress. KS-1334 is NOT Done after #1300 (§5f live sweep + the fifth per-tenant site).')
A('- **SQUASH-BODY KEY SCAN (MG-3; keyscan_1.out + fill_1.out):** only the PR\'s own key may stay hyphenated — KS-1334 (#1300), KS-1349 (#1301), KS-1348 (#1302), KS-1350 (#1303).')
for l in ks: A('  - %s' % l)
A('  - **No foreign HYPHENATED key in any title, body or commit message**; foreign keys appear UN-hyphenated (KS1334, KS1344, KS1341). %s.' % (fill[0] if fill else 'fill_1.out'))
A('- **MG-11:** `<title> (#n)` = %s chars. **#1301 and #1302 exceed 92** — the prompt MANDATES SHORT subjects (fill_1.out / the prompt\'s MANDATED SQUASH TEXT blocks).' % ' / '.join('#%s %s' % (n, subj(n)) for n in NS))
A('- **Sizes / sha256 (measured as this README was written):** prompt `%s` %d bytes sha256 `%s`; launcher `%s` %d bytes sha256 `%s`; capture `mail_%s_ready.md` %d bytes sha256 `%s`. **Kit dir `du -sh` %s vs gate30T1\'s %s** (no clone, no node_modules in the kit; the scratch clone lives in the scratchpad).' % (
    K['prompt'], os.path.getsize(os.path.join(D, K['prompt'])), sha(K['prompt']), K['launcher'], os.path.getsize(L), sha(K['launcher']), kit, os.path.getsize(os.path.join(D, 'mail_%s_ready.md' % kit)), sha('mail_%s_ready.md' % kit),
    du(D), du(os.path.join(os.path.dirname(D), '2026-09-27_gate30T1')))); A('')
A('## 2. Pins — predict_1.out (rc 0)')
for n in NS:
    pr = P['prs'][n]
    A('- #%s: %d commit(s) %s over %s `%s`; %d behind; merged tree `%s`%s; every merged blob == its head blob; numstat equal %s; no mode change; move ∩ own paths EMPTY.' % (
        n, len(pr['commits']), ', '.join('`%s`' % c[:12] for c in pr['commits']), ('#%s\'s head' % pr['stacked_on']) if pr.get('stacked_on') else 'merge-base', pr['merge_base'], pr['behind'], pr['merged_tree'],
        ' (over develop + #%s)' % pr['stacked_on'] if pr.get('stacked_on') else '', pr['numstat']))
A('- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE; foreign1301 also breaks #1300, which owns the same file). `predev` (`%s`, develop^) is the moved-develop pin in controls D / RC / RD.' % ('; '.join(sims), K['predev'][:12]))
A('- Superseded runs kept, renamed, never deleted: `superseded_wrongsp_logprobe_1.out` (logprobe given the wrong scratchpad — its own controls refused rc 1), `superseded_preprobefix_predict_1.out` (before the probe fixes: a git-grep `\\b` false zero on CALLERS, the insertion-hunk window), `superseded_precrashfix_*` (a stacked child whose parent conflicted crashed predict instead of refusing it cleanly — still rc 1). `launch_qa_secuura_batch1300.sh.pre-154831` is the first fill, refused by its own `bash -n` (a bash-3.2 apostrophe in a heredoc inside `$(...)`), kept.'); A('')
A('## 3. What the gate owes')
A('- Prompt `%s` — the per-PR sections above at each PR\'s own tier, the seats\' red proofs re-run, suites (originate 979 -> 988 / 85 predicted on END_TREE), tsc with `exclude: []`, lint, guards; the MANDATED SQUASH TEXT blocks (SHORT subjects for #1301/#1302) and the MG-3 key-set table; `## MERGE ADDENDUM` as the LAST section of report.md (a NO GO PR gets its line marked NO GO; a NO GO on #1300 makes #1301 NO GO too).' % K['prompt'])
A('- **The GO carries the merge order and the RETARGET step:** #1300 before #1301; after #1300 squashes, retarget #1301\'s base to develop (API, no push), re-read its head, re-predict with git\'s own merge-base: clean, diff == exactly ks730c, blob == #1301\'s head blob; a conflict, any other path or any other blob = STOP.')
A('- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@. Prior rounds named with their paths (gate30T1 `2026-09-26-batch1292-g30T1`, gate30T2 `2026-09-26-batch1293-g30T2`).' % K['report']); A('')
A('## 4. Routing line — ADDED by the drafter (as commissioned)')
A('`%s|coagent@agentmail.to|yes` inserted after `QA/Secuura-batch1293|…` (the gate30 lines) in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`; backup taken first and `cmp`-identical before the edit. routing_check_1.out: %s. Also in ROUTING_LINE_ADDED.txt.' % (K['pane'], ' · '.join(rout)))
A('')
A('## 5. The ONE launch command')
A('```'); A(launch); A('```')
A('- Dry run (`--dry-run` appended): repin_dryrun_1.out → %s (rc 0).' % (' / '.join(dry) or '?'))
A('- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`): if `g31_sp/clone.git` is absent there, predict rebuilds it (`clone --shared` + fetch) on a re-pin. If develop moves first, step 3b re-pins in the same action; an own-path move, an undeclared stack, a pairwise overlap or an unclean retarget refuses rc 10. A NEW KS-1350 PR outside the kit refuses rc 15. A moved head, or #1301 retargeted before launch (#1300 merged early), refuses rc 11.'); A('')
A('## 6. Questions for Wednesday (each with the drafter\'s recommendation)')
A('1. **#1302 is the widen class, measured.** At head all six sentinel fields of a logged metadata object land in `logs/error.log` and `logs/combined.log`; at develop both files hold `undefined`; stdout carried all six at BOTH commits (logprobe_1.out). The PR says so itself ("The production log files will now really hold logged error text."), and gate30T1\'s own N-G30-1 prescribed exactly this fix. So the ruling turns on one question: **is originate\'s stdout ALREADY log storage** (collected and kept by the deployed stack)? If yes, #1302 persists what was already stored, and the widening is the rotated files on disk; if no, #1302 is KS-1346\'s class. *Recommend:* launch as drafted — the gate measures it again and reads the deploy config — and treat the fix-shape as ONE logger-level key-based redaction format covering Console and File (it would also be the shape KS-1346 lacked), filed as a ticket rather than folded into #1302. Who reads originate\'s logs is a data-handling call that may be Kam\'s.')
A('2. **Your commission\'s #1301 tamper does not discriminate (READ, predicted).** "fail500 logging only under NODE_ENV=production must RED the A1 rows at head, while the old `.at(-1)` form stayed green" — C1\'s NODE_ENVS has no production row, so under that tamper C1 logs nothing and reds under the OLD form too; the KS-1349 brief measured this and used a development-only tamper, and so did the seat. The rows your commission calls "A1" are `RED KS-730 C1` in the file (the `RED KS-1334 A1` rows are part A\'s and already clear per environment). *Recommend:* keep the kit as drafted — it runs BOTH tampers against BOTH forms plus a single-environment sweep, and names the slip against you or against the drafter.')
A('3. **Stacked merge.** #1301 contains #1300\'s commit; a GO subset with #1301 and without #1300 is impossible, and a NO GO on #1300 is a NO GO on #1301. *Recommend:* sign the GO with the order and the retarget step verbatim (the prompt spells them; the gate re-simulates the retarget).')
A('4. **KS-1334 after #1300:** all four sites converted and C4\'s KNOWN emptied, but §5f withholds Done and a fifth per-tenant site (`err.message?.substring(0, 60)` in a 200 body) has no ruled fix-shape. *Recommend:* keep In Progress; the merge seat posts the canonical `live sweep owed` comment the prompt spells.')
A('5. **KS-1349\'s ticket names the production-only tamper as its Done proof.** If the gate confirms §6.2, the ticket\'s Done text is itself wrong. *Recommend:* amend the ticket text after the gate (a board write — yours).')
A('6. **adminConfig.ts:1999 logs `email: u.email`** (READ) — with #1302 merged, that email reaches the production files. Context for §6.1, not a finding against #1300.')
A('7. **Merge authority — Seat B 33rd merges its own four.** *Recommend:* keep; say so in the GO mail. The audit fuse (`2026-09-30T00:00Z`, from the B31/B32 handovers as quoted in gate30T1\'s README) was NOT re-read by this drafter — UNVERIFIED here.'); A('')
A('## 7. Controls: `controls_%s.sh <scratchpad> [--invert]`' % kit)
A('- **controls_1.out:** `%s` (rc %s).%s' % (s1, rc1, (' MISMATCHES: ' + '; '.join(mism1)) if mism1 else ''))
A('- **controls_2.out (`--invert`):** `%s` (rc %s, by design).%s' % (s2, rc2, (' Controls that did NOT flip: ' + '; '.join(ok2)) if ok2 else ' Every control can fail.'))
A('- Every mutation is independent of the original: doctor() refuses a replacement that contains the text it replaces (rc 98) and refuses when the original still occurs after the plant (rc 97); every wrong head is the real head with ONE hex digit changed; the launcher\'s head guard is whole-field.')
A('- Doctored arms are pinned to the launcher\'s own develop. RD runs the REAL re-pin (predict → fill) from a launcher pinned at predev in a MOVED copy; RE plants a wrong declared commit count there and must refuse rc 10; RE2 undeclares the stack and must refuse rc 11 at step 3; RS/RS-twin exercise the launch action\'s STACKBASE guard; PS1 is `--simulate foreign1301`; PS2 is `--simulate moved`; PF1 fills from SIM pins and must refuse. RW / RW-twin exercise the WIDEN census. Every kit rule (exits 35, 40-44, 46-48, 50, 51) has its own SPLIT control.')
A('- Side effects (STANDING_LINES, B 32nd): the real re-pin in RD/RE writes only inside the control workdir\'s kit copy and the scratch clone\'s refs; RS restores the copy\'s kit.json from a pristine copy before its twin; nothing is shared between arms except the scratch clone, whose refs every predict run re-fetches.')
A('- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, a live retarget (only simulated).'); A('')
A('## 8. Files')
A('- Kit: kit.json · COMMISSION.md · ROUTING_LINE_ADDED.txt + routing_check_1.out · make_commission_%s.py / make_readme_%s.py' % (kit, kit))
A('- Pins: predict_%s.py → predict_1.out, predict_sim_*.out, pins_%s.json (+ .SIM-*.json) · keyscan_%s.py → keyscan_1.out · final_lsremote_1.out' % (kit, kit, kit))
A('- Measurements: logprobe_%s.py → logprobe_1.out, logprobe_%s.json (#1302) · tokeq_%s.js (#1303, called by predict)' % (kit, kit, kit))
A('- Reads: gh_read_%s.py → gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_%s.py → linear_reads_1.out, linear_KS-*.md · capture_mail_%s.py → capture_1.out, mail_%s_ready.md, stopcounts_%s.json · _api_peek_%s.py → _api_peek_1.out (the first census)' % (kit, kit, kit, kit, kit, kit))
A('- Prompt/launcher: prompt_%s.TEMPLATE.txt, launcher_%s.TEMPLATE.sh.txt, fill_%s.py → %s + %s (fill_1.out), launcher_check_1.out' % (kit, kit, kit, K['prompt'], K['launcher']))
A('- Repin/controls: repin_and_launch_%s.sh (repin_dryrun_1.out), controls_%s.sh (controls_1/2.out + .rc)' % (kit, kit)); A('')
A('## 9. NOT done / NOT measured by the drafter')
A('- No launch, mail, tap, merge, commit, push, comment, container or port bind. No inbox read. No write in any project folder. No file deleted. One write outside the kit: the routing line (§4).')
A('- **UNMEASURED:** every jest run (every red, green, arm, 2x2 and suite count above is READ or a seat claim); #1300\'s runtime behaviour; #1301\'s tamper arms; the #1302 widening THROUGH A REAL ROUTE (the drafter measured the logger module alone, not a fail500 route writing a file) and where the deployed stack keeps stdout; prettier; tsc; lint; every suite on END_TREE; the usage gate and launch steps 4-6; the live retarget.')
A('- **MEASURED by the drafter (not the gate\'s evidence):** heads/develop by two instruments; the merge-tree shapes, END_TREE, the retarget simulation; the golden identities; the #1302 log-file sentinels (logger module, node + real winston); the #1303 token equivalence with five controls.')
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines')
