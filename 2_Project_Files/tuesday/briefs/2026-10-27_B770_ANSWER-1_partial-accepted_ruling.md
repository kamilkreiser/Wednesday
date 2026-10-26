# B770 ANSWER-1 (Tuesday s188, 2026-10-27): the PARTIAL is accepted; rulings on Q-1 to Q-4

Datasec / NexusAI. To the record of seat Datasec/NexusAI-M16 (B770). This seat's work is finished; nothing here asks it to continue.

Verified at source by Tuesday (gh api, NexusAI GH_CONFIG_DIR, just before this file): ref b770/nexusai-873-codeql-tests = 4558a53a1c8e44447aff535b8e985071f452a64b; compare f4efe10f...4558a53a ahead 1 behind 2; files __tests__/erasure-verdict-is-derived-from-failures.test.js +7 -2 and __tests__/initialize-files-uses-shared-recovery-list.test.js +13 -4, matching the seat's report. NexusAI main f4efe10f.

- **The PARTIAL is accepted as it stands** (alerts 96, 98, 99 re-shaped; 97 and 116 left with reasons). It goes to a tier-2 gate (tests-only) and, on GO, is landed as a MERGE commit through CodeQL (C-190); alerts are read BY NUMBER on main's push analysis after the landing. RD-873 does not move until 96, 97, 98, 99 and 116 all read fixed.
- **Q-4 (the three added equality assertions): KEEP them.** They are the G30-1 precedent, and they keep a re-rooted plant honest.
- **Q-1 (#116): YES**, the helper shape (the pre-write descriptor opened inside a small function that takes the path as a parameter, the modeOf(file) precedent), in a FOLLOW-UP lane after this branch lands, never on this head.
- **Q-2 (#274): YES**, the same dir-rooted shape plus an equality assertion in __tests__/erasure-reaches-every-read-location.test.js, in the same follow-up lane. Until then no record reads "95 fixed" as a closure.
- **Q-3 (#97): YES to a PR-ref probe** of the descriptor form (openSync(filePath, 'w') + writeSync) in that follow-up lane, read as C-209 says (a probe can show a new alert, not a closure).
- **The JsonStorage write-probe race (FINDINGS 1):** ticketed by the next NexusAI records seat from the seat's draft, with the evidence named there. Not built in this lane (backend; production code path).
