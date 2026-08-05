---
date: 2026-08-05
type: lesson
source: "Self-caught during WED-70 verification: Chrome refused ALL loopback (fresh test listener included) while curl succeeded; the extension's list_connected_browsers said isLocal:true for what fingerprinting proved was a DIFFERENT Mac (8 cores/1470×956 vs this laptop's 12/3024×1964)"
status: live
supersedes: ""
---

# The Chrome extension's "isLocal" is a heuristic — fingerprint before trusting it

**The catch:** a dashboard page verified fine from the shell but "refused to
connect" in the automated Chrome. An hour of port-theories later, the real
cause: the extension was driving Chrome on ANOTHER of Kam's Macs. The
extension reported `isLocal: true` for it. localhost is machine-relative —
every loopback check through that browser was silently testing the wrong
machine.

**The rule:**
1. Before using browser automation for anything machine-relative (localhost
   services, file downloads, machine-specific auth), fingerprint the browser:
   `navigator.hardwareConcurrency` + `screen.width×height` vs local
   `sysctl -n hw.ncpu` / display res. Mismatch → wrong machine → stop and ask
   Kam to connect the right Chrome ("try now" cost him one click).
2. This is [[2026-08-05_identities-float-verify-always]] extended to
   BROWSERS: which machine's Chrome the extension drives is another floating
   pointer. Kam runs several Macs with the extension; connection order is
   not a fact about the present.
3. Diagnostic shape worth keeping: shell-curl OK + browser-refused on
   loopback ≈ "the browser is not where you think it is" — check that before
   port/firewall/proxy theories (which all pattern-matched and were all
   wrong).

**Related:** [[2026-08-05_identities-float-verify-always]],
[[2026-08-03_mental-model-not-source-of-truth]]
