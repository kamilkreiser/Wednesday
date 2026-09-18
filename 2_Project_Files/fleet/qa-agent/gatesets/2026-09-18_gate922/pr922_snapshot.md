# PR #922 SOURCE SNAPSHOT — captured read-only from the GitHub API by the #922 gate drafter

This gate has NO seat READY mail at this head. The seat's own words at the time of capture are the PR body and its comments, reproduced
VERBATIM below. The capture metadata is the API's reading, not the seat's claim. NOTE: the body's Test Evidence and its PREFLIGHT line were
written at e60a24c50 (the 2026-09-14 push), NOT at the head this gate is about; the body never mentions the head below.

- captured_at: 2026-09-18T00:45:15Z
- pr: 922  state: open  draft: False  merged: False  mergeable: True  mergeable_state: unstable
- head_sha (API): 8664826e53cc47d4dd69c784926c9c14af444cec
- head_ref: kamilkreiser/ks-679-anchor-id-format-false
- base: develop
- commits: 4  changed_files: 5
- title: KS-679: publish the anchor id shape the service actually mints
- formal reviews: 0  requested_reviewers: 0
- body_sha256: d2d05aae85229ed9d66cafc7bfd78c50183b0f57b66ec1c34a8bc6d70dd1acaf

## PR BODY (verbatim)

<!-- ⚠️ Keep the "Before merging" block and the two acknowledgment checkboxes below —
     they appear on every PR by design and the pr-premerge-ack workflow parses them. -->

> ## ⚠️ Before merging — run the pre-merge suites
> **Do not merge until the pre-merge tests have been run and pass.** The fast PR
> gate is not sufficient on its own. Run each suite's pre-merge tier — locally
> against the stack, or by dispatching **`pre-merge-platform-suites.yml`**
> (Actions → *pre-merge* → *Run workflow*) — confirm it is green, then tick its box.

### Pre-merge acknowledgment (author)

Tick each box **only after** you have run that suite's pre-merge tier and it passed:

- [ ] <!--ack:schemathesis--> **Schemathesis** pre-merge sweep run and **passing** (`python3 scripts/run.py pre-merge`)
- [ ] <!--ack:akto--> **Akto** pre-merge scan run and **passing** (`npm run test:pre-merge`)

**Left unticked: neither pre-merge tier was run by the author. Under the 2026-09-11 merge flow the QA gate at this head is the test pass; its report names what ran.**

### PII review (KS-256 R15/R16)

<!-- KS-256 · KAMIL-REVIEW 2026-07-20. Why he asked for it, verbatim: "put the PII-review sign-off
     as a checkbox in the PR description so it's auditable, not implicit."
     These boxes deliberately carry NO ack marker:
     pr-premerge-ack.yml matches only ack:schemathesis and ack:akto, so this is a human gate, not
     a CI-enforced one. Do NOT write a literal ack comment marker anywhere in this block — an
     inner comment-close would terminate this comment early and render the remainder as visible
     text in every PR. Delete the section only if the PR genuinely cannot touch published data. -->

Tick if this PR changes **anything that reaches a customer-facing artifact** — the published
OpenAPI spec, example values, fixtures, seed data, logs or error messages:

- [x] **No real personal data ships.** Emails, names, phone numbers, addresses, wallet/stake
      addresses, government or tax IDs, and free text captured from real traffic are placeholdered
      — not merely "looks fake to me".
- [x] **No credentials ship.** No password, token, API key, secret or private key, including in an
      example that "obviously isn't real".
- [ ] **Reviewed by the person who worked the redaction queue**, not just the author. Name them:
      <!-- name -->

> Not applicable? Say so explicitly rather than leaving the boxes blank — a blank box reads as
> "not checked", which is the state this section exists to make visible.

**APPLIES — a published example value changes. Box 1 ticked after reading the one-line yaml hunk (`-        id: anc_01HC9ZN4ANCHORFIXTURE1` / `+        id: anchor_00000000-0000-4000-8000-000000000032` at `docs/openapi/secuura-api.yaml:1032`): at-signs 0, `secuura.ai` 0 (control: 1 on a planted at-sign). Box 2 ticked: the value is a synthetic uuid in the fixture set's own all-zero resource range (`contract.mjs:98-101`) — format-true, account-false. Box 3 left unticked: no redaction queue was worked for this change — the hunk is one example id; left unticked for that reason, not left blank.**

---

## Linear

https://linear.app/secuura/issue/KS-679

## BLUF

**The published `Anchor.id` was a format the anchoring service has never minted**, and because it lived in the canonical fixture set, guard rule E8 **certified** it rather than caught it. An integrator copying it out of Swagger UI got a shape the platform does not issue.

- **mints:** `anchor_${randomUUID()}` — `services/anchoring/src/index.ts:423` (batch appends `_<i>` at `:727`)
- **published:** `anc_01HC9ZN4ANCHORFIXTURE1`
- **live `anchor_store`:** **0** rows matching `anc\_%` against **61,507** matching `anchor\_%` — the control is what makes the zero readable

Independent corroboration in the tree: `services/anchoring/src/__tests__/ks705-submission-idempotency.test.ts:45` uses `anchor_a93bd8dd-10c8-4d52-b12e-c0bff6f5c790`.

## The ticket's prediction came true by a different route

KS-679 says #568 "is about to make that format the canonical fixture". **#568 was closed unmerged — and the promotion happened anyway.** The value now sits in `FX.anchor.id` *and* in the guard's `FIXTURE_ID_VALUES`, which is exactly the state the ticket warned about: membership makes E8 vouch for it. So the estate could not have found this, and a guard was never going to. It needed a cell.

## Making it format-true walked it into E7 — and that is a real gap, not a nuisance

At 43 chars the **true** shape crosses E7's 40-char high-entropy threshold; the **false** 27-char one never did. **E7 was rejecting the real shape and passing the fake one.**

`<prefix>_<uuid>` is a **class**, measured: **13 distinct prefixes across 9 services, 17 mint sites** — `anchor_` `audit_` `batch_` `ce_` `conn_` `did_` `event_` `evt_` `int_` `req_` `site_` `sync_` `ts_`. So it belongs in `BENIGN_SHAPES`, not in a per-path allowlist entry — the next service to publish its own id would hit the same wall.

The list's own comment says *"widening this list is a review decision, not a convenience."* The argument: **a uuid with a namespace prefix is no more secret than the bare uuid already on the line above**, and the pattern is anchored to an exact uuid so a key or token cannot satisfy it.

**Controlled against seven shapes**, and the widening exempts none of the dangerous ones:

| value | verdict |
|---|---|
| `anchor_00000000-…-000000000032` (the new fixture) | BENIGN |
| `req_3f2b1c9e-…` (a real request id) | BENIGN |
| `sk_live_51H8xQ2eZ…` (Stripe-shaped live key) | **E7 FIRES** |
| `ghp_16C7e42F292c…` (GitHub PAT) | **E7 FIRES** |
| `AKIAIOSFODNN7EXAMPLE…` (AWS-key blob) | **E7 FIRES** |
| `anchor_not-a-uuid-at-all-…` (prefix + junk) | **E7 FIRES** |
| a JWT | below E7's threshold — **E2** covers JWTs |

## The cell whose absence made this possible

`describe('KS-256 — fixture ids match the format the API actually returns')` already pinned tenant, issuer, holder and the document id. **It did not pin the anchor.** Now it does — pinning **prefix and uuid separately**, because asserting the whole literal would pass equally for a value that is merely *unchanged*, which is not the property the cell is for.

## Base

`develop`. The reviewed head `2b5075e9f` (2026-09-09) has develop `852e1fff7` merged in on 2026-09-14 (`a7d9e2943`, `--no-ff`) — no rebase, no cherry-pick; `2b5075e9f` is an ancestor of this head. develop moved only the generated yaml among this PR's five files, far from the one example line this PR changes; `check:openapi` re-asserted the merged yaml byte-equal to the generator's output (no regeneration commit). Then ONE commit (`e60a24c50`) for the review's first ask.

## The review's three asks (2026-09-09)

1. **The `BENIGN_SHAPES` widening had no test.** The seven-case control from this body is now a `describe` in `packages/shared/src/__tests__/ks256-spec-example-contract.test.ts`, driven through the guard itself (`check-spec-examples.mjs --json`) on a one-field spec built at run time — the same harness as the positive control. Red-proofs are in Test Evidence below.
2. **The body lacked the Linear URL and the two ack boxes.** Both above.
3. **The ticket's open question.** Answered on the ticket by the reviewer (KS-679, 2026-09-09): `anchor_<uuid>` is what we want published.

## Test Evidence

Written at `e60a24c5024d0adae3fae8966bbd4e243e8b581c` by the seat that ran the tests (2026-09-14; node v24.7.0, /bin/bash 3.2.57, darwin arm64, load 3.5–6.2 during the runs).

**Touched** (5 files; `git diff --name-only develop...HEAD` = exactly these): `packages/shared/src/openapi/examples/fixtures.ts` (+18 −1, the id) · `scripts/spec-examples/check/contract.mjs` (+13 −1, the E7 benign shape) · `packages/shared/src/__tests__/ks256-spec-example-contract.test.ts` (+20 the pinning cell, +119 the seven-case control) · `services/anchoring/src/anchoring.openapi.ts` (+3, comment only) · `docs/openapi/secuura-api.yaml` (+1 −1, regenerated).

**Ran**
- `npm ci` (1,937 packages, 0 tracked changes); `npm run build -w packages/shared` on the raw head and again on the merged tree.
- `packages/shared` vitest at `2b5075e9f`: **788 passed (788), 41 files** (the 09-09 figure); at this head: **844 passed (844), 43 files** (develop added two files between the base and today; this PR adds 8 cells).
- The seven-case control: **8 / 8** — the new fixture `anchor_<uuid>` and a `req_<uuid>` request id are BENIGN (E7 silent); a Stripe-shaped key, a GitHub-PAT-shaped token, an AWS-key-shaped blob and `anchor_` + non-uuid junk all fire E7; a JWT is E2's and never E7's — its dots fall outside E7's character class `[A-Za-z0-9+/=_-]{40,}`, which is the actual reason (this body's earlier "below E7's threshold" was the wrong reason for the right row); plus one cell asserting every row but the JWT is ≥ 40 chars of E7's class, so a row cannot silently stop being E7-shaped. The four dangerous values are assembled at run time from fragments with each provider's fixed-length run broken by a `-` (control: `grep -E 'ghp_[A-Za-z0-9]{36}|sk_live_[A-Za-z0-9]{24}|AKIA[A-Z0-9]{16}'` on the file → 0; positive control on a here-string → 1), planted on an OBJECT example field (`opaqueRef`, a name no name-keyed rule matches).
- **Red-proofs on `contract.mjs`** (the regex code line's anchor count 1; restored by content with the whole-file sha256 asserted; 8/8 after each): the `<prefix>_<uuid>` line deleted (narrowed back) → **2 failed / 6 passed**, exactly the two benign cells; the regex loosened to `/^[a-z]+_.+$/i` → **3 failed / 5 passed** — the prefix+junk, Stripe-shaped and GitHub-shaped cells (every underscore-bearing dangerous row now matched; the AWS row stayed green); `[a-z]+_` → `[a-z]*_?` → **0 failed** — that tamper only admits a bare uuid, which the line above already exempts, so it is not a loosening these cells can see (said, not hidden).
- **The E7 discriminator by hand, both directions** (the reviewer's own gate): a temp spec with `anchor_00000000-0000-4000-8000-000000000032` as an example → the guard at this head: **0 findings**; the same value against develop's guard (a read-only export of `scripts/spec-examples` at `852e1fff7`, `contract.mjs` blob `43a9c5dea`): **1 E7 finding, rc 1**.
- `npm run check:openapi` on the merged tree — **rc 0** (`405 example blocks`). Controls on the yaml at this head: `anc_01HC9ZN4ANCHORFIXTURE1` 0 (1 on develop), `anchor_…0032` 1 (0 on develop), `anchorId: example-anchorId` 4 (4 on develop — pre-existing, unchanged).
- **Pre-push preflight, in-hook, as the push ran it:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` (10:26:50Z → 10:32:47Z) — legs 3/4/8 SKIPPED (no local stack); leg 1 `OK — spec is in sync`; legs 6/7 `OK — no advisories outside the triaged baseline` (`03d1680e3` both sides); leg 14 `shell suites: 33 passed, 0 failed (of 33)`; leg 15 `all 21 tracked guards accounted for`, `13 code guards passed`. Push protocol: tracking ref CHANGED `2b5075e9f` → `e60a24c50`, fast-forward; config identical; 0 other refs changed (the one DIFF was another seat's new worktree, attributed, not restored).

**NOT run — stated plainly**
- **Schemathesis / Akto / Playwright / k6** (`systemTest/schemathesis` · `systemTest/akto` · `systemTest/playwright` · `systemTest/performance`) — not run. The reviewer's own line: *"No system test suite is owed for this one: it is a documentation example plus a guard shape, `Anchor.id` carries no `format` or `pattern`, and no route, schema or status code moves."*
- **Nothing live.** No stack request, no deploy.
- **External consumers hard-coding the old `anc_` literal** are not visible from the repo.
- The batch shape `anchor_<uuid>_<i>` still trips E7 — out of scope (nothing publishes it); the regex stays anchored.

**Migrations + config:** none.

Closes KS-679.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Ba3AnrjGgyT2gsztzk4nKn (original) · https://claude.ai/code/session_01HaQ7755yF8PVZciV9rmK3c (2026-09-14 merge-in + the seven-case cell)


## ISSUE COMMENTS (verbatim, oldest first)

### linear[bot] — 2026-09-09T07:58:23Z (updated 2026-09-09T07:58:41Z)

<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-679/published-anchorid-is-anc-but-anchoring-only-ever-mints-anchor-uuid">KS-679 Published Anchor.id is anc_… but anchoring only ever mints anchor_&lt;uuid&gt; — format-false, live on develop, and #568 promotes it to the canonical fixture</a></summary>
<p>

## BLUF

**The published** `Anchor` **example carries an id in a format the anchoring service has never minted, and #568 is about to make that format the canonical fixture.** The service mints `` `anchor_${randomUUID()}` ``; the spec publishes `anc_…`.

This is the **fourth** instance of the class KS-665 keeps surfacing — a published value that is *plausible* but *false*, which the guard **certifies rather than catches** because the value sits in the fixture set (after 16 `address` fields, `userAgent`, and `channelName: Demo Issuer`).

It is **live on** `develop` **today** — not only on #568.

---

## Evidence

**What the service actually mints** — `services/anchoring/src/index.ts`:

```js
:417   const anchorId = `anchor_${require('crypto').randomUUID()}`;
:699   const anchorId = `anchor_${require('crypto').randomUUID()}_${i}`;   // batch
```

**What the live table holds** (local stack, `anchor_store`, 2026-08-21):

| Query | Rows |
| -- | -- |
| `select count(*) … where id like 'anc\_%'` — the **published** shape | **0** |
| `select count(*) … where id like 'anchor\_%'` — the **real** shape (control) | **61,507** |
| `select split_part(id,'_',1), count(*) … group by 1` | exactly one group: `anchor` → 61,507 |

The control proves the `LIKE` can match, so the zero discriminates. A real id: `anchor_e83ba0cc-47b0-4bd1-8117-52120de467ef` — `anchor_` + a UUID, exactly as line 417 says.

**Where** `anc_` **occurs at all.** Repo-wide on `develop`, **exactly 2 occurrences**, and they are the same example twice: `docs/openapi/secuura-api.yaml:893` and its source `services/anchoring/src/anchoring.openapi.ts:63`. Control: `anchor_` occurs **52** times in the same service. Nothing anywhere mints `anc_` — it exists only in the published example.

---

## What each branch publishes — and why #568 makes it worse

| Ref | Published `Anchor.id` | Backed by |
| -- | -- | -- |
| `origin/develop` | `anc_01HC9ZP3WXYZQ12345VWXY` | a raw literal, in no fixture set |
| `c114ceddd` (#568) | `anc_01HC9ZN4ANCHORFIXTURE1` | `FX.anchor.id` — the canonical fixture |

#568's change is *right in its own terms* and its comment says so honestly (`anchoring.openapi.ts:63`): there were two different anchor ids for one canonical anchor, and collapsing them onto `FX` is exactly what `FX` exists for. **The problem is which shape it collapsed onto.** After #568, a wrong format stops being a stray literal and becomes the fixture the whole spec draws from — and `FIXTURE_ID_VALUES` membership then makes E8 *vouch* for it.

`fixtures.ts` states the contract this breaks, in its own words:

> ⚠ NOTHING HERE IDENTIFIES A LIVE ACCOUNT — and that is the point. … Every value below is *format-true and account-false*: shaped exactly like the real thing, backed by nothing.

`anc_01HC9ZN4ANCHORFIXTURE1` is account-false ✅ and **format-false** ❌. It is not shaped like the real thing.

---

## Fix

Change `FX.anchor.id` (`packages/shared/src/openapi/examples/fixtures.ts:209`) to the shape the service mints — `anchor_` + a fixture UUID from the existing all-zero family, keeping it account-false:

```
anchor_00000000-0000-4000-8000-000000000030
```

Then regenerate the spec so `secuura-api.yaml:893` follows.

⚠ **This interacts with rule E7 and must not be done blind.** `HIGH_ENTROPY_RE` is `/^[A-Za-z0-9+/=_-]{40,}$/`, and `anchor_` + a 36-char UUID is **43 characters** — it will trip E7 unless the prefixed-UUID shape is admitted to `BENIGN_SHAPES`. KS-665's design comment already proposes that widening and tested it (proposed set → exit 0; the seeded-account leak control → still exit 1). **Land the E7 widening first, or this fix turns the build red.**

---

## Sequencing

Implementation deferred to the post-#568 tranche, per the KS-665 plan — a branch off `c114ceddd` cannot reach `develop` until #568 merges, and this touches a file PeterD is actively editing.

**One call from PeterD:** the shape above assumes `anchor_<uuid>` is what you want published. If you would rather keep a ULID-ish opaque id in the spec, then the *service* is the thing that is inconsistent, and this becomes a different (larger) ticket about id format across the platform. Your call — but the spec and the service should not disagree.

---

**Verified by:** kamil.kreiser, 2026-08-21 — mint sites read, live `anchor_store` census with a passing control, repo-wide occurrence sweep, both refs compared. Working tree untouched. Related: KS-665 (design), KS-256/#568.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-679-publish-the-anchor-id-shape-the-service-actually-mints-8420cd99bbc6">Review in Linear</a></p>


### PeterObeden — 2026-09-09T12:25:49Z (updated 2026-09-09T12:25:49Z)

## Review — not approving yet, and none of the three reasons is about the substance

First, credit where it is due: the diagnosis here is right, and the write-up is unusually honest — the "NOT run" section naming the external-consumer blind spot is exactly the kind of thing that makes a PR easy to review. I re-derived the core claims independently rather than taking the body at its word, and they hold.

### What I verified myself

| Claim | Verdict | What I read / ran |
|---|---|---|
| Service mints `anchor_${randomUUID()}` | Confirmed | `services/anchoring/src/index.ts:423`, verbatim |
| Batch path appends `_<i>` | Confirmed | `services/anchoring/src/index.ts:727` |
| Spec published `anc_…` | Confirmed | pre-change `docs/openapi/secuura-api.yaml:1032` |
| The false value sat in `FIXTURE_ID_VALUES`, so E8 certified it | Confirmed | pre-change `scripts/spec-examples/check/contract.mjs:101` |
| True shape trips E7, false shape never did | **Reproduced** | `HIGH_ENTROPY_RE` at `contract.mjs:252`. Ran both guards side by side: `anchor_0000…0032` (43 ch) fires E7 on `develop`, benign on this branch; `anc_01HC9ZN4…` (27 ch) never reached E7 either way |
| The widening exempts none of the dangerous shapes | **Reproduced, 9 cases** | Stripe-shaped `sk_live_…`, GitHub PAT, AWS-key blob and `anchor_<junk>` all still fire E7 on this branch. `req_<uuid>` and the new fixture go benign, as intended |
| Spec regenerated cleanly | Confirmed | 1 insertion / 1 deletion; `anc_` now appears **0** times in the generated spec; the only three remaining repo occurrences are the history comments |
| No runtime behaviour changed | Confirmed | `services/anchoring/src/anchoring.openapi.ts:63-68` is comment-only; `id: FX.anchor.id` is untouched |
| `…0032` rather than the ticket's `…0030` | Right call, and better than the ticket | `…0030` is `FX.document.uuid` (`contract.mjs:100`) and `…0031` is `FX.wallet.challengeId` (`:117`) — the ticket's suggested value would have collided |

The new cell is red on the old literal by construction (`'anc' !== 'anchor'`), and pinning prefix and uuid separately rather than the whole literal is the right instinct — asserting the literal would have passed for a value that was merely unchanged.

Branch hygiene is clean: correct direction into `develop`, one commit, no merge commits, 2 commits behind `develop` and neither touches any of these five files, so no conflict risk.

### The three things holding up approval

**1. The `BENIGN_SHAPES` widening is the one part with no test.** `BENIGN_SHAPES` is read only by `rules-example.mjs:88`; nothing under `packages/shared` imports it, so there is no cell that would notice the anchor being dropped, the regex being loosened, or the entry being narrowed back and reddening the build. The seven-case control already exists and already passes — it just lives in the PR body rather than in the repo. Committing it as a cell (the four dangerous shapes still fire, `<prefix>_<uuid>` does not) would close this in a few lines. The list's own comment sets the bar here: *"widening this list is a review decision, not a convenience"* — a committed control is what makes that review decision durable.

**2. PR body is missing the Linear URL and the two pre-merge ack checkboxes.** The linkback is a bot comment rather than the body, so the body itself has neither. Small, but it is the bit the merge gate reads.

**3. The ticket's open question to me has not been answered on the record.** KS-679 asks explicitly whether `anchor_<uuid>` is the shape we want published, or whether the *service* is the inconsistent side. It is: publishing what the service mints is right, and this PR does that. But that answer should sit on the ticket rather than be inferred from the PR — I will add it there so it is recorded.

### Minor, non-blocking — worth a line in the comment rather than a change

- The prefix census (13 prefixes / 17 sites) does not include **`key_`** — `services/security/src/index.ts:1023` and `services/originate/src/routes/adminConfig.ts:919`. Both are record ids and both say so in their own comments, so the widening is still sound; it is just that `key_` is the one prefix whose *name* argues against the change, and it reads stronger if the comment names it and disposes of it rather than omitting it.
- The regex is anchored, so the batch shape `anchor_<uuid>_<i>` from `index.ts:727` still trips E7. Nothing publishes it today, so this is a scope note rather than a defect — either `(?:_\d+)?$` or a line saying batch is out of scope.
- Four example blocks still carry `anchorId: example-anchorId`, also not a shape the service mints. Pre-existing and unchanged by this PR (4 on `develop`, 4 here) — flagging only so it is not lost.
- Branch name does not follow Linear's suggested `gitBranchName`. Cosmetic.

### What I did not run, so it is not evidence from me

I did not re-run the `packages/shared` suite, `check:openapi`, the `packages/shared` build, or the anchoring suite — those numbers are yours and I am reporting them as unverified rather than as corroborated. The one gate I did reproduce independently is the E7 behaviour, and it came out exactly as described. I did not attempt to re-verify the `threadTokenMint.test.ts` attribution to `BACKLOG.md:136`.

No system test suite is owed for this one: it is a documentation example plus a guard shape, `Anchor.id` carries no `format` or `pattern`, and no route, schema or status code moves. Nothing live was touched.

Happy to approve as soon as the control is committed and the body is filled in — the change itself is good, and the reasoning in the comments is the sort that will still make sense to whoever reads it in a year.


### kksecura — 2026-09-14T10:33:43Z (updated 2026-09-14T10:33:43Z)

## The three things holding up approval (2026-09-09) — each landed or cited, at `e60a24c5024d0adae3fae8966bbd4e243e8b581c`

**1. "The `BENIGN_SHAPES` widening is the one part with no test."** — **LANDED** at `packages/shared/src/__tests__/ks256-spec-example-contract.test.ts:370-489`: seven cells through the guard itself (`check-spec-examples.mjs --json`, the file's own `runGuardOn` harness, a one-field spec built at run time), plus one cell asserting every row but the JWT is ≥ 40 chars of E7's class so a row cannot silently stop being E7-shaped. Rows: `anchor_<uuid>` (the new fixture) and `req_<uuid>` BENIGN; a Stripe-shaped key, a GitHub-PAT-shaped token, an AWS-key-shaped blob and `anchor_` + non-uuid junk all fire E7; a JWT is E2's and never E7's — the dots fall outside E7's character class, which is the actual reason (the body's "below the threshold" was the wrong reason for the right row). The four dangerous values are assembled at run time from fragments with each provider's fixed-length run broken by a `-`, so no committed literal matches a real key pattern (grep control on the file → 0; positive control → 1). Red-proofs on `contract.mjs`, restored by content with the sha256 asserted: the regex line deleted (narrowed back) → the two benign cells red, the four dangerous green; loosened to `/^[a-z]+_.+$/i` → the prefix+junk, Stripe-shaped and GitHub-shaped cells red; `[a-z]+_` → `[a-z]*_?` → no cell reds — that tamper only admits a bare uuid the line above already exempts, so it is not a loosening the cells can see; said rather than hidden.

**2. "PR body is missing the Linear URL and the two pre-merge ack checkboxes."** — **LANDED**: `## Linear` → the KS-679 URL; both ack boxes present, unticked, with the reason (under the 2026-09-11 merge flow the QA gate at this head is the test pass); the PII section filled from the read hunk.

**3. "The ticket's open question to me has not been answered on the record."** — **DONE BY THE REVIEWER**: KS-679 comment of 2026-09-09T12:26Z records it — *"`anchor_<uuid>` is what we want published."* Cited; nothing further.

### The four non-blocking notes, one line each
- **`key_`** — not added to the census in code (nothing beyond the three asks); recorded here: `services/security/src/index.ts:1023` and `services/originate/src/routes/adminConfig.ts:919` are record ids by their own comments, so the widening stands (`key_` occurs 0 times in `contract.mjs` at this head — measured).
- **`anchor_<uuid>_<i>`** (the batch shape) — out of scope: nothing publishes it; the regex stays anchored.
- **The four `anchorId: example-anchorId` blocks** — pre-existing and unchanged (4 on develop `852e1fff7`, 4 at this head); for the board, not this PR.
- **The branch name** — cosmetic, unchanged.

### Since the review
develop `852e1fff7` merged in (`a7d9e2943`, `--no-ff`; `2b5075e9f` stays an ancestor — no rebase); `check:openapi` rc 0 on the merged tree (no regeneration needed); `packages/shared` **844 passed (844), 43 files** at this head (788 / 41 at the reviewed head — develop added two files; this PR adds 8 cells); the E7 discriminator re-run by hand both directions — 0 findings at this head, 1 E7 against develop's guard.


