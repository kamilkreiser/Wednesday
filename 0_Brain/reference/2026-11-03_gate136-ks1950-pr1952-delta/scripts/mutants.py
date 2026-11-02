# Gate 136 delta mutants (fix lines only): product file only, tests untouched; each anchor asserted to match exactly once; sha256 restore asserted after every run.
import hashlib, json, subprocess, sys, re
G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta'
SVC = G + '/repo/Blockchain/Dev/services/governance/src/services/governanceService.ts'
BUMP_P = "  await dbBumpParticipantCounter(proposer.id, 'proposals_created');\n"
BUMP_V = "  await dbBumpParticipantCounter(voter.id, 'votes_cast');\n"
REFRESH = "  let participant = existing ? await dbRefreshSelfRegistration(userId, linked, request.did) : undefined;\n"
M = {
 'K1 F1 undone: the re-read removed (any wallet 23505 is a 409)': [(SVC, '      const own = await dbGetParticipant(p.id);\n      if (own && own.walletAddress === p.walletAddress) return own;\n      throw new ConflictError(WALLET_HELD_MESSAGE);', '      void dbGetParticipant;\n      throw new ConflictError(WALLET_HELD_MESSAGE);')],
 'K2 F1 re-read returns ANY own row (wallet equality dropped)': [(SVC, "      if (own && own.walletAddress === p.walletAddress) return own;", "      if (own) return own;")],
 'K3 F1 re-read returns own row even when absent-check inverted (returns undefined-or-row, never 409 when own exists with other wallet)': [(SVC, "      if (own && own.walletAddress === p.walletAddress) return own;", "      if (own && own.walletAddress !== p.walletAddress) return own;")],
 'K4 F3: any 23505 is the wallet one (constraint name ignored)': [(SVC, "    return !!e && e.code === '23505' && e.constraint === PARTICIPANT_WALLET_UNIQUE;", "    return !!e && e.code === '23505' && typeof PARTICIPANT_WALLET_UNIQUE === 'string';")],
 'K5 F2 undone: any holder is a 409': [(SVC, '    if (holder && holder.id !== proposerId) {', "    if (holder) {")],
 'K6 F2 holder ignored: always insert-if-absent': [(SVC, '    proposer = holder ?? (await dbInsertParticipantIfAbsent(unstakedParticipant(proposerId, linked)));', "    void holder; proposer = await dbInsertParticipantIfAbsent(unstakedParticipant(proposerId, linked));")],
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
