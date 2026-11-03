import re,sys,glob
O='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator94/'
S='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
fixes=[
 ("the timestamp routes in `src/index.ts` (single and batch) await `submitTimestampRequest` and fall back or report per item on `success: false`; a rejection instead reaches the route's own catch.",
  "`requestTimestamp` (same file, line 333) returns it, and `qualified-tsa.ts` imports `requestTimestamp` for the timestamp routes (single and batch); they fall back or report per item on `success: false`, and a rejection instead reaches their own catch."),
 ("the billing routes and the webhook handlers call `sendEmail` for purchase and payment-failure notices and ignore a `false`; a rejection instead reaches the caller's own error path.",
  "NONE at the tip: a search of `billing/src` finds only the definition of `sendEmail` (and its template helpers in the same file), so this is a latent site; were it called, a caller would ignore a `false` and a rejection would reach its own error path."),
 ("the mint routes in `src/routes/nft.routes.ts` call `classifyMintError` in their catch and answer 404, 503 or 400 from the `errorCode` (`mintFailureHttpStatus`); a throw there escapes the route's catch.",
  "`MintingService` (`src/services/minting.service.ts`, line 386) calls `classifyMintError` in its catch, records the message and the failure on the NFT record and passes the `errorCode` on so the route can answer 404, 503 or 400 (`mintFailureHttpStatus`); a throw there escapes that catch and leaves the record unmarked."),
 ("so the route answers its default 400 with that message.","so the mint is recorded failed and the route answers its default 400 with that message."),
]
def fix(t):
    n=0
    for a,b in fixes:
        if a in t: t=t.replace(a,b); n+=1
    return t,n
p=O+'gen/sites94.py'; t=open(p).read(); t,n=fix(t); open(p,'w').write(t); print('sites',n)
for d in glob.glob(S+'ks_1868_o94_p[359]_*'):
    f=d+'/KS-1868.md'; t=open(f).read(); t,n=fix(t); open(f,'w').write(t); print(d[-40:],n)
