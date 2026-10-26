# B741 ADDENDUM-1 - Tuesday's answer to your STOPPED question (follow-up page words)

From Tuesday s182 (the Datasec coordinator seat), Datasec / HPSM-POC. This file answers the question in the last line of `1_Project_Definition/Briefs/2026-10-26_B741_STATUS.md` (STOPPED 14:58:09). It changes ONE thing in your stamped kit and nothing else.

## Answer: OPTION A
For v0.3, take ONLY the header (the logo rectangle) from the release candidate, and keep everything else as v0.2 for EVERY figure, including 16.1 and 16.2. The guide's words stay unchanged, including section 16's quote of "Your session has ended. Open the link again."

**This supersedes the kit's class RESHOOT for Figures 16.1 and 16.2 only** (kit line 35 and step 3c). They become class RECT: the v0.2 raw with only the header rectangle replaced by your 3a rectangle, exactly like the other header figures. Figure 2.1 stays a re-shot only if its visible text is byte-equal to v0.2's (your step 3c diff). If it is not equal, treat 2.1 the same way (RECT) and say so in STATUS. Figure 15.1 is unchanged (your own dimmed capture). T9 (the 16.1 and 16.2 alt text) stays as stamped: the header in those figures will show the logo.

## Why
The product owner asked for the logo added and the guide recreated, as a priority, for sending to HP. A new user-facing sentence in the guide is his word to approve, and it is not part of that ask. Mixing two builds' bodies in one guide would make it inconsistent.

## What the covering note and CHANGES_v0.3.md must say (one short paragraph, plain words)
- v0.3 changes the header to the logo. Every screen body is still the v0.2 build's.
- Since v0.2, the release candidate changed other screens: the signed-out follow-up page's sentence (it now reads "Open the link your partner sent you. If it has stopped working, ask your partner for a new one."), the Home page title ("Partner Dashboard" is now "Home"), and about 21 web files in all (your FOUND 1-2, with the count your own diff printed).
- Bringing every figure and quote up to the current release is a separate refresh (v0.4), for the product owner to decide. Nothing in v0.3 claims to show the current release's bodies.

Put the same paragraph in STATUS under FOR TUESDAY. Then continue from where you stopped, and end on your kit's normal final line.
