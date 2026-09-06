## BLUF
**Your core-only route is RULED — build it. Kam has given a standing direction tonight that bears on
your whole queue, and you are at a context checkpoint. Three things, in order.**

## 1. KS-914 — the shape
**RULED: the core-only pinned-`lookup` route. Do not add `undici`.** Your reason is the deciding one
and it is the reason I would have given: `packages/shared` is copied wholesale into all 24 runtime
images, and KS-920 — filed by you twenty minutes earlier — exists because that tree is already
267 MB. A dependency added to close KS-914 would enlarge the exact tree KS-921's sibling wants
slimmed. The extra code at the two send sites is the right side of that trade.

**What this ruling covers and what it does not.** RATIFIED: the trade-off (no new dependency in a
tree 24 images copy) and the honesty of the header rewrite you propose — a shape, decided in this
mail. NOT ratified, because its truth-maker is in the codebase and not in your mail: that
`net.connect`'s `lookup` + `http.Agent#createConnection` actually closes the rebind on the two send
sites. That is the gate's question. Your red-proof is the instrument: **a cell that goes RED against
the unfixed guard and green after.** If it will not go red, say so and do not claim the fix works —
you wrote that line on KS-921 yourself and it binds here.

Two things to carry into the READY:
- The two REGISTRATION-time call sites (`m365 :1102`, `originate :170`) are correctly out of scope.
  Say so in the READY explicitly, with the reason (they validate, they do not open a socket), so the
  gate does not read the omission as a miss.
- Your header rewrite says what is now closed and what is not. Keep it narrower than "rebind-proof":
  the connection goes to the checked address. The current header's honesty is the asset.

## 2. KAM'S STANDING DIRECTION TONIGHT (verbatim, panel, 20:19)
> "keep pushing the secuura agent to polish the platform to a ready state."

That is the frame for your queue from here: after KS-914, pick by what moves Platform K toward a
state Kam would call ready — defects that a user or Peter would meet, guards that are convention
only, and the residues your own gates have filed — priority then id, by path, with the by-path
confirmation before each cut, exactly as you have been doing. It does not change any boundary: the
signature classes stand, the QA gate stands, nothing deploys beyond his 15:12 lift, and his card
(`secuura-demo-kam-admin-default-password`) is still open with default HOLD, so the two runtime
seeders, the smoke script, the fixture, the docs and the demo env stay untouched.

## 3. CHECKPOINT — you are at ~59% (my watcher, 20:2x)
Rhythm §2 applies now: **finish KS-914 to its boundary and start nothing that will not fit.** When
KS-914 reaches READY, wrap — handover, history, secrets sweep, wrap mail — and I launch your
successor on it. Do not begin a new ticket after the READY.

## Standing, from my seat
develop `b77b20bf622804247b64e504d95a773460e0ca32` (your #851 merge, verified from objects here:
parents `34fc749df` + `330a444d3`, tree `628604996`). **#867 (KS-913 seed-list) is HELD and its gate
is mine** — untouched by you, as you have it. A second seat (s140d) is booting now to push the #863
merge that was made locally and never pushed when its pane closed; it works only in
`worktrees/seat-b` and will not touch `2_Project_Files`, the demo VM or the shared local stack.

-- Wednesday
