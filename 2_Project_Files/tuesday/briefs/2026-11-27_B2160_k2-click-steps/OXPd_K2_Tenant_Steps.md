---
title: "OXPd: the test pieces in datasec-rd.com"
subtitle: "Click steps for Kam (card datasec-oxpd-tenant-pieces-k2-1127, ruled a: Yes, by 7 Dec)"
date: "Prepared Fri 27 Nov 2026 by B2160 for Tuesday"
---

# Before you start

You sign in once, at **https://entra.microsoft.com**, as:

    kamil@datasec-rd.com

Check the tenant name in the top right corner says datasec-rd.com. If you see another tenant, use the **Settings** icon (gear) in the top bar, then **Directories + subscriptions**, and switch. (Source: https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

Microsoft renames menus often. Every path below is copied from a Microsoft Learn page opened on 27 Nov 2026; the page is named beside each part. **If a menu reads differently, type the word given in the top search box of the admin center instead.**

There are five parts. Do them in order. Part 5 is what you send back.

Licences are not in this document. The test user needs the licence from card D2 before the app tests, not before these steps.

Nothing in these steps creates a password or secret that you paste anywhere. If a screen shows you one, keep it to yourself.

# Part 1. The test user

Source for 1.1 to 1.5: https://learn.microsoft.com/en-us/entra/fundamentals/how-to-create-delete-users

**1.1** In the left menu, go to **Entra ID**, then **Users**. (Search box: *Users*.)

**1.2** Select **New user**, then **Create new user**.

**1.3** On the **Basics** tab, type the user name below in **User principal name**, and pick datasec-rd.com from the menu after the @ sign:

    oxpd.test

**1.4** In **Display name**, type:

    OXPd Test User

Leave **Auto-generate password** ticked and **Account enabled** ticked. Copy the password shown into your own password manager. Do not send it to Tuesday.

**1.5** Select **Next: Properties**. Under **Settings**, set the location to Australia (the licence of card D2 needs it later). Then select **Review + create**, then **Create**.

**1.6** Register Microsoft Authenticator for this user. On your phone, install **Microsoft Authenticator** if it is not there. On the Mac, open a private browser window and go to:

    https://mysignins.microsoft.com/security-info

Sign in as oxpd.test@datasec-rd.com with the password from 1.4, set a new password when asked (keep it in your password manager), then add **Microsoft Authenticator** as a sign-in method and follow the screens on the phone until the test notification is approved. (Source: https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-userdevicesettings, which names "My Sign Ins | Security info" at that address as where users add their own methods. The screens after "add" are Microsoft's own and were not copied here.)

**1.7** Check: back in the admin center, **Entra ID**, **Users**, select OXPd Test User, then **Authentication methods**. Microsoft Authenticator is listed. (Same source as 1.6.)

What the tests need this user for: the first printer test (C-76) is "one plain page on the older panel starts Microsoft's sign-in"; it "needs a test tenant user from you". Your w7 answer (C-80) is "we build against kamil@datasec-rd.com". This user is that test user, inside that tenant.

# Part 2. The app registration

Your 18 Nov ruling (card q06, C-25): reuse the existing HP Authentication Manager registration. So first look for it.

**2.1** Go to **Entra ID**, then **App registrations**, then the **All applications** tab. (Source: https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/grant-admin-consent)

**2.2** In the search box, type each of these in turn. These are the names the HP documentation uses for the registration (project analysis A6, lines 288 and 368):

    HP Authentication Manager

    HP Authentication Suite

Also look for "HP Authentication Manager - Azure Only".

**2.3** One found? Go to **Branch A** (2.A1). None found? Go to **Branch B** (2.B1). More than one found? Stop, and tell Tuesday the names you see.

## Branch A: the existing registration is there (your q06 ruling)

Do not rename it, do not delete or change any secret or certificate on it, and do not change **Allow public client flows**. Workpath printers may already use it.

**2.A1** Select it. On its **Overview** page, write down the **Application (client) ID** and the **Directory (tenant) ID**. (Source: https://learn.microsoft.com/en-us/entra/identity-platform/scenario-desktop-app-configuration)

**2.A2** Add the server's web return address. Under **Manage**, select **Authentication**. On the **Redirect URI configuration** tab select **Add Redirect URI** (older screens: **Add a platform**), choose the **Web** tile, type the address below, and select **Configure**. (Source: https://learn.microsoft.com/en-us/entra/identity-platform/how-to-add-redirect-uri)

    Tuesday will send this value (OPEN VALUE 1)

Why: the design's Option A (02 section 7.1, line 726) is "Add a **Web** platform redirect URI on the server's FQDN for the panel sign-in". The server's address is not decided yet. If the address has not arrived, skip 2.A2 and do the rest; it can be added later.

**2.A3** Go to Part 3.

## Branch B: no HP registration in this tenant, so make a test one

**2.B1** Go to **Entra ID**, then **App registrations**, and select **New registration**. (Source: https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

**2.B2** In **Name**, type:

    OXPd Test Server

**2.B3** Under **Supported account types**, choose **Single tenant only - datasec-rd.com** (older screens: "Accounts in this organizational directory only"). The HP registration is single tenant too (A6 line 288).

**2.B4** Leave **Redirect URI** empty. Select **Register**.

**2.B5** On the **Overview** page, write down the **Application (client) ID** and the **Directory (tenant) ID**. (Source: https://learn.microsoft.com/en-us/entra/identity-platform/scenario-desktop-app-configuration)

**2.B6** Add the web return address exactly as step 2.A2 says (the value is OPEN VALUE 1).

**2.B7** **Allow public client flows.** Under **Manage**, select **Authentication**; under **Advanced settings**, **Allow public client flows** is a Yes/No switch, then **Save**. (Source: https://learn.microsoft.com/en-us/entra/identity-platform/scenario-desktop-app-configuration, which says Yes is what device code sign-in needs.) Set it to:

    Tuesday will send this value (OPEN VALUE 2)

Why open: the plan builds device code as a fallback (B2154 lane L2), but the design says keeping public client flows "hang[s] on N-3" (02 line 726), and N-3 is not decided. Until the value arrives, leave it as the screen shows it.

**2.B8** Go to Part 3.

## Both branches: do NOT make a client secret now

The server will need its own credential on this registration (02 line 726; the design prefers a certificate, 02 line 690). Do not make one today. Tuesday sends you a separate secure step for it later, and it never goes on the board.

# Part 3. The card store: the attribute set and the two roles

The card store keeps card records in Entra custom security attributes. The design names the attribute set and the attribute (02 section 7.4, line 756: "CSA attribute set `HPAuthenticationSuite`, `cardId` blob"; also F6, line 70).

Microsoft's warning: Global Administrator does **not** have rights to custom security attributes by default. You give yourself the two roles first. (Source: https://learn.microsoft.com/en-us/entra/fundamentals/custom-security-attributes-add)

**3.1** Give yourself the two roles. Go to **Entra ID**, then **Roles & admins** (Learn's tenant-scope steps also show it as **Identity**, then **Roles & admins**). Select the role name (click the name; do not tick its box), then **Add assignments**, pick kamil@datasec-rd.com, then **Add**. Do it for each role: (Source: https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/manage-roles-portal)

    Attribute Definition Administrator

    Attribute Assignment Administrator

If your screen asks "Eligible" or "Active", choose Active (your tenant then has Privileged Identity Management; Learn's PIM note, same page).

**3.2** Sign out of the admin center and sign in again, so the new roles take effect.

**3.3** Add the attribute set. Go to **Entra ID**, then **Custom security attributes**, then **Add attribute set**. (Source: https://learn.microsoft.com/en-us/entra/fundamentals/custom-security-attributes-add) If **Add attribute set** is greyed out, the role from 3.1 has not taken effect yet; wait a few minutes and sign in again.

Type the name exactly as below. It is case sensitive, has no spaces, and **can never be renamed or deleted**:

    HPAuthenticationSuite

Description:

    HP Authentication Suite card store (OXPd test)

Maximum number of attributes:

    500

(500 is what the existing HP software uses when it makes this set itself: analysis A1, line 185.) Select **Add**.

**3.4** Add the card attribute. Open the set **HPAuthenticationSuite**, select **Add attribute**, and fill in: (Source: same page)

Attribute name (exact, case sensitive; it **can never be renamed or deleted**, only deactivated):

    cardId

Description:

    Card records (OXPd test)

**Data type**: String. **Allow multiple values to be assigned**: Yes. **Only allow predefined values to be assigned**: No. Select **Save**.

(These settings match the HP software: "`cardId` | collection of string, max 15 per user", A1 line 189.) Check the four fields twice before **Save**.

Do not add the set's other attributes (`refreshToken`, `UPAR`, 02 lines 757-758). The HP software makes those itself when first used (A1 line 185: "definitions created on demand").

**3.5** Give the same two roles to the app registration from Part 2. Repeat step 3.1 for each role, but in **Add assignments** search for the app's name (the HP name from 2.2, or OXPd Test Server) instead of your own. This is what the design asks: "directory roles Attribute Assignment Administrator and Attribute Definition Administrator on the service principal" (02 section 7.2, line 740), and what the HP setup guide does (A6 line 294). In Branch A the app may already hold both roles; if so, there is nothing to do.

If the app's name does not appear in the picker, stop and tell Tuesday; Learn shows a PowerShell way to assign a role to an app's service principal (same page as 3.1), and Tuesday will send it.

**3.6** App permissions for the card store: **leave for now.** The design lists three app-only Graph permissions for the card store but marks the names as "inferred" (02 line 740: `User.Read.All`, `CustomSecAttributeAssignment.ReadWrite.All`, `CustomSecAttributeDefinition.ReadWrite.All`), and the HP documentation shows only the two roles (A6 line 364). Whether you add them is OPEN VALUE 3; Tuesday will tell you.

# Part 4. Admin consent to the permissions of all five apps

Source for 4.1 to 4.4: https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis

**4.1** Open the app registration from Part 2 (**Entra ID**, **App registrations**, **All applications**, select it). Select **API permissions**.

**4.2** **Branch A only: before you change anything, note every permission already listed there.** Microsoft warns that granting admin consent "may revoke permissions that have already been granted tenant-wide for that application" (https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/grant-admin-consent). Do not remove any permission that is already listed.

**4.3** Select **Add a permission**, then **Microsoft Graph**, then **Delegated permissions**. Tick each of these 13 that is not already listed (use the search box), then **Add permissions**:

    openid
    profile
    offline_access
    email
    User.Read
    Mail.ReadWrite
    Mail.Send
    People.Read
    Team.ReadBasic.All
    Channel.ReadBasic.All
    ChannelMessage.Send
    Files.ReadWrite.All
    Sites.ReadWrite.All

These are the 13 the HP documentation gives customers: "There are 13 Permissions: Which covers all HP Authentication Suite of apps, excluding permissions required for Universal Print" (CLARIFICATIONS, the W11 / T-08 answer, line 1024). They match the design's per-app table (02 section 7.2, lines 740-743): sign-in hub, Mailflow, Teams, OneDrive and SharePoint.

**4.4** Select **Grant admin consent for datasec-rd.com**, then **Yes**. Select **Refresh**. Every line now shows **Granted for datasec-rd.com** under **Status**. (Source: 4.1's page, and https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)

**4.5** **Universal Print (the fifth app).** Nothing to tick here today. You chose a separate test registration for Universal Print on card D4 (not Datasec's own "Universal Print for HP Authentication Manager" app), so its registration, the Printer Administrator role and the print share come in a separate set of steps from Tuesday (OPEN VALUE 4).

## Card D3 (you picked a: agents create them): extra APPLICATION permissions

You picked a on card D3, so agents make the Teams team, the SharePoint library and the sample mail by Graph, and need these. These are tenant-wide powers: the app could act on any user's mail and files, not only the test user's. Add them to the same registration, use them for the set-up, and Tuesday will tell you when to remove them.

Add them with **Add a permission**, **Microsoft Graph**, **Application permissions** (source: https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis), then **Grant admin consent for datasec-rd.com** as in 4.4. Granting application permissions needs Privileged Role Administrator or higher (https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/grant-admin-consent); a Global Administrator has it.

    Team.Create
    Sites.Manage.All
    Files.ReadWrite.All
    Mail.Send

What each one is for (each from its Microsoft Graph page, least-privileged application permission):

| Permission | Lets agents | Source |
|---|---|---|
| `Team.Create` | make the Teams team, with the test user as a member; a team comes with its own SharePoint site and a General channel | https://learn.microsoft.com/en-us/graph/api/team-post |
| `Sites.Manage.All` | make the document library in that site and add the five column types | https://learn.microsoft.com/en-us/graph/api/list-create and https://learn.microsoft.com/en-us/graph/api/list-post-columns |
| `Files.ReadWrite.All` | put sample files into the library and OneDrive | https://learn.microsoft.com/en-us/graph/api/driveitem-put-content |
| `Mail.Send` | send the test user some mail with attachments | https://learn.microsoft.com/en-us/graph/api/user-sendmail |

Two more only if Tuesday asks (OPEN VALUE 5): `TeamMember.ReadWriteNonOwnerRole.All` adds people to the team after it is made (https://learn.microsoft.com/en-us/graph/api/team-post-members); `Sites.Create.All` makes a SharePoint site separate from the team's, through a beta Graph call (https://learn.microsoft.com/en-us/graph/api/site-post-sites?view=graph-rest-beta).

# Part 5. What you send back to Tuesday

Reply on the board with these lines, filled in:

    Branch: A (existing HP registration) or B (OXPd Test Server)
    Registration name:
    Directory (tenant) ID:
    Application (client) ID:
    Test user: oxpd.test@datasec-rd.com, Authenticator registered: yes/no
    Attribute set HPAuthenticationSuite and attribute cardId made: yes/no
    Both attribute roles on me and on the app: yes/no
    Admin consent to the 13 granted: yes/no
    Web return address added (OPEN VALUE 1): yes/no/waiting
    Card D3 application permissions added: yes/no
    Anything a screen showed differently from these steps:

The tenant ID and client ID are not secrets; they are fine on the board.

**Never send:** the test user's password, or any client secret or certificate. If a secret is ever made on this registration, you do not paste it anywhere. Tuesday sends you a separate secure step for it later.

# OPEN VALUES (Tuesday sends these; do not guess them)

| # | Value | Step | Why it is open |
|---|---|---|---|
| 1 | The web return address (redirect URI) for the server's panel sign-in | 2.A2, 2.B6 | 02 line 726 says "on the server's FQDN"; the server's address and path are not decided |
| 2 | Allow public client flows: Yes or No on the test registration | 2.B7 | 02 line 726: it "hang[s] on N-3"; N-3 is not decided (B2154 L2 builds device code as a fallback) |
| 3 | Whether to add the card store's three app-only Graph permissions | 3.6 | 02 line 740 marks their names "inferred"; A6 line 364 shows only the two roles |
| 4 | The Universal Print steps: a separate test registration, the Printer Administrator role and a print share (card D4, ruled a) | 4.5 | separate steps from Tuesday; OQ-9 (02 line 734) stays open for customers |
| 5 | Whether two further D3 permissions are needed (`TeamMember.ReadWriteNonOwnerRole.All`, `Sites.Create.All`) | Part 4 box | depends on how D3's site is made; a team's own site may be enough |
| 6 | The server's credential (certificate preferred) | Part 2, last box | a separate secure step later (02 line 690) |
