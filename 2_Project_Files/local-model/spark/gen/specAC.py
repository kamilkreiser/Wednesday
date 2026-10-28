# KS-1783 cell 2 of 3 (originate, POST /verify route). TEST-ONLY via gen/mk_testonly.py. Spark operator 5, 2026-10-28.
import importlib.util, os
_s = importlib.util.spec_from_file_location('sab', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'specAB.py')); _m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
REAL="const REAL_TX = '4f1e6a8d2c7b9e3f1a5b7c9d2e4f6a8b1c3d5e7f9a2b4c6d8e0f2a4b6c8d0e2f';\n"
DECL=("// KS-1783: the shape of a REAL tx hash (as ks1634-v2-chain-only-match-carries-simulated.test.ts:49), held apart from REAL_TX on purpose.\n"
      "const REAL_TX_SHAPE = /^[0-9a-f]{64}$/;\n")
OLD2="    const body = await callSite(chainReply({ simulated: true }));\n"
NEW2=("    const reply = chainReply({ simulated: true });\n"
      "    // KS-1783: assert the hash this cell sends is real (it was implicit, from chainReply's default). The route's own reply carries txHash null here, so the check is on the reply handed in.\n"
      "    expect(reply.txHash).toMatch(REAL_TX_SHAPE);\n"
      "    const body = await callSite(reply);\n")
T=dict(_m.T)
T.update(dict(dir='ks_1783_c2_verify_route',
 title='originate: the POST /verify L6 cell titled "simulated true with a real hash" never asserts the hash it sends is real: declare REAL_TX_SHAPE and add `expect(reply.txHash).toMatch(REAL_TX_SHAPE)` (RUNG 3, TEST-ONLY: two in-place test hunks; the product does not change)',
 intro=_m.T['intro'].replace('This brief is cell 1 of','This brief is cell 2 of').replace('(briefs ks_1783_c2_verify_route, ks_1783_c3_verify_file)','(briefs ks_1783_c1_v2, ks_1783_c3_verify_file)'),
 product='Blockchain/Dev/services/originate/src/routes/verification.ts',
 test='Blockchain/Dev/services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash-verify-route.test.ts',
 ref='Blockchain/Dev/services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts',
 tamper_line=1267, tamper_from="                    simulated: chain.simulated,", tamper_to="                    simulated: undefined,",
 statement_ok="line 1267 is one complete property inside the object literal handed to `presentBlockchainHonestly` (:1260-1268) in the chain-first branch of the `/verify` handler (route registered at :841); the tamper stops the reply's `simulated` being carried into the blob (the KS-1628 L6 bug), the object literal stays valid and the file still compiles",
 edit=[(REAL, DECL+REAL),(OLD2,NEW2)],
 red=['RED KS-1628 L6 verify: simulated true with a real hash is not on-chain','RED KS-1628 L6 verify: the shape anchoring really sends (simulated true, txHash null) is not on-chain'],
 runner='jest` (`npx jest src/__tests__/ks1634-a-simulated-anchor-verified-by-hash-verify-route.test.ts` from `Blockchain/Dev/services/originate',
 rung='3 (test-only mode: TWO hunks given byte-exact; the line-107 cell must keep failing by assertion under the product tamper)',
 nh_txt="2 hunks: one declaration beside `REAL_TX`, one inside the cell at lines 107-113",
 nh_word='TWO hunks (one declaration, one cell edit), in file order',
 nh_head='TWO EDITS in the TEST file (two hunks)',
 what_wrong="The cell `RED KS-1628 L6 verify: simulated true with a real hash is not on-chain` (test file :107-113) builds its anchoring reply as `callSite(chainReply({ simulated: true }))` at :108. The `chainReply` helper (:75-87) gives `txHash: REAL_TX` (:80); `REAL_TX` is a 64-hex string (:45). No assertion in the cell reads that hash: the assertions at :109-:112 are about the ROUTE's reply (`body.blockchain.simulated` true, `body.blockchain.anchored` false, `body.blockchain.txHash` toBeNull at :111, `body.checks.isAnchored` false). The presenter marks a reply simulated from a placeholder-shaped hash alone, so with a placeholder-shaped default the cell could pass without the `simulated` fix: the cell says \"real hash\" in its title and nothing holds it. `REAL_TX_SHAPE` does not exist in this file (a literal search returned no line). The sibling file `ks1634-v2-chain-only-match-carries-simulated.test.ts` declares `const REAL_TX_SHAPE = /^[0-9a-f]{64}$/;` at :49 and uses `expect(reply.txHash).toMatch(REAL_TX_SHAPE);` at :159 and :173, after `const reply = chainReply({ ... });` and before the call. This task declares the shape in this file (Edit 1, directly before `REAL_TX`, line 45) and applies the same shape to :108 (Edit 2). IMPORTANT (measured at :111): the route's own reply carries `txHash` null for a simulated reply, so the hash is read from the `reply` object the cell hands in.",
 where="- test file `:45` - (correct, STAYS) `const REAL_TX = '4f1e...0e2f';` - Edit 1 is two NEW lines directly BEFORE it (a comment line and the `const REAL_TX_SHAPE` line); the line itself is unchanged.\n- test file `:108` - (CURRENT, one statement) `    const body = await callSite(chainReply({ simulated: true }));` - Edit 2 turns it into four lines (the object is named, asserted, then passed).\n- `routes/verification.ts:1267` - (correct, STAYS) `                    simulated: chain.simulated,` - the product line the checker's tamper corrupts in a clone.",
 cells="- `RED KS-1628 L6 verify: simulated true with a real hash is not on-chain` is the cell this task edits; with the other L6 RED cell (`the shape anchoring really sends`) it is expected to fail by assertion under the product tamper (the control run measures the exact set) and both are green at the untouched tip. The new `expect(reply.txHash).toMatch(REAL_TX_SHAPE)` passes at the tip and under the tamper; the checker's A4 therefore proves the cell is still red, NOT that the new assertion catches a placeholder default (the operator proves that separately).\n- Every other cell of the file stays exactly as it is and stays green.",
 unmeasured="- Whether the new assertion goes red when `chainReply`'s default is a placeholder: the operator measures that by hand in a scratch clone, outside the checker.\n- That the tamper line 1267 is the site the `/verify` route test reaches (the other identical-shaped site, :724, belongs to `/verify-file`): the checker's A4 measures it; if the declared red cell does not fail under the tamper, A4 says so.\n- Open PRs touching this test file: not read by the drafter.\n- The suite was not run by the drafter; the checker's control run measures it.",
 scope="**Closes 1 of the 3 cells KS-1783 lists** (the /verify file). Refs KS-1783, does NOT close it. The ticket proposes no fix (\"No fix is proposed\").",
))
