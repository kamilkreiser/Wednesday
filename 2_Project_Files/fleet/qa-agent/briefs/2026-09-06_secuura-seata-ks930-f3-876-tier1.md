# QA Agent Invocation Brief — Secuura/Blockchain SEAT A · KS-930 F-3 · PR #876 · TIER 1

**TIER 1.** This is `check-shared-relink.sh`, **preflight leg 13, blocking every push**, and the fix
closes two FALSE CLEANS on the **#851 outage shape** — a whole-tree write clobbering
`@secuura/shared`, reported clean. A guard that reports clean on the shape of a real past outage gets
the full weight.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. Findings-only.

## 1. Target
- Repo `/Volumes/DevMASTER/!CODING/Secuura/Blockchain` (Platform K).
- **PR #876, head `af954c69177116344700ac1433f9573f75323f4a`, base develop `066cff67554a5bd5398fcc9fb4b9ade422fbbd5b`.**
  Both read by Wednesday with `ls-remote` in the same action as writing this.
- **Work in YOUR OWN clone/worktree pinned to the literal SHA.** In a clone taken from the local
  project repo, `origin/develop` resolves to the SOURCE's stale local develop — pin `refs/qa/base` to
  the literal `066cff675` and use only that. (That cost a tester time earlier tonight.)

## 2. Spec / DoD
The two shapes below must be BLOCKED, `npm init -y` must stay CLEAN, the real 25-file tree must stay
`25 of 25 clean` in both default and STRICT modes, and each fix must red only its own cells.

## 3. Scope — the builder named THREE places it could be wrong. Press those first, in this order.
Quoted from its READY, because these are its words and its self-suspicions, not Wednesday's:

**(1) THE FIXTURE SHAPE IS THE FINDING — read this before you build any fixture, or you will produce
a false refutation.**
> The claim that the two shapes were FALSE CLEANS and not merely unreadable rests on the fixtures
> carrying a **SECOND, parseable node_modules write** — without one the guard exits 1 via the
> "unexpected shape" FALLBACK and the hole is hidden. **If the gate reproduces with a single-write
> fixture it will see rc 1 and may conclude I overstated it.** The fixture shape is the finding, and
> it is the shape all 25 real files have.

So: build BOTH. A single-write fixture (expect rc 1 through the fallback) **and** a two-write fixture
(the real-world shape). If your single-write fixture reds and you stop there, you will report a
refutation that is an artefact of your fixture. The claimed false cleans, each being the canonical
clobber file with ONLY the last write's spelling changed:
```
COPY --from=builder /app/node_modules ./node_modules          rc 1  blocked   (the control)
COPY ["--from=builder", "/app/node_modules", "./..."]         rc 0  1 of 1 clean   <- false clean
COPY --from=builder ["/app/node_modules", "./node_modules"]   rc 0  1 of 1 clean   <- false clean
RUN npm i --omit=dev                                          rc 0  1 of 1 clean   <- false clean
```

**(2) DO THE CELLS PIN THE CLAUSE, OR ONLY THE EXIT CODE?**
> The whole argument for the fix is that exit-code-only cells would have PASSED against the unfixed
> guard. Worth tampering the cells' expected-substring away and confirming they then pass against the
> pre-fix guard — **if they do not, my reasoning about why this hid is wrong even though the fix is
> right.**
Run exactly that. It is the campaign's own thesis pointed at this PR, and a negative result here is a
real finding even though the fix stands.

**(3) THE WIDENING IT SUSPECTS OF ITSELF.**
> I widened an alternation to `(ci|install|i)` and that is the kind of widening that goes too far
> quietly. The cell asserts `npm init -y` stays CLEAN. **If `([ \t]|$)` is not actually what saves it,
> I want to know.**
Establish what actually prevents `npm init` matching. Then hunt neighbours the widening may now catch
that it should not (`npm i` inside a longer word, `npm install` in a comment, a heredoc body).

**(4) Re-derive the red-proofs and check they ISOLATE.** Claimed: removing the COPY normalisation →
28 passed / 2 failed (exactly the two JSON cells); reverting `(ci|install|i)` → 29 passed / 1 failed
(exactly the npm-i cell). **A red-proof that reds the new cell alongside its neighbours proves nothing
about what the cell adds** — check each tamper reds ONLY its own fix's cells.

**(5) The real tree.** 25 of 25 clean in BOTH modes at the head, and suite 26 → 30.

**(6) Anything the fix now BLOCKS that it should not.** The builder fixed false cleans; the mirror
risk is a new false block. It has separately measured that heredoc and non-final-stage shapes are
already false blocks and deliberately left them — those are known, not findings. New ones are.

## 4. Credentials (POINTER ONLY)
`4_Credentials/.env`. You should not need any.

## 5. State-mutation & cleanup
- **Two builder seats are LIVE** — seat A in `worktrees/seat-a`, seat B in `worktrees/seat-b`. Touch
  neither. Work only in your own copy.
- No `rm`; quarantine by rename. **Restore any tamper by INVERSE EDIT verified with sha256, never by
  checkout** — the guard's pre-tamper hash per the builder is
  `da304d7e7c676eac2e0da2644666f60af193d7072c6ad5169cd1895490eae071`. **And after the hash matches,
  RE-RUN the suite**: a hash proves the bytes, only a run proves the file still works.
- Report the LISTEN set and Docker container count before and after.

## 6. Output boundary
One mail to Wednesday, subject `[QA -> Wednesday] Secuura SEAT A KS-930 F-3 (#876, tier 1)`.
Findings-only; severity yours, priority Wednesday's. NOT-TESTED at equal prominence.

## 6a. Evidence class on every finding that recommends an action
Oracle, measurement, control, and what you did NOT establish.

## 7. Known-fragile — three ways a search lies, all seen in this fleet TONIGHT
1. **The command never ran** — an unquoted `--include=*.ts` tripping zsh `nomatch` gives a zero that
   is not a measurement. A positive control catches this.
2. **The term could not match** the way the code is written — a real zero read as confirmation.
   Checking the query against the data's shape catches this.
3. **The output was truncated** — `head -8` over eleven `vi.mock` calls hid the only one that
   mattered. **Neither defence catches this: COUNT FIRST (`grep -c`), or do not truncate a list you
   are about to call complete.**
Also: **a RED that proves nothing is as blind as a green that proves nothing, and more dangerous
because red is the colour you were hoping for** — a tamper that reds by timeout, crash, syntax error
or setup failure is the run failing to happen, not a red-proof. State WHICH assertion tripped.
And: **a measurement travels; an explanation of it does not.** Every mechanism in §3 is the builder's,
quoted, and is the thing under test — including Wednesday's framing of it.
Env: darwin, bash 3.2.57, awk (BWK), `core.fileMode` false, `/bin/dash` present, `git grep -a` for
files with NUL bytes. A fresh worktree has no `node_modules`; `npm ci` from `Blockchain/Dev` is the
documented fix for preflight leg 1, never `--no-verify`.

## 8. Logistics
Wednesday reads your verdict whole and rules. Box ~35 minutes. If short, do (1), (2) and (4) first and
say plainly what you did not reach.

---

PROVENANCE:
- PR #876 head af954c69177116344700ac1433f9573f75323f4a and base develop 066cff67554a5bd5398fcc9fb4b9ade422fbbd5b | `git ls-remote origin` from Wednesday's seat (READ verb only) | read 2026-09-06
- the three self-named risk areas quoted verbatim, the four rc values, both red-proof figures, the sha256 restore hash and the 26 → 30 suite count | seat A's READY mail `[Secuura/Blockchain -> Wednesday] READY FOR QA: KS-930 F-3 PR #876 @ af954c691` 2026-09-06T13:11Z and its DECISION mail 13:09Z, both read whole by Wednesday | read 2026-09-06
- the fallback mechanism that hides the hole on a single-write file | seat A's DECISION mail 13:09Z | read 2026-09-06
- the three-ways-a-search-lies taxonomy | Secuura seat B's mail 2026-09-06T13:01Z, adopted into fleet/specs/brief-standing-lines.md | read 2026-09-06
- the stale `origin/develop` trap in a derived clone | the launcher gate's verdict 2026-09-06T12:18:53Z | read 2026-09-06
- NOT READ by me: `check-shared-relink.sh`, its suite, the #876 diff, and KS-930's text. I have opened none of them and run nothing; every mechanism in §3 is the builder's and is under test | not read | read 2026-09-06
