import sys
G='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate134-ks1950-pr1952'
s=open(G+'/logs/prod/head/services_governanceService.ts').read()
a_old="""    if (isWalletHeldError(err)) throw new ConflictError(WALLET_HELD_MESSAGE);
    logger.error('DB insert participant failed'"""
a_new="""    if (isWalletHeldError(err)) {
      // The UNIQUE(wallet_address) index is not this INSERT's arbiter, so a concurrent first registration of the
      // SAME id and wallet can surface here instead of as ON CONFLICT (id) DO NOTHING: re-read by id first.
      const own = await dbGetParticipant(p.id);
      if (own && own.walletAddress === p.walletAddress) return own;
      throw new ConflictError(WALLET_HELD_MESSAGE);
    }
    logger.error('DB insert participant failed'"""
assert s.count(a_old)==1; fa=s.replace(a_old,a_new)
open(G+'/logs/prod/fix/FA_services_governanceService.ts','w').write(fa)
c_old="""    if (await dbGetParticipantByAddress(linked)) {
      // No row has this id (the read above), so any row holding the wallet is another participant's.
      throw new ConflictError('This wallet is registered to another governance participant');
    }
    proposer = await dbInsertParticipantIfAbsent(unstakedParticipant(proposerId, linked));"""
c_new="""    const holder = await dbGetParticipantByAddress(linked);
    if (holder && holder.id !== proposerId) {
      throw new ConflictError('This wallet is registered to another governance participant');
    }
    proposer = holder ?? (await dbInsertParticipantIfAbsent(unstakedParticipant(proposerId, linked)));"""
assert fa.count(c_old)==1
open(G+'/logs/prod/fix/FAC_services_governanceService.ts','w').write(fa.replace(c_old,c_new))
print('ok')
