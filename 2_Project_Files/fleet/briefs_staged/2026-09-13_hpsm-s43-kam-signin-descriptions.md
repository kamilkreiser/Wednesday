BLUF. **New instruction from Kam, first-party, verbatim below.** Each tile on the Composer sign-in page gets a clear description of what that sign-in option means, in much smaller grey text at the bottom of the tile.
- **This is LATE by about 12 minutes, and the fault is Tuesday's.** Kam typed it into Tuesday's terminal at 19:01:39 AEST (09:01:39Z). Tuesday's seat rotated at 19:04 and the line was never passed on. The successor seat found it at 19:1x by reading the previous seat's transcript.
- Your current lanes do not change. Fit this into your partition. No new plan confirmation is needed unless it collides with a lane.

## Kam's words (Tuesday's terminal, 19:01:39 AEST, verbatim)
> "In the HPSM sign-in page, each of the sign-in options needs a much better description of what the options mean. Make this description in gray with a much smaller text at the bottom. Of each tile."

## What the page is today
Read by Tuesday from `apps/web/src/screens/SignIn.tsx` in the main checkout (last touched by 99519a1). Not re-derived on your lanes.
- Each option is a `pc-choice-card` tile, one per synthetic user from idp-mock. A tile shows the user's name in bold and one `pc-hint` line: the role labels (`ROLE_LABELS`) and `preferred_username`.
- Nothing on the tile says what signing in as that user lets you do. That is the gap Kam means.

## The ask
1. **One description per tile**, saying what the option is for: what a user with those roles can do in the Composer, in plain words.
   - Source it from the product's own role model (authz and the role labels). Never invent a capability.
   - If a role's capabilities are unclear from the code, say so in your READY instead of guessing.
2. **Styling:** grey text, much smaller than the current text, at the bottom of each tile. Use existing style tokens. No new colours outside the style guide.
3. **Unchanged:** synthetic users only; no HP marks (Q-03); the product name comes from `brand.ts`.
4. **Partition.** As Tuesday reads your 08:41 plan, `SignIn.tsx` is in no fix lane's paths. But the tile styling lives in `app.css`, and **FX-S7 is the SOLE owner of `app.css` and `e2e/support`.**
   - Either put this inside FX-S7's lane, or run it after FX-S7 merges. One agent per path.
   - Name your choice and an ETA in your next STATUS.
   - If Tuesday has misread the lane paths, say so.
5. **Proof and route:**
   - A render test that every tile shows its description.
   - It ships in a rolling upgrade, with a head mail first.
   - It goes into the delta tier-1 gate. It is a rendered surface, so the gate needs its browser leg.
