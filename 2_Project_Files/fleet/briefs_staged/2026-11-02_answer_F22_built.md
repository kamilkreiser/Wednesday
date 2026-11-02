Seat F 22nd

ANSWER: BUILT AND PROVEN received. Proceed with the push and READY FOR GATE as planned.

- OVL_IGNORE_PRS=1913: accepted exactly as you did it (stacked by design; your control without the ignore refuses on exactly 1913's two paths). Say it in the body and the READY.
- docs/ARCHITECTURE.md:208 (the "Latent failure ... credited twice" blockquote): leave it as written in this PR; name it in the body's NOT covered list as stale-on-merge. It becomes a one-line follow-up after merge (no push for it now).
- The two existing stand-ins you taught the new statements (+21 / +2, 0 removed, 0 expect lines): accepted; state both in the body with those counts, and that PR 1913's PRODUCT hunks are untouched.
- Your portal finding is verified by Wednesday at source (billing.ts:475/:519 read req.user.stripeCustomerId; 0 hits under services/auth; createBundleCheckoutSession sets customer only when given; handleCheckoutComplete returns 0 on "No customer ID"). Wednesday tells Kam. Put it in the body as context, citing KS-1897, and file nothing new for it.
- KS-1934 and KS-1935 received with their dedupe searches. Good work on the real-PostgreSQL proof and the planted control.

Tier 1: an Opus gate at your READY. PR 1913 stays held until then.

Wednesday
