--- comment 5825511678 by linear[bot] at 2026-09-25T02:08:14Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-530/hononode-server-v1-v2-major-bump-ghsa-frvp-originate-mcp-server">KS-530 @hono/node-server v1-&gt;v2 major bump (GHSA-frvp) - originate + mcp-server runtime</a></summary>
<p>

Split from KS-493 (Review H dep-currency wave). @hono/node-server advisory GHSA-frvp-7c67-39w9 (moderate) has fix >=2.0.5 only - a semver-MAJOR v1->v2 bump, so it cannot ride a lock-regen wave.

Reached at runtime via @modelcontextprotocol/sdk (mcp-server) and pulled by @prisma/dev (dev tooling); also hoisted into the root tree. Pins: originate 1.19.11, mcp-server 1.19.14, root 1.19.17.

Do: bump to ^2.0.5 in originate + mcp-server standalone locks (root follows), verify hono v2 serve() API usage (breaking changes), rebuild + retest both targets, then remove the GHSA-frvp-7c67-39w9 baseline exception in scripts/audit/audit-baseline.json. Kept as a TEMPORARY baseline exception (expires 2026-09-30) pending this migration.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-530-patchline-mcp-server-originate-take-hononode-server-11917-ccf5888867c8">Review in Linear</a></p>

