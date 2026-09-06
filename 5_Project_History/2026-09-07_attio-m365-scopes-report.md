# ATTIO-8 — M365 connector scopes report

**Produced 2026-09-07 by the Datasec/Vision seat (s10) on Kam's ruling `attio-entra-consent-m365` => scopes-first.**
**Nothing was granted, requested or triggered.** Relayed here verbatim by Wednesday; Wednesday has verified none of it independently.

---

# ATTIO-8 SCOPES REPORT — for Kam's decision. Nothing granted, nothing requested, nothing triggered.

## BLUF — the answer to the question he asked
**Yes. Something reads message bodies.** `Mail.Read` and `Mail.ReadWrite` cover the full message,
body included, and Attio's own documentation confirms it stores bodies rather than headers alone.
This is not a metadata-only connector.

**And it is not read-only.** Three of the seven permissions are WRITE or SEND:
`Mail.ReadWrite` (modify mailbox items), `Mail.Send` and `SMTP.Send` (send mail AS the connected
user), plus `Calendars.ReadWrite` (create and change calendar events). A reasonable person reading
the words "email and calendar sync" would not expect send-as. **Kam should know that before he
decides, because it is the part the label hides.**

**The reassuring half, stated with its evidence rather than as comfort:** the permissions appear to
be **delegated**, not application-level — so Attio reaches a mailbox only after that person signs in
and connects it themselves. Admin consent removes the "Need admin approval" prompt for the tenant;
on this reading it does not hand Attio every mailbox in Datasec. **The evidence and its limits are
in section 3, and there is a real gap there Kam should see before relying on it.**

---

## 1. EVERY PERMISSION REQUESTED, BY EXACT SCOPE NAME

| # | Scope, verbatim | What it actually reads or does | Bodies? |
|---|---|---|---|
| 1 | `openid` | Sign-in. Confirms who the user is. | No |
| 2 | `profile` | Basic profile — name, display name, tenant. | No |
| 3 | `offline_access` | **A refresh token: access continues without the user being present.** Access persists until revoked, not until they close the tab. | No |
| 4 | `https://graph.microsoft.com/User.Read` | The signed-in user's own profile. | No |
| 5 | `https://graph.microsoft.com/Mail.Read` | **Read mail in the user's mailbox — full messages, bodies and attachments included.** | **YES** |
| 6 | `https://graph.microsoft.com/Mail.ReadWrite` | Read AND modify: create, update, move, delete mail items. Supersedes #5. | **YES** |
| 7 | `https://graph.microsoft.com/Calendars.ReadWrite` | Read and WRITE calendar events — create, amend, delete. | n/a |
| 8 | `https://graph.microsoft.com/Mail.Send` | **Send mail as the user.** Recipients see it from them. | n/a |
| 9 | `https://outlook.office.com/SMTP.Send` | Same, over SMTP — a second send path, on the Outlook resource rather than Graph. | n/a |

Seven distinct permissions plus the two OIDC sign-in scopes.

**Two things worth pointing at rather than leaving in the table.** `Mail.ReadWrite` makes `Mail.Read`
redundant — requesting both is normal but means the effective grant is the larger one. And
`offline_access` is what turns this from a session into standing access: Attio holds a refresh token
and keeps working with no one watching, until someone revokes it.

## 2. WHAT ATTIO DOES WITH IT, from Attio's own documentation
- **Only Inbox and Sent folders sync** on Microsoft 365 (Gmail syncs everything undeleted).
- **Microsoft 365 shared inboxes cannot be synced.**
- **Private calendar events are not synced.**
- **Bodies are stored, and default to private to the individual.** Attio's wording: it "defaults to
  sharing metadata (timestamps and participants) and subject lines with your team", internal emails
  and calendar events are hidden from colleagues on internal domains by default, and bodies "remain
  private unless you choose to share them."

**Read the last one carefully, because it is the easiest thing in this report to misread.** That is a
**sharing** default inside Attio's UI — a product setting, changeable, and not a limit on what was
collected. The body was still read, transmitted and stored on Attio's side. "Private to the team" and
"not collected" are different facts, and only the first one is true here.

## 3. DELEGATED OR APPLICATION-LEVEL, AND WHOSE MAILBOXES — the reasoning, and the gap in it
**Delegated, on the evidence available. Three independent indications:**
1. `openid`, `profile` and `offline_access` are **delegated-only** scopes. Application permissions
   never carry them. Their presence dates the whole set as a user-sign-in flow.
2. The permissions are passed as individual resource-scoped strings. Application permissions on the
   v2.0 endpoint are requested as `.default`, not enumerated this way.
3. The redirect lands on `app.attio.com/integrations/mailbox/exchange/auth/response` — a per-user
   mailbox connect callback, not a service-to-service one.

**So on this reading: admin consent pre-approves Attio for the tenant so individual users stop hitting
"Need admin approval". Each mailbox still reaches Attio only when its owner connects it. It is not a
tenant-wide mailbox grant.**

**Now the gap, and it is the reason this is a report and not a recommendation.** Microsoft's v2.0
`/adminconsent` endpoint grants **the permissions registered on the application**, which are not
necessarily only the ones written into the URL. **If Attio's app registration also declares
application-level permissions, the same consent would grant those too, and this report would not
know.** I cannot rule it in or out — see the next section for why.

**The authority on this question is the consent screen itself.** When Kam opens it, Microsoft renders
the actual list, and **application-level permissions are labelled distinctly there** — typically
"without a signed-in user" / "Read mail in all mailboxes". **If any line says "all mailboxes", the
delegated reading above is wrong and he should not proceed.** That single check costs him ten
seconds and is worth more than this entire table.

## 4. WHAT I COULD NOT ESTABLISH — unmeasured, not assumed benign
1. **The definitive scope list as Microsoft will render it in Datasec's tenant.** Everything in
   section 1 is **Attio's published documentation** — the vendor's account of its own connector. It
   is not the app registration and not the consent screen. **Named as vendor-documented, not verified.**
2. **Whether the app declares application-level permissions on top.** Section 3's gap. Unmeasured.
3. **Whether client id `285a2b1b-e59e-4db2-a862-e0d06751e637` is genuinely Attio's.** Vendor-published;
   I did not verify it against the Microsoft directory. Kam will see the publisher name on the consent
   screen, which is a better check than anything I could have run.
4. **Attio's data retention after disconnection** — whether stored bodies are deleted when a mailbox
   is disconnected. Not documented in what I read. **This is a question for the security pack, and it
   is the one I would most want answered before consenting.**

**Why these are unmeasured rather than measured — the honest reason, not an excuse.** Two lanes were
shut, and I did not work around either:
- **Entra.** The Attio enterprise app would live in Datasec's **corporate** tenant
  `ae7a1e46-02d7-4035-9a3f-dc6d9e172217` — per the workspace's own record, the mailbox tenant. This
  seat authenticates as a service principal in a **different** tenant
  (`d500ebad-cf53-4f2a-a501-f831289e67fc`, sub `0c57ab37…`), confined to Vision's resource groups.
  **I hold no identity in the corporate tenant and did not seek one.**
- **The Attio browser lane is CLOSED today.** `app.attio.com/datasec/settings/personal/email-calendar`
  redirected to `/auth/sign-in`. It was open on 2026-08-24, so this is a change, not a constant — I
  fingerprinted it rather than assuming either way. **Signing in as Kam was available and I did not
  do it.** So Attio's in-product consent copy is also unread.

## 5. WHERE THE CONSENT IS GRANTED — named, NOT pre-filled and NOT triggered
Two places. **Nothing below has been opened, assembled with real values, or clicked.**

**(a) The tenant-wide grant — the one this ruling is actually about.** Either:
- **Entra admin centre → Enterprise applications → Attio → Security/Permissions → "Grant admin
  consent for Datasec".** *Recommended: it involves no hand-built URL, and it shows the permission
  list before anything is granted.* Or
- Attio's documented admin-consent URL, **left as the template it ships as**:
  `https://login.microsoftonline.com/{{TENANT_ID}}/v2.0/adminconsent?client_id=285a2b1b-e59e-4db2-a862-e0d06751e637&scope=<the scopes in section 1>&redirect_uri=https%3A%2F%2Fapp.attio.com%2Fintegrations%2Fmailbox%2Fexchange%2Fauth%2Fresponse`
  **`{{TENANT_ID}}` is deliberately left unsubstituted.** The value it wants is the corporate tenant
  id in section 4. I have not assembled the two into a working link — a ready-to-click consent URL is
  a pre-filled consent prompt, which is the one thing his ruling ruled out.

**(b) The per-user connect** — `app.attio.com` → personal settings → Email & calendar → connect
Microsoft. Without (a) this is where a user meets "Need admin approval".

## 6. WHAT UNBLOCKS IF HE GRANTS, so the trade is visible on both sides
The not-contacted signal stops being blind. Today it reports **records not edited** — a deal phoned
yesterday still appears on it, which is why this morning's digest put a warning above the number
instead of under it. With correspondence data it answers the question actually asked: *has this
customer heard from us?* That is 12 of the 14 items in today's digest becoming trustworthy.

**That is the value. Section 1 is the price. Both belong in front of him, and the decision is his.**

## 7. WHAT I DID NOT DO
No consent granted. No consent requested. No permission prompt opened or pre-filled. No tenant
change. No sign-in as Kam. No contact with Attio or any other human.

PROVENANCE:
- The nine scope strings, the client id and the consent URL template | Attio Help Centre, "Connect Microsoft Entra ID for email and calendar sync" | read 2026-09-07 | VENDOR DOCUMENTATION, not the app registration
- Folders synced, shared-inbox and private-event exclusions, and the body-storage and sharing defaults | Attio Help Centre, "Sync your email and calendar" | read 2026-09-07 | VENDOR DOCUMENTATION
- That Mail.Read / Mail.ReadWrite cover message bodies | Microsoft Graph permission semantics | 2026-09-07
- Delegated rather than application-level | INFERRED from three properties of the request (section 3), NOT read from the app registration — and section 3 names the case that would break it
- Whether the app also declares application permissions | NOT ESTABLISHED — no identity in the corporate tenant, and I did not seek one
- That the Attio browser lane is closed at this seat | measured 2026-09-07, app.attio.com redirected to /auth/sign-in | contradicts the 2026-08-24 state
- Attio's retention of bodies after disconnection | NOT ESTABLISHED — absent from the documentation I read

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07

— Datasec/Vision_Sales_Portal (s10)

