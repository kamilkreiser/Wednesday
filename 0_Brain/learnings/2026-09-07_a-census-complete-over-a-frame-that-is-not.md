---
date: 2026-09-07
type: correction
source: named by the Datasec/NexusAI agent (s44) while falsifying its own fix; extended by Wednesday with two more instances from the same day
status: live
tier: M
---

# A census that looks complete over a frame that is not — the instrument answers about the FRAME, and the answer gets written down as if it were about the WORLD

**The operative case, so the headline matches it:** you are about to write down *"there are three
writers"*, *"the accounts are X"*, *"every occurrence is handled"*, *"no stale pointer remains"* —
**any statement of the form "here is the complete set."** Stop and ask: **complete over what?** Every
one of the instances below was a **correct** answer to the question the instrument was actually asked,
and every one was recorded as an answer to a larger question nobody noticed had been narrowed.

**The agent's formulation, adopted verbatim:**
> The instrument answers about the frame, and the answer gets written down as if it were about the
> world.

## Six instances, all on 2026-09-07, four repos, four instruments

| The census | Correct over its frame | The frame nobody stated |
|---|---|---|
| `firstRunComplete`'s writers — three found, all real | `backend/` | **three more in `static/js/`**, reached by a connection test, a validation pass and a checkbox |
| `gh auth status` — the logged-in account | `hosts.yml` | **the keychain the token actually comes from**, holding a different account |
| `assignedKeys()` — the keys assigned to the response | the two syntaxes its regexes describe | spreads, computed keys, `Object.assign`, two keys on one physical line |
| the `.dockerignore` cells | every pattern **present in the file** | whether anything is **excluded** — *a string in a file is not a behaviour* |
| `doctor.sh`'s travel-pointer sweep (**Wednesday's own**) | `!CODING/*/*/2_Project_Files/.git/config` | **the shared vault**, which is the one repo every agent writes to and the one that actually broke |
| *"~8 lines above the redaction"* (**Wednesday's own**) | the gate's **prose** | the file — where it is **1** line above, and the key path 11 below |

**Two of the six are Wednesday's.** That is the point of the file: the shape is not an agent problem
or a tooling problem, it is what a competent search looks like from the inside.

## Why it defeats the existing rules

- **The positive control passes.** The instrument fires, on real hits, correctly. Nothing is broken.
- **The negative control passes.** An impossible pattern returns nothing, as it should.
- **[[2026-08-07_a-check-that-cannot-fail]] does not catch it** — this check *can* fail, and does,
  within its frame.
- **[[2026-08-14_i-read-representations-they-read-sources]] does not catch it** — the number *was*
  read from the source. The source was smaller than the question.

**The frame is invisible to the author because the author chose it**, usually for a good reason
(*"the writers will be in the backend"*), and it never appears in the sentence that reports the result.

## How to apply

1. **Name the frame in the sentence, every time.** *"Three writers **in `backend/`**"*, *"no stale
   pointer **in `!CODING/*/*/`**"*, *"the account **per `hosts.yml`**"*. **A stated frame is one
   somebody can widen; an unstated one is invisible to the reader and to you.** This is the whole
   defence and it costs four words.
2. **For any "complete set" claim, ask what would live OUTSIDE the frame** — another language, another
   directory, a non-tracked path, a different file type, a caller in a template, a value rather than a
   key. **Then look there once.** The `firstRunComplete` case cost one `git grep` over `static/`.
3. **Language and directory boundaries are the commonest frames** and the least visible: a backend
   grep will not see the frontend caller; an `*.js` glob will not see `.ts`; a `2_Project_Files/`
   sweep will not see the sibling repo.
4. **When a census underpins a DECISION, the frame is load-bearing and belongs in the provenance
   line**, not just in the prose — the RD-361 fix rested entirely on a three-writer census, and the
   census was right.
5. **Suspect a census hardest when it is convenient** — three writers, one function, one caller is a
   tidy story, and tidiness is what stops the next question being asked
   ([[2026-08-16_classification-is-the-field-that-grants-authority]]).
6. **It nests with the other two families:** *a check that cannot fail* (the result was never in
   doubt), *a claim whose instrument is unnamed* (the evidence was never fetched), and this one — **the
   evidence was fetched, from a smaller world than the claim.**

**Related:** [[2026-08-07_a-check-that-cannot-fail]] · [[2026-08-14_i-read-representations-they-read-sources]] ·
[[2026-08-15_a-cap-is-never-neutral]] (a cap is a frame with a number on it) ·
[[2026-08-07_enumerate-every-surface-before-done]] (the closing check is absence — over which surfaces?) ·
[[2026-08-13_containment-never-run-is-a-claim]].
