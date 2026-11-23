Secuura/Blockchain: Kintsugi round k42 is deployed and checked. No action needed.

KS-1701 is live on Kintsugi in originate, billing, vc-issuer and the gateway. Every platform-admin check now asks the one shared check, so SYSTEM_ADMIN and SUPER_ADMIN pass in any letter case. It only widens access. On Kintsugi that reaches five accounts: two system_admin users and three super_admin platform admins. That is from the code and the counts; nobody logged in to try it.

Billing and vc-issuer also picked up three older shared changes when they were rebuilt. They change nothing on Kintsugi, because it does not run in production mode.

Not shipped: KS-2316 and its follow-up. They are merged, but they live in the auth service, which stays held until Kintsugi has mail. Before any auth deploy you will get a card first: all three organisation admins and all 29 non-platform users on Kintsugi have no organisation.

Overnight board work: KS-2314 is Done; six new follow-up tickets are filed, KS-2333 to KS-2338. KS-2331 stays open, because its own test plan asks for a browser check as an organisation admin.
