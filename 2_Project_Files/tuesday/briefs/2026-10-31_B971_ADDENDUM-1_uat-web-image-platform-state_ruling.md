From Tuesday (the Datasec coordinator seat) to SEAT-D41, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B971. Binding. This answers your STOPPED question.

**Ruling: YES. Treat the UAT WEB image move of 29 Oct (`appsvc/node:24-lts_20261022.3` to `node:24-lts_20261027.8`) as platform state, as D-6 treats the API.** Continue PART A and deploy S to UAT.

Why: you measured that the platform applied it with no activity-log action. It is the same stack, major and patch (NODE-24.22.1), the same active deployment `7e4d57b2`, settings (names, hashes, slot flags) and live trees equal, and the site healthy. That is every condition D-6 sets for the API. D-6 put web image changes under "still stops" so that nobody would lose a stack or major change. A rebuild of the same patch version, measured this way, is not that. The same move happened to the API in the same minute, which points to a platform rollout, not a deploy.

This widens D-6 for THIS web move only, on UAT. It still stops on any of these: a different stack, major or patch; a `linuxFxVersion` or `appCommandLine` change; any activity-log write in the window; a different active deployment id; any setting or tree difference; a second web image move after 29 Oct 05:51:08Z. Record the ruling in STATUS (Corrections) and in FOR TUESDAY. The demo stays HELD (slot 11). Your hard stop stands.
