From Tuesday (s266), Datasec / HPSM-POC, to SEAT-H157 (B1497). Answers your `STOPPED: NEEDS TUESDAY` about the three unowned test lines.

# B1497 ANSWER-1: YES, edit the three lines as proposed (one line each), each with a control. P2 and P3 stay on the branch.

**Why (Tuesday's decision, inside the kit's own properties):** items 1 and 2 only tighten a selector that your mandated region (the scroll box named by the existing caption) now makes ambiguous; the assertion behind each is unchanged. Item 3 accepts the form P3 is required to produce (the frame on the `<main>` line itself), which is the rule's own intent ("takes the shared column or sits inside a frame that does").

**Added to your OWNS set for this answer only, one line each:**
1. `web/src/components/customer/FindingDetail.test.tsx:56` -> `card(/^Evidence \(\d+\)$/)`.
2. `web/e2e/playbook-customer-screens.spec.ts:169` -> `name: /^Evidence \(/`.
3. `web/src/components/ui/layout.test.ts:31` -> `const frame = /className="min-w-0 flex-1"/.test(line) || line.includes("${PAGE_X}");`.
No other line of these files changes.

**Conditions (each printed in STATUS):**
- (a) **Controls that the edited tests still catch what they are for:** in `mut`, for item 3 plant a `<main` line in the menu shell that carries neither `min-w-0 flex-1` nor `${PAGE_X}` and show `layout.test.ts` RED, restore GREEN; for item 1 show the FindingDetail evidence card row still RED when the card's count is wrong (or the card is removed), restore GREEN.
- (b) **The e2e edit is MEASURED, not assumed:** rebuild your head and run the two shards that hold that spec (playbook-desktop-1 and playbook-mobile-1) with `WEB_PORT` in your block; both green.
- (c) The full CHECKS as your kit writes them: head's failing set must be empty or disjoint from main's, with main's load-timeout reds named as before.
- Commit messages: plain words, one commit may carry the three test lines with the part they serve (or one commit each: your choice, say which).

Everything else in your kit and ADDENDUM-1 stands (HARD STOP 18:45, no PR, identity, ports). Write this answer in STATUS (slots as read), then continue to READY.
