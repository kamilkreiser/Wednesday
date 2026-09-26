--- comment 5843863646 by linear[bot] at 2026-09-26T06:22:02Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1341/routeswebhooksts-returns-the-thrown-error-text-on-7-unconditional-500s">KS-1341 routes/webhooks.ts returns the thrown error text on 7 unconditional 500s, measured leaking under NODE_ENV=production</a></summary>
<p>

**BLUF:** `routes/webhooks.ts` **carries 7 unconditional** `message: err.message` **500 responses, and they leak under** `NODE_ENV=production` — measured, not inferred. `DELETE /api/webhooks/:id` returns the **thrown text**; rotate-secret returns **internal configuration text**. Same defect class as the systemErrors / gdpr / adminConfig work just merged, but a different route file and a different PR set, which is why it is its own ticket.

## Why High rather than Polish

Those three merges removed this pattern on the grounds that a thrown message can carry internal detail to a client. The reasoning applies unchanged here, and here it is **measured reaching the client in production mode** — including configuration text from rotate-secret, the most sensitive of the group. Nothing about the fix is novel; what is missing is that it was not applied to this file.

## Fix shape (the same one already merged three times)

Return a generic message for 5xx and keep the thrown text in the log only. Where a 4xx legitimately explains itself, gate the echo on the error marking itself safe to expose, as the demo-service handler now does.

## Not claimed

The count of 7 and the two named routes are the gate's measurement. Whether any further file in this family remains was not swept here.

## Board search before filing

Searched over 489 open issues, literal match on identifier + title + description: `routes/webhooks.ts`, `rotate-secret` — 0 open hits each; `err.message` fires and a fresh nonsense token returns 0, so the instrument discriminates both ways.

Refs KS-730
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1341-part-a-route-the-webhooks-get-and-post-500s-through-a-fail500-a45fec92859f">Review in Linear</a></p>

