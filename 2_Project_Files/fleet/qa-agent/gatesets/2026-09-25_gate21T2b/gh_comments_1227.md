--- comment 5826843007 by linear[bot] at 2026-09-25T04:39:05Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1252/spec-example-guard-e7-the-ulid-ish-benign-shape-exempts-any-prefix">KS-1252 Spec-example guard E7: the ULID-ish benign shape exempts any prefix, secret-named ones included (session_/password_/accesstoken_ + 20-32 upper alnum)</a></summary>
<p>

**Found 2026-09-18 while fixing KS-679 round 2 (the #922 gate's F1).** Pre-existing on develop `207716440`. #922 doesn't touch this line.

## What's wrong

The `BENIGN_SHAPES` entry `/^(?:[a-z]+_)?[0-9A-Z]{20,32}$/` ("prefixed ULID-ish fixture id", `scripts/spec-examples/check/contract.mjs:222` on develop) has an **unbounded, name-blind prefix**. E7 is the guard's only name-blind secret rule, so nothing else sees what this entry admits. Measured through `BENIGN_SHAPES` + `HIGH_ENTROPY_RE` from the contract:

| value | length | E7 |
| -- | -- | -- |
| `session_` + 32 upper-case alphanumerics | 40 | silent |
| `password_` + 32 | 41 | silent |
| `accesstoken_` + 32 | 44 | silent |
| 60-letter prefix + `_` + 20 | 81 | silent |
| control: `sk_live_` + 32 (two segments) | 40 | fires |
| control: `session_` + 32 lower-case | 40 | fires |

This is the same class as KS-679's F1, which Wednesday ruled fix-before-merge on #922.

**What depends on it today:** nothing, for E7. The published spec holds exactly 2 values this entry matches (`op_01HC9ZQ2WXYZ123ABCDEFG` and `exp_01HC9ZQ2ABCDEFGHIJKLMN`). Both are under E7's 40-char floor, so E7 never reads the list for them (measured over the spec's 4,730 tokens of 20+ chars; control: the anchor fixture token is found). Tightening the entry reddens nothing that exists.

## What to do

Give it KS-679 round 2's treatment:

* bound the prefix;
* deny secret-named prefixes (reuse `PREFIXED_UUID_RE`'s word list);
* pin each boundary with a guard-driven cell;
* red-proof each loosening.

Or remove the entry, if no fixture needs it after `anc_01HC…` left in KS-679.
</p>
</details>
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1253/spec-example-guard-e7-the-secret-name-deny-list-in-prefixed-uuid-re-is">KS-1253 Spec-example guard E7: the secret-name deny list in PREFIXED_UUID_RE is a denylist - tok_/sess_/sid_/pass_/refresh_/access_/csrf_/nonce_/invite_/reset_/totp_/hmac_/oauth_/creds_ + v4 are still admitted</a></summary>
<p>

**From the #922 tier-2 gate, round 2 (F9, Polish, TICKET), 2026-09-18.** #922 merged as `570ea002d`.

## What's wrong

`PREFIXED_UUID_RE` (`scripts/spec-examples/check/contract.mjs`) refuses secret-NAMED prefixes with a **deny list**. The gate probed that `tok_`, `sess_`, `sid_`, `pass_`, `refresh_`, `access_`, `csrf_`, `nonce_`, `invite_`, `reset_`, `totp_`, `hmac_`, `oauth_` and `creds_`, each followed by a lower-case v4 uuid (43-44 chars, so E7 reaches them), are still admitted. They were admitted at round 1 too.

**Not a blocker today**, measured by the gate:

* the pre-existing bare-uuid shape already exempts the same uuid unprefixed;
* the minter census has **0** uuid-minted prefixed credentials;
* the spec holds exactly 1 prefixed value, the anchor id.

## What to do

The robust fix is an **ALLOW list of the minted prefixes** (the census's 13 benign ones: `anchor` `audit` `batch` `ce` `conn` `did` `event` `evt` `int` `req` `site` `sync` `ts`) in place of the deny list. Then a new record prefix is a reviewed addition, and a new credential name needs no foresight. Pin each allowed prefix with a guard-driven cell and red-proof the list. The same family as KS-1252.

---

Filed from the gate report `2026-09-18-ks679-922-30c773ee8-tier2-r2` (F9).
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1252-ks-1253-e7prefix-bound-the-ulid-ish-prefix-refuse-fourteen-738a2a31c47b">Review in Linear</a></p>

