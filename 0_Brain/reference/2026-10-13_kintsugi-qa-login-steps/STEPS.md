# Create the Kintsugi QA login (ORG_ADMIN) — step by step for Kam

**Secuura / Blockchain · Kintsugi.** Prepared by Wednesday, 2026-10-13, after your live-board note (09:57:02: "please provide a step by step with links and right privileges. I will do now"). Read the **VERIFIED / NOT VERIFIED** box before you start: I read the code and checked the site answers, but I did **not** log in to Kintsugi or create anything (that is yours; I am read-only there).

## What you are making, and why
- One login with role **ORG_ADMIN**, belonging to an organisation that has API keys on Kintsugi.
- Why this role: the key-list route refuses the existing QA login (role OWNER) with 403 (V measured that). ORG_ADMIN and ISSUER_ADMIN are the two roles bounded to their own organisation (`packages/shared/src/security/keyRevokePolicy.ts`), which is exactly what the live checks need. ORG_ADMIN is the safer of the two to create (it cannot be a platform admin).
- Nothing the checks do changes data.

## Links (verified to answer)
- Admin Dashboard: **https://kintsugi.secuura.net/admin/** (HTTP 200 when I checked).
- API base: **https://kintsugi.secuura.net/api** (the exact login route is in step 3).

## VERIFIED (read in the code, develop b28bfaec) / NOT VERIFIED
- VERIFIED in code: `POST /api/users/admin/create` creates a user with a role you choose, needs a **logged-in ORG_ADMIN or SYSTEM_ADMIN** (an OWNER gets 403), takes `email`, `password`, `firstName`, `lastName`, `role`; a tenant admin creates the user inside its own tenant.
- VERIFIED in code: `POST /api/auth/register` (the public sign-up) **always makes an OWNER and rejects a `role` field**. So you cannot make an ORG_ADMIN through public sign-up.
- VERIFIED in code: the Admin Dashboard **Users page** has an "Administrators" category (ORG_ADMIN, SYSTEM_ADMIN) with a create form, **but** the form calls the public `/api/auth/register` with a `role` and a **random password it never shows you**. I believe that path is broken for admins (register rejects `role`), and even if it worked you would not know the password. **Do not use the Users page to make this login.**
- NOT VERIFIED: the exact JSON shape of the login response (I say "copy the access token"); the password-strength rule beyond "at least 8 characters" (use 20+ characters, upper, lower, digit, symbol); whether `admin/create` lets you set the organisation directly (it does not take `organizationId` in the create payload I read; step 5 sets it afterwards with the admin update route, whose payload in the Users page carries `organizationId`); that your own account on Kintsugi is ORG_ADMIN or SYSTEM_ADMIN.
- I asked **V 6th** to run the same steps against its own local copy of the service and mail me any correction; I will post a second message here if it changes anything.

## Steps
1. **You need an admin session.** Sign in at https://kintsugi.secuura.net/admin/ with *your* platform-admin (SYSTEM_ADMIN) or an ORG_ADMIN account. If you have neither on Kintsugi, stop and tell me: then the fallback is option (c) on the card (the deploy seat inserts one row) and I will plan it.
2. **Pick the organisation.** In the Admin Dashboard open **Organizations** and copy the **id (a UUID)** of an organisation that has API keys (the one the connector registrations use is best). The test login will be bounded to this one organisation.
3. **Get a token for the API calls.** Easiest: in the same browser, with the Admin Dashboard open, open Developer Tools → Network, click any page, and copy the `Authorization: Bearer …` value from a request to `/api/...`. (If you prefer curl: `POST https://kintsugi.secuura.net/api/auth/login` with `{"email":…,"password":…}`; the token is in the response.) Treat the token as a password: do not paste it anywhere but your own terminal.
4. **Create the user** (in a terminal; replace the four placeholders; pick a strong password and keep it):
   ```
   curl -s -X POST https://kintsugi.secuura.net/api/users/admin/create \
     -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
     -d '{"email":"<qa-orgadmin@your-domain>","password":"<20+ chars, mixed>","firstName":"QA","lastName":"OrgAdmin","role":"ORG_ADMIN"}'
   ```
   Expected: a JSON success with the new user's `id`. If you get 403, your session is not ORG_ADMIN/SYSTEM_ADMIN; if 400 "Invalid role", tell me the exact text.
5. **Put the user in the organisation** (use the `id` from step 4 and the organisation UUID from step 2):
   ```
   curl -s -X PATCH https://kintsugi.secuura.net/api/users/admin/<USER_ID> \
     -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
     -d '{"organizationId":"<ORG_UUID>"}'
   ```
   (If this is refused, send me the error text; that is the NOT-VERIFIED part.)
6. **Save the login for the seats.** Open `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` and add two lines (the file is git-ignored; never commit it):
   ```
   KINTSUGI_QA_ORGADMIN_EMAIL=<the email>
   KINTSUGI_QA_ORGADMIN_PASSWORD=<the password>
   ```
   The existing `KINTSUGI_QA_GATE_OWNER_EMAIL` / `…_PASSWORD` stay as they are. I never read the values; the seats read them from the file.
7. **Check it yourself (optional, 30 seconds):** log in as the new user (step 3 with its email and password), then
   ```
   curl -s "https://kintsugi.secuura.net/api/keys?organizationId=<ORG_UUID>" -H "Authorization: Bearer <NEW_TOKEN>"
   ```
   Expected: **200** with that organisation's keys. The existing OWNER QA login returns **403** here; a 200 is the proof the new role works.
8. **Tell me "done"** on the panel. I then mark the card delivered and the verify-and-close tickets proceed.

## One more thing the checks need (separate, not this login)
KS-1470's live check needs one **valid connector key** (yours to supply). Say when you have it and where you put it; same rule: in the credentials file, never in a message.

## If something is refused
Send me the exact status and message text. I will not guess a workaround on Kintsugi and I will not use any other identity.
