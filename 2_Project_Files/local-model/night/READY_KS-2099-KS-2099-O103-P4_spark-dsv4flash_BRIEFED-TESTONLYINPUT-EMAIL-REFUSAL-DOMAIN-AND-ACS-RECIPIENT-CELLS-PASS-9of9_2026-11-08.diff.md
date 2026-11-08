# READY - KS-2099-KS-2099-O103-P4 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2099_o103_p4_email_log_domain_and_acs_recipient/out.md.checker/patch.diff` (from `ls` at 23:30 2026-11-08; sha256[:16] 0b1002eaf3aeb037, 1471 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 23:30 2026-11-08 by Spark operator 103 after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-08_ks_2099_o103_p4_email_log_domain_and_acs_recipient/out.md.checker`; product bytes were RE-MEASURED here.** Tip `765701307eb3ffb9cf98f380ffea3a51d8c70b74`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/services/originate/src/__tests__/ks1937-email-service-logs-never-carry-the-recipient-address.test.ts']; `+` lines 14 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/services/originate/src/services/email.ts` blob 78eed82ffe66; plant file(s) also unchanged.
- Red cells [input.json]:
  - `E8 the allow-list refusal line carries no part of the recipient address`
  - `E9 ACS accepts the send: the address still reaches the ACS call`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/originate/src/__tests__/ks1937-email-service-logs-never-carry-the-recipient-address.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 10 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 2563 -> 2565, red 11 -> 11`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/services/originate/src/services/email.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1937-email-service-logs-never-carry-the-recipient-address.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1937-email-service-logs-never-carry-the-recipient-address.test.ts
@@ -139,4 +139,18 @@
     expect(lines('[Email/SMTP] Failed to send')[0]).toContain('ks1937 smtp boom'); // the error text is still forwarded (named under NOT covered above)
     expect(leaks()).toEqual([]);
   });
+
+  it('E8 the allow-list refusal line carries no part of the recipient address either: not even its domain', async () => {
+    const email = loadEmail({ ...SMTP_ENV, EMAIL_RECIPIENT_ALLOWLIST: 'someone.else@example.test' });
+    await expect(email.sendEmail({ to: 'ks2099.person@ks2099-domain.invalid', subject: 'ks2099 subject', text: 'ks2099 body' })).resolves.toBe(false);
+    expect(lines('refusing to send')).toHaveLength(1);
+    expect(mockLogged.filter((l) => l.toLowerCase().includes('ks2099-domain'))).toEqual([]);
+  });
+
+  it('E9 ACS accepts the send: the address still reaches the ACS call as the one recipient (only the LOG changed)', async () => {
+    mockBeginSend.mockResolvedValue({ pollUntilDone: async () => ({ status: 'Succeeded', id: 'acs-msg-2099' }) });
+    await expect(send(loadEmail(ACS_ENV))).resolves.toBe(true);
+    expect(mockBeginSend).toHaveBeenCalledTimes(1);
+    expect(mockBeginSend.mock.calls[0][0].recipients).toEqual({ to: [{ address: ADDRESS }] });
+  });
 });
```
