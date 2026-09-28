#!/usr/bin/env python3
"""make_readme_gate40.py <scratchpad> — writes README.md for gate40 (the directory this script lives in). Every figure is READ from the kit's own output
files at the moment it runs (pins_gate40.json, predict_1.out, predict_sim_*.out(.rc), pgprobe_gate40.json, fill_1.out, keyscan_1.out, rekey_1.out,
launcher_check_1.out, repin_dryrun_N.out, controls_1.out / controls_2.out (+ .rc), final_lsremote_1.out), each named beside it; the prose (doubts,
questions) is the drafter's. Shape copied from gate39's make_readme (gate38 -> gate37 lineage), re-keyed to gate40. The README ENDS with §8, the ONE
launch command; its argument 2 is the EXISTING scratchpad passed here."""
import json, os, re, glob, hashlib, datetime, sys
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
SP = sys.argv[1] if len(sys.argv) > 1 else ''
if not (SP.startswith('/private/tmp/claude-501/') and '/scratchpad' in SP and os.path.isdir(SP)): sys.exit('usage: make_readme_gate40.py <an EXISTING scratchpad dir under /private/tmp/claude-501/*/scratchpad*> (argument 2 of the launch command)')
P = json.load(open('%s/pins_%s.json' % (D, kit))); PG = json.load(open('%s/pgprobe_%s.json' % (D, kit)))
def rd(f): return open(os.path.join(D, f), encoding='utf-8').read() if os.path.exists(os.path.join(D, f)) else ''
def last(f, rx):
    m = [l for l in rd(f).splitlines() if re.search(rx, l)]; return m[-1].strip() if m else 'ABSENT'
def rc(f): return rd(f).strip() or '?'
def strip(s): return re.sub(r'^(PASS )?#1338 ', '', s)
def j(x): return json.dumps(x, ensure_ascii=False, default=str)
DRY = sorted(glob.glob(D + '/repin_dryrun_[0-9]*.out'), key=lambda f: int(re.search(r'_(\d+)\.out$', f).group(1)))
DRYF = os.path.basename(DRY[-1]) if DRY else 'repin_dryrun_1.out'
fill = rd('fill_1.out'); now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
L = os.path.join(D, K['launcher']); PR = os.path.join(D, K['prompt']); CAP = os.path.join(D, 'mail_%s_ready.md' % kit)
def sz(p): b = open(p, 'rb').read(); return '`%s` %d bytes sha256 `%s`' % (os.path.basename(p), len(b), hashlib.sha256(b).hexdigest())
SUM = PG['_summary']; R = PG['runs']
def scen(key, prefix):
    for k, v in ((R.get(key) or {}).get('scen') or {}).items():
        if k.startswith(prefix): return v
    return None
sims = {os.path.basename(f)[len('predict_sim_'):-len('.out')]: (rc(os.path.basename(f) + '.rc'), last(os.path.basename(f), r'^(PASS|REFUSED):')[:44]) for f in sorted(glob.glob(D + '/predict_sim_*.out'))}
fl = rd('final_lsremote_1.out').strip().replace('\n', ' | ')
n = '1338'; pr = P['prs'][n]
cur = pr['head'] in fl and P['develop'] in fl
CH, CD = '42f8a5abc65ef9a6bc20c07797786089f2b9cd93', '0de108577e6199de3c9402c0643a2944d86aee97'   # the values Wednesday's commission named (08:4x AEST)
launch = '%s/repin_and_launch_%s.sh %s %s' % (D, kit, L, SP)
m = re.search(r'#%s (\d+)->(\d+)' % n, fill)
row = '| #%s | %s | %s | `%s` | %d on `%s` | %s | %s -> %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12],
      ', '.join(os.path.basename(p) for p in pr['paths']), m.group(1) if m else '?', m.group(2) if m else '?')
h, b = SUM.get('head', {}), SUM.get('base', {})
out = ['# Gateset %s — README for Wednesday' % os.path.basename(D), '',
 'Written %s by the drafter (make_readme_gate40.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now,
 'The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory (TEXT files only) and scratch on the DATA volume under its session scratchpad `.../scratchpad/g40/` (the scratch clone `g40_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, fetched FROM ORIGIN with the checkout\'s repo-local key; the Postgres data dir `g40_pg/data` (kept, stopped); the git-archive extracts `g40_pg/base|head` and the four ARM copies `g40_pg/arm*`, each with a node_modules SYMLINK FARM into the checkout\'s node_modules; per-run output `g40_pg/runs/`; the control workdirs `g40_controls_*`; one aborted controls run quarantined in `_quarantine_2026-09-29/` — see §7). OUTSIDE the scratchpad it created only a short, empty unix-socket dir `/tmp/q40.*`. Nothing large was written to /Volumes/DevMASTER; every long-running output was written in the scratchpad first and copied in. It did NOT write the routing line (§4).',
 'The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its tsx, pg and installed packages through the symlink farm). Seat records and both seats\' scratchpads were READ. GitHub: REST GET only. Linear: queries only. AgentMail: ONE read-only API listing of wednesday-agent@ (GET messages — touches no seen-state; used ONLY to find the READY mail\'s id by the commissioned subject prefix) and ONE by-id read (inbox_digest.sh full); nothing sent. decisions.json and inbox_routing.conf: read only.', '',
 '**gate40 = ONE PR (T1), one kit, no sibling, NO stack, ONE merge-base (develop itself), pinned over the CURRENT develop.**', '',
 '| PR | ticket | tier | head (API == ls-remote pull/head == branch == fetched) | commits on merge-base | files | subject declared -> lands |', '|---|---|---|---|---|---|---|', row, '',
 'Routing `%s` (**NOT added by the drafter** — §4). The GO string, as the GO mail\'s SUBJECT: `GO (Seat B 42nd): merge 1338 on gate40` (launcher exit 26; kit rule 50 carries requirement 10). The PR TITLE lands at 93 (> 92): the kit mandates the declared subject `KS-1370: validate answers on the stored revoke; its usage write cannot revive one` (fill_gate40.py SHORT).' % K['pane'],
 '', '## 1. BLUF',
 '- **Kit: READY to launch once the routing line is added** — launcher `--check` (launcher_check_1.out: `%s`); repin `--dry-run` (%s: %s).' % (last('launcher_check_1.out', r'all guards pass|REFUSING'), DRYF, last(DRYF, r'DRY RUN COMPLETE|REFUSING|exit')[:200]),
 '- **Heads read at pin vs the commission:** #1338 head `%s` (commission `%s`: **%s**); develop `%s` (commission `%s`: **%s**). Re-read by `ls-remote` AND the PULLS API AND the fetch (predict_1.out), again by the dry run (%s) and a final `ls-remote` (final_lsremote_1.out): %s — every pin still current: **%s**.' % (
     pr['head'], CH, 'EQUAL' if pr['head'] == CH else 'DIFFERENT', P['develop'], CD, 'EQUAL' if P['develop'] == CD else 'DIFFERENT', DRYF, fl, cur),
 '  - Develop tree `%s`; merge-base `%s` (develop itself, move EMPTY); **END_TREE `%s`** (%s); diff(develop, END) == the 3 own paths, every END blob == the head blob (MG-1).' % (P['develop_tree'], pr['merge_base'][:12], P['end_tree'], P['end_shortstat']),
 '- **Controls, both ways (controls_gate40.sh):**',
 '  - normal (controls_1.out, rc %s): `%s`' % (rc('controls_1.rc'), last('controls_1.out', r'^SUMMARY')),
 '  - `--invert` (controls_2.out, rc %s): `%s`' % (rc('controls_2.rc'), last('controls_2.out', r'^SUMMARY')),
 '- **Simulations (predict):** %s (`moved` must PASS; `foreign<n>` must REFUSE).' % '; '.join('%s -> rc %s %s' % (k, v[0], v[1]) for k, v in sims.items()),
 '- **Pinned predict** (predict_1.out, rc %s): `%s`.' % (rc('predict_1.out.rc'), last('predict_1.out', r'^(PASS|REFUSED):')),
 '- **KS-1370 on a REAL PostgreSQL AS THE APP ROLE (MEASURED by the drafter, pgprobe_1.out — %s, unix socket only, listen_addresses \'\', `lsof -a -p <postmaster> -i` 0 lines with the native pg as the control; controls %s):**' % (PG.get('engine', '?')[:40], 'ALL PASS' if all(v is True for v in PG['controls'].values()) else j(PG['controls'])),
 '  - **Requirement 2, the premise — HOLDS for secuura_app** (provisioned by the REAL runStartupMigrations with APP_DB_PASSWORD; read back %s): %s. As the superuser the direct SELECT returns the row (%s) — the builder\'s superuser drill could not have seen the premise.' % (
     j((PG['boots'].get('head') or [{}])[-1].get('db', {}).get('secuura_app')), j(SUM.get('premise as secuura_app (head)')), j(SUM.get('premise as postgres (head)'))),
 '  - **Requirement 1, RED at base / GREEN at head (as secuura_app):** base %s | head %s (answer, row after). Controls: R1 never-revoked validates + usage 0->1 on both; R3 booted-after refuses on both (%s / %s). The superuser run gives the same R2 split (%s).' % (
     j(b.get('R2 stale instance after the stored revoke: answer / row after')), j(h.get('R2 stale instance after the stored revoke: answer / row after')), j((scen('base as secuura_app', 'R3') or {}).get('answer')), j((scen('head as secuura_app', 'R3') or {}).get('answer')),
     j([(x or {}).get('answer') for x in SUM.get("R2 as postgres (the builder's drill), base / head", [])])),
 '  - **Requirement 3, design calls + arms:** A1 cached-revoked/stored-active head %s vs armA (sticky line removed) %s; D1 vanished head %s vs armB (eviction removed) %s; **base %s — the base\'s usage upsert RE-CREATES a deleted row**; each half load-bearing: armC (half (i) reverted, half (ii) off) %s = REVIVED, armD (half (ii) off only) %s = answers valid, row stays revoked.' % (
     j(h.get('A1 cached-revoked stored-active: answer / store')), j(SUM.get('armA_nosticky', {}).get('A1 cached-revoked stored-active: answer / store')), j(h.get('D1 vanished: answer / evicted / row re-created?')),
     j(SUM.get('armB_noevict', {}).get('D1 vanished: answer / evicted / row re-created?')), j(b.get('D1 vanished: answer / evicted / row re-created?')),
     j(SUM.get('armC_revive', {}).get('R2 stale instance after the stored revoke: answer / row after')), j(SUM.get('armD_half1only', {}).get('R2 stale instance after the stored revoke: answer / row after'))),
 '  - **Requirement 4, Kam\'s split:** F1 (EXECUTE on the carve-out revoked from secuura_app) base %s, head %s; the grant restored validates again; the same fault on a cache MISS answers %s on both; M1 memory-only head %s.' % (
     j(b.get('F1 stored read fails (EXECUTE revoked): status / message')), j(h.get('F1 stored read fails (EXECUTE revoked): status / message')), j((scen('head as secuura_app', 'F2') or {}).get('answer')), j(h.get('M1 memory-only: avail / active / revoked'))),
 '  - **Requirement 5, KS-888 kept:** U1 (UPDATE revoked from secuura_app) [status, valid, error lines, lines with key, lines with hash] base %s, head %s.' % (j(b.get('U1 usage write fails: status / valid / error lines / key lines / hash lines')), j(h.get('U1 usage write fails: status / valid / error lines / key lines / hash lines'))),
 '- **Requirements 6-10 (READ by the drafter, owed by the gate):** the re-pin — %s; the cross-package census — %s; the gateway cache — %s; tier T1, round 1 of the cap; subject %s.' % (
     strip(last('predict_1.out', r"#1334's RE-PIN"))[:260], strip(last('predict_1.out', r'CROSS-PACKAGE CENSUS')).split(' — ')[-1], strip(last('predict_1.out', r'GATEWAY REFUSAL CACHE'))[:230], strip(last('keyscan_1.out', r'MANDATED squash text'))[:200]),
 '- **Linear:** %s. **Key scan:** title / body / commit carry only KS-1370 (keyscan_1.out). **Kam\'s cards (decisions.json, READ):** %s.' % (last('linear_reads_1.out', r'^#1338 attachmentsForURL')[:160], strip(last('predict_1.out', r"Kam's cards"))[:400]),
 '- **Re-key / namespace (rekey_1.out, gate39\'s AND gate38\'s namespaces):** %s' % last('rekey_1.out', r'^RESULT'),
 '- **Sizes / sha256:** %s; %s; %s.' % (sz(PR), sz(L), sz(CAP)), '',
 '## 2. Doubts and contradictions the drafter found (each READ or MEASURED as stated)',
 '1. **The PR title lands at 93 (READ, gh_read_1.out)** — over MG-11\'s 92. The kit mandates a declared subject landing at 89 (`;` for `, and`); fill REFUSES the title (control SJ4). The merger must use the declared subject.',
 '2. **The PR body\'s bound is a slip candidate (READ):** "at most once per key per 30 s, not once per request" — the gateway caches a VALID answer for **60 s** (auth.ts :247) and a refusal for 30 s (:229 / :235), per gateway replica; auth\'s connector-token route (`services/auth/src/routes/internal.ts` :43) also calls /api/keys/validate on every exchange (and answers 502 on a non-2xx), unbounded by the gateway cache.',
 '3. **A deleted key is RESURRECTED at the base (MEASURED, D1 base):** the stale instance answers valid AND its usage upsert re-inserts the deleted row (is_active true). The seat calls the vanished-row branch "a defensive path, not a live one"; the head closes the resurrection too. Pre-existing; a record item, not this PR\'s defect.',
 '4. **Where secuura_app\'s EXECUTE on the carve-out comes from (MEASURED + READ):** on a gateway-provisioned database the role is created AFTER 039, so 039\'s own GRANT (:285) is skipped and EXECUTE comes from the gateway\'s `GRANT EXECUTE ON ALL FUNCTIONS` (startup-migrations.ts :941); on the compose path docker/init creates the role first. A database whose role lacks that EXECUTE now answers **503 for EVERY cached key** (MEASURED with the grant revoked) where the base answered valid — a deploy-state question for the §5f sweep, not visible offline.',
 '5. **A silent zero-row usage UPDATE (READ):** dbRecordApiKeyUsage never reads rowCount; an UPDATE the tenant_isolation policy filters to zero rows does not throw. The drafter measured usage 0 -> 1 as secuura_app, so the GUC pin works on this path; no cell pins it.',
 '6. **Cache-miss vs cache-hit asymmetry under a DB fault (MEASURED, F2):** a hit answers 503 (new); a miss answers valid:false `Key not found` (unchanged). Both refuse; the gateway caches both 30 s. The gate rules whether that fits Kam\'s wording.',
 '7. **The re-pin (READ):** of the seat\'s 5 declarations / 7 cases, only V1 (x3) and V3 carry text edits (`state.inserts` -> `state.usageWrites`); R2, C3 and V2 went green through the mock alone (a hash-keyed store the INSERT fills). The gate owes the red set (base file against head product) and a plant on V1 / V3.',
 '8. **The 503 is declared (READ):** security.openapi.ts registers 503 for POST /api/security/keys/validate (:874), so the new response code is not spec drift; legs 3/4/8 still NOT run.',
 '9. **Two module instances, not two OS processes** — the seat\'s limit, and the drafter\'s too. The revoke was a row UPDATE as the superuser (setup), not the revoke route.',
 '10. **The checkout\'s built `@secuura/shared` dist is from 2026-09-11** (READ, ls -la) and is NOT the develop tree: the drafter resolved @secuura/shared to each side\'s own `packages/shared/src/index.ts` through a shim and the tsx hook. The gate builds shared in its worktrees.',
 '11. **GitHub mergeable_state `unstable`** (gh_read_1.out) — mergeable True; not measured further (the seat: Actions retired, no claim either way).',
 '12. **The seat\'s handover says the tree at 0de10857 == gate39\'s END `b5362672…`** — MEASURED equal (develop tree `%s`).' % P['develop_tree'], '',
 '## 3. Pins and what the gate owes',
 '- Prompt `%s` — the TEN requirements BY NAME as kit rules 40-44 / 46-50 (the launcher refuses a prompt missing any; the R<exit> controls split each): the real-Postgres drill RED/GREEN with controls; the stored read AS A NON-SUPERUSER ROLE; both design calls with arms; Kam\'s split; KS-888 kept; the re-pin line by line (a weakened pin is a BLOCKER); the cross-package guards + the KS 764 guard; the gateway cache end to end; T1 round 1 of the cap; the GO string, the subject rule, the key scanner. `## MERGE ADDENDUM` last, ONE LINE (rule 52).' % K['prompt'],
 '- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/` (TEXT only); mail FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE40 batch #1338 (Seat B42, round 40; T1: KS-1370 validate reads the stored revoke, both halves)`.' % K['report'], '',
 '## 4. Routing line — NOT added',
 'Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines) — backup first:',
 '```', '%s|coagent@agentmail.to|yes' % K['pane'], '```',
 'Until it is present the launch action\'s step 0 refuses rc 1 (%s reports it: `%s`; control RB measures the real refusal rc 1).' % (DRYF, last(DRYF, r'line present:')), '',
 '## 5. Controls: `controls_gate40.sh <scratchpad> [--invert]`',
 '- gate39\'s arms re-cut for ONE row: wrong heads (C2 = the develop sha as the head), a moved develop (predev = the #1337 squash, MERGED), a path rename, capture / prompt doctoring, every kit rule 35 / 40-44 / 46-55 SPLIT (the ten requirements among them), the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false (self-)STACK / the REAL re-pin across a move in a copy / RE-RN-RO plants, predict `--simulate foreign1338` and `moved`, fill from SIM / failed pins, SJ1-SJ4 subject plants (SJ4: the 93-char title with no SHORT must refuse), and NS[<spelling>] over gate39\'s AND gate38\'s namespaces.',
 '- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, pgprobe beyond its built-in controls (CT1-CT4 and the arms).', '',
 '## 6. Could not measure (the drafter\'s NOT-MEASURED list)',
 '- No vitest, tsc, eslint, prettier or red-proof run (no `npm ci` — DevMASTER is full and the gate owns them); every suite figure (275/275, 19/19, 9/9 + 5/9 red, 15/15, tsc rc 0, eslint rc 0) is a seat claim. The ks888 re-pin\'s red set was NOT measured (READ only). Not driven: two OS processes, the REAL revoke route, the gateway end to end (READ only), a deployed database\'s grants, the connector-bearer path, a platform DB. The drill\'s socket uses trust auth (the role\'s privileges, not its password, are what the premise needs).', '',
 '## 7. Files',
 '- Kit: kit.json · COMMISSION.md (make_commission_gate40.py) · README.md (make_readme_gate40.py) · rekey_check_gate40.py -> rekey_1.out',
 '- Pins: predict_gate40.py -> predict_1.out(.rc), predict_sim_*.out(.rc), pins_gate40.json (+ .SIM-*.json) · keyscan_gate40.py -> keyscan_1.out · final_lsremote_1.out',
 '- Measurements: pgprobe_gate40.py + pgprobe_gate40.drill.cjs + pgprobe_gate40.runner.ts -> pgprobe_1.out(.rc), pgprobe_gate40.json',
 '- Reads: gh_read_gate40.py -> gh_read_1.out, gh_body_1338.md, gh_comments_1338.md · linear_reads_gate40.py -> linear_reads_1.out, linear_KS-1370.md · capture_mail_gate40.py -> capture_1.out, mail_gate40_ready.md, stopcounts_gate40.json · _api_peek_gate40.py -> _api_peek_1.out',
 '- Prompt/launcher: prompt_gate40.TEMPLATE.txt, launcher_gate40.TEMPLATE.sh.txt, fill_gate40.py -> %s + %s (fill_1.out), launcher_check_1.out · repin_and_launch_gate40.sh -> %s · controls_gate40.sh -> controls_1.out / controls_2.out (+ .rc). The first forward controls run was ABORTED by the drafter\'s own edit of controls_gate40.sh while it ran (bash reads a script incrementally; it died at line 130) — its output is quarantined in the scratchpad `_quarantine_2026-09-29/`. The second forward run read 164/165: control RS still indexed a SECOND row (`ns[1]`, IndexError), so its false stack was never planted — fixed to a self-stack (`ns[0]`), output quarantined beside the first. controls_1.out and controls_2.out are both complete runs of the FINAL script (snapshot compared byte-equal after the runs). Every controls run wrote to the Data-volume scratchpad and was copied in, byte-checked.' % (K['prompt'], K['launcher'], ', '.join(os.path.basename(f) for f in DRY)), '',
 '## 8. The ONE launch command (after the routing line, §4)', '```', launch, '```',
 '- Dry run: append `--dry-run`. Argument 2 may be ANY existing Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`, the Data volume); if `g40_sp/clone.git` is absent there, predict rebuilds it on a re-pin (pgprobe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, an overlap or an END-tree disagreement refuses rc 10; a further `-b42-<n>` PR (e.g. KS-1371 if Seat B 42nd\'s successor raises it) or a KS-1370-titled PR refuses rc 15; a moved head refuses rc 11.']
open(os.path.join(D, 'README.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('wrote %s (%d lines) — launch: %s' % (os.path.join(D, 'README.md'), len(out), launch))
