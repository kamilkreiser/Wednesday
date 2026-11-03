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
      reuse=reuse, dir='ks_1868_o94_%s_%s'%(k,name), prod=SV+svc+'/'+rel, edits=edits, nh=nh, lines=lines,
      test=SV+svc+'/src/__tests__/'+testbase, tsrc=tsrc, fn=fn, short=short, premise=premise, whatwrong=whatwrong, callers=callers,
      ncells=ncells, red1=red1, dbnote=dbnote, greens=greens, redcells=redcells,
      redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,nred+1)))
def guard_s(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? undefined : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
SOr=SV+'originate/'
JREF=SOr+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
HELD_NOTE="Held READY files of other operators edit this product file at other hunks (named in the report); the hunks of this brief are disjoint from them by more than 3 lines."


# ---- P1 / P2: mcp-server tools (vitest)
MCPREF=SV+'mcp-server/src/__tests__/ks1868-hash-tool-unreadable-throw.test.ts'
def guard_msg(ind):
    s=' '*ind
    return (s+"let message: string;\n"+s+"try {\n"+s+"  message = err instanceof Error ? err.message : String(err);\n"+s+"} catch {\n"+s+"  message = 'unreadable thrown value';\n"+s+"}\n")
RD="        const message = err instanceof Error ? err.message : String(err);\n"
V1_O="              text: JSON.stringify(formatVerificationResult(result.data as Record<string, unknown>), null, 2),\n            },\n          ],\n        };\n      } catch (err: unknown) {\n"+RD
V1_N=V1_O.replace(RD,guard_msg(8))
V2_O="                null,\n                2,\n              ),\n            },\n          ],\n        };\n      } catch (err: unknown) {\n"+RD
V2_N=V2_O.replace(RD,guard_msg(8))
V3_O="        } catch (err: unknown) {\n          const message = err instanceof Error ? err.message : String(err);\n          results.push({ input: doc, verified: false, error: message });\n"
V3_N="        } catch (err: unknown) {\n"+guard_msg(10)+"          results.push({ input: doc, verified: false, error: message });\n"
site('p1','mcp-server','src/tools/verify.ts',[(V1_O,V1_N),(V2_O,V2_N),(V3_O,V3_N)],3,
  '42-43, 80-81 and 134-135 (the catches of `secuura_verify_by_id`, `secuura_verify_by_file` and `secuura_verify_documents`)',
  'the three catches of the MCP verify tools in `src/tools/verify.ts`',
  'the unguarded thrown-value read in each of the THREE catches of the verify tools (`secuura_verify_by_id`, `secuura_verify_by_file`, `secuura_verify_documents`); the register tools, the hash tool and `http-server.ts` are deliberately NOT touched',
  "Each catch reads `err instanceof Error ? err.message : String(err)` into `message` with no guard. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch throw, so the tool handler REJECTS instead of answering `verified: false`; in the batch tool the throw escapes the `for` loop, so the results already collected for the other documents are lost with it, where an ordinary Error is listed against its own document and the loop goes on. The fix is the house guard placed in each catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The message text of every value that can be read is unchanged.",
  "CALLERS: the MCP SDK calls the handler when an agent invokes the tool and returns the handler's result to the agent; a rejection becomes a protocol-level error instead of the tool's `verified: false` result. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `isError: true` with `{ verified: false, error: <message> }` (the batch tool lists the message against the document). Today (hostile value): the handler rejects. After: the same result with the constant reason. Persisted state: none (a read). **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the tool answers with the constant reason instead of rejecting.",
  "Premise: `verify.ts` read whole",
  't94_p1.ts.txt',
  "The hashing module and the API client are plain stand-ins (`hashFile` resolves a fixed hash unless the cell arms it to reject; `verifyDocument` rejects with the cell's value); the tools are registered on a duck-typed server that records the handlers; no network, no file system.",
  '8 cells: C1 to C3 controls, R1 to R5 red',
  "'control ks1868 C1', 'C2' and 'C3' (an ordinary Error through each of the three tools), already true at the tip (3 cells)",
  "`R1` to `R5` (a revoked Proxy and an Error whose message getter throws through `secuura_verify_by_id`; a revoked Proxy through `secuura_verify_by_file`; a revoked Proxy and an Error whose message getter throws through `secuura_verify_documents`) (5 cells)", 5,
  'mcp_server_verify_tools_catches_guard_message',
  "At the tip the catch throws before returning (the handler rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=MCPREF,
  testbase='ks1868-mcp-server-verify-tools-catches-unreadable-throw.test.ts')

R1_O="      } catch (err: unknown) {\n"+RD+"        return {\n          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],\n"
R1_N="      } catch (err: unknown) {\n"+guard_msg(8)+"        return {\n          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],\n"
R2_O="        } catch (err: unknown) {\n          const message = err instanceof Error ? err.message : String(err);\n          results.push({ success: false, filePath: doc.filePath, error: message });\n"
R2_N="        } catch (err: unknown) {\n"+guard_msg(10)+"          results.push({ success: false, filePath: doc.filePath, error: message });\n"
site('p2','mcp-server','src/tools/register.ts',[(R1_O,R1_N),(R2_O,R2_N)],2,
  '64-65 and 120-121 (the catches of `secuura_register_document` and `secuura_register_documents`)',
  'the two catches of the MCP register tools in `src/tools/register.ts`',
  'the unguarded thrown-value read in each of the TWO catches of the register tools (`secuura_register_document`, `secuura_register_documents`); the verify tools, the hash tool and `http-server.ts` are deliberately NOT touched',
  "Each catch reads `err instanceof Error ? err.message : String(err)` into `message` with no guard. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch throw, so the tool handler REJECTS instead of answering `success: false`; in the batch tool the throw escapes the `for` loop, so the results already collected for the other documents are lost with it, where an ordinary Error is listed against its own document and the loop goes on. The fix is the house guard placed in each catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The message text of every value that can be read is unchanged.",
  "CALLERS: the MCP SDK calls the handler when an agent invokes the tool and returns the handler's result to the agent; a rejection becomes a protocol-level error instead of the tool's `success: false` result. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `isError: true` with `{ success: false, error: <message> }` (the batch tool lists the message against the document). Today (hostile value): the handler rejects. After: the same result with the constant reason. Persisted state: for the batch tool, documents registered earlier in the same call stay registered (the API call is made before the throw); the loss today is only the report of them. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the tool answers with the constant reason instead of rejecting.",
  "Premise: `register.ts` read whole",
  't94_p2.ts.txt',
  "The hashing module and the API client are plain stand-ins (`hashFile` resolves a fixed hash; `registerDocument` rejects with the cell's value); the tools are registered on a duck-typed server that records the handlers; no network, no file system.",
  '6 cells: C1, C2 controls, R1 to R4 red',
  "'control ks1868 C1' and 'C2' (an ordinary Error through each of the two tools), already true at the tip (2 cells)",
  "`R1` to `R4` (a revoked Proxy and an Error whose message getter throws through `secuura_register_document`; the same two through `secuura_register_documents`) (4 cells)", 4,
  'mcp_server_register_tools_catches_guard_message',
  "At the tip the catch throws before returning (the handler rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=MCPREF,
  testbase='ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts')

# ---- P3: timestamping tsa/rfc3161-client.ts submitTimestampRequest catch (vitest)
def guard_tsa(ind):
    s=' '*ind
    return (s+"let timedOut = false;\n"+s+"let reason: string | null | undefined;\n"+s+"try {\n"
            +s+"  timedOut = err?.name === 'TimeoutError' || err?.name === 'AbortError';\n"
            +s+"  const m = err?.message;\n"+s+"  reason = m === undefined || m === null ? m : String(m);\n"
            +s+"} catch {\n"+s+"  timedOut = false;\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
TS_O=("    if (err?.name === 'TimeoutError' || err?.name === 'AbortError') {\n      return {\n        success: false,\n        error: `TSA request timed out after ${TSA_REQUEST_TIMEOUT_MS}ms (${tsaUrl})`,\n      };\n    }\n    return {\n      success: false,\n      error: `TSA request failed: ${err?.message}`,\n    };\n  }\n}\n\n/**\n * Parse an ASN.1")
TS_N=(guard_tsa(4)+"    if (timedOut) {\n      return {\n        success: false,\n        error: `TSA request timed out after ${TSA_REQUEST_TIMEOUT_MS}ms (${tsaUrl})`,\n      };\n    }\n    return {\n      success: false,\n      error: `TSA request failed: ${reason}`,\n    };\n  }\n}\n\n/**\n * Parse an ASN.1")
site('p3','timestamping','src/tsa/rfc3161-client.ts',[(TS_O,TS_N)],2,
  '170-179 (the catch of `submitTimestampRequest`)',
  'the catch of `submitTimestampRequest` in `src/tsa/rfc3161-client.ts`',
  'the unguarded thrown-value reads (`err?.name`, `${err?.message}`) in the ONE catch of `submitTimestampRequest`; the catch of `parseTimestampResponse` (line 279) is deliberately NOT touched (it is not reachable with a hostile value from a Buffer input, so no cell can prove it)',
  "The catch of `submitTimestampRequest` reads `err?.name` in its timeout test and `${err?.message}` in the failed result, both unguarded. `?.` guards null and undefined only: a revoked Proxy throws on both reads, an Error whose `message` getter throws throws on the second, and an Error whose `message` is a Symbol makes the template literal throw a TypeError. In each case the catch throws, so `submitTimestampRequest` REJECTS instead of returning `{ success: false, error }`. The fix is the house guard placed before the returns: read the name test and the message once inside one `try`, fall back to the constant `'unreadable thrown value'` (and not timed out) when the read throws, and coerce a non-text message with `String(...)`. A value that can be read gives exactly the text it gave before.",
  "CALLERS: `requestTimestamp` (same file, line 333) returns it, and `qualified-tsa.ts` imports `requestTimestamp` for the timestamp routes (single and batch); they fall back or report per item on `success: false`, and a rejection instead reaches their own catch. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ success: false, error: 'TSA request failed: <message>' }`, or the timed-out text for TimeoutError/AbortError. Today (hostile value): the function rejects. After: the failed result with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** an unreadable thrown value now gives the failed result with the constant reason instead of a rejection, and a Symbol message is rendered as text instead of throwing; an Error whose `message` getter throws is never treated as a timeout even when its name says so.",
  "Premise: `rfc3161-client.ts` lines 120-180 read",
  't94_p3.ts.txt',
  "The global `fetch` is a plain function rejecting with the cell's value (stubbed with `vi.stubGlobal`, removed after each cell); no network.",
  '5 cells: C1, C2 controls, R1 to R3 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a TimeoutError), both already true at the tip (2 cells)",
  "`R1` to `R3` (a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)", 3,
  'timestamping_tsa_submit_request_catch_guard_message',
  "At the tip the catch throws before returning (the call rejects), so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'timestamping/src/__tests__/ks1868-timestamping-db-pool-error-listener-unreadable-throw.test.ts',
  testbase='ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts')

# ---- P4: originate services/reanchorInFlight.ts isTimeoutError + readInFlightAnchor catch + postReanchor message helper (jest)
I_O="  const name = (err as { name?: unknown } | null)?.name;\n"
I_N="  let name: unknown;\n  try {\n    name = (err as { name?: unknown } | null)?.name;\n  } catch {\n    return false;\n  }\n"
C_O="  } catch (err: unknown) {\n    answer = { httpStatus: null, fetchError: err instanceof Error ? err.message : String(err) };\n"
C_N="  } catch (err: unknown) {\n"+guard_e(4)+"    answer = { httpStatus: null, fetchError: reason };\n"
M_O="  const message = (err: unknown) => (err instanceof Error ? err.message : String(err));\n"
M_N=("  const message = (err: unknown): string => {\n    try {\n      return err instanceof Error ? err.message : String(err);\n    } catch {\n      return 'unreadable thrown value';\n    }\n  };\n")
site('p4','originate','src/services/reanchorInFlight.ts',[(I_O,I_N),(C_O,C_N),(M_O,M_N)],3,
  '53-54, 193 and 229 (`isTimeoutError`, the catch of `readInFlightAnchor`, the `message` helper of `postReanchor`)',
  '`isTimeoutError`, the catch of `readInFlightAnchor` and the `message` helper of `postReanchor` in `src/services/reanchorInFlight.ts`',
  'the unguarded reads of the rejection value in `isTimeoutError`, in the ONE catch of `readInFlightAnchor` and in the `message` helper of `postReanchor`; `ownCreateClient.ts` (its own catch reads the value too) is a separate file and deliberately NOT touched',
  "`isTimeoutError` reads `.name` of the rejection value, the catch of `readInFlightAnchor` reads `err instanceof Error ? err.message : String(err)` and the `message` helper of `postReanchor` reads the same, all unguarded. A value whose read throws (a revoked Proxy; an Error whose `message` getter throws) makes each of them throw, so the fail-safe answers the retry route depends on (`unavailable` for the read, `failed` for the POST) never come back and the call REJECTS. The fix is the house guard in each place: read inside a `try` and fall back to the constant `'unreadable thrown value'` (`false` for `isTimeoutError`). The text of every value that can be read is unchanged.",
  "CALLERS: the retry route (`POST /api/documents/:id/anchor`) awaits `readInFlightAnchor` before it decides whether to pay for an anchor, and awaits `postReanchor` for the paid POST; `isTimeoutError` is also used by `ownCreateClient.ts`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the read becomes `unavailable` (no POST, 503) and the POST becomes `failed` (nothing written as landed). Today (hostile value): the helper throws and the call rejects into the route's own error path. After: the same fail-safe answers with the constant reason. Persisted state: none from these functions. **BEHAVIOUR CHANGE the raise PR must state, and a Claude seat must judge before raising (this is a paid-anchor fail-safe path):** for a rejection value that cannot be read, `isTimeoutError` answers false (so the POST path says `failed` and not `unknown`), the read says `unavailable`, the POST says `failed`.",
  "Premise: `reanchorInFlight.ts` lines 50-56, 160-196 and 216-275 read",
  't94_p4.ts.txt',
  "The fetch implementations are plain functions rejecting with the cell's value, passed as the `fetchImpl` argument; no module is mocked; no network, no database.",
  '8 cells: C1 to C3 controls, R1 to R5 red',
  "'control ks1868 C1' (isTimeoutError on a TimeoutError and an ordinary Error), 'C2' (the read with an ordinary Error) and 'C3' (the POST with an ordinary Error), already true at the tip (3 cells)",
  "`R1` to `R5` (isTimeoutError on a revoked Proxy; the read with a revoked Proxy and with an Error whose message getter throws; the POST with the same two) (5 cells)", 5,
  'originate_reanchor_in_flight_rejection_reads_guard_message',
  "At the tip the helper throws (the call rejects), so the assertion fails",
  reuse=REUSE_E, runner='jest', ref=JREF,
  testbase='ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts')

# ---- P5: billing utils/email.ts sendEmail catch (vitest)
EM_O="  } catch (error) {\n    logger.error('[Email] Send failed', { error: error instanceof Error ? error.message : String(error) });\n"
EM_N="  } catch (error) {\n"+guard_e(4,'error')+"    logger.error('[Email] Send failed', { error: reason });\n"
site('p5','billing','src/utils/email.ts',[(EM_O,EM_N)],1,
  '43-44 (the catch of `sendEmail`)',
  'the catch of `sendEmail` in `src/utils/email.ts`',
  'the unguarded thrown-value read in the ONE catch of `sendEmail`; the template helpers below it have no catch',
  "The catch of `sendEmail` logs `{ error: error instanceof Error ? error.message : String(error) }` with the read INSIDE the logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch throw, so `sendEmail` REJECTS into its caller where an ordinary Error is logged and `false` is returned (it is best-effort). The fix is the house guard placed before the log call: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The logged text of every value that can be read is unchanged.",
  "CALLERS: NONE at the tip: a search of `billing/src` finds only the definition of `sendEmail` (and its template helpers in the same file), so this is a latent site; were it called, a caller would ignore a `false` and a rejection would reach its own error path. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at error level and `sendEmail` resolves `false`. Today (hostile value): `sendEmail` rejects. After: logged with the constant reason and `false` as for an ordinary Error. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, `sendEmail` resolves `false` and logs the constant reason instead of rejecting.",
  "Premise: `email.ts` lines 1-52 read",
  't94_p5.ts.txt',
  "The global `fetch` is a plain function rejecting with the cell's value (stubbed with `vi.stubGlobal`, removed after each cell); the service logger is a plain recording object; `SENDGRID_API_KEY` is set by the cell; no network.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'billing_email_send_email_catch_guard_message',
  "At the tip the catch throws before logging (`sendEmail` rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'billing/src/__tests__/ks1868-billing-webhook-replay-unreadable-throw.test.ts',
  testbase='ks1868-billing-email-send-email-catch-unreadable-throw.test.ts')

# ---- P6: originate routes/health.ts GET /ready timedCheck catch (jest)
H_O="    } catch (err: any) {\n      checks[name] = {\n        status: 'down',\n        latencyMs: Date.now() - start,\n        error: err?.message || 'Unknown error',\n      };\n"
H_N=("    } catch (err: any) {\n      let reason: string;\n      try {\n        reason = String(err?.message || 'Unknown error');\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n      checks[name] = {\n        status: 'down',\n        latencyMs: Date.now() - start,\n        error: reason,\n      };\n")
site('p6','originate','src/routes/health.ts',[(H_O,H_N)],1,
  '58-64 (the catch of `timedCheck` in GET /ready)',
  'the catch of `timedCheck` in `GET /ready` in `src/routes/health.ts`',
  'the unguarded thrown-value read in the ONE catch of `timedCheck`; the database catch of `GET /` (a bare `catch`) reads nothing and is not touched',
  "The catch of `timedCheck` reads `err?.message || 'Unknown error'` into the check entry, unguarded. A thrown value whose read throws (a revoked Proxy; an Error whose `message` getter throws) makes the catch throw, so the check is never recorded as `down`, `Promise.all` rejects and the `GET /ready` handler REJECTS: Express 4 does not catch a rejected async handler, so the probe gets no 503 answer. An ordinary Error gets `{ status: 'down', error: <message> }` and a 503. The fix is the house guard placed before the entry is written: read the message inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The text of every value that can be read is unchanged.",
  "CALLERS: the platform readiness probe calls `GET /ready`; a non-200 takes the instance out of rotation. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the dependency is reported `down` with its message and the probe gets 503. Today (hostile value): the handler rejects and the probe gets no answer. After: 503 with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the check reports `down` with the constant reason instead of the handler rejecting.",
  "Premise: `health.ts` read whole",
  't94_p6.ts.txt',
  "The database client is a plain stand-in whose `$queryRawUnsafe` rejects with the cell's value; `../config` is a plain object; `ioredis` is a plain class whose connect and ping resolve; the handler is taken from the router stack and called with plain request and response stand-ins; no network, no database.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'originate_health_ready_timed_check_catch_guard_message',
  "At the tip the catch throws (the handler rejects), so the assertion fails",
  reuse=REUSE_Q, runner='jest', ref=JREF,
  testbase='ks1868-originate-health-ready-timed-check-catch-unreadable-throw.test.ts')

# ---- P7: originate services/ownCreateClient.ts askOwnCreate catch (jest)
OC_O="    return notAnswered('unanswered', `own-create could not be reached: ${err instanceof Error ? err.message : String(err)}`);\n"
OC_N=guard_e(4)+"    return notAnswered('unanswered', `own-create could not be reached: ${reason}`);\n"
site('p7','originate','src/services/ownCreateClient.ts',[(OC_O,OC_N)],1,
  '87-88 (the outer catch of `askOwnCreate`)',
  'the outer catch of `askOwnCreate` in `src/services/ownCreateClient.ts`',
  'the unguarded message read in the ONE outer catch of `askOwnCreate`; the inner catch around `resp.json()` reads no message, and `isTimeoutError` (in `reanchorInFlight.ts`, guarded by another pass) is not touched',
  "The outer catch of `askOwnCreate` builds the reason with `${err instanceof Error ? err.message : String(err)}` inside a template literal, unguarded. An Error whose `message` getter throws makes the catch throw, so `askOwnCreate`, documented as 'Never throws', REJECTS where an ordinary Error gives `not-answered` (kind `unanswered`) with the reason. The fix is the house guard placed before the return: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The text of every value that can be read is unchanged.",
  "CALLERS: the resolver (`anchorResolution.ts`) and the retry route's step 3 await `askOwnCreate`; `not-answered` makes the resolver write nothing and the route answer 503 with no POST (fail-safe by construction). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ outcome: 'not-answered', kind: 'unanswered', reason: 'own-create could not be reached: <message>', loose: [] }`. Today (hostile value): the call rejects, outside the fail-safe path. After: the same not-answered answer with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state, and a Claude seat must judge (fail-safe path for a paid anchor):** for a value whose message cannot be read, the answer is `not-answered` instead of a rejection.",
  "Premise: `ownCreateClient.ts` read whole",
  't94_p7.ts.txt',
  "The fetch implementation is a plain function rejecting with the cell's value, passed as the `fetchImpl` argument; no module is mocked; no network.",
  '3 cells: C1, C2 controls, R1 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1` (an Error whose message getter throws) (1 cell)", 1,
  'originate_own_create_client_ask_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails",
  reuse=REUSE_E, runner='jest', ref=JREF,
  testbase='ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts')

# ---- P8: demo-service services/authClient.ts authenticatePersona catch (vitest)
AU_O="    const message = err instanceof Error ? err.message : 'Unknown error';\n"
AU_N="    let message: string;\n    try {\n      message = err instanceof Error ? err.message : 'Unknown error';\n    } catch {\n      message = 'unreadable thrown value';\n    }\n"
site('p8','demo-service','src/services/authClient.ts',[(AU_O,AU_N)],1,
  '60-61 (the catch of `authenticatePersona`)',
  'the catch of `authenticatePersona` in `src/services/authClient.ts`',
  'the unguarded thrown-value read in the ONE catch of `authenticatePersona`',
  "The catch of `authenticatePersona` reads `err instanceof Error ? err.message : 'Unknown error'` into `message` with no guard. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch throw, so `authenticatePersona`, documented as 'does NOT throw on failure', REJECTS where an ordinary Error gives `{ success: false, error }`. The fix is the house guard: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The text of every value that can be read is unchanged.",
  "CALLERS: the demo persona switch route (`src/routes/persona.ts`, line 55) awaits `authenticatePersona` and answers from `success`/`error`; a rejection instead reaches its own catch. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at error level and the call resolves `{ success: false, error: <message> }`. Today (hostile value): the call rejects. After: the failed result with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the call resolves the failed result with the constant reason instead of rejecting.",
  "Premise: `authClient.ts` read whole",
  't94_p8.ts.txt',
  "The global `fetch` is a plain function rejecting with the cell's value (stubbed with `vi.stubGlobal`, removed after each cell); the service logger is a plain no-op object; no network.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'demo_service_auth_client_authenticate_persona_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'demo-service/src/__tests__/ks1868-persona-switch-unreadable-throw.test.ts',
  testbase='ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts')

# ---- P9: nft-certificate utils/mintError.ts classifyMintError (vitest)
MI_O="  const message = error instanceof Error ? error.message : String(error);\n"
MI_N="  let message: string;\n  try {\n    message = error instanceof Error ? error.message : String(error);\n  } catch {\n    message = 'unreadable thrown value';\n  }\n"
site('p9','nft-certificate','src/utils/mintError.ts',[(MI_O,MI_N)],1,
  '37 (the first statement of `classifyMintError`)',
  '`classifyMintError` in `src/utils/mintError.ts`',
  'the unguarded thrown-value read in `classifyMintError`; `mintFailureHttpStatus` and `mintFailureEnvelopeCode` read no thrown value',
  "`classifyMintError` reads `error instanceof Error ? error.message : String(error)` into `message` with no guard. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes `classifyMintError` THROW, from inside the mint route's own catch, where an ordinary Error is classified into `{ message, errorCode }`. The fix is the house guard: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'`, which then takes the same default as any unrecognised failure (`MINT_FAILED`). The classification of every value that can be read is unchanged.",
  "CALLERS: `MintingService` (`src/services/minting.service.ts`, line 386) calls `classifyMintError` in its catch, records the message and the failure on the NFT record and passes the `errorCode` on so the route can answer 404, 503 or 400 (`mintFailureHttpStatus`); a throw there escapes that catch and leaves the record unmarked. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the message and the error code of its class. Today (hostile value): the function throws. After: `{ message: 'unreadable thrown value', errorCode: 'MINT_FAILED' }`, so the mint is recorded failed and the route answers its default 400 with that message. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** a thrown value that cannot be read is classified `MINT_FAILED` (400, the default for an unrecognised failure) with the constant message instead of the route's catch throwing; a Claude seat should decide whether an unreadable value is better answered 500.",
  "Premise: `mintError.ts` read whole",
  't94_p9.ts.txt',
  "No stand-ins: `classifyMintError` is a pure function called directly with the cell's value.",
  '4 cells: C1, C2 controls (C1 holds two assertions), R1, R2 red',
  "'control ks1868 C1' (an ordinary Error, two markers) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'nft_certificate_mint_error_classify_mint_error_guard_message',
  "At the tip the function throws, so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts',
  testbase='ks1868-nft-certificate-classify-mint-error-unreadable-throw.test.ts')

# ---- P10: anchoring threadMintRequest.ts classifyThreadMintError (vitest)
TM_O="  const msg = typeof err?.message === 'string' ? err.message : String(error);\n  const errCode = typeof err?.code === 'string' ? err.code : '';\n"
TM_N=("  let msg: string;\n  let errCode: string;\n  try {\n    msg = typeof err?.message === 'string' ? err.message : String(error);\n    errCode = typeof err?.code === 'string' ? err.code : '';\n  } catch {\n    return null;\n  }\n")
site('p10','anchoring','src/threadMintRequest.ts',[(TM_O,TM_N)],1,
  '76-77 (the first two statements of `classifyThreadMintError`)',
  '`classifyThreadMintError` in `src/threadMintRequest.ts`',
  'the unguarded thrown-value reads (`err?.message`, `err?.code`, `String(error)`) at the top of `classifyThreadMintError`; the schema and `isEncodableDeploymentIdHex` read no thrown value',
  "`classifyThreadMintError` reads `err?.message` (falling back to `String(error)`) and `err?.code` with no guard. `?.` guards null and undefined only: a revoked Proxy throws on both reads, and an Error whose `message` getter throws throws on the first, so `classifyThreadMintError` THROWS from inside the route's catch, where an ordinary Error is classified (503, 400) or left unclassified (null, the route keeps its 500). The fix is the house guard: read both inside one `try` and, when the read throws, return `null` (an unreadable value is an unclassified failure). The classification of every value that can be read is unchanged.",
  "CALLERS: the thread-mint route (`POST /api/anchors/thread-mint`) calls `classifyThreadMintError` in its catch and answers its mapped 400/503, or a generic 500 for `null`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): its mapped status, or `null` (the 500) when unclassified. Today (hostile value): the function throws out of the route's catch. After: `null`, the route's 500. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** a thrown value that cannot be read is unclassified (null, the route's 500) instead of the route's catch throwing.",
  "Premise: `threadMintRequest.ts` lines 60-80 read",
  't94_p10.ts.txt',
  "No stand-ins: `classifyThreadMintError` is a pure function called directly with the cell's value.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error naming ECONNREFUSED) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'anchoring_thread_mint_request_classify_thread_mint_error_guard_message',
  "At the tip the function throws, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'anchoring/src/__tests__/ks1384-f0c-thread-mint.test.ts',
  testbase='ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts')

# ---- P11: anchoring cardano/provider.ts isChainReachableError + recordChainFailure (vitest)
CH_O1="  const status = typeof err?.status_code === 'number' ? err.status_code : null;\n"
CH_N1="  let status: number | null;\n  try {\n    status = typeof err?.status_code === 'number' ? err.status_code : null;\n  } catch {\n    return false;\n  }\n"
CH_O2="  chainHealth.lastFailureStatus = typeof err?.status_code === 'number' ? err.status_code : null;\n  chainHealth.lastFailureMessage = String(err?.message ?? 'unknown error').slice(0, 200);\n"
CH_N2=("  let status: number | null;\n  let message: string;\n  try {\n    status = typeof err?.status_code === 'number' ? err.status_code : null;\n  } catch {\n    status = null;\n  }\n"
       "  try {\n    message = String(err?.message ?? 'unknown error').slice(0, 200);\n  } catch {\n    message = 'unreadable thrown value';\n  }\n"
       "  chainHealth.lastFailureStatus = status;\n  chainHealth.lastFailureMessage = message;\n")
site('p11','anchoring','src/cardano/provider.ts',[(CH_O1,CH_N1),(CH_O2,CH_N2)],2,
  '129 (`isChainReachableError`) and 145-146 (`recordChainFailure`)',
  '`isChainReachableError` and `recordChainFailure` in `src/cardano/provider.ts`',
  'the unguarded thrown-value reads in `isChainReachableError` (`err?.status_code`) and `recordChainFailure` (`err?.status_code`, `err?.message`); the `fetch*` catches of the file (lines 321, 358, 393, 414, 432) are deliberately NOT touched: the instrumentation wrapper reaches these two functions first, so they are the root of those catches and a separate pass',
  "`isChainReachableError` reads `err?.status_code` and `recordChainFailure` reads `err?.status_code` and `String(err?.message ?? ...)`, all unguarded. `?.` guards null and undefined only: a revoked Proxy throws on every read, and an Error whose `message` getter throws throws on the message read. The instrumentation wrapper of the provider handle calls `recordChainOutcome(err)` for every failed Blockfrost call before the call's own catch runs, so the throw replaces the provider's error with a TypeError, and `recordChainFailure` has already set `reachability` to failing and the time but not the count or the message (a half-written record). The fix is the house guard: read each value inside its own `try`; an unreadable status is no status (not reachable: an unreadable error is no answer from the chain) and an unreadable message is the constant `'unreadable thrown value'`. The record of every value that can be read is unchanged.",
  "CALLERS: `recordChainOutcome` is called by the instrumentation wrapper of every provider call (`instrumentProvider`), and `getChainHealth` feeds the `/health` chain-reachability field and the alerting on it. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): classified by status; an unreachable chain is recorded failing with its status and the first 200 characters of its message, and the provider call then rejects with the original error. Today (hostile value): `recordChainOutcome` throws, the wrapper rejects with a TypeError, and the record is half written. After: recorded failing with no status and the constant message, and the original value propagates. Persisted state: in-memory health record only. **BEHAVIOUR CHANGE the raise PR must state:** a value that cannot be read counts as an unreachable-chain failure (it is no answer from the chain) instead of throwing.",
  "Premise: `provider.ts` lines 100-210 read",
  't94_p11.ts.txt',
  "The service logger is a plain no-op object; `@blockfrost/blockfrost-js` is the real package but is never called (only the exported health record functions are used); the record is reset before each cell with the module's own `__resetChainHealth`.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (a 402 error) and 'C2' (a 404 answer), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy; an Error with a readable 503 status whose message getter throws) (2 cells)", 2,
  'anchoring_provider_chain_health_record_guard_message',
  "At the tip `recordChainOutcome` throws, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts',
  testbase='ks1868-anchoring-provider-chain-health-record-unreadable-throw.test.ts')

# ---- P12: anchoring cardano/transaction.ts isInsufficientInputError (vitest)
IN_O="  return /UTxO Balance Insufficient|Insufficient input in transaction/i.test(String((err as { message?: unknown })?.message ?? err));\n"
IN_N="  let text: string;\n  try {\n    text = String((err as { message?: unknown })?.message ?? err);\n  } catch {\n    return false;\n  }\n  return /UTxO Balance Insufficient|Insufficient input in transaction/i.test(text);\n"
site('p12','anchoring','src/cardano/transaction.ts',[(IN_O,IN_N)],1,
  '59-61 (the body of `isInsufficientInputError`)',
  '`isInsufficientInputError` in `src/cardano/transaction.ts`',
  'the unguarded thrown-value read in `isInsufficientInputError`; the transaction builders of the file read no thrown value',
  "`isInsufficientInputError` reads `String((err as { message?: unknown })?.message ?? err)` with no guard. A thrown value whose read throws (a revoked Proxy throws on the message read and again on `String(err)`; an Error whose `message` getter throws) makes the predicate THROW from inside its caller's catch, where an ordinary error gets true or false. The fix is the house guard: read the text inside its own `try` and answer false when the read throws (an unreadable value is not the insufficient-input failure). The answer for every value that can be read is unchanged.",
  "CALLERS: `walletSpend.ts` (lines 157 and 165) calls it in two catches as `if (!isInsufficientInputError(err)) throw err;`, retrying the build with a different input set when the coin-selection failure is recognised and rethrowing any other failure. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): true for the two texts, false otherwise (the original error is rethrown by the caller). Today (hostile value): the predicate throws and replaces the original error. After: false, so the caller rethrows the original value. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** a thrown value that cannot be read is not the insufficient-input failure (false) instead of the predicate throwing.",
  "Premise: `transaction.ts` lines 50-62 read",
  't94_p12.ts.txt',
  "No stand-ins: `isInsufficientInputError` is a pure function called directly with the cell's value.",
  '5 cells: C1 to C3 controls, R1, R2 red',
  "'control ks1868 C1' (an Error with the coin-selection text), 'C2' (a thrown string with the forced-outpoint text) and 'C3' (an unrelated Error), already true at the tip (3 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'anchoring_transaction_is_insufficient_input_error_guard_message',
  "At the tip the predicate throws, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts',
  testbase='ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts')

# ---- P13: anchoring anchorSubmission.ts isAlreadySubmittedError (vitest)
AS_O="  const message = (err as { message?: unknown })?.message;\n"
AS_N="  let message: unknown;\n  try {\n    message = (err as { message?: unknown })?.message;\n  } catch {\n    return false;\n  }\n"
site('p13','anchoring','src/anchorSubmission.ts',[(AS_O,AS_N)],1,
  '182-184 (the first statement of `isAlreadySubmittedError`)',
  '`isAlreadySubmittedError` in `src/anchorSubmission.ts`',
  'the unguarded thrown-value read in `isAlreadySubmittedError`; the submitter around it is deliberately NOT touched',
  "`isAlreadySubmittedError` reads `(err as { message?: unknown })?.message` with no guard. `?.` guards null and undefined only: a revoked Proxy throws on the read, and an Error whose `message` getter throws throws on it, so the predicate THROWS from inside the submitter's catch, where an ordinary error gets true or false. The fix is the house guard: read the message inside its own `try` and answer false when the read throws (an unreadable value is not the node's already-included reply). The answer for every value that can be read is unchanged.",
  "CALLERS: the submitter's catch (`anchorSubmission.ts` line 1042, guard 3 of KS-705) asks it whether the node's reply means our transaction is already in the ledger (re-poll the known hash, never resubmit). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): true for the two node replies, false otherwise (the normal failure path). Today (hostile value): the predicate throws inside the catch and replaces the failure handling. After: false, so the normal failure path runs. Persisted state: none from the predicate. **BEHAVIOUR CHANGE the raise PR must state, and a Claude seat must judge (this sits in the paid-submission path):** a thrown value that cannot be read takes the normal failure path instead of the predicate throwing out of the catch.",
  "Premise: `anchorSubmission.ts` lines 165-190 and 1030-1052 read",
  't94_p13.ts.txt',
  "No stand-ins: `isAlreadySubmittedError` is a pure function called directly with the cell's value.",
  '5 cells: C1 to C3 controls, R1, R2 red',
  "'control ks1868 C1' (an Error with the node reply), 'C2' (an unrelated Error) and 'C3' (a thrown string), already true at the tip (3 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'anchoring_anchor_submission_is_already_submitted_error_guard_message',
  "At the tip the predicate throws, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts',
  testbase='ks1868-anchoring-is-already-submitted-error-unreadable-throw.test.ts')

# ---- P14: anchoring threadMintSpend.ts threadMintUnavailable (vitest)
TU_O="  if (err instanceof WalletLockTimeout) {\n"
TU_N="  let busy: boolean;\n  let noCoin: boolean;\n  let gone: boolean;\n  try {\n    busy = err instanceof WalletLockTimeout;\n    noCoin = err instanceof ThreadMintNoCoin;\n    gone = err instanceof ThreadMintCallerGone;\n  } catch {\n    return null;\n  }\n  if (busy) {\n"
TU_O2="  if (err instanceof ThreadMintNoCoin) {\n"
TU_N2="  if (noCoin) {\n"
TU_O3="  if (err instanceof ThreadMintCallerGone) {\n"
TU_N3="  if (gone) {\n"
site('p14','anchoring','src/threadMintSpend.ts',[(TU_O,TU_N),(TU_O2,TU_N2),(TU_O3,TU_N3)],1,
  '52-61 (the body of `threadMintUnavailable`)',
  '`threadMintUnavailable` in `src/threadMintSpend.ts`',
  'the three unguarded `instanceof` tests in `threadMintUnavailable`; `mintThroughView` and the other functions of the file are deliberately NOT touched',
  "`threadMintUnavailable` tests the thrown value with `err instanceof WalletLockTimeout`, `err instanceof ThreadMintNoCoin` and `err instanceof ThreadMintCallerGone`, unguarded. A revoked Proxy makes `instanceof` throw (its prototype cannot be read), so the function THROWS from inside the route's catch, where an ordinary error gets one of the three 503 answers or null. The fix is the house guard: evaluate the three tests once inside one `try`, return null when that throws (an unreadable value is none of the three refusals), and branch on the results. The answer for every value that can be tested is unchanged.",
  "CALLERS: the thread-mint route's catch (`src/index.ts` line 1190) calls it first and answers its 503 when it returns a mapping; for null it goes on to `classifyThreadMintError`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): its 503 mapping, or null. Today (hostile value): the function throws out of the route's catch. After: null, so the route goes on to its other classification and its default 500. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** a thrown value that cannot be tested is mapped to null instead of the route's catch throwing.",
  "Premise: `threadMintSpend.ts` lines 30-65 and `index.ts` lines 1185-1205 read",
  't94_p14.ts.txt',
  "No stand-ins: `threadMintUnavailable` is a pure function called directly with the cell's value (the error classes are the module's own).",
  '4 cells: C1 to C3 controls, R1 red',
  "'control ks1868 C1' (ThreadMintNoCoin), 'C2' (ThreadMintCallerGone) and 'C3' (an unrelated Error), already true at the tip (3 cells)",
  "`R1` (a revoked Proxy) (1 cell)", 1,
  'anchoring_thread_mint_spend_thread_mint_unavailable_guard_message',
  "At the tip the function throws, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'anchoring/src/__tests__/ks1868-confirmation-wait-catch-unreadable-throw.test.ts',
  testbase='ks1868-anchoring-thread-mint-unavailable-unreadable-throw.test.ts')

# ---- P15: auth repositories/dbErrors.ts isInfrastructureDbError (vitest)
DB_O="  const e = err as { code?: unknown; message?: unknown };\n"
DB_N="  let e: { code?: unknown; message?: unknown };\n  try {\n    e = { code: (err as { code?: unknown }).code, message: (err as { message?: unknown }).message };\n  } catch {\n    return false;\n  }\n"
site('p15','auth','src/repositories/dbErrors.ts',[(DB_O,DB_N)],1,
  '52-53 (the first statements of `isInfrastructureDbError`)',
  '`isInfrastructureDbError` in `src/repositories/dbErrors.ts`',
  'the unguarded `code` and `message` reads in `isInfrastructureDbError`; nothing else in the file reads a thrown value',
  "`isInfrastructureDbError` reads `e.code` and `e.message` of the thrown value with no guard. A revoked Proxy passes the `typeof err === 'object'` test and then throws on both reads, and an object whose `code` or `message` getter throws throws on its read, so the predicate THROWS from inside its caller's catch, where an ordinary error gets true or false. The fix is the house guard: read both once, into a plain object, inside one `try`, and answer false when the read throws (an unreadable value is not known to be an infrastructure failure). The answer for every value that can be read is unchanged.",
  "CALLERS: `userRepo.ts` (eight catches, lines 417 to 1176) and `routes/users.ts` call it in their catches to answer an availability error for a pool or connection failure and let a query-level error take its own path. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): true for an infrastructure failure, false otherwise. Today (hostile value): the predicate throws inside the catch and replaces the original error. After: false, so the caller handles the original value as a query-level error. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** a thrown value that cannot be read is not an infrastructure failure (false) instead of the predicate throwing.",
  "Premise: `dbErrors.ts` lines 40-60 read",
  't94_p15.ts.txt',
  "No stand-ins: `isInfrastructureDbError` is a pure function called directly with the cell's value.",
  '5 cells: C1 to C3 controls, R1, R2 red',
  "'control ks1868 C1' (a connection-terminated Error), 'C2' (a unique-violation error) and 'C3' (a thrown string), already true at the tip (3 cells)",
  "`R1`, `R2` (a revoked Proxy; an object whose code getter throws) (2 cells)", 2,
  'auth_db_errors_is_infrastructure_db_error_guard_message',
  "At the tip the predicate throws, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts',
  testbase='ks1868-auth-is-infrastructure-db-error-unreadable-throw.test.ts')

# ---- P16: m365-integration auth/token-manager.ts classifyMsalTokenError (vitest)
MS_O=("  const name = typeof err?.name === 'string' ? err.name : '';\n  const errorCode = typeof err?.errorCode === 'string' ? err.errorCode : '';\n"
      "  const nodeCode = typeof err?.code === 'string' ? err.code : '';\n  const msg = typeof err?.message === 'string' ? err.message : String(error);\n")
MS_N=("  let name: string;\n  let errorCode: string;\n  let nodeCode: string;\n  let msg: string;\n  try {\n    name = typeof err?.name === 'string' ? err.name : '';\n"
      "    errorCode = typeof err?.errorCode === 'string' ? err.errorCode : '';\n    nodeCode = typeof err?.code === 'string' ? err.code : '';\n"
      "    msg = typeof err?.message === 'string' ? err.message : String(error);\n  } catch {\n    return null;\n  }\n")
site('p16','m365-integration','src/auth/token-manager.ts',[(MS_O,MS_N)],1,
  '211-214 (the first statements of `classifyMsalTokenError`)',
  '`classifyMsalTokenError` in `src/auth/token-manager.ts`',
  'the unguarded thrown-value reads at the top of `classifyMsalTokenError`; the token calls and the cache helpers read no thrown value here',
  "`classifyMsalTokenError` reads `name`, `errorCode`, `code` and `message` of the thrown value (falling back to `String(error)`) with no guard. `?.` guards null and undefined only: a revoked Proxy throws on every read, and an Error whose `message` getter throws throws on the last, so the function THROWS from inside the route's catch, where an ordinary error is classified (503, 400, 401) or left unclassified (null, the route keeps its 500). The fix is the house guard: read the four values inside one `try` and, when the read throws, return `null` (an unreadable value is an unclassified failure). The classification of every value that can be read is unchanged.",
  "CALLERS: the Outlook token-exchange route's catch calls `classifyMsalTokenError` and answers its mapped status, or a generic 500 for `null`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): its mapped status, or `null` (the 500) when unclassified. Today (hostile value): the function throws out of the route's catch. After: `null`, the route's 500. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** a thrown value that cannot be read is unclassified (null, the route's 500) instead of the route's catch throwing.",
  "Premise: `token-manager.ts` lines 183-290 read",
  't94_p16.ts.txt',
  "No stand-ins: `classifyMsalTokenError` is a pure function called directly with the cell's value.",
  '5 cells: C1 to C3 controls, R1, R2 red',
  "'control ks1868 C1' (a network_error), 'C2' (an InteractionRequiredAuthError) and 'C3' (a thrown string), already true at the tip (3 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'm365_token_manager_classify_msal_token_error_guard_message',
  "At the tip the function throws, so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'m365-integration/src/__tests__/ks1868-m365-integration-db-pool-error-and-ready-hook-unreadable-throw.test.ts',
  testbase='ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts')

# ---- P17: originate services/provenance.ts resolveOnBehalfOf catch (jest)
PV_O=("  } catch (err) {\n    if (err instanceof OnBehalfOfError) throw err;\n    // Lookup infrastructure failure")
PV_N=("  } catch (err) {\n    let isOnBehalfOfError: boolean;\n    let reason: string | null | undefined;\n    try {\n      isOnBehalfOfError = err instanceof OnBehalfOfError;\n      const m = (err as Error).message;\n      reason = m === undefined || m === null ? m : String(m);\n    } catch {\n      isOnBehalfOfError = false;\n      reason = 'unreadable thrown value';\n    }\n    if (isOnBehalfOfError) throw err;\n    // Lookup infrastructure failure")
PV_O2="{ error: (err as Error).message });\n"
PV_N2="{ error: reason });\n"
site('p17','originate','src/services/provenance.ts',[(PV_O,PV_N),(PV_O2,PV_N2)],1,
  '156-161 (the catch of `resolveOnBehalfOf`)',
  'the catch of `resolveOnBehalfOf` in `src/services/provenance.ts`',
  'the unguarded `instanceof` test and message read in the ONE catch of `resolveOnBehalfOf`; `parseOnBehalfOf` and the rest of the file read no thrown value',
  "The catch of `resolveOnBehalfOf` tests the thrown value with `err instanceof OnBehalfOfError` and then passes `(err as Error).message` into the warn line, both unguarded. A revoked Proxy makes `instanceof` throw, and an Error whose `message` getter throws makes the read throw, so the catch throws and `resolveOnBehalfOf` REJECTS, failing the whole write, where an ordinary Error is logged and `null` (verbatim provenance) is returned; an `OnBehalfOfError` is rethrown. The fix is the house guard: evaluate the `instanceof` test and read the message once inside one `try`, fall back to not-an-OnBehalfOfError and the constant `'unreadable thrown value'` when the read throws, then branch. The behaviour for every value that can be read is unchanged.",
  "CALLERS: the write routes that accept an `onBehalfOf` field resolve it before they write; `null` means store the attribution verbatim and carry on. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the lookup failure is logged at warn level and the call resolves `null`. Today (hostile value): the call rejects and the write fails. After: logged with the constant reason, `null` as for an ordinary Error. Persisted state: the write proceeds with verbatim provenance as it does for an ordinary lookup failure. **BEHAVIOUR CHANGE the raise PR must state, and a Claude seat must judge (provenance/attribution path):** an unreadable thrown value now yields verbatim provenance instead of failing the write.",
  "Premise: `provenance.ts` lines 33-38 and 120-165 read",
  't94_p17.ts.txt',
  "The database client is a plain stand-in whose `$queryRaw` rejects with the cell's value; `@secuura/shared` is the suite's `makeSharedMock` (KS-1061) with identity encrypt and decrypt and a string lookup hash; the service logger is a plain recording object; no database, no network.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (an OnBehalfOfError, still rethrown), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'originate_provenance_resolve_on_behalf_of_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails",
  reuse=REUSE_Q, runner='jest', ref=JREF,
  testbase='ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts')

# ---- P18: billing routes/billing.ts sendClassifiedBillingError (vitest)
BL_O="  const msg = error instanceof Error ? error.message : String(error);\n  // KS-144: Stripe-config"
BL_N="  let msg: string;\n  try {\n    msg = error instanceof Error ? error.message : String(error);\n  } catch {\n    return false;\n  }\n  // KS-144: Stripe-config"
site('p18','billing','src/routes/billing.ts',[(BL_O,BL_N)],1,
  '58 (the first statement of `sendClassifiedBillingError`)',
  '`sendClassifiedBillingError` in `src/routes/billing.ts`',
  'the first unguarded thrown-value read in `sendClassifiedBillingError`; its later reads of the Stripe fields (`type`, `statusCode`, `code`) and the route catches that call it are deliberately NOT touched',
  "`sendClassifiedBillingError` starts with `const msg = error instanceof Error ? error.message : String(error)`, unguarded. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the classifier THROW from inside the route's catch, so the route's own 500 is never sent where an ordinary error is classified (503, 404, 400) or answered `false` for the caller's 500. The fix is the house guard: read the message inside its own `try` and return `false` when the read throws (an unreadable value is unclassified: nothing is written and the caller answers its 500). The classification of every value that can be read is unchanged.",
  "CALLERS: the billing write and read routes call it in their catches (`sendClassifiedBillingError(error, res, ...)`) and, when it returns false, answer their own 500. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a 503/404/400 written and `true`, or `false` for an unclassified error. Today (hostile value): the classifier throws out of the route's catch (the request gets no JSON answer). After: `false`, nothing written, so the route answers its own 500. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** a thrown value that cannot be read is unclassified (false) instead of the route's catch throwing.",
  "Premise: `billing.ts` lines 30-110 read",
  't94_p18.ts.txt',
  "A plain Response double as in the ks431 suite (status and json record the answer); no other stand-in: the real `routes/billing` module is imported, as in that suite.",
  '5 cells: C1 to C3 controls, R1, R2 red',
  "'control ks1868 C1' (an unconfigured-provider message), 'C2' (a \"No such\" message) and 'C3' (a provider 500), already true at the tip (3 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'billing_routes_send_classified_billing_error_guard_message',
  "At the tip the classifier throws, so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'billing/src/__tests__/ks1868-billing-webhook-replay-unreadable-throw.test.ts',
  testbase='ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts')

# ---- REBRIEF (13:2x): the builder REFUSES a hunk whose last changed line precedes a blank line (blank context) and trim() then leaves zero
# trailing context, which git apply anchors to EOF (strict=False). p9/p10/p15/p16 use the PROBE form (pure insertion before the existing statement);
# p4 drops its hunk 3 (the `message` helper, followed by a blank line) and the cells that need it.
NOTE_PROBE=(" FORM OF THIS BRIEF: the probe form. The diff is a pure insertion of one `try` block that reads the same values once before the existing statement and %s when the read throws; the existing statement is left byte-for-byte untouched (a hunk that ended on it would end before a blank line, which the builder refuses). A Claude seat may prefer the restructured single-read form when raising.")
def probe(k, old, probe_src, ret):
    X=T[k]
    X['edits']=[(old, probe_src+old)]
    X['nh']=1
    X['whatwrong']=X['whatwrong']+NOTE_PROBE%ret
probe('p9',"  const message = error instanceof Error ? error.message : String(error);\n",
      "  try {\n    void (error instanceof Error ? error.message : String(error));\n  } catch {\n    return { message: 'unreadable thrown value', errorCode: 'MINT_FAILED' };\n  }\n",
      "returns `{ message: 'unreadable thrown value', errorCode: 'MINT_FAILED' }`")
probe('p10',"  const msg = typeof err?.message === 'string' ? err.message : String(error);\n",
      "  try {\n    void (typeof err?.message === 'string' ? err.message : String(error));\n    void err?.code;\n  } catch {\n    return null;\n  }\n",
      "returns `null`")
probe('p15',"  if (typeof e.code === 'string') {\n",
      "  try {\n    void e.code;\n    void e.message;\n  } catch {\n    return false;\n  }\n",
      "returns `false`")
probe('p16',"  const name = typeof err?.name === 'string' ? err.name : '';\n",
      "  try {\n    void err?.name;\n    void err?.errorCode;\n    void err?.code;\n    void (typeof err?.message === 'string' ? err.message : String(error));\n  } catch {\n    return null;\n  }\n",
      "returns `null`")
# p4: scope reduced to isTimeoutError + the readInFlightAnchor catch
T['p4']['edits']=[(I_O,I_N),(C_O,C_N)]
T['p4']['nh']=2
T['p4']['lines']='53-54 and 193 (`isTimeoutError` and the catch of `readInFlightAnchor`)'
T['p4']['short']='`isTimeoutError` and the catch of `readInFlightAnchor` in `src/services/reanchorInFlight.ts`'
T['p4']['whatwrong']=T['p4']['whatwrong'].replace("`isTimeoutError` reads `.name` of the rejection value, the catch of `readInFlightAnchor` reads `err instanceof Error ? err.message : String(err)` and the `message` helper of `postReanchor` reads the same, all unguarded.","`isTimeoutError` reads `.name` of the rejection value and the catch of `readInFlightAnchor` reads `err instanceof Error ? err.message : String(err)`, both unguarded; the `message` helper of `postReanchor` reads the same and is deliberately NOT touched by this brief (a hunk on it would end before a blank line, which the builder refuses).")
T['p4']['tsrc']='t94_p4b.ts.txt'
T['p4']['ncells']='5 cells: C1, C2 controls, R1 to R3 red'
T['p4']['greens']="'control ks1868 C1' (isTimeoutError on a TimeoutError and an ordinary Error) and 'C2' (the read with an ordinary Error), already true at the tip (2 cells)"
T['p4']['redcells']="`R1` to `R3` (isTimeoutError on a revoked Proxy; the read with a revoked Proxy and with an Error whose message getter throws) (3 cells)"
T['p4']['redlines']="".join("- RED ks1868 R%d\n"%i for i in range(1,4))
