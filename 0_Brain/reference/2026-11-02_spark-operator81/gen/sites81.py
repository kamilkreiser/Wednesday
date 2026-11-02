# Operator 81 sites: KS-1868 G112-F1 (services/security index.ts + db.ts), vitest.
SEC='Blockchain/Dev/services/security/'
TD=SEC+'src/__tests__/'
IDX=SEC+'src/index.ts'
DBF=SEC+'src/db.ts'
NEWREAD=lambda s: s+"const m = err?.message;\n"+s+"reason = m === undefined || m === null ? m : String(m);\n"
def _ed(ind, tail):
    s=' '*ind
    pre=s[:-2]+"let reason: string;\n"
    # note: the `let` line is at ind-2
    old=(' '*(ind-2))+"let reason: string;\n"+(' '*(ind-2))+"try {\n"+s+"reason = err?.message;\n"+(' '*(ind-2))+"} catch {\n"+s+"reason = 'unreadable thrown value';\n"+(' '*(ind-2))+"}\n"+tail
    new=old.replace(s+"reason = err?.message;\n", NEWREAD(s),1)
    return (old,new)
COMMON=dict(key='KS-1868', runner='vitest', runcmd='run ', rdir='Blockchain/Dev/services/security',
  reuse="This follows the coercing form that PR 1924 merged for the `originate` outer catches and that operator 80's held passes use (`String(...)` inside the same `try`/`catch { reason = 'unreadable thrown value' }`), applied to the guards PR 1930 already merged in this very file. Here the read is first taken into a local `m` and `String(...)` is applied only when `m` is neither undefined nor null, because a thrown plain string or null has no message and today is logged with no `error` (db.ts: returned as `error: undefined`); a bare `String(...)` would newly log or return the text 'undefined' for those. No helper.")
HOST_PROSE="If the getter succeeds and returns a hostile NON-string (a revoked Proxy, an object whose `toString` throws, a null-prototype object, a Symbol), the value is passed on uncoerced: the real winston formatter (and `JSON.stringify` in db.ts's `dbLog`) throws on some of them while formatting, INSIDE the catch, outside the guard (QA gate 112, G112-F1, measured)."
T['p1']=dict(COMMON, dir='ks_1868_o81_p1_security_db_probe_hook_catches_coerce_message', prod=DBF, ref=TD+'ks1868-security-db-probe-and-hook-catches-unreadable-throw.test.ts',
  edits=[_ed(6,"    // Boot work failing must not un-flag an otherwise reachable DB.\n"),_ed(6,"    return { ok: false, error: reason };\n")], nh=2,
  lines='103 (`runDbReadyHook`) and 121 (`probeDb`) (QA gate 112, finding G112-F1, on the file PR 1930 merged into develop)',
  test=TD+'ks1868-security-db-message-coercion-unreadable-throw.test.ts', tsrc='t81_p1.ts.txt',
  fn='the two catches of `db.ts` (`runDbReadyHook`, `probeDb`)',
  short='the `reason = err?.message;` read in TWO catch blocks of `db.ts` (the boot hook and the availability probe)',
  premise="`%s` lines 103 and 121 read `reason = err?.message;` inside the guards PR 1930 added; `reason` is then passed to `dbLog('error', 'DB ready boot work failed', { error: reason })` (line 108) and returned as `error` (line 125) outside the guard" % DBF,
  whatwrong="In `db.ts` the catch of `runDbReadyHook` and the catch of `probeDb` read the thrown value's message in their own `try` (`reason = err?.message;`, constant `unreadable thrown value` when the read throws). The guard covers only the READ. "+HOST_PROSE+" For the boot hook `dbLog` builds its line with `JSON.stringify`, which throws on a revoked Proxy, so `initDb` REJECTS instead of resolving true; for the probe the value is returned as `error` and reaches the same `dbLog` in `initDb`, where `initDb` also rejects. The fix wraps the read: `const m = err?.message; reason = m === undefined || m === null ? m : String(m);` inside the same `try`, so a value that cannot be turned into text throws inside the `try` and the existing `catch` gives the constant.",
  callers="CALLERS: `initDb` (boot, and the background retry timer) is the only caller of both. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a failed probe leaves the database unavailable, logs one warn line with the message and `initDb` resolves false; a failed boot hook logs one error line with the message and `initDb` resolves true (the DB stays flagged available). Today (hostile non-string message, gate 112 measured): `initDb` rejects (and boot's `initDb(...).then` has no catch). After: the ordinary rows, with the constant in the line. Persisted state: none either way. **BEHAVIOUR CHANGE the raise PR must state:** for a readable-but-hostile non-string message only, `initDb` resolves (false for the probe, true for the hook) instead of rejecting; a Symbol message is logged as its text; every string message, and a thrown value with no message, behaves exactly as before.",
  ncells='12 cells: C1 to C4 controls, R1 to R8 red',
  red1="At the tip the hostile message is passed on uncoerced, so the log line does not carry the safe text (or `initDb` rejects) and the assertion fails",
  dbnote="`pg` is replaced by a plain Pool stand-in that rejects with the thrown value; the real `db.ts` runs for each cell (module reloaded per cell); no network, no database, no route.",
  greens="'control ks1868 C1' (an ordinary Error at the probe), 'C2' (an ordinary Error at the boot hook) and 'C3' and 'C4' (a thrown plain string, which has no message, at the probe and at the hook: logged with no `error`), all already true at the tip (4 cells)",
  redcells="`R1` to `R4` (probe: a message that is a revoked Proxy, whose `toString` throws, a null-prototype object, a Symbol) and `R5` to `R8` (boot hook: the same four) (8 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,9)),
  sib="`ks1868-security-db-probe-and-hook-catches-unreadable-throw.test.ts`")
T['p2']=dict(COMMON, dir='ks_1868_o81_p2_security_audit_event_save_catches_coerce_message', prod=IDX, ref=TD+'ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts',
  edits=[_ed(6,"    logger.error('DB save audit log failed', { error: reason });\n"),_ed(6,"    logger.error('DB save event failed', { error: reason });\n")], nh=2,
  lines='179 (`dbSaveAuditLog`) and 201 (`dbSaveSecurityEvent`) (QA gate 112, finding G112-F1, on the file PR 1930 merged into develop)',
  test=TD+'ks1868-security-audit-event-message-coercion-unreadable-throw.test.ts', tsrc='t81_p2.ts.txt',
  fn='the save catches of `dbSaveAuditLog` and `dbSaveSecurityEvent`',
  short='the `reason = err?.message;` read in TWO catch blocks (audit log save, security event save)',
  premise="`%s` lines 179 and 201 read `reason = err?.message;` inside the guards PR 1930 added, and `reason` is then passed to `logger.error('DB save audit log failed' | 'DB save event failed', { error: reason })` outside the guard" % IDX,
  whatwrong="In `index.ts` the save catch of `dbSaveAuditLog` and of `dbSaveSecurityEvent` reads the thrown value's message in its own `try` (`reason = err?.message;`, constant `unreadable thrown value` when the read throws) and logs `{ error: reason }`. The guard covers only the READ. "+HOST_PROSE+" The helper then rejects and `POST /api/audit` or `POST /api/events` answers 500 for a record already kept in memory. The fix wraps the read: `const m = err?.message; reason = m === undefined || m === null ? m : String(m);` inside the same `try`, so a value that cannot be turned into text throws inside the `try` and the existing `catch` gives the constant.",
  callers="CALLERS: `POST /api/audit` and `POST /api/events`, and the other internal callers of the two helpers (all swallow the failure). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): one error log line `{ error: <message> }` and the route answers 201 (record kept in memory, nothing stored in the database). Today (hostile non-string message, gate 112): with the real logger the route answers 500. After: the ordinary 201 and the constant in the log. Persisted state: none either way (the insert failed). **BEHAVIOUR CHANGE the raise PR must state:** for a readable-but-hostile non-string message only, those two routes answer 201 instead of 500; a Symbol message is logged as its text; string messages and a thrown value with no message behave exactly as before.",
  ncells='14 cells: C1 to C4 controls, R1 to R8 red',
  red1="At the tip the hostile message is logged as is, so the safe-text assertion fails",
  dbnote="The db module is replaced by a stand-in whose `query` rejects with the thrown value for the audit and event INSERT only; the logger is replaced by plain recording functions; the real routes run on a loopback listener with an RS256 token.",
  greens="'control ks1868 C1' and 'C2' (an ordinary Error at the audit and the event insert) and 'C3' and 'C4' (a thrown plain string, which has no message, logged with no `error`), all already true at the tip (4 cells)",
  redcells="`R1` to `R4` (audit insert: a message that is a revoked Proxy, whose `toString` throws, a null-prototype object, a Symbol) and `R5` to `R8` (event insert: the same four) (8 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,9)),
  sib="`ks1868-security-audit-and-event-save-catches-unreadable-throw.test.ts`")
T['p3']=dict(COMMON, dir='ks_1868_o81_p3_security_validate_route_catches_coerce_message', prod=IDX, ref=TD+'ks1868-security-validate-route-catches-unreadable-throw.test.ts',
  edits=[_ed(6,"    logger.error('DB save API key failed', { error: reason });\n  }\n}\n\nasync function dbGetApiKey"),
         _ed(8,"      logger.error('KS-1370: stored API key state could not be read', { error: reason });\n"),
         _ed(8,"      logger.warn('DB fallback for api-key validation failed', { error: reason });\n")], nh=3,
  lines='535 (`dbRecordApiKeyUsage`, the usage write), 1929 (validate stored-state read) and 1958 (validate cache-miss lookup) (QA gate 112, finding G112-F1, on the file PR 1930 merged into develop)',
  test=TD+'ks1868-security-validate-message-coercion-unreadable-throw.test.ts', tsrc='t81_p3.ts.txt',
  fn='the usage-write, stored-read and lookup catches on the validate path',
  short='the `reason = err?.message;` read in THREE catch blocks (usage write, stored-state read, cache-miss lookup)',
  premise="`%s` lines 535, 1929 and 1958 read `reason = err?.message;` inside the guards PR 1930 added, and `reason` is then passed to `logger.error('DB save API key failed' | 'KS-1370: stored API key state could not be read', ...)` / `logger.warn('DB fallback for api-key validation failed', ...)` outside the guard" % IDX,
  whatwrong="On the `POST /api/keys/validate` path three catches read the thrown value's message in their own `try` (`reason = err?.message;`, constant `unreadable thrown value` when the read throws) and log `{ error: reason }`: the usage write of `dbRecordApiKeyUsage`, the stored-state read of a cached key (answers 503 `Unable to verify key`) and the cache-miss lookup (falls through to `Key not found`). The guard covers only the READ. "+HOST_PROSE+" The validate handler takes no `next`, so the request is then never answered and an unhandled rejection is raised. The fix wraps the read: `const m = err?.message; reason = m === undefined || m === null ? m : String(m);` inside the same `try`, so a value that cannot be turned into text throws inside the `try` and the existing `catch` gives the constant.",
  callers="CALLERS: `POST /api/keys/validate` (used by the gateway hop and by auth's connector-token caller) and, for the usage write, the other callers of `dbRecordApiKeyUsage`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): stored read: one error line and 503 `SERVICE_UNAVAILABLE`; lookup: one warn line and `Key not found` (valid:false); usage write: one error line and the active key is still answered valid:true (log-only by KS-888 card 3). Today (hostile non-string message, gate 112): with the real logger no answer and an unhandled rejection at all three. After: exactly those ordinary rows. Persisted state: none either way; a stored-revoked key never reaches the usage write. **BEHAVIOUR CHANGE the raise PR must state:** for a readable-but-hostile non-string message only, validate answers (503 / Key not found / valid:true for an ACTIVE key whose usage write failed, the same valid:true an ordinary Error already gets) instead of leaving the request unanswered; this is a TIER 1 path. String messages and a thrown value with no message behave exactly as before.",
  ncells='17 cells: C1 to C5 controls, R1 to R12 red',
  red1="At the tip the hostile message is logged as is, so the safe-text assertion fails",
  dbnote="The db module is replaced by a stand-in whose `query` rejects with the thrown value for the stored read, the lookup or the usage UPDATE; the logger is replaced by plain recording functions; the real routes run on a loopback listener with an RS256 token (the key is minted through POST /api/keys first).",
  greens="'control ks1868 C1' (ordinary Error at the stored read), 'C2' (at the lookup), 'C3' (at the usage write), 'C4' (a thrown plain string at the lookup, logged with no `error`) and 'C5' (no failure, valid, nothing logged), all already true at the tip (5 cells)",
  redcells="`R1` to `R4` (stored read: a message that is a revoked Proxy, whose `toString` throws, a null-prototype object, a Symbol), `R5` to `R8` (lookup: the same four) and `R9` to `R12` (usage write: the same four) (12 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,13)),
  sib="`ks1868-security-validate-route-catches-unreadable-throw.test.ts`")

# ---- P4: api-gateway admin.ts identity catches (G110-F1 class; PR 1928 merged guards not covered by operator 80's G3-G5)
AGW='Blockchain/Dev/services/api-gateway/'
ADM=AGW+'src/routes/admin.ts'
ATD=AGW+'src/__tests__/'
def _eid(tail):
    o=("      let reason: string;\n      try {\n        reason = err instanceof Error ? err.message : String(err);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n"+tail)
    n=o.replace("reason = err instanceof Error ? err.message : String(err);","reason = String(err instanceof Error ? err.message : err);",1)
    return (o,n)
T['p4']=dict(key='KS-1868', runner='vitest', runcmd='run ', rdir='Blockchain/Dev/services/api-gateway', dir='ks_1868_o81_p4_apigateway_admin_identity_route_catches_coerce_message', prod=ADM,
  ref=ATD+'ks1868-admin-identity-seed-catch-unreadable-throw.test.ts',
  reuse="This is the coercing form that PR 1924 merged for the `originate` outer catches (`String(error instanceof Error ? error.message : error)` inside the same `try`), applied to the guards PR 1928 already merged in this very file: the read becomes `String(err instanceof Error ? err.message : err)`, so a non-Error value is still turned into text exactly as before and a hostile message throws INSIDE the existing `try`, where the existing `catch` sets the constant `unreadable thrown value`; no helper. It is the same fix operator 80's held passes make at the other admin.ts guards (organization, forward, export, seed), on three guards they did not cover.",
  edits=[_eid("      log('error', '[Identity] Failed to fetch users', { error: reason });\n"),_eid("      log('error', '[Identity] Failed to fetch organizations', { error: reason });\n"),_eid("      log('error', '[Identity] Failed to update level', { error: reason });\n")], nh=3,
  lines='1288 (GET identity users), 1316 (GET identity organizations) and 1346 (PATCH identity user level) (QA gate 110, finding G110-F1: "several sites"; these three guards are on the file PR 1928 merged into develop and were not in operator 80\'s passes)',
  test=ATD+'ks1868-admin-identity-routes-message-coercion-unreadable-throw.test.ts', tsrc='t81_p4.ts.txt',
  fn='the three identity route catches in `admin.ts`',
  short='the `reason = err instanceof Error ? err.message : String(err);` read in THREE catch blocks (identity users list, identity organizations list, identity user level update)',
  premise="`%s` lines 1288, 1316 and 1346 read `reason = err instanceof Error ? err.message : String(err);` inside the guards PR 1928 added, and `reason` is then passed to `log('error', '[Identity] Failed to fetch users' | 'fetch organizations' | 'update level', { error: reason })` outside the guard" % ADM,
  whatwrong="In `routes/admin.ts` the catch of GET `/api/admin/identity/users`, GET `/api/admin/identity/organizations` and PATCH `/api/admin/identity/users/:id/level` reads the thrown value's message in its own `try` (constant `unreadable thrown value` when the read throws), logs `{ error: reason }` and answers a constant 500. The guard covers only the READ. If the getter succeeds and returns a hostile NON-string (a revoked Proxy, an object whose `toString` throws, a null-prototype object, a Symbol) it is passed to the logger as is, and the real winston Console formatter throws while formatting a revoked Proxy, so the request is never answered (QA gate 110, G110-F1, measured for the sibling guards: NO_RESPONSE plus an unhandled rejection). The fix wraps the read in `String(...)` inside the same `try`.",
  callers="CALLERS: HTTP, the three identity routes, SYSTEM_ADMIN only (`requireAdmin`), via the gateway. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): one error log line `{ error: <message> }` and the constant 500 `{ success:false, error:{ code:'INTERNAL_ERROR', message:'Failed to <fetch identity users|fetch identity organizations|update verification level>' } }`. Today (hostile non-string message, real logger): no answer at all. After: the ordinary constant 500 and the constant reason in the log. Persisted state: the PATCH issues its single UPDATE before the catch in either case, so the stored level is the same; no auth change. **BEHAVIOUR CHANGE the raise PR must state:** for a readable-but-hostile non-string message only, these three routes answer the constant 500 instead of leaving the request unanswered; a Symbol message is logged as its text; string messages and non-Error throws behave exactly as before.",
  ncells='15 cells: C1 and C2 x3 routes controls, R1 to R12 red',
  red1="At the tip the hostile message is passed to the logger as is, so the logged reason is not the safe text and the assertion fails",
  dbnote="The route table's last handler is called directly; `query` and `log` are plain stand-ins from the pinned ref suite that reject or record; no database, no network, no app boot.",
  greens="'control ks1868 C1' (an ordinary Error, per route) and 'C2' (a thrown plain string, per route), already true at the tip (6 cells)",
  redcells="`R1` to `R4` (users list), `R5` to `R8` (organizations list) and `R9` to `R12` (level update): a message that is a revoked Proxy, whose `toString` throws, a null-prototype object, a Symbol (12 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,13)),
  sib="`ks1868-admin-identity-seed-catch-unreadable-throw.test.ts`")
