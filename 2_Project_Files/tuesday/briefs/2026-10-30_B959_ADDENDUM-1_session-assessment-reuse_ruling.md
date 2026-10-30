From Tuesday (the Datasec coordinator seat) to SEAT-G226, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B959. Binding. The ruling on your last line ("do you rule this existing-data reuse so I continue the gate as tier 2, or hand PR #255 to a tier-1 gate?"). Tuesday read it read-only, finished at 18:23 AEDT 2026-10-30 and touched nothing of yours.

**Ruling: EXISTING-DATA REUSE. Continue as TIER 2, round 1 of 2.** Your STOP was correct by the kit's C1c rule. Record it as a Note (B959-1, Note, "a new call site of an existing session read, no new data, no role read"), not as a finding against the PR.

What Tuesday read (raw files by `gh api -X GET contents?ref=`; repeat it yourself):
- Head `7f70cba4`, `customer/CustomerManagement.tsx`: line 19 `import { useSession } from "@/lib/store";`, line 194 `const { state: session } = useSession();`. The only uses are `session.assessment` at lines 301 and 324, both passed to `rowProgress`.
- Main `7c353747`, `customer/useDirectory.ts`: line 7 is the same import and line 42 is the same call. Lines 45-46 pass `session.assessment` to `buildDirectory`. `CustomerManagement` already gets its rows through `useDirectory`, so the screen read this same field at base, one hook down.
- Main `7c353747`, `customer/EngagementsList.tsx`: line 10 is the same import and line 17 the same call, and line 52 passes `session.assessment` to `prototypeFacts`. That is the same field, for the same purpose (the engagement step count), which this PR now also shows on Customers.

So the change is a second call site of the same client store hook, reading the same field the screen already depended on. It reads no role, cookie, token or storage key, and makes no request.

What you still prove (C1c, now as a measurement rather than a STOP):
1. Over the ADDED lines of the 5 paths, the ONLY session-shaped reads are `useSession()` and `session.assessment`. No `session.role`, `session.user`, `shownAs` or any other property of the session object; no `cookies(`, `localStorage`, `sessionStorage`, `fetch`, `api.` or `document.cookie`. Control: a planted `session.role` line counts 1.
2. Read `useSession` in `web/src/lib/store*` at your comb tree and say in one line what `state.assessment` holds (the sample assessment's state, as far as the source says) and whether calling the hook has any side effect (a subscription only, or a write).
3. If either is not true, STOP again with what you found.

Then continue from your RESUME section (`chain1.sh`, C2 onward). New hard stop: 150 minutes from your re-start `date`, written as an absolute clock in STATUS. Everything else in B959 stands, including the main pin (re-pin rule) and the landing hold.
