import json, re, subprocess, itertools, sys

S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/98c591ba-dd19-4b5b-822b-2512baf59468/scratchpad'
CL = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/drafter-lanes1700'
TIP = 'bd6697e079fce41db6b21e094a9eddb3d0e1d08e'
T12 = TIP[:12]
BR = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged'
REF = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-28_secuura-lanes-1700'
D = 'Blockchain/Dev/'
DOC1 = 'Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html'
DOC2 = 'Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
TODAY = '2026-10-28'

tickets = {x['identifier']: x for x in json.load(open(S + '/open.json'))}


def rc(path):
    return subprocess.run(['git', '-C', CL, 'cat-file', '-e', TIP + ':' + path], capture_output=True).returncode


def tstate(k):
    x = tickets[k]
    a = (x['assignee'] or {}).get('email', 'unassigned')
    return f"{k} state {x['state']['name']}, assignee {a}, {len(x['comments']['nodes'])} comments (last: {x['comments']['nodes'][-1]['createdAt'][:16] if x['comments']['nodes'] else 'none'})"


# ---------------------------------------------------------------- lanes
GW = D + 'services/api-gateway/src/'
AU = D + 'services/auth/src/'
OR = D + 'services/originate/src/'
LANES = []

LANES.append(dict(
    n=19, L='X', ord='3rd', slug='ks1240_gateway_and_auth_social_fetch_timeouts', model='claude-opus-5-5', row='C3',
    kind='BUILD seat, on OPUS',
    title='KS-1240 done right on the two request-path surfaces (api-gateway front door + auth social providers): bound every outbound fetch AND map a timeout to the right answer',
    receipt="`model: claude-opus-5-5 -- C3 (the api-gateway front-door key validation and the auth service's social sign-in are authentication surfaces, and the ticket's own open question is what a TIMEOUT must answer there)  -- P1-P4: worktree, install, push under the board identity`. Launch it on that model at launch (`SEAT_MODEL_ENV=claude-opus-5-5`), not by `/model`. **Spark: not eligible** for this lane: the Spark already produced three gateway passes and two social passes (R 6th brief, PRs M and O) and each carries a named defect; a Claude seat builds the correct fix from scratch and reads the held patches ONLY as reference (they are in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1240-*`; each file's foot carries a DECISION NOTE).",
    docs=True,
    tickets=['KS-1240'],
    docker='none does',
    yours=[
        (GW + 'middleware/auth.ts', 'own'), (GW + 'routes/proxy.ts', 'own'), (GW + 'routes/admin.ts', 'own'),
        (GW + 'routes/batch.ts', 'own'), (GW + 'routes/audit-export.ts', 'own'),
        (AU + 'providers/social/github.ts', 'own'), (AU + 'providers/social/google.ts', 'own'),
        (AU + 'providers/social/linkedin.ts', 'own'), (AU + 'providers/social/apple.ts', 'own'),
        (AU + 'providers/social/facebook.ts', 'own'), (AU + 'providers/social/microsoft-personal.ts', 'own'),
        (GW + '__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts', 'new'),
        (GW + '__tests__/ks1240b-every-hand-built-gateway-fetch-is-bounded.test.ts', 'new'),
        (AU + '__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts', 'new'),
    ],
    ro=[
        (AU + 'routes/auth.ts', 'READ-ONLY: the login callback (`:1069-1080`, exchange inside a try) and `POST /social/link` (`:1346-1365`, exchange with NO local try). It is the reserved file of Spark pass J (KS-1776) and of a later lane: fix the classification INSIDE the provider files so this file need not change; if you conclude it must, mail a QUESTION and stop'),
        (AU + 'middleware/errorHandler.ts', 'READ-ONLY: it is R 6th PR C\'s file; read how an unclassified rejection is mapped'),
        (GW + 'index.ts', 'READ-ONLY'),
        (GW + '__tests__/ks1198-a-connector-jwt-is-not-a-bearer-credential.test.ts', 'READ-ONLY: an existing front-door cell family; an existing test that your intended change turns red is a MAIL (QUESTION) naming it, not an edit'),
        (AU + '__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts', 'READ-ONLY (as above)'),
        (AU + '__tests__/ks728-social-link-responds.test.ts', 'READ-ONLY (as above)'),
    ],
    boot_extra='',
))

LANES.append(dict(
    n=20, L='Y', ord='4th', slug='ks1240_ipfs_and_tenant_provisioning_fetch_timeouts', model='claude-sonnet-5-5', row='C2',
    kind='BUILD seat, on SONNET',
    title='KS-1240 done right on the two non-gateway services (nft-certificate IPFS provider, tenant-provisioning): bound every outbound fetch and make the timeout land in the answer the code promises',
    receipt="`model: claude-sonnet-5-5 -- C2 (multi-file build; no auth design: both services sit behind the gateway; the one judgement, what tenant creation answers when key generation times out, is flagged in item 2 with a QUESTION route)  -- P1-P4: worktree, install, push under the board identity`. Launch it on that model at launch (`SEAT_MODEL_ENV=claude-sonnet-5-5`), not by `/model`. **Spark: not eligible** (the Spark passes P and Q exist and each carries a named defect; a Claude seat builds from scratch and reads the held patches `READY_KS-1240-*ks_1240_p7_ipfs*` and `*p8_provisioning*` only as reference).",
    docs=True,
    tickets=['KS-1240'],
    docker='none does',
    yours=[
        (D + 'services/nft-certificate/src/services/ipfs.service.ts', 'own'),
        (D + 'services/tenant-provisioning/src/index.ts', 'own'),
        (D + 'services/tenant-provisioning/src/meteringKey.ts', 'own'),
        (D + 'services/nft-certificate/src/__tests__/ks1240b-ipfs-fetches-are-bounded-and-a-body-stall-maps-to-503.test.ts', 'new'),
        (D + 'services/tenant-provisioning/src/__tests__/ks1240b-provisioning-fetches-are-bounded.test.ts', 'new'),
    ],
    ro=[
        (D + 'services/nft-certificate/src/__tests__/ipfs.service.test.ts', 'READ-ONLY: an existing cell family; a test your change turns red is a MAIL (QUESTION) naming it, not an edit'),
        (D + 'services/tenant-provisioning/src/__tests__/meteringKey.test.ts', 'READ-ONLY (as above)'),
        (D + 'services/tenant-provisioning/src/__tests__/smoke.test.ts', 'READ-ONLY (as above)'),
    ],
    boot_extra='',
))

LANES.append(dict(
    n=21, L='Z', ord='3rd', slug='ks1382_blockchain_testing_target_base_follows_the_slot', model='claude-sonnet-5-5', row='C2',
    kind='BUILD seat, on SONNET',
    title='KS-1382: the five Blockchain/Testing entry points stop defaulting TARGET_BASE to slot 1 and a slot-N run can no longer attack another seat\'s stack',
    receipt="`model: claude-sonnet-5-5 -- C2 (shell build plus a new shell suite; spelled out by the ticket's Fix and Acceptance sections; no auth design)  -- P1-P4: worktree, install, push under the board identity`. Launch it on that model at launch (`SEAT_MODEL_ENV=claude-sonnet-5-5`), not by `/model`. **Spark: not eligible** (six files plus a new suite; the Spark screen's predicate is one to three files with a runnable in-process test).",
    docs=True,
    tickets=['KS-1382'],
    docker='none does',
    yours=[
        ('Blockchain/Testing/ci/orchestrate.sh', 'own'), ('Blockchain/Testing/ci/tools/run-schemathesis.sh', 'own'),
        ('Blockchain/Testing/jobs/05-dast-zap.sh', 'own'), ('Blockchain/Testing/jobs/06-tenant-isolation.sh', 'own'),
        ('Blockchain/Testing/run-internal-audit.sh', 'own'),
        ('Blockchain/Testing/tests/tenant-isolation/runner.ts', 'own'),
        ('Blockchain/Testing/README.md', 'own'), ('Blockchain/Testing/ci/README.md', 'own'),
        (D + 'scripts/__tests__/blockchain_testing_target_base_follows_the_slot.test.sh', 'new'),
    ],
    ro=[
        (D + 'scripts/stack_env.sh', 'READ-ONLY: the slot arithmetic you must SOURCE, never copy (it refuses without PROJECT_ROOT)'),
        (D + 'scripts/run-shell-suites.sh', 'READ-ONLY: discovers `scripts/__tests__/*.test.sh` (`:49`, `:65`); run it, do not edit it'),
        ('Blockchain/Testing/ci/aggregate.test.mjs', 'READ-ONLY: the only existing Blockchain/Testing test'),
    ],
    boot_extra='',
))

LANES.append(dict(
    n=22, L='AA', ord='4th', slug='ks1472_ks1537_spec_prose_and_reserved_key_pins', model='claude-sonnet-5-5', row='C2',
    kind='BUILD seat, on SONNET',
    title='Published-contract prose and the pins behind it: KS-1472 (OAuth authorize wording) and KS-1537 items m-1, N-1, N-2 (reserved metadata keys); regenerate the yaml, never hand-edit it',
    receipt="`model: claude-sonnet-5-5 -- C2 (spec text plus test pins; the one decision in KS-1537, N-4, is NOT built and goes to Wednesday as a card candidate)  -- P1-P4: worktree, install, push under the board identity`. Launch it on that model at launch (`SEAT_MODEL_ENV=claude-sonnet-5-5`), not by `/model`. **Spark: not eligible** (two openapi sources plus a generated yaml; the real-Postgres cells of N-1 and N-2 are not in-process).",
    docs=True,
    tickets=['KS-1472', 'KS-1537'],
    docker='N-1 and N-2 run against a real Postgres through the file\'s own harness (the `ks1508-a-planted...integration` header says how); if that harness needs Docker, send a QUESTION before starting any container',
    yours=[
        (AU + 'auth.openapi.ts', 'own'), (OR + 'originate.openapi.ts', 'own'), (D + 'docs/openapi/secuura-api.yaml', 'own'),
        (AU + '__tests__/ks839-contract-states-the-wildcard-allow-list-rule.test.ts', 'own'),
        (AU + '__tests__/ks1210-contract-publishes-the-closed-oauth-scope-enum.test.ts', 'own'),
        (OR + '__tests__/ks1508-a-planted-versionedbyid-is-not-stored.integration.test.ts', 'own'),
        (OR + '__tests__/ks1537-the-contract-states-the-reserved-metadata-keys.test.ts', 'new'),
    ],
    ro=[
        (OR + '__tests__/ks1508-versionedbyid-is-server-set.test.ts', 'READ-ONLY: the unit file; N-2\'s unit-side kills live there'),
        (OR + 'routes/documents.ts', 'READ-ONLY: `:656` is the strip-before-hash line the HASH cells guard'),
        (OR + 'routes/certifications.ts', 'READ-ONLY: `:531-533`, the N-4 echo/hash; N-4 is a DECISION and is not built here'),
        (AU + '__tests__/ks839-a-wildcard-allow-list-grants-nothing.test.ts', 'READ-ONLY'),
        (D + 'scripts/generate-openapi.ts', 'READ-ONLY: run `npm run generate-openapi` then `npm run check:openapi`'),
    ],
    boot_extra='',
))

LANES.append(dict(
    n=23, L='W', ord='5th', slug='ks1702_ks1588_mutant_pinned_test_cells', model='claude-sonnet-5-5', row='C2',
    kind='BUILD seat, on SONNET',
    title='Two test-only hardening tickets with named mutants: KS-1702 (migration 055 cell file, real Postgres) and KS-1588 (ks1009 wallet-status header and error-path cells); product untouched',
    receipt="`model: claude-sonnet-5-5 -- C2 (test-only cells, each proven red-first by its own named mutant; no product line)  -- P1-P4: worktree, install, push under the board identity`. Launch it on that model at launch (`SEAT_MODEL_ENV=claude-sonnet-5-5`), not by `/model`. **Spark: KS-1588 alone is Spark-eligible in principle (test-only L6, two cells spelled out); it is in this lane because the L6 test_only wiring is Wednesday's call: if Wednesday sends KS-1588 to the Spark, strike QUEUE item 2 from this brief.**",
    docs=True,
    tickets=['KS-1702', 'KS-1588'],
    docker='KS-1702 needs a real Postgres through the file\'s own harness (`import { Client } from \'pg\'`; read how the file locates its database); if that needs Docker, send a QUESTION before starting any container',
    yours=[
        (OR + '__tests__/ks1557-055-backfill.integration.test.ts', 'own'),
        (AU + '__tests__/ks1009-wallet-status-reveals-only-existence.test.ts', 'own'),
    ],
    ro=[
        (D + 'migrations/055_ks1557_backfill_connector_create_for_versioned_documents.sql', 'READ-ONLY: the migration is correct (gate CN1 verified it); no byte of it changes'),
        (AU + 'routes/auth.ts', 'READ-ONLY: the wallet-status route the ks1009 cells drive; R 6th/Spark pass J holds this file'),
    ],
    boot_extra='',
))

LANES.append(dict(
    n=24, L='S', ord='4th', slug='ks1394_ks1113_audit_locks_message_and_dsr_e2e_status', model='claude-sonnet-5-5', row='C2',
    kind='BUILD seat, on SONNET',
    title='Two small spelled-out fixes in tooling and e2e: KS-1394 (audit-locks refusal points at a regen command that cannot work) and KS-1113 (the e2e DSR cell PATCHes a status the enum refuses)',
    receipt="`model: claude-sonnet-5-5 -- C2 (two small fixes in two unrelated files, each with its fix shape written in the ticket)  -- P1-P4: worktree, install, push under the board identity`. Launch it on that model at launch (`SEAT_MODEL_ENV=claude-sonnet-5-5`), not by `/model`. **Spark: both are Spark-eligible in principle (KS-1394 one file; KS-1113 one file, two hunks, but its proof is an e2e run no in-process checker can do); they are in this lane because Wednesday decides what the Spark takes: if Wednesday sends one to the Spark, strike that QUEUE item.**",
    docs=True,
    tickets=['KS-1394', 'KS-1113'],
    docker='KS-1394 proofs may need `docker run node:24-alpine` (the ticket measured with it); KS-1113 needs a local stack for its one cell run. Send a QUESTION before starting any container or stack, naming the slot (the shared laptop runs several)',
    yours=[
        (D + 'scripts/audit/audit-locks.mjs', 'own'),
        (D + 'tests/e2e/tests/gdpr-compliance.prelaunch.spec.ts', 'own'),
    ],
    ro=[
        (D + 'scripts/preflight/lockfile-cleanroom.sh', 'READ-ONLY: `:72` and `:190` print the per-directory command the message cites'),
        (D + 'scripts/audit/lock-discovery.mjs', 'READ-ONLY'),
        (D + 'scripts/audit/audit-baseline.json', 'READ-ONLY and NOT GRANTED: it is KS-1707\'s lane (a push refused by an audit leg is reported, never fixed here)'),
        (D + 'scripts/audit/baseline-contract.test.mjs', 'READ-ONLY'),
        (D + 'scripts/audit/gate-exit-codes.test.mjs', 'READ-ONLY: look for the cell that pins the refusal text'),
    ],
    boot_extra='',
))

# ------------------------------------------------ R 6th partition (parsed)
rb = open(BR + '/2026-10-28_seatRaise_spark_held_passes.md').read()
part = rb[rb.index('## PARTITION'):rb.index('## PROTOCOL AND MAIL')]
r6_yours, r6_reserved = [], []
for line in part.splitlines():
    m = re.match(r'- PR ([A-Z0-9]+) \((KS-\d+)\): (.*)', line)
    if m:
        paths = re.findall(r'`([^`]+)`', m.group(3))
        (r6_yours if m.group(1) in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H1', 'H2', 'I') else r6_reserved).extend(paths)
r6_yours, r6_reserved = sorted(set(r6_yours)), sorted(set(r6_reserved))

prs = json.load(open(S + '/prs.json'))
pr_files = {}
n_entries = sum(len(p['files']) for p in prs)
for p in prs:
    for f in p['files']:
        pr_files.setdefault(f['path'], []).append(p['number'])

# --------------------------------------------------- disjointness
own = {l['n']: {p for p, k in l['yours']} for l in LANES}
pairs = []
for a, b in itertools.combinations(LANES, 2):
    ov = own[a['n']] & own[b['n']]
    pairs.append((a['n'], b['n'], sorted(ov)))
vs_r6 = {l['n']: sorted(own[l['n']] & set(r6_yours)) for l in LANES}
vs_r6res = {l['n']: sorted(own[l['n']] & set(r6_reserved)) for l in LANES}
vs_pr = {l['n']: sorted(own[l['n']] & set(pr_files)) for l in LANES}
# planted control
plant = own[19] | {next(iter(own[20]))}
control_fires = bool(plant & own[20])

rcs = {}
for l in LANES:
    for p, k in l['yours']:
        rcs[p] = rc(p)
    for p, k in l['ro']:
        rcs[p] = rc(p)
for p in (DOC1, DOC2):
    rcs[p] = rc(p)
# sanity: own/ro must exist, new must not
bad = []
for l in LANES:
    for p, k in l['yours']:
        if (k == 'new') != (rcs[p] != 0):
            bad.append((l['n'], p, k, rcs[p]))
    for p, k in l['ro']:
        if rcs[p] != 0:
            bad.append((l['n'], p, 'ro', rcs[p]))
json.dump(dict(bad=bad, pairs=pairs, vs_r6=vs_r6, vs_r6res=vs_r6res, vs_pr=vs_pr, control=control_fires,
               r6=len(r6_yours), r6res=len(r6_reserved), prfiles=len(pr_files)), open(S + '/disj.json', 'w'), indent=1)
print('BAD', bad)
print('overlaps', [p for p in pairs if p[2]])
print('vs_r6', vs_r6, 'vs_r6res', vs_r6res, 'vs_pr', vs_pr, 'control', control_fires)
print('R6 yours', len(r6_yours), 'reserved', len(r6_reserved), 'open PR files', len(pr_files))

exec(open(S + '/briefs.py').read())
