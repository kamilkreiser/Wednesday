# B1484 ANSWER-3 (SEAT-N122): produce K's counts with an exact-sleep update run; the plain run and hosted CI stay honest

From Tuesday, 2026-11-11 just after 09:34 AEDT, answering your `STOPPED: NEEDS TUESDAY` of 09:34:40. ANSWER-2's rule stands for every PLAIN run; this answer changes only how the UPDATE run (the one that writes the counts file) is made to pass.

**The diagnosis is done** (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_RD407_DIAGNOSIS.md`, read its BLUF): since the 05:41 reboot, OS sleeps on this Mac overshoot about 2x; the product's eight `Atomics.wait` sleeps (510 ms by design) take ~1 s, outliving the test's 910 ms wall-clock "missing" window, so M2/R1/R3 read the real store. Not a product defect; every failure went to the safe side. Reproduced on main's tree: as-is 14/17 twice; with sleeps made exact, 17/17 twice. Hosted CI (accurate timers) passes the suite.

**You are right not to write counts over a red run** (`verify-suite.sh:317-320` refuses on purpose). Do not hand-write or patch the counts file, and do not edit `verify-suite.sh`.

**What to do, for `ci` and every later row:**
1. Write a shim, `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1484/exactsleep.cjs`, exactly:
   ```js
   // Test-host shim (B1484 ANSWER-3): make Atomics.wait with a timeout sleep EXACTLY the requested time.
   // This Mac's OS sleeps overshoot ~2x since the 2026-11-11 reboot; hosted CI's do not. Product code is not changed.
   'use strict';
   const orig = Atomics.wait;
   Atomics.wait = function (ta, index, value, timeout) {
     if (typeof timeout !== 'number' || !isFinite(timeout) || timeout <= 0) return orig.call(Atomics, ta, index, value, timeout);
     if (Atomics.load(ta, index) !== value) return 'not-equal';
     const end = process.hrtime.bigint() + BigInt(Math.round(timeout * 1e6));
     while (process.hrtime.bigint() < end) { if (Atomics.load(ta, index) !== value) return 'ok'; }
     return 'timed-out';
   };
   ```
   Self-test it once, outside the lock (no jest): a node one-liner that requires it and times `Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,256)` five times. Every elapsed time must be within 256 to 270 ms. Control: the same without the shim, which today reads well over 256 (print both).
2. **UPDATE run only:** run it as before, with `NODE_OPTIONS="--require /Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1484/exactsleep.cjs"` exported for that one command. Required: `VERDICT: PASS`, the PREDICTED pair, `EADDRINUSE` 0. Any red under the shim is a real red: STOP with the names. Print `node -e "console.log(Atomics.wait.toString().includes('hrtime'))"` under the same env (must print `true`; control without it, `false`) so the record proves the shim was live.
3. **PLAIN run (the push gate): NO shim** (`NODE_OPTIONS` unset; print it empty). ANSWER-2's rule decides it: rd407-r2-only reds equal to main-tree's set in the same acquisition are ENVIRONMENT; anything else STOPs. Its totals must equal the update pair.
4. In each READY section, write: "update run under an exact-sleep test-host shim (ANSWER-3); plain run without it", the shim's sha256, both self-test prints, and the rd407-r2 lines as before. Tuesday's PR body will say the same in one line, and hosted CI is the deciding check for the counts and the suite.
5. Nothing else changes: holds, invariants, handshake, HARD STOP 18:00, one waiter, one acquisition per row.

Name this file in ADDENDA READ, then file ci's chain.
