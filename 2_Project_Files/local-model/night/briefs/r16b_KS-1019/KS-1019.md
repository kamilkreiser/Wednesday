# KS-1019 R16B-LEAVEUNTYPED - comment_patch: record Kam's "leave untyped" ruling as ONE comment line at the head of the schema that publishes the document match's `blockchain` block as `z.unknown()` (originate `originate.openapi.ts`, the block at `:615` at the tip - the ticket's `:601` at its own tip e559f7bb)

Task type: **comment_patch** (`tasks/comment_patch/task.md`). ONE file, comment lines only: `Blockchain/Dev/services/originate/src/originate.openapi.ts`. Tip: `3bad652d17cf111c1e2e1bed1ae7686894637487`. Written 2026-09-22 18:59:14 AEST by Wednesday's feed16 drafter under Kam's ruling (2026-09-22 18:11, card `secuura-ks1019-blockchain-block-untyped`, option a: "Leave untyped; record the reason at :601 in one comment line"). Every context line below is read from the tip file, never typed.

## THE MODE - read this twice

**comment_patch. This is a DECISION RECORD with NO BEHAVIOUR CHANGE.** There is no test cell, no tamper, and nothing to run: the proof is that the PROGRAM is byte-for-byte the same program while ONE comment line was added.

**STOP RULE - no executable line may change.** The fence below has exactly ONE `+` line and it is a `//` comment; there is no `-` line. You do not touch a statement, an identifier, an import, a string, a template literal, a type, or a JSX text. You do not add, remove or reword a directive comment (`@ts-...`, `eslint-...`, `/// <reference`, `istanbul ignore`, `c8 ignore`, `*-environment`, `prettier-ignore`) - there are none in the touched lines and there must be none after. The checker measures the TypeScript token stream (every syntax leaf: kind + text, literals included) before and after and fails on the FIRST differing token. A single changed code token fails the whole task. **Do NOT type the block** - a discriminated union on `status` is option b, a Peter-reviewed product PR, and it is exactly what Kam ruled AGAINST for this task.

**Reproduce the fence. Do not re-wrap, re-word or re-indent it.** The `+` line is copied byte for byte (it starts at column 0, like the `const` line under it). Every context line is the file's real neighbour, copied byte for byte. A blank context line is a single space.

## The ticket's own words (Linear KS-1019, read 2026-09-22 18:59:14 AEST read-only; Backlog, P3, unassigned, 0 PRs)

Title (verbatim): "[Question] The document's whole `blockchain` block is published as z.unknown() - undeclared to integrators, and invisible to every drift guard by construction".

- BLUF (verbatim): "**Should it be typed?** I have not established that the current shape is unintended, so this asks rather than asserts. The answer may legitimately be "deliberate, leave it" - but it should be a decision on the record rather than a default nobody chose."
- The site (verbatim): "`Blockchain/Dev/services/originate/src/originate.openapi.ts:601` ... `blockchain: z.unknown().nullable().openapi({ ... })` ... Measured on `develop` `e559f7bb`."
- Why it matters (verbatim): "**A field typed** `z.unknown()` **cannot drift - because it never said anything.** It is the one shape a drift check cannot fail on, which means the guard's green tells you nothing here."
- Intent, as the ticket left it (verbatim): "It may be deliberate - the block's shape varies by anchoring mode (real / simulated / failed) and a loose type is one honest way to express that."
- **Kam's ruling (2026-09-22 18:11, the decision the ticket asked for):** option a - leave it untyped; record the reason in one comment line. Option b (a discriminated union on `status`) was NOT chosen.

## Premises (measured)

- **P1 the tip.** develop is `3bad652d17cf111c1e2e1bed1ae7686894637487` - instrument: `git ls-remote git@github.com:Secuura/Distributed_Secuura.git refs/heads/develop` from the scratchpad clone (`runs/2026-09-22_feed16-drafter-precheck/clone.log`), the object present as a commit (`git cat-file -t`).
- **P2 the site moved from `:601` to `:615` between the ticket's tip and this one.** At `e559f7bb` line 601 is `      blockchain: z.unknown().nullable().openapi({`; at the tip the byte-identical line is `:615` (the ONLY `blockchain:` schema property in the file - the other two `blockchain` hits, `:672` and `:685`, are example values); four commits touched the file between the two tips (`346b491f2`, `e86bffee0`, `355d82c8b`, `d2fe7d6d2`), none of them this property - instrument: `git show e559f7bb:<file> | sed -n 601p`, `git show <tip>:<file> | grep -n 'blockchain:'`, `git log --oneline e559f7bb..<tip> -- <file>`.
- **P3 the schema that owns the block.** `:615` sits inside `V2VerifyMatchSchema` (`const V2VerifyMatchSchema = sharedRegistry.register(` at `:590`, registered as `'V2VerifyMatch'` at `:591`, closing `);` before the next `const` at `:645`) - the per-document match of the v2 verify response; `DocumentDetail` (`:176-:240`) declares no `blockchain` property at all (0 hits) - instrument: `grep -n "^  '[A-Za-z0-9]*',$"` and `grep -n blockchain` over `git show <tip>:<file>`.
- **P4 why the comment sits at the schema head and not on `:614`/`:615`.** The comment_patch harness inserts only after a line inside a named range, and a range may hold comment/blank lines only (builder R4, checker C5); every line from `:590` to `:642` is code (the only comment/blank lines in `:589-:645` are `:589` and `:643`), so the nearest legal anchor to the property is the blank `:589` directly above the schema's `const` - instrument: a python scan of `git show <tip>:<file>` lines `:589-:645` for blank / `//` / `*` lines (`[589, 643]`; control `:1-:50` = 47 such lines). The comment therefore names the property it is about ("the `blockchain` property below").
- **P5 no `-` line; the ONE `+` line is ASCII (0 non-ASCII, 0 backslash), is not already at the tip (0 copies), and the three context lines are ASCII** - instrument: python `ord(c) > 127` and `lines.count()` over the tip file; the em dashes nearest the hunk are `:585` and `:594`, both OUTSIDE it.
- **P6 the whole hunk is comment/blank/one code context line.** `:588` `);` and `:590` `const V2VerifyMatchSchema = sharedRegistry.register(` are context only (never `-`); the range `:589-:589` is the blank line - instrument: `tasks/comment_patch/token_equiv.cjs lines` (builder R4, re-run at build).
- **P7 no READY diff hunks this file within 10 lines of the range** - instrument: builder R9 (`night/READY_*` scan), re-run at build; its line is quoted under "Measured results".
- **P8 Linear state.** KS-1019 Backlog (type `backlog`), P3, unassigned, not archived, 0 PR attachments, updated 2026-09-08T21:04:47Z - instrument: Linear GraphQL read 2026-09-22 18:59:14 AEST (`fetch_tickets.log`); builder R10 re-run at build.
- **P9 no OPEN pull request changes this file** - instrument: builder R11 (GitHub REST, fail closed), re-run at build.
- **P10 round-19 collision: NONE.** `Blockchain/Dev/services/originate/src/originate.openapi.ts` is in none of the 21 round-19 PR heads' file sets (0 of 38 union paths; control `Blockchain/Dev/CONTRIBUTING.md` = 1) - instrument: `git diff --name-only <tip> <head>` per head in the scratchpad clone (`union.log`). The `services/originate/` DIRECTORY is Seat B's lane (3 originate product files + 4 originate suites are in the union; this file is not).
- **P11 nothing in this task reaches a database.** The comment_patch checker runs no suite, no `tsc` and no runner - instrument: `tasks/comment_patch/checker.sh` header (gates C0-C7) and `tasks/comment_patch/prepare_clone.sh` (links one package, never runs npm).

## Lines

- `Blockchain/Dev/services/originate/src/originate.openapi.ts`:589-589

## The exact change

ONE hunk. **Scope anchor, so you never work from a bare line number:** the blank line between the closing `);` of `V2VerifyRequestSchema` (`:588`) and `const V2VerifyMatchSchema = sharedRegistry.register(` (`:590`). The comment goes on the line directly above that `const`. Both context lines are unique in the file; `:589` is blank (a single-space context line).

```diff
--- a/Blockchain/Dev/services/originate/src/originate.openapi.ts
+++ b/Blockchain/Dev/services/originate/src/originate.openapi.ts
@@ -588,3 +588,4 @@
 );
 
+// KS-1019 (Kam 2026-09-22: leave untyped). The blockchain property below is z.unknown() on purpose: its shape varies by anchoring mode (real / simulated / failed), so every drift guard is blind to it by construction; typing it is a discriminated-union product change for Peter to review, not a widening.
 const V2VerifyMatchSchema = sharedRegistry.register(
```

## What the checker measures (there is no cell here)

- **C0** the clone sits at the tip, the file is present and clean, the clone's own typescript loads.
- **C1** exactly ONE fenced ```diff block and nothing outside it.
- **C2** the diff applies at the tip (strict).
- **C3** the touched-file set is exactly `{ Blockchain/Dev/services/originate/src/originate.openapi.ts }`.
- **C4** **the code-token stream is IDENTICAL before and after** - measured by `tasks/comment_patch/token_equiv.cjs`. This is the whole proof that nothing behaves differently.
- **C4b** the multiset of directive comment lines is identical.
- **C5** the one changed line is an insert after `:589`, inside `:589-:589`.
- **C6** nothing removed (no `-` line).
- **C7** the one `+` line is in the file after, byte-exact.

## Measured results

- Builder (`night/build_comment_input.sh`) at `3bad652d1` and the REAL `tasks/comment_patch/checker.sh` on this brief's own fence in the `git clone --shared` scratchpad clone: `runs/2026-09-22_feed16-drafter-precheck/LEAVEUNTYPED/build.log` and `checker.log` (the verdict is quoted on the queue line, never here by hand).
- Nothing ran against a database; no port was opened or probed.

## Output

Exactly ONE fenced ```diff block, nothing before it and nothing after it: `--- a/Blockchain/Dev/services/originate/src/originate.openapi.ts` then `+++ b/Blockchain/Dev/services/originate/src/originate.openapi.ts`, then the one hunk above exactly as shown, header `@@ -588,3 +588,4 @@`.

## Notes for the raise (not for the model)

- **Behaviour change: none.** One comment line; C4 proves the code-token stream is identical. **Raise tier: comment-only (tier 3 / Polish).** **Closes KS-1019** - the ticket asked for "a decision on the record rather than a default nobody chose"; Kam's ruling is now recorded at the schema that publishes the block. Option b (type it as a discriminated union) is NOT taken; if it is ever wanted it is a new ticket and a Peter-reviewed PR.
- Placement: the schema head (`:590` after the patch), 26 lines above the property, because the harness cannot anchor an insert on a code line (P4). Wednesday may prefer a Claude seat to put the same sentence on `:614`/`:615` itself; the words would be identical.
- The ticket's "scope beyond originate" question (do other services publish `z.unknown()` on consumed fields) is NOT answered here: this file alone has 21 `z.unknown()` sites (`grep -c`), and the ticket's ask was a decision on THIS one.
