# KS residue decision cards (DRAFTS for Wednesday; nothing posted). 2026-11-04
Client_project for all: Secuura/Blockchain. Linear read-only via GraphQL; ruled-queue read via decision_queue.sh.

## ALREADY RULED (no card drafted)
- KS-1223: ALREADY RULED: secuura-ks1223-referrer-wallet-source-1013 = a (build a trusted source, stop reading the header), 2026-10-13T09:50; delivered as #1534/#1536, merged. Ticket comment 63820e71 (11-02) says "no ruling recorded"; the queue has one. Wednesday should post that link and close.
- KS-1561: ALREADY RULED: secuura-ks1561-duplicate-hash-certifier-1102 = a (certify only for the org holding the original registration), 2026-11-02T12:44. The ticket description still says "NO BUILD"; it needs the ruling recorded and a build brief.

---
## CARD 1
id: secuura-ks1202-live-leg-issuer-login-1104
client_project: Secuura/Blockchain
title: KS-1202: the last live check needs an issuer login on the shared kintsugi box. Create one, or close without it?
bluf: Kam, the fix (a mismatched document type is refused with 400) is merged and in the 2026-11-01 deploy (KS-1202 comment 48bf06fd). The one check not run is a live try on kintsugi, because the only login held there is role OWNER, which cannot create documents (comment b5983ec5). The code and the deployed build were checked equal (b5983ec5, sha256 match). Kintsugi is a shared dev box Stuart's team also uses, so a new account is visible to them.
options:
  a: Create a throwaway issuer test account on kintsugi — a Secuura seat runs the live try, you approve the account; Stuart's team shares the box.
  b: Accept in-process and deployed-build evidence and close — Wednesday posts your acceptance on the ticket and moves it to Done.
  c: Leave open — nothing runs, the ticket stays In Progress.
recommended: b — the guard is read at documents.ts:613-618, tests are red without it, and the deployed file matches byte for byte; a shared-box account adds little.
default_action: After 48 h nothing changes (c); Wednesday re-raises it in the morning receipt. No seat touches kintsugi.
SOURCES: KS-1202 description; comments b5983ec5 (10-12), 48bf06fd (11-02); decision_queue ruled list (secuura-served-documenttype-unchecked-n1 and ks1202-build = earlier, different questions).

---
## CARD 2
id: secuura-ks1215-live-connector-key-1104
client_project: Secuura/Blockchain
title: KS-1215: close without the last live check, or supply a throwaway connector key on kintsugi?
bluf: Kam, the fix (the caller's login token is dropped when a connector key is used) is merged and deployed (KS-1215 comment 4dd630e2, auth.ts:455-463). The remaining check needs a valid connector key on kintsugi; the author's key was refused there with 401 (comment 7ce03e19). The case "valid key whose token exchange fails" cannot be made to happen live (7ce03e19). Four real post-deploy mints all succeeded (7ce03e19). A key on kintsugi touches the shared box Stuart's team also uses.
options:
  a: Supply a throwaway kintsugi connector key — a seat sends one request; still cannot induce the failing exchange; shared box.
  b: Accept in-process evidence plus the four post-deploy mints and close — Wednesday posts your acceptance and moves it to Done.
  c: Leave open.
recommended: b — the live key would not even reach the failing case; the in-process cells (41/41, red when reversed) cover it.
default_action: After 48 h nothing changes (c); Wednesday re-raises it. No key is requested.
SOURCES: KS-1215 description; comments 11ca0342, 7ce03e19, 4dd630e2.

---
## CARD 4
id: secuura-ks1234-production-307-1104
client_project: Secuura/Blockchain
title: KS-1234: pin the production-mode 307 with a test, or accept it in writing?
bluf: Kam, the hanging JSON create is fixed and checked live on kintsugi (KS-1234 comment 1781f579, 401 in 0.55 s). The second symptom, a 307 on /api/documents when NODE_ENV=production, cannot be checked on kintsugi because it runs non-production (1781f579). No test pins it in production mode; the existing test boots only the test mode (1781f579, f0fb93b8).
options:
  a: Build a production-mode regression test — a Secuura seat adds one cell on the real gateway app under NODE_ENV=production; small build.
  b: Accept the by-design 307 in writing and close — Wednesday posts your sentence on the ticket and moves it to Done.
recommended: a — it is a cheap cell, and "no test pins production" is exactly how this ticket stayed open.
default_action: After 48 h nothing changes; ticket stays open and Wednesday re-raises it.
SOURCES: KS-1234 description; comments 1781f579, f0fb93b8.

---
## CARD 5
id: secuura-ks1244-repeated-api-key-1104
client_project: Secuura/Blockchain
title: KS-1244: reject a repeated x-api-key outright, or accept the fall-through to anonymous?
bluf: Kam, sending two x-api-key headers makes the key fail and the request fall through to the anonymous login principal, which a public (optional) route answers 200 (KS-1244 description). Merged work only added tests pinning today's behaviour; no product file changed (comment 000af088). On required routes it already answers 401, checked live on kintsugi with junk keys (000af088). The ticket was filed High as an authentication-bypass shape; nobody has ruled on the fall-through.
options:
  a: Build outright rejection — a seat makes a repeated x-api-key a 400/401 on every route; touches the KS-1207 design.
  b: Accept the fall-through in writing and close — it only reaches routes already open to anonymous callers; Wednesday posts your acceptance.
recommended: a — the description asks for it and a refused request is clearer than a silent downgrade.
default_action: After 48 h nothing changes; ticket stays open, Wednesday re-raises it.
SOURCES: KS-1244 description; comment 000af088 (only comment).

---
## CARD 6
id: secuura-ks1233-redis-ttl-read-1104
client_project: Secuura/Blockchain
title: KS-1233: who reads the Redis key's remaining life on kintsugi, which answers NOAUTH?
bluf: Kam, the fix (platform settings are saved with no expiry in Redis) is merged and deployed (KS-1233 comment c1ab228a, redis.ts:683-684). The merge comment (31f1cd26) owes a one-line read of that key's TTL on each environment's Redis, to be sure the old 24 h expiry is gone. No seat holds the Redis password, so the read cannot run (c1ab228a). Giving seats a Redis credential touches the shared kintsugi box Stuart's team also uses.
options:
  a: Read-only Redis credential for seats — one-off read now; adds a standing credential on the shared box.
  b: The next deploy seat runs the read — no new credential; waits for the next kintsugi deploy.
  c: Leave open.
recommended: b — the owner of the deploy already holds access, and the code read shows no TTL is set.
default_action: After 48 h nothing changes (c); Wednesday adds the read to the next deploy brief anyway.
SOURCES: KS-1233 description; comments 31f1cd26, c1ab228a.

---
## CARD 7
id: secuura-ks769-close-keep-owner-1104
client_project: Secuura/Blockchain
title: KS-769: close it and move the 2027-01-01 expiry to a dated review ticket, or keep it open?
bluf: Kam, you ruled the mobile app tree "dormant but kept" on 2026-09-17 (queue card secuura-ks769-mobile-tree-fuse-lapsed-blocks-pushes = dormant; KS-769 comment bb69813e). The exclusion is in lock-discovery.mjs as owned by KS-769 and lapses 2027-01-01 (comment 8cd04443). If KS-769 closes, nobody owns that expiry; if it stays open, it sits In Progress for two months doing nothing.
options:
  a: Close KS-769 and open a new review ticket dated before 2027-01-01; the exclusion row points to it — a Secuura seat edits one row.
  b: Keep KS-769 open as owner until January.
recommended: a — your ruling is implemented; a dated ticket is an honest owner, an open one is noise.
default_action: After 48 h nothing changes (b); Wednesday re-raises it before December.
SOURCES: KS-769 comments bb69813e, d27a0581, 8cd04443; queue ruling above.

---
## CARD 9
id: secuura-ks1624-url-interior-slashes-1104
client_project: Secuura/Blockchain
title: KS-1624: if SECUURA_API_URL is badly formed, should the WhatsApp bot refuse to start, or carry on?
bluf: Kam, the WhatsApp bot builds its API address by gluing strings, so a base with a double slash inside (or a "?" query) makes an odd address; nothing changes the host and the gate found no security issue (KS-1624 description). F1 (banner) is merged (comment ceba48f7). F2 and F3 are marked "needs a ruling" (description). The proposed fix is to parse the address and refuse to start if it is malformed.
options:
  a: Normalise: parse with new URL and refuse at startup on a bad value — a seat builds it; a misconfigured deploy now fails loudly.
  b: Accept as configured — Wednesday posts the acceptance on the ticket and closes F2/F3.
recommended: b — operator misconfiguration only, no new host reachable, and a startup refusal can break a live deploy.
default_action: After 48 h nothing changes; ticket stays open with F2/F3 unruled.
SOURCES: KS-1624 description (F2/F3 section); comments b250bdd4, ceba48f7.

---
## CARD 10
id: secuura-ks1639-api-key-text-forms-1104
client_project: Secuura/Blockchain
title: KS-1639: should the API-key reader refuse a non-boolean "active" value loudly, or keep accepting text?
bluf: Kam, the bug (the text 'f' read as an active key) is fixed and merged as #1631; strings now read active only for 't' or 'true' (KS-1639 comment 6138fb4a). It cannot happen today because the column is a true/false type (description). What remains is the design call: keep accepting text forms, or refuse any non-boolean with an error (comment 6138fb4a; description calls refusal the safer contract). No live check is possible, so this ticket needs your call to close (6138fb4a).
options:
  a: Keep accepting text, as merged, and close — no further build.
  b: Refuse any non-boolean loudly — a seat builds it with cells; a bad row stops the request instead of reading inactive.
  c: Leave open.
recommended: a — the merged rule already fails safe (anything unclear reads inactive), and the bad input cannot arrive.
default_action: After 48 h nothing changes (c); Wednesday lists it again.
SOURCES: KS-1639 description; comments 6138fb4a, 8bdcee40 (id only, not read in full).

---
## CARD 11 (GROUP)
id: secuura-ks-residue-disposable-stack-1104
client_project: Secuura/Blockchain
title: Many KS tickets wait on live checks that cannot run safely on kintsugi. Build a disposable copy of the stack to run them?
bluf: Kam, 32 In-Progress KS tickets stay open only because the owed live check needs a fault switch, writes, real mail, or credentials seats do not hold: 27 are NEEDS-DISPOSABLE-STACK and 5 CANNOT-RUN-SAFELY (residue.tsv, grep count 32). The classes come from keywords, so about 10-15% are probably misfiled. Your 2026-10-12 rule is Done = fully tested + works + deployed. Today these sit open or get closed on code evidence alone.
options:
  a: Wednesday commissions a disposable local copy of the stack at kintsugi's deployed commit ee1e1b832115 (seeded test logins, a connector key, a fault switch); owed checks run there; tickets that pass close with that evidence stated.
  b: Close those tickets on code evidence, with a comment saying the live check was not run.
  c: Leave them open.
recommended: a — it honours your rule without touching the shared box; cost is one build.
default_action: After 48 h nothing changes (c); Wednesday re-raises it.
SOURCES: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_ks-inprogress-residue/residue.tsv (counted by grep; header line 1); commit ee1e1b832115 taken from the brief, not verified.

---
## NOT FULLY VERIFIED
- Card 11: commit ee1e1b832115 as kintsugi's deployed commit is from the brief; tickets' own comments cite b1fb543640e7 (2026-11-01 deploy) and 69f2045af2a4 (10-07). Wednesday should confirm which before commissioning. Class counts 27/5 not re-derived beyond a grep total of 32.
- Card 10: comment 8bdcee40 not read. Options come from the description and 6138fb4a, not an explicit lettered list.
- Cards 1, 2, 6: no live read of kintsugi; claims rest on ticket comments only.
- Card 4/5/9: recommendations are mine; no code read, only ticket text.
