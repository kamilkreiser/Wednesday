#1270 KS-1275: point the lifecycle verb prose at LIFECYCLE_EVENT_ACTIONS
head 448b8b7fdd87a145acc895c4138811f34aa53c59

## What

The two comment sites #1252 left behind on KS-1275. Both hand-enumerated the accepted lifecycle verbs and both had drifted; they now point at the same two sources of truth the published description does, and name no verb at all.

- `services/originate/src/repositories/lifecycleEventRepo.ts:5-8` — named four verbs plus the KS-389 mapping, and omitted `share-attach-consent` (KS-534), `protect`/`unprotect` (KS-556) and the KS-1172/KS-1173 additions.
- `services/originate/src/routes/documents.ts:2428-2432` — named those four **plus** the KS-415/PS-235 share-edit four.

So the two prose sites had drifted apart from **each other**, not only from the enum. Pointing both at `LIFECYCLE_EVENT_ACTIONS` and `docs/VOCABULARY.md` closes both drifts at once, as #1252 did for the published description.

`migrations/037` is an applied migration and is untouched.

## Test Evidence

**Touched:** `services/originate/src/repositories/lifecycleEventRepo.ts`, `services/originate/src/routes/documents.ts`. Comment lines only.

**Ran** — all in `worktrees/s-b29-ks1275` at develop `4db87c3e4b98`, `packages/shared` BUILT (88 dist files), `npx jest --runInBand` in `services/originate`:

| arm | result |
|---|---|
| originate BARE (pre-edit files restored, sha256-verified) | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED (this commit, sha256-verified restore) | **878 passed / 878, 74 suites**, rc 0 |
| `tsc --noEmit` BARE | rc 0 |
| `tsc --noEmit` PATCHED | rc 0 |

Identical readings either side, which is what a comment-only change must produce — and the BARE arm is what makes that a measurement rather than an assumption. Both restores were asserted by sha256 against the pre-tamper hashes, by content, never `git checkout`.

**AST-equivalence, with a control that fires.** Both files transpiled with `removeComments: true` (typescript 5.9.3) and the emitted JavaScript compared:

```
EQUIVALENT  emit 3155 vs 3155 bytes   diag 0/0  lifecycleEventRepo.ts
EQUIVALENT  emit 89849 vs 89849 bytes diag 0/0  documents.ts
```

CONTROL: a **one-character** change to a numeric literal inside a template literal (`LIMIT 1` -> `LIMIT 9`) reads `DIFFERENT` **at an identical emit size of 3155 bytes**, and the tool names the divergent line. So "EQUIVALENT at the same byte count" is not a vacuous pass — this is precisely the case a raw token scan misses, because it swallows comments into one template-literal token.

**Also asserted:** none of the seven removed verb names survives in either file (7 x 2 greps, all 0), against a control showing `LIFECYCLE_EVENT_ACTIONS` present 4 times in `documents.ts` so the greps work.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up). `11/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves in this PR, so there is no LEG-8-PORT reading to give.
- `packages/shared` was run on the sibling head in this batch, not separately here; this PR touches no source its text-scanning guards read differently (comments only).
- No runtime behaviour is exercised, because none changes. The claim this PR makes is exactly "the emitted JavaScript is unchanged", and that is the thing measured.

Refs KS-1275

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Base attribution for the counts above (per the 19:30Z fleet correction)

develop moved to `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9` at 19:20Z, **after** this PR was built and pushed. **This worktree does not contain it** — the object is not present in the checkout at all, because no fetch was taken: `git cat-file -t d7cdecf1d2ee` fails here, against a positive control where `git cat-file -t 4db87c3e4b98` returns `commit`. The worktree base is `4db87c3e4b98` (`HEAD~1`).

So every count in this PR measures **`4db87c3e4b98` + this change**. The push gate read `pre_push_hook_base` **28/0**, `fixture_guard` **6/0**, `run_shell_suites` **49/0**, shell suites **60 passed / 0 failed of 60**, `^FIXTURE BUILD FAILED` **0** — the same quadruple the fleet declaration names for `d7cdecf1`, but **this is not a confirmation of it**: a pre-merge worktree reading the old quadruple is the old tree agreeing with itself.

Nothing about the comment-only claim depends on the base: the AST-equivalence proof is about the two files' emitted output.
