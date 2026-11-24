Answer to item 6 on KS-772: what a rotated connector key carries. Read from K's code at develop `9c1ecde5abd6` (24 Nov). No live key on any host was read.

**A rotate copies nothing from the old key.** `register-connector` with `rotate: true` mints a brand-new key. Unless the request body sends its own `scopes` list, the new key gets the gateway's fixed connector set of nine scopes, and `subjects:erase` is one of them. It is minted at 3,000 requests an hour, with a one-hour window. That limit belongs to the key and is set fresh at every mint; a host can override the number by configuration. So a rotated key carries `subjects:erase` and 3,000 an hour.

**What that means for the dev-ps re-key:**
- Send the rotate with NO `scopes` field, so the new key gets the full set.
- The rotate reply echoes the scopes that were requested, not what was stored. To see what the new key holds, read it back through validate or the key list.
- A key minted before KS-869 (6 Sep) has no connector id, so the rotate does not switch it off. It stays live, with whatever it was minted with, until it is revoked by its id. By commit date, a 20 to 21 Aug key was minted without `subjects:erase` and at the older 1,000-an-hour default; we have not read the live rows.
- The reply says `rotated: false` with a `PRIOR_KEY_STILL_ACTIVE` warning only when none of the organisation's older keys carry a connector id. If one older key has an id and another does not, the reply can say `rotated: true` with no warning while the id-less key is still live. So after each rotate, check the key list for older active keys and revoke them by id.

**The erase gate today:** the scope check on the erasure route is still in its grace mode, so a connector key without `subjects:erase` is admitted and logged rather than refused. The plan is to switch enforcement on once S is using a rotated key.
