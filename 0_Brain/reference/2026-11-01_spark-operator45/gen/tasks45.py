TASKS={}
NP='Blockchain/Dev/services/nft-certificate/'
N_REF=NP+'src/__tests__/ks1836-nft-read-gate.test.ts'
S9="This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator."
EM='—'
def ind(n): return ' '*n
def mkold(i, lvl, msg):
    return "%slogger.%s('%s', { error: err instanceof Error ? err.message : String(err) });\n"%(ind(i),lvl,msg)
def mknew(i, lvl, msg):
    s=ind(i)
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = err instanceof Error ? err.message : String(err);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n"
            +s+"logger.%s('%s', { error: reason });\n")%(lvl,msg)
HEAD="""import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: %(descr)s must still log its line and %(okname)s when the thrown value
// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws,
// throws on `.message`).
// The db stand-in is a plain function, not a vi.fn(): a spy inspects what it rejects with and
// could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  warn: vi.fn(),
  error: vi.fn(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: () => Promise.reject(h.toThrow),
}));

vi.mock('../cardano', () => ({
  isCardanoNFTReady: () => false,
  mintNFTOnChain: vi.fn(),
  getPolicyId: () => null,
  waitForNFTConfirmation: vi.fn(),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: h.warn, error: h.error, debug: vi.fn() },
}));

import { nftMintingService, loadFromDb } from '../services/minting.service';
%(extra)s
const LINES = () => h.%(lvl)s.mock.calls.filter((c) => String(c[0]).includes('%(msg)s'));

describe('KS-1868 %(descr)s reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.warn.mockReset();
    h.error.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message and %(okname)s', async () => {
    h.toThrow = new Error('db down');
    await expect(call()).resolves.%(okexp)s;
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and %(okname)s', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    await call().catch(() => undefined);
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and %(okname)s', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await call().catch(() => undefined);
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
"""
def add(key, slug, helper, via, callsrc, msg, lvl, i, okname, okexp, line, ret, callers):
    extra="\nconst call = %s;\n"%callsrc
    descr='`%s`'%helper
    where_note=("The catch block's `instanceof Error` read is on line %d; the catch logs '%s' at %s level with `{ error: <message> }` and does NOT rethrow: %s. "
      "The message is only logged, never returned to a caller or put in a response. CALLERS (git grep at the tip): %s. Other catch blocks of the file are NOT in this brief.")%(line,msg,lvl,ret,callers)
    TASKS[key]=dict(svc='nft-certificate', runner='vitest', runcmd='run ', runner_dir='Blockchain/Dev/services/nft-certificate', ref=N_REF, s9note=S9,
     dir='ks_1868_o45_%s_nftcertificate_%s_unreadable_throw'%(key,slug),
     prod=NP+'src/services/minting.service.ts', test=NP+'src/__tests__/ks1868-nft-%s-unreadable-throw.test.ts'%slug.replace('_','-'),
     old=mkold(i,lvl,msg), new=mknew(i,lvl,msg),
     tbody=HEAD%dict(descr=descr,extra=extra,lvl=lvl,msg=msg,okname=okname,okexp=okexp),
     where_line=line, fn='`%s`'%helper, file='minting.service.ts',
     shape="a `vi.hoisted` holder, `vi.mock(...)` of the db, cardano and logger modules, then the import of the real minting service",
     intro_site="the catch block of `%s` in `services/minting.service.ts`"%helper,
     where_note=where_note,
     whatwrong=("In `minting.service.ts` the catch block of `%s` logs `logger.%s('%s', { error: err instanceof Error ? err.message : String(err) })` (the read is on line %d) and then %s. "
      "If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. "
      "Either way the catch throws before the line is logged and before the normal return, so the function rejects with the hostile value. "
      "The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }`.")%(helper,lvl,msg,line,ret),
     consequence="Today a hostile rejection from the database layer makes the catch block itself throw, so nothing is logged and the call rejects.",
     red1="At the tip the call rejects, so the `resolves` assertion fails (and no line is logged)",
     dbnote="`../db`, `../cardano` and `../utils/logger` are mocked; no database, no app boot and no network.%s"%(" `%s` is reached through %s."%(helper,via) if via else ""),
     sibling="Every other catch block of `minting.service.ts` is NOT in this brief")
add('p1','load_from_db','loadFromDb','',"() => loadFromDb()",'Failed to load NFT certificates from DB '+EM+' starting empty','warn',4,'resolves undefined','toBeUndefined()',129,'it returns nothing (starting with an empty cache)',
    'server.ts:42 passes it as initDb\'s onReady hook; db.ts runDbReadyHook (:90-98) awaits it inside a try/catch that logs err?.message')
add('p2','db_save_certificate','dbSaveNFTCertificate','the exported `nftMintingService.recordClientMint`',
    "() =>\n  nftMintingService.recordClientMint({\n    certificationId: 'cert-ks1868',\n    txHash: 'tx-ks1868',\n    policyId: 'policy-ks1868',\n    assetName: 'asset-ks1868',\n    assetId: 'assetid-ks1868',\n    walletAddress: 'addr_ks1868',\n    onChainVerified: false,\n    onChainStatus: 'pending',\n  })",
    'DB save certificate failed','error',4,'resolves the saved record','toMatchObject({ certificationId: \'cert-ks1868\' })',90,'the function ends (returns nothing)',
    'minting.service.ts:234, :290, :350 and :707 via updateStatus (all inside the mintNFT try; its catch at :363 runs classifyMintError(error) and returns the message in the response body, so TODAY a hostile rejection from this helper reaches a response through the caller), :376 (inside that catch, rejects out of mintNFT) and :426 (recordClientMint, awaited with no catch). Every caller awaits it with no catch of its own, so a rejection DOES propagate today; the fix makes a hostile throw behave as an ordinary one already does (logged, swallowed)')
add('p3','get_nft_certificate','getNFTCertificate','',"() => nftMintingService.getNFTCertificate('ks1868-missing')",
    'DB get certificate failed','error',8,'resolves null','toBeNull()',504,'it falls through to `return null`',
    'routes/nft.routes.ts:276 (GET /certificates/:id) inside a try whose catch answers 500 with the constant message "Failed to fetch NFT certificate"; no other non-test caller')
add('p4','get_user_nft_certificates','getUserNFTCertificates','',"() => nftMintingService.getUserNFTCertificates('ks1868-user')",
    'DB get user certificates failed','error',8,'resolves an empty list','toEqual([])',584,'it falls through to the sorted `certificates` return',
    'routes/nft.routes.ts:242 (GET /certificates, the non-wallet branch) inside a try whose catch answers 500 with the constant message "Failed to fetch NFT certificates"; no other non-test caller')
