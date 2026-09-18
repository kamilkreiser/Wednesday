# TO-ARMS-JEST test_only arms fixture: a NEW jest test file pinning DOCUMENT_WRITE_ROLES (originate) — never queued

File: `Blockchain/Dev/services/originate/src/__tests__/to-arms-document-write-roles.test.ts`
Tip: `8b9c3f022bee76b79a47f1b8c5de8ad3ddb4a0ae`

## The exact change

```
@@ -0,0 +1,17 @@
+import { DOCUMENT_WRITE_ROLES } from '../middleware/documentWriteRoles';
+
+// test_only tier ARMS fixture (jest runner) - never raised, never queued.
+describe('test_only arms - the document-write allow-list is pinned', () => {
+  it('lists ISSUER_ADMIN', () => {
+    expect(DOCUMENT_WRITE_ROLES).toContain('ISSUER_ADMIN');
+  });
+  it('lists SUPER_ADMIN', () => {
+    expect(DOCUMENT_WRITE_ROLES).toContain('SUPER_ADMIN');
+  });
+  it('leaves OWNER out', () => {
+    expect(DOCUMENT_WRITE_ROLES).not.toContain('OWNER');
+  });
+  it('has exactly four roles', () => {
+    expect(DOCUMENT_WRITE_ROLES).toHaveLength(4);
+  });
+});
```

## Tampers

### J1 — ISSUER_ADMIN dropped from the allow-list
File: `Blockchain/Dev/services/originate/src/middleware/documentWriteRoles.ts`
Line: 37
From:
```
export const DOCUMENT_WRITE_ROLES = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'] as const;
```
To:
```
export const DOCUMENT_WRITE_ROLES = ['ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'] as const;
```
Reds: `lists ISSUER_ADMIN`, `has exactly four roles`

### J2 — OWNER added to the allow-list
File: `Blockchain/Dev/services/originate/src/middleware/documentWriteRoles.ts`
Line: 37
From:
```
export const DOCUMENT_WRITE_ROLES = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN'] as const;
```
To:
```
export const DOCUMENT_WRITE_ROLES = ['ISSUER_ADMIN', 'ORG_ADMIN', 'SYSTEM_ADMIN', 'SUPER_ADMIN', 'OWNER'] as const;
```
Reds: `leaves OWNER out`, `has exactly four roles`

## Controls

- `lists SUPER_ADMIN`
