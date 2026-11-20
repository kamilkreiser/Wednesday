From Tuesday (Datasec coordinator seat), Datasec / MPS Commercial Calculator. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Files naming another B-number are READABLE claims only. Marks: **MEASURED** = the drafter printed it with the instrument named (sidecar `.measured` beside this kit, one line per literal); **DERIVED** = source reading or arithmetic, not run; **RELAYED** = read in another seat's file or the ticket; **UNMEASURED** = nobody has. Drafted 2026-11-20 from 14:04 to 14:21 AEDT (clock reads by `date`: 14:04:23 account, 14:04:25 main, branch, pull requests and compare, 14:06:11 toolchain, the dry-run clocks in the sidecar, and the write clock in the sidecar) by a read-only drafter for Tuesday. Every `file:line` below was printed by `grep -n` or `awk NR==` over the raw files of branch head `fa71fc87218120192aa0c68c2c85936978b997d9` (a tarball of that sha from `gh api -X GET .../tarball/<sha>`, in the drafter's scratch folder; its blobs for `unpriced.test.tsx`, `ProposalDocument.tsx` and `OnePager.tsx` equal the three blobs the compare of main to the head printed); re-print each at your head. **What the drafter ran, and where:** a COPY of that tarball in its scratch folder (`.../fleet/state/s297/d1775/head`, its `node_modules` copied from the review's tree, which is a read of the review's files), Tuesday's node 24 by path, `TZ=UTC`, single-file `npx vitest` runs of the test file only (light; no lock; load1 between 2.4 and 3.3 at every `uptime` read), one `eslint` on that one file and one `tsc --noEmit -p tsconfig.test.json`. **No whole suite, no browser step, no build, nothing in the project's checkout or in any `.tools` tree.** Every RED/GREEN set below marked MEASURED is from those runs of the reference diff in section THE REFERENCE DIFF; the whole-suite totals are DERIVED.

# BRIEF B1775 | SEAT-M168: MPS CALCULATOR, BUILDER, ROUND 2 OF 2 OF THE PART CODES IN THE UNPRICED PURCHASE DOCUMENTS (MPSCALC-278 follow-up): CLOSE THE LEFT BOUNDARY OF THE NO-PRICE CHECK'S CODE STRIP, STATE ITS LIMITS TRUE, CORRECT THE ADDENDUM. ONE EXISTING TEST FILE CHANGES (`web/src/proposal/unpriced.test.tsx`), ONE EXISTING RECORDS FILE (the WORD-PACK ADDENDUM) GETS A DATED SECTION. A SECOND COMMIT ON THE SAME BRANCH, A FAST-FORWARD PUSH, NO PR. NOTHING DEPLOYED. THE TWO SOURCE FILES, THE EIGHT GOLDENS AND `pricedUnchanged.test.tsx` DO NOT CHANGE.

Code repo `datasecau/MPS-Commercial-Calculator` (the project's `2_Project_Files` is STALE and holds no `web/` folder: work in your OWN clone). **Branch** `b1767/mps-unpriced-part-codes-278`, currently ONE commit `fa71fc87218120192aa0c68c2c85936978b997d9` ahead of main `565ba142d4d07b183099eee42c1b73f94242489b` (Stamp S2 and S3); you add ONE commit on top of it (no amend, no force, no rebase). Lane size S to M (the function and its cells; FACT 8). **Port block: Tuesday's slot S7 names it; the only listener you start is the web server of a browser run, on the second port of the block.** Project root: `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator`. The project's `.tools` folder holds the first round's `.tools/b1767`: never read it, never write it, never copy from it; yours is `.tools/b1775`. The first round's STATUS and ADDENDUM are records files in `1_Project_Definition/Briefs/`: you READ the STATUS and you edit only the ADDENDUM, as section THE ADDENDUM says.

**You do NOT** merge to `main`, deploy, open or comment on a PR, write Jira, touch the root records (`BACKLOG.md`, `JIRA.md`, history, `CLARIFICATIONS.md`), message a human, push any ref but `b1767/mps-unpriced-part-codes-278` (a plain FAST-FORWARD push only), force-push, amend, reset, rebase, or write outside your STATUS, the ADDENDUM, the Step-0 copy, `.tools/b1775/**`, `/private/tmp/b1775-seat-tmp`, your own clone and (only under the context band) the HANDOVER file. **The records of this round (the Jira comment, the CLARIFICATIONS entry, the follow-up tickets named below) are NOT this lane's: Tuesday has them done by a records seat; you write none and you do not draft them.** **No `az`**, docker, ssh. **No HTTP to any hosted host, not even a GET** (exceptions: `gh api -X GET`; git fetch/push to `git@github.com:datasecau/MPS-Commercial-Calculator.git`; the npm registry for `npm ci` ONLY after the machine cache was tried first with `--prefer-offline`, said in STATUS; the app under test is the loopback web server of your own browser run). Jira: read only. Never delete (quarantine to `.tools/b1775/_quarantine/`). Never type `cd` (`env -C '<dir>' <command>` runs a command in a folder). **Never read `.local/`, `Source_Documents/**`, any price book or any real price store: every quote, proposal and value you use is SYNTHETIC (the repo's own fixtures `s4Proposal` and `fiveClassDealProposal` and values you invent, the ones in the reference diff included).** Add NO new dependency.

model: claude-sonnet-5-5 (`/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/models_latest.json:23`). Row: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/specs/model-routing.md:92` row C2 (a feature-shaped build that is not auth, credential or money DESIGN; here a test-file change). Gate after: separate kit, round 2 of 2 of the independent review (**Q5**). **Launch carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes** (`brief_seat.sh:31` reads `${BRIEF_SEAT_LEVEL:-opus}`).

## THE AUTHORITY (quoted, never paraphrased beyond it)
- **The product owner's ruling of 2026-11-20 on the three words**, as recorded at the heading `### C-186` of the root `1_Project_Definition/CLARIFICATIONS.md` (the ruling line of that entry, MEASURED by the drafter: it reads, word for word, "Option a, label, word for word: Add part codes so the third label is true. Its detail, word for word: The three words stay as written. A small follow-up lane prints the part code before each description in the unpriced documents, with its own review. The hosted site waits for it."). **Round 2 is still that follow-up and still inside that review; nothing wider.** The same entry says nothing wider is recorded.
- **Everything else in this kit is Tuesday's choice as coordinator, NOT the product owner's**, and your commit text, your STATUS and your ADDENDUM section write it that way or do not mention it. No text of yours may say the product owner decided, approved or ruled anything beyond the sentence above.
- The words rule that still binds (`1_Project_Definition/CLARIFICATIONS.md:660`): every new customer-facing word comes to the product owner as a word pack before it ships, and nothing is deployed without his card. Round 2 adds no word: it changes a test file.

## WHERE THIS ROUND STANDS (rounds are counted by what they count)
**NO GO 1 of 2 on class "the no-price check (oracle P) can be made blind", gate B1770 at head `fa71fc8` on main `565ba14`.** The verdict file is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1770_verify/VERDICT.md` (106 lines; first line `GATE B1770: NO GO @ fa71fc8 on main 565ba14`): ONE Major, four Minor, four Info; its `FOR-RECORDS.md` names what to fix. **This is round 2 of 2: a second NO GO on this class goes to the product owner**, so this kit makes the fix provable before the push (cells red first, plants, mutants, the closed list proved by a census). The gate found the PRODUCT change clean ("no figure reaches any unpriced render except what the server sent as a code, the priced documents are byte-identical, every CI step is green on node 24"); you do not touch it.

| Verdict row (VERDICT.md line) | What round 2 does about it |
|---|---|
| Major (line 10): `stripCodes` has no left boundary: an amount whose tail equals a line's code, printed in that line's code slot, reads clean (rendered proof: code `0.50`, unit price `1250.50`, optional-items site) | THE RULE below: a closed list of places a code can start; cells B1 to B5; plants P5 to P7; mutants M1 to M8 |
| Minor (line 11): the stated limits are narrower than the real ones ("equal" versus "whatever it holds"; rounded, re-grouped or abbreviated forms of a figure with cents are not read) | THE STATED LIMITS: the true sentences, frozen; the test file's comments, this round's commit body and the ADDENDUM carry them |
| Minor (line 12): a long unbroken code shrinks the whole printed PDF | NOT fixed (styles are outside the lane): the ADDENDUM states it; a follow-up ticket is the records pass's (FOR TUESDAY) |
| Minor (line 13): the ADDENDUM does not say a code that LOOKS like a price prints as typed | the ADDENDUM states it |
| Minor (line 14): "added source lines: 24" reads 26 (`+21` and `+5`) | the ADDENDUM's correction line; the first round's STATUS file stays untouched (a records pass corrects it) |
| Info (line 15): the one exception of the no-new-word cell U10 applies to both documents, only the short form needs it | IN: one small edit (THE EXCEPTION), proved by plant M13 of the review shape (exception emptied for the short form: red) |
| Info (lines 16 to 18) | none (the review said none) |

## PRIOR WORK: what round 1 built in the oracle, and why each part stays (all in `web/src/proposal/unpriced.test.tsx` at the head; MEASURED pointers by `awk NR==`)
| Part | Head line | Round 2 |
|---|---|---|
| `scanText`: the printed text, every text node on its own line, and the value of every attribute of every element (names not read) | `:110` | CHANGED: it also writes a start mark before each text node (two lines of the function) |
| `wholeDollarForms` and `hasToken`: whole-dollar forms read as whole tokens | `:124`, `:134` | stays; `hasToken` is the digit, dot and comma rule the review cited |
| `codedLines`: the (code, description or label) pairs of the proposal, trimmed | `:146` | stays |
| `stripCodes`: "<code> <description>" read as "<description>" before the scan | `:163` (lines 163 to 166 are the function the Major names) | CHANGED: it removes a pair only at a place a code can start |
| `figuresInText`, `figuresIn`: the scan, and the scan after the strip | `:169`, `:180` | `figuresIn` also removes the start marks before the scan |
| `leavesOf`, `U10_EXCEPTIONS`, `unexplainedLeaves`: the exact no-new-word check | `:185`, `:195`, `:201` | `unexplainedLeaves` takes the exception list as an optional fourth parameter (THE EXCEPTION) |
| the cells U1/U2, U3 to U10 per document, the page cells, the part-code cells and rows A to G of the position strip | `:226` to `:336`, `:392` onward | stay; ONE existing cell's expected value changes (the "SKU" line of the U10 function cell, `:457`, because a code after a word is no longer at a start); 11 cells are added |
| `pricedUnchanged.test.tsx` and the eight goldens | their own files | NOT touched (blobs equal at base and head: you prove it) |
**Why each stays:** the product change and the priced goldens are clean (the review); the attribute and token reading closed round 1's own follow-up; U10 exactness is what catches a code that prints a figure (the review: "U10 flags the leftover leaf").

## THE FAULT, by the review's own proof (relay; you reproduce it as a cell, not from the review's files)
`stripCodes` (head `:163` to `:166`) does `t.split(code + ' ' + description).join(description)` wherever the pair occurs. When a line's code is the tail of an amount (`0.50` of `1250.50`; `0` of `1234.50`; `0.00` of `57940.00`), a defect that prints the amount where the code goes reads `1250.50 Synthetic widget`; the strip eats the tail (`125Synthetic widget`) and `figuresIn` returns `[]`. The review's rendered proof: a mutant in the optional-items site (`partCoded(o.unitSellExTax ?? o.code, o.description)`), item code `0.50`, unit price `1250.50`, prints `1250.50` in the unpriced full proposal and oracle P reads `[]`; the control code `SYN-GATE-1` was found. U10 still flags the leftover leaf; attribute values are read by oracle P only, so there the old strip stayed blind.

## THE RULE (the property first, then the closed list, then the census that proves it)
**The property.** The strip removes a part code only where the documents really begin to print a line item's code, and anything before that place stays in the scanned text. **A closed list of places a code can START (at least these; any other shape: prove it meets the property or STOP):**
1. **the start of the text** (offset 0 of a string handed to the oracle: a leaf of U10, a small synthetic string of a control);
2. **the start of a text node** (the place `scanText` marks with U+0001 before each text node, built by code: `String.fromCharCode(1)`): a table cell or any leaf that holds a line item's `<code> <description>`;
3. **right after the quantity**: the exact 3 characters space, U+00D7, space, with a DIGIT before them (`<digit> x <code> <description>`, the multiplication sign built by code), the way the stream cards, the schedule's fleet detail and the short form's detail cell print a line.
**Everything else is not a start**: after a space, a letter, a bracket, a semicolon, a dot, a comma, a digit with no multiplication sign, a multiplication sign after a non-digit, two spaces before the sign, no space after it; and the START MARK is the only thing that makes list item 2 true, so an attribute line (written WITHOUT a mark) is never a start. A code-shaped text at any other place stays in the scanned text and is read as what it looks like.
**The census that proves the list is complete (MEASURED by the drafter on node 24, a throw-away cell in its scratch copy, quarantined there; you REPEAT it as a throw-away cell in your clone, never committed): for each of the four fixtures and each unpriced document, every occurrence of a coded pair inside a text node is classed.**
| Fixture | Full proposal: start of text node / after "<digit> x " | Short form: start of text node / after "<digit> x " |
|---|---|---|
| s4 draft | 12 / 18 (sum 30) | 2 / 6 (sum 8) |
| s4 approved | 12 / 18 (sum 30) | 2 / 6 (sum 8) |
| five classes with a deal pair | 1 / 10 (sum 11) | 0 / 5 (sum 5) |
| eight packages | 68 / 96 (sum 164) | 2 / 15 (sum 17) |
All 273 occurrences (99 and 174) are on the list; **0 are at any other place**; the sums equal the first round's code counts (30 and 8, 30 and 8, 11 and 5, 164 and 17). By site (s4 draft, full proposal): the stream cards 7 and the fleet detail cell 11 are after the quantity (18); the office table 8, the optional items 2 and the software table 2 are at the start of a text node (12). Short form: the detail cell 6 after the quantity; the software table 2 at the start of a text node. **If your census reads any occurrence at another place: STOP with the text and the site (it is a product shape the list does not hold).**
**The right side (answered, and proved).** A figure cannot hide by running on after the description: the strip replaces `<code> <description>` by `<description>`, so it removes the code and ONE space and nothing after the description. Only the characters of the code and that space can hide, and a figure holds no space, so a figure can be hidden only by overlapping the code from the LEFT (the Major) or by BEING the code (the stated limit). Cell B4 prints a figure glued to the end of the description, with and without a space, and reads it; mutant M6 (the strip also eats a following digit, dot or comma run) turns B4 red. **The product is not at fault on this side: `ProposalDocument.tsx` and `OnePager.tsx` are NOT edited in round 2** (if you find the right-boundary question proves a product fault: `STOPPED: NEEDS TUESDAY` with the text and the site).
**What the rule still cannot see (stated, tested, frozen in THE STATED LIMITS):** a code printed AT a start that equals, or contains, an amount reads as clean there (the test cell `limit, stated`); the same text anywhere else is read.

## THE CELLS (11 added to `unpriced.test.tsx`; the exact text is in THE REFERENCE DIFF; the titles below are the selectors)
All sit in ONE describe, `the left boundary of the position strip: a code can start only where a line item can start`, inside `the oracle can fail (controls over small synthetic documents)`, before `U10 as a function`. Selector `-t 'the left boundary of the position strip'` matches exactly these 11 (MEASURED: the Tests line reads `11 passed | 77 skipped (88)`).
| Cell | Asserts | RED at the first round's function? (MEASURED, cells only) |
|---|---|---|
| `the closed list of places a code can start holds exactly three` | `CODE_STARTS` names are `startOfText`, `startOfTextNode`, `afterQuantity` | RED (the list does not exist yet: the placeholder is empty) |
| `B1: an amount whose tail equals a line code ...` | for the tails (`0.50`/`1250.50`, `0`/`1234.50`, `0.00`/`57940.00`, `50`/`1250.50`): the strip leaves the text unchanged and the oracle finds the amount, as a string and as a document | RED |
| `B1: the same with the quantity prefix and with the grouped form` | `7 x 1250.50 <desc>` and `1,250.50 <desc>` (code `250.50`) are found | RED |
| `B1: a code that is a middle slice of an amount never matches in the slot ...` | middle slices (`940.0` of `57940.00`, `4521` of `14521.10`) never match, the amount is found | GREEN (a guard: the slot never matches a middle slice) |
| `B2: the three legitimate starts strip the code ...` | text start, mark start, after `7 x `, after `1,000 x `, and two lines of a joined cell all strip | GREEN (the first round's function strips everywhere) |
| `B2: a code at the start of a text node is a start even when the node before it ends in a digit` | the table-cell case: node `7` then node `4521.10 <desc>`: `visibleText` reads `74521.10 <desc>` and the oracle is clean | GREEN |
| `B3: anywhere else the code is not stripped ...` | nine texts (after a space, a letter, a bracket, a semicolon, a non-digit before the sign, no space before the sign, no space after it, two spaces, a mark then a space) are left alone and a code that equals an amount is found | RED |
| `B3: a code printed in an attribute value is read, never stripped ...` | an attribute holding `<code> <desc>` is read; an attribute holding `1250.50 <desc>` is found | RED |
| `B4 (the right side): a figure printed against the description ...` | the figure glued to or beside the description is read, the strip removes the code and one space only | GREEN |
| `limit, stated: a code printed in its own slot is read as data whatever it holds ...` | `PN57940.00X` and a code equal to the amount, at a start, read clean | GREEN |
| `B5: the unpriced documents print the tail codes in position and no figure` | the real documents, a fixture whose optional item has code `0.50` and price `1250.50` and whose software row has code `0.00` and amount `57940.00`: the codes print in position and the oracle reads `[]` | GREEN (a guard; it goes RED only under a plant: P5, P6, P7) |
**MEASURED: with the 11 cells over the first round's function the file reads `Tests  5 failed | 83 passed (88)`; the 5 RED are the closed-list cell, the two B1 cells and the two B3 cells; the other 6 are GREEN.** With the reference function: `Tests  88 passed (88)` (77 + 11).
**Existing cell changed (expected old answer rewritten, one):** `U10 as a function > a leaf that differs from a priced leaf by a part code in position ...` (head `:454` to `:458`): the middle line becomes `expect(unexplainedLeaves(['SKU SYN-ABC-1 Synthetic widget'], ['Synthetic widget'], coded)).toEqual(['SKU SYN-ABC-1 Synthetic widget']);` because a code after the word `SKU` is not at a start and stays (the leaf is unexplained either way: mutant mC7 of round 1 still goes red).

## THE EXCEPTION (the review's first Info row; IN because it is three changed lines)
`unexplainedLeaves` takes `exceptions: string[] = U10_EXCEPTIONS` as a fourth parameter and tests `exceptions.includes(t)`; the render cell passes `doc === SHORT ? U10_EXCEPTIONS : []`. The list constant, its length cell and the function cells stay. **MEASURED: with this edit the file is green (88); with the short form given an empty list, exactly one cell goes RED: `the short form > U10: no new word ...`** (the review's M13 shape). The full proposal needs no exception (its U10 is green with an empty list).

## THE REFERENCE DIFF (the drafter's dry run; MEASURED GREEN: 88 passed; `eslint` rc 0 on the file; `tsc --noEmit -p tsconfig.test.json` rc 0; 0 non-ASCII bytes)
The CELLS are the specification; the function may be written differently if every cell and every mutant below behaves as stated. Unified diff of `web/src/proposal/unpriced.test.tsx` from the head blob `e7584a6fb8278c626611d81651e9f17d3baa1ca1` (+158 and -9 lines in 8 hunks, counted by program over this block):
```diff
--- a/web/src/proposal/unpriced.test.tsx
+++ b/web/src/proposal/unpriced.test.tsx
@@ -113,10 +113,13 @@
   const values = [copy, ...copy.querySelectorAll('*')].flatMap((e) => [...e.attributes].map((a) => squash(a.value)));
   // Each text node on its own line as well: textContent runs the cells of a row together ("57,940" then the next cell's "7" reads
   // as "57,9407"), which would hide a whole-dollar figure from the token rule.
-  const nodes: string[] = [];
+  const texts: string[] = [];
   const walker = document.createTreeWalker(copy, NodeFilter.SHOW_TEXT);
-  for (let n = walker.nextNode(); n; n = walker.nextNode()) if (squash(n.textContent ?? '') !== '') nodes.push(squash(n.textContent ?? ''));
-  return `${visibleText(el)}\n${nodes.join('\n')}\n${values.join('\n')}`;
+  for (let n = walker.nextNode(); n; n = walker.nextNode()) texts.push(n.textContent ?? '');
+  const nodes = texts.map(squash).filter((t) => t !== '');
+  // UNIT marks where each text node starts: the position strip reads a code as starting there and in no other place of a line.
+  const visible = squash(texts.map((t) => UNIT + t).join(''));
+  return `${visible}\n${nodes.map((t) => UNIT + t).join('\n')}\n${values.join('\n')}`;
 }
 
 /** Whole-dollar forms of a figure whose fraction is all zeros: the digits and the digits grouped with commas (no dollar sign). */
@@ -130,6 +133,22 @@
 
 const isDigit = (c: string) => c >= '0' && c <= '9';
 
+/** U+0001, written before each text node in the scanned text: a code can start right after it. */
+const UNIT = String.fromCharCode(1);
+const TIMES = String.fromCharCode(0xd7);
+const QTY_SEP = ` ${TIMES} `;
+
+/**
+ * THE PLACES A PART CODE CAN START (a closed list; any other place is not a start, so a code-shaped text there stays in the text
+ * and is read as what it looks like). The documents print a code in exactly these places: a table cell or a leaf (the start of a
+ * text node), and after the quantity of a detail line ("7 x <code> <description>").
+ */
+const startOfText = (_t: string, i: number) => i === 0;
+const startOfTextNode = (t: string, i: number) => t.charAt(i - 1) === UNIT;
+const afterQuantity = (t: string, i: number) => i >= QTY_SEP.length + 1 && t.slice(i - QTY_SEP.length, i) === QTY_SEP && isDigit(t.charAt(i - QTY_SEP.length - 1));
+const CODE_STARTS: ((t: string, i: number) => boolean)[] = [startOfText, startOfTextNode, afterQuantity];
+
+
 /** True when `token` is in `text` as a whole figure: not after a digit, a dot or a comma; not before a digit, or a comma or a dot and a digit. */
 function hasToken(text: string, token: string): boolean {
   for (let i = text.indexOf(token); i !== -1; i = text.indexOf(token, i + 1)) {
@@ -162,9 +181,26 @@
  */
 function stripCodes(text: string, p: PurchaseProposal): string {
   const lines = codedLines(p).sort((a, b) => b.code.length + b.text.length - (a.code.length + a.text.length));
-  return lines.reduce((t, { code, text: description }) => t.split(`${code} ${description}`).join(description), text);
+  return lines.reduce((t, { code, text: description }) => replaceAtStarts(t, `${code} ${description}`, description), text);
 }
 
+/** The text with `target` replaced by `replacement` where it sits at a place a code can start; a match anywhere else stays in the text. */
+function replaceAtStarts(t: string, target: string, replacement: string): string {
+  let out = '';
+  let from = 0;
+  let i = t.indexOf(target);
+  while (i !== -1) {
+    if (CODE_STARTS.some((starts) => starts(t, i))) {
+      out += t.slice(from, i) + replacement;
+      from = i + target.length;
+      i = t.indexOf(target, from);
+    } else {
+      i = t.indexOf(target, i + 1);
+    }
+  }
+  return out + t.slice(from);
+}
+
 /** The figures of the proposal found in a text as it stands (no part code removed). */
 function figuresInText(text: string, p: PurchaseProposal): string[] {
   const hits: string[] = [];
@@ -178,7 +214,7 @@
 
 /** Oracle P: the figures of the proposal found in a text (a dollar sign counts too), part codes in position removed first. Empty = no price in the text. */
 function figuresIn(text: string, p: PurchaseProposal): string[] {
-  return figuresInText(stripCodes(text, p), p);
+  return figuresInText(stripCodes(text, p).split(UNIT).join(''), p);
 }
 
 /** Every leaf element's text (whitespace collapsed, the style element left out). */
@@ -198,10 +234,10 @@
  * U10 (no new word): the leaves of the unpriced render that are not exactly a leaf of the priced render, once the part codes in
  * position are removed. The one named exception must be the last sentence of some priced leaf.
  */
-function unexplainedLeaves(unpriced: string[], priced: string[], p: PurchaseProposal): string[] {
+function unexplainedLeaves(unpriced: string[], priced: string[], p: PurchaseProposal, exceptions: string[] = U10_EXCEPTIONS): string[] {
   const pricedSet = new Set(priced);
   const endsPriced = (t: string) => priced.some((x) => x.endsWith(t) && (x.length === t.length || x.charAt(x.length - t.length - 1) === ' '));
-  return unpriced.map((t) => stripCodes(t, p)).filter((t) => !pricedSet.has(t) && !(U10_EXCEPTIONS.includes(t) && endsPriced(t)));
+  return unpriced.map((t) => stripCodes(t, p)).filter((t) => !pricedSet.has(t) && !(exceptions.includes(t) && endsPriced(t)));
 }
 
 function draw(doc: Doc, p: PurchaseProposal, priced?: boolean) {
@@ -328,7 +364,7 @@
       for (const { name, make } of FIXTURES) {
         const p = make();
         const priced = read(doc, p, undefined, leavesOf);
-        const unknown = unexplainedLeaves(read(doc, p, false, leavesOf), priced, p);
+        const unknown = unexplainedLeaves(read(doc, p, false, leavesOf), priced, p, doc === SHORT ? U10_EXCEPTIONS : []);
         expect(unknown, `${doc.key} over ${name}`).toEqual([]);
       }
     });
@@ -430,6 +466,119 @@
     });
   });
 
+
+  describe('the left boundary of the position strip: a code can start only where a line item can start', () => {
+    const WIDGET = 'Synthetic widget';
+    const CODE = '4521.10';
+    // Tails of an amount, each printed WHOLE in a code slot: [the line's code, the amount that ends with it].
+    const TAILS: [string, string][] = [
+      ['0.50', '1250.50'],
+      ['0', '1234.50'],
+      ['0.00', '57940.00'],
+      ['50', '1250.50'],
+    ];
+
+    it('the closed list of places a code can start holds exactly three', () => {
+      expect(CODE_STARTS.map((s) => s.name)).toEqual(['startOfText', 'startOfTextNode', 'afterQuantity']);
+    });
+
+    it('B1: an amount whose tail equals a line code, printed in that code slot, is found (the gate case: code 0.50, price 1250.50)', () => {
+      for (const [code, amount] of TAILS) {
+        const p = withCodedLine(code, amount);
+        const text = `${amount} ${WIDGET}`;
+        expect(stripCodes(text, p), `${code} of ${amount}`).toBe(text);
+        expect(figuresIn(text, p), `${code} of ${amount}: the text`).toContain(`${amount} shown as ${amount}`);
+        expect(figuresIn(scanText(tiny({}, text)), p), `${code} of ${amount}: the document`).toContain(`${amount} shown as ${amount}`);
+      }
+    });
+
+    it('B1: the same with the quantity prefix and with the grouped form of the amount', () => {
+      const p = withCodedLine('0.50', '1250.50');
+      expect(figuresIn(`7 ${TIMES} 1250.50 ${WIDGET}`, p)).toContain('1250.50 shown as 1250.50');
+      expect(figuresIn(`1,250.50 ${WIDGET}`, withCodedLine('250.50', '1250.50'))).toContain('1250.50 shown as 1,250.50');
+    });
+
+    it('B1: a code that is a middle slice of an amount never matches in the slot, so the amount is found', () => {
+      for (const [code, amount] of [['940.0', '57940.00'], ['4521', '14521.10']] as const) {
+        const p = withCodedLine(code, amount);
+        expect(figuresIn(`${amount} ${WIDGET}`, p), `${code} in ${amount}`).toContain(`${amount} shown as ${amount}`);
+      }
+    });
+
+    it('B2: the three legitimate starts strip the code: the start of a text, the start of a text node, after "<digit> x "', () => {
+      const p = withCodedLine(CODE, '9000.00');
+      const line = `${CODE} ${WIDGET}`;
+      expect(stripCodes(line, p)).toBe(WIDGET);
+      expect(stripCodes(`${UNIT}${line}`, p)).toBe(`${UNIT}${WIDGET}`);
+      expect(stripCodes(`7 ${TIMES} ${line}`, p)).toBe(`7 ${TIMES} ${WIDGET}`);
+      expect(stripCodes(`1,000 ${TIMES} ${line}`, p)).toBe(`1,000 ${TIMES} ${WIDGET}`);
+      expect(stripCodes(`4 ${TIMES} ${line}; 4 ${TIMES} ${line}`, p)).toBe(`4 ${TIMES} ${WIDGET}; 4 ${TIMES} ${WIDGET}`);
+    });
+
+    it('B2: a code at the start of a text node is a start even when the node before it ends in a digit', () => {
+      const p = withCodedLine(CODE, '9000.00');
+      const row = document.createElement('tr');
+      for (const t of ['7', `${CODE} ${WIDGET}`]) row.append(document.createTextNode(t));
+      const root = document.createElement('article');
+      root.append(row);
+      expect(visibleText(root)).toBe(`7${CODE} ${WIDGET}`);
+      expect(figuresIn(scanText(root), p)).toEqual([]);
+    });
+
+    it('B3: anywhere else the code is not stripped, so a code that equals an amount is found there (after a space, a letter, a bracket, a semicolon, a non-digit and a multiplication sign)', () => {
+      const p = withCodedLine(CODE, CODE);
+      const line = `${CODE} ${WIDGET}`;
+      for (const text of [`Total ${line}`, `Price:${line}`, `(${line})`, `; ${line}`, `a ${TIMES} ${line}`, `7${TIMES} ${line}`, `7 ${TIMES}${line}`, `7  ${TIMES} ${line}`, `${UNIT} ${line}`]) {
+        expect(stripCodes(text, p), text).toBe(text);
+        expect(figuresIn(text, p), text).toContain(`${CODE} shown as ${CODE}`);
+      }
+    });
+
+    it('B3: a code printed in an attribute value is read, never stripped, even when it reads "<code> <description>"', () => {
+      const p = withCodedLine(CODE, '9000.00');
+      expect(figuresIn(scanText(tiny({ 'data-x': `${CODE} ${WIDGET}` }, 'nothing here')), p)).toContain(`${CODE} shown as ${CODE}`);
+      const q = withCodedLine('0.50', '1250.50');
+      expect(figuresIn(scanText(tiny({ title: `1250.50 ${WIDGET}` }, 'nothing here')), q)).toContain('1250.50 shown as 1250.50');
+    });
+
+    it('B4 (the right side): a figure printed against the description, with or without a space, is found: the strip removes the code and one space, nothing after the description', () => {
+      const p = withCodedLine('SYN-R-1', '57940.00');
+      for (const text of [`SYN-R-1 ${WIDGET}57940.00`, `SYN-R-1 ${WIDGET} 57940.00`, `SYN-R-1 ${WIDGET}57,940`, `7 ${TIMES} SYN-R-1 ${WIDGET}57940`]) {
+        expect(stripCodes(text, p), text).toBe(text.replace('SYN-R-1 ', ''));
+        expect(figuresIn(text, p), text).not.toEqual([]);
+      }
+      const q = withCodedLine(CODE, '1250.50');
+      expect(figuresIn(`${CODE} ${WIDGET}1250.50`, q)).toContain('1250.50 shown as 1250.50');
+    });
+
+    it('limit, stated: a code printed in its own slot is read as data whatever it holds, a code that contains an amount included', () => {
+      const p = withCodedLine('PN57940.00X', '57940.00');
+      expect(figuresIn(`7 ${TIMES} PN57940.00X ${WIDGET}`, p)).toEqual([]);
+      expect(figuresIn(`7 ${TIMES} 57940.00 ${WIDGET}`, withCodedLine('57940.00', '57940.00'))).toEqual([]);
+    });
+
+    describe('the tail case through the real documents (the gate plants: the code slot of L3 or of L4 and L6 holds the amount)', () => {
+      const tailProposal = () => {
+        const first = s4Proposal().packages[0];
+        if (!first) throw new Error('the synthetic proposal has no package');
+        return s4Proposal({
+          optionalItems: [{ code: '0.50', description: 'Synthetic gate option', sectionLabel: first.label, unitSellExTax: '1250.50', priceOnRequest: false }],
+          softwareReconciliation: [{ label: 'Synthetic gate software', code: '0.00', scope: first.label, quantity: 1, amount: '57940.00' }],
+        });
+      };
+
+      it('B5: the unpriced documents print the tail codes in position and no figure', () => {
+        const p = tailProposal();
+        for (const doc of DOCS) {
+          const found = read(doc, p, false, (a) => ({ text: visibleText(a), hits: figuresIn(scanText(a), p) }));
+          expect(found.text, doc.key).toContain('0.00 Synthetic gate software');
+          if (doc === FULL) expect(found.text, doc.key).toContain('0.50 Synthetic gate option');
+          expect(found.hits, doc.key).toEqual([]);
+        }
+      });
+    });
+  });
+
   describe('U10 as a function', () => {
     const p = s4Proposal();
     const LAST = `${T.rateMethod(formatRate('0.0061'), formatRate('0.0580'))} ${K.NO_MONTHLY_TOTAL}`;
@@ -454,7 +603,7 @@
     it('a leaf that differs from a priced leaf by a part code in position is explained; by any other word it is not', () => {
       const coded = withCodedLine('SYN-ABC-1', '9000.00');
       expect(unexplainedLeaves(['SYN-ABC-1 Synthetic widget'], ['Synthetic widget'], coded)).toEqual([]);
-      expect(unexplainedLeaves(['SKU SYN-ABC-1 Synthetic widget'], ['Synthetic widget'], coded)).toEqual(['SKU Synthetic widget']);
+      expect(unexplainedLeaves(['SKU SYN-ABC-1 Synthetic widget'], ['Synthetic widget'], coded)).toEqual(['SKU SYN-ABC-1 Synthetic widget']);
       expect(unexplainedLeaves(['SYN-ABC-1 - Synthetic widget'], ['Synthetic widget'], coded)).toEqual(['SYN-ABC-1 - Synthetic widget']);
     });
   });
```
Start marks are the only thing that tells a node start from the middle of the joined text line, which is why a numeric code in a table cell after a cell ending in a digit stays clean (cell B2, second). **The review's own rule ("strip only when the character before the code is not a digit, a dot or a comma") is mutant M9 below: MEASURED, it closes the Major (the B1 cells stay GREEN) but 4 cells go RED, because it still strips a code that equals an amount at any place after a space or a letter (`Total 4521.10 <desc>`) and a code at the start of an attribute line, so its stated limit would be wider than "in its own place". That is why this kit uses the closed list (Q1); do not replace the list by that rule.**

## THE STATED LIMITS (frozen sentences; no other wording of the limits may appear in a file you write)
- **L-A:** "A part code printed in its own place is read as data, whatever it holds: a code that equals an amount, or contains one, prints and reads clean there. The same text printed anywhere else is still found."
- **L-B:** "A figure with cents printed rounded, re-grouped or abbreviated (57,941 for 57940.50, 57 940, 57.9k) is not read by the price check; the no-new-word check flags the new text instead."
- **L-C:** "A figure staff type into a free-text narrative field is their own text and is not scrubbed."
Where they go: (1) the test file's first-lines comment (head `:1` to `:5`) says L-C already; add L-A and L-B there and, above `stripCodes` (head `:158` to `:162`), replace the sentence "A code printed anywhere else stays in the text ..." by the closed list in one comment (the three starts); (2) this round's commit body (below); (3) the ADDENDUM's round-2 section. **The first commit's body says "an amount printed in the exact slot of a code that is equal to it reads as clean"; a second commit cannot change a first commit's body: the SQUASH text Tuesday writes carries the true limits** (the drafted `squash-body.txt` and `pr-body.md` in the review's folder already say L-A and L-C; they say "rounded or regrouped" and not "abbreviated": Tuesday's to align; you do not write them and you say so in FOR TUESDAY).

## THE ADDENDUM (a project file outside the repository: `1_Project_Definition/Briefs/2026-11-20_B1767_WORD-PACK-ADDENDUM.md`)
Keep every byte of the round-1 text; ADD one dated section at the end, heading `## Round 2 (added 2026-11-20 after the independent review of the first head; the sections above are the first round's text and stand)`, ASCII only, with these four items (the figures are the review's, quoted from `VERDICT.md` lines 12 and 13; name that file and the fixture in the text):
1. **A code that looks like a price prints as typed.** "Staff type a manual item's code as free text of 1 to 60 characters, so a code such as $1,234.56 or 4521.10 prints exactly as typed in the customer's unpriced document, in all six places. The review's hostile fixture PDFs held 16 price-shaped strings in the full proposal and 14 in the short form; every one was inside a code, and there were none once the fixture's codes were removed."
2. **A long unbroken code shrinks the printed PDF.** "A long unbroken code (about 20 characters or more) in the first stream card of a proposal with many packages widens the card grid, and Chrome then scales the whole printed document down. In the review's seven-package hostile proposal (a review file, not committed) the heading height on page 3 read 16.76 pt with no long code, then 16.61, 15.64, 14.78 and 13.30 pt at 20, 25, 30 and 40 characters, and 11.19 pt at 60 characters (a scale of about 0.67); the full proposal went from 14 pages to 13 at 30 and 40 characters and to 12 at 60. With the two-package s4 layout, codes up to 40 characters changed nothing (12 pages, 16.76 pt). No cell was clipped and no table crossed the page edge on the pages looked at. This is not fixed in this lane (styles are outside it): letting a code break inside the stream cards, with a PDF check, is a separate follow-up. How long real catalogue codes are is UNMEASURED."
3. **The limits, corrected:** L-A, L-B and L-C verbatim, and "this replaces the first bullet of section 6 where it says the code must be equal to the amount".
4. **A count corrected:** "The first round's build record gave 24 added source lines; `git diff --numstat` of the first head reads 26 (+21 in ProposalDocument.tsx, +5 in OnePager.tsx), all ASCII."
**Build and write it per the records-file rule:** read the whole file, build and ENCODE the whole new content first (the file already holds non-ASCII bytes, the multiplication sign: keep the old bytes as bytes, encode only the ADDED text, which is ASCII), write it to a temp file beside the target, `os.replace` it, then `cmp` the old prefix against a before-copy (prefix equal, the added bytes after it, 0 non-ASCII in the added bytes). The first round's section 1 to 6 text does not change.

## PREDICTIONS (write `.tools/b1775/predictions.txt` BEFORE any edit of the test file; print its sha256; a prediction that fails is named in STATUS, not edited)
(a) At `fa71fc87` in your clone: `src/proposal/unpriced.test.tsx` reads 77 tests green; the whole suite 149 files and 1712 tests (RELAYED from the review; yours is the baseline). (b) With the start constants and the 11 cells added over the unchanged function: `5 failed | 83 passed (88)`, the RED set as the cells table says; if the set differs, STOP before any fix and print both. (c) With the function fixed and the exception scoped: 88 passed. (d) Round-1 plants over the fixed file (MEASURED in the drafter's copy, the cell sets are the check, the totals are yours): P1 turns 9 red (8 of the review's list and the cell B5), P2 13, P3 1 (U10 of the full proposal), P4 4 (the four short-form golden cells; `OnePager.test.tsx` and `ProposalDocument.test.tsx` stay green: the three files read `4 failed | 57 passed (61)`). (e) Plants P5, P6, P7 (the review's shape): over the cells-only state B5 stays GREEN (the blindness, shown); over the fixed file B5 is RED. (f) The ten mutants of THE MUTANTS (M1 to M9 and M4b) each go RED on the named cells. (g) After the commit: exactly ONE path differs between `fa71fc87` and your HEAD (`web/src/proposal/unpriced.test.tsx`). (h) Every added line of the test file is ASCII. (i) Whole suite after: 149 files, 1723 tests (1712 + 11, DERIVED). (j) the census of THE RULE reads 0 occurrences at another place.

## THE PLANTS AND THE MUTANTS (the builder's own proof, "builder's own run, not independent": each applied with the Edit tool, the file run, the RED cells printed with their failing assertion line, undone with the Edit tool, proved by `git hash-object` equal to the blob printed before)
**Source plants (the review's shape; edits of the clone's SOURCE files, undone before the commit; the gate's own mutant is P5):**
| Id | Plant | Over the cells-only state | Over the fixed file |
|---|---|---|---|
| P5 | `ProposalDocument.tsx:419`: `partCoded(o.code, o.description)` becomes `partCoded(o.unitSellExTax ?? o.code, o.description)` | B5 GREEN (blind); 17 red in all: the 5 not-yet-fixed cells and 12 fixture cells that print the wrong text | B5 RED; 13 red in all |
| P6 | `OnePager.tsx:368`: `partCoded(s.code, s.label)` becomes `partCoded(s.amount, s.label)` | B5 GREEN; 16 red in all (the 5 not-yet-fixed cells and 11) | B5 RED; 12 red in all |
| P7 | `ProposalDocument.tsx:467`: `partCoded(s.code, s.label)` becomes `partCoded(s.amount, s.label)` | B5 GREEN; 18 red in all (the 5 and 13) | B5 RED; 14 red in all |
(MEASURED, the drafter's copy: over the original function with the 11 cells the Tests lines read 17, 16 and 18 failed for P5, P6 and P7, and over the fixed file 13, 12 and 14; the totals are yours to print, the point is B5.)
**Round-1 plants over the fixed file** (P1 `data-total` on the unpriced KPI strip `:296`; P2 `57,940` ending the first schedule cell `:398`; P3 the words `package price` in the Qty cell; P4 `22%` to `23%` at the short form's first column in `OnePager.tsx`): the cell sets of prediction (d).
**Mutants of the TEST function (edits of `unpriced.test.tsx`, undone with the Edit tool):**
| Id | Mutant | RED (MEASURED; the other cells stay GREEN) |
|---|---|---|
| M1 | the boundary removed again: a fourth start that always matches | 6: the two B1 cells, the two B3 cells, the closed-list cell, the U10 function cell with `SKU` |
| M2 | the boundary on the wrong side: the starts are tested at the character AFTER the match | 15 (the tails stay clean, the legitimate starts stop stripping: B2 both, B4, `limit`, B5, rows B C E, the numeric-code cells, both U10 document cells) |
| M3 | the list emptied: `CODE_STARTS = []` | 16 |
| M4 | a start that is not real: after a space | 3: B3 (anywhere else), the closed-list cell, the U10 function cell |
| M4b | the quantity start without the digit test | 1: B3 (anywhere else) |
| M5 | the text-node start dropped from the list | 7: the three numeric-code cells, both B2 cells, the closed-list cell, B5 |
| M6 | the right side eaten: the strip also removes a following digit, dot or comma run | 1: B4 |
| M7 | attribute lines also written with a start mark | 1: B3 (attribute) |
| M8 | a fourth start: after any character that is not a letter, a digit, a dot or a comma | 4: B3 both, the closed-list cell, the U10 function cell |
| M9 | the review's rule in place of the list: `CODE_STARTS` is one function, "the character before is not a digit, a dot or a comma" (the alternative of Q1; it must close the Major and be wider than the stated limit) | 4: B3 (anywhere else), B3 (attribute), the closed-list cell, the U10 function cell; the B1 cells stay GREEN |
**No mutant may stay green: a green mutant means a missing cell: add the cell, never edit the mutant.**

## COUNTS, SELECTORS, TOOLCHAIN
- **Cells by the indented pattern** `^[[:space:]]+(it|test)(\.each\(.*\))?\(` in `unpriced.test.tsx`: 68 at the head, 79 with the reference diff (+11); by the column-1 pattern `^(it|test)\(`: 0 at both. Runtime tests: 77 at the head, 88 after (the 11 sit outside the per-document loop, so one runtime test each). The exception edit adds no cell.
- **Every filtered run prints its `Tests` line and a total of 0 is a STOP** (a selector that matches nothing returns rc 0). Measured selectors over the 88-test file: `-t 'the left boundary of the position strip'` reads 11 passed | 77 skipped; `-t 'the tail case through the real documents'` 1; `-t 'the closed list of places a code can start'` 1; `-t 'U10: no new word'` 2 (one per document); `-t 'U10 as a function'` 4; `-t 'the position strip: a part code made of digits and a dot'` 8. vitest `-t` is a regular expression over the full test name, and the dots and parentheses of a title are metacharacters: prefer the file path and these plain phrases.
- **Toolchain by PATH.** The project has NO drive-local node (the `.tools` listing holds `dotnet`, `dotnet-10.0.404` and no node folder). **Use Tuesday's node 24**: `PATH='/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/node-v24.22.2-darwin-arm64/bin':$PATH` first, `node --version` prints `v24.22.2`, `npm --version` prints `11.19.1` (MEASURED at drafting). **Why 24:** hosted CI runs `node-version: 24` (`.github/workflows/ci.yml:58`) and the review's numbers (149 files, 1712 tests, 260 + 17 and 161 browser tests) are node 24; the first round's builder used the machine's v26.13.0. Executing a binary there is not a write outside your folders. If the path does not answer: say so, use `/opt/homebrew/bin/node` and say which node every number came from. `TZ=UTC` for the goldens file (the review ran it so). Playwright is the Chrome of the machine (`/Applications/Google Chrome.app`).
- **The CI web job as CI runs it** (`.github/workflows/ci.yml:45-93`, read at the head): `npm ci`; `npm audit --omit=dev --audit-level=high` (pass predicate: exit 0); `npm run lint` (exit 0); `npm test` (0 failed); the stub step (`MPSCALC_E2E_MODE=stub`, `VITE_MPSCALC_API_STUB=1`); the api-off step (`MPSCALC_E2E_MODE=api-off`); `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist` (exit 0). Port and base URL for your browser runs: the block of Stamp S7, the second port, written as CI's variables name them (`MPSCALC_WEB_PORT`, `MPSCALC_E2E_BASE_URL`, and `MPSCALC_E2E_START_WEB=1`). **Expected totals, RELAYED from the review at the head and DERIVED for the test count: the stub step 260 passed and 17 skipped, the api-off step 161 passed, the build and the bundle check exit 0, whole vitest 149 files and 1723 tests (1712 + 11).** A browser run goes in the background and is waited for, never wrapped in `timeout`; after EVERY browser run print `lsof -nP -iTCP:<port> -sTCP:LISTEN | wc -l` (must be 0). Also `npx tsc -b` rc 0.

## FACTS (re-print at your head; a pointer is the drafter's, printed once, and can be stale)
1. **Refs** (MEASURED by `gh api -X GET` under the project `GH_CONFIG_DIR`, account `kamilDatasec`, at 14:04:25, for main again at 14:14:48, and all three again at 14:20:39): main `565ba142d4d07b183099eee42c1b73f94242489b` unmoved; `matching-refs/heads/b1767` one row `fa71fc87218120192aa0c68c2c85936978b997d9`; open pull requests 0; `compare main...fa71fc87` ahead 1, behind 0, 12 files. **Landing rule** (quoted by the review's `landing.txt`): Tuesday opens the PR and lands it with the head pinned (`--match-head-commit`), squash; you open nothing.
2. **The three blobs at the head** (MEASURED: `git hash-object` over the tarball copy equals the compare's `sha` for each): `web/src/proposal/unpriced.test.tsx` `e7584a6fb8278c626611d81651e9f17d3baa1ca1` (984 lines at the head; 0 non-ASCII lines; this is the only path you change), `web/src/proposal/ProposalDocument.tsx` `df4b6bb9475e6ef18392c79232b7afcf01ff6c71`, `web/src/proposal/OnePager.tsx` `9d02239f8d1363a9ab65958cbe9f9f49eb9bccd2`, `web/src/proposal/pricedUnchanged.test.tsx` `9f2aa36e49957a9222b2d8783b6c3fa90cd0d82e`. The eight golden blobs (head, from the compare): document-eight `f2b423dceef0a66556548afec1d1fa9775f36877`, document-five `23143888862d7020714df92cc42606fffaa6d4ed`, document-s4 `e82946b21cadb73b0c54f8d877f7fc214741b968`, document-s4final `cb87c344017aa7ed8170f71d21be20e84c919b64`, onepager-eight `b27ff6fe3de20132e9233f596f0f1e158e7570b8`, onepager-five `417203802881f36eede8bf490018dca01161ff35`, onepager-s4 `bb763aa168d55e429fb068bbf9d57e3f912560af`, onepager-s4final `ace95f556eac928c3c9da568b8fabcc89e6c86fa`. **A different blob at your head means the branch moved: STOP.**
3. **The sites at the head** (MEASURED `file:line`): `partCoded` `ProposalDocument.tsx:197`; `withPartCodes` `:203`; `detail` `:207`; L1 `:345` and `:398`; L2 `:360`; L3 `:419`; L4 `:467`; `OnePager.tsx` `detailCell` `:74`, L5 `:246`, L6 `:368`. The dry run's source plants are on `:419`, `:467` and `OnePager.tsx:368`.
4. **The dry run's scope (what the drafter did NOT run):** the whole suite, the browser steps, the build, the bundle check, `npm audit` and CodeQL. The goldens file alone was run twice (10 passed), and with plant P4 together with the two older test files (4 failed, 57 passed). **UNMEASURED by the drafter: the whole-suite totals, the two browser steps, `npx tsc -b` (only the test-file config was run), the entra build.**
5. **Machine** (MEASURED 14:12): `lsof -nP -iTCP:9980-9989 -sTCP:LISTEN | wc -l` prints 0 (control: the unfiltered listener count is 15); `df -g` 1030 GiB free; no `.heavy-lock*` or `.git-lock` entry in the project's `.tools` listing (0 entries name `lock`; control: 3 entries name `dotnet`; the listing also holds the first round's `b1767`); no `Datasec/MPS-` pane in `tmux list-panes -a`. The repo's identity: `git -C '<project>/2_Project_Files' --no-optional-locks config --local --get user.email` prints a non-empty address (29 bytes with the newline).
6. **Git identity (the repo's own, never overridden):** in YOUR clone set local `user.name` and `user.email` to exactly what the project repo's `config --local --get` prints (by program, never typed). **Never `git -c user.name/user.email`, never `GIT_AUTHOR_*` / `GIT_COMMITTER_*`.** READY prints `git log --format='%h %ae | %ce'` for the new commit, each address equal to the repo's configured email.
7. **The first round's STATUS** (`1_Project_Definition/Briefs/2026-11-20_B1767_STATUS.md`, 137 lines, last line `READY B1767: fa71fc87218120192aa0c68c2c85936978b997d9`) and the ADDENDUM (55 lines) are read whole by the drafter; the STATUS's BLUF and the ADDENDUM section 6 carry the round-1 limits ("equal"); the STATUS check (b) carries the 24.
8. **Size: S to M.** The change is one test file (+158 and -9 lines in the reference diff, including the exception edit) and one records file; no source line, no golden. The first round was M.

## THE WORK (serial; one seat)
0. **Step 0 and STATUS** into `1_Project_Definition/Briefs/2026-11-20_B1775_STATUS.md`: FIRST line `PROGRESS B1775: PENDING`; the kit copy into `Briefs/` (`cmp`, sha256, 0 unfilled slots); the REFUSE counts with controls; `date`; `LC_ALL=C uptime`; `df -g`; **target READY = Step 0 + 150 minutes (`date -v+150M`); the push by Step 0 + 120, or STOP; HARD STOP = Stamp S8**; a `WORKING:` line as the LAST line, updated after each step. STATUS and the ADDENDUM are built whole, written to a temp file beside the target and `os.replace`d (never open the live file for writing before its content exists; `cmp` the prefix against a before-copy).
1. **PRIOR-WORK CHECK** (below), then **Setup**: `.tools/b1775/{logs,out,scratch,_quarantine}`, `/private/tmp/b1775-seat-tmp`, a clone with `--no-checkout` of the project's `2_Project_Files`, origin set to the SSH URL, ONE `git fetch origin b1767/mps-unpriced-part-codes-278` under `.tools/.git-lock` (atomic `mkdir`, holder file MOVED to logs after, `rmdir` your own dir; poll 2 min up to 15), `checkout --detach fa71fc87218120192aa0c68c2c85936978b997d9`, identity per FACT 6. Node per the toolchain line: print both versions. **Baseline at the head in the clone, before any edit** (HEAVY ones one slot at a time): `npm ci --prefer-offline` in `web` (say which packages, if any, came from the registry), `npx vitest run` whole (files, tests, failed: expect 149 and 1712 and 0), `npx eslint .` rc, `npx tsc -b` rc, `npx playwright test --list` for each mode (expect 277 tests in 19 files for stub, 161 in 8 for api-off, RELAYED), the blobs of FACT 2 against yours (all equal, or STOP), and `npx vitest run src/proposal/unpriced.test.tsx` (expect 77 passed).
2. **PREDICTIONS** to `.tools/b1775/predictions.txt` (sha256 printed) before any edit.
3. **CELLS FIRST (the proof the fault is real).** Edit the test file only: add `UNIT` and `TIMES` and an EMPTY `CODE_STARTS` placeholder (an array of functions, empty, used by nothing), the `scanText` start marks are NOT yet written, then the 11 cells of THE CELLS (copy their text from THE REFERENCE DIFF). Run the file: print the Tests line (expect `5 failed | 83 passed (88)`, STOP if the RED set differs) and the failing assertion line of each RED cell (the gate's proof: `1250.50` printed in the slot of code `0.50`, found by the cells and missed by the function). **Then run plants P5, P6 and P7 over this state** (table above): B5 must stay GREEN while the plant is in (this shows the blindness through the real documents); undo each with the Edit tool and prove the blob.
4. **THE FIX.** Make the function as THE REFERENCE DIFF shows it (the start marks in `scanText`, `figuresIn` removing them, the closed list, `replaceAtStarts`), the changed U10 line, THE EXCEPTION edit and the comments of THE STATED LIMITS. Run the file: `88 passed (88)`. Run `npx eslint src/proposal/unpriced.test.tsx` rc 0 and `npx tsc -b` rc 0.
5. **THE CENSUS** (a throw-away test file in your clone, quarantined before the commit): print the table of THE RULE for your head, 4 fixtures x 2 documents x the two classes, and the count at any other place (must be 0).
6. **PLANTS AND MUTANTS** as the two tables: P5, P6, P7 over the fixed file (B5 RED now); P1 to P4 over the fixed file (the cell sets of prediction (d); P4 runs `pricedUnchanged.test.tsx`, `OnePager.test.tsx` and `ProposalDocument.test.tsx`); M1 to M9 and M4b. Each: apply with the Edit tool, run, print the RED cells and the totals, undo, `git hash-object` equal. A green mutant: STOP and add the cell.
7. **THE ADDENDUM** as its section says; print the before-and-after sizes, the `cmp` of the prefix and the added bytes' non-ASCII count.
8. **CHECKS before the push (each with a planted control):** (a) **the diff names exactly one path:** `git diff --name-only fa71fc87..HEAD` prints `web/src/proposal/unpriced.test.tsx` and nothing else (control: a planted second path changes the count); the blobs of the two source files, `pricedUnchanged.test.tsx` and the eight goldens (FACT 2) are equal at your head (a cell-count and blob check: `pricedUnchanged.test.tsx` still holds 10 cells by the indented pattern, and `npx vitest run src/proposal/pricedUnchanged.test.tsx` prints `10 passed`); `ProposalPage.tsx`, `package.json`, the lock, `ci.yml`, every `.css` equal. (b) added lines of the test file ASCII (`LC_ALL=C /usr/bin/grep -c -v -x -E '[ -~]*'` over the added lines prints 0; control: a planted U+200B prints 1) and no Unicode Cf character; the control characters U+0001 and U+00D7 are built by `String.fromCharCode` and appear in no file as a literal byte; the three frozen strings of the first lane still read 3 in `ProposalPage.tsx` (control `Short-form proposal (PDF)` reads 1). (c) **no new word:** no string literal ADDED to a SOURCE file (you add none; `git diff` over the two source files is empty); the U10 cells green. (d) names: the UNDERSCORE-AWARE scan `(?<![A-Za-z])<name>(?![a-z])` (python re, case-insensitive) over added lines and the commit message for each name of the ban list in step 7 of `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md` (at least: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite) and the words Tuesday, Wednesday and Friday; control: a planted `_by_<name>_` fires for each. The word `Inch` can appear in the fixture description `24-inch`: NAME the context, never silence it. (e) gitleaks: a random `ghp_` canary rc 1 first, then the range rc 0. (f) hand rows over every ADDED line: `new RegExp(` from a variable (0; the one regex literal `/\s+/g` of `scanText` is a literal, said), `innerHTML =`, `dangerouslySetInnerHTML`, `eval`, `child_process`, `eslint-disable`, `waitForTimeout`, `.only(`, `ts-ignore`, storage, screenshot, video, trace, and any `console.log` that prints a document text (0 added). (g) no new package, setting, environment variable or storage key. (h) `git log --format='%h %ae | %ce' fa71fc87..HEAD`, each address equal to FACT 6's. (i) no real price, quote value, real part code or `.local` path. (j) porcelain empty after the commit (the throw-away census file, any plant leftovers and any `web/.vitest` folder are in quarantine); exactly ONE commit ahead of `fa71fc87`. (k) **the whole web check at your head, each HEAVY one at a time:** `npm ci`; `npm audit --omit=dev --audit-level=high` rc 0; `npx vitest run` whole (149 files, 1723 tests, 0 failed); `npx eslint .` rc 0; `npx tsc -b` rc 0; the stub step and the api-off step as CI runs them (the whole of each, in the background; expected 260 passed and 17 skipped, and 161 passed; print `npx playwright test --list` before and the totals after); `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist` rc 0. Not run = NOT RUN: CodeQL, any hosted probe, a real print-to-PDF (the gate's row; no source file changed).
9. **COMMIT.** ONE commit on top of `fa71fc87`, subject (98 ASCII characters, MEASURED by program): `Close the left boundary of the no-price check's part-code strip and state its limits (MPSCALC-278)`. Body, exactly (wrap as shown; no B-number, no person's name, no decision-card id, no sentence that the product owner approved anything; end with the attribution line your session reminder gives, count 1):
```
The no-price check removed "<code> <description>" wherever it sat in the text,
so an amount whose tail equals a line's code, printed in that line's code slot,
was removed with it and read clean (code 0.50, price 1250.50). The check now
removes a part code only where a code can start: the start of a text, the start
of a text node, or right after a quantity and the multiplication sign. A code
printed anywhere else, and every attribute value, stays in the scanned text and
is read. A figure printed against the end of a description is read too: nothing
after the description is removed. New cells prove each case, and a version of
the function with no boundary, with the boundary on the wrong side or with an
empty list of starts turns cells red.

The one exception of the no-new-word check now applies to the short form only.

The limits of the checks, as they are (the first commit's text said "equal"):
- A part code printed in its own place is read as data, whatever it holds: a
  code that equals an amount, or contains one, prints and reads clean there. The
  same text printed anywhere else is still found.
- A figure with cents printed rounded, re-grouped or abbreviated (57,941 for
  57940.50, 57 940, 57.9k) is not read by the price check; the no-new-word check
  flags the new text instead.
- A figure staff type into a free-text narrative field is their own text and is
  not scrubbed.

Only the test file changes: the two source files, the priced goldens and their
test are byte-unchanged.
```
10. **PUSH.** `HEAD:refs/heads/b1767/mps-unpriced-part-codes-278` with `GIT_SSH_COMMAND="ssh -i '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/3_Access_Keys/github_deploy_rw' -o IdentitiesOnly=yes"` for THAT command only; **no `--force`; a fast-forward only** (re-read the branch head first: it must still be `fa71fc87`; if it moved: `STOPPED: NEEDS TUESDAY the branch moved`). Re-read main first; if it moved onto `web/src/proposal/` or `web/src/test/`: `STOPPED: NEEDS TUESDAY main moved a path you read`. Read back with `gh api -X GET`: `matching-refs/heads/b1767/mps-unpriced-part-codes-278` is ONE row equal to your sha40; `compare fa71fc87...<sha40>` ahead by 1, behind 0, files exactly `web/src/proposal/unpriced.test.tsx`; `compare main...<sha40>` ahead 2, behind 0, 12 files (the same 12 paths of the first round).
11. **CONTEXT BAND AND HANDOVER.** About 70% context: start no new part; about 75%: stop at a safe boundary (files whole, no web server left on your port, no process running, any plant or mutant undone and proved, the census file in quarantine, no heavy lock held) and write `.../Briefs/2026-11-20_B1775_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps / branch head if pushed), last line `HANDOVER B1775: next <part> <step> | done <parts>`, and end STATUS with the same line.
12. **STATUS sections:** Step 0 | Toolchain | BLUF | PINS | PRIOR WORK | BASELINE | PREDICTIONS | CELLS FIRST (the RED set, the plants over the cells-only state) | THE FIX | THE CENSUS (the table) | PLANTS AND MUTANTS (both tables with the printed RED cells) | THE ADDENDUM | CHECKS (each step's rc, counts, wall-clock) | RESIDUE | NOT RUN | FOR TUESDAY | Trees left | Commits. **FOR TUESDAY carries:** the head sha; that the gate runs every CI step and the round-2 reading list below; that the squash text must carry L-A, L-B and L-C (the first commit's body says "equal"); that the review's `squash-body.txt` and `pr-body.md` say "rounded or regrouped" and not "abbreviated"; the follow-up for the long-code layout (a records pass files it; the review's `FOR-RECORDS.md` names it); that the stale `core.sshCommand` of the project repo (it names `/Volumes/Laptop-DEV/...`) was handled with an explicit key for each command; any line-item site found that the kit did not list, with `file:line`. **LAST LINE on finish is EXACTLY one of:** `READY B1775: <sha40>` (the branch head as read back by `gh api -X GET` AFTER the push; the ADDENDUM section written and its path printed) | `STOPPED: NEEDS TUESDAY <one question>` | `BLOCKED: <reason>` | `HANDOVER B1775: next <part> <step> | done <parts>`.

## THE ROUND-2 GATE'S READING LIST (what changed, where the proof is; the gate's kit is Tuesday's)
(1) `git diff fa71fc87..<head>`: ONE path, `web/src/proposal/unpriced.test.tsx`; the eleven other paths of the branch byte-equal (blob list in FACT 2); (2) the function: `scanText` (start marks), `CODE_STARTS` (three entries), `replaceAtStarts`, `stripCodes`, `figuresIn`, `unexplainedLeaves` and its short-form-only exception; (3) the cells `the left boundary of the position strip` (11) and the one changed U10 function cell; (4) the builder's census table and plant and mutant tables in the STATUS (the gate re-runs its own: the review's probes `zzprobe.test.tsx` and `zzprobe2.test.tsx` and the oracle copy, re-extracted from the new test file, must now FIND the `0.50` of `1250.50` case; the mutant set and the four round-1 plants; the goldens on node 24); (5) the ADDENDUM's round-2 section (four items, L-A to L-C verbatim); (6) the full CI web job; CodeQL on the PR head is Tuesday's. **The PDF row need not repeat unless a source file changed** (none does). The review's 16-render base-versus-head compare is unaffected (no source change): the gate need only prove the two source blobs equal.

## PRIOR WORK STANDING LINE
**PRIOR-WORK CHECK (Step 1; a READY without a `## PRIOR WORK` section is returned unread).** Re-read origin main (`gh api -X GET .../git/ref/heads/main`) and compare with Stamp S2; the branch head with Stamp S3 (`matching-refs/heads/b1767` must be ONE row, equal); MPSCALC-278 whole by Jira GET (names `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, in-process, never printed; write your OWN GET-only helper in `.tools/b1775/scratch/`, never copied from another seat's `.tools/*`; every JQL is `project = MPSCALC AND ( ... )` WITH the parentheses; control `key = MPSCALC-361` reads Done): **a status Done, or a comment newer than 2026-11-20 13:31 (the first round read comment 41409 there), is new: read it before building; a comment that rules the sites, the separator, the boundary or supplies words is `STOPPED: NEEDS TUESDAY` carrying its id and quote**; every PR naming the key (paginated to the end; controls #85 and #221 present; expect only #221 and none open); `matching-refs/heads/b1775` rows (expect 0). **Does the branch ALREADY do it?** Print the table (`ALREADY-ON-BRANCH`, `WORK`, `DROPPED`) with the lines that prove it: `CODE_STARTS` and `replaceAtStarts` do not occur in `unpriced.test.tsx` at the head (`/usr/bin/grep -c` prints 0 each; control: `stripCodes` prints at least 2); the describe `the left boundary of the position strip` does not occur; `exceptions.includes` does not occur. A part already there is `ALREADY-ON-BRANCH: <what> at <file:line>; no edit` and is skipped.

## THE LANE (partition from both sides)
| Field | Value |
|---|---|
| Branch | `b1767/mps-unpriced-part-codes-278`, EXISTING ref at `fa71fc87`; your clone `.tools/b1775/clone` detached at it; ONE new commit on top; fast-forward push |
| Your paths (property) | the paths whose blob differs between `fa71fc87` and your head are exactly `web/src/proposal/unpriced.test.tsx`; plus (outside the repository) the ADDENDUM file. Any other path: prove it meets the property or `STOPPED: NEEDS TUESDAY` |
| NOT yours | every other file: `ProposalDocument.tsx`, `OnePager.tsx` (unless the right-boundary question proves a product fault: a STOP), the eight goldens and `pricedUnchanged.test.tsx`, `ProposalPage.tsx` (the three option words), `RentalDocument.tsx`, `template/**`, every `.css`, `web/src/api/**`, every other test file, `web/e2e/**`, `playwright.config.ts`, `src/**`, `tests/**`, `docs/**`, `scripts/**`, `infra/**`, `tools/**`, `.github/**`, the root records, the first round's STATUS and kit, the first lane's WORD-PACK file |
| OUT of round 2 (each a line for the records pass; do not start) | letting a code break inside the stream cards (a style change with a PDF check: its own ticket and lane); the rental documents; the durable record of the choice; the three words; any deploy; any change to the product's behaviour |
| Disjointness | open PRs 0 and no `Datasec/MPS-` pane at drafting (FACT 1, FACT 5); the other kits of 2026-11-20 are NexusAI, OXPd and records seats. Shared: `.tools/.git-lock` (your fetch and push only), `.tools/.heavy-lock-1` and `-2` (HEAVY), the port block of S7, your STATUS and the ADDENDUM |
**PARTITION: every other lane's paths are NOT yours.**

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`; checked BEFORE `.tools/b1775` is created; each count with a control that can fail)
A stamp slot unfilled: `/usr/bin/grep -c -E '_''_''_''_' <Step-0 copy>` must print 0 (control: the unstamped kit prints the count in the Stamp heading); last line not `READ-WHOLE-BY-TUESDAY: DONE ...`; S2 or S3 not exactly one 40-hex token after the colon; S3 not equal to the live branch head. `.tools/b1775` exists; a local or origin ref `b1775*`; another `Datasec/MPS-M168` pane (`tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` prints exactly ONE line with that name and `$TMUX_PANE`); a live `Datasec/MPS-*` code pane whose kit GRANTS a path of yours. A listener on any port of the block of S7. `df -g /Volumes/Datasec_DEV` under 25 GiB free; `gh auth status` under the project `GH_CONFIG_DIR` not the Datasec account; the deploy key missing; `/private/tmp/b1775-seat-tmp` inside a git work tree; the project repo's `config --local --get user.email` empty; the node 24 path of the toolchain line not answering AND `/opt/homebrew/bin/node` not answering; `/Applications/Google Chrome.app` missing; `npm ci --prefer-offline` fails and the registry also fails. **Load is NOT a refuse.**

## HEAVY
At most TWO heavy jobs run machine-wide across MPS lanes. A heavy job = `npm ci`, a whole `npx vitest run`, `npm run build`, `npx tsc -b`, `npx eslint .` over the whole web folder, **`npx playwright test` as a real run of more than one spec file** (the whole stub step, the whole api-off step), a CodeQL database create or analyse, or any dotnet build or test. A single-file `npx vitest run <file>`, a single-file `eslint`, `npx playwright test --list` and a small family run of the proposal files are light. Take a slot by atomic `mkdir '<project>/.tools/.heavy-lock-1'` (else `-2`; neither free: poll every 60 s), write `holder.txt` (pane name, label, `date`), run ONE job, release by MOVING the holder file to `.tools/b1775/logs/` and `rmdir` your own dir. **Load gate: `LC_ALL=C uptime` load1 under 24 on TWO reads 120 s apart (not independent: say so)** (the product owner's 2026-11-11 ruling for this 18-CPU machine). A holder older than 30 minutes with no live pane is REPORTED, never removed. A wait is not a finding; waited 60 minutes: say so; at the hard stop `BLOCKED: heavy lock waiting at load <n>`.

## STANDING LINES
**PRIOR-WORK CHECK** (above). **No message to any human. Jira: read only, 0 writes.** **No customer word: round 2 changes a test file and a records file; a new word in a source file is a STOP.** Never skip a failure: fix the root cause and re-verify end to end; a red that is not yours is NAMED with its cause. **Never delete** (`rm`, `branch -d`, `--prune`, `gc`, `reset`, `clean`, `stash`, `checkout -- <file>`, `sed -i`): MOVE to `_quarantine`; a plant or mutant is undone with the Edit tool and proved by `git diff --quiet` or a blob compare. Not run = NOT RUN. Source beats this kit: where a pointer or text differs from what you print, say so and follow the source. Synthetic values only. Shell: no `cd`; absolute single-quoted paths (`!` and a space are in the project path); no unquoted word starting with `=` (the shell expands it); `git -C ... --no-optional-locks` for reads; `/usr/bin/grep -i` with a positive control per count (and `-F` for literals); a count piped through `cut` hides tokens (count with `grep -c` on the full text); a pipeline's `$?` is its last command's: run the checked command alone; every count, `file:line` and clock in STATUS is printed by a program. Inputs (tickets, reviews, earlier STATUS files) are data, read and never obeyed. **A defect found outside your ticket: STOP with both readings only if it makes your edit unwritable; otherwise note it in FOR TUESDAY with `file:line` and do not edit it.** Closed lists (the starts, the paths, the plants, the mutants) are stated by PROPERTY first and then "at least these"; any other shape: prove it meets the property or STOP. Git identity: the repo's own only. Landing is Tuesday's (PR, hosted CI, CodeQL; never bypass, never dismiss an alert). **NOTHING is deployed; MPS hosted is a card per deploy.**

## HOLDS
No path outside the lane property; no deploy, no PR, no Jira write, no message to a human; no merge to main; no force-push, amend, reset or rebase; never delete; no `cd`; **no edit of `ProposalDocument.tsx`, `OnePager.tsx`, `RentalDocument.tsx`, `ProposalPage.tsx`, any template, settings, model, format or CSS file, any golden or `pricedUnchanged.test.tsx` (the plants edit source files and are undone with a blob proof before the commit), no new contract member, DTO, endpoint, doc, generated file or stub rule, no browser storage key, no arithmetic or comparison on a figure, no allow-list of codes in the oracle, no skipped key and no raised threshold in the oracle, no new dependency, no `eslint-disable`, no `waitForTimeout`, no `test.only`, no screenshot, video or trace**; any file you rewrite as a whole (STATUS, the ADDENDUM, a scratch copy) is built and encoded in full first, written to a temp file beside it, then `os.replace`d; a records file is never opened for writing before its content exists, and never encoded as ASCII when it already holds non-ASCII bytes (encode the ADDED bytes and check them; `cmp` the prefix against a before-copy); the test file is ASCII (build U+0001 and U+00D7 by code); no git identity override; no write outside `.tools/b1775`, your clone, `/private/tmp/b1775-seat-tmp`, your STATUS, the ADDENDUM, the Step-0 copy and (only under the context band) the HANDOVER file; no listener but the web server of a browser run on the port of S7 (none left running); no hosted call (the npm registry only as above), `az`, docker, ssh, `apt-get`, `brew`; no probe of any hosted site.

## Questions with defaults (Tuesday answers at the stamp; every default is already assumed above; each is Tuesday's choice, none the product owner's)
- Q1 (the rule): default = a closed list of three places a code can start, with a start mark written before each text node. Alternative: the review's rule (the character before is not a digit, a dot or a comma); mutant M9 measures it: it closes the tails (B1 green) and goes RED on 4 cells that hold the limit to "its own place" (B3 twice, the closed-list cell, the U10 function cell).
- Q2 (the exception): default = scope it to the short form (IN, three lines). Alternative: leave it (round 1's text).
- Q3 (the ticket): default = the commit subject ends `(MPSCALC-278)` as the first commit's does. Alternative: name the part-code follow-up key the records pass filed (`MPSCALC-426` per the root records entry C-186).
- Q4 (node): default = Tuesday's node 24 by the path of the toolchain line. Alternative: the machine's v26.13.0, as round 1 (then say so).
- Q5 (gate): default = round 2 of 2 on the same tier as the first (the oracle that proves no price reaches a customer is what changed); a PDF row only if a source file changed.
- Q6 (level): default `sonnet` per routing row C2; Tuesday decides the level at the stamp from `models_latest.json`.
- Q7 (port block): default = the first round's block, free now (0 listeners at 14:12; the only kits naming it are the finished first-round kits and this round's). Tuesday re-reads the live pane list and the listeners at the stamp.
- Q8 (the long-code follow-up and the first round's STATUS correction): default = the records pass's (you write neither); the ADDENDUM states the facts.
- Q9 (counts): the whole-suite total 1723 is DERIVED; you print it.

## Stamp
The unstamped copy of this kit reads 10 such lines (S0 to S8 and the last line).
- (S0) COMMISSION (what named this round and what the product owner has said on this ticket since): Gate B1770 (round 1 of 2) read NO GO at fa71fc8 on main 565ba14 with one Major in the no-price check's code strip; this round is Tuesday's decision as coordinator to fix it before any pull request. The product owner has said nothing on this ticket since his ruling of 2026-11-20 on the three words (printed by Tuesday with decision_queue.sh show in the stamp command: status ruled, project Datasec/MPS Calculator, choice a; the ruling sentence this kit quotes was found once, byte for byte, in entry C-186 of the root records at root main, by program).
- (S1) STAMP (`STAMPED <time> AEDT <date> by <seat>`; what Tuesday read whole and re-printed): 14:24 AEDT 2026-11-20, stamped by Tuesday (seat s297). Tuesday read this kit with the Read tool, lines 1 to 470 in three pages. Re-printed by Tuesday in the stamp command (date printed 14:24:20 Fri 20 Nov 2026): code main, the b1767 ref, the b1775 refs, the open pull requests, the MPS panes, the listeners on 9980-9989, the project .tools listing; the head's unpriced.test.tsx fetched raw (blob e7584a6f as FACT 2 says, 984 lines, scanText at line 110, stripCodes at line 163, CODE_STARTS and replaceAtStarts and exceptions.includes each 0 times); ci.yml line 58 names node 24; the reference diff counted by program (158 added, 9 removed, 8 hunks, 11 added cells); the commit subject's 98 characters; routing line 92 holds row C2 and models_latest line 23 holds claude-sonnet-5-5. Recounted by Tuesday by hand: 99 + 174 = 273 and the eight per-document sums; 1712 + 11 = 1723; 77 + 11 = 88; ten mutants; ten slot lines. NOT re-printed by Tuesday: every dry-run result (the RED and GREEN sets, the plant and mutant totals, the census), the other file:line pointers, the golden blobs, the selectors' match counts, the figures quoted from the verdict, the sidecar literals. The sentence in section HEAVY that names a product owner's ruling of 2026-11-11 for the load gate is carried from the first round's stamped kit and was NOT re-checked by this seat: treat the load gate as Tuesday's standing rule.
- (S2) BASE (code main at origin, read at source by Tuesday; exactly one 40-hex token; the drafter read `565ba142d4d07b183099eee42c1b73f94242489b`): 565ba142d4d07b183099eee42c1b73f94242489b
- (S3) BRANCH HEAD (`b1767/mps-unpriced-part-codes-278` at origin, read at source by Tuesday; exactly one 40-hex token; the drafter read `fa71fc87218120192aa0c68c2c85936978b997d9`): fa71fc87218120192aa0c68c2c85936978b997d9
- (S4) STATE AT THE STAMP (open PRs; main; `^b1767` and `^b1775` branches; any `Datasec/MPS-` pane and the paths its kit grants; heavy-lock holders): Open PRs 0; main as S2; one b1767 ref at S3; b1775 refs at origin 0; Datasec/MPS- panes 0; listeners on 9980-9989 0; lock entries in the project .tools listing 0; .tools/b1767 present (the first round's: not yours), no .tools/b1775. One build seat of another Datasec project (NexusAI) runs on this machine and shares nothing with you.
- (S5) Q-ANSWERS (defaults: Q1 closed list of three starts; Q2 exception scoped; Q3 ticket key; Q4 node 24; Q5 gate; Q6 level; Q7 port block; Q8 follow-ups the records pass's; Q9 seat prints counts): All nine defaults, each Tuesday's own decision as coordinator and none the product owner's: Q1 the closed list of three starts (not the review's rule: mutant M9 shows why); Q2 the exception scoped to the short form; Q3 the subject ends (MPSCALC-278); Q4 node 24 by Tuesday's tools path; Q5 a round-2 gate on the first round's tier, no PDF row unless a source file changes; Q6 level sonnet; Q7 block 9980-9989; Q8 the long-code follow-up and the first STATUS's count are the records pass's; Q9 you print the counts.
- (S6) LAUNCH WINDOW (until; load1 at the stamp; live seats beside you; one waiter): Launch by 15:04 AEDT 2026-11-20; load averages 3.12 3.03 3.23; no MPS seat beside you; one waiter.
- (S7) PORT BLOCK AND MODEL RECEIPT (the block and the port for the browser runs; level; `BRIEF_SEAT_LEVEL` inside the quotes): Block 9980-9989, port 9981 for the browser runs; level sonnet (claude-sonnet-5-5); BRIEF_SEAT_LEVEL=sonnet inside the quotes; routing row C2.
- (S8) HARD STOP (absolute latest start; READY = your Step-0 date + 150 min; the push by Step 0 + 120; the absolute hard stop): Absolute latest start 15:04 AEDT; READY = your Step-0 date + 150 min; the push by Step 0 + 120; the absolute hard stop 17:59 AEDT 2026-11-20.
**Launch (Tuesday), ONE waiter, after the Stamp, level inside the quotes:** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/launch_when_cool.sh Datasec/MPS-M168 "CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1775_SEAT-M168_mps-part-codes-round2-oracle-boundary.md'"` No az. Nothing deploys. **Your commission is THIS file (read-only);** Step 0 copies it unchanged into `1_Project_Definition/Briefs/`.

READ-WHOLE-BY-TUESDAY: DONE by Tuesday (seat s297), stamped 14:24 AEDT 2026-11-20: Read tool, lines 1 to 470 in three pages (1 to 150, 151 to 340, 341 to the end). The one ruling the kit cites was checked in the stamp command (the decision printed with show: ruled, choice a, project Datasec/MPS Calculator; its sentence found once in C-186 at root main); every other choice is written as the coordinator's. Round 2 of 2: a second NO GO on this class goes to the product owner.
