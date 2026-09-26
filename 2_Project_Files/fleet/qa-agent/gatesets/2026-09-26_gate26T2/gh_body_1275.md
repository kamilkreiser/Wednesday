#1275 KS-1179: N1 reachability overclaim, N2 contract pin, and the one type error that fixes cleanly
head d852e56b912f8a14b8f2cf01639dc37f9c9ff6a2

## BLUF

KS-1179's residue: **N1** (a comment claiming a reachability it does not have), **N2** (a cell pinning a throw the module's contract disclaims), and **TYPECHECK-DEBT**, of which exactly one error fixes cleanly. **The emitted JavaScript is byte-identical to base** — no runtime behaviour and no emitted string moved, which is the constraint this change was held to.

`Refs KS-1179`

> **Base:** this branch is cut from `4db87c3e4b98`. develop is now `d7cdecf1d2ee`, which this worktree does not contain — so the STOP counts below describe `4db87c3e4b98 + this change`, not the combined tree.

## N1 — the comment claimed a live path that does not exist

It said the DNS-timer cleanup was *"a live path, not a defensive one"* because an `isIP` throw rejects the resolve race.

**`net.isIP` does not throw.** Measured on this node — `'x'`, `''`, `null`, `undefined`, `123` — each returns `0`, none throws. The rejecting exit is reachable **only** by mocking `net`. So the `finally` is **defensive**. It stays, because it costs nothing and is correct for any future arm of that race that *can* reject; what it no longer does is overstate how reachable it is. The next reader sizes a bug here on that claim.

## N2 — the cell pinned a throw the contract disclaims

The module's docblock: *"Returns the guard's error rather than throwing it"*, and KS-931 made that literally true even for a synchronous throw out of `http.request`. The cell asserted `.rejects.toThrow(SEAM)` — enshrining, as behaviour, a throw that exists **only because `net` is mocked**.

The rejection is now the **vehicle, not the claim**: it is caught and asserted only to *be the seam*, so the cell still reaches the exit F-6 is about without pinning a path no real input takes. A new **CONTRACT** cell pins what actually holds — on a real input the guard returns `{ ok: false, reason: 'blocked' }` with its error in the returned value, and does not throw.

**Red-proof for the contract cell:** tampering `return { ok: false, … }` to `throw` reds it, together with CALIBRATION and the settling CONTROL, which take the same return. **The F-6 cell stays green there**, because it leaves through the rejecting seam — exactly the separation the two cells are meant to have. Product restored byte-identical.

## TYPECHECK-DEBT — one fixed, one recorded

`tsc -p .` returns **rc 0** and always did: `tsconfig.json` excludes `src/__tests__`, so the package's own check never sees a test file. **That exclusion is the debt.** Under a test-inclusive program (method and controls in the ticket) there are **10** errors across 6 files.

**TS7006 (`(res)` implicitly any) — fixed** with an annotation; annotations erase, so the emit is untouched.

**TS2349 (`mod.request` not callable) — RECORDED, NOT FIXED.** Four shapes measured; each **relocated** the error:

| attempt | result |
|---|---|
| no change | **TS2349** not callable |
| cast the callee | **TS2769** no overload matches (`agent` is `https.Agent \| http.Agent`) |
| callee cast + cast at the call site | errors 10 → 8, **but the emit changes** (`agent,` → `agent: agent,`) |
| callee cast + assertion on the declaration | emit identical, **TS2352** types do not overlap |

The only shape left is `as unknown as https.Agent`. **Refused:** in an SSRF guard, a type the compiler stops checking is the risk to avoid, not the tidiness to buy. Carried into the follow-up ticket as a measured item.

## The emit proof, and why it is the one that matters here

`ast_equiv` (transpile with `removeComments`, compare output) — **pristine vs head: EQUIVALENT, 12,137 vs 12,137 bytes, 0 diagnostics.**

**Control on the same instrument:** change one character of the deadline error `(connect, transfer and drain)` → `(…drained)` and it reads **DIFFERENT**, naming the line. So the instrument can see precisely the string that had to stay fixed, and it says nothing moved.

**Why that string is load-bearing:** `services/originate/src/__tests__/ks914-deliver-webhook-blocked-vs-failed.test.ts:76` and `:86` assert it as an exact string, and `services/originate/` is **not in this lane**. Changing it would have reddened another seat's suite mid-round. **ks914's own cells: 16/16 green at this head.**

**F-5 needed no change** — its docblock correction shipped in an earlier round, and the only remaining element was that runtime string.

## Test Evidence

**Touched**
- `packages/shared/src/security/ssrf-guard.ts` — the N1 comment, and the TS7006 annotation.
- `packages/shared/src/__tests__/ks1179-dns-timer-cleared.test.ts` — N2.

**Ran**
- `packages/shared`: **941/941 bare → 942/942 patched**, 48 files, **+1 = the contract cell**. `npx vitest run --no-file-parallelism` in `s-l7-ks1179`, at base `4db87c3e4b98`, load **7.71** bare / **12.77** patched.
- `npx tsc -p . --noEmit` rc 0; `npm run build` rc 0.
- `ks914-shipped-path` + `ks914-pinned-address`: **16/16**.
- The contract-cell red-proof, and the emit comparison with its control.
- **Push gate:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (legs 3, 4, 8 — local stack not up; not quoted as a pass). STOP count with `packages/shared` built: `pre_push_hook_base` **28/0** · `fixture_guard` **6/0** · `run_shell_suites` **49/0** · shell suites **60 of 60** — on the base named above.

**NOT run**
- Legs 3, 4, 8.
- **The defensive `finally` is not exercised by any real input** — by construction, since nothing real rejects that race. The F-6 cell reaches it through a mock and now says so.
- **TS2349 and the other 8 type errors are not fixed** and are carried to the follow-up ticket.
- **No behaviour change of any kind.** The emit proof is the evidence, not a claim.
- ks914's cells were run to show the string survived; **this PR does not touch `services/originate/`**.

**Migrations + config**
- **None.**

