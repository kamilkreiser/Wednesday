## BLUF — KAM RULED `split` at 12:13. Revert F1 only, ship F2–F5, F1 comes back as its own round. Here is exactly how, and how you prove it.
**Destination: `origin`, branch `develop`, Secuura Blockchain repo, via #885 once the revert is proved.**
**Do NOT merge until Wednesday's GO.**

## 1. THE REVERT — and the ONE proof that settles whether it needs a new gate
**Wednesday's standing rule is "what merges must be what was gated", and it applies here.** The gate
verified `6dbe63cae` **with** F1 in it. A reverted head is not that head.

**But the reverted head is the gated head MINUS the thing the gate objected to**, and that is
provable in one command rather than argued:

```
git diff <base> <reverted-head> -- Blockchain/Dev/services/api-gateway/src/startup-migrations.ts
```
**If that is EMPTY — the file byte-identical to base — then F1 is fully gone and what remains is
exactly F2–F5, which the gate verified individually.** On that proof, **no new gate**, and Wednesday
does a tier-2 through-code completion check instead. **If it is NOT empty, the revert is a change and
it gets a gate.** State the result either way; do not tell Wednesday it is clean, show it.

**Also prove the inverse, so "empty" cannot mean "I diffed the wrong thing":** a control diff on a
file you DID change (say the F2 docs or the F4 guard) must be NON-empty in the same command shape.

## 2. THE F1 REGRESSION SUITE MUST GO WITH IT — this is the part that gets missed
`scripts/__tests__/ks949_main_seed_idempotence.test.sh` asserts the FIXED behaviour. **With F1
reverted it asserts something the code no longer does and will fail** — and a red suite on develop is
worse than no suite. **Take it out with F1** and let it return in F1's own round, where it belongs
and where it is genuinely good work. **Say explicitly which files the revert removes**, and re-run
leg 12 (tracked shell suites reached) so the count moving 15 → 14 is a measured, expected change and
not a surprise later.

## 3. WHAT SHIPS, and it is worth naming because it is real security work
**F2** — three files no longer publish a password beside the identity.
**F3** — the second published super-admin: no default in either seed path, fails closed, and
`run-platform.sh` no longer re-asserts a published password on every run.
**F4** — the drift guard enumerates seed sites from the tree, with the control first.
**F5** — both sites default-DENY.
**These four were held hostage by a fifth that was wrong. Kam's ruling frees them, and that is the
whole point of his cap.**

## 4. TWO TICKETS TO FILE — and the second is the one that actually decides Kam's exposure
**(a) F1's own ticket.** The shape is already ratified — **the migration REMOVES its INSERT** and
keeps the PK conflict target used only to re-sync `tenant_id`/`tenant_slug` on rows that already
exist. Carry the evidence: auth creates all twelve identically; on a stack where the migration has
thrown every boot since encryption landed, all twelve exist ciphertext with hashes set. **And the new
cell must drive BOTH seeders against ONE real database in BOTH orders, on the docker/init shape, and
must NOT stub `isEncryptedPii`** — that stub is what blinded the old suite.

**(b) 🔴 THE PII CUTOFF — P1, its own ticket, and it outranks (a) in consequence.** The gate measured
that the auth remediation is **disabled on prod-like environments**: `decryptEmail` throws once
`plaintextStillAcceptable()` is false (`NODE_ENV` production/staging/demo **and** past
`PII_PLAINTEXT_CUTOFF` = 2026-06-01, **set nowhere in the repo**, so the source default applies);
`getUserById` catches and returns **null**; the remediation reads that as *"no pre-existing row to
remediate"* and skips. `services.bicep:564` defaults to `staging`, `env.demo.json:8` says
`production`. **Four cells, two controls isolating the cutoff rather than the row shape.**
**Why it outranks F1: this is the mechanism that decides whether Kam's address ever comes off any
seeded box.** F1 fixed and deployed with this in place would still not remediate. **File it with the
gate's cells quoted. Do not fix it yet** — Kam has not ruled it and it is not in #885's scope.

## 5. SEQUENCE
1. Revert F1 + its suite → **prove byte-identity against base, with the control** → push one head.
2. **Wednesday's completion check** → GO → **you merge**, tree oid predicted before and matched after,
   containment controls both ways, pinned with `sha=`, as you did on #882 and #876.
3. File (a) and (b).
4. **Then the rotation measurement** — the 183-file credential, Kam ruled `rotate-properly`. Measure
   first, propose the shape to Wednesday before writing it.

## 6. THE PRODUCTION GRANT DOES NOT CHANGE ANY OF THIS
Secuura-only, this week, flag every use. **It does not authorise deploying the reverted head** — that
is a separate decision and Wednesday will take it to Kam once F2–F5 are on develop, because after the
revert **nothing in this PR remediates his row**, and he should not be left thinking a deploy does
something it does not.

## HOLDS
Nothing merges without Wednesday's GO. **No deploy.** No human contacted. No history rewrite. No
`rm` — the suite comes out by `git rm` in the revert commit, which is version control, not deletion.
No plaintext or hash in any artefact.

## PROVENANCE
- Kam's ruling | panel 2026-09-07 12:13:21, card `secuura-ks949-round3-cap-and-the-cutoff` => `split`.
- The NO GO, the cutoff chain, the 12-row blast radius, `services.bicep:564`, `env.demo.json:8` | the
  gate's mail 2026-09-07T02:02:46Z, quoted, not re-derived by Wednesday.
- #885 head `6dbe63cae`, develop `61df129e9` | Wednesday's `ls-remote`; **re-read both yourself before
  you push.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **12:13:21 `split`** — lands in: the revert commit, the two new tickets, and #885's PR body.
- **12:07 + 12:10 production ban lifted, SECUURA ONLY, flag every use** — lands in your standing holds.
