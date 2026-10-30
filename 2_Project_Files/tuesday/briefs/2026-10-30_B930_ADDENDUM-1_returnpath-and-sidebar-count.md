From Tuesday (the Datasec coordinator seat) to SEAT-H61, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B930. Binding. Answers your STOPPED question in `Briefs/2026-10-30_B930_STATUS.md` (its last line).

**Answer: YES to both. Continue from your RESUME section.**

1. **`web/src/server/auth/returnPath.ts`:** add the ONE segment `"training"` to `RETURN_SEGMENTS`, in the list's existing sorted place, nothing else in the file. It is forced by `server/auth/returnPath.test.ts` (the allowed first segments must equal the `app/(app)/*` folders) once your `/training` route exists. Put it in C2 (the Training commit), since that is the commit that adds the folder.
2. **`web/src/components/shell/AppShell.sidebar.test.tsx` line 219:** change the pinned link count from 8 to 9 (the Training entry is a new link in the aside), the number only, plus its comment if it names the count. You already own lines 60 and 74 of this file; this is one more named line. It goes in C2 too, since that is where the Training entry is flipped to built.

**Conditions (each printed in STATUS with a control that can fail):** (a) the `git diff -U0` hunk of each of the two files is exactly that one line (control: a planted second change is reported); (b) `returnPath.test.ts` and `AppShell.sidebar.test.tsx` both red BEFORE the edit on the C2 tree and green after (red-first); (c) Corrections lists both files as additions to YOUR PATHS made by this addendum.

**Coordination you need not act on (FOR TUESDAY only):** seat H68 (kit B937, the customer security preview) also adds a segment (`"security"`) to `RETURN_SEGMENTS` and lowers the `nav-dead-ends.test.ts` floor, both after you land; its kit pins the aside link count at 8 and will be told it is 9 after your landing. Do not touch either of its lines.

Nothing else in B930 changes: the ruled Q-2 module list (the product owner ruled option a at 10:57), the CONTENT RULE, the plants, the hard stop.
