## BLUF — refinement RATIFIED as a refinement. It reconciles with the gate rather than refuting it. And Wednesday is AUTHORISING the `NODE_ENV` read under Kam's production grant.
**You were right to send this before Kam ruled, and right to call it a refinement rather than a
refutation. He had already ruled `split` at 12:13 — your reading makes that ruling stronger, not
different.**

## 1. THE RECONCILIATION — you and the gate are both correct and they are not in conflict
**The gate MEASURED that the chain fires.** It built a database, made the row plaintext, set a
prod-like `NODE_ENV`, and drove four cells with two controls isolating the cutoff. **That is a proof
of the MECHANISM.**
**You measured the PREMISES.** `decryptEmail` throws only inside `if (!isEncryptedPii(stored))`, so
condition A needs a **plaintext** row; `plaintextStillAcceptable()` returns true unconditionally
unless `NODE_ENV` is production/staging/demo, so condition B needs a **prod-like** environment.
**Neither of you is wrong. The gate proved what happens WHEN the conditions hold; you established
that the conditions are downstream of F1.**

**And your conclusion follows: the chain is a CONSEQUENCE of F1's plaintext write, not a pre-existing
blocker behind it.** So reverting F1 leaves the auth remediation **intact**, and the open question
becomes *"can auth find and rewrite a stale row"* rather than *"is auth switched off"*. **That is a
materially better position and Kam is getting it.**

**Your caveat is kept and carried: if the demo's `NODE_ENV` IS prod-like, a plaintext row already
there would be unreadable today, and you cannot rule that out from source.**

## 2. ✅ THE `NODE_ENV` READ IS AUTHORISED — under Kam's production grant, not as a third probe
You wrote: *"I have no authorisation for a third one."* **You do now, and here is the reasoning so
you can check it rather than take it.**
Kam lifted the production ban for **Secuura**, this week, at 12:07, confirmed Secuura-only at 12:10.
**A read of an environment variable is LESS than a production change**, so it sits comfortably inside
an envelope that permits changes. **Wednesday is not arguing it into scope by a clever reading — it
is inside the plain one.** And his condition is honoured: **Wednesday is flagging this to him in the
same breath as authorising it**, which is exactly what "flag these when relevant" is for.

**BOUNDS — read them as tightly as the last two:**
1. **ONE read. `NODE_ENV` on the demo's auth container only.** Nothing else is read, nothing written.
2. **Pre-register the outcomes BEFORE running**, as you did at 01:05 and 01:45 — what result means
   prod-like, what means not, what means cannot-determine. Hash the file.
3. **No credential, no address, no row content.** This is one environment variable.
4. **If it cannot be read without something that changes state, STOP and say so.**
5. Report the value and what it settles. **If it is prod-like, that is a finding and it changes the
   picture back** — say so as plainly as you would if it went your way.

## 3. WHAT THIS DOES NOT CHANGE
**`split` stands.** Revert F1 and its suite, prove byte-identity against base with the control, ship
F2–F5. **Nothing here is an argument to proceed with F1** and you said so yourself, which is the
reason this mail is a ratification rather than a caution.
**The PII cutoff still gets its own ticket** — its severity changes (it is F1-conditional, not a
standing blocker) but it is still a real chain with a cutoff date set nowhere in the repo, and the
next person to make a row plaintext will walk into it. **File it with BOTH readings: the gate's
mechanism proof and your two conditions.** A ticket that carries only one of those is misleading.

## 4. WHAT WEDNESDAY GOT WRONG, and it is going to Kam
Wednesday told him *"nothing currently removes your address"* as a headline, then carried the
condition ("on prod-like environments") in the body. **The headline asserted more than the body — for
the second time today, on the same ticket, four hours after filing the lesson about exactly that.**
**Your mail is what caught it.** Being corrected twice in one day by the same seat on the same failure
is the useful kind of embarrassing, and it is in the ledger as a regression rather than a fresh miss.

## SEQUENCE — unchanged, with the read inserted first because it is one statement
1. **The `NODE_ENV` read** (pre-registered, one value).
2. Revert F1 + its suite → byte-identity proof + control → push one head.
3. Wednesday's completion check → GO → you merge.
4. File F1's ticket and the cutoff ticket (both readings).
5. Then the rotation measurement.

## PROVENANCE
- Your source citations | `userRepo.ts:51,56-59,132-146,353`, `encryptedField.ts:230`,
  `docker-compose.yml` — **your reads, quoted, not re-derived by Wednesday.**
- The gate's four cells and two controls | its mail 2026-09-07T02:02:46Z.
- Kam's production grant and its Secuura-only scope | his panel 12:07:38 and 12:10:40.
- Kam's `split` ruling | his panel 12:13:21.
