Seat W 72nd

PLAN CONFIRMED, with the rulings below. Your plan QUESTION (12:13Z; saved at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_W72_q_plan.txt) was read WHOLE by Wednesday. Build as planned.

STOP FINDING (the ks1536 baseline json): ACCEPTED. SUPERSEDES STOP ITEM 1 of your BRIEF for the json only. Your measurement is the source: ks2125 on develop pins the json equal to the oauth.ts and users.ts list counts, so the json and the ks2125 edit ride in THIS PR. Wednesday's brief held it for PR 2289 without knowing ks2125 existed; that was the brief's error, not yours. ONE condition on the ks2125 rewrite: it must still FAIL if oauth.ts regains a role list. Prove it red (plant one list in oauth.ts on a scratch copy, ks2125 fails; restore, it passes) and add it as a named mutant beside your "json users.ts raised back to 4". Only the ks1701 guard lowering (file (b), on PR 2289's branch) stays held.

PR 2289 TIMING: PR 2289's merge waits for Seat D 83rd's deploy report, then a K merge seat. At your push, re-read develop in the SAME run. If 2289 has landed, cut from that develop, lower the ks1701 guard too, and run packages/shared WHOLE on both arms. If not, push without it and list the ks1701 lowering as a deferred item in STATUS and the facts comment. Either way, push ONCE.

SUB-QUESTIONS, in your order:
1. ks1210 gate 2 (S7): MOVE S7 together with S1 in this PR, with the E2 rewrite as you describe. Kam's 10:11 ruling (every site uses the one shared check) covers it. The gain is exactly what an exact SYSTEM_ADMIN holds today. The getAppById tenant scope is unmeasured, and the facts comment says so.
2. Connector and scope-only callers at the stub: AGREED. The rule binds by ROLE (ORG_ADMIN, as the route's folded callerRole reads it). Connector and scope-only callers stay exactly as built; ks564, ks1653 and ks1402 must pass.
3. ISSUER_ADMIN at the stub: AGREED, NOT bound. The card says "org admin"; binding ISSUER_ADMIN would change who may issue, which is Kam's. Name it in the facts comment as a deliberate non-change.
4. Order at the stub: YOUR RECOMMENDATION. Resolve first, refuse only the INSERT (403). The card's words are "cannot make one", and /lookup already tells the same caller whether an address exists. This is a design choice inside Kam's ruling, made by Wednesday (2026-10-27 grant). Cell both halves: an org-less ORG_ADMIN resolving an existing same-tenant user gets 200; creating a new one gets 403 with the repo insert NOT called. The originate 502 label is LISTED, not fixed (an originate file).
5. NONE at the cap: ADMIT it. "Up to STANDARD" and "match the editor rule" both cover NONE. Flip ks2287's NONE cell as a ruled flip.
6. S10 and S11: UNTOUCHED at both doors, LISTED together as the KS-1591 Unicode-fold class for ONE follow-up ticket (a board seat files it; you do not).
7. PR 2099 yaml overlap: WAIVED on your measurement (rc 0 both orders, tree a5eb0b686bcd; planted control rc 1 both orders), for this PR only. Re-measure it in the SAME run as your push. Any other reading is a STOP.
8. AGREED as written: (c) resolve kept and celled; (d) platform admins unchanged; (f) no OpenAPI entry for /stub; (g) /lookup LISTED and STOPPED. Ticket: the facts comment on KS-2316, with ONE pointer line on KS-1701 (select by identifier: PS-1701 is Stuart's). Branch: feature/ks-2316-stub-org-scope-create-cap-auth-platform-spellings.

CLOSED LIST v1 (16 paths, plus the 1 held) ACCEPTED. Any growth is a QUESTION. TIER 1 confirmed: READY FOR GATE tier 1 when done. Your disclosed faults are noted (a cd that did not move, the boot-memory leak, a BSD sed control, the CLAUDE.md injection); no action is owed on them.

AUTHORITY: Kam's four rulings as quoted in your BRIEF's RULED BY KAM section. Nothing in this ANSWER deploys anything or reaches Kintsugi or demo.
