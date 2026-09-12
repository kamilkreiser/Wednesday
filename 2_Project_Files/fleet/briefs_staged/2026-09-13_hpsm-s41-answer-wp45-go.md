# WP4 + WP5 gate: GO WITH FINDINGS both — W45-m1 to lane A (and an API test in lane C), W45-p1 fix, W45-p2 stands; NO push until the WP3 round-2 verdict

**BLUF.** **For session 41 (seat hpsm-982d).** The tier-1 gate on `1a6b68d` returned **WP4: GO WITH FINDINGS (0/0/1/0) · WP5: GO WITH FINDINGS (0/0/0/2)** (verdict 23:43:37Z, spf/dkim/dmarc pass; report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-1a6b68d-wp4-wp5-tier1/report.md`, 138 lines; verdict and ids confirmed by Tuesday). **The gate planted a real cross-tenant leak and both isolation suites caught it:** the first Composer WP whose tests are proven able to fail at round 1.

## Rulings
1. **W45-m1 (Minor):** 11 realistic credential shapes pass the API's free-text scan and are stored verbatim in engagement notes. This is the API reach of the known **W3-m3**.
   - **Lane A:** its `credentialShapes` fix must cover every one of the gate's 11 shapes.
   - **Lane C:** add an API-level test proving each is refused at the notes and free-text endpoints, RED at `1a6b68d`.
   - Both land in lane A's WP3 round-2 series, and your READY names W45-m1 closed.
2. **W45-p1 (Polish):** the duplicate Not-Found cards. Fix in lane C; it is cheap.
3. **W45-p2 (Polish):** "HP Security Manager" in body copy. **Stays.** Naming the target product descriptively is not an HP mark. Q-03 is about logos and branding.
4. **No push yet.** `1a6b68d` also carries the WP3 round-2 engine changes, whose gate (`%23`) is still running. **Tuesday gives the push word only after that verdict**, then says the exact shape.
5. **The live Azure demo** (S40's, `hpsm-dev-rg`) runs `1a6b68d`. **Do not update it.** That is S40's documented action, on Kam's word.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 09:45

Tuesday
