# Gate 129 mutants: product files only, tests untouched; each edit asserted to match exactly once; sha256 restore asserted after every run.
import hashlib, json, subprocess, sys, re
G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate129-ks1942-pr1947'
A = G + '/repo/Blockchain/Dev/services/governance/src/'
SVC, RT, DB = A + 'services/governanceService.ts', A + 'routes/governance.ts', A + 'db.ts'
M = {
 'M1 accept the body stake (D2a check gone, body stake stored)': [
   (SVC, "    throw new ForbiddenError('Only an admin can set stake or roles');\n", "    /* gate129 M1 */\n"),
   (SVC, "    : unstakedParticipant(userId, linked, request.did);", "    : { ...unstakedParticipant(userId, linked, request.did), stakedAmount: request.stakedAmount, tier: calculateTier(request.stakedAmount), votePower: calculateVotePower(request.stakedAmount, calculateTier(request.stakedAmount)), isDRep: request.isDRep ?? false, isConstitutionalCommittee: request.isConstitutionalCommittee ?? false };")],
 'M1b ignore (not refuse) a body stake/flag': [
   (SVC, "    throw new ForbiddenError('Only an admin can set stake or roles');\n", "    /* gate129 M1b */\n")],
 'M2 skip the wallet-link check (body wallet bound)': [
   (SVC, "  const linked = await readLinkedWallet(userId, tenantId);\n", "  const linked0 = await readLinkedWallet(userId, tenantId);\n  const linked = request.walletAddress || linked0;\n")],
 'M2b drop only the differing-wallet 403': [
   (SVC, "  if (request.walletAddress !== linked) {", "  if (false) {")],
 'M2c drop the no-linked-wallet 403 (bind the body wallet when none linked)': [
   (SVC, "  const linked = await readLinkedWallet(userId, tenantId);\n  if (!linked) {\n    throw new ForbiddenError('Link a wallet to your account first');\n  }\n", "  const linked = (await readLinkedWallet(userId, tenantId)) ?? request.walletAddress;\n")],
 'M3 skip the 409 (self-register)': [
   (SVC, "  if (holder && holder.id !== userId) {", "  if (false) {")],
 'M3b skip the 409 (createProposal auto-register)': [
   (SVC, "    if (await dbGetParticipantByAddress(linked)) {", "    if (false) {")],
 'M4 write before the lookup (self-register)': [
   (SVC, "  const linked = await readLinkedWallet(userId, tenantId);\n", "  await dbSaveParticipant(unstakedParticipant(userId, request.walletAddress, request.did));\n  const linked = await readLinkedWallet(userId, tenantId);\n")],
 'M4b write before the lookup (createProposal)': [
   (SVC, "    const linked = await readLinkedWallet(proposerId, caller?.tenantId);\n", "    await dbSaveParticipant(unstakedParticipant(proposerId, proposerId));\n    const linked = await readLinkedWallet(proposerId, caller?.tenantId);\n")],
 'M5 role check removed (everyone admin-set)': [
   (RT, "    const participant = isPlatformRole(user.role)\n", "    const participant = isPlatformRole(user.role) || user.userId.length > 0\n")],
 'M5b Unicode toUpperCase role compare (fold trick)': [
   (RT, "    const participant = isPlatformRole(user.role)\n", "    const participant = ['SYSTEM_ADMIN', 'SUPER_ADMIN'].includes(String(user.role).toUpperCase())\n")],
 'M6 users-read failure swallowed into "no wallet"': [
   (SVC, "    throw new ServiceUnavailableError('Linked wallet store');", "    return null;")],
 'M7 tenant GUC dropped': [
   (DB, "      await applyTenantGuc(client);\n", "      void applyTenantGuc;\n")],
 'M7b degraded mode reads as no wallet': [
   (DB, "    throw new Error('governance database unavailable (degraded mode)');", "    return null;")],
 'M8 admin flags reset again on omit': [
   (SVC, "    isDRep: options?.isDRep ?? existing?.isDRep ?? (stakedAmount >= 1000),", "    isDRep: options?.isDRep ?? (stakedAmount >= 1000),"),
   (SVC, "    isConstitutionalCommittee: options?.isConstitutionalCommittee ?? existing?.isConstitutionalCommittee ?? false,", "    isConstitutionalCommittee: options?.isConstitutionalCommittee ?? false,")],
 'M9 createProposal keeps the 1000 grant': [
   (SVC, "    proposer = unstakedParticipant(proposerId, linked);", "    proposer = { ...unstakedParticipant(proposerId, linked), stakedAmount: 1000, tier: calculateTier(1000), votePower: calculateVotePower(1000, calculateTier(1000)) };")],
 'M10 SET list loses is_constitutional_committee': [
   (SVC, " is_constitutional_committee = EXCLUDED.is_constitutional_committee,\n", "\n")],
 'M11 non-admin byId failure swallowed (KS-1940 twin)': [
   (SVC, "  const existing = holder ?? (await dbGetParticipant(userId));", "  const existing = holder ?? (await dbGetParticipant(userId).catch(() => undefined));")],
 'M12 non-admin byAddress failure swallowed (KS-1940 twin)': [
   (SVC, "  const holder = await dbGetParticipantByAddress(linked);", "  const holder = await dbGetParticipantByAddress(linked).catch(() => undefined);")],
 'M13 existing participant not kept (self re-register resets to unstaked)': [
   (SVC, "  const stored = existing ?? unstakedParticipant(userId, linked);", "  const stored = unstakedParticipant(userId, linked);")],
}
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
orig = {p: open(p).read() for p in (SVC, RT, DB)}; H = {p: sha(p) for p in orig}
only = sys.argv[1:]  # optional mutant id prefixes
rows = []
for name, edits in M.items():
    mid = name.split()[0]
    if only and mid not in only: continue
    txt = dict(orig)
    for p, a, b in edits:
        c = txt[p].count(a)
        assert c == 1, f'{mid}: anchor count {c} in {p}'
        txt[p] = txt[p].replace(a, b)
    for p in orig: open(p, 'w').write(txt[p])
    log = f'{G}/logs/mut_{mid}.log'; js = f'{G}/logs/mut_{mid}.json'
    subprocess.run(['bash', G + '/scripts/jt.sh', log, '--json', '--outputFile=' + js, 'ks1942-register|ks1940-failed|/governance.test'])
    for p in orig: open(p, 'w').write(orig[p])
    restored = all(sha(p) == H[p] for p in orig)
    try:
        j = json.load(open(js)); fails = []; kinds = set(); suite_err = []
        for s in j['testResults']:
            if not s['assertionResults'] and s.get('message'): suite_err.append(s['message'][:160].replace('\n', ' '))
            for t in s['assertionResults']:
                if t['status'] == 'failed':
                    w = t['title'].split(' '); fails.append((w[1] + ' ' + w[2]) if w[0] in ('RED', 'control') else t['title'][:30])
                    m = ' '.join(t['failureMessages']); kinds.add('assertion' if re.search(r'expect\(|Expected|Received', m) else 'other')
        verdict = 'KILLED' if fails else ('COMPILE/SUITE ERROR' if suite_err else 'SURVIVED')
        rows.append((mid, name, verdict, len(fails), sorted(set(fails))[:14], sorted(kinds), suite_err[:1], restored, j['numTotalTests']))
    except Exception as e:
        rows.append((mid, name, 'NO RESULT ' + repr(e)[:80], 0, [], [], [], restored, 0))
    print(rows[-1], flush=True)
print('ALL RESTORED' if all(r[7] for r in rows) else 'RESTORE FAILURE')
