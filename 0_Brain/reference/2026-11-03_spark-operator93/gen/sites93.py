# Operator 93 sites (KS-1868). Built by mk93.py (exec'd into its namespace: T, SV, OS, mk available).
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
      reuse=reuse, dir='ks_1868_o93_%s_%s'%(k,name), prod=SV+svc+'/'+rel, edits=edits, nh=nh, lines=lines,
      test=SV+svc+'/src/__tests__/'+testbase, tsrc=tsrc, fn=fn, short=short, premise=premise, whatwrong=whatwrong, callers=callers,
      ncells=ncells, red1=red1, dbnote=dbnote, greens=greens, redcells=redcells,
      redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,nred+1)))
def guard_s(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? undefined : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
SOr=SV+'originate/'
JREF=SOr+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
HELD_NOTE="Held READY files of other operators edit this product file at other hunks (named in the report); the hunks of this brief are disjoint from them by more than 3 lines."

# ---- P1: m365-integration sharepoint/client.ts downloadAndHashItem catch (vitest)
M365REF=SV+'m365-integration/src/__tests__/ks1868-m365-integration-db-pool-error-and-ready-hook-unreadable-throw.test.ts'
def guard_dl(ind):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"let cause: string | null | undefined;\n"+s+"let code: unknown;\n"+s+"try {\n"
            +s+"  const m = err?.message;\n"+s+"  const cm = err?.cause?.message;\n"
            +s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"  cause = cm === undefined || cm === null ? cm : String(cm);\n"+s+"  code = err?.cause?.code;\n"
            +s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"  cause = undefined;\n"+s+"  code = undefined;\n"+s+"}\n")
D_O="  } catch (err: any) {\n    logger.warn('[Graph] downloadAndHashItem failed', { error: err?.message, cause: err?.cause?.message, code: err?.cause?.code, itemId });\n"
D_N="  } catch (err: any) {\n"+guard_dl(4)+"    logger.warn('[Graph] downloadAndHashItem failed', { error: reason, cause, code, itemId });\n"
site('p1','m365-integration','src/sharepoint/client.ts',[(D_O,D_N)],1,
  '236-237 (the catch of `downloadAndHashItem`)',
  'the catch of `downloadAndHashItem` in `src/sharepoint/client.ts`',
  'the unguarded thrown-value reads in the ONE catch of the SharePoint `downloadAndHashItem` (`err?.message`, `err?.cause?.message`, `err?.cause?.code` in the warn line); the other functions of the file have no catch',
  "The catch of `downloadAndHashItem` passes `err?.message`, `err?.cause?.message` and `err?.cause?.code` straight into the warn line's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws; an Error whose `cause` is such a value) makes the catch throw, so `downloadAndHashItem` REJECTS where an ordinary Error is logged and it resolves `null`; an Error whose `message` is readable but not a string (a Symbol) is handed to `JSON.stringify` uncoerced and silently dropped from the line. The fix is the house guard placed before the log call: read the message and the cause message once inside one `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, read the cause code in the same `try`, and fall back to the constant `'unreadable thrown value'` (cause and code `undefined`) when a read or a coercion throws; then `error: reason, cause, code`.",
  "CALLERS: the document sync route in `src/index.ts` (line 1042) awaits `downloadAndHashItem(...)`; a `null` answer becomes `502 BAD_GATEWAY` ('The Graph API call succeeded but the document could not be retrieved ...'), a rejection goes to the route's catch and `next(error)` (the error handler, 500). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at warn level and the function resolves `null` (502). Today (hostile value): the catch throws while building the log call, the function rejects and the route answers through `next(error)`. After: the failure is logged with text and the route answers 502 as for an ordinary Error. Persisted state: none (the sync row is saved only after a successful download). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, `downloadAndHashItem` logs text and resolves `null` (the sync route answers 502) instead of rejecting (the route's `next(error)` path); a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 2 (the route's response changes from the error handler's answer to the 502 an ordinary Error already gets).",
  "Premise: `sharepoint/client.ts` lines 155-240 and `index.ts` lines 1030-1075 read",
  't93_p1.ts.txt',
  "The service logger is a plain recording object; the global `fetch` is a plain function rejecting with the cell's value; the Graph readiness flag is set through the real `initGraphClient()` with stand-in `ENTRA_*` variables; no network.",
  '6 cells: C1, C2 controls, R1 to R4 red',
  "'control ks1868 C1' (an ordinary Error with a cause) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` to `R4` (the metadata fetch rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws, an Error whose cause is a revoked Proxy) (4 cells)", 4,
  'm365_sharepoint_download_and_hash_item_catch_guard_message',
  "At the tip the catch throws before logging (the call rejects) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=M365REF,
  testbase='ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts')

# ---- P2: originate routes/webhooks.ts dispatchEvent outer catch (jest)
def guard_dot(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = %s.message;\n"%var+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
W_O="  } catch (err: any) {\n    logger.warn('Webhook dispatch failed', { eventType, error: err.message });\n    return 0;\n"
W_N="  } catch (err: any) {\n"+guard_dot(4)+"    logger.warn('Webhook dispatch failed', { eventType, error: reason });\n    return 0;\n"
site('p2','originate','src/routes/webhooks.ts',[(W_O,W_N)],1,
  '552-554 (the outer catch of `dispatchEvent`)',
  'the outer catch of `dispatchEvent` in `src/routes/webhooks.ts`',
  'the unguarded thrown-value read in the ONE outer catch of `dispatchEvent`; the secret-decrypt catch of `decryptWebhookSecret` (line 61) is deliberately NOT touched: guarding it would let a delivery proceed signed with an empty secret where today the dispatch aborts',
  "The outer catch of `dispatchEvent` passes `err.message` straight into the logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `dispatchEvent` REJECTS where an ordinary Error is logged and it resolves `0`; an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced and dropped from the JSON line. The fix is the house guard placed before the log call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. (The read stays `err.message`, not `err?.message`: a null or undefined rejection value now logs the constant instead of rejecting.)",
  "CALLERS: `dispatchEvent` is the best-effort event fan-out other parts of the service call when a document or certification event happens (subscriptions with HMAC-signed deliveries); the callers do not use the count for control flow beyond reporting it. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at warn level (`Webhook dispatch failed`) and `dispatchEvent` resolves `0`. Today (hostile value): the catch throws while building the log call and `dispatchEvent` rejects. After: the failure is logged with text and `dispatchEvent` resolves `0` as for an ordinary Error. Persisted state: none (the delivery-history insert is inside the loop and not reached when the request itself rejects). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value (and a null or undefined rejection) only, `dispatchEvent` logs text and resolves `0` instead of rejecting; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 3 (best-effort notification; log-and-return).",
  "Premise: `webhooks.ts` lines 485-556 and `deliverWebhook` lines 433-470 read",
  't93_p2.ts.txt',
  "The database stand-in answers one active webhook row; the shared module is the `makeSharedMock` stand-in with a plain-function outbound request rejecting with the cell's value; the auth middleware and the service logger are plain stand-ins; no database, no network.",
  '5 cells: C1, C2 controls, R1 to R3 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` to `R3` (the delivery request rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws) (3 cells)", 3,
  'originate_webhooks_dispatch_event_catch_guard_message',
  "At the tip the catch throws before logging (`dispatchEvent` rejects) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='jest', ref=JREF,
  testbase='ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts')

# ---- P3: prism index.ts loadFromDb catch (vitest)
PR_O="  } catch (err: any) {\n    logger.warn('Failed to load credentials from DB', { error: err?.message });\n"
PR_N="  } catch (err: any) {\n"+guard(4)+"    logger.warn('Failed to load credentials from DB', { error: reason });\n"
site('p3','prism','src/index.ts',[(PR_O,PR_N)],1,
  '291-292 (the catch of `loadFromDb`)',
  'the catch of `loadFromDb` in `src/index.ts`',
  'the unguarded thrown-value read in the ONE catch of the prism `loadFromDb`; the catches of `dbSaveDID` (line 163) and `dbSaveCredential` (line 233) are deliberately NOT touched (route-reached, separate pass)',
  "The catch of `loadFromDb` passes `err?.message` straight into the warn line's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `loadFromDb` REJECTS, and with it the ready hook the database module runs (`initDb(loadFromDb)`), where an ordinary Error is logged and `loadFromDb` resolves (the credential cache stays empty); an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced and silently dropped from the JSON line. The fix is the house guard placed before the log call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`.",
  "CALLERS: `loadFromDb` is passed to `initDb` as its ready hook (line 891): the database module runs it on the boot success path and again on a later background recovery (KS-382, KS-377). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at warn level and `loadFromDb` resolves; the credential cache stays empty and lookups fall back to the database. Today (hostile value): the catch throws while building the log call and `loadFromDb` rejects into the database module's ready-hook handling. After: the failure is logged with text and `loadFromDb` resolves as for an ordinary Error. Persisted state: none (a read). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, `loadFromDb` logs text and resolves instead of rejecting; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 3 (boot-time cache warm; log-and-continue).",
  "Premise: `index.ts` lines 268-296 and 884-897 read",
  't93_p3.ts.txt',
  "The real `index.ts` (it listens on an ephemeral port at import); `./db` is a plain stand-in that is available, hands over the ready hook and rejects the credentials query once the cell arms it; the service logger is a plain recording object; no database, no network.",
  '5 cells: C1, C2 controls, R1 to R3 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` to `R3` (the credentials query rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws) (3 cells)", 3,
  'prism_index_load_from_db_catch_guard_message',
  "At the tip the catch throws before logging (`loadFromDb` rejects) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-prism-index-load-from-db-catch-unreadable-throw.test.ts')

# ---- P4: originate services/anchorStateSync.ts healAnchorForVerify write catch (jest)
A_O="      logger.warn('Verify heal: the confirmed write failed (presentation unaffected)', { documentId: input.documentId, error: err instanceof Error ? err.message : String(err) });\n"
A_N=guard_e(6)+"      logger.warn('Verify heal: the confirmed write failed (presentation unaffected)', { documentId: input.documentId, error: reason });\n"
site('p4','originate','src/services/anchorStateSync.ts',[(A_O,A_N)],1,
  '599-600 (the catch around the confirmed write of `healAnchorForVerify`)',
  'the catch around the confirmed write of `healAnchorForVerify` in `src/services/anchorStateSync.ts`',
  'the unguarded thrown-value read in the ONE catch around the convergence write of `healAnchorForVerify`; the reconcile paths of the file are deliberately NOT touched',
  "The catch around the conditional blob write of `healAnchorForVerify` logs `{ error: err instanceof Error ? err.message : String(err) }` with the read INSIDE the logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: `instanceof` throws; an Error whose `message` getter throws) makes the catch throw, so `healAnchorForVerify` REJECTS and the verify presents nothing, where an ordinary Error is logged as 'presentation unaffected' and the healed blob is returned. The fix is the house guard placed before the logger call: the SAME expression inside a `try`, with the constant `'unreadable thrown value'` when it throws; then `error: reason`.",
  "CALLERS: `healVerifyRow` in `src/routes/verification.ts` (v1 verify and v2 verify) awaits `healAnchorForVerify` and presents the blob it returns. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at warn level ('Verify heal: the confirmed write failed (presentation unaffected)') and the healed (confirmed) blob is returned for presentation; the stored row is converged later by the GET reconcile and the poller. Today (hostile value): the catch throws while building the log call and the heal rejects into the verify route. After: the failure is logged with text and the confirmed blob is presented as for an ordinary Error. Persisted state: none from the heal (the write failed in both cases). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, `healAnchorForVerify` logs text and returns the healed blob instead of rejecting; every readable value behaves exactly as before. TIER 2 (a verify response: the heal result is presented where today the route fails).",
  "Premise: `anchorStateSync.ts` lines 561-606 read; the harness shape is `ks1384-r2b-verify-heals.test.ts`",
  't93_p4.ts.txt',
  "The document repository is a stand-in whose conditional blob write is a plain function rejecting with the cell's value; the anchoring fetch is the existing `verifyHealFetch` helper (a failed own row, own-create finding the bound create tx); the service logger is a plain recording object; no database, no network.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (the conditional write rejects with a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'originate_anchor_state_sync_heal_write_catch_guard_message',
  "At the tip the catch throws before logging (the heal rejects), so the assertion fails",
  reuse=REUSE_E, runner='jest', ref=JREF,
  testbase='ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts')

# ---- P5: auth userRepo.ts reencryptMfaSecretIfLegacy + reencryptPlatformAdminMfaSecretIfLegacy catches (vitest)
U_O1="  } catch (err: any) {\n    // Never fail the verify on a migration hiccup — just log.\n    logger.error('[KS-158] mfa_secret re-encrypt failed', { userId, error: err?.message });\n"
U_N1="  } catch (err: any) {\n    // Never fail the verify on a migration hiccup — just log.\n"+guard(4)+"    logger.error('[KS-158] mfa_secret re-encrypt failed', { userId, error: reason });\n"
U_O2="  } catch (err: any) {\n    // Never fail the login on a migration hiccup — just log.\n    logger.error('[KS-171] platform_admins.mfa_secret re-encrypt failed', { adminId, error: err?.message });\n"
U_N2="  } catch (err: any) {\n    // Never fail the login on a migration hiccup — just log.\n"+guard(4)+"    logger.error('[KS-171] platform_admins.mfa_secret re-encrypt failed', { adminId, error: reason });\n"
site('p5','auth','src/repositories/userRepo.ts',[(U_O1,U_N1),(U_O2,U_N2)],2,
  '1913-1914 and 1981-1982 (the catches of `reencryptMfaSecretIfLegacy` and `reencryptPlatformAdminMfaSecretIfLegacy`)',
  'the catches of `reencryptMfaSecretIfLegacy` and `reencryptPlatformAdminMfaSecretIfLegacy` in `src/repositories/userRepo.ts`',
  'the unguarded thrown-value reads in the TWO catches of the lazy MFA-secret re-encryption helpers; every other catch of the file (the decrypt helpers, the lookups that branch on `isInfrastructureDbError(err)`, the demo seed) is deliberately NOT touched',
  "Two catches pass `err?.message` straight into the error line's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so the helper REJECTS although its own comments say it must never fail the verify or the login ('Never fail the verify on a migration hiccup - just log'; 'never throws - a migration hiccup must not fail the login'), where an ordinary Error is logged and the helper resolves; an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced and silently dropped from the JSON line. The fix is the house guard placed before each log call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`.",
  "CALLERS: the MFA verify path awaits `reencryptMfaSecretIfLegacy(userId)` after a successful verification, and the platform-admin MFA verify path awaits `reencryptPlatformAdminMfaSecretIfLegacy(adminId)`; neither uses a return value. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at error level and the helper resolves, so the verify / login proceeds with the legacy plaintext secret left in place for a later retry. Today (hostile value): the catch throws while building the log call and the helper rejects into the verify / login route, failing a verification that already succeeded. After: the failure is logged with text and the route proceeds as for an ordinary Error. Persisted state: none from the helper (the failed query wrote nothing). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, each helper logs text and resolves instead of rejecting (the login / verify route no longer fails on the unreadable value); a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 2 (an auth route: a login / MFA verify that failed on this value now completes).",
  "Premise: `userRepo.ts` lines 1889-1916 and 1950-1984 read",
  't93_p5.ts.txt',
  "The shared module is spread from the real one with the crypto functions as plain stand-ins; the subject-DEK store and the service logger are plain stand-ins; `../db` and `pg` are plain stand-ins whose queries reject with the cell's value (the platform URL variable is set for the admin cells); no database.",
  '9 cells: C1 to C3 controls, R1 to R6 red',
  "'control ks1868 C1' (an ordinary Error, mfa), 'C2' (a thrown plain string, mfa) and 'C3' (an ordinary Error, platform admin), all already true at the tip (3 cells)",
  "`R1` to `R3` (mfa) and `R4` to `R6` (platform admin): a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws (6 cells)", 6,
  'auth_user_repo_mfa_reencrypt_catches_guard_message',
  "At the tip the catch throws before logging (the helper rejects) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts')
