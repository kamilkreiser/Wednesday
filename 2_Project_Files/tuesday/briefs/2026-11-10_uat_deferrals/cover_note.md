Subject: Playbook v2.1 UAT pack: cases that cannot pass on the hosted UAT site

Hi Paul,

BLUF: HP will test the hosted UAT site, but the pack was written against the v2.1 HTML prototype, so 185 of its cases cannot pass on the site today. They are listed in the attached register, each with a reason and a proposed disposition, for HP to sign or to tell us which it needs built.

- Of the 285 functional cases, 174 cannot pass as written (126 describe a feature the site does not have, 48 are only partly met), and so can 11 of the 12 end-to-end journeys. The 102 functional P0/P1 cases among those matter most, because the pack's pass rule is 100% of P0/P1.
- About 80 of them test a sales layer: opportunity pipeline, quote builder, contracts, sales reporting and revenue attribution. We propose these are deferred to phase 2, each with its ticket. Five cases (JSON import/export, hash routes, a white/blue toggle) are proposed as out of scope for the POC.
- 37 cases are marked "passes with a stated difference", for example data kept on the server rather than in the browser, and the Customer view being a switch rather than a separate role.
- The pack treats the 32 production gates as all unbuilt, but the site already partly covers some: Microsoft Entra sign-in, server-side role rules, consultant approval gates for the narrative and report, and admin export and erase of personal data. We can evidence these against the gate wording if useful.
- The 38 non-functional cases (viewport, accessibility, consistency) are not in the register; we have not yet run them on the site.

What we ask of HP: for each listed case, sign the deferral (signatory, date, signature columns are in the register) or tell us it must be built for UAT. The pack requires a signed record per deferred case, so we have left those columns blank.

Kam
