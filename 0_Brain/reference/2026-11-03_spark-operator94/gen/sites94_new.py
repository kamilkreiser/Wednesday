
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
