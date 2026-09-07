## BLUF — Kam has authorised the DEPLOY and told us to FIX THE VISIBLE DATA. F3 is upgraded from file-only to FIX. The deploy happens AFTER round 2 passes its gate, not now.
**Kam, panel 2026-09-07 11:09:06, verbatim:** *"Go ahead with the deploy, and you've got permission
to deploy for the rest of the week. Also, fix the issues with the visible data."*

**Destination when it deploys: the Secuura demo environment** (Founders Hub subscription
`a0ee7d32-2e4a-47a0-9a49-9c001817a545`, tenant `efc17e5f-7637-4118-b92c-c5236d591cad`). Code lands on
`origin`/`develop` first, gated, as always.

## WEDNESDAY'S READING OF BOTH SENTENCES — stated so Kam can correct it in seconds
**1. "Go ahead with the deploy" = deploy AFTER round 2 passes its gate. Not now.**
**Reasoning, and it is mechanical rather than cautious: deploying the CURRENT head would fix
nothing.** F1 is precisely why the row is never rewritten — the twelve-row batch aborts on
`users_pkey` and the seeder skips. **Deploy today's code and the demo re-runs the same aborting seed
and the row stays exactly as it is.** The deploy only remediates once F1 is fixed. If Kam meant
"deploy immediately", that is his to say and Wednesday will relay it — but it would be a deploy that
achieves nothing, so this is the reading being executed.

**2. "Fix the issues with the visible data" = F2 AND F3, both FIXED this round, not filed.**
This **supersedes** Wednesday's earlier instruction that F3 was file-only. The earlier instruction
was written before Kam had said this.

## F3 IS NOW IN SCOPE — the second published super-admin
`docker/init-platform/01-platform-schema.sql:136-150` and
`deployment/azure/migrate/run-platform.sh:120-124`: a `platform_admins` row, role `super_admin`, with
its **bcrypt hash committed and its PLAINTEXT in a comment on the line above it.**

**Fix requirements:**
1. **No published default.** The credential comes from an environment variable, and the seed
   **fails closed** when it is unset — the same shape the auth path already uses. **A default that
   ships in the repo is the defect; do not replace it with a different default.**
2. **Remove the plaintext comment AND the committed hash.** Do not reproduce either in a commit
   message, a ticket, a PR body or a test fixture.
3. **`run-platform.sh:124` is the sharp end:**
   `ON CONFLICT (email) DO UPDATE SET password_hash = EXCLUDED.password_hash` **re-asserts the
   published default on EVERY run, including on an already-seeded box.** It must not re-assert a
   default it does not have. **Note the irony and use it: that is exactly the remediating shape F1
   lacks, pointed the wrong way.**
4. **The status hardcode is part of the same defect:** `routes/auth.ts:381-383` builds a synthetic
   user with `role: 'SYSTEM_ADMIN'` and `status: 'ACTIVE'` **hardcoded**, so the `platform_admins`
   branch — checked FIRST, at `:344-346` — never consults a row status the way the users path does.
   **A suspended platform admin is not suspended.** Fix it or state precisely why it must stay.

## ⚠ WHAT REMAINS KAM'S, AND YOU MUST NOT DECIDE IT
**Any credential that is live on a deployed system and is being retired is a ROTATION, not a code
change.** If removing the published default means an existing deployment can no longer authenticate,
**that is a consequence for Kam to accept, not for us to spring on him.** State it in your READY mail
as a numbered consequence — which environments authenticate with that credential today, measured, not
assumed — and Wednesday puts it to him before any deploy. **Do not change a credential on a running
system.**

**And the history:** the plaintext and hash are in prior commits. Redacting the working tree does not
remove them. **MEASURE what remains reachable and report it. Do NOT rewrite history and do not
propose it** — that is irreversible and it is Kam's alone.

## THE DEPLOY GRANT — recorded, and it carries an expiry
*"you've got permission to deploy for the rest of the week."* **Wednesday reads that as through
Sunday 2026-09-13**, stated to Kam as a reading he can correct. Under protocol v1.3 deploys to dev /
staging / test / demo were already Wednesday's; **what this adds is the demo deploy in this specific
remediation**, and it does **not** touch production, money, external communication to any human, or
anything irreversible. **A deploy that makes an external commitment is still Kam's.**

## SEQUENCE — unchanged except F3 moves in
1. **F1** — remediate-then-skip on the main-DB path, keyed on `id`; the catch must stop reporting a
   constraint violation at debug level as "skipped". **Regression cell: run the statement TWICE
   against one database**, the second time with a pre-existing `(…060, old-address)` row.
2. **F2** — the three files still publishing a password beside the identity.
3. **F3** — as above. **Its consequence list is required, not optional.**
4. **F4** — the drift guard enumerates seed sites from the tree (all four), not a hand-written list.
5. **F5** — revert `ALLOW_DEFAULT_SEED_PASSWORDS` to default-DENY.
6. **READY FOR QA** → Wednesday commissions the re-gate. **Round 2 of 2 under Kam's cap.**
7. **Then Wednesday's GO, then the deploy**, and only then is the row on the demo actually rewritten.
8. Your displaced queue returns: KS-645/KS-952, then the CI wiring. KS-597 is already pushed
   (`af640e809`).

## ON THE PROBE — Wednesday is not asking for the second one
You identified a one-statement domain check that would close the inference gap and correctly did not
run it. **Kam has now made it moot for decision purposes** — he has ruled the deploy, so the row gets
rewritten either way. **Do not run it.** If he asks, it is one statement and it is still available.

**Your probe is on the scoreboard at 1.0**, and the reason is the method: outcomes hashed before the
run, the address never selected by construction, the control carried, measured separated from
inferred **unprompted and against your own interest**, and a bound respected when a safe extra step
was right there. Wednesday made the measured-vs-inferred error itself this morning; you did not.

## HOLDS (unchanged except where Kam has now ruled)
Nothing merges without the re-gate and Wednesday's GO. **No human is contacted.** No `rm`, no
`--no-verify`, no force push. **No history rewrite.** **No credential changed on a running system.**
Do not reproduce any plaintext or hash in any artefact.

## PROVENANCE
- **Kam's deploy grant and the visible-data instruction** | his panel 2026-09-07 11:09:06, verbatim
  above | read by Wednesday in this action.
- **Kam's 11:01:35 `round2-plus-probe` ruling** | card `secuura-ks949-round2-and-the-second-admin`.
- Every F1–F5 measurement | the tester's mail `[QA -> Wednesday] Secuura KS-949 round 1 (#885, tier 1)`
  2026-09-07T00:57Z | quoted, not re-derived.
- The probe figures | **your** mail 01:06:50Z | quoted.
- develop `61df129e9` | Wednesday's `ls-remote`, 11:0x AEST.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **11:09:06 — deploy authorised + a standing deploy grant for the rest of the week; fix the visible
  data.** Lands in: this round's PR (F2/F3), the deploy receipt, and Wednesday's grant record.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-05 23:24 — do NOT narrate KS-823 in a published contract.
- 2026-09-07 — the base-column criterion is retired; new branch first; what merges must be what was
  gated; a merge GO authorises the base-ref check and any needed retarget.
- 2026-09-07 — KS-597's fallback is not written; the 95k backfill is `afterfix`.
- **2026-09-07 (this mail) — F3 is FIX, not file. This supersedes the file-only instruction in the
  11:02 mail.**
