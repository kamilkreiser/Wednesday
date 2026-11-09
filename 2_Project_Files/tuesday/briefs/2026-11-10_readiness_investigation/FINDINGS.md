# Readiness on UAT: findings (investigator's report, saved by Tuesday because the agent's own write was refused), 2026-11-10 09:1x

**Diagnosis: (e), a mix, mostly (a).** It is built and live, but My readiness (`/assessments`) leads with the newest COMPLETED run, drawn with its own (old-deck) questions. Partly (c): the H1 was kept as "My readiness" (B1380 decision 2), against Kam's 11-09 20:19 words "change title to Playbook Partner Readiness". Not (b) and not (d).

- **Live bundle (unauthenticated GET):** `/_next/static/chunks/32mvoeoixokr_.js` 200, `cmp`-equal to the deployed file, holding 16 of 16 statements, 4 of 4 areas and "Playbook Partner Readiness" x2. The build ID `bytHj28aj21cVQmgGGcmh` equals the deployed BUILD_ID; served `no-store`. `/assessments` answers 307 to sign-in, so the investigator stopped there.
- **At main 0820efe9:**
  - statements: `web/src/content/packages/playbook-placeholder.v0.7.0.json:3775-4060`;
  - areas: `:3743/:3750/:3757/:3764`;
  - title: on the runner H1 `ReadinessRunner.tsx:140`, the result page `ReadinessResult.tsx:46` and the hub card H2 `AssessmentsHub.tsx:100`;
  - the hub H1 and tab are still "My readiness" (`AssessmentsHub.tsx:95`, `app/(app)/assessments/page.tsx:4`);
  - the lead panel is `AssessmentsHub.tsx:61-68, :83`.
- **B1391 had already recorded it:** "the 16 new statements are NOT SHOWN ON UAT; they are what a NEW self-assessment opens" (screenshot `after-uat-readiness-hub-1440x900.png`). That sentence never reached Kam before he looked. **LESSON CANDIDATE:** a deploy seat's 'not shown' line is read into the message to Kam, not left in STATUS.
- **No meeting-notes file exists.** The source is Kam's board message plus the 11-09 Layout v2.1 attachment, `kam_attachments_1109/f-84472617d43a_...:732` (statements), `:791` (areas), `:805` (H1 "Partner capability & readiness"), `:828` (sidebar "My readiness").
- **Fix in progress:** B1392 ADDENDUM-3 (the hub leads with the current set when the last run is older; H1 and tab "Playbook Partner Readiness"; sidebar unchanged), on the same branch as the ADDENDUM-2 caveat reword, then deployed by D58.
