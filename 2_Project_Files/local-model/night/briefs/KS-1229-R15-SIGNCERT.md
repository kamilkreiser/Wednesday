# KS-1229 R15-SIGNCERT - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 226 lines read whole)
File: `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `jest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1229-SIGNCERT_ornith35b-q4_TESTONLY-JEST-REFUSED-SIGNCERT-NO-UPSTREAM-PASS-7of7_2026-09-18.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 1959 B sha256[:16] `aa2a51bd86124fbe`, +29/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` at the tip: EXISTS (226 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/split_1229signcert/KS-1229.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1229: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1229.md.
- Generator notes: dropped 1 blank + line(s) (a blank + is refused in a modify fence); RE-ANCHORED: the old hunk appended at EOF / before a blank line; the last leading context line '});' is now the TRAILING context, so the new block lands one line UP (inside the enclosing block) - a placement change from the old READY, said here; tamper SIGNCERT: the one-line From occurs 3x at the tip; WIDENED to a 5-line block starting at :2609 (the occurrence nearest the old line 2590) - an INFERENCE by line proximity; Wednesday confirms the site.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1229 X-SIGNCERT-AFTER-UPSTREAM (TEST-ONLY, jest, originate: a refused /sign-cert must reach no upstream)
> # FILE: Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts — APPEND the block at EOF (context = the file's last three lines, 224-226 at tip 34cdcfb26). Hunk `@@ -224,3 +224,32 @@`, strict apply, no fuzzy.
> # VERDICT: Ornith PASS 7/7 FIRST sample (run 2026-09-18_ks1229-ornith35b-night4). A2 strict; A3c 28/28; A4 1 failed / 87 — the declared cell SC1, by assertion — control green; A5 87/87; A6 originate 741 -> 743, no new red; A7 tsc rc 0.
> # Source read by Wednesday: the model's 29 `+` lines IDENTICAL in sequence to the brief fence (a one-word mutated copy unequal); its three context lines equal the file's last three lines exactly (no dialect corruption this time).
> # TAMPER used to prove the red (NOT part of this diff): documents.ts:2590 — the sign-cert KS-1213 guard, LINE-PINNED because that exact guard text also sits at :1980 (/version) and :2859 (/sign-wallet), which stay untouched.
> # PR NOTES: Refs KS-1229 (NOT Closes: this is the row X-SIGNCERT-AFTER-UPSTREAM only). TIER 2 (test-only). Behaviour change: none.
> # RAISE WITH the two siblings as ONE PR — READY_KS-1229_…-RECHECK (hunk 204-209) and READY_KS-1229-LOOSE (179-184) — this one appends at EOF, so no hunk overlaps another: `Refs KS-1229 (X-ISSUE-AFTER-HOLDER, X-ISSUE-AFTER-ANCHOR, X-ISSUE-LOOSE, X-SIGNCERT-AFTER-UPSTREAM)`. Apply lowest-line-first and let later hunks take their offsets.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. This service runs JEST (ts-jest): `jest` names only, never `vi`.

## The exact change
```
@@ -224,3 +224,31 @@
     expect(await create({ data: { title: 'nb', documentType: 'DOCUMENT' } })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
   });
+describe('KS-1229 X-SIGNCERT-AFTER-UPSTREAM - a refused sign-cert reaches no upstream', () => {
+  const signCert = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-cert', { metadata });
+  it('RED KS-1229 SC1 - a refused sign-cert sends nothing to the issuer-certs upstream', async () => {
+    // KS-1229 (X-SIGNCERT-AFTER-UPSTREAM): the sign request is a real upstream call, so the refusal must come first.
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    try {
+      const r = await signCert({ documentType: 'PROPERTY_DEED' });
+      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
+    } finally {
+      stub.off('request', onUpstream);
+    }
+  }); // KS-1229 SC1
+  it('control - KS-1229 an accepted sign-cert does reach the issuer-certs upstream', async () => {
+    seed('DOCUMENT');
+    const upstreamUrls: string[] = [];
+    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
+    stub.on('request', onUpstream);
+    try {
+      const r = await signCert({ documentType: 'DOCUMENT' });
+      expect([r.status, upstreamUrls]).toEqual([201, ['/api/issuer-certs/sign']]);
+    } finally {
+      stub.off('request', onUpstream);
+    }
+  }); // KS-1229 SC control
+});
 });
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1229 SC1 - a refused sign-cert sends nothing to the issuer-certs upstream`
- `control - KS-1229 an accepted sign-cert does reach the issuer-certs upstream`  (CONTROL - green on both trees)

## Tampers
### SIGNCERT
File: `Blockchain/Dev/services/originate/src/routes/documents.ts`
Line: 2609
From:
```
      if (metadata.documentType !== undefined && metadata.documentType !== source.type) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      // 2. Call auth-service DIRECTLY (AUTH_SERVICE_URL) to sign
```
To:
```
      if (metadata.documentType !== undefined && metadata.documentType !== source.type && (await fetch((process.env.AUTH_SERVICE_URL || 'http://localhost:6003') + '/api/issuer-certs/sign', { method: 'POST' }).catch(() => null).then(() => true))) { // TAMPER: KS-1229 red-proof, the refusal is decided only after the issuer-certs sign request was sent (the gate row X-SIGNCERT-AFTER-UPSTREAM)
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'metadata.documentType must equal the source document type' } });
      }

      // 2. Call auth-service DIRECTLY (AUTH_SERVICE_URL) to sign
```
Reds: `RED KS-1229 SC1 - a refused sign-cert sends nothing to the issuer-certs upstream`
(From located at the tip: 1 match(es); block tamper of 5 lines; the old brief/input said line 2590)

## Controls
- `control - KS-1229 an accepted sign-cert does reach the issuer-certs upstream`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
