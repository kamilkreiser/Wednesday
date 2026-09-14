```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
new file mode 100644
index 0000000..0000000
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks871-the-audit-log-records-req-path.test.ts
@@ -1,107 +0,0 @@
+/**
+ * =============================================================================
+ * KS-871 — audit log must record the original request path, not the trimmed
+ * mount-relative remainder that express leaves behind after a `router.use`
+ * gate responds.
+ *
+ * Drives `createAuditMiddleware` in-process. The middleware writes into a
+ * captured SQL payload (via a stub `query`) so we can assert on the JSON
+ * `details.path` value without spinning up Postgres.
+ * =============================================================================
+ */
+
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+import { createAuditMiddleware } from '../middleware/audit';
+import type { Request, Response, NextFunction } from 'express';
+
+interface CapturedRow {
+  sql: string;
+  params: unknown[];
+}
+
+function buildDeps() {
+  const captured: CapturedRow[] = [];
+  const query = vi.fn(async (sql: string, params: unknown[]) => {
+    captured.push({ sql, params });
+    return { rows: [] };
+  });
+  const log = vi.fn();
+  const isDbAvailable = () => true;
+  return { query, log, isDbAvailable, captured };
+}
+
+function makeReq(overrides: Partial<Request> = {}): Request {
+  return {
+    method: 'POST',
+    path: '/api/gdpr/erasures',
+    originalUrl: '/api/gdpr/erasures',
+    url: '/api/gdpr/erasures',
+    headers: {},
+    socket: { remoteAddress: '127.0.0.1' },
+    body: {},
+    params: {},
+    ...overrides,
+  } as Request;
+}
+
+function makeRes() {
+  const statusCodes: number[] = [];
+  const headersSent = { value: false };
+  const statusCode = { value: 200 };
+  const setHeader = vi.fn();
+  const writeHead = vi.fn((code: number) => { statusCode.value = code; });
+  const end = vi.fn();
+  const on = vi.fn((event: string, _cb: Function) => res);
+  const removeListener = vi.fn();
+  const getHeader = vi.fn();
+  const setEncoding = vi.fn();
+  const pipe = vi.fn();
+  const unpipe = vi.fn();
+  const write = vi.fn();
+  const flushHeaders = vi.fn();
+  const toJSON = vi.fn();
+  const setTimeout = vi.fn();
+  const close = vi.fn();
+  const addListener = vi.fn();
+  const emit = vi.fn();
+  const once = vi.fn();
+  const prependListener = vi.fn();
+  const rawListeners = vi.fn();
+  const removeAllListeners = vi.fn();
+  const removeListener2 = vi.fn();
+  const listenerCount = vi.fn();
+  const eventNames = vi.fn();
+  const setMaxListeners = vi.fn();
+  const getMaxListeners = vi.fn();
+  const defaultMaxListeners = vi.fn();
+  const pause = vi.fn();
+  const resume = vi.fn();
+  const isPaused = vi.fn();
+  const unshift = vi.fn();
+  const wrap = vi.fn();
+  const push = vi.fn();
+  const destroy = vi.fn();
+  const isDestroyed = vi.fn();
+  const isReadable = vi.fn();
+  const isWritable = vi.fn();
+  const readable = vi.fn();
+  const writable = vi.fn();
+  const readableHighWaterMark = vi.fn();
+  const writableHighWaterMark = vi.fn();
+  const readableEncoding = vi.fn();
+  const writableEncoding = vi.fn();
+  const readableObjectMode = vi.fn();
+  const writableObjectMode = vi.fn();
+  const readableLength = vi.fn();
+  const writableLength = vi.fn();
+  const readableFlowing = vi.fn();
+  const writableFinalized = vi.fn();
+  const readableAborted = vi.fn();
+  const writableFinished = vi.fn();
+  const readableEnded = vi.fn();
+  const writableCorked = vi.fn();
+  const readableNeedDrain = vi.fn();
+  const writableNeedDrain2 = vi.fn();
+  const readablePaused = vi.fn();
+  const writableFinished2 = vi.fn();
+  const readableFlowing2 = vi.fn();
+  const writableFinalized2 = vi.fn();
+  const readableAborted2 = vi.fn();
+  const writableFinished3 = vi.fn();
+  const readableEnded2 = vi.fn();
+  const writableCorked2 = vi.fn();
+  const readableNeedDrain2 = vi.fn();
+  const writableNeedDrain3 = vi.fn();
+  const readablePaused2 = vi.fn();
+  const writableFinished4 = vi.fn();
+  const readableFlowing3 = vi.fn();
+  const writableFinalized3 = vi.fn();
+  const readableAborted3 = vi.fn();
+  const writableFinished5 = vi.fn();
+  const readableEnded3 = vi.fn();
+  const writableCorked3 = vi.fn();
+  const readableNeedDrain3 = vi.fn();
+  const writableNeedDrain4 = vi.fn();
+  const readablePaused3 = vi.fn();
+  const writableFinished6 = vi.fn();
+  const readableFlowing4 = vi.fn();
+  const writableFinalized4 = vi.fn();
+  const readableAborted4 = vi.fn();
+  const writableFinished7 = vi.fn();
+  const readableEnded4 = vi.fn();
+  const writableCorked4 = vi.fn();
+  const readableNeedDrain4 = vi.fn();
+  const writableNeedDrain5 = vi.fn();
+  const readablePaused4 = vi.fn();
+  const writableFinished8 = vi.fn();
+  const readableFlowing5 = vi.fn();
+  const writableFinalized5 = vi.fn();
+  const readableAborted5 = vi.fn();
+  const writableFinished9 = vi.fn();
+  const readableEnded5 = vi.fn();
+  const writableCorked5 = vi.fn();
+  const readableNeedDrain5 = vi.fn();
+  const writableNeedDrain6 = vi.fn();
+  const readablePaused5 = vi.fn();
+  const writableFinished10 = vi.fn();
+  const readableFlowing6 = vi.fn();
+  const writableFinalized6 = vi.fn();
+  const readableAborted6 = vi.fn();
+  const writableFinished11 = vi.fn();
+  const readableEnded6 = vi.fn();
+  const writableCorked6 = vi.fn();
+  const readableNeedDrain6 = vi.fn();
+  const writableNeedDrain7 = vi.fn();
+  const readablePaused6 = vi.fn();
+  const writableFinished12 = vi.fn();
+  const readableFlowing7 = vi.fn();
+  const writableFinalized7 = vi.fn();
+  const readableAborted7 = vi.fn();
+  const writableFinished13 = vi.fn();
+  const readableEnded7 = vi.fn();
+  const writableCorked7 = vi.fn();
+  const readableNeedDrain7 = vi.fn();
+  const writableNeedDrain8 = vi.fn();
+  const readablePaused7 = vi.fn();
+  const writableFinished14 = vi.fn();
+  const readableFlowing8 = vi.fn();
+  const writableFinalized8 = vi.fn();
+  const readableAborted8 = vi.fn();
+  const writableFinished15 = vi.fn();
+  const readableEnded8 = vi.fn();
+  const writableCorked8 = vi.fn();
+  const readableNeedDrain8 = vi.fn();
+  const writableNeedDrain9 = vi.fn();
+  const readablePaused8 = vi.fn();
+  const writableFinished16 = vi.fn();
+  const readableFlowing9 = vi.fn();
+  const writableFinalized9 = vi.fn();
+  const readableAborted9 = vi.fn();
+  const writableFinished17 = vi.fn();
+  const readableEnded9 = vi.fn();
+  const writableCorked9 = vi.fn();
+  const readableNeedDrain9 = vi.fn();
+  const writableNeedDrain10 = vi.fn();
+  const readablePaused9 = vi.fn();
+  const writableFinished18 = vi.fn();
+  const readableFlowing10 = vi.fn();
+  const writableFinalized10 = vi.fn();
+  const readableAborted10 = vi.fn();
+  const writableFinished19 = vi.fn();
+  const readableEnded10 = vi.fn();
+  const writableCorked10 = vi.fn();
+  const readableNeedDrain10 = vi.fn();
+  const writableNeedDrain11 = vi.fn();
+  const readablePaused10 = vi.fn();
+  const writableFinished20 = vi.fn();
+  const readableFlowing11 = vi.fn();
+  const writableFinalized11 = vi.fn();
+  const readableAborted11 = vi.fn();
+  const writableFinished21 = vi.fn();
+  const readableEnded11 = vi.fn();
+  const writableCorked11 = vi.fn();
+  const readableNeedDrain11 = vi.fn();
+  const writableNeedDrain12 = vi.fn();
+  const readablePaused11 = vi.fn();
+  const writableFinished22 = vi.fn();
+  const readableFlowing12 = vi.fn();
+  const writableFinalized12 = vi.fn();
+  const readableAborted12 = vi.fn();
+  const writableFinished23 = vi.fn();
+  const readableEnded12 = vi.fn();
+  const writableCorked12 = vi.fn();
+  const readableNeedDrain12 = vi.fn();
+  const writableNeedDrain13 = vi.fn();
+  const readablePaused12 = vi.fn();
+  const writableFinished24 = vi.fn();
+  const readableFlowing13 = vi.fn();
+  const writableFinalized13 = vi.fn();
+  const readableAborted13 = vi.fn();
+  const writableFinished25 = vi.fn();
+  const readableEnded13 = vi.fn();
+  const writableCorked13 = vi.fn();
+  const readableNeedDrain13 = vi.fn();
+  const writableNeedDrain14 = vi.fn();
+  const readablePaused13 = vi.fn();
+  const writableFinished26 = vi.fn();
+  const readableFlowing14 = vi.fn();
+  const writableFinalized14 = vi.fn();
+  const readableAborted14 = vi.fn();
+  const writableFinished27 = vi.fn();
+  const readableEnded14 = vi.fn();
+  const writableCorked14 = vi.fn();
+  const readableNeedDrain14 = vi.fn();
+  const writableNeedDrain15 = vi.fn();
+  const readablePaused14 = vi.fn();
+  const writableFinished28 = vi.fn();
+  const readableFlowing15 = vi.fn();
+  const writableFinalized15 = vi.fn();
+  const readableAborted15 = vi.fn();
+  const writableFinished29 = vi.fn();
+  const readableEnded15 = vi.fn();
+  const writableCorked15 = vi.fn();
+  const readableNeedDrain15 = vi.fn();
+  const writableNeedDrain16 = vi.fn();
+  const readablePaused15 = vi.fn();
+  const writableFinished30 = vi.fn();
+  const readableFlowing16 = vi.fn();
+  const writableFinalized16 = vi.fn();
+  const readableAborted16 = vi.fn();
+  const writableFinished31 = vi.fn();
+  const readableEnded16 = vi.fn();
+  const writableCorked16 = vi.fn();
+  const readableNeedDrain16 = vi.fn();
+  const writableNeedDrain17 = vi.fn();
+  const readablePaused16 = vi.fn();
+  const writableFinished32 = vi.fn();
+  const readableFlowing17 = vi.fn();
+  const writableFinalized17 = vi.fn();
+  const readableAborted17 = vi.fn();
+  const writableFinished33 = vi.fn();
+  const readableEnded17 = vi.fn();
+  const writableCorked17 = vi.fn();
+  const readableNeedDrain17 = vi.fn();
+  const writableNeedDrain18 = vi.fn();
+  const readablePaused17 = vi.fn();
+  const writableFinished34 = vi.fn();
+  const readableFlowing18 = vi.fn();
+  const writableFinalized18 = vi.fn();
+  const readableAborted18 = vi.fn();
+  const writableFinished35 = vi.fn();
+  const readableEnded18 = vi.fn();
+  const writableCorked18 = vi.fn();
+  const readableNeedDrain18 = vi.fn();
+  const writableNeedDrain19 = vi.fn();
+  const readablePaused18 = vi.fn();
+  const writableFinished36 = vi.fn();
+  const readableFlowing19 = vi.fn();
+  const writableFinalized19 = vi.fn();
+  const readableAborted19 = vi.fn();
+  const writableFinished37 = vi.fn();
+  const readableEnded19 = vi.fn();
+  const writableCorked19 = vi.fn();
+  const readableNeedDrain19 = vi.fn();
+  const writableNeedDrain20 = vi.fn();
+  const readablePaused19 = vi.fn();
+  const writableFinished38 = vi.fn();
+  const readableFlowing20 = vi.fn();
+  const writableFinalized20 = vi.fn();
+  const readableAborted20 = vi.fn();
+  const writableFinished39 = vi.fn();
+  const readableEnded20 = vi.fn();
+  const writableCorked20 = vi.fn();
+  const readableNeedDrain20 = vi.fn();
+  const writableNeedDrain21 = vi.fn();
+  const readablePaused20 = vi.fn();
+  const writableFinished40 = vi.fn();
+  const readableFlowing21 = vi.fn();
+  const writableFinalized21 = vi.fn();
+  const readableAborted21 = vi.fn();
+  const writableFinished41 = vi.fn();
+  const readableEnded21 = vi.fn();
+  const writableCorked21 = vi.fn();
+  const readableNeedDrain21 = vi.fn();
+  const writableNeedDrain22 = vi.fn();
+  const readablePaused21 = vi.fn();
+  const writableFinished42 = vi.fn();
+  const readableFlowing22 = vi.fn();
+  const writableFinalized22 = vi.fn();
+  const readableAborted22 = vi.fn();
+  const writableFinished43 = vi.fn();
+  const readableEnded22 = vi.fn();
+  const writableCorked22 = vi.fn();
+  const readableNeedDrain22 = vi.fn();
+  const writableNeedDrain23 = vi.fn();
+  const readablePaused22 = vi.fn();
+  const writableFinished44 = vi.fn();
+  const readableFlowing23 = vi.fn();
+  const writableFinalized23 = vi.fn();
+  const readableAborted23 = vi.fn();
+  const writableFinished45 = vi.fn();
+  const readableEnded23 = vi.fn();
+  const writableCorked23 = vi.fn();
+  const readableNeedDrain23 = vi.fn();
+  const writableNeedDrain24 = vi.fn();
+  const readablePaused23 = vi.fn();
+  const writableFinished46 = vi.fn();
+  const readableFlowing24 = vi.fn();
+  const writableFinalized24 = vi.fn();
+  const readableAborted24 = vi.fn();
+  const writableFinished47 = vi.fn();
+  const readableEnded24 = vi.fn();
+  const writableCorked24 = vi.fn();
+  const readableNeedDrain24 = vi.fn();
+  const writableNeedDrain25 = vi.fn();
+  const readablePaused24 = vi.fn();
+  const writableFinished48 = vi.fn();
+  const readableFlowing25 = vi.fn();
+  const writableFinalized25 = vi.fn();
+  const readableAborted25 = vi.fn();
+  const writableFinished49 = vi.fn();
+  const readableEnded25 = vi.fn();
+  const writableCorked25 = vi.fn();
+  const readableNeedDrain25 = vi.fn();
+  const writableNeedDrain26 = vi.fn();
+  const readablePaused25 = vi.fn();
+  const writableFinished50 = vi.fn();
+  const readableFlowing26 = vi.fn();
+  const writableFinalized26 = vi.fn();
+  const readableAborted26 = vi.fn();
+  const writableFinished51 = vi.fn();
+  const readableEnded26 = vi.fn();
+  const writableCorked26 = vi.fn();
+  const readableNeedDrain26 = vi.fn();
+  const writableNeedDrain27 = vi.fn();
+  const readablePaused26 = vi.fn();
+  const writableFinished52 = vi.fn();
+  const readableFlowing27 = vi.fn();
+  const writableFinalized27 = vi.fn();
+  const readableAborted27 = vi.fn();
+  const writableFinished53 = vi.fn();
+  const readableEnded27 = vi.fn();
+  const writableCorked27 = vi.fn();
+  const readableNeedDrain27 = vi.fn();
+  const writableNeedDrain28 = vi.fn();
+  const readablePaused27 = vi.fn();
+  const writableFinished54 = vi.fn();
+  const readableFlowing28 = vi.fn();
+  const writableFinalized28 = vi.fn();
+  const readableAborted28 = vi.fn();
+  const writableFinished55 = vi.fn();
+  const readableEnded28 = vi.fn();
+  const writableCorked28 = vi.fn();
+  const readableNeedDrain28 = vi.fn();
+  const writableNeedDrain29 = vi.fn();
+  const readablePaused28 = vi.fn();
+  const writableFinished56 = vi.fn();
+  const readableFlowing29 = vi.fn();
+  const writableFinalized29 = vi.fn();
+  const readableAborted29 = vi.fn();
+  const writableFinished57 = vi.fn();
+  const readableEnded29 = vi.fn();
+  const writableCorked29 = vi.fn();
+  const readableNeedDrain29 = vi.fn();
+  const writableNeedDrain30 = vi.fn();
+  const readablePaused29 = vi.fn();
+  const writableFinished58 = vi.fn();
+  const readableFlowing30 = vi.fn();
+  const writableFinalized30 = vi.fn();
+  const readableAborted30 = vi.fn();
+  const writableFinished59 = vi.fn();
+  const readableEnded30 = vi.fn();
+  const writableCorked30 = vi.fn();
+  const readableNeedDrain30 = vi.fn();
+  const writableNeedDrain31 = vi.fn();
+  const readablePaused30 = vi.fn();
+  const writableFinished60 = vi.fn();
+  const readableFlowing31 = vi.fn();
+  const writableFinalized31 = vi.fn();
+  const readableAborted31 = vi.fn();
+  const writableFinished61 = vi.fn();
+  const readableEnded31 = vi.fn();
+  const writableCorked31 = vi.fn();
+  const readableNeedDrain31 = vi.fn();
+  const writableNeedDrain32 = vi.fn();
+  const readablePaused31 = vi.fn();
+  const writableFinished62 = vi.fn();
+  const readableFlowing32 = vi.fn();
+  const writableFinalized32 = vi.fn();
+  const readableAborted32 = vi.fn();
+  const writableFinished63 = vi.fn();
+  const readableEnded32 = vi.fn();
+  const writableCorked32 = vi.fn();
+  const readableNeedDrain32 = vi.fn();
+  const writableNeedDrain33 = vi.fn();
+  const readablePaused32 = vi.fn();
+  const writableFinished64 = vi.fn();
+  const readableFlowing33 = vi.fn();
+  const writableFinalized33 = vi.fn();
+  const readableAborted33 = vi.fn();
+  const writableFinished65 = vi.fn();
+  const readableEnded33 = vi.fn();
+  const writableCorked33 = vi.fn();
+  const readableNeedDrain33 = vi.fn();
+  const writableNeedDrain34 = vi.fn();
+  const readablePaused33 = vi.fn();
+  const writableFinished66 = vi.fn();
+  const readableFlowing34 = vi.fn();
+  const writableFinalized34 = vi.fn();
+  const readableAborted34 = vi.fn();
+  const writableFinished67 = vi.fn();
+  const readableEnded34 = vi.fn();
+  const writableCorked34 = vi.fn();
+  const readableNeedDrain34 = vi.fn();
+  const writableNeedDrain35 = vi.fn();
+  const readablePaused34 = vi.fn();
+  const writableFinished68 = vi.fn();
+  const readableFlowing35 = vi.fn();
+  const writableFinalized35 = vi.fn();
+  const readableAborted35 = vi.fn();
+  const writableFinished69 = vi.fn();
+  const readableEnded35 = vi.fn();
+  const writableCorked35 = vi.fn();
+  const readableNeedDrain35 = vi.fn();
+  const writableNeedDrain36 = vi.fn();
+  const readablePaused35 = vi.fn();
+  const writableFinished70 = vi.fn();
+  const readableFlowing36 = vi.fn();
+  const writableFinalized36 = vi.fn();
+  const readableAborted36 = vi.fn();
+  const writableFinished71 = vi.fn();
+  const readableEnded36 = vi.fn();
+  const writableCorked36 = vi.fn();
+  const readableNeedDrain36 = vi.fn();
+  const writableNeedDrain37 = vi.fn();
+  const readablePaused36 = vi.fn();
+  const writableFinished72 = vi.fn();
+  const readableFlowing37 = vi.fn();
+  const writableFinalized37 = vi.fn();
+  const readableAborted37 = vi.fn();
+  const writableFinished73 = vi.fn();
+  const readableEnded37 = vi.fn();
+  const writableCorked37 = vi.fn();
+  const readableNeedDrain37 = vi.fn();
+  const writableNeedDrain38 = vi.fn();
+  const readablePaused37 = vi.fn();
+  const writableFinished74 = vi.fn();
+  const readableFlowing38 = vi.fn();
+  const writableFinalized38 = vi.fn();
+  const readableAborted38 = vi.fn();
+  const writableFinished75 = vi.fn();
+  const readableEnded38 = vi.fn();
+  const writableCorked38 = vi.fn();
+  const readableNeedDrain38 = vi.fn();
+  const writableNeedDrain39 = vi.fn();
+  const readablePaused38 = vi.fn();
+  const writableFinished76 = vi.fn();
+  const readableFlowing39 = vi.fn();
+  const writableFinalized39 = vi.fn();
+  const readableAborted39 = vi.fn();
+  const writableFinished77 = vi.fn();
+  const readableEnded39 = vi.fn();
+  const writableCorked39 = vi.fn();
+  const readableNeedDrain39 = vi.fn();
+  const writableNeedDrain40 = vi.fn();
+  const readablePaused39 = vi.fn();
+  const writableFinished78 = vi.fn();
+  const readableFlowing40 = vi.fn();
+  const writableFinalized40 = vi.fn();
+  const readableAborted40 = vi.fn();
+  const writableFinished79 = vi.fn();
+  const readableEnded40 = vi.fn();
+  const writableCorked40 = vi.fn();
+  const readableNeedDrain40 = vi.fn();
+  const writableNeedDrain41 = vi.fn();
+  const readablePaused40 = vi.fn();
+  const writableFinished80 = vi.fn();
+  const readableFlowing41 = vi.fn();
+  const writableFinalized41 = vi.fn();
+  const readableAborted41 = vi.fn();
+  const writableFinished81 = vi.fn();
+  const readableEnded41 = vi.fn();
+  const writableCorked41 = vi.fn();
+  const readableNeedDrain41 = vi.fn();
+  const writableNeedDrain42 = vi.fn();
+  const readablePaused41 = vi.fn();
+  const writableFinished82 = vi.fn();
+  const readableFlowing42 = vi.fn();
+  const writableFinalized42 = vi.fn();
+  const readableAborted42 = vi.fn();
+  const writableFinished83 = vi.fn();
+  const readableEnded42 = vi.fn();
+  const writableCorked42 = vi.fn();
+  const readableNeedDrain42 = vi.fn();
+  const writableNeedDrain43 = vi.fn();
+  const readablePaused42 = vi.fn();
+  const writableFinished84 = vi.fn();
+  const readableFlowing43 = vi.fn();
+  const writableFinalized43 = vi.fn();
+  const readableAborted43 = vi.fn();
+  const writableFinished85 = vi.fn();
+  const readableEnded43 = vi.fn();
+  const writableCorked43 = vi.fn();
+  const readableNeedDrain43 = vi.fn();
+  const writableNeedDrain44 = vi.fn();
+  const readablePaused43 = vi.fn();
+  const writableFinished86 = vi.fn();
+  const readableFlowing44 = vi.fn();
+  const writableFinalized44 = vi.fn();
+  const readableAborted44 = vi.fn();
+  const writableFinished87 = vi.fn();
+  const readableEnded44 = vi.fn();
+  const writableCorked44 = vi.fn();
+  const readableNeedDrain44 = vi.fn();
+  const writableNeedDrain45 = vi.fn();
+  const readablePaused44 = vi.fn();
+  const writableFinished88 = vi.fn();
+  const readableFlowing45 = vi.fn();
+  const writableFinalized45 = vi.fn();
+  const readableAborted45 = vi.fn();
+  const writableFinished89 = vi.fn();
+  const readableEnded45 = vi.fn();
+  const writableCorked45 = vi.fn();
+  const readableNeedDrain45 = vi.fn();
+  const writableNeedDrain46 = vi.fn();
+  const readablePaused45 = vi.fn();
+  const writableFinished90 = vi.fn();
+  const readableFlowing46 = vi.fn();
+  const writableFinalized46 = vi.fn();
+  const readableAborted46 = vi.fn();
+  const writableFinished91 = vi.fn();
+  const readableEnded46 = vi.fn();
+  const writableCorked46 = vi.fn();
+  const readableNeedDrain46 = vi.fn();
+  const writableNeedDrain47 = vi.fn();
+  const readablePaused46 = vi.fn();
+  const writableFinished92 = vi.fn();
+  const readableFlowing47 = vi.fn();
+  const writableFinalized47 = vi.fn();
+  const readableAborted47 = vi.fn();
+  const writableFinished93 = vi.fn();
+  const readableEnded47 = vi.fn();
+  const writableCorked47 = vi.fn();
+  const readableNeedDrain47 = vi.fn();
+  const writableNeedDrain48 = vi.fn();
+  const readablePaused47 = vi.fn();
+  const writableFinished94 = vi.fn();
+  const readableFlowing48 = vi.fn();
+  const writableFinalized48 = vi.fn();
+  const readableAborted48 = vi.fn();
+  const writableFinished95 = vi.fn();
+  const readableEnded48 = vi.fn();
+  const writableCorked48 = vi.fn();
+  const readableNeedDrain48 = vi.fn();
+  const writableNeedDrain49 = vi.fn();
+  const readablePaused48 = vi.fn();
+  const writableFinished96 = vi.fn();
+  const readableFlowing49 = vi.fn();
+  const writableFinalized49 = vi.fn();
+  const readableAborted49 = vi.fn();
+  const writableFinished97 = vi.fn();
+  const readableEnded49 = vi.fn();
+  const writableCorked49 = vi.fn();
+  const readableNeedDrain49 = vi.fn();
+  const writableNeedDrain50 = vi.fn();
+  const readablePaused49 = vi.fn();
+  const writableFinished98 = vi.fn();
+  const readableFlowing50 = vi.fn();
+  const writableFinalized50 = vi.fn();
+  const readableAborted50 = vi.fn();
+  const writableFinished99 = vi.fn();
+  const readableEnded50 = vi.fn();
+  const writableCorked50 = vi.fn();
+  const readableNeedDrain50 = vi.fn();
+  const writableNeedDrain51 = vi.fn();
+  const readablePaused50 = vi.fn();
+  const writableFinished100 = vi.fn();
+  const readableFlowing51 = vi.fn();
+  const writableFinalized51 = vi.fn();
+  const readableAborted51 = vi.fn();
+  const writableFinished101 = vi.fn();
+  const readableEnded51 = vi.fn();
+  const writableCorked51 = vi.fn();
+  const readableNeedDrain51 = vi.fn();
+  const writableNeedDrain52 = vi.fn();
+  const readablePaused51 = vi.fn();
+  const writableFinished102 = vi.fn();
+  const readableFlowing52 = vi.fn();
+  const writableFinalized52 = vi.fn();
+  const readableAborted52 = vi.fn();
+  const writableFinished103 = vi.fn();
+  const readableEnded52 = vi.fn();
+  const writableCorked52 = vi.fn();
+  const readableNeedDrain52 = vi.fn();
+  const writableNeedDrain53 = vi.fn();
+  const readablePaused52 = vi.fn();
+  const writableFinished104 = vi.fn();
+  const readableFlowing53 = vi.fn();
+  const writableFinalized53 = vi.fn();
+  const readableAborted53 = vi.fn();
+  const writableFinished105 = vi.fn();
+  const readableEnded53 = vi.fn();
+  const writableCorked53 = vi.fn();
+  const readableNeedDrain53 = vi.fn();
+  const writableNeedDrain54 = vi.fn();
+  const readablePaused53 = vi.fn();
+  const writableFinished106 = vi.fn();
+  const readableFlowing54 = vi.fn();
+  const writableFinalized54 = vi.fn();
+  const readableAborted54 = vi.fn();
+  const writableFinished107 = vi.fn();
+  const readableEnded54 = vi.fn();
+  const writableCorked54 = vi.fn();
+  const readableNeedDrain54 = vi.fn();
+  const writableNeedDrain55 = vi.fn();
+  const readablePaused54 = vi.fn();
+  const writableFinished108 = vi.fn();
+  const readableFlowing55 = vi.fn();
+  const writableFinalized55 = vi.fn();
+  const readableAborted55 = vi.fn();
+  const writableFinished109 = vi.fn();
+  const readableEnded55 = vi.fn();
+  const writableCorked55 = vi.fn();
+  const readableNeedDrain55 = vi.fn();
+  const writableNeedDrain56 = vi.fn();
+  const readablePaused55 = vi.fn();
+  const writableFinished110 = vi.fn();
+  const readableFlowing56 = vi.fn();
+  const writableFinalized56 = vi.fn();
+  const readableAborted56 = vi.fn();
+  const writableFinished111 = vi.fn();
+  const readableEnded56 = vi.fn();
+  const writableCorked56 = vi.fn();
+  const readableNeedDrain56 = vi.fn();
+  const writableNeedDrain57 = vi.fn();
+  const readablePaused56 = vi.fn();
+  const writableFinished112 = vi.fn();
+  const readableFlowing57 = vi.fn();
+  const writableFinalized57 = vi.fn();
+  const readableAborted57 = vi.fn();
+  const writableFinished113 = vi.fn();
+  const readableEnded57 = vi.fn();
+  const writableCorked57 = vi.fn();
+  const readableNeedDrain57 = vi.fn();
+  const writableNeedDrain58 = vi.fn();
+  const readablePaused57 = vi.fn();
+  const writableFinished114 = vi.fn();
+  const readableFlowing58 = vi.fn();
+  const writableFinalized58 = vi.fn();
+  const readableAborted58 = vi.fn();
+  const writableFinished115 = vi.fn();
+  const readableEnded58 = vi.fn();
+  const writableCorked58 = vi.fn();
+  const readableNeedDrain58 = vi.fn();
+  const writableNeedDrain59 = vi.fn();
+  const readablePaused58 = vi.fn();
+  const writableFinished116 = vi.fn();
+  const readableFlowing59 = vi.fn();
+  const writableFinalized59 = vi.fn();
+  const readableAborted59 = vi.fn();
+  const writableFinished117 = vi.fn();
+  const readableEnded59 = vi.fn();
+  const writableCorked59 = vi.fn();
+  const readableNeedDrain59 = vi.fn();
+  const writableNeedDrain60 = vi.fn();
+  const readablePaused59 = vi.fn();
+  const writableFinished118 = vi.fn();
+  const readableFlowing60 = vi.fn();
+  const writableFinalized60 = vi.fn();
+  const readableAborted60 = vi.fn();
+  const writableFinished119 = vi.fn();
+  const readableEnded60 = vi.fn();
+  const writableCorked60 = vi.fn();
+  const readableNeedDrain60 = vi.fn();
+  const writableNeedDrain61 = vi.fn();
+  const readablePaused60 = vi.fn();
+  const writableFinished120 = vi.fn();
+  const readableFlowing61 = vi.fn();
+  const writableFinalized61 = vi.fn();
+  const readableAborted61 = vi.fn();
+  const writableFinished121 = vi.fn();
+  const readableEnded61 = vi.fn();
+  const writableCorked61 = vi.fn();
+  const readableNeedDrain61 = vi.fn();
+  const writableNeedDrain62 = vi.fn();
+  const readablePaused61 = vi.fn();
+  const writableFinished122 = vi.fn();
+  const readableFlowing62 = vi.fn();
+  const writableFinalized62 = vi.fn();
+  const readableAborted62 = vi.fn();
+  const writableFinished123 = vi.fn();
+  const readableEnded62 = vi.fn();
+  const writableCorked62 = vi.fn();
+  const readableNeedDrain62 = vi.fn();
+  const writableNeedDrain63 = vi.fn();
+  const readablePaused62 = vi.fn();
+  const writableFinished124 = vi.fn();
+  const readableFlowing63 = vi.fn();
+  const writableFinalized63 = vi.fn();
+  const readableAborted63 = vi.fn();
+  const writableFinished125 = vi.fn();
+  const readableEnded63 = vi.fn();
+  const writableCorked63 = vi.fn();
+  const readableNeedDrain63 = vi.fn();
+  const writableNeedDrain64 = vi.fn();
+  const readablePaused63 = vi.fn();
+  const writableFinished126 = vi.fn();
+  const readableFlowing64 = vi.fn();
+  const writableFinalized64 = vi.fn();
+  const readableAborted64 = vi.fn();
+  const writableFinished127 = vi.fn();
+  const readableEnded64 = vi.fn();
+  const writableCorked64 = vi.fn();
+  const readableNeedDrain64 = vi.fn();
+  const writableNeedDrain65 = vi.fn();
+  const readablePaused64 = vi.fn();
+  const writableFinished128 = vi.fn();
+  const readableFlowing65 = vi.fn();
+  const writableFinalized65 = vi.fn();
+  const readableAborted65 = vi.fn();
+  const writableFinished129 = vi.fn();
+  const readableEnded65 = vi.fn();
+  const writableCorked65 = vi.fn();
+  const readableNeedDrain65 = vi.fn();
+  const writableNeedDrain66 = vi.fn();
+  const readablePaused65 = vi.fn();
+  const writableFinished130 = vi.fn();
+  const readableFlowing66 = vi.fn();
+  const writableFinalized66 = vi.fn();
+  const readableAborted66 = vi.fn();
+  const writableFinished131 = vi.fn();
+  const readableEnded66 = vi.fn();
+  const writableCorked66 = vi.fn();
+  const readableNeedDrain66 = vi.fn();
+  const writableNeedDrain67 = vi.fn();
+  const readablePaused66 = vi.fn();
+  const writableFinished132 = vi.fn();
+  const readableFlowing67 = vi.fn();
+  const writableFinalized67 = vi.fn();
+  const readableAborted67 = vi.fn();
+  const writableFinished133 = vi.fn();
+  const readableEnded67 = vi.fn();
+  const writableCorked67 = vi.fn();
+  const readableNeedDrain67 = vi.fn();
+  const writableNeedDrain68 = vi.fn();
+  const readablePaused67 = vi.fn();
+  const writableFinished134 = vi.fn();
+  const readableFlowing68 = vi.fn();
+  const writableFinalized68 = vi.fn();
+  const readableAborted68 = vi.fn();
+  const writableFinished135 = vi.fn();
+  const readableEnded68 = vi.fn();
+  const writableCorked68 = vi.fn();
+  const readableNeedDrain68 = vi.fn();
+  const writableNeedDrain69 = vi.fn();
+  const readablePaused68 = vi.fn();
+  const writableFinished136 = vi.fn();
+  const readableFlowing69 = vi.fn();
+  const writableFinalized69 = vi.fn();
+  const readableAborted69 = vi.fn();
+  const writableFinished137 = vi.fn();
+  const readableEnded69 = vi.fn();
+  const writableCorked69 = vi.fn();
+  const readableNeedDrain69 = vi.fn();
+  const writableNeedDrain70 = vi.fn();
+  const readablePaused69 = vi.fn();
+  const writableFinished138 = vi.fn();
+  const readableFlowing70 = vi.fn();
+  const writableFinalized70 = vi.fn();
+  const readableAborted70 = vi.fn();
+  const writableFinished139 = vi.fn();
+  const readableEnded70 = vi.fn();
+  const writableCorked70 = vi.fn();
+  const readableNeedDrain70 = vi.fn();
+  const writableNeedDrain71 = vi.fn();
+  const readablePaused70 = vi.fn();
+  const writableFinished140 = vi.fn();
+  const readableFlowing71 = vi.fn();
+  const writableFinalized71 = vi.fn();
+  const readableAborted71 = vi.fn();
+  const writableFinished141 = vi.fn();
+  const readableEnded71 = vi.fn();
+  const writableCorked71 = vi.fn();
+  const readableNeedDrain71 = vi.fn();
+  const writableNeedDrain72 = vi.fn();
+  const readablePaused71 = vi.fn();
+  const writableFinished142 = vi.fn();
+  const readableFlowing72 = vi.fn();
+  const writableFinalized72 = vi.fn();
+  const readableAborted72 = vi.fn();
+  const writableFinished143 = vi.fn();
+  const readableEnded72 = vi.fn();
+  const writableCorked72 = vi.fn();
+  const readableNeedDrain72 = vi.fn();
+  const writableNeedDrain73 = vi.fn();
+  const readablePaused72 = vi.fn();
+  const writableFinished144 = vi.fn();
+  const readableFlowing73 = vi.fn();
+  const writableFinalized73 = vi.fn();
+  const readableAborted73 = vi.fn();
+  const writableFinished145 = vi.fn();
+  const readableEnded73 = vi.fn();
+  const writableCorked73 = vi.fn();
+  const readableNeedDrain73 = vi.fn();
+  const writableNeedDrain74 = vi.fn();
+  const readablePaused73 = vi.fn();
+  const writableFinished146 = vi.fn();
+  const readableFlowing74 = vi.fn();
+  const writableFinalized74 = vi.fn();
+  const readableAborted74 = vi.fn();
+  const writableFinished147 = vi.fn();
+  const readableEnded74 = vi.fn();
+  const writableCorked74 = vi.fn();
+  const readableNeedDrain74 = vi.fn();
+  const writableNeedDrain75 = vi.fn();
+  const readablePaused74 = vi.fn();
+  const writableFinished148 = vi.fn();
+  const readableFlowing75 = vi.fn();
+  const writableFinalized75 = vi.fn();
+  const readableAborted75 = vi.fn();
+  const writableFinished149 = vi.fn();
+  const readableEnded75 = vi.fn();
+  const writableCorked75 = vi.fn();
+  const readableNeedDrain75 = vi.fn();
+  const writableNeedDrain76 = vi.fn();
+  const readablePaused75 = vi.fn();
+  const writableFinished150 = vi.fn();
+  const readableFlowing76 = vi.fn();
+  const writableFinalized76 = vi.fn();
+  const readableAborted76 = vi.fn();
+  const writableFinished151 = vi.fn();
+  const readableEnded76 = vi.fn();
+  const writableCorked76 = vi.fn();
+  const readableNeedDrain76 = vi.fn();
+  const writableNeedDrain77 = vi.fn();
+  const readablePaused76 = vi.fn();
+  const writableFinished152 = vi.fn();
+  const readableFlowing77 = vi.fn();
+  const writableFinalized77 = vi.fn();
+  const readableAborted77 = vi.fn();
+  const writableFinished153 = vi.fn();
+  const readableEnded77 = vi.fn();
+  const writableCorked77 = vi.fn();
+  const readableNeedDrain77 = vi.fn();
+  const writableNeedDrain78 = vi.fn();
+  const readablePaused77 = vi.fn();
+  const writableFinished154 = vi.fn();
+  const readableFlowing78 = vi.fn();
+  const writableFinalized78 = vi.fn();
+  const readableAborted78 = vi.fn();
+  const writableFinished155 = vi.fn();
+  const readableEnded78 = vi.fn();
+  const writableCorked78 = vi.fn();
+  const readableNeedDrain78 = vi.fn();
+  const writableNeedDrain79 = vi.fn();
+  const readablePaused78 = vi.fn();
+  const writableFinished156 = vi.fn();
+  const readableFlowing79 = vi.fn();
+  const writableFinalized79 = vi.fn();
+  const readableAborted79 = vi.fn();
+  const writableFinished157 = vi.fn();
+  const readableEnded79 = vi.fn();
+  const writableCorked79 = vi.fn();
+  const readableNeedDrain79 = vi.fn();
+  const writableNeedDrain80 = vi.fn();
+  const readablePaused79 = vi.fn();
+  const writableFinished158 = vi.fn();
+  const readableFlowing80 = vi.fn();
+  const writableFinalized80 = vi.fn();
+  const readableAborted80 = vi.fn();
+  const writableFinished159 = vi.fn();
+  const readableEnded80 = vi.fn();
+  const writableCorked80 = vi.fn();
+  const readableNeedDrain80 = vi.fn();
+  const writableNeedDrain81 = vi.fn();
+  const readablePaused80 = vi.fn();
+  const writableFinished160 = vi.fn();
+  const readableFlowing81 = vi.fn();
+  const writableFinalized81 = vi.fn();
+  const readableAborted81 = vi.fn();
+  const writableFinished161 = vi.fn();
+  const readableEnded81 = vi.fn();
+  const writableCorked81 = vi.fn();
+  const readableNeedDrain81 = vi.fn();
+  const writableNeedDrain82 = vi.fn();
+  const readablePaused81 = vi.fn();
+  const writableFinished162 = vi.fn();
+  const readableFlowing82 = vi.fn();
+  const writableFinalized82 = vi.fn();
+  const readableAborted82 = vi.fn();
+  const writableFinished163 = vi.fn();
+  const readableEnded82 = vi.fn();
+  const writableCorked82 = vi.fn();
+  const readableNeedDrain82 = vi.fn();
+  const writableNeedDrain83 = vi.fn();
+  const readablePaused82 = vi.fn();
+  const writableFinished164 = vi.fn();
+  const readableFlowing83 = vi.fn();
+  const writableFinalized83 = vi.fn();
+  const readableAborted83 = vi.fn();
+  const writableFinished165 = vi.fn();
+  const readableEnded83 = vi.fn();
+  const writableCorked83 = vi.fn();
+  const readableNeedDrain83 = vi.fn();
+  const writableNeedDrain84 = vi.fn();
+  const readablePaused83 = vi.fn();
+  const writableFinished166 = vi.fn();
+  const readableFlowing84 = vi.fn();
+  const writableFinalized84 = vi.fn();
+  const readableAborted84 = vi.fn();
+  const writableFinished167 = vi.fn();
+  const readableEnded84 = vi.fn();
+  const writableCorked84 = vi.fn();
+  const readableNeedDrain84 = vi.fn();
+  const writableNeedDrain85 = vi.fn();
+  const readablePaused84 = vi.fn();
+  const writableFinished168 = vi.fn();
+  const readableFlowing85 = vi.fn();
+  const writableFinalized85 = vi.fn();
+  const readableAborted85 = vi.fn();
+  const writableFinished169 = vi.fn();
+  const readableEnded85 = vi.fn();
+  const writableCorked85 = vi.fn();
+  const readableNeedDrain85 = vi.fn();
+  const writableNeedDrain86 = vi.fn();
+  const readablePaused85 = vi.fn();
+  const writableFinished170 = vi.fn();
+  const readableFlowing86 = vi.fn();
+  const writableFinalized86 = vi.fn();
+  const readableAborted86 = vi.fn();
+  const writableFinished171 = vi.fn();
+  const readableEnded86 = vi.fn();
+  const writableCorked86 = vi.fn();
+  const readableNeedDrain86 = vi.fn();
+  const writableNeedDrain87 = vi.fn();
+  const readablePaused86 = vi.fn();
+  const writableFinished172 = vi.fn();
+  const readableFlowing87 = vi.fn();
+  const writableFinalized87 = vi.fn();
+  const readableAborted87 = vi.fn();
+  const writableFinished173 = vi.fn();
+  const readableEnded87 = vi.fn();
+  const writableCorked87 = vi.fn();
+  const readableNeedDrain87 = vi.fn();
+  const writableNeedDrain88 = vi.fn();
+  const readablePaused87 = vi.fn();
+  const writableFinished174 = vi.fn();
+  const readableFlowing88 = vi.fn();
+  const writableFinalized88 = vi.fn();
+  const readableAborted88 = vi.fn();
+  const writableFinished175 = vi.fn();
+  const readableEnded88 = vi.fn();
+  const writableCorked88 = vi.fn();
+  const readableNeedDrain88 = vi.fn();
+  const writableNeedDrain89 = vi.fn();
+  const readablePaused88 = vi.fn();
+  const writableFinished176 = vi.fn();
+  const readableFlowing89 = vi.fn();
+  const writableFinalized89 = vi.fn();
+  const readableAborted89 = vi.fn();
+  const writableFinished177 = vi.fn();
+  const readableEnded89 = vi.fn();
+  const writableCorked89 = vi.fn();
+  const readableNeedDrain89 = vi.fn();
+  const writableNeedDrain90 = vi.fn();
+  const readablePaused89 = vi.fn();
+  const writableFinished178 = vi.fn();
+  const readableFlowing90 = vi.fn();
+  const writableFinalized90 = vi.fn();
+  const readableAborted90 = vi.fn();
+  const writableFinished179 = vi.fn();
+  const readableEnded90 = vi.fn();
+  const writableCorked90 = vi.fn();
+  const readableNeedDrain90 = vi.fn();
+  const writableNeedDrain91 = vi.fn();
+  const readablePaused90 = vi.fn();
+  const writableFinished180 = vi.fn();
+  const readableFlowing91 = vi.fn();
+  const writableFinalized91 = vi.fn();
+  const readableAborted91 = vi.fn();
+  const writableFinished181 = vi.fn();
+  const readableEnded91 = vi.fn();
+  const writableCorked91 = vi.fn();
+  const readableNeedDrain91 = vi.fn();
+  const writableNeedDrain92 = vi.fn();
+  const readablePaused91 = vi.fn();
+  const writableFinished182 = vi.fn();
+  const readableFlowing92 = vi.fn();
+  const writableFinalized92 = vi.fn();
+  const readableAborted92 = vi.fn();
+  const writableFinished183 = vi.fn();
+  const readableEnded92 = vi.fn();
+  const writableCorked92 = vi.fn();
+  const readableNeedDrain92 = vi.fn();
+  const writableNeedDrain93 = vi.fn();
+  const readablePaused92 = vi.fn();
+  const writableFinished184 = vi.fn();
+  const readableFlowing93 = vi.fn();
+  const writableFinalized93 = vi.fn();
+  const readableAborted93 = vi.fn();
+  const writableFinished185 = vi.fn();
+  const readableEnded93 = vi.fn();
+  const writableCorked93 = vi.fn();
+  const readableNeedDrain93 = vi.fn();
+  const writableNeedDrain94 = vi.fn();
+  const readablePaused93 = vi.fn();
+  const writableFinished186 = vi.fn();
+  const readableFlowing94 = vi.fn();
+  const writableFinalized94 = vi.fn();
+  const readableAborted94 = vi.fn();
+  const writableFinished187 = vi.fn();
+  const readableEnded94 = vi.fn();
+  const writableCorked94 = vi.fn();
+  const readableNeedDrain94 = vi.fn();
+  const writableNeedDrain95 = vi.fn();
+  const readablePaused94 = vi.fn();
+  const writableFinished188 = vi.fn();
+  const readableFlowing95 = vi.fn();
+  const writableFinalized95 = vi.fn();
+  const readableAborted95 = vi.fn();
+  const writableFinished189 = vi.fn();
+  const readableEnded95 = vi.fn();
+  const writableCorked95 = vi.fn();
+  const readableNeedDrain95 = vi.fn();
+  const writableNeedDrain96 = vi.fn();
+  const readablePaused95 = vi.fn();
+  const writableFinished190 = vi.fn();
+  const readableFlowing96 = vi.fn();
+  const writableFinalized96 = vi.fn();
+  const readableAborted96 = vi.fn();
+  const writableFinished191 = vi.fn();
+  const readableEnded96 = vi.fn();
+  const writableCorked96 = vi.fn();
+  const readableNeedDrain96 = vi.fn();
+  const writableNeedDrain97 = vi.fn();
+  const readablePaused96 = vi.fn();
+  const writableFinished192 = vi.fn();
+  const readableFlowing97 = vi.fn();
+  const writableFinalized97 = vi.fn();
+  const readableAborted97 = vi.fn();
+  const writableFinished193 = vi.fn();
+  const readableEnded97 = vi.fn();
+  const writableCorked97 = vi.fn();
+  const readableNeedDrain97 = vi.fn();
+  const writableNeedDrain98 = vi.fn();
+  const readablePaused97 = vi.fn();
+  const writableFinished194 = vi.fn();
+  const readableFlowing98 = vi.fn();
+  const writableFinalized98 = vi.fn();
+  const readableAborted98 = vi.fn();
+  const writableFinished195 = vi.fn();
+  const readableEnded98 = vi.fn();
+  const writableCorked98 = vi.fn();
+  const readableNeedDrain98 = vi.fn();
+  const writableNeedDrain99 = vi.fn();
+  const readablePaused98 = vi.fn();
+  const writableFinished196 = vi.fn();
+  const readableFlowing99 = vi.fn();
+  const writableFinalized99 = vi.fn();
+  const readableAborted99 = vi.fn();
+  const writableFinished197 = vi.fn();
+  const readableEnded99 = vi.fn();
+  const writableCorked99 = vi.fn();
+  const readableNeedDrain99 = vi.fn();
+  const writableNeedDrain100 = vi.fn();
+  const readablePaused99 = vi.fn();
+  const writableFinished200 = vi.fn();
+  const res = {
+    statusCode: 403,
+    headersSent: false,
+    getHeader: vi.fn(),
+    setHeader: vi.fn(),
+    writeHead: vi.fn(),
+    end: vi.fn(),
+    json: vi.fn(),
+    send: vi.fn(),
+    status: vi.fn(),
+    type: vi.fn(),
+    format: vi.fn(),
+    append: vi.fn(),
+    clearCookie: vi.fn(),
+    cookie: vi.fn(),
+    download: vi.fn(),
+    etag: vi.fn(),
+    expires: vi.fn(),
+    fixedPath: vi.fn(),
+    fixedStatus: vi.fn(),
+    get: vi.fn(),
+    link: vi.fn(),
+    location: vi.fn(),
+    redirect: vi.fn(),
+    render: vi.fn(),
+    sendFile: vi.fn(),
+    sendStatus: vi.fn(),
+    set: vi.fn(),
+    status: vi.fn(),
+    vary: vi.fn(),
+    write: vi.fn(),
+    writeHead: vi.fn(),
+    on: vi.fn(),
+    removeListener: vi.fn(),
+    once: vi.fn(),
+    emit: vi.fn(),
+    addListener: vi.fn(),
+    prependListener: vi.fn(),
+    prependOnceListener: vi.fn(),
+    rawListeners: vi.fn(),
+    removeAllListeners: vi.fn(),
+    removeListener: vi.fn(),
+    listenerCount: vi.fn(),
+    eventNames: vi.fn(),
+    setMaxListeners: vi.fn(),
+    getMaxListeners: vi.fn(),
+    defaultMaxListeners: vi.fn(),
+    pause: vi.fn(),
+    resume: vi.fn(),
+    isPaused: vi.fn(),
+    unshift: vi.fn(),
+    wrap: vi.fn(),
+    push: vi.fn(),
+    destroy: vi.fn(),
+    isDestroyed: vi.fn(),
+    isReadable: vi.fn(),
+    isWritable: vi.fn(),
+    readable: vi.fn(),
+    writable: vi.fn(),
+    readableHighWaterMark: vi.fn(),
+    writableHighWaterMark: vi.fn(),
+    readableEncoding: vi.fn(),
+    writableEncoding: vi.fn(),
+    readableObjectMode: vi.fn(),
+    writableObjectMode: vi.fn(),
+    readableLength: vi.fn(),
+    writableLength: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
+    readableFlowing: vi.fn(),
+    writableFinalized: vi.fn(),
+    readableAborted: vi.fn(),
+    writableFinished: vi.fn(),
+    readableEnded: vi.fn(),
+    writableCorked: vi.fn(),
+    readableNeedDrain: vi.fn(),
+    writableNeedDrain: vi.fn(),
+    readablePaused: vi.fn(),
+    writableFinished: vi.fn(),
