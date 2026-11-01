import re
src=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator50/gen/mk50.py',encoding='utf-8').read()
tail=src[src.index('def build(k):'):]
reps=[
("**auth is a security surface: the raise of this pass is gated tier 1.** ",""),
("Secuura (auth) only.","Secuura (nft-certificate) only."),
("KS-1868 auth:","KS-1868 nft-certificate:"),
("in `services/auth/src/routes/auth.ts`.","in `services/nft-certificate/src/services/minting.service.ts`."),
("This pass is one of three sequenced in old-line order in this one file (register :306, login :612, reset-password :880); each is generated against the same tip and is disjoint from the others. Seat S 10th's list of the log-only unguarded reads in this file after its KS-1885 sweep is the source of the three sites.",
 "This pass is one of two sequenced in old-line order in this one file (getCertificationData :177, getWalletNFTCertificates :688); each is generated against the same tip and is disjoint from the other. The sites are the log-only unguarded reads Seat R 72nd left after PR 1899 (and gate 84's list). The third candidate, `mintOnCardano` :798, is deliberately not in this series (it rethrows into the unguarded `classifyMintError`)."),
("**Do NOT touch** any message text, any other line of the file, or any other catch block in it. In particular do NOT touch the other two KS-1868 sites of this file (the other `Failed to publish event` handler, the reset-password revocation block), the KS-1885 code (`authoredExchangeText` at :989-990 and the exchange-error handling near :1113 and :1403; Seat S 10th named :1080-1081 and :1362 at its own tree, which sit about 30-40 lines away at this tip), or any `err?.message` read (:372, :547, :587, :768 here; S 10th listed :371, :546, :586, :767 at its tree): those are a different form and out of this pass.",
 "**Do NOT touch** any message text, any other line of the file, or any other catch block in it. In particular do NOT touch the other unguarded read of this series, the `Real minting failed` catch in `mintOnCardano` (:798), or `classifyMintError` (a different file), and leave the four catch blocks that already carry the inner `try` (:92, :137, :518, :604) alone."),
("services/auth uses its own node_modules; the pinned ref runs in the baseline.","The pinned ref runs in the baseline."),
("the 22 open PRs","the 22 open PRs"),
("(22 PRs, 124","(22 PRs, 124"),
]
for a,b in reps:
    assert a in tail or a in("the 22 open PRs","(22 PRs, 124"), a[:50]
    tail=tail.replace(a,b)
head='''# Operator 51: KS-1868 services/nft-certificate/src/services/minting.service.ts (:177 getCertificationData, :688 getWalletNFTCertificates)
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='8afcf256ed5fb38d05f7273e08e1b912446bac5c'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator51/gen/'
SV='Blockchain/Dev/services/nft-certificate/'
PROD=SV+'src/services/minting.service.ts'
TD=SV+'src/__tests__/'
def edit1(t,old,new):
    assert t.count(old)==1, old
    return t.replace(old,new)
def safe(ind, fn_old_lines):
    pass
P1_OLD=("      logger.error('Error fetching certification data from originate service', {\\n        certificationId,\\n"
        "        error: err instanceof Error ? err.message : String(err),\\n      });\\n")
P1_NEW=("      let reason: string;\\n      try {\\n        reason = err instanceof Error ? err.message : String(err);\\n      } catch {\\n        reason = 'unreadable thrown value';\\n      }\\n"
        "      logger.error('Error fetching certification data from originate service', {\\n        certificationId,\\n        error: reason,\\n      });\\n")
P2_OLD="        logger.error('DB get wallet certificates failed', { error: err instanceof Error ? err.message : String(err) });\\n"
P2_NEW=("        let reason: string;\\n        try {\\n          reason = err instanceof Error ? err.message : String(err);\\n        } catch {\\n          reason = 'unreadable thrown value';\\n        }\\n"
        "        logger.error('DB get wallet certificates failed', { error: reason });\\n")
def p1(t): return edit1(t,P1_OLD,P1_NEW)
def p2(t): return edit1(t,P2_OLD,P2_NEW)
COMMON_PR=("No open PR touches this file: the 22 open PRs read 2026-11-02 through the GitHub API (124 file entries) were scanned for `nft-certificate/src/services/minting.service.ts` and none lists it (PR 1900 is the kyc DB helpers); planted positive control: the same scan finds services/nft-certificate in 2 file entries.")
REF=TD+'ks1836-nft-read-gate.test.ts'
T={}
T['p1']=dict(dir='ks_1868_o51_p1_nftcertificate_get_certification_data_unreadable_throw', fix=p1, line=177, tag='O51-P1',
  test=TD+'ks1868-nft-get-certification-data-unreadable-throw.test.ts', tsrc='t51_p1.ts.txt', ref=REF,
  title="`getCertificationData` must still log and return null when the originate-service fetch throws a value that cannot be read",
  site="the production-branch catch block of the module function `getCertificationData`",
  quote="`error: err instanceof Error ? err.message : String(err),`",
  whatwrong="In production `getCertificationData` fetches the certification from the originate service inside a `try`; its catch block logs `logger.error('Error fetching certification data from originate service', { certificationId, error: err instanceof Error ? err.message : String(err) })` (the read is on line 177) and then `return null`. If the fetch rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before `return null`, so the function rejects with the TypeError. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `error: reason`; the `return null` is then reached as for any ordinary fetch failure. An ordinary Error still logs `error: <its message>`.",
  callers="CALLERS (git grep at the tip): only `NFTMintingService.mintNFT` (:249), `const certification = await getCertificationData(request.certificationId); if (!certification) { throw new Error('Certification not found'); }`, all inside the big `try` of `mintNFT` whose catch calls `classifyMintError(error)` and returns `{ success:false, error: message, errorCode }`; POST /api/nft/mint (routes/nft.routes.ts:85-110) answers that message in the body with `mintFailureHttpStatus(errorCode)`. The read itself only feeds the log line (never a response). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable fetch rejection in production, `mintNFT` today resolves `{ success:false, errorCode:'MINT_FAILED' }` carrying the TypeError's text (a revoked Proxy gives \"Cannot perform 'getPrototypeOf' on a proxy that has been revoked\"; a throwing getter gives the getter's text) and the route answers 400 with that text; after the fix it resolves `{ success:false, error:'Certification not found', errorCode:'CERTIFICATION_NOT_FOUND' }` and the route answers 404, exactly as it already does for every ordinary fetch failure (the fetch-failure-reported-as-not-found conflation is existing behaviour and out of scope). The FAILED record's errorMessage changes the same way. The other branch (non-production, :186) swallows with a bare `catch {}` and is not touched.",
  harness="`../db` (isDbAvailable false, so nothing is saved), `../cardano` and `../utils/logger` are replaced; `fetch` is stubbed with a plain function and `process.env.NODE_ENV` is set to `production` for the test and restored; the real minting service runs through `mintNFT`; no database, no network.",
  red1="At the tip the catch throws, so `mintNFT` resolves `errorCode` `MINT_FAILED` (not `CERTIFICATION_NOT_FOUND`) and no `Error fetching certification data ...` line is logged")
T['p2']=dict(dir='ks_1868_o51_p2_nftcertificate_get_wallet_nft_certificates_unreadable_throw', fix=p2, line=688, tag='O51-P2',
  test=TD+'ks1868-nft-get-wallet-nft-certificates-unreadable-throw.test.ts', tsrc='t51_p2.ts.txt', ref=REF,
  title="`getWalletNFTCertificates` must still report when the thrown value cannot be read",
  site="the catch block of `getWalletNFTCertificates`",
  quote="`logger.error('DB get wallet certificates failed', { error: err instanceof Error ? err.message : String(err) });`",
  whatwrong="In `minting.service.ts` the catch block of `getWalletNFTCertificates` logs `logger.error('DB get wallet certificates failed', { error: err instanceof Error ? err.message : String(err) })` (the read is on line 688) and then falls through to the sorted `certificates` return. If the database call rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch block; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before the normal return, so the function rejects. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `{ error: <its message> }`.",
  callers="CALLERS (git grep at the tip): routes/nft.routes.ts:241 (GET /certificates, the `walletAddress` branch), inside a try whose catch answers 500 with the constant message 'Failed to fetch NFT certificates' (its own log read at :~262 is on the TypeError, an ordinary Error). The message is only logged. **BEHAVIOUR CHANGE the raise PR must state:** when the DB query rejects with an unreadable value, GET /api/nft/certificates?walletAddress=... today answers 500 (the call rejects); after the fix it logs the constant reason and returns the in-memory matches (often an empty list) with 200, then `selectReadableCertificates` filters as usual; this is exactly what an ordinary DB error already does, so an unreadable DB failure now reads to the client as an empty/partial list rather than an error (the read-gate and owner binding of KS-1836 are unchanged).",
  harness="`../db`, `../cardano` and `../utils/logger` are replaced; the real minting service runs; no database, no app boot and no network.",
  red1="At the tip the call rejects, so no `DB get wallet certificates failed` line is logged and the `resolves` assertion fails")
'''
open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator51/gen/mk51.py','w',encoding='utf-8').write(head+tail)
