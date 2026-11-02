# Gate 134 mutants: product file only, tests untouched; each anchor asserted to match exactly once; sha256 restore asserted after every run.
import hashlib, json, subprocess, sys, re
G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952'
SVC = G + '/repo/Blockchain/Dev/services/governance/src/services/governanceService.ts'
BUMP_P = "  await dbBumpParticipantCounter(proposer.id, 'proposals_created');\n"
BUMP_V = "  await dbBumpParticipantCounter(voter.id, 'votes_cast');\n"
REFRESH = "  let participant = existing ? await dbRefreshSelfRegistration(userId, linked, request.did) : undefined;\n"
M = {
 'M1 createProposal re-saves the whole proposer row (the bug)': [(SVC, BUMP_P, "  proposer.proposalsCreated++; proposer.lastActiveAt = new Date(); await dbSaveParticipant(proposer);\n")],
 'M1v castVote re-saves the whole voter row (the bug)': [(SVC, BUMP_V, "  voter.votesCast++; voter.lastActiveAt = new Date(); await dbSaveParticipant(voter);\n")],
 'M1s self-register re-saves the whole existing row (the bug)': [(SVC, REFRESH,
   "  let participant: GovernanceParticipant | undefined = existing ? { ...existing, walletAddress: linked, did: request.did ?? existing.did, lastActiveAt: new Date() } : undefined;\n  if (participant) await dbSaveParticipant(participant);\n  void dbRefreshSelfRegistration;\n")],
 'M2 createProposal writes the counter from the read value': [(SVC, BUMP_P,
   "  await query('UPDATE svc_governance_participants SET proposals_created = $3, last_active_at = $2 WHERE id = $1', [proposer.id, new Date(), proposer.proposalsCreated + 1]);\n")],
 'M2v castVote writes the counter from the read value': [(SVC, BUMP_V,
   "  await query('UPDATE svc_governance_participants SET votes_cast = $3, last_active_at = $2 WHERE id = $1', [voter.id, new Date(), voter.votesCast + 1]);\n")],
 'M2b bump SQL writes counter from the read value inside the helper (same SQL shape, + 0)': [(SVC,
   "'UPDATE svc_governance_participants SET proposals_created = proposals_created + 1, last_active_at = $2 WHERE id = $1',",
   "'UPDATE svc_governance_participants SET proposals_created = proposals_created + 0, last_active_at = $2 WHERE id = $1',")],
 'M3 refresh drops RETURNING (201 reports the stale read)': [(SVC,
   "       WHERE id = $1 RETURNING *`,\n      [id, walletAddress, did ?? null, new Date()]",
   "       WHERE id = $1`,\n      [id, walletAddress, did ?? null, new Date()]"),
   (SVC, "    return result.rows.length > 0 ? rowToParticipant(result.rows[0]) : undefined;\n", "    return result.rowCount ? ({} as GovernanceParticipant) : undefined;\n"),
   (SVC, REFRESH, "  let participant = existing ? await dbRefreshSelfRegistration(userId, linked, request.did) : undefined;\n  if (participant && existing) participant = { ...existing, walletAddress: linked, did: request.did ?? existing.did };\n")],
 'M3b insert drops RETURNING (201 reports the built row, not the stored one)': [(SVC,
   "       ON CONFLICT (id) DO NOTHING RETURNING *`,", "       ON CONFLICT (id) DO NOTHING`,"),
   (SVC, "    if (result.rows.length > 0) inserted = rowToParticipant(result.rows[0]);\n", "    inserted = p; void result;\n")],
 'M4 first registration overwrites on conflict': [(SVC,
   "       ON CONFLICT (id) DO NOTHING RETURNING *`,",
   "       ON CONFLICT (id) DO UPDATE SET wallet_address = EXCLUDED.wallet_address, did = EXCLUDED.did, staked_amount = EXCLUDED.staked_amount, tier = EXCLUDED.tier, vote_power = EXCLUDED.vote_power, is_drep = EXCLUDED.is_drep, is_constitutional_committee = EXCLUDED.is_constitutional_committee, proposals_created = EXCLUDED.proposals_created, votes_cast = EXCLUDED.votes_cast, last_active_at = EXCLUDED.last_active_at RETURNING *`,")],
 'M4b admin upsert writes the counters again (D-4 undone)': [(SVC,
   "         last_active_at = EXCLUDED.last_active_at`,\n      [p.id, p.walletAddress, p.did || null, p.stakedAmount, p.tier, p.votePower,",
   "         proposals_created = EXCLUDED.proposals_created, votes_cast = EXCLUDED.votes_cast, last_active_at = EXCLUDED.last_active_at`,\n      [p.id, p.walletAddress, p.did || null, p.stakedAmount, p.tier, p.votePower,")],
 'M5 refresh clears an omitted did (no COALESCE)': [(SVC, "did = COALESCE($3, did), last_active_at = $4", "did = $3, last_active_at = $4")],
 'M6 bump on a missing row throws (request fails after the write)': [(SVC,
   "  if (!rowCount) logger.warn('Participant row not found at counter bump', { participantId: id, counter });",
   "  if (!rowCount) throw new NotFoundError('Participant');")],
 'M6b bump on a missing row is silent (no warn)': [(SVC,
   "  if (!rowCount) logger.warn('Participant row not found at counter bump', { participantId: id, counter });", "  void rowCount;")],
 'M7 wallet 23505 not recognised (500 again)': [(SVC, "    return !!e && e.code === '23505' && e.constraint === PARTICIPANT_WALLET_UNIQUE;", "    return !!e && false && String(PARTICIPANT_WALLET_UNIQUE) === '';")],
 'M7b any 23505 is a wallet 409 (constraint name ignored)': [(SVC, "    return !!e && e.code === '23505' && e.constraint === PARTICIPANT_WALLET_UNIQUE;", "    return !!e && e.code === '23505' && typeof PARTICIPANT_WALLET_UNIQUE === 'string';")],
 'M8 DO NOTHING (0 rows) answers 503 instead of re-reading': [(SVC, "  const stored = await dbGetParticipant(p.id);\n  if (!stored) throw new ServiceUnavailableError('Governance participant store');\n  return stored;",
   "  throw new ServiceUnavailableError('Governance participant store');")],
 'M9 refresh writes stake from the stale read too': [(SVC, REFRESH,
   "  let participant = existing ? await dbRefreshSelfRegistration(userId, linked, request.did) : undefined;\n  if (participant && existing) { await query('UPDATE svc_governance_participants SET staked_amount = $2, tier = $3, vote_power = $4, is_drep = $5, is_constitutional_committee = $6 WHERE id = $1', [userId, existing.stakedAmount, existing.tier, existing.votePower, existing.isDRep, existing.isConstitutionalCommittee]); participant = { ...participant, ...{ stakedAmount: existing.stakedAmount, tier: existing.tier, votePower: existing.votePower, isDRep: existing.isDRep, isConstitutionalCommittee: existing.isConstitutionalCommittee } }; }\n")],
}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
orig = open(SVC).read(); H0 = sha(SVC)
only = sys.argv[1:]
rows = []
for name, edits in M.items():
    mid = name.split()[0]
    if only and mid not in only: continue
    txt = orig
    for p, a, b in edits:
        c = txt.count(a); assert c == 1, f'{mid}: anchor count {c}'
        txt = txt.replace(a, b)
    open(SVC, 'w').write(txt)
    log = f'{G}/logs/mut_{mid}.log'; js = f'{G}/logs/mut_{mid}.json'
    subprocess.run(['bash', G + '/scripts/jt.sh', log, '--json', '--outputFile=' + js])
    open(SVC, 'w').write(orig)
    restored = sha(SVC) == H0
    try:
        j = json.load(open(js)); fails = []; kinds = set(); suite_err = []
        for s in j['testResults']:
            if not s['assertionResults'] and s.get('message'): suite_err.append(s['message'][:200].replace('\n', ' '))
            for t in s['assertionResults']:
                if t['status'] == 'failed':
                    w = t['title'].split(' '); fails.append((w[1] + ' ' + w[2]) if w[0] in ('RED', 'control') and len(w) > 2 else t['title'][:40])
                    m = ' '.join(t['failureMessages']); kinds.add('assertion' if re.search(r'expect\(|Expected|Received', m) else 'other:' + m[:80].replace('\n', ' '))
        verdict = 'KILLED' if fails else ('COMPILE/SUITE ERROR' if suite_err else 'SURVIVED')
        rows.append((mid, verdict, len(fails), sorted(set(fails))[:12], sorted(kinds), suite_err[:1], restored, j['numTotalTests']))
    except Exception as e:
        rows.append((mid, 'NO RESULT ' + repr(e)[:80], 0, [], [], [], restored, 0))
    print(rows[-1], flush=True)
print('ALL RESTORED' if all(r[6] for r in rows) else 'RESTORE FAILURE')
