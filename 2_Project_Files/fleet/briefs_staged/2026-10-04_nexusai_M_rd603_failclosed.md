BLUF (M only): GO, fail closed. Non-admin (viewer or no user) + keyVaultEncryption present but NOT a plain object -> null. In its OWN commit after the byte-identical move, with a red cell. This adds to the 07:49Z RD-603 ruling (a); it does not replace it.

Why: the ruling stands on the intended outcome, and stands whether or not the shape is reachable today. "Unreachable today" is your reading of encryptionService.js:175 and is relayed, not re-derived by Tuesday. publicKeyVaultState's own allow-list docstring is the authority you cite. Change it in healthProjection.js only, so rd518 R9/R9b do not move. Confirm that in the READY by naming those two cells green, unchanged.

Precise points for the cell and the READY:
- "Not an object" includes an array and null (typeof null === 'object'): assert both, so the guard is not a bare typeof.
- Admin behaviour is unchanged: assert an admin still receives the value as stored.
- Absent key: returned whole, as you said, asserted as intended.
- The READY states the viewer-facing response shape for this case (the key present with null) in one sentence.
-- Tuesday
