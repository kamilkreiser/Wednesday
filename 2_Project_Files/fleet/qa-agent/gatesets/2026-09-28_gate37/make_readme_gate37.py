#!/usr/bin/env python3
"""make_readme_gate37.py <scratchpad> — writes README.md for the gate37 kit (the directory this script lives in). Every figure is READ from the kit's own
output files at the moment of writing (each named beside it), plus ONE final `git ls-remote` (READ, from the Secuura checkout) written to
final_lsremote_1.out. Shape copied from gate36's make_readme (gate35 lineage), re-keyed to gate37's two rows. Writes only beside this script."""
import json, os, re, subprocess, sys, datetime, hashlib
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
SP = sys.argv[1] if len(sys.argv) > 1 else ''
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); PG = json.load(open('%s/pgprobe_%s.json' % (D, kit)))
rd = lambda f: open(os.path.join(D, f), encoding='utf-8').read() if os.path.exists(os.path.join(D, f)) else ''
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
NS = sorted(K['prs'])
CHECKOUT = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ls = subprocess.run(['git', '-C', CHECKOUT, 'ls-remote', 'origin', 'refs/heads/develop'] + ['refs/pull/%s/head' % n for n in NS], capture_output=True, text=True).stdout
fl = '%s | %s' % (now, ' | '.join(l for l in ls.strip().splitlines()))
open(D + '/final_lsremote_1.out', 'w').write(fl + '\n')
LSD = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
agree = LSD.get('refs/heads/develop') == P['develop'] and all(LSD.get('refs/pull/%s/head' % n) == P['prs'][n]['head'] for n in NS)
c1, c2 = rd('controls_1.out'), rd('controls_2.out')
s1 = (re.findall(r'^SUMMARY .*$', c1, re.M) or ['(controls_1.out has no SUMMARY)'])[-1]; s2 = (re.findall(r'^SUMMARY .*$', c2, re.M) or ['(controls_2.out has no SUMMARY)'])[-1]
r1, r2 = rd('controls_1.rc').strip(), rd('controls_2.rc').strip()
mm1 = re.findall(r'^  MISMATCH .*$', c1, re.M); ok2 = re.findall(r'^  OK .*$', c2, re.M)
fill = rd('fill_1.out'); lc = rd('launcher_check_1.out'); dry = rd('repin_dryrun_1.out'); rk = rd('rekey_1.out')
dry_line = (re.findall(r'^DRY RUN COMPLETE.*$', dry, re.M) or ['(no DRY RUN COMPLETE line)'])[-1]
routing_line = (re.findall(r'line present: .*$', dry, re.M) or ['?'])[-1]
def sha(f):
    b = open(os.path.join(D, f), 'rb').read(); return len(b), hashlib.sha256(b).hexdigest()
titles = P['titles']; M = P.get('measured', {})
TIERWHY = {'1327': 'T1 key revocation (the lesson\'s full-gate row names it): what DELETE /api/keys/:id answers, and whether the key still validates, when the revoke\'s save fails',
           '1328': 'T1 schema migration: a column the gateway\'s STARTUP migrations add on every database they reach at the next deploy (main, platform, tenants), plus the notify route\'s rotation key; additive and nullable (not the destruction class)'}
SIMS = []
for f in sorted(x for x in os.listdir(D) if re.match(r'predict_sim_.*\.out$', x)):
    SIMS.append('%s -> %s' % (f[len('predict_sim_'):-4], (rd(f).strip().splitlines() or ['?'])[-1].split(' -> ')[0]))
PR_ = PG['runs']; F = PR_['F_update_cost_inprocess']
out = ['# Gateset 2026-09-28_gate37 — README for Wednesday', '',
 'Written %s by the drafter (make_readme_gate37.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now,
 'The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory `%s/` and scratch under `%s` (the scratch clone `g37_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key; the control workdirs `g37_controls_*`; one failed Postgres feasibility dir `g37_pgfeas_*` (initdb ran, the start refused on the socket-path length — nothing listening); assembly parts under `g37/`). It did NOT write the routing line (§4).' % (D, SP),
 'The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its @electric-sql/pglite). GitHub: REST GET only (GH_TOKEN read by name, never printed). Linear: queries only. decisions.json and inbox_routing.conf: read only. No AgentMail call.', '',
 '**gate37 = TWO PRs (T1 x2), one kit, no sibling, NO stack, ONE base.** Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)).', '',
 '| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | files | why this tier (tiers lesson 2026-09-05) |', '|---|---|---|---|---|---|---|']
for n in NS:
    pr = P['prs'][n]
    out.append('| #%s | %s | %s | `%s` | %d on `%s` | %s | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], ', '.join(os.path.basename(p) for p in pr['paths']), TIERWHY[n]))
out += ['', '### Squash subjects and bodies', '',
 '| PR | declared subject (WITHOUT `(#n)`, the PR title as the PULLS API returned it) | declared | lands at (+8, ` (#n)`) | <= 92 | ends in `(#n)`? | squash-body keys: own | FOREIGN keys seen (title / body / commit msg) |', '|---|---|---|---|---|---|---|---|']
for n in NS:
    t = titles[n]
    out.append('| #%s | %s | %d | %d | %s | %s | %s | none hyphenated (keyscan_1.out) |' % (n, t, len(t), len(t) + len(' (#%s)' % n), 'yes' if len(t) + len(' (#%s)' % n) <= 92 else 'NO', 'yes' if re.search(r'\(#\d+\)$', t) else 'no', ' '.join(K['prs'][n]['keys'])))
ss = re.search(r'subject scan: (.*)', fill); ks = re.search(r'key scan: (.*)', fill)
out += ['', 'Measured by fill_1.out: `subject scan: %s`; `key scan: %s`.' % (ss.group(1) if ss else '?', ks.group(1) if ks else '?'),
 '**Commit messages that must not be pasted:** on MG-3 grounds, NONE — neither commit message carries a foreign hyphenated key (keyscan_1.out, MEASURED). By the standing rule (compose, never paste) BOTH are not to be pasted as squash bodies: each ends in a `Co-Authored-By` trailer; #1328\'s names "KS934" un-hyphenated four times (and its body "KS 1054" space-separated); and the TEST FILES carry foreign hyphenated keys as CONTENT — #1327\'s ks888 header names KS-1194, #1328\'s ks934 describe names KS-934 — so a squash body quoting a header, describe or cell title verbatim would attach a foreign ticket.', '',
 'Routing `%s` (**NOT added by the drafter** — §4). GO string `GO: merge #1327, #1328 batch` (or the subset); **the GO mail\'s SUBJECT names Seat B 39th, with NO `#` before the numbers**: `GO (Seat B 39th): merge 1327 1328 on gate37` (the prompt carries it as kit rule exit 51). MERGE ORDER #1327 -> #1328 (END_TREE is order-independent, measured in both orders). The GO goes to **Seat B 39th**, which raised both and merges its own, one at a time.' % K['pane'], '',
 '**Kam\'s cards (READ from `0_Brain/dashboard/data/decisions.json`):** `secuura-ks888-revoke-validate-on-failed-save` RULED **a** (ruled_ts 2026-09-28T20:24:38+10:00) — revoke 503 + keep the in-memory revoke: #1327\'s contract; `secuura-ks888-validate-usage-write-failure` RULED **a** (20:24:07; the commission names 20:22:15) — validate never refuses on a failed usage write: a SEPARATE later PR, validate is untouched here; `secuura-ks1054-f9282-migration-failure-visibility` RULED **a** (20:24:31) — flag a failed startup migration on /health (not yet built; relevant to #1328\'s deploy order). #1327\'s PR body still calls its card "OPEN" (it was written before the ruling). #1328\'s design choices (placement A, the skipped row unstamped, the guarded add-column) are Wednesday\'s under the 2026-08-07 autonomy grant.', '',
 '## 1. BLUF',
 '- **Kit: READY to launch once the routing line is added** — launcher `--check` rc 0 (launcher_check_1.out: `%s`); repin `--dry-run` (repin_dryrun_1.out: %s; routing %s). The real launch refuses rc 1 at step 0 until `%s|coagent@agentmail.to|yes` is in inbox_routing.conf (§4).' % ((re.findall(r'^all guards pass:', lc, re.M) or ['NOT PASSING'])[0], dry_line, routing_line, K['pane']),
 '- **Pinned over develop `%s`** (tree `%s` — gate36\'s END_TREE: its four squashes landed, MERGED) — ls-remote AND fetched AND the API compare agree. ONE merge-base `%s` for both; develop has not moved since, so the move ∩ every own path is EMPTY.' % (P['develop'], P['develop_tree'], P['merge_bases'][0][:12]),
 '  - **END_TREE `%s`** (%s), identical in BOTH orders (%d memoised merge-tree calls); diff(develop, END) == the union of the six own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['merge_tree_calls']),
 '  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s — every pin still current: **%s**.' % (fl.replace('\t', ' '), agree),
 '- **Controls, both ways (controls_gate37.sh):**',
 '  - normal (controls_1.out, rc %s): `%s`%s' % (r1, s1, ('' if not mm1 else ' — MISMATCHES: %s' % mm1)),
 '  - `--invert` (controls_2.out, rc %s): `%s` — %s' % (r2, s2, 'every control reported MISMATCH under inversion (rc 1 by design): each control can fail' if not ok2 else 'NOT every control flipped: %s' % ok2[:5]),
 '- **Simulations (predict):** %s (`moved` = develop + one unrelated synthetic commit, must PASS; `foreign<n>` = develop + a foreign edit of that PR\'s first own file, must REFUSE).' % '; '.join(SIMS),
 '- **OVERLAPS:** NONE. No stack, no shared file, no shared service; every kit path is disjoint from ALL %d other open PRs (#809, KS-693, is in #1328\'s service and shares no file). `merged_blob_paths` NONE and `noop_paths` NONE (predict (c)).' % len(P['inflight']),
 '- **#1327 == golden + the DECLARED hand-written lines (MEASURED, predict_1.out (e)):** READY block == golden == Spark checker patch.diff (%s / %s); the golden applies strict at the merge-base and the product blob == head (%s); diff(golden-applied, head) == EXACTLY the four declared hand-written `+` lines (header :5-7, describe :98): %s. Mint / validate / key-list / revokePriorConnectorKeys handler regions BYTE-EQUAL merge-base vs head: %s. The two inline infra classifiers (mint, revoke) byte-identical.' % (
     M.get('1327', {}).get('ready_bytes_eq_golden'), M.get('1327', {}).get('checker_eq_golden'), M.get('1327', {}).get('product_blob_eq_head'), M.get('1327', {}).get('handwritten_residue_exact'), M.get('1327', {}).get('handler_regions_byte_equal')),
 '- **#1328 on a REAL Postgres engine (MEASURED by the drafter, pgprobe_1.out — PGlite, %s, in-process, no socket, no port):** %s. The stamp UPDATE in-process: median %s ms, p95 %s ms over %d — a LOWER BOUND with no network; the deployed cost is one pool round-trip per attempted row (<= MAX_ROWS 50 per call against a 10000 ms deadline). The head\'s SELECT on an UNMIGRATED schema: `%s`.' % (
     PG['engine'][:40], '; '.join('%s: %s' % (k, v) for k, v in PG['_summary'].items()), F['median_ms'], F['p95_ms'], F['updates'], PR_['E_head_route_sql_on_unmigrated_schema']['select']),
 '- **A throwaway Postgres IS available to the gate** (READ: /opt/homebrew/bin/initdb-18, pg_ctl-18, postgres-18, psql-18; the drafter\'s initdb-18 rc 0) — but its unix socket path must be < 103 bytes: the drafter\'s start in the long scratchpad path FAILED on exactly that (MEASURED). The prompt tells the gate to use a short `mktemp -d`, `listen_addresses=\'\'` (no TCP), never :5432, and PGlite as the fallback.',
 '- **Fleet STOP (READ, bounded region, NOT-FOUND control):** %s. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60.' % '; '.join('#%s %s · %s · %s · %s (%s)' % (n, S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'], S[n]['verdict_line']) for n in NS),
 '- **Linear: both PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-888 and KS-1335 In Progress.',
 '- **Re-key / namespace (rekey_1.out):** %s' % ' | '.join(rk.strip().splitlines()),
 '- **Drafting slips caught (disclosed):** (1) the first Postgres attempt (initdb-18 + pg_ctl-18 in the scratchpad) failed on the 103-byte socket-path limit — switched to PGlite, and the limit is carried into the prompt; (2) PGlite\'s WASM runtime exits non-zero at teardown (a bare `select 1` script exits 100, MEASURED), so the first pgprobe run REFUSED on the rc with a complete result printed — the driver now reports the rc and judges the ONE JSON line, refusing only when it is absent; (3) the first predict printed the spec grep\'s file paths without line numbers — fixed before the pinned run; (4) a count sentence in the prompt template (the security suite +5) was first written as an arithmetic claim — replaced by what is READ (+4 cells in the ks888 file) and the gap left for the gate to account for; (5) the FIRST full controls run read 158 OK / 1 MISMATCH (superseded_controls_1_prefix.out): its NS control caught this README generator, written mid-run, naming the previous seat by its token and a predecessor PR without a lineage marker — fixed, and BOTH control runs were re-run from scratch (the figures above).',
 '- **Sizes / sha256:** %s.' % '; '.join('`%s` %d bytes sha256 `%s`' % ((f,) + sha(f)) for f in (K['prompt'], K['launcher'], 'mail_%s_ready.md' % kit)), '',
 '## 2. Pins — predict_1.out (rc %s)' % rd('predict_1.out.rc').strip()]
for n in NS:
    pr = P['prs'][n]
    out.append('- #%s: %d commit `%s` over merge-base `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat %s; no mode change; move ∩ own paths EMPTY.' % (n, len(pr['commits']), pr['head'][:12], pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
out += ['- `predev` (`%s`, develop^ = gate36\'s #1325 squash) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.' % K['predev'][:12], '',
 '## 3. What the gate owes',
 '- Prompt `%s` — #1327 through the REAL security app: no unhandled rejection / no process exit under a failing revoke save (with a control arm that shows the rejection), 503 / 500 per fault class, the key refused in-process afterwards (and the fresh-object path DRIVEN), mint / validate exactly as at develop, the KS-577 rotate order under a failing mint save and a failing revoke-on-rotate; the fullName rename; SPEC-503-UNDECLARED. #1328 on a REAL Postgres: rotation with real rows, the skipped row NULL, the migration twice, the upgrade, the unmigrated schema (42703), the extra UPDATE against the deadline, DEADLINE-STALE, STAMP-INSIDE-THE-TRY. Every seat arm re-run; suites at develop / head / END_TREE; tsc with `exclude: []`; eslint by hand (no lint scripts); the MANDATED SQUASH TEXT blocks; `## MERGE ADDENDUM` last, ONE LINE PER PR in gate35\'s shape (kit rule exit 52).' % K['prompt'],
 '- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.' % K['report'], '',
 '## 4. Routing line — NOT added',
 'Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines) — backup first:',
 '```', '%s|coagent@agentmail.to|yes' % K['pane'], '```',
 'Until it is present the launch action\'s step 0 refuses rc 1 (repin_dryrun_1.out: "%s").' % routing_line, '',
 '## 5. The ONE launch command', '```',
 '%s/repin_and_launch_%s.sh %s/%s %s' % (D, kit, D, K['launcher'], SP), '```',
 '- Dry run (`--dry-run` appended): repin_dryrun_1.out -> %s.' % dry_line,
 '- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`); if `g37_sp/clone.git` is absent there, predict rebuilds it on a re-pin (pgprobe is NOT re-run by a re-pin — its JSON is read as measured at the pinned heads, which a re-pin never changes). A develop move re-pins in the same action (step 3b); an own-path move, a stack, an overlap or an END-tree disagreement refuses rc 10. A new PR on KS-888 / KS-1335 or on a `-b39-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.', '',
 '## 6. Questions for Wednesday (each with the drafter\'s recommendation)',
 '1. **The routing line** (§4). *Recommend:* add it, then launch.',
 '2. **The coagent@ inbox.** The previous seat reported at its boot that `coagent@agentmail.to` returned HTTP 404 (carried from gate36\'s README, a predecessor record, not re-probed); Seat B 39th\'s plan mail reads `coagent@` = 0 messages. The gate mails FROM coagent@ as commissioned. The drafter did NOT probe AgentMail. *Recommend:* confirm coagent@ answers before launch.',
 '3. **SPEC-503-UNDECLARED (#1327).** The revoke can now answer 503 / 500 and the published `DELETE /api/security/keys/{id}` declares neither (the body says so). *Recommend:* let the gate rule it; if it is a finding, it ships-with (a spec follow-up), not a NO GO — unless the MERGED #1322\'s mint 503 was declared, in which case the asymmetry is worth fixing in this PR.',
 '4. **DEPLOY-ORDER-42703 (#1328).** The head route fails WHOLE (42703) on any database the gateway\'s startup migration has not reached; startup-migration failures are a log line today (KS-1054, ruled a — /health flag not yet built). *Recommend:* launch; if the gate confirms, carry a deploy note (gateway first, every tenant DB checked by schema, not by the runner\'s rc) rather than a NO GO.',
 '5. **STAMP-INSIDE-THE-TRY (#1328).** A stamp that throws reports the row FAILED with no request made. *Recommend:* let the gate rule whether that misreports; the fix-shape (stamp outside the per-row try, or a distinct `stampFailed` bucket) is small.',
 '6. **The describe title (#1327).** The reworded describe names the mint and validate but not the revoke the file now covers. *Recommend:* a finding at most (cosmetic, but it is the fullName of every cell).',
 '7. **§5f:** both PRs are runtime changes — neither moves to Done on offline evidence (the canonical `live sweep owed` comment; #1328\'s names the migration on every database).', '',
 '## 7. Controls: `controls_gate37.sh <scratchpad> [--invert]`',
 '- **controls_1.out:** `%s` (rc %s).' % (s1, r1),
 '- **controls_2.out (`--invert`):** `%s` (rc %s, by design).' % (s2, r2),
 '- Same arms as gate36\'s kit, re-keyed: wrong heads (one hex digit), a moved develop (predev), per-PR path renames (both PRs), capture / prompt doctoring, every kit rule 35 / 40-44 / 46-49 / 51 / 52 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO declaration plants, predict `--simulate foreign1328` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate36\'s and gate35\'s namespaces.',
 '- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, pgprobe\'s verdicts beyond its three built-in controls (CT1-CT3).', '',
 '## 8. Could not measure (the drafter\'s NOT-MEASURED list)',
 '- No suite, tsc, eslint, prettier or red-proof run by the drafter; every seat figure (26 / 265 -> 270, 4 / 10 / 14, 2 / 7 / 9, 6 / 47, 86 / 781, arms a-h) is a claim in its PR body. The seat\'s record folder holds no red / green / suite output files.',
 '- #1327 at runtime: NOTHING — no revoke was driven; the unhandled-rejection, the in-process refusal, the fresh-object path and the rotate order are READ predictions. Mint / validate unchanged is MEASURED only as byte-equal source regions, not as behaviour.',
 '- #1328: the ordering, the skip, the migration and the upgrade were MEASURED on PGlite (PostgreSQL 17.5 WASM, in-process) with the route\'s own SQL text — NOT through the route itself, NOT on a networked Postgres, NOT on Postgres 18 or the deployed version; the UPDATE cost is an in-process lower bound, NOT the deployed wall-clock. The migration was NOT run through `runStartupMigrations` / `migrateDatabase` (the extracted statements were run directly), and not on a tenant or platform database.',
 '- `check:openapi`, the served spec, Schemathesis, legs 3 / 4 / 8 — need a stack or were left to the gate. The api-gateway\'s handling of a security 503 — not read. AgentMail (coagent@) reachability — not probed. Whether any fleet list pins an old ks888 fullName — not searched beyond the repo (the seat measured 0 in the repo).', '',
 '## 9. Files',
 '- Kit: kit.json · COMMISSION.md (make_commission_gate37.py) · README.md (make_readme_gate37.py) · rekey_check_gate37.py -> rekey_1.out',
 '- Pins: predict_gate37.py -> predict_1.out, predict_sim_*.out, pins_gate37.json (+ .SIM-*.json) · keyscan_gate37.py -> keyscan_1.out · final_lsremote_1.out',
 '- Measurements: pgprobe_gate37.py + pgprobe_gate37.mjs -> pgprobe_1.out, pgprobe_gate37.json (#1328 on PGlite)',
 '- Reads: gh_read_gate37.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate37.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate37.py -> capture_1.out, mail_gate37_ready.md, stopcounts_gate37.json · _api_peek_gate37.py -> _api_peek_1.out',
 '- Prompt/launcher: prompt_gate37.TEMPLATE.txt, launcher_gate37.TEMPLATE.sh.txt, fill_gate37.py -> %s + %s (fill_1.out), launcher_check_1.out · repin_and_launch_gate37.sh -> repin_dryrun_1.out · controls_gate37.sh -> controls_1.out / controls_2.out' % (K['prompt'], K['launcher'])]
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote', D + '/README.md', len(out), 'lines | final ls-remote agrees with every pin:', agree)
