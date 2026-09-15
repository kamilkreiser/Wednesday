# READY — KS-1045 PART A (`deployment/KINTSUGI-DEV-SERVER-PLAN.md`: the lapsed credit-expiry paragraph at :50 and the Stage-B hold row at :173 corrected to the ticket's 2026-09-09 read-only measurements — the VM exists) — Ornith ornith:35b (Q4_K_M) FIRST SAMPLE (`2026-09-15_ks1045-ornith35b-night`; the run's D6 FAIL was a harness false negative on a miscounted hunk header, IMPROVEMENTS row 92; RE-CHECKED PASS 7/7 under the fixed D6) — at develop M55 `48e65c435`
# Source read by Wednesday 23:17: both `+` lines are the brief's byte-for-byte (each ONE physical line); D4/D5 prove the six tokens; D7 both must-remove lines gone. Part B (the status line at :3, which sits BEFORE the first `## ` heading) is a separate task — the checker's section rule needs a preamble arm first. The facts are the TICKET's measurements (s160, 2026-09-09); Wednesday re-measured nothing on Azure (no identity).
# PR NOTES for the raising seat: (1) re-measure the VM (`az vm list` under the Secuura identity, read-only) before merging — the facts are six days old at the time of the brief; (2) Part B (line 3) is the same PR; (3) KS-1044 (the 53-hour outage) is cited in the row — link it; (4) docs PR, tier through-code.

```diff
--- a/Blockchain/Dev/deployment/KINTSUGI-DEV-SERVER-PLAN.md
+++ b/Blockchain/Dev/deployment/KINTSUGI-DEV-SERVER-PLAN.md
@@ -47,7 +47,7 @@ Pricing the non-burstable equivalent changed the answer: `Standard_D2ps_v6` is t
 
 ### 🔴 Before committing to any of these
 
-Project records show the **Founders Hub credit expires 6 September 2026** — about three weeks out. Whichever option is chosen, the standing cost is what matters, not the credited cost. **This should be confirmed against the current subscription before the spend decision**, not taken from these notes. The subscription's consumption API returned no usage data to this credential, so I could not measure current burn to put alongside these figures.
+Project records said the **Founders Hub credit would expire 6 September 2026**; that date has passed and the subscription still reads `state: Enabled` (measured read-only 2026-09-09, KS-1045) — the warning is stale, not live. Whichever option is chosen, the standing cost is what matters, not the credited cost. The subscription's consumption API returned no usage data to this credential, so current burn could not be measured alongside these figures.
 
 ---
 
@@ -170,7 +170,7 @@ A Let's Encrypt certificate `CN=kintsugi.secuura.net` was issued
 | Stage | Contents | Status |
 | -- | -- | -- |
 | **A** | sizing + costs, provisioning script, wallet procedure, promotion gate, DNS/TLS plan | ✅ **complete — this document. No spend, nothing created.** |
-| **B** | run the provisioning above | ⏸ **HOLDS for Kam's explicit go on recurring spend.** KS-601's own recorded gate is *"once Stuart confirms verification displays properly"* — **that confirmation is still not on record** (his last word on KS-584 predates the fix, which has been live on demo since 2026-08-11). Lifting that gate should be a deliberate call, not drift. |
+| **B** | run the provisioning above | ✅ **DONE — the VM exists:** `secuura02-kintsugi-vm` in `SECUURA-DEMO-RG`, `Standard_D2ps_v6` (the size recommended above), `20.198.226.148`, `southeastasia`, running (measured read-only 2026-09-09, KS-1045). It has since run, failed and been recovered from a 53-hour outage (KS-1044). Stuart's confirmation on KS-601's own gate is still not on record — that gate is a separate question from the VM's existence. |
 | **C** | boot the stack, verify matrix, generate + fund the wallet, deploy KS-584's P3 work into Kintsugi, flip demo's role in docs and on the board | ⏸ after B |
```
