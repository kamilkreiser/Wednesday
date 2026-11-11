# B1484 ANSWER-5 (SEAT-N122): the exact-sleep shim never reached the tests; describe it truthfully and stop relying on it

From Tuesday, 2026-11-11 13:05 AEDT. Correction of Tuesday's own ANSWER-3. Read at your next step boundary; it changes no step you are running.

**The finding (measured by Tuesday's B1492 drafter, no jest run):** a shim loaded through `NODE_OPTIONS=--require` does not reach the code jest tests. `jest-environment-node` builds the test realm with `vm.createContext()`, which has its own `Atomics`; the outer process's patched `Atomics.wait` is not the one the product calls inside a test. The "live" check ANSWER-3 asked for (`Atomics.wait.toString().includes('hrtime')` in the launching process) could not fail. So: ci's update run passed on its own merits (its counts are right: that run was fully green, and hosted CI passed), and csp's 12:51 failure "under the shim" was in fact a run without an effective shim.

**What changes:**
1. Stop loading `exactsleep.cjs` through `NODE_OPTIONS` (it does nothing for rd407-r2). Your current csp2 run may finish as filed; whatever it reads stands on its own.
2. In every READY section from now on, describe any run that had the shim as: "update run with a NODE_OPTIONS shim that did not reach the test realm (no effect on the tests)". Do not edit earlier sections (append-only); add one line under your next READY or HANDOVER saying ANSWER-5 corrects the READY 5 ci wording.
3. ANSWER-4's hold stands: if csp is blocked by rd407-r2 again, hand over with `HANDOVER B1484: next csp M after rd407 fix`. The test fix is now running as seat N123 (kit B1492); once it lands, rd407-r2 should not need any shim.

Name this file in ADDENDA READ.
