# Operator 93 sites (KS-1868). Built by mk94.py (exec'd into its namespace: T, SV, OS, mk available).
REFV=SV+'auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts'
def guard(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
def guard_e(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s instanceof Error ? %s.message : String(%s);\n"%(var,var,var)+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
REUSE_Q=("This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (operator 81 `security/src/db.ts`, operator 85 `accountLockout.ts`, operator 86 `userErasedSubscriber.ts`: `const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, the constant `'unreadable thrown value'` on throw) before the log call; no helper exists in this file and none is added.")
REUSE_E=("This follows the guard that the merged KS-1868 passes use for `err instanceof Error ? err.message : String(err)` reads (operator 51 `nft-certificate`, operator 57 `tenant-provisioning`, operator 86 `errorTrackingService.ts`: the same expression inside a `try`, the constant `'unreadable thrown value'` on throw) before the log call; no helper exists in this file and none is added.")
def site(k, svc, rel, edits, nh, lines, fn, short, whatwrong, callers, premise, tsrc, dbnote, ncells, greens, redcells, nred, name, red1, reuse=REUSE_Q, runner='vitest', ref=None, testbase=None):
    run = 'run ' if runner=='vitest' else ''
    T[k]=dict(key='KS-1868', runner=runner, runcmd=run, rdir=SV+svc, ref=ref or REFV,
      sib="`ks1868-oauth-authorize-token-unreadable-throw.test.ts` and `ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts`" if runner=='vitest' else "`ks1868-anchors-route-catches-unreadable-throw.test.ts`",
      reuse=reuse, dir='ks_1868_o98_%s_%s'%(k,name), prod=SV+svc+'/'+rel, edits=edits, nh=nh, lines=lines,
      test=SV+svc+'/src/__tests__/'+testbase, tsrc=tsrc, fn=fn, short=short, premise=premise, whatwrong=whatwrong, callers=callers,
      ncells=ncells, red1=red1, dbnote=dbnote, greens=greens, redcells=redcells,
      redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,nred+1)))
def guard_s(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? undefined : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
SOr=SV+'originate/'
JREF=SOr+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
HELD_NOTE="Held READY files of other operators edit this product file at other hunks (named in the report); the hunks of this brief are disjoint from them by more than 3 lines."


# ===================== Operator 97 sites (KS-1868) =====================
def gv(ind, var, expr, const="'unreadable thrown value'"):
    s=' '*ind
    return (s+"let %s: string;\n"%var+s+"try {\n"+s+"  %s = %s;\n"%(var,expr)+s+"} catch {\n"+s+"  %s = %s;\n"%(var,const)+s+"}\n")
SEXPR="err instanceof Error ? err.message : String(err)"
def std_what(where, what_it_returns, extra=''):
    return ("%s reads the thrown value with no guard. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch itself throw, so %s. The fix is the house guard placed in the catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The message text of every value that can be read is unchanged.%s")%(where, what_it_returns, extra)


PKG_REF='Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts'
SIB_PKG="`ks1868-response-cache-read-unreadable-throw.test.ts` and `ks1868-audit-logger-flush-unreadable-throw.test.ts`"
REUSE_S=("This follows the guard that the merged KS-1868 passes use for `String(err)` reads (operator 51 `nft-certificate`, operator 57 `tenant-provisioning`, operator 86 `errorTrackingService.ts`: the same expression inside a `try`, the constant `'unreadable thrown value'` on throw) before the log call; no helper exists in this file and none is added.")
def what(where, ret, extra=''):
    return ("%s reads the thrown value with `String(...)`, unguarded. A thrown value whose read throws (a revoked Proxy: `String()` throws on it; an Error whose `message` getter throws, since `Error.prototype.toString` reads it) makes the catch itself throw, so %s. The fix is the house guard placed in the catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The text of every value that can be read is unchanged.%s")%(where, ret, extra)
STD_CELLS='4 cells: C1, C2 controls, R1, R2 red'
G2="'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)"
G2R="`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)"
def fixsib(k, pkg=False):
    if pkg:
        for _f in ('prod','test','rdir'):
            T[k][_f]=T[k][_f].replace('services/shared','packages/shared')
    T[k]['sib']=SIB_PKG

def catch_edit(ind, msg, var='error', pre="    } catch (error) {\n", tail="{ error: String(error) }", newtail="{ error: reason }", expr="String(error)"):
    s=' '*ind
    o=pre+s+"logger.error('%s', %s);\n"%(msg,tail)
    n=pre+gv(ind,'reason',expr)+s+"logger.error('%s', %s);\n"%(msg,newtail)
    return (o,n)

RS='src/security/redis-security-store.ts'
# ---- P1
def wd(where, ret, read="the thrown value's `message`"):
    return ("%s reads %s with no guard. A thrown value whose read throws (a revoked Proxy: any property read and `instanceof` throw on it; an Error whose `message` getter throws) makes the catch itself throw, so %s. The fix is the house guard placed in the catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The text of every value that can be read is unchanged.")%(where, read, ret)
def gv_t(ind, var, expr):
    return gv(ind, var, expr)
PKGS='Blockchain/Dev/packages/shared/'
# ---- P1 tenant-rate-limiter

# ===================== Operator 98 sites (KS-1868) =====================
# ---- P1 cardano wallet enableWallet
O1="  } catch (error) {\n    throw new Error(`Failed to enable wallet ${name}: ${error instanceof Error ? error.message : 'User rejected'}`);\n  }\n"
N1="  } catch (error) {\n"+gv(4,'reason',"error instanceof Error ? error.message : 'User rejected'")+"    throw new Error(`Failed to enable wallet ${name}: ${reason}`);\n  }\n"
site('p1','shared','src/cardano/wallet.ts',[(O1,N1)],1,
  '177-180 (the catch of `enableWallet`)',
  'the catch of `enableWallet` in `src/cardano/wallet.ts`',
  'the unguarded `error instanceof Error ? error.message : \'User rejected\'` read in the ONE catch of `enableWallet`; the CBOR and signature code of the file is deliberately NOT touched',
  wd("The catch of `enableWallet`","the call rejects with the engine TypeError or the getter error, not with the documented `Failed to enable wallet <name>: <reason>` Error that callers match on","the thrown value (`error instanceof Error ? error.message : 'User rejected'`)"),
  "CALLERS: `connectWallet` and the browser connect flows. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the call rejects with `Error('Failed to enable wallet <name>: <message>')` (`User rejected` for a non-Error). Today (hostile value): it rejects with a different error (a TypeError, or the getter's error) that leaks no wallet name. After: the same `Failed to enable wallet <name>:` Error with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the rejection is the documented Error with the constant reason.",
  "Premise: `wallet.ts` read lines 1-25 and 112-185",
  't98_p1.ts.txt',
  "`window` is stubbed (`vi.stubGlobal`) with a plain `cardano.nami.enable` that rejects with the cell's value; removed after each cell; no browser, no network.",
  STD_CELLS, G2, G2R, 2, 'shared_cardano_wallet_enable_wallet_catch_guard_message',
  "At the tip the rejection message is not the documented one, so the assertion fails", reuse=REUSE_E, runner='vitest', ref=PKG_REF,
  testbase='ks1868-cardano-wallet-enable-wallet-catch-unreadable-throw.test.ts')
fixsib('p1',True)

NFT_EXPR="error instanceof Error ? error.message : String(error)"
def nft(k, msg, logline, handler_desc, route, status_msg, name, tsrc, harness, premise):
    o="  } catch (error) {\n    logger.error('%s', { error: error instanceof Error ? error.message : String(error) });\n"%msg
    n="  } catch (error) {\n"+gv(4,'reason',NFT_EXPR)+"    logger.error('%s', { error: reason });\n"%msg
    site(k,'nft-certificate','src/routes/nft.routes.ts',[(o,n)],1,
      '%d-%d (the catch of the %s handler)'%(logline-1,logline+4,route),
      'the catch of the `%s` handler in `src/routes/nft.routes.ts`'%route,
      'the unguarded `error instanceof Error ? error.message : String(error)` read in the ONE catch of the `%s` handler; the catches of the other handlers of the router are deliberately NOT touched (each is its own pass)'%route,
      wd("The catch of the `%s` handler"%route,"the async handler REJECTS (Express 4 does not catch it: the request gets no reply and an unhandled rejection is raised) where an ordinary failure logs and answers 500 `INTERNAL_ERROR`","the thrown value (`error instanceof Error ? error.message : String(error)`)"),
      "CALLERS: the nft-certificate service mounts this router at `/api/nft`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `logger.error('%s', { error: <message> })` and HTTP 500 `{ success: false, error: { code: 'INTERNAL_ERROR', message: '%s' } }`. Today (hostile value): the handler rejects, no reply. After: the same log line with the constant reason and the same 500. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the client receives the 500 instead of no reply."%(msg,status_msg),
      premise, tsrc, harness, STD_CELLS, G2, G2R, 2, name,
      "At the tip the catch throws (the handler rejects), so the assertion fails", reuse=REUSE_E, runner='vitest', ref=PKG_REF,
      testbase='ks1868-nft-%s-catch-unreadable-throw.test.ts'%name.replace('nft_','').replace('_','-')[:60])
    T[k]['sib']=SIB_PKG
NFTH="The five sibling services, the logger and nothing else are replaced with plain stand-ins (`vi.mock`); the handler is read off `router.stack` and called with a plain request and a plain response recorder; the logger records `error` calls; no server, no network."
nft('p2','Error fetching certificate',293,'','GET /certificates/:id','Failed to fetch NFT certificate','nft_get_certificate_catch_guard','t98_p2.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 274-300")
nft('p3','Error fetching certificates',262,'','GET /certificates','Failed to fetch NFT certificates','nft_list_certificates_catch_guard','t98_p3.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 229-269 (including `readerIdentity` / `selectReadableCertificates` of `services/nftReadGate.ts`, read lines 60-85)")
nft('p4','Error fetching tiers',321,'','GET /tiers','Failed to fetch storage tiers','nft_tiers_catch_guard','t98_p4.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 305-329")
nft('p5','Error estimating cost',217,'','POST /estimate','Failed to estimate cost','nft_estimate_cost_catch_guard','t98_p5.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 189-227")
nft('p6','Error verifying transaction',426,'','POST /verify/transaction','Failed to verify transaction','nft_verify_transaction_catch_guard','t98_p6.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 404-433")
nft('p7','Error verifying asset',462,'','POST /verify/asset','Failed to verify asset','nft_verify_asset_catch_guard','t98_p7.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 438-468")
nft('p8','Error pinning CID',550,'','POST /ipfs/pin','Failed to pin CID','nft_ipfs_pin_catch_guard','t98_p8.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 534-556")
nft('p9','Error unpinning CID',575,'','POST /ipfs/unpin','Failed to unpin CID','nft_ipfs_unpin_catch_guard','t98_p9.ts.txt',NFTH,"Premise: `nft.routes.ts` read lines 1-30 and the handler at lines 559-581")
