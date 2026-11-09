# Generator + disjointness proof for lanes.md. Inputs are read-only dumps made earlier in this sweep (Jira pager, GitHub GET).
# Run: python3 -I build_lanes.py <scratch dir> <out dir>
import json,re,sys,fnmatch,itertools,collections,subprocess
S=sys.argv[1].rstrip('/')+'/'; OUT=sys.argv[2].rstrip('/')+'/'
def jl(p): return json.load(open(S+p))
def prs(p): return json.loads(open(S+p).read().replace('][',','))
J={'MPSCALC':jl('MPSCALC.json'),'PCOMP':jl('PCOMP.json')}
TREE={'MPSCALC':[x['path'] for x in jl('mps_tree.json')['tree'] if x['type']=='blob'],
      'PCOMP':[x['path'] for x in jl('pc_tree.json')['tree'] if x['type']=='blob']}
PR={'MPSCALC':prs('mps_prs.json'),'PCOMP':prs('pc_prs.json')}
def hits(pre):
    h={}
    for p in PR[pre]:
        if not p.get('merged_at'): continue
        ti=p['title'] or ''; tx=ti+' '+(p.get('body') or '')
        for m in set(re.findall(pre+r'-(\d+)',tx)):
            h.setdefault(int(m),[]).append((p['number'],'title' if (pre+'-'+m) in ti else 'body'))
    return h
H={'MPSCALC':hits('MPSCALC'),'PCOMP':hits('PCOMP')}
def pr_note(pre,k):
    v=H[pre].get(k,[]); 
    return ', '.join('#%d(%s)'%(n,w) for n,w in v[-3:]) if v else 'no merged PR names it'
LANES=[
# ---------------- MPS ----------------
dict(id='M1',proj='MPSCALC',title='Web unit-test pins (test only)',fresh=[369],cond=[334,198],
 owned=['web/src/screens/bom/PurchaseBomEditor.test.tsx','web/src/screens/bom/PriceReason.test.tsx','web/src/screens/FleetGrid*.test.tsx','web/src/api/stub/stubApi.test.ts'],
 notown='web/e2e/**, web/src/feedback/**, web/src/api/generated/**, every non-test file under web/src',
 shape='369: the five rows that time out at the 5 s default under whole-suite load: make them wait on state or give the rows a stated budget; test only, no product byte. 334 and 198: read the landed PRs first (conditional).',
 checks='web job: `npm ci`, `npm run lint`, `npm test` (from web/); no product file changes so the build step is unaffected',size='S'),
dict(id='M2',proj='MPSCALC',title='Playwright e2e repairs (test only)',fresh=[96,135],cond=[297],
 owned=['web/e2e/**','web/playwright.config.ts'],
 notown='web/src/**, web/package.json, web/package-lock.json',
 shape='96: four stub-mode specs red as shipped (POST /api/v1/quotes 502 from the Vite proxy with no API behind it): the ticket measured that a synthetic API base turns them 3/3 green. 135: smoke.spec.ts red at :23 before the proposal; press Short-form first at :61-66 (ticket text). 297: exact nav list and the Proposal link locator (conditional: PR #90 body names it).',
 checks='e2e is NOT in CI (ticket 334 text: "e2e, which is not part of CI"); the seat runs the named specs locally 3 of 3; web job lint + `npm test` stay green; UNMEASURED whether `npm run lint` covers web/e2e',size='M'),
dict(id='M3',proj='MPSCALC',title='.NET test-only pins A (template isolation, care key)',fresh=[380,221],cond=[381],
 owned=['tests/MpsCalc.Api.Tests/TemplateIsolationTests.cs','tests/MpsCalc.Api.Tests/CareKeyPatternApiTests.cs'],
 notown='src/**, every other tests/ file',
 shape='380: the format guard is quiet on four forms of an earlier hole; PR #156 pinned "two line-break forms" so read what remains. 221: rename or reshape the synthetic care key constant at CareKeyPatternApiTests.cs:15 so a generic-key scanner does not match it (or an allow-list entry, which would be a repo-root file: do not; rename). 381 conditional (PR #156 title names it).',
 checks='dotnet job: `dotnet build MpsCalc.slnx -c Release` (0 warnings) then `dotnet test MpsCalc.slnx -c Release --no-build`',size='S'),
dict(id='M4',proj='MPSCALC',title='.NET test-only pins B (governed edges, refusal order, walk survivors)',fresh=[340,341,324,333],cond=[310],
 owned=['tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs','tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs','tests/MpsCalc.Api.Tests/QuoteRefusalOrderGuard.cs','tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs','tests/MpsCalc.Api.Tests/LaneM4*.cs'],
 notown='src/**, every other tests/ file (M3, M5, M6, M11 own theirs)',
 shape='340/341: two more rows and six pins in the edges file (gate text: tests only). 324: three rows (non-document exception at store load not read as unavailable; CannotOpen operator line; last body-refusal branch). 333: the edit-path twin of the fleet-below-limit row and the other pins in QuoteRefusalOrder*.cs. New rows may go in new files named LaneM4*.cs. 310 conditional (PR #99 body names it).',
 checks='dotnet job: Release build 0 warnings + `dotnet test`; each new pin must also turn red under the ticket\'s named mutant (red-first)',size='M'),
dict(id='M5',proj='MPSCALC',title='Source lifecycle and reference-document validator (product + tests)',fresh=[331,99],cond=[189,92,90],
 owned=['src/MpsCalc.Api/Sources/**','src/MpsCalc.Import/Validation/**','tests/MpsCalc.Api.Tests/LaneM5*.cs'],
 notown='src/MpsCalc.Api/Quotes/**, src/MpsCalc.Api/Contracts/**, src/MpsCalc.Api/Inventory/**, tests/MpsCalc.Api.Tests/SourceLifecycleTests.GovernedNullClassEdges.cs (M4)',
 shape='331: ReferenceDocumentValidator.cs:160/:162/:166/:203 throw on a null software product or null cell link; skip a null product in the term-gap check and treat a null link as does-not-agree (gate fix shape), so the existing REFERENCE_DATA_REJECTED refusal answers instead of 500. 99: SemaphoreSlim.WaitAsync(remaining) plus await Task.Delay(25) in the lock poll, bound counted from arrival (ticket fix shape). 189/92/90 conditional: PRs #100 and #29 name them.',
 checks='dotnet job; red-first rows for the 15 shapes in 331',size='M'),
dict(id='M6',proj='MPSCALC',title='Feedback backend hardening (product + tests)',fresh=[97,102,122,124,125],cond=[],
 owned=['src/MpsCalc.Api/Feedback/**','tests/MpsCalc.Api.Tests/Feedback*.cs'],
 notown='web/src/feedback/**, src/MpsCalc.Api/Contracts/**',
 shape='97: overlap guard gets the overlay NFC and link-follow fixes (FeedbackStore.cs RefuseOverlaps). 102: one lock scope for the StateOf read and SaveTicket (FeedbackEndpoints.cs:223/:232). 122: nosniff, no-store and the sandbox CSP at the top of Download before the role check. 124: write .bin files outside the lock, re-check the key under it. 125: Load refuses or logs a second (caller,key) and keeps the earliest by submittedAt. Left out on purpose: 121 (the unreadable-file sentence is the product owner\'s words call), 123 (needs a setting).',
 checks='dotnet job; one regression test per row as the ticket states',size='M'),
dict(id='M8',proj='MPSCALC',title='Docs and runbook sentences',fresh=[200,225],cond=[178,195,207],
 owned=['docs/DEMO.md','docs/IMPORTER.md','docs/ENGINE.md','docs/RECONCILIATION.md','ROOT:SETUP_RUNBOOK.md'],
 notown='docs/API.md, docs/api/openapi.json (M11), web/src/api/generated/**',
 shape='200: IMPORTER.md:112,:117 care-row counts (262 vs 294) re-measured and the A3 (23/8) and A4 (25/22) gaps explained, counts only, from the local price-book store (never paste prices). 225: SETUP_RUNBOOK.md (project root, outside the repo) names the app client id and hosted host variables, names only. 178/195/207: conditional, PRs #47, #105, #84 name them.',
 checks='no code: CI untouched; the seat re-reads each sentence at source; python job unaffected',size='S'),
dict(id='M9',proj='MPSCALC',title='Infra and script follow-ups (no deploy, no az)',fresh=[119,201,205],cond=[203],
 owned=['infra/tests/**','scripts/entra_apps.py','scripts/package.sh','scripts/tests/**'],
 notown='scripts/deploy-from-ci.sh, scripts/deploy-package.py, infra/main.bicep, infra/modules/**, .github/**',
 shape='119: test_infra.py:4,:59 stop falling back to `az bicep build` under a no-az hold (skip is forbidden by the file\'s own rule: every test FAILS if no bicep, so state the BICEP env route). 201: entra_apps.py:172,:174,:356-358 look the group up before the first write; the script is edited and tested against fakes, never run against Entra. 205: package.sh:45 guard words name the fix, or package from a clean output directory.',
 checks='python job: `for t in tools/demo/test/test_*.py infra/tests/test_*.py scripts/tests/test_*.py; do python3 -I "$t"` (ci.yml lines 80-91); package job `bash scripts/package.sh "$(git rev-parse HEAD)" --out ...`',size='S'),
dict(id='M10',proj='MPSCALC',title='Readiness sentence and parity proof',fresh=[302],cond=[295,207],
 owned=['src/MpsCalc.Engine/Readiness/**','tests/MpsCalc.Engine.Tests/ReadinessTests.cs','src/MpsCalc.Import/Parity/**','tools/MpsCalc.ImportCli/**','tests/MpsCalc.Import.Tests/LaneM10*.cs'],
 notown='src/MpsCalc.Engine/Calculation/**, src/MpsCalc.Api/**, docs/**',
 shape='302: ParityProof.cs:189-190 compare the (device,SKU) multiset per sheet, not counts, so a count-preserving swap reads DISAGREE. 295 (conditional): sentence only per the 10-20 coordinator ruling quoted in the ticket (raw line count stays; no behaviour change).',
 checks='dotnet job',size='S'),
dict(id='M11',proj='MPSCALC',title='Api contract and quote validation (product + contract copies)',fresh=[368,378,169],cond=[358,325,338,339],
 owned=['src/MpsCalc.Api/Contracts/**','src/MpsCalc.Api/Quotes/**','docs/API.md','docs/api/openapi.json','web/src/api/generated/**','tests/MpsCalc.Api.Tests/LaneM11*.cs'],
 notown='src/MpsCalc.Api/Sources/**, src/MpsCalc.Api/Feedback/**, tests named in M3/M4',
 shape='368: add the purchase recurring projection to the Api result DTO, formed from the engine figures, omitted when the engine omits it, restricted like the other cost and GP members; docs/API.md and openapi.json and the generated copies move with it (web `sync-contract` script). 378: one attribute or one row (ticket offers both; the gate recorded "nothing today"). 169: a field beside lineMarkupsOverlayVersion naming the source versions. 325/338: main already carries MaxWalkEntriesListed = 20 and per-walk counters (PurchaseValidation.cs:32,:131-165, control: constant found), so first confirm the tickets are residual-free and hand them to the records lane; 339 is a measurement. 358 conditional: PR #150 title names it.',
 checks='dotnet job; web job (`npm run lint`, `npm test`) because the generated copies change; web test "snapshot equals contract, schema.ts equals generator output" is already in main (PR #147)',size='L'),
# ---------------- Composer ----------------
dict(id='C1',proj='PCOMP',title='Change-report footer model',fresh=[120,121,123],cond=[23],
 owned=['packages/renderers/src/change-report.ts','packages/renderers/src/pdf-fit.ts','packages/renderers/test/change-report.test.ts'],
 notown='packages/renderers/src/document-pdf.ts and every other renderer file, DEPLOY.md, packages/db/**',
 shape='120: split the first line with the PDF writer\'s own line-breaking rules before the model counts rows; rows for bracket-space and tab runs (ticket text; the gate wrote it in prose, not ruled). 121: measure a tab as the writer draws it. 123: size the footer by the real page count (a measurement first; the ticket proposes no Done-when, so Tuesday writes one). 23 conditional: PR #113 changed change-report.ts after it was filed. The look (three dots) is Kam\'s to approve before any deploy; this lane builds and does not deploy.',
 checks='scripts/ci.sh step "node: lint, format, typecheck, build, test (--network none)" (needs docker, so run by the seat); hosted: CodeQL `Analyze (javascript-typescript)` and `Analyze (csharp)` on the PR (Composer has no ci workflow file: measured, tree has no .github path and workflows list is Dependabot + CodeQL only)',size='L'),
dict(id='C2',proj='PCOMP',title='Engine timing test under CPU cap',fresh=[114],cond=[62],
 owned=['packages/engine/test/performance.test.ts','apps/web/src/screens/b116-s10-verify-dom.test.tsx'],
 notown='packages/engine/src/**, apps/web/src/** other than the one test file',
 shape='114: the median-of-7 row times out at 5000 ms in the CI image under a CPU cap; raise that row\'s timeout or budget, or run it outside the shared pool (gate fix shape; test only, no product byte). 62 conditional: PR #90 body names it.',
 checks='scripts/ci.sh node step; the row green in the same cells the ticket measured',size='S'),
dict(id='C3',proj='PCOMP',title='DEPLOY.md and the db command-guard tests',fresh=[113,117],cond=[98,116],
 owned=['DEPLOY.md','packages/db/test/b616-deploy-commands.db.test.ts','packages/db/test/b778-route-b-script-complete.db.test.ts'],
 notown='packages/db/migrations/**, scripts/**, any other db test',
 shape='113: name the four remaining row 8 pins or say the paragraph names only the words (b778 row 8, title at :657). 117: say the refusal without the pg_restore version (DEPLOY.md:263 and the row title :769). 98 and 116 conditional: PRs #111 and #114 name them in their titles.',
 checks='scripts/ci.sh db step (migrations, RLS, tests in a throwaway postgres; docker) and node step; PR #118 type-checks the db test files in CI so the new rows must type-check',size='S'),
dict(id='C4',proj='PCOMP',title='Expert Discovery typed sub-answer (latent)',fresh=[12],cond=[],
 owned=['apps/web/src/screens/Discovery.tsx','apps/web/src/screens/LaneC4*.test.tsx'],
 notown='apps/api/**, packages/api-contract/**, apps/web/src/screens/w3/**',
 shape='12: typedDraftFor writes every declared sub-answer at the engagement level, so a device-group sub-answer cannot be answered per group (the API refuses with 400 since B30). Latent: both content releases declare 0 such sub-answers. Red-first test with the synthetic fixture\'s D-013, then per-group keying. The ticket says code-read only: Tuesday confirms the screen is not product-owner-look territory.',
 checks='scripts/ci.sh node step',size='M'),
]
# records lane (no repo paths)
REC_NOTE='R1 (MPS records) and R2 (Composer records) are Jira/BACKLOG/C-entry work in the project root, not repo files; they own no repo path.'
# ---------- classification ----------
def nonepic(pre): return [i for i in J[pre] if i['fields']['status']['name']!='Done' and i['fields']['issuetype']['name']!='Epic']
def kn(i): return int(i['key'].split('-')[1])
EXC={'MPSCALC':{114:'product owner wants it printable? (ticket: no fix proposed)',121:'words call (product owner)',123:'needs a setting (coordinator call)',130:'print look (product owner eyes)',131:'customer-facing design decision',132:'mock gap / design',133:'records-repo process, no product code',162:'hosted overlay read first (ticket) and PR #59 title names it',163:'PR #58 title names it; under-load half stays open',217:'two options (refuse boot or 503), not chosen',223:'deploy-seat runbook against the hosted site',288:'two designs offered, not chosen',306:'layout choice (3 options), looks',314:'ticket says the choice is open and unruled',349:'needs an SDK that carries the tie; Note only',359:'PR #155 landed the engine half; Api and screen halves wait on the 358 shape',360:'needs the coordinator\'s confirmation first (ticket)',364:'held for the product owner\'s word pack',371:'word pack (ticket)',372:'deploy-side store path',383:'DATED 2026-11-12 (Dependabot code-scan question): not before its date'},
     'PCOMP':{66:'tied to held PR #85; product edit deferred',67:'branch of held PR #85',15:'Low, unmeasured: no defect shown',11:'not small; contract bump',9:'needs the VM / deploy',10:'deploy scripts live on the VM',13:'environment (Docker host)',16:'environment (Docker host)',18:'found on the demo VM',21:'unmeasured, restore on the VM',25:'demo VM overlay',26:'registry digest risk, hosted pull',27:'dev volume ownership, machine state',28:'anonymous pull UNMEASURED hosted',127:'each item waits on a go or the product owner\'s words (ticket)',64:'records only (Note)',65:'operator power Note for the product owner',82:'decision (dates in UTC words)',83:'Blocker found by a seat, needs design',93:'demo way-back, coordinator accepted; deploy side'}}
def classify(pre):
    laneof={}
    for L in LANES:
        if L['proj']!=pre: continue
        for k in L['fresh']: laneof[k]=('FRESH',L['id'])
        for k in L['cond']: laneof.setdefault(k,('COND',L['id']))
    out=collections.OrderedDict()
    for i in sorted(nonepic(pre),key=kn):
        k=kn(i); f=i['fields']; lb=set(f['labels']); t=f['summary']
        if k in laneof: c=laneof[k][0]+' '+laneof[k][1]
        elif k in EXC[pre]: c='EXCL explicit: '+EXC[pre][k]
        elif 'question-for-kam' in lb: c='EXCL needs the product owner (question-for-kam)'
        elif 'needs-ruling' in lb or 'needs-kam' in lb: c='EXCL needs a ruling (label)'
        elif 'held' in lb: c='EXCL held (label)'
        elif lb & {'phase-2','later-phase','lane-later'}: c='EXCL later phase'
        elif any(l.startswith('lane-v') for l in lb): c='UNASSESSED feature lane V0-V11 (plan b308; descriptions not read)'
        elif t.startswith('Sample policy document'): c='UNASSESSED sample-policy L-lane rows (seed; wait on reviewer answers per pickup line 37, RELAYED)'
        elif pre=='MPSCALC' and k<=85: c='UNASSESSED seed rows 16-85 (spec seed 09-30)'
        elif H[pre].get(k) and any(w=='title' for _,w in H[pre][k]): c='RECORDS: a merged PR title names it (read PR vs ticket, then move or comment)'
        else: c='UNASSESSED (description not read)'
        out[k]=c
    return out
CL={p:classify(p) for p in ('MPSCALC','PCOMP')}
# records candidates among lane conds also counted in COND. Add explicit RECORDS list: title-hit tickets anywhere
def rec_list(pre):
    return sorted(k for k,i in ((kn(i),i) for i in nonepic(pre)) if any(w=='title' for _,w in H[pre].get(k,[])))
# ---------- disjointness proof ----------
def stem(g): 
    m=re.search(r'[*?\[]',g); return g if not m else g[:m.start()]
def matches(g,paths):
    if g.startswith('ROOT:'): return [g]
    if g.endswith('/**'): return [p for p in paths if p.startswith(g[:-2])]
    return [p for p in paths if fnmatch.fnmatchcase(p,g)]
def may_overlap(a,b,paths):
    if a.startswith('ROOT:') or b.startswith('ROOT:'): return a==b
    if set(matches(a,paths))&set(matches(b,paths)): return True
    sa,sb=stem(a.replace('/**','/')),stem(b.replace('/**','/'))
    wa=('*' in a or '?' in a or a.endswith('/**')); wb=('*' in b or '?' in b or b.endswith('/**'))
    if not wa and not wb: return a==b
    return sa.startswith(sb) or sb.startswith(sa)   # conservative: nested stems with a wildcard may collide
def prove(pre,lanes,extra=None):
    paths=TREE[pre]; res=[]; bad=[]
    for A,B in itertools.combinations(lanes,2):
        for ga in A['owned']:
            for gb in B['owned']:
                if may_overlap(ga,gb,paths): bad.append((A['id'],ga,B['id'],gb))
    return bad
proof=[]
for pre,name in (('MPSCALC','MPS'),('PCOMP','Composer')):
    ls=[L for L in LANES if L['proj']==pre]
    bad=prove(pre,ls)
    zero=[(L['id'],g) for L in ls for g in L['owned'] if not g.startswith('ROOT:') and 'Lane' not in g and not matches(g,TREE[pre])]
    pairs=len(list(itertools.combinations(ls,2)))
    # negative control: a lane that deliberately overlaps must be caught
    ctl=prove(pre,[dict(id='X',owned=[ls[0]['owned'][0]]),dict(id='Y',owned=[ls[0]['owned'][0]])])
    par=ls[0]['owned'][0].rsplit('/',1)[0]+'/**'
    ctl2=prove(pre,[dict(id='X',owned=[par]),dict(id='Y',owned=[ls[0]['owned'][0]])])
    # ticket uniqueness
    cnt=collections.Counter(k for L in ls for k in L['fresh'])
    dup=[k for k,v in cnt.items() if v>1]
    proof.append((name,len(ls),pairs,bad,zero,len(ctl)>0,len(ctl2)>0,dup))
# conservation
cons=[]
for p in CL:
    n=len(nonepic(p)); cnt=collections.Counter(v.split(':')[0].split(' ')[0] if not v.startswith('UNASSESSED') else 'UNASSESSED' for v in CL[p].values())
    cons.append((p,n,len(CL[p]),dict(cnt)))
# ---------- render ----------
o=[]
w=o.append
now=subprocess.run(['date','+%Y-%m-%d %H:%M:%S %Z'],capture_output=True,text=True).stdout.strip()
w('# MPS Calculator and Security Composer: lanes agents can run now (sweep, read-only)\n')
w('Drafted at %s (`date` print in the generator run). Drafter read only: Jira boards by the project\'s own `.env` in-process (no token printed), `gh api -X GET` under each project\'s `.gh-config`, `decision_queue.sh list` (read-only), the pickup file lines for MPS/Composer. No git, board, mail, az, ssh, docker or hosted-host action. Local checkouts are stale (MPS `2_Project_Files` HEAD 7f6ca4c0 is B05; Composer 0b2fca43), so every code fact below is from origin: MPS main `31234f5f` (committed 2026-11-08T12:28:11Z), Composer main `a54250f4` (2026-11-03T20:16:17Z), both equal to the morning sweep\'s reads.\n'%now)
w('## BLUF\n')
n1=len(nonepic('MPSCALC')); n2=len(nonepic('PCOMP'))
def cnt(pre,pfx): return sum(1 for v in CL[pre].values() if v.startswith(pfx))
w('- **MPS Calculator (main 31234f5f, 0 open PRs): %d lanes M1-M6, M8-M11 (M7 dropped: its only ticket, 194, is already named by merged PR #79), %d fresh tickets, %d conditional on a prior-work read.** Lanes are pairwise path-disjoint by program (section Disjointness), so all can run at once; the machine is the limit (each dotnet or web lane is a full CI-equivalent run). Size: S=5, M=4, L=1.'%(sum(1 for L in LANES if L['proj']=='MPSCALC'),len({k for L in LANES if L["proj"]=="MPSCALC" for k in L["fresh"]}),len({k for L in LANES if L["proj"]=="MPSCALC" for k in L["cond"]})))
w('- **Security Composer (main a54250f4, 3 open PRs all held): %d lanes C1-C4, %d fresh tickets, %d conditional.** C1 is the footer fix the 11-03 card left as a ticket; it changes a PDF look, so it builds and does not deploy.'%(sum(1 for L in LANES if L['proj']=='PCOMP'),len({k for L in LANES if L["proj"]=="PCOMP" for k in L["fresh"]}),len({k for L in LANES if L["proj"]=="PCOMP" for k in L["cond"]})))
w('- **OWED LANDINGS: none.** MPS: 0 open PRs (`pulls?state=open` empty; control: the same call on Composer returns 3 and `pulls?state=closed` on MPS returns #166 at the top). The last round-cap card, `mps-106-price-guard-round-cap-1106`, reads `ruled a` and `delivered: MPSCALC-386; 10 rows;` in `decision_queue.sh list`, with #166 merged 2026-11-08T12:28:11Z. Composer: the open PRs are #85 (HOLD), #86 and #91 (Dependabot, held by the product owner\'s 11-04 note), nothing to land. The 11 open cards on the store are none of MPS or Composer except `composer-l05-setup-card-too-1014` (settled by the product owner\'s 10-23 email; the pickup says do not re-raise).')
rl1=rec_list('MPSCALC'); rl2=rec_list('PCOMP')
w('- **OWED RECORDS (the real backlog here): Jira lags the merged PRs.** %d open MPS tickets and %d open Composer tickets are named in the TITLE of a merged PR (list in R1 and R2). Examples read at source: MPSCALC-358 (PR #150 title), -359 (#155), -377 (#151), -381 (#156), -382 (#157), -98 (#34), -178 (#47), -189 (#100), -194 (#79), -203 (#81). Some are residual-by-design (PR #155 said "MPSCALC-359 stays open for the Api and screen halves"), so each needs a read of PR against ticket, not a bulk close. A records seat per project owns it; no repo path is touched.'%(len(rl1),len(rl2)))
w('- **EXCLUSIONS (counts, program-made, conservation checked below):** MPS %d open non-epic tickets: %d in lanes, %d records, %d need the product owner (question-for-kam), %d need a ruling (label), %d explicit with a reason, %d later phase, %d feature lanes V0-V11 not assessed, %d seed rows not assessed, %d other not read. Composer %d open non-epic: %d in lanes, %d held (label), %d need the product owner or a reviewer, %d explicit, %d sample-policy rows not assessed, %d other not read.'%(
 n1,cnt('MPSCALC','FRESH')+cnt('MPSCALC','COND'),cnt('MPSCALC','RECORDS'),cnt('MPSCALC','EXCL needs the product owner'),cnt('MPSCALC','EXCL needs a ruling'),cnt('MPSCALC','EXCL explicit'),cnt('MPSCALC','EXCL later'),cnt('MPSCALC','UNASSESSED feature'),cnt('MPSCALC','UNASSESSED seed'),cnt('MPSCALC','UNASSESSED (desc'),
 n2,cnt('PCOMP','FRESH')+cnt('PCOMP','COND'),cnt('PCOMP','EXCL held'),cnt('PCOMP','EXCL needs'),cnt('PCOMP','EXCL explicit'),cnt('PCOMP','UNASSESSED sample'),cnt('PCOMP','UNASSESSED (desc')))
w('- **Dated item:** 2026-11-12 Dependabot code-scan question (MPSCALC-383 and -384 area, Composer #86/#91): excluded and untouched. MPSCALC-383 is listed as an explicit exclusion; MPSCALC-384 is Done.')
w('- **Decision store:** `decision_queue.sh list` read OK at drafting (%s). The MPS card `mps-106-price-guard-round-cap-1106` default (a) is already executed: `ruled a` @ 2026-11-08T20:31 and delivered. Nothing on the Composer side is pending a card.\n'%now)
w('## Facts every lane copies (sources)\n')
w('- **Landing (both projects):** Tuesday opens and lands PRs; seats push their branch only. MPS: `--squash --match-head-commit <sha>` after hosted checks plus CodeQL (`NEXT-PICKUP-TUESDAY.md` line 32, MPS #112; MPS CLAUDE.md "Datasec CodeQL rule": "Seats push a branch only; Friday opens the PR and merges once CodeQL is green"). Composer: same squash form (`NEXT-PICKUP-TUESDAY.md` line 31, Composer #92). Not deployed either way: Composer "deploys only on Kam\'s card" (pickup line 24); MPS has no deploy without a brief.')
w('- **MPS CI predicate (`.github/workflows/ci.yml` at main 31234f5f):** job `dotnet`: `dotnet build MpsCalc.slnx -c Release` then `dotnet test MpsCalc.slnx -c Release --no-build` ("0 warnings" is in the job name); job `web`: `npm ci`, `npm run lint`, `npm test`, `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`; job `python`: every `tools/demo/test/test_*.py infra/tests/test_*.py scripts/tests/test_*.py` under `python3 -I`, one failing file fails the step; job `package`: `bash scripts/package.sh`. Pass = all four success on the PR head.')
w('- **Composer CI predicate:** the repo has NO ci workflow (tree: no `.github` path; `actions/workflows` lists Dependabot Updates and CodeQL only; control: both calls returned). Hosted pass = CodeQL `Analyze (javascript-typescript)` and `Analyze (csharp)` success (main run at a54250f4 success on both, jobs read). The test predicate is local: `scripts/ci.sh` (secret scan, node lint/format/typecheck/build/test in the CI image with no network, db tests in a throwaway postgres, bridge tests, stack checks) which needs docker, so the seat runs it.')
w('- **Standing for every lane kit:** PRIOR-WORK CHECK (a READY without a PRIOR WORK section is returned), because the sweep found Jira lagging merged PRs (above); no message to any human; never delete; red-first for each product change; Tuesday writes the Done-when where a ticket gives none.\n')
for pre,title in (('MPSCALC','MPS Calculator lanes'),('PCOMP','Security Composer lanes')):
    w('## %s\n'%title)
    for L in [x for x in LANES if x['proj']==pre]:
        w('### %s: %s (size %s)\n'%(L['id'],L['title'],L['size']))
        w('- **Project / repo:** %s\n- **Fresh tickets (no merged PR names them):** %s\n- **Conditional (a merged PR names them; read the PR first):** %s'%(
          'Datasec / MPS Commercial Calculator, datasecau/MPS-Commercial-Calculator' if pre=='MPSCALC' else 'Datasec / Security Composer, datasecau/Datasec-Security-Composer',
          ', '.join('%s-%d'%(pre,k) for k in L['fresh']) or 'none',
          '; '.join('%s-%d [%s]'%(pre,k,pr_note(pre,k)) for k in L['cond']) or 'none'))
        w('- **Owned paths:** '+'; '.join('`%s`'%g for g in L['owned']))
        w('- **NOT yours:** '+L['notown'])
        w('- **Fix shape:** '+L['shape'])
        w('- **Proving checks:** '+L['checks']+'\n')
w('## Records lanes (no repo path; owed work)\n')
w(REC_NOTE+'\n')
for pre,rid,keys in (('MPSCALC','R1',rl1),('PCOMP','R2',rl2)):
    w('### %s: %s records read, PR against ticket\n'%(rid,'MPS' if pre=='MPSCALC' else 'Composer'))
    w('Tickets whose merged PR title names them (Jira status Backlog at drafting; instrument: PR title regex over `pulls?state=closed&per_page=100` paginated to the end, %d PRs, control: PR numbers run from #%d to #%d with no gap in the first/last):\n'%(len(PR[pre]),min(p['number'] for p in PR[pre]),max(p['number'] for p in PR[pre])))
    w('; '.join('%s-%d [%s]'%(pre,k,', '.join('#%d'%n for n,wd in H[pre][k] if wd=='title')) for k in keys)+'\n')
    w('Fix shape: for each, read the PR and the ticket\'s Done-when; move to Done with a facts-only comment where met, comment and keep open where the PR says a half remains. Size: M. Needs Jira writes, so the kit must grant them.\n')
w('## Exclusions (reasons; counts above)\n')
for pre,name in (('MPSCALC','MPS'),('PCOMP','Composer')):
    w('**%s explicit exclusions (read at source):**\n'%name)
    w('; '.join('%s-%d (%s)'%(pre,k,v) for k,v in sorted(EXC[pre].items()) if k in CL[pre])+'\n')
    cc=collections.Counter(v if not v.startswith('EXCL explicit') else 'EXCL explicit' for v in CL[pre].values() if not v.startswith(('FRESH','COND')))
    w('Category counts: '+'; '.join('%s = %d'%(k,v) for k,v in cc.most_common())+'\n')
w('Not assessed is not excluded: the feature lanes V0-V11 (MPS plan b308) and the Composer sample-policy L-lane rows are large; their descriptions were not read, so no claim is made about whether they need a ruling. A separate sweep should read them.\n')
w('## Disjointness (program output)\n')
w('Program: `build_lanes.py` beside this file. It expands each lane\'s owned globs against the origin tree (MPS 767 paths at main 31234f5f; Composer 1,037 at a54250f4, `truncated=false` both), then for every lane pair checks (a) a tree path matched by both, (b) literal equality, (c) nested stems when a wildcard is involved (conservative: may-overlap). Controls: a deliberately duplicated lane and a deliberately nested lane must be flagged, and every non-new glob must match at least one tree path.\n')
w('| Project | Lanes | Pairs checked | Overlaps found | Globs matching 0 paths (non-new) | Control: duplicate flagged | Control: nested flagged | Ticket in 2 lanes (fresh) |\n|---|---|---|---|---|---|---|---|')
for name,nl,pairs,bad,zero,c1,c2,dup in proof:
    w('| %s | %d | %d | %d %s | %s | %s | %s | %s |'%(name,nl,pairs,len(bad),bad[:3] if bad else '',zero if zero else '0',c1,c2,dup if dup else 'none'))
w('\nConservation of the ticket census (every open non-epic ticket in exactly one class):\n')
for p,n,m,c in cons: w('- %s: open non-epic %d, classified %d, classes %s'%(p,n,m,c))
w('\nLimits of the proof: it proves path-disjointness of what the lanes OWN, from main\'s tree; it cannot see a file a seat decides to touch outside its list (the kit must say "any other path: STOP and ask"), and new files named by pattern (`LaneM4*.cs` and so on) are disjoint by their distinct stems only. M8 owns two sentences in files M11 would otherwise share (`docs/API.md`): API.md belongs to M11 alone.\n')
w('## Not done / UNMEASURED\n')
w('- Machine load for running up to 9 MPS lanes beside 4 Composer lanes: UNMEASURED; the dotnet job is 20 minutes on a hosted runner.\n- Per-ticket readiness of the %d UNASSESSED MPS and %d UNASSESSED Composer rows: not read.\n- Whether `npm run lint` covers `web/e2e` (M2): UNMEASURED.\n- Whether the 29 title-named MPS tickets are residual-free: not read ticket-by-ticket (R1\'s job).\n'%(sum(1 for v in CL['MPSCALC'].values() if v.startswith('UNASSESSED')),sum(1 for v in CL['PCOMP'].values() if v.startswith('UNASSESSED'))))
open(OUT+'lanes.md','w').write('\n'.join(o)+'\n')
print('written',len('\n'.join(o)))
for r in proof: print(r[:3],'bad',r[3],'zero',r[4],'ctl',r[5],r[6],'dup',r[7])
for c in cons: print(c)
