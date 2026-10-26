From Tuesday, Datasec / HPSM-POC, to seat Datasec/HPSM-POC-H38 (brief B759). ADDENDUM-3. **It WITHDRAWS ADDENDUM-1 and ADDENDUM-2 for this branch.** Your original brief stands exactly as stamped (D-1: no HP guideline applied; no colour, font or token change).

**Why:** the product owner ruled at 21:44 on the live board: "No guidelines tonight: logo and polish only for the demo". The brand-colour change in ADDENDUM-1 comes from HP's design guidelines, so it is out of tonight's change. ADDENDUM-2 existed only because of ADDENDUM-1, so it goes too.

**What you do:**
1. **If you have NOT yet edited `web/src/styles/brand.css` or `api/src/HpsmPoc.Modules.Reporting/Pdf/BrandTokens.cs`:** do not edit them. Carry on with the logo work as in your brief.
2. **If you HAVE edited either file** (committed or not): first save the colour change as a patch for a later round, `git -C '<wt-b759-fix>' diff <base> -- web/src/styles/brand.css api/src/HpsmPoc.Modules.Reporting/Pdf/BrandTokens.cs <any brand-colour test you added> > '<evidence folder>/brand-colours-deferred.patch'` (print its sha256 and line count; it is evidence, never committed). Then restore each of those files byte-equal to the base by `cp` from the base blob (`git show <base>:<path> > <path>`), never `checkout`/`reset`. If a commit already carries them, make ONE follow-up commit that restores them (never amend, rebase or force-push), and say so in STATUS.
3. **Prove it:** `git diff --name-only <base>..HEAD` lists neither file and no `api/` path at all (control: a planted path is flagged); `brand.css` and `BrandTokens.cs` blobs at HEAD equal the base's; the property check of THE WORK 10 is back to web-only, the original closed list.
4. Remove any colour-specific READY fields (pdf tokens, brand table); the READY line is the original one. Mutants m10/m11 are not run.
5. Record this addendum under Corrections (one line).

Clock unchanged (target READY 23:30, hard stop 01:30; the 23:00 clock rule stands). This is not a stop. Carry on.
