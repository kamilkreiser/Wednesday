B1258 ADDENDUM-1 (answer to your STOPPED: NEEDS TUESDAY on the 136 px page height) -- from Tuesday s241

**Answer: NO rollback. UAT stays at a8497578 (web + API).** Do NOT run `rollback1258uat.sh`. Whether 136 px is covered is the product owner's to say, not yours or Tuesday's: Tuesday puts your measured figure on his board as a card now. His options will be keep, or roll UAT back to 69338b64. The default is keep: the site is healthy, content stays reachable, and a rollback would undo every change he asked to deploy. If he rules rollback, Tuesday commissions it separately; it is not yours in this session.

**Why not covered as is:** his ruling "Accept both and land" accepted "64 px sooner", which the gate measured against the round-3 draft. Your measurement against yesterday's live site (69338b64) is 136 px in 22 of 56 cells. He was never shown that figure, so it goes to him.

**What to do now:** finish the brief's remaining wrap sections (FOR TUESDAY, NOT TESTED, UNMEASURED, processes, trees left) if any are unfinished, recording this addendum by name under Corrections. Then end the FILE with exactly one final line beginning `DEPLOYED: UAT @ a8497578` (web + API, healthy). The rest of that line says the page-height check is NOT PASSED (136 px against yesterday's site in 22 of 56 cells; 64 px accepted against round 3), that no rollback was made, and that the decision is with the product owner. Keep your candidate tickets in FOR TUESDAY item 6 as they stand: (a) the 136 px; (b) the menu's last control half cut at the page's end.

Stop any process of yours that is still running (by pid, never by name) and say so. Everything else in the brief is unchanged.
