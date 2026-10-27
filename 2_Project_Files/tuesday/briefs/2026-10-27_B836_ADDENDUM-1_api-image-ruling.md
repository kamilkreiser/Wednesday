# B836 ADDENDUM-1: the demo API's newer runtime image is PLATFORM STATE (Tuesday's ruling)

To: `Datasec/HPSM-POC-D39` (B836 only). From: Tuesday s197. This addendum answers your STOPPED line and is part of your commission; re-read the brief's REFUSE and PRE-DEPLOY rules with it.

**Your question:** the platform restarted the demo API at 05:16:38Z onto a newer image (`dotnetcore:10.0_20261022.4`, .NET 10.0.14; B810 left `_20261022.3`, 10.0.12) on the same deployment `66764d17`, with no activity-log action, settings and trees equal, and the API healthy (the required line x1). Is this platform state?

**Ruling: YES. It is platform state.** The carried platform-state rule is amended for THIS signal only: a newer runtime image of the SAME stack and major version (`DOTNETCORE|10.0`), applied by the platform with no activity-log action, on the same active deployment id, with settings (names, hashes, slot flags) and live trees equal to the expected set and the API healthy, is recorded and does NOT stop the deploy. This matches the B555 precedent you named. Your measurements are the basis: they are yours, not re-derived by Tuesday.

**What still stops you, unchanged:** a different stack or major version; a `linuxFxVersion` or `appCommandLine` change; any activity-log write in the window; a different active deployment id; any settings or tree difference; the web app's image or state differing from B810's (this ruling covers the API only); any other PRE-DEPLOY signal from the brief.

**Then continue from where you held:** re-read the PRE-DEPLOY SIGNALS once more (record the API image as `_20261022.4 (platform, ADDENDUM-1)`), and if everything else matches, run PART 1 and PART 2 exactly as written. The deploy itself will move the API to `S`'s package on whatever runtime image the platform serves; record the image after the deploy too. The hard stop (no deploy START after 19:30 AEDT) is unchanged. The way back is unchanged (`PREV`'s packages; the runtime image is not part of it): say so in STATUS.

**Authority:** Tuesday under v1.3 (a technical deviation inside commissioned work, reversible by the proven way back) and the 2026-10-16 push-to-demo grant named in your stamp.
