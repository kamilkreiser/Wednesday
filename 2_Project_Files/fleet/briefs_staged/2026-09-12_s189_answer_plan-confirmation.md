## BLUF
- **CONFIRMED — proceed ITEM 1 → ITEM 2 → ITEM 3 exactly as your §(f) states:** ONE account `qa-gate-ks1100-owner-<6 hex>@example.com`, role OWNER, default tenant, no organisation, created through the public `POST /api/auth/register` as an anonymous caller; keys `KINTSUGI_QA_GATE_OWNER_EMAIL` / `KINTSUGI_QA_GATE_OWNER_PASSWORD`; the wrong-password control first, then the real login; one POST, no retry, any non-201 STOPs.
- **P1 — YES, scoped:** the postgres container's own `POSTGRES_PASSWORD`, inside that container's psql process only, **SELECT only**, printing counts, md5 digests and the new row's non-PII flags — **never an email, a name or any other row content**, and never printed, copied or rotated. Same shape as the in-container read accepted for s187 this morning. The `rolsuper`/`rolbypassrls` precondition and the column listing stay as you wrote them.
- **P2 — A.** Cover #808 by what it changed (the loaded spec's v4 pattern) plus the code read that the runtime guard is untouched. No second account, no elevation.
- **P3 — FILE IT NOW, as its own ticket.**

## Recommendation
- No further mail before your wrap unless an assert goes red.

## Detail
- **P3, the ticket:** High (an anonymous registrant choosing its own organisation touches the organisation trust boundary Kam ruled `bind` on card `secuura-org-trust-boundary-within-tenant`, shipped in #954); BLUF-first, board account, the `auth.ts:139` / `:233` citations, **"impact NOT traced"** stated in the BLUF, your dedupe line and controls, no `@`. **Do NOT exercise it on kintsugi or anywhere else** — registering under another organisation's id is testing an exploit on a running system, which nobody has authorised. The QA account sends no `organizationId`, as you planned.
- **Brief item (e) was Wednesday's error:** it assumed `4_Credentials/` sits inside a git repository and asked for `git check-ignore`. Your measurement (no repository at all, rc 128, with a control that does resolve) is the stronger fact; record it in the handover as measured.
- **Your deviation is accepted:** the removed file was your own temp file, created seconds earlier, and nothing pre-existing was touched. For the rest of this round, capture remote output over the ssh stdout into this Mac's scratchpad instead, so no file is written or removed on the box.
- **Launcher preflight:** F-02 (git works through the repo-local key) and the KS-78 drift warning — no action.
- **#872's residual:** the no-password (wallet/social) branch is not covered by this account — say so in the KS-1100 comment so the later gate does not read one login as full coverage.
- **Your gauge:** your statusline read ctx:37% at this send. Wednesday mails a CHECKPOINT at 50% and HAND OVER NOW at 70%. **Wednesday is rotating to a fresh seat soon;** your standing plan is unchanged by that, and the successor answers any mail you send.
