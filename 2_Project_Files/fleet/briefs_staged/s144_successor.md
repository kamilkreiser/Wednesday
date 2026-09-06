# SEAT A successor brief — Secuura / Blockchain, 2026-09-07 08:0x. TWO fix rounds, both gated NO GO.

## BLUF
You are a fresh seat. **s143 wrapped at 21:58** after a very strong session — its handover is in your
own tree. **Two tier-1 gates reported NO GO while it was wrapping, and both are yours.**

**Item 1 is Kam's P1 and it gates something he has ruled must happen TODAY:** #884 (the F5 
rate-limiter bypass fix). **F5 itself is CLOSED and proven** — but the fix carries two Majors of its
own. Kam has ruled that Peter and Stuart are told today **with the fix**, so this round is the
critical path to a client disclosure.

## ITEM 1 (P1, start here) — #884 round 2
**Head `f3a0379787123b45e4ffdb48d9d3db78e9661726`, base develop `306d0db923183f3b62b053f0242549e37bdf362c`.**
Full verdict in your inbox: `[QA -> Wednesday] Secuura KS-858/F5 (#884 @ f3a037978, tier 1)`, 21:50:32Z.
**Read it whole before you touch anything.**

**What HELD, so you do not re-litigate it:** all 8 mounts fire on both  spellings on a fresh HEAD
gateway (16/16, first-429 at exactly limit+1); on a fresh BASE gateway none of the 16 fires while all
8 fire canonically — a real positive control. 75 already-canonical rows across all 67 mount classes
byte-identical. 93 changed rows all land on exactly what the canonical spelling returns. Three of the
four platform suites run and passed. **F5 is closed. Do not rebuild that proof.**

**F-QA-1 — MAJOR.** `collapseRepeatedSlashes` splits on the first `?` and treats everything before it
as path, so an absolute-form target is mangled: `http://host/api/auth/login` → `http:/host/...` →
pathname `/host/api/auth/login` → **404 across the WHOLE app.** Violates RFC 9112 §3.2.2 (a server MUST
accept absolute-form) and the module's own "PATH ONLY" contract. Measured on raw sockets: base returns
429/401/200 on three routes, head returns 404 on all three; origin-form controls on head are fine, so
**the request FORM is what breaks.** Masked by nginx at the stack edge — and `index.ts`'s own KS-245
comment names where there is none: *"Dev/Demo Container Apps expose api-gateway directly with NO nginx
in front."* **The tester was careful and so is this brief: it is availability/conformance, NOT a new
security hole** — the mangled path 404s, it does not reach a handler with a guard skipped.
**Fix-shape (the tester's, prose only):** canonicalise only an ORIGIN-FORM target — return `rawUrl`
unchanged unless it starts with `/`; or collapse with a pattern that cannot eat a scheme's `//`.
**Regression cell it asks for:** a RAW-SOCKET cell driving `POST http://host/api/auth/login` through
the real app, asserting the guarded mount still runs. **`http.request()` cannot express this — it
rewrites an absolute-form target, which is very likely why nobody has seen it.**

**F-QA-2 — MAJOR (process).** **Nothing pins the production mount or its position.** The tester deleted
`app.use(normaliseRepeatedSlashes());` from `index.ts` by exact string replacement and re-ran the full
package suite: **27 files / 277 tests PASSED, unchanged.** Zero tests import `index.ts`. The 9 new
cells pin the FUNCTION and a SYNTHETIC express app the test builds itself — **not the wiring the whole
ticket rests on.** This is also the answer to the double-apply question: **the ORDERING is what makes
`proxy.ts:682` inert, and the ordering is pinned by nothing.** Close both: a cell that drives the real
startup path, and a cell that fails if the mount moves below another predicate.

## ITEM 2 — #876 round 2. **The builder's own suspicion was right, and worse than it thought.**
**Head `8d3e5208a7280af7ad6aec11c0370f1d03e6f423`.** Verdict: `[QA -> Wednesday] Secuura KS-930 round 1
(#876, tier 1)`, 22:04:18Z.

**Everything else re-derived CLEAN** — the zero-consumers safety precondition, the 40→53 suite with no
prior cell weakened, the two-layer red-proof (the tester **predicted the same 3 cells before running**),
findings 2 and 3 closed AND pinned. **NO GO is on ONE arm**, the one s143 flagged and did not cell:

> *"alpine and busybox … are also the images someone would `apk add nodejs` into. That is caught by
> `nodeish` and the unclassified-line count … but that is a claim about OTHER clauses holding, and it
> should be tested rather than asserted. I did not add a cell for it."*

**Tested. The claim is FALSE.** `nodeish` matches `/node_modules|npm|yarn|pnpm/` — **the string
"nodejs" contains none of those four**, and neither does the bare word `node`, so
`CMD ["node", "/app/dist/index.js"]` in the same stage also passes it. **6 of 8 attack shapes land
A_EXEMPT at rc 0**, and against THIS PR's base **all six are regressions**: `306d0db92` blocked every
no-nmwrite final stage outright; the head certifies them clean.
**So the inversion is right in principle and has widened a hole in practice.** Close the arm; do not
revert the inversion. Read the verdict's fix-shape before choosing.

## SHAs, all re-read together by `git ls-remote origin` at 08:0x
```
develop 306d0db923183f3b62b053f0242549e37bdf362c
#884   f3a0379787123b45e4ffdb48d9d3db78e9661726   item 1
#876   8d3e5208a7280af7ad6aec11c0370f1d03e6f423   item 2
#882   7e4603df3e4eea048031489f7b0862611e80f174   do not touch
```

## ITEM 3 (no fix — a state you must not disturb) — #882 is READY and UNGATED
**#882 round 1 is READY at `7e4603df3e4eea048031489f7b0862611e80f174`** from s143. It has NOT been gated yet; Wednesday queues that
separately. **Do not push to #882.**

## HOLDS
- **Nothing merges. Nothing deploys. The demo box is never touched.**
- **No external communication to any human** — the F5 disclosure to Peter and Stuart is drafted and
  held; **Kam sends it, nobody else**, once #884 is clean.
- **New work on a NEW branch; fix rounds on the PR's own branch.** Push to #882 not at all.
- **Never delete — quarantine by rename.** Restore every tamper by inverse edit verified with sha256,
  **then RE-RUN** — a hash proves the bytes, only a run proves the file still works.
- **A control must be able to fail**, and a red-proof must break ONLY the guard it is for.
- **Count first (`grep -c`); never truncate a list you are about to call complete.**
- **Handovers to Peter or Stuart are TEST BLOCKS**, never a list of PRs.
- **Ticket creation AGGREGATES** — one larger ticket per logical path (Kam, 2026-09-06).

RULED BY KAM, NOT YET IN AN ARTEFACT
Five older rulings are ruled-but-undelivered and **none is an action for you** — listed so you do not
re-raise them:
- secuura-ci-billing: "wait" -> Kam's org billing access. Nothing for you.
- secuura-agent-github-identity: "identity" -> a Kam org action. Nothing for you.
- secuura-dependabot-triage: "close-and-rescope" -> Peter's repo. Nothing for you.
- secuura-ks229-disclosure-mailbox: "later" -> deliberately deferred.
- secuura-ps-759-760-merge-owner: "kam-merges" -> Platform S, outside this seat's scope.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **2026-09-07 08:0x: #884 round 2 is the critical path to a client disclosure Kam has ruled for TODAY.**
- **2026-09-07 07:4x: #882 is READY and awaiting a gate — push nothing to it.**
- **2026-09-05 23:24: do NOT narrate an open defect in a published contract** — a defect is not a guarantee.
- **2026-09-07: MFA on the demo platform admin stays OFF** (Kam: "later, revisit after the suites run").

PROVENANCE:
- Every #884 finding, measurement and fix-shape | the QA verdict mail 2026-09-06T21:50:32Z, quoted not paraphrased — Wednesday has re-run none of it | read 2026-09-07
- Every #876 finding, including that nodeish cannot match "nodejs" or bare "node" | the QA verdict mail 2026-09-06T22:04:18Z, quoted not paraphrased | read 2026-09-07
- The four PR heads and develop, all re-read together | git ls-remote origin from Wednesday's own seat, same action as writing this line | read 2026-09-07
- That Kam ruled the disclosure for today with the fix | `kam_rulings_today.sh`, card secuura-f5-disclosure-timing => withfix, 06:43 | read 2026-09-07
- Whether the Dev/Demo Container Apps are actually exposed without nginx | NOT ESTABLISHED — the KS-245 comment says so; the VM demo answered with `server: nginx` this morning | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 08:07
