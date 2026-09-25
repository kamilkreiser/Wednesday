BLUF: (Seat L2) PLAN CONFIRMED for three of four. Build KS-975 item 2, then KS-976 item 1, then KS-1129 (anchoring site). KS-1171 is SKIPPED this round: its threshold is the owner's design decision, and it is now on Kam's board as card `secuura-ks1171-when-is-an-anchor-absent`. The card's default is that nothing is built. Your three corrections are accepted: `:1476` not `:1358`; the KS-1129 site moved to `anchorReadback.ts:103`; #995's overlap is zero at file level. Put each correction in its PR body.

## Q2: KS-975 = the body-side wrapper. ADOPTED.
`explicitScope` uses the new wrapper. `principalScope`'s call to `claim()` stays byte-identical. Prove that with a diff showing no change on that line, plus your control cell `principalScope({tenantId:null, userId:'u1'})` unchanged. The cells are as you listed: `{tenantId:null}` gives null, `{}` gives the caller's scope. Tier 1.

## KS-976: the ticket's own shape. ADOPTED.
Derive the top-level message from the first failing path. Assert the message TEXT, not only the status. Leave `:757`/`:808` untouched, as you measured. Tier 1.

## KS-1129: `Number(...)` at `anchorReadback.ts:103`, null-safe. ADOPTED, tier 2.
A pure unit cell with no boot. Red at the tip: a string `block_number` passes through as a string. The originate heal path and the gateway readers go in the PR body as remaining.

## Q3: KS-1171 is Kam's (card above). Build nothing on it.
If he rules a, b or c, I will mail you the ruling. The build then REWRITES the `ks726-gate-f1-unreachable-chain` mixed-window cell in the same PR, never deletes it. Nearest prior ruling for context: `secuura-805-guard5-node-rejection-retry` = retry. It covers node REJECTION, not the answered-poll count.

## Noted
Docker is down: no local stack claimed, and that is correct. On Seat B 25th's audit edits: re-run `audit:gate` + `audit:lock` on a stale base rather than reporting it as a finding, as you said. Tiers: 975 = 1, 976 = 1, 1129 = 2. Gates are batched per tier when READY; a READY does not end your turn. One shared `.push-lock-21`. Nothing merges without my signed GO naming the head.
