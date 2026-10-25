From Tuesday (the product owner's Datasec coordinator seat), Datasec / NexusAI. ADDENDUM-1 to B713 (SEAT-M14), written by Tuesday s178 on 2026-10-26 at 09:19 AEDT, answering your STOPPED: NEEDS TUESDAY line of 09:18:45.

RULING (Tuesday's technical ruling; no product owner word is needed for a test-harness classifier): YES to the wider class, but ONLY going forward and ONLY with a per-failure proof. Not a retro-count.

1. B-base-02 run 1 (the QA-F2 'notice counts' cell, `notice` undefined at A.test.js:280) stays UNCLASSIFIED. It is reported in your FINDINGS exactly as you wrote it and counted for NEITHER arm. Your p6 probe makes the mechanism likely; the red run itself carries no port or owner, so it cannot be put in the class after the fact.

2. Before resuming the campaign, add ONE instrument to the BASE and CHANGED scratch arms: on any failing cell, before the stand closes, record the stand's port and the output of `lsof -nP -iTCP:<port> -sTCP:LISTEN` (pid and command of every listener). A failing cell counts in the FOREIGN-LISTENER class, in EITHER shape (a fetch error such as `other side closed` / ECONNRESET, or a zero-requests-reached cell such as the notice being undefined), ONLY when a pid other than the stand's own process holds that port at that moment. Any red cell without that proof is a STOP to Tuesday, as before.

3. Prove the instrument before counting with it (it must be able to fail both ways): (a) positive control: one run of the BASE scratch arm with p6's planted ANSWERING squatter on the stand's port must count 1 in-class failure with the squatter's pid captured; (b) one clean run must count 0. Write both rows into your STATUS. If either arm misbehaves, STOP to Tuesday.

4. Then resume the interleaved campaign at pair 2 (BASE first). The A/B predicate is UNCHANGED: BASE fails at least once in-class in the same campaign and CHANGED fails zero times; without that there is no 'fixed' claim. The 20-minute cap per jest-lock ticket and your hard stop are unchanged.

5. If the predicate cannot be met before your hard stop, end as PARTIAL exactly as your brief says: nothing pushed, the 127.0.0.1 change left as `session-tools/b713/change.diff`, the evidence in this file. Tuesday then hands it to a NexusAI records seat as evidence plus a ticket.

Name nothing outside your own lane and ports (9800-9809 only for probes). Append the ruling as one line under DESIGN or Corrections in your STATUS, then continue; your last line keeps the brief's final-line formats.
