## What changes

On a purchase quote, a user who holds the internal-metrics permission now sees one more table in "Purchase outcome", after the usage tables, whenever the server's calculation carries a recurring projection. The table is captioned "Projection" and has six rows (pages, click cost, managed service cost, click revenue, service revenue, recurring GP) and three columns (monthly, annual, contract).

- **A user without internal-metrics sees nothing of it.** The server sends the projection only to an internal-metrics caller, and removes it from every restricted read: the calculation, the snapshot, the version diff and the proposal. The page shows the table only when the projection is present. Without one there is no table, no placeholder and none of its words. Vitest rows and browser rows pin both cases.
- **Every figure is the server's.** The browser only formats each figure through the existing count and money formatters (money to 2 decimals). It adds, multiplies, compares and converts nothing, and the repository's browser-arithmetic guard scans the new file and reads 0. The contract column is the server's own contract figure, not monthly times term.
- **The dev stub** (development only, not in the production bundle) gives an internal-metrics persona a zero projection and gives every other persona none.
- A rental quote is unchanged.

## Words: PENDING

The ten words of the table are new and are PENDING the product owner's word pack: Projection, Monthly, Annual, Contract, Pages, Click cost, Managed service cost, Click revenue, Service revenue, Recurring GP. They are not shown on any hosted site until the pack is ruled. The member name `projection` also still waits for its approval.

## Not built

- The four prototype rows: pages mono and pages colour as two rows, total recurring cost, and total recurring revenue. The Api sends no such figures, and a browser sum is not allowed.
- The "(x12)" and "(xterm)" marks on the column heads.
- A rental projection table. The Api has no rental member yet.

## Not deployed

Nothing is deployed by this change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
