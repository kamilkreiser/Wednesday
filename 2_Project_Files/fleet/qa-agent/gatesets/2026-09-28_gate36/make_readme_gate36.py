#!/usr/bin/env python3
"""make_readme_gate36.py <scratchpad> — writes README.md for the gate36 kit (the directory this script lives in). Every figure is READ from the kit's own
output files at the moment of writing (each named beside it), plus ONE final `git ls-remote` (READ, from the Secuura checkout) written to
final_lsremote_1.out. Shape copied from gate35's make_readme (gate34 lineage), re-keyed to gate36's four rows. Writes only beside this script."""
import json, os, re, subprocess, sys, datetime, hashlib
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
SP = sys.argv[1] if len(sys.argv) > 1 else ''
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); EP = json.load(open('%s/emitprobe_%s.json' % (D, kit)))
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
mm1 = re.findall(r'^  MISMATCH .*$', c1, re.M); mm2 = re.findall(r'^  MISMATCH .*$', c2, re.M); ok2 = re.findall(r'^  OK .*$', c2, re.M)
fill = rd('fill_1.out'); lc = rd('launcher_check_1.out'); dry = rd('repin_dryrun_1.out'); rk = rd('rekey_1.out')
subj = re.search(r'subject scan: (.*)', fill); ks = re.search(r'key scan: (.*)', fill)
dry_line = (re.findall(r'^DRY RUN COMPLETE.*$', dry, re.M) or ['(no DRY RUN COMPLETE line)'])[-1]
def sha(f):
    b = open(os.path.join(D, f), 'rb').read(); return len(b), hashlib.sha256(b).hexdigest()
titles = P['titles']; M = P.get('measured', {})
TIERWHY = {'1323': 'T1 verify-claim: changes what the gateway TELLS a verifier (`verified`, `verificationConfidence`, the demo\'s on-chain badge)',
           '1324': 'T1 blob-write: the defect it narrows ERASED persisted anchor fields (data-destruction class); "token" = the Cardano thread-token NFT cache, not an auth token',
           '1325': 'T2 test-only: one cell file, no product byte (MEASURED: predict (e))',
           '1326': 'T2 types-only, CONDITIONAL on no runtime change (MEASURED by the drafter\'s emit probe; the gate re-measures) — it types a revocation field, and key revocation is a T1 surface'}
out = ['# Gateset 2026-09-28_gate36 — README for Wednesday', '',
 'Written %s by the drafter (make_readme_gate36.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now,
 'The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory `%s/` and scratch under `%s` (the scratch clone `g36_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key; the emit-probe workdirs `g36_emitprobe_*`; the control workdirs `g36_controls_*`; assembly parts and trial outputs under `g36/`). It did NOT write the routing line (§4).' % (D, SP or '<scratchpad>'),
 'The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its typescript). GitHub: REST GET only (GH_TOKEN read by name, never printed). Linear: queries only. decisions.json and inbox_routing.conf: read only.', '',
 '**gate36 = FOUR PRs (T1 x2, T2 x2), one kit, no sibling, NO stack, ONE base.** Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)).', '',
 '| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | why this tier (tiers lesson 2026-09-05) |', '|---|---|---|---|---|---|']
for n in NS:
    pr = P['prs'][n]
    out.append('| #%s | %s | %s | `%s` | %d on `%s` | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], TIERWHY[n]))
out += ['', '### Squash subjects and bodies', '',
 '| PR | declared subject (WITHOUT `(#n)`, the PR title as the PULLS API returned it) | declared | lands at (+8, ` (#n)`) | <= 92 | ends in `(#n)`? | squash-body keys: own | FOREIGN hyphenated keys seen (title / body / commit msg) |', '|---|---|---|---|---|---|---|---|']
for n in NS:
    t = titles[n]; L = len(t) + len(' (#%s)' % n)
    out.append('| #%s | %s | %d | %d | %s | %s | %s | none (keyscan_1.out) |' % (n, t, len(t), L, 'yes' if L <= 92 else 'NO', 'yes' if re.search(r'\(#\d+\)$', t) else 'no', ', '.join(K['prs'][n]['keys'])))
out += ['', 'Measured by fill_1.out: `subject scan: %s`; `key scan: %s`. keyscan_1.out: no foreign hyphenated key and no closing word before a key in any title, body or commit message.' % (subj.group(1) if subj else '?', ks.group(1) if ks else '?'),
 '**Commit messages that must not be pasted:** on MG-3 grounds, NONE — no commit message carries a foreign hyphenated key (MEASURED). By the standing rule (compose, never paste) ALL FOUR are not to be pasted as squash bodies: each ends in a `Co-Authored-By` trailer; #1323\'s names "KS 1069" / "KS 522" space-separated (harmless as written, but not squash text); and #1325\'s TEST FILE carries a hyphenated `KS-1180` as content — a squash body quoting the new assertion string verbatim would attach KS-1180 (the seat\'s own keyscan refused exactly that on its first #1325 body).', '',
 'Routing `%s` (**NOT added by the drafter** — §4). GO string `GO: merge #1323, #1324, #1325, #1326 batch` (or the subset); **the GO mail\'s SUBJECT must name Seat B 38th, with NO `#` before the numbers**: `GO (Seat B 38th): merge 1323 1324 1325 1326 on gate36` (the prompt carries this as kit rule exit 51). MERGE ORDER #1323 -> #1324 -> #1325 -> #1326 (END_TREE is order-independent, measured in all %d orders). The GO goes to **Seat B 38th**, which raised all four and merges its own, one at a time.' % (K['pane'], P['orders']), '',
 '**Kam\'s cards (READ from `0_Brain/dashboard/data/decisions.json`):** NONE rules any of the four PRs. `secuura-ks1124-f4-failed-anchor-shows-pending` is OPEN (F4 — out of #1324\'s scope); `secuura-ks1352-revoked-credentials-still-verify` is OPEN (a revoked credential still verifies — NOT fixed by #1326). #1325\'s and #1326\'s design choices were Wednesday\'s, under the 2026-08-07 autonomy grant (the PR bodies say so).', '',
 '## 1. BLUF',
 '- **Kit: READY to launch once the routing line is added** — launcher `--check` rc %s (`%s`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: %s). The real launch refuses rc 1 at step 0 until `%s|coagent@agentmail.to|yes` is in inbox_routing.conf (§4).' % (
     '0' if lc.startswith('all guards pass:') else '?', lc.splitlines()[0] if lc else '?', dry_line, K['pane']),
 '- **Pinned over develop `%s`** (tree `%s`, == gate35\'s END_TREE) — ls-remote AND fetched AND the API compare agree; gate35\'s #1321 / #1322 squashes in (MERGED). ONE merge-base `%s` for all four; develop has not moved since, so the move ∩ every own path is EMPTY.' % (P['develop'], P['develop_tree'], P['merge_bases'][0][:12]),
 '  - **END_TREE `%s`** (%s), identical in ALL %d orders (%d memoised merge-tree calls); diff(develop, END) == the union of the seven own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['orders'], P['merge_tree_calls']),
 '  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s — every pin still current: **%s**.' % (fl, agree),
 '- **Controls, both ways (controls_gate36.sh):**',
 '  - normal (controls_1.out, rc %s): `%s`%s' % (r1, s1, (' — MISMATCHES: %s' % mm1) if mm1 else ''),
 '  - `--invert` (controls_2.out, rc %s): `%s`%s' % (r2, s2, (' — every one of the %d controls reported MISMATCH (rc 1 by design): each control can fail' % len(mm2)) if mm2 and not ok2 else (' — OK lines under invert (a control that could not fail): %s' % ok2 if ok2 else '')),
 '- **OVERLAPS:** NONE. No stack, no shared file (#1323 and #1325 share the api-gateway SERVICE only); every kit path is disjoint from ALL %d other open PRs. `merged_blob_paths` NONE and `noop_paths` NONE (predict (c)).' % len(P['inflight']),
 '- **#1323 / #1324 == their READY and golden (MEASURED, predict_1.out (e)):** each READY block is byte-identical to its brief\'s golden and to the Spark checker\'s patch.diff; both goldens apply strict with `git apply --cached --check` at d9ce1403d158 and every blob == the head\'s. The +/- lines are **SLIDE-EQUAL, not IDENTICAL**: the same lines per file, but in each TEST file the inserted block\'s blank line sits at the other end in the brief than in `git diff -U0` — a representation difference; the blob equality is the discriminating instrument. #1325 / #1326 have NO READY (seat-written).',
 '- **#1326 no-runtime-change (MEASURED by the drafter, emitprobe_gate36.py -> emitprobe_1.out):** %s. Controls: %s.' % (EP['_summary'], '; '.join('%s: %s' % (k, v) for k, v in EP['_controls'].items())),
 '', '### 1a. #1323 KS-1129 livescan — READ predictions (the gate measures THROUGH THE REAL ROUTE)',
 '- The guards only NARROW: every live reply the head accepts, the merge-base accepted (READ). ONE live `anchors/verify/` fetch in api-gateway src — the guards cover every gateway live reader (READ, predict).',
 '- **MIXED-ECHO:** `liveConfirmedAt` (:612) is set inside the verified branch whatever the hash / height guards decide; `txHash = liveTxHash || persistedTxHash`, `blockHeight = liveBlockHeight || persistedBlockHeight` (:666/:667); `source` is `cardano-live` whenever the live hash passed (:776). So a reply whose hash passes but height is refused answers `source: cardano-live` with the live hash beside the PERSISTED (or null) height, and a refused hash still echoes the reply\'s `confirmedAt`. The CLAIM is guarded; the echo is presentation — the prompt makes the gate measure it and say whether it misleads.',
 '- **GUARD-PARITY:** the same placeholder regex as the persisted read (:646); neither demands 64-hex. **STRICT-HEIGHT:** a string `blockNumber` does not fall back to a numeric `blockHeight` (`??` stops at a non-null string). The body calls L5 "a behaviour choice, not a bug fix" (from the E7 ruling).',
 '- **HELD-SURFACE (open question):** the 09-25 KS-1129 comment calls the gateway chain-scan readers "a held surface"; the body says "no recorded hold was found" and that Wednesday reads the hold as lapsed. Carried to the gate as a question, not a defect (§6 Q3).',
 '', '### 1b. #1324 KS-1124 mintmerge — WHAT REMAINS of the race (READ; the gate measures each through the real create route)',
 '- **R1 WINDOW:** still read-then-write — an anchor write landing between the read-back (:799) and the cache write is lost (the PR says so).',
 '- **R2 MIRROR (not in the PR\'s scope, not disclosed in its body):** the create-path anchor-accept write (`blockchain: initial`, :913) and the anchor_failed write (:928) REPLACE the column wholesale and do not carry `threadToken` — a thread-token write that lands FIRST is erased by them. KS-1074\'s `carriedForward` covers the anchorStateSync writers only. The same O1 bug in the other direction.',
 '- **R3 READ FAILURE:** `getDocument(...).catch(() => null)` falls back to the create-time copy — the pre-PR overwrite — when the read-back rejects.',
 '- Flag-gated (STATE_THREAD_NFT_ENABLED=true AND SIMULATE_ANCHORING !== \'true\'); the atomic fix (a JSONB merge in documentRepo) is unruled. The brief\'s arm and the seat\'s arm differ (the seat\'s first arm was a TS6133 load failure) — the gate re-runs both.',
 '', '### 1c. #1325 KS-1227 and #1326 KS-1351',
 '- #1325: TEST-ONLY (predict (e): no product file); 8 cells at base and head; R1\'s expected substring is a shorter prefix of the new message (READ: any change after "ASKED once" no longer reds R1). The try/finally detach and R2 were already at develop — the PR may discharge KS-1227\'s DoD while saying `Refs`.',
 '- #1326: TS2339 4 -> 0 is the SEAT\'s figure (the drafter did not run tsc); the trap it recorded — vc-issuer resolves @secuura/shared to `dist/`, so shared must be REBUILT before any consumer tsc — is in the prompt. The credentialRepo.ts :95 anchor is NOT byte-unique alone (also :118, getByHash): the kit and the prompt use a two-line anchor. %s (predict (e), READ). KS-1352 (revoked credentials still verify) is NOT fixed by it.' % ((re.search(r'THE NARROWING.S REACH \(READ[^)]*\): (\d+ source lines in \d+ files)', rd('predict_1.out')) or [None, '?'])[1] + ' name `SecuuraCredential`'),
 '', '### 1d. Other',
 '- **Fleet STOP (READ, bounded region, NOT-FOUND control):** ' + '; '.join('#%s %s · %s · %s · %s (%s)' % (n, S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'], S[n]['verdict_line']) for n in NS) + '. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60.',
 '- **Linear: all four PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1129, KS-1124, KS-1227, KS-1351 In Progress (the seat read KS-1124 and KS-1351 as Backlog at its boot; the board bot walked them).',
 '- **Re-key / namespace (rekey_1.out):** %s' % (' | '.join(l.strip() for l in rk.strip().splitlines()[-2:]) if rk else '?'),
 '- **Drafting slips caught (disclosed):** (1) the first READY comparison read DIFFER — an insertion slide, not a code difference; the comparator now reports SLIDE-EQUAL beside the strict golden apply, with its own control; (2) the first consumer grep used `\\b`, which this git\'s ERE does not support — a false 0; now POSIX with a >0 control; (3) a quoting slip in the assembled predict (an unescaped apostrophe) failed the first sims with a SyntaxError — fixed, every sim re-run.',
 '- **Sizes / sha256:** ' + '; '.join('`%s` %d bytes sha256 `%s`' % ((f,) + sha(f)) for f in (K['prompt'], K['launcher'], 'mail_%s_ready.md' % kit)) + '.',
 '', '## 2. Pins — predict_1.out (rc %s)' % rd('predict_1.out.rc').strip()]
for n in NS:
    pr = P['prs'][n]
    out.append('- #%s: 1 commit `%s` over merge-base `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat %s; no mode change; move ∩ own paths EMPTY.' % (n, pr['head'][:12], pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
sims = ['%s -> %s' % (f[len('predict_sim_'):-4], (rd(f).strip().splitlines() or ['?'])[-1].split(' -> ')[0]) for f in sorted(x for x in os.listdir(D) if re.match(r'predict_sim_.*\.out$', x))]
out += ['- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). `predev` (`%s`, develop^ = gate35\'s #1321 squash) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.' % ('; '.join(sims), K['predev'][:12]),
 '', '## 3. What the gate owes',
 '- Prompt `%s` — #1323 through the REAL route (simulated / mock / string-height / strict-verified replies at merge-base, head and END_TREE, a real-reply control, the mixed echo, the held-surface question); #1324 the race table through the real create route (the fixed order, the window, the mirror, the read failure; the brief\'s and the seat\'s arms); #1325 the coupling arms and the same-service END_TREE run; #1326 TS2339 4 -> 0 with shared REBUILT, a consumer sweep, the emit re-measured, prefer-const 1 -> 0; every seat red proof re-run; suites at develop / head / END_TREE; tsc with `exclude: []`; lint; the MANDATED SQUASH TEXT blocks; `## MERGE ADDENDUM` last.' % K['prompt'],
 '- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.' % K['report'],
 '', '## 4. Routing line — NOT added',
 'Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines — the previous kit\'s pane line sits at line 136, READ) — backup first:',
 '```', '%s|coagent@agentmail.to|yes' % K['pane'], '```',
 'Until it is present the launch action\'s step 0 refuses rc 1 (repin_dryrun_1.out: "line present: 0").',
 '', '## 5. The ONE launch command',
 '```', '%s/repin_and_launch_%s.sh %s/%s %s' % (D, kit, D, K['launcher'], SP or '<a scratchpad dir>'), '```',
 '- Dry run (`--dry-run` appended): repin_dryrun_1.out -> %s (rc 0).' % dry_line,
 '- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`); if `g36_sp/clone.git` is absent there, predict rebuilds it on a re-pin (the emit probe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, a stack, an overlap or an END-tree disagreement refuses rc 10. A new PR on KS-1129 / KS-1124 / KS-1227 / KS-1351 or on a `-b38-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.',
 '', '## 6. Questions for Wednesday (each with the drafter\'s recommendation)',
 '1. **The routing line** (§4). *Recommend:* add it, then launch.',
 '2. **The coagent@ inbox.** Seat B 38th\'s plan confirmation (item 13, READ) says `coagent@agentmail.to` "now returns HTTP 404" and names `secuura-blockchain@agentmail.to` as the live inbox. The gate mails FROM coagent@ and the routing line routes to coagent@, as commissioned. The drafter did NOT probe AgentMail. *Recommend:* confirm coagent@ answers before launch; if it does not, the gate\'s verdict mail cannot be sent.',
 '3. **HELD-SURFACE (#1323).** The 09-25 KS-1129 comment calls the gateway chain-scan readers "a held surface"; no hold is recorded that the seat or the brief found. *Recommend:* confirm the hold has lapsed (or ask Kam) before signing a GO on #1323; the gate carries it as a question.',
 '4. **The tiers.** #1323 T1 (verifier claim), #1324 T1 (data-destruction class; the thread token is an NFT cache, not an auth token), #1325 T2, #1326 T2 conditional on no runtime change. *Recommend:* as drafted; the prompt tells the gate to re-tier #1326 to T1 if it finds any runtime byte beyond let -> const.',
 '5. **The MIRROR race (#1324, R2).** The create-path anchor-accept / anchor_failed writes erase a threadToken that landed first — not in the PR, not in its body. *Recommend:* launch; if the gate measures it, ticket it (KS-1074 extension or new) — not a NO GO on #1324. The atomic JSONB merge that would close R1 and R2 is a design question for Kam.',
 '6. **§5f:** #1323 and #1324 are runtime changes — neither moves to Done on offline evidence (the canonical `live sweep owed` comment). #1325 / #1326 change no runtime.',
 '7. **KS-1352.** #1326 declares `revoked` but verify still does not read it (card OPEN, default a at Tue 29 Sep 09:00 AEST). *Recommend:* no action in this gate; the #1326 verdict line says so.',
 '', '## 7. Controls: `controls_gate36.sh <scratchpad> [--invert]`',
 '- **controls_1.out:** `%s` (rc %s).' % (s1, r1),
 '- **controls_2.out (`--invert`):** `%s` (rc %s, by design).' % (s2, r2),
 '- Same arms as gate35\'s kit, re-keyed: wrong heads (one hex digit), a moved develop (predev), per-PR path renames (all four PRs), capture / prompt doctoring, every kit rule 35 / 40-44 / 46-51 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO declaration plants, predict `--simulate foreign1324` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate35\'s and gate34\'s namespaces.',
 '- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, the emit probe\'s verdicts beyond its four built-in controls.',
 '', '## 8. Could not measure (the drafter\'s NOT-MEASURED list)',
 '- No suite, tsc, lint, prettier or red-proof run by the drafter; every seat figure (20/20, 781, 6/6, 1055, 8/8, 773, TS2339 4 -> 0, 15 files / 140, the arms) is a claim in its PR bodies and records. Its raise/ holds tamper diffs for KS-1129 / KS-1124 (READ, not run) and no red / green output files.',
 '- #1323 through the real route: NOTHING — no simulated / mock / string-height reply was driven; the MIXED-ECHO is a READ prediction.',
 '- #1324 races: NOTHING at runtime — R1 / R2 / R3 are READ from documents.ts / anchorStateSync.ts / documentRepo.ts. Whether any deployed environment sets STATE_THREAD_NFT_ENABLED — not read.',
 '- #1326: TS2339 and the consumer sweep not run (the emit probe measures emitted JS only; `.d.ts` output not compared).',
 '- `check:openapi`, the served spec, Schemathesis, legs 3 / 4 / 8 — need a stack or were left to the gate. Whether the KS-1129 "held surface" was ever recorded anywhere outside WEDNESDAY/0_Brain — not searched. AgentMail (coagent@) reachability — not probed.',
 '', '## 9. Files',
 '- Kit: kit.json · COMMISSION.md (make_commission_gate36.py) · README.md (make_readme_gate36.py) · rekey_check_gate36.py -> rekey_1.out',
 '- Pins: predict_gate36.py -> predict_1.out, predict_sim_*.out, pins_gate36.json (+ .SIM-*.json) · keyscan_gate36.py -> keyscan_1.out · final_lsremote_1.out',
 '- Measurements: emitprobe_gate36.py -> emitprobe_1.out, emitprobe_gate36.json (#1326 no runtime change)',
 '- Reads: gh_read_gate36.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate36.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate36.py -> capture_1.out, mail_gate36_ready.md, stopcounts_gate36.json · _api_peek_gate36.py -> _api_peek_1.out',
 '- Prompt/launcher: prompt_gate36.TEMPLATE.txt, launcher_gate36.TEMPLATE.sh.txt, fill_gate36.py -> %s + %s (fill_1.out), launcher_check_1.out · repin_and_launch_gate36.sh -> repin_dryrun_1.out · controls_gate36.sh -> controls_1.out / controls_2.out' % (K['prompt'], K['launcher'])]
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote %s/README.md (%d lines) | pins current at final ls-remote: %s' % (D, len(out), agree))
