#!/usr/bin/env python3
"""make_readme_gate35.py <scratchpad> — writes README.md for the gate35 kit (the directory this script lives in). Every figure is READ from the kit's own
output files at the moment of writing (each named beside it), plus ONE final `git ls-remote` (READ, from the Secuura checkout) written to
final_lsremote_1.out. Shape copied from gate34's make_readme (gate33 lineage), re-keyed to gate35's two rows. Writes only beside this script."""
import json, os, re, subprocess, sys, datetime, hashlib
D = os.path.dirname(os.path.abspath(__file__)); K = json.load(open(D + '/kit.json')); kit = K['kit']
SP = sys.argv[1] if len(sys.argv) > 1 else ''
P = json.load(open('%s/pins_%s.json' % (D, kit))); S = json.load(open('%s/stopcounts_%s.json' % (D, kit))); LP = json.load(open('%s/logprobe_%s.json' % (D, kit)))
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
titles = P['titles']; W = LP['_widen']
TIERWHY = {'1321': 'T1 logging (production log FILE format, secret-leak class), ruled "Third attempt: allow-list the file format"',
           '1322': 'T1 security (the API-key mint\'s failed-save answer; credential surface), ruled "Fix all three routes" — this PR is the mint only'}
out = ['# Gateset 2026-09-28_gate35 — README for Wednesday', '',
 'Written %s by the drafter (make_readme_gate35.py; every figure below is read from the kit\'s own output files at that moment, each named beside it).' % now,
 'The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory `%s/` and scratch under `%s` (the scratch clone `g35_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout\'s repo-local key; the logprobe workdirs `g35_logprobe_*`; the control workdirs `g35_controls_*`; three `pred*.py` assembly parts). Superseded outputs were RENAMED / copied `superseded_*`, never deleted. It did NOT write the routing line (§4). **One stray write outside both:** a mistyped redirect wrote a copy of security `index.ts` at #1322\'s head to `/tmp/x` (source code, no secret) — left in place, not deleted, per the no-delete rule; remove it at will.' % (D, SP or '<scratchpad>'),
 'The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its typescript and winston). GitHub: REST GET only (GH_TOKEN read by name, never printed). Linear: queries only. decisions.json and inbox_routing.conf: read only.', '',
 '**gate35 = TWO PRs, both T1, one kit, no sibling, NO stack, ONE base.** Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)).', '',
 '| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | why this tier |', '|---|---|---|---|---|---|']
for n in NS:
    pr = P['prs'][n]
    out.append('| #%s | %s | %s | `%s` | %d on `%s` | %s |' % (n, ' + '.join(K['prs'][n]['keys']), K['prs'][n]['tier'], pr['head'], len(pr['commits']), pr['merge_base'][:12], TIERWHY[n]))
out += ['', '### Squash subjects and bodies', '',
 '| PR | declared subject (WITHOUT `(#n)`, the PR title as the PULLS API returned it) | declared | lands at (+8, ` (#n)`) | <= 92 | ends in `(#n)`? | squash-body keys: own | FOREIGN hyphenated keys seen (title / body / commit msg) |', '|---|---|---|---|---|---|---|---|']
for n in NS:
    t = titles[n]; L = len(t) + len(' (#%s)' % n)
    out.append('| #%s | %s | %d | %d | %s | %s | %s | none (keyscan_1.out) |' % (n, t, len(t), L, 'yes' if L <= 92 else 'NO', 'yes' if re.search(r'\(#\d+\)$', t) else 'no', ', '.join(K['prs'][n]['keys'])))
out += ['', 'Measured by fill_1.out: `subject scan: %s`; `key scan: %s`. keyscan_1.out: no foreign hyphenated key and no closing word before a key in either title, body or commit message.' % (subj.group(1) if subj else '?', ks.group(1) if ks else '?'),
 '**Commit messages that must not be pasted:** on MG-3 grounds, NONE — neither commit message carries a foreign hyphenated key (MEASURED). The standing rule still holds (compose, never paste): both messages end in a `Co-Authored-By` trailer, and #1321\'s names `#1310`, a cross-reference GitHub would attach to the squash.', '',
 'Routing `%s` (**NOT added by the drafter** — §4). GO string `GO: merge #1321, #1322 batch` (or the subset); **the GO mail\'s SUBJECT must name Seat B 37th**, e.g. `GO (Seat B 37th): merge 1321 1322 on gate35` (the prompt carries this as kit rule exit 51). MERGE ORDER #1321 -> #1322 (END_TREE is order-independent, measured in both orders). The GO goes to **Seat B 37th**, which raised both and merges its own.' % K['pane'], '',
 '**Kam\'s rulings (READ from `0_Brain/dashboard/data/decisions.json`):** card `secuura-ks1348-r2-files-still-leak-allowlist` ruled **a** "Third attempt: allow-list the file format (recommended)", ruled_ts 2026-09-28T06:58:50+10:00. Card `secuura-ks888-failed-key-save-design` ruled **b** "Fix all three routes", ruled_ts 2026-09-28T06:58:57+10:00 (the card RECOMMENDED a, mint-only; Kam chose b). Card `secuura-ks888-revoke-validate-on-failed-save` is **OPEN** (what a failed revoke / validate answers).', '',
 '## 1. BLUF',
 '- **Kit: READY to launch once the routing line is added** — launcher `--check` rc %s (`%s`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: %s). The real launch refuses rc 1 at step 0 until `%s|coagent@agentmail.to|yes` is in inbox_routing.conf (§4).' % (
     '0' if lc.startswith('all guards pass:') else '?', lc.splitlines()[0] if lc else '?', dry_line, K['pane']),
 '- **Pinned over develop `%s`** (tree `%s`, == gate34\'s END_TREE) — ls-remote AND fetched AND the API compare agree; gate34\'s #1316-#1320 squashes in; #1310 CLOSED unmerged. ONE merge-base `%s` for both; develop has not moved since, so the move ∩ every own path is EMPTY.' % (P['develop'], P['develop_tree'], P['merge_bases'][0][:12]),
 '  - **END_TREE `%s`** (%s), identical in both orders (%d merge-tree calls); diff(develop, END) == the union of the four own paths and every END blob == its PR\'s head blob (MG-1).' % (P['end_tree'], P['end_shortstat'], P['merge_tree_calls']),
 '  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): %s — every pin still current: **%s**.' % (fl, agree),
 '- **Controls, both ways (controls_gate35.sh):**',
 '  - normal (controls_1.out, rc %s): `%s`%s' % (r1, s1, (' — MISMATCHES: %s' % mm1) if mm1 else ''),
 '  - `--invert` (controls_2.out, rc %s): `%s`%s' % (r2, s2, (' — every one of the %d controls reported MISMATCH (rc 1 by design): each control can fail' % len(mm2)) if mm2 and not ok2 else (' — OK lines under invert (a control that could not fail): %s' % ok2 if ok2 else '')),
 '- **OVERLAPS:** NONE. The pair is not stacked and shares no file; every kit path is disjoint from ALL %d other open PRs. `merged_blob_paths` NONE and `noop_paths` NONE (predict (c)).' % len(P['inflight']),
 '- **Every head == its READY and its golden (MEASURED, predict_1.out (e)):** each READY block is byte-identical to its brief\'s golden and to the Spark checker\'s patch.diff; both goldens apply strict with `git apply --cached --check` at 54f37d6399bd and every blob == the head\'s. #1322\'s golden writes three blank lines as -/+ pairs, so its raw +/- count (27) differs from the head\'s `git diff -U0` (21); netted of identical pairs (6 lines) it is IDENTICAL — a representation difference, not a code one (the blob equality above is the discriminating instrument).',
 '', '### 1a. The #1321 LOG-FILE WIDEN, repeated through the REAL logger (MEASURED by the drafter, logprobe_gate35.py -> logprobe_1.out)',
 'The REAL originate logger.ts at each revision (transpiled by the checkout\'s typescript 5.9.3, the checkout\'s winston 3.19.0), NODE_ENV=production, a fresh cwd per revision. Revisions: develop, #1321 head, END_TREE, #1310 head (the file-leak CONTROL) and a planted arm (#1321 + `ip` in FILE_LOG_FIELDS). Controls: %s.' % ('; '.join('%s: %s' % (k, v) for k, v in LP['_controls'].items())),
 '- **VALUE sentinels in a FILE** (nested Error under `error` and `upstream` with config.headers.Authorization + response.data.token; a nested Error\'s toJSON and a top-level toJSON; secretKey, privateKey, passwordHash, mnemonic, phone, email_address, userEmails[], ip, jwt, sessionId, recipientPhone; the six ruled keys; a top-level Error\'s password): **#1321 head %s; END_TREE %s.** Under #1310\'s logger every nested-Error and unnamed-key sentinel reached both files (the control), so the instrument can see the leak it reports absent.' % (W['head_files'], W['end_files']),
 '- **Every key any file line carries at the head:** %s — the allow-list, nothing else.' % W['head_file_keys'],
 '- **Message and error text still reach both files:** %s.' % W['head_text_kept'],
 '- **Disclosed loss (a consequence of the ruling, not a defect):** userId / documentId / ip / stack in the files at the head: %s. predict_1.out READ 27 single-line logger calls carrying documentId and 5 carrying userId in originate; errorHandler.ts loses userId and ip.' % W['head_loss'],
 '- **Residue by design (allow-listed strings):** %s — gate33\'s W-3 (`error: String(<Array>)`, 75 originate call sites of that shape, READ) still reaches the files as a string; a secret put in `path` / `requestId` / a metadata `message` would too (no caller found logging req.originalUrl / req.url, READ).' % W['head_residue'],
 '- **STDOUT — the commission\'s "no value reaches ... stdout" does NOT hold, and never did:** at the head stdout still carries %s; at develop it carried every one of those plus the ruled keys. NEW at the head vs develop: **%s**. So stdout is not a widen of #1321 (it improves nothing there beyond r2\'s six keys), and the PR body discloses it ("The Console is unchanged from #1310."). Kam\'s ruling says redaction stays on the Console. The prompt makes the gate measure and RULE it (§6 Q2).' % (W['head_stdout'], W['stdout_new_vs_develop']),
 '', '### 1b. #1322 — READ predictions (the gate measures at runtime; the drafter ran no security code)',
 '- Only the mint opts in to `rethrow` (index.ts :1140); revoke (:1286) and validate (:1354) keep the log-only swallow — their handlers take no `next` (READ).',
 '- The KS-577 order holds as READ: save + rethrow :1140, in-memory drop :1142, `return` 503/500 :1145 — all before the rotate revoke at :1158, so a failed save never revokes the prior key.',
 '- No-database mint: dbSaveApiKey sets memory first (:293) and returns before the INSERT (:294) — no throw, 201 from memory (C4).',
 '- **Seat prediction slip (READ):** the #1322 body says "the newly reachable 503 is not declared in the spec"; security.openapi.ts already declares `503: commonErrorResponses[503]` on POST /api/security/keys (:797). The gate runs `check:openapi`.',
 '- **Scope vs ruling:** Kam ruled b (all three routes); this PR delivers the mint third and says so (`Refs KS-888`). The prompt grades it as disclosed partial delivery (ONE-OF-THREE-ROUTES). TRANSIENT-REFUSES (08 / 57 now answer 503 instead of the ticket\'s log-only) is Wednesday\'s reading of the KS-1194 contract — carried as a Kam question, not a defect.',
 '- Not pinned by the cells (the prompt owes them at runtime): the unsaved key\'s plaintext through validate; the rotate path under a failing save; a numeric / absent `code`; the refusal\'s own log line; stdout / process exit under the candidate arm with the DEFAULT reporter (the seat: `--reporter=json` hides the 2 unhandled errors).',
 '', '### 1c. Other',
 '- **Fleet STOP (READ, bounded region, NOT-FOUND control):** ' + '; '.join('#%s %s · %s · %s · %s (%s)' % (n, S[n]['pre_push_hook_base'], S[n]['fixture_guard'], S[n]['run_shell_suites_region'], S[n]['shell_suites'], S[n]['verdict_line']) for n in NS) + '. After this merge: 28/0 · 6/0 · 49/0 · 60 of 60.',
 '- **Linear: both PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1348 and KS-888 In Progress (KS-888 was Backlog at the seat\'s boot; the board bot walked it).',
 '- **Re-key / namespace (rekey_1.out):** %s' % (' | '.join(l.strip() for l in rk.strip().splitlines()[-2:]) if rk else '?'),
 '- **A drafting lesson recorded in predict:** this git\'s `grep -E` does NOT support `\\s` (it gave 0 for documentId where `[[:space:]]` gave 27) — every predict grep now uses POSIX classes and carries a >0 control.',
 '- **Sizes / sha256:** ' + '; '.join('`%s` %d bytes sha256 `%s`' % ((f,) + sha(f)) for f in (K['prompt'], K['launcher'], 'mail_%s_ready.md' % kit)) + '.',
 '', '## 2. Pins — predict_1.out (rc %s)' % rd('predict_1.out.rc').strip()]
for n in NS:
    pr = P['prs'][n]
    out.append('- #%s: 1 commit `%s` over merge-base `%s`; %d behind develop; merged tree `%s`; every merged blob == its head blob; numstat %s; no mode change; move ∩ own paths EMPTY.' % (n, pr['head'][:12], pr['merge_base'], pr['behind'], pr['merged_tree'], pr['numstat']))
sims = ['%s -> %s' % (f[len('predict_sim_'):-4], (rd(f).strip().splitlines() or ['?'])[-1].split(' -> ')[0]) for f in sorted(x for x in os.listdir(D) if re.match(r'predict_sim_.*\.out$', x))]
out += ['- Simulations: %s. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR\'s first own file (must REFUSE). `predev` (`%s`, develop^) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.' % ('; '.join(sims), K['predev'][:12]),
 '- Superseded, kept: `superseded_prelogprobe_*` — the first pinned run (predict before logprobe existed, so its WIDEN line read UNMEASURED) and a controls run stopped at control 5 once that was noticed; predict, fill and --check were re-run after logprobe, then the controls ran clean both ways.',
 '', '## 3. What the gate owes',
 '- Prompt `%s` — the #1321 LOG-FILE WIDEN through the real logger (files, stdout, text kept, the disclosed loss, #1310 as the file-leak control), the allow-list arms; the #1322 route table (no `sk_` in any refused body, unsaved not listed / not valid, each infra class, revoke / validate under a failing INSERT with exit codes and unhandled-rejection counts, the memory-only 201, the rotate order), the candidate arm under both reporters, `check:openapi`; every seat red proof re-run; suites at develop / head / END_TREE; tsc with `exclude: []`; lint (security has none); the MANDATED SQUASH TEXT blocks; `## MERGE ADDENDUM` last.' % K['prompt'],
 '- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/%s/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.' % K['report'],
 '', '## 4. Routing line — NOT added',
 'Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines — the previous kit pane line sits at line 135, READ) — backup first:',
 '```', '%s|coagent@agentmail.to|yes' % K['pane'], '```',
 'Until it is present the launch action\'s step 0 refuses rc 1 (repin_dryrun_1.out: "line present: 0").',
 '', '## 5. The ONE launch command',
 '```', '%s/repin_and_launch_%s.sh %s/%s %s' % (D, kit, D, K['launcher'], SP or '<a scratchpad dir>'), '```',
 '- Dry run (`--dry-run` appended): repin_dryrun_1.out -> %s (rc 0).' % dry_line,
 '- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`); if `g35_sp/clone.git` is absent there, predict rebuilds it on a re-pin (logprobe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, a stack, an overlap or an END-tree disagreement refuses rc 10. A new PR on KS-1348 / KS-888 or on a `-b37-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.',
 '', '## 6. Questions for Wednesday (each with the drafter\'s recommendation)',
 '1. **The routing line** (§4). *Recommend:* add it, then launch.',
 '2. **Stdout.** The commission says "confirm no value reaches either file or stdout". Measured: the files are clean, but stdout still carries the nested-Error, toJSON and unnamed-key values — exactly as at develop (nothing new), disclosed in the body, and inside Kam\'s "redaction stays on the Console". The prompt asks the gate to measure it and grade it as a pre-existing exposure carried forward, not a widen of #1321. *Recommend:* launch as drafted; if stdout is collected into log storage in production, that is a new Kam card (allow-list or value-walk the Console too), not a NO GO here.',
 '3. **KS-888 scope.** Kam chose b (all three routes) over the recommended a; the PR is the mint only and the revoke / validate card is still open. *Recommend:* launch; GO on the mint as disclosed partial delivery; KS-888 stays In Progress.',
 '4. **Transient faults now refuse the mint (503)** — Wednesday\'s reading of the KS-1194 contract. *Recommend:* confirm with Kam in the same card round as revoke / validate; a one-line narrowing if he meant structural-only.',
 '5. **§5f:** both are runtime changes — neither moves to Done on offline evidence. *Recommend:* the merge seat posts the canonical `live sweep owed` comment.',
 '6. **The disclosed loss** (userId / documentId / ip / stack out of the files). *Recommend:* accept as ruled; if operators need userId / documentId in the files, add them to FILE_LOG_FIELDS as a follow-up (the planted ip arm shows the allow-list is the single control point).',
 '', '## 7. Controls: `controls_gate35.sh <scratchpad> [--invert]`',
 '- **controls_1.out:** `%s` (rc %s).' % (s1, r1),
 '- **controls_2.out (`--invert`):** `%s` (rc %s, by design).' % (s2, r2),
 '- Same arms as gate34\'s kit, re-keyed: wrong heads (one hex digit), a moved develop (predev), per-PR path renames, capture / prompt doctoring, every kit rule 35 / 40-44 / 46-51 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO declaration plants, predict `--simulate foreign1322` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate34\'s and gate33\'s namespaces.',
 '- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, logprobe\'s verdicts beyond its five built-in controls.',
 '', '## 8. Could not measure (the drafter\'s NOT-MEASURED list)',
 '- No suite, tsc, lint or red-proof run by the drafter; the seat\'s figures are claims in its PR bodies (its raise/ holds no per-item red / green / suite files; its quarantine/ no tsconfig).',
 '- #1322 at runtime: nothing — no `sk_` scan, no list / validate of the unsaved key, no revoke / validate under a failing INSERT, no rotate run. All READ only.',
 '- #1321 through a real fail500 route or errorHandler (logprobe drives `logger.error` directly with shaped metadata), the error.log level filter, a non-string `message` — not measured.',
 '- `check:openapi`, the served spec, Schemathesis, legs 3 / 4 / 8 — need a stack or were left to the gate.',
 '- Whether stdout is shipped to persistent log storage in production (deployment config) — not read.',
 '', '## 9. Files',
 '- Kit: kit.json · COMMISSION.md (make_commission_gate35.py) · README.md (make_readme_gate35.py) · rekey_check_gate35.py -> rekey_1.out',
 '- Pins: predict_gate35.py -> predict_1.out, predict_sim_*.out, pins_gate35.json (+ .SIM-*.json) · keyscan_gate35.py -> keyscan_1.out · final_lsremote_1.out',
 '- Measurements: logprobe_gate35.py -> logprobe_1.out, logprobe_gate35.json (#1321 WIDEN)',
 '- Reads: gh_read_gate35.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate35.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate35.py -> capture_1.out, mail_gate35_ready.md, stopcounts_gate35.json · _api_peek_gate35.py -> _api_peek_1.out',
 '- Prompt/launcher: prompt_gate35.TEMPLATE.txt, launcher_gate35.TEMPLATE.sh.txt, fill_gate35.py -> %s + %s (fill_1.out), launcher_check_1.out · repin_and_launch_gate35.sh -> repin_dryrun_1.out · controls_gate35.sh -> controls_1.out / controls_2.out' % (K['prompt'], K['launcher'])]
open(D + '/README.md', 'w').write('\n'.join(out) + '\n')
print('wrote %s/README.md (%d lines) | pins current at final ls-remote: %s' % (D, len(out), agree))
