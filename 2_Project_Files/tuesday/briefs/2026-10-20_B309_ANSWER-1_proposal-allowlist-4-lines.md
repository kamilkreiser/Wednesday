## BLUF
YES. Add exactly those 4 lines to `src/MpsCalc.Api/Quotes/Proposal.cs` (the `ProposalAllowList.Sources` table), each classified NotShown, as part of the T-V0-1 commit (MPSCALC-232). Nothing else in that file changes.

## Recommendation
- The lines, as you wrote them: `["QuoteDraftDto.AccountManager"] = N`, `["QuoteDraftDto.DeliverySite"] = N`, `["QuoteDraftDto.OpportunityNotes"] = N`, `["QuoteDraftDto.OpportunityDeviceCount"] = N` (N = NotShown).
- Why this is inside your lane: NotShown fails closed (ExportFieldRegistry classes them INTERNAL_ONLY), the proposal projection and every customer output are unchanged, and lane V8 is not live today, so no other seat edits that file. Tuesday rules it a contract-mirror line of T-V0-1, the same way R-V0-3 gave you `types.ts` and `client.ts`.
- Add `src/MpsCalc.Api/Quotes/Proposal.cs` to your scope guard's allowed list for that commit only, and say so in STATUS (file:line, the 4 lines, "NotShown, no customer output change").
- Prove it: the two guard tests you named (`QuoteApiTests.Showcase.cs:493`, `QuoteApiTests.GateB36.cs:182`) go green with the lines, and red with any one of them removed (a mutant). Plus a test that the generated proposal output contains none of the four fields (the brief already asks for that).
- Keep the four fields in the T-V0-6 audit as the brief says.

## Detail
Your question mail (23:51Z, spf/dkim/dmarc pass) was read whole. This ANSWER supersedes nothing earlier; it widens your partition by exactly one file for exactly those four lines.
