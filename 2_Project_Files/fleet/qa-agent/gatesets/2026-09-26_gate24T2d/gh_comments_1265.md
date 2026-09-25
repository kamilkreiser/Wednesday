--- comment 5837898143 by linear[bot] at 2026-09-25T18:54:01Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1315/k6-echo-mask-four-sibling-argv-spellings-stay-green-under-the-t-1">KS-1315 k6 echo mask: four sibling argv spellings stay green under the T-1 tamper, so they pin nothing</a></summary>
<p>

## BLUF

Non-blocking finding from the tier-2 gate on PR #1244 (KS-1111, merged `5c59cf9b1ff5`). Four sibling rows in `k6DockerRedaction.test.ts` **do not red under the T-1 tamper** (reverting the QA-961-1 fallthrough), so they are not pinning the behaviour they appear to pin.

## What is unrowed

T-1 reverts the fallthrough that makes the two-argument branch also try the one-argument masks. Measured on the merged tree, it reds exactly three rows — L02, L03 and L08. The sibling spellings the same fix covers have **no row that discriminates them**:

* `--label -one -qe=NAME=VALUE` (the gate's L05)
* `-a -e --env=NAME=VALUE` (L07)
* `-e -e -eKEY=VALUE` (L04)
* `--label -e --env=NAME=VALUE` (L01)

Each is masked today, and each would still be masked under a fix that only handled the three rowed shapes. The suite cannot tell the two implementations apart.

## Why it is Polish and not a defect

Nothing leaks. The behaviour is correct at the merged tree; what is missing is the evidence that it is correct **for a reason** rather than by coincidence — the same shape as the finding this ticket's parent closed (a control that cannot fail is not a control).

⚠ **Name the rows carefully.** `SECRET_ENV_NAME` is UNANCHORED for `PASSWORD|PASSWD|SECRET|TOKEN|MNEMONIC` and ANCHORED only for `KEY` (`(?:^|_)KEY$`). On the broken path the whole glued token is read as the name, so `-eADMIN_PASSWORD` still matches on the PASSWORD substring and is masked **by accident**. A row named with an unanchored word is GREEN before the fix and pins nothing — which happened while building #1244 and is why L03 uses the literal name `KEY`.

## Done when

- ☐ each of the four sibling spellings has a row that reds under T-1
- ☐ each row's name is chosen so it is red before the fix (i.e. reachable only through the anchored `KEY` clause, or the `--env=` / `-e=` forms where the name read is `--env` / `-e`)

## Board search before filing

Literal match over **1,303 issues (includeArchived) and 3,677 comments**: `UNROWED-SIBLINGS` -> 1 (KS-1111, this finding's own record) · `ENV_SHORT_FLAG` -> 1 (same) · `maskAttachedShortEnv` -> **0** · `k6_docker.ts` -> 9 total / 3 open (KS-1164, KS-1111, KS-1098 — the slot-isolation and name-set subjects, none the mask's row coverage). **Searched those four terms, 0 open hits for this defect.** Controls: `readYaml` fires; a nonsense token -> 0.

## Provenance

Tier-2 gate `QA/Secuura-batch1243`, non-blocking, recorded at the merge of #1244.

Refs KS-1111
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1315-row-the-four-sibling-argv-spellings-the-qa-961-1-fallthrough-19068c66eca0">Review in Linear</a></p>

