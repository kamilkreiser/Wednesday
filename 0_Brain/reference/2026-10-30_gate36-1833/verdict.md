## QA GATE - TIER 1, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 36's returned text, 17:1x AEDT. Probes in `probes/` beside this file — on disk, gitignored.)

**Subject:** PR #1833 (Secuura/Distributed_Secuura), KS-1844, author Seat U 7th — GET /api/certifications/:id answers 500 when the thrown value cannot be read.
**Head:** `9361d5979e23f3c0e16323e8c9b6eca8e1dbbeb9`, ls-remote equal at 16:58:39 and 17:13:49 AEDT. Base 530f091120d5; develop a8c554659cb3 at both reads; merge-tree conflicts ONLY in the two Projects Documents html.
**Gate:** 36, tier 1. Clone `repo/` (toplevel asserted, push URL no_push_qa_gate, ends clean). Nothing pushed/commented/merged; nothing under !CODING written.

### Verdict
Correct for every shape it names and a strict improvement: of a 16-shape hunt, 12 hang at base (0 responses); at head 13/16 get the constant 500 under the REAL winston logger (16/16 with the logger mocked). Every code/meta/meta.code/instanceof (getPrototypeOf trap)/message/toString/Symbol.toPrimitive read is inside a try. ONE hole: the log reason is not coerced to a string (`reason = error instanceof Error ? error.message : String(error)`), so a hostile `message` value reaches logger.error and the real logger's redactLogValue (logger.ts:49) / JSON format throws at certifications.ts:1091 outside any try: 3 shapes still get NO ANSWER. The author's suite mocks the logger, so it cannot see this. 404 mapping, single response and body constancy hold.

### Findings
- **F1 Minor — FIX BEFORE MERGE.** H13 `Object.assign(new Error('x'),{message: revokedProxy})`, H14 message getter returning `{toJSON(){throw}}`, H15 message getter returning a proxy whose getPrototypeOf throws: NO ANSWER, writes=0, under the real logger (`bash probes/run.sh head-real HEAD g36-hunt 1`; 3/23 red, twice). Fix: `reason = String(error instanceof Error ? error.message : error);` inside the existing try (probe `mut/FX_reason_coerced.ts`: real-logger hunt 23/23, author file 7/7). Add one cell with the REAL logger (or assert typeof the logged error is string) using an Error whose message is a revoked Proxy. Likelihood low (synthetic class, same as D1-D3). The docs' claim "carries the fixed fallback text, not the thrown value" is false for these shapes until fixed.
- **F2 Minor — FOLLOW-UP (cheap).** Author cells assert only status + error.code: M7 (adds `detail: reason` to the 500 body = leak) survives the author file; M3 (fallback reason -> '') survives both. Fix: toEqual the whole constant envelope; assert mockLog.error called with {error:'unreadable thrown value'} for D1/D3.
- **F3 Info, PRE-EXISTING.** `{code:'P2010', meta:{code:'22P02'}}` with no 22P02 in the message -> 500 at base and head (`??` takes 'P2010'; same for own code ''). The REAL Prisma P2010 shape (22P02 in the message, S4) answers 404.
- **F4 Info.** eslint no-useless-assignment at 1075:11 at head, 0 at base. `let invalidId: boolean;` is SAFE: tsc rc 0, eslint 0, author 7/7, hunt 23/23; negative control (catch assignment removed) gives TS2454, so definite assignment is really checked.
- **F5 Info, CLASS.** `instanceof Error ? error.message : String(error)` appears 88 times across services/ (control 307 `instanceof Error`), 9 in certifications.ts, 15 in documents.ts; each unguarded against a hostile thrown value. A single `safeReason(e)` helper is the structural fix.

### Answers
1. Every read of the thrown value inside a try: yes (H01-H11, H16); the PRODUCT of the message read escapes (F1). No template interpolation in the log line. 2. Exactly one response on every non-hanging cell; follow-up request 404 each time; M6 double send killed. 3. S1-S7 shape table byte-identical base vs head. 4. Every 500 body = constant envelope, no SECRET marker (H11, H16). 5. Author file base 3F/4P, head 7/7. Mutants: M1, M2, M4, M5, M6 killed; M3 survives both; M7 survives the author file. Originate unit at head 1861/1861. 6. Author findings (a) confirmed + safe (F4); (b) confirmed, unchanged (F3).

### NOT TESTED
NODE_ENV=production logger path (json() + keepFileFields transports); whether any real path throws such values; the real app's unhandledRejection handler; the 87 sibling sites; originate integration (DB); platform suites; running stack; Node 24; the author's exact mutants (reconstructed).

### Instrument faults
First hunt run failed H13/H14 on the gate's own JSON.stringify console line (fixed to typeof before any result read). eslint with --config from a foreign cwd gave a false zero ("File ignored"); re-run via probes/eslint_at.js with chdir, positive control fired. jest intercepts process handlers, so the unhandledRejection capture recorded nothing; the hang is evidenced by NO ANSWER + writes=0 + stack. Hooks refused a $G word-split call and a cd (re-issued literal).
