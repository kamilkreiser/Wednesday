# Operator 92 sites (KS-1868). Built by mk91.py (exec'd into its namespace: T, SV, OS, mk available).
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
      reuse=reuse, dir='ks_1868_o92_%s_%s'%(k,name), prod=SV+svc+'/'+rel, edits=edits, nh=nh, lines=lines,
      test=SV+svc+'/src/__tests__/'+testbase, tsrc=tsrc, fn=fn, short=short, premise=premise, whatwrong=whatwrong, callers=callers,
      ncells=ncells, red1=red1, dbnote=dbnote, greens=greens, redcells=redcells,
      redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,nred+1)))
def guard_s(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? undefined : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
SOr=SV+'originate/'
JREF=SOr+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
HELD_NOTE="Held READY files of other operators edit this product file at other hunks (named in the report); the hunks of this brief are disjoint from them by more than 3 lines."

# ---- P1: originate documentRepo.ts getDocument / listDocuments / updateDocument catches (jest)
P1_O1="  } catch (err: any) {\n    if (!err?.message?.includes('invalid input syntax for type uuid')) {\n      logger.warn('DB read failed', { error: err instanceof Error ? err.message : String(err) });\n    }\n    throw err;\n"
P1_N1=("  } catch (err: any) {\n    let reason: string;\n    let isUuidSyntax = false;\n    try {\n"
       "      isUuidSyntax = !!err?.message?.includes('invalid input syntax for type uuid');\n"
       "      reason = err instanceof Error ? err.message : String(err);\n    } catch {\n      isUuidSyntax = false;\n      reason = 'unreadable thrown value';\n    }\n"
       "    if (!isUuidSyntax) {\n      logger.warn('DB read failed', { error: reason });\n    }\n    throw err;\n")
P1_O2="  } catch (err: any) {\n    logger.warn('DB list failed', { error: err instanceof Error ? err.message : String(err) });\n"
P1_N2="  } catch (err: any) {\n"+guard_e(4)+"    logger.warn('DB list failed', { error: reason });\n"
P1_O3="  } catch (err: any) {\n    logger.error('DB update failed for document', { id, error: err instanceof Error ? err.message : String(err) });\n"
P1_N3="  } catch (err: any) {\n"+guard_e(4)+"    logger.error('DB update failed for document', { id, error: reason });\n"
site('p1','originate','src/repositories/documentRepo.ts',[(P1_O1,P1_N1),(P1_O2,P1_N2),(P1_O3,P1_N3)],3,
  '264-267, 297-298 and 696-697 (the catches of `getDocument`, `listDocuments` and `updateDocument`)',
  'the read catch of `getDocument`, the list catch of `listDocuments` and the update catch of `updateDocument` in `src/repositories/documentRepo.ts`',
  'the unguarded thrown-value reads in THREE catches of the originate document repository (getDocument, listDocuments, updateDocument); the write catch of `saveDocument` (line 517) and its inner foreign-key catch (line 503) are deliberately NOT touched',
  "Three catches of this repository log the thrown value inside the logger call's arguments, unguarded (`err instanceof Error ? err.message : String(err)`; the getDocument catch also opens with `err?.message?.includes('invalid input syntax for type uuid')`, which throws first). A thrown value whose read throws (a revoked Proxy: `instanceof` and `.message` throw; an Error whose `message` getter throws) therefore throws INSIDE the catch, so the line is never written and the caller receives the TypeError the read threw instead of the original value that every ordinary failure rethrows. The fix is the house guard placed before each logger call: the SAME expression inside a `try`, with the constant `'unreadable thrown value'` when it throws; for `getDocument` the uuid-syntax test moves into the same `try` (a throw there counts as not a uuid-syntax refusal, so the failure is logged). Then `error: reason`. The `throw err` lines are untouched.",
  "CALLERS: `getDocument` is awaited by the document routes (`src/routes/documents.ts`, many handlers), `updateDocument` by the routes and the anchor pollers, `listDocuments` by the list route. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): each catch logs at warn/error level and rethrows the ORIGINAL error; the uuid-syntax refusal of `getDocument` is rethrown unlogged. Today (hostile value): the catch throws while building the log arguments, so nothing is logged and the caller sees a TypeError instead of the original value. After: each catch logs text and rethrows the original value, exactly as for an ordinary Error. Persisted state: none changed by the catches (the update catch runs after the failed write). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the three lines are logged as text and the ORIGINAL value is rethrown (instead of a TypeError from the failed read); every string message, every non-Error throw and every uuid-syntax refusal behave exactly as before. NOT TOUCHED and why: `saveDocument` catch (line 517) is reached by a hostile value only through the inner foreign-key catch at line 503, whose message read DRIVES control flow (the owner-less retry) and is a separate site. TIER 2 (originate document repository: the read, list and write path of every document route; log-and-rethrow catches only). "+HELD_NOTE,
  "Premise: `documentRepo.ts` lines 238-270, 273-300 and 685-700 read",
  't92_p1.ts.txt',
  "The `../db` module and the service logger are plain stand-ins; the database stand-in is passed as the `db` argument (the read stand-in rejects every query with the thrown value; the update stand-in answers one stored row and rejects the write); no database.",
  '10 cells: C1 to C4 controls, R1 to R6 red',
  "'control ks1868 C1' (an ordinary Error from the read), 'C2' (a uuid-syntax Error from the read, not logged), 'C3' (list) and 'C4' (update), all already true at the tip (4 cells)",
  "`R1`, `R2` (the read rejects with a revoked Proxy, an Error whose message getter throws), `R3`, `R4` (the list) and `R5`, `R6` (the update) (6 cells)", 6,
  'originate_document_repo_read_list_update_catches_guard_message',
  "At the tip the catch throws before logging (nothing is logged and the rejection is the TypeError of the failed read, not the original value), so the assertion fails",
  reuse=REUSE_E, runner='jest', ref=JREF,
  testbase='ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts')

# ---- P2: originate routes/documents.ts GET /:id outer catch (jest)
P2_O="    } catch (error) {\n      logger.error('Failed to get document', { error: error instanceof Error ? error.message : String(error) });\n"
P2_N="    } catch (error) {\n"+guard_e(6,'error')+"      logger.error('Failed to get document', { error: reason });\n"
site('p2','originate','src/routes/documents.ts',[(P2_O,P2_N)],1,
  '1231-1232 (the outer catch of `GET /:id`)',
  'the outer catch of the `GET /api/documents/:id` handler in `src/routes/documents.ts`',
  'the unguarded thrown-value read in the ONE outer catch of the originate GET /:id route; the inner catch of the document read (line 1126, `dbErr?.message?.includes(...)`) is deliberately NOT touched',
  "The outer catch of GET /:id logs `{ error: error instanceof Error ? error.message : String(error) }` with the read INSIDE the logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: `instanceof` throws; an Error whose `message` getter throws) therefore throws INSIDE the catch, so the response `500 INTERNAL_ERROR` is never sent: the request hangs and the async handler's rejection is unhandled. The fix is the house guard placed before the logger call: the SAME expression inside a `try`, with the constant `'unreadable thrown value'` when it throws; then `error: reason`. The `res.status(500)` line is untouched. NOTE: a hostile value thrown by the document read itself is turned into a TypeError by the inner `dbErr?.message?.includes('does not exist')` catch (line 1126) before it reaches this catch; that inner catch drives control flow and is a separate, untouched site, so the cells throw from the anchor-state re-check that follows the ownership check.",
  "CALLERS: the Express router mounts `documentsRouter.get('/:id')` for every authenticated document read. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged and the route answers `500 { error: { code: 'INTERNAL_ERROR', message: 'Failed to get document' } }`. Today (hostile value): the catch throws while building the log arguments, no response is sent and an unhandled rejection is raised. After: the line is logged with text and the same 500 is sent. Persisted state: none (a read route). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, GET /:id answers the constant 500 and logs text instead of hanging with an unhandled rejection; every string message and every non-Error throw behave exactly as before. NOTE for the raise seat: open PR 1964 edits OTHER catches of the same file (hunks at 1282, 1363, 3193, 3464, 3653, 3714), disjoint from this one by more than 40 lines; held READY files KS-1709 (hunk at 1196) and O83-P2/P3 edit it too, also disjoint. TIER 2 (originate document read route; response unchanged for an ordinary Error). ",
  "Premise: `routes/documents.ts` lines 1098-1130 and 1228-1236 read",
  't92_p2.ts.txt',
  "The document repository, the anchor-state module, the share and lifecycle repositories, the event bus, the thread-token client, the verification route, the auth and RBAC middleware and the logger are plain stand-ins (the document read answers one owned document; the anchor-state re-check rejects with the thrown value); the real route module is mounted on a real Express app on an ephemeral port; no database.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (the anchor-state re-check rejects with a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'originate_documents_get_by_id_outer_catch_guard_message',
  "At the tip the catch throws before logging (no response is sent: the request is aborted by the cell's timeout and the rejection is unhandled), so the assertion fails",
  reuse=REUSE_E, runner='jest', ref=JREF,
  testbase='ks1868-originate-documents-get-by-id-catch-unreadable-throw.test.ts')
T['p2']['openpr']="Open PR 1964 lists this file (it edits six OTHER catches, hunks at lines 1282, 1363, 3193, 3464, 3653 and 3714; read 2026-11-03 from the PR diff) but not the hunk of this brief (about 1231) and not the new test file name; held READY files of other operators edit it at 1196 (KS-1709) and at the O83-P2/P3 hunks, also disjoint. The 20 open PRs read 2026-11-03 through the GitHub API; 110 file entries; planted control services/originate present in 8 entries."
T['p2']['premise_pr']="Open PRs: 20 read 2026-11-03 via the GitHub REST API; PR 1964 lists `"+SV+"originate/src/routes/documents.ts` with six hunks (1282, 1363, 3193, 3464, 3653, 3714 in the old file; PR diff read 2026-11-03), none within 40 lines of the hunk of this brief; neither new test file of PR 1964 shares this brief's test file name (110 file entries; planted control services/originate appears in 8 file entries)."

# ---- P3: referral referralService.ts dbSaveReferralCode / dbGetCodeByString catches (vitest)
P3_O1="    } catch (err: any) { logger.error('DB save code failed', { error: err?.message }); }\n"
P3_N1="    } catch (err: any) {\n"+guard(6)+"      logger.error('DB save code failed', { error: reason });\n    }\n"
P3_O2="    } catch (err: any) {\n      logger.error('DB read code by string failed', { error: err?.message, code });\n"
P3_N2="    } catch (err: any) {\n"+guard(6)+"      logger.error('DB read code by string failed', { error: reason, code });\n"
site('p3','referral','src/services/referralService.ts',[(P3_O1,P3_N1),(P3_O2,P3_N2)],2,
  '68 (the catch of `dbSaveReferralCode`) and 228-229 (the catch of `dbGetCodeByString`)',
  'the save catch of `dbSaveReferralCode` and the read catch of `dbGetCodeByString` in `src/services/referralService.ts`',
  'the unguarded thrown-value reads in TWO catches of the referral service (dbSaveReferralCode, dbGetCodeByString); the other DB catches of the file are deliberately NOT touched (four read catches belong to held pass O90-P11, the rest are separate briefs)',
  "Two catches of the referral service pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `dbSaveReferralCode` and `dbGetCodeByString` REJECT where an ordinary Error is logged and swallowed (the save returns, the read returns `null`); an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced. The fix is the house guard placed before each logger call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The one-line catch of the save is expanded to a block so the guard fits; nothing else changes.",
  "CALLERS: `dbSaveReferralCode` is awaited by `generateCode` (line 363), `deactivateCode` (line 408) and the apply path (line 488); `dbGetCodeByString` by `generateCode` (line 333, the custom-code uniqueness check) and `getCodeByString` (line 379). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged and swallowed: the save returns and the caller carries on with the in-memory code, the read returns `null` (so a custom code is treated as free and `getCodeByString` answers `undefined`). Today (hostile value): the catch throws while building the log arguments and the public method rejects. After: the failure is logged with text and the ordinary-Error outcome follows. Persisted state: none changed by the catches. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, `generateCode` and `getCodeByString` follow their existing failure paths (log, carry on, `null`/`undefined`) instead of rejecting with the TypeError of the failed read; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. **RAISE-ORDER CONSTRAINT: this file is ALSO edited by held pass O90-P11 (hunks at old lines 165, 177, 201, 213; the four DB read catches around lines 167-216). The hunks are disjoint from this brief by 12 lines or more, but this PR must be raised AFTER the referral PR carrying O90-P11 merges, and against the post-merge tip.** TIER 2 (referral code issuance and lookup; log-and-fallback catches only).",
  "Premise: `referralService.ts` lines 58-69 and 221-232 read",
  't92_p3.ts.txt',
  "The `../db` module is a plain stand-in whose `query` rejects only the one statement under test (matched by a fragment of its SQL) and answers an empty result for every other; the service logger is a plain recording object; the real service module runs; no database.",
  '6 cells: C1, C2 controls, R1 to R4 red',
  "'control ks1868 C1' (an ordinary Error from `getCodeByString`) and 'C2' (an ordinary Error from the code save of `generateCode`), both already true at the tip (2 cells)",
  "`R1`, `R2` (the code read rejects with a revoked Proxy, an Error whose message getter throws) and `R3`, `R4` (the code save, same two values) (4 cells)", 4,
  'referral_service_save_code_and_get_code_by_string_catches_guard_message',
  "At the tip the catch throws before logging (nothing is logged and the public method rejects), so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts')
T['p3']['openpr']="No open PR lists this file or the new test file name (the 20 open PRs read 2026-11-03 through the GitHub API; 110 file entries; planted control services/originate present in 8 entries). Held pass O90-P11 edits four other read catches of this file (see the raise-order note)."
T['p3']['premise_pr']="Open PRs: 20 read 2026-11-03 via the GitHub REST API; none lists `"+SV+"referral/src/services/referralService.ts` or the new test file (110 file entries; planted control services/originate appears in 8 file entries). Held READY O90-P11 edits the same file at old lines 165-219; this brief's hunks are at 68 and 228."

# ---- P4/P5: prism / timestamping db.ts probeDb catch (vitest)
def probe_site(k, svc, extra_dbnote, dbl):
    O="    dbAvailable = false;\n    return { ok: false, error: err?.message };\n"
    N="    dbAvailable = false;\n"+guard_s(4)+"    return { ok: false, error: reason };\n"
    site(k,svc,'src/db.ts',[(O,N)],1,
      '%d-%d (the catch of `probeDb`)'%(dbl,dbl+1),
      'the catch of `probeDb` in `src/db.ts`',
      'the unguarded thrown-value read in the ONE catch of the %s availability probe'%svc,
      "The catch of `probeDb` returns `{ ok: false, error: err?.message }`, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `probeDb` REJECTS where an ordinary Error resolves `{ ok: false, error }`: `initDb` rejects at boot instead of resolving false, and a failed background re-probe rejects inside the retry timer (an unhandled rejection that also ENDS the retry chain, because the next `scheduleRetry` call is never reached, so the service stays in degraded mode for good); an Error whose `message` is readable but not a string (a Symbol) is handed to `JSON.stringify` uncoerced and silently dropped from the unavailable line. The fix is the house guard before the return: read the message once inside a `try`, keep `undefined`/`null` as no message, coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The return type `error?: string` does not admit `null`, so the guard variable is typed `string | undefined`.",
      "CALLERS: `initDb` (boot) and the `scheduleRetry` timer callback read `probe.ok` and log `probe.error` in the unavailable / still-unavailable lines; nothing else reads it. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `probeDb` resolves `{ ok: false, error: <message> }`, `initDb` logs the unavailable line and schedules the background retry, and the retry chain continues. Today (hostile value): `probeDb` rejects, so `initDb` rejects and the retry chain ends. After: the ordinary-Error outcome. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, `probeDb` resolves `{ ok: false, error: <text> }` (instead of rejecting), so `initDb` resolves false and the background retry keeps running; a Symbol message is logged as its text; a `null` message is now reported as no message (`error` absent from the line) instead of `\"error\": null`; every string message, every non-Error throw and every absent message behave exactly as before. TIER 3 (availability probe; log and retry only; no data path). Held pass O89-%s edited the pool-error listener of the same file; that change is ALREADY MERGED at the tip (PR 1966), so the file here has no held-pass conflict."%('P1' if svc=='prism' else 'P7'),
      "Premise: `db.ts` lines %d-%d read"%(dbl-4,dbl+3),
      't92_%s.ts.txt'%svc,
      extra_dbnote,
      '5 cells: C1, C2 controls, R1 to R3 red',
      "'control ks1868 C1' (an ordinary Error from the probe query) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
      "`R1` to `R3` (the probe query rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws) (3 cells)", 3,
      '%s_db_probe_db_catch_guard_message'%svc,
      "At the tip the catch throws before the line is logged (`initDb` rejects) or the logged value is not text, so the assertion fails",
      reuse=REUSE_Q, runner='vitest', ref=REFV,
      testbase='ks1868-%s-db-probe-db-catch-unreadable-throw.test.ts'%svc)
probe_site('p4','prism',"The `pg` module is a plain stand-in Pool whose `query` is not used; `@secuura/shared` is replaced by a stand-in whose tenant-scoped query rejects with the thrown value; `console.log` is a plain recording function; each cell loads a fresh copy of the real module (`vi.resetModules()` + dynamic import); `closeDb` is called after each cell; no database.",123)
probe_site('p5','timestamping',"The `pg` module is a plain stand-in Pool whose `query` rejects with the thrown value; `console.log` is a plain recording function; each cell loads a fresh copy of the real module (`vi.resetModules()` + dynamic import); `closeDb` is called after each cell; no database.",98)

# ---- P6: wallet-connector server.ts four DB catches (vitest)
def wc(msg, ind, lead=None):
    return ("%s} catch (err: any) {\n%slogger.%s('%s', { error: err?.message });\n"%(' '*(ind-2),' '*ind,'warn' if False else 'error',msg),
            "%s} catch (err: any) {\n"%(' '*(ind-2))+guard(ind)+"%slogger.error('%s', { error: reason });\n"%(' '*ind,msg))
w1=wc('DB save session failed',4); w2=wc('DB get session failed',6); w3=wc('DB disconnect session failed',6); w4=wc('DB list sessions failed',6)
site('p6','wallet-connector','src/server.ts',[w1,w2,w3,w4],4,
  '66-67 (dbSaveWalletSession), 188-189 (GET session), 216-217 (DELETE session) and 300-301 (GET sessions)',
  'the four database catches of `dbSaveWalletSession`, `GET /api/wallets/session/:sessionId`, `DELETE /api/wallets/session/:sessionId` and `GET /api/wallets/sessions` in `src/server.ts`',
  'the unguarded thrown-value reads in FOUR log-only database catches of the wallet-connector server (save, get, disconnect, list); the boot-time catches (line 87 `loadFromDb`, line 329 subscriber start) are deliberately NOT touched',
  "Four catches of the wallet-connector server pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so the async route handler rejects (Express 4 leaves it unhandled and the request never gets an answer) where an ordinary Error is logged and the route answers as usual; an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced. The fix is the house guard placed before each logger call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The route answers are untouched.",
  "CALLERS: `dbSaveWalletSession` is awaited by `POST /api/wallets/session` (201) and by the disconnect route; the other three catches sit inside their route handlers. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged and swallowed, and the route answers its usual response from the in-memory session map (201 for a new session; 404 NOT_FOUND for an unknown id on the get and the disconnect; 200 with the in-memory sessions for the list). Today (hostile value): the catch throws while building the log arguments, the handler rejects unhandled and the request gets no answer. After: the failure is logged with text and the usual answer is sent. Persisted state: none changed by the catches (the failed statement did not persist in either case). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, the four routes answer as they do for an ordinary Error and log text, instead of an unhandled rejection with no answer; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 3 (wallet session bookkeeping; log-and-continue catches; no money or key path).",
  "Premise: `server.ts` lines 55-70, 177-192, 207-222 and 290-304 read",
  't92_p6.ts.txt',
  "The real `server.ts` app is served on 127.0.0.1 (its boot is held off: `initDb` never settles, the user.erased subscriber is a no-op); `../db` is a plain stand-in that reads as available and rejects every statement with the thrown value; the logger is a plain recording object; the shared JWT check is a stand-in that sets a platform administrator; the test collects `unhandledRejection` events itself (the runner's own listeners are removed for each cell and restored after); no database, no network.",
  '12 cells: C1 to C4 controls, R1 to R8 red',
  "'control ks1868 C1' to 'C4' (an ordinary Error on each of the four routes), all already true at the tip (4 cells)",
  "`R1`, `R2` (POST session), `R3`, `R4` (GET session), `R5`, `R6` (DELETE session) and `R7`, `R8` (GET sessions): a revoked Proxy and an Error whose message getter throws on each (8 cells)", 8,
  'wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message',
  "At the tip the catch throws before logging (the request gets no answer and an unhandled rejection is raised), so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts')

# ---- P7: staking stake.ts verifyDbReady catch (vitest)
S_O="  } catch (err: any) {\n    logger.error('[Staking] Failed to verify DB readiness for stake positions', { error: err?.message });\n"
S_N="  } catch (err: any) {\n"+guard(4)+"    logger.error('[Staking] Failed to verify DB readiness for stake positions', { error: reason });\n"
site('p7','staking','src/routes/stake.ts',[(S_O,S_N)],1,
  '147-148 (the catch of `verifyDbReady`)',
  'the catch of `verifyDbReady` in `src/routes/stake.ts`',
  'the unguarded thrown-value read in the ONE catch of the staking `verifyDbReady`',
  "The catch of `verifyDbReady` passes `err?.message` straight into the logger's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `verifyDbReady` REJECTS where an ordinary Error is logged and the function resolves; an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced. The fix is the house guard placed before the logger call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`.",
  "CALLERS: the service entry (`src/index.ts`) awaits `verifyDbReady()` at boot. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at error level and `verifyDbReady` resolves, so the service boots with empty pool statistics. Today (hostile value): the catch throws while building the log arguments and `verifyDbReady` rejects. After: the failure is logged with text and the function resolves. Persisted state: none (a read of aggregate statistics; the catch writes nothing). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, `verifyDbReady` logs text and resolves instead of rejecting with the TypeError of the failed read; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 3 (boot-time statistics read; log-and-continue).",
  "Premise: `stake.ts` lines 134-149 read",
  't92_p7.ts.txt',
  "The `../db` module is a plain stand-in whose `query` rejects with the thrown value; the service logger is a plain recording object; the real module runs; no database.",
  '5 cells: C1, C2 controls, R1 to R3 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` to `R3` (the query rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws) (3 cells)", 3,
  'staking_verify_db_ready_catch_guard_message',
  "At the tip the catch throws before logging (`verifyDbReady` rejects) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts')

# ---- P8: timestamping index.ts three DB lookup catches (vitest)
def ts_site(msg, meta):
    return ("  } catch (err: any) {\n    log('warn', '%s', { %serror: err?.message });\n"%(msg,meta),
            "  } catch (err: any) {\n"+guard(4)+"    log('warn', '%s', { %serror: reason });\n"%(msg,meta))
t1=ts_site('DB lookup by id failed','id, '); t2=ts_site('DB lookup by document failed','documentId, '); t3=ts_site('DB lookup by hash failed','hash, ')
site('p8','timestamping','src/index.ts',[t1,t2,t3],3,
  '776-777 (`dbGetTimestampById`), 788-789 (`dbGetTimestampsByDocument`) and 800-801 (`dbGetTimestampsByHash`)',
  'the three database lookup catches of `dbGetTimestampById`, `dbGetTimestampsByDocument` and `dbGetTimestampsByHash` in `src/index.ts`',
  'the unguarded thrown-value reads in THREE log-and-fallback lookup catches of the timestamping index (by id, by document, by hash); the other `err?.message` catches of the file (lines 120, 603, 738) are deliberately NOT touched',
  "Three catches of the timestamping index pass `err?.message` straight into the log line's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so the async route handler rejects (Express 4 leaves it unhandled and the request never gets an answer) where an ordinary Error is logged and the lookup answers its fallback (`undefined`, or an empty list); an Error whose `message` is readable but not a string (a Symbol) is handed to `JSON.stringify` uncoerced and silently dropped from the line. The fix is the house guard placed before each log call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The fallback returns are untouched.",
  "CALLERS: `GET /api/timestamps/:id` (404 NOT_FOUND when the lookup answers `undefined`), `GET /api/timestamps/document/:documentId` and `GET /api/timestamps/hash/:hash` (200 with an empty list). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at warn level and the lookup answers its fallback, so the route answers 404 / 200-empty. Today (hostile value): the catch throws while building the log call and the handler rejects unhandled with no answer. After: the failure is logged with text and the usual answer is sent. Persisted state: none (reads). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, the three lookup routes answer as they do for an ordinary Error and log text, instead of an unhandled rejection with no answer; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 2 (timestamp lookup routes; log-and-fallback catches; reads only).",
  "Premise: `index.ts` lines 349-415 and 765-805 read",
  't92_p8.ts.txt',
  "The real `index.ts` app (it listens on an ephemeral port at import and is also served on 127.0.0.1 by the test); `./db` is a plain stand-in that is available, answers the startup statements and rejects only the lookup SELECT once the cell arms it; the shared JWT check is a pass-through stand-in; `console.log` is a plain recording function; the test collects `unhandledRejection` events itself (the runner's own listeners are removed for each cell and restored after); no database, no network.",
  '9 cells: C1 to C3 controls, R1 to R6 red',
  "'control ks1868 C1' to 'C3' (an ordinary Error on each of the three lookup routes), all already true at the tip (3 cells)",
  "`R1`, `R2` (by id), `R3`, `R4` (by document) and `R5`, `R6` (by hash): a revoked Proxy and an Error whose message getter throws on each (6 cells)", 6,
  'timestamping_index_db_lookup_by_id_document_hash_catches_guard_message',
  "At the tip the catch throws before logging (the request gets no answer and an unhandled rejection is raised), so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts')

# ---- P9: referral routes/leaderboard.ts buildLeaderboard catch (vitest)
L_O="  } catch (err: any) {\n    logger.error('Leaderboard DB query failed', { error: err?.message });\n"
L_N="  } catch (err: any) {\n"+guard(4)+"    logger.error('Leaderboard DB query failed', { error: reason });\n"
site('p9','referral','src/routes/leaderboard.ts',[(L_O,L_N)],1,
  '285-286 (the catch of `buildLeaderboard`)',
  'the query catch of `buildLeaderboard` in `src/routes/leaderboard.ts`',
  'the unguarded thrown-value read in the ONE catch of the referral `buildLeaderboard`',
  "The catch of `buildLeaderboard` passes `err?.message` straight into the logger's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `buildLeaderboard` REJECTS and the leaderboard routes take their error path (`next(error)`: a 500) where an ordinary Error is logged and the leaderboard is answered empty; an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced. The fix is the house guard placed before the logger call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. `return [];` is untouched.",
  "CALLERS: `GET /` (all-time), `GET /monthly` and `GET /position/:userId` of the leaderboard router call `buildLeaderboard`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at error level and `buildLeaderboard` returns `[]`, so the route answers 200 with an empty list (and caches the empty list for the cache TTL, as it does for every ordinary failure). Today (hostile value): the catch throws while building the log arguments, the route takes the error path (500) and nothing is cached. After: the ordinary-Error outcome (logged text, 200 with an empty list, empty list cached). Persisted state: none beyond the in-memory cache. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, the leaderboard routes answer an empty 200 (as for an ordinary Error) instead of the error path; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 3 (read-only leaderboard; log-and-empty catch).",
  "Premise: `leaderboard.ts` lines 237-289 read",
  't92_p9.ts.txt',
  "The `../db` module is a plain stand-in whose `query` rejects with the thrown value; the service logger is a plain recording object; the real router is mounted on a real express app on 127.0.0.1, with a fresh copy of the module per cell (`vi.resetModules()` + dynamic import: the all-time cache is module state); no database.",
  '5 cells: C1, C2 controls, R1 to R3 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` to `R3` (the query rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws) (3 cells)", 3,
  'referral_leaderboard_build_leaderboard_catch_guard_message',
  "At the tip the catch throws before logging (the route answers 500) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts')

# ---- P10: transfer index.ts loadFromDb catch (vitest)
X_O="  } catch (err: any) {\n    log('warn', 'Failed to load from DB — starting with empty in-memory state', { error: err?.message });\n"
X_N="  } catch (err: any) {\n"+guard(4)+"    log('warn', 'Failed to load from DB — starting with empty in-memory state', { error: reason });\n"
site('p10','transfer','src/index.ts',[(X_O,X_N)],1,
  '326-327 (the catch of `loadFromDb`)',
  'the catch of `loadFromDb` in `src/index.ts`',
  'the unguarded thrown-value read in the ONE catch of the transfer `loadFromDb`; the catches of `dbSaveTransfer` (line 201) and `dbSaveNotification` (line 288) are deliberately NOT touched',
  "The catch of `loadFromDb` passes `err?.message` straight into the log line's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `loadFromDb` REJECTS, and with it `runDbBootTasks`, which skips `verifyWorkflowDb` and `verifyDelegationDb` that follow it, where an ordinary Error is logged and `loadFromDb` resolves (the service starts with empty in-memory state); an Error whose `message` is readable but not a string (a Symbol) is handed to `JSON.stringify` uncoerced and silently dropped from the line. The fix is the house guard placed before the log call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`.",
  "CALLERS: `runDbBootTasks` (line 1072) awaits `loadFromDb()` and then the two table verifications; it is the `onReady` hook handed to `initDb`, run on the boot success path and again on a later background recovery. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at warn level, `loadFromDb` resolves and the table verifications run. Today (hostile value): the catch throws while building the log call, `loadFromDb` and `runDbBootTasks` reject and the table verifications are skipped. After: the failure is logged with text and the boot tasks continue as for an ordinary Error. Persisted state: none (a read; the caches stay empty in both cases). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, `loadFromDb` logs text and resolves (the boot tasks continue) instead of rejecting; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 3 (boot-time cache warm; log-and-continue).",
  "Premise: `index.ts` lines 291-331 and 1063-1076 read",
  't92_p10.ts.txt',
  "The real `index.ts` (it listens on an ephemeral port at import); `./db` is a plain stand-in that is available, never settles `initDb` and rejects the load query once the cell arms it; `console.log` is a plain recording function; no database, no network.",
  '5 cells: C1, C2 controls, R1 to R3 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` to `R3` (the load query rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws) (3 cells)", 3,
  'transfer_index_load_from_db_catch_guard_message',
  "At the tip the catch throws before logging (`loadFromDb` rejects) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-transfer-index-load-from-db-catch-unreadable-throw.test.ts')

# ---- P11: timestamping index.ts ensureTable catch (vitest)
E_O="  } catch (err: any) {\n    log('warn', 'Failed to ensure ts_timestamps table', { error: err?.message });\n"
E_N="  } catch (err: any) {\n"+guard(4)+"    log('warn', 'Failed to ensure ts_timestamps table', { error: reason });\n"
site('p11','timestamping','src/index.ts',[(E_O,E_N)],1,
  '119-120 (the catch of `ensureTable`)',
  'the catch of `ensureTable` in `src/index.ts`',
  'the unguarded thrown-value read in the ONE catch of the timestamping `ensureTable`; the lookup catches (lines 777, 789, 801) belong to separate pass O92-P8 and the catches at lines 603 and 738 are deliberately NOT touched',
  "The catch of `ensureTable` passes `err?.message` straight into the log line's meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch throw, so `ensureTable` REJECTS and its callers see a failure it never reports where an ordinary Error is logged by `ensureTable` itself, `tableEnsured` stays false (so the creation is retried on the next call) and the caller carries on; an Error whose `message` is readable but not a string (a Symbol) is handed to `JSON.stringify` uncoerced and silently dropped from the line. The fix is the house guard placed before the log call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`.",
  "CALLERS: `verifyDbReady` (boot readiness check, inside its own try/catch that logs `DB verification failed` and answers false) and the persistence and lookup helpers (`dbGetTimestampById` and the others, each with its own catch that logs and answers its fallback). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `ensureTable` logs the failure at warn level and returns; the caller carries on (a later statement against a missing table then fails and is handled by that caller's own catch). Today (hostile value): `ensureTable` throws a TypeError from inside its catch, the caller's catch reports the TypeError instead of the real failure, and the `Failed to ensure ts_timestamps table` line is not written. After: the line is logged with text and the caller carries on as for an ordinary Error. Persisted state: none (the DDL failed in both cases). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, `ensureTable` logs text and returns (instead of rejecting with the TypeError of the failed read), so the boot readiness check reaches its table-count statement exactly as it does for an ordinary Error; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. Raise-order: this file is also edited by pass O92-P8 (hunks at 776-801); the hunks are 650 lines apart and independent. TIER 3 (boot-time DDL guard; log-and-continue).",
  "Premise: `index.ts` lines 88-122 and 733-741 read",
  't92_p11.ts.txt',
  "The real `index.ts` (a fresh copy per cell through `vi.resetModules()` + dynamic import; it listens on an ephemeral port at import); `./db` is a plain stand-in that is available and rejects the CREATE TABLE statement; the shared JWT check is a pass-through stand-in; `console.log` is a plain recording function; the test collects `unhandledRejection` events itself; no database, no network.",
  '5 cells: C1, C2 controls, R1 to R3 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` to `R3` (the table creation rejects with a revoked Proxy, an Error whose message is a Symbol, an Error whose message getter throws) (3 cells)", 3,
  'timestamping_index_ensure_table_catch_guard_message',
  "At the tip the catch throws before logging (`ensureTable` rejects and no 'Failed to ensure' line is written) or the logged value is not text, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=REFV,
  testbase='ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts')
