STARTABLE: B1430 YES | B1431 YES | B1432 YES | B1433 YES | B1434 YES (all five still need Tuesday's stamp: four `____` slots each, READ-WHOLE last)

# NexusAI lane kits B1430-B1434: redraft against REVIEW.md

Redrafter: an Agent-tool kit drafter for Tuesday. Clocks are from `date` in the same action: 06:15:01 (origin main read), 06:17:25 (Jira reads), 06:23:21 (first partition run), 06:25:01 AEDT 2026-11-10 (final partition run, main re-read `3929b7946e2de85ce2ea312ac70bb64134a767e6`).
Files written: the five kits, five `.pre-1110-review` copies (each `cmp`-equal to its kit before any edit), and this file. One rename: `2026-11-10_B1434_SEAT-R196_nexusai-records-sweep.md` became `2026-11-10_B1434_SEAT-R202_nexusai-records-sweep.md` (`mv`; `cmp`-equal to its `.pre` copy right after the move; no other file referenced the old name, measured by `grep -rIl` over `2_Project_Files` and `0_Brain/daily_tuesday`). Its `.pre-1110-review` copy keeps the old name.
Instruments: `gh api -X GET` under `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config` (the project `CLAUDE.md` names no gh config dir; this one exists). Jira was read only through a scratch copy of b774lib re-pointed to this drive, with `post_comment`, `create` and `do_transition` set to `None` and `_call` wrapped to refuse any non-GET. No token was printed. No git write verb on any repo.

## Rulings applied, item by item (file:line printed by `grep -n` after the last edit)

| # | Review item | What changed | Where |
|---|---|---|---|
| 1 | Jira helper hard-codes `/Volumes/Laptop-DEV` (HOLD for all five) | Each seat copies `session-tools/b774/b774lib.py` and `jira-adf.py` into its own `.tools/b<NNNN>/`, `cmp`s both, re-points ONLY the two drive-path lines (lines 8 and 12 at drafting; the review said 9 and 13, `grep -n` reads 8 and 12), prints `diff` (2 lines, 4 `^[<>]` lines), proves the import, sets the three write verbs to `None`. Never edits the original. PRIOR-WORK reads go through the copy. The records seat keeps writes off until Step 4. Drafter's proof on a scratch copy: `cmp` equal, diff 2 lines, import ok, `( key = RD-798 )` 1, `( text ~ "zzqxnonexist" )` 0 | B1430:65, B1431:87, B1432:57, B1433:63 (Step 0); the PRIOR-WORK line in each; B1434:26-27, :39 |
| 2 | Models | T, F, B on Sonnet: `claude-sonnet-5-5` (`models_latest.json:23`), launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, routing row `model-routing.md:92` (C2, Sonnet 1st). S stays Opus (`:93`, C3, unchanged). B1434 stays Sonnet (`:110`, G3) | B1431:4 and :241, B1432:4 and :185, B1433:4 and :128; B1430:4 and :192 unchanged |
| 3 | `deploy-demo.yml` not fenced (B1431) | HOLD 12: lane T never edits `.github/workflows/deploy-demo.yml` (not even a `uses:` pin) nor any line naming `CI_DEPLOY_ENABLED`; a ticket that needs either is a STOP for that item (`NEEDS-SHARED <key> <file>:<line>` in HELD, build nothing of it, continue); never execute `scripts/deploy-*.sh` or `scripts/setup-ci-oidc.sh`. The file is `-` in OWNS-T and owned by no lane. Measured at main: `CI_DEPLOY_ENABLED` in 3 lines, all in that file (`:16`, `:53`, `:91`), frame = the 6 files under `.github/` plus `scripts/deploy-dev.sh`, `deploy-manual.sh`, `setup-ci-oidc.sh` (9 files read by `gh api -X GET contents`); control `azure/login` reads 2 | B1431:84 (HOLD 12), :21 OWNS-T, Block 1 RD-605 note |
| 4 | Partition (1a-1f) | See "Partition" below: OWNS blocks in every kit, existing tests per lane, rd486 to B, feedback-attachments to S, cross-lane tickets homed wholly (13 files moved) or dropped (19 tickets). Block 3 of S is now "files moved into YOUR FILES" (no cross-lane wait); T's Block 3 is RD-980 only; F's Block 3 is RD-396 only; B has no Block 3. The "other lanes" prose now lists every lane in full (1f) | B1430:19-60 and :140; B1431:19-82 and :193; B1432:19-52 and :143; B1433:19-58 and :89; B1434:29-36 |
| 5 | `static/js/index.js` reservation | Not reserved now (lanes.md:33/:79). The 13 tickets (RD-146, 220, 349, 350, 439, 532, 613, 676, 677, 771, 835, 861, 901; re-derived from `tickets_paths.json`, control: 78 F keys read) are released into F. HOLD 12 in F: an L3 start re-reserves both files; before each push touching either, `ls-remote` filtered for an L3 branch reads 0 (control `refs/heads/main$` 1) and RD-937 reads To Do | B1432:20, :54 (HOLD 12), :61 |
| 6 | B1433 line 40 | Now: RD-798 remainder, RD-804, RD-805 (its five files), each by its ticket. The S-ticket alerts (intentRouter, queryPreprocessor, ticketStore, marketplaceStore, validators, costCentreMap) and `incidents.js` (no ticket) are gone from the block | B1433:67 |
| 7 | Names | B1431 RD-458 row and B1432 RD-262 row say "the product owner's". Every builder kit gets HOLD 11: an underscore-aware person scan of the commit message and added lines, names taken from `scanlib1114.py:20` by `sed -n 20p` (never imported), pattern `(?<![A-Za-z])<name>(?![a-z])` with `re.I`, control `_by_<name>_` must fire. B1434 copies the library but REPLACES its `person` pattern with the same form (diff printed). The kits no longer type any person name: B1430's itemised-document pointer now names the project's own copy (`1_Project_Definition/Roles-UI-2026-11-06/ITEMISED-CHANGES.md`, sha256 prefix `6ba866d3e960fa9b`, 542 lines, measured) instead of the fleet-state path that held a name | B1431:145, B1432:78; HOLD 11 in each builder kit (B1430:62, B1431:84, B1432:54, B1433:60); B1434:20; B1430:69 |
| 8 | B1434 | Seat R202 everywhere (title, launch line, pane, Step-0 copy name, REFUSE 2, file name): R196 count 0, R202 count 6 (control: 6 R196 in the `.pre` copy). `pwd -P` is compared to `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI`. Late-INSERT fact rewritten to today's reads. HISTORY entries for #180 (if missing), #183, #184 only; **no #182 entry** (the 9 Nov B1375 stamp answer, `2026-11-09_B1375_slots.json`). Also fixed the minor "builders touch no `1_Project_Definition/**`" sentence, and Step 0 now orders REFUSE 1/2/4, folder, helper, REFUSE 3/5 | B1434:3, :5, :6, :9, :10, :17, :39, :44 |
| 9 | Copy-to destination | `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/Briefs/` does not exist; every builder kit now copies to `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/`, which exists (`ls -d`), holds the earlier NexusAI seat kits (e.g. `2026-11-06_B1317_SEAT-N101_...`) and is where every STATUS file already goes. The project `CLAUDE.md` names no brief folder (`grep -n -i 'Briefs'` reads 0, control: `CLARIFICATIONS` at :373); lanes.md:49 names `1_Project_Definition/Briefs/**` | B1430:65, B1431:87, B1432:57, B1433:63 |
| 10 | Placeholders | Four `____` lines per kit, READ-WHOLE last (counts below). No `@MAIN@` was added (the ruling keeps four slots); the literal main sha on line 1 is still true at 06:25:01 | each kit's `## Stamp` |

Other review findings: 1g, 2a-2e, 3 were PASS and are untouched. The B1433 sequencing check on `b1430/*` branches (review row B1433, 1d) is no longer needed, because S owns none of B's files and B owns none of S's. NOT changed (not HOLD reasons): B1431 throughput (57 keyword guesses), DRAFTER_RULES:59 vs C-190, `lanes.md:54`'s "-2 to -6" (the kit already says -2 to -8), the B1434 STATUS first-line mismatch (Step 0 placeholder vs `RECORDS B1434: RUNNING`), and `lanes.md` itself (read-only to me; `lanes.md:55` is now stale on the late-INSERT search, and B1434:17 says so).

## Partition

**The rule I applied (derivation program in my scratchpad, `derive.py`, run over the same inputs):** a ticket's named file outside its own lane is either (a) moved into that lane's OWNS, when no ticket of any other lane names it, so the ticket is homed wholly in one lane, or (b) the ticket is dropped, when another lane's own queue tickets also name that file. Two names are context only, written into the kits: `backend/server.js` in RD-798 (its server.js part is landed; the remainder is `learningManager.js`) and in RD-980 (its fix is in two test files). If either needs a byte of server.js, that item is NEEDS-SHARED.

- **Moved (13 files into S, 1 into F):** to S `backend/costCentreMap.js` (RD-767), `intentRouter.js` (RD-766, RD-909), `marketplaceJwt.js` (RD-445), `marketplaceStore.js` and `validators.js` (RD-769), `queryPreprocessor.js` (RD-766), `routes/feedback.js` and `routes/sustainability.js` (RD-958), `services/authEnforcement.js` (RD-366, RD-445), `services/riskSqlTemplates.js` (RD-876), `services/schedulers/healthSweeperScheduler.js` (RD-689), `services/sustainability/rowSource.js` (RD-331), `ticketStore.js` (RD-765), and `tests/e2e/rd436-r4-login-after-selfheal.browser.js` (RD-691, from F); to F `backend/services/riskAlertScheduler.js` (RD-396).
- **Dropped (19), each with its line in every builder kit's PARTITION ("Dropped from this sweep"):** S: RD-178, RD-188, RD-319, RD-569, RD-596, RD-768, RD-792, RD-806, RD-855, RD-892, RD-925, RD-927; T: RD-346 (feedback-attachments kept by S), RD-598 (rd486 kept by B); F: RD-117, RD-176, RD-280; B: RD-674, RD-745. Reasons per key are in the kit line (for example RD-768/RD-806: `backend/services/emailService.js` is also named by B's RD-805; RD-927/RD-892: `static/js/index.js` is also named by 13 F tickets).
- **Queues:** S 86 to 74, T 98 to 96, F 78 to 75, B 16 to 14. No ticket changed lane and none was added. Rows were renumbered inside each block; headers and the keyword-guess counts were updated (S 12 of 74, T 57 of 96, F 22 of 75, B 0 of 14).
- **Existing tests owned:** S 3, T 25, F 8, B 3 (listed in each OWNS block). The two that were named by two lanes went by the kits' text rule ("the first-named lane keeps the file"): `__tests__/rd486-ai-test-key-forwarding.test.js` to B (RD-590), and `__tests__/feedback-attachments.test.js` to S (RD-366), as the ruling also says.

### Partition program output (final run, 06:25:01 AEDT, main `3929b794`)

Input: `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/git/trees/3929b7946e2de85ce2ea312ac70bb64134a767e6?recursive=1` (985 blobs, `truncated` false). The program parses each kit's OWNS block and QUEUE table AS WRITTEN.

```
tree blobs 985 | truncated False
OWNS lines parsed: {'S': (25, 0, True), 'T': (35, 12, True), 'F': (17, 1, True), 'B': (4, 19, True), 'R': (1, 0, False)} (+, -, +new)
files claimed per lane: {'T': 248, 'R': 1, 'F': 114, 'S': 24, 'B': 81} | unclaimed: 517
FILES CLAIMED BY MORE THAN ONE LANE: 0 []
synthetic new rd<N> test paths claimed by other than exactly their lane: 0 []
owned-by-no-lane check scripts/verify-expected-counts.json in tree -> claimed by []
owned-by-no-lane check .github/workflows/deploy-demo.yml in tree -> claimed by []
queue sizes {'S': 74, 'T': 96, 'F': 75, 'B': 14} | keys in two kits: []
dropped from final_assignment: 19 ['RD-117', 'RD-176', 'RD-178', 'RD-188', 'RD-280', 'RD-319', 'RD-346', 'RD-569', 'RD-596', 'RD-598', 'RD-674', 'RD-745', 'RD-768', 'RD-792', 'RD-806', 'RD-855', 'RD-892', 'RD-925', 'RD-927'] | added: [] | changed lane: []
each builder kit's Dropped line names exactly the dropped set: {'S': True, 'T': True, 'F': True, 'B': True}
queued tickets naming a file outside their own lane: 0 []
CONTROL planted static/js/index.js into S -> ['S', 'F'] caught
CONTROL planted rd486 test into T -> ['T', 'B'] caught
CONTROL removed T's `- deploy-demo.yml` line -> claimed by ['T'] caught
CONTROL overlap count with the S plant: 1 (must be 1)
```

Result: **0 overlaps**. The planted-overlap control fires: one planted glob gives exactly 1 overlap. The "unclaimed 517" are the root docs, ops and data files nobody edits, plus the existing `__tests__` files that no queued ticket names. Under the kits' rule no lane may touch an unclaimed file.

### The program (stdlib, `python3 -I partition_check.py <tree.json>`)

```python
# Partition program for the redrafted NexusAI kits B1430-B1434 (stdlib, python3 -I).
# argv[1] = tree JSON from `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/git/trees/<sha>?recursive=1`
# It parses the ```OWNS-<L> block of each kit AS WRITTEN and the QUEUE table keys of each kit.
import json, re, sys, fnmatch, collections, glob
BR = '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/'
SW = BR + '2026-11-10_nexusai_sweep/'
KITS = {'S': 'B1430_SEAT-N114', 'T': 'B1431_SEAT-N115', 'F': 'B1432_SEAT-N116', 'B': 'B1433_SEAT-N117', 'R': 'B1434_SEAT-R202'}
d = json.load(open(sys.argv[1]))
assert d['truncated'] is False, 'tree truncated'
tree = [e['path'] for e in d['tree'] if e['type'] == 'blob']
treeset = set(tree)
blocks, queues, texts = {}, {}, {}
for L, tag in KITS.items():
    paths = [p for p in glob.glob(BR + '2026-11-10_' + tag + '_*.md') if '.pre' not in p]
    assert len(paths) == 1, (L, paths)
    t = open(paths[0]).read(); texts[L] = t
    m = re.findall(r'```OWNS-' + L + r'\n(.*?)\n```', t, re.S)
    assert len(m) == 1, ('OWNS block count', L, len(m))
    inc, exc, new = [], [], False
    for line in m[0].split('\n'):
        if line.startswith('+new '):
            new = True
        elif line.startswith('+ '):
            inc.append(line[2:].strip())
        elif line.startswith('- '):
            exc.append(line[2:].strip())
        else:
            raise SystemExit('unparsed line in OWNS-%s: %r' % (L, line))
    blocks[L] = (inc, exc, new)
    queues[L] = re.findall(r'^\| [ABCD]\d+ \| (RD-\d+) \|', t, re.M)
def claims(p, B=None):
    B = B or blocks
    out = []
    for L, (inc, exc, new) in B.items():
        hit = any(fnmatch.fnmatch(p, g) for g in inc) and not any(fnmatch.fnmatch(p, g) for g in exc)
        if not hit and new and p not in treeset:
            m = re.match(r'__tests__/rd(\d+)-', p)
            hit = bool(m) and ('RD-' + m.group(1)) in queues[L]
        if hit:
            out.append(L)
    return out
print('tree blobs', len(tree), '| truncated', d['truncated'])
print('OWNS lines parsed:', {L: (len(b[0]), len(b[1]), b[2]) for L, b in blocks.items()}, '(+, -, +new)')
per = collections.Counter(); multi = []
for p in tree:
    c = claims(p)
    for L in c: per[L] += 1
    if len(c) > 1: multi.append((p, c))
print('files claimed per lane:', dict(per), '| unclaimed:', sum(1 for p in tree if not claims(p)))
print('FILES CLAIMED BY MORE THAN ONE LANE:', len(multi), multi[:5])
# new test files: one synthetic NEW path per queued key must be claimed by exactly its lane
newbad = []
for L in 'STFB':
    for k in queues[L]:
        p = '__tests__/rd%s-zz-planted-new.test.js' % k[3:]
        c = claims(p)
        if c != [L]: newbad.append((p, c))
print('synthetic new rd<N> test paths claimed by other than exactly their lane:', len(newbad), newbad[:3])
# unowned
for p in ['scripts/verify-expected-counts.json', '.github/workflows/deploy-demo.yml']:
    print('owned-by-no-lane check', p, 'in tree' if p in treeset else 'NOT IN TREE', '-> claimed by', claims(p))
# queue keys disjoint and dropped keys absent
allk = collections.Counter(k for L in 'STFB' for k in queues[L])
print('queue sizes', {L: len(queues[L]) for L in 'STFB'}, '| keys in two kits:', [k for k, n in allk.items() if n > 1])
fa = json.load(open(SW + 'final_assignment.json')); tp = dict(json.load(open(SW + 'tickets_paths.json')))
orig = {L: sorted(k for k, l, b in fa if l == L) for L in 'STFB'}
dropped = sorted(set(k for L in 'STFB' for k in orig[L]) - set(allk), key=lambda x: int(x[3:]))
added = sorted(set(allk) - set(k for L in 'STFB' for k in orig[L]))
moved_lane = [k for L in 'STFB' for k in queues[L] if k not in orig[L]]
print('dropped from final_assignment:', len(dropped), dropped, '| added:', added, '| changed lane:', moved_lane)
dl = {L: set(re.findall(r'RD-\d+', texts[L][texts[L].find('Dropped from this sweep'):texts[L].find('\n', texts[L].find('Dropped from this sweep'))])) for L in 'STFB'}
print('each builder kit\'s Dropped line names exactly the dropped set:', {L: dl[L] == set(dropped) for L in 'STFB'})
# every queued ticket's named files lie in its lane (context-only names are stated in the kits)
CONTEXT = {('RD-798', 'backend/server.js'), ('RD-980', 'backend/server.js')}
viol = []
for L in 'STFB':
    for k in queues[L]:
        for p in tp.get(k, []):
            if p == 'scripts/verify-expected-counts.json' or (k, p) in CONTEXT: continue
            if claims(p) != [L]: viol.append((k, L, p, claims(p)))
print('queued tickets naming a file outside their own lane:', len(viol), viol[:5])
# controls: planted overlaps must be caught
def plant(L, g):
    B2 = {k: (list(v[0]), list(v[1]), v[2]) for k, v in blocks.items()}
    B2[L][0].append(g); return B2
c1 = claims('static/js/index.js', plant('S', 'static/js/index.js'))
c2 = claims('__tests__/rd486-ai-test-key-forwarding.test.js', plant('T', '__tests__/rd486-ai-test-key-forwarding.test.js'))
B3 = {k: (list(v[0]), [x for x in v[1] if not (k == 'T' and x == '.github/workflows/deploy-demo.yml')], v[2]) for k, v in blocks.items()}
c3 = claims('.github/workflows/deploy-demo.yml', B3)
print('CONTROL planted static/js/index.js into S ->', c1, 'caught' if len(c1) > 1 else 'NOT CAUGHT')
print('CONTROL planted rd486 test into T ->', c2, 'caught' if len(c2) > 1 else 'NOT CAUGHT')
print('CONTROL removed T\'s `- deploy-demo.yml` line -> claimed by', c3, 'caught' if c3 else 'NOT CAUGHT')
mm = sum(1 for p in tree if len(claims(p, plant('S', 'static/js/index.js'))) > 1)
print('CONTROL overlap count with the S plant:', mm, '(must be 1)')
assert len(c1) > 1 and len(c2) > 1 and c3 and mm == 1
```

## Checks on the redrafted kits (06:25 AEDT)

- **Name scan (underscore-aware):** `(?<![A-Za-z])(<the review's 11-name list>)(?![a-z])`, `re.I`. Hits: 0 in all five kits. Controls: `_by_<first>_`, `_by_<surname>_` and a third planted name all fire; the negative control (a longer word starting with the shortest name) does not.
- **Slots:** `/usr/bin/grep -c -E '_''_''_''_'` prints 4 in every kit (3 slots plus the last line). The last line of every kit is `READ-WHOLE-BY-TUESDAY: ____`. No `@@`/placeholder token is left (`@@CLOCK` count 0 in all five).
- **Levels in the launch lines:** S `opus`; T, F, B and R `sonnet`.
- **Stale paths:** `NexusAI/Briefs/` 0 in all five (control: `1_Project_Definition/Briefs/` 4 in each builder kit and 6 in B1434). The original `b774lib.py` is named once per kit, only as the `cp` source.
- **Jira (06:17:25):** `late INSERT` returns RD-219 only (Release Ready); `setQuickQuestions` returns RD-973 only; `ROLLBACK` returns 61; `( key = RD-798 )` returns 1; `zzqxnonexist` returns 0; RD-937 reads To Do.
- **Seat id:** R202 is used by no brief file name or content except REVIEW.md's proposal (control: R201 is found). The live pane list shows no NexusAI or R20x pane (an empty `tmux list-panes` filter; no positive control was run on it, so treat it as UNMEASURED).

## Diff line counts (`diff -u <kit>.pre-1110-review <kit>`)

| Kit | diff lines | removed | added | kit lines now |
|---|---|---|---|---|
| B1430 | 206 | 60 | 58 | 194 |
| B1431 | 309 | 88 | 108 | 243 |
| B1432 | 133 | 20 | 27 | 187 |
| B1433 | 132 | 20 | 45 | 130 |
| B1434 | 64 | 10 | 18 | 63 |

The large removed/added counts in B1431 and B1430 are mostly row renumbering after the dropped rows.

## Q for Tuesday (each has a default)

- Q1: the 19 dropped tickets. Default: re-place each one after the owning lane's branch on the shared file lands (a later sweep). The alternative is to split each into one part per lane.
- Q2: "a STOP for that item (NEEDS-SHARED)" is written as item-level: HELD, build nothing, continue with the queue, not a whole-seat `STOPPED:`. Default: keep. Change it to a seat STOP if that is what you meant.
- Q3: the B1434 rename (R196 to R202 in the file name) is a filesystem `mv` inside the briefs folder. Default: keep it. The `.pre-1110-review` copy keeps the old name for the record.

## UNMEASURED / disclosure

- No test, build or server was run. No branch was compared beyond what REVIEW.md did. The tree is origin main `3929b794`, which was still main at 06:25:01.
- The derivation that chose moves and drops used `tickets_paths.json`: the paths found in ticket text that match the tree. A READ-PATH-FIRST ticket may still turn out to need another lane's file, and the kits' keyword rule covers that.
- Outside the fences: none. Scratch programs and fetched files (`tree.json`, workflow copies, the b774 scratch copy) live in my session scratchpad. Nothing was written into the NexusAI project. I did not read `_ledger.md`, ran no `decision_queue.sh`, and printed no token.
