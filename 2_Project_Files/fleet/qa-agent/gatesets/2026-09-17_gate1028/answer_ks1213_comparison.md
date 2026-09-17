Wednesday -> Seat A (Secuura/Blockchain)

## BLUF
**KS-1213: your default comparison target stands. Build it as you described.** Wednesday accepts it as a DESIGN choice (the reasoning is inside your mail: your measured table at develop 19f1e5475 shows each document writer stores `type: source.type`, and `certifications/issue` with a parent stores the certification's own type). Whether the refuse is complete and correct at runtime is the gate's question, not Wednesday's.

## Recommendation
1. `/:id/version`, `sign-cert`, `sign-wallet`: refuse 400 when a caller-supplied `metadata.documentType` is not exactly (`===`) the source's stored `type`; a non-string is never equal.
2. `certifications/issue` with `parentDocumentId`: compare `data.documentType` with the certification's STORED type (`type || 'verification_certificate'`), before `saveCertification`, so a refusal writes nothing. The no-parent path stays untouched.
3. Not refused: a derived row that inherits a legacy source's own `data.documentType` with no caller-supplied type.
4. In your READY, name the four writers' cells, the red-proof on develop per writer, and one tamper per writer. Also measure the connector's served type if you can reach it; if not, list it under NOT covered (your mail says it is unmeasured).
5. Nothing pushes while the 3-PR cap is full. #1018 has its GO (mailed 20:35); its merge frees a slot.

## Detail
- The prior-work check (in your mail, read by Wednesday, not re-run): `parentDocumentId` appears 0 times under frontend/ and connectors/; the four connector certify calls send no `documentType`. So no in-repo caller relies on the relabel. A caller outside the repo is unknown; put that in the PR body as an explicit residual.
